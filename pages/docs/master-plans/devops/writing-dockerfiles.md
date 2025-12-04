---
sidebar_position: 6
---

# Writing Dockerfiles

Master plan for creating optimized, secure, and maintainable Docker container images. This skill covers Dockerfile best practices, multi-stage builds, layer optimization, security hardening, and language-specific patterns.

**Status**: 🟢 Master Plan Available

## Key Topics

- **Dockerfile Fundamentals**: Instruction syntax, build context, layer caching, .dockerignore usage
- **Multi-Stage Builds**: Build vs runtime separation, artifact copying, image size reduction
- **Layer Optimization**: Layer ordering, combining commands, cache invalidation strategies
- **Base Image Selection**: Official images, minimal images (Alpine, distroless), security considerations
- **Security Hardening**: Non-root users, minimal attack surface, vulnerability scanning, secrets management
- **Build Arguments**: Parameterization, build-time vs runtime variables, ARG vs ENV
- **Health Checks**: Container health monitoring, readiness vs liveness probes
- **Language-Specific Patterns**: Node.js, Python, Go, Java, Ruby, .NET optimizations

## Primary Tools & Technologies

- **Build Tools**: Docker CLI, BuildKit, Buildah, Kaniko, docker-compose
- **Base Images**: Alpine, Debian Slim, Ubuntu, distroless, scratch, language-specific official images
- **Security Scanning**: Trivy, Snyk, Grype, Docker Scout, Clair
- **Image Registries**: Docker Hub, Amazon ECR, Google GCR, GitHub Container Registry, Azure ACR
- **Build Optimization**: BuildKit features, Docker layer caching, multi-platform builds
- **Linting**: Hadolint, Dockerfile linters

## Integration Points

- **Building CI/CD Pipelines**: Container builds in CI, image publishing
- **Kubernetes Operations**: Container images for K8s deployments
- **GitOps Workflows**: Image promotion through environments
- **Security Operations**: Container vulnerability scanning
- **Platform Engineering**: Standardized base images and patterns
- **Testing Strategies**: Container-based testing with Testcontainers
- **Infrastructure as Code**: Container images as infrastructure artifacts

## Use Cases

- Creating optimized production Docker images
- Building multi-stage Dockerfiles for compiled languages
- Implementing security best practices in containers
- Reducing image size for faster deployments
- Standardizing Dockerfiles across teams
- Building multi-platform images (AMD64, ARM64)
- Creating development vs production image variants
- Implementing Docker layer caching in CI/CD

## Decision Framework

**Base image selection:**
- **Alpine**: Smallest size (~5MB), musl libc compatibility concerns, security updates
- **Debian Slim**: Moderate size (~40MB), glibc compatibility, extensive package availability
- **Ubuntu**: Larger size (~60MB), familiar environment, more packages
- **Distroless**: Minimal runtime, no shell, highest security, debugging challenges
- **Scratch**: Empty image, static binaries only (Go), smallest possible size

**Multi-stage patterns:**
- **Build + Runtime**: Compile in build stage, copy artifacts to minimal runtime stage
- **Test + Runtime**: Run tests in dedicated stage, only promote passing builds
- **Development + Production**: Shared base, different final stages for dev/prod

**Security considerations:**
- Run as non-root user (USER instruction)
- Use specific image tags, not `latest`
- Minimize installed packages
- Copy only necessary files
- Scan for vulnerabilities regularly
- Use secrets management (BuildKit secrets, not baked in)
- Sign and verify images

## Dockerfile Best Practices

**Layer optimization:**
```dockerfile
# ❌ BAD: Separate RUN commands create multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# ✅ GOOD: Combined commands, one layer
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

**Cache-friendly ordering:**
```dockerfile
# ❌ BAD: COPY everything first, cache breaks on any file change
COPY . /app
RUN npm install

# ✅ GOOD: Copy dependency files first, install, then copy code
COPY package*.json /app/
RUN npm ci --only=production
COPY . /app
```

**Multi-stage build pattern:**
```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
CMD ["node", "dist/index.js"]
```

## Language-Specific Patterns

**Node.js:**
- Use `npm ci` instead of `npm install` for reproducible builds
- Copy `package*.json` before code for better caching
- Use `.dockerignore` to exclude `node_modules`
- Consider multi-stage builds to exclude devDependencies

**Python:**
- Use virtual environments or multi-stage builds
- Copy `requirements.txt` first for caching
- Use `pip install --no-cache-dir` to reduce size
- Consider distroless Python images

**Go:**
- Multi-stage with builder and `scratch` or `distroless`
- Use `CGO_ENABLED=0` for static binaries
- Leverage Go module caching
- Extremely small final images (< 10MB)

**Java:**
- Use multi-stage with Maven/Gradle and JRE
- Consider JLink for custom JRE with only needed modules
- Use Eclipse Temurin or Amazon Corretto base images
- Optimize JAR with spring-boot-jarmode-layertools

## Common Anti-Patterns to Avoid

- Using `latest` tag for base images (non-reproducible)
- Running as root user (security risk)
- Installing unnecessary packages (larger attack surface)
- Not using `.dockerignore` (bloated build context)
- Baking secrets into images (security vulnerability)
- Not combining RUN commands (too many layers)
- Ignoring image scanning (vulnerable dependencies)
- Not using multi-stage builds (oversized images)
