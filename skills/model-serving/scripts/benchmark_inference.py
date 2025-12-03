#!/usr/bin/env python3
"""
LLM Inference Benchmarking Script

Measures throughput, latency, and token generation speed for LLM serving endpoints.
Supports vLLM, TGI, and OpenAI-compatible APIs.
"""

import asyncio
import time
import argparse
import numpy as np
from typing import List, Dict
import aiohttp
import json

class BenchmarkResults:
    def __init__(self):
        self.latencies: List[float] = []
        self.tokens_generated: List[int] = []
        self.errors: int = 0
        self.start_time: float = 0
        self.end_time: float = 0

    def add_result(self, latency: float, tokens: int = 0):
        self.latencies.append(latency)
        if tokens > 0:
            self.tokens_generated.append(tokens)

    def add_error(self):
        self.errors += 1

    def print_summary(self):
        if not self.latencies:
            print("No successful requests")
            return

        latencies_ms = np.array(self.latencies) * 1000
        duration = self.end_time - self.start_time

        print("\n" + "="*60)
        print("BENCHMARK RESULTS")
        print("="*60)

        print(f"\nThroughput:")
        print(f"  Total requests: {len(self.latencies)}")
        print(f"  Successful: {len(self.latencies)}")
        print(f"  Failed: {self.errors}")
        print(f"  Duration: {duration:.2f}s")
        print(f"  Requests/sec: {len(self.latencies) / duration:.2f}")

        print(f"\nLatency (ms):")
        print(f"  Mean: {np.mean(latencies_ms):.2f}")
        print(f"  Median (P50): {np.percentile(latencies_ms, 50):.2f}")
        print(f"  P95: {np.percentile(latencies_ms, 95):.2f}")
        print(f"  P99: {np.percentile(latencies_ms, 99):.2f}")
        print(f"  Min: {np.min(latencies_ms):.2f}")
        print(f"  Max: {np.max(latencies_ms):.2f}")

        if self.tokens_generated:
            total_tokens = sum(self.tokens_generated)
            print(f"\nToken Generation:")
            print(f"  Total tokens: {total_tokens}")
            print(f"  Tokens/sec: {total_tokens / duration:.2f}")
            print(f"  Avg tokens/request: {np.mean(self.tokens_generated):.1f}")

async def benchmark_openai_compatible(
    endpoint: str,
    model: str,
    prompt: str,
    num_requests: int,
    concurrency: int,
    max_tokens: int = 128
) -> BenchmarkResults:
    """
    Benchmark OpenAI-compatible API (vLLM, TGI, OpenAI).
    """
    results = BenchmarkResults()

    async def send_request(session: aiohttp.ClientSession, request_id: int):
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": f"{prompt} (request {request_id})"}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }

        start = time.time()
        try:
            async with session.post(endpoint, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    latency = time.time() - start

                    # Extract tokens from response
                    tokens = data.get("usage", {}).get("completion_tokens", 0)

                    results.add_result(latency, tokens)
                else:
                    results.add_error()
        except Exception as e:
            print(f"Request {request_id} failed: {e}")
            results.add_error()

    # Create session
    async with aiohttp.ClientSession() as session:
        results.start_time = time.time()

        # Run requests in batches with concurrency limit
        semaphore = asyncio.Semaphore(concurrency)

        async def bounded_request(request_id):
            async with semaphore:
                await send_request(session, request_id)

        tasks = [bounded_request(i) for i in range(num_requests)]
        await asyncio.gather(*tasks)

        results.end_time = time.time()

    return results

async def benchmark_streaming(
    endpoint: str,
    model: str,
    prompt: str,
    num_requests: int,
    max_tokens: int = 128
) -> Dict[str, float]:
    """
    Benchmark streaming endpoints (measure TTFT and inter-token latency).
    """
    ttft_list = []  # Time to first token
    inter_token_latencies = []

    async with aiohttp.ClientSession() as session:
        for i in range(num_requests):
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": f"{prompt} (request {i})"}],
                "max_tokens": max_tokens,
                "stream": True
            }

            request_start = time.time()
            first_token_received = False
            last_token_time = request_start
            token_count = 0

            try:
                async with session.post(endpoint, json=payload) as response:
                    async for line in response.content:
                        if not line:
                            continue

                        line = line.decode('utf-8').strip()
                        if not line.startswith("data: "):
                            continue

                        data_str = line[6:]  # Remove "data: " prefix
                        if data_str == "[DONE]":
                            break

                        try:
                            data = json.loads(data_str)
                        except json.JSONDecodeError:
                            continue

                        current_time = time.time()

                        if not first_token_received:
                            # Time to first token
                            ttft = current_time - request_start
                            ttft_list.append(ttft)
                            first_token_received = True
                        else:
                            # Inter-token latency
                            inter_token = current_time - last_token_time
                            inter_token_latencies.append(inter_token)

                        last_token_time = current_time
                        token_count += 1

            except Exception as e:
                print(f"Streaming request {i} failed: {e}")

    # Print streaming metrics
    print("\n" + "="*60)
    print("STREAMING METRICS")
    print("="*60)

    if ttft_list:
        ttft_ms = np.array(ttft_list) * 1000
        print(f"\nTime to First Token (TTFT):")
        print(f"  Mean: {np.mean(ttft_ms):.2f}ms")
        print(f"  Median: {np.percentile(ttft_ms, 50):.2f}ms")
        print(f"  P95: {np.percentile(ttft_ms, 95):.2f}ms")

    if inter_token_latencies:
        inter_ms = np.array(inter_token_latencies) * 1000
        print(f"\nInter-Token Latency:")
        print(f"  Mean: {np.mean(inter_ms):.2f}ms")
        print(f"  Median: {np.percentile(inter_ms, 50):.2f}ms")
        print(f"  P95: {np.percentile(inter_ms, 95):.2f}ms")

    return {
        "ttft_mean": np.mean(ttft_list) if ttft_list else 0,
        "inter_token_mean": np.mean(inter_token_latencies) if inter_token_latencies else 0
    }

def main():
    parser = argparse.ArgumentParser(description="Benchmark LLM inference endpoints")

    parser.add_argument(
        "--endpoint",
        type=str,
        required=True,
        help="API endpoint (e.g., http://localhost:8000/v1/chat/completions)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="meta-llama/Llama-3.1-8B-Instruct",
        help="Model name"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="Explain quantum computing in simple terms",
        help="Test prompt"
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=100,
        help="Total number of requests"
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=10,
        help="Concurrent requests"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=128,
        help="Maximum tokens to generate"
    )
    parser.add_argument(
        "--streaming",
        action="store_true",
        help="Benchmark streaming (TTFT, inter-token latency)"
    )

    args = parser.parse_args()

    print("LLM Inference Benchmark")
    print("="*60)
    print(f"Endpoint: {args.endpoint}")
    print(f"Model: {args.model}")
    print(f"Requests: {args.requests}")
    print(f"Concurrency: {args.concurrency}")
    print(f"Max tokens: {args.max_tokens}")
    print("="*60)

    if args.streaming:
        # Streaming benchmark
        asyncio.run(benchmark_streaming(
            args.endpoint,
            args.model,
            args.prompt,
            args.requests,
            args.max_tokens
        ))
    else:
        # Throughput/latency benchmark
        results = asyncio.run(benchmark_openai_compatible(
            args.endpoint,
            args.model,
            args.prompt,
            args.requests,
            args.concurrency,
            args.max_tokens
        ))
        results.print_summary()

if __name__ == "__main__":
    main()
