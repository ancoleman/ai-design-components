# Linkerd Configuration Patterns

## Table of Contents

- [HTTPRoute Patterns](#httproute-patterns)
- [ServiceProfile Patterns](#serviceprofile-patterns)
- [Server and Policy Patterns](#server-and-policy-patterns)
- [Authorization Patterns](#authorization-patterns)
- [Observability Integration](#observability-integration)

## HTTPRoute Patterns

HTTPRoute uses Gateway API standard for traffic management.

### Basic Traffic Splitting

Canary deployment with weight-based routing.

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: backend-canary
  namespace: production
spec:
  parentRefs:
  - name: backend
    kind: Service
    group: core
    port: 8080
  rules:
  - backendRefs:
    - name: backend-v1
      port: 8080
      weight: 90
    - name: backend-v2
      port: 8080
      weight: 10
```

### Path-Based Routing

Route based on URL path prefix.

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: api-versioning
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
  - backendRefs:
    - name: api-v1
      port: 8080
```

### Header-Based Routing

Route based on HTTP headers.

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: header-routing
spec:
  parentRefs:
  - name: backend
  rules:
  - matches:
    - headers:
      - name: x-canary-user
        value: "true"
    backendRefs:
    - name: backend-canary
      port: 8080
  - matches:
    - headers:
      - name: user-agent
        value: "mobile"
        type: Exact
    backendRefs:
    - name: backend-mobile
      port: 8080
  - backendRefs:
    - name: backend-stable
      port: 8080
```

### Request Header Modification

Add, set, or remove headers.

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: header-modification
spec:
  parentRefs:
  - name: backend
  rules:
  - filters:
    - type: RequestHeaderModifier
      requestHeaderModifier:
        set:
        - name: x-forwarded-by
          value: linkerd-mesh
        add:
        - name: x-custom-header
          value: custom-value
        remove:
        - x-internal-header
    backendRefs:
    - name: backend
      port: 8080
```

### Cross-Namespace Routing

Route to services in different namespaces.

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: cross-namespace
  namespace: frontend
spec:
  parentRefs:
  - name: frontend-service
    namespace: frontend
  rules:
  - backendRefs:
    - name: backend-service
      namespace: backend
      port: 8080
```

## ServiceProfile Patterns

ServiceProfile configures per-route metrics, retries, and timeouts.

### Basic ServiceProfile

Define routes for better observability.

```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: backend.production.svc.cluster.local
  namespace: production
spec:
  routes:
  - name: GET /api/users
    condition:
      method: GET
      pathRegex: /api/users
  - name: POST /api/users
    condition:
      method: POST
      pathRegex: /api/users
  - name: GET /api/users/[id]
    condition:
      method: GET
      pathRegex: /api/users/[^/]+
```

### Retries Configuration

Configure automatic retries for idempotent requests.

```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: backend.production.svc.cluster.local
  namespace: production
spec:
  routes:
  - name: GET /api/data
    condition:
      method: GET
      pathRegex: /api/data
    timeout: 3s
    retryBudget:
      retryRatio: 0.2
      minRetriesPerSecond: 10
      ttl: 10s
  - name: POST /api/data
    condition:
      method: POST
      pathRegex: /api/data
    timeout: 5s
    isRetryable: false
```

### Timeout Configuration

Set per-route timeout values.

```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: slow-service.production.svc.cluster.local
spec:
  routes:
  - name: GET /slow-operation
    condition:
      method: GET
      pathRegex: /slow-operation
    timeout: 30s
  - name: GET /fast-operation
    condition:
      method: GET
      pathRegex: /fast-operation
    timeout: 1s
```

### Response Class Configuration

Define custom success criteria.

```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: backend.production.svc.cluster.local
spec:
  routes:
  - name: GET /api/users
    condition:
      method: GET
      pathRegex: /api/users
    responseClasses:
    - condition:
        status:
          min: 200
          max: 299
      isFailure: false
    - condition:
        status:
          min: 500
          max: 599
      isFailure: true
```

### Auto-Generated ServiceProfiles

Generate ServiceProfile from live traffic.

```bash
# Generate from OpenAPI spec
linkerd profile --open-api swagger.json backend

# Generate from Protobuf
linkerd profile --proto api.proto backend

# Generate from live traffic observation
linkerd profile -n production backend --tap deploy/backend --tap-duration 60s
```

## Server and Policy Patterns

Server resource defines policy attachment points.

### Basic Server Definition

Define a server for policy targeting.

```yaml
apiVersion: policy.linkerd.io/v1beta3
kind: Server
metadata:
  name: backend-api
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  port: 8080
  proxyProtocol: HTTP/2
```

### Multiple Ports

Define servers for different ports.

```yaml
apiVersion: policy.linkerd.io/v1beta3
kind: Server
metadata:
  name: backend-http
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  port: 8080
  proxyProtocol: HTTP/1
---
apiVersion: policy.linkerd.io/v1beta3
kind: Server
metadata:
  name: backend-grpc
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  port: 9090
  proxyProtocol: gRPC
```

### Server with HTTP Route

Combine Server with HTTPRoute for granular control.

```yaml
apiVersion: policy.linkerd.io/v1beta3
kind: Server
metadata:
  name: api-server
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  port: 8080
---
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: api-routes
  namespace: production
spec:
  parentRefs:
  - name: api-server
    kind: Server
    group: policy.linkerd.io
  rules:
  - matches:
    - path:
        value: /admin
    backendRefs:
    - name: admin-backend
      port: 8080
  - backendRefs:
    - name: public-backend
      port: 8080
```

## Authorization Patterns

Linkerd authorization uses identity-based access control.

### Allow Specific Service

Allow one service to call another.

```yaml
apiVersion: policy.linkerd.io/v1alpha1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend
  namespace: production
spec:
  targetRef:
    group: policy.linkerd.io
    kind: Server
    name: backend-api
  requiredAuthenticationRefs:
  - name: frontend-identity
    kind: MeshTLSAuthentication
---
apiVersion: policy.linkerd.io/v1alpha1
kind: MeshTLSAuthentication
metadata:
  name: frontend-identity
  namespace: production
spec:
  identities:
  - "frontend.production.serviceaccount.identity.linkerd.cluster.local"
```

### Allow Multiple Services

Allow multiple services with one policy.

```yaml
apiVersion: policy.linkerd.io/v1alpha1
kind: MeshTLSAuthentication
metadata:
  name: allowed-clients
  namespace: production
spec:
  identities:
  - "frontend.production.serviceaccount.identity.linkerd.cluster.local"
  - "gateway.production.serviceaccount.identity.linkerd.local"
  - "*.staging.serviceaccount.identity.linkerd.cluster.local"
---
apiVersion: policy.linkerd.io/v1alpha1
kind: AuthorizationPolicy
metadata:
  name: allow-clients
  namespace: production
spec:
  targetRef:
    kind: Server
    name: backend-api
  requiredAuthenticationRefs:
  - name: allowed-clients
    kind: MeshTLSAuthentication
```

### Per-Route Authorization

Apply different policies to different routes.

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: admin-routes
  namespace: production
spec:
  parentRefs:
  - name: api-server
    kind: Server
    group: policy.linkerd.io
  rules:
  - matches:
    - path:
        value: /admin
    backendRefs:
    - name: admin-backend
      port: 8080
---
apiVersion: policy.linkerd.io/v1alpha1
kind: AuthorizationPolicy
metadata:
  name: admin-only
  namespace: production
spec:
  targetRef:
    kind: HTTPRoute
    name: admin-routes
  requiredAuthenticationRefs:
  - name: admin-identity
    kind: MeshTLSAuthentication
---
apiVersion: policy.linkerd.io/v1alpha1
kind: MeshTLSAuthentication
metadata:
  name: admin-identity
  namespace: production
spec:
  identities:
  - "admin-gateway.production.serviceaccount.identity.linkerd.cluster.local"
```

### Network-Based Authentication

Allow traffic from specific networks (use sparingly, prefer identity).

```yaml
apiVersion: policy.linkerd.io/v1alpha1
kind: NetworkAuthentication
metadata:
  name: internal-network
  namespace: production
spec:
  networks:
  - cidr: 10.0.0.0/8
  - cidr: 192.168.0.0/16
---
apiVersion: policy.linkerd.io/v1alpha1
kind: AuthorizationPolicy
metadata:
  name: allow-internal
  namespace: production
spec:
  targetRef:
    kind: Server
    name: backend-api
  requiredAuthenticationRefs:
  - name: internal-network
    kind: NetworkAuthentication
```

### Default Deny Policy

Deny all traffic by default (zero-trust).

```yaml
apiVersion: policy.linkerd.io/v1beta3
kind: Server
metadata:
  name: backend-locked
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  port: 8080
  # No authorization policies = default deny
```

## Observability Integration

### mTLS Verification

Check mTLS status between services.

```bash
# View service connections and mTLS status
linkerd edges deployment/frontend -n production

# Output shows:
# SRC         DST           SECURED       MSG/SEC
# frontend    backend       √             10.2
```

### Live Traffic Observation

Tap live traffic for debugging.

```bash
# Tap all traffic to backend
linkerd tap deployment/backend -n production

# Tap specific route
linkerd tap deployment/backend -n production --path /api/users

# Tap with filtering
linkerd tap deployment/backend -n production \
  --method GET \
  --path /api/users \
  --authority backend.production.svc.cluster.local
```

### Service Statistics

View service metrics.

```bash
# Per-service metrics
linkerd stat deployment/backend -n production

# Per-route metrics (requires ServiceProfile)
linkerd routes deployment/backend -n production

# Output shows success rate, RPS, latencies (P50, P95, P99)
```

### Dashboard Access

Access Linkerd dashboard.

```bash
# Launch dashboard
linkerd dashboard

# Access specific namespace
linkerd dashboard -n production

# View service graph
linkerd viz dashboard
```

### Prometheus Integration

Linkerd exports metrics to Prometheus automatically.

**Useful Queries:**

```promql
# Request rate
sum(rate(request_total[1m])) by (dst_service)

# Success rate
sum(rate(request_total{classification="success"}[1m])) by (dst_service)
/ sum(rate(request_total[1m])) by (dst_service)

# P95 latency
histogram_quantile(0.95,
  sum(rate(response_latency_ms_bucket[1m])) by (le, dst_service)
)
```

## Multi-Cluster Patterns

### Multi-Cluster Setup

Link multiple clusters.

```bash
# Install Linkerd on cluster 1
linkerd install --cluster-domain cluster1.local | kubectl apply -f -

# Install Linkerd on cluster 2
linkerd install --cluster-domain cluster2.local | kubectl apply -f -

# Link clusters (from cluster 1)
linkerd multicluster link --cluster-name cluster2 | \
  kubectl --context=cluster1 apply -f -

# Export service from cluster 2
kubectl --context=cluster2 label svc/backend \
  mirror.linkerd.io/exported=true -n production
```

### Cross-Cluster Traffic Routing

Route traffic to services in remote clusters.

```yaml
# Service is automatically mirrored with suffix
# backend-cluster2.production.svc.cluster1.local

apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: multi-cluster-routing
  namespace: production
spec:
  parentRefs:
  - name: frontend
  rules:
  # 80% local, 20% remote
  - backendRefs:
    - name: backend
      port: 8080
      weight: 80
    - name: backend-cluster2
      port: 8080
      weight: 20
```

## Best Practices

**HTTPRoute:**
- Use Gateway API standard resources (future-proof)
- Leverage header modification for observability
- Keep route matching simple and explicit
- Use cross-namespace routing sparingly

**ServiceProfile:**
- Auto-generate from OpenAPI/Protobuf when possible
- Set timeouts based on actual performance
- Use retry budgets to prevent retry storms
- Mark mutations (POST, PUT, DELETE) as non-retryable

**Authorization:**
- Prefer identity-based over network-based policies
- Start with default-deny, add explicit allows
- Use Server resources for fine-grained control
- Apply policies at route level for sensitive operations

**Observability:**
- Use tap for real-time debugging (not production monitoring)
- Create ServiceProfiles for per-route metrics
- Integrate with Prometheus for alerting
- Monitor edges for mTLS status

**Multi-Cluster:**
- Use consistent naming across clusters
- Monitor cross-cluster latency
- Implement circuit breakers for remote calls
- Test failover scenarios regularly
