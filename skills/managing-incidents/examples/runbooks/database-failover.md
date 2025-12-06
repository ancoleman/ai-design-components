# Runbook: Database Failover

## Metadata

- **Runbook ID:** RB-DB-001
- **Owner:** Database SRE Team (@db-sre-team)
- **Last Updated:** 2025-12-03
- **Version:** 2.1
- **Estimated Duration:** 10-15 minutes

---

## Trigger Conditions

Execute this runbook when:
- Primary database becomes unreachable (alert: "PostgreSQL Primary Down")
- Primary database performance severely degraded (> 10 seconds query latency)
- Planned maintenance requiring failover
- Database corruption detected on primary

**Alert Names:**
- `PostgreSQL-Primary-Down`
- `Database-Failover-Required`
- `Primary-DB-Health-Critical`

---

## Severity Classification

**Expected Severity:** SEV1 (Major Degradation)

**Reasoning:** Application remains functional with degraded performance until failover completes. Becomes SEV0 if secondary unavailable or replication lag > 1 minute.

---

## Prerequisites

Before executing, verify:

1. **Secondary Database Health:**
   ```bash
   pg_isready -h secondary-db.example.com -p 5432
   ```
   Expected: `secondary-db.example.com:5432 - accepting connections`

2. **Replication Lag:**
   ```sql
   -- Run on secondary
   SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp())) AS lag_seconds;
   ```
   Expected: < 5 seconds

   **If lag > 5 seconds:** Wait for replication to catch up or accept potential data loss (consult IC).

3. **Disk Space on Secondary:**
   ```bash
   df -h /var/lib/postgresql
   ```
   Expected: > 20% free space

4. **Required Access:**
   - SSH access to database servers
   - Sudo privileges for PostgreSQL commands
   - AWS/GCP console access for DNS updates
   - Slack channel: #database-operations

---

## Steps

### Step 1: Verify Primary is Truly Down

**Purpose:** Prevent unnecessary failover due to transient network issues.

```bash
# From monitoring server
ping -c 5 primary-db.example.com

# Check PostgreSQL connectivity
pg_isready -h primary-db.example.com -p 5432

# Check last heartbeat in monitoring
curl https://monitoring.example.com/api/v1/query?query=up{job="postgresql-primary"}
```

**Expected Result:** Ping fails OR PostgreSQL not accepting connections

**If Primary Responds:** Do NOT proceed with failover. Investigate performance issue instead (see RB-DB-002).

---

### Step 2: Announce Failover in Incident Channel

**Purpose:** Notify team and stakeholders of impending failover.

```
Post in #incident-YYYY-MM-DD-database:

"@here Starting database failover from primary-db to secondary-db.
Expected downtime: 2-5 minutes.
ETA for completion: 15:30 PST (in 10 minutes)."
```

---

### Step 3: Check Replication Status on Secondary

**Purpose:** Ensure secondary is up-to-date before promotion.

```bash
# SSH to secondary database
ssh admin@secondary-db.example.com

# Check replication status
sudo -u postgres psql -c "SELECT * FROM pg_stat_wal_receiver;"
```

**Expected Output:**
```
status    | streaming
received  | <recent timestamp>
```

**If NOT streaming:** Do NOT promote. Investigate replication failure first.

---

### Step 4: Promote Secondary to Primary

**Purpose:** Make secondary the new writable database.

```bash
# On secondary database server
sudo -u postgres pg_ctl promote -D /var/lib/postgresql/data

# Verify promotion
sudo -u postgres psql -c "SELECT pg_is_in_recovery();"
```

**Expected Result:** `f` (false = not in recovery = primary mode)

**If Promotion Fails:**
- Check PostgreSQL logs: `tail -f /var/log/postgresql/postgresql.log`
- Verify no standby.signal file blocking promotion
- Escalate to senior DBA if unclear

---

### Step 5: Update DNS to Point to New Primary

**Purpose:** Route application traffic to new primary database.

**Option A: Route53 (AWS)**

```bash
# Update DNS record via AWS CLI
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "primary-db.example.com",
        "Type": "A",
        "TTL": 60,
        "ResourceRecords": [{"Value": "10.0.2.20"}]
      }
    }]
  }'
```

**Option B: Terraform**

```bash
# Update terraform variable
cd infrastructure/terraform/database
echo 'primary_db_ip = "10.0.2.20"' >> terraform.tfvars

# Apply change
terraform plan -target=aws_route53_record.db_primary
terraform apply -target=aws_route53_record.db_primary
```

**Verification:**
```bash
# Verify DNS propagation
dig primary-db.example.com +short
# Expected: 10.0.2.20 (new primary IP)

# Wait for DNS TTL (60 seconds)
sleep 60
```

---

### Step 6: Update Application Configuration

**Purpose:** Ensure application connects to correct database endpoint.

**Option A: No Action Required (if using DNS)**

If application uses `primary-db.example.com` hostname, DNS update is sufficient.

**Option B: Update Environment Variables**

```bash
# Update Kubernetes configmap
kubectl edit configmap app-config -n production

# Update DATABASE_HOST value
# DATABASE_HOST: secondary-db.example.com → primary-db.example.com

# Restart application pods to pick up new config
kubectl rollout restart deployment/api -n production
```

---

### Step 7: Verify Application Connectivity

**Purpose:** Confirm application successfully connecting to new primary.

```bash
# Check application error rates in monitoring
curl https://monitoring.example.com/api/v1/query?query=rate(api_errors_total[5m])

# Check database connection pool
curl https://monitoring.example.com/api/v1/query?query=database_connections_active

# Test write operation
curl -X POST https://api.example.com/health/write-test
```

**Expected Result:**
- Error rate returns to baseline (< 0.1%)
- Database connections active (> 0)
- Write test succeeds: `{"status": "ok", "write_success": true}`

**If Errors Persist:**
- Check application logs for connection errors
- Verify DNS propagation: `nslookup primary-db.example.com`
- Verify firewall rules allow app → new primary
- Escalate to application team if needed

---

### Step 8: Monitor for Stability

**Purpose:** Ensure failover was successful and system is stable.

```bash
# Monitor for 10 minutes
# - Database CPU, memory, disk I/O
# - Application error rates
# - Query latency
```

**Monitoring Dashboard:** https://monitoring.example.com/dashboard/database-health

**Stability Criteria:**
- Query latency < 100ms (p99)
- Database CPU < 70%
- Application error rate < 0.1%
- No new database alerts

**If Unstable:** See "Rollback" section below.

---

### Step 9: Document Failover in Incident Timeline

**Purpose:** Record actions for post-mortem.

```
Post in #incident-YYYY-MM-DD-database:

"Failover complete. New primary: secondary-db (10.0.2.20).
- Promotion: 15:20 PST
- DNS Update: 15:22 PST
- App connectivity verified: 15:25 PST
- Monitoring for stability."
```

---

### Step 10: Update Runbook (If Steps Changed)

**Purpose:** Keep runbook accurate for future use.

```bash
# If any steps failed or needed modification
# Update this runbook in Git

git checkout -b update-db-failover-runbook
# Edit runbook
git add runbooks/database-failover.md
git commit -m "Update database failover runbook based on 2025-12-03 incident"
git push origin update-db-failover-runbook
# Create PR for review
```

---

## Rollback Procedure

**When to Rollback:**
- New primary experiencing high error rates (> 5%)
- New primary performance worse than before failover
- Data inconsistency detected

**Rollback Steps:**

1. **Announce Rollback:**
   ```
   Post in incident channel:
   "@here Rollback initiated. Reverting to original primary."
   ```

2. **Revert DNS Change:**
   ```bash
   # Point DNS back to original primary IP
   aws route53 change-resource-record-sets \
     --hosted-zone-id Z1234567890ABC \
     --change-batch '{...}' # Original IP
   ```

3. **Demote Current Primary Back to Secondary:**
   ```bash
   # On current primary (being demoted)
   sudo -u postgres pg_ctl stop -D /var/lib/postgresql/data
   # Reconfigure as replica (create standby.signal)
   touch /var/lib/postgresql/data/standby.signal
   sudo -u postgres pg_ctl start -D /var/lib/postgresql/data
   ```

4. **Verify Rollback:**
   - Check application error rates
   - Verify database connectivity
   - Monitor for 10 minutes

5. **Post-Incident Action:**
   - Schedule post-mortem to understand why rollback was needed
   - Investigate secondary database issues before retry

---

## Escalation Criteria

Escalate to Senior DBA (@senior-dba-oncall) if:
- Replication lag > 1 minute (data loss risk)
- Secondary database not healthy
- Promotion fails with unclear error
- Application connectivity issues after failover
- Rollback required

Escalate to VP Engineering if:
- Estimated downtime > 30 minutes
- Data loss occurred
- Customer-facing impact severe (SEV0)

---

## Common Issues and Solutions

### Issue 1: Replication Lag High

**Symptom:** Replication lag > 5 seconds

**Solutions:**
- **Wait:** Allow replication to catch up (if lag increasing, investigate network)
- **Accept Data Loss:** Consult IC, promote anyway if critical
- **Investigate:** Check network latency, disk I/O on secondary

---

### Issue 2: Secondary Not Responding

**Symptom:** `pg_isready` fails on secondary

**Solutions:**
- **Check PostgreSQL Status:** `systemctl status postgresql`
- **Restart PostgreSQL:** `sudo systemctl restart postgresql`
- **Check Disk Space:** `df -h /var/lib/postgresql`
- **Escalate:** If restart fails, escalate to senior DBA

---

### Issue 3: DNS Not Propagating

**Symptom:** Application still connecting to old primary after DNS update

**Solutions:**
- **Verify DNS Change:** `dig primary-db.example.com +short`
- **Wait for TTL:** 60 seconds for DNS cache expiration
- **Flush Application DNS Cache:** Restart application pods
- **Temporary Fix:** Update application config directly with new IP

---

### Issue 4: Application Connection Errors

**Symptom:** API returning database connection errors after failover

**Solutions:**
- **Check Connection String:** Verify hostname/IP correct
- **Check Firewall Rules:** `telnet primary-db.example.com 5432`
- **Verify PostgreSQL Accepting Connections:** `sudo -u postgres psql -c "SHOW listen_addresses;"`
- **Restart Application:** `kubectl rollout restart deployment/api`

---

## Post-Execution Checklist

After completing failover, verify:

- [ ] Secondary promoted to primary successfully
- [ ] DNS updated to point to new primary
- [ ] Application connectivity verified
- [ ] Error rates returned to baseline
- [ ] Monitoring stable for 10+ minutes
- [ ] Incident timeline documented
- [ ] Old primary (now secondary) replication configured
- [ ] Runbook updated if steps changed
- [ ] Post-mortem scheduled (within 48 hours)

---

## Related Runbooks

- **RB-DB-002:** Database Performance Troubleshooting
- **RB-DB-003:** Database Replication Repair
- **RB-DB-004:** Database Backup and Restore

---

## Testing and Validation

**Last Tested:** 2025-11-15 (disaster recovery drill)
**Test Frequency:** Quarterly (every 3 months)
**Next Test:** 2026-02-15

**Test Procedure:**
1. Announce planned test in #database-operations
2. Execute failover during low-traffic window (2am PST)
3. Verify application functionality
4. Fail back to original primary
5. Document any runbook issues discovered

---

## Changelog

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-12-03 | 2.1 | Added DNS verification step, updated IPs | @alice |
| 2025-10-15 | 2.0 | Added Terraform option for DNS update | @bob |
| 2025-08-01 | 1.5 | Added replication lag check | @charlie |
| 2025-06-01 | 1.0 | Initial version | @db-team |

---

## Contact

**Owner:** Database SRE Team
**Slack:** #database-operations
**On-Call:** @db-sre-oncall
**Escalation:** @senior-dba-oncall

**For questions or improvements:** Open PR against `runbooks/database-failover.md`
