#!/usr/bin/env python3
"""
Benchmark API endpoints

Usage:
    python benchmark_endpoints.py http://localhost:8000 --requests 1000 --concurrency 10

Load tests API endpoints and reports performance metrics.
"""

import sys
import time
import asyncio
import statistics
from urllib.parse import urljoin
from dataclasses import dataclass
from typing import List, Dict
import argparse


@dataclass
class RequestResult:
    """Result of a single request"""
    status_code: int
    duration_ms: float
    error: str | None = None


@dataclass
class EndpointStats:
    """Statistics for an endpoint"""
    endpoint: str
    method: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    avg_duration_ms: float
    min_duration_ms: float
    max_duration_ms: float
    p50_duration_ms: float
    p95_duration_ms: float
    p99_duration_ms: float
    requests_per_second: float


async def make_request(session, method: str, url: str) -> RequestResult:
    """Make a single HTTP request"""
    start_time = time.time()

    try:
        async with session.request(method, url) as response:
            await response.read()
            duration_ms = (time.time() - start_time) * 1000

            return RequestResult(
                status_code=response.status,
                duration_ms=duration_ms
            )
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        return RequestResult(
            status_code=0,
            duration_ms=duration_ms,
            error=str(e)
        )


async def benchmark_endpoint(
    base_url: str,
    endpoint: str,
    method: str = "GET",
    num_requests: int = 100,
    concurrency: int = 10
) -> EndpointStats:
    """Benchmark a single endpoint"""
    try:
        import aiohttp
    except ImportError:
        print("Error: aiohttp not installed. Install with: pip install aiohttp")
        sys.exit(1)

    url = urljoin(base_url, endpoint)

    print(f"\nBenchmarking {method} {endpoint}")
    print(f"  Requests: {num_requests}, Concurrency: {concurrency}")

    results: List[RequestResult] = []

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        # Run requests in batches (concurrency)
        for i in range(0, num_requests, concurrency):
            batch_size = min(concurrency, num_requests - i)
            tasks = [
                make_request(session, method, url)
                for _ in range(batch_size)
            ]

            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)

            # Progress indicator
            completed = min(i + concurrency, num_requests)
            print(f"  Progress: {completed}/{num_requests} requests", end="\r")

    total_duration = time.time() - start_time

    print()  # New line after progress

    # Calculate statistics
    successful_results = [r for r in results if 200 <= r.status_code < 300]
    failed_results = [r for r in results if r.status_code == 0 or r.status_code >= 400]

    durations = [r.duration_ms for r in successful_results]

    if not durations:
        print("  ❌ No successful requests")
        return EndpointStats(
            endpoint=endpoint,
            method=method,
            total_requests=num_requests,
            successful_requests=0,
            failed_requests=len(failed_results),
            avg_duration_ms=0,
            min_duration_ms=0,
            max_duration_ms=0,
            p50_duration_ms=0,
            p95_duration_ms=0,
            p99_duration_ms=0,
            requests_per_second=0
        )

    avg_duration = statistics.mean(durations)
    min_duration = min(durations)
    max_duration = max(durations)

    # Percentiles
    sorted_durations = sorted(durations)
    p50 = sorted_durations[int(len(sorted_durations) * 0.50)]
    p95 = sorted_durations[int(len(sorted_durations) * 0.95)]
    p99 = sorted_durations[int(len(sorted_durations) * 0.99)]

    requests_per_second = num_requests / total_duration

    return EndpointStats(
        endpoint=endpoint,
        method=method,
        total_requests=num_requests,
        successful_requests=len(successful_results),
        failed_requests=len(failed_results),
        avg_duration_ms=avg_duration,
        min_duration_ms=min_duration,
        max_duration_ms=max_duration,
        p50_duration_ms=p50,
        p95_duration_ms=p95,
        p99_duration_ms=p99,
        requests_per_second=requests_per_second
    )


def print_stats(stats: List[EndpointStats]):
    """Print benchmark results"""
    print("\n" + "="*80)
    print("Benchmark Results")
    print("="*80 + "\n")

    for stat in stats:
        print(f"{stat.method} {stat.endpoint}")
        print(f"  Total Requests:     {stat.total_requests}")
        print(f"  Successful:         {stat.successful_requests} ({stat.successful_requests/stat.total_requests*100:.1f}%)")
        print(f"  Failed:             {stat.failed_requests} ({stat.failed_requests/stat.total_requests*100:.1f}%)")
        print(f"  Requests/sec:       {stat.requests_per_second:.2f}")
        print(f"  Latency (avg):      {stat.avg_duration_ms:.2f} ms")
        print(f"  Latency (min):      {stat.min_duration_ms:.2f} ms")
        print(f"  Latency (max):      {stat.max_duration_ms:.2f} ms")
        print(f"  Latency (p50):      {stat.p50_duration_ms:.2f} ms")
        print(f"  Latency (p95):      {stat.p95_duration_ms:.2f} ms")
        print(f"  Latency (p99):      {stat.p99_duration_ms:.2f} ms")
        print()

    print("="*80 + "\n")


async def main():
    parser = argparse.ArgumentParser(
        description="Benchmark API endpoints"
    )
    parser.add_argument(
        "base_url",
        help="Base URL of API (e.g., http://localhost:8000)"
    )
    parser.add_argument(
        "-r", "--requests",
        type=int,
        default=1000,
        help="Total number of requests per endpoint (default: 1000)"
    )
    parser.add_argument(
        "-c", "--concurrency",
        type=int,
        default=10,
        help="Number of concurrent requests (default: 10)"
    )
    parser.add_argument(
        "-e", "--endpoints",
        nargs="+",
        default=["/health", "/items"],
        help="Endpoints to benchmark (default: /health /items)"
    )

    args = parser.parse_args()

    print(f"Benchmarking API: {args.base_url}")
    print(f"Total requests per endpoint: {args.requests}")
    print(f"Concurrency: {args.concurrency}")

    stats = []
    for endpoint in args.endpoints:
        stat = await benchmark_endpoint(
            args.base_url,
            endpoint,
            "GET",
            args.requests,
            args.concurrency
        )
        stats.append(stat)

    print_stats(stats)


if __name__ == "__main__":
    asyncio.run(main())
