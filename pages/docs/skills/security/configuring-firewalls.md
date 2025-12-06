---
sidebar_position: 5
title: Configuring Firewalls
description: Configure host-based firewalls, cloud security groups, and network policies
tags: [security, firewall, iptables, nftables, ufw, aws, security-groups, kubernetes]
---

# Configuring Firewalls

Guide engineers through configuring firewalls across host-based (iptables, nftables, UFW), cloud-based (AWS Security Groups, NACLs), and container-based (Kubernetes NetworkPolicies) environments with practical rule examples and safety patterns.

## When to Use

Use this skill when:
- Initial server setup and hardening
- Exposing a new service (web server, API, database)
- Implementing network segmentation
- Creating bastion host or jump box
- Migrating from iptables to nftables
- Configuring cloud security groups
- Troubleshooting connectivity issues
- Implementing defense-in-depth strategies

## Key Features

**Tool Selection Framework:**
- **Ubuntu/Debian + Simplicity**: UFW (Uncomplicated Firewall)
- **RHEL/CentOS/Fedora**: firewalld (default on Red Hat ecosystem)
- **Modern Distro + Advanced**: nftables (O(log n) performance, unified syntax)
- **Legacy Systems**: iptables (migrate to nftables when feasible)
- **AWS**: Security Groups (stateful) + Network ACLs (stateless)
- **Kubernetes**: NetworkPolicies (requires CNI: Calico, Cilium, Weave)

**Common Patterns:**
- **Web Server**: Allow HTTP/HTTPS from anywhere, SSH from bastion only
- **Database Server**: Allow DB port from app tier only, no public access
- **Bastion Host**: Single hardened entry point for SSH access
- **Egress Filtering**: Control outbound traffic to prevent data exfiltration

**Safety Checklist:**
- Always allow SSH before enabling firewall (prevent lockout)
- Test rules before enabling (dry-run when possible)
- Enable logging for debugging
- Document rules in version control (Git)
- Verify externally with nmap
- Have console access (cloud) or physical access (on-prem)

## Quick Start

```bash
# UFW (Ubuntu/Debian)
# 1. Set defaults
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 2. CRITICAL: Allow SSH before enabling
sudo ufw allow ssh
sudo ufw limit ssh  # Rate-limit to prevent brute force

# 3. Allow web traffic
sudo ufw allow http    # Port 80
sudo ufw allow https   # Port 443

# 4. Allow from specific IP (database access)
sudo ufw allow from 192.168.1.100 to any port 5432

# 5. Enable firewall
sudo ufw enable

# 6. Verify rules
sudo ufw status verbose
```

**nftables (Modern Linux):**

```nftables
#!/usr/sbin/nft -f
# /etc/nftables.conf

flush ruleset

table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;

        # Accept loopback
        iif "lo" accept

        # Accept established connections (stateful)
        ct state established,related accept

        # Drop invalid packets
        ct state invalid drop

        # Allow SSH
        tcp dport 22 accept

        # Allow HTTP/HTTPS
        tcp dport { 80, 443 } accept

        # Log dropped packets
        log prefix "nftables-drop: " drop
    }

    chain forward {
        type filter hook forward priority 0; policy drop;
    }

    chain output {
        type filter hook output priority 0; policy accept;
    }
}
```

**AWS Security Groups (Terraform):**

```hcl
# Web server security group
resource "aws_security_group" "web" {
  name        = "web-server-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  # Allow HTTP/HTTPS from anywhere
  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow SSH from bastion only
  ingress {
    description     = "SSH from bastion"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]
  }

  # Allow all outbound
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web-server-sg"
  }
}
```

**Kubernetes NetworkPolicy (Default Deny):**

```yaml
# Deny all ingress traffic by default
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```

## Universal Best Practices

1. **Default Deny**: Start with deny-all, explicitly allow required traffic
2. **Principle of Least Privilege**: Only open necessary ports/IPs
3. **No 0.0.0.0/0 on Sensitive Ports**: Never allow SSH/RDP/database from anywhere
4. **Version Control**: Store firewall rules in Git
5. **Logging**: Enable and monitor firewall logs
6. **Regular Audits**: Review rules quarterly, remove unused
7. **Don't Mix Tools**: Avoid running iptables and nftables simultaneously
8. **Test Before Production**: Use staging environment first

## Troubleshooting

**Locked out via SSH:**
- Cloud: Use console/session manager to access
- On-prem: Physical console access or IPMI/iLO
- Prevention: Always allow SSH before enabling firewall

**Connection timeouts:**
- Check firewall status: `sudo ufw status` or `sudo nft list ruleset`
- Verify service is listening: `ss -tuln | grep <port>`
- Test externally: `nmap -Pn <ip> -p <port>`
- Check logs: `/var/log/ufw.log` or `journalctl -u nftables`

**AWS ephemeral port issues:**
- NACLs need return traffic: Allow 1024-65535 inbound
- Security Groups are stateful (no ephemeral config needed)

**Kubernetes pods can't communicate:**
- Check NetworkPolicies: `kubectl get networkpolicies -n <namespace>`
- Verify CNI plugin supports NetworkPolicies (Calico, Cilium)
- Test without policies first

## Related Skills

- [Security Hardening](./security-hardening.md) - Comprehensive server hardening including SSH, fail2ban, SELinux
- [Security Architecture](./architecting-security.md) - Strategic network security design
- [Implementing TLS](./implementing-tls.md) - Secure communications through firewalls
- [SIEM Logging](./siem-logging.md) - Monitor and alert on firewall events

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/configuring-firewalls)
- [Master Plan](../../master-plans/security/configuring-firewalls.md)
