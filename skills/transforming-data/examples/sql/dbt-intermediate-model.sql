-- models/intermediate/int_orders_joined.sql
-- Intermediate layer: Business logic, not exposed to end users

{{
  config(
    materialized='ephemeral',
    tags=['intermediate']
  )
}}

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
        -- Order details
        o.order_id,
        o.customer_id,
        o.order_created_at,
        o.order_status,
        o.order_amount,

        -- Customer attributes
        c.customer_email,
        c.customer_segment,
        c.customer_created_at,

        -- Product attributes
        p.product_name,
        p.category,
        p.brand,

        -- Derived business logic
        case
            when o.order_amount >= 1000 then 'high_value'
            when o.order_amount >= 500 then 'medium_value'
            else 'standard'
        end as order_value_tier,

        case
            when c.customer_segment = 'vip' then 0.15
            when c.customer_segment = 'premium' then 0.10
            else 0.05
        end as loyalty_discount_rate

    from orders o
    left join customers c on o.customer_id = c.customer_id
    left join products p on o.product_id = p.product_id
)

select * from joined
