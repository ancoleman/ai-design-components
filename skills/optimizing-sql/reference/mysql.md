# MySQL-Specific Optimizations

MySQL-specific features, storage engines, and optimization techniques.

## MySQL Storage Engines

### InnoDB (Default)

**Characteristics:**
- ACID-compliant transactions
- Row-level locking
- Crash recovery
- Foreign key support
- Clustered primary key

**Use Case:** Default choice for most applications.

**Creation:**
```sql
CREATE TABLE orders (
  id INT PRIMARY KEY,
  customer_id INT,
  total DECIMAL(10,2)
) ENGINE=InnoDB;
```

**Clustered Index:**
- Table data stored in primary key order
- Fast primary key lookups
- Choose small primary key (INT vs BIGINT vs UUID)

**Recommendation:** Use AUTO_INCREMENT INT or BIGINT for primary keys.

### MyISAM

**Characteristics:**
- No transactions
- Table-level locking
- Faster reads (no MVCC overhead)
- No foreign keys
- No crash recovery

**Use Case:** Read-heavy tables with no writes (archives, logs).

**Creation:**
```sql
CREATE TABLE archive_logs (
  id INT PRIMARY KEY,
  message TEXT
) ENGINE=MyISAM;
```

**Warning:** Deprecated, avoid for new applications.

## MySQL Index Types

### B-tree Index (Default)

**Use Case:** General-purpose index.

**Creation:**
```sql
CREATE INDEX idx_users_email ON users (email);
```

**Prefix Indexes for Long Strings:**
```sql
-- Index first 10 characters
CREATE INDEX idx_articles_title ON articles (title(10));
```

**Composite Indexes:**
```sql
CREATE INDEX idx_orders_customer_status
ON orders (customer_id, status);
```

### Full-Text Index

**Use Case:** Text search on VARCHAR/TEXT columns.

**Creation:**
```sql
-- Add full-text index
CREATE FULLTEXT INDEX idx_articles_content ON articles (content);

-- Or in table definition
CREATE TABLE articles (
  id INT PRIMARY KEY,
  title VARCHAR(255),
  content TEXT,
  FULLTEXT (title, content)
) ENGINE=InnoDB;
```

**Query Syntax:**
```sql
-- Natural language search
SELECT * FROM articles
WHERE MATCH(content) AGAINST('mysql optimization');

-- Boolean mode (AND/OR/NOT)
SELECT * FROM articles
WHERE MATCH(content) AGAINST('+mysql +optimization -postgres' IN BOOLEAN MODE);

-- Query expansion (finds related terms)
SELECT * FROM articles
WHERE MATCH(content) AGAINST('database' WITH QUERY EXPANSION);
```

### Spatial Index

**Use Case:** Geometric data (points, polygons).

**Creation:**
```sql
CREATE TABLE locations (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  coordinates POINT NOT NULL,
  SPATIAL INDEX(coordinates)
) ENGINE=InnoDB;
```

**Query:**
```sql
-- Find locations within bounding box
SELECT name FROM locations
WHERE MBRContains(
  ST_GeomFromText('POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))'),
  coordinates
);
```

## MySQL EXPLAIN Analysis

### EXPLAIN Output Format

**Basic EXPLAIN:**
```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 123;
```

**Output:**
```
+----+-------------+--------+------+-------------------+------+---------+------+-------+-------------+
| id | select_type | table  | type | possible_keys     | key  | key_len | ref  | rows  | Extra       |
+----+-------------+--------+------+-------------------+------+---------+------+-------+-------------+
|  1 | SIMPLE      | orders | ref  | idx_orders_cust   | idx  | 4       | const| 150   | Using where |
+----+-------------+--------+------+-------------------+------+---------+------+-------+-------------+
```

### EXPLAIN FORMAT=JSON

**Detailed JSON Output:**
```sql
EXPLAIN FORMAT=JSON
SELECT * FROM orders WHERE customer_id = 123;
```

**Benefits:**
- More detailed information
- Nested structure for complex queries
- Cost estimates
- Filtering statistics

### Access Types (type column)

**Performance Ranking (Best to Worst):**

1. **system** - Single row table
2. **const** - Primary key/unique lookup with constant
3. **eq_ref** - One row per previous table row (unique index join)
4. **ref** - Non-unique index lookup
5. **range** - Index range scan (BETWEEN, >, <, IN)
6. **index** - Full index scan
7. **ALL** - Full table scan

**Target:** const, eq_ref, ref, or range

### Extra Column Meanings

**Good:**
- **Using index** - Index-only scan (covering index)
- **Using index condition** - Index condition pushdown (ICP)

**Acceptable:**
- **Using where** - WHERE clause filtering after retrieval

**Warning:**
- **Using temporary** - Temporary table created
- **Using filesort** - Sorting required (not index-based)

**Bad:**
- **Using join buffer** - Join without index (add index!)

## MySQL Index Hints

### USE INDEX

**Suggest Index:**
```sql
SELECT * FROM orders USE INDEX (idx_orders_customer)
WHERE customer_id = 123 AND created_at > '2025-01-01';
```

**When to Use:** Optimizer chooses wrong index.

### FORCE INDEX

**Force Index Usage:**
```sql
SELECT * FROM orders FORCE INDEX (idx_orders_customer)
WHERE customer_id = 123;
```

**When to Use:** Must use specific index (rare).

### IGNORE INDEX

**Prevent Index Usage:**
```sql
SELECT * FROM orders IGNORE INDEX (idx_orders_status)
WHERE customer_id = 123 AND status = 'pending';
```

**When to Use:** Force full table scan or different index.

### Optimizer Hints (MySQL 8.0+)

**JOIN Order Hints:**
```sql
SELECT /*+ JOIN_ORDER(orders, customers) */
  orders.*, customers.name
FROM orders
INNER JOIN customers ON orders.customer_id = customers.id;
```

**Index Hints:**
```sql
SELECT /*+ INDEX(orders idx_orders_customer) */
  * FROM orders WHERE customer_id = 123;
```

**Subquery Hints:**
```sql
SELECT /*+ SUBQUERY(MATERIALIZATION) */
  * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total > 1000);
```

## MySQL-Specific Optimizations

### Generated Columns (MySQL 5.7+)

**Use Case:** Index computed values.

**Virtual Generated Column:**
```sql
ALTER TABLE users
ADD COLUMN email_lower VARCHAR(255)
  GENERATED ALWAYS AS (LOWER(email)) VIRTUAL;

-- Index generated column
CREATE INDEX idx_users_email_lower ON users (email_lower);
```

**Stored Generated Column:**
```sql
ALTER TABLE users
ADD COLUMN full_name VARCHAR(510)
  GENERATED ALWAYS AS (CONCAT(first_name, ' ', last_name)) STORED;

CREATE INDEX idx_users_full_name ON users (full_name);
```

**Difference:**
- **VIRTUAL**: Computed on read (no storage overhead)
- **STORED**: Computed on write (faster reads, storage overhead)

### JSON Indexes

**Create Generated Column for JSON Path:**
```sql
-- Extract JSON field
ALTER TABLE users
ADD COLUMN premium_status VARCHAR(10)
  GENERATED ALWAYS AS (metadata->>'$.premium') STORED;

-- Index generated column
CREATE INDEX idx_users_premium ON users (premium_status);
```

**Query:**
```sql
SELECT * FROM users WHERE premium_status = 'true';
```

### Index Condition Pushdown (ICP)

**MySQL 5.6+ Feature:** Push WHERE conditions down to storage engine.

**Without ICP:**
```sql
-- Storage engine returns all rows matching first index column
-- MySQL server filters remaining conditions
```

**With ICP:**
```sql
-- Storage engine filters all index columns
-- Fewer rows returned to MySQL server
```

**Check if Enabled:**
```sql
SHOW VARIABLES LIKE 'optimizer_switch';
-- Look for index_condition_pushdown=on
```

**EXPLAIN Indicator:**
```
Extra: Using index condition
```

### Multi-Range Read (MRR)

**MySQL 5.6+ Feature:** Optimize range scans by sorting row IDs before fetching.

**Benefits:**
- Sequential I/O instead of random I/O
- Fewer page fetches

**Enable:**
```sql
SET optimizer_switch='mrr=on,mrr_cost_based=off';
```

## MySQL Configuration Tuning

### Buffer Pool Size (InnoDB)

**Recommendation:** 70-80% of system RAM for dedicated database server.

```sql
-- Check current setting
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';

-- Set in my.cnf / my.ini
[mysqld]
innodb_buffer_pool_size = 8G
```

### Query Cache (Deprecated)

**Warning:** Query cache removed in MySQL 8.0.

**MySQL 5.7 and Earlier:**
```sql
-- Check query cache status
SHOW VARIABLES LIKE 'query_cache%';

-- Disable query cache (recommended for modern apps)
query_cache_type = 0
query_cache_size = 0
```

**Replacement:** Application-level caching (Redis, Memcached).

### Join Buffer Size

**Used for:** Joins without indexes.

```sql
-- Check current setting
SHOW VARIABLES LIKE 'join_buffer_size';

-- Set per session
SET SESSION join_buffer_size = 8388608;  -- 8MB
```

### Sort Buffer Size

**Used for:** ORDER BY, GROUP BY operations.

```sql
-- Check current setting
SHOW VARIABLES LIKE 'sort_buffer_size';

-- Set per session
SET SESSION sort_buffer_size = 2097152;  -- 2MB
```

## MySQL Monitoring

### Slow Query Log

**Enable:**
```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 0.5;  -- Log queries > 500ms
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow-query.log';
```

**Analyze Slow Queries:**
```bash
# mysqldumpslow - Parse slow query log
mysqldumpslow -s t -t 10 /var/log/mysql/slow-query.log
# -s t: Sort by time
# -t 10: Top 10 queries
```

### Performance Schema

**Enable:**
```sql
-- Check if enabled
SHOW VARIABLES LIKE 'performance_schema';

-- Enable in my.cnf
[mysqld]
performance_schema = ON
```

**Query Statistics:**
```sql
-- Top 10 slowest queries
SELECT
  DIGEST_TEXT,
  COUNT_STAR,
  AVG_TIMER_WAIT / 1000000000 AS avg_ms,
  SUM_TIMER_WAIT / 1000000000 AS total_ms
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 10;
```

**Index Usage:**
```sql
-- Tables without primary key
SELECT
  TABLE_SCHEMA,
  TABLE_NAME
FROM information_schema.TABLES
WHERE TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema')
  AND ENGINE = 'InnoDB'
  AND TABLE_TYPE = 'BASE TABLE'
  AND TABLE_CATALOG IS NULL
  AND NOT EXISTS (
    SELECT 1 FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = TABLES.TABLE_SCHEMA
      AND TABLE_NAME = TABLES.TABLE_NAME
      AND INDEX_NAME = 'PRIMARY'
  );
```

### Table Statistics

**Update Statistics:**
```sql
-- Analyze table
ANALYZE TABLE orders;

-- Optimize table (rebuilds, updates stats)
OPTIMIZE TABLE orders;
```

**View Statistics:**
```sql
-- Table sizes
SELECT
  TABLE_SCHEMA,
  TABLE_NAME,
  ROUND(DATA_LENGTH / 1024 / 1024, 2) AS data_mb,
  ROUND(INDEX_LENGTH / 1024 / 1024, 2) AS index_mb,
  ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) AS total_mb,
  TABLE_ROWS
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'your_database'
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;
```

## MySQL Best Practices

### Primary Key Selection

**Recommended:**
```sql
-- Auto-increment integer (clustered index friendly)
CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  ...
) ENGINE=InnoDB;
```

**Avoid:**
```sql
-- UUID as primary key (poor clustered index performance)
CREATE TABLE orders (
  id CHAR(36) PRIMARY KEY DEFAULT (UUID()),  -- ❌ Fragmentation
  ...
) ENGINE=InnoDB;
```

**UUID Alternative (MySQL 8.0+):**
```sql
-- Use UUID_TO_BIN with reordering for better clustering
CREATE TABLE orders (
  id BINARY(16) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID(), 1)),
  ...
) ENGINE=InnoDB;
```

### Composite Index Order

**Rule:** Equality filters → Range filters → ORDER BY columns

```sql
-- Query pattern
SELECT * FROM orders
WHERE customer_id = 123
  AND status IN ('pending', 'processing')
  AND created_at > '2025-01-01'
ORDER BY created_at DESC;

-- Optimal index
CREATE INDEX idx_orders_customer_status_created
ON orders (customer_id, status, created_at);
```

### Avoid SELECT *

**Bad:**
```sql
SELECT * FROM users WHERE id = 123;
```

**Good:**
```sql
SELECT id, name, email FROM users WHERE id = 123;
```

### Use LIMIT for Large Result Sets

**Always limit:**
```sql
-- Good: Limits results
SELECT * FROM orders ORDER BY created_at DESC LIMIT 100;

-- Bad: No limit on large table
SELECT * FROM orders ORDER BY created_at DESC;
```

## Quick Reference

### Index Type Selection

| Use Case | Index Type | Creation |
|----------|-----------|----------|
| General queries | B-tree | `CREATE INDEX ON table (column)` |
| Long strings | B-tree prefix | `CREATE INDEX ON table (column(10))` |
| Full-text search | Full-text | `CREATE FULLTEXT INDEX ON table (column)` |
| Spatial data | Spatial | `CREATE SPATIAL INDEX ON table (column)` |

### Storage Engine Selection

| Requirement | Engine | Notes |
|------------|--------|-------|
| Transactions | InnoDB | Default, recommended |
| Read-only archive | MyISAM | Deprecated, avoid |
| In-memory | MEMORY | Temporary tables only |

### Configuration Priorities

1. **innodb_buffer_pool_size**: 70-80% of RAM
2. **innodb_log_file_size**: 256MB-1GB
3. **max_connections**: Based on workload (100-200 typical)
4. **innodb_flush_log_at_trx_commit**: 2 for better performance (1 for durability)
