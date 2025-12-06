# Cilium eBPF Service Mesh Patterns

## Table of Contents

- [CiliumNetworkPolicy Patterns](#ciliumnetworkpolicy-patterns)
- [L7 HTTP Policies](#l7-http-policies)
- [DNS-Based Policies](#dns-based-policies)
- [mTLS with SPIRE](#mtls-with-spire)
- [Observability with Hubble](#observability-with-hubble)

## CiliumNetworkPolicy Patterns

Cilium enforces network policies at kernel level using eBPF.

### L3/L4 Policy (Basic)

Allow specific pods to communicate on specific ports.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  description: "Allow frontend pods to access backend on port 8080"
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
    toPorts:
    - ports:
      - port: "8080"
        protocol: TCP
```

### Namespace-Level Policy

Allow all pods in one namespace to access another.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-from-frontend-namespace
  namespace: backend
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        k8s:io.kubernetes.pod.namespace: frontend
    toPorts:
    - ports:
      - port: "8080"
        protocol: TCP
```

### Egress Policy

Control outbound traffic from pods.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: backend-egress
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: backend
  egress:
  # Allow to database
  - toEndpoints:
    - matchLabels:
        app: postgres
    toPorts:
    - ports:
      - port: "5432"
        protocol: TCP
  # Allow to external API (requires DNS, see below)
  - toFQDNs:
    - matchName: "api.external.com"
    toPorts:
    - ports:
      - port: "443"
        protocol: TCP
  # Allow DNS queries
  - toEndpoints:
    - matchLabels:
        k8s:io.kubernetes.pod.namespace: kube-system
        k8s:k8s-app: kube-dns
    toPorts:
    - ports:
      - port: "53"
        protocol: ANY
      rules:
        dns:
        - matchPattern: "*"
```

### Deny-All Policy

Default deny for zero-trust security.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: deny-all-ingress
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - {}  # Empty rule denies all ingress
```

### Label-Based Selection

Select endpoints using Kubernetes labels.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: label-based-policy
spec:
  endpointSelector:
    matchLabels:
      app: backend
      env: production
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
        env: production
    - matchLabels:
        app: gateway
        tier: public
    toPorts:
    - ports:
      - port: "8080"
```

## L7 HTTP Policies

Cilium supports L7 (HTTP) policy enforcement.

### HTTP Method and Path

Allow specific HTTP methods and paths.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: http-api-policy
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
    toPorts:
    - ports:
      - port: "8080"
        protocol: TCP
      rules:
        http:
        - method: GET
          path: "/api/users"
        - method: GET
          path: "/api/users/.*"
        - method: POST
          path: "/api/users"
```

### HTTP Header Matching

Match on HTTP headers.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: http-header-policy
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
    toPorts:
    - ports:
      - port: "8080"
      rules:
        http:
        - method: GET
          path: "/api/admin/.*"
          headers:
          - "X-Admin-Token: secret-value"
```

### HTTP Host Header

Route based on Host header.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: http-host-policy
spec:
  endpointSelector:
    matchLabels:
      app: ingress
  ingress:
  - fromEndpoints:
    - matchLabels:
        reserved:world
    toPorts:
    - ports:
      - port: "80"
      rules:
        http:
        - method: GET
          host: "api.example.com"
          path: "/.*"
```

### gRPC Policy

Control gRPC services and methods.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: grpc-policy
spec:
  endpointSelector:
    matchLabels:
      app: grpc-backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: grpc-client
    toPorts:
    - ports:
      - port: "9090"
      rules:
        http:
        - method: POST
          path: "/user.UserService/GetUser"
        - method: POST
          path: "/user.UserService/ListUsers"
```

## DNS-Based Policies

Control egress to external services by DNS name.

### Basic FQDN Matching

Allow egress to specific domain.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-github-api
  namespace: production
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
  # Allow DNS
  - toEndpoints:
    - matchLabels:
        k8s:io.kubernetes.pod.namespace: kube-system
        k8s:k8s-app: kube-dns
    toPorts:
    - ports:
      - port: "53"
        protocol: ANY
      rules:
        dns:
        - matchPattern: "*"
```

### Wildcard FQDN

Allow egress to domain and subdomains.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-aws-services
spec:
  endpointSelector:
    matchLabels:
      app: backend
  egress:
  - toFQDNs:
    - matchPattern: "*.amazonaws.com"
    toPorts:
    - ports:
      - port: "443"
        protocol: TCP
```

### Multiple FQDNs

Allow multiple external services.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-external-apis
spec:
  endpointSelector:
    matchLabels:
      app: backend
  egress:
  - toFQDNs:
    - matchName: "api.github.com"
    - matchName: "api.stripe.com"
    - matchPattern: "*.slack.com"
    toPorts:
    - ports:
      - port: "443"
        protocol: TCP
  # Allow DNS
  - toEndpoints:
    - matchLabels:
        k8s:io.kubernetes.pod.namespace: kube-system
        k8s:k8s-app: kube-dns
    toPorts:
    - ports:
      - port: "53"
        protocol: ANY
      rules:
        dns:
        - matchPattern: "*"
```

### DNS Policy with TTL

Configure DNS TTL for policy updates.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: fqdn-with-ttl
spec:
  endpointSelector:
    matchLabels:
      app: backend
  egress:
  - toFQDNs:
    - matchName: "dynamic.example.com"
    toPorts:
    - ports:
      - port: "443"
  egressDeny:
  - toFQDNs:
    - matchPattern: "malicious.*"
```

## mTLS with SPIRE

Cilium integrates with SPIRE for mutual TLS.

### Enable mTLS (Helm Values)

Install Cilium with SPIRE authentication.

```yaml
# values.yaml for Cilium Helm chart
authentication:
  mutual:
    spire:
      enabled: true
      install:
        enabled: true
        server:
          dataStorage:
            size: 1Gi
        agent:
          image:
            tag: 1.8.5
```

### Install Command

```bash
helm install cilium cilium/cilium \
  --namespace kube-system \
  --set authentication.mutual.spire.enabled=true \
  --set authentication.mutual.spire.install.enabled=true
```

### mTLS Required Policy

Require mTLS for specific traffic.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: mtls-required
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
    authentication:
      mode: required  # Require mTLS
    toPorts:
    - ports:
      - port: "8080"
```

### Service Identity Verification

Verify SPIFFE identity in policy.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: identity-based-mtls
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        k8s:io.cilium.k8s.policy.serviceaccount: frontend-sa
    authentication:
      mode: required
    toPorts:
    - ports:
      - port: "8080"
```

### Check mTLS Status

```bash
# List authenticated connections
cilium bpf auth list

# Check specific endpoint
cilium endpoint list
cilium endpoint get <endpoint-id>
```

## Cluster-Wide Policies

Apply policies across all namespaces.

### CiliumClusterwideNetworkPolicy

Global default-deny policy.

```yaml
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: default-deny-all
spec:
  description: "Deny all traffic by default"
  endpointSelector: {}
  ingress:
  - {}
  egress:
  # Allow DNS for all pods
  - toEndpoints:
    - matchLabels:
        k8s:io.kubernetes.pod.namespace: kube-system
        k8s:k8s-app: kube-dns
    toPorts:
    - ports:
      - port: "53"
        protocol: ANY
```

### Allow Cluster Communication

Allow essential cluster traffic.

```yaml
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: allow-cluster-essentials
spec:
  endpointSelector: {}
  egress:
  # Allow to Kubernetes API server
  - toEntities:
    - kube-apiserver
  # Allow DNS
  - toEndpoints:
    - matchLabels:
        k8s:io.kubernetes.pod.namespace: kube-system
        k8s:k8s-app: kube-dns
    toPorts:
    - ports:
      - port: "53"
```

## Observability with Hubble

Hubble provides eBPF-based observability.

### Enable Hubble

```bash
helm upgrade cilium cilium/cilium \
  --namespace kube-system \
  --reuse-values \
  --set hubble.relay.enabled=true \
  --set hubble.ui.enabled=true
```

### Observe Traffic

```bash
# Watch all traffic in namespace
hubble observe --namespace production

# Filter by specific pod
hubble observe --pod backend-7d8f9c5b4-xyz12

# Filter by verdict (dropped, forwarded)
hubble observe --verdict DROPPED

# Filter by protocol
hubble observe --protocol http

# Show specific ports
hubble observe --port 8080

# Show DNS queries
hubble observe --type l7 --protocol dns
```

### Hubble Metrics

Export metrics to Prometheus.

```yaml
# Enable Hubble metrics
hubble:
  metrics:
    enabled:
    - dns
    - drop
    - tcp
    - flow
    - icmp
    - http
```

**Useful Metrics:**

```promql
# HTTP request rate
rate(hubble_http_requests_total[5m])

# DNS query rate
rate(hubble_dns_queries_total[5m])

# Dropped packets
rate(hubble_drop_total[5m])

# TCP flags
rate(hubble_tcp_flags_total[5m])
```

### Hubble UI

Access visual service map.

```bash
# Port forward Hubble UI
kubectl port-forward -n kube-system svc/hubble-ui 12000:80

# Open browser
open http://localhost:12000
```

### Flow Filtering

Advanced flow filtering.

```bash
# Show flows between specific services
hubble observe --from-pod frontend --to-pod backend

# Show HTTP 500 errors
hubble observe --type l7 --http-status 500

# Show specific HTTP methods
hubble observe --type l7 --http-method POST

# Show specific paths
hubble observe --type l7 --http-path "/api/users"

# Export to JSON
hubble observe -o json --last 100 > flows.json
```

## CiliumEnvoyConfig (Advanced L7)

Use Envoy for advanced L7 routing.

### Basic Envoy Configuration

Enable Envoy for specific service.

```yaml
apiVersion: cilium.io/v2
kind: CiliumEnvoyConfig
metadata:
  name: backend-envoy
  namespace: production
spec:
  services:
  - name: backend
    namespace: production
  resources:
  - "@type": type.googleapis.com/envoy.config.listener.v3.Listener
    name: backend-listener
    filterChains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typedConfig:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          statPrefix: backend
          routeConfig:
            name: backend_route
            virtualHosts:
            - name: backend
              domains: ["*"]
              routes:
              - match:
                  prefix: "/v1"
                route:
                  cluster: backend-v1
              - match:
                  prefix: "/v2"
                route:
                  cluster: backend-v2
```

## Multi-Cluster with Cilium

Cluster Mesh enables multi-cluster connectivity.

### Enable Cluster Mesh

```bash
# Install Cilium on cluster 1
helm install cilium cilium/cilium \
  --namespace kube-system \
  --set cluster.name=cluster1 \
  --set cluster.id=1

# Install Cilium on cluster 2
helm install cilium cilium/cilium \
  --namespace kube-system \
  --set cluster.name=cluster2 \
  --set cluster.id=2

# Enable cluster mesh
cilium clustermesh enable

# Connect clusters
cilium clustermesh connect --context cluster1 --destination-context cluster2
```

### Cross-Cluster Policy

Allow traffic between clusters.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: cross-cluster-policy
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
        k8s:io.cilium.k8s.policy.cluster: cluster1
    - matchLabels:
        app: frontend
        k8s:io.cilium.k8s.policy.cluster: cluster2
```

## Best Practices

**Policy Design:**
- Start with cluster-wide default-deny
- Use explicit allow rules for required traffic
- Prefer identity-based policies over IP-based
- Test policies in audit mode before enforcing
- Use labels consistently across applications

**L7 Policies:**
- Apply L7 rules only where necessary (performance impact)
- Combine with L3/L4 rules for defense in depth
- Use HTTP method and path restrictions
- Monitor L7 policy performance with Hubble

**DNS Policies:**
- Always allow DNS to kube-dns
- Use specific FQDNs over wildcards when possible
- Monitor DNS queries for anomalies
- Consider DNS TTL impact on policy updates

**mTLS:**
- Enable SPIRE for production workloads
- Require mTLS for sensitive services
- Monitor authentication failures
- Rotate SPIRE credentials regularly

**Observability:**
- Enable Hubble for all clusters
- Export metrics to Prometheus
- Use Hubble UI for visual debugging
- Set up alerts for dropped packets and policy violations

**Multi-Cluster:**
- Use consistent cluster IDs
- Test failover scenarios
- Monitor cross-cluster latency
- Implement circuit breakers for remote calls
