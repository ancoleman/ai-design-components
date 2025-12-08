# SQL Anti-Patterns

Common SQL performance anti-patterns with explanations, impact analysis, and solutions.

## Table of Contents

1. [SELECT * Anti-Pattern](#select--anti-pattern)
2. [N+1 Query Problem](#n1-query-problem)
3. [Missing Indexes on Foreign Keys](#missing-indexes-on-foreign-keys)
4. [Non-Sargable Queries](#non-sargable-queries)
5. [Implicit Type Conversion](#implicit-type-conversion)
6. [Correlated Subqueries](#correlated-subqueries)
7. [Unnecessary DISTINCT](#unnecessary-distinct)
8. [OR vs IN Performance](#or-vs-in-performance)
9. [NOT IN with NULL Values](#not-in-with-null-values)
10. [Wildcard at Start of LIKE](#wildcard-at-start-of-like)

## SELECT * Anti-Pattern

### Problem Description

Fetching all columns when only subset needed.

**Anti-Pattern:**
```sql
-- ❌ Bad: Fetches all 50 columns
SELECT * FROM users WHERE id = 1;
```

**Impact:**
- Increased I/O (reading unnecessary data from disk)
- Higher network transfer (sending unnecessary data)
- More memory usage (larger result sets)
- Slower query execution
- Breaks application when schema changes

**Solution:**
```sql
-- ✅ Good: Fetch only needed columns
SELECT id, name, email, created_at FROM users WHERE id = 1;
```

### When SELECT * is Acceptable

**Exception 1: Small tables with few columns**
```sql
SELECT * FROM settings;  -- OK: 3-5 columns, small table
```

**Exception 2: Exploratory queries (development only)**
```sql
-- OK during development/debugging
SELECT * FROM users LIMIT 5;
```

**Exception 3: All columns genuinely needed**
```sql
-- OK if truly need every column
SELECT * FROM user_profiles WHERE user_id = 123;
```

### Performance Comparison

**Test Case:** Users table with 50 columns, 100,000 rows

```sql
-- SELECT * : 250ms, 500MB transferred
SELECT * FROM users WHERE status = 'active';

-- Specific columns: 50ms, 50MB transferred
SELECT id, name, email FROM users WHERE status = 'active';
```

**Result:** 5x performance improvement

## N+1 Query Problem

### Problem Description

Executing 1 query to fetch parent records, then N queries (one per parent) to fetch related records.

**Anti-Pattern:**
```sql
-- ❌ Bad: 1 + N queries

-- Query 1: Fetch users
SELECT * FROM users LIMIT 100;

-- Query 2-101: For each user, fetch posts (executed 100 times in application loop)
SELECT * FROM posts WHERE user_id = ?;
```

**Impact:**
- 101 database round trips instead of 1
- Network latency multiplied by N
- Database connection overhead × N
- Poor scalability (linear growth with N)

**Solution 1: Single JOIN**
```sql
-- ✅ Good: Single query with JOIN
SELECT
  users.id,
  users.name,
  posts.id AS post_id,
  posts.title,
  posts.content
FROM users
LEFT JOIN posts ON users.id = posts.user_id
WHERE users.id IN (1, 2, 3, ...);
```

**Solution 2: Separate Queries with IN Clause**
```sql
-- ✅ Also good: 2 queries instead of N+1
-- Query 1: Fetch users
SELECT * FROM users LIMIT 100;

-- Query 2: Fetch all posts for these users
SELECT * FROM posts WHERE user_id IN (1, 2, 3, ..., 100);
```

### N+1 Detection

**Rails ActiveRecord Example:**
```ruby
# ❌ N+1 Problem
users = User.limit(100)
users.each do |user|
  puts user.posts.count  # Triggers N queries
end

# ✅ Fixed with eager loading
users = User.includes(:posts).limit(100)
users.each do |user|
  puts user.posts.count  # Uses preloaded data
end
```

**Django ORM Example:**
```python
# ❌ N+1 Problem
users = User.objects.all()[:100]
for user in users:
    print(user.posts.count())  # Triggers N queries

# ✅ Fixed with select_related / prefetch_related
users = User.objects.prefetch_related('posts').all()[:100]
for user in users:
    print(user.posts.count())  # Uses preloaded data
```

### Performance Comparison

**Test Case:** 100 users, average 5 posts each

```sql
-- N+1 approach: 101 queries, ~1000ms
-- JOIN approach: 1 query, ~50ms
```

**Result:** 20x performance improvement

## Missing Indexes on Foreign Keys

### Problem Description

Foreign key columns without indexes cause slow joins and cascading operations.

**Anti-Pattern:**
```sql
-- ❌ Bad: No index on foreign key
CREATE TABLE orders (
  id INT PRIMARY KEY,
  customer_id INT,  -- No index!
  total DECIMAL(10,2),
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

**Impact:**
- Slow joins (sequential scan on orders table)
- Slow cascading deletes (must scan entire orders table)
- Slow cascading updates
- Poor performance for queries filtering by customer_id

**Solution:**
```sql
-- ✅ Good: Index on foreign key
CREATE TABLE orders (
  id INT PRIMARY KEY,
  customer_id INT,
  total DECIMAL(10,2),
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE INDEX idx_orders_customer ON orders (customer_id);
```

### Why This Matters

**Query Without Index:**
```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 123;
```
```
Seq Scan on orders  (cost=0.00..10000.00 rows=100)
  Filter: (customer_id = 123)
```
**100,000 rows scanned**

**Query With Index:**
```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 123;
```
```
Index Scan using idx_orders_customer on orders  (cost=0.42..12.44 rows=100)
  Index Cond: (customer_id = 123)
```
**100 rows accessed directly**

### Cascading Delete Performance

**Without Index:**
```sql
DELETE FROM customers WHERE id = 123;
-- Scans entire orders table to find matching rows
-- Time: 500ms for 1 million row orders table
```

**With Index:**
```sql
DELETE FROM customers WHERE id = 123;
-- Uses index to find matching rows directly
-- Time: 5ms
```

**Result:** 100x faster cascading deletes

## Non-Sargable Queries

### Problem Description

**Sargable:** Search ARGument ABLE - conditions that can use indexes.

**Non-sargable:** Functions or operations on indexed columns prevent index usage.

### Anti-Pattern 1: Function on Indexed Column

**Anti-Pattern:**
```sql
-- ❌ Bad: Function prevents index usage
SELECT * FROM orders WHERE YEAR(created_at) = 2025;
```

**Why It Fails:**
- Index on `created_at` cannot be used
- Database must evaluate YEAR() for every row
- Results in sequential scan

**Solution:**
```sql
-- ✅ Good: Sargable range condition
SELECT * FROM orders
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01';
```

### Anti-Pattern 2: Arithmetic on Indexed Column

**Anti-Pattern:**
```sql
-- ❌ Bad: Arithmetic prevents index usage
SELECT * FROM products WHERE price * 1.1 > 100;
```

**Solution:**
```sql
-- ✅ Good: Move arithmetic to other side
SELECT * FROM products WHERE price > 100 / 1.1;
```

### Anti-Pattern 3: String Concatenation

**Anti-Pattern:**
```sql
-- ❌ Bad: Concatenation prevents index usage
SELECT * FROM users WHERE first_name || ' ' || last_name = 'John Doe';
```

**Solution 1: Separate Conditions**
```sql
-- ✅ Better: Use separate conditions
SELECT * FROM users WHERE first_name = 'John' AND last_name = 'Doe';
```

**Solution 2: Computed Column (SQL Server, MySQL)**
```sql
-- Add computed column with index
ALTER TABLE users ADD full_name AS (first_name + ' ' + last_name);
CREATE INDEX idx_users_full_name ON users (full_name);
```

### Anti-Pattern 4: LIKE with Leading Wildcard

**Anti-Pattern:**
```sql
-- ❌ Bad: Leading wildcard prevents index usage
SELECT * FROM users WHERE email LIKE '%@example.com';
```

**Why It Fails:**
- Cannot use B-tree index for prefix search
- Must scan entire table

**Solution 1: Trailing Wildcard (if applicable)**
```sql
-- ✅ Good: Trailing wildcard can use index
SELECT * FROM users WHERE email LIKE 'john%';
```

**Solution 2: Full-Text Index**
```sql
-- PostgreSQL: Use trigram index
CREATE INDEX idx_users_email_trgm ON users USING GIN (email gin_trgm_ops);
SELECT * FROM users WHERE email LIKE '%@example.com';

-- MySQL: Full-text index
CREATE FULLTEXT INDEX idx_users_email_fulltext ON users (email);
SELECT * FROM users WHERE MATCH(email) AGAINST('example.com');
```

### Sargable vs Non-Sargable Examples

| Non-Sargable (Bad) | Sargable (Good) |
|-------------------|----------------|
| `WHERE YEAR(date) = 2025` | `WHERE date >= '2025-01-01' AND date < '2026-01-01'` |
| `WHERE LOWER(email) = 'x@y.com'` | Use expression index on `LOWER(email)` |
| `WHERE price * 1.1 > 100` | `WHERE price > 100 / 1.1` |
| `WHERE column + 10 = 50` | `WHERE column = 40` |
| `WHERE email LIKE '%@example.com'` | `WHERE email LIKE 'john%'` or use full-text |

## Implicit Type Conversion

### Problem Description

Comparing different data types forces type conversion, preventing index usage.

**Anti-Pattern:**
```sql
-- ❌ Bad: user_id is INT, '123' is VARCHAR
SELECT * FROM users WHERE user_id = '123';
```

**Why It Fails:**
- Database converts every row's user_id to string
- Index on user_id cannot be used efficiently
- Sequential scan likely

**EXPLAIN Output:**
```
Seq Scan on users  (cost=0.00..1500.00 rows=1)
  Filter: ((user_id)::text = '123'::text)
```

**Solution:**
```sql
-- ✅ Good: Matching types
SELECT * FROM users WHERE user_id = 123;
```

**EXPLAIN Output:**
```
Index Scan using idx_users_id on users  (cost=0.42..8.44 rows=1)
  Index Cond: (user_id = 123)
```

### Common Type Mismatch Scenarios

**Scenario 1: String to Number**
```sql
-- ❌ Bad
SELECT * FROM orders WHERE order_id = '12345';  -- order_id is INT

-- ✅ Good
SELECT * FROM orders WHERE order_id = 12345;
```

**Scenario 2: Date String Comparison**
```sql
-- ❌ Bad: String comparison on DATE column
SELECT * FROM events WHERE event_date = '2025-01-01';  -- Implicit conversion

-- ✅ Good: Explicit DATE type
SELECT * FROM events WHERE event_date = DATE '2025-01-01';
```

**Scenario 3: UUID Format**
```sql
-- PostgreSQL: UUID column
-- ❌ Bad
SELECT * FROM records WHERE uuid_column = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890';

-- ✅ Good
SELECT * FROM records WHERE uuid_column = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'::uuid;
```

## Correlated Subqueries

### Problem Description

Subquery executes once per row in outer query, resulting in poor performance.

**Anti-Pattern:**
```sql
-- ❌ Bad: Correlated subquery
SELECT
  name,
  (SELECT COUNT(*) FROM orders WHERE orders.user_id = users.id) AS order_count
FROM users;
```

**Why It Fails:**
- Subquery executes once per user
- For 10,000 users → 10,000 subquery executions
- Even with indexes, overhead is significant

**Solution 1: JOIN with GROUP BY**
```sql
-- ✅ Good: Single query with JOIN
SELECT
  users.name,
  COUNT(orders.id) AS order_count
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.id, users.name;
```

**Solution 2: Lateral Join (PostgreSQL)**
```sql
-- ✅ Good: Lateral join for complex subqueries
SELECT
  users.name,
  recent_orders.order_count
FROM users
LEFT JOIN LATERAL (
  SELECT COUNT(*) AS order_count
  FROM orders
  WHERE orders.user_id = users.id
    AND orders.created_at > NOW() - INTERVAL '30 days'
) recent_orders ON true;
```

### Performance Comparison

**Test Case:** 10,000 users, 100,000 orders

```sql
-- Correlated subquery: ~5000ms
-- JOIN with GROUP BY: ~100ms
```

**Result:** 50x performance improvement

## Unnecessary DISTINCT

### Problem Description

Using DISTINCT when data is already unique adds expensive deduplication step.

**Anti-Pattern:**
```sql
-- ❌ Bad: DISTINCT on primary key (already unique)
SELECT DISTINCT id FROM users WHERE status = 'active';
```

**Why It Fails:**
- DISTINCT requires sorting or hashing
- Unnecessary overhead when uniqueness guaranteed
- Wasted CPU and memory

**Solution:**
```sql
-- ✅ Good: Remove DISTINCT (id is unique)
SELECT id FROM users WHERE status = 'active';
```

### When DISTINCT is Necessary

**Necessary Use Case:**
```sql
-- ✅ Good: DISTINCT needed for duplicate customer_ids
SELECT DISTINCT customer_id FROM orders WHERE status = 'completed';
```

**Alternative (often better):**
```sql
-- ✅ Better: Use GROUP BY (can add aggregations)
SELECT customer_id FROM orders WHERE status = 'completed' GROUP BY customer_id;
```

### DISTINCT in JOINs

**Anti-Pattern:**
```sql
-- ❌ Bad: DISTINCT to fix JOIN duplication
SELECT DISTINCT users.id, users.name
FROM users
INNER JOIN orders ON users.id = orders.user_id;
```

**Why It's Wrong:**
- DISTINCT is band-aid for incorrect JOIN
- Expensive deduplication

**Solution:**
```sql
-- ✅ Good: Use EXISTS or LEFT JOIN properly
SELECT id, name FROM users
WHERE EXISTS (SELECT 1 FROM orders WHERE orders.user_id = users.id);

-- Or if you need aggregation:
SELECT users.id, users.name, COUNT(orders.id) AS order_count
FROM users
INNER JOIN orders ON users.id = orders.user_id
GROUP BY users.id, users.name;
```

## OR vs IN Performance

### Problem Description

Multiple OR conditions can be slower than IN clause or UNION ALL.

**Anti-Pattern:**
```sql
-- ❌ Suboptimal: Multiple OR conditions
SELECT * FROM users
WHERE status = 'active'
   OR status = 'pending'
   OR status = 'verified'
   OR status = 'trial';
```

**Why It's Suboptimal:**
- May not use index efficiently
- Query planner may choose sequential scan

**Solution 1: Use IN**
```sql
-- ✅ Better: IN clause
SELECT * FROM users
WHERE status IN ('active', 'pending', 'verified', 'trial');
```

**Solution 2: Use UNION ALL (if separate indexes exist)**
```sql
-- ✅ Alternative: UNION ALL with separate index scans
SELECT * FROM users WHERE status = 'active'
UNION ALL
SELECT * FROM users WHERE status = 'pending'
UNION ALL
SELECT * FROM users WHERE status = 'verified'
UNION ALL
SELECT * FROM users WHERE status = 'trial';
```

### OR on Different Columns

**Anti-Pattern:**
```sql
-- ❌ Bad: OR on different columns
SELECT * FROM users WHERE email = 'x@y.com' OR phone = '555-1234';
```

**Why It Fails:**
- Cannot use indexes effectively
- Often results in sequential scan

**Solution: UNION ALL**
```sql
-- ✅ Good: UNION ALL allows index usage on both columns
SELECT * FROM users WHERE email = 'x@y.com'
UNION ALL
SELECT * FROM users WHERE phone = '555-1234';
```

## NOT IN with NULL Values

### Problem Description

NOT IN with NULL values returns unexpected results (empty set).

**Anti-Pattern:**
```sql
-- ❌ Bad: NOT IN with potential NULLs
SELECT * FROM users
WHERE id NOT IN (SELECT user_id FROM deleted_users);
-- Returns ZERO rows if any user_id is NULL!
```

**Why It Fails:**
- SQL three-valued logic (TRUE, FALSE, NULL)
- NULL in list makes entire NOT IN return NULL
- NULL is not TRUE, so row is excluded

**Solution 1: NOT EXISTS**
```sql
-- ✅ Good: NOT EXISTS handles NULLs correctly
SELECT * FROM users
WHERE NOT EXISTS (
  SELECT 1 FROM deleted_users WHERE deleted_users.user_id = users.id
);
```

**Solution 2: Filter NULLs in Subquery**
```sql
-- ✅ Also good: Explicitly exclude NULLs
SELECT * FROM users
WHERE id NOT IN (
  SELECT user_id FROM deleted_users WHERE user_id IS NOT NULL
);
```

### Performance Comparison

```sql
-- NOT IN: May be slower, fails with NULLs
-- NOT EXISTS: Usually faster, handles NULLs correctly
```

## Wildcard at Start of LIKE

### Problem Description

Leading wildcard in LIKE prevents index usage.

**Anti-Pattern:**
```sql
-- ❌ Bad: Leading wildcard
SELECT * FROM products WHERE name LIKE '%widget%';
```

**Why It Fails:**
- B-tree index cannot be used
- Must scan entire table
- Evaluate LIKE for every row

**Solution 1: Trailing Wildcard (if applicable)**
```sql
-- ✅ Good: Trailing wildcard can use index
SELECT * FROM products WHERE name LIKE 'super%';
```

**Solution 2: Full-Text Search**
```sql
-- PostgreSQL: Full-text search with GIN index
CREATE INDEX idx_products_name_fts ON products
  USING GIN (to_tsvector('english', name));

SELECT * FROM products
WHERE to_tsvector('english', name) @@ to_tsquery('english', 'widget');

-- MySQL: Full-text index
CREATE FULLTEXT INDEX idx_products_name_fulltext ON products (name);

SELECT * FROM products
WHERE MATCH(name) AGAINST('widget' IN NATURAL LANGUAGE MODE);
```

**Solution 3: Trigram Index (PostgreSQL)**
```sql
-- PostgreSQL: Trigram index for LIKE patterns
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_products_name_trgm ON products USING GIN (name gin_trgm_ops);

-- Now LIKE '%widget%' can use index
SELECT * FROM products WHERE name LIKE '%widget%';
```

## Quick Reference: Anti-Patterns Summary

| Anti-Pattern | Impact | Solution |
|-------------|--------|----------|
| SELECT * | Over-fetching, wasted I/O | SELECT specific columns |
| N+1 queries | Network latency × N | JOIN or IN clause |
| Missing FK indexes | Slow joins, cascades | Index all foreign keys |
| Functions on columns | No index usage | Sargable conditions or expression index |
| Type mismatch | Implicit conversion | Match data types |
| Correlated subquery | Subquery per row | JOIN with GROUP BY |
| Unnecessary DISTINCT | Expensive dedup | Remove if uniqueness guaranteed |
| Multiple ORs | Poor index usage | IN clause or UNION ALL |
| NOT IN with NULLs | Unexpected results | NOT EXISTS |
| Leading wildcard LIKE | Full table scan | Full-text or trigram index |

## Anti-Pattern Detection Queries

### PostgreSQL: Find SELECT * Queries

```sql
-- Enable query logging
ALTER DATABASE yourdb SET log_statement = 'all';

-- Analyze logs for SELECT * patterns
-- (requires log analysis tool or grep on log files)
```

### PostgreSQL: Find Missing Foreign Key Indexes

```sql
SELECT
  c.conrelid::regclass AS table_name,
  a.attname AS column_name,
  c.conname AS constraint_name
FROM pg_constraint c
JOIN pg_attribute a ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid
WHERE c.contype = 'f'
  AND NOT EXISTS (
    SELECT 1 FROM pg_index i
    WHERE i.indrelid = c.conrelid
      AND a.attnum = ANY(i.indkey)
  );
```

### SQL Server: Find Implicit Conversions

```sql
-- Check execution plans for warnings
-- Look for "CONVERT_IMPLICIT" warnings in graphical plans
```
