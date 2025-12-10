# Kubernetes Blueprint

**Version:** 2.0.0
**Last Updated:** 2024-12-06
**Category:** Infrastructure

---

## Overview

Pre-configured skill chain optimized for deploying applications to Kubernetes clusters. This blueprint provides production-ready defaults for containerized applications, including namespace organization, resource management, health checks, service exposure, and observability. Minimizes configuration complexity while maximizing reliability and security.

---

## Trigger Keywords

**Primary (high confidence):**
- kubernetes
- k8s
- deploy to kubernetes
- container orchestration
- helm
- kubectl

**Secondary (medium confidence):**
- pods
- deployments
- services
- ingress
- cluster
- microservices deployment
- containerized application
- cloud native

**Example goals that match:**
- "deploy my app to kubernetes"
- "k8s deployment with autoscaling"
- "deploy microservices to kubernetes cluster"
- "containerize and deploy with helm"
- "kubernetes deployment with ingress"
- "deploy to k8s with monitoring"

---

## Skill Chain (Pre-configured)

This blueprint invokes 6-8 skills in the following order:

```
1. configuring-kubernetes        (core - deployment manifests)
2. managing-containers           (Dockerfile optimization)
3. configuring-nginx             (ingress controller configuration)
4. building-ci-pipelines         (CI/CD for automated deployment)
5. implementing-observability    (monitoring, logging, tracing)
6. hardening-security            (RBAC, network policies, secrets)
7. using-relational-databases            (optional - if stateful workloads)
8. assembling-infrastructure     (final validation - always required)
```

**Total estimated time:** 30-45 minutes
**Total estimated questions:** 15-20 questions (or 3 with blueprint defaults)

---

## Pre-configured Defaults

### 1. configuring-kubernetes
```yaml
deployment_strategy: "rolling-update"
  # RollingUpdate strategy for zero-downtime deployments
  # maxSurge: 1 (one extra pod during update)
  # maxUnavailable: 0 (no downtime during rollout)

namespace: "default"
  # Application namespace (can be customized)
  # Namespace isolation for multi-tenant clusters
  # Resource quotas and network policies per namespace

replicas: 3
  # Three replicas for high availability
  # Survives single node failure
  # Distributes traffic across pods

resource_limits:
  requests:
    cpu: "100m"          # Minimum 0.1 CPU cores
    memory: "128Mi"      # Minimum 128 megabytes RAM
  limits:
    cpu: "500m"          # Maximum 0.5 CPU cores
    memory: "512Mi"      # Maximum 512 megabytes RAM
  # Right-sized for typical web applications
  # Prevents resource starvation and OOMKilled errors
  # Adjust based on application profiling

health_checks:
  liveness_probe:
    http_get:
      path: "/health"
      port: 8080
    initial_delay_seconds: 30
    period_seconds: 10
    timeout_seconds: 5
    failure_threshold: 3
    # Restarts pod if application becomes unresponsive

  readiness_probe:
    http_get:
      path: "/ready"
      port: 8080
    initial_delay_seconds: 10
    period_seconds: 5
    timeout_seconds: 3
    failure_threshold: 3
    # Removes pod from service endpoints if not ready

service_type: "ClusterIP"
  # Internal cluster networking by default
  # Use with Ingress for external access
  # Options: ClusterIP, NodePort, LoadBalancer

labels:
  app: "{{ APP_NAME }}"
  version: "{{ VERSION }}"
  environment: "production"
  managed-by: "kubernetes"
  # Standard labels for resource organization
  # Used by selectors, network policies, monitoring
```

### 2. managing-containers
```yaml
base_image: "node:20-alpine"
  # Alpine Linux for minimal image size
  # Official Node.js 20 LTS
  # 50MB vs 900MB for standard Node image
  # Security: fewer packages = smaller attack surface

multi_stage_build: true
  # Stage 1: Build dependencies
  # Stage 2: Production runtime (no dev dependencies)
  # Reduces final image size by 60-80%

security:
  non_root_user: true
    # Run as non-root user (uid: 1000)
    # Prevents privilege escalation attacks

  read_only_filesystem: true
    # Immutable container filesystem
    # Write to tmpfs volumes only
    # Prevents malware persistence

layer_optimization: true
  # Order dependencies by change frequency
  # Cache package.json/package-lock.json layers
  # Fast rebuilds when only code changes

image_scanning: true
  # Scan for vulnerabilities with Trivy/Grype
  # Fail build on critical CVEs
  # Integrated with CI pipeline
```

### 3. configuring-nginx
```yaml
ingress_controller: "nginx"
  # NGINX Ingress Controller (most common)
  # Alternatives: Traefik, HAProxy, Istio

ssl_termination: true
  # TLS termination at ingress
  # Automatic cert provisioning with cert-manager
  # HTTP to HTTPS redirect

rate_limiting:
  enabled: true
  requests_per_minute: 100
  burst: 20
  # Protection against DDoS and abuse
  # Per-client IP rate limiting

annotations:
  nginx.ingress.kubernetes.io/rewrite-target: "/"
  nginx.ingress.kubernetes.io/ssl-redirect: "true"
  nginx.ingress.kubernetes.io/rate-limit: "100"
  cert-manager.io/cluster-issuer: "letsencrypt-prod"
  # Automatic HTTPS with Let's Encrypt
  # Production-grade SSL certificates

routing_rules:
  - host: "app.example.com"
    paths:
      - path: "/"
        service: "{{ APP_NAME }}"
        port: 8080
      - path: "/api"
        service: "{{ APP_NAME }}-api"
        port: 3000
  # Path-based and host-based routing
  # Multiple services behind single ingress
```

### 4. building-ci-pipelines
```yaml
ci_platform: "github-actions"
  # GitHub Actions for CI/CD
  # Alternatives: GitLab CI, Jenkins, CircleCI

pipeline_stages:
  - lint-test
  - build-image
  - scan-security
  - deploy-staging
  - deploy-production (manual approval)
  # Multi-stage pipeline with gates
  # Automated staging, manual production

docker_registry: "ghcr.io"
  # GitHub Container Registry
  # Alternatives: Docker Hub, ECR, GCR, ACR

image_tagging:
  - "latest"
  - "{{ GIT_SHA }}"
  - "{{ VERSION }}"
  # Semantic versioning + git commit SHA
  # Immutable tags for rollback capability

deployment_automation:
  strategy: "gitops"
  tool: "argocd"
  # GitOps workflow with ArgoCD
  # Git as single source of truth
  # Automatic sync and rollback
```

### 5. implementing-observability
```yaml
metrics:
  enabled: true
  exporter: "prometheus"
  port: 9090
  path: "/metrics"
  # Prometheus metrics scraping
  # Application and container metrics
  # ServiceMonitor CRD for auto-discovery

logging:
  enabled: true
  aggregator: "fluentd"
  destination: "elasticsearch"
  format: "json"
  # Structured JSON logging
  # Centralized log aggregation
  # Integration with EFK stack (Elasticsearch, Fluentd, Kibana)

tracing:
  enabled: false
  # Distributed tracing (optional)
  # Enable for microservices architectures
  # Jaeger or Zipkin integration

dashboards:
  grafana_enabled: true
  default_dashboards:
    - "kubernetes-cluster-monitoring"
    - "pod-resource-usage"
    - "application-metrics"
  # Pre-built Grafana dashboards
  # Real-time cluster and app monitoring

alerts:
  enabled: true
  rules:
    - name: "HighPodCPU"
      threshold: "80%"
      severity: "warning"
    - name: "PodCrashLooping"
      threshold: "3 restarts in 5m"
      severity: "critical"
    - name: "HighMemoryUsage"
      threshold: "90%"
      severity: "critical"
  # Alertmanager integration
  # Slack/PagerDuty/Email notifications
```

### 6. hardening-security
```yaml
rbac:
  enabled: true
  service_account: "{{ APP_NAME }}-sa"
  role_type: "least-privilege"
  # Role-Based Access Control
  # Dedicated service account per application
  # Minimal permissions (principle of least privilege)

network_policies:
  enabled: true
  default_deny: true
  allowed_ingress:
    - from: "ingress-controller"
    - from: "same-namespace"
  allowed_egress:
    - to: "kube-dns"
    - to: "external-apis"
  # Zero-trust networking
  # Deny all traffic by default
  # Explicitly allow required connections

secrets_management:
  method: "sealed-secrets"
  # Bitnami Sealed Secrets for GitOps
  # Encrypted secrets in version control
  # Alternatives: External Secrets Operator, Vault

pod_security:
  policy: "restricted"
  standards:
    - no-privileged-containers
    - drop-all-capabilities
    - read-only-root-filesystem
    - run-as-non-root
    - seccomp-profile-runtime-default
  # Pod Security Standards (PSS) enforcement
  # Kubernetes native security policies

image_pull_policy: "Always"
  # Always pull latest tag
  # Ensures vulnerability patches applied
  # Private registry authentication configured
```

### 7. using-relational-databases (optional)
```yaml
database_type: "postgresql"
  # Managed database recommended (RDS, Cloud SQL)
  # In-cluster StatefulSet for development/testing only

persistence:
  enabled: true
  storage_class: "fast-ssd"
  size: "20Gi"
  access_mode: "ReadWriteOnce"
  # Persistent volumes for stateful workloads
  # SSD storage for database performance

backup:
  enabled: true
  schedule: "0 2 * * *"  # Daily at 2 AM
  retention: "7 days"
  # Automated backups with CronJob
  # Point-in-time recovery capability

connection_pooling:
  enabled: true
  max_connections: 100
  # PgBouncer or similar for connection pooling
  # Reduces database connection overhead
```

### 8. assembling-infrastructure
```yaml
validation_checks:
  - manifest_syntax
  - resource_limits_defined
  - health_checks_configured
  - security_context_set
  - labels_consistent
  # Pre-deployment validation
  # Catches common configuration errors

kustomize_enabled: true
  # Kustomize for environment-specific configs
  # Base manifests + overlays (dev, staging, prod)
  # No template engine required

helm_chart: false
  # Option to package as Helm chart
  # Enables parameterized deployments
  # Helm repository publishing

documentation:
  readme: true
  architecture_diagram: true
  runbook: true
  # Deployment documentation
  # Architecture overview
  # Operational runbook for common tasks
```

---

## Quick Questions (Only 3)

When blueprint is detected, ask only these essential questions:

### Question 1: Application Type
```
What type of application are you deploying?

Options:
1. Stateless web application (API, frontend, microservice)
2. Stateful service (database, message queue, cache)
3. Background worker/job processor
4. Batch/CronJob workload

Your answer: _______________
```

**Why this matters:**
- Determines Deployment vs StatefulSet vs Job
- Affects persistence requirements
- Influences resource allocation
- Impacts scaling strategy

**Default if skipped:** "Stateless web application"

---

### Question 2: Scaling Requirements
```
How should your application scale?

Options:
1. Fixed replicas (e.g., always 3 pods) - simple, predictable
2. Horizontal Pod Autoscaling (HPA) - scale based on CPU/memory
3. Advanced autoscaling with custom metrics (e.g., queue length)
4. Spot/preemptible instances for cost savings

Your answer: _______________
```

**Why this matters:**
- Configures HPA resources
- Sets resource requests/limits
- Determines pod disruption budgets
- Affects cost optimization strategies

**Default if skipped:** "Fixed replicas (3 pods)"

---

### Question 3: Exposure Type
```
How should your application be accessed?

Options:
1. Internal only (ClusterIP service) - no external access
2. External via Ingress (domain name, HTTPS) - recommended for web apps
3. External via LoadBalancer (direct cloud LB) - for non-HTTP services
4. NodePort (for development/testing only)

Your answer: _______________
```

**Why this matters:**
- Determines Service type
- Configures Ingress resources
- Sets up SSL/TLS certificates
- Affects networking costs

**Default if skipped:** "External via Ingress with HTTPS"

---

## Blueprint Detection Logic

Trigger this blueprint when the user's goal matches:

```python
def should_use_k8s_blueprint(goal: str) -> bool:
    goal_lower = goal.lower()

    # Primary keywords (high confidence)
    primary_match = any(keyword in goal_lower for keyword in [
        "kubernetes",
        "k8s",
        "deploy to kubernetes",
        "helm",
        "container orchestration"
    ])

    # Secondary keywords + deployment context
    secondary_match = (
        any(keyword in goal_lower for keyword in ["deploy", "deployment", "containerize"]) and
        any(keyword in goal_lower for keyword in ["cluster", "pods", "microservices", "cloud native"])
    )

    # Cloud provider specific
    cloud_k8s_match = any(keyword in goal_lower for keyword in [
        "eks", "gke", "aks",  # AWS EKS, Google GKE, Azure AKS
        "deploy to aws kubernetes",
        "deploy to google kubernetes"
    ])

    return primary_match or secondary_match or cloud_k8s_match
```

**Confidence levels:**
- **High (90%+):** Contains "kubernetes" or "k8s" + deployment intent
- **Medium (70-89%):** Contains "deploy" + "cluster" or "microservices"
- **Low (50-69%):** Contains "containerize" + cloud provider name

**Present blueprint when confidence >= 70%**

---

## Blueprint Offer Message

When blueprint is detected, present this message to the user:

```
┌────────────────────────────────────────────────────────────┐
│ ☸️  KUBERNETES BLUEPRINT DETECTED                          │
├────────────────────────────────────────────────────────────┤
│ Your goal matches our optimized Kubernetes Blueprint!     │
│                                                            │
│ Pre-configured features:                                   │
│  ✓ Production-ready deployment manifests                  │
│  ✓ 3-replica high availability setup                      │
│  ✓ Health checks (liveness + readiness)                   │
│  ✓ Resource limits and requests                           │
│  ✓ Ingress with automatic HTTPS (Let's Encrypt)           │
│  ✓ Security hardening (RBAC, network policies)            │
│  ✓ Prometheus monitoring + Grafana dashboards             │
│  ✓ Multi-stage Dockerfile (optimized for size)            │
│  ✓ CI/CD pipeline (GitHub Actions + ArgoCD)               │
│                                                            │
│ Using blueprint reduces questions from 18 to 3!           │
│                                                            │
│ Options:                                                   │
│  1. Use blueprint (3 quick questions, ~15 min)            │
│  2. Custom configuration (18 questions, ~45 min)          │
│  3. Skip all questions (use all defaults, ~8 min)         │
│                                                            │
│ Your choice (1/2/3): _____                                │
└────────────────────────────────────────────────────────────┘
```

**Handle responses:**
- **1 or "blueprint"** → Ask only 3 blueprint questions
- **2 or "custom"** → Ask all skill questions (normal flow)
- **3 or "skip"** → Use all defaults, skip all questions

---

## Generated Output Structure

When blueprint is executed, generate this file structure:

```
k8s-deployment/
├── kubernetes/
│   ├── base/                           # Kustomize base manifests
│   │   ├── deployment.yaml             # Deployment resource
│   │   ├── service.yaml                # Service resource
│   │   ├── ingress.yaml                # Ingress resource
│   │   ├── configmap.yaml              # Configuration data
│   │   ├── secret.yaml                 # Sealed secret (encrypted)
│   │   ├── serviceaccount.yaml         # RBAC service account
│   │   ├── role.yaml                   # RBAC role
│   │   ├── rolebinding.yaml            # RBAC role binding
│   │   ├── hpa.yaml                    # Horizontal Pod Autoscaler (if enabled)
│   │   ├── pdb.yaml                    # Pod Disruption Budget
│   │   ├── networkpolicy.yaml          # Network policy rules
│   │   └── kustomization.yaml          # Kustomize base config
│   │
│   ├── overlays/                       # Environment-specific configs
│   │   ├── development/
│   │   │   ├── kustomization.yaml      # Dev overrides
│   │   │   ├── namespace.yaml          # dev namespace
│   │   │   └── patches.yaml            # Dev-specific patches
│   │   │
│   │   ├── staging/
│   │   │   ├── kustomization.yaml      # Staging overrides
│   │   │   ├── namespace.yaml          # staging namespace
│   │   │   └── patches.yaml            # Staging-specific patches
│   │   │
│   │   └── production/
│   │       ├── kustomization.yaml      # Prod overrides
│   │       ├── namespace.yaml          # production namespace
│   │       ├── patches.yaml            # Prod-specific patches
│   │       └── certificate.yaml        # TLS certificate
│   │
│   ├── monitoring/
│   │   ├── servicemonitor.yaml         # Prometheus ServiceMonitor
│   │   ├── prometheusrule.yaml         # Alert rules
│   │   ├── grafana-dashboard.json      # Grafana dashboard definition
│   │   └── kustomization.yaml          # Monitoring resources
│   │
│   └── helm/                           # Optional Helm chart
│       ├── Chart.yaml                  # Helm chart metadata
│       ├── values.yaml                 # Default values
│       ├── values-dev.yaml             # Dev environment values
│       ├── values-prod.yaml            # Prod environment values
│       └── templates/                  # Helm templates
│           └── (generated from base manifests)
│
├── docker/
│   ├── Dockerfile                      # Multi-stage production build
│   ├── Dockerfile.dev                  # Development build (hot reload)
│   ├── .dockerignore                   # Build context exclusions
│   └── entrypoint.sh                   # Container entrypoint script
│
├── .github/
│   └── workflows/
│       ├── ci.yaml                     # CI pipeline (lint, test, build)
│       ├── cd-staging.yaml             # Deploy to staging (auto)
│       ├── cd-production.yaml          # Deploy to production (manual)
│       └── security-scan.yaml          # Container image scanning
│
├── scripts/
│   ├── deploy.sh                       # Manual deployment script
│   ├── rollback.sh                     # Rollback to previous version
│   ├── port-forward.sh                 # Local port forwarding
│   ├── logs.sh                         # Tail pod logs
│   ├── shell.sh                        # Exec into pod
│   └── validate-manifests.sh           # Pre-commit manifest validation
│
├── docs/
│   ├── README.md                       # Deployment guide
│   ├── ARCHITECTURE.md                 # System architecture
│   ├── RUNBOOK.md                      # Operational runbook
│   └── TROUBLESHOOTING.md              # Common issues and solutions
│
├── Makefile                            # Common commands (make deploy, make rollback)
├── kustomization.yaml                  # Root kustomization
└── .env.example                        # Environment variables template
```

---

## Manifest Examples

### Example Deployment (base/deployment.yaml)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
    version: v1.0.0
    managed-by: kustomize
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1.0.0
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: myapp-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: myapp
        image: ghcr.io/myorg/myapp:latest
        imagePullPolicy: Always
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        - name: metrics
          containerPort: 9090
          protocol: TCP
        env:
        - name: NODE_ENV
          value: "production"
        - name: PORT
          value: "8080"
        envFrom:
        - configMapRef:
            name: myapp-config
        - secretRef:
            name: myapp-secrets
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          capabilities:
            drop:
            - ALL
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

### Example Service (base/service.yaml)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - name: http
    port: 80
    targetPort: http
    protocol: TCP
  - name: metrics
    port: 9090
    targetPort: metrics
    protocol: TCP
  sessionAffinity: None
```

### Example Ingress (base/ingress.yaml)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp
            port:
              name: http
```

### Example HPA (base/hpa.yaml)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 15
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```

### Example NetworkPolicy (base/networkpolicy.yaml)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: myapp
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    - podSelector:
        matchLabels:
          app: myapp
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443
```

---

## Dockerfile Example

Multi-stage build for Node.js application:

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (including devDependencies)
RUN npm ci

# Copy source code
COPY . .

# Build application (TypeScript, etc.)
RUN npm run build

# Stage 2: Production
FROM node:20-alpine

# Install dumb-init for signal handling
RUN apk add --no-cache dumb-init

# Create app user
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install only production dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Copy built application from builder
COPY --from=builder --chown=appuser:appuser /app/dist ./dist

# Create writable directories
RUN mkdir -p /tmp /app/.cache && \
    chown -R appuser:appuser /tmp /app/.cache

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD node -e "require('http').get('http://localhost:8080/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Start application
CMD ["node", "dist/server.js"]
```

---

## CI/CD Pipeline Example

GitHub Actions workflow for CI/CD:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'

    - run: npm ci
    - run: npm run lint
    - run: npm test
    - run: npm run build

  build-push:
    needs: lint-test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
    - uses: actions/checkout@v4

    - name: Log in to registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha,prefix={{branch}}-

    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  security-scan:
    needs: build-push
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Run Trivy scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        format: 'sarif'
        output: 'trivy-results.sarif'
        severity: 'CRITICAL,HIGH'

    - name: Upload scan results
      uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: 'trivy-results.sarif'

  deploy-staging:
    needs: security-scan
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging
    steps:
    - uses: actions/checkout@v4

    - name: Deploy to staging
      run: |
        kubectl config use-context staging
        kubectl apply -k kubernetes/overlays/staging
        kubectl rollout status deployment/myapp -n staging

  deploy-production:
    needs: security-scan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
    - uses: actions/checkout@v4

    - name: Deploy to production
      run: |
        kubectl config use-context production
        kubectl apply -k kubernetes/overlays/production
        kubectl rollout status deployment/myapp -n production
```

---

## Monitoring Configuration

### ServiceMonitor (monitoring/servicemonitor.yaml)

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

### PrometheusRule (monitoring/prometheusrule.yaml)

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: myapp
spec:
  groups:
  - name: myapp.rules
    interval: 30s
    rules:
    - alert: HighPodCPU
      expr: rate(container_cpu_usage_seconds_total{pod=~"myapp.*"}[5m]) > 0.8
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High CPU usage on {{ $labels.pod }}"
        description: "Pod {{ $labels.pod }} CPU usage is above 80%"

    - alert: PodCrashLooping
      expr: rate(kube_pod_container_status_restarts_total{pod=~"myapp.*"}[15m]) > 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Pod {{ $labels.pod }} is crash looping"
        description: "Pod has restarted {{ $value }} times in the last 15 minutes"

    - alert: HighMemoryUsage
      expr: container_memory_usage_bytes{pod=~"myapp.*"} / container_spec_memory_limit_bytes{pod=~"myapp.*"} > 0.9
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "High memory usage on {{ $labels.pod }}"
        description: "Pod {{ $labels.pod }} memory usage is above 90%"
```

---

## Operational Commands

### Deploy Commands (Makefile)

```makefile
.PHONY: deploy deploy-dev deploy-staging deploy-prod

# Development
deploy-dev:
	kubectl apply -k kubernetes/overlays/development
	kubectl rollout status deployment/myapp -n dev

# Staging
deploy-staging:
	kubectl apply -k kubernetes/overlays/staging
	kubectl rollout status deployment/myapp -n staging

# Production
deploy-prod:
	kubectl apply -k kubernetes/overlays/production
	kubectl rollout status deployment/myapp -n production

# Rollback
rollback:
	kubectl rollout undo deployment/myapp -n $(ENV)

# Logs
logs:
	kubectl logs -f -l app=myapp -n $(ENV) --tail=100

# Shell
shell:
	kubectl exec -it deployment/myapp -n $(ENV) -- /bin/sh

# Port forward
port-forward:
	kubectl port-forward -n $(ENV) svc/myapp 8080:80
```

---

## Accessibility Features (Developer Experience)

All manifests include:

- **Clear naming conventions:** app, component, version labels
- **Comprehensive comments:** Explain non-obvious configurations
- **Validation scripts:** Pre-commit hooks for manifest validation
- **Helpful error messages:** Readiness probe failures logged
- **Documentation:** README, runbook, troubleshooting guide
- **Local development:** Skaffold/Tilt support for hot reload

---

## Cost Optimization

- **Right-sized resources:** CPU/memory requests match actual usage
- **Horizontal autoscaling:** Scale down during low traffic
- **Spot instances:** Use for non-critical workloads
- **Resource quotas:** Prevent runaway costs
- **Image optimization:** Multi-stage builds reduce registry costs
- **Monitoring:** Track resource waste and optimize

---

## Security Best Practices

- **Non-root containers:** All containers run as UID 1000
- **Read-only filesystem:** Immutable containers
- **Network policies:** Zero-trust networking
- **RBAC:** Least-privilege service accounts
- **Image scanning:** Block vulnerable images
- **Secret encryption:** Sealed secrets or external secret managers
- **Pod security standards:** Enforce restricted policy

---

## Version History

**2.0.0** (2024-12-06)
- Initial Kubernetes blueprint
- 6-8 skill chain with production-ready defaults
- 3-question quick configuration
- Multi-stage Dockerfile optimization
- GitOps workflow with ArgoCD
- Comprehensive monitoring and security

---

## Related Blueprints

- **Microservices Blueprint:** For multi-service deployments
- **Database Blueprint:** For stateful workloads
- **API Blueprint:** For API gateway + backend services
- **Monitoring Blueprint:** For observability stack

---

## Deliverables Specification

This section defines concrete validation checks for blueprint promises, ensuring skills produce what users expect.

### Deliverables

```yaml
deliverables:
  "Kubernetes Deployment manifests":
    primary_skill: operating-kubernetes
    required_files:
      - kubernetes/deployment.yaml
      - kubernetes/service.yaml
    content_checks:
      - pattern: "kind: Deployment"
        in: kubernetes/deployment.yaml
      - pattern: "resources:\\s*(requests|limits):"
        in: kubernetes/deployment.yaml
      - pattern: "kind: Service"
        in: kubernetes/service.yaml
    maturity_required: [starter, intermediate, advanced]

  "Health checks configuration":
    primary_skill: operating-kubernetes
    required_files:
      - kubernetes/deployment.yaml
    content_checks:
      - pattern: "livenessProbe:"
        in: kubernetes/deployment.yaml
      - pattern: "readinessProbe:"
        in: kubernetes/deployment.yaml
    maturity_required: [starter, intermediate, advanced]

  "Namespace and ConfigMap":
    primary_skill: operating-kubernetes
    required_files:
      - kubernetes/namespace.yaml
      - kubernetes/configmap.yaml
    content_checks:
      - pattern: "kind: Namespace"
        in: kubernetes/namespace.yaml
      - pattern: "kind: ConfigMap"
        in: kubernetes/configmap.yaml
    maturity_required: [starter, intermediate, advanced]

  "Horizontal Pod Autoscaler":
    primary_skill: operating-kubernetes
    required_files:
      - kubernetes/hpa.yaml
    content_checks:
      - pattern: "kind: HorizontalPodAutoscaler"
        in: kubernetes/hpa.yaml
      - pattern: "minReplicas:|maxReplicas:"
        in: kubernetes/hpa.yaml
      - pattern: "metrics:"
        in: kubernetes/hpa.yaml
    maturity_required: [intermediate, advanced]

  "Network policies":
    primary_skill: operating-kubernetes
    required_files:
      - kubernetes/networkpolicy.yaml
    content_checks:
      - pattern: "kind: NetworkPolicy"
        in: kubernetes/networkpolicy.yaml
      - pattern: "podSelector:"
        in: kubernetes/networkpolicy.yaml
      - pattern: "policyTypes:"
        in: kubernetes/networkpolicy.yaml
    maturity_required: [intermediate, advanced]

  "RBAC configuration":
    primary_skill: operating-kubernetes
    required_files:
      - kubernetes/rbac.yaml
    content_checks:
      - pattern: "kind: Role|kind: RoleBinding"
        in: kubernetes/rbac.yaml
      - pattern: "rules:"
        in: kubernetes/rbac.yaml
    maturity_required: [intermediate, advanced]

  "Pod Disruption Budget":
    primary_skill: operating-kubernetes
    required_files:
      - kubernetes/pdb.yaml
    content_checks:
      - pattern: "kind: PodDisruptionBudget"
        in: kubernetes/pdb.yaml
      - pattern: "minAvailable"
        in: kubernetes/pdb.yaml
    maturity_required: [intermediate, advanced]

  "Kustomize overlays":
    primary_skill: operating-kubernetes
    required_files:
      - kubernetes/kustomization.yaml
      - kubernetes/overlays/production/kustomization.yaml
      - kubernetes/overlays/staging/kustomization.yaml
    content_checks:
      - pattern: "resources:|apiVersion: kustomize"
        in: kubernetes/kustomization.yaml
    maturity_required: [advanced]

  "ServiceMonitor for Prometheus":
    primary_skill: operating-kubernetes
    required_files:
      - kubernetes/servicemonitor.yaml
    content_checks:
      - pattern: "kind: ServiceMonitor"
        in: kubernetes/servicemonitor.yaml
      - pattern: "endpoints:"
        in: kubernetes/servicemonitor.yaml
    maturity_required: [advanced]

  "Multi-stage Dockerfile":
    primary_skill: writing-dockerfiles
    required_files:
      - Dockerfile
      - .dockerignore
    content_checks:
      - pattern: "FROM.*AS builder"
        in: Dockerfile
      - pattern: "COPY --from=builder"
        in: Dockerfile
      - pattern: "USER"
        in: Dockerfile
      - pattern: "\\.git|node_modules|__pycache__"
        in: .dockerignore
    maturity_required: [intermediate, advanced]

  "Docker Compose for development":
    primary_skill: writing-dockerfiles
    required_files:
      - docker-compose.yml
    content_checks:
      - pattern: "services:|build:|ports:"
        in: docker-compose.yml
    maturity_required: [intermediate, advanced]

  "Ingress configuration":
    primary_skill: configuring-nginx
    required_files:
      - kubernetes/ingress.yaml
    content_checks:
      - pattern: "kind: Ingress"
        in: kubernetes/ingress.yaml
      - pattern: "cert-manager\\.io/cluster-issuer|tls:"
        in: kubernetes/ingress.yaml
    maturity_required: [starter, intermediate, advanced]

  "Nginx security headers":
    primary_skill: configuring-nginx
    required_files:
      - kubernetes/ingress.yaml
    content_checks:
      - pattern: "nginx\\.ingress\\.kubernetes\\.io/(ssl-redirect|rate-limit)"
        in: kubernetes/ingress.yaml
    maturity_required: [intermediate, advanced]

  "CI/CD pipeline":
    primary_skill: building-ci-pipelines
    required_files:
      - .github/workflows/ci.yml
      - .github/workflows/cd-staging.yml
      - .github/workflows/cd-production.yml
    content_checks:
      - pattern: "on:|jobs:|steps:"
        in: .github/workflows/ci.yml
      - pattern: "kubectl apply|deploy"
        in: .github/workflows/cd-staging.yml
    maturity_required: [intermediate, advanced]

  "Docker build and push workflow":
    primary_skill: building-ci-pipelines
    required_files:
      - .github/workflows/ci.yml
    content_checks:
      - pattern: "docker/build-push-action|docker/login-action"
        in: .github/workflows/ci.yml
    maturity_required: [intermediate, advanced]

  "Security scanning workflow":
    primary_skill: building-ci-pipelines
    required_files:
      - .github/workflows/security-scan.yaml
    content_checks:
      - pattern: "trivy-action|aquasecurity"
        in: .github/workflows/security-scan.yaml
      - pattern: "severity: 'CRITICAL,HIGH'"
        in: .github/workflows/security-scan.yaml
    maturity_required: [advanced]

  "Prometheus configuration":
    primary_skill: implementing-observability
    required_files:
      - monitoring/prometheus/prometheus.yml
      - monitoring/prometheus/alert_rules.yml
    content_checks:
      - pattern: "scrape_configs:|job_name:"
        in: monitoring/prometheus/prometheus.yml
      - pattern: "alert:|expr:"
        in: monitoring/prometheus/alert_rules.yml
    maturity_required: [intermediate, advanced]

  "Grafana dashboards":
    primary_skill: implementing-observability
    required_files:
      - monitoring/grafana/dashboards/kubernetes-overview.json
    content_checks:
      - pattern: '"type":\\s*"(graph|gauge|stat)"'
        in: monitoring/grafana/dashboards/
      - pattern: '"title".*Kubernetes|"title".*Pod'
        in: monitoring/grafana/dashboards/
    maturity_required: [intermediate, advanced]

  "Istio service mesh (if enabled)":
    primary_skill: implementing-service-mesh
    required_files:
      - mesh/istio/virtualservice.yaml
      - mesh/istio/destinationrule.yaml
      - mesh/istio/peer-authentication.yaml
    content_checks:
      - pattern: "kind: VirtualService"
        in: mesh/istio/virtualservice.yaml
      - pattern: "kind: DestinationRule"
        in: mesh/istio/destinationrule.yaml
      - pattern: "kind: PeerAuthentication"
        in: mesh/istio/peer-authentication.yaml
      - pattern: "STRICT"
        in: mesh/istio/peer-authentication.yaml
    maturity_required: [advanced]

  "StatefulSet for database (if stateful)":
    primary_skill: using-relational-databases
    required_files:
      - kubernetes/statefulset.yaml
      - kubernetes/storageclass.yaml
    content_checks:
      - pattern: "kind: StatefulSet"
        in: kubernetes/statefulset.yaml
      - pattern: "volumeClaimTemplates:"
        in: kubernetes/statefulset.yaml
      - pattern: "kind: StorageClass"
        in: kubernetes/storageclass.yaml
    maturity_required: [intermediate, advanced]

  "Deployment scripts":
    primary_skill: operating-kubernetes
    required_files:
      - scripts/deploy.sh
      - scripts/rollback.sh
    content_checks:
      - pattern: "kubectl apply"
        in: scripts/deploy.sh
      - pattern: "kubectl rollout"
        in: scripts/rollback.sh
    maturity_required: [starter, intermediate, advanced]

  "Makefile with common operations":
    primary_skill: assembling-components
    required_files:
      - Makefile
    content_checks:
      - pattern: "\\.PHONY:|deploy|rollback"
        in: Makefile
      - pattern: "kubectl"
        in: Makefile
    maturity_required: [intermediate, advanced]

  "Documentation":
    primary_skill: assembling-components
    required_files:
      - docs/README.md
      - docs/ARCHITECTURE.md
      - docs/RUNBOOK.md
    content_checks:
      - pattern: "Deployment|Kubernetes|Setup"
        in: docs/README.md
      - pattern: "Architecture|System|Components"
        in: docs/ARCHITECTURE.md
      - pattern: "Operations|Troubleshooting|Common tasks"
        in: docs/RUNBOOK.md
    maturity_required: [intermediate, advanced]
```

### Maturity Profiles

```yaml
maturity_profiles:
  starter:
    description: "Learning-focused with basic Kubernetes deployment, local development, minimal automation"

    require_additionally:
      - "Kubernetes Deployment manifests"
      - "Health checks configuration"
      - "Namespace and ConfigMap"
      - "Ingress configuration"
      - "Multi-stage Dockerfile"
      - "Deployment scripts"

    skip_deliverables:
      - "Horizontal Pod Autoscaler"
      - "Network policies"
      - "RBAC configuration"
      - "Pod Disruption Budget"
      - "Kustomize overlays"
      - "ServiceMonitor for Prometheus"
      - "CI/CD pipeline"
      - "Security scanning workflow"
      - "Prometheus configuration"
      - "Grafana dashboards"
      - "Istio service mesh (if enabled)"
      - "StatefulSet for database (if stateful)"
      - "Makefile with common operations"

    empty_dirs_allowed:
      - kubernetes/overlays/
      - monitoring/prometheus/
      - monitoring/grafana/dashboards/
      - mesh/
      - tests/integration/

    generation_adjustments:
      - Use fixed replicas (3 pods) instead of HPA
      - ClusterIP service with basic Ingress
      - Docker Compose for local development
      - Simple deployment script without GitOps
      - Extensive inline comments in manifests
      - README with step-by-step deployment guide

  intermediate:
    description: "Production-ready with autoscaling, monitoring, security policies, and CI/CD automation"

    require_additionally:
      - "Horizontal Pod Autoscaler"
      - "Network policies"
      - "RBAC configuration"
      - "Pod Disruption Budget"
      - "Docker Compose for development"
      - "Nginx security headers"
      - "CI/CD pipeline"
      - "Docker build and push workflow"
      - "Prometheus configuration"
      - "Grafana dashboards"
      - "Makefile with common operations"
      - "Documentation"

    skip_deliverables:
      - "Kustomize overlays"
      - "ServiceMonitor for Prometheus"
      - "Security scanning workflow"
      - "Istio service mesh (if enabled)"

    empty_dirs_allowed:
      - kubernetes/overlays/
      - mesh/
      - tests/performance/

    generation_adjustments:
      - HPA with CPU/memory metrics
      - NetworkPolicies with default-deny
      - RBAC with least-privilege service accounts
      - GitHub Actions CI/CD with staging deployment
      - Prometheus metrics and basic alerting
      - Grafana dashboards for cluster and app metrics
      - Let's Encrypt TLS with cert-manager

  advanced:
    description: "Enterprise-scale with Kustomize overlays, service mesh, advanced monitoring, comprehensive security"

    require_additionally:
      - "Kustomize overlays"
      - "ServiceMonitor for Prometheus"
      - "Security scanning workflow"
      - "Istio service mesh (if enabled)"
      - "StatefulSet for database (if stateful)"

    skip_deliverables: []

    empty_dirs_allowed:
      - data/
      - logs/

    generation_adjustments:
      - Kustomize with dev/staging/production overlays
      - Vertical Pod Autoscaler for resource optimization
      - Istio service mesh with strict mTLS
      - Pod Security Standards (Restricted)
      - ArgoCD GitOps deployment
      - Multi-cluster setup capability
      - Comprehensive monitoring (Prometheus Operator)
      - Advanced alerting with SLOs
      - Security scanning in CI (Trivy, Grype)
      - SLSA provenance generation
      - Cost analysis and optimization scripts
```

### Validation Process

After all skills complete, the skillchain orchestrator validates deliverables:

1. **File Existence Check**
   - Verify all `required_files` exist for the selected maturity level
   - Allow `empty_dirs_allowed` to be empty or non-existent

2. **Content Pattern Matching**
   - Run regex `pattern` checks against file contents
   - Ensure Kubernetes manifests have required fields
   - Verify Docker multi-stage builds
   - Check CI/CD workflow structure

3. **Cross-Skill Integration**
   - Validate Docker images referenced in Kubernetes manifests exist
   - Ensure Ingress annotations match nginx configuration
   - Verify ServiceMonitor matches Prometheus scrape config
   - Check service mesh manifests reference correct services

4. **Maturity-Specific Validation**
   - **Starter**: Basic deployment works, health checks pass, Ingress accessible
   - **Intermediate**: HPA scales, NetworkPolicies enforced, CI/CD deploys to staging
   - **Advanced**: Kustomize overlays apply, service mesh mTLS active, security scanning passes

5. **Report Generation**
   ```
   ✓ Kubernetes Deployment manifests (operating-kubernetes)
   ✓ Health checks configuration (operating-kubernetes)
   ✓ Multi-stage Dockerfile (writing-dockerfiles)
   ✓ Ingress configuration (configuring-nginx)
   ✗ Horizontal Pod Autoscaler (operating-kubernetes) - SKIPPED (starter)
   ✗ Network policies (operating-kubernetes) - SKIPPED (starter)

   Validation: 15/20 required deliverables present (5 skipped for starter maturity)
   Status: PASSED
   ```

### Common Validation Failures

**Issue**: Missing resource requests/limits
- **Check**: `resources: (requests|limits):` in deployment.yaml
- **Fix**: Add CPU/memory requests and limits to all containers

**Issue**: No health checks configured
- **Check**: `livenessProbe:|readinessProbe:` in deployment.yaml
- **Fix**: Add HTTP health check endpoints

**Issue**: Ingress missing TLS configuration
- **Check**: `tls:|cert-manager.io` in ingress.yaml
- **Fix**: Add cert-manager annotation or TLS secret

**Issue**: CI/CD workflow doesn't build Docker image
- **Check**: `docker/build-push-action` in ci.yml
- **Fix**: Add Docker build and push step

**Issue**: Prometheus not scraping metrics
- **Check**: `kind: ServiceMonitor` exists
- **Fix**: Create ServiceMonitor with correct selector

**Issue**: Service mesh mTLS not enforced
- **Check**: `STRICT` in peer-authentication.yaml
- **Fix**: Change mTLS mode from PERMISSIVE to STRICT

---

**Blueprint Complete**
