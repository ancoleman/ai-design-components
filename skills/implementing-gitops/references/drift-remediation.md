# Drift Detection and Remediation

Detecting and correcting configuration drift in GitOps workflows.


## Table of Contents

- [Drift Detection Concepts](#drift-detection-concepts)
- [ArgoCD Drift Detection](#argocd-drift-detection)
  - [View Sync Status](#view-sync-status)
  - [Automatic Self-Healing](#automatic-self-healing)
  - [Manual Sync Operations](#manual-sync-operations)
- [Flux Drift Detection](#flux-drift-detection)
  - [View Kustomization Status](#view-kustomization-status)
  - [Force Reconciliation](#force-reconciliation)
  - [Automatic Drift Correction](#automatic-drift-correction)
- [Disaster Recovery](#disaster-recovery)
  - [ArgoCD Recovery](#argocd-recovery)
  - [Flux Recovery](#flux-recovery)
- [Troubleshooting](#troubleshooting)
  - [OutOfSync Issues](#outofsync-issues)
  - [Resource Finalizers](#resource-finalizers)

## Drift Detection Concepts

**Drift:** Divergence between desired state (Git) and actual state (cluster).

**Common Causes:**
- Manual kubectl apply commands
- Cluster operators modifying resources
- External controllers changing state
- Resource finalizers preventing deletion
- CRD updates requiring migration

## ArgoCD Drift Detection

### View Sync Status

```bash
# Check application sync status
argocd app get myapp

# View detailed diff
argocd app diff myapp

# Hard refresh (fetch latest Git)
argocd app get myapp --hard-refresh
```

### Automatic Self-Healing

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
spec:
  syncPolicy:
    automated:
      prune: true      # Remove resources not in Git
      selfHeal: true   # Revert manual changes
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### Manual Sync Operations

```bash
# Sync specific resource
argocd app sync myapp --resource apps:Deployment:myapp

# Force sync (ignore hooks)
argocd app sync myapp --force

# Sync with prune
argocd app sync myapp --prune

# Dry-run sync
argocd app sync myapp --dry-run
```

## Flux Drift Detection

### View Kustomization Status

```bash
# Check all kustomizations
flux get kustomizations

# Check specific kustomization
flux get kustomization myapp

# View events
flux events --for Kustomization/myapp
```

### Force Reconciliation

```bash
# Reconcile immediately
flux reconcile kustomization myapp

# Reconcile with source update
flux reconcile kustomization myapp --with-source

# Suspend reconciliation
flux suspend kustomization myapp

# Resume reconciliation
flux resume kustomization myapp
```

### Automatic Drift Correction

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
spec:
  interval: 10m       # Check every 10 minutes
  prune: true         # Remove resources not in Git
  force: true         # Force apply on conflicts
  wait: true          # Wait for resources to be ready
  timeout: 5m
  sourceRef:
    kind: GitRepository
    name: myapp
  path: ./k8s/prod
```

## Disaster Recovery

### ArgoCD Recovery

```bash
# 1. Reinstall ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 2. Re-register clusters
argocd cluster add prod-cluster

# 3. Restore applications from Git
kubectl apply -f git-repo/argocd/applications/

# 4. Sync all applications
argocd app sync --all
```

### Flux Recovery

```bash
# Bootstrap Flux (idempotent operation)
flux bootstrap github \
  --owner=myorg \
  --repository=fleet-infra \
  --branch=main \
  --path=clusters/production

# Flux automatically reconciles all resources from Git
```

## Troubleshooting

### OutOfSync Issues

**Check Git connectivity:**
```bash
argocd repo get https://github.com/myorg/myapp
flux get sources git
```

**Validate manifests:**
```bash
kubectl apply --dry-run=server -f manifest.yaml
kustomize build overlays/prod | kubectl apply --dry-run=server -f -
```

**Review sync logs:**
```bash
argocd app logs myapp
flux logs --kind=Kustomization --name=myapp
```

### Resource Finalizers

```bash
# View finalizers
kubectl get deployment myapp -o yaml | grep finalizers -A 5

# Remove finalizer (if stuck)
kubectl patch deployment myapp -p '{"metadata":{"finalizers":[]}}' --type=merge
```
