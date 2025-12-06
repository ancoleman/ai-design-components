---
sidebar_position: 7
title: DNS Management
description: Master plan for DNS automation including record types, TTL strategies, DNS as code, cloud DNS services, and load balancing
tags: [master-plan, infrastructure, dns, route53, cloudflare]
---

# DNS Management

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

DNS is the internet's phone book and a critical infrastructure component. This skill covers DNS record types, TTL strategies, DNS automation (DNS as code), cloud DNS services, DNS-based load balancing, and troubleshooting patterns.

## Scope

This skill teaches:

- **Record Type Selection** - A, AAAA, CNAME, MX, TXT, SRV, CAA, NS (when to use each)
- **TTL Strategies** - Balancing propagation speed vs query load
- **DNS as Code** - Automating DNS with external-dns, OctoDNS, DNSControl
- **Cloud DNS Services** - Route53, Cloud DNS, Azure DNS, Cloudflare
- **Load Balancing Patterns** - GeoDNS, health checks, weighted routing, failover
- **Troubleshooting** - dig, nslookup, DNS propagation tools

## Key Components

### DNS Record Types

| Record | Purpose | Example |
|--------|---------|---------|
| **A** | IPv4 address | `example.com` → `192.0.2.1` |
| **AAAA** | IPv6 address | `example.com` → `2001:db8::1` |
| **CNAME** | Canonical name (alias) | `www.example.com` → `example.com` |
| **MX** | Mail exchange | `example.com` → `mail.example.com` |
| **TXT** | Text record (SPF, DKIM, verification) | Various |
| **SRV** | Service locator | `_service._proto.name` → `target:port` |
| **CAA** | Certificate authority authorization | SSL/TLS issuance control |
| **NS** | Name server | Delegation to authoritative servers |

### TTL Best Practices (2025)

**General Recommendations:**
- **24 hours (86,400s)**: Standard for stable records
- **1-4 hours**: Balanced approach for most websites
- **5 minutes (300s)**: Critical records, failover scenarios
- **Before changes**: Lower TTL 24-48 hours in advance

**Critical Findings:**
- Never set TTL to 0 (minimum 3600s recommended)
- Maximum practical TTL: 86,400s (24 hours)
- Lower TTL = more queries = higher load on authoritative servers
- Plan changes during off-peak hours

### DNS Automation (Kubernetes Focus)

**ExternalDNS** - Kubernetes DNS Automation
- **Library**: `/kubernetes-sigs/external-dns`
- **Trust Score**: High, 671+ code snippets
- Monitors Services/Ingresses for DNS annotations
- Syncs with 20+ DNS providers (Route53, Cloud DNS, Cloudflare)
- Eliminates manual DNS updates for dynamic workloads
- GitOps-friendly deployment patterns

**OctoDNS** - Multi-provider DNS management
**DNSControl** - DNS as code with version control

## Decision Framework

**Which DNS Provider?**

```
AWS-heavy environment?
  YES → Route53 (tight AWS integration)

Multi-cloud or cloud-agnostic?
  YES → Need DDoS protection?
          YES → Cloudflare (DDoS + CDN included)
          NO → Cloudflare or Route53 (both strong)

Performance critical?
  YES → Cloudflare (fastest DNS globally)

Enterprise compliance/control?
  YES → Route53 or Azure DNS (SLA, support)

Cost-sensitive?
  YES → Cloudflare (free tier available)
```

**TTL Selection:**

```
Production system?
  YES → Changing soon?
          YES → 300s (5 minutes)
          NO → 3600-14400s (1-4 hours)

Development/staging?
  YES → 300s (frequent changes expected)

Critical infrastructure?
  YES → 300-900s (fast failover)

Static content?
  YES → 86400s (24 hours, reduce load)
```

## Tool Recommendations

### Cloud DNS Services

**Route53 (AWS)**
- Tight AWS integration
- Latency-based, geolocation, weighted routing
- Health checks and failover
- Pricing: per-query model

**Cloudflare**
- Fastest DNS query speed globally
- Geo Steering (load balancing feature)
- Platform-agnostic
- DDoS protection included
- Pricing: subscription-based load balancing

**GCP Cloud DNS / Azure DNS**
- Cloud-native integration
- Managed DNS zones
- Private DNS for internal resolution

### DNS Automation Tools

**ExternalDNS** - Kubernetes DNS sync
**OctoDNS** - Multi-provider management
**DNSControl** - DNS as code (GitOps)
**Terraform/Pulumi** - IaC for DNS records

### Troubleshooting Tools

```bash
# Query DNS record
dig example.com A +short

# Trace DNS path
dig example.com +trace

# Query specific nameserver
dig @8.8.8.8 example.com

# Check propagation
nslookup example.com
```

## Integration Points

**With Other Skills:**
- `writing-infrastructure-code` - Terraform/Pulumi for DNS provisioning
- `operating-kubernetes` - ExternalDNS for K8s automation
- `load-balancing-patterns` - DNS-based load balancing, GeoDNS
- `security-hardening` - DNSSEC, CAA records, DNS filtering
- `architecting-networks` - Split-horizon DNS, hybrid DNS

**Workflow Example:**
```
Git → CI/CD → DNS as Code → Provider API
  │      │         │              │
  ▼      ▼         ▼              ▼
Change Review  OctoDNS/     Route53/
commit         external-dns  Cloudflare
```

## Learn More

- [Full Master Plan (init.md)](https://github.com/ancoleman/ai-design-components/blob/main/skills/managing-dns/init.md)
- Related: `load-balancing-patterns`, `operating-kubernetes`, `writing-infrastructure-code`
