---
sidebar_position: 3
title: Vector Databases
description: Vector database implementation for AI/ML applications, semantic search, and RAG systems
tags: [backend, database, vector, ai, rag, embeddings]
---

# Vector Databases for AI Applications

Vector database selection and implementation for AI/ML applications, semantic search, recommendation systems, and RAG (Retrieval-Augmented Generation) systems.

## When to Use

Use when implementing:
- **RAG (Retrieval-Augmented Generation)** systems for AI chatbots
- **Semantic search** capabilities (meaning-based, not just keyword)
- **Recommendation systems** based on similarity
- **Multi-modal AI** (unified search across text, images, audio)
- **Document similarity** and deduplication
- **Question answering** over private knowledge bases

## Multi-Language Support

This skill provides patterns for:
- **Python**: Qdrant client, LangChain, LlamaIndex (primary)
- **Rust**: Qdrant client (1,549 code snippets), high-performance systems
- **TypeScript**: @qdrant/js-client-rest, LangChain.js, Next.js integration
- **Go**: qdrant-go for high-performance microservices

## Quick Decision Framework

### 1. Vector Database Selection

```
EXISTING INFRASTRUCTURE?
├─ Using PostgreSQL already?
│  └─ pgvector (&lt;10M vectors, tight budget)
│
└─ No existing vector database?
   │
   ├─ OPERATIONAL PREFERENCE?
   │  │
   │  ├─ Zero-ops managed only
   │  │  └─ Pinecone (fully managed, excellent DX)
   │  │
   │  └─ Flexible (self-hosted or managed)
   │     │
   │     ├─ SCALE: &lt;100M vectors + complex filtering ⭐
   │     │  └─ Qdrant (RECOMMENDED)
   │     │      • Best metadata filtering
   │     │      • Built-in hybrid search (BM25 + Vector)
   │     │      • Self-host: Docker/K8s
   │     │      • Managed: Qdrant Cloud
   │     │
   │     ├─ SCALE: >100M vectors + GPU acceleration
   │     │  └─ Milvus / Zilliz Cloud
   │     │
   │     └─ Local prototyping
   │        └─ Chroma (simple API, in-memory)
```

### 2. Embedding Model Selection

```
REQUIREMENTS?

├─ Best quality (cost no object)
│  └─ Voyage AI voyage-3 (1024d)
│      • 9.74% better than OpenAI on MTEB
│      • ~$0.12/1M tokens
│
├─ Enterprise reliability
│  └─ OpenAI text-embedding-3-large (3072d)
│      • Industry standard
│      • ~$0.13/1M tokens
│      • Maturity shortening: reduce to 256/512/1024d
│
├─ Cost-optimized
│  └─ OpenAI text-embedding-3-small (1536d)
│      • ~$0.02/1M tokens (6x cheaper)
│      • 90-95% of large model performance
│
└─ Self-hosted / Privacy-critical
   ├─ English: nomic-embed-text-v1.5 (768d, Apache 2.0)
   ├─ Multilingual: BAAI/bge-m3 (1024d, MIT)
   └─ Long docs: jina-embeddings-v2 (768d, 8K context)
```

## Quick Start: Python + Qdrant

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# 1. Initialize client
client = QdrantClient("localhost", port=6333)

# 2. Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
)

# 3. Insert documents with embeddings
points = [
    PointStruct(
        id=idx,
        vector=embedding,  # From OpenAI/Voyage/etc
        payload={
            "text": chunk_text,
            "source": "docs/api.md",
            "section": "Authentication"
        }
    )
    for idx, (embedding, chunk_text) in enumerate(chunks)
]
client.upsert(collection_name="documents", points=points)

# 4. Search with metadata filtering
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    limit=5,
    query_filter={
        "must": [
            {"key": "section", "match": {"value": "Authentication"}}
        ]
    }
)
```

## Key Features

- **Qdrant** (recommended): Best metadata filtering, built-in hybrid search
- **Chunking strategies**: 512 tokens default, 50-100 token overlap
- **Hybrid search**: Vector similarity + BM25 keyword matching
- **Essential metadata**: source tracking, hierarchical context, content classification
- **RAGAS evaluation**: Faithfulness, relevancy, precision, recall metrics
- **Integration with ai-chat skill**: RAG pipeline for chatbots

## Document Chunking Strategy

**Recommended defaults for most RAG systems:**
- **Chunk size:** 512 tokens (not characters)
- **Overlap:** 50 tokens (10% overlap)

**Why these numbers?**
- 512 tokens balances context vs. precision
- Too small (128-256): Fragments concepts, loses context
- Too large (1024-2048): Dilutes relevance, wastes LLM tokens
- 50 token overlap ensures sentences aren't split mid-context

## Hybrid Search Pattern

```
User Query: "OAuth refresh token implementation"
           │
    ┌──────┴──────┐
    │             │
Vector Search   Keyword Search
(Semantic)      (BM25)
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

## Essential Metadata for Production RAG

```python
metadata = {
    # SOURCE TRACKING
    "source": "docs/api-reference.md",
    "source_type": "documentation",
    "last_updated": "2025-12-01T12:00:00Z",

    # HIERARCHICAL CONTEXT
    "section": "Authentication",
    "subsection": "OAuth 2.1",
    "heading_hierarchy": ["API Reference", "Authentication", "OAuth 2.1"],

    # CONTENT CLASSIFICATION
    "content_type": "code_example",
    "programming_language": "python",

    # FILTERING DIMENSIONS
    "product_version": "v2.0",
    "audience": "enterprise",
}
```

## RAG Pipeline Architecture

```
1. INGESTION
   ├─ Document Loading (PDF, web, code, Office)
   ├─ Text Extraction & Cleaning
   ├─ Chunking (semantic, recursive, code-aware)
   └─ Embedding Generation (batch, rate-limited)

2. INDEXING
   ├─ Vector Store Insertion (batch upsert)
   ├─ Index Configuration (HNSW, distance metric)
   └─ Keyword Index (BM25 for hybrid search)

3. RETRIEVAL (Query Time)
   ├─ Query Processing (expansion, embedding)
   ├─ Hybrid Search (vector + keyword)
   ├─ Filtering & Post-Processing (metadata, MMR)
   └─ Re-Ranking (cross-encoder, LLM-based)

4. GENERATION
   ├─ Context Construction (format chunks, citations)
   ├─ Prompt Engineering (system + context + query)
   ├─ LLM Inference (streaming, temperature tuning)
   └─ Response Post-Processing (citations, validation)

5. EVALUATION (Production Critical)
   ├─ Retrieval Metrics (precision, recall, relevancy)
   ├─ Generation Metrics (faithfulness, correctness)
   └─ System Metrics (latency, cost, satisfaction)
```

## Evaluation with RAGAS

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,       # Answer grounded in context
    answer_relevancy,   # Answer addresses query
    context_recall,     # Retrieved docs cover ground truth
    context_precision   # Retrieved docs are relevant
)

# Production targets:
# faithfulness: >0.90 (minimal hallucination)
# answer_relevancy: >0.85 (addresses user query)
# context_recall: >0.80 (sufficient context retrieved)
# context_precision: >0.75 (minimal noise)
```

## Related Skills

- [AI Chat](../frontend/building-ai-chat) - Frontend chat interface powered by vector DB RAG
- [AI Data Engineering](./ai-data-engineering) - RAG pipeline orchestration
- [Model Serving](./model-serving) - LLM serving for RAG generation
- [Relational Databases](./using-relational-databases) - Hybrid approach using pgvector

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/using-vector-databases)
- Qdrant: https://qdrant.tech/
- pgvector: https://github.com/pgvector/pgvector
- RAGAS: https://docs.ragas.io/
