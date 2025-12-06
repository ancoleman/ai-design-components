#!/usr/bin/env python3
"""
OpenTelemetry Setup Bootstrap Script

Automatically configures OpenTelemetry instrumentation for Python projects.
Supports FastAPI, Flask, and Django frameworks.

Usage:
    python setup_otel.py --language python --framework fastapi
    python setup_otel.py --language python --framework flask --service-name my-service
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Dict

# Template configurations
PYTHON_DEPENDENCIES = {
    "common": [
        "opentelemetry-api",
        "opentelemetry-sdk",
        "opentelemetry-exporter-otlp",
        "opentelemetry-instrumentation",
    ],
    "fastapi": [
        "opentelemetry-instrumentation-fastapi",
        "opentelemetry-instrumentation-httpx",
        "opentelemetry-instrumentation-sqlalchemy",
    ],
    "flask": [
        "opentelemetry-instrumentation-flask",
        "opentelemetry-instrumentation-requests",
    ],
    "django": [
        "opentelemetry-instrumentation-django",
        "opentelemetry-instrumentation-psycopg2",
    ],
}

FASTAPI_TEMPLATE = '''# instrumentation.py
"""OpenTelemetry instrumentation for FastAPI."""

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor


def setup_opentelemetry(app, service_name: str = "{service_name}"):
    """
    Configure OpenTelemetry for FastAPI application.

    Args:
        app: FastAPI application instance
        service_name: Name of the service for telemetry

    Returns:
        tuple: (tracer_provider, meter_provider)
    """
    # Resource attributes
    resource = Resource.create({{"service.name": service_name}})

    # Trace provider
    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
                endpoint="{otlp_endpoint}",
                insecure=True,
            )
        )
    )
    trace.set_tracer_provider(trace_provider)

    # Metrics provider
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(
            endpoint="{otlp_endpoint}",
            insecure=True,
        )
    )
    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[metric_reader]
    )
    metrics.set_meter_provider(meter_provider)

    # Auto-instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    # Auto-instrument HTTP client
    HTTPXClientInstrumentor().instrument()

    print(f"OpenTelemetry initialized for {{service_name}}")
    print(f"Exporting to {{'{otlp_endpoint}'}}")

    return trace_provider, meter_provider


def shutdown_opentelemetry(trace_provider, meter_provider):
    """Gracefully shutdown OpenTelemetry providers."""
    trace_provider.shutdown()
    meter_provider.shutdown()
'''

FLASK_TEMPLATE = '''# instrumentation.py
"""OpenTelemetry instrumentation for Flask."""

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


def setup_opentelemetry(app, service_name: str = "{service_name}"):
    """
    Configure OpenTelemetry for Flask application.

    Args:
        app: Flask application instance
        service_name: Name of the service for telemetry

    Returns:
        tuple: (tracer_provider, meter_provider)
    """
    resource = Resource.create({{"service.name": service_name}})

    # Trace provider
    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint="{otlp_endpoint}", insecure=True)
        )
    )
    trace.set_tracer_provider(trace_provider)

    # Metrics provider
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint="{otlp_endpoint}", insecure=True)
    )
    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[metric_reader]
    )
    metrics.set_meter_provider(meter_provider)

    # Auto-instrument Flask
    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()

    print(f"OpenTelemetry initialized for {{service_name}}")

    return trace_provider, meter_provider
'''


def create_requirements_file(framework: str, output_dir: Path) -> None:
    """Create requirements.txt with OpenTelemetry dependencies."""
    requirements_path = output_dir / "requirements-otel.txt"

    deps = PYTHON_DEPENDENCIES["common"] + PYTHON_DEPENDENCIES.get(framework, [])

    with open(requirements_path, "w") as f:
        f.write("# OpenTelemetry dependencies\n")
        f.write("# Install with: pip install -r requirements-otel.txt\n\n")
        for dep in deps:
            f.write(f"{dep}\n")

    print(f"✓ Created {requirements_path}")


def create_instrumentation_file(
    framework: str,
    service_name: str,
    otlp_endpoint: str,
    output_dir: Path
) -> None:
    """Create instrumentation.py file."""
    instrumentation_path = output_dir / "instrumentation.py"

    if framework == "fastapi":
        template = FASTAPI_TEMPLATE
    elif framework == "flask":
        template = FLASK_TEMPLATE
    else:
        print(f"✗ Framework '{framework}' not supported yet")
        return

    content = template.format(
        service_name=service_name,
        otlp_endpoint=otlp_endpoint
    )

    with open(instrumentation_path, "w") as f:
        f.write(content)

    print(f"✓ Created {instrumentation_path}")


def create_usage_example(framework: str, service_name: str, output_dir: Path) -> None:
    """Create example main.py showing how to use instrumentation."""
    example_path = output_dir / "main_example.py"

    if framework == "fastapi":
        content = f'''# main.py
"""Example FastAPI application with OpenTelemetry."""

from fastapi import FastAPI
from instrumentation import setup_opentelemetry, shutdown_opentelemetry
import signal

app = FastAPI(title="{service_name}")

# Initialize OpenTelemetry
trace_provider, meter_provider = setup_opentelemetry(app, service_name="{service_name}")


# Graceful shutdown
def shutdown_handler(signum, frame):
    print("Shutting down OpenTelemetry...")
    shutdown_opentelemetry(trace_provider, meter_provider)
    exit(0)


signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)


@app.get("/")
async def root():
    """Root endpoint - automatically traced."""
    return {{"message": "Hello World", "service": "{service_name}"}}


@app.get("/health")
async def health():
    """Health check - automatically traced."""
    return {{"status": "healthy"}}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    elif framework == "flask":
        content = f'''# main.py
"""Example Flask application with OpenTelemetry."""

from flask import Flask
from instrumentation import setup_opentelemetry

app = Flask(__name__)

# Initialize OpenTelemetry
setup_opentelemetry(app, service_name="{service_name}")


@app.route("/")
def root():
    """Root endpoint - automatically traced."""
    return {{"message": "Hello World", "service": "{service_name}"}}


@app.route("/health")
def health():
    """Health check - automatically traced."""
    return {{"status": "healthy"}}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
'''
    else:
        return

    with open(example_path, "w") as f:
        f.write(content)

    print(f"✓ Created {example_path}")


def create_readme(framework: str, service_name: str, output_dir: Path) -> None:
    """Create README with setup instructions."""
    readme_path = output_dir / "README_OTEL.md"

    content = f'''# OpenTelemetry Setup for {service_name}

## Installation

```bash
# Install dependencies
pip install -r requirements-otel.txt
```

## Configuration

The instrumentation is configured to export to:
- OTLP endpoint: `localhost:4317` (gRPC)

To change the endpoint, edit `instrumentation.py`:

```python
OTLPSpanExporter(endpoint="your-endpoint:4317")
```

## Usage

### Import and initialize

```python
from instrumentation import setup_opentelemetry

# In your main.py
app = {'Flask()' if framework == 'flask' else 'FastAPI()'}
setup_opentelemetry(app, service_name="{service_name}")
```

### Run your application

```bash
python main_example.py
```

### Verify telemetry

1. Ensure LGTM stack is running:
   ```bash
   cd examples/lgtm-docker-compose
   docker-compose up -d
   ```

2. Make requests to your app:
   ```bash
   curl http://localhost:8000/
   ```

3. View traces in Grafana:
   - Navigate to http://localhost:3000
   - Go to Explore → Tempo
   - Search for `service.name = "{service_name}"`

## Environment Variables

Override configuration via environment variables:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
export OTEL_SERVICE_NAME={service_name}
export OTEL_TRACES_SAMPLER=always_on
```

## Auto-Instrumented Libraries

The following are automatically instrumented:

- {'FastAPI routes' if framework == 'fastapi' else 'Flask routes'}
- {'httpx' if framework == 'fastapi' else 'requests'} (HTTP client)
- SQLAlchemy (database)

## Adding Manual Spans

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def my_function():
    with tracer.start_as_current_span("my_operation") as span:
        span.set_attribute("custom_attribute", "value")
        # Your code here
```

## Troubleshooting

**Traces not appearing**:
- Check OTLP endpoint is reachable: `telnet localhost 4317`
- Verify Grafana Alloy is running: `docker ps | grep alloy`
- Enable debug logging: `export OTEL_LOG_LEVEL=debug`

**High overhead**:
- Reduce sampling: `export OTEL_TRACES_SAMPLER_ARG=0.1` (10% sampling)
- Disable auto-instrumentation for specific libraries

## Next Steps

1. Add structured logging (see `references/structured-logging.md`)
2. Configure alerting rules (see `references/alerting-rules.md`)
3. Create Grafana dashboards
'''

    with open(readme_path, "w") as f:
        f.write(content)

    print(f"✓ Created {readme_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Bootstrap OpenTelemetry setup for Python applications"
    )
    parser.add_argument(
        "--language",
        choices=["python"],
        default="python",
        help="Programming language (currently only Python supported)"
    )
    parser.add_argument(
        "--framework",
        choices=["fastapi", "flask", "django"],
        required=True,
        help="Web framework"
    )
    parser.add_argument(
        "--service-name",
        default="my-service",
        help="Service name for telemetry (default: my-service)"
    )
    parser.add_argument(
        "--otlp-endpoint",
        default="localhost:4317",
        help="OTLP gRPC endpoint (default: localhost:4317)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd(),
        help="Output directory for generated files (default: current directory)"
    )

    args = parser.parse_args()

    print(f"\n🔧 Setting up OpenTelemetry for {args.framework}...")
    print(f"   Service: {args.service_name}")
    print(f"   Output: {args.output_dir}\n")

    # Create output directory if it doesn't exist
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Generate files
    create_requirements_file(args.framework, args.output_dir)
    create_instrumentation_file(
        args.framework,
        args.service_name,
        args.otlp_endpoint,
        args.output_dir
    )
    create_usage_example(args.framework, args.service_name, args.output_dir)
    create_readme(args.framework, args.service_name, args.output_dir)

    print("\n✅ OpenTelemetry setup complete!\n")
    print("Next steps:")
    print(f"  1. Install dependencies: pip install -r {args.output_dir}/requirements-otel.txt")
    print(f"  2. Review instrumentation.py and customize if needed")
    print(f"  3. Import and use in your main.py (see main_example.py)")
    print(f"  4. Start LGTM stack: cd examples/lgtm-docker-compose && docker-compose up")
    print(f"  5. Run your app and verify traces in Grafana (http://localhost:3000)\n")


if __name__ == "__main__":
    main()
