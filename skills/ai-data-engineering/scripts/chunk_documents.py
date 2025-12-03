#!/usr/bin/env python3
"""
Document Chunking Script (TOKEN-FREE)

Chunks documents with configurable size and overlap without loading into context.

Usage:
    python chunk_documents.py --input docs/ --output chunks/ --chunk-size 512 --overlap 50

Dependencies:
    pip install langchain langchain-text-splitters
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict


def chunk_file(
    file_path: Path,
    chunk_size: int,
    chunk_overlap: int,
    file_type: str = "text"
) -> List[Dict]:
    """Chunk a single file."""
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain.document_loaders import TextLoader
    except ImportError:
        print("Error: Missing dependencies. Run: pip install langchain langchain-text-splitters", file=sys.stderr)
        sys.exit(1)

    # Load document
    try:
        if file_type == "text":
            loader = TextLoader(str(file_path))
        else:
            print(f"Warning: Unsupported file type '{file_type}', treating as text", file=sys.stderr)
            loader = TextLoader(str(file_path))

        documents = loader.load()
    except Exception as e:
        print(f"Error loading {file_path}: {e}", file=sys.stderr)
        return []

    # Create splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    # Split documents
    chunks = splitter.split_documents(documents)

    # Convert to dict format
    chunk_dicts = []
    for i, chunk in enumerate(chunks):
        chunk_dicts.append({
            "chunk_id": i,
            "source_file": str(file_path),
            "content": chunk.page_content,
            "metadata": chunk.metadata,
            "chunk_size": len(chunk.page_content)
        })

    return chunk_dicts


def chunk_directory(
    input_dir: Path,
    output_dir: Path,
    chunk_size: int,
    chunk_overlap: int,
    pattern: str = "*.txt"
):
    """Chunk all files in directory."""

    # Find files
    files = list(input_dir.glob(pattern))

    if not files:
        print(f"Warning: No files matching '{pattern}' found in {input_dir}", file=sys.stderr)
        return

    print(f"Found {len(files)} files")

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each file
    total_chunks = 0
    for file_path in files:
        print(f"Chunking: {file_path.name}...", end=" ")

        chunks = chunk_file(file_path, chunk_size, chunk_overlap)

        if chunks:
            # Save chunks
            output_file = output_dir / f"{file_path.stem}_chunks.json"
            with open(output_file, "w") as f:
                json.dump(chunks, f, indent=2)

            print(f"{len(chunks)} chunks")
            total_chunks += len(chunks)
        else:
            print("FAILED")

    # Save summary
    summary = {
        "input_directory": str(input_dir),
        "output_directory": str(output_dir),
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "total_files": len(files),
        "total_chunks": total_chunks,
        "avg_chunks_per_file": total_chunks / len(files) if files else 0
    }

    summary_file = output_dir / "chunking_summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nTotal: {total_chunks} chunks from {len(files)} files")
    print(f"Average: {summary['avg_chunks_per_file']:.1f} chunks per file")
    print(f"\nSummary saved to: {summary_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Chunk documents for RAG pipelines"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input directory containing documents"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output directory for chunks"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=512,
        help="Chunk size in characters (default: 512)"
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=50,
        help="Chunk overlap in characters (default: 50)"
    )
    parser.add_argument(
        "--pattern",
        default="*.txt",
        help="File pattern to match (default: *.txt)"
    )

    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}", file=sys.stderr)
        return 1

    chunk_directory(
        input_dir,
        output_dir,
        args.chunk_size,
        args.overlap,
        args.pattern
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
