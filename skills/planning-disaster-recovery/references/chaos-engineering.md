# Chaos Engineering for DR Validation

## Chaos Engineering Principles

1. **Start Small:** Begin in staging with limited blast radius
2. **Hypothesize:** Define expected behavior before experiment
3. **Measure:** Quantify impact (latency, error rate, availability)
4. **Automate:** Integrate into CI/CD for continuous validation
5. **Learn:** Document findings, improve systems and runbooks

## DR Test Scenarios

### Database Failover Test

**Hypothesis:** Application continues with < 30s downtime when primary DB fails.

**Procedure:**
```bash
#!/bin/bash
# chaos/db-failover-test.sh

# Collect baseline metrics
BASELINE_ERROR_RATE=$(curl -s http://prometheus:9090/api/v1/query?query='rate(http_requests_total{status=~"5.."}[1m])')

# Simulate failure
ssh primary-db "sudo systemctl stop postgresql"

# Measure recovery time
START=$(date +%s)
while true; do
  ERROR_RATE=$(curl -s http://prometheus:9090/api/v1/query?query='rate(http_requests_total{status=~"5.."}[1m])')
  if [[ $(echo "$ERROR_RATE < $BASELINE_ERROR_RATE * 1.1" | bc) -eq 1 ]]; then
    END=$(date +%s)
    DOWNTIME=$((END - START))
    echo "Recovery: ${DOWNTIME}s"
    break
  fi
  sleep 1
done

# Verify secondary promoted
RECOVERY_STATUS=$(psql -h db-vip -c "SELECT pg_is_in_recovery();" -t)
if [[ "$RECOVERY_STATUS" == "f" ]]; then
  echo "PASS: Secondary promoted"
else
  echo "FAIL: Secondary not promoted"
fi
```

### Region Failure Test

**Hypothesis:** Application fails over to secondary region with < 5 min RTO.

**Steps:**
1. Block network to primary region (AWS NACL deny rule)
2. Trigger DNS failover to secondary
3. Measure time until application healthy
4. Cleanup and restore primary

**See:** `examples/chaos/region-failure-test.sh`

### Kubernetes Namespace Recovery

**Hypothesis:** Velero restores deleted namespace within 10 minutes.

**Steps:**
1. Capture current state
2. Delete namespace
3. Restore from Velero backup
4. Verify resource count matches
5. Confirm restore time < 10 min

**See:** `examples/chaos/k8s-namespace-recovery-test.sh`

## Chaos Engineering Tools

| Tool | Use Case | Platform |
|------|----------|----------|
| **Chaos Mesh** | Kubernetes chaos | K8s |
| **Gremlin** | Enterprise platform | Multi-cloud |
| **Litmus** | Cloud-native chaos | K8s |
| **Chaos Monkey** | Instance termination | AWS/GCP/Azure |
| **Toxiproxy** | Network failures | Any |

## Failure Injection Techniques

- Pod/container termination
- Network latency/partition
- Database connection failures
- Disk fill
- Data corruption
- DNS resolution failures
- Region/AZ outages
