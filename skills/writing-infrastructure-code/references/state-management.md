# State Management - Remote State, Locking, and Isolation

Comprehensive guide to infrastructure state management patterns across Terraform and Pulumi.

## Table of Contents

1. [State Fundamentals](#state-fundamentals)
2. [Remote State Backends](#remote-state-backends)
3. [State Locking](#state-locking)
4. [State Isolation Strategies](#state-isolation-strategies)
5. [Sensitive Data in State](#sensitive-data-in-state)
6. [State Operations](#state-operations)
7. [State Recovery](#state-recovery)
8. [Migration Patterns](#migration-patterns)

---

## State Fundamentals

### What is State?

Infrastructure state tracks the mapping between your code and real cloud resources:

**Terraform State:**
- JSON file mapping resource names to cloud resource IDs
- Stores resource metadata (ARNs, IPs, etc.)
- Tracks dependencies between resources
- Contains sensitive data (passwords, keys)

**Pulumi State:**
- Checkpoint files tracking resource state
- Supports Pulumi Service or self-managed backends
- Encrypted by default
- Includes secrets management

### Why Remote State?

**Problems with Local State:**
- ❌ Team collaboration impossible (state on one machine)
- ❌ No locking (concurrent runs corrupt state)
- ❌ No encryption at rest
- ❌ No versioning/rollback
- ❌ CI/CD requires shared storage

**Benefits of Remote State:**
- ✅ Team collaboration (shared state)
- ✅ State locking (prevents corruption)
- ✅ Encryption at rest
- ✅ Versioning and rollback
- ✅ CI/CD integration

---

## Remote State Backends

### Terraform - S3 Backend with DynamoDB Locking

**Bootstrap State Backend (One-Time Setup):**

```hcl
# bootstrap/state-bucket.tf
# Run this FIRST with local state, then migrate to S3

provider "aws" {
  region = "us-east-1"
}

# S3 bucket for state files
resource "aws_s3_bucket" "terraform_state" {
  bucket = "company-terraform-state-12345"  # Must be globally unique

  lifecycle {
    prevent_destroy = true  # Never accidentally destroy state bucket
  }

  tags = {
    Name        = "Terraform State Bucket"
    Environment = "shared"
    Purpose     = "terraform-state"
  }
}

# Enable versioning for rollback capability
resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Enable encryption at rest
resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.terraform_state.arn
    }
  }
}

# Block public access
resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# KMS key for encryption
resource "aws_kms_key" "terraform_state" {
  description             = "KMS key for Terraform state encryption"
  deletion_window_in_days = 10
  enable_key_rotation     = true

  tags = {
    Name = "terraform-state-key"
  }
}

resource "aws_kms_alias" "terraform_state" {
  name          = "alias/terraform-state"
  target_key_id = aws_kms_key.terraform_state.key_id
}

# DynamoDB table for state locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  lifecycle {
    prevent_destroy = true
  }

  tags = {
    Name        = "Terraform State Lock Table"
    Environment = "shared"
  }
}

# Outputs for backend configuration
output "state_bucket_name" {
  value       = aws_s3_bucket.terraform_state.bucket
  description = "Name of the S3 bucket for Terraform state"
}

output "dynamodb_table_name" {
  value       = aws_dynamodb_table.terraform_locks.name
  description = "Name of the DynamoDB table for state locking"
}

output "kms_key_id" {
  value       = aws_kms_key.terraform_state.id
  description = "KMS key ID for state encryption"
}
```

**Bootstrap Deployment:**
```bash
# Step 1: Initialize with local state
cd bootstrap/
terraform init

# Step 2: Apply to create state backend
terraform apply

# Step 3: Note outputs for backend configuration
terraform output

# Step 4: Migrate to remote state (optional)
# Add backend.tf (below), then:
terraform init -migrate-state
```

**Using S3 Backend:**

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "company-terraform-state-12345"
    key            = "prod/vpc/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    kms_key_id     = "arn:aws:kms:us-east-1:123456789012:key/abc123"
    dynamodb_table = "terraform-state-locks"

    # Optional: Workspace-specific state paths
    # workspace_key_prefix = "workspaces"
  }
}
```

**Partial Backend Configuration (Recommended):**

```hcl
# backend.tf (static - committed to Git)
terraform {
  backend "s3" {}
}
```

```hcl
# backend-prod.tfbackend (dynamic - not committed)
bucket         = "company-terraform-state-12345"
key            = "prod/vpc/terraform.tfstate"
region         = "us-east-1"
encrypt        = true
kms_key_id     = "arn:aws:kms:us-east-1:123456789012:key/abc123"
dynamodb_table = "terraform-state-locks"
```

```bash
# Initialize with backend config
terraform init -backend-config=backend-prod.tfbackend
```

### Terraform - GCS Backend (Google Cloud)

```hcl
terraform {
  backend "gcs" {
    bucket = "company-terraform-state"
    prefix = "prod/vpc"

    # Optional: encryption
    encryption_key = "your-base64-encoded-encryption-key"
  }
}
```

### Terraform - Azure Blob Backend

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "companytfstate"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

### Terraform Cloud/Enterprise

```hcl
terraform {
  cloud {
    organization = "company-name"

    workspaces {
      name = "prod-vpc"
    }
  }
}
```

### Pulumi State Backends

**Pulumi Service (Default):**
```bash
# Automatic - no configuration needed
pulumi login

# Deploy
pulumi up
```

**Self-Managed S3 Backend:**
```bash
# Login to S3 backend
pulumi login s3://company-pulumi-state

# Set region
pulumi stack init prod --secrets-provider=awskms://alias/pulumi-secrets

# Deploy
pulumi up
```

**Azure Blob Backend:**
```bash
pulumi login azblob://container-name
```

**Google Cloud Storage Backend:**
```bash
pulumi login gs://bucket-name
```

**Local Backend (Not Recommended for Teams):**
```bash
pulumi login --local
```

---

## State Locking

### Terraform State Locking

**How Locking Works:**
1. `terraform apply` acquires lock via DynamoDB
2. Lock prevents concurrent operations
3. Lock released after apply completes
4. Failed operations auto-release after timeout

**Manual Lock Management:**
```bash
# View lock information
terraform force-unlock <lock-id>

# Only use force-unlock if certain no other process is running
# Better: wait for lock to release naturally or investigate
```

**Lock Timeout:**
```bash
# Set custom lock timeout (default: 0s = no timeout)
terraform apply -lock-timeout=10m
```

### Pulumi State Locking

Pulumi automatically handles locking:
- Pulumi Service: Built-in locking
- Self-managed backends: File-based locking

```bash
# Cancel ongoing operation (releases lock)
pulumi cancel
```

---

## State Isolation Strategies

### Strategy 1: Directory Separation (Recommended)

**Structure:**
```
infrastructure/
├── environments/
│   ├── prod/
│   │   ├── networking/
│   │   │   ├── main.tf
│   │   │   └── backend.tf  # key: prod/networking/terraform.tfstate
│   │   ├── compute/
│   │   │   ├── main.tf
│   │   │   └── backend.tf  # key: prod/compute/terraform.tfstate
│   │   └── data/
│   │       ├── main.tf
│   │       └── backend.tf  # key: prod/data/terraform.tfstate
│   ├── staging/
│   │   ├── networking/
│   │   │   └── backend.tf  # key: staging/networking/terraform.tfstate
│   │   └── ...
│   └── dev/
│       └── ...
└── modules/
    └── ...
```

**Benefits:**
- ✅ Complete state isolation
- ✅ No risk of cross-environment changes
- ✅ Clear separation of concerns
- ✅ Easy to understand

**Drawbacks:**
- ⚠️ Code duplication across environments
- ⚠️ Must keep environments in sync manually

**Mitigate with Modules:**
```hcl
# environments/prod/networking/main.tf
module "vpc" {
  source = "../../../modules/vpc"

  environment = "prod"
  cidr_block  = "10.0.0.0/16"
}

# environments/staging/networking/main.tf
module "vpc" {
  source = "../../../modules/vpc"

  environment = "staging"
  cidr_block  = "10.1.0.0/16"
}
```

### Strategy 2: Workspaces

**Structure:**
```
infrastructure/
├── main.tf
├── variables.tf
├── backend.tf  # Single backend, workspace-specific keys
└── terraform.tfvars
```

**Backend Configuration:**
```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "vpc/terraform.tfstate"  # Workspace name prepended automatically
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
    workspace_key_prefix = "environments"  # Results in: environments/prod/vpc/terraform.tfstate
  }
}
```

**Usage:**
```bash
# Create workspaces
terraform workspace new prod
terraform workspace new staging
terraform workspace new dev

# Switch workspace
terraform workspace select prod

# List workspaces
terraform workspace list

# Current workspace
terraform workspace show
```

**Workspace-Aware Code:**
```hcl
locals {
  environment = terraform.workspace

  instance_type = {
    prod    = "t3.large"
    staging = "t3.medium"
    dev     = "t3.micro"
  }[terraform.workspace]

  instance_count = {
    prod    = 3
    staging = 2
    dev     = 1
  }[terraform.workspace]
}

resource "aws_instance" "app" {
  count         = local.instance_count
  instance_type = local.instance_type
  # ...
}
```

**Benefits:**
- ✅ Single codebase
- ✅ DRY (Don't Repeat Yourself)
- ✅ Easy to add new environments

**Drawbacks:**
- ⚠️ Easy to accidentally operate on wrong workspace
- ⚠️ Shared backend = potential for errors
- ⚠️ Workspace name must be passed around

### Strategy 3: Layered Architecture

**Structure:**
```
infrastructure/
├── 1-networking/
│   └── backend.tf  # key: networking/terraform.tfstate
├── 2-security/
│   └── backend.tf  # key: security/terraform.tfstate
├── 3-data/
│   └── backend.tf  # key: data/terraform.tfstate
└── 4-compute/
    └── backend.tf  # key: compute/terraform.tfstate
```

**Cross-Layer References:**
```hcl
# 4-compute/main.tf
data "terraform_remote_state" "networking" {
  backend = "s3"
  config = {
    bucket = "company-terraform-state"
    key    = "networking/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_instance" "app" {
  subnet_id = data.terraform_remote_state.networking.outputs.private_subnet_ids[0]
  # ...
}
```

**Benefits:**
- ✅ Blast radius reduction
- ✅ Independent layer updates
- ✅ Clear dependencies

**Drawbacks:**
- ⚠️ More complex cross-layer references
- ⚠️ Must apply layers in order

---

## Sensitive Data in State

### Handling Secrets in Terraform

**Problem:** Terraform state contains sensitive data in plaintext.

**Solution 1: Encrypt State at Rest**
```hcl
# Always use KMS encryption for S3 backend
terraform {
  backend "s3" {
    bucket     = "company-terraform-state"
    key        = "prod/db/terraform.tfstate"
    region     = "us-east-1"
    encrypt    = true  # AES-256 encryption
    kms_key_id = "arn:aws:kms:us-east-1:123456789012:key/abc123"  # KMS encryption
  }
}
```

**Solution 2: Mark Outputs as Sensitive**
```hcl
resource "random_password" "db" {
  length  = 32
  special = true
}

resource "aws_db_instance" "main" {
  password = random_password.db.result
  # ...
}

# Prevent password from appearing in logs
output "db_password" {
  value     = random_password.db.result
  sensitive = true  # Hidden in terraform output
}
```

**Solution 3: Use Secret References Instead of Values**
```hcl
# BAD: Password stored in state
resource "aws_db_instance" "main" {
  password = "hardcoded-password"  # ❌ Stored in state
}

# GOOD: Reference secret from secret manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/db/master-password"
}

resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string  # ✅ Not stored
}
```

### Handling Secrets in Pulumi

Pulumi encrypts secrets in state automatically:

```typescript
const config = new pulumi.Config();
const dbPassword = config.requireSecret("dbPassword");  // Encrypted in state

const db = new aws.rds.Instance("database", {
  password: dbPassword,  // Stored encrypted
});

export const password = pulumi.secret(dbPassword);  // Exported as secret
```

---

## State Operations

### Terraform State Commands

```bash
# List resources in state
terraform state list

# Show resource details
terraform state show aws_vpc.main

# Move resource (rename)
terraform state mv aws_instance.old aws_instance.new

# Remove resource from state (doesn't destroy)
terraform state rm aws_instance.abandoned

# Replace resource (taint)
terraform apply -replace=aws_instance.app

# Import existing resource
terraform import aws_vpc.main vpc-12345678

# Pull state to local file
terraform state pull > terraform.tfstate.backup

# Push local state to remote
terraform state push terraform.tfstate
```

### Pulumi State Commands

```bash
# List resources in stack
pulumi stack --show-urns

# Export state to file
pulumi stack export > state.json

# Import state from file
pulumi stack import < state.json

# Refresh state
pulumi refresh

# Remove resource from state
pulumi state delete 'urn:pulumi:...'

# Import existing resource
pulumi import aws:ec2/vpc:Vpc main vpc-12345678
```

---

## State Recovery

### Terraform State Recovery

**Scenario 1: Corrupted State**

```bash
# Restore from S3 versioning
aws s3api list-object-versions \
  --bucket company-terraform-state \
  --prefix prod/vpc/terraform.tfstate

# Download previous version
aws s3api get-object \
  --bucket company-terraform-state \
  --key prod/vpc/terraform.tfstate \
  --version-id <version-id> \
  terraform.tfstate.restored

# Restore
terraform state push terraform.tfstate.restored
```

**Scenario 2: Lost State**

```bash
# Rebuild state by importing all resources
terraform import aws_vpc.main vpc-12345678
terraform import aws_subnet.private[0] subnet-abc123
# ... import all resources
```

### Pulumi State Recovery

```bash
# Restore from checkpoint history
pulumi stack export --version <timestamp> > state.json
pulumi stack import < state.json
```

---

## Migration Patterns

### Local to Remote State (Terraform)

```bash
# Step 1: Add backend configuration
# (Create backend.tf with S3 configuration)

# Step 2: Initialize with migration
terraform init -migrate-state

# Step 3: Verify
terraform plan  # Should show no changes
```

### Workspace to Directory Migration (Terraform)

```bash
# For each workspace:
terraform workspace select prod
terraform state pull > prod-state.tfstate

# Create new directory structure
mkdir -p environments/prod
mv prod-state.tfstate environments/prod/terraform.tfstate

# Update backend config and re-init
cd environments/prod
terraform init
terraform plan  # Verify no changes
```

### Terraform to Pulumi Migration

```bash
# Convert HCL to Pulumi
pulumi convert --from terraform --language typescript --out ./pulumi

# Import state
cd pulumi
pulumi stack init prod
pulumi import <resources>
```

---

## Best Practices

**State Security:**
- ✅ Always use remote state for teams
- ✅ Enable encryption at rest (KMS)
- ✅ Enable versioning for rollback
- ✅ Restrict access with IAM policies
- ✅ Never commit state files to Git
- ✅ Use separate state files per environment

**State Organization:**
- ✅ Use directory separation for true isolation
- ✅ Layer state files by infrastructure concern
- ✅ Keep state files small and focused
- ✅ Document state structure

**State Operations:**
- ✅ Always back up state before operations
- ✅ Use state locking to prevent corruption
- ✅ Test state migrations in non-prod first
- ✅ Monitor state file access logs

**Secrets Management:**
- ✅ Mark sensitive outputs as sensitive
- ✅ Use secret references, not values
- ✅ Encrypt state at rest
- ✅ Rotate secrets regularly
- ✅ Audit secret access

---

See SKILL.md for links to drift detection and testing strategies.
