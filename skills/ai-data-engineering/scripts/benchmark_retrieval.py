#!/usr/bin/env python3
"""
Retrieval Benchmark Script (TOKEN-FREE)

Benchmarks retrieval quality and latency without loading into context.

Usage:
    python benchmark_retrieval.py --config benchmark_config.json

Dependencies:
    pip install qdrant-client langchain-qdrant langchain-voyageai numpy
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import List, Dict
import numpy as np


def benchmark_retrieval(
    query: str,
    vectorstore,
    k: int = 5,
    search_type: str = "similarity"
) -> Dict:
    """Benchmark a single query."""

    # Measure latency
    start_time = time.time()

    try:
        retriever = vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs={"k": k}
        )
        results = retriever.get_relevant_documents(query)
    except Exception as e:
        return {
            "query": query,
            "error": str(e),
            "latency_ms": None,
            "num_results": 0
        }

    latency_ms = (time.time() - start_time) * 1000

    return {
        "query": query,
        "latency_ms": latency_ms,
        "num_results": len(results),
        "results": [
            {
                "content": doc.page_content[:200],  # First 200 chars
                "metadata": doc.metadata
            }
            for doc in results
        ]
    }


def run_benchmarks(config_path: str):
    """Run retrieval benchmarks."""

    # Load config
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found: {config_path}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config: {e}", file=sys.stderr)
        return 1

    # Import dependencies
    try:
        from langchain_qdrant import QdrantVectorStore
        from langchain_voyageai import VoyageAIEmbeddings
        from langchain_openai import OpenAIEmbeddings
        from qdrant_client import QdrantClient
    except ImportError as e:
        print(f"Error: Missing dependencies: {e}", file=sys.stderr)
        print("Run: pip install qdrant-client langchain-qdrant langchain-voyageai langchain-openai", file=sys.stderr)
        return 1

    # Setup vector store
    print("Connecting to vector store...")

    client = QdrantClient(url=config.get("qdrant_url", "http://localhost:6333"))

    # Get embeddings
    embedding_model = config.get("embedding_model", "voyage-3")
    if "voyage" in embedding_model:
        embeddings = VoyageAIEmbeddings(model=embedding_model)
    else:
        embeddings = OpenAIEmbeddings(model=embedding_model)

    vectorstore = QdrantVectorStore(
        client=client,
        collection_name=config["collection_name"],
        embedding=embeddings
    )

    # Run benchmarks
    queries = config.get("queries", [])
    k = config.get("top_k", 5)
    search_type = config.get("search_type", "similarity")

    print(f"\nRunning {len(queries)} queries...")
    print(f"Parameters: k={k}, search_type={search_type}\n")

    results = []
    latencies = []

    for i, query in enumerate(queries, 1):
        print(f"[{i}/{len(queries)}] {query[:50]}...", end=" ")

        result = benchmark_retrieval(query, vectorstore, k, search_type)

        if "error" in result and result["error"]:
            print(f"ERROR: {result['error']}")
        else:
            print(f"{result['latency_ms']:.0f}ms ({result['num_results']} results)")
            latencies.append(result['latency_ms'])

        results.append(result)

    # Calculate statistics
    if latencies:
        stats = {
            "total_queries": len(queries),
            "successful_queries": len(latencies),
            "failed_queries": len(queries) - len(latencies),
            "latency_stats": {
                "mean_ms": float(np.mean(latencies)),
                "median_ms": float(np.median(latencies)),
                "p95_ms": float(np.percentile(latencies, 95)),
                "p99_ms": float(np.percentile(latencies, 99)),
                "min_ms": float(np.min(latencies)),
                "max_ms": float(np.max(latencies))
            }
        }

        print("\n=== Benchmark Results ===\n")
        print(f"Queries: {stats['successful_queries']}/{stats['total_queries']} successful")
        print(f"\nLatency Statistics:")
        print(f"  Mean:   {stats['latency_stats']['mean_ms']:.1f}ms")
        print(f"  Median: {stats['latency_stats']['median_ms']:.1f}ms")
        print(f"  P95:    {stats['latency_stats']['p95_ms']:.1f}ms")
        print(f"  P99:    {stats['latency_stats']['p99_ms']:.1f}ms")
        print(f"  Min:    {stats['latency_stats']['min_ms']:.1f}ms")
        print(f"  Max:    {stats['latency_stats']['max_ms']:.1f}ms")

        # Quality check
        if stats['latency_stats']['p95_ms'] > 1000:
            print("\nWARNING: P95 latency > 1000ms (consider optimization)")

        # Save results
        output = {
            "config": config,
            "statistics": stats,
            "results": results
        }

        output_path = config.get("output_path", "benchmark_results.json")
        with open(output_path, "w") as f:
            json.dump(output, f, indent=2)

        print(f"\nResults saved to: {output_path}")

    else:
        print("\nNo successful queries to analyze")
        return 1

    return 0


def create_sample_config():
    """Create sample benchmark config."""
    config = {
        "qdrant_url": "http://localhost:6333",
        "collection_name": "documents",
        "embedding_model": "voyage-3",
        "top_k": 5,
        "search_type": "similarity",
        "queries": [
            "What is machine learning?",
            "How do neural networks work?",
            "What are the types of machine learning?",
            "Explain deep learning",
            "What is supervised learning?"
        ],
        "output_path": "benchmark_results.json"
    }

    with open("benchmark_config.json", "w") as f:
        json.dump(config, f, indent=2)

    print("Sample config created: benchmark_config.json")


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark RAG retrieval performance"
    )
    parser.add_argument(
        "--config",
        help="Path to benchmark config (JSON file)"
    )
    parser.add_argument(
        "--create-sample",
        action="store_true",
        help="Create sample config file"
    )

    args = parser.parse_args()

    if args.create_sample:
        create_sample_config()
        return 0

    if not args.config:
        print("Error: --config required (or use --create-sample)", file=sys.stderr)
        return 1

    return run_benchmarks(args.config)


if __name__ == "__main__":
    sys.exit(main())
