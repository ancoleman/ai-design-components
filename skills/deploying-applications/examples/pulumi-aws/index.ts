import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

const config = new pulumi.Config();
const imageTag = config.require("imageTag");
const dbPassword = config.requireSecret("dbPassword");

// VPC with public/private subnets across 2 AZs
const vpc = new awsx.ec2.Vpc("app-vpc", {
    numberOfAvailabilityZones: 2,
    natGateways: { strategy: "Single" }, // Cost optimization: 1 NAT gateway
    tags: {
        Name: "app-vpc",
        Environment: pulumi.getStack(),
        ManagedBy: "Pulumi",
    },
});

// ECS Cluster
const cluster = new aws.ecs.Cluster("app-cluster", {
    tags: {
        Environment: pulumi.getStack(),
        ManagedBy: "Pulumi",
    },
});

// CloudWatch Log Group
const logGroup = new aws.cloudwatch.LogGroup("app-logs", {
    retentionInDays: 7,
});

// Application Load Balancer
const alb = new awsx.lb.ApplicationLoadBalancer("app-alb", {
    subnetIds: vpc.publicSubnetIds,
    defaultTargetGroup: {
        port: 3000,
        protocol: "HTTP",
        healthCheck: {
            path: "/health",
            interval: 30,
            timeout: 5,
            healthyThreshold: 2,
            unhealthyThreshold: 3,
        },
    },
});

// Fargate Task Execution Role
const executionRole = new aws.iam.Role("task-execution-role", {
    assumeRolePolicy: JSON.stringify({
        Version: "2012-10-17",
        Statement: [{
            Action: "sts:AssumeRole",
            Effect: "Allow",
            Principal: {
                Service: "ecs-tasks.amazonaws.com",
            },
        }],
    }),
});

new aws.iam.RolePolicyAttachment("task-execution-policy", {
    role: executionRole.name,
    policyArn: "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
});

// Fargate Task Role (for application permissions)
const taskRole = new aws.iam.Role("task-role", {
    assumeRolePolicy: JSON.stringify({
        Version: "2012-10-17",
        Statement: [{
            Action: "sts:AssumeRole",
            Effect: "Allow",
            Principal: {
                Service: "ecs-tasks.amazonaws.com",
            },
        }],
    }),
});

// Fargate Service
const service = new awsx.ecs.FargateService("app-service", {
    cluster: cluster.arn,
    assignPublicIp: false, // Use private subnets
    desiredCount: 2,
    taskDefinitionArgs: {
        executionRole: {
            roleArn: executionRole.arn,
        },
        taskRole: {
            roleArn: taskRole.arn,
        },
        container: {
            name: "app",
            image: `my-repo:${imageTag}`, // Replace with your ECR repository
            cpu: 512,
            memory: 1024,
            essential: true,
            portMappings: [{
                containerPort: 3000,
                targetGroup: alb.defaultTargetGroup,
            }],
            environment: [
                {
                    name: "NODE_ENV",
                    value: pulumi.getStack() === "production" ? "production" : "development",
                },
                {
                    name: "PORT",
                    value: "3000",
                },
            ],
            secrets: [
                {
                    name: "DATABASE_PASSWORD",
                    valueFrom: dbPassword,
                },
            ],
            logConfiguration: {
                logDriver: "awslogs",
                options: {
                    "awslogs-group": logGroup.name,
                    "awslogs-region": aws.config.region!,
                    "awslogs-stream-prefix": "app",
                },
            },
            healthCheck: {
                command: ["CMD-SHELL", "curl -f http://localhost:3000/health || exit 1"],
                interval: 30,
                timeout: 5,
                retries: 3,
                startPeriod: 60,
            },
        },
    },
});

// Auto Scaling
const scalingTarget = new aws.appautoscaling.Target("app-scaling-target", {
    maxCapacity: 10,
    minCapacity: 2,
    resourceId: pulumi.interpolate`service/${cluster.name}/${service.service.name}`,
    scalableDimension: "ecs:service:DesiredCount",
    serviceNamespace: "ecs",
});

const cpuScalingPolicy = new aws.appautoscaling.Policy("cpu-scaling-policy", {
    policyType: "TargetTrackingScaling",
    resourceId: scalingTarget.resourceId,
    scalableDimension: scalingTarget.scalableDimension,
    serviceNamespace: scalingTarget.serviceNamespace,
    targetTrackingScalingPolicyConfiguration: {
        targetValue: 70,
        predefinedMetricSpecification: {
            predefinedMetricType: "ECSServiceAverageCPUUtilization",
        },
        scaleInCooldown: 300,
        scaleOutCooldown: 60,
    },
});

// Exports
export const vpcId = vpc.vpcId;
export const clusterName = cluster.name;
export const url = pulumi.interpolate`http://${alb.loadBalancer.dnsName}`;
export const logGroupName = logGroup.name;
export const serviceName = service.service.name;
