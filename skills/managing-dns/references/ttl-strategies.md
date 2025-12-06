# TTL Strategies - Detailed Reference

Complete guide to Time-To-Live (TTL) strategies for DNS records with scenarios, calculations, and best practices.

## Table of Contents

1. [TTL Fundamentals](#ttl-fundamentals)
2. [TTL by Scenario](#ttl-by-scenario)
3. [Propagation Calculations](#propagation-calculations)
4. [Change Management Strategies](#change-management-strategies)
5. [TTL by Record Type](#ttl-by-record-type)
6. [Common Mistakes](#common-mistakes)

---

## TTL Fundamentals

### What is TTL?

Time-To-Live (TTL) is the duration (in seconds) that DNS resolvers cache a DNS record before querying the authoritative nameserver again.

**Key Concepts:**
- **Lower TTL** = Faster propagation but more DNS queries (higher load)
- **Higher TTL** = Slower propagation but fewer DNS queries (lower load, faster responses)
- **Old TTL matters** = When changing a record, the old TTL must expire first

### TTL Trade-offs

| Aspect | Low TTL (60-300s) | High TTL (3600-86400s) |
|--------|-------------------|------------------------|
| **Propagation Speed** | Fast (minutes) | Slow (hours) |
| **DNS Query Load** | High | Low |
| **DNS Costs** | Higher (more queries) | Lower |
| **Resolution Speed** | Slower (more lookups) | Faster (cached) |
| **Flexibility** | High (quick changes) | Low (slow changes) |
| **Use Case** | Dynamic, failover | Stable, production |

### TTL in DNS Resolution

```
User Request → Local Resolver
                ├─ Cache Hit (within TTL) → Return cached result
                └─ Cache Miss (expired TTL) → Query authoritative server
                                              ├─ Get new record + TTL
                                              └─ Cache for TTL duration
```

**Example Timeline:**
```
T+0s:    Record created with TTL 3600s
T+100s:  First query → Cached for 3600s
T+200s:  Second query → Returns cached result (3500s remaining)
T+3700s: Third query → TTL expired, queries authoritative again
```

---

## TTL by Scenario

### Scenario 1: Normal Operation (Stable Infrastructure)

**Goal:** Minimize DNS queries, optimize performance

**Recommended TTL Values:**
```
A/AAAA records:    3600s (1 hour)
CNAME records:     3600-86400s (1-24 hours)
MX records:        3600-86400s (1-24 hours)
TXT records:       3600-86400s (1-24 hours)
NS records:        86400s (24 hours)
CAA records:       3600-86400s (1-24 hours)
```

**Rationale:**
- Servers are stable and IP addresses rarely change
- Reduces load on authoritative DNS servers
- Improves resolution time for cached queries
- Balances flexibility with efficiency

**Example Configuration:**
```
# Zone file
example.com.     3600   IN  A      192.0.2.1
www.example.com. 3600   IN  CNAME  example.com.
example.com.     86400  IN  MX     10 mail.example.com.
example.com.     3600   IN  TXT    "v=spf1 include:_spf.google.com ~all"
example.com.     86400  IN  NS     ns1.example.com.
```

---

### Scenario 2: Pre-Change Preparation

**Goal:** Enable fast propagation for upcoming DNS changes

**Timeline:**
```
T-48h: Lower TTL to 300s (5 minutes)
T-24h: Verify TTL has propagated globally
       └─ Check: dig example.com | grep -A1 "ANSWER"
T-0h:  Make the DNS change
T+1h:  Verify new records propagating
       └─ Check multiple resolvers
T+6h:  Verify global propagation
       └─ Use whatsmydns.net
T+24h: Raise TTL back to normal (3600s)
```

**Commands:**
```bash
# T-48h: Lower TTL
# (Update via DNS provider or IaC)

# T-24h: Verify TTL propagated
dig example.com | grep -A1 "ANSWER SECTION"
# Should show: example.com. 300 IN A 192.0.2.1

# T+1h: Check propagation
dig @8.8.8.8 example.com +short       # Google DNS
dig @1.1.1.1 example.com +short       # Cloudflare DNS
dig @208.67.222.222 example.com +short # OpenDNS

# T+6h: Global check
# Visit: https://www.whatsmydns.net/#A/example.com
```

**Why 48 Hours?**
- Old TTL (3600s = 1 hour) must expire
- Safety margin for global propagation
- Allows time to verify new TTL active

---

### Scenario 3: Blue-Green Deployment

**Goal:** Switch traffic quickly between environments

**Strategy:**
```
Phase 1: Preparation (T-48h)
├─ Current: Blue environment (192.0.2.1)
├─ Action: Lower TTL to 300s
└─ Verify: TTL propagated

Phase 2: Deployment (T-0h)
├─ Deploy: Green environment (192.0.2.2)
├─ Test: Validate green environment ready
└─ Monitor: Keep blue running

Phase 3: Cutover (T+0h)
├─ Update: Change DNS to green (192.0.2.2)
├─ Monitor: Traffic shifting to green
└─ Timeline: Full cutover in ~10 minutes (300s TTL + buffer)

Phase 4: Verification (T+30m)
├─ Verify: All traffic on green
├─ Monitor: Error rates, performance
└─ Keep: Blue environment running (rollback ready)

Phase 5: Stabilization (T+24h)
├─ Decommission: Blue environment (if stable)
├─ Raise TTL: Back to 1800s (30 min) for 24h
└─ Final raise: Back to 3600s (1 hour) after 48h
```

**Example:**
```bash
# T-48h: Lower TTL
# Blue environment
example.com.  300  IN  A  192.0.2.1

# T-0h: Switch to green
example.com.  300  IN  A  192.0.2.2

# Verify propagation
dig @8.8.8.8 example.com +short        # Should show 192.0.2.2
dig @1.1.1.1 example.com +short        # Should show 192.0.2.2

# T+24h: Gradual TTL increase
example.com.  1800  IN  A  192.0.2.2

# T+48h: Back to normal
example.com.  3600  IN  A  192.0.2.2
```

**Rollback Process:**
```bash
# If issues detected within 30 minutes
# Simply change DNS back to blue
example.com.  300  IN  A  192.0.2.1

# Traffic will shift back in ~5 minutes
```

---

### Scenario 4: DNS-Based Failover

**Goal:** Fastest possible failover to backup systems

**Configuration:**
```
Primary:   192.0.2.1 (health checked every 30s)
Secondary: 192.0.2.2 (standby)
TTL:       60-300s (1-5 minutes)
```

**Recommended TTL:**
- **Active-active**: 60-120s (fast failover, both active)
- **Active-passive**: 120-300s (moderate failover, standby ready)
- **Health check interval**: 30-60s
- **Failure threshold**: 2-3 consecutive failures

**Example (Route53):**
```hcl
# Health check configuration
resource "aws_route53_health_check" "primary" {
  fqdn              = "primary.example.com"
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3       # 3 failures = unhealthy
  request_interval  = 30      # Check every 30 seconds
}

# Primary record with health check
resource "aws_route53_record" "primary" {
  zone_id         = aws_route53_zone.main.zone_id
  name            = "api.example.com"
  type            = "A"
  ttl             = 60        # Fast failover
  set_identifier  = "primary"

  failover_routing_policy {
    type = "PRIMARY"
  }

  health_check_id = aws_route53_health_check.primary.id
  records         = ["192.0.2.1"]
}

# Secondary record (no health check needed)
resource "aws_route53_record" "secondary" {
  zone_id         = aws_route53_zone.main.zone_id
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
```
T+0s:   Primary server fails
T+30s:  First health check failure
T+60s:  Second health check failure
T+90s:  Third health check failure → Route53 marks unhealthy
T+90s:  New DNS queries return secondary IP
T+150s: All clients using secondary (90s detection + 60s TTL)

Total failover time: ~2.5 minutes
```

**Optimizing Failover Time:**
- **Lower TTL**: 60s instead of 300s (saves 4 minutes)
- **Faster health checks**: 10s interval (Route53 premium)
- **Lower failure threshold**: 2 failures instead of 3 (saves 30s)

**Trade-off:**
- Faster failover = More DNS queries + higher costs
- Recommended minimum: 60s TTL for production

---

### Scenario 5: Canary/Weighted Routing

**Goal:** Gradually shift traffic to new version

**Strategy:**
```
Phase 1: Initial canary (10%)
├─ Old version: Weight 90, TTL 60s
└─ New version: Weight 10, TTL 60s

Phase 2: Expand canary (30%)
├─ Old version: Weight 70, TTL 60s
└─ New version: Weight 30, TTL 60s

Phase 3: Majority canary (70%)
├─ Old version: Weight 30, TTL 60s
└─ New version: Weight 70, TTL 60s

Phase 4: Full cutover (100%)
├─ Remove: Old version record
└─ New version: Weight 100, TTL 300s

Phase 5: Stabilize
└─ New version: Standard TTL 3600s
```

**Example (Route53):**
```hcl
# 90% to stable version
resource "aws_route53_record" "stable" {
  zone_id        = aws_route53_zone.main.zone_id
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
  zone_id        = aws_route53_zone.main.zone_id
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

**TTL Considerations:**
- **During canary**: 60-120s (adjust weights quickly)
- **After full cutover**: 300s (moderate)
- **Stable state**: 3600s (normal)

---

### Scenario 6: Dynamic DNS (DDNS)

**Goal:** Keep DNS updated with changing IP addresses

**Recommended TTL:** 30-60 minutes (half of DHCP lease time)

**Configuration:**
```
DHCP Lease:       60 minutes
DNS TTL:          30 minutes
Update Frequency: Every 15-30 minutes
```

**Rationale:**
- TTL shorter than DHCP lease prevents stale records
- Update frequency ensures IP change captured
- Not too short to avoid excessive DNS queries

**Example (ddclient configuration):**
```
# /etc/ddclient.conf
daemon=1800                 # Update every 30 minutes
protocol=cloudflare
zone=example.com
ttl=1800                    # 30 minutes
login=token
password=your-api-token
example.com
```

**Common DDNS Services:**
- Cloudflare: Supports DDNS via API
- Route53: Supported via route53-ddns
- No-IP, DynDNS: Dedicated DDNS services
- Router built-in: Many routers support DDNS

---

### Scenario 7: GeoDNS / Latency-Based Routing

**Goal:** Route users to nearest/fastest endpoint

**Recommended TTL:** 300-900s (5-15 minutes)

**Rationale:**
- Moderate TTL balances performance and flexibility
- Allows rebalancing if endpoint performance changes
- Not too low (users don't move that fast)
- Not too high (allows for outage response)

**Example (Route53):**
```hcl
# US endpoint
resource "aws_route53_record" "us" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  ttl            = 300
  set_identifier = "us-east-1"

  latency_routing_policy {
    region = "us-east-1"
  }

  records = ["192.0.2.1"]
}

# EU endpoint
resource "aws_route53_record" "eu" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  ttl            = 300
  set_identifier = "eu-west-1"

  latency_routing_policy {
    region = "eu-west-1"
  }

  records = ["192.0.2.10"]
}
```

---

## Propagation Calculations

### Formula

```
Maximum Propagation Time = Old TTL + New TTL + DNS Query Time
```

**Components:**
- **Old TTL**: Cached records must expire (worst case: full TTL)
- **New TTL**: New records may be cached immediately
- **Query Time**: Usually negligible (<1s) but add buffer

### Examples

**Example 1: Changing stable record**
```
Old TTL:   3600s (1 hour)
New TTL:   3600s (1 hour)
Query:     ~5s
────────────────────────────
Max Time:  ~2 hours 5 seconds

Timeline:
T+0:       Change made
T+3600:    Old TTL expires, new records queried
T+7200:    All caches have new record
```

**Example 2: Pre-lowered TTL change**
```
Old TTL:   300s (5 minutes)
New TTL:   300s (5 minutes)
Query:     ~5s
────────────────────────────
Max Time:  ~10 minutes 5 seconds

Timeline:
T+0:       Change made
T+300:     Old TTL expires, new records queried
T+600:     All caches have new record
```

**Example 3: Emergency change (high TTL)**
```
Old TTL:   86400s (24 hours)
New TTL:   300s (5 minutes)
Query:     ~5s
────────────────────────────
Max Time:  ~24 hours 5 minutes

Timeline:
T+0:       Emergency change made
T+86400:   Old TTL expires (worst case)
T+86700:   All caches have new record
```

### Propagation Tables

| Old TTL | New TTL | Max Propagation | Typical Scenario |
|---------|---------|----------------|------------------|
| 60s | 60s | ~2 min | Failover (fast) |
| 300s | 300s | ~10 min | Pre-lowered change |
| 3600s | 300s | ~1h 5min | Emergency with high TTL |
| 3600s | 3600s | ~2h | Normal change |
| 86400s | 300s | ~24h 5min | Emergency without prep |

**Key Insight:** Old TTL matters most! Always plan ahead by lowering TTL before changes.

---

## Change Management Strategies

### Strategy 1: Planned Change (Recommended)

```
Step 1 (T-48h): Lower TTL to 300s
├─ Update DNS records with TTL 300s
├─ Verify change applied
└─ Wait 48 hours for global propagation

Step 2 (T-24h): Verify low TTL active
├─ Check: dig example.com | grep TTL
├─ Expected: 300s or less
└─ Proceed if verified

Step 3 (T-0h): Make DNS change
├─ Update A/CNAME/etc records
├─ Keep TTL at 300s
└─ Monitor propagation

Step 4 (T+6h): Verify global propagation
├─ Check multiple resolvers
├─ Use whatsmydns.net
└─ Confirm 100% propagation

Step 5 (T+24h): Raise TTL (gradual)
├─ Raise to 1800s (30 min)
└─ Monitor for 24h

Step 6 (T+48h): Restore normal TTL
├─ Raise to 3600s (1 hour)
└─ Normal operation resumed
```

**Pros:**
- Predictable propagation (~10 minutes)
- Low risk of extended outages
- Can plan during maintenance window

**Cons:**
- Requires 48h+ planning
- Increased DNS queries during low TTL period

---

### Strategy 2: Emergency Change (Unplanned)

```
Step 1 (T-0h): Make change immediately
├─ Update DNS with lowest possible TTL (60-300s)
├─ Accept propagation will take old TTL duration
└─ Monitor closely

Step 2 (T+0h to T+old_TTL): Monitor propagation
├─ Check multiple resolvers
├─ Communicate expected propagation time
└─ Wait for old TTL to expire

Step 3 (T+old_TTL): Verify completion
├─ Confirm global propagation
└─ Service restored

Step 4 (T+24h): Normalize TTL
├─ Gradually raise TTL back to normal
└─ Document incident
```

**Example Timeline (Old TTL = 3600s):**
```
T+0:       Emergency change made
T+1h:      Old TTL expires, some users see new records
T+2h:      Most users on new records
T+3h:      Virtually all users migrated
T+24h:     Raise TTL back to normal
```

**Pros:**
- Immediate action possible
- No pre-planning required

**Cons:**
- Extended propagation time
- Unpredictable user experience during transition

---

### Strategy 3: Hybrid (Best of Both)

```
Default State:
├─ Critical records: TTL 300-600s (always low)
├─ Standard records: TTL 3600s (normal)
└─ Stable records: TTL 86400s (very stable)

Change Process:
├─ Critical records: Change immediately (~10 min propagation)
├─ Standard records: Use planned strategy (48h prep)
└─ Stable records: Plan weeks in advance
```

**Example Classification:**
```
Critical (TTL 300s):
- API endpoints
- Load balancer records
- Failover targets

Standard (TTL 3600s):
- Website A records
- CDN CNAMEs
- Mail server A records

Stable (TTL 86400s):
- NS records
- Static subdomains
- Long-term CNAMEs
```

---

## TTL by Record Type

### Recommended TTL Values

| Record Type | Normal Operation | Before Change | Rationale |
|-------------|------------------|---------------|-----------|
| **A/AAAA** | 3600s (1h) | 300s (5min) | Balance flexibility and performance |
| **CNAME** | 3600-86400s | 300s | Usually stable, point to stable targets |
| **MX** | 3600-86400s | 300s | Mail servers rarely change |
| **TXT (SPF/DKIM)** | 3600-86400s | 3600s | Email auth rarely changes |
| **TXT (verification)** | 3600s | N/A | Can remove after verification |
| **SRV** | 3600-86400s | 300s | Services relatively stable |
| **NS** | 86400-172800s | 86400s | Very stable, rarely change |
| **CAA** | 3600-86400s | 3600s | Certificate policy stable |
| **PTR (reverse)** | 86400s | 86400s | Rarely changes |

### Special Considerations

**MX Records:**
- Higher TTL acceptable (3600-86400s)
- Email delivery retries automatically
- Rarely need emergency changes

**NS Records:**
- Highest TTL (86400-172800s = 1-2 days)
- Changes are very rare
- Plan changes weeks in advance
- Update both parent and child zone

**TXT Records:**
- Verification records: 3600s (can remove after verification)
- SPF/DKIM/DMARC: 3600-86400s (rarely change)
- API keys/tokens: 3600s (moderate flexibility)

---

## Common Mistakes

### Mistake 1: TTL Too High Before Changes

**Problem:**
```bash
# Day 1: Record with 24-hour TTL
example.com.  86400  IN  A  192.0.2.1

# Day 2: Emergency - need to change IP
# Problem: Must wait 24 hours for full propagation!
```

**Solution:**
- Maintain moderate TTL (3600s) for production records
- Lower TTL 48h before planned changes
- Keep critical records at lower TTL (300s) always

---

### Mistake 2: Setting TTL to 0

**Problem:**
```bash
# ❌ WRONG - TTL of 0
example.com.  0  IN  A  192.0.2.1
```

**Why It's Bad:**
- Resolvers ignore TTL of 0 (use minimum instead)
- Causes excessive queries to authoritative servers
- No performance benefit
- May be treated as error by some resolvers

**Solution:**
- Minimum TTL: 60s (1 minute)
- Recommended minimum: 300s (5 minutes)

---

### Mistake 3: Not Waiting for Old TTL

**Problem:**
```bash
# T+0h: Change DNS
# T+5min: "Why isn't it working?!"
# Old TTL was 3600s - must wait 1 hour!
```

**Solution:**
- Check current TTL before making changes
- Communicate expected propagation time
- Use propagation formula: Old TTL + New TTL

---

### Mistake 4: Forgetting to Raise TTL After Change

**Problem:**
```bash
# After emergency change, TTL left at 60s
# Result: Excessive DNS queries forever
# Higher costs, slower performance
```

**Solution:**
- Schedule TTL normalization 24-48h after change
- Document TTL changes in change management
- Use infrastructure-as-code to enforce standards

---

### Mistake 5: Inconsistent TTL Across Records

**Problem:**
```bash
example.com.      3600  IN  A      192.0.2.1
www.example.com.  60    IN  CNAME  example.com.
# CNAME refreshes every minute, but points to record cached for 1 hour
```

**Solution:**
- Keep related records at similar TTL
- A record and CNAME should have similar TTL
- Coordinate TTL changes across record sets

---

## TTL Best Practices Summary

### Golden Rules

1. **Default to 3600s (1 hour)** for most production records
2. **Lower to 300s (5 min)** 48 hours before planned changes
3. **Keep NS records high** (86400s / 24 hours)
4. **Never use 0** (minimum 60s, recommended 300s)
5. **Raise TTL after changes** (don't leave at low values)
6. **Monitor DNS query costs** (lower TTL = higher costs)
7. **Document TTL strategy** in runbooks

### Quick Decision Matrix

```
How often does this change?
├─ Never → 86400s (24h)
├─ Rarely (years) → 86400s (24h)
├─ Occasionally (months) → 3600s (1h)
├─ Regularly (weeks) → 1800s (30min)
├─ Frequently (days) → 300-600s (5-10min)
└─ Very frequently (hours) → 60-300s (1-5min)

Is this critical for failover?
├─ Yes → 60-300s (1-5min)
└─ No → Use frequency-based rule above

Are DNS costs a concern?
├─ Yes → Use higher TTLs (3600-86400s)
└─ No → Optimize for flexibility (300-3600s)
```

### Monitoring TTL Effectiveness

**Metrics to Track:**
- DNS query volume (lower TTL = higher volume)
- DNS resolution time (higher TTL = faster, more cached)
- Propagation time during changes (lower TTL = faster)
- DNS costs (provider-specific)

**Adjust TTL if:**
- Query volume too high → Raise TTL
- Changes take too long → Lower TTL (or pre-plan)
- Costs too high → Raise TTL
- Failover too slow → Lower TTL for critical records
