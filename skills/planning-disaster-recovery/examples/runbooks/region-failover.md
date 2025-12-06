# Multi-Region Failover Runbook

## Overview

This runbook provides comprehensive procedures for executing multi-region failover during primary region failure scenarios. Covers complete infrastructure failover including databases, application servers, load balancers, and DNS management across AWS, GCP, and Azure.

**Target RTO:** 30-60 minutes (depends on architecture pattern)
**Target RPO:** 5-30 minutes (depends on replication configuration)

## When to Use This Runbook

Execute this runbook when:
- Entire primary region becomes unavailable (AWS outage, natural disaster)
- Network connectivity lost to primary region
- Multiple critical services failing simultaneously in primary region
- Primary region experiencing severe degradation affecting SLA
- Planned region migration or maintenance requiring full failover

**Do NOT use for:**
- Single service failures (use service-specific runbooks)
- Transient network issues (wait for recovery)
- Performance degradation without outage (use scaling procedures)
- Database-only issues (use database failover runbook)

## Architecture Patterns

This runbook covers three common multi-region patterns:

### Pattern 1: Active-Passive (Warm Standby)
- Primary region handles all traffic
- Secondary region has scaled-down infrastructure
- Database continuously replicated to secondary
- **RTO:** 30-60 minutes (requires scaling up secondary)
- **RPO:** 5-30 minutes (replication lag)

### Pattern 2: Active-Active (Multi-Master)
- Both regions handle production traffic
- Traffic split via global load balancer
- Database supports multi-region writes
- **RTO:** < 5 minutes (automatic failover)
- **RPO:** < 1 minute (synchronous replication)

### Pattern 3: Pilot Light
- Secondary region has minimal infrastructure (database only)
- Application servers provisioned during failover
- Most cost-effective, longest RTO
- **RTO:** 60-120 minutes (requires full provisioning)
- **RPO:** 5-30 minutes (replication lag)

## Prerequisites

### Required Access
- Cloud console admin access (AWS/GCP/Azure)
- DNS management (Route53/Cloud DNS/Azure DNS)
- Global load balancer access (CloudFront/Cloud CDN/Traffic Manager)
- Infrastructure-as-code repository access (Terraform/CloudFormation)
- Monitoring system access (Prometheus/DataDog/CloudWatch)

### Required Tools
- Cloud CLI: `aws`, `gcloud`, or `az`
- Terraform or CloudFormation CLI
- `kubectl` for Kubernetes management
- `dig` or `nslookup` for DNS verification
- `curl` or `wget` for health checks

### Pre-Failover Validation
Verify these conditions BEFORE initiating region failover:
- [ ] Secondary region infrastructure is operational
- [ ] Database replication lag is acceptable (< 5 minutes)
- [ ] DNS TTLs are lowered (recommended: 60 seconds)
- [ ] Monitoring dashboards accessible
- [ ] Incident communication channels active
- [ ] Stakeholders notified of impending failover

## Decision Tree

```
Primary region completely unavailable?
├─ YES → Continue to Secondary Health Check
└─ NO → Evaluate service-specific failover
    ├─ Database only → Use database-failover.md
    ├─ Application only → Use application restart procedures
    └─ Multiple services → Continue with region failover

Is secondary region healthy?
├─ YES → Continue to Replication Check
└─ NO → ESCALATE - Declare major incident, engage vendor support

Is database replication current (lag < 5 min)?
├─ YES → Proceed with failover
└─ NO → Evaluate data loss tolerance
    ├─ RPO acceptable → Proceed with failover
    ├─ RPO unacceptable → Attempt primary region recovery
    └─ Unknown → STOP - Investigate replication status

Is this planned maintenance?
├─ YES → Use controlled switchover (additional testing steps)
└─ NO → Use emergency failover (prioritize speed)

What architecture pattern?
├─ Active-Active → Execute Pattern A procedure
├─ Active-Passive → Execute Pattern B procedure
└─ Pilot Light → Execute Pattern C procedure
```

## Procedure A: Active-Passive Failover (Warm Standby)

### Phase 1: Assessment and Preparation (10 minutes)

**Step 1.1: Verify Primary Region Failure**
```bash
# Test primary region endpoints
PRIMARY_REGION="us-east-1"
SECONDARY_REGION="us-west-2"

# Check multiple services in primary region
for service in api.example.com db.example.com admin.example.com; do
  echo "Testing $service..."
  curl -f -m 10 "https://$service/health" 2>&1 || echo "FAILED: $service"
done

# Check AWS service health
aws health describe-events \
  --filter eventTypeCategories=issue \
  --region $PRIMARY_REGION

# Expected: Multiple service failures, possible AWS service events
```

**Step 1.2: Assess Secondary Region Health**
```bash
# Verify secondary region infrastructure
aws ec2 describe-instances \
  --region $SECONDARY_REGION \
  --filters "Name=tag:Environment,Values=production" "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[?State.Name==`running`].InstanceId' \
  --output table

# Check database replication status
aws rds describe-db-instances \
  --region $SECONDARY_REGION \
  --db-instance-identifier prod-db-secondary \
  --query 'DBInstances[0].[DBInstanceStatus,StatusInfos]'

# Expected: Instances running, database available
```

**Step 1.3: Check Database Replication Lag**
```bash
# For PostgreSQL
psql -h secondary-db.$SECONDARY_REGION.example.com -U postgres -c "
SELECT
  CASE WHEN pg_is_in_recovery() THEN 'REPLICA' ELSE 'PRIMARY' END AS role,
  pg_last_wal_receive_lsn() AS received,
  pg_last_wal_replay_lsn() AS replayed,
  EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp())) AS lag_seconds;
"

# Record lag_seconds - if > 300 (5 min), evaluate RPO tolerance
LAG_SECONDS=<RECORDED_VALUE>
echo "Replication lag: $LAG_SECONDS seconds" >> /var/log/region-failover.log
```

**Step 1.4: Document Failover Initiation**
```bash
# Create incident log
FAILOVER_LOG="/var/log/region-failover-$(date +%Y%m%d-%H%M%S).log"
cat <<EOF > $FAILOVER_LOG
=== REGION FAILOVER INITIATED ===
Timestamp: $(date -Iseconds)
Operator: $(whoami)
Primary Region: $PRIMARY_REGION (FAILED)
Secondary Region: $SECONDARY_REGION (ACTIVE)
Replication Lag: $LAG_SECONDS seconds
Architecture: Active-Passive (Warm Standby)
EOF
```

### Phase 2: Database Failover (15 minutes)

**Step 2.1: Stop Application Traffic to Database**
```bash
# Scale down application servers in primary region (if accessible)
aws autoscaling set-desired-capacity \
  --auto-scaling-group-name prod-app-asg-$PRIMARY_REGION \
  --desired-capacity 0 \
  --region $PRIMARY_REGION 2>/dev/null || echo "Primary region unreachable"

# Wait for in-flight transactions to complete
sleep 30
```

**Step 2.2: Promote Secondary Database**
```bash
# AWS RDS - Promote read replica
aws rds promote-read-replica \
  --db-instance-identifier prod-db-secondary \
  --backup-retention-period 7 \
  --region $SECONDARY_REGION

# Wait for promotion (typically 5-10 minutes)
echo "Waiting for database promotion..."
while true; do
  STATUS=$(aws rds describe-db-instances \
    --region $SECONDARY_REGION \
    --db-instance-identifier prod-db-secondary \
    --query 'DBInstances[0].DBInstanceStatus' \
    --output text)

  echo "Database status: $STATUS"

  if [[ "$STATUS" == "available" ]]; then
    echo "$(date -Iseconds): Database promoted successfully" >> $FAILOVER_LOG
    break
  elif [[ "$STATUS" == "failed" ]]; then
    echo "ERROR: Database promotion failed" >> $FAILOVER_LOG
    exit 1
  fi

  sleep 15
done
```

**Step 2.3: Verify Database Write Capability**
```bash
# Test write operations on promoted database
psql -h prod-db-secondary.$SECONDARY_REGION.example.com -U postgres -c "
-- Verify read-only mode disabled
SHOW transaction_read_only;

-- Test write operation
CREATE TABLE IF NOT EXISTS dr_region_failover_test (
  id SERIAL PRIMARY KEY,
  failover_time TIMESTAMP DEFAULT now(),
  source_region VARCHAR(50)
);

INSERT INTO dr_region_failover_test (source_region)
VALUES ('$SECONDARY_REGION');

SELECT * FROM dr_region_failover_test ORDER BY id DESC LIMIT 1;
"

# Expected: transaction_read_only = off, successful insert
```

### Phase 3: Scale Up Secondary Infrastructure (15 minutes)

**Step 3.1: Scale Application Servers**
```bash
# Increase auto-scaling group capacity to production levels
# Warm standby typically runs at 50% capacity, scale to 100%

# Get current capacity
CURRENT_CAPACITY=$(aws autoscaling describe-auto-scaling-groups \
  --auto-scaling-group-names prod-app-asg-$SECONDARY_REGION \
  --region $SECONDARY_REGION \
  --query 'AutoScalingGroups[0].DesiredCapacity' \
  --output text)

TARGET_CAPACITY=$((CURRENT_CAPACITY * 2))

echo "Scaling from $CURRENT_CAPACITY to $TARGET_CAPACITY instances" >> $FAILOVER_LOG

# Scale up
aws autoscaling set-desired-capacity \
  --auto-scaling-group-name prod-app-asg-$SECONDARY_REGION \
  --desired-capacity $TARGET_CAPACITY \
  --region $SECONDARY_REGION

# Wait for instances to become healthy (5-10 minutes)
echo "Waiting for instances to become healthy..."
for i in {1..30}; do
  HEALTHY=$(aws autoscaling describe-auto-scaling-groups \
    --auto-scaling-group-names prod-app-asg-$SECONDARY_REGION \
    --region $SECONDARY_REGION \
    --query 'AutoScalingGroups[0].Instances[?HealthStatus==`Healthy`] | length(@)' \
    --output text)

  echo "Attempt $i: $HEALTHY healthy instances (target: $TARGET_CAPACITY)"

  if [[ $HEALTHY -ge $TARGET_CAPACITY ]]; then
    echo "$(date -Iseconds): All instances healthy" >> $FAILOVER_LOG
    break
  fi

  sleep 20
done
```

**Step 3.2: Verify Application Health**
```bash
# Test application endpoints in secondary region
SECONDARY_LB="app-lb.$SECONDARY_REGION.example.com"

for endpoint in /health /api/v1/status /api/v1/users/healthcheck; do
  echo "Testing $endpoint..."
  RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "https://$SECONDARY_LB$endpoint")

  if [[ $RESPONSE == "200" ]]; then
    echo "✓ $endpoint: OK"
  else
    echo "✗ $endpoint: FAILED (HTTP $RESPONSE)"
  fi
done
```

**Step 3.3: Update Application Configuration**
```bash
# Update environment variables to point to new database
# Using Kubernetes ConfigMap example
kubectl set env deployment/api \
  --namespace production \
  DATABASE_HOST=prod-db-secondary.$SECONDARY_REGION.example.com \
  ACTIVE_REGION=$SECONDARY_REGION \
  --record

# Restart pods to pick up new configuration
kubectl rollout restart deployment/api -n production

# Wait for rollout to complete
kubectl rollout status deployment/api -n production --timeout=300s
```

### Phase 4: DNS and Traffic Cutover (10 minutes)

**Step 4.1: Lower DNS TTL (if not already done)**
```bash
# Check current TTL
dig api.example.com +noall +answer

# If TTL > 60, update to 60 seconds and wait for propagation
# (This step should be done proactively before disasters)
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "api.example.com",
        "Type": "A",
        "TTL": 60,
        "ResourceRecords": [{"Value": "PRIMARY_IP"}]
      }
    }]
  }'
```

**Step 4.2: Update DNS Records to Secondary Region**
```bash
# Get secondary load balancer IP/DNS
SECONDARY_LB_DNS=$(aws elbv2 describe-load-balancers \
  --region $SECONDARY_REGION \
  --names prod-app-lb \
  --query 'LoadBalancers[0].DNSName' \
  --output text)

echo "Secondary LB: $SECONDARY_LB_DNS" >> $FAILOVER_LOG

# Update Route53 to point to secondary region
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch "{
    \"Changes\": [{
      \"Action\": \"UPSERT\",
      \"ResourceRecordSet\": {
        \"Name\": \"api.example.com\",
        \"Type\": \"CNAME\",
        \"TTL\": 60,
        \"ResourceRecords\": [{\"Value\": \"$SECONDARY_LB_DNS\"}]
      }
    }]
  }"

# Record DNS change
echo "$(date -Iseconds): DNS updated to secondary region" >> $FAILOVER_LOG
```

**Step 4.3: Verify DNS Propagation**
```bash
# Check DNS resolution from multiple locations
for resolver in 8.8.8.8 1.1.1.1 208.67.222.222; do
  echo "Checking resolver: $resolver"
  dig @$resolver api.example.com +short
done

# Test from public DNS
for i in {1..12}; do
  RESOLVED=$(dig +short api.example.com)
  echo "Attempt $i: $RESOLVED"

  if [[ "$RESOLVED" == *"$SECONDARY_REGION"* ]] || [[ "$RESOLVED" == "$SECONDARY_LB_DNS" ]]; then
    echo "✓ DNS propagated successfully"
    break
  fi

  sleep 10
done
```

### Phase 5: Validation and Monitoring (10 minutes)

**Step 5.1: Test Critical User Journeys**
```bash
# Test authentication
curl -X POST https://api.example.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}' \
  -w "\nHTTP Status: %{http_code}\n"

# Test read operation
curl -X GET https://api.example.com/api/v1/users/1 \
  -H "Authorization: Bearer $TOKEN" \
  -w "\nHTTP Status: %{http_code}\n"

# Test write operation
curl -X POST https://api.example.com/api/v1/test \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"test":"region-failover"}' \
  -w "\nHTTP Status: %{http_code}\n"

# Expected: All operations return 200 OK
```

**Step 5.2: Verify Metrics and Monitoring**
```bash
# Check application error rates
curl -s "http://prometheus.example.com/api/v1/query?query=rate(http_requests_total{status=~'5..'}[5m])"

# Check database connection pool
psql -h prod-db-secondary.$SECONDARY_REGION.example.com -U postgres -c "
SELECT
  count(*) AS total_connections,
  state,
  wait_event_type
FROM pg_stat_activity
WHERE backend_type = 'client backend'
GROUP BY state, wait_event_type
ORDER BY total_connections DESC;
"

# Check application response times
curl -s "http://prometheus.example.com/api/v1/query?query=histogram_quantile(0.95,rate(http_request_duration_seconds_bucket[5m]))"
```

**Step 5.3: Verify Data Integrity**
```bash
# Compare row counts (if primary region accessible for comparison)
psql -h prod-db-secondary.$SECONDARY_REGION.example.com -U postgres -d production -c "
SELECT
  schemaname,
  tablename,
  n_live_tup AS row_count
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY n_live_tup DESC
LIMIT 20;
"

# Check for replication gaps (if applicable)
psql -h prod-db-secondary.$SECONDARY_REGION.example.com -U postgres -c "
SELECT * FROM dr_region_failover_test ORDER BY id DESC LIMIT 5;
"
```

## Procedure B: Active-Active Failover

### Phase 1: Assessment (5 minutes)

**Step 1.1: Verify Primary Region Failure**
```bash
# Check global load balancer health
aws globalaccelerator describe-accelerator \
  --accelerator-arn arn:aws:globalaccelerator::123456789012:accelerator/abc123

# Check endpoint group health
aws globalaccelerator describe-endpoint-group \
  --endpoint-group-arn arn:aws:globalaccelerator::123456789012:accelerator/abc123/listener/xyz/endpoint-group/def456
```

**Step 1.2: Verify Secondary Region Capacity**
```bash
# Both regions already handle production traffic
# Check if secondary can handle 100% load
SECONDARY_CAPACITY=$(aws autoscaling describe-auto-scaling-groups \
  --auto-scaling-group-names prod-app-asg-$SECONDARY_REGION \
  --region $SECONDARY_REGION \
  --query 'AutoScalingGroups[0].DesiredCapacity')

# Verify sufficient capacity (typically 50% can scale to 100%)
echo "Secondary region current capacity: $SECONDARY_CAPACITY"
```

### Phase 2: Traffic Rerouting (5 minutes)

**Step 2.1: Update Global Load Balancer**
```bash
# Remove primary region endpoints
aws globalaccelerator update-endpoint-group \
  --endpoint-group-arn arn:aws:globalaccelerator::123456789012:accelerator/abc123/listener/xyz/endpoint-group/def456 \
  --endpoint-configurations '[
    {
      "EndpointId": "arn:aws:elasticloadbalancing:us-west-2:123456789012:loadbalancer/app/prod-lb/xyz",
      "Weight": 100,
      "ClientIPPreservationEnabled": true
    }
  ]'

# Traffic now flows 100% to secondary region
echo "$(date -Iseconds): Traffic rerouted to secondary region" >> $FAILOVER_LOG
```

**Step 2.2: Scale Secondary Region**
```bash
# Auto-scaling should handle increased load automatically
# Monitor for 5 minutes to ensure scaling triggers

for i in {1..10}; do
  CURRENT=$(aws autoscaling describe-auto-scaling-groups \
    --auto-scaling-group-names prod-app-asg-$SECONDARY_REGION \
    --region $SECONDARY_REGION \
    --query 'AutoScalingGroups[0].[DesiredCapacity,Instances[?HealthStatus==`Healthy`]|length(@)]' \
    --output text)

  echo "Iteration $i: Desired/Healthy - $CURRENT"
  sleep 30
done
```

### Phase 3: Validation (10 minutes)

**Step 3.1: Monitor Application Performance**
```bash
# Check error rates
curl "http://prometheus.example.com/api/v1/query?query=rate(http_requests_total{status=~'5..'}[5m])"

# Check response times
curl "http://prometheus.example.com/api/v1/query?query=histogram_quantile(0.95,rate(http_request_duration_seconds_bucket[5m]))"

# Check CPU utilization
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=AutoScalingGroupName,Value=prod-app-asg-$SECONDARY_REGION \
  --region $SECONDARY_REGION \
  --start-time $(date -u -d '10 minutes ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average
```

## Procedure C: Pilot Light Failover

### Phase 1: Provision Infrastructure (30-45 minutes)

**Step 1.1: Deploy Infrastructure via IaC**
```bash
# Use Terraform to provision secondary region
cd /infrastructure/terraform/secondary-region

# Initialize and plan
terraform init
terraform plan -var="region=$SECONDARY_REGION" -var="environment=production"

# Apply with auto-approve (emergency failover)
terraform apply -auto-approve -var="region=$SECONDARY_REGION" -var="environment=production"

# Record deployment
echo "$(date -Iseconds): Infrastructure provisioned in $SECONDARY_REGION" >> $FAILOVER_LOG
```

**Step 1.2: Deploy Application**
```bash
# Deploy using CI/CD pipeline or kubectl
kubectl apply -f /manifests/production/ -n production

# Wait for deployments
kubectl wait --for=condition=available --timeout=600s \
  deployment --all -n production
```

**Step 1.3: Follow Active-Passive Procedure**
```bash
# Continue with Phase 2 of Active-Passive procedure (database failover)
# Then Phase 3 (scale up), Phase 4 (DNS), Phase 5 (validation)
```

## Rollback Procedure

**Use rollback when:**
- Secondary region exhibits critical issues post-failover
- Primary region becomes available and stable
- Data integrity issues discovered in secondary

### Rollback Steps

**Step 1: Verify Primary Region Recovery**
```bash
# Check AWS service health
aws health describe-events \
  --filter eventTypeCategories=issue \
  --region $PRIMARY_REGION

# Test primary region endpoints
for service in api.example.com db.example.com; do
  curl -f -m 10 "https://$service/health"
done
```

**Step 2: Restore Primary Database**
```bash
# Recreate replication from secondary to primary
aws rds create-db-instance-read-replica \
  --db-instance-identifier prod-db-primary-restored \
  --source-db-instance-identifier prod-db-secondary \
  --region $PRIMARY_REGION

# Wait for replication to catch up
# Then promote primary
```

**Step 3: Reverse Traffic Cutover**
```bash
# Update DNS back to primary region
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch "{
    \"Changes\": [{
      \"Action\": \"UPSERT\",
      \"ResourceRecordSet\": {
        \"Name\": \"api.example.com\",
        \"Type\": \"CNAME\",
        \"TTL\": 60,
        \"ResourceRecords\": [{\"Value\": \"PRIMARY_LB_DNS\"}]
      }
    }]
  }"
```

## Post-Failover Tasks

**Immediate (Within 1 Hour):**
- [ ] Update status page with resolution
- [ ] Notify all stakeholders
- [ ] Verify all monitoring alerts cleared
- [ ] Document actual RTO/RPO achieved
- [ ] Create incident timeline

**Short-term (Within 24 Hours):**
- [ ] Conduct incident retrospective
- [ ] Analyze root cause of region failure
- [ ] Review cloud provider incident reports
- [ ] Update runbook with lessons learned
- [ ] Test rollback procedure in non-production

**Long-term (Within 1 Week):**
- [ ] Restore original architecture (if Active-Passive)
- [ ] Rebuild primary region infrastructure
- [ ] Re-establish cross-region replication
- [ ] Review and update RTO/RPO targets
- [ ] Schedule follow-up DR drill
- [ ] Update disaster recovery documentation

## Troubleshooting

### Issue: Secondary region cannot handle full load

**Symptoms:** High CPU, response time degradation, connection errors

**Resolution:**
```bash
# Emergency scale-up
aws autoscaling set-desired-capacity \
  --auto-scaling-group-name prod-app-asg-$SECONDARY_REGION \
  --desired-capacity 50 \
  --region $SECONDARY_REGION

# Add more instance types if capacity exhausted
aws autoscaling update-auto-scaling-group \
  --auto-scaling-group-name prod-app-asg-$SECONDARY_REGION \
  --region $SECONDARY_REGION \
  --mixed-instances-policy '{
    "InstancesDistribution": {"OnDemandPercentageAboveBaseCapacity": 100},
    "LaunchTemplate": {"LaunchTemplateSpecification": {...},
    "Overrides": [
      {"InstanceType": "c5.2xlarge"},
      {"InstanceType": "c5.4xlarge"},
      {"InstanceType": "m5.2xlarge"}
    ]}
  }'
```

### Issue: Database replication lag too high

**Symptoms:** Secondary database minutes or hours behind primary

**Resolution:**
```bash
# Check replication status
aws rds describe-db-instances \
  --db-instance-identifier prod-db-secondary \
  --region $SECONDARY_REGION \
  --query 'DBInstances[0].StatusInfos'

# Options:
# 1. Wait for replication to catch up (if time permits)
# 2. Accept data loss and promote (document RPO breach)
# 3. Restore from latest backup if replication broken
```

### Issue: DNS not propagating

**Symptoms:** Some users still hitting primary region, mixed results

**Resolution:**
```bash
# Check DNS propagation globally
for server in 8.8.8.8 1.1.1.1 208.67.222.222 4.2.2.2; do
  echo "Nameserver $server:"
  dig @$server api.example.com +short
done

# Flush CloudFlare cache if using CDN
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"purge_everything":true}'

# If TTL too high, users must wait for expiration
# Consider implementing client-side failover logic
```

### Issue: Application cannot reach secondary database

**Symptoms:** Database connection errors, authentication failures

**Resolution:**
```bash
# Check security groups
aws ec2 describe-security-groups \
  --region $SECONDARY_REGION \
  --group-ids sg-xyz123 \
  --query 'SecurityGroups[0].IpPermissions'

# Add application security group to database security group
aws ec2 authorize-security-group-ingress \
  --region $SECONDARY_REGION \
  --group-id sg-database \
  --source-group sg-application \
  --protocol tcp \
  --port 5432

# Verify network connectivity
kubectl run -it --rm debug --image=postgres:15 --restart=Never -- \
  psql -h prod-db-secondary.$SECONDARY_REGION.example.com -U postgres -c "SELECT 1"
```

## RTO/RPO Tracking

**Calculate Actual Metrics:**
```bash
# Extract timestamps from failover log
FAILURE_TIME=$(grep "REGION FAILOVER INITIATED" $FAILOVER_LOG | awk '{print $3}')
TRAFFIC_RESTORED=$(grep "DNS updated to secondary region" $FAILOVER_LOG | awk '{print $3}')
SERVICE_VALIDATED=$(grep "All instances healthy" $FAILOVER_LOG | awk '{print $3}')

# Calculate RTO
echo "=== Failover Metrics ===" >> $FAILOVER_LOG
echo "Failure Detection: $FAILURE_TIME" >> $FAILOVER_LOG
echo "Traffic Cutover: $TRAFFIC_RESTORED" >> $FAILOVER_LOG
echo "Service Validated: $SERVICE_VALIDATED" >> $FAILOVER_LOG

# RPO from replication lag
echo "Replication Lag (RPO): $LAG_SECONDS seconds" >> $FAILOVER_LOG
```

## Automation Scripts

**Automated region failover:**
```bash
/Users/antoncoleman/Documents/repos/ai-design-components/skills/planning-disaster-recovery/scripts/automated-region-failover.sh \
  --primary-region us-east-1 \
  --secondary-region us-west-2 \
  --architecture active-passive \
  --verify-health
```

**DR drill execution:**
```bash
/Users/antoncoleman/Documents/repos/ai-design-components/skills/planning-disaster-recovery/scripts/dr-drill.sh \
  --environment staging \
  --test-type region
```

## Related Runbooks

- **Database Failover:** `examples/runbooks/database-failover.md`
- **Kubernetes Recovery:** `references/kubernetes-dr.md`
- **Cloud DR Patterns:** `references/cloud-dr-patterns.md`
- **Cross-Region Replication:** `references/cross-region-replication.md`

## References

- AWS Multi-Region Architecture: https://aws.amazon.com/solutions/implementations/disaster-recovery/
- GCP Disaster Recovery: https://cloud.google.com/architecture/dr-scenarios-planning-guide
- Azure Site Recovery: https://docs.microsoft.com/azure/site-recovery/
- RTO/RPO Planning Guide: `references/rto-rpo-planning.md`
