# Scan Types Interpretation

Detailed guide to understanding scan types and join algorithms across PostgreSQL, MySQL, and SQL Server.

## PostgreSQL Scan Types

### Sequential Scan (Seq Scan)

**Description:** Reads entire table sequentially from disk.

**When Used:**
- No suitable index available
- Small tables (optimizer determines full scan is cheaper)
- Query needs majority of table rows

**Performance:**
- Poor for large tables with selective WHERE clause
- Acceptable for small tables (<1000 rows)
- Acceptable when retrieving large percentage of rows

**Example:**
```sql
EXPLAIN SELECT * FROM users WHERE last_login < '2020-01-01';
```
```
Seq Scan on users  (cost=0.00..1500.00 rows=50000)
  Filter: (last_login < '2020-01-01')
```

**Optimization:** Add index on `last_login`

### Index Scan

**Description:** Traverses index to find matching rows, then fetches full rows from heap table.

**When Used:**
- Index available on WHERE/JOIN columns
- Small to medium result sets
- Random access pattern acceptable

**Performance:**
- Excellent for selective queries (<5% of table)
- Better than Seq Scan for most filtered queries

**Example:**
```sql
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';
```
```
Index Scan using idx_users_email on users  (cost=0.42..8.44 rows=1)
  Index Cond: (email = 'user@example.com')
```

**Key Indicator:** `Index Cond` shows index is being used.

### Index-Only Scan

**Description:** Retrieves all data from index without accessing heap table.

**When Used:**
- Covering index contains all needed columns
- Index includes WHERE and SELECT columns

**Performance:**
- Best possible performance
- No heap access required
- Minimal I/O

**Example:**
```sql
CREATE INDEX idx_users_email_covering ON users (email) INCLUDE (id, name);

EXPLAIN SELECT id, name FROM users WHERE email = 'user@example.com';
```
```
Index Only Scan using idx_users_email_covering on users  (cost=0.42..4.44 rows=1)
  Index Cond: (email = 'user@example.com')
```

**Optimization Goal:** Design covering indexes for frequently-run queries.

### Bitmap Heap Scan

**Description:** Two-step process:
1. Bitmap Index Scan: Create bitmap of matching row locations
2. Bitmap Heap Scan: Fetch rows from heap using bitmap

**When Used:**
- Medium-sized result sets (5-50% of table)
- Multiple index conditions combined with OR
- PostgreSQL optimizer determines it's more efficient than Index Scan

**Performance:**
- More efficient than Index Scan for medium result sets
- Allows combining multiple indexes

**Example:**
```sql
EXPLAIN SELECT * FROM orders WHERE status = 'pending' AND priority = 'high';
```
```
Bitmap Heap Scan on orders  (cost=20.00..500.00 rows=1000)
  Recheck Cond: ((status = 'pending') AND (priority = 'high'))
  -> Bitmap Index Scan on idx_orders_status  (cost=0.00..10.00 rows=2000)
        Index Cond: (status = 'pending')
  -> Bitmap Index Scan on idx_orders_priority  (cost=0.00..10.00 rows=1500)
        Index Cond: (priority = 'high')
```

**Key Indicator:** Multiple bitmap index scans combined.

## PostgreSQL Join Algorithms

### Nested Loop Join

**Description:** For each row in outer table, scan inner table for matches.

**When Used:**
- Small outer table
- Index on inner table join column
- Selective join conditions

**Performance:**
- Excellent when outer table is small (<100 rows)
- Poor when outer table is large

**Example:**
```sql
EXPLAIN SELECT * FROM small_table
INNER JOIN large_table ON small_table.id = large_table.small_id;
```
```
Nested Loop  (cost=0.42..100.00 rows=10)
  -> Seq Scan on small_table  (cost=0.00..1.10 rows=10)
  -> Index Scan using idx_large_small_id on large_table  (cost=0.42..9.89 rows=1)
        Index Cond: (small_id = small_table.id)
```

**Optimization:** Ensure inner table has index on join column.

### Hash Join

**Description:**
1. Build hash table of inner table
2. Probe hash table with outer table rows

**When Used:**
- Large tables being joined
- Equality join conditions (=)
- No suitable indexes

**Performance:**
- Excellent for large tables
- Memory-intensive (hash table must fit in work_mem)
- Single pass through each table

**Example:**
```sql
EXPLAIN SELECT * FROM orders
INNER JOIN customers ON orders.customer_id = customers.id;
```
```
Hash Join  (cost=500.00..5000.00 rows=10000)
  Hash Cond: (orders.customer_id = customers.id)
  -> Seq Scan on orders  (cost=0.00..1000.00 rows=10000)
  -> Hash  (cost=250.00..250.00 rows=5000)
        -> Seq Scan on customers  (cost=0.00..250.00 rows=5000)
```

**Tuning:** Increase `work_mem` if hash join spills to disk.

### Merge Join

**Description:**
1. Sort both tables by join key
2. Merge sorted results

**When Used:**
- Both tables already sorted by join key
- Merge join cheaper than hash join
- Equality join conditions

**Performance:**
- Excellent when data pre-sorted
- Expensive if sorting required
- Efficient for very large tables (no memory constraints)

**Example:**
```sql
EXPLAIN SELECT * FROM table1
INNER JOIN table2 ON table1.sorted_col = table2.sorted_col;
```
```
Merge Join  (cost=1000.00..2000.00 rows=10000)
  Merge Cond: (table1.sorted_col = table2.sorted_col)
  -> Index Scan using idx_table1_sorted on table1  (cost=0.00..500.00 rows=10000)
  -> Index Scan using idx_table2_sorted on table2  (cost=0.00..500.00 rows=10000)
```

**Optimization:** Add indexes matching join columns for pre-sorted data.

## MySQL Access Types

### ALL (Table Scan)

**Description:** Full table scan, reads every row.

**When Used:**
- No suitable index
- Small tables
- Query retrieves most rows

**Performance:**
- Worst performance for large tables
- Acceptable for small tables (<1000 rows)

**Example:**
```sql
EXPLAIN SELECT * FROM products WHERE description LIKE '%widget%';
```
```
type: ALL, rows: 50000
```

**Optimization:** Add index or use full-text search.

### const

**Description:** Single row lookup via primary key or unique index.

**When Used:**
- WHERE clause on primary key or unique index with constant value
- Comparison with constant value

**Performance:**
- Best possible performance
- Single row access

**Example:**
```sql
EXPLAIN SELECT * FROM users WHERE id = 123;
```
```
type: const, key: PRIMARY, rows: 1
```

**Key Indicator:** `type: const`, `rows: 1`

### eq_ref

**Description:** One row from table for each combination of rows from previous tables.

**When Used:**
- JOIN on primary key or unique index
- All parts of index used

**Performance:**
- Excellent for joins
- One row per outer table row

**Example:**
```sql
EXPLAIN SELECT * FROM orders
INNER JOIN customers ON orders.customer_id = customers.id;
```
```
type: eq_ref, key: PRIMARY, ref: orders.customer_id, rows: 1
```

### ref

**Description:** Non-unique index lookup.

**When Used:**
- Index used but not unique
- Multiple rows may match

**Performance:**
- Good performance
- Efficient for moderately selective queries

**Example:**
```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 123;
```
```
type: ref, key: idx_orders_customer, ref: const, rows: 10
```

### range

**Description:** Index range scan using BETWEEN, <, >, IN, LIKE.

**When Used:**
- Range conditions on indexed columns
- IN with small list
- LIKE with prefix (not wildcard at start)

**Performance:**
- Good performance
- Better than full table scan

**Example:**
```sql
EXPLAIN SELECT * FROM orders WHERE created_at > '2025-01-01';
```
```
type: range, key: idx_orders_created, rows: 1000
```

### index

**Description:** Full index scan (reads entire index).

**When Used:**
- All needed columns in index (covering index)
- Scanning entire index cheaper than table scan

**Performance:**
- Better than ALL if index smaller than table
- Still inefficient for large indexes

**Example:**
```sql
EXPLAIN SELECT id FROM users;
```
```
type: index, key: PRIMARY, rows: 100000
```

## SQL Server Scan Types

### Table Scan

**Description:** Reads entire heap table (no clustered index).

**When Used:**
- Table has no clustered index
- No suitable non-clustered index

**Performance:**
- Worst performance
- Entire table read from disk

**Optimization:** Add clustered index or non-clustered index.

### Clustered Index Scan

**Description:** Reads entire clustered index (reads all table data).

**When Used:**
- Query needs most/all rows
- No filtering or non-sargable WHERE clause

**Performance:**
- Similar to table scan
- Entire table scanned

**Example:**
```sql
-- Execution plan shows "Clustered Index Scan"
SELECT * FROM Orders WHERE YEAR(OrderDate) = 2025;
```

**Optimization:** Make WHERE clause sargable or add non-clustered index.

### Index Seek

**Description:** Efficient index traversal to specific rows.

**When Used:**
- WHERE clause uses indexed columns
- Sargable query conditions

**Performance:**
- Best performance
- Minimal I/O

**Example:**
```sql
-- Execution plan shows "Index Seek"
SELECT * FROM Orders WHERE OrderID = 12345;
```

**Key Indicator:** Seek operation in graphical plan.

### Index Scan

**Description:** Reads entire index (not entire table).

**When Used:**
- Covering index contains all needed columns
- Non-sargable conditions

**Performance:**
- Better than table scan if index smaller
- Not as efficient as Index Seek

**Example:**
```sql
-- Execution plan shows "Index Scan" on non-clustered index
SELECT CustomerID FROM Orders;
```

### Key Lookup (RID Lookup / Bookmark Lookup)

**Description:** After index seek, additional lookup to retrieve non-indexed columns.

**When Used:**
- Non-clustered index seek finds rows
- Additional columns needed not in index

**Performance:**
- Additional I/O per row
- Indicates covering index opportunity

**Example:**
```sql
-- Index on CustomerID, but SELECT includes other columns
SELECT * FROM Orders WHERE CustomerID = 123;
```
```
Index Seek (idx_Orders_CustomerID)
  -> Key Lookup (retrieve remaining columns)
```

**Optimization:** Create covering index with INCLUDE clause:
```sql
CREATE NONCLUSTERED INDEX idx_Orders_CustomerID_Covering
ON Orders (CustomerID)
INCLUDE (OrderDate, TotalAmount);
```

## Performance Hierarchy

### PostgreSQL (Best to Worst)

1. Index-Only Scan
2. Index Scan
3. Bitmap Heap Scan
4. Sequential Scan

### MySQL (Best to Worst)

1. system
2. const
3. eq_ref
4. ref
5. range
6. index
7. ALL

### SQL Server (Best to Worst)

1. Index Seek (non-clustered)
2. Clustered Index Seek
3. Index Scan (covering index)
4. Clustered Index Scan
5. Table Scan

## Decision Matrix: When to Add Index

| Scan Type | Rows Examined | Rows Returned | Action |
|-----------|---------------|---------------|--------|
| Seq Scan / ALL | >10,000 | <1% | ADD INDEX |
| Seq Scan / ALL | >10,000 | 1-10% | ADD INDEX |
| Seq Scan / ALL | >10,000 | >50% | OK (full scan appropriate) |
| Index Scan | Any | <5% | GOOD |
| Bitmap Heap Scan | Any | 5-50% | GOOD (PostgreSQL optimization) |
| Hash Join | Large tables | Any | Consider indexes on join columns |

## Common Optimization Patterns

### Pattern 1: Seq Scan → Index Scan

**Symptom:**
```
Seq Scan on table  (cost=0.00..10000.00 rows=1)
  Filter: (column = value)
  Rows Removed by Filter: 999999
```

**Solution:**
```sql
CREATE INDEX idx_table_column ON table (column);
```

### Pattern 2: Index Scan → Index-Only Scan

**Symptom:**
```
Index Scan using idx_table_column on table  (cost=0.42..100.00 rows=10)
  Index Cond: (column = value)
```

**Solution:** Create covering index
```sql
CREATE INDEX idx_table_column_covering
ON table (column) INCLUDE (other_column1, other_column2);
```

### Pattern 3: Nested Loop → Hash Join

**Symptom:**
```
Nested Loop  (cost=0.00..100000.00 rows=10000)
  -> Seq Scan on large_outer  (rows=10000)
  -> Index Scan on large_inner
```

**Solution:** Add index to outer table to reduce rows, or let optimizer choose hash join.

### Pattern 4: Multiple Index Scans → Composite Index

**Symptom:**
```
Bitmap Heap Scan on table
  -> Bitmap Index Scan on idx_col1
  -> Bitmap Index Scan on idx_col2
```

**Solution:** Create composite index
```sql
CREATE INDEX idx_table_col1_col2 ON table (col1, col2);
```

## Quick Reference

### Scan Type Performance

| Database | Best | Good | Acceptable | Poor |
|----------|------|------|------------|------|
| PostgreSQL | Index-Only Scan | Index Scan, Bitmap Heap Scan | - | Seq Scan |
| MySQL | const, eq_ref | ref, range | index | ALL |
| SQL Server | Index Seek | Index Scan (covering) | Clustered Index Scan | Table Scan |

### When Each Scan Type is OK

- **Sequential/Full Table Scan**: Small tables (<1000 rows), or query needs >50% of rows
- **Index Scan**: Selective queries (<10% of rows), index available
- **Index-Only Scan**: Always preferred when possible (covering index)
- **Bitmap Heap Scan**: Medium result sets (PostgreSQL optimization)
- **Nested Loop**: Small outer table with index on inner join column
- **Hash Join**: Large tables, equality joins, no suitable indexes
