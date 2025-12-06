---
sidebar_position: 5
title: Network Architecture
description: Master plan for cloud network design including VPC patterns, zero trust, hybrid connectivity, and multi-region networking
tags: [master-plan, infrastructure, networking, vpc, zero-trust]
---

# Network Architecture

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Cloud network architecture has evolved from simple VPC configurations to complex, multi-cloud, zero-trust environments. This skill covers VPC design patterns, network segmentation, hybrid connectivity, multi-region networking, and zero trust architecture.

## Scope

This skill teaches:

- **VPC Design Patterns** - Flat, hub-and-spoke, mesh, Transit Gateway patterns
- **Subnet Strategy** - Public/private/isolated tiers, CIDR planning (IPAM), multi-AZ distribution
- **Network Segmentation** - Microsegmentation, security groups, NACLs, service isolation
- **Hybrid Connectivity** - VPN vs Direct Connect/ExpressRoute/Cloud Interconnect patterns
- **Multi-Region Networking** - Cross-region peering, global load balancing, disaster recovery
- **Zero Trust Architecture** - Identity-based access, least privilege, continuous verification
- **Service Networking** - Private endpoints (PrivateLink, Private Link, Private Service Connect)
- **Network Observability** - VPC flow logs, traffic analysis, cost attribution

## Key Components

### VPC Design Patterns

**Flat Architecture** - Single VPC for all workloads
- Best for: Small deployments, startups, simple environments
- Trade-offs: Limited isolation, can become complex over time

**Hub-and-Spoke** - Central hub VPC connected to spoke VPCs
- Best for: Enterprise, multi-account, centralized security
- Advantages: Simplified management, centralized inspection
- Examples: Transit Gateway (AWS), VPC Network Peering (GCP), Virtual WAN (Azure)

**Mesh Networking** - Full connectivity between VPCs
- Best for: Heavy inter-VPC communication
- Trade-offs: Complex to manage, higher cost

**Transit Gateway** - Centralized routing hub
- Best for: Multi-account, multi-region, hybrid connectivity
- Advantages: Scalable, simplified routing

### Zero Trust Principles

- **Never trust, always verify** - Identity-based access (not IP-based)
- **Least privilege networking** - Minimal required access
- **Continuous verification** - Real-time security assessment
- **Microsegmentation** - Service-to-service isolation

## Decision Framework

**Which VPC Pattern?**

```
Small deployment (&lt;5 VPCs)?
  YES → Flat Architecture (single VPC or simple peering)

Multi-account / multi-team?
  YES → Need centralized security?
          YES → Hub-and-Spoke (Transit Gateway)
          NO → Mesh (VPC Peering)

Hybrid cloud (on-prem + cloud)?
  YES → Hub-and-Spoke with hybrid gateway

Multi-region with inter-region traffic?
  YES → Transit Gateway with cross-region peering
```

**Hybrid Connectivity: VPN vs Direct Connect?**

| Criteria | VPN | Direct Connect |
|----------|-----|----------------|
| **Setup Time** | Minutes | Weeks |
| **Cost** | Low ($0.05/hr + data) | High ($0.30/hr/Gbps + port) |
| **Bandwidth** | Up to 1.25 Gbps | 1/10/100 Gbps |
| **Latency** | Higher (internet) | Lower (dedicated) |
| **Use Case** | Dev/staging, temporary | Production, high bandwidth |

## Tool Recommendations

### Cloud-Native Networking

**AWS:**
- VPC, Transit Gateway, PrivateLink
- Direct Connect (hybrid)
- Route 53 (DNS), Global Accelerator (anycast)

**GCP:**
- VPC Network, Shared VPC, VPC Network Peering
- Cloud Interconnect (hybrid)
- Cloud DNS, Cloud CDN

**Azure:**
- Virtual Network, Virtual WAN, Private Link
- ExpressRoute (hybrid)
- Azure DNS, Traffic Manager

### Network Automation

**Terraform/Pulumi** - IaC for network provisioning
**Network Policy Engines** - Calico, Cilium (Kubernetes)
**Flow Analysis** - VPC Flow Logs, Traffic Mirroring, Network Watcher

### Best Practices (2025)

- **Identity-first security** with ABAC and service control policies
- **Multi-AZ baseline** for production, multi-region for business-critical
- **Centralize connectivity** and inspection (hub-spoke model)
- **Segment aggressively** using VPCs, routing tables, service-to-service identity
- **Prefer managed services** and serverless to reduce infrastructure

## Integration Points

**With Other Skills:**
- `writing-infrastructure-code` - Terraform/Pulumi for network provisioning
- `operating-kubernetes` - Network policies, service mesh integration
- `load-balancing-patterns` - LB networking, global load balancing
- `security-hardening` - Security groups, NACLs, firewall rules
- `managing-dns` - DNS architecture, split-horizon DNS
- `implementing-observability` - VPC flow logs, network monitoring

**Cross-Skill Workflows:**
```
IaC → Network → Load Balancer → Applications
  │       │           │              │
  ▼       ▼           ▼              ▼
Create  Configure  Distribute    Deploy
VPCs    routing    traffic       workloads
```

## Learn More

- [Full Master Plan (init.md)](https://github.com/ancoleman/ai-design-components/blob/main/skills/architecting-networks/init.md)
- Related: `writing-infrastructure-code`, `security-hardening`, `load-balancing-patterns`
