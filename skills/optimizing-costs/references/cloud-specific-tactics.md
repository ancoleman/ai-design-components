# Cloud-Specific Cost Optimization Tactics

Quick reference for AWS, Azure, and GCP cost optimization tactics beyond the universal strategies covered in SKILL.md.

## Table of Contents

1. [AWS Optimization Tactics](#aws-optimization-tactics)
2. [Azure Optimization Tactics](#azure-optimization-tactics)
3. [GCP Optimization Tactics](#gcp-optimization-tactics)
4. [Multi-Cloud Cost Comparison](#multi-cloud-cost-comparison)

---

## AWS Optimization Tactics

### Compute

**EC2 Compute Optimizer:** ML-based rightsizing recommendations
```bash
aws compute-optimizer get-ec2-instance-recommendations \
  --instance-arns arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0
```

**Savings Plans:** More flexible than Reserved Instances
- Compute Savings Plans: Apply to EC2, Fargate, Lambda
- EC2 Instance Savings Plans: Apply within instance family

**Graviton Instances:** 40% better price/performance
- Migrate x86 workloads to ARM-based Graviton2/Graviton3 instances
- Example: m6g.xlarge (Graviton) vs m5.xlarge (x86) = 20% cost savings

### Storage

**S3 Intelligent-Tiering:** Automatic cost optimization
```bash
aws s3api put-bucket-intelligent-tiering-configuration \
  --bucket mybucket \
  --id default-config \
  --intelligent-tiering-configuration '{
    "Id": "default-config",
    "Status": "Enabled",
    "Tierings": [
      {"Days": 90, "AccessTier": "ARCHIVE_ACCESS"},
      {"Days": 180, "AccessTier": "DEEP_ARCHIVE_ACCESS"}
    ]
  }'
```

**EBS gp3 Migration:** 20% cheaper than gp2
```bash
# Modify volume type from gp2 to gp3
aws ec2 modify-volume \
  --volume-id vol-1234567890abcdef0 \
  --volume-type gp3
```

**S3 Lifecycle Policies:**
```xml
<LifecycleConfiguration>
  <Rule>
    <Filter><Prefix>logs/</Prefix></Filter>
    <Status>Enabled</Status>
    <Transition>
      <Days>30</Days>
      <StorageClass>STANDARD_IA</StorageClass>
    </Transition>
    <Transition>
      <Days>90</Days>
      <StorageClass>GLACIER</StorageClass>
    </Transition>
    <Expiration><Days>365</Days></Expiration>
  </Rule>
</LifecycleConfiguration>
```

### Lambda

**Right-Size Memory:** CPU scales proportionally with memory
- Over-provisioned memory = wasted cost
- Under-provisioned memory = longer execution time (higher cost)
- Use AWS Lambda Power Tuning to find optimal memory allocation

**Provisioned Concurrency:** Avoid if possible ($0.015/GB-hour)
- Use only for latency-sensitive workloads
- Consider Application Auto Scaling for Provisioned Concurrency

### Networking

**NAT Gateway Optimization:** $0.045/hour = $32.85/month each
- Use single NAT Gateway per AZ (not per subnet)
- Consider NAT instances for low-traffic workloads (cheaper)
- VPC Endpoints for AWS services (avoid NAT Gateway data transfer)

**CloudFront for Static Content:** Reduce data transfer costs
- S3 data transfer: $0.09/GB (egress)
- CloudFront: $0.085/GB (first 10 TB)

### Database

**RDS Reserved Instances:** 60-72% discount
- Purchase for production databases (24/7 uptime)
- Use Aurora Serverless v2 for variable workloads

**DynamoDB On-Demand vs. Provisioned:**
```
On-Demand: $1.25/million writes, $0.25/million reads
Provisioned: $0.00065/WCU/hour, $0.00013/RCU/hour

Break-even: ~350 WCU or 1,750 RCU continuous usage
Use On-Demand for: Unpredictable traffic, new workloads
Use Provisioned for: Predictable traffic, cost optimization
```

---

## Azure Optimization Tactics

### Compute

**Azure Hybrid Benefit:** Bring Windows Server licenses
- Savings: Up to 85% on Windows VMs
- Eligibility: Windows Server licenses with Software Assurance
- Stack with Reserved VM Instances for maximum savings

**Azure Spot VMs:** Up to 90% discount
```bash
az vm create \
  --resource-group myResourceGroup \
  --name mySpotVM \
  --priority Spot \
  --max-price 0.05 \
  --eviction-policy Deallocate
```

**Dev/Test Pricing:** 20-40% discount for non-production
- Requires Visual Studio subscription
- Applies to VMs, App Service, SQL Database

**B-Series Burstable VMs:** 30-60% cheaper for low-utilization workloads
- Accumulates CPU credits during idle time
- Bursts to 100% CPU when needed
- Ideal for: Web servers, dev/test, small databases

### Storage

**Azure Blob Lifecycle Management:**
```json
{
  "rules": [{
    "name": "archive-old-logs",
    "type": "Lifecycle",
    "definition": {
      "actions": {
        "baseBlob": {
          "tierToCool": { "daysAfterModificationGreaterThan": 30 },
          "tierToArchive": { "daysAfterModificationGreaterThan": 90 },
          "delete": { "daysAfterModificationGreaterThan": 365 }
        }
      }
    }
  }]
}
```

**Managed Disk Optimization:**
- Premium SSD: $0.135/GB/month (high IOPS)
- Standard SSD: $0.075/GB/month (moderate IOPS, 44% cheaper)
- Standard HDD: $0.045/GB/month (low IOPS, 67% cheaper)

### Database

**Azure SQL Database Serverless:** Pay per use
- Autopause during inactivity (no compute charges)
- Auto-resume on connection
- Ideal for: Dev/test, intermittent workloads

**Hyperscale Tier:** Separate compute and storage pricing
- Scale compute independently of storage
- Pay only for storage used (no pre-provisioning)

### Networking

**Azure Front Door vs. Application Gateway:**
- Application Gateway: Regional load balancer ($0.025/hour)
- Front Door: Global load balancer with CDN ($0.36/hour)
- Use Application Gateway if traffic is regional (cheaper)

---

## GCP Optimization Tactics

### Compute

**Sustained Use Discounts:** Automatic 20-30% discount
- No commitment required
- Applied automatically for VMs running >25% of month
- Stacks with Committed Use Discounts

**Committed Use Discounts:** 52-70% savings
```bash
gcloud compute commitments create my-commitment \
  --plan=36-month \
  --resources=vcpu=100,memory=400GB \
  --region=us-central1
```

**Preemptible VMs:** Up to 91% discount
```bash
gcloud compute instances create preemptible-instance \
  --preemptible \
  --zone=us-central1-a \
  --machine-type=n1-standard-4
```

**E2 Instances:** 30% cheaper than N1 instances
- Same performance for most workloads
- Automatically uses cost-optimized CPU platform

### Storage

**Cloud Storage Autoclass:** Automatic tier management
```bash
gcloud storage buckets update gs://mybucket \
  --autoclass
```

**Tiers:**
- Standard: $0.020/GB/month (hot data)
- Nearline: $0.010/GB/month (accessed <1/month)
- Coldline: $0.004/GB/month (accessed <1/quarter)
- Archive: $0.0012/GB/month (accessed <1/year)

**Lifecycle Management:**
```yaml
lifecycle:
  rule:
  - action:
      type: SetStorageClass
      storageClass: NEARLINE
    condition:
      age: 30
  - action:
      type: Delete
    condition:
      age: 365
```

### BigQuery

**Flat-Rate Pricing:** Predictable costs for heavy usage
- On-Demand: $5/TB scanned
- Flat-Rate: $10,000/month for 500 slots (100 TB/month break-even)

**Query Cost Optimization:**
```sql
-- Bad: Full table scan
SELECT * FROM bigquery-public-data.usa_names.usa_1910_current;

-- Good: Partition pruning
SELECT * FROM bigquery-public-data.usa_names.usa_1910_current
WHERE year BETWEEN 2000 AND 2010;

-- Good: Column selection
SELECT name, year FROM bigquery-public-data.usa_names.usa_1910_current;
```

**Clustering and Partitioning:** Reduce scanned data
```sql
CREATE TABLE mydataset.mytable (
  transaction_id STRING,
  transaction_date DATE,
  amount NUMERIC
)
PARTITION BY transaction_date
CLUSTER BY transaction_id;
```

### Networking

**Cloud CDN:** Reduce egress costs
- Standard egress: $0.12/GB
- Cloud CDN: $0.08/GB (33% cheaper)
- Cache static content at edge locations

**Private Google Access:** Avoid NAT Gateway costs
- Access Google APIs from private VMs without external IP
- No NAT Gateway charges ($0.045/hour saved)

---

## Multi-Cloud Cost Comparison

### Compute (General Purpose, 4 vCPU, 16 GB RAM)

| Cloud | On-Demand | 1-Year Reserved | 3-Year Reserved | Spot/Preemptible |
|-------|-----------|-----------------|-----------------|------------------|
| **AWS** (m5.xlarge) | $0.192/hour | $0.116/hour (40%) | $0.077/hour (60%) | $0.038/hour (80%) |
| **Azure** (D4s_v3) | $0.192/hour | $0.115/hour (40%) | $0.076/hour (60%) | $0.019/hour (90%) |
| **GCP** (n2-standard-4) | $0.195/hour | $0.122/hour (37%) | $0.098/hour (50%) | $0.020/hour (90%) |

### Storage (Object Storage, Standard Tier)

| Cloud | Storage | Retrieval | Egress (first 10 TB) |
|-------|---------|-----------|---------------------|
| **AWS S3** | $0.023/GB | Free | $0.09/GB |
| **Azure Blob** | $0.018/GB | Free | $0.087/GB |
| **GCP Cloud Storage** | $0.020/GB | Free | $0.12/GB |

### Database (Managed PostgreSQL, 4 vCPU, 16 GB RAM)

| Cloud | On-Demand | 1-Year Reserved | 3-Year Reserved |
|-------|-----------|-----------------|-----------------|
| **AWS RDS** (db.m5.xlarge) | $0.384/hour | $0.231/hour (40%) | $0.154/hour (60%) |
| **Azure SQL** (GP_Gen5_4) | $0.388/hour | $0.233/hour (40%) | $0.155/hour (60%) |
| **GCP Cloud SQL** (db-n1-standard-4) | $0.385/hour | $0.241/hour (37%) | $0.193/hour (50%) |
