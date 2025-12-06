# OpenTelemetry SDK Setup by Language

Complete setup guide for OpenTelemetry instrumentation across Python, Rust, Go, and TypeScript.

## Table of Contents

- [Python](#python)
  - [FastAPI](#fastapi)
  - [Flask](#flask)
  - [Django](#django)
- [Rust](#rust)
  - [Axum](#axum)
  - [Actix-web](#actix-web)
- [Go](#go)
  - [Gin](#gin)
  - [net/http](#nethttp)
- [TypeScript](#typescript)
  - [Express](#express)
  - [Next.js](#nextjs)

---

## Python

### Installation

```bash
pip install \
    opentelemetry-api \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    opentelemetry-instrumentation
```

### FastAPI

**Auto-Instrumentation (Recommended)**:

```python
# instrumentation.py
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

def setup_opentelemetry(app, service_name: str = "my-service"):
    """Configure OpenTelemetry for FastAPI application."""

    # Trace provider
    trace_provider = TracerProvider(
        resource=Resource.create({"service.name": service_name})
    )
    trace_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint="localhost:4317"))
    )
    trace.set_tracer_provider(trace_provider)

    # Metrics provider
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint="localhost:4317")
    )
    meter_provider = MeterProvider(
        resource=Resource.create({"service.name": service_name}),
        metric_readers=[metric_reader]
    )
    metrics.set_meter_provider(meter_provider)

    # Auto-instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    # Auto-instrument HTTP client (httpx)
    HTTPXClientInstrumentor().instrument()

    return trace_provider, meter_provider
```

**Usage**:

```python
# main.py
from fastapi import FastAPI
from instrumentation import setup_opentelemetry

app = FastAPI()
setup_opentelemetry(app, service_name="api-service")

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    # Automatically traced
    return {"user_id": user_id}
```

**Additional Dependencies**:
```bash
pip install opentelemetry-instrumentation-fastapi \
    opentelemetry-instrumentation-httpx \
    opentelemetry-instrumentation-sqlalchemy
```

### Flask

```python
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from flask import Flask

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
```

### Django

```python
from opentelemetry.instrumentation.django import DjangoInstrumentor

# In settings.py or wsgi.py
DjangoInstrumentor().instrument()
```

---

## Rust

### Installation (Cargo.toml)

```toml
[dependencies]
# OpenTelemetry
opentelemetry = { version = "0.21", features = ["rt-tokio"] }
opentelemetry-otlp = { version = "0.14", features = ["grpc-tonic"] }
opentelemetry_sdk = { version = "0.21", features = ["rt-tokio"] }

# Tracing
tracing = "0.1.40"
tracing-opentelemetry = "0.22"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }

# Framework-specific
axum = "0.7"  # or actix-web = "4"
tokio = { version = "1", features = ["full"] }
```

### Axum

**Complete Setup**:

```rust
// src/tracing.rs
use opentelemetry::{global, KeyValue};
use opentelemetry_otlp::WithExportConfig;
use opentelemetry_sdk::{runtime, Resource};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt, EnvFilter};

pub fn init_tracing(service_name: &str) -> Result<(), Box<dyn std::error::Error>> {
    // OTLP exporter
    let otlp_exporter = opentelemetry_otlp::new_exporter()
        .tonic()
        .with_endpoint("http://localhost:4317");

    // Tracer provider
    let tracer = opentelemetry_otlp::new_pipeline()
        .tracing()
        .with_exporter(otlp_exporter)
        .with_trace_config(
            opentelemetry_sdk::trace::config().with_resource(Resource::new(vec![
                KeyValue::new("service.name", service_name.to_string()),
            ])),
        )
        .install_batch(runtime::Tokio)?;

    // Set global tracer
    global::set_tracer_provider(tracer.clone());

    // Configure tracing-subscriber
    tracing_subscriber::registry()
        .with(EnvFilter::from_default_env())
        .with(tracing_subscriber::fmt::layer().json())
        .with(tracing_opentelemetry::layer().with_tracer(tracer))
        .init();

    Ok(())
}
```

**Usage in Axum**:

```rust
// src/main.rs
use axum::{routing::get, Router};
use tower_http::trace::TraceLayer;
use tracing::{info, instrument};

mod tracing;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize tracing
    tracing::init_tracing("axum-service")?;

    // Build router
    let app = Router::new()
        .route("/api/users/:user_id", get(get_user))
        .layer(TraceLayer::new_for_http());  // Auto-trace HTTP requests

    // Start server
    info!("Starting server on :3000");
    axum::Server::bind(&"0.0.0.0:3000".parse()?)
        .serve(app.into_make_service())
        .await?;

    Ok(())
}

#[instrument(
    skip(db),
    fields(user_id = %user_id)
)]
async fn get_user(
    Path(user_id): Path<u64>,
    Extension(db): Extension<PgPool>,
) -> Result<Json<User>, AppError> {
    info!(user_id = user_id, "fetching user");

    let user = sqlx::query_as::<_, User>("SELECT * FROM users WHERE id = $1")
        .bind(user_id)
        .fetch_one(&db)
        .await?;

    info!(user_id = user_id, "user found");
    Ok(Json(user))
}
```

**Key Insight**: The `#[instrument]` macro automatically:
- Creates a span with the function name
- Includes specified fields (user_id)
- Injects trace_id/span_id into logs
- Handles async functions correctly

### Actix-web

```rust
use actix_web::{web, App, HttpServer};
use tracing_actix_web::TracingLogger;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    tracing::init_tracing("actix-service")?;

    HttpServer::new(|| {
        App::new()
            .wrap(TracingLogger::default())  // Auto-trace HTTP requests
            .route("/api/users/{user_id}", web::get().to(get_user))
    })
    .bind("0.0.0.0:3000")?
    .run()
    .await
}
```

---

## Go

### Installation

```bash
go get -u \
    go.opentelemetry.io/otel \
    go.opentelemetry.io/otel/sdk \
    go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc \
    go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp
```

### Gin

**Setup**:

```go
// internal/tracing/tracing.go
package tracing

import (
    "context"
    "time"

    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.21.0"
)

func InitTracer(serviceName string) (*sdktrace.TracerProvider, error) {
    ctx := context.Background()

    // OTLP exporter
    exporter, err := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint("localhost:4317"),
        otlptracegrpc.WithInsecure(),
    )
    if err != nil {
        return nil, err
    }

    // Resource
    res, err := resource.New(ctx,
        resource.WithAttributes(semconv.ServiceName(serviceName)),
    )
    if err != nil {
        return nil, err
    }

    // Tracer provider
    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(res),
    )

    otel.SetTracerProvider(tp)
    return tp, nil
}
```

**Usage**:

```go
// main.go
package main

import (
    "github.com/gin-gonic/gin"
    "go.opentelemetry.io/contrib/instrumentation/github.com/gin-gonic/gin/otelgin"
    "go.opentelemetry.io/otel"

    "myapp/internal/tracing"
)

func main() {
    // Initialize tracer
    tp, err := tracing.InitTracer("gin-service")
    if err != nil {
        panic(err)
    }
    defer tp.Shutdown(context.Background())

    // Create router
    r := gin.Default()

    // Auto-instrument HTTP requests
    r.Use(otelgin.Middleware("gin-service"))

    r.GET("/api/users/:user_id", getUser)

    r.Run(":3000")
}

func getUser(c *gin.Context) {
    ctx := c.Request.Context()
    tracer := otel.Tracer("api")

    // Create custom span
    ctx, span := tracer.Start(ctx, "fetch_user")
    defer span.End()

    userID := c.Param("user_id")
    span.SetAttributes(attribute.String("user_id", userID))

    // Business logic...
    c.JSON(200, gin.H{"user_id": userID})
}
```

**Additional Dependencies**:
```bash
go get go.opentelemetry.io/contrib/instrumentation/github.com/gin-gonic/gin/otelgin
```

### net/http

```go
import (
    "net/http"
    "go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
)

func main() {
    // Wrap handler with otelhttp
    handler := otelhttp.NewHandler(http.HandlerFunc(handleRequest), "my-handler")
    http.ListenAndServe(":3000", handler)
}
```

---

## TypeScript

### Installation

```bash
npm install \
    @opentelemetry/api \
    @opentelemetry/sdk-node \
    @opentelemetry/auto-instrumentations-node \
    @opentelemetry/exporter-trace-otlp-grpc
```

### Express

**Setup (instrumentation.ts)**:

```typescript
// instrumentation.ts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'express-service',
  }),
  traceExporter: new OTLPTraceExporter({
    url: 'http://localhost:4317',
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      // Auto-instrument: http, https, express, pg, mysql, redis, etc.
      '@opentelemetry/instrumentation-fs': {
        enabled: false, // Disable filesystem tracing
      },
    }),
  ],
});

sdk.start();

// Graceful shutdown
process.on('SIGTERM', () => {
  sdk
    .shutdown()
    .then(() => console.log('Tracing terminated'))
    .catch((error) => console.log('Error terminating tracing', error))
    .finally(() => process.exit(0));
});
```

**Usage (server.ts)**:

```typescript
// CRITICAL: Import instrumentation FIRST
import './instrumentation';

import express from 'express';
import { trace, context } from '@opentelemetry/api';

const app = express();
const tracer = trace.getTracer('express-service');

app.get('/api/users/:userId', async (req, res) => {
  // HTTP request automatically traced

  // Create custom span
  const span = tracer.startSpan('fetch_user_details');
  span.setAttribute('user_id', req.params.userId);

  try {
    const user = await fetchUser(req.params.userId);
    span.setStatus({ code: SpanStatusCode.OK });
    res.json(user);
  } catch (error) {
    span.recordException(error as Error);
    span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
    res.status(500).json({ error: 'Internal Server Error' });
  } finally {
    span.end();
  }
});

app.listen(3000, () => {
  console.log('Server running on :3000');
});
```

**Package.json**:

```json
{
  "scripts": {
    "start": "node -r ./instrumentation.js dist/server.js"
  }
}
```

### Next.js

**Setup (instrumentation.ts in root)**:

```typescript
// instrumentation.ts (Next.js 13.4+)
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    const { registerOTel } = await import('@vercel/otel');
    registerOTel({
      serviceName: 'nextjs-app',
      traceExporter: 'otlp',
    });
  }
}
```

**next.config.js**:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    instrumentationHook: true,
  },
};

module.exports = nextConfig;
```

**Alternative (manual)**:

```typescript
// instrumentation.ts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: 'http://localhost:4317',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

---

## Environment Variables

All SDKs support configuration via environment variables:

```bash
# OTLP endpoint
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Service name
export OTEL_SERVICE_NAME=my-service

# Trace sampling (1.0 = 100%)
export OTEL_TRACES_SAMPLER=parentbased_always_on

# Log level
export OTEL_LOG_LEVEL=debug
```

---

## Validation

**Test trace export**:

```bash
# Python
python -c "from opentelemetry import trace; trace.get_tracer(__name__).start_span('test').end()"

# Rust
cargo run --example test-trace

# Go
go run test-trace.go

# TypeScript
node -r ./instrumentation.js -e "console.log('Tracing initialized')"
```

**Verify in Grafana**:
1. Navigate to Explore → Tempo
2. Query: `{service.name="my-service"}`
3. Should see traces appearing

---

## Context7 References

- **OpenTelemetry**: `/websites/opentelemetry_io` (Trust: High, Snippets: 5,888, Score: 85.9)
- **Python**: `/websites/opentelemetry-python_readthedocs_io_en_stable` (Snippets: 926)
- **.NET** (best docs): `/open-telemetry/opentelemetry-dotnet` (Score: 96.9)
- **JavaScript**: `/open-telemetry/opentelemetry-js` (Score: 81.3)
- **Rust**: `/open-telemetry/opentelemetry-rust` (Score: 68.2)
- **Go**: `/open-telemetry/opentelemetry-go` (Score: 64.3)
- **Tracing OTel**: `/tokio-rs/tracing-opentelemetry` (Score: 86.6)

---

## Troubleshooting

**Traces not appearing in Tempo**:
- Check OTLP endpoint is reachable: `telnet localhost 4317`
- Verify Grafana Alloy is running: `docker ps | grep alloy`
- Check application logs for export errors

**High memory usage**:
- Reduce batch size in exporter configuration
- Enable sampling for high-traffic services
- Use tail-based sampling in Grafana Alloy

**Slow performance**:
- Use gRPC exporter instead of HTTP (4317 vs 4318)
- Enable async/batching exporters
- Verify auto-instrumentation isn't over-instrumenting
