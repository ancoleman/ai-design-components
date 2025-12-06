# Pinecone Vector Database Reference

Comprehensive guide to Pinecone, a fully-managed vector database designed for production AI applications. Use Pinecone for zero-ops deployment, excellent developer experience, and enterprise-grade reliability.

## Table of Contents

1. [When to Use Pinecone](#when-to-use-pinecone)
2. [Core Concepts](#core-concepts)
3. [Getting Started](#getting-started)
4. [Index Configuration](#index-configuration)
5. [Indexing Strategies](#indexing-strategies)
6. [Metadata Filtering](#metadata-filtering)
7. [Sparse-Dense Vectors (Hybrid Search)](#sparse-dense-vectors-hybrid-search)
8. [Namespaces and Multi-Tenancy](#namespaces-and-multi-tenancy)
9. [Python Code Examples](#python-code-examples)
10. [TypeScript Code Examples](#typescript-code-examples)
11. [Best Practices](#best-practices)
12. [Performance Optimization](#performance-optimization)
13. [Cost Optimization](#cost-optimization)
14. [Troubleshooting](#troubleshooting)

---

## When to Use Pinecone

**Choose Pinecone when:**
- **Zero-ops requirement:** No infrastructure management desired
- **Enterprise reliability:** Need 99.9% SLA guarantees
- **Rapid development:** Excellent SDKs and documentation
- **Hybrid search:** Built-in sparse-dense vector support
- **Global distribution:** Need low-latency worldwide access

**Consider alternatives when:**
- **Cost-sensitive:** Pinecone pricing higher than self-hosted (use Qdrant)
- **On-premises required:** Pinecone is cloud-only (use Qdrant/Milvus)
- **Small scale:** <10M vectors on existing PostgreSQL (use pgvector)
- **Complex filtering:** Qdrant has more advanced metadata filtering

**Scale characteristics:**
- Efficient for 1M to 100M+ vectors
- Serverless tier: Auto-scaling, pay-per-use
- Pod-based tier: Reserved capacity, predictable costs

---

## Core Concepts

### Index
Highest-level organizational unit in Pinecone. Each index:
- Contains vectors of identical dimensions
- Uses single distance metric (cosine, euclidean, dotproduct)
- Deployed in specific cloud region (AWS us-east-1, GCP us-central1, etc.)
- Configured with pod type (serverless vs. pod-based)

### Namespace
Logical partition within an index for data isolation:
- Share same index configuration (dimensions, metric)
- Enable multi-tenancy (isolate user/org data)
- Support efficient bulk operations (delete namespace)
- No cross-namespace querying (filter by namespace)

### Metadata
JSON-compatible key-value pairs attached to vectors:
- Support filtering during queries
- Maximum 40KB per vector
- Indexed types: string, number, boolean, array
- Enable pre-filtering before vector search

### Sparse-Dense Vectors
Hybrid representation combining semantic and keyword signals:
- **Dense vectors:** Semantic embeddings (1024-3072 dimensions)
- **Sparse vectors:** Keyword weights (BM25, SPLADE)
- Combined via weighted scoring (alpha parameter)
- Improves retrieval quality for exact term matching

---

## Getting Started

### Installation

**Python:**
```bash
pip install pinecone-client
```

**TypeScript:**
```bash
npm install @pinecone-database/pinecone
```

### Create API Key

1. Sign up at https://app.pinecone.io
2. Navigate to API Keys section
3. Create new API key (save securely)
4. Note the environment (e.g., `us-east-1-aws`)

### Initialize Client

**Python:**
```python
from pinecone import Pinecone

pc = Pinecone(api_key="YOUR_API_KEY")
```

**TypeScript:**
```typescript
import { Pinecone } from '@pinecone-database/pinecone';

const pc = new Pinecone({ apiKey: 'YOUR_API_KEY' });
```

### Create First Index

**Python:**
```python
from pinecone import ServerlessSpec

# Create serverless index
pc.create_index(
    name="my-index",
    dimension=1024,  # Match embedding model
    metric="cosine",  # cosine, euclidean, dotproduct
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)
```

**TypeScript:**
```typescript
await pc.createIndex({
  name: 'my-index',
  dimension: 1024,
  metric: 'cosine',
  spec: {
    serverless: {
      cloud: 'aws',
      region: 'us-east-1'
    }
  }
});
```

### Connect to Index

**Python:**
```python
index = pc.Index("my-index")
```

**TypeScript:**
```typescript
const index = pc.index('my-index');
```

---

## Index Configuration

### Serverless vs. Pod-Based

**Serverless (Recommended for most use cases):**
```python
from pinecone import ServerlessSpec

pc.create_index(
    name="serverless-index",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)
```

**Benefits:**
- Auto-scaling (no capacity planning)
- Pay only for storage and operations
- No idle costs
- Instant deployment

**Use when:** Variable workload, development, cost-conscious

**Pod-Based (Reserved capacity):**
```python
from pinecone import PodSpec

pc.create_index(
    name="pod-index",
    dimension=1536,
    metric="cosine",
    spec=PodSpec(
        environment="us-east-1-aws",
        pod_type="p1.x1",  # Performance tier
        pods=2,  # Number of replicas
        replicas=2,  # Redundancy
        shards=1  # Horizontal partitioning
    )
)
```

**Benefits:**
- Predictable performance
- Dedicated resources
- Lower per-operation cost at scale
- Advanced tuning options

**Use when:** High-throughput production, consistent load, >10M requests/month

### Distance Metrics

**Cosine similarity (most common):**
```python
metric="cosine"  # Range: -1 to 1 (1 = identical)
```
- Use with normalized embeddings (OpenAI, Voyage, Cohere)
- Measures angle between vectors
- Invariant to magnitude

**Euclidean distance:**
```python
metric="euclidean"  # Range: 0 to infinity (0 = identical)
```
- Use with unnormalized embeddings
- Measures straight-line distance
- Sensitive to magnitude

**Dot product:**
```python
metric="dotproduct"  # Range: -infinity to infinity
```
- Use with pre-normalized embeddings
- Fastest computation
- Equivalent to cosine for unit vectors

**Choosing metric:**
- **OpenAI/Cohere/Voyage:** Use `cosine` (embeddings are normalized)
- **Custom embeddings:** Use `euclidean` unless normalized
- **Performance-critical:** Use `dotproduct` with normalized vectors

---

## Indexing Strategies

### Single Vector Insertion

**Python:**
```python
index.upsert(
    vectors=[
        {
            "id": "doc1",
            "values": embedding_vector,  # List[float]
            "metadata": {
                "text": "Full document text",
                "source": "docs/api.md",
                "section": "Authentication"
            }
        }
    ]
)
```

**TypeScript:**
```typescript
await index.upsert([
  {
    id: 'doc1',
    values: embeddingVector,
    metadata: {
      text: 'Full document text',
      source: 'docs/api.md',
      section: 'Authentication'
    }
  }
]);
```

### Batch Insertion (Recommended)

**Python:**
```python
batch_size = 100  # Optimal: 100-200 vectors per batch

vectors = [
    {
        "id": f"doc{i}",
        "values": embeddings[i],
        "metadata": {
            "text": chunks[i],
            "chunk_index": i
        }
    }
    for i in range(len(embeddings))
]

# Upsert in batches
for i in range(0, len(vectors), batch_size):
    batch = vectors[i:i + batch_size]
    index.upsert(vectors=batch)
```

**TypeScript:**
```typescript
const batchSize = 100;

for (let i = 0; i < vectors.length; i += batchSize) {
  const batch = vectors.slice(i, i + batchSize);
  await index.upsert(batch);
}
```

### Async/Parallel Insertion

**Python (with asyncio):**
```python
import asyncio
from pinecone import Pinecone

async def upsert_batch(index, batch):
    # Pinecone client is sync, use thread executor
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, index.upsert, batch)

async def upsert_all(index, vectors, batch_size=100):
    batches = [
        vectors[i:i + batch_size]
        for i in range(0, len(vectors), batch_size)
    ]

    await asyncio.gather(*[
        upsert_batch(index, batch) for batch in batches
    ])

# Usage
asyncio.run(upsert_all(index, vectors))
```

**TypeScript (parallel promises):**
```typescript
const batchSize = 100;
const batches = [];

for (let i = 0; i < vectors.length; i += batchSize) {
  batches.push(vectors.slice(i, i + batchSize));
}

await Promise.all(
  batches.map(batch => index.upsert(batch))
);
```

### Update Metadata Only

**Python:**
```python
index.update(
    id="doc1",
    set_metadata={
        "updated_at": "2025-12-05",
        "status": "reviewed"
    }
)
```

**TypeScript:**
```typescript
await index.update({
  id: 'doc1',
  setMetadata: {
    updated_at: '2025-12-05',
    status: 'reviewed'
  }
});
```

---

## Metadata Filtering

### Filter Syntax

Pinecone supports filtering during queries to reduce search space before vector comparison.

**Supported operators:**
- `$eq`: Equal to
- `$ne`: Not equal to
- `$gt`, `$gte`: Greater than (or equal)
- `$lt`, `$lte`: Less than (or equal)
- `$in`: Value in array
- `$nin`: Value not in array
- `$exists`: Field exists/doesn't exist

**Logical operators:**
- `$and`: All conditions must match
- `$or`: Any condition must match

### Basic Filtering

**Python:**
```python
# Exact match
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={
        "source": {"$eq": "docs/api.md"}
    }
)

# Numeric range
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={
        "timestamp": {"$gte": 1701388800}
    }
)

# Array membership
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={
        "category": {"$in": ["tutorial", "guide"]}
    }
)
```

**TypeScript:**
```typescript
// Exact match
const results = await index.query({
  vector: queryEmbedding,
  topK: 10,
  filter: {
    source: { $eq: 'docs/api.md' }
  }
});

// Numeric range
const results = await index.query({
  vector: queryEmbedding,
  topK: 10,
  filter: {
    timestamp: { $gte: 1701388800 }
  }
});
```

### Complex Filtering

**Python:**
```python
# AND condition
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={
        "$and": [
            {"source_type": {"$eq": "documentation"}},
            {"version": {"$gte": "2.0"}},
            {"language": {"$in": ["python", "typescript"]}}
        ]
    }
)

# OR condition
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={
        "$or": [
            {"priority": {"$eq": "high"}},
            {"updated_at": {"$gte": "2025-12-01"}}
        ]
    }
)

# Nested conditions
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={
        "$and": [
            {"product": {"$eq": "api"}},
            {
                "$or": [
                    {"section": {"$eq": "authentication"}},
                    {"section": {"$eq": "authorization"}}
                ]
            }
        ]
    }
)
```

### Metadata Best Practices

**Index frequently-filtered fields:**
```python
metadata = {
    # High-cardinality (many unique values)
    "doc_id": "uuid-string",  # Unique identifier

    # Low-cardinality (few unique values) - BEST FOR FILTERING
    "source_type": "documentation",  # 5-10 categories
    "language": "python",  # Limited options
    "version": "v2",  # Version tags

    # Numeric ranges
    "timestamp": 1701388800,
    "word_count": 512,

    # Text content (for inclusion in results)
    "text": "Full chunk text...",
    "title": "Document title"
}
```

**Avoid over-indexing:**
- Limit to 10-15 metadata fields per vector
- Store large text in `text` field (not filtered, only returned)
- Use consistent data types (don't mix strings/numbers)

---

## Sparse-Dense Vectors (Hybrid Search)

Hybrid search combines dense semantic vectors with sparse keyword vectors for improved retrieval quality.

### Dense Vectors (Semantic)
Standard embeddings from models like OpenAI, Voyage, Cohere.

### Sparse Vectors (Keyword)
Token-based representations (BM25, SPLADE) encoding exact term importance.

**Format:**
```python
sparse_vector = {
    "indices": [100, 542, 1023],  # Token IDs
    "values": [0.8, 0.5, 0.3]     # Weights (TF-IDF, BM25)
}
```

### Python Hybrid Search Example

**Using BM25 for sparse vectors:**
```python
from rank_bm25 import BM25Okapi
import numpy as np

# 1. Create BM25 index from corpus
corpus = ["document one text", "document two text", ...]
tokenized_corpus = [doc.split() for doc in corpus]
bm25 = BM25Okapi(tokenized_corpus)

# 2. Generate sparse vector for query
query = "example search query"
tokenized_query = query.split()
bm25_scores = bm25.get_scores(tokenized_query)

# Convert to sparse format (top-k terms only)
top_k = 50  # Keep top 50 terms
top_indices = np.argsort(bm25_scores)[-top_k:]
sparse_vector = {
    "indices": top_indices.tolist(),
    "values": bm25_scores[top_indices].tolist()
}

# 3. Query with both dense and sparse
results = index.query(
    vector=dense_embedding,  # From OpenAI/Voyage
    sparse_vector=sparse_vector,  # From BM25
    top_k=10,
    include_metadata=True
)
```

### TypeScript Hybrid Search Example

```typescript
import { BM25 } from 'natural';

// 1. Create BM25 index
const bm25 = new BM25();
corpus.forEach(doc => bm25.addDocument(doc.split(' ')));

// 2. Generate sparse vector
const query = 'example search query';
const scores = bm25.search(query.split(' '));

// Keep top 50 terms
const topK = 50;
const sortedIndices = scores
  .map((score, idx) => ({ score, idx }))
  .sort((a, b) => b.score - a.score)
  .slice(0, topK);

const sparseVector = {
  indices: sortedIndices.map(x => x.idx),
  values: sortedIndices.map(x => x.score)
};

// 3. Hybrid query
const results = await index.query({
  vector: denseEmbedding,
  sparseVector: sparseVector,
  topK: 10,
  includeMetadata: true
});
```

### Hybrid Search Configuration

**Control dense vs. sparse weighting:**
```python
# Alpha parameter (0.0 to 1.0)
results = index.query(
    vector=dense_embedding,
    sparse_vector=sparse_vector,
    top_k=10,
    alpha=0.5  # 0.5 = equal weight to dense and sparse
    # 0.0 = sparse only
    # 1.0 = dense only
)
```

**Recommended alpha values:**
- **0.7-0.8:** General RAG (favor semantic understanding)
- **0.5:** Balanced (code search, mixed queries)
- **0.3-0.4:** Keyword-heavy (legal, compliance, exact terms)

### Upsert Sparse-Dense Vectors

**Python:**
```python
index.upsert(
    vectors=[
        {
            "id": "doc1",
            "values": dense_embedding,  # [0.1, 0.5, ..., 0.3]
            "sparse_values": {
                "indices": [100, 542, 1023],
                "values": [0.8, 0.5, 0.3]
            },
            "metadata": {"text": "Document content"}
        }
    ]
)
```

**TypeScript:**
```typescript
await index.upsert([
  {
    id: 'doc1',
    values: denseEmbedding,
    sparseValues: {
      indices: [100, 542, 1023],
      values: [0.8, 0.5, 0.3]
    },
    metadata: { text: 'Document content' }
  }
]);
```

---

## Namespaces and Multi-Tenancy

### What are Namespaces?

Namespaces partition vectors within an index for logical isolation while sharing infrastructure.

**Use cases:**
- **Multi-tenant systems:** Isolate customer data
- **Environment separation:** dev, staging, production
- **Content versioning:** v1, v2, v3 documentation
- **A/B testing:** Separate experimental embeddings

### Create and Use Namespaces

**Python:**
```python
# Upsert to specific namespace
index.upsert(
    vectors=[
        {
            "id": "doc1",
            "values": embedding,
            "metadata": {"text": "Content"}
        }
    ],
    namespace="customer-123"  # Tenant identifier
)

# Query specific namespace
results = index.query(
    vector=query_embedding,
    top_k=10,
    namespace="customer-123",
    include_metadata=True
)
```

**TypeScript:**
```typescript
// Upsert to namespace
await index.namespace('customer-123').upsert([
  {
    id: 'doc1',
    values: embedding,
    metadata: { text: 'Content' }
  }
]);

// Query namespace
const results = await index.namespace('customer-123').query({
  vector: queryEmbedding,
  topK: 10,
  includeMetadata: true
});
```

### Multi-Tenant Architecture

**Namespace-per-tenant (recommended):**
```python
def upsert_tenant_docs(tenant_id: str, documents: list):
    namespace = f"tenant-{tenant_id}"

    vectors = [
        {
            "id": f"{tenant_id}-{doc['id']}",
            "values": doc['embedding'],
            "metadata": {
                "text": doc['text'],
                "tenant_id": tenant_id  # Redundant but useful
            }
        }
        for doc in documents
    ]

    index.upsert(vectors=vectors, namespace=namespace)

def query_tenant_docs(tenant_id: str, query_embedding: list):
    namespace = f"tenant-{tenant_id}"

    results = index.query(
        vector=query_embedding,
        top_k=10,
        namespace=namespace,
        include_metadata=True
    )

    return results
```

**Benefits:**
- Complete data isolation (no cross-tenant leakage)
- Efficient bulk operations (delete entire namespace)
- Simplified access control
- Independent scaling per tenant

### Namespace Operations

**List namespaces:**
```python
stats = index.describe_index_stats()
namespaces = stats['namespaces'].keys()
print(f"Namespaces: {list(namespaces)}")
```

**Delete namespace:**
```python
# Delete all vectors in namespace
index.delete(delete_all=True, namespace="customer-123")
```

**Get namespace statistics:**
```python
stats = index.describe_index_stats()
namespace_stats = stats['namespaces'].get('customer-123', {})
vector_count = namespace_stats.get('vector_count', 0)
print(f"Vectors in namespace: {vector_count}")
```

---

## Python Code Examples

### Complete RAG Pipeline

```python
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
import os

# Initialize clients
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Create index
index_name = "rag-pipeline"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # text-embedding-3-small
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

# 1. INGESTION: Load and chunk documents
documents = [
    "OAuth 2.1 is the latest authorization framework...",
    "Refresh tokens allow long-lived access...",
    "API keys should be rotated every 90 days..."
]

# 2. EMBEDDING: Generate embeddings
def get_embedding(text: str) -> list[float]:
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

embeddings = [get_embedding(doc) for doc in documents]

# 3. INDEXING: Upsert to Pinecone
vectors = [
    {
        "id": f"doc{i}",
        "values": embeddings[i],
        "metadata": {
            "text": documents[i],
            "source": "api-docs",
            "section": "authentication"
        }
    }
    for i in range(len(documents))
]

index.upsert(vectors=vectors)

# 4. RETRIEVAL: Query with context
query = "How do refresh tokens work?"
query_embedding = get_embedding(query)

results = index.query(
    vector=query_embedding,
    top_k=3,
    include_metadata=True
)

# 5. GENERATION: Build context and generate answer
context = "\n\n".join([
    match['metadata']['text']
    for match in results['matches']
])

response = openai_client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "Answer using only the provided context."
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {query}"
        }
    ]
)

answer = response.choices[0].message.content
print(f"Answer: {answer}")
```

### Batch Processing with Error Handling

```python
import time
from typing import List, Dict

def batch_upsert_with_retry(
    index,
    vectors: List[Dict],
    batch_size: int = 100,
    max_retries: int = 3
):
    """Upsert vectors in batches with exponential backoff."""

    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]

        for attempt in range(max_retries):
            try:
                index.upsert(vectors=batch)
                print(f"Upserted batch {i//batch_size + 1}")
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Failed after {max_retries} attempts: {e}")

                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retry {attempt + 1} after {wait_time}s")
                time.sleep(wait_time)

# Usage
batch_upsert_with_retry(index, vectors, batch_size=100)
```

### Multi-Namespace Query

```python
def query_all_namespaces(
    index,
    query_embedding: list[float],
    namespaces: list[str],
    top_k: int = 5
):
    """Query multiple namespaces and aggregate results."""

    all_results = []

    for namespace in namespaces:
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            namespace=namespace,
            include_metadata=True
        )

        # Tag results with namespace
        for match in results['matches']:
            match['namespace'] = namespace
            all_results.append(match)

    # Sort by score across all namespaces
    all_results.sort(key=lambda x: x['score'], reverse=True)

    return all_results[:top_k]

# Usage
namespaces = ["docs-v1", "docs-v2", "docs-v3"]
results = query_all_namespaces(index, query_embedding, namespaces)
```

---

## TypeScript Code Examples

### Complete RAG Pipeline

```typescript
import { Pinecone } from '@pinecone-database/pinecone';
import OpenAI from 'openai';

const pc = new Pinecone({ apiKey: process.env.PINECONE_API_KEY! });
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY! });

// Create index
const indexName = 'rag-pipeline';
const indexList = await pc.listIndexes();

if (!indexList.indexes?.find(idx => idx.name === indexName)) {
  await pc.createIndex({
    name: indexName,
    dimension: 1536,
    metric: 'cosine',
    spec: {
      serverless: {
        cloud: 'aws',
        region: 'us-east-1'
      }
    }
  });
}

const index = pc.index(indexName);

// 1. INGESTION
const documents = [
  'OAuth 2.1 is the latest authorization framework...',
  'Refresh tokens allow long-lived access...',
  'API keys should be rotated every 90 days...'
];

// 2. EMBEDDING
async function getEmbedding(text: string): Promise<number[]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: text
  });
  return response.data[0].embedding;
}

const embeddings = await Promise.all(
  documents.map(doc => getEmbedding(doc))
);

// 3. INDEXING
const vectors = documents.map((doc, i) => ({
  id: `doc${i}`,
  values: embeddings[i],
  metadata: {
    text: doc,
    source: 'api-docs',
    section: 'authentication'
  }
}));

await index.upsert(vectors);

// 4. RETRIEVAL
const query = 'How do refresh tokens work?';
const queryEmbedding = await getEmbedding(query);

const results = await index.query({
  vector: queryEmbedding,
  topK: 3,
  includeMetadata: true
});

// 5. GENERATION
const context = results.matches
  .map(match => match.metadata?.text)
  .join('\n\n');

const response = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [
    {
      role: 'system',
      content: 'Answer using only the provided context.'
    },
    {
      role: 'user',
      content: `Context:\n${context}\n\nQuestion: ${query}`
    }
  ]
});

const answer = response.choices[0].message.content;
console.log(`Answer: ${answer}`);
```

### Batch Processing with Error Handling

```typescript
interface Vector {
  id: string;
  values: number[];
  metadata?: Record<string, any>;
}

async function batchUpsertWithRetry(
  index: any,
  vectors: Vector[],
  batchSize = 100,
  maxRetries = 3
): Promise<void> {
  for (let i = 0; i < vectors.length; i += batchSize) {
    const batch = vectors.slice(i, i + batchSize);

    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        await index.upsert(batch);
        console.log(`Upserted batch ${Math.floor(i / batchSize) + 1}`);
        break;
      } catch (error) {
        if (attempt === maxRetries - 1) {
          throw new Error(`Failed after ${maxRetries} attempts: ${error}`);
        }

        const waitTime = Math.pow(2, attempt) * 1000;
        console.log(`Retry ${attempt + 1} after ${waitTime}ms`);
        await new Promise(resolve => setTimeout(resolve, waitTime));
      }
    }
  }
}

// Usage
await batchUpsertWithRetry(index, vectors, 100);
```

### Streaming Query Results

```typescript
async function* streamingQuery(
  index: any,
  queryEmbedding: number[],
  topK = 10,
  namespace?: string
) {
  const results = await index.query({
    vector: queryEmbedding,
    topK,
    namespace,
    includeMetadata: true
  });

  for (const match of results.matches) {
    yield {
      id: match.id,
      score: match.score,
      text: match.metadata?.text,
      metadata: match.metadata
    };
  }
}

// Usage with async iteration
for await (const result of streamingQuery(index, queryEmbedding, 5)) {
  console.log(`Score: ${result.score} - ${result.text}`);
}
```

---

## Best Practices

### Indexing Best Practices

**1. Batch operations for efficiency:**
```python
# ✅ Good: Batch upserts
index.upsert(vectors=batch_of_100)

# ❌ Bad: Individual upserts
for vector in vectors:
    index.upsert(vectors=[vector])
```

**2. Use consistent ID schemes:**
```python
# ✅ Good: Predictable, collision-resistant
id = f"{tenant_id}-{doc_id}-{chunk_index}"

# ❌ Bad: Random IDs (can't update)
id = str(uuid.uuid4())
```

**3. Store full text in metadata:**
```python
metadata = {
    "text": full_chunk_text,  # For retrieval/display
    "source": "docs/api.md",  # For filtering
    "chunk_index": 3  # For ordering
}
```

### Querying Best Practices

**1. Pre-filter before vector search:**
```python
# ✅ Good: Filter reduces search space
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={"source_type": {"$eq": "documentation"}}
)

# ❌ Bad: Post-filter wastes computation
results = index.query(vector=query_embedding, top_k=100)
filtered = [r for r in results if r['metadata']['source_type'] == 'documentation'][:10]
```

**2. Use appropriate top_k:**
```python
# ✅ Good: Retrieve enough for re-ranking
top_k = 20  # Re-rank to 5

# ❌ Bad: Too few (miss relevant docs)
top_k = 3
```

**3. Include metadata selectively:**
```python
# ✅ Good: Only when needed
results = index.query(
    vector=query_embedding,
    top_k=10,
    include_metadata=True  # Need text for generation
)

# ❌ Bad: Always including (wastes bandwidth)
include_metadata=True  # Even for similarity-only tasks
```

### Metadata Best Practices

**1. Optimize for filtering:**
```python
# ✅ Good: Low-cardinality categorical
metadata = {
    "category": "tutorial",  # 5-10 values
    "language": "python",  # Limited set
    "version": "v2"  # Few versions
}

# ❌ Bad: High-cardinality (inefficient)
metadata = {
    "unique_id": "uuid-12345",  # Unique per doc
    "timestamp_ms": 1701388812345  # Millions of values
}
```

**2. Consistent data types:**
```python
# ✅ Good: Consistent types
metadata = {"version": "2.0"}  # Always string

# ❌ Bad: Mixed types
metadata = {"version": 2.0}  # Sometimes number
metadata = {"version": "2.0"}  # Sometimes string
```

### Namespace Best Practices

**1. Namespace per tenant:**
```python
# ✅ Good: Complete isolation
namespace = f"tenant-{tenant_id}"

# ❌ Bad: Metadata filtering only (risk of leakage)
metadata = {"tenant_id": tenant_id}
```

**2. Namespace for environment separation:**
```python
# ✅ Good: Separate dev/staging/prod
namespaces = {
    "development": "dev",
    "staging": "staging",
    "production": "prod"
}
```

---

## Performance Optimization

### Query Performance

**1. Optimize vector dimensions:**
```python
# Use dimension reduction for faster queries
dimension = 1024  # vs. 3072 (3x faster)

# OpenAI supports maturity shortening
embedding = get_embedding(text)[:1024]  # Truncate to 1024d
```

**2. Reduce top_k when possible:**
```python
# Balance precision vs. speed
top_k = 10  # Fast, usually sufficient
# vs.
top_k = 100  # Slower, more comprehensive
```

**3. Use pod-based for high-throughput:**
```python
# Serverless: Variable performance
spec = ServerlessSpec(cloud="aws", region="us-east-1")

# Pod-based: Consistent, faster at scale
spec = PodSpec(
    environment="us-east-1-aws",
    pod_type="p1.x2",  # Higher tier
    pods=2
)
```

### Indexing Performance

**1. Batch upserts:**
```python
batch_size = 100  # Optimal range: 100-200
```

**2. Parallel batch processing:**
```python
import concurrent.futures

def upsert_batch(batch):
    index.upsert(vectors=batch)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(upsert_batch, batches)
```

**3. Async upserts (TypeScript):**
```typescript
const batches = [...]; // Array of batches
await Promise.all(batches.map(batch => index.upsert(batch)));
```

---

## Cost Optimization

### Serverless Pricing

**Pricing components:**
- **Storage:** $0.10 per GB-month
- **Reads:** $1.00 per 1M queries
- **Writes:** $2.00 per 1M upserts

**Optimization strategies:**

**1. Reduce vector dimensions:**
```python
# 3072d OpenAI embedding
storage_3072d = 3072 * 4 bytes = 12.3 KB per vector

# 1024d (maturity shortening)
storage_1024d = 1024 * 4 bytes = 4.1 KB per vector
# 3x storage savings
```

**2. Minimize metadata size:**
```python
# ✅ Good: Compact metadata
metadata = {
    "txt": chunk[:500],  # Truncate text
    "src": "api.md",
    "sec": "auth"
}

# ❌ Bad: Bloated metadata
metadata = {
    "full_document_text": entire_document,  # 10KB+
    "source_file_path": "/very/long/path/...",
    "section_hierarchy": ["Level1", "Level2", ...]
}
```

**3. Use namespaces for bulk deletion:**
```python
# ✅ Good: Delete entire namespace (fast, cheap)
index.delete(delete_all=True, namespace="temp-docs")

# ❌ Bad: Delete individual vectors (slow, expensive)
for id in doc_ids:
    index.delete(ids=[id])
```

**4. Cache embeddings:**
```python
import hashlib
import json

embedding_cache = {}

def get_cached_embedding(text: str):
    # Hash text for cache key
    cache_key = hashlib.md5(text.encode()).hexdigest()

    if cache_key in embedding_cache:
        return embedding_cache[cache_key]

    # Generate embedding
    embedding = get_embedding(text)
    embedding_cache[cache_key] = embedding

    return embedding
```

### Pod-Based Pricing

**Pricing:** Fixed monthly cost per pod ($70-$1000/month depending on tier)

**When pod-based is cheaper:**
- High query volume (>10M queries/month)
- Consistent workload (predictable traffic)
- Large-scale production (cost per operation lower)

---

## Troubleshooting

### Common Issues

**1. Dimension mismatch:**
```
Error: Vector dimension 1536 does not match index dimension 1024
```

**Solution:**
```python
# Verify embedding dimension matches index
embedding_dim = len(embedding)
index_dim = 1024  # From index creation

assert embedding_dim == index_dim, f"Mismatch: {embedding_dim} != {index_dim}"
```

**2. Empty query results:**
```python
results = index.query(vector=query_embedding, top_k=10)
# results['matches'] is empty
```

**Solutions:**
- Check if vectors were actually indexed (describe_index_stats)
- Verify namespace (querying wrong namespace)
- Check filter constraints (too restrictive)
- Verify embedding generation (not all zeros)

**3. Slow queries:**

**Diagnose:**
```python
import time

start = time.time()
results = index.query(vector=query_embedding, top_k=10)
elapsed = time.time() - start
print(f"Query took {elapsed:.2f}s")
```

**Solutions:**
- Reduce top_k
- Reduce vector dimensions
- Use pre-filtering (metadata filters)
- Consider pod-based for consistent performance

**4. Metadata filtering not working:**

**Common mistake:**
```python
# ❌ Wrong: Missing operator
filter = {"source": "docs/api.md"}

# ✅ Correct: Explicit operator
filter = {"source": {"$eq": "docs/api.md"}}
```

**5. Rate limiting:**
```
Error: Rate limit exceeded
```

**Solution:**
```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def upsert_with_retry(vectors):
    return index.upsert(vectors=vectors)
```

### Debugging Tips

**1. Check index statistics:**
```python
stats = index.describe_index_stats()
print(f"Total vectors: {stats['total_vector_count']}")
print(f"Namespaces: {list(stats['namespaces'].keys())}")
```

**2. Inspect query results:**
```python
results = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True,
    include_values=True  # Include vectors for debugging
)

for match in results['matches']:
    print(f"ID: {match['id']}")
    print(f"Score: {match['score']}")
    print(f"Metadata: {match['metadata']}")
    print(f"Vector (first 5): {match['values'][:5]}")
```

**3. Verify embeddings are non-zero:**
```python
import numpy as np

embedding = get_embedding(text)
magnitude = np.linalg.norm(embedding)

if magnitude < 0.01:
    print("Warning: Embedding is near-zero (check generation)")
```

---

## Additional Resources

**Official Documentation:**
- Pinecone Docs: https://docs.pinecone.io
- Python SDK: https://docs.pinecone.io/docs/python-client
- TypeScript SDK: https://docs.pinecone.io/docs/typescript-client

**Code Examples:**
- `examples/pinecone-python/` - Python RAG implementation
- `examples/typescript-rag/` - TypeScript RAG with Pinecone
