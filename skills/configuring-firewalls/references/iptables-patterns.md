# iptables Patterns Guide

iptables is the legacy Linux firewall tool. While nftables is recommended for new deployments, iptables is still widely used on older systems.


## Table of Contents

- [Why iptables Still Matters](#why-iptables-still-matters)
- [Basic Architecture](#basic-architecture)
- [Basic Commands](#basic-commands)
- [Basic Web Server Setup](#basic-web-server-setup)
- [Common Patterns](#common-patterns)
  - [SSH Rate Limiting](#ssh-rate-limiting)
  - [Allow from Specific IP](#allow-from-specific-ip)
  - [Port Forwarding (DNAT)](#port-forwarding-dnat)
  - [Masquerading (SNAT)](#masquerading-snat)
  - [Block Specific IP](#block-specific-ip)
- [Match Criteria](#match-criteria)
  - [Protocol](#protocol)
  - [Source/Destination](#sourcedestination)
  - [Interface](#interface)
  - [Connection State](#connection-state)
- [Persistence](#persistence)
  - [Debian/Ubuntu](#debianubuntu)
  - [RHEL/CentOS](#rhelcentos)
  - [Manual Save/Restore](#manual-saverestore)
- [Logging](#logging)
- [Testing](#testing)
- [Migration to nftables](#migration-to-nftables)
- [Complete Example Script](#complete-example-script)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Common Mistakes](#common-mistakes)
- [Resources](#resources)

## Why iptables Still Matters

- **Legacy Systems:** Required for kernels < 4.14
- **Existing Scripts:** Many organizations have extensive iptables automation
- **Documentation:** Extensive community knowledge and examples
- **Migration Path:** Understanding iptables helps migrate to nftables

**Recommendation:** Migrate to nftables when feasible for better performance and maintainability.

## Basic Architecture

```
Tables → Chains → Rules

Tables:
  - filter (default): Packet filtering
  - nat: Network address translation
  - mangle: Packet alteration
  - raw: Connection tracking exceptions

Chains:
  - INPUT: Incoming packets to local process
  - OUTPUT: Outgoing packets from local process
  - FORWARD: Packets being routed through system
  - PREROUTING: Packets before routing decision
  - POSTROUTING: Packets after routing decision
```

## Basic Commands

```bash
# List rules
sudo iptables -L -v -n

# List with line numbers
sudo iptables -L INPUT --line-numbers

# Add rule (-A append)
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Insert rule at position (-I insert)
sudo iptables -I INPUT 1 -p tcp --dport 22 -j ACCEPT

# Delete rule by number
sudo iptables -D INPUT 3

# Delete rule by specification
sudo iptables -D INPUT -p tcp --dport 80 -j ACCEPT

# Flush all rules (dangerous!)
sudo iptables -F
```

## Basic Web Server Setup

```bash
# Set default policies
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# Allow loopback
sudo iptables -A INPUT -i lo -j ACCEPT

# Allow established connections (stateful)
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow SSH
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Allow HTTPS
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow ICMP (ping)
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT

# Log dropped packets
sudo iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables-drop: " --log-level 7

# Save rules (Debian/Ubuntu)
sudo netfilter-persistent save

# Enable on boot
sudo systemctl enable netfilter-persistent
```

## Common Patterns

### SSH Rate Limiting

```bash
# Rate limit SSH (max 4 connections per 60 seconds per IP)
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 -j DROP
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

### Allow from Specific IP

```bash
# Allow SSH from office IP only
sudo iptables -A INPUT -p tcp -s 203.0.113.0/24 --dport 22 -j ACCEPT

# Allow PostgreSQL from app server
sudo iptables -A INPUT -p tcp -s 10.0.2.10 --dport 5432 -j ACCEPT
```

### Port Forwarding (DNAT)

```bash
# Forward external port 8080 to internal 80
sudo iptables -t nat -A PREROUTING -p tcp --dport 8080 -j REDIRECT --to-port 80

# Forward to different internal IP
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to-destination 192.168.1.10:8080
```

### Masquerading (SNAT)

```bash
# Enable masquerading on eth0 (for NAT gateway)
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Enable IP forwarding (required for NAT)
sudo sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
```

### Block Specific IP

```bash
# Block IP address
sudo iptables -A INPUT -s 198.51.100.50 -j DROP

# Block IP range
sudo iptables -A INPUT -s 198.51.100.0/24 -j DROP

# Block with rejection message
sudo iptables -A INPUT -s 198.51.100.50 -j REJECT
```

## Match Criteria

### Protocol

```bash
# TCP
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# UDP
sudo iptables -A INPUT -p udp --dport 53 -j ACCEPT

# ICMP
sudo iptables -A INPUT -p icmp -j ACCEPT
```

### Source/Destination

```bash
# Source IP
sudo iptables -A INPUT -s 192.168.1.100 -j ACCEPT

# Destination IP
sudo iptables -A INPUT -d 10.0.0.5 -j ACCEPT

# Source port
sudo iptables -A INPUT -p tcp --sport 1024:65535 -j ACCEPT

# Destination port
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Port range
sudo iptables -A INPUT -p tcp --dport 6000:6007 -j ACCEPT
```

### Interface

```bash
# Input interface
sudo iptables -A INPUT -i eth0 -j ACCEPT

# Output interface
sudo iptables -A OUTPUT -o eth1 -j ACCEPT
```

### Connection State

```bash
# Established and related
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# New connections
sudo iptables -A INPUT -p tcp --dport 80 -m conntrack --ctstate NEW -j ACCEPT

# Invalid packets
sudo iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
```

## Persistence

### Debian/Ubuntu

```bash
# Install persistence tool
sudo apt install iptables-persistent

# Save current rules
sudo netfilter-persistent save

# Rules saved to:
# /etc/iptables/rules.v4 (IPv4)
# /etc/iptables/rules.v6 (IPv6)

# Reload rules
sudo netfilter-persistent reload

# Enable on boot
sudo systemctl enable netfilter-persistent
```

### RHEL/CentOS

```bash
# Save rules
sudo service iptables save

# Rules saved to: /etc/sysconfig/iptables

# Enable on boot
sudo systemctl enable iptables
```

### Manual Save/Restore

```bash
# Save to file
sudo iptables-save > /etc/iptables/rules.v4

# Restore from file
sudo iptables-restore < /etc/iptables/rules.v4
```

## Logging

```bash
# Log before dropping
sudo iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables-drop: " --log-level 7
sudo iptables -A INPUT -j DROP

# View logs
sudo tail -f /var/log/syslog | grep "iptables-drop"
sudo dmesg | grep "iptables-drop"
```

## Testing

```bash
# List rules verbosely
sudo iptables -L -v -n

# Check packet counters
sudo iptables -L -v -n | grep "pkts"

# Reset counters
sudo iptables -Z

# Test with temporary rule
sudo iptables -I INPUT 1 -p tcp --dport 8080 -j LOG --log-prefix "test: "
# Check logs
sudo dmesg | grep "test:"
# Remove rule
sudo iptables -D INPUT 1
```

## Migration to nftables

```bash
# 1. Export iptables rules
sudo iptables-save > /tmp/iptables-rules.txt

# 2. Convert to nftables
sudo iptables-restore-translate -f /tmp/iptables-rules.txt > /tmp/nftables-rules.nft

# 3. Review converted rules
cat /tmp/nftables-rules.nft

# 4. Load nftables rules
sudo nft -f /tmp/nftables-rules.nft

# 5. Test (both running simultaneously for validation)
sudo nft list ruleset

# 6. Once confident, switch:
sudo systemctl stop iptables
sudo systemctl disable iptables
sudo iptables -F
sudo systemctl enable nftables
sudo systemctl start nftables
```

For detailed migration process, see the main SKILL.md migration guide section.

## Complete Example Script

```bash
#!/bin/bash
# iptables firewall script for web server

# Flush existing rules
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X

# Set default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Drop invalid packets
iptables -A INPUT -m conntrack --ctstate INVALID -j DROP

# Allow SSH with rate limiting
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 -j DROP
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow ICMP
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT

# Log dropped packets
iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables-drop: " --log-level 7

# Save rules
netfilter-persistent save

echo "Firewall configured successfully"
iptables -L -v -n
```

## Troubleshooting

**Rules not persisting after reboot:**
- Install and enable netfilter-persistent (Debian/Ubuntu) or iptables service (RHEL)
- Verify rules saved: `cat /etc/iptables/rules.v4`

**Can't connect after enabling firewall:**
- Check if service is listening: `ss -tuln`
- Verify rules: `sudo iptables -L INPUT -v -n`
- Temporarily disable: `sudo iptables -P INPUT ACCEPT`

**Performance issues:**
- Minimize number of rules
- Place frequently matched rules first
- Use connection tracking (--ctstate) for efficiency
- Consider migrating to nftables for better performance

## Best Practices

1. **Always allow SSH before setting DROP policy** - Prevent lockout
2. **Use connection tracking** - More efficient than per-packet checks
3. **Order matters** - First match wins, place specific rules before general
4. **Save rules** - Use netfilter-persistent for persistence
5. **Test before production** - Validate on non-critical system first
6. **Document rules** - Comment in script or external documentation
7. **Enable logging** - Use --limit to avoid log flooding
8. **Migrate to nftables** - Better performance, modern syntax

## Common Mistakes

❌ **Not saving rules** - Lost on reboot
❌ **Setting DROP policy before allowing SSH** - Lockout
❌ **Forgetting established/related** - Breaks two-way communication
❌ **No logging** - Can't debug connection issues
❌ **Too many rules** - Performance degradation

## Resources

- iptables man page: `man iptables`
- netfilter documentation: https://netfilter.org/documentation/
- For migration guide, see the main SKILL.md
