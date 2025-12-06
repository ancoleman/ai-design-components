# Production-Ready FastAPI Application Dockerfile
#
# This example demonstrates:
# - Multi-stage build with uv (fastest Python package manager)
# - BuildKit cache mounts for dependencies
# - Non-root user for security
# - Virtual environment isolation
# - Health check implementation
#
# Expected image size: 280-380MB
#
# Build: docker build -f python-fastapi.Dockerfile -t fastapi-app:latest .
# Run: docker run -p 8000:8000 fastapi-app:latest

# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder

# Install uv (10-100x faster than pip)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies with cache mount
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Copy application code
COPY . .

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy application and virtual environment from builder
COPY --from=builder /app /app

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Activate virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Python optimizations
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=2)" || exit 1

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
