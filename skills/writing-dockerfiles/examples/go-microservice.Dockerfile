# Production-Ready Go Microservice Dockerfile
#
# This example demonstrates:
# - Multi-stage build with distroless runtime
# - Static binary compilation (CGO_ENABLED=0)
# - BuildKit cache mounts for Go modules and build cache
# - Binary stripping for minimal size
# - Non-root user (nonroot in distroless)
# - Distroless static base (smallest possible)
#
# Expected image size: 10-30MB
#
# Build: docker build -f go-microservice.Dockerfile -t go-api:latest .
# Run: docker run -p 8080:8080 go-api:latest

# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Download dependencies first (cached layer)
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Verify dependencies
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod verify

# Copy source code
COPY . .

# Build static binary with optimizations
# - CGO_ENABLED=0: Static binary, no libc dependency
# - -ldflags="-s -w": Strip debug symbols (30-50% smaller)
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-s -w" -o /app/main .

# Runtime stage: distroless static (minimal base)
FROM gcr.io/distroless/static-debian12

# Copy static binary from builder
COPY --from=builder /app/main /app/main

# Use built-in nonroot user (UID 65532)
USER nonroot:nonroot

EXPOSE 8080

ENTRYPOINT ["/app/main"]
