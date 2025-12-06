---
sidebar_position: 3
title: Data Transformation
description: Transform raw data using ETL/ELT patterns, dbt, pandas/polars, and orchestration
tags: [data-engineering, dbt, etl, elt, pandas, polars, pyspark, airflow]
---

# Data Transformation

Transform raw data into analytical assets using modern transformation patterns, frameworks (dbt, polars, PySpark), and orchestration tools (Airflow, Dagster, Prefect).

## When to Use

Use when:
- Choosing between ETL and ELT transformation patterns
- Building dbt models (staging, intermediate, marts)
- Implementing incremental data loads and merge strategies
- Migrating pandas code to polars for performance improvements
- Orchestrating data pipelines with dependencies and retries
- Adding data quality tests and validation
- Processing large datasets with PySpark
- Creating production-ready transformation workflows

## Key Features

### ETL vs ELT Decision Framework

**Use ELT (Extract, Load, Transform)** when:
- Using modern cloud data warehouse (Snowflake, BigQuery, Databricks)
- Transformation logic changes frequently
- Team includes SQL analysts
- Data volume 10GB-1TB+ (leverage warehouse parallelism)

**Tools**: dbt, Dataform, Snowflake tasks, BigQuery scheduled queries

**Use ETL (Extract, Transform, Load)** when:
- Regulatory compliance requires pre-load data redaction (PII/PHI)
- Target system lacks compute power
- Real-time streaming with immediate transformation
- Legacy systems without cloud warehouse

**Default recommendation**: ELT with dbt

### DataFrame Library Selection

- **pandas**: Data size < 500MB, prototyping, pandas-only library compatibility
- **polars**: 500MB-100GB, performance critical (10-100x faster), production pipelines
- **PySpark**: >100GB, distributed processing across cluster, existing Spark infrastructure

**Migration path**: pandas → polars (easier, similar API)

## Quick Start

### dbt Incremental Model

```sql
{{
  config(
    materialized='incremental',
    unique_key='order_id'
  )
}}

select
  order_id,
  customer_id,
  order_created_at,
  sum(revenue) as total_revenue
from {{ ref('int_order_items_joined') }}
group by 1, 2, 3

{% if is_incremental() %}
    where order_created_at > (select max(order_created_at) from {{ this }})
{% endif %}
```

### polars High-Performance Transformation

```python
import polars as pl

result = (
    pl.scan_csv('large_dataset.csv')  # Lazy evaluation
    .filter(pl.col('year') == 2024)
    .with_columns([
        (pl.col('quantity') * pl.col('price')).alias('revenue')
    ])
    .group_by('region')
    .agg(pl.col('revenue').sum())
    .collect()  # Execute lazy query
)
```

**Key benefits**: 10-100x faster than pandas, multi-threaded, lazy evaluation

### Airflow Data Pipeline

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG(
    dag_id='daily_sales_pipeline',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    default_args={
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    },
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:
    extract = PythonOperator(task_id='extract', python_callable=extract_data)
    transform = PythonOperator(task_id='transform', python_callable=transform_data)
    extract >> transform  # Define dependency
```

## dbt Model Layer Structure

1. **Staging Layer** (`models/staging/`)
   - 1:1 with source tables
   - Minimal transformations (renaming, type casting, basic filtering)
   - Materialized as views or ephemeral

2. **Intermediate Layer** (`models/intermediate/`)
   - Business logic and complex joins
   - Not exposed to end users
   - Often ephemeral (CTEs only)

3. **Marts Layer** (`models/marts/`)
   - Final models for reporting
   - Fact tables (events, transactions)
   - Dimension tables (customers, products)
   - Materialized as tables or incremental

### dbt Materialization Types

- **View**: Query re-run each time (fast queries, staging layer)
- **Table**: Full refresh on each run (frequently queried, expensive computations)
- **Incremental**: Only processes new/changed records (large fact tables, event logs)
- **Ephemeral**: CTE only, not persisted (intermediate calculations)

### dbt Testing

```yaml
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - relationships:
              to: ref('dim_customers')
              field: customer_id
      - name: total_revenue
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
```

## DataFrame Comparison

### pandas to polars Migration

```python
# pandas
import pandas as pd
df = pd.read_csv('sales.csv')
result = (
    df.query('year == 2024')
    .assign(revenue=lambda x: x['quantity'] * x['price'])
    .groupby('region')
    .agg({'revenue': ['sum', 'mean']})
)

# polars (10-100x faster)
import polars as pl
result = (
    pl.scan_csv('sales.csv')  # Lazy
    .filter(pl.col('year') == 2024)
    .with_columns([
        (pl.col('quantity') * pl.col('price')).alias('revenue')
    ])
    .group_by('region')
    .agg([
        pl.col('revenue').sum().alias('revenue_sum'),
        pl.col('revenue').mean().alias('revenue_mean')
    ])
    .collect()  # Execute
)
```

**Key differences**:
- polars uses `scan_csv()` (lazy) vs pandas `read_csv()` (eager)
- polars uses `with_columns()` vs pandas `assign()`
- polars uses `pl.col()` expressions vs pandas string references
- polars requires `collect()` to execute lazy queries

## Orchestration Tool Selection

**Choose Airflow** when:
- Enterprise production (proven at scale)
- Need 5,000+ integrations
- Managed services available (AWS MWAA, GCP Cloud Composer)

**Choose Dagster** when:
- Heavy dbt usage (native `dbt_assets` integration)
- Data lineage and asset-based workflows prioritized
- ML pipelines requiring testability

**Choose Prefect** when:
- Dynamic workflows (runtime task generation)
- Cloud-native architecture preferred
- Pythonic API with decorators

## Production Best Practices

### Idempotency

Ensure transformations produce same result when run multiple times:
- Use `merge` statements in incremental models
- Implement deduplication logic
- Use `unique_key` in dbt incremental models

### Error Handling

```python
try:
    result = perform_transformation()
    validate_result(result)
except ValidationError as e:
    log_error(e)
    raise
```

### Monitoring

- Set up Airflow email/Slack alerts on task failure
- Monitor dbt test failures
- Track data freshness (SLAs)
- Log row counts and data quality metrics

## Tool Recommendations

**SQL Transformations**: dbt Core (industry standard, multi-warehouse)
```bash
pip install dbt-core dbt-snowflake
```

**Python DataFrames**: polars (10-100x faster than pandas)
```bash
pip install polars
```

**Orchestration**: Apache Airflow (battle-tested, 5,000+ integrations)
```bash
pip install apache-airflow
```

## Related Skills

- [Data Architecture](./architecting-data) - Data platform design and medallion architecture
- [Streaming Data](./streaming-data) - Real-time transformations with Flink and Spark
- [SQL Optimization](./optimizing-sql) - Query performance tuning

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/transforming-data)
- [dbt Documentation](https://docs.getdbt.com/)
- [Polars Documentation](https://pola-rs.github.io/polars/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
