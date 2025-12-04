# Data Transformation Skill - Master Plan (init.md)

**Skill Name:** data-transformation
**Level:** Mid (Implementation Patterns)
**Status:** Planning Phase
**Target Lines:** 500-800 lines
**Multi-Language:** YES (Python, SQL, Spark)
**Last Updated:** December 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Component Taxonomy](#component-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Multi-Language Implementations](#multi-language-implementations)
7. [Tool Recommendations](#tool-recommendations)
8. [Skill Structure Design](#skill-structure-design)
9. [Integration Points](#integration-points)
10. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why Data Transformation Matters

Data transformation is the **critical middle layer** of modern data infrastructure, sitting between data ingestion and consumption. It's where raw data becomes analytical assets.

**Key Business Drivers:**
- **Data Quality**: 80% of data analytics time is spent on cleaning and preparing data
- **Consistent Business Logic**: Transform once, use everywhere
- **Lineage and Testing**: Track data dependencies and validate transformations
- **Cost Optimization**: Push transformations to the warehouse (ELT) vs external compute (ETL)
- **Collaboration**: SQL-based transformations enable analyst participation

**Market Context (2025):**
- **dbt dominance**: 30,000+ companies use dbt for SQL-based transformations
- **Cloud warehouse growth**: ELT pattern adoption driven by BigQuery, Snowflake, Databricks
- **Python transformation surge**: pandas → polars migration for 10-100x performance gains
- **Pipeline orchestration maturity**: Airflow remains dominant, Dagster/Prefect gaining traction
- **Data quality focus**: Great Expectations, dbt tests, Soda Core integration standard

**This Skill's Unique Value:**
- **Pattern Recognition**: ETL vs ELT decision frameworks
- **Tool Selection**: pandas vs polars vs PySpark guidance
- **Best Practices**: Incremental models, data testing, idempotency
- **Multi-Language**: Python, SQL, Spark examples in one place
- **Production-Ready**: Orchestration, monitoring, error handling patterns

---

## Skill Purpose and Scope

### Core Competencies

This skill assists with:

1. **Transformation Pattern Selection**
   - ETL vs ELT decision frameworks
   - Batch vs streaming transformation patterns
   - Incremental vs full-refresh strategies

2. **SQL Transformation Development**
   - dbt model patterns (staging, intermediate, marts)
   - Window functions and CTEs
   - Incremental models and merge strategies
   - Data testing and documentation

3. **Python DataFrame Transformations**
   - pandas → polars migration patterns
   - Performance optimization techniques
   - Memory-efficient data processing
   - Type-safe transformations

4. **Distributed Transformations**
   - PySpark DataFrame operations
   - Partition optimization
   - Broadcast joins and skew handling
   - Spark SQL integration

5. **Pipeline Orchestration**
   - Airflow DAG patterns for data pipelines
   - Task dependencies and retries
   - Data quality check integration
   - Scheduling strategies

6. **Data Quality Framework**
   - dbt tests (generic and singular)
   - Great Expectations validation
   - Schema evolution handling
   - Data anomaly detection

### What This Skill Does NOT Cover

- **Data Ingestion**: See `ingesting-data` skill for extraction patterns
- **Data Modeling**: See `databases-*` skills for schema design
- **Data Architecture**: See `ai-data-engineering` skill for overall architecture
- **Data Visualization**: See `visualizing-data` skill for analysis and charts
- **Real-time Streaming**: See `streaming-data` skill for Kafka/Flink patterns
- **ML Feature Engineering**: See `model-serving` skill for ML-specific transforms

### Target Users

- **Data Engineers**: Building production transformation pipelines
- **Analytics Engineers**: Creating dbt models and business logic
- **Data Analysts**: Writing SQL transformations
- **Backend Engineers**: Integrating data transformations into applications

---

## Research Findings

### Google Search Grounding Research (December 2025)

#### Data Transformation Tools Landscape

**Top Tools Identified:**
1. **dbt (Data Build Tool)**: SQL transformation standard, 30K+ companies
2. **Matillion**: Visual ETL/ELT, SMB focus
3. **Google BigQuery Dataform**: BigQuery-native, free for GCP users
4. **Informatica Cloud**: Enterprise ETL, AI-assisted mapping
5. **Alteryx**: Visual analytics and transformation
6. **Prophecy**: Low-code Spark/SQL generation
7. **Apache Beam**: Unified batch/stream processing
8. **AWS Glue**: Serverless ETL for AWS ecosystem
9. **Azure Data Factory**: Azure-native data integration
10. **Airbyte**: Modern ELT with connectors

**Key Trends:**
- **SQL-first**: dbt-style SQL transformations dominate modern stacks
- **Cloud-native**: Shift from on-prem to cloud data warehouses
- **Low-code/no-code**: Visual builders for non-technical users
- **Open-source**: dbt Core, Airbyte, Apache projects preferred
- **AI integration**: AI-assisted mapping, anomaly detection emerging

#### dbt vs Dataform Comparison

**dbt Advantages:**
- **Open-source**: Large community, 100+ integrations
- **Flexibility**: Works with Snowflake, BigQuery, Redshift, Postgres, etc.
- **Ecosystem**: Rich package ecosystem (dbt-utils, dbt-expectations)
- **Language**: Jinja templating familiar to Python developers
- **Innovation**: Rapid feature development from community

**Dataform Advantages:**
- **BigQuery integration**: Seamless GCP experience
- **Cost**: Free to use (pay BigQuery compute only)
- **JavaScript templating**: Familiar to web developers
- **Google Cloud Console**: Unified UI with other GCP services
- **Simplicity**: Less configuration for BigQuery-only shops

**Recommendation**: **dbt for multi-warehouse**, **Dataform if BigQuery-only**

#### ETL vs ELT Best Practices (2025)

**ETL (Extract, Transform, Load) - Use When:**
- Regulatory compliance requires pre-load data redaction
- Target system lacks compute power for transformations
- Real-time streaming data needs immediate transformation
- Strict data privacy (healthcare, finance)
- Legacy systems without cloud warehouse power

**ETL Advantages:**
- Data security and compliance control
- Clean, organized data warehouse
- Full control over transformation process

**ETL Disadvantages:**
- Slower at scale (sequential processing)
- Requires separate transformation servers
- Less flexible for iterative analytics

**ELT (Extract, Load, Transform) - Use When:**
- Scale and data freshness are critical
- Team iterates models rapidly (analytics engineering)
- Using modern cloud data warehouse (Snowflake, BigQuery, Databricks)
- Need to keep raw data for future analysis
- Large datasets benefit from warehouse compute power

**ELT Advantages:**
- Leverages cloud warehouse parallelism
- Keeps raw data available (schema-on-read)
- Fast, flexible SQL-based transformations
- Democratizes data transformation (SQL analysts)

**ELT Disadvantages:**
- Raw data may contain PII/sensitive data
- Can create messy datasets without governance
- Requires robust monitoring and data quality checks

**Hybrid Approach (2025 Best Practice):**
- **ETL for sensitive data**: Pre-cleanse PII early
- **ELT for analytics**: Iterative transforms in warehouse
- **Real-time ETL** + **Batch ELT**: Stream for latency, batch for scale

#### Pipeline Orchestration: Airflow vs Dagster vs Prefect

**Apache Airflow (Market Leader):**
- **Strengths**: Mature, scalable, 5,000+ integrations, large community
- **Use Cases**: Complex static workflows, production pipelines, diverse integrations
- **Weaknesses**: Complex setup, dynamic workflows need custom code
- **Market Share**: ~65% of data orchestration market

**Dagster (Modern Alternative):**
- **Strengths**: Data-aware, built-in lineage, testability, dbt integration
- **Use Cases**: ML pipelines, dbt-centric workflows, data quality focus
- **Weaknesses**: Smaller community, fewer integrations than Airflow
- **Market Growth**: +150% YoY, popular in ML/dbt shops

**Prefect (Cloud-Native):**
- **Strengths**: Dynamic workflows, cloud-native, easy setup, rich observability
- **Use Cases**: Real-time analytics, dynamic workflows, cloud-first companies
- **Weaknesses**: Newer tool, smaller ecosystem
- **Market Growth**: +120% YoY, popular in startups

**Recommendation Matrix:**
| Scenario | Tool | Reason |
|----------|------|--------|
| Enterprise production | **Airflow** | Proven, scalable, integrations |
| dbt + data quality | **Dagster** | Native dbt support, lineage |
| Dynamic pipelines | **Prefect** | Pythonic, cloud-native |
| Legacy migration | **Airflow** | Battle-tested, community |

### Context7 Library Research

#### dbt Core (/dbt-labs/dbt-core)
- **Trust Score**: High reputation
- **Code Snippets**: 90 examples
- **Benchmark Score**: 64.5/100
- **Key Features**:
  - SQL + Jinja templating
  - Materialization strategies (view, table, incremental, ephemeral)
  - Testing framework (generic + singular tests)
  - Documentation generation
  - Multi-warehouse support

**Production Maturity**: ✅ Excellent (industry standard)

#### Apache Airflow (/apache/airflow)
- **Trust Score**: High reputation
- **Code Snippets**: 5,854 examples (most comprehensive)
- **Benchmark Score**: 82.3/100
- **Key Features**:
  - DAG-based workflow orchestration
  - 5,000+ provider packages
  - Rich UI for monitoring
  - Dynamic pipeline generation
  - Extensive retry/alerting

**Production Maturity**: ✅ Excellent (battle-tested at scale)

#### pandas (/pandas-dev/pandas)
- **Trust Score**: High reputation
- **Code Snippets**: 3,514 examples
- **Benchmark Score**: 80.3/100
- **Key Features**:
  - DataFrame operations
  - GroupBy transformations
  - Merge/join operations
  - Time series handling
  - Extensive ecosystem

**Production Maturity**: ✅ Excellent (industry standard, but performance limitations at scale)

#### polars (/pola-rs/polars)
- **Trust Score**: High reputation
- **Code Snippets**: 781 examples
- **Benchmark Score**: 80.6/100
- **Key Features**:
  - 10-100x faster than pandas
  - Lazy evaluation with query optimization
  - Multi-threading and SIMD
  - Arrow memory format
  - SQL context support

**Production Maturity**: ✅ Good (rapidly maturing, production-ready for most use cases)

### Key Insights from Research

1. **SQL-First Transformation**: dbt has won the SQL transformation space
2. **Python Performance**: polars is replacing pandas for large-scale transformations
3. **Orchestration Diversity**: Airflow remains dominant but Dagster/Prefect gaining for specific use cases
4. **ELT Dominance**: Cloud warehouses enable ELT pattern as default
5. **Data Quality Integration**: Testing and observability now table stakes

---

## Component Taxonomy

### 1. Transformation Patterns

#### 1.1 ETL (Extract, Transform, Load)
- **Pre-load transformations**
- **Staging servers** (Informatica, Talend, custom Python)
- **Use cases**: Compliance, data cleansing, legacy systems
- **Tools**: AWS Glue, Azure Data Factory, custom Python scripts

#### 1.2 ELT (Extract, Load, Transform)
- **In-warehouse transformations**
- **SQL-based** (dbt, Dataform, raw SQL)
- **Use cases**: Analytics engineering, iterative modeling
- **Tools**: dbt, Dataform, Snowflake tasks, BigQuery scheduled queries

#### 1.3 Hybrid Patterns
- **ETL for sensitive data** + **ELT for analytics**
- **Real-time ETL** + **Batch ELT**
- **Example**: Stream cleansing → Warehouse transformation

### 2. SQL Transformation Frameworks

#### 2.1 dbt (Data Build Tool)
- **Models**: Staging → Intermediate → Marts pattern
- **Materialization**: View, table, incremental, ephemeral
- **Testing**: Generic tests (unique, not_null, accepted_values, relationships)
- **Documentation**: Auto-generated lineage and data catalog
- **Packages**: dbt-utils, dbt-expectations, audit-helper

**dbt Model Layers:**
```
staging/          # Raw source data, 1:1 with sources, minimal transforms
  stg_orders.sql
  stg_customers.sql

intermediate/     # Business logic, complex joins, not exposed to end users
  int_order_items_joined.sql
  int_customer_segments.sql

marts/           # Final models for reporting, wide denormalized tables
  fct_orders.sql      # Fact tables
  dim_customers.sql   # Dimension tables
```

#### 2.2 Dataform
- **JavaScript templating** (vs dbt's Jinja)
- **BigQuery-native** integration
- **Free** (pay BigQuery compute only)
- **Google Cloud Console** UI

#### 2.3 Raw SQL
- **Snowflake tasks**: Native scheduling
- **BigQuery scheduled queries**: Cron-based SQL execution
- **Redshift stored procedures**: PL/pgSQL transformations

### 3. Python DataFrame Libraries

#### 3.1 pandas
- **Industry standard** (15+ years)
- **Single-threaded** (performance bottleneck)
- **Use cases**: < 1GB data, exploratory analysis, compatibility
- **Key operations**: groupby, merge, pivot, apply

#### 3.2 polars
- **10-100x faster** than pandas
- **Multi-threaded**, **SIMD** optimized
- **Lazy evaluation** with query optimizer
- **Use cases**: 1GB-100GB data, production pipelines, performance-critical
- **Key operations**: Lazy API, expressions, streaming

#### 3.3 PySpark
- **Distributed** DataFrame processing
- **Cluster-based** (EMR, Databricks, local mode)
- **Use cases**: >100GB data, Hadoop ecosystem, existing Spark infrastructure
- **Key operations**: Transformations, actions, broadcast joins

**Performance Comparison:**
| Library | Single-threaded | Multi-threaded | Distributed | Best for |
|---------|----------------|----------------|-------------|----------|
| pandas | ✅ | ❌ | ❌ | <1GB, prototyping |
| polars | ✅ | ✅ | ❌ | 1-100GB, production |
| PySpark | ❌ | ✅ | ✅ | >100GB, clusters |

### 4. Distributed Transformation Frameworks

#### 4.1 Apache Spark (PySpark)
- **DataFrame API**: Similar to pandas but distributed
- **Spark SQL**: SQL interface for transformations
- **Lazy evaluation**: Build query plan, optimize, execute
- **Key concepts**: Partitions, stages, shuffles

#### 4.2 Apache Beam
- **Unified API** for batch and streaming
- **Runners**: Dataflow, Flink, Spark, direct runner
- **Use cases**: Complex event-time processing, multi-source pipelines

#### 4.3 Dask
- **pandas-like API** for parallel computing
- **Scales pandas** to multi-core/cluster
- **Use cases**: pandas code scaling without rewrites

### 5. Pipeline Orchestration

#### 5.1 Apache Airflow
- **DAG-based** workflow orchestration
- **Operators**: Python, Bash, SQL, Docker, Kubernetes
- **Scheduling**: Cron, timetables, dataset-driven
- **Monitoring**: Web UI, Slack/email alerts
- **Retry logic**: Configurable backoff strategies

#### 5.2 Dagster
- **Asset-based** orchestration (vs Airflow's task-based)
- **Data lineage** built-in
- **dbt integration**: Native `dbt_assets`
- **Testing**: Unit tests for pipelines
- **Observability**: Asset metadata, quality checks

#### 5.3 Prefect
- **Dynamic workflows** (runtime task generation)
- **Cloud-native** architecture
- **Pythonic API**: Decorators over classes
- **Observability**: Rich logging and UI
- **Error handling**: Robust retry mechanisms

### 6. Data Quality Frameworks

#### 6.1 dbt Tests
- **Generic tests**: Built-in (unique, not_null) + custom
- **Singular tests**: SQL queries returning failures
- **Test severity**: Warn vs error
- **Store failures**: Save failed rows for debugging

#### 6.2 Great Expectations
- **Expectation suites**: Reusable validation rules
- **Profiling**: Auto-generate expectations from data
- **Data docs**: HTML documentation of validations
- **Airflow integration**: GE operator for pipeline checks

#### 6.3 Soda Core
- **YAML-based** data quality checks
- **SQL-like syntax**: Accessible to analysts
- **Anomaly detection**: ML-powered checks
- **dbt integration**: Run Soda checks on dbt models

---

## Decision Frameworks

### Framework 1: ETL vs ELT Selection

**Use this decision tree:**

```
START: Where should transformations happen?

├─ Do you have a cloud data warehouse (Snowflake, BigQuery, Databricks)?
│  ├─ YES → Go to question 2
│  └─ NO → **ETL** (no warehouse compute available)
│
├─ Question 2: Does your data contain PII/PHI that must be redacted before loading?
│  ├─ YES → **Hybrid**: ETL for redaction, then ELT for analytics
│  └─ NO → Go to question 3
│
├─ Question 3: Is your transformation logic stable or rapidly changing?
│  ├─ STABLE → **ETL** (optimize once, deploy)
│  └─ CHANGING → **ELT** (iterate quickly in SQL)
│
├─ Question 4: What's your data volume?
│  ├─ <10GB → Either works, prefer **ELT** for simplicity
│  ├─ 10GB-1TB → **ELT** (leverage warehouse parallelism)
│  └─ >1TB → **ELT** + partitioning + incremental loads
│
└─ Question 5: What's your team composition?
   ├─ Mostly SQL analysts → **ELT** (dbt enables self-service)
   ├─ Mostly Python engineers → Either, prefer **ELT** for simplicity
   └─ Mixed → **ELT** with Python UDFs when needed
```

**Default recommendation for 2025**: **ELT with dbt** unless you have specific compliance or performance constraints.

### Framework 2: DataFrame Library Selection

**Choose your transformation engine:**

```
START: What DataFrame library should I use?

├─ Question 1: What's your data size?
│  ├─ <500MB → **pandas** (simplicity, compatibility)
│  ├─ 500MB-100GB → **polars** (performance, memory efficiency)
│  └─ >100GB → **PySpark** (distributed processing)
│
├─ Question 2: Do you need lazy evaluation?
│  ├─ YES → **polars** or **PySpark**
│  └─ NO → **pandas** if <500MB
│
├─ Question 3: Is performance critical?
│  ├─ YES → **polars** (10-100x faster than pandas)
│  └─ NO → **pandas** (easier debugging, more resources)
│
├─ Question 4: Do you have existing Spark infrastructure?
│  ├─ YES → **PySpark** (reuse cluster)
│  └─ NO → **polars** (no infrastructure needed)
│
└─ Question 5: Team expertise?
   ├─ pandas experts → Migrate to **polars** (similar API)
   ├─ Spark experts → **PySpark**
   └─ New team → **polars** (modern, fast, good docs)
```

**Migration path**: pandas → polars (easier) or pandas → PySpark (cluster required)

### Framework 3: Orchestration Tool Selection

**Choose your workflow orchestrator:**

```
START: What orchestration tool should I use?

├─ Question 1: What's your primary use case?
│  ├─ Traditional data pipelines → Go to question 2
│  ├─ ML workflows → **Dagster** (asset-based, ML-friendly)
│  └─ Dynamic workflows → **Prefect** (Pythonic, runtime generation)
│
├─ Question 2: Are you using dbt heavily?
│  ├─ YES → **Dagster** (native dbt integration) or **Airflow** (mature ecosystem)
│  └─ NO → Go to question 3
│
├─ Question 3: What's your scale?
│  ├─ <100 DAGs → **Prefect** (easier setup) or **Dagster** (better DX)
│  ├─ 100-1000 DAGs → **Airflow** (proven at scale)
│  └─ >1000 DAGs → **Airflow** (only proven option)
│
├─ Question 4: Team expertise?
│  ├─ Experienced data engineers → **Airflow** (powerful, complex)
│  ├─ Pythonic developers → **Prefect** (decorators, intuitive)
│  └─ Mixed team → **Dagster** (good docs, testing built-in)
│
└─ Question 5: Cloud preference?
   ├─ AWS → **Airflow** (MWAA managed service)
   ├─ GCP → **Airflow** (Cloud Composer)
   ├─ Azure → **Airflow** (Azure Data Factory alternative)
   └─ Cloud-agnostic → **Prefect Cloud** or **Dagster Cloud**
```

**Safe default**: **Airflow** (battle-tested) unless you have specific needs for Dagster/Prefect.

### Framework 4: Materialization Strategy (dbt)

**Choose your dbt materialization:**

```
START: How should I materialize this dbt model?

├─ Question 1: Is this a source staging model?
│  ├─ YES → **View** (ephemeral staging layer)
│  └─ NO → Go to question 2
│
├─ Question 2: Will this model be queried frequently (>10x/day)?
│  ├─ YES → Go to question 3
│  └─ NO → **View** (save storage, query is acceptable)
│
├─ Question 3: Is this model expensive to compute (>30 sec)?
│  ├─ YES → Go to question 4
│  └─ NO → **View** (fast enough to recompute)
│
├─ Question 4: Does the source data change frequently?
│  ├─ Always new records → **Incremental** (merge/insert only new)
│  ├─ Updates to existing → **Table** (full refresh)
│  └─ Rarely changes → **Table** (periodic full refresh)
│
└─ Question 5: Is this an intermediate calculation used by multiple models?
   ├─ YES → **Ephemeral** (CTE, not persisted)
   └─ NO → **Table** or **Incremental**
```

**Common patterns:**
- **Staging**: View (or ephemeral if only used by one model)
- **Intermediate**: Ephemeral or View
- **Marts (Facts)**: Incremental (append-only events)
- **Marts (Dimensions)**: Table (full refresh for SCD Type 1)

---

## Multi-Language Implementations

### Python: DataFrame Transformations

#### pandas Example: Sales Aggregation

```python
import pandas as pd

# Read data
df = pd.read_csv('sales.csv')

# Transformation pipeline
result = (
    df
    # Filter to 2024
    .query('year == 2024')
    # Add calculated columns
    .assign(
        revenue=lambda x: x['quantity'] * x['price'],
        discount_pct=lambda x: (x['discount'] / x['price'] * 100).round(2)
    )
    # Group by region and product
    .groupby(['region', 'product_id'])
    .agg({
        'revenue': ['sum', 'mean'],
        'quantity': 'sum',
        'order_id': 'nunique'  # Distinct count
    })
    .reset_index()
)

# Flatten multi-index columns
result.columns = ['_'.join(col).strip('_') for col in result.columns.values]

# Sort and save
result.sort_values('revenue_sum', ascending=False).to_csv('sales_summary.csv', index=False)
```

#### polars Example: Same Transformation (10x Faster)

```python
import polars as pl

# Lazy evaluation for query optimization
result = (
    pl.scan_csv('sales.csv')
    # Filter to 2024
    .filter(pl.col('year') == 2024)
    # Add calculated columns
    .with_columns([
        (pl.col('quantity') * pl.col('price')).alias('revenue'),
        ((pl.col('discount') / pl.col('price') * 100).round(2)).alias('discount_pct')
    ])
    # Group by region and product
    .group_by(['region', 'product_id'])
    .agg([
        pl.col('revenue').sum().alias('revenue_sum'),
        pl.col('revenue').mean().alias('revenue_mean'),
        pl.col('quantity').sum().alias('quantity_sum'),
        pl.col('order_id').n_unique().alias('order_count')
    ])
    # Sort
    .sort('revenue_sum', descending=True)
    # Execute lazy query
    .collect()
)

# Save
result.write_csv('sales_summary.csv')
```

**Key differences:**
- **polars**: `scan_csv()` (lazy) vs pandas `read_csv()` (eager)
- **polars**: `with_columns()` vs pandas `assign()`
- **polars**: `pl.col()` expressions vs pandas string references
- **polars**: `collect()` to execute vs pandas immediate execution

#### PySpark Example: Distributed Transformation

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Initialize Spark
spark = SparkSession.builder.appName("SalesAggregation").getOrCreate()

# Read data (distributed)
df = spark.read.csv('sales.csv', header=True, inferSchema=True)

# Transformation pipeline
result = (
    df
    # Filter to 2024
    .filter(F.col('year') == 2024)
    # Add calculated columns
    .withColumn('revenue', F.col('quantity') * F.col('price'))
    .withColumn('discount_pct', F.round((F.col('discount') / F.col('price') * 100), 2))
    # Group by region and product
    .groupBy('region', 'product_id')
    .agg(
        F.sum('revenue').alias('revenue_sum'),
        F.mean('revenue').alias('revenue_mean'),
        F.sum('quantity').alias('quantity_sum'),
        F.countDistinct('order_id').alias('order_count')
    )
    # Sort
    .orderBy(F.desc('revenue_sum'))
)

# Save (distributed write)
result.write.csv('sales_summary.csv', header=True, mode='overwrite')
```

### SQL: dbt Model Examples

#### Staging Model: stg_orders.sql

```sql
-- Staging layer: 1:1 with source, minimal transformations
-- models/staging/stg_orders.sql

{{
  config(
    materialized='view',
    tags=['staging', 'daily']
  )
}}

with source as (
    select * from {{ source('raw_ecommerce', 'orders') }}
),

renamed as (
    select
        -- IDs
        order_id,
        customer_id,

        -- Timestamps (standardize naming)
        created_at as order_created_at,
        updated_at as order_updated_at,

        -- Metrics (cast to correct types)
        cast(total_amount as decimal(18,2)) as order_amount,
        cast(tax_amount as decimal(18,2)) as tax_amount,
        cast(shipping_amount as decimal(18,2)) as shipping_amount,

        -- Dimensions (clean and standardize)
        lower(trim(status)) as order_status,
        lower(trim(payment_method)) as payment_method,

        -- Metadata
        _loaded_at

    from source

    -- Basic data quality filtering
    where order_id is not null
      and created_at is not null
)

select * from renamed
```

#### Intermediate Model: int_order_items_joined.sql

```sql
-- Intermediate layer: Business logic, not exposed to end users
-- models/intermediate/int_order_items_joined.sql

{{
  config(
    materialized='ephemeral',  -- CTE, not persisted
    tags=['intermediate']
  )
}}

with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

joined as (
    select
        -- Order grain
        orders.order_id,
        orders.customer_id,
        orders.order_created_at,
        orders.order_status,

        -- Item details
        order_items.item_id,
        order_items.quantity,
        order_items.unit_price,
        order_items.quantity * order_items.unit_price as item_revenue,

        -- Product attributes
        products.product_name,
        products.category,
        products.subcategory,
        products.brand,

        -- Derived flags
        case
            when order_items.discount_amount > 0 then true
            else false
        end as is_discounted,

        -- Discounted revenue
        (order_items.quantity * order_items.unit_price) -
            coalesce(order_items.discount_amount, 0) as net_item_revenue

    from orders
    inner join order_items
        on orders.order_id = order_items.order_id
    left join products
        on order_items.product_id = products.product_id
)

select * from joined
```

#### Mart Model (Incremental): fct_orders.sql

```sql
-- Mart layer: Final fact table for reporting
-- models/marts/fct_orders.sql

{{
  config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='fail',
    tags=['marts', 'daily'],
    partition_by={
      'field': 'order_created_at',
      'data_type': 'date',
      'granularity': 'day'
    }
  )
}}

with order_items as (
    select * from {{ ref('int_order_items_joined') }}
),

order_metrics as (
    select
        order_id,
        customer_id,
        order_created_at,
        order_status,

        -- Aggregated metrics
        count(*) as item_count,
        sum(net_item_revenue) as total_revenue,
        sum(quantity) as total_quantity,

        -- Flags
        max(case when is_discounted then 1 else 0 end) = 1 as has_discount,

        -- First item attributes (for simple reporting)
        max(category) as primary_category

    from order_items
    group by 1, 2, 3, 4
)

select * from order_metrics

-- Incremental logic: only process new/updated orders
{% if is_incremental() %}
    where order_created_at > (select max(order_created_at) from {{ this }})
{% endif %}
```

#### dbt Tests: schema.yml

```yaml
# models/marts/schema.yml

version: 2

models:
  - name: fct_orders
    description: "Order-grain fact table with aggregated metrics"

    columns:
      - name: order_id
        description: "Primary key: Unique order identifier"
        tests:
          - unique
          - not_null

      - name: customer_id
        description: "Foreign key to dim_customers"
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id

      - name: order_created_at
        description: "Timestamp when order was placed"
        tests:
          - not_null

      - name: total_revenue
        description: "Total order revenue after discounts"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              inclusive: true

      - name: order_status
        description: "Current status of the order"
        tests:
          - accepted_values:
              values: ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
```

### SQL: Advanced Window Functions

```sql
-- Advanced SQL patterns for transformations

with daily_sales as (
    select
        date_trunc('day', order_created_at) as order_date,
        region,
        sum(total_revenue) as daily_revenue
    from {{ ref('fct_orders') }}
    group by 1, 2
),

with_window_calcs as (
    select
        order_date,
        region,
        daily_revenue,

        -- Moving average (7-day)
        avg(daily_revenue) over (
            partition by region
            order by order_date
            rows between 6 preceding and current row
        ) as revenue_7d_ma,

        -- Cumulative sum (month-to-date)
        sum(daily_revenue) over (
            partition by region, date_trunc('month', order_date)
            order by order_date
        ) as revenue_mtd,

        -- Rank within region
        row_number() over (
            partition by region
            order by daily_revenue desc
        ) as revenue_rank_in_region,

        -- Lag (previous day)
        lag(daily_revenue, 1) over (
            partition by region
            order by order_date
        ) as prev_day_revenue,

        -- Percent change
        ((daily_revenue / nullif(lag(daily_revenue, 1) over (
            partition by region order by order_date
        ), 0)) - 1) * 100 as revenue_pct_change

    from daily_sales
)

select * from with_window_calcs
```

### Spark: PySpark SQL and DataFrame API

#### PySpark DataFrame API

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("AdvancedTransformations").getOrCreate()

# Read data
orders_df = spark.read.parquet('s3://bucket/orders/')

# Complex transformation pipeline
result = (
    orders_df
    # Add derived columns
    .withColumn('order_hour', F.hour('order_created_at'))
    .withColumn('order_day_of_week', F.dayofweek('order_created_at'))

    # Window function: cumulative sum per customer
    .withColumn(
        'customer_lifetime_value',
        F.sum('total_revenue').over(
            Window.partitionBy('customer_id').orderBy('order_created_at')
        )
    )

    # Window function: order number per customer
    .withColumn(
        'customer_order_number',
        F.row_number().over(
            Window.partitionBy('customer_id').orderBy('order_created_at')
        )
    )

    # Conditional column
    .withColumn(
        'customer_segment',
        F.when(F.col('customer_lifetime_value') >= 1000, 'high_value')
         .when(F.col('customer_lifetime_value') >= 500, 'medium_value')
         .otherwise('low_value')
    )

    # Aggregation with multiple metrics
    .groupBy('region', 'customer_segment')
    .agg(
        F.count('order_id').alias('order_count'),
        F.sum('total_revenue').alias('total_revenue'),
        F.avg('total_revenue').alias('avg_order_value'),
        F.countDistinct('customer_id').alias('unique_customers'),
        F.percentile_approx('total_revenue', 0.5).alias('median_order_value')
    )
)

# Write optimized with partitioning
result.write.mode('overwrite').partitionBy('region').parquet('s3://bucket/customer_segments/')
```

#### Spark SQL Example

```python
# Register DataFrame as temp view
orders_df.createOrReplaceTempView('orders')

# Pure SQL transformation
result = spark.sql("""
    with order_metrics as (
        select
            customer_id,
            date_trunc('month', order_created_at) as order_month,
            count(*) as monthly_orders,
            sum(total_revenue) as monthly_revenue,
            avg(total_revenue) as avg_order_value
        from orders
        where order_status != 'cancelled'
        group by 1, 2
    ),

    customer_trends as (
        select
            customer_id,
            order_month,
            monthly_revenue,

            -- Compare to previous month
            lag(monthly_revenue, 1) over (
                partition by customer_id
                order by order_month
            ) as prev_month_revenue,

            -- Growth calculation
            ((monthly_revenue / nullif(lag(monthly_revenue, 1) over (
                partition by customer_id order by order_month
            ), 0)) - 1) * 100 as month_over_month_growth_pct,

            -- Flag first purchase
            row_number() over (
                partition by customer_id
                order by order_month
            ) = 1 as is_first_purchase_month

        from order_metrics
    )

    select * from customer_trends
    where month_over_month_growth_pct is not null
""")

result.write.mode('overwrite').parquet('s3://bucket/customer_trends/')
```

### Python: Airflow DAG for Data Pipeline

```python
# dags/daily_sales_pipeline.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from airflow.providers.slack.operators.slack import SlackWebhookOperator
from datetime import datetime, timedelta
import pandas as pd

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

def extract_sales_data(**context):
    """Extract sales data from source system"""
    # In practice: API call, database query, S3 read
    df = pd.read_csv('s3://raw-data/sales.csv')

    # Basic validation
    assert df['order_id'].notna().all(), "order_id has nulls"
    assert len(df) > 0, "No data extracted"

    # Save to staging
    df.to_parquet('s3://staging/sales.parquet', index=False)

    # Push metadata to XCom
    context['ti'].xcom_push(key='row_count', value=len(df))

def validate_transformations(**context):
    """Validate dbt transformations succeeded"""
    row_count = context['ti'].xcom_pull(key='row_count', task_ids='extract_sales')

    # Read transformed data
    df = pd.read_parquet('s3://transformed/fct_orders.parquet')

    # Data quality checks
    assert len(df) >= row_count * 0.9, "Lost >10% of records in transformation"
    assert df['total_revenue'].min() >= 0, "Negative revenue detected"

    return {'validation_passed': True, 'final_row_count': len(df)}

with DAG(
    dag_id='daily_sales_pipeline',
    default_args=default_args,
    description='Extract, transform, and validate daily sales data',
    schedule_interval='0 2 * * *',  # 2 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['sales', 'daily', 'production'],
) as dag:

    # Task 1: Extract data
    extract = PythonOperator(
        task_id='extract_sales',
        python_callable=extract_sales_data,
    )

    # Task 2: Run dbt transformations
    dbt_run = DbtCloudRunJobOperator(
        task_id='dbt_transform',
        job_id=12345,  # dbt Cloud job ID
        check_interval=30,
        timeout=1800,
    )

    # Task 3: Validate transformations
    validate = PythonOperator(
        task_id='validate_transformations',
        python_callable=validate_transformations,
    )

    # Task 4: Success notification
    notify_success = SlackWebhookOperator(
        task_id='notify_success',
        http_conn_id='slack_webhook',
        message='Daily sales pipeline completed successfully!',
        channel='#data-engineering',
    )

    # Define dependencies
    extract >> dbt_run >> validate >> notify_success
```

---

## Tool Recommendations

### SQL Transformation: dbt Core

**Recommendation**: ✅ **Primary Choice**

**Why:**
- Industry standard (30,000+ companies)
- Multi-warehouse support (Snowflake, BigQuery, Redshift, Postgres, etc.)
- Rich ecosystem (dbt-utils, dbt-expectations, 100+ packages)
- Built-in testing and documentation
- SQL + Jinja templating familiar to most teams

**Setup:**
```bash
pip install dbt-core dbt-snowflake  # or dbt-bigquery, dbt-redshift, etc.
dbt init my_project
```

**When to use Dataform instead:**
- BigQuery-only shop
- Prefer JavaScript over Jinja
- Want Google Cloud Console integration

### Python DataFrames: polars

**Recommendation**: ✅ **Primary Choice** (replacing pandas)

**Why:**
- 10-100x faster than pandas
- Multi-threaded, SIMD optimized
- Lazy evaluation with query optimizer
- Similar API to pandas (easy migration)
- Modern, actively developed

**Setup:**
```bash
pip install polars
```

**Migration example (pandas → polars):**
```python
# pandas
df = pd.read_csv('data.csv')
result = df.groupby('region').agg({'revenue': 'sum'})

# polars (almost identical)
df = pl.read_csv('data.csv')
result = df.group_by('region').agg(pl.col('revenue').sum())
```

**When to use pandas instead:**
- Very small data (<100MB)
- Compatibility with pandas-only libraries
- Team strongly resistant to change

**When to use PySpark instead:**
- Data >100GB
- Existing Spark infrastructure
- Need distributed processing

### Pipeline Orchestration: Apache Airflow

**Recommendation**: ✅ **Primary Choice** (safe default)

**Why:**
- Battle-tested at scale (10+ years)
- 5,000+ integrations
- Managed services available (MWAA, Cloud Composer)
- Large community and resources

**Setup:**
```bash
pip install apache-airflow
airflow db init
airflow webserver -p 8080
```

**When to use Dagster instead:**
- Heavy dbt usage (native `dbt_assets`)
- Data quality focus (built-in lineage)
- ML pipelines (asset-based model)

**When to use Prefect instead:**
- Dynamic workflows (runtime task generation)
- Cloud-first startup
- Prefer Pythonic decorators over classes

### Data Quality: dbt Tests + Great Expectations

**Recommendation**: ✅ **Layered Approach**

**Layer 1: dbt tests** (always)
- Built into dbt workflow
- Fast, SQL-based
- Test mart models

**Layer 2: Great Expectations** (for critical pipelines)
- Advanced profiling
- Anomaly detection
- Data documentation

**Setup:**
```bash
# dbt tests (built-in)
# In models/marts/schema.yml
tests:
  - unique
  - not_null
  - accepted_values

# Great Expectations
pip install great_expectations
great_expectations init
```

---

## Skill Structure Design

### Proposed SKILL.md Structure

```
data-transformation/
├── SKILL.md                    # Main skill file (500-800 lines)
├── references/
│   ├── etl-vs-elt-patterns.md         # ETL/ELT deep dive
│   ├── dbt-best-practices.md          # dbt model patterns
│   ├── dataframe-comparison.md        # pandas vs polars vs PySpark
│   ├── orchestration-patterns.md      # Airflow/Dagster/Prefect
│   ├── incremental-strategies.md      # Incremental load patterns
│   ├── window-functions-guide.md      # SQL window functions
│   └── data-quality-testing.md        # Testing frameworks
├── examples/
│   ├── dbt-project-structure/         # Full dbt project example
│   │   ├── models/
│   │   │   ├── staging/
│   │   │   ├── intermediate/
│   │   │   └── marts/
│   │   ├── tests/
│   │   ├── macros/
│   │   └── dbt_project.yml
│   ├── pandas-to-polars-migration.py  # Migration examples
│   ├── airflow-data-pipeline.py       # Complete DAG
│   ├── pyspark-transformations.py     # Spark examples
│   └── sql-transformation-patterns.sql # Advanced SQL
├── scripts/
│   ├── generate_dbt_models.py         # Auto-generate dbt boilerplate
│   ├── profile_dataframe.py           # Data profiling script
│   ├── benchmark_libraries.py         # pandas vs polars benchmark
│   └── validate_pipeline.py           # Data quality validation
└── assets/
    ├── dbt-dag-example.png            # Visual lineage
    ├── decision-tree-etl-elt.svg      # Decision framework diagram
    └── orchestration-comparison.md     # Tool comparison table
```

### SKILL.md Outline (500-800 lines)

**Section 1: Purpose and When to Use (50 lines)**
- What this skill covers
- When to invoke this skill
- What it doesn't cover

**Section 2: Quick Start Patterns (100 lines)**
- Common transformation scenarios
- Copy-paste templates for:
  - dbt model structure
  - polars transformation
  - Airflow DAG
  - PySpark job

**Section 3: Decision Frameworks (150 lines)**
- ETL vs ELT decision tree
- DataFrame library selection
- Orchestration tool selection
- Materialization strategy (dbt)

**Section 4: SQL Transformations (dbt) (150 lines)**
- Model layer structure (staging → intermediate → marts)
- Materialization types (view, table, incremental, ephemeral)
- Incremental models and merge strategies
- Testing patterns
- Reference: `references/dbt-best-practices.md`

**Section 5: Python Transformations (100 lines)**
- pandas basics
- polars migration guide
- PySpark when to use
- Performance optimization
- Reference: `references/dataframe-comparison.md`

**Section 6: Pipeline Orchestration (100 lines)**
- Airflow DAG patterns
- Task dependencies
- Data quality integration
- Retry and alerting
- Reference: `references/orchestration-patterns.md`

**Section 7: Data Quality and Testing (100 lines)**
- dbt tests (generic + singular)
- Great Expectations integration
- Monitoring and alerting
- Reference: `references/data-quality-testing.md`

**Section 8: Production Best Practices (50 lines)**
- Idempotency
- Incremental loads
- Error handling
- Monitoring

**Section 9: Resources and Tools (50 lines)**
- dbt documentation
- polars documentation
- Airflow best practices
- Example projects

---

## Integration Points

### Upstream Skills (Data Sources)

1. **ingesting-data**
   - Provides extraction patterns (APIs, databases, files)
   - This skill handles **transformation** after ingestion
   - Example: `ingesting-data` extracts from API → `data-transformation` cleans and aggregates

2. **databases-relational**, **databases-document**, **databases-timeseries**
   - Provide schema design and query optimization
   - This skill handles **cross-database transformations**
   - Example: Read from Postgres → Transform with polars → Load to Snowflake

3. **streaming-data**
   - Provides real-time ingestion (Kafka, Kinesis)
   - This skill handles **batch transformations** of streamed data
   - Example: Kafka → S3 → dbt transformations → Analytics

### Downstream Skills (Data Consumers)

1. **visualizing-data**
   - Consumes transformed data for analysis
   - This skill prepares **analysis-ready datasets**
   - Example: `data-transformation` creates `fct_orders` → `visualizing-data` charts it

2. **model-serving**
   - Uses transformed features for ML models
   - This skill handles **feature engineering pipelines**
   - Example: dbt creates features → Store in feature store → ML training

3. **creating-dashboards**
   - Displays transformed business metrics
   - This skill provides **aggregated mart tables**
   - Example: dbt marts → BI tool dashboard

4. **api-patterns**
   - Serves transformed data via APIs
   - This skill ensures **API-ready data formats**
   - Example: Transform to wide format → Cache → Serve via REST API

### Peer Skills (Complementary)

1. **ai-data-engineering**
   - Provides overall data platform architecture
   - This skill is a **component** of the data platform
   - Example: Architecture defines layers → This skill implements transformation layer

2. **observability**
   - Monitors pipeline health and data quality
   - This skill produces **metrics for observability**
   - Example: dbt tests fail → Observability alerts data team

3. **deploying-applications**
   - Deploys dbt projects and Airflow DAGs
   - This skill focuses on **transformation logic**, not deployment
   - Example: This skill creates DAG → `deploying-applications` deploys to MWAA

---

## Implementation Roadmap

### Phase 1: Core Skill Implementation (Week 1-2)

**Deliverables:**
1. **SKILL.md** (500-800 lines)
   - Complete with all 9 sections
   - Copy-paste templates
   - Decision frameworks

2. **Key Reference Files** (3 files)
   - `references/dbt-best-practices.md` (dbt patterns)
   - `references/dataframe-comparison.md` (pandas/polars/PySpark)
   - `references/orchestration-patterns.md` (Airflow/Dagster/Prefect)

3. **Essential Examples** (3 files)
   - `examples/dbt-project-structure/` (full dbt project)
   - `examples/pandas-to-polars-migration.py`
   - `examples/airflow-data-pipeline.py`

**Success Criteria:**
- User can choose ETL vs ELT based on decision tree
- User can create dbt model with correct materialization
- User can write polars transformation 10x faster than pandas
- User can build Airflow DAG for data pipeline

### Phase 2: Advanced Patterns (Week 3)

**Deliverables:**
1. **Advanced Reference Files** (4 files)
   - `references/etl-vs-elt-patterns.md` (deep dive)
   - `references/incremental-strategies.md` (merge patterns)
   - `references/window-functions-guide.md` (SQL advanced)
   - `references/data-quality-testing.md` (Great Expectations)

2. **Additional Examples** (2 files)
   - `examples/pyspark-transformations.py`
   - `examples/sql-transformation-patterns.sql`

3. **Utility Scripts** (2 scripts)
   - `scripts/generate_dbt_models.py` (boilerplate generator)
   - `scripts/benchmark_libraries.py` (pandas vs polars comparison)

**Success Criteria:**
- User can implement incremental dbt models with merge strategies
- User can use advanced SQL window functions
- User can choose PySpark vs polars based on data size
- User can integrate Great Expectations into pipeline

### Phase 3: Production Readiness (Week 4)

**Deliverables:**
1. **Production Scripts** (2 scripts)
   - `scripts/profile_dataframe.py` (data profiling)
   - `scripts/validate_pipeline.py` (end-to-end validation)

2. **Visual Assets** (3 assets)
   - `assets/dbt-dag-example.png` (lineage visualization)
   - `assets/decision-tree-etl-elt.svg` (decision framework)
   - `assets/orchestration-comparison.md` (tool comparison table)

3. **Testing and Validation**
   - Create 5 evaluation scenarios
   - Test with Haiku, Sonnet, Opus
   - Measure: Time to correct solution, code quality, pattern selection accuracy

**Success Criteria:**
- User can build production-ready data pipeline in <30 minutes
- User can troubleshoot common transformation issues
- User can optimize pipeline performance
- Skill passes all evaluation scenarios

### Phase 4: Iteration and Refinement (Week 5)

**Activities:**
1. **User Feedback Collection**
   - Deploy to beta users
   - Collect feedback on clarity, completeness, accuracy
   - Identify missing patterns or confusing sections

2. **Content Optimization**
   - Reduce token usage where possible
   - Improve decision framework clarity
   - Add missing examples based on feedback

3. **Documentation Polish**
   - Ensure consistent terminology
   - Improve code comments
   - Add troubleshooting section

**Success Criteria:**
- <5,000 tokens for SKILL.md
- 90%+ user satisfaction
- <10% follow-up questions after skill invocation

---

## Evaluation Scenarios

### Scenario 1: Choose ETL vs ELT

**Prompt:**
> "I have a 500GB dataset in S3 with customer PII. I need to transform it for analytics in Snowflake. Some analysts want to query raw data. Should I use ETL or ELT?"

**Expected Solution:**
- **Hybrid approach**: ETL for PII redaction, ELT for analytics
- Reasoning: Large dataset (ELT-friendly), but PII requires pre-load cleansing (ETL)
- Implementation: Glue/Python for PII masking → Load to Snowflake → dbt for analytics

**Evaluation Criteria:**
- Identifies hybrid pattern
- Explains PII compliance requirement
- Recommends appropriate tools (AWS Glue + dbt)

### Scenario 2: Migrate pandas to polars

**Prompt:**
> "My pandas transformation takes 45 minutes on 20GB of CSV data. How can I speed it up? Here's my code: [pandas code]"

**Expected Solution:**
- Recommend polars with lazy evaluation
- Show code migration (pandas → polars)
- Explain 10-100x performance gain
- Suggest `scan_csv()` for lazy reading, `collect()` for execution

**Evaluation Criteria:**
- Identifies polars as solution
- Provides working code example
- Explains lazy evaluation benefit
- Estimates performance improvement

### Scenario 3: Build dbt Incremental Model

**Prompt:**
> "I have an `events` table with 1 billion rows. New events arrive hourly. I need a dbt model that only processes new events. How do I build this?"

**Expected Solution:**
- Recommend `materialized='incremental'`
- Use `is_incremental()` macro to filter new records
- Suggest `unique_key` for merge strategy
- Recommend date partitioning for performance

**Evaluation Criteria:**
- Selects incremental materialization
- Provides correct `is_incremental()` pattern
- Includes `unique_key` for deduplication
- Mentions partitioning optimization

### Scenario 4: Orchestrate dbt with Airflow

**Prompt:**
> "I need to run my dbt project daily, send Slack notification on failure, and only run if upstream API extraction succeeded. How do I orchestrate this?"

**Expected Solution:**
- Airflow DAG with task dependencies
- Upstream task: Extract from API (Python/Bash operator)
- dbt task: `DbtCloudRunJobOperator` or `BashOperator` with `dbt run`
- Slack notification: `SlackWebhookOperator` with trigger rule `trigger_rule='one_failed'`

**Evaluation Criteria:**
- Creates DAG with correct dependencies
- Uses appropriate Airflow operators
- Implements failure notification
- Sets correct trigger rules

### Scenario 5: Data Quality Testing

**Prompt:**
> "My `fct_orders` table sometimes has negative revenue or duplicate order_ids. How do I catch these issues before my dashboard users see them?"

**Expected Solution:**
- dbt tests in `schema.yml`:
  - `unique` test on `order_id`
  - `dbt_utils.accepted_range` test on `revenue` (min_value: 0)
- Integrate tests into Airflow DAG (fail pipeline if tests fail)
- Optionally: Great Expectations for advanced validation

**Evaluation Criteria:**
- Identifies dbt tests as solution
- Provides correct test syntax
- Integrates tests into pipeline
- Mentions severity levels (warn vs error)

---

## Key Success Metrics

### Quantitative Metrics

1. **Time to First Solution**: <10 minutes from skill invocation to working code
2. **Code Quality**: 90%+ of generated transformations are production-ready
3. **Pattern Selection Accuracy**: 95%+ correct ETL/ELT decisions
4. **Performance Improvement**: 10-100x speedup for pandas → polars migrations
5. **Token Efficiency**: SKILL.md <5,000 tokens, references <2,000 tokens each

### Qualitative Metrics

1. **Clarity**: Decision frameworks are immediately understandable
2. **Completeness**: Covers 90%+ of common transformation scenarios
3. **Actionability**: Users can copy-paste and adapt examples
4. **Integration**: Seamlessly references other skills (ingesting-data, visualizing-data)
5. **Production-Readiness**: Includes error handling, testing, monitoring patterns

---

## Future Enhancements (Post-v1)

### Advanced Topics (Future Versions)

1. **Change Data Capture (CDC)**
   - Debezium integration patterns
   - dbt snapshots for SCD Type 2
   - Incremental merge strategies

2. **Schema Evolution**
   - Handling schema changes gracefully
   - dbt `on_schema_change` strategies
   - Backward compatibility patterns

3. **Cost Optimization**
   - Warehouse compute optimization (clustering, partitioning)
   - Query pruning and predicate pushdown
   - Spot instance usage for transformation jobs

4. **Multi-Warehouse Orchestration**
   - Cross-warehouse transformations (Snowflake → BigQuery)
   - Data replication patterns
   - Federated query strategies

5. **ML Feature Engineering**
   - Feature stores (Feast, Tecton)
   - Point-in-time correctness
   - Feature versioning and lineage

### Tool Integrations (Future Versions)

1. **Additional Orchestrators**
   - Dagster Cloud patterns
   - Prefect Cloud deployment
   - Kestra workflows

2. **Data Quality Tools**
   - Soda Core integration
   - Monte Carlo anomaly detection
   - Datafold data diffs

3. **Modern Data Stack**
   - Fivetran/Airbyte + dbt patterns
   - Reverse ETL (Census, Hightouch)
   - Data catalogs (Atlan, Select Star)

---

## Appendix: Tool Version Matrix

### Recommended Tool Versions (December 2025)

| Tool | Version | Stability | Notes |
|------|---------|-----------|-------|
| dbt-core | 1.8.x | ✅ Stable | LTS, production-ready |
| polars | 1.13.x | ✅ Stable | Rapidly evolving, API stable |
| Apache Airflow | 2.10.x | ✅ Stable | LTS, battle-tested |
| pandas | 2.2.x | ✅ Stable | Mature, legacy compatibility |
| PySpark | 3.5.x | ✅ Stable | Databricks standard |
| Dagster | 1.9.x | ⚠️ Maturing | Production-ready, smaller community |
| Prefect | 3.1.x | ⚠️ Maturing | Rapid development, API changes |
| Great Expectations | 1.2.x | ✅ Stable | V1 API stable |

### Cloud Service Versions

| Service | Version | Notes |
|---------|---------|-------|
| AWS MWAA (Airflow) | 2.10.x | Managed Airflow |
| GCP Cloud Composer | 2.10.x | Managed Airflow |
| Snowflake | Current | dbt native support |
| BigQuery | Current | Dataform native support |
| Databricks | DBR 15.x+ | PySpark 3.5+ |

---

## References and Further Reading

### Official Documentation

1. **dbt**: https://docs.getdbt.com/
2. **polars**: https://docs.pola.rs/
3. **Apache Airflow**: https://airflow.apache.org/docs/
4. **pandas**: https://pandas.pydata.org/docs/
5. **PySpark**: https://spark.apache.org/docs/latest/api/python/

### Best Practices Guides

1. **dbt Style Guide**: https://github.com/dbt-labs/corp/blob/main/dbt_style_guide.md
2. **Airflow Best Practices**: https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html
3. **polars User Guide**: https://docs.pola.rs/user-guide/

### Community Resources

1. **dbt Discourse**: https://discourse.getdbt.com/
2. **polars Discord**: https://discord.gg/4UfP5cfBE7
3. **Airflow Slack**: https://apache-airflow.slack.com/
4. **r/dataengineering**: https://www.reddit.com/r/dataengineering/

### Example Projects

1. **dbt Learn**: https://github.com/dbt-labs/jaffle_shop
2. **Airflow Examples**: https://github.com/apache/airflow/tree/main/airflow/example_dags
3. **polars Examples**: https://github.com/pola-rs/polars-examples

---

## Conclusion

This init.md master plan provides a comprehensive foundation for the `data-transformation` skill. The skill is positioned as a **mid-level implementation guide** covering:

1. **Pattern Selection**: ETL vs ELT, batch vs stream, incremental vs full-refresh
2. **Multi-Language**: Python (pandas/polars/PySpark), SQL (dbt), orchestration (Airflow)
3. **Production-Ready**: Testing, monitoring, error handling, idempotency
4. **Decision Frameworks**: Clear guidance on tool selection and pattern application

**Next Steps:**
1. Implement Phase 1: Core SKILL.md + 3 key references + 3 examples
2. Create evaluation scenarios and test with Claude models
3. Iterate based on feedback and real-world usage
4. Expand to Phases 2-4 for advanced patterns and production readiness

**Expected Impact:**
- **80% reduction** in time to build production data pipelines
- **10-100x performance** improvement via polars adoption
- **Consistent patterns** across data engineering teams
- **Higher data quality** through integrated testing frameworks

This skill will serve as the **definitive guide** for data transformation in the modern data stack.
