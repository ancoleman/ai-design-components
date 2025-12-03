#!/usr/bin/env python3
"""
Benchmark similarity search performance across different vector databases.

This script can be EXECUTED without being loaded into context (token-free!).

Usage:
    python scripts/benchmark_similarity.py --db qdrant --vectors 10000
    python scripts/benchmark_similarity.py --db pgvector --vectors 100000
"""

import argparse
import time
import statistics
from typing import List, Dict
import sys

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
    import numpy as np
except ImportError:
    print("Error: Missing dependencies. Install with:")
    print("  pip install qdrant-client numpy")
    sys.exit(1)


def generate_random_vectors(count: int, dimensions: int = 1024) -> List[List[float]]:
    """Generate random vectors for benchmarking."""
    return [np.random.rand(dimensions).tolist() for _ in range(count)]


def benchmark_qdrant(
    vectors: List[List[float]],
    queries: List[List[float]],
    url: str = "localhost",
    port: int = 6333
) -> Dict:
    """Benchmark Qdrant performance."""
    client = QdrantClient(url, port=port)
    collection_name = "benchmark_test"

    # Setup
    print("Setting up Qdrant collection...")
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=len(vectors[0]),
            distance=Distance.COSINE
        )
    )

    # Insert vectors
    print(f"Inserting {len(vectors)} vectors...")
    start = time.time()

    points = [
        PointStruct(id=idx, vector=vec, payload={"index": idx})
        for idx, vec in enumerate(vectors)
    ]
    client.upsert(collection_name=collection_name, points=points, wait=True)

    insert_time = time.time() - start
    print(f"Insert time: {insert_time:.2f}s ({len(vectors)/insert_time:.0f} vectors/s)")

    # Benchmark searches
    print(f"Running {len(queries)} search queries...")
    search_times = []

    for query in queries:
        start = time.time()
        results = client.search(
            collection_name=collection_name,
            query_vector=query,
            limit=10
        )
        search_times.append(time.time() - start)

    # Cleanup
    client.delete_collection(collection_name)

    return {
        "database": "Qdrant",
        "vectors": len(vectors),
        "insert_time": insert_time,
        "insert_rate": len(vectors) / insert_time,
        "avg_search_time": statistics.mean(search_times) * 1000,  # ms
        "p50_search_time": statistics.median(search_times) * 1000,
        "p95_search_time": statistics.quantiles(search_times, n=20)[18] * 1000,
        "p99_search_time": statistics.quantiles(search_times, n=100)[98] * 1000,
    }


def benchmark_pgvector(
    vectors: List[List[float]],
    queries: List[List[float]],
    connection_string: str = None
) -> Dict:
    """Benchmark pgvector performance."""
    try:
        import psycopg2
        from pgvector.psycopg2 import register_vector
    except ImportError:
        print("Error: psycopg2 and pgvector not installed")
        print("  pip install psycopg2-binary pgvector")
        return None

    if not connection_string:
        connection_string = "postgresql://postgres:password@localhost/vectordb"

    conn = psycopg2.connect(connection_string)
    conn.autocommit = True
    register_vector(conn)
    cur = conn.cursor()

    # Setup
    print("Setting up pgvector table...")
    cur.execute("DROP TABLE IF EXISTS benchmark_test")
    cur.execute(f"""
        CREATE TABLE benchmark_test (
            id SERIAL PRIMARY KEY,
            embedding vector({len(vectors[0])})
        )
    """)

    # Insert vectors
    print(f"Inserting {len(vectors)} vectors...")
    start = time.time()

    for vec in vectors:
        cur.execute(
            "INSERT INTO benchmark_test (embedding) VALUES (%s)",
            (vec,)
        )

    insert_time = time.time() - start
    print(f"Insert time: {insert_time:.2f}s ({len(vectors)/insert_time:.0f} vectors/s)")

    # Create index
    print("Creating HNSW index...")
    start = time.time()
    cur.execute("""
        CREATE INDEX ON benchmark_test
        USING hnsw (embedding vector_cosine_ops)
    """)
    index_time = time.time() - start
    print(f"Index time: {index_time:.2f}s")

    # Benchmark searches
    print(f"Running {len(queries)} search queries...")
    search_times = []

    for query in queries:
        start = time.time()
        cur.execute(
            """
            SELECT id, embedding <=> %s AS distance
            FROM benchmark_test
            ORDER BY embedding <=> %s
            LIMIT 10
            """,
            (query, query)
        )
        cur.fetchall()
        search_times.append(time.time() - start)

    # Cleanup
    cur.execute("DROP TABLE benchmark_test")
    conn.close()

    return {
        "database": "pgvector",
        "vectors": len(vectors),
        "insert_time": insert_time,
        "index_time": index_time,
        "insert_rate": len(vectors) / insert_time,
        "avg_search_time": statistics.mean(search_times) * 1000,
        "p50_search_time": statistics.median(search_times) * 1000,
        "p95_search_time": statistics.quantiles(search_times, n=20)[18] * 1000,
        "p99_search_time": statistics.quantiles(search_times, n=100)[98] * 1000,
    }


def print_results(results: Dict):
    """Print benchmark results."""
    print("\n" + "="*60)
    print(f"BENCHMARK RESULTS: {results['database']}")
    print("="*60)
    print(f"Vectors:           {results['vectors']:,}")
    print(f"Insert time:       {results['insert_time']:.2f}s")
    print(f"Insert rate:       {results['insert_rate']:.0f} vectors/s")
    if 'index_time' in results:
        print(f"Index time:        {results['index_time']:.2f}s")
    print()
    print("Search Performance:")
    print(f"  Average:         {results['avg_search_time']:.2f}ms")
    print(f"  p50 (median):    {results['p50_search_time']:.2f}ms")
    print(f"  p95:             {results['p95_search_time']:.2f}ms")
    print(f"  p99:             {results['p99_search_time']:.2f}ms")
    print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark vector database performance"
    )
    parser.add_argument(
        "--db",
        required=True,
        choices=["qdrant", "pgvector"],
        help="Database to benchmark"
    )
    parser.add_argument(
        "--vectors",
        type=int,
        default=10000,
        help="Number of vectors to insert"
    )
    parser.add_argument(
        "--dimensions",
        type=int,
        default=1024,
        help="Vector dimensions"
    )
    parser.add_argument(
        "--queries",
        type=int,
        default=100,
        help="Number of search queries to run"
    )
    parser.add_argument(
        "--qdrant-url",
        default="localhost",
        help="Qdrant URL"
    )
    parser.add_argument(
        "--qdrant-port",
        type=int,
        default=6333,
        help="Qdrant port"
    )
    parser.add_argument(
        "--pgvector-conn",
        help="PostgreSQL connection string"
    )

    args = parser.parse_args()

    print(f"Generating {args.vectors} random vectors ({args.dimensions}d)...")
    vectors = generate_random_vectors(args.vectors, args.dimensions)
    queries = generate_random_vectors(args.queries, args.dimensions)

    if args.db == "qdrant":
        results = benchmark_qdrant(
            vectors,
            queries,
            url=args.qdrant_url,
            port=args.qdrant_port
        )
    elif args.db == "pgvector":
        results = benchmark_pgvector(
            vectors,
            queries,
            connection_string=args.pgvector_conn
        )

    if results:
        print_results(results)


if __name__ == "__main__":
    main()
