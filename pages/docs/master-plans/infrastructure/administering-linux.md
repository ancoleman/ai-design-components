---
sidebar_position: 10
title: Linux Administration
description: Master plan for Linux system administration covering systemd, process management, filesystem operations, networking, and troubleshooting
tags: [master-plan, infrastructure, linux, systemd, administration]
---

# Linux Administration

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Linux administration remains critical in the cloud-native era. This skill covers systemd service management, process monitoring, filesystem operations, networking fundamentals, and production troubleshooting patterns.

## Scope

This skill teaches:

- **Systemd Service Management** - Creating units, service lifecycle, timers (modern cron)
- **Process Management** - Monitoring (ps, top, htop), control (kill, nice), resource limits
- **Filesystem Operations** - Mount management, disk usage, permissions, quotas
- **Networking Fundamentals** - Interface config, routing, firewall basics, DNS resolution
- **Log Management** - journalctl, log rotation, log aggregation
- **Performance Tuning** - CPU, memory, disk I/O optimization
- **Troubleshooting** - Systematic debugging for production issues

## Key Components

### Systemd Service Management

**Core Concepts:**
- **Units**: Services, timers, targets, sockets, mounts
- **Unit Files**: `/etc/systemd/system/` (custom), `/lib/systemd/system/` (package)
- **Service Lifecycle**: start, stop, restart, reload, enable, disable
- **Timers**: Modern replacement for cron with better logging

**Common Commands:**
```bash
systemctl start service
systemctl status service
systemctl enable service  # Start on boot
journalctl -u service -f  # Follow service logs
systemctl list-timers     # List scheduled tasks
```

### Process Management

**Monitoring:**
- `ps aux` - List all processes
- `top`/`htop` - Interactive process viewer
- `pgrep`/`pidof` - Find process IDs
- `/proc/[pid]/` - Process information filesystem

**Control:**
- `kill` - Send signals (SIGTERM, SIGKILL)
- `nice`/`renice` - Process priority
- `nohup` - Run process immune to hangups
- `systemd-run` - Run transient services

### Filesystem Operations

**Disk Management:**
- `df -h` - Disk free space
- `du -sh *` - Directory sizes
- `lsblk` - List block devices
- `mount`/`umount` - Mount filesystems

**Permissions:**
- `chmod` - Change file permissions (755, 644)
- `chown` - Change file ownership
- `setfacl`/`getfacl` - Access control lists

**Quotas:**
- User/group disk quotas
- Soft/hard limits
- Grace periods

### Networking Fundamentals

**Configuration:**
- `ip addr` - Show/configure IP addresses
- `ip route` - Show/configure routing table
- `ss` - Socket statistics (modern `netstat`)
- `nmcli` - NetworkManager CLI

**Diagnostics:**
- `ping` - Test connectivity
- `traceroute` - Trace network path
- `dig`/`nslookup` - DNS queries
- `tcpdump` - Packet capture

**Firewall:**
- `firewalld` (RHEL/CentOS/Fedora)
- `ufw` (Ubuntu/Debian)
- `iptables` (legacy, still used)

## Decision Framework

**Which Init System?**

```
2025 Reality:
  Almost all distributions use systemd
  Exceptions: Alpine (OpenRC), some containers

Use systemd unless:
  - Alpine Linux (lightweight containers)
  - Legacy system (pre-2015)
  - Embedded systems (custom init)
```

**Performance Tuning Priority:**

```
Where's the bottleneck?
  CPU bound? → nice/renice, CPU affinity
  Memory bound? → Swap tuning, memory limits
  Disk I/O? → I/O scheduler, filesystem tuning
  Network? → TCP tuning, NIC ring buffers

Monitor first:
  top/htop → CPU/memory
  iostat → Disk I/O
  sar → Historical trends
  netstat/ss → Network connections
```

## Tool Recommendations

### System Monitoring

**Process Monitoring:**
- `top` - Classic process viewer
- `htop` - Interactive, color-coded
- `atop` - Advanced with history

**Performance Analysis:**
- `vmstat` - Virtual memory stats
- `iostat` - I/O statistics
- `sar` - System activity reporter
- `perf` - Performance profiling

### Log Management

**journalctl** - Systemd journal
```bash
journalctl -u service    # Service logs
journalctl -f            # Follow all logs
journalctl --since today # Filter by time
journalctl -p err        # Error priority and above
```

**Traditional Logs:**
- `/var/log/syslog` or `/var/log/messages`
- `/var/log/auth.log` - Authentication
- `logrotate` - Log rotation automation

### Package Management

**RHEL/CentOS/Fedora:** `dnf`/`yum`, `rpm`
**Debian/Ubuntu:** `apt`, `dpkg`
**Arch:** `pacman`
**Universal:** `snap`, `flatpak` (sandboxed)

## Integration Points

**With Other Skills:**
- `managing-configuration` - Automate Linux configuration at scale (Ansible)
- `security-hardening` - Apply CIS benchmarks, SELinux, AppArmor
- `operating-kubernetes` - Understand K8s node OS layer
- `shell-scripting` - Automate administrative tasks
- `implementing-observability` - Integrate with monitoring (Prometheus, Grafana)

**Workflow Example:**
```
Manual Admin → Script → Ansible → IaC
     │            │        │        │
     ▼            ▼        ▼        ▼
Learn system  Automate  Scale to  Provision
commands      tasks     100s      infrastructure
```

## Learn More

- [Full Master Plan (init.md)](https://github.com/ancoleman/ai-design-components/blob/main/skills/administering-linux/init.md)
- Related: `managing-configuration`, `security-hardening`, `shell-scripting`
