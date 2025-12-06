# OpenTofu Reference Guide

Comprehensive guide to OpenTofu, the open-source Terraform alternative under CNCF governance.

## Table of Contents

1. [Overview](#overview)
2. [OpenTofu vs Terraform](#opentofu-vs-terraform)
3. [Installation and Setup](#installation-and-setup)
4. [Migration from Terraform](#migration-from-terraform)
5. [State Management](#state-management)
6. [Module Development](#module-development)
7. [Provider Configuration](#provider-configuration)
8. [Best Practices](#best-practices)
9. [Advanced Patterns](#advanced-patterns)
10. [Troubleshooting](#troubleshooting)

## Overview

OpenTofu is a CNCF project providing open-source Infrastructure as Code (IaC) with Terraform compatibility. Forked from Terraform 1.5.x, OpenTofu maintains HashiCorp Configuration Language (HCL) syntax while ensuring open governance under the Mozilla Public License 2.0.

**Key Characteristics**:
- **CNCF Project**: Linux Foundation governance
- **MPL-2.0 License**: Open-source with community control
- **Terraform Compatible**: Drop-in replacement for Terraform 1.5.x and earlier
- **Active Development**: Regular releases with community contributions
- **Provider Support**: Uses same provider ecosystem as Terraform

**When to Use OpenTofu**:
- Require open-source governance guarantees
- Migrating from Terraform to avoid license concerns
- Prefer HCL syntax over TypeScript (otherwise use Pulumi)
- Need Terraform compatibility with open governance

**When to Use Alternatives**:
- **Pulumi**: Prefer TypeScript/Python/Go over HCL
- **SST**: Building AWS serverless applications
- **Terraform**: Require HashiCorp enterprise support

## OpenTofu vs Terraform

### Key Differences

| Feature | OpenTofu | Terraform |
|---------|----------|-----------|
| **License** | MPL-2.0 (open-source) | BSL 1.1 (source-available) |
| **Governance** | CNCF (community) | HashiCorp (corporate) |
| **Compatibility** | Terraform 1.5.x baseline | Latest HashiCorp features |
| **State Encryption** | Built-in (native) | Enterprise only |
| **Community** | Open contribution model | HashiCorp-controlled |
| **Commercial Support** | Third-party vendors | HashiCorp only |

### Feature Parity

**Identical Features**:
- HCL syntax and language features
- Provider ecosystem (same registry)
- State file format (compatible)
- Module structure and composition
- Workspaces and remote backends

**OpenTofu Enhancements**:
- Native state encryption (client-side)
- Enhanced testing framework (planned)
- Community-driven feature roadmap
- No vendor lock-in

**Terraform Exclusive**:
- Terraform Cloud integration (use Spacelift, env0, Scalr instead)
- HashiCorp enterprise support
- Latest HashiCorp-proprietary features

### Version Compatibility

```hcl
# Specify OpenTofu version in configuration
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

**Migration Path**:
- Terraform 1.5.x or earlier → Direct migration (100% compatible)
- Terraform 1.6.x+ → Review compatibility, test thoroughly
- State file format is compatible in both directions

## Installation and Setup

### Install OpenTofu

**macOS (Homebrew)**:
```bash
brew install opentofu
```

**Linux (Package Manager)**:
```bash
# Debian/Ubuntu
curl -L https://get.opentofu.org/install-opentofu.sh | bash

# Fedora/RHEL
dnf install opentofu
```

**Windows (Chocolatey)**:
```powershell
choco install opentofu
```

**Verify Installation**:
```bash
tofu version
# OpenTofu v1.6.0
```

### CLI Usage

OpenTofu uses `tofu` command (not `terraform`):

```bash
tofu init        # Initialize working directory
tofu plan        # Preview changes
tofu apply       # Apply changes
tofu destroy     # Destroy infrastructure
tofu validate    # Validate configuration
tofu fmt         # Format configuration files
```

### Alias for Compatibility

Create alias for seamless Terraform-to-OpenTofu transition:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias terraform='tofu'
```

This allows using `terraform` commands while running OpenTofu.

## Migration from Terraform

### Pre-Migration Checklist

Before migrating from Terraform to OpenTofu:

1. **Backup state files**:
   ```bash
   terraform state pull > terraform.tfstate.backup
   ```

2. **Verify Terraform version**:
   ```bash
   terraform version
   # Terraform v1.5.7 or earlier recommended
   ```

3. **Check provider compatibility**:
   ```bash
   # List providers in use
   terraform providers
   ```

4. **Document custom modules and configurations**

5. **Test in non-production environment first**

### Migration Steps

#### Step 1: Install OpenTofu

Install OpenTofu alongside Terraform (no need to uninstall Terraform):

```bash
brew install opentofu
```

#### Step 2: Initialize with State Migration

Navigate to Terraform project directory:

```bash
cd /path/to/terraform/project

# Initialize OpenTofu and migrate state
tofu init -migrate-state
```

Response when prompted:
```
Do you want to copy existing state to the new backend?
  Enter a value: yes
```

#### Step 3: Verify State Migration

```bash
# Verify state is accessible
tofu state list

# Compare with Terraform state
terraform state list
```

Both should show identical resources.

#### Step 4: Plan and Verify

```bash
# Generate plan
tofu plan

# Should show "No changes" if migration successful
```

#### Step 5: Apply Changes

```bash
# Apply with OpenTofu
tofu apply
```

### Handling Migration Issues

**Issue: Provider version mismatch**

```bash
# Update provider versions in configuration
tofu init -upgrade
```

**Issue: State lock errors**

```bash
# Force unlock (use with caution)
tofu force-unlock <lock-id>
```

**Issue: Backend configuration differences**

```hcl
# Update backend configuration if needed
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Gradual Migration Strategy

For large infrastructures, migrate incrementally:

1. **Pilot Project**: Start with small, non-critical project
2. **Parallel Testing**: Run both Terraform and OpenTofu side-by-side
3. **Environment-by-Environment**: Migrate dev → staging → production
4. **Service-by-Service**: Migrate one service at a time
5. **Monitoring**: Track state consistency and drift

## State Management

### State File Basics

OpenTofu state tracks infrastructure resources and metadata.

**Local State**:
```bash
# State stored in terraform.tfstate (local file)
tofu init
tofu apply
```

**Remote State** (Recommended for teams):
```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "services/api/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-locks"
  }
}
```

### State Encryption

OpenTofu provides native state encryption (Terraform Enterprise only feature):

```hcl
terraform {
  encryption {
    key_provider "pbkdf2" "mykey" {
      passphrase = var.state_encryption_passphrase
    }

    method "aes_gcm" "state_encryption" {
      keys = key_provider.pbkdf2.mykey
    }

    state {
      method = method.aes_gcm.state_encryption
    }
  }
}
```

**Environment Variable Alternative**:
```bash
export TF_ENCRYPTION_PASSPHRASE="your-secure-passphrase"
tofu apply
```

### State Operations

**View State**:
```bash
# List all resources
tofu state list

# Show specific resource
tofu state show aws_instance.web
```

**Move Resources**:
```bash
# Rename resource in state
tofu state mv aws_instance.old aws_instance.new
```

**Remove Resources**:
```bash
# Remove from state (doesn't destroy)
tofu state rm aws_instance.deprecated
```

**Import Existing Resources**:
```bash
# Import existing AWS EC2 instance
tofu import aws_instance.web i-1234567890abcdef0
```

### Remote State Backends

**AWS S3 + DynamoDB**:
```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-state-prod"
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"

    # Enable versioning for state history
    versioning     = true
  }
}
```

**Google Cloud Storage**:
```hcl
terraform {
  backend "gcs" {
    bucket = "terraform-state-prod"
    prefix = "global/gcs"
  }
}
```

**Azure Blob Storage**:
```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "terraformstateprod"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

**Terraform Cloud Alternative (Spacelift)**:
```hcl
terraform {
  backend "http" {
    address = "https://spacelift.io/api/v1/state"
    lock_address = "https://spacelift.io/api/v1/state/lock"
    unlock_address = "https://spacelift.io/api/v1/state/unlock"
  }
}
```

### State Locking

Prevents concurrent modifications:

```hcl
# DynamoDB for S3 backend locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name = "Terraform State Locks"
  }
}
```

**Force Unlock** (emergency only):
```bash
tofu force-unlock <lock-id>
```

## Module Development

### Module Structure

Standard module layout:

```
terraform-module-name/
├── main.tf           # Primary resource definitions
├── variables.tf      # Input variable declarations
├── outputs.tf        # Output value declarations
├── versions.tf       # Provider version constraints
├── README.md         # Module documentation
├── examples/         # Usage examples
│   └── basic/
│       ├── main.tf
│       └── variables.tf
└── tests/            # Module tests
    └── basic_test.go
```

### Creating a Module

**main.tf**:
```hcl
# VPC Module Example
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = var.enable_dns_hostnames
  enable_dns_support   = var.enable_dns_support

  tags = merge(
    var.tags,
    {
      Name = var.vpc_name
    }
  )
}

resource "aws_subnet" "public" {
  count = length(var.public_subnet_cidrs)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = merge(
    var.tags,
    {
      Name = "${var.vpc_name}-public-${count.index + 1}"
      Type = "public"
    }
  )
}
```

**variables.tf**:
```hcl
variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "VPC CIDR must be valid IPv4 CIDR block."
  }
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "availability_zones" {
  description = "Availability zones for subnets"
  type        = list(string)
}

variable "enable_dns_hostnames" {
  description = "Enable DNS hostnames in VPC"
  type        = bool
  default     = true
}

variable "enable_dns_support" {
  description = "Enable DNS support in VPC"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
```

**outputs.tf**:
```hcl
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "availability_zones" {
  description = "Availability zones used"
  value       = aws_subnet.public[*].availability_zone
}
```

**versions.tf**:
```hcl
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

### Using Modules

**Local Module**:
```hcl
module "vpc" {
  source = "./modules/vpc"

  vpc_name           = "production-vpc"
  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

  tags = {
    Environment = "production"
    Team        = "platform"
  }
}

# Reference module outputs
resource "aws_instance" "web" {
  subnet_id = module.vpc.public_subnet_ids[0]
  # ...
}
```

**Remote Module (Git)**:
```hcl
module "vpc" {
  source = "git::https://github.com/company/terraform-modules.git//vpc?ref=v1.2.0"

  vpc_name = "staging-vpc"
  vpc_cidr = "10.1.0.0/16"
}
```

**OpenTofu Registry**:
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"

  name = "production-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = false
}
```

### Module Composition

**Root Module** (composes multiple modules):
```hcl
# main.tf
module "vpc" {
  source = "./modules/vpc"

  vpc_name = "production"
  vpc_cidr = "10.0.0.0/16"
}

module "security_groups" {
  source = "./modules/security-groups"

  vpc_id = module.vpc.vpc_id
}

module "ecs_cluster" {
  source = "./modules/ecs"

  cluster_name       = "production-cluster"
  vpc_id             = module.vpc.vpc_id
  subnet_ids         = module.vpc.private_subnet_ids
  security_group_ids = [module.security_groups.ecs_sg_id]
}
```

### Module Testing

**Terratest Example** (Go):
```go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestVPCModule(t *testing.T) {
    terraformOptions := &terraform.Options{
        TerraformDir: "../examples/basic",
        Vars: map[string]interface{}{
            "vpc_name": "test-vpc",
            "vpc_cidr": "10.0.0.0/16",
        },
    }

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    vpcID := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcID)
}
```

## Provider Configuration

### AWS Provider

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      ManagedBy   = "OpenTofu"
      Environment = var.environment
    }
  }
}

# Multiple regions
provider "aws" {
  alias  = "us_west"
  region = "us-west-2"
}

resource "aws_s3_bucket" "west_coast" {
  provider = aws.us_west
  bucket   = "my-west-coast-bucket"
}
```

### Google Cloud Provider

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
  zone    = var.gcp_zone
}

resource "google_compute_instance" "vm" {
  name         = "web-server"
  machine_type = "n2-standard-2"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }
}
```

### Azure Provider

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = true
    }
  }

  subscription_id = var.azure_subscription_id
}

resource "azurerm_resource_group" "main" {
  name     = "production-resources"
  location = "East US"
}
```

### Cloudflare Provider

```hcl
terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

resource "cloudflare_zone" "example" {
  zone = "example.com"
  plan = "free"
}

resource "cloudflare_record" "www" {
  zone_id = cloudflare_zone.example.id
  name    = "www"
  value   = "198.51.100.4"
  type    = "A"
  proxied = true
}
```

### Provider Authentication

**AWS (Environment Variables)**:
```bash
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_REGION="us-east-1"

tofu apply
```

**AWS (Assumed Role)**:
```hcl
provider "aws" {
  assume_role {
    role_arn     = "arn:aws:iam::123456789012:role/TerraformRole"
    session_name = "terraform-session"
  }
}
```

**Google Cloud (Service Account)**:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
tofu apply
```

**Azure (Service Principal)**:
```bash
export ARM_CLIENT_ID="00000000-0000-0000-0000-000000000000"
export ARM_CLIENT_SECRET="..."
export ARM_SUBSCRIPTION_ID="00000000-0000-0000-0000-000000000000"
export ARM_TENANT_ID="00000000-0000-0000-0000-000000000000"

tofu apply
```

## Best Practices

### Project Structure

**Recommended Layout**:
```
infrastructure/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   └── ...
│   └── prod/
│       └── ...
├── modules/
│   ├── vpc/
│   ├── ecs/
│   └── rds/
└── global/
    ├── iam/
    ├── route53/
    └── s3/
```

### Variable Management

**variables.tf** (declarations):
```hcl
variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}
```

**terraform.tfvars** (values):
```hcl
environment   = "production"
instance_type = "t3.large"
region        = "us-east-1"

tags = {
  Team        = "platform"
  CostCenter  = "engineering"
}
```

**Environment Variables**:
```bash
export TF_VAR_environment="production"
export TF_VAR_db_password="$(aws secretsmanager get-secret-value --secret-id prod/db/password --query SecretString --output text)"
```

### Security Best Practices

**1. Never Commit Secrets**:
```hcl
# Bad: Hardcoded secret
resource "aws_db_instance" "main" {
  password = "MyP@ssw0rd123"  # NEVER DO THIS
}

# Good: Use variables with sensitive flag
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

resource "aws_db_instance" "main" {
  password = var.db_password
}
```

**2. Use AWS Secrets Manager**:
```hcl
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "production/database/password"
}

resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

**3. Enable State Encryption**:
```hcl
terraform {
  backend "s3" {
    bucket  = "terraform-state"
    key     = "prod/terraform.tfstate"
    encrypt = true  # Server-side encryption
  }

  # Additional client-side encryption
  encryption {
    key_provider "pbkdf2" "main" {
      passphrase = var.encryption_passphrase
    }

    method "aes_gcm" "default" {
      keys = key_provider.pbkdf2.main
    }

    state {
      method = method.aes_gcm.default
    }
  }
}
```

**4. Use .gitignore**:
```gitignore
# .gitignore
*.tfstate
*.tfstate.*
.terraform/
.terraform.lock.hcl
*.tfvars
!example.tfvars
crash.log
override.tf
override.tf.json
```

### Resource Naming

**Consistent Naming Convention**:
```hcl
locals {
  name_prefix = "${var.project}-${var.environment}"

  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "OpenTofu"
    Timestamp   = timestamp()
  }
}

resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  tags = merge(
    local.common_tags,
    {
      Name = "${local.name_prefix}-vpc"
    }
  )
}

resource "aws_subnet" "public" {
  count = length(var.public_subnet_cidrs)

  vpc_id     = aws_vpc.main.id
  cidr_block = var.public_subnet_cidrs[count.index]

  tags = merge(
    local.common_tags,
    {
      Name = "${local.name_prefix}-public-subnet-${count.index + 1}"
      Type = "public"
    }
  )
}
```

### State Management Best Practices

**1. Use Remote State**:
```hcl
# Never use local state for production
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "prod/services/api/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

**2. Enable State Locking**:
```hcl
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

**3. Use Workspaces Cautiously**:
```bash
# Workspaces share same backend
tofu workspace new staging
tofu workspace select prod

# Prefer separate directories for environments
# environments/dev/, environments/staging/, environments/prod/
```

### Code Quality

**Use `tofu fmt`**:
```bash
# Format all .tf files
tofu fmt -recursive

# Check if files are formatted
tofu fmt -check
```

**Use `tofu validate`**:
```bash
# Validate configuration syntax
tofu validate
```

**Use Static Analysis** (tflint):
```bash
# Install tflint
brew install tflint

# Run linter
tflint --init
tflint
```

**Pre-commit Hooks**:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.83.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
```

## Advanced Patterns

### Dynamic Blocks

Generate repeated nested blocks:

```hcl
resource "aws_security_group" "web" {
  name   = "web-sg"
  vpc_id = aws_vpc.main.id

  dynamic "ingress" {
    for_each = var.ingress_rules

    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
      description = ingress.value.description
    }
  }
}

# variables.tf
variable "ingress_rules" {
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
    description = string
  }))

  default = [
    {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "Allow HTTP"
    },
    {
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "Allow HTTPS"
    }
  ]
}
```

### For Expressions

Transform collections:

```hcl
locals {
  # Create map from list
  subnet_map = {
    for idx, cidr in var.subnet_cidrs :
    "subnet-${idx}" => cidr
  }

  # Filter and transform
  public_subnets = [
    for subnet in aws_subnet.all :
    subnet.id if subnet.tags.Type == "public"
  ]

  # Uppercase all tags
  uppercase_tags = {
    for key, value in var.tags :
    key => upper(value)
  }
}
```

### Conditional Resources

Create resources conditionally:

```hcl
resource "aws_instance" "bastion" {
  count = var.enable_bastion ? 1 : 0

  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name = "bastion-host"
  }
}

# Alternative: use for_each with empty set
resource "aws_instance" "bastion_v2" {
  for_each = var.enable_bastion ? { bastion = true } : {}

  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
}
```

### Data Sources

Reference existing infrastructure:

```hcl
# Get VPC by tag
data "aws_vpc" "existing" {
  tags = {
    Name = "production-vpc"
  }
}

# Get latest AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Get availability zones
data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_subnet" "public" {
  count = 3

  vpc_id            = data.aws_vpc.existing.id
  cidr_block        = cidrsubnet(data.aws_vpc.existing.cidr_block, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
}
```

### Lifecycle Rules

Control resource behavior:

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  lifecycle {
    # Create new resource before destroying old
    create_before_destroy = true

    # Prevent accidental deletion
    prevent_destroy = true

    # Ignore changes to specific attributes
    ignore_changes = [
      ami,
      tags["LastModified"]
    ]
  }
}
```

### Provisioners

Execute scripts during resource creation:

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  # Local-exec: runs on machine running OpenTofu
  provisioner "local-exec" {
    command = "echo ${self.private_ip} >> private_ips.txt"
  }

  # Remote-exec: runs on the resource
  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx",
      "sudo systemctl start nginx"
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/id_rsa")
      host        = self.public_ip
    }
  }

  # Destroy-time provisioner
  provisioner "local-exec" {
    when    = destroy
    command = "echo 'Instance ${self.id} is being destroyed'"
  }
}
```

**Note**: Prefer configuration management tools (Ansible, cloud-init) over provisioners when possible.

## Troubleshooting

### Common Errors

**Error: State Lock**:
```
Error: Error locking state: Error acquiring the state lock
```

**Solution**:
```bash
# View lock info
tofu force-unlock <lock-id>

# Or wait for lock to expire (usually 15 minutes)
```

**Error: Provider Plugin**:
```
Error: Could not load plugin
```

**Solution**:
```bash
# Re-initialize and upgrade providers
tofu init -upgrade
```

**Error: State Divergence**:
```
Error: Your state is out of sync with the actual infrastructure
```

**Solution**:
```bash
# Refresh state
tofu refresh

# Or import missing resources
tofu import aws_instance.web i-1234567890abcdef0
```

**Error: Cycle Detected**:
```
Error: Cycle: aws_security_group.app, aws_security_group.db
```

**Solution**:
```hcl
# Use separate resources or data sources
# Break circular dependency by referencing IDs directly
resource "aws_security_group_rule" "app_to_db" {
  type                     = "egress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.db.id
  security_group_id        = aws_security_group.app.id
}
```

### Debugging

**Enable Debug Logging**:
```bash
export TF_LOG=DEBUG
export TF_LOG_PATH=./terraform.log

tofu apply
```

**Log Levels**:
- `TRACE`: Most verbose
- `DEBUG`: Detailed debugging info
- `INFO`: General informational messages
- `WARN`: Warning messages
- `ERROR`: Error messages only

**Graph Visualization**:
```bash
# Generate dependency graph
tofu graph | dot -Tpng > graph.png

# Requires graphviz: brew install graphviz
```

### State Recovery

**Restore from Backup**:
```bash
# S3 backend with versioning enabled
aws s3api list-object-versions --bucket terraform-state --prefix prod/terraform.tfstate

# Download specific version
aws s3api get-object --bucket terraform-state --key prod/terraform.tfstate --version-id <version-id> terraform.tfstate.restored

# Restore state
cp terraform.tfstate.restored terraform.tfstate
```

**Manual State Editing** (last resort):
```bash
# Pull state to local file
tofu state pull > terraform.tfstate.backup

# Edit terraform.tfstate.backup manually
# Push state back
tofu state push terraform.tfstate.backup
```

### Performance Optimization

**Reduce Plan Time**:
```bash
# Target specific resources
tofu plan -target=aws_instance.web

# Parallelize operations (default: 10)
tofu apply -parallelism=20
```

**State File Size**:
```bash
# Check state size
ls -lh terraform.tfstate

# Split large states into separate workspaces or backends
```

### Drift Detection

**Detect Configuration Drift**:
```bash
# Show differences between state and actual infrastructure
tofu plan -detailed-exitcode

# Exit codes:
# 0 = no changes
# 1 = error
# 2 = changes detected
```

**Continuous Drift Detection** (CI/CD):
```yaml
# .github/workflows/drift-detection.yml
name: Terraform Drift Detection
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  detect-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: opentofu/setup-opentofu@v1

      - name: Detect drift
        run: |
          tofu init
          tofu plan -detailed-exitcode
```

## Additional Resources

**Official Documentation**:
- OpenTofu Website: https://opentofu.org/
- OpenTofu Docs: https://opentofu.org/docs/
- OpenTofu GitHub: https://github.com/opentofu/opentofu

**Migration Guides**:
- Terraform to OpenTofu: https://opentofu.org/docs/intro/migration/
- State Encryption: https://opentofu.org/docs/language/state/encryption/

**Community Resources**:
- OpenTofu Registry: https://registry.opentofu.org/
- OpenTofu Slack: https://opentofu.org/slack
- CNCF OpenTofu: https://www.cncf.io/projects/opentofu/

**Alternative Tools**:
- Pulumi (TypeScript IaC): https://www.pulumi.com/
- SST (Serverless TypeScript): https://sst.dev/
- Spacelift (OpenTofu Platform): https://spacelift.io/
