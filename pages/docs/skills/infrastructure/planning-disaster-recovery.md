---
sidebar_position: 6
title: Planning Disaster Recovery
description: RTO/RPO planning, database backups, Kubernetes DR, and chaos engineering
tags: [infrastructure, disaster-recovery, backup, chaos-engineering]
---

# Planning Disaster Recovery

Design and implement disaster recovery strategies with RTO/RPO planning, database backups, Kubernetes DR, cross-region replication, and chaos engineering testing.

## When to Use

Use when:
- Defining recovery time objectives (RTO) and recovery point objectives (RPO)
- Implementing database backups with point-in-time recovery (PITR)
- Setting up Kubernetes cluster backup and restore workflows
- Configuring cross-region replication for high availability
- Testing disaster recovery procedures through chaos experiments
- Meeting compliance requirements (GDPR, SOC 2, HIPAA)
- Automating backup monitoring and alerting

## Core Concepts

### RTO and RPO Fundamentals

**Recovery Time Objective (RTO):** Maximum acceptable downtime after a disaster before business impact becomes unacceptable.

**Recovery Point Objective (RPO):** Maximum acceptable data loss measured in time.

**Criticality Tiers:**
- **Tier 0 (Mission-Critical):** RTO < 1 hour, RPO < 5 minutes
- **Tier 1 (Production):** RTO 1-4 hours, RPO 15-60 minutes
- **Tier 2 (Important):** RTO 4-24 hours, RPO 1-6 hours
- **Tier 3 (Standard):** RTO > 24 hours, RPO > 6 hours

### 3-2-1 Backup Rule

Maintain **3 copies** of data on **2 different media** types with **1 copy offsite**.

Example implementation:
- Primary: Production database
- Secondary: Local backup storage
- Tertiary: Cloud backup (S3/GCS/Azure)

### Backup Types

**Full Backup:** Complete copy of all data. Slowest to create, fastest to restore.

**Incremental Backup:** Only changes since last backup. Fastest to create, requires full + all incrementals to restore.

**Differential Backup:** Changes since last full backup. Balance between storage and restore speed.

**Continuous Backup:** Real-time or near-real-time via WAL/binlog archiving. Lowest RPO.

## Decision Framework

### Step 1: Map RTO/RPO to Strategy

```
RTO < 1 hour, RPO < 5 min
→ Active-Active replication, continuous archiving, automated failover
→ Tools: Aurora Global DB, GCS Multi-Region, pgBackRest PITR
→ Cost: Highest

RTO 1-4 hours, RPO 15-60 min
→ Warm standby, incremental backups, automated failover
→ Tools: pgBackRest, WAL-G, RDS Multi-AZ
→ Cost: High

RTO 4-24 hours, RPO 1-6 hours
→ Daily full + incremental, cross-region backup
→ Tools: pgBackRest, Velero, Restic
→ Cost: Medium

RTO > 24 hours, RPO > 6 hours
→ Weekly full + daily incremental, single region
→ Tools: pg_dump, mysqldump, S3 versioning
→ Cost: Low
```

### Step 2: Select Backup Tools

| Use Case | Primary Tool | Alternative | Key Feature |
|----------|-------------|-------------|-------------|
| PostgreSQL production | pgBackRest | WAL-G | PITR, compression, multi-repo |
| MySQL production | Percona XtraBackup | WAL-G | Hot backups, incremental |
| MongoDB | Atlas Backup | mongodump | Continuous backup, PITR |
| Kubernetes cluster | Velero | ArgoCD + Git | PV snapshots, scheduling |
| File/object backup | Restic | Duplicity | Encryption, deduplication |

## Database Backup Patterns

### PostgreSQL with pgBackRest

**Use Case:** Production PostgreSQL with < 5 minute RPO

Configure continuous WAL archiving with full/differential/incremental backups to S3/GCS/Azure. Schedule weekly full, daily differential backups.

**Restore:**
```bash
pgbackrest --stanza=main --delta restore
```

### MySQL with Percona XtraBackup

**Use Case:** MySQL production requiring hot backups

Perform full and incremental backups with binary log archiving for PITR.

**Backup:**
```bash
xtrabackup --backup --parallel=4 --target-dir=/backups/full
```

### Kubernetes with Velero

**Quick Start:**
```bash
velero install --provider aws --bucket my-backups

# Create backup
velero backup create production-backup --include-namespaces production

# Restore
velero restore create --from-backup production-backup
```

## Cross-Region Replication

| Pattern | RTO | RPO | Cost | Use Case |
|---------|-----|-----|------|----------|
| **Active-Active** | < 1 min | < 1 min | High | Both regions serve traffic |
| **Active-Passive** | 15-60 min | 5-15 min | Medium | Standby for failover |
| **Pilot Light** | 10-30 min | 5-15 min | Low | Minimal secondary infra |
| **Warm Standby** | 5-15 min | 5-15 min | Med-High | Scaled-down secondary |

**Implementation Examples:**
- PostgreSQL streaming replication (Active-Passive)
- Aurora Global Database (Active-Active)
- ASG scale-up automation (Pilot Light)

## Chaos Engineering

### Purpose
Validate DR procedures through controlled failure injection.

### Test Scenarios
- Database failover (stop primary, measure promotion time)
- Region failure (block network, trigger DNS failover)
- Kubernetes recovery (delete namespace, restore from Velero)

**Tools:** Chaos Mesh, Gremlin, Litmus, Toxiproxy

### Automated DR Drills

```bash
./scripts/dr-drill.sh --environment staging --test-type full
./scripts/test-restore.sh --backup latest --target staging-db
```

## Compliance and Retention

| Regulation | Retention | Requirements |
|------------|-----------|--------------|
| GDPR | 1-7 years | EU data residency, right to erasure |
| SOC 2 | 1 year+ | Secure deletion, access controls |
| HIPAA | 6 years | Encryption, PHI protection |
| PCI DSS | 3mo-1yr | Secure deletion, quarterly reviews |

**Implement with lifecycle policies:**
- 30d → Standard-IA
- 90d → Glacier
- 365d → Deep Archive

**Immutable backups:** S3 Object Lock or Azure Immutable Blob Storage for ransomware protection.

## Monitoring and Alerting

**Key Metrics:**
- Backup success rate
- Backup duration
- Time since last backup
- RPO breach
- Storage utilization

**Validation Scripts:**
```bash
./scripts/validate-backup.sh --backup latest --verify-integrity
./scripts/check-retention.sh --report-violations
./scripts/generate-dr-report.sh --format pdf
```

## Best Practices

### Do
- ✓ Test restores regularly (monthly for critical systems)
- ✓ Automate backup monitoring and alerting
- ✓ Encrypt backups at rest and in transit
- ✓ Implement 3-2-1 backup rule
- ✓ Run chaos experiments to validate DR
- ✓ Document recovery procedures
- ✓ Use immutable backups for ransomware protection

### Don't
- ✗ Assume backups work without testing
- ✗ Store all backups in single region
- ✗ Skip retention policy definition
- ✗ Forget to encrypt sensitive data
- ✗ Ignore backup monitoring
- ✗ Store encryption keys with backups

## Related Skills

- [Writing Infrastructure Code](./writing-infrastructure-code) - Provision backup infrastructure, DR regions
- [Operating Kubernetes](./operating-kubernetes) - K8s cluster setup for Velero
- [Architecting Networks](./architecting-networks) - Multi-region failover networking
- [Managing Configuration](./managing-configuration) - Ansible for DR automation

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/planning-disaster-recovery)
- RTO/RPO Planning: `references/rto-rpo-planning.md`
- Database Backups: `references/database-backups.md`
- Kubernetes DR: `references/kubernetes-dr.md`
- Cross-Region Replication: `references/cross-region-replication.md`
- Chaos Engineering: `references/chaos-engineering.md`
- Compliance Requirements: `references/compliance-retention.md`
