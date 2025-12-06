# DMZ (Demilitarized Zone) Pattern

DMZ architecture isolates public-facing services from internal networks, providing an additional security layer.


## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Key Principles](#key-principles)
- [AWS Implementation](#aws-implementation)
  - [VPC and Subnet Setup](#vpc-and-subnet-setup)
  - [DMZ Security Group](#dmz-security-group)
  - [DMZ Network ACL](#dmz-network-acl)
- [On-Premise DMZ (nftables)](#on-premise-dmz-nftables)
  - [DMZ Firewall](#dmz-firewall)
- [Monitoring DMZ Traffic](#monitoring-dmz-traffic)
  - [VPC Flow Logs](#vpc-flow-logs)
  - [CloudWatch Alarms](#cloudwatch-alarms)
- [Best Practices](#best-practices)
- [Common DMZ Mistakes](#common-dmz-mistakes)
- [DMZ vs Bastion Host](#dmz-vs-bastion-host)
- [Testing DMZ Configuration](#testing-dmz-configuration)
- [Resources](#resources)

## Architecture Overview

```
Internet
    │
    ▼
┌───────────────────────────┐
│ Public Subnet (DMZ)       │  ← Web/API servers, Load Balancers
│ - Accepts Internet traffic│
│ - Limited outbound access │
│ - Heavily monitored       │
└───────────┬───────────────┘
            │
            ▼ (One-way: DMZ → App)
┌───────────────────────────┐
│ Private Subnet (App Tier) │  ← Application servers
│ - No direct Internet      │
│ - Accepts from DMZ only   │
└───────────┬───────────────┘
            │
            ▼ (One-way: App → Data)
┌───────────────────────────┐
│ Private Subnet (Data Tier)│  ← Databases
│ - No Internet access      │
│ - Accepts from App only   │
└───────────────────────────┘
```

## Key Principles

1. **Network Segmentation:** Separate subnets for each tier
2. **Controlled Connectivity:** DMZ can't directly access database
3. **Minimal Exposure:** Only necessary ports open externally
4. **Layered Firewall Rules:** NACLs + Security Groups (AWS) or equivalent
5. **Monitoring:** Extra logging and alerting for DMZ traffic

## AWS Implementation

### VPC and Subnet Setup

```hcl
# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "dmz-vpc"
  }
}

# DMZ Subnet (Public)
resource "aws_subnet" "dmz" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"

  tags = {
    Name = "dmz-subnet"
    Tier = "dmz"
  }
}

# App Subnet (Private)
resource "aws_subnet" "app" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "app-subnet"
    Tier = "app"
  }
}

# Data Subnet (Private)
resource "aws_subnet" "data" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "data-subnet"
    Tier = "data"
  }
}

# Internet Gateway for DMZ
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "dmz-igw"
  }
}

# NAT Gateway for private subnets (optional)
resource "aws_eip" "nat" {
  domain = "vpc"
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.dmz.id

  tags = {
    Name = "dmz-nat-gw"
  }
}
```

### DMZ Security Group

```hcl
resource "aws_security_group" "dmz_web" {
  name        = "dmz-web-sg"
  description = "DMZ web servers (public-facing)"
  vpc_id      = aws_vpc.main.id

  # Inbound: HTTPS from Internet
  ingress {
    description = "HTTPS from Internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Inbound: HTTP (redirect to HTTPS)
  ingress {
    description = "HTTP from Internet"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound: To app tier only (no general Internet)
  egress {
    description = "To app tier"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["10.0.2.0/24"]  # App subnet
  }

  # Outbound: DNS
  egress {
    description = "DNS"
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound: HTTPS for external APIs (if needed)
  egress {
    description = "HTTPS for external APIs"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "dmz-web-sg"
    Tier = "dmz"
  }
}
```

### DMZ Network ACL

```hcl
resource "aws_network_acl" "dmz" {
  vpc_id     = aws_vpc.main.id
  subnet_ids = [aws_subnet.dmz.id]

  # Inbound rules

  # Rule 100: Allow HTTPS
  ingress {
    rule_no    = 100
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 443
    to_port    = 443
  }

  # Rule 110: Allow HTTP
  ingress {
    rule_no    = 110
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 80
    to_port    = 80
  }

  # Rule 120: Allow responses from app tier
  ingress {
    rule_no    = 120
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "10.0.2.0/24"  # App subnet
    from_port  = 1024
    to_port    = 65535
  }

  # Rule 130: Allow ephemeral ports from Internet
  ingress {
    rule_no    = 130
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 1024
    to_port    = 65535
  }

  # Rule 200: Deny known malicious IP
  ingress {
    rule_no    = 200
    protocol   = "-1"
    action     = "deny"
    cidr_block = "198.51.100.0/24"
    from_port  = 0
    to_port    = 0
  }

  # Outbound rules

  # Rule 100: To app tier
  egress {
    rule_no    = 100
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "10.0.2.0/24"
    from_port  = 8080
    to_port    = 8080
  }

  # Rule 110: HTTPS to Internet
  egress {
    rule_no    = 110
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 443
    to_port    = 443
  }

  # Rule 120: Ephemeral ports to Internet
  egress {
    rule_no    = 120
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 1024
    to_port    = 65535
  }

  # Rule 130: DNS
  egress {
    rule_no    = 130
    protocol   = "udp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 53
    to_port    = 53
  }

  tags = {
    Name = "dmz-nacl"
  }
}
```

## On-Premise DMZ (nftables)

### DMZ Firewall

```nftables
#!/usr/sbin/nft -f
# DMZ firewall on web server

flush ruleset

table inet filter {
    # App tier IPs (backend servers)
    set app_tier {
        type ipv4_addr
        elements = { 10.0.2.10, 10.0.2.11, 10.0.2.12 }
    }

    chain input {
        type filter hook input priority 0; policy drop;

        iif "lo" accept
        ct state established,related accept
        ct state invalid drop

        # Accept HTTPS from Internet
        tcp dport { 80, 443 } accept

        # Accept SSH from bastion only (not from Internet)
        tcp dport 22 ip saddr 10.0.1.5 accept

        # Log dropped
        log prefix "dmz-drop: " limit rate 5/minute
    }

    chain forward {
        type filter hook forward priority 0; policy drop;
        # No forwarding on DMZ server itself
    }

    chain output {
        type filter hook output priority 0; policy drop;

        oif "lo" accept
        ct state established,related accept

        # Allow to app tier
        tcp dport 8080 ip daddr @app_tier accept

        # Allow DNS
        udp dport 53 accept

        # Allow HTTPS for external APIs (if needed)
        tcp dport 443 accept

        # Block everything else (including direct database access)
        log prefix "dmz-egress-block: " limit rate 2/minute
    }
}
```

## Monitoring DMZ Traffic

### VPC Flow Logs

```hcl
resource "aws_flow_log" "dmz" {
  vpc_id          = aws_vpc.main.id
  traffic_type    = "ALL"
  iam_role_arn    = aws_iam_role.flow_logs.arn
  log_destination = aws_cloudwatch_log_group.dmz_flow_logs.arn

  tags = {
    Name = "dmz-flow-logs"
  }
}

resource "aws_cloudwatch_log_group" "dmz_flow_logs" {
  name              = "/aws/vpc/dmz-flow-logs"
  retention_in_days = 30
}
```

### CloudWatch Alarms

```hcl
# Alert on rejected connections to DMZ
resource "aws_cloudwatch_log_metric_filter" "dmz_rejected" {
  name           = "dmz-rejected-connections"
  log_group_name = aws_cloudwatch_log_group.dmz_flow_logs.name
  pattern        = "[version, account, eni, source, destination, srcport, destport, protocol, packets, bytes, windowstart, windowend, action=REJECT, flowlogstatus]"

  metric_transformation {
    name      = "DMZRejectedConnections"
    namespace = "DMZ"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "dmz_rejected" {
  alarm_name          = "dmz-high-rejected-connections"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "DMZRejectedConnections"
  namespace           = "DMZ"
  period              = "300"
  statistic           = "Sum"
  threshold           = "100"
  alarm_description   = "High number of rejected connections to DMZ"
  alarm_actions       = [aws_sns_topic.alerts.arn]
}
```

## Best Practices

1. **Principle of Least Privilege:** DMZ can't directly access database
2. **No Internet from Private Tiers:** App/Data tiers use NAT Gateway for updates
3. **Bastion for SSH:** No direct SSH to DMZ from Internet
4. **WAF for DMZ:** Use AWS WAF or similar for web protection
5. **IDS/IPS:** Deploy intrusion detection in DMZ
6. **Regular Audits:** Review DMZ traffic patterns monthly
7. **Separate Logging:** Enhanced logging for DMZ tier
8. **Automated Scanning:** Regular vulnerability scans of DMZ instances

## Common DMZ Mistakes

❌ **DMZ to Database:** DMZ should never directly connect to database
❌ **No Egress Filtering:** DMZ should have restricted outbound access
❌ **Weak Monitoring:** DMZ needs extra scrutiny
❌ **Single Layer:** DMZ needs both NACLs and Security Groups
❌ **No WAF:** Public-facing web servers should have WAF

## DMZ vs Bastion Host

**DMZ:** Isolates public services (web, API)
**Bastion:** Single entry point for administrative access

Often deployed together:
- DMZ: Public subnet with web servers
- Bastion: Public subnet with hardened jump box
- App/Data: Private subnets, accessible via bastion

## Testing DMZ Configuration

```bash
# From Internet: Should access web services
curl https://dmz-server.example.com

# From DMZ: Should reach app tier
curl http://app-server:8080/health

# From DMZ: Should NOT reach database directly
telnet database-server 5432  # Should fail

# From App tier: Should reach database
psql -h database-server -U app_user -d mydb  # Should succeed
```

## Resources

- AWS VPC Design: https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario3.html
- For nftables patterns and AWS Security Groups, see the main SKILL.md
