/**
 * Pulumi TypeScript VPC Example
 *
 * Demonstrates: Component resource pattern with multi-AZ VPC
 *
 * Dependencies:
 * - npm install @pulumi/pulumi @pulumi/aws
 *
 * Usage:
 * - pulumi stack init dev
 * - pulumi config set aws:region us-east-1
 * - pulumi up
 */

import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

export interface VpcArgs {
  name: string;
  cidrBlock?: pulumi.Input<string>;
  availabilityZones: pulumi.Input<string>[];
  enableNatGateway?: pulumi.Input<boolean>;
  tags?: pulumi.Input<{ [key: string]: pulumi.Input<string> }>;
}

export class Vpc extends pulumi.ComponentResource {
  public readonly vpcId: pulumi.Output<string>;
  public readonly publicSubnetIds: pulumi.Output<string>[];
  public readonly privateSubnetIds: pulumi.Output<string>[];
  public readonly natGatewayIds: pulumi.Output<string>[];

  constructor(name: string, args: VpcArgs, opts?: pulumi.ComponentResourceOptions) {
    super("custom:network:Vpc", name, {}, opts);

    const cidr = args.cidrBlock ?? "10.0.0.0/16";
    const enableNat = args.enableNatGateway ?? true;

    // Create VPC
    const vpc = new aws.ec2.Vpc(
      `${name}-vpc`,
      {
        cidrBlock: cidr,
        enableDnsHostnames: true,
        enableDnsSupport: true,
        tags: pulumi.output(args.tags).apply(tags => ({
          ...tags,
          Name: `${args.name}-vpc`,
          ManagedBy: "pulumi",
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
        tags: { Name: `${args.name}-igw` },
      },
      { parent: this }
    );

    // Create public subnets
    const publicSubnets: aws.ec2.Subnet[] = [];
    this.publicSubnetIds = [];

    const azs = pulumi.output(args.availabilityZones);
    const subnetCount = azs.apply(a => a.length);

    // Use a promise to handle dynamic subnet creation
    const createPublicSubnets = azs.apply(zones => {
      const subnets = zones.map((az, i) => {
        const subnet = new aws.ec2.Subnet(
          `${name}-public-${i}`,
          {
            vpcId: vpc.id,
            cidrBlock: pulumi.interpolate`${cidr}`.apply(c => {
              // Calculate CIDR: 10.0.0.0/24, 10.0.1.0/24, etc.
              const parts = c.split(".");
              return `${parts[0]}.${parts[1]}.${i}.0/24`;
            }),
            availabilityZone: az,
            mapPublicIpOnLaunch: true,
            tags: {
              Name: `${args.name}-public-${az}`,
              Type: "public",
            },
          },
          { parent: this }
        );
        publicSubnets.push(subnet);
        return subnet.id;
      });
      return subnets;
    });

    this.publicSubnetIds = createPublicSubnets.apply(ids => ids);

    // Create private subnets
    const privateSubnets: aws.ec2.Subnet[] = [];
    this.privateSubnetIds = [];

    const createPrivateSubnets = azs.apply(zones => {
      const subnets = zones.map((az, i) => {
        const subnet = new aws.ec2.Subnet(
          `${name}-private-${i}`,
          {
            vpcId: vpc.id,
            cidrBlock: pulumi.interpolate`${cidr}`.apply(c => {
              // Calculate CIDR: 10.0.10.0/24, 10.0.11.0/24, etc.
              const parts = c.split(".");
              return `${parts[0]}.${parts[1]}.${i + 10}.0/24`;
            }),
            availabilityZone: az,
            tags: {
              Name: `${args.name}-private-${az}`,
              Type: "private",
            },
          },
          { parent: this }
        );
        privateSubnets.push(subnet);
        return subnet.id;
      });
      return subnets;
    });

    this.privateSubnetIds = createPrivateSubnets.apply(ids => ids);

    // Create NAT Gateways (optional)
    this.natGatewayIds = [];

    if (enableNat) {
      const createNatGateways = pulumi
        .all([azs, this.publicSubnetIds])
        .apply(([zones, pubSubnets]) => {
          return zones.map((az, i) => {
            const eip = new aws.ec2.Eip(
              `${name}-nat-eip-${i}`,
              {
                domain: "vpc",
                tags: { Name: `${args.name}-nat-eip-${az}` },
              },
              { parent: this, dependsOn: [igw] }
            );

            const natGw = new aws.ec2.NatGateway(
              `${name}-nat-${i}`,
              {
                allocationId: eip.id,
                subnetId: pubSubnets[i],
                tags: { Name: `${args.name}-nat-${az}` },
              },
              { parent: this, dependsOn: [igw] }
            );

            return natGw.id;
          });
        });

      this.natGatewayIds = createNatGateways.apply(ids => ids);
    }

    // Create public route table
    const publicRt = new aws.ec2.RouteTable(
      `${name}-public-rt`,
      {
        vpcId: vpc.id,
        routes: [
          {
            cidrBlock: "0.0.0.0/0",
            gatewayId: igw.id,
          },
        ],
        tags: { Name: `${args.name}-public-rt` },
      },
      { parent: this }
    );

    // Associate public subnets with public route table
    this.publicSubnetIds.apply(subnetIds => {
      subnetIds.forEach((subnetId, i) => {
        new aws.ec2.RouteTableAssociation(
          `${name}-public-rta-${i}`,
          {
            subnetId: subnetId,
            routeTableId: publicRt.id,
          },
          { parent: this }
        );
      });
    });

    // Create private route tables (one per AZ) and associate with NAT gateways
    if (enableNat) {
      pulumi.all([azs, this.privateSubnetIds, this.natGatewayIds]).apply(
        ([zones, privSubnets, natGws]) => {
          zones.forEach((az, i) => {
            const privateRt = new aws.ec2.RouteTable(
              `${name}-private-rt-${i}`,
              {
                vpcId: vpc.id,
                routes: [
                  {
                    cidrBlock: "0.0.0.0/0",
                    natGatewayId: natGws[i],
                  },
                ],
                tags: { Name: `${args.name}-private-rt-${az}` },
              },
              { parent: this }
            );

            new aws.ec2.RouteTableAssociation(
              `${name}-private-rta-${i}`,
              {
                subnetId: privSubnets[i],
                routeTableId: privateRt.id,
              },
              { parent: this }
            );
          });
        }
      );
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

// Example usage
const config = new pulumi.Config();
const environment = config.get("environment") || "dev";

// Create VPC
const vpc = new Vpc("example", {
  name: environment,
  cidrBlock: "10.0.0.0/16",
  availabilityZones: ["us-east-1a", "us-east-1b", "us-east-1c"],
  enableNatGateway: true,
  tags: {
    Environment: environment,
    Project: "pulumi-example",
  },
});

// Export outputs
export const vpcId = vpc.vpcId;
export const publicSubnetIds = vpc.publicSubnetIds;
export const privateSubnetIds = vpc.privateSubnetIds;
export const natGatewayIds = vpc.natGatewayIds;
