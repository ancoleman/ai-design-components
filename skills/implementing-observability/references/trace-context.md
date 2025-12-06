# Trace Context Propagation Patterns

Complete guide for propagating trace context across services, background jobs, and message queues.

## Table of Contents

- [Context Propagation Fundamentals](#context-propagation-fundamentals)
- [HTTP Service-to-Service](#http-service-to-service)
- [Message Queues](#message-queues)
- [Background Jobs](#background-jobs)
- [Database Calls](#database-calls)
- [Cross-Language Propagation](#cross-language-propagation)

---

## Context Propagation Fundamentals

### What is Trace Context?

**Trace context** consists of:
- `trace_id`: Unique identifier for the entire request flow (128-bit)
- `span_id`: Unique identifier for the current operation (64-bit)
- `trace_flags`: Sampling and other flags (8-bit)

**W3C Trace Context Standard** (HTTP header):
```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
             │  └──────────────trace_id──────────────┘ └───span_id───┘ │
             │                                                          │
        version                                                    flags
```

### Automatic Propagation

OpenTelemetry SDKs automatically propagate context via:
- **HTTP headers**: `traceparent`, `tracestate`
- **gRPC metadata**: Same headers in metadata
- **Message attributes**: Injected into message headers/properties

---

## HTTP Service-to-Service

### Python (httpx + FastAPI)

**Service A (Client)**:

```python
# No manual propagation needed with auto-instrumentation
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
import httpx

# Auto-instrument httpx (propagates trace context automatically)
HTTPXClientInstrumentor().instrument()

@app.get("/api/proxy")
async def proxy_request():
    async with httpx.AsyncClient() as client:
        # trace_id automatically included in headers
        response = await client.get("http://service-b:3000/api/data")
        return response.json()
```

**Service B (Server)**:

```python
# FastAPI auto-instrumentation extracts trace context from headers
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

@app.get("/api/data")
async def get_data():
    # Automatically continues trace from Service A
    # Same trace_id, new span_id
    return {"data": "value"}
```

**Manual Propagation** (if auto-instrumentation unavailable):

```python
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry import trace

# Inject trace context into HTTP headers
propagator = TraceContextTextMapPropagator()
carrier = {}
propagator.inject(carrier)  # Adds traceparent header

# Make request with injected headers
async with httpx.AsyncClient() as client:
    response = await client.get(
        "http://service-b:3000/api/data",
        headers=carrier
    )
```

### Rust (reqwest + Axum)

**Service A (Client)**:

```rust
use opentelemetry::global;
use opentelemetry_http::HeaderInjector;
use reqwest;

async fn call_service_b() -> Result<String, reqwest::Error> {
    let client = reqwest::Client::new();

    // Manually inject trace context
    let mut req = client.get("http://service-b:3000/api/data").build()?;

    let cx = opentelemetry::Context::current();
    global::get_text_map_propagator(|propagator| {
        propagator.inject_context(&cx, &mut HeaderInjector(req.headers_mut()));
    });

    let response = client.execute(req).await?;
    Ok(response.text().await?)
}
```

**Service B (Server with Axum)**:

```rust
use axum::{http::Request, middleware::Next, response::Response};
use opentelemetry::global;
use opentelemetry_http::HeaderExtractor;

// Middleware to extract trace context
async fn extract_trace_context<B>(
    req: Request<B>,
    next: Next<B>,
) -> Response {
    let cx = global::get_text_map_propagator(|propagator| {
        propagator.extract(&HeaderExtractor(req.headers()))
    });

    // Attach context to current scope
    let _guard = cx.attach();

    next.run(req).await
}

// Apply middleware
let app = Router::new()
    .route("/api/data", get(handler))
    .layer(axum::middleware::from_fn(extract_trace_context));
```

**With tracing crate** (automatic):

```rust
use tower_http::trace::TraceLayer;

// TraceLayer automatically propagates trace context
let app = Router::new()
    .route("/api/data", get(handler))
    .layer(TraceLayer::new_for_http());
```

### Go (net/http)

**Service A (Client)**:

```go
import (
    "net/http"
    "go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
)

func callServiceB(ctx context.Context) (string, error) {
    // Use otelhttp.NewTransport for automatic propagation
    client := &http.Client{
        Transport: otelhttp.NewTransport(http.DefaultTransport),
    }

    req, err := http.NewRequestWithContext(ctx, "GET", "http://service-b:3000/api/data", nil)
    if err != nil {
        return "", err
    }

    resp, err := client.Do(req)
    if err != nil {
        return "", err
    }
    defer resp.Body.Close()

    // Read response...
}
```

**Service B (Server)**:

```go
import (
    "net/http"
    "go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
)

func main() {
    // Wrap handler with otelhttp
    handler := otelhttp.NewHandler(http.HandlerFunc(getData), "api-data")
    http.ListenAndServe(":3000", handler)
}

func getData(w http.ResponseWriter, r *http.Request) {
    // Trace context automatically extracted from headers
    ctx := r.Context()

    // Create child span
    _, span := tracer.Start(ctx, "fetch_data")
    defer span.End()

    // ...
}
```

### TypeScript (fetch + Express)

**Service A (Client)**:

```typescript
import { trace, context, propagation } from '@opentelemetry/api';

async function callServiceB(): Promise<any> {
  const headers: Record<string, string> = {};

  // Inject trace context into headers
  propagation.inject(context.active(), headers);

  const response = await fetch('http://service-b:3000/api/data', {
    headers,
  });

  return response.json();
}
```

**Service B (Server with Express)**:

```typescript
import express from 'express';
import { trace, context, propagation } from '@opentelemetry/api';

const app = express();

// Middleware to extract trace context
app.use((req, res, next) => {
  const ctx = propagation.extract(context.active(), req.headers);
  context.with(ctx, next);
});

app.get('/api/data', (req, res) => {
  // Trace context automatically available
  const span = trace.getActiveSpan();
  res.json({ data: 'value' });
});
```

---

## Message Queues

### Kafka (Python)

**Producer**:

```python
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_message(topic: str, data: dict):
    # Inject trace context into message headers
    carrier = {}
    TraceContextTextMapPropagator().inject(carrier)

    message = {
        "data": data,
        "trace_context": carrier  # Include trace context in message
    }

    producer.send(topic, value=message)
```

**Consumer**:

```python
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry import trace
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'my-topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

tracer = trace.get_tracer(__name__)

for message in consumer:
    payload = message.value

    # Extract trace context from message
    ctx = TraceContextTextMapPropagator().extract(payload.get("trace_context", {}))

    # Continue trace in consumer
    with tracer.start_as_current_span("process_kafka_message", context=ctx) as span:
        span.set_attribute("topic", message.topic)
        span.set_attribute("partition", message.partition)

        # Process message...
        process_data(payload["data"])
```

### RabbitMQ (Python)

**Producer**:

```python
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

def publish_message(queue: str, data: dict):
    # Inject trace context
    carrier = {}
    TraceContextTextMapPropagator().inject(carrier)

    # Add trace context to message properties
    properties = pika.BasicProperties(
        headers=carrier,
        content_type='application/json'
    )

    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(data),
        properties=properties
    )
```

**Consumer**:

```python
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry import trace
import pika

tracer = trace.get_tracer(__name__)

def callback(ch, method, properties, body):
    # Extract trace context from message headers
    carrier = properties.headers or {}
    ctx = TraceContextTextMapPropagator().extract(carrier)

    # Continue trace
    with tracer.start_as_current_span("process_rabbitmq_message", context=ctx) as span:
        data = json.loads(body)
        span.set_attribute("queue", method.routing_key)

        # Process message...
        process_data(data)

channel.basic_consume(queue='my-queue', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
```

---

## Background Jobs

### Celery (Python)

**Task Producer**:

```python
from celery import Celery
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def process_data(data, trace_context=None):
    # Extract trace context
    if trace_context:
        ctx = TraceContextTextMapPropagator().extract(trace_context)
    else:
        ctx = None

    with tracer.start_as_current_span("celery_task", context=ctx) as span:
        # Process data...
        result = perform_computation(data)
        return result

def enqueue_task(data):
    # Inject trace context
    carrier = {}
    TraceContextTextMapPropagator().inject(carrier)

    # Pass trace context to task
    process_data.delay(data, trace_context=carrier)
```

### Background Thread (Rust)

**Spawning Background Task**:

```rust
use opentelemetry::global;
use opentelemetry::trace::TraceContextExt;
use tokio::spawn;

async fn enqueue_background_job(data: String) {
    // Capture current trace context
    let cx = opentelemetry::Context::current();

    // Spawn background task with context
    spawn(async move {
        // Attach trace context to background task
        let _guard = cx.attach();

        // Create child span
        let tracer = global::tracer("background-job");
        let span = tracer.start("process_background_job");
        let _cx = opentelemetry::Context::current_with_span(span);

        // Process data...
        process_data(&data).await;
    });
}
```

### Tokio Spawn (Rust)

```rust
use tracing::{info, instrument, Instrument};

#[instrument]
async fn spawn_background_task(user_id: u64) {
    // Capture current span
    let span = tracing::Span::current();

    tokio::spawn(
        async move {
            // This task inherits the trace context
            info!(user_id = user_id, "background task started");

            // Process...
            process_user_data(user_id).await;

            info!(user_id = user_id, "background task completed");
        }
        .instrument(span)  // Attach span to spawned task
    );
}
```

---

## Database Calls

### SQL (Python + SQLAlchemy)

**Auto-Instrumentation**:

```python
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

engine = create_engine("postgresql://...")
SQLAlchemyInstrumentor().instrument(engine=engine)

# All SQL queries now automatically traced
async with engine.begin() as conn:
    result = await conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
    # Span created: db.statement = "SELECT * FROM users WHERE id = $1"
```

### SQL (Rust + sqlx)

**Manual Instrumentation**:

```rust
use tracing::{info, instrument};
use sqlx::PgPool;

#[instrument(skip(pool))]
async fn fetch_user(pool: &PgPool, user_id: i64) -> Result<User, sqlx::Error> {
    // tracing automatically includes trace context
    info!(user_id = user_id, "executing SQL query");

    let user = sqlx::query_as::<_, User>("SELECT * FROM users WHERE id = $1")
        .bind(user_id)
        .fetch_one(pool)
        .await?;

    info!(user_id = user_id, user_found = true, "query completed");
    Ok(user)
}
```

### Redis (TypeScript)

```typescript
import { trace, context } from '@opentelemetry/api';
import Redis from 'ioredis';

const redis = new Redis();
const tracer = trace.getTracer('redis-client');

async function getFromCache(key: string): Promise<string | null> {
  const span = tracer.startSpan('redis.get');
  span.setAttribute('db.system', 'redis');
  span.setAttribute('db.operation', 'GET');
  span.setAttribute('db.key', key);

  try {
    const value = await redis.get(key);
    span.setStatus({ code: SpanStatusCode.OK });
    return value;
  } catch (error) {
    span.recordException(error as Error);
    span.setStatus({ code: SpanStatusCode.ERROR });
    throw error;
  } finally {
    span.end();
  }
}
```

---

## Cross-Language Propagation

### Python → Rust

**Python Service (Upstream)**:

```python
import httpx
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

HTTPXClientInstrumentor().instrument()

async def call_rust_service():
    async with httpx.AsyncClient() as client:
        # Automatically injects W3C Trace Context headers
        response = await client.get("http://rust-service:3000/api/process")
        return response.json()
```

**Rust Service (Downstream)**:

```rust
use axum::{routing::get, Router};
use tower_http::trace::TraceLayer;

#[tokio::main]
async fn main() {
    // TraceLayer automatically extracts W3C Trace Context
    let app = Router::new()
        .route("/api/process", get(process_handler))
        .layer(TraceLayer::new_for_http());

    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn process_handler() -> &'static str {
    // Trace context automatically propagated from Python service
    "processed"
}
```

### Go → TypeScript

**Go Service (Upstream)**:

```go
import (
    "net/http"
    "go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
)

func callTypeScriptService(ctx context.Context) (string, error) {
    client := &http.Client{
        Transport: otelhttp.NewTransport(http.DefaultTransport),
    }

    req, _ := http.NewRequestWithContext(ctx, "GET", "http://ts-service:3000/api/data", nil)
    resp, err := client.Do(req)
    // W3C Trace Context automatically injected
}
```

**TypeScript Service (Downstream)**:

```typescript
import express from 'express';
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';

// Auto-instrumentation extracts W3C Trace Context
const sdk = new NodeSDK({
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();

const app = express();

app.get('/api/data', (req, res) => {
  // Trace context automatically extracted from Go service
  res.json({ data: 'value' });
});
```

---

## Baggage Propagation

**Use baggage to propagate custom context** (user_id, tenant_id, etc.):

### Python

```python
from opentelemetry import baggage, context

# Set baggage
ctx = baggage.set_baggage("user.id", str(user_id))
ctx = baggage.set_baggage("tenant.id", tenant_id)

# Propagates to all downstream services via W3C Baggage header
with context.attach(ctx):
    await call_downstream_service()

# In downstream service
user_id = baggage.get_baggage("user.id")
logger.info("processing request", user_id=user_id)
```

### Rust

```rust
use opentelemetry::baggage::BaggageExt;
use opentelemetry::Context;

let cx = Context::current()
    .with_baggage(vec![
        ("user.id".to_string(), user_id.to_string()),
        ("tenant.id".to_string(), tenant_id.to_string()),
    ]);

let _guard = cx.attach();

// Baggage propagates to downstream services
call_downstream_service().await;
```

---

## Validation

**Check trace propagation**:

```bash
# 1. Make request to Service A
curl http://localhost:3000/api/proxy

# 2. Check Tempo for trace
# Navigate to Grafana → Explore → Tempo
# Search for service.name = "service-a"

# 3. Verify both Service A and Service B appear in trace
# Trace should show:
# └─ service-a: /api/proxy
#    └─ service-b: /api/data
```

**Debug propagation issues**:

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check injected headers
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

carrier = {}
TraceContextTextMapPropagator().inject(carrier)
print("Injected headers:", carrier)
# Output: {'traceparent': '00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01'}
```

---

## Best Practices

1. **Use auto-instrumentation first** - Manual propagation is error-prone
2. **Always propagate in async contexts** - Use `.instrument()` (Rust) or context managers (Python)
3. **Test cross-service traces** - Verify end-to-end trace visibility
4. **Use baggage sparingly** - High cardinality data bloats headers
5. **Monitor propagation failures** - Alert on orphaned spans (no parent)
6. **Version compatibility** - W3C Trace Context is backwards compatible

---

## Troubleshooting

**Traces appear disconnected (no parent-child relationship)**:
- Verify auto-instrumentation is enabled on both services
- Check HTTP client propagates `traceparent` header
- Ensure server extracts `traceparent` from headers

**Baggage not propagating**:
- Verify W3C Baggage propagator is configured
- Check header size limits (default: 8KB)
- Reduce baggage cardinality

**Context lost in async code**:
- Python: Use `contextvars` or `asyncio` task context
- Rust: Use `.instrument(span)` on spawned tasks
- Go: Pass `context.Context` explicitly
- TypeScript: Use `context.with()` or async hooks
