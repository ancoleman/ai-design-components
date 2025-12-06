# Module Design - Composable, Reusable Infrastructure

Comprehensive guide to designing, versioning, and testing infrastructure modules.

## Table of Contents

1. [Module Fundamentals](#module-fundamentals)
2. [Module Structure](#module-structure)
3. [Input Design](#input-design)
4. [Output Design](#output-design)
5. [Module Composition](#module-composition)
6. [Versioning Strategy](#versioning-strategy)
7. [Module Registries](#module-registries)
8. [Testing Modules](#testing-modules)
9. [Documentation](#documentation)

---

## Module Fundamentals

### What is a Module?

A module is a reusable package of infrastructure code that encapsulates related resources with a clear interface.

**Benefits:**
- ✅ DRY (Don't Repeat Yourself)
- ✅ Consistency across environments
- ✅ Testable in isolation
- ✅ Versioned and governed
- ✅ Composable into larger systems

### When to Create a Module

**Create a Module When:**
- Resource group is reused 3+ times
- Clear input/output boundaries exist
- Complexity benefits from abstraction
- Team has capacity to maintain

**Keep Monolithic When:**
- One-off infrastructure
- Rapid prototyping phase
- High coupling between resources
- Small team, simple infrastructure

---

## Module Structure

### Terraform Module Structure

```
modules/vpc/
├── README.md              # Module documentation
├── main.tf                # Primary resource definitions
├── variables.tf           # Input variable declarations
├── outputs.tf             # Output declarations
├── versions.tf            # Provider version constraints
├── CHANGELOG.md           # Version history
├── examples/
│   ├── basic/
│   │   └── main.tf        # Basic usage example
│   └── complete/
│       └── main.tf        # Advanced usage example
└── tests/
    └── vpc_test.go        # Terratest tests
```

### Pulumi Component Structure

```
components/vpc/
├── README.md              # Component documentation
├── index.ts               # Main component (TypeScript)
├── package.json           # Dependencies
├── tsconfig.json          # TypeScript config
├── CHANGELOG.md           # Version history
├── examples/
│   ├── basic/
│   │   └── index.ts
│   └── complete/
│       └── index.ts
└── tests/
    └── vpc.test.ts        # Unit tests
```

---

## Input Design

### Variable Patterns (Terraform)

**Required vs Optional:**
```hcl
# variables.tf

# Required: No default
variable "name" {
  type        = string
  description = "Name prefix for all resources"
}

# Optional: Has default
variable "vpc_cidr" {
  type        = string
  description = "VPC CIDR block"
  default     = "10.0.0.0/16"
}

# Optional: Nullable
variable "custom_tags" {
  type        = map(string)
  description = "Custom tags to apply to all resources"
  default     = {}
  nullable    = false  # Prevent null values
}
```

**Complex Types:**
```hcl
# Simple list
variable "availability_zones" {
  type        = list(string)
  description = "List of availability zones"
}

# List of objects
variable "subnets" {
  type = list(object({
    name = string
    cidr = string
    az   = string
    type = string  # "public" or "private"
  }))
  description = "Subnet configuration"
  default     = []
}

# Map of objects
variable "security_groups" {
  type = map(object({
    description = string
    ingress_rules = list(object({
      from_port   = number
      to_port     = number
      protocol    = string
      cidr_blocks = list(string)
    }))
  }))
  description = "Security group configurations"
  default     = {}
}
```

**Validation:**
```hcl
variable "environment" {
  type        = string
  description = "Environment name (prod, staging, dev)"

  validation {
    condition     = contains(["prod", "staging", "dev"], var.environment)
    error_message = "Environment must be prod, staging, or dev."
  }
}

variable "vpc_cidr" {
  type        = string
  description = "VPC CIDR block"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "Must be a valid IPv4 CIDR block."
  }
}

variable "instance_count" {
  type        = number
  description = "Number of instances to create"

  validation {
    condition     = var.instance_count >= 1 && var.instance_count <= 10
    error_message = "Instance count must be between 1 and 10."
  }
}
```

### Input Design (Pulumi TypeScript)

```typescript
// vpc.ts
export interface VpcArgs {
  // Required
  name: string;
  availabilityZones: pulumi.Input<string>[];

  // Optional with defaults
  cidrBlock?: pulumi.Input<string>;
  enableNatGateway?: pulumi.Input<boolean>;
  enableVpnGateway?: pulumi.Input<boolean>;

  // Optional without defaults
  tags?: pulumi.Input<{ [key: string]: pulumi.Input<string> }>;
}

export class Vpc extends pulumi.ComponentResource {
  constructor(name: string, args: VpcArgs, opts?: pulumi.ComponentResourceOptions) {
    super("custom:network:Vpc", name, {}, opts);

    // Provide defaults
    const cidr = args.cidrBlock ?? "10.0.0.0/16";
    const enableNat = args.enableNatGateway ?? false;
    const enableVpn = args.enableVpnGateway ?? false;

    // Validate inputs
    if (pulumi.runtime.isDryRun()) {
      const azCount = pulumi.output(args.availabilityZones).apply(azs => azs.length);
      azCount.apply(count => {
        if (count < 2) {
          throw new Error("At least 2 availability zones required");
        }
      });
    }

    // ...
  }
}
```

---

## Output Design

### Output Patterns (Terraform)

```hcl
# outputs.tf

# Simple output
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

# List output
output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}

# Map output
output "subnet_cidrs" {
  description = "Map of subnet names to CIDR blocks"
  value = {
    for k, subnet in aws_subnet.private :
    k => subnet.cidr_block
  }
}

# Complex output
output "vpc_info" {
  description = "VPC information"
  value = {
    vpc_id              = aws_vpc.main.id
    vpc_cidr            = aws_vpc.main.cidr_block
    public_subnet_ids   = aws_subnet.public[*].id
    private_subnet_ids  = aws_subnet.private[*].id
    nat_gateway_ids     = aws_nat_gateway.main[*].id
  }
}

# Sensitive output
output "database_password" {
  description = "Database master password"
  value       = random_password.db.result
  sensitive   = true  # Hidden in logs
}

# Conditional output
output "bastion_ip" {
  description = "Bastion host public IP (if enabled)"
  value       = var.enable_bastion ? aws_instance.bastion[0].public_ip : null
}
```

### Output Design (Pulumi)

```typescript
export class Vpc extends pulumi.ComponentResource {
  // Public outputs
  public readonly vpcId: pulumi.Output<string>;
  public readonly publicSubnetIds: pulumi.Output<string>[];
  public readonly privateSubnetIds: pulumi.Output<string>[];

  constructor(name: string, args: VpcArgs, opts?: pulumi.ComponentResourceOptions) {
    super("custom:network:Vpc", name, {}, opts);

    // Create resources...

    // Assign outputs
    this.vpcId = vpc.id;
    this.publicSubnetIds = publicSubnets.map(s => s.id);
    this.privateSubnetIds = privateSubnets.map(s => s.id);

    // Register outputs for stack exports
    this.registerOutputs({
      vpcId: this.vpcId,
      publicSubnetIds: this.publicSubnetIds,
      privateSubnetIds: this.privateSubnetIds,
    });
  }
}
```

---

## Module Composition

### Terraform Module Composition

**modules/vpc/main.tf:**
```hcl
# VPC Module (Low-level)
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags                 = merge(var.tags, { Name = var.name })
}

resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, count.index)
  availability_zone = var.availability_zones[count.index]
  tags              = merge(var.tags, { Name = "${var.name}-private-${count.index}" })
}

# ... more resources
```

**modules/ecs-cluster/main.tf:**
```hcl
# ECS Cluster Module (Mid-level)
# Depends on VPC module

resource "aws_ecs_cluster" "main" {
  name = var.cluster_name

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_cluster_capacity_providers" "main" {
  cluster_name       = aws_ecs_cluster.main.name
  capacity_providers = ["FARGATE", "FARGATE_SPOT"]

  default_capacity_provider_strategy {
    base              = 1
    weight            = 100
    capacity_provider = "FARGATE"
  }
}
```

**environments/prod/main.tf:**
```hcl
# Application Composition (High-level)
# Composes multiple modules

module "vpc" {
  source = "../../modules/vpc"

  name               = "prod"
  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  enable_nat_gateway = true

  tags = local.common_tags
}

module "ecs_cluster" {
  source = "../../modules/ecs-cluster"

  cluster_name = "prod-cluster"
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.private_subnet_ids

  tags = local.common_tags
}

module "api_service" {
  source = "../../modules/ecs-service"

  service_name  = "api"
  cluster_id    = module.ecs_cluster.cluster_id
  vpc_id        = module.vpc.vpc_id
  subnet_ids    = module.vpc.private_subnet_ids
  desired_count = 3

  tags = local.common_tags
}
```

### Pulumi Component Composition

```typescript
// infrastructure/index.ts
import { Vpc } from "./components/vpc";
import { EcsCluster } from "./components/ecs-cluster";
import { EcsService } from "./components/ecs-service";

// Create VPC
const vpc = new Vpc("prod", {
  cidrBlock: "10.0.0.0/16",
  availabilityZones: ["us-east-1a", "us-east-1b", "us-east-1c"],
  enableNatGateway: true,
});

// Create ECS Cluster
const cluster = new EcsCluster("prod-cluster", {
  vpcId: vpc.vpcId,
  subnetIds: vpc.privateSubnetIds,
});

// Create ECS Service
const apiService = new EcsService("api", {
  clusterId: cluster.clusterId,
  vpcId: vpc.vpcId,
  subnetIds: vpc.privateSubnetIds,
  desiredCount: 3,
});

export const vpcId = vpc.vpcId;
export const clusterArn = cluster.clusterArn;
export const serviceArn = apiService.serviceArn;
```

---

## Versioning Strategy

### Semantic Versioning

Follow [Semantic Versioning](https://semver.org/):
- **Major version** (1.0.0 → 2.0.0): Breaking changes
- **Minor version** (1.0.0 → 1.1.0): New features, backward compatible
- **Patch version** (1.0.0 → 1.0.1): Bug fixes, backward compatible

**Example: Breaking vs Non-Breaking Changes**

**Breaking Change (Major Version):**
```hcl
# v1.0.0
variable "vpc_cidr" {
  type = string
}

# v2.0.0 (BREAKING: changed variable name)
variable "cidr_block" {  # Renamed variable
  type = string
}
```

**Non-Breaking Change (Minor Version):**
```hcl
# v1.0.0
output "vpc_id" {
  value = aws_vpc.main.id
}

# v1.1.0 (NON-BREAKING: new output)
output "vpc_id" {
  value = aws_vpc.main.id
}

output "vpc_cidr" {  # New output
  value = aws_vpc.main.cidr_block
}
```

### Version Pinning

**Terraform - Pin Module Versions:**
```hcl
# ❌ BAD: No version constraint (uses latest)
module "vpc" {
  source = "git::https://github.com/company/terraform-modules.git//vpc"
}

# ⚠️ BETTER: Use version tag
module "vpc" {
  source = "git::https://github.com/company/terraform-modules.git//vpc?ref=v2.3.0"
}

# ✅ BEST: Use Terraform Registry with version constraint
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"  # Exact version for production

  # Or allow patch updates
  # version = "~> 5.1.0"  # Allows 5.1.x
}
```

**Pulumi - Pin Package Versions:**
```json
// package.json
{
  "dependencies": {
    "@pulumi/aws": "6.8.0",  // Exact version
    "@company/pulumi-vpc": "^2.3.0"  // Allows 2.x updates
  }
}
```

### CHANGELOG.md

```markdown
# Changelog

All notable changes to this module will be documented in this file.

## [2.1.0] - 2025-01-15

### Added
- Support for IPv6 dual-stack VPCs
- New output: `ipv6_cidr_block`

### Changed
- Default NAT gateway count changed from 1 to match AZ count

## [2.0.0] - 2024-12-01

### Breaking Changes
- Renamed variable `vpc_cidr` to `cidr_block` for consistency
- Removed deprecated `enable_s3_endpoint` variable (use `vpc_endpoints` instead)

### Added
- Support for multiple VPC endpoints

## [1.2.1] - 2024-10-20

### Fixed
- Fixed NAT gateway route table associations
```

---

## Module Registries

### Terraform Registry (Public)

**Publishing to Terraform Registry:**

1. GitHub repository structure:
```
terraform-aws-vpc/
├── main.tf
├── variables.tf
├── outputs.tf
├── README.md
├── LICENSE
├── examples/
└── .github/
    └── workflows/
        └── release.yml
```

2. Tag release:
```bash
git tag v1.0.0
git push origin v1.0.0
```

3. Registry automatically indexes module.

**Using Public Modules:**
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"
}
```

### Private Module Registry

**Terraform Cloud/Enterprise:**
```hcl
module "vpc" {
  source  = "app.terraform.io/company/vpc/aws"
  version = "2.3.0"
}
```

**Git-Based Private Registry:**
```hcl
module "vpc" {
  source = "git::ssh://git@github.com/company/terraform-modules.git//vpc?ref=v2.3.0"
}
```

### Pulumi Packages

**Publishing to npm (TypeScript):**
```bash
npm publish
```

**Using Private Package:**
```json
// package.json
{
  "dependencies": {
    "@company/pulumi-vpc": "^2.3.0"
  }
}
```

```typescript
import { Vpc } from "@company/pulumi-vpc";

const vpc = new Vpc("main", { ... });
```

---

## Testing Modules

### Unit Testing with Terratest (Go)

```go
// tests/vpc_test.go
package test

import (
    "testing"

    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestVpcModule(t *testing.T) {
    t.Parallel()

    terraformOptions := &terraform.Options{
        TerraformDir: "../examples/complete",
        Vars: map[string]interface{}{
            "name":               "test",
            "vpc_cidr":           "10.0.0.0/16",
            "availability_zones": []string{"us-east-1a", "us-east-1b"},
        },
        EnvVars: map[string]string{
            "AWS_DEFAULT_REGION": "us-east-1",
        },
    }

    // Clean up resources after test
    defer terraform.Destroy(t, terraformOptions)

    // Deploy infrastructure
    terraform.InitAndApply(t, terraformOptions)

    // Validate outputs
    vpcId := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcId)
    assert.Regexp(t, "^vpc-", vpcId)

    privateSubnetIds := terraform.OutputList(t, terraformOptions, "private_subnet_ids")
    assert.Len(t, privateSubnetIds, 2)
}

func TestVpcValidation(t *testing.T) {
    t.Parallel()

    terraformOptions := &terraform.Options{
        TerraformDir: "../",
        Vars: map[string]interface{}{
            "name":     "test",
            "vpc_cidr": "invalid-cidr",  // Invalid CIDR
        },
    }

    // Expect validation to fail
    _, err := terraform.InitAndApplyE(t, terraformOptions)
    assert.Error(t, err)
}
```

### Unit Testing with Pulumi (TypeScript)

```typescript
// tests/vpc.test.ts
import * as pulumi from "@pulumi/pulumi";
import { Vpc } from "../index";

pulumi.runtime.setMocks({
  newResource: function(args: pulumi.runtime.MockResourceArgs): {id: string, state: any} {
    switch (args.type) {
      case "aws:ec2/vpc:Vpc":
        return { id: "vpc-12345", state: { ...args.inputs, id: "vpc-12345" } };
      case "aws:ec2/subnet:Subnet":
        return { id: "subnet-12345", state: { ...args.inputs, id: "subnet-12345" } };
      default:
        return { id: args.inputs.name + "_id", state: args.inputs };
    }
  },
  call: function(args: pulumi.runtime.MockCallArgs) {
    return args.inputs;
  },
});

describe("VPC Component", () => {
  let vpc: Vpc;

  before(async () => {
    vpc = new Vpc("test", {
      name: "test-vpc",
      availabilityZones: ["us-east-1a", "us-east-1b"],
    });
  });

  it("must have a VPC ID", (done) => {
    pulumi.all([vpc.vpcId]).apply(([vpcId]) => {
      expect(vpcId).to.contain("vpc-");
      done();
    });
  });

  it("must create subnets in each AZ", (done) => {
    pulumi.all([vpc.privateSubnetIds]).apply(([subnetIds]) => {
      expect(subnetIds).to.have.length(2);
      done();
    });
  });
});
```

### Policy Testing (Sentinel/OPA)

**Sentinel (Terraform Cloud):**
```hcl
# sentinel.hcl
policy "enforce-vpc-encryption" {
  enforcement_level = "hard-mandatory"
}

policy "require-tags" {
  enforcement_level = "soft-mandatory"
}
```

```python
# enforce-vpc-encryption.sentinel
import "tfplan/v2" as tfplan

main = rule {
  all tfplan.resource_changes as _, rc {
    rc.type is "aws_vpc" implies
      rc.change.after.enable_dns_support is true
  }
}
```

---

## Documentation

### Module README Template

```markdown
# VPC Module

Terraform module for creating a production-ready AWS VPC.

## Features

- Multi-AZ deployment
- Public and private subnets
- NAT gateways for private subnet internet access
- Optional VPN gateway
- Flow logs to CloudWatch

## Usage

### Basic Example

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"

  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
}
```

### Complete Example

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"

  name               = "production-vpc"
  cidr               = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

  enable_nat_gateway = true
  enable_vpn_gateway = true
  enable_flow_logs   = true

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
  }
}
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.6 |
| aws | >= 5.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| name | Name prefix for resources | `string` | n/a | yes |
| cidr | VPC CIDR block | `string` | `"10.0.0.0/16"` | no |
| availability_zones | List of AZs | `list(string)` | n/a | yes |
| enable_nat_gateway | Enable NAT gateways | `bool` | `false` | no |

## Outputs

| Name | Description |
|------|-------------|
| vpc_id | VPC ID |
| private_subnet_ids | List of private subnet IDs |
| public_subnet_ids | List of public subnet IDs |

## License

MIT
```

---

## Best Practices

**Module Design:**
- ✅ Single responsibility principle
- ✅ Clear input/output contract
- ✅ Validation for critical inputs
- ✅ Sane defaults where appropriate
- ✅ Comprehensive documentation

**Versioning:**
- ✅ Semantic versioning (MAJOR.MINOR.PATCH)
- ✅ Pin versions in production
- ✅ Maintain CHANGELOG.md
- ✅ Test before releasing

**Testing:**
- ✅ Unit tests for module logic
- ✅ Integration tests for deployments
- ✅ Policy tests for compliance
- ✅ Automated testing in CI

**Documentation:**
- ✅ Clear README with examples
- ✅ Document all inputs and outputs
- ✅ Provide basic and complete examples
- ✅ Explain common use cases

---

See SKILL.md for links to testing infrastructure and CI/CD integration topics.
