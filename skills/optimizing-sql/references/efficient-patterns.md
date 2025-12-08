# Efficient Query Patterns

Collection of proven efficient SQL patterns for optimal query performance.

## Table of Contents

1. [Existence Checks](#existence-checks)
2. [Pagination](#pagination)
3. [Aggregation Patterns](#aggregation-patterns)
4. [Union Operations](#union-operations)
5. [Window Functions](#window-functions)
6. [Batch Operations](#batch-operations)

## Existence Checks

### Pattern: EXISTS vs COUNT

**Use Case:** Check if related records exist.

**Inefficient:**
```sql
-- ❌ Bad: Counts all matching rows
SELECT * FROM users
WHERE (SELECT COUNT(*) FROM orders WHERE orders.user_id = users.id) > 0;
```

**Efficient:**
```sql
-- ✅ Good: Stops at first match
SELECT * FROM users
WHERE EXISTS (SELECT 1 FROM orders WHERE orders.user_id = users.id);
```

**Why EXISTS is Better:**
- Stops execution at first matching row
- No need to count all rows
- Better performance for large result sets

**Performance Comparison:**
```
COUNT(*) with 1000 matches: ~100ms
EXISTS with 1000 matches: ~5ms (stops at first match)
```

### Pattern: EXISTS vs IN

**Use Case:** Filter by values in subquery.

**Less Efficient:**
```sql
-- ❌ Suboptimal: Builds full list
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total > 1000);
```

**More Efficient:**
```sql
-- ✅ Better: Can stop early with semi-join
SELECT * FROM users
WHERE EXISTS (
  SELECT 1 FROM orders WHERE orders.user_id = users.id AND orders.total > 1000
);
```

**When to Use Each:**
- **EXISTS**: When checking existence or correlated conditions
- **IN**: When list is small and static (e.g., `IN (1, 2, 3)`)

## Pagination

### Pattern: Efficient LIMIT/OFFSET

**Inefficient for Deep Pagination:**
```sql
-- ❌ Bad: Offset skips rows but database still processes them
SELECT * FROM posts
ORDER BY created_at DESC
LIMIT 20 OFFSET 10000;  -- Skip 10,000 rows
```

**Why It's Slow:**
- Database processes all 10,020 rows
- Sorts 10,020 rows
- Then discards first 10,000
- Performance degrades linearly with offset

**Efficient Keyset Pagination:**
```sql
-- ✅ Good: Use last seen value as cursor
SELECT * FROM posts
WHERE created_at < '2025-01-15 10:30:00'  -- Last seen timestamp
ORDER BY created_at DESC
LIMIT 20;
```

**Why It's Fast:**
- Index scan starts at cursor position
- No offset processing
- Constant performance regardless of page depth

**Implementation Pattern:**
```sql
-- Page 1
SELECT id, title, created_at FROM posts
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Page 2 (last_created_at = '2025-01-15 10:30:00', last_id = 12345)
SELECT id, title, created_at FROM posts
WHERE (created_at < '2025-01-15 10:30:00')
   OR (created_at = '2025-01-15 10:30:00' AND id < 12345)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

**Required Index:**
```sql
CREATE INDEX idx_posts_created_id ON posts (created_at DESC, id DESC);
```

### Pattern: Cursor-Based Pagination

**API Response Format:**
```json
{
  "data": [...],
  "cursor": {
    "next": "eyJjcmVhdGVkX2F0IjoiMjAyNS0wMS0xNSIsImlkIjoxMjM0NX0=",
    "has_more": true
  }
}
```

**Cursor Encoding:**
```python
import base64
import json

# Encode cursor
cursor_data = {"created_at": "2025-01-15 10:30:00", "id": 12345}
cursor = base64.b64encode(json.dumps(cursor_data).encode()).decode()

# Decode cursor
cursor_data = json.loads(base64.b64decode(cursor).decode())
```

## Aggregation Patterns

### Pattern: Conditional Aggregation

**Use Case:** Multiple aggregations with different conditions.

**Inefficient (Multiple Subqueries):**
```sql
-- ❌ Bad: Multiple scans of orders table
SELECT
  c.id,
  c.name,
  (SELECT COUNT(*) FROM orders WHERE customer_id = c.id) AS total_orders,
  (SELECT COUNT(*) FROM orders WHERE customer_id = c.id AND status = 'completed') AS completed_orders,
  (SELECT SUM(total) FROM orders WHERE customer_id = c.id AND status = 'completed') AS revenue
FROM customers c;
```

**Efficient (Single Query with CASE):**
```sql
-- ✅ Good: Single scan with conditional aggregation
SELECT
  c.id,
  c.name,
  COUNT(o.id) AS total_orders,
  COUNT(CASE WHEN o.status = 'completed' THEN 1 END) AS completed_orders,
  SUM(CASE WHEN o.status = 'completed' THEN o.total ELSE 0 END) AS revenue
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name;
```

**Performance Comparison:**
```
Multiple subqueries: 3 table scans, ~300ms
Conditional aggregation: 1 table scan, ~100ms
```

### Pattern: Filtered Aggregation (PostgreSQL)

**PostgreSQL FILTER Clause:**
```sql
-- ✅ PostgreSQL-specific: FILTER clause (more readable)
SELECT
  c.id,
  c.name,
  COUNT(o.id) AS total_orders,
  COUNT(o.id) FILTER (WHERE o.status = 'completed') AS completed_orders,
  SUM(o.total) FILTER (WHERE o.status = 'completed') AS revenue
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name;
```

## Union Operations

### Pattern: UNION ALL vs UNION

**Inefficient:**
```sql
-- ❌ Bad: UNION removes duplicates (expensive)
SELECT id, name FROM active_users
UNION
SELECT id, name FROM trial_users;
```

**Why UNION is Expensive:**
- Sorts both result sets
- Performs deduplication
- Additional memory and CPU overhead

**Efficient:**
```sql
-- ✅ Good: UNION ALL (no deduplication)
SELECT id, name FROM active_users
UNION ALL
SELECT id, name FROM trial_users;
```

**When to Use Each:**
- **UNION ALL**: When duplicates acceptable or datasets don't overlap (99% of cases)
- **UNION**: Only when duplicates must be removed and datasets may overlap

**Performance Comparison:**
```
UNION with 100k rows: ~500ms (sorting + dedup)
UNION ALL with 100k rows: ~50ms (no overhead)
```

### Pattern: Efficient Set Operations

**Use Case:** Combine results from partitioned tables.

```sql
-- ✅ Good: UNION ALL for partitioned data
SELECT * FROM orders_2024 WHERE status = 'pending'
UNION ALL
SELECT * FROM orders_2025 WHERE status = 'pending';
```

## Window Functions

### Pattern: Row Numbering for Deduplication

**Use Case:** Get first/last record per group.

**Inefficient (Correlated Subquery):**
```sql
-- ❌ Bad: Correlated subquery
SELECT *
FROM products p
WHERE p.created_at = (
  SELECT MAX(created_at)
  FROM products
  WHERE category_id = p.category_id
);
```

**Efficient (Window Function):**
```sql
-- ✅ Good: Window function with CTE
WITH ranked_products AS (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY created_at DESC) AS rn
  FROM products
)
SELECT * FROM ranked_products WHERE rn = 1;
```

**Performance Comparison:**
```
Correlated subquery: ~2000ms (N subqueries)
Window function: ~200ms (single scan)
```

### Pattern: Running Totals

**Use Case:** Calculate cumulative sum.

**Inefficient (Correlated Subquery):**
```sql
-- ❌ Bad: Subquery per row
SELECT
  order_date,
  total,
  (SELECT SUM(total)
   FROM orders o2
   WHERE o2.order_date <= orders.order_date) AS running_total
FROM orders;
```

**Efficient (Window Function):**
```sql
-- ✅ Good: Window function
SELECT
  order_date,
  total,
  SUM(total) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM orders;
```

### Pattern: Rank Within Group

**Use Case:** Find top N items per category.

```sql
-- ✅ Efficient: Top 3 products per category by sales
WITH ranked_products AS (
  SELECT
    category_id,
    product_name,
    sales,
    RANK() OVER (PARTITION BY category_id ORDER BY sales DESC) AS rank
  FROM products
)
SELECT * FROM ranked_products WHERE rank <= 3;
```

## Batch Operations

### Pattern: Bulk INSERT

**Inefficient:**
```sql
-- ❌ Bad: Individual INSERTs (1000 round trips)
INSERT INTO users (name, email) VALUES ('User1', 'user1@example.com');
INSERT INTO users (name, email) VALUES ('User2', 'user2@example.com');
-- ... 998 more
```

**Efficient:**
```sql
-- ✅ Good: Bulk INSERT (1 round trip)
INSERT INTO users (name, email) VALUES
  ('User1', 'user1@example.com'),
  ('User2', 'user2@example.com'),
  ('User3', 'user3@example.com'),
  -- ... up to 1000 rows
  ('User1000', 'user1000@example.com');
```

**Performance Comparison:**
```
Individual INSERTs: ~5000ms
Bulk INSERT: ~50ms
```

**Batch Size Recommendations:**
- **PostgreSQL**: 1000-5000 rows per INSERT
- **MySQL**: 1000 rows per INSERT (max_allowed_packet limit)
- **SQL Server**: 1000 rows per INSERT

### Pattern: Bulk UPDATE with CASE

**Use Case:** Update multiple rows with different values.

**Inefficient:**
```sql
-- ❌ Bad: Multiple UPDATE statements
UPDATE products SET price = 19.99 WHERE id = 1;
UPDATE products SET price = 29.99 WHERE id = 2;
UPDATE products SET price = 39.99 WHERE id = 3;
```

**Efficient:**
```sql
-- ✅ Good: Single UPDATE with CASE
UPDATE products
SET price = CASE id
  WHEN 1 THEN 19.99
  WHEN 2 THEN 29.99
  WHEN 3 THEN 39.99
END
WHERE id IN (1, 2, 3);
```

### Pattern: Upsert (INSERT or UPDATE)

**PostgreSQL (ON CONFLICT):**
```sql
-- ✅ Efficient upsert
INSERT INTO user_stats (user_id, login_count, last_login)
VALUES (123, 1, NOW())
ON CONFLICT (user_id)
DO UPDATE SET
  login_count = user_stats.login_count + 1,
  last_login = NOW();
```

**MySQL (ON DUPLICATE KEY UPDATE):**
```sql
-- ✅ Efficient upsert
INSERT INTO user_stats (user_id, login_count, last_login)
VALUES (123, 1, NOW())
ON DUPLICATE KEY UPDATE
  login_count = login_count + 1,
  last_login = NOW();
```

**SQL Server (MERGE):**
```sql
-- ✅ Efficient upsert
MERGE INTO user_stats AS target
USING (SELECT 123 AS user_id, 1 AS login_count, GETDATE() AS last_login) AS source
ON target.user_id = source.user_id
WHEN MATCHED THEN
  UPDATE SET login_count = target.login_count + 1, last_login = GETDATE()
WHEN NOT MATCHED THEN
  INSERT (user_id, login_count, last_login)
  VALUES (source.user_id, source.login_count, source.last_login);
```

## Common Table Expressions (CTEs)

### Pattern: Readable Complex Queries

**Inefficient (Nested Subqueries):**
```sql
-- ❌ Hard to read and maintain
SELECT *
FROM (
  SELECT *
  FROM (
    SELECT user_id, SUM(total) as revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY user_id
  ) AS user_revenue
  WHERE revenue > 1000
) AS high_value_users
INNER JOIN users ON users.id = high_value_users.user_id;
```

**Efficient (CTEs):**
```sql
-- ✅ Readable and maintainable
WITH user_revenue AS (
  SELECT user_id, SUM(total) as revenue
  FROM orders
  WHERE status = 'completed'
  GROUP BY user_id
),
high_value_users AS (
  SELECT * FROM user_revenue WHERE revenue > 1000
)
SELECT
  users.*,
  high_value_users.revenue
FROM high_value_users
INNER JOIN users ON users.id = high_value_users.user_id;
```

**Benefits:**
- Better readability
- Easier debugging (can SELECT from CTEs individually)
- Query optimizer can optimize entire query

### Pattern: Recursive CTEs

**Use Case:** Hierarchical data (org charts, nested categories).

```sql
-- ✅ Recursive CTE for org chart
WITH RECURSIVE org_chart AS (
  -- Base case: top-level managers
  SELECT id, name, manager_id, 1 AS level
  FROM employees
  WHERE manager_id IS NULL

  UNION ALL

  -- Recursive case: employees reporting to previous level
  SELECT e.id, e.name, e.manager_id, oc.level + 1
  FROM employees e
  INNER JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart ORDER BY level, name;
```

## Index-Friendly Patterns

### Pattern: Prefix Matching

**Efficient:**
```sql
-- ✅ Can use B-tree index
SELECT * FROM users WHERE email LIKE 'john%';
```

**Index:**
```sql
CREATE INDEX idx_users_email ON users (email);
```

### Pattern: Range Queries

**Efficient:**
```sql
-- ✅ Can use B-tree index
SELECT * FROM orders
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01';
```

**Index:**
```sql
CREATE INDEX idx_orders_created ON orders (created_at);
```

### Pattern: Composite Filters

**Efficient:**
```sql
-- ✅ Uses composite index efficiently
SELECT * FROM orders
WHERE customer_id = 123 AND status = 'pending'
ORDER BY created_at DESC
LIMIT 10;
```

**Optimal Index:**
```sql
CREATE INDEX idx_orders_customer_status_created
ON orders (customer_id, status, created_at DESC);
```

## Quick Reference

### Existence Checks
- Use `EXISTS` instead of `COUNT(*) > 0`
- Use `NOT EXISTS` instead of `NOT IN` (handles NULLs)

### Pagination
- Use keyset/cursor pagination instead of OFFSET for deep pagination
- Index columns in ORDER BY and WHERE clauses

### Aggregation
- Use conditional aggregation (CASE in aggregate) instead of multiple subqueries
- PostgreSQL: Use FILTER clause for readability

### Unions
- Use `UNION ALL` by default (no deduplication overhead)
- Only use `UNION` when duplicates must be removed

### Window Functions
- Use window functions instead of correlated subqueries for ranking/running totals
- More efficient and more readable

### Batch Operations
- Bulk INSERT/UPDATE instead of row-by-row operations
- Use upsert operations (ON CONFLICT, ON DUPLICATE KEY, MERGE)

### CTEs
- Use CTEs for complex queries (better readability)
- PostgreSQL 12+: CTEs are inline-optimized by default
