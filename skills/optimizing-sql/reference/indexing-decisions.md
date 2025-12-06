# Indexing Decisions Guide

Comprehensive framework for deciding when and how to add indexes to optimize SQL query performance.

## Table of Contents

1. [Index Decision Framework](#index-decision-framework)
2. [Index Selection Criteria](#index-selection-criteria)
3. [Single-Column vs Composite Indexes](#single-column-vs-composite-indexes)
4. [Covering Indexes](#covering-indexes)
5. [When NOT to Add Indexes](#when-not-to-add-indexes)
6. [Index Maintenance](#index-maintenance)

## Index Decision Framework

### Primary Decision Tree

```
Is column used in WHERE, JOIN, ORDER BY, or GROUP BY?
├─ YES → Is column selective (many unique values)?
│  ├─ YES → Is table frequently queried?
│  │  ├─ YES → Is table write-heavy?
│  │  │  ├─ YES → Balance read vs write performance
│  │  │  └─ NO → ADD INDEX ✅
│  │  └─ NO → Consider based on query frequency
│  └─ NO (low selectivity) → Skip index ❌
│     Exception: Partial index for specific subset
└─ NO → Skip index ❌
```

### Selectivity Assessment

**High Selectivity (Good for Indexes):**
- Primary keys (100% unique)
- Email addresses (usually unique)
- UUIDs (unique)
- User IDs (unique per user)
- Timestamps (high variety)

**Low Selectivity (Poor for Indexes):**
- Boolean fields (true/false)
- Status fields with few values (active/inactive)
- Gender fields (limited values)
- Small enum fields (<10 values)

**Selectivity Formula:**
```sql
-- PostgreSQL
SELECT
  COUNT(DISTINCT column_name)::float / COUNT(*)::float AS selectivity
FROM table_name;
```

**Guideline:** Selectivity > 0.1 (10% unique) = candidate for index

### Query Frequency Assessment

**High Frequency (Prioritize Indexing):**
- User-facing queries (every page load)
- API endpoints hit frequently
- Real-time dashboards
- Background jobs running every minute

**Medium Frequency (Evaluate Trade-offs):**
- Admin dashboards
- Reporting queries (daily/weekly)
- Batch processes (hourly)

**Low Frequency (Deprioritize Indexing):**
- Ad-hoc queries
- One-time data migrations
- Infrequent reports (monthly/quarterly)

## Index Selection Criteria

### Criteria 1: Column Usage Patterns

**WHERE Clause:**
```sql
SELECT * FROM orders WHERE customer_id = 123;
```
**Decision:** Index `customer_id` (equality filter)

**JOIN Conditions:**
```sql
SELECT * FROM orders
INNER JOIN customers ON orders.customer_id = customers.id;
```
**Decision:** Index `orders.customer_id` and `customers.id` (foreign key + primary key)

**ORDER BY:**
```sql
SELECT * FROM orders ORDER BY created_at DESC LIMIT 10;
```
**Decision:** Index `created_at DESC` (sort optimization)

**GROUP BY:**
```sql
SELECT status, COUNT(*) FROM orders GROUP BY status;
```
**Decision:** Index `status` (grouping optimization)

### Criteria 2: Table Size

| Table Size | Index Threshold | Reasoning |
|-----------|----------------|-----------|
| <1,000 rows | Skip indexes | Query planner may prefer seq scan |
| 1,000-10,000 rows | Selective indexes | Index beneficial for selective queries |
| 10,000-1M rows | Most queries | Indexes critical for performance |
| >1M rows | All frequent queries | Index essential, consider partitioning |

### Criteria 3: Write vs Read Ratio

**Read-Heavy Tables (>90% reads):**
- Aggressive indexing strategy
- Multiple indexes acceptable
- Covering indexes beneficial

**Balanced Tables (50-90% reads):**
- Moderate indexing
- Focus on most frequent queries
- Limit to 3-5 indexes per table

**Write-Heavy Tables (>50% writes):**
- Minimal indexing
- Only index critical queries
- Consider batching writes

**Write Performance Impact:**
```
Each additional index:
- INSERT: +5-10% overhead per index
- UPDATE: +5-10% overhead per affected index
- DELETE: +5-10% overhead per index
```

### Criteria 4: Data Type Considerations

**Good for Indexing:**
- Integer types (INT, BIGINT)
- UUID/GUID
- Timestamps (DATE, TIMESTAMP)
- Short strings (VARCHAR(100))

**Acceptable for Indexing:**
- Medium strings (VARCHAR(255))
- DECIMAL/NUMERIC

**Poor for Indexing:**
- Large TEXT/BLOB columns
- Very long strings (>1000 chars)
- JSON (use specialized indexes: GIN for PostgreSQL, generated columns for MySQL)

**Exception:** Full-text indexes for TEXT columns

## Single-Column vs Composite Indexes

### When to Use Single-Column Index

**Use Case 1: Single Filter**
```sql
SELECT * FROM users WHERE email = 'user@example.com';
```
**Index:**
```sql
CREATE INDEX idx_users_email ON users (email);
```

**Use Case 2: Simple JOIN**
```sql
SELECT * FROM orders
INNER JOIN customers ON orders.customer_id = customers.id;
```
**Index:**
```sql
CREATE INDEX idx_orders_customer ON orders (customer_id);
```

### When to Use Composite Index

**Use Case 1: Multiple Equality Filters**
```sql
SELECT * FROM orders
WHERE customer_id = 123 AND status = 'shipped';
```
**Index:**
```sql
CREATE INDEX idx_orders_customer_status ON orders (customer_id, status);
```

**Use Case 2: Filter + Sort**
```sql
SELECT * FROM orders
WHERE customer_id = 123
ORDER BY created_at DESC;
```
**Index:**
```sql
CREATE INDEX idx_orders_customer_created ON orders (customer_id, created_at DESC);
```

**Use Case 3: Filter + Group**
```sql
SELECT customer_id, status, COUNT(*)
FROM orders
WHERE created_at > '2025-01-01'
GROUP BY customer_id, status;
```
**Index:**
```sql
CREATE INDEX idx_orders_created_customer_status
ON orders (created_at, customer_id, status);
```

### Composite Index Column Order

**Rule of Thumb:**
1. **Equality filters** (most selective first)
2. **Range filters** (if any)
3. **ORDER BY columns** (matching sort direction)

**Example:**
```sql
SELECT * FROM orders
WHERE customer_id = 123        -- Equality (put first)
  AND status IN ('shipped', 'pending')  -- Equality (put second)
  AND total > 100              -- Range (put third)
ORDER BY created_at DESC;      -- Sort (put last)
```

**Optimal Index:**
```sql
CREATE INDEX idx_orders_customer_status_total_created
ON orders (customer_id, status, total, created_at DESC);
```

**Left-Prefix Rule:**
Composite index on (A, B, C) can be used for:
- WHERE A = ?
- WHERE A = ? AND B = ?
- WHERE A = ? AND B = ? AND C = ?

But NOT for:
- WHERE B = ? (skips leading column)
- WHERE C = ? (skips leading columns)

## Covering Indexes

### What is a Covering Index?

Index that contains ALL columns needed by query (no heap table access required).

**Benefits:**
- Fastest possible performance (Index-Only Scan)
- Reduced I/O (no heap access)
- Better cache utilization

### Creating Covering Indexes

**PostgreSQL INCLUDE Clause:**
```sql
CREATE INDEX idx_users_email_covering
ON users (email) INCLUDE (id, name, created_at);
```

**MySQL Composite Index:**
```sql
-- MySQL doesn't have INCLUDE, add columns to index
CREATE INDEX idx_users_email_id_name
ON users (email, id, name);
```

**SQL Server INCLUDE Clause:**
```sql
CREATE NONCLUSTERED INDEX IX_Users_Email_Covering
ON Users (Email)
INCLUDE (ID, Name, CreatedAt);
```

### When to Use Covering Indexes

**Use Case 1: Frequent Query with Specific Columns**
```sql
-- Query runs 1000x per second
SELECT id, name FROM users WHERE email = 'user@example.com';
```
**Covering Index:**
```sql
CREATE INDEX idx_users_email_covering ON users (email) INCLUDE (id, name);
```

**Use Case 2: API Endpoint Returning Specific Fields**
```sql
-- API: GET /api/orders?customer_id=123 (returns id, total, status)
SELECT id, total, status FROM orders WHERE customer_id = 123;
```
**Covering Index:**
```sql
CREATE INDEX idx_orders_customer_covering
ON orders (customer_id) INCLUDE (id, total, status);
```

### Covering Index Trade-offs

**Benefits:**
- Dramatic performance improvement (Index-Only Scan)
- No heap access = less I/O

**Costs:**
- Larger index size
- Slower writes (more data to update)
- More storage required

**Guideline:** Use covering indexes for critical queries (user-facing, high-frequency).

## When NOT to Add Indexes

### Anti-Pattern 1: Indexing Low-Selectivity Columns

**Bad:**
```sql
CREATE INDEX idx_users_is_active ON users (is_active);  -- ❌ Boolean
```

**Why:** Only 2 values (true/false), index scan often worse than seq scan.

**Exception:** Partial index for minority case
```sql
-- If 99% inactive, 1% active
CREATE INDEX idx_users_active ON users (id) WHERE is_active = true;
```

### Anti-Pattern 2: Indexing Small Tables

**Bad:**
```sql
CREATE INDEX idx_config_key ON config (key);  -- ❌ Table has 50 rows
```

**Why:** Small tables fit in memory, seq scan faster than index overhead.

**Guideline:** Skip indexes for tables <1000 rows (unless foreign keys).

### Anti-Pattern 3: Over-Indexing

**Bad:**
```sql
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_email_name ON users (email, name);       -- ❌ Redundant
CREATE INDEX idx_users_email_name_id ON users (email, name, id); -- ❌ Redundant
```

**Why:** Multiple overlapping indexes waste space and slow writes.

**Fix:** Use single covering index
```sql
CREATE INDEX idx_users_email_covering ON users (email) INCLUDE (name, id);
```

### Anti-Pattern 4: Indexing Write-Heavy Columns

**Bad:**
```sql
CREATE INDEX idx_pageviews_timestamp ON pageviews (timestamp);  -- ❌ High-insert table
```

**Why:** Each insert updates index, slowing down write-heavy operations.

**Alternative:** Partition table by time range, index within partitions.

### Anti-Pattern 5: Indexing Calculated Columns (Without Expression Index)

**Bad:**
```sql
-- Query uses function
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';
-- Regular index won't help
CREATE INDEX idx_users_email ON users (email);  -- ❌ Not used
```

**Fix:** Expression index (PostgreSQL, SQL Server)
```sql
CREATE INDEX idx_users_email_lower ON users (LOWER(email));
```

## Index Maintenance

### Monitoring Index Usage

**PostgreSQL:**
```sql
-- Find unused indexes
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexname NOT LIKE 'pg_toast_%'
ORDER BY idx_scan;
```

**MySQL:**
```sql
-- Enable index statistics
SELECT * FROM sys.schema_unused_indexes;
```

**SQL Server:**
```sql
-- Find unused indexes
SELECT
  OBJECT_NAME(i.object_id) AS TableName,
  i.name AS IndexName,
  s.user_seeks,
  s.user_scans,
  s.user_lookups,
  s.user_updates
FROM sys.indexes i
LEFT JOIN sys.dm_db_index_usage_stats s
  ON i.object_id = s.object_id AND i.index_id = s.index_id
WHERE s.user_seeks = 0
  AND s.user_scans = 0
  AND s.user_lookups = 0
  AND i.type_desc = 'NONCLUSTERED';
```

### Removing Unused Indexes

**Process:**
1. Identify unused indexes (0 scans over 7+ days)
2. Verify index not used for constraints
3. Drop index during low-traffic period
4. Monitor for performance regressions

**Drop Command:**
```sql
DROP INDEX idx_unused_index ON table_name;
```

### Updating Index Statistics

**PostgreSQL:**
```sql
-- Analyze entire database
ANALYZE;

-- Analyze specific table
ANALYZE table_name;
```

**MySQL:**
```sql
-- Analyze table
ANALYZE TABLE table_name;
```

**SQL Server:**
```sql
-- Update statistics
UPDATE STATISTICS table_name;

-- Update statistics for specific index
UPDATE STATISTICS table_name index_name;
```

**Schedule:** Weekly for active tables, monthly for stable tables.

### Rebuilding Fragmented Indexes

**PostgreSQL:**
```sql
-- Rebuild index (locks table)
REINDEX INDEX idx_name;

-- Rebuild concurrently (no lock)
REINDEX INDEX CONCURRENTLY idx_name;
```

**MySQL:**
```sql
-- Optimize table (rebuilds indexes)
OPTIMIZE TABLE table_name;
```

**SQL Server:**
```sql
-- Rebuild index
ALTER INDEX index_name ON table_name REBUILD;

-- Reorganize index (online, less intrusive)
ALTER INDEX index_name ON table_name REORGANIZE;
```

**When to Rebuild:**
- Fragmentation >30%
- After large batch deletes
- Query performance degrades over time

## Index Design Patterns

### Pattern 1: Foreign Key Indexing

**Rule:** Always index foreign keys.

**Example:**
```sql
CREATE TABLE orders (
  id INT PRIMARY KEY,
  customer_id INT,
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Always add this index
CREATE INDEX idx_orders_customer ON orders (customer_id);
```

**Why:** Enables efficient joins and cascading deletes.

### Pattern 2: Status + Timestamp Indexing

**Use Case:** Queries filtering by status and ordering by time.

```sql
SELECT * FROM orders
WHERE status = 'pending'
ORDER BY created_at DESC
LIMIT 10;
```

**Index:**
```sql
CREATE INDEX idx_orders_status_created
ON orders (status, created_at DESC);
```

### Pattern 3: Multi-Tenant Indexing

**Use Case:** SaaS application with tenant_id in most queries.

```sql
SELECT * FROM documents
WHERE tenant_id = 123 AND status = 'active'
ORDER BY updated_at DESC;
```

**Index:**
```sql
CREATE INDEX idx_documents_tenant_status_updated
ON documents (tenant_id, status, updated_at DESC);
```

**Rule:** Always lead with tenant_id in multi-tenant applications.

### Pattern 4: Partial Index for Subset

**Use Case:** Query only active records (minority of data).

```sql
SELECT * FROM users WHERE status = 'active';
```

**Full Index (Inefficient):**
```sql
CREATE INDEX idx_users_status ON users (status);  -- Large index
```

**Partial Index (Efficient - PostgreSQL):**
```sql
CREATE INDEX idx_users_active ON users (id)
WHERE status = 'active';  -- Smaller, faster
```

### Pattern 5: Expression Index for Case-Insensitive Search

**Use Case:** Case-insensitive email lookup.

```sql
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';
```

**Expression Index (PostgreSQL, SQL Server):**
```sql
CREATE INDEX idx_users_email_lower ON users (LOWER(email));
```

**MySQL Alternative (Generated Column):**
```sql
ALTER TABLE users ADD COLUMN email_lower VARCHAR(255)
  GENERATED ALWAYS AS (LOWER(email)) STORED;
CREATE INDEX idx_users_email_lower ON users (email_lower);
```

## Quick Reference

### Index Decision Checklist

- [ ] Column used in WHERE, JOIN, ORDER BY, or GROUP BY?
- [ ] High selectivity (>10% unique values)?
- [ ] Table size >1,000 rows?
- [ ] Query frequency high (user-facing or frequent)?
- [ ] Write-to-read ratio acceptable (<50% writes)?
- [ ] No overlapping composite indexes already exist?
- [ ] Index size acceptable (<20% of table size)?

### Index Type Selection

| Use Case | PostgreSQL | MySQL | SQL Server |
|----------|-----------|-------|------------|
| General queries | B-tree | B-tree | Non-clustered |
| Equality only | Hash | B-tree | Non-clustered |
| Full-text search | GIN | Full-text | Full-text |
| Spatial data | GiST | Spatial | Spatial |
| JSONB | GIN | Generated column + index | JSON index |
| Large sequential table | BRIN | B-tree with partitions | Clustered columnstore |

### Index Maintenance Schedule

| Task | Frequency | Purpose |
|------|-----------|---------|
| Update statistics | Weekly | Optimize query plans |
| Review unused indexes | Monthly | Remove waste |
| Rebuild fragmented indexes | Quarterly | Fix fragmentation |
| Analyze query performance | Weekly | Identify missing indexes |
