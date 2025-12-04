# Network Architecture Skill - Master Plan

**Skill Name:** `network-architecture`
**Skill Level:** High Level (8,000-12,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Network Architecture Taxonomy](#network-architecture-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Multi-Cloud Implementations](#multi-cloud-implementations)
7. [Zero Trust Architecture Patterns](#zero-trust-architecture-patterns)
8. [Hybrid Connectivity Patterns](#hybrid-connectivity-patterns)
9. [Tool and Service Recommendations](#tool-and-service-recommendations)
10. [Skill Structure Design](#skill-structure-design)
11. [Integration Points](#integration-points)
12. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why Network Architecture Matters in 2025

Cloud network architecture has evolved from simple VPC configurations to complex, multi-cloud, zero-trust environments that span on-premises datacenters, multiple cloud providers, and edge locations. In 2025, network architecture is the foundation of cloud security, performance, and operational excellence.

**Market Drivers:**

1. **Zero Trust Mandate**: Government regulations (Federal Zero Trust Strategy) and enterprise security requirements demand "never trust, always verify" architectures
2. **Multi-Cloud Reality**: 90%+ of enterprises use multiple cloud providers, requiring unified network strategies
3. **Hybrid Cloud Permanence**: On-premises infrastructure integration is permanent, not transitional
4. **Global Distribution**: Applications must serve users worldwide with low latency
5. **Compliance Requirements**: Data sovereignty, GDPR, HIPAA require network-level controls
6. **Cost Optimization**: Network egress charges drive architectural decisions

**Strategic Value:**

- **Security Foundation**: Network segmentation is the first line of defense against lateral movement
- **Performance Enabler**: Proper network design reduces latency and increases throughput
- **Cost Control**: Smart networking reduces egress charges by 40-60%
- **Compliance Assurance**: Network-level controls satisfy regulatory requirements
- **Operational Excellence**: Well-designed networks are easier to monitor and troubleshoot

### How This Differs from Existing Solutions

**Traditional Network Documentation:**
- **Cloud-Specific**: AWS VPC docs OR GCP VPC docs, not unified patterns
- **Tactical Focus**: "How to create a subnet" vs "When to use hub-spoke vs mesh"
- **Single-Pattern**: One-size-fits-all approaches
- **Static**: Doesn't address drift, evolution, or refactoring

**Our Approach:**
- **Decision Frameworks**: When to use hub-spoke vs mesh vs transit gateway
- **Multi-Cloud Patterns**: Unified concepts across AWS, GCP, Azure
- **Zero Trust Integration**: Security-first architecture from day one
- **Operational Reality**: Addresses monitoring, drift, cost optimization
- **Migration Paths**: How to evolve from flat VPC to sophisticated architecture

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **VPC Design Patterns**
   - Flat (single VPC) architecture
   - Hub-and-spoke topology
   - Mesh networking
   - Transit Gateway patterns
   - VPC peering strategies

2. **Subnet Strategy**
   - Public, private, isolated tier design
   - CIDR block planning and IP addressing (IPAM)
   - Multi-AZ subnet distribution
   - Reserved address space planning

3. **Network Segmentation**
   - Microsegmentation patterns
   - Security group architecture
   - Network ACLs vs security groups
   - Service-to-service isolation

4. **Hybrid Connectivity**
   - VPN vs Direct Connect/ExpressRoute/Cloud Interconnect
   - Resilient hybrid architectures
   - Bandwidth and latency considerations
   - Cost optimization patterns

5. **Multi-Region Networking**
   - Cross-region VPC peering
   - Global load balancing patterns
   - Disaster recovery networking
   - Data residency and sovereignty

6. **Zero Trust Architecture**
   - Identity-based access (IAM integration)
   - Least privilege networking
   - Continuous verification patterns
   - Microsegmentation for zero trust

7. **Service Networking**
   - Private endpoints (AWS PrivateLink, Azure Private Link, GCP Private Service Connect)
   - Service mesh integration
   - API gateway networking
   - CDN and edge networking

8. **Network Observability**
   - VPC flow logs
   - Network performance monitoring
   - Traffic analysis and anomaly detection
   - Cost attribution by network path

### What This Skill Does NOT Cover

**Out of Scope (See Other Skills):**
- Kubernetes networking internals (see `kubernetes-operations`)
- Load balancer configuration details (covered in separate skill when created)
- Firewall rule specifics (covered in `security-hardening`)
- DNS record management (covered in separate skill when created)
- Infrastructure as Code syntax (see `infrastructure-as-code`)

**Boundary:**
- This skill focuses on network ARCHITECTURE and PATTERNS
- IaC skill covers HOW to implement with Terraform/Pulumi
- This skill provides WHAT and WHEN, IaC provides HOW

---

## Research Findings

### Google Search Grounding Research (December 2025)

**Query 1: Cloud Network Architecture Best Practices 2025**

**Key Findings:**
- **Well-Architected Framework**: Treat cloud provider frameworks as core operating systems
- **Automation-First**: Automate what you believe, measure what you automate, review what you measure
- **Multi-Layered Security**: Design cloud and network security using multilayered approach
- **Zero Trust Adoption**: Zero Trust is now standard, not optional
- **Centralized Connectivity**: Centralize connectivity and inspection (hub-spoke model)
- **Aggressive Segmentation**: Segment using VPCs, routing tables, and service-to-service identity
- **Sustainability Focus**: Integrate sustainability into cloud design (energy-efficient routing)

**AWS-Specific Best Practices (2025):**
- Identity-first security with ABAC and service control policies
- Multi-AZ baseline for production, multi-region for business-critical
- Prefer managed services and serverless to reduce infrastructure
- Standardize on Graviton for compute efficiency
- Centralize connectivity and inspection
- Segment aggressively using VPCs, routing tables, service-to-service identity

**Azure-Specific Best Practices (2025):**
- Hub-and-spoke network topology as standard
- Azure Virtual Network Manager for centralized IP planning (IPAM)
- Network Watcher VM troubleshooter for diagnostics
- Private endpoints for Azure services over private IP
- Private DNS Zones for private endpoint DNS resolution
- Few large VNets vs many small VNets (reduce management overhead)
- Virtual Network Peering for multi-region connectivity

**GCP-Specific Best Practices (2025):**
- Custom mode VPC networks (not auto-mode)
- Group applications into fewer subnets with larger address ranges
- Start with single VPC for resources with common requirements
- Shared VPC for multi-workgroup administration
- Grant network user role at subnet level (not VPC level)
- Limit external access and define service perimeters
- Use Dedicated Interconnect for hybrid connectivity
- Hybrid DNS with two authoritative DNS systems
- Consider IPv6 addressing early

---

**Query 2: VPC Design Patterns Hub-Spoke Transit Gateway 2025**

**Key Findings:**
- **Hub-Spoke Remains Dominant**: Transit Gateway hub-spoke model is still recommended in 2025
- **Scalability**: Easy to add new VPCs without redesigning architecture
- **Simplified Management**: Central point for routing and security policies
- **Centralized Security**: Deploy firewalls in hub to inspect spoke-to-spoke traffic
- **Multi-Account Support**: Works well with AWS Organizations

**Implementation Pattern:**
1. Deploy Transit Gateway in central AWS account
2. Attach VPCs (spokes) via VPC attachments
3. Configure route tables for inter-spoke routing
4. (Optional) Deploy inspection VPC for security

**Use Cases in 2025:**
- Multi-tenant environments (SaaS providers)
- Hybrid cloud connectivity
- Centralized egress (route all outbound through inspection VPC)
- Generative AI application isolation

**Alternatives:**
- VPC Peering: Simple pairwise connections
- VPC Lattice: Application-layer networking for microservices

---

**Query 3: Zero Trust Network Architecture Implementation 2025**

**Core Principles:**
1. **Never Trust, Always Verify**: Authenticate and authorize every request
2. **Least Privilege Access**: Grant only minimum necessary permissions
3. **Assume Breach**: Operate under assumption attackers are inside network

**Implementation Steps:**
1. **Assessment and Inventory**: List users, devices, apps, data flows
2. **Strengthen IAM**:
   - Enforce phishing-resistant MFA
   - Standardize identity controls across platforms
   - Separate user accounts from administrative accounts
3. **Network Segmentation (Microsegmentation)**: Divide network into isolated zones
4. **Continuous Monitoring**: Real-time traffic and behavior analysis
5. **Automation and AI**: Streamline monitoring and incident response

**Key Components:**
- Identity and Access Management (IAM)
- Multi-Factor Authentication (MFA)
- Endpoint Security
- Encryption (data in transit and at rest)

**Challenges and Solutions:**
- **Compatibility Issues**: Roll out in phases, start with riskiest areas
- **Resource Strain**: 24/7 monitoring requires investment
- **Operational Disruptions**: Transition causes temporary friction
- **Executive Buy-In**: Demonstrate ROI and risk reduction

**Benefits:**
- Reduced attack surface
- Minimized lateral movement
- Enhanced protection against advanced threats
- Adaptability to emerging technologies

---

**Query 4: Hybrid Cloud Network Connectivity VPN Direct Connect**

**VPN (Virtual Private Network):**
- **How it works**: Encrypted tunnel over public internet
- **Features**: IPsec with dual tunnels, BGP routing, CloudWatch monitoring
- **Throughput**: Up to ~1.25 Gbps per tunnel
- **Latency**: Dependent on public internet (variable)
- **Use Cases**: Test/dev, temporary connections, backup to primary link
- **Cost**: Low (no dedicated hardware required)
- **Setup**: Quick (no contracts)

**Accelerated VPN:**
- Leverages AWS global network for stable routing
- Use when internet connectivity is unreliable

**Direct Connect / ExpressRoute / Cloud Interconnect:**
- **How it works**: Dedicated network connection (bypasses public internet)
- **Features**: Private connectivity, consistent performance, higher bandwidth
- **Throughput**: Up to 100 Gbps (depending on connection type)
- **Latency**: Low and consistent
- **Use Cases**: Production workloads, large data transfers, real-time applications
- **Cost**: Higher (dedicated circuit fees)
- **Setup**: Slower (contracts, managed service provider coordination)

**Decision Framework:**
```
Need hybrid connectivity?
│
├─► Test/Dev/Temp? → VPN
├─► Production + Performance Critical? → Direct Connect
├─► Large Data Transfers? → Direct Connect
├─► Real-Time Applications? → Direct Connect
└─► Backup/Redundancy? → VPN as backup to Direct Connect
```

---

### Context7 Research: Terraform AWS VPC Module

**Library:** `/terraform-aws-modules/terraform-aws-vpc`
**Trust Score:** High
**Code Snippets:** 93
**Benchmark Score:** 66.9

**Key Features:**
- Multi-AZ subnet support (public, private, database, elasticache, redshift, intra)
- NAT Gateway configuration (single, per-AZ, or none)
- VPN Gateway support
- VPC endpoints (gateway and interface endpoints)
- Network ACL customization
- IPv6 support
- Outpost subnet support
- VPC Block Public Access configuration

**Example Basic VPC:**
```hcl
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "my-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = true

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}
```

**NAT Gateway Patterns:**
- Single NAT Gateway (cost-optimized, single point of failure)
- NAT Gateway per AZ (resilient, higher cost)
- External EIP allocation (consistent public IPs)

---

## Network Architecture Taxonomy

### Tier 1: Flat (Single VPC) Architecture

**Description:** All resources in a single VPC with subnet-level segmentation.

**Use When:**
- Small applications or startups
- Single environment (dev OR staging OR prod, not multiple)
- Simple security requirements
- Team < 10 engineers

**Pros:**
- Simplest to understand and manage
- No inter-VPC routing complexity
- Lowest cost (no Transit Gateway fees)
- Fast to set up

**Cons:**
- Poor isolation between workloads
- Difficult to enforce least privilege
- CIDR exhaustion risks
- Hard to scale as organization grows
- Blast radius is entire VPC

**Architecture Diagram:**
```
┌─────────────────────────────────────────────────────┐
│                    VPC 10.0.0.0/16                  │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │   Public     │  │   Private    │  │ Database │ │
│  │   Subnet     │  │   Subnet     │  │  Subnet  │ │
│  │ 10.0.1.0/24  │  │ 10.0.10.0/24 │  │10.0.20./24│ │
│  │              │  │              │  │          │ │
│  │ ┌─────────┐ │  │ ┌─────────┐  │  │ ┌──────┐ │ │
│  │ │   ALB   │ │  │ │   ECS   │  │  │ │  RDS │ │ │
│  │ └─────────┘ │  │ └─────────┘  │  │ └──────┘ │ │
│  └──────────────┘  └──────────────┘  └──────────┘ │
│                                                     │
│  Internet Gateway          NAT Gateway             │
└─────────────────────────────────────────────────────┘
```

**Implementation (AWS):**
```hcl
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "app-vpc"
  cidr = "10.0.0.0/16"

  azs              = ["us-east-1a", "us-east-1b", "us-east-1c"]
  public_subnets   = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets  = ["10.0.10.0/24", "10.0.11.0/24", "10.0.12.0/24"]
  database_subnets = ["10.0.20.0/24", "10.0.21.0/24", "10.0.22.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway   = false  # NAT per AZ for resilience
  enable_dns_hostnames = true

  tags = {
    Architecture = "flat"
    Environment  = "dev"
  }
}
```

---

### Tier 2: Multi-VPC (Isolated) Architecture

**Description:** Separate VPCs per environment or workload with no direct connectivity.

**Use When:**
- Multiple environments (dev, staging, prod)
- Strong isolation requirements
- Different teams managing different VPCs
- Compliance requires network-level separation

**Pros:**
- Strong blast radius containment
- Independent CIDR ranges (no overlap concerns)
- Clear security boundaries
- Easy cost allocation per VPC

**Cons:**
- No cross-VPC communication without explicit setup
- Management overhead (multiple VPCs)
- Duplicate infrastructure (NAT, endpoints)
- Higher costs

**Architecture Diagram:**
```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   Dev VPC       │  │  Staging VPC    │  │   Prod VPC      │
│  10.0.0.0/16    │  │  10.1.0.0/16    │  │  10.2.0.0/16    │
│                 │  │                 │  │                 │
│  ┌───────────┐  │  │  ┌───────────┐  │  │  ┌───────────┐  │
│  │  Subnets  │  │  │  │  Subnets  │  │  │  │  Subnets  │  │
│  │  + Apps   │  │  │  │  + Apps   │  │  │  │  + Apps   │  │
│  └───────────┘  │  │  └───────────┘  │  │  └───────────┘  │
│                 │  │                 │  │                 │
│  IGW + NAT      │  │  IGW + NAT      │  │  IGW + NAT      │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                    │                    │
         └────────────────────┴────────────────────┘
                        Internet
```

**No direct connectivity between VPCs**

---

### Tier 3: Hub-and-Spoke (Transit Gateway) Architecture

**Description:** Central hub VPC/Transit Gateway with spoke VPCs connecting to it. All inter-VPC traffic routes through the hub.

**Use When:**
- 5+ VPCs need to communicate
- Centralized security inspection required
- Hybrid connectivity (on-premises to multiple VPCs)
- Multi-account AWS Organizations setup
- Need for network-level segmentation and policy

**Pros:**
- Simplified routing (spokes only connect to hub)
- Centralized security inspection (firewall in hub)
- Scales easily (add spokes without redesigning)
- Works with AWS Resource Access Manager (RAM) for multi-account
- Centralized hybrid connectivity (single Direct Connect to hub)

**Cons:**
- Transit Gateway costs (~$0.05/hour + $0.02/GB)
- Increased latency (traffic hairpins through hub)
- Hub becomes single point of failure (mitigate with multi-AZ TGW)
- More complex than simple peering

**Architecture Diagram:**
```
                         On-Premises
                              │
                          VPN / DX
                              │
                              ▼
                   ┌─────────────────────┐
                   │   Transit Gateway   │
                   │   (Hub)            │
                   └─────────────────────┘
                     │      │       │
            ┌────────┘      │       └────────┐
            │               │                │
            ▼               ▼                ▼
     ┌───────────┐   ┌───────────┐   ┌───────────┐
     │  Prod VPC │   │  Dev VPC  │   │ Shared    │
     │  (Spoke)  │   │  (Spoke)  │   │ Services  │
     │           │   │           │   │ (Spoke)   │
     └───────────┘   └───────────┘   └───────────┘
```

**Routing Flow:**
- Spoke-to-Spoke: VPC-A → TGW → VPC-B
- Spoke-to-On-Prem: VPC-A → TGW → VPN/DX → On-Prem
- Centralized Egress: VPC-A → TGW → Egress VPC → Internet

**Implementation (AWS):**
```hcl
# Transit Gateway
resource "aws_ec2_transit_gateway" "main" {
  description                     = "Main TGW for hub-spoke"
  amazon_side_asn                 = 64512
  default_route_table_association = "enable"
  default_route_table_propagation = "enable"
  dns_support                     = "enable"
  vpn_ecmp_support               = "enable"

  tags = {
    Name = "main-tgw"
  }
}

# Spoke VPC Attachment
resource "aws_ec2_transit_gateway_vpc_attachment" "spoke_prod" {
  transit_gateway_id = aws_ec2_transit_gateway.main.id
  vpc_id             = module.vpc_prod.vpc_id
  subnet_ids         = module.vpc_prod.private_subnets

  dns_support = "enable"

  tags = {
    Name = "prod-vpc-attachment"
  }
}

# TGW Route Table
resource "aws_ec2_transit_gateway_route_table" "main" {
  transit_gateway_id = aws_ec2_transit_gateway.main.id

  tags = {
    Name = "main-tgw-rt"
  }
}

# Route: Spoke to Spoke
resource "aws_ec2_transit_gateway_route" "spoke_to_spoke" {
  destination_cidr_block         = "10.1.0.0/16"  # Dev VPC CIDR
  transit_gateway_attachment_id  = aws_ec2_transit_gateway_vpc_attachment.spoke_prod.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.main.id
}
```

**Advanced: Inspection VPC Pattern**
```
                   ┌─────────────────────┐
                   │  Transit Gateway    │
                   └─────────────────────┘
                     │      │       │
            ┌────────┘      │       └────────┐
            │               │                │
            ▼               ▼                ▼
     ┌───────────┐   ┌───────────┐   ┌───────────┐
     │  Prod VPC │   │Inspection │   │  Dev VPC  │
     │           │   │    VPC    │   │           │
     │           │   │  ┌──────┐ │   │           │
     │           │   │  │Firewall│   │           │
     │           │   │  └──────┘ │   │           │
     └───────────┘   └───────────┘   └───────────┘
```

All spoke-to-spoke traffic routes through Inspection VPC firewall.

---

### Tier 4: Full Mesh (VPC Peering) Architecture

**Description:** Every VPC directly connected to every other VPC via VPC peering connections.

**Use When:**
- Small number of VPCs (< 5)
- Low latency required (no hub hop)
- No centralized inspection needed
- Cost optimization (no Transit Gateway fees)

**Pros:**
- Lowest latency (direct VPC-to-VPC)
- No Transit Gateway costs
- Simple for small number of VPCs

**Cons:**
- Management complexity scales as O(n²) - n VPCs require n(n-1)/2 peering connections
- No centralized security inspection
- Difficult to add new VPCs
- Route table management becomes unwieldy
- Does not scale beyond ~10 VPCs

**Architecture Diagram:**
```
           ┌───────────┐
           │  VPC-A    │
           └───────────┘
              /  |  \
             /   |   \
            /    |    \
           /     |     \
    ┌─────┐  ┌─────┐  ┌─────┐
    │VPC-B│──│VPC-C│──│VPC-D│
    └─────┘  └─────┘  └─────┘
       │        │        │
       └────────┼────────┘
                │
           ┌─────────┐
           │  VPC-E  │
           └─────────┘
```

For 5 VPCs: 10 peering connections required

**Implementation (AWS):**
```hcl
# VPC Peering Connection
resource "aws_vpc_peering_connection" "prod_to_dev" {
  vpc_id      = module.vpc_prod.vpc_id
  peer_vpc_id = module.vpc_dev.vpc_id
  auto_accept = true

  tags = {
    Name = "prod-to-dev-peering"
  }
}

# Accept the peering connection
resource "aws_vpc_peering_connection_accepter" "prod_to_dev" {
  vpc_peering_connection_id = aws_vpc_peering_connection.prod_to_dev.id
  auto_accept               = true
}

# Routes in Prod VPC to reach Dev VPC
resource "aws_route" "prod_to_dev" {
  count = length(module.vpc_prod.private_route_table_ids)

  route_table_id            = module.vpc_prod.private_route_table_ids[count.index]
  destination_cidr_block    = module.vpc_dev.vpc_cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.prod_to_dev.id
}

# Routes in Dev VPC to reach Prod VPC
resource "aws_route" "dev_to_prod" {
  count = length(module.vpc_dev.private_route_table_ids)

  route_table_id            = module.vpc_dev.private_route_table_ids[count.index]
  destination_cidr_block    = module.vpc_prod.vpc_cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.prod_to_dev.id
}
```

**Scaling Issue Example:**
- 3 VPCs = 3 peering connections
- 5 VPCs = 10 peering connections
- 10 VPCs = 45 peering connections
- 20 VPCs = 190 peering connections

---

### Tier 5: Hybrid (Multi-Pattern) Architecture

**Description:** Combination of patterns based on workload requirements. Common: Hub-spoke for most VPCs + direct peering for latency-sensitive pairs.

**Use When:**
- Large enterprise with diverse requirements
- Some workloads need low latency (direct peering)
- Other workloads need centralized inspection (hub-spoke)
- Balancing cost, performance, and security

**Architecture Diagram:**
```
                   ┌─────────────────────┐
                   │  Transit Gateway    │
                   │      (Hub)          │
                   └─────────────────────┘
                     │      │       │
            ┌────────┘      │       └────────┐
            │               │                │
            ▼               ▼                ▼
     ┌───────────┐   ┌───────────┐   ┌───────────┐
     │  Prod VPC │◄──┤  Dev VPC  │   │ Shared    │
     │           │   │           │   │ Services  │
     └───────────┘   └───────────┘   └───────────┘
          ▲                                 │
          │          VPC Peering            │
          └─────────────────────────────────┘
           (Low-latency path for specific traffic)
```

**Use Cases:**
- Prod ↔ Shared Services: Low-latency direct peering
- Dev → Prod: Routed through TGW for inspection
- All → On-Prem: Routed through TGW

---

## Decision Frameworks

### Framework 1: Which Network Pattern?

```
START: Designing network architecture for cloud environment
│
├─► Number of VPCs/VNets?
│   │
│   ├─► 1 VPC
│   │   └─► Use: FLAT (Single VPC) Architecture
│   │       └─► Segment with subnets + security groups
│   │
│   ├─► 2-4 VPCs + No inter-VPC communication needed?
│   │   └─► Use: MULTI-VPC (Isolated) Architecture
│   │       └─► Separate environments, strong isolation
│   │
│   ├─► 2-5 VPCs + Frequent inter-VPC communication + Low latency critical?
│   │   └─► Use: FULL MESH (VPC Peering) Architecture
│   │       └─► Warning: Doesn't scale beyond ~10 VPCs
│   │
│   ├─► 5+ VPCs + Need centralized inspection/security?
│   │   └─► Use: HUB-AND-SPOKE (Transit Gateway) Architecture
│   │       └─► Scales to 100+ VPCs
│   │
│   └─► 10+ VPCs + Mixed requirements (some need low latency)?
│       └─► Use: HYBRID (Multi-Pattern) Architecture
│           └─► Hub-spoke base + direct peering for latency-sensitive pairs
│
└─► Additional Considerations:
    │
    ├─► Hybrid connectivity (on-prem) required?
    │   └─► YES → Hub-and-Spoke preferred (single hybrid connection point)
    │
    ├─► Centralized egress/inspection required?
    │   └─► YES → Hub-and-Spoke with Inspection VPC
    │
    ├─► Multi-account environment?
    │   └─► YES → Hub-and-Spoke with AWS RAM sharing
    │
    └─► Cost optimization priority?
        └─► Flat or Multi-VPC (avoid Transit Gateway fees)
```

---

### Framework 2: Subnet Strategy Design

```
Designing subnet layout for VPC/VNet
│
├─► Application Tier Requirements?
│   │
│   ├─► Public-facing tier (ALB, API Gateway, Bastion)
│   │   └─► Public Subnets (route to IGW)
│   │       └─► CIDR: Use smallest acceptable (e.g., /27 for 32 IPs)
│   │
│   ├─► Application/Compute tier (ECS, EKS, EC2)
│   │   └─► Private Subnets (route to NAT Gateway)
│   │       └─► CIDR: Size for expected instance count + 50% growth
│   │
│   ├─► Database tier (RDS, DynamoDB endpoints, ElastiCache)
│   │   └─► Database Subnets (no direct internet, no NAT)
│   │       └─► CIDR: Smaller than app tier (fewer IPs needed)
│   │
│   └─► Isolated tier (VPC endpoints, Lambda in VPC)
│       └─► Isolated Subnets (no internet route)
│           └─► CIDR: Minimal sizing
│
├─► Multi-AZ Requirements?
│   │
│   ├─► Production workload?
│   │   └─► YES → Distribute each tier across 3 AZs minimum
│   │       └─► Example: public-subnet-1a, 1b, 1c
│   │
│   └─► Dev/Test workload?
│       └─► 1-2 AZs acceptable for cost savings
│
├─► CIDR Block Planning
│   │
│   ├─► VPC CIDR: /16 (65,536 IPs) for large environments
│   ├─► VPC CIDR: /20 (4,096 IPs) for medium environments
│   ├─► VPC CIDR: /24 (256 IPs) for small/dev environments
│   │
│   ├─► Public Subnets: /24 or /27 (256 or 32 IPs)
│   ├─► Private Subnets: /20 to /22 (4,096 to 1,024 IPs)
│   └─► Database Subnets: /24 to /26 (256 to 64 IPs)
│
└─► IP Address Management (IPAM)
    │
    ├─► Multi-VPC environment?
    │   └─► YES → Use non-overlapping CIDR ranges
    │       └─► Example: 10.0.0.0/16, 10.1.0.0/16, 10.2.0.0/16
    │
    └─► Hybrid connectivity?
        └─► YES → Coordinate with on-prem network team
            └─► Ensure no overlap with on-prem CIDRs
```

**Example Subnet Layout (Production VPC):**

```
VPC: 10.0.0.0/16 (65,536 IPs)

┌─ Public Subnets (256 IPs total, 3 AZs)
│  ├─ 10.0.1.0/26  (64 IPs)  - us-east-1a
│  ├─ 10.0.1.64/26 (64 IPs)  - us-east-1b
│  └─ 10.0.1.128/26 (64 IPs) - us-east-1c
│
┌─ Private Subnets (12,288 IPs total, 3 AZs)
│  ├─ 10.0.16.0/20  (4,096 IPs) - us-east-1a
│  ├─ 10.0.32.0/20  (4,096 IPs) - us-east-1b
│  └─ 10.0.48.0/20  (4,096 IPs) - us-east-1c
│
┌─ Database Subnets (768 IPs total, 3 AZs)
│  ├─ 10.0.64.0/24 (256 IPs) - us-east-1a
│  ├─ 10.0.65.0/24 (256 IPs) - us-east-1b
│  └─ 10.0.66.0/24 (256 IPs) - us-east-1c
│
└─ Reserved (future expansion)
   └─ 10.0.128.0/17 (32,768 IPs)
```

---

### Framework 3: NAT Gateway Strategy

```
Designing NAT Gateway configuration for private subnets
│
├─► Cost Optimization vs Resilience?
│   │
│   ├─► Cost Priority (Development/Test)
│   │   └─► Single NAT Gateway
│   │       ├─ Cost: ~$32/month + data transfer
│   │       ├─ Risk: Single point of failure
│   │       └─ Use Case: Dev, test, non-critical workloads
│   │
│   ├─► Balanced (Most Production)
│   │   └─► One NAT Gateway per AZ
│   │       ├─ Cost: ~$96/month (3 AZs) + data transfer
│   │       ├─ Resilience: AZ failure doesn't break connectivity
│   │       └─ Use Case: Standard production workloads
│   │
│   └─► Maximum Resilience
│       └─► Multiple NAT Gateways per AZ + monitoring
│           ├─ Cost: Higher
│           ├─ Resilience: NAT Gateway failure auto-recovers
│           └─ Use Case: Critical workloads, SLA-dependent
│
├─► External IP Requirements?
│   │
│   ├─► Consistent public IPs needed (e.g., third-party IP whitelisting)?
│   │   └─► Pre-allocate Elastic IPs
│   │       └─► Associate with NAT Gateways
│   │           └─► IPs remain consistent across recreations
│   │
│   └─► No external IP requirements?
│       └─► Use auto-assigned NAT Gateway IPs
│
├─► Internet Access Patterns?
│   │
│   ├─► No outbound internet needed?
│   │   └─► NO NAT Gateway (cost savings)
│   │       └─► Use VPC Endpoints for AWS service access
│   │
│   ├─► Minimal outbound (package updates, API calls)?
│   │   └─► NAT Gateway standard configuration
│   │
│   └─► High outbound traffic (data transfers, streaming)?
│       └─► Consider NAT Instance (cost optimization)
│           └─► Or centralized egress VPC pattern
│
└─► Alternative: Centralized Egress Pattern
    └─► Hub-and-Spoke: Single egress VPC with NAT
        ├─ Spokes route internet traffic to egress VPC
        ├─ Cost: Reduce NAT Gateway count
        └─ Benefit: Centralized logging, inspection, control
```

**Cost Comparison Example (3 AZs):**

| Pattern | NAT Gateways | Monthly Cost | Resilience |
|---------|--------------|--------------|------------|
| Single NAT | 1 | ~$32 | Low |
| NAT per AZ | 3 | ~$96 | High |
| Centralized Egress | 1-3 (in hub) | ~$32-96 | Medium-High |

*Note: Add ~$0.045/GB data transfer costs*

---

### Framework 4: Security Group vs Network ACL

```
Implementing network security controls
│
├─► Security Groups (Stateful, Instance-Level)
│   │
│   ├─► Use For:
│   │   ├─ Instance-level security (EC2, RDS, ECS tasks)
│   │   ├─ Service-to-service communication rules
│   │   ├─ Dynamic rule sets (reference other SGs)
│   │   └─ Most common use case
│   │
│   ├─► Characteristics:
│   │   ├─ Stateful (return traffic auto-allowed)
│   │   ├─ Allow rules only (implicit deny)
│   │   ├─ Evaluates all rules before decision
│   │   └─ Associated with ENIs
│   │
│   └─► Best Practices:
│       ├─ Use descriptive names (app-alb-sg, app-backend-sg)
│       ├─ Reference other SGs instead of CIDR blocks
│       ├─ Keep rules minimal and specific
│       └─ Use tags for management
│
└─► Network ACLs (Stateless, Subnet-Level)
    │
    ├─► Use For:
    │   ├─ Subnet-level coarse-grained filtering
    │   ├─ Explicit deny rules (block specific IPs)
    │   ├─ Compliance requirements (defense in depth)
    │   └─ Additional layer beyond security groups
    │
    ├─► Characteristics:
    │   ├─ Stateless (must allow both request and response)
    │   ├─ Allow and Deny rules
    │   ├─ Processes rules in order (lowest number first)
    │   └─ Associated with subnets
    │
    └─► Best Practices:
        ├─ Use sparingly (complex to manage)
        ├─ Start with rule 100, increment by 100
        ├─ Remember to allow ephemeral ports (1024-65535)
        └─ Test thoroughly (stateless nature causes issues)
```

**Decision Matrix:**

| Requirement | Security Group | Network ACL |
|-------------|----------------|-------------|
| Block specific IP | No | Yes (deny rule) |
| Instance-level control | Yes | No (subnet-level) |
| Stateful filtering | Yes | No |
| Reference other SGs | Yes | No |
| Order-dependent rules | No | Yes |
| Default recommendation | Yes | Only if needed |

**Example: Security Group Architecture**

```
┌───────────────────────────────────────────────────┐
│                  VPC                              │
│                                                   │
│  ┌─────────────────────────────────────────┐    │
│  │  ALB Security Group (alb-sg)            │    │
│  │  Ingress: 0.0.0.0/0:443 (HTTPS)         │    │
│  └─────────────────────────────────────────┘    │
│                      │                           │
│                      ▼                           │
│  ┌─────────────────────────────────────────┐    │
│  │  Backend Security Group (backend-sg)    │    │
│  │  Ingress: [alb-sg]:8080 (from ALB only) │    │
│  └─────────────────────────────────────────┘    │
│                      │                           │
│                      ▼                           │
│  ┌─────────────────────────────────────────┐    │
│  │  Database Security Group (db-sg)        │    │
│  │  Ingress: [backend-sg]:5432 (from BE)   │    │
│  └─────────────────────────────────────────┘    │
│                                                   │
└───────────────────────────────────────────────────┘
```

---

## Multi-Cloud Implementations

### AWS Network Architecture Patterns

#### Pattern 1: AWS Standard Multi-Tier VPC

**Topology:** Public + Private + Database subnets across 3 AZs

```hcl
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "production-vpc"
  cidr = "10.0.0.0/16"

  azs              = ["us-east-1a", "us-east-1b", "us-east-1c"]
  public_subnets   = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets  = ["10.0.10.0/20", "10.0.26.0/20", "10.0.42.0/20"]
  database_subnets = ["10.0.64.0/24", "10.0.65.0/24", "10.0.66.0/24"]

  # NAT Gateway per AZ for resilience
  enable_nat_gateway   = true
  single_nat_gateway   = false
  one_nat_gateway_per_az = true

  # DNS
  enable_dns_hostnames = true
  enable_dns_support   = true

  # VPC Endpoints (cost optimization - avoid NAT charges)
  enable_s3_endpoint       = true
  enable_dynamodb_endpoint = true

  tags = {
    Terraform   = "true"
    Environment = "production"
  }
}

# VPC Flow Logs
resource "aws_flow_log" "vpc" {
  iam_role_arn    = aws_iam_role.vpc_flow_log.arn
  log_destination = aws_cloudwatch_log_group.vpc_flow_log.arn
  traffic_type    = "ALL"
  vpc_id          = module.vpc.vpc_id
}
```

**Service-Specific Subnets:**
```hcl
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  # ... basic config ...

  # ElastiCache subnets
  elasticache_subnets = ["10.0.80.0/24", "10.0.81.0/24", "10.0.82.0/24"]
  create_elasticache_subnet_group = true

  # Redshift subnets
  redshift_subnets = ["10.0.90.0/24", "10.0.91.0/24", "10.0.92.0/24"]
  create_redshift_subnet_group = true

  # Intra subnets (no internet, for VPC endpoints)
  intra_subnets = ["10.0.100.0/24", "10.0.101.0/24", "10.0.102.0/24"]
}
```

#### Pattern 2: AWS Transit Gateway Hub-Spoke

```hcl
# Transit Gateway
resource "aws_ec2_transit_gateway" "main" {
  description                     = "Main hub for multi-VPC connectivity"
  amazon_side_asn                 = 64512
  default_route_table_association = "disable"  # Custom route tables
  default_route_table_propagation = "disable"
  dns_support                     = "enable"
  vpn_ecmp_support               = "enable"

  tags = {
    Name = "main-tgw"
  }
}

# Spoke VPCs
module "vpc_prod" {
  source = "terraform-aws-modules/vpc/aws"
  name   = "prod"
  cidr   = "10.0.0.0/16"
  # ... subnet config ...
}

module "vpc_dev" {
  source = "terraform-aws-modules/vpc/aws"
  name   = "dev"
  cidr   = "10.1.0.0/16"
  # ... subnet config ...
}

module "vpc_shared" {
  source = "terraform-aws-modules/vpc/aws"
  name   = "shared-services"
  cidr   = "10.2.0.0/16"
  # ... subnet config ...
}

# TGW Attachments
resource "aws_ec2_transit_gateway_vpc_attachment" "prod" {
  transit_gateway_id = aws_ec2_transit_gateway.main.id
  vpc_id             = module.vpc_prod.vpc_id
  subnet_ids         = module.vpc_prod.private_subnets

  transit_gateway_default_route_table_association = false
  transit_gateway_default_route_table_propagation = false

  tags = {
    Name = "prod-tgw-attachment"
  }
}

resource "aws_ec2_transit_gateway_vpc_attachment" "dev" {
  transit_gateway_id = aws_ec2_transit_gateway.main.id
  vpc_id             = module.vpc_dev.vpc_id
  subnet_ids         = module.vpc_dev.private_subnets

  transit_gateway_default_route_table_association = false
  transit_gateway_default_route_table_propagation = false

  tags = {
    Name = "dev-tgw-attachment"
  }
}

# TGW Route Tables
resource "aws_ec2_transit_gateway_route_table" "prod" {
  transit_gateway_id = aws_ec2_transit_gateway.main.id

  tags = {
    Name = "prod-tgw-rt"
  }
}

resource "aws_ec2_transit_gateway_route_table" "dev" {
  transit_gateway_id = aws_ec2_transit_gateway.main.id

  tags = {
    Name = "dev-tgw-rt"
  }
}

# Route Table Associations
resource "aws_ec2_transit_gateway_route_table_association" "prod" {
  transit_gateway_attachment_id  = aws_ec2_transit_gateway_vpc_attachment.prod.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.prod.id
}

# Routes: Prod can reach Shared Services
resource "aws_ec2_transit_gateway_route" "prod_to_shared" {
  destination_cidr_block         = module.vpc_shared.vpc_cidr_block
  transit_gateway_attachment_id  = aws_ec2_transit_gateway_vpc_attachment.shared.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.prod.id
}

# VPC Routes: Route to TGW
resource "aws_route" "prod_private_to_tgw" {
  count = length(module.vpc_prod.private_route_table_ids)

  route_table_id         = module.vpc_prod.private_route_table_ids[count.index]
  destination_cidr_block = "10.0.0.0/8"  # All RFC1918 traffic to TGW
  transit_gateway_id     = aws_ec2_transit_gateway.main.id
}
```

#### Pattern 3: AWS PrivateLink (VPC Endpoints)

```hcl
# Interface Endpoint (for AWS services)
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = module.vpc.vpc_id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Interface"

  subnet_ids         = module.vpc.intra_subnets
  security_group_ids = [aws_security_group.vpc_endpoints.id]

  private_dns_enabled = true

  tags = {
    Name = "s3-vpc-endpoint"
  }
}

# Gateway Endpoint (S3 and DynamoDB)
resource "aws_vpc_endpoint" "s3_gateway" {
  vpc_id            = module.vpc.vpc_id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"

  route_table_ids = concat(
    module.vpc.private_route_table_ids,
    module.vpc.database_route_table_ids
  )

  tags = {
    Name = "s3-gateway-endpoint"
  }
}

# Security Group for VPC Endpoints
resource "aws_security_group" "vpc_endpoints" {
  name        = "vpc-endpoints-sg"
  description = "Security group for VPC endpoints"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [module.vpc.vpc_cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

---

### GCP Network Architecture Patterns

#### Pattern 1: GCP Custom VPC with Shared VPC

```hcl
# Custom Mode VPC (recommended over auto-mode)
resource "google_compute_network" "main" {
  name                    = "main-vpc"
  auto_create_subnetworks = false  # Custom subnets
  routing_mode            = "GLOBAL"
  description             = "Main production VPC"
}

# Subnets (Regional)
resource "google_compute_subnetwork" "us_private" {
  name          = "us-private-subnet"
  ip_cidr_range = "10.0.0.0/20"
  region        = "us-central1"
  network       = google_compute_network.main.id

  # Secondary ranges for GKE pods and services
  secondary_ip_range {
    range_name    = "gke-pods"
    ip_cidr_range = "10.1.0.0/16"
  }

  secondary_ip_range {
    range_name    = "gke-services"
    ip_cidr_range = "10.2.0.0/20"
  }

  private_ip_google_access = true  # Access to Google APIs without external IP
}

resource "google_compute_subnetwork" "us_public" {
  name          = "us-public-subnet"
  ip_cidr_range = "10.0.16.0/24"
  region        = "us-central1"
  network       = google_compute_network.main.id
}

# Cloud Router (for Cloud NAT)
resource "google_compute_router" "main" {
  name    = "main-router"
  region  = google_compute_subnetwork.us_private.region
  network = google_compute_network.main.id

  bgp {
    asn = 64514
  }
}

# Cloud NAT
resource "google_compute_router_nat" "main" {
  name                               = "main-nat"
  router                             = google_compute_router.main.name
  region                             = google_compute_router.main.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

# Firewall Rules
resource "google_compute_firewall" "allow_internal" {
  name    = "allow-internal"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "udp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "icmp"
  }

  source_ranges = ["10.0.0.0/8"]
}

resource "google_compute_firewall" "allow_ssh_iap" {
  name    = "allow-ssh-iap"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["35.235.240.0/20"]  # IAP CIDR range
}
```

#### Pattern 2: GCP Shared VPC (Multi-Project)

```hcl
# Host Project (owns the VPC)
resource "google_compute_shared_vpc_host_project" "host" {
  project = "host-project-id"
}

# Shared VPC Network
resource "google_compute_network" "shared" {
  name                    = "shared-vpc"
  auto_create_subnetworks = false
  project                 = google_compute_shared_vpc_host_project.host.project
}

# Subnet for Service Project A
resource "google_compute_subnetwork" "service_a" {
  name          = "service-a-subnet"
  ip_cidr_range = "10.0.0.0/20"
  region        = "us-central1"
  network       = google_compute_network.shared.id
  project       = google_compute_shared_vpc_host_project.host.project
}

# Attach Service Project to Shared VPC
resource "google_compute_shared_vpc_service_project" "service_a" {
  host_project    = google_compute_shared_vpc_host_project.host.project
  service_project = "service-a-project-id"
}

# Grant network user role to service project's compute service account
resource "google_project_iam_member" "service_a_network_user" {
  project = google_compute_shared_vpc_host_project.host.project
  role    = "roles/compute.networkUser"
  member  = "serviceAccount:service-a-compute@developer.gserviceaccount.com"
}
```

#### Pattern 3: GCP Private Service Connect

```hcl
# Private Service Connect for accessing Google APIs
resource "google_compute_global_address" "private_service_connect" {
  name          = "psc-address"
  purpose       = "PRIVATE_SERVICE_CONNECT"
  address_type  = "INTERNAL"
  address       = "10.3.0.5"
  network       = google_compute_network.main.id
}

resource "google_compute_global_forwarding_rule" "psc" {
  name                  = "psc-forwarding-rule"
  target                = "all-apis"
  network               = google_compute_network.main.id
  ip_address            = google_compute_global_address.private_service_connect.id
  load_balancing_scheme = ""
}
```

---

### Azure Network Architecture Patterns

#### Pattern 1: Azure Hub-Spoke Topology

```hcl
# Hub VNet
resource "azurerm_virtual_network" "hub" {
  name                = "hub-vnet"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.0.0.0/16"]

  tags = {
    Environment = "Production"
    Topology    = "Hub"
  }
}

# Hub Subnets
resource "azurerm_subnet" "hub_firewall" {
  name                 = "AzureFirewallSubnet"  # Fixed name for Azure Firewall
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_subnet" "hub_gateway" {
  name                 = "GatewaySubnet"  # Fixed name for VPN Gateway
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_subnet" "hub_bastion" {
  name                 = "AzureBastionSubnet"  # Fixed name for Bastion
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.0.3.0/24"]
}

# Spoke VNet (Production)
resource "azurerm_virtual_network" "spoke_prod" {
  name                = "prod-vnet"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.1.0.0/16"]

  tags = {
    Environment = "Production"
    Topology    = "Spoke"
  }
}

# Spoke Subnets
resource "azurerm_subnet" "spoke_prod_web" {
  name                 = "web-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.spoke_prod.name
  address_prefixes     = ["10.1.1.0/24"]
}

resource "azurerm_subnet" "spoke_prod_app" {
  name                 = "app-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.spoke_prod.name
  address_prefixes     = ["10.1.10.0/23"]
}

# VNet Peering: Hub → Spoke
resource "azurerm_virtual_network_peering" "hub_to_spoke_prod" {
  name                         = "hub-to-prod"
  resource_group_name          = azurerm_resource_group.main.name
  virtual_network_name         = azurerm_virtual_network.hub.name
  remote_virtual_network_id    = azurerm_virtual_network.spoke_prod.id
  allow_virtual_network_access = true
  allow_forwarded_traffic      = true  # Allow spoke to use hub's gateway
  allow_gateway_transit        = true  # Hub provides gateway
}

# VNet Peering: Spoke → Hub
resource "azurerm_virtual_network_peering" "spoke_prod_to_hub" {
  name                         = "prod-to-hub"
  resource_group_name          = azurerm_resource_group.main.name
  virtual_network_name         = azurerm_virtual_network.spoke_prod.name
  remote_virtual_network_id    = azurerm_virtual_network.hub.id
  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
  use_remote_gateways          = true  # Use hub's gateway
}

# Azure Firewall in Hub
resource "azurerm_public_ip" "firewall" {
  name                = "firewall-pip"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_firewall" "hub" {
  name                = "hub-firewall"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku_name            = "AZFW_VNet"
  sku_tier            = "Standard"

  ip_configuration {
    name                 = "configuration"
    subnet_id            = azurerm_subnet.hub_firewall.id
    public_ip_address_id = azurerm_public_ip.firewall.id
  }
}

# Route Table: Force spoke traffic through firewall
resource "azurerm_route_table" "spoke_prod" {
  name                = "prod-route-table"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  route {
    name                   = "to-internet-via-firewall"
    address_prefix         = "0.0.0.0/0"
    next_hop_type          = "VirtualAppliance"
    next_hop_in_ip_address = azurerm_firewall.hub.ip_configuration[0].private_ip_address
  }
}

resource "azurerm_subnet_route_table_association" "spoke_prod_app" {
  subnet_id      = azurerm_subnet.spoke_prod_app.id
  route_table_id = azurerm_route_table.spoke_prod.id
}
```

#### Pattern 2: Azure Private Endpoints

```hcl
# Private Endpoint for Storage Account
resource "azurerm_private_endpoint" "storage" {
  name                = "storage-private-endpoint"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.spoke_prod_app.id

  private_service_connection {
    name                           = "storage-privateserviceconnection"
    private_connection_resource_id = azurerm_storage_account.main.id
    subresource_names              = ["blob"]
    is_manual_connection           = false
  }
}

# Private DNS Zone for Storage
resource "azurerm_private_dns_zone" "storage" {
  name                = "privatelink.blob.core.windows.net"
  resource_group_name = azurerm_resource_group.main.name
}

# Link DNS Zone to VNet
resource "azurerm_private_dns_zone_virtual_network_link" "storage" {
  name                  = "storage-dns-link"
  resource_group_name   = azurerm_resource_group.main.name
  private_dns_zone_name = azurerm_private_dns_zone.storage.name
  virtual_network_id    = azurerm_virtual_network.spoke_prod.id
}

# DNS A Record for Private Endpoint
resource "azurerm_private_dns_a_record" "storage" {
  name                = azurerm_storage_account.main.name
  zone_name           = azurerm_private_dns_zone.storage.name
  resource_group_name = azurerm_resource_group.main.name
  ttl                 = 300
  records             = [azurerm_private_endpoint.storage.private_service_connection[0].private_ip_address]
}
```

---

## Zero Trust Architecture Patterns

### Zero Trust Core Principles (2025)

**Principle 1: Never Trust, Always Verify**
- Authenticate every request, regardless of source
- Verify identity AND device health
- No implicit trust based on network location

**Principle 2: Least Privilege Access**
- Grant minimum necessary permissions
- Time-bound access (just-in-time)
- Continuous authorization

**Principle 3: Assume Breach**
- Segment network aggressively
- Monitor all traffic
- Rapid detection and response

### Zero Trust Network Architecture Patterns

#### Pattern 1: Microsegmentation with Security Groups

**Concept:** Isolate every workload with granular security group rules.

```
Traditional Network (Large Blast Radius):
┌────────────────────────────────────────────────┐
│              DMZ (0.0.0.0/0 allowed)           │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  │ App1│ │ App2│ │ App3│ │ App4│ │ App5│     │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘     │
│   All apps can talk to each other              │
└────────────────────────────────────────────────┘

Zero Trust (Microsegmentation):
┌────────────────────────────────────────────────┐
│         Microsegmented Environment             │
│  ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐       │
│  │App1 │──►│App2 │   │App3 │──►│App4 │       │
│  │[SG1]│   │[SG2]│   │[SG3]│   │[SG4]│       │
│  └─────┘   └─────┘   └─────┘   └─────┘       │
│    Only App1→App2 and App3→App4 allowed       │
└────────────────────────────────────────────────┘
```

**Implementation (AWS):**
```hcl
# Frontend Service
resource "aws_security_group" "frontend" {
  name        = "frontend-sg"
  description = "Frontend service security group"
  vpc_id      = module.vpc.vpc_id

  # Only accept traffic from ALB
  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    description     = "Allow traffic from ALB only"
  }

  # Only send traffic to backend
  egress {
    from_port       = 8081
    to_port         = 8081
    protocol        = "tcp"
    security_groups = [aws_security_group.backend.id]
    description     = "Allow traffic to backend only"
  }

  tags = {
    Name        = "frontend-sg"
    ZeroTrust   = "true"
    ServiceTier = "frontend"
  }
}

# Backend Service
resource "aws_security_group" "backend" {
  name        = "backend-sg"
  description = "Backend service security group"
  vpc_id      = module.vpc.vpc_id

  # Only accept traffic from frontend
  ingress {
    from_port       = 8081
    to_port         = 8081
    protocol        = "tcp"
    security_groups = [aws_security_group.frontend.id]
    description     = "Allow traffic from frontend only"
  }

  # Only send traffic to database
  egress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.database.id]
    description     = "Allow traffic to database only"
  }

  tags = {
    Name        = "backend-sg"
    ZeroTrust   = "true"
    ServiceTier = "backend"
  }
}

# Database
resource "aws_security_group" "database" {
  name        = "database-sg"
  description = "Database security group"
  vpc_id      = module.vpc.vpc_id

  # Only accept traffic from backend
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.backend.id]
    description     = "Allow traffic from backend only"
  }

  # No egress (database doesn't initiate connections)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Required for health checks"
  }

  tags = {
    Name        = "database-sg"
    ZeroTrust   = "true"
    ServiceTier = "database"
  }
}
```

#### Pattern 2: Identity-Based Network Access (IAM Integration)

**Concept:** Use identity (IAM roles) instead of IP addresses for authorization.

**AWS Example: VPC Endpoints with IAM Policies**
```hcl
# S3 VPC Endpoint with IAM Policy
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = module.vpc.vpc_id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = module.vpc.private_route_table_ids

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.app.arn  # Only this role can access S3
        }
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.app.arn}/*"
      }
    ]
  })
}

# Application IAM Role
resource "aws_iam_role" "app" {
  name = "app-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}
```

#### Pattern 3: Continuous Verification with Flow Logs

```hcl
# VPC Flow Logs to CloudWatch
resource "aws_flow_log" "vpc" {
  iam_role_arn             = aws_iam_role.flow_log.arn
  log_destination          = aws_cloudwatch_log_group.flow_log.arn
  traffic_type             = "ALL"
  vpc_id                   = module.vpc.vpc_id
  max_aggregation_interval = 60  # 1 minute intervals

  tags = {
    Name      = "vpc-flow-logs"
    ZeroTrust = "true"
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "flow_log" {
  name              = "/aws/vpc/flow-logs"
  retention_in_days = 30
}

# CloudWatch Metric Filter: Detect Rejected Connections
resource "aws_cloudwatch_log_metric_filter" "rejected_connections" {
  name           = "rejected-connections"
  log_group_name = aws_cloudwatch_log_group.flow_log.name
  pattern        = "[version, account, eni, source, destination, srcport, destport, protocol, packets, bytes, windowstart, windowend, action=\"REJECT\", flowlogstatus]"

  metric_transformation {
    name      = "RejectedConnectionCount"
    namespace = "VPC/FlowLogs"
    value     = "1"
  }
}

# CloudWatch Alarm: Alert on Spike in Rejected Connections
resource "aws_cloudwatch_metric_alarm" "rejected_connections_spike" {
  alarm_name          = "rejected-connections-spike"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "RejectedConnectionCount"
  namespace           = "VPC/FlowLogs"
  period              = "300"  # 5 minutes
  statistic           = "Sum"
  threshold           = "100"  # Alert if >100 rejections in 5 min
  alarm_description   = "Alert when rejected connection count is high"
  alarm_actions       = [aws_sns_topic.alerts.arn]
}
```

---

## Hybrid Connectivity Patterns

### Pattern 1: VPN for Dev/Test Environments

**Use Case:** Low-cost hybrid connectivity for non-production workloads.

**Architecture:**
```
On-Premises Datacenter                    AWS VPC
┌─────────────────────┐                 ┌─────────────────────┐
│                     │                 │                     │
│  ┌──────────────┐   │                 │   ┌──────────────┐  │
│  │  Dev         │   │   IPsec VPN    │   │  Dev         │  │
│  │  Servers     │   │ ◄────────────► │   │  Workloads   │  │
│  └──────────────┘   │  (Encrypted)   │   └──────────────┘  │
│                     │                 │                     │
│  On-Prem Gateway    │                 │  Virtual Private    │
│  (Customer Side)    │                 │  Gateway (AWS)      │
└─────────────────────┘                 └─────────────────────┘

Throughput: ~1.25 Gbps per tunnel
Latency: Variable (internet-dependent)
Cost: Low (~$0.05/hour + data transfer)
```

**Implementation (AWS):**
```hcl
# Virtual Private Gateway
resource "aws_vpn_gateway" "main" {
  vpc_id = module.vpc.vpc_id

  tags = {
    Name = "main-vpn-gateway"
  }
}

# Customer Gateway (on-premises side)
resource "aws_customer_gateway" "onprem" {
  bgp_asn    = 65000
  ip_address = "203.0.113.10"  # Public IP of on-prem VPN device
  type       = "ipsec.1"

  tags = {
    Name = "onprem-customer-gateway"
  }
}

# VPN Connection (creates 2 tunnels for HA)
resource "aws_vpn_connection" "main" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.onprem.id
  type                = "ipsec.1"
  static_routes_only  = false  # Use BGP

  tags = {
    Name = "main-vpn-connection"
  }
}

# Route Propagation
resource "aws_vpn_gateway_route_propagation" "private" {
  count = length(module.vpc.private_route_table_ids)

  vpn_gateway_id = aws_vpn_gateway.main.id
  route_table_id = module.vpc.private_route_table_ids[count.index]
}
```

---

### Pattern 2: Direct Connect for Production Workloads

**Use Case:** High-throughput, low-latency hybrid connectivity for production.

**Architecture:**
```
On-Premises Datacenter          DX Location          AWS
┌─────────────────────┐       ┌──────────┐       ┌─────────────────────┐
│                     │       │          │       │                     │
│  ┌──────────────┐   │       │  ┌────┐  │       │   ┌──────────────┐  │
│  │  Prod        │   │  Dark │  │ DX │  │ Priv  │   │  Prod        │  │
│  │  Servers     │◄──┼──Fiber├──┤Port├──┼──VIF──┤──►│  VPC         │  │
│  └──────────────┘   │       │  └────┘  │       │   └──────────────┘  │
│                     │       │          │       │                     │
│  On-Prem Router     │       │  AWS     │       │  Virtual Private    │
│                     │       │  Equipment│       │  Gateway            │
└─────────────────────┘       └──────────┘       └─────────────────────┘

Throughput: Up to 100 Gbps (dedicated connection)
Latency: Low and consistent (<5ms typical)
Cost: Higher (port fee + data transfer)
```

**Implementation (AWS):**
```hcl
# Direct Connect Gateway (for multi-VPC connectivity)
resource "aws_dx_gateway" "main" {
  name            = "main-dx-gateway"
  amazon_side_asn = "64512"
}

# Virtual Private Gateway
resource "aws_vpn_gateway" "main" {
  vpc_id          = module.vpc.vpc_id
  amazon_side_asn = 64513

  tags = {
    Name = "prod-vgw"
  }
}

# DX Gateway Association with VGW
resource "aws_dx_gateway_association" "prod" {
  dx_gateway_id         = aws_dx_gateway.main.id
  associated_gateway_id = aws_vpn_gateway.main.id

  allowed_prefixes = [
    module.vpc.vpc_cidr_block
  ]
}

# Private Virtual Interface (created on DX connection)
# Note: DX connection itself is physical and created via AWS Console/API
resource "aws_dx_private_virtual_interface" "prod" {
  connection_id  = "dxcon-xxxxxxxxx"  # Your DX connection ID
  name           = "prod-vif"
  vlan           = 100
  address_family = "ipv4"
  bgp_asn        = 65000  # On-prem BGP ASN
  dx_gateway_id  = aws_dx_gateway.main.id
}
```

---

### Pattern 3: Hybrid with Transit Gateway + Direct Connect

**Use Case:** Multiple VPCs need on-premises connectivity via single DX connection.

**Architecture:**
```
On-Premises          DX Location          AWS
┌────────────┐       ┌──────┐       ┌────────────────────┐
│            │       │      │       │  Transit Gateway   │
│  Datacenter│◄──────┤ DX   ├───────┤                    │
│            │       │      │       └────────────────────┘
└────────────┘       └──────┘              │
                                           ├──► VPC-Prod
                                           ├──► VPC-Dev
                                           └──► VPC-Shared

Single DX connection → TGW → Multiple VPCs
Cost Efficient + Scalable
```

**Implementation:**
```hcl
# Transit Gateway
resource "aws_ec2_transit_gateway" "main" {
  description                     = "Main TGW for hybrid connectivity"
  amazon_side_asn                 = 64512
  default_route_table_association = "enable"
  default_route_table_propagation = "enable"

  tags = {
    Name = "main-tgw"
  }
}

# Direct Connect Gateway
resource "aws_dx_gateway" "main" {
  name            = "main-dx-gateway"
  amazon_side_asn = "64512"
}

# Associate DX Gateway with Transit Gateway
resource "aws_dx_gateway_association" "tgw" {
  dx_gateway_id         = aws_dx_gateway.main.id
  associated_gateway_id = aws_ec2_transit_gateway.main.id

  allowed_prefixes = [
    "10.0.0.0/8"  # Allow all RFC1918 10.x traffic
  ]
}

# Attach VPCs to Transit Gateway
resource "aws_ec2_transit_gateway_vpc_attachment" "prod" {
  transit_gateway_id = aws_ec2_transit_gateway.main.id
  vpc_id             = module.vpc_prod.vpc_id
  subnet_ids         = module.vpc_prod.private_subnets

  transit_gateway_default_route_table_association = true
  transit_gateway_default_route_table_propagation = true

  tags = {
    Name = "prod-tgw-attachment"
  }
}

# Private VIF connects to DX Gateway
resource "aws_dx_private_virtual_interface" "main" {
  connection_id = "dxcon-xxxxxxxxx"
  name          = "main-vif"
  vlan          = 100
  address_family = "ipv4"
  bgp_asn       = 65000
  dx_gateway_id = aws_dx_gateway.main.id
}
```

---

## Tool and Service Recommendations

### Cloud Provider Network Services

#### AWS Network Services

| Service | Use Case | Pricing Model |
|---------|----------|---------------|
| **VPC** | Virtual network isolation | Free |
| **Transit Gateway** | Hub-spoke multi-VPC connectivity | $0.05/hour/attachment + $0.02/GB |
| **VPC Peering** | Direct VPC-to-VPC | Free (data transfer charged) |
| **Direct Connect** | Dedicated on-prem connectivity | Port fee + data transfer |
| **VPN** | Encrypted hybrid connectivity | $0.05/hour + data transfer |
| **PrivateLink** | Private access to services | $0.01/hour/endpoint + $0.01/GB |
| **VPC Endpoints** | Private AWS service access | Gateway: Free, Interface: $0.01/hour |
| **CloudFront** | CDN and edge networking | Pay per GB |
| **Route 53** | DNS service | $0.50/hosted zone/month + queries |
| **Global Accelerator** | Global load balancing | $0.025/hour + $0.015/GB |

#### GCP Network Services

| Service | Use Case | Pricing Model |
|---------|----------|---------------|
| **VPC** | Virtual network isolation | Free |
| **VPC Peering** | VPC-to-VPC connectivity | Free (data transfer charged) |
| **Shared VPC** | Multi-project networking | Free |
| **Cloud Interconnect** | Dedicated on-prem connectivity | Port fee + data transfer |
| **Cloud VPN** | Encrypted hybrid connectivity | $0.05/hour/tunnel + data transfer |
| **Private Service Connect** | Private access to services | $0.01/hour + data transfer |
| **Cloud Load Balancing** | Global/regional LB | $0.025/hour + traffic rules |
| **Cloud CDN** | CDN and edge networking | Pay per GB |
| **Cloud DNS** | DNS service | $0.20/zone/month + queries |
| **Cloud Armor** | DDoS protection | $6/policy/month + requests |

#### Azure Network Services

| Service | Use Case | Pricing Model |
|---------|----------|---------------|
| **Virtual Network** | Virtual network isolation | Free |
| **VNet Peering** | VNet-to-VNet connectivity | $0.01/GB |
| **ExpressRoute** | Dedicated on-prem connectivity | Port fee + data transfer |
| **VPN Gateway** | Encrypted hybrid connectivity | $0.04-0.36/hour + data transfer |
| **Azure Firewall** | Network security appliance | $1.25/hour + $0.016/GB |
| **Private Link** | Private access to services | $0.01/hour/endpoint + $0.01/GB |
| **Azure Bastion** | Secure RDP/SSH access | $0.19/hour |
| **Traffic Manager** | DNS-based global LB | $0.54/million queries |
| **Azure Front Door** | Global CDN/WAF | $0.035/hour + traffic |
| **DDoS Protection** | DDoS mitigation | Standard: $2,944/month |

---

### Terraform Modules for Network Architecture

#### AWS VPC Module

**Module:** `/terraform-aws-modules/terraform-aws-vpc`
**Trust Score:** High
**Code Snippets:** 93
**Benchmark Score:** 66.9

**Features:**
- Multi-tier subnet support (public, private, database, elasticache, redshift, intra)
- NAT Gateway configurations (single, per-AZ, none)
- VPC endpoints (gateway and interface)
- IPv6 support
- VPN Gateway integration
- Network ACL customization

**Installation:**
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.5.0"  # Check for latest version

  # Configuration...
}
```

#### GCP Network Module

**Module:** `/terraform-google-modules/terraform-google-network`
**Trust Score:** High
**Code Snippets:** 55

**Features:**
- Custom mode VPC
- Regional subnets
- Secondary IP ranges (for GKE)
- Firewall rules
- Cloud Router and Cloud NAT

**Installation:**
```hcl
module "vpc" {
  source  = "terraform-google-modules/network/google"
  version = "9.0.0"  # Check for latest version

  # Configuration...
}
```

#### Azure VNET Module

**Community Module:** Various available on Terraform Registry

**Features:**
- Virtual Network creation
- Subnet management
- NSG association
- Route tables
- VNet peering

---

### Network Monitoring and Observability Tools

| Tool | Purpose | Cloud Support |
|------|---------|---------------|
| **VPC Flow Logs** (AWS) | Network traffic logging | AWS |
| **VPC Flow Logs** (GCP) | Network traffic logging | GCP |
| **NSG Flow Logs** (Azure) | Network traffic logging | Azure |
| **CloudWatch** | AWS metrics and logs | AWS |
| **Cloud Logging** | GCP logs and analysis | GCP |
| **Azure Monitor** | Azure metrics and logs | Azure |
| **Datadog** | Multi-cloud monitoring | All |
| **New Relic** | APM and network monitoring | All |
| **Kentik** | Network analytics | All |
| **ThousandEyes** | Internet and cloud network monitoring | All |

---

## Skill Structure Design

```
network-architecture/
├── SKILL.md                          # Main skill (600-800 lines)
│   ├─ Core decision frameworks
│   ├─ Pattern selection guide
│   ├─ Quick reference architectures
│   └─ When to reference detailed docs
│
├── references/
│   ├── vpc-design-patterns.md         # Flat, Multi-VPC, Hub-Spoke, Mesh, Hybrid
│   ├── subnet-strategy.md             # CIDR planning, IPAM, multi-AZ
│   ├── zero-trust-networking.md       # Microsegmentation, IAM integration
│   ├── hybrid-connectivity.md         # VPN, Direct Connect, patterns
│   ├── multi-cloud-networking.md      # AWS, GCP, Azure implementations
│   ├── security-controls.md           # Security groups, NACLs, firewalls
│   ├── private-networking.md          # VPC Endpoints, PrivateLink, PSC
│   ├── multi-region-networking.md     # Cross-region peering, global LB
│   ├── network-observability.md       # Flow logs, monitoring, troubleshooting
│   └── cost-optimization.md           # Egress reduction, NAT strategies
│
├── examples/
│   ├── aws/
│   │   ├── flat-vpc/                  # Single VPC with subnets
│   │   ├── hub-spoke-tgw/             # Transit Gateway hub-spoke
│   │   ├── vpc-peering/               # VPC peering mesh
│   │   ├── hybrid-vpn/                # VPN connectivity
│   │   ├── hybrid-dx/                 # Direct Connect
│   │   └── privatelink/               # VPC Endpoints
│   ├── gcp/
│   │   ├── custom-vpc/                # Custom mode VPC
│   │   ├── shared-vpc/                # Multi-project Shared VPC
│   │   ├── hybrid-interconnect/       # Cloud Interconnect
│   │   └── private-service-connect/   # PSC
│   ├── azure/
│   │   ├── hub-spoke/                 # Hub-spoke with firewall
│   │   ├── vnet-peering/              # VNet peering
│   │   ├── hybrid-expressroute/       # ExpressRoute
│   │   └── private-endpoints/         # Private Link
│   └── multi-cloud/
│       ├── aws-gcp-interconnect/      # AWS-GCP connectivity
│       └── aws-azure-interconnect/    # AWS-Azure connectivity
│
└── scripts/
    ├── cidr-calculator.py             # CIDR block planning
    ├── cost-estimator.sh              # Estimate network costs
    ├── validate-sg-rules.py           # Security group validation
    └── flow-log-analyzer.py           # Analyze VPC flow logs
```

---

## Integration Points

### With Existing Skills

| Skill | Integration Point |
|-------|-------------------|
| `infrastructure-as-code` | IaC implements network architectures defined here |
| `kubernetes-operations` | K8s networking (CNI, pod networking) builds on VPC design |
| `security-hardening` | Network security is foundational layer |
| `deploying-applications` | Applications deploy into network architecture |
| `secret-management` | Network isolation for secrets (private endpoints) |
| `observability` | Network monitoring complements application monitoring |
| `performance-engineering` | Network latency impacts application performance |

### Skill Chaining Examples

**Example 1: New Application Deployment**
```
network-architecture → infrastructure-as-code → deploying-applications
        │                      │                       │
        ▼                      ▼                       ▼
  Design VPC/subnets    Implement with Terraform   Deploy workloads
  Select pattern        Create SGs, NACLs          Configure networking
  Plan CIDR blocks      Set up NAT, VPC endpoints  Verify connectivity
```

**Example 2: Zero Trust Implementation**
```
network-architecture → security-hardening → observability
        │                      │                  │
        ▼                      �▼                  ▼
  Microsegmentation    Implement firewall    Monitor flow logs
  Design SG rules      WAF configuration     Alert on anomalies
  Private endpoints    IAM policies          Compliance reporting
```

**Example 3: Hybrid Cloud Setup**
```
network-architecture → infrastructure-as-code → kubernetes-operations
        │                      │                       │
        ▼                      ▼                       ▼
  Design hybrid pattern  Provision DX/VPN       Deploy EKS/GKE
  Plan IP addressing     Create TGW/routers     Configure CNI
  BGP configuration      Implement HA           Workload networking
```

---

## Implementation Roadmap

### Phase 1: Core Patterns (Weeks 1-2)
- [ ] Write main SKILL.md with decision frameworks
- [ ] Document VPC design patterns (flat, multi-VPC, hub-spoke, mesh)
- [ ] Create subnet strategy reference
- [ ] AWS examples for each pattern
- [ ] Testing and validation

### Phase 2: Multi-Cloud (Weeks 3-4)
- [ ] GCP network patterns and examples
- [ ] Azure network patterns and examples
- [ ] Multi-cloud interconnectivity patterns
- [ ] Cost comparison matrices
- [ ] Provider-specific best practices

### Phase 3: Zero Trust & Security (Weeks 5-6)
- [ ] Zero Trust architecture patterns
- [ ] Microsegmentation reference
- [ ] IAM integration examples
- [ ] Flow log monitoring patterns
- [ ] Security control comparison (SG vs NACL)

### Phase 4: Hybrid & Advanced (Weeks 7-8)
- [ ] Hybrid connectivity patterns (VPN, DX, ExpressRoute)
- [ ] Multi-region networking
- [ ] Private networking (VPC Endpoints, PrivateLink)
- [ ] Network observability deep-dive
- [ ] Cost optimization strategies

### Phase 5: Polish & Integration (Week 9)
- [ ] Scripts (CIDR calculator, cost estimator)
- [ ] Integration with other skills
- [ ] Review and feedback
- [ ] Final testing across cloud providers

---

## Key Takeaways

**1. Pattern Selection Matters**
- Flat VPC for simple apps, hub-spoke for scale, mesh for low latency
- No one-size-fits-all solution

**2. Zero Trust is Standard**
- Microsegmentation, identity-based access, continuous verification
- Network location no longer implies trust

**3. Multi-Cloud is Reality**
- Patterns transcend cloud providers
- Consistent concepts (VPC/VNet, subnets, peering, transit)
- Provider-specific implementations

**4. Hybrid Connectivity is Permanent**
- VPN for dev/test, Direct Connect for production
- Transit Gateway simplifies multi-VPC hybrid
- Cost vs performance tradeoffs

**5. Cost Optimization Through Design**
- NAT Gateway costs add up (per AZ can be $96/mo)
- VPC Endpoints reduce egress charges
- Centralized egress patterns save money

**6. Security Through Segmentation**
- Security groups > network ACLs (stateful, easier)
- Reference other security groups (not IP ranges)
- Defense in depth with multiple layers

**7. Observability is Critical**
- VPC Flow Logs for traffic analysis
- Monitor rejected connections for security
- Cost attribution through network monitoring

---

**Progressive disclosure:** This init.md provides the comprehensive master plan. The actual SKILL.md will be concise (600-800 lines) with references to detailed documentation in the `references/` directory.