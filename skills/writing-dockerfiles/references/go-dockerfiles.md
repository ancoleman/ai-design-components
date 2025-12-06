# Go Dockerfiles

Complete patterns for containerizing Go applications with minimal image sizes.

## Table of Contents

1. [Why Go is Perfect for Docker](#why-go-is-perfect-for-docker)
2. [Base Image Selection](#base-image-selection)
3. [Pattern 1: Distroless Static (Smallest)](#pattern-1-distroless-static-smallest)
4. [Pattern 2: Alpine Runtime](#pattern-2-alpine-runtime)
5. [Pattern 3: Scratch Base (Advanced)](#pattern-3-scratch-base-advanced)
6. [Build Optimization Techniques](#build-optimization-techniques)
7. [Common Go Pitfalls](#common-go-pitfalls)

## Why Go is Perfect for Docker

**Go's advantages for containerization:**
- **Static binaries**: Single executable with no external dependencies
- **Small size**: 5-30MB final images with distroless/scratch
- **Fast startup**: No JVM warmup or interpreter overhead
- **Cross-compilation**: Build for Linux on any platform
- **No runtime**: Unlike Python/Node.js, no language runtime needed

**Typical image sizes:**
- Go + distroless/static: 10-30MB
- Go + alpine: 15-35MB
- Go + scratch: 5-20MB
- Python equivalent: 200-400MB
- Node.js equivalent: 180-320MB

## Base Image Selection

**Recommended Go base images:**

| Build Stage | Runtime Stage | Final Size | Use Case |
|-------------|---------------|------------|----------|
| `golang:1.22-alpine` | `gcr.io/distroless/static-debian12` | 10-30MB | Production (recommended) |
| `golang:1.22-alpine` | `alpine:3.19` | 15-35MB | Need shell for debugging |
| `golang:1.22-alpine` | `scratch` | 5-20MB | Maximum minimalism |
| `golang:1.22` | `gcr.io/distroless/base-debian12` | 15-35MB | CGO dependencies |

**Version pinning:**
```dockerfile
# ✅ Good: Exact version
FROM golang:1.22.0-alpine

# ⚠️ OK: Minor version pinned
FROM golang:1.22-alpine

# ❌ Bad: Unpredictable
FROM golang:alpine
FROM golang:latest
```

## Pattern 1: Distroless Static (Smallest)

**Use when:**
- Pure Go code (no CGO)
- Production deployments
- Security is priority
- Minimal image size needed

**Multi-stage Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Download dependencies first (cached layer)
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Copy source code
COPY . .

# Build static binary
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-s -w" -o /app/main .

# Runtime stage: distroless static
FROM gcr.io/distroless/static-debian12

COPY --from=builder /app/main /app/main

# Use built-in nonroot user (UID 65532)
USER nonroot:nonroot

EXPOSE 8080

ENTRYPOINT ["/app/main"]
```

**Key build flags explained:**
- `CGO_ENABLED=0` → Disable CGO, produce pure static binary
- `GOOS=linux` → Target Linux (default, explicit for clarity)
- `GOARCH=amd64` → Target amd64 (or arm64 for ARM)
- `-ldflags="-s -w"` → Strip debug symbols (30-50% smaller)
  - `-s` → Omit symbol table
  - `-w` → Omit DWARF debug info

**Build command:**
```bash
docker build -t myapp:latest .
```

**Expected size:** 10-30MB

## Pattern 2: Alpine Runtime

**Use when:**
- Need shell access for debugging
- Need to install runtime packages
- Slightly larger image acceptable

**Multi-stage Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Download dependencies
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Copy source code
COPY . .

# Build static binary
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/main .

# Runtime stage: Alpine
FROM alpine:3.19

# Install CA certificates (for HTTPS requests)
RUN apk --no-cache add ca-certificates

WORKDIR /app

COPY --from=builder /app/main /app/main

# Create non-root user
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

ENTRYPOINT ["/app/main"]
```

**When to use Alpine runtime:**
- Need `sh` shell for debugging
- Need runtime utilities (`curl`, `wget`)
- Need to install packages at runtime

**Build command:**
```bash
docker build -t myapp:latest .
```

**Expected size:** 15-35MB

## Pattern 3: Scratch Base (Advanced)

**Use when:**
- Absolute minimum size required
- Static binary with zero dependencies
- No HTTPS calls (no CA certs needed)

**Multi-stage Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Download dependencies
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Copy source code
COPY . .

# Build completely static binary
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags="-s -w -extldflags '-static'" -o /app/main .

# Runtime stage: scratch (empty base)
FROM scratch

# Copy CA certificates from builder (if HTTPS needed)
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copy binary
COPY --from=builder /app/main /app/main

# Run as non-root (numeric UID only, no user creation possible)
USER 1000:1000

EXPOSE 8080

ENTRYPOINT ["/app/main"]
```

**Scratch base limitations:**
- No shell (cannot `docker exec -it`)
- No utilities (no debugging tools)
- Cannot install packages
- Numeric UID only (no username resolution)

**When scratch works:**
- Pure Go services
- No debugging needed in production
- Maximum security posture

**Build command:**
```bash
docker build -t myapp:latest .
```

**Expected size:** 5-20MB

## Build Optimization Techniques

### Technique 1: Layer Caching for Dependencies

**Problem:** Re-downloads all modules on every code change.

```dockerfile
# ❌ Re-downloads modules on every build
COPY . .
RUN go mod download
```

**Solution:** Copy go.mod/go.sum first, cache layer:
```dockerfile
# ✅ Cached layer if dependencies unchanged
COPY go.mod go.sum ./
RUN go mod download

# Code changes don't invalidate dependency cache
COPY . .
RUN go build -o main .
```

### Technique 2: BuildKit Cache Mounts

**Without cache mount:**
```dockerfile
# ❌ Re-downloads every build
RUN go mod download
```

**With cache mount:**
```dockerfile
# ✅ Persistent cache across builds
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download
```

**Dual cache mounts (dependencies + build cache):**
```dockerfile
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o main .
```

**Speed improvement:** 5-10x faster rebuilds.

### Technique 3: Stripping Debug Symbols

**Default build (with debug symbols):**
```dockerfile
RUN go build -o main .
# Binary size: 20MB
```

**Stripped build:**
```dockerfile
RUN go build -ldflags="-s -w" -o main .
# Binary size: 12MB (40% smaller)
```

**Advanced stripping:**
```dockerfile
RUN go build -ldflags="-s -w -extldflags '-static'" -o main .
# Additional flags for static linking
```

### Technique 4: Multi-Architecture Builds

**Build for multiple platforms:**
```dockerfile
ARG TARGETOS=linux
ARG TARGETARCH=amd64

RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
    go build -ldflags="-s -w" -o /app/main .
```

**Build command:**
```bash
# Build for amd64
docker buildx build --platform linux/amd64 -t myapp:amd64 .

# Build for arm64
docker buildx build --platform linux/arm64 -t myapp:arm64 .

# Build for both (multi-arch)
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .
```

## Common Go Pitfalls

### Pitfall 1: CGO Enabled with Distroless/Scratch

**Problem:** CGO requires libc, which distroless/static doesn't have.

```dockerfile
# ❌ This will fail at runtime
FROM golang:1.22-alpine AS builder
RUN go build -o main .  # CGO_ENABLED=1 by default

FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/main /app/main
ENTRYPOINT ["/app/main"]
# Runtime error: binary needs libc
```

**Solution 1:** Disable CGO:
```dockerfile
# ✅ Static binary
RUN CGO_ENABLED=0 go build -o main .

FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/main /app/main
ENTRYPOINT ["/app/main"]
```

**Solution 2:** Use distroless/base (includes libc):
```dockerfile
# ✅ Dynamic binary with libc
RUN go build -o main .  # CGO_ENABLED=1

FROM gcr.io/distroless/base-debian12
COPY --from=builder /app/main /app/main
ENTRYPOINT ["/app/main"]
```

### Pitfall 2: Missing CA Certificates for HTTPS

**Problem:** HTTPS calls fail without CA certificates.

```dockerfile
FROM scratch
COPY --from=builder /app/main /app/main
ENTRYPOINT ["/app/main"]
# Runtime error: x509: certificate signed by unknown authority
```

**Solution:** Copy CA certificates from builder:
```dockerfile
FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/main /app/main
ENTRYPOINT ["/app/main"]
```

**Alternative:** Use distroless (includes CA certs):
```dockerfile
FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/main /app/main
ENTRYPOINT ["/app/main"]
```

### Pitfall 3: Not Using go.sum for Verification

**Problem:** Dependencies change unexpectedly.

```dockerfile
# ❌ No checksum verification
COPY go.mod ./
RUN go mod download
```

**Solution:** Copy go.sum for verification:
```dockerfile
# ✅ Checksum verification
COPY go.mod go.sum ./
RUN go mod download
```

### Pitfall 4: Large Binary Due to Debug Symbols

**Problem:** Binary includes debug symbols, stack traces, etc.

```dockerfile
# ❌ 20MB binary
RUN go build -o main .
```

**Solution:** Strip symbols with ldflags:
```dockerfile
# ✅ 12MB binary (40% smaller)
RUN go build -ldflags="-s -w" -o main .
```

### Pitfall 5: Running as Root

**Problem:** Security risk.

```dockerfile
# ❌ Runs as root
FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/main /app/main
ENTRYPOINT ["/app/main"]
```

**Solution:** Use nonroot user:
```dockerfile
# ✅ Runs as UID 65532
FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/main /app/main
USER nonroot:nonroot
ENTRYPOINT ["/app/main"]
```

## HTTP Server Complete Example

**Production-ready Go HTTP server:**

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Download dependencies
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Copy source code
COPY . .

# Build static binary
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server ./cmd/server

# Runtime stage
FROM gcr.io/distroless/static-debian12

COPY --from=builder /app/server /app/server

USER nonroot:nonroot

EXPOSE 8080

ENTRYPOINT ["/app/server"]
```

**main.go (cmd/server/main.go):**
```go
package main

import (
    "fmt"
    "log"
    "net/http"
)

func main() {
    http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
        fmt.Fprintf(w, "OK")
    })

    log.Println("Server starting on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatal(err)
    }
}
```

**go.mod:**
```go
module github.com/myuser/myapp

go 1.22
```

**Expected size:** 10-15MB

## Gin Framework Complete Example

**Production-ready Gin API:**

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Download dependencies
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Verify dependencies
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod verify

# Copy source code
COPY . .

# Build static binary
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server .

# Runtime stage
FROM gcr.io/distroless/static-debian12

COPY --from=builder /app/server /app/server

USER nonroot:nonroot

EXPOSE 8080

ENTRYPOINT ["/app/server"]
```

**main.go:**
```go
package main

import (
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()

    r.GET("/health", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "status": "healthy",
        })
    })

    r.Run(":8080")
}
```

**Expected size:** 15-25MB

## gRPC Service Complete Example

**Production-ready gRPC service:**

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder

# Install protobuf compiler (if generating protos)
RUN apk add --no-cache protobuf-dev

WORKDIR /app

# Download dependencies
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Copy source code
COPY . .

# Generate protobuf code (if needed)
# RUN go generate ./...

# Build static binary
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server ./cmd/server

# Runtime stage
FROM gcr.io/distroless/static-debian12

COPY --from=builder /app/server /app/server

USER nonroot:nonroot

EXPOSE 50051

ENTRYPOINT ["/app/server"]
```

**Expected size:** 20-35MB (includes gRPC libraries)

## Private Go Module Example

**Using BuildKit secret mount for GITHUB_TOKEN:**

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Configure git to use token
RUN apk add --no-cache git

# Download dependencies using secret
COPY go.mod go.sum ./
RUN --mount=type=secret,id=github_token \
    --mount=type=cache,target=/go/pkg/mod \
    git config --global url."https://$(cat /run/secrets/github_token)@github.com/".insteadOf "https://github.com/" && \
    go mod download

# Copy source and build
COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/main .

# Runtime stage
FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/main /app/main
USER nonroot:nonroot
ENTRYPOINT ["/app/main"]
```

**Build command:**
```bash
echo "ghp_your_token" > github_token.txt
docker buildx build --secret id=github_token,src=github_token.txt -t myapp:latest .
rm github_token.txt
```

## Summary

**Go Dockerfile patterns ranked:**

| Pattern | Size | Security | Debug-ability | Use Case |
|---------|------|----------|---------------|----------|
| Distroless static | 10-30MB | Highest | None | Production (recommended) |
| Alpine | 15-35MB | High | Shell access | Development, debugging |
| Scratch | 5-20MB | Highest | None | Ultra-minimal production |
| Distroless base | 15-35MB | High | None | CGO dependencies |

**Key takeaways:**
- Always use multi-stage builds
- Disable CGO for static binaries (`CGO_ENABLED=0`)
- Strip symbols with `-ldflags="-s -w"` (30-50% smaller)
- Use BuildKit cache mounts for `/go/pkg/mod` and build cache
- Use distroless/static for production (smallest + most secure)
- Copy go.mod/go.sum before source code (layer caching)
- Use nonroot:nonroot user in distroless
- Copy CA certificates if making HTTPS calls
- Pin Go version in base image
- Final images: 10-30MB (vs 200-400MB for Python/Node.js)
