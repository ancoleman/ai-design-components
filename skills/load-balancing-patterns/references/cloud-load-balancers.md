# Cloud Load Balancers

Complete configurations for AWS, GCP, and Azure managed load balancing services.


## Table of Contents

- [AWS Load Balancers](#aws-load-balancers)
  - [Application Load Balancer (ALB)](#application-load-balancer-alb)
  - [Network Load Balancer (NLB)](#network-load-balancer-nlb)
  - [Global Accelerator](#global-accelerator)
- [GCP Load Balancing](#gcp-load-balancing)
  - [Application Load Balancer](#application-load-balancer)
  - [Network Load Balancer](#network-load-balancer)
  - [Cloud Load Balancing](#cloud-load-balancing)
- [Azure Load Balancing](#azure-load-balancing)
  - [Application Gateway](#application-gateway)
  - [Load Balancer](#load-balancer)
  - [Traffic Manager](#traffic-manager)
- [Cost Comparison](#cost-comparison)
- [Selection Guide](#selection-guide)
- [Multi-Cloud Considerations](#multi-cloud-considerations)

## AWS Load Balancers

### Application Load Balancer (ALB)

Layer 7 HTTP/HTTPS load balancer with advanced routing capabilities.

**Use cases:**
- Web applications
- Microservices
- Container-based applications
- Lambda functions

**Key features:**
- Path-based routing (`/api/*` → API servers)
- Host-based routing (`api.example.com` → API servers)
- HTTP header routing
- Query string parameter routing
- WebSocket support
- HTTP/2 and gRPC support
- AWS WAF integration
- Cognito authentication

**Terraform example:** See `examples/aws/alb-terraform.tf`

### Network Load Balancer (NLB)

Layer 4 TCP/UDP load balancer for ultra-low latency and high throughput.

**Use cases:**
- Non-HTTP protocols
- Static IP addresses required
- Extreme performance requirements (millions RPS)
- Client IP preservation critical

**Key features:**
- Static IP per availability zone
- Elastic IP support
- Preserves source client IP
- TLS termination
- Cross-zone load balancing
- PrivateLink support

**Terraform example:** See `examples/aws/nlb-terraform.tf`

### Global Accelerator

Global Layer 4 load balancer using AWS global network.

**Use cases:**
- Multi-region applications
- Global user base
- DDoS protection
- Automatic regional failover

**Key features:**
- Two static anycast IP addresses
- AWS Shield Standard DDoS protection
- Health checks per endpoint
- Traffic dials (gradual migration)
- Integration with ALB, NLB, EC2, EIP

## GCP Load Balancing

### Application Load Balancer

Global Layer 7 load balancer.

**Types:**
- External Application Load Balancer (global)
- Internal Application Load Balancer (regional)
- Regional External Application Load Balancer

**Key features:**
- URL map-based routing
- Cloud CDN integration
- Cloud Armor (WAF and DDoS)
- SSL policies and certificates
- Backend services with health checks

### Network Load Balancer

Regional Layer 4 load balancer.

**Types:**
- External passthrough Network Load Balancer
- Internal passthrough Network Load Balancer

**Key features:**
- TCP/UDP load balancing
- Preserves client IP
- Regional or zonal backends
- Session affinity

### Cloud Load Balancing

Global load balancing service with single anycast IP.

**Key features:**
- Single global anycast IP
- Cross-region load balancing
- Automatic multi-region failover
- Backend buckets (Cloud Storage)

## Azure Load Balancing

### Application Gateway

Layer 7 web traffic load balancer.

**Key features:**
- WAF integration (Web Application Firewall)
- URL-based routing
- Multi-site hosting
- SSL termination and end-to-end SSL
- Autoscaling
- Zone redundancy
- Rewrite HTTP headers and URL

### Load Balancer

Layer 4 network load balancer.

**SKUs:**
- **Basic:** Simple load balancing, free tier
- **Standard:** Production-ready with zone redundancy

**Key features:**
- TCP/UDP load balancing
- Health probes (TCP, HTTP, HTTPS)
- Outbound rules
- HA ports
- Multiple frontends
- Zone redundant

### Traffic Manager

DNS-based global load balancer.

**Routing methods:**
- **Priority:** Failover routing
- **Weighted:** Distribute across endpoints
- **Performance:** Lowest latency endpoint
- **Geographic:** Based on DNS location
- **MultiValue:** Return multiple healthy endpoints
- **Subnet:** Based on client subnet

## Cost Comparison

| Provider | L4 Solution | L7 Solution | Pricing Model |
|----------|-------------|-------------|---------------|
| AWS | NLB | ALB | Per hour + LCU (capacity units) |
| GCP | Network LB | Application LB | Per hour + forwarding rules |
| Azure | Load Balancer | Application Gateway | Per hour + data processed |

## Selection Guide

**Choose AWS ALB when:**
- HTTP/HTTPS applications
- Need AWS WAF integration
- Lambda as backend targets
- Path-based microservices routing

**Choose AWS NLB when:**
- Non-HTTP protocols
- Static IPs required
- Ultra-low latency critical
- High throughput needs

**Choose GCP Application LB when:**
- Global HTTP(S) load balancing
- Cloud CDN integration needed
- Cloud Armor for DDoS/WAF

**Choose Azure Application Gateway when:**
- Azure-native web applications
- WAF required
- URL rewriting needed

## Multi-Cloud Considerations

For multi-cloud deployments, consider:
- Self-managed load balancers (NGINX, HAProxy)
- Cloud-agnostic tools (Traefik, Envoy)
- DNS-based global load balancing
- Avoid cloud-specific features that lock you in

Complete configuration examples available in `examples/aws/`, `examples/gcp/`, and `examples/azure/` directories.
