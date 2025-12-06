---
sidebar_position: 1
title: Cost Optimization
description: FinOps best practices for cloud cost optimization with commitment strategies, right-sizing, and Kubernetes cost management
tags: [master-plan, finops, cost-optimization]
---

# Cost Optimization

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Comprehensive FinOps practices for cloud cost optimization, covering visibility, commitment discounts, right-sizing, and Kubernetes cost management.

## Scope

This skill provides FinOps frameworks and automation:

- **Cost Visibility** - Tagging, showback/chargeback, anomaly detection
- **Commitment Discounts** - Reserved Instances, Savings Plans, Committed Use Discounts
- **Right-Sizing** - Compute, database, storage, Kubernetes optimization
- **Spot Instances** - 70-90% savings for fault-tolerant workloads
- **Kubernetes Cost Management** - Kubecost, OpenCost, resource requests/limits
- **Automation** - Idle resource cleanup, budget alerts, policy enforcement

## Key Components

- **FinOps Lifecycle** - Inform → Optimize → Operate (continuous improvement)
- **Cost Allocation Tags** - Enable showback/chargeback reporting
- **Commitment Strategy** - When to purchase Reserved Instances vs. Savings Plans
- **Kubernetes Rightsizing** - VPA recommendations, namespace quotas, cluster autoscaling
- **Budget Alerts** - Cascading notifications at 50%, 75%, 90%, 100%
- **Unit Cost Metrics** - Cost per customer, cost per transaction (business value)

## Decision Framework

**Commitment Discount Strategy:**
```
Steady-state baseline (6+ months) → Reserved Instances (40-72% savings)
Variable compute workload → Savings Plans (flexible)
Fault-tolerant batch jobs → Spot Instances (70-90% savings)
Unpredictable/spiky traffic → On-Demand (no commitment)
```

**Right-Sizing Priority:**
```
HIGH: Idle resources (100% waste) - Delete unattached volumes, stopped instances
MEDIUM: Over-provisioned instances (&lt;40% utilization) - Downsize
LOW: Application optimization - Requires code changes
```

## Tool Recommendations

**Cost Visibility:**
- **Kubecost** - Kubernetes cost allocation and optimization
- **Infracost** - Terraform cost estimation in CI/CD
- **CloudZero** - Unit cost economics and anomaly detection
- **AWS Cost Explorer / Azure Cost Management / GCP Cloud Billing** - Native cloud tools

**Automation:**
- **AWS Compute Optimizer** - ML-based EC2 rightsizing
- **Azure Advisor** - Multi-service optimization recommendations
- **GCP Recommender** - Idle resource detection, commitment advice

## Integration Points

- `resource-tagging` - Cost allocation tags enable showback/chargeback
- `operating-kubernetes` - K8s rightsizing, VPA, cluster autoscaling
- `writing-infrastructure-code` - Infracost for Terraform cost estimation
- `deploying-on-aws` / `deploying-on-gcp` / `deploying-on-azure` - Cloud-specific optimizations
- `platform-engineering` - Internal FinOps platforms and self-service tools

## Learn More

- [Full Master Plan](https://github.com/ancoleman/ai-design-components/blob/main/skills/optimizing-costs/init.md)
- [FinOps Foundation](https://www.finops.org/)
- [Kubecost Documentation](https://docs.kubecost.com/)
