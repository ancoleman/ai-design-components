# Cost Optimization Skill - Master Plan

**Skill Name:** `cost-optimization`
**Level:** Mid (Implementation Patterns)
**Target SKILL.md Size:** 500-800 lines
**Research Date:** December 3, 2025
**Status:** Master Plan Complete → Ready for SKILL.md implementation

---

## Strategic Positioning

### Why FinOps is Critical in 2025

Cloud cost optimization has evolved from IT efficiency to **strategic business imperative**:

```
┌─────────────────────────────────────────────────────────┐
│      FinOps: From IT Cost to Business Strategy         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Global Cloud Waste Statistics (2025):                  │
│  ├── $61.3B in wasted cloud spend annually (Gartner)    │
│  ├── 32% average cloud waste rate (unused resources)    │
│  ├── 35% of cloud spend unallocated to business units   │
│  ├── 47% of organizations lack cost visibility tools    │
│  └── 3.2x cost increase YoY without optimization        │
│                                                          │
│  FinOps Maturity Impact:                                │
│  ├── Mature FinOps: 15-30% cost reduction achieved      │
│  ├── Real-time visibility: Prevent 80% of overruns      │
│  ├── Automated rightsizing: 40-60% savings on compute   │
│  ├── Commitment discounts: 30-72% savings vs. on-demand │
│  └── Culture shift: Cost = engineering metric           │
│                                                          │
│  The FinOps Lifecycle:                                  │
│  ┌─────────────────────────────────────────────┐        │
│  │  INFORM → OPTIMIZE → OPERATE (continuous)   │        │
│  │     ↓         ↓           ↓                  │        │
│  │  Visibility  Action   Automation             │        │
│  └─────────────────────────────────────────────┘        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Why This Matters Now:**
- **Board-Level Scrutiny:** Cloud spend is the #2 budget line item after headcount
- **Recession Readiness:** Economic uncertainty drives aggressive cost optimization
- **AI/ML Workloads:** GPU costs can exceed $100K/month without guardrails
- **Multi-Cloud Complexity:** Managing costs across AWS, Azure, GCP, and on-prem
- **Developer Ownership:** Shift-left cost accountability to engineering teams

**Integration with Other Skills:**
- **resource-tagging**: Tags enable cost allocation and budgeting
- **kubernetes-operations**: K8s cost optimization (rightsizing, spot nodes)
- **infrastructure-as-code**: Infracost for Terraform cost estimation
- **aws-patterns** / **gcp-patterns** / **azure-patterns**: Cloud-specific optimizations
- **platform-engineering**: Internal FinOps platforms and self-service tools

---

## Research Findings

### Google Search Grounding (December 2025)

**Query 1: "FinOps best practices 2025"**

**Core FinOps Principles (FinOps Foundation):**
1. **Collaboration** - Cross-functional teams (finance, engineering, operations, product)
2. **Accountability** - Clear ownership of cloud costs by teams
3. **Transparency** - All costs visible and understandable to stakeholders
4. **Optimization** - Continuous improvement of cost efficiency

**2025 Best Practices:**
- **Align Cloud Spend with Business Goals** - Cost metrics tied to business value
- **Real-Time Cost Visibility** - Dashboards for engineering teams (not just finance)
- **Single Source of Truth** - Unified cost data across all cloud providers
- **Showback/Chargeback Models** - Allocate costs to teams/departments
- **Automated Cost Controls** - Guardrails prevent overspend before it happens
- **Reserved Instance/Savings Plans Management** - Dynamic commitment optimization
- **Unit Cost Metrics** - Cost per transaction, cost per customer (business metrics)
- **Budget Alerts & Guardrails** - Proactive notifications and enforcement
- **Regular Cloud Spend Audits** - Weekly/monthly cost reviews with stakeholders
- **FinOps Culture Education** - Cost awareness across all levels

**Query 2: "cloud cost optimization strategies 2025"**

**Key Optimization Strategies:**

1. **Gain Full Cost Visibility**
   - Native tools: AWS Cost Explorer, Azure Cost Management, GCP Cloud Billing
   - Third-party: Kubecost, CloudHealth, Apptio Cloudability, CloudZero
   - AI-driven observability: Anomaly detection, forecasting, waste identification

2. **Establish Cost Governance**
   - Define ownership rules and per-project/per-department budgets
   - Enforce tagging policies (cost allocation tags)
   - Cloud-native guardrails: AWS Budgets, Azure Policy, GCP Budgets
   - FinOps team structure (cross-functional)

3. **Optimize Resource Utilization**
   - Turn off idle resources (dev/test environments)
   - Right-size compute resources (match workload to instance type)
   - Implement autoscaling (scale down during low demand)
   - Leverage spot instances/preemptible VMs (70-90% discount)

4. **Storage Cost Optimization**
   - Tiered storage strategies (hot/cool/archive)
   - Lifecycle policies (automatic tier migration)
   - Automated cleanup (delete unattached volumes, old snapshots)

5. **Network & Data Transfer Costs**
   - Keep data processing in same region (minimize egress)
   - Use CDNs (CloudFront, Azure CDN) for static content
   - Compress payloads and optimize API calls

6. **Commitment-Based Discounts**
   - Reserved Instances (1-year or 3-year commitments)
   - Savings Plans (flexible compute commitments)
   - Committed Use Discounts (GCP)
   - Spot Instances for fault-tolerant workloads

7. **Automation & Monitoring**
   - Automate shutdown of idle resources
   - Continuous monitoring with alerts
   - AI-driven automation for optimization decisions

8. **Cloud Architecture Optimization**
   - Serverless and managed services (reduce operational overhead)
   - Multi-cloud strategy (avoid vendor lock-in, optimize costs)

**Top Cloud Cost Management Tools (2025):**
- **Kubecost** - Kubernetes cost visibility and optimization
- **Infracost** - Terraform cost estimation in CI/CD
- **CloudPilot AI** - Intelligent K8s cost optimization
- **AWS Cost Explorer** - Native AWS cost analysis
- **Azure Cost Management** - Native Azure cost tracking
- **Google Cloud Cost Management** - Native GCP billing analysis
- **CloudZero** - Unit cost economics and anomaly detection
- **Spot by NetApp** - Automated spot instance management
- **nOps** - AWS cost optimization with automation
- **Harness CCM** - Cloud cost management with BI capabilities

### Context7 Research: Kubecost

**Library:** IBM Kubecost Self-Hosted 3.x
**Trust Score:** High (IBM documentation)
**Code Snippets:** 655

**Key Kubecost Concepts:**

1. **Cost Allocation**
   - Allocates costs by namespace, deployment, service, label, annotation
   - Based on max(requests, usage) for CPU/memory/GPU
   - Idle cost allocation: Distributes unallocated cluster capacity

2. **Efficiency Metrics**
   - **Workload Idle**: Resources requested but not used (waste)
   - **Infra Idle**: Cluster capacity not allocated to workloads
   - **Cluster Efficiency**: (cost of resources used) / (total cost)

3. **Cost Monitoring APIs**
   - Allocation API: Cost breakdown by any K8s concept
   - Assets API: Infrastructure costs (nodes, disks, network)
   - Cloud Costs API: External cloud costs (integrated with cloud bills)
   - Trends API: Cost comparisons over time

4. **Optimization Features**
   - Node group sizing recommendations
   - Container rightsizing suggestions
   - Anomaly detection and budget alerts
   - Showback/chargeback reporting

**Use Cases:**
- Real-time Kubernetes cost visibility
- Multi-cluster cost aggregation
- Cost allocation for internal chargebacks
- Optimization recommendations (rightsizing, spot nodes)

### Context7 Research: Infracost

**Library:** Infracost (GitHub)
**Trust Score:** High
**Code Snippets:** 69

**Key Infracost Capabilities:**

1. **Terraform Cost Estimation**
   - Estimates cloud costs before infrastructure changes
   - Integrates with terminal, VS Code, and pull requests
   - Supports AWS, Azure, GCP pricing

2. **CI/CD Integration**
   - Pull request comments with cost diffs
   - Prevents surprise cost increases
   - Cost breakdowns by resource type

3. **FinOps Best Practices**
   - Shift-left cost awareness (developers see costs early)
   - Usage-based cost components (data transfer, storage tiers)
   - Cost component breakdown (hourly, monthly costs)

**Implementation Pattern:**
```go
// Cost component structure
&schema.CostComponent{
  Name:           "Protocol enabled",
  Unit:           "hours",
  UnitMultiplier: decimal.NewFromInt(1),
  HourlyQuantity: decimalPtr(decimal.NewFromInt(1)),
  ProductFilter: &schema.ProductFilter{
    VendorName:    "aws",
    Region:        region,
    Service:       "AWSTransfer",
    ProductFamily: "AWS Transfer Family",
  }
}
```

**Use Cases:**
- Terraform cost estimation in CI/CD pipelines
- Pull request cost impact visibility
- Infrastructure cost planning and budgeting
- Multi-cloud cost forecasting

---

## Component Taxonomy

### 1. Cost Visibility (INFORM Phase)

```
┌─────────────────────────────────────────────────────────┐
│             Cost Visibility Architecture                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. TAGGING & ALLOCATION                                │
│     ├── Cost Allocation Tags (Owner, Project, Env)      │
│     ├── Showback (informational cost reports)           │
│     ├── Chargeback (actual billing to teams)            │
│     └── Unit Economics (cost per customer/transaction)  │
│                                                          │
│  2. MONITORING & DASHBOARDS                             │
│     ├── Real-time cost tracking                         │
│     ├── Anomaly detection (ML-based)                    │
│     ├── Budget alerts (threshold notifications)         │
│     └── Custom dashboards (per team/project)            │
│                                                          │
│  3. CLOUD BILLING INTEGRATION                           │
│     ├── AWS Cost & Usage Reports (CUR)                  │
│     ├── Azure Consumption API                           │
│     ├── GCP BigQuery Billing Export                     │
│     └── Multi-cloud aggregation                         │
│                                                          │
│  4. KUBERNETES COST VISIBILITY                          │
│     ├── Kubecost / OpenCost                             │
│     ├── Namespace-level cost allocation                 │
│     ├── Pod-level resource usage                        │
│     └── Idle capacity tracking                          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Visibility Tools by Cloud:**

| Cloud | Native Tool | Third-Party |
|-------|-------------|-------------|
| **AWS** | Cost Explorer, CUR, Budgets | CloudZero, nOps, CloudHealth |
| **Azure** | Cost Management + Billing | Apptio Cloudability, Spot.io |
| **GCP** | Cloud Billing, Recommender | CloudHealth, Finout |
| **Kubernetes** | kubectl top, metrics-server | Kubecost, OpenCost, CloudPilot AI |

### 2. Commitment Discounts (OPTIMIZE Phase)

```
┌─────────────────────────────────────────────────────────┐
│          Commitment-Based Discount Strategies           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  AWS DISCOUNTS                                          │
│  ├── Reserved Instances (EC2, RDS, ElastiCache)         │
│  │   ├── Standard RI: 1-year (40% off) / 3-year (60%)   │
│  │   ├── Convertible RI: Flexible instance type         │
│  │   └── Payment: All upfront, partial, no upfront      │
│  ├── Savings Plans                                      │
│  │   ├── Compute Savings Plans (EC2, Fargate, Lambda)   │
│  │   │   └── 1-year: 17% | 3-year: 54% savings          │
│  │   └── EC2 Instance Savings Plans                     │
│  │       └── 1-year: 28% | 3-year: 66% savings          │
│  └── Spot Instances: 70-90% discount (interruptible)    │
│                                                          │
│  AZURE DISCOUNTS                                        │
│  ├── Reserved VM Instances (1-year: 40% | 3-year: 62%)  │
│  ├── Azure Hybrid Benefit (bring Windows licenses)      │
│  ├── Spot VMs (up to 90% discount)                      │
│  └── Dev/Test Pricing (non-production workloads)        │
│                                                          │
│  GCP DISCOUNTS                                          │
│  ├── Committed Use Discounts (CUDs)                     │
│  │   ├── 1-year: 25-37% | 3-year: 52-70% savings        │
│  │   ├── Resource-based CUDs (vCPU, memory, GPU)        │
│  │   └── Spend-based CUDs (flexible)                    │
│  ├── Sustained Use Discounts (automatic, no commitment) │
│  │   └── 20-30% discount for sustained usage            │
│  └── Preemptible VMs (up to 91% discount)               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Decision Framework: When to Commit?**

```
Reserve when:
├─→ Workload is production-critical (24/7 uptime)
├─→ Usage is predictable (stable baseline over 6+ months)
├─→ Architecture is unlikely to change (stable instance types)
└─→ Financial commitment acceptable (1-3 year lock-in)

Use Spot/Preemptible when:
├─→ Workload is fault-tolerant (can handle interruptions)
├─→ Stateless applications (no data loss risk)
├─→ Batch jobs, CI/CD runners, data processing
└─→ Kubernetes nodes (with fallback to on-demand)

Use On-Demand when:
├─→ Development/testing environments
├─→ Unpredictable spiky workloads
├─→ Short-term projects (<6 months)
└─→ Evaluating new instance types
```

### 3. Right-Sizing Strategies

```
┌─────────────────────────────────────────────────────────┐
│              Resource Right-Sizing Framework            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  COMPUTE RIGHT-SIZING                                   │
│  ├── Analyze actual CPU/memory utilization (30 days+)   │
│  ├── Target: 60-80% average utilization (headroom)      │
│  ├── Downsize over-provisioned instances                │
│  ├── Consolidate underutilized workloads                │
│  └── Switch instance families (compute vs. memory opt)  │
│                                                          │
│  DATABASE RIGHT-SIZING                                  │
│  ├── Connection pool analysis (max connections used)    │
│  ├── Storage IOPS utilization (downgrade if <50%)       │
│  ├── Read replica necessity (can use cache instead?)    │
│  └── Serverless option evaluation (Aurora Serverless)   │
│                                                          │
│  KUBERNETES RIGHT-SIZING                                │
│  ├── Set requests = avg usage (not peak)                │
│  ├── Set limits = 2x requests (allow bursting)          │
│  ├── Use VPA for automated rightsizing                  │
│  └── Identify pods with 0% CPU usage (candidates for    │
│      consolidation or removal)                          │
│                                                          │
│  STORAGE RIGHT-SIZING                                   │
│  ├── Identify unattached volumes (delete)               │
│  ├── Delete old snapshots (>90 days, not needed)        │
│  ├── Use lifecycle policies (S3 Intelligent-Tiering)    │
│  └── Compress/deduplicate data                          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Right-Sizing Tools:**

| Platform | Tool | Capability |
|----------|------|------------|
| **AWS** | AWS Compute Optimizer | ML-based EC2, Lambda, EBS recommendations |
| **Azure** | Azure Advisor | VM rightsizing, reserved instance advice |
| **GCP** | GCP Recommender | VM, disk, commitment recommendations |
| **Kubernetes** | VPA (Vertical Pod Autoscaler) | Automated container resource requests |
| **Multi-Cloud** | CloudHealth, Densify | Cross-cloud rightsizing analysis |

### 4. Spot & Preemptible Instance Strategies

```
┌─────────────────────────────────────────────────────────┐
│         Spot/Preemptible Instance Best Practices        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  WHEN TO USE SPOT/PREEMPTIBLE                           │
│  ✅ CI/CD build workers (can retry on interruption)     │
│  ✅ Batch processing jobs (stateless, resumable)        │
│  ✅ ML training (checkpointing enabled)                 │
│  ✅ Kubernetes worker nodes (with fallback)             │
│  ✅ Data analytics (Spark, Hadoop clusters)             │
│  ✅ Rendering farms (video/image processing)            │
│                                                          │
│  WHEN NOT TO USE SPOT/PREEMPTIBLE                       │
│  ❌ Stateful databases (data loss risk)                 │
│  ❌ Real-time user-facing services (uptime critical)    │
│  ❌ Long-running jobs without checkpointing             │
│  ❌ Workloads requiring 99.9%+ availability             │
│                                                          │
│  SPOT INSTANCE PATTERNS                                 │
│  ├── Diversification: Use multiple instance types       │
│  ├── Availability Zones: Spread across AZs              │
│  ├── Fallback Strategy: Auto-fallback to on-demand      │
│  ├── Graceful Shutdown: Handle termination notices      │
│  └── Capacity Pools: Use lowest price pools             │
│                                                          │
│  KUBERNETES SPOT NODE POOLS                             │
│  ├── Use node autoscaling (scale to zero when idle)     │
│  ├── Mix spot + on-demand nodes (e.g., 70% spot)        │
│  ├── Taints/tolerations (route workloads appropriately) │
│  └── Pod Disruption Budgets (ensure availability)       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Spot Management Tools:**
- **AWS**: EC2 Spot Fleet, EKS managed node groups with spot
- **Azure**: Azure Spot VMs, AKS spot node pools
- **GCP**: Preemptible VMs, GKE spot node pools
- **Third-Party**: Spot.io, CAST AI (Kubernetes spot optimization)

### 5. Kubernetes Cost Management

```
┌─────────────────────────────────────────────────────────┐
│          Kubernetes Cost Optimization Strategies        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. RESOURCE REQUESTS & LIMITS                          │
│     ├── Set requests = average usage (not peak)         │
│     ├── Set limits = 2-3x requests (burst headroom)     │
│     ├── Avoid missing requests (causes bin-packing issues)│
│     └── Use VPA for automated recommendations           │
│                                                          │
│  2. NAMESPACE QUOTAS                                    │
│     ├── Prevent runaway resource consumption            │
│     ├── ResourceQuota: Limit total CPU/memory per NS    │
│     ├── LimitRange: Default/max requests per pod        │
│     └── PriorityClass: Ensure critical pods get resources│
│                                                          │
│  3. CLUSTER AUTOSCALING                                 │
│     ├── Scale down idle nodes (cost savings)            │
│     ├── Scale-to-zero for dev clusters (off-hours)      │
│     ├── Use multiple node pools (spot + on-demand mix)  │
│     └── Set max node limits (prevent overspend)         │
│                                                          │
│  4. WORKLOAD SCHEDULING                                 │
│     ├── Topology spread constraints (zone distribution) │
│     ├── Bin packing (maximize node utilization)         │
│     ├── Pod priority/preemption (critical workloads)    │
│     └── Affinity/anti-affinity (co-locate related pods) │
│                                                          │
│  5. COST VISIBILITY & ALLOCATION                        │
│     ├── Kubecost / OpenCost integration                 │
│     ├── Namespace-level cost tracking                   │
│     ├── Label-based cost allocation (team, project)     │
│     └── Idle cost attribution (distribute fairly)       │
│                                                          │
│  6. STORAGE OPTIMIZATION                                │
│     ├── Delete unused PVCs (orphaned volumes)           │
│     ├── Use appropriate StorageClasses (SSD vs. HDD)    │
│     ├── Set volume reclaim policies (Delete vs. Retain) │
│     └── Monitor storage IOPS (overpaying for unused?)   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Kubernetes Cost Tools:**
- **Kubecost** (commercial, free tier) - Most comprehensive K8s cost platform
- **OpenCost** (open-source) - CNCF project for Kubernetes cost monitoring
- **CloudPilot AI** - AI-powered K8s cost optimization
- **CAST AI** - Automated K8s cost optimization with autoscaling

### 6. FinOps Team Structure

```
┌─────────────────────────────────────────────────────────┐
│              FinOps Operating Model (2025)              │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  CENTRALIZED FINOPS TEAM                                │
│  ├── FinOps Lead (cross-functional coordination)        │
│  ├── Cloud Financial Analyst (cost analysis, reporting) │
│  ├── Cloud Architect (technical optimization advice)    │
│  ├── Automation Engineer (tooling, guardrails)          │
│  └── Finance Partner (budgeting, forecasting)           │
│                                                          │
│  STAKEHOLDER ROLES                                      │
│  ├── Engineering Teams                                  │
│  │   └── Own cost of their services (accountability)    │
│  ├── Finance Department                                 │
│  │   └── Budget allocation and variance tracking        │
│  ├── Product Management                                 │
│  │   └── Cost vs. feature prioritization                │
│  └── Executive Leadership                               │
│      └── Strategic cloud investment decisions           │
│                                                          │
│  FINOPS PRACTICES                                       │
│  ├── Weekly Cost Reviews (all teams)                    │
│  ├── Monthly Optimization Sprints (top 10 cost drivers) │
│  ├── Quarterly Budget Planning (forecast vs. actual)    │
│  ├── On-Call Cost Alerts (anomaly response)             │
│  └── Continuous Education (FinOps training programs)    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**FinOps Maturity Levels:**

| Level | Characteristics | Cost Savings Potential |
|-------|----------------|------------------------|
| **Crawl** | Manual reporting, reactive | 5-10% reduction |
| **Walk** | Automated dashboards, proactive | 15-25% reduction |
| **Run** | Predictive, culture embedded | 25-40% reduction |

---

## Decision Frameworks

### Framework 1: Commitment Discount Strategy

```
SCENARIO: Should we purchase Reserved Instances / Savings Plans?
│
├─→ STEP 1: Analyze Historical Usage (6-12 months)
│   ├─ Identify steady-state baseline (minimum usage)
│   ├─ Exclude spiky/seasonal workloads
│   └─ Calculate: (baseline usage) / (total usage) = commitment %
│
├─→ STEP 2: Choose Commitment Type
│   ├─ RESERVED INSTANCES
│   │   ├─ Pros: Highest discount (up to 72%)
│   │   ├─ Cons: Instance type locked (unless convertible)
│   │   └─ Use for: Databases, stable production workloads
│   │
│   ├─ SAVINGS PLANS
│   │   ├─ Pros: Flexible (across instance types, regions)
│   │   ├─ Cons: Slightly lower discount than RI
│   │   └─ Use for: Compute workloads, Lambda, Fargate
│   │
│   └─ COMMITTED USE DISCOUNTS (GCP)
│       ├─ Resource-based: vCPU/memory commitments
│       └─ Spend-based: Dollar amount commitments
│
├─→ STEP 3: Determine Commitment Period
│   ├─ 1-year commitment
│   │   ├─ Lower discount (40-50%)
│   │   └─ Less risk if architecture changes
│   │
│   └─ 3-year commitment
│       ├─ Higher discount (60-72%)
│       └─ Only for mature, stable workloads
│
├─→ STEP 4: Payment Option
│   ├─ All Upfront: Highest discount, requires capital
│   ├─ Partial Upfront: Balanced discount, split payment
│   └─ No Upfront: Lower discount, pay monthly
│
└─→ STEP 5: Continuous Optimization
    ├─ Monitor utilization (target >95% RI/SP usage)
    ├─ Sell unused RIs (AWS Reserved Instance Marketplace)
    └─ Adjust commitments quarterly based on trends
```

### Framework 2: Spot vs. On-Demand Decision Tree

```
QUESTION: Should this workload use Spot/Preemptible instances?
│
├─→ Is the workload fault-tolerant?
│   ├─ NO → Use On-Demand (spot interruptions unacceptable)
│   └─ YES → Continue to next question
│
├─→ Is the workload stateless (or has checkpointing)?
│   ├─ NO → Use On-Demand (data loss risk)
│   └─ YES → Continue to next question
│
├─→ Can the workload handle interruptions gracefully?
│   ├─ NO → Use On-Demand
│   └─ YES → Continue to next question
│
├─→ Is availability requirement <99%?
│   ├─ NO → Use On-Demand (or mixed fleet)
│   └─ YES → Continue to next question
│
├─→ Workload Type Assessment:
│   ├─ Batch Jobs / CI/CD → ✅ Use Spot (70-90% savings)
│   ├─ ML Training → ✅ Use Spot (with checkpointing)
│   ├─ Kubernetes Workers → ✅ Use Spot (mixed with on-demand)
│   ├─ Development Environments → ✅ Use Spot
│   ├─ Production API Servers → ⚠️  Mixed fleet (70% spot, 30% on-demand)
│   ├─ Databases → ❌ Use On-Demand (or Reserved)
│   └─ Real-time Services → ❌ Use On-Demand (or Reserved)
│
└─→ IMPLEMENTATION PATTERN
    ├─ Diversify instance types (multiple families)
    ├─ Spread across Availability Zones
    ├─ Implement termination handlers (graceful shutdown)
    ├─ Set up fallback to on-demand (auto-recovery)
    └─ Monitor interruption rate (if >10%, reconsider)
```

### Framework 3: Right-Sizing Priority Matrix

```
PRIORITY: Which resources to right-size first?
│
COST IMPACT vs. EFFORT MATRIX:
│
High Impact, Low Effort (DO FIRST):
├─→ Idle resources (100% waste)
│   ├─ Stopped EC2 instances (still charged for EBS)
│   ├─ Unattached EBS volumes
│   ├─ Old snapshots (>90 days)
│   └─ Unused NAT Gateways ($0.045/hour = $32/month each)
│
├─→ Over-provisioned databases
│   ├─ RDS instances at <20% CPU for 30 days
│   ├─ High IOPS storage with low utilization
│   └─ Unnecessary read replicas (can use caching?)
│
└─→ Kubernetes pods with no requests set
    ├─ Causes inefficient bin-packing
    └─ Use VPA to auto-generate recommendations

High Impact, Medium Effort (DO SECOND):
├─→ Over-provisioned compute instances
│   ├─ EC2/VM instances at <40% CPU/memory for 30 days
│   ├─ Lambda functions with max memory >2x used memory
│   └─ ECS/Fargate tasks with oversized CPU/memory
│
└─→ Storage optimization
    ├─ S3 buckets (enable Intelligent-Tiering)
    ├─ EBS volumes (gp3 vs. gp2 savings)
    └─ Archive old logs to Glacier/Archive Storage

Low Impact, High Effort (DO LAST):
├─→ Application code optimization
│   ├─ Requires profiling and refactoring
│   └─ Long-term investment, not quick win
│
└─→ Architecture redesign
    ├─ Serverless migration
    └─ Multi-region optimization

WEEKLY OPTIMIZATION ROUTINE:
1. Delete idle resources (automated script)
2. Review top 10 cost drivers (manual analysis)
3. Right-size 3-5 instances/week (incremental)
4. Monitor impact (cost trend over 4 weeks)
```

### Framework 4: Budget Alert Strategy

```
QUESTION: How to set up effective budget alerts?
│
├─→ BUDGET LEVELS (Cascading Alerts)
│   ├─ 50% of monthly budget
│   │   └─ Alert: Email to team lead (informational)
│   ├─ 75% of monthly budget
│   │   └─ Alert: Email + Slack to team (warning)
│   ├─ 90% of monthly budget
│   │   └─ Alert: Email + Slack + PagerDuty (urgent)
│   └─ 100% of monthly budget
│       └─ Action: Trigger automated shutdown (non-prod only)
│
├─→ BUDGET GRANULARITY
│   ├─ Organization-level (total cloud spend)
│   ├─ Department-level (engineering, data, marketing)
│   ├─ Project-level (per application/service)
│   └─ Environment-level (prod vs. dev/staging)
│
├─→ ANOMALY DETECTION ALERTS
│   ├─ >20% cost increase WoW (week-over-week)
│   ├─ >$500 unexpected daily cost spike
│   └─ New resource types (unusual spend patterns)
│
└─→ RESPONSE PLAYBOOK
    ├─ Investigate: Which service/resource?
    ├─ Root cause: Why the increase?
    ├─ Triage: Legitimate growth or waste?
    ├─ Action: Optimize, scale down, or accept
    └─ Document: Add to cost review notes
```

---

## Implementation Patterns

### Pattern 1: AWS Cost Optimization Stack (Terraform)

```hcl
# terraform/aws-cost-optimization.tf

# Enable Cost Allocation Tags
resource "aws_ce_cost_allocation_tag" "environment" {
  tag_key = "Environment"
  status  = "Active"
}

resource "aws_ce_cost_allocation_tag" "project" {
  tag_key = "Project"
  status  = "Active"
}

# Budget with Alerts
resource "aws_budgets_budget" "monthly_cost" {
  name              = "monthly-cloud-budget"
  budget_type       = "COST"
  limit_amount      = var.monthly_budget
  limit_unit        = "USD"
  time_period_start = "2025-12-01_00:00"
  time_unit         = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 50
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.team_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 75
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.team_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 90
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.oncall_email]
    subscriber_sns_topic_arns  = [aws_sns_topic.cost_alerts.arn]
  }
}

# Cost Anomaly Monitor
resource "aws_ce_anomaly_monitor" "service_monitor" {
  name              = "service-cost-anomaly-monitor"
  monitor_type      = "DIMENSIONAL"
  monitor_dimension = "SERVICE"
}

resource "aws_ce_anomaly_subscription" "anomaly_alerts" {
  name      = "cost-anomaly-alerts"
  frequency = "IMMEDIATE"

  monitor_arn_list = [
    aws_ce_anomaly_monitor.service_monitor.arn
  ]

  subscriber {
    type    = "SNS"
    address = aws_sns_topic.cost_alerts.arn
  }

  threshold_expression {
    dimension {
      key           = "ANOMALY_TOTAL_IMPACT_PERCENTAGE"
      values        = ["20"]
      match_options = ["GREATER_THAN_OR_EQUAL"]
    }
  }
}

# SNS Topic for Cost Alerts
resource "aws_sns_topic" "cost_alerts" {
  name = "cloud-cost-alerts"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.cost_alerts.arn
  protocol  = "email"
  endpoint  = var.finops_team_email
}

resource "aws_sns_topic_subscription" "slack" {
  topic_arn = aws_sns_topic.cost_alerts.arn
  protocol  = "https"
  endpoint  = var.slack_webhook_url
}
```

### Pattern 2: Kubernetes Cost Visibility (Kubecost)

```yaml
# kubecost-values.yaml
# Helm chart: kubecost/cost-analyzer

kubecostProductConfigs:
  # Cloud integration for accurate pricing
  cloudIntegrationSecret: cloud-integration

  # Cost allocation by labels
  labelMappingConfigs:
    enabled: true
    owner_label: "team"
    product_label: "product"
    department_label: "department"
    environment_label: "environment"

# Enable multi-cluster aggregation
kubecostAggregator:
  enabled: true

# Prometheus integration (cost metrics)
prometheus:
  server:
    persistentVolume:
      enabled: true
      size: 100Gi
    retention: 30d

# Budget alerts
notifications:
  alertConfigs:
    enabled: true
    frontendUrl: https://kubecost.company.com
    globalSlackWebhookUrl: ${SLACK_WEBHOOK}
    alerts:
      - type: budget
        threshold: 1000  # USD
        window: 1d
        aggregation: namespace
        filter: environment=prod

# Recommendations engine
recommendations:
  enabled: true
  containerResourceRequests:
    enabled: true
    targetCPUUtilization: 0.65
    targetRAMUtilization: 0.80
```

**Deploy Kubecost:**
```bash
helm repo add kubecost https://kubecost.github.io/cost-analyzer/
helm repo update

helm install kubecost kubecost/cost-analyzer \
  --namespace kubecost \
  --create-namespace \
  --values kubecost-values.yaml \
  --set kubecostToken="<your-token>"
```

### Pattern 3: Infracost in CI/CD (GitHub Actions)

```yaml
# .github/workflows/infracost.yml
name: Terraform Cost Estimation

on:
  pull_request:
    paths:
      - 'terraform/**'

jobs:
  infracost:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3

      - name: Setup Infracost
        uses: infracost/actions/setup@v3
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}

      - name: Terraform Init
        run: terraform init
        working-directory: terraform/

      - name: Terraform Plan (JSON)
        run: terraform plan -out=tfplan.binary && terraform show -json tfplan.binary > plan.json
        working-directory: terraform/

      - name: Generate Infracost Diff
        run: |
          infracost diff \
            --path=terraform/plan.json \
            --format=json \
            --out-file=/tmp/infracost.json

      - name: Post Infracost Comment
        uses: infracost/actions/comment@v3
        with:
          path: /tmp/infracost.json
          behavior: update

      - name: Fail if cost increase > $500/month
        run: |
          MONTHLY_DIFF=$(jq '.diffTotalMonthlyCost | tonumber' /tmp/infracost.json)
          if (( $(echo "$MONTHLY_DIFF > 500" | bc -l) )); then
            echo "Cost increase >$500/month requires approval"
            exit 1
          fi
```

### Pattern 4: Automated Idle Resource Cleanup (AWS Lambda)

```python
# lambda_function.py - Cleanup idle resources

import boto3
from datetime import datetime, timedelta

ec2 = boto3.client('ec2')
rds = boto3.client('rds')
cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    """
    Cleanup idle AWS resources to reduce costs.
    Run weekly via CloudWatch Events.
    """

    cleanup_results = {
        'unattached_volumes': cleanup_unattached_ebs(),
        'old_snapshots': cleanup_old_snapshots(),
        'stopped_instances': cleanup_stopped_instances(),
        'idle_load_balancers': cleanup_idle_load_balancers(),
    }

    return cleanup_results

def cleanup_unattached_ebs():
    """Delete EBS volumes not attached to any instance for >7 days"""
    volumes = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )['Volumes']

    deleted = []
    for volume in volumes:
        create_time = volume['CreateTime'].replace(tzinfo=None)
        if (datetime.now() - create_time).days > 7:
            # Check for 'KeepAlive' tag
            tags = {tag['Key']: tag['Value'] for tag in volume.get('Tags', [])}
            if tags.get('KeepAlive') != 'true':
                ec2.delete_volume(VolumeId=volume['VolumeId'])
                deleted.append(volume['VolumeId'])

    return {'count': len(deleted), 'volume_ids': deleted}

def cleanup_old_snapshots():
    """Delete snapshots older than 90 days (unless tagged)"""
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']

    deleted = []
    for snapshot in snapshots:
        start_time = snapshot['StartTime'].replace(tzinfo=None)
        if (datetime.now() - start_time).days > 90:
            tags = {tag['Key']: tag['Value'] for tag in snapshot.get('Tags', [])}
            if tags.get('Retain') != 'true':
                ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                deleted.append(snapshot['SnapshotId'])

    return {'count': len(deleted), 'snapshot_ids': deleted}

def cleanup_stopped_instances():
    """Alert on EC2 instances stopped for >14 days"""
    instances = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]
    )

    alerts = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            # Check how long instance has been stopped
            state_transition = instance['StateTransitionReason']
            # Example: "User initiated (2025-11-15 14:30:00 GMT)"
            # Parse and check if >14 days

            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            alerts.append({
                'instance_id': instance['InstanceId'],
                'name': tags.get('Name', 'N/A'),
                'owner': tags.get('Owner', 'unknown'),
            })

    return {'count': len(alerts), 'instances': alerts}

def cleanup_idle_load_balancers():
    """Alert on load balancers with 0 active connections for 7 days"""
    elb = boto3.client('elbv2')
    load_balancers = elb.describe_load_balancers()['LoadBalancers']

    idle = []
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)

    for lb in load_balancers:
        lb_arn = lb['LoadBalancerArn']

        # Check ActiveConnectionCount metric
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/ApplicationELB',
            MetricName='ActiveConnectionCount',
            Dimensions=[{'Name': 'LoadBalancer', 'Value': lb_arn.split('/')[-1]}],
            StartTime=start_time,
            EndTime=end_time,
            Period=86400,  # 1 day
            Statistics=['Maximum']
        )

        max_connections = max([dp['Maximum'] for dp in response['Datapoints']], default=0)
        if max_connections == 0:
            idle.append({
                'name': lb['LoadBalancerName'],
                'arn': lb_arn,
                'cost_estimate_monthly': 18.25  # $0.025/hour * 730 hours
            })

    return {'count': len(idle), 'load_balancers': idle}
```

**CloudFormation to deploy Lambda:**
```yaml
# cleanup-lambda.yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  CleanupFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: cost-optimization-cleanup
      Runtime: python3.11
      Handler: lambda_function.lambda_handler
      Timeout: 300
      Role: !GetAtt CleanupRole.Arn
      Code:
        S3Bucket: !Ref LambdaCodeBucket
        S3Key: cleanup.zip

  CleanupSchedule:
    Type: AWS::Events::Rule
    Properties:
      ScheduleExpression: 'cron(0 2 ? * SUN *)'  # Every Sunday 2 AM UTC
      State: ENABLED
      Targets:
        - Arn: !GetAtt CleanupFunction.Arn
          Id: CleanupFunctionTarget

  CleanupRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: CleanupPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - ec2:DescribeVolumes
                  - ec2:DeleteVolume
                  - ec2:DescribeSnapshots
                  - ec2:DeleteSnapshot
                  - ec2:DescribeInstances
                  - elasticloadbalancing:DescribeLoadBalancers
                  - cloudwatch:GetMetricStatistics
                Resource: '*'
```

### Pattern 5: GCP Cost Optimization (Terraform)

```hcl
# terraform/gcp-cost-optimization.tf

# Enable Billing Export to BigQuery
resource "google_bigquery_dataset" "billing_export" {
  dataset_id = "cloud_billing_export"
  location   = "US"

  labels = {
    environment = "production"
    purpose     = "cost-analysis"
  }
}

# Budget with Alerts
resource "google_billing_budget" "project_budget" {
  billing_account = var.billing_account_id
  display_name    = "Project Monthly Budget"

  budget_filter {
    projects = ["projects/${var.project_id}"]
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units         = var.monthly_budget
    }
  }

  threshold_rules {
    threshold_percent = 0.5  # 50%
  }

  threshold_rules {
    threshold_percent = 0.75  # 75%
  }

  threshold_rules {
    threshold_percent = 0.9  # 90%
    spend_basis       = "CURRENT_SPEND"
  }

  threshold_rules {
    threshold_percent = 1.0  # 100%
    spend_basis       = "FORECASTED_SPEND"
  }

  all_updates_rule {
    monitoring_notification_channels = [
      google_monitoring_notification_channel.email.id,
      google_monitoring_notification_channel.slack.id,
    ]
    disable_default_iam_recipients = false
  }
}

# Email Notification Channel
resource "google_monitoring_notification_channel" "email" {
  display_name = "FinOps Team Email"
  type         = "email"
  labels = {
    email_address = var.finops_team_email
  }
}

# Slack Notification Channel
resource "google_monitoring_notification_channel" "slack" {
  display_name = "FinOps Slack Channel"
  type         = "slack"
  labels = {
    channel_name = "#cloud-costs"
  }
  sensitive_labels {
    auth_token = var.slack_auth_token
  }
}

# Recommender: Idle VM instances
resource "google_project_service" "recommender" {
  service = "recommender.googleapis.com"
}

# Cloud Function to auto-apply low-risk recommendations
resource "google_cloudfunctions_function" "recommender_automation" {
  name        = "apply-cost-recommendations"
  runtime     = "python311"
  entry_point = "apply_recommendations"

  event_trigger {
    event_type = "google.cloud.scheduler.job.run"
    resource   = google_cloud_scheduler_job.weekly_recommendations.name
  }

  source_archive_bucket = google_storage_bucket.functions.name
  source_archive_object = google_storage_bucket_object.function_code.name
}

# Schedule weekly recommendation checks
resource "google_cloud_scheduler_job" "weekly_recommendations" {
  name     = "weekly-cost-recommendations"
  schedule = "0 2 * * 0"  # Every Sunday 2 AM

  http_target {
    uri         = google_cloudfunctions_function.recommender_automation.https_trigger_url
    http_method = "POST"
  }
}
```

---

## Tool Recommendations

### Cost Visibility Platforms

| Tool | Platform | Strengths | Best For |
|------|----------|-----------|----------|
| **Kubecost** | Kubernetes | Real-time K8s cost allocation, showback/chargeback | Teams running Kubernetes clusters |
| **OpenCost** | Kubernetes | Open-source K8s cost monitoring, CNCF project | Budget-conscious K8s users |
| **Infracost** | Terraform | IaC cost estimation in CI/CD, shift-left | Platform teams using Terraform |
| **CloudZero** | Multi-cloud | Unit cost economics, anomaly detection | SaaS companies tracking COGS |
| **CloudHealth** | Multi-cloud | Comprehensive multi-cloud cost management | Enterprises with AWS/Azure/GCP |
| **nOps** | AWS | Automated AWS cost optimization, ShareSave | AWS-heavy organizations |
| **Azure Cost Management** | Azure | Native Azure cost tracking, budgets | Azure-focused teams |
| **GCP Billing** | GCP | Native GCP cost analysis, recommender | GCP-centric organizations |

### Automation & Optimization Tools

| Tool | Use Case | Capability |
|------|----------|------------|
| **AWS Compute Optimizer** | EC2 rightsizing | ML-based instance recommendations |
| **Azure Advisor** | Multi-service optimization | VM, disk, reserved instance advice |
| **GCP Recommender** | GCP optimization | Idle resource detection, commitment advice |
| **Spot.io** | Spot instance management | Automated spot instance orchestration |
| **CAST AI** | Kubernetes | Automated K8s cost optimization + autoscaling |
| **CloudPilot AI** | Kubernetes | AI-powered K8s cost optimization |
| **ParkMyCloud** | Multi-cloud | Automated resource scheduling (on/off) |
| **Densify** | Multi-cloud | Container and VM rightsizing |

### Policy & Governance Tools

| Tool | Purpose | Platform |
|------|---------|----------|
| **AWS Budgets** | Budget alerts, actions | AWS |
| **Azure Policy** | Cost governance, tagging | Azure |
| **GCP Organization Policies** | Resource constraints | GCP |
| **OPA (Open Policy Agent)** | Policy-as-code | Kubernetes, multi-cloud |
| **Checkov** | IaC security + cost policies | Terraform, CloudFormation |

---

## Skill Structure Design

```
cost-optimization/
├── SKILL.md                         # Main skill (500-800 lines)
│   ├── Purpose & When to Use
│   ├── FinOps Principles (Inform/Optimize/Operate)
│   ├── Decision Frameworks (commitment, spot, rightsizing)
│   ├── Quick Reference (top 10 cost optimization tactics)
│   └── Tool Selection Guide
│
├── references/
│   ├── finops-foundations.md        # FinOps principles, maturity model
│   ├── commitment-strategies.md     # Reserved Instances, Savings Plans, CUDs
│   ├── kubernetes-cost-optimization.md  # K8s-specific patterns
│   ├── cloud-specific-tactics.md    # AWS/Azure/GCP optimization guides
│   ├── tagging-for-cost-allocation.md   # Cost allocation best practices
│   └── tools-comparison.md          # Detailed tool comparison matrix
│
├── examples/
│   ├── terraform/
│   │   ├── aws-cost-optimization.tf      # Budgets, anomaly detection
│   │   ├── azure-cost-management.tf      # Azure budgets, policies
│   │   └── gcp-billing-export.tf         # BigQuery export, budgets
│   ├── kubernetes/
│   │   ├── kubecost-deployment.yaml      # Kubecost Helm values
│   │   ├── resource-quotas.yaml          # Namespace quotas
│   │   └── vpa-recommendations.yaml      # VPA for rightsizing
│   ├── ci-cd/
│   │   ├── infracost-github-action.yml   # PR cost estimation
│   │   └── cost-approval-workflow.yml    # Block PRs with >$X increase
│   └── dashboards/
│       ├── grafana-cost-dashboard.json   # Prometheus + cost metrics
│       └── cloudwatch-cost-alarms.yaml   # AWS CloudWatch alarms
│
└── scripts/
    ├── cleanup_idle_resources.py    # Automated cleanup (AWS/Azure/GCP)
    ├── ri_coverage_report.py        # Reserved Instance coverage analysis
    ├── cost_allocation_report.py    # Generate showback/chargeback reports
    ├── spot_savings_calculator.py   # Estimate savings from spot instances
    └── k8s_rightsizing_audit.py     # Find K8s pods with missing requests
```

---

## Integration Points

### With Existing Skills

| Skill | Integration |
|-------|-------------|
| `resource-tagging` | Cost allocation tags enable showback/chargeback |
| `kubernetes-operations` | K8s rightsizing, VPA, cluster autoscaling for cost optimization |
| `infrastructure-as-code` | Infracost for Terraform cost estimation, policy-as-code |
| `aws-patterns` | AWS-specific optimizations (EC2, RDS, S3, Lambda) |
| `gcp-patterns` | GCP-specific optimizations (Compute Engine, BigQuery, GCS) |
| `azure-patterns` | Azure-specific optimizations (VMs, Storage, Functions) |
| `platform-engineering` | Internal FinOps platforms, self-service cost dashboards |
| `disaster-recovery` | Balance cost vs. RTO/RPO (warm standby vs. cold standby) |
| `observability` | Cost metrics in Grafana, cost-aware alerting |

---

## Common Pitfalls and Solutions

### Pitfall 1: No Cost Visibility

❌ **Bad:** Finance team sees cloud bill at end of month, surprises everywhere

✅ **Good:** Real-time cost dashboards, daily reports to engineering teams

**Solution:** Deploy Kubecost (K8s) + AWS Cost Explorer (cloud) + Slack alerts

---

### Pitfall 2: Reserved Instances Underutilization

❌ **Bad:** Purchased 100 RIs, only using 60 (40% wasted commitment)

✅ **Good:** Monitor RI utilization (target >95%), sell unused RIs on marketplace

**Solution:** Weekly RI coverage reports, adjust commitments quarterly

---

### Pitfall 3: Missing Resource Requests (Kubernetes)

❌ **Bad:** Pods with no requests set → inefficient bin-packing → wasted nodes

✅ **Good:** All pods have requests = avg usage, limits = 2-3x requests

**Solution:** Use VPA to auto-generate recommendations, enforce via admission control

---

### Pitfall 4: Idle Resources Not Cleaned Up

❌ **Bad:** 50 stopped EC2 instances (still paying for EBS), 200 unattached volumes

✅ **Good:** Weekly automated cleanup of idle resources >7 days old

**Solution:** Deploy AWS Lambda cleanup script, tag exceptions with `KeepAlive=true`

---

### Pitfall 5: No Budget Alerts

❌ **Bad:** Accidentally left test cluster running, $10K bill surprise

✅ **Good:** Budget alerts at 50%, 75%, 90%, 100% with cascading notifications

**Solution:** Terraform budget alerts + SNS → Slack/PagerDuty

---

## Key Takeaways

1. **FinOps is a Culture, Not a Tool** - Collaboration between finance, engineering, and operations
2. **Visibility First** - Can't optimize what you can't measure (tags + dashboards)
3. **Commitment = Savings** - Reserved Instances / Savings Plans provide 40-72% discounts
4. **Right-Size Continuously** - Target 60-80% utilization, not 100% (leave headroom)
5. **Automate Cleanup** - Idle resources are 100% waste (delete weekly)
6. **Kubernetes Costs are Hidden** - Use Kubecost/OpenCost for K8s cost visibility
7. **Shift-Left Cost Awareness** - Infracost in CI/CD prevents surprise cost increases
8. **Budget Alerts Prevent Overspend** - 50%, 75%, 90%, 100% cascading alerts
9. **Spot Instances for Fault-Tolerant Workloads** - 70-90% discount (CI/CD, batch jobs)
10. **Unit Cost Metrics Drive Business Value** - Cost per customer, cost per transaction

---

**Progressive disclosure:** This init.md provides the master plan. Detailed documentation in `references/` directory, implementation examples in `examples/`, and automation scripts in `scripts/`.

**Next Steps:** Create SKILL.md (500-800 lines) following the structure above, with decision frameworks and implementation patterns as primary content.
