# Data Pipeline Blueprint

**Version:** 1.0.0
**Last Updated:** 2025-12-06
**Category:** Data

---

## Overview

Pre-configured skill chain optimized for building production-grade data pipelines, ETL workflows, streaming data architectures, and batch processing systems. This blueprint provides battle-tested defaults for the most common data engineering patterns, minimizing configuration while maximizing reliability and performance.

---

## Trigger Keywords

**Primary (high confidence):**
- data pipeline
- etl
- data ingestion
- data processing
- streaming
- batch processing

**Secondary (medium confidence):**
- kafka
- spark
- airflow
- data warehouse
- data lake
- data transformation
- data integration
- data flow

**Example goals that match:**
- "ETL pipeline from PostgreSQL to Snowflake"
- "real-time streaming pipeline with Kafka"
- "batch processing pipeline for analytics"
- "data ingestion from APIs to data warehouse"
- "build data pipeline with validation and monitoring"
- "streaming data processing with transformations"

---

## Skill Chain (Pre-configured)

This blueprint invokes 6 skills in the following order:

```
1. designing-databases-relational   (data modeling - source/destination schemas)
2. streaming-data                   (real-time processing architecture)
3. optimizing-sql                   (query performance and transformations)
4. testing-strategies               (data quality and validation tests)
5. implementing-observability       (pipeline monitoring and alerting)
6. writing-documentation            (pipeline documentation and runbooks)
```

**Total estimated time:** 35-45 minutes
**Total estimated questions:** 10-15 questions (or 3 with blueprint defaults)

---

## Pre-configured Defaults

### 1. designing-databases-relational
```yaml
schema_design: "star-schema"
  # Optimized for analytics workloads
  # Fact tables: Transactional events, metrics
  # Dimension tables: Reference data, lookups
  # Supports efficient JOIN operations

normalization: "3NF-source-denormalized-target"
  # Source: Normalized (3NF) for data integrity
  # Target: Denormalized (star/snowflake) for query performance
  # Balance between consistency and speed

partitioning_strategy: "time-based"
  # Partition by date/timestamp (daily or monthly)
  # Enables efficient incremental processing
  # Supports retention policies and archival

indexes: "selective"
  # Primary keys: Clustered indexes on fact tables
  # Foreign keys: Non-clustered indexes on dimension tables
  # Composite indexes for common query patterns
  # Avoid over-indexing (impacts write performance)

data_types: "strict"
  # Enforce explicit data types (no VARCHAR(MAX))
  # Use appropriate precision (DECIMAL for money)
  # Timestamp with timezone for temporal data
  # JSON/JSONB for semi-structured data
```

### 2. streaming-data
```yaml
architecture: "kappa"
  # Single stream processing layer (no batch layer)
  # Real-time processing with replayable event log
  # Simpler than Lambda architecture for most use cases
  # Kafka or Kinesis as event backbone

processing_model: "micro-batching"
  # Balance between latency and throughput
  # Default window: 5 seconds
  # Enables aggregations and windowing operations
  # Better resource utilization than per-event processing

backpressure_handling: "dynamic-scaling"
  # Auto-scale consumers based on lag
  # Rate limiting on producers
  # Dead letter queue for failed messages
  # Circuit breaker for downstream failures

message_format: "avro"
  # Schema evolution support
  # Compact binary format
  # Schema registry for version management
  # Better than JSON for high-volume streams

exactly_once_semantics: true
  # Idempotent producers
  # Transactional consumers
  # Deduplication at sink
  # Critical for financial/billing data

watermarking: "event-time"
  # Use event timestamp (not processing time)
  # Handle late-arriving data
  # Configurable allowed lateness (default: 1 hour)
  # Ensures correct windowing and aggregations
```

### 3. optimizing-sql
```yaml
query_optimization: "explain-plan-driven"
  # Analyze execution plans for all queries
  # Identify sequential scans, missing indexes
  # Optimize JOIN order and conditions
  # Use CTEs for readability, subqueries for performance

materialized_views: true
  # Pre-compute expensive aggregations
  # Refresh strategy: Incremental (not full refresh)
  # Index materialized views for query performance
  # Balance freshness vs. compute cost

partitioning: "range-and-hash"
  # Range partitioning on timestamp (primary)
  # Hash partitioning on high-cardinality keys (secondary)
  # Enables partition pruning in queries
  # Supports parallel processing

batch_operations: true
  # Bulk INSERT/UPDATE over row-by-row
  # Use COPY for large data loads
  # Batch DELETE with chunking (avoid locks)
  # Transaction batching for commit efficiency

connection_pooling: true
  # Pool size: 10-50 connections (based on load)
  # Connection timeout: 30 seconds
  # Idle connection timeout: 5 minutes
  # Prevents connection exhaustion
```

### 4. testing-strategies
```yaml
data_quality_tests: "great-expectations"
  # Expectation suites for each data source
  # Validate schema, completeness, uniqueness, ranges
  # Run on every pipeline execution
  # Fail pipeline on critical violations

test_levels:
  unit: "transformation-functions"
    # Test individual data transformations
    # Pure functions, deterministic outputs
    # Mock data sources and sinks

  integration: "end-to-end-pipeline"
    # Test full pipeline with sample data
    # Validate source → transform → sink flow
    # Check idempotency and error handling

  data_quality: "production-data-sampling"
    # Sample recent production data
    # Run validation rules
    # Monitor quality metrics over time

validation_rules:
  - schema_validation: "strict"
      # Column names, types, nullability
      # Fail on schema drift

  - completeness: "required-fields"
      # No nulls in non-nullable columns
      # Row count expectations

  - uniqueness: "primary-keys"
      # Duplicate detection
      # Composite key validation

  - freshness: "max-staleness"
      # Data arrival SLAs
      # Alert if data delayed >1 hour

  - referential_integrity: "foreign-keys"
      # Validate JOIN integrity
      # Orphaned record detection

test_data: "production-snapshot"
  # Use anonymized production data
  # Realistic data distributions
  # Include edge cases and outliers
```

### 5. implementing-observability
```yaml
metrics: "prometheus-format"
  # Pipeline-level metrics:
    # - Records processed per second
    # - Processing latency (p50, p95, p99)
    # - Error rate (errors per 1000 records)
    # - Backlog/lag (for streaming)
    # - Resource utilization (CPU, memory, disk)

  # Data quality metrics:
    # - Validation failures
    # - Schema violations
    # - Null rate by column
    # - Duplicate rate

logging: "structured-json"
  # JSON format for easy parsing
  # Log levels: DEBUG, INFO, WARN, ERROR, CRITICAL
  # Include correlation IDs for request tracing
  # Log sampling for high-volume events (1% of INFO)

tracing: "distributed"
  # OpenTelemetry for trace propagation
  # Trace each record through pipeline stages
  # Identify bottlenecks and latency spikes
  # Visualize in Jaeger or Zipkin

alerting: "threshold-and-anomaly"
  # Threshold alerts:
    # - Error rate >1%
    # - Processing lag >5 minutes
    # - Data freshness >1 hour
    # - Validation failure rate >5%

  # Anomaly detection:
    # - Sudden drop in throughput
    # - Unusual data patterns
    # - Resource spikes

alert_channels:
  critical: "pagerduty"
    # Pipeline failures
    # Data loss events
    # SLA violations

  warning: "slack"
    # Performance degradation
    # Validation warnings
    # Resource alerts

  info: "dashboard"
    # Daily summaries
    # Trend analysis

dashboards: "grafana"
  # Real-time pipeline health
  # Historical performance trends
  # Data quality scorecards
  # Resource utilization
  # Alert status
```

### 6. writing-documentation
```yaml
documentation_types:
  architecture: "pipeline-diagram"
    # Data flow visualization
    # Component dependencies
    # Technology stack
    # Deployment topology

  runbook: "operational-procedures"
    # Deployment steps
    # Rollback procedures
    # Troubleshooting guides
    # Common failure modes

  data_dictionary: "schema-catalog"
    # Table and column descriptions
    # Data lineage
    # Sample values
    # Business rules

  sla: "service-level-objectives"
    # Latency targets
    # Freshness guarantees
    # Availability requirements
    # Error budgets

format: "markdown-with-diagrams"
  # Markdown for readability
  # Mermaid diagrams for data flow
  # Code blocks for SQL/config
  # Searchable and version-controlled

maintenance: "living-documentation"
  # Update with code changes
  # Review quarterly
  # Include in PR checklist
  # Auto-generate from code where possible
```

---

## Quick Questions (Only 3)

When blueprint is detected, ask only these essential questions:

### Question 1: Processing Type
```
What type of data processing do you need?

Options:
1. Batch processing (scheduled runs, large volumes)
2. Stream processing (real-time, continuous)
3. Hybrid (batch + streaming - Lambda/Kappa architecture)

Your answer: _______________
```

**Why this matters:**
- Determines orchestration tool (Airflow vs Kafka/Flink)
- Affects architecture complexity
- Influences resource provisioning
- Changes monitoring requirements

**Default if skipped:** "Batch processing (Airflow-based)"

---

### Question 2: Data Volume
```
What is your expected data volume?

Options:
1. Small (<10 GB/day, <100K records/hour)
2. Medium (10-100 GB/day, 100K-1M records/hour)
3. Large (100+ GB/day, 1M+ records/hour)

Your answer: _______________
```

**Why this matters:**
- Small: Single-node processing (Pandas, DuckDB)
- Medium: Distributed processing optional (Spark on small cluster)
- Large: Distributed processing required (Spark, Flink)
- Affects infrastructure costs and complexity

**Default if skipped:** "Medium (10-100 GB/day)"

---

### Question 3: Primary Destination
```
Where will the processed data be stored?

Options:
1. Data warehouse (Snowflake, BigQuery, Redshift)
2. Data lake (S3/Parquet, Delta Lake, Iceberg)
3. OLTP database (PostgreSQL, MySQL)
4. Analytics platform (Elasticsearch, ClickHouse)

Your answer: _______________
```

**Why this matters:**
- Determines data format (Parquet, JSON, CSV)
- Affects partitioning strategy
- Influences schema design
- Changes optimization approaches

**Default if skipped:** "Data warehouse (Snowflake/BigQuery)"

---

## Blueprint Detection Logic

Trigger this blueprint when the user's goal matches:

```python
def should_use_data_pipeline_blueprint(goal: str) -> bool:
    goal_lower = goal.lower()

    # Primary keywords (high confidence)
    primary_match = any(keyword in goal_lower for keyword in [
        "data pipeline",
        "etl",
        "data ingestion",
        "data processing",
        "streaming",
        "batch processing"
    ])

    # Secondary keywords + data movement
    secondary_match = (
        any(keyword in goal_lower for keyword in [
            "kafka", "spark", "airflow", "flink", "beam"
        ]) and
        any(keyword in goal_lower for keyword in [
            "data", "pipeline", "processing", "streaming", "batch"
        ])
    )

    # Data integration pattern
    integration_match = (
        any(keyword in goal_lower for keyword in [
            "from", "to", "into", "load", "extract", "transform"
        ]) and
        any(keyword in goal_lower for keyword in [
            "warehouse", "database", "lake", "postgres", "s3", "snowflake"
        ])
    )

    return primary_match or secondary_match or integration_match
```

**Confidence levels:**
- **High (90%+):** Contains "data pipeline" or "ETL"
- **Medium (70-89%):** Contains data technology + processing term
- **Low (50-69%):** Contains data integration pattern

**Present blueprint when confidence >= 70%**

---

## Blueprint Offer Message

When blueprint is detected, present this message to the user:

```
┌────────────────────────────────────────────────────────────┐
│ 🔄 DATA PIPELINE BLUEPRINT DETECTED                        │
├────────────────────────────────────────────────────────────┤
│ Your goal matches our optimized Data Pipeline Blueprint!  │
│                                                            │
│ Pre-configured features:                                   │
│  ✓ Battle-tested architecture (batch/streaming/hybrid)    │
│  ✓ Data quality validation (Great Expectations)           │
│  ✓ Schema design (star schema for analytics)              │
│  ✓ Query optimization (indexes, partitions, views)        │
│  ✓ Comprehensive monitoring (metrics, logs, traces)       │
│  ✓ Error handling (retries, dead letter queue)            │
│  ✓ Production-ready (idempotency, exactly-once)           │
│                                                            │
│ Using blueprint reduces questions from 15 to 3!           │
│                                                            │
│ Options:                                                   │
│  1. Use blueprint (3 quick questions, ~10 min)            │
│  2. Custom configuration (15 questions, ~40 min)          │
│  3. Skip all questions (use all defaults, ~5 min)         │
│                                                            │
│ Your choice (1/2/3): _____                                │
└────────────────────────────────────────────────────────────┘
```

**Handle responses:**
- **1 or "blueprint"** → Ask only 3 blueprint questions
- **2 or "custom"** → Ask all skill questions (normal flow)
- **3 or "skip"** → Use all defaults, skip all questions

---

## Generated Output Structure

When blueprint is executed, generate this file structure:

```
data-pipeline-project/
├── pipeline/
│   ├── config/
│   │   ├── pipeline.yaml               # Main pipeline configuration
│   │   ├── connections.yaml            # Source/destination configs
│   │   ├── schema_definitions.yaml     # Data schemas and contracts
│   │   └── quality_expectations.yaml   # Data quality rules
│   │
│   ├── extract/
│   │   ├── sources/
│   │   │   ├── database_extractor.py   # SQL database extraction
│   │   │   ├── api_extractor.py        # REST API extraction
│   │   │   ├── file_extractor.py       # CSV/JSON/Parquet files
│   │   │   └── stream_consumer.py      # Kafka/Kinesis consumer
│   │   │
│   │   └── schemas/
│   │       ├── source_schema.py        # Source data models
│   │       └── validation.py           # Input validation
│   │
│   ├── transform/
│   │   ├── transformations/
│   │   │   ├── cleansing.py            # Data cleaning functions
│   │   │   ├── enrichment.py           # Data enrichment
│   │   │   ├── aggregations.py         # Aggregation logic
│   │   │   └── business_rules.py       # Business logic
│   │   │
│   │   ├── sql/
│   │   │   ├── staging_tables.sql      # Staging table DDL
│   │   │   ├── transformations.sql     # SQL transformations
│   │   │   └── materialized_views.sql  # Pre-computed views
│   │   │
│   │   └── schemas/
│   │       ├── intermediate_schema.py  # Intermediate models
│   │       └── target_schema.py        # Final output models
│   │
│   ├── load/
│   │   ├── sinks/
│   │   │   ├── warehouse_loader.py     # Data warehouse loading
│   │   │   ├── database_loader.py      # Database INSERT/UPDATE
│   │   │   ├── file_writer.py          # Parquet/CSV output
│   │   │   └── stream_producer.py      # Kafka/Kinesis producer
│   │   │
│   │   ├── strategies/
│   │   │   ├── full_refresh.py         # Truncate and load
│   │   │   ├── incremental.py          # Append new records
│   │   │   ├── upsert.py               # Merge/update logic
│   │   │   └── scd_type2.py            # Slowly changing dimensions
│   │   │
│   │   └── partitioning/
│   │       ├── time_partitions.py      # Date-based partitioning
│   │       └── hash_partitions.py      # Key-based partitioning
│   │
│   ├── quality/
│   │   ├── expectations/
│   │   │   ├── source_expectations.py  # Source data validation
│   │   │   ├── transform_expectations.py # Mid-pipeline checks
│   │   │   └── output_expectations.py  # Final validation
│   │   │
│   │   ├── validators/
│   │   │   ├── schema_validator.py     # Schema compliance
│   │   │   ├── completeness_validator.py # Null checks
│   │   │   ├── uniqueness_validator.py # Duplicate detection
│   │   │   └── freshness_validator.py  # Timeliness checks
│   │   │
│   │   └── reports/
│   │       ├── quality_report.py       # Generate reports
│   │       └── data_profiling.py       # Data profiling
│   │
│   ├── orchestration/
│   │   ├── airflow/
│   │   │   ├── dags/
│   │   │   │   ├── batch_pipeline.py   # Batch DAG definition
│   │   │   │   └── monitoring_dag.py   # Health check DAG
│   │   │   │
│   │   │   ├── operators/
│   │   │   │   ├── custom_operators.py # Custom Airflow operators
│   │   │   │   └── sensors.py          # Custom sensors
│   │   │   │
│   │   │   └── plugins/
│   │   │       └── pipeline_plugin.py  # Airflow plugins
│   │   │
│   │   └── streaming/
│   │       ├── kafka_streams.py        # Kafka Streams app
│   │       ├── flink_job.py            # Flink job definition
│   │       └── consumer_groups.py      # Consumer group config
│   │
│   ├── monitoring/
│   │   ├── metrics/
│   │   │   ├── pipeline_metrics.py     # Custom metrics
│   │   │   ├── prometheus_exporter.py  # Prometheus exporter
│   │   │   └── metric_definitions.yaml # Metric catalog
│   │   │
│   │   ├── logging/
│   │   │   ├── logger.py               # Structured logging
│   │   │   ├── log_config.yaml         # Logging configuration
│   │   │   └── correlation.py          # Trace correlation
│   │   │
│   │   ├── alerts/
│   │   │   ├── alert_rules.yaml        # Alert definitions
│   │   │   ├── pagerduty_config.yaml   # PagerDuty integration
│   │   │   └── slack_notifier.py       # Slack notifications
│   │   │
│   │   └── dashboards/
│   │       ├── grafana/
│   │       │   ├── pipeline_dashboard.json # Main dashboard
│   │       │   └── quality_dashboard.json  # Data quality
│   │       │
│   │       └── templates/
│   │           └── dashboard_template.py   # Dashboard as code
│   │
│   ├── utils/
│   │   ├── connection_pool.py          # Database connection pooling
│   │   ├── retry_logic.py              # Retry/backoff strategies
│   │   ├── error_handling.py           # Error handlers
│   │   ├── deduplication.py            # Dedup utilities
│   │   └── watermarking.py             # Event-time watermarks
│   │
│   └── tests/
│       ├── unit/
│       │   ├── test_transformations.py # Transformation tests
│       │   ├── test_validators.py      # Validation tests
│       │   └── test_utils.py           # Utility tests
│       │
│       ├── integration/
│       │   ├── test_extract.py         # Extraction tests
│       │   ├── test_load.py            # Loading tests
│       │   └── test_end_to_end.py      # Full pipeline tests
│       │
│       └── fixtures/
│           ├── sample_data.json        # Test data
│           └── expected_outputs.json   # Expected results
│
├── infrastructure/
│   ├── terraform/
│   │   ├── main.tf                     # Infrastructure as code
│   │   ├── variables.tf                # Configuration variables
│   │   ├── outputs.tf                  # Output values
│   │   └── modules/
│   │       ├── kafka_cluster/          # Kafka infrastructure
│   │       ├── database/               # Database setup
│   │       └── monitoring/             # Monitoring stack
│   │
│   ├── docker/
│   │   ├── Dockerfile                  # Pipeline container
│   │   ├── docker-compose.yml          # Local development stack
│   │   └── airflow.Dockerfile          # Airflow container
│   │
│   └── kubernetes/
│       ├── deployment.yaml             # K8s deployment
│       ├── service.yaml                # Service definition
│       └── configmap.yaml              # Configuration
│
├── docs/
│   ├── architecture/
│   │   ├── data_flow_diagram.md        # Data flow visualization
│   │   ├── component_diagram.md        # Component architecture
│   │   └── technology_stack.md         # Tech stack details
│   │
│   ├── runbooks/
│   │   ├── deployment.md               # Deployment procedures
│   │   ├── rollback.md                 # Rollback guide
│   │   ├── troubleshooting.md          # Common issues
│   │   └── disaster_recovery.md        # DR procedures
│   │
│   ├── data_catalog/
│   │   ├── data_dictionary.md          # Table/column docs
│   │   ├── lineage.md                  # Data lineage
│   │   └── sample_queries.md           # Example queries
│   │
│   └── sla/
│       ├── service_levels.md           # SLA definitions
│       └── error_budgets.md            # Error budget tracking
│
├── scripts/
│   ├── setup_database.sh               # Database initialization
│   ├── backfill_data.py                # Historical data backfill
│   ├── validate_pipeline.py            # Pipeline validation
│   └── generate_sample_data.py         # Test data generation
│
├── requirements.txt                    # Python dependencies
├── setup.py                            # Package setup
├── pyproject.toml                      # Poetry/modern setup
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore rules
├── Makefile                            # Common commands
└── README.md                           # Project overview
```

---

## Pipeline Architecture Patterns

### Batch Processing Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   BATCH PIPELINE (AIRFLOW)                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌─────────┐ │
│  │ Extract  │──→│Transform │──→│  Load    │──→│Validate │ │
│  └──────────┘   └──────────┘   └──────────┘   └─────────┘ │
│       │              │              │              │        │
│  [Source DB]    [Staging]    [Data Warehouse]  [Quality]   │
│       │              │              │              │        │
│  ┌────▼──────────────▼──────────────▼──────────────▼─────┐ │
│  │         Airflow DAG (Scheduled Execution)             │ │
│  │  - Extract: 02:00 UTC daily                           │ │
│  │  - Transform: On extract success                      │ │
│  │  - Load: On transform success                         │ │
│  │  - Validate: On load success                          │ │
│  │  - Retry: 3 attempts with exponential backoff         │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              MONITORING & ALERTING                    │ │
│  │  - Metrics: Prometheus (records/sec, errors)          │ │
│  │  - Logs: Structured JSON to CloudWatch/ELK           │ │
│  │  - Alerts: PagerDuty (failures), Slack (warnings)     │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Streaming Architecture (Kappa)

```
┌─────────────────────────────────────────────────────────────┐
│               STREAMING PIPELINE (KAFKA + FLINK)            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐                                          │
│  │   Producers  │ (APIs, DBs, Apps)                        │
│  └──────┬───────┘                                          │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              KAFKA TOPIC (raw-events)               │   │
│  │  - Partitions: 10 (for parallelism)                │   │
│  │  - Replication: 3 (for durability)                 │   │
│  │  - Retention: 7 days                                │   │
│  └────────┬────────────────────────────────────────────┘   │
│           │                                                 │
│           ▼                                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │         FLINK STREAM PROCESSING                    │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐        │    │
│  │  │ Validate │─→│Transform │─→│Aggregate │        │    │
│  │  └──────────┘  └──────────┘  └──────────┘        │    │
│  │  - Window: 5-second tumbling                      │    │
│  │  - Watermark: 1-hour allowed lateness             │    │
│  │  - State: RocksDB backend                         │    │
│  │  - Checkpoints: Every 60 seconds                  │    │
│  └────────┬────────────────────────────────────────┬──┘    │
│           │                                         │       │
│           ▼                                         ▼       │
│  ┌────────────────┐                    ┌──────────────────┐│
│  │ KAFKA TOPIC    │                    │ DEAD LETTER      ││
│  │ (processed)    │                    │ QUEUE (errors)   ││
│  └────────┬───────┘                    └──────────────────┘│
│           │                                                 │
│           ▼                                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │          SINK CONNECTORS                           │    │
│  │  - Snowflake Connector (analytics)                 │    │
│  │  - S3 Sink (data lake)                             │    │
│  │  - Elasticsearch (search)                          │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │         MONITORING (REAL-TIME)                        │ │
│  │  - Consumer lag: <5 minutes                           │ │
│  │  - Throughput: Records/sec per partition             │ │
│  │  - Error rate: Failed messages/total                 │ │
│  │  - Latency: End-to-end processing time               │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Hybrid Architecture (Lambda)

```
┌─────────────────────────────────────────────────────────────┐
│         HYBRID PIPELINE (LAMBDA ARCHITECTURE)               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                     ┌──────────────┐                        │
│                     │ Data Sources │                        │
│                     └───────┬──────┘                        │
│                             │                               │
│              ┌──────────────┴──────────────┐                │
│              │                             │                │
│              ▼                             ▼                │
│  ┌─────────────────────┐      ┌─────────────────────────┐  │
│  │   BATCH LAYER       │      │   SPEED LAYER           │  │
│  │   (Spark)           │      │   (Flink/Kafka Streams) │  │
│  │                     │      │                         │  │
│  │  - Full history     │      │  - Recent data only     │  │
│  │  - High latency     │      │  - Low latency          │  │
│  │  - High accuracy    │      │  - Approximate results  │  │
│  │  - Runs: Daily      │      │  - Runs: Continuous     │  │
│  │  - Recomputes all   │      │  - Incremental updates  │  │
│  └──────────┬──────────┘      └──────────┬──────────────┘  │
│             │                            │                  │
│             └─────────┬──────────────────┘                  │
│                       │                                     │
│                       ▼                                     │
│            ┌────────────────────┐                           │
│            │   SERVING LAYER    │                           │
│            │   (Data Warehouse) │                           │
│            │                    │                           │
│            │  - Batch Views     │                           │
│            │  - Real-time Views │                           │
│            │  - Merged queries  │                           │
│            └────────────────────┘                           │
│                                                             │
│  Use case: Financial reporting with real-time dashboard    │
│  - Batch: Official daily reports (accurate)                │
│  - Speed: Live dashboard updates (approximate)             │
│  - Serving: Query merges both views                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Quality Framework

### Validation Checkpoints

```yaml
checkpoint_1_source_validation:
  location: "After extraction, before transformation"
  rules:
    - schema_compliance:
        description: "Validate column names, types, nullability"
        severity: "critical"
        action: "fail_pipeline"

    - row_count:
        description: "Expected range: 1000-100000 records"
        severity: "warning"
        action: "alert_only"

    - freshness:
        description: "Data must be <24 hours old"
        severity: "critical"
        action: "fail_pipeline"

checkpoint_2_transformation_validation:
  location: "After transformations, before loading"
  rules:
    - completeness:
        description: "Required columns must be non-null"
        columns: ["user_id", "timestamp", "event_type"]
        severity: "critical"
        action: "fail_pipeline"

    - uniqueness:
        description: "Primary key must be unique"
        columns: ["transaction_id"]
        severity: "critical"
        action: "fail_pipeline"

    - value_ranges:
        description: "Amount must be between 0 and 1000000"
        column: "amount"
        min: 0
        max: 1000000
        severity: "warning"
        action: "log_violations"

checkpoint_3_output_validation:
  location: "After loading to destination"
  rules:
    - referential_integrity:
        description: "Foreign keys must exist in dimension tables"
        severity: "critical"
        action: "fail_pipeline"

    - reconciliation:
        description: "Row count matches between source and destination"
        tolerance: "0.01%"  # Allow 0.01% discrepancy
        severity: "critical"
        action: "fail_pipeline"

    - business_rules:
        description: "Total revenue must be positive"
        custom_sql: "SELECT SUM(revenue) > 0 FROM fact_sales"
        severity: "warning"
        action: "alert_only"
```

---

## Error Handling Strategies

### Retry Configuration

```yaml
retry_policies:
  transient_errors:
    description: "Network timeouts, temporary unavailability"
    max_attempts: 3
    backoff_strategy: "exponential"
    initial_delay: "5s"
    max_delay: "60s"
    multiplier: 2
    jitter: true

  data_quality_failures:
    description: "Validation failures, schema violations"
    max_attempts: 1
    action: "send_to_dead_letter_queue"
    alert: "pagerduty"

  resource_exhaustion:
    description: "Out of memory, connection pool exhausted"
    max_attempts: 2
    backoff_strategy: "fixed"
    delay: "30s"
    action: "reduce_batch_size_and_retry"

dead_letter_queue:
  enabled: true
  retention: "30 days"
  processing:
    - manual_review: "Data quality team"
    - automated_retry: "After source data fix"
    - discard: "After 30 days"
```

---

## Performance Optimization

### Batch Processing Optimizations

```yaml
optimizations:
  parallelization:
    - partition_data: "Process data in parallel chunks"
    - chunk_size: "10000 records"
    - max_workers: "CPU count * 2"

  incremental_loading:
    - strategy: "Change Data Capture (CDC)"
    - watermark_column: "updated_at"
    - checkpoint: "Store last processed timestamp"
    - fallback: "Full refresh if checkpoint missing"

  compression:
    - format: "Parquet with Snappy compression"
    - compression_ratio: "~10:1 for typical data"
    - benefits: "Reduced I/O, faster queries"

  caching:
    - dimension_tables: "Cache in memory (small tables)"
    - lookup_tables: "Redis cache for frequent lookups"
    - ttl: "1 hour"
```

### Streaming Optimizations

```yaml
optimizations:
  batching:
    - micro_batch_size: "1000 records or 5 seconds"
    - benefits: "Higher throughput, lower overhead"

  state_management:
    - backend: "RocksDB (persistent, fast)"
    - checkpointing: "Every 60 seconds"
    - state_ttl: "7 days for inactive keys"

  partitioning:
    - strategy: "Hash partitioning on user_id"
    - partition_count: "10 (matches Kafka partitions)"
    - benefits: "Parallel processing, even distribution"

  backpressure:
    - detection: "Monitor consumer lag"
    - action: "Scale consumers horizontally"
    - threshold: "Lag > 5 minutes"
```

---

## Dependencies

The blueprint includes these Python packages:

```toml
[tool.poetry.dependencies]
python = "^3.10"

# Core data processing
pandas = "^2.1.0"                  # Data manipulation
polars = "^0.19.0"                 # Fast DataFrame library (alternative to pandas)
duckdb = "^0.9.0"                  # In-process SQL OLAP database

# Distributed processing (optional - based on volume)
pyspark = "^3.5.0"                 # Batch processing (medium/large data)
apache-flink = "^1.18.0"           # Stream processing

# Orchestration
apache-airflow = "^2.7.0"          # Batch orchestration
apache-airflow-providers-postgres = "^5.7.0"
apache-airflow-providers-snowflake = "^5.1.0"

# Streaming
kafka-python = "^2.0.2"            # Kafka client
confluent-kafka = "^2.3.0"         # Confluent Kafka (better performance)
fastavro = "^1.9.0"                # Avro serialization

# Data quality
great-expectations = "^0.18.0"     # Data validation
pydantic = "^2.5.0"                # Data models and validation

# Database connectors
psycopg2-binary = "^2.9.0"         # PostgreSQL
pymysql = "^1.1.0"                 # MySQL
snowflake-connector-python = "^3.4.0"  # Snowflake
google-cloud-bigquery = "^3.13.0"  # BigQuery

# Storage
boto3 = "^1.29.0"                  # AWS S3
pyarrow = "^14.0.0"                # Parquet files

# Monitoring
prometheus-client = "^0.19.0"      # Metrics
opentelemetry-api = "^1.21.0"      # Distributed tracing
structlog = "^23.2.0"              # Structured logging

# Utilities
tenacity = "^8.2.0"                # Retry logic
python-dotenv = "^1.0.0"           # Environment variables
pyyaml = "^6.0.0"                  # YAML parsing
```

**Infrastructure dependencies:**
- Airflow: Orchestration for batch pipelines
- Kafka: Event streaming platform
- PostgreSQL: Metadata storage
- Redis: Caching and state management
- Prometheus + Grafana: Monitoring
- Docker + Kubernetes: Containerization

---

## Monitoring Dashboards

### Pipeline Health Dashboard

```yaml
dashboard: "Pipeline Health"
panels:
  - title: "Pipeline Status"
    type: "stat"
    metrics:
      - current_status: "Success | Failed | Running"
      - last_run_time: "2024-12-06 02:00 UTC"
      - next_scheduled_run: "2024-12-07 02:00 UTC"

  - title: "Processing Rate"
    type: "graph"
    metrics:
      - records_per_second: "Gauge"
      - total_records_processed: "Counter"
      - processing_duration: "Histogram"

  - title: "Error Rate"
    type: "graph"
    metrics:
      - errors_per_minute: "Rate of failed records"
      - error_percentage: "Errors / total records"
    thresholds:
      - warning: ">0.5%"
      - critical: ">1.0%"

  - title: "Data Quality"
    type: "table"
    metrics:
      - validation_pass_rate: "Percentage"
      - schema_violations: "Count"
      - null_rate_by_column: "Percentage per column"

  - title: "Resource Utilization"
    type: "graph"
    metrics:
      - cpu_usage: "Percentage"
      - memory_usage: "Percentage"
      - disk_io: "MB/s"

  - title: "Latency"
    type: "graph"
    metrics:
      - p50_latency: "Median processing time"
      - p95_latency: "95th percentile"
      - p99_latency: "99th percentile"
```

### Data Quality Dashboard

```yaml
dashboard: "Data Quality Scorecard"
panels:
  - title: "Overall Quality Score"
    type: "gauge"
    calculation: "Weighted average of all quality checks"
    thresholds:
      - excellent: ">99%"
      - good: "95-99%"
      - needs_attention: "<95%"

  - title: "Completeness"
    type: "stat"
    metrics:
      - null_rate: "Percentage of null values"
      - missing_records: "Expected vs actual row count"

  - title: "Uniqueness"
    type: "stat"
    metrics:
      - duplicate_rate: "Percentage of duplicate records"
      - primary_key_violations: "Count"

  - title: "Freshness"
    type: "stat"
    metrics:
      - data_age: "Time since last update"
      - sla_compliance: "Within freshness SLA"

  - title: "Validity"
    type: "table"
    metrics:
      - schema_compliance: "Matches expected schema"
      - value_range_violations: "Values outside expected ranges"
      - format_violations: "Invalid formats (email, phone, etc.)"

  - title: "Quality Trends"
    type: "graph"
    metrics:
      - quality_score_over_time: "7-day trend"
      - issues_by_category: "Stacked bar chart"
```

---

## Security Considerations

```yaml
security:
  secrets_management:
    - tool: "AWS Secrets Manager / HashiCorp Vault"
    - never_commit: "Database passwords, API keys, credentials"
    - rotation: "Automatic rotation every 90 days"

  data_encryption:
    - at_rest: "AES-256 encryption for S3, databases"
    - in_transit: "TLS 1.2+ for all connections"
    - column_level: "Encrypt PII columns (SSN, credit card)"

  access_control:
    - principle: "Least privilege"
    - authentication: "IAM roles, service accounts"
    - authorization: "RBAC for pipeline resources"

  data_masking:
    - pii_detection: "Automatic detection of PII fields"
    - masking_strategy: "Hash, tokenize, or redact"
    - environments: "Mask in dev/test, plain in prod"

  audit_logging:
    - log_all_access: "Who accessed what data when"
    - retention: "3 years for compliance"
    - tamper_proof: "Write-once storage"
```

---

## Disaster Recovery

```yaml
disaster_recovery:
  backup_strategy:
    - frequency: "Daily full backup, hourly incremental"
    - retention: "30 days daily, 12 months monthly"
    - storage: "Geo-replicated S3 buckets"
    - testing: "Monthly restore tests"

  recovery_time_objective:
    - critical_pipelines: "RTO: 1 hour"
    - standard_pipelines: "RTO: 4 hours"
    - batch_reports: "RTO: 24 hours"

  recovery_point_objective:
    - streaming: "RPO: 5 minutes (last checkpoint)"
    - batch: "RPO: 24 hours (last successful run)"

  failover_procedures:
    - automated: "Health checks trigger automatic failover"
    - manual: "Runbook for manual intervention"
    - testing: "Quarterly disaster recovery drills"
```

---

## Customization Points

After blueprint generation, users can easily customize:

1. **Data sources:** Add extractors in `pipeline/extract/sources/`
2. **Transformations:** Modify business logic in `pipeline/transform/transformations/`
3. **Data quality rules:** Update `pipeline/config/quality_expectations.yaml`
4. **Orchestration schedule:** Edit Airflow DAG schedule in `pipeline/orchestration/airflow/dags/`
5. **Monitoring alerts:** Adjust thresholds in `pipeline/monitoring/alerts/alert_rules.yaml`
6. **Partitioning strategy:** Change in `pipeline/load/partitioning/`

---

## Migration Path

If user starts with blueprint but needs additional features later:

1. **Add CDC:** Run `/skillchain change-data-capture`
2. **Add machine learning:** Run `/skillchain building-ml-models`
3. **Add real-time analytics:** Run `/skillchain real-time-analytics`
4. **Add data governance:** Run `/skillchain data-governance`

All additions will integrate with existing pipeline structure.

---

## Version History

**1.0.0** (2025-12-06)
- Initial data pipeline blueprint
- 6-skill chain with production-ready defaults
- 3-question quick configuration
- Batch, streaming, and hybrid architectures
- Comprehensive data quality framework
- Full observability stack
- Security and disaster recovery

---

## Related Blueprints

- **Dashboard Blueprint:** For visualizing pipeline metrics
- **Database Blueprint:** For schema design and optimization
- **API Blueprint:** For building data APIs on top of warehouse
- **ML Pipeline Blueprint:** For machine learning workflows

---

**Blueprint Complete**
