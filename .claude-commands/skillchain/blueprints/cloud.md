# Cloud Deployment Blueprint

**Version:** 1.1.0
**Last Updated:** 2025-12-08
**Category:** Cloud Infrastructure

---

## Overview

Pre-configured skill chain optimized for deploying applications to cloud platforms (AWS, GCP, Azure). This blueprint provides production-ready infrastructure as code (IaC), security hardening, observability setup, and cost optimization defaults. Minimize cloud complexity while maximizing reliability, security, and cost efficiency.

---

## Trigger Keywords

**Primary (high confidence):**
- aws deployment
- gcp deployment
- azure deployment
- cloud deployment
- serverless
- lambda
- cloud infrastructure
- terraform
- aws infrastructure
- provision aws
- provision gcp
- provision azure

**Secondary (medium confidence):**
- cloud functions
- s3 bucket
- ec2 instance
- cloud run
- ecs
- fargate
- kubernetes
- docker deploy
- cloudformation
- infrastructure as code
- pulumi
- cdk

**Example goals that match:**
- "deploy my app to AWS"
- "serverless deployment with lambda"
- "containerized deployment on GCP"
- "set up AWS infrastructure with terraform"
- "deploy to azure with monitoring"
- "production-ready cloud deployment"
- "scalable cloud infrastructure"

---

## Skill Chain (Pre-configured)

This blueprint invokes 6 skills in the following order:

```
1. provisioning-terraform       (infrastructure as code - always required)
2. deploying-aws                (AWS deployment - primary provider)
   OR deploying-gcp             (GCP deployment - alternative)
   OR deploying-azure           (Azure deployment - alternative)
3. implementing-observability   (monitoring, logging, tracing)
4. hardening-security           (IAM, secrets, compliance)
5. optimizing-finops            (cost optimization, budgets)
6. assembling-infrastructure    (validation, documentation - always required)
```

**Total estimated time:** 30-45 minutes
**Total estimated questions:** 10-15 questions (or 3 with blueprint defaults)

---

## Pre-configured Defaults

### 1. provisioning-terraform
```yaml
iac_tool: "terraform"
  # HashiCorp Terraform for multi-cloud support
  # HCL syntax, state management, plan/apply workflow
  # Version: >= 1.6.0

provider: "aws"
  # Default to AWS (can override to gcp/azure)
  # Region: us-east-1 (can override per environment)
  # Provider version: ~> 5.0

state_backend: "s3"
  # Remote state storage in S3 + DynamoDB locking
  # State encryption enabled
  # Versioning enabled for rollback
  # Bucket: terraform-state-{project}-{env}
  # DynamoDB table: terraform-locks

modules: true
  # Reusable modules for common resources
  # modules/vpc/ - Network infrastructure
  # modules/compute/ - EC2, Lambda, containers
  # modules/database/ - RDS, DynamoDB
  # modules/storage/ - S3, EFS
  # modules/monitoring/ - CloudWatch, alarms

workspaces: ["dev", "staging", "prod"]
  # Separate environments via Terraform workspaces
  # dev: Single AZ, t3.small instances
  # staging: Multi-AZ, t3.medium instances
  # prod: Multi-AZ, t3.large+ instances, auto-scaling
```

### 2. deploying-aws (default provider)
```yaml
deployment_model: "serverless"
  # Options: serverless, containers, vms
  # Serverless: Lambda + API Gateway + DynamoDB
  # Containers: ECS Fargate + ALB + RDS
  # VMs: EC2 Auto Scaling + ALB + RDS

compute:
  serverless:
    runtime: "nodejs20.x"          # Lambda runtime
    memory: 1024                   # MB (128-10240)
    timeout: 30                    # Seconds (1-900)
    concurrent_executions: 100     # Reserved concurrency

  containers:
    platform: "ecs-fargate"        # Serverless containers
    cpu: 256                       # CPU units (256-4096)
    memory: 512                    # MB (512-30720)
    desired_count: 2               # Number of tasks

  vms:
    instance_type: "t3.medium"     # EC2 instance type
    ami: "amazon-linux-2023"       # OS image
    min_size: 2                    # Auto-scaling min
    max_size: 10                   # Auto-scaling max

networking:
  vpc_cidr: "10.0.0.0/16"          # VPC IP range
  subnets:
    public: ["10.0.1.0/24", "10.0.2.0/24"]
    private: ["10.0.11.0/24", "10.0.12.0/24"]
    database: ["10.0.21.0/24", "10.0.22.0/24"]
  nat_gateway: true                # Enable internet for private subnets
  multi_az: true                   # Deploy across availability zones

storage:
  primary: "s3"                    # Object storage (S3)
  database: "rds-postgres"         # Relational database
  cache: "elasticache-redis"       # Optional caching layer

  s3_config:
    versioning: true               # Keep object versions
    encryption: "AES256"           # Server-side encryption
    lifecycle_rules: true          # Auto-archive/delete old objects

  rds_config:
    engine: "postgres15"           # Database engine
    instance_class: "db.t3.medium" # Instance size
    multi_az: true                 # High availability
    backup_retention: 7            # Days to keep backups
    deletion_protection: true      # Prevent accidental deletion

auto_scaling:
  enabled: true                    # Enable auto-scaling
  target_cpu: 70                   # CPU percentage trigger
  target_memory: 80                # Memory percentage trigger
  scale_up_cooldown: 300           # Seconds before next scale-up
  scale_down_cooldown: 600         # Seconds before next scale-down
```

### 3. implementing-observability
```yaml
monitoring: "cloudwatch"
  # AWS CloudWatch for metrics, logs, alarms
  # Custom dashboards for key metrics
  # 1-minute metric granularity (production)
  # 5-minute granularity (dev/staging)

metrics:
  - cpu_utilization                # Compute resource usage
  - memory_utilization             # Memory usage
  - request_count                  # API request volume
  - error_count                    # Application errors
  - latency_p50                    # Median response time
  - latency_p99                    # 99th percentile response time
  - database_connections           # DB connection pool
  - storage_bytes                  # Storage usage

logging:
  retention: 30                    # Days (dev/staging)
  retention_prod: 90               # Days (production)
  format: "json"                   # Structured logging
  level: "info"                    # Default log level
  sampling: false                  # Don't sample in production

  log_groups:
    - /aws/lambda/{function}       # Lambda function logs
    - /ecs/{cluster}/{service}     # ECS container logs
    - /rds/{instance}              # Database logs
    - /application/access          # Access logs
    - /application/error           # Error logs

alarms:
  error_rate:
    threshold: 5                   # Percent errors
    evaluation_periods: 2          # Consecutive periods
    action: "sns-oncall"           # Alert on-call team

  high_latency:
    threshold: 1000                # Milliseconds (p99)
    evaluation_periods: 3
    action: "sns-oncall"

  high_cpu:
    threshold: 80                  # Percent
    evaluation_periods: 5
    action: "sns-team"             # Alert team (not urgent)

  database_connections:
    threshold: 80                  # Percent of max connections
    evaluation_periods: 2
    action: "sns-oncall"

tracing: "xray"
  # AWS X-Ray for distributed tracing
  # Trace all requests in production
  # Sample 10% in dev/staging
  # Service map visualization
  # Latency analysis by service

dashboards:
  - overview                       # High-level health metrics
  - compute                        # CPU, memory, instances
  - database                       # RDS metrics, connections
  - api                            # Request rate, latency, errors
  - cost                           # Daily spend by service
```

### 4. hardening-security
```yaml
iam:
  principle: "least-privilege"     # Minimal permissions required
  mfa_required: true               # Multi-factor authentication
  password_policy:
    min_length: 16
    require_symbols: true
    require_numbers: true
    max_age: 90                    # Days before rotation

  service_roles:
    - lambda-execution-role        # Lambda function permissions
    - ecs-task-role                # ECS container permissions
    - ec2-instance-role            # EC2 instance permissions

  assume_role_policy: true         # Cross-account access

secrets_management: "aws-secrets-manager"
  # Centralized secrets storage
  # Automatic rotation for database passwords
  # Encryption at rest (KMS)
  # Audit logging via CloudTrail

  secrets:
    - database-password            # RDS credentials
    - api-keys                     # Third-party API keys
    - jwt-secret                   # JWT signing key
    - encryption-key               # Application encryption

encryption:
  at_rest: true                    # Encrypt all storage
  in_transit: true                 # TLS for all network traffic
  kms_key: "custom"                # Customer-managed KMS key

  encrypted_resources:
    - s3-buckets                   # Object storage
    - ebs-volumes                  # EC2 disk volumes
    - rds-instances                # Database storage
    - elasticache                  # Cache data
    - lambda-env-vars              # Environment variables

network_security:
  vpc_isolation: true              # Private VPC
  security_groups:
    - alb-public                   # Allow 80/443 from internet
    - app-private                  # Allow traffic from ALB only
    - db-private                   # Allow traffic from app only

  nacls: true                      # Network ACLs for subnet-level filtering
  vpc_endpoints: true              # Private connections to AWS services

  waf: true                        # Web Application Firewall
  waf_rules:
    - rate-limiting                # Prevent DDoS (1000 req/5min)
    - sql-injection                # Block SQL injection attempts
    - xss-protection               # Block cross-site scripting
    - geo-blocking                 # Optional geographic restrictions

compliance:
  standards: ["soc2", "hipaa"]     # Compliance frameworks
  audit_logging: true              # CloudTrail enabled
  log_retention: 365               # Days for audit logs
  access_analyzer: true            # IAM Access Analyzer
  guardduty: true                  # Threat detection
  security_hub: true               # Centralized security findings
```

### 5. optimizing-finops
```yaml
cost_optimization:
  reserved_instances: false        # Start with on-demand, optimize later
  savings_plans: false             # Evaluate after 3 months
  spot_instances: false            # Not recommended for production initially

  right_sizing:
    enabled: true                  # Continuous resource optimization
    schedule: "weekly"             # Review and adjust weekly
    metrics: ["cpu", "memory", "network"]

  storage_optimization:
    s3_intelligent_tiering: true   # Auto-move to cheaper storage
    ebs_gp3: true                  # Use newer, cheaper volume type
    snapshot_lifecycle: true       # Auto-delete old snapshots

budgets:
  monthly_limit: 1000              # USD per month (customize)
  alerts:
    - threshold: 50                # Alert at 50% of budget
      action: "email-team"

    - threshold: 80                # Alert at 80% of budget
      action: "email-leadership"

    - threshold: 100               # Alert at 100% of budget
      action: "email-leadership-urgent"

  forecasting: true                # Predict month-end costs

tagging:
  required_tags:
    - Environment                  # dev, staging, prod
    - Project                      # Project name
    - Owner                        # Team or individual
    - CostCenter                   # Billing allocation
    - Terraform                    # "true" for IaC-managed resources

  tag_enforcement: true            # Prevent untagged resources
  tag_policies: true               # Centralized tag governance

cost_reporting:
  frequency: "daily"               # Daily cost reports
  breakdown_by: ["service", "environment", "project"]
  anomaly_detection: true          # Alert on unusual spend
  showback: true                   # Per-team cost visibility
```

### 6. assembling-infrastructure
```yaml
validation:
  terraform_validate: true         # Validate HCL syntax
  terraform_fmt: true              # Format code consistently
  tflint: true                     # Terraform linting
  checkov: true                    # Security scanning
  cost_estimation: true            # Infracost for cost preview

documentation:
  auto_generate: true              # Auto-generate from Terraform
  architecture_diagram: true       # Network and resource diagram
  runbook: true                    # Operational procedures
  disaster_recovery: true          # Backup and restore procedures

  includes:
    - infrastructure-overview.md   # High-level architecture
    - deployment-guide.md          # Step-by-step deployment
    - troubleshooting.md           # Common issues and solutions
    - cost-optimization.md         # Cost reduction strategies
    - security-checklist.md        # Security review checklist

ci_cd:
  pipeline: "github-actions"       # Default CI/CD tool
  stages:
    - validate                     # terraform validate, tflint
    - plan                         # terraform plan
    - security-scan                # checkov, tfsec
    - cost-estimate                # infracost
    - apply                        # terraform apply (manual approval)

  environments:
    dev: "auto-deploy"             # Auto-deploy on merge to dev
    staging: "auto-deploy"         # Auto-deploy on merge to staging
    prod: "manual-approval"        # Require approval for production

backup_restore:
  automated_backups: true          # Daily automated backups
  backup_schedule: "daily-1am"     # 1 AM UTC
  retention: 30                    # Days
  cross_region: true               # Backup to secondary region
  test_restores: "monthly"         # Monthly restore tests
```

---

## Quick Questions (Only 3)

When blueprint is detected, ask only these essential questions:

### Question 1: Cloud Provider
```
Which cloud provider will you use?

Options:
1. AWS (Amazon Web Services) - recommended, most mature
2. GCP (Google Cloud Platform) - great for data/ML workloads
3. Azure (Microsoft Azure) - best for .NET/Microsoft stack

Your answer (1/2/3): _______________
```

**Why this matters:**
- Determines which deployment skill is invoked
- Affects available services and pricing
- Changes IaC provider configuration

**Default if skipped:** "AWS (Amazon Web Services)"

---

### Question 2: Deployment Model
```
How will you deploy your application?

Options:
1. Serverless - Lambda functions, API Gateway, DynamoDB (lowest ops, auto-scale)
2. Containers - ECS/Fargate or Cloud Run (balanced ops, flexible)
3. Virtual Machines - EC2 or Compute Engine (full control, higher ops)

Your answer (1/2/3): _______________
```

**Why this matters:**
- Determines compute resources provisioned
- Affects cost model (pay-per-use vs. reserved)
- Influences auto-scaling strategy
- Changes operational complexity

**Default if skipped:** "Serverless" (lowest operational overhead)

---

### Question 3: Environment Tier
```
What environment tier are you deploying?

Options:
1. Development/Test - minimal resources, cost-optimized
2. Staging - production-like, used for testing before prod
3. Production - high availability, multi-AZ, full monitoring

Your answer (1/2/3): _______________
```

**Why this matters:**
- Determines instance sizes and counts
- Affects high-availability configuration (multi-AZ, replicas)
- Changes monitoring granularity and alerting
- Influences backup and disaster recovery settings
- Impacts cost significantly

**Default if skipped:** "Production" (safest, most robust)

---

## Blueprint Detection Logic

Trigger this blueprint when the user's goal matches:

```python
def should_use_cloud_blueprint(goal: str) -> bool:
    goal_lower = goal.lower()

    # Primary keywords (high confidence)
    primary_match = any(keyword in goal_lower for keyword in [
        "aws deployment",
        "gcp deployment",
        "azure deployment",
        "cloud deployment",
        "deploy to aws",
        "deploy to gcp",
        "deploy to azure",
        "serverless",
        "lambda deployment"
    ])

    # Secondary keywords + deployment context
    secondary_match = (
        any(keyword in goal_lower for keyword in [
            "aws", "gcp", "azure", "cloud", "lambda", "ec2",
            "s3", "ecs", "fargate", "cloud run", "cloud functions"
        ]) and
        any(keyword in goal_lower for keyword in [
            "deploy", "infrastructure", "provision", "terraform",
            "cloudformation", "setup"
        ])
    )

    # Infrastructure as Code mention
    iac_match = any(keyword in goal_lower for keyword in [
        "terraform", "cloudformation", "pulumi", "infrastructure as code", "iac"
    ])

    return primary_match or secondary_match or iac_match
```

**Confidence levels:**
- **High (90%+):** Contains "{provider} deployment" or "deploy to {provider}"
- **Medium (70-89%):** Contains cloud provider + deployment term
- **Low (50-69%):** Contains IaC tool mention without explicit deployment

**Present blueprint when confidence >= 70%**

---

## Blueprint Offer Message

When blueprint is detected, present this message to the user:

```
┌────────────────────────────────────────────────────────────┐
│ ☁️  CLOUD DEPLOYMENT BLUEPRINT DETECTED                    │
├────────────────────────────────────────────────────────────┤
│ Your goal matches our optimized Cloud Deployment Blueprint│
│                                                            │
│ Pre-configured features:                                   │
│  ✓ Infrastructure as Code (Terraform)                     │
│  ✓ Multi-environment setup (dev/staging/prod)             │
│  ✓ Auto-scaling and high availability                     │
│  ✓ Comprehensive monitoring and alerting                  │
│  ✓ Security hardening (IAM, encryption, WAF)              │
│  ✓ Cost optimization and budgets                          │
│  ✓ Automated backups and disaster recovery                │
│  ✓ CI/CD pipeline integration                             │
│                                                            │
│ Using blueprint reduces questions from 15 to 3!           │
│                                                            │
│ Options:                                                   │
│  1. Use blueprint (3 quick questions, ~10 min)            │
│  2. Custom configuration (15 questions, ~40 min)          │
│  3. Skip all questions (use all defaults, ~5 min)         │
│                                                            │
│ Your choice (1/2/3): _____                                │
└────────────────────────────────────────────────────────────┘
```

**Handle responses:**
- **1 or "blueprint"** → Ask only 3 blueprint questions
- **2 or "custom"** → Ask all skill questions (normal flow)
- **3 or "skip"** → Use all defaults, skip all questions

---

## Generated Output Structure

When blueprint is executed, generate this file structure:

```
cloud-infrastructure/
├── terraform/                             # Infrastructure as Code
│   ├── main.tf                            # Root configuration
│   ├── variables.tf                       # Input variables
│   ├── outputs.tf                         # Output values
│   ├── terraform.tfvars                   # Variable values (gitignored)
│   ├── backend.tf                         # Remote state configuration
│   ├── providers.tf                       # Cloud provider setup
│   │
│   ├── modules/                           # Reusable modules
│   │   ├── vpc/                           # Virtual Private Cloud
│   │   │   ├── main.tf                    # VPC, subnets, route tables
│   │   │   ├── variables.tf
│   │   │   ├── outputs.tf
│   │   │   └── README.md
│   │   │
│   │   ├── compute/                       # Compute resources
│   │   │   ├── lambda/                    # Serverless functions
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── ecs/                       # Container orchestration
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   └── ec2/                       # Virtual machines
│   │   │       ├── main.tf
│   │   │       ├── variables.tf
│   │   │       └── outputs.tf
│   │   │
│   │   ├── database/                      # Database resources
│   │   │   ├── main.tf                    # RDS, DynamoDB, etc.
│   │   │   ├── variables.tf
│   │   │   ├── outputs.tf
│   │   │   └── README.md
│   │   │
│   │   ├── storage/                       # Storage resources
│   │   │   ├── main.tf                    # S3, EFS, etc.
│   │   │   ├── variables.tf
│   │   │   ├── outputs.tf
│   │   │   └── README.md
│   │   │
│   │   ├── monitoring/                    # Observability
│   │   │   ├── main.tf                    # CloudWatch, alarms, dashboards
│   │   │   ├── variables.tf
│   │   │   ├── outputs.tf
│   │   │   └── README.md
│   │   │
│   │   ├── security/                      # Security resources
│   │   │   ├── iam.tf                     # IAM roles and policies
│   │   │   ├── secrets.tf                 # Secrets Manager
│   │   │   ├── waf.tf                     # Web Application Firewall
│   │   │   ├── variables.tf
│   │   │   ├── outputs.tf
│   │   │   └── README.md
│   │   │
│   │   └── networking/                    # Network security
│   │       ├── security-groups.tf         # Security groups
│   │       ├── nacls.tf                   # Network ACLs
│   │       ├── vpc-endpoints.tf           # VPC endpoints
│   │       ├── variables.tf
│   │       ├── outputs.tf
│   │       └── README.md
│   │
│   ├── environments/                      # Environment-specific configs
│   │   ├── dev/
│   │   │   ├── main.tf                    # Dev environment
│   │   │   ├── variables.tf
│   │   │   └── terraform.tfvars
│   │   ├── staging/
│   │   │   ├── main.tf                    # Staging environment
│   │   │   ├── variables.tf
│   │   │   └── terraform.tfvars
│   │   └── prod/
│   │       ├── main.tf                    # Production environment
│   │       ├── variables.tf
│   │       └── terraform.tfvars
│   │
│   └── scripts/                           # Utility scripts
│       ├── init.sh                        # Initialize Terraform
│       ├── plan.sh                        # Generate plan
│       ├── apply.sh                       # Apply changes
│       ├── destroy.sh                     # Destroy infrastructure
│       └── cost-estimate.sh               # Infracost estimation
│
├── .github/                               # CI/CD workflows
│   └── workflows/
│       ├── terraform-plan.yml             # PR validation
│       ├── terraform-apply-dev.yml        # Auto-deploy dev
│       ├── terraform-apply-staging.yml    # Auto-deploy staging
│       └── terraform-apply-prod.yml       # Manual prod deployment
│
├── docs/                                  # Documentation
│   ├── architecture/
│   │   ├── overview.md                    # High-level architecture
│   │   ├── network-diagram.png            # VPC and network layout
│   │   └── resource-diagram.png           # All cloud resources
│   │
│   ├── deployment/
│   │   ├── getting-started.md             # Initial setup
│   │   ├── deployment-guide.md            # Step-by-step deployment
│   │   └── rollback-procedures.md         # How to rollback changes
│   │
│   ├── operations/
│   │   ├── monitoring.md                  # Monitoring and alerting
│   │   ├── troubleshooting.md             # Common issues
│   │   ├── scaling.md                     # Scaling procedures
│   │   └── backup-restore.md              # Backup and recovery
│   │
│   ├── security/
│   │   ├── security-checklist.md          # Pre-launch security review
│   │   ├── iam-guide.md                   # IAM best practices
│   │   ├── secrets-management.md          # Managing secrets
│   │   └── compliance.md                  # Compliance requirements
│   │
│   └── cost/
│       ├── cost-optimization.md           # Cost reduction strategies
│       ├── budgets-alerts.md              # Budget configuration
│       └── showback.md                    # Per-team cost allocation
│
├── monitoring/                            # Monitoring configuration
│   ├── dashboards/
│   │   ├── overview.json                  # CloudWatch dashboard - overview
│   │   ├── compute.json                   # Compute metrics
│   │   ├── database.json                  # Database metrics
│   │   └── cost.json                      # Cost metrics
│   │
│   └── alarms/
│       ├── critical.tf                    # Critical alarms (page on-call)
│       ├── warning.tf                     # Warning alarms (notify team)
│       └── informational.tf               # Info alarms (logs only)
│
├── scripts/                               # Operational scripts
│   ├── deploy.sh                          # Master deployment script
│   ├── validate.sh                        # Pre-deployment validation
│   ├── backup.sh                          # Manual backup trigger
│   ├── restore.sh                         # Restore from backup
│   └── health-check.sh                    # Post-deployment health check
│
├── tests/                                 # Infrastructure tests
│   ├── terraform/
│   │   ├── validate_test.go               # Terraform validation tests
│   │   └── security_test.go               # Security policy tests
│   │
│   └── integration/
│       ├── smoke_test.sh                  # Basic connectivity tests
│       └── load_test.sh                   # Performance tests
│
├── .gitignore                             # Git ignore (secrets, state files)
├── .tflint.hcl                            # Terraform linting config
├── .checkov.yml                           # Security scanning config
├── README.md                              # Project overview
└── RUNBOOK.md                             # Operational runbook
```

---

## Infrastructure Architecture

### Serverless Architecture (Default)

```
┌──────────────────────────────────────────────────────────────┐
│                        Internet                              │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   CloudFront    │ (Optional CDN)
                    │   + WAF         │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  API Gateway    │ (REST/HTTP API)
                    │  + WAF Rules    │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
    ┌─────────┐        ┌─────────┐        ┌─────────┐
    │ Lambda  │        │ Lambda  │        │ Lambda  │
    │ Function│        │ Function│        │ Function│
    │    1    │        │    2    │        │    3    │
    └────┬────┘        └────┬────┘        └────┬────┘
         │                  │                  │
         └──────────────────┼──────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
       ┌─────────┐    ┌──────────┐    ┌────────┐
       │DynamoDB │    │    S3    │    │Secrets │
       │  Tables │    │  Bucket  │    │Manager │
       └─────────┘    └──────────┘    └────────┘

Monitoring Layer (All Resources):
┌──────────────────────────────────────────────┐
│  CloudWatch Logs + Metrics + Alarms + X-Ray │
└──────────────────────────────────────────────┘
```

### Container Architecture (ECS Fargate)

```
┌──────────────────────────────────────────────────────────────┐
│                        Internet                              │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                      VPC (10.0.0.0/16)                      │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │           Public Subnets (2 AZs)                      │ │
│  │                                                       │ │
│  │  ┌─────────────────────────────┐                     │ │
│  │  │  Application Load Balancer  │                     │ │
│  │  │  (ALB) + WAF                │                     │ │
│  │  └──────────────┬──────────────┘                     │ │
│  └─────────────────┼────────────────────────────────────┘ │
│                    │                                       │
│  ┌─────────────────▼────────────────────────────────────┐ │
│  │          Private Subnets (2 AZs)                     │ │
│  │                                                      │ │
│  │  ┌──────────────┐         ┌──────────────┐          │ │
│  │  │ ECS Fargate  │         │ ECS Fargate  │          │ │
│  │  │   Task 1     │         │   Task 2     │          │ │
│  │  │ (Container)  │         │ (Container)  │          │ │
│  │  └──────┬───────┘         └──────┬───────┘          │ │
│  │         │                        │                  │ │
│  │         └────────────┬───────────┘                  │ │
│  └──────────────────────┼──────────────────────────────┘ │
│                         │                                 │
│  ┌──────────────────────▼──────────────────────────────┐ │
│  │         Database Subnets (2 AZs)                    │ │
│  │                                                     │ │
│  │  ┌──────────────┐         ┌──────────────┐         │ │
│  │  │     RDS      │◄───────►│     RDS      │         │ │
│  │  │   Primary    │         │   Replica    │         │ │
│  │  └──────────────┘         └──────────────┘         │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  NAT Gateway (internet for private subnets)        │ │
│  └─────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘

External Services:
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│    S3    │  │  Secrets │  │CloudWatch│  │   X-Ray  │
│  Bucket  │  │ Manager  │  │Logs/Alarms│ │  Tracing │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
```

---

## Region Selection Strategy

### Default Region by Provider

```yaml
aws:
  primary: "us-east-1"       # N. Virginia (most services, lowest cost)
  secondary: "us-west-2"     # Oregon (disaster recovery)

gcp:
  primary: "us-central1"     # Iowa (balanced performance/cost)
  secondary: "us-east1"      # South Carolina (disaster recovery)

azure:
  primary: "eastus"          # Virginia (most services)
  secondary: "westus2"       # Washington (disaster recovery)
```

### Multi-Region Considerations

**Enable multi-region when:**
- Compliance requires data residency
- Global user base needs low latency
- Disaster recovery SLA < 1 hour
- Budget supports 2x infrastructure cost

**Start single-region for:**
- Regional user base
- Development/staging environments
- Budget constraints
- Simpler operations preferred

---

## Auto-Scaling Policies

### Serverless (Lambda)
```yaml
scaling:
  type: "automatic"              # AWS manages scaling
  concurrent_executions: 100     # Reserved concurrency
  provisioned_concurrency: 0     # Optional warm instances

throttling:
  burst_limit: 1000              # Concurrent executions
  rate_limit: 500                # Requests per second
```

### Containers (ECS)
```yaml
scaling:
  min_tasks: 2                   # Minimum running tasks
  max_tasks: 10                  # Maximum running tasks
  desired_tasks: 2               # Initial task count

  policies:
    - type: "target-tracking"
      metric: "cpu-utilization"
      target: 70                 # Percent

    - type: "target-tracking"
      metric: "memory-utilization"
      target: 80                 # Percent

    - type: "target-tracking"
      metric: "request-count-per-target"
      target: 1000               # Requests per task
```

### Virtual Machines (EC2)
```yaml
scaling:
  min_instances: 2               # Minimum instances
  max_instances: 10              # Maximum instances
  desired_instances: 2           # Initial count

  policies:
    - type: "target-tracking"
      metric: "cpu-utilization"
      target: 70                 # Percent
      scale_out_cooldown: 300    # Seconds
      scale_in_cooldown: 600     # Seconds
```

---

## Backup and Disaster Recovery

### Automated Backups

```yaml
rds_backups:
  automated: true                # Daily automated backups
  window: "03:00-04:00"          # UTC backup window
  retention: 7                   # Days (dev/staging)
  retention_prod: 30             # Days (production)
  cross_region: true             # Copy to secondary region

s3_versioning:
  enabled: true                  # Keep object versions
  mfa_delete: true               # Require MFA to delete
  lifecycle:
    - transition_to_ia: 30       # Days until Infrequent Access
    - transition_to_glacier: 90  # Days until Glacier
    - expire: 365                # Days until deletion

ebs_snapshots:
  schedule: "daily"              # Daily snapshots
  retention: 7                   # Days
  cross_region: true             # Copy to secondary region
```

### Disaster Recovery Plan

```yaml
rto: 1                           # Recovery Time Objective (hours)
rpo: 15                          # Recovery Point Objective (minutes)

strategy: "warm-standby"
  # Options: backup-restore, pilot-light, warm-standby, active-active
  # warm-standby: Minimal resources running in DR region, scale up on failover

dr_region: "us-west-2"           # Disaster recovery region
dr_testing: "quarterly"          # Test failover quarterly

failover_triggers:
  - region-outage                # Primary region down
  - data-center-failure          # Availability zone failure
  - security-breach              # Security incident
  - manual-initiation            # Manual DR drill
```

---

## Cost Optimization Strategies

### Initial Deployment (Month 1-3)
```yaml
approach: "baseline-establishment"
  # Use on-demand instances to understand usage patterns
  # No upfront commitments
  # Monitor cost and utilization closely

focus:
  - right-sizing                 # Ensure instances aren't over-provisioned
  - unused-resources             # Delete idle resources
  - tagging                      # Enable cost allocation
```

### Optimization Phase (Month 4-6)
```yaml
approach: "strategic-commitments"
  # Purchase Savings Plans or Reserved Instances
  # 1-year commitment for predictable workloads
  # Continue on-demand for variable workloads

savings_plans:
  coverage: 70                   # Percent of compute spend
  term: "1-year"                 # Commitment length
  payment: "no-upfront"          # Payment option

focus:
  - storage-tiering              # Move cold data to cheaper tiers
  - data-transfer                # Optimize cross-region transfers
  - lambda-memory                # Right-size Lambda memory
```

### Mature Operations (Month 7+)
```yaml
approach: "continuous-optimization"
  # Regular reviews and adjustments
  # Spot instances for fault-tolerant workloads
  # Reserved capacity for stable workloads

advanced_strategies:
  - spot-instances               # 70-90% discount for interruptible workloads
  - auto-shutdowns               # Stop dev/staging after hours
  - container-density            # Optimize task packing
  - serverless-first             # Prefer serverless to reduce idle costs
```

---

## Security Checklist

Before going to production, verify:

### Network Security
- [ ] VPC with private subnets for compute/database
- [ ] Public subnets only for load balancers
- [ ] Security groups follow least-privilege (minimal ports)
- [ ] Network ACLs configured for subnet-level filtering
- [ ] VPC Flow Logs enabled for traffic analysis
- [ ] NAT Gateway in public subnet (not instances)
- [ ] VPC endpoints for AWS service access (no internet routing)

### Identity and Access
- [ ] Root account MFA enabled
- [ ] IAM users with MFA enabled
- [ ] Service roles with least-privilege policies
- [ ] No hardcoded credentials in code
- [ ] Secrets in Secrets Manager, not environment variables
- [ ] CloudTrail enabled for audit logging
- [ ] IAM Access Analyzer enabled

### Data Protection
- [ ] Encryption at rest for all storage (S3, RDS, EBS)
- [ ] Encryption in transit (TLS 1.2+ everywhere)
- [ ] KMS customer-managed keys (not AWS-managed)
- [ ] Database backups encrypted
- [ ] S3 bucket policies deny unencrypted uploads
- [ ] S3 versioning enabled for critical buckets
- [ ] S3 public access blocked by default

### Application Security
- [ ] WAF enabled on ALB/API Gateway/CloudFront
- [ ] WAF rules for SQL injection, XSS, rate limiting
- [ ] GuardDuty enabled for threat detection
- [ ] Security Hub enabled for findings aggregation
- [ ] Secrets rotation configured (90-day max)
- [ ] Container image scanning enabled
- [ ] Lambda environment variables encrypted

### Monitoring and Response
- [ ] CloudWatch alarms for critical metrics
- [ ] SNS topics for on-call notifications
- [ ] Log aggregation in CloudWatch Logs
- [ ] Log retention configured (30+ days production)
- [ ] X-Ray tracing enabled for distributed systems
- [ ] Incident response runbook documented
- [ ] Security contact configured in AWS account

---

## Dependencies

### Required Tools
```bash
# Terraform
terraform >= 1.6.0

# AWS CLI (if using AWS)
aws-cli >= 2.0.0

# Google Cloud SDK (if using GCP)
gcloud >= 400.0.0

# Azure CLI (if using Azure)
az >= 2.50.0

# Optional but recommended
tflint >= 0.48.0          # Terraform linting
checkov >= 2.4.0          # Security scanning
infracost >= 0.10.0       # Cost estimation
terraform-docs >= 0.16.0  # Auto-generate docs
```

### CI/CD Requirements
```yaml
github_actions:
  secrets:
    - AWS_ACCESS_KEY_ID         # AWS credentials (or OIDC)
    - AWS_SECRET_ACCESS_KEY
    - TERRAFORM_CLOUD_TOKEN     # Optional: Terraform Cloud

  permissions:
    id-token: write             # For OIDC auth
    contents: read
    pull-requests: write        # Comment on PRs with plan
```

---

## Terraform State Management

### Remote State (Recommended)

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "terraform-state-myproject-prod"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"

    # Optional: Terraform Cloud
    # organization = "my-org"
    # workspaces {
    #   name = "myproject-prod"
    # }
  }
}
```

### State Locking

```hcl
# DynamoDB table for state locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name        = "Terraform State Lock Table"
    Environment = "shared"
  }
}
```

---

## Environment-Specific Configurations

### Development
```yaml
resources:
  compute: "minimal"             # t3.small, 128MB Lambda
  database: "single-az"          # db.t3.micro, no replicas
  monitoring: "basic"            # 5-min metrics, 7-day logs

scaling:
  enabled: false                 # No auto-scaling

backups:
  retention: 3                   # Days
  cross_region: false

cost:
  target: "lowest"               # Optimize for minimum cost
```

### Staging
```yaml
resources:
  compute: "moderate"            # t3.medium, 512MB Lambda
  database: "multi-az"           # db.t3.small, 1 replica
  monitoring: "enhanced"         # 1-min metrics, 30-day logs

scaling:
  enabled: true                  # Auto-scaling enabled
  max: 5                         # Limited max capacity

backups:
  retention: 7                   # Days
  cross_region: false

cost:
  target: "balanced"             # Balance cost and performance
```

### Production
```yaml
resources:
  compute: "robust"              # t3.large+, 1024MB Lambda
  database: "multi-az"           # db.t3.medium+, 2+ replicas
  monitoring: "comprehensive"    # 1-min metrics, 90-day logs

scaling:
  enabled: true                  # Auto-scaling enabled
  max: 20                        # High max capacity

backups:
  retention: 30                  # Days
  cross_region: true             # Disaster recovery

cost:
  target: "reliability"          # Optimize for uptime, not cost
```

---

## Customization Points

After blueprint generation, easily customize:

1. **Region selection:** Edit `providers.tf` region values
2. **Instance sizes:** Update `variables.tf` instance type defaults
3. **Scaling policies:** Modify auto-scaling thresholds in modules
4. **Monitoring alarms:** Adjust alarm thresholds in `monitoring/alarms/`
5. **Cost budgets:** Update budget amounts in `optimizing-finops` module
6. **Security rules:** Customize WAF rules, security groups
7. **Backup schedules:** Change backup windows and retention

---

## Migration Path

Add features after initial deployment:

1. **Add CDN:** Run `/skillchain cloudfront-cdn` (AWS) or equivalent
2. **Add CI/CD:** Run `/skillchain github-actions-cicd`
3. **Add monitoring dashboards:** Run `/skillchain grafana-dashboards`
4. **Add container registry:** Run `/skillchain ecr-registry` (AWS)
5. **Add service mesh:** Run `/skillchain service-mesh` (advanced)

---

## Validation and Testing

### Pre-Deployment Validation
```bash
# Terraform validation
terraform init
terraform validate
terraform fmt -check

# Linting
tflint --recursive

# Security scanning
checkov --directory terraform/

# Cost estimation
infracost breakdown --path terraform/
```

### Post-Deployment Testing
```bash
# Infrastructure smoke tests
./scripts/health-check.sh

# Load testing (staging)
./tests/integration/load_test.sh

# Disaster recovery drill (quarterly)
./scripts/dr-failover-test.sh
```

---

## Troubleshooting

### Common Issues

**Issue: Terraform state locked**
```bash
# Solution: Force unlock (use with caution)
terraform force-unlock <LOCK_ID>
```

**Issue: Resources quota exceeded**
```bash
# Solution: Request limit increase in AWS Service Quotas
aws service-quotas request-service-quota-increase \
  --service-code ec2 \
  --quota-code L-1216C47A \
  --desired-value 20
```

**Issue: High data transfer costs**
```bash
# Solution: Enable VPC endpoints for AWS services
# Avoid cross-region transfers when possible
# Use CloudFront for static assets
```

---

## Related Blueprints

- **Kubernetes Blueprint:** For container orchestration with EKS/GKE/AKS
- **Serverless API Blueprint:** For API-focused serverless deployments
- **Data Pipeline Blueprint:** For ETL and data processing workloads
- **ML Deployment Blueprint:** For machine learning model serving

---

## Version History

**1.0.0** (2024-12-06)
- Initial cloud deployment blueprint
- 6-skill chain with multi-cloud support
- 3-question quick configuration
- Terraform as default IaC tool
- AWS as default provider
- Serverless as default deployment model
- Comprehensive security and cost optimization
- Full observability stack

---

**Blueprint Complete**
