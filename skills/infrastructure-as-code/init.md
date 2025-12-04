# Infrastructure as Code Skill - Master Plan

**Skill Name:** `infrastructure-as-code`
**Skill Level:** High Level (8,000-12,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [IaC Tool Taxonomy](#iac-tool-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Multi-Language Implementations](#multi-language-implementations)
7. [State Management Patterns](#state-management-patterns)
8. [Module Design Patterns](#module-design-patterns)
9. [Library Recommendations](#library-recommendations)
10. [Skill Structure Design](#skill-structure-design)
11. [Integration Points](#integration-points)
12. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

Infrastructure as Code (IaC) is the foundation of modern cloud operations. In 2025, with multi-cloud strategies, platform engineering, and GitOps becoming standard, comprehensive IaC skills are essential for any organization.

**Market Drivers:**
- **Multi-Cloud Reality:** 90%+ enterprises use multiple cloud providers
- **Platform Engineering:** Internal developer platforms require standardized IaC
- **GitOps Adoption:** IaC + Git = auditable, reproducible infrastructure
- **FinOps Integration:** Cost optimization requires infrastructure visibility
- **Compliance Requirements:** Regulatory needs demand infrastructure auditability

**Strategic Value:**
1. **Foundation Skill:** Every cloud deployment starts with IaC
2. **Tool Agnostic:** Patterns apply across Terraform, Pulumi, CDK
3. **Multi-Cloud:** Same concepts work across AWS, GCP, Azure
4. **DevOps Critical:** CI/CD pipelines depend on reliable IaC

### How This Differs from Existing Solutions

**Existing IaC Documentation:**
- **Tool-Specific:** Terraform docs OR Pulumi docs, not unified
- **Single-Cloud:** AWS examples OR GCP examples
- **Tactical Focus:** "How to create a resource" vs "How to architect modules"

**Our Approach:**
- **Decision Framework:** When to use Terraform vs Pulumi vs CDK
- **Multi-Language:** HCL, TypeScript, Python, Go examples
- **State Management:** Critical patterns often overlooked
- **Module Architecture:** Composable, reusable infrastructure
- **Drift Detection:** Operational reality beyond initial deployment

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **Tool Selection**
   - Terraform/OpenTofu for multi-cloud, declarative IaC
   - Pulumi for developer-centric, programming language IaC
   - AWS CDK for AWS-native, TypeScript/Python IaC
   - CloudFormation for AWS-native, YAML/JSON IaC

2. **State Management**
   - Remote state backends (S3, GCS, Azure Blob)
   - State locking for team collaboration
   - State isolation strategies (workspaces vs directories)
   - Sensitive data handling in state

3. **Module Architecture**
   - Composable module design
   - Module versioning and registries
   - Input/output contracts
   - Testing infrastructure code

4. **Operational Patterns**
   - Drift detection and remediation
   - Import existing resources
   - Blue-green infrastructure deployments
   - Disaster recovery patterns

### What This Skill Does NOT Cover

- Cloud provider specifics (use aws-patterns, gcp-patterns skills)
- Kubernetes manifests (use kubernetes-operations skill)
- CI/CD pipeline construction (use building-ci-pipelines skill)
- Secret management details (use secret-management skill)

---

## Research Findings

### Google Search Grounding (December 2025)

**Key 2025 Trends:**
- Terraform remains dominant but OpenTofu gaining adoption
- Pulumi preferred by developer-centric teams
- CDK adoption growing for AWS-heavy organizations
- State management and drift detection are top operational challenges
- Module composition and testing becoming standard practices

**Best Practices Identified:**
1. Treat infrastructure as software (testing, code reviews, CI/CD)
2. Automation reduces human error and accelerates deployment
3. Idempotency ensures safe repeated execution
4. Version control enables rollback and auditing
5. Modular design enables reusability

### Tool Comparison Matrix

| Aspect | Terraform | Pulumi | AWS CDK | CloudFormation |
|--------|-----------|--------|---------|----------------|
| **Language** | HCL | TS/Python/Go/C# | TS/Python/Java | YAML/JSON |
| **Multi-Cloud** | Excellent | Excellent | AWS Only | AWS Only |
| **Learning Curve** | Medium | Low (if you know lang) | Medium | Low |
| **State** | Remote backend | Pulumi Service/S3 | CloudFormation | CloudFormation |
| **Ecosystem** | Largest | Growing | AWS-focused | AWS-focused |
| **Testing** | Terratest | Native unit tests | CDK assertions | cfn-lint |
| **Best For** | Ops teams, multi-cloud | Dev teams, polyglot | AWS shops, devs | AWS-native, simple |

---

## IaC Tool Taxonomy

### Tier 1: Declarative Multi-Cloud (Terraform/OpenTofu)

**Use When:**
- Multi-cloud or hybrid-cloud deployments
- Ops/SRE team manages infrastructure
- Large ecosystem of providers needed
- Compliance requires reproducible state

**HCL Example - VPC Module:**
```hcl
# modules/vpc/main.tf
variable "name" {
  type        = string
  description = "VPC name prefix"
}

variable "cidr" {
  type        = string
  default     = "10.0.0.0/16"
}

variable "azs" {
  type        = list(string)
  description = "Availability zones"
}

resource "aws_vpc" "main" {
  cidr_block           = var.cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = var.name
    ManagedBy   = "terraform"
    Environment = terraform.workspace
  }
}

resource "aws_subnet" "private" {
  count             = length(var.azs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.cidr, 4, count.index)
  availability_zone = var.azs[count.index]

  tags = {
    Name = "${var.name}-private-${var.azs[count.index]}"
    Type = "private"
  }
}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}
```

### Tier 2: Imperative Multi-Cloud (Pulumi)

**Use When:**
- Developer team manages infrastructure
- Complex logic required (loops, conditionals)
- Native testing desired
- Team prefers TypeScript/Python/Go

**TypeScript Example - VPC:**
```typescript
// infra/vpc.ts
import * as aws from "@pulumi/aws";
import * as pulumi from "@pulumi/pulumi";

export interface VpcArgs {
  name: string;
  cidr?: string;
  azs: string[];
}

export class Vpc extends pulumi.ComponentResource {
  public readonly vpcId: pulumi.Output<string>;
  public readonly privateSubnetIds: pulumi.Output<string>[];

  constructor(name: string, args: VpcArgs, opts?: pulumi.ComponentResourceOptions) {
    super("custom:network:Vpc", name, {}, opts);

    const vpc = new aws.ec2.Vpc(`${name}-vpc`, {
      cidrBlock: args.cidr ?? "10.0.0.0/16",
      enableDnsHostnames: true,
      enableDnsSupport: true,
      tags: { Name: args.name, ManagedBy: "pulumi" },
    }, { parent: this });

    this.vpcId = vpc.id;

    this.privateSubnetIds = args.azs.map((az, i) => {
      const subnet = new aws.ec2.Subnet(`${name}-private-${i}`, {
        vpcId: vpc.id,
        cidrBlock: `10.0.${i}.0/24`,
        availabilityZone: az,
        tags: { Name: `${args.name}-private-${az}`, Type: "private" },
      }, { parent: this });
      return subnet.id;
    });

    this.registerOutputs({
      vpcId: this.vpcId,
      privateSubnetIds: this.privateSubnetIds,
    });
  }
}
```

**Python Example - VPC:**
```python
# infra/vpc.py
import pulumi
import pulumi_aws as aws
from typing import List, Optional

class VpcArgs:
    def __init__(self, name: str, azs: List[str], cidr: str = "10.0.0.0/16"):
        self.name = name
        self.azs = azs
        self.cidr = cidr

class Vpc(pulumi.ComponentResource):
    def __init__(self, name: str, args: VpcArgs, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("custom:network:Vpc", name, None, opts)

        self.vpc = aws.ec2.Vpc(
            f"{name}-vpc",
            cidr_block=args.cidr,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            tags={"Name": args.name, "ManagedBy": "pulumi"},
            opts=pulumi.ResourceOptions(parent=self),
        )

        self.private_subnets = []
        for i, az in enumerate(args.azs):
            subnet = aws.ec2.Subnet(
                f"{name}-private-{i}",
                vpc_id=self.vpc.id,
                cidr_block=f"10.0.{i}.0/24",
                availability_zone=az,
                tags={"Name": f"{args.name}-private-{az}", "Type": "private"},
                opts=pulumi.ResourceOptions(parent=self),
            )
            self.private_subnets.append(subnet)

        self.register_outputs({
            "vpc_id": self.vpc.id,
            "private_subnet_ids": [s.id for s in self.private_subnets],
        })
```

**Go Example - VPC:**
```go
// infra/vpc.go
package infra

import (
	"fmt"
	"github.com/pulumi/pulumi-aws/sdk/v6/go/aws/ec2"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

type VpcArgs struct {
	Name string
	Cidr string
	Azs  []string
}

type Vpc struct {
	pulumi.ResourceState
	VpcId            pulumi.StringOutput   `pulumi:"vpcId"`
	PrivateSubnetIds pulumi.StringArrayOutput `pulumi:"privateSubnetIds"`
}

func NewVpc(ctx *pulumi.Context, name string, args *VpcArgs) (*Vpc, error) {
	vpc := &Vpc{}
	err := ctx.RegisterComponentResource("custom:network:Vpc", name, vpc)
	if err != nil {
		return nil, err
	}

	awsVpc, err := ec2.NewVpc(ctx, fmt.Sprintf("%s-vpc", name), &ec2.VpcArgs{
		CidrBlock:          pulumi.String(args.Cidr),
		EnableDnsHostnames: pulumi.Bool(true),
		EnableDnsSupport:   pulumi.Bool(true),
		Tags: pulumi.StringMap{
			"Name":      pulumi.String(args.Name),
			"ManagedBy": pulumi.String("pulumi"),
		},
	}, pulumi.Parent(vpc))
	if err != nil {
		return nil, err
	}

	vpc.VpcId = awsVpc.ID().ToStringOutput()

	subnetIds := pulumi.StringArray{}
	for i, az := range args.Azs {
		subnet, err := ec2.NewSubnet(ctx, fmt.Sprintf("%s-private-%d", name, i), &ec2.SubnetArgs{
			VpcId:            awsVpc.ID(),
			CidrBlock:        pulumi.String(fmt.Sprintf("10.0.%d.0/24", i)),
			AvailabilityZone: pulumi.String(az),
			Tags: pulumi.StringMap{
				"Name": pulumi.String(fmt.Sprintf("%s-private-%s", args.Name, az)),
				"Type": pulumi.String("private"),
			},
		}, pulumi.Parent(vpc))
		if err != nil {
			return nil, err
		}
		subnetIds = append(subnetIds, subnet.ID().ToStringOutput())
	}
	vpc.PrivateSubnetIds = subnetIds.ToStringArrayOutput()

	return vpc, nil
}
```

### Tier 3: AWS-Native (CDK/CloudFormation)

**Use When:**
- AWS-only infrastructure
- Tight integration with AWS services
- Team familiar with TypeScript/Python
- AWS Construct Library benefits needed

**CDK TypeScript Example:**
```typescript
// lib/vpc-stack.ts
import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import { Construct } from 'constructs';

export interface VpcStackProps extends cdk.StackProps {
  maxAzs?: number;
}

export class VpcStack extends cdk.Stack {
  public readonly vpc: ec2.Vpc;

  constructor(scope: Construct, id: string, props?: VpcStackProps) {
    super(scope, id, props);

    this.vpc = new ec2.Vpc(this, 'MainVpc', {
      maxAzs: props?.maxAzs ?? 3,
      natGateways: 1,
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: 'Public',
          subnetType: ec2.SubnetType.PUBLIC,
        },
        {
          cidrMask: 24,
          name: 'Private',
          subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
        },
        {
          cidrMask: 28,
          name: 'Isolated',
          subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
        },
      ],
    });

    new cdk.CfnOutput(this, 'VpcId', { value: this.vpc.vpcId });
  }
}
```

---

## Decision Frameworks

### Framework 1: Which IaC Tool?

```
START
  │
  ├─► Multi-cloud required?
  │     YES ──► Team composition?
  │               ├─► Ops/SRE heavy ──► TERRAFORM
  │               └─► Dev heavy ──► PULUMI
  │     NO ──► AWS only?
  │              YES ──► Language preference?
  │                       ├─► HCL/declarative ──► TERRAFORM
  │                       ├─► TypeScript/Python ──► CDK
  │                       └─► YAML/simple ──► CLOUDFORMATION
  │              NO ──► GCP/Azure only?
  │                       ├─► GCP ──► TERRAFORM or PULUMI
  │                       └─► Azure ──► TERRAFORM or BICEP
```

### Framework 2: State Backend Selection

| Scenario | Backend | Why |
|----------|---------|-----|
| AWS + Team | S3 + DynamoDB | Native locking, IAM integration |
| GCP + Team | GCS | Native locking |
| Azure + Team | Azure Blob | Native locking |
| Multi-cloud | Terraform Cloud | Unified state management |
| Pulumi | Pulumi Service | Best integration, free tier |
| Self-hosted | PostgreSQL | Full control, air-gapped |

### Framework 3: Module vs Monolith

**Use Modules When:**
- Resource group is reused 3+ times
- Clear input/output contract exists
- Team can maintain versioned modules
- Testing infrastructure is available

**Keep Monolith When:**
- One-off infrastructure
- Rapid prototyping phase
- Small team, simple infrastructure
- High coupling between resources

### Framework 4: Workspace vs Directory Isolation

| Approach | Use Case | Pros | Cons |
|----------|----------|------|------|
| **Workspaces** | Same infra, different envs | Single codebase | Shared state file risks |
| **Directories** | Different infra per env | Full isolation | Code duplication |
| **Terragrunt** | Complex multi-env | DRY + isolation | Added complexity |

---

## State Management Patterns

### Pattern 1: Remote State with Locking

**Terraform S3 Backend:**
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "prod/vpc/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

**State Bucket Setup (one-time):**
```hcl
# bootstrap/state-bucket.tf
resource "aws_s3_bucket" "state" {
  bucket = "company-terraform-state"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "state" {
  bucket = aws_s3_bucket.state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "state" {
  bucket = aws_s3_bucket.state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

resource "aws_dynamodb_table" "locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

### Pattern 2: State Isolation Strategy

```
terraform-states/
├── bootstrap/           # State bucket itself (local state, careful!)
├── networking/
│   ├── prod/           # prod/networking/terraform.tfstate
│   ├── staging/        # staging/networking/terraform.tfstate
│   └── dev/            # dev/networking/terraform.tfstate
├── compute/
│   ├── prod/
│   ├── staging/
│   └── dev/
└── data/
    ├── prod/
    ├── staging/
    └── dev/
```

### Pattern 3: Sensitive Data in State

```hcl
# Mark outputs as sensitive
output "database_password" {
  value     = random_password.db.result
  sensitive = true
}

# Use data sources for secrets (don't store in state)
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret.db.id
}
```

---

## Module Design Patterns

### Pattern 1: Composable Modules

```
modules/
├── vpc/                 # Network foundation
├── security-group/      # Reusable SG patterns
├── rds/                 # Database module
├── ecs-cluster/         # ECS base
├── ecs-service/         # Individual service
└── alb/                 # Load balancer
```

**Module Composition:**
```hcl
# environments/prod/main.tf
module "vpc" {
  source = "../../modules/vpc"
  name   = "prod"
  cidr   = "10.0.0.0/16"
}

module "web_sg" {
  source = "../../modules/security-group"
  name   = "web"
  vpc_id = module.vpc.vpc_id
  rules  = local.web_sg_rules
}

module "api" {
  source           = "../../modules/ecs-service"
  name             = "api"
  cluster_id       = module.ecs.cluster_id
  vpc_id           = module.vpc.vpc_id
  subnet_ids       = module.vpc.private_subnet_ids
  security_groups  = [module.web_sg.id]
}
```

### Pattern 2: Module Versioning

```hcl
# Use versioned modules from registry
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"  # Pin version!

  name = "prod-vpc"
  cidr = "10.0.0.0/16"
}

# Use versioned modules from Git
module "internal_vpc" {
  source = "git::https://github.com/company/tf-modules.git//vpc?ref=v2.3.0"

  name = "internal"
}
```

### Pattern 3: Module Testing

**Terratest Example (Go):**
```go
// test/vpc_test.go
package test

import (
	"testing"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestVpcModule(t *testing.T) {
	terraformOptions := &terraform.Options{
		TerraformDir: "../modules/vpc",
		Vars: map[string]interface{}{
			"name": "test",
			"cidr": "10.0.0.0/16",
			"azs":  []string{"us-east-1a", "us-east-1b"},
		},
	}

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	vpcId := terraform.Output(t, terraformOptions, "vpc_id")
	assert.NotEmpty(t, vpcId)
}
```

---

## Library Recommendations

### Primary Tools

| Tool | Version | Use Case | Languages |
|------|---------|----------|-----------|
| **Terraform** | 1.6+ | Multi-cloud declarative | HCL |
| **OpenTofu** | 1.6+ | Open-source Terraform fork | HCL |
| **Pulumi** | 3.x | Developer-centric IaC | TS, Python, Go, C# |
| **AWS CDK** | 2.x | AWS-native constructs | TS, Python, Java, C# |

### Supporting Tools

| Tool | Purpose |
|------|---------|
| **Terragrunt** | DRY Terraform wrapper |
| **tflint** | Terraform linter |
| **Checkov** | IaC security scanner |
| **Infracost** | Cost estimation |
| **Terratest** | Infrastructure testing |
| **driftctl** | Drift detection |

---

## Skill Structure Design

```
infrastructure-as-code/
├── SKILL.md                         # Main skill (500-700 lines)
├── references/
│   ├── terraform-patterns.md        # HCL best practices
│   ├── pulumi-patterns.md           # Multi-language Pulumi
│   ├── cdk-patterns.md              # AWS CDK specifics
│   ├── state-management.md          # State backends, locking
│   ├── module-design.md             # Composable modules
│   ├── drift-detection.md           # Operational patterns
│   └── testing-iac.md               # Terratest, CDK assertions
├── examples/
│   ├── terraform/
│   │   ├── vpc-module/
│   │   ├── ecs-service/
│   │   └── rds-cluster/
│   ├── pulumi/
│   │   ├── typescript/
│   │   ├── python/
│   │   └── go/
│   └── cdk/
│       └── typescript/
└── scripts/
    ├── validate-tf.sh               # Terraform validation
    ├── cost-estimate.sh             # Infracost wrapper
    └── drift-check.sh               # Drift detection
```

---

## Integration Points

### With Existing Skills

| Skill | Integration |
|-------|-------------|
| `deploying-applications` | IaC creates infrastructure for deployments |
| `kubernetes-operations` | Terraform provisions EKS/GKE/AKS clusters |
| `building-ci-pipelines` | CI/CD runs terraform plan/apply |
| `secret-management` | Vault/ESO provisioned via IaC |
| `observability` | Monitoring infrastructure via IaC |

### Skill Chaining Example

```
infrastructure-as-code → kubernetes-operations → deploying-applications
        │                        │                       │
        ▼                        ▼                       ▼
  Create EKS cluster    Configure RBAC, HPA      Deploy workloads
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Core decision frameworks
- [ ] Terraform patterns and examples
- [ ] State management deep-dive

### Phase 2: Multi-Language (Week 3-4)
- [ ] Pulumi TypeScript examples
- [ ] Pulumi Python examples
- [ ] Pulumi Go examples

### Phase 3: Advanced Patterns (Week 5-6)
- [ ] Module composition
- [ ] Testing infrastructure
- [ ] Drift detection

### Phase 4: Integration (Week 7-8)
- [ ] CI/CD integration patterns
- [ ] CDK examples
- [ ] Polish and review

---

## Key Takeaways

1. **Choose the right tool** - Terraform for ops, Pulumi for devs, CDK for AWS-native
2. **State management is critical** - Remote backends with locking are non-negotiable
3. **Modules enable scale** - Composable, versioned, tested modules
4. **Drift happens** - Plan for detection and remediation
5. **Test infrastructure** - Terratest, CDK assertions, policy checks
6. **Multi-language support** - HCL, TypeScript, Python, Go for different teams

---

**Progressive disclosure:** This init.md provides the master plan. Detailed documentation in `references/` directory.
