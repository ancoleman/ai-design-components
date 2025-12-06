# Flux CD Implementation Patterns

Complete guide to implementing Flux CD for GitOps workflows.

## Table of Contents

1. [Installation and Bootstrap](#installation-and-bootstrap)
2. [Source Controllers](#source-controllers)
3. [Kustomization Controller](#kustomization-controller)
4. [Helm Controller](#helm-controller)
5. [Notification Controller](#notification-controller)
6. [Image Automation](#image-automation)
7. [Multi-Tenancy](#multi-tenancy)

## Installation and Bootstrap

### Flux CLI Installation

```bash
# macOS
brew install fluxcd/tap/flux

# Linux
curl -s https://fluxcd.io/install.sh | sudo bash

# Verify installation
flux --version
```

### Bootstrap GitHub

```bash
# Export GitHub token
export GITHUB_TOKEN=<your-token>

# Bootstrap Flux
flux bootstrap github \
  --owner=myorg \
  --repository=fleet-infra \
  --branch=main \
  --path=clusters/production \
  --personal
```

### Bootstrap GitLab

```bash
# Export GitLab token
export GITLAB_TOKEN=<your-token>

# Bootstrap Flux
flux bootstrap gitlab \
  --owner=myorg \
  --repository=fleet-infra \
  --branch=main \
  --path=clusters/production \
  --token-auth
```

### Bootstrap Generic Git

```bash
# For any Git server
flux bootstrap git \
  --url=ssh://git@git.example.com/myorg/fleet-infra \
  --branch=main \
  --path=clusters/production \
  --private-key-file=/path/to/private-key
```

## Source Controllers

### GitRepository Source

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/myorg/myapp
  ref:
    branch: main
  secretRef:
    name: git-credentials
  ignore: |
    # Exclude files from sync
    .git/
    .github/
    *.md
```

### GitRepository with SSH

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: myapp-ssh
  namespace: flux-system
spec:
  interval: 5m
  url: ssh://git@github.com/myorg/myapp.git
  ref:
    branch: main
  secretRef:
    name: ssh-credentials
---
apiVersion: v1
kind: Secret
metadata:
  name: ssh-credentials
  namespace: flux-system
type: Opaque
stringData:
  identity: |
    -----BEGIN OPENSSH PRIVATE KEY-----
    ...
    -----END OPENSSH PRIVATE KEY-----
  known_hosts: |
    github.com ssh-rsa AAAA...
```

### GitRepository with Tag

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: myapp-release
  namespace: flux-system
spec:
  interval: 10m
  url: https://github.com/myorg/myapp
  ref:
    tag: v1.2.3
```

### GitRepository with SemVer

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: myapp-semver
  namespace: flux-system
spec:
  interval: 10m
  url: https://github.com/myorg/myapp
  ref:
    semver: ">=1.0.0 <2.0.0"
```

### OCIRepository Source

```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: OCIRepository
metadata:
  name: myapp-oci
  namespace: flux-system
spec:
  interval: 5m
  url: oci://ghcr.io/myorg/myapp-config
  ref:
    tag: latest
  provider: generic
```

### OCIRepository with Authentication

```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: OCIRepository
metadata:
  name: private-oci
  namespace: flux-system
spec:
  interval: 5m
  url: oci://registry.example.com/myapp/config
  ref:
    tag: v1.0.0
  secretRef:
    name: oci-credentials
  provider: generic
---
apiVersion: v1
kind: Secret
metadata:
  name: oci-credentials
  namespace: flux-system
type: kubernetes.io/dockerconfigjson
stringData:
  .dockerconfigjson: |
    {
      "auths": {
        "registry.example.com": {
          "username": "myuser",
          "password": "mytoken"
        }
      }
    }
```

### HelmRepository Source

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: HelmRepository
metadata:
  name: bitnami
  namespace: flux-system
spec:
  interval: 1h
  url: https://charts.bitnami.com/bitnami
```

### HelmRepository with Authentication

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: HelmRepository
metadata:
  name: private-charts
  namespace: flux-system
spec:
  interval: 1h
  url: https://charts.example.com
  secretRef:
    name: helm-credentials
---
apiVersion: v1
kind: Secret
metadata:
  name: helm-credentials
  namespace: flux-system
type: Opaque
stringData:
  username: myuser
  password: mytoken
```

## Kustomization Controller

### Basic Kustomization

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  retryInterval: 2m
  timeout: 5m
  path: "./k8s/base"
  prune: true
  sourceRef:
    kind: GitRepository
    name: myapp
  targetNamespace: myapp
  wait: true
```

### Kustomization with Dependencies

```yaml
# Base infrastructure
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: infrastructure
  namespace: flux-system
spec:
  interval: 10m
  path: "./infrastructure"
  prune: true
  sourceRef:
    kind: GitRepository
    name: fleet-infra
---
# Application depends on infrastructure
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 5m
  dependsOn:
  - name: infrastructure
  path: "./apps/myapp"
  prune: true
  sourceRef:
    kind: GitRepository
    name: fleet-infra
```

### Kustomization with Health Checks

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  path: "./k8s/prod"
  prune: true
  sourceRef:
    kind: GitRepository
    name: myapp
  healthChecks:
  - apiVersion: apps/v1
    kind: Deployment
    name: myapp
    namespace: myapp
  - apiVersion: apps/v1
    kind: StatefulSet
    name: myapp-db
    namespace: myapp
  wait: true
  timeout: 5m
```

### Kustomization with Patches

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp-prod
  namespace: flux-system
spec:
  interval: 10m
  path: "./k8s/base"
  prune: true
  sourceRef:
    kind: GitRepository
    name: myapp
  targetNamespace: myapp-prod
  patches:
  - patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: myapp
      spec:
        replicas: 5
    target:
      kind: Deployment
      name: myapp
  - patch: |-
      apiVersion: v1
      kind: Service
      metadata:
        name: myapp
      spec:
        type: LoadBalancer
    target:
      kind: Service
      name: myapp
```

### Kustomization with Post-Build Variables

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  path: "./k8s/base"
  prune: true
  sourceRef:
    kind: GitRepository
    name: myapp
  postBuild:
    substitute:
      APP_VERSION: "v1.2.3"
      ENVIRONMENT: "production"
      REPLICAS: "5"
    substituteFrom:
    - kind: ConfigMap
      name: cluster-vars
```

### Kustomization with Force Apply

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  path: "./k8s/prod"
  prune: true
  force: true  # Force apply on conflicts
  sourceRef:
    kind: GitRepository
    name: myapp
```

## Helm Controller

### Basic HelmRelease

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: nginx
  namespace: flux-system
spec:
  interval: 10m
  chart:
    spec:
      chart: nginx
      version: ">=13.0.0 <14.0.0"
      sourceRef:
        kind: HelmRepository
        name: bitnami
        namespace: flux-system
  values:
    replicaCount: 3
    service:
      type: LoadBalancer
```

### HelmRelease with ValuesFrom

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  chart:
    spec:
      chart: myapp
      sourceRef:
        kind: HelmRepository
        name: myorg-charts
  valuesFrom:
  - kind: ConfigMap
    name: myapp-values
  - kind: Secret
    name: myapp-secrets
    valuesKey: values.yaml
  values:
    replicas: 5
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-values
  namespace: flux-system
data:
  values.yaml: |
    service:
      type: LoadBalancer
    ingress:
      enabled: true
```

### HelmRelease with Rollback

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  chart:
    spec:
      chart: myapp
      sourceRef:
        kind: HelmRepository
        name: myorg-charts
  upgrade:
    remediation:
      retries: 3
  rollback:
    recreate: true
    force: true
    cleanupOnFail: true
  test:
    enable: true
```

### HelmRelease with Dependencies

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  dependsOn:
  - name: postgresql
    namespace: flux-system
  - name: redis
    namespace: flux-system
  chart:
    spec:
      chart: myapp
      sourceRef:
        kind: HelmRepository
        name: myorg-charts
```

## Notification Controller

### Slack Notifications

```yaml
apiVersion: notification.toolkit.fluxcd.io/v1beta3
kind: Provider
metadata:
  name: slack
  namespace: flux-system
spec:
  type: slack
  channel: deployments
  secretRef:
    name: slack-webhook-url
---
apiVersion: v1
kind: Secret
metadata:
  name: slack-webhook-url
  namespace: flux-system
type: Opaque
stringData:
  address: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
---
apiVersion: notification.toolkit.fluxcd.io/v1beta3
kind: Alert
metadata:
  name: slack-deployments
  namespace: flux-system
spec:
  providerRef:
    name: slack
  eventSeverity: info
  eventSources:
  - kind: GitRepository
    name: '*'
  - kind: Kustomization
    name: '*'
```

### Microsoft Teams Notifications

```yaml
apiVersion: notification.toolkit.fluxcd.io/v1beta3
kind: Provider
metadata:
  name: teams
  namespace: flux-system
spec:
  type: msteams
  secretRef:
    name: teams-webhook-url
---
apiVersion: notification.toolkit.fluxcd.io/v1beta3
kind: Alert
metadata:
  name: teams-alerts
  namespace: flux-system
spec:
  providerRef:
    name: teams
  eventSeverity: error
  eventSources:
  - kind: Kustomization
    name: '*'
```

### Git Commit Status

```yaml
apiVersion: notification.toolkit.fluxcd.io/v1beta3
kind: Provider
metadata:
  name: github
  namespace: flux-system
spec:
  type: github
  address: https://github.com/myorg/myapp
  secretRef:
    name: github-token
---
apiVersion: notification.toolkit.fluxcd.io/v1beta3
kind: Alert
metadata:
  name: github-status
  namespace: flux-system
spec:
  providerRef:
    name: github
  eventSeverity: info
  eventSources:
  - kind: Kustomization
    name: myapp
```

## Image Automation

### ImageRepository

```yaml
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageRepository
metadata:
  name: myapp
  namespace: flux-system
spec:
  image: ghcr.io/myorg/myapp
  interval: 1m
  secretRef:
    name: ghcr-credentials
```

### ImagePolicy

```yaml
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata:
  name: myapp
  namespace: flux-system
spec:
  imageRepositoryRef:
    name: myapp
  policy:
    semver:
      range: ">=1.0.0 <2.0.0"
```

### ImageUpdateAutomation

```yaml
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageUpdateAutomation
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 1m
  sourceRef:
    kind: GitRepository
    name: myapp
  git:
    checkout:
      ref:
        branch: main
    commit:
      author:
        email: flux@example.com
        name: Flux Bot
      messageTemplate: |
        Update image to {{range .Updated.Images}}{{println .}}{{end}}
    push:
      branch: main
  update:
    path: ./k8s
    strategy: Setters
```

### Image Marker in Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
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
        image: ghcr.io/myorg/myapp:v1.0.0 # {"$imagepolicy": "flux-system:myapp"}
        ports:
        - containerPort: 8080
```

## Multi-Tenancy

### Namespace Isolation

```yaml
# Tenant namespace
apiVersion: v1
kind: Namespace
metadata:
  name: tenant-a
  labels:
    toolkit.fluxcd.io/tenant: tenant-a
---
# Tenant GitRepository
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: tenant-a-repo
  namespace: tenant-a
spec:
  interval: 1m
  url: https://github.com/tenant-a/apps
  ref:
    branch: main
---
# Tenant Kustomization
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: tenant-a-apps
  namespace: tenant-a
spec:
  interval: 10m
  path: "./apps"
  prune: true
  serviceAccountName: kustomize-controller
  sourceRef:
    kind: GitRepository
    name: tenant-a-repo
  targetNamespace: tenant-a
```

### Service Account with RBAC

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tenant-a-reconciler
  namespace: tenant-a
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: tenant-a-reconciler
  namespace: tenant-a
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: tenant-a-reconciler
  namespace: tenant-a
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: tenant-a-reconciler
subjects:
- kind: ServiceAccount
  name: tenant-a-reconciler
  namespace: tenant-a
```

## CLI Operations

### Source Commands

```bash
# List all sources
flux get sources all

# Get GitRepository status
flux get sources git myapp

# Reconcile source immediately
flux reconcile source git myapp

# Suspend/resume source
flux suspend source git myapp
flux resume source git myapp
```

### Kustomization Commands

```bash
# List kustomizations
flux get kustomizations

# View kustomization details
flux get kustomization myapp --with-source

# Reconcile immediately
flux reconcile kustomization myapp --with-source

# Suspend/resume
flux suspend kustomization myapp
flux resume kustomization myapp
```

### HelmRelease Commands

```bash
# List HelmReleases
flux get helmreleases

# View HelmRelease details
flux get helmrelease nginx

# Reconcile immediately
flux reconcile helmrelease nginx

# Suspend/resume
flux suspend helmrelease nginx
flux resume helmrelease nginx
```

### Troubleshooting Commands

```bash
# View controller logs
flux logs --all-namespaces
flux logs --kind=Kustomization --name=myapp

# Check system status
flux check

# View events
flux events --for Kustomization/myapp

# Export configuration
flux export source git myapp
flux export kustomization myapp
```

## Best Practices

### Repository Structure

Organize repositories with clear separation:

```
fleet-infra/
├── clusters/
│   ├── production/
│   │   └── flux-system/
│   ├── staging/
│   └── dev/
├── infrastructure/
│   ├── sources/
│   ├── crds/
│   └── controllers/
└── apps/
    ├── base/
    └── production/
```

### Source Management

- Use appropriate intervals (1m for dev, 5-10m for prod)
- Implement authentication for private repositories
- Use semver for production deployments
- Enable verification for signed commits

### Kustomization Strategy

- Use dependencies for ordered deployment
- Enable health checks for critical apps
- Set appropriate timeouts
- Use prune carefully in production

### Helm Management

- Pin chart versions in production
- Use valuesFrom for environment-specific config
- Enable rollback for safety
- Test charts before production deployment

### Monitoring

- Configure notifications for failures
- Track reconciliation metrics
- Monitor Git source health
- Alert on sync failures
