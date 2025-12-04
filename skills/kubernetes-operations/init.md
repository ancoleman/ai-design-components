# Kubernetes Operations Skill - Master Plan

**Skill Name:** `kubernetes-operations`
**Skill Level:** Mid Level (5,000-8,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Operations Taxonomy](#operations-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Multi-Language Implementations](#multi-language-implementations)
7. [Library and Tool Recommendations](#library-and-tool-recommendations)
8. [Skill Structure Design](#skill-structure-design)
9. [Integration Points](#integration-points)
10. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

Kubernetes has become the de facto standard for container orchestration in 2025. However, operating Kubernetes clusters effectively requires deep knowledge of resource management, networking, storage, security, and observability patterns. Most organizations struggle with:

- **Resource Optimization:** Over-provisioning (wasted costs) vs. under-provisioning (performance issues)
- **Complex Networking:** Service mesh integration, NetworkPolicies, Ingress controllers
- **Security Hardening:** RBAC misconfigurations, pod security, supply chain vulnerabilities
- **Autoscaling Complexity:** Balancing HPA, VPA, and cluster autoscaling
- **Troubleshooting Blind Spots:** Lack of systematic debugging approaches

**Market Drivers (2025):**
- **FinOps Integration:** Kubernetes cost optimization is now part of financial operations
- **Platform Engineering:** Internal developer platforms (IDPs) built on Kubernetes
- **AI Workload Shift:** LLM training and inference moving to Kubernetes (GPU scheduling)
- **Multi-Cluster Management:** Organizations running 10+ clusters across regions/clouds
- **GitOps Adoption:** Declarative infrastructure with Flux/ArgoCD as standard practice

**Strategic Value:**
1. **Universal Cloud-Native Foundation:** Powers AWS EKS, Google GKE, Azure AKS, and on-prem
2. **Cross-Cutting Operations:** Applies to all workloads (apps, databases, ML, batch jobs)
3. **Cost Impact:** Proper resource management can reduce cloud costs by 30-50%
4. **Security Critical:** Misconfigured Kubernetes is a primary attack vector
5. **Developer Productivity:** Well-configured clusters accelerate deployment velocity

### How This Differs from Existing Solutions

**Existing Kubernetes Documentation:**
- **Official Docs (kubernetes.io):** Comprehensive but overwhelming (6,932+ code snippets)
- **Vendor-Specific Guides:** Focused on managed offerings (EKS, GKE, AKS) - not portable
- **Blog Posts/Tutorials:** Tactical "how-to" without strategic decision frameworks
- **Books (e.g., Kubernetes Up & Running):** Breadth without depth in operations patterns

**Our Approach:**
- **Operations-First Framework:** When to use each pattern, not just how
- **Decision Trees:** Resource QoS, networking model selection, storage class choice
- **Multi-Language Tooling:** YAML manifests + Go operators + Python automation
- **Troubleshooting Playbooks:** Systematic debugging for common failure modes
- **Cost-Aware Patterns:** FinOps integration with every resource decision
- **2025 Best Practices:** Pod Security Standards, topology spread, KEDA, Gateway API

### Target Audience

**Primary Users:**
- Platform engineers managing internal Kubernetes platforms
- DevOps/SRE teams operating production clusters
- Backend developers deploying services to Kubernetes
- Cloud architects designing multi-cluster strategies

**Skill Level Assumptions:**
- Understands containers and basic Kubernetes concepts (Pod, Deployment, Service)
- Familiar with YAML manifest structure
- Knows basic kubectl commands (get, describe, logs)
- Needs guidance on advanced operations patterns

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **Resource Management Mastery**
   - CPU/memory requests and limits (right-sizing)
   - Quality of Service (QoS) classes: Guaranteed, Burstable, BestEffort
   - Resource quotas and LimitRanges for multi-tenancy
   - Vertical Pod Autoscaler (VPA) for automated right-sizing

2. **Advanced Scheduling Patterns**
   - Node affinity (required vs. preferred)
   - Taints and tolerations (workload isolation)
   - Topology spread constraints (zone/region distribution)
   - Pod priority and preemption (critical workloads)

3. **Networking Architecture**
   - NetworkPolicies for micro-segmentation
   - Ingress controllers (Nginx, Traefik, Gateway API)
   - Service types (ClusterIP, NodePort, LoadBalancer)
   - Service mesh integration patterns (Istio, Linkerd)

4. **Storage Operations**
   - PersistentVolume (PV) and PersistentVolumeClaim (PVC) lifecycle
   - StorageClasses for dynamic provisioning
   - Container Storage Interface (CSI) drivers
   - Volume snapshots and cloning

5. **Security Hardening**
   - RBAC (Roles, ClusterRoles, RoleBindings)
   - Pod Security Standards (Restricted, Baseline, Privileged)
   - Policy enforcement (OPA/Gatekeeper, Kyverno)
   - Secrets management (encryption at rest, external secrets)

6. **Autoscaling Strategies**
   - Horizontal Pod Autoscaler (HPA) - when and how
   - Vertical Pod Autoscaler (VPA) - use cases and limitations
   - Cluster Autoscaler - node pool management
   - KEDA (event-driven autoscaling) - beyond CPU/memory

7. **Troubleshooting Playbooks**
   - Pod startup failures (ImagePullBackOff, CrashLoopBackOff)
   - Resource exhaustion (CPU throttling, OOMKilled)
   - Networking issues (DNS resolution, NetworkPolicy blocks)
   - Storage problems (PVC pending, mount failures)

### What This Skill Does NOT Cover

**Out of Scope:**
- **Cluster Installation/Setup:** Covered by infrastructure-as-code skills (Terraform, etc.)
- **CI/CD Pipelines:** Covered by `building-ci-pipelines` skill
- **Application Development:** Focus is on operations, not app code
- **Service Mesh Deep Dive:** Brief coverage; full service mesh patterns need separate skill
- **Monitoring/Observability:** Covered by `observability` skill (Prometheus, Grafana, tracing)
- **GitOps Implementation:** Brief mention; full Flux/ArgoCD patterns elsewhere

### Success Criteria

**A user successfully uses this skill when they can:**
1. Right-size container resources to balance cost and performance
2. Configure advanced scheduling for high-availability workloads
3. Implement NetworkPolicies for zero-trust security
4. Design storage strategies for stateful applications
5. Apply RBAC following least-privilege principles
6. Set up autoscaling (HPA, VPA, cluster) appropriately
7. Systematically troubleshoot common Kubernetes issues

---

## Research Findings

### Research Date: December 3, 2025

**Research Tools Used:**
- Google Search Grounding (Vertex AI): Kubernetes best practices 2025
- Context7: /websites/kubernetes_io (6,932 snippets, 93.7 trust score)
- Official Kubernetes documentation (kubernetes.io)

### Key Trends for 2025

**1. FinOps Integration for Kubernetes**
- **Trend:** Kubernetes cost optimization is now a board-level concern
- **Tools:** Kubecost, OpenCost, Cloud provider native tools
- **Patterns:**
  - Real-time cost visibility per namespace/team/workload
  - Automated rightsizing based on actual usage (not guesses)
  - Showback/chargeback for multi-tenant clusters
- **Impact:** Resource requests/limits now tied to cost accountability

**2. Pod Security Standards (PSS) Adoption**
- **Trend:** Pod Security Policies (deprecated in 1.25) replaced by Pod Security Standards
- **Three Levels:**
  - **Restricted:** Most secure, removes all known privilege escalations
  - **Baseline:** Minimally restrictive, prevents known privilege escalations
  - **Privileged:** Unrestricted (for system-level workloads only)
- **Enforcement:** Admission controllers (built-in) + policy engines (OPA, Kyverno)
- **Impact:** Default-deny security posture is now standard

**3. Gateway API Replacing Ingress**
- **Trend:** Gateway API (networking.k8s.io/v1) is the future of L4/L7 routing
- **Advantages over Ingress:**
  - Role-oriented design (cluster operators vs. app developers)
  - More expressive (HTTPRoute, TCPRoute, TLSRoute)
  - Multi-namespace support
  - Vendor-neutral (Istio, Nginx, Envoy, Traefik all support it)
- **Status:** GA in Kubernetes 1.29+

**4. Event-Driven Autoscaling (KEDA)**
- **Trend:** CPU/memory HPA is insufficient for modern workloads
- **KEDA Scalers:** 50+ event sources (Kafka, RabbitMQ, AWS SQS, Prometheus, Cron)
- **Use Cases:**
  - Queue-based autoscaling (scale to zero when queue empty)
  - Schedule-based scaling (scale up before business hours)
  - Custom metrics from external systems
- **Adoption:** CNCF graduated project, widely used in production

**5. Topology Spread Constraints**
- **Trend:** Replacing older anti-affinity patterns
- **Purpose:** Even distribution across zones/regions/nodes
- **Advantages:**
  - More intuitive than podAntiAffinity
  - Better control over skew (max difference in pod counts)
  - Zone-aware scheduling for high availability
- **Impact:** Default HA pattern for critical workloads

**6. Automated Resource Rightsizing**
- **Trend:** Manual resource tuning is obsolete
- **Tools:** Vertical Pod Autoscaler (VPA), Goldilocks, StormForge
- **Patterns:**
  - VPA in "recommend" mode for visibility
  - Automated updates during deployment windows
  - Historical analysis for long-running workloads
- **Impact:** 30-50% cost reduction typical

**7. Multi-Cluster Management**
- **Trend:** Single cluster is an anti-pattern in 2025
- **Patterns:**
  - Regional clusters (US-East, EU-West, APAC)
  - Environment clusters (Dev, Staging, Prod)
  - Workload-specific clusters (ML training, batch jobs)
- **Tools:** Cluster API, Crossplane, Fleet management (Rancher, etc.)
- **Challenges:** Cross-cluster service discovery, unified observability

### Best Practices Summary (2025)

**Resource Management:**
- ✅ Always set CPU/memory requests and limits
- ✅ Use VPA for automated rightsizing
- ✅ Implement resource quotas per namespace
- ✅ Monitor actual usage vs. requests (cost optimization)
- ❌ Don't over-provision "just to be safe"

**Scheduling:**
- ✅ Use topology spread constraints for HA
- ✅ Apply taints for workload isolation (GPU nodes, spot instances)
- ✅ Set pod priority for critical workloads
- ✅ Use node affinity for special hardware (SSD, NVME)
- ❌ Don't rely on default scheduler for complex requirements

**Networking:**
- ✅ Implement NetworkPolicies (default deny ingress/egress)
- ✅ Use Gateway API for new applications
- ✅ Apply rate limiting at ingress layer
- ✅ Enable mTLS for sensitive workloads (service mesh)
- ❌ Don't expose services publicly without authentication

**Storage:**
- ✅ Use CSI drivers (not legacy in-tree provisioners)
- ✅ Define StorageClasses per performance tier
- ✅ Enable volume snapshots for stateful apps
- ✅ Set appropriate reclaim policies (Retain vs. Delete)
- ❌ Don't use hostPath in production

**Security:**
- ✅ Enforce Pod Security Standards (Restricted for apps)
- ✅ Implement RBAC with least privilege
- ✅ Use policy engines (Kyverno/OPA) for guardrails
- ✅ Scan images for vulnerabilities (Trivy, Grype)
- ✅ Encrypt secrets at rest
- ❌ Don't run containers as root
- ❌ Don't mount service account tokens unless needed

**Autoscaling:**
- ✅ Use HPA for stateless workloads (web servers, APIs)
- ✅ Use KEDA for event-driven workloads (queue processors)
- ✅ Enable cluster autoscaler with appropriate limits
- ✅ Set PodDisruptionBudgets to prevent over-disruption
- ❌ Don't use VPA + HPA on the same metric (conflicts)

---

## Operations Taxonomy

### Resource Management

#### Tier 1: Resource Requests and Limits

**Purpose:** Define CPU and memory guarantees and boundaries for containers

**Concepts:**
- **Requests:** Minimum guaranteed resources (used for scheduling)
- **Limits:** Maximum allowed resources (enforced by kubelet)
- **QoS Classes:**
  - **Guaranteed:** requests == limits (highest priority, never killed unless exceeds limits)
  - **Burstable:** requests < limits (medium priority, can burst, killed if node pressure)
  - **BestEffort:** no requests/limits (lowest priority, first to be evicted)

**Decision Framework:**

| Workload Type | Requests | Limits | QoS | Rationale |
|---------------|----------|--------|-----|-----------|
| **Critical Services** | High | Same as requests | Guaranteed | Predictable performance, never evicted |
| **Web Servers** | Moderate | 1.5-2x requests | Burstable | Handle traffic spikes, cost-effective |
| **Batch Jobs** | Low | 2-3x requests | Burstable | Use spare capacity, tolerate variability |
| **Development** | Low | None | BestEffort | Cost savings, non-critical |

**YAML Example (Guaranteed QoS):**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: critical-app
spec:
  containers:
  - name: app
    image: myapp:latest
    resources:
      requests:
        memory: "512Mi"
        cpu: "500m"      # 0.5 CPU cores
      limits:
        memory: "512Mi"  # Same as request = Guaranteed QoS
        cpu: "500m"
```

**YAML Example (Burstable QoS):**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-server
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m"      # 0.25 CPU cores
      limits:
        memory: "512Mi"  # 2x request = can burst
        cpu: "500m"      # 2x request = can burst
```

---

#### Tier 2: Resource Quotas and LimitRanges

**Purpose:** Enforce multi-tenancy and prevent resource monopolization

**ResourceQuota (Namespace-Level Limits):**
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-quota
  namespace: team-alpha
spec:
  hard:
    requests.cpu: "10"        # Max 10 CPU cores requested
    requests.memory: "20Gi"   # Max 20GB memory requested
    limits.cpu: "20"          # Max 20 CPU cores limit
    limits.memory: "40Gi"     # Max 40GB memory limit
    persistentvolumeclaims: "10"  # Max 10 PVCs
    pods: "50"                # Max 50 pods
```

**LimitRange (Default Constraints per Container):**
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: team-alpha
spec:
  limits:
  - max:
      memory: "2Gi"
      cpu: "2"
    min:
      memory: "128Mi"
      cpu: "100m"
    default:
      memory: "512Mi"  # Applied if no limit specified
      cpu: "500m"
    defaultRequest:
      memory: "256Mi"  # Applied if no request specified
      cpu: "250m"
    type: Container
```

---

#### Tier 3: Vertical Pod Autoscaler (VPA)

**Purpose:** Automated CPU/memory right-sizing based on actual usage

**VPA Modes:**
- **Off:** Recommendations only (safe starting point)
- **Initial:** Set requests on pod creation
- **Recreate:** Update running pods (causes restart)
- **Auto:** Update requests automatically (future mode)

**VPA YAML Example:**
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
    updateMode: "Recreate"  # Or "Off" for recommendations only
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
```

**When to Use VPA:**
- ✅ Stateless applications with predictable patterns
- ✅ Long-running services (collect 7+ days of metrics)
- ✅ Applications where restarts are acceptable
- ❌ Don't use VPA + HPA on same metric (conflicts)
- ❌ Avoid for stateful apps requiring stable resources

---

### Scheduling Patterns

#### Tier 1: Node Affinity

**Purpose:** Control which nodes pods can be scheduled on

**Types:**
- **requiredDuringSchedulingIgnoredDuringExecution:** Hard constraint (pod won't schedule if not met)
- **preferredDuringSchedulingIgnoredDuringExecution:** Soft constraint (scheduler tries but not guaranteed)

**Node Affinity YAML:**
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
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        preference:
          matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values:
            - us-west-2a  # Prefer this zone (cost savings)
  containers:
  - name: ml-training
    image: pytorch:latest
```

---

#### Tier 2: Taints and Tolerations

**Purpose:** Reserve nodes for specific workloads (inverse of affinity)

**Concept:**
- **Taint:** Applied to nodes (repels pods)
- **Toleration:** Applied to pods (allows scheduling on tainted nodes)

**Common Taint Effects:**
- **NoSchedule:** New pods won't schedule (existing pods stay)
- **PreferNoSchedule:** Avoid scheduling but not strict
- **NoExecute:** Evict existing pods (immediate effect)

**Taint Node (kubectl):**
```bash
# Taint GPU nodes to prevent non-GPU workloads
kubectl taint nodes gpu-node-1 workload=gpu:NoSchedule

# Taint spot instances (may be terminated)
kubectl taint nodes spot-node-1 instance-type=spot:NoSchedule
```

**Toleration YAML:**
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
  containers:
  - name: ml-training
    image: pytorch:latest
    resources:
      limits:
        nvidia.com/gpu: 1  # Request 1 GPU
```

---

#### Tier 3: Topology Spread Constraints

**Purpose:** Even distribution across failure domains (zones, nodes, regions)

**Topology Spread YAML:**
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
        topologyKey: topology.kubernetes.io/zone  # Spread across zones
        whenUnsatisfiable: DoNotSchedule  # Hard constraint
        labelSelector:
          matchLabels:
            app: critical-app
      - maxSkew: 2
        topologyKey: kubernetes.io/hostname  # Spread across nodes
        whenUnsatisfiable: ScheduleAnyway   # Soft constraint
        labelSelector:
          matchLabels:
            app: critical-app
      containers:
      - name: app
        image: myapp:latest
```

**Result:** 9 replicas spread evenly across 3 zones (3 per zone), further spread across nodes within zones.

---

### Networking

#### Tier 1: NetworkPolicies (Micro-Segmentation)

**Purpose:** Control traffic flow between pods (default-deny security)

**Default Deny All Traffic:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}  # Applies to all pods in namespace
  policyTypes:
  - Ingress
  - Egress
```

**Allow Specific Ingress (Frontend → Backend):**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-allow-frontend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend  # Only frontend pods allowed
    ports:
    - protocol: TCP
      port: 8080
```

**Allow Egress to External API:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-external-api
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 203.0.113.0/24  # External API CIDR
    ports:
    - protocol: TCP
      port: 443
  - to:  # Allow DNS resolution
    - namespaceSelector:
        matchLabels:
          name: kube-system
    - podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
```

---

#### Tier 2: Ingress and Gateway API

**Ingress (Legacy, Still Widely Used):**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend
            port:
              number: 8080
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```

**Gateway API (Modern, Recommended for New Apps):**
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: production-gateway
spec:
  gatewayClassName: nginx
  listeners:
  - name: https
    protocol: HTTPS
    port: 443
    tls:
      certificateRefs:
      - name: myapp-tls
    allowedRoutes:
      namespaces:
        from: Same
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: app-routes
spec:
  parentRefs:
  - name: production-gateway
  hostnames:
  - myapp.example.com
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /api
    backendRefs:
    - name: backend
      port: 8080
  - matches:
    - path:
        type: PathPrefix
        value: /
    backendRefs:
    - name: frontend
      port: 80
```

---

### Storage

#### Tier 1: StorageClasses

**Purpose:** Define storage tiers (performance, cost, durability)

**AWS EBS StorageClass (SSD):**
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: ebs.csi.aws.com
parameters:
  type: gp3              # General Purpose SSD v3
  iopsPerGB: "50"
  throughput: "1000"     # MB/s
  encrypted: "true"
  kmsKeyId: "arn:aws:kms:us-east-1:123456789:key/..."
volumeBindingMode: WaitForFirstConsumer  # Topology-aware
allowVolumeExpansion: true
reclaimPolicy: Delete
```

**NFS StorageClass (Shared Storage):**
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: shared-nfs
provisioner: nfs.csi.k8s.io
parameters:
  server: nfs-server.example.com
  share: /exports/kubernetes
mountOptions:
  - hard
  - nfsvers=4.1
volumeBindingMode: Immediate
reclaimPolicy: Retain  # Keep data after PVC deletion
```

---

#### Tier 2: PersistentVolumeClaims

**Purpose:** Request storage for pods

**PVC YAML:**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-data
spec:
  storageClassName: fast-ssd
  accessModes:
  - ReadWriteOnce  # Single node access
  resources:
    requests:
      storage: 50Gi
```

**Using PVC in Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: postgres-data
```

---

### Security

#### Tier 1: RBAC (Role-Based Access Control)

**Purpose:** Define who can do what in the cluster

**Role (Namespace-Scoped):**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch"]
```

**ClusterRole (Cluster-Wide):**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-admin
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list", "watch", "update", "patch"]
```

**RoleBinding (Assign Role to User):**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: production
subjects:
- kind: User
  name: jane@example.com
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

**ServiceAccount with Limited Permissions:**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app-sa
  namespace: production
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: configmap-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-configmap-access
  namespace: production
subjects:
- kind: ServiceAccount
  name: my-app-sa
  namespace: production
roleRef:
  kind: Role
  name: configmap-reader
  apiGroup: rbac.authorization.k8s.io
```

---

#### Tier 2: Pod Security Standards

**Purpose:** Enforce secure pod configurations

**Namespace Labels (Enable PSS):**
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

**Restricted Pod Example (Most Secure):**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
  namespace: production
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: myapp:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
    volumeMounts:
    - name: tmp
      mountPath: /tmp
  volumes:
  - name: tmp
    emptyDir: {}
```

---

#### Tier 3: Policy Enforcement (Kyverno)

**Purpose:** Automated policy enforcement (alternative to OPA/Gatekeeper)

**Kyverno Policy (Require Resource Limits):**
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resources
spec:
  validationFailureAction: enforce
  background: true
  rules:
  - name: check-resources
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "CPU and memory resource requests and limits are required"
      pattern:
        spec:
          containers:
          - resources:
              requests:
                memory: "?*"
                cpu: "?*"
              limits:
                memory: "?*"
                cpu: "?*"
```

**Kyverno Policy (Block Latest Tag):**
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-latest-tag
spec:
  validationFailureAction: enforce
  rules:
  - name: require-image-tag
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Using 'latest' image tag is not allowed"
      pattern:
        spec:
          containers:
          - image: "!*:latest"
```

---

### Autoscaling

#### Tier 1: Horizontal Pod Autoscaler (HPA)

**Purpose:** Scale pod replicas based on metrics

**HPA v2 (CPU and Memory):**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
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

---

#### Tier 2: KEDA (Event-Driven Autoscaling)

**Purpose:** Scale based on events (queue depth, cron schedules, etc.)

**KEDA ScaledObject (RabbitMQ Queue):**
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: rabbitmq-scaler
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

**KEDA ScaledObject (Prometheus Metric):**
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
      query: sum(rate(http_requests_total[2m]))
      threshold: "100"  # Scale when >100 req/sec
```

**KEDA ScaledObject (Cron Schedule):**
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

---

### Troubleshooting Playbooks

#### Playbook 1: Pod Stuck in Pending

**Symptoms:**
```bash
$ kubectl get pods
NAME                     READY   STATUS    RESTARTS   AGE
my-app-6d5f8b9c4-xz7k2   0/1     Pending   0          5m
```

**Diagnosis Steps:**
```bash
# 1. Check pod events
kubectl describe pod my-app-6d5f8b9c4-xz7k2

# Common causes and solutions:

# A. Insufficient CPU/memory
# Event: "0/3 nodes are available: 3 Insufficient cpu."
# Solution: Reduce resource requests or add nodes

# B. No nodes matching affinity
# Event: "0/3 nodes are available: 3 node(s) didn't match node selector."
# Solution: Fix nodeSelector or add matching labels to nodes

# C. PVC not bound
# Event: "persistentvolumeclaim "data" not found"
# Solution: Create PVC or fix PVC name

# D. No nodes with toleration
# Event: "0/3 nodes are available: 3 node(s) had taints that the pod didn't tolerate."
# Solution: Add toleration or remove taint
```

---

#### Playbook 2: CrashLoopBackOff

**Symptoms:**
```bash
$ kubectl get pods
NAME                     READY   STATUS             RESTARTS   AGE
my-app-6d5f8b9c4-abc12   0/1     CrashLoopBackOff   5          3m
```

**Diagnosis Steps:**
```bash
# 1. Check container logs
kubectl logs my-app-6d5f8b9c4-abc12

# 2. Check previous container logs (if restarted)
kubectl logs my-app-6d5f8b9c4-abc12 --previous

# 3. Check events
kubectl describe pod my-app-6d5f8b9c4-abc12

# Common causes:

# A. Application crash on startup
# Solution: Fix application code or configuration

# B. Missing environment variables
# Solution: Add required env vars to deployment

# C. Liveness probe failing too quickly
# Solution: Increase initialDelaySeconds or fix probe

# D. OOMKilled (out of memory)
# Event: "Container killed: OOMKilled"
# Solution: Increase memory limit or fix memory leak
```

---

#### Playbook 3: ImagePullBackOff

**Symptoms:**
```bash
$ kubectl get pods
NAME                     READY   STATUS              RESTARTS   AGE
my-app-6d5f8b9c4-def34   0/1     ImagePullBackOff    0          2m
```

**Diagnosis Steps:**
```bash
# 1. Check events
kubectl describe pod my-app-6d5f8b9c4-def34

# Common causes:

# A. Image doesn't exist
# Event: "Failed to pull image: manifest unknown"
# Solution: Fix image name/tag

# B. Authentication required
# Event: "Failed to pull image: unauthorized"
# Solution: Create imagePullSecrets

# Example: Create Docker registry secret
kubectl create secret docker-registry regcred \
  --docker-server=myregistry.azurecr.io \
  --docker-username=myuser \
  --docker-password=mypassword \
  --docker-email=myemail@example.com

# Add to deployment:
spec:
  imagePullSecrets:
  - name: regcred
  containers:
  - name: app
    image: myregistry.azurecr.io/myapp:v1.0

# C. Network issues pulling image
# Solution: Check network policies, firewall rules
```

---

#### Playbook 4: Service Not Accessible

**Symptoms:**
```bash
# Service exists but can't connect
$ kubectl get svc
NAME      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
my-app    ClusterIP   10.96.100.50    <none>        80/TCP    5m

$ curl http://10.96.100.50
curl: (7) Failed to connect to 10.96.100.50 port 80: Connection refused
```

**Diagnosis Steps:**
```bash
# 1. Check if pods are running
kubectl get pods -l app=my-app

# 2. Check endpoints (should list pod IPs)
kubectl get endpoints my-app

# If endpoints are empty:
# - Service selector doesn't match pod labels
# - Pods aren't ready (readiness probe failing)

# 3. Check service selector matches pod labels
kubectl get svc my-app -o yaml | grep -A5 selector
kubectl get pods -l app=my-app -o wide

# 4. Test from within cluster
kubectl run test --rm -it --image=busybox -- wget -O- http://my-app

# 5. Check NetworkPolicies blocking traffic
kubectl get networkpolicies -n <namespace>
kubectl describe networkpolicy <policy-name>

# 6. For LoadBalancer services, check external-IP
kubectl get svc my-app
# If EXTERNAL-IP is <pending>, check cloud controller logs
```

---

## Decision Frameworks

### Framework 1: Which Resource QoS Class?

**Decision Tree:**

```
START: Selecting QoS class for workload

Q1: Is this a critical production service?
  ├─ YES → Q2
  └─ NO  → Q3

Q2: Can you tolerate ANY performance variability?
  ├─ YES → Burstable (requests < limits)
  └─ NO  → Guaranteed (requests == limits)

Q3: Is this a batch/background job?
  ├─ YES → Burstable (low requests, high limits)
  └─ NO  → Q4

Q4: Is this a development/testing environment?
  ├─ YES → BestEffort (no requests/limits)
  └─ NO  → Burstable (cost-effective default)
```

**Examples:**

| Workload | QoS | Configuration |
|----------|-----|---------------|
| Payment API | Guaranteed | requests: 1 CPU / 2Gi, limits: 1 CPU / 2Gi |
| Web Frontend | Burstable | requests: 500m / 512Mi, limits: 1 CPU / 1Gi |
| Batch ETL | Burstable | requests: 100m / 256Mi, limits: 2 CPU / 4Gi |
| Dev Environment | BestEffort | No requests/limits |

---

### Framework 2: When to Use HPA vs. VPA vs. Cluster Autoscaler?

**Decision Matrix:**

| Scenario | Use HPA | Use VPA | Use Cluster Autoscaler |
|----------|---------|---------|------------------------|
| Stateless web app with traffic spikes | ✅ Yes | ❌ No | Maybe (if nodes full) |
| Stateful database (single instance) | ❌ No | ✅ Yes | Maybe (if node undersized) |
| Queue processor (event-driven) | ✅ KEDA | ❌ No | Maybe |
| Pods pending due to insufficient resources | ❌ No | ❌ No | ✅ Yes |
| CPU/memory requests too high/low | ❌ No | ✅ Yes | ❌ No |

**HPA Decision:**
- ✅ Stateless workloads
- ✅ Can scale horizontally (>1 replica)
- ✅ Traffic/load varies over time
- ❌ Stateful apps requiring stable identity

**VPA Decision:**
- ✅ Single-instance or limited replicas
- ✅ Resource requests need tuning
- ✅ Can tolerate pod restarts
- ❌ Running with HPA on same metric

**Cluster Autoscaler Decision:**
- ✅ Pods pending due to insufficient nodes
- ✅ Node utilization varies (scale down when idle)
- ✅ Cost optimization important
- ❌ All workloads are critical (might not scale up fast enough)

---

### Framework 3: Which Networking Pattern?

**Decision Tree:**

```
START: Exposing application

Q1: Is this internal or external access?
  ├─ INTERNAL → Q2
  └─ EXTERNAL → Q3

Q2: Which pods need access?
  ├─ Same namespace → ClusterIP Service + NetworkPolicy
  ├─ Multiple namespaces → ClusterIP Service + cross-namespace NetworkPolicy
  └─ All pods → ClusterIP Service (no NetworkPolicy)

Q3: What protocol?
  ├─ HTTP/HTTPS → Q4
  └─ TCP/UDP → LoadBalancer Service

Q4: Do you need advanced routing (path-based, headers, etc.)?
  ├─ YES → Gateway API (or Ingress if legacy)
  └─ NO  → LoadBalancer Service (simpler)
```

**Examples:**

| Use Case | Pattern |
|----------|---------|
| Database (only backend pods need access) | ClusterIP + NetworkPolicy |
| Internal API (cross-namespace) | ClusterIP + cross-namespace NetworkPolicy |
| Public website | Gateway API (HTTPRoute) |
| gRPC API (external) | LoadBalancer Service (TCP) |

---

### Framework 4: Which Storage Class?

**Decision Matrix:**

| Workload | Performance | Durability | Access Mode | Storage Class |
|----------|-------------|------------|-------------|---------------|
| Database | High | High | ReadWriteOnce | SSD (gp3/io2) |
| Shared files | Medium | High | ReadWriteMany | NFS/EFS |
| Logs (temp) | Low | Low | ReadWriteOnce | Standard HDD |
| ML models | High | Medium | ReadOnlyMany | Object storage (S3) |

**Access Modes:**
- **ReadWriteOnce (RWO):** Single node can mount read-write (most common)
- **ReadOnlyMany (ROX):** Multiple nodes can mount read-only
- **ReadWriteMany (RWX):** Multiple nodes can mount read-write (requires network storage)

---

## Multi-Language Implementations

### YAML (Declarative Manifests)

**Primary Use:** All Kubernetes resources are defined in YAML

**Best Practices:**
- ✅ Use `---` separator for multi-resource files
- ✅ Include namespace in metadata (avoid default)
- ✅ Add labels for all resources (app, version, component)
- ✅ Use kustomize or Helm for templating
- ❌ Don't hardcode environment-specific values

---

### Go (Kubernetes Operators)

**Purpose:** Extend Kubernetes API with custom controllers

**When to Use Go:**
- Building custom operators (CRDs + controllers)
- Advanced reconciliation logic
- Performance-critical controllers
- Native Kubernetes client library

**Example: Simple Controller (Pseudocode):**
```go
package main

import (
    "context"
    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/tools/cache"
    "k8s.io/client-go/informers"
)

func main() {
    clientset := kubernetes.NewForConfig(config)

    // Watch for Deployment changes
    factory := informers.NewSharedInformerFactory(clientset, 0)
    informer := factory.Apps().V1().Deployments().Informer()

    informer.AddEventHandler(cache.ResourceEventHandlerFuncs{
        AddFunc: func(obj interface{}) {
            // Handle new Deployment
        },
        UpdateFunc: func(old, new interface{}) {
            // Handle Deployment update
        },
        DeleteFunc: func(obj interface{}) {
            // Handle Deployment deletion
        },
    })

    informer.Run(context.Background().Done())
}
```

**Tools:**
- **Kubebuilder:** Scaffolding for operators
- **Operator SDK:** Alternative framework
- **client-go:** Official Kubernetes Go client

---

### Python (Automation and Tooling)

**Purpose:** Cluster automation, reporting, custom tooling

**When to Use Python:**
- Custom automation scripts
- Kubernetes resource reporting (cost, usage)
- Integration with external systems
- Rapid prototyping

**Example: List Pods Without Resource Limits:**
```python
from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()

pods = v1.list_pod_for_all_namespaces()
missing_limits = []

for pod in pods.items:
    for container in pod.spec.containers:
        if not container.resources.limits:
            missing_limits.append({
                'namespace': pod.metadata.namespace,
                'pod': pod.metadata.name,
                'container': container.name
            })

print(f"Found {len(missing_limits)} containers without resource limits:")
for item in missing_limits:
    print(f"  {item['namespace']}/{item['pod']}/{item['container']}")
```

**Tools:**
- **kubernetes-python:** Official Python client
- **kubectl-python:** Higher-level wrapper
- **kopf:** Python framework for operators

---

## Library and Tool Recommendations

### Research Summary

**Research Date:** December 3, 2025
**Libraries Evaluated:** 10+
**Research Tools:** Google Search Grounding (Vertex AI), Context7

---

### Core: Kubernetes

**Library:** `/websites/kubernetes_io`
**Trust Score:** 93.7/100
**Code Snippets:** 6,932+
**Source Reputation:** High

**Why Kubernetes Official Docs?**
- **Authoritative Source:** CNCF-maintained, community-driven
- **Comprehensive Coverage:** All API versions, resources, concepts
- **Code Examples:** 6,932+ YAML snippets and examples
- **Up-to-Date:** Tracks latest versions (1.29+)

**Installation (kubectl CLI):**
```bash
# macOS
brew install kubectl

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Windows
choco install kubernetes-cli
```

**Verify Version:**
```bash
kubectl version --client
```

---

### Autoscaling: KEDA (Event-Driven)

**Project:** KEDA (Kubernetes Event-Driven Autoscaling)
**Status:** CNCF Graduated Project (2025)
**Why KEDA?**
- **50+ Event Sources:** Kafka, RabbitMQ, AWS SQS, Prometheus, Cron, and more
- **Scale to Zero:** Cost savings for idle workloads
- **HPA-Compatible:** Works alongside native HPA
- **Production-Ready:** Used by Microsoft, Red Hat, SAP

**Installation (Helm):**
```bash
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
helm install keda kedacore/keda --namespace keda --create-namespace
```

**When to Use:**
- ✅ Queue-based autoscaling (RabbitMQ, Kafka, SQS)
- ✅ Schedule-based scaling (cron patterns)
- ✅ External metrics (Prometheus, Datadog)
- ✅ Scale-to-zero scenarios

---

### Policy Enforcement: Kyverno

**Project:** Kyverno
**Status:** CNCF Incubating Project
**Why Kyverno?**
- **Native Kubernetes:** No custom language (uses YAML)
- **Easier than OPA:** Less learning curve than Rego
- **Validate, Mutate, Generate:** Comprehensive policy actions
- **CLI Tool:** Test policies locally

**Installation (Helm):**
```bash
helm repo add kyverno https://kyverno.github.io/kyverno/
helm install kyverno kyverno/kyverno --namespace kyverno --create-namespace
```

**When to Use:**
- ✅ Enforce resource limits on all pods
- ✅ Block latest image tag
- ✅ Auto-generate NetworkPolicies
- ✅ Add labels/annotations to resources

**Alternative: OPA Gatekeeper**
- More powerful (Rego language)
- Steeper learning curve
- Better for complex policies

---

### Monitoring: Metrics Server

**Library:** `/kubernetes-sigs/metrics-server`
**Trust Score:** 61.8/100
**Code Snippets:** 32+
**Why Metrics Server?**
- **HPA Requirement:** Required for Horizontal Pod Autoscaler
- **Resource Metrics:** CPU/memory usage per pod
- **Lightweight:** Low overhead

**Installation (Manifest):**
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

**Verify:**
```bash
kubectl top nodes
kubectl top pods -A
```

---

### GitOps: Flux (Brief Mention)

**Why Flux?**
- **CNCF Graduated Project**
- **GitOps Standard:** Sync Git → Cluster
- **Helm/Kustomize Support**

**Note:** Full GitOps patterns covered in separate skill. Kubernetes-operations focuses on runtime operations.

---

## Skill Structure Design

### Skill File Organization

**Proposed Structure:**

```
kubernetes-operations/
├── SKILL.md                          # Main skill file (<500 lines)
├── references/
│   ├── resource-management.md        # Deep dive: Requests, limits, QoS, VPA
│   ├── scheduling-patterns.md        # Deep dive: Affinity, taints, topology spread
│   ├── networking.md                 # Deep dive: NetworkPolicies, Gateway API
│   ├── storage.md                    # Deep dive: StorageClasses, CSI, PVCs
│   ├── security.md                   # Deep dive: RBAC, PSS, secrets, policies
│   ├── autoscaling.md                # Deep dive: HPA, VPA, KEDA, cluster autoscaler
│   └── troubleshooting.md            # Playbooks for common issues
├── examples/
│   ├── manifests/
│   │   ├── qos-guaranteed.yaml       # Guaranteed QoS pod
│   │   ├── qos-burstable.yaml        # Burstable QoS pod
│   │   ├── networkpolicy-default-deny.yaml
│   │   ├── networkpolicy-allow-frontend.yaml
│   │   ├── hpa-cpu-memory.yaml       # HPA with CPU and memory
│   │   ├── keda-rabbitmq.yaml        # KEDA RabbitMQ scaler
│   │   ├── storageclass-ssd.yaml     # AWS EBS SSD
│   │   ├── rbac-least-privilege.yaml # RBAC example
│   │   └── pod-security-restricted.yaml
│   ├── python/
│   │   ├── list_pods_without_limits.py
│   │   ├── generate_cost_report.py
│   │   └── validate_rbac.py
│   └── go/
│       └── simple-operator/          # Basic operator example
└── scripts/
    ├── validate-resources.sh         # Check all pods have requests/limits
    ├── audit-networkpolicies.sh      # Find namespaces without NetworkPolicies
    └── cost-analysis.sh              # Resource cost breakdown
```

---

### SKILL.md Structure (Main File)

**Sections (Target: ~450-500 lines):**

1. **Frontmatter** (YAML)
   - name, description

2. **Purpose** (2-3 paragraphs)
   - What this skill teaches
   - When to use this skill

3. **Quick Start: Resource Management** (~80 lines)
   - Requests and limits overview
   - QoS classes (Guaranteed, Burstable, BestEffort)
   - Quick decision tree
   - Link to references/resource-management.md

4. **Quick Start: Scheduling** (~60 lines)
   - Node affinity basics
   - Taints and tolerations
   - Topology spread
   - Link to references/scheduling-patterns.md

5. **Quick Start: Networking** (~60 lines)
   - NetworkPolicy patterns
   - Ingress vs. Gateway API
   - Link to references/networking.md

6. **Quick Start: Storage** (~50 lines)
   - StorageClass selection
   - PVC lifecycle
   - Link to references/storage.md

7. **Quick Start: Security** (~60 lines)
   - RBAC essentials
   - Pod Security Standards
   - Link to references/security.md

8. **Quick Start: Autoscaling** (~60 lines)
   - HPA vs. VPA vs. Cluster Autoscaler
   - KEDA introduction
   - Link to references/autoscaling.md

9. **Troubleshooting** (~40 lines)
   - Common issues overview
   - Link to references/troubleshooting.md

10. **Reference Links** (~20 lines)
    - Links to all references/ files
    - Links to examples/

---

### Progressive Disclosure Strategy

**Main SKILL.md Contains:**
- High-level decision frameworks
- Quick reference patterns
- When to use each approach
- Links to detailed references

**References/ Contains:**
- Deep dives into each topic
- Comprehensive YAML examples
- Advanced patterns
- Edge cases and considerations

**Examples/ Contains:**
- Copy-paste ready YAML manifests
- Working Python scripts
- Go operator skeleton

**Scripts/ Contains:**
- Validation scripts (executable)
- Audit scripts
- Cost analysis tools

---

## Integration Points

### Integration with Existing Skills

#### 1. **building-ci-pipelines** Skill
- **Connection:** Deploy to Kubernetes from CI/CD
- **Patterns:**
  - kubectl apply in GitHub Actions
  - Helm chart deployment
  - GitOps with Flux/ArgoCD

**Example Integration (.github/workflows/deploy.yml):**
```yaml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG }}

      - name: Deploy application
        run: |
          kubectl apply -f k8s/namespace.yaml
          kubectl apply -f k8s/deployment.yaml
          kubectl apply -f k8s/service.yaml
          kubectl rollout status deployment/my-app -n production
```

---

#### 2. **observability** Skill
- **Connection:** Monitor Kubernetes clusters and workloads
- **Patterns:**
  - Prometheus for metrics (HPA, resource usage)
  - Grafana dashboards for Kubernetes
  - Tracing distributed workloads

**Metrics to Monitor:**
- Node CPU/memory utilization
- Pod restart count
- HPA scaling events
- PVC storage usage
- NetworkPolicy denied connections

---

#### 3. **secret-management** Skill
- **Connection:** Secure secrets in Kubernetes
- **Patterns:**
  - External Secrets Operator (AWS Secrets Manager, Vault)
  - Sealed Secrets (encrypted at rest in Git)
  - SOPS (encrypt YAML files)

**Example: External Secrets Operator:**
```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets
    kind: SecretStore
  target:
    name: db-secret
  data:
  - secretKey: password
    remoteRef:
      key: production/postgres/password
```

---

#### 4. **testing-strategies** Skill
- **Connection:** Test Kubernetes manifests and deployments
- **Patterns:**
  - Kubeval (validate YAML syntax)
  - Conftest (policy testing with OPA)
  - Kind (local Kubernetes for integration tests)

**Example: Test NetworkPolicy:**
```bash
# Validate YAML syntax
kubeval manifests/networkpolicy.yaml

# Test policy with OPA
conftest test manifests/networkpolicy.yaml -p policies/

# Integration test in Kind cluster
kind create cluster --config kind-config.yaml
kubectl apply -f manifests/
# Run connectivity tests
kubectl run test --rm -it --image=busybox -- wget -O- http://service
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)

**Deliverables:**
- [x] Complete init.md (this document)
- [ ] Create SKILL.md main file
- [ ] Write references/resource-management.md
- [ ] Write examples/manifests/qos-*.yaml

**Content Focus:**
- Resource requests and limits
- QoS classes
- Decision framework

---

### Phase 2: Scheduling and Networking (Week 2)

**Deliverables:**
- [ ] Write references/scheduling-patterns.md
- [ ] Write references/networking.md
- [ ] Create NetworkPolicy examples
- [ ] Create affinity/taint examples

---

### Phase 3: Storage and Security (Week 3)

**Deliverables:**
- [ ] Write references/storage.md
- [ ] Write references/security.md
- [ ] Create StorageClass examples
- [ ] Create RBAC examples
- [ ] Create Pod Security Standards examples

---

### Phase 4: Autoscaling (Week 4)

**Deliverables:**
- [ ] Write references/autoscaling.md
- [ ] Create HPA examples
- [ ] Create KEDA examples
- [ ] Document VPA patterns

---

### Phase 5: Troubleshooting and Tooling (Week 5)

**Deliverables:**
- [ ] Write references/troubleshooting.md
- [ ] Create Python automation scripts
- [ ] Create validation/audit scripts
- [ ] Document common debugging patterns

---

### Phase 6: Integration and Polish (Week 6)

**Deliverables:**
- [ ] Cross-link with related skills
- [ ] Create Go operator example
- [ ] Test all examples
- [ ] Final review and validation

---

## Validation Checklist

### Before Creating SKILL.md

- [x] Research complete (Google Search + Context7)
- [x] Library recommendations validated
- [x] Decision frameworks designed
- [x] YAML examples identified
- [x] Integration points mapped

### Before Finalizing Skill

- [ ] SKILL.md under 500 lines
- [ ] All references/ files created
- [ ] All examples/ tested in live cluster
- [ ] Progressive disclosure effective
- [ ] Cross-language consistency validated
- [ ] Integration with related skills verified

---

## Success Metrics

**This skill is successful if operators can:**

1. **Resource Optimization:**
   - Right-size container resources (reduce costs by 30%+)
   - Choose appropriate QoS classes
   - Implement resource quotas for multi-tenancy

2. **High Availability:**
   - Configure topology spread for zone distribution
   - Use taints for workload isolation
   - Implement pod priority for critical workloads

3. **Security Hardening:**
   - Apply RBAC with least privilege
   - Enforce Pod Security Standards
   - Implement NetworkPolicies for zero-trust

4. **Effective Autoscaling:**
   - Configure HPA for stateless apps
   - Use KEDA for event-driven workloads
   - Enable cluster autoscaler appropriately

5. **Rapid Troubleshooting:**
   - Diagnose pod startup failures in <5 minutes
   - Identify resource exhaustion issues
   - Debug networking problems systematically

---

## Future Enhancements

**Potential Additions (Not in Initial Release):**

1. **Multi-Cluster Patterns**
   - Cluster API
   - Federation v2
   - Cross-cluster service discovery

2. **Advanced Networking**
   - Service mesh deep dive (Istio, Linkerd)
   - Cilium eBPF networking
   - Multi-cluster networking

3. **Stateful Workloads**
   - StatefulSet patterns
   - Operators for databases (Postgres, MySQL)
   - Data replication and backups

4. **GPU Scheduling**
   - GPU resource management
   - Time-slicing GPUs
   - Multi-instance GPU (MIG)

5. **Cost Optimization**
   - Kubecost integration
   - Spot instance patterns
   - Resource rightsizing automation

---

## Appendix: Library Comparison Matrix

### Kubernetes Tooling

| Tool | Purpose | Trust | Best For |
|------|---------|-------|----------|
| **kubectl** | CLI for Kubernetes | Official | All operations |
| **Helm** | Package manager | CNCF | Application deployment |
| **Kustomize** | YAML templating | CNCF | Manifest customization |
| **KEDA** | Event-driven autoscaling | CNCF Graduated | Scale-to-zero, queues |
| **Kyverno** | Policy enforcement | CNCF Incubating | Simpler than OPA |
| **OPA Gatekeeper** | Policy enforcement | CNCF Graduated | Complex policies |
| **Metrics Server** | Resource metrics | CNCF | HPA requirement |

---

## References

**Research Sources:**
- Google Search Grounding (Vertex AI): Kubernetes best practices 2025
- Context7 Documentation: /websites/kubernetes_io (6,932 snippets, 93.7 trust)
- Official Kubernetes documentation: kubernetes.io
- CNCF Landscape: cncf.io/projects

**Related Skills:**
- `building-ci-pipelines` - Deploy to Kubernetes from CI/CD
- `observability` - Monitor clusters and workloads
- `secret-management` - Secure secrets in Kubernetes
- `testing-strategies` - Test manifests and deployments

---

**Document Status:** ✅ Complete
**Next Step:** Create SKILL.md from this master plan
**Owner:** AI Design Components Project
**Last Updated:** December 3, 2025
