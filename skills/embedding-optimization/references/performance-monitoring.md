# Performance Monitoring for Embedding Pipelines

Comprehensive guide to monitoring embedding generation performance, tracking costs, and optimizing throughput.

## Table of Contents

1. [Key Metrics](#key-metrics)
2. [Monitoring Architecture](#monitoring-architecture)
3. [Latency Tracking](#latency-tracking)
4. [Cost Tracking](#cost-tracking)
5. [Cache Performance](#cache-performance)
6. [Alerting and Thresholds](#alerting-and-thresholds)

## Key Metrics

### Critical Metrics (Monitor Always)

**1. Latency**
- **Definition:** Time to generate embeddings for a single text or batch
- **Unit:** Milliseconds (ms)
- **Target:** <100ms for single, <500ms for batch (API); <50ms for local
- **Measurement:**
  ```python
  start = time.time()
  embedding = embedder.embed_single(text)
  latency_ms = (time.time() - start) * 1000
  ```

**2. Throughput**
- **Definition:** Number of texts embedded per unit time
- **Unit:** Texts per second (texts/sec) or per minute (texts/min)
- **Target:** 1,000+ texts/min (API), 5,000+ texts/min (local GPU)
- **Measurement:**
  ```python
  start = time.time()
  embeddings = embedder.embed_batch(texts)
  elapsed = time.time() - start
  throughput = len(texts) / elapsed  # texts/sec
  ```

**3. Cost**
- **Definition:** Total API spending on embeddings
- **Unit:** USD per 1K/1M tokens
- **Target:** Varies by budget; track against baseline
- **Measurement:**
  ```python
  tokens = estimate_tokens(text)
  cost_usd = (tokens / 1_000_000) * cost_per_1m_tokens
  ```

**4. Cache Hit Rate**
- **Definition:** Percentage of embeddings served from cache
- **Unit:** Percentage (%)
- **Target:** >60% for production systems with repeated content
- **Measurement:**
  ```python
  hit_rate = (cache_hits / total_requests) * 100
  ```

### Secondary Metrics (Monitor Periodically)

**5. Error Rate**
- **Definition:** Percentage of failed embedding requests
- **Target:** <1%
- **Causes:** Rate limits, network errors, invalid input

**6. Queue Depth**
- **Definition:** Number of pending embedding requests
- **Target:** <1,000 for real-time systems
- **Indicates:** Backlog, need for scaling

**7. Model Load Time**
- **Definition:** Time to load local model into memory/GPU
- **Target:** <30 seconds
- **Relevant for:** Local models (sentence-transformers)

**8. GPU Utilization**
- **Definition:** Percentage of GPU compute used
- **Target:** 70-90% (indicates good batching)
- **Measurement:** `nvidia-smi` for NVIDIA GPUs

## Monitoring Architecture

### Level 1: Basic Logging

**Suitable For:** Prototyping, small applications (<10K embeddings/day)

**Implementation:**
```python
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingEmbedder:
    def __init__(self, embedder):
        self.embedder = embedder

    def embed_single(self, text):
        start = time.time()
        embedding = self.embedder.embed_single(text)
        latency = (time.time() - start) * 1000

        logger.info(f"Embedded 1 text in {latency:.2f}ms")
        return embedding
```

**Pros:** Simple, no dependencies
**Cons:** No aggregation, hard to query, no visualization

### Level 2: Structured Metrics

**Suitable For:** Production applications (10K-1M embeddings/day)

**Implementation:**
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict

@dataclass
class EmbeddingMetrics:
    total_texts: int = 0
    total_api_calls: int = 0
    total_cache_hits: int = 0
    total_latency_ms: float = 0.0
    total_cost_usd: float = 0.0
    errors: int = 0
    start_time: datetime = field(default_factory=datetime.now)

    def record_operation(self, num_texts, latency_ms, cache_hits=0, cost=0.0, error=False):
        self.total_texts += num_texts
        self.total_api_calls += 1 if cache_hits < num_texts else 0
        self.total_cache_hits += cache_hits
        self.total_latency_ms += latency_ms
        self.total_cost_usd += cost
        if error:
            self.errors += 1

    def summary(self) -> Dict:
        elapsed = (datetime.now() - self.start_time).total_seconds()
        return {
            'total_texts': self.total_texts,
            'cache_hit_rate': (self.total_cache_hits / self.total_texts * 100) if self.total_texts > 0 else 0,
            'avg_latency_ms': self.total_latency_ms / self.total_api_calls if self.total_api_calls > 0 else 0,
            'throughput_texts_per_sec': self.total_texts / elapsed if elapsed > 0 else 0,
            'total_cost_usd': self.total_cost_usd,
            'error_rate': (self.errors / self.total_api_calls * 100) if self.total_api_calls > 0 else 0,
            'elapsed_seconds': elapsed
        }
```

**Pros:** Queryable, in-memory aggregation
**Cons:** Lost on restart, no time-series data

### Level 3: Time-Series Metrics (Prometheus)

**Suitable For:** Large-scale production (1M+ embeddings/day)

**Implementation:**
```python
from prometheus_client import Counter, Histogram, Gauge

# Metrics
embedding_requests = Counter('embedding_requests_total', 'Total embedding requests')
embedding_latency = Histogram('embedding_latency_seconds', 'Embedding latency', buckets=[.01, .05, .1, .5, 1, 5])
cache_hits = Counter('embedding_cache_hits_total', 'Cache hits')
embedding_cost = Counter('embedding_cost_usd_total', 'Total embedding cost in USD')
queue_depth = Gauge('embedding_queue_depth', 'Current queue depth')

class PrometheusEmbedder:
    def __init__(self, embedder):
        self.embedder = embedder

    def embed_batch(self, texts):
        embedding_requests.inc(len(texts))
        queue_depth.set(len(texts))

        with embedding_latency.time():
            embeddings = self.embedder.embed_batch(texts)

        # Track cache hits
        if hasattr(self.embedder, 'cache_hits'):
            cache_hits.inc(self.embedder.cache_hits)

        return embeddings
```

**Pros:** Industry-standard, time-series, dashboards (Grafana)
**Cons:** Requires Prometheus infrastructure

### Level 4: APM (Application Performance Monitoring)

**Suitable For:** Enterprise applications, multi-service architectures

**Implementation (Datadog Example):**
```python
from ddtrace import tracer

class DatadogEmbedder:
    def __init__(self, embedder):
        self.embedder = embedder

    @tracer.wrap(service='embedding-service', resource='embed_batch')
    def embed_batch(self, texts):
        with tracer.trace('embedding.api_call', service='embedding-service') as span:
            span.set_tag('batch_size', len(texts))
            embeddings = self.embedder.embed_batch(texts)
            span.set_metric('embedding.batch_size', len(texts))

        return embeddings
```

**Pros:** Full observability, distributed tracing, alerting
**Cons:** Cost ($15-100/month), vendor lock-in

## Latency Tracking

### Percentiles vs. Average

**Problem:** Average latency hides outliers.

**Example:**
- 95% of requests: 50ms
- 5% of requests: 2,000ms (rate limits, retries)
- **Average:** 147ms (misleading)
- **p95:** 2,000ms (shows real user experience)

**Solution:** Track percentiles (p50, p95, p99)

```python
import numpy as np

class LatencyTracker:
    def __init__(self):
        self.latencies = []

    def record(self, latency_ms):
        self.latencies.append(latency_ms)

    def percentiles(self):
        if not self.latencies:
            return {}

        return {
            'p50': np.percentile(self.latencies, 50),
            'p95': np.percentile(self.latencies, 95),
            'p99': np.percentile(self.latencies, 99),
            'avg': np.mean(self.latencies),
            'min': np.min(self.latencies),
            'max': np.max(self.latencies)
        }

# Usage
tracker = LatencyTracker()
for text in texts:
    start = time.time()
    embedding = embedder.embed_single(text)
    tracker.record((time.time() - start) * 1000)

print(tracker.percentiles())
# Output: {'p50': 52.3, 'p95': 87.1, 'p99': 102.5, 'avg': 54.8, ...}
```

### Latency Breakdown

**Identify bottlenecks:**
- Network latency (API calls)
- Embedding generation (model inference)
- Cache lookup
- Serialization/deserialization

```python
class DetailedLatencyTracker:
    def track_embedding(self, text):
        timings = {}

        # Cache lookup
        start = time.time()
        cached = self.cache.get(text)
        timings['cache_lookup_ms'] = (time.time() - start) * 1000

        if cached:
            return cached, timings

        # API call or model inference
        start = time.time()
        embedding = self.embedder.embed_single(text)
        timings['embedding_generation_ms'] = (time.time() - start) * 1000

        # Cache write
        start = time.time()
        self.cache.set(text, embedding)
        timings['cache_write_ms'] = (time.time() - start) * 1000

        timings['total_ms'] = sum(timings.values())
        return embedding, timings

# Analyze
embedding, timings = tracker.track_embedding(text)
print(f"Cache lookup: {timings['cache_lookup_ms']:.2f}ms")
print(f"Generation: {timings['embedding_generation_ms']:.2f}ms")
print(f"Cache write: {timings['cache_write_ms']:.2f}ms")
```

## Cost Tracking

### Token Estimation

**Accurate Token Counting:**
```python
import tiktoken

def count_tokens_openai(text, model='text-embedding-3-small'):
    """Accurate token count for OpenAI models."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Usage
text = "What is the capital of France?"
tokens = count_tokens_openai(text)
print(f"Tokens: {tokens}")  # Output: Tokens: 7
```

**Fast Token Estimation (Approximation):**
```python
def estimate_tokens_fast(text):
    """Fast approximation: 1 token ≈ 4 characters."""
    return len(text) // 4

# Usage
tokens = estimate_tokens_fast(text)  # Faster, less accurate
```

### Cost Calculation

```python
class CostTracker:
    PRICING = {
        'text-embedding-3-small': 0.00002,  # per 1K tokens
        'text-embedding-3-large': 0.00013,
        'embed-english-v3.0': 0.0001,
    }

    def __init__(self, model):
        self.model = model
        self.total_tokens = 0
        self.total_cost = 0.0

    def record_embedding(self, text):
        tokens = count_tokens_openai(text, self.model)
        cost = (tokens / 1000) * self.PRICING[self.model]

        self.total_tokens += tokens
        self.total_cost += cost

        return tokens, cost

    def summary(self):
        return {
            'total_tokens': self.total_tokens,
            'total_cost_usd': round(self.total_cost, 4),
            'avg_tokens_per_text': self.total_tokens / max(1, self.calls),
        }

# Usage
tracker = CostTracker(model='text-embedding-3-small')
for text in texts:
    tokens, cost = tracker.record_embedding(text)

print(tracker.summary())
# Output: {'total_tokens': 50000, 'total_cost_usd': 1.0, ...}
```

### Budget Alerting

```python
class BudgetMonitor:
    def __init__(self, daily_budget_usd=10.0):
        self.daily_budget = daily_budget_usd
        self.today_spend = 0.0
        self.today = datetime.now().date()

    def record_cost(self, cost_usd):
        # Reset if new day
        if datetime.now().date() != self.today:
            self.today_spend = 0.0
            self.today = datetime.now().date()

        self.today_spend += cost_usd

        # Alert if over budget
        if self.today_spend > self.daily_budget:
            self.alert_over_budget()

    def alert_over_budget(self):
        print(f"WARNING: Daily budget exceeded! Spent: ${self.today_spend:.2f}, Budget: ${self.daily_budget:.2f}")
        # Send alert (email, Slack, PagerDuty, etc.)

    def remaining_budget(self):
        return max(0, self.daily_budget - self.today_spend)
```

## Cache Performance

### Cache Hit Rate Tracking

```python
class CacheMetrics:
    def __init__(self):
        self.hits = 0
        self.misses = 0

    def record_hit(self):
        self.hits += 1

    def record_miss(self):
        self.misses += 1

    def hit_rate(self):
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0

    def summary(self):
        return {
            'hits': self.hits,
            'misses': self.misses,
            'total': self.hits + self.misses,
            'hit_rate_pct': round(self.hit_rate(), 2)
        }

# Usage
cache_metrics = CacheMetrics()

for text in texts:
    if cache.exists(text):
        cache_metrics.record_hit()
        embedding = cache.get(text)
    else:
        cache_metrics.record_miss()
        embedding = embedder.embed_single(text)
        cache.set(text, embedding)

print(cache_metrics.summary())
# Output: {'hits': 600, 'misses': 400, 'total': 1000, 'hit_rate_pct': 60.0}
```

### Cache Size Monitoring

```python
class CacheSizeMonitor:
    def __init__(self, redis_client):
        self.redis = redis_client

    def get_cache_size(self):
        """Get total number of cached embeddings."""
        return self.redis.dbsize()

    def get_memory_usage(self):
        """Get Redis memory usage in MB."""
        info = self.redis.info('memory')
        return info['used_memory'] / (1024 * 1024)  # Convert to MB

    def get_stats(self):
        return {
            'cache_entries': self.get_cache_size(),
            'memory_mb': round(self.get_memory_usage(), 2),
            'avg_entry_size_kb': round(self.get_memory_usage() * 1024 / max(1, self.get_cache_size()), 2)
        }

# Usage
monitor = CacheSizeMonitor(redis_client)
stats = monitor.get_stats()
print(f"Cache entries: {stats['cache_entries']}")
print(f"Memory usage: {stats['memory_mb']} MB")
```

### Cache Effectiveness Analysis

```python
def analyze_cache_effectiveness(cache_metrics, cost_tracker):
    """Calculate cost savings from caching."""

    total_requests = cache_metrics.hits + cache_metrics.misses
    cache_hit_rate = cache_metrics.hit_rate()

    # Calculate costs
    actual_cost = cost_tracker.total_cost  # With caching
    no_cache_cost = actual_cost / (1 - cache_hit_rate / 100)  # Without caching (estimated)

    savings = no_cache_cost - actual_cost
    savings_pct = (savings / no_cache_cost * 100) if no_cache_cost > 0 else 0

    return {
        'cache_hit_rate': round(cache_hit_rate, 2),
        'actual_cost_usd': round(actual_cost, 4),
        'no_cache_cost_usd': round(no_cache_cost, 4),
        'savings_usd': round(savings, 4),
        'savings_pct': round(savings_pct, 2)
    }

# Usage
analysis = analyze_cache_effectiveness(cache_metrics, cost_tracker)
print(f"Cache hit rate: {analysis['cache_hit_rate']}%")
print(f"Cost with cache: ${analysis['actual_cost_usd']}")
print(f"Cost without cache: ${analysis['no_cache_cost_usd']}")
print(f"Savings: ${analysis['savings_usd']} ({analysis['savings_pct']}%)")
```

## Alerting and Thresholds

### Threshold Configuration

```python
THRESHOLDS = {
    'latency_p95_ms': 500,      # Alert if p95 latency > 500ms
    'error_rate_pct': 1.0,      # Alert if error rate > 1%
    'cache_hit_rate_pct': 40,   # Alert if cache hit rate < 40%
    'daily_cost_usd': 100,      # Alert if daily cost > $100
    'queue_depth': 1000,        # Alert if queue depth > 1000
}
```

### Alert System

```python
class AlertSystem:
    def __init__(self, thresholds):
        self.thresholds = thresholds
        self.alerts = []

    def check_metrics(self, metrics):
        """Check metrics against thresholds and generate alerts."""

        # Latency
        if metrics.get('latency_p95_ms', 0) > self.thresholds['latency_p95_ms']:
            self.alert('HIGH_LATENCY', f"p95 latency: {metrics['latency_p95_ms']:.2f}ms")

        # Error rate
        if metrics.get('error_rate_pct', 0) > self.thresholds['error_rate_pct']:
            self.alert('HIGH_ERROR_RATE', f"Error rate: {metrics['error_rate_pct']:.2f}%")

        # Cache hit rate
        if metrics.get('cache_hit_rate_pct', 100) < self.thresholds['cache_hit_rate_pct']:
            self.alert('LOW_CACHE_HIT_RATE', f"Cache hit rate: {metrics['cache_hit_rate_pct']:.2f}%")

        # Cost
        if metrics.get('daily_cost_usd', 0) > self.thresholds['daily_cost_usd']:
            self.alert('BUDGET_EXCEEDED', f"Daily cost: ${metrics['daily_cost_usd']:.2f}")

    def alert(self, alert_type, message):
        """Send alert (print, email, Slack, PagerDuty, etc.)."""
        alert = {
            'type': alert_type,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        self.alerts.append(alert)
        print(f"ALERT [{alert_type}]: {message}")

        # Send notification (implement as needed)
        # self.send_slack(message)
        # self.send_email(message)

    def get_alerts(self):
        return self.alerts

# Usage
alert_system = AlertSystem(THRESHOLDS)
metrics = {
    'latency_p95_ms': 650,       # Over threshold (500)
    'error_rate_pct': 0.5,       # OK
    'cache_hit_rate_pct': 35,    # Under threshold (40)
    'daily_cost_usd': 50,        # OK
}

alert_system.check_metrics(metrics)
# Output:
# ALERT [HIGH_LATENCY]: p95 latency: 650.00ms
# ALERT [LOW_CACHE_HIT_RATE]: Cache hit rate: 35.00%
```

### Dashboard Example (Textual)

```python
def print_dashboard(metrics, cache_metrics, cost_tracker):
    """Print a simple textual dashboard."""

    print("=" * 60)
    print("EMBEDDING PIPELINE DASHBOARD")
    print("=" * 60)

    print("\nPERFORMANCE:")
    print(f"  Throughput:     {metrics['throughput_texts_per_sec']:.2f} texts/sec")
    print(f"  Latency (avg):  {metrics['avg_latency_ms']:.2f} ms")
    print(f"  Latency (p95):  {metrics['latency_p95_ms']:.2f} ms")
    print(f"  Error Rate:     {metrics['error_rate_pct']:.2f}%")

    print("\nCACHE:")
    print(f"  Hit Rate:       {cache_metrics['hit_rate_pct']:.2f}%")
    print(f"  Total Hits:     {cache_metrics['hits']:,}")
    print(f"  Total Misses:   {cache_metrics['misses']:,}")

    print("\nCOST:")
    print(f"  Total Cost:     ${cost_tracker['total_cost_usd']:.4f}")
    print(f"  Total Tokens:   {cost_tracker['total_tokens']:,}")
    print(f"  Avg Cost/Text:  ${cost_tracker['avg_cost_per_text']:.6f}")

    print("\nOVERALL:")
    print(f"  Total Texts:    {metrics['total_texts']:,}")
    print(f"  Elapsed Time:   {metrics['elapsed_seconds']:.2f}s")

    print("=" * 60)

# Usage
print_dashboard(metrics, cache_metrics.summary(), cost_tracker.summary())
```

## Monitoring Checklist

Before deploying to production:

**Metrics Collection:**
- [ ] Latency tracking (p50, p95, p99)
- [ ] Throughput measurement (texts/sec)
- [ ] Cost tracking (tokens, USD)
- [ ] Cache hit rate monitoring
- [ ] Error rate tracking

**Infrastructure:**
- [ ] Metrics storage (in-memory, Prometheus, APM)
- [ ] Alerting system configured
- [ ] Thresholds set for critical metrics
- [ ] Dashboard for visualization

**Alerting:**
- [ ] High latency alerts (p95 > threshold)
- [ ] Low cache hit rate alerts (<40%)
- [ ] Budget exceeded alerts
- [ ] High error rate alerts (>1%)

**Analysis:**
- [ ] Baseline metrics established
- [ ] Percentile analysis (not just averages)
- [ ] Cost breakdown (cache hits vs. misses)
- [ ] Performance regression detection
