"""
Embedding Model Benchmarking

Benchmark different embedding models for latency, quality, and cost.
Compare OpenAI, Cohere, Voyage AI, and open-source models.

Dependencies:
    pip install numpy sentence-transformers openai cohere voyageai matplotlib

Usage:
    python benchmark_embeddings.py

Environment Variables:
    OPENAI_API_KEY: Your OpenAI API key (optional)
    COHERE_API_KEY: Your Cohere API key (optional)
    VOYAGE_API_KEY: Your Voyage AI API key (optional)
"""

import os
import time
import numpy as np
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, field
import matplotlib.pyplot as plt
from datetime import datetime


@dataclass
class BenchmarkResult:
    """Results from benchmarking a single model."""

    model_name: str
    provider: str  # 'openai', 'cohere', 'voyage', 'local'
    dimensions: int

    # Latency metrics (milliseconds)
    latency_p50: float = 0.0
    latency_p95: float = 0.0
    latency_p99: float = 0.0
    latency_avg: float = 0.0

    # Throughput
    throughput_texts_per_sec: float = 0.0

    # Cost (per 1M tokens)
    cost_per_1m_tokens: float = 0.0

    # Quality (MTEB score approximation or known benchmark)
    mteb_score: Optional[float] = None

    # Additional metadata
    batch_size: int = 1
    num_samples: int = 0
    errors: int = 0

    def cost_per_1k_texts(self, avg_tokens_per_text: int = 100) -> float:
        """Calculate cost per 1,000 texts."""
        if self.cost_per_1m_tokens == 0:
            return 0.0
        return (avg_tokens_per_text * 1000 / 1_000_000) * self.cost_per_1m_tokens

    def quality_per_dollar(self, avg_tokens_per_text: int = 100) -> float:
        """Calculate quality score per dollar (higher is better)."""
        if not self.mteb_score or self.cost_per_1m_tokens == 0:
            return 0.0
        cost_per_1k = self.cost_per_1k_texts(avg_tokens_per_text)
        if cost_per_1k == 0:
            return float('inf')  # Local models
        return self.mteb_score / cost_per_1k


class EmbedderBenchmark:
    """Benchmark embedding models."""

    # Known MTEB scores (as of Nov 2024)
    MTEB_SCORES = {
        'text-embedding-3-small': 62.3,
        'text-embedding-3-large': 64.6,
        'embed-english-v3.0': 64.5,
        'embed-multilingual-v3.0': 62.0,
        'voyage-2': 63.5,
        'voyage-large-2': 65.2,
        'all-MiniLM-L6-v2': 56.3,
        'all-mpnet-base-v2': 57.8,
        'bge-base-en-v1.5': 63.5,
        'bge-large-en-v1.5': 64.2,
    }

    # Pricing per 1M tokens
    PRICING = {
        'text-embedding-3-small': 0.02,
        'text-embedding-3-large': 0.13,
        'embed-english-v3.0': 0.10,
        'embed-multilingual-v3.0': 0.10,
        'voyage-2': 0.10,
        'voyage-large-2': 0.12,
        # Local models have zero API cost
        'all-MiniLM-L6-v2': 0.0,
        'all-mpnet-base-v2': 0.0,
        'bge-base-en-v1.5': 0.0,
        'bge-large-en-v1.5': 0.0,
    }

    def __init__(self, test_texts: Optional[List[str]] = None):
        """
        Initialize benchmark.

        Args:
            test_texts: Texts to use for benchmarking (default: sample texts)
        """
        if test_texts is None:
            self.test_texts = self._default_test_texts()
        else:
            self.test_texts = test_texts

        self.results: List[BenchmarkResult] = []

    def _default_test_texts(self) -> List[str]:
        """Generate default test texts for benchmarking."""
        return [
            "Machine learning is a subset of artificial intelligence.",
            "Natural language processing enables computers to understand human language.",
            "Deep learning uses neural networks with multiple layers.",
            "Computer vision allows machines to interpret visual information.",
            "Reinforcement learning trains agents through rewards and penalties.",
            "Supervised learning uses labeled data for training models.",
            "Unsupervised learning finds patterns in unlabeled data.",
            "Transfer learning adapts pre-trained models to new tasks.",
            "Generative AI creates new content like text and images.",
            "Large language models understand and generate human-like text.",
            "The quick brown fox jumps over the lazy dog.",
            "Paris is the capital and most populous city of France.",
            "Python is a high-level, interpreted programming language.",
            "Climate change refers to long-term shifts in temperatures.",
            "Quantum computing uses quantum phenomena for computation.",
        ] * 2  # 30 texts total for better statistics

    def benchmark_embedder(
        self,
        model_name: str,
        embed_func: Callable[[List[str]], List[List[float]]],
        provider: str,
        dimensions: int,
        batch_size: int = 10,
        warmup_runs: int = 2
    ) -> BenchmarkResult:
        """
        Benchmark a single embedder.

        Args:
            model_name: Name of the model
            embed_func: Function that takes texts and returns embeddings
            provider: Provider name ('openai', 'cohere', 'voyage', 'local')
            dimensions: Embedding dimensions
            batch_size: Batch size for embedding
            warmup_runs: Number of warmup runs before measurement

        Returns:
            BenchmarkResult with metrics
        """
        print(f"\nBenchmarking {model_name} ({provider})...")

        # Warmup
        for _ in range(warmup_runs):
            try:
                embed_func(self.test_texts[:batch_size])
            except Exception as e:
                print(f"  Warning: Warmup failed: {e}")

        # Measure latency
        latencies = []
        errors = 0

        for i in range(0, len(self.test_texts), batch_size):
            batch = self.test_texts[i:i + batch_size]

            start = time.time()
            try:
                embeddings = embed_func(batch)
                latency_ms = (time.time() - start) * 1000
                latencies.append(latency_ms)

                # Verify dimensions
                if len(embeddings) > 0 and len(embeddings[0]) != dimensions:
                    print(f"  Warning: Expected {dimensions} dims, got {len(embeddings[0])}")

            except Exception as e:
                print(f"  Error: {e}")
                errors += 1
                latencies.append(float('nan'))

        # Filter out errors
        valid_latencies = [l for l in latencies if not np.isnan(l)]

        if not valid_latencies:
            print(f"  Failed: No valid results")
            return BenchmarkResult(
                model_name=model_name,
                provider=provider,
                dimensions=dimensions,
                errors=errors,
                num_samples=0
            )

        # Calculate metrics
        total_time_sec = sum(valid_latencies) / 1000
        total_texts = len(self.test_texts) - (errors * batch_size)

        result = BenchmarkResult(
            model_name=model_name,
            provider=provider,
            dimensions=dimensions,
            latency_p50=np.percentile(valid_latencies, 50),
            latency_p95=np.percentile(valid_latencies, 95),
            latency_p99=np.percentile(valid_latencies, 99),
            latency_avg=np.mean(valid_latencies),
            throughput_texts_per_sec=total_texts / total_time_sec if total_time_sec > 0 else 0,
            cost_per_1m_tokens=self.PRICING.get(model_name, 0.0),
            mteb_score=self.MTEB_SCORES.get(model_name),
            batch_size=batch_size,
            num_samples=len(valid_latencies),
            errors=errors
        )

        print(f"  Latency p50: {result.latency_p50:.2f} ms")
        print(f"  Throughput: {result.throughput_texts_per_sec:.2f} texts/sec")
        print(f"  Cost per 1M tokens: ${result.cost_per_1m_tokens:.2f}")

        return result

    def benchmark_openai(self, model: str = 'text-embedding-3-small') -> Optional[BenchmarkResult]:
        """Benchmark OpenAI embedding model."""
        try:
            from openai import OpenAI

            if not os.getenv('OPENAI_API_KEY'):
                print(f"\nSkipping {model} (no OPENAI_API_KEY)")
                return None

            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

            dimensions = {
                'text-embedding-3-small': 1536,
                'text-embedding-3-large': 3072,
            }.get(model, 1536)

            def embed_func(texts: List[str]) -> List[List[float]]:
                response = client.embeddings.create(model=model, input=texts)
                return [d.embedding for d in response.data]

            return self.benchmark_embedder(
                model_name=model,
                embed_func=embed_func,
                provider='openai',
                dimensions=dimensions,
                batch_size=20
            )

        except ImportError:
            print(f"\nSkipping {model} (openai not installed)")
            return None
        except Exception as e:
            print(f"\nError benchmarking {model}: {e}")
            return None

    def benchmark_cohere(self, model: str = 'embed-english-v3.0') -> Optional[BenchmarkResult]:
        """Benchmark Cohere embedding model."""
        try:
            import cohere

            if not os.getenv('COHERE_API_KEY'):
                print(f"\nSkipping {model} (no COHERE_API_KEY)")
                return None

            client = cohere.Client(api_key=os.getenv('COHERE_API_KEY'))

            dimensions = 1024  # Cohere v3 models

            def embed_func(texts: List[str]) -> List[List[float]]:
                response = client.embed(texts=texts, model=model, input_type='search_document')
                return response.embeddings

            return self.benchmark_embedder(
                model_name=model,
                embed_func=embed_func,
                provider='cohere',
                dimensions=dimensions,
                batch_size=20
            )

        except ImportError:
            print(f"\nSkipping {model} (cohere not installed)")
            return None
        except Exception as e:
            print(f"\nError benchmarking {model}: {e}")
            return None

    def benchmark_voyage(self, model: str = 'voyage-2') -> Optional[BenchmarkResult]:
        """Benchmark Voyage AI embedding model."""
        try:
            import voyageai

            if not os.getenv('VOYAGE_API_KEY'):
                print(f"\nSkipping {model} (no VOYAGE_API_KEY)")
                return None

            client = voyageai.Client(api_key=os.getenv('VOYAGE_API_KEY'))

            dimensions = {
                'voyage-2': 1024,
                'voyage-large-2': 1536,
            }.get(model, 1024)

            def embed_func(texts: List[str]) -> List[List[float]]:
                response = client.embed(texts=texts, model=model)
                return response.embeddings

            return self.benchmark_embedder(
                model_name=model,
                embed_func=embed_func,
                provider='voyage',
                dimensions=dimensions,
                batch_size=20
            )

        except ImportError:
            print(f"\nSkipping {model} (voyageai not installed)")
            return None
        except Exception as e:
            print(f"\nError benchmarking {model}: {e}")
            return None

    def benchmark_local(self, model: str = 'all-MiniLM-L6-v2') -> Optional[BenchmarkResult]:
        """Benchmark local sentence-transformers model."""
        try:
            from sentence_transformers import SentenceTransformer

            print(f"\nLoading local model {model}...")
            encoder = SentenceTransformer(model)

            dimensions = {
                'all-MiniLM-L6-v2': 384,
                'all-mpnet-base-v2': 768,
                'bge-base-en-v1.5': 768,
                'bge-large-en-v1.5': 1024,
            }.get(model, 384)

            def embed_func(texts: List[str]) -> List[List[float]]:
                embeddings = encoder.encode(texts, convert_to_numpy=True)
                return embeddings.tolist()

            return self.benchmark_embedder(
                model_name=model,
                embed_func=embed_func,
                provider='local',
                dimensions=dimensions,
                batch_size=16
            )

        except ImportError:
            print(f"\nSkipping {model} (sentence-transformers not installed)")
            return None
        except Exception as e:
            print(f"\nError benchmarking {model}: {e}")
            return None

    def run_benchmarks(self, models: Optional[Dict[str, List[str]]] = None) -> List[BenchmarkResult]:
        """
        Run benchmarks for multiple models.

        Args:
            models: Dictionary mapping provider to list of model names
                   If None, uses default model set

        Returns:
            List of BenchmarkResults
        """
        if models is None:
            models = {
                'openai': ['text-embedding-3-small', 'text-embedding-3-large'],
                'cohere': ['embed-english-v3.0'],
                'voyage': ['voyage-2'],
                'local': ['all-MiniLM-L6-v2', 'bge-base-en-v1.5']
            }

        self.results = []

        # Benchmark OpenAI models
        for model in models.get('openai', []):
            result = self.benchmark_openai(model)
            if result:
                self.results.append(result)

        # Benchmark Cohere models
        for model in models.get('cohere', []):
            result = self.benchmark_cohere(model)
            if result:
                self.results.append(result)

        # Benchmark Voyage models
        for model in models.get('voyage', []):
            result = self.benchmark_voyage(model)
            if result:
                self.results.append(result)

        # Benchmark local models
        for model in models.get('local', []):
            result = self.benchmark_local(model)
            if result:
                self.results.append(result)

        return self.results

    def print_summary(self):
        """Print benchmark summary table."""
        if not self.results:
            print("\nNo benchmark results available.")
            return

        print("\n" + "=" * 100)
        print("EMBEDDING MODEL BENCHMARK SUMMARY")
        print("=" * 100)

        # Header
        print(f"\n{'Model':<30} {'Provider':<10} {'Dims':<6} {'p50 (ms)':<10} {'p95 (ms)':<10} "
              f"{'Throughput':<15} {'Cost/1M':<10} {'MTEB':<8}")
        print("-" * 100)

        # Results
        for r in sorted(self.results, key=lambda x: x.latency_p50):
            throughput_str = f"{r.throughput_texts_per_sec:.1f} tx/s"
            cost_str = f"${r.cost_per_1m_tokens:.3f}" if r.cost_per_1m_tokens > 0 else "Free"
            mteb_str = f"{r.mteb_score:.1f}" if r.mteb_score else "N/A"

            print(f"{r.model_name:<30} {r.provider:<10} {r.dimensions:<6} "
                  f"{r.latency_p50:<10.2f} {r.latency_p95:<10.2f} "
                  f"{throughput_str:<15} {cost_str:<10} {mteb_str:<8}")

        print("\n" + "=" * 100)

    def visualize_results(self, save_path: Optional[str] = None):
        """
        Create visualization of benchmark results.

        Args:
            save_path: Optional path to save figure
        """
        if not self.results:
            print("\nNo results to visualize.")
            return

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Embedding Model Benchmark Results', fontsize=16, fontweight='bold')

        # Extract data
        models = [r.model_name for r in self.results]
        providers = [r.provider for r in self.results]
        colors = {'openai': '#10a37f', 'cohere': '#39594D', 'voyage': '#4B8BBE', 'local': '#646464'}
        model_colors = [colors.get(p, '#000000') for p in providers]

        # 1. Latency comparison
        ax = axes[0, 0]
        latencies_p50 = [r.latency_p50 for r in self.results]
        latencies_p95 = [r.latency_p95 for r in self.results]

        x = np.arange(len(models))
        width = 0.35
        ax.bar(x - width/2, latencies_p50, width, label='p50', color=model_colors, alpha=0.8)
        ax.bar(x + width/2, latencies_p95, width, label='p95', color=model_colors, alpha=0.5)

        ax.set_ylabel('Latency (ms)')
        ax.set_title('Latency by Model')
        ax.set_xticks(x)
        ax.set_xticklabels([m.replace('text-embedding-', '').replace('embed-', '')[:15] for m in models],
                          rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        # 2. Throughput comparison
        ax = axes[0, 1]
        throughputs = [r.throughput_texts_per_sec for r in self.results]
        ax.bar(models, throughputs, color=model_colors, alpha=0.8)
        ax.set_ylabel('Throughput (texts/sec)')
        ax.set_title('Throughput by Model')
        ax.set_xticklabels([m.replace('text-embedding-', '').replace('embed-', '')[:15] for m in models],
                          rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)

        # 3. Cost vs Quality (scatter)
        ax = axes[1, 0]
        costs = [r.cost_per_1k_texts() for r in self.results]
        qualities = [r.mteb_score if r.mteb_score else 0 for r in self.results]

        for i, r in enumerate(self.results):
            if r.mteb_score:
                ax.scatter(costs[i], qualities[i], s=200, c=model_colors[i], alpha=0.7)
                # Label with shortened model name
                label = r.model_name.replace('text-embedding-', '').replace('embed-', '')[:10]
                ax.annotate(label, (costs[i], qualities[i]),
                          xytext=(5, 5), textcoords='offset points', fontsize=8)

        ax.set_xlabel('Cost per 1K texts ($)')
        ax.set_ylabel('MTEB Score')
        ax.set_title('Quality vs Cost Trade-off')
        ax.grid(alpha=0.3)

        # 4. Dimensions vs Latency (scatter)
        ax = axes[1, 1]
        dimensions = [r.dimensions for r in self.results]

        ax.scatter(dimensions, latencies_p50, s=200, c=model_colors, alpha=0.7)
        for i, r in enumerate(self.results):
            label = r.model_name.replace('text-embedding-', '').replace('embed-', '')[:10]
            ax.annotate(label, (dimensions[i], latencies_p50[i]),
                       xytext=(5, 5), textcoords='offset points', fontsize=8)

        ax.set_xlabel('Embedding Dimensions')
        ax.set_ylabel('Latency p50 (ms)')
        ax.set_title('Dimensions vs Latency')
        ax.grid(alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"\nVisualization saved to {save_path}")
        else:
            plt.show()


def main():
    """Run embedding model benchmarks."""

    print("=" * 100)
    print("EMBEDDING MODEL BENCHMARK")
    print("=" * 100)
    print("\nThis benchmark will compare:")
    print("  - OpenAI: text-embedding-3-small, text-embedding-3-large")
    print("  - Cohere: embed-english-v3.0")
    print("  - Voyage AI: voyage-2")
    print("  - Local: all-MiniLM-L6-v2, bge-base-en-v1.5")
    print("\nMetrics: latency, throughput, cost, quality (MTEB score)")
    print("\nNote: API keys required for cloud providers (set as env vars)")
    print("=" * 100)

    # Initialize benchmark
    benchmark = EmbedderBenchmark()

    # Run benchmarks
    print("\nStarting benchmarks...")
    results = benchmark.run_benchmarks()

    # Print summary
    benchmark.print_summary()

    # Print recommendations
    print("\n" + "=" * 100)
    print("RECOMMENDATIONS")
    print("=" * 100)

    if results:
        # Best by latency (local)
        local_results = [r for r in results if r.provider == 'local']
        if local_results:
            fastest_local = min(local_results, key=lambda x: x.latency_p50)
            print(f"\nFastest Local Model: {fastest_local.model_name}")
            print(f"  - Latency p50: {fastest_local.latency_p50:.2f} ms")
            print(f"  - Dimensions: {fastest_local.dimensions}")
            print(f"  - MTEB Score: {fastest_local.mteb_score or 'N/A'}")
            print(f"  - Use case: High volume, tight budgets, data privacy")

        # Best API model (quality/cost balance)
        api_results = [r for r in results if r.provider != 'local' and r.mteb_score]
        if api_results:
            best_value = max(api_results, key=lambda x: x.quality_per_dollar())
            print(f"\nBest Value API Model: {best_value.model_name}")
            print(f"  - MTEB Score: {best_value.mteb_score:.1f}")
            print(f"  - Cost per 1K texts: ${best_value.cost_per_1k_texts():.4f}")
            print(f"  - Quality per dollar: {best_value.quality_per_dollar():.2f}")
            print(f"  - Use case: Production RAG systems")

        # Highest quality
        if api_results:
            best_quality = max(api_results, key=lambda x: x.mteb_score or 0)
            print(f"\nHighest Quality: {best_quality.model_name}")
            print(f"  - MTEB Score: {best_quality.mteb_score:.1f}")
            print(f"  - Dimensions: {best_quality.dimensions}")
            print(f"  - Cost per 1K texts: ${best_quality.cost_per_1k_texts():.4f}")
            print(f"  - Use case: Premium applications, accuracy-critical")

    print("\n" + "=" * 100)

    # Visualize
    print("\nGenerating visualization...")
    benchmark.visualize_results(save_path='benchmark_results.png')

    print("\nBenchmark complete!")


if __name__ == "__main__":
    main()
