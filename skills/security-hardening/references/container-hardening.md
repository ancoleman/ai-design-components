# Container Hardening Reference

Comprehensive guide to hardening Docker containers and Kubernetes workloads using minimal images, security contexts, and policy enforcement.

## Table of Contents

1. [Container Image Hardening](#container-image-hardening)
2. [Dockerfile Best Practices](#dockerfile-best-practices)
3. [Docker Runtime Security](#docker-runtime-security)
4. [Kubernetes Pod Security](#kubernetes-pod-security)
5. [Pod Security Standards](#pod-security-standards)
6. [Network Policies](#network-policies)
7. [Supply Chain Security](#supply-chain-security)
8. [Runtime Security Monitoring](#runtime-security-monitoring)

---

## Container Image Hardening

### Base Image Selection

Choose minimal base images to reduce attack surface and vulnerabilities:

| Base Image | Size | CVEs | Use Case | Trade-offs |
|------------|------|------|----------|------------|
| **Chainguard Images** | ~10MB | 0 | Production apps | Zero CVEs, minimal packages |
| **Distroless** | ~20MB | Few | Production apps | No shell, harder to debug |
| **Alpine Linux** | ~5MB | Few | General use | Small, auditable, musl libc |
| **Wolfi** | ~15MB | Few | Modern apps | Based on Alpine, glibc |
| **Debian Slim** | ~80MB | More | Compatibility | Has debugging tools |
| **Ubuntu** | ~100MB | Many | Legacy apps | Full compatibility |

**Production recommendation:**
- **First choice:** Chainguard Images (cgr.dev/chainguard/*)
- **Second choice:** Distroless (gcr.io/distroless/*)
- **Development:** Alpine (for easier debugging)

### Multi-Stage Builds

Use multi-stage builds to minimize final image size:

```dockerfile
# Build stage
FROM cgr.dev/chainguard/python:latest-dev AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target=/app/deps

# Production stage
FROM cgr.dev/chainguard/python:latest

# Run as non-root user (nonroot user exists in Chainguard images)
USER nonroot

WORKDIR /app
COPY --from=builder --chown=nonroot:nonroot /app/deps /app/deps
COPY --chown=nonroot:nonroot . .

ENV PYTHONPATH=/app/deps

# Read-only filesystem compatible
ENTRYPOINT ["python", "-m", "app"]
```

### Image Scanning

Scan images for vulnerabilities before deployment:

```bash
# Trivy: Comprehensive scanner
trivy image --severity HIGH,CRITICAL myapp:latest

# Grype: Fast vulnerability scanner
grype myapp:latest

# Scan in CI/CD
docker build -t myapp:test .
trivy image --exit-code 1 --severity CRITICAL myapp:test
```

---

## Dockerfile Best Practices

### Secure Dockerfile Template

```dockerfile
# Use minimal base image
FROM cgr.dev/chainguard/node:latest AS builder

# Set working directory
WORKDIR /app

# Copy only dependency files first (layer caching)
COPY package*.json ./

# Install dependencies (no dev dependencies in production)
RUN npm ci --only=production

# Copy application code
COPY . .

# Production image
FROM cgr.dev/chainguard/node:latest

# Security labels
LABEL org.opencontainers.image.source="https://github.com/org/repo"
LABEL org.opencontainers.image.description="Application description"
LABEL org.opencontainers.image.licenses="MIT"

# Run as non-root user
USER nonroot

WORKDIR /app

# Copy from builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Expose port (documentation only, doesn't actually open port)
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js || exit 1

# Run application
CMD ["node", "server.js"]
```

### Key Dockerfile Hardening Rules

**1. Never run as root:**
```dockerfile
# Bad
FROM ubuntu
RUN apt-get update && apt-get install -y nginx
CMD ["nginx"]

# Good
FROM ubuntu
RUN apt-get update && apt-get install -y nginx \
  && useradd -r -s /bin/false nginx-user
USER nginx-user
CMD ["nginx"]
```

**2. Use COPY instead of ADD:**
```dockerfile
# Bad (ADD has implicit tar extraction)
ADD app.tar.gz /app

# Good (explicit, predictable)
COPY app /app
```

**3. Don't include secrets:**
```dockerfile
# Bad
COPY .env /app/.env
ENV API_KEY=secret123

# Good (use runtime secrets)
# Mount secrets at runtime or use secret management
```

**4. Minimize layers and clean up:**
```dockerfile
# Bad (multiple layers, leftover files)
RUN apt-get update
RUN apt-get install -y curl
RUN curl -O https://example.com/file
RUN rm -rf /var/lib/apt/lists/*

# Good (single layer, cleanup)
RUN apt-get update \
  && apt-get install -y --no-install-recommends curl \
  && curl -O https://example.com/file \
  && apt-get purge -y curl \
  && rm -rf /var/lib/apt/lists/*
```

**5. Use specific versions:**
```dockerfile
# Bad (unpredictable)
FROM node:latest

# Good (pinned version)
FROM node:20.10.0-alpine3.19
```

**6. Set read-only filesystem:**
```dockerfile
# Application must be compatible with read-only filesystem
# No writing to container filesystem
USER nonroot
COPY --chown=nonroot:nonroot app /app

# Use volume mounts for writable directories
VOLUME ["/app/tmp", "/app/logs"]
```

---

## Docker Runtime Security

### Docker Daemon Hardening

Configure Docker daemon in `/etc/docker/daemon.json`:

```json
{
  "icc": false,
  "userns-remap": "default",
  "no-new-privileges": true,
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "live-restore": true,
  "userland-proxy": false,
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 64000,
      "Soft": 64000
    }
  }
}
```

Restart Docker after changes:
```bash
systemctl restart docker
```

### Secure Docker Run Options

Run containers with security flags:

```bash
# Secure container runtime
docker run \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=100m \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --security-opt=no-new-privileges:true \
  --user 1000:1000 \
  --memory=256m \
  --cpus=0.5 \
  --pids-limit=100 \
  --health-cmd="curl -f http://localhost/health || exit 1" \
  --health-interval=30s \
  --health-timeout=3s \
  --health-retries=3 \
  myapp:latest
```

**Docker security options explained:**
- `--read-only`: Root filesystem is read-only
- `--tmpfs`: Mount writable tmpfs for temporary files
- `--cap-drop=ALL`: Drop all Linux capabilities
- `--cap-add`: Add only required capabilities
- `--security-opt=no-new-privileges`: Prevent privilege escalation
- `--user`: Run as non-root user (UID:GID)
- `--memory`, `--cpus`: Resource limits
- `--pids-limit`: Limit number of processes

### Docker Compose Security

```yaml
version: '3.9'

services:
  app:
    image: myapp:latest
    read_only: true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
    user: "1000:1000"
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=100m
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
        reservations:
          cpus: '0.25'
          memory: 128M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 5s
```

---

## Kubernetes Pod Security

### Pod Security Context

Apply security context to pods:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hardened-app
spec:
  # Pod-level security context
  securityContext:
    runAsNonRoot: true
    runAsUser: 65534        # nobody user
    runAsGroup: 65534       # nobody group
    fsGroup: 65534          # filesystem group
    seccompProfile:
      type: RuntimeDefault  # Apply default seccomp profile
    supplementalGroups: [1000]

  containers:
  - name: app
    image: myapp:latest

    # Container-level security context
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 65534
      capabilities:
        drop:
          - ALL                    # Drop all capabilities
        add:
          - NET_BIND_SERVICE       # Only if needed

    # Resource limits
    resources:
      limits:
        memory: "256Mi"
        cpu: "500m"
        ephemeral-storage: "1Gi"
      requests:
        memory: "128Mi"
        cpu: "100m"
        ephemeral-storage: "500Mi"

    # Writable volumes for read-only filesystem
    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: cache
      mountPath: /app/.cache

  volumes:
  - name: tmp
    emptyDir: {}
  - name: cache
    emptyDir: {}
```

### Deployment with Security

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      # Service account (not default)
      serviceAccountName: secure-app-sa
      automountServiceAccountToken: false  # Don't mount unless needed

      # Security context
      securityContext:
        runAsNonRoot: true
        runAsUser: 65534
        fsGroup: 65534
        seccompProfile:
          type: RuntimeDefault

      containers:
      - name: app
        image: myapp:latest
        imagePullPolicy: Always

        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          capabilities:
            drop: ["ALL"]

        resources:
          limits:
            memory: "256Mi"
            cpu: "500m"
          requests:
            memory: "128Mi"
            cpu: "100m"

        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10

        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5

        volumeMounts:
        - name: tmp
          mountPath: /tmp

      volumes:
      - name: tmp
        emptyDir: {}
```

---

## Pod Security Standards

Kubernetes defines three Pod Security Standards:

### 1. Privileged (No restrictions)
For system-level workloads only. **Avoid in production applications.**

### 2. Baseline (Minimally restrictive)
Prevents known privilege escalations:
- Disallows privileged containers
- Restricts host namespaces
- Restricts capabilities
- Limits volume types

### 3. Restricted (Heavily restricted)
Production best practice:
- Everything in Baseline, plus:
- Requires non-root user
- Drops all capabilities
- Restricts volume types further

### Enforce Pod Security Standards

```yaml
# Namespace-level enforcement
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    # Enforce restricted standard
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest

    # Audit mode (log violations)
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/audit-version: latest

    # Warn mode (show warnings)
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: latest
```

### Using Policy Engines

**OPA Gatekeeper:**
```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8spspallowprivilegeescalationcontainer
spec:
  crd:
    spec:
      names:
        kind: K8sPSPAllowPrivilegeEscalationContainer
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8spspallowprivilegeescalationcontainer

        violation[{"msg": msg}] {
          c := input.review.object.spec.containers[_]
          c.securityContext.allowPrivilegeEscalation == true
          msg := sprintf("Privilege escalation container is not allowed: %v", [c.name])
        }
```

**Kyverno:**
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-privilege-escalation
spec:
  validationFailureAction: enforce
  background: true
  rules:
  - name: disallow-privilege-escalation
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Privilege escalation is not allowed"
      pattern:
        spec:
          containers:
          - securityContext:
              allowPrivilegeEscalation: false
```

---

## Network Policies

### Default Deny All Traffic

Start with default deny, then explicitly allow:

```yaml
# Deny all ingress traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress

---
# Deny all egress traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Egress
```

### Allow Specific Traffic

```yaml
# Allow frontend to access API
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow-frontend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
  # Allow DNS
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
```

---

## Supply Chain Security

### Image Signing with Sigstore

Sign container images to verify authenticity:

```bash
# Install cosign
go install github.com/sigstore/cosign/v2/cmd/cosign@latest

# Generate key pair
cosign generate-key-pair

# Sign image
cosign sign --key cosign.key myregistry.io/myapp:v1.0.0

# Verify signature
cosign verify --key cosign.pub myregistry.io/myapp:v1.0.0
```

### Verify Signatures in Kubernetes

```yaml
# Kyverno policy to verify image signatures
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-image-signatures
spec:
  validationFailureAction: enforce
  background: false
  rules:
  - name: verify-signature
    match:
      any:
      - resources:
          kinds:
          - Pod
    verifyImages:
    - imageReferences:
      - "myregistry.io/*"
      attestors:
      - count: 1
        entries:
        - keys:
            publicKeys: |-
              -----BEGIN PUBLIC KEY-----
              ...
              -----END PUBLIC KEY-----
```

### Software Bill of Materials (SBOM)

Generate SBOM for container images:

```bash
# Generate SBOM with syft
syft myapp:latest -o json > sbom.json

# Attach SBOM to image
cosign attach sbom --sbom sbom.json myregistry.io/myapp:v1.0.0

# Verify SBOM
cosign verify-attestation --key cosign.pub \
  --type https://spdx.dev/Document \
  myregistry.io/myapp:v1.0.0
```

---

## Runtime Security Monitoring

### Falco Rules

Deploy Falco for runtime threat detection:

```yaml
# Falco DaemonSet (simplified)
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: falco
  namespace: falco
spec:
  selector:
    matchLabels:
      app: falco
  template:
    metadata:
      labels:
        app: falco
    spec:
      serviceAccountName: falco
      hostNetwork: true
      hostPID: true
      containers:
      - name: falco
        image: falcosecurity/falco:latest
        securityContext:
          privileged: true
        volumeMounts:
        - mountPath: /host/var/run/docker.sock
          name: docker-socket
        - mountPath: /host/dev
          name: dev-fs
        - mountPath: /host/proc
          name: proc-fs
          readOnly: true
      volumes:
      - name: docker-socket
        hostPath:
          path: /var/run/docker.sock
      - name: dev-fs
        hostPath:
          path: /dev
      - name: proc-fs
        hostPath:
          path: /proc
```

**Custom Falco rules:**
```yaml
# /etc/falco/falco_rules.local.yaml
- rule: Unexpected outbound connection
  desc: Detect unexpected outbound network connections
  condition: >
    outbound and
    not container.image.repository in (allowed_images) and
    not fd.sip in (allowed_ips)
  output: >
    Unexpected outbound connection
    (command=%proc.cmdline connection=%fd.name user=%user.name
    container=%container.info)
  priority: WARNING

- list: allowed_images
  items: [myregistry.io/myapp, myregistry.io/sidecar]

- list: allowed_ips
  items: [10.0.0.0/8, 172.16.0.0/12]
```

### Automated Response

Integrate Falco with incident response:

```yaml
# Falcosidekick for alert routing
apiVersion: v1
kind: ConfigMap
metadata:
  name: falcosidekick
  namespace: falco
data:
  config.yaml: |
    slack:
      webhookurl: "https://hooks.slack.com/services/XXX"
      minimumpriority: "warning"
    pagerduty:
      integrationkey: "XXX"
      minimumpriority: "critical"
```

---

## Verification Checklist

Run these checks to verify container hardening:

```bash
#!/bin/bash
# verify-container-hardening.sh

echo "=== Container Hardening Verification ==="

# Check image vulnerabilities
echo -e "\n[Image Scanning]"
trivy image --severity HIGH,CRITICAL myapp:latest

# Check Dockerfile best practices
echo -e "\n[Dockerfile Linting]"
docker run --rm -i hadolint/hadolint < Dockerfile

# Check Kubernetes manifests
echo -e "\n[Kubernetes Security]"
kubesec scan k8s/deployment.yaml

# Check running containers (Docker)
echo -e "\n[Running Container Security]"
docker ps --format "table {{.Names}}\t{{.Image}}" | while read name image; do
  [ "$name" = "NAMES" ] && continue
  echo "Checking $name..."
  docker inspect "$name" --format '{{.HostConfig.Privileged}}' | grep -q false && echo "  ✓ Not privileged" || echo "  ✗ Running privileged"
  docker inspect "$name" --format '{{.HostConfig.ReadonlyRootfs}}' | grep -q true && echo "  ✓ Read-only root" || echo "  ✗ Writable root"
done

echo -e "\n=== Verification Complete ==="
```

---

## Additional Resources

- CIS Docker Benchmark: https://www.cisecurity.org/benchmark/docker
- CIS Kubernetes Benchmark: https://www.cisecurity.org/benchmark/kubernetes
- Kubernetes Pod Security Standards: https://kubernetes.io/docs/concepts/security/pod-security-standards/
- Chainguard Images: https://www.chainguard.dev/chainguard-images
- Distroless Images: https://github.com/GoogleContainerTools/distroless
- Trivy Scanner: https://github.com/aquasecurity/trivy
- Falco Runtime Security: https://falco.org/
- Sigstore: https://www.sigstore.dev/
