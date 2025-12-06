# Subnet Strategy

Comprehensive guide to subnet design, CIDR planning, IP address management (IPAM), and multi-AZ distribution for cloud networks.

## Table of Contents

1. [Subnet Tier Design](#subnet-tier-design)
2. [CIDR Block Planning](#cidr-block-planning)
3. [IP Address Management (IPAM)](#ip-address-management-ipam)
4. [Multi-AZ Distribution](#multi-az-distribution)
5. [Reserved Address Space](#reserved-address-space)
6. [Subnet Sizing Calculator](#subnet-sizing-calculator)

---

## Subnet Tier Design

### Standard Three-Tier Architecture

#### Public Subnets

**Purpose:** Resources that need direct internet access

**Routes:**
- Default route (0.0.0.0/0) points to Internet Gateway

**Use For:**
- Application Load Balancers (ALB)
- Network Load Balancers (NLB)
- NAT Gateways
- Bastion hosts
- Public-facing web servers

**CIDR Sizing:**
- Small: /27 (32 IPs) - For load balancers only
- Medium: /26 (64 IPs) - Load balancers + NAT
- Large: /24 (256 IPs) - Public-facing workloads

**Example (3 AZs):**
```
10.0.1.0/26   - us-east-1a (64 IPs)
10.0.1.64/26  - us-east-1b (64 IPs)
10.0.1.128/26 - us-east-1c (64 IPs)
```

#### Private Subnets

**Purpose:** Application workloads with outbound internet access

**Routes:**
- Default route (0.0.0.0/0) points to NAT Gateway

**Use For:**
- EC2 instances
- ECS/EKS containers
- Lambda functions in VPC
- Application servers
- Kubernetes worker nodes

**CIDR Sizing:**
- Small: /22 (1,024 IPs) - Small workloads
- Medium: /21 (2,048 IPs) - Medium workloads
- Large: /20 (4,096 IPs) - Large workloads, Kubernetes

**Example (3 AZs):**
```
10.0.16.0/20  - us-east-1a (4,096 IPs)
10.0.32.0/20  - us-east-1b (4,096 IPs)
10.0.48.0/20  - us-east-1c (4,096 IPs)
```

#### Database Subnets

**Purpose:** Database and cache layers with no direct internet

**Routes:**
- No default route to internet
- Routes to VPC CIDR only

**Use For:**
- RDS databases
- Aurora clusters
- ElastiCache
- Redshift
- Self-managed databases

**CIDR Sizing:**
- Small: /26 (64 IPs) - Few databases
- Medium: /25 (128 IPs) - Multiple databases
- Large: /24 (256 IPs) - Many databases, read replicas

**Example (3 AZs):**
```
10.0.64.0/24 - us-east-1a (256 IPs)
10.0.65.0/24 - us-east-1b (256 IPs)
10.0.66.0/24 - us-east-1c (256 IPs)
```

### Advanced: Specialized Subnet Tiers

#### Isolated Subnets (Intra)

**Purpose:** Resources with no internet access at all

**Routes:**
- Only VPC-local routes
- No NAT Gateway

**Use For:**
- VPC Endpoints (Interface endpoints)
- Highly sensitive workloads
- Compliance-isolated resources

**CIDR Sizing:** /24 (256 IPs)

#### Service-Specific Subnets

**ElastiCache Subnets:**
```
10.0.80.0/24 - us-east-1a
10.0.81.0/24 - us-east-1b
10.0.82.0/24 - us-east-1c
```

**Redshift Subnets:**
```
10.0.90.0/24 - us-east-1a
10.0.91.0/24 - us-east-1b
10.0.92.0/24 - us-east-1c
```

**Kubernetes Pod Subnets (GCP):**
```
# Secondary IP range for pods
10.1.0.0/16 (65,536 IPs)

# Secondary IP range for services
10.2.0.0/20 (4,096 IPs)
```

---

## CIDR Block Planning

### VPC CIDR Sizing Guidelines

| Environment | VPC CIDR | Total IPs | Use Case |
|-------------|----------|-----------|----------|
| Large Production | /16 | 65,536 | Large-scale production, Kubernetes |
| Medium Production | /18 | 16,384 | Medium production workloads |
| Small Production | /20 | 4,096 | Small production, limited services |
| Development | /20 | 4,096 | Dev/test environments |
| POC/Sandbox | /24 | 256 | Proof of concept, experimentation |

### CIDR Allocation Examples

#### Example 1: Production VPC (10.0.0.0/16)

```
VPC: 10.0.0.0/16 (65,536 IPs)

Public Subnets (3 AZs, 192 IPs total):
├─ 10.0.1.0/26   (64 IPs)  - us-east-1a
├─ 10.0.1.64/26  (64 IPs)  - us-east-1b
└─ 10.0.1.128/26 (64 IPs)  - us-east-1c

Private Subnets (3 AZs, 12,288 IPs total):
├─ 10.0.16.0/20  (4,096 IPs) - us-east-1a
├─ 10.0.32.0/20  (4,096 IPs) - us-east-1b
└─ 10.0.48.0/20  (4,096 IPs) - us-east-1c

Database Subnets (3 AZs, 768 IPs total):
├─ 10.0.64.0/24 (256 IPs) - us-east-1a
├─ 10.0.65.0/24 (256 IPs) - us-east-1b
└─ 10.0.66.0/24 (256 IPs) - us-east-1c

ElastiCache Subnets (3 AZs, 768 IPs total):
├─ 10.0.80.0/24 (256 IPs) - us-east-1a
├─ 10.0.81.0/24 (256 IPs) - us-east-1b
└─ 10.0.82.0/24 (256 IPs) - us-east-1c

Isolated Subnets (3 AZs, 768 IPs total):
├─ 10.0.100.0/24 (256 IPs) - us-east-1a
├─ 10.0.101.0/24 (256 IPs) - us-east-1b
└─ 10.0.102.0/24 (256 IPs) - us-east-1c

Reserved for Future (32,768 IPs):
└─ 10.0.128.0/17 - Reserved expansion
```

#### Example 2: Development VPC (10.1.0.0/20)

```
VPC: 10.1.0.0/20 (4,096 IPs)

Public Subnets (2 AZs, 128 IPs total):
├─ 10.1.1.0/26   (64 IPs) - us-east-1a
└─ 10.1.1.64/26  (64 IPs) - us-east-1b

Private Subnets (2 AZs, 2,048 IPs total):
├─ 10.1.4.0/21   (1,024 IPs) - us-east-1a
└─ 10.1.8.0/21   (1,024 IPs) - us-east-1b

Database Subnets (2 AZs, 512 IPs total):
├─ 10.1.12.0/24 (256 IPs) - us-east-1a
└─ 10.1.13.0/24 (256 IPs) - us-east-1b

Reserved (1,408 IPs):
└─ 10.1.14.0/23 - Future expansion
```

### CIDR Planning Rules

1. **Non-Overlapping CIDRs Across VPCs**
   ```
   Production VPC:  10.0.0.0/16
   Staging VPC:     10.1.0.0/16
   Development VPC: 10.2.0.0/16
   Shared Services: 10.3.0.0/16
   ```

2. **Coordinate with On-Premises**
   - Avoid overlapping with on-premises CIDR ranges
   - Example: If on-prem uses 172.16.0.0/12, use 10.0.0.0/8 for cloud

3. **Reserve Address Space**
   - Always reserve at least 20% for future growth
   - Use larger CIDR than immediately needed

4. **AWS Reserved Addresses**
   - First 4 IPs and last IP in each subnet are reserved
   - Example: In 10.0.1.0/24:
     - 10.0.1.0 - Network address
     - 10.0.1.1 - VPC router
     - 10.0.1.2 - DNS server
     - 10.0.1.3 - Reserved for future use
     - 10.0.1.255 - Broadcast address

---

## IP Address Management (IPAM)

### IPAM Best Practices

#### 1. Centralized IPAM Tool

**AWS:**
- Use Amazon VPC IP Address Manager (IPAM)
- Automated CIDR allocation
- Prevent overlapping ranges

**Azure:**
- Azure Virtual Network Manager
- Centralized IP planning

**GCP:**
- Manual tracking or third-party tools
- IP address utilization dashboard

#### 2. CIDR Allocation Strategy

**Hierarchical Allocation:**
```
10.0.0.0/8 - Entire cloud organization

├─ 10.0.0.0/12 - AWS
│  ├─ 10.0.0.0/13 - Production
│  │  ├─ 10.0.0.0/16 - Prod VPC 1
│  │  ├─ 10.1.0.0/16 - Prod VPC 2
│  │  └─ 10.2.0.0/16 - Prod VPC 3
│  └─ 10.8.0.0/13 - Non-Production
│     ├─ 10.8.0.0/16 - Staging
│     └─ 10.9.0.0/16 - Development
│
└─ 10.16.0.0/12 - GCP
   └─ (similar structure)
```

#### 3. Documentation

**Maintain IPAM Registry:**
```
| VPC Name | CIDR | Cloud | Region | Environment |
|----------|------|-------|--------|-------------|
| prod-vpc-1 | 10.0.0.0/16 | AWS | us-east-1 | Production |
| prod-vpc-2 | 10.1.0.0/16 | AWS | us-west-2 | Production |
| dev-vpc-1 | 10.8.0.0/16 | AWS | us-east-1 | Development |
```

### Avoiding CIDR Conflicts

**Common Pitfalls:**
1. Overlapping VPC CIDRs (prevents peering)
2. Overlapping with on-premises
3. Overlapping with VPN client pools
4. Not reserving enough space for growth

**Resolution Strategy:**
- Plan CIDR allocation before creating VPCs
- Use IPAM tools to prevent overlaps
- Document all allocations
- Communicate with network team

---

## Multi-AZ Distribution

### Production Requirements

**Minimum: 3 Availability Zones**
- Survives single AZ failure
- Meets most SLA requirements
- AWS best practice for production

**Configuration:**
```hcl
azs = ["us-east-1a", "us-east-1b", "us-east-1c"]

public_subnets = [
  "10.0.1.0/24",   # AZ-a
  "10.0.2.0/24",   # AZ-b
  "10.0.3.0/24"    # AZ-c
]

private_subnets = [
  "10.0.10.0/24",  # AZ-a
  "10.0.11.0/24",  # AZ-b
  "10.0.12.0/24"   # AZ-c
]
```

### Non-Production Flexibility

**Cost-Optimized: 2 Availability Zones**
```hcl
azs = ["us-east-1a", "us-east-1b"]

public_subnets = [
  "10.0.1.0/24",   # AZ-a
  "10.0.2.0/24"    # AZ-b
]

private_subnets = [
  "10.0.10.0/24",  # AZ-a
  "10.0.11.0/24"   # AZ-b
]
```

**Extreme Cost-Optimization: 1 Availability Zone**
- Only for dev/test
- No resilience
- Not recommended

### Multi-Region Considerations

**Regional CIDR Planning:**
```
us-east-1 Production: 10.0.0.0/16
us-west-2 Production: 10.1.0.0/16
eu-west-1 Production: 10.2.0.0/16
```

**Cross-Region Peering Requirements:**
- Non-overlapping CIDRs mandatory
- Plan global CIDR strategy early

---

## Reserved Address Space

### Why Reserve Space

1. **Future Growth:** Add new subnet tiers without redesigning
2. **Service Expansion:** New AWS services may require dedicated subnets
3. **Unforeseen Requirements:** Compliance, security, or business needs

### Reservation Strategy

**Allocate 30-50% for Future Use:**
```
VPC: 10.0.0.0/16 (65,536 IPs)

Active Allocation: 32,768 IPs (50%)
├─ Public, Private, Database, etc.

Reserved: 32,768 IPs (50%)
└─ 10.0.128.0/17 - Reserved for future
```

**Use Larger VPC CIDR Than Needed:**
- Planning for 1,000 IPs? Use /20 (4,096 IPs)
- Planning for 4,000 IPs? Use /18 (16,384 IPs)
- Planning for 16,000 IPs? Use /16 (65,536 IPs)

---

## Subnet Sizing Calculator

### Quick Reference Table

| CIDR | Subnet Mask | Total IPs | Usable IPs (AWS) | Use Case |
|------|-------------|-----------|------------------|----------|
| /28 | 255.255.255.240 | 16 | 11 | Very small (< 10 resources) |
| /27 | 255.255.255.224 | 32 | 27 | Small (ALB only) |
| /26 | 255.255.255.192 | 64 | 59 | Public subnets |
| /25 | 255.255.255.128 | 128 | 123 | Small private subnets |
| /24 | 255.255.255.0 | 256 | 251 | Database subnets |
| /23 | 255.255.254.0 | 512 | 507 | Medium private subnets |
| /22 | 255.255.252.0 | 1,024 | 1,019 | Large private subnets |
| /21 | 255.255.248.0 | 2,048 | 2,043 | Large private subnets |
| /20 | 255.255.240.0 | 4,096 | 4,091 | Large private subnets, Kubernetes |
| /19 | 255.255.224.0 | 8,192 | 8,187 | Very large private subnets |
| /18 | 255.255.192.0 | 16,384 | 16,379 | Medium VPC |
| /17 | 255.255.128.0 | 32,768 | 32,763 | Large VPC segment |
| /16 | 255.255.0.0 | 65,536 | 65,531 | Standard VPC size |

### Sizing Formula

**Calculate Required CIDR:**
```
Required IPs = (Current IPs × Growth Factor) + Buffer

Growth Factor: 2x to 3x for production
Buffer: 20-30% additional for unforeseen needs

Example:
Current: 500 IPs
Growth: 2x = 1,000 IPs
Buffer: 30% = 300 IPs
Total: 1,300 IPs → Use /21 (2,048 IPs)
```

### Kubernetes-Specific Sizing

**EKS/GKE Pod Networking:**
```
Private Subnet for Nodes: /20 (4,096 IPs)
Secondary Range for Pods: /16 (65,536 IPs)
Secondary Range for Services: /20 (4,096 IPs)
```

**Calculation:**
- 100 nodes × 30 pods/node = 3,000 pods
- Use /16 for pod range (65,536 IPs)
