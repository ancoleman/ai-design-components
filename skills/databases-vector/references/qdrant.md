# Qdrant: Production-Ready Vector Database

## Overview

Qdrant is an open-source vector database optimized for complex metadata filtering and hybrid search. It is the **primary recommendation** for RAG systems requiring production-grade filtering.

**Context7 Documentation:** `/llmstxt/qdrant_tech_llms-full_txt` (10,154 snippets, 83.1 score)

## Why Qdrant?

### Strengths
- **Best-in-class metadata filtering** - Critical for RAG systems with complex requirements
- **Built-in hybrid search** - Combines vector similarity + BM25 keyword matching
- **Multi-language SDKs** - Official Python, Rust, Go, TypeScript, Java support
- **Flexible deployment** - Self-hosted (Docker, Kubernetes) or managed (Qdrant Cloud)
- **Production-proven** - Used by Anthropic, Hugging Face, and major AI companies
- **Excellent documentation** - Comprehensive guides and 10K+ code examples

### When to Choose Qdrant
- Complex metadata filtering requirements (multi-tenant, versioned docs, permissions)
- Need hybrid search (semantic + keyword) out of the box
- Want deployment flexibility (self-host or managed)
- Require <100M vectors with exceptional filtering performance
- Building production RAG systems

### When to Consider Alternatives
- **Pinecone:** Zero-ops managed-only requirement, no self-hosting needed
- **Milvus:** >100M vectors requiring GPU acceleration
- **pgvector:** Already using PostgreSQL, <10M vectors, tight budget

## Installation and Setup

### Docker (Development)

```bash
# Pull and run Qdrant
docker pull qdrant/qdrant
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

### Docker Compose (Recommended)

```yaml
# docker-compose.yml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"  # REST API
      - "6334:6334"  # gRPC API
    volumes:
      - ./qdrant_storage:/qdrant/storage:z
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334
    restart: unless-stopped
```

```bash
docker-compose up -d
```

### Kubernetes (Production)

```yaml
# qdrant-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: qdrant
spec:
  replicas: 3
  selector:
    matchLabels:
      app: qdrant
  template:
    metadata:
      labels:
        app: qdrant
    spec:
      containers:
      - name: qdrant
        image: qdrant/qdrant:latest
        ports:
        - containerPort: 6333
        - containerPort: 6334
        volumeMounts:
        - name: storage
          mountPath: /qdrant/storage
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
      volumes:
      - name: storage
        persistentVolumeClaim:
          claimName: qdrant-pvc
```

### Qdrant Cloud (Managed)

1. Visit https://cloud.qdrant.io
2. Create cluster (free tier available)
3. Copy cluster URL and API key
4. Connect with client:

```python
from qdrant_client import QdrantClient

client = QdrantClient(
    url="https://your-cluster.qdrant.io",
    api_key="your-api-key"
)
```

## Python Client Setup

### Installation

```bash
pip install qdrant-client
```

### Basic Usage

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Connect to Qdrant
client = QdrantClient("localhost", port=6333)

# Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=1024,  # Voyage AI default
        distance=Distance.COSINE
    )
)

# Insert vectors
points = [
    PointStruct(
        id=1,
        vector=[0.1] * 1024,
        payload={
            "text": "Document content here",
            "source": "docs/api.md",
            "section": "Authentication"
        }
    )
]
client.upsert(collection_name="documents", points=points)

# Search
results = client.search(
    collection_name="documents",
    query_vector=[0.1] * 1024,
    limit=5
)
```

## Collections and Indexing

### Creating Collections

```python
from qdrant_client.models import VectorParams, Distance

# Cosine distance (most common for embeddings)
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
)

# Dot product (for normalized vectors)
client.create_collection(
    collection_name="normalized_docs",
    vectors_config=VectorParams(size=1024, distance=Distance.DOT)
)

# Euclidean distance
client.create_collection(
    collection_name="euclidean_docs",
    vectors_config=VectorParams(size=1024, distance=Distance.EUCLID)
)
```

### Multiple Vector Types (Named Vectors)

```python
from qdrant_client.models import VectorParams, Distance

# Support both dense and sparse vectors
client.create_collection(
    collection_name="hybrid_docs",
    vectors_config={
        "dense": VectorParams(size=1024, distance=Distance.COSINE),
        "sparse": VectorParams(size=30000, distance=Distance.COSINE)  # BM25
    }
)
```

### Index Configuration (HNSW)

```python
from qdrant_client.models import VectorParams, Distance, HnswConfigDiff

client.create_collection(
    collection_name="optimized_docs",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
    hnsw_config=HnswConfigDiff(
        m=16,                    # Number of edges per node (16 is default)
        ef_construct=100,        # Search quality during indexing (100 default)
        full_scan_threshold=10000 # Switch to HNSW after this many vectors
    )
)
```

**HNSW Parameters:**
- **m:** Higher = better quality, more memory (default: 16, range: 4-64)
- **ef_construct:** Higher = better index quality, slower indexing (default: 100)
- **full_scan_threshold:** Flat search below this threshold (default: 10000)

## Metadata Filtering

### Filter Syntax

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

# Simple match
results = client.search(
    collection_name="documents",
    query_vector=embedding,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="section",
                match=MatchValue(value="Authentication")
            )
        ]
    ),
    limit=5
)

# Multiple conditions (AND)
results = client.search(
    collection_name="documents",
    query_vector=embedding,
    query_filter=Filter(
        must=[
            FieldCondition(key="source_type", match=MatchValue(value="documentation")),
            FieldCondition(key="product_version", match=MatchValue(value="v2.0"))
        ]
    ),
    limit=5
)

# OR conditions
results = client.search(
    collection_name="documents",
    query_vector=embedding,
    query_filter=Filter(
        should=[
            FieldCondition(key="audience", match=MatchValue(value="pro")),
            FieldCondition(key="audience", match=MatchValue(value="enterprise"))
        ]
    ),
    limit=5
)

# NOT conditions
results = client.search(
    collection_name="documents",
    query_vector=embedding,
    query_filter=Filter(
        must_not=[
            FieldCondition(key="classification", match=MatchValue(value="confidential"))
        ]
    ),
    limit=5
)
```

### Advanced Filters

```python
from qdrant_client.models import (
    Filter, FieldCondition, MatchValue, Range, MatchAny
)

# Range filtering (dates, numbers)
results = client.search(
    collection_name="documents",
    query_vector=embedding,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="timestamp",
                range=Range(gte="2025-01-01T00:00:00Z")
            )
        ]
    ),
    limit=5
)

# Match any (IN clause)
results = client.search(
    collection_name="documents",
    query_vector=embedding,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="programming_language",
                match=MatchAny(any=["python", "rust", "typescript"])
            )
        ]
    ),
    limit=5
)

# Nested fields
results = client.search(
    collection_name="documents",
    query_vector=embedding,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="metadata.category",
                match=MatchValue(value="tutorial")
            )
        ]
    ),
    limit=5
)
```

## Hybrid Search (Vector + BM25)

### Setup for Hybrid Search

```python
from qdrant_client.models import VectorParams, Distance, SparseVectorParams

# Create collection with both dense and sparse vectors
client.create_collection(
    collection_name="hybrid_docs",
    vectors_config={
        "dense": VectorParams(size=1024, distance=Distance.COSINE)
    },
    sparse_vectors_config={
        "sparse": SparseVectorParams()  # BM25 index
    }
)
```

### Inserting with Sparse Vectors

```python
from qdrant_client.models import PointStruct, SparseVector

# Generate BM25 vectors (token counts)
def generate_sparse_vector(text):
    # Simplified - use proper BM25 implementation
    tokens = text.lower().split()
    indices = []
    values = []
    for idx, token in enumerate(set(tokens)):
        indices.append(hash(token) % 30000)
        values.append(tokens.count(token))
    return SparseVector(indices=indices, values=values)

# Insert with both dense and sparse
points = [
    PointStruct(
        id=1,
        vector={
            "dense": dense_embedding,  # From OpenAI/Voyage
            "sparse": generate_sparse_vector(text)  # BM25
        },
        payload={"text": text}
    )
]
client.upsert(collection_name="hybrid_docs", points=points)
```

### Hybrid Search with Reciprocal Rank Fusion

```python
from qdrant_client.models import Prefetch, FusionQuery, Fusion

# Hybrid search
results = client.query_points(
    collection_name="hybrid_docs",
    prefetch=[
        # Vector search
        Prefetch(
            query=dense_query_embedding,
            using="dense",
            limit=20
        ),
        # Keyword search (BM25)
        Prefetch(
            query=generate_sparse_vector(query_text),
            using="sparse",
            limit=20
        )
    ],
    query=FusionQuery(fusion=Fusion.RRF),  # Reciprocal Rank Fusion
    limit=5
)
```

## Batch Operations

### Batch Insertion

```python
from qdrant_client.models import PointStruct
import uuid

# Prepare batch
points = []
for idx, (embedding, metadata) in enumerate(chunks):
    points.append(
        PointStruct(
            id=str(uuid.uuid4()),  # Or use integer IDs
            vector=embedding,
            payload=metadata
        )
    )

# Batch upsert (recommended: 100-1000 points per batch)
batch_size = 500
for i in range(0, len(points), batch_size):
    batch = points[i:i + batch_size]
    client.upsert(
        collection_name="documents",
        points=batch,
        wait=True  # Wait for indexing to complete
    )
```

### Batch Search

```python
# Search with multiple vectors at once
search_requests = [
    {"vector": embedding1, "limit": 5},
    {"vector": embedding2, "limit": 5},
    {"vector": embedding3, "limit": 5}
]

batch_results = client.search_batch(
    collection_name="documents",
    requests=search_requests
)
```

## Scroll and Pagination

```python
# Scroll through all points
offset = None
all_points = []

while True:
    response = client.scroll(
        collection_name="documents",
        limit=100,
        offset=offset,
        with_payload=True,
        with_vectors=False  # Don't return vectors to save bandwidth
    )

    all_points.extend(response[0])
    offset = response[1]

    if offset is None:
        break

print(f"Total points: {len(all_points)}")
```

## Collection Management

```python
# List collections
collections = client.get_collections()

# Get collection info
info = client.get_collection(collection_name="documents")
print(f"Vectors count: {info.vectors_count}")
print(f"Points count: {info.points_count}")

# Update collection (add payload index)
client.create_payload_index(
    collection_name="documents",
    field_name="section",
    field_schema="keyword"  # keyword, integer, float, geo
)

# Delete collection
client.delete_collection(collection_name="old_docs")
```

## Performance Optimization

### Search Performance

```python
# Use ef parameter for search quality vs. speed trade-off
results = client.search(
    collection_name="documents",
    query_vector=embedding,
    search_params={"ef": 128},  # Higher = better quality, slower (default: 100)
    limit=5
)
```

### Quantization (Reduce Memory)

```python
from qdrant_client.models import ScalarQuantization, ScalarType

# Create collection with quantization
client.create_collection(
    collection_name="quantized_docs",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
    quantization_config=ScalarQuantization(
        scalar=ScalarType.INT8,  # Reduce memory by ~4x
        quantile=0.99,
        always_ram=True
    )
)
```

### Payload Indexing

```python
# Create index on frequently filtered fields
client.create_payload_index(
    collection_name="documents",
    field_name="source_type",
    field_schema="keyword"
)

client.create_payload_index(
    collection_name="documents",
    field_name="timestamp",
    field_schema="datetime"
)
```

## Monitoring and Observability

```python
# Get cluster info
cluster_info = client.cluster_info()

# Get collection metrics
collection_info = client.get_collection("documents")
print(f"Vectors count: {collection_info.vectors_count}")
print(f"Indexed vectors: {collection_info.indexed_vectors_count}")
print(f"Points count: {collection_info.points_count}")

# Get point by ID
point = client.retrieve(
    collection_name="documents",
    ids=[1, 2, 3],
    with_payload=True,
    with_vectors=False
)
```

## Rust Client Example

```rust
use qdrant_client::{
    client::QdrantClient,
    qdrant::{
        CreateCollection, Distance, PointStruct, SearchPoints,
        VectorParams, VectorsConfig
    }
};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Connect
    let client = QdrantClient::from_url("http://localhost:6333").build()?;

    // Create collection
    client.create_collection(&CreateCollection {
        collection_name: "documents".to_string(),
        vectors_config: Some(VectorsConfig {
            config: Some(qdrant::vectors_config::Config::Params(VectorParams {
                size: 1024,
                distance: Distance::Cosine.into(),
                ..Default::default()
            }))
        }),
        ..Default::default()
    }).await?;

    // Search
    let search_result = client.search_points(&SearchPoints {
        collection_name: "documents".to_string(),
        vector: vec![0.1; 1024],
        limit: 5,
        with_payload: Some(true.into()),
        ..Default::default()
    }).await?;

    Ok(())
}
```

**Context7 ID:** `/websites/rs_qdrant-client_qdrant_client` (1,549 snippets)

## TypeScript Client Example

```typescript
import { QdrantClient } from '@qdrant/js-client-rest';

const client = new QdrantClient({ url: 'http://localhost:6333' });

// Create collection
await client.createCollection('documents', {
  vectors: {
    size: 1024,
    distance: 'Cosine'
  }
});

// Insert
await client.upsert('documents', {
  points: [
    {
      id: 1,
      vector: Array(1024).fill(0.1),
      payload: {
        text: 'Document content',
        source: 'docs/api.md'
      }
    }
  ]
});

// Search
const results = await client.search('documents', {
  vector: Array(1024).fill(0.1),
  limit: 5
});
```

## Common Patterns

### Multi-Tenant RAG System

```python
# Filter by organization/user ID
results = client.search(
    collection_name="documents",
    query_vector=embedding,
    query_filter=Filter(
        must=[
            FieldCondition(key="org_id", match=MatchValue(value=user_org_id))
        ]
    ),
    limit=5
)
```

### Versioned Documentation

```python
# Filter by product version
results = client.search(
    collection_name="documents",
    query_vector=embedding,
    query_filter=Filter(
        must=[
            FieldCondition(key="product_version", match=MatchValue(value="v2.0"))
        ]
    ),
    limit=5
)
```

### Code Search

```python
# Filter by programming language
results = client.search(
    collection_name="code",
    query_vector=embedding,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="language",
                match=MatchAny(any=["python", "rust"])
            )
        ]
    ),
    limit=5
)
```

## Troubleshooting

### Connection Issues
```python
# Check if Qdrant is running
docker ps | grep qdrant

# Test connection
try:
    client = QdrantClient("localhost", port=6333)
    print("Connected:", client.get_collections())
except Exception as e:
    print(f"Connection failed: {e}")
```

### Out of Memory
- Enable quantization (INT8)
- Reduce vector dimensions (maturity shortening)
- Increase Docker memory limit
- Use disk-based storage (not in-memory)

### Slow Searches
- Reduce `ef` parameter (default: 100)
- Create payload indexes on filtered fields
- Use pre-filtering (metadata first, then vector search)
- Consider quantization

## Production Checklist

- [ ] Enable authentication (API keys)
- [ ] Set up monitoring (metrics endpoint)
- [ ] Configure backups (snapshots)
- [ ] Enable TLS/HTTPS
- [ ] Set resource limits (memory, CPU)
- [ ] Create payload indexes on filtered fields
- [ ] Test failover and recovery
- [ ] Document collection schemas
- [ ] Set up alerting (disk space, memory)
- [ ] Implement rate limiting

## Additional Resources

- **Official Docs:** https://qdrant.tech/documentation/
- **Context7 Full Docs:** `/llmstxt/qdrant_tech_llms-full_txt` (10,154 snippets)
- **Python SDK:** `/qdrant/qdrant-client` (43 snippets)
- **Rust SDK:** `/websites/rs_qdrant-client_qdrant_client` (1,549 snippets)
- **LangChain Integration:** `/websites/python_langchain_api_reference_qdrant` (108 snippets)
- **GitHub:** https://github.com/qdrant/qdrant
- **Discord:** https://qdrant.to/discord
