# Resource Management

## Table of Contents

1. [Resource Requests and Limits](#resource-requests-and-limits)
2. [Quality of Service Classes](#quality-of-service-classes)
3. [Resource Quotas](#resource-quotas)
4. [LimitRanges](#limitranges)
5. [Vertical Pod Autoscaler](#vertical-pod-autoscaler)
6. [Cost Optimization Patterns](#cost-optimization-patterns)

## Resource Requests and Limits

### CPU Resources

**CPU Units:**
- **1 CPU** = 1 vCPU/core on cloud provider
- **1000m** (millicores) = 1 CPU
- **100m** = 0.1 CPU (10% of one core)

**CPU Requests:**
- Minimum guaranteed CPU for scheduling
- Scheduler finds nodes with available CPU
- Pod can use more than request (up to limit)

**CPU Limits:**
- Maximum CPU pod can use
- Enforced by throttling (CFS quota)
- Pod slowed down, not killed

**Example:**
```yaml
resources:
  requests:
    cpu: "500m"     # Guaranteed 0.5 cores
  limits:
    cpu: "1"        # Max 1 core (can burst 2x)
```

### Memory Resources

**Memory Units:**
- **Ki/Mi/Gi** (binary, 1024-based): 1Ki = 1024 bytes, 1Mi = 1048576 bytes
- **k/M/G** (decimal, 1000-based): 1k = 1000 bytes
- Use binary units (Ki/Mi/Gi) for consistency

**Memory Requests:**
- Minimum guaranteed memory for scheduling
- Pod evicted if exceeds request under node pressure

**Memory Limits:**
- Maximum memory pod can allocate
- Pod killed (OOMKilled) if exceeds limit
- No throttling like CPU

**Example:**
```yaml
resources:
  requests:
    memory: "512Mi"   # Guaranteed 512MB
  limits:
    memory: "1Gi"     # Max 1GB (OOMKilled if exceeded)
```

### Compressible vs. Incompressible Resources

**Compressible (CPU):**
- Can be throttled without killing pod
- Degraded performance, but pod survives
- Safer to overcommit

**Incompressible (Memory):**
- Cannot be reclaimed once allocated
- Pod killed if exceeds limit or under pressure
- Must be carefully sized

## Quality of Service Classes

Kubernetes assigns QoS classes automatically based on requests and limits:

### Guaranteed QoS

**Criteria:**
- Every container has CPU and memory requests
- Every container has CPU and memory limits
- Requests equal limits for both CPU and memory

**Behavior:**
- Highest priority
- Never evicted unless exceeding limits
- Predictable performance
- Most expensive (can't overcommit)

**Example:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: guaranteed-pod
spec:
  containers:
  - name: app
    image: myapp:latest
    resources:
      requests:
        memory: "512Mi"
        cpu: "500m"
      limits:
        memory: "512Mi"  # Same as request
        cpu: "500m"      # Same as request
```

**Use Cases:**
- Critical production services (payments, auth)
- Databases requiring stable performance
- Real-time processing systems
- Compliance-required workloads

### Burstable QoS

**Criteria:**
- At least one container has CPU or memory request
- Requests less than limits (or only requests set)

**Behavior:**
- Medium priority
- Can burst above requests (use spare capacity)
- Evicted under node pressure (after BestEffort)
- Cost-effective balance

**Example:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: burstable-pod
spec:
  containers:
  - name: app
    image: myapp:latest
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m"
      limits:
        memory: "512Mi"  # 2x request (can burst)
        cpu: "500m"      # 2x request
```

**Use Cases:**
- Web servers (handle traffic spikes)
- API services (most common pattern)
- Batch jobs (use spare capacity)
- Non-critical background workers

### BestEffort QoS

**Criteria:**
- No requests or limits set for any container

**Behavior:**
- Lowest priority
- First to be evicted under node pressure
- No resource guarantees
- Most cost-effective

**Example:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: besteffort-pod
spec:
  containers:
  - name: app
    image: myapp:latest
    # No resources specified
```

**Use Cases:**
- Development environments
- Testing workloads
- Experimental services
- Low-priority batch jobs

### QoS Selection Decision Tree

```
START: Which QoS class for my workload?

Q1: Is this a critical production service?
  ├─ YES → Can you tolerate ANY performance variability?
  │   ├─ YES → Burstable (cost-effective)
  │   └─ NO  → Guaranteed (predictable)
  └─ NO  → Is this production at all?
      ├─ YES → Burstable (default for most apps)
      └─ NO  → BestEffort (dev/test only)
```

## Resource Quotas

### Namespace-Level Limits

ResourceQuotas enforce limits at the namespace level for multi-tenancy:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-quota
  namespace: team-alpha
spec:
  hard:
    # Compute resources
    requests.cpu: "10"        # Max 10 CPU cores requested
    requests.memory: "20Gi"   # Max 20GB memory requested
    limits.cpu: "20"          # Max 20 CPU cores limit
    limits.memory: "40Gi"     # Max 40GB memory limit

    # Storage
    persistentvolumeclaims: "10"
    requests.storage: "100Gi"

    # Object counts
    pods: "50"
    services: "10"
    secrets: "20"
    configmaps: "20"
```

### Quota Scopes

Apply quotas to specific pod classes:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: best-effort-quota
  namespace: team-alpha
spec:
  hard:
    pods: "5"  # Max 5 BestEffort pods
  scopes:
  - BestEffort
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: high-priority-quota
  namespace: team-alpha
spec:
  hard:
    requests.cpu: "20"
    requests.memory: "40Gi"
  scopeSelector:
    matchExpressions:
    - operator: In
      scopeName: PriorityClass
      values: ["high"]
```

### Checking Quota Usage

```bash
# View quota details
kubectl describe resourcequota -n team-alpha

# Example output:
# Name:            team-quota
# Namespace:       team-alpha
# Resource         Used   Hard
# --------         ----   ----
# requests.cpu     8      10
# requests.memory  15Gi   20Gi
# pods             35     50
```

## LimitRanges

### Default Constraints per Container

LimitRanges set defaults and boundaries for individual containers:

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: team-alpha
spec:
  limits:
  - max:
      memory: "2Gi"    # No container can exceed 2GB
      cpu: "2"         # No container can exceed 2 cores
    min:
      memory: "128Mi"  # All containers must request at least 128MB
      cpu: "100m"      # All containers must request at least 0.1 cores
    default:
      memory: "512Mi"  # Applied if no limit specified
      cpu: "500m"
    defaultRequest:
      memory: "256Mi"  # Applied if no request specified
      cpu: "250m"
    maxLimitRequestRatio:
      memory: "2"      # Limit can't exceed 2x request
      cpu: "2"
    type: Container
```

### LimitRange for PVCs

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: storage-limits
  namespace: team-alpha
spec:
  limits:
  - max:
      storage: "50Gi"
    min:
      storage: "1Gi"
    type: PersistentVolumeClaim
```

### LimitRange Behavior

**When pod is created:**
1. If no request set → apply `defaultRequest`
2. If no limit set → apply `default`
3. Validate against `min` and `max`
4. Validate `maxLimitRequestRatio`
5. Reject pod if violations found

## Vertical Pod Autoscaler

### VPA Modes

**Off (Recommendations Only):**
- Safest starting point
- VPA calculates recommendations
- No automatic changes
- View recommendations: `kubectl describe vpa`

**Initial:**
- Apply recommendations only on pod creation
- Existing pods unchanged
- Useful for StatefulSets

**Recreate:**
- Update running pods (causes restart)
- Evicts and recreates pods with new resources
- Not suitable for single-replica workloads

**Auto (Future):**
- Update requests in-place without restart
- Not yet available in production

### VPA Configuration

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
    updateMode: "Off"  # Start with recommendations only

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
      mode: "Auto"  # Per-container override
```

### VPA Recommendations

View VPA recommendations:

```bash
kubectl describe vpa my-app-vpa

# Output includes:
# Recommendation:
#   Container Recommendations:
#     Container Name:  app
#     Lower Bound:     (minimum for cost efficiency)
#       Cpu:     250m
#       Memory:  256Mi
#     Target:          (recommended values)
#       Cpu:     500m
#       Memory:  512Mi
#     Upper Bound:     (maximum safe values)
#       Cpu:     1
#       Memory:  1Gi
```

### VPA Best Practices

**When to Use VPA:**
- ✅ Stateless applications with predictable patterns
- ✅ Long-running services (collect 7+ days of metrics)
- ✅ Applications where restarts are acceptable
- ✅ Unknown resource requirements (let VPA learn)

**When to Avoid VPA:**
- ❌ Running with HPA on same metric (conflicts)
- ❌ Stateful apps requiring stable resources
- ❌ Single-replica critical workloads
- ❌ Short-lived jobs (insufficient data)

**VPA + HPA Compatibility:**
- ✅ VPA on CPU/memory + HPA on custom metric
- ✅ VPA off mode (recommendations) + HPA on any metric
- ❌ VPA auto mode + HPA on same metric (CPU/memory)

### VPA Installation

```bash
# Install VPA (Helm)
helm repo add fairwinds-stable https://charts.fairwinds.com/stable
helm install vpa fairwinds-stable/vpa --namespace vpa --create-namespace

# Or via manifest
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler
./hack/vpa-up.sh
```

## Cost Optimization Patterns

### Right-Sizing Workflow

**Phase 1: Baseline (Week 1)**
1. Deploy with conservative requests (overestimate)
2. Set higher limits (allow bursting)
3. Monitor actual usage

```yaml
# Initial deployment (conservative)
resources:
  requests:
    cpu: "500m"
    memory: "512Mi"
  limits:
    cpu: "2"
    memory: "2Gi"
```

**Phase 2: Observation (Week 2-4)**
1. Deploy VPA in "Off" mode
2. Collect 2-4 weeks of usage data
3. Review VPA recommendations
4. Check Prometheus/metrics for actual usage

```bash
# View actual usage
kubectl top pods -n production

# View VPA recommendations
kubectl describe vpa my-app-vpa
```

**Phase 3: Optimization (Week 5+)**
1. Apply VPA recommendations
2. Monitor for OOMKilled or CPU throttling
3. Adjust based on real behavior
4. Iterate quarterly

```yaml
# Optimized resources (based on VPA)
resources:
  requests:
    cpu: "250m"      # Reduced from 500m
    memory: "256Mi"  # Reduced from 512Mi
  limits:
    cpu: "500m"      # Tighter than initial 2
    memory: "512Mi"  # Tighter than initial 2Gi
```

### Cost Monitoring

```bash
# Audit pods without resource limits
kubectl get pods --all-namespaces -o json | \
  jq -r '.items[] | select(.spec.containers[].resources.limits == null) | .metadata.name'

# Calculate namespace cost (requests)
kubectl get pods -n production -o json | \
  jq -r '.items[].spec.containers[] |
    (.resources.requests.cpu // "0") + " " +
    (.resources.requests.memory // "0")'
```

### Cost Allocation Tags

Label resources for cost allocation:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  labels:
    app: my-app
    team: backend          # Cost center
    env: production        # Environment
    cost-center: "12345"   # Finance tracking
spec:
  containers:
  - name: app
    image: myapp:latest
```

### Savings Estimates

**Typical Cost Reductions:**
- **Overprovisioned CPU:** 40-60% reduction
- **Overprovisioned Memory:** 30-50% reduction
- **BestEffort → Burstable:** No cost change (same requests)
- **Burstable → Guaranteed:** Cost increase (tighter limits)

**Example Calculation:**
- **Before:** 100 pods × 2 CPU × 4 GB = 200 cores, 400GB
- **After VPA:** 100 pods × 0.5 CPU × 2 GB = 50 cores, 200GB
- **Savings:** 75% CPU, 50% memory = ~60% total cost

### Resource Waste Detection

```python
# Python script: detect overprovisioned pods
from kubernetes import client, config

config.load_kube_config()
metrics = client.CustomObjectsApi()
v1 = client.CoreV1Api()

# Get pod metrics
metrics_data = metrics.list_cluster_custom_object(
    "metrics.k8s.io", "v1beta1", "pods"
)

for pod in metrics_data["items"]:
    for container in pod["containers"]:
        usage_cpu = container["usage"]["cpu"]
        usage_mem = container["usage"]["memory"]

        # Compare to requests
        pod_obj = v1.read_namespaced_pod(
            pod["metadata"]["name"],
            pod["metadata"]["namespace"]
        )

        for c in pod_obj.spec.containers:
            if c.resources.requests:
                req_cpu = c.resources.requests.get("cpu")
                req_mem = c.resources.requests.get("memory")

                # Flag if usage < 20% of request
                # (potential waste)
```

## Monitoring and Alerts

### Key Metrics to Track

**Per-Pod:**
- `container_cpu_usage_seconds_total` - Actual CPU usage
- `container_memory_working_set_bytes` - Actual memory usage
- `kube_pod_container_resource_requests` - Configured requests
- `kube_pod_container_resource_limits` - Configured limits

**Per-Node:**
- `kube_node_status_allocatable` - Available resources
- `kube_node_status_capacity` - Total capacity
- Node CPU/memory utilization

### Prometheus Queries

```promql
# CPU throttling (pods hitting limits)
rate(container_cpu_cfs_throttled_seconds_total[5m]) > 0.1

# Memory usage vs. limit
container_memory_working_set_bytes / container_spec_memory_limit_bytes > 0.9

# Pods without requests
kube_pod_container_resource_requests{resource="memory"} == 0

# Node CPU pressure
(1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m]))) > 0.8
```

### Recommended Alerts

```yaml
# Alert: Pod OOMKilled
- alert: PodOOMKilled
  expr: increase(kube_pod_container_status_terminated_reason{reason="OOMKilled"}[5m]) > 0
  annotations:
    summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} was OOMKilled"

# Alert: High CPU throttling
- alert: HighCPUThrottling
  expr: rate(container_cpu_cfs_throttled_seconds_total[5m]) > 0.2
  annotations:
    summary: "Pod {{ $labels.pod }} is CPU throttled >20%"

# Alert: No resource limits
- alert: MissingResourceLimits
  expr: kube_pod_container_resource_limits{resource="memory"} == 0
  annotations:
    summary: "Pod {{ $labels.pod }} has no memory limit"
```

## Summary

**Key Takeaways:**
1. Always set requests and limits to enable QoS
2. Use Guaranteed QoS for critical services
3. Use Burstable QoS for most applications
4. Implement ResourceQuotas for multi-tenancy
5. Use VPA for automated rightsizing
6. Monitor actual usage vs. requests
7. Iterate on resource sizing quarterly
8. Label resources for cost allocation
