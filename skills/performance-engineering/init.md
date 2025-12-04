# Performance Engineering Skill - Master Plan

**Skill Name:** `performance-engineering`
**Skill Level:** Mid Level (5,000-8,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Performance Testing Taxonomy](#performance-testing-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Multi-Language Implementations](#multi-language-implementations)
7. [Library Recommendations](#library-recommendations)
8. [Skill Structure Design](#skill-structure-design)
9. [Integration Points](#integration-points)
10. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

Performance engineering is critical for delivering reliable, scalable systems that meet user expectations. In 2025, with increasing demands for real-time responsiveness, global scale, and cost efficiency, systematic performance optimization has become a core competency.

**Market Drivers:**
- **Cloud Cost Optimization:** Poor performance directly impacts infrastructure costs (over-provisioning, inefficient resource usage)
- **User Experience Expectations:** Sub-second response times are now baseline expectations, not aspirations
- **Regulatory Compliance:** SLA requirements and compliance standards mandate performance testing
- **AI/ML Workload Growth:** LLM inference, vector search, and real-time AI features introduce new performance challenges
- **Global Scale Requirements:** Systems must perform well across geographies with varying network conditions

**Strategic Value:**
1. **Universal Need:** Every production system requires performance validation
2. **Cost Reduction:** Performance optimization reduces cloud/infrastructure costs by 30-70%
3. **Risk Mitigation:** Load testing prevents costly production outages and poor launch experiences
4. **Competitive Advantage:** Faster systems win users and retain them
5. **Developer Productivity:** Slow local development loops hurt team velocity

### How This Differs from Existing Solutions

**Existing Performance Documentation:**
- **Tool-Specific:** k6 docs, Locust docs, profiler-specific guides (separate, disconnected)
- **Single-Language Focus:** Python OR JavaScript OR Go, not unified patterns
- **Tactical Focus:** "How to run a load test" vs. "When to use load vs. stress vs. soak testing"
- **Missing Integration:** Performance testing treated as separate from profiling, optimization, and monitoring

**Our Approach:**
- **Holistic Performance Engineering:** Load testing + profiling + optimization + monitoring in one skill
- **Multi-Language Unified:** Consistent patterns across Python, Go, TypeScript
- **Decision-First Framework:** When to use load/stress/soak, what metrics matter, when to optimize
- **Full-Stack Coverage:** Backend (API), frontend (Core Web Vitals), database query optimization
- **Modern Best Practices:** 2025 patterns including AI-driven testing, shift-left performance, continuous profiling

### Target Audience

**Primary Users:**
- Backend engineers optimizing API performance
- Full-stack developers improving application responsiveness
- DevOps/SRE teams establishing performance baselines and monitoring
- Frontend developers optimizing Core Web Vitals and bundle sizes

**Skill Level Assumptions:**
- Understands basic HTTP concepts (requests, responses, status codes)
- Familiar with at least one programming language (Python, Go, or TypeScript)
- Knows basic profiling concepts (CPU, memory, I/O)
- Understands difference between load testing and profiling (but needs guidance on when/how to use each)

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **Performance Testing Strategy**
   - When to use load, stress, soak, spike testing
   - How to design realistic test scenarios
   - Interpreting test results and identifying bottlenecks
   - Setting meaningful SLOs (Service Level Objectives)

2. **Load Testing Patterns**
   - Load testing: Validate system under expected traffic
   - Stress testing: Find breaking points and capacity limits
   - Soak testing: Identify memory leaks and degradation over time
   - Spike testing: Validate auto-scaling and burst handling

3. **Profiling and Bottleneck Identification**
   - CPU profiling: Find hot paths and expensive functions
   - Memory profiling: Detect leaks, excessive allocations
   - I/O profiling: Database queries, network calls, filesystem operations
   - Language-specific profilers (pprof for Go, py-spy for Python, Chrome DevTools for TypeScript)

4. **Optimization Strategies**
   - Caching strategies (in-memory, CDN, database query caching)
   - Database query optimization (indexes, N+1 prevention, connection pooling)
   - API performance patterns (pagination, field selection, batch operations)
   - Frontend performance (code splitting, lazy loading, Core Web Vitals)

5. **Benchmarking and Metrics**
   - Key performance metrics (latency percentiles, throughput, error rate)
   - Establishing baselines and detecting regressions
   - Continuous performance monitoring
   - Performance budgets and SLOs

### What This Skill Does NOT Cover

**Out of Scope:**
- **Security Testing:** Covered by `security-hardening` skill (penetration testing, vulnerability scanning)
- **Infrastructure Provisioning:** Covered by `infrastructure-as-code` skill (Terraform, CloudFormation)
- **Application Monitoring:** Covered by separate observability skill (distributed tracing, log aggregation)
- **Chaos Engineering:** Advanced resilience testing (separate advanced skill)
- **Mobile App Performance:** Specialized mobile profiling (separate skill)

**Boundary Cases (Minimal Coverage):**
- **Database Administration:** Touch on query optimization, not full DBA topics
- **Network Engineering:** Cover basic network profiling, not deep network optimization
- **Hardware Performance:** Focus on software optimization, not hardware tuning

### Success Criteria

**A user successfully uses this skill when they can:**
1. Design and execute load tests for their API/service
2. Identify performance bottlenecks using profiling tools
3. Optimize database queries and API endpoints
4. Implement effective caching strategies
5. Measure and improve Core Web Vitals for frontend applications
6. Establish performance SLOs and track regressions
7. Integrate performance testing into CI/CD pipelines

---

## Research Findings

### Research Date: December 3, 2025

**Research Tools Used:**
- Google Search Grounding (Vertex AI): Performance engineering best practices 2025
- Context7: k6, Locust library documentation
- Official documentation: k6.io, locust.io, pprof, py-spy

### Key Trends for 2025

**1. Shift-Left Performance Testing**
- Performance testing earlier in development cycle (not just pre-production)
- Developer-owned performance validation
- Fast feedback loops (local load testing, quick profiling)

**2. AI-Driven Performance Optimization**
- AI-powered bottleneck detection
- Automated test scenario generation
- Intelligent load profile creation based on production traffic patterns

**3. Continuous Performance Monitoring**
- Performance testing in CI/CD pipelines (every commit)
- Automated regression detection
- Performance budgets enforced via build gates

**4. Cost-Driven Optimization**
- Cloud cost reduction as primary driver for performance work
- Resource efficiency metrics (cost per request, CPU utilization)
- Auto-scaling optimization to reduce over-provisioning

**5. Frontend Performance Focus (Core Web Vitals)**
- LCP (Largest Contentful Paint) < 2.5s
- FID (First Input Delay) < 100ms → replaced by INP (Interaction to Next Paint) < 200ms
- CLS (Cumulative Layout Shift) < 0.1
- Google ranking factor and user retention metric

**6. Multi-Language Profiling Standardization**
- Continuous profiling in production (Grafana Pyroscope, Google Cloud Profiler)
- Unified profiling formats (pprof becoming cross-language standard)
- Language-agnostic profiling UIs

### Performance Testing Evolution (2025)

**Load Testing Philosophy:**
```
Traditional: "Run load test before launch, hope it works"
Modern 2025: "Continuous load testing, shift-left validation, production traffic replay"
```

**Key Principles:**
1. **Realistic Scenarios:** Use production traffic patterns, not artificial constant load
2. **Gradual Ramp-Up:** Identify capacity limits with controlled load increases
3. **SLO-Driven:** Test against Service Level Objectives (e.g., p95 latency < 200ms)
4. **Automated Execution:** CI/CD integration for regression detection
5. **Distributed Testing:** Simulate global user distribution

---

## Performance Testing Taxonomy

### Testing Types (By Purpose)

#### Tier 1: Load Testing (Baseline Performance)

**Purpose:** Validate system behavior under expected traffic levels

**Characteristics:**
- **Load Level:** Normal to high (expected peak traffic)
- **Duration:** 10-30 minutes
- **Goal:** Verify system meets SLOs under typical conditions
- **Metrics:** Response time percentiles (p50, p95, p99), throughput, error rate

**When to Use:**
- Before production launch (capacity planning)
- After major refactors (regression testing)
- Validating auto-scaling configuration
- Setting performance baselines

**Example Scenarios:**
- E-commerce site: Simulate Black Friday traffic (10,000 concurrent users)
- API service: Test 1,000 requests/second sustained load
- Dashboard: Validate 500 concurrent viewers

---

#### Tier 2: Stress Testing (Breaking Point Discovery)

**Purpose:** Find system capacity limits and failure modes

**Characteristics:**
- **Load Level:** Progressively increasing beyond normal capacity
- **Duration:** Until system breaks or reaches max capacity
- **Goal:** Identify bottlenecks and maximum throughput
- **Metrics:** Max sustained throughput, error rate threshold, failure modes

**When to Use:**
- Capacity planning (how much can we handle?)
- Understanding failure behavior (graceful degradation vs. cascading failure)
- Validating rate limiting and circuit breakers
- Infrastructure sizing decisions

**Example Scenarios:**
- API service: Ramp from 100 to 10,000 req/s until errors spike
- Database: Increase connection pool until connection exhaustion
- Message queue: Push messages until consumer lag becomes unrecoverable

---

#### Tier 3: Soak Testing (Endurance/Stability)

**Purpose:** Identify memory leaks, resource exhaustion, degradation over time

**Characteristics:**
- **Load Level:** Moderate (typical production load)
- **Duration:** Extended (hours to days)
- **Goal:** Ensure stability over time, detect resource leaks
- **Metrics:** Memory growth over time, connection leaks, disk space usage, latency degradation

**When to Use:**
- Detecting memory leaks
- Validating connection pool cleanup
- Testing long-running batch jobs
- Ensuring database query plan stability

**Example Scenarios:**
- API service: Run at 60% capacity for 24 hours, monitor memory
- Background job processor: Process 10,000 jobs over 12 hours
- WebSocket server: Maintain 1,000 connections for 8 hours

---

#### Tier 4: Spike Testing (Burst Traffic Handling)

**Purpose:** Validate system response to sudden traffic spikes

**Characteristics:**
- **Load Level:** Sudden jump from low to very high
- **Duration:** Short bursts (minutes)
- **Goal:** Test auto-scaling responsiveness and burst capacity
- **Metrics:** Time to scale, error rate during spike, recovery time

**When to Use:**
- Validating auto-scaling configuration
- Testing event-driven systems (product launches, breaking news)
- Ensuring rate limiting doesn't block legitimate traffic
- Cloud resource burst capacity validation

**Example Scenarios:**
- News site: Simulate breaking news traffic spike (0 to 5,000 users in 1 minute)
- Ticketing platform: Concert ticket release (10x normal load instantly)
- API rate limiter: Burst 100 req/s for 10 seconds, then 10 req/s baseline

---

### Profiling Types (By Resource)

#### CPU Profiling

**Purpose:** Identify computationally expensive code paths

**When to Use:**
- High CPU utilization (>70%)
- Slow response times with low I/O wait
- Hot path optimization
- Algorithm inefficiencies

**Tools by Language:**
- **Python:** py-spy, cProfile, Pyroscope
- **Go:** pprof (built-in), Pyroscope
- **TypeScript/Node.js:** Chrome DevTools, clinic.js, 0x

**Key Metrics:**
- CPU time per function
- Call graph (who calls whom)
- Hot spots (functions using most CPU)

---

#### Memory Profiling

**Purpose:** Detect memory leaks, excessive allocations, heap growth

**When to Use:**
- Memory usage growing over time
- Out-of-memory errors
- High garbage collection overhead
- Large object allocations

**Tools by Language:**
- **Python:** memory_profiler, tracemalloc, Pympler
- **Go:** pprof (heap profile), runtime.MemStats
- **TypeScript/Node.js:** Chrome DevTools heap snapshot, clinic.js

**Key Metrics:**
- Heap size over time
- Allocation rate
- Object retention (leaked objects)
- GC pause time

---

#### I/O Profiling

**Purpose:** Identify slow database queries, network calls, filesystem operations

**When to Use:**
- High I/O wait time
- Slow response times with low CPU usage
- Database connection exhaustion
- Network latency issues

**Tools by Language:**
- **Python:** Django Debug Toolbar, py-spy (I/O events), asyncio profiler
- **Go:** pprof (block profile), database query logging
- **TypeScript/Node.js:** Chrome DevTools network tab, database query logs

**Key Metrics:**
- Query execution time
- Number of queries (N+1 detection)
- Network latency
- File I/O throughput

---

## Decision Frameworks

### Framework 1: Which Performance Test Should I Use?

**Decision Tree:**

```
START: I need to test my system's performance

Q1: What am I trying to learn?
  ├─ "Can my system handle expected traffic?" → LOAD TEST
  ├─ "What's the maximum capacity?" → STRESS TEST
  ├─ "Will it stay stable over time?" → SOAK TEST
  └─ "Can it handle traffic spikes?" → SPIKE TEST

Q2: What's my current stage?
  ├─ "Pre-launch / capacity planning" → LOAD TEST + STRESS TEST
  ├─ "Post-refactor / regression check" → LOAD TEST
  ├─ "Investigating memory leak" → SOAK TEST
  └─ "Validating auto-scaling" → SPIKE TEST

Q3: What resources do I have?
  ├─ "< 30 minutes" → LOAD TEST (quick baseline)
  ├─ "Few hours" → LOAD TEST + STRESS TEST
  └─ "Overnight/weekend" → SOAK TEST
```

**Examples:**

| Scenario | Test Type | Rationale |
|----------|-----------|-----------|
| New API launch next week | Load Test | Verify meets SLOs under expected traffic |
| Refactored database layer | Load Test | Ensure no performance regression |
| Memory usage creeping up | Soak Test | Detect memory leak over 24h run |
| Black Friday preparation | Stress Test + Spike Test | Find capacity limits and test burst handling |
| Auto-scaling validation | Spike Test | Ensure scales fast enough for traffic bursts |
| Investigating slow queries | Profiling (I/O) | NOT load testing, need query-level insight |

---

### Framework 2: Which Profiling Approach Should I Use?

**Decision Matrix:**

| Symptom | Likely Bottleneck | Profiling Type | Tool Recommendation |
|---------|-------------------|----------------|---------------------|
| High CPU usage (>70%) | Expensive computations | CPU Profiling | pprof (Go), py-spy (Python), DevTools (JS) |
| Memory growing over time | Memory leak | Memory Profiling | pprof heap (Go), tracemalloc (Python), heap snapshot (JS) |
| Slow response, low CPU | Database/network I/O | I/O Profiling | Query logs, pprof block (Go), Django Debug Toolbar |
| Inconsistent latency spikes | GC pauses or I/O wait | CPU + Memory Profiling | Combined profiling to correlate |
| High request rate failures | Connection pool exhaustion | I/O Profiling + Metrics | Database connection metrics, pool monitoring |

**Profiling Workflow:**

```
1. Observe symptoms (metrics, logs, user reports)
2. Hypothesize bottleneck (CPU? Memory? I/O?)
3. Choose profiling type based on hypothesis
4. Run profiler under realistic load
5. Analyze profile (flamegraph, call tree)
6. Identify hot spots (top 20% functions using 80% resources)
7. Optimize identified bottlenecks
8. Re-profile to validate improvement
```

---

### Framework 3: When to Cache vs. Optimize Query?

**Decision Tree:**

```
START: Slow database query

Q1: How often is this data queried?
  ├─ Frequently (>100 req/min) → Consider caching
  └─ Infrequently (<10 req/min) → Optimize query (don't cache)

Q2: How fresh must data be?
  ├─ Real-time (seconds) → Optimize query (caching too stale)
  ├─ Near real-time (1-5 min) → Cache with short TTL
  └─ Eventually consistent (>5 min) → Cache with longer TTL

Q3: How complex is the query?
  ├─ Simple (single table, indexed) → Optimize query (add index)
  ├─ Complex (joins, aggregations) → Cache + optimize
  └─ Very complex (materialized view candidate) → Consider pre-computation

Q4: What's the cache invalidation strategy?
  ├─ Time-based (TTL) → Cache if tolerable staleness
  ├─ Event-based (on update) → Cache if events are trackable
  └─ Complex invalidation → Optimize query instead (cache complexity not worth it)
```

**Caching Strategies:**

| Strategy | Use Case | Pros | Cons |
|----------|----------|------|------|
| **In-Memory (Redis)** | Session data, leaderboards | Very fast (<1ms) | Limited by memory, requires persistence |
| **CDN Caching** | Static assets, API responses | Global distribution, low origin load | Invalidation complexity, costs |
| **Application-Level (LRU)** | Frequently accessed objects | No external dependency | Memory limited, not shared across instances |
| **Database Query Cache** | Repeated identical queries | Transparent, no code changes | Limited effectiveness, invalidation issues |
| **Materialized Views** | Complex aggregations | Pre-computed, fast reads | Stale data, refresh overhead |

---

### Framework 4: Setting Performance SLOs (Service Level Objectives)

**SLO Framework:**

**Key Metrics:**
1. **Latency:** Response time percentiles (p50, p95, p99)
2. **Availability:** Uptime percentage (99%, 99.9%, 99.99%)
3. **Throughput:** Requests per second sustained
4. **Error Rate:** Percentage of failed requests

**Recommended SLOs by Service Type:**

| Service Type | p95 Latency | p99 Latency | Availability | Error Rate |
|--------------|-------------|-------------|--------------|------------|
| **User-Facing API** | < 200ms | < 500ms | 99.9% | < 0.1% |
| **Internal API** | < 100ms | < 300ms | 99.5% | < 0.5% |
| **Database Query** | < 50ms | < 100ms | 99.99% | < 0.01% |
| **Background Job** | < 5s | < 10s | 99% | < 1% |
| **Batch Process** | < 1h | < 2h | 95% | < 5% |
| **Real-time API (Chat)** | < 50ms | < 100ms | 99.95% | < 0.05% |

**Frontend SLOs (Core Web Vitals):**

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP (Largest Contentful Paint)** | < 2.5s | 2.5s - 4s | > 4s |
| **INP (Interaction to Next Paint)** | < 200ms | 200ms - 500ms | > 500ms |
| **CLS (Cumulative Layout Shift)** | < 0.1 | 0.1 - 0.25 | > 0.25 |

**SLO Selection Process:**
1. Start with industry benchmarks (above tables)
2. Measure current performance baseline
3. Set SLOs 10-20% better than baseline (achievable improvement)
4. Iterate as system matures (stricter SLOs over time)
5. Tie SLOs to business metrics (conversion, retention)

---

## Multi-Language Implementations

### TypeScript/JavaScript (PRIMARY)

**Ecosystem Overview:**

**Load Testing:**
- **k6** (Primary, 2025 recommendation)
  - Modern JavaScript-based load testing tool
  - Grafana-backed, cloud-native
  - Built-in HTTP, WebSocket, gRPC support
  - CI/CD friendly (GitHub Actions, GitLab CI)
  - Distributed execution (k6 Cloud)

**Profiling:**
- **Chrome DevTools** (CPU, Memory, Network)
- **clinic.js** (Node.js performance profiling suite)
- **0x** (Flamegraph generator for Node.js)
- **autocannon** (HTTP benchmarking)

**Frontend Performance:**
- **Lighthouse** (Core Web Vitals, performance audits)
- **WebPageTest** (Real-world performance testing)
- **Chrome User Experience Report (CrUX)** (Field data)

---

### Python (PRIMARY)

**Ecosystem Overview:**

**Load Testing:**
- **Locust** (Primary, Python-based)
  - Developer-friendly (tests in Python code)
  - Web UI for monitoring
  - Distributed execution across machines
  - Flexible for complex user scenarios

**Profiling:**
- **py-spy** (Sampling profiler, low overhead)
- **cProfile** (Built-in deterministic profiler)
- **memory_profiler** (Memory usage profiling)
- **Pyroscope** (Continuous profiling, Grafana integration)

**Database Profiling:**
- **Django Debug Toolbar** (Query profiling for Django)
- **SQLAlchemy query logging** (ORM query analysis)

---

### Go (PRIMARY)

**Ecosystem Overview:**

**Load Testing:**
- **k6** (Can be used with Go via xk6 extensions)
- **vegeta** (HTTP load testing library/CLI)
- **hey** (HTTP load generator)

**Profiling:**
- **pprof** (Built-in profiler, industry standard)
  - CPU profiling
  - Heap profiling
  - Block profiling (I/O wait)
  - Goroutine profiling
- **Pyroscope** (Continuous profiling)

**Benchmarking:**
- **testing.B** (Built-in benchmarking framework)

---

## Library Recommendations

### Research Summary

**Research Date:** December 3, 2025
**Libraries Evaluated:** 8+ (load testing, profiling tools)
**Research Tools:** Google Search Grounding (Vertex AI), Context7

---

### Load Testing Libraries (2025)

#### **Primary: k6** (Multi-Language Support via JavaScript)

**Library:** `/grafana/k6-docs`
**Trust Score:** High (Grafana-backed)
**Code Snippets:** 27,079+
**Benchmark Score:** 76.8/100

**Why k6?**
- **Modern Architecture:** Built for cloud-native, microservices era
- **JavaScript DSL:** Familiar syntax for developers (ES6+)
- **Grafana Integration:** Built-in metrics streaming to Grafana, Prometheus
- **CI/CD Native:** Designed for automated testing (exit codes, thresholds)
- **Multi-Protocol:** HTTP/1.1, HTTP/2, WebSocket, gRPC support
- **Distributed Execution:** k6 Cloud for large-scale tests (millions of VUs)
- **Hybrid Testing:** Combine browser (Playwright-like) + protocol tests

**When to Use:**
- Modern API/microservices architectures
- Teams familiar with JavaScript
- Need for CI/CD integration
- Grafana/Prometheus observability stack
- Cross-protocol testing (HTTP + WebSocket)

**Installation:**
```bash
# macOS
brew install k6

# Linux
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

# Windows
choco install k6

# Docker
docker pull grafana/k6
```

**Example (Load Test):**
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

// Test configuration
export const options = {
  stages: [
    { duration: '30s', target: 20 },  // Ramp up to 20 users
    { duration: '1m', target: 20 },   // Stay at 20 users
    { duration: '30s', target: 0 },   // Ramp down to 0
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests < 500ms
    http_req_failed: ['rate<0.01'],    // Error rate < 1%
  },
};

export default function () {
  // Make HTTP request
  const res = http.get('https://api.example.com/products');

  // Validate response
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}
```

**Example (Stress Test with Ramping):**
```javascript
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp to 100 users
    { duration: '5m', target: 100 },   // Stay at 100
    { duration: '2m', target: 200 },   // Ramp to 200
    { duration: '5m', target: 200 },   // Stay at 200
    { duration: '2m', target: 300 },   // Ramp to 300 (stress)
    { duration: '5m', target: 300 },   // Stay at 300
    { duration: '2m', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(99)<1000'],
    http_req_failed: ['rate<0.05'],  // Allow 5% errors under stress
  },
};

export default function () {
  const res = http.post('https://api.example.com/orders', JSON.stringify({
    product_id: 123,
    quantity: 1,
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(res, {
    'order created': (r) => r.status === 201,
  });
}
```

**Example (API Test with Custom Metrics):**
```javascript
import http from 'k6/http';
import { Trend, Rate, Counter } from 'k6/metrics';

// Custom metrics
const loginDuration = new Trend('login_duration');
const loginSuccess = new Rate('login_success');
const loginAttempts = new Counter('login_attempts');

export default function () {
  const payload = JSON.stringify({
    username: 'testuser',
    password: 'testpass',
  });

  const res = http.post('https://api.example.com/login', payload, {
    headers: { 'Content-Type': 'application/json' },
  });

  // Track custom metrics
  loginDuration.add(res.timings.duration);
  loginSuccess.add(res.status === 200);
  loginAttempts.add(1);
}
```

**Running k6 Tests:**
```bash
# Local execution
k6 run script.js

# With custom VUs and duration
k6 run --vus 10 --duration 30s script.js

# Output to Grafana Cloud
k6 run --out cloud script.js

# Output to InfluxDB
k6 run --out influxdb=http://localhost:8086/k6 script.js

# CI/CD mode (exit code 1 if thresholds fail)
k6 run --quiet script.js
```

---

#### **Alternative: Locust** (Python)

**Library:** `/locustio/locust`
**Trust Score:** Medium (Community-driven)
**Code Snippets:** 165+
**Benchmark Score:** 84/100

**Why Locust?**
- **Python-Native:** Write tests in Python (familiar for Python developers)
- **Web UI:** Real-time monitoring dashboard
- **Distributed Architecture:** Scale across multiple machines
- **Flexible Scenarios:** Complex user behavior easy to model
- **CSV Data Loading:** Data-driven testing from CSV files
- **REST API:** Programmatic control of tests

**When to Use:**
- Python-heavy teams
- Complex user scenarios (state machines, multi-step workflows)
- Need for web UI monitoring
- Custom protocol testing (not just HTTP)

**Installation:**
```bash
pip install locust
```

**Example (Load Test):**
```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    host = "https://api.example.com"

    def on_start(self):
        # Login once when user starts
        self.client.post("/login", json={
            "username": "testuser",
            "password": "testpass"
        })

    @task(3)  # Weight: 3x more likely than other tasks
    def view_products(self):
        self.client.get("/products")

    @task(1)
    def view_product_detail(self):
        self.client.get("/products/123")

    @task(1)
    def add_to_cart(self):
        self.client.post("/cart", json={
            "product_id": 123,
            "quantity": 1
        })
```

**Example (REST API Testing with Validation):**
```python
from locust import FastHttpUser, task

class ApiUser(FastHttpUser):
    host = "https://api.example.com"

    @task
    def test_api(self):
        # GET request with JSON validation
        with self.rest("GET", "/users/1") as resp:
            if resp.js["id"] != 1:
                resp.failure(f"Unexpected user ID: {resp.text}")

        # POST with assertion-based validation
        with self.rest("POST", "/users", json={"name": "Test User"}) as resp:
            assert resp.js["name"] == "Test User", "Name mismatch"
            assert "id" in resp.js, "Missing ID in response"
```

**Example (Data-Driven Testing with CSV):**
```python
from locust import HttpUser, task
import csv
import os

csvfile = open(os.path.join(os.path.dirname(__file__), "users.csv"))
users_iter = csv.reader(csvfile)

class DataDrivenUser(HttpUser):
    host = "https://api.example.com"

    @task
    def login_with_csv_data(self):
        try:
            username, password = next(users_iter)
        except StopIteration:
            csvfile.seek(0)  # Reset to start
            username, password = next(users_iter)

        with self.rest("POST", "/login", json={
            "username": username,
            "password": password
        }) as resp:
            if "token" not in resp.js:
                resp.failure("Login failed")
```

**Running Locust Tests:**
```bash
# Web UI mode (http://localhost:8089)
locust -f locustfile.py

# Headless mode (no UI)
locust -f locustfile.py --headless -u 100 -r 10 --run-time 10m

# Distributed execution (master + workers)
# Master
locust -f locustfile.py --master

# Workers (on same or different machines)
locust -f locustfile.py --worker --master-host=<master-ip>
```

---

### Profiling Tools

#### **Python Profiling**

**Primary: py-spy** (Sampling Profiler)

**Why py-spy?**
- **Low Overhead:** Sampling profiler (doesn't slow down app significantly)
- **No Code Changes:** Attach to running process
- **Production-Safe:** Designed for profiling production workloads
- **Flamegraph Output:** Visual representation of CPU usage

**Installation:**
```bash
pip install py-spy
```

**Usage:**
```bash
# Profile running process
py-spy record -o profile.svg --pid <PID>

# Top-like view of functions
py-spy top --pid <PID>

# Profile command
py-spy record -o profile.svg -- python app.py

# Flamegraph output (open in browser)
py-spy record -o profile.svg --format speedscope --pid <PID>
```

**Alternative: cProfile** (Deterministic Profiler)

```python
import cProfile
import pstats

# Profile function
profiler = cProfile.Profile()
profiler.enable()

# Code to profile
my_function()

profiler.disable()

# Print stats
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions
```

**Memory Profiling: memory_profiler**

```bash
pip install memory-profiler
```

```python
from memory_profiler import profile

@profile
def my_function():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a

# Run with: python -m memory_profiler script.py
```

---

#### **Go Profiling**

**Primary: pprof** (Built-in)

**Why pprof?**
- **Built-in:** Part of Go standard library
- **Comprehensive:** CPU, heap, goroutine, block profiling
- **Production-Ready:** Low overhead, safe in production
- **Excellent Visualization:** Flamegraphs, call graphs

**Usage (HTTP Server):**
```go
import (
    "net/http"
    _ "net/http/pprof"
)

func main() {
    // Start pprof HTTP server
    go func() {
        http.ListenAndServe("localhost:6060", nil)
    }()

    // Your application code
    startApp()
}
```

**Profiling Commands:**
```bash
# CPU profile (30 seconds)
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# Heap profile
go tool pprof http://localhost:6060/debug/pprof/heap

# Goroutine profile
go tool pprof http://localhost:6060/debug/pprof/goroutine

# Block profile (I/O wait)
go tool pprof http://localhost:6060/debug/pprof/block

# Interactive analysis
(pprof) top
(pprof) list functionName
(pprof) web  # Open flamegraph in browser
```

**Programmatic Profiling:**
```go
import (
    "os"
    "runtime/pprof"
)

func profileCPU() {
    f, _ := os.Create("cpu.prof")
    defer f.Close()

    pprof.StartCPUProfile(f)
    defer pprof.StopCPUProfile()

    // Code to profile
    doWork()
}

func profileHeap() {
    f, _ := os.Create("heap.prof")
    defer f.Close()

    pprof.WriteHeapProfile(f)
}
```

---

#### **TypeScript/JavaScript Profiling**

**Primary: Chrome DevTools** (Browser/Node.js)

**Why Chrome DevTools?**
- **Comprehensive:** CPU, memory, network profiling
- **Visual:** Flamegraphs, timeline view
- **Browser Native:** Built into Chrome
- **Node.js Support:** Can profile Node.js apps

**Usage (Browser):**
1. Open Chrome DevTools (F12)
2. Performance tab → Record
3. Perform actions
4. Stop recording
5. Analyze flamegraph

**Usage (Node.js):**
```bash
# Start Node with inspector
node --inspect app.js

# Open chrome://inspect in Chrome
# Click "Open dedicated DevTools for Node"
# Go to Performance/Memory tab
```

**Alternative: clinic.js** (Node.js Performance Suite)

```bash
npm install -g clinic
```

```bash
# CPU profiling
clinic doctor -- node app.js

# Flamegraph
clinic flame -- node app.js

# Bubble profiling (async operations)
clinic bubbleprof -- node app.js
```

**Alternative: 0x** (Flamegraph Generator)

```bash
npm install -g 0x
```

```bash
# Generate flamegraph
0x app.js

# Output: Interactive HTML flamegraph
```

---

### Frontend Performance Tools

#### **Lighthouse** (Core Web Vitals Auditing)

**Why Lighthouse?**
- **Comprehensive Audits:** Performance, accessibility, SEO, PWA
- **Core Web Vitals:** LCP, INP, CLS measurement
- **Actionable Recommendations:** Specific optimization suggestions
- **CI/CD Integration:** Automated performance budgets

**Usage:**
```bash
# CLI
npm install -g lighthouse
lighthouse https://example.com --view

# CI/CD (with budgets)
lighthouse https://example.com --budget-path=./budget.json --preset=desktop

# Chrome DevTools: Lighthouse tab
```

**Budget Example (budget.json):**
```json
[
  {
    "path": "/*",
    "resourceSizes": [
      { "resourceType": "script", "budget": 300 },
      { "resourceType": "image", "budget": 500 },
      { "resourceType": "total", "budget": 1000 }
    ],
    "resourceCounts": [
      { "resourceType": "third-party", "budget": 10 }
    ]
  }
]
```

---

#### **WebPageTest** (Real-World Performance Testing)

**Why WebPageTest?**
- **Real Devices:** Test on actual devices and networks
- **Global Testing:** Locations worldwide
- **Filmstrip View:** Visual progression of page load
- **Waterfall Charts:** Detailed resource loading timeline

**Usage:**
```bash
# Web UI: https://www.webpagetest.org/

# API (for automation)
curl "https://www.webpagetest.org/runtest.php?url=https://example.com&k=API_KEY&f=json"
```

---

### Benchmarking Tools

#### **TypeScript/JavaScript: autocannon**

```bash
npm install -g autocannon
```

```bash
# Benchmark HTTP endpoint
autocannon -c 100 -d 30 http://localhost:3000/api/products

# Output: Requests/sec, latency percentiles
```

#### **Go: Built-in Benchmarking**

```go
func BenchmarkCalculate(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Calculate(100)
    }
}

// Run: go test -bench=. -benchmem
```

#### **Python: pytest-benchmark**

```bash
pip install pytest-benchmark
```

```python
def test_my_function(benchmark):
    result = benchmark(my_function, arg1, arg2)
    assert result == expected
```

---

## Skill Structure Design

### Skill File Organization

**Proposed Structure:**

```
performance-engineering/
├── SKILL.md                          # Main skill file (<500 lines)
├── references/
│   ├── testing-types.md              # Load, stress, soak, spike testing
│   ├── profiling-guide.md            # CPU, memory, I/O profiling
│   ├── optimization-strategies.md    # Caching, query optimization, API patterns
│   ├── frontend-performance.md       # Core Web Vitals, bundle optimization
│   ├── slo-framework.md              # Setting SLOs, performance budgets
│   └── benchmarking.md               # Benchmarking best practices
├── examples/
│   ├── k6/
│   │   ├── load-test.js              # Basic load test
│   │   ├── stress-test.js            # Stress test with ramping
│   │   ├── soak-test.js              # Long-duration soak test
│   │   └── api-test.js               # API testing with custom metrics
│   ├── locust/
│   │   ├── load_test.py              # Basic load test
│   │   ├── api_test.py               # REST API testing
│   │   └── data_driven.py            # CSV data-driven testing
│   ├── profiling/
│   │   ├── python/
│   │   │   ├── pyspy_example.sh      # py-spy profiling
│   │   │   ├── cprofile_example.py   # cProfile usage
│   │   │   └── memory_profile.py     # Memory profiling
│   │   ├── go/
│   │   │   ├── pprof_example.go      # pprof integration
│   │   │   └── benchmark_test.go     # Go benchmarking
│   │   └── typescript/
│   │       ├── devtools_profiling.md # Chrome DevTools guide
│   │       └── clinic_example.sh     # clinic.js usage
│   └── optimization/
│       ├── caching_patterns.md       # Redis, CDN, application caching
│       ├── query_optimization.sql    # SQL optimization examples
│       └── api_optimization.ts       # API pagination, batching
└── scripts/
    ├── run-load-test.sh              # Wrapper for k6/Locust execution
    └── analyze-profile.sh            # Profile analysis automation
```

---

### SKILL.md Structure (Main File)

**Sections (Target: ~400-450 lines):**

1. **Frontmatter** (YAML)
   - name, description

2. **Purpose** (2-3 paragraphs)
   - What this skill teaches
   - When to use this skill

3. **Performance Testing Overview** (~100 lines)
   - Load, stress, soak, spike testing explained
   - Quick decision tree: Which test type to use
   - SLO framework introduction

4. **Load Testing Quick Starts** (~150 lines)
   - k6 (JavaScript): Basic load test example
   - Locust (Python): Basic load test example
   - Running tests and interpreting results

5. **Profiling Quick Starts** (~100 lines)
   - Python: py-spy, cProfile
   - Go: pprof
   - TypeScript: Chrome DevTools, clinic.js
   - When to use CPU vs. Memory vs. I/O profiling

6. **Optimization Strategies** (~80 lines)
   - Caching strategies (when to cache)
   - Database query optimization (indexes, N+1)
   - API performance patterns (pagination, batching)
   - Frontend performance (Core Web Vitals)

7. **Reference Links** (~20 lines)
   - Links to detailed references/ files
   - Links to examples/ files

---

### Progressive Disclosure Strategy

**Main SKILL.md Contains:**
- High-level decision frameworks (which test type, which profiling approach)
- Quick-start examples (minimal working code)
- When to use each tool/technique
- Links to detailed references

**References/ Contains:**
- Detailed testing methodologies (references/testing-types.md)
- Comprehensive profiling guide (references/profiling-guide.md)
- In-depth optimization strategies (references/optimization-strategies.md)
- Frontend performance deep dive (references/frontend-performance.md)

**Examples/ Contains:**
- Working code examples (copy-paste ready)
- Organized by tool (k6, Locust, profilers)
- Real-world scenarios with comments

**Scripts/ Contains:**
- Automation wrappers for running tests
- Profile analysis helpers

---

## Integration Points

### Integration with Existing Skills

#### 1. **testing-strategies** Skill

**Integration:** Performance testing complements functional testing

- **Functional Tests:** Validate correctness (does it work?)
- **Performance Tests:** Validate scalability (does it work under load?)

**Example Integration:**
```javascript
// testing-strategies: Functional test (Vitest)
test('API returns products', async () => {
  const response = await fetch('/api/products')
  expect(response.status).toBe(200)
})

// performance-engineering: Load test (k6)
export default function() {
  const res = http.get('https://api.example.com/products')
  check(res, { 'status is 200': (r) => r.status === 200 })
}
```

**Workflow:**
1. Write functional tests (testing-strategies)
2. Validate correctness
3. Add load tests (performance-engineering)
4. Validate scalability

---

#### 2. **building-ci-pipelines** Skill

**Integration:** Performance tests in CI/CD

**Example CI/CD Pipeline (.github/workflows/performance.yml):**
```yaml
name: Performance Tests

on:
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Nightly

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

      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: load-test-results
          path: results.json
```

**Performance Regression Detection:**
```javascript
// k6 test with thresholds (fail build if violated)
export const options = {
  thresholds: {
    http_req_duration: ['p(95)<500'],  // Fail if p95 > 500ms
    http_req_failed: ['rate<0.01'],    // Fail if error rate > 1%
  },
};
```

---

#### 3. **infrastructure-as-code** Skill

**Integration:** Performance testing informs infrastructure sizing

**Example Workflow:**
1. Run stress test to find capacity limits
2. Use results to size infrastructure (Terraform/CloudFormation)
3. Configure auto-scaling based on load test findings

**Example (Terraform Auto-Scaling based on Load Test Results):**
```hcl
# After stress test shows CPU spikes at 300 req/s:
resource "aws_autoscaling_policy" "scale_up" {
  name                   = "scale-up"
  scaling_adjustment     = 2
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.app.name
}

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "cpu-utilization-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 60
  statistic           = "Average"
  threshold           = 70  # Based on load test findings

  alarm_actions = [aws_autoscaling_policy.scale_up.arn]
}
```

---

#### 4. **kubernetes-operations** Skill

**Integration:** Performance testing for Kubernetes deployments

**Example (Load Test Kubernetes Service):**
```javascript
// k6 test targeting Kubernetes service
import http from 'k6/http';

export const options = {
  stages: [
    { duration: '5m', target: 100 },
    { duration: '10m', target: 100 },
    { duration: '5m', target: 0 },
  ],
};

export default function() {
  // Test via LoadBalancer or Ingress
  http.get('http://app.example.com/api/health');
}
```

**HPA Configuration based on Load Test:**
```yaml
# After load test shows 200 req/s per pod capacity:
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70  # Based on profiling results
```

---

#### 5. **secret-management** Skill

**Integration:** Load test authentication/authorization flows

**Example (Load Test with API Keys):**
```javascript
// k6 test with secret rotation simulation
import http from 'k6/http';

const API_KEYS = [
  __ENV.API_KEY_1,
  __ENV.API_KEY_2,
  __ENV.API_KEY_3,
];

export default function() {
  const apiKey = API_KEYS[Math.floor(Math.random() * API_KEYS.length)];

  http.get('https://api.example.com/data', {
    headers: { 'Authorization': `Bearer ${apiKey}` },
  });
}
```

---

### Integration with CI/CD Workflows

**Key Patterns:**

1. **Fast Feedback Loop:**
   - Run smoke load test on every PR (< 2 minutes, 10 VUs)
   - Run full load test nightly
   - Run stress test weekly

2. **Performance Budgets:**
   - Define acceptable latency percentiles
   - Fail build if thresholds violated
   - Track trends over time (e.g., Grafana dashboards)

3. **Profiling on Demand:**
   - Manual trigger for profiling (GitHub Actions workflow_dispatch)
   - Automated profiling on performance regression detection
   - Store profiles as artifacts for analysis

4. **Result Artifacts:**
   - Upload k6/Locust results as artifacts
   - Store flamegraphs from profiling
   - Track performance trends in database

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)

**Deliverables:**
- [x] Complete init.md (this document)
- [ ] Create SKILL.md main file
- [ ] Write references/testing-types.md
- [ ] Write references/profiling-guide.md

**Content Focus:**
- Performance testing types (load, stress, soak, spike)
- Profiling fundamentals (CPU, memory, I/O)
- Decision frameworks

---

### Phase 2: Load Testing (Week 2)

**Deliverables:**
- [ ] k6 examples (load, stress, soak, spike)
- [ ] Locust examples (basic, REST API, data-driven)
- [ ] Write references/slo-framework.md

**Files:**
- examples/k6/load-test.js
- examples/k6/stress-test.js
- examples/k6/soak-test.js
- examples/locust/load_test.py
- examples/locust/api_test.py

---

### Phase 3: Profiling (Week 3)

**Deliverables:**
- [ ] Python profiling examples (py-spy, cProfile, memory)
- [ ] Go profiling examples (pprof)
- [ ] TypeScript profiling examples (DevTools, clinic.js)

**Files:**
- examples/profiling/python/pyspy_example.sh
- examples/profiling/python/cprofile_example.py
- examples/profiling/go/pprof_example.go
- examples/profiling/typescript/devtools_profiling.md

---

### Phase 4: Optimization (Week 4)

**Deliverables:**
- [ ] Write references/optimization-strategies.md
- [ ] Write references/frontend-performance.md
- [ ] Caching patterns examples
- [ ] Database query optimization examples

**Files:**
- examples/optimization/caching_patterns.md
- examples/optimization/query_optimization.sql
- examples/optimization/api_optimization.ts

---

### Phase 5: Integration & Polish (Week 5)

**Deliverables:**
- [ ] CI/CD integration examples
- [ ] Create scripts/run-load-test.sh
- [ ] Create scripts/analyze-profile.sh
- [ ] Cross-link with related skills

---

## Validation Checklist

### Before Creating SKILL.md

- [x] Research complete (Google Search + Context7)
- [x] Library recommendations validated (trust scores, code snippets)
- [x] Decision frameworks designed
- [x] Multi-language patterns identified
- [x] Integration points with other skills mapped

### Before Finalizing Skill

- [ ] SKILL.md under 500 lines
- [ ] All references/ files created
- [ ] All examples/ files working and tested
- [ ] Progressive disclosure effective (main → references → examples)
- [ ] Tested with real projects
- [ ] Cross-language consistency validated
- [ ] Integration with related skills verified

---

## Success Metrics

**This skill is successful if developers can:**

1. **Design Performance Tests:**
   - Choose correct test type (load vs. stress vs. soak)
   - Create realistic test scenarios
   - Set meaningful SLOs

2. **Execute Load Tests:**
   - Run k6/Locust tests successfully
   - Interpret results (latency percentiles, throughput)
   - Identify capacity limits

3. **Profile Applications:**
   - Use appropriate profiler (CPU, memory, I/O)
   - Read flamegraphs and identify hot spots
   - Correlate profiling data with performance issues

4. **Optimize Performance:**
   - Implement caching strategies effectively
   - Optimize database queries (indexes, N+1 prevention)
   - Improve API performance (pagination, batching)
   - Optimize frontend Core Web Vitals

5. **Integrate with Workflow:**
   - Add load tests to CI/CD pipelines
   - Track performance trends over time
   - Set up automated regression detection

---

## Future Enhancements

**Potential Additions (Not in Initial Release):**

1. **Advanced Load Testing Patterns**
   - Multi-region distributed testing
   - Production traffic replay (shadowing)
   - Chaos engineering integration

2. **Advanced Profiling**
   - Continuous profiling (Pyroscope, Grafana)
   - Production profiling best practices
   - Distributed tracing correlation

3. **Cost Optimization**
   - Cloud cost profiling (FinOps)
   - Right-sizing recommendations
   - Cost per request tracking

4. **Database Performance Deep Dive**
   - Query plan analysis
   - Index optimization strategies
   - Connection pool tuning

5. **Frontend Performance Advanced**
   - Web Worker optimization
   - Service Worker caching strategies
   - Progressive Web App (PWA) performance

---

## Appendix: Tool Comparison Matrix

### Load Testing Tools

| Tool | Language | Protocols | Distributed | UI | CI/CD Integration | Best For |
|------|----------|-----------|-------------|----|--------------------|----------|
| **k6** | JavaScript | HTTP/1.1, HTTP/2, WebSocket, gRPC | ✅ (k6 Cloud) | CLI + Grafana | ⭐⭐⭐⭐⭐ | Modern APIs, microservices, CI/CD |
| **Locust** | Python | HTTP (extensible) | ✅ (built-in) | Web UI | ⭐⭐⭐⭐ | Python teams, complex scenarios |
| **JMeter** | Java | HTTP, SOAP, FTP, JDBC | ✅ | GUI + CLI | ⭐⭐⭐ | Enterprise, legacy systems |
| **Gatling** | Scala | HTTP, WebSocket | ✅ | HTML reports | ⭐⭐⭐⭐ | JVM teams, high performance |

---

### Profiling Tools

| Tool | Language | Profile Types | Overhead | Production-Safe | Visualization |
|------|----------|---------------|----------|-----------------|---------------|
| **pprof** | Go | CPU, heap, goroutine, block | Low | ✅ | Flamegraph, call graph |
| **py-spy** | Python | CPU | Very Low | ✅ | Flamegraph, speedscope |
| **cProfile** | Python | CPU (deterministic) | Medium | ⚠️ | Stats, SnakeViz |
| **Chrome DevTools** | JS/Node | CPU, heap, network | Low | ✅ (Node) | Timeline, flamegraph |
| **clinic.js** | Node.js | CPU, async, event loop | Low | ✅ | Interactive HTML |

---

## References

**Research Sources:**
- Google Search Grounding (Vertex AI): Performance engineering best practices 2025
- Context7 Documentation: k6, Locust
- Official Documentation: k6.io, locust.io, pprof, py-spy
- Industry Best Practices: Load testing, profiling, optimization patterns

**Related Skills:**
- `testing-strategies` - Functional testing (complements performance testing)
- `building-ci-pipelines` - CI/CD integration for performance tests
- `infrastructure-as-code` - Infrastructure sizing based on load tests
- `kubernetes-operations` - K8s performance testing and HPA configuration
- `secret-management` - Load testing auth flows

---

**Document Status:** ✅ Complete
**Next Step:** Create SKILL.md from this master plan
**Owner:** AI Design Components Project
**Last Updated:** December 3, 2025
