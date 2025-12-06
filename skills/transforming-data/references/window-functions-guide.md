# SQL Window Functions Guide


## Table of Contents

- [Overview](#overview)
- [Basic Syntax](#basic-syntax)
- [Common Window Functions](#common-window-functions)
  - [1. Ranking Functions](#1-ranking-functions)
  - [2. Aggregate Functions](#2-aggregate-functions)
  - [3. LAG and LEAD](#3-lag-and-lead)
- [Advanced Patterns](#advanced-patterns)
  - [Percent Change Calculation](#percent-change-calculation)
  - [First and Last Values](#first-and-last-values)
  - [Percentiles](#percentiles)
- [Frame Specifications](#frame-specifications)
  - [ROWS vs RANGE](#rows-vs-range)
- [Best Practices](#best-practices)

## Overview

Window functions perform calculations across a set of table rows related to the current row, without grouping rows into a single output row.

## Basic Syntax

```sql
<window_function>() OVER (
    PARTITION BY <columns>
    ORDER BY <columns>
    ROWS/RANGE BETWEEN <start> AND <end>
)
```

## Common Window Functions

### 1. Ranking Functions

#### ROW_NUMBER()

Assigns unique sequential numbers to rows.

```sql
select
    order_id,
    customer_id,
    order_date,
    row_number() over (
        partition by customer_id
        order by order_date
    ) as customer_order_number
from orders
```

#### RANK() and DENSE_RANK()

```sql
select
    product_id,
    sales_amount,
    rank() over (order by sales_amount desc) as rank,
    dense_rank() over (order by sales_amount desc) as dense_rank
from product_sales
```

### 2. Aggregate Functions

#### Running Totals

```sql
select
    order_date,
    daily_revenue,
    sum(daily_revenue) over (
        order by order_date
        rows between unbounded preceding and current row
    ) as cumulative_revenue
from daily_sales
```

#### Moving Averages

```sql
select
    order_date,
    daily_revenue,
    avg(daily_revenue) over (
        order by order_date
        rows between 6 preceding and current row
    ) as revenue_7day_ma
from daily_sales
```

### 3. LAG and LEAD

Access previous or next row values.

```sql
select
    order_date,
    daily_revenue,
    lag(daily_revenue, 1) over (order by order_date) as prev_day_revenue,
    lead(daily_revenue, 1) over (order by order_date) as next_day_revenue,
    daily_revenue - lag(daily_revenue, 1) over (order by order_date) as revenue_change
from daily_sales
```

## Advanced Patterns

### Percent Change Calculation

```sql
select
    order_date,
    revenue,
    (revenue / lag(revenue, 1) over (order by order_date) - 1) * 100 as pct_change
from daily_sales
```

### First and Last Values

```sql
select
    customer_id,
    order_date,
    first_value(order_date) over (
        partition by customer_id
        order by order_date
    ) as first_order_date,
    last_value(order_date) over (
        partition by customer_id
        order by order_date
        rows between unbounded preceding and unbounded following
    ) as last_order_date
from orders
```

### Percentiles

```sql
select
    customer_id,
    total_spent,
    percent_rank() over (order by total_spent) as percentile_rank,
    ntile(4) over (order by total_spent) as quartile
from customer_lifetime_value
```

## Frame Specifications

### ROWS vs RANGE

**ROWS**: Physical number of rows
**RANGE**: Logical range based on values

```sql
-- ROWS: Last 3 physical rows
sum(amount) over (
    order by date
    rows between 2 preceding and current row
)

-- RANGE: All rows with same date value
sum(amount) over (
    order by date
    range between unbounded preceding and current row
)
```

## Best Practices

1. Always use `PARTITION BY` when analyzing groups separately
2. Use `ORDER BY` to define the window frame
3. Specify frame bounds explicitly for clarity
4. Consider performance impact on large datasets
5. Use CTEs to make complex window logic readable

```sql
with daily_metrics as (
    select
        date,
        revenue,
        avg(revenue) over (
            order by date
            rows between 6 preceding and current row
        ) as ma_7day
    from sales
)
select * from daily_metrics
where ma_7day > 10000
```
