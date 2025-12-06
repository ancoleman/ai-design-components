# Optimization Strategies

## Table of Contents

1. [Optimization Philosophy](#optimization-philosophy)
2. [Caching Strategies](#caching-strategies)
3. [Database Query Optimization](#database-query-optimization)
4. [API Performance Patterns](#api-performance-patterns)
5. [Connection Pooling](#connection-pooling)
6. [Async and Concurrency](#async-and-concurrency)
7. [Algorithm Optimization](#algorithm-optimization)

---

## Optimization Philosophy

### First Principles

**Rule 1: Profile Before Optimizing**
- Never optimize without profiling data
- Intuition about bottlenecks is often wrong
- "Premature optimization is the root of all evil" - Donald Knuth

**Rule 2: Focus on Hot Paths**
- Top 20% of code causes 80% of performance issues (Pareto Principle)
- Optimize functions consuming most resources
- Ignore infrequently called code (low impact)

**Rule 3: Measure Impact**
- Benchmark before and after optimization
- Quantify improvement (2x faster? 50% less memory?)
- Re-profile to validate (ensure no regressions)

**Rule 4: Consider Trade-offs**
- Performance vs. maintainability (complex optimizations harder to maintain)
- Memory vs. speed (caching uses memory for speed)
- Consistency vs. latency (eventual consistency faster than strong consistency)

### Optimization Priority

1. **Algorithmic improvements** (O(n²) → O(n log n))
2. **Caching** (avoid recomputation)
3. **Database query optimization** (indexes, N+1 prevention)
4. **I/O reduction** (batching, connection pooling)
5. **Concurrency** (parallelization where safe)
6. **Micro-optimizations** (last resort, minimal impact)

---

## Caching Strategies

### When to Cache

**Decision tree:**
```
Is data queried frequently? (>100 req/min)
├─ Yes → Consider caching
└─ No → Don't cache (overhead not worth it)

How fresh must data be?
├─ Real-time (seconds) → Don't cache
├─ Near real-time (1-5 min) → Cache with short TTL
└─ Eventually consistent (>5 min) → Cache with longer TTL

How complex is data generation?
├─ Simple query (indexed) → Optimize query, don't cache
├─ Complex (joins, aggregations) → Cache + optimize
└─ Very complex (computed) → Consider pre-computation
```

### Caching Layers

#### 1. Application-Level Caching (In-Memory)

**Use case:** Frequently accessed objects, shared across requests.

**Python (functools.lru_cache):**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_user_permissions(user_id: int):
    # Expensive database query
    return db.query("SELECT * FROM permissions WHERE user_id = ?", user_id)

# First call: Query database
perms = get_user_permissions(123)

# Second call: Return from cache
perms = get_user_permissions(123)
```

**TypeScript (simple object cache):**
```typescript
const cache = new Map<string, any>();

function getCached<T>(key: string, fn: () => T, ttl: number): T {
  const cached = cache.get(key);
  if (cached && Date.now() < cached.expiry) {
    return cached.value;
  }

  const value = fn();
  cache.set(key, {
    value,
    expiry: Date.now() + ttl
  });

  return value;
}

// Usage
const users = getCached('users', () => fetchUsers(), 60000); // 1 min TTL
```

**Go (sync.Map):**
```go
import "sync"

var cache sync.Map

func getCached(key string, fn func() interface{}) interface{} {
    if val, ok := cache.Load(key); ok {
        return val
    }

    val := fn()
    cache.Store(key, val)
    return val
}
```

**Pros:**
- Very fast (<1ms)
- No network overhead
- Simple implementation

**Cons:**
- Limited by process memory
- Not shared across instances
- Invalidation requires restart or TTL

#### 2. Redis (Distributed Cache)

**Use case:** Shared cache across multiple instances, session data, leaderboards.

**Python (redis-py):**
```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_cached_data(key: str, fn, ttl: int = 300):
    # Try cache
    cached = r.get(key)
    if cached:
        return json.loads(cached)

    # Cache miss, compute and store
    data = fn()
    r.setex(key, ttl, json.dumps(data))
    return data

# Usage
users = get_cached_data('users:active', lambda: db.query("SELECT * FROM users WHERE active = 1"), ttl=60)
```

**TypeScript (ioredis):**
```typescript
import Redis from 'ioredis';

const redis = new Redis();

async function getCachedData<T>(
  key: string,
  fn: () => Promise<T>,
  ttl: number = 300
): Promise<T> {
  // Try cache
  const cached = await redis.get(key);
  if (cached) {
    return JSON.parse(cached);
  }

  // Cache miss
  const data = await fn();
  await redis.setex(key, ttl, JSON.stringify(data));
  return data;
}

// Usage
const users = await getCachedData('users:active', () => db.query('SELECT * FROM users WHERE active = 1'), 60);
```

**Go (go-redis):**
```go
import (
    "context"
    "encoding/json"
    "github.com/go-redis/redis/v8"
    "time"
)

var ctx = context.Background()
var rdb = redis.NewClient(&redis.Options{
    Addr: "localhost:6379",
})

func getCachedData(key string, fn func() interface{}, ttl time.Duration) (interface{}, error) {
    // Try cache
    val, err := rdb.Get(ctx, key).Result()
    if err == nil {
        var data interface{}
        json.Unmarshal([]byte(val), &data)
        return data, nil
    }

    // Cache miss
    data := fn()
    json, _ := json.Marshal(data)
    rdb.Set(ctx, key, json, ttl)
    return data, nil
}
```

**Pros:**
- Shared across instances
- Fast (<1ms over LAN)
- Rich data structures (lists, sets, sorted sets)
- Persistence options

**Cons:**
- Network overhead
- Additional infrastructure
- Cache invalidation complexity

#### 3. CDN Caching

**Use case:** Static assets, API responses for global users.

**HTTP headers for CDN caching:**
```typescript
// TypeScript (Express)
app.get('/api/products', (req, res) => {
  res.set({
    'Cache-Control': 'public, max-age=300, s-maxage=600',
    'Vary': 'Accept-Encoding',
  });

  const products = getProducts();
  res.json(products);
});
```

**Cache-Control directives:**
- `public`: Cacheable by CDN and browsers
- `private`: Cacheable by browsers only (not CDN)
- `max-age=300`: Cache for 5 minutes (browser)
- `s-maxage=600`: Cache for 10 minutes (CDN)
- `no-cache`: Revalidate before serving
- `no-store`: Never cache

**Pros:**
- Global distribution
- Reduced origin load
- Low latency for global users

**Cons:**
- Invalidation complexity (purge API)
- Costs (CDN bandwidth)
- Stale data risk

#### 4. Materialized Views (Database)

**Use case:** Complex aggregations queried frequently.

**PostgreSQL:**
```sql
-- Create materialized view
CREATE MATERIALIZED VIEW daily_sales AS
SELECT
    DATE(created_at) as date,
    SUM(amount) as total_sales,
    COUNT(*) as order_count
FROM orders
GROUP BY DATE(created_at);

-- Query is now fast
SELECT * FROM daily_sales WHERE date = '2025-12-01';

-- Refresh view (nightly cron job)
REFRESH MATERIALIZED VIEW daily_sales;
```

**Pros:**
- Pre-computed, very fast queries
- Transparent to application (looks like table)
- Reduces database load

**Cons:**
- Stale data (refresh required)
- Storage overhead
- Refresh time (can be slow for large datasets)

### Cache Invalidation Strategies

#### Time-Based (TTL)

**When to use:** Data changes predictably (every N minutes/hours).

```python
# Cache for 5 minutes
r.setex('products:featured', 300, json.dumps(products))
```

**Pros:** Simple, automatic expiration.
**Cons:** Stale data until TTL expires.

#### Event-Based (Manual Invalidation)

**When to use:** Data changes known (on create/update/delete).

```python
def update_product(product_id, data):
    # Update database
    db.update('products', product_id, data)

    # Invalidate cache
    r.delete(f'product:{product_id}')
    r.delete('products:all')
```

**Pros:** Fresh data immediately.
**Cons:** Requires code changes, cache stampede risk.

#### Write-Through Cache

**When to use:** Strong consistency required.

```python
def update_product(product_id, data):
    # Update database
    db.update('products', product_id, data)

    # Update cache
    r.setex(f'product:{product_id}', 300, json.dumps(data))
```

**Pros:** Cache always fresh.
**Cons:** Write latency (two writes), complexity.

---

## Database Query Optimization

### N+1 Query Problem

**Problem:** Loading related data in loop causes N queries.

**Bad (N+1):**
```python
# 1 query to get users
users = User.query.all()

# N queries (one per user)
for user in users:
    print(user.orders)  # Separate query per user
```

**Good (Eager Loading):**
```python
# Single query with JOIN
users = User.query.options(joinedload(User.orders)).all()

for user in users:
    print(user.orders)  # No additional query
```

**TypeScript (Prisma):**
```typescript
// Bad: N+1
const users = await prisma.user.findMany();
for (const user of users) {
  const orders = await prisma.order.findMany({ where: { userId: user.id } });
}

// Good: Include related data
const users = await prisma.user.findMany({
  include: { orders: true }
});
```

**Go (sqlx):**
```go
// Bad: N+1
users := []User{}
db.Select(&users, "SELECT * FROM users")

for _, user := range users {
    orders := []Order{}
    db.Select(&orders, "SELECT * FROM orders WHERE user_id = ?", user.ID)
}

// Good: JOIN
type UserWithOrders struct {
    User
    Orders []Order
}

result := []UserWithOrders{}
db.Select(&result, `
    SELECT u.*, o.*
    FROM users u
    LEFT JOIN orders o ON o.user_id = u.id
`)
```

### Indexing

**When to add index:**
- Column used in WHERE clause frequently
- Column used in JOIN condition
- Column used in ORDER BY
- Foreign keys

**When NOT to add index:**
- Small tables (<1000 rows)
- Columns rarely queried
- High write:read ratio (indexes slow writes)

**PostgreSQL:**
```sql
-- Add index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (for multiple columns in WHERE)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Check if index is used
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';
```

**Index types:**
- **B-tree (default):** General purpose, equality and range queries
- **Hash:** Equality only, faster than B-tree for equality
- **GIN/GiST:** Full-text search, JSON, arrays
- **BRIN:** Very large tables, sequential data (timestamps)

### Query Analysis (EXPLAIN)

**PostgreSQL:**
```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123 AND status = 'active';
```

**Output interpretation:**
```
Seq Scan on orders  (cost=0.00..1234.56 rows=100)  -- BAD: Sequential scan
  Filter: (user_id = 123 AND status = 'active')

Index Scan using idx_orders_user_status on orders  -- GOOD: Index scan
  (cost=0.29..8.30 rows=100)
  Index Cond: (user_id = 123 AND status = 'active')
```

**Look for:**
- **Seq Scan:** Bad (full table scan), add index
- **Index Scan:** Good (using index)
- **high cost:** Query expensive, optimize
- **high rows:** Too many rows, add filter

### Connection Pooling

**Problem:** Creating database connections is expensive (100ms+).

**Solution:** Reuse connections via pooling.

**Python (SQLAlchemy):**
```python
from sqlalchemy import create_engine

engine = create_engine(
    'postgresql://user:pass@localhost/db',
    pool_size=10,           # Max connections in pool
    max_overflow=20,        # Max connections beyond pool_size
    pool_timeout=30,        # Wait 30s for connection
    pool_recycle=3600,      # Recycle connections after 1h
)
```

**TypeScript (node-postgres):**
```typescript
import { Pool } from 'pg';

const pool = new Pool({
  host: 'localhost',
  database: 'mydb',
  max: 20,              // Max connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Use pool
const result = await pool.query('SELECT * FROM users');
```

**Go (database/sql):**
```go
import "database/sql"

db, _ := sql.Open("postgres", "postgres://user:pass@localhost/db")
db.SetMaxOpenConns(25)          // Max open connections
db.SetMaxIdleConns(5)           // Max idle connections
db.SetConnMaxLifetime(5 * time.Minute)  // Max connection lifetime
```

**Pool sizing:**
- **CPU-bound:** connections = CPU cores
- **I/O-bound:** connections = 2-3× CPU cores
- **Start small:** 10-20 connections, increase if needed
- **Monitor:** Connection utilization, wait times

### Query Optimization Checklist

- [ ] Identify slow queries (query logs, APM)
- [ ] Run EXPLAIN ANALYZE
- [ ] Add indexes to WHERE/JOIN/ORDER BY columns
- [ ] Prevent N+1 queries (eager loading)
- [ ] Use connection pooling
- [ ] Limit result set size (pagination)
- [ ] Avoid SELECT * (specify columns)
- [ ] Use prepared statements (prevent SQL injection + performance)

---

## API Performance Patterns

### Pagination

**Problem:** Returning large datasets is slow and memory-intensive.

**Solution:** Limit result set size.

#### Offset/Limit Pagination

**Simple, but slow for large offsets.**

```typescript
// TypeScript (Express)
app.get('/api/products', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 20;
  const offset = (page - 1) * limit;

  const products = await db.query(
    'SELECT * FROM products LIMIT ? OFFSET ?',
    [limit, offset]
  );

  res.json({
    data: products,
    page,
    limit,
  });
});
```

**Cons:** Slow for large offsets (database must skip rows).

#### Cursor-Based Pagination

**Fast, efficient for large datasets.**

```typescript
// TypeScript (Express)
app.get('/api/products', async (req, res) => {
  const cursor = req.query.cursor;
  const limit = parseInt(req.query.limit) || 20;

  const query = cursor
    ? db.query('SELECT * FROM products WHERE id > ? ORDER BY id LIMIT ?', [cursor, limit])
    : db.query('SELECT * FROM products ORDER BY id LIMIT ?', [limit]);

  const products = await query;
  const nextCursor = products[products.length - 1]?.id;

  res.json({
    data: products,
    next_cursor: nextCursor,
  });
});
```

**Pros:** Constant time complexity, efficient for large datasets.
**Cons:** No direct page jumping (page 5), cursor must be opaque.

### Field Selection (Partial Responses)

**Problem:** Returning all fields wastes bandwidth and serialization time.

**Solution:** Allow clients to select fields.

```typescript
// TypeScript (Express)
app.get('/api/users', async (req, res) => {
  const fields = req.query.fields?.split(',') || ['id', 'name', 'email'];

  const query = `SELECT ${fields.join(', ')} FROM users`;
  const users = await db.query(query);

  res.json(users);
});

// Usage: GET /api/users?fields=id,name
```

**GraphQL alternative:**
```graphql
query {
  users {
    id
    name
    # Only fetch requested fields
  }
}
```

### Batch Operations

**Problem:** Multiple requests have overhead (latency, connection overhead).

**Solution:** Combine multiple operations into single request.

```typescript
// Bad: Multiple requests
const user1 = await fetch('/api/users/1').then(r => r.json());
const user2 = await fetch('/api/users/2').then(r => r.json());
const user3 = await fetch('/api/users/3').then(r => r.json());

// Good: Single batch request
const users = await fetch('/api/users/batch', {
  method: 'POST',
  body: JSON.stringify({ ids: [1, 2, 3] })
}).then(r => r.json());
```

**Server-side batch endpoint:**
```typescript
app.post('/api/users/batch', async (req, res) => {
  const { ids } = req.body;

  const users = await db.query(
    'SELECT * FROM users WHERE id IN (?)',
    [ids]
  );

  res.json(users);
});
```

### Response Compression

**Enable gzip/brotli compression for responses.**

```typescript
// TypeScript (Express)
import compression from 'compression';

app.use(compression({
  level: 6,              // Compression level (1-9)
  threshold: 1024,       // Only compress > 1KB
}));
```

**Savings:** 60-80% reduction for JSON responses.

### API Performance Checklist

- [ ] Implement pagination (cursor-based for large datasets)
- [ ] Allow field selection (reduce payload size)
- [ ] Batch operations where possible
- [ ] Enable response compression (gzip/brotli)
- [ ] Rate limiting (prevent abuse)
- [ ] ETag support (conditional requests)
- [ ] HTTP/2 (multiplexing, header compression)

---

## Connection Pooling

### HTTP Connection Pooling

**Problem:** Creating HTTP connections is expensive (DNS, TCP handshake, TLS).

**Solution:** Reuse connections via pooling.

**Python (requests with Session):**
```python
import requests

# Bad: New connection per request
for i in range(100):
    requests.get('https://api.example.com/data')

# Good: Reuse connections
session = requests.Session()
for i in range(100):
    session.get('https://api.example.com/data')
```

**TypeScript (node-fetch with agent):**
```typescript
import fetch from 'node-fetch';
import { Agent } from 'https';

const agent = new Agent({
  keepAlive: true,
  maxSockets: 50,
});

for (let i = 0; i < 100; i++) {
  await fetch('https://api.example.com/data', { agent });
}
```

**Go (http.Client with Transport):**
```go
import (
    "net/http"
    "time"
)

client := &http.Client{
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 10,
        IdleConnTimeout:     90 * time.Second,
    },
}

for i := 0; i < 100; i++ {
    client.Get("https://api.example.com/data")
}
```

---

## Async and Concurrency

### When to Use Async

**Use async for I/O-bound operations:**
- Database queries
- Network requests
- File system operations

**Avoid async for CPU-bound operations:**
- Complex calculations
- Data transformations
- Image processing (use worker threads instead)

### Python Async (asyncio)

```python
import asyncio
import aiohttp

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    # Bad: Sequential (10s total for 10 requests)
    results = []
    for i in range(10):
        data = await fetch_data(f'https://api.example.com/data/{i}')
        results.append(data)

    # Good: Concurrent (1s total for 10 requests)
    tasks = [fetch_data(f'https://api.example.com/data/{i}') for i in range(10)]
    results = await asyncio.gather(*tasks)

asyncio.run(main())
```

### TypeScript Async (Promise.all)

```typescript
// Bad: Sequential
const results = [];
for (let i = 0; i < 10; i++) {
  const data = await fetch(`https://api.example.com/data/${i}`).then(r => r.json());
  results.push(data);
}

// Good: Concurrent
const promises = Array.from({ length: 10 }, (_, i) =>
  fetch(`https://api.example.com/data/${i}`).then(r => r.json())
);
const results = await Promise.all(promises);
```

### Go Goroutines

```go
import "sync"

// Bad: Sequential
results := make([]Data, 10)
for i := 0; i < 10; i++ {
    results[i] = fetchData(i)
}

// Good: Concurrent
var wg sync.WaitGroup
results := make([]Data, 10)

for i := 0; i < 10; i++ {
    wg.Add(1)
    go func(index int) {
        defer wg.Done()
        results[index] = fetchData(index)
    }(i)
}

wg.Wait()
```

---

## Algorithm Optimization

### Time Complexity Matters

**Common complexities:**
- O(1): Constant time (hash table lookup)
- O(log n): Logarithmic (binary search)
- O(n): Linear (single loop)
- O(n log n): Efficient sorting (merge sort)
- O(n²): Quadratic (nested loops) - **AVOID**
- O(2ⁿ): Exponential - **VERY BAD**

**Example (remove duplicates):**
```python
# Bad: O(n²)
def remove_duplicates_slow(items):
    result = []
    for item in items:
        if item not in result:  # O(n) lookup
            result.append(item)
    return result

# Good: O(n)
def remove_duplicates_fast(items):
    return list(set(items))  # O(n) with hash set
```

### Data Structure Selection

| Operation | List | Set | Dict |
|-----------|------|-----|------|
| Lookup | O(n) | O(1) | O(1) |
| Insert | O(1) | O(1) | O(1) |
| Delete | O(n) | O(1) | O(1) |
| Ordered | ✅ | ❌ | ❌ (Python 3.7+) |

**Use sets for membership testing:**
```python
# Bad: O(n) per lookup
allowed_ids = [1, 2, 3, 4, 5]
if user_id in allowed_ids:  # O(n)
    pass

# Good: O(1) per lookup
allowed_ids = {1, 2, 3, 4, 5}
if user_id in allowed_ids:  # O(1)
    pass
```

### Optimization Checklist

- [ ] Profile before optimizing (identify hot paths)
- [ ] Fix algorithm complexity (O(n²) → O(n log n))
- [ ] Cache expensive computations
- [ ] Optimize database queries (indexes, N+1)
- [ ] Use connection pooling
- [ ] Implement pagination
- [ ] Enable response compression
- [ ] Parallelize I/O operations
- [ ] Measure improvement (validate with benchmarks)
