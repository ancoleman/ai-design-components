# Layer 4 vs Layer 7 Load Balancing Comparison

Comprehensive comparison of transport layer (L4) and application layer (L7) load balancing to guide architecture decisions.

## Table of Contents

1. [Fundamental Differences](#fundamental-differences)
2. [L4 Load Balancing Deep Dive](#l4-load-balancing-deep-dive)
3. [L7 Load Balancing Deep Dive](#l7-load-balancing-deep-dive)
4. [Performance Comparison](#performance-comparison)
5. [Use Case Decision Matrix](#use-case-decision-matrix)
6. [Hybrid Approaches](#hybrid-approaches)

## Fundamental Differences

### OSI Layer Operation

**Layer 4 (Transport Layer):**
- Operates on TCP/UDP packets
- Routing decisions based on: Source IP, destination IP, source port, destination port
- No visibility into application data
- No understanding of HTTP, headers, URLs

**Layer 7 (Application Layer):**
- Operates on HTTP/HTTPS requests
- Routing decisions based on: URLs, headers, cookies, request method, request body
- Full visibility into application data
- Understands HTTP semantics

### Packet Inspection Depth

**L4 Load Balancer Visibility:**
```
IP Header: Source IP, Dest IP
TCP Header: Source Port, Dest Port, Flags
Payload: [OPAQUE - Not inspected]
```

**L7 Load Balancer Visibility:**
```
IP Header: Source IP, Dest IP
TCP Header: Source Port, Dest Port
HTTP Request:
  Method: GET, POST, PUT, DELETE
  URL: /api/users/123
  Headers: Host, User-Agent, Authorization
  Cookies: session_id=abc123
  Body: {"key": "value"}
```

### Connection Handling

**L4 Connection Model:**
```
Client ←→ L4 LB ←→ Backend Server
      [Single TCP connection passed through]
```
- Connection forwarding (not termination)
- Client IP preserved
- No SSL termination at LB

**L7 Connection Model:**
```
Client ←→ L7 LB    L7 LB ←→ Backend Server
      [Connection 1]  [Connection 2]
```
- Two separate connections
- LB terminates client connection
- LB initiates new connection to backend
- Client IP in `X-Forwarded-For` header

## L4 Load Balancing Deep Dive

### Routing Mechanisms

**TCP Connection Forwarding:**
1. Client initiates TCP handshake with LB
2. LB selects backend based on algorithm
3. LB forwards packets to backend (NAT mode) or routes directly (DSR mode)
4. Backend sees client IP (DSR) or LB IP (NAT)

**NAT Mode (Network Address Translation):**
```
Client (1.2.3.4) → LB (10.0.0.5) → Backend
Backend sees source: 10.0.0.5
Response: Backend → LB → Client
```

**DSR Mode (Direct Server Return):**
```
Client (1.2.3.4) → LB → Backend
Backend sees source: 1.2.3.4
Response: Backend → Client (bypasses LB)
```

### Performance Characteristics

**Throughput:**
- Handles millions of requests per second
- Minimal CPU overhead (no deep packet inspection)
- Example: AWS NLB handles 100M+ requests per second

**Latency:**
- Sub-millisecond latency added
- No SSL handshake at LB (passthrough)
- Faster than L7 by 2-10x

**Resource Usage:**
- Low memory footprint
- Minimal CPU per connection
- Can handle 100K+ concurrent connections per instance

### L4 Algorithms

**IP Hash (Source IP):**
```
hash(client_ip) % num_servers → server_index
```
- Provides natural stickiness
- Poor distribution with NAT/proxies
- No application awareness

**Random Selection:**
```
random() % num_servers → server_index
```
- Simple, fast
- Good distribution over time
- No session affinity

**Least Connections (TCP):**
```
select server with min(active_connections)
```
- Tracks TCP connection count
- Better than round-robin for varying request durations
- Small overhead for connection tracking

### L4 Use Cases

**Database Load Balancing:**
- MySQL, PostgreSQL connection pooling
- Protocol: TCP (not HTTP)
- Client IP preservation important for auditing
- High throughput, low latency critical

**Real-Time Protocols:**
- Video streaming (RTMP, RTP)
- Gaming servers (UDP)
- VoIP (SIP, H.323)
- WebRTC signaling

**Financial Trading Systems:**
- Ultra-low latency required (microseconds matter)
- High message throughput
- TCP-based proprietary protocols

**IoT Device Communication:**
- MQTT (TCP port 1883)
- CoAP (UDP)
- Millions of concurrent connections
- Non-HTTP protocols

## L7 Load Balancing Deep Dive

### Routing Mechanisms

**URL Path-Based Routing:**
```
/api/*     → API backend pool
/static/*  → CDN/static file servers
/admin/*   → Admin backend pool
/*         → Default web backend
```

**Host-Based Routing:**
```
api.example.com  → API servers
www.example.com  → Web servers
admin.example.com → Admin servers
```

**Header-Based Routing:**
```
Header: X-API-Version: v2 → API v2 servers
Header: X-Mobile: true    → Mobile backend
Header: Authorization: *  → Authenticated pool
```

**Cookie-Based Routing:**
```
Cookie: beta_user=true    → Beta features backend
Cookie: region=us-east    → Regional backend
Cookie: session_id=*      → Sticky session routing
```

**Query Parameter Routing:**
```
?version=2     → API v2
?locale=en-US  → US backend
?debug=true    → Debug servers
```

### Advanced L7 Features

**SSL/TLS Termination:**
- LB handles SSL handshake
- Decrypts HTTPS traffic
- Inspects plaintext HTTP
- Re-encrypts to backend (optional)
- Offloads CPU from application servers

**Request/Response Transformation:**
- Add/remove headers
- Rewrite URLs
- Inject custom headers (`X-Forwarded-For`, `X-Real-IP`)
- Response header modification

**Content Caching:**
- Cache static responses at LB
- Reduce backend load
- Faster response times
- Cache invalidation support

**Web Application Firewall (WAF):**
- SQL injection prevention
- XSS attack blocking
- Rate limiting per client
- Bot detection
- Geographic blocking

**Authentication/Authorization:**
- OAuth/JWT validation at LB
- API key verification
- Client certificate validation
- Integration with identity providers

### L7 Algorithms

**URL Hash:**
```
hash(request_url) % num_servers → server_index
```
- Cache affinity for CDN origins
- Consistent routing for specific URLs

**Cookie-Based Affinity:**
```
if cookie_exists(SERVER_ID):
    route to cookie_value
else:
    server = select_server()
    set_cookie(SERVER_ID, server)
```

**Least Request (Application-Aware):**
```
select server with min(active_requests)
```
- Counts HTTP requests (not just connections)
- Better than least connections for HTTP/2 multiplexing

**Weighted Response Time:**
```
select server with min(avg_response_time * weight)
```
- Performance-based routing
- Adapts to server health dynamically

### L7 Use Cases

**Microservices Architecture:**
```
/users/*     → User service
/products/*  → Product service
/orders/*    → Order service
/payments/*  → Payment service
```
- Different services on different paths
- Service-specific routing
- Canary deployments per service

**Multi-Tenant SaaS:**
```
tenant1.saas.com → Tenant 1 database shard
tenant2.saas.com → Tenant 2 database shard
```
- Host-based tenant isolation
- Per-tenant routing

**A/B Testing:**
```
Cookie: experiment=B → Variant B servers (10%)
Default              → Variant A servers (90%)
```
- Traffic splitting for experiments
- User-consistent experience

**Geographic Content Delivery:**
```
Header: Accept-Language: es → Spanish content servers
Header: Accept-Language: en → English content servers
```
- Language-based routing
- Regional compliance

## Performance Comparison

### Latency Comparison

| Operation | L4 Latency | L7 Latency | Difference |
|-----------|------------|------------|------------|
| Connection setup | <1ms | 2-5ms | 2-5x slower |
| Request routing | <0.1ms | 0.5-2ms | 5-20x slower |
| SSL termination | N/A (passthrough) | 5-10ms | L7 overhead |
| Total overhead | 1-2ms | 7-17ms | 3-8x slower |

### Throughput Comparison

| Load Balancer | Requests/Second | Connections | Notes |
|---------------|----------------|-------------|-------|
| AWS NLB (L4) | 100M+ | Millions | Ultra-high throughput |
| AWS ALB (L7) | 1M+ | 100K+ | Lower due to HTTP parsing |
| HAProxy (L4) | 1M+ | 500K+ | Optimized C implementation |
| HAProxy (L7) | 200K-500K | 100K+ | HTTP processing overhead |
| NGINX (L7) | 100K-300K | 50K+ | General purpose |
| Envoy (L7) | 50K-150K | 30K+ | Feature-rich, more overhead |

### Resource Usage

**L4 Load Balancer:**
- Memory: ~1KB per connection
- CPU: <1% per 10K connections
- Can run on small instances (2 vCPU, 4GB RAM)

**L7 Load Balancer:**
- Memory: ~10KB per connection (HTTP parsing, buffering)
- CPU: 5-10% per 10K requests/second
- Requires larger instances (4+ vCPU, 8+ GB RAM)

## Use Case Decision Matrix

### Choose L4 When:

**Protocol is not HTTP:**
- Database connections (MySQL, PostgreSQL, MongoDB)
- Message queues (RabbitMQ, Redis, Kafka)
- Custom TCP/UDP protocols
- Legacy applications

**Performance is critical:**
- Financial trading systems
- Real-time gaming
- Video streaming
- High-frequency APIs

**Client IP preservation required:**
- Security logging and auditing
- Geographic restriction enforcement
- Rate limiting by client IP
- Legacy applications expecting client IP

**Simplicity preferred:**
- No advanced routing needed
- Simple round-robin sufficient
- Minimize configuration complexity

### Choose L7 When:

**HTTP/HTTPS traffic:**
- Web applications
- REST APIs
- GraphQL services
- gRPC (HTTP/2 based)

**Content-based routing needed:**
- Microservices on different paths
- Multi-tenant applications
- A/B testing
- Canary deployments

**SSL termination required:**
- Certificate management at LB
- Decrypt traffic for inspection
- Reduce backend SSL overhead

**Advanced features needed:**
- WAF integration
- Caching at LB
- Request transformation
- Authentication at LB

**Application intelligence wanted:**
- Session affinity based on cookies
- Routing based on headers
- Response transformation
- Health checks with body validation

## Hybrid Approaches

### L4 + L7 Chaining

**Architecture:**
```
Internet → L4 NLB → L7 ALB → Application Servers
          (DDoS)    (Routing)
```

**Benefits:**
- L4 absorbs volumetric DDoS attacks
- Static IP addresses from NLB
- L7 provides intelligent routing
- Best of both worlds

**AWS Example:**
```
NLB (Layer 4):
  - Static IP per AZ
  - DDoS protection
  - High throughput

ALB (Layer 7) as NLB target:
  - Path-based routing
  - Host-based routing
  - WAF integration
```

### Regional L4 + Global L7

**Architecture:**
```
Global DNS → CloudFlare (L7 Global) → Regional NLB (L4) → Apps
            [WAF, DDoS, caching]      [High performance]
```

**Benefits:**
- Global L7 for edge caching and security
- Regional L4 for low-latency local routing
- Optimal performance and protection

### L4 for Internal, L7 for External

**Architecture:**
```
External clients → L7 ALB → Application
Internal services → L4 NLB → Application
```

**Rationale:**
- External needs WAF, SSL termination, content routing
- Internal needs high throughput, low latency
- Different requirements warrant different LBs

## Summary

**L4 strengths:** Performance, simplicity, protocol agnostic, low latency
**L7 strengths:** Intelligent routing, security features, HTTP awareness, flexibility

**Decision guideline:** Default to L7 for HTTP applications unless performance requirements demand L4. Consider hybrid approaches for large-scale deployments.
