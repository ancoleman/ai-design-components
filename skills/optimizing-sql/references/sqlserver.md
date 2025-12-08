# SQL Server-Specific Optimizations

SQL Server-specific features, execution plans, and optimization techniques.

## SQL Server Index Types

### Clustered Index

**Characteristics:**
- Table data physically sorted by index key
- One per table
- Primary key creates clustered index by default

**Creation:**
```sql
-- Explicit clustered index
CREATE CLUSTERED INDEX IX_Orders_OrderDate
ON Orders (OrderDate);

-- Primary key with clustered index (default)
CREATE TABLE Orders (
  OrderID INT PRIMARY KEY CLUSTERED,
  ...
);
```

**Benefits:**
- Fast range queries on index key
- Fast ORDER BY on index columns

**Considerations:**
- Choose narrow, unique, sequential key (avoid GUID)
- Use INT IDENTITY or BIGINT IDENTITY

### Non-Clustered Index

**Characteristics:**
- Separate structure from table data
- Multiple non-clustered indexes per table
- Includes pointer to clustered index key

**Creation:**
```sql
CREATE NONCLUSTERED INDEX IX_Orders_CustomerID
ON Orders (CustomerID);
```

### Covering Index with INCLUDE

**Use Case:** Include non-indexed columns for Index-Only Scans.

**Syntax:**
```sql
CREATE NONCLUSTERED INDEX IX_Orders_CustomerID_Covering
ON Orders (CustomerID)
INCLUDE (OrderDate, TotalAmount, Status);
```

**Query Benefits:**
```sql
-- Uses covering index (no Key Lookup)
SELECT OrderDate, TotalAmount, Status
FROM Orders
WHERE CustomerID = 123;
```

### Filtered Index

**Use Case:** Index subset of rows (similar to PostgreSQL partial index).

**Creation:**
```sql
-- Index only active orders
CREATE NONCLUSTERED INDEX IX_Orders_Active
ON Orders (OrderDate)
WHERE Status = 'Active';

-- Index only recent orders
CREATE NONCLUSTERED INDEX IX_Orders_Recent
ON Orders (OrderDate)
WHERE OrderDate >= '2025-01-01';
```

**Benefits:**
- Smaller index size
- Faster maintenance
- More efficient for common filtered queries

### Columnstore Index

**Use Case:** Data warehouse, analytics queries.

**Clustered Columnstore:**
```sql
-- Convert entire table to columnstore
CREATE CLUSTERED COLUMNSTORE INDEX CCI_Sales
ON Sales;
```

**Non-Clustered Columnstore:**
```sql
-- Add columnstore index alongside rowstore
CREATE NONCLUSTERED COLUMNSTORE INDEX NCCI_Sales
ON Sales (ProductID, OrderDate, Quantity, Amount);
```

**Benefits:**
- 10x compression
- 10-100x faster aggregation queries
- Batch mode execution

**When to Use:**
- Large fact tables (millions of rows)
- Read-heavy analytical queries
- Data warehouse scenarios

## SQL Server Execution Plans

### Accessing Execution Plans

**Estimated Execution Plan (Ctrl+L):**
- No query execution
- Estimated costs and row counts
- Quick analysis

**Actual Execution Plan (Ctrl+M, then execute):**
- Query executes
- Actual row counts and timing
- More accurate for optimization

### Reading Execution Plans

**Graphical Plan Direction:** Right to left, top to bottom.

**Operation Icons:**
- **Clustered Index Scan** - Full table scan (expensive)
- **Clustered Index Seek** - Efficient lookup (good)
- **Index Seek** - Non-clustered index lookup (good)
- **Index Scan** - Full index scan (less efficient)
- **Table Scan** - Full heap scan (worst)
- **Key Lookup** - Additional lookup for non-indexed columns
- **Nested Loops** - Join algorithm
- **Hash Match** - Join or aggregation

**Arrow Thickness:** Relative row count (thicker = more rows).

**Warnings (Yellow Exclamation Mark):**
- Missing index suggestion
- Implicit type conversion
- Excessive memory grant
- Spills to tempdb

### Missing Index Suggestions

**Execution Plan Recommendation:**
```xml
<MissingIndexes>
  <MissingIndexGroup Impact="95.5">
    <MissingIndex Database="YourDB" Schema="dbo" Table="Orders">
      <ColumnGroup Usage="EQUALITY">
        <Column Name="CustomerID" />
      </ColumnGroup>
      <ColumnGroup Usage="INCLUDE">
        <Column Name="OrderDate" />
        <Column Name="TotalAmount" />
      </ColumnGroup>
    </MissingIndex>
  </MissingIndexGroup>
</MissingIndexes>
```

**Create Suggested Index:**
```sql
CREATE NONCLUSTERED INDEX IX_Orders_CustomerID
ON Orders (CustomerID)
INCLUDE (OrderDate, TotalAmount);
```

## SQL Server Query Store

### Enable Query Store

**Database-Level Setting:**
```sql
ALTER DATABASE YourDatabase
SET QUERY_STORE = ON (
  OPERATION_MODE = READ_WRITE,
  DATA_FLUSH_INTERVAL_SECONDS = 900,
  INTERVAL_LENGTH_MINUTES = 60,
  MAX_STORAGE_SIZE_MB = 1000,
  QUERY_CAPTURE_MODE = AUTO
);
```

### Find Expensive Queries

**Top Queries by Duration:**
```sql
SELECT TOP 10
  q.query_id,
  qt.query_sql_text,
  rs.avg_duration / 1000.0 AS avg_duration_ms,
  rs.avg_logical_io_reads,
  rs.avg_physical_io_reads,
  rs.count_executions,
  rs.last_execution_time
FROM sys.query_store_query q
INNER JOIN sys.query_store_query_text qt
  ON q.query_text_id = qt.query_text_id
INNER JOIN sys.query_store_plan p
  ON q.query_id = p.query_id
INNER JOIN sys.query_store_runtime_stats rs
  ON p.plan_id = rs.plan_id
WHERE rs.last_execution_time > DATEADD(DAY, -7, GETDATE())
ORDER BY rs.avg_duration DESC;
```

**Top Queries by CPU:**
```sql
SELECT TOP 10
  qt.query_sql_text,
  rs.avg_cpu_time / 1000.0 AS avg_cpu_ms,
  rs.count_executions,
  rs.avg_duration / 1000.0 AS avg_duration_ms
FROM sys.query_store_query q
INNER JOIN sys.query_store_query_text qt
  ON q.query_text_id = qt.query_text_id
INNER JOIN sys.query_store_plan p
  ON q.query_id = p.query_id
INNER JOIN sys.query_store_runtime_stats rs
  ON p.plan_id = rs.plan_id
ORDER BY rs.avg_cpu_time DESC;
```

### Query Performance Comparison

**Compare Plans Over Time:**
```sql
-- Track query performance regression
SELECT
  q.query_id,
  qt.query_sql_text,
  p.plan_id,
  rs.avg_duration / 1000.0 AS avg_duration_ms,
  rs.first_execution_time,
  rs.last_execution_time
FROM sys.query_store_query q
INNER JOIN sys.query_store_query_text qt
  ON q.query_text_id = qt.query_text_id
INNER JOIN sys.query_store_plan p
  ON q.query_id = p.query_id
INNER JOIN sys.query_store_runtime_stats rs
  ON p.plan_id = rs.plan_id
WHERE q.query_id = 123  -- Specific query
ORDER BY rs.first_execution_time;
```

## SQL Server-Specific Optimizations

### Statistics Management

**Update Statistics:**
```sql
-- Update all statistics for table
UPDATE STATISTICS Orders;

-- Update specific index statistics
UPDATE STATISTICS Orders IX_Orders_CustomerID;

-- Update with full scan (more accurate)
UPDATE STATISTICS Orders WITH FULLSCAN;
```

**Auto-Update Statistics:**
```sql
-- Check setting
SELECT name, is_auto_update_stats_on
FROM sys.databases
WHERE name = 'YourDatabase';

-- Enable auto-update
ALTER DATABASE YourDatabase
SET AUTO_UPDATE_STATISTICS ON;
```

### Index Fragmentation

**Check Fragmentation:**
```sql
SELECT
  OBJECT_NAME(ips.object_id) AS TableName,
  i.name AS IndexName,
  ips.index_type_desc,
  ips.avg_fragmentation_in_percent,
  ips.page_count
FROM sys.dm_db_index_physical_stats(
  DB_ID(), NULL, NULL, NULL, 'LIMITED'
) ips
INNER JOIN sys.indexes i
  ON ips.object_id = i.object_id
  AND ips.index_id = i.index_id
WHERE ips.avg_fragmentation_in_percent > 10
  AND ips.page_count > 1000
ORDER BY ips.avg_fragmentation_in_percent DESC;
```

**Rebuild vs Reorganize:**
```sql
-- Rebuild index (offline, faster, more thorough)
ALTER INDEX IX_Orders_CustomerID ON Orders REBUILD;

-- Rebuild online (SQL Server Enterprise)
ALTER INDEX IX_Orders_CustomerID ON Orders REBUILD WITH (ONLINE = ON);

-- Reorganize index (online, slower, less thorough)
ALTER INDEX IX_Orders_CustomerID ON Orders REORGANIZE;
```

**Guidelines:**
- **Fragmentation <10%**: No action needed
- **Fragmentation 10-30%**: REORGANIZE
- **Fragmentation >30%**: REBUILD

### Partitioning

**Partition Function:**
```sql
-- Create partition function (monthly partitions)
CREATE PARTITION FUNCTION PF_Orders_Monthly (DATE)
AS RANGE RIGHT FOR VALUES
  ('2025-01-01', '2025-02-01', '2025-03-01', ..., '2025-12-01');
```

**Partition Scheme:**
```sql
-- Create partition scheme
CREATE PARTITION SCHEME PS_Orders_Monthly
AS PARTITION PF_Orders_Monthly
ALL TO ([PRIMARY]);
```

**Partitioned Table:**
```sql
-- Create partitioned table
CREATE TABLE Orders (
  OrderID INT IDENTITY(1,1),
  OrderDate DATE,
  CustomerID INT,
  TotalAmount DECIMAL(10,2),
  ...
) ON PS_Orders_Monthly (OrderDate);
```

**Benefits:**
- Partition elimination (scan only relevant partitions)
- Partition switching (fast archive/purge)
- Parallel query execution per partition

### Computed Columns

**Persisted Computed Column:**
```sql
ALTER TABLE Users
ADD FullName AS (FirstName + ' ' + LastName) PERSISTED;

-- Index computed column
CREATE INDEX IX_Users_FullName ON Users (FullName);
```

**Non-Persisted Computed Column:**
```sql
ALTER TABLE Users
ADD EmailDomain AS (SUBSTRING(Email, CHARINDEX('@', Email) + 1, LEN(Email)));
-- Computed on read, no storage overhead
```

## SQL Server Configuration

### Max Degree of Parallelism (MAXDOP)

**Check Current Setting:**
```sql
SELECT value_in_use
FROM sys.configurations
WHERE name = 'max degree of parallelism';
```

**Set MAXDOP:**
```sql
-- Limit to 4 cores per query
EXEC sp_configure 'max degree of parallelism', 4;
RECONFIGURE;
```

**Recommendation:**
- Small servers (<8 cores): MAXDOP = 4
- Large servers (>8 cores): MAXDOP = 8
- OLTP workloads: Lower MAXDOP (2-4)
- Analytics workloads: Higher MAXDOP (8-16)

### Cost Threshold for Parallelism

**Set Threshold:**
```sql
-- Only parallelize queries with cost > 50
EXEC sp_configure 'cost threshold for parallelism', 50;
RECONFIGURE;
```

**Default:** 5 (too low for most systems)
**Recommended:** 50-100

### Memory Configuration

**Max Server Memory:**
```sql
-- Reserve memory for OS and other apps
-- Example: 32GB server, allocate 28GB to SQL Server
EXEC sp_configure 'max server memory (MB)', 28672;
RECONFIGURE;
```

**Recommendation:**
- Leave 4GB for OS on small servers
- Leave 10-20% for OS on large servers

## SQL Server Monitoring

### DMVs for Query Performance

**Most Expensive Queries (CPU):**
```sql
SELECT TOP 10
  SUBSTRING(qt.text, (qs.statement_start_offset/2)+1,
    ((CASE qs.statement_end_offset
      WHEN -1 THEN DATALENGTH(qt.text)
      ELSE qs.statement_end_offset
    END - qs.statement_start_offset)/2)+1) AS query_text,
  qs.execution_count,
  qs.total_worker_time / 1000 AS total_cpu_ms,
  qs.total_worker_time / qs.execution_count / 1000 AS avg_cpu_ms,
  qs.last_execution_time
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY qs.total_worker_time DESC;
```

**Missing Indexes:**
```sql
SELECT
  mid.database_id,
  mid.object_id,
  OBJECT_NAME(mid.object_id, mid.database_id) AS table_name,
  migs.avg_user_impact,
  migs.user_seeks,
  mid.equality_columns,
  mid.inequality_columns,
  mid.included_columns
FROM sys.dm_db_missing_index_details mid
INNER JOIN sys.dm_db_missing_index_groups mig
  ON mid.index_handle = mig.index_handle
INNER JOIN sys.dm_db_missing_index_group_stats migs
  ON mig.index_group_handle = migs.group_handle
WHERE migs.avg_user_impact > 50
ORDER BY migs.avg_user_impact DESC;
```

### Blocking and Waits

**Current Blocking:**
```sql
SELECT
  blocking.session_id AS blocking_session,
  blocked.session_id AS blocked_session,
  blocked_text.text AS blocked_query,
  blocking_text.text AS blocking_query
FROM sys.dm_exec_requests blocked
INNER JOIN sys.dm_exec_requests blocking
  ON blocked.blocking_session_id = blocking.session_id
CROSS APPLY sys.dm_exec_sql_text(blocked.sql_handle) blocked_text
CROSS APPLY sys.dm_exec_sql_text(blocking.sql_handle) blocking_text;
```

## Quick Reference

### Index Types

| Index Type | Use Case | Creation |
|-----------|----------|----------|
| Clustered | Primary key, range queries | `CREATE CLUSTERED INDEX` |
| Non-Clustered | Secondary lookups | `CREATE NONCLUSTERED INDEX` |
| Covering | Index-only scans | `CREATE INDEX ... INCLUDE (...)` |
| Filtered | Partial index | `CREATE INDEX ... WHERE ...` |
| Columnstore | Analytics, DW | `CREATE COLUMNSTORE INDEX` |

### Execution Plan Operations

| Operation | Performance | Action |
|-----------|-------------|--------|
| Clustered Index Seek | Excellent | Keep |
| Index Seek | Excellent | Keep |
| Index Scan | Fair | Consider covering index |
| Clustered Index Scan | Poor | Add index or acceptable for small tables |
| Table Scan | Worst | Add index |
| Key Lookup | Moderate | Consider covering index |

### Configuration Priorities

1. **Max Server Memory**: Leave 4GB+ for OS
2. **MAXDOP**: 4-8 for most workloads
3. **Cost Threshold for Parallelism**: 50-100
4. **Query Store**: Enable for all databases
