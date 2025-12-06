---
sidebar_position: 3
title: Implementing GitOps
description: GitOps continuous delivery for Kubernetes using ArgoCD or Flux with Git as single source of truth
tags: [devops, gitops, argocd, flux, kubernetes, continuous-delivery]
---

# Implementing GitOps

Implement GitOps continuous delivery for Kubernetes using declarative, pull-based deployment models where Git serves as the single source of truth for infrastructure and application configuration.

## When to Use

Use GitOps workflows for:
- **Kubernetes Deployments**: Automating application and infrastructure deployments
- **Multi-Cluster Management**: Managing dev, staging, production, and edge clusters
- **Continuous Delivery**: Pull-based CD pipelines with automated reconciliation
- **Drift Detection**: Automatically detecting and correcting configuration drift
- **Audit Requirements**: Complete audit trails via Git commits for compliance
- **Progressive Delivery**: Canary, blue-green, or rolling deployment strategies
- **Disaster Recovery**: Rapid cluster recovery with GitOps bootstrap

**Trigger keywords**: "deploy to Kubernetes", "ArgoCD setup", "Flux bootstrap", "GitOps pipeline", "environment promotion", "multi-cluster deployment"

## Core GitOps Principles

### 1. Git as Single Source of Truth
All system configuration stored in Git repositories. No manual `kubectl apply` or cluster modifications. Declarative manifests (YAML) for all Kubernetes resources, environment-specific overlays, infrastructure configuration, and application deployments.

### 2. Pull-Based Deployment
Operators running inside clusters pull changes from Git and apply them automatically. Benefits include:
- No cluster credentials in CI/CD pipelines
- Support for air-gapped environments
- Self-healing through continuous reconciliation
- Simplified CI/CD

### 3. Automated Reconciliation
GitOps operators continuously compare actual cluster state with desired state in Git and reconcile differences through a continuous loop: watch Git → compare live state → apply differences → report status → repeat.

### 4. Declarative Configuration
Use declarative Kubernetes manifests (not imperative scripts) to define desired state.

## Tool Selection: ArgoCD vs Flux

| Decision Factor | Choose ArgoCD | Choose Flux |
|----------------|---------------|-------------|
| **Team Preference** | Visual management with web UI | CLI/API-first workflows |
| **Learning Curve** | Easier onboarding with UI | Steeper but more flexible |
| **Architecture** | Monolithic, stateful controller | Modular, stateless controllers |
| **Multi-Tenancy** | Built-in RBAC and projects | Kubernetes-native RBAC |
| **Resource Usage** | Higher (includes UI components) | Lower (minimal controllers) |
| **Best For** | Transitioning to GitOps | Platform engineering |

**Hybrid Approach**: Some teams use Flux for infrastructure and ArgoCD for applications.

## Quick Start: ArgoCD

### Installation

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### Basic Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo.git
    targetRevision: HEAD
    path: k8s/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
  syncPolicy:
    automated:
      prune: true      # Remove resources not in Git
      selfHeal: true   # Revert manual changes
```

## Quick Start: Flux

### Bootstrap

```bash
flux bootstrap github \
  --owner=myorg \
  --repository=fleet-infra \
  --branch=main \
  --path=clusters/production
```

### Basic Kustomization

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
```

## Environment Promotion

**Branch-Based Strategy**: `dev` branch → `staging` branch → `main` branch (prod)

**Kustomize-Based Strategy**: `k8s/base/` → `k8s/overlays/{dev,staging,prod}/`

**Promotion Process**:
1. Merge code changes to main branch
2. CI builds container image with tag
3. Update image tag in environment overlay (Git commit)
4. GitOps operator detects change and deploys
5. Test in environment
6. Promote to next environment by updating Git

## Drift Detection and Remediation

GitOps operators continuously monitor for drift between Git (desired state) and cluster (actual state).

### ArgoCD Automatic Self-Healing

```yaml
syncPolicy:
  automated:
    prune: true      # Remove resources not in Git
    selfHeal: true   # Revert manual changes
```

### Flux Automatic Reconciliation

```yaml
spec:
  interval: 10m    # Check every 10 minutes
  prune: true      # Remove resources not in Git
  force: true      # Force apply on conflicts
```

### Manual Operations

```bash
# ArgoCD
argocd app get myapp           # View sync status
argocd app diff myapp          # Show differences
argocd app sync myapp          # Manually trigger sync

# Flux
flux get kustomizations              # View sync status
flux reconcile kustomization myapp   # Force immediate sync
```

## Progressive Delivery

### Canary Deployments
Gradually shift traffic to new version, monitor metrics during rollout, automated rollback on failures.

**ArgoCD**: Use Argo Rollouts for progressive delivery
**Flux**: Integrate Flagger for automated canary analysis

### Blue-Green Deployments
Deploy new version alongside old, switch traffic atomically, instant rollback if issues detected.

## Secret Management

GitOps requires storing configuration in Git, but secrets must be protected.

| Tool | Approach | Security | Complexity |
|------|----------|----------|------------|
| **Sealed Secrets** | Encrypt secrets for Git | Medium | Low |
| **SOPS** | Encrypt files with KMS | High | Medium |
| **External Secrets** | Reference external vaults | High | Medium |
| **HashiCorp Vault** | Central secret management | Very High | High |

## Multi-Cluster Management

### ArgoCD
- Register external clusters with argocd CLI
- Use ApplicationSets to generate Applications per cluster
- Manage from single ArgoCD instance

### Flux
- Bootstrap Flux per cluster
- Use same Git repo with cluster-specific paths
- Configure remote clusters via kubeConfig secrets

## Sync Hooks and Lifecycle

Execute operations before/after syncs using hooks.

### PreSync Hook (Database Migration)

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
```

### PostSync Hook (Smoke Test)

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  annotations:
    argocd.argoproj.io/hook: PostSync
```

## Monitoring and Key Metrics

### Metrics to Track
- **Sync Status**: OutOfSync, Synced, Unknown
- **Sync Frequency**: How often reconciliation occurs
- **Drift Detection**: Time to detect configuration drift
- **Sync Duration**: Time to apply changes
- **Failure Rate**: Failed syncs and causes

**ArgoCD Metrics**: Exposed at `/metrics` endpoint (`argocd_app_sync_total`, `argocd_app_info`)

**Flux Metrics**: From controllers (`gotk_reconcile_condition`, `gotk_reconcile_duration_seconds`)

## CLI Quick Reference

### ArgoCD Commands

```bash
argocd app create <name>          # Create application
argocd app get <name>              # View status
argocd app sync <name>             # Trigger sync
argocd app diff <name>             # Show drift
argocd app list                    # List all applications
```

### Flux Commands

```bash
flux create source git <name>      # Create Git source
flux create kustomization <name>   # Create kustomization
flux get all                       # View all resources
flux reconcile <kind> <name>       # Force reconciliation
flux logs                          # View controller logs
```

## Troubleshooting Common Issues

**Sync Stuck/OutOfSync**:
- Check Git repository accessibility
- Verify manifests are valid YAML
- Review sync logs for errors
- Check resource finalizers

**Self-Heal Not Working**:
- Verify selfHeal enabled in syncPolicy
- Check operator has write permissions
- Review resource ownership labels

**Secrets Not Decrypting**:
- Verify SOPS/ESO controllers installed
- Check KMS/Vault credentials
- Review encryption key configuration

## Related Skills

- [Building CI Pipelines](./building-ci-pipelines) - CI builds images, GitOps deploys them
- [Platform Engineering](./platform-engineering) - GitOps as deployment mechanism in IDPs
- [Writing Dockerfiles](./writing-dockerfiles) - Container images deployed via GitOps

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/implementing-gitops)
- [ArgoCD Patterns](https://github.com/ancoleman/ai-design-components/tree/main/skills/implementing-gitops/references/argocd-patterns.md)
- [Flux Patterns](https://github.com/ancoleman/ai-design-components/tree/main/skills/implementing-gitops/references/flux-patterns.md)
- [Progressive Delivery](https://github.com/ancoleman/ai-design-components/tree/main/skills/implementing-gitops/references/progressive-delivery.md)
- [Working Examples](https://github.com/ancoleman/ai-design-components/tree/main/skills/implementing-gitops/examples)
