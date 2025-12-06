---
sidebar_position: 6
title: Writing Dockerfiles
description: Write optimized, secure, multi-stage Dockerfiles with language-specific patterns and distroless images
tags: [devops, docker, containers, security, multi-stage-builds, buildkit]
---

# Writing Dockerfiles

Create production-grade Dockerfiles with multi-stage builds, security hardening, and language-specific optimizations.

## When to Use

Invoke this skill when:
- "Write a Dockerfile for [Python/Node.js/Go/Rust] application"
- "Optimize this Dockerfile to reduce image size"
- "Use multi-stage build for..."
- "Secure Dockerfile with non-root user"
- "Use distroless base image"
- "Add BuildKit cache mounts"
- "Prevent secrets from leaking in Docker layers"

## Quick Decision Framework

Ask three questions to determine the approach:

**1. What language?**
- Python → Use poetry/pip with virtual environments
- Node.js → Use npm ci with alpine images
- Go → Static binary + distroless = 10-30MB
- Rust → musl static linking + scratch = 5-15MB

**2. Is security critical?**
- YES → Use distroless runtime images
- NO → Use slim/alpine base images

**3. Is image size critical?**
- YES (&lt;50MB) → Multi-stage + distroless + static linking
- NO (&lt;500MB) → Multi-stage + slim base images

## Core Concepts

### Multi-Stage Builds

Separate build environment from runtime environment to minimize final image size.

**Pattern**:
```dockerfile
# Stage 1: Build
FROM build-image AS builder
RUN compile application

# Stage 2: Runtime
FROM minimal-runtime-image
COPY --from=builder /app/binary /app/
CMD ["/app/binary"]
```

**Benefits**:
- 80-95% smaller images (excludes build tools)
- Improved security (no compilers in production)
- Faster deployments
- Better layer caching

### Base Image Selection

| Language | Build Stage | Runtime Stage | Final Size |
|----------|-------------|---------------|------------|
| Go (static) | `golang:1.22-alpine` | `gcr.io/distroless/static-debian12` | 10-30MB |
| Rust (static) | `rust:1.75-alpine` | `scratch` | 5-15MB |
| Python | `python:3.12-slim` | `python:3.12-slim` | 200-400MB |
| Node.js | `node:20-alpine` | `node:20-alpine` | 150-300MB |
| Java | `maven:3.9-eclipse-temurin-21` | `eclipse-temurin:21-jre-alpine` | 200-350MB |

**Distroless images** (Google-maintained):
- `gcr.io/distroless/static-debian12` → Static binaries (2MB)
- `gcr.io/distroless/base-debian12` → Dynamic binaries with libc (20MB)
- `gcr.io/distroless/python3-debian12` → Python runtime (60MB)
- `gcr.io/distroless/nodejs20-debian12` → Node.js runtime (150MB)

### BuildKit Features

Enable BuildKit for advanced caching and security:

```bash
export DOCKER_BUILDKIT=1
docker build .
# OR
docker buildx build .
```

**Key features**:
- `--mount=type=cache` → Persistent package manager caches
- `--mount=type=secret` → Inject secrets without storing in layers
- `--mount=type=ssh` → SSH agent forwarding for private repos
- Parallel stage execution
- Improved layer caching

### Layer Optimization

Order Dockerfile instructions from least to most frequently changing:

```dockerfile
# 1. Base image (rarely changes)
FROM python:3.12-slim

# 2. System packages (rarely changes)
RUN apt-get update && apt-get install -y build-essential

# 3. Dependencies manifest (changes occasionally)
COPY requirements.txt .
RUN pip install -r requirements.txt

# 4. Application code (changes frequently)
COPY . .

# 5. Runtime configuration (rarely changes)
CMD ["python", "app.py"]
```

**BuildKit cache mounts**:
```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

Cache persists across builds, eliminating redundant downloads.

## Security Hardening

### Essential Security Practices

**1. Non-root users**
```dockerfile
# Debian/Ubuntu
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Alpine
RUN adduser -D -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Distroless (built-in)
USER nonroot:nonroot
```

**2. Secret management**
```dockerfile
# ❌ NEVER: Secret in layer history
RUN git clone https://${GITHUB_TOKEN}@github.com/private/repo.git

# ✅ ALWAYS: BuildKit secret mount
RUN --mount=type=secret,id=github_token \
    TOKEN=$(cat /run/secrets/github_token) && \
    git clone https://${TOKEN}@github.com/private/repo.git
```

Build with:
```bash
docker buildx build --secret id=github_token,src=./token.txt .
```

**3. Vulnerability scanning**
```bash
# Trivy (recommended)
trivy image myimage:latest

# Docker Scout
docker scout cves myimage:latest
```

**4. Health checks**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1
```

### .dockerignore Configuration

Create `.dockerignore` to exclude unnecessary files:

```
# Version control
.git
.gitignore

# CI/CD
.github
.gitlab-ci.yml

# IDE
.vscode
.idea

# Testing
tests/
coverage/
**/*_test.go
**/*.test.js

# Build artifacts
node_modules/
dist/
build/
target/
__pycache__/

# Environment
.env
.env.local
*.log
```

Reduces build context size and prevents leaking secrets.

## Language-Specific Patterns

### Python: Poetry Multi-Stage

```dockerfile
FROM python:3.12-slim AS builder
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install poetry==1.7.1

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv /opt/venv && \
    /opt/venv/bin/pip install -r requirements.txt

FROM python:3.12-slim
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
USER 1000:1000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0"]
```

### Node.js: Express Multi-Stage

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci
COPY . .
RUN npm run build
RUN npm prune --omit=dev

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
USER node
CMD ["node", "dist/index.js"]
```

### Go: Distroless Static

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o main .

FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/main /app/main
USER nonroot:nonroot
ENTRYPOINT ["/app/main"]
```

**Final image**: 10-30MB

### Rust: Scratch Base

```dockerfile
FROM rust:1.75-alpine AS builder
RUN apk add --no-cache musl-dev
WORKDIR /app

# Cache dependencies
COPY Cargo.toml Cargo.lock ./
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    mkdir src && echo "fn main() {}" > src/main.rs && \
    cargo build --release --target x86_64-unknown-linux-musl && \
    rm -rf src

# Build application
COPY src ./src
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    cargo build --release --target x86_64-unknown-linux-musl

FROM scratch
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/app /app
USER 1000:1000
ENTRYPOINT ["/app"]
```

**Final image**: 5-15MB

## Package Manager Cache Mounts

| Language | Package Manager | Cache Mount Target |
|----------|----------------|-------------------|
| Python | pip | `--mount=type=cache,target=/root/.cache/pip` |
| Python | poetry | `--mount=type=cache,target=/root/.cache/pypoetry` |
| Python | uv | `--mount=type=cache,target=/root/.cache/uv` |
| Node.js | npm | `--mount=type=cache,target=/root/.npm` |
| Node.js | pnpm | `--mount=type=cache,target=/root/.local/share/pnpm/store` |
| Go | go mod | `--mount=type=cache,target=/go/pkg/mod` |
| Rust | cargo | `--mount=type=cache,target=/usr/local/cargo/registry` |

Persistent caches eliminate redundant package downloads across builds.

## Common Patterns Quick Reference

**1. Static binary (Go/Rust) → Smallest image**
- Build: Language-specific builder image
- Runtime: `gcr.io/distroless/static-debian12` or `scratch`
- Size: 5-30MB

**2. Interpreted language (Python/Node.js) → Production-optimized**
- Build: Install dependencies, build artifacts
- Runtime: Same base, production dependencies only
- Size: 150-400MB

**3. Security-critical → Maximum hardening**
- Base: Distroless images
- User: Non-root (nonroot:nonroot)
- Secrets: BuildKit secret mounts
- Scan: Trivy/Docker Scout in CI

## Anti-Patterns to Avoid

**❌ Never**:
- Use `latest` tags (unpredictable builds)
- Run as root in production
- Store secrets in ENV vars or layers
- Install unnecessary packages
- Combine unrelated RUN commands (breaks caching)
- Skip .dockerignore (bloated build context)

**✅ Always**:
- Pin exact image versions (`python:3.12.1-slim`, not `python:3`)
- Create and use non-root user
- Use BuildKit secret mounts for credentials
- Minimize layers and image size
- Order commands from least to most frequently changing
- Create .dockerignore file

## Related Skills

- [Building CI Pipelines](./building-ci-pipelines) - Build and push Docker images in CI
- [Implementing GitOps](./implementing-gitops) - Deploy containers to K8s clusters
- [Testing Strategies](./testing-strategies) - Test application before containerizing

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/writing-dockerfiles)
- [Base Image Selection](https://github.com/ancoleman/ai-design-components/tree/main/skills/writing-dockerfiles/references/base-image-selection.md)
- [BuildKit Features](https://github.com/ancoleman/ai-design-components/tree/main/skills/writing-dockerfiles/references/buildkit-features.md)
- [Security Hardening](https://github.com/ancoleman/ai-design-components/tree/main/skills/writing-dockerfiles/references/security-hardening.md)
- [Language Examples](https://github.com/ancoleman/ai-design-components/tree/main/skills/writing-dockerfiles/examples)
