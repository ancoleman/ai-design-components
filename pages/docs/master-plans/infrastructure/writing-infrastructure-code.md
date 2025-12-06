---
sidebar_position: 1
title: Infrastructure as Code
description: Master plan for infrastructure provisioning and management across Terraform, Pulumi, CDK, and CloudFormation
tags: [master-plan, infrastructure, iac, terraform, pulumi]
---

# Infrastructure as Code

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Infrastructure as Code (IaC) is the foundation of modern cloud operations. This skill covers declarative infrastructure management across multiple tools and cloud providers, with emphasis on state management, module architecture, and operational patterns.

## Scope

This skill teaches:

- **Tool Selection** - Terraform/OpenTofu, Pulumi, AWS CDK, CloudFormation decision frameworks
- **State Management** - Remote backends, locking, isolation strategies, sensitive data handling
- **Module Architecture** - Composable design, versioning, input/output contracts, testing
- **Operational Patterns** - Drift detection, resource imports, blue-green deployments, disaster recovery
- **Multi-Language Support** - HCL, TypeScript, Python, Go implementations

## Key Components

### IaC Tools
1. **Terraform/OpenTofu** - Multi-cloud declarative IaC (HCL)
2. **Pulumi** - Developer-centric IaC (TypeScript, Python, Go, C#)
3. **AWS CDK** - AWS-native constructs (TypeScript, Python, Java, C#)
4. **CloudFormation** - AWS-native YAML/JSON

### Core Patterns
- Remote state with locking (S3, GCS, Azure Blob)
- State isolation (workspaces vs directories)
- Module composition and versioning
- Testing infrastructure code (Terratest)

## Decision Framework

**Which IaC Tool?**

```
Multi-cloud required?
  YES → Team composition?
          Ops/SRE → TERRAFORM
          Dev-heavy → PULUMI
  NO → AWS only?
          YES → Language preference?
                  HCL → TERRAFORM
                  TypeScript/Python → CDK
                  YAML → CLOUDFORMATION
          NO → GCP/Azure only?
                  GCP → TERRAFORM or PULUMI
                  Azure → TERRAFORM or BICEP
```

**State Backend Selection:**
- AWS + Team → S3 + DynamoDB (native locking, IAM)
- GCP + Team → GCS (native locking)
- Azure + Team → Azure Blob (native locking)
- Multi-cloud → Terraform Cloud (unified)
- Pulumi → Pulumi Service (best integration, free tier)

## Tool Recommendations

| Tool | Version | Use Case | Languages |
|------|---------|----------|-----------|
| **Terraform** | 1.6+ | Multi-cloud declarative | HCL |
| **OpenTofu** | 1.6+ | Open-source Terraform fork | HCL |
| **Pulumi** | 3.x | Developer-centric IaC | TS, Python, Go, C# |
| **AWS CDK** | 2.x | AWS-native constructs | TS, Python, Java, C# |

**Supporting Tools:**
- Terragrunt (DRY Terraform wrapper)
- tflint (Terraform linter)
- Checkov (IaC security scanner)
- Infracost (cost estimation)
- Terratest (infrastructure testing)
- driftctl (drift detection)

## Integration Points

**With Other Skills:**
- `deploying-applications` - IaC creates infrastructure for deployments
- `operating-kubernetes` - Terraform provisions EKS/GKE/AKS clusters
- `building-ci-pipelines` - CI/CD runs terraform plan/apply
- `secret-management` - Vault/ESO provisioned via IaC
- `implementing-observability` - Monitoring infrastructure via IaC

**Workflow Example:**
```
IaC → Kubernetes → Applications
  │         │            │
  ▼         ▼            ▼
Create   Configure   Deploy
EKS       RBAC,       workloads
cluster   HPA
```

## Learn More

- [Full Master Plan (init.md)](https://github.com/ancoleman/ai-design-components/blob/main/skills/writing-infrastructure-code/init.md)
- Related: `operating-kubernetes`, `building-ci-pipelines`, `secret-management`
