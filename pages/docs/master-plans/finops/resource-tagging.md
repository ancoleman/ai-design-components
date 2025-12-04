---
sidebar_position: 2
title: Resource Tagging
description: Cloud resource tagging strategies for cost allocation, compliance, and automation with multi-cloud enforcement patterns
tags: [master-plan, finops, tagging, governance]
---

# Resource Tagging

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Foundational metadata layer for cloud operations through comprehensive resource tagging strategies.

## Scope

This skill provides tagging frameworks and enforcement:

- **Tag Taxonomy** - 6 core categories (technical, business, security, automation, operational, custom)
- **Minimum Viable Tags** - "Big Six" required tags (Name, Environment, Owner, CostCenter, Project, ManagedBy)
- **Naming Conventions** - PascalCase (AWS), lowercase (GCP), kebab-case (Azure)
- **Enforcement Patterns** - AWS Config, Azure Policy, GCP Organization Policies, OPA Gatekeeper
- **Cost Allocation** - Tags enable showback/chargeback and budget alerts
- **Compliance Auditing** - Tag compliance queries and automated remediation

## Key Components

- **"Big Six" Required Tags** - Name, Environment, Owner, CostCenter, Project, ManagedBy
- **Tag Inheritance** - Parent resources propagate tags to children (reduces manual effort)
- **Automated Enforcement** - Deny resource creation without required tags
- **Provider Default Tags** - Terraform/Pulumi provider-level tags (applied to all resources)
- **Cost Allocation Tags** - Enable 80% reduction in unallocated cloud spend
- **Audit Queries** - AWS Config, Azure Resource Graph, GCP Cloud Asset Inventory

## Decision Framework

**Required vs. Optional Tags:**
```
REQUIRED (enforce at creation):
- Cost allocation: Owner, CostCenter, Project
- Lifecycle: Environment, ManagedBy
- Identification: Name

OPTIONAL (recommended):
- Operational: Backup, Monitoring, Schedule
- Security: Compliance, DataClassification
- Custom: Application, Component, Customer
```

**Enforcement Strategy:**
```
Hard enforcement (deny creation) → Cost allocation tags
Soft enforcement (alert only) → Operational tags
No enforcement (best-effort) → Experimental tags
```

## Tool Recommendations

**Tagging Enforcement:**
- **AWS Config** - Tag compliance monitoring and auto-remediation
- **Azure Policy** - Tag enforcement and inheritance
- **GCP Organization Policies** - Label restrictions and validation
- **OPA Gatekeeper** - Kubernetes admission control
- **Kyverno** - K8s policy engine (auto-tagging)

**Cost Allocation:**
- **AWS Cost Explorer** - Tag-based cost analysis
- **Azure Cost Management** - Tag grouping and budgets
- **GCP Cloud Billing** - Label-based cost breakdown

## Integration Points

- `infrastructure-as-code` - Tags applied via Terraform/Pulumi default_tags
- `cost-optimization` - Tags enable cost allocation and budgeting
- `compliance-frameworks` - Tags prove PCI/HIPAA/SOC2 scope
- `security-hardening` - Tags enforce security policies
- `disaster-recovery` - Tags identify resources for backup policies
- `kubernetes-operations` - Labels for pod scheduling and resource quotas

## Learn More

- [Full Master Plan](https://github.com/ancoleman/ai-design-components/blob/main/skills/resource-tagging/init.md)
- [AWS Tagging Best Practices](https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html)
- [Azure Tagging Strategy](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-tagging)
