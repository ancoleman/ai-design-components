---
sidebar_position: 4
title: SQL Optimization
description: Optimize SQL query performance through EXPLAIN analysis, indexing, and query rewriting
tags: [data-engineering, sql, performance, indexing, query-optimization, postgresql, mysql]
---

# SQL Optimization

Optimize SQL query performance across PostgreSQL, MySQL, and SQL Server through execution plan analysis, strategic indexing, and query rewriting.

## When to Use

Use when:
- Debugging slow queries or database timeouts
- Analyzing EXPLAIN plans or execution plans
- Determining index requirements
- Rewriting inefficient queries
- Identifying query anti-patterns (N+1, SELECT *, correlated subqueries)
- Database-specific optimization needs (PostgreSQL, MySQL, SQL Server)

## Key Features

### Core Optimization Workflow

1. **Analyze Query Performance**: Run EXPLAIN ANALYZE to identify bottlenecks
2. **Identify Opportunities**: Look for sequential scans, high row counts, inefficient joins
3. **Apply Indexing Strategies**: Add strategic indexes based on WHERE, JOIN, ORDER BY
4. **Rewrite Queries**: Eliminate anti-patterns and optimize query structure
5. **Verify Improvement**: Re-run EXPLAIN and compare performance

### Common Red Flags

| Indicator | Problem | Solution |
|-----------|---------|----------|
| Seq Scan / Table Scan | Full table scan on large table | Add index on filter columns |
| High row count | Processing excessive rows | Add WHERE filter or index |
| Nested Loop with large outer | Inefficient join algorithm | Index join columns |
| Correlated subquery | Subquery executes per row | Rewrite as JOIN or EXISTS |
| Sort on large result set | Expensive sorting | Add index matching ORDER BY |

## Quick Start

### Analyze Query Performance

**PostgreSQL:**
```sql
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = 123
ORDER BY created_at DESC
LIMIT 10;
```

**Output Analysis:**
```
Seq Scan on orders (cost=0.00..2500.00 rows=10)
  Filter: (customer_id = 123)
  Rows Removed by Filter: 99990
```
**Problem**: Sequential scan filtering 99,990 rows

### Add Composite Index

```sql
CREATE INDEX idx_orders_customer_created
ON orders (customer_id, created_at DESC);
```

### Verify Improvement

```sql
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = 123
ORDER BY created_at DESC
LIMIT 10;
```

**Result**: 200x faster (2000ms → 10ms)

```
Index Scan using idx_orders_customer_created (cost=0.42..12.44 rows=10)
  Index Cond: (customer_id = 123)
```

## Indexing Strategies

### Index Decision Framework

```
Is column used in WHERE, JOIN, ORDER BY, or GROUP BY?
├─ YES → Is column selective (many unique values)?
│  ├─ YES → Is table frequently queried?
│  │  ├─ YES → ADD INDEX
│  │  └─ NO → Consider based on query frequency
│  └─ NO (low selectivity) → Skip index
└─ NO → Skip index
```

### Composite Index Design

**Column Order Matters**:
1. **Equality filters first** (most selective)
2. **Additional equality filters** (by selectivity)
3. **Range filters or ORDER BY** (last)

**Example:**
```sql
-- Query pattern
SELECT * FROM orders
WHERE customer_id = 123 AND status = 'shipped'
ORDER BY created_at DESC
LIMIT 10;

-- Optimal composite index
CREATE INDEX idx_orders_customer_status_created
ON orders (customer_id, status, created_at DESC);
```

### Index Types by Use Case

**PostgreSQL**:
- **B-tree** (default): General-purpose, supports &lt;, ≤, =, ≥, &gt;, BETWEEN, IN
- **GIN**: Full-text search, JSONB, arrays
- **GiST**: Spatial data, geometric types
- **BRIN**: Very large tables with naturally ordered data

**MySQL**:
- **B-tree** (default): General-purpose index
- **Full-text**: Text search on VARCHAR/TEXT columns
- **Spatial**: Spatial data types

## Query Anti-Patterns

### 1. SELECT * (Over-fetching)

```sql
-- ❌ Bad: Fetches all columns
SELECT * FROM users WHERE id = 1;

-- ✅ Good: Fetch only needed columns
SELECT id, name, email FROM users WHERE id = 1;
```

### 2. N+1 Queries

```sql
-- ❌ Bad: 1 + N queries
SELECT * FROM users LIMIT 100;
-- Then in loop: SELECT * FROM posts WHERE user_id = ?;

-- ✅ Good: Single JOIN
SELECT users.*, posts.id AS post_id, posts.title
FROM users
LEFT JOIN posts ON users.id = posts.user_id;
```

### 3. Non-Sargable Queries

Functions on indexed columns prevent index usage:

```sql
-- ❌ Bad: Function prevents index usage
SELECT * FROM orders WHERE YEAR(created_at) = 2025;

-- ✅ Good: Sargable range condition
SELECT * FROM orders
WHERE created_at >= '2025-01-01'
  AND created_at < '2026-01-01';
```

### 4. Correlated Subqueries

```sql
-- ❌ Bad: Subquery executes per row
SELECT name,
  (SELECT COUNT(*) FROM orders WHERE orders.user_id = users.id)
FROM users;

-- ✅ Good: JOIN with GROUP BY
SELECT users.name, COUNT(orders.id) AS order_count
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.id, users.name;
```

## Database-Specific Optimizations

### PostgreSQL-Specific Features

**Partial Indexes** (index subset of rows):
```sql
CREATE INDEX idx_active_users_login
ON users (last_login)
WHERE status = 'active';
```

**Expression Indexes** (index computed values):
```sql
CREATE INDEX idx_users_email_lower
ON users (LOWER(email));
```

**Covering Indexes** (avoid heap access):
```sql
CREATE INDEX idx_users_email_covering
ON users (email) INCLUDE (id, name);
```

### MySQL-Specific Features

**Index Hints** (override optimizer):
```sql
SELECT * FROM orders USE INDEX (idx_orders_customer)
WHERE customer_id = 123;
```

### SQL Server-Specific Features

**Query Store** (track query performance over time):
```sql
ALTER DATABASE YourDatabase SET QUERY_STORE = ON;
```

## Advanced Techniques

### EXISTS vs IN for Subqueries

Use EXISTS for better performance with large datasets:

```sql
-- ✅ Good: EXISTS stops at first match
SELECT * FROM users
WHERE EXISTS (SELECT 1 FROM orders WHERE orders.user_id = users.id);

-- ❌ Less efficient: IN builds full list
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders);
```

### Common Table Expressions (CTEs)

Break complex queries into readable parts:

```sql
WITH active_customers AS (
  SELECT id, name FROM customers WHERE status = 'active'
),
recent_orders AS (
  SELECT customer_id, COUNT(*) as order_count
  FROM orders
  WHERE created_at > NOW() - INTERVAL '30 days'
  GROUP BY customer_id
)
SELECT ac.name, COALESCE(ro.order_count, 0) as orders
FROM active_customers ac
LEFT JOIN recent_orders ro ON ac.id = ro.customer_id;
```

## Monitoring and Maintenance

**Regular Optimization Tasks**:
- Review slow query logs weekly
- Update database statistics regularly (ANALYZE in PostgreSQL)
- Monitor index usage (drop unused indexes)
- Archive old data to keep tables manageable
- Review execution plans for critical queries quarterly

**PostgreSQL Statistics Update:**
```sql
ANALYZE table_name;
```

**MySQL Statistics Update:**
```sql
ANALYZE TABLE table_name;
```

## Related Skills

- [Data Architecture](./architecting-data) - Schema design and database fundamentals
- [Performance Engineering](./performance-engineering) - Application performance profiling
- [Data Transformation](./transforming-data) - dbt and query optimization

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/optimizing-sql)
- [PostgreSQL EXPLAIN Documentation](https://www.postgresql.org/docs/current/using-explain.html)
- [MySQL EXPLAIN Documentation](https://dev.mysql.com/doc/refman/8.0/en/explain.html)
