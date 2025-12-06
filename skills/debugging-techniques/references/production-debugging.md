# Production Debugging Reference

## Table of Contents

1. [Production Debugging Principles](#production-debugging-principles)
2. [Structured Logging](#structured-logging)
3. [Correlation IDs](#correlation-ids)
4. [Distributed Tracing](#distributed-tracing)
5. [Error Tracking](#error-tracking)
6. [Production Debugging Workflow](#production-debugging-workflow)
7. [Anti-Patterns](#anti-patterns)
8. [Best Practices Summary](#best-practices-summary)

## Production Debugging Principles

### Golden Rules

1. **Minimal performance impact** - Profile overhead, limit scope
2. **No blocking operations** - Use non-breaking techniques
3. **Security-aware** - Avoid logging secrets, PII
4. **Reversible** - Can roll back quickly (feature flags, Git)
5. **Observable** - Structured logging, correlation IDs, tracing

### Safety Checklist

Before debugging in production:
- [ ] Will this impact performance? (Profile overhead)
- [ ] Will this block users? (Use non-breaking techniques)
- [ ] Could this expose secrets? (Avoid variable dumps)
- [ ] Is there a rollback plan? (Git branch, feature flag)
- [ ] Have we tried logs first? (Less invasive)
- [ ] Do we have correlation IDs? (Trace requests)
- [ ] Is error tracking enabled? (Sentry, New Relic)
- [ ] Can we reproduce in staging? (Safer environment)

## Structured Logging

### Python Example

```python
import logging
import json
from datetime import datetime

# Configure structured logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_order(order_id, user_id, correlation_id):
    logger.info(json.dumps({
        "timestamp": datetime.utcnow().isoformat(),
        "event": "order_processing_started",
        "order_id": order_id,
        "user_id": user_id,
        "correlation_id": correlation_id,
        "service": "order-service"
    }))

    try:
        # Process order
        result = process_payment(order_id)

        logger.info(json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "event": "order_processing_completed",
            "order_id": order_id,
            "correlation_id": correlation_id,
            "result": "success"
        }))
    except Exception as e:
        logger.error(json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "event": "order_processing_failed",
            "order_id": order_id,
            "correlation_id": correlation_id,
            "error": str(e),
            "error_type": type(e).__name__
        }))
        raise
```

### Go Example

```go
package main

import (
    "encoding/json"
    "log"
    "time"
)

type LogEntry struct {
    Timestamp     time.Time `json:"timestamp"`
    Event         string    `json:"event"`
    OrderID       string    `json:"order_id"`
    CorrelationID string    `json:"correlation_id"`
    Service       string    `json:"service"`
    Level         string    `json:"level"`
}

func logStructured(entry LogEntry) {
    entry.Timestamp = time.Now().UTC()
    entry.Service = "order-service"
    jsonData, _ := json.Marshal(entry)
    log.Println(string(jsonData))
}

func processOrder(orderID, correlationID string) error {
    logStructured(LogEntry{
        Event:         "order_processing_started",
        OrderID:       orderID,
        CorrelationID: correlationID,
        Level:         "info",
    })

    // Process order

    logStructured(LogEntry{
        Event:         "order_processing_completed",
        OrderID:       orderID,
        CorrelationID: correlationID,
        Level:         "info",
    })

    return nil
}
```

### Node.js Example

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  format: winston.format.json(),
  transports: [
    new winston.transports.Console()
  ]
});

function processOrder(orderId, userId, correlationId) {
  logger.info({
    timestamp: new Date().toISOString(),
    event: 'order_processing_started',
    order_id: orderId,
    user_id: userId,
    correlation_id: correlationId,
    service: 'order-service'
  });

  try {
    // Process order

    logger.info({
      timestamp: new Date().toISOString(),
      event: 'order_processing_completed',
      order_id: orderId,
      correlation_id: correlationId,
      result: 'success'
    });
  } catch (error) {
    logger.error({
      timestamp: new Date().toISOString(),
      event: 'order_processing_failed',
      order_id: orderId,
      correlation_id: correlationId,
      error: error.message,
      stack: error.stack
    });
    throw error;
  }
}
```

## Correlation IDs

### What Are Correlation IDs?

Unique identifiers that track a single request across multiple services.

**Benefits:**
- Trace request flow across microservices
- Find all logs for a specific request
- Debug distributed system failures
- Understand request timeline

### Implementation Patterns

#### HTTP Headers

**Standard headers:**
- `X-Correlation-ID`
- `X-Request-ID`
- `X-Trace-ID`

#### Python (Flask Example)

```python
from flask import Flask, request, g
import uuid

app = Flask(__name__)

@app.before_request
def before_request():
    # Get or generate correlation ID
    correlation_id = request.headers.get('X-Correlation-ID')
    if not correlation_id:
        correlation_id = str(uuid.uuid4())

    # Store in request context
    g.correlation_id = correlation_id

@app.after_request
def after_request(response):
    # Add to response headers
    response.headers['X-Correlation-ID'] = g.correlation_id
    return response

@app.route('/api/orders', methods=['POST'])
def create_order():
    correlation_id = g.correlation_id

    logger.info({
        "event": "order_created",
        "correlation_id": correlation_id,
        "data": request.json
    })

    # Pass correlation ID to downstream services
    response = requests.post(
        'http://payment-service/pay',
        headers={'X-Correlation-ID': correlation_id},
        json=request.json
    )

    return jsonify({"order_id": "123", "correlation_id": correlation_id})
```

#### Go (HTTP Middleware)

```go
package main

import (
    "context"
    "github.com/google/uuid"
    "net/http"
)

type contextKey string

const correlationIDKey contextKey = "correlationID"

func correlationIDMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        correlationID := r.Header.Get("X-Correlation-ID")
        if correlationID == "" {
            correlationID = uuid.New().String()
        }

        // Add to response
        w.Header().Set("X-Correlation-ID", correlationID)

        // Add to context
        ctx := context.WithValue(r.Context(), correlationIDKey, correlationID)

        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

func handler(w http.ResponseWriter, r *http.Request) {
    correlationID := r.Context().Value(correlationIDKey).(string)

    logStructured(LogEntry{
        Event:         "request_received",
        CorrelationID: correlationID,
    })

    // Make downstream request
    req, _ := http.NewRequest("POST", "http://payment-service/pay", nil)
    req.Header.Set("X-Correlation-ID", correlationID)
    client := &http.Client{}
    client.Do(req)
}
```

#### Node.js (Express Middleware)

```javascript
const express = require('express');
const { v4: uuidv4 } = require('uuid');

const app = express();

// Correlation ID middleware
app.use((req, res, next) => {
  const correlationId = req.headers['x-correlation-id'] || uuidv4();

  // Add to request
  req.correlationId = correlationId;

  // Add to response
  res.setHeader('X-Correlation-ID', correlationId);

  next();
});

app.post('/api/orders', async (req, res) => {
  const { correlationId } = req;

  logger.info({
    event: 'order_created',
    correlation_id: correlationId,
    data: req.body
  });

  // Pass to downstream service
  await axios.post('http://payment-service/pay', req.body, {
    headers: { 'X-Correlation-ID': correlationId }
  });

  res.json({ order_id: '123', correlation_id: correlationId });
});
```

## Distributed Tracing

### OpenTelemetry Integration

#### Python Example

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# Setup tracing
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name='localhost',
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)

def process_order(order_id):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        span.add_event("Order validation started")

        # Validation
        validate_order(order_id)
        span.add_event("Order validated")

        # Payment
        process_payment(order_id)
        span.add_event("Payment processed")

        # Fulfillment
        fulfill_order(order_id)
        span.add_event("Order fulfilled")

        span.set_status(trace.Status(trace.StatusCode.OK))

def validate_order(order_id):
    with tracer.start_as_current_span("validate_order") as span:
        span.set_attribute("order.id", order_id)
        # Validation logic
```

#### Go Example

```go
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/trace"
)

func processOrder(ctx context.Context, orderID string) error {
    tracer := otel.Tracer("order-service")
    ctx, span := tracer.Start(ctx, "process_order")
    defer span.End()

    span.SetAttributes(attribute.String("order.id", orderID))
    span.AddEvent("Order processing started")

    // Validation
    if err := validateOrder(ctx, orderID); err != nil {
        span.RecordError(err)
        return err
    }
    span.AddEvent("Order validated")

    // Payment
    if err := processPayment(ctx, orderID); err != nil {
        span.RecordError(err)
        return err
    }
    span.AddEvent("Payment processed")

    return nil
}
```

## Error Tracking

### Sentry Integration

#### Python Example

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://your-dsn@sentry.io/project",
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.1,  # 10% of transactions
    environment="production"
)

def process_order(order_id):
    try:
        # Process order
        result = risky_operation()
    except Exception as e:
        # Automatically captured by Sentry
        # Or manually capture with context:
        sentry_sdk.capture_exception(e)
        sentry_sdk.set_context("order", {
            "order_id": order_id,
            "status": "failed"
        })
        raise
```

#### Node.js Example

```javascript
const Sentry = require('@sentry/node');

Sentry.init({
  dsn: 'https://your-dsn@sentry.io/project',
  tracesSampleRate: 0.1,
  environment: 'production'
});

async function processOrder(orderId) {
  try {
    await riskyOperation();
  } catch (error) {
    Sentry.captureException(error, {
      tags: {
        order_id: orderId
      },
      contexts: {
        order: {
          id: orderId,
          status: 'failed'
        }
      }
    });
    throw error;
  }
}
```

## Production Debugging Workflow

### Step 1: Detect

**Monitoring alerts:**
- Error tracking platform (Sentry)
- Log aggregation (ELK, Splunk)
- Metrics spike (Prometheus)
- APM alerts (New Relic, Datadog)

### Step 2: Locate

**Find correlation ID:**
```bash
# In Sentry
# Copy correlation_id from error report

# In ELK/Kibana
correlation_id:"abc-123-def-456"

# In Datadog
@correlation_id:abc-123-def-456
```

**Search logs:**
```bash
# Grep logs
grep "abc-123-def-456" /var/log/app/*.log

# Or in log aggregation tool
# Trace entire request flow
```

**View distributed trace:**
```bash
# In Jaeger UI
# Search by correlation ID
# View span timeline
# Identify slow/failed services
```

### Step 3: Reproduce

**In staging environment:**
```bash
# Use production data (sanitized)
# Trigger same request flow
# Add additional logging if needed
```

### Step 4: Fix

**Feature flag for gradual rollout:**
```python
from flagsmith import Flagsmith

flagsmith = Flagsmith(environment_key='your-key')

if flagsmith.has_feature('new-order-logic'):
    # New logic
    process_order_v2(order_id)
else:
    # Old logic
    process_order_v1(order_id)
```

**Canary deployment:**
```yaml
# Kubernetes
apiVersion: v1
kind: Service
metadata:
  name: order-service
spec:
  selector:
    app: order-service
    version: stable  # 90% of traffic

---
apiVersion: v1
kind: Service
metadata:
  name: order-service-canary
spec:
  selector:
    app: order-service
    version: canary  # 10% of traffic
```

### Step 5: Verify

**Monitor error rates:**
```bash
# In Sentry
# Check error count decrease

# In Prometheus
rate(http_errors_total[5m])

# In logs
# Search for correlation IDs with errors
```

## Anti-Patterns

### DON'T DO These

**1. Use interactive debuggers in production**
```python
# NEVER
breakpoint()  # Blocks all requests!
```

**2. Log sensitive data**
```python
# BAD
logger.info(f"User password: {password}")
logger.info(f"Credit card: {card_number}")

# GOOD
logger.info(f"User authenticated: {user_id}")
logger.info(f"Payment processed: {order_id}")
```

**3. Add excessive logging**
```python
# BAD (performance impact)
for item in items:
    logger.info(f"Processing item: {item}")  # Logs millions of times
```

**4. Deploy untested fixes**
```bash
# BAD
git commit -m "fix prod issue"
git push origin main
kubectl rollout restart deployment/app

# GOOD
# Test in staging
# Use canary deployment
# Monitor closely
```

**5. Debug without correlation IDs**
```python
# BAD
logger.info("Processing order")  # Which order?

# GOOD
logger.info(f"Processing order: {order_id}, correlation_id: {correlation_id}")
```

## Best Practices Summary

1. **Use structured logging** - JSON format, consistent fields
2. **Implement correlation IDs** - Track requests across services
3. **Enable distributed tracing** - OpenTelemetry, Jaeger
4. **Use error tracking platforms** - Sentry, New Relic
5. **Test fixes in staging first** - Never deploy blindly
6. **Gradual rollouts** - Feature flags, canary deployments
7. **Monitor after changes** - Metrics, logs, traces
8. **Never block execution** - No breakpoints in production
9. **Sanitize logs** - No secrets, PII
10. **Document runbooks** - Playbooks for common issues
