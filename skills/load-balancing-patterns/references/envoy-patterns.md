# Envoy Proxy Load Balancing Patterns

Cloud-native proxy for microservices and service mesh architectures.


## Table of Contents

- [Basic HTTP Load Balancing](#basic-http-load-balancing)
- [Load Balancing Policies](#load-balancing-policies)
- [Health Checks](#health-checks)
  - [HTTP Health Check](#http-health-check)
  - [TCP Health Check](#tcp-health-check)
  - [gRPC Health Check](#grpc-health-check)
- [Circuit Breakers](#circuit-breakers)
- [Retry and Timeout Policies](#retry-and-timeout-policies)
- [Advanced Routing](#advanced-routing)
  - [Path-Based Routing](#path-based-routing)
  - [Header-Based Routing](#header-based-routing)
- [TLS Configuration](#tls-configuration)
- [Dynamic Configuration (xDS)](#dynamic-configuration-xds)

## Basic HTTP Load Balancing

```yaml
static_resources:
  listeners:
  - name: main_listener
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 80
    filter_chains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          stat_prefix: ingress_http
          http_filters:
          - name: envoy.filters.http.router
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
          route_config:
            name: local_route
            virtual_hosts:
            - name: backend
              domains: ["*"]
              routes:
              - match:
                  prefix: "/"
                route:
                  cluster: backend_cluster

  clusters:
  - name: backend_cluster
    type: STRICT_DNS
    lb_policy: ROUND_ROBIN
    load_assignment:
      cluster_name: backend_cluster
      endpoints:
      - lb_endpoints:
        - endpoint:
            address:
              socket_address:
                address: backend1.example.com
                port_value: 8080
        - endpoint:
            address:
              socket_address:
                address: backend2.example.com
                port_value: 8080
```

## Load Balancing Policies

**Round Robin:**
```yaml
lb_policy: ROUND_ROBIN
```

**Least Request:**
```yaml
lb_policy: LEAST_REQUEST
least_request_lb_config:
  choice_count: 2
```

**Random:**
```yaml
lb_policy: RANDOM
```

**Ring Hash (consistent hashing):**
```yaml
lb_policy: RING_HASH
ring_hash_lb_config:
  minimum_ring_size: 1024
```

## Health Checks

### HTTP Health Check

```yaml
clusters:
- name: backend_cluster
  health_checks:
  - timeout: 1s
    interval: 5s
    unhealthy_threshold: 3
    healthy_threshold: 2
    http_health_check:
      path: /health
      expected_statuses:
      - start: 200
        end: 299
```

### TCP Health Check

```yaml
health_checks:
- timeout: 1s
  interval: 5s
  unhealthy_threshold: 3
  healthy_threshold: 2
  tcp_health_check: {}
```

### gRPC Health Check

```yaml
health_checks:
- timeout: 1s
  interval: 5s
  grpc_health_check:
    service_name: "myservice"
    authority: "grpc.example.com"
```

## Circuit Breakers

```yaml
clusters:
- name: backend_cluster
  circuit_breakers:
    thresholds:
    - priority: DEFAULT
      max_connections: 1000
      max_pending_requests: 100
      max_requests: 1000
      max_retries: 3
      retry_budget:
        budget_percent:
          value: 25.0
        min_retry_concurrency: 10
```

## Retry and Timeout Policies

```yaml
routes:
- match:
    prefix: "/api"
  route:
    cluster: backend_cluster
    timeout: 15s
    retry_policy:
      retry_on: "5xx"
      num_retries: 3
      per_try_timeout: 5s
```

## Advanced Routing

### Path-Based Routing

```yaml
virtual_hosts:
- name: backend
  domains: ["*"]
  routes:
  - match:
      prefix: "/api"
    route:
      cluster: api_cluster
  - match:
      prefix: "/static"
    route:
      cluster: static_cluster
  - match:
      prefix: "/"
    route:
      cluster: web_cluster
```

### Header-Based Routing

```yaml
routes:
- match:
    prefix: "/"
    headers:
    - name: "X-API-Version"
      exact_match: "v2"
  route:
    cluster: api_v2_cluster
```

## TLS Configuration

```yaml
filter_chains:
- filters:
  - name: envoy.filters.network.http_connection_manager
    # ... config ...
  transport_socket:
    name: envoy.transport_sockets.tls
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.DownstreamTlsContext
      common_tls_context:
        tls_certificates:
        - certificate_chain:
            filename: "/etc/envoy/certs/cert.pem"
          private_key:
            filename: "/etc/envoy/certs/key.pem"
```

## Dynamic Configuration (xDS)

Envoy supports dynamic configuration via xDS APIs:
- **EDS:** Endpoint Discovery Service
- **CDS:** Cluster Discovery Service
- **RDS:** Route Discovery Service
- **LDS:** Listener Discovery Service

Used by service meshes like Istio and Consul Connect.

Complete examples in `examples/envoy/` directory.
