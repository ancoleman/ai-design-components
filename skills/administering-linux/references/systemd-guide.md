# Systemd Comprehensive Guide

Complete reference for systemd service management, unit files, dependencies, targets, and advanced configurations.

## Table of Contents

1. [Unit File Structure](#unit-file-structure)
2. [Service Unit Directives](#service-unit-directives)
3. [Timer Units](#timer-units)
4. [Dependencies and Ordering](#dependencies-and-ordering)
5. [Systemd Targets](#systemd-targets)
6. [Advanced Configurations](#advanced-configurations)
7. [Security Hardening](#security-hardening)
8. [Troubleshooting](#troubleshooting)

## Unit File Structure

### File Locations and Priority

Systemd searches for unit files in this order (highest to lowest priority):

1. **`/etc/systemd/system/`** - System administrator units (highest priority)
   - Place custom units and override files here
   - Takes precedence over all other locations

2. **`/run/systemd/system/`** - Runtime units (volatile)
   - Transient units created at runtime
   - Cleared on reboot

3. **`/lib/systemd/system/`** - Distribution-provided units (lowest priority)
   - Installed by package manager
   - Never modify directly - use overrides instead

### Basic Unit File Format

```ini
[Unit]
# Description and dependencies

[Service]
# Service-specific configuration

[Install]
# Installation information (for enable/disable)
```

### Creating Override Files

Override without modifying original:

```bash
# Create override directory and file
sudo systemctl edit nginx.service

# This creates: /etc/systemd/system/nginx.service.d/override.conf
# Add your overrides:
[Service]
MemoryLimit=1G
CPUQuota=50%

# Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart nginx
```

View merged configuration:
```bash
systemctl cat nginx.service
```

## Service Unit Directives

### [Unit] Section

Metadata and dependencies for the unit.

**Description and Documentation:**
```ini
[Unit]
Description=My Web Application
Documentation=https://docs.example.com
Documentation=man:myapp(8)
```

**Dependencies:**
```ini
# Hard dependency (fails if dependency fails)
Requires=postgresql.service

# Soft dependency (continues if dependency fails)
Wants=redis.service

# Conflicts (stop if other unit starts)
Conflicts=apache2.service
```

**Ordering:**
```ini
# Start after these units
After=network.target postgresql.service

# Start before these units
Before=nginx.service

# Conditions (skip if condition fails)
ConditionPathExists=/etc/myapp/config.yml
ConditionFileNotEmpty=/etc/myapp/secret.key
```

### [Service] Section

Service-specific configuration.

**Service Type:**
```ini
[Service]
# Type determines how systemd tracks the service

# simple (default) - Main process doesn't fork
Type=simple

# forking - Main process forks, systemd tracks parent
Type=forking
PIDFile=/var/run/myapp.pid

# oneshot - Process completes and exits (for scripts)
Type=oneshot
RemainAfterExit=yes

# notify - Process signals systemd when ready (sd_notify)
Type=notify

# dbus - Service acquires DBus name
Type=dbus
BusName=com.example.myapp

# idle - Wait until other services start
Type=idle
```

**Execution Commands:**
```ini
[Service]
# Main command to start service
ExecStart=/usr/bin/myapp --config /etc/myapp/config.yml

# Pre-start commands (preparation)
ExecStartPre=/usr/bin/myapp-check-config
ExecStartPre=/bin/mkdir -p /var/run/myapp

# Post-start commands (verification)
ExecStartPost=/usr/bin/myapp-notify-monitoring

# Reload command (SIGHUP alternative)
ExecReload=/bin/kill -HUP $MAINPID

# Stop command (default: SIGTERM)
ExecStop=/usr/bin/myapp-shutdown

# Post-stop cleanup
ExecStopPost=/bin/rm -rf /var/run/myapp
```

**Restart Policies:**
```ini
[Service]
# When to restart
Restart=on-failure    # Restart only on failures
# Restart=always      # Always restart (even on clean exit)
# Restart=on-success  # Restart only on successful exits
# Restart=on-abnormal # Restart on watchdog, signal, or timeout
# Restart=no          # Never restart (default)

# Delay before restart
RestartSec=5s         # Wait 5 seconds before restart

# Maximum restart attempts
StartLimitBurst=5     # Max 5 restarts
StartLimitIntervalSec=10m  # Within 10 minutes

# Action when start limit hit
StartLimitAction=reboot    # Reboot system
# StartLimitAction=none    # Do nothing (default)
```

**User and Group:**
```ini
[Service]
# Run as specific user/group (security best practice)
User=myapp
Group=myapp

# Supplementary groups
SupplementaryGroups=docker ssl-cert

# Working directory
WorkingDirectory=/opt/myapp

# Root directory (chroot)
RootDirectory=/srv/myapp-root
```

**Environment Variables:**
```ini
[Service]
# Set environment variables
Environment="PORT=8080"
Environment="LOG_LEVEL=info"
Environment="DATABASE_URL=postgresql://localhost/myapp"

# Load from file
EnvironmentFile=/etc/myapp/environment
EnvironmentFile=-/etc/myapp/optional.env  # - prefix = optional

# Unset variables
UnsetEnvironment=DEBUG
```

**Logging:**
```ini
[Service]
# Output to journald (default)
StandardOutput=journal
StandardError=journal

# Syslog identifier (for filtering)
SyslogIdentifier=myapp

# Log level
SyslogLevel=info

# Output to file
StandardOutput=append:/var/log/myapp/output.log
StandardError=append:/var/log/myapp/error.log

# Null (discard)
StandardOutput=null
```

### [Install] Section

Installation information for `systemctl enable`.

```ini
[Install]
# Target to enable service with
WantedBy=multi-user.target
# WantedBy=graphical.target  # For desktop services

# Alternative names
Alias=myapp-server.service
Alias=web-app.service

# Required by other units
RequiredBy=nginx.service
```

## Timer Units

Systemd timers replace cron for scheduled tasks.

### Basic Timer Structure

**Timer Unit (myapp.timer):**
```ini
[Unit]
Description=Run My Application Daily
Requires=myapp.service

[Timer]
# Calendar-based scheduling
OnCalendar=daily
OnCalendar=*-*-* 02:00:00

# Run missed timers after boot
Persistent=true

# Accuracy (allow slack for batch scheduling)
AccuracySec=5min

# Random delay (distribute load)
RandomizedDelaySec=30min

[Install]
WantedBy=timers.target
```

**Service Unit (myapp.service):**
```ini
[Unit]
Description=My Application Task

[Service]
Type=oneshot
User=myapp
ExecStart=/usr/local/bin/myapp-task
StandardOutput=journal
StandardError=journal
```

### Timer Scheduling

**Calendar Specifications:**
```ini
# Predefined schedules
OnCalendar=minutely         # Every minute
OnCalendar=hourly           # Every hour
OnCalendar=daily            # Every day at 00:00
OnCalendar=weekly           # Every Monday at 00:00
OnCalendar=monthly          # 1st of month at 00:00
OnCalendar=yearly           # January 1st at 00:00

# Custom schedules
OnCalendar=*-*-* 02:00:00              # Daily at 2:00 AM
OnCalendar=Mon *-*-* 09:00:00          # Monday at 9:00 AM
OnCalendar=*-*-01 00:00:00             # 1st of month
OnCalendar=Mon,Fri *-*-* 08:00:00      # Monday and Friday 8:00 AM
OnCalendar=*-01,06,12-01 00:00:00      # Jan, Jun, Dec 1st
OnCalendar=*-*-* 00/2:00:00            # Every 2 hours

# Multiple schedules (runs on any match)
OnCalendar=Mon *-*-* 09:00:00
OnCalendar=Fri *-*-* 17:00:00
```

**Relative Timers:**
```ini
# Time after boot
OnBootSec=5min              # 5 minutes after boot

# Time after systemd starts
OnStartupSec=10min          # 10 minutes after systemd

# Time after unit activation
OnActiveSec=1h              # 1 hour after timer activated

# Time after unit last ran
OnUnitActiveSec=30min       # 30 minutes after last run
OnUnitInactiveSec=1h        # 1 hour after last finished
```

**Time Units:**
- `s`, `sec`, `seconds`
- `m`, `min`, `minutes`
- `h`, `hr`, `hours`
- `d`, `days`
- `w`, `weeks`
- `M`, `months`
- `y`, `years`

### Timer Management

```bash
# List all timers
systemctl list-timers

# Show timer details
systemctl status backup.timer

# Show next activation
systemctl list-timers backup.timer

# Enable timer (not service!)
systemctl enable backup.timer
systemctl start backup.timer

# Manually trigger timer
systemctl start backup.service

# View logs
journalctl -u backup.service
journalctl -u backup.timer
```

## Dependencies and Ordering

### Dependency Types

**Requires (Hard Dependency):**
```ini
[Unit]
Requires=postgresql.service
After=postgresql.service

# If postgresql fails, this unit fails
# After= ensures ordering
```

**Wants (Soft Dependency):**
```ini
[Unit]
Wants=redis.service
After=redis.service

# If redis fails, this unit continues
# Recommended for optional dependencies
```

**Requisite (Must Already Be Active):**
```ini
[Unit]
Requisite=network.target
After=network.target

# Fails if network.target not already active
```

**BindsTo (Stronger Than Requires):**
```ini
[Unit]
BindsTo=special-device.mount
After=special-device.mount

# Stopped when dependency stops
# Used for device/mount dependencies
```

**PartOf (Propagates Stop/Restart):**
```ini
[Unit]
PartOf=nginx.service

# When nginx stops/restarts, this unit does too
# Useful for helper services
```

**Conflicts:**
```ini
[Unit]
Conflicts=apache2.service

# Cannot run simultaneously with apache2
```

### Ordering Directives

**After:**
```ini
[Unit]
After=network.target postgresql.service

# Start after these units
# Does NOT imply dependency (combine with Requires/Wants)
```

**Before:**
```ini
[Unit]
Before=nginx.service

# Start before nginx
```

**Ordering Without Dependencies:**
```ini
# BAD: Requires without After (race condition)
[Unit]
Requires=postgresql.service

# GOOD: Explicit ordering
[Unit]
Requires=postgresql.service
After=postgresql.service
```

### Condition Directives

Skip service if condition not met:

```ini
[Unit]
# Path checks
ConditionPathExists=/etc/myapp/config.yml
ConditionPathIsDirectory=/var/lib/myapp
ConditionFileNotEmpty=/etc/myapp/secret.key

# Filesystem checks
ConditionFileSystem=/mnt/data=ext4

# Host checks
ConditionHost=webserver01
ConditionHost=!database-server

# Virtualization checks
ConditionVirtualization=yes    # Running in VM
ConditionVirtualization=kvm
ConditionVirtualization=docker

# Architecture checks
ConditionArchitecture=x86-64

# Kernel checks
ConditionKernelVersion=>=5.10

# User checks
ConditionUser=root
ConditionGroup=admin
```

**Assert vs. Condition:**
- **Condition** - Skip unit if false (no error)
- **Assert** - Fail unit if false (error logged)

```ini
# Use Assert for required conditions
AssertPathExists=/etc/critical-config.yml
```

## Systemd Targets

Targets group units and define system states (like runlevels).

### Common Targets

| Target | Description | Equivalent Runlevel |
|--------|-------------|---------------------|
| `poweroff.target` | System shutdown | 0 |
| `rescue.target` | Single-user mode | 1 |
| `multi-user.target` | Multi-user, no GUI | 3 |
| `graphical.target` | Multi-user with GUI | 5 |
| `reboot.target` | System reboot | 6 |

### Target Management

```bash
# Show current target
systemctl get-default

# Set default target
sudo systemctl set-default multi-user.target

# Switch to target
sudo systemctl isolate rescue.target

# Show units in target
systemctl list-dependencies multi-user.target

# Show active targets
systemctl list-units --type=target
```

### Creating Custom Targets

```ini
# /etc/systemd/system/myapp-stack.target
[Unit]
Description=My Application Stack
Requires=postgresql.service redis.service myapp.service
After=postgresql.service redis.service

[Install]
WantedBy=multi-user.target
```

Usage:
```bash
sudo systemctl start myapp-stack.target
sudo systemctl enable myapp-stack.target
```

## Advanced Configurations

### Resource Limits (Control Groups)

```ini
[Service]
# CPU limits
CPUQuota=50%                    # Limit to 50% of one CPU
CPUWeight=500                   # Relative weight (1-10000, default 100)
CPUAccounting=yes               # Enable CPU accounting

# Memory limits
MemoryLimit=1G                  # Hard limit
MemoryHigh=800M                 # Soft limit (throttle before hard limit)
MemoryMax=1G                    # Maximum (same as MemoryLimit)
MemoryAccounting=yes            # Enable memory accounting

# Task limits
TasksMax=100                    # Max number of processes/threads

# I/O limits
IOWeight=500                    # I/O weight (1-10000)
IOReadBandwidthMax=/dev/sda 10M # Read bandwidth limit
IOWriteBandwidthMax=/dev/sda 5M # Write bandwidth limit

# Device access
DeviceAllow=/dev/null rw
DeviceAllow=/dev/zero rw
DevicePolicy=strict             # Only allow explicitly listed devices

# Slice assignment
Slice=myapp.slice               # Custom cgroup slice
```

### Watchdog

Monitor service health and restart on failure:

```ini
[Service]
Type=notify
WatchdogSec=30s                 # Expect notification every 30s
Restart=on-watchdog             # Restart if watchdog timeout

# Application must call sd_notify periodically:
# sd_notify(0, "WATCHDOG=1");
```

### Socket Activation

Start service on-demand when socket accessed:

**Socket Unit (myapp.socket):**
```ini
[Unit]
Description=My Application Socket

[Socket]
ListenStream=8080
Accept=no

[Install]
WantedBy=sockets.target
```

**Service Unit (myapp.service):**
```ini
[Unit]
Description=My Application

[Service]
ExecStart=/usr/bin/myapp
StandardInput=socket
```

Benefits:
- Delayed service start (faster boot)
- Automatic service activation
- Zero-downtime restarts

### Path Units

Trigger service on filesystem changes:

```ini
# /etc/systemd/system/myapp-watch.path
[Unit]
Description=Watch Config Changes

[Path]
PathChanged=/etc/myapp/config.yml
Unit=myapp-reload.service

[Install]
WantedBy=multi-user.target
```

## Security Hardening

### Sandboxing Directives

```ini
[Service]
# Filesystem protection
PrivateTmp=true                 # Private /tmp and /var/tmp
ProtectSystem=strict            # Read-only /usr, /boot, /etc
ProtectHome=true                # Inaccessible /home
ReadWritePaths=/var/lib/myapp   # Exception for write access
ReadOnlyPaths=/etc/myapp
InaccessiblePaths=/proc/sys

# Privilege restrictions
NoNewPrivileges=true            # Prevent privilege escalation
PrivateDevices=true             # Private /dev (only pseudo devices)
ProtectKernelTunables=true      # Read-only /proc/sys, /sys
ProtectKernelModules=true       # Deny module loading
ProtectControlGroups=true       # Read-only cgroups

# Network restrictions
PrivateNetwork=true             # Private network namespace (no network)
RestrictAddressFamilies=AF_INET AF_INET6  # Only IPv4/IPv6

# Capability restrictions
CapabilityBoundingSet=CAP_NET_BIND_SERVICE  # Specific capabilities
AmbientCapabilities=CAP_NET_BIND_SERVICE

# System call filtering
SystemCallFilter=@system-service  # Whitelist common syscalls
SystemCallFilter=~@privileged     # Blacklist privileged syscalls
SystemCallErrorNumber=EPERM       # Return EPERM on denied syscall

# Execution restrictions
LockPersonality=true            # Prevent personality changes
RestrictRealtime=true           # Deny realtime scheduling
RestrictSUIDSGID=true           # Deny SUID/SGID execution
RemoveIPC=true                  # Remove IPC objects on exit
```

### Security Analysis

Check security restrictions:
```bash
systemd-analyze security myapp.service
```

This shows:
- Current security settings
- Recommendations for hardening
- Security score (lower is better)

## Troubleshooting

### Debugging Service Failures

**Check service status:**
```bash
systemctl status myapp.service
```

**View logs:**
```bash
journalctl -u myapp.service
journalctl -u myapp.service --since today
journalctl -u myapp.service -n 100        # Last 100 lines
journalctl -u myapp.service -f            # Follow
journalctl -u myapp.service -p err        # Errors only
```

**Check dependencies:**
```bash
systemctl list-dependencies myapp.service
systemctl list-dependencies --reverse myapp.service
```

**Test unit file:**
```bash
systemd-analyze verify myapp.service
```

**Show loaded unit:**
```bash
systemctl cat myapp.service              # Show file
systemctl show myapp.service             # Show all properties
systemctl show myapp.service -p ExecStart -p Restart
```

### Common Issues

**Service fails to start:**
```bash
# Check syntax
systemd-analyze verify myapp.service

# Check file permissions
ls -la /etc/systemd/system/myapp.service
# Should be: -rw-r--r-- root root

# Check executable exists
which myapp
ls -la /usr/bin/myapp

# Check user/group exists
id myapp
```

**Service starts but stops immediately:**
```bash
# Type=forking but no PIDFile
[Service]
Type=forking
PIDFile=/var/run/myapp.pid  # Must specify PID file

# Type=oneshot but should be simple
[Service]
Type=simple                  # For long-running processes

# Missing RemainAfterExit for oneshot
[Service]
Type=oneshot
RemainAfterExit=yes         # Keep active after exit
```

**Dependency timeout:**
```bash
# Increase timeout
[Service]
TimeoutStartSec=300         # 5 minutes (default 90s)

# Or make dependency optional
[Unit]
Wants=slow-service.service  # Instead of Requires
```

**Service killed by OOM:**
```bash
# Check for OOM kills
journalctl -k | grep -i "out of memory"
dmesg | grep -i oom

# Increase memory limit
[Service]
MemoryMax=2G                # Increase limit

# Or disable limit
MemoryMax=infinity
```

### Systemd Boot Analysis

**Analyze boot time:**
```bash
systemd-analyze                          # Total boot time
systemd-analyze blame                    # Time per unit
systemd-analyze critical-chain           # Critical path
systemd-analyze plot > boot.svg          # Visual timeline
```

**Find slow services:**
```bash
systemd-analyze blame | head -20
```

### Emergency Mode Recovery

**Booting into rescue mode:**
1. At GRUB, edit boot entry (press 'e')
2. Add `systemd.unit=rescue.target` to kernel line
3. Boot with Ctrl+X

**Reset failed units:**
```bash
systemctl reset-failed
```

**Mask service (prevent start):**
```bash
systemctl mask myapp.service     # Symlink to /dev/null
systemctl unmask myapp.service
```

## Best Practices

### Unit File Organization

1. **Use override files for customization**
   ```bash
   systemctl edit myapp.service  # Don't modify original
   ```

2. **Drop-in directories for modular config**
   ```bash
   /etc/systemd/system/myapp.service.d/
   ├── 10-resources.conf    # Resource limits
   ├── 20-security.conf     # Security hardening
   └── 30-monitoring.conf   # Monitoring hooks
   ```

3. **Document with Description and Documentation**
   ```ini
   [Unit]
   Description=My Web Application Server
   Documentation=https://docs.example.com
   Documentation=man:myapp(8)
   ```

### Dependency Management

1. **Always combine Requires/Wants with After**
   ```ini
   [Unit]
   Requires=postgresql.service
   After=postgresql.service      # Explicit ordering
   ```

2. **Use Wants for optional dependencies**
   ```ini
   Wants=redis.service           # Continues if redis fails
   ```

3. **Check dependency loops**
   ```bash
   systemctl list-dependencies myapp.service --all
   ```

### Security Hardening

1. **Run as non-root**
   ```ini
   [Service]
   User=myapp
   Group=myapp
   ```

2. **Apply sandboxing**
   ```ini
   PrivateTmp=true
   ProtectSystem=strict
   NoNewPrivileges=true
   ```

3. **Analyze security**
   ```bash
   systemd-analyze security myapp.service
   ```

### Logging

1. **Use journal for centralized logs**
   ```ini
   [Service]
   StandardOutput=journal
   StandardError=journal
   SyslogIdentifier=myapp
   ```

2. **Set appropriate log levels**
   ```ini
   SyslogLevel=info
   ```

3. **Query logs efficiently**
   ```bash
   journalctl -u myapp -f -n 100 -p warning
   ```

## References

- Official systemd documentation: https://systemd.io/
- systemd.service(5) man page: `man systemd.service`
- systemd.timer(5) man page: `man systemd.timer`
- systemd.unit(5) man page: `man systemd.unit`
- systemd.exec(5) man page: `man systemd.exec`
