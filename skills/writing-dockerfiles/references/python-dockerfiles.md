# Python Dockerfiles

Complete patterns for containerizing Python applications with pip, poetry, and uv.

## Table of Contents

1. [Base Image Selection](#base-image-selection)
2. [Pattern 1: pip (Simple)](#pattern-1-pip-simple)
3. [Pattern 2: Poetry (Production)](#pattern-2-poetry-production)
4. [Pattern 3: uv (Fastest)](#pattern-3-uv-fastest)
5. [Virtual Environment Best Practices](#virtual-environment-best-practices)
6. [Common Python Pitfalls](#common-python-pitfalls)

## Base Image Selection

**Recommended Python base images:**

| Image | Size | Use Case |
|-------|------|----------|
| `python:3.12-slim` | ~150MB | Production (recommended) |
| `python:3.12-alpine` | ~50MB | Smallest (compilation issues possible) |
| `python:3.12` | ~1GB | Development only |
| `gcr.io/distroless/python3-debian12` | ~60MB | Maximum security (pure Python only) |

**Version pinning:**
```dockerfile
# ✅ Good: Exact version
FROM python:3.12.1-slim

# ⚠️ OK: Minor version pinned
FROM python:3.12-slim

# ❌ Bad: Unpredictable
FROM python:3-slim
FROM python:latest
```

## Pattern 1: pip (Simple)

**Use when:**
- Small projects with simple dependencies
- No complex dependency resolution needed
- Quick prototypes

**Single-stage Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app

# Install dependencies with cache mount
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["python", "app.py"]
```

**requirements.txt format:**
```
# Pin all versions
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
```

**Build command:**
```bash
docker build -t myapp:latest .
```

**Expected size:** 200-300MB

## Pattern 2: Poetry (Production)

**Use when:**
- Production applications
- Complex dependency management
- Lock file reproducibility required

**Multi-stage Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder

# Install poetry
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install poetry==1.7.1

# Configure poetry to not create virtual env (we handle it manually)
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN --mount=type=cache,target=/tmp/poetry_cache \
    poetry install --no-root --only main

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Activate virtual environment
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Alternative: Export to requirements.txt**
```dockerfile
# In builder stage
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Then install with pip (faster than poetry install)
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
```

**Build command:**
```bash
docker build -t myapp:latest .
```

**Expected size:** 250-400MB

## Pattern 3: uv (Fastest)

**Use when:**
- Large dependency trees (10-100x faster than pip)
- CI/CD pipelines (speed critical)
- Modern Python projects

**Multi-stage Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Copy application code
COPY . .

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy application and dependencies from builder
COPY --from=builder /app /app

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Activate virtual environment
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**pyproject.toml example:**
```toml
[project]
name = "myapp"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.4.0",
    "black>=23.12.0",
]
```

**Build command:**
```bash
docker build -t myapp:latest .
```

**Expected size:** 250-400MB

**Speed comparison:**
- pip: ~60 seconds (cold cache)
- poetry: ~45 seconds (cold cache)
- uv: ~3-6 seconds (cold cache)

## Virtual Environment Best Practices

**Why use virtual environments in Docker?**
- Dependency isolation
- Explicit Python path
- Compatible with local development
- Easier to copy between stages

**Pattern: Separate virtual environment**
```dockerfile
# Create virtual environment in builder
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies in virtual env
RUN pip install -r requirements.txt

# In runtime stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
```

**Alternative: Poetry in-project venv**
```dockerfile
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
RUN poetry install

# Runtime
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
```

## Common Python Pitfalls

### Pitfall 1: Compiled Dependencies on Alpine

**Problem:** Alpine uses musl libc, not glibc. Wheels (pre-compiled packages) don't work.

```dockerfile
# ❌ This will compile numpy from source (slow, large image)
FROM python:3.12-alpine
RUN pip install numpy pandas
```

**Solution:** Use slim base or install build dependencies:
```dockerfile
# ✅ Use slim (glibc-based)
FROM python:3.12-slim
RUN pip install numpy pandas

# OR install Alpine build deps (not recommended)
FROM python:3.12-alpine
RUN apk add --no-cache gcc musl-dev python3-dev
RUN pip install numpy pandas
```

### Pitfall 2: Missing System Dependencies

**Problem:** Some Python packages require system libraries.

```dockerfile
# ❌ psycopg2 needs PostgreSQL client libraries
FROM python:3.12-slim
RUN pip install psycopg2
# ERROR: pg_config not found
```

**Solution:** Install system packages first:
```dockerfile
# ✅ Install PostgreSQL client libraries
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install psycopg2
```

**Better:** Use binary wheel variants:
```dockerfile
# ✅ psycopg2-binary includes compiled libraries
FROM python:3.12-slim
RUN pip install psycopg2-binary
```

### Pitfall 3: .pyc Files Bloat

**Problem:** Bytecode cache files increase image size.

**Solution:** Disable .pyc generation:
```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
```

### Pitfall 4: pip Cache Not Used

**Problem:** Without cache mounts, pip re-downloads every build.

```dockerfile
# ❌ Re-downloads every time
RUN pip install -r requirements.txt
```

**Solution:** Use BuildKit cache mount:
```dockerfile
# ✅ Persistent cache across builds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

### Pitfall 5: Development Dependencies in Production

**Problem:** Installing dev dependencies bloats production image.

```dockerfile
# ❌ Installs pytest, black, etc. in production
RUN poetry install
```

**Solution:** Install production dependencies only:
```dockerfile
# ✅ Skip dev dependencies
RUN poetry install --only main

# OR with pip
RUN pip install -r requirements.txt
# (requirements.txt should not include dev deps)
```

## FastAPI Complete Example

**Production-ready FastAPI application:**

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder

# Install uv (fastest)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Copy application
COPY . .

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy application and venv
COPY --from=builder /app /app

# Install runtime system dependencies (if needed)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libpq5 \
#     && rm -rf /var/lib/apt/lists/*

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
  CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Expected size:** 280-380MB

## Django Complete Example

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder

# Install poetry
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install poetry==1.7.1

WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN --mount=type=cache,target=/tmp/poetry_cache \
    poetry install --no-root --only main

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Install PostgreSQL client library
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment
COPY --from=builder /app/.venv /app/.venv

# Copy application
COPY . .

# Collect static files
ENV PATH="/app/.venv/bin:$PATH"
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Django settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings.production

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

**Expected size:** 350-450MB

## Summary

**Choose pattern based on needs:**

| Pattern | Use Case | Build Time | Image Size | Complexity |
|---------|----------|------------|------------|------------|
| pip | Simple apps, prototypes | Fast | 200-300MB | Low |
| poetry | Production, lock files | Medium | 250-400MB | Medium |
| uv | Large deps, speed critical | Very fast | 250-400MB | Low |

**Key takeaways:**
- Always use multi-stage builds for production
- Use BuildKit cache mounts for package managers
- Pin Python version and all dependencies
- Create non-root user
- Use slim base images (not alpine for compiled deps)
- Disable .pyc file generation
- Install only production dependencies
