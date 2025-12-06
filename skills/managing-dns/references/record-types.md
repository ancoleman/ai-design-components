# DNS Record Types - Detailed Reference

Complete guide to DNS record types with examples, use cases, and best practices.

## Table of Contents

1. [Address Records](#address-records)
2. [Mail Records](#mail-records)
3. [Service Discovery Records](#service-discovery-records)
4. [Delegation and Authority Records](#delegation-and-authority-records)
5. [Security Records](#security-records)
6. [Cloud-Specific Records](#cloud-specific-records)
7. [Record Type Selection Decision Tree](#record-type-selection-decision-tree)

---

## Address Records

### A Record (IPv4 Address)

**Purpose:** Map hostname to IPv4 address

**Format:**
```
hostname  TTL  IN  A  ipv4-address
```

**Examples:**
```
# Basic A record
example.com.     3600  IN  A  192.0.2.1
www.example.com. 3600  IN  A  192.0.2.1

# Multiple A records (round-robin)
example.com.     300   IN  A  192.0.2.1
example.com.     300   IN  A  192.0.2.2
example.com.     300   IN  A  192.0.2.3
```

**When to Use:**
- Point domain to server IPv4 address
- Load balancing with round-robin DNS
- Zone apex (@) records

**TTL Recommendations:**
- Stable servers: 3600s (1 hour)
- Load balanced: 300s (5 minutes)
- Before changes: 300s

**Common Mistakes:**
- Using CNAME instead of A at zone apex (not allowed)
- Setting TTL too high before planned changes
- Forgetting to add both @ and www records

---

### AAAA Record (IPv6 Address)

**Purpose:** Map hostname to IPv6 address

**Format:**
```
hostname  TTL  IN  AAAA  ipv6-address
```

**Examples:**
```
example.com.     3600  IN  AAAA  2001:db8::1
www.example.com. 3600  IN  AAAA  2001:db8::1
```

**When to Use:**
- IPv6-enabled servers
- Dual-stack deployments (A + AAAA)
- Future-proofing infrastructure

**Best Practices:**
- Always include A record alongside AAAA (dual-stack)
- Use same TTL for A and AAAA records
- Test IPv6 connectivity before adding AAAA

---

### CNAME Record (Canonical Name)

**Purpose:** Alias one domain to another

**Format:**
```
alias  TTL  IN  CNAME  target.
```

**Examples:**
```
# Basic CNAME
www.example.com.    3600  IN  CNAME  example.com.
blog.example.com.   3600  IN  CNAME  example.com.

# CNAME to external service
shop.example.com.   3600  IN  CNAME  shops.myshopify.com.
docs.example.com.   3600  IN  CNAME  cname.vercel-dns.com.
```

**When to Use:**
- Alias subdomains to main domain
- Point to external services (CDN, hosting)
- Create friendly names for complex hostnames

**Restrictions:**
- **Cannot** use at zone apex (@)
- **Cannot** coexist with other records at same name
- Target must be FQDN (fully qualified domain name with trailing dot)

**Common Mistakes:**
```
# ❌ WRONG - CNAME at zone apex
example.com.  3600  IN  CNAME  target.example.com.

# ✅ CORRECT - Use A or ALIAS at zone apex
example.com.  3600  IN  A      192.0.2.1

# ❌ WRONG - CNAME with MX record
mail.example.com.  3600  IN  CNAME  example.com.
mail.example.com.  3600  IN  MX     10 mail.example.com.

# ✅ CORRECT - Use A record instead
mail.example.com.  3600  IN  A      192.0.2.1
example.com.       3600  IN  MX     10 mail.example.com.
```

**TTL Recommendations:**
- Stable CNAMEs: 3600-86400s (1-24 hours)
- CDN/hosting: 3600s (1 hour)

---

## Mail Records

### MX Record (Mail Exchange)

**Purpose:** Direct email to mail servers

**Format:**
```
domain  TTL  IN  MX  priority  mail-server.
```

**Examples:**

**Google Workspace:**
```
example.com.  3600  IN  MX  1   aspmx.l.google.com.
example.com.  3600  IN  MX  5   alt1.aspmx.l.google.com.
example.com.  3600  IN  MX  5   alt2.aspmx.l.google.com.
example.com.  3600  IN  MX  10  alt3.aspmx.l.google.com.
example.com.  3600  IN  MX  10  alt4.aspmx.l.google.com.
```

**Microsoft 365:**
```
example.com.  3600  IN  MX  0  example-com.mail.protection.outlook.com.
```

**Self-Hosted:**
```
example.com.  3600  IN  MX  10  mail1.example.com.
example.com.  3600  IN  MX  20  mail2.example.com.
```

**Priority Values:**
- Lower number = higher priority
- Sending servers try lowest priority first
- Same priority = load balancing (random selection)

**Best Practices:**
- Always include multiple MX records for redundancy
- Use priority 10, 20, 30 (leave room for future additions)
- Ensure mail servers have A/AAAA records
- Add SPF/DKIM/DMARC TXT records for email authentication

**TTL Recommendations:**
- Standard: 3600-86400s (1-24 hours)
- Mail servers rarely change

---

### TXT Record (Text)

**Purpose:** Store arbitrary text data, commonly used for:
- SPF (Sender Policy Framework)
- DKIM (DomainKeys Identified Mail)
- DMARC (Domain-based Message Authentication)
- Domain verification
- Other metadata

**Format:**
```
hostname  TTL  IN  TXT  "text-content"
```

**SPF Examples:**
```
# Google Workspace
example.com.  3600  IN  TXT  "v=spf1 include:_spf.google.com ~all"

# Microsoft 365
example.com.  3600  IN  TXT  "v=spf1 include:spf.protection.outlook.com ~all"

# Multiple mail sources
example.com.  3600  IN  TXT  "v=spf1 ip4:192.0.2.0/24 include:_spf.google.com mx ~all"

# Strict SPF (reject all others)
example.com.  3600  IN  TXT  "v=spf1 include:_spf.google.com -all"
```

**SPF Qualifiers:**
- `+all` - Pass all (not recommended)
- `~all` - Soft fail (most common)
- `-all` - Hard fail (strict)
- `?all` - Neutral

**DKIM Examples:**
```
# DKIM selector record
default._domainkey.example.com.  3600  IN  TXT  "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA..."

# Google DKIM
google._domainkey.example.com.  3600  IN  TXT  "v=DKIM1; k=rsa; p=..."
```

**DMARC Examples:**
```
# Quarantine policy with reporting
_dmarc.example.com.  3600  IN  TXT  "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"

# Reject policy
_dmarc.example.com.  3600  IN  TXT  "v=DMARC1; p=reject; rua=mailto:dmarc@example.com; ruf=mailto:forensics@example.com"

# Monitor mode (no action)
_dmarc.example.com.  3600  IN  TXT  "v=DMARC1; p=none; rua=mailto:dmarc@example.com"
```

**Domain Verification Examples:**
```
# Google site verification
example.com.  3600  IN  TXT  "google-site-verification=abc123def456..."

# Facebook domain verification
example.com.  3600  IN  TXT  "facebook-domain-verification=abc123def456..."

# General verification token
example.com.  3600  IN  TXT  "verification-token=xyz789..."
```

**Best Practices:**
- Keep TXT records under 255 characters per string
- Split long records into multiple strings
- Use descriptive prefixes (_dmarc, _domainkey)
- Document purpose of each TXT record

**TTL Recommendations:**
- Verification records: 3600s (remove after verification)
- SPF/DKIM/DMARC: 3600-86400s (1-24 hours)

---

## Service Discovery Records

### SRV Record (Service Locator)

**Purpose:** Specify location of services

**Format:**
```
_service._protocol.domain  TTL  IN  SRV  priority  weight  port  target.
```

**Components:**
- **priority**: Lower = higher priority (like MX)
- **weight**: Load distribution (0 = no preference)
- **port**: Service port number
- **target**: Hostname providing the service

**Examples:**

**SIP (VoIP):**
```
_sip._tcp.example.com.     3600  IN  SRV  10  60  5060  sipserver.example.com.
_sip._udp.example.com.     3600  IN  SRV  10  60  5060  sipserver.example.com.
```

**XMPP/Jabber:**
```
_xmpp-client._tcp.example.com.  3600  IN  SRV  5  0  5222  xmpp.example.com.
_xmpp-server._tcp.example.com.  3600  IN  SRV  5  0  5269  xmpp.example.com.
```

**LDAP:**
```
_ldap._tcp.example.com.    3600  IN  SRV  0  0  389  ldap.example.com.
```

**Minecraft Server:**
```
_minecraft._tcp.example.com.  3600  IN  SRV  0  5  25565  mc.example.com.
```

**When to Use:**
- Service discovery (VoIP, messaging, game servers)
- Multiple servers with priority/weight
- Port-specific service routing

**Best Practices:**
- Ensure target hostname has A/AAAA record
- Use priority for failover
- Use weight for load balancing among same priority

---

## Delegation and Authority Records

### NS Record (Name Server)

**Purpose:** Delegate subdomain to different nameservers

**Format:**
```
subdomain  TTL  IN  NS  nameserver.
```

**Examples:**

**Zone delegation:**
```
# Delegate subdomain.example.com to different nameservers
subdomain.example.com.  86400  IN  NS  ns1.provider.com.
subdomain.example.com.  86400  IN  NS  ns2.provider.com.
```

**Root zone NS records:**
```
example.com.  86400  IN  NS  ns1.example.com.
example.com.  86400  IN  NS  ns2.example.com.
```

**When to Use:**
- Delegate subdomain to different DNS provider
- Separate management of different subdomains
- Multi-team DNS management

**Best Practices:**
- Always specify multiple NS records (minimum 2)
- Use high TTL (86400-172800s / 1-2 days)
- Ensure glue records exist for in-zone nameservers

**TTL Recommendations:**
- 86400s (24 hours) - NS records rarely change

---

### SOA Record (Start of Authority)

**Purpose:** Define zone metadata

**Format:**
```
domain  TTL  IN  SOA  primary-ns  admin-email  (
    serial      ; Serial number
    refresh     ; Refresh interval
    retry       ; Retry interval
    expire      ; Expiration time
    minimum     ; Minimum TTL
)
```

**Example:**
```
example.com.  3600  IN  SOA  ns1.example.com. admin.example.com. (
    2024120401  ; Serial (YYYYMMDDnn)
    7200        ; Refresh (2 hours)
    3600        ; Retry (1 hour)
    1209600     ; Expire (2 weeks)
    3600        ; Minimum TTL (1 hour)
)
```

**Best Practices:**
- Automatically managed by DNS providers (rarely edit manually)
- Increment serial number when making zone changes
- Use date-based serial: YYYYMMDDnn format

---

## Security Records

### CAA Record (Certificate Authority Authorization)

**Purpose:** Restrict which Certificate Authorities can issue certificates

**Format:**
```
domain  TTL  IN  CAA  flags  tag  "value"
```

**Tags:**
- `issue`: Authorize CA for domain and subdomains
- `issuewild`: Authorize CA for wildcard certificates
- `iodef`: Email for certificate issue violations

**Examples:**

**Let's Encrypt only:**
```
example.com.  3600  IN  CAA  0  issue     "letsencrypt.org"
example.com.  3600  IN  CAA  0  issuewild "letsencrypt.org"
```

**Multiple CAs:**
```
example.com.  3600  IN  CAA  0  issue  "letsencrypt.org"
example.com.  3600  IN  CAA  0  issue  "digicert.com"
```

**No certificates allowed:**
```
example.com.  3600  IN  CAA  0  issue  ";"
```

**With notification:**
```
example.com.  3600  IN  CAA  0  issue  "letsencrypt.org"
example.com.  3600  IN  CAA  0  iodef  "mailto:security@example.com"
```

**Best Practices:**
- Always add CAA records for security
- Include both `issue` and `issuewild` tags
- Add `iodef` for violation notifications
- Test with CA before enforcing strict policy

**TTL Recommendations:**
- 3600-86400s (1-24 hours)

---

### DNSSEC Records

**Purpose:** Cryptographic signatures for DNS data integrity

**Record Types:**
- **DNSKEY**: Public signing key
- **RRSIG**: Signature for record set
- **DS**: Delegation signer (at parent zone)
- **NSEC/NSEC3**: Authenticated denial of existence

**When to Use:**
- Prevent DNS cache poisoning
- Authenticate DNS responses
- Required for high-security environments

**Best Practices:**
- Use provider-managed DNSSEC (complex to manage manually)
- Enable at both registrar and DNS provider
- Monitor for key rotation
- Test thoroughly before enabling

**Note:** DNSSEC is typically managed by DNS providers automatically. Manual configuration is complex and error-prone.

---

## Cloud-Specific Records

### ALIAS Record (Route53, Cloudflare, DNS Made Easy)

**Purpose:** CNAME-like record that works at zone apex

**Provider Support:**
- AWS Route53: ALIAS record
- Cloudflare: CNAME flattening
- DNS Made Easy: ANAME record
- NS1: ALIAS record

**Example (Route53):**
```hcl
resource "aws_route53_record" "apex" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "example.com"
  type    = "A"

  alias {
    name                   = aws_lb.main.dns_name
    zone_id                = aws_lb.main.zone_id
    evaluate_target_health = true
  }
}
```

**When to Use:**
- Point zone apex to CDN (CloudFront, Cloudflare)
- Point zone apex to load balancer
- Alternative to A record when IP may change

**Benefits:**
- Works at zone apex (unlike CNAME)
- Automatically updated when target changes
- No additional charge for queries (Route53)

---

## Record Type Selection Decision Tree

### Complete Decision Flow

```
What are you trying to configure?

1. Point domain to server IP
   ├─ IPv4 address → A record
   ├─ IPv6 address → AAAA record
   └─ Both → A + AAAA records (dual-stack)

2. Point domain to another domain
   ├─ Subdomain (www, blog, api)
   │  └─ CNAME record
   └─ Zone apex (@, example.com)
      ├─ Provider supports ALIAS → ALIAS record
      └─ Provider doesn't support ALIAS → A record (use IP)

3. Configure email
   ├─ Mail servers → MX record
   ├─ Sender authentication
   │  ├─ SPF → TXT record at @
   │  ├─ DKIM → TXT record at selector._domainkey
   │  └─ DMARC → TXT record at _dmarc
   └─ Email forwarding → MX + A records

4. Service discovery
   └─ Service location (SIP, XMPP, LDAP) → SRV record

5. Domain verification
   └─ Verification token → TXT record

6. Certificate management
   └─ Restrict certificate issuance → CAA record

7. Subdomain delegation
   └─ Different nameservers → NS record

8. Security
   ├─ DNS integrity → DNSSEC (DNSKEY, RRSIG, DS)
   └─ Certificate control → CAA record
```

### Common Use Cases

**Static Website:**
```
example.com.     3600  IN  A      192.0.2.1
www.example.com. 3600  IN  CNAME  example.com.
```

**Website + Email (Google Workspace):**
```
example.com.     3600  IN  A   192.0.2.1
www.example.com. 3600  IN  CNAME  example.com.
example.com.     3600  IN  MX  1  aspmx.l.google.com.
example.com.     3600  IN  TXT "v=spf1 include:_spf.google.com ~all"
```

**CDN (CloudFront):**
```
example.com.     3600  IN  ALIAS  d111111abcdef8.cloudfront.net.
www.example.com. 3600  IN  CNAME  d111111abcdef8.cloudfront.net.
```

**Load Balanced Application:**
```
example.com.  300  IN  A  192.0.2.1
example.com.  300  IN  A  192.0.2.2
example.com.  300  IN  A  192.0.2.3
```

**Subdomain Delegation:**
```
api.example.com.  86400  IN  NS  ns1.apihost.com.
api.example.com.  86400  IN  NS  ns2.apihost.com.
```

---

## Quick Reference Table

| Record Type | Zone Apex | Subdomain | Multiple | TTL Recommendation |
|-------------|-----------|-----------|----------|-------------------|
| A | ✅ | ✅ | ✅ | 3600s |
| AAAA | ✅ | ✅ | ✅ | 3600s |
| CNAME | ❌ | ✅ | ❌ | 3600-86400s |
| ALIAS | ✅ | ✅ | ❌ | Auto |
| MX | ✅ | ✅ | ✅ | 3600-86400s |
| TXT | ✅ | ✅ | ✅ | 3600s |
| SRV | ❌ | ✅ | ✅ | 3600-86400s |
| NS | ✅ | ✅ | ✅ | 86400s |
| CAA | ✅ | ✅ | ✅ | 3600-86400s |

**Legend:**
- ✅ Allowed
- ❌ Not allowed
- Auto: Managed by provider
