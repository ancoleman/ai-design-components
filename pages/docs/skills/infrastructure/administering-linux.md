---
sidebar_position: 3
title: Administering Linux
description: Linux system administration with systemd, networking, and performance tuning
tags: [infrastructure, linux, systemd, sysadmin]
---

# Administering Linux

Comprehensive Linux system administration for managing servers, deploying applications, and troubleshooting production issues in modern cloud-native environments.

## When to Use

Use when:
- Deploying custom applications to Linux servers
- Troubleshooting slow systems or service failures
- Optimizing server performance and resource usage
- Managing users, SSH access, and security
- Configuring systemd services and timers
- Monitoring disk space and system resources
- Scheduling tasks with cron or systemd timers
- Diagnosing network connectivity issues

## Key Features

### Systemd Service Management
- Create and manage systemd unit files
- Configure automatic restarts and dependencies
- Security hardening with PrivateTmp, ProtectSystem
- Journal logs with journalctl filtering

### Process Management
- Monitor processes with top/htop
- Process states and signal handling (SIGTERM, SIGKILL)
- Process priority with nice/renice
- Resource limits with ulimit

### Filesystem Operations
- ext4, XFS, Btrfs, ZFS filesystem selection
- LVM for flexible volume management
- Disk usage monitoring with df, du, ncdu
- File permissions and ACLs

### Package Management
- apt (Ubuntu/Debian) and dnf (RHEL/Fedora)
- System updates and security patches
- snap/flatpak for cross-distribution packages

### Network Configuration
- Interface management with ip command
- Firewall setup (ufw, firewalld)
- Socket statistics with ss
- DNS configuration and troubleshooting

### Performance Tuning
- sysctl for kernel parameter tuning
- I/O scheduler configuration
- TCP/BBR congestion control
- Memory swappiness and cache pressure

## Quick Start

### Creating a Systemd Service

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Web Application
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=simple
User=myapp
Group=myapp
WorkingDirectory=/opt/myapp
Environment="PORT=8080"
ExecStart=/opt/myapp/bin/server
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5s
StandardOutput=journal

# Security hardening
PrivateTmp=true
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/var/lib/myapp

[Install]
WantedBy=multi-user.target
```

**Deploy service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable myapp.service
sudo systemctl start myapp.service
sudo systemctl status myapp.service
```

### SSH Hardening

```bash
# /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
AllowUsers admin deploy
X11Forwarding no

# Apply changes
sudo sshd -t
sudo systemctl restart sshd
```

### Performance Tuning

```bash
# /etc/sysctl.d/99-custom.conf
# Network tuning
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_congestion_control = bbr

# Memory management
vm.swappiness = 10
vm.vfs_cache_pressure = 50

# Apply changes
sudo sysctl -p /etc/sysctl.d/99-custom.conf
```

## Essential Commands

### Service Management
```bash
systemctl start nginx              # Start service
systemctl stop nginx               # Stop service
systemctl restart nginx            # Restart service
systemctl status nginx             # Check status
systemctl enable nginx             # Enable at boot
journalctl -u nginx -f             # Follow service logs
```

### Process Monitoring
```bash
top                                # Interactive process monitor
htop                               # Enhanced process monitor
ps aux | grep process_name         # Find specific process
kill -15 PID                       # Graceful shutdown (SIGTERM)
kill -9 PID                        # Force kill (SIGKILL)
```

### Disk Management
```bash
df -h                              # Filesystem usage
du -sh /path/to/dir                # Directory size
ncdu /path                         # Interactive disk analyzer
lsblk                              # List block devices
```

### Network Tools
```bash
ip addr show                       # Show interfaces
ip route show                      # Show routing table
ss -tunap                          # All TCP/UDP connections
ss -tlnp                           # Listening TCP ports
ping -c 4 8.8.8.8                  # Test connectivity
dig example.com                    # DNS query
```

## Troubleshooting Workflows

### Performance Issues

1. **Identify bottleneck:**
   ```bash
   top                             # Quick overview
   uptime                          # Load averages
   ```

2. **CPU Issues (usage >80%):**
   ```bash
   top                             # Press Shift+P to sort by CPU
   ps aux --sort=-%cpu | head
   ```

3. **Memory Issues (swap used):**
   ```bash
   free -h                         # Memory usage
   top                             # Press Shift+M to sort by memory
   ```

4. **Disk I/O Issues (high wa%):**
   ```bash
   iostat -x 1                     # Disk statistics
   iotop                           # I/O by process
   ```

## Related Skills

- [Operating Kubernetes](./operating-kubernetes) - Container orchestration on Linux
- [Managing Configuration](./managing-configuration) - Automate Linux admin at scale
- [Shell Scripting](./shell-scripting) - Automate system tasks
- [Configuring NGINX](./configuring-nginx) - Web server setup

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/administering-linux)
- Systemd Guide: `references/systemd-guide.md`
- Performance Tuning: `references/performance-tuning.md`
- Filesystem Management: `references/filesystem-management.md`
- Network Configuration: `references/network-configuration.md`
- Security Hardening: `references/security-hardening.md`
- Troubleshooting Guide: `references/troubleshooting-guide.md`
