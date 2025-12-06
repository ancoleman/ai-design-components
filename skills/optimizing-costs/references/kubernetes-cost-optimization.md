# Kubernetes Cost Optimization

## Table of Contents

1. [Kubernetes Cost Challenges](#kubernetes-cost-challenges)
2. [Resource Requests and Limits](#resource-requests-and-limits)
3. [Namespace Quotas and Limits](#namespace-quotas-and-limits)
4. [Cluster Autoscaling](#cluster-autoscaling)
5. [Node Pool Strategies](#node-pool-strategies)
6. [Storage Optimization](#storage-optimization)
7. [Kubecost Implementation](#kubecost-implementation)
8. [Cost Allocation Best Practices](#cost-allocation-best-practices)

---

## Kubernetes Cost Challenges

Kubernetes abstracts infrastructure, making cost visibility difficult:

**Hidden Costs:**
- Idle cluster capacity (nodes allocated but not used by pods)
- Over-provisioned pods (requests >> actual usage)
- Missing resource requests (inefficient bin-packing)
- Orphaned resources (PVCs, LoadBalancers after workload deletion)
- Multi-tenant cost allocation (which team owns what?)

**Cost Drivers:**
```
Total Cluster Cost = Node Costs + Storage Costs + Network Costs + Control Plane

Node Costs = (Number of nodes) × (Instance type cost) × (Uptime hours)
Storage Costs = PV provisioning + Snapshot storage
Network Costs = LoadBalancers + Data transfer + Ingress controllers
```

**Visibility Problem:**
Traditional cloud billing shows node costs, but not:
- Cost per namespace
- Cost per deployment
- Cost per team/project
- Idle vs. utilized capacity

**Solution:** Kubecost or OpenCost for Kubernetes-native cost visibility.

---

## Resource Requests and Limits

### The Problem

**Missing Requests:**
```yaml
# BAD: No resource requests
spec:
  containers:
  - name: app
    image: myapp:latest
    # No resources defined
```

**Impact:**
- Kubernetes scheduler cannot bin-pack efficiently
- Pods may be scheduled on oversized nodes (wasted capacity)
- No cost allocation possible (Kubecost can't attribute costs)

**Over-Provisioned Requests:**
```yaml
# BAD: Requests >> actual usage
spec:
  containers:
  - name: app
    resources:
      requests:
        cpu: 4          # App uses 0.5 CPU average
        memory: 16Gi    # App uses 2 GiB average
```

**Impact:**
- 8x over-provisioning ($1,000/month pod costs $125/month to run)
- Forces cluster to scale up unnecessarily
- Wastes node capacity (other pods can't schedule)

### The Solution

**Right-Sized Requests:**
```yaml
# GOOD: Requests match average usage
spec:
  containers:
  - name: app
    resources:
      requests:
        cpu: 500m        # 0.5 CPU (average usage)
        memory: 2Gi      # 2 GiB (average usage)
      limits:
        cpu: 1500m       # 1.5 CPU (3x requests, allows bursting)
        memory: 6Gi      # 6 GiB (3x requests)
```

**Guidelines:**
- **Requests = Average usage** (measured over 7-30 days)
- **Limits = 2-3x requests** (allow bursting, prevent noisy neighbors)
- **Never set requests > limits** (Kubernetes will reject)
- **CPU limits optional** (throttling can cause latency)
- **Memory limits required** (OOM kills without limits)

### Measuring Actual Usage

**kubectl top:**
```bash
# Current CPU/memory usage per pod
kubectl top pods -n production --containers

# Average over time (requires metrics-server)
kubectl top pods -n production --containers --use-protocol-buffers
```

**Prometheus queries:**
```promql
# Average CPU usage per container (7 days)
avg_over_time(
  container_cpu_usage_seconds_total{namespace="production"}[7d]
)

# Average memory usage per container (7 days)
avg_over_time(
  container_memory_working_set_bytes{namespace="production"}[7d]
)
```

**Kubecost recommendations:**
- Navigate to "Savings" > "Right-size your container requests"
- Kubecost analyzes actual usage and suggests optimal requests/limits

### Vertical Pod Autoscaler (VPA)

Automate resource request recommendations:

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: app-vpa
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  updatePolicy:
    updateMode: "Auto"  # or "Recreate" or "Initial"
  resourcePolicy:
    containerPolicies:
    - containerName: app
      minAllowed:
        cpu: 100m
        memory: 256Mi
      maxAllowed:
        cpu: 2
        memory: 8Gi
      controlledResources: ["cpu", "memory"]
```

**Update Modes:**
- **Auto:** VPA updates pods automatically (recreates pods)
- **Recreate:** VPA updates pods on eviction/restart
- **Initial:** VPA sets requests only on pod creation
- **Off:** VPA generates recommendations only (manual review)

**Recommendation:** Start with "Off" mode, review recommendations, then enable "Auto" for non-critical workloads.

---

## Namespace Quotas and Limits

Prevent runaway resource consumption:

### ResourceQuota

Limit total resources per namespace:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-quota
  namespace: team-backend
spec:
  hard:
    requests.cpu: "100"         # Max 100 CPU cores requested
    requests.memory: 200Gi      # Max 200 GiB memory requested
    limits.cpu: "200"           # Max 200 CPU cores limit
    limits.memory: 400Gi        # Max 400 GiB memory limit
    persistentvolumeclaims: "10" # Max 10 PVCs
    services.loadbalancers: "2"  # Max 2 LoadBalancers
    pods: "50"                   # Max 50 pods
```

**Enforcement:**
- Kubernetes rejects pod creation if quota exceeded
- Prevents single team from consuming entire cluster
- Allocates costs predictably (quota = budget)

### LimitRange

Set default and max requests/limits per pod:

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: team-backend
spec:
  limits:
  - max:
      cpu: "4"
      memory: 16Gi
    min:
      cpu: 100m
      memory: 128Mi
    default:
      cpu: 500m        # Default limit if not specified
      memory: 1Gi
    defaultRequest:
      cpu: 250m        # Default request if not specified
      memory: 512Mi
    type: Container
```

**Benefits:**
- Prevents pods without requests (defaults applied)
- Prevents oversized pods (max enforcement)
- Ensures minimum resources (prevents starvation)

### PriorityClass

Ensure critical workloads get resources:

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: critical-priority
value: 1000000  # Higher = more important
preemptionPolicy: PreemptLowerPriority
globalDefault: false
description: "Critical production workloads"
```

**Usage in Pod:**
```yaml
spec:
  priorityClassName: critical-priority
  containers:
  - name: app
    image: myapp:latest
```

**Cost Impact:**
- Low-priority pods evicted first during node pressure
- Critical workloads guaranteed resources (may increase costs if cluster scales)

---

## Cluster Autoscaling

### Cluster Autoscaler

Automatically add/remove nodes based on pod scheduling:

```yaml
# GKE example (AWS/Azure similar)
gcloud container clusters update my-cluster \
  --enable-autoscaling \
  --min-nodes=3 \
  --max-nodes=20 \
  --zone=us-central1-a
```

**How it Works:**
```
1. Pod scheduled → No node capacity → Scale up (add node)
2. Node idle >10 minutes → Scale down (remove node)
3. Max nodes limit → Prevents overspend
```

**Scale-Down Constraints:**
```yaml
# Prevent scale-down of specific nodes
kubectl annotate node node-1 \
  cluster-autoscaler.kubernetes.io/scale-down-disabled=true

# Allow eviction for scale-down
kubectl annotate pod myapp \
  cluster-autoscaler.kubernetes.io/safe-to-evict=true
```

**Cost Savings:**
- Dev clusters: Scale to 0 during off-hours (nights/weekends)
- Staging: Scale down 50-75% during off-hours
- Production: Scale down to baseline (3-5 nodes minimum)

### Scale-to-Zero Strategies

**CronJob to scale down:**
```yaml
# Scale down dev cluster at 6 PM
apiVersion: batch/v1
kind: CronJob
metadata:
  name: scale-down-dev
spec:
  schedule: "0 18 * * 1-5"  # 6 PM weekdays
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: kubectl
            image: bitnami/kubectl:latest
            command:
            - kubectl
            - scale
            - deployment
            - --all
            - --replicas=0
            - -n
            - development
```

**Scale up at 8 AM:**
```yaml
schedule: "0 8 * * 1-5"  # 8 AM weekdays
command: kubectl scale deployment --all --replicas=3 -n development
```

**Savings:** 60% reduction in dev/test costs (14 hours/day × 5 days/week saved).

---

## Node Pool Strategies

### Mixed Node Pools (Spot + On-Demand)

**Pattern:**
```
├── Critical node pool (on-demand)
│   ├── 3-5 baseline nodes (always running)
│   ├── Hosts: Stateful workloads, databases, critical services
│   └── Taint: node-type=on-demand:NoSchedule
│
└── Burstable node pool (spot/preemptible)
    ├── 0-20 nodes (autoscale to zero)
    ├── Hosts: Stateless workloads, batch jobs, web servers
    ├── Taint: node-type=spot:NoSchedule
    └── Discount: 70-90% vs. on-demand
```

**Toleration for Spot Nodes:**
```yaml
spec:
  tolerations:
  - key: node-type
    operator: Equal
    value: spot
    effect: NoSchedule
  nodeSelector:
    node-type: spot
```

**Benefits:**
- 70% cost reduction on burst workloads
- Critical workloads protected on on-demand nodes
- Graceful handling of spot interruptions (30-second warning)

### Pod Disruption Budgets (PDB)

Ensure availability during node scale-down:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2  # Always keep 2 pods running
  selector:
    matchLabels:
      app: myapp
```

**Use Cases:**
- Prevent all pods evicted during node scale-down
- Ensure availability during voluntary disruptions (upgrades, spot interruptions)

---

## Storage Optimization

### Persistent Volume Cleanup

**Problem:** Orphaned PVCs after workload deletion

```bash
# Find unattached PVCs
kubectl get pvc --all-namespaces | grep Released

# Delete PVC and associated PV
kubectl delete pvc <pvc-name> -n <namespace>
```

**Automation:**
```bash
# Delete PVCs released >7 days ago
kubectl get pvc -A -o json | \
  jq -r '.items[] | select(.status.phase=="Released") |
    select((.metadata.creationTimestamp | fromdateiso8601) < (now - 604800)) |
    "\(.metadata.namespace) \(.metadata.name)"' | \
  xargs -n2 kubectl delete pvc -n
```

### StorageClass Cost Optimization

**Use appropriate storage tiers:**

```yaml
# Expensive: High-performance SSD
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: io2  # $0.125/GB/month + $0.065/IOPS
```

```yaml
# Cost-effective: General purpose SSD
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3  # $0.08/GB/month (37% cheaper)
```

**Reclaim Policy:**
```yaml
reclaimPolicy: Delete  # Auto-delete PV when PVC deleted (prevent orphaned volumes)
```

---

## Kubecost Implementation

### Installation

```bash
helm repo add kubecost https://kubecost.github.io/cost-analyzer/
helm repo update

helm install kubecost kubecost/cost-analyzer \
  --namespace kubecost \
  --create-namespace \
  --set kubecostToken="<your-token>" \
  --set prometheus.server.persistentVolume.size=100Gi
```

### Configuration

```yaml
# kubecost-values.yaml
kubecostProductConfigs:
  cloudIntegrationSecret: cloud-integration  # AWS/Azure/GCP billing data

  labelMappingConfigs:
    enabled: true
    owner_label: "team"
    product_label: "product"
    department_label: "department"
    environment_label: "environment"

# Multi-cluster aggregation
kubecostAggregator:
  enabled: true

# Budget alerts
notifications:
  alertConfigs:
    enabled: true
    globalSlackWebhookUrl: ${SLACK_WEBHOOK}
    alerts:
      - type: budget
        threshold: 1000  # USD per day
        window: 1d
        aggregation: namespace
        filter: environment=prod
```

### Cost Allocation Queries

**Namespace cost breakdown:**
```bash
curl http://kubecost:9090/model/allocation \
  -d window=7d \
  -d aggregate=namespace
```

**Team cost allocation:**
```bash
curl http://kubecost:9090/model/allocation \
  -d window=month \
  -d aggregate=label:team
```

**Idle cost analysis:**
```bash
curl http://kubecost:9090/model/allocation \
  -d window=7d \
  -d idle=separate
```

---

## Cost Allocation Best Practices

### Label Strategy

**Required labels:**
```yaml
metadata:
  labels:
    team: backend            # Owning team
    product: api             # Product/service
    environment: production  # Environment
    cost-center: engineering # Finance cost center
```

**Enforcement (OPA/Gatekeeper):**
```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: RequireLabels
metadata:
  name: require-cost-labels
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment", "StatefulSet"]
  parameters:
    labels:
      - key: team
      - key: product
      - key: environment
```

### Showback vs. Chargeback

**Showback (informational):**
- Teams see their costs (no actual billing)
- Monthly cost reports via email/Slack
- Cost awareness without financial consequences

**Chargeback (actual billing):**
- Teams charged for their usage
- Costs deducted from team budgets
- Financial accountability (reduces waste)

**Implementation:**
```
1. Start with Showback (3-6 months)
2. Establish baseline costs per team
3. Set budgets based on historical usage
4. Transition to Chargeback (financial accountability)
```

### Cost Attribution Models

**Idle Cost Distribution:**
```
Option 1: Proportional (distribute idle cost by usage)
  ├── Team A uses 40% of cluster → pays 40% of idle cost
  └── Team B uses 60% of cluster → pays 60% of idle cost

Option 2: Share equally
  ├── Team A pays 50% of idle cost
  └── Team B pays 50% of idle cost

Option 3: Allocate to platform team
  └── Platform team pays 100% of idle cost (incentive to optimize)
```

**Recommendation:** Proportional distribution (fairest allocation).
