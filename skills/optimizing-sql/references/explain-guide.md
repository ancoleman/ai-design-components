# EXPLAIN Analysis Guide

Comprehensive guide to interpreting execution plans across PostgreSQL, MySQL, and SQL Server.

## Table of Contents

1. [PostgreSQL EXPLAIN](#postgresql-explain)
2. [MySQL EXPLAIN](#mysql-explain)
3. [SQL Server Execution Plans](#sql-server-execution-plans)
4. [Key Metrics to Monitor](#key-metrics-to-monitor)
5. [Common Patterns and Solutions](#common-patterns-and-solutions)

## PostgreSQL EXPLAIN

### Basic EXPLAIN Syntax

**EXPLAIN** - Show query plan without execution:
```sql
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';
```

**EXPLAIN ANALYZE** - Execute query and show actual timing:
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';
```

**EXPLAIN (ANALYZE, BUFFERS)** - Include buffer usage:
```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE email = 'user@example.com';
```

### Reading PostgreSQL Output

**Example Output:**
```
Seq Scan on users  (cost=0.00..1500.00 rows=1 width=100) (actual time=50.123..50.124 rows=1 loops=1)
  Filter: (email = 'user@example.com'::text)
  Rows Removed by Filter: 99999
Planning Time: 0.100 ms
Execution Time: 50.150 ms
```

**Key Components:**

- **Operation**: `Seq Scan` (scan type)
- **Table**: `users` (table being scanned)
- **cost=0.00..1500.00**: Estimated cost range (startup..total)
- **rows=1**: Estimated rows returned
- **width=100**: Average row size in bytes
- **actual time=50.123..50.124**: Actual time range (milliseconds)
- **rows=1**: Actual rows returned
- **loops=1**: Number of times operation executed

**Cost Interpretation:**
- Cost is arbitrary units (not milliseconds)
- Compare relative costs between plans
- Lower cost = better (usually)

### PostgreSQL Scan Types

**Sequential Scan (Seq Scan):**
- Reads entire table from disk
- No index used
- Acceptable for small tables or full table queries
- **Red flag** for large tables with WHERE clause

**Index Scan:**
- Direct index traversal
- Excellent for small result sets
- Accesses heap table to retrieve full rows

**Index-Only Scan:**
- All data retrieved from index (no heap access)
- Best performance
- Requires covering index with all needed columns

**Bitmap Heap Scan:**
- Two-step process: identify rows in index → fetch from heap
- Efficient for medium result sets
- Combines multiple index scans

**Nested Loop Join:**
- Iterate outer table, lookup inner table per row
- Good when outer table is small
- Requires index on inner table join column

**Hash Join:**
- Build hash table of inner table, probe with outer
- Good for large tables
- Memory-intensive

**Merge Join:**
- Sort both tables, merge sorted results
- Good for pre-sorted data
- Expensive if sorting required

### PostgreSQL Optimization Examples

**Example 1: Sequential Scan → Index Scan**

**Before:**
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';
```
```
Seq Scan on users  (cost=0.00..1500.00 rows=1) (actual time=50.123..50.124 rows=1)
  Filter: (email = 'user@example.com')
  Rows Removed by Filter: 99999
```

**Optimization:**
```sql
CREATE INDEX idx_users_email ON users (email);
```

**After:**
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';
```
```
Index Scan using idx_users_email on users  (cost=0.42..8.44 rows=1) (actual time=0.025..0.026 rows=1)
  Index Cond: (email = 'user@example.com')
```

**Result:** 1000x faster (50ms → 0.05ms)

## MySQL EXPLAIN

### Basic EXPLAIN Syntax

**Standard EXPLAIN:**
```sql
EXPLAIN SELECT * FROM products WHERE category_id = 5 AND price > 100;
```

**JSON Format** (detailed output):
```sql
EXPLAIN FORMAT=JSON SELECT * FROM products WHERE category_id = 5;
```

### Reading MySQL Output

**Example Output:**
```
+----+-------------+----------+------+---------------+------+---------+------+-------+-------------+
| id | select_type | table    | type | possible_keys | key  | key_len | ref  | rows  | Extra       |
+----+-------------+----------+------+---------------+------+---------+------+-------+-------------+
|  1 | SIMPLE      | products | ALL  | NULL          | NULL | NULL    | NULL | 50000 | Using where |
+----+-------------+----------+------+---------------+------+---------+------+-------+-------------+
```

**Key Columns:**

- **id**: Query identifier
- **select_type**: SIMPLE, PRIMARY, SUBQUERY, DERIVED, UNION
- **table**: Table being accessed
- **type**: Access type (performance indicator)
- **possible_keys**: Indexes MySQL could use
- **key**: Index actually used (NULL = no index)
- **key_len**: Bytes of index used
- **ref**: Columns/constants compared to index
- **rows**: Estimated rows examined
- **Extra**: Additional information

### MySQL Access Types (type column)

**Best to Worst Performance:**

1. **system** - Single row table (best)
2. **const** - Primary key or unique index lookup
3. **eq_ref** - One row from table for each previous row combination
4. **ref** - Non-unique index lookup
5. **range** - Index range scan (BETWEEN, >, <, IN)
6. **index** - Full index scan
7. **ALL** - Full table scan (worst)

**Target:** Achieve `const`, `eq_ref`, `ref`, or `range` types.

**Red Flag:** `ALL` (full table scan) on large tables.

### MySQL Extra Column Meanings

- **Using index**: Index-only scan (excellent)
- **Using where**: Filtering rows after retrieval
- **Using temporary**: Temporary table created (expensive)
- **Using filesort**: Sorting required (expensive for large result sets)
- **Using join buffer**: Join buffer used (index missing on join column)

### MySQL Optimization Examples

**Example 1: ALL → range**

**Before:**
```sql
EXPLAIN SELECT * FROM products WHERE category_id = 5 AND price > 100;
```
```
type: ALL, possible_keys: NULL, key: NULL, rows: 50000
```

**Optimization:**
```sql
CREATE INDEX idx_products_category_price ON products (category_id, price);
```

**After:**
```sql
EXPLAIN SELECT * FROM products WHERE category_id = 5 AND price > 100;
```
```
type: range, key: idx_products_category_price, rows: 150
```

**Result:** Rows examined reduced from 50,000 to 150.

## SQL Server Execution Plans

### Accessing Execution Plans

**Estimated Execution Plan** (Ctrl+L in SSMS):
```sql
-- Right-click query → Display Estimated Execution Plan
SELECT * FROM Sales.Orders WHERE CustomerID = 123;
```

**Actual Execution Plan** (Ctrl+M, then execute):
```sql
-- Query → Include Actual Execution Plan → Execute
SELECT * FROM Sales.Orders WHERE CustomerID = 123;
```

### Reading SQL Server Execution Plans

**Graphical Execution Plan Components:**

- **Operations**: Boxes representing operations (Scan, Seek, Join)
- **Arrows**: Data flow direction (right to left)
- **Thickness**: Relative row count (thick = many rows)
- **Warnings**: Yellow exclamation marks (missing indexes, implicit conversions)
- **Cost %**: Percentage of total query cost

**Read Direction:** Right to left, top to bottom.

### SQL Server Scan Types

**Table Scan:**
- Reads entire table
- No index available
- Red flag for large tables

**Clustered Index Scan:**
- Reads entire clustered index (full table)
- Similar to table scan

**Index Seek:**
- Direct index lookup
- Excellent performance
- Target for WHERE, JOIN conditions

**Index Scan:**
- Reads entire index
- Better than table scan if index is smaller
- Still inefficient for large indexes

**Key Lookup:**
- Additional lookup to retrieve non-indexed columns
- Indicates covering index opportunity

### SQL Server Optimization Examples

**Example 1: Identify Missing Index**

**Execution Plan Warning:**
```
Missing Index (Impact 95%)
CREATE NONCLUSTERED INDEX [<Name of Missing Index>]
ON [dbo].[Orders] ([CustomerID])
```

**Action:**
```sql
CREATE NONCLUSTERED INDEX IX_Orders_CustomerID
ON dbo.Orders (CustomerID);
```

**Example 2: Query Store Analysis**

Find top 10 expensive queries:
```sql
SELECT TOP 10
    q.query_id,
    qt.query_sql_text,
    rs.avg_duration / 1000.0 AS avg_duration_ms,
    rs.avg_logical_io_reads,
    rs.count_executions
FROM sys.query_store_query q
INNER JOIN sys.query_store_query_text qt ON q.query_text_id = qt.query_text_id
INNER JOIN sys.query_store_plan p ON q.query_id = p.query_id
INNER JOIN sys.query_store_runtime_stats rs ON p.plan_id = rs.plan_id
ORDER BY rs.avg_duration DESC;
```

## Key Metrics to Monitor

### Cross-Database Metrics

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Rows examined vs returned | <10x | 10-100x | >100x |
| Execution time | <10ms | 10-100ms | >100ms |
| Index usage | Present | Partial | None |
| Sort operations | None | Small dataset | Large dataset |

### PostgreSQL-Specific Metrics

- **Buffer hits vs reads**: High hit ratio indicates good cache usage
- **Planning time**: Should be <1ms typically
- **Execution time**: Target <100ms for user-facing queries

### MySQL-Specific Metrics

- **Handler_read_rnd_next**: High value indicates full table scans
- **Created_tmp_tables**: Temporary table creation count
- **Sort_scan**: Number of sorts requiring table scan

### SQL Server-Specific Metrics

- **Logical reads**: Pages read from cache
- **Physical reads**: Pages read from disk (minimize)
- **CPU time**: CPU milliseconds consumed

## Common Patterns and Solutions

### Pattern 1: High Row Count with Low Results

**Symptom:**
```
Seq Scan on table  (cost=0.00..10000.00 rows=100000)
  Filter: (column = value)
  Rows Removed by Filter: 99999
```

**Solution:** Add index on filter column
```sql
CREATE INDEX idx_table_column ON table (column);
```

### Pattern 2: Nested Loop with Large Outer Table

**Symptom:**
```
Nested Loop  (cost=0.00..50000.00 rows=10000)
  -> Seq Scan on large_table (rows=10000)
  -> Index Scan on small_table
```

**Solutions:**
1. Add index on large_table filter columns (reduce outer rows)
2. Reorder joins (start with smaller result set)
3. Force hash join if appropriate (PostgreSQL: `SET enable_nestloop = off`)

### Pattern 3: Sort Operation on Large Result Set

**Symptom:**
```
Sort  (cost=5000.00..6000.00 rows=100000)
  Sort Key: created_at DESC
  -> Seq Scan on orders
```

**Solution:** Create index matching ORDER BY
```sql
CREATE INDEX idx_orders_created ON orders (created_at DESC);
```

### Pattern 4: Multiple OR Conditions

**Symptom:**
```sql
SELECT * FROM users WHERE status = 'active' OR status = 'pending' OR status = 'verified';
```
```
Seq Scan on users
  Filter: ((status = 'active') OR (status = 'pending') OR (status = 'verified'))
```

**Solution:** Use IN or UNION ALL
```sql
-- Better: Use IN
SELECT * FROM users WHERE status IN ('active', 'pending', 'verified');

-- Or: Use UNION ALL with separate indexes
SELECT * FROM users WHERE status = 'active'
UNION ALL
SELECT * FROM users WHERE status = 'pending'
UNION ALL
SELECT * FROM users WHERE status = 'verified';
```

## Quick Reference: EXPLAIN Command Comparison

| Feature | PostgreSQL | MySQL | SQL Server |
|---------|-----------|-------|------------|
| Basic plan | `EXPLAIN` | `EXPLAIN` | Ctrl+L (SSMS) |
| Execute + timing | `EXPLAIN ANALYZE` | N/A | Ctrl+M, execute |
| Detailed output | `EXPLAIN (ANALYZE, BUFFERS, VERBOSE)` | `EXPLAIN FORMAT=JSON` | Execution Plan XML |
| Cost shown | Yes (arbitrary units) | Yes (not displayed in output) | Yes (percentage) |
| Actual rows | With ANALYZE | No | With actual plan |
| Index recommendations | No | No | Yes (warnings) |

## Best Practices

1. **Always run EXPLAIN before optimizing** - Understand the problem before solving it
2. **Compare before/after plans** - Verify optimizations work
3. **Use ANALYZE variant when possible** - Actual timing beats estimates
4. **Check row estimates vs actuals** - Large discrepancies indicate outdated statistics
5. **Update statistics regularly** - Run ANALYZE/UPDATE STATISTICS weekly
6. **Monitor production queries** - Enable slow query log or Query Store
7. **Archive execution plans** - Track performance changes over time
