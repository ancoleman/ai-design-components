# Cost Optimization

Strategies for reducing cloud network infrastructure costs.

## Common Cost Drivers

### 1. NAT Gateway
- **Cost:** $0.045/hour + $0.045/GB data processed
- **Annual (3 AZs):** ~$1,150 (base) + data processing

**Optimization:**
- Use VPC Endpoints for AWS services (S3, DynamoDB)
- Single NAT Gateway for dev/test (accept availability risk)
- Centralized egress VPC pattern

### 2. Transit Gateway
- **Cost:** $0.05/hour/attachment + $0.02/GB
- **Annual (5 VPCs):** ~$2,190 (base) + data transfer

**Optimization:**
- Use VPC Peering for small number of VPCs (< 5)
- Direct peering for latency-sensitive pairs
- Avoid unnecessary Transit Gateway attachments

### 3. Data Transfer
- **Egress Costs:** Vary by destination
  - Same region: Free
  - Cross-region: $0.02/GB
  - To internet: $0.09/GB

**Optimization:**
- Keep traffic within same region
- Use VPC Endpoints instead of public internet
- Private connectivity for high-volume transfers

### 4. VPN / Direct Connect
- **VPN:** $0.05/hour + data transfer
- **Direct Connect:** Port fee + lower data transfer ($0.02/GB)

**Break-even:** Direct Connect cheaper if > 8 TB/month

## Cost Comparison Examples

### NAT Gateway Configuration (3 AZs)

| Pattern | Monthly Cost | Resilience |
|---------|--------------|------------|
| Single NAT | ~$32 | Low |
| NAT per AZ | ~$96 | High |
| Centralized Egress | ~$32-96 | Medium-High |

### VPN vs Direct Connect (10 TB/month)

| Solution | Monthly Cost |
|----------|--------------|
| VPN | ~$957 |
| Direct Connect 1 Gbps | ~$420 |

## Optimization Checklist

- [ ] Use VPC Endpoints for AWS services
- [ ] Right-size NAT Gateways (dev: single, prod: per AZ)
- [ ] Minimize cross-region traffic
- [ ] Use Transit Gateway only when needed (5+ VPCs)
- [ ] Monitor and alert on data transfer costs
- [ ] Review and remove unused resources monthly
