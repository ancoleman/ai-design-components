# Milvus: Billion-Scale Vector Database

## Overview

Milvus is an open-source vector database designed for billion-scale vector similarity search with GPU acceleration support.

## When to Use Milvus

### Ideal For:
- **>100M vectors** - Optimized for massive scale
- **GPU acceleration** - Leverage CUDA for 10-100x faster search
- **Enterprise features** - Role-based access control, multi-tenancy
- **Distributed deployments** - Horizontal scaling across nodes
- **High throughput** - Millions of searches per second

### Not Ideal For:
- **<10M vectors** - Overkill for small datasets (use Qdrant/pgvector)
- **Simple use cases** - More complex than Qdrant
- **Resource-constrained** - Requires more infrastructure
- **Rapid prototyping** - Longer setup time

## Architecture Options

### Standalone Mode
- Single-node deployment
- Up to 100M vectors
- Good for development and small production workloads

### Cluster Mode
- Distributed deployment
- Billions of vectors
- Horizontal scaling
- Production-grade high availability

### Zilliz Cloud (Managed)
- Fully managed Milvus
- Serverless options available
- Auto-scaling
- Built-in monitoring

## Installation

### Docker (Standalone)

```bash
# Pull Milvus
docker pull milvusdb/milvus:latest

# Run standalone
docker run -d --name milvus \
  -p 19530:19530 \
  -p 9091:9091 \
  -v milvus_data:/var/lib/milvus \
  milvusdb/milvus:latest
```

### Docker Compose (with etcd, MinIO)

```yaml
version: '3.5'

services:
  etcd:
    image: quay.io/coreos/etcd:latest
    environment:
      - ETCD_AUTO_COMPACTION_MODE=revision
      - ETCD_AUTO_COMPACTION_RETENTION=1000
      - ETCD_QUOTA_BACKEND_BYTES=4294967296

  minio:
    image: minio/minio:latest
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: minio server /minio_data

  milvus:
    image: milvusdb/milvus:latest
    depends_on:
      - etcd
      - minio
    ports:
      - "19530:19530"
      - "9091:9091"
    volumes:
      - milvus_data:/var/lib/milvus
```

## Python Client

### Installation

```bash
pip install pymilvus
```

### Basic Usage

```python
from pymilvus import (
    connections, Collection, CollectionSchema, FieldSchema, DataType
)

# Connect
connections.connect("default", host="localhost", port="19530")

# Define schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
    FieldSchema(name="metadata", dtype=DataType.JSON)
]
schema = CollectionSchema(fields, description="Documents collection")

# Create collection
collection = Collection(name="documents", schema=schema)

# Insert data
entities = [
    [text1, text2, text3],                    # text field
    [[0.1]*1024, [0.2]*1024, [0.3]*1024],   # embedding field
    [{"source": "doc1"}, {"source": "doc2"}, {"source": "doc3"}]  # metadata
]
collection.insert(entities)

# Create index (HNSW recommended)
index_params = {
    "index_type": "HNSW",
    "metric_type": "COSINE",
    "params": {"M": 16, "efConstruction": 256}
}
collection.create_index(field_name="embedding", index_params=index_params)

# Load collection to memory
collection.load()

# Search
search_params = {"metric_type": "COSINE", "params": {"ef": 64}}
results = collection.search(
    data=[[0.1]*1024],
    anns_field="embedding",
    param=search_params,
    limit=5,
    expr="metadata['source'] == 'doc1'"  # Filtering
)
```

## Index Types

### IVF_FLAT
- **Best for:** <1M vectors
- **Memory:** High (stores full vectors)
- **Speed:** Fast
- **Recall:** Good

```python
index_params = {
    "index_type": "IVF_FLAT",
    "metric_type": "COSINE",
    "params": {"nlist": 1024}
}
```

### IVF_SQ8 (Scalar Quantization)
- **Best for:** 1M-10M vectors
- **Memory:** Medium (8-bit quantization)
- **Speed:** Very fast
- **Recall:** Good

```python
index_params = {
    "index_type": "IVF_SQ8",
    "metric_type": "COSINE",
    "params": {"nlist": 1024}
}
```

### HNSW (Recommended)
- **Best for:** All scales
- **Memory:** High
- **Speed:** Fastest
- **Recall:** Excellent

```python
index_params = {
    "index_type": "HNSW",
    "metric_type": "COSINE",
    "params": {
        "M": 16,              # Edges per node (8-64)
        "efConstruction": 256  # Build quality (40-500)
    }
}
```

### GPU Indexes (CUDA Required)

```python
# GPU_IVF_FLAT - Fastest with GPU
index_params = {
    "index_type": "GPU_IVF_FLAT",
    "metric_type": "COSINE",
    "params": {"nlist": 1024}
}

# GPU_IVF_PQ - GPU + Product Quantization
index_params = {
    "index_type": "GPU_IVF_PQ",
    "metric_type": "COSINE",
    "params": {"nlist": 1024, "m": 8, "nbits": 8}
}
```

## Filtering with Scalar Fields

```python
# Define schema with scalar fields for filtering
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024),
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="timestamp", dtype=DataType.INT64),
    FieldSchema(name="metadata", dtype=DataType.JSON)
]

# Search with filtering
results = collection.search(
    data=[[0.1]*1024],
    anns_field="embedding",
    param=search_params,
    limit=5,
    expr='category == "documentation" and timestamp > 1640000000000'
)
```

## Hybrid Search (Vector + Scalar)

```python
# Pre-filter with scalar, then vector search
results = collection.search(
    data=[[0.1]*1024],
    anns_field="embedding",
    param=search_params,
    limit=5,
    expr='metadata["product_version"] == "v2.0"',
    output_fields=["text", "metadata"]
)
```

## Partition Management (Multi-Tenancy)

```python
# Create partitions for different tenants/categories
collection.create_partition("org_1")
collection.create_partition("org_2")

# Insert into specific partition
collection.insert(entities, partition_name="org_1")

# Search in specific partition
results = collection.search(
    data=[[0.1]*1024],
    anns_field="embedding",
    param=search_params,
    limit=5,
    partition_names=["org_1"]
)
```

## Performance Optimization

### Batch Operations

```python
# Batch insert (10K-50K vectors per batch)
batch_size = 10000
for i in range(0, len(embeddings), batch_size):
    batch_embeddings = embeddings[i:i+batch_size]
    batch_texts = texts[i:i+batch_size]
    collection.insert([batch_texts, batch_embeddings])
```

### Search Parameters Tuning

```python
# Adjust ef for recall vs. speed trade-off
search_params = {
    "metric_type": "COSINE",
    "params": {
        "ef": 128  # Higher = better recall, slower (default: 64)
    }
}
```

### Resource Configuration

```yaml
# Configure Milvus resources
queryNode:
  replicas: 3
  resources:
    limits:
      memory: 32Gi
      cpu: 8
    requests:
      memory: 16Gi
      cpu: 4

dataNode:
  replicas: 2
  resources:
    limits:
      memory: 16Gi
```

## Monitoring

```python
# Get collection stats
stats = collection.get_stats()
print(f"Row count: {stats['row_count']}")

# Get query node metrics
from pymilvus import utility
metrics = utility.get_query_segment_info("documents")
```

## Zilliz Cloud (Managed Milvus)

```python
from pymilvus import connections

# Connect to Zilliz Cloud
connections.connect(
    alias="default",
    uri="https://your-cluster.cloud.zilliz.com:19530",
    token="your-api-key"
)
```

## Use Cases

### Billion-Scale Semantic Search
- E-commerce product search (100M+ products)
- Video similarity search (millions of videos)
- Image search engines

### Recommendation Systems
- Content recommendations at Netflix scale
- Product recommendations for large catalogs
- User behavior-based recommendations

### Anomaly Detection
- Security threat detection across billions of events
- Fraud detection in financial transactions
- Network intrusion detection

## Production Checklist

- [ ] Deploy in cluster mode for high availability
- [ ] Configure resource limits (CPU, memory, GPU)
- [ ] Set up monitoring (Prometheus, Grafana)
- [ ] Enable authentication and authorization
- [ ] Configure backups (snapshots)
- [ ] Tune index parameters (M, efConstruction)
- [ ] Set up load balancing
- [ ] Test failover and recovery
- [ ] Monitor query performance
- [ ] Configure partitions for multi-tenancy

## Additional Resources

- **Official Docs:** https://milvus.io/docs
- **GitHub:** https://github.com/milvus-io/milvus
- **Zilliz Cloud:** https://cloud.zilliz.com
- **Performance Tuning:** https://milvus.io/docs/tune.md
- **Slack Community:** https://milvusio.slack.com
