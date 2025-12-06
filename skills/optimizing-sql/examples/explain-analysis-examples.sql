-- EXPLAIN Analysis Examples
-- Demonstrates before/after query optimization using EXPLAIN/EXPLAIN ANALYZE

-- ============================================================================
-- Example 1: Adding Index to Eliminate Sequential Scan (PostgreSQL)
-- ============================================================================

-- BEFORE: Sequential scan on users table
-- ❌ SLOW: Full table scan
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'john@example.com';
/*
Expected output:
Seq Scan on users  (cost=0.00..1500.00 rows=1 width=100) (actual time=50.123..50.124 rows=1 loops=1)
  Filter: (email = 'john@example.com'::text)
  Rows Removed by Filter: 99999
Planning Time: 0.100 ms
Execution Time: 50.150 ms
*/

-- ADD INDEX
CREATE INDEX idx_users_email ON users (email);

-- AFTER: Index scan
-- ✅ FAST: Direct index lookup
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'john@example.com';
/*
Expected output:
Index Scan using idx_users_email on users  (cost=0.42..8.44 rows=1 width=100) (actual time=0.025..0.026 rows=1 loops=1)
  Index Cond: (email = 'john@example.com'::text)
Planning Time: 0.150 ms
Execution Time: 0.050 ms

Result: 1000x faster (50ms → 0.05ms)
*/

-- ============================================================================
-- Example 2: Composite Index for Multi-Column WHERE (PostgreSQL)
-- ============================================================================

-- BEFORE: Sequential scan or single-column index
-- ❌ SLOW: Filters on multiple columns without optimal index
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = 123 AND status = 'pending'
ORDER BY created_at DESC
LIMIT 10;
/*
Expected output (no index):
Limit  (cost=10000.00..10010.00 rows=10 width=200)
  -> Sort  (cost=10000.00..10500.00 rows=1000 width=200)
        Sort Key: created_at DESC
        -> Seq Scan on orders  (cost=0.00..9000.00 rows=1000 width=200)
              Filter: ((customer_id = 123) AND (status = 'pending'::text))
              Rows Removed by Filter: 99000
*/

-- ADD COMPOSITE INDEX
CREATE INDEX idx_orders_customer_status_created
ON orders (customer_id, status, created_at DESC);

-- AFTER: Index scan with no sort
-- ✅ FAST: Uses composite index for filter and sort
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = 123 AND status = 'pending'
ORDER BY created_at DESC
LIMIT 10;
/*
Expected output:
Limit  (cost=0.42..15.44 rows=10 width=200)
  -> Index Scan using idx_orders_customer_status_created on orders  (cost=0.42..150.00 rows=100 width=200)
        Index Cond: ((customer_id = 123) AND (status = 'pending'::text))

Result: 100x faster, no sort operation
*/

-- ============================================================================
-- Example 3: MySQL EXPLAIN for Index Analysis
-- ============================================================================

-- BEFORE: Full table scan
-- ❌ SLOW: type = ALL
EXPLAIN SELECT * FROM products WHERE category_id = 5 AND price > 100;
/*
Expected output:
+----+-------------+----------+------+---------------+------+---------+------+-------+-------------+
| id | select_type | table    | type | possible_keys | key  | key_len | ref  | rows  | Extra       |
+----+-------------+----------+------+---------------+------+---------+------+-------+-------------+
|  1 | SIMPLE      | products | ALL  | NULL          | NULL | NULL    | NULL | 50000 | Using where |
+----+-------------+----------+------+---------------+------+---------+------+-------+-------------+

Problem: type = ALL (full table scan), rows = 50000
*/

-- ADD COMPOSITE INDEX
CREATE INDEX idx_products_category_price ON products (category_id, price);

-- AFTER: Range scan
-- ✅ FAST: type = range
EXPLAIN SELECT * FROM products WHERE category_id = 5 AND price > 100;
/*
Expected output:
+----+-------------+----------+-------+------------------------------+------------------------------+---------+------+------+-------------+
| id | select_type | table    | type  | possible_keys                | key                          | key_len | ref  | rows | Extra       |
+----+-------------+----------+-------+------------------------------+------------------------------+---------+------+------+-------------+
|  1 | SIMPLE      | products | range | idx_products_category_price  | idx_products_category_price  | 9       | NULL | 150  | Using where |
+----+-------------+----------+-------+------------------------------+------------------------------+---------+------+------+-------------+

Result: type = range, rows reduced from 50000 to 150
*/

-- ============================================================================
-- Example 4: Covering Index for Index-Only Scan (PostgreSQL)
-- ============================================================================

-- BEFORE: Index scan + heap fetch
-- ❌ SLOW: Must access heap table for non-indexed columns
EXPLAIN ANALYZE
SELECT id, name, email FROM users WHERE email = 'john@example.com';
/*
Expected output:
Index Scan using idx_users_email on users  (cost=0.42..8.44 rows=1 width=100)
  Index Cond: (email = 'john@example.com'::text)

Note: Heap Fetches needed for 'id' and 'name'
*/

-- ADD COVERING INDEX
CREATE INDEX idx_users_email_covering
ON users (email) INCLUDE (id, name);

-- AFTER: Index-only scan
-- ✅ FAST: All data from index, no heap access
EXPLAIN ANALYZE
SELECT id, name, email FROM users WHERE email = 'john@example.com';
/*
Expected output:
Index Only Scan using idx_users_email_covering on users  (cost=0.42..4.44 rows=1 width=50)
  Index Cond: (email = 'john@example.com'::text)
  Heap Fetches: 0

Result: 2x faster, no heap access
*/

-- ============================================================================
-- Example 5: Fixing Non-Sargable Query (PostgreSQL)
-- ============================================================================

-- BEFORE: Function on indexed column
-- ❌ SLOW: Cannot use index (function on column)
EXPLAIN ANALYZE
SELECT * FROM orders WHERE YEAR(created_at) = 2025;
/*
Expected output:
Seq Scan on orders  (cost=0.00..5000.00 rows=1000 width=200)
  Filter: (YEAR(created_at) = 2025)
  Rows Removed by Filter: 99000

Problem: YEAR() function prevents index usage
*/

-- REWRITE: Sargable condition
-- ✅ FAST: Range condition can use index
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01';
/*
Expected output:
Index Scan using idx_orders_created on orders  (cost=0.42..500.00 rows=1000 width=200)
  Index Cond: ((created_at >= '2025-01-01') AND (created_at < '2026-01-01'))

Result: 10x faster, uses index
*/

-- Alternative: Expression index (if function is necessary)
CREATE INDEX idx_orders_created_year ON orders (EXTRACT(YEAR FROM created_at));

-- ============================================================================
-- Example 6: Join Optimization (PostgreSQL)
-- ============================================================================

-- BEFORE: Missing index on foreign key
-- ❌ SLOW: Sequential scan on orders for each customer
EXPLAIN ANALYZE
SELECT customers.name, COUNT(orders.id) AS order_count
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
GROUP BY customers.id, customers.name;
/*
Expected output:
HashAggregate  (cost=15000.00..16000.00 rows=10000 width=100)
  Group Key: customers.id, customers.name
  -> Hash Left Join  (cost=2000.00..10000.00 rows=100000 width=50)
        Hash Cond: (customers.id = orders.customer_id)
        -> Seq Scan on customers  (cost=0.00..500.00 rows=10000 width=50)
        -> Hash  (cost=5000.00..5000.00 rows=100000 width=8)
              -> Seq Scan on orders  (cost=0.00..5000.00 rows=100000 width=8)

Problem: Sequential scan on orders table
*/

-- ADD INDEX on foreign key
CREATE INDEX idx_orders_customer ON orders (customer_id);

-- AFTER: Index scan on orders
-- ✅ FAST: Uses index for join
EXPLAIN ANALYZE
SELECT customers.name, COUNT(orders.id) AS order_count
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
GROUP BY customers.id, customers.name;
/*
Expected output:
HashAggregate  (cost=8000.00..9000.00 rows=10000 width=100)
  Group Key: customers.id, customers.name
  -> Hash Left Join  (cost=2000.00..6000.00 rows=100000 width=50)
        Hash Cond: (customers.id = orders.customer_id)
        -> Seq Scan on customers  (cost=0.00..500.00 rows=10000 width=50)
        -> Hash  (cost=2000.00..2000.00 rows=100000 width=8)
              -> Index Scan using idx_orders_customer on orders  (cost=0.00..2000.00 rows=100000 width=8)

Result: 2-3x faster, uses index for join
*/

-- ============================================================================
-- Example 7: SQL Server Execution Plan Analysis
-- ============================================================================

-- In SQL Server Management Studio:
-- 1. Enable "Include Actual Execution Plan" (Ctrl+M)
-- 2. Run query
-- 3. View execution plan tab

-- BEFORE: Clustered Index Scan (full table scan)
-- ❌ SLOW: Reads entire table
SELECT * FROM Sales.Orders WHERE CustomerID = 123;
/*
Graphical Plan shows:
  Clustered Index Scan on Orders
  Cost: 100%
  Rows: 100,000 (estimated)

Warning: Missing index suggestion
*/

-- ADD NON-CLUSTERED INDEX
CREATE NONCLUSTERED INDEX IX_Orders_CustomerID
ON Sales.Orders (CustomerID);

-- AFTER: Index Seek
-- ✅ FAST: Direct index lookup
SELECT * FROM Sales.Orders WHERE CustomerID = 123;
/*
Graphical Plan shows:
  Index Seek on IX_Orders_CustomerID
    -> Key Lookup (clustered) to retrieve remaining columns
  Cost: 5%
  Rows: 150 (estimated)

Result: 95% cost reduction
*/

-- Further optimization: Covering index to eliminate Key Lookup
CREATE NONCLUSTERED INDEX IX_Orders_CustomerID_Covering
ON Sales.Orders (CustomerID)
INCLUDE (OrderDate, TotalAmount, Status);

DROP INDEX IX_Orders_CustomerID ON Sales.Orders;

-- AFTER: Index Seek only (no Key Lookup)
-- ✅ FASTEST: All data from index
SELECT CustomerID, OrderDate, TotalAmount, Status
FROM Sales.Orders
WHERE CustomerID = 123;
/*
Graphical Plan shows:
  Index Seek on IX_Orders_CustomerID_Covering
  Cost: 2%
  No Key Lookup needed

Result: 98% cost reduction
*/
