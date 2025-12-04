# SQL Optimization - Master Plan

**Skill Level:** Low (Tactical/Quick Reference)
**Status:** Planning Phase
**Last Updated:** December 3, 2025
**Target Lines:** 300-500 lines (Low-level tactical skill)

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Component Taxonomy](#component-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [SQL Dialect Examples](#sql-dialect-examples)
7. [Anti-Patterns](#anti-patterns)
8. [Skill Structure Design](#skill-structure-design)
9. [Integration Points](#integration-points)
10. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why SQL Optimization Matters

SQL optimization is a critical tactical skill for building performant data-driven applications. Poor query performance can cascade into:

- **User Experience Impact**: Slow page loads, timeouts, frustrated users
- **Infrastructure Costs**: Over-provisioned databases to compensate for inefficient queries
- **Scalability Bottlenecks**: Systems that can't handle growth due to N+1 queries and missing indexes
- **Development Velocity**: Teams spending time firefighting performance issues instead of building features

This is a **low-level tactical skill** focused on actionable optimization techniques: analyzing EXPLAIN plans, adding the right indexes, rewriting problematic queries, and understanding database-specific optimizations.

### Skill Context

- **Level**: Low (Quick reference, tactical decision-making)
- **Audience**: Developers, DBAs, backend engineers optimizing queries
- **Trigger Words**: "slow query", "optimize SQL", "add index", "EXPLAIN plan", "N+1 problem"
- **Multi-Database**: Covers PostgreSQL, MySQL, SQL Server with dialect-specific guidance

---

## Skill Purpose and Scope

### Core Competencies

This skill helps users:

1. **Analyze query performance** using EXPLAIN/EXPLAIN ANALYZE
2. **Identify optimization opportunities** through execution plan analysis
3. **Apply indexing strategies** appropriate to query patterns
4. **Rewrite queries** to eliminate anti-patterns (N+1, SELECT *, correlated subqueries)
5. **Understand database-specific optimizations** for PostgreSQL, MySQL, SQL Server
6. **Make informed decisions** about when to denormalize, partition, or cache

### What This Skill Doesn't Cover

- **Database schema design** (covered in `databases-relational`)
- **Database administration** (backups, replication, high availability)
- **ORM-specific optimization** (though it informs ORM usage)
- **NoSQL query optimization** (covered in respective database skills)
- **Advanced database internals** (buffer pools, WAL, vacuum strategies)

### Target Audience

- Backend developers writing SQL queries
- Full-stack developers experiencing slow API responses
- DBAs troubleshooting performance issues
- Engineers optimizing existing codebases

---

## Research Findings

### Search: "SQL query optimization best practices 2025"

**Key Findings:**

1. **Indexing Strategies**
   - Use proper indexing on frequently queried columns
   - Clustered indexes for sequential/sorted data with no duplicates (primary keys)
   - Non-clustered indexes for lookup tables
   - Full-text indexes for large text fields
   - Index join columns to speed up joins

2. **Query Structure Best Practices**
   - Avoid `SELECT *` - fetch only necessary columns
   - Use `LIMIT`/`TOP` to reduce rows retrieved
   - Order joins logically, starting with tables returning fewest rows
   - Use INNER JOIN when possible (more efficient than OUTER JOIN)
   - Write sargable queries (Search ARGument ABLE - queries that can use indexes)

3. **Subquery Optimization**
   - Minimize subqueries - replace with JOINs when possible
   - Use `EXISTS` instead of `IN` for subqueries
   - Use `EXISTS` instead of `COUNT(*)` when checking for row existence
   - Use `UNION ALL` instead of `UNION` when duplicates don't matter

4. **Advanced Techniques**
   - Use CTEs (Common Table Expressions) to break down complex queries
   - Partition large tables so queries scan only relevant partitions
   - Implement materialized views for expensive aggregations
   - Use query hints sparingly (override optimizer behavior)
   - Leverage database-specific features (PostgreSQL ANY(ARRAY[]), MySQL query cache)

5. **Monitoring & Maintenance**
   - Regularly review execution plans (EXPLAIN/EXPLAIN ANALYZE)
   - Monitor query performance metrics (execution time, I/O, CPU)
   - Update database statistics frequently
   - Archive old data to keep tables manageable
   - Choose appropriate data types (avoid defaulting to large TEXT fields)

**Sources:**
- datacamp.com: SQL Query Optimization Best Practices
- simplelogic-it.com: Advanced SQL Optimization Techniques
- idera.com: SQL Server Performance Tuning
- dev.to: Modern SQL Optimization Strategies
- medium.com: AI-Powered Query Optimization

### Context7: PostgreSQL Documentation

**Key Findings:**

1. **EXPLAIN Command**
   - `EXPLAIN` shows query plan without execution
   - `EXPLAIN ANALYZE` executes query and shows actual timing
   - Shows: Seq Scan, Index Scan, Bitmap Heap Scan, Hash Join, Nested Loop

2. **Index Scan Types**
   - **Simple Index Scan**: Direct index traversal for exact matches or small result sets
   - **Bitmap Index Scan**: Two-step process (identify locations → fetch rows), efficient for medium result sets
   - **Index-Only Scan**: All data retrieved from index without touching heap table
   - **Skip Scan**: Optimization for multi-column indexes when leading column isn't in WHERE clause

3. **PostgreSQL-Specific Optimizations**
   - Index types: B-tree (default), Hash, GIN (full-text), GiST (spatial), BRIN (large tables)
   - CTEs (WITH clauses) for query organization and materialization
   - Partial indexes: `CREATE INDEX ON table (column) WHERE condition`
   - Expression indexes: `CREATE INDEX ON table (LOWER(column))`
   - Covering indexes: Include extra columns to enable Index-Only Scans

4. **LIMIT Optimization**
   - PostgreSQL automatically switches to Index Scan for LIMIT queries
   - Can stop execution once LIMIT satisfied (significant cost reduction)

**Source:** /websites/postgresql (61,065 code snippets, High reputation, Benchmark Score 81.9)

### Context7: MySQL Documentation

**Key Findings:**

1. **EXPLAIN Variants**
   - `EXPLAIN SELECT ...` - Standard execution plan
   - `EXPLAIN FORMAT=JSON SELECT ...` - Detailed JSON output
   - Shows: type (ALL, index, range, ref, eq_ref, const), possible_keys, key, rows

2. **MySQL Index Optimization**
   - Indexes speed up WHERE clause, JOIN conditions, ORDER BY, GROUP BY
   - Use EXPLAIN to identify missing indexes
   - Create minimal set of indexes (too many slow down writes)
   - Index join columns on both sides of JOIN

3. **MySQL-Specific Features**
   - Query cache (deprecated in MySQL 8.0, removed in MySQL 8.4)
   - Index hints: `SELECT * FROM table USE INDEX (index_name)`
   - Optimizer hints: `/*+ BKA(t1) */` for block nested loop join
   - FORCE INDEX, IGNORE INDEX to override optimizer

4. **Storage Engine Considerations**
   - InnoDB (default): Clustered primary key, supports transactions
   - MyISAM: Faster reads, no transactions, full-table locks
   - Optimization strategies differ by storage engine

**Source:** /websites/dev_mysql_doc_refman_9_4_en (19,896 code snippets, High reputation, Benchmark Score 87.5)

### Research Summary

**Consensus across sources:**
- EXPLAIN/EXPLAIN ANALYZE is the foundation of optimization
- Indexing is the #1 performance lever (when done right)
- Avoid anti-patterns: SELECT *, N+1 queries, correlated subqueries
- Query structure matters: JOIN order, sargability, LIMIT placement
- Database-specific features provide additional optimization opportunities

**Dialect Differences:**
- **PostgreSQL**: Rich index types, CTEs, skip scan optimization
- **MySQL**: Index hints, optimizer hints, storage engine selection
- **SQL Server**: Execution plans, index tuning wizard, query store

---

## Component Taxonomy

### 1. Query Analysis

**Purpose**: Understand how queries execute and identify bottlenecks

**Components:**

#### 1.1 Execution Plan Analysis
- **EXPLAIN**: Show query plan without execution (PostgreSQL, MySQL, SQL Server)
- **EXPLAIN ANALYZE**: Execute and show actual timing (PostgreSQL)
- **EXPLAIN FORMAT=JSON**: Detailed JSON output (MySQL)
- **Execution Plan**: Graphical execution plan (SQL Server Management Studio)

**Key Metrics:**
- **Cost**: Estimated resource consumption (arbitrary units)
- **Rows**: Estimated/actual rows processed
- **Scan Types**: Sequential, Index, Bitmap, Index-Only
- **Join Algorithms**: Nested Loop, Hash Join, Merge Join
- **Timing**: Actual execution time per operation

#### 1.2 Scan Type Interpretation
- **Sequential Scan (Seq Scan)**: Full table scan - no index used
- **Index Scan**: Direct index traversal
- **Bitmap Heap Scan**: Two-step index scan for medium result sets
- **Index-Only Scan**: All data from index (no heap access)
- **Table Scan (MySQL)**: Full table scan

**Decision Point**: If seeing Seq Scan on filtered queries → add index

### 2. Indexing Strategies

**Purpose**: Speed up data retrieval through appropriate index design

**Components:**

#### 2.1 Index Types (PostgreSQL)
- **B-tree** (default): General-purpose, supports <, ≤, =, ≥, >, BETWEEN, IN, IS NULL
- **Hash**: Equality comparisons only, faster than B-tree for =
- **GIN** (Generalized Inverted Index): Full-text search, JSONB, arrays
- **GiST** (Generalized Search Tree): Spatial data, full-text, custom operators
- **BRIN** (Block Range Index): Very large tables, naturally ordered data
- **Bloom**: Multi-column equality with fewer false positives

#### 2.2 Index Types (MySQL)
- **B-tree** (default): General-purpose index
- **Full-text**: Text search on VARCHAR/TEXT columns
- **Spatial**: Spatial data types
- **Hash**: Memory engine only

#### 2.3 Index Strategies
- **Single-column indexes**: For simple WHERE clauses
- **Composite indexes**: Multiple columns, left-to-right matching
- **Covering indexes**: Include extra columns to avoid heap lookup
- **Partial indexes** (PostgreSQL): `WHERE` clause in index definition
- **Expression indexes**: Index on computed values (e.g., `LOWER(email)`)
- **Unique indexes**: Enforce uniqueness + query optimization

**Decision Point**: Index columns in WHERE, JOIN, ORDER BY, GROUP BY clauses

### 3. Query Patterns

**Purpose**: Recognize efficient vs inefficient query structures

**Components:**

#### 3.1 Efficient Patterns
- **Sargable queries**: Conditions that can use indexes
  ```sql
  WHERE column = value          -- ✅ Sargable
  WHERE column > 100 AND column < 200  -- ✅ Sargable
  ```

- **JOIN optimization**:
  ```sql
  -- Start with smallest result set
  FROM small_table
  INNER JOIN large_table ON small_table.id = large_table.small_id
  ```

- **EXISTS for existence checks**:
  ```sql
  WHERE EXISTS (SELECT 1 FROM related WHERE related.id = main.id)
  ```

- **UNION ALL when duplicates don't matter**:
  ```sql
  SELECT id FROM table1 UNION ALL SELECT id FROM table2
  ```

#### 3.2 Inefficient Patterns (Anti-Patterns)
- **Non-sargable queries**: Functions on indexed columns
  ```sql
  WHERE YEAR(date_column) = 2025   -- ❌ Index can't be used
  WHERE date_column >= '2025-01-01' AND date_column < '2026-01-01'  -- ✅
  ```

- **SELECT \***: Fetches unnecessary columns
  ```sql
  SELECT *                         -- ❌ Over-fetching
  SELECT id, name, email           -- ✅ Specific columns
  ```

- **N+1 queries**: One query + N queries in loop
  ```sql
  -- ❌ N+1 Problem
  SELECT * FROM users;              -- 1 query
  -- Then for each user:
  SELECT * FROM posts WHERE user_id = ?;  -- N queries

  -- ✅ Single JOIN
  SELECT users.*, posts.* FROM users
  LEFT JOIN posts ON users.id = posts.user_id;
  ```

- **Correlated subqueries**: Subquery executes per row
  ```sql
  -- ❌ Correlated
  SELECT * FROM users WHERE id IN (SELECT user_id FROM posts WHERE posts.user_id = users.id);

  -- ✅ JOIN or EXISTS
  SELECT DISTINCT users.* FROM users
  INNER JOIN posts ON users.id = posts.user_id;
  ```

### 4. Join Optimization

**Purpose**: Efficient multi-table queries

**Components:**

#### 4.1 Join Algorithms
- **Nested Loop Join**: Iterate outer table, lookup inner table (good for small outer table)
- **Hash Join**: Build hash table of inner, probe with outer (good for large tables)
- **Merge Join**: Sort both tables, merge (good for sorted data)

#### 4.2 Join Best Practices
- **Index foreign keys**: Both sides of join condition
- **Order joins**: Start with table returning fewest rows
- **Limit join count**: Break complex queries with 5+ joins
- **Use INNER JOIN**: When possible (more efficient than OUTER JOIN)
- **Consider denormalization**: For frequently joined tables in read-heavy systems

### 5. Partitioning and Sharding

**Purpose**: Manage large tables by dividing data

**Components:**

#### 5.1 Partitioning (Single Database)
- **Range partitioning**: By date ranges (e.g., monthly partitions)
- **List partitioning**: By discrete values (e.g., by region)
- **Hash partitioning**: Distribute evenly by hash function
- **Composite partitioning**: Combine strategies

**Benefit**: Queries scan only relevant partitions (partition pruning)

#### 5.2 Sharding (Multiple Databases)
- **Horizontal sharding**: Split rows across multiple databases
- **Vertical sharding**: Split tables across multiple databases

**Decision Point**: Partition when single table > 100GB, shard when single database > 1TB

---

## Decision Frameworks

### Framework 1: When to Add an Index

**Decision Tree:**

```
Is the column used in WHERE, JOIN, ORDER BY, or GROUP BY?
├─ YES → Is the column selective (many unique values)?
│  ├─ YES → Is the table frequently queried?
│  │  ├─ YES → ADD INDEX ✅
│  │  └─ NO → Consider based on query frequency
│  └─ NO (low selectivity, e.g., boolean) → Skip index ❌
└─ NO → Skip index ❌
```

**Additional Considerations:**

- **Write frequency**: Heavy writes? Minimize indexes (slow down INSERT/UPDATE)
- **Table size**: Small tables (< 1000 rows) may not benefit from indexes
- **Composite indexes**: Index multiple columns if queried together
- **Covering indexes**: Add non-WHERE columns to avoid heap lookup

### Framework 2: EXPLAIN Plan Interpretation

**Red Flags in Execution Plans:**

| Indicator | Problem | Solution |
|-----------|---------|----------|
| Seq Scan / Table Scan | Full table scan on large table | Add index on filter columns |
| High "rows" estimate | Processing too many rows | Add WHERE filter or index |
| Nested Loop with large outer | Inefficient join algorithm | Index join columns, rewrite query |
| Correlated subquery | Subquery executes per row | Rewrite as JOIN or EXISTS |
| Sort operation | Sorting large result set | Add index matching ORDER BY |
| Filter after scan | Filtering non-indexed column | Add index on filter column |

**Good Signs:**

- Index Scan / Index-Only Scan
- Low "rows" counts
- Hash Join or Merge Join for large tables
- Bitmap Heap Scan for medium result sets

### Framework 3: When to Denormalize

**Normalization vs Performance Trade-off:**

```
Is the query joining 3+ tables frequently?
├─ YES → Is the data relatively static (infrequent updates)?
│  ├─ YES → Is read performance critical?
│  │  ├─ YES → Consider denormalization (duplicate data) ✅
│  │  └─ NO → Keep normalized
│  └─ NO (frequent updates) → Keep normalized, use caching
└─ NO → Keep normalized
```

**Denormalization Strategies:**

1. **Duplicate columns**: Copy foreign key data into main table
2. **Summary tables**: Pre-aggregate data
3. **Materialized views**: Database-maintained denormalized views
4. **Caching layer**: Application-level caching (Redis, Memcached)

### Framework 4: Query Rewriting Strategy

**Process:**

1. **Run EXPLAIN ANALYZE**: Identify bottleneck
2. **Check for anti-patterns**: SELECT *, N+1, correlated subqueries
3. **Optimize structure**:
   - Replace subqueries with JOINs
   - Use EXISTS instead of IN
   - Add LIMIT to constrain results
4. **Add indexes**: Based on WHERE, JOIN, ORDER BY columns
5. **Re-run EXPLAIN**: Verify improvement
6. **Benchmark**: Compare actual execution times

---

## SQL Dialect Examples

### PostgreSQL Examples

#### Example 1: EXPLAIN ANALYZE for Query Profiling

**Problem**: Slow user query

```sql
-- Initial query (slow)
SELECT * FROM users WHERE email = 'john@example.com';
```

**Step 1: Analyze**

```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'john@example.com';
```

**Output:**
```
Seq Scan on users  (cost=0.00..1500.00 rows=1 width=100) (actual time=50.123..50.124 rows=1 loops=1)
  Filter: (email = 'john@example.com'::text)
  Rows Removed by Filter: 99999
Planning Time: 0.100 ms
Execution Time: 50.150 ms
```

**Problem Identified**: Sequential scan, 99,999 rows filtered

**Step 2: Add Index**

```sql
CREATE INDEX idx_users_email ON users (email);
```

**Step 3: Re-analyze**

```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'john@example.com';
```

**Output:**
```
Index Scan using idx_users_email on users  (cost=0.42..8.44 rows=1 width=100) (actual time=0.025..0.026 rows=1 loops=1)
  Index Cond: (email = 'john@example.com'::text)
Planning Time: 0.150 ms
Execution Time: 0.050 ms
```

**Result**: 1000x faster (50ms → 0.05ms)

#### Example 2: Composite Index for Multi-Column WHERE

```sql
-- Query with multiple filters
SELECT * FROM orders
WHERE customer_id = 123 AND status = 'shipped'
ORDER BY created_at DESC
LIMIT 10;
```

**Optimal Composite Index:**

```sql
-- Order matters: equality first, range/order last
CREATE INDEX idx_orders_customer_status_created
ON orders (customer_id, status, created_at DESC);
```

**Why this order?**
1. `customer_id` - Equality filter (most selective)
2. `status` - Equality filter (second filter)
3. `created_at DESC` - ORDER BY matches index sort

#### Example 3: Partial Index for Specific Queries

```sql
-- Only query active users
SELECT * FROM users WHERE status = 'active' AND last_login > NOW() - INTERVAL '30 days';
```

**Partial Index** (smaller, faster):

```sql
CREATE INDEX idx_active_users_login
ON users (last_login)
WHERE status = 'active';
```

**Benefit**: Index only contains active users (smaller index, faster scans)

#### Example 4: Index-Only Scan with Covering Index

```sql
-- Query only needs id and email
SELECT id, email FROM users WHERE email LIKE 'john%';
```

**Covering Index:**

```sql
CREATE INDEX idx_users_email_covering ON users (email) INCLUDE (id);
```

**Result**: PostgreSQL never accesses heap table (Index-Only Scan)

#### Example 5: Expression Index for Case-Insensitive Search

```sql
-- Case-insensitive email lookup
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';
```

**Expression Index:**

```sql
CREATE INDEX idx_users_email_lower ON users (LOWER(email));
```

**Query** (must use same expression):

```sql
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';
```

### MySQL Examples

#### Example 1: EXPLAIN for Index Analysis

**Problem**: Slow product search

```sql
-- Initial query
SELECT * FROM products WHERE category_id = 5 AND price > 100;
```

**Step 1: Analyze**

```sql
EXPLAIN SELECT * FROM products WHERE category_id = 5 AND price > 100;
```

**Output:**
```
+----+-------------+----------+------+---------------+------+---------+------+-------+-------------+
| id | select_type | table    | type | possible_keys | key  | key_len | ref  | rows  | Extra       |
+----+-------------+----------+------+---------------+------+---------+------+-------+-------------+
|  1 | SIMPLE      | products | ALL  | NULL          | NULL | NULL    | NULL | 50000 | Using where |
+----+-------------+----------+------+---------------+------+---------+------+-------+-------------+
```

**Problem**: `type = ALL` (full table scan), no key used

**Step 2: Add Composite Index**

```sql
CREATE INDEX idx_products_category_price ON products (category_id, price);
```

**Step 3: Re-analyze**

```sql
EXPLAIN SELECT * FROM products WHERE category_id = 5 AND price > 100;
```

**Output:**
```
+----+-------------+----------+-------+--------------------------------+------------------------------+---------+------+------+-------------+
| id | select_type | table    | type  | possible_keys                  | key                          | key_len | ref  | rows | Extra       |
+----+-------------+----------+-------+--------------------------------+------------------------------+---------+------+------+-------------+
|  1 | SIMPLE      | products | range | idx_products_category_price    | idx_products_category_price  | 9       | NULL | 150  | Using where |
+----+-------------+----------+-------+--------------------------------+------------------------------+---------+------+------+-------------+
```

**Result**: `type = range` (using index), rows reduced from 50,000 to 150

#### Example 2: Index Hint Override

```sql
-- Force MySQL to use specific index
SELECT * FROM orders USE INDEX (idx_orders_customer)
WHERE customer_id = 123 AND created_at > '2025-01-01';
```

**Index Hints:**
- `USE INDEX (index_name)` - Suggest index
- `FORCE INDEX (index_name)` - Force index usage
- `IGNORE INDEX (index_name)` - Prevent index usage

**When to use**: Rare cases where optimizer chooses wrong index

#### Example 3: Optimize JOIN with Indexes

```sql
-- Slow join
SELECT customers.name, orders.total
FROM customers
INNER JOIN orders ON customers.id = orders.customer_id
WHERE orders.status = 'completed';
```

**Add Indexes:**

```sql
-- Index foreign key on orders table
CREATE INDEX idx_orders_customer_id ON orders (customer_id);

-- Composite index including filter column
CREATE INDEX idx_orders_customer_status ON orders (customer_id, status);
```

**Result**: MySQL uses index for JOIN and WHERE filter

### SQL Server Examples

#### Example 1: Execution Plan Analysis

**Query:**

```sql
SELECT * FROM Sales.Orders WHERE CustomerID = 123;
```

**In SQL Server Management Studio:**
1. Click "Display Estimated Execution Plan" (Ctrl+L)
2. Look for:
   - **Table Scan** (bad) vs **Index Seek** (good)
   - **Thick arrows** = Many rows flowing through
   - **Warnings** (yellow exclamation marks)

**Optimization:**

```sql
CREATE NONCLUSTERED INDEX IX_Orders_CustomerID ON Sales.Orders (CustomerID);
```

#### Example 2: Query Store for Historical Analysis

**Enable Query Store:**

```sql
ALTER DATABASE YourDatabase SET QUERY_STORE = ON;
```

**Find expensive queries:**

```sql
SELECT TOP 10
    q.query_id,
    qt.query_sql_text,
    rs.avg_duration / 1000.0 AS avg_duration_ms,
    rs.avg_logical_io_reads
FROM sys.query_store_query q
INNER JOIN sys.query_store_query_text qt ON q.query_text_id = qt.query_text_id
INNER JOIN sys.query_store_plan p ON q.query_id = p.query_id
INNER JOIN sys.query_store_runtime_stats rs ON p.plan_id = rs.plan_id
ORDER BY rs.avg_duration DESC;
```

---

## Anti-Patterns

### 1. SELECT * Anti-Pattern

**Problem**: Over-fetching data

```sql
-- ❌ Bad: Fetches all 50 columns
SELECT * FROM users WHERE id = 1;

-- ✅ Good: Fetches only needed columns
SELECT id, name, email FROM users WHERE id = 1;
```

**Impact**: Increased I/O, network transfer, memory usage

### 2. N+1 Query Problem

**Problem**: One query + N queries in loop

```sql
-- ❌ Bad: N+1 queries
-- Query 1: Fetch all users
SELECT * FROM users LIMIT 100;

-- Query 2-101: Fetch posts for each user (in application loop)
SELECT * FROM posts WHERE user_id = ?;  -- Executed 100 times
```

**Solution**: Single JOIN query

```sql
-- ✅ Good: Single query with JOIN
SELECT users.*, posts.id AS post_id, posts.title
FROM users
LEFT JOIN posts ON users.id = posts.user_id
WHERE users.id IN (1, 2, 3, ...);
```

### 3. Missing Indexes on Foreign Keys

**Problem**: Slow joins and cascading deletes

```sql
-- ❌ Bad: No index on foreign key
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,  -- No index!
    total DECIMAL(10,2)
);
```

**Solution**: Always index foreign keys

```sql
-- ✅ Good: Index on foreign key
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    total DECIMAL(10,2),
    INDEX idx_orders_customer (customer_id)
);
```

### 4. Non-Sargable Queries

**Problem**: Functions on indexed columns prevent index usage

```sql
-- ❌ Bad: Function on indexed column
SELECT * FROM orders WHERE YEAR(created_at) = 2025;

-- ✅ Good: Sargable range condition
SELECT * FROM orders
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01';
```

### 5. Implicit Type Conversion

**Problem**: Comparing different data types

```sql
-- ❌ Bad: String compared to INT (indexed)
SELECT * FROM users WHERE user_id = '123';  -- user_id is INT

-- ✅ Good: Matching types
SELECT * FROM users WHERE user_id = 123;
```

### 6. Unnecessary DISTINCT

**Problem**: Expensive deduplication when not needed

```sql
-- ❌ Bad: DISTINCT when data is already unique
SELECT DISTINCT id FROM users WHERE id = 123;

-- ✅ Good: Remove DISTINCT (id is unique)
SELECT id FROM users WHERE id = 123;
```

### 7. Correlated Subqueries

**Problem**: Subquery executes once per outer row

```sql
-- ❌ Bad: Correlated subquery
SELECT name,
    (SELECT COUNT(*) FROM orders WHERE orders.user_id = users.id) AS order_count
FROM users;

-- ✅ Good: JOIN with GROUP BY
SELECT users.name, COUNT(orders.id) AS order_count
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.id, users.name;
```

---

## Skill Structure Design

### Proposed SKILL.md Structure

**Target Lines:** 300-500 lines (Low-level tactical skill)

**Structure:**

```markdown
---
name: sql-optimization
description: Optimize SQL query performance through EXPLAIN analysis, indexing strategies, and query rewriting for PostgreSQL, MySQL, and SQL Server. Use when debugging slow queries, analyzing execution plans, or improving database performance.
---

## Purpose

Provide tactical guidance for optimizing SQL query performance across PostgreSQL, MySQL, and SQL Server.

## When to Use This Skill

Trigger this skill when users mention:
- "slow query", "performance issue"
- "EXPLAIN plan", "execution plan"
- "add index", "optimize query"
- "N+1 problem", "missing index"
- Database-specific: PostgreSQL EXPLAIN ANALYZE, MySQL EXPLAIN FORMAT=JSON

## Quick Reference

### 1. Analyze Query Performance
- [EXPLAIN Analysis Guide] - reference/explain-guide.md
- [Scan Types Interpretation] - reference/scan-types.md

### 2. Indexing Strategies
- [When to Add Indexes] - reference/indexing-decisions.md
- [Index Types by Database] - reference/index-types.md
- [Composite Index Design] - reference/composite-indexes.md

### 3. Query Rewriting
- [Anti-Patterns to Avoid] - reference/anti-patterns.md
- [Efficient Query Patterns] - reference/efficient-patterns.md

### 4. Database-Specific Optimizations
- [PostgreSQL Optimization] - reference/postgresql.md
- [MySQL Optimization] - reference/mysql.md
- [SQL Server Optimization] - reference/sqlserver.md

## Progressive Disclosure

Reference detailed guides based on user's specific need:
- First-time users → Start with EXPLAIN Analysis Guide
- Indexing questions → Indexing Decisions Guide
- Anti-pattern detection → Anti-Patterns Reference
- Database-specific → Appropriate dialect guide
```

### Proposed reference/ Files

**File Structure:**

```
skills/sql-optimization/
├── SKILL.md                          # Main skill file (300-500 lines)
├── reference/
│   ├── explain-guide.md              # EXPLAIN/EXPLAIN ANALYZE interpretation
│   ├── scan-types.md                 # Scan type meanings and implications
│   ├── indexing-decisions.md         # When to add indexes (decision framework)
│   ├── index-types.md                # Index types by database (B-tree, Hash, GIN, etc.)
│   ├── composite-indexes.md          # Multi-column index design
│   ├── anti-patterns.md              # Common anti-patterns with examples
│   ├── efficient-patterns.md         # Efficient query patterns
│   ├── postgresql.md                 # PostgreSQL-specific optimizations
│   ├── mysql.md                      # MySQL-specific optimizations
│   └── sqlserver.md                  # SQL Server-specific optimizations
└── examples/
    ├── explain-analysis-examples.sql # Before/after EXPLAIN examples
    ├── indexing-examples.sql         # Index creation examples
    └── query-rewriting-examples.sql  # Anti-pattern → optimized rewrites
```

**Content Distribution:**

- **SKILL.md**: Overview, when to use, quick reference to other files
- **reference/**: Detailed guides (100-300 lines each)
- **examples/**: Concrete SQL examples with comments

**Progressive Disclosure Strategy:**

1. User asks about slow query → SKILL.md triggers
2. SKILL.md directs to `explain-guide.md` for analysis
3. If indexing needed → Reference `indexing-decisions.md`
4. If anti-pattern detected → Reference `anti-patterns.md`
5. Database-specific questions → Reference appropriate dialect file

---

## Integration Points

### Connects to Other Skills

1. **databases-relational** (Upstream)
   - Schema design decisions affect optimization
   - Normalization vs denormalization trade-offs
   - This skill assumes schema already exists

2. **api-patterns** (Peer)
   - API endpoints causing N+1 queries
   - Pagination affecting LIMIT/OFFSET queries
   - Caching strategies to reduce query load

3. **observability** (Peer)
   - Query performance monitoring
   - Slow query logs
   - APM tools showing database bottlenecks

4. **performance-engineering** (Peer)
   - Application-level performance profiling
   - Load testing revealing database bottlenecks
   - Caching strategies (Redis, CDN)

### Typical User Journey

```
User → "My API is slow"
  ↓
observability skill → Identifies database as bottleneck
  ↓
sql-optimization skill → Analyze queries, add indexes
  ↓
Improvement or...
  ↓
databases-relational skill → Consider schema changes
```

---

## Implementation Roadmap

### Phase 1: Core Documentation (Week 1)

**Deliverables:**
- [x] init.md master plan (this document)
- [ ] SKILL.md (main skill file, 300-500 lines)
- [ ] reference/explain-guide.md
- [ ] reference/indexing-decisions.md
- [ ] reference/anti-patterns.md

**Goal**: Minimum viable skill covering 80% of optimization scenarios

### Phase 2: Database-Specific Guides (Week 2)

**Deliverables:**
- [ ] reference/postgresql.md (EXPLAIN ANALYZE, index types, CTEs)
- [ ] reference/mysql.md (EXPLAIN FORMAT=JSON, index hints, storage engines)
- [ ] reference/sqlserver.md (Execution plans, Query Store, index tuning wizard)

**Goal**: Complete dialect-specific guidance

### Phase 3: Advanced Topics (Week 3)

**Deliverables:**
- [ ] reference/composite-indexes.md (Multi-column index design)
- [ ] reference/scan-types.md (Detailed scan type interpretation)
- [ ] reference/efficient-patterns.md (Efficient query patterns)
- [ ] examples/ directory with SQL examples

**Goal**: Cover advanced optimization techniques

### Phase 4: Testing & Refinement (Week 4)

**Activities:**
1. **Create evaluations** (3+ test scenarios)
   - "User reports slow query" → Skill guides EXPLAIN analysis
   - "N+1 problem in API" → Skill suggests JOIN optimization
   - "When to add index?" → Skill provides decision framework

2. **Test with different models**
   - Haiku: Does it need more guidance?
   - Sonnet: Balanced experience
   - Opus: Can handle less detail

3. **Token usage optimization**
   - Measure token usage for typical workflows
   - Ensure progressive disclosure works (SKILL.md stays loaded, references load on-demand)

4. **Refine based on observations**
   - Update SKILL.md based on common user paths
   - Add examples for frequently misunderstood concepts

### Success Criteria

- [ ] Skill file under 500 lines
- [ ] 3+ evaluations passing
- [ ] Tested with Haiku, Sonnet, Opus
- [ ] Token usage acceptable (<10k tokens for typical workflow)
- [ ] Real-world testing: Can solve actual slow query problems
- [ ] Clear progressive disclosure: Users find relevant info in 1-2 references

---

## Evaluation Scenarios

### Evaluation 1: Analyze Slow Query

**Scenario:**
```
User: "This query is slow:
SELECT * FROM orders WHERE customer_id = 123 ORDER BY created_at DESC LIMIT 10;
```

**Expected Skill Behavior:**
1. Suggest running EXPLAIN/EXPLAIN ANALYZE
2. Identify likely issue: missing index on customer_id
3. Recommend composite index: (customer_id, created_at DESC)
4. Explain why ORDER BY column should be in index

**Success Criteria:** Skill provides actionable index recommendation

### Evaluation 2: N+1 Problem Detection

**Scenario:**
```
User: "My API endpoint fetches users then loops through each user to get their posts. It's slow."
```

**Expected Skill Behavior:**
1. Recognize N+1 query pattern
2. Explain the problem (1 query + N queries)
3. Provide JOIN-based solution
4. Show before/after query examples

**Success Criteria:** Skill identifies anti-pattern and provides alternative

### Evaluation 3: EXPLAIN Plan Interpretation

**Scenario:**
```
User: "What does this EXPLAIN output mean?
Seq Scan on users (cost=0.00..1500.00 rows=1 width=100)
  Filter: (email = 'john@example.com')
```

**Expected Skill Behavior:**
1. Explain Seq Scan = full table scan
2. Identify problem: filtering 100k rows for 1 result
3. Recommend index on email column
4. Show expected EXPLAIN output after indexing

**Success Criteria:** Skill interprets plan and suggests optimization

---

## Appendix: Key Terminology

**Sargable**: Search ARGument ABLE - query conditions that can use indexes
**Selectivity**: Proportion of unique values in a column (high selectivity = good for indexes)
**Cardinality**: Number of unique values in a column
**Covering Index**: Index containing all columns needed by query (enables Index-Only Scan)
**Heap Table**: Main table storage (as opposed to index)
**Bitmap Scan**: Two-step scan (identify rows in index → fetch from heap)
**Nested Loop**: Join algorithm iterating outer table, looking up inner table per row
**Hash Join**: Join algorithm building hash table of inner table, probing with outer
**CTE**: Common Table Expression (WITH clause) for query organization
**Materialized View**: Pre-computed query results stored as table

---

## References

**Research Sources:**
- PostgreSQL Documentation: /websites/postgresql (61,065 snippets, score 81.9)
- MySQL Reference Manual: /websites/dev_mysql_doc_refman_9_4_en (19,896 snippets, score 87.5)
- SQL Optimization Best Practices 2025: datacamp.com, simplelogic-it.com, dev.to
- Anthropic Skills Best Practices: skill_best_practice.md

**Related Skills:**
- databases-relational: Schema design and database fundamentals
- observability: Performance monitoring and slow query detection
- api-patterns: API-level optimization (pagination, caching)
- performance-engineering: Application performance profiling

---

**End of Master Plan**
