---
sidebar_position: 1
title: Data Architecture
description: Design modern data platforms with storage paradigms, modeling approaches, and governance frameworks
tags: [data-engineering, data-architecture, data-lake, data-warehouse, lakehouse, medallion, data-mesh]
---

# Data Architecture

Strategic guidance for designing modern data platforms, covering storage paradigms (data lake, warehouse, lakehouse), modeling approaches (dimensional, normalized, data vault, wide tables), data mesh principles, and medallion architecture patterns.

## When to Use

Use when:
- Designing a new data platform or modernizing legacy systems
- Choosing between data lake, data warehouse, or data lakehouse
- Deciding on data modeling approaches (dimensional, normalized, data vault, wide tables)
- Evaluating centralized vs data mesh architecture
- Selecting open table formats (Apache Iceberg, Delta Lake, Apache Hudi)
- Designing medallion architecture (bronze, silver, gold layers)
- Implementing data governance and cataloging

## Key Features

### Storage Paradigms

Three primary patterns for analytical data storage:

- **Data Lake**: Centralized repository for raw data at scale (schema-on-read, cost-optimized)
- **Data Warehouse**: Structured repository optimized for BI (schema-on-write, ACID, fast queries)
- **Data Lakehouse**: Hybrid combining lake flexibility with warehouse reliability (60-80% cost savings)

**Decision Framework**:
- BI/Reporting only + Known queries → Data Warehouse
- ML/AI primary + Raw data needed → Data Lake or Lakehouse
- Mixed BI + ML + Cost optimization → Data Lakehouse (recommended)

### Data Modeling Approaches

- **Dimensional (Kimball)**: Star/snowflake schemas for BI dashboards
- **Normalized (3NF)**: Eliminate redundancy for transactional systems
- **Data Vault 2.0**: Flexible model with complete audit trail for compliance
- **Wide Tables**: Denormalized, optimized for columnar storage and ML

### Medallion Architecture

Standard lakehouse pattern: Bronze (raw) → Silver (cleaned) → Gold (business-level)

- **Bronze Layer**: Exact copy of source data, immutable, append-only
- **Silver Layer**: Validated, deduplicated, typed data
- **Gold Layer**: Business logic, aggregates, dimensional models, ML features

## Quick Start

### Apache Iceberg Table (Recommended)

```sql
-- Create lakehouse table with ACID guarantees
CREATE TABLE catalog.db.sales (
  order_id BIGINT,
  amount DECIMAL(10,2),
  order_date DATE
)
USING iceberg
PARTITIONED BY (days(order_date));

-- Time travel queries
SELECT * FROM catalog.db.sales
TIMESTAMP AS OF '2025-01-01';
```

### dbt Transformation (Gold Layer)

```sql
-- models/marts/fct_sales.sql
WITH source AS (
  SELECT * FROM {{ source('silver', 'sales') }}
),
cleaned AS (
  SELECT
    order_id,
    customer_id,
    UPPER(customer_name) AS customer_name,
    amount
  FROM source
  WHERE order_id IS NOT NULL
)
SELECT * FROM cleaned
```

### Data Mesh Readiness Assessment

Score these 6 factors (1-5 each):
1. Domain clarity
2. Team maturity
3. Platform capability
4. Governance maturity
5. Scale need
6. Organizational buy-in

**Scoring**: 24-30: Strong candidate | 18-23: Hybrid | 12-17: Build foundation first | 6-11: Centralized

## Tool Recommendations (2025)

**Research-Validated (Context7)**:

- **dbt**: Score 87.0, 3,532+ code snippets - SQL-based transformations, industry standard
- **Apache Iceberg**: Score 79.7, 832+ code snippets - Open table format, vendor-neutral

**By Organization Size**:

- **Startup (&lt;50)**: BigQuery + Airbyte + dbt + Metabase (&lt;$1K/month)
- **Growth (50-500)**: Snowflake + Fivetran + dbt + Airflow + Tableau ($10K-50K/month)
- **Enterprise (&gt;500)**: Snowflake + Databricks + Fivetran + Kafka + dbt + Airflow + Alation ($50K-500K/month)

## Decision Frameworks

### Storage Paradigm Selection

**Step 1: Identify Primary Use Case**
- BI/Reporting only → Data Warehouse
- ML/AI primary → Data Lake or Lakehouse
- Mixed BI + ML → Data Lakehouse
- Exploratory → Data Lake

**Step 2: Evaluate Budget**
- High budget, known queries → Data Warehouse
- Cost-sensitive, flexible → Data Lakehouse

### Open Table Format Selection

- Multi-engine flexibility → **Apache Iceberg** (recommended)
- Databricks ecosystem → Delta Lake
- Frequent upserts/CDC → Apache Hudi

## Best Practices

1. **Start simple**: Avoid over-engineering; begin with warehouse or basic lakehouse
2. **Invest in governance early**: Catalog, lineage, quality from day one
3. **Medallion architecture**: Use bronze-silver-gold for clear quality layers
4. **Open table formats**: Prefer Iceberg or Delta Lake to avoid vendor lock-in
5. **Assess mesh readiness**: Don't decentralize prematurely (&lt;500 people)
6. **Automate quality**: Integrate tests (Great Expectations, dbt) into CI/CD
7. **Document as code**: Use dbt docs, DataHub, YAML for self-service

## Related Skills

- [Streaming Data](./streaming-data) - Real-time data pipelines with Kafka, Flink
- [Data Transformation](./transforming-data) - dbt and Spark transformations
- [SQL Optimization](./optimizing-sql) - Query performance tuning

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/architecting-data)
- [Apache Iceberg Documentation](https://iceberg.apache.org/)
- [dbt Documentation](https://docs.getdbt.com/)
- [Databricks Medallion Architecture](https://www.databricks.com/glossary/medallion-architecture)
