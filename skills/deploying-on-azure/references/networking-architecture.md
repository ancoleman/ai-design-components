# Azure Networking Architecture Reference

Comprehensive guide to Azure networking patterns and architectures.

## Table of Contents

1. [Hub-and-Spoke Topology](#hub-and-spoke-topology)
2. [Private Endpoints](#private-endpoints)
3. [Network Security Groups](#network-security-groups)
4. [Load Balancing](#load-balancing)
5. [DNS Configuration](#dns-configuration)

---

## Hub-and-Spoke Topology

Centralized network architecture with shared services in hub and workloads in spokes.

### Hub VNet Components

- Azure Firewall (centralized traffic filtering)
- VPN Gateway (hybrid connectivity)
- Azure Bastion (secure VM access)
- Private Endpoints (shared PaaS services)
- DNS forwarders

### Spoke VNet Components

- Application workloads
- Environment isolation (dev, staging, prod)
- Team isolation

### VNet Peering

- Low-latency, high-bandwidth connectivity
- No data egress charges between peered VNets in same region
- Hub-spoke peering: Enable "Allow Gateway Transit" in hub, "Use Remote Gateway" in spoke

---

## Private Endpoints

Network interface that connects privately and securely to a service powered by Azure Private Link.

### Supported Services

100+ Azure services support Private Endpoints including:
- Storage (Blob, Files, Queue, Table)
- Databases (SQL, Cosmos DB, PostgreSQL, MySQL)
- Azure OpenAI, Cognitive Services
- Key Vault, App Configuration
- Container Registry, Event Hub, Service Bus

### Private DNS Zones

Required for automatic DNS resolution of privatelink FQDNs.

---

## Network Security Groups

Stateful firewall rules for subnet and NIC level filtering.

### Rule Priority

- Lower numbers = higher priority
- Default rules (65000-65500) allow VNet traffic, deny internet
- Custom rules (100-4096) take precedence

---

## Load Balancing

Distribute network traffic across multiple backends for high availability and scalability.

### Service Comparison

| Service | Layer | Scope | Use Case |
|---------|-------|-------|----------|
| **Azure Front Door** | L7 (HTTP/S) | Global | Global routing, WAF |
| **Application Gateway** | L7 (HTTP/S) | Regional | Regional load balancing, WAF |
| **Load Balancer** | L4 (TCP/UDP) | Regional | Non-HTTP traffic |
| **Traffic Manager** | DNS | Global | DNS-based routing |

---

## DNS Configuration

### Azure Private DNS Zones

Link private DNS zones to VNets for automatic resolution of Private Endpoints.

### DNS Forwarding

Conditional forwarders for hybrid DNS resolution (on-premises ↔ Azure).
