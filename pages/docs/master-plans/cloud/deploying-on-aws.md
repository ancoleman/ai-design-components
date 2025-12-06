---
sidebar_position: 1
title: AWS Patterns
description: Comprehensive AWS architectural patterns with service selection frameworks, Well-Architected principles, and IaC examples
tags: [master-plan, cloud, aws, architecture]
---

# AWS Patterns

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Comprehensive AWS architectural patterns covering service selection, Well-Architected Framework, and infrastructure as code across 200+ AWS services.

## Scope

This skill provides decision-first frameworks for AWS service selection, covering:

- **Compute**: Lambda vs. Fargate vs. ECS vs. EKS vs. EC2
- **Storage**: S3 tiers, EBS, EFS, FSx optimization
- **Databases**: RDS vs. Aurora vs. DynamoDB selection
- **Networking**: VPC design, load balancing, CloudFront
- **Security**: IAM, KMS, Secrets Manager, WAF patterns
- **Cost Optimization**: Reserved instances, Savings Plans, Spot instances

## Key Components

- **Service Selection Frameworks** - When to use each AWS service
- **Well-Architected Pillars** - Operational excellence, security, reliability, performance, cost, sustainability
- **Serverless Patterns** - Lambda + API Gateway + EventBridge + DynamoDB
- **Container Patterns** - ECS on Fargate, EKS cluster design
- **Multi-IaC Support** - CDK, Terraform, and CloudFormation examples
- **2025 Best Practices** - Lambda SnapStart, S3 Express One Zone, Aurora Limitless

## Decision Framework

**Compute Service Selection:**
```
Event-driven (&lt;15 min) → Lambda
Stateless containers → Fargate
Need Kubernetes → EKS
Need control plane → EC2
```

**Database Selection:**
```
Relational + MySQL/PostgreSQL → RDS or Aurora
Key-value + scale → DynamoDB
Multi-region ACID → Aurora Global Database
```

## Tool Recommendations

- **AWS CDK** (TypeScript/Python) - Type-safe infrastructure with L2/L3 constructs
- **Terraform** (HCL) - Multi-cloud IaC with AWS provider
- **AWS CLI v2** - Command-line management with SSO support
- **boto3** (Python SDK) - Automation and scripting

## Integration Points

- `writing-infrastructure-code` - AWS-specific IaC patterns (CDK, CloudFormation)
- `operating-kubernetes` - EKS cluster operations and IAM for Service Accounts
- `building-ci-pipelines` - AWS CodePipeline, CodeBuild, CodeDeploy
- `secret-management` - Secrets Manager and Parameter Store
- `optimizing-costs` - AWS Cost Explorer, Budgets, Compute Optimizer
- `implementing-observability` - CloudWatch, X-Ray distributed tracing

## Learn More

- [Full Master Plan](https://github.com/ancoleman/ai-design-components/blob/main/skills/deploying-on-aws/init.md)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)
