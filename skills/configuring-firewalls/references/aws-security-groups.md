# AWS Security Groups and Network ACLs Guide

Complete guide to AWS firewall controls with Terraform examples.


## Table of Contents

- [Security Groups vs Network ACLs](#security-groups-vs-network-acls)
- [Security Groups](#security-groups)
  - [Key Characteristics](#key-characteristics)
  - [Best Practices](#best-practices)
  - [Terraform Examples](#terraform-examples)
  - [Using Managed Prefix Lists](#using-managed-prefix-lists)
- [Network ACLs](#network-acls)
  - [Key Characteristics](#key-characteristics)
  - [Best Practices](#best-practices)
  - [Terraform Examples](#terraform-examples)
- [Ephemeral Ports Reference](#ephemeral-ports-reference)
- [VPC Flow Logs](#vpc-flow-logs)
- [Defense-in-Depth Strategy](#defense-in-depth-strategy)
- [Common Patterns](#common-patterns)
  - [Three-Tier Architecture](#three-tier-architecture)
  - [Bastion Access](#bastion-access)
  - [Load Balancer](#load-balancer)
- [Troubleshooting](#troubleshooting)
- [AWS CLI Examples](#aws-cli-examples)
- [Infrastructure as Code Best Practices](#infrastructure-as-code-best-practices)

## Security Groups vs Network ACLs

| Feature | Security Groups | Network ACLs |
|---------|----------------|--------------|
| **Level** | Instance (ENI) | Subnet |
| **State** | Stateful | Stateless |
| **Rules** | Allow only | Allow + Deny |
| **Evaluation** | All rules evaluated | Sequential (order matters) |
| **Default** | Deny inbound, allow outbound | Allow all |
| **Return Traffic** | Automatic | Must explicitly allow |
| **Use Case** | Resource-specific control | Subnet-wide policies |
| **Rule Limit** | 60 inbound + 60 outbound per SG | 20 inbound + 20 outbound per NACL |

## Security Groups

### Key Characteristics

**Stateful Behavior:**
- Outbound response traffic automatically allowed
- No need to configure ephemeral ports
- Simpler configuration

**Rule Evaluation:**
- All rules evaluated (most permissive wins)
- No rule ordering required
- Cannot create explicit deny rules

**Scope:**
- Attached to Elastic Network Interfaces (ENIs)
- Multiple SGs per instance (up to 5)
- Multiple instances per SG

### Best Practices

1. **Principle of Least Privilege** - Only open required ports
2. **Dedicated SGs by Function** - Separate web, app, database SGs
3. **Reference SGs, Not IPs** - Use SG IDs for internal communication
4. **Descriptive Names** - Use clear, searchable names
5. **Description for Every Rule** - Document purpose
6. **Avoid Default SG** - Create custom SGs for active resources
7. **Use Managed Prefix Lists** - For IP grouping
8. **Regular Audits** - Quarterly review, remove unused rules
9. **Infrastructure as Code** - Terraform/CloudFormation
10. **Enable VPC Flow Logs** - Monitor actual traffic

### Terraform Examples

#### Basic Web Server

```hcl
resource "aws_security_group" "web" {
  name        = "web-server-sg"
  description = "Security group for public web servers"
  vpc_id      = aws_vpc.main.id

  # Inbound rules
  ingress {
    description = "HTTP from Internet"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS from Internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description     = "SSH from bastion only"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]  # Reference another SG
  }

  # Outbound rules
  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # All protocols
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "web-server-sg"
    Environment = "production"
    Tier        = "web"
  }
}
```

#### Application Server (Private)

```hcl
resource "aws_security_group" "app" {
  name        = "app-server-sg"
  description = "Security group for application servers in private subnet"
  vpc_id      = aws_vpc.main.id

  # Allow traffic from web tier
  ingress {
    description     = "HTTP from web tier"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }

  # SSH from bastion
  ingress {
    description     = "SSH from bastion"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]
  }

  # Outbound to database
  egress {
    description     = "PostgreSQL to database"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.database.id]
  }

  # Outbound HTTPS for API calls
  egress {
    description = "HTTPS to Internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # DNS
  egress {
    description = "DNS"
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "app-server-sg"
    Environment = "production"
    Tier        = "app"
  }
}
```

#### Database (RDS/Private)

```hcl
resource "aws_security_group" "database" {
  name        = "database-sg"
  description = "Security group for RDS PostgreSQL database"
  vpc_id      = aws_vpc.main.id

  # Only allow from app tier
  ingress {
    description     = "PostgreSQL from app servers"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  # SSH from bastion (if using EC2, not RDS)
  ingress {
    description     = "SSH from bastion"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]
  }

  # Minimal outbound (database typically doesn't need Internet)
  egress {
    description = "Local VPC only"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

  tags = {
    Name        = "database-sg"
    Environment = "production"
    Tier        = "data"
  }
}
```

#### Bastion Host

```hcl
resource "aws_security_group" "bastion" {
  name        = "bastion-sg"
  description = "Security group for bastion host (jump box)"
  vpc_id      = aws_vpc.main.id

  # Allow SSH from office/VPN only
  ingress {
    description = "SSH from office"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.office_ip_ranges  # ["203.0.113.0/24"]
  }

  # Outbound SSH to private instances
  egress {
    description = "SSH to private instances"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

  # HTTPS for updates
  egress {
    description = "HTTPS for package updates"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "bastion-sg"
    Environment = "production"
  }
}
```

### Using Managed Prefix Lists

Managed Prefix Lists allow grouping multiple CIDRs:

```hcl
resource "aws_ec2_managed_prefix_list" "office_ips" {
  name           = "office-ip-ranges"
  address_family = "IPv4"
  max_entries    = 10

  entry {
    cidr        = "203.0.113.0/24"
    description = "HQ Office"
  }

  entry {
    cidr        = "198.51.100.0/24"
    description = "Remote Office"
  }

  tags = {
    Name = "office-ips"
  }
}

resource "aws_security_group" "example" {
  # ... other config

  ingress {
    description     = "SSH from office"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    prefix_list_ids = [aws_ec2_managed_prefix_list.office_ips.id]
  }
}
```

## Network ACLs

### Key Characteristics

**Stateless Behavior:**
- Must explicitly allow return traffic
- Must configure ephemeral ports (1024-65535)
- More complex configuration

**Rule Evaluation:**
- Sequential (lowest number first)
- First match wins
- Can create explicit deny rules

**Scope:**
- Applied at subnet level
- One NACL per subnet
- Affects all instances in subnet

### Best Practices

1. **Use NACLs as Secondary Defense** - Primary control via Security Groups
2. **Separate NACLs for Public/Private Subnets** - Different security postures
3. **Number Rules by 100s** - Allows easy insertion (100, 200, 300)
4. **Place Deny Rules First** - Lower numbers = higher priority
5. **Remember Ephemeral Ports** - 1024-65535 for return traffic
6. **Separate IPv4 and IPv6 Rules** - Different rule numbers
7. **Limit Rule Count** - Performance impact with many rules
8. **Include ELB Health Checks** - Don't block load balancer ranges
9. **Document Rule Purpose** - Use descriptions in Terraform

### Terraform Examples

#### Public Subnet NACL

```hcl
resource "aws_network_acl" "public" {
  vpc_id     = aws_vpc.main.id
  subnet_ids = aws_subnet.public[*].id

  # Inbound rules

  # Rule 100: Allow HTTP
  ingress {
    rule_no    = 100
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 80
    to_port    = 80
  }

  # Rule 110: Allow HTTPS
  ingress {
    rule_no    = 110
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 443
    to_port    = 443
  }

  # Rule 120: Allow SSH from office
  ingress {
    rule_no    = 120
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "203.0.113.0/24"
    from_port  = 22
    to_port    = 22
  }

  # Rule 130: CRITICAL - Allow ephemeral ports (return traffic)
  ingress {
    rule_no    = 130
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 1024
    to_port    = 65535
  }

  # Rule 200: Deny specific malicious IP
  ingress {
    rule_no    = 200
    protocol   = "-1"
    action     = "deny"
    cidr_block = "198.51.100.0/24"
    from_port  = 0
    to_port    = 0
  }

  # Default deny (implicit rule *)

  # Outbound rules

  # Rule 100: Allow HTTP outbound
  egress {
    rule_no    = 100
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 80
    to_port    = 80
  }

  # Rule 110: Allow HTTPS outbound
  egress {
    rule_no    = 110
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 443
    to_port    = 443
  }

  # Rule 120: Allow ephemeral ports (response traffic)
  egress {
    rule_no    = 120
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 1024
    to_port    = 65535
  }

  tags = {
    Name = "public-subnet-nacl"
  }
}
```

#### Private Subnet NACL

```hcl
resource "aws_network_acl" "private" {
  vpc_id     = aws_vpc.main.id
  subnet_ids = aws_subnet.private[*].id

  # Inbound from VPC only

  # Rule 100: Allow all from VPC
  ingress {
    rule_no    = 100
    protocol   = "-1"
    action     = "allow"
    cidr_block = aws_vpc.main.cidr_block
    from_port  = 0
    to_port    = 0
  }

  # Rule 110: Allow ephemeral ports from Internet (for responses)
  ingress {
    rule_no    = 110
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 1024
    to_port    = 65535
  }

  # Outbound

  # Rule 100: Allow all to VPC
  egress {
    rule_no    = 100
    protocol   = "-1"
    action     = "allow"
    cidr_block = aws_vpc.main.cidr_block
    from_port  = 0
    to_port    = 0
  }

  # Rule 110: Allow HTTPS to Internet (for updates)
  egress {
    rule_no    = 110
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 443
    to_port    = 443
  }

  # Rule 120: Allow DNS
  egress {
    rule_no    = 120
    protocol   = "udp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 53
    to_port    = 53
  }

  # Rule 130: Allow ephemeral ports outbound
  egress {
    rule_no    = 130
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 1024
    to_port    = 65535
  }

  tags = {
    Name = "private-subnet-nacl"
  }
}
```

## Ephemeral Ports Reference

Different operating systems use different ephemeral port ranges:

- **Linux:** 32768-60999 (can be narrower: 32768-65535)
- **Windows Server 2008+:** 49152-65535
- **NAT Gateway:** 1024-65535
- **Application Load Balancer:** 1024-65535

**Best Practice for NACLs:** Allow 1024-65535 to cover all cases.

## VPC Flow Logs

Enable Flow Logs to monitor traffic and validate firewall rules:

```hcl
resource "aws_flow_log" "main" {
  vpc_id          = aws_vpc.main.id
  traffic_type    = "ALL"  # ACCEPT, REJECT, or ALL
  iam_role_arn    = aws_iam_role.flow_logs.arn
  log_destination = aws_cloudwatch_log_group.flow_logs.arn

  tags = {
    Name = "vpc-flow-logs"
  }
}

resource "aws_cloudwatch_log_group" "flow_logs" {
  name              = "/aws/vpc/flow-logs"
  retention_in_days = 30
}
```

Query with CloudWatch Insights:

```sql
fields @timestamp, srcAddr, dstAddr, srcPort, dstPort, protocol, action
| filter action = "REJECT"
| sort @timestamp desc
| limit 100
```

## Defense-in-Depth Strategy

Combine Security Groups and NACLs:

```
Internet
    │
    ├─ Public Subnet NACL (Layer 1: Subnet-wide)
    │   └─ Web Server Security Group (Layer 2: Instance-specific)
    │       └─ EC2 Instance
    │
    ├─ Private Subnet NACL (Layer 1)
    │   └─ App Server Security Group (Layer 2)
    │       └─ EC2 Instance
    │
    └─ Private Subnet NACL (Layer 1)
        └─ Database Security Group (Layer 2)
            └─ RDS Instance
```

**Strategy:**
- **Security Groups:** Primary control (allow required traffic)
- **NACLs:** Secondary enforcement (block known threats, enforce subnet policies)

## Common Patterns

### Three-Tier Architecture

See examples above: Web → App → Database with proper SG/NACL layering.

### Bastion Access

1. Bastion SG allows SSH from office IP
2. Private instance SGs allow SSH from bastion SG only
3. No direct Internet access to private instances

### Load Balancer

```hcl
resource "aws_security_group" "alb" {
  name        = "alb-sg"
  description = "Security group for Application Load Balancer"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTPS from Internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description     = "To target instances"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }
}

# Web server SG allows traffic from ALB
resource "aws_security_group" "web" {
  # ...
  ingress {
    description     = "HTTP from ALB"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }
}
```

## Troubleshooting

**Security Group not blocking traffic:**
- Remember: SGs are stateful (return traffic auto-allowed)
- All rules evaluated (can't have conflicting allow/deny)
- Check if multiple SGs attached to instance

**NACL blocking expected traffic:**
- Check rule order (lowest number first)
- Verify ephemeral ports allowed (1024-65535)
- Confirm both inbound AND outbound rules
- Check for explicit deny rules with lower numbers

**Can't SSH to instance:**
- Check SG allows SSH from your IP
- Check NACL allows SSH inbound and ephemeral ports outbound
- Verify instance has public IP (or accessible via bastion)
- Check route table and Internet Gateway

**VPC Flow Logs showing rejected traffic:**
- Filter by action=REJECT
- Check source/dest IP, port, protocol
- Correlate with SG/NACL rules
- Common: Missing ephemeral ports in NACL

## AWS CLI Examples

```bash
# List security groups
aws ec2 describe-security-groups

# List security group rules
aws ec2 describe-security-group-rules --filters Name=group-id,Values=sg-xxxxx

# Add inbound rule
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

# Remove rule
aws ec2 revoke-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

# List NACLs
aws ec2 describe-network-acls

# Describe specific NACL
aws ec2 describe-network-acls --network-acl-ids acl-xxxxx
```

## Infrastructure as Code Best Practices

1. **Use Terraform Modules** - Reusable SG definitions
2. **Parameterize CIDRs** - Use variables for IP ranges
3. **Tag Everything** - Name, Environment, Tier, Owner
4. **Plan Before Apply** - Review changes
5. **State Management** - Use remote state (S3 + DynamoDB)
6. **Separate Environments** - Different workspaces/accounts
7. **Version Control** - Git with meaningful commits
8. **Code Review** - Security-critical changes reviewed
9. **Automated Testing** - Validate rules with Terraform tests
10. **Documentation** - README with architecture diagrams
