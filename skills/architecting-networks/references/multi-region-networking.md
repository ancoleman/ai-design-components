# Multi-Region Networking

Cross-region connectivity patterns for disaster recovery and global applications.

## Table of Contents

1. [Use Cases](#use-cases)
2. [Cross-Region VPC Peering](#cross-region-vpc-peering)
3. [Global Load Balancing](#global-load-balancing)
4. [Multi-Region Architecture Pattern](#multi-region-architecture-pattern)

---

## Use Cases

1. **Disaster Recovery**
   - Failover to secondary region
   - Data replication across regions

2. **Global Applications**
   - Serve users worldwide with low latency
   - Geo-distributed workloads

3. **Data Residency**
   - Compliance with regional data laws
   - Data sovereignty requirements

## Cross-Region VPC Peering

### AWS

**Setup:**
```hcl
# Peering connection between regions
resource "aws_vpc_peering_connection" "us_to_eu" {
  vpc_id        = aws_vpc.us_east.id
  peer_vpc_id   = aws_vpc.eu_west.id
  peer_region   = "eu-west-1"
  auto_accept   = false  # Requires acceptance in peer region

  tags = {
    Name = "us-east-to-eu-west-peering"
  }
}

# Accept peering in peer region
resource "aws_vpc_peering_connection_accepter" "eu_accept" {
  provider                  = aws.eu_west
  vpc_peering_connection_id = aws_vpc_peering_connection.us_to_eu.id
  auto_accept               = true
}
```

**Data Transfer Costs:**
- Cross-region: $0.02/GB

### GCP

**VPC is global by default**
- Subnets are regional
- No cross-region peering needed within single VPC
- Multi-region by design

### Azure

**VNet Peering:**
- Cross-region peering supported
- Data transfer: $0.01/GB

## Global Load Balancing

### AWS Global Accelerator

**Use When:**
- Need static anycast IPs
- Improve availability and performance globally
- Instant regional failover

**Cost:** $0.025/hour + $0.015/GB

### GCP Cloud Load Balancing

**Use When:**
- Global HTTP(S) load balancing
- Anycast IP addresses
- Cross-region failover

### Azure Traffic Manager

**Use When:**
- DNS-based global load balancing
- Geographic routing
- Priority-based failover

**Cost:** $0.54/million queries

## Multi-Region Architecture Pattern

```
        Global Load Balancer
               │
       ┌───────┴────────┐
       │                │
   us-east-1        eu-west-1
   (Primary)        (DR/Active)
       │                │
   ┌───────┐        ┌───────┐
   │  VPC  │◄───────┤  VPC  │
   │       │ Peering│       │
   └───────┘        └───────┘
```

**Benefits:**
- Low latency for global users
- High availability (multi-region failover)
- Disaster recovery
