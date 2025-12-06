"""
Large-Scale Document Batch Processing

Process thousands to millions of documents efficiently with parallel processing,
rate limiting, and error recovery.

Dependencies:
    pip install openai numpy tqdm

Usage:
    python batch_processor.py --input documents.jsonl --output embeddings.npy

Environment Variables:
    OPENAI_API_KEY: Your OpenAI API key
"""

import os
import json
import time
import argparse
import numpy as np
from typing import List, Dict, Optional, Iterator
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import hashlib


@dataclass
class ProcessingStats:
    """Statistics for batch processing."""

    total_documents: int = 0
    successful: int = 0
    failed: int = 0
    skipped: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0

    @property
    def elapsed_seconds(self) -> float:
        """Get elapsed time in seconds."""
        return self.end_time - self.start_time if self.end_time > 0 else 0

    @property
    def throughput(self) -> float:
        """Get processing throughput (docs/sec)."""
        if self.elapsed_seconds > 0:
            return self.successful / self.elapsed_seconds
        return 0.0


class RateLimiter:
    """Rate limiter for API calls."""

    def __init__(self, max_requests_per_minute: int = 500):
        """
        Initialize rate limiter.

        Args:
            max_requests_per_minute: Maximum API requests per minute
        """
        self.max_requests = max_requests_per_minute
        self.window_seconds = 60
        self.requests = []

    def acquire(self):
        """Wait if necessary to respect rate limit."""
        now = time.time()

        # Remove requests outside current window
        self.requests = [t for t in self.requests if now - t < self.window_seconds]

        # Wait if at limit
        if len(self.requests) >= self.max_requests:
            oldest = min(self.requests)
            sleep_time = self.window_seconds - (now - oldest)
            if sleep_time > 0:
                time.sleep(sleep_time)

        # Record this request
        self.requests.append(time.time())


class BatchProcessor:
    """Process large document collections with embeddings."""

    def __init__(
        self,
        model: str = 'text-embedding-3-small',
        batch_size: int = 100,
        max_workers: int = 5,
        max_requests_per_minute: int = 500,
        retry_attempts: int = 3,
        retry_delay: float = 1.0
    ):
        """
        Initialize batch processor.

        Args:
            model: OpenAI embedding model
            batch_size: Number of documents per API call
            max_workers: Number of parallel workers
            max_requests_per_minute: API rate limit
            retry_attempts: Number of retries on failure
            retry_delay: Delay between retries (seconds)
        """
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        except ImportError:
            raise ImportError("Install openai: pip install openai")

        self.model = model
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay

        self.rate_limiter = RateLimiter(max_requests_per_minute)
        self.stats = ProcessingStats()

        # Cost per 1M tokens
        self.cost_per_1m = {
            'text-embedding-3-small': 0.02,
            'text-embedding-3-large': 0.13,
        }.get(model, 0.02)

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)."""
        return len(text) // 4

    def _embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a batch of texts with retry logic.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        for attempt in range(self.retry_attempts):
            try:
                # Respect rate limit
                self.rate_limiter.acquire()

                # Call API
                response = self.client.embeddings.create(
                    model=self.model,
                    input=texts
                )

                # Extract embeddings
                embeddings = [d.embedding for d in response.data]

                # Update stats
                for text in texts:
                    tokens = self._estimate_tokens(text)
                    self.stats.total_tokens += tokens
                    self.stats.total_cost += (tokens / 1_000_000) * self.cost_per_1m

                return embeddings

            except Exception as e:
                if attempt < self.retry_attempts - 1:
                    # Exponential backoff
                    delay = self.retry_delay * (2 ** attempt)
                    print(f"  Retry {attempt + 1}/{self.retry_attempts} after {delay:.1f}s: {e}")
                    time.sleep(delay)
                else:
                    print(f"  Failed after {self.retry_attempts} attempts: {e}")
                    raise

    def _process_chunk(self, documents: List[Dict]) -> List[Optional[List[float]]]:
        """
        Process a chunk of documents.

        Args:
            documents: List of document dicts with 'text' field

        Returns:
            List of embeddings (None for failed documents)
        """
        texts = [doc.get('text', '') for doc in documents]

        try:
            embeddings = self._embed_batch(texts)
            self.stats.successful += len(documents)
            return embeddings
        except Exception as e:
            self.stats.failed += len(documents)
            return [None] * len(documents)

    def load_documents(self, input_path: Path) -> Iterator[List[Dict]]:
        """
        Load documents from JSONL file in batches.

        Args:
            input_path: Path to JSONL file

        Yields:
            Batches of documents
        """
        batch = []

        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    doc = json.loads(line)
                    batch.append(doc)

                    if len(batch) >= self.batch_size:
                        yield batch
                        batch = []

        # Yield remaining documents
        if batch:
            yield batch

    def process_documents(
        self,
        input_path: Path,
        output_path: Path,
        resume: bool = False
    ) -> ProcessingStats:
        """
        Process documents from JSONL file and save embeddings.

        Args:
            input_path: Path to input JSONL file
            output_path: Path to output .npy file
            resume: Resume from checkpoint if available

        Returns:
            Processing statistics
        """
        print(f"Processing documents from {input_path}")
        print(f"Model: {self.model}")
        print(f"Batch size: {self.batch_size}")
        print(f"Max workers: {self.max_workers}")
        print(f"Rate limit: {self.rate_limiter.max_requests} req/min")
        print()

        # Count total documents
        with open(input_path, 'r') as f:
            total_docs = sum(1 for line in f if line.strip())
        self.stats.total_documents = total_docs
        print(f"Total documents: {total_docs:,}")

        # Check for checkpoint
        checkpoint_path = output_path.with_suffix('.checkpoint.npy')
        processed_docs = 0
        all_embeddings = []

        if resume and checkpoint_path.exists():
            print(f"\nResuming from checkpoint: {checkpoint_path}")
            all_embeddings = np.load(checkpoint_path).tolist()
            processed_docs = len(all_embeddings)
            print(f"Loaded {processed_docs:,} previously processed embeddings")

        # Initialize stats
        self.stats.start_time = time.time()

        try:
            # Progress tracking
            try:
                from tqdm import tqdm
                progress = tqdm(total=total_docs, initial=processed_docs, desc="Processing")
            except ImportError:
                progress = None
                print("Install tqdm for progress bar: pip install tqdm")

            # Process in parallel batches
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = []

                # Submit batches
                for batch_docs in self.load_documents(input_path):
                    # Skip if already processed (for resume)
                    if processed_docs >= len(all_embeddings) + len(batch_docs):
                        processed_docs += len(batch_docs)
                        if progress:
                            progress.update(len(batch_docs))
                        continue

                    future = executor.submit(self._process_chunk, batch_docs)
                    futures.append(future)

                    # Limit queue size to avoid memory issues
                    if len(futures) >= self.max_workers * 2:
                        # Wait for some to complete
                        done = as_completed(futures[:self.max_workers])
                        for future in done:
                            embeddings = future.result()
                            all_embeddings.extend(embeddings)
                            if progress:
                                progress.update(len(embeddings))

                        futures = futures[self.max_workers:]

                # Wait for remaining futures
                for future in as_completed(futures):
                    embeddings = future.result()
                    all_embeddings.extend(embeddings)
                    if progress:
                        progress.update(len(embeddings))

            if progress:
                progress.close()

            # Save results
            self.stats.end_time = time.time()

            # Filter out failed embeddings (None values)
            valid_embeddings = [e for e in all_embeddings if e is not None]

            if valid_embeddings:
                embeddings_array = np.array(valid_embeddings, dtype=np.float32)
                np.save(output_path, embeddings_array)
                print(f"\nSaved {len(valid_embeddings):,} embeddings to {output_path}")

                # Remove checkpoint if exists
                if checkpoint_path.exists():
                    checkpoint_path.unlink()
            else:
                print("\nNo valid embeddings generated")

        except KeyboardInterrupt:
            print("\n\nInterrupted! Saving checkpoint...")
            if all_embeddings:
                checkpoint_array = np.array([e for e in all_embeddings if e is not None], dtype=np.float32)
                np.save(checkpoint_path, checkpoint_array)
                print(f"Checkpoint saved to {checkpoint_path}")
                print("Resume with --resume flag")
            raise

        return self.stats

    def print_summary(self):
        """Print processing summary."""
        print("\n" + "=" * 60)
        print("BATCH PROCESSING SUMMARY")
        print("=" * 60)

        print(f"\nDocuments:")
        print(f"  Total:       {self.stats.total_documents:,}")
        print(f"  Successful:  {self.stats.successful:,}")
        print(f"  Failed:      {self.stats.failed:,}")
        print(f"  Skipped:     {self.stats.skipped:,}")

        success_rate = (self.stats.successful / self.stats.total_documents * 100) if self.stats.total_documents > 0 else 0
        print(f"  Success Rate: {success_rate:.2f}%")

        print(f"\nPerformance:")
        print(f"  Elapsed Time: {self.stats.elapsed_seconds:.2f}s")
        print(f"  Throughput:   {self.stats.throughput:.2f} docs/sec")

        print(f"\nCost:")
        print(f"  Total Tokens: {self.stats.total_tokens:,}")
        print(f"  Total Cost:   ${self.stats.total_cost:.4f}")
        print(f"  Cost per Doc: ${self.stats.total_cost / max(1, self.stats.successful):.6f}")

        print("=" * 60)


def main():
    """CLI for batch processing."""

    parser = argparse.ArgumentParser(
        description='Batch process documents with embeddings',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '--input',
        type=Path,
        required=True,
        help='Input JSONL file (one document per line with "text" field)'
    )

    parser.add_argument(
        '--output',
        type=Path,
        required=True,
        help='Output .npy file for embeddings'
    )

    parser.add_argument(
        '--model',
        type=str,
        default='text-embedding-3-small',
        choices=['text-embedding-3-small', 'text-embedding-3-large'],
        help='OpenAI embedding model'
    )

    parser.add_argument(
        '--batch-size',
        type=int,
        default=100,
        help='Documents per API call (max 2048)'
    )

    parser.add_argument(
        '--workers',
        type=int,
        default=5,
        help='Number of parallel workers'
    )

    parser.add_argument(
        '--rate-limit',
        type=int,
        default=500,
        help='Max API requests per minute'
    )

    parser.add_argument(
        '--resume',
        action='store_true',
        help='Resume from checkpoint if available'
    )

    args = parser.parse_args()

    # Validate inputs
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        return

    if args.batch_size > 2048:
        print("Warning: OpenAI max batch size is 2048")
        args.batch_size = 2048

    # Create processor
    processor = BatchProcessor(
        model=args.model,
        batch_size=args.batch_size,
        max_workers=args.workers,
        max_requests_per_minute=args.rate_limit
    )

    # Process documents
    try:
        stats = processor.process_documents(
            input_path=args.input,
            output_path=args.output,
            resume=args.resume
        )

        processor.print_summary()

        print("\nProcessing complete!")
        print(f"\nLoad embeddings with:")
        print(f"  import numpy as np")
        print(f"  embeddings = np.load('{args.output}')")

    except KeyboardInterrupt:
        print("\n\nProcessing interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        raise


if __name__ == "__main__":
    main()
