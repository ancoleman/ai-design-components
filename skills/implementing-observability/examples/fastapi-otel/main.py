"""
FastAPI + OpenTelemetry Complete Example

Demonstrates:
- Auto-instrumentation with FastAPI
- Manual span creation
- Log-trace correlation
- HTTP client instrumentation
- Database instrumentation
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx
import structlog
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.trace import Status, StatusCode
import signal
import sys

# Configure structured logging with trace context
def otel_processor(logger, log_method, event_dict):
    """Inject OpenTelemetry trace context into logs."""
    span = trace.get_current_span()
    if span.is_recording():
        ctx = span.get_span_context()
        event_dict["trace_id"] = format(ctx.trace_id, '032x')
        event_dict["span_id"] = format(ctx.span_id, '016x')
    return event_dict


structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        otel_processor,  # Add trace context
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()

# Initialize OpenTelemetry
resource = Resource.create({"service.name": "fastapi-example"})

tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint="localhost:4317",
            insecure=True,
        )
    )
)
trace.set_tracer_provider(tracer_provider)

# Get tracer
tracer = trace.get_tracer(__name__)

# Create FastAPI app
app = FastAPI(
    title="FastAPI OpenTelemetry Example",
    description="Complete example with tracing, logging, and metrics"
)

# Auto-instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Auto-instrument HTTP client
HTTPXClientInstrumentor().instrument()


# Graceful shutdown
def shutdown_handler(signum, frame):
    logger.info("shutting_down", signal=signum)
    tracer_provider.shutdown()
    sys.exit(0)


signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)


@app.on_event("startup")
async def startup_event():
    logger.info("application_started", service="fastapi-example")


@app.get("/")
async def root():
    """Root endpoint - automatically traced by FastAPI instrumentation."""
    logger.info("root_endpoint_called")
    return {"message": "Hello from FastAPI with OpenTelemetry", "status": "ok"}


@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    """
    Fetch user data with manual span creation.

    Demonstrates:
    - Manual span creation
    - Span attributes
    - Log-trace correlation
    """
    # Automatic HTTP span created by FastAPI instrumentation

    # Create manual span for business logic
    with tracer.start_as_current_span("fetch_user_data") as span:
        span.set_attribute("user_id", user_id)
        span.set_attribute("operation", "fetch_user")

        logger.info(
            "fetching_user",
            user_id=user_id,
            # trace_id and span_id automatically added by processor
        )

        # Simulate database query
        if user_id == 0:
            logger.error("invalid_user_id", user_id=user_id)
            span.set_status(Status(StatusCode.ERROR, "Invalid user ID"))
            raise HTTPException(status_code=400, detail="Invalid user ID")

        # Simulate user data
        user = {
            "user_id": user_id,
            "name": f"User {user_id}",
            "email": f"user{user_id}@example.com"
        }

        span.set_attribute("user_found", True)
        logger.info(
            "user_fetched",
            user_id=user_id,
            user_name=user["name"]
        )

    return user


@app.get("/api/external")
async def call_external_service():
    """
    Call external service with trace propagation.

    Demonstrates:
    - HTTP client auto-instrumentation
    - Trace context propagation
    - Error handling with spans
    """
    logger.info("calling_external_service", url="https://jsonplaceholder.typicode.com/posts/1")

    with tracer.start_as_current_span("call_external_api") as span:
        span.set_attribute("http.url", "https://jsonplaceholder.typicode.com/posts/1")

        try:
            async with httpx.AsyncClient() as client:
                # httpx automatically propagates trace context via headers
                response = await client.get("https://jsonplaceholder.typicode.com/posts/1")
                response.raise_for_status()

                data = response.json()
                span.set_attribute("http.status_code", response.status_code)
                span.set_status(Status(StatusCode.OK))

                logger.info(
                    "external_call_success",
                    status_code=response.status_code,
                    response_size=len(response.content)
                )

                return {"external_data": data, "status": "success"}

        except httpx.HTTPError as e:
            logger.error(
                "external_call_failed",
                error=str(e),
                exc_info=True
            )
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            raise HTTPException(status_code=502, detail="External service unavailable")


@app.get("/api/error")
async def simulate_error():
    """
    Simulate an error to test error tracking.

    Demonstrates:
    - Exception recording in spans
    - Error logging with trace context
    """
    logger.warning("simulating_error")

    with tracer.start_as_current_span("error_operation") as span:
        try:
            # Simulate error
            raise ValueError("Simulated error for testing")

        except ValueError as e:
            logger.error(
                "operation_failed",
                error=str(e),
                error_type=type(e).__name__,
                exc_info=True
            )
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))

            # Return error response with trace_id for debugging
            trace_id = format(span.get_span_context().trace_id, '032x')

            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "trace_id": trace_id,  # Client can reference this for support
                    "message": "An error occurred. Please reference this trace_id when contacting support."
                }
            )


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "fastapi-example"}


if __name__ == "__main__":
    import uvicorn

    logger.info("starting_server", host="0.0.0.0", port=8000)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=None  # Use structlog instead of uvicorn's default logger
    )
