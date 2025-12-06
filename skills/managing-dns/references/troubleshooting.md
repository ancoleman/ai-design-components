# DNS Troubleshooting - Detailed Reference

Complete guide to diagnosing and resolving common DNS issues with tools, commands, and solutions.

## Table of Contents

1. [Essential DNS Tools](#essential-dns-tools)
2. [Common Problems and Solutions](#common-problems-and-solutions)
3. [Diagnostic Workflows](#diagnostic-workflows)
4. [Provider-Specific Issues](#provider-specific-issues)
5. [Propagation Checkers](#propagation-checkers)

---

## Essential DNS Tools

### dig (Domain Information Groper)

Primary DNS debugging tool on Unix/Linux/macOS.

**Basic Queries:**
```bash
# Simple query
dig example.com

# Clean output (just the answer)
dig example.com +short

# Specific record type
dig example.com A
dig example.com AAAA
dig example.com MX
dig example.com TXT
dig example.com NS
dig example.com CAA
```

**Query Specific DNS Server:**
```bash
# Google DNS
dig @8.8.8.8 example.com

# Cloudflare DNS
dig @1.1.1.1 example.com

# Quad9
dig @9.9.9.9 example.com

# OpenDNS
dig @208.67.222.222 example.com

# Authoritative nameserver
dig @ns1.example.com example.com
```

**Advanced Queries:**
```bash
# Trace DNS resolution path
dig +trace example.com
# Shows: root servers → TLD servers → authoritative servers → answer

# Check TTL
dig example.com | grep -A1 "ANSWER SECTION"
# Output: example.com. 300 IN A 192.0.2.1
#                      ^^^ TTL value

# DNSSEC validation
dig example.com +dnssec

# Reverse DNS lookup
dig -x 192.0.2.1

# Only show answer section
dig example.com +noall +answer

# Show query time
dig example.com +stats
```

---

### nslookup

Cross-platform DNS query tool (Windows/Unix/Linux/macOS).

**Basic Usage:**
```bash
# Simple query
nslookup example.com

# Query specific server
nslookup example.com 8.8.8.8

# Interactive mode
nslookup
> server 8.8.8.8
> set type=MX
> example.com
> set type=TXT
> example.com
> exit
```

**Query Types:**
```bash
# MX records
nslookup -type=MX example.com

# NS records
nslookup -type=NS example.com

# TXT records
nslookup -type=TXT example.com

# Any record
nslookup -type=ANY example.com
```

---

### host

Simple DNS lookup utility.

**Usage:**
```bash
# Simple lookup
host example.com

# Verbose output
host -v example.com

# Specific record type
host -t MX example.com
host -t TXT example.com
host -t NS example.com

# Query specific server
host example.com 8.8.8.8

# All records
host -a example.com
```

---

### whois

Domain registration and nameserver information.

**Usage:**
```bash
# Domain registration info
whois example.com

# Specific section
whois example.com | grep -i "name server"
whois example.com | grep -i "registrar"
whois example.com | grep -i "expir"
```

---

### DNS Cache Flushing

**macOS:**
```bash
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

# Verify cache cleared
sudo dscacheutil -cachedump -entries Host
```

**Windows:**
```cmd
ipconfig /flushdns
ipconfig /displaydns  # View cache
```

**Linux (systemd-resolved):**
```bash
sudo systemd-resolve --flush-caches
sudo systemd-resolve --statistics

# resolvectl (newer)
sudo resolvectl flush-caches
```

**Linux (nscd):**
```bash
sudo /etc/init.d/nscd restart
# or
sudo systemctl restart nscd
```

**Linux (dnsmasq):**
```bash
sudo systemctl restart dnsmasq
```

---

## Common Problems and Solutions

### Problem 1: DNS Propagation Delays

**Symptoms:**
- Changes not visible after DNS update
- Some locations see new records, others see old
- Client reports "not working" but you see updated records

**Diagnosis:**
```bash
# Check current TTL
dig example.com | grep -A1 "ANSWER SECTION"
# If TTL is high (e.g., 3600s), propagation will take that long

# Check authoritative server directly
dig @$(dig example.com NS +short | head -1) example.com
# This shows what the authoritative server returns

# Check multiple public resolvers
dig @8.8.8.8 example.com +short       # Google
dig @1.1.1.1 example.com +short       # Cloudflare
dig @208.67.222.222 example.com +short # OpenDNS

# Check from client's resolver
dig example.com
# Shows what the client's resolver is caching
```

**Solutions:**

**Solution 1: Wait for TTL to Expire**
```
Max propagation time = Old TTL + New TTL
Example: Old TTL 3600s means up to 1 hour wait
```

**Solution 2: Pre-Lower TTL (Future Prevention)**
```bash
# 48 hours before change
# Lower TTL to 300s

# Make change
# Propagation now only ~10 minutes

# 24 hours after change
# Raise TTL back to 3600s
```

**Solution 3: Flush Local Cache**
```bash
# Client-side
# macOS
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder

# Windows
ipconfig /flushdns

# Linux
sudo systemd-resolve --flush-caches
```

**Solution 4: Verify with Propagation Checkers**
- https://www.whatsmydns.net/
- https://dnschecker.org/
- https://dnspropagation.net/

---

### Problem 2: CNAME at Zone Apex Error

**Symptoms:**
- Error: "CNAME conflicts with other records at apex"
- Cannot point example.com (not www) to CDN
- DNS validation fails for CNAME at @

**Diagnosis:**
```bash
# Check for CNAME at zone apex
dig example.com CNAME

# Check for SOA record (conflicts with CNAME)
dig example.com SOA

# Verify nameservers
dig example.com NS
```

**Explanation:**
CNAME records cannot exist at the zone apex because:
1. SOA and NS records must exist at zone apex
2. CNAME cannot coexist with other records
3. RFC 1912 restriction

**Solutions:**

**Solution 1: Use ALIAS Record (Provider-Specific)**
```hcl
# Route53 ALIAS
resource "aws_route53_record" "apex" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "example.com"
  type    = "A"

  alias {
    name                   = "d111111abcdef8.cloudfront.net"
    zone_id                = "Z2FDTNDATAQYW2"
    evaluate_target_health = false
  }
}

# Cloudflare (automatic CNAME flattening)
resource "cloudflare_record" "apex" {
  zone_id = cloudflare_zone.main.id
  name    = "example.com"
  type    = "CNAME"
  value   = "d111111abcdef8.cloudfront.net"
  proxied = true
}
```

**Solution 2: Use A/AAAA Record**
```bash
# If CDN provides static IP
example.com.  300  IN  A  192.0.2.1
```

**Solution 3: Use Subdomain**
```bash
# Point www to CDN
www.example.com.  3600  IN  CNAME  cdn.provider.com.

# Redirect apex to www at application level
example.com.  300  IN  A  192.0.2.1  # Your redirect server
```

---

### Problem 3: Missing DNS Records After Migration

**Symptoms:**
- Some services stop working after DNS provider migration
- Email or subdomains not resolving
- Incomplete zone transfer

**Diagnosis:**
```bash
# Export all record types from old provider
for type in A AAAA CNAME MX TXT SRV CAA NS SOA; do
  echo "=== $type records ==="
  dig @old-ns1.provider.com example.com $type +noall +answer
done

# Compare with new provider
for type in A AAAA CNAME MX TXT SRV CAA NS SOA; do
  echo "=== $type records ==="
  dig @new-ns1.provider.com example.com $type +noall +answer
done

# Check for zone transfer support (usually disabled)
dig @old-ns1.provider.com example.com AXFR
```

**Solutions:**

**Solution 1: Audit Before Migration**
```bash
# Create complete inventory
# Save to file for comparison
dig @old-ns1.provider.com example.com ANY > old-dns.txt

# After migration, compare
dig @new-ns1.provider.com example.com ANY > new-dns.txt
diff old-dns.txt new-dns.txt
```

**Solution 2: Use DNS Migration Tools**
```bash
# OctoDNS to export existing config
octodns-dump \
  --config-file=octodns-config.yaml \
  --output-dir=./backup \
  example.com

# Import to new provider
octodns-sync \
  --config-file=octodns-config.yaml \
  --doit
```

**Solution 3: Parallel Operation**
```bash
# Keep old provider active for 48 hours
# Add both old and new NS records temporarily
# Verify all records migrated before full cutover
```

**Solution 4: Common Missed Records**
```bash
# Often forgotten:
# - TXT records (SPF, DKIM, DMARC, verification)
# - SRV records (VoIP, XMPP)
# - CAA records
# - Wildcard records (*.example.com)
# - Subdomain delegations (NS records)

# Verify each:
dig example.com TXT +short
dig example.com CAA +short
dig _dmarc.example.com TXT +short
dig *.example.com A +short
```

---

### Problem 4: DNS Loops or CNAME Chains

**Symptoms:**
- DNS resolution fails
- Error: "CNAME loop detected"
- Timeout or SERVFAIL response

**Diagnosis:**
```bash
# Trace CNAME chain
dig +trace www.example.com

# Check for circular references
dig www.example.com CNAME +short
# If returns www.example.com → loop!

# Visualize chain
dig www.example.com +noall +answer
```

**Examples of Loops:**
```bash
# ❌ Direct loop
www.example.com.  IN  CNAME  www.example.com.

# ❌ Indirect loop
www.example.com.  IN  CNAME  web.example.com.
web.example.com.  IN  CNAME  www.example.com.

# ❌ Excessive chain (>5 hops)
www → cdn → lb → app → backend → server → IP
```

**Solutions:**

**Solution 1: Break the Loop**
```bash
# Identify loop point
dig +trace www.example.com

# Fix: Point to A record instead
www.example.com.  IN  A  192.0.2.1
```

**Solution 2: Limit CNAME Depth**
```bash
# ✅ Good: 1-2 hops
www.example.com.   IN  CNAME  cdn.example.com.
cdn.example.com.   IN  A      192.0.2.1

# ❌ Bad: 5+ hops
# Causes slow resolution, potential timeouts
```

**Solution 3: Use A Records for Final Target**
```bash
# Always terminate CNAME chain with A/AAAA
app.example.com.   IN  CNAME  lb.example.com.
lb.example.com.    IN  A      192.0.2.1  # Terminal record
```

---

### Problem 5: external-dns Not Creating Records

**Symptoms:**
- Kubernetes Service/Ingress has annotation
- No DNS record created
- external-dns logs show errors

**Diagnosis:**
```bash
# Check external-dns logs
kubectl logs -n external-dns deployment/external-dns -f

# Check Service annotations
kubectl get service nginx -o yaml | grep -A5 annotations

# Verify domain filter
kubectl logs -n external-dns deployment/external-dns | grep "domain-filter"

# Check provider credentials
kubectl get secret -n external-dns

# Test DNS provider access
kubectl logs -n external-dns deployment/external-dns | grep -i "error\|fail"
```

**Common Issues and Solutions:**

**Issue 1: Domain Not in Filter**
```bash
# Check current filter
kubectl describe deployment -n external-dns external-dns | grep domain-filter

# Fix: Add domain to filter
helm upgrade external-dns external-dns/external-dns \
  --namespace external-dns \
  --set domainFilters[0]=example.com \
  --reuse-values
```

**Issue 2: Missing Provider Credentials**
```bash
# Check secret exists
kubectl get secret -n external-dns external-dns

# Create secret (AWS example)
kubectl create secret generic external-dns \
  --namespace external-dns \
  --from-literal=aws_access_key_id=$AWS_ACCESS_KEY_ID \
  --from-literal=aws_secret_access_key=$AWS_SECRET_ACCESS_KEY
```

**Issue 3: Wrong Policy**
```bash
# Check current policy
kubectl describe deployment -n external-dns external-dns | grep policy

# upsert-only: Only creates, doesn't delete
# sync: Creates and deletes (recommended)

# Fix: Change to sync
helm upgrade external-dns external-dns/external-dns \
  --namespace external-dns \
  --set policy=sync \
  --reuse-values
```

**Issue 4: Annotation Typo**
```yaml
# ❌ WRONG - typo in annotation name
metadata:
  annotations:
    external-dns.alpha.kubernetes.io/hostnam: example.com  # Missing 'e'

# ✅ CORRECT
metadata:
  annotations:
    external-dns.alpha.kubernetes.io/hostname: example.com
    external-dns.alpha.kubernetes.io/ttl: "300"
```

**Issue 5: LoadBalancer Not Ready**
```bash
# Check Service status
kubectl get service nginx

# external-dns waits for LoadBalancer IP/hostname
# If EXTERNAL-IP is <pending>, external-dns cannot create record

# Solution: Wait for LoadBalancer to provision
# Or use type: NodePort with externalIPs
```

---

### Problem 6: DNSSEC Validation Failures

**Symptoms:**
- SERVFAIL responses
- Works with some resolvers, not others
- dig +dnssec shows bogus status

**Diagnosis:**
```bash
# Check DNSSEC status
dig example.com +dnssec

# Validate DNSSEC chain
dig example.com +dnssec +multiline

# Check with validating resolver
dig @1.1.1.1 example.com +dnssec
dig @8.8.8.8 example.com +dnssec

# Verify DS record at parent
dig example.com DS +trace
```

**Common DNSSEC Issues:**

**Issue 1: Missing DS Record at Registrar**
```bash
# Check parent zone for DS record
dig example.com DS

# If missing, DNSSEC chain is broken
# Solution: Add DS record at domain registrar
```

**Issue 2: Key Rotation Problems**
```bash
# DNSSEC keys expire
# Provider should auto-rotate

# Check key expiration
dig example.com DNSKEY +multiline

# Solution: Use provider-managed DNSSEC
# AWS Route53, Google Cloud DNS, Cloudflare all auto-rotate
```

**Issue 3: Clock Skew**
```bash
# DNSSEC signatures are time-sensitive
# Check server time
date

# Ensure NTP is running
timedatectl status
```

---

## Diagnostic Workflows

### Workflow 1: Website Not Resolving

```bash
# Step 1: Verify DNS record exists
dig example.com +short
# Expected: IP address
# If empty: Record doesn't exist or TTL expired

# Step 2: Check authoritative nameservers
dig example.com NS +short
# Expected: List of nameservers

# Step 3: Query authoritative directly
dig @$(dig example.com NS +short | head -1) example.com
# Compare with Step 1

# Step 4: Check propagation
dig @8.8.8.8 example.com +short
dig @1.1.1.1 example.com +short
# Should match authoritative answer

# Step 5: Trace full resolution path
dig +trace example.com
# Shows root → TLD → authoritative → answer

# Step 6: Check client cache
dig example.com
# If different from Step 4, flush client cache

# Step 7: Verify TTL
dig example.com | grep -A1 "ANSWER"
# If high TTL, wait for expiration
```

---

### Workflow 2: Email Delivery Issues

```bash
# Step 1: Check MX records
dig example.com MX +short
# Expected: Priority and mail server

# Step 2: Verify mail server A records
dig mail.example.com A +short
# Mail server must resolve

# Step 3: Check SPF record
dig example.com TXT +short | grep "v=spf1"
# Should include mail servers

# Step 4: Check DMARC
dig _dmarc.example.com TXT +short
# Should have DMARC policy

# Step 5: Check DKIM
dig default._domainkey.example.com TXT +short
# Should have public key

# Step 6: Test from multiple resolvers
dig @8.8.8.8 example.com MX +short
dig @1.1.1.1 example.com MX +short

# Step 7: Verify reverse DNS (PTR)
dig -x <mail-server-ip>
# Should match forward lookup
```

---

### Workflow 3: SSL Certificate Not Working

```bash
# Step 1: Check A record
dig example.com +short
# Must resolve to server IP

# Step 2: Check CAA records
dig example.com CAA +short
# If exists, must allow certificate authority

# Step 3: Check DNS propagation
# Certificate authorities check DNS globally
dig @8.8.8.8 example.com +short
dig @1.1.1.1 example.com +short
# Must be consistent

# Step 4: Verify TXT record (if using DNS challenge)
dig _acme-challenge.example.com TXT +short
# Must match CA's challenge value

# Step 5: Check TTL
dig _acme-challenge.example.com TXT | grep TTL
# If high, CA may cache old value

# Step 6: Test CAA compatibility
dig example.com CAA +short
# Example: 0 issue "letsencrypt.org"
```

---

## Provider-Specific Issues

### AWS Route53 Issues

**Issue: ALIAS Record Not Resolving**
```bash
# Check if target resource exists
dig d111111abcdef8.cloudfront.net +short

# Verify ALIAS configuration
aws route53 list-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --query "ResourceRecordSets[?Name=='example.com.']"

# Common mistake: Wrong zone ID for target
# Each AWS service has specific zone IDs
```

**Issue: Health Check Failing**
```bash
# View health check status
aws route53 get-health-check-status \
  --health-check-id abc123

# Test endpoint manually
curl -I https://example.com/health

# Check health check configuration
aws route53 get-health-check \
  --health-check-id abc123
```

---

### Google Cloud DNS Issues

**Issue: Private Zone Not Resolving**
```bash
# Verify VPC link
gcloud dns managed-zones describe internal-zone

# Check VM is in linked VPC
gcloud compute instances list --filter="name=my-vm"

# Test from VM in VPC
gcloud compute ssh my-vm --command "dig db.internal.example.com"

# If fails, check VPC link
gcloud dns managed-zones describe internal-zone \
  --format="json" | jq '.privateVisibilityConfig'
```

---

### Cloudflare Issues

**Issue: Orange Cloud (Proxied) Showing Cloudflare IP**
```bash
# Check if record is proxied
dig example.com +short
# If shows Cloudflare IP (104.x.x.x), record is proxied

# To see origin IP
# Option 1: Use DNS query to origin
dig @origin-nameserver.cloudflare.com example.com

# Option 2: Temporarily disable proxy
# (Cloudflare dashboard or API)

# Option 3: Query specific Cloudflare DNS
dig example.com A +short @1.1.1.1
```

---

## Propagation Checkers

### Online Tools

**Recommended:**
- **https://www.whatsmydns.net/** - Best visual interface
- **https://dnschecker.org/** - Comprehensive global check
- **https://dnspropagation.net/** - Clean interface
- **https://www.digwebinterface.com/** - Advanced options

**How to Use:**
1. Enter domain name
2. Select record type (A, AAAA, MX, etc.)
3. View results from 20+ global locations
4. Green checkmarks = propagated
5. Wait and recheck if not propagated

### Command-Line Propagation Check

**Check Multiple Resolvers:**
```bash
#!/bin/bash
# check-propagation.sh

DOMAIN=$1
RECORD_TYPE=${2:-A}

resolvers=(
  "8.8.8.8 (Google)"
  "8.8.4.4 (Google Secondary)"
  "1.1.1.1 (Cloudflare)"
  "1.0.0.1 (Cloudflare Secondary)"
  "208.67.222.222 (OpenDNS)"
  "208.67.220.220 (OpenDNS Secondary)"
  "9.9.9.9 (Quad9)"
  "64.6.64.6 (Verisign)"
)

echo "Checking DNS propagation for $DOMAIN ($RECORD_TYPE)"
echo "================================================"

for resolver in "${resolvers[@]}"; do
  ip=$(echo $resolver | awk '{print $1}')
  name=$(echo $resolver | cut -d'(' -f2 | cut -d')' -f1)
  result=$(dig @$ip $DOMAIN $RECORD_TYPE +short | head -1)
  echo "$name: $result"
done
```

**Usage:**
```bash
chmod +x check-propagation.sh
./check-propagation.sh example.com A
./check-propagation.sh example.com MX
```

---

## Quick Reference

### Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| NXDOMAIN | Domain doesn't exist | Check spelling, verify NS records |
| SERVFAIL | Server failure | Check authoritative NS, DNSSEC issues |
| REFUSED | Query refused | Nameserver doesn't serve this zone |
| TIMEOUT | No response | Network issue, firewall, wrong NS |
| NOERROR (no answer) | Zone exists but record doesn't | Add missing record |

### Quick Diagnostic Commands

```bash
# Essential checks
dig example.com +short           # Basic resolution
dig example.com NS +short        # Nameservers
dig example.com +trace           # Full resolution path
dig example.com | grep TTL       # Current TTL

# Propagation check
dig @8.8.8.8 example.com +short  # Google
dig @1.1.1.1 example.com +short  # Cloudflare

# Cache flush
# macOS: sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
# Windows: ipconfig /flushdns
# Linux: sudo systemd-resolve --flush-caches
```

---

## When to Contact Support

Contact DNS provider support when:
- Authoritative nameservers not responding (TIMEOUT)
- DNSSEC validation consistently fails
- Zone transfers not working
- Provider dashboard shows errors
- Records not updating after 24+ hours
- Health checks failing for working endpoints
- API/automation not working with valid credentials

Before contacting support, gather:
- Domain name
- Record type and value
- Screenshots of configuration
- Output of `dig +trace example.com`
- External propagation checker results
- Timeline of changes made
