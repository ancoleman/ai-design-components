# Kubernetes + ArgoCD GitOps Example

Complete GitOps deployment with Kubernetes and ArgoCD.

## Prerequisites

- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl configured
- ArgoCD installed on cluster

## Project Structure

```
k8s-argocd/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── kustomization.yaml
├── overlays/
│   ├── development/
│   │   └── kustomization.yaml
│   ├── staging/
│   │   └── kustomization.yaml
│   └── production/
│       └── kustomization.yaml
├── argocd/
│   └── application.yaml
└── README.md
```

## Setup ArgoCD

```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for ArgoCD to be ready
kubectl wait --for=condition=available --timeout=600s deployment/argocd-server -n argocd

# Access ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

## Deploy Application with ArgoCD

1. **Update Git repository URL** in `argocd/application.yaml`

2. **Apply ArgoCD application**:
```bash
kubectl apply -f argocd/application.yaml
```

3. **Sync application**:
```bash
# Via CLI
argocd app sync my-app

# Or via UI
# Navigate to http://localhost:8080
# Click on application → SYNC
```

## Manual Deployment (Without ArgoCD)

```bash
# Development
kubectl apply -k overlays/development

# Staging
kubectl apply -k overlays/staging

# Production
kubectl apply -k overlays/production
```

## Verify Deployment

```bash
# Check pods
kubectl get pods -n production

# Check service
kubectl get svc -n production

# View logs
kubectl logs -l app=my-app -n production --tail=100 -f

# Port forward to access locally
kubectl port-forward svc/my-app 3000:80 -n production
```

## GitOps Workflow

1. **Make changes** to Kubernetes manifests in Git
2. **Commit and push** to Git repository
3. **ArgoCD detects** changes automatically (every 3 minutes)
4. **ArgoCD syncs** cluster state to match Git
5. **Self-healing**: If manual changes made to cluster, ArgoCD reverts them

## Rollback

```bash
# Via ArgoCD UI
# Click application → HISTORY → Select previous version → ROLLBACK

# Via CLI
argocd app rollback my-app 1
```

## Troubleshooting

**Application out of sync**:
```bash
argocd app get my-app
argocd app diff my-app
```

**Sync errors**:
```bash
argocd app sync my-app --dry-run
```

**Pod fails to start**:
```bash
kubectl describe pod <pod-name> -n production
kubectl logs <pod-name> -n production
```

## Next Steps

- Add Helm charts for complex applications
- Configure health checks
- Set up notifications (Slack, email)
- Implement progressive delivery (Argo Rollouts)
- Add secrets management (Sealed Secrets)
