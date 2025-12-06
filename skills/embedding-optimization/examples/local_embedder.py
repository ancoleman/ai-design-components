"""
Local Embedding with sentence-transformers

Demonstrates zero-cost local embedding with GPU acceleration.

Dependencies:
    pip install sentence-transformers torch

Usage:
    python local_embedder.py

Notes:
    - Automatically detects GPU (CUDA, MPS for Apple Silicon)
    - Falls back to CPU if no GPU available
    - First run downloads model (~90MB for all-MiniLM-L6-v2)
"""

from sentence_transformers import SentenceTransformer
from typing import List
import torch
import time


class LocalEmbedder:
    """Local embedding model with GPU acceleration."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        device: str = None,
        batch_size: int = 32
    ):
        """
        Initialize local embedder.

        Args:
            model_name: Model from sentence-transformers Hub
                Available models:
                - 'all-MiniLM-L6-v2': 384 dims, fast (22M params)
                - 'BAAI/bge-base-en-v1.5': 768 dims, SOTA quality (109M params)
                - 'BAAI/bge-large-en-v1.5': 1024 dims, max quality (335M params)
                - 'paraphrase-multilingual-MiniLM-L12-v2': 384 dims, 50+ languages
            device: 'cuda', 'mps' (Apple Silicon), 'cpu', or None (auto-detect)
            batch_size: Batch size for encoding (tune based on GPU memory)
        """
        if device is None:
            device = self._auto_detect_device()

        self.model = SentenceTransformer(model_name, device=device)
        self.model_name = model_name
        self.device = device
        self.batch_size = batch_size

        print(f"Loaded {model_name} on {device}")
        print(f"Embedding dimension: {self.get_embedding_dim()}")

    def _auto_detect_device(self) -> str:
        """Auto-detect best available device."""
        if torch.cuda.is_available():
            return 'cuda'
        elif torch.backends.mps.is_available():
            return 'mps'
        else:
            return 'cpu'

    def embed_single(self, text: str) -> List[float]:
        """
        Embed single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector (list of floats)
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_batch(
        self,
        texts: List[str],
        show_progress: bool = False,
        normalize_embeddings: bool = False
    ) -> List[List[float]]:
        """
        Embed batch of texts with optimized batching.

        Args:
            texts: List of texts to embed
            show_progress: Show progress bar (useful for large batches)
            normalize_embeddings: Normalize embeddings to unit length (for cosine similarity)

        Returns:
            List of embedding vectors (each is a list of floats)
        """
        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True,
            normalize_embeddings=normalize_embeddings
        )
        return embeddings.tolist()

    def get_embedding_dim(self) -> int:
        """Return embedding dimensionality."""
        return self.model.get_sentence_embedding_dimension()

    def get_max_seq_length(self) -> int:
        """Return maximum sequence length (in tokens)."""
        return self.model.get_max_seq_length()


def benchmark_throughput(embedder: LocalEmbedder, num_texts: int = 1000):
    """
    Benchmark embedding throughput.

    Args:
        embedder: LocalEmbedder instance
        num_texts: Number of texts to embed for benchmark
    """
    print(f"\nBenchmarking throughput ({num_texts} texts)...")

    # Generate sample texts
    texts = [
        f"This is sample text number {i} for benchmarking embedding throughput."
        for i in range(num_texts)
    ]

    # Benchmark
    start = time.time()
    embeddings = embedder.embed_batch(texts, show_progress=True)
    elapsed = time.time() - start

    throughput = num_texts / elapsed
    avg_latency = (elapsed / num_texts) * 1000  # ms per text

    print(f"\nBenchmark Results:")
    print(f"  Total texts: {num_texts}")
    print(f"  Total time: {elapsed:.2f}s")
    print(f"  Throughput: {throughput:.2f} texts/sec")
    print(f"  Avg latency: {avg_latency:.2f}ms per text")
    print(f"  Device: {embedder.device}")


def compare_models():
    """Compare different embedding models."""
    print("\nComparing different models...")
    print("=" * 60)

    models = [
        ("all-MiniLM-L6-v2", "Fast, small (384 dims)"),
        # Uncomment to test (requires download):
        # ("BAAI/bge-base-en-v1.5", "High quality (768 dims)"),
    ]

    sample_text = "What is machine learning?"

    for model_name, description in models:
        print(f"\nModel: {model_name}")
        print(f"Description: {description}")

        embedder = LocalEmbedder(model_name=model_name)

        # Embed sample
        start = time.time()
        embedding = embedder.embed_single(sample_text)
        latency = (time.time() - start) * 1000

        print(f"  Dimension: {len(embedding)}")
        print(f"  Latency: {latency:.2f}ms")
        print(f"  First 5 values: {[round(v, 4) for v in embedding[:5]]}")


def main():
    """Example usage of LocalEmbedder."""

    print("Local Embedding with sentence-transformers Demo")
    print("=" * 60)

    # Initialize embedder (auto-detects GPU)
    embedder = LocalEmbedder(model_name="all-MiniLM-L6-v2")

    print(f"\nDevice: {embedder.device}")
    print(f"Max sequence length: {embedder.get_max_seq_length()} tokens")

    # Example 1: Single text embedding
    print("\n1. Single text embedding:")
    text = "What is the capital of France?"
    embedding = embedder.embed_single(text)
    print(f"   Text: {text}")
    print(f"   Embedding dimension: {len(embedding)}")
    print(f"   First 5 values: {[round(v, 4) for v in embedding[:5]]}")

    # Example 2: Batch embedding
    print("\n2. Batch embedding:")
    texts = [
        "Paris is the capital of France.",
        "London is the capital of the UK.",
        "Berlin is the capital of Germany.",
        "Madrid is the capital of Spain.",
        "Rome is the capital of Italy."
    ]

    embeddings = embedder.embed_batch(texts)
    print(f"   Embedded {len(embeddings)} texts")
    print(f"   All embeddings have dimension: {len(embeddings[0])}")

    # Example 3: Semantic similarity
    print("\n3. Semantic similarity:")
    query = "French capital city"
    query_embedding = embedder.embed_single(query)

    # Calculate cosine similarity with each text
    def cosine_similarity(a, b):
        import numpy as np
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    print(f"   Query: {query}")
    for i, text in enumerate(texts):
        similarity = cosine_similarity(query_embedding, embeddings[i])
        print(f"   {text}: {similarity:.4f}")

    # Example 4: Normalized embeddings (for faster cosine similarity)
    print("\n4. Normalized embeddings (unit length):")
    normalized_embeddings = embedder.embed_batch(texts, normalize_embeddings=True)

    # With normalized embeddings, cosine similarity = dot product
    import numpy as np
    query_norm = embedder.embed_batch([query], normalize_embeddings=True)[0]

    print(f"   Query: {query}")
    for i, text in enumerate(texts):
        similarity = np.dot(query_norm, normalized_embeddings[i])
        print(f"   {text}: {similarity:.4f}")

    # Example 5: Throughput benchmark
    if embedder.device in ['cuda', 'mps']:
        benchmark_throughput(embedder, num_texts=1000)
    else:
        print("\n5. Throughput benchmark:")
        print("   Skipping (CPU inference is slow, use GPU for benchmarking)")

    # Example 6: Cost comparison
    print("\n6. Cost comparison (local vs. API):")
    print("   Local model (all-MiniLM-L6-v2):")
    print("   - API cost: $0 (free, runs locally)")
    print("   - Infrastructure: GPU recommended (~$150-400/month)")
    print("   - Throughput: 5,000-10,000 texts/sec (GPU)")
    print("\n   OpenAI API (text-embedding-3-small):")
    print("   - API cost: $0.02 per 1M tokens (~$0.50/month for 10M chars)")
    print("   - Infrastructure: None (managed)")
    print("   - Throughput: 1,000-5,000 texts/min (rate-limited)")
    print("\n   Break-even: Local is cost-effective above ~1M embeddings/month")

    print("\n" + "=" * 60)
    print("Demo complete!")


if __name__ == "__main__":
    main()
