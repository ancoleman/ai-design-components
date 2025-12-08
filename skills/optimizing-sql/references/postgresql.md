# PostgreSQL-Specific Optimizations

PostgreSQL-specific features, index types, and optimization techniques.

## PostgreSQL Index Types

### B-tree (Default)

**Use Case:** General-purpose index for most queries.

**Supported Operators:** <, ≤, =, ≥, >, BETWEEN, IN, IS NULL, IS NOT NULL

**Creation:**
```sql
CREATE INDEX idx_users_email ON users (email);
-- Or explicitly:
CREATE INDEX idx_users_email ON users USING BTREE (email);
```

### Hash

**Use Case:** Equality comparisons only (=).

**Benefits:** Faster than B-tree for equality, smaller index size.

**Limitations:** Only supports =, no range queries.

**Creation:**
```sql
CREATE INDEX idx_users_email_hash ON users USING HASH (email);
```

**When to Use:** High-frequency equality lookups only.

### GIN (Generalized Inverted Index)

**Use Case:** Full-text search, JSONB, arrays, composite types.

**Supported Types:**
- JSONB documents
- Arrays
- Full-text search (tsvector)
- hstore

**Full-Text Search:**
```sql
-- Create GIN index on tsvector
CREATE INDEX idx_articles_content_fts
ON articles USING GIN (to_tsvector('english', content));

-- Query
SELECT * FROM articles
WHERE to_tsvector('english', content) @@ to_tsquery('english', 'postgres & optimization');
```

**JSONB:**
```sql
-- Create GIN index on JSONB column
CREATE INDEX idx_users_metadata ON users USING GIN (metadata);

-- Query with containment
SELECT * FROM users WHERE metadata @> '{"premium": true}';

-- Query with existence
SELECT * FROM users WHERE metadata ? 'premium';
```

**Arrays:**
```sql
-- Create GIN index on array column
CREATE INDEX idx_products_tags ON products USING GIN (tags);

-- Query with array overlap
SELECT * FROM products WHERE tags && ARRAY['electronics', 'sale'];

-- Query with array contains
SELECT * FROM products WHERE tags @> ARRAY['electronics'];
```

### GiST (Generalized Search Tree)

**Use Case:** Spatial data, ranges, full-text search, geometric types.

**Geometric Types:**
```sql
-- Create GiST index on geometry column
CREATE INDEX idx_locations_point ON locations USING GIST (point);

-- Query with spatial operators
SELECT * FROM locations
WHERE point <-> POINT(40.7128, -74.0060) < 10;  -- Within 10 units
```

**Range Types:**
```sql
-- Create GiST index on date range
CREATE INDEX idx_bookings_dates ON bookings USING GIST (date_range);

-- Query with range overlap
SELECT * FROM bookings
WHERE date_range && '[2025-01-01,2025-01-31)'::daterange;
```

### BRIN (Block Range Index)

**Use Case:** Very large tables (100GB+) with naturally ordered data.

**Benefits:**
- Tiny index size (1000x smaller than B-tree)
- Very fast to build
- Minimal maintenance overhead

**Limitations:**
- Only efficient for ordered data (timestamps, sequential IDs)
- Less precise than B-tree (may scan extra blocks)

**Creation:**
```sql
-- BRIN index on timestamp column
CREATE INDEX idx_logs_created_brin ON logs USING BRIN (created_at);
```

**When to Use:**
- Tables >100GB
- Naturally ordered data (append-only logs, time-series)
- Insert-heavy workloads

**Performance:**
```
B-tree index on 1TB table: ~50GB index size
BRIN index on 1TB table: ~50MB index size
```

## PostgreSQL-Specific Features

### Partial Indexes

**Use Case:** Index only subset of rows matching condition.

**Benefits:**
- Smaller index size
- Faster index scans
- Lower maintenance overhead

**Example 1: Index Active Users Only**
```sql
CREATE INDEX idx_users_active
ON users (last_login)
WHERE status = 'active';
```

**Example 2: Index Recent Orders**
```sql
CREATE INDEX idx_orders_recent
ON orders (created_at)
WHERE created_at > NOW() - INTERVAL '90 days';
```

**When to Use:**
- Queries frequently filter on same condition
- Minority of rows match condition (<20%)

### Expression Indexes

**Use Case:** Index computed values or function results.

**Example 1: Case-Insensitive Search**
```sql
CREATE INDEX idx_users_email_lower ON users (LOWER(email));

-- Query must use same expression
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';
```

**Example 2: Date Truncation**
```sql
CREATE INDEX idx_orders_created_date ON orders (DATE(created_at));

-- Query for specific date
SELECT * FROM orders WHERE DATE(created_at) = '2025-01-15';
```

**Example 3: JSONB Path**
```sql
CREATE INDEX idx_users_premium ON users ((metadata->>'premium'));

SELECT * FROM users WHERE metadata->>'premium' = 'true';
```

### Covering Indexes (INCLUDE Clause)

**Use Case:** Include non-indexed columns in index for Index-Only Scans.

**Syntax:**
```sql
CREATE INDEX idx_users_email_covering
ON users (email) INCLUDE (id, name, created_at);
```

**Query Benefits:**
```sql
-- This query uses Index-Only Scan (no heap access)
SELECT id, name, created_at
FROM users
WHERE email = 'user@example.com';
```

**Performance:**
```
Without INCLUDE: Index Scan + Heap Fetch = 10ms
With INCLUDE: Index-Only Scan = 1ms
```

### Concurrent Index Creation

**Use Case:** Create indexes on production tables without blocking writes.

**Standard Index Creation (Locks Table):**
```sql
CREATE INDEX idx_users_email ON users (email);
-- Blocks all writes until complete
```

**Concurrent Index Creation (No Lock):**
```sql
CREATE INDEX CONCURRENTLY idx_users_email ON users (email);
-- Allows concurrent writes, takes longer
```

**Trade-offs:**
- Slower to build (multiple table scans)
- No table lock (production-safe)
- Can fail mid-build (index marked INVALID)

**Cleanup Failed Index:**
```sql
-- List invalid indexes
SELECT indexname FROM pg_indexes WHERE indexname LIKE '%_ccnew%';

-- Drop invalid index
DROP INDEX CONCURRENTLY idx_users_email;
```

## PostgreSQL Execution Plan Analysis

### EXPLAIN ANALYZE with Buffers

**Basic EXPLAIN ANALYZE:**
```sql
EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 123;
```

**With Buffer Statistics:**
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE customer_id = 123;
```

**Output:**
```
Index Scan using idx_orders_customer on orders
  (cost=0.42..12.44 rows=10 width=200)
  (actual time=0.025..0.035 rows=10 loops=1)
  Index Cond: (customer_id = 123)
  Buffers: shared hit=5
Planning Time: 0.150 ms
Execution Time: 0.050 ms
```

**Buffer Analysis:**
- **shared hit**: Pages read from cache (good)
- **shared read**: Pages read from disk (slow)
- **shared dirtied**: Pages modified
- **shared written**: Pages written to disk

**Goal:** Maximize "shared hit", minimize "shared read".

### EXPLAIN Options

```sql
-- Verbose output (column list, table aliases)
EXPLAIN (VERBOSE) SELECT ...;

-- Show costs without execution
EXPLAIN SELECT ...;

-- Execute and show actual timing
EXPLAIN ANALYZE SELECT ...;

-- Show buffer usage
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;

-- Show detailed timing per node
EXPLAIN (ANALYZE, TIMING) SELECT ...;

-- Machine-readable JSON format
EXPLAIN (ANALYZE, FORMAT JSON) SELECT ...;
```

## PostgreSQL Query Optimization

### Parallel Query Execution

**Enable Parallel Queries:**
```sql
-- Check parallel workers setting
SHOW max_parallel_workers_per_gather;

-- Set parallel workers for session
SET max_parallel_workers_per_gather = 4;
```

**Parallel Seq Scan:**
```sql
EXPLAIN SELECT COUNT(*) FROM large_table;
```
```
Finalize Aggregate  (cost=xxx rows=1)
  -> Gather  (cost=xxx rows=4)
        Workers Planned: 4
        -> Partial Aggregate
              -> Parallel Seq Scan on large_table
```

**Force Parallel Execution:**
```sql
-- Lower threshold for parallel scans
SET parallel_setup_cost = 0;
SET parallel_tuple_cost = 0;
```

### Common Table Expressions (CTEs)

**Materialized CTEs (Default in PostgreSQL 12+):**
```sql
-- CTE is inline-optimized (not materialized)
WITH recent_orders AS (
  SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '7 days'
)
SELECT * FROM recent_orders WHERE total > 100;
```

**Force Materialization:**
```sql
-- Explicitly materialize CTE
WITH recent_orders AS MATERIALIZED (
  SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '7 days'
)
SELECT * FROM recent_orders WHERE total > 100;
```

**When to Materialize:**
- CTE used multiple times in main query
- CTE is expensive and produces small result set

### LATERAL Joins

**Use Case:** Correlated subqueries with better performance.

**Without LATERAL (Correlated Subquery):**
```sql
SELECT
  u.name,
  (SELECT COUNT(*) FROM orders WHERE orders.user_id = u.id) AS order_count
FROM users u;
```

**With LATERAL:**
```sql
SELECT
  u.name,
  o.order_count
FROM users u
LEFT JOIN LATERAL (
  SELECT COUNT(*) AS order_count
  FROM orders
  WHERE orders.user_id = u.id
) o ON true;
```

**Advanced LATERAL (Top N per Group):**
```sql
-- Get 3 most recent orders per customer
SELECT
  c.name,
  o.order_date,
  o.total
FROM customers c
LEFT JOIN LATERAL (
  SELECT order_date, total
  FROM orders
  WHERE customer_id = c.id
  ORDER BY order_date DESC
  LIMIT 3
) o ON true;
```

## PostgreSQL Configuration Tuning

### Memory Settings

**shared_buffers:**
```sql
-- 25% of system RAM (typical recommendation)
ALTER SYSTEM SET shared_buffers = '4GB';
```

**work_mem:**
```sql
-- Memory per sort/hash operation
-- Set per session for complex queries
SET work_mem = '256MB';
```

**effective_cache_size:**
```sql
-- Estimate of OS file cache
-- 50-75% of system RAM
ALTER SYSTEM SET effective_cache_size = '12GB';
```

### Query Planning

**random_page_cost:**
```sql
-- Lower for SSDs (default 4.0)
ALTER SYSTEM SET random_page_cost = 1.1;
```

**effective_io_concurrency:**
```sql
-- Number of concurrent I/O operations
-- Higher for SSDs (default 1)
ALTER SYSTEM SET effective_io_concurrency = 200;
```

### Statistics

**default_statistics_target:**
```sql
-- Increase for better query planning (default 100)
ALTER SYSTEM SET default_statistics_target = 500;

-- Per-column statistics
ALTER TABLE orders ALTER COLUMN customer_id SET STATISTICS 1000;
```

## PostgreSQL Monitoring

### Find Slow Queries

**Enable slow query logging:**
```sql
-- Log queries slower than 100ms
ALTER SYSTEM SET log_min_duration_statement = 100;
SELECT pg_reload_conf();
```

### Index Usage Statistics

**Find unused indexes:**
```sql
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan,
  pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexname NOT LIKE 'pg_toast_%'
ORDER BY pg_relation_size(indexrelid) DESC;
```

**Find most used indexes:**
```sql
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC
LIMIT 20;
```

### Table Statistics

**Update statistics:**
```sql
-- Analyze entire database
ANALYZE;

-- Analyze specific table
ANALYZE orders;

-- Verbose output
ANALYZE VERBOSE orders;
```

**View table statistics:**
```sql
SELECT
  schemaname,
  tablename,
  n_live_tup AS live_rows,
  n_dead_tup AS dead_rows,
  last_vacuum,
  last_autovacuum,
  last_analyze,
  last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;
```

## Quick Reference

### Index Type Selection

| Use Case | Index Type | Creation |
|----------|-----------|----------|
| General queries | B-tree | `CREATE INDEX ON table (column)` |
| Equality only | Hash | `CREATE INDEX ON table USING HASH (column)` |
| Full-text search | GIN | `CREATE INDEX ON table USING GIN (to_tsvector('english', column))` |
| JSONB | GIN | `CREATE INDEX ON table USING GIN (jsonb_column)` |
| Arrays | GIN | `CREATE INDEX ON table USING GIN (array_column)` |
| Spatial data | GiST | `CREATE INDEX ON table USING GIST (geometry_column)` |
| Large ordered tables | BRIN | `CREATE INDEX ON table USING BRIN (timestamp_column)` |

### PostgreSQL-Specific Optimizations

- Use **partial indexes** for frequently-filtered subsets
- Use **expression indexes** for computed values
- Use **INCLUDE** clause for covering indexes
- Use **LATERAL** for efficient correlated subqueries
- Use **BRIN** for very large time-series tables
- Create indexes **CONCURRENTLY** on production tables
