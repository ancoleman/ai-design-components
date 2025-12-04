# QuestDB Reference Guide

QuestDB is a high-performance time-series database optimized for maximum write throughput (4M+ inserts/sec) using SIMD-accelerated SQL.

## Installation

```bash
# Docker
docker run -p 9000:9000 -p 9009:9009 -p 8812:8812 questdb/questdb:latest

# Homebrew (macOS)
brew install questdb
questdb start

# Binary download
wget https://github.com/questdb/questdb/releases/download/7.3.4/questdb-7.3.4-rt-linux-amd64.tar.gz
tar -xzf questdb-7.3.4-rt-linux-amd64.tar.gz
./questdb-7.3.4-rt-linux-amd64/bin/questdb.sh start
```

Access:
- **Web Console:** http://localhost:9000
- **PostgreSQL wire protocol:** localhost:8812
- **InfluxDB Line Protocol (ILP):** localhost:9009

## Core Features

### 1. SIMD-Accelerated Queries

QuestDB uses SIMD (Single Instruction, Multiple Data) for vectorized query execution, achieving 100x faster aggregations than traditional row-based processing.

**Optimized operations:**
- Time-based aggregations (AVG, SUM, MIN, MAX)
- SAMPLE BY (downsampling)
- WHERE clause filtering
- JOIN operations

### 2. Designated Timestamp Column

Every table must have a designated timestamp for optimal partitioning.

```sql
CREATE TABLE trades (
  symbol SYMBOL,
  side SYMBOL,
  price DOUBLE,
  amount DOUBLE,
  timestamp TIMESTAMP
) TIMESTAMP(timestamp) PARTITION BY DAY;
```

**Key points:**
- `TIMESTAMP(timestamp)` designates the time column
- `PARTITION BY DAY` creates daily partitions (also: HOUR, MONTH, YEAR)
- SYMBOL type for low-cardinality strings (internalized)

### 3. Symbol Type for String Optimization

Use SYMBOL instead of STRING for repeated values (tickers, device IDs, regions).

```sql
CREATE TABLE sensor_data (
  sensor_id SYMBOL,        -- Internalized (stored once)
  region SYMBOL,
  temperature DOUBLE,
  humidity INT,
  ts TIMESTAMP
) TIMESTAMP(ts) PARTITION BY HOUR;
```

**Benefits:**
- 10-100x space savings for repeated strings
- Faster filtering and aggregations
- Automatic deduplication

## Ingestion Methods

### Method 1: InfluxDB Line Protocol (ILP) - Fastest

**4M+ inserts/sec with auto-commit batching.**

```python
# Python client
from questdb.ingress import Sender, IngressError

with Sender('localhost', 9009) as sender:
    sender.row(
        'trades',
        symbols={'symbol': 'BTC-USD', 'side': 'buy'},
        columns={'price': 50000.0, 'amount': 0.1},
        at=TimestampNanos.now()
    )
    sender.flush()
```

**Key features:**
- Auto-creates tables with optimal schema
- Batching for maximum throughput
- Named vs positional timestamps

### Method 2: PostgreSQL Wire Protocol

Standard SQL INSERT with JDBC/ODBC/psycopg compatibility.

```python
import psycopg2

conn = psycopg2.connect(
    host='localhost',
    port=8812,
    user='admin',
    password='quest',
    database='qdb'
)

cursor = conn.cursor()
cursor.execute("""
    INSERT INTO trades VALUES
    ('BTC-USD', 'buy', 50000.0, 0.1, '2025-12-03T10:00:00.000000Z')
""")
conn.commit()
```

**Batch inserts for performance:**

```python
cursor.executemany(
    "INSERT INTO trades VALUES (%s, %s, %s, %s, %s)",
    [
        ('BTC-USD', 'buy', 50000.0, 0.1, '2025-12-03T10:00:00Z'),
        ('ETH-USD', 'sell', 3000.0, 1.5, '2025-12-03T10:00:01Z'),
        # ... 1000s more
    ]
)
conn.commit()
```

### Method 3: REST API (CSV Upload)

```bash
curl -F data=@trades.csv 'http://localhost:9000/imp'
```

CSV format:
```csv
symbol,side,price,amount,timestamp
BTC-USD,buy,50000.0,0.1,2025-12-03T10:00:00.000000Z
ETH-USD,sell,3000.0,1.5,2025-12-03T10:00:01.000000Z
```

## Querying Patterns

### SAMPLE BY - Downsampling

Efficiently downsample high-frequency data.

```sql
-- 1-minute OHLC (Open-High-Low-Close) for trading data
SELECT
    timestamp,
    symbol,
    first(price) AS open,
    max(price) AS high,
    min(price) AS low,
    last(price) AS close,
    sum(amount) AS volume
FROM trades
WHERE symbol = 'BTC-USD'
SAMPLE BY 1m ALIGN TO CALENDAR;
```

**Sampling intervals:**
- Microseconds: `100us`, `500us`
- Milliseconds: `10ms`, `100ms`
- Seconds: `1s`, `30s`
- Minutes: `1m`, `5m`, `15m`
- Hours: `1h`, `4h`
- Days: `1d`

**ALIGN TO CALENDAR** aligns buckets to clock boundaries (e.g., 10:00:00, 10:01:00).

### LATEST ON - Get Most Recent Row

```sql
-- Latest price for each symbol
SELECT * FROM trades
LATEST ON timestamp PARTITION BY symbol;
```

Efficient replacement for:
```sql
-- Slow approach (avoid)
SELECT * FROM trades t1
WHERE timestamp = (
    SELECT MAX(timestamp) FROM trades t2
    WHERE t1.symbol = t2.symbol
);
```

### ASOF JOIN - Point-in-Time Join

Join time-series with different frequencies.

```sql
-- Join trades with mid-market prices
SELECT
    t.timestamp,
    t.symbol,
    t.price AS trade_price,
    m.mid_price,
    (t.price - m.mid_price) AS spread
FROM trades t
ASOF JOIN market_data m
WHERE t.symbol = m.symbol;
```

**Use case:** Join sparse events (trades) with dense reference data (quotes).

## Partitioning Strategy

### Partition Guidelines

```sql
-- High-frequency data (millions/day): Partition by HOUR
CREATE TABLE ticks (...) TIMESTAMP(ts) PARTITION BY HOUR;

-- Medium-frequency (100K-1M/day): Partition by DAY
CREATE TABLE metrics (...) TIMESTAMP(ts) PARTITION BY DAY;

-- Low-frequency (<100K/day): Partition by MONTH
CREATE TABLE events (...) TIMESTAMP(ts) PARTITION BY MONTH;
```

### Partition Management

```sql
-- Drop old partitions (data retention)
ALTER TABLE trades DROP PARTITION LIST '2024-01', '2024-02';

-- Detach partition (archive without delete)
ALTER TABLE trades DETACH PARTITION LIST '2024-01';
```

## Performance Optimization

### 1. Out-of-Order Ingestion

QuestDB handles out-of-order data automatically but with performance cost.

**Configuration (server.conf):**
```
cairo.max.uncommitted.rows=100000
cairo.o3.max.lag=60000000    # 60 seconds in microseconds
```

**Best practice:** Ingest in chronological order when possible.

### 2. Commit Lag

Set commit lag to batch micro-commits for higher throughput.

```sql
-- 1-second commit lag (ILP only)
ALTER TABLE trades SET PARAM commit.lag = 1000000us;
```

### 3. Columnar Storage Benefits

QuestDB stores data columnar-first:
- Only read columns in SELECT clause
- Compression-friendly
- SIMD vectorization

**Query optimization:**
```sql
-- Fast: Only reads 2 columns
SELECT timestamp, price FROM trades WHERE symbol = 'BTC-USD';

-- Slower: Reads all columns
SELECT * FROM trades WHERE symbol = 'BTC-USD';
```

## Financial Tick Data Use Case

QuestDB excels at handling financial market data.

### Schema Design

```sql
CREATE TABLE quotes (
    symbol SYMBOL,
    exchange SYMBOL,
    bid_price DOUBLE,
    bid_size INT,
    ask_price DOUBLE,
    ask_size INT,
    timestamp TIMESTAMP
) TIMESTAMP(timestamp) PARTITION BY DAY
INDEX(symbol CAPACITY 256) INDEX(exchange CAPACITY 16);
```

### Common Queries

**Time-weighted average price (TWAP):**
```sql
SELECT
    symbol,
    avg(mid_price) AS twap
FROM (
    SELECT
        symbol,
        (bid_price + ask_price) / 2 AS mid_price,
        timestamp
    FROM quotes
    WHERE timestamp > dateadd('h', -1, now())
)
GROUP BY symbol;
```

**Volume-weighted average price (VWAP):**
```sql
SELECT
    symbol,
    sum(price * amount) / sum(amount) AS vwap
FROM trades
WHERE timestamp > dateadd('d', -1, now())
SAMPLE BY 5m;
```

## Integration with Python

### Official Client

```python
from questdb.ingress import Sender, IngressError
import datetime

def ingest_sensor_data(sensor_id, temp, humidity):
    with Sender('localhost', 9009) as sender:
        sender.row(
            'sensors',
            symbols={'sensor_id': sensor_id},
            columns={
                'temperature': temp,
                'humidity': humidity
            },
            at=datetime.datetime.utcnow()
        )
        sender.flush()
```

### Using psycopg2 (PostgreSQL compatibility)

```python
import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host='localhost',
    port=8812,
    user='admin',
    password='quest',
    database='qdb'
)

# Query to DataFrame
df = pd.read_sql("""
    SELECT * FROM trades
    WHERE symbol = 'BTC-USD'
    SAMPLE BY 1h
""", conn)

print(df.head())
```

## Integration with Grafana

QuestDB has native PostgreSQL wire protocol support for Grafana.

**Data Source Configuration:**
- Type: PostgreSQL
- Host: localhost:8812
- Database: qdb
- User: admin
- Password: quest
- TLS/SSL Mode: disable

**Example query for Grafana:**
```sql
SELECT
    timestamp AS time,
    symbol AS metric,
    price AS value
FROM trades
WHERE
    $__timeFilter(timestamp)
    AND symbol IN ($symbols)
SAMPLE BY $__interval
```

## Comparison with Other TSDBs

| Feature | QuestDB | TimescaleDB | InfluxDB | ClickHouse |
|---------|---------|-------------|----------|------------|
| **Write throughput** | 4M+ rows/s | 1M rows/s | 1M rows/s | 10M+ rows/s |
| **Query language** | SQL | SQL | InfluxQL/Flux | SQL |
| **Out-of-order data** | Native | Manual | Native | Manual |
| **PostgreSQL compatible** | Yes | Yes | No | No |
| **SIMD acceleration** | Yes | No | No | Yes |
| **Best for** | Financial, IoT | Hybrid workloads | DevOps metrics | Analytics |

## Best Practices

1. **Use SYMBOL type** for repeated strings (10-100x space savings)
2. **Partition by time frequency** (HOUR for high-volume, DAY for medium, MONTH for low)
3. **Ingest in chronological order** when possible (avoid O3 overhead)
4. **Use ILP for maximum throughput** (4M+ inserts/sec)
5. **Use SAMPLE BY for downsampling** (much faster than GROUP BY)
6. **Use LATEST ON instead of subqueries** for most recent rows
7. **Select only needed columns** (columnar storage optimization)
8. **Set commit lag for batching** (1-5 seconds for high throughput)

## Common Pitfalls

**Don't:**
- Use VARCHAR/STRING for repeated values (use SYMBOL)
- Query without WHERE on timestamp (full table scan)
- Use `SELECT *` in production (read all columns)
- Insert out-of-order data without O3 configuration
- Over-partition (too many small partitions)

**Do:**
- Filter by time range first (leverages partitioning)
- Use SYMBOL for low-cardinality columns
- Batch inserts for better performance
- Use SAMPLE BY for downsampling (not GROUP BY)
- Monitor partition sizes and consolidate if needed

## Resources

- **Official docs:** https://questdb.io/docs/
- **GitHub:** https://github.com/questdb/questdb
- **Context7 ID:** (Not yet available)
- **Community:** https://questdb.io/community/

---

**When to use QuestDB:**
- Financial tick data (trades, quotes, order books)
- High-frequency IoT sensor data
- Maximum write throughput required (4M+ inserts/sec)
- Need SQL with PostgreSQL compatibility
- Time-series analytics with SIMD acceleration

**When to use alternatives:**
- **TimescaleDB:** Already on PostgreSQL, need relational JOINs
- **InfluxDB:** DevOps metrics, Prometheus ecosystem
- **ClickHouse:** Analytical workloads, 10M+ inserts/sec needed
