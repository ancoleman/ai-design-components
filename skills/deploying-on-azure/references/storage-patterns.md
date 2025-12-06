# Azure Storage Patterns Reference

Comprehensive guide to Azure storage services, tier selection, and lifecycle management.

## Table of Contents

1. [Blob Storage](#blob-storage)
2. [Azure Files](#azure-files)
3. [Managed Disks](#managed-disks)
4. [Data Lake Storage Gen2](#data-lake-storage-gen2)

---

## Blob Storage

Azure Blob Storage provides scalable object storage for unstructured data with multiple access tiers.

### Storage Redundancy Options

| Type | Copies | Scope | Use Case | Cost Multiplier |
|------|--------|-------|----------|-----------------|
| **LRS** | 3 | Single datacenter | Dev/test, non-critical | 1x |
| **ZRS** | 3 | 3 availability zones | Production, zone failures | 1.25x |
| **GRS** | 6 | 2 regions (async) | Disaster recovery | 2x |
| **GZRS** | 6 | Zones + regions | Mission-critical | 2.5x |

---

## Azure Files

Managed file shares with SMB and NFS protocols.

### Service Tiers

| Tier | Performance | Use Case | Cost/GB |
|------|-------------|----------|---------|
| **Transaction Optimized** | Standard | General purpose | Medium |
| **Hot** | Standard | Frequently accessed | Higher |
| **Cool** | Standard | Archival | Lower |
| **Premium** | SSD-backed | Low latency, high IOPS | Highest |

---

## Managed Disks

Block storage for virtual machines.

### Disk Types

| Type | Max IOPS | Max Throughput | Use Case |
|------|----------|----------------|----------|
| **Standard HDD** | 500 | 60 MB/s | Dev/test, infrequent access |
| **Standard SSD** | 6,000 | 750 MB/s | Web servers, light apps |
| **Premium SSD** | 20,000 | 900 MB/s | Production databases |
| **Ultra Disk** | 160,000 | 4,000 MB/s | SAP HANA, top-tier databases |

---

## Data Lake Storage Gen2

Hierarchical namespace for big data analytics built on Blob Storage.

**When to Use:**
- Big data analytics (Spark, Databricks)
- Data warehousing pipelines
- Machine learning feature stores
- Requires POSIX-compliant file system operations
