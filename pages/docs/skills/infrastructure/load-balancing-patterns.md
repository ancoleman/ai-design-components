---
sidebar_position: 5
title: Load Balancing Patterns
description: Distribute traffic with L4/L7 load balancers, health checks, and session management
tags: [infrastructure, load-balancing, networking, high-availability]
---

# Load Balancing Patterns

Distribute traffic across infrastructure using appropriate load balancing approaches, from simple round-robin to global multi-region failover.

## When to Use

Use when:
- Distributing traffic across multiple application servers
- Implementing high availability and failover
- Routing traffic based on URLs, headers, or geographic location
- Managing session persistence across stateless backends
- Deploying applications to Kubernetes clusters
- Configuring global traffic management across regions
- Implementing zero-downtime deployments (blue-green, canary)

## Core Concepts

### Layer 4 vs Layer 7

**Layer 4 (Transport Layer):**
- Routes based on IP address and port (TCP/UDP packets)
- No application data inspection
- Lower latency, higher throughput
- Client source IP preservation
- **Use for:** Database connections, video streaming, gaming, non-HTTP protocols

**Layer 7 (Application Layer):**
- Routes based on HTTP URLs, headers, cookies, request body
- Full application data visibility
- SSL/TLS termination, caching, WAF integration
- Content-based routing capabilities
- **Use for:** Web applications, REST APIs, microservices, complex routing logic

### Load Balancing Algorithms

| Algorithm | Distribution Method | Use Case |
|-----------|-------------------|----------|
| **Round Robin** | Sequential | Stateless, similar servers |
| **Weighted Round Robin** | Capacity-based | Different server specs |
| **Least Connections** | Fewest active connections | Long-lived connections |
| **Least Response Time** | Fastest server | Performance-sensitive |
| **IP Hash** | Client IP-based | Session persistence |
| **Resource-Based** | CPU/memory metrics | Varying workloads |

### Health Check Types

**Shallow (Liveness):** Is the process alive?
- Endpoint: `/health/live` or `/live`
- Returns: 200 if process running
- Use for: Process monitoring, container health

**Deep (Readiness):** Can the service handle requests?
- Endpoint: `/health/ready` or `/ready`
- Validates: Database, cache, external API connectivity
- Use for: Load balancer routing decisions

**Health Check Hysteresis:**
- Different thresholds for marking up vs down
- Example: 3 failures to mark down, 2 successes to mark up
- Prevents flapping

## Cloud Load Balancers

### AWS

**Application Load Balancer (ALB) - Layer 7:**
- HTTP/HTTPS applications, microservices, WebSocket
- Path/host/header routing, AWS WAF integration
- Choose when: Content-based routing needed

**Network Load Balancer (NLB) - Layer 4:**
- Ultra-low latency (&lt;1ms), TCP/UDP, static IPs
- Millions of requests per second
- Choose when: Non-HTTP protocols, performance critical

**Global Accelerator - Layer 4 Global:**
- Multi-region applications, global users
- Anycast IPs, automatic regional failover

### GCP

**Application LB (L7):** Global HTTPS LB, Cloud CDN integration, Cloud Armor (WAF/DDoS)
**Network LB (L4):** Regional TCP/UDP, pass-through balancing, session affinity
**Cloud Load Balancing:** Single anycast IP, global distribution

### Azure

**Application Gateway (L7):** WAF integration, URL-based routing, SSL termination
**Load Balancer (L4):** Basic and Standard SKUs, health probes
**Traffic Manager (Global):** DNS-based routing (priority, weighted, performance)

## Self-Managed Load Balancers

### NGINX
**Best for:** General-purpose HTTP/HTTPS load balancing

```nginx
upstream backend {
    least_conn;
    server backend1.example.com:8080 weight=3;
    server backend2.example.com:8080 weight=2;
    keepalive 32;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### HAProxy
**Best for:** Maximum performance, database load balancing

```haproxy
frontend http_front
    bind *:80
    default_backend web_servers

backend web_servers
    balance roundrobin
    option httpchk GET /health
    server web1 192.168.1.101:8080 check
    server web2 192.168.1.102:8080 check
```

### Envoy
**Best for:** Microservices, Kubernetes, service mesh integration
- Cloud-native design with dynamic configuration (xDS APIs)
- Circuit breakers, retries, timeouts
- Advanced health checks (TCP, HTTP, gRPC)

### Traefik
**Best for:** Docker/Kubernetes environments, dynamic configuration
- Automatic service discovery
- Native Kubernetes integration
- Built-in Let's Encrypt support

## Session Persistence

### Sticky Sessions (Use Sparingly)

**Cookie-Based:**
- Load balancer sets cookie to track server affinity
- Accurate routing, works with NAT/proxies
- HTTP only, adds cookie overhead

**IP Hash:**
- Hash client IP to select backend server
- No cookie required, works for non-HTTP
- Poor distribution with NAT/proxies

**Drawbacks:**
- Uneven load distribution
- Session lost on server failure
- Complicates scaling

### Shared Session Store (Recommended)

Architecture: Stateless application servers + centralized session storage (Redis, Memcached)

**Benefits:**
- No sticky sessions needed
- True load balancing
- Server failures don't lose sessions
- Horizontal scaling trivial

### Client-Side Tokens (Best for APIs)

JWT (JSON Web Tokens): Server generates signed token, client stores and sends with requests

**Benefits:**
- Fully stateless servers
- Perfect load balancing
- No session storage needed

## Kubernetes Ingress Controllers

| Controller | Best For | Strengths |
|------------|----------|-----------|
| **NGINX Ingress** (F5) | General purpose | Stability, wide adoption |
| **Traefik** | Dynamic environments | Easy configuration, service discovery |
| **HAProxy Ingress** | High performance | Advanced L7 routing |
| **Envoy** (Contour/Gateway) | Service mesh | Rich L7 features, extensibility |
| **Kong** | API-heavy apps | JWT auth, rate limiting, plugins |

## Progressive Delivery

### Canary Deployment

```yaml
# Istio VirtualService
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend-canary
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend
        subset: v1
      weight: 90
    - destination:
        host: backend
        subset: v2
      weight: 10
```

### Blue/Green Deployment
- Instant cutover with quick rollback
- Deploy green alongside blue
- Test green, then instant switch
- Rollback to blue if needed

## Quick Selection Guide

| Use Case | Recommended Solution |
|----------|---------------------|
| HTTP web app (AWS) | ALB |
| Non-HTTP protocol (AWS) | NLB |
| Kubernetes HTTP ingress | NGINX Ingress or Traefik |
| Maximum performance | HAProxy |
| Service mesh | Envoy |
| Multi-cloud portable | NGINX or HAProxy |
| Global distribution | CloudFlare, AWS Global Accelerator |

## Related Skills

- [Architecting Networks](./architecting-networks) - Network design and topology for load balancing
- [Operating Kubernetes](./operating-kubernetes) - Ingress controllers for K8s traffic management
- [Writing Infrastructure Code](./writing-infrastructure-code) - Deploy load balancers via Terraform/Pulumi
- [Implementing Service Mesh](./implementing-service-mesh) - Envoy as both ingress and service mesh proxy

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/load-balancing-patterns)
- L4 vs L7 Comparison: `references/l4-vs-l7-comparison.md`
- Health Check Strategies: `references/health-check-strategies.md`
- Cloud Load Balancers: `references/cloud-load-balancers.md`
- Session Persistence: `references/session-persistence.md`
- Kubernetes Ingress: `references/kubernetes-ingress.md`
