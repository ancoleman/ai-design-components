# GitOps with ArgoCD and Flux

GitOps patterns for continuous deployment with ArgoCD and Flux.

## Table of Contents

- [GitOps Principles](#gitops-principles)
- [ArgoCD Setup](#argocd-setup)
- [Flux Setup](#flux-setup)
- [Comparison](#argocd-vs-flux)
- [Best Practices](#best-practices)

## GitOps Principles

GitOps uses Git as the single source of truth for declarative infrastructure and applications.

**Core Principles**:
1. **Declarative**: Entire system state described declaratively
2. **Versioned**: System state versioned in Git
3. **Immutable**: Pull-based deployment (Git → Cluster)
4. **Automated**: Changes automatically applied
5. **Reconciled**: System continuously reconciles to desired state

**Benefits**:
- Audit trail (Git history)
- Rollback capability (git revert)
- Disaster recovery (redeploy from Git)
- Developer experience (git push to deploy)

## ArgoCD Setup

ArgoCD is a declarative, GitOps continuous delivery tool for Kubernetes.

### Installation

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Access ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Application Definition

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default

  source:
    repoURL: https://github.com/org/repo
    targetRevision: main
    path: k8s/manifests

    # For Helm charts
    helm:
      valueFiles:
        - values-production.yaml
      parameters:
        - name: replicaCount
          value: "3"

  destination:
    server: https://kubernetes.default.svc
    namespace: production

  syncPolicy:
    automated:
      prune: true        # Delete resources not in Git
      selfHeal: true     # Force sync if cluster state differs
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### Directory Structure for ArgoCD

```
git-repo/
├── apps/
│   ├── production/
│   │   ├── api/
│   │   │   ├── kustomization.yaml
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   └── frontend/
│   │       └── ...
│   └── staging/
│       └── ...
├── base/
│   ├── api/
│   │   ├── kustomization.yaml
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── frontend/
│       └── ...
└── argocd-apps/
    ├── production-apps.yaml
    └── staging-apps.yaml
```

### Multi-Environment Pattern

**App of Apps Pattern**:

```yaml
# argocd-apps/production-apps.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: production-apps
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo
    targetRevision: main
    path: apps/production
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Health Checks

ArgoCD automatically detects health based on resource type.

**Custom Health Check**:

```lua
-- Custom health check for CRD
hs = {}
if obj.status ~= nil then
  if obj.status.conditions ~= nil then
    for i, condition in ipairs(obj.status.conditions) do
      if condition.type == "Ready" and condition.status == "True" then
        hs.status = "Healthy"
        hs.message = "Application is ready"
        return hs
      end
    end
  end
end
hs.status = "Progressing"
hs.message = "Application is not ready"
return hs
```

### ArgoCD CLI Usage

```bash
# Install ArgoCD CLI
brew install argocd

# Login
argocd login localhost:8080

# List applications
argocd app list

# Get application details
argocd app get my-app

# Sync application
argocd app sync my-app

# Rollback to previous version
argocd app rollback my-app

# View diff before sync
argocd app diff my-app

# Set application parameters
argocd app set my-app --helm-set replicaCount=5
```

## Flux Setup

Flux is a GitOps toolkit for Kubernetes.

### Installation

```bash
# Install Flux CLI
brew install fluxcd/tap/flux

# Check prerequisites
flux check --pre

# Bootstrap Flux (GitHub)
flux bootstrap github \
  --owner=my-org \
  --repository=my-repo \
  --branch=main \
  --path=clusters/production \
  --personal

# Bootstrap creates:
# - flux-system namespace
# - source-controller
# - kustomize-controller
# - helm-controller
# - notification-controller
```

### GitRepository Source

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: my-app-repo
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/org/repo
  ref:
    branch: main
  secretRef:
    name: git-credentials
```

### Kustomization

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: my-app
  namespace: flux-system
spec:
  interval: 5m
  path: ./k8s/overlays/production
  prune: true
  sourceRef:
    kind: GitRepository
    name: my-app-repo
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: my-app
      namespace: production
  timeout: 2m
```

### HelmRelease

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
  name: my-app
  namespace: production
spec:
  interval: 10m
  chart:
    spec:
      chart: my-app
      version: "1.0.0"
      sourceRef:
        kind: HelmRepository
        name: my-helm-repo
        namespace: flux-system
  values:
    replicaCount: 3
    image:
      tag: v1.2.3
  upgrade:
    remediation:
      retries: 3
```

### Directory Structure for Flux

```
git-repo/
├── clusters/
│   ├── production/
│   │   ├── flux-system/
│   │   │   ├── gotk-components.yaml
│   │   │   ├── gotk-sync.yaml
│   │   │   └── kustomization.yaml
│   │   └── apps/
│   │       ├── kustomization.yaml
│   │       ├── api.yaml
│   │       └── frontend.yaml
│   └── staging/
│       └── ...
└── apps/
    ├── base/
    │   ├── api/
    │   └── frontend/
    └── overlays/
        ├── production/
        └── staging/
```

### Flux Notifications

```yaml
apiVersion: notification.toolkit.fluxcd.io/v1beta1
kind: Provider
metadata:
  name: slack
  namespace: flux-system
spec:
  type: slack
  channel: deployments
  secretRef:
    name: slack-webhook

---
apiVersion: notification.toolkit.fluxcd.io/v1beta1
kind: Alert
metadata:
  name: deployment-alerts
  namespace: flux-system
spec:
  providerRef:
    name: slack
  eventSeverity: info
  eventSources:
    - kind: Kustomization
      name: '*'
    - kind: HelmRelease
      name: '*'
```

## ArgoCD vs Flux

### Comparison Matrix

| Feature | ArgoCD | Flux |
|---------|--------|------|
| **UI** | Rich web UI | CLI-focused (no UI) |
| **Multi-tenancy** | Built-in RBAC | Requires setup |
| **CNCF Status** | Graduated | Graduated |
| **Architecture** | Single controller | Multiple controllers |
| **Complexity** | Higher learning curve | Simpler, Kubernetes-native |
| **Helm Support** | Excellent | Excellent |
| **Kustomize Support** | Excellent | Excellent |
| **Image Automation** | Via Image Updater | Built-in |
| **Notifications** | Built-in | Built-in |
| **Multi-cluster** | Excellent | Good |
| **Best for** | Platform teams, multi-cluster | DevOps automation, single cluster |

### When to Choose ArgoCD

- Multi-team platform (RBAC, SSO)
- Need web UI for visibility
- Centralized control plane
- Multi-cluster management
- Complex application dependencies

### When to Choose Flux

- Kubernetes-native approach
- CI/CD pipeline integration
- Image automation workflows
- Simpler architecture preferred
- Strong Kustomize usage

## Best Practices

### Repository Structure

**Monorepo Pattern**:
```
gitops-repo/
├── apps/
│   ├── base/          # Base configurations
│   └── overlays/      # Environment-specific
│       ├── dev/
│       ├── staging/
│       └── production/
├── infrastructure/
│   ├── controllers/   # Ingress, cert-manager
│   └── monitoring/    # Prometheus, Grafana
└── clusters/
    ├── dev-cluster/
    ├── staging-cluster/
    └── production-cluster/
```

**Multi-Repo Pattern**:
```
app-repo/              # Application code
├── src/
└── k8s/              # Manifests

infra-repo/           # Infrastructure configs
├── base/
└── overlays/
```

### Secrets Management

**Sealed Secrets** (Recommended):

```bash
# Install kubeseal
brew install kubeseal

# Create sealed secret
kubectl create secret generic my-secret \
  --from-literal=password=mysecret \
  --dry-run=client -o yaml | \
  kubeseal -o yaml > sealed-secret.yaml

# Commit sealed-secret.yaml to Git
git add sealed-secret.yaml
git commit -m "Add sealed secret"
```

**External Secrets Operator**:

Works with AWS Secrets Manager, Vault, GCP Secret Manager.

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secretsmanager
  target:
    name: database-secret
  data:
  - secretKey: password
    remoteRef:
      key: prod/database/password
```

### Progressive Rollout

**Canary Deployment with ArgoCD + Argo Rollouts**:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  replicas: 10
  strategy:
    canary:
      steps:
      - setWeight: 10
      - pause: {duration: 5m}
      - setWeight: 30
      - pause: {duration: 5m}
      - setWeight: 60
      - pause: {duration: 5m}
      - setWeight: 100
  template:
    spec:
      containers:
      - name: my-app
        image: my-app:v2
```

### Disaster Recovery

**Backup Strategy**:
1. Git is source of truth (commit history = backup)
2. Periodic cluster state snapshots (Velero)
3. Database backups (separate from GitOps)

**Recovery Procedure**:
```bash
# 1. Provision new cluster

# 2. Install ArgoCD/Flux
flux bootstrap github --owner=org --repository=repo

# 3. Applications auto-deploy from Git

# 4. Restore databases from backups
```

### Monitoring and Alerting

**Metrics to Monitor**:
- Sync status (healthy, degraded, progressing)
- Sync frequency
- Failed syncs
- Out-of-sync duration

**Prometheus Metrics (ArgoCD)**:
```
argocd_app_sync_total
argocd_app_health_status
argocd_app_sync_status
```

**Alerts**:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: argocd-alerts
spec:
  groups:
  - name: argocd
    rules:
    - alert: AppOutOfSync
      expr: argocd_app_sync_status{sync_status="OutOfSync"} > 0
      for: 10m
      annotations:
        summary: "Application out of sync for 10 minutes"
```

## Troubleshooting

### ArgoCD Sync Issues

```bash
# Check application status
argocd app get my-app

# View sync errors
argocd app sync my-app --dry-run

# Force sync (bypass hooks)
argocd app sync my-app --force

# Delete and recreate resources
argocd app sync my-app --prune --replace
```

### Flux Reconciliation Issues

```bash
# Check Flux controllers
flux check

# View Kustomization status
flux get kustomizations

# Suspend reconciliation
flux suspend kustomization my-app

# Resume reconciliation
flux resume kustomization my-app

# Force reconciliation
flux reconcile kustomization my-app --with-source
```

### Git Authentication Issues

```bash
# ArgoCD: Add repository
argocd repo add https://github.com/org/repo \
  --username git \
  --password <PAT>

# Flux: Create secret
flux create secret git git-credentials \
  --url=https://github.com/org/repo \
  --username=git \
  --password=<PAT>
```
