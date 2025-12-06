# AWS Storage Services - Deep Dive

## Table of Contents

1. [S3 (Simple Storage Service)](#s3-simple-storage-service)
2. [EBS (Elastic Block Store)](#ebs-elastic-block-store)
3. [EFS (Elastic File System)](#efs-elastic-file-system)
4. [FSx Family](#fsx-family)
5. [Storage Selection Guide](#storage-selection-guide)

---

## S3 (Simple Storage Service)

### Storage Classes

| Class | Use Case | Durability | Availability | Cost/GB | Retrieval Cost |
|-------|----------|------------|--------------|---------|----------------|
| **Standard** | Frequent access | 99.999999999% | 99.99% | $0.023 | Free |
| **Intelligent-Tiering** | Unknown/changing | 99.999999999% | 99.9% | $0.023-$0.00099 | Free |
| **Standard-IA** | Infrequent (>30 days) | 99.999999999% | 99.9% | $0.0125 | $0.01/GB |
| **One Zone-IA** | Non-critical | 99.999999999% | 99.5% | $0.01 | $0.01/GB |
| **Glacier Instant** | Archive, instant | 99.999999999% | 99.9% | $0.004 | $0.03/GB |
| **Glacier Flexible** | Archive, 1-5 min | 99.999999999% | 99.99% | $0.0036 | $0.01-$0.03/GB |
| **Glacier Deep Archive** | Long-term (7-10yr) | 99.999999999% | 99.99% | $0.00099 | $0.02/GB + 12hr |
| **S3 Express One Zone** | High perf (NEW) | 99.999999999% | 99.95% | $0.16 | Free |

### S3 Intelligent-Tiering

**How it Works:**
- Automatic optimization across 5 tiers
- No retrieval fees
- Small monitoring fee: $0.0025 per 1,000 objects

**Tiers:**
1. Frequent Access (0-30 days): $0.023/GB
2. Infrequent Access (30-90 days): $0.0125/GB
3. Archive Instant Access (90-180 days): $0.004/GB
4. Archive Access (180-365 days): $0.0036/GB
5. Deep Archive (365+ days): $0.00099/GB

**Use When:**
- Unknown or changing access patterns
- Want automated cost optimization
- Can tolerate small monitoring fee

### S3 Express One Zone (2024)

**Performance:**
- 10x faster than S3 Standard
- Single-digit millisecond latency
- Hundreds of thousands of requests per second

**Use Cases:**
- Low-latency data processing
- ML training data access
- High-performance computing

**Cost Trade-off:**
- $0.16/GB vs. $0.023/GB (7x more expensive)
- No data transfer charges within same AZ

### Lifecycle Policies

**Example Configuration:**

```json
{
  "Rules": [{
    "Id": "Archive old data",
    "Status": "Enabled",
    "Filter": { "Prefix": "logs/" },
    "Transitions": [
      { "Days": 30, "StorageClass": "STANDARD_IA" },
      { "Days": 90, "StorageClass": "GLACIER_IR" },
      { "Days": 365, "StorageClass": "DEEP_ARCHIVE" }
    ],
    "Expiration": { "Days": 2555 }
  }]
}
```

### S3 Features

**Versioning:**
- Preserve all versions of objects
- Protect against accidental deletion
- Enable MFA delete for extra protection

**Replication:**
- Cross-Region Replication (CRR): Disaster recovery
- Same-Region Replication (SRR): Compliance, lower latency

**S3 Object Lambda:**
- Transform objects on retrieval
- Redact PII, resize images, convert formats

**S3 Batch Operations:**
- Perform operations on billions of objects
- Copy, tag, restore from Glacier, invoke Lambda

### Best Practices

1. Enable versioning for critical data
2. Use lifecycle policies to reduce costs
3. Enable S3 Intelligent-Tiering for unknown patterns
4. Encrypt at rest (SSE-S3 or SSE-KMS)
5. Use CloudFront for frequently accessed content
6. Enable access logging for auditing

---

## EBS (Elastic Block Store)

### Volume Types

| Type | IOPS | Throughput | Cost/GB | Use Case |
|------|------|------------|---------|----------|
| **gp3** | 3,000-16,000 | 125-1,000 MB/s | $0.08 | General purpose (recommended) |
| **gp2** | 3,000-16,000 | 250 MB/s max | $0.10 | Legacy general purpose |
| **io2 Block Express** | 256,000 | 4,000 MB/s | $0.125 + IOPS | Highest performance |
| **io2** | 64,000 | 1,000 MB/s | $0.125 + IOPS | Critical workloads |
| **st1** (HDD) | 500 | 500 MB/s | $0.045 | Throughput-optimized |
| **sc1** (HDD) | 250 | 250 MB/s | $0.015 | Cold storage |

### gp3 vs. gp2

**gp3 Advantages:**
- 20% cheaper ($0.08 vs. $0.10)
- Independent IOPS and throughput scaling
- Baseline: 3,000 IOPS, 125 MB/s
- Configurable up to 16,000 IOPS, 1,000 MB/s

**Recommendation:** Use gp3 for 99% of workloads

### EBS Snapshots

**Features:**
- Incremental backups to S3
- Copy across regions
- Create volumes from snapshots

**EBS Snapshots Archive (2024):**
- 75% cheaper storage ($0.0125 vs. $0.05/GB-month)
- Restore takes 24-72 hours
- Use for compliance, long-term retention

**Fast Snapshot Restore (FSR):**
- Pre-warm snapshots for instant recovery
- $0.75/hour per AZ per snapshot
- Use for critical recovery scenarios

### Multi-Attach io2 Volumes

**Purpose:**
- Share volume across multiple EC2 instances
- Cluster file systems, HA applications

**Limitations:**
- Up to 16 instances
- Same AZ only
- io2 volumes only

### Best Practices

1. Use gp3 for general purpose workloads
2. Enable EBS encryption by default
3. Automate snapshot creation (lifecycle policies)
4. Delete unused snapshots
5. Archive old snapshots (75% cost savings)
6. Use Fast Snapshot Restore for critical backups

---

## EFS (Elastic File System)

### Storage Classes

| Class | Cost/GB-month | Performance | Use Case |
|-------|---------------|-------------|----------|
| **Standard** | $0.30 | High | Frequent access |
| **Infrequent Access (IA)** | $0.025 | Lower | >30 days idle |
| **One Zone** | $0.16 | High | Non-critical |
| **One Zone-IA** | $0.0133 | Lower | Dev/test |

### Performance Modes

**General Purpose:**
- Low latency (<10ms)
- Up to 7,000 file ops/sec
- Default mode

**Max I/O:**
- Higher aggregate throughput
- Slightly higher latency
- Big data, media processing

### Throughput Modes

**Elastic (Default):**
- Automatically scales
- Pay only for actual throughput
- $0.30/GB transferred

**Provisioned:**
- Specify throughput independent of storage
- Consistent high throughput
- $6.00/MB/s-month

**Bursting:**
- Throughput scales with storage size
- 50 MB/s per TB stored
- Legacy mode

### EFS Features (2025)

**Intelligent-Tiering:**
- Automatic movement to IA tier
- After 7, 14, 30, 60, or 90 days idle
- No retrieval fees

**EFS Replication:**
- Cross-region disaster recovery
- Near real-time replication
- $0.015/GB replicated

### Use Cases

**Ideal:**
- Shared file storage across EC2/Fargate/Lambda
- Content management systems
- Container persistent storage (ECS, EKS)
- Home directories

**Avoid:**
- Single-instance applications (use EBS)
- Windows workloads (use FSx for Windows)
- High-performance HPC (use FSx for Lustre)

### Best Practices

1. Enable Intelligent-Tiering (save 92% on IA files)
2. Use One Zone class for dev/test (50% cheaper)
3. Mount via NFS 4.1 for best compatibility
4. Use encryption in transit (TLS)
5. Monitor with CloudWatch metrics

---

## FSx Family

### FSx for Windows File Server

**Purpose:**
- Windows-native SMB file shares
- Active Directory integration

**Cost:**
- SSD: $0.013/GB-month + throughput
- HDD: $0.0065/GB-month + throughput

**Use Cases:**
- Windows applications (SQL Server, IIS)
- Home directories
- SharePoint storage

### FSx for Lustre

**Purpose:**
- High-performance computing (HPC)
- Sub-millisecond latency
- 100+ GB/s throughput

**Cost:**
- Persistent SSD: $0.145/GB-month
- Scratch: $0.084/GB-month (no replication)

**Use Cases:**
- ML training
- Video rendering
- Genomics research
- Financial modeling

**S3 Integration:**
- Link to S3 bucket
- Lazy-load data on first access
- Write results back to S3

### FSx for NetApp ONTAP

**Purpose:**
- Enterprise NAS features
- Multi-protocol (NFS, SMB, iSCSI)

**Features:**
- Snapshots, clones
- Data compression, deduplication
- SnapMirror replication
- Hybrid cloud integration

**Cost:**
- SSD: $0.230/GB-month + IOPS
- Throughput: $0.50/MB/s-month

### FSx for OpenZFS

**Purpose:**
- Linux ZFS file systems
- Up to 12.5 GB/s throughput

**Features:**
- Snapshots, clones
- Compression
- Point-in-time recovery

**Cost:**
- SSD: $0.150/GB-month + throughput

---

## Storage Selection Guide

### Decision Matrix

```
Use Case → Service

Objects (files, media, static assets) → S3
  ├─ Frequent access → S3 Standard
  ├─ Infrequent (>30 days) → S3 Standard-IA
  ├─ Archive → S3 Glacier (Instant, Flexible, Deep)
  └─ Unknown pattern → S3 Intelligent-Tiering

Block storage (databases, boot volumes) → EBS
  ├─ General purpose → gp3
  ├─ High IOPS → io2 or io2 Block Express
  └─ Throughput optimized → st1 (HDD)

Shared files (NFS) → EFS or FSx
  ├─ Linux NFS → EFS
  ├─ Windows SMB → FSx for Windows
  ├─ High-performance HPC → FSx for Lustre
  └─ Enterprise NAS → FSx for NetApp ONTAP

Container storage:
  ├─ Ephemeral → Local SSD
  ├─ Persistent single-container → EBS
  └─ Persistent shared → EFS or FSx
```

### Cost Comparison (1TB for 1 Month)

| Service | Monthly Cost | Access Pattern |
|---------|--------------|----------------|
| S3 Standard | $23 | Frequent |
| S3 Standard-IA | $12.50 | Infrequent |
| S3 Glacier Instant | $4 | Archive, instant |
| S3 Deep Archive | $0.99 | Long-term archive |
| EBS gp3 | $80 | Block storage |
| EFS Standard | $300 | Shared files, frequent |
| EFS IA | $25 | Shared files, infrequent |
| FSx for Lustre | ~$145 | High-performance HPC |

### Performance Comparison

| Service | Latency | IOPS | Throughput |
|---------|---------|------|------------|
| S3 Standard | ~100ms | N/A | Unlimited |
| S3 Express One Zone | <10ms | 100,000+ | Unlimited |
| EBS gp3 | <1ms | 16,000 | 1,000 MB/s |
| EBS io2 Block Express | <1ms | 256,000 | 4,000 MB/s |
| EFS General Purpose | <10ms | 7,000 ops/s | Elastic |
| FSx for Lustre | <1ms | Millions | 100+ GB/s |

### Lifecycle Cost Optimization

**Scenario: 100TB data with 10% active**

**Without Optimization:**
- S3 Standard: 100TB × $23 = $2,300/month

**With Lifecycle Policies:**
- Active (10TB): S3 Standard = $230
- Infrequent (30TB): S3 Standard-IA = $375
- Archive (60TB): S3 Glacier Instant = $240
- **Total: $845/month (63% savings)**

**With Intelligent-Tiering:**
- Automatic optimization
- Similar savings
- Small monitoring fee (~$250 for 100M objects)
