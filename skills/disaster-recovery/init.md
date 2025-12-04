# Disaster Recovery Skill - Master Plan

**Skill Name:** `disaster-recovery`
**Skill Level:** High Level (8,000-12,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [DR Strategy Taxonomy](#dr-strategy-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Database Backup Patterns](#database-backup-patterns)
7. [Kubernetes DR Patterns](#kubernetes-dr-patterns)
8. [Cloud-Specific DR Patterns](#cloud-specific-dr-patterns)
9. [Cross-Region Replication](#cross-region-replication)
10. [Chaos Engineering for DR](#chaos-engineering-for-dr)
11. [Tool Recommendations](#tool-recommendations)
12. [Skill Structure Design](#skill-structure-design)
13. [Integration Points](#integration-points)
14. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why Disaster Recovery Matters in 2025

Disaster recovery (DR) has evolved from "nice-to-have" to business-critical infrastructure. In 2025, with cloud-native architectures, distributed systems, and regulatory compliance requirements, comprehensive DR capabilities are essential.

**Market Drivers:**

- **Zero Downtime Expectations:** Customers expect 99.99%+ availability (52 minutes downtime/year)
- **Ransomware Pandemic:** Immutable backups and rapid recovery are survival requirements
- **Multi-Cloud Reality:** DR strategies must work across AWS, GCP, Azure, on-premises
- **Regulatory Compliance:** GDPR, SOC 2, HIPAA mandate data retention and recovery capabilities
- **Cloud-Native Complexity:** Kubernetes, microservices, distributed databases require specialized DR approaches

**Strategic Value:**

1. **Business Continuity Foundation:** Systems can fail; recovery capability determines survival
2. **Compliance Enabler:** Regulatory requirements demand proven DR capabilities
3. **Risk Mitigation:** Reduces financial impact of outages, data loss, ransomware
4. **Customer Trust:** Demonstrable DR builds confidence in service reliability

### How This Differs from Existing Solutions

**Existing DR Documentation:**
- **Tool-Specific:** Velero docs OR pgBackRest docs, not unified
- **Single-Layer Focus:** Database backups OR infrastructure OR Kubernetes
- **Tactical:** "How to run a backup" vs "How to design a DR strategy"
- **Limited Testing Guidance:** Assumes backups work without validation

**Our Approach:**
- **Decision Framework:** RTO/RPO → DR strategy mapping
- **Full-Stack Coverage:** Databases, Kubernetes, infrastructure, application-level
- **Multi-Cloud Patterns:** AWS, GCP, Azure with unified concepts
- **Testing & Validation:** Chaos engineering, DR drills, runbook automation
- **Operational Reality:** Drift detection, data integrity, compliance reporting

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **RTO/RPO Planning**
   - Defining recovery time objectives (RTO)
   - Defining recovery point objectives (RPO)
   - Classifying criticality tiers
   - Cost-benefit analysis of DR strategies

2. **Backup Strategy Design**
   - Full, incremental, differential, continuous backups
   - 3-2-1 backup rule (3 copies, 2 media, 1 offsite)
   - Immutable backups for ransomware protection
   - Backup retention policies

3. **Database-Specific DR**
   - PostgreSQL: pgBackRest, WAL-G, Barman
   - MySQL: Percona XtraBackup, mysqldump, WAL-G
   - MongoDB: mongodump, Ops Manager
   - Point-in-Time Recovery (PITR)

4. **Kubernetes DR**
   - Velero for cluster backups
   - Persistent volume snapshots
   - etcd backup and restore
   - Namespace-level and cluster-level recovery

5. **Cross-Region Replication**
   - AWS: S3 CRR, RDS Multi-AZ, Aurora Global Database
   - GCP: Multi-Regional Storage, Cloud SQL HA
   - Azure: GRS, RA-GRS, Azure Site Recovery
   - Active-Active vs Active-Passive patterns

6. **DR Testing & Validation**
   - Chaos engineering for DR validation
   - Automated DR drills
   - Runbook development and testing
   - Data integrity verification
   - Compliance reporting

### What This Skill Does NOT Cover

- **Specific database operations** → Use `databases-postgresql`, `databases-mysql` skills
- **Infrastructure provisioning** → Use `infrastructure-as-code` skill
- **Monitoring/alerting setup** → Use `observability` skill
- **Incident response procedures** → Use `incident-management` skill
- **Security hardening** → Use `security-hardening` skill

**Integration:** This skill focuses on DR strategy and implementation. It integrates with other skills for complete coverage.

---

## Research Findings

### Google Search Grounding Results (December 2025)

#### Query 1: Disaster Recovery Best Practices 2025 RTO RPO Cloud

**Key Findings:**

- **3-2-1 Rule Remains Gold Standard:** Keep 3 copies of data on 2 different media, with 1 copy offsite
- **Immutable Backups Critical:** Protection against ransomware requires immutable, air-gapped backups
- **Cloud DR Benefits:** Scalability, flexibility, automated failover, cross-region replication
- **DRaaS Growth:** Disaster Recovery as a Service (DRaaS) providers handle setup, replication, failover
- **Automation Priority:** Automate DR testing, infrastructure rebuilding, failover orchestration

**RTO/RPO Definitions:**
- **RTO:** Maximum acceptable downtime (e.g., 1 hour for customer-facing website, 4 hours for internal tool)
- **RPO:** Maximum acceptable data loss measured in time (e.g., 5 minutes for transaction DB, 24 hours for analytics)

**2025 Best Practices:**
1. Risk assessment and Business Impact Analysis (BIA)
2. Define RTO/RPO for each system
3. Comprehensive backup strategies (3-2-1 rule)
4. Regular testing and drills
5. Multi-layered security to prevent disasters
6. Expand beyond IT (supply chain, logistics, energy)

**Sources:**
- techprosecurity.com
- fusionrm.com
- wanclouds.net
- dev.to

#### Query 2: Database Backup Strategies PostgreSQL MySQL 2025

**Key Findings:**

**General Best Practices:**
- Regular automated backups aligned with RPO
- Test backups regularly
- Monitor backup jobs for success/failure
- Encrypt backups for sensitive data
- Implement 3-2-1 rule
- Document recovery procedures
- Define RPO and RTO before choosing strategy

**MySQL Backup Strategies:**
- **Logical Backups:** `mysqldump` exports SQL statements, `mydumper` for parallel dumps
- **Physical Backups:** MySQL Enterprise Backup, Percona XtraBackup for hot backups
- **Incremental Backups:** Binary logs for PITR, capture only changes
- **Point-in-Time Recovery:** Combine full backups with binary log archiving
- **Cloud-Native Solutions:** AWS RDS automated backups, Azure Database for MySQL

**PostgreSQL Backup Strategies:**
- **Full Backups:** `pg_basebackup` for complete cluster backup
- **Incremental Backups:** Only changes since last backup
- **Continuous Archiving:** WAL archiving for real-time recovery
- **Logical Backups:** `pg_dump` for database export to SQL
- **Tools:** pgBackRest (physical + WAL), WAL-G (cloud-first), Barman (central backup server)
- **PITR:** Combine base backup with WAL files for recovery to any point in time

**Zero-Downtime Strategies:**
- Replication for near-real-time copies
- Snapshot-based backups (storage-level)
- Online backups without locking

**Sources:**
- instaclustr.com
- percona.com
- scalegrid.io
- sqlflash.ai

#### Query 3: Kubernetes Disaster Recovery Velero Backup Patterns

**Key Findings:**

**Velero Overview:**
- Open-source tool for backing up/restoring Kubernetes cluster resources and persistent volumes
- Enables disaster recovery, cluster migration, data protection

**Basic DR Pattern:**
1. Regular scheduled backups (daily or more frequent based on criticality)
2. Retention policies to manage storage costs (default 30 days)
3. Read-only backup storage before restore
4. Restore from latest backup
5. Revert to read-write mode after restore

**Best Practices:**
- Verify backups through testing
- Store backups in different region/cloud provider
- Use clear namespace conventions and labels
- Set up alerts for failed backups (Prometheus metrics)
- Configure resource limits for Velero pod
- Include persistent volumes for stateful apps
- Consistent snapshots for both stateful and stateless apps

**Selective Backups:**
- Filter by namespace, resource type, labels
- Include/exclude specific resources
- Cluster-wide resource backups

**Velero Components:**
- Velero Server (deployment in cluster)
- Velero CLI (trigger operations)

**Benefits:**
- Disaster recovery to known good state
- Cluster migration with minimal downtime
- Compliance for data retention
- Isolated environments for testing

**Sources:**
- devtron.ai
- amazon.com (AWS EKS)
- velero.io
- medium.com

#### Query 4: Cross-Region Replication AWS GCP Azure Patterns

**Key Findings:**

**AWS:**
- S3 Cross-Region Replication (CRR) for automatic object replication
- Availability Zones for in-region geo-redundancy
- RDS Multi-AZ for automatic failover
- Aurora Global Database for cross-region reads

**Azure:**
- Geo-Redundant Storage (GRS) replicates to secondary region hundreds of miles away
- Read-Access GRS (RA-GRS) provides read access to secondary
- Azure Site Recovery for VM/workload replication
- Paired regions for compliance and DR

**GCP:**
- Multi-Regional Storage replicates across 2+ locations 100+ miles apart
- Global Load Balancing for traffic distribution
- Cloud SQL HA configuration
- Regional and multi-regional options

**Replication Patterns:**
- **Active-Passive:** One active region, standby passive region for failover
- **Active-Active:** Both regions active, serving traffic simultaneously
- **Pilot Light:** Minimal version in secondary region (low cost, slower failover)
- **Warm Standby:** Scaled-down version in secondary (faster failover, higher cost)

**General Considerations:**
- Choose regions close to users for low latency
- Consider data residency compliance requirements
- Evaluate costs vs benefits
- Regularly test failover procedures

**Sources:**
- msp360.com
- hokstadconsulting.com
- cloudoptimo.com
- awsstatic.com

#### Query 5: Chaos Engineering Disaster Recovery Testing 2025

**Key Findings:**

**Why Chaos Engineering Matters:**
- Rising system complexity (cloud-native, microservices, hybrid)
- Cost of downtime (financial losses, customer trust)
- AI-powered resilience (ML predicts failure points)
- Self-healing architectures (automatic detection and resolution)
- Business-driven reliability (executive-level priority)

**Chaos Engineering for DR:**
- Controlled experiments to reveal hidden failure modes
- Validates RTO/RPO achievability
- Tests runbook procedures effectiveness
- Builds confidence in automation
- Identifies brittle dependencies
- Improves monitoring and incident response

**Implementation Approach:**
1. Start small in staging with blast radius controls
2. Progress to selective production testing (low-risk periods)
3. Use tools: Chaos Mesh, Gremlin, Netflix Chaos Monkey
4. Orchestrate failover tests for stateful services
5. Automate DR drills in CI/CD pipelines

**Failure Injection Techniques:**
- Shut down servers/containers
- Introduce network latency/partitions
- Terminate database connections
- Fill disks
- Corrupt data
- Simulate region failures

**Sources:**
- medium.com
- moss.sh
- gigantics.io
- conf42.com

### Context7 Library Research Results

#### Velero (/vmware-tanzu/velero)

**Trust Score:** High (VMware Tanzu official)
**Code Snippets:** 8,004+
**Source Reputation:** High

**Key Capabilities:**
- Backup/restore Kubernetes cluster resources
- Persistent volume snapshots
- Schedule-based automated backups
- Selective backups (namespace, labels, resource types)
- Cross-cluster migration
- Disaster recovery workflows

**Example Usage:**
```bash
# Create backup schedule (daily at 7 AM)
velero schedule create daily-backup --schedule "0 7 * * *"

# Restore from backup
velero restore create --from-backup daily-backup-20251203070000
```

#### Restic (/restic/restic)

**Trust Score:** High
**Code Snippets:** 284+
**Source Reputation:** High

**Key Capabilities:**
- Fast, efficient, secure backup program
- Multiple OS support (Linux, macOS, Windows, BSD)
- Multiple backend storage (S3, Azure, GCS, SFTP, local)
- Encryption by default
- Deduplication
- Incremental backups
- Mount backups as FUSE filesystem

**Example Usage:**
```bash
# Initialize repository
restic init --repo /backup/location

# Create backup
restic backup ~/data --repo /backup/location

# Restore specific snapshot
restic restore abc123 --target /restore/location --repo /backup/location
```

#### pgBackRest (/pgbackrest/pgbackrest)

**Trust Score:** High
**Code Snippets:** 88+
**Benchmark Score:** 66.5
**Source Reputation:** High

**Key Capabilities:**
- Reliable PostgreSQL backup and restore
- Full, incremental, differential backups
- Point-in-Time Recovery (PITR)
- Parallel processing for speed
- Multiple repository support (local, S3, Azure, GCS)
- Encryption and compression
- Delta restore for efficiency
- Block-level incremental backups

**Example Configuration:**
```ini
[global]
repo1-type=s3
repo1-s3-bucket=my-backups
repo1-retention-full=2
repo1-cipher-type=aes-256-cbc
process-max=4
compress-type=lz4

[main]
pg1-path=/var/lib/postgresql/14/main
archive-async=y
backup-standby=y
```

#### WAL-G (/wal-g/wal-g)

**Trust Score:** Medium
**Code Snippets:** 246+
**Benchmark Score:** 81.8
**Source Reputation:** Medium

**Key Capabilities:**
- Fast archival and restoration for PostgreSQL, MySQL, MongoDB
- Cloud-first design (S3, GCS, Azure)
- Delta backups for efficiency
- Parallel uploads/downloads
- Encryption support
- Compression (zstd, lz4)
- PITR for all supported databases
- MySQL binlog archiving and replay
- Catchup backups for replication

**Example Usage:**
```bash
# PostgreSQL backup push
export WALG_S3_PREFIX=s3://my-backups/postgres
export WALG_COMPRESSION_METHOD=zstd
wal-g backup-push

# PostgreSQL restore
wal-g backup-fetch /var/lib/postgresql/14/main LATEST

# MySQL backup with xtrabackup
export WALG_STREAM_CREATE_COMMAND="xtrabackup --backup --stream=xbstream"
wal-g backup-push
```

### Research Summary

**2025 DR Landscape:**
1. **Automation is Essential:** Manual DR processes are error-prone and slow
2. **Multi-Cloud is Standard:** DR strategies must span cloud providers
3. **Testing is Non-Negotiable:** Untested backups are not backups
4. **Encryption Everywhere:** Ransomware requires immutable, encrypted backups
5. **Kubernetes is Complex:** Specialized tools (Velero) required for cloud-native DR
6. **PITR is Expected:** Databases need point-in-time recovery, not just full backups
7. **Chaos Engineering Validates:** DR plans must be tested under failure conditions

---

## DR Strategy Taxonomy

### Tier 1: Backup Types

#### 1.1 Full Backup

**Definition:** Complete copy of all data at a point in time

**Characteristics:**
- Largest storage requirement
- Slowest to create
- Fastest to restore (single restore operation)
- Independent (no dependency on other backups)

**Use Cases:**
- Weekly/monthly baseline backups
- Long-term archival
- Compliance retention
- Disaster recovery foundation

**Example (PostgreSQL):**
```bash
# pgBackRest full backup
pgbackrest --stanza=main --type=full backup

# WAL-G full backup
wal-g backup-push --full
```

#### 1.2 Incremental Backup

**Definition:** Only data changed since last backup (full or incremental)

**Characteristics:**
- Smallest storage requirement
- Fastest to create
- Slower to restore (requires full + all incrementals)
- Chain dependency (need all incrementals in sequence)

**Use Cases:**
- Frequent backups (hourly/daily)
- Low RPO requirements
- Storage-constrained environments
- Cost-sensitive scenarios

**Example (MySQL):**
```bash
# Percona XtraBackup incremental
xtrabackup --backup --incremental-basedir=/backup/base --target-dir=/backup/incr1

# WAL-G delta backup
export WALG_DELTA_MAX_STEPS=5
wal-g backup-push
```

#### 1.3 Differential Backup

**Definition:** Data changed since last full backup

**Characteristics:**
- Medium storage requirement
- Medium creation time
- Faster restore than incremental (full + latest differential)
- Simpler dependency (only need full + one differential)

**Use Cases:**
- Daily backups with weekly full
- Balance between storage and restore speed
- Simplified restore procedures

**Example (PostgreSQL):**
```bash
# pgBackRest differential backup
pgbackrest --stanza=main --type=diff backup
```

#### 1.4 Continuous Backup

**Definition:** Real-time or near-real-time backup of changes

**Characteristics:**
- Minimal data loss (lowest RPO, often seconds)
- Most complex to manage
- Highest resource requirements
- Enables point-in-time recovery

**Use Cases:**
- Mission-critical databases
- Financial transactions
- Regulatory compliance
- Zero data loss tolerance

**Example (PostgreSQL WAL Archiving):**
```postgresql
-- Enable continuous archiving
ALTER SYSTEM SET wal_level = 'replica';
ALTER SYSTEM SET archive_mode = 'on';
ALTER SYSTEM SET archive_command = 'pgbackrest --stanza=main archive-push %p';
SELECT pg_reload_conf();
```

### Tier 2: Backup Scope

#### 2.1 Logical Backup

**Definition:** Export data in logical format (SQL, JSON, etc.)

**Pros:**
- Human-readable
- Database-independent restore
- Selective restore (tables, schemas)
- Version-independent

**Cons:**
- Slower than physical backups
- Larger backup size
- Resource-intensive restore

**Tools:**
- PostgreSQL: `pg_dump`, `pg_dumpall`
- MySQL: `mysqldump`, `mydumper`
- MongoDB: `mongodump`

**Example:**
```bash
# PostgreSQL logical backup
pg_dump -h localhost -U postgres -d mydb -F c -f mydb.dump

# MySQL logical backup
mysqldump --all-databases --single-transaction --events --routines > backup.sql
```

#### 2.2 Physical Backup

**Definition:** Copy of database files at filesystem level

**Pros:**
- Fastest backup and restore
- Smallest backup size (with compression)
- Consistent point-in-time snapshot

**Cons:**
- Version-specific
- Platform-specific
- Requires downtime or hot backup tools

**Tools:**
- PostgreSQL: `pg_basebackup`, pgBackRest, WAL-G
- MySQL: Percona XtraBackup, MySQL Enterprise Backup
- Filesystem: LVM snapshots, ZFS snapshots

**Example:**
```bash
# PostgreSQL physical backup
pg_basebackup -h localhost -U postgres -D /backup/base -Ft -z -P

# MySQL physical backup (Percona XtraBackup)
xtrabackup --backup --target-dir=/backup/base
```

### Tier 3: Backup Location

#### 3.1 On-Site Backup

**Characteristics:**
- Fast backup and restore
- Lower costs
- Full control
- Vulnerable to site-level disasters

**Use Cases:**
- Operational recovery (accidental deletion)
- Rapid restore requirements
- Sensitive data (compliance restrictions)

#### 3.2 Off-Site Backup

**Characteristics:**
- Protected from site-level disasters
- Higher transfer costs
- Network-dependent speed
- Geographic distribution

**Use Cases:**
- Disaster recovery
- Compliance requirements
- Ransomware protection

#### 3.3 Cloud Backup

**Characteristics:**
- Scalable storage
- Geographic redundancy
- Pay-as-you-go pricing
- Managed services available

**Providers:**
- AWS: S3, S3 Glacier, RDS automated backups
- GCP: Cloud Storage, Cloud SQL backups
- Azure: Blob Storage, Azure Backup

**Example (S3 lifecycle):**
```bash
# S3 lifecycle policy for cost optimization
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-backups \
  --lifecycle-configuration '{
    "Rules": [
      {
        "Id": "archive-old-backups",
        "Status": "Enabled",
        "Transitions": [
          {"Days": 30, "StorageClass": "STANDARD_IA"},
          {"Days": 90, "StorageClass": "GLACIER"},
          {"Days": 365, "StorageClass": "DEEP_ARCHIVE"}
        ],
        "Expiration": {"Days": 2555}
      }
    ]
  }'
```

---

## Decision Frameworks

### Framework 1: RTO/RPO to DR Strategy Mapping

```
RTO/RPO Requirements → Backup Strategy

┌─────────────────────────────────────────────────────────────┐
│ RTO: < 1 hour, RPO: < 5 minutes                             │
│ Strategy: Active-Active, Continuous Replication, PITR       │
│ Tools: Aurora Global DB, GCS Multi-Region, Azure Site Rec   │
│ Cost: $$$$$ (Highest)                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ RTO: 1-4 hours, RPO: 15-60 minutes                         │
│ Strategy: Warm Standby, Incremental + WAL, Automated Fail  │
│ Tools: pgBackRest PITR, WAL-G, RDS Multi-AZ               │
│ Cost: $$$$ (High)                                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ RTO: 4-24 hours, RPO: 1-6 hours                            │
│ Strategy: Daily Full + Incremental, Cross-Region Backup    │
│ Tools: pgBackRest, Restic, Velero                          │
│ Cost: $$$ (Medium)                                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ RTO: > 24 hours, RPO: > 6 hours                            │
│ Strategy: Weekly Full + Daily Incremental, Single Region   │
│ Tools: pg_dump, mysqldump, S3 versioning                   │
│ Cost: $$ (Low)                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ RTO: > 1 week, RPO: > 24 hours                             │
│ Strategy: Weekly/Monthly Full, Archival                     │
│ Tools: tar + S3 Glacier, Azure Archive                     │
│ Cost: $ (Minimal)                                           │
└─────────────────────────────────────────────────────────────┘
```

### Framework 2: Backup Strategy Selection

```
START: What are you backing up?

├─► DATABASE
│   ├─► Size?
│   │   ├─► < 100GB → Logical backups (pg_dump, mysqldump)
│   │   └─► > 100GB → Physical backups (pgBackRest, XtraBackup)
│   ├─► RPO?
│   │   ├─► < 5 min → Continuous archiving (WAL, binlog)
│   │   └─► > 5 min → Incremental backups
│   └─► Load?
│       ├─► High → Backup from replica/standby
│       └─► Low → Backup from primary
│
├─► KUBERNETES CLUSTER
│   ├─► Stateful apps?
│   │   ├─► YES → Velero + PV snapshots
│   │   └─► NO → Velero (resources only)
│   ├─► Multi-cluster?
│   │   ├─► YES → Cross-cluster backups
│   │   └─► NO → Single cluster backups
│   └─► Namespace isolation?
│       ├─► YES → Per-namespace schedules
│       └─► NO → Cluster-wide backup
│
├─► FILES/OBJECTS
│   ├─► Change frequency?
│   │   ├─► High → Incremental (restic, duplicity)
│   │   └─► Low → Full snapshots (tar, rsync)
│   ├─► Size?
│   │   ├─► < 1TB → Daily full backups
│   │   └─► > 1TB → Weekly full + daily incremental
│   └─► Retention?
│       ├─► > 7 years → S3 Glacier Deep Archive
│       └─► < 7 years → S3 Standard-IA
│
└─► VIRTUAL MACHINES
    ├─► Hypervisor?
    │   ├─► VMware → Veeam, Nakivo
    │   ├─► Hyper-V → Azure Backup
    │   └─► KVM → Proxmox Backup Server
    └─► Cloud?
        ├─► AWS → EBS snapshots, AMI
        ├─► GCP → Persistent disk snapshots
        └─► Azure → VM backup, Site Recovery
```

### Framework 3: Multi-Cloud Backup Storage

| Scenario | Primary Storage | Secondary Storage | Tertiary Storage |
|----------|----------------|-------------------|------------------|
| **AWS-Native** | S3 Standard | S3 Standard-IA (30d) | S3 Glacier (90d) |
| **GCP-Native** | Cloud Storage Standard | Nearline (30d) | Coldline/Archive (90d) |
| **Azure-Native** | Blob Storage (Hot) | Cool tier (30d) | Archive tier (90d) |
| **Multi-Cloud** | Primary cloud (S3/GCS) | Secondary cloud (Azure) | Third cloud or on-prem |
| **Hybrid** | On-prem NAS | Cloud (S3/Azure) | Second cloud or tape |
| **Compliance** | Production cloud | Different region | Air-gapped on-prem |

### Framework 4: Testing Frequency by Criticality

| System Criticality | Backup Frequency | Test Restore Frequency | DR Drill Frequency |
|-------------------|------------------|------------------------|-------------------|
| **Tier 0: Mission-Critical** | Continuous (WAL/binlog) | Weekly | Monthly |
| **Tier 1: Production** | Hourly incremental, Daily full | Bi-weekly | Quarterly |
| **Tier 2: Important** | Daily incremental, Weekly full | Monthly | Semi-annually |
| **Tier 3: Standard** | Daily | Quarterly | Annually |
| **Tier 4: Low-Priority** | Weekly | Semi-annually | As needed |

---

## Database Backup Patterns

### PostgreSQL Backup Patterns

#### Pattern 1: Production-Grade PITR with pgBackRest

**Use Case:** Mission-critical PostgreSQL with < 5 min RPO

**Architecture:**
```
PostgreSQL Primary
    ├─► WAL Archive (continuous) → S3/GCS/Azure
    ├─► Full Backup (weekly) → S3/GCS/Azure
    ├─► Differential Backup (daily) → S3/GCS/Azure
    └─► Incremental Backup (hourly) → S3/GCS/Azure

Standby Replica (optional)
    └─► Backup from standby (zero impact on primary)
```

**Configuration:**

```ini
# /etc/pgbackrest/pgbackrest.conf

[global]
# Repository configuration
repo1-type=s3
repo1-s3-bucket=my-pg-backups
repo1-s3-region=us-east-1
repo1-s3-key=YOUR_ACCESS_KEY
repo1-s3-key-secret=YOUR_SECRET_KEY
repo1-path=/pgbackrest

# Retention policies
repo1-retention-full=2          # Keep 2 full backups
repo1-retention-diff=6          # Keep 6 differential backups
repo1-retention-archive=4       # Keep 4 sets of WAL archives

# Encryption
repo1-cipher-type=aes-256-cbc
repo1-cipher-pass=YOUR_CIPHER_PASSPHRASE

# Performance
process-max=4
compress-type=lz4
compress-level=3

# Logging
log-level-console=info
log-level-file=debug

[main]
# PostgreSQL configuration
pg1-path=/var/lib/postgresql/14/main
pg1-port=5432
pg1-socket-path=/var/run/postgresql

# Backup from standby (if available)
backup-standby=y

# Archive settings
archive-async=y
archive-push-queue-max=128MB

# Backup settings
start-fast=y
stop-auto=y
```

**PostgreSQL Configuration:**

```sql
-- Enable WAL archiving
ALTER SYSTEM SET wal_level = 'replica';
ALTER SYSTEM SET archive_mode = 'on';
ALTER SYSTEM SET archive_command = 'pgbackrest --stanza=main archive-push %p';
ALTER SYSTEM SET archive_timeout = 60;  -- Archive WAL every 60 seconds
ALTER SYSTEM SET max_wal_senders = 3;
ALTER SYSTEM SET wal_keep_size = '1GB';

SELECT pg_reload_conf();
```

**Backup Schedule (cron):**

```bash
# /etc/cron.d/pgbackrest

# Full backup every Sunday at 2 AM
0 2 * * 0 postgres pgbackrest --stanza=main --type=full backup

# Differential backup every day at 2 AM (except Sunday)
0 2 * * 1-6 postgres pgbackrest --stanza=main --type=diff backup

# Check configuration daily
30 3 * * * postgres pgbackrest --stanza=main check

# Monitor backup status
0 * * * * postgres pgbackrest --stanza=main info --output=json > /var/log/pgbackrest/status.json
```

**Restore Procedure:**

```bash
# 1. Stop PostgreSQL
sudo systemctl stop postgresql

# 2. Restore from latest backup
sudo -u postgres pgbackrest --stanza=main --delta restore

# 3. Configure recovery (PostgreSQL 12+)
sudo -u postgres tee $PGDATA/postgresql.auto.conf > /dev/null <<EOF
restore_command = 'pgbackrest --stanza=main archive-get %f %p'
recovery_target_time = '2025-12-03 14:30:00'  # Optional: PITR to specific time
EOF

# 4. Create recovery signal file
sudo -u postgres touch $PGDATA/recovery.signal

# 5. Start PostgreSQL
sudo systemctl start postgresql

# 6. Monitor recovery
sudo -u postgres tail -f /var/log/postgresql/postgresql-14-main.log

# 7. Verify recovery completed
sudo -u postgres psql -c "SELECT pg_is_in_recovery();"  # Should return 'f'
```

#### Pattern 2: Cloud-First PostgreSQL DR with WAL-G

**Use Case:** Cloud-native PostgreSQL with S3/GCS/Azure backends

**Configuration:**

```bash
# Environment variables (add to /etc/environment or systemd service)
export WALG_S3_PREFIX=s3://my-pg-backups/prod
export WALG_COMPRESSION_METHOD=zstd
export WALG_UPLOAD_CONCURRENCY=16
export WALG_DOWNLOAD_CONCURRENCY=16
export WALG_DELTA_MAX_STEPS=5
export WALG_DELTA_ORIGIN=LATEST
export PGHOST=/var/run/postgresql
export PGUSER=postgres

# Encryption
export WALG_LIBSODIUM_KEY=$(openssl rand -hex 32)
export WALG_LIBSODIUM_KEY_TRANSFORM=hex
```

**PostgreSQL Configuration:**

```sql
-- WAL archiving with WAL-G
ALTER SYSTEM SET wal_level = 'replica';
ALTER SYSTEM SET archive_mode = 'on';
ALTER SYSTEM SET archive_command = 'wal-g wal-push %p';
ALTER SYSTEM SET archive_timeout = 60;
ALTER SYSTEM SET restore_command = 'wal-g wal-fetch %f %p';

SELECT pg_reload_conf();
```

**Backup Script:**

```bash
#!/bin/bash
# /usr/local/bin/walg-backup.sh

set -euo pipefail

# Metadata for this backup
export WALG_SENTINEL_USER_DATA=$(cat <<EOF
{
  "env": "production",
  "region": "us-east-1",
  "version": "$(psql -t -c 'SELECT version()' | head -n1)",
  "backup_time": "$(date -Iseconds)"
}
EOF
)

# Perform backup
echo "Starting WAL-G backup at $(date)"
wal-g backup-push

# List recent backups
echo "Recent backups:"
wal-g backup-list --json | jq -r '.[] | "\(.backup_name) - \(.time) - \(.data_size)"'

echo "Backup completed at $(date)"
```

**Restore Script:**

```bash
#!/bin/bash
# /usr/local/bin/walg-restore.sh

set -euo pipefail

RESTORE_TARGET="${1:-LATEST}"
RESTORE_PATH="${2:-/var/lib/postgresql/14/restore}"

# Stop PostgreSQL if running
systemctl stop postgresql || true

# Clean restore directory
rm -rf "$RESTORE_PATH"
mkdir -p "$RESTORE_PATH"
chown postgres:postgres "$RESTORE_PATH"

# Fetch backup
echo "Fetching backup: $RESTORE_TARGET"
sudo -u postgres wal-g backup-fetch "$RESTORE_PATH" "$RESTORE_TARGET"

# Configure recovery
cat > "$RESTORE_PATH/postgresql.auto.conf" <<EOF
restore_command = 'wal-g wal-fetch %f %p'
EOF

# Create recovery signal
sudo -u postgres touch "$RESTORE_PATH/recovery.signal"

echo "Restore completed. Start PostgreSQL with:"
echo "  pg_ctl -D $RESTORE_PATH start"
```

### MySQL Backup Patterns

#### Pattern 3: MySQL PITR with Percona XtraBackup

**Use Case:** MySQL production with hot backups and PITR

**Full Backup Script:**

```bash
#!/bin/bash
# /usr/local/bin/mysql-full-backup.sh

set -euo pipefail

BACKUP_DIR="/backups/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
FULL_BACKUP_DIR="$BACKUP_DIR/full/$DATE"

# Create backup directory
mkdir -p "$FULL_BACKUP_DIR"

# Perform full backup
xtrabackup --backup \
  --target-dir="$FULL_BACKUP_DIR" \
  --parallel=4 \
  --compress \
  --compress-threads=4

# Store backup metadata
echo "Backup completed at $(date)" > "$FULL_BACKUP_DIR/backup.info"
echo "GTID: $(cat $FULL_BACKUP_DIR/xtrabackup_binlog_info | awk '{print $3}')" >> "$FULL_BACKUP_DIR/backup.info"

# Upload to S3
aws s3 sync "$FULL_BACKUP_DIR" "s3://my-mysql-backups/full/$DATE/" --storage-class STANDARD_IA

echo "Full backup completed: $FULL_BACKUP_DIR"
```

**Incremental Backup Script:**

```bash
#!/bin/bash
# /usr/local/bin/mysql-incr-backup.sh

set -euo pipefail

BACKUP_DIR="/backups/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
LATEST_FULL=$(ls -td $BACKUP_DIR/full/* | head -n1)
INCR_BACKUP_DIR="$BACKUP_DIR/incremental/$DATE"

# Create incremental backup
mkdir -p "$INCR_BACKUP_DIR"

xtrabackup --backup \
  --target-dir="$INCR_BACKUP_DIR" \
  --incremental-basedir="$LATEST_FULL" \
  --parallel=4 \
  --compress \
  --compress-threads=4

# Upload to S3
aws s3 sync "$INCR_BACKUP_DIR" "s3://my-mysql-backups/incremental/$DATE/"

echo "Incremental backup completed: $INCR_BACKUP_DIR"
```

**Restore Script:**

```bash
#!/bin/bash
# /usr/local/bin/mysql-restore.sh

set -euo pipefail

RESTORE_TARGET="${1:-}"
MYSQL_DATADIR="/var/lib/mysql"

if [ -z "$RESTORE_TARGET" ]; then
  echo "Usage: $0 <backup_timestamp>"
  echo "Available backups:"
  ls -1 /backups/mysql/full/
  exit 1
fi

# Stop MySQL
systemctl stop mysql

# Backup existing data
mv "$MYSQL_DATADIR" "${MYSQL_DATADIR}.old.$(date +%s)"
mkdir -p "$MYSQL_DATADIR"

# Decompress and prepare full backup
FULL_BACKUP="/backups/mysql/full/$RESTORE_TARGET"
xtrabackup --decompress --target-dir="$FULL_BACKUP"
xtrabackup --prepare --apply-log-only --target-dir="$FULL_BACKUP"

# Apply incremental backups (if any)
for INCR in $(ls -td /backups/mysql/incremental/* | tac); do
  if [ "$INCR" -nt "$FULL_BACKUP" ]; then
    echo "Applying incremental backup: $INCR"
    xtrabackup --decompress --target-dir="$INCR"
    xtrabackup --prepare --apply-log-only --target-dir="$FULL_BACKUP" --incremental-dir="$INCR"
  fi
done

# Final prepare
xtrabackup --prepare --target-dir="$FULL_BACKUP"

# Copy back to datadir
xtrabackup --copy-back --target-dir="$FULL_BACKUP"

# Fix permissions
chown -R mysql:mysql "$MYSQL_DATADIR"

# Reset GTID (if needed)
GTID=$(cat "$FULL_BACKUP/xtrabackup_binlog_info" | awk '{print $3}')
echo "SET @@GLOBAL.GTID_PURGED='$GTID';" > /tmp/reset_gtid.sql

# Start MySQL
systemctl start mysql

# Apply GTID reset
mysql < /tmp/reset_gtid.sql

echo "Restore completed successfully"
```

#### Pattern 4: MySQL Backup with WAL-G

**Configuration:**

```bash
# Environment setup
export WALG_S3_PREFIX=s3://my-mysql-backups/prod
export WALG_MYSQL_DATASOURCE_NAME="root:password@tcp(localhost:3306)/mysql"
export WALG_COMPRESSION_METHOD=zstd
export WALG_UPLOAD_CONCURRENCY=8

# For xtrabackup-based backups
export WALG_STREAM_CREATE_COMMAND="xtrabackup --backup --stream=xbstream --datadir=/var/lib/mysql"
export WALG_STREAM_RESTORE_COMMAND="xbstream -x -C /var/lib/mysql"
export WALG_MYSQL_BACKUP_PREPARE_COMMAND="xtrabackup --prepare --target-dir=/var/lib/mysql"
export WALG_MYSQL_BINLOG_REPLAY_COMMAND='mysqlbinlog --stop-datetime="$WALG_MYSQL_BINLOG_END_TS" "$WALG_MYSQL_CURRENT_BINLOG" | mysql'

# For logical backups (alternative)
# export WALG_STREAM_CREATE_COMMAND="mysqldump --all-databases --single-transaction --events --routines"
# export WALG_STREAM_RESTORE_COMMAND="mysql"
```

**Backup:**

```bash
# Stream-based backup
wal-g backup-push

# Push binary logs (for PITR)
wal-g binlog-push
```

**Restore:**

```bash
# Fetch backup
wal-g backup-fetch /var/lib/mysql LATEST

# Replay binlogs to specific time
wal-g binlog-replay --since "backup_name" --until "2025-12-03T14:30:00Z"
```

### MongoDB Backup Patterns

#### Pattern 5: MongoDB Atlas-Style Backup

**Use Case:** MongoDB with continuous backup and PITR

**Backup Script (mongodump):**

```bash
#!/bin/bash
# /usr/local/bin/mongodb-backup.sh

set -euo pipefail

BACKUP_DIR="/backups/mongodb"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="$BACKUP_DIR/$DATE"

# Create backup
mongodump \
  --uri="mongodb://localhost:27017" \
  --out="$BACKUP_PATH" \
  --gzip \
  --numParallelCollections=4

# Upload to S3
aws s3 sync "$BACKUP_PATH" "s3://my-mongo-backups/$DATE/" \
  --storage-class STANDARD_IA

# Cleanup old backups (keep last 7 days locally)
find "$BACKUP_DIR" -type d -mtime +7 -exec rm -rf {} +

echo "Backup completed: $BACKUP_PATH"
```

**Restore Script:**

```bash
#!/bin/bash
# /usr/local/bin/mongodb-restore.sh

set -euo pipefail

BACKUP_DATE="${1:-}"

if [ -z "$BACKUP_DATE" ]; then
  echo "Usage: $0 <backup_date>"
  exit 1
fi

RESTORE_PATH="/backups/mongodb/$BACKUP_DATE"

# Download from S3 if not local
if [ ! -d "$RESTORE_PATH" ]; then
  aws s3 sync "s3://my-mongo-backups/$BACKUP_DATE/" "$RESTORE_PATH"
fi

# Restore
mongorestore \
  --uri="mongodb://localhost:27017" \
  --gzip \
  --numParallelCollections=4 \
  --drop \
  "$RESTORE_PATH"

echo "Restore completed from: $RESTORE_PATH"
```

---

## Kubernetes DR Patterns

### Pattern 1: Velero with Scheduled Backups

**Use Case:** Kubernetes cluster backup with persistent volumes

**Installation:**

```bash
# Install Velero CLI
wget https://github.com/vmware-tanzu/velero/releases/latest/download/velero-linux-amd64.tar.gz
tar -xvf velero-linux-amd64.tar.gz
sudo mv velero-linux-amd64/velero /usr/local/bin/

# Install Velero on cluster (AWS example)
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.9.0 \
  --bucket my-velero-backups \
  --backup-location-config region=us-east-1 \
  --snapshot-location-config region=us-east-1 \
  --secret-file ./credentials-velero
```

**Backup Schedules:**

```yaml
# daily-full-backup.yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-full-backup
  namespace: velero
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  template:
    ttl: 720h  # 30 days retention
    includedNamespaces:
      - '*'
    includeClusterResources: true
    snapshotVolumes: true
    storageLocation: default
```

```yaml
# hourly-app-backup.yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: hourly-app-backup
  namespace: velero
spec:
  schedule: "0 * * * *"  # Every hour
  template:
    ttl: 168h  # 7 days retention
    includedNamespaces:
      - production
      - staging
    labelSelector:
      matchLabels:
        backup: enabled
    snapshotVolumes: true
```

**Apply Schedules:**

```bash
kubectl apply -f daily-full-backup.yaml
kubectl apply -f hourly-app-backup.yaml

# Verify schedules
velero schedule get

# View backups
velero backup get
```

**Selective Backup Examples:**

```bash
# Backup specific namespace
velero backup create nginx-backup --include-namespaces nginx

# Backup with label selector
velero backup create app-backup \
  --selector app=super-important

# Backup specific resources
velero backup create pvc-backup \
  --include-resources persistentvolumeclaims,persistentvolumes

# Exclude resources
velero backup create no-secrets-backup \
  --exclude-resources secrets
```

**Restore Examples:**

```bash
# Restore from latest backup
velero restore create --from-backup daily-full-backup-20251203020000

# Restore to different namespace
velero restore create --from-backup nginx-backup \
  --namespace-mappings nginx:nginx-restored

# Restore specific resources
velero restore create --from-backup app-backup \
  --include-resources deployments,services

# Restore with different storage class
velero restore create --from-backup pvc-backup \
  --restore-volumes \
  --storage-class-mappings gp2:gp3
```

**Monitoring Velero:**

```yaml
# velero-monitoring.yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: velero
  namespace: velero
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: velero
  endpoints:
    - port: monitoring
      interval: 30s
```

**Prometheus Alerts:**

```yaml
# velero-alerts.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: velero-alerts
  namespace: velero
spec:
  groups:
    - name: velero
      interval: 30s
      rules:
        - alert: VeleroBackupFailed
          expr: velero_backup_failure_total > 0
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "Velero backup failed"
            description: "Backup {{ $labels.schedule }} failed"

        - alert: VeleroBackupPartiallyFailed
          expr: velero_backup_partial_failure_total > 0
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Velero backup partially failed"

        - alert: VeleroBackupTooOld
          expr: time() - velero_backup_last_successful_timestamp > 86400
          for: 1h
          labels:
            severity: warning
          annotations:
            summary: "Velero backup is more than 24 hours old"
```

### Pattern 2: Velero with Restic for File-Level Backup

**Use Case:** Kubernetes backup with Restic for persistent volumes (no snapshot support)

**Installation with Restic:**

```bash
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.9.0 \
  --bucket my-velero-backups \
  --backup-location-config region=us-east-1 \
  --use-node-agent \
  --uploader-type restic
```

**Opt-in Volumes for Restic Backup:**

```yaml
# app-with-restic-backup.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
spec:
  replicas: 3
  template:
    metadata:
      annotations:
        # Opt-in to Restic backup
        backup.velero.io/backup-volumes: data,logs
    spec:
      containers:
        - name: app
          image: myapp:latest
          volumeMounts:
            - name: data
              mountPath: /data
            - name: logs
              mountPath: /var/log
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: myapp-data
        - name: logs
          emptyDir: {}
```

**Backup with Restic:**

```bash
# Backup namespace with Restic
velero backup create myapp-restic \
  --include-namespaces production \
  --default-volumes-to-fs-backup

# Check Restic backup status
velero backup describe myapp-restic --details
```

### Pattern 3: etcd Backup for Cluster Recovery

**Use Case:** Disaster recovery for Kubernetes control plane

**etcd Backup Script:**

```bash
#!/bin/bash
# /usr/local/bin/etcd-backup.sh

set -euo pipefail

ETCD_ENDPOINTS="https://127.0.0.1:2379"
ETCD_CACERT="/etc/kubernetes/pki/etcd/ca.crt"
ETCD_CERT="/etc/kubernetes/pki/etcd/server.crt"
ETCD_KEY="/etc/kubernetes/pki/etcd/server.key"

BACKUP_DIR="/backups/etcd"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/etcd-snapshot-$DATE.db"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Snapshot etcd
ETCDCTL_API=3 etcdctl \
  --endpoints="$ETCD_ENDPOINTS" \
  --cacert="$ETCD_CACERT" \
  --cert="$ETCD_CERT" \
  --key="$ETCD_KEY" \
  snapshot save "$BACKUP_FILE"

# Verify snapshot
ETCDCTL_API=3 etcdctl \
  --write-out=table \
  snapshot status "$BACKUP_FILE"

# Upload to S3
aws s3 cp "$BACKUP_FILE" "s3://my-k8s-backups/etcd/$DATE/"

# Cleanup old backups (keep last 7 days)
find "$BACKUP_DIR" -type f -name "etcd-snapshot-*.db" -mtime +7 -delete

echo "etcd backup completed: $BACKUP_FILE"
```

**etcd Restore Procedure:**

```bash
#!/bin/bash
# /usr/local/bin/etcd-restore.sh

set -euo pipefail

SNAPSHOT_FILE="${1:-}"

if [ -z "$SNAPSHOT_FILE" ]; then
  echo "Usage: $0 <snapshot_file>"
  exit 1
fi

ETCD_DATA_DIR="/var/lib/etcd"
ETCD_NAME="etcd-master"
INITIAL_CLUSTER="etcd-master=https://10.0.1.10:2380"
INITIAL_ADVERTISE_PEER_URLS="https://10.0.1.10:2380"

# Stop etcd and kube-apiserver
systemctl stop etcd
systemctl stop kube-apiserver

# Backup existing data
mv "$ETCD_DATA_DIR" "${ETCD_DATA_DIR}.backup.$(date +%s)"

# Restore from snapshot
ETCDCTL_API=3 etcdctl snapshot restore "$SNAPSHOT_FILE" \
  --name="$ETCD_NAME" \
  --initial-cluster="$INITIAL_CLUSTER" \
  --initial-advertise-peer-urls="$INITIAL_ADVERTISE_PEER_URLS" \
  --data-dir="$ETCD_DATA_DIR"

# Fix permissions
chown -R etcd:etcd "$ETCD_DATA_DIR"

# Start services
systemctl start etcd
systemctl start kube-apiserver

echo "etcd restored from: $SNAPSHOT_FILE"
```

---

## Cloud-Specific DR Patterns

### AWS DR Patterns

#### Pattern 1: RDS Automated Backups with PITR

**Configuration:**

```hcl
# terraform/rds.tf
resource "aws_db_instance" "postgres" {
  identifier     = "prod-postgres"
  engine         = "postgres"
  engine_version = "14.7"
  instance_class = "db.r6g.xlarge"

  # Storage
  allocated_storage     = 100
  storage_type          = "gp3"
  storage_encrypted     = true
  kms_key_id            = aws_kms_key.rds.arn

  # Backup configuration
  backup_retention_period   = 30  # 30 days retention
  backup_window             = "03:00-04:00"  # UTC
  maintenance_window        = "sun:04:00-sun:05:00"
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  # PITR enabled automatically with backup_retention_period > 0
  copy_tags_to_snapshot = true

  # Multi-AZ for HA
  multi_az = true

  # Final snapshot on deletion
  final_snapshot_identifier = "prod-postgres-final-${formatdate("YYYYMMDD-hhmm", timestamp())}"
  skip_final_snapshot       = false

  tags = {
    Environment = "production"
    Backup      = "automated"
  }
}
```

**Restore to Point-in-Time:**

```bash
# Restore to specific time
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier prod-postgres \
  --target-db-instance-identifier prod-postgres-restored \
  --restore-time "2025-12-03T14:30:00Z" \
  --db-subnet-group-name prod-db-subnet \
  --publicly-accessible false

# Restore to latest restorable time
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier prod-postgres \
  --target-db-instance-identifier prod-postgres-restored \
  --use-latest-restorable-time \
  --db-subnet-group-name prod-db-subnet
```

#### Pattern 2: S3 Cross-Region Replication

**Configuration:**

```hcl
# Primary region (us-east-1)
resource "aws_s3_bucket" "primary" {
  provider = aws.us-east-1
  bucket   = "my-data-primary"

  tags = {
    Environment = "production"
    Replication = "source"
  }
}

resource "aws_s3_bucket_versioning" "primary" {
  provider = aws.us-east-1
  bucket   = aws_s3_bucket.primary.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_replication_configuration" "primary" {
  provider = aws.us-east-1
  bucket   = aws_s3_bucket.primary.id
  role     = aws_iam_role.replication.arn

  rule {
    id     = "replicate-all"
    status = "Enabled"

    filter {
      prefix = ""
    }

    destination {
      bucket        = aws_s3_bucket.replica.arn
      storage_class = "STANDARD_IA"

      # Replication Time Control (RTC) for 15-minute SLA
      replication_time {
        status = "Enabled"
        time {
          minutes = 15
        }
      }

      metrics {
        status = "Enabled"
        event_threshold {
          minutes = 15
        }
      }
    }

    delete_marker_replication {
      status = "Enabled"
    }
  }
}

# Replica region (us-west-2)
resource "aws_s3_bucket" "replica" {
  provider = aws.us-west-2
  bucket   = "my-data-replica"

  tags = {
    Environment = "production"
    Replication = "destination"
  }
}

resource "aws_s3_bucket_versioning" "replica" {
  provider = aws.us-west-2
  bucket   = aws_s3_bucket.replica.id

  versioning_configuration {
    status = "Enabled"
  }
}
```

#### Pattern 3: Aurora Global Database

**Configuration:**

```hcl
resource "aws_rds_global_cluster" "aurora_global" {
  global_cluster_identifier = "prod-aurora-global"
  engine                    = "aurora-postgresql"
  engine_version            = "14.7"
  database_name             = "myapp"
  storage_encrypted         = true
}

# Primary cluster (us-east-1)
resource "aws_rds_cluster" "primary" {
  provider                  = aws.us-east-1
  cluster_identifier        = "prod-aurora-primary"
  engine                    = aws_rds_global_cluster.aurora_global.engine
  engine_version            = aws_rds_global_cluster.aurora_global.engine_version
  global_cluster_identifier = aws_rds_global_cluster.aurora_global.id

  database_name   = "myapp"
  master_username = "admin"
  master_password = random_password.aurora.result

  backup_retention_period = 30
  preferred_backup_window = "03:00-04:00"

  enabled_cloudwatch_logs_exports = ["postgresql"]
}

resource "aws_rds_cluster_instance" "primary" {
  provider           = aws.us-east-1
  count              = 2
  identifier         = "prod-aurora-primary-${count.index}"
  cluster_identifier = aws_rds_cluster.primary.id
  instance_class     = "db.r6g.xlarge"
  engine             = aws_rds_cluster.primary.engine
  engine_version     = aws_rds_cluster.primary.engine_version
}

# Secondary cluster (eu-west-1)
resource "aws_rds_cluster" "secondary" {
  provider                  = aws.eu-west-1
  cluster_identifier        = "prod-aurora-secondary"
  engine                    = aws_rds_global_cluster.aurora_global.engine
  engine_version            = aws_rds_global_cluster.aurora_global.engine_version
  global_cluster_identifier = aws_rds_global_cluster.aurora_global.id

  # Secondary cluster is read-only
  depends_on = [aws_rds_cluster_instance.primary]
}

resource "aws_rds_cluster_instance" "secondary" {
  provider           = aws.eu-west-1
  count              = 2
  identifier         = "prod-aurora-secondary-${count.index}"
  cluster_identifier = aws_rds_cluster.secondary.id
  instance_class     = "db.r6g.xlarge"
  engine             = aws_rds_cluster.secondary.engine
  engine_version     = aws_rds_cluster.secondary.engine_version
}
```

**Failover to Secondary Region:**

```bash
# Promote secondary cluster to standalone
aws rds remove-from-global-cluster \
  --region eu-west-1 \
  --global-cluster-identifier prod-aurora-global \
  --db-cluster-identifier prod-aurora-secondary

# Update application to point to new primary (eu-west-1)
# Update DNS/load balancer endpoints
```

### GCP DR Patterns

#### Pattern 1: Cloud SQL Automated Backups

**Configuration:**

```hcl
resource "google_sql_database_instance" "postgres" {
  name             = "prod-postgres"
  database_version = "POSTGRES_14"
  region           = "us-central1"

  settings {
    tier = "db-custom-4-16384"  # 4 vCPU, 16GB RAM

    backup_configuration {
      enabled                        = true
      start_time                     = "03:00"
      point_in_time_recovery_enabled = true
      transaction_log_retention_days = 7
      backup_retention_settings {
        retained_backups = 30
        retention_unit   = "COUNT"
      }
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.private_network.id
    }

    database_flags {
      name  = "max_connections"
      value = "200"
    }
  }

  deletion_protection = true
}
```

**Restore from Backup:**

```bash
# List available backups
gcloud sql backups list --instance=prod-postgres

# Restore from specific backup
gcloud sql backups restore BACKUP_ID \
  --backup-instance=prod-postgres \
  --backup-id=BACKUP_ID

# Clone instance to point-in-time
gcloud sql instances clone prod-postgres prod-postgres-clone \
  --point-in-time='2025-12-03T14:30:00.000Z'
```

#### Pattern 2: GCS Multi-Regional Storage

**Configuration:**

```hcl
resource "google_storage_bucket" "backups" {
  name          = "my-backups-multi-region"
  location      = "US"  # Multi-region (us-east1, us-west1, us-central1)
  storage_class = "STANDARD"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"
    }
  }

  uniform_bucket_level_access = true
}
```

### Azure DR Patterns

#### Pattern 1: Azure Backup for VMs

**Configuration:**

```hcl
resource "azurerm_recovery_services_vault" "vault" {
  name                = "prod-recovery-vault"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "Standard"

  soft_delete_enabled = true
}

resource "azurerm_backup_policy_vm" "policy" {
  name                = "prod-vm-backup-policy"
  resource_group_name = azurerm_resource_group.main.name
  recovery_vault_name = azurerm_recovery_services_vault.vault.name

  timezone = "UTC"

  backup {
    frequency = "Daily"
    time      = "03:00"
  }

  retention_daily {
    count = 30
  }

  retention_weekly {
    count    = 12
    weekdays = ["Sunday"]
  }

  retention_monthly {
    count    = 12
    weekdays = ["Sunday"]
    weeks    = ["First"]
  }

  retention_yearly {
    count    = 7
    weekdays = ["Sunday"]
    weeks    = ["First"]
    months   = ["January"]
  }
}

resource "azurerm_backup_protected_vm" "vm" {
  resource_group_name = azurerm_resource_group.main.name
  recovery_vault_name = azurerm_recovery_services_vault.vault.name
  source_vm_id        = azurerm_virtual_machine.main.id
  backup_policy_id    = azurerm_backup_policy_vm.policy.id
}
```

#### Pattern 2: Azure Site Recovery

**Configuration:**

```hcl
# Primary region resources
resource "azurerm_site_recovery_fabric" "primary" {
  name                = "primary-fabric"
  resource_group_name = azurerm_resource_group.main.name
  recovery_vault_name = azurerm_recovery_services_vault.vault.name
  location            = "eastus"
}

# Secondary region resources
resource "azurerm_site_recovery_fabric" "secondary" {
  name                = "secondary-fabric"
  resource_group_name = azurerm_resource_group.main.name
  recovery_vault_name = azurerm_recovery_services_vault.vault.name
  location            = "westus"
}

resource "azurerm_site_recovery_replication_policy" "policy" {
  name                                                 = "replication-policy"
  resource_group_name                                  = azurerm_resource_group.main.name
  recovery_vault_name                                  = azurerm_recovery_services_vault.vault.name
  recovery_point_retention_in_minutes                  = 1440  # 24 hours
  application_consistent_snapshot_frequency_in_minutes = 240   # 4 hours
}
```

---

## Cross-Region Replication

### Active-Passive Pattern

**Use Case:** Primary region serves all traffic, secondary region on standby

**Architecture:**
```
Primary Region (Active)
    ├─► Application Servers
    ├─► Database (Read/Write)
    └─► Continuous Replication → Secondary Region (Passive)
                                       ├─► Application Servers (Stopped)
                                       └─► Database (Read-Only Replica)

Failover:
    1. Promote secondary database to read/write
    2. Start application servers in secondary
    3. Update DNS/load balancer to secondary
    4. RTO: 15-60 minutes, RPO: 5-15 minutes
```

**Implementation (PostgreSQL):**

```bash
# Primary region: Configure replication
# postgresql.conf
wal_level = replica
max_wal_senders = 5
wal_keep_size = '1GB'

# pg_hba.conf
host replication replicator secondary-ip/32 md5

# Create replication user
CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'password';

# Secondary region: Set up standby
pg_basebackup -h primary-ip -U replicator -D /var/lib/postgresql/14/main -P -R

# Failover script
#!/bin/bash
# Promote standby to primary
pg_ctl promote -D /var/lib/postgresql/14/main

# Update DNS (Route 53 example)
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "db.example.com",
        "Type": "CNAME",
        "TTL": 60,
        "ResourceRecords": [{"Value": "secondary-db.example.com"}]
      }
    }]
  }'
```

### Active-Active Pattern

**Use Case:** Both regions serve traffic simultaneously

**Architecture:**
```
Region 1 (Active)                   Region 2 (Active)
    ├─► Application Servers             ├─► Application Servers
    ├─► Database (Multi-Master)   ◄──►  ├─► Database (Multi-Master)
    └─► Bi-directional Replication      └─► Bi-directional Replication

Load Balancer (Global)
    ├─► Route users to nearest region
    └─► Failover automatically if one region down

RTO: < 1 minute (automatic), RPO: < 1 minute
```

**Implementation (Aurora Global Database):**

```hcl
# See Aurora Global Database configuration in AWS DR Patterns section above

# Application configuration
# Use read-write endpoint for writes: prod-aurora-primary.cluster-xxx.us-east-1.rds.amazonaws.com
# Use read-only endpoint for reads: prod-aurora-secondary.cluster-xxx.eu-west-1.rds.amazonaws.com
```

### Pilot Light Pattern

**Use Case:** Minimal resources in secondary region, fast scale-up on failover

**Architecture:**
```
Primary Region (Active)
    ├─► Full application stack
    └─► Continuous data replication → Secondary Region (Pilot Light)
                                           ├─► Database (running, replicated)
                                           ├─► AMIs/Images (pre-baked)
                                           └─► Auto Scaling Groups (min=0)

Failover:
    1. Scale up auto scaling groups
    2. Update database to read/write
    3. Update DNS
    4. RTO: 10-30 minutes, RPO: 5-15 minutes
```

**Implementation:**

```hcl
# Secondary region ASG (scaled to 0)
resource "aws_autoscaling_group" "secondary" {
  provider            = aws.us-west-2
  name                = "app-secondary"
  min_size            = 0
  max_size            = 10
  desired_capacity    = 0
  vpc_zone_identifier = data.aws_subnet_ids.secondary.ids

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  tags = [
    {
      key                 = "Environment"
      value               = "dr-secondary"
      propagate_at_launch = true
    }
  ]
}

# Failover Lambda
resource "aws_lambda_function" "failover" {
  function_name = "dr-failover"
  role          = aws_iam_role.lambda.arn
  handler       = "index.handler"
  runtime       = "python3.11"
  timeout       = 300

  environment {
    variables = {
      ASG_NAME = aws_autoscaling_group.secondary.name
      REGION   = "us-west-2"
    }
  }
}
```

**Failover Script:**

```python
# lambda/failover.py
import boto3
import os

def handler(event, context):
    asg_name = os.environ['ASG_NAME']
    region = os.environ['REGION']

    asg = boto3.client('autoscaling', region_name=region)
    route53 = boto3.client('route53')

    # Scale up ASG
    asg.set_desired_capacity(
        AutoScalingGroupName=asg_name,
        DesiredCapacity=5
    )

    # Update DNS
    route53.change_resource_record_sets(
        HostedZoneId='Z1234567890ABC',
        ChangeBatch={
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': 'app.example.com',
                    'Type': 'CNAME',
                    'TTL': 60,
                    'ResourceRecords': [{'Value': 'app-secondary-lb.us-west-2.elb.amazonaws.com'}]
                }
            }]
        }
    )

    return {'statusCode': 200, 'body': 'Failover completed'}
```

---

## Chaos Engineering for DR

### Chaos Engineering Principles

1. **Start Small:** Begin in staging, limited blast radius
2. **Hypothesize:** Define expected behavior before experiment
3. **Measure:** Quantify impact (latency, error rate, availability)
4. **Automate:** Integrate into CI/CD for continuous validation
5. **Learn:** Document findings, improve systems and runbooks

### DR-Specific Chaos Experiments

#### Experiment 1: Database Failover Test

**Hypothesis:** Application should continue operating with < 30s downtime when primary database fails

**Procedure:**

```bash
#!/bin/bash
# chaos/db-failover-test.sh

set -euo pipefail

# Baseline metrics
echo "Collecting baseline metrics..."
BASELINE_ERROR_RATE=$(curl -s http://prometheus:9090/api/v1/query?query=rate\(http_requests_total\{status=~\"5..\"\}\[1m\]\) | jq -r '.data.result[0].value[1]')

# Simulate database failure (stop primary)
echo "Simulating database failure..."
ssh primary-db "sudo systemctl stop postgresql"

# Measure impact
START_TIME=$(date +%s)
while true; do
  ERROR_RATE=$(curl -s http://prometheus:9090/api/v1/query?query=rate\(http_requests_total\{status=~\"5..\"\}\[1m\]\) | jq -r '.data.result[0].value[1]')

  if (( $(echo "$ERROR_RATE < $BASELINE_ERROR_RATE * 1.1" | bc -l) )); then
    END_TIME=$(date +%s)
    DOWNTIME=$((END_TIME - START_TIME))
    echo "Recovery completed in ${DOWNTIME}s"
    break
  fi

  sleep 1
done

# Verify secondary promoted
CURRENT_PRIMARY=$(psql -h db-vip -U app -c "SELECT pg_is_in_recovery();" -t)
if [ "$CURRENT_PRIMARY" = "f" ]; then
  echo "SUCCESS: Secondary promoted to primary"
else
  echo "FAILURE: Secondary not promoted"
  exit 1
fi

# Report
if [ $DOWNTIME -lt 30 ]; then
  echo "PASS: Downtime ($DOWNTIME s) within SLA (< 30s)"
else
  echo "FAIL: Downtime ($DOWNTIME s) exceeds SLA (< 30s)"
  exit 1
fi
```

#### Experiment 2: Region Failure Simulation

**Hypothesis:** Application should failover to secondary region with < 5 min RTO when primary region becomes unavailable

**Procedure:**

```bash
#!/bin/bash
# chaos/region-failure-test.sh

set -euo pipefail

PRIMARY_REGION="us-east-1"
SECONDARY_REGION="us-west-2"
PRIMARY_LB="app-primary-123.us-east-1.elb.amazonaws.com"
SECONDARY_LB="app-secondary-456.us-west-2.elb.amazonaws.com"

# Baseline health check
echo "Checking baseline health..."
curl -f "http://$PRIMARY_LB/health" || { echo "Primary unhealthy before test"; exit 1; }
curl -f "http://$SECONDARY_LB/health" || { echo "Secondary unhealthy before test"; exit 1; }

# Simulate region failure (block all traffic to primary)
echo "Simulating region failure (blocking primary region)..."
aws ec2 create-network-acl-entry \
  --region $PRIMARY_REGION \
  --network-acl-id acl-12345678 \
  --ingress \
  --rule-number 1 \
  --protocol -1 \
  --rule-action deny \
  --cidr-block 0.0.0.0/0

START_TIME=$(date +%s)

# Trigger failover (manual or automated)
echo "Triggering failover to secondary region..."
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "app.example.com",
        "Type": "CNAME",
        "TTL": 60,
        "ResourceRecords": [{"Value": "'$SECONDARY_LB'"}]
      }
    }]
  }'

# Wait for DNS propagation and verify
echo "Waiting for DNS propagation..."
while true; do
  RESOLVED=$(dig +short app.example.com @8.8.8.8 | head -n1)
  if [[ "$RESOLVED" == *"us-west-2"* ]]; then
    echo "DNS updated to secondary region"
    break
  fi
  sleep 5
done

# Verify application health
while true; do
  if curl -f "http://app.example.com/health" 2>/dev/null; then
    END_TIME=$(date +%s)
    RTO=$((END_TIME - START_TIME))
    echo "Application recovered in ${RTO}s"
    break
  fi
  sleep 5
done

# Cleanup (remove NACL rule)
aws ec2 delete-network-acl-entry \
  --region $PRIMARY_REGION \
  --network-acl-id acl-12345678 \
  --ingress \
  --rule-number 1

# Report
if [ $RTO -lt 300 ]; then
  echo "PASS: RTO ($RTO s) within SLA (< 5 min)"
else
  echo "FAIL: RTO ($RTO s) exceeds SLA (< 5 min)"
  exit 1
fi
```

#### Experiment 3: Kubernetes Pod Deletion (Velero Restore)

**Hypothesis:** Velero can restore deleted namespace with all resources within 10 minutes

**Procedure:**

```bash
#!/bin/bash
# chaos/k8s-namespace-recovery-test.sh

set -euo pipefail

NAMESPACE="test-app"
BACKUP_NAME="daily-full-backup-latest"

# Capture current state
echo "Capturing current state..."
kubectl get all -n $NAMESPACE -o yaml > /tmp/original-state.yaml
ORIGINAL_POD_COUNT=$(kubectl get pods -n $NAMESPACE --no-headers | wc -l)

# Delete namespace
echo "Deleting namespace $NAMESPACE..."
kubectl delete namespace $NAMESPACE

# Verify deletion
kubectl get namespace $NAMESPACE 2>/dev/null && { echo "Namespace still exists"; exit 1; }

# Start restore
echo "Starting Velero restore..."
START_TIME=$(date +%s)
RESTORE_NAME="test-restore-$(date +%s)"
velero restore create $RESTORE_NAME --from-backup $BACKUP_NAME --include-namespaces $NAMESPACE

# Wait for restore completion
while true; do
  STATUS=$(velero restore describe $RESTORE_NAME --details | grep "Phase:" | awk '{print $2}')
  if [ "$STATUS" = "Completed" ]; then
    END_TIME=$(date +%s)
    RESTORE_TIME=$((END_TIME - START_TIME))
    echo "Restore completed in ${RESTORE_TIME}s"
    break
  elif [ "$STATUS" = "Failed" ] || [ "$STATUS" = "PartiallyFailed" ]; then
    echo "FAIL: Restore failed with status: $STATUS"
    velero restore logs $RESTORE_NAME
    exit 1
  fi
  sleep 5
done

# Verify restored resources
RESTORED_POD_COUNT=$(kubectl get pods -n $NAMESPACE --no-headers | wc -l)
if [ "$RESTORED_POD_COUNT" -eq "$ORIGINAL_POD_COUNT" ]; then
  echo "SUCCESS: All pods restored ($RESTORED_POD_COUNT/$ORIGINAL_POD_COUNT)"
else
  echo "FAIL: Pod count mismatch (restored: $RESTORED_POD_COUNT, original: $ORIGINAL_POD_COUNT)"
  exit 1
fi

# Report
if [ $RESTORE_TIME -lt 600 ]; then
  echo "PASS: Restore time ($RESTORE_TIME s) within SLA (< 10 min)"
else
  echo "FAIL: Restore time ($RESTORE_TIME s) exceeds SLA (< 10 min)"
  exit 1
fi
```

### Chaos Engineering Tools

| Tool | Use Case | Platform |
|------|----------|----------|
| **Chaos Mesh** | Kubernetes chaos engineering | K8s |
| **Gremlin** | Enterprise chaos platform | Cloud, K8s, VMs |
| **Chaos Monkey** | Random instance termination | AWS, GCP, Azure |
| **Litmus** | Cloud-native chaos experiments | K8s |
| **Pumba** | Docker chaos testing | Docker |
| **Toxiproxy** | Network chaos (latency, failures) | Any |

---

## Tool Recommendations

### Recommended Tools by Use Case

#### Database Backups

| Database | Primary Tool | Alternative | Strengths |
|----------|-------------|-------------|-----------|
| **PostgreSQL** | pgBackRest | WAL-G, Barman | PITR, compression, multi-repo support |
| **MySQL** | Percona XtraBackup | WAL-G, mysqldump | Hot backups, incremental, PITR |
| **MongoDB** | MongoDB Atlas Backup | mongodump, Ops Manager | Continuous backup, PITR, automation |
| **Redis** | RDB snapshots + AOF | Redis Enterprise | Persistence, fast recovery |
| **Cassandra** | Nodetool snapshot | Medusa | Distributed backups |

#### Kubernetes Backups

| Use Case | Tool | Why |
|----------|------|-----|
| **Full cluster DR** | Velero | Industry standard, PV support, schedule-based |
| **File-level backup** | Restic (via Velero) | No snapshot support required |
| **etcd backup** | etcdctl snapshot | Control plane recovery |
| **GitOps sync** | ArgoCD + Git | Declarative, version-controlled |

#### Cloud Storage

| Provider | Service | Storage Class | Use Case |
|----------|---------|---------------|----------|
| **AWS** | S3 | Standard → IA → Glacier → Deep Archive | General backups |
| **AWS** | EBS Snapshots | N/A | Volume backups |
| **GCP** | Cloud Storage | Standard → Nearline → Coldline → Archive | General backups |
| **GCP** | Persistent Disk Snapshots | N/A | Volume backups |
| **Azure** | Blob Storage | Hot → Cool → Archive | General backups |
| **Azure** | Managed Disks Snapshots | N/A | Volume backups |

#### File/Object Backups

| Tool | Trust Score | Strengths |
|------|-------------|-----------|
| **Restic** | High | Encryption, deduplication, multi-backend |
| **Duplicity** | High | GPG encryption, incremental |
| **Rclone** | High | 40+ cloud backends, sync |
| **Borg Backup** | High | Deduplication, compression |

#### Cross-Region Replication

| Scenario | Tool/Service | Pattern |
|----------|-------------|---------|
| **AWS database** | Aurora Global DB | Active-Active |
| **AWS database** | RDS Read Replicas | Active-Passive |
| **GCP database** | Cloud SQL HA | Active-Passive |
| **Azure database** | SQL Database Geo-Replication | Active-Passive |
| **Object storage** | S3 CRR / GCS Multi-Regional | Automatic |
| **Application** | Global load balancer + local DBs | Active-Active |

### Tool Comparison Matrix

| Tool | Type | Platforms | Encryption | Compression | PITR | Complexity |
|------|------|-----------|------------|-------------|------|------------|
| **pgBackRest** | DB Backup | PostgreSQL | Yes (AES-256) | Yes (lz4, gz, zst) | Yes | Medium |
| **WAL-G** | DB Backup | PostgreSQL, MySQL, MongoDB | Yes (libsodium) | Yes (zstd, lz4) | Yes | Medium |
| **Percona XtraBackup** | DB Backup | MySQL | No | Yes | Yes | Low |
| **Velero** | K8s Backup | Kubernetes | Optional | Optional | No | Medium |
| **Restic** | File Backup | Multi-OS | Yes (AES-256) | Yes | No | Low |
| **Rclone** | Sync/Backup | Multi-cloud | Optional | Optional | No | Low |

---

## Skill Structure Design

```
disaster-recovery/
├── SKILL.md                                # Main skill (600-800 lines)
│   ├── Purpose and when to use
│   ├── Quick RTO/RPO decision framework
│   ├── Backup strategy selection guide
│   └── References to detailed docs
├── references/
│   ├── rto-rpo-planning.md                # Defining objectives, criticality tiers
│   ├── database-backups.md                # PostgreSQL, MySQL, MongoDB patterns
│   ├── kubernetes-dr.md                   # Velero, etcd, PV backups
│   ├── cloud-dr-patterns.md               # AWS, GCP, Azure specific DR
│   ├── cross-region-replication.md        # Active-Active, Active-Passive patterns
│   ├── chaos-engineering.md               # DR testing with chaos experiments
│   ├── compliance-retention.md            # GDPR, SOC 2, HIPAA requirements
│   └── runbook-automation.md              # Automating DR procedures
├── examples/
│   ├── postgresql/
│   │   ├── pgbackrest-config/
│   │   │   ├── pgbackrest.conf
│   │   │   ├── postgresql.conf
│   │   │   └── restore.sh
│   │   └── walg-config/
│   │       ├── env-vars.sh
│   │       ├── backup.sh
│   │       └── restore.sh
│   ├── mysql/
│   │   ├── xtrabackup/
│   │   │   ├── full-backup.sh
│   │   │   ├── incr-backup.sh
│   │   │   └── restore.sh
│   │   └── walg/
│   │       ├── stream-backup.sh
│   │       └── restore.sh
│   ├── kubernetes/
│   │   ├── velero/
│   │   │   ├── install.sh
│   │   │   ├── schedules/
│   │   │   │   ├── daily-full.yaml
│   │   │   │   └── hourly-app.yaml
│   │   │   └── restore-examples.sh
│   │   └── etcd/
│   │       ├── backup.sh
│   │       └── restore.sh
│   ├── cloud/
│   │   ├── aws/
│   │   │   ├── rds-pitr.tf
│   │   │   ├── s3-replication.tf
│   │   │   └── aurora-global.tf
│   │   ├── gcp/
│   │   │   ├── cloud-sql-backup.tf
│   │   │   └── gcs-multi-region.tf
│   │   └── azure/
│   │       ├── vm-backup.tf
│   │       └── site-recovery.tf
│   └── chaos/
│       ├── db-failover-test.sh
│       ├── region-failure-test.sh
│       └── k8s-namespace-recovery-test.sh
└── scripts/
    ├── validate-backup.sh                  # Verify backup integrity
    ├── test-restore.sh                     # Automated restore testing
    ├── dr-drill.sh                         # Run full DR drill
    ├── check-retention.sh                  # Verify retention policies
    └── generate-dr-report.sh               # Compliance reporting
```

### SKILL.md Structure (600-800 lines)

```markdown
# Disaster Recovery Skill

## Purpose
Guide DR strategy design, backup implementation, and recovery procedures...

## When to Use This Skill
- Designing DR strategy (RTO/RPO planning)
- Implementing database backups with PITR
- Setting up Kubernetes cluster backups
- Configuring cross-region replication
- Testing DR procedures with chaos engineering
- Meeting compliance requirements (GDPR, SOC 2)

## Quick Decision Framework

### 1. Define RTO/RPO Requirements
[Framework 1: RTO/RPO to DR Strategy Mapping - condensed version]

### 2. Choose Backup Strategy
[Framework 2: Backup Strategy Selection - condensed decision tree]

### 3. Select Tools
[Tool selection guide by use case - table format]

## Database Backup Patterns

### PostgreSQL
**Quick Start:** See `examples/postgresql/pgbackrest-config/`
**Detailed Guide:** See `references/database-backups.md#postgresql`

[Condensed pgBackRest example]

### MySQL
**Quick Start:** See `examples/mysql/xtrabackup/`
**Detailed Guide:** See `references/database-backups.md#mysql`

[Condensed XtraBackup example]

## Kubernetes DR

### Velero
**Quick Start:** See `examples/kubernetes/velero/`
**Detailed Guide:** See `references/kubernetes-dr.md#velero`

[Condensed Velero example]

## Cloud DR Patterns

### AWS
See `references/cloud-dr-patterns.md#aws`
Examples: `examples/cloud/aws/`

### GCP
See `references/cloud-dr-patterns.md#gcp`
Examples: `examples/cloud/gcp/`

### Azure
See `references/cloud-dr-patterns.md#azure`
Examples: `examples/cloud/azure/`

## Testing DR

### Chaos Engineering
See `references/chaos-engineering.md`
Examples: `examples/chaos/`

[Brief overview of chaos experiments]

## Compliance

### Retention Requirements
See `references/compliance-retention.md`

[Table of common compliance requirements]

## Automation

### DR Drills
See `references/runbook-automation.md`
Scripts: `scripts/dr-drill.sh`

[Overview of automated testing]

## Integration with Other Skills

- `infrastructure-as-code`: Provision DR infrastructure
- `kubernetes-operations`: K8s cluster management
- `databases-postgresql`: PostgreSQL operations
- `databases-mysql`: MySQL operations
- `observability`: Monitor backup jobs, alert on failures
- `incident-management`: Invoke DR during incidents
```

---

## Integration Points

### With Existing Skills

| Skill | Integration | Direction |
|-------|-------------|-----------|
| `infrastructure-as-code` | Provision backup infrastructure, DR regions | Prerequisite |
| `kubernetes-operations` | K8s cluster setup for Velero, etcd | Prerequisite |
| `databases-postgresql` | PostgreSQL configuration, operations | Parallel |
| `databases-mysql` | MySQL configuration, operations | Parallel |
| `secret-management` | Backup encryption keys, credentials | Prerequisite |
| `observability` | Backup monitoring, alerting | Parallel |
| `building-ci-pipelines` | Automated backup testing, DR drills | Parallel |
| `incident-management` | Invoke DR procedures during incidents | Consumer |
| `security-hardening` | Secure backup storage, access control | Parallel |

### Skill Chaining Examples

#### Example 1: Full Stack DR Setup

```
infrastructure-as-code → secret-management → disaster-recovery → observability
        ↓                       ↓                    ↓                ↓
  Create S3 buckets     Store encryption    Configure pgBackRest   Monitor backups
  Create VPCs           keys in Vault       Schedule Velero        Alert on failures
  Provision RDS                             Set up replication
```

#### Example 2: Kubernetes DR with Testing

```
kubernetes-operations → disaster-recovery → building-ci-pipelines
        ↓                      ↓                     ↓
  Deploy apps          Install Velero        Automate DR drills
  Configure RBAC       Schedule backups      Test restores daily
  Set up monitoring    etcd snapshots        Chaos experiments
```

#### Example 3: Database PITR

```
databases-postgresql → secret-management → disaster-recovery → observability
        ↓                     ↓                   ↓                  ↓
  Configure WAL         Store passwords    pgBackRest setup    Grafana dashboard
  Tune performance      Backup keys        PITR config         Backup metrics
  Replication                              Test restores       Alert on RPO breach
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

**Deliverables:**
- [ ] Core SKILL.md with decision frameworks
- [ ] RTO/RPO planning reference doc
- [ ] Database backup patterns (PostgreSQL, MySQL)
- [ ] pgBackRest and XtraBackup examples
- [ ] Basic backup validation scripts

**Focus:** Enable database DR for most common use cases

### Phase 2: Kubernetes DR (Week 3-4)

**Deliverables:**
- [ ] Kubernetes DR reference doc
- [ ] Velero installation and configuration examples
- [ ] etcd backup/restore procedures
- [ ] Namespace and cluster-level backup schedules
- [ ] PV snapshot integration
- [ ] Restore testing automation

**Focus:** Complete K8s cluster backup and recovery

### Phase 3: Cloud-Specific Patterns (Week 5-6)

**Deliverables:**
- [ ] Cloud DR patterns reference doc
- [ ] AWS examples (RDS, Aurora, S3 CRR)
- [ ] GCP examples (Cloud SQL, GCS)
- [ ] Azure examples (VM Backup, Site Recovery)
- [ ] Cross-region replication patterns
- [ ] Multi-cloud DR architecture examples

**Focus:** Cloud-native DR with provider-specific services

### Phase 4: Testing & Chaos (Week 7-8)

**Deliverables:**
- [ ] Chaos engineering reference doc
- [ ] DR testing scripts (db failover, region failure)
- [ ] Automated DR drill framework
- [ ] Compliance reporting
- [ ] Runbook automation examples
- [ ] Integration with CI/CD for continuous DR testing

**Focus:** Validate DR procedures through automated testing

### Phase 5: Polish & Integration (Week 9-10)

**Deliverables:**
- [ ] Complete all reference docs
- [ ] Comprehensive examples for all patterns
- [ ] Integration guides with other skills
- [ ] Video walkthroughs (optional)
- [ ] Troubleshooting guide
- [ ] Final review and testing

**Focus:** Production-ready skill with complete documentation

---

## Key Takeaways

### Strategic Insights

1. **Untested Backups Are Not Backups:** Regular testing is non-negotiable
2. **RTO/RPO Drive Everything:** Define objectives before choosing tools
3. **3-2-1 Rule is Foundational:** 3 copies, 2 media types, 1 offsite
4. **Immutable Backups for Ransomware:** Versioning and object lock protect against deletion
5. **PITR is Expected:** Databases need point-in-time recovery, not just full backups
6. **Automation Reduces Error:** Manual DR procedures fail under pressure
7. **Multi-Cloud Requires Unified Strategy:** Same concepts, different implementations

### Technical Highlights

**PostgreSQL DR:**
- pgBackRest: Production-grade with compression, encryption, PITR
- WAL-G: Cloud-first, delta backups, multi-database support
- Continuous archiving: < 5 min RPO with WAL shipping

**MySQL DR:**
- Percona XtraBackup: Hot backups without downtime
- Binary log archiving: Point-in-time recovery
- WAL-G: Unified tool for MySQL, PostgreSQL, MongoDB

**Kubernetes DR:**
- Velero: Industry standard for cluster backups
- etcd snapshots: Control plane recovery
- Restic integration: File-level backups without snapshots

**Cloud DR:**
- AWS: RDS automated backups, Aurora Global Database, S3 CRR
- GCP: Cloud SQL PITR, Multi-Regional Storage
- Azure: VM Backup, Site Recovery for geo-replication

**Chaos Engineering:**
- Validates DR procedures under failure conditions
- Builds confidence in automation
- Identifies brittle dependencies
- Should be integrated into CI/CD

### Common Pitfalls

❌ **Don't:**
- Assume backups work without testing
- Forget to document recovery procedures
- Ignore encryption for sensitive data
- Store all backups in single region
- Skip retention policy definition
- Rely solely on cloud provider backups

✅ **Do:**
- Test restores regularly (monthly for critical systems)
- Automate backup monitoring and alerting
- Encrypt backups at rest and in transit
- Implement 3-2-1 backup rule
- Define and measure RTO/RPO
- Run chaos experiments to validate DR

---

**Progressive Disclosure:** This init.md provides the master plan with comprehensive examples. Detailed documentation and additional patterns will be organized in `references/` directory. Scripts in `scripts/` provide automation for validation, testing, and reporting.

**Next Steps:** Create SKILL.md following the structure outlined above, then populate reference docs and examples based on this master plan.
