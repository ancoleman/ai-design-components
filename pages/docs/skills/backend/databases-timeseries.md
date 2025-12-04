---
sidebar_position: 4
title: Time-Series Databases
description: Time-series database implementation for metrics, IoT, financial data, and observability
tags: [backend, database, timeseries, metrics, iot]
---

# Time-Series Databases

Efficient storage and querying for time-stamped data (metrics, IoT sensors, financial ticks, logs).

## When to Use

Use when building:
- **Dashboards** requiring real-time metrics visualization
- **Monitoring systems** for DevOps and infrastructure
- **IoT platforms** with millions of devices
- **Financial applications** with tick data
- **Observability backends** for application metrics

## Multi-Language Support

This skill provides patterns for:
- **Python**: TimescaleDB (psycopg2, asyncpg), InfluxDB client
- **TypeScript**: TimescaleDB (node-postgres), InfluxDB client
- **Rust**: TimescaleDB (tokio-postgres), InfluxDB client
- **Go**: TimescaleDB (pgx), InfluxDB client, QuestDB

## Database Selection

Choose based on primary use case:

**TimescaleDB** - PostgreSQL extension
- Use when: Already on PostgreSQL, need SQL + JOINs, hybrid workloads
- Query: Standard SQL
- Scale: 100K-1M inserts/sec

**InfluxDB** - Purpose-built TSDB
- Use when: DevOps metrics, Prometheus integration, Telegraf ecosystem
- Query: InfluxQL or Flux
- Scale: 500K-1M points/sec

**ClickHouse** - Columnar analytics
- Use when: Fastest aggregations needed, analytics dashboards, log analysis
- Query: SQL
- Scale: 1M-10M inserts/sec, 100M-1B rows/sec queries

**QuestDB** - High-throughput IoT
- Use when: Highest write performance needed, financial tick data
- Query: SQL + Line Protocol
- Scale: 4M+ inserts/sec

## Core Patterns

### 1. Hypertables (TimescaleDB)

Automatic time-based partitioning:

```sql
CREATE TABLE sensor_data (
  time        TIMESTAMPTZ NOT NULL,
  sensor_id   INTEGER NOT NULL,
  temperature DOUBLE PRECISION,
  humidity    DOUBLE PRECISION
);

SELECT create_hypertable('sensor_data', 'time');
```

Benefits:
- Efficient data expiration (drop old chunks)
- Parallel query execution
- Compression on older chunks (10-20x savings)

### 2. Continuous Aggregates

Pre-computed rollups for fast dashboard queries:

```sql
-- TimescaleDB: hourly rollup
CREATE MATERIALIZED VIEW sensor_data_hourly
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 hour', time) AS hour,
       sensor_id,
       AVG(temperature) AS avg_temp,
       MAX(temperature) AS max_temp,
       MIN(temperature) AS min_temp
FROM sensor_data
GROUP BY hour, sensor_id;

-- Auto-refresh policy
SELECT add_continuous_aggregate_policy('sensor_data_hourly',
  start_offset => INTERVAL '3 hours',
  end_offset => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour');
```

Query strategy:
- Short range (last hour): Raw data
- Medium range (last day): 1-minute rollups
- Long range (last month): 1-hour rollups
- Very long (last year): Daily rollups

### 3. Retention Policies

Automatic data expiration:

```sql
-- TimescaleDB: delete data older than 90 days
SELECT add_retention_policy('sensor_data', INTERVAL '90 days');
```

Common patterns:
- Raw data: 7-90 days
- Hourly rollups: 1-2 years
- Daily rollups: Infinite retention

### 4. Downsampling for Visualization

Use LTTB (Largest-Triangle-Three-Buckets) algorithm to reduce points for charts.

Problem: Browsers can't smoothly render 1M points
Solution: Downsample to 500-1000 points preserving visual fidelity

```sql
-- TimescaleDB toolkit LTTB
SELECT time, value
FROM lttb(
  'SELECT time, temperature FROM sensor_data WHERE sensor_id = 1',
  1000  -- target number of points
);
```

Thresholds:
- < 1,000 points: No downsampling
- 1,000-10,000 points: LTTB to 1,000 points
- 10,000+ points: LTTB to 500 points or use pre-aggregated data

## Dashboard Integration

Time-series databases are the primary data source for real-time dashboards.

Query patterns by component:

| Component | Query Pattern | Example |
|-----------|---------------|---------|
| KPI Card | Latest value | `SELECT temperature FROM sensors ORDER BY time DESC LIMIT 1` |
| Trend Chart | Time-bucketed avg | `SELECT time_bucket('5m', time), AVG(cpu) GROUP BY 1` |
| Heatmap | Multi-metric window | `SELECT hour, AVG(cpu), AVG(memory) GROUP BY hour` |
| Alert | Threshold check | `SELECT COUNT(*) WHERE cpu > 80 AND time > NOW() - '5m'` |

Auto-refresh intervals:
- Critical alerts: 1-5 seconds (WebSocket)
- Operations dashboard: 10-30 seconds (polling)
- Analytics dashboard: 1-5 minutes (cached)
- Historical reports: On-demand only

## Performance Optimization

### Write Optimization

Batch inserts:

| Database | Batch Size | Expected Throughput |
|----------|------------|---------------------|
| TimescaleDB | 1,000-10,000 | 100K-1M rows/sec |
| InfluxDB | 5,000+ | 500K-1M points/sec |
| ClickHouse | 10,000-100,000 | 1M-10M rows/sec |
| QuestDB | 10,000+ | 4M+ rows/sec |

### Query Optimization

**Rule 1:** Always filter by time first (indexed)

```sql
-- BAD: Full table scan
SELECT * FROM metrics WHERE metric_name = 'cpu';

-- GOOD: Time index used
SELECT * FROM metrics
WHERE time > NOW() - INTERVAL '1 hour'
  AND metric_name = 'cpu';
```

**Rule 2:** Use continuous aggregates for dashboard queries

**Rule 3:** Downsample for visualization

```typescript
// Request optimal point count
const points = Math.min(1000, chartWidth);
const query = `/api/metrics?start=${start}&end=${end}&points=${points}`;
```

## Use Cases

**DevOps Monitoring** → InfluxDB or TimescaleDB
- Prometheus metrics, application traces, infrastructure

**IoT Sensor Data** → QuestDB or TimescaleDB
- Millions of devices, high write throughput

**Financial Tick Data** → QuestDB or ClickHouse
- Sub-millisecond queries, OHLC aggregates

**User Analytics** → ClickHouse
- Event tracking, daily active users, funnel analysis

**Real-time Dashboards** → Any TSDB + Continuous Aggregates
- Pre-computed rollups, WebSocket streaming, LTTB downsampling

## Related Skills

- [Dashboards](../frontend/dashboards) - Visualizing time-series data
- [Real-time Sync](./realtime-sync) - WebSocket streaming for live metrics
- [Observability](./observability) - Application metrics and traces
- [Data Visualization](../frontend/data-viz) - Chart components for metrics

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/databases-timeseries)
- TimescaleDB: https://www.timescale.com/
- InfluxDB: https://www.influxdata.com/
- ClickHouse: https://clickhouse.com/
- QuestDB: https://questdb.io/
