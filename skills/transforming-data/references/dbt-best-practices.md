# dbt Best Practices

## Table of Contents

1. [Project Structure](#project-structure)
2. [Model Layering](#model-layering)
3. [Naming Conventions](#naming-conventions)
4. [Materialization Strategies](#materialization-strategies)
5. [Testing Patterns](#testing-patterns)
6. [Documentation](#documentation)
7. [Performance Optimization](#performance-optimization)
8. [Common Patterns](#common-patterns)

---

## Project Structure

### Recommended Directory Layout

```
my_dbt_project/
├── dbt_project.yml          # Project configuration
├── profiles.yml             # Connection profiles (gitignored)
├── packages.yml             # dbt packages (dbt-utils, etc.)
├── models/
│   ├── staging/             # Source staging models
│   │   ├── source.yml       # Source definitions
│   │   ├── stg_orders.sql
│   │   └── stg_customers.sql
│   ├── intermediate/        # Business logic
│   │   └── int_orders_joined.sql
│   ├── marts/               # Final analytics models
│   │   ├── schema.yml       # Tests and documentation
│   │   ├── fct_orders.sql   # Fact tables
│   │   └── dim_customers.sql # Dimension tables
│   └── _models.yml          # Model-level configs
├── macros/                  # Custom SQL macros
│   └── custom_tests.sql
├── tests/                   # Singular tests
│   └── assert_positive_revenue.sql
├── seeds/                   # CSV reference data
│   └── country_codes.csv
├── snapshots/               # SCD Type 2 snapshots
│   └── dim_customers_snapshot.sql
└── analyses/                # Ad-hoc analyses
    └── customer_analysis.sql
```

---

## Model Layering

### Three-Layer Architecture

#### Layer 1: Staging (`models/staging/`)

**Purpose**: Light touch on source data

**Responsibilities**:
- Rename columns for consistency
- Cast data types
- Basic filtering (remove test data, null IDs)
- 1:1 relationship with source tables

**Materialization**: View or Ephemeral

**Example**:
```sql
-- models/staging/stg_orders.sql

with source as (
    select * from {{ source('ecommerce', 'raw_orders') }}
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

        -- Dimensions (clean and standardize)
        lower(trim(status)) as order_status

    from source
    where order_id is not null
)

select * from renamed
```

#### Layer 2: Intermediate (`models/intermediate/`)

**Purpose**: Complex business logic

**Responsibilities**:
- Join multiple staging models
- Apply business rules
- Create reusable building blocks
- NOT exposed to end users

**Materialization**: Ephemeral (preferred) or View

**Naming**: Prefix with `int_`

**Example**:
```sql
-- models/intermediate/int_orders_joined.sql

with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

joined as (
    select
        o.order_id,
        o.customer_id,
        c.customer_email,
        c.customer_segment,
        o.order_created_at,
        o.order_status,
        p.product_name,
        p.category,
        o.order_amount,

        -- Business logic
        case
            when o.order_amount >= 1000 then 'high_value'
            when o.order_amount >= 500 then 'medium_value'
            else 'standard'
        end as order_value_tier

    from orders o
    left join customers c on o.customer_id = c.customer_id
    left join products p on o.product_id = p.product_id
)

select * from joined
```

#### Layer 3: Marts (`models/marts/`)

**Purpose**: Business-facing analytics models

**Responsibilities**:
- Fact tables (events, transactions)
- Dimension tables (customers, products)
- Aggregated metrics
- Wide denormalized tables for BI tools

**Materialization**: Table or Incremental

**Naming**: `fct_` (facts), `dim_` (dimensions)

**Example**:
```sql
-- models/marts/fct_orders.sql

with orders as (
    select * from {{ ref('int_orders_joined') }}
),

aggregated as (
    select
        order_id,
        customer_id,
        order_created_at,
        order_status,
        sum(order_amount) as total_order_amount,
        count(*) as line_item_count

    from orders
    group by 1, 2, 3, 4
)

select * from aggregated
```

---

## Naming Conventions

### Model Names

**Staging models**: `stg_<source>_<entity>.sql`
- Examples: `stg_salesforce_accounts.sql`, `stg_stripe_payments.sql`

**Intermediate models**: `int_<entity>_<verb>.sql`
- Examples: `int_orders_joined.sql`, `int_customers_pivoted.sql`

**Fact tables**: `fct_<entity>.sql`
- Examples: `fct_orders.sql`, `fct_sessions.sql`

**Dimension tables**: `dim_<entity>.sql`
- Examples: `dim_customers.sql`, `dim_products.sql`

### Column Names

**IDs**: Suffix with `_id`
- Good: `customer_id`, `order_id`
- Bad: `customer`, `order`

**Booleans**: Prefix with `is_` or `has_`
- Good: `is_active`, `has_purchased`
- Bad: `active`, `purchased`

**Timestamps**: Suffix with `_at`
- Good: `created_at`, `updated_at`
- Bad: `creation_date`, `update_time`

**Dates**: Suffix with `_date`
- Good: `order_date`, `signup_date`
- Bad: `order_day`, `signup`

**Counts**: Suffix with `_count`
- Good: `order_count`, `session_count`
- Bad: `orders`, `sessions`

---

## Materialization Strategies

### View

**Use when**:
- Staging models (always views or ephemeral)
- Rarely queried models
- Fast queries (<1 second)

**Config**:
```sql
{{
  config(
    materialized='view'
  )
}}
```

**Pros**: Always up-to-date, no storage cost
**Cons**: Query runs every time model is referenced

### Table

**Use when**:
- Frequently queried models (>10x/day)
- Expensive queries (>30 seconds)
- Dimension tables with full refresh

**Config**:
```sql
{{
  config(
    materialized='table'
  )
}}
```

**Pros**: Fast query performance
**Cons**: Stale data between runs, storage cost

### Incremental

**Use when**:
- Large fact tables (millions of rows)
- Append-only data (events, logs)
- Data updates frequently

**Config**:
```sql
{{
  config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='fail'
  )
}}

select
    order_id,
    customer_id,
    order_created_at,
    total_amount
from {{ ref('stg_orders') }}

{% if is_incremental() %}
    -- Only process new records
    where order_created_at > (select max(order_created_at) from {{ this }})
{% endif %}
```

**Pros**: Fast runs, efficient storage
**Cons**: More complex, risk of data drift

### Ephemeral

**Use when**:
- Intermediate models used by only one downstream model
- Want to avoid persisting intermediate tables

**Config**:
```sql
{{
  config(
    materialized='ephemeral'
  )
}}
```

**Pros**: No storage, always up-to-date
**Cons**: Cannot query directly, recomputed in every downstream model

---

## Testing Patterns

### Generic Tests

Built-in tests for common validations:

```yaml
# models/marts/schema.yml

version: 2

models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null

      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id

      - name: order_status
        tests:
          - accepted_values:
              values: ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']

      - name: total_amount
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
              inclusive: true
```

### Singular Tests

Custom SQL tests for complex validations:

```sql
-- tests/assert_order_amount_matches_items.sql

-- Test fails if any rows are returned
select
    order_id,
    sum(item_amount) as calculated_total,
    order_amount as reported_total
from {{ ref('fct_orders') }}
group by order_id, order_amount
having abs(sum(item_amount) - order_amount) > 0.01
```

### Custom Generic Tests (Macros)

```sql
-- macros/test_is_recent.sql

{% test is_recent(model, column_name, days=7) %}

select *
from {{ model }}
where {{ column_name }} < current_date - interval '{{ days }}' day

{% endtest %}
```

Usage:
```yaml
models:
  - name: fct_orders
    columns:
      - name: order_created_at
        tests:
          - is_recent:
              days: 30
```

---

## Documentation

### Model Documentation

```yaml
# models/marts/schema.yml

models:
  - name: fct_orders
    description: "Order-level fact table with one row per order"
    columns:
      - name: order_id
        description: "Unique identifier for each order"
      - name: customer_id
        description: "Foreign key to dim_customers"
      - name: total_amount
        description: "Total order amount including tax and shipping"
```

### Inline Documentation

```sql
-- models/marts/fct_orders.sql

{{
  config(
    materialized='incremental',
    unique_key='order_id'
  )
}}

-- This model calculates order-level metrics by aggregating line items.
-- It runs incrementally to process only new orders since the last run.

with orders as (
    select * from {{ ref('stg_orders') }}
),

-- Join order items to calculate totals
order_items as (
    select * from {{ ref('stg_order_items') }}
),

aggregated as (
    select
        o.order_id,
        o.customer_id,
        o.order_created_at,
        sum(oi.item_amount) as total_amount,
        count(*) as item_count
    from orders o
    inner join order_items oi on o.order_id = oi.order_id
    group by 1, 2, 3
)

select * from aggregated

{% if is_incremental() %}
    where order_created_at > (select max(order_created_at) from {{ this }})
{% endif %}
```

### Generate Documentation

```bash
dbt docs generate
dbt docs serve
```

Access at `http://localhost:8080`

---

## Performance Optimization

### 1. Use CTEs for Readability

```sql
-- Good: Clear, maintainable
with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

joined as (
    select
        o.order_id,
        c.customer_name,
        o.total_amount
    from orders o
    left join customers c on o.customer_id = c.customer_id
)

select * from joined
```

### 2. Limit Data Early

```sql
-- Good: Filter before joins
with orders as (
    select * from {{ ref('stg_orders') }}
    where order_status != 'cancelled'  -- Filter early
),

customers as (
    select * from {{ ref('stg_customers') }}
    where is_active = true  -- Filter early
),

joined as (
    select * from orders o
    left join customers c on o.customer_id = c.customer_id
)

select * from joined
```

### 3. Use Incremental Models for Large Tables

```sql
{{
  config(
    materialized='incremental',
    unique_key='event_id',
    partition_by={'field': 'event_date', 'data_type': 'date'}
  )
}}

select * from {{ ref('stg_events') }}

{% if is_incremental() %}
    where event_date > (select max(event_date) from {{ this }})
{% endif %}
```

### 4. Partition Large Tables (BigQuery, Snowflake)

```sql
{{
  config(
    materialized='table',
    partition_by={
      'field': 'order_date',
      'data_type': 'date',
      'granularity': 'day'
    },
    cluster_by=['customer_id', 'region']
  )
}}

select * from {{ ref('stg_orders') }}
```

---

## Common Patterns

### Pattern 1: Slowly Changing Dimensions (SCD Type 2)

```sql
-- snapshots/dim_customers_snapshot.sql

{% snapshot dim_customers_snapshot %}

{{
    config(
      target_schema='snapshots',
      unique_key='customer_id',
      strategy='timestamp',
      updated_at='updated_at'
    )
}}

select * from {{ ref('stg_customers') }}

{% endsnapshot %}
```

Run with: `dbt snapshot`

### Pattern 2: Surrogate Keys

```sql
-- models/intermediate/int_orders_with_surrogate.sql

select
    {{ dbt_utils.generate_surrogate_key(['order_id', 'line_item_id']) }} as order_line_key,
    order_id,
    line_item_id,
    product_id,
    quantity
from {{ ref('stg_order_items') }}
```

### Pattern 3: Pivot Tables

```sql
-- models/intermediate/int_sales_pivoted.sql

select
    customer_id,
    sum(case when product_category = 'Electronics' then sales_amount else 0 end) as electronics_sales,
    sum(case when product_category = 'Clothing' then sales_amount else 0 end) as clothing_sales,
    sum(case when product_category = 'Food' then sales_amount else 0 end) as food_sales
from {{ ref('stg_sales') }}
group by customer_id
```

Or use dbt_utils:

```sql
{{ dbt_utils.pivot(
    'product_category',
    dbt_utils.get_column_values(ref('stg_sales'), 'product_category'),
    agg='sum',
    cmp='=',
    prefix='',
    suffix='_sales',
    then_value='sales_amount'
) }}
```

### Pattern 4: Deduplication

```sql
-- models/staging/stg_orders_deduplicated.sql

with source as (
    select * from {{ source('raw', 'orders') }}
),

deduplicated as (
    select *,
        row_number() over (
            partition by order_id
            order by updated_at desc
        ) as row_num
    from source
)

select * from deduplicated
where row_num = 1
```

---

## Macros and Packages

### Install Packages

```yaml
# packages.yml

packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: calogica/dbt_expectations
    version: 0.10.3
```

Install with: `dbt deps`

### Common Macros

**dbt_utils.star**:
```sql
select
    {{ dbt_utils.star(from=ref('stg_orders'), except=['_loaded_at']) }},
    current_timestamp() as transformed_at
from {{ ref('stg_orders') }}
```

**dbt_utils.union_relations**:
```sql
{{ dbt_utils.union_relations(
    relations=[
        ref('stg_orders_2023'),
        ref('stg_orders_2024')
    ]
) }}
```

---

## Additional Resources

- Official dbt Docs: https://docs.getdbt.com/
- dbt Style Guide: https://github.com/dbt-labs/corp/blob/main/dbt_style_guide.md
- dbt Utils Package: https://github.com/dbt-labs/dbt-utils
- dbt Discourse Community: https://discourse.getdbt.com/
