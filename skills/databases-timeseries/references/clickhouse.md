# ClickHouse Reference Guide

ClickHouse is a columnar database optimized for OLAP and analytics, delivering 100M-1B rows/sec query performance.

## Installation

### Docker (Single Node)

```bash
docker run -d \
  --name clickhouse-server \
  -p 8123:8123 \
  -p 9000:9000 \
  --ulimit nofile=262144:262144 \
  -v clickhouse-data:/var/lib/clickhouse \
  clickhouse/clickhouse-server:latest
```

### Docker Compose (Cluster)

```yaml
version: '3.8'
services:
  clickhouse-01:
    image: clickhouse/clickhouse-server:latest
    hostname: clickhouse-01
    volumes:
      - ./config/clickhouse-01:/etc/clickhouse-server
      - clickhouse-01-data:/var/lib/clickhouse
    ports:
      - "8123:8123"
      - "9000:9000"

  clickhouse-02:
    image: clickhouse/clickhouse-server:latest
    hostname: clickhouse-02
    volumes:
      - ./config/clickhouse-02:/etc/clickhouse-server
      - clickhouse-02-data:/var/lib/clickhouse

  clickhouse-03:
    image: clickhouse/clickhouse-server:latest
    hostname: clickhouse-03
    volumes:
      - ./config/clickhouse-03:/etc/clickhouse-server
      - clickhouse-03-data:/var/lib/clickhouse

  clickhouse-keeper:
    image: clickhouse/clickhouse-keeper:latest
    volumes:
      - clickhouse-keeper-data:/var/lib/clickhouse-keeper
```

## Table Engines

ClickHouse uses MergeTree family engines for time-series data.

### MergeTree (Basic)

```sql
CREATE TABLE events (
  timestamp DateTime,
  user_id UInt32,
  event_type String,
  page String,
  duration UInt32
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (user_id, timestamp);
```

Key concepts:
- **PARTITION BY**: Groups data by month (enables efficient data dropping)
- **ORDER BY**: Sorting key (used for range queries)
- **PRIMARY KEY**: Subset of ORDER BY (optional, for sparse index)

### ReplacingMergeTree (Deduplication)

```sql
CREATE TABLE sensor_data (
  timestamp DateTime,
  sensor_id UInt32,
  temperature Float64,
  humidity Float64
) ENGINE = ReplacingMergeTree()
PARTITION BY toYYYYMMDD(timestamp)
ORDER BY (sensor_id, timestamp);
```

Deduplicates rows with same ORDER BY key (keeps last version).

### SummingMergeTree (Pre-aggregation)

```sql
CREATE TABLE metrics_rollup (
  hour DateTime,
  metric_name String,
  sum_value Float64,
  count UInt64
) ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(hour)
ORDER BY (metric_name, hour);
```

Automatically sums numeric columns when merging parts.

### AggregatingMergeTree (Complex Aggregations)

```sql
CREATE TABLE events_agg (
  date Date,
  event_type String,
  user_count AggregateFunction(uniq, UInt32),
  total_duration AggregateFunction(sum, UInt32)
) ENGINE = AggregatingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (event_type, date);

-- Insert with aggregate state
INSERT INTO events_agg
SELECT
  toDate(timestamp) AS date,
  event_type,
  uniqState(user_id) AS user_count,
  sumState(duration) AS total_duration
FROM events
GROUP BY date, event_type;

-- Query aggregate result
SELECT
  date,
  event_type,
  uniqMerge(user_count) AS unique_users,
  sumMerge(total_duration) AS total_duration
FROM events_agg
GROUP BY date, event_type;
```

## Data Types

### Numeric Types

```sql
-- Integers
UInt8, UInt16, UInt32, UInt64    -- Unsigned (0 to 2^N-1)
Int8, Int16, Int32, Int64        -- Signed (-2^(N-1) to 2^(N-1)-1)

-- Floats
Float32, Float64                 -- Standard floating point

-- Decimal (for financial data)
Decimal(P, S)                    -- P=precision, S=scale
Decimal(18, 2)                   -- 16 digits before decimal, 2 after
```

### Date/Time Types

```sql
Date           -- 1970-01-01 to 2149-06-06
Date32         -- 1900-01-01 to 2299-12-31
DateTime       -- Unix timestamp with second precision
DateTime64(3)  -- Millisecond precision
```

### String Types

```sql
String              -- Variable length (use for text)
FixedString(N)      -- Fixed length (faster for short strings)
LowCardinality(String)  -- Dictionary encoding (for repeated values)
```

## Writing Data

### Single Insert

```sql
INSERT INTO events (timestamp, user_id, event_type, page, duration)
VALUES (now(), 1234, 'page_view', '/dashboard', 5);
```

### Batch Insert

```sql
INSERT INTO events (timestamp, user_id, event_type, page, duration)
VALUES
  (now(), 1234, 'page_view', '/dashboard', 5),
  (now(), 1235, 'page_view', '/profile', 10),
  (now(), 1236, 'click', '/button', 1);
```

### Insert from SELECT

```sql
-- Copy data from another table
INSERT INTO events_summary
SELECT
  toDate(timestamp) AS date,
  event_type,
  count() AS event_count
FROM events
WHERE timestamp >= today() - 7
GROUP BY date, event_type;
```

### Async Inserts (Batching)

```sql
SET async_insert = 1;
SET wait_for_async_insert = 0;

INSERT INTO events VALUES (...);  -- Batched automatically
```

## Querying Data

### Basic Queries

```sql
-- Select with time filter
SELECT timestamp, user_id, event_type
FROM events
WHERE timestamp >= now() - INTERVAL 1 HOUR
ORDER BY timestamp DESC
LIMIT 100;

-- Aggregation
SELECT
  toStartOfHour(timestamp) AS hour,
  event_type,
  count() AS event_count,
  uniq(user_id) AS unique_users
FROM events
WHERE timestamp >= today()
GROUP BY hour, event_type
ORDER BY hour DESC;
```

### Time Functions

```sql
-- Time bucketing
toStartOfMinute(timestamp)
toStartOfHour(timestamp)
toStartOfDay(timestamp)
toStartOfWeek(timestamp)
toStartOfMonth(timestamp)

-- Date arithmetic
now() - INTERVAL 1 HOUR
today() - INTERVAL 7 DAY
toDate('2025-01-01') + INTERVAL 30 DAY

-- Date parts
toYear(timestamp)
toMonth(timestamp)
toDayOfWeek(timestamp)
toHour(timestamp)
```

### Aggregation Functions

```sql
-- Standard aggregations
count()              -- Row count
sum(column)          -- Sum
avg(column)          -- Average
min(column)          -- Minimum
max(column)          -- Maximum

-- Statistical functions
stddevPop(column)    -- Standard deviation
varPop(column)       -- Variance
median(column)       -- Median
quantile(0.95)(column)  -- 95th percentile

-- Unique counting
uniq(column)         -- Approximate unique count (HyperLogLog)
uniqExact(column)    -- Exact unique count (slower)

-- Arrays
groupArray(column)   -- Collect values into array
arraySum(array)      -- Sum array elements
```

### Window Functions

```sql
-- Running total
SELECT
  timestamp,
  user_id,
  duration,
  sum(duration) OVER (PARTITION BY user_id ORDER BY timestamp) AS cumulative_duration
FROM events
WHERE timestamp >= today();

-- Rank
SELECT
  user_id,
  count() AS event_count,
  rank() OVER (ORDER BY count() DESC) AS rank
FROM events
GROUP BY user_id
ORDER BY rank;
```

## Materialized Views

Pre-compute aggregations for fast queries.

### Creating Materialized Views

```sql
-- Create target table (SummingMergeTree)
CREATE TABLE events_hourly (
  hour DateTime,
  event_type String,
  event_count UInt64,
  unique_users UInt64
) ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(hour)
ORDER BY (event_type, hour);

-- Create materialized view
CREATE MATERIALIZED VIEW events_hourly_mv TO events_hourly AS
SELECT
  toStartOfHour(timestamp) AS hour,
  event_type,
  count() AS event_count,
  uniq(user_id) AS unique_users
FROM events
GROUP BY hour, event_type;
```

Now every insert to `events` automatically updates `events_hourly`.

### Querying Materialized Views

```sql
-- Query pre-aggregated data (fast)
SELECT
  hour,
  event_type,
  sum(event_count) AS total_events,
  sum(unique_users) AS total_users  -- Note: Won't be accurate with SummingMergeTree
FROM events_hourly
WHERE hour >= today() - 7
GROUP BY hour, event_type
ORDER BY hour DESC;
```

**Note**: For accurate unique counts, use AggregatingMergeTree with `uniqState`/`uniqMerge`.

## Client Libraries

### Python

```python
from clickhouse_connect import get_client

client = get_client(host='localhost', port=8123, username='default', password='')

# Insert data
client.insert('events', [
    [datetime.now(), 1234, 'page_view', '/dashboard', 5],
    [datetime.now(), 1235, 'page_view', '/profile', 10],
], column_names=['timestamp', 'user_id', 'event_type', 'page', 'duration'])

# Query (returns list of rows)
result = client.query("""
    SELECT
      toStartOfHour(timestamp) AS hour,
      event_type,
      count() AS event_count
    FROM events
    WHERE timestamp >= now() - INTERVAL 1 HOUR
    GROUP BY hour, event_type
    ORDER BY hour DESC
""")

for row in result.result_rows:
    print(row)

# Query (returns pandas DataFrame)
import pandas as pd
df = client.query_df("""
    SELECT timestamp, user_id, event_type
    FROM events
    WHERE timestamp >= today()
    LIMIT 1000
""")
print(df.head())
```

### TypeScript

```typescript
import { createClient } from '@clickhouse/client';

const client = createClient({
  host: 'http://localhost:8123',
  username: 'default',
  password: '',
  database: 'default'
});

// Insert data
await client.insert({
  table: 'events',
  values: [
    { timestamp: new Date(), user_id: 1234, event_type: 'page_view', page: '/dashboard', duration: 5 },
    { timestamp: new Date(), user_id: 1235, event_type: 'page_view', page: '/profile', duration: 10 }
  ],
  format: 'JSONEachRow'
});

// Query
const result = await client.query({
  query: `
    SELECT
      toStartOfHour(timestamp) AS hour,
      event_type,
      count() AS event_count
    FROM events
    WHERE timestamp >= now() - INTERVAL 1 HOUR
    GROUP BY hour, event_type
    ORDER BY hour DESC
  `,
  format: 'JSONEachRow'
});

const rows = await result.json();
console.log(rows);
```

### Rust

```rust
use clickhouse::Client;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::default()
        .with_url("http://localhost:8123")
        .with_database("default");

    // Insert data
    let mut insert = client.insert("events")?;
    insert.write(&Event {
        timestamp: chrono::Utc::now(),
        user_id: 1234,
        event_type: "page_view".to_string(),
        page: "/dashboard".to_string(),
        duration: 5,
    }).await?;
    insert.end().await?;

    // Query
    let rows = client
        .query("SELECT timestamp, user_id, event_type FROM events WHERE timestamp >= today() LIMIT 100")
        .fetch_all::<Event>()
        .await?;

    for row in rows {
        println!("{:?}", row);
    }

    Ok(())
}
```

## Performance Optimization

### Compression Codecs

```sql
CREATE TABLE metrics (
  timestamp DateTime CODEC(DoubleDelta, LZ4),
  sensor_id UInt32 CODEC(LZ4),
  temperature Float64 CODEC(Gorilla, LZ4)
) ENGINE = MergeTree()
ORDER BY (sensor_id, timestamp);
```

Recommended codecs:
- **DateTime**: DoubleDelta + LZ4 (15-30x compression)
- **Floats**: Gorilla + LZ4 (10-20x compression)
- **Integers**: Delta + LZ4 or LZ4HC
- **Strings**: LZ4HC or ZSTD(1)

### Partitioning Strategy

```sql
-- Monthly partitions (standard)
PARTITION BY toYYYYMM(timestamp)

-- Daily partitions (high data volume)
PARTITION BY toYYYYMMDD(timestamp)

-- No partitioning (small datasets)
PARTITION BY tuple()
```

Partition by month for most time-series use cases. Use daily partitions if ingesting > 100M rows/day.

### Index Optimization

```sql
-- Primary key (sparse index)
PRIMARY KEY (sensor_id, timestamp)

-- Skipping indices for filtering
CREATE TABLE events (
  timestamp DateTime,
  user_id UInt32,
  event_type LowCardinality(String),
  page String
) ENGINE = MergeTree()
ORDER BY (timestamp, user_id)
SETTINGS index_granularity = 8192;

-- Create skipping index
ALTER TABLE events ADD INDEX idx_event_type event_type TYPE set(100) GRANULARITY 4;
```

### Query Optimization

```sql
-- BAD: No ORDER BY key in WHERE
SELECT * FROM events WHERE event_type = 'click';  -- Full table scan

-- GOOD: Filter by ORDER BY columns first
SELECT * FROM events
WHERE timestamp >= today()
  AND user_id BETWEEN 1000 AND 2000
  AND event_type = 'click';

-- BEST: Use materialized view for aggregations
SELECT * FROM events_hourly WHERE hour >= today() - 7;
```

## TTL (Time-to-Live)

Automatically delete or move old data.

### Delete Old Data

```sql
ALTER TABLE events
MODIFY TTL timestamp + INTERVAL 90 DAY;
```

### Tiered Storage (Hot/Cold)

```sql
-- Define storage policies in config.xml
-- <storage_configuration>
--   <disks>
--     <hot><path>/var/lib/clickhouse/hot/</path></hot>
--     <cold><path>/var/lib/clickhouse/cold/</path></cold>
--   </disks>
--   <policies>
--     <tiered>
--       <volumes>
--         <hot><disk>hot</disk></hot>
--         <cold><disk>cold</disk></cold>
--       </volumes>
--     </tiered>
--   </policies>
-- </storage_configuration>

CREATE TABLE events (
  timestamp DateTime,
  user_id UInt32,
  event_type String
) ENGINE = MergeTree()
ORDER BY (timestamp, user_id)
PARTITION BY toYYYYMM(timestamp)
TTL timestamp + INTERVAL 7 DAY TO VOLUME 'cold',  -- Move to cold after 7 days
    timestamp + INTERVAL 90 DAY DELETE            -- Delete after 90 days
SETTINGS storage_policy = 'tiered';
```

## Distributed Tables

Shard data across multiple nodes for horizontal scaling.

### Cluster Configuration

```xml
<!-- config.xml -->
<remote_servers>
  <my_cluster>
    <shard>
      <replica>
        <host>clickhouse-01</host>
        <port>9000</port>
      </replica>
      <replica>
        <host>clickhouse-02</host>
        <port>9000</port>
      </replica>
    </shard>
    <shard>
      <replica>
        <host>clickhouse-03</host>
        <port>9000</port>
      </replica>
      <replica>
        <host>clickhouse-04</host>
        <port>9000</port>
      </replica>
    </shard>
  </my_cluster>
</remote_servers>
```

### Create Distributed Table

```sql
-- Create local table on each node
CREATE TABLE events_local ON CLUSTER my_cluster (
  timestamp DateTime,
  user_id UInt32,
  event_type String
) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/events', '{replica}')
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, user_id);

-- Create distributed table (query endpoint)
CREATE TABLE events ON CLUSTER my_cluster AS events_local
ENGINE = Distributed(my_cluster, default, events_local, rand());
```

### Query Distributed Table

```sql
-- Query automatically distributed across shards
SELECT
  toStartOfHour(timestamp) AS hour,
  count() AS event_count
FROM events
WHERE timestamp >= today()
GROUP BY hour
ORDER BY hour DESC;
```

## Dashboard Integration

### FastAPI Backend

```python
from fastapi import FastAPI
from clickhouse_connect import get_client

app = FastAPI()
client = get_client(host='localhost', port=8123)

@app.get("/api/analytics/dau")
async def get_daily_active_users(days: int = 30):
    query = f"""
        SELECT
          toDate(timestamp) AS date,
          uniq(user_id) AS dau
        FROM events
        WHERE timestamp >= today() - {days}
        GROUP BY date
        ORDER BY date DESC
    """

    result = client.query(query)
    return [{"date": row[0], "dau": row[1]} for row in result.result_rows]

@app.get("/api/analytics/events")
async def get_event_counts(start: str = "7d"):
    # Parse start (e.g., "7d", "30d", "1h")
    interval = start

    query = f"""
        SELECT
          toStartOfHour(timestamp) AS hour,
          event_type,
          count() AS event_count
        FROM events_hourly
        WHERE hour >= now() - INTERVAL {interval}
        GROUP BY hour, event_type
        ORDER BY hour DESC
        LIMIT 1000
    """

    df = client.query_df(query)
    return df.to_dict(orient="records")
```

## Best Practices

1. **ORDER BY**: Choose columns used most in WHERE clauses (timestamp, user_id)
2. **PARTITION BY**: Use monthly partitions for most use cases
3. **Compression**: Use DoubleDelta for timestamps, Gorilla for floats
4. **Materialized Views**: Pre-aggregate for fast dashboard queries
5. **Batch Inserts**: Insert 10,000-100,000 rows per batch
6. **Async Inserts**: Enable for automatic batching
7. **TTL**: Set automatic data expiration to control storage costs
8. **Distributed Tables**: Shard by user_id or device_id for even distribution
9. **Query Patterns**: Always filter by ORDER BY columns first
10. **Monitoring**: Track merge times, query duration, and replication lag
