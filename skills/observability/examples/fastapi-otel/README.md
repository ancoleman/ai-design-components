# FastAPI + OpenTelemetry Complete Example

Complete working example of FastAPI with OpenTelemetry tracing and structured logging.

## Features

- ✅ Auto-instrumentation with FastAPI
- ✅ Manual span creation for business logic
- ✅ Log-trace correlation (trace_id/span_id in logs)
- ✅ HTTP client auto-instrumentation
- ✅ Error tracking and exception recording
- ✅ Structured JSON logging with structlog
- ✅ OTLP export to LGTM stack

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start LGTM Stack

```bash
# From the lgtm-docker-compose directory
cd ../lgtm-docker-compose
docker-compose up -d

# Wait for services to start (30 seconds)
```

### 3. Run Application

```bash
python main.py
```

### 4. Generate Traces

```bash
# Root endpoint
curl http://localhost:8000/

# User endpoint with manual span
curl http://localhost:8000/api/users/123

# External API call with trace propagation
curl http://localhost:8000/api/external

# Error handling example
curl http://localhost:8000/api/error
```

### 5. View in Grafana

1. Navigate to http://localhost:3000 (login: admin/admin)
2. Go to Explore → Tempo
3. Search for `service.name="fastapi-example"`
4. Click on a trace to see spans and timing
5. Click "Logs for this span" to see correlated logs

## Project Structure

```
fastapi-otel/
├── main.py                 # FastAPI app with OTel instrumentation
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── docker-compose.yml     # Optional: Run with Docker
```

## Code Walkthrough

### OpenTelemetry Setup

```python
# Initialize tracer provider
tracer_provider = TracerProvider(
    resource=Resource.create({"service.name": "fastapi-example"})
)

# Add OTLP exporter
tracer_provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(endpoint="localhost:4317")
    )
)

# Set as global provider
trace.set_tracer_provider(tracer_provider)

# Auto-instrument FastAPI
FastAPIInstrumentor.instrument_app(app)
```

### Manual Span Creation

```python
@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    # Create manual span
    with tracer.start_as_current_span("fetch_user_data") as span:
        span.set_attribute("user_id", user_id)

        # Business logic here
        user = fetch_from_db(user_id)

        span.set_attribute("user_found", True)
        return user
```

### Log-Trace Correlation

```python
# Custom processor to inject trace context
def otel_processor(logger, log_method, event_dict):
    span = trace.get_current_span()
    if span.is_recording():
        ctx = span.get_span_context()
        event_dict["trace_id"] = format(ctx.trace_id, '032x')
        event_dict["span_id"] = format(ctx.span_id, '016x')
    return event_dict

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        otel_processor,  # Add trace context
        structlog.processors.JSONRenderer()
    ]
)
```

### Error Handling

```python
@app.get("/api/error")
async def simulate_error():
    with tracer.start_as_current_span("error_operation") as span:
        try:
            raise ValueError("Simulated error")
        except ValueError as e:
            # Record exception in span
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))

            # Log with trace context
            logger.error("operation_failed", error=str(e))

            # Return trace_id to client for support
            trace_id = format(span.get_span_context().trace_id, '032x')
            return {"error": "Internal error", "trace_id": trace_id}
```

## Observability Queries

### Grafana Tempo (Traces)

```
# Find all traces for this service
{service.name="fastapi-example"}

# Find traces with errors
{service.name="fastapi-example" && status=error}

# Find slow requests (>1s)
{service.name="fastapi-example" && duration>1s}
```

### Grafana Loki (Logs)

```logql
# All logs for this service
{service="fastapi-example"}

# Error logs with trace_id
{service="fastapi-example"} | json | level="error"

# Find logs for specific trace
{service="fastapi-example"} | json | trace_id="4bf92f3577b34da6a3ce929d0e0e4736"
```

## Testing

### Manual Testing

```bash
# Test normal request
curl http://localhost:8000/api/users/123

# Test error handling
curl http://localhost:8000/api/users/0

# Test external call
curl http://localhost:8000/api/external
```

### Load Testing

```bash
# Install hey
go install github.com/rakyll/hey@latest

# Generate load
hey -n 1000 -c 10 http://localhost:8000/api/users/123

# View traces in Grafana to see performance distribution
```

## Configuration

### Environment Variables

```bash
# OTLP endpoint
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Service name
export OTEL_SERVICE_NAME=fastapi-example

# Sampling (1.0 = 100%, 0.1 = 10%)
export OTEL_TRACES_SAMPLER_ARG=1.0

# Log level
export LOG_LEVEL=INFO
```

### Custom OTLP Endpoint

Edit `main.py`:

```python
OTLPSpanExporter(
    endpoint="your-collector:4317",
    insecure=False,  # Use TLS
    headers=(("x-api-key", "your-key"),)  # Authentication
)
```

## Troubleshooting

**Traces not appearing in Tempo**:

1. Check OTLP endpoint is reachable:
   ```bash
   telnet localhost 4317
   ```

2. Verify Grafana Alloy is running:
   ```bash
   docker ps | grep alloy
   ```

3. Enable debug logging:
   ```bash
   export OTEL_LOG_LEVEL=debug
   python main.py
   ```

**Logs missing trace_id**:

- Verify logs are emitted inside a span context
- Check structlog processor is configured correctly
- Ensure OpenTelemetry is initialized before logging

**High memory usage**:

- Reduce batch size in exporter
- Enable sampling for high-traffic endpoints
- Use async exporter for better performance

## Next Steps

1. Add database instrumentation (see `references/opentelemetry-setup.md`)
2. Configure alerting rules (see `references/alerting-rules.md`)
3. Create custom Grafana dashboards
4. Add metrics collection
5. Deploy to production with proper sampling and batching

## Resources

- OpenTelemetry Python Docs: https://opentelemetry-python.readthedocs.io
- FastAPI Docs: https://fastapi.tiangolo.com
- Grafana Tempo Docs: https://grafana.com/docs/tempo
