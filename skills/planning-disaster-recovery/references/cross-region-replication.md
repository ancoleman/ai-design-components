# Cross-Region Replication Patterns

## Active-Passive Pattern

**Use Case:** Primary region handles all traffic, secondary on standby for failover.

**RTO:** 15-60 minutes | **RPO:** 5-15 minutes | **Cost:** Medium

**Architecture:**
- Primary: All application servers, read/write database
- Secondary: Stopped/minimal servers, read-only database replica
- Failover: Promote secondary DB, start servers, update DNS

**PostgreSQL Implementation:**
```bash
# Primary: Enable replication
ALTER SYSTEM SET wal_level = 'replica';
ALTER SYSTEM SET max_wal_senders = 5;
CREATE USER replicator WITH REPLICATION;

# Secondary: Setup streaming replication
pg_basebackup -h primary -U replicator -D /var/lib/postgresql/14/main -P -R

# Failover: Promote secondary
pg_ctl promote -D /var/lib/postgresql/14/main
```

## Active-Active Pattern

**Use Case:** Both regions serve traffic simultaneously.

**RTO:** < 1 minute | **RPO:** < 1 minute | **Cost:** High

**Architecture:**
- Both regions: Full application stack
- Database: Multi-master or Aurora Global DB
- Load balancer: Route to nearest region with automatic failover

**Aurora Global DB Example:**
Use Aurora Global Database for multi-region active-active replication with automatic promotion capability.

## Pilot Light Pattern

**Use Case:** Minimal secondary infrastructure, rapid scale-up on failover.

**RTO:** 10-30 minutes | **RPO:** 5-15 minutes | **Cost:** Low

**Architecture:**
- Primary: Full stack
- Secondary: Database replica (running), AMIs pre-baked, ASGs at min=0
- Failover: Scale ASGs, promote DB, update DNS

**AWS Lambda Failover:**
```python
import boto3

def failover_handler(event, context):
    asg = boto3.client('autoscaling', region_name='us-west-2')
    asg.set_desired_capacity(
        AutoScalingGroupName='app-secondary',
        DesiredCapacity=5
    )
    # Update Route53 DNS to secondary
```

## Warm Standby Pattern

**Use Case:** Scaled-down secondary infrastructure for faster failover.

**RTO:** 5-15 minutes | **RPO:** 5-15 minutes | **Cost:** Medium-High

**Architecture:**
- Primary: Full capacity
- Secondary: 20-50% capacity (running), replicated database
- Failover: Scale up secondary, update DNS
