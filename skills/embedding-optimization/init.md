# Embedding Optimization Skill - Master Plan

**Skill Name:** `embedding-optimization`
**Skill Level:** Low Level (Quick Reference - 300-500 tokens in SKILL.md)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Optimization Taxonomy](#optimization-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Python Implementations](#python-implementations)
7. [Library and Tool Recommendations](#library-and-tool-recommendations)
8. [Skill Structure Design](#skill-structure-design)
9. [Integration Points](#integration-points)
10. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

Vector embeddings are the foundation of modern AI retrieval systems, powering RAG (Retrieval Augmented Generation), semantic search, recommendation engines, and similarity detection. However, embedding optimization is often overlooked, leading to:

- **Cost Overruns:** Excessive API calls to embedding providers ($0.0001-0.00002 per 1K tokens adds up)
- **Latency Issues:** Slow embedding generation bottlenecks real-time applications
- **Poor Retrieval Quality:** Suboptimal chunking strategies reduce RAG accuracy
- **Wasted Storage:** High-dimensional embeddings consume excessive vector database space
- **Inefficient Caching:** Repeated embedding of identical content

**Market Drivers (2025):**
- **RAG Everywhere:** Every AI application now includes retrieval components
- **Cost Pressure:** OpenAI's `text-embedding-3-large` (3,072 dimensions) is overkill for many use cases
- **Open Source Models:** High-quality local embedding models (sentence-transformers) eliminate API dependency
- **Multi-Modal Embeddings:** Text, images, and code now share embedding spaces
- **Semantic Caching:** LLM providers (Anthropic, OpenAI) offer prompt caching; embeddings need similar patterns

**Strategic Value:**
1. **Universal RAG Foundation:** Every RAG system needs optimized embeddings
2. **Cost Reduction:** Proper caching and model selection can reduce embedding costs by 70-90%
3. **Performance Gains:** Local models + batching can achieve 10x throughput improvements
4. **Quality Improvement:** Better chunking strategies directly improve retrieval accuracy
5. **Scalability:** Optimized pipelines handle millions of documents efficiently

### How This Differs from Existing Solutions

**Existing Embedding Documentation:**
- **Provider Docs (OpenAI, Cohere):** Focus on API usage, not optimization strategies
- **Library Docs (sentence-transformers):** Model details without selection frameworks
- **RAG Tutorials:** End-to-end examples without performance tuning guidance
- **Academic Papers:** Theoretical chunking strategies without practical implementation patterns

**Our Approach:**
- **Decision-First Framework:** When to use OpenAI vs. local models, what chunk size for what content
- **Cost-Aware Patterns:** Caching strategies, batch processing, dimensionality reduction
- **Production-Ready Code:** Working Python examples with error handling and monitoring
- **Chunking Decision Tree:** Content type → Chunking strategy (fixed vs. semantic vs. recursive)
- **Performance Benchmarks:** Latency and throughput comparisons for common scenarios

### Target Audience

**Primary Users:**
- Backend engineers building RAG systems
- Data engineers ingesting documents into vector databases
- ML engineers optimizing retrieval pipelines
- Full-stack developers adding semantic search features

**Skill Level Assumptions:**
- Understands embeddings conceptually (vectors representing semantic meaning)
- Familiar with Python and basic API usage
- Knows what RAG is (retrieval + generation pattern)
- Needs tactical guidance on model selection, chunking, and optimization

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **Embedding Model Selection**
   - OpenAI `text-embedding-3-small` (1,536 dims) vs. `text-embedding-3-large` (3,072 dims)
   - Cohere `embed-english-v3.0` (1,024 dims) with compression
   - Open source models: `all-MiniLM-L6-v2` (384 dims), `BGE-base-en-v1.5` (768 dims)
   - When to use local vs. API-based models
   - Multi-lingual model considerations

2. **Chunking Strategies**
   - **Fixed-Size Chunking:** Simple, predictable (500-1,000 tokens per chunk)
   - **Semantic Chunking:** Split on paragraph/section boundaries (better context preservation)
   - **Recursive Chunking:** Hierarchical splitting (documents → sections → paragraphs)
   - **Sliding Window:** Overlapping chunks (prevents context loss at boundaries)
   - **Content-Aware Chunking:** Code (function-level), markdown (heading-level), tables (preserve structure)

3. **Dimensionality and Trade-offs**
   - **High Dimensionality (1,536-3,072 dims):** Better accuracy, higher storage costs, slower similarity search
   - **Low Dimensionality (384-768 dims):** Faster search, lower costs, acceptable quality for most use cases
   - Dimensionality reduction: Matryoshka embeddings (embed once, use at multiple dimensions)

4. **Batch Processing Optimization**
   - Batching API calls (OpenAI supports up to 2,048 inputs per request)
   - Parallel processing with rate limiting
   - Local model batching (sentence-transformers multi-GPU support)
   - Queue-based processing for large ingestion jobs

5. **Caching Strategies**
   - Content-addressable caching (hash content → cache embedding)
   - Redis/Memcached for hot embeddings
   - Database-backed embedding cache (PostgreSQL with vector extension)
   - Cache invalidation strategies (TTL vs. content-based)

6. **Performance Monitoring**
   - Latency tracking (embedding generation time)
   - Throughput measurement (embeddings per second)
   - Cost tracking (API usage, compute costs)
   - Quality metrics (retrieval accuracy, relevance scores)

### What This Skill Does NOT Cover

**Out of Scope:**
- **Vector Database Operations:** Covered by separate vector database skills (Pinecone, Weaviate, Qdrant)
- **RAG Architecture:** Full RAG system design (separate `building-ai-chat` skill covers this)
- **Fine-Tuning Embedding Models:** Training custom embedding models (advanced ML skill)
- **Multi-Modal Embeddings:** Image/audio embeddings (specialized skill)
- **Reranking:** Post-retrieval reranking strategies (covered in RAG skill)

**Boundary Cases (Minimal Coverage):**
- **Vector Similarity Algorithms:** Brief mention of cosine similarity, but implementation is in vector DB skill
- **Metadata Filtering:** Touch on attaching metadata, but filtering patterns are in vector DB skill

### Success Criteria

**A user successfully uses this skill when they can:**
1. Select the appropriate embedding model for their use case
2. Implement effective chunking strategies for different content types
3. Set up caching to reduce embedding API costs by 70%+
4. Batch process documents efficiently (1,000+ documents/minute)
5. Monitor embedding pipeline performance (latency, cost, quality)
6. Optimize dimensionality for their storage and search requirements

---

## Research Findings

### Research Date: December 3, 2025

**Research Tools Used:**
- Claude's knowledge (January 2025 cutoff)
- Industry best practices from RAG implementations
- Official documentation: OpenAI, Cohere, sentence-transformers

**Note:** MCP tools (Google Search Grounding, Context7) were unavailable during init.md creation. Research is based on Claude's training data and general knowledge of embedding optimization patterns as of January 2025.

### Key Trends for 2025

**1. Matryoshka Embeddings (Variable Dimensionality)**

Matryoshka Representation Learning allows training embedding models to be useful at multiple dimensions:
- Embed once with `text-embedding-3-large` (3,072 dims)
- Use at 256, 512, 1,024, or 3,072 dimensions depending on use case
- **Benefit:** Flexibility without re-embedding, progressive quality/cost trade-offs

**2. Open Source Model Parity**

Open source embedding models now match or exceed commercial quality:
- **BGE (BAAI General Embedding) v1.5:** State-of-the-art open source (768 dims)
- **E5 models:** Microsoft's multilingual embeddings (strong cross-lingual performance)
- **Nomic Embed:** Fully open (weights + data), 768 dims, reproducible
- **Adoption Driver:** Cost control and data privacy requirements

**3. Semantic Chunking Libraries**

Move from naive fixed-size chunking to content-aware splitting:
- **LangChain RecursiveCharacterTextSplitter:** Language-aware splitting (Python, JS, Markdown, LaTeX)
- **LlamaIndex SentenceSplitter:** Semantic boundary detection
- **Semantic Chunker (experimental):** Embedding-based chunk boundary detection
- **Benefit:** Better context preservation → improved retrieval quality

**4. Embedding Caching Patterns**

Inspired by LLM prompt caching (Anthropic's prompt caching, OpenAI's cached responses):
- **Content-Addressable Storage:** Hash document chunks → cache embeddings
- **Database-Backed Caching:** PostgreSQL with pgvector stores embeddings + original text
- **Redis for Hot Cache:** Fast lookups for frequently accessed embeddings
- **Cost Reduction:** 80-90% reduction in embedding API calls for repeated content

**5. Multi-Stage Retrieval**

Use cheap embeddings for initial retrieval, expensive embeddings for reranking:
- **Stage 1:** Fast retrieval with low-dimensional embeddings (384 dims)
- **Stage 2:** Rerank top-k results with high-dimensional embeddings (1,536 dims)
- **Benefit:** 3-5x cost reduction with minimal quality loss

### Embedding Model Landscape (2025)

**Commercial APIs:**

| Provider | Model | Dimensions | Cost (per 1M tokens) | Best For |
|----------|-------|-----------|----------------------|----------|
| OpenAI | text-embedding-3-small | 1,536 | $0.02 | General purpose, good balance |
| OpenAI | text-embedding-3-large | 3,072 | $0.13 | High accuracy, large corpora |
| Cohere | embed-english-v3.0 | 1,024 | $0.10 | English-only, compression support |
| Cohere | embed-multilingual-v3.0 | 1,024 | $0.10 | 100+ languages |
| Voyage AI | voyage-2 | 1,024 | $0.10 | Domain-specific (code, legal, medical) |

**Open Source Models (sentence-transformers):**

| Model | Dimensions | Parameters | Best For |
|-------|-----------|-----------|----------|
| all-MiniLM-L6-v2 | 384 | 22M | Fast inference, low resource |
| BGE-base-en-v1.5 | 768 | 109M | SOTA quality, English |
| BGE-large-en-v1.5 | 1,024 | 335M | Maximum quality, English |
| multilingual-e5-base | 768 | 278M | Cross-lingual retrieval |
| nomic-embed-text-v1 | 768 | 137M | Fully open, reproducible |

**Key Insight:** For most RAG use cases, `all-MiniLM-L6-v2` (384 dims, local) or `text-embedding-3-small` (1,536 dims, API) provide the best quality/cost/speed trade-off.

---

## Optimization Taxonomy

### Embedding Model Selection Matrix

**Decision Criteria:**

```
┌─────────────────────────────────────────────────────────────┐
│ EMBEDDING MODEL SELECTION FRAMEWORK                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Question 1: Do you have data privacy requirements?         │
│   ├─ YES → Use local models (sentence-transformers)        │
│   └─ NO → Continue to Question 2                          │
│                                                             │
│ Question 2: What is your query volume?                     │
│   ├─ <1M queries/month → OpenAI API (simple, reliable)    │
│   ├─ 1M-10M queries/month → Consider costs, evaluate both │
│   └─ >10M queries/month → Local models (cost-effective)   │
│                                                             │
│ Question 3: What is your quality requirement?              │
│   ├─ HIGHEST → text-embedding-3-large (3,072 dims)        │
│   ├─ HIGH → text-embedding-3-small (1,536 dims)           │
│   ├─ GOOD → BGE-base-en-v1.5 (768 dims, local)           │
│   └─ FAST → all-MiniLM-L6-v2 (384 dims, local)           │
│                                                             │
│ Question 4: Do you need multilingual support?              │
│   ├─ YES → Cohere embed-multilingual-v3.0 or e5-base     │
│   └─ NO → English-optimized models (BGE, MiniLM)         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Chunking Strategy Decision Tree

**Content Type → Chunking Strategy:**

```python
# Decision Framework
def select_chunking_strategy(content_type, content_length, use_case):
    """
    Select optimal chunking strategy based on content characteristics.

    Args:
        content_type: 'code', 'markdown', 'plaintext', 'legal', 'technical'
        content_length: Total document size in characters
        use_case: 'qa', 'search', 'summarization'

    Returns:
        Recommended chunking strategy and parameters
    """

    # Code: Function-level chunking
    if content_type == 'code':
        return {
            'strategy': 'recursive',
            'separators': ['\nclass ', '\ndef ', '\n\n', '\n'],
            'chunk_size': 1000,
            'chunk_overlap': 100
        }

    # Markdown: Heading-aware chunking
    if content_type == 'markdown':
        return {
            'strategy': 'recursive',
            'separators': ['\n## ', '\n### ', '\n\n', '\n'],
            'chunk_size': 800,
            'chunk_overlap': 100
        }

    # Legal/Technical: Semantic chunking (preserve context)
    if content_type in ['legal', 'technical']:
        return {
            'strategy': 'semantic',
            'chunk_size': 1500,  # Larger chunks preserve context
            'chunk_overlap': 200
        }

    # Q&A: Small chunks (precise retrieval)
    if use_case == 'qa':
        return {
            'strategy': 'fixed',
            'chunk_size': 500,
            'chunk_overlap': 50
        }

    # Search: Medium chunks (balance context and precision)
    if use_case == 'search':
        return {
            'strategy': 'fixed',
            'chunk_size': 800,
            'chunk_overlap': 100
        }

    # Summarization: Large chunks (maximum context)
    if use_case == 'summarization':
        return {
            'strategy': 'semantic',
            'chunk_size': 2000,
            'chunk_overlap': 200
        }

    # Default: Fixed-size with overlap
    return {
        'strategy': 'fixed',
        'chunk_size': 1000,
        'chunk_overlap': 100
    }
```

### Dimensionality Trade-off Matrix

| Dimensions | Storage (1M vectors) | Search Speed | Quality | Best Use Case |
|-----------|----------------------|--------------|---------|---------------|
| 384       | 1.5 GB              | 10ms p95     | Good    | Large-scale search, tight budgets |
| 768       | 3 GB                | 15ms p95     | High    | General purpose RAG |
| 1,536     | 6 GB                | 25ms p95     | Very High | High-quality retrieval |
| 3,072     | 12 GB               | 40ms p95     | Highest | Premium applications, small corpora |

**Key Insight:** For most applications, 768 dimensions (BGE-base-en-v1.5) offers the best quality/cost/speed balance.

---

## Decision Frameworks

### Framework 1: Model Selection (Cost vs. Quality)

**Scenario-Based Recommendations:**

**Scenario 1: Startup MVP (Limited Budget)**
- **Model:** `all-MiniLM-L6-v2` (local, free)
- **Dimensions:** 384
- **Chunking:** Fixed-size (500 tokens)
- **Caching:** Redis (hot cache only)
- **Expected Cost:** Infrastructure only (~$50/month for 10M vectors)

**Scenario 2: Production RAG (Medium Scale)**
- **Model:** `text-embedding-3-small` (OpenAI API)
- **Dimensions:** 1,536
- **Chunking:** Recursive (content-aware)
- **Caching:** PostgreSQL + pgvector (persistent cache)
- **Expected Cost:** $200-500/month (1-5M queries)

**Scenario 3: Enterprise (High Quality Requirements)**
- **Model:** `text-embedding-3-large` (OpenAI API)
- **Dimensions:** 3,072 (with Matryoshka reduction to 1,536 for search)
- **Chunking:** Semantic (paragraph-level)
- **Caching:** Multi-tier (Redis hot + PostgreSQL warm)
- **Expected Cost:** $1,000-5,000/month (10M+ queries)

**Scenario 4: Multi-Lingual Support**
- **Model:** `multilingual-e5-base` (local) or Cohere `embed-multilingual-v3.0` (API)
- **Dimensions:** 768-1,024
- **Chunking:** Language-aware recursive
- **Caching:** Content-addressable with language tagging
- **Expected Cost:** $300-1,000/month (mixed API + local)

### Framework 2: Chunking Strategy (Content Type → Strategy)

**Content Type Analysis:**

| Content Type | Chunking Strategy | Chunk Size | Overlap | Reasoning |
|-------------|-------------------|-----------|---------|-----------|
| **Documentation** | Recursive (heading-aware) | 800 | 100 | Preserve section context |
| **Code** | Recursive (function-level) | 1000 | 100 | Complete functions/classes |
| **Q&A Pairs** | Fixed (small) | 500 | 50 | Precise answer retrieval |
| **Legal Documents** | Semantic (large) | 1500 | 200 | Context-critical |
| **Blog Posts** | Semantic (paragraph) | 1000 | 100 | Natural boundaries |
| **Chat Transcripts** | Fixed (time-based) | 800 | 100 | Conversational flow |
| **Academic Papers** | Recursive (section) | 1200 | 150 | Logical structure |

### Framework 3: Caching Architecture (Query Volume → Strategy)

```
Query Volume Decision Tree:

<10K queries/month
├─ Simple: In-memory cache (Python dict or lru_cache)
└─ No persistence needed

10K-100K queries/month
├─ Redis: Fast, simple, scales horizontally
└─ TTL-based expiration (7-30 days)

100K-1M queries/month
├─ Redis (hot) + PostgreSQL (warm)
└─ Two-tier caching with intelligent promotion

>1M queries/month
├─ Redis (hot) + PostgreSQL + S3 (cold)
└─ Three-tier with content-addressable storage
└─ Automated cache warming based on access patterns
```

---

## Python Implementations

### Implementation 1: OpenAI Embedding with Caching

```python
"""
OpenAI embedding with content-addressable caching.
Reduces API costs by 80-90% for repeated content.
"""

import hashlib
import json
from typing import List, Dict
from openai import OpenAI
import redis

class CachedEmbedder:
    """OpenAI embedder with Redis caching."""

    def __init__(
        self,
        model: str = "text-embedding-3-small",
        redis_host: str = "localhost",
        redis_port: int = 6379,
        cache_ttl: int = 86400 * 30  # 30 days
    ):
        self.client = OpenAI()
        self.model = model
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=False)
        self.cache_ttl = cache_ttl
        self.cache_hits = 0
        self.cache_misses = 0

    def _cache_key(self, text: str) -> str:
        """Generate content-addressable cache key."""
        content_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        return f"embed:{self.model}:{content_hash}"

    def embed_single(self, text: str) -> List[float]:
        """Embed single text with caching."""
        cache_key = self._cache_key(text)

        # Check cache
        cached = self.redis_client.get(cache_key)
        if cached:
            self.cache_hits += 1
            return json.loads(cached)

        # Generate embedding
        self.cache_misses += 1
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

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed batch with caching (up to 2,048 texts)."""
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

        return embeddings

    def get_cache_stats(self) -> Dict[str, int]:
        """Return cache hit/miss statistics."""
        total = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total * 100) if total > 0 else 0
        return {
            'hits': self.cache_hits,
            'misses': self.cache_misses,
            'total': total,
            'hit_rate_pct': round(hit_rate, 2)
        }


# Usage Example
if __name__ == "__main__":
    embedder = CachedEmbedder(model="text-embedding-3-small")

    # Embed single text
    text = "What is the capital of France?"
    embedding = embedder.embed_single(text)
    print(f"Embedding dimension: {len(embedding)}")

    # Embed batch
    texts = [
        "Paris is the capital of France.",
        "London is the capital of the UK.",
        "Berlin is the capital of Germany."
    ]
    embeddings = embedder.embed_batch(texts)
    print(f"Batch embedded: {len(embeddings)} texts")

    # Cache stats
    stats = embedder.get_cache_stats()
    print(f"Cache hit rate: {stats['hit_rate_pct']}%")
```

### Implementation 2: Local Embedding with sentence-transformers

```python
"""
Local embedding with sentence-transformers.
Zero API costs, full data privacy, optimized batching.
"""

from sentence_transformers import SentenceTransformer
from typing import List
import torch

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
            model_name: Model from sentence-transformers
                - 'all-MiniLM-L6-v2': 384 dims, fast (22M params)
                - 'BAAI/bge-base-en-v1.5': 768 dims, SOTA quality (109M params)
                - 'BAAI/bge-large-en-v1.5': 1024 dims, max quality (335M params)
            device: 'cuda', 'mps' (Apple Silicon), or 'cpu' (auto-detected if None)
            batch_size: Batch size for encoding (tune based on GPU memory)
        """
        if device is None:
            if torch.cuda.is_available():
                device = 'cuda'
            elif torch.backends.mps.is_available():
                device = 'mps'
            else:
                device = 'cpu'

        self.model = SentenceTransformer(model_name, device=device)
        self.device = device
        self.batch_size = batch_size
        print(f"Loaded {model_name} on {device}")

    def embed_single(self, text: str) -> List[float]:
        """Embed single text."""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_batch(
        self,
        texts: List[str],
        show_progress: bool = False
    ) -> List[List[float]]:
        """
        Embed batch of texts with optimized batching.

        Args:
            texts: List of texts to embed
            show_progress: Show progress bar (useful for large batches)

        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        return embeddings.tolist()

    def get_embedding_dim(self) -> int:
        """Return embedding dimensionality."""
        return self.model.get_sentence_embedding_dimension()


# Usage Example
if __name__ == "__main__":
    # Fast model (384 dims)
    embedder = LocalEmbedder(model_name="all-MiniLM-L6-v2")

    # Single text
    text = "What is the capital of France?"
    embedding = embedder.embed_single(text)
    print(f"Embedding dimension: {len(embedding)}")

    # Batch processing (efficient for large volumes)
    texts = [
        "Paris is the capital of France.",
        "London is the capital of the UK.",
        "Berlin is the capital of Germany."
    ] * 100  # 300 texts

    embeddings = embedder.embed_batch(texts, show_progress=True)
    print(f"Batch embedded: {len(embeddings)} texts")
    print(f"Device: {embedder.device}")

    # High-quality model (768 dims) - uncomment to use
    # embedder_hq = LocalEmbedder(model_name="BAAI/bge-base-en-v1.5")
    # embedding_hq = embedder_hq.embed_single(text)
    # print(f"High-quality embedding dimension: {len(embedding_hq)}")
```

### Implementation 3: Intelligent Chunking (Recursive)

```python
"""
Intelligent recursive chunking for different content types.
Preserves semantic boundaries (paragraphs, headings, functions).
"""

from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter

class SmartChunker:
    """Content-aware chunking with recursive splitting."""

    # Separators for different content types
    SEPARATORS = {
        'markdown': ['\n## ', '\n### ', '\n#### ', '\n\n', '\n', ' ', ''],
        'code_python': ['\nclass ', '\ndef ', '\n\n', '\n', ' ', ''],
        'code_js': ['\nfunction ', '\nconst ', '\nclass ', '\n\n', '\n', ' ', ''],
        'plaintext': ['\n\n', '\n', '. ', ' ', ''],
    }

    def __init__(self, content_type: str = 'plaintext'):
        """
        Initialize chunker for specific content type.

        Args:
            content_type: 'markdown', 'code_python', 'code_js', 'plaintext'
        """
        self.content_type = content_type
        self.separators = self.SEPARATORS.get(content_type, self.SEPARATORS['plaintext'])

    def chunk(
        self,
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 100
    ) -> List[str]:
        """
        Split text into chunks using recursive splitting.

        Args:
            text: Input text to chunk
            chunk_size: Target chunk size in characters
            chunk_overlap: Overlap between chunks (prevents context loss)

        Returns:
            List of text chunks
        """
        splitter = RecursiveCharacterTextSplitter(
            separators=self.separators,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )

        chunks = splitter.split_text(text)
        return chunks

    def chunk_with_metadata(
        self,
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
        source_metadata: Dict = None
    ) -> List[Dict]:
        """
        Chunk text and attach metadata to each chunk.

        Args:
            text: Input text
            chunk_size: Target chunk size
            chunk_overlap: Overlap size
            source_metadata: Metadata to attach (e.g., document_id, title)

        Returns:
            List of dicts with 'text' and 'metadata' keys
        """
        chunks = self.chunk(text, chunk_size, chunk_overlap)

        result = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = source_metadata.copy() if source_metadata else {}
            chunk_metadata.update({
                'chunk_index': i,
                'total_chunks': len(chunks),
                'chunk_size': len(chunk)
            })

            result.append({
                'text': chunk,
                'metadata': chunk_metadata
            })

        return result


# Usage Examples
if __name__ == "__main__":
    # Example 1: Markdown documentation
    markdown_text = """
# Introduction

This is an introduction paragraph.

## Section 1

Content for section 1 goes here.
It can span multiple paragraphs.

## Section 2

Content for section 2 is here.
"""

    chunker = SmartChunker(content_type='markdown')
    chunks = chunker.chunk(markdown_text, chunk_size=100, chunk_overlap=20)
    print(f"Markdown chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}:\n{chunk[:80]}...")

    # Example 2: Python code
    python_code = """
class MyClass:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

def standalone_function():
    return "Hello"
"""

    code_chunker = SmartChunker(content_type='code_python')
    code_chunks = code_chunker.chunk(python_code, chunk_size=100, chunk_overlap=20)
    print(f"\nPython code chunks: {len(code_chunks)}")

    # Example 3: With metadata
    chunker = SmartChunker(content_type='plaintext')
    chunks_with_meta = chunker.chunk_with_metadata(
        text="Long document text here..." * 100,
        chunk_size=500,
        chunk_overlap=50,
        source_metadata={
            'document_id': 'doc_123',
            'title': 'Sample Document',
            'author': 'John Doe'
        }
    )
    print(f"\nChunks with metadata: {len(chunks_with_meta)}")
    print(f"First chunk metadata: {chunks_with_meta[0]['metadata']}")
```

### Implementation 4: Performance Monitoring

```python
"""
Embedding pipeline performance monitoring.
Track latency, throughput, costs, and cache efficiency.
"""

import time
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

    start_time: datetime = field(default_factory=datetime.now)

    def add_operation(
        self,
        num_texts: int,
        latency_ms: float,
        cache_hits: int = 0,
        api_calls: int = 1,
        cost_usd: float = 0.0
    ):
        """Record an embedding operation."""
        self.total_texts += num_texts
        self.total_embeddings += num_texts
        self.total_api_calls += api_calls
        self.total_cache_hits += cache_hits
        self.total_latency_ms += latency_ms
        self.total_cost_usd += cost_usd

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

        return {
            'total_texts': self.total_texts,
            'total_api_calls': self.total_api_calls,
            'cache_hit_rate_pct': round(cache_hit_rate, 2),
            'throughput_texts_per_sec': round(throughput, 2),
            'avg_latency_ms': round(avg_latency, 2),
            'total_cost_usd': round(self.total_cost_usd, 4),
            'elapsed_seconds': round(elapsed_seconds, 2)
        }


class MonitoredEmbedder:
    """Wrapper for any embedder with performance monitoring."""

    def __init__(
        self,
        embedder: any,
        cost_per_1k_tokens: float = 0.00002  # OpenAI text-embedding-3-small
    ):
        """
        Initialize monitored embedder.

        Args:
            embedder: Underlying embedder (CachedEmbedder or LocalEmbedder)
            cost_per_1k_tokens: API cost (0.0 for local models)
        """
        self.embedder = embedder
        self.cost_per_1k_tokens = cost_per_1k_tokens
        self.metrics = EmbeddingMetrics()

    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (4 chars per token)."""
        return len(text) // 4

    def embed_single(self, text: str) -> List[float]:
        """Embed with monitoring."""
        start = time.time()

        # Check if embedder has cache
        cache_hit = 0
        if hasattr(self.embedder, '_cache_key'):
            cache_key = self.embedder._cache_key(text)
            if self.embedder.redis_client.exists(cache_key):
                cache_hit = 1

        # Embed
        embedding = self.embedder.embed_single(text)

        # Record metrics
        latency_ms = (time.time() - start) * 1000
        tokens = self._estimate_tokens(text)
        cost = (tokens / 1000) * self.cost_per_1k_tokens

        self.metrics.add_operation(
            num_texts=1,
            latency_ms=latency_ms,
            cache_hits=cache_hit,
            api_calls=1 if cache_hit == 0 else 0,
            cost_usd=cost if cache_hit == 0 else 0
        )

        return embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed batch with monitoring."""
        start = time.time()

        # Check cache hits
        cache_hits = 0
        if hasattr(self.embedder, '_cache_key'):
            for text in texts:
                cache_key = self.embedder._cache_key(text)
                if self.embedder.redis_client.exists(cache_key):
                    cache_hits += 1

        # Embed
        embeddings = self.embedder.embed_batch(texts)

        # Record metrics
        latency_ms = (time.time() - start) * 1000
        total_tokens = sum(self._estimate_tokens(t) for t in texts)
        cost = (total_tokens / 1000) * self.cost_per_1k_tokens
        api_calls = 1 if cache_hits < len(texts) else 0

        self.metrics.add_operation(
            num_texts=len(texts),
            latency_ms=latency_ms,
            cache_hits=cache_hits,
            api_calls=api_calls,
            cost_usd=cost * (len(texts) - cache_hits) / len(texts)
        )

        return embeddings

    def get_metrics(self) -> Dict:
        """Get performance metrics summary."""
        return self.metrics.get_summary()


# Usage Example
if __name__ == "__main__":
    from openai import OpenAI
    import redis

    # Create cached embedder
    embedder = CachedEmbedder(model="text-embedding-3-small")

    # Wrap with monitoring
    monitored = MonitoredEmbedder(
        embedder=embedder,
        cost_per_1k_tokens=0.00002  # OpenAI pricing
    )

    # Embed some texts
    texts = [
        "What is machine learning?",
        "Explain deep learning.",
        "What is machine learning?",  # Duplicate (cache hit)
    ] * 10  # 30 texts

    embeddings = monitored.embed_batch(texts)

    # Get metrics
    metrics = monitored.get_metrics()
    print("\nPerformance Metrics:")
    print(f"  Total texts: {metrics['total_texts']}")
    print(f"  API calls: {metrics['total_api_calls']}")
    print(f"  Cache hit rate: {metrics['cache_hit_rate_pct']}%")
    print(f"  Throughput: {metrics['throughput_texts_per_sec']} texts/sec")
    print(f"  Avg latency: {metrics['avg_latency_ms']} ms")
    print(f"  Total cost: ${metrics['total_cost_usd']}")
```

---

## Library and Tool Recommendations

### Primary Libraries (Production-Ready)

**1. OpenAI Python SDK**
- **Purpose:** API-based embeddings (text-embedding-3-small, text-embedding-3-large)
- **Version:** 1.0+ (January 2025)
- **Installation:** `pip install openai`
- **Strengths:**
  - High quality embeddings (SOTA as of 2025)
  - Matryoshka embeddings (variable dimensionality)
  - Reliable infrastructure (99.9% uptime SLA)
  - Batch API support (up to 2,048 inputs)
- **Weaknesses:**
  - API costs ($0.02-0.13 per 1M tokens)
  - Rate limits (tier-dependent, up to 5,000 RPM)
  - Network latency (50-200ms per request)
- **Best For:** Production applications, high-quality requirements, moderate volume

**2. sentence-transformers**
- **Purpose:** Local embedding models (no API dependency)
- **Version:** 2.2+ (January 2025)
- **Installation:** `pip install sentence-transformers`
- **Strengths:**
  - Zero API costs (compute-only)
  - Full data privacy (no external calls)
  - GPU acceleration (CUDA, MPS for Apple Silicon)
  - Wide model selection (100+ models on HuggingFace)
- **Weaknesses:**
  - Requires GPU for fast inference (CPU is 10-50x slower)
  - Model management (download, storage)
  - Lower quality than OpenAI for some tasks
- **Best For:** High-volume applications, data privacy requirements, cost-sensitive projects

**3. LangChain Text Splitters**
- **Purpose:** Intelligent chunking (recursive, semantic, character-based)
- **Version:** 0.1+ (January 2025)
- **Installation:** `pip install langchain-text-splitters`
- **Strengths:**
  - Content-aware splitting (markdown, code, latex)
  - Configurable separators
  - Overlap support (prevents context loss)
  - Metadata preservation
- **Weaknesses:**
  - Large dependency (full LangChain ecosystem)
  - Overkill for simple fixed-size chunking
- **Best For:** Complex documents, multiple content types, production RAG systems

**4. Redis**
- **Purpose:** Fast caching for embeddings
- **Version:** 7.0+ (with RedisJSON module)
- **Installation:** `pip install redis`
- **Strengths:**
  - Sub-millisecond latency
  - TTL-based expiration
  - Horizontal scalability (Redis Cluster)
  - Simple key-value interface
- **Weaknesses:**
  - In-memory (expensive for large caches)
  - Requires separate Redis server
- **Best For:** Hot cache (frequently accessed embeddings), real-time applications

**5. PostgreSQL with pgvector**
- **Purpose:** Persistent embedding storage and caching
- **Version:** PostgreSQL 15+, pgvector 0.5+
- **Installation:** PostgreSQL extension (`CREATE EXTENSION vector`)
- **Strengths:**
  - Persistent storage (survives restarts)
  - ACID transactions
  - SQL queries (join with metadata)
  - Cost-effective (disk storage)
- **Weaknesses:**
  - Slower than Redis (5-20ms vs. <1ms)
  - Limited to 2,000 dimensions per vector (as of 2025)
- **Best For:** Warm cache (less frequently accessed), embedding storage with metadata

### Alternative Tools (Specialized Use Cases)

**Cohere Python SDK**
- **Purpose:** Multilingual embeddings, compression-aware embeddings
- **Installation:** `pip install cohere`
- **Best For:** 100+ language support, compression requirements

**Nomic Embed**
- **Purpose:** Fully open embedding model (weights + training data)
- **Installation:** `pip install sentence-transformers`, model: `nomic-ai/nomic-embed-text-v1`
- **Best For:** Reproducibility, academic research, full transparency

**LlamaIndex**
- **Purpose:** Full RAG framework (includes chunking, embedding, retrieval)
- **Installation:** `pip install llama-index`
- **Best For:** End-to-end RAG systems (not just embedding optimization)

---

## Skill Structure Design

### SKILL.md Structure (300-500 Tokens Target)

Given the **Low Level** classification (quick reference, tactical guidance), the SKILL.md will be concise and script-heavy:

```yaml
---
name: embedding-optimization
description: Optimizing vector embeddings for RAG systems through model selection, chunking strategies, caching, and performance tuning. Use when building semantic search, RAG pipelines, or document retrieval systems.
---

## Purpose

Optimize embedding generation for cost, performance, and quality in RAG/semantic search systems.

## When to Use This Skill

Trigger this skill when:
- Building RAG (Retrieval Augmented Generation) systems
- Implementing semantic search
- Optimizing embedding API costs
- Improving document retrieval quality
- Processing large document corpora

## Model Selection Framework

**Decision tree:** [reference: model-selection-guide.md]

Quick recommendations:
- **Startup/MVP:** `all-MiniLM-L6-v2` (local, 384 dims, fast)
- **Production:** `text-embedding-3-small` (API, 1,536 dims, balanced)
- **High Quality:** `text-embedding-3-large` (API, 3,072 dims, expensive)
- **Multilingual:** `multilingual-e5-base` (local, 768 dims)

## Chunking Strategies

**Content-aware chunking:** [reference: chunking-strategies.md]

Use `scripts/chunk_document.py` for intelligent chunking:
```bash
python scripts/chunk_document.py \
  --input document.txt \
  --content-type markdown \
  --chunk-size 800 \
  --overlap 100
```

## Caching Implementation

**80-90% cost reduction with content-addressable caching.**

Use `scripts/cached_embedder.py` for production caching:
```bash
# Embed with Redis caching
python scripts/cached_embedder.py \
  --model text-embedding-3-small \
  --input documents.jsonl \
  --output embeddings.npy \
  --cache-backend redis \
  --cache-ttl 2592000  # 30 days
```

## Performance Monitoring

**Track latency, throughput, cost, cache efficiency.**

[reference: performance-monitoring.md]

## Examples

See `examples/` directory:
- `openai_cached.py` - OpenAI with Redis caching
- `local_embedder.py` - sentence-transformers local embedding
- `smart_chunker.py` - Content-aware chunking
- `performance_monitor.py` - Pipeline monitoring
```

**Token Estimate:** ~400 tokens (fits Low Level target)

### Directory Structure

```
skills/embedding-optimization/
├── SKILL.md                        # Main skill file (400 tokens)
├── init.md                         # This file (master plan)
│
├── references/
│   ├── model-selection-guide.md   # Decision framework for models
│   ├── chunking-strategies.md     # Detailed chunking patterns
│   └── performance-monitoring.md  # Metrics and monitoring setup
│
├── scripts/
│   ├── cached_embedder.py         # Production-ready cached embedder
│   ├── chunk_document.py          # CLI for chunking documents
│   └── performance_monitor.py     # Monitoring wrapper
│
└── examples/
    ├── openai_cached.py           # OpenAI with caching example
    ├── local_embedder.py          # sentence-transformers example
    ├── smart_chunker.py           # Recursive chunking example
    └── README.md                  # Examples guide
```

### Progressive Disclosure Strategy

**Level 1: SKILL.md (Always Loaded)**
- When to use this skill (triggers)
- Quick model recommendations
- Script references for common operations
- ~400 tokens

**Level 2: Reference Files (Loaded on Demand)**
- `model-selection-guide.md`: Decision tree, cost comparison, quality benchmarks (~800 tokens)
- `chunking-strategies.md`: Content-type decision tree, examples, overlap strategies (~600 tokens)
- `performance-monitoring.md`: Metrics setup, monitoring patterns, cost tracking (~500 tokens)

**Level 3: Scripts (Executed Without Loading)**
- `scripts/cached_embedder.py`: Production-ready cached embedding (ZERO tokens loaded, only executed)
- `scripts/chunk_document.py`: CLI chunking tool (ZERO tokens loaded)
- `scripts/performance_monitor.py`: Monitoring wrapper (ZERO tokens loaded)

**Total Context Budget:**
- SKILL.md: 400 tokens (always)
- References: 1,900 tokens (on-demand)
- Scripts: 0 tokens (executed, not loaded)
- **Grand Total: ~2,300 tokens worst case** (well under Low Level target)

---

## Integration Points

### Upstream Skills (Dependencies)

**This skill depends on:**

1. **None (Standalone Skill)**
   - Embedding optimization is foundational; no upstream dependencies
   - Can be used independently for any embedding pipeline

### Downstream Skills (Consumers)

**This skill supports:**

1. **RAG/AI Chat Systems**
   - `building-ai-chat`: Uses optimized embeddings for retrieval
   - **Integration:** Pass embedder instance to RAG pipeline
   - **Example:** `rag_pipeline.py` uses `CachedEmbedder` for document encoding

2. **Vector Databases**
   - `databases-vector`: Stores embeddings generated by this skill
   - **Integration:** Embeddings flow into Pinecone, Weaviate, Qdrant, pgvector
   - **Example:** Chunked documents → embeddings → vector DB ingestion

3. **Document Processing**
   - `ingesting-data`: Document ingestion pipelines use chunking strategies
   - **Integration:** SmartChunker prepares documents for embedding
   - **Example:** PDF/Markdown ingestion → chunking → embedding → storage

4. **Search/Filter Systems**
   - `implementing-search-filter`: Semantic search uses embeddings
   - **Integration:** Query embedding + document embedding → similarity search
   - **Example:** User query → embed → search vector DB → return results

### Cross-Skill Patterns

**Pattern 1: RAG Pipeline Integration**
```
Document → Chunk (embedding-optimization) →
Embed (embedding-optimization) →
Store (databases-vector) →
Retrieve (building-ai-chat)
```

**Pattern 2: Semantic Search**
```
Query → Embed (embedding-optimization) →
Search (databases-vector) →
Rank (implementing-search-filter) →
Display
```

**Pattern 3: Multi-Stage Retrieval**
```
Query → Cheap Embedding (384 dims) →
Initial Search (databases-vector) →
Rerank with Expensive Embedding (1,536 dims) →
Return Top-K
```

---

## Implementation Roadmap

### Phase 1: Core Skill (Week 1)

**Deliverables:**
1. **SKILL.md** - Main skill file (~400 tokens)
2. **references/model-selection-guide.md** - Decision framework
3. **references/chunking-strategies.md** - Chunking patterns
4. **examples/openai_cached.py** - Working caching example
5. **examples/local_embedder.py** - sentence-transformers example

**Success Criteria:**
- User can select embedding model based on requirements
- User can implement caching to reduce costs by 70%+
- User can chunk documents appropriately for their content type

### Phase 2: Production Scripts (Week 2)

**Deliverables:**
1. **scripts/cached_embedder.py** - Production-ready cached embedder CLI
2. **scripts/chunk_document.py** - Chunking CLI tool
3. **scripts/performance_monitor.py** - Monitoring wrapper
4. **references/performance-monitoring.md** - Monitoring guide

**Success Criteria:**
- User can run production embedding pipeline from CLI
- User can monitor latency, throughput, cost, cache efficiency
- Scripts handle errors gracefully (rate limits, network failures)

### Phase 3: Advanced Patterns (Week 3)

**Deliverables:**
1. **examples/multi_stage_retrieval.py** - Cheap initial search + expensive reranking
2. **examples/batch_processor.py** - Large-scale document processing
3. **examples/semantic_chunker.py** - Embedding-based chunk boundary detection
4. **Integration examples** - RAG pipeline, vector DB ingestion

**Success Criteria:**
- User can implement multi-stage retrieval (70% cost reduction)
- User can process 10,000+ documents efficiently (batch processing)
- Clear integration patterns with vector databases and RAG systems

### Phase 4: Testing and Validation (Week 4)

**Deliverables:**
1. **Evaluation suite** - Test scenarios for common use cases
2. **Performance benchmarks** - Latency/throughput/cost comparisons
3. **Documentation polish** - Clear examples, troubleshooting guide
4. **Integration testing** - Verify compatibility with vector DB skills

**Success Criteria:**
- All examples run successfully
- Performance benchmarks documented
- Integration points validated with downstream skills

---

## Appendix: Quick Reference Tables

### Model Comparison Matrix

| Model | Provider | Dims | Cost (1M tokens) | Quality | Speed | Best For |
|-------|---------|------|------------------|---------|-------|----------|
| text-embedding-3-small | OpenAI | 1,536 | $0.02 | High | Fast | General purpose |
| text-embedding-3-large | OpenAI | 3,072 | $0.13 | Highest | Medium | Premium quality |
| all-MiniLM-L6-v2 | Local | 384 | $0 (compute) | Good | Very Fast | High volume |
| BGE-base-en-v1.5 | Local | 768 | $0 (compute) | High | Fast | Quality + cost |
| BGE-large-en-v1.5 | Local | 1,024 | $0 (compute) | Highest | Medium | Max quality local |
| embed-english-v3.0 | Cohere | 1,024 | $0.10 | High | Fast | English-only |
| embed-multilingual-v3.0 | Cohere | 1,024 | $0.10 | High | Fast | 100+ languages |

### Chunking Size Recommendations

| Use Case | Chunk Size | Overlap | Strategy | Reasoning |
|----------|-----------|---------|----------|-----------|
| Q&A / FAQ | 500 | 50 | Fixed | Precise answer retrieval |
| Documentation | 800 | 100 | Recursive (headings) | Preserve sections |
| Code | 1,000 | 100 | Recursive (functions) | Complete functions |
| Legal/Technical | 1,500 | 200 | Semantic | Context-critical |
| Blog Posts | 1,000 | 100 | Semantic (paragraphs) | Natural boundaries |
| Chat Logs | 800 | 100 | Fixed (time-based) | Conversational flow |
| Academic Papers | 1,200 | 150 | Recursive (sections) | Logical structure |

### Caching ROI Calculator

**Example Scenario:**
- 10,000 documents
- Average 5 chunks per document = 50,000 chunks
- 20% duplicate content (documentation, repeated sections)

**Without Caching:**
- API calls: 50,000
- Cost: 50,000 × (500 tokens / 1,000) × $0.00002 = $0.50

**With Caching:**
- API calls: 40,000 (20% cache hits)
- Cost: 40,000 × (500 tokens / 1,000) × $0.00002 = $0.40
- **Savings: 20%**

**With Aggressive Caching (60% hit rate):**
- API calls: 20,000
- Cost: $0.20
- **Savings: 60%**

**Lesson:** Even modest cache hit rates (20-40%) provide significant cost savings. For production systems with repeated queries or document updates, cache hit rates of 70-90% are achievable.

---

**End of Master Plan**

This init.md provides the complete strategic and tactical foundation for the embedding-optimization skill. Next step: Create SKILL.md (400 tokens) following the progressive disclosure pattern outlined above.
