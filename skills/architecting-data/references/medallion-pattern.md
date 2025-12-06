# Medallion Architecture Pattern

Standard pattern for organizing data in lakehouses. Three layers of increasing data quality.


## Table of Contents

- [Three Layers](#three-layers)
  - [Bronze Layer (Raw)](#bronze-layer-raw)
  - [Silver Layer (Cleaned & Conformed)](#silver-layer-cleaned-conformed)
  - [Gold Layer (Business-Level)](#gold-layer-business-level)
- [Data Quality by Layer](#data-quality-by-layer)
- [Medallion + Data Mesh](#medallion-data-mesh)
- [Benefits](#benefits)

## Three Layers

### Bronze Layer (Raw)

**Purpose:** Exact copy of source systems; immutable historical archive

**Characteristics:**
- Append-only (never modify or delete)
- Full fidelity (all columns, all rows)
- Format: Source format or Parquet
- Retention: Forever (or years)

**Example:**
```sql
CREATE TABLE bronze.raw_customers (
  _ingested_at TIMESTAMP,
  _source_file STRING,
  _raw_data STRING  -- entire JSON/CSV blob
);
```

### Silver Layer (Cleaned & Conformed)

**Purpose:** Validated, deduplicated, typed data

**Transformations:**
- Parse JSON/XML
- Type conversions (string → int, date)
- Deduplication
- Normalized naming

**Example:**
```sql
CREATE TABLE silver.customers AS
SELECT
  json_extract_scalar(_raw_data, '$.id') AS customer_id,
  json_extract_scalar(_raw_data, '$.name') AS customer_name,
  CAST(json_extract_scalar(_raw_data, '$.revenue') AS BIGINT) AS annual_revenue,
  DATE(json_extract_scalar(_raw_data, '$.created')) AS created_date
FROM bronze.raw_customers
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY _ingested_at DESC) = 1;
```

**Data Quality Checks:**
- Primary key uniqueness
- Null checks on required fields
- Referential integrity
- Value range validation

### Gold Layer (Business-Level)

**Purpose:** Optimized for consumption (BI, ML, APIs)

**Patterns:**
- Star schemas (dimensional models)
- Wide tables (ML features)
- Aggregates (daily_sales_by_region)

**Example:**
```sql
CREATE TABLE gold.fact_sales AS
SELECT
  s.order_id,
  d.date_key,
  c.customer_key,
  p.product_key,
  s.quantity * s.unit_price AS gross_revenue,
  s.quantity * s.unit_price - s.discount_amount AS net_revenue,
  (s.quantity * s.unit_price - s.discount_amount) - (s.quantity * p.unit_cost) AS profit
FROM silver.sales s
JOIN gold.dim_date d ON s.order_date = d.date
JOIN gold.dim_customer c ON s.customer_id = c.customer_id
JOIN gold.dim_product p ON s.product_id = p.product_id;
```

## Data Quality by Layer

| Layer | Quality Checks | Purpose |
|-------|---------------|---------|
| Bronze → Silver | Schema validation, type checks, deduplication | Ensure data is parseable and unique |
| Silver → Gold | Business rule validation, referential integrity | Ensure data meets business logic |
| Gold | Anomaly detection, statistical checks | Ensure data is reasonable |

## Medallion + Data Mesh

Each domain owns bronze-silver-gold for their data products:

```
Sales Domain:
  bronze.sales_raw
  silver.sales_cleaned
  gold.sales_analytics (data product)

Marketing Domain:
  bronze.marketing_raw
  silver.marketing_cleaned
  gold.marketing_analytics (data product)

Cross-Domain:
  gold.customer_360 (combines sales + marketing)
```

## Benefits

- Clear separation of concerns
- Reprocessing at any layer
- Incremental quality improvement
- Standard pattern across organization
