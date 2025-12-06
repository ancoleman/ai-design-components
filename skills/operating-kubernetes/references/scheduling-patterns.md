# Scheduling Patterns

## Table of Contents

1. [Node Affinity](#node-affinity)
2. [Taints and Tolerations](#taints-and-tolerations)
3. [Topology Spread Constraints](#topology-spread-constraints)
4. [Pod Priority and Preemption](#pod-priority-and-preemption)
5. [Pod Affinity and Anti-Affinity](#pod-affinity-and-anti-affinity)
6. [Scheduling Decision Framework](#scheduling-decision-framework)

## Node Affinity

### Required Node Affinity (Hard Constraint)

Pod will not schedule unless node matches criteria:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-workload
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: node.kubernetes.io/instance-type
            operator: In
            values:
            - g4dn.xlarge   # AWS GPU instance
            - g4dn.2xlarge
          - key: topology.kubernetes.io/zone
            operator: In
            values:
            - us-west-2a
            - us-west-2b
  containers:
  - name: ml-training
    image: pytorch:latest
    resources:
      limits:
        nvidia.com/gpu: 1
```

### Preferred Node Affinity (Soft Constraint)

Scheduler tries to match but will schedule anyway if no match:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: cache-service
spec:
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100  # Highest preference
        preference:
          matchExpressions:
          - key: node.kubernetes.io/instance-type
            operator: In
            values:
            - r5.xlarge  # Prefer memory-optimized
      - weight: 50   # Lower preference
        preference:
          matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values:
            - us-west-2a  # Prefer this zone (cost savings)
  containers:
  - name: redis
    image: redis:7
```

### Node Affinity Operators

| Operator | Behavior |
|----------|----------|
| `In` | Label value in list |
| `NotIn` | Label value not in list |
| `Exists` | Label key exists (any value) |
| `DoesNotExist` | Label key doesn't exist |
| `Gt` | Label value greater than (numeric) |
| `Lt` | Label value less than (numeric) |

### Common Node Labels

```bash
# Built-in labels
kubernetes.io/hostname=node-1
kubernetes.io/os=linux
kubernetes.io/arch=amd64
node.kubernetes.io/instance-type=m5.xlarge
topology.kubernetes.io/zone=us-west-2a
topology.kubernetes.io/region=us-west-2

# Custom labels
kubectl label nodes node-1 workload=gpu
kubectl label nodes node-2 storage=ssd
kubectl label nodes node-3 team=backend
```

### Use Cases

**GPU Scheduling:**
```yaml
# Require GPU nodes
requiredDuringSchedulingIgnoredDuringExecution:
  nodeSelectorTerms:
  - matchExpressions:
    - key: accelerator
      operator: In
      values:
      - nvidia-tesla-v100
```

**SSD Storage:**
```yaml
# Prefer SSD nodes for databases
preferredDuringSchedulingIgnoredDuringExecution:
- weight: 100
  preference:
    matchExpressions:
    - key: storage
      operator: In
      values:
      - ssd
```

**Cost Optimization:**
```yaml
# Prefer spot instances (non-critical workloads)
preferredDuringSchedulingIgnoredDuringExecution:
- weight: 100
  preference:
    matchExpressions:
    - key: node.kubernetes.io/instance-lifecycle
      operator: In
      values:
      - spot
```

## Taints and Tolerations

### Taint Effects

**NoSchedule:**
- New pods won't schedule
- Existing pods remain

**PreferNoSchedule:**
- Scheduler tries to avoid
- Will schedule if no other options

**NoExecute:**
- Evict existing pods immediately
- New pods won't schedule

### Applying Taints

```bash
# Taint GPU nodes
kubectl taint nodes gpu-node-1 workload=gpu:NoSchedule

# Taint spot instances (may be terminated)
kubectl taint nodes spot-node-1 instance-type=spot:NoSchedule

# Taint nodes for maintenance
kubectl taint nodes node-1 maintenance=true:NoExecute

# Remove taint
kubectl taint nodes node-1 maintenance-
```

### Pod Tolerations

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod
spec:
  tolerations:
  - key: "workload"
    operator: "Equal"
    value: "gpu"
    effect: "NoSchedule"
  - key: "instance-type"
    operator: "Equal"
    value: "spot"
    effect: "NoSchedule"
  containers:
  - name: ml-training
    image: pytorch:latest
```

### Toleration Operators

**Equal:**
```yaml
tolerations:
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoSchedule"
```

**Exists:**
```yaml
# Tolerate any value for key1
tolerations:
- key: "key1"
  operator: "Exists"
  effect: "NoSchedule"
```

**Wildcard:**
```yaml
# Tolerate all taints
tolerations:
- operator: "Exists"
```

### Toleration with Timeout

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: fault-tolerant-app
spec:
  tolerations:
  - key: "node.kubernetes.io/unreachable"
    operator: "Exists"
    effect: "NoExecute"
    tolerationSeconds: 300  # Wait 5min before eviction
  - key: "node.kubernetes.io/not-ready"
    operator: "Exists"
    effect: "NoExecute"
    tolerationSeconds: 300
  containers:
  - name: app
    image: myapp:latest
```

### Common Taint Use Cases

**Dedicated Nodes for Team:**
```bash
# Taint nodes for team-alpha only
kubectl taint nodes node-1 node-2 node-3 team=alpha:NoSchedule

# Team-alpha pods tolerate
tolerations:
- key: "team"
  operator: "Equal"
  value: "alpha"
  effect: "NoSchedule"
```

**Isolate System Workloads:**
```bash
# Taint nodes for system components only
kubectl taint nodes master-1 node-role.kubernetes.io/master:NoSchedule
```

**Handle Hardware Failures:**
```bash
# Taint nodes with disk issues
kubectl taint nodes node-1 disk=failing:NoExecute
```

## Topology Spread Constraints

### Even Distribution Across Zones

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: critical-app
spec:
  replicas: 9
  selector:
    matchLabels:
      app: critical-app
  template:
    metadata:
      labels:
        app: critical-app
    spec:
      topologySpreadConstraints:
      - maxSkew: 1              # Max difference in pod count
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule  # Hard constraint
        labelSelector:
          matchLabels:
            app: critical-app
      containers:
      - name: app
        image: myapp:latest
```

**Result:** 9 replicas spread evenly across 3 zones (3 per zone)

### Multi-Level Spreading

```yaml
topologySpreadConstraints:
# Level 1: Spread across zones (hard)
- maxSkew: 1
  topologyKey: topology.kubernetes.io/zone
  whenUnsatisfiable: DoNotSchedule
  labelSelector:
    matchLabels:
      app: critical-app

# Level 2: Spread across nodes within zones (soft)
- maxSkew: 2
  topologyKey: kubernetes.io/hostname
  whenUnsatisfiable: ScheduleAnyway
  labelSelector:
    matchLabels:
      app: critical-app
```

### maxSkew Behavior

**maxSkew: 1 (Strict)**
- Zone A: 3 pods
- Zone B: 3 pods
- Zone C: 3 pods
- Cannot add pod to Zone A until B and C catch up

**maxSkew: 2 (Relaxed)**
- Zone A: 4 pods
- Zone B: 3 pods
- Zone C: 2 pods
- Max difference is 2 (4-2=2)

### whenUnsatisfiable

**DoNotSchedule (Hard):**
- Pod remains Pending if constraint violated
- Strict high-availability requirement

**ScheduleAnyway (Soft):**
- Scheduler tries to satisfy but schedules anyway
- Preference, not requirement

### minDomains

```yaml
topologySpreadConstraints:
- maxSkew: 1
  topologyKey: topology.kubernetes.io/zone
  whenUnsatisfiable: DoNotSchedule
  labelSelector:
    matchLabels:
      app: critical-app
  minDomains: 3  # Require at least 3 zones
```

### Topology Spread vs. Pod Anti-Affinity

**Topology Spread (Modern):**
- More intuitive (maxSkew semantics)
- Better control over distribution
- Recommended for new applications

**Pod Anti-Affinity (Legacy):**
- More complex configuration
- Less flexible
- Still widely used

**Migration Example:**

```yaml
# Old: Pod anti-affinity
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchLabels:
            app: myapp
        topologyKey: kubernetes.io/hostname

# New: Topology spread
topologySpreadConstraints:
- maxSkew: 1
  topologyKey: kubernetes.io/hostname
  whenUnsatisfiable: ScheduleAnyway
  labelSelector:
    matchLabels:
      app: myapp
```

## Pod Priority and Preemption

### Priority Classes

```yaml
# High priority for critical services
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
globalDefault: false
description: "Critical production services"
---
# Medium priority (default)
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: medium-priority
value: 500000
globalDefault: true
description: "Standard production workloads"
---
# Low priority for batch jobs
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority
value: 100000
globalDefault: false
description: "Batch jobs and background tasks"
```

### Using Priority Classes

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: critical-api
spec:
  priorityClassName: high-priority
  containers:
  - name: api
    image: api:latest
```

### Preemption Behavior

**When node resources exhausted:**
1. Scheduler tries to find node for high-priority pod
2. If no node available, scheduler looks for preemption candidates
3. Lower-priority pods evicted to make room
4. High-priority pod scheduled

**Preemption Example:**
- Node capacity: 4 CPU cores
- Running: 2 medium-priority pods (2 cores each)
- Pending: 1 high-priority pod (2 cores)
- Result: 1 medium-priority pod evicted, high-priority scheduled

### PodDisruptionBudget (Protect from Preemption)

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-pdb
spec:
  minAvailable: 2  # Keep at least 2 replicas running
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
  maxUnavailable: 1  # Max 1 pod disrupted at a time
  selector:
    matchLabels:
      app: api
```

### Priority Use Cases

**Critical Services:**
```yaml
# Payment API - highest priority
priorityClassName: high-priority
value: 1000000
```

**Standard Applications:**
```yaml
# Web frontend - medium priority
priorityClassName: medium-priority
value: 500000
```

**Batch Jobs:**
```yaml
# ETL jobs - low priority (preemptible)
priorityClassName: low-priority
value: 100000
```

**Development:**
```yaml
# Dev environments - lowest priority
priorityClassName: dev-priority
value: 0
```

## Pod Affinity and Anti-Affinity

### Pod Affinity (Co-locate Pods)

Schedule pods on same node or zone as other pods:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-frontend
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchLabels:
            app: cache
        topologyKey: kubernetes.io/hostname  # Same node
  containers:
  - name: frontend
    image: frontend:latest
```

**Use Case:** Co-locate frontend with cache for low latency

### Pod Anti-Affinity (Spread Pods)

Schedule pods away from other pods:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: api-pod
  labels:
    app: api
spec:
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchLabels:
            app: api
        topologyKey: kubernetes.io/hostname  # Different nodes
  containers:
  - name: api
    image: api:latest
```

**Use Case:** Spread API replicas across nodes for high availability

### Preferred Anti-Affinity

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 5
  template:
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: web-app
              topologyKey: topology.kubernetes.io/zone  # Prefer different zones
          - weight: 50
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: web-app
              topologyKey: kubernetes.io/hostname  # Then different nodes
```

## Scheduling Decision Framework

### Decision Tree

```
START: How should I schedule this workload?

Q1: Does it need special hardware?
  ├─ YES → Use Node Affinity (GPU, SSD, etc.)
  └─ NO  → Q2

Q2: Should it be isolated from other workloads?
  ├─ YES → Use Taints + Tolerations
  └─ NO  → Q3

Q3: Does it need high availability?
  ├─ YES → Use Topology Spread Constraints
  └─ NO  → Q4

Q4: Is it more critical than other workloads?
  ├─ YES → Use Priority Class
  └─ NO  → Default scheduling
```

### Pattern Combinations

**High-Availability API:**
```yaml
spec:
  # 1. Topology spread (even distribution)
  topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: api

  # 2. High priority
  priorityClassName: high-priority

  # 3. PodDisruptionBudget
  # (separate resource)
```

**ML Training Job:**
```yaml
spec:
  # 1. Node affinity (GPU nodes)
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: accelerator
            operator: In
            values:
            - nvidia-tesla-v100

  # 2. Toleration (GPU taints)
  tolerations:
  - key: workload
    operator: Equal
    value: gpu
    effect: NoSchedule

  # 3. Low priority (preemptible)
  priorityClassName: low-priority
```

**Cost-Optimized Batch Job:**
```yaml
spec:
  # 1. Prefer spot instances
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        preference:
          matchExpressions:
          - key: node.kubernetes.io/instance-lifecycle
            operator: In
            values:
            - spot

  # 2. Tolerate spot interruptions
  tolerations:
  - key: instance-type
    operator: Equal
    value: spot
    effect: NoSchedule

  # 3. Lowest priority
  priorityClassName: batch-priority
```

## Summary

**Scheduling Pattern Selection:**

| Use Case | Pattern | Example |
|----------|---------|---------|
| GPU workloads | Node Affinity (required) | ML training, video encoding |
| Isolated workloads | Taints + Tolerations | GPU nodes, spot instances |
| High availability | Topology Spread | Critical APIs, databases |
| Cost optimization | Node Affinity (preferred) | Spot instances, cheaper zones |
| Critical services | Priority Class | Payment API, auth services |
| Low latency | Pod Affinity | Frontend + cache co-location |
| Fault tolerance | Pod Anti-Affinity | Spread replicas |

**Best Practices:**
1. Use topology spread over pod anti-affinity
2. Combine node affinity with taints for isolation
3. Set PodDisruptionBudgets with priority classes
4. Test scheduling constraints in dev/staging
5. Monitor pod Pending events
6. Use preferred constraints when possible (more flexible)
