# Incremental Loading Strategies


## Table of Contents

- [Overview](#overview)
- [dbt Incremental Strategies](#dbt-incremental-strategies)
  - [1. Append Strategy (Default)](#1-append-strategy-default)
  - [2. Merge Strategy](#2-merge-strategy)
  - [3. Insert Overwrite Strategy](#3-insert-overwrite-strategy)
- [Python Incremental Patterns](#python-incremental-patterns)
  - [State Tracking with Checkpoints](#state-tracking-with-checkpoints)
  - [Watermark-Based Loading](#watermark-based-loading)
- [Best Practices](#best-practices)
- [Common Issues](#common-issues)

## Overview

Incremental loading processes only new or changed data since the last run, improving performance and reducing costs for large datasets.

## dbt Incremental Strategies

### 1. Append Strategy (Default)

Insert new rows only, no updates to existing rows.

```sql
{{
  config(
    materialized='incremental',
    unique_key='event_id'
  )
}}

select
    event_id,
    user_id,
    event_type,
    event_timestamp
from {{ ref('stg_events') }}

{% if is_incremental() %}
    where event_timestamp > (select max(event_timestamp) from {{ this }})
{% endif %}
```

**Use for**: Immutable event streams, logs, clickstreams

### 2. Merge Strategy

Update existing rows and insert new rows (upsert).

```sql
{{
  config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    merge_update_columns=['order_status', 'updated_at']
  )
}}

select
    order_id,
    customer_id,
    order_status,
    total_amount,
    updated_at
from {{ ref('stg_orders') }}

{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

**Use for**: Mutable data with updates (orders, customer profiles)

### 3. Insert Overwrite Strategy

Replace data for specific partitions only.

```sql
{{
  config(
    materialized='incremental',
    unique_key='date',
    incremental_strategy='insert_overwrite',
    partition_by={'field': 'date', 'data_type': 'date'}
  )
}}

select
    date_trunc('day', event_timestamp) as date,
    count(*) as event_count
from {{ ref('stg_events') }}
group by 1

{% if is_incremental() %}
    where date_trunc('day', event_timestamp) >= current_date - interval '7' day
{% endif %}
```

**Use for**: Partitioned data, reprocessing specific dates

## Python Incremental Patterns

### State Tracking with Checkpoints

```python
import polars as pl
from datetime import datetime

def incremental_load():
    # Load last checkpoint
    last_timestamp = read_checkpoint('last_load_timestamp')

    # Extract only new data
    new_data = (
        pl.scan_parquet('s3://bucket/data/*.parquet')
        .filter(pl.col('created_at') > last_timestamp)
        .collect()
    )

    # Process and load
    transform_and_load(new_data)

    # Save new checkpoint
    save_checkpoint('last_load_timestamp', datetime.now())
```

### Watermark-Based Loading

```python
def load_with_watermark():
    # Get high watermark from target table
    high_watermark = get_max_value('target_table', 'updated_at')

    # Extract data above watermark
    new_data = extract_from_source(f"WHERE updated_at > '{high_watermark}'")

    # Merge into target
    merge_data('target_table', new_data, on='id')
```

## Best Practices

1. **Always use unique_key** for merge strategies
2. **Partition large tables** for efficient overwrites
3. **Test full-refresh** periodically to validate incremental logic
4. **Monitor data drift** between incremental and full loads
5. **Use lookback windows** to catch late-arriving data

```sql
-- Lookback window for late data
{% if is_incremental() %}
    where updated_at > (select max(updated_at) - interval '3' day from {{ this }})
{% endif %}
```

## Common Issues

**Issue**: Data drift between incremental and full refresh
**Solution**: Schedule periodic full refreshes (`dbt run --full-refresh`)

**Issue**: Late-arriving data missed
**Solution**: Use lookback window (process last N days each run)

**Issue**: Duplicate data from multiple runs
**Solution**: Use `unique_key` with merge strategy
