# Hybrid Search: Combining Vector and Keyword Search

## Table of Contents

- [Overview](#overview)
- [Why Hybrid Search](#why-hybrid-search)
- [Core Concepts](#core-concepts)
  - [Vector Search (Semantic)](#vector-search-semantic)
  - [Keyword Search (BM25)](#keyword-search-bm25)
  - [Fusion Strategies](#fusion-strategies)
- [Reciprocal Rank Fusion (RRF)](#reciprocal-rank-fusion-rrf)
- [Weighted Scoring Approaches](#weighted-scoring-approaches)
- [Implementation by Platform](#implementation-by-platform)
  - [Qdrant](#qdrant)
  - [Pinecone](#pinecone)
  - [Weaviate](#weaviate)
  - [pgvector](#pgvector)
- [Advanced Patterns](#advanced-patterns)
- [Performance Optimization](#performance-optimization)
- [Evaluation](#evaluation)

## Overview

Hybrid search combines vector similarity search (semantic understanding) with traditional keyword search (exact matching) to achieve superior retrieval quality. This approach addresses the limitations of each method when used in isolation.

**Key benefit:** Retrieval quality improvement of 15-30% over vector-only search in production RAG systems.

## Why Hybrid Search

### Vector Search Limitations

**Strengths:**
- Captures semantic meaning ("OAuth token renewal" ≈ "refresh authentication credentials")
- Handles synonyms and paraphrasing automatically
- Language-agnostic similarity

**Weaknesses:**
- May miss exact technical terms (API names, error codes)
- Can retrieve semantically similar but contextually wrong results
- Struggles with acronyms and identifiers

### Keyword Search Limitations

**Strengths:**
- Exact matches for technical terms ("refresh_token" literal)
- Fast lookup for known phrases
- Deterministic and explainable

**Weaknesses:**
- Misses synonyms and paraphrases
- No understanding of semantic meaning
- Sensitive to typos and variations

### Hybrid Advantage

Combining both methods provides:
- **Recall:** Vector search finds conceptually similar content
- **Precision:** Keyword search ensures important terms are present
- **Robustness:** Complementary strengths cover each method's weaknesses

## Core Concepts

### Vector Search (Semantic)

Uses embedding models to convert text into high-dimensional vectors, then computes similarity using distance metrics.

**Distance metrics:**
- **Cosine similarity:** Most common, works with normalized embeddings
- **Euclidean distance:** Absolute distance in vector space
- **Dot product:** Efficient for normalized vectors

**Formula (Cosine):**
```
similarity = (A · B) / (||A|| × ||B||)
```

### Keyword Search (BM25)

BM25 (Best Matching 25) is a probabilistic ranking function for keyword matching.

**Formula:**
```
BM25(D,Q) = Σ IDF(qi) × (f(qi,D) × (k1 + 1)) / (f(qi,D) + k1 × (1 - b + b × |D| / avgdl))
```

Where:
- `f(qi,D)`: Term frequency of query term qi in document D
- `|D|`: Document length
- `avgdl`: Average document length
- `k1`: Term frequency saturation (typical: 1.2)
- `b`: Length normalization (typical: 0.75)
- `IDF(qi)`: Inverse document frequency

**Key parameters:**
- `k1 = 1.2`: Controls term frequency saturation
- `b = 0.75`: Controls document length penalty

### Fusion Strategies

Three primary approaches to combine vector and keyword results:

1. **Reciprocal Rank Fusion (RRF)** - Rank-based merging
2. **Weighted Scoring** - Linear combination of normalized scores
3. **Re-ranking** - Two-stage retrieval with cross-encoder

## Reciprocal Rank Fusion (RRF)

RRF combines ranked lists without requiring normalized scores, making it robust and implementation-agnostic.

### Algorithm

**Formula:**
```
RRF_score(d) = Σ 1 / (k + rank_i(d))
```

Where:
- `d`: Document
- `rank_i(d)`: Rank of document d in result set i
- `k`: Constant (typical: 60)

### Example Calculation

```
Query: "OAuth refresh token implementation"

Vector Search Results:
1. Doc A (rank 1)
2. Doc B (rank 2)
3. Doc C (rank 3)

Keyword Search Results:
1. Doc B (rank 1)
2. Doc D (rank 2)
3. Doc A (rank 3)

RRF Scores (k=60):
Doc A: 1/(60+1) + 1/(60+3) = 0.0164 + 0.0159 = 0.0323
Doc B: 1/(60+2) + 1/(60+1) = 0.0161 + 0.0164 = 0.0325 ← Winner
Doc C: 1/(60+3) + 0 = 0.0159
Doc D: 0 + 1/(60+2) = 0.0161

Final Ranking: B, A, D, C
```

### Characteristics

**Advantages:**
- No score normalization required
- Robust to score scale differences
- Simple to implement
- Works across different search systems

**Disadvantages:**
- Ignores absolute score magnitudes
- Treats all rank positions equally within the formula
- May not fully leverage high-confidence matches

### Tuning the k Parameter

- **k = 60**: Default, balanced approach
- **k = 10-30**: Emphasizes top-ranked results more strongly
- **k = 100-200**: More gradual rank decay, considers more results

## Weighted Scoring Approaches

Linear combination of normalized vector and keyword scores.

### Normalization Methods

**Min-Max Normalization:**
```python
normalized_score = (score - min_score) / (max_score - min_score)
```

**Z-Score Normalization:**
```python
normalized_score = (score - mean_score) / std_dev
```

### Weighted Combination

**Formula:**
```
hybrid_score = (alpha × vector_score) + ((1 - alpha) × keyword_score)
```

Where `alpha` ∈ [0, 1] controls the balance.

**Recommended alpha values:**
- `alpha = 0.7`: Semantic-heavy (general Q&A, conversational)
- `alpha = 0.5`: Balanced (most RAG applications)
- `alpha = 0.3`: Keyword-heavy (technical documentation, code search)

### Adaptive Weighting

Adjust alpha based on query characteristics:

```python
def calculate_alpha(query: str) -> float:
    """
    Adjust semantic vs keyword weight based on query type.
    """
    # Technical terms suggest keyword importance
    technical_terms = ["API", "function", "class", "error", "code"]
    has_technical = any(term in query for term in technical_terms)

    # Question words suggest semantic importance
    question_words = ["how", "why", "what", "when", "explain"]
    is_question = any(word in query.lower() for word in question_words)

    if has_technical and not is_question:
        return 0.3  # Keyword-heavy
    elif is_question and not has_technical:
        return 0.7  # Semantic-heavy
    else:
        return 0.5  # Balanced
```

## Implementation by Platform

### Architecture Overview

```
User Query: "OAuth refresh token implementation"
           │
    ┌──────┴──────┐
    │             │
Vector Search   BM25 Search
(Semantic)      (Keyword)
    │             │
Top 20 docs   Top 20 docs
    │             │
    └──────┬──────┘
           │
   Reciprocal Rank Fusion
   (Merge + Re-rank)
           │
    Final Top 5 Results
```

---

### Qdrant

Qdrant provides built-in hybrid search with fusion support.

#### Basic Hybrid Search

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    SearchRequest,
    Prefetch,
    QueryEnum,
    FusionQuery
)

client = QdrantClient("localhost", port=6333)

# Hybrid search with RRF fusion
results = client.query_points(
    collection_name="documents",
    prefetch=[
        # Vector search prefetch
        Prefetch(
            query=query_vector,
            limit=20
        ),
        # Keyword search prefetch
        Prefetch(
            query=QueryEnum(text="OAuth refresh token"),
            using="text-index",  # Named text index
            limit=20
        )
    ],
    query=FusionQuery(fusion="rrf"),  # Reciprocal Rank Fusion
    limit=5
)
```

#### Collection Setup for Hybrid Search

```python
from qdrant_client.models import (
    VectorParams,
    Distance,
    TextIndexParams,
    TextIndexType,
    TokenizerType
)

# Create collection with vector and text indexes
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=1024,
        distance=Distance.COSINE
    )
)

# Create named text index for BM25
client.create_payload_index(
    collection_name="documents",
    field_name="text",
    field_schema=TextIndexParams(
        type=TextIndexType.TEXT,
        tokenizer=TokenizerType.WORD,
        min_token_len=2,
        max_token_len=20,
        lowercase=True
    ),
    field_type="text"
)
```

#### Advanced: Custom Fusion Weights

```python
# Weighted scoring instead of RRF
results = client.query_points(
    collection_name="documents",
    prefetch=[
        Prefetch(query=query_vector, limit=20),
        Prefetch(query=QueryEnum(text=query_text), using="text-index", limit=20)
    ],
    query=FusionQuery(
        fusion="score",  # Use score-based fusion
        weights=[0.7, 0.3]  # 70% vector, 30% keyword
    ),
    limit=5
)
```

### Pinecone

Pinecone supports hybrid search through sparse-dense vectors.

#### Setup with Sparse Embeddings

```python
from pinecone import Pinecone, ServerlessSpec
from pinecone_text.sparse import BM25Encoder

# Initialize
pc = Pinecone(api_key="your-api-key")
bm25 = BM25Encoder()

# Create index with hybrid support
index = pc.create_index(
    name="hybrid-search",
    dimension=1024,
    metric="dotproduct",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)

# Fit BM25 on corpus
bm25.fit(documents)

# Upsert with sparse and dense vectors
index.upsert(
    vectors=[
        {
            "id": str(i),
            "values": dense_vector,  # From OpenAI/Voyage
            "sparse_values": bm25.encode_documents(doc),
            "metadata": {"text": doc}
        }
        for i, doc in enumerate(documents)
    ]
)
```

#### Hybrid Query

```python
# Query with both dense and sparse
query_dense = get_embedding(query_text)
query_sparse = bm25.encode_queries(query_text)

results = index.query(
    vector=query_dense,
    sparse_vector=query_sparse,
    top_k=5,
    alpha=0.5  # Balance between dense (1.0) and sparse (0.0)
)
```

#### Custom Alpha Tuning

```python
def hybrid_search(query: str, alpha: float = 0.5):
    """
    Hybrid search with configurable semantic vs keyword balance.

    Args:
        query: Search query string
        alpha: Weight for dense vectors (0.0 = sparse only, 1.0 = dense only)
    """
    query_dense = get_embedding(query)
    query_sparse = bm25.encode_queries(query)

    results = index.query(
        vector=query_dense,
        sparse_vector=query_sparse,
        top_k=10,
        alpha=alpha
    )

    return results
```

### Weaviate

Weaviate provides native hybrid search with automatic score normalization.

#### Basic Hybrid Query

```python
import weaviate
from weaviate.classes.query import HybridFusion

client = weaviate.connect_to_local()

collection = client.collections.get("Document")

# Hybrid search with RRF
results = collection.query.hybrid(
    query="OAuth refresh token implementation",
    alpha=0.5,  # 0.5 = balanced, 0 = BM25 only, 1 = vector only
    fusion_type=HybridFusion.RANKED,  # RRF fusion
    limit=5
)

for item in results.objects:
    print(f"Score: {item.metadata.score}")
    print(f"Text: {item.properties['text']}")
```

#### Schema Definition

```python
import weaviate.classes.config as wc

# Create collection with vectorizer
client.collections.create(
    name="Document",
    vectorizer_config=wc.Configure.Vectorizer.text2vec_openai(
        model="text-embedding-3-large"
    ),
    properties=[
        wc.Property(
            name="text",
            data_type=wc.DataType.TEXT,
            tokenization=wc.Tokenization.WORD  # Enable BM25
        )
    ]
)
```

#### Fusion Types

```python
from weaviate.classes.query import HybridFusion

# Ranked Fusion (RRF)
results_rrf = collection.query.hybrid(
    query="OAuth implementation",
    fusion_type=HybridFusion.RANKED,
    limit=5
)

# Relative Score Fusion (weighted)
results_relative = collection.query.hybrid(
    query="OAuth implementation",
    fusion_type=HybridFusion.RELATIVE_SCORE,
    alpha=0.7,
    limit=5
)
```

### pgvector

PostgreSQL with pgvector requires manual implementation of hybrid search.

#### Schema Setup

```sql
-- Enable extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- For text search

-- Create table with vector and text search
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1024),
    metadata JSONB,
    ts_vector tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED
);

-- Indexes
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX ON documents USING GIN (ts_vector);
```

#### RRF Implementation in SQL

```sql
WITH vector_search AS (
    SELECT
        id,
        content,
        1 - (embedding <=> $1::vector) AS vector_score,
        ROW_NUMBER() OVER (ORDER BY embedding <=> $1::vector) AS vector_rank
    FROM documents
    ORDER BY embedding <=> $1::vector
    LIMIT 20
),
keyword_search AS (
    SELECT
        id,
        content,
        ts_rank(ts_vector, plainto_tsquery('english', $2)) AS keyword_score,
        ROW_NUMBER() OVER (ORDER BY ts_rank(ts_vector, plainto_tsquery('english', $2)) DESC) AS keyword_rank
    FROM documents
    WHERE ts_vector @@ plainto_tsquery('english', $2)
    ORDER BY ts_rank(ts_vector, plainto_tsquery('english', $2)) DESC
    LIMIT 20
),
rrf_scores AS (
    SELECT
        COALESCE(v.id, k.id) AS id,
        COALESCE(v.content, k.content) AS content,
        COALESCE(1.0 / (60 + v.vector_rank), 0) + COALESCE(1.0 / (60 + k.keyword_rank), 0) AS rrf_score
    FROM vector_search v
    FULL OUTER JOIN keyword_search k ON v.id = k.id
)
SELECT id, content, rrf_score
FROM rrf_scores
ORDER BY rrf_score DESC
LIMIT 5;
```

#### Python Implementation with SQLAlchemy

```python
from sqlalchemy import text
from pgvector.sqlalchemy import Vector

def hybrid_search_rrf(
    session,
    query_text: str,
    query_vector: list[float],
    k: int = 60,
    limit: int = 5
):
    """
    Hybrid search using RRF in PostgreSQL.
    """
    sql = text("""
        WITH vector_search AS (
            SELECT
                id,
                content,
                metadata,
                ROW_NUMBER() OVER (ORDER BY embedding <=> :vector) AS rank
            FROM documents
            ORDER BY embedding <=> :vector
            LIMIT 20
        ),
        keyword_search AS (
            SELECT
                id,
                content,
                metadata,
                ROW_NUMBER() OVER (
                    ORDER BY ts_rank(ts_vector, plainto_tsquery('english', :query)) DESC
                ) AS rank
            FROM documents
            WHERE ts_vector @@ plainto_tsquery('english', :query)
            ORDER BY ts_rank(ts_vector, plainto_tsquery('english', :query)) DESC
            LIMIT 20
        )
        SELECT
            COALESCE(v.id, k.id) AS id,
            COALESCE(v.content, k.content) AS content,
            COALESCE(v.metadata, k.metadata) AS metadata,
            (COALESCE(1.0 / (:k + v.rank), 0) +
             COALESCE(1.0 / (:k + k.rank), 0)) AS score
        FROM vector_search v
        FULL OUTER JOIN keyword_search k ON v.id = k.id
        ORDER BY score DESC
        LIMIT :limit
    """)

    results = session.execute(
        sql,
        {
            "vector": query_vector,
            "query": query_text,
            "k": k,
            "limit": limit
        }
    ).fetchall()

    return results
```

#### Weighted Scoring Approach

```python
def hybrid_search_weighted(
    session,
    query_text: str,
    query_vector: list[float],
    alpha: float = 0.5,
    limit: int = 5
):
    """
    Hybrid search using weighted score combination.

    Args:
        alpha: Weight for vector score (0.0 = keyword only, 1.0 = vector only)
    """
    sql = text("""
        WITH vector_search AS (
            SELECT
                id,
                content,
                metadata,
                1 - (embedding <=> :vector) AS score
            FROM documents
            ORDER BY embedding <=> :vector
            LIMIT 20
        ),
        keyword_search AS (
            SELECT
                id,
                content,
                metadata,
                ts_rank(ts_vector, plainto_tsquery('english', :query)) AS score
            FROM documents
            WHERE ts_vector @@ plainto_tsquery('english', :query)
            ORDER BY ts_rank(ts_vector, plainto_tsquery('english', :query)) DESC
            LIMIT 20
        ),
        normalized AS (
            SELECT
                id,
                content,
                metadata,
                'vector' AS source,
                (score - MIN(score) OVER ()) /
                NULLIF(MAX(score) OVER () - MIN(score) OVER (), 0) AS norm_score
            FROM vector_search
            UNION ALL
            SELECT
                id,
                content,
                metadata,
                'keyword' AS source,
                (score - MIN(score) OVER ()) /
                NULLIF(MAX(score) OVER () - MIN(score) OVER (), 0) AS norm_score
            FROM keyword_search
        )
        SELECT
            id,
            content,
            metadata,
            SUM(
                CASE
                    WHEN source = 'vector' THEN :alpha * norm_score
                    WHEN source = 'keyword' THEN (1 - :alpha) * norm_score
                END
            ) AS hybrid_score
        FROM normalized
        GROUP BY id, content, metadata
        ORDER BY hybrid_score DESC
        LIMIT :limit
    """)

    results = session.execute(
        sql,
        {
            "vector": query_vector,
            "query": query_text,
            "alpha": alpha,
            "limit": limit
        }
    ).fetchall()

    return results
```

---

## Advanced Patterns

### Two-Stage Retrieval with Re-ranking

Combine hybrid search with cross-encoder re-ranking for maximum quality.

```python
from sentence_transformers import CrossEncoder

# Stage 1: Hybrid retrieval (top 20)
initial_results = hybrid_search(query, top_k=20)

# Stage 2: Re-rank with cross-encoder (top 5)
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
pairs = [[query, result.text] for result in initial_results]
scores = reranker.predict(pairs)

# Sort by reranking scores
reranked = sorted(
    zip(initial_results, scores),
    key=lambda x: x[1],
    reverse=True
)[:5]
```

### Query Expansion

Expand queries before hybrid search to improve recall.

```python
from openai import OpenAI

client = OpenAI()

def expand_query(query: str) -> list[str]:
    """
    Generate query variations for improved recall.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Generate 3 alternative phrasings of the query that maintain the same intent."
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    variations = response.choices[0].message.content.split('\n')
    return [query] + variations

# Search with multiple query variations
def multi_query_hybrid_search(query: str):
    queries = expand_query(query)
    all_results = []

    for q in queries:
        results = hybrid_search(q, top_k=10)
        all_results.extend(results)

    # Deduplicate and merge scores
    merged = {}
    for result in all_results:
        if result.id not in merged:
            merged[result.id] = result
        else:
            merged[result.id].score += result.score

    return sorted(merged.values(), key=lambda x: x.score, reverse=True)[:5]
```

### Metadata-Filtered Hybrid Search

Apply metadata filters before hybrid search to constrain the search space.

```python
# Qdrant example
from qdrant_client.models import Filter, FieldCondition, MatchValue

results = client.query_points(
    collection_name="documents",
    prefetch=[
        Prefetch(
            query=query_vector,
            limit=20,
            filter=Filter(
                must=[
                    FieldCondition(
                        key="product_version",
                        match=MatchValue(value="v2.0")
                    ),
                    FieldCondition(
                        key="content_type",
                        match=MatchValue(value="documentation")
                    )
                ]
            )
        ),
        Prefetch(
            query=QueryEnum(text=query_text),
            using="text-index",
            limit=20,
            filter=Filter(
                must=[
                    FieldCondition(
                        key="product_version",
                        match=MatchValue(value="v2.0")
                    )
                ]
            )
        )
    ],
    query=FusionQuery(fusion="rrf"),
    limit=5
)
```

## Performance Optimization

### Prefetch Strategies

**Optimal prefetch limits:**
- Vector search: 20-50 results
- Keyword search: 20-50 results
- Final fusion: 5-10 results

**Rationale:**
- Larger prefetch improves fusion quality
- Diminishing returns beyond 50 results
- Balance quality vs. latency

### Index Optimization

**Vector indexes:**
- Use HNSW for <10M vectors
- Use IVF for >10M vectors
- Tune `ef_construct` and `m` parameters

**Text indexes:**
- Use inverted indexes (GIN in PostgreSQL)
- Configure stopwords appropriately
- Consider language-specific tokenizers

### Caching

Implement semantic caching for repeated queries:

```python
from functools import lru_cache
import hashlib

def query_hash(query: str) -> str:
    """
    Create hash of query for caching.
    """
    return hashlib.md5(query.encode()).hexdigest()

@lru_cache(maxsize=1000)
def cached_hybrid_search(query_hash: str, query: str, alpha: float):
    """
    Cache hybrid search results.
    """
    return hybrid_search(query, alpha=alpha)

# Usage
qhash = query_hash(user_query)
results = cached_hybrid_search(qhash, user_query, alpha=0.5)
```

### Batch Processing

Process multiple queries in parallel:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def batch_hybrid_search(queries: list[str], alpha: float = 0.5):
    """
    Execute multiple hybrid searches concurrently.
    """
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=10) as executor:
        tasks = [
            loop.run_in_executor(executor, hybrid_search, q, alpha)
            for q in queries
        ]
        results = await asyncio.gather(*tasks)

    return results
```

## Evaluation

### Metrics

**Retrieval Quality:**
- **Precision@k:** Proportion of relevant results in top k
- **Recall@k:** Proportion of all relevant results found in top k
- **MRR (Mean Reciprocal Rank):** Average inverse rank of first relevant result
- **NDCG (Normalized Discounted Cumulative Gain):** Ranking quality metric

**Production Targets:**
- Precision@5: >0.80
- Recall@10: >0.70
- MRR: >0.75

### A/B Testing Framework

```python
from dataclasses import dataclass
from typing import List

@dataclass
class SearchVariant:
    name: str
    alpha: float
    fusion_type: str  # "rrf" or "weighted"
    k_param: int = 60

def evaluate_variants(
    queries: List[str],
    ground_truth: dict,
    variants: List[SearchVariant]
):
    """
    Compare different hybrid search configurations.
    """
    results = {}

    for variant in variants:
        precision_scores = []
        recall_scores = []

        for query in queries:
            if variant.fusion_type == "rrf":
                search_results = hybrid_search_rrf(
                    query,
                    k=variant.k_param
                )
            else:
                search_results = hybrid_search_weighted(
                    query,
                    alpha=variant.alpha
                )

            # Calculate metrics
            relevant = ground_truth[query]
            retrieved = [r.id for r in search_results]

            precision = len(set(retrieved) & set(relevant)) / len(retrieved)
            recall = len(set(retrieved) & set(relevant)) / len(relevant)

            precision_scores.append(precision)
            recall_scores.append(recall)

        results[variant.name] = {
            "precision": sum(precision_scores) / len(precision_scores),
            "recall": sum(recall_scores) / len(recall_scores)
        }

    return results

# Example usage
variants = [
    SearchVariant("vector_heavy", alpha=0.7, fusion_type="weighted"),
    SearchVariant("balanced", alpha=0.5, fusion_type="weighted"),
    SearchVariant("keyword_heavy", alpha=0.3, fusion_type="weighted"),
    SearchVariant("rrf_default", alpha=0.5, fusion_type="rrf", k_param=60),
    SearchVariant("rrf_aggressive", alpha=0.5, fusion_type="rrf", k_param=20)
]

results = evaluate_variants(test_queries, ground_truth_data, variants)
```

### RAGAS Integration

```python
from ragas import evaluate
from ragas.metrics import context_precision, context_recall

def evaluate_hybrid_rag(
    questions: list[str],
    ground_truth: list[str],
    alpha: float = 0.5
):
    """
    Evaluate RAG system with hybrid search using RAGAS.
    """
    contexts = []

    for question in questions:
        results = hybrid_search(question, alpha=alpha)
        contexts.append([r.text for r in results])

    dataset = {
        "question": questions,
        "ground_truth": ground_truth,
        "contexts": contexts
    }

    scores = evaluate(
        dataset,
        metrics=[context_precision, context_recall]
    )

    return scores

# Compare different alpha values
for alpha in [0.3, 0.5, 0.7]:
    scores = evaluate_hybrid_rag(test_questions, test_answers, alpha=alpha)
    print(f"Alpha {alpha}: Precision={scores['context_precision']:.3f}, "
          f"Recall={scores['context_recall']:.3f}")
```

### Performance Comparison

**Benchmark (MTEB retrieval tasks):**

| Method | Recall@5 | Recall@10 | Latency |
|--------|----------|-----------|---------|
| Vector only | 0.72 | 0.81 | 10ms |
| BM25 only | 0.65 | 0.75 | 5ms |
| **Hybrid (RRF)** | **0.84** | **0.91** | 15ms |

**Conclusion:** Hybrid provides 12-point recall improvement at minimal latency cost.

---

## Summary

Hybrid search combines the semantic understanding of vector search with the precision of keyword matching, providing 15-30% improvement in retrieval quality for RAG applications.

**Key takeaways:**
- Use RRF for simplicity and robustness across platforms
- Use weighted scoring when fine-tuning search behavior
- Start with alpha=0.5 (balanced), adjust based on query characteristics
- Implement two-stage retrieval (hybrid + re-ranking) for maximum quality
- Evaluate with real queries and ground truth data

**Platform recommendations:**
- Qdrant: Built-in RRF, best metadata filtering
- Pinecone: Sparse-dense vectors, fully managed
- Weaviate: Native hybrid with multiple fusion types
- pgvector: Manual implementation, full SQL control
