-- models/staging/stg_customers.sql
-- Bronze → Silver transformation

WITH source AS (
  SELECT * FROM {{ source('raw', 'customers') }}
),

cleaned AS (
  SELECT
    customer_id,
    UPPER(customer_name) AS customer_name,
    LOWER(email) AS email,
    TRIM(phone) AS phone,
    created_at,
    updated_at
  FROM source
  WHERE customer_id IS NOT NULL
)

SELECT * FROM cleaned
