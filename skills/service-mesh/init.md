# Service Mesh - Master Plan

**Skill Name:** `service-mesh`
**Level:** Mid Level (5,000-8,000 tokens, 500-800 lines)
**Status:** Planning Phase - Research Complete
**Date:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Service Mesh Taxonomy](#service-mesh-taxonomy)
5. [Decision Framework](#decision-framework)
6. [Istio Patterns](#istio-patterns)
7. [Linkerd Patterns](#linkerd-patterns)
8. [Cilium Patterns](#cilium-patterns)
9. [Security Patterns](#security-patterns)
10. [Progressive Delivery](#progressive-delivery)
11. [Tool Recommendations](#tool-recommendations)
12. [Skill Structure Design](#skill-structure-design)
13. [Integration Points](#integration-points)
14. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why Service Mesh Matters

Service meshes have become foundational infrastructure for cloud-native applications in 2025:

**Key Value Propositions:**
- **Zero-Trust Security:** Automatic mTLS, identity-based authorization, defense in depth
- **Traffic Control:** Advanced routing, retries, circuit breaking, progressive rollouts
- **Observability:** Distributed tracing, metrics, traffic visibility without code changes
- **Resilience:** Timeout management, fault injection, request hedging
- **Compliance:** Centralized policy enforcement, audit trails, encryption at rest/transit

**Market Landscape (2025):**
- **Istio:** Enterprise standard, feature-rich, ambient mode (sidecar-less) now stable
- **Linkerd:** Lightweight, Rust-based, simplicity-focused, low latency overhead
- **Cilium:** eBPF-native, kernel-level performance, sidecar-less by design

### Strategic Differentiation

**This skill focuses on:**
1. **Architecture decisions** - Sidecar vs sidecar-less (ambient/eBPF)
2. **Security-first patterns** - mTLS, authorization policies, zero-trust
3. **Progressive delivery** - Traffic splitting, canary deployments, blue/green
4. **Production patterns** - Real-world YAML configurations, not toy examples
5. **Multi-cluster scenarios** - Cross-cluster communication, mesh federation

**Not covered (see other skills):**
- Kubernetes basics → `kubernetes-operations`
- Load balancing algorithms → `load-balancing-patterns`
- Network architecture → `network-architecture`
- Container security → `security-hardening`

### Skill Positioning in DevOps Stack

```
Infrastructure Stack:
┌─────────────────────────────────────┐
│   Application Code (Your Services)  │
├─────────────────────────────────────┤
│   Service Mesh (This Skill)         │ ← Traffic, Security, Observability
├─────────────────────────────────────┤
│   Kubernetes (kubernetes-ops)       │ ← Orchestration
├─────────────────────────────────────┤
│   Container Runtime (security-hard) │ ← Isolation
├─────────────────────────────────────┤
│   Infrastructure (IaC)               │ ← Provisioning
└─────────────────────────────────────┘
```

---

## Skill Purpose and Scope

### Purpose

Guide implementation of production-ready service mesh deployments across Istio, Linkerd, and Cilium, with emphasis on security, traffic management, and observability patterns. Provide decision frameworks for architecture choices (sidecar vs sidecar-less) and concrete YAML configurations for common scenarios.

### When to Use This Skill

**Trigger Phrases:**
- "Set up service mesh with mTLS"
- "Configure Istio traffic routing"
- "Implement canary deployments"
- "Secure microservices communication"
- "Add authorization policies"
- "Traffic splitting between versions"
- "Multi-cluster service mesh"
- "Ambient mode vs sidecar"
- "Circuit breaker configuration"
- "Distributed tracing setup"

### Scope Boundaries

**✅ In Scope:**
- Service mesh architecture decisions (Istio/Linkerd/Cilium)
- Sidecar vs sidecar-less patterns (ambient mode, eBPF)
- mTLS configuration and certificate management
- Authorization policies and zero-trust security
- Traffic management (routing, retries, timeouts, circuit breaking)
- Progressive rollouts (canary, blue/green, A/B testing)
- Observability integration (Prometheus, Jaeger, Grafana)
- Multi-cluster mesh federation
- Gateway configuration (ingress/egress)
- Service discovery and DNS

**❌ Out of Scope:**
- Kubernetes cluster setup (see `kubernetes-operations`)
- Container image security (see `security-hardening`)
- Load balancer provisioning (see `load-balancing-patterns`)
- CI/CD pipeline setup (see `building-ci-pipelines`)
- Infrastructure provisioning (see `infrastructure-as-code`)
- Application code instrumentation

---

## Research Findings

### Research Methodology

**Tools Used:**
- Google Search Grounding (Vertex AI, max_results: 8)
- Context7 Library Documentation (Istio, Linkerd, Cilium)

**Queries Executed:**
1. "service mesh comparison 2025 Istio Linkerd Cilium architecture mTLS"
2. "Istio traffic management virtual service destination rule 2025 patterns"
3. "service mesh mTLS authorization policies security 2025 best practices"

### Key Findings Summary

#### 1. Service Mesh Comparison (2025)

**Istio:**
- **Architecture:** Control plane (Istiod) + Data plane (Envoy sidecars or ambient ztunnel)
- **Maturity:** Production-proven, enterprise-grade
- **Performance:** 166% latency increase with sidecar mTLS, **8% with ambient mode**
- **Ambient Mode:** Now stable, L4 ztunnel + optional L7 waypoint proxies
- **Best For:** Feature-rich requirements, enterprise compliance, multi-cloud
- **Context7:** 7,796 code snippets, Trust Score: High (91/100)

**Linkerd:**
- **Architecture:** Control plane + Rust-based micro-proxies (linkerd2-proxy)
- **Maturity:** Production-ready, simplicity-focused
- **Performance:** 33% latency increase with mTLS (lowest sidecar overhead)
- **Best For:** Small-medium teams, simplicity, low resource consumption
- **Context7:** 2,457 code snippets, Trust Score: High

**Cilium:**
- **Architecture:** eBPF-based, sidecar-less by design
- **Maturity:** Growing adoption, eBPF-native networking
- **Performance:** 99% latency increase with mTLS (eBPF overhead vs sidecar)
- **Best For:** Kernel-level performance, advanced networking, future-proof eBPF
- **Context7:** 4,511 code snippets, Trust Score: High (83.5/100)

#### 2. Architecture Trends (2025)

**Sidecar-less is Growing:**
- **Istio Ambient Mode:** L4 security via ztunnel (per-node), L7 via waypoint (optional)
- **Cilium:** Native sidecar-less using eBPF in kernel
- **Performance:** Ambient mode reduces latency from 166% to 8% (Istio benchmark)
- **Resource Efficiency:** No sidecar = lower CPU/memory per pod

**When to Use Sidecar vs Sidecar-less:**
- **Sidecar:** Per-pod isolation, fine-grained L7 control, legacy compatibility
- **Sidecar-less:** Lower overhead, simpler operations, kernel-level performance

#### 3. Security Best Practices (2025)

**Zero-Trust Architecture:**
- Never trust, always verify every request
- Default-deny authorization policies
- Identity-based access control (not IP-based)
- Micro-segmentation at service level

**mTLS Configuration:**
- **Automatic mTLS:** Service mesh handles cert lifecycle
- **Strict mode:** Reject plaintext connections (vs permissive mode)
- **Certificate rotation:** Automate with cert-manager or mesh CA
- **SPIFFE/SPIRE:** Industry standard for workload identity

**Authorization Policies:**
- **Least privilege:** Grant minimum required permissions
- **Granular policies:** Namespace, workload, route-level controls
- **Mesh-wide defaults:** Start with deny-all, add allow rules
- **Audit logging:** Track policy violations and access patterns

#### 4. Traffic Management Patterns (2025)

**Istio Patterns:**
- **VirtualService:** L7 routing rules (path, headers, weights)
- **DestinationRule:** Traffic policies (connection pools, circuit breakers, TLS)
- **Gateway:** Ingress/egress configuration
- **ServiceEntry:** External service integration

**Linkerd Patterns:**
- **HTTPRoute:** Traffic splitting, retries (Gateway API standard)
- **ServiceProfile:** Per-route metrics, timeouts, retries
- **TrafficSplit:** Canary deployments (SMI-compatible)
- **Authorization Policy:** Route-level access control

**Cilium Patterns:**
- **CiliumNetworkPolicy:** L3/L4/L7 network rules
- **CiliumEnvoyConfig:** Envoy-based L7 routing
- **DNS-based policies:** FQDN matching for external services
- **eBPF programs:** Custom packet processing

#### 5. Progressive Delivery (2025)

**Canary Deployments:**
- Gradual traffic shift: 5% → 10% → 25% → 50% → 100%
- Automated rollback on metric thresholds (error rate, latency)
- Integration with Flagger for GitOps-driven rollouts

**Blue/Green Deployments:**
- Instant traffic switch between versions
- Test green environment with subset of traffic
- Quick rollback by switching back to blue

**A/B Testing:**
- Route by headers (user-agent, cookies, custom headers)
- Subset-based routing (logged-in users, beta testers)
- Metrics comparison between variants

---

## Service Mesh Taxonomy

### Core Components

#### 1. Control Plane

**Istio (Istiod):**
- Service discovery
- Configuration management
- Certificate authority (CA)
- xDS API server (for Envoy)
- Sidecar injection webhook

**Linkerd (Control Plane):**
- Destination service (service discovery)
- Identity service (mTLS certificates)
- Proxy injector (automatic injection)
- Web dashboard (UI)

**Cilium (Cilium Agent + Operator):**
- Agent on every node (eBPF programs)
- Operator (cluster-wide CRD management)
- Hubble (observability)
- Cluster mesh (multi-cluster)

#### 2. Data Plane

**Istio:**
- **Sidecar mode:** Envoy proxy per pod
- **Ambient mode:** ztunnel (L4, per-node) + waypoint (L7, optional)

**Linkerd:**
- **linkerd2-proxy:** Rust-based, ultralight micro-proxy

**Cilium:**
- **eBPF programs:** Kernel-level packet processing
- **Envoy (optional):** L7 proxy for advanced HTTP routing

#### 3. Traffic Management

**Routing Constructs:**
- Path-based routing (`/api/v1`, `/api/v2`)
- Header-based routing (user-agent, custom headers)
- Weight-based routing (traffic splitting)
- Geo-routing (region-based)

**Resilience Patterns:**
- Retries (automatic, with backoff)
- Timeouts (request, connection)
- Circuit breakers (fail-fast)
- Fault injection (chaos engineering)

#### 4. Security

**Identity and Authentication:**
- SPIFFE workload identity
- X.509 certificates
- JWT authentication
- Service account binding

**Authorization:**
- Network policies (L3/L4)
- Authorization policies (L7)
- RBAC integration
- External authorization (OPA, ext-authz)

**Encryption:**
- mTLS (service-to-service)
- TLS termination (at gateway)
- TLS origination (to external services)

#### 5. Observability

**Metrics (Prometheus):**
- Request rate, error rate, duration (RED)
- TCP connections, bytes sent/received
- Service-level objectives (SLOs)

**Tracing (Jaeger/Zipkin):**
- Distributed traces across services
- Span context propagation
- Latency analysis

**Logging:**
- Access logs (Envoy format)
- Audit logs (policy enforcement)
- Control plane logs

---

## Decision Framework

### Choosing a Service Mesh

```
Decision Tree:

Start: Need service mesh?
│
├─→ Priority: Simplicity + Low Overhead
│   └─→ **Linkerd**
│       - Lightweight (Rust micro-proxy)
│       - Easy setup, minimal config
│       - Best latency overhead (33%)
│
├─→ Priority: eBPF Future + Kernel Performance
│   └─→ **Cilium**
│       - Sidecar-less by design
│       - Advanced networking (eBPF)
│       - Integrated with CNI
│
├─→ Priority: Enterprise Features + Flexibility
│   └─→ **Istio**
│       ├─→ Sidecar Mode (traditional)
│       │   - Fine-grained L7 control per pod
│       │   - Mature, battle-tested
│       │   - 166% latency overhead with mTLS
│       │
│       └─→ Ambient Mode (modern)
│           - Sidecar-less L4 (ztunnel)
│           - Optional L7 (waypoint)
│           - 8% latency overhead with mTLS
│           - Lower resource consumption
```

### Sidecar vs Sidecar-less

| Criteria | Sidecar (Traditional) | Sidecar-less (Ambient/eBPF) |
|----------|----------------------|----------------------------|
| **Resource Usage** | Higher (per-pod proxy) | Lower (shared node proxy or kernel) |
| **Latency Overhead** | 33-166% (varies by mesh) | 8-99% (Istio ambient: 8%, Cilium: 99%) |
| **L7 Granularity** | Per-pod control | Per-namespace or cluster-wide (waypoint) |
| **Upgrade Complexity** | Pod restart required | Node-level or kernel upgrade |
| **Isolation** | Strong (per-pod) | Weaker (per-node or kernel) |
| **Maturity** | Production-proven | Growing adoption (2025) |
| **Best For** | Fine-grained control, per-service policies | Lower overhead, simplified ops |

### Architecture Selection Matrix

| Use Case | Istio Sidecar | Istio Ambient | Linkerd | Cilium |
|----------|---------------|---------------|---------|--------|
| **Enterprise multi-cloud** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Startup/small team** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Low latency critical** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Advanced L7 routing** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **eBPF-based networking** | ⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐⭐ |
| **Simplicity** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Multi-cluster** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Security (mTLS)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## Istio Patterns

### 1. VirtualService (Traffic Routing)

**Purpose:** Define L7 routing rules for HTTP/gRPC/TCP traffic.

**Common Use Cases:**
- Path-based routing (`/v1`, `/v2`)
- Header-based routing (canary by user-agent)
- Weight-based traffic splitting (90/10 split)
- Fault injection (chaos engineering)

**Example 1: Path-Based Routing**

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews-route
  namespace: bookstore
spec:
  hosts:
  - reviews.bookstore.svc.cluster.local
  http:
  - match:
    - uri:
        prefix: /v2/
    route:
    - destination:
        host: reviews.bookstore.svc.cluster.local
        subset: v2
  - route:
    - destination:
        host: reviews.bookstore.svc.cluster.local
        subset: v1
```

**Example 2: Canary Deployment (90/10)**

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews-canary
  namespace: bookstore
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        user-agent:
          regex: ".*Chrome.*"  # Canary for Chrome users
    route:
    - destination:
        host: reviews
        subset: v2
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 90
    - destination:
        host: reviews
        subset: v2
      weight: 10
```

**Example 3: Timeout and Retries**

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews-resilience
spec:
  hosts:
  - reviews
  http:
  - route:
    - destination:
        host: reviews
        subset: v1
    timeout: 3s
    retries:
      attempts: 3
      perTryTimeout: 1s
      retryOn: 5xx,reset,connect-failure
```

### 2. DestinationRule (Traffic Policy)

**Purpose:** Configure traffic policies for service subsets.

**Common Use Cases:**
- Load balancing algorithms
- Connection pool settings
- Circuit breaker configuration
- TLS settings

**Example 1: Circuit Breaker**

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: reviews-circuit-breaker
spec:
  host: reviews.bookstore.svc.cluster.local
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 10
        http2MaxRequests: 100
        maxRequestsPerConnection: 2
    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

**Example 2: Load Balancing**

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: reviews-lb
spec:
  host: reviews
  trafficPolicy:
    loadBalancer:
      consistentHash:
        httpHeaderName: x-user-id  # Sticky sessions by user ID
  subsets:
  - name: v1
    labels:
      version: v1
    trafficPolicy:
      loadBalancer:
        simple: ROUND_ROBIN
```

### 3. Gateway (Ingress/Egress)

**Purpose:** Configure entry/exit points for mesh traffic.

**Example 1: HTTPS Ingress Gateway**

```yaml
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: bookstore-gateway
  namespace: istio-system
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    hosts:
    - bookstore.example.com
    tls:
      mode: SIMPLE
      credentialName: bookstore-cert  # K8s secret with TLS cert
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: bookstore-ingress
spec:
  hosts:
  - bookstore.example.com
  gateways:
  - istio-system/bookstore-gateway
  http:
  - match:
    - uri:
        prefix: /reviews
    route:
    - destination:
        host: reviews.bookstore.svc.cluster.local
        port:
          number: 9080
```

### 4. AuthorizationPolicy (L7 Security)

**Purpose:** Control access to services based on identity, HTTP attributes.

**Example 1: Deny All by Default**

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: bookstore
spec:
  {}  # Empty spec = deny all traffic
```

**Example 2: Allow Specific Service**

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: allow-productpage
  namespace: bookstore
spec:
  selector:
    matchLabels:
      app: reviews
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/bookstore/sa/productpage
    to:
    - operation:
        methods: ["GET"]
        paths: ["/reviews/*"]
```

**Example 3: JWT Authentication**

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: require-jwt
spec:
  selector:
    matchLabels:
      app: api-gateway
  action: ALLOW
  rules:
  - from:
    - source:
        requestPrincipals: ["*"]  # Any valid JWT
    to:
    - operation:
        methods: ["GET", "POST"]
    when:
    - key: request.auth.claims[role]
      values: ["admin", "developer"]
```

### 5. PeerAuthentication (mTLS)

**Purpose:** Configure mTLS mode for services.

**Example 1: Strict mTLS (Mesh-wide)**

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT  # Reject plaintext connections
```

**Example 2: Permissive Mode (Migration)**

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: reviews-mtls
  namespace: bookstore
spec:
  selector:
    matchLabels:
      app: reviews
  mtls:
    mode: PERMISSIVE  # Accept both mTLS and plaintext
```

---

## Linkerd Patterns

### 1. HTTPRoute (Traffic Splitting)

**Purpose:** Split traffic between service versions (Gateway API standard).

**Example: Canary Deployment (90/10)**

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: reviews-canary
  namespace: bookstore
spec:
  parentRefs:
  - name: reviews
    kind: Service
    group: core
    port: 8080
  rules:
  - backendRefs:
    - name: reviews-v1
      port: 8080
      weight: 90
    - name: reviews-v2
      port: 8080
      weight: 10
```

**Example: Path-Based Routing**

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: api-routing
spec:
  parentRefs:
  - name: api-gateway
    kind: Service
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /v1
    backendRefs:
    - name: api-v1
      port: 8080
  - matches:
    - path:
        type: PathPrefix
        value: /v2
    backendRefs:
    - name: api-v2
      port: 8080
```

### 2. ServiceProfile (Retries and Timeouts)

**Purpose:** Configure per-route resilience policies.

**Example: Per-Route Configuration**

```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: reviews.bookstore.svc.cluster.local
  namespace: bookstore
spec:
  routes:
  - name: GET /api/reviews
    condition:
      method: GET
      pathRegex: /api/reviews
    timeout: 3s
    retryBudget:
      retryRatio: 0.2
      minRetriesPerSecond: 10
      ttl: 10s
  - name: POST /api/reviews
    condition:
      method: POST
      pathRegex: /api/reviews
    timeout: 5s
    isRetryable: false  # Don't retry mutations
```

### 3. Server (Policy Targeting)

**Purpose:** Define subsets of traffic for policy application.

**Example: Target Specific Port**

```yaml
apiVersion: policy.linkerd.io/v1beta3
kind: Server
metadata:
  name: reviews-api
  namespace: bookstore
spec:
  podSelector:
    matchLabels:
      app: reviews
  port: 8080
  proxyProtocol: HTTP/2
```

### 4. AuthorizationPolicy (Access Control)

**Purpose:** Control which services can access others.

**Example 1: Allow Specific Service**

```yaml
apiVersion: policy.linkerd.io/v1alpha1
kind: AuthorizationPolicy
metadata:
  name: reviews-policy
  namespace: bookstore
spec:
  targetRef:
    group: policy.linkerd.io
    kind: Server
    name: reviews-api
  requiredAuthenticationRefs:
  - name: productpage-client
    kind: MeshTLSAuthentication
---
apiVersion: policy.linkerd.io/v1alpha1
kind: MeshTLSAuthentication
metadata:
  name: productpage-client
  namespace: bookstore
spec:
  identities:
  - "productpage.bookstore.serviceaccount.identity.linkerd.cluster.local"
```

**Example 2: Per-Route Authorization**

```yaml
apiVersion: policy.linkerd.io/v1alpha1
kind: HTTPRoute
metadata:
  name: reviews-route
spec:
  parentRefs:
  - name: reviews-api
    kind: Server
  rules:
  - matches:
    - path:
        value: /admin
    filters:
    - type: RequestHeaderModifier
      requestHeaderModifier:
        set:
        - name: x-admin-route
          value: "true"
---
apiVersion: policy.linkerd.io/v1alpha1
kind: AuthorizationPolicy
metadata:
  name: admin-only
spec:
  targetRef:
    group: policy.linkerd.io
    kind: HTTPRoute
    name: reviews-route
  requiredAuthenticationRefs:
  - name: admin-identity
```

### 5. mTLS Configuration

**Purpose:** Linkerd enables mTLS by default. Configuration via control plane.

**Enable mTLS (Default):**
```bash
# mTLS is automatic for all meshed pods
# Certificate rotation handled by Linkerd identity service
linkerd check --proxy
```

**Verify mTLS:**
```bash
linkerd edges deployment/reviews
# Shows mTLS status for each connection
```

---

## Cilium Patterns

### 1. CiliumNetworkPolicy (L3/L4/L7)

**Purpose:** Define network policies using eBPF at kernel level.

**Example 1: L3/L4 Policy (Allow Specific Pods)**

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: reviews-policy
  namespace: bookstore
spec:
  description: "Allow productpage to access reviews on port 8080"
  endpointSelector:
    matchLabels:
      app: reviews
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: productpage
    toPorts:
    - ports:
      - port: "8080"
        protocol: TCP
```

**Example 2: L7 HTTP Policy**

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: reviews-http-policy
spec:
  endpointSelector:
    matchLabels:
      app: reviews
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: productpage
    toPorts:
    - ports:
      - port: "8080"
        protocol: TCP
      rules:
        http:
        - method: GET
          path: "/api/reviews/.*"
        - method: POST
          path: "/api/reviews"
```

**Example 3: DNS-Based Egress Policy**

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: external-api-access
spec:
  endpointSelector:
    matchLabels:
      app: backend
  egress:
  - toFQDNs:
    - matchName: "api.github.com"
    toPorts:
    - ports:
      - port: "443"
        protocol: TCP
  - toEndpoints:  # Allow DNS
    - matchLabels:
        "k8s:io.kubernetes.pod.namespace": kube-system
        "k8s:k8s-app": kube-dns
    toPorts:
    - ports:
      - port: "53"
        protocol: ANY
      rules:
        dns:
        - matchPattern: "*"
```

### 2. CiliumEnvoyConfig (L7 Routing)

**Purpose:** Advanced L7 routing using Envoy integration.

**Example: HTTP Path Routing**

```yaml
apiVersion: cilium.io/v2
kind: CiliumEnvoyConfig
metadata:
  name: reviews-routing
spec:
  services:
  - name: reviews
    namespace: bookstore
  resources:
  - "@type": type.googleapis.com/envoy.config.listener.v3.Listener
    name: reviews-listener
    filterChains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typedConfig:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          routeConfig:
            virtualHosts:
            - name: reviews
              domains: ["*"]
              routes:
              - match:
                  prefix: "/v1"
                route:
                  cluster: reviews-v1
              - match:
                  prefix: "/v2"
                route:
                  cluster: reviews-v2
```

### 3. CiliumClusterwideNetworkPolicy (Multi-Namespace)

**Purpose:** Apply policies across all namespaces.

**Example: Deny All by Default**

```yaml
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: default-deny-all
spec:
  description: "Deny all traffic by default"
  endpointSelector: {}
  ingress:
  - {}  # Empty rule = no traffic allowed
  egress:
  - toEntities:
    - kube-dns  # Allow DNS
```

### 4. mTLS with Cilium

**Purpose:** Enable mutual TLS for pod communication.

**Example: Enable mTLS**

```yaml
# Helm values.yaml for Cilium
authentication:
  mutual:
    spire:
      enabled: true
      install:
        enabled: true
        server:
          dataStorage:
            size: 1Gi
```

**CiliumNetworkPolicy with mTLS:**

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: mtls-required
spec:
  endpointSelector:
    matchLabels:
      app: reviews
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: productpage
    authentication:
      mode: required  # Require mTLS
```

---

## Security Patterns

### Zero-Trust Security Model

**Core Principles:**
1. **Never trust, always verify** - Authenticate every request
2. **Least privilege** - Grant minimum required access
3. **Micro-segmentation** - Isolate services at network level
4. **Defense in depth** - Multiple security layers

**Implementation Pattern:**

```yaml
# Step 1: Deny all by default (Istio)
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: production
spec: {}

---
# Step 2: Enable strict mTLS
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: strict-mtls
  namespace: production
spec:
  mtls:
    mode: STRICT

---
# Step 3: Allow specific service-to-service
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: allow-productpage-to-reviews
  namespace: production
spec:
  selector:
    matchLabels:
      app: reviews
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/production/sa/productpage
    to:
    - operation:
        methods: ["GET"]
        paths: ["/api/reviews/*"]
```

### mTLS Certificate Management

**Automatic Rotation:**

```yaml
# Istio CA configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: istio
  namespace: istio-system
data:
  mesh: |
    certificates:
    - certSigners:
      - clusterissuers.cert-manager.io/istio-ca
      workloadCertTtl: 24h  # Certificate TTL
```

**External CA Integration (cert-manager):**

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: istio-ca
spec:
  ca:
    secretName: istio-ca-secret
---
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  meshConfig:
    caCertificates:
    - pem: |
        # CA certificate
```

### Authorization Policy Patterns

**Pattern 1: Namespace-level Isolation**

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: ns-isolation
  namespace: production
spec:
  action: DENY
  rules:
  - from:
    - source:
        notNamespaces: ["production"]
```

**Pattern 2: JWT-Based Authorization**

```yaml
apiVersion: security.istio.io/v1
kind: RequestAuthentication
metadata:
  name: jwt-auth
spec:
  selector:
    matchLabels:
      app: api-gateway
  jwtRules:
  - issuer: "https://auth.example.com"
    jwksUri: "https://auth.example.com/.well-known/jwks.json"
---
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: require-jwt
spec:
  selector:
    matchLabels:
      app: api-gateway
  action: ALLOW
  rules:
  - from:
    - source:
        requestPrincipals: ["*"]
    when:
    - key: request.auth.claims[role]
      values: ["admin"]
```

**Pattern 3: External Authorization (OPA)**

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: ext-authz-opa
spec:
  selector:
    matchLabels:
      app: reviews
  action: CUSTOM
  provider:
    name: opa
  rules:
  - to:
    - operation:
        paths: ["/api/*"]
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: istio
  namespace: istio-system
data:
  mesh: |
    extensionProviders:
    - name: opa
      envoyExtAuthzGrpc:
        service: opa.opa-system.svc.cluster.local
        port: 9191
```

---

## Progressive Delivery

### Canary Deployment (Istio)

**Stage 1: Deploy v2 with 0% traffic**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: reviews-v2
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: reviews
        version: v2
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews-canary
spec:
  hosts:
  - reviews
  http:
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 100
    - destination:
        host: reviews
        subset: v2
      weight: 0
```

**Stage 2: Route 10% traffic to v2**

```bash
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews-canary
spec:
  hosts:
  - reviews
  http:
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 90
    - destination:
        host: reviews
        subset: v2
      weight: 10
EOF
```

**Stage 3: Progressive increase**

```yaml
# 25%, 50%, 75%, 100% over time
# Monitor metrics between each stage
```

**Stage 4: Automated Rollback (Flagger)**

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: reviews
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: reviews
  service:
    port: 8080
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 1m
  webhooks:
  - name: load-test
    url: http://flagger-loadtester/
    timeout: 5s
```

### Blue/Green Deployment (Linkerd)

**Stage 1: Deploy green alongside blue**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: reviews-blue
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: reviews
        version: blue
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: reviews-green
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: reviews
        version: green
```

**Stage 2: Test green with subset of traffic**

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: reviews-test
spec:
  parentRefs:
  - name: reviews
  rules:
  - matches:
    - headers:
      - name: x-test-version
        value: green
    backendRefs:
    - name: reviews-green
      port: 8080
  - backendRefs:
    - name: reviews-blue
      port: 8080
```

**Stage 3: Instant cutover**

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: reviews-cutover
spec:
  parentRefs:
  - name: reviews
  rules:
  - backendRefs:
    - name: reviews-green  # All traffic to green
      port: 8080
```

**Stage 4: Rollback (if needed)**

```yaml
# Instant rollback to blue
kubectl apply -f - <<EOF
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: reviews-rollback
spec:
  parentRefs:
  - name: reviews
  rules:
  - backendRefs:
    - name: reviews-blue
      port: 8080
EOF
```

### A/B Testing (Header-Based Routing)

**Istio Example:**

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews-ab-test
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        x-user-type:
          exact: beta-tester
    route:
    - destination:
        host: reviews
        subset: v2
  - match:
    - headers:
        cookie:
          regex: "^(.*?;)?(ab-test=variant-b)(;.*)?$"
    route:
    - destination:
        host: reviews
        subset: v2
  - route:
    - destination:
        host: reviews
        subset: v1
```

---

## Tool Recommendations

### Service Mesh Platforms (2025)

#### **Primary: Istio** (Enterprise-grade, feature-rich)

**Context7 Library:** `/websites/istio_io`
**Trust Score:** High (91/100)
**Code Snippets:** 7,796+

**Why Istio?**
- Most mature service mesh (2025)
- Ambient mode reduces overhead (8% vs 166% with sidecars)
- Enterprise features (multi-cluster, multi-tenancy, advanced routing)
- Strong ecosystem (Kiali, Jaeger, Grafana integrations)
- Production-proven at scale

**When to Use:**
- Enterprise environments
- Multi-cloud deployments
- Advanced L7 routing needs
- Multi-cluster federation
- Compliance requirements

**Installation:**
```bash
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH

# Ambient mode (recommended 2025)
istioctl install --set profile=ambient -y

# Sidecar mode (traditional)
istioctl install --set profile=default -y
```

---

#### **Alternative 1: Linkerd** (Lightweight, simplicity-focused)

**Context7 Library:** `/websites/linkerd_io_2_18`
**Trust Score:** High
**Code Snippets:** 2,457+

**Why Linkerd?**
- Lowest latency overhead (33% with mTLS)
- Rust-based micro-proxy (fast, memory-safe)
- Simple installation and operation
- Automatic mTLS with zero config
- Best for small-medium teams

**When to Use:**
- Simplicity is priority
- Low resource overhead required
- Small to medium scale
- Easy onboarding for team

**Installation:**
```bash
curl -sL https://run.linkerd.io/install-edge | sh
export PATH=$HOME/.linkerd2/bin:$PATH

linkerd install --crds | kubectl apply -f -
linkerd install | kubectl apply -f -
linkerd check
```

---

#### **Alternative 2: Cilium** (eBPF-native, future-proof)

**Context7 Library:** `/websites/cilium_io-en-stable`
**Trust Score:** High (83.5/100)
**Code Snippets:** 4,511+

**Why Cilium?**
- Sidecar-less by design (eBPF in kernel)
- Advanced networking capabilities
- Integrated with CNI (replaces kube-proxy)
- Kernel-level observability
- Best for eBPF believers

**When to Use:**
- eBPF-based infrastructure
- Performance-critical workloads
- Advanced network policies
- Future-proof architecture

**Installation:**
```bash
helm repo add cilium https://helm.cilium.io/
helm install cilium cilium/cilium \
  --namespace kube-system \
  --set meshMode=enabled \
  --set authentication.mutual.spire.enabled=true
```

---

### Observability Tools

#### **Kiali** (Service Mesh Dashboard)

**Why Kiali?**
- Visual service topology
- Traffic flow visualization
- Configuration validation
- Policy editor (GUI)

**Installation (with Istio):**
```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/kiali.yaml
kubectl port-forward -n istio-system svc/kiali 20001:20001
```

#### **Prometheus + Grafana** (Metrics)

**Why Prometheus?**
- Standard metrics collection
- Service mesh metrics (RED: Rate, Errors, Duration)
- AlertManager integration

**Installation:**
```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/prometheus.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/grafana.yaml
```

#### **Jaeger** (Distributed Tracing)

**Why Jaeger?**
- Trace requests across services
- Latency analysis
- Dependency visualization

**Installation:**
```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/jaeger.yaml
```

---

### Progressive Delivery Tools

#### **Flagger** (GitOps Canary Deployments)

**Why Flagger?**
- Automated canary analysis
- Rollback on metric thresholds
- Integrates with Istio/Linkerd/Cilium
- Prometheus-driven decisions

**Installation:**
```bash
helm repo add flagger https://flagger.app
helm install flagger flagger/flagger \
  --namespace istio-system \
  --set meshProvider=istio \
  --set metricsServer=http://prometheus:9090
```

#### **Argo Rollouts** (Advanced Deployment Strategies)

**Why Argo Rollouts?**
- Blue/green, canary, A/B testing
- GitOps-native (Argo CD integration)
- Analysis templates (custom metrics)

**Installation:**
```bash
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
```

---

## Skill Structure Design

### SKILL.md Structure (500 lines target)

```markdown
---
name: service-mesh
description: Implement production-ready service mesh deployments with Istio, Linkerd, or Cilium. Configure mTLS, authorization policies, traffic routing, and progressive delivery patterns for secure, observable microservices. Use when setting up service-to-service communication, implementing zero-trust security, or enabling canary deployments.
---

# Service Mesh Implementation Guide

## Purpose
[2-3 sentences on what this skill does]

## When to Use
[Trigger phrases and scenarios]

## Service Mesh Selection
[Quick decision framework with references to decision-tree.md]

## Core Patterns

### Istio Patterns
Reference: references/istio-patterns.md
- VirtualService for traffic routing
- DestinationRule for resilience
- Gateway for ingress/egress
- AuthorizationPolicy for security

### Linkerd Patterns
Reference: references/linkerd-patterns.md
- HTTPRoute for traffic splitting
- ServiceProfile for retries/timeouts
- Server for policy targeting

### Cilium Patterns
Reference: references/cilium-patterns.md
- CiliumNetworkPolicy for L3/L4/L7
- eBPF-based enforcement

## Security (mTLS + Authorization)
Reference: references/security-patterns.md

## Progressive Delivery
Reference: references/progressive-delivery.md

## Multi-Cluster
Reference: references/multi-cluster.md

## Troubleshooting
Reference: references/troubleshooting.md
```

### Bundled Resources (references/)

**1. references/decision-tree.md** (150 lines)
- Visual decision tree (ASCII art)
- Comparison matrix (Istio vs Linkerd vs Cilium)
- Sidecar vs sidecar-less trade-offs

**2. references/istio-patterns.md** (200 lines)
- VirtualService examples (10+ patterns)
- DestinationRule examples (circuit breakers, load balancing)
- Gateway examples (ingress, egress, TLS)
- AuthorizationPolicy examples (L7 security)
- PeerAuthentication (mTLS modes)

**3. references/linkerd-patterns.md** (150 lines)
- HTTPRoute examples (traffic splitting)
- ServiceProfile examples (retries, timeouts)
- Server examples (policy targeting)
- AuthorizationPolicy examples
- mTLS verification commands

**4. references/cilium-patterns.md** (150 lines)
- CiliumNetworkPolicy examples (L3/L4/L7)
- CiliumEnvoyConfig (L7 routing)
- DNS-based egress policies
- mTLS with SPIRE integration
- eBPF observability (Hubble)

**5. references/security-patterns.md** (200 lines)
- Zero-trust architecture
- mTLS configuration (strict, permissive)
- Certificate management (auto-rotation)
- Authorization policy patterns
- JWT authentication
- External authorization (OPA)

**6. references/progressive-delivery.md** (200 lines)
- Canary deployment (step-by-step)
- Blue/green deployment
- A/B testing (header-based routing)
- Flagger integration
- Automated rollback

**7. references/multi-cluster.md** (150 lines)
- Multi-cluster setup (Istio, Linkerd, Cilium)
- Cross-cluster service discovery
- mTLS across clusters
- Failure isolation

**8. references/troubleshooting.md** (100 lines)
- Common issues and solutions
- Debug commands (istioctl, linkerd, cilium)
- Certificate issues
- mTLS troubleshooting
- Performance tuning

### Scripts (scripts/)

**1. scripts/mesh-status.sh**
```bash
#!/bin/bash
# Check service mesh health across all three platforms
```

**2. scripts/validate-mtls.sh**
```bash
#!/bin/bash
# Verify mTLS is working between services
```

**3. scripts/generate-canary-config.py**
```python
#!/usr/bin/env python3
# Generate canary deployment configs with progressive stages
```

---

## Integration Points

### Related Skills

**1. kubernetes-operations**
- Cluster setup prerequisites
- Namespace management
- Service account configuration
- RBAC for service mesh components

**2. security-hardening**
- Container security best practices
- Secret management (TLS certs)
- Vulnerability scanning
- Runtime security

**3. infrastructure-as-code**
- Terraform modules for mesh installation
- Helm chart management
- GitOps workflows (ArgoCD, Flux)

**4. building-ci-pipelines**
- Automated canary deployments
- Progressive delivery in CI/CD
- Integration tests with mesh
- Rollback automation

**5. performance-engineering**
- Latency benchmarking
- Resource optimization (CPU, memory)
- Sidecar overhead tuning
- eBPF performance profiling

**6. testing-strategies**
- Chaos engineering (fault injection)
- Load testing with mesh
- Security testing (penetration tests)
- mTLS verification tests

### External Tool Integrations

**Observability:**
- Prometheus (metrics scraping)
- Grafana (dashboards)
- Jaeger/Zipkin (tracing)
- Kiali (service graph)
- Hubble (Cilium observability)

**Security:**
- cert-manager (certificate lifecycle)
- SPIFFE/SPIRE (workload identity)
- OPA (external authorization)
- Vault (secret management)

**GitOps:**
- Argo CD (declarative deployments)
- Flux (GitOps operator)
- Flagger (progressive delivery)
- Argo Rollouts (advanced strategies)

**Cloud Providers:**
- AWS App Mesh integration
- GCP Traffic Director
- Azure Service Fabric Mesh
- Multi-cloud federation

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

**Deliverables:**
- [ ] Complete SKILL.md (500 lines)
- [ ] Create decision-tree.md
- [ ] Create istio-patterns.md
- [ ] Create linkerd-patterns.md
- [ ] Create cilium-patterns.md

**Tasks:**
1. Write SKILL.md with progressive disclosure
2. Build decision framework (visual tree)
3. Document Istio patterns (10+ examples)
4. Document Linkerd patterns (8+ examples)
5. Document Cilium patterns (8+ examples)

### Phase 2: Security & Delivery (Week 3)

**Deliverables:**
- [ ] Create security-patterns.md
- [ ] Create progressive-delivery.md
- [ ] Create scripts/validate-mtls.sh
- [ ] Create scripts/generate-canary-config.py

**Tasks:**
1. Document zero-trust patterns
2. Document mTLS configurations
3. Document authorization policies
4. Document canary deployment steps
5. Build validation scripts

### Phase 3: Advanced Patterns (Week 4)

**Deliverables:**
- [ ] Create multi-cluster.md
- [ ] Create troubleshooting.md
- [ ] Create scripts/mesh-status.sh
- [ ] Integration with other skills

**Tasks:**
1. Document multi-cluster setup
2. Build troubleshooting guide
3. Create health check scripts
4. Test integration with kubernetes-operations
5. Test integration with security-hardening

### Phase 4: Testing & Refinement (Week 5)

**Deliverables:**
- [ ] 3+ evaluation scenarios
- [ ] Test with real deployments
- [ ] Validate against best practices
- [ ] Performance benchmarks

**Tasks:**
1. Create evaluation: "Set up Istio with mTLS"
2. Create evaluation: "Implement canary deployment"
3. Create evaluation: "Configure multi-cluster mesh"
4. Test skill on production-like scenarios
5. Gather feedback and iterate

---

## Success Metrics

### Skill Effectiveness

**Quantitative:**
- Token usage < 8,000 (Mid Level target)
- SKILL.md < 500 lines (progressive disclosure)
- References total < 1,500 lines
- Script execution time < 30s

**Qualitative:**
- Claude can select correct mesh (Istio/Linkerd/Cilium) based on requirements
- Claude generates valid YAML configurations
- Claude applies security patterns correctly
- Claude troubleshoots common issues effectively

### User Outcomes

**After Using This Skill:**
- Deploy production-ready service mesh in < 1 hour
- Configure mTLS with zero application code changes
- Implement canary deployments with automated rollback
- Set up authorization policies following zero-trust principles
- Troubleshoot mesh issues using provided debugging patterns

---

## References

### Research Sources

**Google Search Grounding (2025):**
- Service mesh comparisons (Istio, Linkerd, Cilium)
- mTLS best practices and authorization policies
- Performance benchmarks (latency overhead)

**Context7 Documentation:**
- Istio: `/websites/istio_io` (7,796 snippets, Trust: 91/100)
- Linkerd: `/websites/linkerd_io_2_18` (2,457 snippets, Trust: High)
- Cilium: `/websites/cilium_io-en-stable` (4,511 snippets, Trust: 83.5/100)

### Key Insights from Research

**2025 Trends:**
1. **Sidecar-less is growing** - Istio ambient mode (8% overhead) vs traditional (166%)
2. **eBPF is maturing** - Cilium adoption increasing for kernel-level performance
3. **Zero-trust is standard** - Default-deny policies, mTLS everywhere
4. **Multi-cluster is essential** - Service mesh federation for multi-cloud
5. **GitOps integration** - Flagger, Argo Rollouts for automated delivery

**Performance Data (mTLS Impact):**
- Istio Sidecar: 166% latency increase
- Istio Ambient: 8% latency increase ⭐
- Linkerd: 33% latency increase ⭐⭐
- Cilium: 99% latency increase

**Recommendation Priority:**
1. **Istio Ambient** - Best balance (features + performance)
2. **Linkerd** - Best simplicity + low overhead
3. **Cilium** - Best for eBPF + future-proof

---

## Appendix: Quick Reference

### Istio Commands

```bash
# Install ambient mode
istioctl install --set profile=ambient -y

# Verify installation
istioctl verify-install

# Add namespace to mesh
kubectl label namespace bookstore istio-injection=enabled

# Analyze configuration
istioctl analyze

# Check mTLS status
istioctl authn tls-check productpage.bookstore.svc.cluster.local

# Proxy status
istioctl proxy-status
```

### Linkerd Commands

```bash
# Install
linkerd install --crds | kubectl apply -f -
linkerd install | kubectl apply -f -

# Check health
linkerd check

# Add namespace to mesh
kubectl annotate namespace bookstore linkerd.io/inject=enabled

# View edges (mTLS status)
linkerd edges deployment/reviews

# Tap live traffic
linkerd tap deployment/reviews

# View metrics
linkerd stat deployment/reviews
```

### Cilium Commands

```bash
# Install with service mesh
helm install cilium cilium/cilium \
  --set meshMode=enabled \
  --set authentication.mutual.spire.enabled=true

# Check status
cilium status

# Verify connectivity
cilium connectivity test

# Observe traffic (Hubble)
hubble observe --namespace bookstore

# Policy analysis
cilium policy get

# mTLS status
cilium bpf auth list
```

---

**End of Master Plan - Ready for SKILL.md Implementation**
