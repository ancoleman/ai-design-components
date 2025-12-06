# Commitment-Based Discount Strategies

## Table of Contents

1. [Overview](#overview)
2. [AWS Commitment Options](#aws-commitment-options)
3. [Azure Commitment Options](#azure-commitment-options)
4. [GCP Commitment Options](#gcp-commitment-options)
5. [Commitment Strategy Framework](#commitment-strategy-framework)
6. [Monitoring and Optimization](#monitoring-and-optimization)
7. [Common Mistakes](#common-mistakes)

---

## Overview

Commitment-based discounts are the single largest cost optimization opportunity in cloud computing, offering **40-72% savings** compared to on-demand pricing. However, commitments require careful planning to avoid waste.

### Key Principles

1. **Commit to Baseline, Not Peak:** Reserve only for steady-state usage
2. **Start Conservative:** Better to under-commit and expand than over-commit and waste
3. **Monitor Utilization:** Target >95% utilization of commitments
4. **Review Quarterly:** Usage patterns change, adjust commitments accordingly
5. **Mix Strategies:** Combine reserved, savings plans, spot, and on-demand

---

## AWS Commitment Options

### Reserved Instances (RIs)

Reserved Instances provide the highest discounts but are locked to specific instance attributes.

#### RI Types

**Standard Reserved Instances:**
- **Discount:** Up to 72% off on-demand (3-year, all upfront)
- **Flexibility:** None (locked to instance type, region, OS, tenancy)
- **Use Case:** Stable, predictable workloads with no architecture changes expected
- **Best For:** Production databases (RDS, ElastiCache), long-running EC2 instances

**Convertible Reserved Instances:**
- **Discount:** Up to 54% off on-demand (3-year, all upfront)
- **Flexibility:** Can exchange for different instance types, regions, OS
- **Use Case:** Production workloads where instance type might change
- **Best For:** Applications that may need upsizing/downsizing

**Scheduled Reserved Instances:**
- **Discount:** 5-10% off on-demand
- **Flexibility:** Reserved for specific time windows (e.g., 9am-5pm weekdays)
- **Use Case:** Predictable recurring workloads (batch jobs, business hours apps)
- **Best For:** Non-24/7 production workloads

#### RI Payment Options

| Payment Option | Upfront Cost | Monthly Cost | Discount |
|----------------|--------------|--------------|----------|
| **All Upfront** | 100% | $0 | Highest (72% for 3-year) |
| **Partial Upfront** | ~50% | 50% | Medium (69% for 3-year) |
| **No Upfront** | 0% | 100% | Lower (63% for 3-year) |

**Recommendation:** All upfront for 3-year if cash flow allows (maximum savings).

#### RI Scopes

**Regional RIs:**
- Apply to any Availability Zone in the region
- Instance size flexibility within same instance family
- **Example:** m5.xlarge RI can cover 2x m5.large or 4x m5.medium

**Zonal RIs:**
- Locked to specific Availability Zone
- Provides capacity reservation (guaranteed availability)
- No instance size flexibility
- **Use Case:** Capacity-constrained AZs

---

### AWS Savings Plans

Savings Plans offer more flexibility than Reserved Instances with slightly lower discounts.

#### Compute Savings Plans

**Coverage:**
- EC2 (any instance type, region, OS, tenancy)
- AWS Fargate
- AWS Lambda

**Discount:** Up to 66% off on-demand (3-year)

**Flexibility:** Maximum (applies across all compute services)

**Commitment:** Hourly spend amount (e.g., $10/hour)

**Use Case:** Dynamic workloads that change instance types or regions

**Example:**
```
Commit to $10/hour for 1 year:
- Covers EC2 m5.2xlarge in us-east-1 (current usage)
- Automatically applies if you switch to c5.4xlarge in eu-west-1
- Also covers Lambda and Fargate usage
```

#### EC2 Instance Savings Plans

**Coverage:**
- EC2 instances within a specific instance family (e.g., m5)
- Any size, OS, tenancy within that family
- Any region

**Discount:** Up to 72% off on-demand (3-year)

**Flexibility:** Medium (locked to instance family, but flexible on size/region/OS)

**Commitment:** Hourly spend amount (e.g., $10/hour on m5 instances)

**Use Case:** Workloads committed to instance family but may change sizes

#### Savings Plan Term Options

| Term | Discount | Flexibility | Recommendation |
|------|----------|-------------|----------------|
| **1-Year** | 40-45% | Less risk | New workloads, uncertain growth |
| **3-Year** | 60-72% | More risk | Mature, stable workloads |

---

### Reserved Instances vs. Savings Plans Decision Matrix

| Scenario | Recommendation | Reason |
|----------|---------------|---------|
| Stable RDS database | Standard RI (3-year) | Highest discount, database unlikely to change |
| Production EC2 app (stable instance type) | EC2 Instance SP (3-year) | High discount, some flexibility |
| Microservices (instance types vary) | Compute SP (1-3 year) | Maximum flexibility |
| Lambda + Fargate workloads | Compute SP | Only option that covers serverless |
| Dev/test environments | On-demand + Spot | Too variable for commitments |

---

## Azure Commitment Options

### Azure Reserved VM Instances

**Discount:** Up to 72% off pay-as-you-go (3-year)

**Coverage:**
- Virtual Machines (Linux and Windows)
- Azure Dedicated Host
- Azure App Service
- Azure SQL Database
- Azure Cosmos DB
- Azure Synapse Analytics

**Flexibility:**
- **Instance Size Flexibility:** Reservation applies to VM sizes in same series
- **Scope Options:** Shared (subscription), single resource group, management group

**Payment Options:**
- **Upfront:** Pay entire amount upfront (maximum discount)
- **Monthly:** Pay monthly installments (slightly lower discount)

**Example:**
```
Purchase: D4s_v3 VM reservation (4 vCPUs, 16 GB RAM) for 3 years
Discount: 72% off pay-as-you-go
Flexibility: Can apply to D2s_v3, D4s_v3, or D8s_v3 (same series)
```

### Azure Hybrid Benefit

**Discount:** Bring existing Windows Server licenses to Azure (up to 85% savings)

**Eligibility:**
- Windows Server licenses with Software Assurance
- SQL Server licenses with Software Assurance

**Use Case:** Enterprises with existing Microsoft licensing agreements

**Combination:** Stack with Reserved Instances for even greater savings

### Azure Savings Plans for Compute

**Discount:** Up to 65% off pay-as-you-go (3-year)

**Coverage:**
- Virtual Machines
- Dedicated Hosts
- Container Instances
- Premium Functions

**Commitment:** Hourly spend amount (e.g., $5/hour)

**Flexibility:** Applies across VM sizes, regions, operating systems

---

### Azure Dev/Test Pricing

**Discount:** Reduced rates for non-production workloads (no minimum commitment)

**Eligibility:**
- Visual Studio subscribers
- Development/testing workloads only

**Savings:** 20-40% off standard pricing

**Use Case:** Dev, QA, staging environments

---

## GCP Commitment Options

### Committed Use Discounts (CUDs)

Google Cloud offers two types of committed use discounts:

#### Resource-Based CUDs

**Commitment:** Specific resources (vCPU, memory, GPUs)

**Discount:** Up to 57% off on-demand (3-year)

**Flexibility:** Applies to any machine type using those resources

**Use Case:** Predictable compute usage with flexible machine types

**Example:**
```
Commit to: 100 vCPUs + 400 GB memory for 1 year
Discount: 37% off on-demand
Applies to: n1-standard-4 (4 vCPU, 15 GB), n2-standard-8 (8 vCPU, 32 GB), etc.
```

#### Spend-Based CUDs

**Commitment:** Dollar amount per hour (e.g., $10/hour)

**Discount:** Up to 52% off on-demand (3-year)

**Flexibility:** Maximum (applies to any compute usage)

**Use Case:** Variable workloads with unpredictable resource needs

**Example:**
```
Commit to: $10/hour for 3 years
Discount: 52% off on-demand
Applies to: All Compute Engine, GKE, Cloud SQL usage
```

### Sustained Use Discounts (Automatic)

**Discount:** 20-30% off on-demand (automatic, no commitment required)

**How it Works:** Automatically applied for VMs running >25% of the month

**Calculation:** Incremental discount increases with usage (up to 30% at 100% usage)

**Use Case:** No action needed, automatic savings for sustained workloads

**Example:**
```
VM runs 100% of month: 30% discount applied automatically
VM runs 50% of month: 15% discount applied automatically
```

### Preemptible VMs

**Discount:** Up to 91% off on-demand

**Availability:** Can be terminated with 30-second warning

**Use Case:** Fault-tolerant workloads (batch jobs, CI/CD, ML training)

**Limitations:** Maximum 24-hour runtime (VM automatically terminated)

---

## Commitment Strategy Framework

### Step 1: Analyze Historical Usage (6-12 Months)

**Goal:** Identify baseline usage (steady-state, not peak)

**Analysis:**
```
1. Export 12 months of compute usage data
2. Identify minimum daily usage (baseline floor)
3. Calculate average usage (typical steady state)
4. Identify peak usage (exclude from commitment sizing)

Example:
├── Minimum daily usage: 100 vCPUs
├── Average usage: 150 vCPUs
├── Peak usage: 250 vCPUs
└── Commitment size: 100-120 vCPUs (baseline + 20% growth buffer)
```

**Tools:**
- AWS Cost Explorer: "Reserved Instance Recommendations"
- Azure Cost Management: "Reservation Recommendations"
- GCP Billing: "Commitment Recommendations"

### Step 2: Segment Workloads

**Categorize workloads by commitment suitability:**

| Workload Type | Commitment Strategy |
|--------------|---------------------|
| Production databases | Standard RI / Reserved VM (highest discount) |
| Stable web servers | EC2 Instance SP / Resource CUD |
| Variable microservices | Compute SP / Spend-based CUD |
| Batch jobs | Spot / Preemptible (no commitment) |
| Dev/test | On-demand (shut down off-hours) |

### Step 3: Calculate Commitment Size

**Conservative Sizing Formula:**
```
Commitment Size = MIN(6-month average, 12-month minimum) × 0.85

Example:
├── 6-month average: 150 vCPUs
├── 12-month minimum: 100 vCPUs
├── MIN(150, 100) = 100 vCPUs
└── 100 × 0.85 = 85 vCPUs (commit to 85 vCPUs)

Rationale: 15% buffer to avoid underutilization
```

### Step 4: Choose Commitment Term

**1-Year vs. 3-Year Decision Matrix:**

| Factor | 1-Year | 3-Year |
|--------|--------|--------|
| **Workload Age** | <2 years | >2 years |
| **Architecture Stability** | Changing | Stable |
| **Business Certainty** | Uncertain growth | Predictable growth |
| **Discount Priority** | Moderate (40-45%) | Maximum (60-72%) |
| **Risk Tolerance** | Low (short lock-in) | High (long lock-in) |

**Recommendation:**
- **3-Year:** Mature, stable production databases and core infrastructure
- **1-Year:** Applications in growth phase, new workloads, uncertain future

### Step 5: Payment Option Selection

**All Upfront vs. No Upfront:**

| Payment | Discount | Cash Flow | Best For |
|---------|----------|-----------|----------|
| **All Upfront** | Highest | Requires capital | Enterprises with available cash |
| **Partial Upfront** | Medium | Balanced | Standard choice |
| **No Upfront** | Lower | Spreads cost | Startups, constrained cash flow |

**ROI Calculation:**
```
3-year EC2 m5.2xlarge RI (us-east-1):
├── On-demand cost: $0.384/hour × 8,760 hours/year × 3 years = $10,097
├── RI all upfront: $6,063 (40% discount)
├── RI no upfront: $7,152 (29% discount)
└── Savings: $4,034 (all upfront) vs. $2,945 (no upfront)

Extra $1,089 savings with all upfront payment.
```

---

## Monitoring and Optimization

### Track Utilization (Target >95%)

**AWS:**
```bash
aws ce get-reservation-utilization \
  --time-period Start=2025-12-01,End=2025-12-31 \
  --granularity MONTHLY
```

**Azure:**
```bash
az consumption reservation summary list \
  --reservation-order-id <order-id> \
  --grain daily
```

**GCP:**
```bash
gcloud billing accounts cud-analysis get \
  --billing-account=<account-id> \
  --start-date=2025-12-01 \
  --end-date=2025-12-31
```

### Quarterly Review Checklist

- [ ] Check RI/SP/CUD utilization (target >95%)
- [ ] Identify underutilized commitments (utilization <90%)
- [ ] Analyze new commitment opportunities (growing workloads)
- [ ] Review expiring commitments (renew or let expire)
- [ ] Adjust commitment sizes based on usage trends
- [ ] Sell unused RIs on marketplace (AWS only)

### Unused Commitment Actions

**Underutilized (<90% usage):**
1. **Modify instance family:** Exchange Convertible RI for different type
2. **Sell on marketplace:** AWS Reserved Instance Marketplace
3. **Repurpose:** Move commitment to different workload
4. **Accept loss:** If no alternatives, let expire at end of term

**Over-committed (running out of capacity):**
1. **Purchase additional commitments:** Top up with new RI/SP/CUD
2. **Use spot for overflow:** Spot instances for peak traffic
3. **Optimize existing:** Right-size to fit within commitments

---

## Common Mistakes

### Mistake 1: Over-Committing

❌ **Problem:** Purchased 3-year RIs for 200 vCPUs, usage dropped to 120 vCPUs
💰 **Cost:** Paying for 80 unused vCPUs ($10K/year wasted)

✅ **Solution:**
- Start with 1-year commitments for new workloads
- Commit to 80-85% of baseline (not average or peak)
- Review and expand commitments quarterly

### Mistake 2: Wrong Commitment Type

❌ **Problem:** Purchased Standard RIs for microservices that change instance types monthly
💰 **Cost:** RIs unused because workload migrated to different instance type

✅ **Solution:**
- Use Savings Plans for variable workloads (not RIs)
- Reserve Standard RIs for stable workloads only (databases)

### Mistake 3: Ignoring Regional Differences

❌ **Problem:** Purchased RIs in us-east-1, workload migrated to eu-west-1
💰 **Cost:** RIs unused, paying full on-demand in new region

✅ **Solution:**
- Purchase Compute Savings Plans (region-flexible)
- Or use Convertible RIs (can change region via exchange)

### Mistake 4: Not Monitoring Utilization

❌ **Problem:** RI utilization at 65%, wasting 35% of commitment
💰 **Cost:** $50K/year commitment, $17.5K wasted

✅ **Solution:**
- Weekly utilization reports (automated alerts)
- Quarterly commitment reviews
- Reallocate or sell unused commitments

### Mistake 5: All Upfront Without Cash Flow

❌ **Problem:** Purchased $500K all-upfront RIs, caused cash flow crunch
💰 **Cost:** Opportunity cost of capital tied up

✅ **Solution:**
- Use no upfront or partial upfront if cash flow constrained
- Balance discount savings vs. cash flow needs

---

## Commitment Strategy Examples

### Example 1: E-Commerce Platform

**Workload:**
- Production RDS PostgreSQL: 24/7 uptime, db.r5.4xlarge
- Web servers: Variable traffic (50-200 m5.large instances)
- Background jobs: Batch processing (10-30 c5.2xlarge instances)

**Commitment Strategy:**
```
1. RDS Database:
   ├── Purchase: db.r5.4xlarge Standard RI (3-year, all upfront)
   ├── Discount: 72% off on-demand
   └── Savings: $25,000/year

2. Web Servers:
   ├── Purchase: Compute Savings Plan (1-year, $5/hour)
   ├── Covers: Baseline 50 m5.large instances
   ├── Discount: 40% off on-demand
   └── Overflow: On-demand for traffic spikes

3. Batch Jobs:
   ├── Purchase: No commitment (use Spot instances)
   ├── Discount: 70-80% off on-demand via Spot
   └── Fallback: On-demand if Spot unavailable
```

### Example 2: SaaS Startup

**Workload:**
- Kubernetes cluster: 100-150 vCPUs (growing)
- PostgreSQL RDS: db.r5.xlarge (stable)
- Redis ElastiCache: cache.r5.large (stable)

**Commitment Strategy:**
```
1. Kubernetes (GKE):
   ├── Purchase: Spend-based CUD (1-year, $3/hour)
   ├── Covers: 100 vCPU baseline
   ├── Growth: Add commitments quarterly as usage grows
   └── Discount: 37% off on-demand

2. RDS + ElastiCache:
   ├── Purchase: Standard RIs (1-year, no upfront)
   ├── Reason: Startup cash flow constrained
   └── Discount: 40% off on-demand
```

### Example 3: Enterprise Multi-Cloud

**Workload:**
- AWS: 500 EC2 instances (mix of types)
- Azure: 200 VMs (Windows + Linux)
- GCP: 300 VMs (Compute Engine)

**Commitment Strategy:**
```
1. AWS:
   ├── Compute Savings Plans: $50/hour (covers 60% of usage)
   ├── Standard RIs: RDS, ElastiCache databases
   └── Spot: Batch workloads (30% of compute)

2. Azure:
   ├── Reserved VM Instances: $30/hour (covers 50% of usage)
   ├── Azure Hybrid Benefit: Windows VMs (bring licenses)
   └── Dev/Test Pricing: Non-prod environments

3. GCP:
   ├── Spend-based CUDs: $20/hour (covers 55% of usage)
   ├── Sustained Use Discounts: Automatic (no action needed)
   └── Preemptible VMs: 40% of workloads
```

---

## Commitment ROI Calculator

**Formula:**
```
Annual Savings = (On-Demand Cost - Commitment Cost) × Hours per Year

ROI % = (Annual Savings / Upfront Investment) × 100

Payback Period (months) = Upfront Investment / (Annual Savings / 12)
```

**Example:**
```
Workload: 10x m5.2xlarge instances (24/7)
On-Demand Cost: $0.384/hour × 10 instances × 8,760 hours = $33,638/year
Standard RI (3-year, all upfront): $20,210 total ($6,737/year)
Annual Savings: $33,638 - $6,737 = $26,901/year (80% reduction)
ROI: $26,901 / $20,210 = 133% over 3 years
Payback: $20,210 / ($26,901/12) = 9 months
```
