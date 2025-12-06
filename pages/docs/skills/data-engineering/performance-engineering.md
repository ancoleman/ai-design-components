---
sidebar_position: 6
title: Performance Engineering
description: Load testing, profiling, and optimization for reliable, scalable systems
tags: [data-engineering, performance, load-testing, profiling, optimization, k6, locust]
---

# Performance Engineering

Load testing, profiling, and optimization to deliver reliable, scalable systems. Covers choosing performance testing approaches (load, stress, soak, spike), profiling techniques (CPU, memory, I/O), and optimization strategies for backend APIs, databases, and frontend applications.

## When to Use

Use when:
- Validating system can handle expected traffic
- Finding maximum capacity and breaking points
- Identifying why the application is slow
- Detecting memory leaks or resource exhaustion
- Optimizing Core Web Vitals for SEO
- Setting up performance testing in CI/CD
- Reducing cloud infrastructure costs

## Key Features

### Performance Testing Types

- **Load Testing**: Validate system behavior under expected traffic levels
- **Stress Testing**: Find system capacity limits and failure modes
- **Soak Testing**: Identify memory leaks, resource exhaustion over time
- **Spike Testing**: Validate system response to sudden traffic spikes

### Quick Decision Framework

```
What am I trying to learn?
├─ Can my system handle expected traffic? → LOAD TEST
├─ What's the maximum capacity? → STRESS TEST
├─ Will it stay stable over time? → SOAK TEST
└─ Can it handle traffic spikes? → SPIKE TEST
```

## Quick Start

### k6 Load Testing (JavaScript)

**Installation:**
```bash
brew install k6  # macOS
sudo apt-get install k6  # Linux
```

**Basic Load Test:**
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },  // Ramp up
    { duration: '1m', target: 20 },   // Stay at 20 users
    { duration: '30s', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests < 500ms
    http_req_failed: ['rate<0.01'],    // Error rate < 1%
  },
};

export default function () {
  const res = http.get('https://api.example.com/products');
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
  sleep(1);
}
```

**Run:** `k6 run script.js`

### Locust Load Testing (Python)

**Installation:**
```bash
pip install locust
```

**Basic Load Test:**
```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://api.example.com"

    @task(3)
    def view_products(self):
        self.client.get("/products")

    @task(1)
    def view_product_detail(self):
        self.client.get("/products/123")
```

**Run:** `locust -f locustfile.py --headless -u 100 -r 10 --run-time 10m`

## Profiling Quick Starts

### When to Profile

| Symptom | Profiling Type | Tool |
|---------|----------------|------|
| High CPU (>70%) | CPU Profiling | py-spy, pprof, DevTools |
| Memory growing | Memory Profiling | memory_profiler, pprof heap |
| Slow response, low CPU | I/O Profiling | Query logs, pprof block |

### Python Profiling (py-spy)

```bash
pip install py-spy

# Profile running process (production-safe)
py-spy record -o profile.svg --pid <PID> --duration 30

# Top-like view
py-spy top --pid <PID>
```

### Go Profiling (pprof)

```go
import (
    "net/http"
    _ "net/http/pprof"
)

func main() {
    go func() {
        http.ListenAndServe("localhost:6060", nil)
    }()
    startApp()
}
```

**Capture profile:**
```bash
# CPU profile (30 seconds)
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# Interactive analysis
(pprof) top
(pprof) web
```

### TypeScript/JavaScript Profiling

**Node.js:**
```bash
node --inspect app.js
# Open chrome://inspect
# Performance tab → Record
```

**clinic.js:**
```bash
npm install -g clinic
clinic doctor -- node app.js
```

## Optimization Strategies

### Caching with Redis

```python
import redis
r = redis.Redis()

def get_cached_data(key, fn, ttl=300):
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    data = fn()
    r.setex(key, ttl, json.dumps(data))
    return data
```

**When to cache**:
- Data queried frequently (>100 req/min)
- Data freshness tolerance (>1 minute acceptable staleness)

### Database Query Optimization

**N+1 Prevention:**
```python
# ❌ Bad: N+1 queries
users = User.query.all()
for user in users:
    print(user.orders)  # Separate query per user

# ✅ Good: Eager loading
users = User.query.options(joinedload(User.orders)).all()
```

**Indexing:**
```sql
CREATE INDEX idx_users_email ON users(email);
```

### API Performance: Cursor-based Pagination

```typescript
app.get('/api/products', async (req, res) => {
  const { cursor, limit = 20 } = req.query;

  const products = await db.query(
    'SELECT * FROM products WHERE id > ? ORDER BY id LIMIT ?',
    [cursor || 0, limit]
  );

  res.json({
    data: products,
    next_cursor: products[products.length - 1]?.id,
  });
});
```

### Frontend Performance (Core Web Vitals)

**Key metrics**:
- **LCP (Largest Contentful Paint)**: < 2.5s
- **INP (Interaction to Next Paint)**: < 200ms
- **CLS (Cumulative Layout Shift)**: < 0.1

**Optimization techniques**:
- Code splitting (lazy loading)
- Image optimization (WebP, responsive, lazy loading)
- Preload critical resources
- Minimize render-blocking resources

## Performance SLOs

### Recommended SLOs by Service Type

| Service Type | p95 Latency | p99 Latency | Availability |
|--------------|-------------|-------------|--------------|
| User-Facing API | < 200ms | < 500ms | 99.9% |
| Internal API | < 100ms | < 300ms | 99.5% |
| Database Query | < 50ms | < 100ms | 99.99% |
| Background Job | < 5s | < 10s | 99% |
| Real-time API | < 50ms | < 100ms | 99.95% |

### SLO Selection Process

1. Measure baseline performance
2. Identify user expectations
3. Set achievable targets (10-20% better than baseline)
4. Iterate as system matures

## CI/CD Integration

### Performance Testing in GitHub Actions

```yaml
name: Performance Tests

on:
  pull_request:
    branches: [main]

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install k6
        run: |
          curl https://github.com/grafana/k6/releases/download/v0.48.0/k6-v0.48.0-linux-amd64.tar.gz -L | tar xvz
          sudo mv k6-v0.48.0-linux-amd64/k6 /usr/local/bin/

      - name: Run load test
        run: k6 run tests/load/api-test.js
```

**Performance budgets (fail build if violated):**
```javascript
export const options = {
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};
```

## Profiling Workflow

**Standard process**:
1. Observe symptoms (high CPU, memory growth, slow response)
2. Hypothesize bottleneck (CPU? Memory? I/O?)
3. Choose profiling type based on hypothesis
4. Run profiler under realistic load
5. Analyze profile (flamegraph, call tree)
6. Identify hot spots (top 20% functions using 80% resources)
7. Optimize bottlenecks
8. Re-profile to validate improvement

**Best practices**:
- Profile under realistic load (not idle systems)
- Use sampling profilers (py-spy, pprof) in production (low overhead)
- Focus on hot paths (optimize biggest bottlenecks first)
- Validate optimizations with before/after comparisons

## Tool Recommendations

### Load Testing

**Primary: k6** (JavaScript-based, Grafana-backed)
- Modern architecture, cloud-native
- JavaScript DSL (ES6+)
- Grafana/Prometheus integration
- Multi-protocol (HTTP/1.1, HTTP/2, WebSocket, gRPC)

**Alternative: Locust** (Python-based)
- Python-native (write tests in Python)
- Web UI for real-time monitoring
- Flexible for complex user scenarios

### Profiling

**Python**:
- py-spy (sampling, production-safe)
- cProfile (deterministic, detailed)
- memory_profiler (memory leak detection)

**Go**:
- pprof (built-in, CPU/heap/goroutine/block profiling)

**TypeScript/JavaScript**:
- Chrome DevTools (browser/Node.js)
- clinic.js (Node.js performance suite)

## Related Skills

- [SQL Optimization](./optimizing-sql) - Database query performance tuning
- [Data Transformation](./transforming-data) - ETL/ELT pipeline optimization
- [Streaming Data](./streaming-data) - Real-time system performance

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/performance-engineering)
- [k6 Documentation](https://k6.io/docs/)
- [Locust Documentation](https://docs.locust.io/)
- [Web Vitals](https://web.dev/vitals/)
