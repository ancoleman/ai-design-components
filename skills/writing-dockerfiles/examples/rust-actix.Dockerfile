# Production-Ready Rust Actix-web Application Dockerfile
#
# This example demonstrates:
# - Multi-stage build with scratch runtime
# - musl static linking for zero dependencies
# - Dependency caching with dummy build
# - BuildKit cache mounts for cargo registry
# - Binary stripping for minimal size
# - Ultra-small final image
#
# Expected image size: 8-12MB
#
# Build: docker build -f rust-actix.Dockerfile -t actix-app:latest .
# Run: docker run -p 8080:8080 actix-app:latest

# syntax=docker/dockerfile:1
FROM rust:1.75-alpine AS builder

# Install musl build tools for static linking
RUN apk add --no-cache musl-dev

WORKDIR /app

# Cache dependencies layer (dummy build technique)
COPY Cargo.toml Cargo.lock ./
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    mkdir src && \
    echo "fn main() {}" > src/main.rs && \
    cargo build --release --target x86_64-unknown-linux-musl && \
    rm -rf src

# Build actual application
COPY src ./src
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release --target x86_64-unknown-linux-musl && \
    strip target/x86_64-unknown-linux-musl/release/app

# Runtime stage: scratch (empty base, 0 bytes overhead)
FROM scratch

# Copy only the static binary
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/app /app

# Run as non-root (numeric UID only in scratch)
USER 1000:1000

EXPOSE 8080

ENTRYPOINT ["/app"]
