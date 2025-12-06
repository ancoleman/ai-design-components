---
sidebar_position: 1
title: Deploying on AWS
description: Selecting and implementing AWS services and architectural patterns
tags: [cloud, aws, lambda, ec2, rds, s3, serverless, containers, architecture]
---

# Deploying on AWS

Select and implement Amazon Web Services through proven architectural patterns, service selection frameworks, and Well-Architected principles.

## When to Use

Use this skill when:

- Choosing between Lambda, Fargate, ECS, EKS, or EC2 for compute workloads
- Selecting database services (RDS, Aurora, DynamoDB) based on access patterns
- Designing VPC architecture for multi-tier applications
- Implementing serverless patterns with API Gateway and Lambda
- Building container-based microservices on ECS or EKS
- Applying AWS Well-Architected Framework to designs
- Optimizing AWS costs while maintaining performance
- Implementing security best practices (IAM, KMS, encryption)

## Key Features

### 1. Compute Service Selection

**Decision Flow:**

```
Execution Duration:
  <15 minutes → Evaluate Lambda
  >15 minutes → Evaluate containers or VMs

Event-Driven/Scheduled:
  YES → Lambda (serverless)
  NO → Consider traffic patterns

Containerized:
  YES → Need Kubernetes?
    YES → EKS
    NO → ECS (Fargate or EC2)
  NO → Evaluate EC2 or containerize first

Special Requirements:
  GPU/Windows/BYOL licensing → EC2
  Predictable high traffic → EC2 or ECS on EC2 (cost optimization)
  Variable traffic → Lambda or Fargate
```

**Quick Reference:**

| Workload | Primary Choice | Cost Model | Key Benefit |
|----------|---------------|------------|-------------|
| API Backend | Lambda + API Gateway | Pay per request | Auto-scale, no servers |
| Microservices | ECS on Fargate | Pay for runtime | Simple operations |
| Kubernetes Apps | EKS | $73/mo + compute | Portability, ecosystem |
| Batch Jobs | Lambda or Fargate Spot | Request/spot pricing | Cost efficiency |
| Long-Running | EC2 Reserved Instances | 30-60% savings | Predictable cost |

### 2. Database Service Selection

**Decision Matrix by Access Pattern:**

| Access Pattern | Data Model | Primary Choice | Key Criteria |
|----------------|------------|----------------|--------------|
| Transactional (OLTP) | Relational | Aurora | Performance + HA |
| Simple CRUD | Relational | RDS PostgreSQL | Cost vs. features |
| Key-Value Lookups | NoSQL | DynamoDB | Serverless scale |
| Document Storage | JSON/BSON | DynamoDB | Flexibility vs. MongoDB compat |
| Caching | In-Memory | ElastiCache Redis | Speed + durability |
| Analytics (OLAP) | Columnar | Redshift/Athena | Dedicated vs. serverless |
| Time-Series | Timestamped | Timestream | Purpose-built |

### 3. Storage Service Selection

**Primary Decision Tree:**

```
Data Type:
  Objects (files, media) → S3 + lifecycle policies
  Blocks (databases, boot volumes) → EBS
  Shared Files (cross-instance) → Evaluate protocol

File Protocol Required:
  NFS (Linux) → EFS
  SMB (Windows) → FSx for Windows
  High-Performance HPC → FSx for Lustre
  Multi-Protocol + Enterprise → FSx for NetApp ONTAP
```

**Cost Comparison (1TB/month):**

| Service | Monthly Cost | Access Pattern |
|---------|--------------|----------------|
| S3 Standard | $23 | Frequent access |
| S3 Standard-IA | $12.50 | Infrequent (>30 days) |
| S3 Glacier Instant | $4 | Archive, instant retrieval |
| EBS gp3 | $80 | Block storage |
| EFS Standard | $300 | Shared files, frequent |
| EFS IA | $25 | Shared files, infrequent |

## Architecture Patterns

### Pattern 1: REST API (Lambda + API Gateway + DynamoDB)

**Architecture:**
```
Client → API Gateway (HTTP API) → Lambda → DynamoDB
                                        ↓
                                       S3 (file uploads)
```

**Use When:**
- Building RESTful APIs with CRUD operations
- Variable or unpredictable traffic
- Minimal operational overhead desired
- Pay-per-request cost model acceptable

**Cost Estimate (1M requests/month):**
- API Gateway: $3.50
- Lambda: $3.53
- DynamoDB: ~$7.50
- **Total: ~$15/month** (vs. Fargate ~$35+, EC2 ~$50+)

### Pattern 2: Event-Driven Processing (EventBridge + Lambda + SQS)

**Architecture:**
```
S3 Upload → EventBridge Rule → Lambda (process) → DynamoDB (metadata)
                                              ↓
                                            SQS (downstream tasks)
```

**Use When:**
- Asynchronous file processing
- Decoupled microservices communication
- Fan-out patterns (one event, multiple consumers)
- Need retry logic and dead-letter queues

**Key Features (2025):**
- **EventBridge Pipes**: Simplified source → filter → enrichment → target
- **Lambda Response Streaming**: Stream responses up to 20MB
- **Step Functions Distributed Map**: Process millions of items in parallel

### Pattern 3: ECS on Fargate (Serverless Containers)

**Architecture:**
```
ALB → ECS Service (Fargate tasks) → RDS Aurora
                                 ↓
                           ElastiCache Redis
```

**Use When:**
- Containerized applications without cluster management
- Variable traffic with auto-scaling
- Avoid EC2 instance management
- Docker-based deployment

**Cost Model (2 vCPU, 4GB RAM, 24/7):**
- Fargate: ~$70/month
- ALB: ~$20/month
- RDS Aurora db.t3.medium: ~$50/month
- **Total: ~$140/month**

## AWS Well-Architected Framework

### Six Pillars

**1. Operational Excellence**
- Infrastructure as code (CDK, Terraform, CloudFormation)
- Automated deployments (CI/CD pipelines)
- Observability (CloudWatch Logs, Metrics, X-Ray)

**2. Security**
- Strong identity foundation (IAM roles and policies)
- Defense in depth (Security Groups, NACLs, WAF)
- Data protection (encryption at rest and in transit)
- Detective controls (CloudTrail, GuardDuty, Security Hub)

**3. Reliability**
- Multi-AZ deployments (RDS Multi-AZ, Aurora replicas)
- Auto-scaling (EC2 ASG, ECS Service Auto Scaling)
- Backup and recovery (automated snapshots, cross-region)

**4. Performance Efficiency**
- Right-size resources (use Compute Optimizer)
- Use managed services (reduce operational overhead)
- Caching strategies (CloudFront, ElastiCache, DAX)

**5. Cost Optimization**
- Right-sizing compute (match capacity to demand)
- Pricing models (Reserved Instances, Savings Plans, Spot)
- Storage optimization (S3 Intelligent-Tiering, lifecycle policies)
- Cost monitoring (Cost Explorer, Budgets, Trusted Advisor)

**6. Sustainability (Added 2024)**
- Use Graviton processors (60% less energy, 25% better performance)
- Optimize workload placement (renewable energy regions)
- Storage efficiency (delete unused data, compression)

## Infrastructure as Code

### Tool Selection

**AWS CDK (Cloud Development Kit):**
- **Languages**: TypeScript, Python, Java, C#, Go
- **Best For**: AWS-native workloads, type-safe infrastructure
- **Key Benefit**: High-level constructs, synthesizes to CloudFormation

**Terraform:**
- **Language**: HCL (HashiCorp Configuration Language)
- **Best For**: Multi-cloud environments
- **Key Benefit**: Largest ecosystem, mature state management

**CloudFormation:**
- **Language**: YAML or JSON
- **Best For**: Native AWS integration, no additional tools
- **Key Benefit**: AWS service support on day 1

### CDK Quick Start

```bash
# Install CDK CLI
npm install -g aws-cdk

# Initialize new project
cdk init app --language=typescript
npm install

# Deploy infrastructure
cdk bootstrap  # One-time setup
cdk deploy
```

### Terraform Quick Start

```bash
# Install Terraform
brew install terraform  # macOS

# Initialize project
terraform init

# Preview changes
terraform plan

# Apply changes
terraform apply
```

## Cost Optimization Strategies

### Compute Cost Optimization

**Right-Sizing:**
- Use AWS Compute Optimizer for EC2/Lambda recommendations
- Monitor CloudWatch metrics (CPU, memory utilization)
- Start conservatively, scale based on actual usage

**Pricing Models:**

| Model | Commitment | Savings | Best For |
|-------|------------|---------|----------|
| On-Demand | None | 0% | Variable workloads |
| Savings Plans | 1-3 years | 30-40% | Flexible compute |
| Reserved Instances | 1-3 years | 30-60% | Predictable workloads |
| Spot Instances | None | 60-90% | Fault-tolerant tasks |

**Graviton Advantage:**
- Graviton3 instances: 25% better performance vs. Graviton2
- 60% less energy consumption
- Available: EC2, Lambda, Fargate, RDS, ElastiCache

### Storage Cost Optimization

**S3 Lifecycle Policies:**
```
Day 0-30:    S3 Standard         ($0.023/GB)
Day 30-90:   S3 Standard-IA      ($0.0125/GB)
Day 90-365:  S3 Glacier Instant  ($0.004/GB)
Day 365+:    S3 Deep Archive     ($0.00099/GB)
```

**EBS Optimization:**
- Use gp3 volumes (20% cheaper than gp2, configurable IOPS)
- Delete unused snapshots
- Archive old snapshots (75% cheaper)

## Quick Reference

### VPC Architecture (3-Tier Pattern)

```
VPC: 10.0.0.0/16

Per Availability Zone (deploy across 3 AZs):
  Public Subnet:    10.0.X.0/24   (ALB, NAT Gateway)
  Private Subnet:   10.0.1X.0/24  (ECS, Lambda, app tier)
  Database Subnet:  10.0.2X.0/24  (RDS, Aurora, isolated)
```

### Security Best Practices

**IAM Principles:**
- Use IAM roles (not users) for applications
- Implement least privilege
- Enable MFA for privileged users
- Use IAM Access Analyzer to validate policies

**Data Protection:**
- S3: SSE-S3 or SSE-KMS encryption
- EBS: KMS encryption
- RDS/Aurora: KMS encryption + TLS connections
- DynamoDB: KMS encryption + HTTPS API

**Secrets Management:**
- Secrets Manager: Database credentials with automatic rotation
- Parameter Store: Application configuration (free tier available)
- KMS: Encryption key management

## AWS Service Updates (2025)

**Recent Innovations:**
- **Lambda SnapStart**: Near-instant cold starts for Java functions
- **Lambda Response Streaming**: Stream responses up to 20MB
- **EventBridge Pipes**: Simplified event processing
- **S3 Express One Zone**: 10x faster S3, single-digit millisecond latency
- **ECS Service Connect**: Built-in service mesh for ECS
- **EKS Auto Mode**: Fully managed Kubernetes node lifecycle
- **EKS Pod Identities**: Simplified IAM for pods (replaces IRSA)
- **Aurora Limitless Database**: Horizontal write scaling
- **DynamoDB Standard-IA**: Infrequent access tables at 60% cost savings
- **RDS Blue/Green Deployments**: Zero-downtime version upgrades

## Related Skills

- **writing-infrastructure-code**: Multi-cloud IaC concepts, CDK and Terraform patterns
- **operating-kubernetes**: EKS cluster operations, kubectl, Helm charts
- **building-ci-pipelines**: CodePipeline, CodeBuild, GitHub Actions → AWS
- **managing-secrets**: Secrets Manager rotation, Parameter Store hierarchies
- **implementing-observability**: CloudWatch advanced queries, X-Ray distributed tracing
- **architecting-security**: IAM policy best practices, security automation
- **planning-disaster-recovery**: Multi-region strategies, backup automation

## References

- Full skill documentation: `/skills/deploying-on-aws/SKILL.md`
- Compute services: `/skills/deploying-on-aws/references/compute-services.md`
- Database services: `/skills/deploying-on-aws/references/database-services.md`
- Storage services: `/skills/deploying-on-aws/references/storage-services.md`
- Networking: `/skills/deploying-on-aws/references/networking.md`
- Security: `/skills/deploying-on-aws/references/security.md`
- Serverless patterns: `/skills/deploying-on-aws/references/serverless-patterns.md`
- Container patterns: `/skills/deploying-on-aws/references/container-patterns.md`
- Well-Architected: `/skills/deploying-on-aws/references/well-architected.md`
