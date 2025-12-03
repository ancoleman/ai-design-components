# TimescaleDB Reference Guide

TimescaleDB is a PostgreSQL extension that adds time-series optimizations while maintaining full SQL compatibility.

## Installation

```bash
# Docker
docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg16

# Ubuntu/Debian
sudo sh -c "echo 'deb https://packagecloud.io/timescale/timescaledb/ubuntu/ $(lsb_release -c -s) main' > /etc/apt/sources.list.d/timescaledb.list"
wget --quiet -O - https://packagecloud.io/timescale/timescaledb/gpgkey | sudo apt-key add -
sudo apt update
sudo apt install timescaledb-2-postgresql-16

# Enable extension
psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
```

## Hypertables

Hypertables are automatically partitioned tables optimized for time-series data.

### Creating Hypertables

```sql
-- Standard table first
CREATE TABLE metrics (
  time        TIMESTAMPTZ NOT NULL,
  device_id   INTEGER NOT NULL,
  cpu_usage   DOUBLE PRECISION,
  memory_mb   INTEGER
);

-- Convert to hypertable
SELECT create_hypertable('metrics', 'time');

-- Create index on device_id for fast filtering
CREATE INDEX ON metrics (device_id, time DESC);
```

### Chunk Management

TimescaleDB partitions hypertables into chunks (default: 7 days per chunk).

```sql
-- View chunks
SELECT show_chunks('metrics');

-- Drop old chunks manually
SELECT drop_chunks('metrics', INTERVAL '90 days');

-- Configure chunk interval (before inserting data)
SELECT set_chunk_time_interval('metrics', INTERVAL '1 day');
```

Chunk sizing guidelines:
- High-ingest (1M+ rows/day): 1-day chunks
- Medium-ingest (100K-1M rows/day): 7-day chunks
- Low-ingest (< 100K rows/day): 30-day chunks

## Compression

Native columnar compression achieves 10-20x space savings.

### Enable Compression

```sql
-- Enable compression on chunks older than 7 days
ALTER TABLE metrics SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'device_id'
);

SELECT add_compression_policy('metrics', INTERVAL '7 days');
```

### Compression Options

```sql
-- Segment by high-cardinality columns
timescaledb.compress_segmentby = 'device_id, region'

-- Order by frequently queried columns
timescaledb.compress_orderby = 'time DESC'

-- Check compression ratio
SELECT
  pg_size_pretty(before_compression_total_bytes) as before,
  pg_size_pretty(after_compression_total_bytes) as after,
  before_compression_total_bytes::numeric / after_compression_total_bytes AS ratio
FROM timescaledb_information.compression_settings
WHERE hypertable_name = 'metrics';
```

## Continuous Aggregates

Materialized views that auto-refresh as new data arrives.

### Creating Continuous Aggregates

```sql
-- 1-minute rollup
CREATE MATERIALIZED VIEW metrics_1min
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 minute', time) AS bucket,
       device_id,
       AVG(cpu_usage) AS avg_cpu,
       MAX(cpu_usage) AS max_cpu,
       COUNT(*) AS sample_count
FROM metrics
GROUP BY bucket, device_id;

-- 1-hour rollup
CREATE MATERIALIZED VIEW metrics_1hour
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 hour', time) AS bucket,
       device_id,
       AVG(cpu_usage) AS avg_cpu,
       MAX(cpu_usage) AS max_cpu,
       MIN(cpu_usage) AS min_cpu
FROM metrics
GROUP BY bucket, device_id;

-- Daily rollup
CREATE MATERIALIZED VIEW metrics_daily
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 day', time) AS bucket,
       device_id,
       AVG(cpu_usage) AS avg_cpu,
       MAX(cpu_usage) AS max_cpu,
       MIN(cpu_usage) AS min_cpu,
       STDDEV(cpu_usage) AS stddev_cpu
FROM metrics
GROUP BY bucket, device_id;
```

### Refresh Policies

```sql
-- Refresh 1-minute rollup every minute for last 3 hours
SELECT add_continuous_aggregate_policy('metrics_1min',
  start_offset => INTERVAL '3 hours',
  end_offset => INTERVAL '1 minute',
  schedule_interval => INTERVAL '1 minute');

-- Refresh 1-hour rollup every hour for last 7 days
SELECT add_continuous_aggregate_policy('metrics_1hour',
  start_offset => INTERVAL '7 days',
  end_offset => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour');

-- Refresh daily rollup once per day for last 90 days
SELECT add_continuous_aggregate_policy('metrics_daily',
  start_offset => INTERVAL '90 days',
  end_offset => INTERVAL '1 day',
  schedule_interval => INTERVAL '1 day');
```

### Querying Continuous Aggregates

```sql
-- Query behaves like a normal view
SELECT bucket, device_id, avg_cpu
FROM metrics_1hour
WHERE bucket > NOW() - INTERVAL '7 days'
  AND device_id = 123
ORDER BY bucket DESC;
```

## Retention Policies

Automatically drop old data.

```sql
-- Delete raw data older than 30 days
SELECT add_retention_policy('metrics', INTERVAL '30 days');

-- Delete 1-minute rollups older than 90 days
SELECT add_retention_policy('metrics_1min', INTERVAL '90 days');

-- Keep hourly and daily rollups forever (no retention policy)
```

Typical retention strategy:
- Raw data: 7-30 days
- 1-minute rollups: 90 days
- 1-hour rollups: 1-2 years
- Daily rollups: Infinite

## Client Libraries

### Python (psycopg2)

```python
import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="password"
)

cur = conn.cursor()

# Insert data
cur.execute("""
    INSERT INTO metrics (time, device_id, cpu_usage, memory_mb)
    VALUES (%s, %s, %s, %s)
""", (datetime.now(), 123, 45.2, 2048))
conn.commit()

# Batch insert (faster)
from psycopg2.extras import execute_values
data = [
    (datetime.now(), 123, 45.2, 2048),
    (datetime.now(), 124, 67.8, 4096),
    # ... 10,000 more rows
]
execute_values(cur, "INSERT INTO metrics (time, device_id, cpu_usage, memory_mb) VALUES %s", data)
conn.commit()

# Query with time bucket
cur.execute("""
    SELECT time_bucket('5 minutes', time) AS bucket,
           AVG(cpu_usage) AS avg_cpu
    FROM metrics
    WHERE time > NOW() - INTERVAL '1 hour'
    GROUP BY bucket
    ORDER BY bucket DESC
""")
results = cur.fetchall()
```

### TypeScript (pg)

```typescript
import { Pool } from 'pg';

const pool = new Pool({
  host: 'localhost',
  database: 'postgres',
  user: 'postgres',
  password: 'password',
  port: 5432,
});

// Insert data
await pool.query(
  'INSERT INTO metrics (time, device_id, cpu_usage, memory_mb) VALUES ($1, $2, $3, $4)',
  [new Date(), 123, 45.2, 2048]
);

// Batch insert
const client = await pool.connect();
try {
  await client.query('BEGIN');

  for (const row of data) {
    await client.query(
      'INSERT INTO metrics (time, device_id, cpu_usage, memory_mb) VALUES ($1, $2, $3, $4)',
      [row.time, row.device_id, row.cpu_usage, row.memory_mb]
    );
  }

  await client.query('COMMIT');
} catch (e) {
  await client.query('ROLLBACK');
  throw e;
} finally {
  client.release();
}

// Query
const result = await pool.query(`
  SELECT time_bucket('5 minutes', time) AS bucket,
         AVG(cpu_usage) AS avg_cpu
  FROM metrics
  WHERE time > NOW() - INTERVAL '1 hour'
  GROUP BY bucket
  ORDER BY bucket DESC
`);
console.log(result.rows);
```

## Performance Tuning

### PostgreSQL Configuration

```sql
-- postgresql.conf adjustments for time-series workload

-- Memory settings
shared_buffers = 8GB                  -- 25% of RAM
effective_cache_size = 24GB           -- 75% of RAM
work_mem = 128MB                      -- For sorting/aggregation
maintenance_work_mem = 2GB            -- For VACUUM, CREATE INDEX

-- Write performance
synchronous_commit = off              -- Higher throughput, slight risk
wal_buffers = 16MB
checkpoint_completion_target = 0.9

-- TimescaleDB specific
timescaledb.max_background_workers = 8
```

### Batch Inserts

```python
# BAD: 1 row at a time (slow)
for row in data:
    cur.execute("INSERT INTO metrics VALUES (%s, %s, %s, %s)", row)
    conn.commit()

# GOOD: Batch 10,000 rows
from psycopg2.extras import execute_values
execute_values(cur, "INSERT INTO metrics VALUES %s", data[:10000], page_size=1000)
conn.commit()

# BEST: Use COPY for bulk loads
from io import StringIO
csv_data = StringIO()
for row in data:
    csv_data.write(f"{row[0]},{row[1]},{row[2]},{row[3]}\n")
csv_data.seek(0)

cur.copy_from(csv_data, 'metrics', sep=',', columns=['time', 'device_id', 'cpu_usage', 'memory_mb'])
conn.commit()
```

### Query Optimization

```sql
-- Explain analyze to check query plan
EXPLAIN (ANALYZE, BUFFERS)
SELECT time_bucket('1 hour', time), AVG(cpu_usage)
FROM metrics
WHERE time > NOW() - INTERVAL '7 days'
  AND device_id = 123
GROUP BY 1;

-- Should see "Index Scan" on time index, not "Seq Scan"
```

## High-Cardinality Data

For metrics with many unique label combinations (Prometheus-style), use JSONB.

```sql
CREATE TABLE prometheus_metrics (
  time        TIMESTAMPTZ NOT NULL,
  metric_name TEXT NOT NULL,
  labels      JSONB NOT NULL,
  value       DOUBLE PRECISION
);

SELECT create_hypertable('prometheus_metrics', 'time');

-- GIN index for JSONB queries
CREATE INDEX ON prometheus_metrics USING GIN (labels jsonb_path_ops);

-- Insert
INSERT INTO prometheus_metrics VALUES (
  NOW(),
  'http_requests_total',
  '{"method": "GET", "status": "200", "path": "/api/users"}',
  1234.0
);

-- Query
SELECT time_bucket('5 minutes', time) AS bucket,
       SUM(value) AS total_requests
FROM prometheus_metrics
WHERE metric_name = 'http_requests_total'
  AND labels @> '{"status": "200"}'
  AND time > NOW() - INTERVAL '1 hour'
GROUP BY bucket
ORDER BY bucket DESC;
```

## Multi-Node (Distributed Hypertables)

TimescaleDB supports distributed hypertables for horizontal scaling (requires Timescale Cloud or self-managed cluster).

```sql
-- On access node
SELECT add_data_node('data_node_1', host => 'node1.example.com');
SELECT add_data_node('data_node_2', host => 'node2.example.com');
SELECT add_data_node('data_node_3', host => 'node3.example.com');

-- Create distributed hypertable
SELECT create_distributed_hypertable('metrics', 'time', 'device_id');

-- Inserts and queries automatically distributed
```

## Troubleshooting

### Check Background Jobs

```sql
-- View all scheduled jobs
SELECT * FROM timescaledb_information.jobs;

-- View job stats
SELECT * FROM timescaledb_information.job_stats;

-- Manually run a job
CALL run_job(1000);  -- job_id from jobs table
```

### Compression Issues

```sql
-- Find uncompressed chunks
SELECT show_chunks('metrics', older_than => INTERVAL '7 days')
EXCEPT
SELECT show_chunks('metrics', older_than => INTERVAL '7 days', compressed => true);

-- Manually compress a chunk
SELECT compress_chunk('_timescaledb_internal._hyper_1_1_chunk');
```

### Slow Queries

```sql
-- Enable pg_stat_statements
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- View slowest queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;
```

## Best Practices

1. **Index Strategy**: Index on time + commonly filtered columns (device_id, metric_name)
2. **Chunk Sizing**: Match chunk interval to data retention and query patterns
3. **Compression**: Compress chunks older than your typical query range
4. **Continuous Aggregates**: Create rollups at multiple resolutions (1min, 1hour, 1day)
5. **Retention Policies**: Set automatic data expiration to control storage costs
6. **Batch Inserts**: Insert 1,000-10,000 rows per transaction for best performance
7. **Query Patterns**: Always filter by time first, use continuous aggregates for long ranges
8. **Monitoring**: Track chunk count, compression ratios, and background job health
