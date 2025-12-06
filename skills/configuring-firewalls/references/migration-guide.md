# Migrating from iptables to nftables

Guide for converting existing iptables rules to nftables.


## Table of Contents

- [Why Migrate?](#why-migrate)
- [Pre-Migration Checklist](#pre-migration-checklist)
- [Migration Steps](#migration-steps)
  - [Step 1: Export iptables Rules](#step-1-export-iptables-rules)
  - [Step 2: Convert to nftables](#step-2-convert-to-nftables)
  - [Step 3: Clean Up Converted Rules](#step-3-clean-up-converted-rules)
  - [Step 4: Test nftables Rules](#step-4-test-nftables-rules)
  - [Step 5: Run Both Simultaneously (Validation)](#step-5-run-both-simultaneously-validation)
  - [Step 6: Switch to nftables](#step-6-switch-to-nftables)
- [Common Conversion Issues](#common-conversion-issues)
  - [Issue 1: Table Family](#issue-1-table-family)
  - [Issue 2: Implicit Chains](#issue-2-implicit-chains)
  - [Issue 3: Match Criteria Syntax](#issue-3-match-criteria-syntax)
  - [Issue 4: Multiple Ports](#issue-4-multiple-ports)
- [Optimization Opportunities](#optimization-opportunities)
  - [Use Sets for IP/Port Lists](#use-sets-for-ipport-lists)
  - [Combine IPv4 and IPv6](#combine-ipv4-and-ipv6)
  - [Use meta l4proto](#use-meta-l4proto)
- [Rollback Plan](#rollback-plan)
- [Testing Checklist](#testing-checklist)
- [Example: Complete Migration](#example-complete-migration)
- [Migration Timeline](#migration-timeline)
- [Resources](#resources)

## Why Migrate?

- **Performance:** O(log n) vs O(n) rule processing
- **Unified Syntax:** IPv4, IPv6, NAT in single ruleset
- **Modern Features:** Sets, maps, transaction-based updates
- **Default on New Distros:** RHEL 8+, Debian 11+, Ubuntu 22.04+

## Pre-Migration Checklist

- [ ] Backup current iptables rules
- [ ] Test migration on non-production system first
- [ ] Plan maintenance window
- [ ] Have rollback plan ready
- [ ] Ensure kernel supports nftables (>= 4.14)

## Migration Steps

### Step 1: Export iptables Rules

```bash
# Export current rules
sudo iptables-save > /tmp/iptables-rules.txt
sudo ip6tables-save > /tmp/ip6tables-rules.txt

# Review exported rules
cat /tmp/iptables-rules.txt
```

### Step 2: Convert to nftables

```bash
# Convert IPv4 rules
sudo iptables-restore-translate -f /tmp/iptables-rules.txt > /tmp/nftables-rules.nft

# Convert IPv6 rules
sudo ip6tables-restore-translate -f /tmp/ip6tables-rules.txt >> /tmp/nftables-rules.nft

# Review converted rules
cat /tmp/nftables-rules.nft
```

### Step 3: Clean Up Converted Rules

Automated conversion may need manual cleanup:

```nftables
# Before (converted):
table ip filter {
    chain INPUT {
        type filter hook input priority 0; policy accept;
        # Many individual rules...
    }
}

# After (optimized with sets):
table inet filter {  # Use inet for IPv4+IPv6
    set ssh_allowed {
        type ipv4_addr
        elements = { 192.168.1.100, 203.0.113.50 }
    }

    chain input {
        type filter hook input priority 0; policy drop;  # Explicit drop
        tcp dport 22 ip saddr @ssh_allowed accept
    }
}
```

### Step 4: Test nftables Rules

```bash
# Load nftables rules (test mode)
sudo nft -f /tmp/nftables-rules.nft

# Verify rules loaded
sudo nft list ruleset

# Test connectivity
# - SSH access
# - HTTP/HTTPS access
# - Application-specific ports

# Check logs
sudo journalctl -k | grep "nft"
```

### Step 5: Run Both Simultaneously (Validation)

```bash
# Keep iptables running while testing nftables
sudo iptables -L -v -n   # Check iptables still active
sudo nft list ruleset     # Check nftables also active

# Monitor for conflicts
# Test all application flows
# Verify no unexpected blocks
```

### Step 6: Switch to nftables

```bash
# Disable iptables
sudo systemctl stop iptables
sudo systemctl disable iptables

# Flush iptables rules
sudo iptables -F
sudo iptables -X

# Enable nftables
sudo cp /tmp/nftables-rules.nft /etc/nftables.conf
sudo systemctl enable nftables
sudo systemctl start nftables

# Verify
sudo systemctl status nftables
sudo nft list ruleset
```

## Common Conversion Issues

### Issue 1: Table Family

**iptables uses separate commands:**
- `iptables` (IPv4)
- `ip6tables` (IPv6)

**nftables uses table families:**
```nftables
# Use inet for both IPv4 and IPv6
table inet filter {
    # Works for both protocols
}
```

### Issue 2: Implicit Chains

**iptables has built-in chains:**
- INPUT, OUTPUT, FORWARD always exist

**nftables requires explicit chain definition:**
```nftables
chain input {
    type filter hook input priority 0; policy drop;
    # Must define type, hook, priority
}
```

### Issue 3: Match Criteria Syntax

**iptables:**
```bash
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
```

**nftables:**
```nftables
tcp dport 80 accept
# More concise, protocol matching integrated
```

### Issue 4: Multiple Ports

**iptables (requires multiple rules or multiport):**
```bash
iptables -A INPUT -p tcp -m multiport --dports 80,443 -j ACCEPT
```

**nftables (native set support):**
```nftables
tcp dport { 80, 443 } accept
```

## Optimization Opportunities

### Use Sets for IP/Port Lists

**Before (iptables):**
```bash
iptables -A INPUT -s 192.168.1.10 -j ACCEPT
iptables -A INPUT -s 192.168.1.11 -j ACCEPT
iptables -A INPUT -s 192.168.1.12 -j ACCEPT
```

**After (nftables):**
```nftables
set allowed_ips {
    type ipv4_addr
    elements = { 192.168.1.10, 192.168.1.11, 192.168.1.12 }
}

ip saddr @allowed_ips accept
```

### Combine IPv4 and IPv6

**Before (separate rulesets):**
- /etc/iptables/rules.v4
- /etc/iptables/rules.v6

**After (unified):**
```nftables
table inet filter {
    # Single ruleset handles both protocols
    chain input {
        tcp dport 22 accept  # Works for IPv4 and IPv6
    }
}
```

### Use meta l4proto

**Old conversion may use:**
```nftables
nexthdr tcp dport 22 accept  # Deprecated
```

**Best practice:**
```nftables
meta l4proto tcp tcp dport 22 accept  # Recommended
# Or simply:
tcp dport 22 accept
```

## Rollback Plan

If migration causes issues:

```bash
# Flush nftables
sudo nft flush ruleset
sudo systemctl stop nftables
sudo systemctl disable nftables

# Restore iptables
sudo iptables-restore < /tmp/iptables-rules.txt
sudo ip6tables-restore < /tmp/ip6tables-rules.txt
sudo systemctl enable iptables
sudo systemctl start iptables

# Verify
sudo iptables -L -v -n
```

## Testing Checklist

After migration:

- [ ] SSH access works
- [ ] Web services accessible (HTTP/HTTPS)
- [ ] Application-specific ports working
- [ ] Logging functioning
- [ ] Rules persist after reboot
- [ ] No unexpected connection failures
- [ ] External port scan shows expected results (`nmap -Pn <ip>`)
- [ ] Internal application flows tested
- [ ] Monitoring tools still receiving data

## Example: Complete Migration

**Original iptables script:**
```bash
iptables -P INPUT DROP
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

**Converted and optimized nftables:**
```nftables
#!/usr/sbin/nft -f

flush ruleset

table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;

        iif "lo" accept
        ct state established,related accept
        tcp dport { 22, 80, 443 } accept
    }

    chain forward {
        type filter hook forward priority 0; policy drop;
    }

    chain output {
        type filter hook output priority 0; policy accept;
    }
}
```

## Migration Timeline

Recommended phased approach:

**Week 1: Planning**
- Audit current rules
- Backup configuration
- Test conversion on staging

**Week 2: Testing**
- Load nftables alongside iptables
- Run both simultaneously
- Validate all traffic flows

**Week 3: Cutover**
- Schedule maintenance window
- Disable iptables, enable nftables
- Monitor for 24-48 hours
- Keep rollback plan ready

**Week 4: Optimization**
- Optimize rules with sets/maps
- Tune logging and monitoring
- Document new configuration

## Resources

- nftables Migration Guide: https://wiki.nftables.org/wiki-nftables/index.php/Moving_from_iptables_to_nftables
- For nftables and iptables patterns, see the main SKILL.md
