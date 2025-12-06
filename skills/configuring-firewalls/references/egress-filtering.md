# Egress Filtering Pattern

Control outbound traffic to prevent data exfiltration, malware communication, and unauthorized external access.


## Table of Contents

- [Why Egress Filtering?](#why-egress-filtering)
- [nftables Egress Filtering](#nftables-egress-filtering)
- [AWS Security Group Egress Restrictions](#aws-security-group-egress-restrictions)
- [Domain-Based Egress Filtering](#domain-based-egress-filtering)
  - [Squid Proxy Configuration](#squid-proxy-configuration)
- [Kubernetes Egress NetworkPolicy](#kubernetes-egress-networkpolicy)
- [Monitoring Egress Traffic](#monitoring-egress-traffic)
  - [VPC Flow Logs Analysis](#vpc-flow-logs-analysis)
  - [nftables Egress Logging](#nftables-egress-logging)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
  - [Database Server (Minimal Egress)](#database-server-minimal-egress)
  - [Application Server (Limited Egress)](#application-server-limited-egress)
- [Testing Egress Rules](#testing-egress-rules)
- [Egress Filtering for Different Tiers](#egress-filtering-for-different-tiers)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

## Why Egress Filtering?

**Threats Mitigated:**
- Data exfiltration by malware
- Command and control (C2) communication
- Unauthorized cloud storage uploads
- Crypto-mining to external pools

**Default Approach:** Deny all outbound, allow only necessary destinations.

## nftables Egress Filtering

```nftables
#!/usr/sbin/nft -f

flush ruleset

table inet filter {
    # Allowed external destinations
    set allowed_external {
        type ipv4_addr
        flags interval
        elements = {
            52.4.48.0/24,      # AWS API
            140.82.112.0/20,   # GitHub
            151.101.0.0/16     # Fastly CDN (package repos)
        }
    }

    # Allowed internal networks
    set internal_networks {
        type ipv4_addr
        flags interval
        elements = {
            10.0.0.0/8,
            172.16.0.0/12,
            192.168.0.0/16
        }
    }

    chain input {
        type filter hook input priority 0; policy drop;
        iif "lo" accept
        ct state established,related accept
        tcp dport { 22, 80, 443 } accept
    }

    chain output {
        type filter hook output priority 0; policy drop;

        oif "lo" accept
        ct state established,related accept

        # Allow DNS (required for name resolution)
        udp dport 53 accept
        tcp dport 53 accept

        # Allow to internal networks
        ip daddr @internal_networks accept

        # Allow to approved external destinations
        ip daddr @allowed_external accept

        # Allow HTTPS to specific domains (using IP sets)
        # Note: For domain-based filtering, use external tools (Squid, etc.)
        tcp dport 443 accept comment "HTTPS - add specific IPs above"

        # Log blocked egress attempts
        log prefix "egress-blocked: " limit rate 5/minute level warn

        # Drop everything else
        drop
    }
}
```

## AWS Security Group Egress Restrictions

```hcl
resource "aws_security_group" "restricted_egress" {
  name        = "restricted-egress-sg"
  description = "Restrictive egress firewall"
  vpc_id      = aws_vpc.main.id

  # NO default "allow all outbound" rule

  # Explicit egress rules only

  # Allow to internal VPC
  egress {
    description = "To VPC resources"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

  # Allow DNS
  egress {
    description = "DNS queries"
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTPS to specific service (e.g., AWS S3 endpoint)
  egress {
    description = "HTTPS to S3"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    prefix_list_ids = [data.aws_prefix_list.s3.id]
  }

  # Allow to specific external API
  egress {
    description = "To external API"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["52.1.2.0/24"]  # External API endpoint
  }

  tags = {
    Name = "restricted-egress-sg"
  }
}

# Use AWS managed prefix list for S3
data "aws_prefix_list" "s3" {
  filter {
    name   = "prefix-list-name"
    values = ["com.amazonaws.${var.region}.s3"]
  }
}
```

## Domain-Based Egress Filtering

For domain-based control (e.g., allow github.com), use a proxy:

### Squid Proxy Configuration

```bash
# Install Squid
sudo apt install squid

# Configure /etc/squid/squid.conf
acl allowed_domains dstdomain .github.com .npmjs.com .pypi.org
http_access allow allowed_domains
http_access deny all

# Restart Squid
sudo systemctl restart squid
```

Configure applications to use proxy:
```bash
export HTTP_PROXY=http://proxy-server:3128
export HTTPS_PROXY=http://proxy-server:3128
```

## Kubernetes Egress NetworkPolicy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: restrictive-egress
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Egress
  egress:
    # Allow DNS
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: UDP
          port: 53

    # Allow to internal pods
    - to:
        - podSelector: {}

    # Allow to specific external IP blocks
    - to:
        - ipBlock:
            cidr: 52.1.2.0/24  # External API
      ports:
        - protocol: TCP
          port: 443
```

## Monitoring Egress Traffic

### VPC Flow Logs Analysis

```sql
-- CloudWatch Insights query for egress traffic
fields @timestamp, srcAddr, dstAddr, dstPort, action
| filter action = "ACCEPT" and dstAddr not like /^10\./
| filter dstAddr not like /^172\.(1[6-9]|2[0-9]|3[01])\./
| filter dstAddr not like /^192\.168\./
| stats count() by dstAddr, dstPort
| sort count desc
| limit 50
```

### nftables Egress Logging

```nftables
# Add counter and log to egress rules
chain output {
    # ... other rules

    # Count and log blocked egress
    counter name egress_blocked_counter
    log prefix "egress-block: " flags all
    drop
}
```

View stats:
```bash
sudo nft list counter inet filter egress_blocked_counter
```

## Best Practices

1. **Default Deny:** Start with deny-all egress, allow explicitly
2. **Allow DNS:** Always allow DNS (port 53) or name resolution fails
3. **Internal Networks:** Allow RFC1918 private ranges
4. **Use Prefix Lists:** AWS managed prefix lists for services (S3, DynamoDB)
5. **Log Blocked Traffic:** Monitor for legitimate traffic being blocked
6. **Regular Reviews:** Audit allowed destinations quarterly
7. **Domain-Based:** Use proxy (Squid) for domain-based control
8. **Network Segmentation:** Different egress policies per tier

## Common Patterns

### Database Server (Minimal Egress)

```nftables
chain output {
    type filter hook output priority 0; policy drop;

    oif "lo" accept
    ct state established,related accept

    # DNS
    udp dport 53 accept

    # Internal network only
    ip daddr 10.0.0.0/8 accept

    # No Internet access at all
    log prefix "db-egress-block: "
    drop
}
```

### Application Server (Limited Egress)

```nftables
chain output {
    type filter hook output priority 0; policy drop;

    oif "lo" accept
    ct state established,related accept

    # DNS
    udp dport 53 accept

    # Internal
    ip daddr 10.0.0.0/8 accept

    # Specific external APIs
    ip daddr { 52.1.2.0/24, 140.82.112.0/20 } tcp dport 443 accept

    # Package repos (for updates)
    ip daddr 151.101.0.0/16 tcp dport 443 accept

    log prefix "app-egress-block: "
    drop
}
```

## Testing Egress Rules

```bash
# Test DNS resolution (should work)
nslookup google.com

# Test allowed external IP (should work)
curl https://api.example.com

# Test blocked destination (should fail)
curl https://blocked-site.com

# Check logs for blocked attempts
sudo journalctl -k | grep "egress-block"
```

## Egress Filtering for Different Tiers

| Tier | Egress Policy |
|------|--------------|
| **Web (DMZ)** | Internal + specific APIs + package repos |
| **App** | Internal + database + external APIs |
| **Database** | Internal only (no Internet) |
| **Bastion** | Minimal (internal SSH only) |

## Troubleshooting

**Application fails after enabling egress filtering:**
- Check logs for blocked connections
- Identify legitimate external dependencies
- Add to allow list
- Re-test

**DNS resolution fails:**
- Ensure UDP port 53 allowed
- Check if DNS server IP blocked
- Verify DNS server address: `cat /etc/resolv.conf`

**Package updates fail:**
- Allow package repository IPs
- For apt: Allow `archive.ubuntu.com`, `security.ubuntu.com`
- For yum: Allow `mirror.centos.org`

## Resources

- For nftables patterns, AWS Security Groups, and Kubernetes NetworkPolicies, see the main SKILL.md
