-- Query Rewriting Examples
-- Demonstrates converting anti-patterns to efficient queries

-- ============================================================================
-- Example 1: N+1 Query Problem → JOIN
-- ============================================================================

-- ❌ ANTI-PATTERN: N+1 Queries
-- Application executes:
-- Query 1:
SELECT * FROM users LIMIT 100;

-- Then for each user (100 queries):
SELECT * FROM posts WHERE user_id = ?;  -- Executed 100 times

-- Total: 101 database round trips
-- Time: ~1000ms

-- ✅ SOLUTION: Single JOIN Query
SELECT
  users.id,
  users.name,
  users.email,
  posts.id AS post_id,
  posts.title,
  posts.content,
  posts.created_at
FROM users
LEFT JOIN posts ON users.id = posts.user_id
WHERE users.id IN (1, 2, 3, ..., 100);

-- Total: 1 database round trip
-- Time: ~50ms
-- Result: 20x faster

-- Alternative: 2 Queries with IN Clause
-- Query 1:
SELECT * FROM users LIMIT 100;
-- Returns user IDs: 1, 2, 3, ..., 100

-- Query 2:
SELECT * FROM posts WHERE user_id IN (1, 2, 3, ..., 100);

-- Total: 2 database round trips
-- Time: ~100ms
-- Still 10x faster than N+1

-- ============================================================================
-- Example 2: SELECT * → Specific Columns
-- ============================================================================

-- ❌ ANTI-PATTERN: SELECT *
SELECT * FROM users WHERE id = 1;
-- Fetches all 50 columns
-- Data transfer: 5KB
-- Time: 10ms

-- ✅ SOLUTION: Select Specific Columns
SELECT id, name, email, created_at FROM users WHERE id = 1;
-- Fetches only 4 columns
-- Data transfer: 0.5KB
-- Time: 1ms
-- Result: 10x faster

-- ============================================================================
-- Example 3: Correlated Subquery → JOIN with GROUP BY
-- ============================================================================

-- ❌ ANTI-PATTERN: Correlated Subquery
SELECT
  name,
  (SELECT COUNT(*) FROM orders WHERE orders.user_id = users.id) AS order_count,
  (SELECT SUM(total) FROM orders WHERE orders.user_id = users.id) AS revenue
FROM users;
-- Subquery executes once per user
-- For 10,000 users: 20,000 subquery executions
-- Time: ~5000ms

-- ✅ SOLUTION: JOIN with GROUP BY
SELECT
  users.name,
  COUNT(orders.id) AS order_count,
  COALESCE(SUM(orders.total), 0) AS revenue
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.id, users.name;
-- Single scan of both tables
-- Time: ~100ms
-- Result: 50x faster

-- ============================================================================
-- Example 4: Non-Sargable → Sargable Condition
-- ============================================================================

-- ❌ ANTI-PATTERN: Function on Indexed Column
SELECT * FROM orders WHERE YEAR(created_at) = 2025;
-- Function prevents index usage
-- Sequential scan of entire table
-- Time: ~500ms

-- ✅ SOLUTION: Sargable Range Condition
SELECT * FROM orders
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01';
-- Can use index on created_at
-- Index scan
-- Time: ~50ms
-- Result: 10x faster

-- Another Example: String Function
-- ❌ ANTI-PATTERN
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';
-- LOWER() prevents index usage

-- ✅ SOLUTION 1: Expression Index (PostgreSQL)
CREATE INDEX idx_users_email_lower ON users (LOWER(email));
-- Query can now use index

-- ✅ SOLUTION 2: Store Lowercase Email
ALTER TABLE users ADD COLUMN email_lower VARCHAR(255)
  GENERATED ALWAYS AS (LOWER(email)) STORED;
CREATE INDEX idx_users_email_lower ON users (email_lower);

SELECT * FROM users WHERE email_lower = 'john@example.com';

-- ============================================================================
-- Example 5: IN vs EXISTS for Subqueries
-- ============================================================================

-- ❌ LESS EFFICIENT: IN with Large Subquery
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total > 1000);
-- Builds full list of user_ids
-- May create large temporary result set

-- ✅ MORE EFFICIENT: EXISTS
SELECT * FROM users
WHERE EXISTS (
  SELECT 1 FROM orders WHERE orders.user_id = users.id AND orders.total > 1000
);
-- Stops at first match per user
-- Semi-join optimization possible
-- Generally faster for large result sets

-- ============================================================================
-- Example 6: UNION vs UNION ALL
-- ============================================================================

-- ❌ UNNECESSARY: UNION (with deduplication)
SELECT id, name FROM active_users
UNION
SELECT id, name FROM trial_users;
-- Sorts and deduplicates
-- Time: ~500ms (for 100k rows)

-- ✅ EFFICIENT: UNION ALL (no deduplication)
SELECT id, name FROM active_users
UNION ALL
SELECT id, name FROM trial_users;
-- No sorting, no deduplication
-- Time: ~50ms
-- Result: 10x faster
-- Use when datasets don't overlap or duplicates are acceptable

-- ============================================================================
-- Example 7: COUNT(*) vs EXISTS for Existence Check
-- ============================================================================

-- ❌ INEFFICIENT: COUNT(*) for Existence
SELECT * FROM users
WHERE (SELECT COUNT(*) FROM orders WHERE orders.user_id = users.id) > 0;
-- Counts ALL matching rows

-- ✅ EFFICIENT: EXISTS
SELECT * FROM users
WHERE EXISTS (SELECT 1 FROM orders WHERE orders.user_id = users.id);
-- Stops at first match
-- Much faster when many matches exist

-- ============================================================================
-- Example 8: DISTINCT vs GROUP BY
-- ============================================================================

-- ❌ UNNECESSARY DISTINCT: On Already Unique Data
SELECT DISTINCT id FROM users WHERE status = 'active';
-- Unnecessary deduplication (id is unique)

-- ✅ SOLUTION: Remove DISTINCT
SELECT id FROM users WHERE status = 'active';
-- No deduplication overhead

-- Another Example: When Aggregation Needed
-- ❌ LESS EFFICIENT: DISTINCT to Fix JOIN
SELECT DISTINCT users.id, users.name
FROM users
INNER JOIN orders ON users.id = orders.user_id;

-- ✅ MORE EFFICIENT: GROUP BY or EXISTS
-- Option 1: GROUP BY with aggregation
SELECT users.id, users.name, COUNT(orders.id) AS order_count
FROM users
INNER JOIN orders ON users.id = orders.user_id
GROUP BY users.id, users.name;

-- Option 2: EXISTS (if no aggregation needed)
SELECT id, name FROM users
WHERE EXISTS (SELECT 1 FROM orders WHERE orders.user_id = users.id);

-- ============================================================================
-- Example 9: OR on Different Columns → UNION ALL
-- ============================================================================

-- ❌ LESS EFFICIENT: OR on Different Columns
SELECT * FROM users WHERE email = 'john@example.com' OR phone = '555-1234';
-- May not use indexes efficiently
-- Often results in sequential scan

-- ✅ MORE EFFICIENT: UNION ALL with Separate Index Scans
SELECT * FROM users WHERE email = 'john@example.com'
UNION ALL
SELECT * FROM users WHERE phone = '555-1234';
-- Each query can use its own index
-- Index scan on idx_users_email
-- Index scan on idx_users_phone
-- Generally faster with proper indexes

-- ============================================================================
-- Example 10: NOT IN → NOT EXISTS (Handling NULLs)
-- ============================================================================

-- ❌ ANTI-PATTERN: NOT IN with Potential NULLs
SELECT * FROM users
WHERE id NOT IN (SELECT user_id FROM deleted_users);
-- Returns ZERO rows if any user_id is NULL!
-- SQL three-valued logic issue

-- ✅ SOLUTION 1: NOT EXISTS
SELECT * FROM users
WHERE NOT EXISTS (
  SELECT 1 FROM deleted_users WHERE deleted_users.user_id = users.id
);
-- Handles NULLs correctly
-- Generally faster

-- ✅ SOLUTION 2: Filter NULLs in Subquery
SELECT * FROM users
WHERE id NOT IN (
  SELECT user_id FROM deleted_users WHERE user_id IS NOT NULL
);
-- Explicit NULL handling
-- Works correctly but slower than NOT EXISTS

-- ============================================================================
-- Example 11: Implicit Type Conversion → Explicit Types
-- ============================================================================

-- ❌ ANTI-PATTERN: Type Mismatch
SELECT * FROM users WHERE user_id = '123';  -- user_id is INT
-- Implicit conversion prevents index usage
-- Sequential scan

-- ✅ SOLUTION: Matching Types
SELECT * FROM users WHERE user_id = 123;
-- No conversion needed
-- Index scan
-- Much faster

-- ============================================================================
-- Example 12: Multiple OR → IN Clause
-- ============================================================================

-- ❌ LESS EFFICIENT: Multiple OR
SELECT * FROM users
WHERE status = 'active'
   OR status = 'pending'
   OR status = 'verified'
   OR status = 'trial';
-- May not optimize well

-- ✅ MORE EFFICIENT: IN Clause
SELECT * FROM users
WHERE status IN ('active', 'pending', 'verified', 'trial');
-- Better optimization
-- Cleaner query

-- ============================================================================
-- Example 13: Offset Pagination → Keyset Pagination
-- ============================================================================

-- ❌ INEFFICIENT: OFFSET for Deep Pagination
SELECT * FROM posts
ORDER BY created_at DESC
LIMIT 20 OFFSET 10000;
-- Processes and discards 10,000 rows
-- Performance degrades linearly with offset
-- Time for page 500: ~1000ms

-- ✅ EFFICIENT: Keyset/Cursor Pagination
-- Page 1:
SELECT id, title, created_at FROM posts
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Page 2 (using last_created_at and last_id from page 1):
SELECT id, title, created_at FROM posts
WHERE (created_at < '2025-01-15 10:30:00')
   OR (created_at = '2025-01-15 10:30:00' AND id < 12345)
ORDER BY created_at DESC, id DESC
LIMIT 20;
-- Constant performance regardless of page depth
-- Time for any page: ~10ms

-- Required index:
CREATE INDEX idx_posts_created_id ON posts (created_at DESC, id DESC);

-- ============================================================================
-- Example 14: Wildcard at Start → Trigram or Full-Text Index
-- ============================================================================

-- ❌ ANTI-PATTERN: Leading Wildcard
SELECT * FROM products WHERE name LIKE '%widget%';
-- Cannot use B-tree index
-- Full table scan

-- ✅ SOLUTION 1: Trailing Wildcard (if applicable)
SELECT * FROM products WHERE name LIKE 'super%';
-- Can use B-tree index

-- ✅ SOLUTION 2: Full-Text Search (PostgreSQL)
CREATE INDEX idx_products_name_fts
ON products USING GIN (to_tsvector('english', name));

SELECT * FROM products
WHERE to_tsvector('english', name) @@ to_tsquery('english', 'widget');

-- ✅ SOLUTION 3: Trigram Index (PostgreSQL)
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_products_name_trgm
ON products USING GIN (name gin_trgm_ops);

SELECT * FROM products WHERE name LIKE '%widget%';
-- Now can use trigram index

-- ============================================================================
-- Example 15: Window Function vs Correlated Subquery
-- ============================================================================

-- ❌ ANTI-PATTERN: Correlated Subquery for Ranking
SELECT
  product_name,
  category_id,
  sales,
  (SELECT COUNT(*)
   FROM products p2
   WHERE p2.category_id = products.category_id
     AND p2.sales > products.sales) + 1 AS rank_in_category
FROM products;
-- Subquery executes per row
-- Very slow for large tables

-- ✅ SOLUTION: Window Function
SELECT
  product_name,
  category_id,
  sales,
  RANK() OVER (PARTITION BY category_id ORDER BY sales DESC) AS rank_in_category
FROM products;
-- Single table scan
-- Much faster (10-100x)
