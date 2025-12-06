# Pulumi Patterns - Multi-Language Infrastructure as Code

Comprehensive guide to Pulumi across TypeScript, Python, and Go with modern programming patterns.

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [TypeScript Patterns](#typescript-patterns)
3. [Python Patterns](#python-patterns)
4. [Go Patterns](#go-patterns)
5. [Component Resources](#component-resources)
6. [Stack References](#stack-references)
7. [Configuration Management](#configuration-management)
8. [Secrets Management](#secrets-management)
9. [Testing Patterns](#testing-patterns)
10. [Automation API](#automation-api)

---

## Core Concepts

### Pulumi vs Terraform

| Aspect | Pulumi | Terraform |
|--------|--------|-----------|
| Language | TypeScript/Python/Go/C#/.NET | HCL |
| State | Pulumi Service or S3 | S3/GCS/Blob/TF Cloud |
| Testing | Native unit tests | Terratest (Go) |
| Loops/Conditionals | Native language | Limited HCL |
| IDE Support | Full IntelliSense | Limited |
| Type Safety | Strong (TS/Go) | None (HCL) |

### Project Structure

```
pulumi-project/
├── Pulumi.yaml           # Project metadata
├── Pulumi.dev.yaml       # Dev stack config
├── Pulumi.staging.yaml   # Staging stack config
├── Pulumi.prod.yaml      # Prod stack config
├── index.ts              # Main program (TypeScript)
├── package.json          # Node dependencies
├── tsconfig.json         # TypeScript config
├── src/
│   ├── vpc.ts            # VPC component
│   ├── ecs.ts            # ECS component
│   └── rds.ts            # RDS component
└── tests/
    └── infrastructure.test.ts
```

---

## TypeScript Patterns

### Basic Project Setup

```bash
# Initialize new project
pulumi new aws-typescript

# Install dependencies
npm install

# Preview changes
pulumi preview

# Deploy
pulumi up

# Destroy
pulumi destroy
```

### Simple Resources

```typescript
// index.ts
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// Create VPC
const vpc = new aws.ec2.Vpc("main-vpc", {
  cidrBlock: "10.0.0.0/16",
  enableDnsHostnames: true,
  enableDnsSupport: true,
  tags: {
    Name: "main-vpc",
    ManagedBy: "pulumi",
  },
});

// Create subnet
const subnet = new aws.ec2.Subnet("private-subnet", {
  vpcId: vpc.id,
  cidrBlock: "10.0.1.0/24",
  availabilityZone: "us-east-1a",
  tags: {
    Name: "private-subnet-1a",
  },
});

// Export outputs
export const vpcId = vpc.id;
export const subnetId = subnet.id;
```

### Component Resources (TypeScript)

```typescript
// src/vpc.ts
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

export interface VpcArgs {
  cidrBlock?: pulumi.Input<string>;
  availabilityZones: pulumi.Input<string>[];
  enableNatGateway?: boolean;
  tags?: pulumi.Input<{ [key: string]: pulumi.Input<string> }>;
}

export class Vpc extends pulumi.ComponentResource {
  public readonly vpcId: pulumi.Output<string>;
  public readonly publicSubnetIds: pulumi.Output<string>[];
  public readonly privateSubnetIds: pulumi.Output<string>[];
  public readonly natGatewayIds?: pulumi.Output<string>[];

  constructor(name: string, args: VpcArgs, opts?: pulumi.ComponentResourceOptions) {
    super("custom:network:Vpc", name, {}, opts);

    const cidr = args.cidrBlock ?? "10.0.0.0/16";

    // Create VPC
    const vpc = new aws.ec2.Vpc(
      `${name}-vpc`,
      {
        cidrBlock: cidr,
        enableDnsHostnames: true,
        enableDnsSupport: true,
        tags: pulumi.output(args.tags).apply(tags => ({
          ...tags,
          Name: `${name}-vpc`,
        })),
      },
      { parent: this }
    );

    this.vpcId = vpc.id;

    // Create Internet Gateway
    const igw = new aws.ec2.InternetGateway(
      `${name}-igw`,
      {
        vpcId: vpc.id,
        tags: { Name: `${name}-igw` },
      },
      { parent: this }
    );

    // Create public subnets
    this.publicSubnetIds = [];
    const publicSubnets: aws.ec2.Subnet[] = [];

    pulumi.output(args.availabilityZones).apply(azs => {
      azs.forEach((az, i) => {
        const subnet = new aws.ec2.Subnet(
          `${name}-public-${i}`,
          {
            vpcId: vpc.id,
            cidrBlock: `10.0.${i}.0/24`,
            availabilityZone: az,
            mapPublicIpOnLaunch: true,
            tags: {
              Name: `${name}-public-${az}`,
              Type: "public",
            },
          },
          { parent: this }
        );
        publicSubnets.push(subnet);
        this.publicSubnetIds.push(subnet.id);
      });
    });

    // Create private subnets
    this.privateSubnetIds = [];
    const privateSubnets: aws.ec2.Subnet[] = [];

    pulumi.output(args.availabilityZones).apply(azs => {
      azs.forEach((az, i) => {
        const subnet = new aws.ec2.Subnet(
          `${name}-private-${i}`,
          {
            vpcId: vpc.id,
            cidrBlock: `10.0.${i + 10}.0/24`,
            availabilityZone: az,
            tags: {
              Name: `${name}-private-${az}`,
              Type: "private",
            },
          },
          { parent: this }
        );
        privateSubnets.push(subnet);
        this.privateSubnetIds.push(subnet.id);
      });
    });

    // Create NAT Gateways (optional)
    if (args.enableNatGateway) {
      this.natGatewayIds = [];

      pulumi.output(args.availabilityZones).apply(azs => {
        azs.forEach((az, i) => {
          const eip = new aws.ec2.Eip(
            `${name}-nat-eip-${i}`,
            {
              domain: "vpc",
              tags: { Name: `${name}-nat-eip-${az}` },
            },
            { parent: this }
          );

          const natGw = new aws.ec2.NatGateway(
            `${name}-nat-${i}`,
            {
              allocationId: eip.id,
              subnetId: publicSubnets[i].id,
              tags: { Name: `${name}-nat-${az}` },
            },
            { parent: this }
          );

          this.natGatewayIds!.push(natGw.id);
        });
      });
    }

    // Register outputs
    this.registerOutputs({
      vpcId: this.vpcId,
      publicSubnetIds: this.publicSubnetIds,
      privateSubnetIds: this.privateSubnetIds,
      natGatewayIds: this.natGatewayIds,
    });
  }
}
```

### Using Component Resources

```typescript
// index.ts
import { Vpc } from "./src/vpc";

const vpc = new Vpc("production", {
  cidrBlock: "10.0.0.0/16",
  availabilityZones: ["us-east-1a", "us-east-1b", "us-east-1c"],
  enableNatGateway: true,
  tags: {
    Environment: "production",
    ManagedBy: "pulumi",
  },
});

export const vpcId = vpc.vpcId;
export const publicSubnets = vpc.publicSubnetIds;
export const privateSubnets = vpc.privateSubnetIds;
```

### Advanced TypeScript Patterns

**Dynamic Resource Creation:**
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const subnetCount = config.getNumber("subnetCount") || 3;

// Create subnets dynamically
const subnets = Array.from({ length: subnetCount }, (_, i) => {
  return new aws.ec2.Subnet(`subnet-${i}`, {
    vpcId: vpc.id,
    cidrBlock: `10.0.${i}.0/24`,
    availabilityZone: `us-east-1${String.fromCharCode(97 + i)}`,
  });
});

export const subnetIds = subnets.map(s => s.id);
```

**Conditional Resources:**
```typescript
const config = new pulumi.Config();
const enableBastion = config.getBoolean("enableBastion") ?? false;

let bastionInstance: aws.ec2.Instance | undefined;

if (enableBastion) {
  bastionInstance = new aws.ec2.Instance("bastion", {
    ami: "ami-12345678",
    instanceType: "t3.micro",
    subnetId: publicSubnets[0],
  });
}

export const bastionIp = bastionInstance?.publicIp;
```

**Output Transformations:**
```typescript
// Transform outputs with apply()
const subnetCidrs = pulumi.all(subnets.map(s => s.cidrBlock)).apply(cidrs => {
  return cidrs.join(", ");
});

// Multiple outputs
const clusterEndpoint = pulumi.all([cluster.endpoint, cluster.port]).apply(
  ([endpoint, port]) => `${endpoint}:${port}`
);
```

---

## Python Patterns

### Basic Project Setup

```bash
# Initialize new project
pulumi new aws-python

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Deploy
pulumi up
```

### Simple Resources (Python)

```python
# __main__.py
import pulumi
import pulumi_aws as aws

# Create VPC
vpc = aws.ec2.Vpc(
    "main-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={
        "Name": "main-vpc",
        "ManagedBy": "pulumi",
    }
)

# Create subnet
subnet = aws.ec2.Subnet(
    "private-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="us-east-1a",
    tags={
        "Name": "private-subnet-1a",
    }
)

# Export outputs
pulumi.export("vpc_id", vpc.id)
pulumi.export("subnet_id", subnet.id)
```

### Component Resources (Python)

```python
# vpc.py
import pulumi
import pulumi_aws as aws
from typing import List, Optional, Sequence

class VpcArgs:
    def __init__(
        self,
        cidr_block: str = "10.0.0.0/16",
        availability_zones: Sequence[str] = None,
        enable_nat_gateway: bool = False,
        tags: Optional[dict] = None,
    ):
        self.cidr_block = cidr_block
        self.availability_zones = availability_zones or ["us-east-1a", "us-east-1b"]
        self.enable_nat_gateway = enable_nat_gateway
        self.tags = tags or {}

class Vpc(pulumi.ComponentResource):
    def __init__(
        self,
        name: str,
        args: VpcArgs,
        opts: Optional[pulumi.ResourceOptions] = None,
    ):
        super().__init__("custom:network:Vpc", name, None, opts)

        # Create VPC
        self.vpc = aws.ec2.Vpc(
            f"{name}-vpc",
            cidr_block=args.cidr_block,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            tags={**args.tags, "Name": f"{name}-vpc"},
            opts=pulumi.ResourceOptions(parent=self),
        )

        # Create Internet Gateway
        self.igw = aws.ec2.InternetGateway(
            f"{name}-igw",
            vpc_id=self.vpc.id,
            tags={"Name": f"{name}-igw"},
            opts=pulumi.ResourceOptions(parent=self),
        )

        # Create public subnets
        self.public_subnets = []
        for i, az in enumerate(args.availability_zones):
            subnet = aws.ec2.Subnet(
                f"{name}-public-{i}",
                vpc_id=self.vpc.id,
                cidr_block=f"10.0.{i}.0/24",
                availability_zone=az,
                map_public_ip_on_launch=True,
                tags={"Name": f"{name}-public-{az}", "Type": "public"},
                opts=pulumi.ResourceOptions(parent=self),
            )
            self.public_subnets.append(subnet)

        # Create private subnets
        self.private_subnets = []
        for i, az in enumerate(args.availability_zones):
            subnet = aws.ec2.Subnet(
                f"{name}-private-{i}",
                vpc_id=self.vpc.id,
                cidr_block=f"10.0.{i + 10}.0/24",
                availability_zone=az,
                tags={"Name": f"{name}-private-{az}", "Type": "private"},
                opts=pulumi.ResourceOptions(parent=self),
            )
            self.private_subnets.append(subnet)

        # Create NAT Gateways (optional)
        if args.enable_nat_gateway:
            self.nat_gateways = []
            for i, az in enumerate(args.availability_zones):
                eip = aws.ec2.Eip(
                    f"{name}-nat-eip-{i}",
                    domain="vpc",
                    tags={"Name": f"{name}-nat-eip-{az}"},
                    opts=pulumi.ResourceOptions(parent=self),
                )

                nat_gw = aws.ec2.NatGateway(
                    f"{name}-nat-{i}",
                    allocation_id=eip.id,
                    subnet_id=self.public_subnets[i].id,
                    tags={"Name": f"{name}-nat-{az}"},
                    opts=pulumi.ResourceOptions(parent=self),
                )
                self.nat_gateways.append(nat_gw)

        # Register outputs
        self.register_outputs({
            "vpc_id": self.vpc.id,
            "public_subnet_ids": [s.id for s in self.public_subnets],
            "private_subnet_ids": [s.id for s in self.private_subnets],
        })
```

### Using Component Resources (Python)

```python
# __main__.py
import pulumi
from vpc import Vpc, VpcArgs

# Create VPC
vpc = Vpc(
    "production",
    VpcArgs(
        cidr_block="10.0.0.0/16",
        availability_zones=["us-east-1a", "us-east-1b", "us-east-1c"],
        enable_nat_gateway=True,
        tags={"Environment": "production", "ManagedBy": "pulumi"},
    ),
)

# Export outputs
pulumi.export("vpc_id", vpc.vpc.id)
pulumi.export("public_subnets", [s.id for s in vpc.public_subnets])
pulumi.export("private_subnets", [s.id for s in vpc.private_subnets])
```

### Advanced Python Patterns

**Dynamic Resource Creation:**
```python
import pulumi
import pulumi_aws as aws

config = pulumi.Config()
subnet_count = config.get_int("subnet_count") or 3

# Create subnets dynamically
subnets = []
for i in range(subnet_count):
    subnet = aws.ec2.Subnet(
        f"subnet-{i}",
        vpc_id=vpc.id,
        cidr_block=f"10.0.{i}.0/24",
        availability_zone=f"us-east-1{chr(97 + i)}",
    )
    subnets.append(subnet)

pulumi.export("subnet_ids", [s.id for s in subnets])
```

**Output Transformations:**
```python
# Transform outputs with apply()
subnet_cidrs = pulumi.Output.all(*[s.cidr_block for s in subnets]).apply(
    lambda cidrs: ", ".join(cidrs)
)

# Conditional logic
def get_instance_type(env):
    return "t3.large" if env == "prod" else "t3.micro"

instance_type = pulumi.Output.from_input(environment).apply(get_instance_type)
```

---

## Go Patterns

### Basic Project Setup

```bash
# Initialize new project
pulumi new aws-go

# Build
go build -o pulumi-infrastructure

# Deploy
pulumi up
```

### Simple Resources (Go)

```go
// main.go
package main

import (
    "github.com/pulumi/pulumi-aws/sdk/v6/go/aws/ec2"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        // Create VPC
        vpc, err := ec2.NewVpc(ctx, "main-vpc", &ec2.VpcArgs{
            CidrBlock:          pulumi.String("10.0.0.0/16"),
            EnableDnsHostnames: pulumi.Bool(true),
            EnableDnsSupport:   pulumi.Bool(true),
            Tags: pulumi.StringMap{
                "Name":      pulumi.String("main-vpc"),
                "ManagedBy": pulumi.String("pulumi"),
            },
        })
        if err != nil {
            return err
        }

        // Create subnet
        subnet, err := ec2.NewSubnet(ctx, "private-subnet", &ec2.SubnetArgs{
            VpcId:            vpc.ID(),
            CidrBlock:        pulumi.String("10.0.1.0/24"),
            AvailabilityZone: pulumi.String("us-east-1a"),
            Tags: pulumi.StringMap{
                "Name": pulumi.String("private-subnet-1a"),
            },
        })
        if err != nil {
            return err
        }

        // Export outputs
        ctx.Export("vpcId", vpc.ID())
        ctx.Export("subnetId", subnet.ID())

        return nil
    })
}
```

### Component Resources (Go)

```go
// vpc/vpc.go
package vpc

import (
    "fmt"

    "github.com/pulumi/pulumi-aws/sdk/v6/go/aws/ec2"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

type VpcArgs struct {
    CidrBlock          string
    AvailabilityZones  []string
    EnableNatGateway   bool
    Tags               map[string]string
}

type Vpc struct {
    pulumi.ResourceState

    VpcId            pulumi.StringOutput      `pulumi:"vpcId"`
    PublicSubnetIds  pulumi.StringArrayOutput `pulumi:"publicSubnetIds"`
    PrivateSubnetIds pulumi.StringArrayOutput `pulumi:"privateSubnetIds"`
}

func NewVpc(ctx *pulumi.Context, name string, args *VpcArgs, opts ...pulumi.ResourceOption) (*Vpc, error) {
    vpc := &Vpc{}
    err := ctx.RegisterComponentResource("custom:network:Vpc", name, vpc, opts...)
    if err != nil {
        return nil, err
    }

    // Create VPC
    awsVpc, err := ec2.NewVpc(ctx, fmt.Sprintf("%s-vpc", name), &ec2.VpcArgs{
        CidrBlock:          pulumi.String(args.CidrBlock),
        EnableDnsHostnames: pulumi.Bool(true),
        EnableDnsSupport:   pulumi.Bool(true),
        Tags:               pulumi.ToStringMap(args.Tags),
    }, pulumi.Parent(vpc))
    if err != nil {
        return nil, err
    }

    vpc.VpcId = awsVpc.ID().ToStringOutput()

    // Create Internet Gateway
    igw, err := ec2.NewInternetGateway(ctx, fmt.Sprintf("%s-igw", name), &ec2.InternetGatewayArgs{
        VpcId: awsVpc.ID(),
        Tags: pulumi.StringMap{
            "Name": pulumi.String(fmt.Sprintf("%s-igw", name)),
        },
    }, pulumi.Parent(vpc))
    if err != nil {
        return nil, err
    }

    // Create public subnets
    publicSubnetIds := pulumi.StringArray{}
    for i, az := range args.AvailabilityZones {
        subnet, err := ec2.NewSubnet(ctx, fmt.Sprintf("%s-public-%d", name, i), &ec2.SubnetArgs{
            VpcId:               awsVpc.ID(),
            CidrBlock:           pulumi.String(fmt.Sprintf("10.0.%d.0/24", i)),
            AvailabilityZone:    pulumi.String(az),
            MapPublicIpOnLaunch: pulumi.Bool(true),
            Tags: pulumi.StringMap{
                "Name": pulumi.String(fmt.Sprintf("%s-public-%s", name, az)),
                "Type": pulumi.String("public"),
            },
        }, pulumi.Parent(vpc))
        if err != nil {
            return nil, err
        }
        publicSubnetIds = append(publicSubnetIds, subnet.ID().ToStringOutput())
    }
    vpc.PublicSubnetIds = publicSubnetIds.ToStringArrayOutput()

    // Create private subnets
    privateSubnetIds := pulumi.StringArray{}
    for i, az := range args.AvailabilityZones {
        subnet, err := ec2.NewSubnet(ctx, fmt.Sprintf("%s-private-%d", name, i), &ec2.SubnetArgs{
            VpcId:            awsVpc.ID(),
            CidrBlock:        pulumi.String(fmt.Sprintf("10.0.%d.0/24", i+10)),
            AvailabilityZone: pulumi.String(az),
            Tags: pulumi.StringMap{
                "Name": pulumi.String(fmt.Sprintf("%s-private-%s", name, az)),
                "Type": pulumi.String("private"),
            },
        }, pulumi.Parent(vpc))
        if err != nil {
            return nil, err
        }
        privateSubnetIds = append(privateSubnetIds, subnet.ID().ToStringOutput())
    }
    vpc.PrivateSubnetIds = privateSubnetIds.ToStringArrayOutput()

    return vpc, nil
}
```

---

## Stack References

### Cross-Stack References (TypeScript)

```typescript
// infrastructure/networking/index.ts
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const vpc = new aws.ec2.Vpc("main", { cidrBlock: "10.0.0.0/16" });

export const vpcId = vpc.id;
export const vpcCidr = vpc.cidrBlock;
```

```typescript
// infrastructure/compute/index.ts
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// Reference networking stack
const networkingStack = new pulumi.StackReference("organization/networking/prod");
const vpcId = networkingStack.getOutput("vpcId");

const instance = new aws.ec2.Instance("app", {
  ami: "ami-12345678",
  instanceType: "t3.micro",
  subnetId: networkingStack.getOutput("privateSubnetIds").apply(ids => ids[0]),
});
```

---

## Configuration Management

### Stack Configuration (TypeScript)

```yaml
# Pulumi.prod.yaml
config:
  aws:region: us-east-1
  infrastructure:vpcCidr: "10.0.0.0/16"
  infrastructure:instanceType: "t3.large"
  infrastructure:enableBastion: true
```

```typescript
// index.ts
import * as pulumi from "@pulumi/pulumi";

const config = new pulumi.Config();
const vpcCidr = config.require("vpcCidr");
const instanceType = config.get("instanceType") || "t3.micro";
const enableBastion = config.getBoolean("enableBastion") ?? false;
```

---

## Secrets Management

```typescript
// Set secret
// pulumi config set --secret dbPassword P@ssw0rd!

const config = new pulumi.Config();
const dbPassword = config.requireSecret("dbPassword");

const db = new aws.rds.Instance("database", {
  password: dbPassword,
  // ...
});
```

---

## Testing Patterns

### Unit Tests (TypeScript)

```typescript
// tests/infrastructure.test.ts
import * as pulumi from "@pulumi/pulumi";

pulumi.runtime.setMocks({
  newResource: function(args: pulumi.runtime.MockResourceArgs): {id: string, state: any} {
    return {
      id: args.inputs.name + "_id",
      state: args.inputs,
    };
  },
  call: function(args: pulumi.runtime.MockCallArgs) {
    return args.inputs;
  },
});

describe("Infrastructure", () => {
  let vpcId: pulumi.Output<string>;

  before(async () => {
    const infra = await import("../index");
    vpcId = infra.vpcId;
  });

  it("VPC must have a valid ID", (done) => {
    pulumi.all([vpcId]).apply(([id]) => {
      expect(id).to.contain("vpc");
      done();
    });
  });
});
```

---

## Automation API

```typescript
// automation-api-example.ts
import * as pulumi from "@pulumi/pulumi/automation";

async function deployInfrastructure() {
  const stackName = "dev";
  const projectName = "my-infrastructure";

  // Create or select stack
  const stack = await pulumi.LocalWorkspace.createOrSelectStack({
    stackName,
    projectName,
    program: async () => {
      // Inline Pulumi program
      const vpc = new aws.ec2.Vpc("main", { cidrBlock: "10.0.0.0/16" });
      return { vpcId: vpc.id };
    },
  });

  // Set configuration
  await stack.setConfig("aws:region", { value: "us-east-1" });

  // Run pulumi up
  const upResult = await stack.up({ onOutput: console.log });
  console.log(`VPC ID: ${upResult.outputs.vpcId.value}`);
}

deployInfrastructure();
```

---

## Best Practices

**TypeScript:**
- ✅ Use strict TypeScript (`strict: true` in tsconfig.json)
- ✅ Leverage IDE IntelliSense
- ✅ Create component resources for reusability
- ✅ Use `apply()` for output transformations

**Python:**
- ✅ Use type hints for clarity
- ✅ Follow PEP 8 style guide
- ✅ Use virtual environments
- ✅ Create component resources as classes

**Go:**
- ✅ Handle all errors explicitly
- ✅ Use Go modules for dependencies
- ✅ Follow Go naming conventions
- ✅ Leverage strong typing

**All Languages:**
- ✅ Use stack references for cross-stack dependencies
- ✅ Store secrets in Pulumi config (encrypted)
- ✅ Write unit tests for infrastructure
- ✅ Use component resources for composition

---

See SKILL.md for links to other IaC topics including Terraform patterns, state management, and testing strategies.
