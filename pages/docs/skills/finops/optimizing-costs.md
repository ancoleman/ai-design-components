---
sidebar_position: 1
title: Optimizing Costs
description: Optimize cloud infrastructure costs through FinOps practices and automated cost management
tags: [finops, cost-optimization, cloud-costs, reserved-instances, spot-instances, kubernetes]
---

# Optimizing Costs

Transform uncontrolled cloud spending into strategic resource allocation through the FinOps lifecycle: Inform, Optimize, and Operate.

## When to Use

Use this skill when:

- Reducing cloud spend by 15-40% through systematic optimization
- Implementing cost visibility dashboards and allocation tracking
- Establishing budget alerts and anomaly detection
- Optimizing Kubernetes resource requests and cluster efficiency
- Managing Reserved Instances, Savings Plans, or Committed Use Discounts
- Automating idle resource cleanup and right-sizing recommendations
- Setting up showback/chargeback models for internal teams
- Preventing cost overruns through CI/CD cost estimation (Infracost)
- Responding to finance team requests for cloud cost reduction

## Key Features

### 1. FinOps Lifecycle

**The Three Phases:**

```
┌─────────────────────────────────────────────────────┐
│  INFORM → OPTIMIZE → OPERATE (continuous loop)      │
│    ↓         ↓           ↓                          │
│ Visibility  Action   Automation                     │
└─────────────────────────────────────────────────────┘
```

**Inform Phase:** Establish cost visibility
- Enable cost allocation tags (Owner, Project, Environment)
- Deploy real-time cost dashboards for engineering teams
- Integrate cloud billing data (AWS CUR, Azure Consumption API, GCP BigQuery)
- Set up Kubernetes cost monitoring (Kubecost, OpenCost)

**Optimize Phase:** Take action on cost drivers
- Purchase commitment-based discounts (40-72% savings)
- Right-size over-provisioned resources (target 60-80% utilization)
- Implement spot/preemptible instances for fault-tolerant workloads
- Clean up idle resources (unattached volumes, old snapshots)

**Operate Phase:** Automate and govern
- Budget alerts with cascading notifications (50%, 75%, 90%, 100%)
- Automated cleanup scripts for idle resources
- CI/CD cost estimation to prevent surprise increases
- Continuous monitoring with anomaly detection

### 2. Commitment-Based Discounts

**Reserved Instances (RIs):** 40-72% discount for 1-3 year commitments
- **Standard RI**: Instance type locked, highest discount (60% for 3-year)
- **Convertible RI**: Flexible instance types, moderate discount (54% for 3-year)
- **Use for**: Databases (RDS, ElastiCache), stable production EC2 workloads

**Savings Plans:** Flexible compute commitments
- **Compute Savings Plans**: Applies to EC2, Fargate, Lambda (54% discount for 3-year)
- **EC2 Instance Savings Plans**: Tied to instance family (66% discount for 3-year)
- **Use for**: Workloads that change instance types or regions

**GCP Committed Use Discounts (CUDs):** 25-70% discount
- **Resource-based CUDs**: Commit to vCPU, memory, GPUs
- **Spend-based CUDs**: Commit to dollar amount (flexible)
- **Sustained Use Discounts**: Automatic 20-30% discount for sustained usage (no commitment)

**Decision Framework:**
```
Reserve when:
├─ Workload is production-critical (24/7 uptime required)
├─ Usage is predictable (stable baseline over 6+ months)
├─ Architecture is stable (unlikely to change instance types)
└─ Financial commitment acceptable (1-3 year lock-in)

Use On-Demand when:
├─ Development/testing environments
├─ Unpredictable spiky workloads
├─ Short-term projects (<6 months)
└─ Evaluating new instance types
```

### 3. Spot and Preemptible Instances

**Discount:** 70-90% off on-demand pricing (interruptible with 2-minute warning)

**Use Spot For:**
- CI/CD workers
- Batch jobs
- ML training (with checkpointing)
- Kubernetes workers
- Data analytics

**Avoid Spot For:**
- Stateful databases
- Real-time services
- Long-running jobs without checkpointing

**Best Practices:**
- Diversify instance types and spread across Availability Zones
- Implement graceful shutdown handlers
- Auto-fallback to on-demand when capacity unavailable
- Kubernetes: Mix 70% spot + 30% on-demand nodes with taints/tolerations

### 4. Right-Sizing Strategies

**Target Utilization:** 60-80% average (leave headroom for spikes)

**Compute Right-Sizing:**
- Analyze actual CPU/memory utilization over 30+ days
- Downsize instances with &lt;40% average utilization
- Consolidate underutilized workloads
- Switch instance families (compute-optimized vs. memory-optimized)

**Database Right-Sizing:**
- Analyze connection pool usage (max connections vs. allocated)
- Downgrade storage IOPS if utilization &lt;50%
- Evaluate read replica necessity (can caching replace it?)
- Consider serverless options (Aurora Serverless, Azure SQL Serverless)

**Kubernetes Right-Sizing:**
- Set requests = average usage (not peak)
- Set limits = 2-3x requests (allow bursting)
- Use Vertical Pod Autoscaler (VPA) for automated recommendations
- Identify pods with 0% CPU usage (candidates for consolidation)

**Storage Right-Sizing:**
- Delete unattached volumes (EBS, Azure Disks, GCP Persistent Disks)
- Delete old snapshots (>90 days, retention policy not required)
- Implement lifecycle policies (S3 Intelligent-Tiering, Azure Blob Lifecycle)
- Compress/deduplicate data

### 5. Kubernetes Cost Management

**Resource Requests and Limits:**
```yaml
# Set requests = average usage (enables efficient bin-packing)
resources:
  requests:
    cpu: 500m        # 0.5 CPU cores (average usage)
    memory: 1Gi      # 1 GiB memory (average usage)
  limits:
    cpu: 1500m       # 1.5 CPU cores (3x requests, allows bursting)
    memory: 3Gi      # 3 GiB memory (3x requests)
```

**Namespace Quotas:** Prevent runaway resource consumption
- ResourceQuota: Limit total CPU/memory per namespace
- LimitRange: Default/max requests per pod
- PriorityClass: Ensure critical pods get resources

**Cluster Autoscaling:**
- Scale down idle nodes to reduce costs
- Scale-to-zero for dev clusters during off-hours
- Use multiple node pools (spot + on-demand mix)
- Set max node limits to prevent overspend

**Cost Visibility:**
- Deploy Kubecost or OpenCost for namespace-level cost tracking
- Allocate costs by labels (team, project, environment)
- Track idle cost (cluster capacity not allocated to workloads)
- Generate showback/chargeback reports

### 6. Cost Visibility and Monitoring

**Tagging for Cost Allocation:**

**Required Tags:**
- `Owner` or `Team` - Responsible team/department
- `Project` or `Application` - Business unit or application name
- `Environment` - prod, staging, dev, test
- `CostCenter` - Finance cost center code

**Monitoring and Dashboards:**

**Native Cloud Tools:**
- **AWS Cost Explorer**: Analyze spending patterns, forecast costs
- **Azure Cost Management + Billing**: Budget tracking, cost analysis
- **GCP Cloud Billing**: BigQuery export for custom analysis

**Third-Party Platforms:**
- **Kubecost**: Kubernetes cost visibility and optimization
- **CloudZero**: Unit cost economics, anomaly detection
- **CloudHealth**: Multi-cloud cost management
- **Infracost**: Terraform cost estimation in CI/CD

**Key Metrics to Track:**
- Total monthly cloud spend (trend over time)
- Cost per service/team/project (allocation accuracy)
- Unit cost metrics (cost per customer, cost per transaction)
- Reserved Instance/Savings Plan utilization (target &gt;95%)
- Idle resource waste (target &lt;5% of total spend)
- Budget variance (forecasted vs. actual)

### 7. Budget Alerts and Anomaly Detection

**Cascading Budget Alerts:**
```
50% of budget  → Email to team lead (informational)
75% of budget  → Email + Slack to team (warning)
90% of budget  → Email + Slack + PagerDuty (urgent)
100% of budget → Automated shutdown (non-prod only) or escalation
```

**Anomaly Detection:** Alert on unexpected cost spikes
- &gt;20% cost increase week-over-week
- &gt;$500 unexpected daily cost spike
- New resource types (unusual spend patterns)

## Quick Start

### Enable AWS Cost Allocation Tags
```bash
# Using AWS CLI
aws ce create-cost-allocation-tag --key Environment
aws ce create-cost-allocation-tag --key Project
```

### Deploy Kubecost for Kubernetes
```bash
# Install via Helm
helm repo add kubecost https://kubecost.github.io/cost-analyzer/
helm install kubecost kubecost/cost-analyzer \
  --namespace kubecost \
  --create-namespace \
  --set kubecostToken="your-token"
```

### Set Up Budget Alerts (AWS)
```bash
aws budgets create-budget \
  --account-id 123456789012 \
  --budget file://budget.json \
  --notifications-with-subscribers file://notifications.json
```

## Implementation Checklist

### Phase 1: Establish Visibility (Week 1-2)
- [ ] Enable cost allocation tags (Owner, Project, Environment)
- [ ] Activate cost allocation tags in cloud billing console
- [ ] Deploy Kubecost for Kubernetes cost visibility (if using K8s)
- [ ] Create cost dashboards (Grafana, CloudWatch, Azure Monitor, GCP)
- [ ] Set up weekly cost reports (emailed to team leads)

### Phase 2: Set Up Governance (Week 2-3)
- [ ] Create budget alerts (50%, 75%, 90%, 100% thresholds)
- [ ] Enable anomaly detection (>20% WoW increase)
- [ ] Implement tagging policy enforcement (Azure Policy, AWS Config, GCP Org Policy)
- [ ] Establish showback reports (cost by team/project)
- [ ] Document cost ownership (who owns which services)

### Phase 3: Quick Wins (Week 3-4)
- [ ] Delete idle resources (unattached volumes, old snapshots)
- [ ] Stop/terminate unused development instances
- [ ] Right-size top 10 over-provisioned instances (&lt;40% utilization)
- [ ] Implement S3 Intelligent-Tiering or lifecycle policies
- [ ] Evaluate Reserved Instance/Savings Plan coverage

### Phase 4: Commitment Discounts (Month 2)
- [ ] Analyze 6-12 months usage history
- [ ] Calculate baseline usage for commitment sizing
- [ ] Purchase Reserved Instances for databases
- [ ] Purchase Savings Plans for compute workloads
- [ ] Monitor RI/SP utilization (target &gt;95%)

### Phase 5: Automation (Month 2-3)
- [ ] Deploy automated cleanup scripts (weekly schedule)
- [ ] Integrate Infracost into CI/CD pipelines
- [ ] Implement auto-shutdown for dev/test environments (off-hours)
- [ ] Enable Vertical Pod Autoscaler (VPA) for K8s rightsizing
- [ ] Set up Spot instance automation (Spot.io, CAST AI, or native)

### Phase 6: Continuous Optimization (Ongoing)
- [ ] Weekly cost reviews with engineering teams
- [ ] Monthly optimization sprints (top cost drivers)
- [ ] Quarterly commitment adjustments (RI/SP coverage)
- [ ] Annual FinOps maturity assessment

## Common Pitfalls

### Pitfall 1: No Cost Visibility
❌ **Problem**: Finance team sees cloud bill at end of month, surprises everywhere
✅ **Solution**: Deploy real-time cost dashboards, daily Slack reports to engineering teams

### Pitfall 2: Reserved Instance Underutilization
❌ **Problem**: Purchased 100 RIs, only using 60 (40% wasted commitment)
✅ **Solution**: Monitor RI utilization weekly (target >95%), sell unused RIs on marketplace

### Pitfall 3: Missing Kubernetes Resource Requests
❌ **Problem**: Pods with no requests set → inefficient bin-packing → wasted nodes
✅ **Solution**: Use VPA to auto-generate recommendations, enforce via admission control

### Pitfall 4: Idle Resources Not Cleaned Up
❌ **Problem**: 50 stopped EC2 instances (still paying for EBS), 200 unattached volumes
✅ **Solution**: Weekly automated cleanup of idle resources >7 days old

### Pitfall 5: No Budget Alerts
❌ **Problem**: Accidentally left test cluster running, $10K bill surprise
✅ **Solution**: Budget alerts at 50%, 75%, 90%, 100% with Slack/PagerDuty notifications

## Related Skills

- **resource-tagging**: Cost allocation tags enable showback/chargeback models
- **operating-kubernetes**: K8s rightsizing, VPA, cluster autoscaling
- **writing-infrastructure-code**: Infracost for Terraform cost estimation
- **deploying-on-aws**: AWS-specific cost optimization tactics
- **deploying-on-gcp**: GCP-specific optimizations
- **deploying-on-azure**: Azure-specific optimizations
- **engineering-platforms**: Internal FinOps platforms and self-service dashboards
- **planning-disaster-recovery**: Balance cost vs. RTO/RPO

## Key Takeaways

1. **FinOps is a Culture**: Collaboration between finance, engineering, and operations
2. **Visibility First**: Can't optimize what can't measure (tags + dashboards mandatory)
3. **Commitment = Savings**: Reserved Instances/Savings Plans provide 40-72% discounts
4. **Right-Size Continuously**: Target 60-80% utilization (leave headroom for spikes)
5. **Automate Cleanup**: Idle resources are 100% waste (weekly automated deletion)
6. **Kubernetes Costs Hidden**: Use Kubecost/OpenCost for namespace-level visibility
7. **Shift-Left Cost Awareness**: Infracost in CI/CD prevents surprise cost increases
8. **Budget Alerts Prevent Overspend**: Cascading notifications at 50%, 75%, 90%, 100%
9. **Spot for Fault-Tolerant Workloads**: 70-90% discount (CI/CD, batch jobs, ML training)
10. **Unit Cost Metrics Drive Value**: Track cost per customer, cost per transaction

## References

- Full skill documentation: `/skills/optimizing-costs/SKILL.md`
- FinOps foundations: `/skills/optimizing-costs/references/finops-foundations.md`
- Commitment strategies: `/skills/optimizing-costs/references/commitment-strategies.md`
- Kubernetes cost optimization: `/skills/optimizing-costs/references/kubernetes-cost-optimization.md`
- Tagging for cost allocation: `/skills/optimizing-costs/references/tagging-for-cost-allocation.md`
- Cloud-specific tactics: `/skills/optimizing-costs/references/cloud-specific-tactics.md`
- Tools comparison: `/skills/optimizing-costs/references/tools-comparison.md`
