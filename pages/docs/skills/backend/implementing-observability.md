---
sidebar_position: 9
title: Observability
description: Monitoring, logging, and tracing with OpenTelemetry
tags: [backend, observability, opentelemetry, metrics, logs, traces]
---

# Production Observability with OpenTelemetry

Implement production-grade observability using OpenTelemetry as the 2025 industry standard. Covers the three pillars (metrics, logs, traces), LGTM stack deployment, and critical log-trace correlation patterns.

## When to Use

Use when:
- Building production systems requiring visibility into performance and errors
- Debugging distributed systems with multiple services
- Setting up monitoring, logging, or tracing infrastructure
- Implementing structured logging with trace correlation
- Configuring alerting rules for production systems

Skip if:
- Building proof-of-concept without production deployment
- System has < 100 requests/day (console logging may suffice)

## Multi-Language Support

This skill provides patterns for:
- **Python**: opentelemetry-api, opentelemetry-sdk, structlog
- **Rust**: opentelemetry, tracing-opentelemetry
- **Go**: go.opentelemetry.io/otel, slog
- **TypeScript**: @opentelemetry/api, pino

## The OpenTelemetry Standard (2025)

OpenTelemetry is the CNCF graduated project unifying observability:

```
┌────────────────────────────────────────────────────────┐
│          OpenTelemetry: The Unified Standard           │
├────────────────────────────────────────────────────────┤
│                                                         │
│  ONE SDK for ALL signals:                              │
│  ├── Metrics (Prometheus-compatible)                   │
│  ├── Logs (structured, correlated)                     │
│  ├── Traces (distributed, standardized)                │
│  └── Context (propagates across services)              │
│                                                         │
│  Language SDKs:                                         │
│  ├── Python: opentelemetry-api, opentelemetry-sdk      │
│  ├── Rust: opentelemetry, tracing-opentelemetry        │
│  ├── Go: go.opentelemetry.io/otel                      │
│  └── TypeScript: @opentelemetry/api                    │
│                                                         │
│  Export to ANY backend:                                │
│  ├── LGTM Stack (Loki, Grafana, Tempo, Mimir)          │
│  ├── Prometheus + Jaeger                               │
│  ├── Datadog, New Relic, Honeycomb (SaaS)              │
│  └── Custom backends via OTLP protocol                 │
│                                                         │
└────────────────────────────────────────────────────────┘
```

## The Three Pillars of Observability

### 1. Metrics (What is happening?)

Track system health and performance over time.

**Metric Types**: Counters (always increase), Gauges (up/down), Histograms (distributions), Summaries (percentiles).

**Example (Python)**:
```python
from opentelemetry import metrics

meter = metrics.get_meter(__name__)
http_requests = meter.create_counter("http.server.requests")
http_requests.add(1, {"method": "GET", "status": 200})
```

### 2. Logs (What happened?)

Record discrete events with context.

**CRITICAL**: Always inject trace_id/span_id for log-trace correlation.

**Example (Python + structlog)**:
```python
import structlog
from opentelemetry import trace

logger = structlog.get_logger()
span = trace.get_current_span()
ctx = span.get_span_context()

logger.info(
    "processing_request",
    trace_id=format(ctx.trace_id, '032x'),
    span_id=format(ctx.span_id, '016x'),
    user_id=user_id
)
```

### 3. Traces (Where did time go?)

Track request flow across distributed services.

**Key Concepts**: Trace (end-to-end journey), Span (individual operation), Parent-Child (nested operations).

**Example (Python + FastAPI)**:
```python
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)  # Auto-traces all HTTP requests
```

## The LGTM Stack (Self-Hosted Observability)

LGTM = **L**oki (Logs) + **G**rafana (Visualization) + **T**empo (Traces) + **M**imir (Metrics)

```
┌────────────────────────────────────────────────────────┐
│                  LGTM Architecture                      │
├────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────┐      │
│  │           Grafana Dashboard (Port 3000)      │      │
│  │  Unified UI for Logs, Metrics, Traces       │      │
│  └──────┬──────────────┬─────────────┬─────────┘      │
│         │              │             │                 │
│         ▼              ▼             ▼                 │
│  ┌──────────┐   ┌──────────┐  ┌──────────┐            │
│  │   Loki   │   │  Tempo   │  │  Mimir   │            │
│  │  (Logs)  │   │ (Traces) │  │(Metrics) │            │
│  │Port 3100 │   │Port 3200 │  │Port 9009 │            │
│  └────▲─────┘   └────▲─────┘  └────▲─────┘            │
│       │              │             │                   │
│       └──────────────┴─────────────┘                   │
│                      │                                 │
│              ┌───────▼────────┐                        │
│              │ Grafana Alloy  │                        │
│              │  (Collector)   │                        │
│              │  Port 4317/8   │ ← OTLP gRPC/HTTP       │
│              └───────▲────────┘                        │
│                      │                                 │
│         OpenTelemetry Instrumented Apps                │
│                                                         │
└────────────────────────────────────────────────────────┘
```

## Critical Pattern: Log-Trace Correlation

**The Problem**: Logs and traces live in separate systems. You see an error log but can't find the related trace.

**The Solution**: Inject `trace_id` and `span_id` into every log record.

### Python (structlog)

```python
import structlog
from opentelemetry import trace

logger = structlog.get_logger()
span = trace.get_current_span()
ctx = span.get_span_context()

logger.info(
    "request_processed",
    trace_id=format(ctx.trace_id, '032x'),  # 32-char hex
    span_id=format(ctx.span_id, '016x'),    # 16-char hex
    user_id=user_id
)
```

### Rust (tracing)

```rust
use tracing::{info, instrument};

#[instrument(fields(user_id = %user_id))]
async fn process_request(user_id: u64) -> Result<Response> {
    // trace_id/span_id automatically included
    info!(user_id = user_id, "processing request");
    Ok(result)
}
```

### Query in Grafana

```logql
{job="api-service"} |= "trace_id=4bf92f3577b34da6a3ce929d0e0e4736"
```

## Quick Setup Guide

### 1. Choose Your Stack

**Decision Tree**:
- **Greenfield**: OpenTelemetry SDK + LGTM Stack (self-hosted) or Grafana Cloud (managed)
- **Existing Prometheus**: Add Loki (logs) + Tempo (traces)
- **Kubernetes**: LGTM via Helm, Alloy DaemonSet
- **Zero-ops**: Managed SaaS (Grafana Cloud, Datadog, New Relic)

### 2. Install OpenTelemetry SDK

**Manual (Python)**:
```bash
pip install opentelemetry-api opentelemetry-sdk \
    opentelemetry-instrumentation-fastapi \
    opentelemetry-exporter-otlp
```

### 3. Deploy LGTM Stack

**Docker Compose** (development):
```bash
cd examples/lgtm-docker-compose
docker-compose up -d
# Grafana: http://localhost:3000 (admin/admin)
# OTLP: localhost:4317 (gRPC), localhost:4318 (HTTP)
```

## Auto-Instrumentation

OpenTelemetry auto-instruments popular frameworks:

```python
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)  # Auto-trace all HTTP requests
```

**Supported**: FastAPI, Flask, Django, Express, Gin, Echo, Nest.js

## Common Patterns

### Custom Spans

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("fetch_user_details") as span:
    span.set_attribute("user_id", user_id)
    user = await db.fetch_user(user_id)
    span.set_attribute("user_found", user is not None)
```

### Error Tracking

```python
from opentelemetry.trace import Status, StatusCode

with tracer.start_as_current_span("process_payment") as span:
    try:
        result = process_payment(amount, card_token)
        span.set_status(Status(StatusCode.OK))
    except PaymentError as e:
        span.set_status(Status(StatusCode.ERROR, str(e)))
        span.record_exception(e)
        raise
```

## Integration with Other Skills

- **Dashboards**: Embed Grafana panels, query Prometheus metrics
- **Feedback**: Alert routing (Slack, PagerDuty), notification UI
- **Data-Viz**: Time-series charts, trace waterfall, latency heatmaps
- **API Patterns**: Auto-instrument REST/GraphQL APIs
- **Message Queues**: Trace async job processing

## Key Principles

1. **OpenTelemetry is THE standard** - Use OTel SDK, not vendor-specific SDKs
2. **Auto-instrumentation first** - Prefer auto over manual spans
3. **Always correlate logs and traces** - Inject trace_id/span_id into every log
4. **Use structured logging** - JSON format, consistent field names
5. **LGTM stack for self-hosting** - Production-ready open-source stack

## Common Pitfalls

**Don't**:
- Use vendor-specific SDKs (use OpenTelemetry)
- Log without trace_id/span_id context
- Manually instrument what auto-instrumentation covers
- Mix logging libraries (pick one: structlog, tracing, slog, pino)

**Do**:
- Start with auto-instrumentation
- Add manual spans only for business-critical operations
- Use semantic conventions for span attributes
- Export to OTLP (gRPC preferred over HTTP)
- Test locally with LGTM docker-compose before production

## Success Metrics

1. 100% of logs include trace_id when in request context
2. Mean time to resolution (MTTR) decreases by >50%
3. Developers use Grafana as first debugging tool
4. 80%+ of telemetry from auto-instrumentation
5. Alert noise < 5% false positives

## Related Skills

- [API Patterns](./implementing-api-patterns) - Instrument APIs automatically
- [Message Queues](./using-message-queues) - Trace async workflows
- [Dashboards](../frontend/creating-dashboards) - Visualize metrics in Grafana
- [Deploying Applications](./deploying-applications) - Deploy LGTM stack

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/implementing-observability)
- OpenTelemetry: https://opentelemetry.io/
- Grafana LGTM: https://grafana.com/
- Prometheus: https://prometheus.io/
