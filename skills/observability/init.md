# Observability - Master Plan

> **Skill Purpose**: Production visibility through monitoring, logging, and tracing using OpenTelemetry as the unified 2025 standard.
>
> **Date**: December 2025
> **Status**: Planning Phase
> **Research Sources**: FULL_STACK_SKILLS_UNIFIED.md (Context7 research), OpenTelemetry 2025 specifications, LGTM stack documentation

---

## Strategic Positioning

### The Critical Production Gap

Most applications ship to production blind:
- **No visibility** into performance bottlenecks
- **No correlation** between logs, metrics, and traces
- **Alert fatigue** from poorly configured monitoring
- **Debugging black holes** when distributed systems fail

This skill solves production visibility with **OpenTelemetry** as the 2025 standard:
- **One SDK** for metrics, logs, and traces across all languages
- **Vendor-neutral** - works with any backend (Prometheus, Datadog, etc.)
- **Automatic instrumentation** for popular frameworks
- **Standardized context propagation** across microservices

### Why OpenTelemetry is THE Standard (2025)

```
┌─────────────────────────────────────────────────────────────┐
│           The Observability Landscape Evolution              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Pre-2020: Fragmented                                        │
│  ├── Prometheus SDK for metrics                             │
│  ├── Custom logging libraries                               │
│  └── Jaeger/Zipkin for traces (incompatible protocols)      │
│                                                              │
│  2025: OpenTelemetry Unified Standard                        │
│  └── One SDK for ALL observability signals                  │
│      ├── Metrics (Prometheus-compatible)                    │
│      ├── Logs (structured, correlated)                      │
│      ├── Traces (distributed, standardized)                 │
│      └── Baggage (context propagation)                      │
│                                                              │
│  Adoption: CNCF graduated project, industry standard         │
│  ├── Supported by: Google, Microsoft, AWS, Datadog          │
│  ├── Native SDKs: Python, Rust, Go, TypeScript, Java, .NET  │
│  └── Auto-instrumentation: 50+ frameworks                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Integration with Frontend Skills

| Frontend Skill | Backend Observability Pattern |
|----------------|-------------------------------|
| **dashboards** | Grafana panels consuming OTel metrics, real-time alerts |
| **data-viz** | Time-series charts from Prometheus/Mimir |
| **feedback** | Alert threshold configuration, notification routing |
| **forms** | Form submission metrics (success rate, validation errors) |
| **ai-chat** | LLM request tracing, token usage metrics, latency monitoring |

---

## Component Taxonomy (Tiered Architecture)

### Tier 1: The Three Pillars (OpenTelemetry Signals)

```
┌─────────────────────────────────────────────────────────────┐
│                  Three Pillars of Observability              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. METRICS (What is happening?)                             │
│     ├── Gauges: Current CPU, memory, queue depth            │
│     ├── Counters: Total requests, errors                    │
│     ├── Histograms: Request latency distribution            │
│     └── Summaries: Percentiles (p50, p95, p99)              │
│                                                              │
│  2. LOGS (What happened?)                                    │
│     ├── Structured format (JSON with trace_id)              │
│     ├── Log levels (DEBUG, INFO, WARN, ERROR)               │
│     ├── Context binding (user_id, request_id)               │
│     └── Correlation with traces                             │
│                                                              │
│  3. TRACES (Where did time go?)                              │
│     ├── Spans: Individual operations                        │
│     ├── Distributed tracing: Across services                │
│     ├── Parent-child relationships                          │
│     └── Timing breakdown (network, DB, compute)             │
│                                                              │
│  UNIFIED BY: OpenTelemetry Context Propagation               │
│  └── trace_id, span_id flow through all signals             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Tier 2: OpenTelemetry SDKs by Language

#### Context7 Library Research

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **OpenTelemetry** | `/websites/opentelemetry_io` | High | 5,888 | 85.9 | Unified standard |
| **OTel Python** | `/websites/opentelemetry-python_readthedocs_io_en_stable` | High | 926 | - | Python SDK |
| **OTel .NET** | `/open-telemetry/opentelemetry-dotnet` | High | 202 | 96.9 | .NET SDK (highest score) |
| **OTel JavaScript** | `/open-telemetry/opentelemetry-js` | High | 219 | 81.3 | Node.js/Browser |
| **OTel Rust** | `/open-telemetry/opentelemetry-rust` | High | 55 | 68.2 | Rust SDK |
| **OTel Go** | `/open-telemetry/opentelemetry-go` | High | 76 | 64.3 | Go SDK |
| **Tracing OTel** | `/tokio-rs/tracing-opentelemetry` | High | 10 | 86.6 | Rust tracing integration |

**Key Insight**: .NET SDK has the highest Context7 score (96.9), indicating exceptional documentation quality. Use as reference for implementation patterns.

#### SDK Quick Reference

| Language | SDK Package | Auto-Instrumentation | Manual Instrumentation |
|----------|-------------|----------------------|------------------------|
| **Python** | `opentelemetry-api`, `opentelemetry-sdk` | FastAPI, Flask, Django | Decorators, context managers |
| **Rust** | `opentelemetry`, `tracing-opentelemetry` | Axum, Actix-web | `tracing` macros |
| **Go** | `go.opentelemetry.io/otel` | Gin, Echo | Middleware, wrappers |
| **TypeScript** | `@opentelemetry/api`, `@opentelemetry/sdk-node` | Express, Fastify, Hono | Hooks, middleware |

### Tier 3: Structured Logging Libraries

**Critical Pattern**: Structured logging libraries inject `trace_id` and `span_id` into log records, enabling log-trace correlation.

| Language | Logger | Version | Key Feature | Integration |
|----------|--------|---------|-------------|-------------|
| **Python** | structlog | 24.x | Context binding, processors | OTel context extraction |
| **Rust** | tracing | 0.1.40 | Spans + events, async-aware | Native OTel bridge |
| **Go** | slog | stdlib 1.21+ | Native structured logging | Custom OTel handler |
| **TypeScript** | pino | 9.x | Fastest Node.js logger | OTel transport |

---

## The LGTM Stack (Self-Hosted Observability)

**LGTM** = **L**oki (Logs) + **G**rafana (Visualization) + **T**empo (Traces) + **M**imir (Metrics)

```
┌─────────────────────────────────────────────────────────────┐
│                    LGTM Observability Stack                  │
│              (Grafana Labs Open Source Stack)                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    Grafana Dashboard                  │   │
│  │  (Unified Visualization & Querying - Port 3000)      │   │
│  └────┬─────────────────┬─────────────────┬────────────┘   │
│       │                 │                 │                 │
│       ▼                 ▼                 ▼                 │
│  ┌─────────┐      ┌─────────┐      ┌─────────┐             │
│  │  Loki   │      │  Tempo  │      │  Mimir  │             │
│  │ (Logs)  │      │(Traces) │      │(Metrics)│             │
│  │Port 3100│      │Port 3200│      │Port 9009│             │
│  └────▲────┘      └────▲────┘      └────▲────┘             │
│       │                │                │                   │
│       │                │                │                   │
│       └────────────────┴────────────────┘                   │
│                        │                                    │
│                 ┌──────▼──────┐                             │
│                 │ Grafana     │                             │
│                 │   Alloy     │                             │
│                 │ (Collector) │                             │
│                 │  Port 4317  │  ← OTLP gRPC                │
│                 │  Port 4318  │  ← OTLP HTTP                │
│                 └──────▲──────┘                             │
│                        │                                    │
│                        │                                    │
│           OpenTelemetry Instrumented Apps                   │
│           (Python, Rust, Go, TypeScript)                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### LGTM Component Details

#### Loki (Logs)
- **Purpose**: Log aggregation and querying
- **Query Language**: LogQL (Prometheus-like syntax)
- **Storage**: Object storage (S3, GCS) or local filesystem
- **Key Feature**: Indexes only metadata, not log content (cost-effective)

#### Grafana (Visualization)
- **Purpose**: Unified dashboards, alerting, and exploration
- **Data Sources**: Loki, Tempo, Mimir, Prometheus
- **Key Feature**: Trace-to-logs correlation in one UI

#### Tempo (Traces)
- **Purpose**: Distributed tracing backend
- **Protocol**: OTLP, Jaeger, Zipkin
- **Storage**: Object storage (S3, GCS)
- **Key Feature**: Trace ID-based queries, no sampling required

#### Mimir (Metrics)
- **Purpose**: Prometheus-compatible long-term storage
- **Protocol**: Prometheus remote write, OTLP
- **Storage**: Object storage with aggressive compression
- **Key Feature**: Horizontally scalable, multi-tenant

#### Grafana Alloy (Collector)
- **Purpose**: Unified telemetry collector (replaces Grafana Agent)
- **Protocol**: OTLP gRPC/HTTP
- **Key Feature**: One collector for all signals (logs, metrics, traces)

### Alternative: Managed Observability

| Provider | Best For | LGTM Equivalent |
|----------|----------|-----------------|
| **Grafana Cloud** | Managed LGTM stack | All components (SaaS) |
| **Datadog** | Turnkey APM, extensive integrations | Proprietary stack |
| **New Relic** | Full observability, AI insights | Proprietary stack |
| **Honeycomb** | High-cardinality tracing, complex queries | Traces + events |

---

## Critical Pattern: Log-Trace Correlation

**The Problem**: Logs and traces live in separate systems. When debugging, you see an error log but can't find the related trace, or vice versa.

**The Solution**: Inject `trace_id` and `span_id` into every log record.

### Implementation by Language

#### Python (structlog + OpenTelemetry)

```python
import structlog
from opentelemetry import trace

# Configure structlog with OTel processor
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        # CRITICAL: Extract OTel context
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.PATHNAME,
                structlog.processors.CallsiteParameter.LINENO,
            ]
        ),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Usage in application code
@app.get("/api/data")
async def get_data(user_id: int):
    # Get current span
    span = trace.get_current_span()
    ctx = span.get_span_context()

    # CRITICAL: Include trace_id and span_id in logs
    logger.info(
        "processing_request",
        trace_id=format(ctx.trace_id, '032x'),  # 32-char hex
        span_id=format(ctx.span_id, '016x'),    # 16-char hex
        user_id=user_id,
        service="api-service"
    )

    # Business logic...
    result = await fetch_data(user_id)

    logger.info(
        "request_completed",
        trace_id=format(ctx.trace_id, '032x'),
        span_id=format(ctx.span_id, '016x'),
        user_id=user_id,
        records_returned=len(result)
    )

    return result
```

#### Rust (tracing + tracing-opentelemetry)

```rust
use tracing::{info, instrument};
use tracing_opentelemetry::OpenTelemetrySpanExt;

#[instrument(
    skip(db_pool),
    fields(
        user_id = %user_id,
        otel.kind = "server"
    )
)]
async fn get_data(user_id: u64, db_pool: &PgPool) -> Result<Vec<Record>> {
    // tracing automatically includes trace_id and span_id in logs
    info!(
        user_id = user_id,
        "processing request"
    );

    let result = sqlx::query_as::<_, Record>("SELECT * FROM data WHERE user_id = $1")
        .bind(user_id)
        .fetch_all(db_pool)
        .await?;

    info!(
        user_id = user_id,
        records_returned = result.len(),
        "request completed"
    );

    Ok(result)
}
```

**Key Insight (Rust)**: The `tracing` ecosystem automatically propagates trace context. Use `#[instrument]` macro for zero-boilerplate tracing.

#### Go (slog + OpenTelemetry)

```go
package main

import (
    "context"
    "log/slog"
    "go.opentelemetry.io/otel/trace"
)

// Custom handler that injects trace context
type OTelHandler struct {
    handler slog.Handler
}

func (h *OTelHandler) Handle(ctx context.Context, r slog.Record) error {
    span := trace.SpanFromContext(ctx)
    if span.SpanContext().IsValid() {
        r.AddAttrs(
            slog.String("trace_id", span.SpanContext().TraceID().String()),
            slog.String("span_id", span.SpanContext().SpanID().String()),
        )
    }
    return h.handler.Handle(ctx, r)
}

// Usage
func getData(ctx context.Context, userID int64) ([]Record, error) {
    logger := slog.Default()

    logger.InfoContext(ctx, "processing request",
        slog.Int64("user_id", userID),
    )

    // Business logic...
    result := fetchData(ctx, userID)

    logger.InfoContext(ctx, "request completed",
        slog.Int64("user_id", userID),
        slog.Int("records_returned", len(result)),
    )

    return result, nil
}
```

#### TypeScript (pino + OpenTelemetry)

```typescript
import pino from 'pino';
import { trace, context } from '@opentelemetry/api';

// Create logger with OTel integration
const logger = pino({
  mixin() {
    const span = trace.getActiveSpan();
    if (!span) return {};

    const spanContext = span.spanContext();
    return {
      trace_id: spanContext.traceId,
      span_id: spanContext.spanId,
      trace_flags: spanContext.traceFlags,
    };
  },
  formatters: {
    level(label) {
      return { level: label };
    },
  },
});

// Usage
async function getData(userId: number): Promise<Record[]> {
  logger.info({ user_id: userId }, 'processing request');

  const result = await fetchData(userId);

  logger.info(
    { user_id: userId, records_returned: result.length },
    'request completed'
  );

  return result;
}
```

### Querying Correlated Data in Grafana

```promql
# Find all logs for a specific trace
{job="api-service"} |= "trace_id=4bf92f3577b34da6a3ce929d0e0e4736"

# Find traces with errors, then jump to logs
{job="api-service"} | json | status_code >= 500
```

---

## Decision Framework: Observability Stack Selection

```
┌─────────────────────────────────────────────────────────────┐
│              Observability Stack Decision Tree               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PRIMARY CONCERN?                                            │
│                                                              │
│  ├── STARTING FRESH (greenfield)                             │
│  │   └─ OpenTelemetry SDK + LGTM Stack (self-hosted)        │
│  │       OR Grafana Cloud (managed)                         │
│  │                                                          │
│  ├── ALREADY USING PROMETHEUS                                │
│  │   └─ Add: Loki (logs) + Tempo (traces) + Alloy          │
│  │       ├─ Keep Prometheus for metrics                    │
│  │       └─ Migrate to Mimir for long-term storage         │
│  │                                                          │
│  ├── NEED METRICS ONLY (no logs/traces)                      │
│  │   └─ Prometheus + Grafana                                │
│  │       ├─ Instrument with OpenTelemetry SDK               │
│  │       └─ Export to Prometheus (OTLP → Prometheus)        │
│  │                                                          │
│  ├── NEED LOGS ONLY (debugging, audit)                       │
│  │   └─ Loki + Grafana                                      │
│  │       ├─ Use structured logging (structlog, pino)        │
│  │       └─ Ship via Alloy or Promtail                     │
│  │                                                          │
│  ├── KUBERNETES DEPLOYMENT                                   │
│  │   └─ LGTM Stack via Helm charts                         │
│  │       ├─ DaemonSet: Alloy on every node                 │
│  │       ├─ StatefulSet: Loki, Tempo, Mimir                │
│  │       └─ Service mesh: Auto-instrument with Istio       │
│  │                                                          │
│  ├── BUDGET / ZERO-OPS                                       │
│  │   └─ Managed SaaS                                        │
│  │       ├─ Small team → Grafana Cloud                     │
│  │       ├─ Enterprise → Datadog or New Relic              │
│  │       └─ Trace-focused → Honeycomb                      │
│  │                                                          │
│  └── HIGH-CARDINALITY QUERIES (many unique tags)             │
│      └─ Tempo (traces) or Honeycomb                         │
│          └─ Traditional metrics DBs struggle with this      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Frontend Integration Patterns

### 1. Dashboards Skill Integration

**Use Case**: Grafana panels embedded in custom dashboards

```typescript
// components/monitoring-dashboard.tsx
import { GrafanaPanel } from '@/components/grafana-panel';

export function MonitoringDashboard() {
  return (
    <div className="dashboard">
      <GrafanaPanel
        panelId="cpu-usage"
        query="rate(process_cpu_seconds_total[5m])"
        title="CPU Usage"
      />
      <GrafanaPanel
        panelId="request-rate"
        query="sum(rate(http_requests_total[1m]))"
        title="Request Rate"
      />
    </div>
  );
}
```

### 2. Feedback Skill Integration

**Use Case**: Alert threshold configuration UI

```typescript
// components/alert-config.tsx
interface AlertConfig {
  metric: string;
  threshold: number;
  duration: string;
  severity: 'warning' | 'critical';
}

export function AlertConfigForm() {
  const [config, setConfig] = useState<AlertConfig>({
    metric: 'http_request_duration_seconds',
    threshold: 0.5,
    duration: '5m',
    severity: 'warning'
  });

  const handleSave = async () => {
    // POST to backend API
    await fetch('/api/alerts', {
      method: 'POST',
      body: JSON.stringify({
        expr: `${config.metric} > ${config.threshold}`,
        for: config.duration,
        annotations: { severity: config.severity }
      })
    });
  };

  return <form>{ /* Form fields */ }</form>;
}
```

### 3. Data-Viz Skill Integration

**Use Case**: Time-series charts from Prometheus

```typescript
// lib/prometheus-client.ts
export async function queryPrometheus(query: string, start: number, end: number, step: string) {
  const params = new URLSearchParams({
    query,
    start: start.toString(),
    end: end.toString(),
    step
  });

  const response = await fetch(`/api/v1/query_range?${params}`);
  const data = await response.json();

  // Transform to chart format
  return data.data.result.map((series: any) => ({
    name: series.metric.__name__,
    data: series.values.map(([timestamp, value]: [number, string]) => ({
      x: timestamp * 1000,
      y: parseFloat(value)
    }))
  }));
}
```

---

## Skill Structure

```
observability/
├── init.md                           # This file - master plan
├── SKILL.md                          # Main skill file (< 500 lines)
├── references/
│   ├── opentelemetry-setup.md        # OTel SDK setup by language
│   ├── structured-logging.md         # structlog, tracing, slog, pino patterns
│   ├── lgtm-stack.md                 # LGTM stack deployment guide
│   ├── trace-context.md              # Log-trace correlation patterns
│   ├── alerting-rules.md             # Prometheus/Loki alerting rules
│   ├── grafana-dashboards.md         # Dashboard JSON templates
│   └── auto-instrumentation.md       # Framework-specific auto-instrumentation
├── scripts/
│   ├── setup_otel.py                 # Bootstrap OTel SDK (Python)
│   ├── setup_otel.sh                 # Bootstrap OTel SDK (Rust/Go)
│   ├── generate_dashboards.py       # Generate Grafana dashboard JSON
│   └── validate_metrics.py          # Validate metric naming conventions
├── examples/
│   ├── fastapi-otel/                 # Complete FastAPI + OTel example
│   │   ├── main.py
│   │   ├── instrumentation.py
│   │   └── docker-compose.yml
│   ├── axum-tracing/                 # Complete Axum + tracing example
│   │   ├── src/main.rs
│   │   ├── Cargo.toml
│   │   └── docker-compose.yml
│   ├── nextjs-otel/                  # Complete Next.js + OTel example
│   │   ├── instrumentation.ts
│   │   ├── next.config.js
│   │   └── docker-compose.yml
│   └── lgtm-docker-compose/          # LGTM stack docker-compose
│       ├── docker-compose.yml
│       ├── alloy-config.yaml
│       ├── prometheus.yml
│       └── grafana-datasources.yaml
└── assets/
    ├── templates/
    │   ├── alert-rules.yaml          # Prometheus alert templates
    │   └── dashboard-templates.json  # Grafana dashboard templates
    └── diagrams/
        ├── lgtm-architecture.svg     # LGTM stack diagram
        └── trace-flow.svg            # Distributed trace flow

```

---

## SKILL.md Frontmatter Template

```yaml
---
name: observability
description: Monitoring, logging, and tracing implementation using OpenTelemetry as the unified 2025 standard. Use when building production systems requiring visibility into performance, errors, and behavior. Covers OpenTelemetry SDKs (Python, Rust, Go, TypeScript), the three pillars (metrics, logs, traces), LGTM stack (Loki, Grafana, Tempo, Mimir), structured logging (structlog, tracing, slog, pino), log-trace correlation, Prometheus metrics, and alerting patterns.
---
```

---

## Quality Checklist

### Before Finalizing SKILL.md:

**Core Quality:**
- [ ] OpenTelemetry emphasized as THE standard
- [ ] All Context7 IDs included for OTel SDKs
- [ ] LGTM stack diagram included
- [ ] Log-trace correlation pattern with code examples
- [ ] Structured logging libraries by language
- [ ] Examples are production-ready, not toy code
- [ ] SKILL.md body under 500 lines

**Naming and Structure:**
- [ ] Name: `observability` (gerund form would be "monitoring", but observability is the industry term)
- [ ] Description: Includes WHAT (monitoring, logging, tracing) and WHEN (production systems)
- [ ] File paths use forward slashes
- [ ] All references link directly from SKILL.md (one level deep)

**Code and Scripts:**
- [ ] `setup_otel.py` is executable and self-contained
- [ ] `generate_dashboards.py` generates valid Grafana JSON
- [ ] `validate_metrics.py` checks Prometheus naming conventions
- [ ] All dependencies listed in requirements.txt or inline

**Testing:**
- [ ] LGTM docker-compose stack starts successfully
- [ ] OTel instrumentation examples run and export telemetry
- [ ] Log-trace correlation verified in Grafana
- [ ] Token usage minimized via progressive disclosure

**Cross-Ecosystem Consistency:**
- [ ] Same patterns across Python, Rust, Go, TypeScript
- [ ] Consistent terminology (span, trace, metric, log)
- [ ] Same LGTM stack for all languages

---

## Integration Points

### With Other Backend Skills

| Backend Skill | Integration Pattern |
|---------------|---------------------|
| **api-patterns** | Auto-instrument REST/GraphQL endpoints, track latency/error rates |
| **databases-relational** | Trace SQL queries, measure connection pool metrics |
| **databases-vector** | Trace embedding generation, measure retrieval latency |
| **message-queues** | Trace messages across Kafka/RabbitMQ, measure queue depth |
| **auth-security** | Log authentication attempts, trace JWT validation |
| **deploying-applications** | Kubernetes service mesh integration (Istio), pod metrics |

### With Frontend Skills

| Frontend Skill | Integration Pattern |
|----------------|---------------------|
| **dashboards** | Embed Grafana panels, real-time metrics display |
| **data-viz** | Query Prometheus for time-series charts |
| **feedback** | Alert configuration UI, notification routing |
| **ai-chat** | Trace LLM requests, token usage metrics |

---

## Research Summary

### OpenTelemetry Documentation Quality

Based on Context7 scores, the .NET SDK has the best documentation (96.9), followed by Rust's tracing-opentelemetry bridge (86.6). Use these as reference implementations.

### LGTM Stack Maturity (2025)

- **Loki 3.x**: Production-ready, used by Grafana Labs internally
- **Tempo 2.x**: Mature, supports unlimited retention (object storage)
- **Mimir 2.x**: Horizontally scalable Prometheus replacement
- **Grafana Alloy**: New unified collector (replaces Grafana Agent)

### Structured Logging Best Practices

| Language | Logger | Maturity | Ecosystem |
|----------|--------|----------|-----------|
| Python | structlog | Mature (10+ years) | Extensive processors |
| Rust | tracing | Mature (5+ years) | Native async support |
| Go | slog | New (Go 1.21+) | Stdlib, no dependencies |
| TypeScript | pino | Mature (7+ years) | Fastest Node.js logger |

---

## Success Metrics

This skill is successful when:

1. **OpenTelemetry Adoption**: Developers default to OTel SDK (not vendor-specific SDKs)
2. **Log-Trace Correlation**: 100% of logs include trace_id when in request context
3. **LGTM Stack Deployment**: < 10 minutes to deploy full stack via docker-compose
4. **Auto-Instrumentation**: 80% of telemetry via auto-instrumentation (not manual)
5. **Mean Time to Resolution**: Reduced debugging time via correlated signals

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2025-12-02 | Initial master plan created |

---

*Document Status: Planning Phase - Ready for SKILL.md implementation*
*Next Step: Create SKILL.md with progressive disclosure to references/*
