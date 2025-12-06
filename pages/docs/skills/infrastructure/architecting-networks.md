---
sidebar_position: 4
title: Architecting Networks
description: Cloud network architecture with VPC patterns, zero trust, and hybrid connectivity
tags: [infrastructure, networking, vpc, aws, gcp, azure]
---

# Architecting Networks

Design secure, scalable cloud network architectures using proven patterns across AWS, GCP, and Azure. Covers VPC design, subnet strategy, zero trust implementation, and hybrid connectivity.

## When to Use

Use when:
- Designing VPC/VNet topology for new cloud environments
- Implementing network segmentation and security controls
- Planning multi-VPC or multi-cloud connectivity
- Establishing hybrid cloud connectivity (on-premises to cloud)
- Migrating from flat network to sophisticated architecture
- Implementing zero trust network principles
- Optimizing network costs and performance

## Core Architecture Patterns

### Pattern 1: Flat (Single VPC)
**Use when:** Small applications, single environment, team < 10 engineers
- All resources in one VPC with subnet-level segmentation
- Public, private, and database subnet tiers
- Lowest cost, fastest to set up
- Poor isolation, difficult to scale

### Pattern 2: Multi-VPC (Isolated)
**Use when:** Multiple environments (dev/staging/prod), strong isolation required
- Separate VPCs per environment or workload
- No direct connectivity without explicit setup
- Strong blast radius containment
- Higher management overhead and costs

### Pattern 3: Hub-and-Spoke (Transit Gateway)
**Use when:** 5+ VPCs need communication, centralized security inspection
- Central hub VPC/Transit Gateway
- All inter-VPC traffic routes through hub
- Scales to 100+ VPCs easily
- Transit Gateway costs (~$0.05/hour + $0.02/GB)

### Pattern 4: Full Mesh (VPC Peering)
**Use when:** Small number of VPCs (< 5), low latency critical
- Every VPC directly connected via peering
- Lowest latency, no Transit Gateway costs
- Management complexity scales as O(n²)

### Pattern 5: Hybrid (Multi-Pattern)
**Use when:** Large enterprise with diverse requirements
- Hub-spoke for most VPCs + direct peering for latency-sensitive pairs
- Optimized for specific needs
- More complex to design and manage

## Pattern Selection Framework

```
Number of VPCs?
│
├─► 1 VPC → Flat (Single VPC)
├─► 2-4 VPCs + No inter-VPC communication → Multi-VPC (Isolated)
├─► 2-5 VPCs + Low latency critical → Full Mesh (VPC Peering)
├─► 5+ VPCs + Centralized inspection → Hub-and-Spoke (Transit Gateway)
└─► 10+ VPCs + Mixed requirements → Hybrid (Multi-Pattern)

Additional Considerations:
├─► Hybrid connectivity required? → Hub-and-Spoke preferred
├─► Centralized egress/inspection? → Hub-and-Spoke with Inspection VPC
└─► Cost optimization priority? → Flat or Multi-VPC (avoid TGW fees)
```

## Subnet Strategy

### Standard Three-Tier Design

**Public Subnets:**
- Route to Internet Gateway
- Load balancers, bastion hosts, NAT Gateways
- CIDR: /24 to /27 (256 to 32 IPs)

**Private Subnets:**
- Route to NAT Gateway for outbound
- Application servers, containers, compute
- CIDR: /20 to /22 (4,096 to 1,024 IPs)

**Database Subnets:**
- No direct internet route
- RDS, ElastiCache, managed databases
- CIDR: /24 to /26 (256 to 64 IPs)

### Multi-AZ Distribution
- **Production:** 3 Availability Zones minimum
- **Dev/Test:** 1-2 AZs for cost savings

### CIDR Block Planning
- /16 (65,536 IPs) - Large production
- /20 (4,096 IPs) - Medium environments
- /24 (256 IPs) - Small/dev environments
- **Critical:** Non-overlapping ranges, coordinate with on-premises

## Security Controls

### Security Groups (Recommended)
- Stateful (return traffic auto-allowed)
- Instance-level control
- Allow rules only (implicit deny)
- Reference other security groups

**Best practices:**
- Descriptive names (app-alb-sg, app-backend-sg)
- Reference security groups instead of CIDR blocks
- Keep rules minimal and specific

### Network ACLs (Optional)
- Stateless (must allow both request/response)
- Subnet-level control
- Allow and deny rules
- Use for explicit deny rules, compliance

## Zero Trust Implementation

### Core Tenets
1. **Never Trust, Always Verify** - Authenticate every request
2. **Least Privilege Access** - Minimum necessary permissions
3. **Assume Breach** - Segment aggressively, monitor all traffic

### Implementation Patterns
- **Microsegmentation:** Isolate every workload with granular security group rules
- **Identity-Based Access:** Use IAM roles instead of IP addresses
- **Continuous Verification:** VPC Flow Logs, monitor rejected connections

## Hybrid Connectivity

### VPN (Virtual Private Network)
**Use when:** Dev/test, backup connectivity, temporary connections
- Encrypted tunnel over public internet
- Throughput: ~1.25 Gbps per tunnel
- Cost: Low (~$0.05/hour + data transfer)
- Setup: Quick (no contracts)

### Direct Connect / ExpressRoute / Cloud Interconnect
**Use when:** Production workloads, large data transfers, real-time apps
- Dedicated network connection
- Throughput: Up to 100 Gbps
- Latency: Low and consistent
- Cost: Higher (port fees + data transfer)
- Setup: Slower (contracts required)

## Cloud Provider Comparison

| Concept | AWS | GCP | Azure |
|---------|-----|-----|-------|
| Virtual Network | VPC | VPC | VNet |
| NAT | NAT Gateway | Cloud NAT | NAT Gateway |
| Peering | VPC Peering | VPC Peering | VNet Peering |
| Hub-Spoke | Transit Gateway | Cloud Router | Virtual WAN |
| Hybrid VPN | VPN | Cloud VPN | VPN Gateway |
| Hybrid Dedicated | Direct Connect | Cloud Interconnect | ExpressRoute |

## Cost Optimization

### Common Cost Drivers
1. NAT Gateway: $0.045/hour + $0.045/GB
2. Transit Gateway: $0.05/hour/attachment + $0.02/GB
3. Data Transfer: Egress charges vary by destination

### Optimization Strategies
- **Reduce NAT costs:** Use VPC Endpoints for AWS services, centralized egress
- **Reduce data transfer:** Keep traffic in same region, use VPC Endpoints
- **Avoid Transit Gateway:** Use VPC Peering for < 5 VPCs

## Related Skills

- [Writing Infrastructure Code](./writing-infrastructure-code) - Implement network architectures with Terraform/Pulumi
- [Operating Kubernetes](./operating-kubernetes) - Kubernetes networking (CNI) on top of VPC design
- [Load Balancing Patterns](./load-balancing-patterns) - Application load balancing within network architecture
- [Planning Disaster Recovery](./planning-disaster-recovery) - Multi-region failover networking

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/architecting-networks)
- VPC Design Patterns: `references/vpc-design-patterns.md`
- Subnet Strategy: `references/subnet-strategy.md`
- Zero Trust Networking: `references/zero-trust-networking.md`
- Hybrid Connectivity: `references/hybrid-connectivity.md`
- Multi-Cloud Networking: `references/multi-cloud-networking.md`
- Cost Optimization: `references/cost-optimization.md`
