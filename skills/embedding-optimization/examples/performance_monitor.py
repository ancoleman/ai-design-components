"""
Embedding Pipeline Performance Monitoring

Demonstrates tracking latency, throughput, cost, and cache efficiency.

Dependencies:
    pip install numpy

Usage:
    python performance_monitor.py
"""

import time
import numpy as np
from typing import List, Dict, Callable
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class EmbeddingMetrics:
    """Metrics for embedding operations."""

    total_texts: int = 0
    total_embeddings: int = 0
    total_api_calls: int = 0
    total_cache_hits: int = 0
    total_latency_ms: float = 0.0
    total_cost_usd: float = 0.0
    errors: int = 0

    start_time: datetime = field(default_factory=datetime.now)

    def add_operation(
        self,
        num_texts: int,
        latency_ms: float,
        cache_hits: int = 0,
        api_calls: int = 1,
        cost_usd: float = 0.0,
        error: bool = False
    ):
        """Record an embedding operation."""
        self.total_texts += num_texts
        self.total_embeddings += num_texts
        self.total_api_calls += api_calls
        self.total_cache_hits += cache_hits
        self.total_latency_ms += latency_ms
        self.total_cost_usd += cost_usd
        if error:
            self.errors += 1

    def get_summary(self) -> Dict:
        """Get performance summary."""
        elapsed_seconds = (datetime.now() - self.start_time).total_seconds()

        cache_hit_rate = (
            (self.total_cache_hits / self.total_texts * 100)
            if self.total_texts > 0 else 0
        )

        throughput = (
            self.total_texts / elapsed_seconds
            if elapsed_seconds > 0 else 0
        )

        avg_latency = (
            self.total_latency_ms / self.total_api_calls
            if self.total_api_calls > 0 else 0
        )

        error_rate = (
            (self.errors / self.total_api_calls * 100)
            if self.total_api_calls > 0 else 0
        )

        return {
            'total_texts': self.total_texts,
            'total_api_calls': self.total_api_calls,
            'cache_hit_rate_pct': round(cache_hit_rate, 2),
            'throughput_texts_per_sec': round(throughput, 2),
            'avg_latency_ms': round(avg_latency, 2),
            'total_cost_usd': round(self.total_cost_usd, 4),
            'error_rate_pct': round(error_rate, 2),
            'elapsed_seconds': round(elapsed_seconds, 2)
        }


class LatencyTracker:
    """Track latency percentiles."""

    def __init__(self):
        self.latencies = []

    def record(self, latency_ms: float):
        """Record a latency measurement."""
        self.latencies.append(latency_ms)

    def percentiles(self) -> Dict:
        """Get latency percentiles."""
        if not self.latencies:
            return {}

        return {
            'p50': round(np.percentile(self.latencies, 50), 2),
            'p95': round(np.percentile(self.latencies, 95), 2),
            'p99': round(np.percentile(self.latencies, 99), 2),
            'avg': round(np.mean(self.latencies), 2),
            'min': round(np.min(self.latencies), 2),
            'max': round(np.max(self.latencies), 2)
        }

    def reset(self):
        """Reset latency measurements."""
        self.latencies = []


class CostTracker:
    """Track embedding costs."""

    PRICING = {
        'text-embedding-3-small': 0.00002,  # per 1K tokens
        'text-embedding-3-large': 0.00013,
        'embed-english-v3.0': 0.0001,
        'local': 0.0,  # Local models have zero API cost
    }

    def __init__(self, model: str = 'text-embedding-3-small'):
        self.model = model
        self.total_tokens = 0
        self.total_cost = 0.0
        self.calls = 0

    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (4 chars per token)."""
        return len(text) // 4

    def record_embedding(self, text: str, from_cache: bool = False) -> Dict:
        """
        Record embedding cost.

        Args:
            text: Input text
            from_cache: Whether this was served from cache (no cost)

        Returns:
            Dictionary with tokens and cost
        """
        tokens = self._estimate_tokens(text)
        cost = 0.0

        if not from_cache:
            cost = (tokens / 1000) * self.PRICING.get(self.model, 0)
            self.total_tokens += tokens
            self.total_cost += cost
            self.calls += 1

        return {
            'tokens': tokens,
            'cost_usd': cost
        }

    def summary(self) -> Dict:
        """Get cost summary."""
        avg_tokens = self.total_tokens / max(1, self.calls)
        avg_cost = self.total_cost / max(1, self.calls)

        return {
            'total_tokens': self.total_tokens,
            'total_cost_usd': round(self.total_cost, 4),
            'avg_tokens_per_text': round(avg_tokens, 2),
            'avg_cost_per_text': round(avg_cost, 6),
            'total_calls': self.calls
        }


class MonitoredEmbedder:
    """Wrapper for any embedder with performance monitoring."""

    def __init__(
        self,
        embedder: any,
        model: str = 'text-embedding-3-small'
    ):
        """
        Initialize monitored embedder.

        Args:
            embedder: Underlying embedder instance
            model: Model name for cost tracking
        """
        self.embedder = embedder
        self.metrics = EmbeddingMetrics()
        self.latency_tracker = LatencyTracker()
        self.cost_tracker = CostTracker(model)

    def embed_single(self, text: str) -> List[float]:
        """Embed with monitoring."""
        start = time.time()

        # Check if embedder has cache
        from_cache = False
        if hasattr(self.embedder, '_cache_key') and hasattr(self.embedder, 'redis_client'):
            cache_key = self.embedder._cache_key(text)
            from_cache = self.embedder.redis_client.exists(cache_key)

        # Embed
        try:
            embedding = self.embedder.embed_single(text)

            # Record metrics
            latency_ms = (time.time() - start) * 1000
            self.latency_tracker.record(latency_ms)

            cost_info = self.cost_tracker.record_embedding(text, from_cache)

            self.metrics.add_operation(
                num_texts=1,
                latency_ms=latency_ms,
                cache_hits=1 if from_cache else 0,
                api_calls=0 if from_cache else 1,
                cost_usd=cost_info['cost_usd']
            )

            return embedding

        except Exception as e:
            self.metrics.add_operation(
                num_texts=1,
                latency_ms=(time.time() - start) * 1000,
                error=True
            )
            raise

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed batch with monitoring."""
        start = time.time()

        # Check cache hits
        cache_hits = 0
        if hasattr(self.embedder, '_cache_key') and hasattr(self.embedder, 'redis_client'):
            for text in texts:
                cache_key = self.embedder._cache_key(text)
                if self.embedder.redis_client.exists(cache_key):
                    cache_hits += 1

        # Embed
        try:
            embeddings = self.embedder.embed_batch(texts)

            # Record metrics
            latency_ms = (time.time() - start) * 1000
            self.latency_tracker.record(latency_ms)

            # Calculate costs
            total_cost = 0.0
            for text in texts:
                from_cache = False
                if hasattr(self.embedder, '_cache_key') and hasattr(self.embedder, 'redis_client'):
                    cache_key = self.embedder._cache_key(text)
                    from_cache = self.embedder.redis_client.exists(cache_key)

                cost_info = self.cost_tracker.record_embedding(text, from_cache)
                total_cost += cost_info['cost_usd']

            api_calls = 1 if cache_hits < len(texts) else 0

            self.metrics.add_operation(
                num_texts=len(texts),
                latency_ms=latency_ms,
                cache_hits=cache_hits,
                api_calls=api_calls,
                cost_usd=total_cost
            )

            return embeddings

        except Exception as e:
            self.metrics.add_operation(
                num_texts=len(texts),
                latency_ms=(time.time() - start) * 1000,
                error=True
            )
            raise

    def get_metrics(self) -> Dict:
        """Get comprehensive performance metrics."""
        summary = self.metrics.get_summary()
        latency = self.latency_tracker.percentiles()
        cost = self.cost_tracker.summary()

        return {
            **summary,
            'latency': latency,
            'cost': cost
        }

    def print_dashboard(self):
        """Print a comprehensive dashboard."""
        metrics = self.get_metrics()

        print("=" * 60)
        print("EMBEDDING PIPELINE DASHBOARD")
        print("=" * 60)

        print("\nPERFORMANCE:")
        print(f"  Throughput:     {metrics['throughput_texts_per_sec']:.2f} texts/sec")
        print(f"  Avg Latency:    {metrics['avg_latency_ms']:.2f} ms")
        if metrics.get('latency'):
            print(f"  Latency p50:    {metrics['latency']['p50']:.2f} ms")
            print(f"  Latency p95:    {metrics['latency']['p95']:.2f} ms")
            print(f"  Latency p99:    {metrics['latency']['p99']:.2f} ms")
        print(f"  Error Rate:     {metrics['error_rate_pct']:.2f}%")

        print("\nCACHE:")
        print(f"  Hit Rate:       {metrics['cache_hit_rate_pct']:.2f}%")
        print(f"  Cache Hits:     {metrics['total_cache_hits']:,}")
        print(f"  Cache Misses:   {metrics['total_texts'] - metrics['total_cache_hits']:,}")

        print("\nCOST:")
        if metrics.get('cost'):
            print(f"  Total Cost:     ${metrics['cost']['total_cost_usd']:.4f}")
            print(f"  Total Tokens:   {metrics['cost']['total_tokens']:,}")
            print(f"  Avg Cost/Text:  ${metrics['cost']['avg_cost_per_text']:.6f}")

        print("\nOVERALL:")
        print(f"  Total Texts:    {metrics['total_texts']:,}")
        print(f"  API Calls:      {metrics['total_api_calls']:,}")
        print(f"  Elapsed Time:   {metrics['elapsed_seconds']:.2f}s")

        print("=" * 60)


# Mock embedder for demonstration
class MockEmbedder:
    """Mock embedder for testing monitoring."""

    def embed_single(self, text: str) -> List[float]:
        time.sleep(0.01)  # Simulate API latency
        return [0.1] * 384

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        time.sleep(0.05)  # Simulate batch API latency
        return [[0.1] * 384 for _ in texts]


def main():
    """Example usage of performance monitoring."""

    print("Embedding Pipeline Performance Monitoring Demo")
    print("=" * 60)

    # Create mock embedder
    embedder = MockEmbedder()
    monitored = MonitoredEmbedder(embedder, model='text-embedding-3-small')

    # Example 1: Single text embeddings
    print("\n1. Embedding single texts...")
    for i in range(10):
        text = f"Sample text number {i}"
        monitored.embed_single(text)

    print("   Embedded 10 texts")

    # Example 2: Batch embedding
    print("\n2. Embedding batch...")
    texts = [f"Batch text {i}" for i in range(50)]
    monitored.embed_batch(texts)

    print("   Embedded 50 texts in batch")

    # Example 3: Show metrics
    print("\n3. Performance Metrics:")
    metrics = monitored.get_metrics()

    print(f"\n   Total Texts: {metrics['total_texts']}")
    print(f"   Throughput: {metrics['throughput_texts_per_sec']:.2f} texts/sec")
    print(f"   Avg Latency: {metrics['avg_latency_ms']:.2f} ms")

    if metrics.get('latency'):
        print(f"\n   Latency Percentiles:")
        print(f"     p50: {metrics['latency']['p50']:.2f} ms")
        print(f"     p95: {metrics['latency']['p95']:.2f} ms")
        print(f"     p99: {metrics['latency']['p99']:.2f} ms")

    if metrics.get('cost'):
        print(f"\n   Cost Metrics:")
        print(f"     Total Cost: ${metrics['cost']['total_cost_usd']:.4f}")
        print(f"     Total Tokens: {metrics['cost']['total_tokens']:,}")
        print(f"     Avg Cost/Text: ${metrics['cost']['avg_cost_per_text']:.6f}")

    # Example 4: Full dashboard
    print("\n4. Full Dashboard:")
    monitored.print_dashboard()

    print("\n" + "=" * 60)
    print("Demo complete!")
    print("\nKey Metrics to Track:")
    print("  1. Latency (p95, p99 - not just average)")
    print("  2. Throughput (texts/sec)")
    print("  3. Cache hit rate (target: >60%)")
    print("  4. Cost (total USD and per-text)")
    print("  5. Error rate (target: <1%)")


if __name__ == "__main__":
    main()
