# Base Image Selection Guide

Comprehensive guide to selecting the right base image for your Docker containers.

## Table of Contents

1. [Quick Decision Matrix](#quick-decision-matrix)
2. [Base Image Categories](#base-image-categories)
3. [Language-Specific Recommendations](#language-specific-recommendations)
4. [Distroless Image Variants](#distroless-image-variants)
5. [Alpine vs Debian Slim](#alpine-vs-debian-slim)
6. [Version Pinning Strategies](#version-pinning-strategies)
7. [Multi-Architecture Images](#multi-architecture-images)
8. [Base Image Registries](#base-image-registries)
9. [Security Considerations](#security-considerations)
10. [Summary Table](#summary-table)

## Quick Decision Matrix

| Language | Build Stage | Runtime Stage | Final Size | Use Case |
|----------|-------------|---------------|------------|----------|
| **Go** | `golang:1.22-alpine` | `gcr.io/distroless/static-debian12` | 10-30MB | Production (recommended) |
| **Go** | `golang:1.22-alpine` | `scratch` | 5-20MB | Ultra-minimal |
| **Rust** | `rust:1.75-alpine` | `scratch` | 5-15MB | Production (recommended) |
| **Rust** | `rust:1.75-alpine` | `gcr.io/distroless/static-debian12` | 8-18MB | With CA certs |
| **Python** | `python:3.12-slim` | `python:3.12-slim` | 200-400MB | Production |
| **Python** | `python:3.12-slim` | `gcr.io/distroless/python3-debian12` | 100-200MB | Pure Python only |
| **Node.js** | `node:20-alpine` | `node:20-alpine` | 150-300MB | Production |
| **Node.js** | `node:20-alpine` | `gcr.io/distroless/nodejs20-debian12` | 150-250MB | Security-focused |
| **Java** | `maven:3.9-eclipse-temurin-21` | `eclipse-temurin:21-jre-alpine` | 200-350MB | Production |

## Base Image Categories

### 1. Full Images (Largest)

**Examples:**
- `python:3.12` (1GB)
- `node:20` (1GB)
- `golang:1.22` (800MB)
- `rust:1.75` (1.5GB)

**Contents:**
- Full OS (Debian/Ubuntu)
- Language runtime
- Build tools (gcc, make, etc.)
- Package manager (apt)
- Shell and utilities

**Use for:**
- Development only
- Building complex dependencies
- Debugging

**Never for production.**

### 2. Slim Images (Medium)

**Examples:**
- `python:3.12-slim` (150MB)
- `node:20-slim` (250MB)
- `debian:bookworm-slim` (80MB)

**Contents:**
- Minimal OS (Debian)
- Language runtime
- Package manager (apt)
- Essential libraries
- Shell and basic utilities

**Use for:**
- Production (interpreted languages)
- When dependencies need glibc
- When debugging tools needed

**Recommended for Python and Node.js production.**

### 3. Alpine Images (Small)

**Examples:**
- `python:3.12-alpine` (50MB)
- `node:20-alpine` (180MB)
- `golang:1.22-alpine` (300MB)
- `rust:1.75-alpine` (600MB)
- `alpine:3.19` (7MB)

**Contents:**
- Alpine Linux (musl libc, not glibc)
- Language runtime
- Package manager (apk)
- Busybox utilities
- Shell (ash, not bash)

**Use for:**
- Production (if no glibc dependencies)
- Build stages
- Small image size priority

**Caveats:**
- Uses musl instead of glibc (wheel compatibility issues for Python)
- Some packages require compilation
- DNS resolution differences
- Not recommended for Python with compiled dependencies

### 4. Distroless Images (Minimal)

**Examples:**
- `gcr.io/distroless/static-debian12` (2MB)
- `gcr.io/distroless/base-debian12` (20MB)
- `gcr.io/distroless/python3-debian12` (60MB)
- `gcr.io/distroless/nodejs20-debian12` (150MB)

**Contents:**
- Application + runtime ONLY
- No package manager
- No shell
- No utilities
- Includes: CA certs, timezone data, /etc/passwd

**Use for:**
- Production (maximum security)
- Static binaries (Go, Rust)
- Security-critical applications

**Caveats:**
- Cannot debug with shell
- Cannot install packages at runtime
- Use debug variants for debugging

### 5. Scratch (Empty)

**Example:**
- `scratch` (0 bytes)

**Contents:**
- Literally nothing
- Just the kernel namespace

**Use for:**
- Static binaries only (Go, Rust)
- Absolute minimum size
- Maximum security

**Caveats:**
- No shell (cannot exec)
- No CA certificates (unless copied)
- No /etc/passwd (numeric UIDs only)
- No debugging tools

## Language-Specific Recommendations

### Python

**Production (with compiled dependencies):**
```dockerfile
FROM python:3.12-slim
# 200-400MB, includes glibc for numpy, pandas, etc.
```

**Production (pure Python):**
```dockerfile
FROM gcr.io/distroless/python3-debian12
# 100-200MB, no compiled extensions
```

**Development:**
```dockerfile
FROM python:3.12
# 1GB, all build tools
```

**Avoid:**
```dockerfile
FROM python:3.12-alpine
# Compiles numpy from source (slow, large)
```

### Node.js

**Production:**
```dockerfile
FROM node:20-alpine
# 150-300MB, recommended
```

**Security-focused:**
```dockerfile
FROM gcr.io/distroless/nodejs20-debian12
# 150-250MB, no shell
```

**Development:**
```dockerfile
FROM node:20
# 1GB, all tools
```

### Go

**Production (recommended):**
```dockerfile
FROM gcr.io/distroless/static-debian12
# 10-30MB, static binary
```

**Ultra-minimal:**
```dockerfile
FROM scratch
# 5-20MB, just the binary
```

**With debugging:**
```dockerfile
FROM alpine:3.19
# 15-35MB, includes shell
```

### Rust

**Production (recommended):**
```dockerfile
FROM scratch
# 5-15MB, musl static binary
```

**With CA certs:**
```dockerfile
FROM gcr.io/distroless/static-debian12
# 8-18MB, includes CA certificates
```

**With debugging:**
```dockerfile
FROM alpine:3.19
# 12-25MB, includes shell
```

### Java

**Production:**
```dockerfile
FROM eclipse-temurin:21-jre-alpine
# 200-350MB, JRE only
```

**Development:**
```dockerfile
FROM eclipse-temurin:21-jdk
# 500-700MB, full JDK
```

## Distroless Image Variants

### Static Variant

**Image:** `gcr.io/distroless/static-debian12`
**Size:** ~2MB
**Contents:** Filesystem, CA certs, timezone data
**Use for:** Static binaries (Go, Rust with musl)

**Example:**
```dockerfile
FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/binary /app/binary
USER nonroot:nonroot
ENTRYPOINT ["/app/binary"]
```

### Base Variant

**Image:** `gcr.io/distroless/base-debian12`
**Size:** ~20MB
**Contents:** Static + glibc, libssl, tzdata
**Use for:** Dynamic binaries (Go with CGO, Rust with dynamic linking)

**Example:**
```dockerfile
FROM gcr.io/distroless/base-debian12
COPY --from=builder /app/binary /app/binary
USER nonroot:nonroot
ENTRYPOINT ["/app/binary"]
```

### CC Variant

**Image:** `gcr.io/distroless/cc-debian12`
**Size:** ~25MB
**Contents:** Base + glibc, libgcc, libstdc++
**Use for:** C/C++ applications

### Python3 Variant

**Image:** `gcr.io/distroless/python3-debian12`
**Size:** ~60MB
**Contents:** Python 3 runtime
**Use for:** Pure Python applications (no compiled extensions)

**Limitations:**
- No pip (install in builder stage)
- No compiled extensions (numpy, pandas won't work)

### Java Variants

**Java 17:**
```dockerfile
FROM gcr.io/distroless/java17-debian12
# ~200MB, Java 17 JRE
```

**Java 21:**
```dockerfile
FROM gcr.io/distroless/java21-debian12
# ~200MB, Java 21 JRE
```

### Node.js Variant

**Image:** `gcr.io/distroless/nodejs20-debian12`
**Size:** ~150MB
**Contents:** Node.js 20 runtime

## Alpine vs Debian Slim

**Alpine advantages:**
- Smaller base image (7MB vs 80MB)
- Faster package manager (apk)
- Smaller final images

**Alpine disadvantages:**
- musl libc (not glibc) → wheel compatibility issues
- Compilation required for some packages
- DNS resolution differences
- Less common in production

**Debian Slim advantages:**
- glibc (standard) → better compatibility
- Binary wheels work (Python)
- More predictable behavior

**Debian Slim disadvantages:**
- Larger base image
- Slower package manager (apt)

**Recommendation:**
- **Python:** Use `slim` (not alpine) to avoid compilation
- **Node.js:** Use `alpine` (smaller, no glibc issues)
- **Go/Rust:** Use `alpine` for build stage, `distroless`/`scratch` for runtime

## Version Pinning Strategies

### Pin Exact Version (Recommended)

```dockerfile
FROM python:3.12.1-slim
# Reproducible, predictable
```

### Pin Minor Version

```dockerfile
FROM python:3.12-slim
# Gets patch updates (3.12.0 → 3.12.1)
```

### Pin Major Version (Not Recommended)

```dockerfile
FROM python:3-slim
# Unpredictable (3.11 → 3.12 → 3.13)
```

### Never Use Latest

```dockerfile
FROM python:latest
# ❌ Completely unpredictable
```

## Multi-Architecture Images

**Most official images support multiple architectures:**

```bash
# Build for amd64
docker buildx build --platform linux/amd64 -t myapp:amd64 .

# Build for arm64
docker buildx build --platform linux/arm64 -t myapp:arm64 .

# Build for both (manifest list)
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest --push .
```

**Common platforms:**
- `linux/amd64` (Intel/AMD x86_64)
- `linux/arm64` (ARM 64-bit, M1/M2 Macs, AWS Graviton)
- `linux/arm/v7` (ARM 32-bit, Raspberry Pi)

## Base Image Registries

### Docker Hub (Official Images)

**Registry:** `docker.io` (default)
**Images:** `python:*`, `node:*`, `golang:*`, etc.
**Trust:** High (Docker Official Images)
**Rate limits:** 100 pulls per 6 hours (anonymous), 200 (authenticated)

**Example:**
```dockerfile
FROM python:3.12-slim
# Pulls from docker.io/library/python:3.12-slim
```

### Google Container Registry (Distroless)

**Registry:** `gcr.io`
**Images:** `gcr.io/distroless/*`
**Trust:** High (Google-maintained)
**Rate limits:** None

**Example:**
```dockerfile
FROM gcr.io/distroless/static-debian12
```

### Red Hat (UBI)

**Registry:** `registry.access.redhat.com`
**Images:** `ubi9/*`
**Trust:** High (Red Hat)
**Use for:** Enterprise environments, RHEL ecosystem

**Example:**
```dockerfile
FROM registry.access.redhat.com/ubi9/python-39
```

### GitHub Container Registry

**Registry:** `ghcr.io`
**Images:** Various open-source projects
**Trust:** Varies by maintainer

**Example:**
```dockerfile
FROM ghcr.io/astral-sh/uv:latest
```

## Security Considerations

**Choose base images with:**
- ✅ Official maintainer (Docker, Google, Red Hat)
- ✅ Regular security updates
- ✅ Minimal CVE count
- ✅ Active community
- ✅ Clear provenance

**Avoid:**
- ❌ Unmaintained images
- ❌ Images with HIGH/CRITICAL CVEs
- ❌ Images from unknown publishers
- ❌ Images without version tags

**Scan before use:**
```bash
trivy image python:3.12-slim
docker scout cves python:3.12-slim
```

## Summary Table

| Category | Size | Security | Compatibility | Debug-ability | Use Case |
|----------|------|----------|---------------|---------------|----------|
| Full | 1GB+ | Low | High | High | Development only |
| Slim | 100-300MB | Medium | High | High | Production (Python, Node.js) |
| Alpine | 50-200MB | Medium | Medium | High | Production (Go, Rust build) |
| Distroless | 2-200MB | High | Medium | None | Production (security-focused) |
| Scratch | 0MB | Highest | Low | None | Static binaries only |

**Key recommendations:**
- **Python:** `python:3.12-slim` (production), `gcr.io/distroless/python3-debian12` (pure Python)
- **Node.js:** `node:20-alpine` (production), `gcr.io/distroless/nodejs20-debian12` (security)
- **Go:** `gcr.io/distroless/static-debian12` (production), `scratch` (ultra-minimal)
- **Rust:** `scratch` (production), `gcr.io/distroless/static-debian12` (with CA certs)
- **Java:** `eclipse-temurin:21-jre-alpine` (production)

**Always:**
- Pin exact versions
- Scan for vulnerabilities
- Use multi-stage builds
- Choose smallest viable image
- Prefer official images
