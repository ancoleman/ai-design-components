# Hybrid Connectivity

Comprehensive guide to connecting on-premises datacenters to cloud environments using VPN, Direct Connect, ExpressRoute, and Cloud Interconnect.

## Table of Contents

1. [VPN Connectivity](#vpn-connectivity)
2. [Dedicated Connectivity](#dedicated-connectivity)
3. [Transit Gateway Patterns](#transit-gateway-patterns)
4. [High Availability Patterns](#high-availability-patterns)
5. [Cost Optimization](#cost-optimization)

---

## VPN Connectivity

### Use Cases

**Ideal For:**
- Development and test environments
- Temporary connections
- Backup connectivity to dedicated link
- Low-cost hybrid requirements
- Quick setup needed (no contracts)

**Not Suitable For:**
- High-throughput production workloads (> 1.25 Gbps)
- Low-latency requirements
- Large data transfers
- Mission-critical applications

### Architecture Pattern (AWS)

```
On-Premises Datacenter                    AWS VPC
┌─────────────────────┐                 ┌─────────────────────┐
│                     │                 │                     │
│  ┌──────────────┐   │                 │   ┌──────────────┐  │
│  │  Dev         │   │   IPsec VPN    │   │  Dev         │  │
│  │  Servers     │   │ ◄────────────► │   │  Workloads   │  │
│  └──────────────┘   │  (Encrypted)   │   └──────────────┘  │
│                     │                 │                     │
│  Customer Gateway   │                 │  Virtual Private    │
│  (On-Prem Device)   │                 │  Gateway (AWS)      │
└─────────────────────┘                 └─────────────────────┘

Throughput: ~1.25 Gbps per tunnel (2 tunnels for HA)
Latency: Variable (internet-dependent)
Cost: Low (~$0.05/hour + data transfer)
```

### Implementation (AWS)

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
  static_routes_only  = false  # Use BGP for dynamic routing

  tags = {
    Name = "main-vpn-connection"
  }
}

# Route Propagation (automatic BGP routes)
resource "aws_vpn_gateway_route_propagation" "private" {
  count = length(module.vpc.private_route_table_ids)

  vpn_gateway_id = aws_vpn_gateway.main.id
  route_table_id = module.vpc.private_route_table_ids[count.index]
}
```

### VPN Configuration

**Tunnel 1:**
- Outside IP: 203.0.113.10
- Inside IP: 169.254.10.1/30
- BGP ASN: 65000
- Pre-shared key: (generated)

**Tunnel 2:**
- Outside IP: 203.0.113.11
- Inside IP: 169.254.10.5/30
- BGP ASN: 65000
- Pre-shared key: (generated)

### Accelerated VPN (AWS)

**Use When:** Internet connectivity is unreliable

```hcl
resource "aws_vpn_connection" "accelerated" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.onprem.id
  type                = "ipsec.1"
  enable_acceleration = true  # Use AWS Global Accelerator

  tags = {
    Name = "accelerated-vpn"
  }
}
```

**Benefits:**
- Routes over AWS global network (not public internet)
- More stable performance
- Reduced latency variability

**Costs:**
- Additional $0.05/hour per tunnel
- Accelerated data transfer charges

---

## Dedicated Connectivity

### AWS Direct Connect

#### Use Cases

**Ideal For:**
- Production workloads
- Large data transfers (TB+)
- Real-time applications
- Predictable network performance
- Hybrid cloud at scale

**Architecture:**

```
On-Premises          DX Location          AWS
┌────────────┐       ┌──────────┐       ┌─────────────────────┐
│            │       │          │       │                     │
│  ┌──────┐  │ Dark  │  ┌────┐  │ Priv  │   ┌──────────────┐  │
│  │ Prod │  │ Fiber │  │ DX │  │ VIF   │   │  Prod        │  │
│  │Servers├──┼───────┤  │Port├──┼───────┤──►│  VPC         │  │
│  └──────┘  │       │  └────┘  │       │   └──────────────┘  │
│            │       │          │       │                     │
│  Router    │       │  AWS     │       │  Virtual Private    │
│            │       │  Cage    │       │  Gateway            │
└────────────┘       └──────────┘       └─────────────────────┘

Throughput: Up to 100 Gbps (dedicated connection)
Latency: Low and consistent (<5ms typical)
Cost: Port fee ($0.30/hour for 1 Gbps) + data transfer ($0.02/GB)
Setup: 2-4 weeks (contracts, cross-connect)
```

#### Implementation (AWS)

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

# Private Virtual Interface (on DX connection)
# Note: DX connection itself is physical, created via AWS Console
resource "aws_dx_private_virtual_interface" "prod" {
  connection_id  = "dxcon-fg5678gh"  # Your DX connection ID
  name           = "prod-vif"
  vlan           = 100
  address_family = "ipv4"
  bgp_asn        = 65000  # On-prem BGP ASN
  dx_gateway_id  = aws_dx_gateway.main.id
}
```

#### Direct Connect Capacity Options

| Port Speed | Monthly Cost | Use Case |
|------------|--------------|----------|
| 50 Mbps (Hosted) | ~$36 | Small workloads |
| 100 Mbps (Hosted) | ~$72 | Dev/test |
| 500 Mbps (Hosted) | ~$360 | Medium workloads |
| 1 Gbps | ~$220 | Production |
| 10 Gbps | ~$1,700 | High-volume |
| 100 Gbps | ~$17,000 | Enterprise-scale |

### Azure ExpressRoute

#### Architecture

```
On-Premises          ExpressRoute Location          Azure
┌────────────┐       ┌──────────────────┐       ┌─────────────────┐
│            │       │                  │       │                 │
│  ┌──────┐  │       │  ┌────────────┐  │       │   ┌─────────┐   │
│  │ Prod │  │       │  │ExpressRoute│  │       │   │  VNet   │   │
│  │Servers├──┼───────┤  │  Circuit   ├──┼───────┤──►│         │   │
│  └──────┘  │       │  └────────────┘  │       │   └─────────┘   │
│            │       │                  │       │                 │
│  Router    │       │  Connectivity    │       │  Virtual        │
│            │       │  Provider        │       │  Network        │
└────────────┘       └──────────────────┘       └─────────────────┘
```

#### Implementation (Azure)

```hcl
# ExpressRoute Circuit
resource "azurerm_express_route_circuit" "main" {
  name                  = "prod-expressroute"
  resource_group_name   = azurerm_resource_group.main.name
  location              = azurerm_resource_group.main.location
  service_provider_name = "Equinix"
  peering_location      = "Silicon Valley"
  bandwidth_in_mbps     = 1000

  sku {
    tier   = "Standard"
    family = "MeteredData"
  }

  tags = {
    Environment = "Production"
  }
}

# Private Peering
resource "azurerm_express_route_circuit_peering" "private" {
  peering_type                  = "AzurePrivatePeering"
  express_route_circuit_name    = azurerm_express_route_circuit.main.name
  resource_group_name           = azurerm_resource_group.main.name
  peer_asn                      = 65000
  primary_peer_address_prefix   = "192.168.1.0/30"
  secondary_peer_address_prefix = "192.168.2.0/30"
  vlan_id                       = 100
}

# VNet Gateway Connection
resource "azurerm_virtual_network_gateway_connection" "expressroute" {
  name                = "expressroute-connection"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  type                            = "ExpressRoute"
  virtual_network_gateway_id      = azurerm_virtual_network_gateway.main.id
  express_route_circuit_id        = azurerm_express_route_circuit.main.id
  connection_protocol             = "IKEv2"
}
```

### GCP Cloud Interconnect

#### Dedicated Interconnect

```
On-Premises          Colocation          GCP
┌────────────┐       ┌────────────┐       ┌─────────────────┐
│            │       │            │       │                 │
│  ┌──────┐  │       │  ┌──────┐  │       │   ┌─────────┐   │
│  │ Prod │  │       │  │ GCP  │  │       │   │  VPC    │   │
│  │Servers├──┼───────┤  │Cage  ├──┼───────┤──►│         │   │
│  └──────┘  │       │  └──────┘  │       │   └─────────┘   │
│            │       │            │       │                 │
│  Router    │       │  Cross-    │       │  Cloud          │
│            │       │  Connect   │       │  Router         │
└────────────┘       └────────────┘       └─────────────────┘
```

#### Implementation (GCP)

```hcl
# Cloud Router
resource "google_compute_router" "main" {
  name    = "main-router"
  region  = "us-central1"
  network = google_compute_network.main.id

  bgp {
    asn               = 64514
    advertise_mode    = "CUSTOM"
    advertised_groups = ["ALL_SUBNETS"]
  }
}

# Interconnect Attachment (VLAN)
resource "google_compute_interconnect_attachment" "main" {
  name                     = "main-vlan"
  interconnect             = "https://www.googleapis.com/compute/v1/projects/${var.project}/global/interconnects/${var.interconnect_name}"
  router                   = google_compute_router.main.id
  region                   = "us-central1"
  type                     = "DEDICATED"
  bandwidth                = "BPS_10G"
  admin_enabled            = true
  vlan_tag8021q            = 100
  candidate_subnets        = ["169.254.100.0/29"]
}

# Router Interface
resource "google_compute_router_interface" "main" {
  name       = "main-interface"
  router     = google_compute_router.main.name
  region     = google_compute_router.main.region
  ip_range   = "169.254.100.1/29"
  vpn_tunnel = google_compute_interconnect_attachment.main.self_link
}

# BGP Peer
resource "google_compute_router_peer" "main" {
  name                      = "main-peer"
  router                    = google_compute_router.main.name
  region                    = google_compute_router.main.region
  interface                 = google_compute_router_interface.main.name
  peer_ip_address           = "169.254.100.2"
  peer_asn                  = 65000
  advertised_route_priority = 100
}
```

---

## Transit Gateway Patterns

### Pattern: Hybrid with Transit Gateway + Direct Connect

**Use Case:** Multiple VPCs need on-premises connectivity via single DX connection

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
  description                     = "Main TGW for hybrid"
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

  tags = {
    Name = "prod-tgw-attachment"
  }
}

# Private VIF connects to DX Gateway
resource "aws_dx_private_virtual_interface" "main" {
  connection_id  = "dxcon-fg5678gh"
  name           = "main-vif"
  vlan           = 100
  address_family = "ipv4"
  bgp_asn        = 65000
  dx_gateway_id  = aws_dx_gateway.main.id
}
```

---

## High Availability Patterns

### Pattern 1: VPN Backup to Direct Connect

**Architecture:**

```
                  Primary Path
On-Prem ────────► Direct Connect ────────► AWS VPC
   │                                          ▲
   │           Backup Path (failover)         │
   └───────────► VPN ──────────────────────────┘

If DX fails, traffic automatically routes through VPN
```

**Implementation:**

```hcl
# Direct Connect (Primary)
resource "aws_dx_private_virtual_interface" "primary" {
  connection_id = "dxcon-fg5678gh"
  # ... DX config
}

# VPN (Backup)
resource "aws_vpn_connection" "backup" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.onprem.id
  type                = "ipsec.1"

  tags = {
    Name = "backup-vpn"
    Role = "Backup to Direct Connect"
  }
}
```

**BGP Configuration:**
- Direct Connect: Local preference 200 (preferred)
- VPN: Local preference 100 (backup)
- Automatic failover via BGP

### Pattern 2: Dual Direct Connect

**Architecture:**

```
On-Prem ────► DX Connection 1 (Primary) ────► AWS VPC
   │                                              ▲
   └──────────► DX Connection 2 (Secondary) ──────┘

Two Direct Connect connections for redundancy
```

**Resilience:**
- Different physical paths
- Different colocation facilities
- Active-active or active-passive

**Cost:**
- Double the Direct Connect port fees
- Highest availability

---

## Cost Optimization

### VPN vs Direct Connect Cost Comparison

**Scenario:** 1 Gbps bandwidth, 10 TB/month data transfer

| Solution | Setup | Monthly | Data Transfer | Total Monthly |
|----------|-------|---------|---------------|---------------|
| VPN | Free | ~$37 (2 tunnels) | $920 ($0.09/GB) | ~$957 |
| Direct Connect 1 Gbps | $0-2000 (one-time) | ~$220 (port) | $200 ($0.02/GB) | ~$420 |

**Break-even:** Direct Connect cheaper if > 8 TB/month or need consistent performance

### Optimization Strategies

1. **Use VPN for Dev/Test**
   - Direct Connect for production only
   - Reduces costs 50%+

2. **Right-size Direct Connect**
   - Start with 1 Gbps, upgrade if needed
   - Monitor utilization

3. **Centralized Hybrid Connection**
   - Single Direct Connect + Transit Gateway
   - Multiple VPCs share one connection

4. **Hosted Connections for Smaller Needs**
   - 50 Mbps to 500 Mbps options
   - Lower cost than dedicated
