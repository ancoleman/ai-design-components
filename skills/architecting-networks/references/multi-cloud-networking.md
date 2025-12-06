# Multi-Cloud Networking

Unified networking concepts and implementations across AWS, GCP, and Azure.

## Unified Concepts

| Concept | AWS | GCP | Azure |
|---------|-----|-----|-------|
| Virtual Network | VPC | VPC | Virtual Network (VNet) |
| Subnets | Subnets (AZ-scoped) | Subnets (Regional) | Subnets |
| NAT | NAT Gateway | Cloud NAT | NAT Gateway |
| Peering | VPC Peering | VPC Peering | VNet Peering |
| Hub-Spoke | Transit Gateway | Cloud Router | Virtual WAN |
| Private Endpoints | PrivateLink | Private Service Connect | Private Link |
| Hybrid VPN | VPN | Cloud VPN | VPN Gateway |
| Hybrid Dedicated | Direct Connect | Cloud Interconnect | ExpressRoute |

## Provider Best Practices

### AWS
- Multi-AZ baseline for production
- Prefer Transit Gateway for 5+ VPCs
- Use VPC Endpoints to avoid NAT charges

### GCP
- Custom mode VPC (not auto-mode)
- Start with single VPC, use Shared VPC for multi-project
- Grant network user role at subnet level

### Azure
- Hub-and-spoke network topology as standard
- Few large VNets vs many small VNets
- Private endpoints for Azure services

For detailed implementation examples, see `examples/aws/`, `examples/gcp/`, and `examples/azure/` directories.
