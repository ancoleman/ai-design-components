# DNS Management Skill - Master Plan

**Skill Name:** `dns-management`
**Level:** Mid Level (5,000-8,000 tokens, 500-800 lines)
**Status:** Planning Phase
**Created:** 2025-12-03
**Last Updated:** 2025-12-03

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [DNS Management Taxonomy](#dns-management-taxonomy)
5. [Decision Framework](#decision-framework)
6. [Record Type Patterns](#record-type-patterns)
7. [TTL Strategy Guide](#ttl-strategy-guide)
8. [DNS as Code](#dns-as-code)
9. [Cloud DNS Services](#cloud-dns-services)
10. [DNS-Based Load Balancing](#dns-based-load-balancing)
11. [Troubleshooting Guide](#troubleshooting-guide)
12. [Tool Recommendations](#tool-recommendations)
13. [Skill Structure Design](#skill-structure-design)
14. [Integration Points](#integration-points)
15. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why DNS Management Matters

DNS is the internet's phone book, but it's also a critical component of modern infrastructure:

**Business Impact:**
- **Availability**: DNS failures = complete service outage
- **Performance**: Improper TTL = slow updates or excessive queries
- **Security**: DNS hijacking, cache poisoning, DDoS attacks
- **Cost**: Inefficient DNS = wasted API calls and traffic

**Technical Complexity:**
- Record types (A, AAAA, CNAME, MX, TXT, SRV, CAA, NS)
- TTL strategies (propagation vs caching)
- Multi-provider management (AWS, GCP, Azure, Cloudflare)
- Automation patterns (external-dns, OctoDNS, DNSControl)
- Load balancing (GeoDNS, health checks, failover)

**Common Pain Points:**
1. **Manual DNS updates** - Error-prone, slow, doesn't scale
2. **Propagation delays** - Not understanding TTL impact
3. **Split-horizon DNS** - Different records for internal/external
4. **Multi-cloud complexity** - Managing DNS across providers
5. **Lack of version control** - No audit trail for DNS changes

### Where DNS Management Fits

**Complements:**
- `infrastructure-as-code` - DNS is part of IaC (Terraform, Pulumi)
- `kubernetes-operations` - external-dns automates K8s → DNS
- `load-balancing-patterns` - DNS-based LB and failover
- `security-hardening` - DNSSEC, CAA records, DNS filtering

**Does NOT Cover:**
- Network architecture (routing, subnets, VPCs)
- Certificate management (see `secret-management`)
- Full CDN configuration (only DNS aspects)
- Application-level load balancing (Layer 7)

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**
1. **Record Type Selection** - Which record for which use case
2. **TTL Strategies** - Balancing propagation speed vs query load
3. **DNS as Code** - Automating DNS with external-dns, OctoDNS, DNSControl
4. **Cloud DNS Services** - Route53, Cloud DNS, Azure DNS, Cloudflare
5. **Load Balancing Patterns** - GeoDNS, health checks, weighted routing
6. **Troubleshooting** - dig, nslookup, DNS propagation tools

### When to Use This Skill

**Trigger Scenarios:**
- "Set up DNS for my application"
- "Automate DNS updates from Kubernetes"
- "Configure failover using DNS"
- "Migrate DNS between providers"
- "Why is DNS propagation taking so long?"
- "How do I set up GeoDNS for global users?"
- "What TTL should I use?"

### Out of Scope

**Not Covered:**
- DNS server implementation (BIND, PowerDNS, CoreDNS internals)
- Full network security (firewalls, WAF, DDoS mitigation)
- Email deliverability optimization (SPF/DKIM/DMARC deep dive)
- Domain registration and transfer processes

---

## Research Findings

### Research Date: 2025-12-03

**Research Tools Used:**
- Google Search Grounding (Vertex AI)
- Context7 Library Documentation

### Key Research Insights

#### 1. TTL Best Practices (2025)

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

**Source:** ionos.ca, phoenixnap.com, runcloud.io, catchpoint.com

#### 2. DNS Automation (Kubernetes Focus)

**ExternalDNS (2025 Status):**
- Kubernetes controller for automatic DNS management
- Monitors Services/Ingresses for DNS annotations
- Syncs with external DNS providers (Route53, Cloud DNS, Cloudflare)
- Eliminates manual DNS updates for dynamic workloads

**Key Benefits:**
- Real-time synchronization (no manual updates)
- Reduces configuration drift
- Supports 20+ DNS providers
- GitOps-friendly deployment patterns

**Source:** medium.com, komodor.com, containerinfra.com

#### 3. DNS-Based Load Balancing (2025 Landscape)

**Leading Solutions:**

**Route53 (AWS):**
- Tight AWS integration
- Latency-based, geolocation, weighted routing
- Health checks and failover
- Pricing: per-query model

**Cloudflare:**
- Fastest DNS query speed globally
- Geo Steering (load balancing feature)
- Platform-agnostic
- DDoS protection included
- Pricing: subscription-based load balancing

**Key Considerations:**
- Route53: Best for AWS-heavy environments
- Cloudflare: Best for performance and simplicity
- Both offer robust GeoDNS capabilities

**Source:** cloudflare.com, mattgadient.com, dev.to, runcloud.io

### Library Research Results

#### Primary: ExternalDNS (Kubernetes DNS Automation)

**Library:** `/kubernetes-sigs/external-dns`
**Trust Score:** High
**Code Snippets:** 671+
**Source Reputation:** High

**Why ExternalDNS?**
- Industry standard for Kubernetes DNS automation
- Supports 20+ DNS providers (AWS, GCP, Azure, Cloudflare)
- Annotation-based configuration (no CRDs required)
- TTL control via annotations
- Active maintenance (Kubernetes SIG project)

**When to Use:**
- Running Kubernetes workloads
- Need automatic DNS updates on service changes
- Multi-cluster DNS management
- GitOps workflows

**Example Configuration:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  annotations:
    external-dns.alpha.kubernetes.io/hostname: example.com
    external-dns.alpha.kubernetes.io/ttl: "300"
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
    - port: 80
```

**Provider Support:**
- AWS Route53: ✅ (TTL, alias records, health checks)
- GCP Cloud DNS: ✅ (TTL, geo-routing)
- Azure DNS: ✅ (TTL 1-2,147,483,647s, default 300s)
- Cloudflare: ✅ (TTL auto mode support)
- 16+ additional providers

---

#### Alternative 1: OctoDNS (Multi-Provider DNS as Code)

**Library:** `/octodns/octodns`
**Trust Score:** High
**Code Snippets:** 128+
**Source Reputation:** High
**Benchmark Score:** 88.2/100

**Why OctoDNS?**
- DNS-as-code with version control
- Sync DNS across multiple providers
- YAML-based configuration
- Provider-agnostic abstraction layer
- Python-based (extensible)

**When to Use:**
- Managing DNS across multiple providers
- Need version control for DNS records
- Migrating between DNS providers
- Complex multi-environment setups

**Example Configuration:**
```yaml
---
providers:
  config:
    class: octodns.provider.yaml.YamlProvider
    directory: ./config
    default_ttl: 3600
  route53:
    class: octodns_route53.Route53Provider
    access_key_id: env/AWS_ACCESS_KEY_ID
    secret_access_key: env/AWS_SECRET_ACCESS_KEY
  cloudflare:
    class: octodns_cloudflare.CloudflareProvider
    token: env/CLOUDFLARE_TOKEN

zones:
  example.com.:
    sources:
      - config
    targets:
      - route53
      - cloudflare
```

**Record Definition (config/example.com.yaml):**
```yaml
---
'':
  ttl: 300
  type: A
  values:
    - 1.2.3.4
    - 1.2.3.5

www:
  type: CNAME
  value: example.com.
  ttl: 3600

'_dmarc':
  type: TXT
  value: "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"
```

---

#### Alternative 2: DNSControl (StackExchange)

**Library:** `/stackexchange/dnscontrol`
**Trust Score:** High
**Code Snippets:** 649+
**Source Reputation:** High

**Why DNSControl?**
- JavaScript-based DSL (familiar syntax)
- Multi-provider management
- Preview changes before applying (--preview)
- Used at scale by StackExchange
- Strong community

**When to Use:**
- Prefer JavaScript over YAML/Python
- Need multi-provider DNS management
- Want preview mode for safety
- Managing complex DNS configurations

**Example Configuration (dnsconfig.js):**
```javascript
var REG_NONE = NewRegistrar("none");
var DNS_CLOUDFLARE = NewDnsProvider("cloudflare");
var DNS_ROUTE53 = NewDnsProvider("route53");

D("example.com", REG_NONE,
  DnsProvider(DNS_CLOUDFLARE),
  DnsProvider(DNS_ROUTE53),

  A("@", "1.2.3.4", TTL(300)),
  A("www", "1.2.3.4", TTL(300)),
  CNAME("blog", "example.com."),
  MX("@", 10, "mail1.example.com."),
  MX("@", 20, "mail2.example.com."),
  TXT("@", "v=spf1 include:_spf.google.com ~all")
);
```

**Credentials (creds.json):**
```json
{
  "cloudflare": {
    "TYPE": "CLOUDFLAREAPI",
    "accountid": "your-account-id",
    "apitoken": "your-api-token"
  },
  "route53": {
    "TYPE": "ROUTE53",
    "KeyId": "your-key-id",
    "SecretKey": "your-secret-key"
  }
}
```

---

### Library Comparison Matrix

| Tool | Language | Best For | Learning Curve | Kubernetes | Multi-Provider |
|------|----------|----------|----------------|------------|----------------|
| **ExternalDNS** | Go | Kubernetes automation | Low | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **OctoDNS** | Python/YAML | Version-controlled DNS | Medium | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **DNSControl** | JavaScript | Multi-provider mgmt | Medium | ⭐⭐ | ⭐⭐⭐⭐⭐ |

**Recommendation by Use Case:**
- **Kubernetes DNS automation** → ExternalDNS
- **Multi-cloud DNS management** → OctoDNS or DNSControl
- **Version control for DNS** → OctoDNS or DNSControl
- **JavaScript preference** → DNSControl
- **Python preference** → OctoDNS

---

## DNS Management Taxonomy

### Record Types by Category

#### 1. Address Records (Host Resolution)

**A Record (IPv4 Address)**
- Maps hostname to IPv4 address
- Most common record type
- TTL: 300-3600s (5min-1hr)
- Example: `example.com → 192.0.2.1`

**AAAA Record (IPv6 Address)**
- Maps hostname to IPv6 address
- Increasingly important for IPv6 adoption
- TTL: 300-3600s
- Example: `example.com → 2001:db8::1`

**CNAME Record (Canonical Name)**
- Alias from one domain to another
- Cannot coexist with other records at same name
- Cannot be used at zone apex (@)
- TTL: 3600-86400s (1-24hr)
- Example: `www.example.com → example.com`

---

#### 2. Mail Records (Email Delivery)

**MX Record (Mail Exchange)**
- Directs email to mail servers
- Includes priority (lower = higher priority)
- TTL: 3600-86400s (1-24hr)
- Example: `example.com → 10 mail1.example.com`

**TXT Record (Text/SPF/DKIM/DMARC)**
- Arbitrary text data
- Used for email authentication (SPF, DKIM, DMARC)
- Used for domain verification
- TTL: 3600-86400s
- Example: `example.com → "v=spf1 include:_spf.google.com ~all"`

---

#### 3. Service Discovery Records

**SRV Record (Service Locator)**
- Specifies location of services
- Format: priority, weight, port, target
- Used for VoIP, XMPP, LDAP
- TTL: 3600-86400s
- Example: `_sip._tcp.example.com → 10 60 5060 sipserver.example.com`

---

#### 4. Delegation and Authority Records

**NS Record (Name Server)**
- Delegates subdomain to different nameservers
- Critical for zone delegation
- TTL: 86400-172800s (1-2 days)
- Example: `subdomain.example.com → ns1.provider.com`

**SOA Record (Start of Authority)**
- Metadata about the zone
- Includes serial number, refresh, retry, expire
- Only one per zone
- Automatically managed by DNS providers

---

#### 5. Security and Validation Records

**CAA Record (Certificate Authority Authorization)**
- Restricts which CAs can issue certificates
- Improves certificate security
- TTL: 3600-86400s
- Example: `example.com → 0 issue "letsencrypt.org"`

**DNSSEC Records (DS, DNSKEY, RRSIG, NSEC)**
- Cryptographic signatures for DNS data
- Prevents DNS spoofing and cache poisoning
- Requires registrar and DNS provider support
- Complex to manage (use provider tooling)

---

#### 6. Cloud-Specific Records

**ALIAS Record (Route53, Cloudflare)**
- Like CNAME but works at zone apex
- Provider-specific implementation
- Used for CDN and load balancer endpoints
- Example: `example.com → d111111abcdef8.cloudfront.net`

---

## Decision Framework

### 1. Record Type Selection

Use this decision tree to choose the correct record type:

```
Need to point domain to:
│
├─→ IPv4 Address?
│   ├─ Zone apex (@) → A record
│   └─ Subdomain → A record (or CNAME if pointing to another domain)
│
├─→ IPv6 Address?
│   └─ AAAA record
│
├─→ Another Domain Name?
│   ├─ Zone apex (@) → ALIAS/ANAME (provider-specific) or A record
│   └─ Subdomain → CNAME
│
├─→ Mail Server?
│   └─ MX record (with priority)
│
├─→ Email Authentication?
│   ├─ SPF → TXT record starting with "v=spf1"
│   ├─ DKIM → TXT record at selector._domainkey
│   └─ DMARC → TXT record at _dmarc
│
├─→ Service Discovery?
│   └─ SRV record (protocol, service, priority, weight, port, target)
│
├─→ Domain Verification?
│   └─ TXT record (value provided by service)
│
├─→ Certificate Authority Control?
│   └─ CAA record (restrict certificate issuance)
│
└─→ Subdomain Delegation?
    └─ NS record (point to different nameservers)
```

---

### 2. TTL Strategy Selection

Choose TTL based on change frequency and criticality:

```
How often does this record change?
│
├─→ Never/Rarely (years)
│   └─ TTL: 86400s (24 hours)
│       Examples: NS records, stable A records
│
├─→ Infrequently (months)
│   └─ TTL: 3600-43200s (1-12 hours)
│       Examples: MX records, stable CNAMEs
│
├─→ Occasionally (weeks/months)
│   └─ TTL: 1800-3600s (30min-1hr)
│       Examples: Website A records
│
├─→ Frequently (days/weeks)
│   └─ TTL: 300-1800s (5-30min)
│       Examples: Development environments, A/B testing
│
├─→ Very Frequently (hours/days)
│   └─ TTL: 60-300s (1-5min)
│       Examples: Failover scenarios, blue-green deployments
│
└─→ Planning a change NOW?
    ├─ Step 1: Lower TTL to 300s (24-48 hours before)
    ├─ Step 2: Make the change
    ├─ Step 3: Verify propagation
    └─ Step 4: Raise TTL back to normal
```

**TTL Strategy Cheat Sheet:**

| Use Case | Recommended TTL | Rationale |
|----------|----------------|-----------|
| Production website (stable) | 3600s (1hr) | Balance between speed and load |
| Production website (change planned) | 300s (5min) | Fast propagation |
| Development/staging | 300-600s | Frequent changes expected |
| Mail servers | 3600s (1hr) | Rarely change, critical |
| CDN endpoints | 300-1800s | May change for failover |
| DNS-based failover | 60-300s | Need fast failover |
| Load balancer endpoints | 300s | May add/remove backends |
| TXT records (verification) | 3600s | Rarely change |
| NS records | 86400s (24hr) | Very stable |

---

### 3. DNS Provider Selection

Choose based on your environment:

**Use AWS Route53 if:**
- Already using AWS heavily
- Need tight integration with ELB, CloudFront, S3
- Want health checks and failover
- Using Terraform/CloudFormation for IaC

**Use Google Cloud DNS if:**
- Using GCP as primary cloud
- Need DNSSEC support
- Want per-zone pricing
- Integrating with GKE/GCE

**Use Azure DNS if:**
- Using Azure as primary cloud
- Need integration with Traffic Manager
- Using Azure Private DNS zones
- Managing via ARM templates

**Use Cloudflare if:**
- Need fastest DNS query times
- Want built-in DDoS protection
- Need CDN + DNS combo
- Want simplest GeoDNS setup
- Working across multiple clouds

**Use OctoDNS/DNSControl if:**
- Managing DNS across multiple providers
- Need version control for DNS
- Want provider-agnostic configuration
- Complex multi-environment requirements

---

## Record Type Patterns

### A Record Examples

**Basic A Record:**
```
; Zone file format
example.com.     3600    IN    A    192.0.2.1
www.example.com. 3600    IN    A    192.0.2.1
```

**Multiple A Records (Round-Robin):**
```
example.com.     300     IN    A    192.0.2.1
example.com.     300     IN    A    192.0.2.2
example.com.     300     IN    A    192.0.2.3
```
*Note: This provides basic load distribution but no health checking*

**Route53 ALIAS Record (AWS-specific):**
```yaml
Type: AWS::Route53::RecordSet
Properties:
  HostedZoneId: Z1234567890ABC
  Name: example.com
  Type: A
  AliasTarget:
    HostedZoneId: Z2FDTNDATAQYW2  # CloudFront zone ID
    DNSName: d111111abcdef8.cloudfront.net
    EvaluateTargetHealth: false
```

---

### CNAME Record Examples

**Basic CNAME:**
```
www.example.com.    3600    IN    CNAME    example.com.
blog.example.com.   3600    IN    CNAME    example.com.
```
*Note: Always use FQDN (fully qualified domain name) with trailing dot*

**CNAME to External Service:**
```
shop.example.com.   3600    IN    CNAME    shops.myshopify.com.
docs.example.com.   3600    IN    CNAME    cname.vercel-dns.com.
```

**Common CNAME Mistake:**
```
# ❌ WRONG - CNAME at zone apex
example.com.        3600    IN    CNAME    target.example.com.

# ✅ CORRECT - Use A record or ALIAS at zone apex
example.com.        3600    IN    A        192.0.2.1
```

---

### MX Record Examples

**Google Workspace (Gmail):**
```
example.com.    3600    IN    MX    1  aspmx.l.google.com.
example.com.    3600    IN    MX    5  alt1.aspmx.l.google.com.
example.com.    3600    IN    MX    5  alt2.aspmx.l.google.com.
example.com.    3600    IN    MX    10 alt3.aspmx.l.google.com.
example.com.    3600    IN    MX    10 alt4.aspmx.l.google.com.
```

**Microsoft 365:**
```
example.com.    3600    IN    MX    0  example-com.mail.protection.outlook.com.
```

**Self-Hosted Mail:**
```
example.com.    3600    IN    MX    10 mail1.example.com.
example.com.    3600    IN    MX    20 mail2.example.com.
```

---

### TXT Record Examples

**SPF (Sender Policy Framework):**
```
example.com.    3600    IN    TXT    "v=spf1 include:_spf.google.com ~all"
example.com.    3600    IN    TXT    "v=spf1 ip4:192.0.2.0/24 mx ~all"
```

**DKIM (DomainKeys Identified Mail):**
```
default._domainkey.example.com.    3600    IN    TXT    "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA..."
```

**DMARC (Domain-based Message Authentication):**
```
_dmarc.example.com.    3600    IN    TXT    "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"
```

**Domain Verification (various services):**
```
example.com.    3600    IN    TXT    "google-site-verification=abcdef123456"
example.com.    3600    IN    TXT    "facebook-domain-verification=abcdef123456"
```

---

### SRV Record Examples

**SIP Service:**
```
_sip._tcp.example.com.    3600    IN    SRV    10 60 5060 sipserver.example.com.
```
*Format: priority weight port target*

**XMPP/Jabber:**
```
_xmpp-client._tcp.example.com.    3600    IN    SRV    5 0 5222 xmpp.example.com.
_xmpp-server._tcp.example.com.    3600    IN    SRV    5 0 5269 xmpp.example.com.
```

**Minecraft Server:**
```
_minecraft._tcp.example.com.    3600    IN    SRV    0 5 25565 mc.example.com.
```

---

### CAA Record Examples

**Let's Encrypt Only:**
```
example.com.    3600    IN    CAA    0 issue "letsencrypt.org"
example.com.    3600    IN    CAA    0 issuewild "letsencrypt.org"
```

**Multiple CAs:**
```
example.com.    3600    IN    CAA    0 issue "letsencrypt.org"
example.com.    3600    IN    CAA    0 issue "digicert.com"
```

**No CA Allowed:**
```
example.com.    3600    IN    CAA    0 issue ";"
```

**With Contact Email:**
```
example.com.    3600    IN    CAA    0 issue "letsencrypt.org"
example.com.    3600    IN    CAA    0 iodef "mailto:security@example.com"
```

---

## TTL Strategy Guide

### TTL Best Practices by Scenario

#### Scenario 1: Normal Operation (Stable Infrastructure)

**Goal:** Minimize DNS queries, optimize performance

**Recommended TTLs:**
- **A/AAAA records**: 3600s (1 hour)
- **CNAME records**: 3600-86400s (1-24 hours)
- **MX records**: 3600-86400s (1-24 hours)
- **TXT records**: 3600-86400s (1-24 hours)
- **NS records**: 86400s (24 hours)

**Rationale:** Longer TTLs reduce load on authoritative servers and improve resolution times.

---

#### Scenario 2: Pre-Change Preparation

**Goal:** Enable fast propagation for upcoming changes

**Timeline:**
```
T-48h: Lower TTL to 300s
T-24h: Verify TTL has propagated (check with dig)
T-0h:  Make the DNS change
T+1h:  Verify new records propagating
T+6h:  Verify globally propagated
T+24h: Raise TTL back to normal (3600s)
```

**Command to Check TTL:**
```bash
dig example.com | grep -A1 "ANSWER SECTION"
# Look for TTL value (number before IN A)
```

---

#### Scenario 3: Maintenance Window / Blue-Green Deployment

**Goal:** Switch traffic quickly between environments

**Strategy:**
1. **Before deployment:** TTL = 300s (5 minutes)
2. **During deployment:** Keep monitoring DNS propagation
3. **Switch traffic:** Update A record to new IP
4. **After verification:** Raise TTL to 1800s (30 min) for 24 hours
5. **Stable state:** Raise TTL to 3600s (1 hour)

**Example:**
```bash
# Before: Blue environment
example.com.    300    IN    A    192.0.2.1

# After: Green environment
example.com.    300    IN    A    192.0.2.2

# Verify propagation from multiple locations
dig @8.8.8.8 example.com +short        # Google DNS
dig @1.1.1.1 example.com +short        # Cloudflare DNS
dig @208.67.222.222 example.com +short # OpenDNS
```

---

#### Scenario 4: DNS-Based Failover

**Goal:** Fastest possible failover to backup systems

**Recommended TTLs:**
- **Primary A record**: 60-300s (1-5 minutes)
- **Health check interval**: 30-60s
- **Failover detection**: 2-3 failed checks

**Example (Route53 Health Check):**
```yaml
Type: AWS::Route53::RecordSet
Properties:
  HostedZoneId: Z1234567890ABC
  Name: example.com
  Type: A
  TTL: 60
  SetIdentifier: primary
  Failover: PRIMARY
  ResourceRecords:
    - 192.0.2.1
  HealthCheckId: abc123def456
---
Type: AWS::Route53::RecordSet
Properties:
  HostedZoneId: Z1234567890ABC
  Name: example.com
  Type: A
  TTL: 60
  SetIdentifier: secondary
  Failover: SECONDARY
  ResourceRecords:
    - 192.0.2.2
```

**Failover Timeline:**
- Health check fails: T+0s
- Route53 marks unhealthy: T+60s (after 2 failures)
- DNS updates: T+60s
- Clients respect new TTL: T+120s (60s old TTL + 60s new)
- Total failover time: ~2-3 minutes

---

#### Scenario 5: Dynamic DNS (DDNS)

**Goal:** Keep DNS updated with changing IP addresses

**Recommended TTL:** 30-60 minutes (half of DHCP lease time)

**Example:**
- DHCP lease: 60 minutes
- DNS TTL: 30 minutes
- Update frequency: Every 15-30 minutes

**DDNS Tools:**
- `ddclient` (Linux/Unix)
- Router built-in DDNS (many support Cloudflare, Route53)
- `external-dns` with `--source=node` (Kubernetes)

---

### TTL Propagation Calculator

**Formula:** `Max Propagation Time = Old TTL + New TTL + DNS Query Time`

**Examples:**

| Old TTL | New TTL | Change Type | Max Propagation |
|---------|---------|-------------|-----------------|
| 3600s (1h) | 3600s | Update A record | ~2 hours |
| 3600s | 300s | Lower TTL | ~1 hour 5 min |
| 300s | 3600s | Raise TTL | ~1 hour 5 min |
| 86400s (24h) | 300s | Emergency change | ~24 hours 5 min |

**Key Insight:** Old TTL matters most! Plan TTL changes in advance.

---

## DNS as Code

### Pattern 1: ExternalDNS (Kubernetes Native)

**Architecture:**
```
Kubernetes Cluster
├─ Service/Ingress (with annotations)
├─ ExternalDNS Controller (watches resources)
└─ Syncs to → DNS Provider (Route53, Cloud DNS, Cloudflare)
```

**Deployment (Helm):**
```bash
helm repo add external-dns https://kubernetes-sigs.github.io/external-dns/
helm repo update

helm install external-dns external-dns/external-dns \
  --namespace external-dns \
  --create-namespace \
  --set provider=aws \
  --set aws.region=us-east-1 \
  --set txtOwnerId=my-cluster \
  --set domainFilters[0]=example.com \
  --set policy=sync
```

**Service with DNS Annotation:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  annotations:
    external-dns.alpha.kubernetes.io/hostname: nginx.example.com
    external-dns.alpha.kubernetes.io/ttl: "300"
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 80
```

**Ingress with DNS Annotation:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    external-dns.alpha.kubernetes.io/hostname: app.example.com,www.example.com
    external-dns.alpha.kubernetes.io/ttl: "300"
spec:
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app
                port:
                  number: 80
```

**Provider-Specific Annotations (Route53):**
```yaml
metadata:
  annotations:
    external-dns.alpha.kubernetes.io/hostname: example.com
    external-dns.alpha.kubernetes.io/alias: "true"  # Use ALIAS record
    external-dns.alpha.kubernetes.io/set-identifier: "my-cluster"  # For weighted routing
```

**Supported Providers (20+):**
- AWS Route53, Azure DNS, Google Cloud DNS
- Cloudflare, DigitalOcean, Linode
- OVH, TransIP, Scaleway
- RFC2136 (BIND, PowerDNS)

---

### Pattern 2: OctoDNS (Multi-Provider Sync)

**Architecture:**
```
Git Repository (DNS config)
├─ config/example.com.yaml (YAML records)
├─ octodns-config.yaml (providers)
└─ octodns-sync → Syncs to multiple providers
```

**Directory Structure:**
```
dns-config/
├── octodns-config.yaml      # Main config
├── config/
│   ├── example.com.yaml     # Zone records
│   ├── example.org.yaml
│   └── internal.local.yaml
└── .github/workflows/
    └── sync-dns.yml         # CI/CD automation
```

**Main Configuration (octodns-config.yaml):**
```yaml
---
providers:
  config:
    class: octodns.provider.yaml.YamlProvider
    directory: ./config
    default_ttl: 3600

  route53:
    class: octodns_route53.Route53Provider
    access_key_id: env/AWS_ACCESS_KEY_ID
    secret_access_key: env/AWS_SECRET_ACCESS_KEY

  cloudflare:
    class: octodns_cloudflare.CloudflareProvider
    token: env/CLOUDFLARE_TOKEN

zones:
  example.com.:
    sources:
      - config
    targets:
      - route53
      - cloudflare
```

**Zone Records (config/example.com.yaml):**
```yaml
---
# Root domain
'':
  - type: A
    ttl: 300
    values:
      - 192.0.2.1
      - 192.0.2.2
  - type: MX
    ttl: 3600
    values:
      - exchange: mail1.example.com.
        preference: 10
      - exchange: mail2.example.com.
        preference: 20
  - type: TXT
    ttl: 3600
    values:
      - "v=spf1 include:_spf.google.com ~all"

# Subdomains
www:
  type: CNAME
  ttl: 3600
  value: example.com.

blog:
  type: CNAME
  ttl: 3600
  value: example.com.

api:
  type: A
  ttl: 300
  values:
    - 192.0.2.10

'_dmarc':
  type: TXT
  ttl: 3600
  value: "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"
```

**Sync Commands:**
```bash
# Preview changes (dry run)
octodns-sync --config-file=octodns-config.yaml

# Apply changes
octodns-sync --config-file=octodns-config.yaml --doit

# Sync specific zone
octodns-sync --config-file=octodns-config.yaml --doit example.com
```

**CI/CD Integration (.github/workflows/sync-dns.yml):**
```yaml
name: Sync DNS
on:
  push:
    branches: [main]
    paths:
      - 'config/**'
      - 'octodns-config.yaml'

jobs:
  sync-dns:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install OctoDNS
        run: |
          pip install octodns octodns-route53 octodns-cloudflare

      - name: Validate DNS config
        run: octodns-validate --config-file=octodns-config.yaml

      - name: Sync DNS
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          CLOUDFLARE_TOKEN: ${{ secrets.CLOUDFLARE_TOKEN }}
        run: octodns-sync --config-file=octodns-config.yaml --doit
```

---

### Pattern 3: DNSControl (JavaScript DSL)

**Architecture:**
```
Git Repository
├─ dnsconfig.js    # Main config (JavaScript)
├─ creds.json      # Provider credentials (gitignored)
└─ dnscontrol preview/push → Syncs to providers
```

**Configuration (dnsconfig.js):**
```javascript
var REG_NONE = NewRegistrar("none");
var DNS_CLOUDFLARE = NewDnsProvider("cloudflare");
var DNS_ROUTE53 = NewDnsProvider("route53");

// Helper function for common records
function StandardWeb(domain, ip) {
  return [
    A("@", ip, TTL(300)),
    A("www", ip, TTL(300)),
    CNAME("blog", domain + "."),
  ];
}

// Main domain - dual provider
D("example.com", REG_NONE,
  DnsProvider(DNS_CLOUDFLARE),
  DnsProvider(DNS_ROUTE53),

  // Apply standard web records
  StandardWeb("example.com", "192.0.2.1"),

  // Mail
  MX("@", 10, "mail1.example.com.", TTL(3600)),
  MX("@", 20, "mail2.example.com.", TTL(3600)),

  // Email auth
  TXT("@", "v=spf1 include:_spf.google.com ~all"),
  TXT("_dmarc", "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"),

  // API endpoint
  A("api", "192.0.2.10", TTL(300)),

  // Certificate verification
  CAA("@", "issue", "letsencrypt.org"),
  CAA("@", "iodef", "mailto:security@example.com"),
);

// Staging environment
D("staging.example.com", REG_NONE,
  DnsProvider(DNS_CLOUDFLARE),

  A("@", "192.0.2.100", TTL(300)),
  A("*", "192.0.2.100", TTL(300)),  // Wildcard
);
```

**Credentials (creds.json):**
```json
{
  "cloudflare": {
    "TYPE": "CLOUDFLAREAPI",
    "accountid": "your-account-id",
    "apitoken": "your-api-token"
  },
  "route53": {
    "TYPE": "ROUTE53",
    "KeyId": "your-key-id",
    "SecretKey": "your-secret-key"
  }
}
```

**Commands:**
```bash
# Validate configuration
dnscontrol check

# Preview changes (dry run)
dnscontrol preview

# Apply changes
dnscontrol push

# Push to specific provider
dnscontrol push --providers cloudflare

# Get current DNS config from provider
dnscontrol get-zones --format=js cloudflare example.com
```

---

### Pattern Comparison

| Feature | ExternalDNS | OctoDNS | DNSControl |
|---------|-------------|---------|------------|
| **Language** | YAML (annotations) | YAML | JavaScript |
| **Primary Use** | Kubernetes automation | Multi-provider sync | Multi-provider mgmt |
| **Learning Curve** | Low | Medium | Medium |
| **Version Control** | Via K8s manifests | Native (YAML files) | Native (JS files) |
| **Preview Mode** | No | Yes (`--doit` required) | Yes (`preview` cmd) |
| **Multi-Provider** | Via multiple deployments | Native | Native |
| **CI/CD Friendly** | GitOps (ArgoCD, Flux) | Excellent | Excellent |
| **Provider Count** | 20+ | 15+ | 30+ |

**Recommendation:**
- **Kubernetes-native** → ExternalDNS
- **Python ecosystem** → OctoDNS
- **JavaScript preference** → DNSControl
- **Complex logic/functions** → DNSControl (most expressive)

---

## Cloud DNS Services

### AWS Route53

**Key Features:**
- **Routing Policies**: Simple, weighted, latency-based, geolocation, geoproximity, failover, multivalue
- **Health Checks**: HTTP/HTTPS/TCP with failover
- **Alias Records**: Cost-free queries to AWS resources (ELB, CloudFront, S3)
- **Traffic Flow**: Visual policy editor for complex routing
- **DNSSEC**: Supported for domain registration and hosted zones

**Pricing (2025):**
- Hosted zone: $0.50/month per zone
- Queries: $0.40 per million (first 1 billion)
- Health checks: $0.50/month per check

**When to Use:**
- AWS-heavy infrastructure
- Need tight integration with ELB, CloudFront, API Gateway
- Using Terraform/CloudFormation for IaC
- Need advanced routing policies

**Example (Terraform):**
```hcl
resource "aws_route53_zone" "primary" {
  name = "example.com"
}

resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.primary.zone_id
  name    = "www.example.com"
  type    = "A"
  ttl     = 300
  records = ["192.0.2.1"]
}

resource "aws_route53_record" "www_alias" {
  zone_id = aws_route53_zone.primary.zone_id
  name    = "example.com"
  type    = "A"

  alias {
    name                   = aws_lb.main.dns_name
    zone_id                = aws_lb.main.zone_id
    evaluate_target_health = true
  }
}

# Health check with failover
resource "aws_route53_health_check" "primary" {
  fqdn              = "192.0.2.1"
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30
}

resource "aws_route53_record" "primary" {
  zone_id         = aws_route53_zone.primary.zone_id
  name            = "example.com"
  type            = "A"
  ttl             = 60
  set_identifier  = "primary"
  failover_routing_policy {
    type = "PRIMARY"
  }
  health_check_id = aws_route53_health_check.primary.id
  records         = ["192.0.2.1"]
}

resource "aws_route53_record" "secondary" {
  zone_id         = aws_route53_zone.primary.zone_id
  name            = "example.com"
  type            = "A"
  ttl             = 60
  set_identifier  = "secondary"
  failover_routing_policy {
    type = "SECONDARY"
  }
  records         = ["192.0.2.2"]
}
```

---

### Google Cloud DNS

**Key Features:**
- **Global Anycast Network**: Fast resolution worldwide
- **DNSSEC**: Full support with automatic key rotation
- **Private Zones**: Internal DNS for VPCs
- **GeoIP Routing**: Route based on client location
- **Split-Horizon DNS**: Different answers for internal/external

**Pricing (2025):**
- Managed zone: $0.20/month per zone
- Queries: $0.40 per million (first 1 billion)

**When to Use:**
- GCP-native applications
- Need DNSSEC with automatic management
- Using GKE (Kubernetes)
- Split-horizon DNS requirements

**Example (Terraform):**
```hcl
resource "google_dns_managed_zone" "primary" {
  name        = "example-com"
  dns_name    = "example.com."
  description = "Production DNS zone"

  dnssec_config {
    state = "on"
  }
}

resource "google_dns_record_set" "a" {
  name         = "example.com."
  managed_zone = google_dns_managed_zone.primary.name
  type         = "A"
  ttl          = 300
  rrdatas      = ["192.0.2.1", "192.0.2.2"]
}

# Private zone for internal services
resource "google_dns_managed_zone" "private" {
  name        = "internal-example"
  dns_name    = "internal.example.com."
  description = "Internal DNS zone"
  visibility  = "private"

  private_visibility_config {
    networks {
      network_url = google_compute_network.main.id
    }
  }
}
```

---

### Azure DNS

**Key Features:**
- **Azure Integration**: Tight integration with Azure resources
- **Private DNS Zones**: Name resolution within VNets
- **Anycast Network**: Microsoft's global network
- **RBAC**: Azure role-based access control
- **Alias Records**: Point to Azure resources without IP

**Pricing (2025):**
- Hosted zone: $0.50/month per zone (first 25 zones)
- Queries: $0.40 per million (first 1 billion)

**When to Use:**
- Azure-native applications
- Need integration with Azure Traffic Manager
- Using Azure Private Link
- ARM template-based deployments

**Example (Terraform):**
```hcl
resource "azurerm_dns_zone" "primary" {
  name                = "example.com"
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_dns_a_record" "www" {
  name                = "www"
  zone_name           = azurerm_dns_zone.primary.name
  resource_group_name = azurerm_resource_group.main.name
  ttl                 = 300
  records             = ["192.0.2.1"]
}

# Private DNS zone
resource "azurerm_private_dns_zone" "internal" {
  name                = "internal.example.com"
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "example" {
  name                  = "example-link"
  resource_group_name   = azurerm_resource_group.main.name
  private_dns_zone_name = azurerm_private_dns_zone.internal.name
  virtual_network_id    = azurerm_virtual_network.main.id
}
```

---

### Cloudflare DNS

**Key Features:**
- **Fastest DNS**: Consistently fastest query times globally
- **DDoS Protection**: Built-in, always-on
- **DNSSEC**: One-click enablement
- **Load Balancing**: Geo-steering, health checks
- **CDN Integration**: Seamless Cloudflare CDN
- **Free Tier**: Generous free plan for basic use

**Pricing (2025):**
- Free tier: Unlimited DNS queries
- Pro: $20/month (advanced features)
- Business: $200/month (load balancing, geo-steering)

**When to Use:**
- Need fastest DNS globally
- Want DDoS protection included
- Multi-cloud or cloud-agnostic
- Budget-conscious (free tier)
- Need CDN + DNS combo

**Example (Terraform):**
```hcl
resource "cloudflare_zone" "example" {
  account_id = var.cloudflare_account_id
  zone       = "example.com"
}

resource "cloudflare_record" "www" {
  zone_id = cloudflare_zone.example.id
  name    = "www"
  type    = "A"
  value   = "192.0.2.1"
  ttl     = 300
  proxied = true  # Route through Cloudflare CDN
}

# Load balancer with geo-steering
resource "cloudflare_load_balancer_pool" "us" {
  account_id = var.cloudflare_account_id
  name       = "us-pool"

  origins {
    name    = "us-east-1"
    address = "192.0.2.1"
    enabled = true
  }

  check_regions = ["WNAM", "ENAM"]
}

resource "cloudflare_load_balancer" "example" {
  zone_id          = cloudflare_zone.example.id
  name             = "example.com"
  default_pool_ids = [cloudflare_load_balancer_pool.us.id]
  fallback_pool_id = cloudflare_load_balancer_pool.us.id
  ttl              = 30
  proxied          = true
}
```

---

## DNS-Based Load Balancing

### GeoDNS (Geographic Routing)

**Concept:** Return different IP addresses based on client's geographic location.

**Use Cases:**
- Direct users to nearest data center (reduce latency)
- Comply with data residency requirements
- Distribute load across regions

**Example (Route53 Geolocation Routing):**
```hcl
# US users → US data center
resource "aws_route53_record" "us" {
  zone_id        = aws_route53_zone.primary.zone_id
  name           = "app.example.com"
  type           = "A"
  ttl            = 300
  set_identifier = "US"

  geolocation_routing_policy {
    continent = "NA"  # North America
  }

  records = ["192.0.2.1"]  # US data center
}

# EU users → EU data center
resource "aws_route53_record" "eu" {
  zone_id        = aws_route53_zone.primary.zone_id
  name           = "app.example.com"
  type           = "A"
  ttl            = 300
  set_identifier = "EU"

  geolocation_routing_policy {
    continent = "EU"
  }

  records = ["192.0.2.10"]  # EU data center
}

# Default → nearest CloudFront edge
resource "aws_route53_record" "default" {
  zone_id        = aws_route53_zone.primary.zone_id
  name           = "app.example.com"
  type           = "A"
  set_identifier = "Default"

  geolocation_routing_policy {
    location = "*"  # Default
  }

  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = false
  }
}
```

**Example (Cloudflare Geo-Steering):**
```hcl
resource "cloudflare_load_balancer_pool" "us" {
  account_id = var.cloudflare_account_id
  name       = "us-pool"
  origins {
    name    = "us-east"
    address = "192.0.2.1"
  }
}

resource "cloudflare_load_balancer_pool" "eu" {
  account_id = var.cloudflare_account_id
  name       = "eu-pool"
  origins {
    name    = "eu-west"
    address = "192.0.2.10"
  }
}

resource "cloudflare_load_balancer" "geo" {
  zone_id          = cloudflare_zone.example.id
  name             = "app.example.com"
  default_pool_ids = [cloudflare_load_balancer_pool.us.id]

  region_pools {
    region   = "WNAM"  # Western North America
    pool_ids = [cloudflare_load_balancer_pool.us.id]
  }

  region_pools {
    region   = "WEU"  # Western Europe
    pool_ids = [cloudflare_load_balancer_pool.eu.id]
  }
}
```

---

### Weighted Routing (A/B Testing, Canary Deployments)

**Concept:** Distribute traffic by percentage across multiple targets.

**Use Cases:**
- Blue-green deployments
- Canary releases (10% to new version)
- A/B testing

**Example (Route53):**
```hcl
# 90% to stable version
resource "aws_route53_record" "stable" {
  zone_id        = aws_route53_zone.primary.zone_id
  name           = "api.example.com"
  type           = "A"
  ttl            = 60
  set_identifier = "stable"

  weighted_routing_policy {
    weight = 90
  }

  records = ["192.0.2.1"]
}

# 10% to canary version
resource "aws_route53_record" "canary" {
  zone_id        = aws_route53_zone.primary.zone_id
  name           = "api.example.com"
  type           = "A"
  ttl            = 60
  set_identifier = "canary"

  weighted_routing_policy {
    weight = 10
  }

  records = ["192.0.2.2"]
}
```

---

### Health Check-Based Failover

**Concept:** Automatically route traffic away from unhealthy endpoints.

**Architecture:**
```
Client Query → DNS Provider
                ├─ Health Check: Primary (every 30s)
                │   ├─ Healthy → Return Primary IP
                │   └─ Unhealthy → Return Secondary IP
                └─ Health Check: Secondary (every 30s)
```

**Example (Route53 with Health Checks):**
```hcl
# Health check for primary
resource "aws_route53_health_check" "primary" {
  fqdn              = "primary.example.com"
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30

  tags = {
    Name = "Primary Health Check"
  }
}

# Primary record with health check
resource "aws_route53_record" "primary" {
  zone_id         = aws_route53_zone.primary.zone_id
  name            = "api.example.com"
  type            = "A"
  ttl             = 60
  set_identifier  = "primary"

  failover_routing_policy {
    type = "PRIMARY"
  }

  health_check_id = aws_route53_health_check.primary.id
  records         = ["192.0.2.1"]
}

# Secondary record (no health check needed)
resource "aws_route53_record" "secondary" {
  zone_id         = aws_route53_zone.primary.zone_id
  name            = "api.example.com"
  type            = "A"
  ttl             = 60
  set_identifier  = "secondary"

  failover_routing_policy {
    type = "SECONDARY"
  }

  records = ["192.0.2.2"]
}
```

**Failover Timeline:**
1. Health check fails (T+0s)
2. After 3 failures (90s with 30s interval)
3. Route53 marks unhealthy (T+90s)
4. New queries return secondary IP
5. Cached queries expire (T+90s + old TTL)
6. Full failover complete (T+150s with 60s TTL)

---

## Troubleshooting Guide

### Essential DNS Debugging Commands

#### 1. dig (Domain Information Groper)

**Basic Query:**
```bash
dig example.com

# Clean output (just the answer)
dig example.com +short

# Query specific record type
dig example.com A
dig example.com AAAA
dig example.com MX
dig example.com TXT
dig example.com NS
```

**Query Specific DNS Server:**
```bash
# Query Google DNS
dig @8.8.8.8 example.com

# Query Cloudflare DNS
dig @1.1.1.1 example.com

# Query authoritative nameserver
dig @ns1.example.com example.com
```

**Check TTL:**
```bash
dig example.com | grep -A1 "ANSWER SECTION"
# Output: example.com.  300  IN  A  192.0.2.1
#                        ^^^
#                        TTL value
```

**Trace DNS Resolution Path:**
```bash
dig +trace example.com

# Shows:
# 1. Root servers (.)
# 2. TLD servers (.com)
# 3. Authoritative servers (example.com)
# 4. Final answer
```

**Check DNSSEC:**
```bash
dig example.com +dnssec
```

---

#### 2. nslookup

**Basic Query:**
```bash
nslookup example.com

# Query specific server
nslookup example.com 8.8.8.8

# Interactive mode
nslookup
> server 8.8.8.8
> set type=MX
> example.com
```

---

#### 3. host

**Simple Lookup:**
```bash
host example.com

# Verbose output
host -v example.com

# Query specific record
host -t MX example.com
host -t TXT example.com
```

---

### Common DNS Problems and Solutions

#### Problem 1: DNS Propagation Delays

**Symptoms:**
- Changes not visible after DNS update
- Some locations see new records, others see old

**Diagnosis:**
```bash
# Check TTL (if low, should propagate fast)
dig example.com | grep -A1 "ANSWER"

# Check from multiple DNS resolvers
dig @8.8.8.8 example.com +short       # Google
dig @1.1.1.1 example.com +short       # Cloudflare
dig @208.67.222.222 example.com +short # OpenDNS

# Check authoritative server directly
dig @$(dig example.com NS +short | head -1) example.com
```

**Solutions:**
1. **Wait for TTL to expire** (old TTL + new TTL)
2. **Lower TTL 24-48 hours before changes**
3. **Flush local DNS cache:**
   ```bash
   # macOS
   sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder

   # Windows
   ipconfig /flushdns

   # Linux
   sudo systemd-resolve --flush-caches
   ```

**Propagation Checkers:**
- https://www.whatsmydns.net/
- https://dnschecker.org/
- https://dnspropagation.net/

---

#### Problem 2: CNAME at Zone Apex

**Symptoms:**
- Error: "CNAME conflicts with other records at apex"
- Cannot point example.com (not www) to CDN

**Diagnosis:**
```bash
dig example.com CNAME
# Should return NOERROR but no CNAME (not allowed)

dig example.com SOA
# SOA record exists at apex (conflicts with CNAME)
```

**Solutions:**
1. **Use provider-specific ALIAS record** (Route53, Cloudflare)
   ```hcl
   # Route53
   alias {
     name    = "d111111abcdef8.cloudfront.net"
     zone_id = "Z2FDTNDATAQYW2"
   }
   ```

2. **Use A record** (if CDN provides static IP)
   ```
   example.com.  300  IN  A  192.0.2.1
   ```

3. **Use ANAME record** (DNS Made Easy, NS1)

---

#### Problem 3: Missing DNS Records After Migration

**Symptoms:**
- Some services stop working after DNS migration
- Email or subdomains not resolving

**Diagnosis:**
```bash
# Export records from old provider
dig @old-ns1.provider.com example.com AXFR  # Zone transfer (if allowed)

# Check for all record types
for type in A AAAA CNAME MX TXT SRV CAA NS; do
  echo "=== $type ==="
  dig @old-ns1.provider.com example.com $type
done

# Compare with new provider
dig @new-ns1.provider.com example.com MX
```

**Solutions:**
1. **Audit all record types before migration**
2. **Use DNS migration tools:**
   ```bash
   # OctoDNS to export existing config
   octodns-dump --config-file=config.yaml --output-dir=./backup
   ```
3. **Keep old provider active for 48 hours** (parallel)

---

#### Problem 4: DNS Loops or CNAME Chains

**Symptoms:**
- DNS resolution fails
- "CNAME loop detected"

**Diagnosis:**
```bash
dig example.com +trace

# Check for circular references
dig www.example.com
# If www → example.com → www (loop!)
```

**Solutions:**
1. **Break the loop** - ensure CNAMEs point to A/AAAA records, not other CNAMEs
2. **Limit CNAME chains** - maximum 1-2 hops
3. **Use A records for final targets**

---

#### Problem 5: ExternalDNS Not Creating Records

**Symptoms:**
- Kubernetes Service with annotation, but no DNS record created
- ExternalDNS logs show errors

**Diagnosis:**
```bash
# Check ExternalDNS logs
kubectl logs -n external-dns deployment/external-dns

# Check Service annotations
kubectl get service nginx -o yaml | grep external-dns

# Verify domain filter matches
kubectl logs -n external-dns deployment/external-dns | grep "domain-filter"
```

**Common Issues:**
1. **Domain not in filter:**
   ```bash
   # Fix: Add to Helm values
   --set domainFilters[0]=example.com
   ```

2. **Missing provider credentials:**
   ```bash
   # Check secret exists
   kubectl get secret -n external-dns
   ```

3. **Wrong policy (upsert-only vs sync):**
   ```bash
   # Change to sync mode
   --set policy=sync
   ```

4. **Annotation typo:**
   ```yaml
   # Wrong
   external-dns.alpha.kubernetes.io/hostnam: example.com

   # Correct
   external-dns.alpha.kubernetes.io/hostname: example.com
   ```

---

## Tool Recommendations

### DNS Management Tools by Use Case

#### Kubernetes DNS Automation
**Primary:** ExternalDNS (`/kubernetes-sigs/external-dns`)
- **Trust:** High
- **Snippets:** 671+
- **When:** Running Kubernetes, need automatic DNS updates

**Alternative:** cert-manager + external-dns (for SSL + DNS)

---

#### Multi-Provider DNS Management
**Primary:** OctoDNS (`/octodns/octodns`)
- **Trust:** High, **Score:** 88.2/100
- **Snippets:** 128+
- **When:** Managing DNS across multiple providers, Python shop

**Alternative:** DNSControl (`/stackexchange/dnscontrol`)
- **Trust:** High
- **Snippets:** 649+
- **When:** JavaScript preference, complex logic needed

---

#### DNS Monitoring and Alerting
**Tools:**
- **DNSPerf** - Real-time DNS performance monitoring
- **DNS Check** - Multi-location propagation checking
- **Datadog** - DNS query monitoring and alerting
- **Prometheus + Blackbox Exporter** - Self-hosted DNS monitoring

**Example (Prometheus Blackbox):**
```yaml
- job_name: 'dns'
  metrics_path: /probe
  params:
    module: [dns_soa]
  static_configs:
    - targets:
      - example.com
      - www.example.com
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: blackbox-exporter:9115
```

---

#### DNS Testing Tools
- **dig** - Command-line DNS lookup
- **nslookup** - Simple DNS query tool
- **host** - DNS lookup utility
- **dnsperf** - DNS performance testing
- **namebench** - DNS server benchmark

---

### Recommended Tool Stack

**Tier 1: Essential (All Teams)**
```
ExternalDNS (if Kubernetes)
+ dig/nslookup (debugging)
+ whatsmydns.net (propagation checking)
```

**Tier 2: Professional (DevOps Teams)**
```
OctoDNS or DNSControl (version control)
+ Terraform (IaC for DNS)
+ Prometheus (monitoring)
+ PagerDuty (alerting)
```

**Tier 3: Enterprise (Large Scale)**
```
Multi-provider setup (Route53 + Cloudflare)
+ OctoDNS (sync across providers)
+ Datadog (comprehensive monitoring)
+ Custom health check infrastructure
+ DNSSEC enforcement
```

---

## Skill Structure Design

### Proposed Skill File Structure

```
dns-management/
├── SKILL.md                           # Main skill file (~400 lines)
│   ├── Purpose and When to Use
│   ├── Quick Reference (record types, TTL guide)
│   ├── Decision Frameworks
│   └── References to detailed docs
│
├── reference/
│   ├── record-types.md                # Detailed record type reference
│   ├── ttl-strategies.md              # TTL best practices by scenario
│   ├── cloud-providers.md             # Route53, Cloud DNS, Azure DNS, Cloudflare
│   ├── troubleshooting.md             # Common problems and solutions
│   └── dns-as-code-comparison.md      # ExternalDNS vs OctoDNS vs DNSControl
│
├── examples/
│   ├── external-dns/
│   │   ├── helm-values.yaml           # ExternalDNS Helm configuration
│   │   ├── service-example.yaml       # Service with annotations
│   │   └── ingress-example.yaml       # Ingress with annotations
│   │
│   ├── octodns/
│   │   ├── octodns-config.yaml        # Main OctoDNS config
│   │   ├── zone-records.yaml          # Example zone records
│   │   └── ci-cd-workflow.yml         # GitHub Actions integration
│   │
│   ├── dnscontrol/
│   │   ├── dnsconfig.js               # DNSControl configuration
│   │   └── creds-template.json        # Credentials template
│   │
│   ├── terraform/
│   │   ├── route53-example.tf         # AWS Route53
│   │   ├── cloud-dns-example.tf       # GCP Cloud DNS
│   │   ├── azure-dns-example.tf       # Azure DNS
│   │   └── cloudflare-example.tf      # Cloudflare
│   │
│   └── load-balancing/
│       ├── geodns-route53.tf          # GeoDNS with Route53
│       ├── failover-route53.tf        # Health check failover
│       └── cloudflare-lb.tf           # Cloudflare load balancing
│
└── scripts/
    ├── check-dns-propagation.sh       # Multi-resolver propagation check
    ├── validate-dns-config.py         # Validate DNS configuration
    ├── export-dns-records.sh          # Export existing DNS records
    └── calculate-ttl-propagation.py   # Calculate propagation time
```

---

### SKILL.md Structure (Main File)

```markdown
---
name: dns-management
description: Manage DNS records, TTL strategies, DNS-as-code automation, and DNS-based load balancing. Covers record types, cloud DNS services (Route53, Cloud DNS, Azure DNS, Cloudflare), external-dns, OctoDNS, DNSControl, troubleshooting, and best practices for infrastructure.
---

# DNS Management

Manage DNS records efficiently with proper TTL strategies, automation, and troubleshooting.

## Purpose

Guide DNS configuration for applications, infrastructure, and services. Covers:
- Record type selection (A, AAAA, CNAME, MX, TXT, SRV)
- TTL strategies (propagation, caching, failover)
- DNS-as-code (external-dns, OctoDNS, DNSControl)
- Cloud DNS services (Route53, Cloud DNS, Azure DNS, Cloudflare)
- DNS-based load balancing (GeoDNS, failover)
- Troubleshooting (dig, propagation tools)

## When to Use This Skill

Trigger when:
- Setting up DNS for applications
- Automating DNS from Kubernetes
- Configuring failover/load balancing
- Troubleshooting DNS issues
- Migrating DNS providers
- Planning DNS changes

## Quick Decision Trees

### Record Type Selection
See reference/record-types.md for detailed decision tree.

Quick guide:
- Point to IPv4 → A record
- Point to IPv6 → AAAA record
- Point to another domain → CNAME (subdomains) or ALIAS (apex)
- Email servers → MX record
- Email auth → TXT record (SPF/DKIM/DMARC)
- Service discovery → SRV record
- Certificate control → CAA record

### TTL Strategy
See reference/ttl-strategies.md for scenarios.

Quick guide:
- Normal operation → 3600s (1 hour)
- Before changes → 300s (5 minutes)
- Failover scenarios → 60-300s
- NS records → 86400s (24 hours)

## DNS-as-Code Tools

See reference/dns-as-code-comparison.md for detailed comparison.

**Kubernetes → external-dns**
See examples/external-dns/

**Multi-provider → OctoDNS or DNSControl**
See examples/octodns/ or examples/dnscontrol/

## Cloud DNS Providers

See reference/cloud-providers.md for detailed guide.

**Choose:**
- Route53 → AWS-heavy
- Cloud DNS → GCP-native
- Azure DNS → Azure-native
- Cloudflare → Multi-cloud, fastest, DDoS protection

## Troubleshooting

See reference/troubleshooting.md for common problems.

**Basic diagnostics:**
```bash
dig example.com
dig @8.8.8.8 example.com +short
dig example.com +trace
```

**Check propagation:**
Scripts: scripts/check-dns-propagation.sh

## Examples

All examples in examples/ directory:
- examples/external-dns/ - Kubernetes automation
- examples/octodns/ - Multi-provider sync
- examples/terraform/ - Cloud provider configs
- examples/load-balancing/ - GeoDNS, failover

## Additional Resources

- reference/record-types.md - Detailed record type guide
- reference/ttl-strategies.md - TTL best practices
- reference/cloud-providers.md - Provider comparison
- reference/troubleshooting.md - Problem solving
```

---

## Integration Points

### Complements Other Skills

**infrastructure-as-code:**
- DNS managed via Terraform/Pulumi
- Zone configuration in IaC
- Integration with cloud resources

**kubernetes-operations:**
- external-dns automates K8s → DNS
- Ingress/Service annotations
- Multi-cluster DNS management

**load-balancing-patterns:**
- DNS-based load balancing (GeoDNS)
- Health checks and failover
- Weighted routing for canary

**security-hardening:**
- DNSSEC for DNS integrity
- CAA records for certificate control
- DNS-based DDoS mitigation

**secret-management:**
- DNS provider credentials in vaults
- API keys for DNS automation
- Secure DDNS updates

---

### Shared Patterns

**Pattern: DNS + SSL Automation**
```yaml
# external-dns + cert-manager
apiVersion: v1
kind: Service
metadata:
  annotations:
    external-dns.alpha.kubernetes.io/hostname: app.example.com
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: app-tls
spec:
  dnsNames:
    - app.example.com
  issuerRef:
    name: letsencrypt
```

**Pattern: DNS + Load Balancer**
```hcl
# Route53 + ALB
resource "aws_lb" "main" {
  name               = "app-lb"
  load_balancer_type = "application"
}

resource "aws_route53_record" "app" {
  zone_id = aws_route53_zone.primary.zone_id
  name    = "app.example.com"
  type    = "A"

  alias {
    name                   = aws_lb.main.dns_name
    zone_id                = aws_lb.main.zone_id
    evaluate_target_health = true
  }
}
```

**Pattern: DNS + Monitoring**
```yaml
# Prometheus blackbox exporter
- job_name: 'dns-monitoring'
  scrape_interval: 30s
  metrics_path: /probe
  params:
    module: [dns_soa]
  static_configs:
    - targets:
      - example.com
      - api.example.com
```

---

## Implementation Roadmap

### Phase 1: Core Documentation (Week 1)

**Deliverables:**
- [ ] SKILL.md (main file, ~400 lines)
- [ ] reference/record-types.md (detailed record guide)
- [ ] reference/ttl-strategies.md (TTL scenarios)
- [ ] reference/troubleshooting.md (common problems)

**Focus:** Essential knowledge, decision frameworks, quick reference

---

### Phase 2: DNS-as-Code Examples (Week 2)

**Deliverables:**
- [ ] examples/external-dns/ (Kubernetes automation)
- [ ] examples/octodns/ (multi-provider sync)
- [ ] examples/dnscontrol/ (JavaScript DSL)
- [ ] reference/dns-as-code-comparison.md

**Focus:** Practical automation patterns, working examples

---

### Phase 3: Cloud Provider Guide (Week 3)

**Deliverables:**
- [ ] reference/cloud-providers.md (Route53, Cloud DNS, Azure DNS, Cloudflare)
- [ ] examples/terraform/ (Terraform for each provider)
- [ ] examples/load-balancing/ (GeoDNS, failover)

**Focus:** Provider-specific patterns, load balancing

---

### Phase 4: Tooling and Scripts (Week 4)

**Deliverables:**
- [ ] scripts/check-dns-propagation.sh
- [ ] scripts/validate-dns-config.py
- [ ] scripts/export-dns-records.sh
- [ ] scripts/calculate-ttl-propagation.py

**Focus:** Automation, validation, troubleshooting helpers

---

### Phase 5: Testing and Refinement (Week 5)

**Activities:**
- [ ] Test skill with real DNS scenarios
- [ ] Validate examples in cloud environments
- [ ] Gather feedback from DNS use cases
- [ ] Refine decision frameworks
- [ ] Add missing patterns

**Focus:** Real-world validation, completeness

---

## Success Criteria

### Skill is Successful When:

**Knowledge Transfer:**
- [ ] User can select correct record type for any scenario
- [ ] User understands TTL trade-offs (speed vs load)
- [ ] User can troubleshoot DNS issues with dig/nslookup

**Automation:**
- [ ] User can deploy external-dns for Kubernetes
- [ ] User can set up OctoDNS or DNSControl for multi-provider
- [ ] User can configure DNS-based load balancing

**Best Practices:**
- [ ] User plans TTL changes before DNS updates
- [ ] User validates DNS propagation globally
- [ ] User implements health checks for failover

**Integration:**
- [ ] User integrates DNS with IaC (Terraform)
- [ ] User automates DNS with CI/CD
- [ ] User monitors DNS performance

---

## Maintenance Plan

**Quarterly Reviews:**
- Update cloud provider pricing
- Check for new external-dns/OctoDNS features
- Validate Terraform examples with latest versions
- Update tool recommendations

**Trigger for Updates:**
- Major cloud provider DNS changes
- New DNS automation tools emerge
- Breaking changes in external-dns/OctoDNS
- New DNS record types standardized

---

## Notes for Implementation

### Key Insights from Research

1. **TTL is critical** - Most DNS issues stem from not understanding TTL propagation
2. **Plan changes in advance** - Lower TTL 24-48 hours before changes
3. **ExternalDNS is mature** - 671+ snippets, well-documented, production-ready
4. **Multi-provider is common** - OctoDNS/DNSControl fill real need
5. **Cloudflare is fastest** - Consistently fastest query times globally

### Progressive Disclosure Strategy

**Tier 1 (SKILL.md):**
- Quick decision trees
- Common patterns
- When to use which tool

**Tier 2 (reference/):**
- Detailed record type docs
- TTL scenario guide
- Provider comparison

**Tier 3 (examples/):**
- Working code examples
- Full configurations
- Real-world patterns

**Tier 4 (scripts/):**
- Automation tools
- Validation scripts
- Troubleshooting helpers

---

## Appendix: Research Sources

### Google Search Grounding Results

**Query 1: "DNS best practices 2025 TTL strategies propagation"**
- ionos.ca - TTL best practices
- phoenixnap.com - DNS propagation guide
- runcloud.io - TTL optimization
- catchpoint.com - DNS monitoring

**Key Findings:**
- TTL: 24h for stable, 5min for changes, never 0
- Lower TTL 24-48h before changes
- Monitor propagation with tools

**Query 2: "external-dns Kubernetes DNS automation 2025"**
- medium.com - ExternalDNS tutorial
- komodor.com - Kubernetes DNS automation
- containerinfra.com - ExternalDNS patterns

**Key Findings:**
- ExternalDNS is standard for K8s
- 20+ provider support
- Annotation-based configuration

**Query 3: "DNS-based load balancing GeoDNS Route53 CloudFlare 2025"**
- cloudflare.com - Geo-steering docs
- mattgadient.com - Route53 vs Cloudflare
- dev.to - DNS load balancing guide

**Key Findings:**
- Route53: Best AWS integration
- Cloudflare: Fastest globally, DDoS protection
- Both offer robust GeoDNS

### Context7 Library Results

**ExternalDNS:**
- ID: `/kubernetes-sigs/external-dns`
- Snippets: 671+
- Trust: High
- Status: Production-ready

**OctoDNS:**
- ID: `/octodns/octodns`
- Snippets: 128+
- Trust: High
- Benchmark: 88.2/100

**DNSControl:**
- ID: `/stackexchange/dnscontrol`
- Snippets: 649+
- Trust: High
- Used by StackExchange at scale

---

## Version History

- **v1.0** (2025-12-03): Initial master plan created
  - Research completed (Google Search Grounding + Context7)
  - Taxonomy defined (6 record categories)
  - Decision frameworks created
  - Tool recommendations finalized
  - 5-phase implementation roadmap

---

**End of Master Plan**

*This init.md serves as the comprehensive blueprint for implementing the dns-management skill. Proceed to Phase 1 when ready to create SKILL.md and reference documentation.*
