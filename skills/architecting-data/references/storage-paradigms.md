# Storage Paradigms Deep Dive

## Table of Contents

1. [Data Lake](#data-lake)
2. [Data Warehouse](#data-warehouse)
3. [Data Lakehouse](#data-lakehouse)
4. [Architectural Patterns](#architectural-patterns)

---

## Data Lake

### Definition

Centralized repository storing raw data in native format at massive scale. Schema-on-read approach allows flexibility but requires discipline to avoid "data swamp."

### Core Characteristics

- **Schema-on-read:** Structure applied when querying, not when storing
- **Format-agnostic:** CSV, JSON, Parquet, Avro, images, videos, logs
- **Cost-optimized:** Object storage (AWS S3, Google GCS, Azure ADLS)
- **Scalability:** Petabyte+ capacity with linear scaling
- **Immutability:** Write-once, read-many pattern

### Three-Zone Architecture

```
┌─────────────────────────────────────────┐
│ Raw Zone (Bronze)                       │
│ - Exact copy of source data             │
│ - No transformations                    │
│ - Immutable historical record           │
│ - Retention: Forever                    │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Cleaned Zone (Silver)                   │
│ - Validated, deduplicated               │
│ - Type conversions                      │
│ - Normalized formats                    │
│ - Retention: 1-2 years                  │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Curated Zone (Gold)                     │
│ - Business-level aggregates             │
│ - Ready for consumption                 │
│ - Optimized for queries                 │
│ - Retention: Business-defined           │
└─────────────────────────────────────────┘
```

### When to Use Data Lake

**Ideal Scenarios:**
- Diverse data sources (structured + semi-structured + unstructured)
- Exploratory analytics with unknown use cases
- ML/AI training data requiring raw, full-history data
- Cost-sensitive workloads (storage is cheapest)
- Long-term archival (years to decades)
- Future-proof data retention

**Anti-Patterns:**
- Known BI/reporting requirements (warehouse is better)
- Need for strong data quality guarantees
- Users require SQL-first interface
- No data engineering team to manage complexity

### Trade-Offs

**Advantages:**
- Lowest storage cost ($0.02-0.03/GB/month)
- Maximum schema flexibility
- Store all data types
- Future-proof (keep raw data for unforeseen use cases)
- No upfront schema design required

**Disadvantages:**
- No ACID guarantees (eventual consistency)
- Data quality issues common ("garbage in, garbage out")
- Governance challenges (risk of data swamp)
- Slower query performance vs warehouse
- Requires data engineering expertise

### Technologies

**Storage:**
- AWS S3 (Standard, Infrequent Access, Glacier tiers)
- Google Cloud Storage (Standard, Nearline, Coldline)
- Azure Data Lake Storage Gen2

**File Formats:**
- Parquet (columnar, best for analytics)
- ORC (columnar, Hive-optimized)
- Avro (row-based, schema evolution)
- JSON, CSV (human-readable, not optimized)

**Query Engines:**
- Presto / Trino (distributed SQL)
- AWS Athena (serverless Presto)
- Apache Spark (batch and streaming)
- Google Cloud Dataproc (managed Spark)

---

## Data Warehouse

### Definition

Centralized, structured repository optimized for analytical queries. Schema-on-write enforces data quality but reduces flexibility.

### Core Characteristics

- **Schema-on-write:** Structure enforced on ingestion
- **Optimized for BI:** Indexing, partitioning, materialized views
- **ACID transactions:** Consistency guaranteed
- **Columnar storage:** Only read needed columns
- **Query optimization:** Cost-based optimizer, statistics

### Three-Layer Architecture

```
┌─────────────────────────────────────────┐
│ Staging Layer                           │
│ - Raw data ingestion                    │
│ - Temporary storage                     │
│ - Minimal transformations               │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Integration Layer (EDW)                 │
│ - Cleaned, conformed data               │
│ - Normalized or data vault              │
│ - Source of truth                       │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Presentation Layer (Data Marts)         │
│ - Star/snowflake schemas                │
│ - Department-specific views             │
│ - Optimized for reporting               │
└─────────────────────────────────────────┘
```

### When to Use Data Warehouse

**Ideal Scenarios:**
- Structured, relational data primarily
- Known BI and reporting use cases
- Strong governance and compliance requirements
- Performance-critical dashboards
- Financial reporting, regulatory compliance
- Business users need SQL interface

**Anti-Patterns:**
- Highly unstructured data (images, videos, logs)
- Exploratory analytics with unknown requirements
- Rapid schema changes
- Tight budget constraints

### Trade-Offs

**Advantages:**
- Best query performance (sub-second for most queries)
- Strong governance and data quality
- ACID transactions
- Mature tooling and ecosystem
- User-friendly for analysts (SQL interface)

**Disadvantages:**
- Highest storage cost ($20-40/TB/month)
- Schema inflexibility (migrations are painful)
- Not ideal for unstructured data
- Difficult to support ML workloads requiring raw data
- Compute tightly coupled to storage (scaling complexity)

### Technologies

**Cloud Data Warehouses:**
- Snowflake (multi-cloud, zero-maintenance)
- Google BigQuery (serverless, pay-per-query)
- AWS Redshift (AWS-native, columnar)
- Azure Synapse Analytics (Azure-native, integrated)

**On-Premises (Legacy):**
- Teradata
- Oracle Exadata
- IBM Netezza
- Vertica

### Optimization Techniques

**1. Partitioning:**
- Time-based (daily, monthly) - most common
- Geography (region, country)
- Hash (even distribution)

**2. Clustering:**
- Co-locate related data on disk
- Snowflake: Automatic micro-partitions + clustering keys
- BigQuery: Clustering columns (max 4)

**3. Materialized Views:**
- Pre-compute expensive aggregations
- Auto-refresh on base table changes
- Trade storage cost for query performance

**4. Incremental Loading:**
- Only load new/changed data
- Watermark column (e.g., `last_updated_timestamp`)
- Reduces load time by 90%+

---

## Data Lakehouse

### Definition

Hybrid architecture combining data lake cost efficiency and flexibility with data warehouse reliability and performance. Enabled by open table formats (Iceberg, Delta Lake, Hudi).

### Core Characteristics

- **Open table formats:** ACID transactions on object storage
- **Schema enforcement:** Optional validation on write
- **Time travel:** Query historical versions
- **Unified platform:** BI and ML on same data
- **Multi-engine support:** Spark, Trino, Flink, Presto
- **Cost-effective:** Lake storage prices with warehouse features

### Architecture

```
┌─────────────────────────────────────────┐
│ Cloud Object Storage (S3, GCS, ADLS)   │
│ - Low-cost, scalable                    │
│ - Parquet/ORC files                     │
│ - Open formats (no proprietary lock-in)│
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Metadata Layer (Iceberg/Delta)          │
│ - Table schema, statistics              │
│ - Partition information                 │
│ - Transaction log (ACID)                │
│ - Time travel snapshots                 │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Compute Engines (Multi-Engine)          │
│ - Spark (batch, ML)                     │
│ - Trino/Presto (SQL analytics)          │
│ - Flink (streaming)                     │
│ - Dremio (semantic layer)               │
└─────────────────────────────────────────┘
```

### When to Use Data Lakehouse

**Ideal Scenarios:**
- Both BI and ML workloads (unified platform)
- Cost optimization (60-80% cheaper than warehouse)
- Multi-engine access (Spark, Trino, Flink)
- Schema evolution requirements (frequent changes)
- Streaming + batch processing
- Avoid vendor lock-in (open formats)

**Anti-Patterns:**
- Only BI workloads (warehouse is simpler)
- Very small scale (<100GB data)
- No data engineering expertise
- Legacy tools incompatible with lakehouse

### Trade-Offs

**Advantages:**
- Cost-effective (lake pricing, warehouse features)
- Flexible (structured + semi-structured)
- Multi-engine support (avoid vendor lock-in)
- Open formats (Iceberg, Delta Lake)
- Time travel and schema evolution
- Unified BI + ML platform

**Disadvantages:**
- Newer technology (less mature than warehouse)
- Performance not quite warehouse-level (improving)
- Requires careful optimization (partitioning, clustering)
- Steeper learning curve
- Smaller ecosystem than traditional warehouses

### Technologies

**Table Formats:**
- Apache Iceberg (vendor-neutral, multi-engine)
- Delta Lake (Databricks-led, Spark-optimized)
- Apache Hudi (upsert-optimized, streaming)

**Lakehouse Platforms:**
- Databricks (Delta Lake native)
- Snowflake (Iceberg support added)
- AWS Lake Formation (Iceberg + Hudi)
- Dremio (Iceberg semantic layer)

**Compute Engines:**
- Apache Spark
- Trino / Presto
- Apache Flink
- Dremio

---

## Architectural Patterns

### Lambda Architecture (Batch + Speed Layers)

```
Data Sources
     ↓
┌────────────────────┬────────────────────┐
│ Batch Layer        │ Speed Layer        │
│ (Hourly/Daily)     │ (Real-time)        │
│ - Historical data  │ - Recent data      │
│ - Reprocessable    │ - Low latency      │
│ - Spark batch      │ - Kafka + Flink    │
└──────────┬─────────┴──────────┬─────────┘
           │                     │
           ↓                     ↓
      Batch View            Real-time View
           │                     │
           └──────────┬──────────┘
                      ↓
                 Serving Layer
                  (Queries)
```

**When to Use:**
- Need both historical accuracy and real-time insights
- Batch reprocessing for data corrections
- Trade-off between latency and correctness

**Challenges:**
- Complexity (two parallel pipelines)
- Code duplication (batch and streaming logic)
- Consistency challenges between layers

### Kappa Architecture (Streaming-Only)

```
Data Sources
     ↓
 Stream Processing
 (Kafka + Flink)
     ↓
┌────────────────────┬────────────────────┐
│ Serving Layer      │ Archive Layer      │
│ (Last 30 days)     │ (All history)      │
│ - Fast queries     │ - S3/GCS           │
│ - Hot data         │ - Reprocessable    │
└────────────────────┴────────────────────┘
```

**When to Use:**
- Streaming-first organization
- Simplified architecture (one pipeline)
- Reprocessing via stream replay

**Challenges:**
- Stream processing for everything (including batch)
- Requires mature streaming infrastructure
- Reprocessing can be slow

### Medallion Architecture (Databricks/Lakehouse Standard)

```
Bronze Layer (Raw)
- Exact copy of source
- Append-only
- All history retained
     ↓
Silver Layer (Cleaned)
- Validated, deduplicated
- Type conversions
- Slowly Changing Dimensions applied
     ↓
Gold Layer (Business-level)
- Aggregates
- Star schemas
- Feature tables
- Ready for BI/ML
```

**When to Use:**
- Lakehouse platform (Databricks, Iceberg)
- Clear data quality layers
- Progressive data refinement

**Benefits:**
- Clear separation of concerns
- Reprocessing at any layer
- Incremental quality improvement

### Comparison

| Pattern | Complexity | Real-Time | Batch | Reprocessing |
|---------|------------|-----------|-------|--------------|
| Lambda | High | Excellent | Excellent | Batch layer |
| Kappa | Medium | Excellent | Good | Stream replay |
| Medallion | Low-Medium | Good | Excellent | Any layer |

**Recommendation:**
- Start with **Medallion** (simplest, most flexible)
- Add **Kappa** if streaming-first
- Avoid **Lambda** unless strong requirement for separate batch/speed layers
