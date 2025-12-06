# Multi-Cluster Management

Manage deployments across multiple Kubernetes clusters using GitOps.


## Table of Contents

- [ArgoCD Multi-Cluster](#argocd-multi-cluster)
  - [Cluster Registration](#cluster-registration)
  - [ApplicationSet for Multi-Cluster](#applicationset-for-multi-cluster)
- [Flux Multi-Cluster](#flux-multi-cluster)
  - [Bootstrap Multiple Clusters](#bootstrap-multiple-clusters)
  - [Remote Cluster Management](#remote-cluster-management)

## ArgoCD Multi-Cluster

### Cluster Registration

```bash
# List available contexts
kubectl config get-contexts

# Add cluster to ArgoCD
argocd cluster add prod-cluster \
  --kubeconfig ~/.kube/prod-config \
  --name prod-cluster \
  --namespace argocd

# List registered clusters
argocd cluster list

# Get cluster details
argocd cluster get https://prod-cluster.example.com
```

### ApplicationSet for Multi-Cluster

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: multi-cluster-app
  namespace: argocd
spec:
  generators:
  - clusters:
      selector:
        matchLabels:
          environment: production
  template:
    metadata:
      name: 'myapp-{{name}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/myapp.git
        targetRevision: HEAD
        path: k8s/base
      destination:
        server: '{{server}}'
        namespace: myapp
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

## Flux Multi-Cluster

### Bootstrap Multiple Clusters

```bash
# Bootstrap production cluster
flux bootstrap github \
  --owner=myorg \
  --repository=fleet-infra \
  --branch=main \
  --path=clusters/production

# Bootstrap staging cluster
flux bootstrap github \
  --owner=myorg \
  --repository=fleet-infra \
  --branch=main \
  --path=clusters/staging
```

### Remote Cluster Management

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp-remote
  namespace: flux-system
spec:
  interval: 10m
  kubeConfig:
    secretRef:
      name: remote-cluster-kubeconfig
  sourceRef:
    kind: GitRepository
    name: myapp
  path: ./k8s/prod
---
apiVersion: v1
kind: Secret
metadata:
  name: remote-cluster-kubeconfig
  namespace: flux-system
type: Opaque
stringData:
  value: |
    apiVersion: v1
    kind: Config
    clusters:
    - cluster:
        certificate-authority-data: LS0t...
        server: https://remote-cluster.example.com
      name: remote-cluster
    contexts:
    - context:
        cluster: remote-cluster
        user: flux
      name: flux@remote-cluster
    current-context: flux@remote-cluster
    users:
    - name: flux
      user:
        token: eyJhbG...
```
