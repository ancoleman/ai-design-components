-- models/staging/stg_orders.sql
-- Staging layer: 1:1 with source, minimal transformations

{{
  config(
    materialized='view',
    tags=['staging', 'daily']
  )
}}

with source as (
    select * from {{ source('ecommerce', 'raw_orders') }}
),

renamed as (
    select
        -- IDs
        order_id,
        customer_id,
        product_id,

        -- Timestamps (standardize naming)
        created_at as order_created_at,
        updated_at as order_updated_at,

        -- Metrics (cast to correct types)
        cast(total_amount as decimal(18,2)) as order_amount,
        cast(tax_amount as decimal(18,2)) as tax_amount,
        cast(quantity as integer) as quantity,

        -- Dimensions (clean and standardize)
        lower(trim(status)) as order_status,
        lower(trim(payment_method)) as payment_method,

        -- Metadata
        _loaded_at

    from source

    -- Basic data quality filtering
    where order_id is not null
      and customer_id is not null
      and created_at is not null
)

select * from renamed
