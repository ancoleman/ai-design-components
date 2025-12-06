# Azure Governance and Compliance Reference

Comprehensive guide to Azure Policy, Blueprints, and cost management.

## Table of Contents

1. [Azure Policy](#azure-policy)
2. [Azure Blueprints](#azure-blueprints)
3. [Cost Management](#cost-management)
4. [Resource Tagging](#resource-tagging)
5. [Azure Landing Zones](#azure-landing-zones)

---

## Azure Policy

Governance service to enforce organizational standards and assess compliance at scale.

### Policy Effects

| Effect | Behavior | Use Case |
|--------|----------|----------|
| **Deny** | Block resource creation/update | Prevent non-compliant resources |
| **Audit** | Log compliance | Visibility without blocking |
| **AuditIfNotExists** | Check for related resources | Ensure diagnostics enabled |
| **DeployIfNotExists** | Auto-remediate | Deploy missing configurations |
| **Modify** | Change properties | Add missing tags |
| **Disabled** | Turn off policy | Testing |

### Common Policies

- Allowed resource types
- Allowed locations
- Required tags
- Storage account encryption
- Network security rules
- SQL Database TDE

---

## Azure Blueprints

Repeatable environment deployment with policy, RBAC, and ARM templates.

### Blueprint Components

1. **Artifacts:** Policy assignments, role assignments, ARM templates
2. **Parameters:** Environment-specific values
3. **Versions:** Track changes over time

### Use Cases

- Regulatory compliance (ISO 27001, HIPAA, PCI-DSS)
- Landing zone deployment
- Multi-region rollouts

---

## Cost Management

Monitor, allocate, and optimize Azure spending across organization.

### Cost Allocation Tags

Required tags for cost tracking:
- Environment (dev, staging, production)
- CostCenter (billing code)
- Owner (team responsible)
- Project (initiative)

### Azure Advisor Cost Recommendations

- Right-size underutilized VMs
- Delete unattached disks
- Purchase Reserved Instances
- Enable auto-pause for SQL serverless
- Optimize storage tiers

---

## Resource Tagging

### Tag Strategy

| Tag Name | Values | Purpose |
|----------|--------|---------|
| Environment | dev, staging, production | Lifecycle management |
| Owner | team@example.com | Accountability |
| CostCenter | CC-1234 | Chargeback |
| Project | project-alpha | Initiative tracking |
| Criticality | low, medium, high | SLA/support priority |
| Compliance | pci, hipaa, sox | Regulatory requirements |

### Tag Inheritance

Tags on Resource Groups do NOT inherit to resources automatically (use Azure Policy to enforce).

---

## Azure Landing Zones

Enterprise-scale architecture for Azure adoption.

### Core Components

1. **Management Groups:** Hierarchical organization
2. **Subscriptions:** Billing and resource boundaries
3. **Policies:** Governance guardrails
4. **Networking:** Hub-spoke topology
5. **Identity:** Entra ID integration
6. **Security:** Microsoft Defender for Cloud

### Reference Architectures

- CAF (Cloud Adoption Framework) Landing Zones
- Azure Landing Zone Accelerator
- Industry-specific landing zones (FSI, healthcare)
