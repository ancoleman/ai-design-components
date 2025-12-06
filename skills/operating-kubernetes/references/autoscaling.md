# Autoscaling

## Table of Contents

1. [Horizontal Pod Autoscaler (HPA)](#horizontal-pod-autoscaler-hpa)
2. [Vertical Pod Autoscaler (VPA)](#vertical-pod-autoscaler-vpa)
3. [KEDA (Event-Driven Autoscaling)](#keda-event-driven-autoscaling)
4. [Cluster Autoscaler](#cluster-autoscaler)
5. [Autoscaling Decision Framework](#autoscaling-decision-framework)

## Horizontal Pod Autoscaler (HPA)

### HPA v2 (Recommended)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
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
        type: AverageValue
        averageValue: 500Mi
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5min before scaling down
      policies:
      - type: Percent
        value: 50        # Scale down max 50% of current pods
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100       # Can double pods in 1 minute
        periodSeconds: 60
      - type: Pods
        value: 4         # Or add 4 pods, whichever is higher
        periodSeconds: 60
      selectPolicy: Max
```

### Target Types

**Utilization (Percentage):**
```yaml
metrics:
- type: Resource
  resource:
    name: cpu
    target:
      type: Utilization
      averageUtilization: 70  # 70% of requested CPU
```

**AverageValue (Absolute):**
```yaml
metrics:
- type: Resource
  resource:
    name: memory
    target:
      type: AverageValue
      averageValue: 500Mi  # 500MB per pod
```

**Value (Total):**
```yaml
metrics:
- type: Resource
  resource:
    name: cpu
    target:
      type: Value
      value: "2"  # 2 CPU cores total across all pods
```

### Custom Metrics (Prometheus)

**Prerequisites:**
```bash
# Install Prometheus Adapter
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus-adapter prometheus-community/prometheus-adapter \
  --namespace monitoring
```

**HPA with Custom Metric:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "100"  # Scale when >100 req/s per pod
```

**Prometheus Adapter ConfigMap:**
```yaml
rules:
- seriesQuery: 'http_requests_total{namespace="production"}'
  resources:
    overrides:
      namespace: {resource: "namespace"}
      pod: {resource: "pod"}
  name:
    matches: "^(.*)_total$"
    as: "${1}_per_second"
  metricsQuery: 'rate(<<.Series>>{<<.LabelMatchers>>}[2m])'
```

### External Metrics (Datadog, New Relic)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: External
    external:
      metric:
        name: datadog.metric.name
        selector:
          matchLabels:
            app: api
      target:
        type: Value
        value: "100"
```

### Scaling Behavior

**Aggressive Scale-Up, Conservative Scale-Down:**
```yaml
behavior:
  scaleUp:
    stabilizationWindowSeconds: 0  # Scale up immediately
    policies:
    - type: Percent
      value: 100       # Double pods
      periodSeconds: 15
    - type: Pods
      value: 4         # Or add 4 pods
      periodSeconds: 15
    selectPolicy: Max
  scaleDown:
    stabilizationWindowSeconds: 300  # Wait 5 minutes
    policies:
    - type: Percent
      value: 25        # Remove max 25% of pods
      periodSeconds: 60
```

**Prevent Flapping:**
```yaml
behavior:
  scaleDown:
    stabilizationWindowSeconds: 300  # Look at 5min window
    selectPolicy: Max               # Take max recommendation
    policies:
    - type: Pods
      value: 1
      periodSeconds: 60
```

### HPA Troubleshooting

```bash
# Check HPA status
kubectl get hpa -n production

# Describe HPA (see events)
kubectl describe hpa web-app-hpa -n production

# Common issues:
# 1. "unable to get metrics": Metrics server not installed
# 2. "failed to get cpu utilization": No resource requests set
# 3. "invalid metrics": Wrong metric name or query
```

**Fix:**
```bash
# Install metrics server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Ensure pods have resource requests
kubectl get pods -n production -o json | \
  jq '.items[].spec.containers[].resources.requests'
```

## Vertical Pod Autoscaler (VPA)

### Installation

```bash
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler
./hack/vpa-up.sh
```

### VPA Configuration

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app

  updatePolicy:
    updateMode: "Auto"  # Off, Initial, Recreate, Auto

  resourcePolicy:
    containerPolicies:
    - containerName: app
      minAllowed:
        cpu: "100m"
        memory: "128Mi"
      maxAllowed:
        cpu: "2"
        memory: "2Gi"
      controlledResources: ["cpu", "memory"]
      mode: "Auto"
    - containerName: sidecar
      mode: "Off"  # Don't VPA this container
```

### Update Modes

**Off (Recommendations Only):**
```yaml
updatePolicy:
  updateMode: "Off"
```
- VPA calculates recommendations
- No automatic updates
- View: `kubectl describe vpa my-app-vpa`

**Initial:**
```yaml
updatePolicy:
  updateMode: "Initial"
```
- Apply recommendations on pod creation
- Existing pods unchanged
- Good for StatefulSets

**Recreate:**
```yaml
updatePolicy:
  updateMode: "Recreate"
```
- Update running pods (causes restart)
- Evicts and recreates with new resources
- Not for single-replica

**Auto (Future):**
```yaml
updatePolicy:
  updateMode: "Auto"
```
- In-place updates without restart
- Not yet production-ready

### View VPA Recommendations

```bash
kubectl describe vpa my-app-vpa

# Output:
# Recommendation:
#   Container Recommendations:
#     Container Name:  app
#     Lower Bound:
#       Cpu:     250m
#       Memory:  256Mi
#     Target:
#       Cpu:     500m
#       Memory:  512Mi
#     Upper Bound:
#       Cpu:     1
#       Memory:  1Gi
#     Uncapped Target:
#       Cpu:     750m
#       Memory:  768Mi
```

**Interpretation:**
- **Lower Bound:** Minimum for cost efficiency
- **Target:** Recommended values
- **Upper Bound:** Maximum safe values
- **Uncapped Target:** What VPA would recommend without limits

### VPA + HPA Compatibility

**Compatible:**
```yaml
# VPA on CPU/memory
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
    - containerName: app
      controlledResources: ["memory"]  # Only memory
---
# HPA on CPU
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**Not Compatible:**
- VPA Auto/Recreate + HPA on same metric (CPU or memory)
- Results in thrashing and instability

## KEDA (Event-Driven Autoscaling)

### Installation

```bash
helm repo add kedacore https://kedacore.github.io/charts
helm install keda kedacore/keda --namespace keda --create-namespace
```

### RabbitMQ Scaler

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: rabbitmq-scaler
  namespace: production
spec:
  scaleTargetRef:
    name: message-processor
  minReplicaCount: 0   # Scale to zero when queue empty
  maxReplicaCount: 30
  triggers:
  - type: rabbitmq
    metadata:
      host: amqp://user:password@rabbitmq.default.svc.cluster.local:5672
      queueName: tasks
      queueLength: "10"  # Scale up when >10 messages
```

### Kafka Scaler

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: kafka-scaler
spec:
  scaleTargetRef:
    name: kafka-consumer
  minReplicaCount: 1
  maxReplicaCount: 50
  triggers:
  - type: kafka
    metadata:
      bootstrapServers: kafka-broker.kafka:9092
      consumerGroup: my-consumer-group
      topic: events
      lagThreshold: "100"  # Scale when lag >100
```

### AWS SQS Scaler

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: sqs-scaler
spec:
  scaleTargetRef:
    name: sqs-processor
  minReplicaCount: 0
  maxReplicaCount: 20
  triggers:
  - type: aws-sqs-queue
    metadata:
      queueURL: https://sqs.us-east-1.amazonaws.com/123456789/my-queue
      queueLength: "5"
      awsRegion: us-east-1
      identityOwner: operator  # Use IRSA
```

### Prometheus Scaler

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: prometheus-scaler
spec:
  scaleTargetRef:
    name: api-server
  minReplicaCount: 2
  maxReplicaCount: 20
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus.monitoring.svc:9090
      metricName: http_requests_per_second
      query: sum(rate(http_requests_total{service="api"}[2m]))
      threshold: "100"  # Scale when >100 req/sec total
```

### Cron Scaler (Schedule-Based)

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: cron-scaler
spec:
  scaleTargetRef:
    name: batch-processor
  minReplicaCount: 0
  maxReplicaCount: 10
  triggers:
  - type: cron
    metadata:
      timezone: America/New_York
      start: 0 8 * * 1-5     # Scale up at 8am Mon-Fri
      end: 0 18 * * 1-5      # Scale down at 6pm Mon-Fri
      desiredReplicas: "5"
```

### CPU/Memory Scaler (KEDA Alternative to HPA)

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: cpu-scaler
spec:
  scaleTargetRef:
    name: web-app
  minReplicaCount: 2
  maxReplicaCount: 10
  triggers:
  - type: cpu
    metricType: Utilization
    metadata:
      value: "70"
  - type: memory
    metricType: Utilization
    metadata:
      value: "80"
```

### KEDA Fallback

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: fallback-scaler
spec:
  scaleTargetRef:
    name: processor
  fallback:
    failureThreshold: 3
    replicas: 5  # Scale to 5 if scaler fails
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus.monitoring.svc:9090
      query: queue_depth
      threshold: "10"
```

## Cluster Autoscaler

### AWS Installation

```bash
helm repo add autoscaler https://kubernetes.github.io/autoscaler
helm install cluster-autoscaler autoscaler/cluster-autoscaler \
  --namespace kube-system \
  --set autoDiscovery.clusterName=my-cluster \
  --set awsRegion=us-east-1 \
  --set rbac.create=true
```

### Configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-autoscaler-status
  namespace: kube-system
data:
  scale-down-enabled: "true"
  scale-down-delay-after-add: "10m"
  scale-down-unneeded-time: "10m"
  scale-down-utilization-threshold: "0.5"
  max-node-provision-time: "15m"
  skip-nodes-with-local-storage: "false"
  skip-nodes-with-system-pods: "true"
```

### Node Groups (AWS)

```yaml
# Auto Scaling Group tags
k8s.io/cluster-autoscaler/<cluster-name>=owned
k8s.io/cluster-autoscaler/enabled=true
k8s.io/cluster-autoscaler/node-template/label/workload=general
```

### Cluster Autoscaler Behavior

**Scale Up:**
- Pods are Pending due to insufficient resources
- Provision new nodes from auto-scaling group
- Takes 2-5 minutes (cloud provider dependent)

**Scale Down:**
- Node utilization < threshold (default 50%)
- All pods can be rescheduled elsewhere
- Node not running system pods (unless configured)
- Wait 10 minutes (configurable) before scale down

**Prevent Scale Down:**
```yaml
# Annotate pod to prevent node scale-down
apiVersion: v1
kind: Pod
metadata:
  annotations:
    cluster-autoscaler.kubernetes.io/safe-to-evict: "false"
```

### PodDisruptionBudget (PDB)

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-pdb
  namespace: production
spec:
  minAvailable: 2  # Keep at least 2 replicas
  selector:
    matchLabels:
      app: api
```

**Alternative (percentage):**
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-pdb
spec:
  maxUnavailable: 1  # Max 1 pod disrupted
  selector:
    matchLabels:
      app: api
```

## Autoscaling Decision Framework

### Decision Matrix

| Workload | Scaling Dimension | Use HPA | Use VPA | Use KEDA | Use Cluster Autoscaler |
|----------|------------------|---------|---------|----------|------------------------|
| Stateless web app (traffic-driven) | Horizontal | ✅ | ❌ | ❌ | If needed |
| Single DB instance | Vertical | ❌ | ✅ | ❌ | Maybe |
| Queue processor | Horizontal | ❌ | ❌ | ✅ | If needed |
| Scheduled batch job | Horizontal | ❌ | ❌ | ✅ (cron) | If needed |
| Pods pending (no nodes) | Nodes | ❌ | ❌ | ❌ | ✅ |
| Unknown resource needs | Vertical | ❌ | ✅ (Off mode) | ❌ | ❌ |

### Pattern Combinations

**Web Application (Full Stack):**
```yaml
# 1. HPA for horizontal scaling
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
spec:
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
---
# 2. VPA for right-sizing (recommendations only)
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: web-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web
  updatePolicy:
    updateMode: "Off"  # Recommendations only
---
# 3. PDB to protect during scale-down
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: web-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: web
---
# 4. Cluster Autoscaler (configured at cluster level)
```

**Queue Processor:**
```yaml
# KEDA for event-driven scaling
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: processor-scaler
spec:
  scaleTargetRef:
    name: processor
  minReplicaCount: 0
  maxReplicaCount: 50
  triggers:
  - type: rabbitmq
    metadata:
      queueName: tasks
      queueLength: "10"
---
# VPA for right-sizing (Off mode)
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: processor-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: processor
  updatePolicy:
    updateMode: "Off"
```

## Summary

**Autoscaling Pattern Selection:**

| Scenario | Pattern | Configuration |
|----------|---------|---------------|
| Traffic-driven web app | HPA | CPU/memory metrics, 2-10 replicas |
| Queue-based processing | KEDA | RabbitMQ/Kafka/SQS scaler, 0-50 replicas |
| Schedule-based workload | KEDA | Cron scaler, business hours |
| Unknown resource needs | VPA | Off mode, review recommendations |
| Single-instance DB | VPA | Initial/Recreate mode |
| Insufficient nodes | Cluster Autoscaler | Configured at cluster level |

**Best Practices:**
1. Start with HPA for stateless workloads
2. Use KEDA for event-driven scaling (better than HPA for queues)
3. Use VPA in Off mode first (review recommendations)
4. Don't combine VPA Auto + HPA on same metric
5. Set PodDisruptionBudgets to protect critical workloads
6. Enable Cluster Autoscaler with appropriate limits
7. Monitor autoscaling events and adjust thresholds
8. Test autoscaling behavior under load before production
