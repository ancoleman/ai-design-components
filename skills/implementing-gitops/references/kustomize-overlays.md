# Kustomize Overlay Patterns

Template-free Kubernetes configuration management using Kustomize base and overlay pattern.

## Table of Contents

1. [Basic Concepts](#basic-concepts)
2. [Base Configuration](#base-configuration)
3. [Environment Overlays](#environment-overlays)
4. [Advanced Patterns](#advanced-patterns)
5. [Components](#components)

## Basic Concepts

### Kustomize Principles

- **Declarative:** Pure YAML, no templating
- **Composable:** Base + overlays for environments
- **Patchable:** Strategic merge and JSON patches
- **Reusable:** Components for cross-cutting concerns

### Directory Structure

```
k8s/
├── base/                    # Common configuration
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── kustomization.yaml
├── overlays/
│   ├── dev/                # Development overlay
│   │   └── kustomization.yaml
│   ├── staging/            # Staging overlay
│   │   └── kustomization.yaml
│   └── prod/               # Production overlay
│       ├── kustomization.yaml
│       └── patches/
└── components/             # Reusable components
    ├── monitoring/
    └── security/
```

## Base Configuration

### base/deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 8080
        env:
        - name: LOG_LEVEL
          value: info
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
```

### base/service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
```

### base/configmap.yaml

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  APP_NAME: myapp
  ENVIRONMENT: base
```

### base/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml
- configmap.yaml

commonLabels:
  app: myapp
  managed-by: kustomize

namespace: myapp
```

## Environment Overlays

### overlays/dev/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base

namespace: myapp-dev

namePrefix: dev-

commonLabels:
  environment: development

replicas:
- name: myapp
  count: 1

images:
- name: myapp
  newTag: dev-latest

patches:
- patch: |-
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: myapp-config
    data:
      LOG_LEVEL: debug
      ENVIRONMENT: development
- patch: |-
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: myapp
    spec:
      template:
        spec:
          containers:
          - name: myapp
            env:
            - name: DEBUG
              value: "true"
```

### overlays/staging/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base

namespace: myapp-staging

namePrefix: staging-

commonLabels:
  environment: staging

replicas:
- name: myapp
  count: 2

images:
- name: myapp
  newTag: staging-v1.2.3

patches:
- patch: |-
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: myapp-config
    data:
      LOG_LEVEL: info
      ENVIRONMENT: staging
- patch: |-
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: myapp
    spec:
      template:
        spec:
          containers:
          - name: myapp
            resources:
              limits:
                memory: "256Mi"
                cpu: "500m"
              requests:
                memory: "128Mi"
                cpu: "250m"
```

### overlays/prod/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base

namespace: myapp-prod

namePrefix: prod-

commonLabels:
  environment: production

replicas:
- name: myapp
  count: 5

images:
- name: myapp
  newTag: v1.2.3

patches:
- path: patches/production-resources.yaml
- path: patches/production-service.yaml

configMapGenerator:
- name: myapp-config
  behavior: merge
  literals:
  - LOG_LEVEL=warn
  - ENVIRONMENT=production
  - ENABLE_MONITORING=true

secretGenerator:
- name: myapp-secrets
  files:
  - secrets/database-url
  - secrets/api-key
```

### overlays/prod/patches/production-resources.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: myapp
        resources:
          limits:
            memory: "512Mi"
            cpu: "1000m"
          requests:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

### overlays/prod/patches/production-service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  type: LoadBalancer
  ports:
  - port: 443
    targetPort: 8080
```

## Advanced Patterns

### Strategic Merge Patches

```yaml
# overlays/prod/kustomization.yaml
patches:
- patch: |-
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: myapp
    spec:
      template:
        spec:
          affinity:
            podAntiAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - labelSelector:
                  matchExpressions:
                  - key: app
                    operator: In
                    values:
                    - myapp
                topologyKey: kubernetes.io/hostname
```

### JSON 6902 Patches

```yaml
# overlays/prod/kustomization.yaml
patches:
- target:
    kind: Deployment
    name: myapp
  patch: |-
    - op: add
      path: /spec/template/spec/containers/0/env/-
      value:
        name: FEATURE_FLAG
        value: "enabled"
    - op: replace
      path: /spec/replicas
      value: 10
```

### Image Transformations

```yaml
# overlays/prod/kustomization.yaml
images:
- name: myapp
  newName: registry.example.com/myapp
  newTag: v1.2.3
  digest: sha256:abc123...
```

### Variable Substitution

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml

vars:
- name: SERVICE_NAME
  objref:
    kind: Service
    name: myapp
    apiVersion: v1
  fieldref:
    fieldpath: metadata.name
```

### Generators

```yaml
# overlays/prod/kustomization.yaml
configMapGenerator:
- name: app-config
  literals:
  - DB_HOST=prod-db.example.com
  - CACHE_TTL=3600
  files:
  - configs/app.properties

secretGenerator:
- name: app-secrets
  envs:
  - secrets/.env.prod
  files:
  - tls.crt
  - tls.key
```

## Components

### Monitoring Component

```yaml
# components/monitoring/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1alpha1
kind: Component

resources:
- servicemonitor.yaml

labels:
- pairs:
    monitoring: prometheus

patches:
- patch: |-
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: not-important
    spec:
      template:
        metadata:
          annotations:
            prometheus.io/scrape: "true"
            prometheus.io/port: "8080"
            prometheus.io/path: "/metrics"
  target:
    kind: Deployment
```

### components/monitoring/servicemonitor.yaml

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp-metrics
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
```

### Security Component

```yaml
# components/security/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1alpha1
kind: Component

resources:
- networkpolicy.yaml
- podsecuritypolicy.yaml

patches:
- patch: |-
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: not-important
    spec:
      template:
        spec:
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
            fsGroup: 1000
          containers:
          - name: not-important
            securityContext:
              allowPrivilegeEscalation: false
              readOnlyRootFilesystem: true
              capabilities:
                drop:
                - ALL
  target:
    kind: Deployment
```

### Using Components in Overlays

```yaml
# overlays/prod/kustomization.yaml
resources:
- ../../base

components:
- ../../components/monitoring
- ../../components/security

replicas:
- name: myapp
  count: 5
```

## Testing and Preview

### Preview Generated Manifests

```bash
# Preview dev overlay
kustomize build overlays/dev

# Preview prod overlay
kustomize build overlays/prod

# Preview with kubectl
kubectl kustomize overlays/prod
```

### Validate Manifests

```bash
# Validate YAML syntax
kustomize build overlays/prod | kubectl apply --dry-run=client -f -

# Validate with server
kustomize build overlays/prod | kubectl apply --dry-run=server -f -

# Diff against cluster
kubectl diff -k overlays/prod
```

### Apply Overlays

```bash
# Apply dev overlay
kubectl apply -k overlays/dev

# Apply prod overlay
kubectl apply -k overlays/prod

# Delete resources
kubectl delete -k overlays/dev
```

## Best Practices

### Base Configuration

- Keep base minimal and generic
- Use sensible defaults
- Avoid environment-specific values
- Document customization points

### Overlays

- One overlay per environment
- Use meaningful names (dev, staging, prod)
- Keep patches focused and small
- Document overlay purpose

### Patches

- Prefer strategic merge over JSON 6902
- Keep patches maintainable
- Group related changes
- Use patch files for complex changes

### Components

- Create components for cross-cutting concerns
- Make components optional
- Document component dependencies
- Test components in isolation

### Repository Organization

- Base at repository root or k8s/base
- Overlays in k8s/overlays/
- Components in k8s/components/
- Use consistent naming conventions

### GitOps Integration

Both ArgoCD and Flux support Kustomize natively:

**ArgoCD:**
```yaml
spec:
  source:
    path: k8s/overlays/prod
```

**Flux:**
```yaml
spec:
  path: "./k8s/overlays/prod"
```
