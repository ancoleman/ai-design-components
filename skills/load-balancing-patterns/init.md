# Load Balancing Patterns Skill - Master Plan

**Skill Name:** `load-balancing-patterns`
**Skill Level:** Mid Level (5,000-8,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Load Balancing Taxonomy](#load-balancing-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Cloud Load Balancers](#cloud-load-balancers)
7. [Self-Managed Load Balancers](#self-managed-load-balancers)
8. [Kubernetes Ingress Controllers](#kubernetes-ingress-controllers)
9. [Health Check Patterns](#health-check-patterns)
10. [Session Persistence Strategies](#session-persistence-strategies)
11. [Global Load Balancing](#global-load-balancing)
12. [Library Recommendations](#library-recommendations)
13. [Skill Structure Design](#skill-structure-design)
14. [Integration Points](#integration-points)
15. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

Load balancing is the critical control plane for distributing traffic across infrastructure. In 2025, with multi-cloud deployments, edge computing, and global user bases, sophisticated load balancing patterns are essential for availability, performance, and cost optimization.

**Market Drivers:**
- **Zero-Downtime Deployments:** Blue-green and canary patterns require advanced traffic management
- **Global Scale:** GeoDNS and multi-region load balancing for worldwide user bases
- **Cost Optimization:** Efficient load distribution reduces infrastructure costs by 20-40%
- **Security:** Load balancers as security control points (DDoS protection, WAF integration)
- **Kubernetes Dominance:** 90%+ cloud-native apps require ingress controller expertise

**Strategic Value:**
1. **Universal Need:** Every distributed system requires load balancing
2. **L4 vs L7 Decision:** Understanding the trade-offs prevents costly mistakes
3. **Multi-Cloud Ready:** Patterns apply across AWS, GCP, Azure
4. **DevOps Critical:** GitOps and IaC require load balancer automation

### How This Differs from Existing Solutions

**Existing Load Balancer Documentation:**
- **Vendor-Specific:** AWS docs OR NGINX docs, not unified decision framework
- **Configuration-Focused:** "How to configure" vs "When to use which type"
- **Missing Context:** No L4 vs L7 comparison or cloud vs self-managed trade-offs

**Our Approach:**
- **Decision Framework First:** When to use ALB vs NLB vs NGINX vs Envoy
- **Multi-Tool Coverage:** Cloud (AWS, GCP, Azure) + Self-managed (HAProxy, NGINX, Envoy, Traefik)
- **Real-World Patterns:** Health checks, session persistence, connection draining
- **Kubernetes Integration:** Ingress controller comparison and selection guide

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **L4 vs L7 Load Balancing**
   - Transport layer (TCP/UDP) vs Application layer (HTTP/HTTPS)
   - Performance vs feature trade-offs
   - When to use each type

2. **Cloud Load Balancers**
   - AWS: ALB (L7), NLB (L4), GLB (Global)
   - GCP: Application LB, Network LB, Cloud Load Balancing
   - Azure: Application Gateway (L7), Load Balancer (L4)

3. **Self-Managed Load Balancers**
   - NGINX: Reverse proxy, load balancer, API gateway
   - HAProxy: High-performance TCP/HTTP load balancer
   - Envoy: Cloud-native, service mesh proxy
   - Traefik: Dynamic, cloud-native ingress

4. **Health Check Patterns**
   - TCP, HTTP, gRPC health checks
   - Active vs passive health monitoring
   - Health check hysteresis and failover

5. **Session Persistence**
   - Sticky sessions (IP hash, cookie-based)
   - Session replication vs client-side tokens
   - Trade-offs and when to avoid stickiness

6. **Global Load Balancing**
   - GeoDNS routing (proximity-based)
   - Multi-region failover
   - CDN integration patterns

7. **Kubernetes Ingress**
   - Ingress controllers: NGINX, Traefik, HAProxy, Envoy
   - Gateway API (evolution of Ingress)
   - Certificate management and TLS termination

### What This Skill Does NOT Cover

- Full service mesh patterns (use service-mesh skill)
- CDN-specific configurations (covered in CDN patterns)
- Network architecture design (use network-architecture skill)
- Cloud provider account setup (use cloud provider-specific skills)

---

## Research Findings

### Google Search Grounding Research (December 2025)

#### Research Query 1: "load balancing best practices 2025 L4 L7 comparison"

**Key Findings:**
- **L4 (Layer 4) Load Balancing:**
  - Operates at transport layer (TCP/UDP)
  - Routes based on IP address and port only
  - Faster, lower latency (no packet inspection)
  - Best for: High throughput, non-HTTP protocols, client IP preservation
  - Use cases: Database connections, video streaming, gaming, financial transactions

- **L7 (Layer 7) Load Balancing:**
  - Operates at application layer (HTTP/HTTPS)
  - Routes based on URLs, headers, cookies, application data
  - Enables: Content caching, SSL termination, WAF integration
  - Best for: Microservices, content-based routing, advanced security
  - Use cases: Web applications, APIs, complex routing logic

**Best Practices 2025:**
- Implement active health checks (not just TCP connect)
- Use auto-scaling with load balancers
- Multi-zone/multi-region failover eliminates single points of failure
- Combine L4 for volumetric defense, L7 for application-level security
- Tune connection timeouts based on application needs
- Monitor connection patterns to verify algorithm effectiveness

**Popular Algorithms:**
- Round Robin: Sequential distribution (ensure server homogeneity)
- Weighted Round Robin: Capacity-based distribution
- Least Connections: Route to server with fewest connections
- Least Response Time: Route to fastest-responding server
- IP Hash: Client IP-based sticky sessions
- Resource-Based: CPU/memory metrics for routing

#### Research Query 2: "AWS ALB NLB vs HAProxy NGINX Envoy comparison"

**Cloud Load Balancers:**

**AWS ALB (Application Load Balancer):**
- Layer 7 (HTTP/HTTPS)
- Advanced routing: path-based, host-based, header-based
- WebSocket support, TLS termination
- Integrates with AWS WAF
- Auto-scaling and high availability
- Targets: EC2, containers, Lambda, IP addresses

**AWS NLB (Network Load Balancer):**
- Layer 4 (TCP/UDP)
- Ultra-low latency, static IP addresses
- Handles millions of requests per second
- TLS termination support
- Preserves client IP addresses
- Best for: Unpredictable traffic spikes, low latency requirements

**Decision: Choose ALB by default, NLB for:**
- UDP or non-HTTP protocols
- Ultra-low latency critical
- Static IP addresses required
- Massive traffic spikes expected

**Self-Managed Comparison:**

**HAProxy:**
- Dedicated high-performance load balancer
- Excellent for HTTP/1.1, HTTP/2 (no native HTTP/3)
- Lowest memory footprint
- Sophisticated algorithms and health checks
- Best for: Maximum performance, database load balancing

**NGINX:**
- Web server + reverse proxy + load balancer
- Good performance across workloads
- HTTP/3 support (mature implementation)
- TLS termination with SNI
- Best for: Web stacks, CDN integration, general purpose

**Envoy:**
- Cloud-native, service mesh-oriented
- Automatic retries, circuit breaking, rate limiting
- Dynamic configuration via APIs
- Excellent observability
- Higher resource consumption than HAProxy/NGINX
- Best for: Microservices, Kubernetes, service mesh

**Performance Summary:**
- **Highest throughput:** HAProxy (HTTP/1.1)
- **Best HTTP/3:** NGINX
- **Lowest memory:** HAProxy < NGINX < Envoy
- **Best for K8s:** Envoy, Traefik

#### Research Query 3: "global load balancing GeoDNS CDN patterns 2025"

**GeoDNS Patterns:**
- Route users to nearest server based on geographic location
- Reduces latency, improves load times
- Supports: Proximity routing, load balancing, failover routing
- Enables geo-targeting for compliance and regional content
- Challenges: VPN/mobile networks can affect accuracy

**CDN Integration:**
- Cache content at multiple PoPs worldwide
- GeoDNS routes to closest CDN node
- Automatic failover if PoP is down or overloaded
- Seamless scalability for traffic surges
- Enhanced DDoS protection

**Multi-CDN Load Balancing:**
- Use multiple CDNs as reverse proxies
- Adaptive geo-defense: Switch to local providers if global CDN blocked
- Regional intelligence for country-specific blocking

**2025 Trends:**
- Security and resilience are top priorities
- AI-related threat protection
- Edge computing integration

#### Research Query 4: "Kubernetes ingress controller comparison 2025"

**Top Ingress Controllers 2025:**

**NGINX Ingress Controller:**
- Most widely used, stable, reliable
- Extensive features: load balancing, SSL termination
- **Important:** Kubernetes community retiring Ingress NGINX in March 2026
- F5 maintains open-source NGINX Ingress Controller (use this)

**Traefik:**
- Dynamic, cloud-native design
- Automated service discovery and SSL management
- Excellent for microservices
- Easy configuration via labels/annotations

**HAProxy Ingress:**
- High performance and reliability
- Advanced Layer 7 routing
- Best for: Performance-critical applications

**Envoy (via Contour, Istio Gateway, Emissary):**
- Advanced L7 features, highly extensible
- Part of service mesh ecosystems
- Steeper learning curve
- Best for: Complex traffic management

**Kong Ingress Controller:**
- API gateway + ingress functionality
- JWT authentication, rate limiting, logging
- Best for: API-heavy applications

**AWS/GCP/Azure Load Balancer Controllers:**
- Direct integration with cloud-managed load balancers
- Best for: Cloud-native, single-cloud deployments

**Gateway API:**
- Next evolution of Kubernetes traffic management
- Role-based resource separation
- Standardized extension points
- Rich traffic management capabilities

**Selection Criteria:**
- **Security:** SSL/TLS termination, WAF integration, zero-trust
- **Performance:** Throughput, latency, CPU utilization
- **Dynamic Configuration:** Auto-discovery for changing environments
- **Extensibility:** Custom plugins, complex routing
- **Cloud Integration:** Managed cloud LB support

### Context7 Library Research (December 2025)

#### NGINX (`/nginx/documentation`)
- **Trust Score:** High
- **Code Snippets:** 5,762
- **Benchmark Score:** 88.5

**Key Capabilities:**
- HTTP/HTTPS reverse proxy and load balancing
- TCP/UDP (stream) load balancing
- Active health checks (NGINX Plus)
- Passive health checks (open source)
- Sticky sessions (cookie-based, IP hash)
- Slow start for gradual traffic ramp-up
- WebSocket support
- SSL/TLS termination

#### HAProxy (`/haproxy/haproxy`)
- **Trust Score:** High
- **Code Snippets:** 1,020
- **Benchmark Score:** N/A (primary repo)

**Key Capabilities:**
- 10+ load balancing algorithms
- Per-server weights and dynamic weight adjustment
- Sophisticated health checks (TCP, HTTP, SMTP, SSL, LDAP, SQL, Redis)
- Sticky sessions with multiple methods
- Health check hysteresis for stable transitions
- Server tracking for atomic failover
- Agent integration for load/health reporting
- Multi-process mode for CPU scaling

#### Envoy (`/envoyproxy/envoy`)
- **Trust Score:** High
- **Code Snippets:** 2,058
- **Benchmark Score:** 77.4

**Key Capabilities:**
- Advanced load balancing algorithms (random, least request, round robin)
- Circuit breakers for fault tolerance
- Active health checks (TCP, HTTP, gRPC)
- Per-endpoint health check addresses
- Priority-based load balancing
- Retry budgets and policies
- Load balancer subsets (metadata-based routing)
- Dynamic configuration via xDS APIs

#### Traefik (`/traefik/traefik`)
- **Trust Score:** High
- **Code Snippets:** 2,466
- **Benchmark Score:** 76.1

**Key Capabilities:**
- Dynamic service discovery (Docker, Kubernetes, etc.)
- Automatic SSL/TLS with Let's Encrypt
- Health checks for load balancer services
- Weighted load balancing
- Highest Random Weight (HRW) algorithm
- Mirroring services
- Native Kubernetes load balancing support
- Middleware for traffic manipulation

#### Kubernetes Ingress Controllers

**NGINX Ingress (`/kubernetes/ingress-nginx`):**
- Trust: High, Snippets: 461, Benchmark: 83.9

**HAProxy Ingress (`/jcmoraisjr/haproxy-ingress`):**
- Trust: High, Snippets: 462

**Envoy Gateway (`/envoyproxy/gateway`):**
- Trust: High, Snippets: 8,780, Benchmark: 86.4

**Contour (`/projectcontour/contour`):**
- Trust: High, Snippets: 10,147, Benchmark: 82.3

---

## Load Balancing Taxonomy

### Tier 1: OSI Layer Classification

#### L4 (Layer 4) - Transport Layer

**Operates on:** TCP/UDP packets
**Routes by:** IP address, port number
**Visibility:** No application data inspection

**Characteristics:**
- Lower latency (no deep packet inspection)
- Higher throughput
- Protocol agnostic (works with any TCP/UDP)
- Preserves client IP addresses
- Limited routing intelligence

**Use Cases:**
- Database connection pooling
- Video/audio streaming
- Gaming servers
- Financial trading systems
- IoT device communication
- DNS load balancing

**Tools:**
- AWS NLB
- GCP Network Load Balancer
- Azure Load Balancer (Standard)
- HAProxy (TCP mode)
- NGINX (stream module)
- Envoy (TCP proxy)

#### L7 (Layer 7) - Application Layer

**Operates on:** HTTP/HTTPS requests
**Routes by:** URLs, headers, cookies, request body
**Visibility:** Full application data

**Characteristics:**
- Content-based routing
- SSL/TLS termination
- Request transformation
- Caching capabilities
- WAF integration
- Authentication/authorization

**Use Cases:**
- Web applications
- Microservices architectures
- REST APIs
- GraphQL endpoints
- WebSocket connections
- gRPC services

**Tools:**
- AWS ALB
- GCP Application Load Balancer
- Azure Application Gateway
- NGINX (HTTP reverse proxy)
- HAProxy (HTTP mode)
- Envoy (HTTP proxy)
- Traefik

### Tier 2: Deployment Model

#### Cloud-Managed Load Balancers

**Advantages:**
- Fully managed (no maintenance)
- Auto-scaling built-in
- High availability guaranteed
- Integrated monitoring
- Native cloud service integration

**Disadvantages:**
- Vendor lock-in
- Cost increases with traffic
- Limited customization
- Configuration via cloud APIs/console

**When to Use:**
- Cloud-native applications
- Teams without LB expertise
- Need for rapid scaling
- Integration with cloud services critical

#### Self-Managed Load Balancers

**Advantages:**
- Full control and customization
- No vendor lock-in
- Predictable costs (infrastructure only)
- Advanced features (HAProxy, NGINX Plus)
- Multi-cloud portable

**Disadvantages:**
- Requires expertise
- Manual scaling
- Maintenance overhead
- High availability requires planning

**When to Use:**
- Multi-cloud or hybrid deployments
- Advanced routing requirements
- Cost optimization important
- Team has load balancing expertise

### Tier 3: Kubernetes Ingress

**Role:** Exposes HTTP/HTTPS routes from outside cluster to services within

**Components:**
- **Ingress Resource:** Kubernetes object defining routing rules
- **Ingress Controller:** Implementation (NGINX, Traefik, HAProxy, etc.)
- **Gateway API:** Next-generation ingress (more expressive)

**Common Patterns:**
- Path-based routing: `/api` → api-service, `/web` → web-service
- Host-based routing: `api.example.com` → api-service
- TLS termination: Handle SSL at ingress
- Rate limiting, authentication via middleware

---

## Decision Frameworks

### Framework 1: L4 vs L7 Selection

```
START: Selecting load balancer type
  │
  ├─► Protocol?
  │     ├─ HTTP/HTTPS only? ──► L7 (ALB, NGINX HTTP, Traefik)
  │     ├─ TCP/UDP? ──► L4 (NLB, HAProxy TCP, NGINX stream)
  │     └─ gRPC? ──► L7 with HTTP/2 support (Envoy, NGINX, Traefik)
  │
  ├─► Routing requirements?
  │     ├─ URL/header-based routing? ──► L7 required
  │     ├─ Content transformation? ──► L7 required
  │     └─ Simple connection balancing? ──► L4 sufficient
  │
  ├─► Performance requirements?
  │     ├─ Ultra-low latency critical? ──► L4 (lower overhead)
  │     ├─ High throughput (millions RPS)? ──► L4 (NLB, HAProxy)
  │     └─ Moderate traffic? ──► Either works
  │
  ├─► Security requirements?
  │     ├─ WAF integration needed? ──► L7 (ALB + WAF)
  │     ├─ SSL termination? ──► L7 (or L4 with TLS passthrough)
  │     └─ DDoS volumetric defense? ──► L4 (absorbs attacks)
  │
  └─► Client IP preservation?
        ├─ Must preserve source IP? ──► L4 (or L7 with X-Forwarded-For)
        └─ Don't care? ──► Either works
```

### Framework 2: Cloud vs Self-Managed

```
START: Cloud or self-managed load balancer?
  │
  ├─► Cloud strategy?
  │     ├─ Single cloud (AWS/GCP/Azure)? ──► Cloud-managed LB
  │     ├─ Multi-cloud? ──► Self-managed (portable)
  │     └─ Hybrid (cloud + on-prem)? ──► Self-managed
  │
  ├─► Team expertise?
  │     ├─ No LB experience? ──► Cloud-managed
  │     ├─ DevOps/SRE team? ──► Either works
  │     └─ Advanced LB needs? ──► Self-managed (more features)
  │
  ├─► Budget model?
  │     ├─ OPEX preferred? ──► Cloud-managed (pay per use)
  │     ├─ CAPEX budget? ──► Self-managed (infrastructure cost)
  │     └─ Cost optimization critical? ──► Self-managed (predictable)
  │
  ├─► Scaling requirements?
  │     ├─ Unpredictable traffic spikes? ──► Cloud-managed (auto-scale)
  │     ├─ Steady traffic? ──► Self-managed (over-provision)
  │     └─ Need instant scale? ──► Cloud-managed
  │
  └─► Customization needs?
        ├─ Standard features sufficient? ──► Cloud-managed
        ├─ Advanced routing/plugins? ──► Self-managed (HAProxy/NGINX)
        └─ Service mesh integration? ──► Self-managed (Envoy)
```

### Framework 3: Health Check Strategy

```
START: Configuring health checks
  │
  ├─► Health check type?
  │     ├─ TCP connect (basic)
  │     │   └─ Checks: Port is open
  │     │   └─ Use for: Non-HTTP services, basic availability
  │     ├─ HTTP request (application-aware)
  │     │   └─ Checks: HTTP 200 response, optional body match
  │     │   └─ Use for: Web apps, APIs, most HTTP services
  │     ├─ HTTPS (with certificate validation)
  │     │   └─ Checks: TLS handshake + HTTP response
  │     │   └─ Use for: Secure services, certificate monitoring
  │     └─ gRPC (application protocol)
  │         └─ Checks: gRPC health check protocol
  │         └─ Use for: gRPC services, microservices
  │
  ├─► Health check interval?
  │     ├─ Critical service? ──► Short interval (5-10s)
  │     ├─ Standard service? ──► Medium interval (10-30s)
  │     └─ Slow-changing backend? ──► Long interval (30-60s)
  │
  ├─► Failure threshold?
  │     ├─ Flaky network? ──► Higher threshold (3-5 failures)
  │     ├─ Stable network? ──► Lower threshold (2-3 failures)
  │     └─ Use hysteresis: Different thresholds for up/down
  │
  └─► Health check endpoint?
        ├─ Shallow check (/health)
        │   └─ Returns 200 if process alive
        │   └─ Fast, but may miss issues
        ├─ Deep check (/health/ready)
        │   └─ Checks dependencies (DB, cache, etc.)
        │   └─ More reliable, but slower
        └─ Best practice: Separate /live and /ready endpoints
```

### Framework 4: Session Persistence Decision

```
START: Do I need sticky sessions?
  │
  ├─► Application architecture?
  │     ├─ Stateless (JWT, client-side tokens)? ──► NO sticky sessions needed
  │     ├─ Server-side sessions (in-memory)? ──► YES, sticky sessions or...
  │     └─ Shared session store (Redis, DB)? ──► NO sticky sessions needed
  │
  ├─► If sticky sessions needed, method?
  │     ├─ Source IP hash
  │     │   └─ Pros: No cookie, works for non-HTTP
  │     │   └─ Cons: NAT/proxy causes uneven distribution
  │     ├─ Cookie-based (load balancer sets cookie)
  │     │   └─ Pros: Accurate, works with NAT
  │     │   └─ Cons: HTTP only, cookie overhead
  │     └─ Application session ID (existing cookie)
  │         └─ Pros: No extra cookie, app-aware
  │         └─ Cons: Requires app support
  │
  ├─► Trade-offs to consider:
  │     ├─ Uneven load distribution (sticky = less balanced)
  │     ├─ Failover complexity (session lost on server failure)
  │     ├─ Scaling difficulty (can't just add servers)
  │     └─ Consider session replication or shared store instead
  │
  └─► Best practice:
        ├─ Prefer stateless architecture (12-factor app)
        ├─ Use shared session store (Redis, Memcached)
        └─ If sticky required, use cookie-based with session replication
```

### Framework 5: Kubernetes Ingress Controller Selection

```
START: Choosing Kubernetes ingress controller
  │
  ├─► Primary requirement?
  │     ├─ Simplicity, wide adoption? ──► NGINX Ingress (F5 version)
  │     ├─ Dynamic, cloud-native? ──► Traefik
  │     ├─ Maximum performance? ──► HAProxy Ingress
  │     ├─ Service mesh integration? ──► Envoy (Contour/Istio Gateway)
  │     ├─ API gateway features? ──► Kong Ingress
  │     └─ Cloud-native only? ──► Cloud provider controller (ALB, etc.)
  │
  ├─► Traffic patterns?
  │     ├─ Mostly HTTP/HTTPS? ──► NGINX, Traefik
  │     ├─ gRPC heavy? ──► Envoy, Traefik
  │     ├─ WebSocket? ──► NGINX, Traefik, Envoy
  │     └─ TCP/UDP? ──► NGINX, HAProxy
  │
  ├─► Configuration style?
  │     ├─ Annotations on services? ──► NGINX, Traefik
  │     ├─ CRDs (Custom Resources)? ──► Traefik, Contour, Gateway API
  │     ├─ Gateway API (future)? ──► Envoy Gateway, upcoming others
  │     └─ File-based? ──► Most support, but less k8s-native
  │
  ├─► Observability needs?
  │     ├─ Prometheus metrics? ──► All major controllers
  │     ├─ Detailed tracing? ──► Envoy (native), Jaeger integration
  │     ├─ Access logs? ──► All support
  │     └─ Dashboard? ──► Traefik (built-in), NGINX (external)
  │
  └─► Migration path?
        ├─ From legacy NGINX Ingress? ──► F5 NGINX Ingress Controller
        ├─ Future-proof? ──► Gateway API compatible (Envoy Gateway)
        └─ Multi-cluster? ──► Traefik Enterprise, Gloo Edge
```

---

## Cloud Load Balancers

### AWS Load Balancers

#### Application Load Balancer (ALB) - Layer 7

**When to Use:**
- HTTP/HTTPS applications
- Microservices with path-based routing
- WebSocket or HTTP/2 applications
- Lambda function targets
- Container-based applications

**Key Features:**
- Host-based routing: `api.example.com` vs `web.example.com`
- Path-based routing: `/api/*` vs `/static/*`
- HTTP header routing: Route based on custom headers
- Query string routing: Route based on parameters
- WebSocket support
- HTTP/2 and gRPC support
- AWS WAF integration
- Cognito authentication
- SSL/TLS termination
- Slow start mode (gradual traffic ramp)

**Configuration Example (Terraform):**

```hcl
resource "aws_lb" "application" {
  name               = "app-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = true
  enable_http2              = true

  tags = {
    Environment = "production"
  }
}

resource "aws_lb_target_group" "app" {
  name     = "app-targets"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    path                = "/health"
    matcher             = "200"
  }

  deregistration_delay = 30

  stickiness {
    type            = "lb_cookie"
    cookie_duration = 86400
    enabled         = true
  }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.application.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = aws_acm_certificate.main.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# Path-based routing
resource "aws_lb_listener_rule" "api" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }

  condition {
    path_pattern {
      values = ["/api/*"]
    }
  }
}
```

#### Network Load Balancer (NLB) - Layer 4

**When to Use:**
- Ultra-low latency required (<1ms)
- TCP/UDP protocols
- Static IP addresses needed
- Millions of requests per second
- Preserve client source IP
- PrivateLink integration

**Key Features:**
- Static IP per AZ (or Elastic IP)
- Extreme performance (millions RPS)
- TLS termination support
- Preserve source IP
- Long-lived TCP connections
- Cross-zone load balancing
- Target: EC2, IP, ALB (yes, NLB → ALB chaining)

**Configuration Example (Terraform):**

```hcl
resource "aws_lb" "network" {
  name               = "app-nlb"
  internal           = false
  load_balancer_type = "network"
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection       = true
  enable_cross_zone_load_balancing = true

  tags = {
    Environment = "production"
  }
}

resource "aws_lb_target_group" "tcp" {
  name     = "tcp-targets"
  port     = 3306
  protocol = "TCP"
  vpc_id   = aws_vpc.main.id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 2
    interval            = 10
    protocol            = "TCP"
  }

  deregistration_delay = 30
  preserve_client_ip   = true
}

resource "aws_lb_listener" "tcp" {
  load_balancer_arn = aws_lb.network.arn
  port              = "3306"
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tcp.arn
  }
}
```

#### Global Accelerator - Layer 4 Global

**When to Use:**
- Multi-region applications
- Global users requiring low latency
- Static anycast IP addresses
- Automatic failover across regions
- DDoS protection via AWS Shield

**Key Features:**
- Two static anycast IPs
- Automatic regional failover
- Health checks per region
- Traffic dials for gradual migration
- Integration with ALB, NLB, EC2, EIP

### GCP Load Balancers

#### Application Load Balancer (L7)

**Types:**
- **External:** Global HTTPS load balancer
- **Internal:** Regional HTTP(S) load balancer
- **Regional External:** Regional HTTP(S) load balancer

**Features:**
- URL map-based routing
- Cloud CDN integration
- Cloud Armor (DDoS/WAF)
- SSL policies
- Backend services with health checks

#### Network Load Balancer (L4)

**Types:**
- **External:** Regional TCP/UDP load balancer
- **Internal:** Regional TCP/UDP load balancer

**Features:**
- Pass-through load balancing
- Preserve client IP
- Session affinity
- Ultra-low latency

#### Cloud Load Balancing (Global)

**Features:**
- Single anycast IP
- Global load distribution
- Cross-region failover
- Integration with Cloud CDN
- Backend buckets (Cloud Storage)

### Azure Load Balancers

#### Application Gateway (L7)

**Features:**
- WAF integration
- URL-based routing
- Multi-site hosting
- SSL termination
- Autoscaling
- Zone redundancy

#### Load Balancer (L4)

**SKUs:**
- **Basic:** Simple TCP/UDP load balancing
- **Standard:** Production-ready, zone redundancy

**Features:**
- Health probes
- Outbound rules
- HA ports
- Multiple frontends

#### Traffic Manager (Global)

**Routing Methods:**
- Priority (failover)
- Weighted
- Performance (latency-based)
- Geographic
- MultiValue
- Subnet

---

## Self-Managed Load Balancers

### NGINX Load Balancing

#### HTTP Load Balancing Configuration

```nginx
# Upstream server pool
upstream backend {
    # Load balancing method (default: round-robin)
    # Options: least_conn, ip_hash, hash $variable [consistent]
    least_conn;

    # Servers
    server backend1.example.com:8080 weight=3 max_fails=3 fail_timeout=30s;
    server backend2.example.com:8080 weight=2;
    server backend3.example.com:8080 backup;  # Only used if primaries fail

    # Keepalive connections
    keepalive 32;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://backend;

        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Keepalive to upstream
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

#### NGINX Plus: Active Health Checks

```nginx
upstream backend {
    zone backend 64k;  # Shared memory for health status

    server backend1.example.com:8080;
    server backend2.example.com:8080;
    server backend3.example.com:8080;
}

# Custom health check match
match server_ok {
    status 200-399;
    header Content-Type = "application/json";
    body ~ "\"status\":\"healthy\"";
}

server {
    listen 80;

    location / {
        proxy_pass http://backend;

        # Active health check
        health_check interval=5s fails=3 passes=2 uri=/health match=server_ok;
    }
}
```

#### NGINX Plus: Sticky Sessions

```nginx
upstream backend {
    zone backend 64k;

    server backend1.example.com:8080;
    server backend2.example.com:8080;

    # Cookie-based sticky sessions
    sticky cookie srv_id expires=1h domain=.example.com path=/;

    # OR: Learn from application cookie
    # sticky learn create=$upstream_cookie_JSESSIONID
    #              lookup=$cookie_JSESSIONID
    #              zone=client_sessions:1m;
}
```

#### TCP/UDP Stream Load Balancing

```nginx
stream {
    upstream mysql_backend {
        least_conn;
        server mysql1.example.com:3306 max_fails=3 fail_timeout=30s;
        server mysql2.example.com:3306;
    }

    server {
        listen 3306;
        proxy_pass mysql_backend;
        proxy_timeout 5s;
        proxy_connect_timeout 1s;
    }
}
```

### HAProxy Load Balancing

#### HTTP Load Balancing Configuration

```haproxy
global
    log /dev/log local0
    log /dev/log local1 notice
    maxconn 4096
    user haproxy
    group haproxy
    daemon

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    option  http-server-close
    option  forwardfor except 127.0.0.0/8
    option  redispatch
    retries 3
    timeout connect 5000
    timeout client  50000
    timeout server  50000

# Frontend
frontend http_front
    bind *:80
    bind *:443 ssl crt /etc/haproxy/certs/example.com.pem

    # Redirect HTTP to HTTPS
    redirect scheme https code 301 if !{ ssl_fc }

    # ACLs
    acl is_api path_beg /api
    acl is_static path_beg /static

    # Backend routing
    use_backend api_servers if is_api
    use_backend static_servers if is_static
    default_backend web_servers

# Backend: Web servers
backend web_servers
    balance roundrobin
    option httpchk GET /health HTTP/1.1\r\nHost:\ example.com
    http-check expect status 200

    # Servers
    server web1 192.168.1.101:8080 check inter 5s fall 3 rise 2 weight 100
    server web2 192.168.1.102:8080 check inter 5s fall 3 rise 2 weight 100
    server web3 192.168.1.103:8080 check inter 5s fall 3 rise 2 weight 50 backup

    # Cookie-based persistence
    cookie SERVERID insert indirect nocache

# Backend: API servers
backend api_servers
    balance leastconn
    option httpchk GET /api/health
    http-check expect rstring \"status\":\"ok\"

    server api1 192.168.1.201:8080 check inter 3s
    server api2 192.168.1.202:8080 check inter 3s
    server api3 192.168.1.203:8080 check inter 3s
```

#### HAProxy Health Checks

```haproxy
backend web_servers
    # HTTP health check with custom request
    option httpchk GET /health HTTP/1.1\r\nHost:\ example.com\r\nUser-Agent:\ HAProxy
    http-check expect status 200

    # Or: Check response body
    http-check expect rstring \"healthy\"

    # Or: Multiple checks
    http-check send meth GET uri /health ver HTTP/1.1 hdr Host example.com
    http-check expect status 200
    http-check expect string OK

# TCP health check
backend mysql_servers
    mode tcp
    option tcp-check
    tcp-check connect port 3306

    server mysql1 192.168.1.101:3306 check inter 5s

# Redis health check
backend redis_servers
    mode tcp
    option tcp-check
    tcp-check send PING\r\n
    tcp-check expect string +PONG

    server redis1 192.168.1.101:6379 check inter 1s
```

#### HAProxy Sticky Sessions

```haproxy
backend web_servers
    balance roundrobin

    # Method 1: Source IP hash
    # balance source
    # hash-type consistent  # Better distribution

    # Method 2: Cookie insertion
    cookie SERVERID insert indirect nocache
    server web1 192.168.1.101:8080 check cookie web1
    server web2 192.168.1.102:8080 check cookie web2

    # Method 3: Learn from application cookie
    # stick-table type string len 32 size 100k expire 30m
    # stick on cookie(JSESSIONID)
```

### Envoy Load Balancing

#### Basic Cluster Configuration

```yaml
# envoy.yaml
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

#### Envoy Health Checks

```yaml
clusters:
- name: backend_cluster
  type: STRICT_DNS
  lb_policy: LEAST_REQUEST
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
      - start: 404
        end: 404
  load_assignment:
    # ... endpoints
```

#### Envoy Circuit Breaker

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

### Traefik Load Balancing

#### Docker Provider Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  traefik:
    image: traefik:v3.0
    command:
      - --api.insecure=true
      - --providers.docker=true
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"  # Dashboard
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro

  app1:
    image: myapp:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`app.example.com`)"
      - "traefik.http.services.app.loadbalancer.server.port=8080"
      - "traefik.http.services.app.loadbalancer.healthcheck.path=/health"
      - "traefik.http.services.app.loadbalancer.healthcheck.interval=10s"
    deploy:
      replicas: 3

  app2:
    image: myapp:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`app.example.com`) && PathPrefix(`/api`)"
      - "traefik.http.services.api.loadbalancer.server.port=8080"
      - "traefik.http.services.api.loadbalancer.sticky.cookie=true"
      - "traefik.http.services.api.loadbalancer.sticky.cookie.name=api_session"
```

#### File Provider Configuration

```yaml
# traefik.yml (static config)
entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"

providers:
  file:
    filename: /etc/traefik/dynamic.yml
    watch: true

# dynamic.yml (dynamic config)
http:
  routers:
    app-router:
      rule: "Host(`app.example.com`)"
      service: app-service
      entryPoints:
        - websecure
      tls:
        certResolver: letsencrypt

  services:
    app-service:
      loadBalancer:
        servers:
          - url: "http://192.168.1.101:8080"
          - url: "http://192.168.1.102:8080"
          - url: "http://192.168.1.103:8080"
        healthCheck:
          path: /health
          interval: 10s
          timeout: 3s
        sticky:
          cookie:
            name: app_session
            httpOnly: true
```

---

## Kubernetes Ingress Controllers

### NGINX Ingress Controller

#### Installation (Helm)

```bash
# Add helm repo (F5 maintained version)
helm repo add nginx-stable https://helm.nginx.com/stable
helm repo update

# Install
helm install nginx-ingress nginx-stable/nginx-ingress \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.type=LoadBalancer
```

#### Basic Ingress Resource

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - app.example.com
    secretName: app-tls
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

#### Advanced: Load Balancing and Health Checks

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
  annotations:
    nginx.ingress.kubernetes.io/load-balance: "least_conn"
    nginx.ingress.kubernetes.io/upstream-hash-by: "$request_uri"
    nginx.ingress.kubernetes.io/affinity: "cookie"
    nginx.ingress.kubernetes.io/affinity-mode: "persistent"
    nginx.ingress.kubernetes.io/session-cookie-name: "api_session"
    nginx.ingress.kubernetes.io/session-cookie-max-age: "3600"
spec:
  selector:
    app: api
  ports:
  - port: 80
    targetPort: 8080
```

### Traefik Ingress Controller

#### Installation (Helm)

```bash
helm repo add traefik https://traefik.github.io/charts
helm repo update

helm install traefik traefik/traefik \
  --namespace traefik \
  --create-namespace \
  --set service.type=LoadBalancer
```

#### IngressRoute (CRD-based)

```yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: app-route
spec:
  entryPoints:
    - websecure
  routes:
  - match: Host(`app.example.com`) && PathPrefix(`/api`)
    kind: Rule
    services:
    - name: api-service
      port: 80
      sticky:
        cookie:
          name: api_session
          httpOnly: true
    middlewares:
    - name: api-ratelimit
  - match: Host(`app.example.com`)
    kind: Rule
    services:
    - name: web-service
      port: 80
  tls:
    certResolver: letsencrypt
```

#### Middleware: Rate Limiting

```yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: api-ratelimit
spec:
  rateLimit:
    average: 100
    burst: 50
    period: 1s
```

### HAProxy Ingress Controller

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    haproxy.org/load-balance: "leastconn"
    haproxy.org/cookie-persistence: "app-cookie"
    haproxy.org/check: "enabled"
    haproxy.org/check-interval: "5s"
spec:
  ingressClassName: haproxy
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

### Gateway API (Future-Proof)

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: app-gateway
spec:
  gatewayClassName: envoy
  listeners:
  - name: http
    protocol: HTTP
    port: 80
  - name: https
    protocol: HTTPS
    port: 443
    tls:
      certificateRefs:
      - name: app-tls

---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: app-route
spec:
  parentRefs:
  - name: app-gateway
  hostnames:
  - "app.example.com"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /api
    backendRefs:
    - name: api-service
      port: 80
  - matches:
    - path:
        type: PathPrefix
        value: /
    backendRefs:
    - name: web-service
      port: 80
```

---

## Health Check Patterns

### Pattern 1: Shallow vs Deep Health Checks

#### Shallow Health Check (Liveness)

**Purpose:** Is the process alive?
**Endpoint:** `/health/live` or `/live`
**Response:** 200 if process running

```python
# Python/Flask example
@app.route('/health/live')
def liveness():
    return {'status': 'alive'}, 200
```

**Use for:** Kubernetes liveness probe, basic monitoring

#### Deep Health Check (Readiness)

**Purpose:** Can the service handle requests?
**Endpoint:** `/health/ready` or `/ready`
**Checks:** Dependencies (DB, cache, external APIs)

```python
@app.route('/health/ready')
def readiness():
    checks = {
        'database': check_database(),
        'redis': check_redis(),
        'api': check_external_api()
    }

    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503

    return {
        'status': 'ready' if all_healthy else 'not_ready',
        'checks': checks
    }, status_code
```

**Use for:** Load balancer health checks, Kubernetes readiness probe

### Pattern 2: Health Check Hysteresis

**Problem:** Flapping services (up/down/up/down) cause instability

**Solution:** Different thresholds for marking up vs down

```nginx
# NGINX Plus
health_check interval=5s fails=3 passes=2 uri=/health;
# Requires 3 failures to mark down
# Requires 2 successes to mark up
```

```hcl
# AWS ALB Target Group
resource "aws_lb_target_group" "app" {
  health_check {
    healthy_threshold   = 2  # Successes to mark healthy
    unhealthy_threshold = 3  # Failures to mark unhealthy
    interval            = 30
  }
}
```

### Pattern 3: Timeout Configuration

**Guidelines:**
- **Connect timeout:** 1-5 seconds (fast detection of down servers)
- **Read timeout:** Application-dependent (5-60 seconds)
- **Health check timeout:** Shorter than interval (e.g., 3s check every 10s)

```yaml
# Kubernetes readiness probe
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 3
  successThreshold: 1
  failureThreshold: 3
```

### Pattern 4: Custom Health Check Matchers

```nginx
# NGINX Plus: Match response body
match app_healthy {
    status 200-299;
    header Content-Type = "application/json";
    body ~ "\"status\":\"healthy\"";
}

health_check match=app_healthy;
```

```haproxy
# HAProxy: Expect specific response
backend api_servers
    option httpchk GET /health
    http-check expect rstring \"status\":\"ok\"
```

---

## Session Persistence Strategies

### Strategy 1: Sticky Sessions (Avoid if Possible)

#### Cookie-Based Stickiness

**Load Balancer Sets Cookie:**

```nginx
# NGINX Plus
upstream backend {
    sticky cookie srv_id expires=1h domain=.example.com path=/;
    server backend1.example.com:8080;
    server backend2.example.com:8080;
}
```

```haproxy
# HAProxy
backend web_servers
    cookie SERVERID insert indirect nocache
    server web1 192.168.1.101:8080 check cookie web1
    server web2 192.168.1.102:8080 check cookie web2
```

**Application Cookie Stickiness:**

```nginx
# NGINX Plus: Learn from app cookie
upstream backend {
    sticky learn create=$upstream_cookie_JSESSIONID
                 lookup=$cookie_JSESSIONID
                 zone=client_sessions:1m;

    server backend1.example.com:8080;
    server backend2.example.com:8080;
}
```

#### IP Hash Stickiness

```nginx
upstream backend {
    ip_hash;  # Hash client IP to select server
    server backend1.example.com:8080;
    server backend2.example.com:8080;
}
```

**Drawbacks:**
- NAT/proxies cause uneven distribution
- All clients behind same NAT go to same server
- Doesn't work with IPv4/IPv6 dual-stack

### Strategy 2: Shared Session Store (Recommended)

**Architecture:** Stateless app servers + centralized session storage

```
Client → Load Balancer → App Server 1 ↘
                      ↘ App Server 2 → Redis/Memcached (Sessions)
                       ↘ App Server 3 ↗
```

**Implementation (Node.js/Express):**

```javascript
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const { createClient } = require('redis');

// Redis client
const redisClient = createClient({
  host: 'redis.example.com',
  port: 6379
});

// Session middleware
app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: 'session-secret',
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,
    httpOnly: true,
    maxAge: 3600000  // 1 hour
  }
}));
```

**Benefits:**
- No sticky sessions needed
- Horizontal scaling simple
- Server failures don't lose sessions
- True load balancing

### Strategy 3: Client-Side Tokens (Best for APIs)

**JWT (JSON Web Tokens):**

```javascript
// Server generates JWT
const jwt = require('jsonwebtoken');

function login(user) {
  const token = jwt.sign(
    { userId: user.id, role: user.role },
    process.env.JWT_SECRET,
    { expiresIn: '1h' }
  );

  return { token };
}

// Client stores in localStorage/cookie
// Sends with each request: Authorization: Bearer <token>

// Server validates (stateless)
function authenticate(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    res.status(401).json({ error: 'Invalid token' });
  }
}
```

**Benefits:**
- Fully stateless servers
- Perfect load balancing
- Horizontal scaling trivial
- No session storage needed

---

## Global Load Balancing

### Pattern 1: GeoDNS Routing

**How It Works:** DNS returns different IPs based on client location

**AWS Route 53 Example:**

```hcl
resource "aws_route53_record" "geo" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  # US-East users
  geolocation_routing_policy {
    continent = "NA"
  }

  set_identifier = "US-East"
  alias {
    name                   = aws_lb.us_east.dns_name
    zone_id                = aws_lb.us_east.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "geo_eu" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  # Europe users
  geolocation_routing_policy {
    continent = "EU"
  }

  set_identifier = "EU-West"
  alias {
    name                   = aws_lb.eu_west.dns_name
    zone_id                = aws_lb.eu_west.zone_id
    evaluate_target_health = true
  }
}

# Default (fallback)
resource "aws_route53_record" "geo_default" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  geolocation_routing_policy {
    continent = "*"
  }

  set_identifier = "Default"
  alias {
    name                   = aws_lb.us_east.dns_name
    zone_id                = aws_lb.us_east.zone_id
    evaluate_target_health = true
  }
}
```

### Pattern 2: Latency-Based Routing

```hcl
resource "aws_route53_record" "latency_us" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  latency_routing_policy {
    region = "us-east-1"
  }

  set_identifier = "US-East"
  alias {
    name                   = aws_lb.us_east.dns_name
    zone_id                = aws_lb.us_east.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "latency_eu" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  latency_routing_policy {
    region = "eu-west-1"
  }

  set_identifier = "EU-West"
  alias {
    name                   = aws_lb.eu_west.dns_name
    zone_id                = aws_lb.eu_west.zone_id
    evaluate_target_health = true
  }
}
```

### Pattern 3: Multi-Region Failover

```hcl
# Primary region
resource "aws_route53_record" "primary" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  failover_routing_policy {
    type = "PRIMARY"
  }

  set_identifier = "Primary"
  alias {
    name                   = aws_lb.us_east.dns_name
    zone_id                = aws_lb.us_east.zone_id
    evaluate_target_health = true
  }

  health_check_id = aws_route53_health_check.primary.id
}

# Secondary region (failover)
resource "aws_route53_record" "secondary" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  failover_routing_policy {
    type = "SECONDARY"
  }

  set_identifier = "Secondary"
  alias {
    name                   = aws_lb.eu_west.dns_name
    zone_id                = aws_lb.eu_west.zone_id
    evaluate_target_health = true
  }
}

# Health check for primary
resource "aws_route53_health_check" "primary" {
  fqdn              = aws_lb.us_east.dns_name
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30
}
```

---

## Library Recommendations

### Cloud Load Balancers (Managed)

| Provider | L4 Solution | L7 Solution | Global | Trust |
|----------|-------------|-------------|--------|-------|
| **AWS** | NLB | ALB | Global Accelerator | ⭐⭐⭐⭐⭐ |
| **GCP** | Network LB | Application LB | Cloud Load Balancing | ⭐⭐⭐⭐⭐ |
| **Azure** | Load Balancer | Application Gateway | Traffic Manager | ⭐⭐⭐⭐⭐ |

**When to Use:**
- Cloud-native applications
- Need auto-scaling
- Managed service preferred
- Single-cloud deployment

### Self-Managed Load Balancers

#### NGINX (`/nginx/documentation`)
- **Trust Score:** High
- **Code Snippets:** 5,762
- **Benchmark Score:** 88.5

**Strengths:**
- Mature, stable, widely adopted
- Good HTTP/1.1, HTTP/2, HTTP/3 support
- Web server + reverse proxy + load balancer
- Excellent documentation
- NGINX Plus: Active health checks, advanced features

**Best For:**
- General-purpose load balancing
- Web application stacks
- HTTP/HTTPS traffic
- Teams familiar with NGINX

**Installation:**
```bash
# Ubuntu/Debian
apt install nginx

# NGINX Plus (commercial)
# Requires license key
```

#### HAProxy (`/haproxy/haproxy`)
- **Trust Score:** High
- **Code Snippets:** 1,020

**Strengths:**
- Highest performance (raw throughput)
- Lowest memory footprint
- Sophisticated health checks
- Advanced algorithms (10+ built-in)
- Excellent for TCP load balancing

**Best For:**
- Maximum performance requirements
- Database load balancing
- Mixed TCP/HTTP workloads
- Cost optimization (resource efficiency)

**Installation:**
```bash
# Ubuntu/Debian
apt install haproxy

# Enterprise edition available
```

#### Envoy (`/envoyproxy/envoy`)
- **Trust Score:** High
- **Code Snippets:** 2,058
- **Benchmark Score:** 77.4

**Strengths:**
- Cloud-native design
- Service mesh integration
- Advanced observability
- Dynamic configuration (xDS APIs)
- Excellent for microservices

**Best For:**
- Kubernetes/microservices
- Service mesh (Istio, Linkerd)
- Modern cloud-native apps
- gRPC heavy workloads

**Installation:**
```bash
# Docker
docker pull envoyproxy/envoy:v1.28-latest

# Kubernetes via Contour/Istio/etc.
```

#### Traefik (`/traefik/traefik`)
- **Trust Score:** High
- **Code Snippets:** 2,466
- **Benchmark Score:** 76.1

**Strengths:**
- Automatic service discovery
- Native Kubernetes integration
- Built-in Let's Encrypt
- Dynamic configuration
- Great for Docker/Kubernetes

**Best For:**
- Docker Swarm/Kubernetes
- Dynamic environments
- Automatic SSL management
- Developers (easy configuration)

**Installation:**
```bash
# Docker
docker run -d -p 80:80 -p 443:443 traefik:v3.0

# Kubernetes
helm install traefik traefik/traefik
```

### Kubernetes Ingress Controllers

| Controller | Snippets | Benchmark | Best For |
|------------|----------|-----------|----------|
| **NGINX Ingress** (F5) | 461 | 83.9 | General purpose |
| **Traefik** | 2,466 | 76.1 | Dynamic environments |
| **HAProxy Ingress** | 462 | N/A | High performance |
| **Envoy Gateway** | 8,780 | 86.4 | Service mesh |
| **Contour** | 10,147 | 82.3 | Production Envoy |

### Load Balancer Comparison Matrix

| Feature | NGINX | HAProxy | Envoy | Traefik | ALB | NLB |
|---------|-------|---------|-------|---------|-----|-----|
| **L4 Support** | ✅ Stream | ✅ Native | ✅ TCP proxy | ✅ TCP | ❌ | ✅ |
| **L7 Support** | ✅ HTTP | ✅ HTTP | ✅ HTTP | ✅ HTTP | ✅ | ❌ |
| **HTTP/3** | ✅ | ❌ | ⚠️ Exp | ✅ | ❌ | ❌ |
| **gRPC** | ✅ | ✅ | ✅✅ | ✅ | ✅ | ✅ |
| **Health Checks** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Performance** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Memory Use** | Low | Lowest | High | Medium | N/A | N/A |
| **K8s Native** | ✅ | ✅ | ✅✅ | ✅✅ | ✅ | ✅ |
| **Config Complexity** | Medium | Medium | High | Low | Low | Low |
| **Dynamic Config** | Plus | No | ✅✅ | ✅✅ | ✅ | ✅ |
| **Cost** | Free/Plus | Free/Ent | Free | Free/Ent | Pay | Pay |

---

## Skill Structure Design

```
load-balancing-patterns/
├── SKILL.md                           # Main skill (500-800 lines)
├── references/
│   ├── l4-vs-l7-comparison.md         # Layer 4 vs Layer 7 deep dive
│   ├── cloud-load-balancers.md        # AWS, GCP, Azure configurations
│   ├── nginx-patterns.md              # NGINX load balancing cookbook
│   ├── haproxy-patterns.md            # HAProxy configuration guide
│   ├── envoy-patterns.md              # Envoy proxy configurations
│   ├── traefik-patterns.md            # Traefik dynamic config
│   ├── health-check-strategies.md     # Health check best practices
│   ├── session-persistence.md         # Sticky sessions and alternatives
│   ├── global-load-balancing.md       # GeoDNS, multi-region patterns
│   └── kubernetes-ingress.md          # Ingress controller comparison
├── examples/
│   ├── aws/
│   │   ├── alb-terraform.tf
│   │   ├── nlb-terraform.tf
│   │   └── global-accelerator.tf
│   ├── nginx/
│   │   ├── http-load-balancing.conf
│   │   ├── tcp-load-balancing.conf
│   │   └── health-checks.conf
│   ├── haproxy/
│   │   ├── http-lb.cfg
│   │   ├── tcp-lb.cfg
│   │   └── health-checks.cfg
│   ├── envoy/
│   │   ├── basic-lb.yaml
│   │   ├── circuit-breaker.yaml
│   │   └── health-checks.yaml
│   ├── traefik/
│   │   ├── docker-compose.yml
│   │   ├── kubernetes-ingress.yaml
│   │   └── middleware.yaml
│   └── kubernetes/
│       ├── nginx-ingress.yaml
│       ├── traefik-ingress.yaml
│       ├── haproxy-ingress.yaml
│       └── gateway-api.yaml
└── scripts/
    ├── validate-lb-config.sh          # Config validation scripts
    ├── test-health-endpoints.sh       # Health check testing
    └── benchmark-lb.sh                # Load testing wrapper
```

---

## Integration Points

### With Existing Skills

| Skill | Integration |
|-------|-------------|
| `infrastructure-as-code` | Deploy load balancers via Terraform/Pulumi |
| `kubernetes-operations` | Ingress controllers for K8s traffic |
| `deploying-applications` | Blue-green, canary via load balancer |
| `observability` | LB metrics, access logs, health checks |
| `security-hardening` | WAF, rate limiting, DDoS protection |
| `service-mesh` | Envoy as both ingress and service mesh |

### Skill Chaining Example

```
infrastructure-as-code → load-balancing-patterns → deploying-applications
        │                        │                         │
        ▼                        ▼                         ▼
  Provision ALB/NLB     Configure health checks    Blue-green deployment
```

---

## Implementation Roadmap

### Phase 1: Core Concepts (Week 1-2)
- [ ] L4 vs L7 comparison and decision framework
- [ ] Cloud load balancer overview (AWS, GCP, Azure)
- [ ] Basic health check patterns

### Phase 2: Self-Managed LBs (Week 3-4)
- [ ] NGINX configuration patterns
- [ ] HAProxy configuration patterns
- [ ] Envoy basic configurations
- [ ] Traefik dynamic configuration

### Phase 3: Advanced Patterns (Week 5-6)
- [ ] Session persistence strategies
- [ ] Global load balancing (GeoDNS)
- [ ] Multi-region failover
- [ ] Connection draining and graceful shutdown

### Phase 4: Kubernetes Integration (Week 7-8)
- [ ] Ingress controller comparison
- [ ] NGINX, Traefik, HAProxy ingress examples
- [ ] Gateway API (future-proof)
- [ ] Certificate management (cert-manager)

### Phase 5: Polish (Week 9)
- [ ] Validation scripts
- [ ] Testing patterns
- [ ] Troubleshooting guide
- [ ] Review and refinement

---

## Key Takeaways

1. **L4 for speed, L7 for smarts** - Choose based on protocol and routing needs
2. **Cloud for convenience, self-managed for control** - Consider team expertise and multi-cloud
3. **Health checks are critical** - Use appropriate depth (shallow vs deep)
4. **Avoid sticky sessions** - Prefer shared session store or client-side tokens
5. **Global load balancing** - GeoDNS + multi-region for worldwide users
6. **Kubernetes ingress** - NGINX for stability, Traefik for ease, Envoy for service mesh
7. **Test failover** - Regularly test health check failover and recovery
8. **Monitor continuously** - Track latency, error rates, connection counts

---

**Progressive disclosure:** This init.md provides the master plan. Detailed configurations and examples in `references/` and `examples/` directories.
