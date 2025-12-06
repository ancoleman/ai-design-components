# Security Hardening for Dockerfiles

Comprehensive security patterns for production Docker images.

## Table of Contents

1. [Security Principles](#security-principles)
2. [Non-Root Users](#non-root-users)
3. [Distroless Images](#distroless-images)
4. [Secret Management](#secret-management)
5. [Vulnerability Scanning](#vulnerability-scanning)
6. [Additional Hardening](#additional-hardening)

## Security Principles

**Defense in depth for containers:**

1. **Minimal attack surface** → Distroless/scratch base images
2. **Least privilege** → Non-root users
3. **Secret protection** → BuildKit secret mounts, not ENV vars
4. **Vulnerability management** → Regular scanning and updates
5. **Immutable runtime** → Read-only filesystems where possible
6. **Network segmentation** → Firewall rules, network policies

**The 5-minute security checklist:**
- [ ] Run as non-root user
- [ ] Use minimal base image (distroless/alpine/slim)
- [ ] Pin all versions (base image, dependencies)
- [ ] No secrets in ENV vars or layers
- [ ] Scan with Trivy or Docker Scout
- [ ] Health check included
- [ ] .dockerignore configured

## Non-Root Users

**Why non-root matters:**
- Principle of least privilege
- Limits blast radius if container compromised
- Prevents privilege escalation attacks
- Required by many Kubernetes security policies

### Pattern 1: Debian/Ubuntu Base

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Create non-root user and group
RUN groupadd -r appuser -g 1000 && \
    useradd -r -u 1000 -g appuser -m -d /home/appuser -s /bin/bash appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

CMD ["python", "app.py"]
```

**Key commands:**
- `groupadd -r appuser -g 1000` → Create system group with GID 1000
- `useradd -r -u 1000 -g appuser` → Create system user with UID 1000
- `-m -d /home/appuser` → Create home directory
- `chown -R appuser:appuser /app` → Set ownership

### Pattern 2: Alpine Base

```dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy and install dependencies
COPY package*.json ./
RUN npm ci

# Copy application
COPY . .

# Create non-root user and group
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Key commands:**
- `addgroup -g 1000 appuser` → Create group with GID 1000
- `adduser -D -u 1000 -G appuser appuser` → Create user with UID 1000
  - `-D` → Don't create password
  - `-G appuser` → Add to group
- `chown -R appuser:appuser /app` → Set ownership

### Pattern 3: Distroless Base (Built-in User)

```dockerfile
FROM gcr.io/distroless/static-debian12

COPY --from=builder /app/binary /app/binary

# Use built-in nonroot user (UID 65532)
USER nonroot:nonroot

ENTRYPOINT ["/app/binary"]
```

**Built-in users in distroless:**
- `nonroot:nonroot` → UID 65532, GID 65532
- `nobody:nogroup` → UID 65534, GID 65534

**No user creation needed** - distroless images include these users.

### Pattern 4: Numeric UID (Scratch Base)

```dockerfile
FROM scratch

COPY --from=builder /app/binary /app/binary

# Use numeric UID/GID (no username resolution in scratch)
USER 1000:1000

ENTRYPOINT ["/app/binary"]
```

**Why numeric:** scratch has no `/etc/passwd`, so usernames don't resolve.

### Common Mistakes

**❌ Running as root (default):**
```dockerfile
FROM python:3.12-slim
COPY . /app
CMD ["python", "app.py"]
# Runs as UID 0 (root)
```

**❌ Creating user but not using it:**
```dockerfile
RUN useradd -m appuser
# Missing: USER appuser
CMD ["python", "app.py"]
# Still runs as root!
```

**❌ Wrong ownership:**
```dockerfile
USER appuser
COPY . /app
# Files owned by root, appuser can't write
```

**✅ Correct pattern:**
```dockerfile
COPY . /app
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
CMD ["python", "app.py"]
```

## Distroless Images

**What is distroless?**
- Minimal base images from Google
- Contain ONLY application + runtime dependencies
- No package manager, no shell, no utilities
- 60-80% fewer vulnerabilities than standard base images

**Available distroless images:**

| Image | Size | Contents | Use Case |
|-------|------|----------|----------|
| `gcr.io/distroless/static-debian12` | ~2MB | Just filesystem + CA certs | Static binaries (Go, Rust) |
| `gcr.io/distroless/base-debian12` | ~20MB | glibc, libssl, tzdata | Dynamic binaries |
| `gcr.io/distroless/cc-debian12` | ~25MB | glibc, libgcc, libstdc++ | C/C++ applications |
| `gcr.io/distroless/python3-debian12` | ~60MB | Python 3 runtime | Pure Python apps |
| `gcr.io/distroless/java17-debian12` | ~200MB | Java 17 JRE | Java applications |
| `gcr.io/distroless/nodejs20-debian12` | ~150MB | Node.js 20 runtime | Node.js apps |

### Pattern: Go with Distroless Static

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /app/main .

FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/main /app/main
USER nonroot:nonroot
ENTRYPOINT ["/app/main"]
```

**Image size:** 10-30MB

### Pattern: Python with Distroless

```dockerfile
FROM python:3.12-slim AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM gcr.io/distroless/python3-debian12
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
ENV PATH=/root/.local/bin:$PATH
USER nonroot:nonroot
CMD ["main.py"]
```

**Limitations:**
- Only pure Python (no compiled extensions like numpy)
- No pip at runtime (install in builder stage)

### Pattern: Node.js with Distroless

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
RUN npm prune --omit=dev

FROM gcr.io/distroless/nodejs20-debian12
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
USER nonroot:nonroot
CMD ["dist/index.js"]
```

**Image size:** 150-200MB (vs 200-350MB with alpine)

### Debugging Distroless Images

**Problem:** No shell, can't `docker exec -it`.

**Solution 1:** Use debug variant (includes shell):
```dockerfile
# Development
FROM gcr.io/distroless/static-debian12:debug
```

**Solution 2:** Use ephemeral debug container (Kubernetes 1.23+):
```bash
kubectl debug -it pod/mypod --image=busybox --target=mycontainer
```

**Solution 3:** Use multi-stage with debug stage:
```dockerfile
FROM gcr.io/distroless/static-debian12 AS prod
# ... production config

FROM gcr.io/distroless/static-debian12:debug AS debug
# ... same config with debug shell
```

Build with:
```bash
# Production
docker build --target prod -t myapp:prod .

# Debug
docker build --target debug -t myapp:debug .
```

## Secret Management

**Critical rule:** Secrets MUST NEVER enter image layers.

### Anti-Pattern: Secrets in ENV Vars

**❌ NEVER do this:**
```dockerfile
ENV API_KEY=super_secret_key_12345
# Secret visible in: docker inspect, docker history, image layers
```

**❌ NEVER do this:**
```dockerfile
ARG GITHUB_TOKEN
RUN git clone https://${GITHUB_TOKEN}@github.com/private/repo.git
# Token persists in layer history even after deletion
```

### Pattern 1: BuildKit Secret Mounts (Build-Time)

**Use for:**
- Downloading private dependencies
- Cloning private git repos
- Authenticating to private registries

**Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app

# Install from private PyPI using secret
RUN --mount=type=secret,id=pypi_token \
    pip config set global.index-url https://$(cat /run/secrets/pypi_token)@pypi.example.com/simple && \
    pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]
```

**Build command:**
```bash
echo "my_token" > pypi_token.txt
docker buildx build --secret id=pypi_token,src=pypi_token.txt -t myapp:latest .
rm pypi_token.txt
```

**How it works:**
- Secret mounted at `/run/secrets/{id}` during build
- Secret NOT stored in image layers
- Secret NOT visible in `docker history`

### Pattern 2: Multi-Line Secrets (SSH Keys)

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine

# Clone private repo using SSH key
RUN --mount=type=ssh \
    apk add --no-cache git openssh-client && \
    mkdir -p ~/.ssh && \
    ssh-keyscan github.com >> ~/.ssh/known_hosts && \
    git clone git@github.com:private/repo.git
```

**Build command:**
```bash
docker buildx build --ssh default -t myapp:latest .
# Uses ssh-agent for authentication
```

### Pattern 3: Runtime Secrets (Environment Variables)

**For runtime secrets (API keys, database passwords):**

**Option 1: Docker secrets (Swarm/Compose):**
```yaml
# docker-compose.yml
services:
  app:
    image: myapp:latest
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

**Option 2: Kubernetes secrets:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
  - name: app
    image: myapp:latest
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: password
```

**Option 3: External secret manager:**
- AWS Secrets Manager
- HashiCorp Vault
- Google Secret Manager
- Azure Key Vault

**Application code fetches secrets at runtime**, not hardcoded.

### Pattern 4: .netrc for Private Registries

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
password ghp_your_personal_access_token
```

**Build command:**
```bash
docker buildx build --secret id=netrc,src=.netrc -t myapp:latest .
```

### Secret Verification Checklist

After building, verify no secrets leaked:

```bash
# Check image layers
docker history myapp:latest

# Check environment variables
docker inspect myapp:latest | grep -i env

# Check running container
docker run --rm myapp:latest env
```

**No secrets should appear in any output.**

## Vulnerability Scanning

**Scan every image before production deployment.**

### Tool 1: Trivy (Recommended)

**Install:**
```bash
# macOS
brew install trivy

# Linux
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update && sudo apt-get install trivy
```

**Scan image:**
```bash
# Basic scan
trivy image myapp:latest

# Scan with severity threshold (fail CI if HIGH or CRITICAL)
trivy image --severity HIGH,CRITICAL --exit-code 1 myapp:latest

# Generate SBOM (Software Bill of Materials)
trivy image --format cyclonedx --output sbom.json myapp:latest

# Scan Dockerfile before building
trivy config Dockerfile
```

**Example output:**
```
myapp:latest (debian 12)
========================
Total: 45 (UNKNOWN: 0, LOW: 25, MEDIUM: 15, HIGH: 5, CRITICAL: 0)

┌───────────────┬──────────────┬──────────┬───────────────┬───────────────────┬──────────────────┐
│   Library     │ Vulnerability│ Severity │ Installed Ver │   Fixed Version   │      Title       │
├───────────────┼──────────────┼──────────┼───────────────┼───────────────────┼──────────────────┤
│ libssl1.1     │ CVE-2023-1234│   HIGH   │ 1.1.1n-0      │ 1.1.1n-0+deb12u1  │ OpenSSL vuln     │
└───────────────┴──────────────┴──────────┴───────────────┴───────────────────┴──────────────────┘
```

### Tool 2: Docker Scout

**Scan image:**
```bash
# Basic scan
docker scout cves myapp:latest

# Compare images
docker scout compare myapp:v1 myapp:v2

# Get recommendations
docker scout recommendations myapp:latest

# Quick health check
docker scout quickview myapp:latest
```

**Example output:**
```
Target: myapp:latest (linux/amd64)
Digest: sha256:abc123...

  5C    12H    25M    30L
  ✓ No vulnerabilities in base image
```

### Tool 3: Grype (Anchore)

```bash
# Install
brew tap anchore/grype
brew install grype

# Scan
grype myapp:latest
```

### Scan in CI/CD

**GitHub Actions:**
```yaml
- name: Run Trivy scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'myapp:latest'
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'

- name: Upload results to GitHub Security
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: 'trivy-results.sarif'
```

**GitLab CI:**
```yaml
trivy_scan:
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity CRITICAL,HIGH $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

## Additional Hardening

### Health Checks

**Pattern:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1
```

**Parameters:**
- `--interval=30s` → Check every 30 seconds
- `--timeout=3s` → Timeout after 3 seconds
- `--start-period=10s` → Grace period on startup
- `--retries=3` → Retry 3 times before marking unhealthy

**For distroless (no wget):**
```dockerfile
# Option 1: Copy health check binary
COPY --from=builder /usr/bin/wget /usr/bin/wget
HEALTHCHECK CMD ["/usr/bin/wget", "--spider", "http://localhost:8080/health"]

# Option 2: Use application binary
HEALTHCHECK CMD ["/app/app", "healthcheck"]
```

### Read-Only Filesystem

**Run container with read-only root:**
```bash
docker run --read-only --tmpfs /tmp myapp:latest
```

**Application must write only to /tmp or mounted volumes.**

### Resource Limits

**Prevent DoS attacks:**
```dockerfile
# Not in Dockerfile - set at runtime
```

**Runtime:**
```bash
docker run --memory=512m --cpus=0.5 myapp:latest
```

**Kubernetes:**
```yaml
resources:
  limits:
    memory: "512Mi"
    cpu: "500m"
  requests:
    memory: "256Mi"
    cpu: "250m"
```

### Drop Capabilities

**Default capabilities are often excessive.**

**Runtime:**
```bash
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp:latest
```

**Kubernetes:**
```yaml
securityContext:
  capabilities:
    drop:
      - ALL
    add:
      - NET_BIND_SERVICE
```

### Security Summary Checklist

**Build-time:**
- [ ] Minimal base image (distroless/alpine/slim)
- [ ] Multi-stage build (separate build/runtime)
- [ ] Non-root user configured
- [ ] Pin all versions (base image, dependencies)
- [ ] No secrets in ENV vars or layers
- [ ] Health check included
- [ ] .dockerignore configured
- [ ] Vulnerability scan passed

**Runtime:**
- [ ] Run as non-root user
- [ ] Read-only filesystem (where possible)
- [ ] Resource limits configured
- [ ] Capabilities dropped
- [ ] Network policies configured
- [ ] Secrets from external source (K8s secrets, vault)
- [ ] Regular image rebuilds for security updates

**CI/CD:**
- [ ] Automated vulnerability scanning
- [ ] SBOM generation
- [ ] Fail build on HIGH/CRITICAL CVEs
- [ ] Image signing (Docker Content Trust)
- [ ] Registry scanning enabled
