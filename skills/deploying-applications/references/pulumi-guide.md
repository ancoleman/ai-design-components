# Pulumi Infrastructure as Code Guide

TypeScript-first Infrastructure as Code with Pulumi.

**Context7 Research**:
- Library: `/pulumi/docs` (Trust: 94.6/100, 9,525 snippets)
- Website: `/websites/pulumi` (86.4 score, 6,034 snippets)

## Table of Contents

- [Core Concepts](#core-concepts)
- [Project Structure](#project-structure)
- [AWS Patterns](#aws-patterns)
- [GCP Patterns](#gcp-patterns)
- [Multi-Cloud Patterns](#multi-cloud-patterns)
- [Component Model](#component-model)
- [Best Practices](#best-practices)

## Core Concepts

### Resources

Infrastructure components (EC2, S3, Lambda, etc.).

```typescript
import * as aws from "@pulumi/aws";

// Create S3 bucket (resource)
const bucket = new aws.s3.Bucket("my-bucket", {
    acl: "private",
    tags: {
        Environment: "production",
    },
});

// Export bucket name
export const bucketName = bucket.id;
```

### Stacks

Isolated environments (dev, staging, production).

```typescript
import * as pulumi from "@pulumi/pulumi";

const config = new pulumi.Config();
const environment = config.require("environment");

// Stack-specific configuration
const instanceType = environment === "production" ? "t3.large" : "t3.micro";
```

### Outputs

Values available after deployment.

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const bucket = new aws.s3.Bucket("bucket");

// Simple export
export const bucketName = bucket.id;

// Interpolated output
export const bucketUrl = pulumi.interpolate`https://${bucket.bucketDomainName}`;
```

### Configuration

Stack-specific values (secrets, environment variables).

```yaml
# Pulumi.dev.yaml
config:
  aws:region: us-east-1
  myapp:dbSize: small
  myapp:dbPassword:
    secure: AAABAQCc...  # Encrypted secret

# Pulumi.prod.yaml
config:
  aws:region: us-east-1
  myapp:dbSize: large
  myapp:dbPassword:
    secure: AAABAQD...
```

**Access in Code**:
```typescript
import * as pulumi from "@pulumi/pulumi";

const config = new pulumi.Config();
const dbSize = config.require("dbSize");
const dbPassword = config.requireSecret("dbPassword");
```

## Project Structure

### Basic Structure

```
my-infrastructure/
├── index.ts                 # Main entry point
├── Pulumi.yaml              # Project metadata
├── Pulumi.dev.yaml          # Dev stack config
├── Pulumi.staging.yaml      # Staging stack config
├── Pulumi.production.yaml   # Production stack config
├── package.json
├── tsconfig.json
└── node_modules/
```

### Component-Based Structure

```
my-infrastructure/
├── index.ts                 # Stack definition
├── components/
│   ├── WebService.ts        # Reusable web service
│   ├── Database.ts          # Database component
│   └── Network.ts           # VPC/networking
├── config/
│   ├── dev.ts               # Dev configuration
│   ├── staging.ts           # Staging configuration
│   └── production.ts        # Production configuration
└── Pulumi.yaml
```

### Pulumi.yaml

```yaml
name: my-infrastructure
runtime: nodejs
description: Production infrastructure for my application

# Optional: Template for new stacks
template:
  config:
    aws:region:
      description: AWS region
      default: us-east-1
    myapp:environment:
      description: Environment name
    myapp:dbSize:
      description: Database instance size
      default: small
```

## AWS Patterns

### ECS Fargate Service

Complete serverless container deployment.

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

const config = new pulumi.Config();
const imageTag = config.require("imageTag");
const dbUrl = config.requireSecret("dbUrl");

// VPC with public/private subnets
const vpc = new awsx.ec2.Vpc("app-vpc", {
    numberOfAvailabilityZones: 2,
    natGateways: { strategy: "Single" },
});

// ECS Cluster
const cluster = new aws.ecs.Cluster("app-cluster", {
    tags: { Environment: "production" },
});

// Application Load Balancer
const alb = new awsx.lb.ApplicationLoadBalancer("app-alb", {
    subnetIds: vpc.publicSubnetIds,
});

// Fargate Service
const service = new awsx.ecs.FargateService("app-service", {
    cluster: cluster.arn,
    assignPublicIp: false,
    taskDefinitionArgs: {
        container: {
            image: `my-repo:${imageTag}`,
            cpu: 512,
            memory: 1024,
            essential: true,
            environment: [
                { name: "NODE_ENV", value: "production" },
            ],
            secrets: [
                {
                    name: "DATABASE_URL",
                    valueFrom: dbUrl,
                },
            ],
            portMappings: [{
                containerPort: 3000,
                targetGroup: alb.defaultTargetGroup,
            }],
        },
    },
    desiredCount: 2,
});

export const url = pulumi.interpolate`http://${alb.loadBalancer.dnsName}`;
```

### Lambda Function with API Gateway

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// IAM role for Lambda
const role = new aws.iam.Role("lambda-role", {
    assumeRolePolicy: JSON.stringify({
        Version: "2012-10-17",
        Statement: [{
            Action: "sts:AssumeRole",
            Effect: "Allow",
            Principal: { Service: "lambda.amazonaws.com" },
        }],
    }),
});

// Attach basic execution policy
new aws.iam.RolePolicyAttachment("lambda-policy", {
    role: role.name,
    policyArn: "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
});

// Lambda function
const lambda = new aws.lambda.Function("api", {
    runtime: "nodejs20.x",
    handler: "index.handler",
    role: role.arn,
    code: new pulumi.asset.FileArchive("./dist"),
    environment: {
        variables: {
            NODE_ENV: "production",
        },
    },
    timeout: 30,
    memorySize: 512,
});

// API Gateway
const api = new aws.apigatewayv2.Api("api", {
    protocolType: "HTTP",
});

const integration = new aws.apigatewayv2.Integration("api-integration", {
    apiId: api.id,
    integrationType: "AWS_PROXY",
    integrationUri: lambda.arn,
    payloadFormatVersion: "2.0",
});

const route = new aws.apigatewayv2.Route("api-route", {
    apiId: api.id,
    routeKey: "$default",
    target: pulumi.interpolate`integrations/${integration.id}`,
});

const stage = new aws.apigatewayv2.Stage("api-stage", {
    apiId: api.id,
    name: "$default",
    autoDeploy: true,
});

// Grant API Gateway permission to invoke Lambda
new aws.lambda.Permission("api-permission", {
    action: "lambda:InvokeFunction",
    function: lambda.name,
    principal: "apigateway.amazonaws.com",
    sourceArn: pulumi.interpolate`${api.executionArn}/*`,
});

export const apiUrl = pulumi.interpolate`${api.apiEndpoint}`;
```

### S3 + CloudFront (Static Website)

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// S3 bucket for static files
const bucket = new aws.s3.Bucket("website-bucket", {
    website: {
        indexDocument: "index.html",
        errorDocument: "index.html", // SPA routing
    },
});

// Bucket policy for CloudFront
const bucketPolicy = new aws.s3.BucketPolicy("bucket-policy", {
    bucket: bucket.id,
    policy: bucket.arn.apply(arn => JSON.stringify({
        Version: "2012-10-17",
        Statement: [{
            Effect: "Allow",
            Principal: "*",
            Action: "s3:GetObject",
            Resource: `${arn}/*`,
        }],
    })),
});

// CloudFront Origin Access Identity
const oai = new aws.cloudfront.OriginAccessIdentity("oai", {
    comment: "OAI for static website",
});

// CloudFront distribution
const cdn = new aws.cloudfront.Distribution("cdn", {
    enabled: true,
    defaultRootObject: "index.html",
    origins: [{
        originId: bucket.id,
        domainName: bucket.bucketRegionalDomainName,
        s3OriginConfig: {
            originAccessIdentity: oai.cloudfrontAccessIdentityPath,
        },
    }],
    defaultCacheBehavior: {
        targetOriginId: bucket.id,
        viewerProtocolPolicy: "redirect-to-https",
        allowedMethods: ["GET", "HEAD", "OPTIONS"],
        cachedMethods: ["GET", "HEAD"],
        forwardedValues: {
            queryString: false,
            cookies: { forward: "none" },
        },
        compress: true,
        minTtl: 0,
        defaultTtl: 3600,
        maxTtl: 86400,
    },
    restrictions: {
        geoRestriction: {
            restrictionType: "none",
        },
    },
    viewerCertificate: {
        cloudfrontDefaultCertificate: true,
    },
    customErrorResponses: [
        {
            errorCode: 404,
            responseCode: 200,
            responsePagePath: "/index.html", // SPA routing
        },
    ],
});

// Sync local files to S3
const indexHtml = new aws.s3.BucketObject("index.html", {
    bucket: bucket.id,
    source: new pulumi.asset.FileAsset("./dist/index.html"),
    contentType: "text/html",
    acl: "public-read",
});

export const cdnUrl = cdn.domainName;
export const bucketName = bucket.id;
```

## GCP Patterns

### Cloud Run Service

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as gcp from "@pulumi/gcp";

const config = new pulumi.Config();
const imageTag = config.require("imageTag");
const gcpProject = config.require("gcpProject");

// Cloud Run service
const service = new gcp.cloudrun.Service("api-service", {
    location: "us-central1",
    template: {
        spec: {
            containers: [{
                image: `gcr.io/${gcpProject}/api:${imageTag}`,
                ports: [{ containerPort: 8000 }],
                envs: [
                    { name: "ENV", value: "production" },
                ],
                resources: {
                    limits: {
                        memory: "1Gi",
                        cpu: "1000m",
                    },
                },
            }],
            containerConcurrency: 80,
        },
        metadata: {
            annotations: {
                "autoscaling.knative.dev/maxScale": "10",
                "autoscaling.knative.dev/minScale": "0", // Scale to zero
            },
        },
    },
    traffics: [{
        percent: 100,
        latestRevision: true,
    }],
});

// Allow public access
const iamPolicy = new gcp.cloudrun.IamMember("public-access", {
    service: service.name,
    location: service.location,
    role: "roles/run.invoker",
    member: "allUsers",
});

export const url = service.statuses[0].url;
```

### GKE Cluster

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as gcp from "@pulumi/gcp";

const cluster = new gcp.container.Cluster("gke-cluster", {
    location: "us-central1-a",
    removeDefaultNodePool: true,
    initialNodeCount: 1,
    releaseChannel: {
        channel: "REGULAR",
    },
    workloadIdentityConfig: {
        workloadPool: `${gcp.config.project}.svc.id.goog`,
    },
});

const nodePool = new gcp.container.NodePool("primary-nodes", {
    location: cluster.location,
    cluster: cluster.name,
    nodeCount: 3,
    autoscaling: {
        minNodeCount: 1,
        maxNodeCount: 10,
    },
    nodeConfig: {
        machineType: "e2-medium",
        oauthScopes: [
            "https://www.googleapis.com/auth/cloud-platform",
        ],
        metadata: {
            "disable-legacy-endpoints": "true",
        },
    },
});

// Generate kubeconfig
export const kubeconfig = pulumi.all([
    cluster.name,
    cluster.endpoint,
    cluster.masterAuth,
]).apply(([name, endpoint, masterAuth]) => {
    const context = `gke_${gcp.config.project}_${cluster.location}_${name}`;
    return `apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: ${masterAuth.clusterCaCertificate}
    server: https://${endpoint}
  name: ${context}
contexts:
- context:
    cluster: ${context}
    user: ${context}
  name: ${context}
current-context: ${context}
kind: Config
preferences: {}
users:
- name: ${context}
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      command: gke-gcloud-auth-plugin
      installHint: Install gke-gcloud-auth-plugin
      provideClusterInfo: true
`;
});
```

## Multi-Cloud Patterns

### Multi-Region Deployment

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const regions = ["us-east-1", "eu-west-1", "ap-southeast-1"];

// Deploy Lambda to multiple regions
const lambdas = regions.map(region => {
    const provider = new aws.Provider(`provider-${region}`, { region });

    const lambda = new aws.lambda.Function(`api-${region}`, {
        runtime: "nodejs20.x",
        handler: "index.handler",
        role: role.arn,
        code: new pulumi.asset.FileArchive("./dist"),
    }, { provider });

    return { region, lambda };
});

export const lambdaUrls = lambdas.map(({ region, lambda }) => ({
    region,
    arn: lambda.arn,
}));
```

### AWS + Cloudflare

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as cloudflare from "@pulumi/cloudflare";

// AWS resources
const bucket = new aws.s3.Bucket("assets");

const cdn = new aws.cloudfront.Distribution("cdn", {
    // ... CloudFront config
});

// Cloudflare DNS
const zone = cloudflare.getZoneOutput({
    name: "example.com",
});

const record = new cloudflare.Record("cdn-record", {
    zoneId: zone.id,
    name: "assets",
    type: "CNAME",
    value: cdn.domainName,
    proxied: true, // Cloudflare proxy
});

export const assetUrl = pulumi.interpolate`https://assets.example.com`;
```

## Component Model

### Reusable Component

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

interface WebServiceArgs {
    imageTag: string;
    environment: pulumi.Input<{ [key: string]: pulumi.Input<string> }>;
    cpu: number;
    memory: number;
    desiredCount: number;
}

export class WebService extends pulumi.ComponentResource {
    public readonly url: pulumi.Output<string>;
    public readonly cluster: aws.ecs.Cluster;

    constructor(name: string, args: WebServiceArgs, opts?: pulumi.ComponentResourceOptions) {
        super("custom:WebService", name, {}, opts);

        // VPC
        const vpc = new awsx.ec2.Vpc(`${name}-vpc`, {
            numberOfAvailabilityZones: 2,
        }, { parent: this });

        // ECS Cluster
        this.cluster = new aws.ecs.Cluster(`${name}-cluster`, {
            tags: { ManagedBy: "Pulumi" },
        }, { parent: this });

        // ALB
        const alb = new awsx.lb.ApplicationLoadBalancer(`${name}-alb`, {
            subnetIds: vpc.publicSubnetIds,
        }, { parent: this });

        // Fargate Service
        const service = new awsx.ecs.FargateService(`${name}-service`, {
            cluster: this.cluster.arn,
            taskDefinitionArgs: {
                container: {
                    image: `my-repo:${args.imageTag}`,
                    cpu: args.cpu,
                    memory: args.memory,
                    environment: args.environment,
                    portMappings: [{
                        containerPort: 3000,
                        targetGroup: alb.defaultTargetGroup,
                    }],
                },
            },
            desiredCount: args.desiredCount,
        }, { parent: this });

        this.url = pulumi.interpolate`http://${alb.loadBalancer.dnsName}`;

        this.registerOutputs({
            url: this.url,
            cluster: this.cluster,
        });
    }
}
```

**Usage**:

```typescript
import { WebService } from "./components/WebService";

const webService = new WebService("my-app", {
    imageTag: "v1.2.3",
    environment: {
        NODE_ENV: "production",
    },
    cpu: 512,
    memory: 1024,
    desiredCount: 3,
});

export const appUrl = webService.url;
```

## Best Practices

### Stack Management

```bash
# Create new stack
pulumi stack init production

# Select stack
pulumi stack select staging

# List stacks
pulumi stack ls

# Stack configuration
pulumi config set aws:region us-east-1
pulumi config set --secret dbPassword mySecurePassword

# Preview changes
pulumi preview

# Deploy
pulumi up

# Destroy
pulumi destroy
```

### Secrets Management

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const dbPassword = config.requireSecret("dbPassword");

// Store secret in AWS Secrets Manager
const secret = new aws.secretsmanager.Secret("db-password");

const secretVersion = new aws.secretsmanager.SecretVersion("db-password-version", {
    secretId: secret.id,
    secretString: dbPassword,
});

// Use secret ARN in ECS task
const taskDefinition = new aws.ecs.TaskDefinition("task", {
    containerDefinitions: pulumi.jsonStringify([{
        name: "app",
        image: "my-app:latest",
        secrets: [{
            name: "DATABASE_PASSWORD",
            valueFrom: secretVersion.arn,
        }],
    }]),
});
```

### Tagging Strategy

```typescript
import * as pulumi from "@pulumi/pulumi";

const config = new pulumi.Config();
const environment = config.require("environment");

const tags = {
    Environment: environment,
    ManagedBy: "Pulumi",
    Project: pulumi.getProject(),
    Stack: pulumi.getStack(),
};

// Apply to all resources
const bucket = new aws.s3.Bucket("bucket", {
    tags: tags,
});
```

### Import Existing Resources

```bash
# Import existing S3 bucket
pulumi import aws:s3/bucket:Bucket my-bucket my-existing-bucket-name

# Import existing EC2 instance
pulumi import aws:ec2/instance:Instance my-instance i-1234567890abcdef0
```

### Testing (Policy as Code)

```typescript
import * as policy from "@pulumi/policy";

const policies = new policy.PolicyPack("aws-policies", {
    policies: [
        {
            name: "s3-no-public-read",
            description: "Prohibits public read access on S3 buckets",
            enforcementLevel: "mandatory",
            validateResource: policy.validateResourceOfType(aws.s3.Bucket, (bucket, args, reportViolation) => {
                if (bucket.acl === "public-read") {
                    reportViolation("S3 buckets cannot have public-read ACL");
                }
            }),
        },
    ],
});
```
