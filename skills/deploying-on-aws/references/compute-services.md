# AWS Compute Services - Deep Dive

## Table of Contents

1. [Lambda (Serverless Functions)](#lambda-serverless-functions)
2. [Fargate (Serverless Containers)](#fargate-serverless-containers)
3. [ECS (Elastic Container Service)](#ecs-elastic-container-service)
4. [EKS (Elastic Kubernetes Service)](#eks-elastic-kubernetes-service)
5. [EC2 (Virtual Machines)](#ec2-virtual-machines)
6. [Service Comparison Matrix](#service-comparison-matrix)
7. [Migration Paths](#migration-paths)

---

## Lambda (Serverless Functions)

### Overview

AWS Lambda runs code without provisioning servers. Pay only for compute time consumed. Supports multiple languages and automatic scaling.

### Key Specifications (2025)

- **Execution Time:** 1ms to 15 minutes maximum
- **Memory:** 128MB to 10,240MB (increments of 1MB)
- **Storage:** 512MB to 10GB ephemeral storage (/tmp)
- **Deployment Package:** 50MB zipped, 250MB unzipped
- **Concurrent Executions:** 1,000 default (can increase via quota)
- **Supported Runtimes:** Node.js, Python, Java, Go, .NET, Ruby, Custom (containers)

### Performance Features (2025)

**Lambda SnapStart (Java):**
- Near-instant cold starts for Java functions
- Caches initialized execution environment
- 10x faster startup vs. traditional Java

**Lambda Response Streaming:**
- Stream responses up to 20MB
- Progressive results for large payloads
- Ideal for generative AI, video processing

**Provisioned Concurrency:**
- Pre-initialized execution environments
- Sub-10ms cold starts
- Predictable performance for latency-sensitive apps

### Cost Model

**Request Pricing:**
- Free tier: 1M requests/month (perpetual)
- $0.20 per 1M requests thereafter

**Compute Pricing (us-east-1):**
- $0.0000166667 per GB-second
- Free tier: 400,000 GB-seconds/month

**Example Calculations:**

```
Scenario: API with 5M requests/month, 512MB memory, 200ms avg execution

Requests: (5M - 1M free) × $0.20/1M = $0.80
Compute: 5M × 0.2s × 0.5GB × $0.0000166667 = $8.33
Total: $9.13/month
```

### Use Cases

**Ideal:**
- API backends (via API Gateway)
- File processing (S3 triggers)
- Scheduled jobs (EventBridge cron)
- Stream processing (Kinesis, DynamoDB Streams)
- WebHooks and event handlers

**Avoid:**
- Long-running tasks (>15 minutes)
- Stateful applications
- Predictable high throughput (EC2 cheaper at scale)
- Large deployment packages (>250MB)

### Best Practices

1. **Optimize Memory Allocation:**
   - CPU scales with memory (1,769MB = 1 vCPU)
   - Test different memory sizes (more memory = faster execution = lower cost)
   - Use AWS Lambda Power Tuning tool

2. **Reduce Cold Starts:**
   - Minimize dependencies
   - Use SnapStart for Java
   - Provision concurrency for critical functions
   - Keep functions warm with scheduled pings (if cost-effective)

3. **Environment Variables:**
   - Use for configuration (no code changes)
   - Encrypt sensitive values with KMS
   - Consider Parameter Store or Secrets Manager for secrets

4. **Observability:**
   - Enable X-Ray tracing
   - Use structured logging (JSON)
   - Create CloudWatch dashboards
   - Set up alarms for errors and throttling

---

## Fargate (Serverless Containers)

### Overview

AWS Fargate runs containers without managing servers. Pay for vCPU and memory used. Works with ECS and EKS.

### Key Specifications

**CPU Options:**
- 0.25 vCPU to 16 vCPU
- Must match valid CPU/memory combinations

**Memory Options:**
- 0.5GB to 120GB
- Scales with CPU selection

**Platform Versions:**
- **1.4.0:** Current default, supports EFS, container insights
- **1.3.0:** Legacy, missing some features

### Cost Model (Linux, us-east-1)

**Per vCPU-hour:** $0.04048
**Per GB-hour:** $0.004445

**Example Configurations:**

| vCPU | Memory | Hourly | Monthly (24/7) |
|------|--------|--------|----------------|
| 0.25 | 0.5GB | $0.01 | $7.50 |
| 0.5 | 1GB | $0.02 | $15.00 |
| 1 | 2GB | $0.05 | $35.00 |
| 2 | 4GB | $0.10 | $70.00 |
| 4 | 8GB | $0.20 | $140.00 |

**Fargate Spot:**
- 70% discount vs. on-demand Fargate
- Can be interrupted with 2-minute notice
- Ideal for fault-tolerant batch jobs

### Use Cases

**Ideal:**
- Containerized microservices
- Batch processing (with Fargate Spot)
- CI/CD build agents
- Variable traffic applications
- Multi-hour running tasks

**Avoid:**
- Extremely cost-sensitive at high scale (EC2 cheaper)
- GPU workloads (use EC2)
- Stateful apps requiring persistent local storage
- High-performance computing

### Best Practices

1. **Task Sizing:**
   - Start small, monitor CloudWatch Container Insights
   - Scale up based on actual utilization
   - Use Application Auto Scaling

2. **Networking:**
   - Use awsvpc network mode (required)
   - Each task gets ENI with private IP
   - Use Security Groups for network isolation

3. **Storage:**
   - Ephemeral storage: 20GB default (can increase to 200GB)
   - Persistent storage: Mount EFS volumes
   - Logs: Send to CloudWatch Logs

---

## ECS (Elastic Container Service)

### Overview

AWS-native container orchestration. Simpler than Kubernetes. Tight integration with AWS services.

### Launch Types

**Fargate:**
- Serverless, no EC2 management
- Pay per task

**EC2:**
- Manage EC2 instances
- Lower cost at scale
- More control

**External:**
- Run on on-premises servers
- ECS Anywhere

### Key Features (2025)

**ECS Service Connect:**
- Built-in service mesh
- Service discovery without custom code
- Load balancing and circuit breaking

**ECS Exec:**
- Interactive shell access to containers
- Debugging without SSH

**Capacity Providers:**
- Auto-scale between Fargate and EC2
- Mix spot and on-demand instances

### Cost Model

**No ECS Control Plane Fees:**
- Only pay for underlying compute (Fargate or EC2)

**Example (10 services, t3.medium EC2):**
- EC2: 10 × $30/month = $300
- ECS: $0
- **Total: $300/month**

### Use Cases

**Ideal:**
- Docker-based applications
- AWS-native deployments
- Simpler than Kubernetes requirements
- Tight ALB/CloudWatch/IAM integration

**Avoid:**
- Multi-cloud portability needed (use EKS)
- Team has Kubernetes expertise
- Need Kubernetes ecosystem (Helm, Operators)

---

## EKS (Elastic Kubernetes Service)

### Overview

Managed Kubernetes control plane. Full Kubernetes compatibility. Multi-cloud/hybrid portability.

### Key Specifications

**Control Plane:**
- Highly available across 3 AZs
- Automatic version upgrades
- Integrated with AWS IAM

**Supported Versions:**
- Kubernetes 1.25 to 1.28 (as of 2025)
- Automatic minor version upgrades available

### Key Features (2025)

**EKS Auto Mode:**
- Fully managed node lifecycle
- Automatic capacity provisioning
- No manual node group management

**EKS Pod Identities:**
- Simplified IAM for pods
- Replaces IRSA (IAM Roles for Service Accounts)
- Easier setup and debugging

**EKS Hybrid Nodes:**
- Run Kubernetes nodes on-premises
- Consistent management plane

### Cost Model

**Control Plane:** $0.10/hour = $73/month per cluster

**Worker Nodes:**
- Fargate: Per-task pricing
- EC2: Instance pricing
- On-Demand, Reserved, or Spot

**Example (3 m5.large nodes on-demand):**
- Control plane: $73/month
- Nodes: 3 × $70 = $210/month
- **Total: $283/month**

### Use Cases

**Ideal:**
- Kubernetes expertise exists
- Multi-cloud/hybrid strategy
- Complex orchestration needs
- Kubernetes ecosystem required (Helm, Operators, Istio)

**Avoid:**
- Team lacks Kubernetes knowledge
- Simple workloads (over-engineering)
- Cost-sensitive (ECS cheaper)

### Best Practices

1. **Node Groups:**
   - Use managed node groups
   - Mix on-demand (baseline) + spot (burst)
   - Use Auto Mode for simplicity

2. **Networking:**
   - Use AWS VPC CNI plugin
   - Enable Pod Security Groups
   - Use Network Policies for isolation

3. **Storage:**
   - Use EBS CSI Driver for persistent volumes
   - Use EFS CSI Driver for shared storage
   - Implement StorageClasses for automation

---

## EC2 (Virtual Machines)

### Overview

Virtual servers in the cloud. Full OS control. Widest instance type selection.

### Instance Families

**General Purpose (T, M):**
- Balanced CPU, memory, network
- t3: Burstable, cost-effective
- m5: Consistent performance

**Compute Optimized (C):**
- High CPU-to-memory ratio
- Batch processing, HPC, gaming

**Memory Optimized (R, X):**
- High memory-to-CPU ratio
- Databases, caches, in-memory analytics

**Storage Optimized (I, D):**
- High IOPS, throughput
- NoSQL databases, data warehousing

**Accelerated Computing (P, G, Inf):**
- GPU, FPGA, inference
- ML training, rendering, genomics

### Pricing Models

**On-Demand:**
- Pay by the second
- No commitment
- Highest cost

**Reserved Instances:**
- 1-year or 3-year commitment
- 30-60% savings
- Predictable workloads

**Savings Plans:**
- 1-year or 3-year commitment
- Flexible across instance families
- 30-40% savings

**Spot Instances:**
- Bid on spare capacity
- 60-90% savings
- Can be interrupted with 2-minute notice

### Cost Examples (us-east-1, On-Demand)

| Instance | vCPU | Memory | Hourly | Monthly | Use Case |
|----------|------|--------|--------|---------|----------|
| t3.micro | 2 | 1GB | $0.0104 | $7.60 | Dev/test |
| t3.medium | 2 | 4GB | $0.0416 | $30.37 | Small apps |
| m5.large | 2 | 8GB | $0.096 | $70.08 | General purpose |
| c5.xlarge | 4 | 8GB | $0.17 | $124.10 | Compute heavy |
| r5.large | 2 | 16GB | $0.126 | $91.98 | Memory heavy |

### Use Cases

**Ideal:**
- Maximum OS control
- GPU/FPGA workloads
- Windows Server
- BYOL licensing
- Predictable high traffic (with Reserved Instances)

**Avoid:**
- Variable traffic (use Lambda/Fargate)
- Minimal ops desired
- Serverless patterns applicable

---

## Service Comparison Matrix

| Criteria | Lambda | Fargate | ECS (EC2) | EKS | EC2 |
|----------|--------|---------|-----------|-----|-----|
| **Ops Overhead** | Minimal | Low | Medium | High | High |
| **Cost (variable)** | Excellent | Good | Fair | Fair | Poor |
| **Cost (predictable)** | Poor | Fair | Good | Good | Excellent |
| **Cold Start** | Yes | No | No | No | No |
| **Max Runtime** | 15 min | Unlimited | Unlimited | Unlimited | Unlimited |
| **Portability** | Low | Medium | Medium | High | High |
| **Scaling Speed** | Instant | Fast | Medium | Medium | Slow |
| **State Management** | None | Limited | Good | Excellent | Excellent |

---

## Migration Paths

### VM to Containers

```
EC2 → ECS on EC2 → ECS on Fargate → Serverless (Lambda)
```

**Step 1: EC2 → ECS on EC2**
- Containerize application (Dockerfile)
- Deploy to ECS with EC2 launch type
- Benefit: Better resource utilization

**Step 2: ECS on EC2 → ECS on Fargate**
- Migrate task definitions to Fargate
- Remove EC2 instance management
- Benefit: No server operations

**Step 3: ECS on Fargate → Lambda (if applicable)**
- Refactor to event-driven functions
- Use API Gateway for HTTP
- Benefit: Pay-per-request pricing

### Monolith to Microservices

```
Single EC2 → Multiple ECS Services → Lambda Functions
```

**Strategy:**
- Identify bounded contexts
- Extract services incrementally
- Use API Gateway or ALB for routing
- Implement service mesh (ECS Service Connect)

### On-Premises to AWS

```
On-Prem VMs → EC2 → Containers (ECS/EKS) → Serverless
```

**Tools:**
- AWS Application Migration Service (MGN)
- VM Import/Export
- Database Migration Service (DMS)
