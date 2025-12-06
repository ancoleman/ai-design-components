-- models/marts/fct_orders.sql
-- Mart layer: Incremental fact table

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

with orders as (
    select * from {{ ref('int_orders_joined') }}
),

aggregated as (
    select
        order_id,
        customer_id,
        order_created_at,
        order_status,
        order_value_tier,

        -- Aggregated metrics
        sum(order_amount) as total_order_amount,
        count(*) as line_item_count,

        -- Flags
        max(case when order_status = 'returned' then 1 else 0 end) = 1 as has_return

    from orders
    group by 1, 2, 3, 4, 5
)

select * from aggregated

-- Incremental logic: only process new/updated orders
{% if is_incremental() %}
    where order_created_at > (select max(order_created_at) from {{ this }})
{% endif %}
