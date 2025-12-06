---
sidebar_position: 9
title: Managing DNS
description: DNS records, TTL strategies, DNS-as-code automation with external-dns
tags: [infrastructure, dns, networking, route53, cloudflare]
---

# Managing DNS

Manage DNS records, TTL strategies, and DNS-as-code automation for infrastructure. Configure domain resolution, automate DNS from Kubernetes, and troubleshoot propagation issues.

## When to Use

Use when:
- Setting up DNS for new applications or services
- Automating DNS updates from Kubernetes workloads
- Configuring DNS-based failover or load balancing
- Troubleshooting DNS propagation or resolution issues
- Migrating DNS between providers
- Planning DNS changes with minimal downtime
- Implementing GeoDNS for global users

## Record Type Selection

### Quick Reference

**Address Resolution:**
- **A Record**: Map hostname to IPv4 address (example.com → 192.0.2.1)
- **AAAA Record**: Map hostname to IPv6 address (example.com → 2001:db8::1)
- **CNAME Record**: Alias to another domain (www.example.com → example.com)
  - Cannot use at zone apex (@)
  - Cannot coexist with other records at same name

**Email Configuration:**
- **MX Record**: Direct email to mail servers with priority
- **TXT Record**: Email authentication (SPF, DKIM, DMARC) and verification

**Service Discovery:**
- **SRV Record**: Specify service location (protocol, priority, weight, port, target)

**Security:**
- **CAA Record**: Restrict which Certificate Authorities can issue certificates

**Cloud-Specific:**
- **ALIAS Record**: Like CNAME but works at zone apex (Route53, Cloudflare)

### Decision Tree

```
Need to point domain to:
├─ IPv4 Address? → A record
├─ IPv6 Address? → AAAA record
├─ Another Domain?
│  ├─ Zone apex (@) → ALIAS/ANAME or A record
│  └─ Subdomain → CNAME
├─ Mail Server? → MX record (with priority)
├─ Email Authentication? → TXT record (SPF/DKIM/DMARC)
├─ Service Discovery? → SRV record
├─ Domain Verification? → TXT record
├─ Certificate Control? → CAA record
└─ Subdomain Delegation? → NS record
```

## TTL Strategy

### Standard TTL Values

**By Change Frequency:**
- **Stable records**: 3600-86400s (1-24 hours) - NS, stable A/AAAA
- **Normal operation**: 3600s (1 hour) - Standard websites, MX
- **Moderate changes**: 300-1800s (5-30 min) - Development, A/B testing
- **Failover scenarios**: 60-300s (1-5 min) - Critical records needing fast updates

**Key Principle:** Lower TTL = faster propagation but higher DNS query load

### Pre-Change Process

When planning DNS changes:

```
T-48h: Lower TTL to 300s
T-24h: Verify TTL propagated globally
T-0h:  Make DNS change
T+1h:  Verify new records propagating
T+6h:  Confirm global propagation
T+24h: Raise TTL back to normal (3600s)
```

**Propagation Formula:** `Max Time = Old TTL + New TTL + Query Time`

## DNS-as-Code Tools

### Tool Selection

**Kubernetes DNS Automation → external-dns**
- Annotation-based configuration on Services/Ingresses
- Automatic sync to DNS providers (20+ supported)
- No manual DNS updates required

**Multi-Provider DNS Management → OctoDNS or DNSControl**
- Version control for DNS records
- Sync configuration across multiple providers
- Preview changes before applying

**Infrastructure-as-Code → Terraform**
- Manage DNS alongside cloud resources
- Provider-specific resources (aws_route53_record, etc.)

### Quick Start: external-dns

```yaml
# Kubernetes Service with DNS annotation
apiVersion: v1
kind: Service
metadata:
  name: app
  annotations:
    external-dns.alpha.kubernetes.io/hostname: app.example.com
    external-dns.alpha.kubernetes.io/ttl: "300"
spec:
  type: LoadBalancer
  ports:
    - port: 80
```

Deploy external-dns controller once, then all annotated Services/Ingresses automatically create DNS records.

## Cloud DNS Provider Selection

### Provider Characteristics

**AWS Route53**
- Best for AWS-heavy infrastructure
- Advanced routing policies (weighted, latency, geolocation, failover)
- Health checks with automatic failover
- Pricing: $0.50/month per zone + $0.40 per million queries

**Google Cloud DNS**
- Best for GCP-native applications
- Strong DNSSEC support with automatic key rotation
- Private zones for VPC internal DNS
- Pricing: $0.20/month per zone + $0.40 per million queries

**Azure DNS**
- Best for Azure-native applications
- Integration with Azure Traffic Manager
- Azure RBAC for access control
- Pricing: $0.50/month per zone + $0.40 per million queries

**Cloudflare**
- Best for multi-cloud or cloud-agnostic
- Fastest DNS query times globally
- Built-in DDoS protection
- Free tier with unlimited queries
- CDN integration

### Selection Decision Tree

```
Choose based on:
├─ AWS-heavy? → Route53
├─ GCP-native? → Cloud DNS
├─ Azure-native? → Azure DNS
├─ Multi-cloud? → Cloudflare or OctoDNS/DNSControl
├─ Need fastest global DNS? → Cloudflare
├─ Need DDoS protection? → Cloudflare
└─ Budget-conscious? → Cloudflare (free tier) or Cloud DNS
```

## DNS-Based Load Balancing

### GeoDNS (Geographic Routing)

Return different IP addresses based on client location to:
- Reduce latency (route to nearest data center)
- Comply with data residency requirements
- Distribute load across regions

**Example Pattern:**
```
Client Location → DNS Response
├─ North America → 192.0.2.1 (US data center)
├─ Europe → 192.0.2.10 (EU data center)
└─ Default → CloudFront edge (global CDN)
```

### Weighted Routing

Distribute traffic by percentage for:
- Blue-green deployments
- Canary releases (10% to new version)
- A/B testing

### Health Check-Based Failover

Automatically route traffic away from unhealthy endpoints.

**Pattern:**
```
Primary: 192.0.2.1 (health checked every 30s)
├─ Healthy → Return primary IP
└─ Unhealthy → Return secondary IP (192.0.2.2)

Failover time: ~2-3 minutes
= Health check failures (90s) + TTL expiration (60s)
```

## Troubleshooting

### Essential Commands

```bash
# Basic query
dig example.com

# Clean output (just IP)
dig example.com +short

# Query specific DNS server
dig @8.8.8.8 example.com
dig @1.1.1.1 example.com

# Trace resolution path
dig +trace example.com

# Check TTL
dig example.com | grep -A1 "ANSWER SECTION"
```

### Check Propagation

```bash
# Multiple resolvers
dig @8.8.8.8 example.com +short       # Google
dig @1.1.1.1 example.com +short       # Cloudflare
dig @208.67.222.222 example.com +short # OpenDNS
```

### Flush Local DNS Cache

```bash
# macOS
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder

# Windows
ipconfig /flushdns

# Linux
sudo systemd-resolve --flush-caches
```

### Common Problems

**Slow Propagation:**
- Check current TTL (old TTL must expire first)
- Lower TTL 24-48 hours before changes
- Use propagation checkers: whatsmydns.net, dnschecker.org

**CNAME at Zone Apex:**
- Error: Cannot use CNAME at @ (zone apex)
- Solution: Use ALIAS record (Route53, Cloudflare) or A record

**external-dns Not Creating Records:**
- Verify annotation spelling: `external-dns.alpha.kubernetes.io/hostname`
- Check domain filter matches: `--domain-filter=example.com`
- Review external-dns logs for errors
- Confirm provider credentials configured

## Quick Reference

### Record Types Cheat Sheet

| Record | Purpose | Example |
|--------|---------|---------|
| A | IPv4 address | example.com → 192.0.2.1 |
| AAAA | IPv6 address | example.com → 2001:db8::1 |
| CNAME | Alias to domain | www → example.com |
| MX | Mail server | 10 mail.example.com |
| TXT | Text/verification | "v=spf1 include:_spf.google.com ~all" |
| SRV | Service location | 10 60 5060 sip.example.com |
| CAA | CA authorization | 0 issue "letsencrypt.org" |

### TTL Cheat Sheet

| Scenario | TTL | Why |
|----------|-----|-----|
| Stable production | 3600s | Balance speed/load |
| Before change | 300s | Fast propagation |
| Failover | 60-300s | Fast recovery |
| NS records | 86400s | Very stable |

## Related Skills

- [Writing Infrastructure Code](./writing-infrastructure-code) - Manage DNS via Terraform/Pulumi
- [Operating Kubernetes](./operating-kubernetes) - external-dns for K8s workloads
- [Load Balancing Patterns](./load-balancing-patterns) - DNS-based load balancing
- [Architecting Networks](./architecting-networks) - Network design and DNS integration

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/managing-dns)
- Record Types: `references/record-types.md`
- TTL Strategies: `references/ttl-strategies.md`
- Cloud Providers: `references/cloud-providers.md`
- DNS-as-Code Comparison: `references/dns-as-code-comparison.md`
- Troubleshooting: `references/troubleshooting.md`
