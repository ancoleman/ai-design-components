# Writing Dockerfiles - Master Plan

**Skill Name:** `writing-dockerfiles`
**Skill Level:** Low Level (2,000-5,000 tokens, 300-500 lines init.md)
**Last Updated:** December 3, 2025
**Status:** Master Plan (init.md) - Ready for SKILL.md implementation

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Dockerfile Taxonomy](#dockerfile-taxonomy)
5. [Decision Framework](#decision-framework)
6. [Multi-Stage Build Patterns](#multi-stage-build-patterns)
7. [Security Hardening Patterns](#security-hardening-patterns)
8. [Language-Specific Dockerfiles](#language-specific-dockerfiles)
9. [Tool Recommendations](#tool-recommendations)
10. [Skill Structure Design](#skill-structure-design)
11. [Integration Points](#integration-points)
12. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### The Docker Competency Gap

While containerization is ubiquitous, **writing optimized, secure, and maintainable Dockerfiles remains a specialized skill**. Common issues include:

- **Bloated images**: 2GB+ images when 50MB would suffice
- **Security vulnerabilities**: Running as root, outdated base images, secrets in layers
- **Slow builds**: Poor layer caching, redundant package installs
- **Maintenance nightmares**: Monolithic Dockerfiles without multi-stage separation
- **Language-specific pitfalls**: Python package managers, Node.js dependency hell, Go build complexity

### Why This Skill Matters (2025)

**1. Image Size = Cost & Speed**
- 10MB image vs 1GB image: 100x faster pulls, lower registry costs
- Multi-stage builds can reduce image size by 80-95%
- Distroless images minimize attack surface (no shell, no package manager)

**2. Security is Non-Negotiable**
- CVE scanning required for production (Trivy, Docker Scout)
- Non-root containers prevent privilege escalation
- Distroless base images reduce vulnerabilities by 60-80%
- BuildKit secrets prevent credential leakage in layers

**3. Build Speed = Developer Productivity**
- Proper layer ordering: 10x faster rebuilds with cache hits
- BuildKit cache mounts: Zero re-downloads of dependencies
- Multi-stage parallelization: Build stages concurrently

**4. Emerging Best Practices**
- Distroless images (Google's hardened base images)
- BuildKit advanced features (cache mounts, secret mounts, SSH mounts)
- Health checks for container orchestration
- Reproducible builds with pinned versions

### Integration with Related Skills

**Upstream Dependencies:**
- `testing-strategies` → Test application before containerizing
- `security-hardening` → Application-level security before Docker layer

**Downstream Consumers:**
- `building-ci-pipelines` → Build and push Docker images in CI
- `kubernetes-operations` → Deploy containers to K8s clusters
- `infrastructure-as-code` → Terraform/Pulumi infrastructure with containers

**Does NOT Cover:**
- Container orchestration (see `kubernetes-operations`)
- Docker Compose for development environments
- CI/CD integration specifics (see `building-ci-pipelines`)

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**
- Multi-stage build patterns for all major languages
- Layer optimization and caching strategies
- Security hardening (non-root users, distroless images, secret management)
- BuildKit advanced features (cache mounts, secret mounts)
- Language-specific best practices (Python, Node.js, Go, Rust)
- .dockerignore configuration
- Health check implementation

**Out of Scope:**
- Docker Compose (multi-container applications)
- Container networking and volumes
- Docker Swarm or Kubernetes orchestration
- CI/CD pipeline configuration
- Container registry management

### Target Audience

**Primary Users:**
- Backend developers containerizing applications
- DevOps engineers optimizing existing Dockerfiles
- Platform engineers establishing standards

**Skill Prerequisites:**
- Basic Docker knowledge (FROM, RUN, COPY, CMD)
- Understanding of Linux file systems
- Familiarity with package managers (pip, npm, apt, etc.)

---

## Research Findings

### Research Methodology

**Research Date:** December 3, 2025
**Tools Used:** Google Search Grounding (mcp__litellm__gs-google_search_grounding)
**Queries:**
1. "Dockerfile best practices 2025 multi-stage builds"
2. "Docker security hardening distroless non-root 2025"
3. "Docker layer optimization build cache 2025" (fallback to existing knowledge)

### Key Findings (2025)

**1. Multi-Stage Builds Remain Essential**

**Benefits:**
- **Reduced Image Size**: 80-95% smaller by excluding build tools from runtime
- **Improved Security**: Build dependencies don't ship to production
- **Faster Build Times**: Docker layer caching optimizes stage rebuilds
- **Simplified Dockerfiles**: Consolidate complex builds in single file

**Best Practices:**
- Use minimal base images (`alpine`, `debian-slim`, language-specific slim variants)
- Pin exact image versions (no `latest` tags)
- Enable BuildKit for advanced caching
- Optimize build order to maximize cache utilization
- Use `.dockerignore` to exclude unnecessary files
- Run as non-root user
- Scan images with Trivy or Docker Scout

**Source:** talent500.com, iximiuz.com, spacelift.io, docker.com, blacksmith.sh, cherryservers.com, bytescrum.com (via Google Search Grounding)

**2. Security Hardening with Distroless and Non-Root**

**Distroless Images:**
- Contain ONLY application + runtime dependencies
- No package manager, shell, or unnecessary binaries
- 60-80% fewer vulnerabilities than traditional base images
- Google's distroless images are production-proven

**Non-Root Users:**
- Principle of least privilege: Limit blast radius of container breach
- Create dedicated user in Dockerfile, switch before CMD/ENTRYPOINT
- User namespaces map container root to host non-privileged user

**Additional Hardening:**
- Regular image rebuilds with security updates
- Vulnerability scanning (Trivy, Clair, Docker Scan)
- Externalize secrets (BuildKit secret mounts, not ENV vars)
- Network segmentation and firewall rules
- Read-only filesystems where possible
- Resource limits (CPU/memory) to prevent DoS
- Docker Content Trust (signed images)
- Seccomp and AppArmor profiles

**Source:** talent500.com, opsmoon.com, medium.com, signiance.com, onlinehashcrack.com, cloudnativenow.com (via Google Search Grounding)

**3. Layer Optimization Strategies**

**Key Principles:**
- Order Dockerfile instructions from least to most frequently changing
- Combine related RUN commands to reduce layers
- Use BuildKit cache mounts (`--mount=type=cache`) to persist package caches
- Leverage build cache between CI runs
- Multi-stage builds separate build and runtime layers

**BuildKit Advanced Features:**
- `--mount=type=cache`: Persist package manager caches across builds
- `--mount=type=secret`: Inject secrets without storing in layers
- `--mount=type=ssh`: SSH agent forwarding for private repos
- `--mount=type=bind`: Mount files from other stages without COPY

---

## Dockerfile Taxonomy

### Dockerfile Types

**1. Single-Stage Dockerfile**
```
FROM base-image
RUN install dependencies
COPY application code
CMD run application
```

**Use Case:**
- Interpreted languages where build = runtime (Python, Node.js for simple apps)
- Quick prototypes or development images
- When image size is not a concern

**Limitations:**
- Large image size (includes all build tools)
- More attack surface (compilers, dev tools)
- Slower image pulls

---

**2. Multi-Stage Dockerfile**
```
# Stage 1: Build
FROM build-image AS builder
RUN compile application

# Stage 2: Runtime
FROM minimal-runtime-image
COPY --from=builder /app/binary /app/
CMD ["/app/binary"]
```

**Use Case:**
- Compiled languages (Go, Rust, Java, C++)
- JavaScript/TypeScript with build steps (webpack, tsc)
- Python with compiled dependencies (numpy, pandas)
- Production deployments (optimized size and security)

**Benefits:**
- 10x-100x smaller images (50MB vs 2GB)
- No build tools in production image
- Better security posture
- Faster deployments

---

**3. Distroless Multi-Stage Dockerfile**
```
# Stage 1: Build
FROM debian:bookworm AS builder
RUN apt-get update && apt-get install -y build-tools
COPY . /src
RUN make build

# Stage 2: Distroless runtime
FROM gcr.io/distroless/base-debian12
COPY --from=builder /src/app /app
USER nonroot:nonroot
CMD ["/app"]
```

**Use Case:**
- Production environments requiring maximum security
- Regulatory compliance (minimal CVE exposure)
- Static binaries or self-contained runtimes

**Benefits:**
- Minimal attack surface (no shell, no package manager)
- 60-80% fewer vulnerabilities
- Smallest possible image size
- Immutable at runtime

---

## Decision Framework

### Base Image Selection

**Decision Tree:**

```
WHAT LANGUAGE ARE YOU USING?

├── COMPILED LANGUAGE (Go, Rust, C++) → Multi-stage with distroless
│   ├─ Build Stage: language:latest or debian with build tools
│   └─ Runtime Stage: gcr.io/distroless/static-debian12
│
├── PYTHON → Multi-stage with slim base
│   ├─ Build Stage: python:3.12-slim for pip/poetry/uv install
│   └─ Runtime Stage: python:3.12-slim (or distroless if pure Python)
│
├── NODE.JS → Multi-stage with alpine
│   ├─ Build Stage: node:20-alpine for npm/pnpm install
│   └─ Runtime Stage: node:20-alpine (production deps only)
│
└── JAVA → Multi-stage with JRE
    ├─ Build Stage: maven:3.9-eclipse-temurin-21 or gradle:8-jdk21
    └─ Runtime Stage: eclipse-temurin:21-jre-alpine

IS SECURITY CRITICAL?

├── YES → Distroless runtime
│   ✅ No shell access
│   ✅ Minimal CVE surface
│   ⚠️  Harder to debug (no shell)
│
└── NO → Slim/alpine runtime
    ✅ Smaller than full images
    ✅ Shell available for debugging
    ✅ Package manager for runtime installs

IS IMAGE SIZE CRITICAL?

├── YES (<50MB) → Multi-stage + distroless + static linking
│   ├─ Go: Static binary + scratch base = 5-20MB
│   ├─ Rust: musl static binary + scratch = 5-15MB
│   └─ Node: Multi-stage with production deps only
│
└── NO (<500MB acceptable) → Slim base images
    ├─ Python: python:3.12-slim (~150MB)
    ├─ Node: node:20-alpine (~180MB)
    └─ Java: temurin:21-jre-alpine (~200MB)
```

---

### Build Tool Selection

**Package Manager Caching:**

| Language | Package Manager | Cache Location | BuildKit Mount |
|----------|----------------|----------------|----------------|
| Python | pip | `/root/.cache/pip` | `--mount=type=cache,target=/root/.cache/pip` |
| Python | poetry | `/root/.cache/pypoetry` | `--mount=type=cache,target=/root/.cache/pypoetry` |
| Python | uv | `/root/.cache/uv` | `--mount=type=cache,target=/root/.cache/uv` |
| Node.js | npm | `/root/.npm` | `--mount=type=cache,target=/root/.npm` |
| Node.js | pnpm | `/root/.local/share/pnpm/store` | `--mount=type=cache,target=/root/.local/share/pnpm/store` |
| Go | go mod | `/go/pkg/mod` | `--mount=type=cache,target=/go/pkg/mod` |
| Rust | cargo | `/usr/local/cargo/registry` | `--mount=type=cache,target=/usr/local/cargo/registry` |

---

## Multi-Stage Build Patterns

### Pattern 1: Go Static Binary (Smallest Possible)

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o main .

# Runtime stage: distroless static
FROM gcr.io/distroless/static-debian12

COPY --from=builder /app/main /app/main
USER nonroot:nonroot
EXPOSE 8080

ENTRYPOINT ["/app/main"]
```

**Key Features:**
- Static binary (CGO_ENABLED=0) = no libc dependencies
- Smallest base image: `distroless/static` (2MB)
- BuildKit cache mounts for go modules and build cache
- Non-root user for security
- Stripped symbols (-ldflags="-s -w") for smaller binary
- **Final image size: 10-30MB**

---

### Pattern 2: Python with Poetry (Production-Grade)

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder

# Install poetry
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install poetry==1.7.1

WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Export dependencies to requirements.txt (for faster installs)
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Install dependencies in virtual environment
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

# Runtime stage
FROM python:3.12-slim

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Activate virtual environment
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Key Features:**
- Poetry for dependency management
- Virtual environment for isolation
- BuildKit cache for pip downloads
- Non-root user (appuser)
- Requirements export for faster installs
- **Final image size: 200-400MB** (depending on dependencies)

---

### Pattern 3: Node.js with pnpm (Monorepo-Friendly)

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS builder

# Enable Corepack for pnpm
RUN corepack enable && corepack prepare pnpm@8.15.0 --activate

WORKDIR /app

# Copy dependency manifests
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY packages/api/package.json ./packages/api/

# Install dependencies with cache mount
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile --prod=false

# Copy source code and build
COPY . .
RUN pnpm --filter=api build

# Prune dev dependencies
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile --prod --ignore-scripts

# Runtime stage
FROM node:20-alpine

WORKDIR /app

# Copy production dependencies and built code
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/packages/api/dist ./dist
COPY --from=builder /app/packages/api/package.json ./

# Create non-root user
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Key Features:**
- pnpm for efficient monorepo dependency management
- BuildKit cache mount for pnpm store
- Production dependencies only in runtime
- Non-root user
- **Final image size: 150-300MB**

---

### Pattern 4: Rust with musl (Ultra-Small Static Binary)

```dockerfile
# syntax=docker/dockerfile:1
FROM rust:1.75-alpine AS builder

# Install musl build tools
RUN apk add --no-cache musl-dev

WORKDIR /app

# Cache dependencies layer
COPY Cargo.toml Cargo.lock ./
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    mkdir src && echo "fn main() {}" > src/main.rs && \
    cargo build --release --target x86_64-unknown-linux-musl && \
    rm -rf src

# Build actual application
COPY src ./src
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release --target x86_64-unknown-linux-musl && \
    cp target/x86_64-unknown-linux-musl/release/app /app/binary

# Runtime stage: scratch (absolutely minimal)
FROM scratch

COPY --from=builder /app/binary /app
USER 1000:1000
EXPOSE 8080

ENTRYPOINT ["/app"]
```

**Key Features:**
- musl static linking (no libc dependencies)
- scratch base image (0 bytes overhead)
- BuildKit cache for cargo registry
- Dummy build for dependency caching
- **Final image size: 5-15MB** (just the binary)

---

## Security Hardening Patterns

### Pattern 1: Non-Root User Configuration

**Debian/Ubuntu base:**
```dockerfile
# Create user and group
RUN groupadd -r appuser -g 1000 && \
    useradd -r -u 1000 -g appuser -m -d /home/appuser -s /bin/bash appuser

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser
```

**Alpine base:**
```dockerfile
# Create user and group
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser
```

**Distroless images (built-in):**
```dockerfile
# Distroless images include 'nonroot' user (UID 65532)
FROM gcr.io/distroless/static-debian12
USER nonroot:nonroot
```

---

### Pattern 2: Secret Management with BuildKit

**NEVER do this (secrets in layer history):**
```dockerfile
# ❌ BAD: Secret persists in layer
RUN echo "machine github.com login token password ${GITHUB_TOKEN}" > ~/.netrc && \
    git clone https://github.com/private/repo.git && \
    rm ~/.netrc
# Even though .netrc is deleted, GITHUB_TOKEN is in layer history!
```

**DO this (BuildKit secret mount):**
```dockerfile
# ✅ GOOD: Secret never enters layer
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=github_token \
    GITHUB_TOKEN=$(cat /run/secrets/github_token) && \
    git clone https://${GITHUB_TOKEN}@github.com/private/repo.git
```

**Build command:**
```bash
docker buildx build --secret id=github_token,src=./token.txt .
```

---

### Pattern 3: Minimal Distroless Runtime

**Available distroless variants:**

| Image | Use Case | Size | Contents |
|-------|----------|------|----------|
| `gcr.io/distroless/static-debian12` | Static binaries (Go, Rust) | ~2MB | Just filesystem + CA certs |
| `gcr.io/distroless/base-debian12` | Dynamic binaries (needs libc) | ~20MB | glibc, libssl, tzdata |
| `gcr.io/distroless/cc-debian12` | C/C++ applications | ~25MB | glibc, libgcc, libstdc++ |
| `gcr.io/distroless/python3-debian12` | Python applications | ~60MB | Python 3 runtime |
| `gcr.io/distroless/java17-debian12` | Java 17 applications | ~200MB | Java 17 JRE |
| `gcr.io/distroless/nodejs20-debian12` | Node.js applications | ~150MB | Node.js 20 runtime |

**Example:**
```dockerfile
FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/binary /app/binary
USER nonroot:nonroot
ENTRYPOINT ["/app/binary"]
```

---

### Pattern 4: Health Checks

```dockerfile
# For HTTP servers
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

# For distroless (no shell - use binary)
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD ["/app/healthcheck"]

# For databases
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
  CMD pg_isready -U postgres || exit 1
```

**Why health checks matter:**
- Kubernetes/Docker knows when container is ready
- Prevents routing traffic to unhealthy containers
- Automatic container restart on health check failure

---

## Language-Specific Dockerfiles

### Python Best Practices

**Option 1: pip (Simple)**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copy requirements first (cache layer)
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "app.py"]
```

**Option 2: uv (Fastest - 10-100x faster than pip)**
```dockerfile
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

COPY . .

FROM python:3.12-slim
COPY --from=builder /app /app
WORKDIR /app
USER 1000:1000
CMD ["python", "app.py"]
```

**Key Python Considerations:**
- Always use `--no-cache-dir` with pip (or cache mounts)
- Virtual environments isolate dependencies
- uv is 10-100x faster than pip for large dependency trees
- Pin Python version (no `:latest`)

---

### Node.js Best Practices

**Production-optimized Dockerfile:**
```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Build application
COPY . .
RUN npm run build

# Prune dev dependencies
RUN npm prune --omit=dev

FROM node:20-alpine

WORKDIR /app

# Copy production files
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

USER node
CMD ["node", "dist/index.js"]
```

**Key Node.js Considerations:**
- Use `npm ci` (not `npm install`) for reproducible builds
- `npm prune --omit=dev` removes dev dependencies
- Built-in `node` user (UID 1000)
- Alpine variant is smallest (~180MB vs 1GB for full Node)

---

### Go Best Practices

**Production-optimized Dockerfile:**
```dockerfile
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Download dependencies first (cached layer)
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Build application
COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/main .

FROM gcr.io/distroless/static-debian12

COPY --from=builder /app/main /app/main
USER nonroot:nonroot
ENTRYPOINT ["/app/main"]
```

**Key Go Considerations:**
- `CGO_ENABLED=0` produces static binary (no libc dependency)
- `-ldflags="-s -w"` strips debug symbols (30-50% smaller)
- Distroless static image (2MB base)
- Cache both `/go/pkg/mod` and build cache
- Final image: 10-30MB

---

### Rust Best Practices

**Production-optimized Dockerfile:**
```dockerfile
FROM rust:1.75-alpine AS builder

RUN apk add --no-cache musl-dev

WORKDIR /app

# Cache dependencies
COPY Cargo.toml Cargo.lock ./
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    mkdir src && \
    echo "fn main() {}" > src/main.rs && \
    cargo build --release --target x86_64-unknown-linux-musl && \
    rm -rf src

# Build application
COPY src ./src
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release --target x86_64-unknown-linux-musl && \
    strip target/x86_64-unknown-linux-musl/release/app

FROM scratch

COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/app /app
USER 1000:1000
ENTRYPOINT ["/app"]
```

**Key Rust Considerations:**
- musl target produces static binary
- Dummy build caches dependencies
- `strip` further reduces binary size
- scratch base (0 bytes overhead)
- Final image: 5-15MB

---

## Tool Recommendations

### Base Image Registries

**1. Google Container Registry (GCR) - Distroless**
- **Images:** `gcr.io/distroless/*`
- **Trust:** High (Google-maintained)
- **Use Case:** Maximum security, minimal CVE surface
- **Variants:** static, base, cc, python3, java17, nodejs20

**2. Docker Hub Official Images**
- **Images:** `python:*`, `node:*`, `golang:*`, etc.
- **Trust:** High (Docker Official)
- **Use Case:** General-purpose base images
- **Tip:** Use `-slim` or `-alpine` variants

**3. RedHat Universal Base Image (UBI)**
- **Images:** `registry.access.redhat.com/ubi9/*`
- **Trust:** High (Red Hat)
- **Use Case:** Enterprise environments, RHEL ecosystem

---

### Vulnerability Scanning

**1. Trivy (Recommended)**
```bash
# Scan Docker image
trivy image myimage:latest

# Generate SBOM
trivy image --format cyclonedx --output sbom.json myimage:latest

# Scan Dockerfile
trivy config Dockerfile
```

**Why Trivy?**
- Free and open-source
- Fast scanning (seconds)
- SBOM generation (CycloneDX, SPDX)
- Detects CVEs in OS packages and language dependencies
- Integrates with CI/CD

**2. Docker Scout (Docker Native)**
```bash
# Scan image
docker scout cves myimage:latest

# Compare images
docker scout compare myimage:v1 myimage:v2

# Get recommendations
docker scout recommendations myimage:latest
```

**3. Grype (Anchore)**
```bash
grype myimage:latest
```

---

### BuildKit Configuration

**Enable BuildKit:**
```bash
# Environment variable
export DOCKER_BUILDKIT=1
docker build .

# Or use buildx
docker buildx build .
```

**BuildKit Features:**
- `--mount=type=cache`: Persistent cache across builds
- `--mount=type=secret`: Inject secrets without storing in layers
- `--mount=type=ssh`: SSH agent forwarding
- `--mount=type=bind`: Mount files from other stages
- Parallel stage execution
- Better layer caching

---

### .dockerignore Recommendations

```
# Version control
.git
.gitignore
.gitattributes

# CI/CD
.github
.gitlab-ci.yml
.travis.yml

# IDE
.vscode
.idea
*.swp
*.swo

# Testing
tests/
test/
**/*_test.go
**/*.test.js
coverage/
.pytest_cache/

# Documentation
*.md
docs/
LICENSE

# Build artifacts (managed separately)
node_modules/
dist/
build/
target/
__pycache__/
*.pyc
.next/

# Environment files
.env
.env.local
*.log

# OS files
.DS_Store
Thumbs.db
```

---

## Skill Structure Design

### SKILL.md Structure (When Implementing)

```markdown
---
name: writing-dockerfiles
description: Writing optimized, secure, multi-stage Dockerfiles with language-specific patterns (Python, Node.js, Go, Rust), BuildKit features, and distroless images. Use when containerizing applications or optimizing existing Dockerfiles.
---

# Writing Dockerfiles

## When to Use This Skill

Trigger this skill when:
- "Write a Dockerfile for..."
- "Optimize this Dockerfile..."
- "Multi-stage build for..."
- "Reduce Docker image size..."
- "Secure Dockerfile with non-root user..."
- "Use distroless image..."

## Quick Start Decision

Ask these questions:
1. What language? → Python, Node.js, Go, Rust, Java?
2. Security critical? → Use distroless runtime
3. Image size priority? → Multi-stage build

Then reference appropriate pattern from references/.

## Language-Specific Patterns

For detailed Dockerfiles by language:
- Python: See reference/python-dockerfiles.md
- Node.js: See reference/nodejs-dockerfiles.md
- Go: See reference/go-dockerfiles.md
- Rust: See reference/rust-dockerfiles.md

## Security Hardening

For security patterns:
- See reference/security-hardening.md

## BuildKit Features

For advanced BuildKit:
- See reference/buildkit-features.md

## Validation

To validate Dockerfile quality:
- Run: `scripts/validate_dockerfile.py`
```

---

### Bundled Resources Structure

```
writing-dockerfiles/
├── SKILL.md                           # Main skill file (300-400 lines)
├── reference/
│   ├── python-dockerfiles.md          # Python patterns (pip, poetry, uv)
│   ├── nodejs-dockerfiles.md          # Node patterns (npm, pnpm, yarn)
│   ├── go-dockerfiles.md              # Go static binary patterns
│   ├── rust-dockerfiles.md            # Rust musl patterns
│   ├── java-dockerfiles.md            # Java/Maven/Gradle patterns
│   ├── security-hardening.md          # Non-root, distroless, secrets
│   ├── buildkit-features.md           # Cache mounts, secret mounts
│   └── base-image-selection.md        # Distroless vs slim vs alpine
├── scripts/
│   ├── validate_dockerfile.py         # Lint Dockerfile for best practices
│   └── analyze_image_size.sh          # Compare image sizes
└── examples/
    ├── python-fastapi.Dockerfile      # Complete FastAPI example
    ├── nodejs-express.Dockerfile      # Complete Express example
    ├── go-microservice.Dockerfile     # Complete Go API example
    └── rust-actix.Dockerfile          # Complete Rust API example
```

---

### Progressive Disclosure Pattern

**Level 1:** User asks "Write a Dockerfile for Python FastAPI app"

**Level 2:** SKILL.md guides to reference/python-dockerfiles.md

**Level 3:** reference/python-dockerfiles.md shows 3 options:
- Quick (pip, single-stage)
- Production (poetry, multi-stage)
- Maximum security (distroless)

**Level 4:** User chooses "Production" → Full Dockerfile pattern provided

---

## Integration Points

### Upstream Skills (Provide Input)

**`testing-strategies`:**
- Test application locally before containerizing
- Dockerfile should run tests in build stage
- Multi-stage: test stage → build stage → runtime stage

**`security-hardening`:**
- Application security (input validation, auth) before Docker layer
- Secrets management (environment variables, vaults)

---

### Downstream Skills (Consume Dockerfiles)

**`building-ci-pipelines`:**
- Build Docker images in CI
- Push to container registry
- Scan images for vulnerabilities
- Tag with git commit SHA

**`kubernetes-operations`:**
- Deploy containers to K8s clusters
- Reference images in pod specs
- Health checks translate to K8s liveness/readiness probes

**`infrastructure-as-code`:**
- Terraform/Pulumi provision infrastructure
- Deploy containerized applications to cloud (ECS, Cloud Run, etc.)

---

### Parallel Skills (Related Context)

**`secret-management`:**
- Inject secrets into containers at runtime
- Use BuildKit secret mounts for build-time secrets
- Kubernetes secrets, AWS Secrets Manager, HashiCorp Vault

**`observability`:**
- Container logging (stdout/stderr)
- Metrics collection (Prometheus exporters)
- Tracing (OpenTelemetry)

---

## Implementation Roadmap

### Phase 1: Core SKILL.md (Week 1)
- [ ] Write SKILL.md frontmatter and main guidance
- [ ] Decision tree for base image selection
- [ ] Quick reference table: Language → Pattern file
- [ ] Integration with BuildKit (enable BuildKit instructions)

### Phase 2: Language-Specific References (Week 2)
- [ ] reference/python-dockerfiles.md (pip, poetry, uv)
- [ ] reference/nodejs-dockerfiles.md (npm, pnpm, yarn)
- [ ] reference/go-dockerfiles.md (static binaries, distroless)
- [ ] reference/rust-dockerfiles.md (musl, scratch base)

### Phase 3: Security & Advanced (Week 3)
- [ ] reference/security-hardening.md (non-root, distroless, secrets)
- [ ] reference/buildkit-features.md (cache/secret/ssh mounts)
- [ ] reference/base-image-selection.md (distroless vs slim vs alpine)

### Phase 4: Scripts & Validation (Week 4)
- [ ] scripts/validate_dockerfile.py (linting, best practice checks)
- [ ] scripts/analyze_image_size.sh (compare before/after optimization)

### Phase 5: Examples & Testing (Week 5)
- [ ] examples/ directory with complete, working Dockerfiles
- [ ] Test each example builds successfully
- [ ] Document expected image sizes
- [ ] Create evaluations (3+ test scenarios)

### Phase 6: Iteration & Refinement (Week 6)
- [ ] Test with Haiku, Sonnet, Opus
- [ ] Gather feedback from real usage
- [ ] Refine SKILL.md based on observations
- [ ] Ensure conciseness (SKILL.md <500 lines)

---

## Evaluation Scenarios

### Evaluation 1: Python FastAPI Application

**Task:** "Write a production-ready Dockerfile for a Python FastAPI application using Poetry for dependency management. The app should run as a non-root user."

**Success Criteria:**
- Multi-stage build (builder + runtime)
- Poetry for dependency management
- python:3.12-slim base image
- Non-root user created and used
- Virtual environment copied to runtime
- Port exposed (8000)
- Health check included
- .dockerignore recommended

**Expected Image Size:** 200-400MB

---

### Evaluation 2: Go Microservice (Minimal)

**Task:** "Write the smallest possible Dockerfile for a Go microservice. Security and image size are top priorities."

**Success Criteria:**
- Multi-stage build (builder + distroless)
- CGO_ENABLED=0 for static binary
- Distroless static base image
- ldflags="-s -w" for stripped binary
- nonroot user
- BuildKit cache mounts for go modules
- Final image <30MB

**Expected Image Size:** 10-30MB

---

### Evaluation 3: Node.js with Private npm Registry

**Task:** "Write a Dockerfile for a Node.js application that installs packages from a private npm registry. The NPM_TOKEN must not leak into the image layers."

**Success Criteria:**
- Multi-stage build
- BuildKit secret mount for NPM_TOKEN
- `.npmrc` configured with registry auth
- Secret never in layer history
- Production dependencies only in runtime
- Node user (non-root)
- Instructions for build command with --secret flag

**Expected Image Size:** 150-300MB

---

## Summary

This skill provides:

✅ **Multi-stage build patterns** for all major languages (Python, Node.js, Go, Rust, Java)
✅ **Security hardening** with distroless images and non-root users
✅ **BuildKit advanced features** (cache mounts, secret mounts, SSH forwarding)
✅ **Language-specific optimizations** (package manager caching, static linking)
✅ **Decision frameworks** for base image selection and architecture
✅ **Tool recommendations** for vulnerability scanning and image optimization
✅ **Progressive disclosure** structure for efficient context management

**Primary Value:**
- Reduce image sizes by 80-95% (2GB → 50MB)
- Minimize CVE exposure by 60-80% (distroless)
- Speed up builds by 5-10x (BuildKit caching)
- Establish production-grade containerization standards

**Integration:**
- Upstream: `testing-strategies`, `security-hardening`
- Downstream: `building-ci-pipelines`, `kubernetes-operations`, `infrastructure-as-code`
- Parallel: `secret-management`, `observability`

---

**Status:** Ready for SKILL.md implementation
**Next Step:** Write SKILL.md (300-400 lines) with references to bundled resources
**Target Token Usage:** 2,000-5,000 tokens (Low Level skill)
