# AWS Networking - Deep Dive


## Table of Contents

- [VPC Architecture](#vpc-architecture)
  - [Standard 3-Tier Pattern](#standard-3-tier-pattern)
  - [Security Groups vs. NACLs](#security-groups-vs-nacls)
  - [NAT Gateway](#nat-gateway)
- [Load Balancers](#load-balancers)
  - [Application Load Balancer (ALB)](#application-load-balancer-alb)
  - [Network Load Balancer (NLB)](#network-load-balancer-nlb)
- [CloudFront (CDN)](#cloudfront-cdn)
- [Route 53 (DNS)](#route-53-dns)
  - [Routing Policies](#routing-policies)
- [VPC Peering](#vpc-peering)
- [PrivateLink](#privatelink)
- [Transit Gateway](#transit-gateway)

## VPC Architecture

### Standard 3-Tier Pattern

```
VPC: 10.0.0.0/16 (65,536 IPs)

Availability Zone A:
  Public Subnet:    10.0.1.0/24  (256 IPs: ALB, NAT Gateway, Bastion)
  Private Subnet:   10.0.11.0/24 (256 IPs: ECS, Lambda, App Servers)
  Database Subnet:  10.0.21.0/24 (256 IPs: RDS, Aurora, ElastiCache)

Availability Zone B:
  Public Subnet:    10.0.2.0/24
  Private Subnet:   10.0.12.0/24
  Database Subnet:  10.0.22.0/24

Availability Zone C:
  Public Subnet:    10.0.3.0/24
  Private Subnet:   10.0.13.0/24
  Database Subnet:  10.0.23.0/24
```

### Security Groups vs. NACLs

| Feature | Security Groups | Network ACLs |
|---------|----------------|--------------|
| **Level** | Instance (ENI) | Subnet |
| **State** | Stateful | Stateless |
| **Rules** | Allow only | Allow + Deny |
| **Return Traffic** | Automatic | Must configure |
| **Evaluation** | All rules | Numbered order |

### NAT Gateway

**Purpose:** Enable private subnet instances to access internet for updates, APIs

**Cost (us-east-1):**
- $0.045/hour = $32.85/month
- $0.045/GB processed
- Deploy one per AZ for HA

**Alternative:** NAT Instance (EC2) - cheaper but manual management

---

## Load Balancers

### Application Load Balancer (ALB)

**Features:**
- Layer 7 (HTTP/HTTPS)
- Path-based routing: `/api` → backend, `/web` → frontend
- Host-based routing: `api.example.com`, `web.example.com`
- WebSocket support
- Lambda targets (serverless backends)
- HTTP/2, gRPC support

**Cost:**
- $0.0225/hour = $16.43/month
- $0.008/LCU-hour (Load Balancer Capacity Unit)
- Minimum ~$20/month

### Network Load Balancer (NLB)

**Features:**
- Layer 4 (TCP/UDP)
- Ultra-low latency (<100 microseconds)
- Millions of requests/second
- Static IP addresses (Elastic IP)
- PrivateLink support

**Cost:**
- $0.0225/hour = $16.43/month
- $0.006/NLCU-hour

**Use When:**
- Extreme performance needed
- Static IPs required
- Non-HTTP protocols

---

## CloudFront (CDN)

**Purpose:** Global content delivery network with 450+ edge locations

**Features:**
- Cache static content (images, CSS, JS)
- Dynamic content acceleration
- DDoS protection (AWS Shield)
- Lambda@Edge for edge compute

**Cost:**
- Data transfer: $0.085/GB (first 10TB, decreases)
- Requests: $0.0075 per 10,000
- Free tier: 1TB transfer, 10M requests/month (12 months)

**Cache Behaviors:**
- Match path patterns: `/images/*`, `/api/*`
- TTL configuration per pattern
- Origin types: S3, ALB, custom

---

## Route 53 (DNS)

### Routing Policies

| Policy | Use Case |
|--------|----------|
| **Simple** | Single resource |
| **Weighted** | A/B testing, gradual migration (10% → 90%) |
| **Latency** | Route to lowest-latency region |
| **Failover** | Active-passive disaster recovery |
| **Geolocation** | Route based on user location |
| **Geoproximity** | Route based on resource location + bias |
| **Multi-value** | Return multiple IPs with health checks |

**Cost:**
- Hosted zone: $0.50/month
- Queries: $0.40 per million
- Health checks: $0.50/month each

---

## VPC Peering

**Purpose:** Connect two VPCs privately (same region or cross-region)

**Characteristics:**
- Non-transitive (A↔B, B↔C doesn't mean A↔C)
- No overlapping CIDR blocks
- Data transfer: $0.01/GB (same region), $0.02/GB (cross-region)

---

## PrivateLink

**Purpose:** Privately access AWS services or third-party services

**Use Cases:**
- Access S3, DynamoDB without internet gateway
- SaaS vendor connections
- Shared services across accounts

**Cost:**
- $0.01/hour per AZ = $7.30/month per AZ
- $0.01/GB processed

---

## Transit Gateway

**Purpose:** Hub-and-spoke network architecture for 100s of VPCs

**Features:**
- Connect VPCs, on-premises networks (VPN, Direct Connect)
- Transitive routing
- Route table customization

**Cost:**
- $0.05/hour per attachment = $36.50/month
- $0.02/GB processed

**Use When:**
- >5 VPCs to connect
- Need centralized routing
- Hybrid cloud architecture
