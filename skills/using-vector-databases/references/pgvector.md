# pgvector: PostgreSQL Vector Extension


## Table of Contents

- [Overview](#overview)
- [When to Use pgvector](#when-to-use-pgvector)
  - [Ideal For:](#ideal-for)
  - [Not Ideal For:](#not-ideal-for)
- [Installation](#installation)
  - [PostgreSQL Extension](#postgresql-extension)
  - [Docker Setup](#docker-setup)
  - [Managed Services](#managed-services)
- [Python Integration](#python-integration)
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
- [Distance Metrics](#distance-metrics)
- [Indexing for Performance](#indexing-for-performance)
  - [IVFFlat Index](#ivfflat-index)
  - [HNSW Index (Better Performance)](#hnsw-index-better-performance)
  - [Index Comparison](#index-comparison)
- [Prisma Integration](#prisma-integration)
  - [Schema Definition](#schema-definition)
  - [Usage](#usage)
- [Drizzle ORM Integration](#drizzle-orm-integration)
- [Filtering with Metadata](#filtering-with-metadata)
  - [JSONB Filtering](#jsonb-filtering)
  - [Relational Filtering](#relational-filtering)
- [Batch Operations](#batch-operations)
  - [Bulk Insert](#bulk-insert)
  - [Batch Search](#batch-search)
- [Hybrid Search with pg_search](#hybrid-search-with-pg_search)
- [Performance Optimization](#performance-optimization)
  - [Query Tuning](#query-tuning)
  - [Table Partitioning](#table-partitioning)
  - [Materialized Views](#materialized-views)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
  - [Check Index Usage](#check-index-usage)
  - [Vacuum and Analyze](#vacuum-and-analyze)
  - [Monitor Performance](#monitor-performance)
- [Common Patterns](#common-patterns)
  - [Multi-Tenant RAG](#multi-tenant-rag)
  - [Versioned Documentation](#versioned-documentation)
  - [Code Search](#code-search)
- [Migration from Other Vector DBs](#migration-from-other-vector-dbs)
  - [From Qdrant to pgvector](#from-qdrant-to-pgvector)
- [Limitations](#limitations)
  - [Scale Limits](#scale-limits)
  - [Filtering Performance](#filtering-performance)
  - [Feature Gaps](#feature-gaps)
- [When to Migrate Away](#when-to-migrate-away)
- [Production Checklist](#production-checklist)
- [Additional Resources](#additional-resources)

## Overview

pgvector is an open-source PostgreSQL extension for vector similarity search. It enables vector operations within your existing PostgreSQL database without requiring additional infrastructure.

## When to Use pgvector

### Ideal For:
- **Already using PostgreSQL** - No new infrastructure required
- **<10M vectors** - Performance is good up to this scale
- **Tight budget** - Leverage existing PostgreSQL servers
- **Simple use cases** - Basic similarity search with limited filtering
- **Relational + vector hybrid** - Join vector search with relational data

### Not Ideal For:
- **>10M vectors** - Performance degrades significantly
- **Complex metadata filtering** - Slower than specialized vector DBs
- **High-throughput search** - Limited compared to Qdrant/Milvus
- **Hybrid search** - No built-in BM25, requires extensions (pg_search)

## Installation

### PostgreSQL Extension

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
```

### Docker Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: vectordb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

### Managed Services
- **Supabase** - Built-in pgvector support
- **Neon** - Serverless PostgreSQL with pgvector
- **AWS RDS** - pgvector available on PostgreSQL 15+
- **Google Cloud SQL** - pgvector available
- **Azure Database for PostgreSQL** - pgvector available

## Python Integration

### Installation

```bash
pip install psycopg2-binary pgvector
```

### Basic Usage

```python
import psycopg2
from pgvector.psycopg2 import register_vector

# Connect
conn = psycopg2.connect(
    host="localhost",
    database="vectordb",
    user="postgres",
    password="password"
)
conn.autocommit = True

# Register vector type
register_vector(conn)

# Create table
cur = conn.cursor()
cur.execute("""
    CREATE TABLE documents (
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding vector(1024),
        metadata JSONB
    )
""")

# Insert vectors
embedding = [0.1] * 1024
cur.execute(
    "INSERT INTO documents (content, embedding, metadata) VALUES (%s, %s, %s)",
    ("Document content", embedding, {"source": "docs/api.md"})
)

# Search by similarity (L2 distance)
query_embedding = [0.1] * 1024
cur.execute(
    """
    SELECT id, content, embedding <-> %s AS distance
    FROM documents
    ORDER BY embedding <-> %s
    LIMIT 5
    """,
    (query_embedding, query_embedding)
)
results = cur.fetchall()
```

## Distance Metrics

pgvector supports three distance metrics:

```python
# L2 distance (Euclidean)
cur.execute(
    "SELECT * FROM documents ORDER BY embedding <-> %s LIMIT 5",
    (query_vector,)
)

# Inner product (negated dot product)
cur.execute(
    "SELECT * FROM documents ORDER BY embedding <#> %s LIMIT 5",
    (query_vector,)
)

# Cosine distance (1 - cosine similarity)
cur.execute(
    "SELECT * FROM documents ORDER BY embedding <=> %s LIMIT 5",
    (query_vector,)
)
```

**Which to use?**
- **Cosine (`<=>`)** - Most common for embeddings (OpenAI, Voyage, etc.)
- **L2 (`<->`)** - When vectors are not normalized
- **Inner product (`<#>`)** - For normalized vectors, equivalent to cosine

## Indexing for Performance

### IVFFlat Index

```sql
-- Create IVFFlat index (faster than sequential scan)
CREATE INDEX ON documents USING ivfflat (embedding vector_l2_ops)
WITH (lists = 100);

-- For cosine distance
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- For inner product
CREATE INDEX ON documents USING ivfflat (embedding vector_ip_ops)
WITH (lists = 100);
```

**Lists parameter:**
- Formula: `lists = rows / 1000` (for 1M rows, use lists=1000)
- Trade-off: More lists = faster search, less accurate
- Recommendation: Start with `lists = sqrt(rows)`

### HNSW Index (Better Performance)

```sql
-- Create HNSW index (better recall than IVFFlat)
CREATE INDEX ON documents USING hnsw (embedding vector_l2_ops);

-- For cosine distance
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);

-- Configure parameters
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

**HNSW parameters:**
- **m:** Edges per node (default: 16, higher = better recall, more memory)
- **ef_construction:** Index build quality (default: 64, higher = better index)

### Index Comparison

| Index Type | Speed | Recall | Memory | Best For |
|------------|-------|--------|--------|----------|
| **Sequential** | Slowest | 100% | Low | <10K rows |
| **IVFFlat** | Fast | ~95% | Medium | 10K-1M rows |
| **HNSW** | Fastest | ~99% | High | >100K rows |

## Prisma Integration

### Schema Definition

```prisma
// schema.prisma
generator client {
  provider = "prisma-client-js"
  previewFeatures = ["postgresqlExtensions"]
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  extensions = [vector]
}

model Document {
  id        Int      @id @default(autoincrement())
  content   String
  embedding Unsupported("vector(1024)")
  metadata  Json
  createdAt DateTime @default(now())

  @@map("documents")
}
```

### Usage

```typescript
import { PrismaClient } from '@prisma/client';
import { Prisma } from '@prisma/client';

const prisma = new PrismaClient();

// Insert document with embedding
await prisma.$executeRaw`
  INSERT INTO documents (content, embedding, metadata)
  VALUES (${content}, ${embedding}::vector, ${metadata}::jsonb)
`;

// Similarity search
const results = await prisma.$queryRaw<Array<{
  id: number;
  content: string;
  distance: number;
}>>`
  SELECT id, content, embedding <=> ${queryEmbedding}::vector AS distance
  FROM documents
  ORDER BY embedding <=> ${queryEmbedding}::vector
  LIMIT 5
`;
```

## Drizzle ORM Integration

```typescript
import { pgTable, serial, text, vector, jsonb } from 'drizzle-orm/pg-core';
import { drizzle } from 'drizzle-orm/node-postgres';
import { sql } from 'drizzle-orm';
import { Pool } from 'pg';

// Define schema
export const documents = pgTable('documents', {
  id: serial('id').primaryKey(),
  content: text('content').notNull(),
  embedding: vector('embedding', { dimensions: 1024 }),
  metadata: jsonb('metadata')
});

// Initialize
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const db = drizzle(pool);

// Insert
await db.insert(documents).values({
  content: 'Document content',
  embedding: Array(1024).fill(0.1),
  metadata: { source: 'docs/api.md' }
});

// Search
const results = await db.execute(sql`
  SELECT id, content, embedding <=> ${queryEmbedding}::vector AS distance
  FROM ${documents}
  ORDER BY embedding <=> ${queryEmbedding}::vector
  LIMIT 5
`);
```

## Filtering with Metadata

### JSONB Filtering

```sql
-- Filter by metadata before vector search
SELECT id, content, embedding <=> %s AS distance
FROM documents
WHERE metadata->>'source_type' = 'documentation'
  AND metadata->>'product_version' = 'v2.0'
ORDER BY embedding <=> %s
LIMIT 5;

-- Create index on JSONB for performance
CREATE INDEX idx_metadata_source ON documents
USING gin ((metadata->>'source_type'));
```

### Relational Filtering

```sql
-- Join with relational tables
SELECT d.id, d.content, d.embedding <=> %s AS distance
FROM documents d
JOIN organizations o ON d.org_id = o.id
WHERE o.plan = 'enterprise'
  AND d.is_active = true
ORDER BY d.embedding <=> %s
LIMIT 5;
```

## Batch Operations

### Bulk Insert

```python
from psycopg2.extras import execute_values

# Prepare batch
data = [
    (content, embedding, metadata)
    for content, embedding, metadata in chunks
]

# Bulk insert
execute_values(
    cur,
    """
    INSERT INTO documents (content, embedding, metadata)
    VALUES %s
    """,
    data,
    template="(%s, %s, %s::jsonb)"
)
```

### Batch Search

```python
# Search with multiple vectors
query_vectors = [embedding1, embedding2, embedding3]

for query_vector in query_vectors:
    cur.execute(
        """
        SELECT id, content, embedding <=> %s AS distance
        FROM documents
        ORDER BY embedding <=> %s
        LIMIT 5
        """,
        (query_vector, query_vector)
    )
    results = cur.fetchall()
```

## Hybrid Search with pg_search

Install pg_search extension for BM25 keyword search:

```sql
CREATE EXTENSION IF NOT EXISTS pg_search;

-- Add full-text search column
ALTER TABLE documents ADD COLUMN content_tsv tsvector;

-- Update tsvector column
UPDATE documents
SET content_tsv = to_tsvector('english', content);

-- Create index
CREATE INDEX idx_content_tsv ON documents USING gin(content_tsv);

-- Hybrid search (combine vector + keyword)
WITH vector_results AS (
  SELECT id, content, embedding <=> %s AS distance,
         0.7 AS weight
  FROM documents
  ORDER BY embedding <=> %s
  LIMIT 20
),
keyword_results AS (
  SELECT id, content, ts_rank(content_tsv, query) AS rank,
         0.3 AS weight
  FROM documents, plainto_tsquery('OAuth refresh tokens') query
  WHERE content_tsv @@ query
  ORDER BY rank DESC
  LIMIT 20
)
SELECT DISTINCT ON (id) id, content,
       (vr.distance * vr.weight + kr.rank * kr.weight) AS score
FROM vector_results vr
FULL OUTER JOIN keyword_results kr USING (id)
ORDER BY score
LIMIT 5;
```

## Performance Optimization

### Query Tuning

```sql
-- Set search parameters (trade recall for speed)
SET ivfflat.probes = 10;  -- Default: 1, higher = better recall, slower

SET hnsw.ef_search = 40;  -- Default: 40, higher = better recall
```

### Table Partitioning

```sql
-- Partition by organization for multi-tenant
CREATE TABLE documents (
    id SERIAL,
    org_id INTEGER NOT NULL,
    content TEXT,
    embedding vector(1024),
    metadata JSONB
) PARTITION BY LIST (org_id);

-- Create partitions
CREATE TABLE documents_org1 PARTITION OF documents FOR VALUES IN (1);
CREATE TABLE documents_org2 PARTITION OF documents FOR VALUES IN (2);

-- Create indexes per partition
CREATE INDEX ON documents_org1 USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON documents_org2 USING hnsw (embedding vector_cosine_ops);
```

### Materialized Views

```sql
-- Pre-compute frequently accessed subsets
CREATE MATERIALIZED VIEW recent_docs AS
SELECT id, content, embedding, metadata
FROM documents
WHERE created_at > NOW() - INTERVAL '30 days';

-- Create index on materialized view
CREATE INDEX ON recent_docs USING hnsw (embedding vector_cosine_ops);

-- Refresh periodically
REFRESH MATERIALIZED VIEW recent_docs;
```

## Monitoring and Maintenance

### Check Index Usage

```sql
-- Check if indexes are being used
EXPLAIN ANALYZE
SELECT id, content, embedding <=> %s AS distance
FROM documents
ORDER BY embedding <=> %s
LIMIT 5;
```

### Vacuum and Analyze

```sql
-- Regular maintenance
VACUUM ANALYZE documents;

-- Rebuild indexes if needed
REINDEX TABLE documents;
```

### Monitor Performance

```sql
-- Check table size
SELECT pg_size_pretty(pg_total_relation_size('documents'));

-- Check index sizes
SELECT indexname, pg_size_pretty(pg_relation_size(indexname::regclass))
FROM pg_indexes
WHERE tablename = 'documents';
```

## Common Patterns

### Multi-Tenant RAG

```sql
-- Filter by organization
SELECT id, content, embedding <=> %s AS distance
FROM documents
WHERE org_id = %s
ORDER BY embedding <=> %s
LIMIT 5;

-- Partition by organization for better performance
```

### Versioned Documentation

```sql
-- Filter by version
SELECT id, content, embedding <=> %s AS distance
FROM documents
WHERE metadata->>'product_version' = 'v2.0'
ORDER BY embedding <=> %s
LIMIT 5;
```

### Code Search

```sql
-- Filter by programming language
SELECT id, content, embedding <=> %s AS distance
FROM documents
WHERE metadata->>'content_type' = 'code'
  AND metadata->>'language' = 'python'
ORDER BY embedding <=> %s
LIMIT 5;
```

## Migration from Other Vector DBs

### From Qdrant to pgvector

```python
from qdrant_client import QdrantClient
import psycopg2
from pgvector.psycopg2 import register_vector

# Source: Qdrant
qdrant = QdrantClient("localhost", port=6333)

# Destination: PostgreSQL
conn = psycopg2.connect(database="vectordb")
register_vector(conn)
cur = conn.cursor()

# Scroll through Qdrant
offset = None
while True:
    response = qdrant.scroll(
        collection_name="documents",
        limit=1000,
        offset=offset
    )

    points = response[0]
    for point in points:
        cur.execute(
            "INSERT INTO documents (id, content, embedding, metadata) VALUES (%s, %s, %s, %s)",
            (point.id, point.payload['text'], point.vector, point.payload)
        )

    offset = response[1]
    if offset is None:
        break

conn.commit()
```

## Limitations

### Scale Limits
- **Performance degrades** beyond 10M vectors
- **Memory requirements** increase linearly with vector count
- **Index build time** can be slow for large datasets

### Filtering Performance
- **JSONB queries** are slower than specialized vector DBs
- **Complex filters** can bypass index usage
- **Pre-filtering** may not leverage index

### Feature Gaps
- **No built-in hybrid search** (requires pg_search)
- **No distributed clustering** (single-node only)
- **Limited query optimization** compared to Qdrant/Milvus

## When to Migrate Away

Consider migrating to Qdrant/Milvus/Pinecone if:
- Vector count exceeds 10M
- Need complex metadata filtering at scale
- Require hybrid search (vector + BM25) out of the box
- Need distributed/clustered deployment
- Search latency becomes unacceptable (>100ms p95)

## Production Checklist

- [ ] Enable pgvector extension
- [ ] Create HNSW index for production workloads
- [ ] Set up connection pooling (PgBouncer)
- [ ] Configure autovacuum settings
- [ ] Monitor index usage with EXPLAIN ANALYZE
- [ ] Set up backups (pg_dump)
- [ ] Tune PostgreSQL parameters (shared_buffers, work_mem)
- [ ] Create JSONB indexes on frequently filtered fields
- [ ] Set up monitoring (query performance, table size)
- [ ] Test failover and recovery

## Additional Resources

- **GitHub:** https://github.com/pgvector/pgvector
- **Supabase Guide:** https://supabase.com/docs/guides/ai/vector-databases
- **Neon Guide:** https://neon.tech/docs/extensions/pgvector
- **Performance Tuning:** https://github.com/pgvector/pgvector#performance
