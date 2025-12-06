# BuildKit Advanced Features

Comprehensive guide to Docker BuildKit's advanced features for faster, more secure builds.

## Table of Contents

1. [Enabling BuildKit](#enabling-buildkit)
2. [Cache Mounts](#cache-mounts)
3. [Secret Mounts](#secret-mounts)
4. [SSH Mounts](#ssh-mounts)
5. [Bind Mounts](#bind-mounts)
6. [Parallel Stage Execution](#parallel-stage-execution)
7. [BuildKit Syntax](#buildkit-syntax)

## Enabling BuildKit

**BuildKit benefits:**
- Parallel stage execution
- Advanced caching mechanisms
- Secret and SSH mounts
- Better layer caching
- 20-50% faster builds

### Method 1: Environment Variable

```bash
export DOCKER_BUILDKIT=1
docker build -t myapp:latest .
```

### Method 2: Docker Buildx (Recommended)

```bash
# Buildx is built-in to Docker Desktop
docker buildx build -t myapp:latest .

# Create and use buildx builder
docker buildx create --name mybuilder --use
docker buildx build -t myapp:latest .
```

### Method 3: Daemon Configuration

**Edit `/etc/docker/daemon.json`:**
```json
{
  "features": {
    "buildkit": true
  }
}
```

**Restart Docker:**
```bash
sudo systemctl restart docker
```

### Method 4: Per-Dockerfile (Syntax Directive)

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim
# ... rest of Dockerfile
```

**This enables BuildKit features even without environment variable.**

## Cache Mounts

**Purpose:** Persist package manager caches across builds.

**Without cache mount:**
```dockerfile
# ❌ Re-downloads every build (60s)
RUN pip install -r requirements.txt
```

**With cache mount:**
```dockerfile
# ✅ Persistent cache (5s on rebuild)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

**Speed improvement:** 10-100x faster on cache hit.

### Python Cache Mounts

**pip:**
```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

**poetry:**
```dockerfile
RUN --mount=type=cache,target=/root/.cache/pypoetry \
    poetry install --no-dev
```

**uv:**
```dockerfile
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev
```

### Node.js Cache Mounts

**npm:**
```dockerfile
RUN --mount=type=cache,target=/root/.npm \
    npm ci
```

**pnpm:**
```dockerfile
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile
```

**yarn:**
```dockerfile
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn \
    yarn install --frozen-lockfile
```

### Go Cache Mounts

**Module cache:**
```dockerfile
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download
```

**Build cache:**
```dockerfile
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o main .
```

### Rust Cache Mounts

**Cargo registry:**
```dockerfile
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    cargo build --release
```

**Target directory (build artifacts):**
```dockerfile
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release
```

### APT/APK Cache Mounts

**Debian/Ubuntu (apt):**
```dockerfile
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y build-essential
```

**Alpine (apk):**
```dockerfile
RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache build-base
```

### Cache Mount Options

**Full syntax:**
```dockerfile
RUN --mount=type=cache,target=/path/to/cache,id=unique-id,sharing=shared,mode=0755,uid=1000,gid=1000 \
    command
```

**Parameters:**
- `target` → Directory to cache (required)
- `id` → Unique cache identifier (default: hash of target)
- `sharing` → `shared` (default), `locked`, or `private`
- `mode` → Directory permissions (default: 0755)
- `uid`/`gid` → Owner UID/GID

**Sharing modes:**
- `shared` → Multiple builds can read/write simultaneously
- `locked` → One build at a time (safer for apt/yum)
- `private` → Exclusive cache per build

### Managing Cache

**Inspect cache:**
```bash
docker buildx du
```

**Prune cache:**
```bash
# Remove unused cache
docker buildx prune

# Remove all cache
docker buildx prune --all

# Remove cache older than 7 days
docker buildx prune --filter until=168h
```

## Secret Mounts

**Purpose:** Inject secrets during build without storing in layers.

**Key principle:** Secrets available during RUN command, but NOT stored in image.

### Pattern 1: Token from File

**Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app

# Use secret to install from private registry
RUN --mount=type=secret,id=pypi_token \
    pip config set global.index-url https://$(cat /run/secrets/pypi_token)@pypi.example.com/simple && \
    pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]
```

**Build command:**
```bash
echo "my_token_here" > pypi_token.txt
docker buildx build --secret id=pypi_token,src=pypi_token.txt -t myapp:latest .
rm pypi_token.txt
```

**How it works:**
- Secret mounted at `/run/secrets/pypi_token` during build
- Accessible only during RUN command execution
- NOT stored in image layers or history

### Pattern 2: Token from Environment Variable

**Dockerfile (same as above):**
```dockerfile
RUN --mount=type=secret,id=pypi_token \
    pip config set global.index-url https://$(cat /run/secrets/pypi_token)@pypi.example.com/simple && \
    pip install -r requirements.txt
```

**Build command:**
```bash
export PYPI_TOKEN="my_token_here"
echo "$PYPI_TOKEN" | docker buildx build --secret id=pypi_token,src=- -t myapp:latest .
```

### Pattern 3: Multiple Secrets

**Dockerfile:**
```dockerfile
RUN --mount=type=secret,id=npm_token \
    --mount=type=secret,id=github_token \
    echo "//registry.npmjs.org/:_authToken=$(cat /run/secrets/npm_token)" > ~/.npmrc && \
    git config --global url."https://$(cat /run/secrets/github_token)@github.com/".insteadOf "https://github.com/" && \
    npm ci
```

**Build command:**
```bash
docker buildx build \
  --secret id=npm_token,src=npm_token.txt \
  --secret id=github_token,src=github_token.txt \
  -t myapp:latest .
```

### Pattern 4: .netrc for Go Modules

**Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Download private Go modules using .netrc
RUN --mount=type=secret,id=netrc,target=/root/.netrc \
    go mod download

COPY . .
RUN go build -o main .

FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/main /app/main
USER nonroot:nonroot
ENTRYPOINT ["/app/main"]
```

**.netrc file:**
```
machine github.com
login your-username
password ghp_your_token
```

**Build command:**
```bash
docker buildx build --secret id=netrc,src=.netrc -t myapp:latest .
```

### Pattern 5: AWS Credentials

**Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Install AWS CLI
RUN pip install awscli

# Download from S3 using AWS credentials
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
    aws s3 cp s3://my-private-bucket/data.tar.gz /app/data.tar.gz && \
    tar -xzf /app/data.tar.gz -C /app

CMD ["python", "app.py"]
```

**Build command:**
```bash
docker buildx build --secret id=aws,src=$HOME/.aws/credentials -t myapp:latest .
```

### Secret Mount Options

**Full syntax:**
```dockerfile
RUN --mount=type=secret,id=my_secret,target=/run/secrets/my_secret,required=true,mode=0400,uid=1000 \
    command
```

**Parameters:**
- `id` → Secret identifier (required)
- `target` → Mount path (default: `/run/secrets/{id}`)
- `required` → Fail if secret missing (default: false)
- `mode` → File permissions (default: 0400)
- `uid`/`gid` → Owner UID/GID

## SSH Mounts

**Purpose:** Use SSH keys for git clones without storing in image.

### Pattern 1: Clone Private Repo

**Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM alpine

# Install git and SSH client
RUN apk add --no-cache git openssh-client

# Clone private repository using SSH
RUN --mount=type=ssh \
    mkdir -p ~/.ssh && \
    ssh-keyscan github.com >> ~/.ssh/known_hosts && \
    git clone git@github.com:myorg/private-repo.git /app

WORKDIR /app
CMD ["./start.sh"]
```

**Build command:**
```bash
# Start ssh-agent and add key
eval $(ssh-agent)
ssh-add ~/.ssh/id_rsa

# Build with SSH forwarding
docker buildx build --ssh default -t myapp:latest .
```

### Pattern 2: Multiple SSH Keys

**Dockerfile:**
```dockerfile
RUN --mount=type=ssh,id=github \
    --mount=type=ssh,id=gitlab \
    git clone git@github.com:org/repo1.git && \
    git clone git@gitlab.com:org/repo2.git
```

**Build command:**
```bash
docker buildx build \
  --ssh github=~/.ssh/github_key \
  --ssh gitlab=~/.ssh/gitlab_key \
  -t myapp:latest .
```

### SSH Mount Options

**Full syntax:**
```dockerfile
RUN --mount=type=ssh,id=default,target=/root/.ssh/id_rsa,required=true,mode=0600 \
    git clone git@github.com:private/repo.git
```

**Parameters:**
- `id` → SSH key identifier (default: `default`)
- `target` → Mount path (default: auto-configured)
- `required` → Fail if key missing (default: false)
- `mode` → File permissions (default: 0600)

## Bind Mounts

**Purpose:** Mount files from other stages or host without COPY.

### Pattern 1: Mount from Build Context

**Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Mount go.mod temporarily (don't copy)
RUN --mount=type=bind,source=go.mod,target=go.mod \
    --mount=type=bind,source=go.sum,target=go.sum \
    --mount=type=cache,target=/go/pkg/mod \
    go mod download

COPY . .
RUN go build -o main .

FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/main /app/main
ENTRYPOINT ["/app/main"]
```

**Benefits:**
- Faster than COPY for large files
- Doesn't create intermediate layer

### Pattern 2: Mount from Another Stage

**Dockerfile:**
```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app

# Mount node_modules from deps stage
RUN --mount=type=bind,from=deps,source=/app/node_modules,target=/app/node_modules \
    npm run build

FROM node:20-alpine
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
```

### Bind Mount Options

**Full syntax:**
```dockerfile
RUN --mount=type=bind,source=src,target=dst,from=stage,rw=true \
    command
```

**Parameters:**
- `source` → Source path (default: build context root)
- `target` → Mount path in container (required)
- `from` → Source stage name (default: build context)
- `rw` → Read-write mount (default: false, read-only)

## Parallel Stage Execution

**BuildKit automatically parallelizes independent stages.**

**Sequential execution (old Docker):**
```dockerfile
FROM base AS stage1
RUN task1

FROM base AS stage2
RUN task2  # Waits for stage1

FROM stage1 AS final
COPY --from=stage2 /output /output
```

**With BuildKit:**
- `stage1` and `stage2` run in parallel
- `final` waits for both

### Pattern: Parallel Builds

**Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM golang:1.22-alpine AS backend-builder
WORKDIR /app/backend
COPY backend/go.mod backend/go.sum ./
RUN go mod download
COPY backend/ ./
RUN go build -o server .

# Both stages build in parallel
FROM alpine:3.19
COPY --from=frontend-builder /app/frontend/dist /app/public
COPY --from=backend-builder /app/backend/server /app/server
CMD ["/app/server"]
```

**BuildKit parallelizes frontend-builder and backend-builder.**

### Viewing Build Graph

```bash
# Show build graph
docker buildx build --print=outline .

# Show build provenance
docker buildx build --provenance=true --sbom=true -t myapp:latest .
```

## BuildKit Syntax

**Specify BuildKit version:**
```dockerfile
# syntax=docker/dockerfile:1.6
```

**Available versions:**
- `docker/dockerfile:1` → Latest stable (recommended)
- `docker/dockerfile:1.6` → Specific version
- `docker/dockerfile:labs` → Experimental features

### Experimental Features (Labs)

**Enable labs:**
```dockerfile
# syntax=docker/dockerfile:1-labs
```

**Features:**
- `RUN --network=none` → Disable network during RUN
- `COPY --parents` → Preserve directory structure
- `COPY --exclude` → Exclude patterns

**Example:**
```dockerfile
# syntax=docker/dockerfile:1-labs
FROM alpine

# Disable network for security
RUN --network=none \
    apk add --no-cache ca-certificates

# Copy with exclusions
COPY --exclude=*.test.js . /app
```

## Complete BuildKit Example

**Production-optimized Dockerfile using all features:**

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS deps

WORKDIR /app

# Cache npm packages
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Builder stage
FROM node:20-alpine AS builder

WORKDIR /app

# Mount node_modules from deps
RUN --mount=type=bind,from=deps,source=/app/node_modules,target=/app/node_modules \
    --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=tsconfig.json,target=tsconfig.json \
    --mount=type=bind,source=src,target=src \
    npm run build

# Install private packages using secret
RUN --mount=type=secret,id=npm_token \
    --mount=type=cache,target=/root/.npm \
    echo "//registry.npmjs.org/:_authToken=$(cat /run/secrets/npm_token)" > ~/.npmrc && \
    npm ci --omit=dev && \
    rm ~/.npmrc

# Runtime stage
FROM node:20-alpine

WORKDIR /app

# Copy production files
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

# Non-root user
USER node

ENV NODE_ENV=production

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Build command:**
```bash
docker buildx build \
  --secret id=npm_token,src=npm_token.txt \
  --cache-from type=registry,ref=myapp:cache \
  --cache-to type=registry,ref=myapp:cache,mode=max \
  -t myapp:latest \
  --push \
  .
```

**Features used:**
- ✅ Multi-stage build
- ✅ Cache mounts (npm)
- ✅ Secret mounts (private packages)
- ✅ Bind mounts (avoid COPY for temporary files)
- ✅ Parallel stage execution
- ✅ Remote cache (registry)

## Summary

**BuildKit features ranked by impact:**

| Feature | Speed Improvement | Security Improvement | Use Case |
|---------|------------------|---------------------|----------|
| Cache mounts | 10-100x | None | Package managers |
| Secret mounts | None | Critical | Private registries |
| Parallel stages | 2-4x | None | Multi-component builds |
| SSH mounts | None | High | Private git repos |
| Bind mounts | 20-50% | None | Large temporary files |

**Key takeaways:**
- Always enable BuildKit (`# syntax=docker/dockerfile:1`)
- Use cache mounts for all package managers (10-100x faster)
- Use secret mounts for credentials (never ENV vars)
- Use SSH mounts for private git clones
- BuildKit automatically parallelizes independent stages
- Cache is persistent across builds (manage with `docker buildx du/prune`)
- Bind mounts avoid intermediate layers for temporary files
