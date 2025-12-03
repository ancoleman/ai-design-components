# Connection Pooling Guide

## Why Connection Pooling Matters

Creating database connections is expensive:
- TCP handshake: 50-100ms
- Authentication: 50-200ms
- **Total**: 100-500ms per connection

Connection pooling reuses connections, reducing latency from 100ms to <1ms.

## Recommended Pool Sizes

| Deployment Type | Pool Size | max_overflow | Reasoning |
|----------------|-----------|--------------|-----------|
| **Web API (single instance)** | 10-20 | 10 | `(CPU cores × 2) + effective_spindle_count` |
| **Serverless (per function)** | 1-2 | 0 | Minimize idle connections, use pgBouncer |
| **Background workers** | 5-10 | 5 | Depends on concurrency needs |
| **High-traffic API** | 20-50 | 20 | Monitor with pgBouncer/PgPool II |

**Formula:** `pool_size = (num_cores * 2) + num_disks`
- Example: 4 cores, 1 disk = 10 connections
- More connections != better (causes contention)

## Configuration by Language

### Python (SQLAlchemy)

```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,           # Normal connections
    max_overflow=10,        # Extra connections under load (total max = 30)
    pool_timeout=30,        # Wait 30s for connection before error
    pool_recycle=3600,      # Recycle connections after 1 hour
    pool_pre_ping=True      # Verify connection before use (prevents stale connections)
)
```

### TypeScript (Prisma)

```typescript
// Configure in DATABASE_URL
// postgresql://user:pass@host/db?connection_limit=20&pool_timeout=30

// Or programmatically
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL,
    },
  },
})
```

### TypeScript (Drizzle + pg)

```typescript
import { Pool } from 'pg'

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,                    // Max connections
  min: 5,                     // Min idle connections
  idleTimeoutMillis: 30000,   // Close idle after 30s
  connectionTimeoutMillis: 2000,  // Wait 2s for connection
})
```

### Rust (SQLx)

```rust
use sqlx::postgres::PgPoolOptions;
use std::time::Duration;

let pool = PgPoolOptions::new()
    .max_connections(20)
    .min_connections(5)
    .acquire_timeout(Duration::from_secs(30))
    .idle_timeout(Some(Duration::from_secs(600)))  // 10 min
    .max_lifetime(Some(Duration::from_secs(3600))) // 1 hour
    .connect("postgresql://...")
    .await?;
```

### Go (database/sql)

```go
import "database/sql"

db, _ := sql.Open("postgres", "postgresql://...")
db.SetMaxOpenConns(20)                    // Max connections
db.SetMaxIdleConns(10)                    // Max idle connections
db.SetConnMaxLifetime(time.Hour)          // Max lifetime
db.SetConnMaxIdleTime(time.Minute * 10)   // Max idle time
```

### Go (pgx)

```go
import "github.com/jackc/pgx/v5/pgxpool"

config, _ := pgxpool.ParseConfig("postgresql://...")
config.MaxConns = 20
config.MinConns = 5
config.MaxConnLifetime = time.Hour
config.MaxConnIdleTime = time.Minute * 10
pool, _ := pgxpool.NewWithConfig(context.Background(), config)
```

## Serverless Considerations

### Problem

Traditional connection pooling doesn't work well in serverless:
- Each function instance creates its own pool
- 100 concurrent functions × 10 connections = 1,000 database connections!
- Database runs out of connections (typically max 100-500)

### Solution: pgBouncer

**pgBouncer** is a connection pooler that sits between your app and database.

```
Your App (1000 instances, 1 connection each) → pgBouncer (20 connections) → Database
```

**Setup:**

```bash
# Install pgBouncer
apt-get install pgbouncer

# Configure /etc/pgbouncer/pgbouncer.ini
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
```

**Application Configuration:**

```python
# Connect to pgBouncer instead of PostgreSQL directly
engine = create_engine(
    "postgresql://user:pass@pgbouncer-host:6432/db",
    pool_size=1,  # Serverless: 1-2 connections per function
    max_overflow=0
)
```

### Serverless Database Services

Modern serverless databases handle pooling automatically:

| Service | Type | Connection Pooling |
|---------|------|--------------------|
| **Neon** | PostgreSQL | Built-in connection pooler |
| **PlanetScale** | MySQL | Built-in connection pooler |
| **Supabase** | PostgreSQL | pgBouncer included |

```typescript
// Neon serverless driver (no pooling needed)
import { neon } from '@neondatabase/serverless'

const sql = neon(process.env.DATABASE_URL!)
const users = await sql`SELECT * FROM users`
```

## Monitoring Connection Pools

### PostgreSQL

```sql
-- Current connections
SELECT count(*) FROM pg_stat_activity;

-- Connections by state
SELECT state, count(*)
FROM pg_stat_activity
GROUP BY state;

-- Long-running connections
SELECT pid, now() - query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active' AND now() - query_start > interval '5 minutes';

-- Kill connection
SELECT pg_terminate_backend(pid);
```

### Application Metrics

**Track:**
- Active connections
- Idle connections
- Connection wait time
- Connection errors

**Python (SQLAlchemy):**

```python
# Check pool status
print(f"Pool size: {engine.pool.size()}")
print(f"Checked out: {engine.pool.checkedout()}")
print(f"Overflow: {engine.pool.overflow()}")
```

**Rust (SQLx):**

```rust
println!("Pool size: {}", pool.size());
println!("Idle connections: {}", pool.num_idle());
```

## Best Practices

### 1. Right-Size Your Pool

**Too few connections:**
- Requests wait for connections
- High latency
- Poor throughput

**Too many connections:**
- Database CPU exhaustion
- Memory pressure
- Context switching overhead

**Start with:** `pool_size = (num_cores * 2) + num_disks`

### 2. Use Connection Lifecycle Management

```python
# SQLAlchemy - verify connection before use
engine = create_engine(..., pool_pre_ping=True)

# Also recycle connections periodically
engine = create_engine(..., pool_recycle=3600)  # 1 hour
```

### 3. Handle Connection Errors

```python
from sqlalchemy.exc import OperationalError
import time

def execute_with_retry(query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return session.execute(query)
        except OperationalError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### 4. Close Connections Properly

```python
# Context manager (recommended)
with Session(engine) as session:
    user = session.query(User).first()

# Or manual close
session = Session(engine)
try:
    user = session.query(User).first()
finally:
    session.close()
```

### 5. Serverless: Use Connection Poolers

```typescript
// Option 1: Use serverless-friendly database
const sql = neon(process.env.DATABASE_URL!)  // Neon handles pooling

// Option 2: Use pgBouncer
const pool = new Pool({
  connectionString: process.env.PGBOUNCER_URL,
  max: 1  // Serverless: 1 connection per function
})

// Option 3: Use Prisma Data Proxy (for Prisma users)
// DATABASE_URL="prisma://aws-us-east-1.prisma-data.com/?api_key=..."
```

## Troubleshooting

### "Too many connections" Error

**Cause:** Application pool size × number of instances > database max_connections

**Solutions:**
1. Reduce `pool_size` in application
2. Increase `max_connections` in PostgreSQL (requires more RAM)
3. Add pgBouncer connection pooler
4. Use serverless database (Neon, PlanetScale)

### High Connection Wait Times

**Cause:** Pool too small for workload

**Solutions:**
1. Increase `pool_size`
2. Increase `max_overflow` for bursty traffic
3. Optimize slow queries (reduce connection hold time)

### Stale Connections

**Cause:** Database closed connections but pool still holds them

**Solutions:**
1. Enable `pool_pre_ping` (SQLAlchemy)
2. Set `pool_recycle` to less than database timeout
3. Configure `idle_timeout` and `max_lifetime` (SQLx)

## Resources

- pgBouncer: https://www.pgbouncer.org/
- PgPool II: https://www.pgpool.net/
- HikariCP (Java): https://github.com/brettwooldridge/HikariCP
