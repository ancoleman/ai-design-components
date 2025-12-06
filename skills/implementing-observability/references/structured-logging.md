# Structured Logging with OpenTelemetry Context

Complete guide for structured logging with trace context injection across Python, Rust, Go, and TypeScript.

## Table of Contents

- [Why Structured Logging](#why-structured-logging)
- [Python (structlog)](#python-structlog)
- [Rust (tracing)](#rust-tracing)
- [Go (slog)](#go-slog)
- [TypeScript (pino)](#typescript-pino)
- [Log Correlation Patterns](#log-correlation-patterns)

---

## Why Structured Logging

**Traditional logging (BAD)**:
```
2025-12-02 10:15:23 INFO User 12345 logged in from 192.168.1.100
```

**Problems**:
- String parsing required to extract fields
- No standard format
- Cannot correlate with traces
- Difficult to query

**Structured logging (GOOD)**:
```json
{
  "timestamp": "2025-12-02T10:15:23.456Z",
  "level": "info",
  "message": "user_logged_in",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "user_id": 12345,
  "ip_address": "192.168.1.100",
  "service": "auth-service"
}
```

**Benefits**:
- Machine-readable (JSON)
- Easy to query in Loki: `{service="auth-service"} | json | user_id=12345`
- Trace correlation via trace_id
- Consistent field names

---

## Python (structlog)

### Installation

```bash
pip install structlog
```

### Basic Configuration

```python
# logging_config.py
import structlog
from opentelemetry import trace

def otel_processor(logger, log_method, event_dict):
    """Processor to inject OpenTelemetry context."""
    span = trace.get_current_span()
    if span.is_recording():
        ctx = span.get_span_context()
        event_dict["trace_id"] = format(ctx.trace_id, '032x')
        event_dict["span_id"] = format(ctx.span_id, '016x')
        event_dict["trace_flags"] = ctx.trace_flags
    return event_dict

def configure_logging():
    """Configure structlog with OpenTelemetry integration."""
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            otel_processor,  # Inject trace context
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
```

### Usage

```python
# main.py
import structlog
from logging_config import configure_logging

configure_logging()
logger = structlog.get_logger()

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    # Automatic trace context injection
    logger.info(
        "processing_request",
        user_id=user_id,
        endpoint="/api/users"
    )

    try:
        user = await fetch_user(user_id)
        logger.info(
            "request_completed",
            user_id=user_id,
            user_found=user is not None
        )
        return user
    except Exception as e:
        logger.error(
            "request_failed",
            user_id=user_id,
            error=str(e),
            exc_info=True
        )
        raise
```

### Context Binding

**Bind context for entire request scope**:

```python
from contextvars import ContextVar
import structlog

# Context variable for request-scoped logging
request_context: ContextVar[dict] = ContextVar("request_context", default={})

@app.middleware("http")
async def bind_request_context(request: Request, call_next):
    """Middleware to bind request context to logs."""
    context = {
        "request_id": str(uuid.uuid4()),
        "method": request.method,
        "path": request.url.path,
        "client_ip": request.client.host,
    }
    request_context.set(context)

    # Bind context to logger
    logger = structlog.get_logger()
    logger = logger.bind(**context)

    # Process request
    response = await call_next(request)

    logger.info(
        "request_completed",
        status_code=response.status_code,
        duration_ms=response.headers.get("X-Process-Time")
    )

    return response
```

### Advanced: Custom Processors

```python
import structlog

def drop_debug_logs(logger, log_method, event_dict):
    """Drop DEBUG logs in production."""
    if event_dict.get("log_level") == "debug" and not DEBUG:
        raise structlog.DropEvent
    return event_dict

def redact_sensitive_fields(logger, log_method, event_dict):
    """Redact sensitive information."""
    sensitive_keys = {"password", "token", "secret", "api_key"}
    for key in sensitive_keys:
        if key in event_dict:
            event_dict[key] = "***REDACTED***"
    return event_dict

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        redact_sensitive_fields,  # Redact first
        drop_debug_logs,          # Then filter
        otel_processor,
        structlog.processors.JSONRenderer()
    ]
)
```

---

## Rust (tracing)

### Installation (Cargo.toml)

```toml
[dependencies]
tracing = "0.1.40"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
tracing-opentelemetry = "0.22"
opentelemetry = "0.21"
```

### Basic Configuration

```rust
// src/logging.rs
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt, EnvFilter};

pub fn init_logging() -> Result<(), Box<dyn std::error::Error>> {
    // OTLP tracer (from opentelemetry-setup.md)
    let tracer = init_otel_tracer("my-service")?;

    // Configure tracing-subscriber
    tracing_subscriber::registry()
        .with(EnvFilter::from_default_env())
        .with(tracing_subscriber::fmt::layer().json())  // JSON output
        .with(tracing_opentelemetry::layer().with_tracer(tracer))
        .init();

    Ok(())
}
```

### Usage with #[instrument]

```rust
use tracing::{info, warn, error, instrument};

#[instrument(
    skip(db_pool),
    fields(
        user_id = %user_id,
        otel.kind = "server"
    )
)]
async fn get_user(user_id: u64, db_pool: &PgPool) -> Result<User, AppError> {
    // trace_id and span_id automatically included in logs
    info!(user_id = user_id, "processing request");

    match fetch_user_from_db(user_id, db_pool).await {
        Ok(user) => {
            info!(user_id = user_id, user_found = true, "request completed");
            Ok(user)
        }
        Err(e) => {
            error!(
                user_id = user_id,
                error = %e,
                "failed to fetch user"
            );
            Err(e.into())
        }
    }
}
```

**Key Features**:
- `#[instrument]` automatically creates a span
- All `info!`, `warn!`, `error!` logs inside the function inherit trace context
- Zero boilerplate for trace context injection

### Manual Spans

```rust
use tracing::{info_span, info};

async fn process_payment(amount: f64, user_id: u64) -> Result<PaymentResult> {
    let span = info_span!(
        "process_payment",
        user_id = user_id,
        amount = amount,
        payment_id = tracing::field::Empty  // Fill later
    );

    let _enter = span.enter();

    info!(amount = amount, "initiating payment");

    let payment_id = generate_payment_id();
    span.record("payment_id", &payment_id);

    // Process payment...
    info!(payment_id = %payment_id, "payment processed");

    Ok(PaymentResult { payment_id })
}
```

### Structured Fields

```rust
use tracing::info;
use serde::Serialize;

#[derive(Serialize)]
struct PaymentDetails {
    amount: f64,
    currency: String,
    method: String,
}

#[instrument(skip(details))]
async fn log_payment(user_id: u64, details: PaymentDetails) {
    // Structured field with serde
    info!(
        user_id = user_id,
        payment = ?details,  // Debug format (uses serde)
        "payment logged"
    );
}
```

---

## Go (slog)

### Standard Library (Go 1.21+)

```go
// internal/logging/logging.go
package logging

import (
    "context"
    "log/slog"
    "os"

    "go.opentelemetry.io/otel/trace"
)

// OTelHandler wraps slog.Handler to inject trace context
type OTelHandler struct {
    handler slog.Handler
}

func NewOTelHandler(handler slog.Handler) *OTelHandler {
    return &OTelHandler{handler: handler}
}

func (h *OTelHandler) Enabled(ctx context.Context, level slog.Level) bool {
    return h.handler.Enabled(ctx, level)
}

func (h *OTelHandler) Handle(ctx context.Context, r slog.Record) error {
    // Extract trace context
    span := trace.SpanFromContext(ctx)
    if span.SpanContext().IsValid() {
        spanCtx := span.SpanContext()
        r.AddAttrs(
            slog.String("trace_id", spanCtx.TraceID().String()),
            slog.String("span_id", spanCtx.SpanID().String()),
            slog.Int("trace_flags", int(spanCtx.TraceFlags())),
        )
    }

    return h.handler.Handle(ctx, r)
}

func (h *OTelHandler) WithAttrs(attrs []slog.Attr) slog.Handler {
    return &OTelHandler{handler: h.handler.WithAttrs(attrs)}
}

func (h *OTelHandler) WithGroup(name string) slog.Handler {
    return &OTelHandler{handler: h.handler.WithGroup(name)}
}

// InitLogger initializes slog with OTel integration
func InitLogger() {
    // JSON handler
    jsonHandler := slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
        Level: slog.LevelInfo,
    })

    // Wrap with OTel handler
    otelHandler := NewOTelHandler(jsonHandler)

    // Set as default logger
    logger := slog.New(otelHandler)
    slog.SetDefault(logger)
}
```

### Usage

```go
package main

import (
    "context"
    "log/slog"

    "myapp/internal/logging"
)

func main() {
    logging.InitLogger()

    // ... initialize OpenTelemetry tracer ...

    http.HandleFunc("/api/users/", handleGetUser)
    http.ListenAndServe(":3000", nil)
}

func handleGetUser(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()

    userID := extractUserID(r)

    // Automatic trace context injection via custom handler
    slog.InfoContext(ctx, "processing request",
        slog.Int64("user_id", userID),
        slog.String("endpoint", r.URL.Path),
    )

    user, err := fetchUser(ctx, userID)
    if err != nil {
        slog.ErrorContext(ctx, "failed to fetch user",
            slog.Int64("user_id", userID),
            slog.String("error", err.Error()),
        )
        http.Error(w, "Internal Server Error", 500)
        return
    }

    slog.InfoContext(ctx, "request completed",
        slog.Int64("user_id", userID),
        slog.Bool("user_found", user != nil),
    )

    respondJSON(w, user)
}
```

### Context-Bound Loggers

```go
// Bind logger with request-scoped context
func middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        requestID := uuid.New().String()

        // Create logger with request context
        logger := slog.With(
            slog.String("request_id", requestID),
            slog.String("method", r.Method),
            slog.String("path", r.URL.Path),
        )

        // Store in context
        ctx := context.WithValue(r.Context(), "logger", logger)
        r = r.WithContext(ctx)

        next.ServeHTTP(w, r)
    })
}

// Usage
func handler(w http.ResponseWriter, r *http.Request) {
    logger := r.Context().Value("logger").(*slog.Logger)
    logger.Info("handling request")
}
```

---

## TypeScript (pino)

### Installation

```bash
npm install pino pino-pretty @opentelemetry/api
```

### Configuration

```typescript
// src/logger.ts
import pino from 'pino';
import { trace, context } from '@opentelemetry/api';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level(label) {
      return { level: label };
    },
  },
  mixin() {
    // Inject OpenTelemetry context
    const span = trace.getActiveSpan();
    if (!span) return {};

    const spanContext = span.spanContext();
    return {
      trace_id: spanContext.traceId,
      span_id: spanContext.spanId,
      trace_flags: spanContext.traceFlags,
    };
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});

export default logger;
```

### Usage

```typescript
// src/handlers/users.ts
import logger from '../logger';

export async function getUser(req: Request, res: Response) {
  const userId = parseInt(req.params.userId);

  // Automatic trace context via mixin
  logger.info({ user_id: userId, endpoint: req.path }, 'processing request');

  try {
    const user = await fetchUser(userId);

    logger.info(
      { user_id: userId, user_found: user !== null },
      'request completed'
    );

    res.json(user);
  } catch (error) {
    logger.error(
      { user_id: userId, error: error.message, stack: error.stack },
      'request failed'
    );
    res.status(500).json({ error: 'Internal Server Error' });
  }
}
```

### Child Loggers (Context Binding)

```typescript
import pino from 'pino';
import { v4 as uuidv4 } from 'uuid';

const logger = pino();

// Middleware to create request-scoped logger
app.use((req, res, next) => {
  const requestId = uuidv4();

  // Create child logger with request context
  req.log = logger.child({
    request_id: requestId,
    method: req.method,
    path: req.path,
    ip: req.ip,
  });

  next();
});

// Usage in route handlers
app.get('/api/users/:userId', (req, res) => {
  req.log.info({ user_id: req.params.userId }, 'processing request');
  // ...
});
```

### Redacting Sensitive Fields

```typescript
const logger = pino({
  redact: {
    paths: ['password', 'token', 'secret', 'api_key', '*.password'],
    censor: '***REDACTED***',
  },
});

logger.info({ username: 'alice', password: 'secret123' }, 'user logged in');
// Output: {"username":"alice","password":"***REDACTED***","msg":"user logged in"}
```

---

## Log Correlation Patterns

### Pattern 1: Trace ID in Error Messages

**Python**:
```python
from opentelemetry import trace

span = trace.get_current_span()
trace_id = format(span.get_span_context().trace_id, '032x')

return JSONResponse(
    status_code=500,
    content={
        "error": "Internal Server Error",
        "trace_id": trace_id  # Return to client for support
    }
)
```

**Frontend can now reference trace_id when reporting bugs**:
```typescript
console.error('API error, trace_id:', response.trace_id);
// User reports: "Error occurred, trace_id: 4bf92f3577b34da6a3ce929d0e0e4736"
```

### Pattern 2: Querying Logs by Trace ID

**Loki (LogQL)**:
```promql
# Find all logs for a specific trace
{job="api-service"} | json | trace_id="4bf92f3577b34da6a3ce929d0e0e4736"

# Find traces with errors, then view logs
{job="api-service"} | json | level="error" | trace_id=~".+"
```

### Pattern 3: Jump from Trace to Logs in Grafana

**In Grafana Tempo**:
1. View trace for request
2. Click "Logs for this span" button
3. Grafana automatically queries Loki with trace_id filter
4. See all logs correlated with the trace

**Configure in Grafana datasource**:
```yaml
# datasources.yaml
apiVersion: 1
datasources:
  - name: Tempo
    type: tempo
    uid: tempo
    url: http://tempo:3200
    jsonData:
      tracesToLogsV2:
        datasourceUid: loki
        filterByTraceID: true
        filterBySpanID: true
        tags: ['job', 'instance']
```

### Pattern 4: Baggage Propagation

**Use OpenTelemetry Baggage to propagate user context**:

```python
from opentelemetry import baggage, context

# Set baggage in request handler
ctx = baggage.set_baggage("user.id", str(user_id))
ctx = baggage.set_baggage("user.role", user_role)

# Propagates to all downstream services and logs
with context.attach(ctx):
    await process_request()

# In logs
user_id = baggage.get_baggage("user.id")
logger.info("processing", user_id=user_id)
```

---

## Comparison Matrix

| Language   | Logger   | Trace Injection | Performance | Ease of Use | Context Binding |
|------------|----------|-----------------|-------------|-------------|-----------------|
| **Python** | structlog | Manual processor | Medium | ⭐⭐⭐⭐ | ContextVar |
| **Rust**   | tracing | Automatic | High | ⭐⭐⭐⭐⭐ | Span scope |
| **Go**     | slog | Custom handler | High | ⭐⭐⭐ | Context.Value |
| **TypeScript** | pino | Mixin function | High | ⭐⭐⭐⭐ | Child loggers |

**Recommendation by Language**:
- **Python**: structlog (most flexible, extensive ecosystem)
- **Rust**: tracing (zero-boilerplate, native async)
- **Go**: slog (stdlib, no dependencies, fast)
- **TypeScript**: pino (fastest Node.js logger)

---

## Best Practices

1. **Always inject trace context** - Every log should include trace_id when available
2. **Use structured fields** - JSON format, consistent field names
3. **Bind request context** - User ID, request ID should be in all logs
4. **Redact sensitive data** - Never log passwords, tokens, API keys
5. **Use log levels appropriately**:
   - DEBUG: Development only
   - INFO: Normal operations
   - WARN: Recoverable errors
   - ERROR: Unrecoverable errors
6. **Include error stack traces** - Use exc_info=True (Python) or error formatting
7. **Test log correlation** - Verify trace_id appears in both logs and traces

---

## Troubleshooting

**Trace context not appearing in logs**:
- Verify OpenTelemetry SDK is initialized BEFORE logger
- Check that logger configuration includes OTel processor/mixin
- Ensure logs are emitted within a span context

**JSON logs not parsing in Loki**:
- Verify JSON is valid (use `jq` to test)
- Check Loki pipeline configuration for JSON parsing
- Ensure timestamp field is ISO 8601 format

**Performance degradation**:
- Disable DEBUG logs in production
- Use async logging (pino, structlog async mode)
- Batch log exports to reduce I/O
