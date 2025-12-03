# Pulumi AWS ECS Fargate Example

Complete example deploying a containerized application to AWS ECS Fargate with Pulumi.

## Prerequisites

- AWS account with credentials configured
- Pulumi CLI installed (`brew install pulumi`)
- Node.js 18+ installed
- Docker (for building container images)

## Project Structure

```
pulumi-aws/
├── index.ts           # Main Pulumi program
├── package.json       # Dependencies
├── tsconfig.json      # TypeScript config
├── Pulumi.yaml        # Project metadata
├── Pulumi.dev.yaml    # Dev stack config
└── Pulumi.prod.yaml   # Production stack config
```

## Setup

1. **Install dependencies**:
```bash
npm install
```

2. **Configure AWS credentials**:
```bash
aws configure
```

3. **Initialize Pulumi stack**:
```bash
# Development
pulumi stack init dev
pulumi config set aws:region us-east-1
pulumi config set imageTag v1.0.0
pulumi config set --secret dbPassword mySecurePassword

# Production
pulumi stack init production
pulumi config set aws:region us-east-1
pulumi config set imageTag v1.0.0
pulumi config set --secret dbPassword productionPassword
```

## Deployment

1. **Preview changes**:
```bash
pulumi preview
```

2. **Deploy infrastructure**:
```bash
pulumi up
```

3. **Get outputs**:
```bash
pulumi stack output url
# Output: http://app-alb-1234567.us-east-1.elb.amazonaws.com
```

## What Gets Deployed

- **VPC**: 2 availability zones, public/private subnets, NAT gateway
- **ECS Cluster**: Fargate-based container orchestration
- **Application Load Balancer**: HTTP traffic distribution
- **Fargate Service**: 2 container replicas, auto-scaling enabled
- **CloudWatch Logs**: Container logging
- **IAM Roles**: Task execution and task roles

## Customization

Edit `index.ts` to customize:
- Container image repository
- CPU/memory allocation (default: 512 CPU, 1024 memory)
- Desired task count (default: 2)
- Environment variables
- Secrets (from AWS Secrets Manager)

## Cost Estimate

**Development** (~$20-30/month):
- NAT Gateway: ~$32/month
- Fargate tasks (2 x t3.micro equivalent): ~$15/month
- ALB: ~$20/month
- **Total**: ~$67/month

**Production** (~$100-150/month):
- NAT Gateway: ~$32/month
- Fargate tasks (3 x t3.small equivalent): ~$50/month
- ALB: ~$20/month
- **Total**: ~$102/month

## Cleanup

```bash
pulumi destroy
```

## Troubleshooting

**Task fails to start**:
```bash
# Check task logs
aws ecs describe-tasks --cluster <cluster-name> --tasks <task-id>

# View CloudWatch logs
aws logs tail /ecs/app-service --follow
```

**ALB returns 502/503**:
- Verify container health check endpoint
- Check security group rules
- Ensure container port matches ALB target group

## Next Steps

- Add CloudFront for CDN
- Configure custom domain with Route 53
- Set up auto-scaling policies
- Add RDS database
- Implement blue-green deployment
