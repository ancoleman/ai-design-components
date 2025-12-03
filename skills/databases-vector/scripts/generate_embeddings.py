#!/usr/bin/env python3
"""
Generate embeddings for documents with progress tracking.

This script can be EXECUTED without being loaded into context (token-free!).

Usage:
    python scripts/generate_embeddings.py --input docs/ --output embeddings.json
    python scripts/generate_embeddings.py --input docs/ --model text-embedding-3-small
"""

import argparse
import json
import os
from pathlib import Path
from typing import List, Dict
import sys

try:
    from openai import OpenAI
    from tqdm import tqdm
except ImportError:
    print("Error: Missing dependencies. Install with:")
    print("  pip install openai tqdm")
    sys.exit(1)


def read_documents(input_path: str) -> List[Dict[str, str]]:
    """Read all documents from a directory or file."""
    docs = []
    input_path = Path(input_path)

    if input_path.is_file():
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
            docs.append({"path": str(input_path), "content": content})
    elif input_path.is_dir():
        for file_path in input_path.rglob('*.md'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                docs.append({"path": str(file_path), "content": content})
    else:
        raise ValueError(f"Invalid input path: {input_path}")

    return docs


def generate_embeddings(
    documents: List[Dict[str, str]],
    model: str = "text-embedding-3-large",
    batch_size: int = 100,
    api_key: str = None
) -> List[Dict]:
    """Generate embeddings for documents with batching."""
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    results = []
    total_batches = (len(documents) + batch_size - 1) // batch_size

    with tqdm(total=len(documents), desc="Generating embeddings") as pbar:
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            texts = [doc["content"] for doc in batch]

            # Generate embeddings
            response = client.embeddings.create(
                input=texts,
                model=model
            )

            # Collect results
            for doc, emb in zip(batch, response.data):
                results.append({
                    "path": doc["path"],
                    "embedding": emb.embedding,
                    "model": model,
                    "dimensions": len(emb.embedding)
                })

            pbar.update(len(batch))

    return results


def save_embeddings(embeddings: List[Dict], output_path: str):
    """Save embeddings to JSON file."""
    with open(output_path, 'w') as f:
        json.dump(embeddings, f, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Generate embeddings for documents"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input directory or file path"
    )
    parser.add_argument(
        "--output",
        default="embeddings.json",
        help="Output JSON file path"
    )
    parser.add_argument(
        "--model",
        default="text-embedding-3-large",
        choices=[
            "text-embedding-3-large",
            "text-embedding-3-small",
            "text-embedding-ada-002"
        ],
        help="OpenAI embedding model"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Batch size for API requests"
    )
    parser.add_argument(
        "--api-key",
        help="OpenAI API key (or set OPENAI_API_KEY env var)"
    )

    args = parser.parse_args()

    # Validate API key
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OpenAI API key not found.")
        print("Set OPENAI_API_KEY environment variable or use --api-key")
        sys.exit(1)

    try:
        # Read documents
        print(f"Reading documents from {args.input}...")
        documents = read_documents(args.input)
        print(f"Found {len(documents)} documents")

        # Generate embeddings
        print(f"Generating embeddings with {args.model}...")
        embeddings = generate_embeddings(
            documents,
            model=args.model,
            batch_size=args.batch_size,
            api_key=api_key
        )

        # Save results
        save_embeddings(embeddings, args.output)
        print(f"\nSaved {len(embeddings)} embeddings to {args.output}")

        # Print summary
        total_dims = sum(e["dimensions"] for e in embeddings)
        avg_dims = total_dims / len(embeddings)
        print(f"Average dimensions: {avg_dims:.0f}")
        print(f"Model: {embeddings[0]['model']}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
