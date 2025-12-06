# Istio Configuration Patterns

## Table of Contents

- [VirtualService Patterns](#virtualservice-patterns)
- [DestinationRule Patterns](#destinationrule-patterns)
- [Gateway Patterns](#gateway-patterns)
- [ServiceEntry Patterns](#serviceentry-patterns)
- [Combined Routing Examples](#combined-routing-examples)

## VirtualService Patterns

VirtualService defines routing rules for traffic within the mesh.

### Path-Based Routing

Route traffic based on URL path.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: api-versioning
  namespace: production
spec:
  hosts:
  - api.example.com
  http:
  - match:
    - uri:
        prefix: /v2/
    route:
    - destination:
        host: api-v2.production.svc.cluster.local
        port:
          number: 8080
  - match:
    - uri:
        prefix: /v1/
    route:
    - destination:
        host: api-v1.production.svc.cluster.local
        port:
          number: 8080
  - route:
    - destination:
        host: api-v1.production.svc.cluster.local
        port:
          number: 8080
```

### Header-Based Routing

Route based on HTTP headers (user-agent, custom headers, cookies).

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: header-routing
spec:
  hosts:
  - backend
  http:
  # Route mobile users to mobile-optimized backend
  - match:
    - headers:
        user-agent:
          regex: ".*(Mobile|Android|iPhone).*"
    route:
    - destination:
        host: backend
        subset: mobile
  # Route beta testers to canary
  - match:
    - headers:
        x-beta-user:
          exact: "true"
    route:
    - destination:
        host: backend
        subset: canary
  # Default route
  - route:
    - destination:
        host: backend
        subset: stable
```

### Weight-Based Traffic Splitting

Distribute traffic across multiple versions.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: canary-rollout
spec:
  hosts:
  - reviews
  http:
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 75
    - destination:
        host: reviews
        subset: v2
      weight: 25
```

### Fault Injection

Inject faults for chaos engineering and testing.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: fault-injection
spec:
  hosts:
  - backend
  http:
  - match:
    - headers:
        x-test-fault:
          exact: "true"
    fault:
      delay:
        percentage:
          value: 10.0
        fixedDelay: 5s
      abort:
        percentage:
          value: 5.0
        httpStatus: 503
    route:
    - destination:
        host: backend
  - route:
    - destination:
        host: backend
```

### Traffic Mirroring

Mirror traffic to a shadow deployment for testing.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: traffic-mirror
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend
        subset: v1
      weight: 100
    mirror:
      host: backend
      subset: v2-shadow
    mirrorPercentage:
      value: 10.0
```

### Retries and Timeouts

Configure resilience policies.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: resilient-routing
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend
    timeout: 3s
    retries:
      attempts: 3
      perTryTimeout: 1s
      retryOn: 5xx,reset,connect-failure,refused-stream
```

### URL Rewrite

Rewrite URLs before routing.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: url-rewrite
spec:
  hosts:
  - api.example.com
  http:
  - match:
    - uri:
        prefix: /legacy/
    rewrite:
      uri: /api/v1/
    route:
    - destination:
        host: backend
```

### CORS Configuration

Configure Cross-Origin Resource Sharing.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: cors-enabled
spec:
  hosts:
  - api.example.com
  http:
  - corsPolicy:
      allowOrigins:
      - exact: https://example.com
      - prefix: https://*.example.com
      allowMethods:
      - GET
      - POST
      - PUT
      - DELETE
      allowHeaders:
      - Authorization
      - Content-Type
      maxAge: "24h"
      allowCredentials: true
    route:
    - destination:
        host: backend
```

## DestinationRule Patterns

DestinationRule configures traffic policies for destinations.

### Circuit Breaker

Fail fast when backend is unhealthy.

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: circuit-breaker
spec:
  host: backend.production.svc.cluster.local
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
      minHealthPercent: 20
```

### Load Balancing Algorithms

Configure client-side load balancing.

**Round Robin:**

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: round-robin-lb
spec:
  host: backend
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN
```

**Consistent Hash (Sticky Sessions):**

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: sticky-sessions
spec:
  host: backend
  trafficPolicy:
    loadBalancer:
      consistentHash:
        httpHeaderName: x-user-id
```

**Least Connections:**

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: least-conn-lb
spec:
  host: backend
  trafficPolicy:
    loadBalancer:
      simple: LEAST_CONN
```

### Subset Configuration

Define subsets based on labels.

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: backend-subsets
spec:
  host: backend
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
  - name: canary
    labels:
      version: v2
      track: canary
```

### TLS Configuration

Configure client-side TLS for upstream connections.

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: tls-origination
spec:
  host: external-service.example.com
  trafficPolicy:
    tls:
      mode: SIMPLE
      sni: external-service.example.com
```

**Mutual TLS to External Service:**

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: mtls-origination
spec:
  host: secure-external.example.com
  trafficPolicy:
    tls:
      mode: MUTUAL
      clientCertificate: /etc/certs/client-cert.pem
      privateKey: /etc/certs/client-key.pem
      caCertificates: /etc/certs/ca-cert.pem
```

### Connection Pool Settings

Control connection pooling behavior.

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: connection-pool
spec:
  host: backend
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
        connectTimeout: 30ms
        tcpKeepalive:
          time: 7200s
          interval: 75s
      http:
        h2UpgradePolicy: UPGRADE
        http1MaxPendingRequests: 10
        http2MaxRequests: 100
        maxRequestsPerConnection: 2
        idleTimeout: 3600s
```

## Gateway Patterns

Gateway manages ingress and egress traffic.

### HTTPS Ingress Gateway

Terminate TLS at gateway.

```yaml
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: https-gateway
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
    - api.example.com
    - web.example.com
    tls:
      mode: SIMPLE
      credentialName: example-com-cert
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: gateway-routing
spec:
  hosts:
  - api.example.com
  gateways:
  - istio-system/https-gateway
  http:
  - match:
    - uri:
        prefix: /api/
    route:
    - destination:
        host: backend.production.svc.cluster.local
        port:
          number: 8080
```

### HTTP to HTTPS Redirect

Redirect all HTTP traffic to HTTPS.

```yaml
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: http-redirect
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - api.example.com
    tls:
      httpsRedirect: true
  - port:
      number: 443
      name: https
      protocol: HTTPS
    hosts:
    - api.example.com
    tls:
      mode: SIMPLE
      credentialName: api-cert
```

### Mutual TLS at Gateway

Require client certificates at ingress.

```yaml
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: mtls-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 443
      name: https-mtls
      protocol: HTTPS
    hosts:
    - secure.example.com
    tls:
      mode: MUTUAL
      credentialName: secure-example-com-cert
      caCertificates: /etc/istio/ca-certificates/ca-cert.pem
```

### Egress Gateway

Route external traffic through egress gateway.

```yaml
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: egress-gateway
  namespace: istio-system
spec:
  selector:
    istio: egressgateway
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    hosts:
    - api.external.com
    tls:
      mode: PASSTHROUGH
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: egress-routing
spec:
  hosts:
  - api.external.com
  gateways:
  - mesh
  - istio-system/egress-gateway
  http:
  - match:
    - gateways:
      - mesh
      port: 80
    route:
    - destination:
        host: istio-egressgateway.istio-system.svc.cluster.local
        port:
          number: 443
  - match:
    - gateways:
      - istio-system/egress-gateway
      port: 443
    route:
    - destination:
        host: api.external.com
        port:
          number: 443
```

## ServiceEntry Patterns

ServiceEntry adds external services to mesh.

### External HTTPS Service

Add external API to service registry.

```yaml
apiVersion: networking.istio.io/v1
kind: ServiceEntry
metadata:
  name: external-api
spec:
  hosts:
  - api.github.com
  ports:
  - number: 443
    name: https
    protocol: HTTPS
  location: MESH_EXTERNAL
  resolution: DNS
```

### External Database

Add external database with static IPs.

```yaml
apiVersion: networking.istio.io/v1
kind: ServiceEntry
metadata:
  name: external-postgres
spec:
  hosts:
  - postgres.example.com
  addresses:
  - 10.20.30.40
  ports:
  - number: 5432
    name: postgres
    protocol: TCP
  location: MESH_EXTERNAL
  resolution: STATIC
  endpoints:
  - address: 10.20.30.40
    ports:
      postgres: 5432
```

### Mesh Expansion (VM Integration)

Add VMs to service mesh.

```yaml
apiVersion: networking.istio.io/v1
kind: ServiceEntry
metadata:
  name: vm-service
spec:
  hosts:
  - vm-backend.example.com
  ports:
  - number: 8080
    name: http
    protocol: HTTP
  location: MESH_INTERNAL
  resolution: STATIC
  endpoints:
  - address: 192.168.1.100
    ports:
      http: 8080
    labels:
      app: backend
      version: v1
```

## Combined Routing Examples

### Canary Deployment with Monitoring

Canary deployment with header-based routing and traffic split.

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: backend-subsets
spec:
  host: backend
  subsets:
  - name: stable
    labels:
      version: v1
  - name: canary
    labels:
      version: v2
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend-canary
spec:
  hosts:
  - backend
  http:
  # Internal testers always see canary
  - match:
    - headers:
        x-canary-user:
          exact: "true"
    route:
    - destination:
        host: backend
        subset: canary
  # 10% of production traffic to canary
  - route:
    - destination:
        host: backend
        subset: stable
      weight: 90
    - destination:
        host: backend
        subset: canary
      weight: 10
```

### Multi-Region Routing with Failover

Route to nearest region with failover.

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: multi-region
spec:
  host: backend
  trafficPolicy:
    loadBalancer:
      localityLbSetting:
        enabled: true
        distribute:
        - from: us-east/*
          to:
            "us-east/*": 80
            "us-west/*": 20
        - from: us-west/*
          to:
            "us-west/*": 80
            "us-east/*": 20
    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
```

### A/B Testing

Route traffic based on user segments.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: ab-test
spec:
  hosts:
  - frontend
  http:
  # Variant A: Control group
  - match:
    - headers:
        cookie:
          regex: "^(.*?;)?(ab-test=a)(;.*)?$"
    route:
    - destination:
        host: frontend
        subset: variant-a
  # Variant B: Treatment group
  - match:
    - headers:
        cookie:
          regex: "^(.*?;)?(ab-test=b)(;.*)?$"
    route:
    - destination:
        host: frontend
        subset: variant-b
  # Default: 50/50 split with cookie injection
  - route:
    - destination:
        host: frontend
        subset: variant-a
      weight: 50
    - destination:
        host: frontend
        subset: variant-b
      weight: 50
```

### Blue/Green Deployment

Instant cutover between versions.

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: blue-green
spec:
  hosts:
  - backend
  http:
  # Route all traffic to green (or blue for rollback)
  - route:
    - destination:
        host: backend
        subset: green
---
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: backend-versions
spec:
  host: backend
  subsets:
  - name: blue
    labels:
      version: blue
  - name: green
    labels:
      version: green
```

## Best Practices

**VirtualService:**
- Use specific host matches (avoid wildcards in production)
- Order match conditions from most to least specific
- Always include a default route (no match conditions)
- Set reasonable timeouts (avoid infinite waits)
- Use retries judiciously (avoid retry storms)

**DestinationRule:**
- Configure circuit breakers for external dependencies
- Use outlier detection to remove unhealthy endpoints
- Set connection pool limits to prevent resource exhaustion
- Choose load balancing algorithm based on workload characteristics
- Define subsets for all versions in use

**Gateway:**
- Use TLS for all ingress traffic (HTTPS only)
- Store certificates in Kubernetes secrets
- Configure HTTP to HTTPS redirects
- Use separate gateways for different security zones
- Rotate certificates before expiration

**ServiceEntry:**
- Use DNS resolution for cloud services
- Use STATIC resolution with specific IPs for legacy systems
- Set appropriate protocols (HTTP, HTTPS, TCP, gRPC)
- Configure timeouts and retries for external services
- Monitor external service health
