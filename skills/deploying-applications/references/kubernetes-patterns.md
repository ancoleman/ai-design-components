# Kubernetes Deployment Patterns

Advanced Kubernetes patterns including Helm 4.0, service mesh, and autoscaling.

## Table of Contents

- [Helm 4.0 Chart Structure](#helm-40-chart-structure)
- [Service Mesh Comparison](#service-mesh-comparison)
- [Autoscaling Strategies](#autoscaling-strategies)
- [Security Best Practices](#security-best-practices)

## Helm 4.0 Chart Structure

Helm 4.0 (November 2025 release) introduces architectural changes.

### Basic Chart Structure

```
my-app-chart/
├── Chart.yaml              # Chart metadata
├── values.yaml             # Default configuration
├── values-production.yaml  # Production overrides
├── values-staging.yaml     # Staging overrides
├── templates/
│   ├── deployment.yaml     # Kubernetes Deployment
│   ├── service.yaml        # Kubernetes Service
│   ├── ingress.yaml        # Ingress configuration
│   ├── configmap.yaml      # ConfigMap
│   ├── secret.yaml         # Secrets (use sealed-secrets)
│   └── hpa.yaml            # Horizontal Pod Autoscaler
└── charts/                 # Dependency charts
```

### Chart.yaml Example

```yaml
apiVersion: v2
name: my-app
description: My production application
type: application
version: 1.0.0
appVersion: "1.0.0"

dependencies:
  - name: postgresql
    version: 12.x.x
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
```

### values.yaml Example

```yaml
replicaCount: 3

image:
  repository: my-app
  pullPolicy: IfNotPresent
  tag: "latest"

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: my-app.example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

### Deployment Template

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "my-app.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: 3000
          protocol: TCP
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
        env:
        - name: NODE_ENV
          value: production
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: {{ include "my-app.fullname" . }}-secrets
              key: database-url
```

### Deployment Commands

```bash
# Install chart
helm install my-app ./my-app-chart

# Install with custom values
helm install my-app ./my-app-chart -f values-production.yaml

# Upgrade release
helm upgrade my-app ./my-app-chart -f values-production.yaml

# Rollback to previous version
helm rollback my-app 1

# List releases
helm list

# Get release status
helm status my-app
```

## Service Mesh Comparison

### Linkerd (Performance-Focused)

**Performance Characteristics**:
- 5-10% latency overhead
- Rust-based control plane
- Minimal resource usage

**When to Use**:
- Performance is critical
- Simple, opinionated configuration
- Lightweight footprint required

**Installation**:

```bash
# Install Linkerd CLI
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh

# Check pre-requisites
linkerd check --pre

# Install control plane
linkerd install --crds | kubectl apply -f -
linkerd install | kubectl apply -f -

# Verify installation
linkerd check

# Inject service mesh into namespace
kubectl annotate namespace default linkerd.io/inject=enabled

# Or inject into deployment
kubectl get deployment my-app -o yaml | linkerd inject - | kubectl apply -f -
```

**mTLS Verification**:

```bash
# Check if traffic is encrypted
linkerd tap deployment/my-app

# Verify mTLS
linkerd edges deployment
```

### Istio (Feature-Rich)

**Performance Characteristics**:
- 25-35% latency overhead
- Envoy-based (C++)
- Higher resource usage

**When to Use**:
- Advanced traffic management (canary, A/B testing)
- Rich observability (Kiali, Grafana)
- Complex routing requirements

**Installation**:

```bash
# Install Istio CLI
curl -L https://istio.io/downloadIstio | sh -

# Install Istio
istioctl install --set profile=default -y

# Label namespace for injection
kubectl label namespace default istio-injection=enabled

# Verify installation
istioctl verify-install
```

**Traffic Splitting (Canary)**:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-app
spec:
  hosts:
  - my-app
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: my-app
        subset: v2
  - route:
    - destination:
        host: my-app
        subset: v1
      weight: 90
    - destination:
        host: my-app
        subset: v2
      weight: 10
```

### Comparison Matrix

| Feature | Linkerd | Istio |
|---------|---------|-------|
| **Performance** | 5-10% overhead | 25-35% overhead |
| **Language** | Rust | C++ (Envoy) |
| **Complexity** | Low | High |
| **mTLS** | Automatic | Automatic |
| **Traffic Splitting** | Yes | Yes (more advanced) |
| **Circuit Breaking** | Basic | Advanced |
| **Retry Logic** | Basic | Advanced |
| **Observability** | Built-in | Kiali, Grafana |
| **Memory Usage** | ~100MB | ~500MB+ |
| **Learning Curve** | Easy | Steep |

## Autoscaling Strategies

### Horizontal Pod Autoscaler (HPA)

Scale pod count based on metrics.

**CPU-Based HPA**:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**Memory-Based HPA**:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
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
```

**Custom Metrics (RPS)**:

Requires Prometheus adapter.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
```

### Vertical Pod Autoscaler (VPA)

Automatically adjust CPU/memory requests.

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: my-app
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 1000m
        memory: 1Gi
```

### Cluster Autoscaler

Automatically add/remove nodes based on resource needs.

**AWS EKS Example**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  template:
    spec:
      containers:
      - image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.28.0
        name: cluster-autoscaler
        command:
        - ./cluster-autoscaler
        - --v=4
        - --stderrthreshold=info
        - --cloud-provider=aws
        - --skip-nodes-with-local-storage=false
        - --expander=least-waste
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/my-cluster
```

## Security Best Practices

### Network Policies

Restrict pod-to-pod communication.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
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
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

### Pod Security Standards

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### Secrets Management

Use external secrets operator with AWS Secrets Manager, Vault, or GCP Secret Manager.

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secretsmanager
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secretsmanager
    kind: SecretStore
  target:
    name: database-secret
    creationPolicy: Owner
  data:
  - secretKey: database-url
    remoteRef:
      key: prod/database/url
```

### RBAC Policies

Principle of least privilege.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: deployment-manager
rules:
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "watch", "create", "update", "patch"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: deployment-manager-binding
  namespace: production
subjects:
- kind: ServiceAccount
  name: ci-cd-sa
  namespace: production
roleRef:
  kind: Role
  name: deployment-manager
  apiGroup: rbac.authorization.k8s.io
```

## Troubleshooting

### Pod Crashes

```bash
# Check pod status
kubectl get pods

# View pod logs
kubectl logs <pod-name>

# Describe pod (events section critical)
kubectl describe pod <pod-name>

# Previous container logs (if crashed)
kubectl logs <pod-name> --previous

# Interactive debugging
kubectl exec -it <pod-name> -- /bin/sh
```

### Resource Issues

```bash
# Check resource usage
kubectl top pods
kubectl top nodes

# Check resource requests vs limits
kubectl describe pod <pod-name> | grep -A 5 "Requests:"

# View events
kubectl get events --sort-by='.lastTimestamp'
```

### Service Mesh Issues

```bash
# Linkerd tap traffic
linkerd tap deployment/my-app

# Linkerd check
linkerd check

# Istio proxy status
istioctl proxy-status

# Istio analyze configuration
istioctl analyze
```
