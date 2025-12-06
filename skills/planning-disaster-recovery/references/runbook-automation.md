# Runbook Automation Guide

## Table of Contents

1. [Automated DR Runbook Structure](#automated-dr-runbook-structure)
2. [Example Automated Failover Script](#example-automated-failover-script)
3. [DR Drill Automation](#dr-drill-automation)
4. [Monitoring Integration](#monitoring-integration)

## Automated DR Runbook Structure

### Phase 1: Detection
- Monitor triggers alert (automated)
- Incident declared (manual or automated)
- Stakeholders notified

### Phase 2: Assessment
- Verify scope of failure
- Determine if failover required
- Check secondary region health

### Phase 3: Execution
- Promote secondary database
- Scale up application servers
- Update DNS/load balancer
- Verify application health

### Phase 4: Verification
- Test critical user journeys
- Verify data integrity
- Confirm RTO/RPO met

### Phase 5: Communication
- Update status page
- Notify customers
- Document incident

## Example Automated Failover Script

```bash
#!/bin/bash
# scripts/automated-failover.sh

set -euo pipefail

SECONDARY_REGION="us-west-2"
PRIMARY_REGION="us-east-1"
LOG_FILE="/var/log/dr-failover-$(date +%Y%m%d-%H%M%S).log"

log() {
  echo "[$(date -Iseconds)] $*" | tee -a "$LOG_FILE"
}

check_primary_health() {
  log "Checking primary region health..."
  if curl -f -m 10 https://primary-lb.example.com/health 2>/dev/null; then
    log "Primary is healthy - aborting failover"
    exit 0
  fi
  log "Primary unhealthy - proceeding with failover"
}

promote_secondary_db() {
  log "Promoting secondary database..."
  aws rds promote-read-replica \
    --region "$SECONDARY_REGION" \
    --db-instance-identifier prod-db-secondary

  # Wait for promotion
  while true; do
    STATUS=$(aws rds describe-db-instances \
      --region "$SECONDARY_REGION" \
      --db-instance-identifier prod-db-secondary \
      --query 'DBInstances[0].DBInstanceStatus' \
      --output text)

    if [[ "$STATUS" == "available" ]]; then
      log "Database promoted successfully"
      break
    fi
    sleep 10
  done
}

update_dns() {
  log "Updating DNS to point to secondary..."
  # Update Route53 DNS records
  aws route53 change-resource-record-sets \
    --hosted-zone-id Z1234567890ABC \
    --change-batch '{"Changes":[{"Action":"UPSERT","ResourceRecordSet":{"Name":"app.example.com","Type":"CNAME","TTL":60,"ResourceRecords":[{"Value":"secondary-lb.example.com"}]}}]}'
}

verify_failover() {
  log "Verifying failover success..."
  sleep 30  # Wait for DNS propagation

  for i in {1..10}; do
    if curl -f https://app.example.com/health 2>/dev/null; then
      log "Failover verified - application healthy"
      return 0
    fi
    log "Attempt $i failed, retrying..."
    sleep 10
  done

  log "ERROR: Failover verification failed"
  return 1
}

# Main execution
log "=== Starting DR Failover ==="
check_primary_health
promote_secondary_db
update_dns
verify_failover
log "=== Failover Complete ==="
```

## DR Drill Automation

```bash
#!/bin/bash
# scripts/dr-drill.sh

ENVIRONMENT="${1:-staging}"
TEST_TYPE="${2:-database}"

echo "Running DR drill: $TEST_TYPE in $ENVIRONMENT"

case $TEST_TYPE in
  database)
    # Test database failover
    ./examples/chaos/db-failover-test.sh
    ;;
  region)
    # Test region failover
    ./examples/chaos/region-failure-test.sh
    ;;
  kubernetes)
    # Test K8s namespace recovery
    ./examples/chaos/k8s-namespace-recovery-test.sh
    ;;
  full)
    # Run all tests
    echo "Running comprehensive DR drill..."
    ./examples/chaos/db-failover-test.sh
    ./examples/chaos/region-failure-test.sh
    ./examples/chaos/k8s-namespace-recovery-test.sh
    ;;
  *)
    echo "Unknown test type: $TEST_TYPE"
    exit 1
    ;;
esac
```

## Monitoring Integration

### Prometheus Alert for Triggering DR

```yaml
groups:
  - name: planning-disaster-recovery
    rules:
      - alert: PrimaryRegionDown
        expr: up{job="app", region="us-east-1"} == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: Primary region unavailable
          description: Consider DR failover
```

### Auto-Remediation with AlertManager

```yaml
receivers:
  - name: 'dr-webhook'
    webhook_configs:
      - url: 'https://dr-automation.example.com/trigger-failover'
        send_resolved: true
```
