# Runbook: Cache Invalidation

## Metadata

- **Runbook ID:** RB-CACHE-001
- **Owner:** Platform Engineering Team (@platform-team)
- **Last Updated:** 2025-12-05
- **Version:** 1.3
- **Estimated Duration:** 5-10 minutes

---

## Trigger Conditions

Execute this runbook when:
- Stale data detected in production (users seeing outdated content)
- Code deployment requires cache clear (API schema changes, pricing updates)
- Configuration changes not reflecting (feature flags, A/B test variants)
- Corrupted cache entries causing application errors
- Emergency data correction requiring immediate propagation

**Alert Names:**
- `Cache-Stale-Data-Detected`
- `Cache-Hit-Rate-Anomaly`
- `API-Serving-Old-Data`

**Manual Triggers:**
- Post-deployment cache clear requested by engineering team
- Customer support escalation reporting stale data
- Product team requesting immediate content update propagation

---

## Severity Classification

**Expected Severity:** SEV2 (Minor Issues) - SEV1 (Major Degradation)

**Reasoning:**
- **SEV2:** Limited data staleness, affects subset of users, workaround available (hard refresh)
- **SEV1:** Critical data incorrect (pricing, inventory, permissions), widespread user impact
- **SEV0:** Escalate only if incorrect cached data causing financial loss or security vulnerability

**Severity Decision:**

```
Is cached data causing security vulnerability or financial loss?
├─ YES → SEV0 (Page immediately, declare incident)
└─ NO  → Is critical business data incorrect (pricing, inventory, auth)?
          ├─ YES → SEV1 (Page during business hours, IC assigned)
          └─ NO  → SEV2 (Slack alert, execute runbook during business hours)
```

---

## Prerequisites

Before executing, verify:

1. **Cache System Health:**
   ```bash
   # Check Redis cluster health
   redis-cli -h cache-cluster.example.com PING
   # Expected: PONG

   # Check cluster info
   redis-cli -h cache-cluster.example.com CLUSTER INFO
   # Expected: cluster_state:ok
   ```

2. **Identify Cache Scope:**
   Determine what needs invalidation:
   - **Global:** Entire cache (all keys) - RARE, high impact
   - **Namespace:** Specific service or feature (`user:*`, `product:*`)
   - **Pattern:** Keys matching pattern (`product:123:*`, `session:abc*`)
   - **Single Key:** Specific cache entry (`product:456`, `user:789:profile`)

3. **Impact Assessment:**
   ```bash
   # Check current cache hit rate
   redis-cli -h cache-cluster.example.com INFO stats | grep keyspace_hits

   # Estimate keys affected
   redis-cli -h cache-cluster.example.com --scan --pattern "product:*" | wc -l
   ```

4. **Required Access:**
   - Redis CLI access or admin credentials
   - Kubernetes access (if invalidating via API)
   - Monitoring dashboard access
   - Slack channel: #platform-engineering

5. **Database Load Check:**
   ```bash
   # Verify database can handle cache miss traffic
   curl https://monitoring.example.com/api/v1/query?query=database_cpu_percent
   # Expected: < 60% (buffer for cache miss spike)
   ```

   **WARNING:** Invalidating large cache volumes causes database load spike. If DB CPU > 70%, consult DBA before proceeding.

---

## Steps

### Step 1: Announce Cache Invalidation

**Purpose:** Notify team and prepare for potential brief performance impact.

```
Post in #platform-engineering (or incident channel if SEV1):

"@here Executing cache invalidation for [scope: global/namespace/pattern].
Expected impact: Potential brief latency increase (1-2 minutes) as cache rebuilds.
Reason: [Brief reason: stale data, deployment, config change]
ETA for completion: [TIMESTAMP + 5-10 minutes]"
```

**If SEV1/SEV0:** Post status page update (see `communication-templates.md`).

---

### Step 2: Verify Database Can Handle Load

**Purpose:** Prevent cascading failure from database overload.

```bash
# Check database connection pool
curl https://monitoring.example.com/api/v1/query?query=database_connection_pool_usage

# Check database CPU
curl https://monitoring.example.com/api/v1/query?query=database_cpu_percent

# Check query queue depth
curl https://monitoring.example.com/api/v1/query?query=database_query_queue_length
```

**Health Criteria:**
- Database CPU < 60%
- Connection pool usage < 70%
- Query queue depth < 100

**If Database Unhealthy:**
- **Option A:** Partial invalidation (invalidate keys in batches)
- **Option B:** Scale database read replicas first
- **Option C:** Escalate to @db-sre-oncall for guidance

---

### Step 3: Choose Invalidation Method

**Purpose:** Select appropriate method based on scope and urgency.

#### Option A: Pattern-Based Invalidation (RECOMMENDED)

**Use when:** Need to invalidate specific namespace or pattern (most common).

```bash
# Connect to Redis
redis-cli -h cache-cluster.example.com

# Scan and delete keys matching pattern
redis-cli -h cache-cluster.example.com --scan --pattern "product:*" | xargs redis-cli -h cache-cluster.example.com DEL

# For large datasets (> 10,000 keys), use batching
redis-cli -h cache-cluster.example.com --scan --pattern "product:*" | while read key; do
  redis-cli -h cache-cluster.example.com DEL "$key"
  sleep 0.01  # Rate limit to avoid overwhelming Redis
done
```

**Verification:**
```bash
# Confirm keys deleted
redis-cli -h cache-cluster.example.com --scan --pattern "product:*" | wc -l
# Expected: 0 (or significantly reduced count)
```

---

#### Option B: Single Key Invalidation

**Use when:** Need to invalidate specific cache entry.

```bash
# Delete single key
redis-cli -h cache-cluster.example.com DEL "product:456"

# Verify deletion
redis-cli -h cache-cluster.example.com EXISTS "product:456"
# Expected: (integer) 0
```

---

#### Option C: Namespace Invalidation via API

**Use when:** Application provides cache invalidation API endpoint.

```bash
# POST to invalidation endpoint
curl -X POST https://api.example.com/admin/cache/invalidate \
  -H "Authorization: Bearer $ADMIN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace": "product",
    "reason": "Product pricing update",
    "force": true
  }'

# Expected Response
# {"status": "success", "keys_invalidated": 1234, "duration_ms": 543}
```

---

#### Option D: Time-Based Expiration Update (GENTLE)

**Use when:** Not urgent, prefer gradual invalidation.

```bash
# Reduce TTL to 60 seconds for gradual invalidation
redis-cli -h cache-cluster.example.com --scan --pattern "product:*" | while read key; do
  redis-cli -h cache-cluster.example.com EXPIRE "$key" 60
done
```

**Benefit:** Avoids sudden cache miss spike, cache naturally expires over 1 minute.

---

#### Option E: Global Cache Flush (NUCLEAR OPTION)

**Use when:** Complete cache corruption, all data stale, no other option.

**WARNING:** Causes massive database load spike. Only use in emergencies after consulting IC and DBA.

```bash
# DANGER: Flushes entire Redis database
redis-cli -h cache-cluster.example.com FLUSHDB

# For multi-node cluster, flush all nodes
for node in cache-node-1 cache-node-2 cache-node-3; do
  redis-cli -h $node.example.com FLUSHDB
done
```

**Pre-Flush Requirements:**
- [ ] IC approval obtained
- [ ] Database team notified and standing by
- [ ] Monitoring dashboard open
- [ ] Rollback plan ready (restore from Redis persistence if available)

---

### Step 4: Verify Cache Invalidation

**Purpose:** Confirm keys deleted and cache rebuilding correctly.

```bash
# Check keys deleted
redis-cli -h cache-cluster.example.com --scan --pattern "product:*" | wc -l
# Expected: 0 or significantly reduced

# Monitor cache miss rate (should spike briefly)
curl https://monitoring.example.com/api/v1/query?query=rate(cache_misses_total[1m])

# Monitor cache hit rate (should recover within 2-5 minutes)
curl https://monitoring.example.com/api/v1/query?query=cache_hit_rate

# Check API latency (may increase briefly)
curl https://monitoring.example.com/api/v1/query?query=http_request_duration_seconds{quantile="0.99"}
```

**Expected Behavior:**
- Cache miss rate spikes immediately (2-10x normal)
- API latency increases briefly (1.5-2x normal)
- Cache hit rate recovers within 2-5 minutes
- Database CPU increases temporarily (10-20% increase)

---

### Step 5: Verify Data Freshness

**Purpose:** Confirm new data correctly propagating to users.

#### Test with API Request

```bash
# Fetch data via API (should trigger cache rebuild)
curl -v https://api.example.com/v1/products/456 | jq '.updated_at'

# Verify response contains fresh data
# Expected: Timestamp shows recent update (not stale value)
```

#### Test from User Perspective

```bash
# Test from multiple regions (if multi-region cache)
for region in us-east us-west eu-west; do
  echo "Testing region: $region"
  curl -H "X-Region: $region" https://api.example.com/v1/products/456 | jq '.updated_at'
done

# Expected: All regions return fresh data
```

#### Manual Verification Checklist

- [ ] Load affected page/API endpoint in browser/Postman
- [ ] Verify data shows expected values (not stale)
- [ ] Check multiple users/sessions if user-specific cache
- [ ] Verify across all regions if multi-region deployment

---

### Step 6: Monitor for Stability

**Purpose:** Ensure cache invalidation didn't cause secondary issues.

**Monitor for 10-15 minutes:**

```bash
# Watch cache hit rate recovery
watch -n 5 'redis-cli -h cache-cluster.example.com INFO stats | grep keyspace_hits'

# Monitor API error rate
curl https://monitoring.example.com/api/v1/query?query=rate(api_errors_total[5m])

# Monitor database CPU
curl https://monitoring.example.com/api/v1/query?query=database_cpu_percent

# Monitor API latency
curl https://monitoring.example.com/api/v1/query?query=http_request_duration_seconds{quantile="0.99"}
```

**Monitoring Dashboard:** https://monitoring.example.com/dashboard/cache-health

**Stability Criteria:**
- Cache hit rate > 85% (recovered to normal)
- API error rate < 0.5% (normal baseline)
- Database CPU < 70% (normal range)
- API p99 latency < 500ms (acceptable)

**If Unstable:** See "Rollback" section below.

---

### Step 7: Update Team and Close

**Purpose:** Notify team of completion and document outcome.

```
Post in #platform-engineering (or incident channel):

"Cache invalidation complete.
- Keys invalidated: [N keys or pattern]
- Duration: [X minutes]
- Cache hit rate recovered: [Y%]
- API latency returned to normal: p99 [Z]ms
- Database CPU stable: [N%]
- No errors detected.

Monitoring for next 30 minutes. Will close if stable."
```

**If SEV1/SEV0:** Post status page update: "Monitoring - Issue resolved, watching for stability."

---

### Step 8: Document in Incident Timeline (If SEV1+)

**Purpose:** Record actions for post-mortem.

```
Post in incident channel:

"[TIMESTAMP] Cache invalidation executed
- Scope: [Pattern/namespace]
- Method: [Pattern-based / API / Manual]
- Keys invalidated: [N]
- Impact: Brief latency increase (1-2 minutes), cache rebuilt successfully
- Verification: Fresh data confirmed across all regions
- Monitoring: Stable"
```

---

## Rollback Procedure

**When to Rollback:**
- Database overload (CPU > 90%, query queue growing)
- API error rate spike (> 5%)
- Cache not rebuilding (hit rate stuck < 50% after 10 minutes)
- Application errors from malformed cache data

**Rollback Steps:**

### Option A: Restore from Redis Persistence (If Available)

```bash
# Stop Redis
redis-cli -h cache-cluster.example.com SHUTDOWN SAVE

# Restore from last RDB snapshot (if persistence enabled)
# SSH to Redis server
ssh admin@cache-cluster.example.com
sudo cp /var/lib/redis/dump.rdb.backup /var/lib/redis/dump.rdb
sudo systemctl start redis

# Verify restoration
redis-cli -h cache-cluster.example.com DBSIZE
# Expected: Previous key count restored
```

---

### Option B: Disable Cache Temporarily

**Use when:** Cache causing more problems than solving.

```bash
# Set feature flag to bypass cache
curl -X POST https://api.example.com/admin/feature-flags \
  -H "Authorization: Bearer $ADMIN_API_TOKEN" \
  -d '{"flag": "cache_enabled", "value": false}'

# Verify flag set
curl https://api.example.com/admin/feature-flags/cache_enabled
# Expected: {"flag": "cache_enabled", "value": false}
```

**Impact:** API latency increases 2-3x, database load increases 3-5x. Only sustainable short-term.

**Recovery:** Fix underlying issue, re-enable cache gradually:
```bash
# Re-enable cache
curl -X POST https://api.example.com/admin/feature-flags \
  -d '{"flag": "cache_enabled", "value": true}'
```

---

### Option C: Rate-Limit Cache Rebuilds

**Use when:** Cache rebuilding too aggressively, overwhelming database.

```bash
# Implement application-level rate limiting for cache writes
# (Requires code change or runtime config if supported)

# Temporary: Reduce Redis connection pool to slow cache writes
kubectl set env deployment/api REDIS_POOL_SIZE=10 -n production
```

---

## Escalation Criteria

Escalate to Senior Engineer (@platform-lead) if:
- Database CPU > 90% after invalidation
- API error rate > 5%
- Cache hit rate not recovering (< 50% after 15 minutes)
- Unclear which keys to invalidate
- Global flush being considered

Escalate to VP Engineering if:
- SEV0 incident (financial/security impact)
- Customer data integrity concerns
- Multi-region cache synchronization failure

---

## Common Issues and Solutions

### Issue 1: Cache Not Rebuilding

**Symptom:** Cache hit rate remains low (< 50%) 10+ minutes after invalidation.

**Solutions:**
- **Check Application Health:** Verify API pods running: `kubectl get pods -n production`
- **Check Redis Connection:** Verify app can connect to Redis: `kubectl logs deployment/api -n production | grep redis`
- **Check Database:** Verify DB responding: `pg_isready -h primary-db.example.com`
- **Manual Cache Warm:** Trigger cache population via script or API calls

**Manual Cache Warm:**
```bash
# Warm cache with top 100 product pages
for id in {1..100}; do
  curl https://api.example.com/v1/products/$id > /dev/null
  sleep 0.1
done
```

---

### Issue 2: Database Overload

**Symptom:** Database CPU > 80%, query queue growing, API timeouts.

**Solutions:**
- **Pause Invalidation:** Stop if using batched approach
- **Scale Read Replicas:** Add temporary read replicas (AWS RDS/GCP Cloud SQL)
- **Enable Query Caching:** Database-level query cache if available
- **Rate Limit Traffic:** Temporarily rate limit API requests

**Emergency Database Relief:**
```bash
# Scale RDS read replicas (AWS)
aws rds create-db-instance-read-replica \
  --db-instance-identifier mydb-replica-temp \
  --source-db-instance-identifier mydb-primary \
  --db-instance-class db.r5.large

# Takes 5-10 minutes to provision
```

---

### Issue 3: Multi-Region Cache Desync

**Symptom:** Some regions showing fresh data, others showing stale data.

**Solutions:**
- **Invalidate Each Region Separately:**
  ```bash
  for region in us-east us-west eu-west; do
    redis-cli -h cache-$region.example.com --scan --pattern "product:*" | xargs redis-cli -h cache-$region.example.com DEL
  done
  ```
- **Check Replication Lag:** If using Redis replication between regions
- **Verify CDN Purge:** If using CDN, purge CDN cache separately:
  ```bash
  # Cloudflare purge
  curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
    -H "Authorization: Bearer $CF_API_TOKEN" \
    -d '{"tags": ["product"]}'
  ```

---

### Issue 4: Accidentally Deleted Wrong Keys

**Symptom:** Unintended cache keys deleted, unrelated functionality broken.

**Solutions:**
- **Restore from Backup:** If Redis persistence enabled, restore from RDB snapshot
- **Rebuild Specific Namespace:** Re-populate accidentally deleted keys:
  ```bash
  # Trigger cache rebuild for specific namespace
  curl -X POST https://api.example.com/admin/cache/rebuild \
    -d '{"namespace": "user", "async": true}'
  ```
- **Wait for Natural Rebuild:** Cache will rebuild on-demand as users access data

---

## Post-Execution Checklist

After completing cache invalidation, verify:

- [ ] Targeted keys successfully deleted
- [ ] Fresh data verified via API/browser
- [ ] Cache hit rate recovered (> 85%)
- [ ] API latency returned to normal (< 200ms p99)
- [ ] Database CPU returned to baseline (< 60%)
- [ ] No application errors detected
- [ ] Multi-region consistency verified (if applicable)
- [ ] Team notified of completion
- [ ] Incident timeline updated (if SEV1+)
- [ ] Runbook updated if steps changed

---

## Related Runbooks

- **RB-DB-001:** Database Failover (if cache overload causes DB issues)
- **RB-PERF-001:** Performance Troubleshooting (if latency remains high)
- **RB-CDN-001:** CDN Cache Purge (if CDN also caching stale data)

---

## Cache Invalidation Patterns

### Pattern 1: Deployment-Triggered Invalidation

**Use when:** Code deployment changes API schema or data format.

**Automation:**
```yaml
# GitHub Actions workflow
- name: Invalidate cache post-deployment
  run: |
    curl -X POST https://api.example.com/admin/cache/invalidate \
      -H "Authorization: Bearer ${{ secrets.ADMIN_API_TOKEN }}" \
      -d '{"namespace": "api_v1", "reason": "Deployment ${{ github.sha }}"}'
```

---

### Pattern 2: Time-Based Auto-Expiration

**Use when:** Data naturally becomes stale over time (news, prices).

**Implementation:**
```bash
# Set TTL when writing to cache (application code)
redis-cli SET "product:456:price" "29.99" EX 3600  # 1 hour TTL

# Or update TTLs in bulk
redis-cli --scan --pattern "product:*" | while read key; do
  redis-cli EXPIRE "$key" 3600
done
```

---

### Pattern 3: Event-Driven Invalidation

**Use when:** Backend data changes should immediately invalidate cache.

**Implementation (Pseudocode):**
```python
# After database write
def update_product(product_id, data):
    db.update(product_id, data)
    cache.delete(f"product:{product_id}")
    cache.delete(f"product:{product_id}:*")  # Invalidate all related keys
```

---

### Pattern 4: Gradual Rollout Invalidation

**Use when:** Want to test cache invalidation impact on subset of traffic.

**Implementation:**
```bash
# Invalidate 10% of keys (testing)
redis-cli --scan --pattern "product:*" | head -n 100 | xargs redis-cli DEL

# Monitor impact for 15 minutes

# Invalidate remaining 90%
redis-cli --scan --pattern "product:*" | xargs redis-cli DEL
```

---

## Testing and Validation

**Last Tested:** 2025-11-20 (disaster recovery drill)
**Test Frequency:** Monthly (simulate cache invalidation)
**Next Test:** 2026-01-05

**Test Procedure:**
1. Announce test in #platform-engineering (off-hours)
2. Invalidate non-critical cache namespace (e.g., "test:*")
3. Monitor cache hit rate recovery
4. Verify no impact to production traffic
5. Document any runbook issues discovered
6. Update runbook if needed

---

## Changelog

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-12-05 | 1.3 | Added multi-region invalidation, gradual patterns | @platform-team |
| 2025-10-10 | 1.2 | Added database load check prerequisite | @alice |
| 2025-08-15 | 1.1 | Added API-based invalidation method | @bob |
| 2025-06-01 | 1.0 | Initial version | @platform-team |

---

## Contact

**Owner:** Platform Engineering Team
**Slack:** #platform-engineering
**On-Call:** @platform-oncall
**Escalation:** @platform-lead

**For questions or improvements:** Open PR against `runbooks/cache-invalidation.md`
