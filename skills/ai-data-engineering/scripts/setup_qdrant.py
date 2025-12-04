#!/usr/bin/env python3
"""
Qdrant Collection Setup Script

Creates and configures Qdrant collections for RAG pipelines.

Usage:
    python scripts/setup_qdrant.py --collection docs --dimension 1024
    python scripts/setup_qdrant.py --collection docs --dimension 1024 --enable-hybrid
    python scripts/setup_qdrant.py --delete docs
"""

import argparse
import sys
from typing import Optional

try:
    from qdrant_client import QdrantClient, models
except ImportError:
    print("Error: qdrant-client not installed")
    print("Install: pip install qdrant-client")
    sys.exit(1)


def create_collection(
    client: QdrantClient,
    collection_name: str,
    vector_size: int,
    enable_hybrid: bool = False,
    distance: str = "Cosine",
):
    """Create Qdrant collection with optional hybrid search"""

    print(f"Creating collection: {collection_name}")
    print(f"  Vector size: {vector_size}")
    print(f"  Distance metric: {distance}")
    print(f"  Hybrid search: {'enabled' if enable_hybrid else 'disabled'}")

    # Distance metric mapping
    distance_map = {
        "Cosine": models.Distance.COSINE,
        "Euclidean": models.Distance.EUCLID,
        "Dot": models.Distance.DOT,
    }

    # Basic vector configuration
    vectors_config = models.VectorParams(
        size=vector_size,
        distance=distance_map.get(distance, models.Distance.COSINE),
    )

    # Hybrid search configuration (vector + BM25)
    sparse_vectors_config = None
    if enable_hybrid:
        sparse_vectors_config = {
            "text": models.SparseVectorParams(
                modifier=models.Modifier.IDF
            )
        }
        print("  Sparse vectors (BM25): enabled")

    try:
        # Create collection
        client.create_collection(
            collection_name=collection_name,
            vectors_config=vectors_config,
            sparse_vectors_config=sparse_vectors_config,
            optimizers_config=models.OptimizersConfigDiff(
                indexing_threshold=10000,  # Start indexing after 10K vectors
            ),
            hnsw_config=models.HnswConfigDiff(
                m=16,                       # Number of edges per node
                ef_construct=100,           # Size of dynamic candidate list
                full_scan_threshold=10000,  # Use full scan for small collections
            ),
        )

        print(f"\n✓ Collection '{collection_name}' created successfully")
        print(f"\nCollection info:")
        print(f"  Endpoint: http://localhost:6333")
        print(f"  Collection: {collection_name}")
        print(f"  Vector dimensions: {vector_size}")
        print(f"  Index: HNSW (m=16, ef_construct=100)")

        if enable_hybrid:
            print(f"\nHybrid search enabled - use both dense and sparse vectors:")
            print(f"  Dense: Your embedding model (Voyage AI, OpenAI, etc.)")
            print(f"  Sparse: BM25 tokenization (use tiktoken)")

    except Exception as e:
        print(f"Error creating collection: {e}", file=sys.stderr)
        sys.exit(1)


def delete_collection(client: QdrantClient, collection_name: str):
    """Delete a collection"""
    try:
        client.delete_collection(collection_name=collection_name)
        print(f"✓ Collection '{collection_name}' deleted")
    except Exception as e:
        print(f"Error deleting collection: {e}", file=sys.stderr)
        sys.exit(1)


def list_collections(client: QdrantClient):
    """List all collections"""
    collections = client.get_collections().collections

    if not collections:
        print("No collections found")
        return

    print(f"Found {len(collections)} collection(s):")
    for coll in collections:
        info = client.get_collection(coll.name)
        print(f"\n{coll.name}:")
        print(f"  Vectors: {info.points_count}")
        print(f"  Dimensions: {info.config.params.vectors.size}")
        print(f"  Distance: {info.config.params.vectors.distance}")


def main():
    parser = argparse.ArgumentParser(description="Setup Qdrant collections")
    parser.add_argument(
        "--host",
        default="localhost",
        help="Qdrant host (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=6333,
        help="Qdrant port (default: 6333)"
    )
    parser.add_argument(
        "--collection",
        help="Collection name"
    )
    parser.add_argument(
        "--dimension",
        type=int,
        help="Vector dimension (e.g., 1024 for Voyage AI, 1536 for OpenAI)"
    )
    parser.add_argument(
        "--enable-hybrid",
        action="store_true",
        help="Enable hybrid search (vector + BM25)"
    )
    parser.add_argument(
        "--distance",
        choices=["Cosine", "Euclidean", "Dot"],
        default="Cosine",
        help="Distance metric (default: Cosine)"
    )
    parser.add_argument(
        "--delete",
        metavar="COLLECTION",
        help="Delete a collection"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all collections"
    )

    args = parser.parse_args()

    # Connect to Qdrant
    try:
        client = QdrantClient(host=args.host, port=args.port)
        print(f"Connected to Qdrant at {args.host}:{args.port}")
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}", file=sys.stderr)
        print("\nIs Qdrant running? Start with:")
        print("  docker run -p 6333:6333 qdrant/qdrant")
        sys.exit(1)

    # Handle commands
    if args.list:
        list_collections(client)

    elif args.delete:
        delete_collection(client, args.delete)

    elif args.collection and args.dimension:
        create_collection(
            client,
            args.collection,
            args.dimension,
            args.enable_hybrid,
            args.distance,
        )

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
