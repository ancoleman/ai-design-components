# AWS Patterns Skill - Master Plan

**Skill Name:** `aws-patterns`
**Skill Level:** Mid Level (5,000-8,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [AWS Service Taxonomy](#aws-service-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Implementation Patterns](#implementation-patterns)
7. [Well-Architected Framework](#well-architected-framework)
8. [Multi-Language Infrastructure as Code](#multi-language-infrastructure-as-code)
9. [Library Recommendations](#library-recommendations)
10. [Skill Structure Design](#skill-structure-design)
11. [Integration Points](#integration-points)
12. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

Amazon Web Services (AWS) remains the dominant cloud platform in 2025, with 32% market share and the most comprehensive service portfolio. Organizations choosing AWS benefit from the broadest feature set, deepest enterprise adoption, and most mature tooling ecosystem.

**Market Reality (2025):**
- **Market Leadership:** AWS maintains #1 position with $90B+ annual revenue
- **Service Breadth:** 200+ services vs. Azure (175+), GCP (150+)
- **Enterprise Adoption:** 90% of Fortune 500 use AWS for at least some workloads
- **Developer Ecosystem:** Largest community, most third-party integrations
- **Geographic Reach:** 32 regions, 102 availability zones worldwide

**Strategic Drivers:**
1. **Multi-Cloud Reality:** Most organizations use AWS + at least one other cloud
2. **Well-Architected Framework:** Industry-standard architectural guidance
3. **Serverless Leadership:** Lambda, API Gateway, EventBridge set the standard
4. **Enterprise Integration:** Deep integration with SAP, Oracle, Windows workloads
5. **Innovation Velocity:** Fastest feature release cadence (3,000+ launches/year)

### How This Differs from Existing Solutions

**Existing AWS Documentation:**
- **AWS Official Docs:** Comprehensive but service-focused, not pattern-focused
- **AWS Well-Architected:** Strategic guidance but lacks tactical implementation
- **AWS Workshops:** Hands-on but narrow scope (single service deep-dives)
- **Third-Party Courses:** Often outdated (missing 2024-2025 features)

**Our Approach:**
- **Decision-First Framework:** When to use each service combination
- **Cost-Aware Patterns:** FinOps integrated into every decision
- **2025 Best Practices:** Modern patterns (Lambda SnapStart, EventBridge Pipes, S3 Express)
- **Multi-IaC Support:** CloudFormation, CDK, Terraform examples
- **Migration Patterns:** On-prem → AWS, monolith → microservices
- **Security by Default:** Every pattern includes IAM, encryption, compliance considerations

### Target Audience

**Primary Users:**
- Cloud architects designing AWS solutions
- Backend developers deploying to AWS
- DevOps/SRE teams operating AWS infrastructure
- Platform engineers building AWS-based internal platforms

**Skill Level Assumptions:**
- Understands cloud computing fundamentals
- Familiar with basic AWS services (EC2, S3, IAM)
- Knows infrastructure-as-code concepts
- Needs guidance on service selection and architectural patterns

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **Service Selection Frameworks**
   - Compute: Lambda vs. Fargate vs. ECS vs. EKS vs. EC2
   - Storage: S3 vs. EBS vs. EFS vs. FSx
   - Database: RDS vs. DynamoDB vs. Aurora vs. DocumentDB vs. ElastiCache
   - Networking: VPC design, load balancing (ALB/NLB), CloudFront, Route53

2. **Architectural Patterns**
   - Serverless architectures (Lambda, API Gateway, EventBridge)
   - Container orchestration (ECS, EKS, Fargate)
   - Event-driven architectures (EventBridge, SNS, SQS)
   - Data processing pipelines (Kinesis, Glue, EMR)

3. **Security and Compliance**
   - IAM best practices (least privilege, roles, policies)
   - Encryption (KMS, at-rest, in-transit)
   - Secrets management (Secrets Manager, Parameter Store)
   - Network security (Security Groups, NACLs, WAF)

4. **Cost Optimization**
   - Right-sizing compute resources
   - Storage tier selection
   - Reserved instances and Savings Plans
   - Cost monitoring and budgets

5. **Operational Excellence**
   - Infrastructure as code (CDK, CloudFormation, Terraform)
   - Monitoring and logging (CloudWatch, X-Ray)
   - Deployment strategies (blue-green, canary)
   - Disaster recovery patterns

### What This Skill Does NOT Cover

**Out of Scope:**
- **Cloud Provider Comparison:** Not AWS vs. GCP vs. Azure (use multi-cloud skill)
- **AWS Certification Prep:** Not exam-focused content
- **Service Deep-Dives:** Detailed feature documentation (use AWS docs)
- **AI/ML Specifics:** SageMaker, Bedrock patterns (separate skill needed)
- **Account Setup:** Organization structure, billing setup (foundational topics)

### Success Criteria

**A user successfully uses this skill when they can:**
1. Choose the right AWS compute service for a given workload
2. Design VPC architecture for multi-tier applications
3. Select appropriate database service based on access patterns
4. Implement serverless patterns with Lambda and API Gateway
5. Apply AWS Well-Architected Framework principles
6. Use CDK or Terraform to define AWS infrastructure
7. Optimize costs while maintaining performance and reliability

---

## Research Findings

### Research Date: December 3, 2025

**Research Tools Used:**
- MCP tools unavailable (Google Search Grounding, Context7)
- Fallback to existing AWS knowledge base (November 2025)
- AWS re:Invent 2024 announcements
- AWS Well-Architected Framework (latest revision)

### Key AWS Trends for 2025

**1. Serverless Evolution**
- **Lambda SnapStart:** Near-instant cold starts for Java functions
- **Lambda Response Streaming:** Stream responses up to 20MB
- **EventBridge Pipes:** Simplified event processing (source → filter → enrichment → target)
- **Step Functions Distributed Map:** Process millions of items in parallel
- **Impact:** Serverless now viable for more workload types

**2. Storage Innovation**
- **S3 Express One Zone:** 10x faster S3 for low-latency workloads
- **EBS io2 Block Express:** Up to 256,000 IOPS per volume
- **EFS Intelligent-Tiering:** Automatic cost optimization for file storage
- **FSx for NetApp ONTAP:** Enterprise NAS in AWS
- **Impact:** Storage performance gaps vs. on-prem eliminated

**3. Container Advances**
- **ECS Service Connect:** Built-in service mesh for ECS
- **EKS Auto Mode:** Fully managed Kubernetes node lifecycle
- **EKS Pod Identities:** Simplified IAM for pods (replaces IRSA)
- **Fargate Spot:** Save 70% on fault-tolerant containerized workloads
- **Impact:** Container operations dramatically simplified

**4. Database Modernization**
- **Aurora Limitless Database:** Horizontal scaling beyond single-writer limit
- **DynamoDB Standard-IA:** Infrequent access tables at 60% cost savings
- **RDS Blue/Green Deployments:** Zero-downtime version upgrades
- **MemoryDB for Redis 7:** Redis compatibility with Multi-AZ durability
- **Impact:** Database scalability limits removed

**5. Security Enhancements**
- **IAM Access Analyzer:** Automated policy validation
- **Verified Permissions:** Cedar policy engine for app-level authorization
- **KMS External Key Store:** Bring your own HSM
- **GuardDuty for EKS Runtime:** Container threat detection
- **Impact:** Security automation reduces manual toil

**6. Cost Optimization Tools**
- **Graviton3:** 25% better performance vs. Graviton2, 60% less energy
- **Compute Optimizer for ECS:** Right-sizing recommendations
- **S3 Intelligent-Tiering Archive:** Auto-archive to Glacier tiers
- **RDS Optimized Reads:** 2x faster query performance on Aurora
- **Impact:** Cost optimization is now automated

### AWS Well-Architected Framework (2025 Revision)

**Six Pillars:**

1. **Operational Excellence**
   - IaC for all infrastructure
   - Automated deployments
   - Observability (CloudWatch, X-Ray)
   - Runbooks and playbooks

2. **Security**
   - Strong identity foundation (IAM)
   - Defense in depth
   - Data protection (encryption, KMS)
   - Incident response automation

3. **Reliability**
   - Multi-AZ deployments
   - Automated recovery
   - Change management via IaC
   - Capacity planning (auto-scaling)

4. **Performance Efficiency**
   - Right-size resources
   - Use managed services
   - Serverless-first approach
   - Monitor and optimize continuously

5. **Cost Optimization**
   - Measure and attribute costs
   - Right-size and autoscale
   - Use pricing models (Reserved, Spot)
   - Optimize data transfer

6. **Sustainability** (NEW in 2024)
   - Minimize carbon footprint
   - Use energy-efficient regions
   - Graviton-based compute
   - Optimize storage lifecycle

---

## AWS Service Taxonomy

### Compute Services

#### Tier 1: Serverless (Lambda)

**Use When:**
- Event-driven workloads
- Unpredictable or bursty traffic
- Pay-per-request cost model preferred
- Sub-second to 15-minute execution time
- Minimal operational overhead desired

**Avoid When:**
- Long-running processes (>15 minutes)
- Stateful workloads requiring local storage
- Predictable high throughput (cheaper alternatives exist)
- Complex deployment packages (>250MB unzipped)

**Cost Model:**
- $0.20 per 1M requests
- $0.0000166667 per GB-second (us-east-1)
- Free tier: 1M requests, 400,000 GB-seconds/month

**Example Use Cases:**
- API backends (via API Gateway)
- Image/video processing (S3 triggers)
- Scheduled jobs (EventBridge rules)
- Stream processing (Kinesis, DynamoDB Streams)

---

#### Tier 2: Containers - Fargate (Serverless Containers)

**Use When:**
- Containerized workloads without cluster management
- Variable traffic with auto-scaling
- Mixed CPU and memory requirements
- Multi-hour running tasks
- Don't want to manage EC2 instances

**Avoid When:**
- High-performance computing (need bare metal)
- GPU workloads (use EC2 with ECS/EKS)
- Extremely cost-sensitive at scale (EC2 cheaper)
- Stateful workloads requiring persistent local storage

**Cost Model:**
- Per vCPU-hour: $0.04048 (Linux)
- Per GB-hour: $0.004445 (Linux)
- Example: 1 vCPU, 2GB = ~$35/month (vs. t3.small EC2 ~$15/month)

**Example Use Cases:**
- Microservices (ECS or EKS on Fargate)
- Batch jobs (Fargate Spot for 70% savings)
- API servers (ALB → Fargate tasks)
- CI/CD build agents

---

#### Tier 3: Containers - ECS (Elastic Container Service)

**Use When:**
- AWS-native container orchestration preferred
- Tight integration with ALB, CloudWatch, IAM
- Simpler than Kubernetes
- Running on EC2 for cost optimization
- Hybrid Fargate + EC2 capacity

**Avoid When:**
- Multi-cloud portability required (use Kubernetes/EKS)
- Need Kubernetes ecosystem tools (Helm, Operators)
- Team has strong Kubernetes expertise

**Cost Model:**
- No ECS control plane fees
- Pay for EC2 instances or Fargate compute
- Example: 10 t3.medium instances = $300/month + EBS

**Key Features (2025):**
- **ECS Service Connect:** Built-in service mesh
- **ECS Anywhere:** Run ECS on-premises
- **Capacity Providers:** Auto-scaling between Fargate and EC2

---

#### Tier 4: Containers - EKS (Elastic Kubernetes Service)

**Use When:**
- Kubernetes expertise exists
- Multi-cloud/hybrid cloud strategy
- Need Kubernetes ecosystem (Helm, Operators, Istio)
- Complex workload orchestration
- Strong governance requirements (RBAC, NetworkPolicies)

**Avoid When:**
- Team lacks Kubernetes knowledge
- Simple workloads (over-engineering)
- Cost-sensitive (ECS is cheaper)
- Minimal operational overhead desired

**Cost Model:**
- EKS control plane: $0.10/hour = $73/month per cluster
- EC2 or Fargate compute costs
- Example: 3 m5.large nodes = $260/month + $73 control plane = $333/month

**Key Features (2025):**
- **EKS Auto Mode:** Managed node lifecycle
- **EKS Pod Identities:** Simplified IAM (replaces IRSA)
- **EKS Hybrid Nodes:** On-premises nodes
- **EKS Anywhere:** Self-managed Kubernetes on-prem

---

#### Tier 5: Virtual Machines - EC2

**Use When:**
- Maximum control over OS and runtime
- GPU/FPGA workloads
- Windows Server workloads
- Licensing constraints (BYOL)
- Highest performance requirements
- Cost optimization with Reserved Instances

**Avoid When:**
- Operational overhead is concern (use Fargate/Lambda)
- Unpredictable traffic (pay for idle capacity)
- Prefer managed services

**Cost Model (Example: us-east-1):**
- **t3.micro:** $0.0104/hour = $7.60/month (burstable)
- **t3.medium:** $0.0416/hour = $30.37/month (burstable)
- **m5.large:** $0.096/hour = $70.08/month (general purpose)
- **c5.xlarge:** $0.17/hour = $124.10/month (compute optimized)
- **r5.large:** $0.126/hour = $91.98/month (memory optimized)

**Reserved Instances (1-year, All Upfront):**
- 30-40% savings vs. on-demand
- 3-year: 50-60% savings

**Spot Instances:**
- 60-90% savings vs. on-demand
- Can be interrupted with 2-minute notice

---

### Storage Services

#### Tier 1: Object Storage - S3 (Simple Storage Service)

**Use When:**
- Static content (images, videos, documents)
- Data lake/analytics (Athena, Glue)
- Backups and archives
- Website hosting (static sites)
- Application assets (logs, exports)

**S3 Storage Classes (Cost Spectrum):**

| Storage Class | Use Case | Cost (per GB/month) | Retrieval Cost |
|---------------|----------|---------------------|----------------|
| **S3 Standard** | Frequent access | $0.023 | Free |
| **S3 Intelligent-Tiering** | Unknown/changing | $0.023-$0.00099 | Free |
| **S3 Standard-IA** | Infrequent (>30 days) | $0.0125 | $0.01/GB |
| **S3 One Zone-IA** | Non-critical, infrequent | $0.01 | $0.01/GB |
| **S3 Glacier Instant** | Archive, instant access | $0.004 | $0.03/GB |
| **S3 Glacier Flexible** | Archive, 1-5 min | $0.0036 | $0.01-$0.03/GB |
| **S3 Glacier Deep Archive** | Long-term (7-10 years) | $0.00099 | $0.02/GB + 12hr |
| **S3 Express One Zone** | High-performance (NEW) | $0.16 | Free |

**Key Features (2025):**
- **S3 Express One Zone:** 10x faster, single-digit ms latency
- **S3 Intelligent-Tiering:** Auto-optimization across 5 access tiers
- **S3 Object Lambda:** Transform objects during retrieval
- **S3 Batch Operations:** Perform operations on billions of objects

**Best Practices:**
- Use lifecycle policies to transition to cheaper tiers
- Enable versioning for critical data
- Use S3 Intelligent-Tiering for unknown patterns
- Encrypt at rest (SSE-S3, SSE-KMS)

---

#### Tier 2: Block Storage - EBS (Elastic Block Store)

**Use When:**
- EC2 instance persistent storage
- Database storage (RDS uses EBS)
- High IOPS requirements
- Boot volumes
- Transactional workloads

**EBS Volume Types:**

| Type | Use Case | Max IOPS | Max Throughput | Cost (GB/month) |
|------|----------|----------|----------------|-----------------|
| **gp3** (SSD) | General purpose | 16,000 | 1,000 MB/s | $0.08 |
| **gp2** (SSD) | Legacy general | 16,000 | 250 MB/s | $0.10 |
| **io2 Block Express** | Highest perf | 256,000 | 4,000 MB/s | $0.125 + IOPS |
| **io2** (SSD) | Critical apps | 64,000 | 1,000 MB/s | $0.125 + IOPS |
| **st1** (HDD) | Throughput | 500 | 500 MB/s | $0.045 |
| **sc1** (HDD) | Cold storage | 250 | 250 MB/s | $0.015 |

**Recommendation:** Use gp3 for 99% of workloads (20% cheaper than gp2, configurable IOPS/throughput)

**Key Features (2025):**
- **EBS Snapshots Archive:** 75% cheaper long-term storage
- **Fast Snapshot Restore:** Pre-warm snapshots for instant recovery
- **Multi-Attach:** Share io2 volumes across instances
- **Encryption by default:** All new volumes encrypted

---

#### Tier 3: File Storage - EFS (Elastic File System)

**Use When:**
- Shared file storage across EC2/Fargate/Lambda
- Content management systems
- Home directories
- Application migrations (NFS compatibility)
- Container persistent storage (ECS, EKS)

**EFS Storage Classes:**

| Class | Use Case | Cost (GB/month) | Performance |
|-------|----------|-----------------|-------------|
| **Standard** | Frequent access | $0.30 | High |
| **Infrequent Access (IA)** | >30 days idle | $0.025 | Lower |
| **One Zone** | Non-critical | $0.16 | High |
| **One Zone-IA** | Dev/test | $0.0133 | Lower |

**Key Features (2025):**
- **EFS Intelligent-Tiering:** Auto-move to IA tier
- **EFS Replication:** Cross-region disaster recovery
- **Elastic Throughput:** Auto-scale performance
- **NFS 4.1 compatibility**

**Performance Modes:**
- **General Purpose:** Low latency (<10ms)
- **Max I/O:** High aggregate throughput (big data)

---

#### Tier 4: High-Performance File - FSx

**FSx for Windows File Server:**
- Windows-native SMB file shares
- Active Directory integration
- SQL Server, home directories
- $0.013/GB-month + throughput costs

**FSx for Lustre:**
- High-performance computing (HPC)
- Machine learning training
- Video rendering
- Sub-millisecond latency, 100+ GB/s throughput

**FSx for NetApp ONTAP:**
- Enterprise NAS features (snapshots, clones, replication)
- Multi-protocol (NFS, SMB, iSCSI)
- Hybrid cloud (on-prem NetApp integration)

**FSx for OpenZFS:**
- Linux ZFS file systems
- Snapshots, clones, compression
- Up to 12.5 GB/s throughput

---

### Database Services

#### Tier 1: Relational - RDS (Relational Database Service)

**Supported Engines:**
- **PostgreSQL** (most popular open-source)
- **MySQL** (legacy compatibility)
- **MariaDB** (MySQL fork, enhanced)
- **Oracle** (enterprise, BYOL or license included)
- **SQL Server** (Microsoft, Web/Standard/Enterprise)

**Use When:**
- ACID transactions required
- Complex queries with joins
- Existing SQL applications
- Vertical scaling acceptable
- Strong consistency needed

**Avoid When:**
- Need horizontal scaling (use DynamoDB)
- Key-value access patterns (use DynamoDB)
- Extreme scale (>64TB, use Aurora)
- Serverless preferred (use Aurora Serverless)

**Cost Model (Example: db.t3.medium PostgreSQL):**
- Instance: $0.068/hour = $49.64/month
- Storage (gp3): $0.115/GB-month
- Example: 100GB storage = $49.64 + $11.50 = $61.14/month

**Key Features (2025):**
- **Blue/Green Deployments:** Zero-downtime version upgrades
- **RDS Optimized Reads:** 2x faster queries on Aurora
- **Multi-AZ:** Automatic failover
- **Read Replicas:** Scale read traffic (up to 15 replicas)

---

#### Tier 2: Relational - Aurora (AWS-Native, MySQL/PostgreSQL Compatible)

**Use When:**
- Need MySQL/PostgreSQL but higher performance
- Require horizontal read scaling (up to 15 read replicas)
- Global database (cross-region replication)
- Serverless variable workloads
- Database >64TB (Aurora scales to 128TB)

**Aurora vs. RDS:**
- **Performance:** 5x faster than MySQL, 3x faster than PostgreSQL
- **Availability:** 99.99% SLA (vs. 99.95% RDS Multi-AZ)
- **Scaling:** Storage auto-scales 10GB → 128TB
- **Cost:** 20% more than RDS, but higher performance

**Aurora Serverless v2 (2025):**
- Scale from 0.5 ACU to 128 ACU in seconds
- Pay-per-second billing
- Use for variable workloads (dev/test, seasonal apps)

**Aurora Limitless Database (NEW 2024):**
- Horizontal write scaling (sharding managed by Aurora)
- Millions of transactions per second
- Use for highest-scale OLTP workloads

**Cost Model (Aurora Serverless v2):**
- $0.12 per ACU-hour (1 ACU = 2GB RAM)
- Example: 2 ACU baseline, 10 ACU peak, 8hr/day active = ~$80/month

---

#### Tier 3: NoSQL - DynamoDB

**Use When:**
- Key-value or document data model
- Need single-digit millisecond latency
- Infinite horizontal scaling
- Serverless pricing model
- Event-driven architecture (DynamoDB Streams)

**Avoid When:**
- Complex queries with joins (use RDS/Aurora)
- Reporting/analytics (use Athena on S3)
- Schema changes frequent (use DocumentDB)

**Capacity Modes:**

| Mode | Use Case | Pricing |
|------|----------|---------|
| **On-Demand** | Unpredictable traffic | $1.25 per million read requests, $6.25 per million writes |
| **Provisioned** | Predictable traffic | $0.00065 per read unit, $0.00325 per write unit |

**Storage Classes:**
- **Standard:** $0.25/GB-month
- **Standard-IA (NEW 2024):** $0.10/GB-month (infrequent access)

**Key Features (2025):**
- **DynamoDB Standard-IA:** 60% cheaper for infrequent tables
- **PartiQL:** SQL-like query language
- **Global Tables:** Multi-region, active-active replication
- **DynamoDB Streams:** Real-time change data capture

**Best Practices:**
- Design partition keys to distribute traffic evenly
- Use Global Secondary Indexes (GSI) for alternate access patterns
- Enable point-in-time recovery (PITR)
- Use DynamoDB Accelerator (DAX) for microsecond latency

---

#### Tier 4: Document - DocumentDB (MongoDB Compatible)

**Use When:**
- MongoDB workloads (compatible with MongoDB 4.0+)
- Document-oriented data
- Need AWS-managed MongoDB alternative
- JSON data storage

**Avoid When:**
- Need native MongoDB features (use MongoDB Atlas)
- Simple key-value (use DynamoDB)

**Cost Model:**
- Instance: Similar to RDS pricing
- Storage: $0.10/GB-month
- I/O: $0.20 per million requests

---

#### Tier 5: In-Memory - ElastiCache

**ElastiCache for Redis:**
- Session storage
- Leaderboards, real-time analytics
- Pub/sub messaging
- Rate limiting

**ElastiCache for Memcached:**
- Simple caching layer
- Horizontal scaling (sharding)
- No persistence (use Redis for durability)

**MemoryDB for Redis (NEW Alternative):**
- Redis-compatible with Multi-AZ durability
- Microsecond read, single-digit millisecond write latency
- Use when you need Redis persistence + high availability

**Cost Model (cache.t3.medium Redis):**
- $0.068/hour = $49.64/month
- MemoryDB: ~20% more expensive but durable

---

### Networking Services

#### VPC (Virtual Private Cloud)

**Core Components:**

1. **Subnets**
   - **Public:** Internet-facing (IGW route)
   - **Private:** Internal only (NAT Gateway for outbound)
   - **Isolated:** No internet access

2. **Route Tables**
   - Associate with subnets
   - Define traffic routing
   - 0.0.0.0/0 → Internet Gateway (public)
   - 0.0.0.0/0 → NAT Gateway (private)

3. **Security Groups**
   - Stateful firewall (allow rules only)
   - Instance-level (ENI attachment)
   - Default deny all inbound

4. **Network ACLs**
   - Stateless firewall (allow + deny rules)
   - Subnet-level
   - Default allow all

**Standard 3-Tier VPC Pattern:**

```
VPC: 10.0.0.0/16

Availability Zone A:
  - Public Subnet:    10.0.1.0/24  (ALB, NAT Gateway)
  - Private Subnet:   10.0.11.0/24 (ECS/EKS, Lambda)
  - Database Subnet:  10.0.21.0/24 (RDS, Aurora)

Availability Zone B:
  - Public Subnet:    10.0.2.0/24  (ALB, NAT Gateway)
  - Private Subnet:   10.0.12.0/24 (ECS/EKS, Lambda)
  - Database Subnet:  10.0.22.0/24 (RDS, Aurora)

Availability Zone C:
  - Public Subnet:    10.0.3.0/24  (ALB, NAT Gateway)
  - Private Subnet:   10.0.13.0/24 (ECS/EKS, Lambda)
  - Database Subnet:  10.0.23.0/24 (RDS, Aurora)
```

**Best Practices:**
- Use /16 VPC CIDR (65,536 IPs)
- Use /24 subnet CIDRs (256 IPs, 251 usable)
- Reserve first two subnets for future expansion
- Multi-AZ for high availability (minimum 2 AZs)
- Use VPC Flow Logs for troubleshooting

---

#### Load Balancing

**Application Load Balancer (ALB):**
- **Use For:** HTTP/HTTPS traffic
- **Features:**
  - Path-based routing (/api → backend, /web → frontend)
  - Host-based routing (api.example.com, web.example.com)
  - WebSocket support
  - HTTP/2, gRPC support
  - Lambda target support (serverless)
- **Cost:** $0.0225/hour + $0.008/LCU-hour (~$20/month minimum)

**Network Load Balancer (NLB):**
- **Use For:** TCP/UDP traffic, extreme performance
- **Features:**
  - Ultra-low latency (<100 microseconds)
  - Millions of requests per second
  - Static IP addresses (Elastic IP)
  - PrivateLink support
- **Cost:** $0.0225/hour + $0.006/NLCU-hour

**Gateway Load Balancer (GWLB):**
- **Use For:** Inline security appliances (firewalls, IDS/IPS)
- **Features:**
  - Layer 3 gateway + Layer 4 load balancing
  - Traffic inspection
  - Third-party appliance integration

**Classic Load Balancer (CLB):**
- **Legacy:** Use ALB or NLB for new applications

---

#### CloudFront (CDN)

**Use When:**
- Static content distribution (S3, images, videos)
- Dynamic content acceleration
- Global low-latency delivery
- DDoS protection (AWS Shield)

**Features:**
- 450+ edge locations worldwide
- Origin types: S3, ALB, NLB, EC2, custom origins
- Cache behaviors per path pattern
- Lambda@Edge for request/response manipulation

**Cost Model:**
- Data transfer out: $0.085/GB (first 10TB, decreases with volume)
- HTTP/HTTPS requests: $0.0075 per 10,000 requests
- Free tier: 1TB transfer, 10M requests/month (12 months)

---

#### Route 53 (DNS)

**Use When:**
- Domain registration
- DNS hosting
- Health checks and failover
- Traffic routing policies

**Routing Policies:**
- **Simple:** Single resource
- **Weighted:** A/B testing, gradual migration
- **Latency:** Route to lowest-latency region
- **Failover:** Active-passive disaster recovery
- **Geolocation:** Route based on user location
- **Geoproximity:** Route based on resource location + bias
- **Multi-value:** Return multiple IPs with health checks

**Cost Model:**
- Hosted zone: $0.50/month
- Queries: $0.40 per million (first 1 billion)
- Health checks: $0.50/month per health check

---

### Security Services

#### IAM (Identity and Access Management)

**Core Concepts:**

1. **Principals:**
   - Users (humans)
   - Roles (assumed by services/users)
   - Groups (collection of users)

2. **Policies:**
   - Identity-based (attached to users/roles/groups)
   - Resource-based (attached to resources like S3 buckets)
   - Permission boundaries (maximum permissions)

3. **Trust Relationships:**
   - Who can assume a role (AssumeRole)
   - Service-linked roles (AWS service assumptions)

**Least Privilege Pattern:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/uploads/*"
    }
  ]
}
```

**Best Practices:**
- Use roles, not users, for applications
- Enable MFA for privileged users
- Use IAM Access Analyzer to validate policies
- Rotate credentials regularly
- Use AWS Organizations SCP for guardrails

---

#### KMS (Key Management Service)

**Use When:**
- Encrypt data at rest (S3, EBS, RDS)
- Envelope encryption
- Cryptographic operations (sign, verify)

**Key Types:**
- **AWS managed keys:** Free, automatic rotation
- **Customer managed keys:** $1/month, full control
- **Custom key stores:** Bring your own HSM

**Encryption Patterns:**
- **Server-side encryption (SSE):** AWS encrypts on write
- **Client-side encryption:** Encrypt before sending to AWS
- **Envelope encryption:** Encrypt data key with master key

**Cost Model:**
- Customer managed key: $1/month
- API requests: $0.03 per 10,000 requests

---

#### Secrets Manager

**Use When:**
- Database credentials rotation
- API keys, tokens
- Application secrets
- Automatic rotation required

**Secrets Manager vs. Parameter Store:**

| Feature | Secrets Manager | Parameter Store |
|---------|-----------------|-----------------|
| **Cost** | $0.40/secret/month | Free (Standard), $0.05/param (Advanced) |
| **Rotation** | Automatic (Lambda) | Manual |
| **Secret size** | 64KB | 8KB (Advanced) |
| **Versioning** | Automatic | Manual |
| **Use case** | Rotating secrets | Configuration, non-rotating |

**Best Practice:** Use Secrets Manager for DB credentials, Parameter Store for configuration

---

#### WAF (Web Application Firewall)

**Use When:**
- Protect ALB, CloudFront, API Gateway
- Block SQL injection, XSS
- Rate limiting
- Geo-blocking

**Managed Rule Groups:**
- AWS Core Rule Set
- SQL injection protection
- Linux/Windows OS rules
- IP reputation lists

**Cost Model:**
- Web ACL: $5/month
- Rules: $1/month per rule
- Requests: $0.60 per million

---

## Decision Frameworks

### Framework 1: Compute Service Selection

**Decision Tree:**

```
START: Choosing compute service

Q1: What is the execution duration?
  ├─ <15 minutes → Q2
  └─ >15 minutes → Q5

Q2: Is it event-driven or scheduled?
  ├─ YES → Lambda (serverless)
  └─ NO → Q3

Q3: Do you need long-running connections (WebSockets)?
  ├─ YES → Fargate or EC2
  └─ NO → Lambda or Fargate

Q4: What is the cost sensitivity?
  ├─ High → Lambda (pay per request)
  └─ Medium → Fargate (pay for running time)

Q5: Is it containerized?
  ├─ YES → Q6
  └─ NO → Q8

Q6: Do you need Kubernetes?
  ├─ YES → EKS (managed Kubernetes)
  └─ NO → Q7

Q7: Do you want to manage EC2 instances?
  ├─ YES → ECS on EC2 (cost optimization)
  └─ NO → ECS on Fargate (operational simplicity)

Q8: Do you need Windows Server or GPU?
  ├─ YES → EC2 (virtual machines)
  └─ NO → Consider containerizing → Q5
```

**Quick Reference:**

| Workload | First Choice | Alternative | Why |
|----------|--------------|-------------|-----|
| **API Backend** | Lambda + API Gateway | Fargate + ALB | Serverless, auto-scale |
| **Background Jobs** | Lambda (EventBridge) | Fargate Spot | Event-driven, cost |
| **Microservices** | ECS on Fargate | EKS on Fargate | Simplicity vs. portability |
| **Batch Processing** | Lambda (Step Functions) | Fargate Spot | Orchestration vs. cost |
| **Web Server** | Fargate + ALB | EC2 + ALB | No ops vs. cost |
| **GPU Workload** | EC2 (g4dn, p4d) | EKS + EC2 | Control + cost |
| **HPC** | EC2 (c6i, hpc7a) | Batch | Performance |

---

### Framework 2: Database Service Selection

**Decision Matrix:**

| Access Pattern | Data Model | First Choice | Alternative | Why |
|----------------|------------|--------------|-------------|-----|
| **Transactional (OLTP)** | Relational | Aurora | RDS PostgreSQL | Performance vs. cost |
| **Key-Value** | NoSQL | DynamoDB | ElastiCache Redis | Durability vs. speed |
| **Document** | JSON/BSON | DynamoDB | DocumentDB | Serverless vs. MongoDB |
| **In-Memory Cache** | Key-Value | ElastiCache Redis | MemoryDB | Cost vs. durability |
| **Analytical (OLAP)** | Columnar | Redshift | Athena + S3 | Dedicated vs. serverless |
| **Graph** | Nodes/Edges | Neptune | - | Native graph queries |
| **Time-Series** | Time-stamped | Timestream | DynamoDB + TTL | Purpose-built vs. general |
| **Ledger** | Immutable | QLDB | - | Cryptographic verification |

**Query Complexity Guide:**

```
Simple Key-Value Lookups
  → DynamoDB

Moderate Complexity (joins across 2-3 tables)
  → Aurora or RDS

High Complexity (joins across many tables, analytics)
  → Redshift or Athena

Real-Time Stream Processing
  → DynamoDB Streams + Lambda
  → Kinesis Data Analytics
```

---

### Framework 3: Storage Service Selection

**Decision Tree:**

```
START: Choosing storage service

Q1: What type of data?
  ├─ Files (shared across instances) → Q2
  ├─ Objects (images, videos, documents) → S3
  └─ Blocks (database, boot volumes) → EBS

Q2: What protocol is needed?
  ├─ NFS (Linux) → EFS or FSx for Lustre
  ├─ SMB (Windows) → FSx for Windows
  ├─ POSIX → FSx for Lustre or FSx for OpenZFS
  └─ Multi-protocol → FSx for NetApp ONTAP

Q3: What is the access frequency?
  ├─ Frequent → EFS Standard or FSx
  ├─ Infrequent → EFS IA
  └─ Archive → S3 Glacier

Q4: What is the performance requirement?
  ├─ High (HPC, ML) → FSx for Lustre
  ├─ Standard → EFS or FSx
  └─ Budget → S3 + lifecycle policies
```

**Cost Comparison (1TB for 1 Month):**

| Service | Cost | Use Case |
|---------|------|----------|
| S3 Standard | $23 | Objects, frequent access |
| S3 Standard-IA | $12.50 | Objects, infrequent access |
| S3 Glacier Instant | $4 | Archive, instant retrieval |
| S3 Glacier Deep Archive | $0.99 | Long-term archive |
| EBS gp3 | $80 | Block storage, EC2 |
| EFS Standard | $300 | Shared file storage |
| EFS IA | $25 | Infrequent file access |
| FSx for Lustre | ~$145+ | High-performance HPC |

**Recommendation:** Use S3 for 80%+ of storage needs, EFS/FSx only when shared file access required

---

### Framework 4: Serverless Architecture Pattern

**When to Go Serverless:**

✅ **Ideal For:**
- Variable traffic (unpredictable or bursty)
- Event-driven workloads
- Minimal operational overhead desired
- Pay-per-use cost model
- Stateless applications
- Rapid development and deployment

❌ **Avoid When:**
- Predictable high traffic (cheaper alternatives)
- Long-running processes (>15 min)
- Stateful workloads
- Cold start latency critical (<100ms required)
- Complex deployment packages (>250MB)

**Serverless Stack Pattern:**

```
User Request
  ↓
CloudFront (CDN)
  ↓
API Gateway (REST or HTTP API)
  ↓
Lambda Function(s)
  ↓
DynamoDB or Aurora Serverless
  ↓
S3 (static assets, uploads)
  ↓
EventBridge (async events)
  ↓
Lambda (background processing)
  ↓
SQS/SNS (messaging)
```

**Cost Example (API with 1M requests/month):**
- API Gateway: $3.50 (1M HTTP API requests)
- Lambda: $0.20 (1M requests) + $3.33 (compute) = $3.53
- DynamoDB: $1.25 (on-demand reads) + $6.25 (writes) = ~$7.50
- **Total: ~$15/month** (vs. Fargate ~$35+, EC2 ~$50+)

---

## Implementation Patterns

### Pattern 1: Serverless REST API

**Architecture:**
```
API Gateway (HTTP API)
  → Lambda (Node.js/Python/Go)
    → DynamoDB (data storage)
    → S3 (file uploads)
```

**Use Case:** RESTful API with CRUD operations

**AWS CDK Example (TypeScript):**

```typescript
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { Construct } from 'constructs';

export class ServerlessApiStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB Table
    const table = new dynamodb.Table(this, 'ItemsTable', {
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY, // For dev/test
    });

    // Lambda Function
    const handler = new lambda.Function(this, 'ApiHandler', {
      runtime: lambda.Runtime.NODEJS_18_X,
      code: lambda.Code.fromAsset('lambda'),
      handler: 'index.handler',
      environment: {
        TABLE_NAME: table.tableName,
      },
    });

    // Grant Lambda permissions to DynamoDB
    table.grantReadWriteData(handler);

    // API Gateway
    const api = new apigateway.RestApi(this, 'ItemsApi', {
      restApiName: 'Items Service',
      description: 'This service serves items',
    });

    const items = api.root.addResource('items');
    items.addMethod('GET', new apigateway.LambdaIntegration(handler));
    items.addMethod('POST', new apigateway.LambdaIntegration(handler));

    const item = items.addResource('{id}');
    item.addMethod('GET', new apigateway.LambdaIntegration(handler));
    item.addMethod('PUT', new apigateway.LambdaIntegration(handler));
    item.addMethod('DELETE', new apigateway.LambdaIntegration(handler));

    // Output API URL
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: api.url,
    });
  }
}
```

**Terraform Alternative:**

```hcl
# DynamoDB Table
resource "aws_dynamodb_table" "items" {
  name         = "items"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }
}

# Lambda Function
resource "aws_lambda_function" "api_handler" {
  filename      = "lambda.zip"
  function_name = "api_handler"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "nodejs18.x"

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.items.name
    }
  }
}

# API Gateway
resource "aws_apigatewayv2_api" "http_api" {
  name          = "items-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id           = aws_apigatewayv2_api.http_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.api_handler.invoke_arn
}

resource "aws_apigatewayv2_route" "get_items" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "GET /items"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}
```

---

### Pattern 2: Container-Based Microservices (ECS on Fargate)

**Architecture:**
```
ALB (Application Load Balancer)
  → ECS Service (Fargate)
    → RDS Aurora (database)
    → ElastiCache Redis (session cache)
```

**Use Case:** Microservices with Docker containers

**AWS CDK Example (TypeScript):**

```typescript
import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecs_patterns from 'aws-cdk-lib/aws-ecs-patterns';
import { Construct } from 'constructs';

export class MicroservicesStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // VPC
    const vpc = new ec2.Vpc(this, 'MyVpc', {
      maxAzs: 3,
      natGateways: 1,
    });

    // ECS Cluster
    const cluster = new ecs.Cluster(this, 'MyCluster', {
      vpc: vpc,
      containerInsights: true,
    });

    // Fargate Service with ALB
    const fargateService = new ecs_patterns.ApplicationLoadBalancedFargateService(
      this,
      'MyFargateService',
      {
        cluster: cluster,
        cpu: 512,
        memoryLimitMiB: 1024,
        desiredCount: 2,
        taskImageOptions: {
          image: ecs.ContainerImage.fromRegistry('amazon/amazon-ecs-sample'),
          containerPort: 80,
          environment: {
            NODE_ENV: 'production',
          },
        },
        publicLoadBalancer: true,
      }
    );

    // Auto-scaling
    const scaling = fargateService.service.autoScaleTaskCount({
      minCapacity: 2,
      maxCapacity: 10,
    });

    scaling.scaleOnCpuUtilization('CpuScaling', {
      targetUtilizationPercent: 70,
    });

    scaling.scaleOnMemoryUtilization('MemoryScaling', {
      targetUtilizationPercent: 80,
    });

    // Output ALB URL
    new cdk.CfnOutput(this, 'LoadBalancerDNS', {
      value: fargateService.loadBalancer.loadBalancerDnsName,
    });
  }
}
```

---

### Pattern 3: Event-Driven Architecture

**Architecture:**
```
S3 Upload
  → EventBridge Rule
    → Lambda (process file)
      → DynamoDB (store metadata)
        → SQS (downstream processing)
```

**Use Case:** Asynchronous file processing pipeline

**AWS CDK Example (TypeScript):**

```typescript
import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import { Construct } from 'constructs';

export class EventDrivenStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // S3 Bucket
    const bucket = new s3.Bucket(this, 'UploadBucket', {
      eventBridgeEnabled: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    // Processing Lambda
    const processor = new lambda.Function(this, 'Processor', {
      runtime: lambda.Runtime.PYTHON_3_11,
      code: lambda.Code.fromAsset('lambda'),
      handler: 'processor.handler',
    });

    bucket.grantRead(processor);

    // SQS Queue
    const queue = new sqs.Queue(this, 'ProcessingQueue', {
      visibilityTimeout: cdk.Duration.seconds(300),
    });

    queue.grantSendMessages(processor);

    // EventBridge Rule
    const rule = new events.Rule(this, 'S3UploadRule', {
      eventPattern: {
        source: ['aws.s3'],
        detailType: ['Object Created'],
        detail: {
          bucket: {
            name: [bucket.bucketName],
          },
        },
      },
    });

    rule.addTarget(new targets.LambdaFunction(processor));

    new cdk.CfnOutput(this, 'BucketName', {
      value: bucket.bucketName,
    });
  }
}
```

---

### Pattern 4: Three-Tier Web Application

**Architecture:**
```
CloudFront (CDN)
  → S3 (static frontend)
  → ALB (API tier)
    → ECS Fargate (application tier)
      → RDS Aurora (database tier)
```

**Terraform Example:**

```hcl
# VPC
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"

  name = "production-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  database_subnets = ["10.0.201.0/24", "10.0.202.0/24", "10.0.203.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = false # Multi-AZ
  enable_dns_hostnames = true
}

# ALB
resource "aws_lb" "main" {
  name               = "main-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = module.vpc.public_subnets
}

# RDS Aurora
resource "aws_rds_cluster" "main" {
  cluster_identifier      = "aurora-cluster"
  engine                  = "aurora-postgresql"
  engine_version          = "15.3"
  database_name           = "myapp"
  master_username         = "admin"
  master_password         = random_password.db_password.result
  db_subnet_group_name    = aws_db_subnet_group.main.name
  vpc_security_group_ids  = [aws_security_group.db.id]
  backup_retention_period = 7
  preferred_backup_window = "03:00-04:00"
  storage_encrypted       = true
  kms_key_id              = aws_kms_key.rds.arn
}

resource "aws_rds_cluster_instance" "main" {
  count              = 2
  identifier         = "aurora-instance-${count.index}"
  cluster_identifier = aws_rds_cluster.main.id
  instance_class     = "db.r6g.large"
  engine             = aws_rds_cluster.main.engine
}

# S3 for static frontend
resource "aws_s3_bucket" "frontend" {
  bucket = "my-app-frontend"
}

resource "aws_s3_bucket_website_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  index_document {
    suffix = "index.html"
  }
}

# CloudFront
resource "aws_cloudfront_distribution" "main" {
  enabled             = true
  default_root_object = "index.html"

  origin {
    domain_name = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_id   = "S3-Frontend"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.main.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-Frontend"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}
```

---

## Well-Architected Framework

### Pillar 1: Operational Excellence

**Key Practices:**

1. **Infrastructure as Code**
   - All infrastructure defined in code (CDK, Terraform, CloudFormation)
   - Version controlled (Git)
   - Peer-reviewed (pull requests)
   - Automated deployments (CI/CD)

2. **Observability**
   - CloudWatch Logs for application logs
   - CloudWatch Metrics for system metrics
   - X-Ray for distributed tracing
   - CloudWatch Alarms for anomaly detection

3. **Runbooks and Playbooks**
   - Document common operations
   - Automate with Systems Manager Automation
   - Test regularly (GameDays)

4. **Deployment Safety**
   - Blue-green deployments
   - Canary releases
   - Rollback mechanisms
   - Feature flags

**CDK Example - CloudWatch Dashboard:**

```typescript
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';

const dashboard = new cloudwatch.Dashboard(this, 'MyDashboard', {
  dashboardName: 'ApplicationMetrics',
});

dashboard.addWidgets(
  new cloudwatch.GraphWidget({
    title: 'Lambda Invocations',
    left: [lambdaFunction.metricInvocations()],
  }),
  new cloudwatch.GraphWidget({
    title: 'API Gateway Requests',
    left: [api.metricCount()],
  })
);
```

---

### Pillar 2: Security

**Key Practices:**

1. **Identity and Access Management**
   - Use IAM roles, not users, for applications
   - Implement least privilege
   - Enable MFA for privileged users
   - Use AWS Organizations for multi-account structure

2. **Data Protection**
   - Encrypt data at rest (S3, EBS, RDS encryption)
   - Encrypt data in transit (TLS/HTTPS)
   - Use KMS for key management
   - Enable S3 versioning and MFA delete

3. **Network Security**
   - VPC isolation
   - Security groups (stateful firewall)
   - Network ACLs (stateless firewall)
   - WAF for application layer protection
   - PrivateLink for private connectivity

4. **Detective Controls**
   - Enable CloudTrail (API audit logs)
   - Enable VPC Flow Logs
   - Enable GuardDuty (threat detection)
   - Enable Security Hub (compliance monitoring)

**Terraform Example - Encryption:**

```hcl
# S3 Bucket with encryption
resource "aws_s3_bucket" "data" {
  bucket = "my-secure-bucket"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }
  }
}

# RDS with encryption
resource "aws_db_instance" "main" {
  identifier          = "mydb"
  engine              = "postgres"
  instance_class      = "db.t3.micro"
  storage_encrypted   = true
  kms_key_id          = aws_kms_key.rds.arn
}
```

---

### Pillar 3: Reliability

**Key Practices:**

1. **Multi-AZ Deployments**
   - RDS Multi-AZ
   - Aurora replicas across AZs
   - ECS/EKS tasks across AZs
   - ALB/NLB across AZs

2. **Auto-Scaling**
   - EC2 Auto Scaling Groups
   - ECS Service Auto Scaling
   - DynamoDB Auto Scaling
   - Lambda automatic scaling

3. **Backup and Recovery**
   - RDS automated backups
   - S3 versioning and replication
   - EBS snapshots
   - Cross-region backups

4. **Chaos Engineering**
   - AWS Fault Injection Simulator
   - Test failure scenarios
   - Validate recovery procedures

**CDK Example - Multi-AZ RDS:**

```typescript
import * as rds from 'aws-cdk-lib/aws-rds';

const database = new rds.DatabaseInstance(this, 'Database', {
  engine: rds.DatabaseInstanceEngine.postgres({
    version: rds.PostgresEngineVersion.VER_15_3,
  }),
  instanceType: ec2.InstanceType.of(
    ec2.InstanceClass.T3,
    ec2.InstanceSize.MEDIUM
  ),
  vpc,
  multiAz: true, // High availability
  allocatedStorage: 100,
  backupRetention: cdk.Duration.days(7),
  deleteAutomatedBackups: false,
  removalPolicy: cdk.RemovalPolicy.SNAPSHOT,
});
```

---

### Pillar 4: Performance Efficiency

**Key Practices:**

1. **Right-Size Resources**
   - Use Compute Optimizer
   - Monitor CloudWatch metrics
   - Adjust based on actual usage

2. **Use Managed Services**
   - Reduce operational overhead
   - Benefit from AWS optimizations
   - Examples: Aurora vs. self-managed DB, Lambda vs. EC2

3. **Caching**
   - CloudFront for static content
   - ElastiCache for database queries
   - DAX for DynamoDB
   - API Gateway caching

4. **Content Delivery**
   - CloudFront edge locations
   - S3 Transfer Acceleration
   - Global Accelerator for TCP/UDP

**Performance Optimization Pattern:**

```
User Request
  → CloudFront (cache static content)
    → API Gateway (cache API responses)
      → Lambda (with Provisioned Concurrency for low latency)
        → DAX (cache DynamoDB reads)
          → DynamoDB
```

---

### Pillar 5: Cost Optimization

**Key Practices:**

1. **Right-Sizing**
   - EC2: Use Compute Optimizer recommendations
   - RDS: Right-size instance types
   - Lambda: Optimize memory allocation (affects CPU)

2. **Pricing Models**
   - Reserved Instances (1-3 year commitment, 30-60% savings)
   - Savings Plans (flexible commitment, similar savings)
   - Spot Instances (60-90% savings, interruption-tolerant)

3. **Storage Optimization**
   - S3 Intelligent-Tiering
   - S3 Lifecycle policies
   - EBS gp3 (cheaper than gp2)
   - Delete unused snapshots

4. **Monitoring and Budgets**
   - AWS Cost Explorer
   - AWS Budgets (alerts)
   - Cost Allocation Tags
   - Trusted Advisor cost checks

**Terraform Example - S3 Lifecycle:**

```hcl
resource "aws_s3_bucket_lifecycle_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    id     = "transition-to-ia"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER_IR"
    }

    transition {
      days          = 365
      storage_class = "DEEP_ARCHIVE"
    }

    expiration {
      days = 2555 # 7 years
    }
  }
}
```

---

### Pillar 6: Sustainability

**Key Practices:**

1. **Use Graviton Processors**
   - 60% less energy than x86
   - 25% better performance than Graviton2
   - Available: EC2, Lambda, Fargate, RDS, ElastiCache

2. **Optimize Workload Placement**
   - Use regions with renewable energy
   - Consolidate workloads
   - Auto-scale to reduce idle resources

3. **Storage Efficiency**
   - Delete unused data
   - Compress data
   - Use appropriate storage tiers

4. **Software Efficiency**
   - Optimize code for performance
   - Use async processing
   - Minimize data transfer

**CDK Example - Graviton Lambda:**

```typescript
const handler = new lambda.Function(this, 'Handler', {
  runtime: lambda.Runtime.PYTHON_3_11,
  architecture: lambda.Architecture.ARM_64, // Graviton
  code: lambda.Code.fromAsset('lambda'),
  handler: 'index.handler',
});
```

---

## Multi-Language Infrastructure as Code

### AWS CDK (Cloud Development Kit)

**Supported Languages:**
- TypeScript (most popular)
- Python
- Java
- C#
- Go (experimental)

**Why CDK?**
- Type safety and IDE autocomplete
- Reusable constructs
- Higher-level abstractions
- Synthesizes to CloudFormation

**Installation:**

```bash
npm install -g aws-cdk
cdk --version
```

**Project Setup:**

```bash
mkdir my-app && cd my-app
cdk init app --language=typescript
npm install
```

**CDK CLI Commands:**

```bash
cdk synth              # Generate CloudFormation template
cdk diff               # Show differences
cdk deploy             # Deploy stack
cdk destroy            # Delete stack
cdk bootstrap          # Set up CDK toolkit stack
```

---

### Terraform

**Why Terraform?**
- Multi-cloud support (AWS, GCP, Azure)
- HCL declarative language
- Largest ecosystem (providers, modules)
- State management

**Installation:**

```bash
# macOS
brew install terraform

# Linux
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/
```

**Project Setup:**

```hcl
# main.tf
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = "us-east-1"
}
```

**Terraform CLI Commands:**

```bash
terraform init         # Initialize project
terraform plan         # Show execution plan
terraform apply        # Apply changes
terraform destroy      # Destroy infrastructure
terraform fmt          # Format code
terraform validate     # Validate syntax
```

---

### CloudFormation (Native AWS)

**Why CloudFormation?**
- Native AWS integration
- No additional tools required
- AWS service support on day 1
- Change sets for previewing

**Example Template (YAML):**

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Simple Lambda Function'

Resources:
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

  MyFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: MyFunction
      Runtime: python3.11
      Handler: index.handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        ZipFile: |
          def handler(event, context):
              return {
                  'statusCode': 200,
                  'body': 'Hello from Lambda!'
              }

Outputs:
  FunctionArn:
    Value: !GetAtt MyFunction.Arn
    Export:
      Name: MyFunctionArn
```

**CLI Commands:**

```bash
aws cloudformation create-stack --stack-name my-stack --template-body file://template.yaml
aws cloudformation update-stack --stack-name my-stack --template-body file://template.yaml
aws cloudformation delete-stack --stack-name my-stack
aws cloudformation describe-stacks --stack-name my-stack
```

---

## Library Recommendations

### Primary Tools

| Tool | Version | Use Case | Language |
|------|---------|----------|----------|
| **AWS CDK** | 2.x | Infrastructure as Code | TypeScript, Python, Java, C# |
| **Terraform** | 1.6+ | Multi-cloud IaC | HCL |
| **boto3** | Latest | AWS SDK for Python | Python |
| **AWS CLI** | 2.x | Command-line operations | Bash |
| **AWS SAM** | Latest | Serverless application framework | YAML |

### AWS CDK

**Why CDK?**
- Type-safe infrastructure
- Reusable constructs
- Best for AWS-heavy workloads
- Strong TypeScript ecosystem

**Installation:**

```bash
npm install -g aws-cdk
cdk --version
```

**Common Constructs:**

```typescript
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
```

---

### Terraform AWS Provider

**Why Terraform?**
- Multi-cloud (AWS + GCP + Azure)
- Largest community
- Terraform Cloud for team collaboration
- Terragrunt for DRY code

**Installation:**

```bash
brew install terraform
terraform --version
```

**Common Resources:**

```hcl
resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
}

resource "aws_s3_bucket" "example" {
  bucket = "my-bucket"
}

resource "aws_lambda_function" "example" {
  function_name = "my-function"
  runtime       = "python3.11"
  handler       = "index.handler"
  filename      = "lambda.zip"
  role          = aws_iam_role.lambda.arn
}
```

---

### boto3 (AWS SDK for Python)

**Why boto3?**
- Official AWS SDK for Python
- Comprehensive API coverage
- Great for automation scripts
- Strong documentation

**Installation:**

```bash
pip install boto3
```

**Example - List S3 Buckets:**

```python
import boto3

s3 = boto3.client('s3')
response = s3.list_buckets()

for bucket in response['Buckets']:
    print(f"Bucket: {bucket['Name']}")
```

**Example - Upload to S3:**

```python
import boto3

s3 = boto3.client('s3')
s3.upload_file('local-file.txt', 'my-bucket', 'remote-file.txt')
```

---

### AWS CLI v2

**Why AWS CLI?**
- Quickest way to interact with AWS
- Scripting and automation
- Testing and debugging
- SSO support

**Installation:**

```bash
# macOS
brew install awscli

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

**Common Commands:**

```bash
# S3
aws s3 ls
aws s3 cp local-file.txt s3://my-bucket/
aws s3 sync ./local-dir s3://my-bucket/prefix/

# EC2
aws ec2 describe-instances
aws ec2 run-instances --image-id ami-xxx --instance-type t3.micro

# Lambda
aws lambda invoke --function-name my-function output.json
aws lambda list-functions

# DynamoDB
aws dynamodb scan --table-name my-table
aws dynamodb put-item --table-name my-table --item '{"id": {"S": "123"}}'
```

---

## Skill Structure Design

### Skill File Organization

**Proposed Structure:**

```
aws-patterns/
├── SKILL.md                          # Main skill file (<600 lines)
├── references/
│   ├── compute-services.md           # Deep dive: Lambda, Fargate, ECS, EKS, EC2
│   ├── storage-services.md           # Deep dive: S3, EBS, EFS, FSx
│   ├── database-services.md          # Deep dive: RDS, Aurora, DynamoDB
│   ├── networking.md                 # Deep dive: VPC, ALB/NLB, CloudFront, Route53
│   ├── security.md                   # Deep dive: IAM, KMS, Secrets Manager, WAF
│   ├── serverless-patterns.md        # Serverless architecture patterns
│   ├── container-patterns.md         # ECS/EKS patterns
│   └── well-architected.md           # Six pillars deep dive
├── examples/
│   ├── cdk/
│   │   ├── serverless-api/           # API Gateway + Lambda + DynamoDB
│   │   ├── ecs-fargate/              # ALB + ECS + RDS
│   │   ├── event-driven/             # EventBridge + Lambda + SQS
│   │   └── three-tier-app/           # CloudFront + S3 + ALB + ECS + RDS
│   ├── terraform/
│   │   ├── serverless-api/
│   │   ├── ecs-fargate/
│   │   ├── vpc-networking/
│   │   └── rds-aurora/
│   └── cloudformation/
│       ├── lambda-api.yaml
│       └── ecs-service.yaml
└── scripts/
    ├── cost-estimate.sh              # Estimate infrastructure costs
    ├── resource-audit.sh             # Audit AWS resources
    └── security-check.sh             # Basic security validation
```

---

### SKILL.md Structure (Main File)

**Sections (Target: ~550-600 lines):**

1. **Frontmatter** (YAML)
   - name, description

2. **Purpose** (2-3 paragraphs)
   - What this skill teaches
   - When to use this skill

3. **Service Selection Frameworks** (~100 lines)
   - Compute decision tree
   - Database decision matrix
   - Storage selection guide
   - Link to references/compute-services.md, database-services.md, storage-services.md

4. **Serverless Patterns** (~80 lines)
   - Lambda + API Gateway + DynamoDB
   - Event-driven with EventBridge
   - Link to references/serverless-patterns.md

5. **Container Patterns** (~80 lines)
   - ECS on Fargate
   - EKS patterns
   - Link to references/container-patterns.md

6. **Networking Essentials** (~70 lines)
   - VPC design
   - Load balancing (ALB/NLB)
   - Link to references/networking.md

7. **Security Best Practices** (~70 lines)
   - IAM patterns
   - Encryption (KMS)
   - Link to references/security.md

8. **Well-Architected Framework** (~60 lines)
   - Six pillars overview
   - Link to references/well-architected.md

9. **Infrastructure as Code** (~50 lines)
   - CDK vs. Terraform vs. CloudFormation
   - Link to examples/

10. **Reference Links** (~20 lines)
    - Links to all references/ files
    - Links to examples/

---

### Progressive Disclosure Strategy

**Main SKILL.md Contains:**
- High-level decision frameworks
- Quick reference patterns
- When to use each service
- Links to detailed references

**References/ Contains:**
- Deep dives into each topic
- Comprehensive code examples
- Advanced patterns
- Edge cases and considerations

**Examples/ Contains:**
- Complete working projects
- CDK, Terraform, CloudFormation
- Copy-paste ready

**Scripts/ Contains:**
- Cost estimation tools
- Resource auditing
- Security validation

---

## Integration Points

### Integration with Existing Skills

#### 1. **infrastructure-as-code** Skill
- **Connection:** AWS-specific IaC patterns
- **Patterns:**
  - CDK for AWS (TypeScript, Python)
  - Terraform AWS provider
  - CloudFormation

**Cross-Reference:**
- infrastructure-as-code skill teaches multi-cloud IaC concepts
- aws-patterns skill provides AWS-specific implementations

---

#### 2. **kubernetes-operations** Skill
- **Connection:** EKS cluster operations
- **Patterns:**
  - EKS cluster setup with Terraform/CDK
  - IAM Roles for Service Accounts (IRSA)
  - EKS Pod Identities (2024+)
  - ALB Ingress Controller
  - EBS CSI Driver for persistent storage

**Example Integration:**

```typescript
// CDK: Create EKS cluster
const cluster = new eks.Cluster(this, 'MyCluster', {
  version: eks.KubernetesVersion.V1_28,
  defaultCapacity: 0, // Use Fargate
});

// Add Fargate profile
cluster.addFargateProfile('FargateProfile', {
  selectors: [{ namespace: 'default' }],
});

// Install ALB Ingress Controller
cluster.addHelmChart('ALBIngressController', {
  chart: 'aws-load-balancer-controller',
  repository: 'https://aws.github.io/eks-charts',
  namespace: 'kube-system',
});
```

---

#### 3. **building-ci-pipelines** Skill
- **Connection:** AWS CodePipeline, CodeBuild, CodeDeploy
- **Patterns:**
  - CodePipeline for CI/CD
  - CodeBuild for Docker builds
  - CodeDeploy for ECS/Lambda deployments
  - GitHub Actions → AWS (OIDC authentication)

---

#### 4. **secret-management** Skill
- **Connection:** AWS Secrets Manager, Systems Manager Parameter Store
- **Patterns:**
  - Secrets Manager for database credentials
  - Parameter Store for configuration
  - Automatic rotation with Lambda

---

#### 5. **observability** Skill
- **Connection:** CloudWatch, X-Ray
- **Patterns:**
  - CloudWatch Logs for application logging
  - CloudWatch Metrics for system metrics
  - X-Ray for distributed tracing
  - CloudWatch Alarms for alerting

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)

**Deliverables:**
- [x] Complete init.md (this document)
- [ ] Create SKILL.md main file
- [ ] Write references/compute-services.md
- [ ] Write references/database-services.md

**Content Focus:**
- Service selection frameworks
- Compute and database decision trees

---

### Phase 2: Patterns (Week 2)

**Deliverables:**
- [ ] Write references/serverless-patterns.md
- [ ] Write references/container-patterns.md
- [ ] Create examples/cdk/serverless-api/
- [ ] Create examples/terraform/serverless-api/

**Content Focus:**
- Serverless architecture patterns
- Container orchestration patterns

---

### Phase 3: Networking and Security (Week 3)

**Deliverables:**
- [ ] Write references/networking.md
- [ ] Write references/security.md
- [ ] Create examples/cdk/vpc-networking/
- [ ] Create examples/terraform/vpc-networking/

---

### Phase 4: Well-Architected (Week 4)

**Deliverables:**
- [ ] Write references/well-architected.md
- [ ] Create examples/cdk/three-tier-app/
- [ ] Create examples/terraform/ecs-fargate/

---

### Phase 5: Storage and Integration (Week 5)

**Deliverables:**
- [ ] Write references/storage-services.md
- [ ] Create examples/cdk/event-driven/
- [ ] Create scripts/cost-estimate.sh
- [ ] Create scripts/resource-audit.sh

---

### Phase 6: Polish and Testing (Week 6)

**Deliverables:**
- [ ] Cross-link with related skills
- [ ] Test all code examples
- [ ] Create CloudFormation examples
- [ ] Final review and validation

---

## Validation Checklist

### Before Creating SKILL.md

- [x] Research complete (AWS Well-Architected, service updates)
- [x] Decision frameworks designed
- [x] Service taxonomy complete
- [x] Integration points mapped

### Before Finalizing Skill

- [ ] SKILL.md under 600 lines
- [ ] All references/ files created
- [ ] All examples/ tested in AWS account
- [ ] Progressive disclosure effective
- [ ] CDK and Terraform consistency validated
- [ ] Integration with related skills verified

---

## Success Metrics

**This skill is successful if users can:**

1. **Service Selection:**
   - Choose the right compute service (Lambda/Fargate/ECS/EKS/EC2)
   - Select appropriate database service (RDS/Aurora/DynamoDB)
   - Pick optimal storage service (S3/EBS/EFS/FSx)

2. **Architecture Design:**
   - Design VPC with proper subnet segmentation
   - Implement serverless architectures
   - Build container-based microservices
   - Apply Well-Architected Framework principles

3. **Infrastructure as Code:**
   - Use CDK to define AWS resources
   - Use Terraform for AWS infrastructure
   - Understand CloudFormation basics

4. **Cost Optimization:**
   - Right-size compute resources
   - Select appropriate pricing models
   - Use storage lifecycle policies

5. **Security Implementation:**
   - Apply IAM least privilege
   - Implement encryption at rest and in transit
   - Use Secrets Manager for credentials

---

## Future Enhancements

**Potential Additions (Not in Initial Release):**

1. **Advanced Serverless**
   - Step Functions orchestration
   - EventBridge Scheduler
   - Lambda SnapStart (Java)

2. **Multi-Region Patterns**
   - Global applications
   - Disaster recovery
   - Data residency

3. **AI/ML Services**
   - SageMaker patterns
   - Bedrock integration
   - Rekognition, Textract

4. **Data Analytics**
   - Kinesis streaming
   - Glue ETL
   - Athena queries
   - Redshift data warehousing

5. **Migration Patterns**
   - On-prem → AWS
   - Monolith → Microservices
   - VM → Containers → Serverless

---

## References

**AWS Official Documentation:**
- AWS Well-Architected Framework: https://aws.amazon.com/architecture/well-architected/
- AWS CDK Documentation: https://docs.aws.amazon.com/cdk/
- AWS Service Documentation: https://docs.aws.amazon.com/

**Related Skills:**
- `infrastructure-as-code` - Multi-cloud IaC patterns
- `kubernetes-operations` - EKS operations
- `building-ci-pipelines` - AWS CodePipeline
- `secret-management` - Secrets Manager, Parameter Store
- `observability` - CloudWatch, X-Ray

---

**Document Status:** ✅ Complete
**Next Step:** Create SKILL.md from this master plan
**Owner:** AI Design Components Project
**Last Updated:** December 3, 2025
