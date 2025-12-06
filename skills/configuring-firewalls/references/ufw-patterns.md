# UFW Patterns Guide

UFW (Uncomplicated Firewall) is a user-friendly front-end for iptables/nftables, default on Ubuntu and available on Debian-based systems.


## Table of Contents

- [Installation](#installation)
- [Basic Setup](#basic-setup)
- [Common Rule Patterns](#common-rule-patterns)
  - [Allow by Port Number](#allow-by-port-number)
  - [Allow by Service Name](#allow-by-service-name)
  - [Allow from Specific IP](#allow-from-specific-ip)
  - [Rate Limiting (Prevent Brute Force)](#rate-limiting-prevent-brute-force)
  - [Deny Rules](#deny-rules)
  - [Interface-Specific Rules](#interface-specific-rules)
- [Managing Rules](#managing-rules)
  - [View Rules](#view-rules)
  - [Delete Rules](#delete-rules)
  - [Insert Rules at Specific Position](#insert-rules-at-specific-position)
  - [Reset Firewall](#reset-firewall)
- [Logging](#logging)
  - [Enable Logging](#enable-logging)
  - [View Logs](#view-logs)
- [Application Profiles](#application-profiles)
  - [List Profiles](#list-profiles)
  - [View Profile Details](#view-profile-details)
  - [Allow Application](#allow-application)
  - [Custom Application Profiles](#custom-application-profiles)
- [Common Scenarios](#common-scenarios)
  - [Web Server](#web-server)
  - [Database Server (PostgreSQL)](#database-server-postgresql)
  - [Mail Server](#mail-server)
  - [Development Machine](#development-machine)
- [IPv6 Support](#ipv6-support)
- [Troubleshooting](#troubleshooting)
  - [Check if UFW is Active](#check-if-ufw-is-active)
  - [Test Rules Without Enabling](#test-rules-without-enabling)
  - [Verify External Access](#verify-external-access)
  - [UFW Not Blocking Traffic](#ufw-not-blocking-traffic)
  - [Reload Rules](#reload-rules)
- [Best Practices](#best-practices)
- [Performance Considerations](#performance-considerations)
- [Migration to nftables Backend](#migration-to-nftables-backend)
- [Configuration Files](#configuration-files)
- [Advanced: Direct iptables Rules](#advanced-direct-iptables-rules)

## Installation

```bash
# Usually pre-installed on Ubuntu
sudo apt install ufw

# Check status
sudo ufw status
```

## Basic Setup

```bash
# 1. Set default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 2. CRITICAL: Allow SSH before enabling (prevent lockout)
sudo ufw allow ssh
# OR specific port:
sudo ufw allow 22/tcp

# 3. Enable firewall
sudo ufw enable

# 4. Check status
sudo ufw status verbose
```

## Common Rule Patterns

### Allow by Port Number

```bash
# HTTP
sudo ufw allow 80/tcp

# HTTPS
sudo ufw allow 443/tcp

# Custom port
sudo ufw allow 8080/tcp

# Port range
sudo ufw allow 6000:6007/tcp
```

### Allow by Service Name

```bash
# SSH (port 22)
sudo ufw allow ssh

# HTTP (port 80)
sudo ufw allow http

# HTTPS (port 443)
sudo ufw allow https

# DNS (port 53)
sudo ufw allow dns
```

Service names defined in `/etc/services`

### Allow from Specific IP

```bash
# Allow all traffic from IP
sudo ufw allow from 192.168.1.100

# Allow specific port from IP
sudo ufw allow from 192.168.1.100 to any port 22

# Allow from subnet
sudo ufw allow from 192.168.1.0/24

# Allow specific port from subnet
sudo ufw allow from 192.168.1.0/24 to any port 5432
```

### Rate Limiting (Prevent Brute Force)

```bash
# Limit SSH connections (max 6 attempts in 30 seconds)
sudo ufw limit ssh

# Limit specific port
sudo ufw limit 22/tcp
```

UFW will deny connections if an IP attempts 6+ connections in 30 seconds.

### Deny Rules

```bash
# Deny specific port
sudo ufw deny 23/tcp

# Deny from specific IP
sudo ufw deny from 198.51.100.100

# Deny to specific port from IP
sudo ufw deny from 198.51.100.100 to any port 22
```

### Interface-Specific Rules

```bash
# Allow on specific interface
sudo ufw allow in on eth0 to any port 80

# Allow out on specific interface
sudo ufw allow out on eth1
```

## Managing Rules

### View Rules

```bash
# Verbose status
sudo ufw status verbose

# Numbered list (for deletion)
sudo ufw status numbered

# Show added rules (not active rules)
sudo ufw show added
```

### Delete Rules

```bash
# By rule number (recommended)
sudo ufw status numbered
sudo ufw delete 3

# By rule specification
sudo ufw delete allow 80/tcp
sudo ufw delete allow from 192.168.1.100
```

### Insert Rules at Specific Position

```bash
# Insert at position 1 (top priority)
sudo ufw insert 1 allow from 10.0.0.0/8
```

### Reset Firewall

```bash
# Disable and remove all rules
sudo ufw reset

# Disable (keep rules)
sudo ufw disable
```

## Logging

### Enable Logging

```bash
# Enable logging (low level)
sudo ufw logging on

# Set log level
sudo ufw logging low     # Default
sudo ufw logging medium  # More detail
sudo ufw logging high    # Full logging
sudo ufw logging full    # Maximum verbosity
```

### View Logs

```bash
# UFW logs
sudo tail -f /var/log/ufw.log

# Or via syslog
sudo journalctl -u ufw -f
```

## Application Profiles

UFW supports application profiles for common services.

### List Profiles

```bash
sudo ufw app list
```

### View Profile Details

```bash
sudo ufw app info 'Nginx Full'
```

### Allow Application

```bash
# Allow Nginx HTTP and HTTPS
sudo ufw allow 'Nginx Full'

# Allow OpenSSH
sudo ufw allow 'OpenSSH'

# Allow Apache
sudo ufw allow 'Apache Full'
```

### Custom Application Profiles

Create file in `/etc/ufw/applications.d/myapp`:

```ini
[MyApp]
title=My Application
description=My custom application
ports=8080,8443/tcp
```

Then:

```bash
sudo ufw app update MyApp
sudo ufw allow MyApp
```

## Common Scenarios

### Web Server

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw limit ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

### Database Server (PostgreSQL)

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw limit ssh
# Only allow PostgreSQL from app servers
sudo ufw allow from 10.0.2.0/24 to any port 5432
sudo ufw enable
```

### Mail Server

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw limit ssh
sudo ufw allow smtp     # Port 25
sudo ufw allow imaps    # Port 993
sudo ufw allow submission  # Port 587
sudo ufw enable
```

### Development Machine

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
# Allow common development ports from local network only
sudo ufw allow from 192.168.1.0/24 to any port 3000  # React dev server
sudo ufw allow from 192.168.1.0/24 to any port 5000  # Flask dev server
sudo ufw allow from 192.168.1.0/24 to any port 8080  # Common HTTP alternate
sudo ufw enable
```

## IPv6 Support

UFW supports IPv6 by default. Ensure enabled in `/etc/default/ufw`:

```bash
IPV6=yes
```

All rules apply to both IPv4 and IPv6 unless specified:

```bash
# IPv4 only
sudo ufw allow from 192.168.1.0/24

# IPv6 only
sudo ufw allow from 2001:db8::/32
```

## Troubleshooting

### Check if UFW is Active

```bash
sudo ufw status
# Should show: Status: active
```

### Test Rules Without Enabling

```bash
# Add rules, but don't enable
sudo ufw allow ssh
sudo ufw allow http

# Review what would be enabled
sudo ufw show added

# Enable when ready
sudo ufw enable
```

### Verify External Access

```bash
# From another machine
nmap -Pn <server-ip>

# Should only show allowed ports
```

### UFW Not Blocking Traffic

Check kernel modules:

```bash
# Ensure iptables modules loaded
sudo lsmod | grep ip_tables

# Check ufw service
sudo systemctl status ufw
```

### Reload Rules

```bash
# Reload without interrupting connections
sudo ufw reload
```

## Best Practices

1. **Always allow SSH before enabling** - Prevent lockout
2. **Use `limit` for SSH** - Prevents brute force attacks
3. **Default deny incoming** - Whitelist approach
4. **Use service names when possible** - More readable (`http` vs `80/tcp`)
5. **Enable logging** - For debugging and auditing
6. **Document changes** - Use descriptive comments or external documentation
7. **Test before production** - Verify rules on staging first
8. **Regular audits** - Review rules quarterly, remove unused

## Performance Considerations

UFW is optimized for simplicity, not extreme performance:
- For high-performance needs (>100k pps), use nftables directly
- UFW is suitable for most servers (web, database, application)
- Rule order matters: frequently matched rules should be first

## Migration to nftables Backend

Modern UFW versions use nftables backend:

```bash
# Check backend
sudo ufw version
# If using nftables: "ufw 0.36"

# Force iptables backend (if needed)
sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
```

No configuration changes needed; UFW abstracts the backend.

## Configuration Files

- `/etc/ufw/ufw.conf` - UFW daemon configuration
- `/etc/ufw/before.rules` - Rules processed before UFW rules
- `/etc/ufw/after.rules` - Rules processed after UFW rules
- `/etc/ufw/user.rules` - Generated from `ufw` commands (don't edit manually)
- `/etc/default/ufw` - Default policies and IPv6 settings
- `/var/log/ufw.log` - Firewall logs

## Advanced: Direct iptables Rules

For advanced scenarios, edit `/etc/ufw/before.rules`:

```bash
# Example: Allow ICMP (ping)
-A ufw-before-input -p icmp --icmp-type echo-request -j ACCEPT
```

Reload: `sudo ufw reload`

**Warning:** Direct iptables rules bypass UFW simplicity; use sparingly.
