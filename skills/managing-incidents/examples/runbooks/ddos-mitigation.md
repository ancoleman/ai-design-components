# Runbook: DDoS Mitigation

## Metadata

- **Runbook ID:** RB-SEC-001
- **Owner:** Security & Infrastructure Team (@security-team, @infrastructure-team)
- **Last Updated:** 2025-12-05
- **Version:** 2.0
- **Estimated Duration:** 15-30 minutes (initial mitigation), ongoing monitoring

---

## Trigger Conditions

Execute this runbook when:
- Abnormal traffic spike (> 10x normal request rate)
- Infrastructure resource exhaustion (CPU, memory, bandwidth saturation)
- Application unresponsive due to traffic volume
- Alert indicating DDoS attack pattern (bot signatures, geographic anomalies)
- CDN/WAF reporting attack traffic

**Alert Names:**
- `DDoS-Attack-Detected`
- `Traffic-Anomaly-Critical`
- `Infrastructure-Resource-Exhaustion`
- `CDN-DDoS-Mitigation-Active`
- `Rate-Limit-Exceeded-Widespread`

**External Indicators:**
- CDN dashboard showing attack (Cloudflare Under Attack Mode triggered)
- Customer reports: "Website extremely slow or unavailable"
- Network operations center (NOC) notification

---

## Severity Classification

**Expected Severity:** SEV0 (Critical Outage) - SEV1 (Major Degradation)

**Reasoning:**
- **SEV0:** Complete service unavailability, infrastructure saturated, revenue loss
- **SEV1:** Service degraded but functional, partial availability, legitimate traffic affected

**Severity Decision:**

```
Is service completely unavailable to legitimate users?
├─ YES → SEV0 (Page immediately 24/7, all hands, executive notification)
└─ NO  → Is service significantly degraded (latency > 5s, error rate > 10%)?
          ├─ YES → SEV1 (Page during business hours, IC assigned, security team engaged)
          └─ NO  → SEV2 (Monitor closely, prepare for escalation)
```

---

## Prerequisites

Before executing, verify:

1. **Confirm DDoS Attack (Not Legitimate Traffic):**
   ```bash
   # Check traffic patterns in monitoring
   curl https://monitoring.example.com/api/v1/query?query=rate(http_requests_total[5m])

   # Check geographic distribution (unusual countries?)
   curl https://monitoring.example.com/api/v1/query?query=http_requests_by_country

   # Check User-Agent distribution (bot signatures?)
   # Access CDN/WAF dashboard for bot detection scores
   ```

   **DDoS Indicators:**
   - Traffic spike > 10x normal without marketing event
   - Unusual geographic sources (countries you don't serve)
   - Repetitive User-Agent strings (bot signatures)
   - Single IP or small IP range generating high volume
   - Request patterns (same endpoint repeatedly, random query strings)

   **Legitimate Traffic Indicators:**
   - Gradual increase aligned with marketing campaign
   - Normal geographic distribution
   - Diverse User-Agents (real browsers/apps)
   - Expected referrers (social media, press coverage)

   **If Legitimate Traffic Spike:** Do NOT proceed with DDoS mitigation. Instead, scale infrastructure (see RB-SCALE-001).

2. **Identify Attack Type:**
   - **Layer 7 (Application):** HTTP/HTTPS floods targeting specific endpoints
   - **Layer 4 (Transport):** SYN floods, UDP floods (requires network-level mitigation)
   - **Layer 3 (Network):** ICMP floods, IP fragmentation attacks

   Most application-level incidents are Layer 7 attacks (HTTP floods).

3. **Required Access:**
   - CDN dashboard access (Cloudflare, Fastly, Akamai)
   - WAF configuration access (AWS WAF, Cloudflare WAF, Imperva)
   - Kubernetes/infrastructure admin access
   - DNS management access (for traffic shifting)
   - Slack channels: #security-incidents, #infrastructure

4. **Incident Declaration:**
   ```
   Post in #security-incidents:
   "@here SEV0/SEV1 - DDoS attack detected. Declaring incident.
   Traffic volume: [X req/s, normal: Y req/s]
   Impact: [Service status, customer impact]
   Incident channel: #incident-YYYY-MM-DD-ddos
   IC: @[incident-commander]
   Security lead: @[security-oncall]"
   ```

5. **Executive Notification (SEV0):**
   - Notify VP Engineering, CTO immediately via phone
   - Prepare status page update draft
   - Alert customer support team for incoming tickets

---

## Steps

### Step 1: Immediate Damage Control

**Purpose:** Reduce immediate impact while investigating.

#### Quick Win 1: Enable CDN DDoS Protection (If Available)

**Cloudflare:**
```bash
# Enable "I'm Under Attack Mode" (aggressive challenge page)
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/security_level" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"value": "under_attack"}'
```

**Impact:** Shows challenge page to visitors, blocks most bots. May false-positive on API clients.

---

**AWS CloudFront:**
```bash
# Enable AWS Shield Standard (automatic, always on)
# For Shield Advanced (requires subscription):
aws shield create-protection \
  --name "CloudFront-DDoS-Protection" \
  --resource-arn "arn:aws:cloudfront::account-id:distribution/DISTRIBUTION_ID"
```

---

**Fastly:**
```bash
# Enable DDoS mitigation via API
curl -X POST "https://api.fastly.com/service/$SERVICE_ID/version/$VERSION/ddos" \
  -H "Fastly-Key: $FASTLY_API_KEY" \
  -d '{"enabled": true}'
```

---

#### Quick Win 2: Enable Rate Limiting

**Purpose:** Limit requests per IP to prevent single-source attacks.

**Cloudflare WAF:**
```bash
# Create rate limiting rule: 100 req/min per IP
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/rate_limits" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "threshold": 100,
    "period": 60,
    "action": {
      "mode": "challenge",
      "timeout": 86400
    },
    "match": {
      "request": {
        "url": "*"
      },
      "response": {
        "status": [200, 201, 202, 301, 302]
      }
    }
  }'
```

---

**Application-Level (Nginx):**
```nginx
# Edit nginx config
# /etc/nginx/conf.d/rate-limit.conf

limit_req_zone $binary_remote_addr zone=ddos_protection:10m rate=10r/s;

server {
    location / {
        limit_req zone=ddos_protection burst=20 nodelay;
        limit_req_status 429;
    }
}
```

```bash
# Reload nginx
sudo nginx -t && sudo nginx -s reload
```

---

#### Quick Win 3: Block Known Bad IPs (If Identified)

**Purpose:** Immediately block confirmed attack sources.

**Cloudflare:**
```bash
# Block specific IP or IP range
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/firewall/access_rules/rules" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "block",
    "configuration": {
      "target": "ip",
      "value": "192.0.2.1"
    },
    "notes": "DDoS attack source - blocked 2025-12-05"
  }'
```

---

**AWS WAF:**
```bash
# Create IP set
aws wafv2 create-ip-set \
  --name DDoS-Block-List \
  --scope REGIONAL \
  --ip-address-version IPV4 \
  --addresses 192.0.2.0/24 203.0.113.0/24

# Create rule to block IP set
aws wafv2 create-rule-group \
  --name DDoS-Block-Rules \
  --scope REGIONAL \
  --capacity 100 \
  --rules file://block-rule.json
```

---

### Step 2: Analyze Attack Pattern

**Purpose:** Understand attack vectors to implement targeted mitigations.

#### Analyze Traffic Logs

**Cloudflare Logs:**
```bash
# Export recent logs (requires Cloudflare Enterprise)
curl -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/logs/received?start=$(date -u -d '10 minutes ago' +%s)&end=$(date -u +%s)" \
  -H "Authorization: Bearer $CF_API_TOKEN" > ddos-logs.json

# Analyze top source IPs
cat ddos-logs.json | jq -r '.ClientIP' | sort | uniq -c | sort -rn | head -20

# Analyze top User-Agents
cat ddos-logs.json | jq -r '.ClientRequestUserAgent' | sort | uniq -c | sort -rn | head -20

# Analyze top requested paths
cat ddos-logs.json | jq -r '.ClientRequestURI' | sort | uniq -c | sort -rn | head -20
```

---

**Application Logs (Kubernetes):**
```bash
# Export API access logs
kubectl logs -l app=api -n production --tail=10000 | grep -E "GET|POST" > api-logs.txt

# Analyze top source IPs
awk '{print $1}' api-logs.txt | sort | uniq -c | sort -rn | head -20

# Analyze top endpoints
awk '{print $7}' api-logs.txt | sort | uniq -c | sort -rn | head -20
```

---

#### Identify Attack Characteristics

**Questions to Answer:**
1. **Volume:** Total req/s vs. normal baseline?
2. **Source:** Single IP, IP range, botnet (distributed IPs)?
3. **Geographic:** Specific countries/regions?
4. **Targets:** Specific endpoints or entire site?
5. **Patterns:** Random query strings? Specific User-Agents?
6. **HTTP Method:** GET floods? POST abuse?

**Example Analysis:**
```
Attack Profile:
- Volume: 50,000 req/s (normal: 2,000 req/s) = 25x spike
- Source: 5,000+ unique IPs (distributed botnet)
- Geographic: 80% traffic from Eastern Europe, Southeast Asia
- Target: /api/v1/search endpoint (expensive query)
- Pattern: Random search queries, consistent User-Agent "python-requests/2.28.0"
- Method: GET requests with complex query parameters
```

---

### Step 3: Implement Targeted Mitigations

**Purpose:** Block attack traffic while preserving legitimate user access.

#### Mitigation A: Block Bot User-Agents

**Use when:** Attack uses consistent bot User-Agent strings.

**Cloudflare WAF:**
```bash
# Block specific User-Agent
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/firewall/rules" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "expression": "(http.user_agent contains \"python-requests\")"
    },
    "action": "block",
    "description": "Block DDoS bot User-Agent"
  }'
```

---

**Nginx:**
```nginx
# /etc/nginx/conf.d/block-bots.conf
if ($http_user_agent ~* (python-requests|curl|wget|bot|crawler)) {
    return 403;
}
```

---

#### Mitigation B: Geographic Blocking

**Use when:** Attack originates from countries you don't serve.

**Cloudflare:**
```bash
# Block specific countries (use ISO 3166-1 alpha-2 codes)
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/firewall/rules" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "expression": "(ip.geoip.country in {\"CN\" \"RU\" \"KP\"})"
    },
    "action": "challenge",
    "description": "Challenge traffic from high-risk countries during DDoS"
  }'
```

**Note:** Use "challenge" instead of "block" to avoid false positives (VPN users, legitimate traffic).

---

**AWS WAF:**
```bash
# Create geo-blocking rule
aws wafv2 create-rule-group \
  --name GeoBlock-DDoS \
  --scope REGIONAL \
  --capacity 50 \
  --rules file://geo-block-rule.json
```

**geo-block-rule.json:**
```json
[
  {
    "Name": "BlockHighRiskCountries",
    "Priority": 0,
    "Statement": {
      "GeoMatchStatement": {
        "CountryCodes": ["CN", "RU", "KP"]
      }
    },
    "Action": {
      "Block": {}
    },
    "VisibilityConfig": {
      "SampledRequestsEnabled": true,
      "CloudWatchMetricsEnabled": true,
      "MetricName": "GeoBlockRule"
    }
  }
]
```

---

#### Mitigation C: Endpoint-Specific Protection

**Use when:** Attack targets specific expensive endpoints.

**Rate Limit Expensive Endpoints:**
```bash
# Cloudflare: Aggressive rate limit for /api/v1/search
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/rate_limits" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -d '{
    "threshold": 10,
    "period": 60,
    "action": {"mode": "block", "timeout": 3600},
    "match": {
      "request": {"url": "*/api/v1/search*"}
    }
  }'
```

---

**Require Authentication for Expensive Endpoints:**
```bash
# Temporarily require API key for /search endpoint
# (Requires application code change or feature flag)

curl -X POST https://api.example.com/admin/feature-flags \
  -H "Authorization: Bearer $ADMIN_API_TOKEN" \
  -d '{"flag": "search_requires_auth", "value": true}'
```

---

**Disable Endpoint Temporarily (LAST RESORT):**
```bash
# Return 503 Service Unavailable for /search endpoint
# Nginx config
location /api/v1/search {
    return 503 "Service temporarily unavailable due to maintenance";
}

# Reload nginx
sudo nginx -s reload
```

---

#### Mitigation D: CAPTCHA/JavaScript Challenge

**Use when:** Need to distinguish humans from bots.

**Cloudflare:**
```bash
# Enable JavaScript challenge (less intrusive than CAPTCHA)
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/security_level" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -d '{"value": "high"}'  # "high" = JS challenge for suspicious traffic
```

**Note:** Breaks API clients without JavaScript support. Use selectively.

---

#### Mitigation E: Scale Infrastructure (If Budget Allows)

**Use when:** Mitigation alone insufficient, need more capacity.

**Horizontal Scaling (Kubernetes):**
```bash
# Scale API deployment
kubectl scale deployment/api --replicas=20 -n production
# Normal: 5 replicas, Emergency: 20+ replicas

# Verify scaling
kubectl get pods -l app=api -n production
```

---

**AWS Auto Scaling:**
```bash
# Temporarily increase Auto Scaling Group max size
aws autoscaling update-auto-scaling-group \
  --auto-scaling-group-name api-asg \
  --max-size 50 \
  --desired-capacity 20
```

---

**Vertical Scaling (Last Resort, Requires Downtime):**
```bash
# Increase instance sizes (AWS)
# Switch from t3.medium → c5.2xlarge for CPU-intensive workloads
# Requires terraform/CloudFormation update and rolling restart
```

---

### Step 4: Monitor Mitigation Effectiveness

**Purpose:** Verify attack mitigated without blocking legitimate users.

```bash
# Monitor traffic volume
watch -n 10 'curl -s https://monitoring.example.com/api/v1/query?query=rate(http_requests_total[5m])'

# Monitor error rates
curl https://monitoring.example.com/api/v1/query?query=rate(api_errors_total[5m])

# Monitor API latency
curl https://monitoring.example.com/api/v1/query?query=http_request_duration_seconds{quantile="0.99"}

# Monitor infrastructure CPU/memory
curl https://monitoring.example.com/api/v1/query?query=node_cpu_seconds_total
```

**Success Criteria:**
- Traffic volume decreased to manageable levels (< 5x normal)
- Error rate < 1% (acceptable)
- API latency < 1 second (p99)
- Infrastructure CPU < 70%
- Legitimate user reports: No complaints about accessibility

**If Mitigation Insufficient:**
- Increase mitigation aggressiveness (rate limits, stricter challenges)
- Consider more drastic measures (whitelist-only mode, maintenance page)
- Escalate to DDoS mitigation specialist or CDN support

---

### Step 5: Engage External Support (If Needed)

**Purpose:** Leverage CDN/ISP DDoS mitigation services for large attacks.

#### Cloudflare DDoS Support

```
Contact Cloudflare Support:
- Email: support@cloudflare.com
- Phone: +1 (650) 319-8930 (Enterprise customers)
- Dashboard: Open support ticket

Provide:
- Zone ID: $ZONE_ID
- Attack start time
- Traffic volume metrics
- Current mitigations applied
```

**Cloudflare Enterprise:** DDoS Response Team available 24/7.

---

#### AWS Shield Advanced

**If Subscribed:**
```bash
# Engage AWS DDoS Response Team (DRT)
# Call AWS Support: +1-866-947-4287
# Or open case in AWS Console: Support → Create Case → DDoS Attack
```

**AWS DRT Can:**
- Apply custom mitigations at network edge
- Analyze attack traffic patterns
- Provide post-attack forensics

---

#### ISP/Upstream Provider

**For Network-Layer Attacks (Layer 3/4):**

```
Contact ISP/Network Provider:
- Report volumetric attack (bandwidth saturation)
- Request BGP blackholing or upstream filtering
- Provide: Source IPs, attack start time, traffic volume
```

**Example ISP Contacts:**
- AWS: Support case (Premium Support required)
- GCP: DDoS mitigation automatic (no action needed)
- Azure: Azure DDoS Protection Standard (automatic)

---

### Step 6: Communicate Status

**Purpose:** Keep stakeholders informed during ongoing attack.

#### Internal Updates (Every 15-30 Minutes)

```
Post in #incident-YYYY-MM-DD-ddos:

"[TIMESTAMP] Update #N - Mitigating

Current Status: Mitigating DDoS attack

Attack Profile:
- Volume: 50,000 req/s (down from 80,000 req/s)
- Type: Layer 7 HTTP flood targeting /api/v1/search
- Source: Distributed botnet (5,000+ IPs)

Mitigations Applied:
- ✅ Cloudflare "Under Attack Mode" enabled
- ✅ Rate limiting: 100 req/min per IP
- ✅ Blocked bot User-Agent: python-requests
- ✅ Geographic challenge: CN, RU, KP
- ✅ Endpoint-specific rate limit: /search (10 req/min)

Current Impact:
- Traffic reduced 60% from peak
- Error rate: 2% (down from 25%)
- API latency: 800ms p99 (down from 5s)
- Legitimate users: Minor slowness, no reports of blocking

Next Steps:
- Continue monitoring for 30 minutes
- Scale infrastructure if volume remains high
- Analyze logs for additional attack vectors

Next Update: [TIMESTAMP + 30min]"
```

---

#### External Status Page (SEV0)

```markdown
**[Timestamp] Investigating - API Performance**

We are investigating reports of slow API performance. Our team has identified and is actively mitigating a DDoS attack. Legitimate users may experience brief delays (1-2 seconds) while we block malicious traffic. No data is at risk. Updates every 15 minutes.
```

**Update when mitigated:**
```markdown
**[Timestamp] Monitoring - API Performance**

The DDoS attack has been successfully mitigated. API performance is returning to normal. We are monitoring closely to ensure stability. Legitimate users should experience normal performance within 5-10 minutes.
```

---

### Step 7: Forensics and Evidence Collection

**Purpose:** Gather evidence for post-mortem and potential legal action.

```bash
# Export attack logs (retain for 30+ days)
# Cloudflare
curl "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/logs/received?start=$ATTACK_START&end=$ATTACK_END" \
  -H "Authorization: Bearer $CF_API_TOKEN" > ddos-attack-logs-$(date +%Y%m%d).json

# Application logs
kubectl logs -l app=api -n production --since=3h > api-attack-logs-$(date +%Y%m%d).txt

# Infrastructure metrics (Prometheus)
curl "https://prometheus.example.com/api/v1/query_range?query=http_requests_total&start=$ATTACK_START&end=$ATTACK_END&step=60" > attack-metrics.json
```

**Evidence Checklist:**
- [ ] Full traffic logs (raw CDN/WAF logs)
- [ ] Application error logs
- [ ] Infrastructure metrics (CPU, memory, bandwidth)
- [ ] List of blocked IPs
- [ ] Attack timeline (start, peak, end)
- [ ] Mitigation actions taken (with timestamps)
- [ ] Customer impact assessment

**Retention:** Store for 90 days minimum (legal/forensic requirements).

---

### Step 8: Gradual Mitigation Relaxation

**Purpose:** Return to normal operation without re-exposing to attack.

**Wait Period:** Monitor for 2-4 hours after attack subsides before relaxing mitigations.

**Gradual Relaxation (Over 24-48 Hours):**

**Hour 2-4 (Initial Stability):**
```bash
# Reduce Cloudflare security level from "I'm Under Attack" to "High"
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/security_level" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -d '{"value": "high"}'

# Monitor for 2 hours - if stable, proceed
```

---

**Hour 4-8 (Partial Relaxation):**
```bash
# Loosen rate limits (100 → 200 req/min)
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/rate_limits/$RATE_LIMIT_ID" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -d '{"threshold": 200}'

# Monitor for 4 hours - if stable, proceed
```

---

**Hour 8-24 (Geographic Unblocking):**
```bash
# Change geographic blocks from "block" to "challenge"
# Or remove if false positives reported

# Remove User-Agent blocks if attack ceased
```

---

**Hour 24-48 (Return to Normal):**
```bash
# Return Cloudflare to "Medium" security level
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/security_level" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -d '{"value": "medium"}'

# Remove temporary rate limits
# Scale infrastructure back to normal capacity

# Keep monitoring for 7 days (potential repeat attacks)
```

---

## Rollback Procedure

**When to Rollback:**
- Mitigations blocking legitimate users (> 5% false positive rate)
- Customer complaints about accessibility
- Critical API clients unable to connect
- Business impact exceeds attack impact

**Rollback Steps:**

### Option A: Disable Specific Mitigation

```bash
# Identify problematic mitigation from customer reports

# Example: Remove User-Agent block
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/firewall/rules/$RULE_ID" \
  -H "Authorization: Bearer $CF_API_TOKEN"

# Example: Remove geographic block
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/firewall/access_rules/rules/$RULE_ID" \
  -H "Authorization: Bearer $CF_API_TOKEN"
```

---

### Option B: Whitelist Legitimate IPs/Ranges

```bash
# Add enterprise customer IP ranges to whitelist
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/firewall/access_rules/rules" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -d '{
    "mode": "whitelist",
    "configuration": {"target": "ip_range", "value": "203.0.113.0/24"},
    "notes": "Enterprise customer - always allow"
  }'
```

---

### Option C: Disable All Mitigations (LAST RESORT)

**Only if:** Mitigations causing more harm than attack.

```bash
# Disable Cloudflare "Under Attack Mode"
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/security_level" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -d '{"value": "medium"}'

# Remove all rate limiting rules
# Remove all firewall rules applied during incident

# Accept attack impact temporarily while refining mitigations
```

---

## Escalation Criteria

Escalate to Security Lead (@security-lead) if:
- Attack volume > 100,000 req/s (large-scale attack)
- Mitigations ineffective after 30 minutes
- Layer 3/4 network attack (requires ISP coordination)
- Suspected state-sponsored or advanced persistent threat
- Ransom demand received

Escalate to VP Engineering / CTO if:
- SEV0 lasting > 1 hour
- Revenue loss exceeding $10,000/hour
- Media attention or PR concern
- Legal threats or extortion

Escalate to Law Enforcement if:
- Extortion/ransom demand
- Suspected nation-state attack
- Attack part of larger campaign

---

## Common Issues and Solutions

### Issue 1: Mitigations Block Legitimate API Clients

**Symptom:** Mobile app or third-party integrations failing due to bot challenges.

**Solutions:**
- **Whitelist API Clients by IP:** Add known IPs to allowlist
- **API Key Authentication:** Bypass challenges for authenticated API requests
- **Dedicated API Subdomain:** `api.example.com` with less aggressive rules than `www.example.com`

**Cloudflare Bypass for API:**
```bash
# Allow authenticated API requests to bypass challenges
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/firewall/rules" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -d '{
    "filter": {
      "expression": "(http.host eq \"api.example.com\" and http.request.uri.path contains \"/v1/\")"
    },
    "action": "allow",
    "description": "Bypass challenges for API endpoints"
  }'
```

---

### Issue 2: Attack Resumes After Mitigation Relaxation

**Symptom:** Traffic spike returns after relaxing mitigations.

**Solutions:**
- **Re-enable Mitigations:** Return to aggressive posture
- **Gradual Relaxation:** Relax mitigations slower (over days, not hours)
- **Permanent Protections:** Keep baseline protections (moderate rate limiting, bot detection) permanently

---

### Issue 3: Distributed Botnet (Cannot Block by IP)

**Symptom:** Attack from 10,000+ unique IPs, blocking ineffective.

**Solutions:**
- **Behavioral Analysis:** Use machine learning/bot detection (Cloudflare Bot Management, AWS Bot Control)
- **JavaScript Challenge:** Require JavaScript execution (bots often fail)
- **CAPTCHA:** Human verification (last resort, UX impact)
- **Accept Capacity Cost:** Scale infrastructure to absorb attack if blocking ineffective

**Cloudflare Bot Management (Enterprise):**
```bash
# Enable bot detection and automatic mitigation
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/bot_management" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -d '{"value": "on"}'
```

---

### Issue 4: Attack Targeting Multiple Services Simultaneously

**Symptom:** Website, API, and DNS all under attack.

**Solutions:**
- **Coordinate Mitigations:** Apply protections across all services simultaneously
- **DNS Protection:** Use DNSSEC, DNS provider DDoS protection (Cloudflare, Route53)
- **Failover to Static Page:** Serve static "Under Maintenance" page from CDN if backend overwhelmed

---

## Post-Execution Checklist

After DDoS attack mitigated, verify:

- [ ] Traffic volume returned to normal (< 2x baseline)
- [ ] Error rate < 0.5% (normal)
- [ ] API latency < 200ms p99 (normal)
- [ ] Infrastructure scaled back to normal capacity
- [ ] Mitigations relaxed (if appropriate) or documented as permanent
- [ ] No legitimate user reports of blocking
- [ ] Logs and evidence exported and archived
- [ ] Status page updated: "Resolved"
- [ ] Team debriefed on attack and mitigations
- [ ] Post-mortem scheduled (within 48 hours)
- [ ] DDoS protection improvements identified

---

## Related Runbooks

- **RB-SCALE-001:** Infrastructure Scaling (if legitimate traffic spike)
- **RB-SEC-002:** Security Incident Response (if data breach suspected)
- **RB-NET-001:** Network Troubleshooting (if connectivity issues)

---

## DDoS Prevention Best Practices

### Architectural Defenses

**1. Use CDN/WAF:**
- Cloudflare, Fastly, Akamai absorb attacks at edge
- Automatically detect and block bot traffic
- Cost-effective compared to bandwidth overages

**2. Rate Limiting:**
- Application-level: Limit requests per user/IP
- Infrastructure-level: Nginx, HAProxy rate limits
- API: Require authentication, enforce quotas

**3. Caching:**
- Cache static content aggressively (images, CSS, JS)
- Cache dynamic content when possible (API responses)
- CDN caching reduces origin load

**4. Geofencing:**
- If serving specific regions, block other geos by default
- Use "challenge" instead of "block" to avoid VPN false positives

**5. Auto-Scaling:**
- Horizontal scaling (Kubernetes HPA, AWS Auto Scaling)
- Scale out during traffic spikes (legitimate or attack)
- Cost: Pay for capacity, but maintain availability

**6. Monitoring and Alerting:**
- Traffic volume anomaly detection
- Geographic distribution monitoring
- User-Agent pattern analysis
- Alert on traffic > 5x normal

---

### Testing and Validation

**Last Tested:** 2025-11-01 (tabletop exercise)
**Test Frequency:** Quarterly (tabletop), Annually (live drill with CDN)
**Next Test:** 2026-02-01

**Tabletop Exercise Procedure:**
1. Announce test in #security-team (1 week advance notice)
2. Simulate attack scenario (coordinator plays "attacker")
3. Team executes runbook in staging environment
4. Document gaps, improve runbook
5. No production impact

**Live Drill (Coordinated with CDN):**
1. Schedule with CDN provider (Cloudflare, Fastly)
2. Provider simulates attack against staging environment
3. Team executes mitigations
4. Measure MTTA, MTTR
5. Debrief and improve

---

## Changelog

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-12-05 | 2.0 | Major update: added mitigation patterns, forensics, relaxation process | @security-team |
| 2025-09-10 | 1.5 | Added Cloudflare Bot Management, AWS Shield | @alice |
| 2025-07-01 | 1.2 | Added geographic blocking, API client whitelist | @bob |
| 2025-05-01 | 1.0 | Initial version | @security-team |

---

## Contact

**Owner:** Security & Infrastructure Teams
**Slack:** #security-incidents (during attack), #security-team (general)
**On-Call:** @security-oncall, @infrastructure-oncall
**Escalation:** @security-lead, @infrastructure-director

**For questions or improvements:** Open PR against `runbooks/ddos-mitigation.md`

---

## Appendix: DDoS Attack Types Reference

### Layer 7 (Application Layer) Attacks

**HTTP Flood:**
- Large volume of HTTP GET/POST requests
- Targets application resources (web pages, API endpoints)
- Mitigation: Rate limiting, WAF, JavaScript challenge

**Slowloris:**
- Holds connections open by sending partial HTTP requests
- Exhausts server connection pool
- Mitigation: Connection timeouts, reverse proxy (Nginx, HAProxy)

**HTTP POST Flood:**
- Large POST requests with max allowed body size
- Exhausts bandwidth and application processing
- Mitigation: Request size limits, rate limiting

---

### Layer 4 (Transport Layer) Attacks

**SYN Flood:**
- Exploits TCP handshake, sends SYN packets without completing connection
- Exhausts connection state table
- Mitigation: SYN cookies (kernel level), ISP filtering

**UDP Flood:**
- Sends large volume of UDP packets to random ports
- Exhausts bandwidth and server resources
- Mitigation: ISP filtering, firewall rules

---

### Layer 3 (Network Layer) Attacks

**ICMP Flood (Ping Flood):**
- Large volume of ICMP Echo Request packets
- Saturates network bandwidth
- Mitigation: ICMP rate limiting, ISP filtering

**Amplification Attacks (DNS, NTP, Memcached):**
- Spoofs victim IP, sends small request to amplification service
- Service responds with large payload to victim
- Mitigation: Disable open resolvers, ISP filtering

---

## Appendix: Cloudflare DDoS Protection Levels

| Level | Protection | Impact on Users | Use Case |
|-------|-----------|----------------|----------|
| Essentially Off | Minimal | None | Low-risk sites, development |
| Low | Basic bot detection | None | Normal operation |
| Medium | Moderate bot detection | None | Normal operation (DEFAULT) |
| High | JavaScript challenge for suspicious | Slight delay (< 1s) | Elevated threat |
| I'm Under Attack | Challenge page for all | 5-second challenge page | Active DDoS attack |

**Recommendation:** Use "Medium" normally, "High" for threats, "I'm Under Attack" only during active attack.
