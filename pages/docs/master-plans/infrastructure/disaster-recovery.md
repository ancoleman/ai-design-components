---
sidebar_position: 9
title: Disaster Recovery
description: Master plan for DR strategies including RTO/RPO planning, backup patterns, database DR, Kubernetes DR, and cross-region replication
tags: [master-plan, infrastructure, disaster-recovery, backup, business-continuity]
---

# Disaster Recovery

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Disaster recovery has evolved from "nice-to-have" to business-critical. This skill covers RTO/RPO planning, backup strategies, database-specific DR, Kubernetes DR, cross-region replication, and chaos engineering validation.

## Scope

This skill teaches:

- **RTO/RPO Planning** - Recovery time/point objectives, criticality tiers, cost-benefit analysis
- **Backup Strategy Design** - Full/incremental/differential backups, 3-2-1 rule, immutable backups
- **Database DR** - PostgreSQL (pgBackRest, WAL-G), MySQL (Percona XtraBackup), MongoDB
- **Kubernetes DR** - Velero cluster backups, PV snapshots, etcd backup/restore
- **Cross-Region Replication** - AWS (S3 CRR, RDS Multi-AZ), GCP (Multi-Regional Storage), Azure (GRS)
- **Chaos Engineering** - DR testing, recovery drills, runbook automation

## Key Components

### RTO/RPO Framework

**Recovery Time Objective (RTO)** - Maximum acceptable downtime
**Recovery Point Objective (RPO)** - Maximum acceptable data loss

| Tier | RTO | RPO | Strategy | Cost |
|------|-----|-----|----------|------|
| **Critical** | < 1 hour | < 15 min | Hot standby, continuous replication | $$$$ |
| **Important** | < 4 hours | < 1 hour | Warm standby, frequent backups | $$$ |
| **Standard** | < 24 hours | < 4 hours | Cold backups, daily snapshots | $$ |
| **Low Priority** | < 1 week | < 24 hours | Archived backups, weekly snapshots | $ |

### Backup Strategies

**3-2-1 Backup Rule:**
- **3 copies** - Production + 2 backups
- **2 different media types** - Local disk + cloud storage
- **1 offsite** - Protect against site-wide disasters

**Backup Types:**
- **Full**: Complete data copy (highest storage, fastest recovery)
- **Incremental**: Only changes since last backup (lowest storage, slower recovery)
- **Differential**: Changes since last full backup (medium storage/recovery)
- **Continuous**: Real-time replication (highest cost, lowest RPO)

**Immutable Backups** - Ransomware protection via write-once-read-many (WORM)

### Database-Specific DR

**PostgreSQL:**
- pgBackRest - Full/incremental/differential, PITR
- WAL-G - WAL archiving, cloud-native
- Barman - Backup management, retention policies
- Point-in-Time Recovery (PITR) via WAL replay

**MySQL:**
- Percona XtraBackup - Hot backups, incremental
- mysqldump - Logical backups
- Binary log replication for DR

**MongoDB:**
- mongodump - Logical backups
- Ops Manager - Enterprise backup management
- Replica set failover

### Kubernetes DR

**Velero** - Cluster backup and restore
- Namespace-level or cluster-level backups
- Persistent volume snapshots
- Backup schedules and retention
- Cross-cluster migration

**etcd Backup** - Kubernetes state store
- Regular etcd snapshots
- Automated backup to object storage
- Restore procedures

## Decision Framework

**Which DR Strategy?**

```
What's your RTO?
  < 1 hour → Hot standby required
              → Multi-region active-active OR
                 Multi-AZ with automated failover
  < 4 hours → Warm standby acceptable
              → Frequent backups (hourly) +
                 Automated restore scripts
  < 24 hours → Cold backups sufficient
               → Daily snapshots +
                  Manual restore procedures
  < 1 week → Archived backups
              → Weekly backups, tape/glacier storage
```

**Database DR Pattern Selection:**

```
PostgreSQL?
  YES → Need PITR?
          YES → pgBackRest or WAL-G
          NO → pg_dump (simple, logical)

MySQL?
  YES → Hot backups?
          YES → Percona XtraBackup
          NO → mysqldump

MongoDB?
  YES → Enterprise?
          YES → Ops Manager
          NO → mongodump + replica sets
```

## Tool Recommendations

### Backup Tools

**PostgreSQL:**
- pgBackRest - Production-grade, PITR support
- WAL-G - Cloud-native, S3/GCS/Azure Blob
- Barman - Backup manager, retention automation

**MySQL:**
- Percona XtraBackup - Hot backups, no downtime
- mysqldump - Logical backups, simple

**Kubernetes:**
- Velero - Industry standard for K8s backups
- Kasten K10 - Enterprise K8s data management
- Stash - Kubernetes native backup

**Object Storage:**
- AWS S3 - Cross-region replication (CRR)
- GCP Cloud Storage - Multi-regional buckets
- Azure Storage - Geo-redundant storage (GRS)

### Chaos Engineering

**Chaos Monkey** - Netflix's production testing tool
**Litmus Chaos** - Kubernetes chaos engineering
**Gremlin** - Failure injection platform

## Integration Points

**With Other Skills:**
- `infrastructure-as-code` - Automate DR infrastructure (Terraform/Pulumi)
- `kubernetes-operations` - K8s-specific DR patterns
- `observability` - Monitor backup success, test recovery times
- `security-hardening` - Encrypt backups, access controls
- `testing-strategies` - DR drill automation, runbook testing

**Workflow Example:**
```
Daily Operations → Continuous Backup → Disaster Occurs → Recovery
        │                 │                  │             │
        ▼                 ▼                  ▼             ▼
    Monitor         Velero/WAL-G      Detect via      Restore from
    metrics         to S3/GCS         alerts          backup +
                                                      failover DNS
```

## Learn More

- [Full Master Plan (init.md)](https://github.com/ancoleman/ai-design-components/blob/main/skills/disaster-recovery/init.md)
- Related: `infrastructure-as-code`, `kubernetes-operations`, `observability`
