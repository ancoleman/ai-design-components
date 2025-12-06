---
sidebar_position: 2
title: Writing Infrastructure Code
description: Terraform, Pulumi, and AWS CDK for declarative infrastructure provisioning
tags: [infrastructure, iac, terraform, pulumi, cdk]
---

# Writing Infrastructure Code

Provision and manage cloud infrastructure using declarative IaC tools. Covers Terraform/OpenTofu, Pulumi, and AWS CDK with state management, module design, and operational patterns.

## When to Use

Use when:
- Provisioning cloud resources (compute, networking, databases, storage)
- Migrating from manual infrastructure to code-based workflows
- Designing reusable infrastructure modules
- Implementing multi-cloud or hybrid-cloud deployments
- Establishing state management and drift detection patterns
- Integrating infrastructure provisioning into CI/CD pipelines
- Evaluating IaC tools (Terraform vs Pulumi vs CDK)

## Key Features

### Tool Selection Framework
- **Terraform/OpenTofu**: Declarative HCL, multi-cloud, largest provider ecosystem (3000+)
- **Pulumi**: Imperative programming (TypeScript/Python/Go), strong typing, native testing
- **AWS CDK**: AWS-native, L1/L2/L3 constructs, CloudFormation under the hood

### State Management
- Remote state with locking (S3+DynamoDB, GCS, Azure Blob, Terraform Cloud)
- State isolation strategies (directory separation, workspaces, layered architecture)
- Encryption at rest and versioning for rollback
- Never commit state files to Git

### Module Design
- Composable module structure with clear input/output contracts
- Semantic versioning for internal modules
- Pin module versions in production
- Examples directory showing usage patterns

### Operational Patterns
- Drift detection with scheduled runs
- Cost estimation with Infracost
- Security scanning with Checkov/tfsec
- Disaster recovery with state backups

## Quick Start

### Terraform VPC Module

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(
    var.tags,
    {
      Name = var.vpc_name
    }
  )
}

resource "aws_subnet" "public" {
  count             = length(var.public_subnets)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnets[count.index]
  availability_zone = var.azs[count.index]

  map_public_ip_on_launch = true

  tags = {
    Name = "${var.vpc_name}-public-${var.azs[count.index]}"
  }
}

# State backend configuration
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "production/vpc/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

### Pulumi VPC (TypeScript)

```typescript
import * as aws from "@pulumi/aws";
import * as pulumi from "@pulumi/pulumi";

const vpc = new aws.ec2.Vpc("main", {
    cidrBlock: "10.0.0.0/16",
    enableDnsHostnames: true,
    enableDnsSupport: true,
    tags: {
        Name: "production-vpc",
    },
});

const publicSubnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"].map(
    (cidr, i) => new aws.ec2.Subnet(`public-${i}`, {
        vpcId: vpc.id,
        cidrBlock: cidr,
        availabilityZone: `us-east-1${["a", "b", "c"][i]}`,
        mapPublicIpOnLaunch: true,
    })
);

export const vpcId = vpc.id;
export const publicSubnetIds = publicSubnets.map(s => s.id);
```

## Decision Framework

**Choose Terraform/OpenTofu when:**
- Multi-cloud or hybrid-cloud required
- Operations/SRE team prefers declarative approach
- Mature module ecosystem needed
- HCL experience on team

**Choose Pulumi when:**
- Developer-centric team (TypeScript/Python/Go)
- Complex logic requires programming constructs
- Native unit testing desired
- Strong typing and IDE support critical

**Choose AWS CDK when:**
- AWS-only infrastructure
- Tight AWS service integration needed
- L2/L3 construct abstractions beneficial
- CloudFormation familiarity exists

## State Management Best Practices

### Remote State Configuration

```hcl
# AWS: S3 + DynamoDB
terraform {
  backend "s3" {
    bucket         = "terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

# GCP: Google Cloud Storage
terraform {
  backend "gcs" {
    bucket = "terraform-state"
    prefix = "production"
  }
}
```

### State Isolation Strategies

1. **Directory Separation** (recommended)
   - `prod/`, `staging/`, `dev/` directories
   - Complete state file isolation
   - No cross-environment contamination risk

2. **Workspaces** (use carefully)
   - Single codebase, environment namespacing
   - Risk of accidental cross-environment operations

3. **Layered Architecture** (blast radius reduction)
   - Separate state: networking, compute, data layers
   - Cross-layer references via remote state data sources

## Related Skills

- [Operating Kubernetes](./operating-kubernetes) - Provision EKS, GKE, AKS clusters
- [Architecting Networks](./architecting-networks) - VPC design implemented via IaC
- [Managing Configuration](./managing-configuration) - Ansible post-provisioning configuration
- [Planning Disaster Recovery](./planning-disaster-recovery) - Infrastructure rebuild procedures

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/writing-infrastructure-code)
- Terraform Patterns: `references/terraform-patterns.md`
- Pulumi Patterns: `references/pulumi-patterns.md`
- State Management: `references/state-management.md`
- Module Design: `references/module-design.md`
- Drift Detection: `references/drift-detection.md`
