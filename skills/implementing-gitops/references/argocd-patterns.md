# ArgoCD Implementation Patterns

Complete guide to implementing ArgoCD for GitOps workflows.

## Table of Contents

1. [Installation and Configuration](#installation-and-configuration)
2. [Application Patterns](#application-patterns)
3. [ApplicationSet Patterns](#applicationset-patterns)
4. [Sync Policies](#sync-policies)
5. [Sync Hooks](#sync-hooks)
6. [Multi-Tenancy](#multi-tenancy)
7. [CLI Operations](#cli-operations)

## Installation and Configuration

### Standard Installation

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Access UI via port-forward
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

### High Availability Installation

```bash
# Install HA version with multiple replicas
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/ha/install.yaml
```

### Ingress Configuration

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: argocd-server-ingress
  namespace: argocd
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-passthrough: "true"
    nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
spec:
  ingressClassName: nginx
  rules:
  - host: argocd.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: argocd-server
            port:
              name: https
  tls:
  - hosts:
    - argocd.example.com
    secretName: argocd-secret
```

## Application Patterns

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
    repoURL: https://github.com/myorg/myapp.git
    targetRevision: HEAD
    path: k8s/base
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

### Helm Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: nginx
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://charts.bitnami.com/bitnami
    chart: nginx
    targetRevision: 13.2.0
    helm:
      releaseName: nginx
      values: |
        replicaCount: 3
        service:
          type: LoadBalancer
  destination:
    server: https://kubernetes.default.svc
    namespace: nginx
  syncPolicy:
    automated:
      prune: true
```

### Kustomize Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myapp.git
    targetRevision: main
    path: k8s/overlays/prod
    kustomize:
      namePrefix: prod-
      commonLabels:
        environment: production
      images:
      - name: myapp
        newTag: v1.2.3
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp-prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Multi-Source Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-multi
  namespace: argocd
spec:
  project: default
  sources:
  - repoURL: https://github.com/myorg/myapp.git
    targetRevision: main
    path: k8s/base
  - repoURL: https://charts.example.com
    chart: common-library
    targetRevision: 1.0.0
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
```

## ApplicationSet Patterns

### List Generator (Static Environments)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp-envs
  namespace: argocd
spec:
  goTemplate: true
  generators:
  - list:
      elements:
      - env: dev
        cluster: https://kubernetes.default.svc
        replicas: 1
        imageTag: latest
      - env: staging
        cluster: https://kubernetes.default.svc
        replicas: 2
        imageTag: staging-v1.2.3
      - env: prod
        cluster: https://prod-cluster.example.com
        replicas: 5
        imageTag: v1.2.3
  template:
    metadata:
      name: 'myapp-{{.env}}'
      labels:
        environment: '{{.env}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/myapp.git
        targetRevision: HEAD
        path: 'k8s/overlays/{{.env}}'
        kustomize:
          images:
          - name: myapp
            newTag: '{{.imageTag}}'
      destination:
        server: '{{.cluster}}'
        namespace: 'myapp-{{.env}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
        - CreateNamespace=true
```

### Cluster Generator (Dynamic Multi-Cluster)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-apps
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

### Git Directory Generator

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: repo-apps
  namespace: argocd
spec:
  generators:
  - git:
      repoURL: https://github.com/myorg/apps.git
      revision: HEAD
      directories:
      - path: apps/*
  template:
    metadata:
      name: '{{path.basename}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/apps.git
        targetRevision: HEAD
        path: '{{path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{path.basename}}'
      syncPolicy:
        automated:
          prune: true
```

### Progressive Rollout Strategy

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: progressive-rollout
  namespace: argocd
spec:
  generators:
  - list:
      elements:
      - cluster: dev
        url: https://dev-cluster.example.com
        env: development
      - cluster: staging
        url: https://staging-cluster.example.com
        env: staging
      - cluster: prod-us-east
        url: https://prod-us-east.example.com
        env: production
      - cluster: prod-us-west
        url: https://prod-us-west.example.com
        env: production
  strategy:
    type: RollingSync
    rollingSync:
      steps:
      - matchExpressions:
        - key: envLabel
          operator: In
          values:
          - development
        # Deploy to dev immediately (100%)
      - matchExpressions:
        - key: envLabel
          operator: In
          values:
          - staging
        maxUpdate: 1
        # Deploy to staging one at a time
      - matchExpressions:
        - key: envLabel
          operator: In
          values:
          - production
        maxUpdate: 50%
        # Deploy to 50% of prod clusters at once
  template:
    metadata:
      name: 'myapp-{{.cluster}}'
      labels:
        envLabel: '{{.env}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/myapp.git
        targetRevision: HEAD
        path: 'k8s/{{.cluster}}'
      destination:
        server: '{{.url}}'
        namespace: myapp
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

## Sync Policies

### Automated Sync (Dev/Staging)

```yaml
syncPolicy:
  automated:
    prune: true      # Delete resources removed from Git
    selfHeal: true   # Revert manual changes
  syncOptions:
  - CreateNamespace=true
  retry:
    limit: 5
    backoff:
      duration: 5s
      factor: 2
      maxDuration: 3m
```

### Manual Sync (Production)

```yaml
syncPolicy:
  syncOptions:
  - CreateNamespace=true
  - PrunePropagationPolicy=foreground
  - PruneLast=true
  retry:
    limit: 2
    backoff:
      duration: 5s
      maxDuration: 1m
```

### Selective Sync

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
  syncOptions:
  - CreateNamespace=true
  - ApplyOutOfSyncOnly=true  # Only sync out-of-sync resources
  managedNamespaceMetadata:
    labels:
      managed-by: argocd
```

## Sync Hooks

### PreSync: Database Migration

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
      - name: migrate
        image: myapp:latest
        command: ["/bin/sh"]
        args:
        - -c
        - |
          echo "Running database migrations..."
          /app/migrate up
      restartPolicy: Never
  backoffLimit: 3
```

### PostSync: Smoke Test

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: smoke-test
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
spec:
  template:
    spec:
      containers:
      - name: test
        image: curlimages/curl:latest
        command: ["/bin/sh"]
        args:
        - -c
        - |
          echo "Running smoke tests..."
          curl -f http://myapp-service/health || exit 1
          echo "Smoke tests passed!"
      restartPolicy: Never
```

### SyncFail: Rollback

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: rollback-notification
  annotations:
    argocd.argoproj.io/hook: SyncFail
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
      - name: notify
        image: curlimages/curl:latest
        command: ["/bin/sh"]
        args:
        - -c
        - |
          curl -X POST https://slack.com/api/chat.postMessage \
            -H "Authorization: Bearer $SLACK_TOKEN" \
            -d "channel=deployments" \
            -d "text=Deployment failed for myapp"
      restartPolicy: Never
```

### Skip: Resource Lifecycle Management

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: cleanup-job
  annotations:
    argocd.argoproj.io/hook: Skip
    # Resource ignored during sync
spec:
  template:
    spec:
      containers:
      - name: cleanup
        image: busybox
        command: ["echo", "Cleanup task"]
```

## Multi-Tenancy

### Project-Based Isolation

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: team-frontend
  namespace: argocd
spec:
  description: Frontend team project
  sourceRepos:
  - https://github.com/myorg/frontend-*
  destinations:
  - namespace: 'frontend-*'
    server: https://kubernetes.default.svc
  clusterResourceWhitelist:
  - group: ''
    kind: Namespace
  namespaceResourceWhitelist:
  - group: 'apps'
    kind: Deployment
  - group: ''
    kind: Service
  - group: ''
    kind: ConfigMap
  roles:
  - name: frontend-admin
    policies:
    - p, proj:team-frontend:frontend-admin, applications, *, team-frontend/*, allow
    groups:
    - frontend-team
```

### RBAC Configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  policy.default: role:readonly
  policy.csv: |
    # Admin role
    p, role:admin, applications, *, */*, allow
    p, role:admin, clusters, *, *, allow
    p, role:admin, repositories, *, *, allow
    g, admins-group, role:admin

    # Developer role
    p, role:developer, applications, get, */*, allow
    p, role:developer, applications, sync, */*, allow
    g, developers-group, role:developer

    # Read-only role
    p, role:readonly, applications, get, */*, allow
    g, viewers-group, role:readonly
```

## CLI Operations

### Application Management

```bash
# Create application
argocd app create myapp \
  --repo https://github.com/myorg/myapp.git \
  --path k8s/base \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace myapp

# Get application status
argocd app get myapp

# List applications
argocd app list

# Sync application
argocd app sync myapp

# Show diff
argocd app diff myapp

# Delete application
argocd app delete myapp
```

### Cluster Management

```bash
# Add cluster
argocd cluster add prod-cluster \
  --kubeconfig ~/.kube/prod-config \
  --name prod-cluster

# List clusters
argocd cluster list

# Remove cluster
argocd cluster rm https://prod-cluster.example.com
```

### Repository Management

```bash
# Add Git repository
argocd repo add https://github.com/myorg/myapp.git \
  --username myuser \
  --password mytoken

# Add Helm repository
argocd repo add https://charts.example.com \
  --type helm \
  --name example-charts

# List repositories
argocd repo list
```

### Advanced Operations

```bash
# Hard refresh (force Git fetch)
argocd app get myapp --hard-refresh

# Sync specific resources
argocd app sync myapp --resource apps:Deployment:myapp

# Rollback to previous version
argocd app rollback myapp 12

# View application history
argocd app history myapp

# Set application parameters
argocd app set myapp \
  --helm-set replicaCount=5

# Patch application
argocd app patch myapp \
  --patch '{"spec":{"syncPolicy":{"automated":{"prune":true}}}}'
```

## Best Practices

### Application Organization

- Use ApplicationSets for multi-environment deployments
- One Application per microservice
- Group related apps using labels
- Use meaningful application names

### Sync Strategy

- Enable automated sync for dev/staging
- Use manual sync for production
- Enable selfHeal for stability
- Configure retry policies

### Resource Management

- Use resource limits in manifests
- Enable prune to clean up deleted resources
- Use sync waves for ordered deployment
- Implement health checks

### Security

- Use Projects for multi-tenancy
- Configure RBAC policies
- Store secrets using Sealed Secrets or ESO
- Enable audit logging

### Monitoring

- Track sync status and duration
- Alert on sync failures
- Monitor drift detection
- Review application health metrics
