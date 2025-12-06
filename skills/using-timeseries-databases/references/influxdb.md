# InfluxDB Reference Guide

InfluxDB is a purpose-built time-series database with native support for DevOps metrics and Prometheus integration.


## Table of Contents

- [Version Overview](#version-overview)
- [Installation](#installation)
  - [InfluxDB 3.x (Docker)](#influxdb-3x-docker)
  - [InfluxDB 2.x (Docker)](#influxdb-2x-docker)
- [Data Model](#data-model)
- [Writing Data](#writing-data)
  - [Line Protocol (Universal)](#line-protocol-universal)
  - [Python Client (InfluxDB 3.x)](#python-client-influxdb-3x)
  - [TypeScript Client](#typescript-client)
- [Querying Data](#querying-data)
  - [InfluxQL (SQL-like)](#influxql-sql-like)
  - [Flux (InfluxDB 2.x)](#flux-influxdb-2x)
  - [SQL (InfluxDB 3.x)](#sql-influxdb-3x)
- [Retention Policies](#retention-policies)
  - [InfluxDB 2.x](#influxdb-2x)
  - [InfluxDB 1.x](#influxdb-1x)
- [Downsampling (Continuous Queries)](#downsampling-continuous-queries)
  - [InfluxDB 1.x](#influxdb-1x)
  - [InfluxDB 2.x (Tasks)](#influxdb-2x-tasks)
- [Prometheus Integration](#prometheus-integration)
  - [prometheus.yml Configuration](#prometheusyml-configuration)
  - [Query Prometheus Metrics in InfluxDB](#query-prometheus-metrics-in-influxdb)
- [Client Libraries](#client-libraries)
  - [Python](#python)
  - [Go](#go)
- [Performance Optimization](#performance-optimization)
  - [Write Performance](#write-performance)
  - [Query Performance](#query-performance)
  - [Cardinality Management](#cardinality-management)
- [Dashboard Integration](#dashboard-integration)
  - [FastAPI Backend](#fastapi-backend)
  - [TypeScript Frontend](#typescript-frontend)
- [Telegraf Integration](#telegraf-integration)
  - [telegraf.conf](#telegrafconf)
- [Best Practices](#best-practices)

## Version Overview

| Version | Query Language | License | Best For |
|---------|---------------|---------|----------|
| **InfluxDB 1.x** | InfluxQL (SQL-like) | MIT | Legacy systems, simple use cases |
| **InfluxDB 2.x** | Flux (functional) | Proprietary (limits apply) | Newer deployments (caution: licensing) |
| **InfluxDB 3.x** | SQL + InfluxQL | Apache 2.0 | Recommended (OSS core, Apache Arrow-based) |

**Recommendation**: Use InfluxDB 3.x for new projects (open-source core, best performance).

## Installation

### InfluxDB 3.x (Docker)

```bash
docker run -d \
  --name influxdb3 \
  -p 8086:8086 \
  -v influxdb3-data:/var/lib/influxdb3 \
  influxdata/influxdb:3.0-alpine
```

### InfluxDB 2.x (Docker)

```bash
docker run -d \
  --name influxdb \
  -p 8086:8086 \
  -v influxdb-data:/var/lib/influxdb2 \
  influxdb:2.7-alpine

# Initial setup (creates admin user, org, bucket)
docker exec influxdb influx setup \
  --username admin \
  --password adminpassword \
  --org myorg \
  --bucket mybucket \
  --retention 30d \
  --force
```

## Data Model

InfluxDB uses **measurements** (like tables), **tags** (indexed metadata), **fields** (actual values), and **timestamps**.

```
measurement,tag1=value1,tag2=value2 field1=value1,field2=value2 timestamp
```

Example:
```
cpu,host=server01,region=us-west usage=0.64,cores=8 1465839830100400200
```

Tags vs. Fields:
- **Tags**: Indexed, use for filtering (host, region, device_id)
- **Fields**: Not indexed, use for actual measurements (temperature, cpu_usage)

**Anti-pattern**: High-cardinality tags (unique user IDs, UUIDs) - causes performance issues.

## Writing Data

### Line Protocol (Universal)

```bash
# Write via HTTP POST
curl -XPOST "http://localhost:8086/api/v2/write?org=myorg&bucket=mybucket" \
  --header "Authorization: Token YOUR_API_TOKEN" \
  --data-raw "
cpu,host=server01 usage=0.64 1465839830100400200
cpu,host=server01 usage=0.72 1465839830200400200
cpu,host=server01 usage=0.68 1465839830300400200
"
```

### Python Client (InfluxDB 3.x)

```python
from influxdb_client_3 import InfluxDBClient3, Point

client = InfluxDBClient3(
    host='localhost',
    token='YOUR_API_TOKEN',
    org='myorg',
    database='mybucket'
)

# Write single point
point = Point("cpu") \
    .tag("host", "server01") \
    .tag("region", "us-west") \
    .field("usage", 0.64) \
    .field("cores", 8)

client.write(point)

# Batch write (recommended)
points = []
for i in range(10000):
    point = Point("cpu") \
        .tag("host", f"server{i:02d}") \
        .field("usage", random.uniform(0, 100)) \
        .time(datetime.now())
    points.append(point)

client.write(points)
```

### TypeScript Client

```typescript
import { InfluxDB, Point } from '@influxdata/influxdb-client';

const client = new InfluxDB({
  url: 'http://localhost:8086',
  token: 'YOUR_API_TOKEN'
});

const writeApi = client.getWriteApi('myorg', 'mybucket', 'ns');

// Write single point
const point = new Point('cpu')
  .tag('host', 'server01')
  .floatField('usage', 0.64)
  .intField('cores', 8);

writeApi.writePoint(point);

// Batch write
for (let i = 0; i < 10000; i++) {
  const point = new Point('cpu')
    .tag('host', `server${i.toString().padStart(2, '0')}`)
    .floatField('usage', Math.random() * 100);

  writeApi.writePoint(point);
}

await writeApi.close();
```

## Querying Data

### InfluxQL (SQL-like)

```sql
-- Select all fields
SELECT * FROM cpu WHERE time > now() - 1h;

-- Aggregate
SELECT mean("usage")
FROM cpu
WHERE time > now() - 1h
GROUP BY time(5m), host;

-- Multiple aggregations
SELECT mean("usage") AS avg_usage,
       max("usage") AS max_usage,
       min("usage") AS min_usage
FROM cpu
WHERE time > now() - 1d
GROUP BY time(1h);
```

### Flux (InfluxDB 2.x)

```flux
// Basic query
from(bucket: "mybucket")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "cpu")
  |> filter(fn: (r) => r._field == "usage")

// Aggregation
from(bucket: "mybucket")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "cpu")
  |> aggregateWindow(every: 5m, fn: mean)

// Join multiple measurements
cpu = from(bucket: "mybucket")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "cpu")

mem = from(bucket: "mybucket")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "memory")

join(tables: {cpu: cpu, mem: mem}, on: ["_time", "host"])
```

### SQL (InfluxDB 3.x)

```sql
-- Standard SQL syntax
SELECT time, host, usage
FROM cpu
WHERE time > NOW() - INTERVAL '1 hour'
ORDER BY time DESC;

-- Aggregation with time bucket
SELECT
  time_bucket(INTERVAL '5 minutes', time) AS bucket,
  host,
  AVG(usage) AS avg_usage
FROM cpu
WHERE time > NOW() - INTERVAL '1 hour'
GROUP BY bucket, host
ORDER BY bucket DESC;
```

## Retention Policies

Automatically expire old data.

### InfluxDB 2.x

```bash
# Create bucket with retention
influx bucket create \
  --name metrics \
  --org myorg \
  --retention 30d

# Update retention
influx bucket update \
  --name metrics \
  --retention 90d
```

### InfluxDB 1.x

```sql
-- Create retention policy
CREATE RETENTION POLICY "30_days" ON "mydb" DURATION 30d REPLICATION 1 DEFAULT;

-- Create retention policy for rollups (infinite)
CREATE RETENTION POLICY "infinite" ON "mydb" DURATION INF REPLICATION 1;
```

## Downsampling (Continuous Queries)

Pre-aggregate data for faster queries.

### InfluxDB 1.x

```sql
-- Create continuous query: hourly rollup
CREATE CONTINUOUS QUERY "cpu_hourly" ON "mydb"
BEGIN
  SELECT mean("usage") AS avg_usage,
         max("usage") AS max_usage
  INTO "infinite"."cpu_hourly"
  FROM "cpu"
  GROUP BY time(1h), host
END;

-- Create continuous query: daily rollup
CREATE CONTINUOUS QUERY "cpu_daily" ON "mydb"
BEGIN
  SELECT mean("usage") AS avg_usage
  INTO "infinite"."cpu_daily"
  FROM "cpu"
  GROUP BY time(1d), host
END;
```

### InfluxDB 2.x (Tasks)

```flux
// Create task: hourly rollup
option task = {
  name: "cpu_hourly_rollup",
  every: 1h,
  offset: 5m
}

from(bucket: "mybucket")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "cpu")
  |> aggregateWindow(every: 1h, fn: mean)
  |> to(bucket: "mybucket_rollups")
```

## Prometheus Integration

InfluxDB can act as long-term storage for Prometheus.

### prometheus.yml Configuration

```yaml
# Prometheus remote write to InfluxDB 2.x
remote_write:
  - url: "http://localhost:8086/api/v2/write?org=myorg&bucket=prometheus"
    headers:
      Authorization: "Token YOUR_API_TOKEN"

remote_read:
  - url: "http://localhost:8086/api/v2/read?org=myorg&bucket=prometheus"
    headers:
      Authorization: "Token YOUR_API_TOKEN"
```

### Query Prometheus Metrics in InfluxDB

```flux
from(bucket: "prometheus")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "http_requests_total")
  |> filter(fn: (r) => r.status == "200")
  |> aggregateWindow(every: 5m, fn: sum)
```

## Client Libraries

### Python

```python
from influxdb_client_3 import InfluxDBClient3, Point
from datetime import datetime

client = InfluxDBClient3(
    host='localhost',
    token='YOUR_API_TOKEN',
    org='myorg',
    database='mybucket'
)

# Write
point = Point("temperature") \
    .tag("sensor_id", "sensor_01") \
    .tag("location", "warehouse_a") \
    .field("value", 22.5) \
    .time(datetime.now())

client.write(point)

# Query (returns pandas DataFrame)
query = """
    SELECT time, sensor_id, value
    FROM temperature
    WHERE time > NOW() - INTERVAL '1 hour'
    ORDER BY time DESC
"""
df = client.query(query=query, language="sql")
print(df.head())
```

### Go

```go
package main

import (
    "context"
    "fmt"
    "time"
    influxdb2 "github.com/influxdata/influxdb-client-go/v2"
)

func main() {
    client := influxdb2.NewClient("http://localhost:8086", "YOUR_API_TOKEN")
    defer client.Close()

    // Write
    writeAPI := client.WriteAPI("myorg", "mybucket")

    p := influxdb2.NewPointWithMeasurement("cpu").
        AddTag("host", "server01").
        AddField("usage", 0.64).
        SetTime(time.Now())

    writeAPI.WritePoint(p)
    writeAPI.Flush()

    // Query
    queryAPI := client.QueryAPI("myorg")
    query := `from(bucket: "mybucket")
        |> range(start: -1h)
        |> filter(fn: (r) => r._measurement == "cpu")`

    result, err := queryAPI.Query(context.Background(), query)
    if err == nil {
        for result.Next() {
            fmt.Printf("time: %v, value: %v\n", result.Record().Time(), result.Record().Value())
        }
    }
}
```

## Performance Optimization

### Write Performance

```python
# BAD: Write one point at a time
for point in points:
    client.write(point)  # Slow: 1,000 HTTP requests

# GOOD: Batch write
client.write(points)  # Fast: 1 HTTP request

# BEST: Use write options for batching
from influxdb_client_3 import WriteOptions

write_api = client.get_write_api(write_options=WriteOptions(
    batch_size=5000,
    flush_interval=10_000,  # 10 seconds
    jitter_interval=2_000,
    retry_interval=5_000
))

for point in points:
    write_api.write(point)  # Automatically batched
```

### Query Performance

```flux
// BAD: Select all fields, no time filter
from(bucket: "mybucket")
  |> filter(fn: (r) => r._measurement == "cpu")

// GOOD: Filter by time, select specific field
from(bucket: "mybucket")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "cpu")
  |> filter(fn: (r) => r._field == "usage")

// BEST: Use continuous queries/tasks for aggregations
from(bucket: "mybucket_rollups")  // Pre-aggregated data
  |> range(start: -7d)
```

### Cardinality Management

```python
# BAD: High-cardinality tag (unique per row)
Point("events") \
    .tag("user_id", "uuid-123-456")  # Millions of unique values
    .field("event_type", "click")

# GOOD: Low-cardinality tags, high-cardinality as field
Point("events") \
    .tag("event_type", "click")       # Few unique values
    .field("user_id", "uuid-123-456") # Not indexed
```

## Dashboard Integration

### FastAPI Backend

```python
from fastapi import FastAPI
from influxdb_client_3 import InfluxDBClient3

app = FastAPI()
client = InfluxDBClient3(host='localhost', token='YOUR_API_TOKEN', org='myorg', database='mybucket')

@app.get("/api/metrics/cpu")
async def get_cpu_metrics(start: str = "1h", host: str = None):
    query = f"""
        SELECT time, host, usage
        FROM cpu
        WHERE time > NOW() - INTERVAL '{start}'
    """

    if host:
        query += f" AND host = '{host}'"

    query += " ORDER BY time DESC LIMIT 1000"

    df = client.query(query=query, language="sql")
    return df.to_dict(orient="records")
```

### TypeScript Frontend

```typescript
import useSWR from 'swr';
import { LineChart, Line, XAxis, YAxis } from 'recharts';

const fetcher = (url: string) => fetch(url).then(r => r.json());

function CPUChart() {
  const { data } = useSWR('/api/metrics/cpu?start=1h&host=server01', fetcher, {
    refreshInterval: 10000  // Refresh every 10 seconds
  });

  return (
    <LineChart data={data} width={800} height={400}>
      <XAxis dataKey="time" />
      <YAxis />
      <Line dataKey="usage" stroke="var(--color-primary)" />
    </LineChart>
  );
}
```

## Telegraf Integration

Telegraf is InfluxDB's official metrics collector with 200+ input plugins.

### telegraf.conf

```toml
# Output to InfluxDB 2.x
[[outputs.influxdb_v2]]
  urls = ["http://localhost:8086"]
  token = "YOUR_API_TOKEN"
  organization = "myorg"
  bucket = "mybucket"

# Input: System metrics
[[inputs.cpu]]
  percpu = true
  totalcpu = true

[[inputs.mem]]

[[inputs.disk]]
  ignore_fs = ["tmpfs", "devtmpfs"]

# Input: Prometheus scraper
[[inputs.prometheus]]
  urls = ["http://localhost:9090/metrics"]
```

## Best Practices

1. **Data Model**: Use low-cardinality tags (host, region), high-cardinality fields (user_id)
2. **Retention**: Set appropriate retention policies (raw: 30d, rollups: 1y)
3. **Downsampling**: Create continuous queries for hourly/daily rollups
4. **Batch Writes**: Write 1,000-5,000 points per batch for best performance
5. **Query Optimization**: Always filter by time, use downsampled data for long ranges
6. **Cardinality**: Avoid high-cardinality tags (> 100K unique values)
7. **Telegraf**: Use Telegraf for collecting system metrics (easier than custom code)
8. **Grafana**: InfluxDB has excellent Grafana integration for dashboards
