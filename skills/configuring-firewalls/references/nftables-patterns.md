# nftables Patterns Guide

nftables is the modern Linux firewall framework, replacing iptables with improved performance and unified syntax for IPv4, IPv6, and NAT.


## Table of Contents

- [Why nftables?](#why-nftables)
- [Installation](#installation)
- [Basic Architecture](#basic-architecture)
- [Basic Ruleset](#basic-ruleset)
- [Loading and Managing Rules](#loading-and-managing-rules)
- [Rule Syntax](#rule-syntax)
  - [Basic Match Criteria](#basic-match-criteria)
  - [Multiple Ports (Sets)](#multiple-ports-sets)
  - [Connection State](#connection-state)
- [Named Sets (Reusable)](#named-sets-reusable)
  - [Dynamic Sets (Runtime Updates)](#dynamic-sets-runtime-updates)
- [Maps (Key-Value Rules)](#maps-key-value-rules)
- [Logging](#logging)
- [NAT (Network Address Translation)](#nat-network-address-translation)
  - [Source NAT (SNAT) - Masquerading](#source-nat-snat-masquerading)
  - [Destination NAT (DNAT) - Port Forwarding](#destination-nat-dnat-port-forwarding)
- [Rate Limiting](#rate-limiting)
- [Verdicts](#verdicts)
- [Complete Examples](#complete-examples)
  - [Web Server](#web-server)
  - [Database Server (Restricted)](#database-server-restricted)
  - [Egress Filtering](#egress-filtering)
- [Debugging and Tracing](#debugging-and-tracing)
- [Migration from iptables](#migration-from-iptables)
- [Best Practices](#best-practices)
- [Performance Tips](#performance-tips)
- [Configuration Files](#configuration-files)
- [Common Errors](#common-errors)

## Why nftables?

- **Performance:** O(log n) vs iptables O(n) linear processing
- **Unified Syntax:** Single tool for IPv4, IPv6, NAT, filtering
- **Built-in Sets/Maps:** No external ipset required
- **Transaction-based:** Atomic updates, no partial rule states
- **Advanced Debugging:** Built-in tracing for troubleshooting
- **Default on Modern Distros:** RHEL 8+, Debian 11+, Ubuntu 22.04+

## Installation

```bash
# Debian/Ubuntu
sudo apt install nftables

# RHEL/CentOS/Fedora
sudo dnf install nftables

# Enable on boot
sudo systemctl enable nftables
sudo systemctl start nftables
```

## Basic Architecture

```
Tables (inet, ip, ip6, arp, bridge)
  └─ Chains (input, output, forward, prerouting, postrouting)
      └─ Rules (match criteria → verdict)
```

**Table Families:**
- `inet` - IPv4 + IPv6 (recommended)
- `ip` - IPv4 only
- `ip6` - IPv6 only
- `arp` - ARP packets
- `bridge` - Bridge traffic

## Basic Ruleset

Create `/etc/nftables.conf`:

```nftables
#!/usr/sbin/nft -f

# Flush existing rules
flush ruleset

# Define table (inet = IPv4 + IPv6)
table inet filter {
    # Input chain (incoming traffic)
    chain input {
        type filter hook input priority 0; policy drop;

        # Accept loopback
        iif "lo" accept

        # Accept established/related connections (stateful)
        ct state established,related accept

        # Drop invalid packets
        ct state invalid drop

        # Allow ICMP (ping)
        meta l4proto icmp accept
        meta l4proto ipv6-icmp accept

        # Allow SSH (port 22)
        tcp dport 22 accept

        # Allow HTTP/HTTPS
        tcp dport { 80, 443 } accept

        # Log and drop everything else
        log prefix "nftables-drop: " drop
    }

    # Forward chain (for routing/NAT)
    chain forward {
        type filter hook forward priority 0; policy drop;
    }

    # Output chain (outgoing traffic)
    chain output {
        type filter hook output priority 0; policy accept;
    }
}
```

## Loading and Managing Rules

```bash
# Load ruleset from file
sudo nft -f /etc/nftables.conf

# List current ruleset
sudo nft list ruleset

# List specific table
sudo nft list table inet filter

# List specific chain
sudo nft list chain inet filter input

# Flush all rules
sudo nft flush ruleset

# Flush specific table
sudo nft flush table inet filter

# Enable persistence
sudo systemctl enable nftables
```

## Rule Syntax

### Basic Match Criteria

```nftables
# Protocol matching
tcp dport 80 accept
udp dport 53 accept
meta l4proto icmp accept

# IP address matching
ip saddr 192.168.1.100 accept
ip daddr 10.0.0.0/8 accept

# Interface matching
iif "eth0" accept
oif "eth1" accept

# Port matching
tcp dport 22 accept
tcp sport 1024-65535 accept
```

### Multiple Ports (Sets)

```nftables
# Anonymous set (inline)
tcp dport { 80, 443, 8080 } accept

# Port range
tcp dport 6000-6007 accept
```

### Connection State

```nftables
# Accept established connections
ct state established,related accept

# Drop invalid packets
ct state invalid drop

# Accept new SSH connections
tcp dport 22 ct state new accept
```

## Named Sets (Reusable)

Define sets for IP addresses or ports:

```nftables
table inet filter {
    # Define set of allowed IPs
    set allowed_ips {
        type ipv4_addr
        elements = { 192.168.1.100, 203.0.113.50, 203.0.113.60 }
    }

    # Define set of admin IPs
    set admin_ips {
        type ipv4_addr
        flags interval  # Allow CIDR ranges
        elements = { 10.0.0.0/8, 192.168.0.0/16 }
    }

    # Define set of allowed ports
    set allowed_ports {
        type inet_service
        elements = { 80, 443, 8080 }
    }

    chain input {
        type filter hook input priority 0; policy drop;

        # Allow SSH only from allowed IPs
        tcp dport 22 ip saddr @allowed_ips accept

        # Allow HTTP/HTTPS from anywhere
        tcp dport @allowed_ports accept

        # Allow from admin subnet
        ip saddr @admin_ips accept
    }
}
```

### Dynamic Sets (Runtime Updates)

```bash
# Add IP to set
sudo nft add element inet filter allowed_ips { 192.168.1.200 }

# Remove IP from set
sudo nft delete element inet filter allowed_ips { 192.168.1.200 }

# List set contents
sudo nft list set inet filter allowed_ips
```

## Maps (Key-Value Rules)

Maps allow different actions based on criteria:

```nftables
table inet filter {
    # Map source IPs to verdicts
    map ip_verdict {
        type ipv4_addr : verdict
        elements = {
            192.168.1.100 : accept,
            198.51.100.50 : drop
        }
    }

    chain input {
        type filter hook input priority 0; policy drop;

        # Apply verdict based on source IP
        ip saddr vmap @ip_verdict
    }
}
```

## Logging

```nftables
# Log before dropping
log prefix "dropped: " level info drop

# Log with more detail
log prefix "ssh-attempt: " level warn flags all

# Log and continue processing
log prefix "new-conn: "
tcp dport 22 accept
```

View logs:

```bash
sudo journalctl -k | grep "dropped:"
# OR
sudo dmesg | grep "dropped:"
```

## NAT (Network Address Translation)

### Source NAT (SNAT) - Masquerading

```nftables
table inet nat {
    chain postrouting {
        type nat hook postrouting priority 100; policy accept;

        # Masquerade outbound traffic on eth0
        oifname "eth0" masquerade
    }
}
```

### Destination NAT (DNAT) - Port Forwarding

```nftables
table inet nat {
    chain prerouting {
        type nat hook prerouting priority -100; policy accept;

        # Forward external port 80 to internal 192.168.1.10:8080
        iifname "eth0" tcp dport 80 dnat to 192.168.1.10:8080
    }
}
```

## Rate Limiting

```nftables
# Limit SSH connections (10 per minute)
tcp dport 22 limit rate 10/minute accept

# Burst limit
tcp dport 22 limit rate over 10/minute burst 5 packets drop

# Per-source IP rate limiting
tcp dport 22 ct state new limit rate over 3/minute burst 5 packets drop
```

## Verdicts

- `accept` - Allow packet
- `drop` - Silently discard packet
- `reject` - Discard and send rejection message
- `queue` - Pass to userspace
- `continue` - Continue processing rules
- `return` - Return to calling chain
- `jump <chain>` - Jump to another chain
- `goto <chain>` - Goto chain (no return)

## Complete Examples

### Web Server

```nftables
#!/usr/sbin/nft -f

flush ruleset

table inet filter {
    # Allowed SSH IPs
    set ssh_allowed {
        type ipv4_addr
        elements = { 203.0.113.0/24 }  # Office IP range
    }

    chain input {
        type filter hook input priority 0; policy drop;

        # Accept loopback
        iif "lo" accept

        # Accept established connections
        ct state established,related accept
        ct state invalid drop

        # Allow ICMP
        meta l4proto icmp accept
        meta l4proto ipv6-icmp accept

        # Allow SSH from allowed IPs only
        tcp dport 22 ip saddr @ssh_allowed ct state new limit rate 5/minute accept

        # Allow HTTP/HTTPS from anywhere
        tcp dport { 80, 443 } accept

        # Log dropped packets
        log prefix "dropped-input: " limit rate 5/minute
        drop
    }

    chain forward {
        type filter hook forward priority 0; policy drop;
    }

    chain output {
        type filter hook output priority 0; policy accept;
    }
}
```

### Database Server (Restricted)

```nftables
#!/usr/sbin/nft -f

flush ruleset

table inet filter {
    # App tier IPs
    set app_servers {
        type ipv4_addr
        elements = { 10.0.2.10, 10.0.2.11, 10.0.2.12 }
    }

    # Bastion host
    set bastion {
        type ipv4_addr
        elements = { 10.0.1.5 }
    }

    chain input {
        type filter hook input priority 0; policy drop;

        iif "lo" accept
        ct state established,related accept
        ct state invalid drop

        # SSH from bastion only
        tcp dport 22 ip saddr @bastion accept

        # PostgreSQL from app servers only
        tcp dport 5432 ip saddr @app_servers accept

        log prefix "db-dropped: " limit rate 1/minute
        drop
    }

    chain forward {
        type filter hook forward priority 0; policy drop;
    }

    chain output {
        type filter hook output priority 0; policy drop;

        oif "lo" accept
        ct state established,related accept

        # Allow DNS
        udp dport 53 accept
        tcp dport 53 accept

        # Allow internal network only
        ip daddr 10.0.0.0/8 accept

        log prefix "db-egress-dropped: " limit rate 1/minute
        drop
    }
}
```

### Egress Filtering

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
            140.82.112.0/20    # GitHub
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

        # Allow DNS
        udp dport 53 accept
        tcp dport 53 accept

        # Allow to approved external destinations
        ip daddr @allowed_external accept

        # Allow internal network
        ip daddr 10.0.0.0/8 accept

        log prefix "egress-blocked: " limit rate 2/minute
        drop
    }
}
```

## Debugging and Tracing

Enable tracing for specific traffic:

```nftables
# Add trace to rule
tcp dport 22 meta nftrace set 1

# Monitor trace events
sudo nft monitor trace
```

Check rule counters:

```bash
# Add counter to rule
tcp dport 80 counter accept

# View counters
sudo nft list ruleset
```

## Migration from iptables

```bash
# Export iptables rules
sudo iptables-save > /tmp/iptables-rules.txt

# Convert to nftables
sudo iptables-restore-translate -f /tmp/iptables-rules.txt > /tmp/nftables-rules.nft

# Review converted rules
cat /tmp/nftables-rules.nft

# Load and test
sudo nft -f /tmp/nftables-rules.nft
sudo nft list ruleset

# If satisfied, disable iptables
sudo systemctl stop iptables
sudo systemctl disable iptables
sudo systemctl enable nftables
```

## Best Practices

1. **Use `inet` family** - Handles IPv4 and IPv6 with single ruleset
2. **Use `meta l4proto`** - More robust than deprecated `nexthdr`
3. **Leverage sets** - Better performance for IP/port lists
4. **Transaction-based updates** - Load entire ruleset at once
5. **Enable logging** - Use `limit` to avoid log flooding
6. **Test before saving** - Load rules, test, then persist
7. **Document rules** - Use comments: `# Description`
8. **Version control** - Store `/etc/nftables.conf` in Git
9. **Don't mix with iptables** - Choose one (nftables recommended)
10. **Use rate limiting** - Prevent brute force and DoS

## Performance Tips

- Place frequently matched rules first
- Use sets instead of multiple rules for IP/port lists
- Avoid excessive logging (use `limit`)
- Use `ct state` for stateful filtering (more efficient)
- Consider using `maps` for complex conditional logic

## Configuration Files

- `/etc/nftables.conf` - Main configuration file
- `/etc/nftables/ directory` - Additional rulesets (can be included)

Example with includes:

```nftables
#!/usr/sbin/nft -f

flush ruleset

include "/etc/nftables.d/sets.nft"
include "/etc/nftables.d/filter.nft"
include "/etc/nftables.d/nat.nft"
```

## Common Errors

**"Error: Could not process rule: No such file or directory"**
- nftables kernel module not loaded: `sudo modprobe nf_tables`

**"Error: syntax error, unexpected..."**
- Check nftables version: `sudo nft --version`
- Ensure correct syntax for version

**Rules not persisting after reboot**
- Enable service: `sudo systemctl enable nftables`
- Ensure `/etc/nftables.conf` exists and is valid

**Conflicts with iptables**
- Disable iptables: `sudo systemctl stop iptables && sudo systemctl disable iptables`
- Or use iptables-nft compatibility: `update-alternatives --set iptables /usr/sbin/iptables-nft`
