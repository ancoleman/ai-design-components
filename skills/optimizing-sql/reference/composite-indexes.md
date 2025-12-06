# Composite Index Design

Guide to designing multi-column composite indexes for optimal query performance.

## Column Order Rules

### Rule 1: Equality Filters First (Most Selective)

**Query Pattern:**
```sql
SELECT * FROM orders
WHERE customer_id = 123 AND status = 'shipped';
```

**Optimal Index:**
```sql
CREATE INDEX idx_orders_customer_status
ON orders (customer_id, status);
```

**Why:** Most selective filters first reduce index tree traversal.

### Rule 2: Range Filters After Equality

**Query Pattern:**
```sql
SELECT * FROM orders
WHERE customer_id = 123
  AND created_at > '2025-01-01';
```

**Optimal Index:**
```sql
CREATE INDEX idx_orders_customer_created
ON orders (customer_id, created_at);
```

**Why:** Equality narrows down to specific branch, then range scan within.

### Rule 3: ORDER BY Columns Last

**Query Pattern:**
```sql
SELECT * FROM orders
WHERE customer_id = 123
ORDER BY created_at DESC
LIMIT 10;
```

**Optimal Index:**
```sql
CREATE INDEX idx_orders_customer_created
ON orders (customer_id, created_at DESC);
```

**Why:** Pre-sorted results, no separate sort operation needed.

## Left-Prefix Rule

**Composite Index:** `(A, B, C)`

**Can Be Used For:**
- `WHERE A = ?`
- `WHERE A = ? AND B = ?`
- `WHERE A = ? AND B = ? AND C = ?`
- `WHERE A = ? ORDER BY B`

**Cannot Be Used For:**
- `WHERE B = ?` (skips leading column A)
- `WHERE C = ?` (skips leading columns A, B)
- `WHERE B = ? AND C = ?` (skips leading column A)

**Example:**
```sql
-- Index: (customer_id, status, created_at)

-- ✅ Uses index (customer_id)
SELECT * FROM orders WHERE customer_id = 123;

-- ✅ Uses index (customer_id, status)
SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending';

-- ✅ Uses full index
SELECT * FROM orders
WHERE customer_id = 123 AND status = 'pending' AND created_at > '2025-01-01';

-- ❌ Cannot use index (skips customer_id)
SELECT * FROM orders WHERE status = 'pending';
```

## Common Patterns

### Pattern 1: Multi-Tenant Application

**Query:**
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

**Why:** tenant_id first (always filtered), status second, updated_at for sorting.

### Pattern 2: Status + Time Range

**Query:**
```sql
SELECT * FROM tasks
WHERE status = 'pending' AND due_date < NOW();
```

**Index:**
```sql
CREATE INDEX idx_tasks_status_due
ON tasks (status, due_date);
```

### Pattern 3: Multiple Equality + Range

**Query:**
```sql
SELECT * FROM products
WHERE category_id = 5
  AND brand_id = 10
  AND price > 100;
```

**Index:**
```sql
CREATE INDEX idx_products_category_brand_price
ON products (category_id, brand_id, price);
```

**Column Order:** Most selective first, range last.

### Pattern 4: JOIN + Filter

**Query:**
```sql
SELECT * FROM order_items
INNER JOIN orders ON order_items.order_id = orders.id
WHERE orders.customer_id = 123;
```

**Indexes:**
```sql
-- Index on order_items for JOIN
CREATE INDEX idx_order_items_order ON order_items (order_id);

-- Composite index on orders
CREATE INDEX idx_orders_customer ON orders (customer_id);
```

## Selectivity Ordering

### High Selectivity → Low Selectivity

**Table:** 1,000,000 orders
- `customer_id`: 10,000 unique values (high selectivity)
- `status`: 5 unique values (low selectivity)

**Query:**
```sql
SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending';
```

**Optimal:**
```sql
CREATE INDEX idx_orders_customer_status ON orders (customer_id, status);
```

**Why:**
- `customer_id = 123` narrows to ~100 rows
- `status = 'pending'` filters within those 100 rows
- Much better than filtering 200,000 pending orders for customer_id

**Suboptimal:**
```sql
CREATE INDEX idx_orders_status_customer ON orders (status, customer_id);
```
- `status = 'pending'` starts with 200,000 rows
- Then filters for customer_id
- Larger initial scan

## Index vs Query Mismatch

### Mismatch Example

**Index:**
```sql
CREATE INDEX idx_orders_customer_status ON orders (customer_id, status);
```

**Query:**
```sql
-- ❌ Query uses status first (skips customer_id)
SELECT * FROM orders WHERE status = 'pending';
```

**Solution:** Create separate index for status-only queries:
```sql
CREATE INDEX idx_orders_status ON orders (status);
```

### Partial Index Solution (PostgreSQL)

Instead of full index on low-selectivity column:

```sql
-- ✅ Partial index for specific status
CREATE INDEX idx_orders_pending
ON orders (created_at)
WHERE status = 'pending';
```

## Including Non-Indexed Columns

### PostgreSQL INCLUDE Clause

**Query:**
```sql
SELECT customer_id, status, total, created_at
FROM orders
WHERE customer_id = 123;
```

**Covering Index:**
```sql
CREATE INDEX idx_orders_customer_covering
ON orders (customer_id)
INCLUDE (status, total, created_at);
```

**Benefit:** Index-Only Scan (no heap access).

### MySQL Approach

**Composite Index with Extra Columns:**
```sql
CREATE INDEX idx_orders_customer_covering
ON orders (customer_id, status, total, created_at);
```

**Trade-off:** Larger index, but enables covering scans.

### SQL Server INCLUDE Clause

**Covering Index:**
```sql
CREATE NONCLUSTERED INDEX IX_Orders_CustomerID
ON Orders (CustomerID)
INCLUDE (Status, Total, CreatedAt);
```

## Multi-Column vs Multiple Indexes

### Single Composite Index

**Index:**
```sql
CREATE INDEX idx_orders_customer_status ON orders (customer_id, status);
```

**Queries Supported:**
- `WHERE customer_id = ?`
- `WHERE customer_id = ? AND status = ?`

**Queries NOT Supported:**
- `WHERE status = ?` (skips leading column)

### Multiple Single-Column Indexes

**Indexes:**
```sql
CREATE INDEX idx_orders_customer ON orders (customer_id);
CREATE INDEX idx_orders_status ON orders (status);
```

**Queries Supported:**
- `WHERE customer_id = ?` (uses idx_orders_customer)
- `WHERE status = ?` (uses idx_orders_status)
- `WHERE customer_id = ? AND status = ?` (bitmap scan in PostgreSQL, index merge in MySQL)

**Trade-off:**
- More indexes = slower writes
- More flexible for varied query patterns

### Recommendation

**High-frequency query patterns:** Composite index
**Varied query patterns:** Multiple indexes or partial indexes

## Testing Composite Indexes

### Before Creating Index

```sql
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = 123 AND status = 'pending'
ORDER BY created_at DESC;
```

**Look for:**
- Sequential Scan / Table Scan
- High row counts
- Sort operation

### After Creating Index

```sql
CREATE INDEX idx_orders_customer_status_created
ON orders (customer_id, status, created_at DESC);

EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = 123 AND status = 'pending'
ORDER BY created_at DESC;
```

**Look for:**
- Index Scan / Index Seek
- Low row counts
- No sort operation (pre-sorted by index)

## Quick Reference

### Column Order Priority

1. **Equality filters** (most selective first)
2. **Additional equality filters** (by selectivity)
3. **Range filters** (after all equality)
4. **ORDER BY columns** (matching sort direction)
5. **GROUP BY columns** (if not already covered)

### Common Mistakes

**❌ Wrong order:**
```sql
CREATE INDEX ON orders (created_at, customer_id);
-- Query: WHERE customer_id = ? ORDER BY created_at
-- Inefficient: Large scan on created_at first
```

**✅ Correct order:**
```sql
CREATE INDEX ON orders (customer_id, created_at);
-- Query: WHERE customer_id = ? ORDER BY created_at
-- Efficient: Narrow by customer_id, then sorted by created_at
```

### Index Size Considerations

**Each additional column:**
- Increases index size by column width
- Slows down write operations slightly
- Enables more query patterns

**Balance:**
- 2-4 columns typical
- 5+ columns rare (diminishing returns)
