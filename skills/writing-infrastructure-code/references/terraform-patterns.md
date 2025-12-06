# Terraform Patterns and Best Practices

Comprehensive guide to Terraform/OpenTofu patterns, HCL best practices, and production-ready infrastructure code.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Variable Management](#variable-management)
3. [Provider Configuration](#provider-configuration)
4. [Resource Patterns](#resource-patterns)
5. [Data Sources](#data-sources)
6. [Outputs](#outputs)
7. [Locals](#locals)
8. [Dynamic Blocks](#dynamic-blocks)
9. [Count vs For_Each](#count-vs-for_each)
10. [Conditional Resources](#conditional-resources)
11. [Backend Configuration](#backend-configuration)
12. [Workspace Patterns](#workspace-patterns)
13. [Dependency Management](#dependency-management)
14. [Error Handling](#error-handling)

---

## Project Structure

### Recommended Directory Layout

**Monolithic Structure (Small Projects):**
```
terraform/
├── main.tf           # Primary resources
├── variables.tf      # Input variables
├── outputs.tf        # Outputs
├── versions.tf       # Terraform and provider versions
├── backend.tf        # Backend configuration
├── terraform.tfvars  # Default values (not committed)
├── prod.tfvars       # Production values
├── staging.tfvars    # Staging values
└── dev.tfvars        # Development values
```

**Modular Structure (Medium/Large Projects):**
```
infrastructure/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── security-group/
│   ├── rds/
│   └── ecs-service/
├── environments/
│   ├── prod/
│   │   ├── main.tf
│   │   ├── backend.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── dev/
└── global/
    └── state-backend/  # Bootstrap S3 + DynamoDB
```

**Layered Structure (Enterprise):**
```
infrastructure/
├── 1-bootstrap/        # State backend, IAM
├── 2-networking/       # VPCs, subnets, routing
├── 3-security/         # Security groups, NACLs, WAF
├── 4-data/             # Databases, caches, queues
├── 5-compute/          # ECS, Lambda, EC2
└── 6-applications/     # Application-specific resources
```

---

## Variable Management

### Variable Definitions

**variables.tf:**
```hcl
# Required variable with validation
variable "environment" {
  type        = string
  description = "Environment name (prod, staging, dev)"

  validation {
    condition     = contains(["prod", "staging", "dev"], var.environment)
    error_message = "Environment must be prod, staging, or dev."
  }
}

# Optional with default
variable "vpc_cidr" {
  type        = string
  description = "VPC CIDR block"
  default     = "10.0.0.0/16"
}

# Complex types
variable "subnet_config" {
  type = map(object({
    cidr = string
    az   = string
    type = string
  }))
  description = "Subnet configuration map"
  default = {
    private_a = {
      cidr = "10.0.1.0/24"
      az   = "us-east-1a"
      type = "private"
    }
  }
}

# Sensitive variable
variable "database_password" {
  type        = string
  description = "RDS master password"
  sensitive   = true
}

# List variable
variable "availability_zones" {
  type        = list(string)
  description = "List of availability zones"
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}
```

### Variable Precedence

Order of precedence (highest to lowest):
1. `-var` or `-var-file` command line flags
2. `*.auto.tfvars` files (alphabetical order)
3. `terraform.tfvars` file
4. Environment variables (`TF_VAR_name`)
5. Default values in variable definitions

### Variable Best Practices

```hcl
# ✅ Good: Descriptive name, validation, documentation
variable "rds_instance_class" {
  type        = string
  description = "RDS instance class (e.g., db.t3.medium)"

  validation {
    condition     = can(regex("^db\\.", var.rds_instance_class))
    error_message = "Instance class must start with 'db.'"
  }
}

# ❌ Bad: Vague name, no validation, no description
variable "size" {
  type = string
}

# ✅ Good: Complex type with clear structure
variable "tags" {
  type        = map(string)
  description = "Resource tags"
  default = {
    ManagedBy = "terraform"
  }
}

# ✅ Good: Nullable for optional resources
variable "enable_monitoring" {
  type        = bool
  description = "Enable CloudWatch monitoring"
  default     = true
  nullable    = false  # Prevent null values
}
```

---

## Provider Configuration

### Provider Versioning

**versions.tf:**
```hcl
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # Allow minor updates, not major
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "terraform"
      Project     = var.project_name
    }
  }
}

# Additional provider for cross-region resources
provider "aws" {
  alias  = "us_west_2"
  region = "us-west-2"
}
```

### Provider Aliases for Multi-Region

```hcl
# Create resources in multiple regions
resource "aws_s3_bucket" "primary" {
  provider = aws.us_east_1
  bucket   = "primary-bucket"
}

resource "aws_s3_bucket" "replica" {
  provider = aws.us_west_2
  bucket   = "replica-bucket"
}
```

---

## Resource Patterns

### Resource Naming Convention

```hcl
# Pattern: <resource_type>.<logical_name>
# Use descriptive names that indicate purpose

# ✅ Good
resource "aws_vpc" "main" {}
resource "aws_subnet" "private" {}
resource "aws_security_group" "web" {}

# ❌ Bad
resource "aws_vpc" "vpc1" {}
resource "aws_subnet" "subnet" {}
resource "aws_security_group" "sg" {}
```

### Resource Dependencies

```hcl
# Implicit dependency (recommended)
resource "aws_subnet" "private" {
  vpc_id = aws_vpc.main.id  # Terraform infers dependency
}

# Explicit dependency (use sparingly)
resource "aws_instance" "app" {
  ami           = data.aws_ami.latest.id
  instance_type = "t3.micro"

  depends_on = [
    aws_iam_role_policy_attachment.app_policy
  ]
}
```

### Lifecycle Rules

```hcl
resource "aws_s3_bucket" "state" {
  bucket = "terraform-state-bucket"

  lifecycle {
    # Prevent accidental deletion
    prevent_destroy = true

    # Create new resource before destroying old
    create_before_destroy = true

    # Ignore changes to specific attributes
    ignore_changes = [
      tags["LastModified"],
    ]
  }
}
```

### Provisioners (Use Sparingly)

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.latest.id
  instance_type = "t3.micro"

  # Local provisioner (runs on Terraform machine)
  provisioner "local-exec" {
    command = "echo ${self.private_ip} >> private_ips.txt"
  }

  # Remote provisioner (use configuration management instead)
  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx"
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
    command = "echo 'Instance destroyed' >> cleanup.log"
  }
}
```

---

## Data Sources

### Common Data Source Patterns

```hcl
# Fetch latest AMI
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Fetch availability zones
data "aws_availability_zones" "available" {
  state = "available"
}

# Fetch current caller identity
data "aws_caller_identity" "current" {}

# Fetch existing VPC by tag
data "aws_vpc" "selected" {
  tags = {
    Name = "production-vpc"
  }
}

# Fetch remote state from another workspace
data "terraform_remote_state" "networking" {
  backend = "s3"
  config = {
    bucket = "company-terraform-state"
    key    = "networking/terraform.tfstate"
    region = "us-east-1"
  }
}
```

---

## Outputs

### Output Best Practices

```hcl
# Simple output
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

# Sensitive output (hidden in logs)
output "database_password" {
  description = "RDS master password"
  value       = aws_db_instance.main.password
  sensitive   = true
}

# Complex output
output "subnet_info" {
  description = "Subnet IDs and CIDR blocks"
  value = {
    private_subnet_ids   = aws_subnet.private[*].id
    private_subnet_cidrs = aws_subnet.private[*].cidr_block
    public_subnet_ids    = aws_subnet.public[*].id
    public_subnet_cidrs  = aws_subnet.public[*].cidr_block
  }
}

# Conditional output
output "alb_dns" {
  description = "ALB DNS name (if created)"
  value       = try(aws_lb.main[0].dns_name, null)
}
```

---

## Locals

### Local Value Patterns

```hcl
locals {
  # Computed values
  common_tags = {
    Environment = var.environment
    ManagedBy   = "terraform"
    Project     = var.project_name
    CostCenter  = var.cost_center
  }

  # Conditional logic
  instance_type = var.environment == "prod" ? "t3.large" : "t3.micro"

  # List transformations
  availability_zones = slice(data.aws_availability_zones.available.names, 0, 3)

  # Map transformations
  subnet_cidrs = {
    for idx, az in local.availability_zones :
    az => cidrsubnet(var.vpc_cidr, 4, idx)
  }

  # Derived names
  resource_prefix = "${var.project_name}-${var.environment}"
  vpc_name        = "${local.resource_prefix}-vpc"
  cluster_name    = "${local.resource_prefix}-ecs"
}
```

---

## Dynamic Blocks

### Dynamic Block Patterns

```hcl
# Dynamic ingress rules
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Web server security group"
  vpc_id      = aws_vpc.main.id

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

# Variable definition
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
      description = "HTTP"
    },
    {
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "HTTPS"
    }
  ]
}
```

---

## Count vs For_Each

### When to Use Count

```hcl
# Count: Simple numeric iteration
resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "private-subnet-${count.index}"
  }
}

# Reference: aws_subnet.private[0].id
```

### When to Use For_Each

```hcl
# For_each: Key-based iteration (preferred)
variable "subnets" {
  type = map(object({
    cidr = string
    az   = string
  }))
  default = {
    private_a = { cidr = "10.0.1.0/24", az = "us-east-1a" }
    private_b = { cidr = "10.0.2.0/24", az = "us-east-1b" }
    private_c = { cidr = "10.0.3.0/24", az = "us-east-1c" }
  }
}

resource "aws_subnet" "private" {
  for_each          = var.subnets
  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value.cidr
  availability_zone = each.value.az

  tags = {
    Name = "private-subnet-${each.key}"
  }
}

# Reference: aws_subnet.private["private_a"].id
```

**Recommendation:** Use `for_each` over `count` for most cases - adding/removing items won't affect other resources.

---

## Conditional Resources

```hcl
# Create resource conditionally
resource "aws_instance" "bastion" {
  count = var.enable_bastion ? 1 : 0

  ami           = data.aws_ami.latest.id
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public[0].id
}

# Reference conditional resource
output "bastion_ip" {
  value = var.enable_bastion ? aws_instance.bastion[0].public_ip : null
}

# Conditional attribute
resource "aws_db_instance" "main" {
  allocated_storage = var.environment == "prod" ? 100 : 20
  instance_class    = var.environment == "prod" ? "db.m5.large" : "db.t3.micro"
}
```

---

## Backend Configuration

### S3 Backend with DynamoDB Locking

**backend.tf:**
```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "prod/vpc/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    kms_key_id     = "arn:aws:kms:us-east-1:123456789012:key/abc123"
    dynamodb_table = "terraform-locks"

    # Optional: State file versioning rollback
    # Enable versioning on S3 bucket separately
  }
}
```

### Partial Backend Configuration

**backend.tf (static):**
```hcl
terraform {
  backend "s3" {}
}
```

**backend-prod.tfbackend (dynamic):**
```hcl
bucket         = "company-terraform-state"
key            = "prod/vpc/terraform.tfstate"
region         = "us-east-1"
encrypt        = true
dynamodb_table = "terraform-locks"
```

**Usage:**
```bash
terraform init -backend-config=backend-prod.tfbackend
```

---

## Workspace Patterns

```bash
# Create workspace
terraform workspace new staging

# List workspaces
terraform workspace list

# Select workspace
terraform workspace select prod

# Show current workspace
terraform workspace show
```

**Use workspace in code:**
```hcl
resource "aws_instance" "app" {
  instance_type = terraform.workspace == "prod" ? "t3.large" : "t3.micro"

  tags = {
    Name        = "app-${terraform.workspace}"
    Environment = terraform.workspace
  }
}
```

**Warning:** Workspaces share the same state backend. Use directory separation for true isolation.

---

## Dependency Management

### Explicit Dependencies

```hcl
# Use depends_on when implicit dependencies aren't sufficient
resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "app" {
  # Implicit: role = aws_iam_role.lambda.arn creates dependency
  role = aws_iam_role.lambda.arn

  # Explicit: Ensure policy is attached before creating function
  depends_on = [aws_iam_role_policy_attachment.lambda_policy]
}
```

### Module Dependencies

```hcl
module "vpc" {
  source = "./modules/vpc"
}

module "ecs_cluster" {
  source = "./modules/ecs-cluster"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids

  # Implicit dependency via output references
}
```

---

## Error Handling

### Validation Functions

```hcl
variable "cidr_block" {
  type = string

  validation {
    condition     = can(cidrhost(var.cidr_block, 0))
    error_message = "Must be a valid IPv4 CIDR block."
  }
}

variable "environment" {
  type = string

  validation {
    condition     = contains(["prod", "staging", "dev"], var.environment)
    error_message = "Environment must be prod, staging, or dev."
  }
}
```

### Try/Can Functions

```hcl
# Try with fallback
locals {
  # Returns first successful expression
  vpc_id = try(aws_vpc.main[0].id, data.aws_vpc.existing.id)
}

# Can for validation
variable "json_config" {
  type = string

  validation {
    condition     = can(jsondecode(var.json_config))
    error_message = "Must be valid JSON."
  }
}

# Coalescelist for first non-empty list
locals {
  subnet_ids = coalescelist(
    aws_subnet.private[*].id,
    data.aws_subnet.existing[*].id
  )
}
```

### Preconditions and Postconditions

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.latest.id
  instance_type = var.instance_type

  lifecycle {
    precondition {
      condition     = data.aws_ami.latest.architecture == "x86_64"
      error_message = "AMI must be x86_64 architecture."
    }

    postcondition {
      condition     = self.public_ip != ""
      error_message = "Instance must have a public IP address."
    }
  }
}
```

---

## Advanced Patterns

### Remote State Data Source

```hcl
# Reference outputs from another Terraform workspace
data "terraform_remote_state" "networking" {
  backend = "s3"
  config = {
    bucket = "company-terraform-state"
    key    = "networking/terraform.tfstate"
    region = "us-east-1"
  }
}

# Use outputs
resource "aws_instance" "app" {
  subnet_id = data.terraform_remote_state.networking.outputs.private_subnet_ids[0]
}
```

### Terraform Data Source (Self-Reference)

```hcl
data "terraform_remote_state" "self" {
  backend = "local"
  config = {
    path = "${path.module}/terraform.tfstate"
  }
}
```

### Import Existing Resources

```bash
# Import existing AWS resource
terraform import aws_vpc.main vpc-12345678

# Import module resource
terraform import 'module.vpc.aws_vpc.main' vpc-12345678
```

---

## Testing Terraform Code

### Validation Commands

```bash
# Format code
terraform fmt -recursive

# Validate syntax
terraform validate

# Plan with detailed output
terraform plan -out=tfplan

# Show plan in JSON
terraform show -json tfplan | jq

# Lint with tflint
tflint --init
tflint
```

### Terratest Example

See `examples/terraform/testing/` for Terratest examples.

---

## Performance Optimization

### Parallelism

```bash
# Increase parallelism (default: 10)
terraform apply -parallelism=20
```

### Target Specific Resources

```bash
# Plan/apply specific resource
terraform plan -target=aws_instance.web
terraform apply -target=module.vpc
```

### Refresh vs No-Refresh

```bash
# Skip refresh for faster plans
terraform plan -refresh=false

# Refresh state only (no changes)
terraform apply -refresh-only
```

---

## Best Practices Summary

**Code Organization:**
- ✅ Separate environments by directory
- ✅ Use modules for reusable components
- ✅ Pin provider and module versions
- ✅ Keep state files small and focused

**Variable Management:**
- ✅ Add validation rules for critical variables
- ✅ Provide descriptions for all variables
- ✅ Use sensitive = true for secrets
- ✅ Document variable precedence

**Resource Design:**
- ✅ Use for_each over count
- ✅ Add lifecycle rules where appropriate
- ✅ Use descriptive resource names
- ✅ Implement default_tags at provider level

**State Management:**
- ✅ Use remote state with locking
- ✅ Enable encryption and versioning
- ✅ Separate state by layer/environment
- ✅ Never commit state files to Git

**Operations:**
- ✅ Run terraform fmt before commits
- ✅ Run terraform validate in CI
- ✅ Review terraform plan before apply
- ✅ Use terraform import for existing resources

---

See SKILL.md for links to other IaC topics including Pulumi patterns, state management, and module design.
