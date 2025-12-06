---
sidebar_position: 14
title: Ingesting Data
description: Data ingestion patterns for loading data from cloud storage, APIs, files, and streaming sources
tags: [backend, data, etl, ingestion, pipelines]
---

# Data Ingestion Patterns

Data ingestion patterns for getting data INTO your systems from external sources.

## When to Use

Use when:
- Importing CSV, JSON, Parquet, or Excel files
- Loading data from S3, GCS, or Azure Blob storage
- Consuming REST/GraphQL API feeds
- Building ETL/ELT pipelines
- Database migration and CDC (Change Data Capture)
- Streaming data ingestion from Kafka/Kinesis

## Multi-Language Support

This skill provides patterns for:
- **Python**: dlt, Polars, boto3, pandas (primary for ETL)
- **TypeScript**: AWS SDK, csv-parse, data transformation
- **Rust**: Polars-rs, aws-sdk-s3, high-performance processing
- **Go**: AWS SDK, encoding/csv, concurrent processing

## Ingestion Pattern Decision Tree

```
What is your data source?
├── Cloud Storage (S3, GCS, Azure) → See cloud-storage.md
├── Files (CSV, JSON, Parquet) → See file-formats.md
├── REST/GraphQL APIs → See api-feeds.md
├── Streaming (Kafka, Kinesis) → See streaming-sources.md
├── Legacy Database → See database-migration.md
└── Need full ETL framework → See etl-tools.md
```

## Quick Start by Language

### Python (Recommended for ETL)

**dlt (data load tool) - Modern Python ETL:**
```python
import dlt

# Define a source
@dlt.source
def github_source(repo: str):
    @dlt.resource(write_disposition="merge", primary_key="id")
    def issues():
        response = requests.get(f"https://api.github.com/repos/{repo}/issues")
        yield response.json()
    return issues

# Load to destination
pipeline = dlt.pipeline(
    pipeline_name="github_issues",
    destination="postgres",  # or duckdb, bigquery, snowflake
    dataset_name="github_data"
)

load_info = pipeline.run(github_source("owner/repo"))
print(load_info)
```

**Polars for file processing (faster than pandas):**
```python
import polars as pl

# Read CSV with schema inference
df = pl.read_csv("data.csv")

# Read Parquet (columnar, efficient)
df = pl.read_parquet("s3://bucket/data.parquet")

# Read JSON lines
df = pl.read_ndjson("events.jsonl")

# Write to database
df.write_database(
    table_name="events",
    connection="postgresql://user:pass@localhost/db",
    if_table_exists="append"
)
```

### TypeScript/Node.js

**S3 ingestion:**
```typescript
import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";
import { parse } from "csv-parse/sync";

const s3 = new S3Client({ region: "us-east-1" });

async function ingestFromS3(bucket: string, key: string) {
  const response = await s3.send(new GetObjectCommand({ Bucket: bucket, Key: key }));
  const body = await response.Body?.transformToString();

  // Parse CSV
  const records = parse(body, { columns: true, skip_empty_lines: true });

  // Insert to database
  await db.insert(eventsTable).values(records);
}
```

**API feed polling:**
```typescript
import { Hono } from "hono";

// Webhook receiver for real-time ingestion
const app = new Hono();

app.post("/webhooks/stripe", async (c) => {
  const event = await c.req.json();

  // Validate webhook signature
  const signature = c.req.header("stripe-signature");
  // ... validation logic

  // Ingest event
  await db.insert(stripeEventsTable).values({
    eventId: event.id,
    type: event.type,
    data: event.data,
    receivedAt: new Date()
  });

  return c.json({ received: true });
});
```

### Rust

**High-performance file ingestion:**
```rust
use polars::prelude::*;
use aws_sdk_s3::Client;

async fn ingest_parquet(client: &Client, bucket: &str, key: &str) -> Result<DataFrame> {
    // Download from S3
    let resp = client.get_object()
        .bucket(bucket)
        .key(key)
        .send()
        .await?;

    let bytes = resp.body.collect().await?.into_bytes();

    // Parse with Polars
    let df = ParquetReader::new(Cursor::new(bytes))
        .finish()?;

    Ok(df)
}
```

### Go

**Concurrent file processing:**
```go
package main

import (
    "context"
    "encoding/csv"
    "github.com/aws/aws-sdk-go-v2/service/s3"
)

func ingestCSV(ctx context.Context, client *s3.Client, bucket, key string) error {
    resp, err := client.GetObject(ctx, &s3.GetObjectInput{
        Bucket: &bucket,
        Key:    &key,
    })
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    reader := csv.NewReader(resp.Body)
    records, err := reader.ReadAll()
    if err != nil {
        return err
    }

    // Batch insert to database
    return batchInsert(ctx, records)
}
```

## Ingestion Patterns

### 1. Batch Ingestion (Files/Storage)

For periodic bulk loads:

```
Source → Extract → Transform → Load → Validate
  ↓         ↓          ↓         ↓        ↓
 S3      Download   Clean/Map  Insert   Count check
```

**Key considerations:**
- Use chunked reading for large files (>100MB)
- Implement idempotency with checksums
- Track file processing state
- Handle partial failures

### 2. Streaming Ingestion (Real-time)

For continuous data flow:

```
Source → Buffer → Process → Load → Ack
  ↓        ↓         ↓        ↓      ↓
Kafka   In-memory  Transform  DB   Commit offset
```

**Key considerations:**
- At-least-once vs exactly-once semantics
- Backpressure handling
- Dead letter queues for failures
- Checkpoint management

### 3. API Polling (Feeds)

For external API data:

```
Schedule → Fetch → Dedupe → Load → Update cursor
   ↓         ↓        ↓       ↓         ↓
 Cron     API call  By ID   Insert   Last timestamp
```

**Key considerations:**
- Rate limiting and backoff
- Incremental loading (cursors, timestamps)
- API pagination handling
- Retry with exponential backoff

### 4. Change Data Capture (CDC)

For database replication:

```
Source DB → Capture changes → Transform → Target DB
    ↓             ↓               ↓            ↓
 Postgres    Debezium/WAL      Map schema   Insert/Update
```

**Key considerations:**
- Initial snapshot + streaming changes
- Schema evolution handling
- Ordering guarantees
- Conflict resolution

## Library Recommendations

| Use Case | Python | TypeScript | Rust | Go |
|----------|--------|------------|------|-----|
| **ETL Framework** | dlt, Meltano, Dagster | - | - | - |
| **Cloud Storage** | boto3, gcsfs, adlfs | @aws-sdk/*, @google-cloud/* | aws-sdk-s3, object_store | aws-sdk-go-v2 |
| **File Processing** | polars, pandas, pyarrow | papaparse, xlsx, parquetjs | polars-rs, arrow-rs | encoding/csv, parquet-go |
| **Streaming** | confluent-kafka, aiokafka | kafkajs | rdkafka-rs | franz-go, sarama |
| **CDC** | Debezium, pg_logical | - | - | - |

## Chaining with Database Skills

After ingestion, chain to appropriate database skill:

| Destination | Chain to Skill |
|-------------|----------------|
| PostgreSQL, MySQL | [Relational Databases](./using-relational-databases) |
| MongoDB, DynamoDB | [Document Databases](./using-document-databases) |
| Qdrant, Pinecone | [Vector Databases](./using-vector-databases) (after embedding) |
| ClickHouse, TimescaleDB | [Time-Series Databases](./using-timeseries-databases) |
| Neo4j | [Graph Databases](./using-graph-databases) |

For vector databases, chain through `ai-data-engineering` for embedding:
```
ingesting-data → ai-data-engineering → databases-vector
```

## Common Workflows

### CSV to PostgreSQL

```python
import polars as pl

# Read CSV
df = pl.read_csv("users.csv")

# Write to PostgreSQL
df.write_database(
    table_name="users",
    connection="postgresql://user:pass@localhost/db",
    if_table_exists="append"
)
```

### S3 to Data Warehouse

```python
import dlt

@dlt.source
def s3_source(bucket: str, prefix: str):
    @dlt.resource
    def files():
        for key in list_s3_keys(bucket, prefix):
            data = read_s3_file(bucket, key)
            yield data

pipeline = dlt.pipeline(
    pipeline_name="s3_to_warehouse",
    destination="snowflake",
    dataset_name="raw_data"
)

pipeline.run(s3_source("my-bucket", "data/"))
```

### API to Database

```python
import dlt
import requests

@dlt.source
def api_source(endpoint: str):
    @dlt.resource(write_disposition="merge", primary_key="id")
    def records():
        cursor = None
        while True:
            response = requests.get(endpoint, params={"cursor": cursor})
            data = response.json()
            yield data["items"]
            cursor = data.get("next_cursor")
            if not cursor:
                break

pipeline = dlt.pipeline(
    pipeline_name="api_to_db",
    destination="postgres",
    dataset_name="external_data"
)

pipeline.run(api_source("https://api.example.com/data"))
```

## Best Practices

**Idempotency:**
- Use checksums to detect duplicate files
- Implement upsert logic (INSERT ... ON CONFLICT)
- Track processing state in metadata table

**Performance:**
- Batch inserts (1000-10000 rows)
- Use chunked reading for large files
- Parallel processing where possible
- Use columnar formats (Parquet) for analytics

**Reliability:**
- Implement retry logic with exponential backoff
- Use dead letter queues for failed records
- Monitor ingestion metrics (rows/sec, failures)
- Set up alerts for pipeline failures

**Security:**
- Use IAM roles for cloud storage access
- Validate data schemas before insertion
- Sanitize inputs to prevent SQL injection
- Encrypt sensitive data at rest and in transit

## Related Skills

- [AI Data Engineering](./ai-data-engineering) - RAG pipeline ingestion
- [Relational Databases](./using-relational-databases) - Target for structured data
- [Time-Series Databases](./using-timeseries-databases) - Target for metrics/events
- [Vector Databases](./using-vector-databases) - Target for embeddings (after processing)

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/ingesting-data)
- dlt: https://dlthub.com/
- Polars: https://pola.rs/
- AWS SDK: https://aws.amazon.com/sdk-for-python/
- Debezium: https://debezium.io/
