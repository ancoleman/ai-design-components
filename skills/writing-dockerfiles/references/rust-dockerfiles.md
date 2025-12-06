# Rust Dockerfiles

Complete patterns for containerizing Rust applications with ultra-small static binaries.

## Table of Contents

1. [Why Rust Excels at Docker](#why-rust-excels-at-docker)
2. [Base Image Selection](#base-image-selection)
3. [Pattern 1: Scratch Base (Smallest)](#pattern-1-scratch-base-smallest)
4. [Pattern 2: Distroless Static](#pattern-2-distroless-static)
5. [Pattern 3: Alpine Runtime](#pattern-3-alpine-runtime)
6. [Build Optimization Techniques](#build-optimization-techniques)
7. [Common Rust Pitfalls](#common-rust-pitfalls)

## Why Rust Excels at Docker

**Rust's advantages for containerization:**
- **Static binaries**: musl linking produces zero-dependency executables
- **Ultra-small**: 5-15MB final images with scratch base
- **Memory safe**: No runtime overhead, maximum performance
- **No runtime**: Unlike Python/Node.js, just the binary
- **Cross-compilation**: Build for any platform from any platform

**Typical image sizes:**
- Rust + scratch: 5-15MB
- Rust + distroless/static: 8-18MB
- Rust + alpine: 12-25MB
- Go equivalent: 10-30MB
- Python equivalent: 200-400MB

## Base Image Selection

**Recommended Rust base images:**

| Build Stage | Runtime Stage | Final Size | Use Case |
|-------------|---------------|------------|----------|
| `rust:1.75-alpine` | `scratch` | 5-15MB | Production (recommended) |
| `rust:1.75-alpine` | `gcr.io/distroless/static-debian12` | 8-18MB | Need CA certs built-in |
| `rust:1.75-alpine` | `alpine:3.19` | 12-25MB | Need shell for debugging |
| `rust:1.75` | `debian:bookworm-slim` | 20-40MB | Dynamic linking needed |

**Version pinning:**
```dockerfile
# ✅ Good: Exact version
FROM rust:1.75.0-alpine

# ⚠️ OK: Minor version pinned
FROM rust:1.75-alpine

# ❌ Bad: Unpredictable
FROM rust:alpine
FROM rust:latest
```

## Pattern 1: Scratch Base (Smallest)

**Use when:**
- Pure Rust code
- Production deployments
- Absolute minimum size required
- Maximum security posture

**Multi-stage Dockerfile with musl:**
```dockerfile
# syntax=docker/dockerfile:1
FROM rust:1.75-alpine AS builder

# Install musl build tools
RUN apk add --no-cache musl-dev

WORKDIR /app

# Cache dependencies layer (dummy build)
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

# Runtime stage: scratch (empty base)
FROM scratch

# Copy binary only
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/app /app

# Run as non-root (numeric UID only)
USER 1000:1000

EXPOSE 8080

ENTRYPOINT ["/app"]
```

**Key features:**
- musl static linking → No libc dependencies
- scratch base → 0 bytes overhead
- Dummy build → Caches dependencies
- strip → Further reduces binary size
- **Final image: 5-15MB**

**Build command:**
```bash
docker build -t myapp:latest .
```

**Expected size:** 5-15MB

## Pattern 2: Distroless Static

**Use when:**
- Need CA certificates for HTTPS
- Want minimal base with some structure
- Security-critical production

**Multi-stage Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
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

# Runtime stage: distroless static
FROM gcr.io/distroless/static-debian12

COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/app /app/app

# Use built-in nonroot user
USER nonroot:nonroot

EXPOSE 8080

ENTRYPOINT ["/app/app"]
```

**Benefits over scratch:**
- Includes CA certificates (for HTTPS)
- Includes timezone data
- Includes /etc/passwd (for nonroot user)
- Still minimal (2MB base)

**Build command:**
```bash
docker build -t myapp:latest .
```

**Expected size:** 8-18MB

## Pattern 3: Alpine Runtime

**Use when:**
- Need shell access for debugging
- Need runtime utilities
- Slightly larger image acceptable

**Multi-stage Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
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
    cargo build --release --target x86_64-unknown-linux-musl

# Runtime stage: Alpine
FROM alpine:3.19

# Install CA certificates
RUN apk --no-cache add ca-certificates

WORKDIR /app

COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/app /app/app

# Create non-root user
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

ENTRYPOINT ["/app/app"]
```

**When to use Alpine runtime:**
- Development/staging environments
- Need debugging tools
- Need to install runtime packages

**Build command:**
```bash
docker build -t myapp:latest .
```

**Expected size:** 12-25MB

## Build Optimization Techniques

### Technique 1: Dependency Caching

**Problem:** Cargo recompiles all dependencies on every code change.

```dockerfile
# ❌ Recompiles dependencies every time
COPY . .
RUN cargo build --release
```

**Solution:** Dummy build to cache dependencies:
```dockerfile
# ✅ Cached dependencies if Cargo.toml unchanged
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && \
    echo "fn main() {}" > src/main.rs && \
    cargo build --release && \
    rm -rf src

# Now copy real source (dependencies already cached)
COPY src ./src
RUN cargo build --release
```

**Speed improvement:** 10-50x faster rebuilds.

### Technique 2: BuildKit Cache Mounts

**Dual cache mounts:**
```dockerfile
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release --target x86_64-unknown-linux-musl
```

**What's cached:**
- `/usr/local/cargo/registry` → Downloaded crates
- `/app/target` → Compiled artifacts

**Speed improvement:** 5-10x faster rebuilds.

### Technique 3: Binary Stripping

**Default build:**
```dockerfile
RUN cargo build --release
# Binary size: 15MB
```

**Stripped build:**
```dockerfile
RUN cargo build --release && \
    strip target/release/app
# Binary size: 8MB (47% smaller)
```

**Alternative: Cargo.toml profile:**
```toml
[profile.release]
strip = true
lto = true
codegen-units = 1
panic = "abort"
```

### Technique 4: LTO and Size Optimization

**Cargo.toml optimization profile:**
```toml
[profile.release]
opt-level = "z"        # Optimize for size
lto = true             # Link-time optimization
codegen-units = 1      # Single codegen unit (slower build, smaller binary)
strip = true           # Strip symbols
panic = "abort"        # Smaller panic handler
```

**Binary size reduction:** Up to 60% smaller than default release build.

### Technique 5: Multi-Architecture Builds

**Build for multiple platforms:**
```dockerfile
ARG TARGETARCH

FROM rust:1.75-alpine AS builder

RUN apk add --no-cache musl-dev

# Install cross-compilation target
RUN case ${TARGETARCH} in \
    "amd64") RUST_TARGET=x86_64-unknown-linux-musl ;; \
    "arm64") RUST_TARGET=aarch64-unknown-linux-musl ;; \
    *) echo "Unsupported architecture" && exit 1 ;; \
    esac && \
    rustup target add ${RUST_TARGET}

WORKDIR /app

COPY Cargo.toml Cargo.lock ./
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    mkdir src && \
    echo "fn main() {}" > src/main.rs && \
    cargo build --release --target ${RUST_TARGET} && \
    rm -rf src

COPY src ./src
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    cargo build --release --target ${RUST_TARGET}

FROM scratch
ARG TARGETARCH
COPY --from=builder /app/target/${RUST_TARGET}/release/app /app
USER 1000:1000
ENTRYPOINT ["/app"]
```

**Build command:**
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .
```

## Common Rust Pitfalls

### Pitfall 1: Dynamic Linking with Scratch

**Problem:** Default Rust build dynamically links libc.

```dockerfile
# ❌ This will fail at runtime
FROM rust:1.75-alpine AS builder
RUN cargo build --release

FROM scratch
COPY --from=builder /app/target/release/app /app
ENTRYPOINT ["/app"]
# Runtime error: binary needs libc
```

**Solution:** Use musl target for static linking:
```dockerfile
# ✅ Static binary
RUN apk add --no-cache musl-dev
RUN cargo build --release --target x86_64-unknown-linux-musl

FROM scratch
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/app /app
ENTRYPOINT ["/app"]
```

### Pitfall 2: Missing CA Certificates for HTTPS

**Problem:** HTTPS calls fail without CA certificates.

```dockerfile
FROM scratch
COPY --from=builder /app/target/release/app /app
ENTRYPOINT ["/app"]
# Runtime error: certificate signed by unknown authority
```

**Solution 1:** Copy CA certs from builder:
```dockerfile
FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/target/release/app /app
ENTRYPOINT ["/app"]
```

**Solution 2:** Use distroless (includes CA certs):
```dockerfile
FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/target/release/app /app
ENTRYPOINT ["/app"]
```

### Pitfall 3: Not Caching Dependencies

**Problem:** Rebuilds all dependencies on every code change.

```dockerfile
# ❌ Recompiles everything
COPY . .
RUN cargo build --release
# Takes 10+ minutes every build
```

**Solution:** Dummy build for dependency caching:
```dockerfile
# ✅ Dependencies cached
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs && \
    cargo build --release && \
    rm -rf src

COPY src ./src
RUN cargo build --release
# Takes 30 seconds for incremental builds
```

### Pitfall 4: Large Binary Due to Debug Info

**Problem:** Binary includes debug symbols, stack traces, etc.

```dockerfile
# ❌ 15MB binary
RUN cargo build --release
```

**Solution:** Strip symbols:
```dockerfile
# ✅ 8MB binary
RUN cargo build --release && \
    strip target/release/app
```

**Better:** Configure in Cargo.toml:
```toml
[profile.release]
strip = true
```

### Pitfall 5: Slow Builds Without LTO

**Problem:** Cargo builds quickly but binaries are larger.

**Solution:** Enable LTO in Cargo.toml:
```toml
[profile.release]
lto = true          # Link-time optimization
codegen-units = 1   # Better optimization, slower build
```

**Trade-off:**
- Build time: 2-3x slower
- Binary size: 20-40% smaller
- Runtime performance: 5-15% faster

## Actix-Web Complete Example

**Production-ready Actix-web API:**

```dockerfile
# syntax=docker/dockerfile:1
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

# Runtime stage
FROM scratch

COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/app /app

USER 1000:1000

EXPOSE 8080

ENTRYPOINT ["/app"]
```

**Cargo.toml:**
```toml
[package]
name = "app"
version = "0.1.0"
edition = "2021"

[dependencies]
actix-web = "4.4"
tokio = { version = "1.35", features = ["full"] }

[profile.release]
opt-level = "z"
lto = true
codegen-units = 1
strip = true
panic = "abort"
```

**src/main.rs:**
```rust
use actix_web::{web, App, HttpResponse, HttpServer};

async fn health() -> HttpResponse {
    HttpResponse::Ok().body("OK")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/health", web::get().to(health))
    })
    .bind("0.0.0.0:8080")?
    .run()
    .await
}
```

**Expected size:** 8-12MB

## Rocket Framework Complete Example

```dockerfile
# syntax=docker/dockerfile:1
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
    cargo build --release --target x86_64-unknown-linux-musl

# Runtime stage
FROM gcr.io/distroless/static-debian12

COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/app /app/app

USER nonroot:nonroot

EXPOSE 8000

ENTRYPOINT ["/app/app"]
```

**Cargo.toml:**
```toml
[package]
name = "app"
version = "0.1.0"
edition = "2021"

[dependencies]
rocket = "0.5"

[profile.release]
opt-level = "z"
lto = true
strip = true
```

**Expected size:** 10-15MB

## Private Crate Registry Example

**Using BuildKit secret mount for CARGO_TOKEN:**

```dockerfile
# syntax=docker/dockerfile:1
FROM rust:1.75-alpine AS builder

RUN apk add --no-cache musl-dev

WORKDIR /app

# Configure cargo to use private registry
RUN --mount=type=secret,id=cargo_token \
    mkdir -p ~/.cargo && \
    echo "[registries.private]" > ~/.cargo/config.toml && \
    echo "index = \"https://my-registry.com/git/index\"" >> ~/.cargo/config.toml && \
    echo "[registry]" >> ~/.cargo/config.toml && \
    echo "token = \"$(cat /run/secrets/cargo_token)\"" >> ~/.cargo/config.toml

# Cache dependencies
COPY Cargo.toml Cargo.lock ./
RUN --mount=type=secret,id=cargo_token \
    --mount=type=cache,target=/usr/local/cargo/registry \
    mkdir src && \
    echo "fn main() {}" > src/main.rs && \
    cargo build --release --target x86_64-unknown-linux-musl && \
    rm -rf src

# Build application
COPY src ./src
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release --target x86_64-unknown-linux-musl

FROM scratch
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/app /app
USER 1000:1000
ENTRYPOINT ["/app"]
```

**Build command:**
```bash
echo "my_cargo_token" > cargo_token.txt
docker buildx build --secret id=cargo_token,src=cargo_token.txt -t myapp:latest .
rm cargo_token.txt
```

## Summary

**Rust Dockerfile patterns ranked:**

| Pattern | Size | Security | Debug-ability | Use Case |
|---------|------|----------|---------------|----------|
| Scratch | 5-15MB | Highest | None | Production (smallest) |
| Distroless static | 8-18MB | Highest | None | Production (with CA certs) |
| Alpine | 12-25MB | High | Shell access | Development, debugging |

**Key takeaways:**
- Always use multi-stage builds
- Use musl target for static binaries (`x86_64-unknown-linux-musl`)
- Enable LTO and size optimizations in Cargo.toml
- Strip symbols with `strip` command or `strip = true` in profile
- Use BuildKit cache mounts for cargo registry and target
- Dummy build caches dependencies (10-50x faster rebuilds)
- Use scratch base for smallest images (5-15MB)
- Copy CA certificates if making HTTPS calls
- Configure release profile for size optimization
- Final images: 5-15MB (smallest of any language)

**Cargo.toml release profile (copy-paste):**
```toml
[profile.release]
opt-level = "z"        # Optimize for size
lto = true             # Link-time optimization
codegen-units = 1      # Single codegen unit
strip = true           # Strip symbols
panic = "abort"        # Smaller panic handler
```
