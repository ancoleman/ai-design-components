"""
OpenAI Embedding with Redis Caching

Demonstrates content-addressable caching to reduce API costs by 80-90%.

Dependencies:
    pip install openai redis

Usage:
    python openai_cached.py

Environment Variables:
    OPENAI_API_KEY: Your OpenAI API key
    REDIS_HOST: Redis server host (default: localhost)
    REDIS_PORT: Redis server port (default: 6379)
"""

import hashlib
import json
import os
from typing import List, Dict, Optional
from openai import OpenAI
import redis


class CachedEmbedder:
    """OpenAI embedder with Redis content-addressable caching."""

    def __init__(
        self,
        model: str = "text-embedding-3-small",
        redis_host: str = "localhost",
        redis_port: int = 6379,
        cache_ttl: int = 86400 * 30  # 30 days
    ):
        """
        Initialize cached embedder.

        Args:
            model: OpenAI embedding model name
            redis_host: Redis server hostname
            redis_port: Redis server port
            cache_ttl: Cache time-to-live in seconds
        """
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=False
        )
        self.cache_ttl = cache_ttl

        # Statistics
        self.cache_hits = 0
        self.cache_misses = 0
        self.api_calls = 0

    def _cache_key(self, text: str) -> str:
        """
        Generate content-addressable cache key.

        Args:
            text: Input text

        Returns:
            Cache key (SHA-256 hash)
        """
        content_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        return f"embed:{self.model}:{content_hash}"

    def embed_single(self, text: str) -> List[float]:
        """
        Embed single text with caching.

        Args:
            text: Text to embed

        Returns:
            Embedding vector (list of floats)
        """
        cache_key = self._cache_key(text)

        # Check cache
        cached = self.redis_client.get(cache_key)
        if cached:
            self.cache_hits += 1
            return json.loads(cached)

        # Generate embedding via API
        self.cache_misses += 1
        self.api_calls += 1

        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            embedding = response.data[0].embedding

            # Cache result
            self.redis_client.setex(
                cache_key,
                self.cache_ttl,
                json.dumps(embedding)
            )

            return embedding

        except Exception as e:
            print(f"Error embedding text: {e}")
            raise

    def embed_batch(self, texts: List[str], batch_size: int = 2048) -> List[List[float]]:
        """
        Embed batch of texts with caching (up to 2,048 texts per API call).

        Args:
            texts: List of texts to embed
            batch_size: Maximum batch size for OpenAI API

        Returns:
            List of embedding vectors
        """
        if len(texts) > batch_size:
            # Split into multiple batches
            embeddings = []
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                embeddings.extend(self.embed_batch(batch, batch_size))
            return embeddings

        # Prepare result array and track uncached texts
        embeddings = []
        uncached_texts = []
        uncached_indices = []

        # Check cache for all texts
        for i, text in enumerate(texts):
            cache_key = self._cache_key(text)
            cached = self.redis_client.get(cache_key)

            if cached:
                self.cache_hits += 1
                embeddings.append(json.loads(cached))
            else:
                embeddings.append(None)
                uncached_texts.append(text)
                uncached_indices.append(i)

        # Generate embeddings for uncached texts
        if uncached_texts:
            self.cache_misses += len(uncached_texts)
            self.api_calls += 1

            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=uncached_texts
                )

                # Insert into results and cache
                for idx, data in zip(uncached_indices, response.data):
                    embedding = data.embedding
                    embeddings[idx] = embedding

                    # Cache result
                    cache_key = self._cache_key(texts[idx])
                    self.redis_client.setex(
                        cache_key,
                        self.cache_ttl,
                        json.dumps(embedding)
                    )

            except Exception as e:
                print(f"Error embedding batch: {e}")
                raise

        return embeddings

    def get_cache_stats(self) -> Dict[str, float]:
        """
        Get cache hit/miss statistics.

        Returns:
            Dictionary with cache statistics
        """
        total = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total * 100) if total > 0 else 0

        return {
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'total_requests': total,
            'hit_rate_pct': round(hit_rate, 2),
            'api_calls': self.api_calls,
            'api_savings_pct': round((1 - self.api_calls / max(1, total)) * 100, 2)
        }

    def clear_cache(self) -> int:
        """
        Clear all cached embeddings for this model.

        Returns:
            Number of keys deleted
        """
        pattern = f"embed:{self.model}:*"
        keys = self.redis_client.keys(pattern)
        if keys:
            return self.redis_client.delete(*keys)
        return 0


def main():
    """Example usage of CachedEmbedder."""

    print("OpenAI Embedding with Redis Caching Demo")
    print("=" * 60)

    # Initialize embedder
    embedder = CachedEmbedder(model="text-embedding-3-small")

    # Example 1: Single text embedding
    print("\n1. Single text embedding:")
    text = "What is the capital of France?"
    embedding = embedder.embed_single(text)
    print(f"   Text: {text}")
    print(f"   Embedding dimension: {len(embedding)}")
    print(f"   First 5 values: {embedding[:5]}")

    # Example 2: Embed same text again (cache hit)
    print("\n2. Embed same text again (should be cached):")
    embedding = embedder.embed_single(text)
    stats = embedder.get_cache_stats()
    print(f"   Cache hit rate: {stats['hit_rate_pct']}%")
    print(f"   API calls: {stats['api_calls']}")

    # Example 3: Batch embedding
    print("\n3. Batch embedding:")
    texts = [
        "Paris is the capital of France.",
        "London is the capital of the UK.",
        "Berlin is the capital of Germany.",
        "What is the capital of France?",  # Duplicate (cached)
        "Madrid is the capital of Spain."
    ]

    embeddings = embedder.embed_batch(texts)
    print(f"   Embedded {len(embeddings)} texts")
    print(f"   All embeddings have dimension: {len(embeddings[0])}")

    # Example 4: Cache statistics
    print("\n4. Cache statistics:")
    stats = embedder.get_cache_stats()
    print(f"   Total requests: {stats['total_requests']}")
    print(f"   Cache hits: {stats['cache_hits']}")
    print(f"   Cache misses: {stats['cache_misses']}")
    print(f"   Hit rate: {stats['hit_rate_pct']}%")
    print(f"   API calls: {stats['api_calls']}")
    print(f"   API call savings: {stats['api_savings_pct']}%")

    # Example 5: Cost estimation
    print("\n5. Cost estimation:")
    avg_tokens = 25  # Estimated average tokens per text
    total_tokens_without_cache = stats['total_requests'] * avg_tokens
    total_tokens_with_cache = stats['api_calls'] * avg_tokens
    cost_per_1m_tokens = 0.02  # text-embedding-3-small pricing

    cost_without_cache = (total_tokens_without_cache / 1_000_000) * cost_per_1m_tokens
    cost_with_cache = (total_tokens_with_cache / 1_000_000) * cost_per_1m_tokens
    savings = cost_without_cache - cost_with_cache

    print(f"   Without caching: ${cost_without_cache:.6f}")
    print(f"   With caching: ${cost_with_cache:.6f}")
    print(f"   Savings: ${savings:.6f} ({stats['api_savings_pct']}%)")

    print("\n" + "=" * 60)
    print("Demo complete!")


if __name__ == "__main__":
    main()
