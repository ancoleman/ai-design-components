# databases-timeseries Claude Skill

Production-ready Claude Skill for implementing time-series databases in metrics, IoT, financial, and observability systems.

## What This Skill Does

This skill guides implementation of time-series databases optimized for:
- **DevOps Monitoring**: Prometheus metrics, application traces, infrastructure monitoring
- **IoT Sensor Networks**: Temperature, pressure, location data from millions of devices
- **Financial Systems**: Stock tickers, trading data, portfolio analytics
- **User Analytics**: Behavior tracking, A/B tests, business KPIs
- **Real-time Dashboards**: Pre-aggregated data for fast visualization

## When to Use This Skill

Use this skill when:
- Building real-time monitoring dashboards
- Storing high-volume sensor data (IoT)
- Implementing DevOps observability backends
- Creating financial data platforms
- Optimizing time-series queries (> 1M rows)
- Needing automatic data expiration (retention policies)
- Requiring efficient downsampling for visualization

## Structure

```
using-timeseries-databases/
├── SKILL.md                          # Main skill file (230 lines, <500 limit)
├── init.md                           # Master plan and research
├── README.md                         # This file
├── references/                       # Detailed documentation (4 files)
│   ├── timescaledb.md               # TimescaleDB guide (850 lines)
│   ├── influxdb.md                  # InfluxDB guide (600 lines)
│   ├── clickhouse.md                # ClickHouse guide (700 lines)
│   └── downsampling-strategies.md   # LTTB algorithm (400 lines)
├── examples/                         # Working code examples (2 complete projects)
│   ├── metrics-dashboard-backend/   # TimescaleDB + FastAPI
│   │   ├── schema.sql               # Hypertables, continuous aggregates
│   │   ├── api.py                   # REST API with LTTB downsampling
│   │   └── README.md                # Setup and usage guide
│   └── iot-data-pipeline/           # InfluxDB + Go + MQTT
│       ├── main.go                  # MQTT → InfluxDB pipeline
│       └── README.md                # Architecture and deployment
└── scripts/                          # Token-free utility scripts (2 scripts)
    ├── setup_hypertable.py          # Create TimescaleDB hypertables
    └── generate_retention_policy.py # Generate retention recommendations
```

## Database Coverage

### TimescaleDB (PostgreSQL Extension)
- **Best for**: PostgreSQL shops, hybrid workloads (relational + time-series)
- **Query**: Standard SQL
- **Scale**: 100K-1M inserts/sec
- **Strengths**: SQL compatibility, JSONB support, mature ecosystem

### InfluxDB (Purpose-Built TSDB)
- **Best for**: DevOps metrics, Prometheus integration, Telegraf ecosystem
- **Query**: InfluxQL (v1, v3) or Flux (v2)
- **Scale**: 500K-1M points/sec
- **Strengths**: Native Grafana support, built-in downsampling

### ClickHouse (Columnar Analytics)
- **Best for**: Fastest aggregations, analytics dashboards, log analysis
- **Query**: SQL
- **Scale**: 1M-10M inserts/sec, 100M-1B rows/sec queries
- **Strengths**: Best compression (15-30x), horizontal scaling

### QuestDB (High-Throughput IoT)
- **Best for**: Highest write performance, financial tick data
- **Query**: SQL + Line Protocol
- **Scale**: 4M+ inserts/sec (single node)
- **Strengths**: Sub-millisecond queries, SIMD optimization

## Key Patterns

### 1. Hypertables (TimescaleDB)
Automatic time-based partitioning:
- Efficient data expiration (drop old chunks)
- Parallel query execution
- Compression on older chunks (10-20x savings)

### 2. Continuous Aggregates
Pre-computed rollups for fast dashboards:
- 1-minute rollups: Last 90 days
- 1-hour rollups: Last 1-2 years
- Daily rollups: Forever

Query strategy: Short ranges use raw data, long ranges use rollups.

### 3. Retention Policies
Automatic data expiration:
- Raw data: 7-90 days (troubleshooting)
- Hourly rollups: 1-2 years (trends)
- Daily rollups: Infinite (historical reporting)

### 4. LTTB Downsampling
Largest-Triangle-Three-Buckets algorithm:
- Reduce 1M points → 1,000 for charting
- Preserves visual fidelity (peaks, valleys)
- 99%+ network bandwidth savings

## Dashboard Integration

Time-series databases are the **primary data source** for real-time dashboards:

```
Application Metrics
        ↓
TimescaleDB Hypertables
        ↓
Continuous Aggregates (1min, 1hour, daily)
        ↓
REST API with LTTB Downsampling
        ↓
React Dashboard (Recharts/visx)
```

## Quick Start Examples

### Example 1: TimescaleDB + FastAPI Dashboard

```bash
cd examples/metrics-dashboard-backend/

# Start TimescaleDB
docker run -d --name timescaledb -p 5432:5432 \
  -e POSTGRES_PASSWORD=password \
  timescale/timescaledb:latest-pg16

# Create schema
psql -h localhost -U postgres -f schema.sql

# Run API
pip install fastapi uvicorn psycopg2-binary
python api.py

# Test
curl "http://localhost:8000/api/metrics/cpu_usage?start=1h&points=1000"
```

### Example 2: IoT Sensor Pipeline (InfluxDB + Go)

```bash
cd examples/iot-data-pipeline/

# Start infrastructure
docker run -d --name mosquitto -p 1883:1883 eclipse-mosquitto
docker run -d --name influxdb -p 8086:8086 influxdb:3.0-alpine

# Run pipeline
export INFLUX_TOKEN="your-token"
go run main.go

# Simulate sensors
python sensor_simulator.py
```

## Utility Scripts

### Setup Hypertable

```bash
python scripts/setup_hypertable.py \
  --table metrics \
  --partition-interval "7 days" \
  --compress-after "7 days" \
  --retention "90 days" \
  --segment-by "host,metric_name"
```

### Generate Retention Policy

```bash
python scripts/generate_retention_policy.py \
  --table metrics \
  --daily-rows 1000000 \
  --use-case devops \
  --budget-gb 500
```

## Progressive Disclosure

The skill follows Anthropic's best practices for progressive disclosure:

1. **SKILL.md** (230 lines): Core patterns, database selection, quick examples
2. **references/** (4 files): Deep-dive guides for each database
3. **examples/** (2 projects): Production-ready code with full setup
4. **scripts/** (2 utilities): Token-free automation (executed, not loaded)

Claude loads files on-demand as needed, minimizing token usage.

## Performance Benchmarks

| Database    | Write Throughput | Query Latency (1h) | Compression |
|-------------|------------------|--------------------|-------------|
| TimescaleDB | 100K-1M/sec      | <100ms             | 10-20x      |
| InfluxDB    | 500K-1M/sec      | <50ms              | 8-15x       |
| ClickHouse  | 1M-10M/sec       | <50ms              | 15-30x      |
| QuestDB     | 4M+/sec          | <10ms              | 10-15x      |

## Use Cases

| Use Case                  | Recommended Database      | Key Features                          |
|---------------------------|---------------------------|---------------------------------------|
| DevOps Monitoring         | InfluxDB or TimescaleDB   | Prometheus integration, Grafana       |
| IoT Sensor Networks       | QuestDB or TimescaleDB    | High write throughput, MQTT support   |
| Financial Tick Data       | QuestDB or ClickHouse     | Sub-ms queries, OHLC aggregates       |
| User Analytics            | ClickHouse                | Fastest aggregations, event tracking  |
| Real-time Dashboards      | Any + Continuous Aggs     | Pre-computed rollups, LTTB downsampling |

## Best Practices

1. **Batch Inserts**: 1,000-10,000 rows per transaction
2. **Continuous Aggregates**: Pre-compute hourly/daily rollups
3. **Retention Policies**: Auto-delete old data to control costs
4. **Compression**: Enable on chunks > 7 days old
5. **LTTB Downsampling**: Reduce points for frontend rendering (500-1000 points)
6. **Query Optimization**: Always filter by time first (indexed)
7. **Dashboard Integration**: Use WebSocket for real-time (< 5s latency)
8. **Monitoring**: Track query latency, compression ratio, chunk count

## Dependencies

### Python (TimescaleDB examples)
```bash
pip install psycopg2-binary fastapi uvicorn
```

### Go (InfluxDB examples)
```bash
go get github.com/eclipse/paho.mqtt.golang
go get github.com/influxdata/influxdb-client-go/v2
```

### TypeScript (Optional)
```bash
npm install pg @influxdata/influxdb-client @clickhouse/client
```

## Integration with Other Skills

| Skill                | Integration Pattern                                      |
|----------------------|----------------------------------------------------------|
| **dashboards**       | Primary data source for KPI cards, trend charts          |
| **data-viz**         | Provides pre-aggregated data for line/area charts        |
| **feedback**         | Powers alerting thresholds (CPU > 80%, latency > 500ms)  |
| **ai-chat**          | Enables "Show me last hour's error rate" queries         |
| **observability**    | Stores Prometheus metrics, traces, logs                  |
| **api-patterns**     | Exposes time-series data via REST/GraphQL                |
| **realtime-sync**    | Streams live metrics via WebSocket/SSE                   |

## Validation Checklist

- [x] SKILL.md under 500 lines (230 lines)
- [x] Frontmatter valid (name, description)
- [x] Progressive disclosure (references, examples, scripts)
- [x] Multi-language support (Python, TypeScript, Go)
- [x] Working code examples (2 complete projects)
- [x] Token-free scripts (2 utilities)
- [x] Dashboard integration documented
- [x] LTTB downsampling explained with code
- [x] Retention policies for 7d/30d/1y scenarios
- [x] No time-sensitive information
- [x] Consistent terminology
- [x] Concrete examples (not abstract)

## Version

- **Created**: December 2, 2025
- **Status**: Production-ready
- **Database Versions**: TimescaleDB 2.16.x, InfluxDB 3.0.x, ClickHouse 24.11.x, QuestDB 8.1.x
- **Skill Version**: 1.0.0

## License

This skill is part of the ai-design-components repository and follows the repository's license.

## Support

For issues or questions:
1. Check reference files for detailed documentation
2. Review example projects for working code
3. Run utility scripts for automated setup
4. Consult init.md for research and decision frameworks
