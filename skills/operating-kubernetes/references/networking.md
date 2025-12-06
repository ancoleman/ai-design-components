# Networking

## Table of Contents

1. [NetworkPolicies](#networkpolicies)
2. [Services](#services)
3. [Ingress](#ingress)
4. [Gateway API](#gateway-api)
5. [Service Mesh Integration](#service-mesh-integration)
6. [DNS and Service Discovery](#dns-and-service-discovery)

## NetworkPolicies

### Default Deny Pattern

Implement zero-trust networking with default-deny policies:

```yaml
# Step 1: Deny all ingress and egress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}  # Applies to all pods
  policyTypes:
  - Ingress
  - Egress
```

```yaml
# Step 2: Allow specific traffic
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
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

### Ingress Policies

**Allow from specific namespace:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-frontend-ns
  namespace: backend
spec:
  podSelector:
    matchLabels:
      app: api
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: frontend
    ports:
    - protocol: TCP
      port: 8080
```

**Allow from external IP range:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-external-lb
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: web
  ingress:
  - from:
    - ipBlock:
        cidr: 10.0.0.0/16      # Load balancer CIDR
        except:
        - 10.0.5.0/24          # Exclude monitoring subnet
    ports:
    - protocol: TCP
      port: 80
```

### Egress Policies

**Allow DNS only:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
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

**Allow external API:**
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
  # Allow DNS
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
  # Allow external API
  - to:
    - ipBlock:
        cidr: 203.0.113.0/24  # External API CIDR
    ports:
    - protocol: TCP
      port: 443
```

**Allow all egress (common pattern):**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-egress
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Egress
  egress:
  - {}  # Allow all egress
```

### Database Access Pattern

```yaml
# Backend → Database
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: postgres-allow-backend
  namespace: database
spec:
  podSelector:
    matchLabels:
      app: postgres
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: backend
      podSelector:
        matchLabels:
          tier: api
    ports:
    - protocol: TCP
      port: 5432
```

### Multi-Tier Application Pattern

```yaml
# Tier 1: Frontend → only from ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      tier: frontend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 80
  egress:
  - to:
    - podSelector:
        matchLabels:
          tier: backend
    ports:
    - protocol: TCP
      port: 8080
  - to:  # DNS
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
---
# Tier 2: Backend → only from frontend
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      tier: backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          tier: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          tier: database
    ports:
    - protocol: TCP
      port: 5432
  - to:  # DNS
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
---
# Tier 3: Database → only from backend
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: database-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      tier: database
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          tier: backend
    ports:
    - protocol: TCP
      port: 5432
```

### Testing NetworkPolicies

```bash
# Test connectivity from pod
kubectl run test --rm -it --image=busybox -- wget -O- http://backend:8080

# If connection refused:
# 1. Check NetworkPolicy exists
kubectl get networkpolicies -n production

# 2. Describe policy
kubectl describe networkpolicy backend-allow-frontend -n production

# 3. Check pod labels match selectors
kubectl get pods -n production --show-labels

# 4. Test DNS resolution
kubectl run test --rm -it --image=busybox -- nslookup backend

# 5. Check CNI plugin supports NetworkPolicies
kubectl get nodes -o wide
# (Calico, Cilium, Weave support NetworkPolicies; Flannel does not)
```

## Services

### Service Types

**ClusterIP (Default):**
- Internal cluster access only
- Use for internal microservices

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
  - protocol: TCP
    port: 80        # Service port
    targetPort: 8080  # Container port
```

**NodePort:**
- Expose on each node's IP at static port
- Use for testing or edge cases

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nodeport-svc
spec:
  type: NodePort
  selector:
    app: web
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
    nodePort: 30080  # Optional (auto-assigned if omitted)
```

**LoadBalancer:**
- Provision cloud load balancer
- Use for external HTTP/gRPC services

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-lb
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb  # AWS NLB
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```

**ExternalName:**
- DNS CNAME to external service
- Use for migrating to Kubernetes

```yaml
apiVersion: v1
kind: Service
metadata:
  name: legacy-db
spec:
  type: ExternalName
  externalName: db.example.com
```

### Headless Services

For StatefulSets requiring stable network IDs:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  clusterIP: None  # Headless
  selector:
    app: postgres
  ports:
  - protocol: TCP
    port: 5432
```

**DNS entries:**
- `postgres-0.postgres.default.svc.cluster.local`
- `postgres-1.postgres.default.svc.cluster.local`

### Session Affinity

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: web
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800  # 3 hours
  ports:
  - protocol: TCP
    port: 80
```

### Service Topology

Route traffic to same zone/node for cost savings:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  selector:
    app: backend
  topologyKeys:
  - "kubernetes.io/hostname"           # Prefer same node
  - "topology.kubernetes.io/zone"      # Then same zone
  - "*"                                # Then any node
  ports:
  - protocol: TCP
    port: 8080
```

## Ingress

### Basic Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
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

### TLS/HTTPS

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls  # Created by cert-manager
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```

### Path Types

**Prefix:**
```yaml
path: /api
pathType: Prefix
# Matches: /api, /api/, /api/v1, /api/v1/users
```

**Exact:**
```yaml
path: /api
pathType: Exact
# Matches: /api only (not /api/ or /api/v1)
```

**ImplementationSpecific:**
```yaml
path: /api
pathType: ImplementationSpecific
# Depends on ingress controller
```

### Common Annotations (Nginx)

```yaml
metadata:
  annotations:
    # Rate limiting
    nginx.ingress.kubernetes.io/limit-rps: "10"

    # Timeouts
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "30"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "30"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "30"

    # CORS
    nginx.ingress.kubernetes.io/enable-cors: "true"
    nginx.ingress.kubernetes.io/cors-allow-origin: "https://example.com"

    # Authentication
    nginx.ingress.kubernetes.io/auth-url: "https://auth.example.com"
    nginx.ingress.kubernetes.io/auth-response-headers: "X-User-ID"

    # Rewrite
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    # Matches: /something(/|$)(.*)
```

## Gateway API

### Gateway Resource

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: production-gateway
spec:
  gatewayClassName: nginx
  listeners:
  - name: http
    protocol: HTTP
    port: 80
  - name: https
    protocol: HTTPS
    port: 443
    tls:
      mode: Terminate
      certificateRefs:
      - name: myapp-tls
    allowedRoutes:
      namespaces:
        from: Selector
        selector:
          matchLabels:
            gateway: production
```

### HTTPRoute

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: app-routes
  namespace: production
spec:
  parentRefs:
  - name: production-gateway
    namespace: default
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
      weight: 100
  - matches:
    - path:
        type: PathPrefix
        value: /
    backendRefs:
    - name: frontend
      port: 80
```

### Advanced Routing

**Header-based routing:**
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: header-route
spec:
  parentRefs:
  - name: production-gateway
  rules:
  - matches:
    - headers:
      - name: X-Version
        value: v2
    backendRefs:
    - name: backend-v2
      port: 8080
  - matches:
    - headers:
      - name: X-Version
        value: v1
    backendRefs:
    - name: backend-v1
      port: 8080
```

**Traffic splitting (canary):**
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: canary-route
spec:
  parentRefs:
  - name: production-gateway
  rules:
  - backendRefs:
    - name: backend-v2
      port: 8080
      weight: 10     # 10% traffic
    - name: backend-v1
      port: 8080
      weight: 90     # 90% traffic
```

**Query parameter routing:**
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: query-route
spec:
  parentRefs:
  - name: production-gateway
  rules:
  - matches:
    - queryParams:
      - name: debug
        value: "true"
    backendRefs:
    - name: backend-debug
      port: 8080
```

### Gateway vs. Ingress Comparison

| Feature | Ingress | Gateway API |
|---------|---------|-------------|
| **Role separation** | No | Yes (Gateway for ops, HTTPRoute for devs) |
| **Multi-namespace** | No | Yes |
| **Header routing** | Annotations | Native |
| **Weight-based routing** | Limited | Native |
| **TCP/UDP routing** | No | Yes (TCPRoute, UDPRoute) |
| **Status** | Mature | GA (v1 in 1.29+) |

## Service Mesh Integration

### Istio Integration

**Enable sidecar injection:**
```bash
kubectl label namespace production istio-injection=enabled
```

**VirtualService (L7 routing):**
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: backend
spec:
  hosts:
  - backend
  http:
  - match:
    - headers:
        x-version:
          exact: v2
    route:
    - destination:
        host: backend
        subset: v2
  - route:
    - destination:
        host: backend
        subset: v1
```

**DestinationRule (load balancing, circuit breaking):**
```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: backend
spec:
  host: backend
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
```

### Linkerd Integration

**Inject proxy:**
```bash
kubectl annotate namespace production linkerd.io/inject=enabled
```

**ServiceProfile (retries, timeouts):**
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
    responseClasses:
    - condition:
        status:
          min: 500
          max: 599
      isFailure: true
    retries:
      maxAttempts: 3
      timeout: 10s
```

## DNS and Service Discovery

### DNS Names

**Within same namespace:**
- `backend` → `backend.production.svc.cluster.local`

**Cross-namespace:**
- `backend.production` → `backend.production.svc.cluster.local`

**Full FQDN:**
- `backend.production.svc.cluster.local`

### Custom DNS

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: custom-dns
spec:
  dnsPolicy: "None"
  dnsConfig:
    nameservers:
    - 8.8.8.8
    - 8.8.4.4
    searches:
    - production.svc.cluster.local
    - svc.cluster.local
    - cluster.local
    options:
    - name: ndots
      value: "2"
  containers:
  - name: app
    image: myapp:latest
```

### DNS Caching

```yaml
# NodeLocal DNSCache (DaemonSet)
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-local-dns
  namespace: kube-system
spec:
  selector:
    matchLabels:
      k8s-app: node-local-dns
  template:
    spec:
      containers:
      - name: node-cache
        image: registry.k8s.io/dns/k8s-dns-node-cache:1.22.20
```

## Summary

**Networking Pattern Selection:**

| Use Case | Pattern |
|----------|---------|
| Internal microservices | ClusterIP + NetworkPolicies |
| External HTTP/HTTPS | Ingress or Gateway API |
| TCP/UDP external | LoadBalancer Service |
| Service mesh (advanced routing) | Istio or Linkerd |
| Multi-tenant isolation | NetworkPolicies (default-deny) |
| Zero-trust security | NetworkPolicies + mTLS |

**Best Practices:**
1. Always implement NetworkPolicies (start with default-deny)
2. Use Gateway API for new applications
3. Enable TLS for external traffic (cert-manager)
4. Consider service mesh for advanced routing and mTLS
5. Test NetworkPolicies thoroughly before production
6. Monitor DNS resolution latency
7. Use headless services for StatefulSets
