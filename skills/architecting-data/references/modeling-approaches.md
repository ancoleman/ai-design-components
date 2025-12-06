# Data Modeling Approaches

## Table of Contents

1. [Dimensional Modeling (Kimball)](#dimensional-modeling-kimball)
2. [Normalized Modeling (Inmon)](#normalized-modeling-inmon)
3. [Data Vault 2.0](#data-vault-20)
4. [Wide Tables (Denormalized)](#wide-tables-denormalized)

---

## Dimensional Modeling (Kimball)

### Overview

Optimized for analytical queries and business intelligence. Organizes data into fact tables (metrics) and dimension tables (context).

### Star Schema Design Process

**Step 1: Identify Business Process**
- Example: "Analyze product sales performance"
- Focus on measurable business events

**Step 2: Declare Grain**
- Grain = level of detail in fact table
- Examples: "one row per order line item" or "one row per daily sales summary"
- **Critical:** Grain must be specific and consistent

**Step 3: Identify Dimensions (Context)**
- **Who:** Customer, Salesperson
- **What:** Product, Promotion
- **When:** Date, Time
- **Where:** Store, Location
- **How:** Payment Method
- **Why:** Campaign, Channel

**Step 4: Identify Facts (Measures)**
- Quantity Sold
- Unit Price
- Discount Amount
- Net Revenue
- Cost
- Profit

### Star Schema Example

```
DimDate                DimProduct              DimCustomer
- DateKey (PK)         - ProductKey (PK)       - CustomerKey (PK)
- Date                 - ProductID             - CustomerID
- DayOfWeek            - ProductName           - CustomerName
- Month                - Category              - Segment
- Quarter              - Brand                 - Country
- Year                 - UnitCost              - JoinDate
           \                 |                 /
            \                |                /
             \               |               /
              \              |              /
               \             |             /
                \            |            /
                 FactSales (Fact Table)
                 - SalesKey (PK, surrogate)
                 - DateKey (FK)
                 - ProductKey (FK)
                 - CustomerKey (FK)
                 - StoreKey (FK)
                 - Quantity
                 - UnitPrice
                 - DiscountAmount
                 - NetRevenue
```

### Slowly Changing Dimensions (SCD)

**Type 1: Overwrite (No History)**
```sql
-- Update customer segment
UPDATE DimCustomer
SET Segment = 'Premium'
WHERE CustomerID = 12345;

-- Old value lost, no history
```

**Use When:** History doesn't matter (typo corrections, insignificant changes)

---

**Type 2: Add Row (Full History)**
```sql
-- Current record
INSERT INTO DimCustomer (CustomerKey, CustomerID, Name, Segment, EffectiveDate, EndDate, IsCurrent)
VALUES (98765, 12345, 'John Doe', 'Premium', '2025-01-01', '9999-12-31', TRUE);

-- When segment changes
UPDATE DimCustomer SET EndDate = '2025-06-30', IsCurrent = FALSE WHERE CustomerKey = 98765;
INSERT INTO DimCustomer (CustomerKey, CustomerID, Name, Segment, EffectiveDate, EndDate, IsCurrent)
VALUES (98766, 12345, 'John Doe', 'VIP', '2025-07-01', '9999-12-31', TRUE);
```

**Query Pattern:**
```sql
-- Current customers
SELECT * FROM DimCustomer WHERE IsCurrent = TRUE;

-- Historical customers at specific date
SELECT * FROM DimCustomer
WHERE '2025-03-15' BETWEEN EffectiveDate AND EndDate;
```

**Use When:** Full history is critical (customer address, product pricing, employee roles)

---

**Type 3: Add Column (Limited History)**
```sql
ALTER TABLE DimCustomer
ADD COLUMN PreviousSegment VARCHAR(50);

-- Track current and previous
UPDATE DimCustomer
SET PreviousSegment = Segment, Segment = 'VIP'
WHERE CustomerID = 12345;
```

**Use When:** Need to compare current vs previous (not full history)

---

**Type 6: Hybrid (1+2+3)**
Combines Type 2 (full history) with Type 1 (current value in all rows).

```sql
CREATE TABLE DimCustomer (
  CustomerKey BIGINT PRIMARY KEY,
  CustomerID BIGINT,
  Name VARCHAR(100),
  CurrentSegment VARCHAR(50),      -- Type 1: Always current
  HistoricalSegment VARCHAR(50),   -- Type 2: Historical value
  EffectiveDate DATE,              -- Type 2
  EndDate DATE,                    -- Type 2
  IsCurrent BOOLEAN                -- Type 2
);

-- All rows show current segment, but history preserved
```

**Use When:** Need both point-in-time history and current value for all historical rows

### When to Use Dimensional Modeling

**Ideal Scenarios:**
- Business intelligence and reporting
- Known query patterns (dashboards, KPIs)
- Historical trend analysis
- User-friendly for SQL analysts
- BI tools (Tableau, Power BI, Looker)

**Trade-Offs:**
- ✅ Fast analytical queries (denormalized, few joins)
- ✅ Intuitive for business users
- ✅ Optimized for BI tools
- ❌ Inflexible to schema changes
- ❌ Denormalization creates redundancy
- ❌ Requires upfront modeling effort

---

## Normalized Modeling (Inmon)

### Overview

Eliminate redundancy and ensure data integrity through normalization (3NF, BCNF). Designed for transactional systems (OLTP).

### Normal Forms

**1st Normal Form (1NF):**
- Atomic values (no repeating groups)
- Each column contains single value

**2nd Normal Form (2NF):**
- 1NF + No partial dependencies
- Non-key attributes depend on entire primary key

**3rd Normal Form (3NF):**
- 2NF + No transitive dependencies
- Non-key attributes depend only on primary key (not other non-key attributes)

**Boyce-Codd Normal Form (BCNF):**
- Stricter version of 3NF
- Every determinant is a candidate key

### Normalized Example (3NF)

```
Customers Table
- CustomerID (PK)
- CustomerName
- Email
- PhoneNumber

Orders Table
- OrderID (PK)
- CustomerID (FK)
- OrderDate
- TotalAmount

OrderLines Table
- OrderLineID (PK)
- OrderID (FK)
- ProductID (FK)
- Quantity
- UnitPrice

Products Table
- ProductID (PK)
- ProductName
- CategoryID (FK)
- UnitCost

Categories Table
- CategoryID (PK)
- CategoryName
```

### When to Use Normalized Modeling

**Ideal Scenarios:**
- Transactional systems (OLTP)
- Data with frequent updates
- Strong consistency requirements
- Source systems feeding data warehouse

**Trade-Offs:**
- ✅ No redundancy (DRY principle)
- ✅ Data integrity enforced
- ✅ Flexible to changes
- ❌ Complex joins slow analytical queries
- ❌ Not intuitive for business users
- ❌ Poor performance for BI

---

## Data Vault 2.0

### Overview

Flexible, auditable, scalable model for enterprise data warehouses. Designed for compliance, multi-source integration, and agile requirements.

### Core Structures

**Hubs: Unique Business Keys**
```sql
CREATE TABLE HubCustomer (
  CustomerHashKey BINARY(20) PRIMARY KEY,  -- Hash of CustomerID
  CustomerID VARCHAR(50),                  -- Business key
  LoadDate TIMESTAMP,
  RecordSource VARCHAR(50)
);

-- Immutable (never deleted)
-- No descriptive attributes
```

**Links: Relationships Between Hubs**
```sql
CREATE TABLE LinkOrder (
  OrderHashKey BINARY(20) PRIMARY KEY,    -- Hash of OrderID
  CustomerHashKey BINARY(20),             -- FK to HubCustomer
  ProductHashKey BINARY(20),              -- FK to HubProduct
  OrderID VARCHAR(50),                    -- Business key
  LoadDate TIMESTAMP,
  RecordSource VARCHAR(50),
  FOREIGN KEY (CustomerHashKey) REFERENCES HubCustomer(CustomerHashKey),
  FOREIGN KEY (ProductHashKey) REFERENCES HubProduct(ProductHashKey)
);

-- Represents transactions or associations
```

**Satellites: Descriptive Attributes**
```sql
CREATE TABLE SatCustomer (
  CustomerHashKey BINARY(20),             -- FK to HubCustomer
  LoadDate TIMESTAMP,                     -- Part of PK
  EndDate TIMESTAMP,
  CustomerName VARCHAR(100),
  Email VARCHAR(100),
  Phone VARCHAR(20),
  Address VARCHAR(200),
  RecordSource VARCHAR(50),
  PRIMARY KEY (CustomerHashKey, LoadDate),
  FOREIGN KEY (CustomerHashKey) REFERENCES HubCustomer(CustomerHashKey)
);

-- Temporal (tracks changes over time)
-- Multiple satellites per hub (source-specific)
```

### Query Pattern (Join Hubs, Links, Satellites)

```sql
-- Reconstruct customer orders (current state)
SELECT
  hc.CustomerID,
  sc.CustomerName,
  sc.Email,
  lo.OrderID,
  hp.ProductID,
  sp.ProductName
FROM HubCustomer hc
JOIN SatCustomer sc ON hc.CustomerHashKey = sc.CustomerHashKey
  AND sc.EndDate = '9999-12-31'  -- Current record
JOIN LinkOrder lo ON hc.CustomerHashKey = lo.CustomerHashKey
JOIN HubProduct hp ON lo.ProductHashKey = hp.ProductHashKey
JOIN SatProduct sp ON hp.ProductHashKey = sp.ProductHashKey
  AND sp.EndDate = '9999-12-31';  -- Current record
```

### When to Use Data Vault

**Ideal Scenarios:**
- Compliance requirements (full audit trail)
- Multiple source systems with overlapping data
- Agile warehousing (requirements change frequently)
- Long-term historical archive

**Trade-Offs:**
- ✅ Highly flexible (easy to add sources)
- ✅ Complete audit trail
- ✅ Parallel loading (hubs, links, satellites independent)
- ❌ Complex queries (many joins)
- ❌ Requires data mart layer for BI
- ❌ Storage overhead

---

## Wide Tables (Denormalized)

### Overview

Single table with hundreds of pre-joined columns. Optimized for columnar storage and query performance.

### Example: Customer Feature Table (ML)

```sql
CREATE TABLE CustomerFeatures (
  -- Identity
  customer_id BIGINT PRIMARY KEY,
  created_at DATE,

  -- Demographics
  age INT,
  gender VARCHAR(10),
  country VARCHAR(50),
  segment VARCHAR(50),

  -- Behavioral (Last 30 Days)
  total_purchases_last_30d INT,
  total_revenue_last_30d DECIMAL(10,2),
  avg_order_value_last_30d DECIMAL(10,2),
  days_since_last_purchase INT,

  -- Behavioral (Last 90 Days)
  total_purchases_last_90d INT,
  total_revenue_last_90d DECIMAL(10,2),

  -- Lifetime
  total_purchases_lifetime INT,
  total_revenue_lifetime DECIMAL(10,2),
  tenure_days INT,
  customer_lifetime_value DECIMAL(10,2),

  -- Product Affinity (100+ category columns)
  purchases_category_electronics INT,
  purchases_category_clothing INT,
  -- ... 100+ more category columns

  -- Predictions
  churn_risk_score DECIMAL(3,2),
  next_purchase_days INT,

  -- Metadata
  last_updated TIMESTAMP
);
```

### Optimization Techniques

**1. Columnar Storage (Parquet, ORC):**
```python
# Write as Parquet (columnar format)
df.write.parquet("s3://bucket/customer_features.parquet")

# Only read needed columns
spark.read.parquet("s3://bucket/customer_features.parquet") \
  .select("customer_id", "churn_risk_score", "total_revenue_lifetime")

# Reads only 3 columns, not all 100+
```

**2. Partitioning:**
```sql
CREATE TABLE CustomerFeatures (
  customer_id BIGINT,
  segment VARCHAR(50),
  -- ... 100+ columns
  last_updated DATE
)
PARTITIONED BY (segment, last_updated);

-- Prune partitions
SELECT * FROM CustomerFeatures
WHERE segment = 'VIP' AND last_updated = '2025-01-01';
```

**3. Clustering:**
```sql
-- Snowflake clustering
ALTER TABLE CustomerFeatures
CLUSTER BY (customer_id, segment);

-- Co-locate related data for faster joins/filters
```

**4. Materialized Views:**
```sql
-- Pre-compute aggregates
CREATE MATERIALIZED VIEW CustomerSummary AS
SELECT
  segment,
  COUNT(*) AS customer_count,
  AVG(total_revenue_lifetime) AS avg_ltv,
  AVG(churn_risk_score) AS avg_churn_risk
FROM CustomerFeatures
GROUP BY segment;

-- Auto-refresh on base table changes
```

### When to Use Wide Tables

**Ideal Scenarios:**
- ML feature stores
- Data science notebooks (exploratory analysis)
- High-performance dashboards
- Columnar databases (Snowflake, BigQuery, Redshift)

**Trade-Offs:**
- ✅ Fastest analytical queries (no joins)
- ✅ Simple for users (one table)
- ✅ Efficient in columnar storage (only read needed columns)
- ❌ Significant redundancy
- ❌ Large storage footprint
- ❌ Update complexity (many columns to maintain)

---

## Modeling Approach Comparison

| Factor | Dimensional | Normalized | Data Vault | Wide Tables |
|--------|-------------|------------|------------|-------------|
| **Primary Use Case** | BI/Reporting | OLTP | Compliance | ML/Data Science |
| **Query Performance** | Fast | Slow | Slow | Fastest |
| **Storage Efficiency** | Medium | Best | Medium | Worst |
| **Update Complexity** | Medium | Low | Low | High |
| **Historical Tracking** | SCD Types | Difficult | Excellent | Medium |
| **Schema Flexibility** | Low | Medium | High | Low |
| **Learning Curve** | Medium | Low | High | Low |
| **Governance** | Medium | Medium | Excellent | Low |

### Hybrid Approaches

**1. Data Vault + Dimensional (Common Pattern):**
```
Source Systems
  → Data Vault (Integration Layer, full history, audit)
  → Dimensional (Presentation Layer, star schemas for BI)
  → BI Tools
```

**Benefits:** Flexibility of Data Vault + performance of dimensional models

---

**2. Dimensional + Wide Tables:**
```
Dimensional Model (Star Schema)
  → Wide Tables (ML Feature Tables)
  → ML Models
```

**Benefits:** BI on dimensional, ML on denormalized features

---

**3. Normalized (OLTP) + Dimensional (OLAP):**
```
Transactional Database (3NF)
  → ETL/ELT
  → Data Warehouse (Dimensional)
  → BI Tools
```

**Benefits:** Classic separation of transactional and analytical workloads
