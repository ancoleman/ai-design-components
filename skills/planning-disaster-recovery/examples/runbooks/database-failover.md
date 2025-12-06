# Database Failover Runbook

## Overview

This runbook provides step-by-step procedures for executing database failover during primary database failure scenarios. Covers PostgreSQL and MySQL failover patterns with automated promotion, validation, and rollback procedures.

**Target RTO:** 15-30 minutes
**Target RPO:** 5-15 minutes (depending on replication lag)

## When to Use This Runbook

Execute this runbook when:
- Primary database becomes unresponsive or unavailable
- Database performance degradation exceeds acceptable thresholds
- Planned maintenance requiring database switchover
- Data center or availability zone failure affecting primary database
- Corruption detected in primary database requiring failover to replica

**Do NOT use for:**
- Application-layer issues (use application restart procedures)
- Network connectivity issues (resolve network first)
- Disk space issues (expand storage rather than failover)

## Prerequisites

### Required Access
- Database administrative credentials (postgres/root user)
- Cloud console access (AWS/GCP/Azure IAM)
- DNS management access (Route53/Cloud DNS)
- Monitoring system access (Prometheus/Grafana/CloudWatch)

### Required Tools
- Database CLI (`psql`/`mysql`)
- Cloud CLI (`aws`/`gcloud`/`az`)
- `curl` or `wget` for health checks
- SSH access to database servers

### Pre-Failover Validation
Verify these conditions BEFORE initiating failover:
- [ ] Secondary database is healthy and reachable
- [ ] Replication lag is acceptable (< 60 seconds for critical systems)
- [ ] Sufficient storage available on secondary (> 20% free)
- [ ] No ongoing backup operations on secondary
- [ ] Application connection strings configured for failover

## Decision Tree

```
Primary DB unhealthy?
├─ YES → Continue to Assessment
└─ NO → Do not proceed with failover

Is secondary DB healthy?
├─ YES → Continue to Replication Check
└─ NO → STOP - Contact DBA team, evaluate backup restoration

Is replication lag < 60 seconds?
├─ YES → Proceed with failover
└─ NO → Evaluate data loss tolerance
    ├─ Acceptable → Proceed with failover
    └─ Unacceptable → STOP - Attempt primary recovery first

Is this planned maintenance?
├─ YES → Use controlled switchover procedure
└─ NO → Use emergency failover procedure
```

## Procedure 1: PostgreSQL Failover (Streaming Replication)

### Phase 1: Assessment (5 minutes)

**Step 1.1: Verify Primary Failure**
```bash
# Check primary database connectivity
psql -h primary-db.example.com -U postgres -c "SELECT version();" 2>&1

# Expected: Connection timeout or error
# If successful, primary is operational - STOP
```

**Step 1.2: Check Secondary Health**
```bash
# Connect to secondary database
psql -h secondary-db.example.com -U postgres -c "SELECT version();"

# Check replication status
psql -h secondary-db.example.com -U postgres -c "
SELECT
  pg_last_wal_receive_lsn() AS receive,
  pg_last_wal_replay_lsn() AS replay,
  EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp())) AS lag_seconds;
"

# Record lag_seconds value - if > 60, evaluate data loss tolerance
```

**Step 1.3: Document Current State**
```bash
# Record for incident report
echo "Failover initiated: $(date -Iseconds)" >> /var/log/dr-failover.log
echo "Primary: primary-db.example.com - FAILED" >> /var/log/dr-failover.log
echo "Secondary lag: [RECORDED_LAG] seconds" >> /var/log/dr-failover.log
```

### Phase 2: Promotion (10 minutes)

**Step 2.1: Stop Application Writes**
```bash
# Update load balancer to reject database writes
# AWS ALB example:
aws elbv2 modify-target-group \
  --target-group-arn arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/db-writers/abc \
  --health-check-enabled=false

# Verify no active connections to primary
psql -h secondary-db.example.com -U postgres -c "
SELECT count(*) FROM pg_stat_activity
WHERE backend_type = 'client backend' AND state = 'active';
"

# Wait 30 seconds for in-flight transactions
sleep 30
```

**Step 2.2: Promote Secondary to Primary**
```bash
# PostgreSQL 12+ promotion
pg_ctl promote -D /var/lib/postgresql/14/main

# Alternative: Using trigger file method
touch /var/lib/postgresql/14/main/promote

# Verify promotion completed
psql -h secondary-db.example.com -U postgres -c "
SELECT pg_is_in_recovery();
"

# Expected output: f (false = not in recovery = primary)
```

**Step 2.3: Verify Write Capability**
```bash
# Test write operation on promoted database
psql -h secondary-db.example.com -U postgres -c "
CREATE TABLE IF NOT EXISTS dr_failover_test (
  failover_time TIMESTAMP DEFAULT now()
);
INSERT INTO dr_failover_test VALUES (DEFAULT);
SELECT * FROM dr_failover_test ORDER BY failover_time DESC LIMIT 1;
"

# Expected: Successful insert with current timestamp
```

### Phase 3: DNS Update (5 minutes)

**Step 3.1: Update DNS Records**
```bash
# AWS Route53 example - update CNAME to point to secondary
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "primary-db.example.com",
        "Type": "CNAME",
        "TTL": 60,
        "ResourceRecords": [{"Value": "secondary-db.example.com"}]
      }
    }]
  }'

# Record change ID
CHANGE_ID=$(aws route53 list-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --query "ResourceRecordSets[?Name=='primary-db.example.com'].ResourceRecords[0].Value" \
  --output text)
echo "DNS updated to: $CHANGE_ID" >> /var/log/dr-failover.log
```

**Step 3.2: Wait for DNS Propagation**
```bash
# Check DNS propagation (typically 60-120 seconds)
for i in {1..12}; do
  RESOLVED=$(dig +short primary-db.example.com)
  echo "Attempt $i: $RESOLVED"
  if [[ "$RESOLVED" == *"secondary-db"* ]]; then
    echo "DNS propagated successfully"
    break
  fi
  sleep 10
done
```

### Phase 4: Application Reconnection (5 minutes)

**Step 4.1: Enable Application Connections**
```bash
# Re-enable load balancer health checks
aws elbv2 modify-target-group \
  --target-group-arn arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/db-writers/abc \
  --health-check-enabled=true

# Wait for health checks to pass (30 seconds)
sleep 30
```

**Step 4.2: Verify Application Connectivity**
```bash
# Test application health endpoint
curl -f https://api.example.com/health

# Check application logs for database connection errors
kubectl logs -n production deployment/api --tail=50 | grep -i "database"

# Expected: No connection errors, successful health check
```

### Phase 5: Validation (5 minutes)

**Step 5.1: Test Critical User Journeys**
```bash
# Test read operation
curl -X GET https://api.example.com/users/1

# Test write operation
curl -X POST https://api.example.com/test-write \
  -H "Content-Type: application/json" \
  -d '{"test":"failover"}'

# Expected: Both operations successful
```

**Step 5.2: Verify Data Integrity**
```bash
# Check row counts match expected values
psql -h primary-db.example.com -U postgres -d production -c "
SELECT
  'users' AS table_name, COUNT(*) AS row_count FROM users
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'transactions', COUNT(*) FROM transactions;
"

# Compare against pre-failover counts (if available)
# Acceptable variance: < 1% for most tables
```

**Step 5.3: Monitor Metrics**
```bash
# Check database connection pool
psql -h primary-db.example.com -U postgres -c "
SELECT count(*), state FROM pg_stat_activity
WHERE backend_type = 'client backend'
GROUP BY state;
"

# Check query performance
psql -h primary-db.example.com -U postgres -c "
SELECT query, calls, mean_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
"

# Expected: Normal connection counts, acceptable query times
```

## Procedure 2: MySQL Failover (InnoDB Cluster)

### Phase 1: Assessment (5 minutes)

**Step 1.1: Check Cluster Status**
```bash
# Connect to MySQL Router or any cluster member
mysql -h mysql-router.example.com -u admin -p -e "
SELECT * FROM performance_schema.replication_group_members;
"

# Identify PRIMARY and SECONDARY members
# Expected: One PRIMARY (ONLINE), multiple SECONDARYs (ONLINE)
```

**Step 1.2: Verify Primary Failure**
```bash
# Check primary member status
mysql -h primary-mysql.example.com -u admin -p -e "SELECT 1;"

# If connection fails, primary is down
# Check Group Replication status
mysql -h secondary-mysql.example.com -u admin -p -e "
SHOW STATUS LIKE 'group_replication%';
"
```

### Phase 2: Automatic Failover (5-10 minutes)

**Step 2.1: Verify Automatic Promotion**
```bash
# InnoDB Cluster typically auto-promotes secondary
# Verify new primary election
mysql -h mysql-router.example.com -u admin -p -e "
SELECT member_host, member_role, member_state
FROM performance_schema.replication_group_members;
"

# Expected: New PRIMARY elected, old primary OFFLINE or UNREACHABLE
```

**Step 2.2: Verify Quorum**
```bash
# Ensure cluster has majority quorum
mysql -h mysql-router.example.com -u admin -p -e "
SELECT COUNT(*) AS online_members
FROM performance_schema.replication_group_members
WHERE member_state = 'ONLINE';
"

# Expected: At least (N/2 + 1) members online for 3+ member cluster
# Example: 3 members = need 2 online, 5 members = need 3 online
```

### Phase 3: Application Validation (5 minutes)

**Step 3.1: Test MySQL Router Connections**
```bash
# MySQL Router automatically redirects to new primary
mysql -h mysql-router.example.com -u app_user -p -e "
SELECT @@hostname, @@read_only;
"

# Expected: read_only = 0 (writes enabled on new primary)
```

**Step 3.2: Verify Application Writes**
```bash
# Test write operation
mysql -h mysql-router.example.com -u app_user -p -e "
INSERT INTO dr_test (failover_time) VALUES (NOW());
SELECT * FROM dr_test ORDER BY failover_time DESC LIMIT 1;
"

# Expected: Successful insert
```

## Rollback Procedure

**Use rollback when:**
- Promoted secondary exhibits critical issues
- Data corruption detected on secondary
- Application failures persist after failover

### Rollback Steps

**Step 1: Assess Original Primary Recovery**
```bash
# Check if original primary can be recovered
psql -h original-primary.example.com -U postgres -c "SELECT version();"

# If accessible, check data integrity
psql -h original-primary.example.com -U postgres -c "
SELECT pg_last_wal_receive_lsn();
"
```

**Step 2: Resynchronize Databases**
```bash
# If original primary is behind, resync from promoted secondary
# Use pg_rewind for PostgreSQL
pg_rewind \
  --target-pgdata=/var/lib/postgresql/14/main \
  --source-server="host=promoted-secondary.example.com user=postgres"

# Restart original primary as replica
systemctl start postgresql
```

**Step 3: Promote Original Primary**
```bash
# Reverse failover procedure
pg_ctl promote -D /var/lib/postgresql/14/main

# Update DNS back to original primary
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch '[ORIGINAL_DNS_CONFIG]'
```

## Post-Failover Tasks

**Within 1 Hour:**
- [ ] Update incident documentation with timeline
- [ ] Notify stakeholders of resolution
- [ ] Verify all monitoring alerts cleared
- [ ] Check application error rates returned to baseline

**Within 24 Hours:**
- [ ] Conduct incident retrospective
- [ ] Analyze root cause of primary failure
- [ ] Restore original replication topology (if desired)
- [ ] Rebuild or repair failed primary database
- [ ] Update runbook with lessons learned

**Within 1 Week:**
- [ ] Review and update RTO/RPO metrics
- [ ] Test failback procedure in staging environment
- [ ] Validate backup integrity post-failover
- [ ] Schedule follow-up DR drill

## Troubleshooting

### Issue: Secondary replication lag too high

**Symptoms:** Replication lag > 5 minutes, data loss unacceptable

**Resolution:**
```bash
# Check replication bandwidth
psql -h secondary-db.example.com -U postgres -c "
SELECT pg_size_pretty(pg_wal_lsn_diff(pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn())) AS lag_bytes;
"

# Identify slow queries blocking replay
psql -h secondary-db.example.com -U postgres -c "
SELECT pid, query, state, wait_event
FROM pg_stat_activity
WHERE backend_type = 'walreceiver';
"

# Options:
# 1. Wait for replication to catch up (if time permits)
# 2. Accept data loss and proceed with failover
# 3. Attempt primary recovery instead of failover
```

### Issue: Promotion fails

**Symptoms:** `pg_ctl promote` returns error, database remains in recovery mode

**Resolution:**
```bash
# Check PostgreSQL logs
tail -n 100 /var/log/postgresql/postgresql-14-main.log

# Common causes:
# - WAL files missing: Restore from backup
# - Disk full: Expand storage
# - Permission issues: Check file ownership

# Manual promotion via trigger file
echo "promote" > /var/lib/postgresql/14/main/promote.signal
systemctl restart postgresql
```

### Issue: Application cannot connect after failover

**Symptoms:** Connection timeouts, authentication failures

**Resolution:**
```bash
# Verify DNS resolution
dig primary-db.example.com

# Check firewall rules
nc -zv secondary-db.example.com 5432

# Verify pg_hba.conf allows connections
psql -h secondary-db.example.com -U postgres -c "
SHOW hba_file;
"
cat /etc/postgresql/14/main/pg_hba.conf | grep -v '^#'

# Reload configuration if needed
psql -h secondary-db.example.com -U postgres -c "SELECT pg_reload_conf();"
```

## RTO/RPO Tracking

**Actual RTO Calculation:**
```
RTO = Time(Service Restored) - Time(Failure Detected)

Example:
- Failure Detected: 10:00:00
- Service Restored: 10:23:45
- Actual RTO: 23 minutes 45 seconds
```

**Actual RPO Calculation:**
```
RPO = Replication Lag at Failover Time

Example:
- Last transaction on primary: 09:59:45
- Last replayed transaction on secondary: 09:59:30
- Actual RPO: 15 seconds
```

**Record in Incident Report:**
```bash
echo "=== Failover Metrics ===" >> /var/log/dr-failover.log
echo "Failure Detection Time: [TIMESTAMP]" >> /var/log/dr-failover.log
echo "Promotion Complete Time: [TIMESTAMP]" >> /var/log/dr-failover.log
echo "DNS Update Complete: [TIMESTAMP]" >> /var/log/dr-failover.log
echo "Service Restored Time: [TIMESTAMP]" >> /var/log/dr-failover.log
echo "Actual RTO: [MINUTES]" >> /var/log/dr-failover.log
echo "Actual RPO: [SECONDS]" >> /var/log/dr-failover.log
```

## Automation Script

For automated failover execution, use:
```bash
/Users/antoncoleman/Documents/repos/ai-design-components/skills/planning-disaster-recovery/scripts/automated-db-failover.sh \
  --primary primary-db.example.com \
  --secondary secondary-db.example.com \
  --verify-replication \
  --update-dns
```

See `scripts/automated-db-failover.sh` for implementation details.

## Related Runbooks

- **Region Failover:** `examples/runbooks/region-failover.md`
- **Kubernetes Recovery:** `references/kubernetes-dr.md`
- **Backup Restoration:** `references/database-backups.md`

## References

- PostgreSQL High Availability Documentation: https://www.postgresql.org/docs/current/high-availability.html
- MySQL InnoDB Cluster: https://dev.mysql.com/doc/refman/8.0/en/mysql-innodb-cluster.html
- RTO/RPO Planning: `references/rto-rpo-planning.md`
