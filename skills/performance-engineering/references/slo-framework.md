# Performance SLO Framework

## Table of Contents

1. [SLO Fundamentals](#slo-fundamentals)
2. [Key Metrics](#key-metrics)
3. [Setting SLOs](#setting-slos)
4. [Performance Budgets](#performance-budgets)
5. [Tracking and Alerting](#tracking-and-alerting)
6. [SLO Examples by Service Type](#slo-examples-by-service-type)

---

## SLO Fundamentals

### Definitions

**SLI (Service Level Indicator):** Quantitative measure of service performance.
- Examples: Response time (p95 latency), error rate, availability

**SLO (Service Level Objective):** Target value for SLI.
- Example: "p95 latency < 200ms" or "99.9% availability"

**SLA (Service Level Agreement):** Customer-facing commitment with consequences.
- Example: "99.99% uptime or customer gets refund"

**Relationship:**
```
SLI (what we measure) → SLO (internal target) → SLA (customer commitment)

Example:
SLI: p95 latency = 150ms
SLO: p95 latency < 200ms (internal goal)
SLA: p95 latency < 500ms (customer agreement)
```

### Why SLOs Matter

**Benefits:**
1. **Objective Performance Targets:** No guessing, clear goals
2. **Regression Detection:** Automated alerts when SLOs violated
3. **Capacity Planning:** Know when to scale infrastructure
4. **Prioritization:** Focus optimization efforts on SLO violations
5. **Customer Expectations:** Align internal goals with user needs

**Without SLOs:**
- "The app feels slow" (subjective)
- No objective way to detect regressions
- Optimization efforts scattered

**With SLOs:**
- "p95 latency is 300ms, target is 200ms" (objective)
- Automated alerts when threshold exceeded
- Clear prioritization (fix SLO violations first)

---

## Key Metrics

### Latency (Response Time)

**Why percentiles, not averages?**

Average hides outliers:
```
10 requests: 9 × 50ms + 1 × 5000ms
Average: 545ms (misleading, most users see 50ms)
p95: 50ms (accurate for 95% of users)
p99: 5000ms (shows outlier issue)
```

**Percentile definitions:**
- **p50 (median):** 50% of requests faster, 50% slower
- **p95:** 95% of requests faster (only 5% slower)
- **p99:** 99% of requests faster (only 1% slower)
- **p99.9:** 99.9% of requests faster (only 0.1% slower)

**Which percentile to use?**
- **p50:** Typical user experience (median)
- **p95:** Good target for SLOs (balance performance and reliability)
- **p99:** Stricter target for critical services
- **p99.9:** Very strict (expensive to achieve)

**Recommended SLO:** p95 or p99 (not average).

### Availability

**Definition:** Percentage of time service is operational.

**Availability levels:**
- **99%:** 3.65 days downtime/year (not acceptable for most services)
- **99.9%:** 8.76 hours downtime/year
- **99.99%:** 52.56 minutes downtime/year
- **99.999%:** 5.26 minutes downtime/year (very expensive)

**Calculation:**
```
Availability = (Uptime / Total Time) × 100

Example:
Total Time: 30 days = 43,200 minutes
Downtime: 4 hours = 240 minutes
Uptime: 43,200 - 240 = 42,960 minutes
Availability: (42,960 / 43,200) × 100 = 99.44%
```

**Error Budget:**
```
Error Budget = 100% - Availability SLO

Example:
SLO: 99.9% availability
Error Budget: 0.1% (8.76 hours/year)

If you're down 4 hours so far this year:
Remaining Error Budget: 4.76 hours
```

### Throughput

**Definition:** Requests per second (RPS) system can handle.

**Why it matters:**
- Capacity planning (how many servers needed?)
- Load balancing (distribute traffic evenly)
- Auto-scaling triggers (scale at 80% capacity)

**Example SLO:**
```
Target Throughput: 1,000 RPS sustained
Max Burst: 2,000 RPS for 5 minutes
```

### Error Rate

**Definition:** Percentage of failed requests.

**Types of errors:**
- HTTP 5xx (server errors)
- Timeouts (slow responses)
- Connection failures

**Calculation:**
```
Error Rate = (Failed Requests / Total Requests) × 100

Example:
Total Requests: 10,000
Failed Requests: 5
Error Rate: 0.05%
```

**Recommended SLO:**
- **User-facing APIs:** < 0.1% error rate
- **Internal APIs:** < 0.5% error rate
- **Background jobs:** < 1% error rate

---

## Setting SLOs

### SLO Selection Process

**Step 1: Measure Baseline**
Run load tests or analyze production metrics.

```
Current Performance:
- p50: 50ms
- p95: 150ms
- p99: 300ms
- Availability: 99.5%
- Error Rate: 0.05%
```

**Step 2: Identify User Expectations**
What do users tolerate?

```
User Research:
- Users abandon after 3s load time
- Users tolerate 200ms button click latency
- Users expect app always available (99.9%+)
```

**Step 3: Set Achievable Targets**
10-20% better than baseline, aligned with user expectations.

```
SLOs:
- p95 latency: < 200ms (current: 150ms, room for growth)
- Availability: 99.9% (current: 99.5%, achievable improvement)
- Error Rate: < 0.1% (current: 0.05%, buffer for spikes)
```

**Step 4: Iterate**
Start conservative, tighten over time.

```
Quarter 1: p95 < 300ms (achievable)
Quarter 2: p95 < 250ms (improvement)
Quarter 3: p95 < 200ms (target)
```

### SLO Hierarchy

**Tiered SLOs:**
```
Tier 1 (Critical Path - Strictest):
  - Login endpoint: p95 < 100ms
  - Checkout API: p99 < 200ms, 99.99% availability

Tier 2 (Important - Moderate):
  - Product search: p95 < 200ms
  - User profile: p95 < 300ms

Tier 3 (Background - Lenient):
  - Analytics processing: p95 < 5s
  - Report generation: p95 < 30s
```

---

## Performance Budgets

### Frontend Performance Budgets

**Definition:** Maximum resource sizes for acceptable performance.

**Example Budget:**
```json
{
  "resourceSizes": {
    "javascript": 300,   // 300 KB max JavaScript
    "css": 100,          // 100 KB max CSS
    "images": 500,       // 500 KB max images
    "fonts": 100,        // 100 KB max fonts
    "total": 1000        // 1 MB max total
  },
  "resourceCounts": {
    "thirdParty": 10,    // Max 10 third-party scripts
    "requests": 50       // Max 50 HTTP requests
  },
  "metrics": {
    "LCP": 2500,         // 2.5s max Largest Contentful Paint
    "FID": 100,          // 100ms max First Input Delay
    "CLS": 0.1           // 0.1 max Cumulative Layout Shift
  }
}
```

**Enforcement (Lighthouse CI):**
```yaml
# .lighthouserc.json
{
  "ci": {
    "assert": {
      "assertions": {
        "first-contentful-paint": ["error", {"maxNumericValue": 2000}],
        "largest-contentful-paint": ["error", {"maxNumericValue": 2500}],
        "cumulative-layout-shift": ["error", {"maxNumericValue": 0.1}],
        "total-byte-weight": ["error", {"maxNumericValue": 1000000}]
      }
    }
  }
}
```

### Backend Performance Budgets

**Example Budget:**
```yaml
endpoints:
  - path: /api/users
    budgets:
      p95_latency_ms: 100
      p99_latency_ms: 200
      error_rate_percent: 0.1

  - path: /api/products/search
    budgets:
      p95_latency_ms: 200
      p99_latency_ms: 500
      error_rate_percent: 0.5
```

**Enforcement (k6 thresholds):**
```javascript
export const options = {
  thresholds: {
    'http_req_duration{endpoint:/api/users}': ['p(95)<100', 'p(99)<200'],
    'http_req_failed{endpoint:/api/users}': ['rate<0.001'],
  },
};
```

---

## Tracking and Alerting

### Metrics Collection

**Tools:**
- **Prometheus:** Time-series metrics (latency, error rate, throughput)
- **Grafana:** Visualization dashboards
- **Datadog/New Relic:** Commercial APM solutions

**Example (Prometheus Metrics):**
```python
# Python (prometheus_client)
from prometheus_client import Histogram, Counter

REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')
REQUEST_ERRORS = Counter('http_request_errors_total', 'HTTP request errors')

@REQUEST_LATENCY.time()
def handle_request():
    try:
        # Handle request
        pass
    except Exception:
        REQUEST_ERRORS.inc()
        raise
```

```go
// Go (prometheus client)
import "github.com/prometheus/client_golang/prometheus"

var (
    requestLatency = prometheus.NewHistogram(prometheus.HistogramOpts{
        Name: "http_request_duration_seconds",
        Help: "HTTP request latency",
    })
)

func handleRequest(w http.ResponseWriter, r *http.Request) {
    timer := prometheus.NewTimer(requestLatency)
    defer timer.ObserveDuration()

    // Handle request
}
```

### Alerting Rules

**Prometheus AlertManager:**
```yaml
groups:
  - name: slo_alerts
    rules:
      - alert: HighLatency
        expr: histogram_quantile(0.95, http_request_duration_seconds) > 0.2
        for: 5m
        annotations:
          summary: "p95 latency > 200ms for 5 minutes"

      - alert: HighErrorRate
        expr: rate(http_request_errors_total[5m]) > 0.01
        for: 5m
        annotations:
          summary: "Error rate > 1% for 5 minutes"

      - alert: LowAvailability
        expr: up == 0
        for: 1m
        annotations:
          summary: "Service down for 1 minute"
```

### Dashboards

**Grafana Dashboard (Key Metrics):**
```
┌─────────────────────────────────────────────────┐
│ Latency (p50, p95, p99)                         │
│ ────────────────────────────────────────        │
│ [Line graph showing latency over time]          │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Throughput (RPS)                                │
│ ────────────────────────────────────────────    │
│ [Line graph showing requests/sec over time]     │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Error Rate (%)                                  │
│ ────────────────────────────────────────────    │
│ [Line graph showing error percentage]           │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ SLO Compliance (%)                              │
│ ────────────────────────────────────────────    │
│ Current: 99.95%                                 │
│ Target:  99.90%                                 │
│ Status:  ✅ MEETING SLO                         │
└─────────────────────────────────────────────────┘
```

---

## SLO Examples by Service Type

### User-Facing API

```yaml
service: api.example.com/v1/products

slos:
  latency:
    p95: 200ms
    p99: 500ms
  availability: 99.9%
  error_rate: 0.1%
  throughput: 1000 RPS sustained

rationale:
  - User-facing requires fast response (< 200ms perceived as instant)
  - 99.9% availability = 8.76 hours downtime/year (acceptable)
  - Error rate < 0.1% = 1 in 1000 requests fail (good UX)
```

### Internal API

```yaml
service: internal-api.example.com/v1/users

slos:
  latency:
    p95: 100ms
    p99: 300ms
  availability: 99.5%
  error_rate: 0.5%
  throughput: 500 RPS sustained

rationale:
  - Internal API can be stricter on latency (controlled clients)
  - Lower availability acceptable (not customer-facing)
  - Higher error rate tolerable (retry logic in clients)
```

### Database Query

```yaml
service: postgres-primary.example.com

slos:
  latency:
    p95: 50ms
    p99: 100ms
  availability: 99.99%
  error_rate: 0.01%

rationale:
  - Database queries should be very fast (indexed)
  - High availability critical (single point of failure)
  - Very low error rate (data consistency)
```

### Background Job

```yaml
service: email-worker.example.com

slos:
  latency:
    p95: 5s
    p99: 10s
  availability: 99%
  error_rate: 1%
  throughput: 100 jobs/min

rationale:
  - Background jobs not latency-sensitive (async)
  - Lower availability acceptable (retries built-in)
  - Higher error rate OK (jobs retry automatically)
```

### Real-time API (Chat/WebSocket)

```yaml
service: chat.example.com

slos:
  latency:
    p95: 50ms
    p99: 100ms
  availability: 99.95%
  error_rate: 0.05%
  throughput: 10,000 concurrent connections

rationale:
  - Real-time requires very low latency (< 100ms perceived as instant)
  - High availability critical (real-time communication)
  - Very low error rate (dropped messages hurt UX)
```

---

## SLO Best Practices

### Start Simple

**Phase 1:** Basic SLOs
- p95 latency
- Availability
- Error rate

**Phase 2:** Advanced SLOs
- p99, p99.9 latency
- Per-endpoint SLOs
- Customer-facing SLAs

### Review and Adjust

**Monthly Review:**
- Are we consistently meeting SLOs? (too easy, tighten)
- Are we consistently missing SLOs? (too strict, relax)
- Have user expectations changed?

**Quarterly Adjustment:**
```
Q1: p95 < 300ms (baseline)
Q2: p95 < 250ms (improvement observed, tighten)
Q3: p95 < 200ms (target)
Q4: p95 < 200ms (maintain, focus on p99)
```

### Tie SLOs to Business Metrics

**Example:**
```
Performance Impact on Conversion:
- p95 latency < 200ms → 5% conversion rate
- p95 latency 200-500ms → 4% conversion rate
- p95 latency > 500ms → 2% conversion rate

Business Value: 100ms improvement = 1% conversion increase = $500K revenue/year

Priority: High (optimize to < 200ms)
```

---

## SLO Checklist

### Defining SLOs
- [ ] Measure baseline performance (load tests or production metrics)
- [ ] Identify user expectations (user research, industry benchmarks)
- [ ] Set achievable targets (10-20% better than baseline)
- [ ] Define key metrics (latency, availability, error rate, throughput)
- [ ] Prioritize endpoints (critical path stricter than background)

### Tracking SLOs
- [ ] Collect metrics (Prometheus, Datadog, New Relic)
- [ ] Build dashboards (Grafana, DataDog)
- [ ] Set up alerts (violated SLOs)
- [ ] Review weekly (SLO compliance)
- [ ] Adjust quarterly (tighten or relax based on performance)

### Enforcing SLOs
- [ ] Performance budgets (frontend: Lighthouse CI, backend: k6 thresholds)
- [ ] CI/CD gates (fail build if SLO violated)
- [ ] Automated alerts (Slack, PagerDuty)
- [ ] Incident response (SLO violation = incident)
- [ ] Post-mortem (analyze root cause, prevent recurrence)
