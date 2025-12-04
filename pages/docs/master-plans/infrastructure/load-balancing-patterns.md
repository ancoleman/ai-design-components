---
sidebar_position: 6
title: Load Balancing Patterns
description: Master plan for load balancing strategies across cloud and self-managed solutions with L4/L7 patterns, health checks, and global load balancing
tags: [master-plan, infrastructure, load-balancing, nginx, haproxy, envoy]
---

# Load Balancing Patterns

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Load balancing is critical for distributing traffic across infrastructure. This skill covers L4 vs L7 load balancing, cloud-native solutions, self-managed load balancers, health check patterns, session persistence, and global load balancing strategies.

## Scope

This skill teaches:

- **L4 vs L7 Load Balancing** - Transport layer vs Application layer trade-offs
- **Cloud Load Balancers** - AWS (ALB, NLB), GCP (Application LB, Network LB), Azure (Application Gateway, Load Balancer)
- **Self-Managed** - NGINX, HAProxy, Envoy, Traefik
- **Health Check Patterns** - TCP, HTTP, gRPC, active vs passive monitoring
- **Session Persistence** - Sticky sessions (IP hash, cookie-based), trade-offs
- **Global Load Balancing** - GeoDNS routing, multi-region failover, CDN integration
- **Kubernetes Ingress** - Ingress controllers, Gateway API evolution

## Key Components

### L4 vs L7 Comparison

**Layer 4 (Transport Layer)**
- Routes based on IP address and port only
- Faster, lower latency (no packet inspection)
- Best for: High throughput, non-HTTP protocols, client IP preservation
- Use cases: Database connections, video streaming, gaming, financial transactions

**Layer 7 (Application Layer)**
- Routes based on URLs, headers, cookies, application data
- Enables: Content caching, SSL termination, WAF integration
- Best for: Microservices, content-based routing, advanced security
- Use cases: Web applications, APIs, complex routing logic

### Load Balancing Algorithms

**Round Robin** - Sequential distribution (ensure server homogeneity)
**Weighted Round Robin** - Capacity-based distribution
**Least Connections** - Route to server with fewest connections
**Least Response Time** - Route to fastest-responding server
**IP Hash** - Client IP-based sticky sessions
**Resource-Based** - CPU/memory metrics for routing

### Cloud Load Balancers

**AWS ALB (Application Load Balancer)** - Layer 7
- Advanced routing: path, host, header-based
- WebSocket, TLS termination, AWS WAF integration
- Auto-scaling, high availability
- Targets: EC2, containers, Lambda, IP addresses

**AWS NLB (Network Load Balancer)** - Layer 4
- Ultra-low latency, static IP addresses
- Handles millions of requests/second
- Preserves client IP, TLS termination
- Best for: Unpredictable spikes, low latency

**Decision: ALB by default, NLB for:**
- UDP or non-HTTP protocols
- Ultra-low latency critical
- Static IP addresses required
- Massive traffic spikes

### Self-Managed Comparison

**HAProxy**
- Dedicated high-performance load balancer
- Excellent for HTTP/1.1, HTTP/2 (no native HTTP/3)
- Lowest memory footprint
- Sophisticated algorithms, health checks
- Best for: Maximum performance, database load balancing

**NGINX**
- Web server + reverse proxy + load balancer
- Good performance across workloads
- HTTP/3 support (mature implementation)
- TLS termination with SNI
- Best for: Web stacks, CDN integration, general purpose

**Envoy**
- Cloud-native, service mesh-oriented
- Automatic retries, circuit breaking, rate limiting
- Dynamic configuration via APIs
- Excellent observability
- Higher resource consumption
- Best for: Microservices, Kubernetes, service mesh

**Traefik**
- Dynamic, cloud-native ingress
- Automatic HTTPS (Let's Encrypt)
- Configuration via labels/annotations
- Best for: Kubernetes, Docker, rapid deployment

## Decision Framework

**Which Load Balancer?**

```
Cloud-native application?
  YES → Using Kubernetes?
          YES → Ingress controller needed?
                  YES → NGINX Ingress OR Traefik
                  NO → Service mesh?
                          YES → Envoy (via Istio/Linkerd)
                          NO → Cloud LB (ALB/NLB)
          NO → Cloud provider?
                  AWS → L7 routing? → ALB
                         L4/UDP? → NLB
                  GCP → L7 routing? → Application LB
                         L4? → Network LB
                  Azure → L7 routing? → Application Gateway
                           L4? → Load Balancer
  NO → Self-managed VMs?
          → Maximum performance? → HAProxy
          → General purpose? → NGINX
          → Modern/dynamic? → Traefik
```

## Tool Recommendations

### Kubernetes Ingress Controllers

| Controller | Strengths | Best For |
|------------|-----------|----------|
| **NGINX Ingress** | Mature, widely used, extensive features | General purpose, production |
| **Traefik** | Dynamic config, automatic HTTPS | Cloud-native, ease of use |
| **HAProxy Ingress** | High performance, TCP/UDP | Performance-critical |
| **Envoy (Contour)** | Service mesh integration | Microservices, observability |

### Health Check Best Practices

- Implement active health checks (not just TCP connect)
- Use auto-scaling with load balancers
- Multi-zone/multi-region failover eliminates single points of failure
- Combine L4 for volumetric defense, L7 for application-level security
- Tune connection timeouts based on application needs
- Monitor connection patterns to verify algorithm effectiveness

## Integration Points

**With Other Skills:**
- `network-architecture` - LB networking, hybrid connectivity
- `kubernetes-operations` - Ingress controllers, service mesh
- `infrastructure-as-code` - Terraform/Pulumi for LB provisioning
- `security-hardening` - WAF integration, TLS/SSL
- `dns-management` - GeoDNS, DNS-based load balancing
- `observability` - LB metrics, request tracing

**Workflow Example:**
```
DNS → Global LB → Regional LB → Application
  │       │           │             │
  ▼       ▼           ▼             ▼
Route53  ALB/NLB   Service      Containers
GeoDNS   (AWS)     (K8s)        (Pods)
```

## Learn More

- [Full Master Plan (init.md)](https://github.com/ancoleman/ai-design-components/blob/main/skills/load-balancing-patterns/init.md)
- Related: `network-architecture`, `kubernetes-operations`, `dns-management`
