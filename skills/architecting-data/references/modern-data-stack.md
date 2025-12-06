# Modern Data Stack Architecture


## Table of Contents

- [Standard Architecture Layers (2025)](#standard-architecture-layers-2025)
- [Layer Selection Criteria](#layer-selection-criteria)
  - [Ingestion](#ingestion)
  - [Storage](#storage)
  - [Transformation](#transformation)
  - [Orchestration](#orchestration)
- [Typical Workflow](#typical-workflow)
- [Tool Stack Evolution](#tool-stack-evolution)

## Standard Architecture Layers (2025)

```
┌─────────────────────────────────────────┐
│ Data Sources                            │
│ - Databases (PostgreSQL, MySQL, MongoDB)│
│ - SaaS (Salesforce, Stripe, HubSpot)   │
│ - Events (Segment, Rudderstack)         │
│ - Files (S3, GCS, SFTP)                 │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Ingestion Layer                         │
│ - Fivetran (ELT, pre-built connectors)  │
│ - Airbyte (open-source, custom)        │
│ - Kafka (streaming, event-driven)       │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Storage Layer                           │
│ - Snowflake (cloud data warehouse)      │
│ - Databricks (lakehouse, Spark)         │
│ - BigQuery (Google Cloud, serverless)   │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Transformation Layer                    │
│ - dbt (SQL-based, version controlled)   │
│ - Dataform (Google, SQL + Dataform)    │
│ - Spark (PySpark, large-scale)          │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Orchestration Layer                     │
│ - Airflow (Python DAGs, most popular)   │
│ - Dagster (asset-based, modern)         │
│ - Prefect (Python, dynamic workflows)   │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Visualization/BI Layer                  │
│ - Tableau (enterprise visualizations)   │
│ - Looker (Google, LookML modeling)      │
│ - Power BI (Microsoft ecosystem)        │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Governance Layer (Cross-Cutting)        │
│ - DataHub (catalog, open-source)        │
│ - Great Expectations (data quality)     │
│ - OpenLineage (lineage tracking)        │
└─────────────────────────────────────────┘
```

## Layer Selection Criteria

### Ingestion

**Fivetran:**
- ✅ Pre-built connectors (300+)
- ✅ SaaS, low maintenance
- ❌ Expensive ($1K-10K+/month)

**Airbyte:**
- ✅ Open-source, free
- ✅ Custom connectors
- ❌ More maintenance

**Kafka:**
- ✅ Real-time streaming
- ✅ High throughput
- ❌ Complex setup

### Storage

**Snowflake:**
- Best for: BI/analytics
- Strength: Zero-maintenance, strong governance
- Cost: $$$

**Databricks:**
- Best for: ML/data science
- Strength: Unified analytics (BI + ML)
- Cost: $$

**BigQuery:**
- Best for: Google Cloud users
- Strength: Serverless, pay-per-query
- Cost: $$

### Transformation

**dbt:**
- SQL-based, analysts can write
- Version control, testing
- Cost: Free (open-source)

**Spark:**
- PySpark/Scala, data engineers
- Large-scale processing
- Cost: Compute-based

### Orchestration

**Airflow:**
- Most mature (2014)
- Large community
- Complexity: High

**Dagster:**
- Asset-based (modern)
- Strong testing
- Complexity: Medium

**Prefect:**
- Simpler than Airflow
- Dynamic workflows
- Complexity: Low-Medium

## Typical Workflow

**Batch ELT Pipeline:**
```
PostgreSQL → Fivetran → Snowflake → dbt → Tableau
             (Extract/Load)  (Transform)  (Visualize)
```

**Streaming Pipeline:**
```
App Events → Kafka → Flink → Iceberg → Trino → Dashboard
            (Stream)  (Process) (Store)  (Query)
```

**Hybrid Pipeline:**
```
Batch Sources → Fivetran → Lakehouse
                             ↓
Streaming Sources → Kafka → Lakehouse
                             ↓
                           dbt (Transform)
                             ↓
                           BI Tools
```

## Tool Stack Evolution

**Phase 1 (Startup):**
- BigQuery + Airbyte + dbt + Metabase
- Cost: <$1K/month
- Team: 1-2 analysts

**Phase 2 (Growth):**
- Snowflake + Fivetran + dbt + Tableau + DataHub
- Cost: $10K-50K/month
- Team: 2-5 data engineers, 5-10 analysts

**Phase 3 (Enterprise):**
- Snowflake + Databricks + Fivetran + Kafka + dbt + Airflow + Tableau + Alation
- Cost: $50K-500K/month
- Team: 10+ data engineers, 20+ analysts

See [tool-recommendations.md](tool-recommendations.md) for detailed comparisons.
