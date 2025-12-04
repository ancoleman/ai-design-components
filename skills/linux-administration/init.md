# Linux Administration Skill - Master Plan

**Skill Name:** `linux-administration`
**Skill Level:** Mid Level (5,000-8,000 tokens, 500-800 lines init.md)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Linux Administration Taxonomy](#linux-administration-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Implementation Patterns](#implementation-patterns)
7. [Tool Recommendations](#tool-recommendations)
8. [Skill Structure Design](#skill-structure-design)
9. [Integration Points](#integration-points)
10. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters in 2025

Linux administration remains a critical skill in the cloud-native era, despite (or because of) containerization and orchestration platforms. Modern infrastructure still requires solid Linux fundamentals.

**Market Reality:**
- **Cloud-Native Foundation:** Even Kubernetes nodes run Linux - understanding the underlying OS is essential
- **Container Runtime Knowledge:** Docker, containerd, and CRI-O all depend on Linux kernel features (cgroups, namespaces)
- **Cost Optimization:** Properly tuned Linux systems reduce cloud costs through better resource utilization
- **Security Baseline:** Container security starts with host OS security hardening
- **Troubleshooting Reality:** When things break, you need to know systemd, logs, processes, and networking

**2025 Trends:**
1. **Systemd Dominance:** Virtually all major distributions use systemd (RHEL, Ubuntu, Debian, Fedora, Arch)
2. **Immutable Infrastructure:** While infrastructure is more disposable, the fundamentals still matter
3. **eBPF and Modern Observability:** New tools (bpftrace, cilium) require deeper kernel knowledge
4. **Security Hardening Standard:** SELinux/AppArmor, secure boot, and kernel hardening are baseline expectations
5. **Automated Compliance:** Infrastructure-as-code requires understanding what you're automating

### How This Differs from Configuration Management

**This Skill Covers:**
- **Manual Administration:** Direct system management via command-line
- **System Internals:** Understanding how Linux works (processes, filesystems, networking)
- **Troubleshooting:** Diagnosing and fixing production issues
- **Performance Tuning:** Optimizing system resources for specific workloads

**NOT Covered (See Other Skills):**
- **Configuration Management at Scale:** Ansible, Puppet, Chef (see `configuration-management` skill)
- **Container Orchestration:** Kubernetes, Docker Swarm (see `kubernetes-operations` skill)
- **Security Hardening Deep Dive:** CIS benchmarks, compliance (see `security-hardening` skill)
- **CI/CD Pipelines:** Build and deployment automation (see `building-ci-pipelines` skill)

**Complementary Relationship:**
```
Linux Administration → Understand the system
Configuration Management → Automate the system at scale
Security Hardening → Harden the system
Kubernetes Operations → Orchestrate containers on the system
```

### Target Audience

**Primary Users:**
- DevOps engineers managing Linux servers
- Site Reliability Engineers (SREs) troubleshooting production issues
- Backend developers deploying applications
- Cloud engineers managing EC2/Compute Engine instances
- Platform engineers building internal tooling

**Skill Level Assumptions:**
- Comfortable with command line
- Basic understanding of Unix/Linux philosophy
- Familiar with common commands (ls, cd, grep, etc.)
- Needs guidance on systemd, performance tuning, advanced troubleshooting

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **Systemd Service Management**
   - Creating and managing systemd units (services, timers, targets)
   - Understanding unit file structure and dependencies
   - Service lifecycle (start, stop, restart, reload)
   - Systemd timers (modern cron replacement)
   - Target management (boot states, dependencies)

2. **Process Management and Monitoring**
   - Process inspection (ps, top, htop, pgrep, pidof)
   - Resource monitoring (CPU, memory, disk I/O)
   - Process control (kill, nice, renice, nohup)
   - Background jobs and daemons
   - Understanding process states and signals

3. **Filesystem Management**
   - Filesystem types (ext4, XFS, Btrfs, ZFS)
   - Logical Volume Manager (LVM) for flexible storage
   - Mounting and unmounting filesystems
   - Disk usage monitoring (df, du, ncdu)
   - RAID configurations (software RAID with mdadm)
   - Filesystem permissions and ACLs

4. **User and Group Management**
   - Creating and managing users (useradd, usermod, userdel)
   - Group management (groupadd, usermod -aG)
   - sudo configuration and security
   - PAM (Pluggable Authentication Modules)
   - Password policies and management

5. **Package Management**
   - apt (Debian/Ubuntu): install, update, upgrade, search
   - yum/dnf (RHEL/CentOS/Fedora): install, update, groupinstall
   - snap and flatpak (universal packages)
   - Repository management
   - Package troubleshooting (dependency conflicts, broken packages)

6. **Performance Tuning**
   - sysctl: Kernel parameter tuning
   - ulimits: Resource limits for processes
   - cgroups: Control group resource management
   - Swappiness tuning for memory optimization
   - TCP/IP stack tuning for network performance
   - I/O schedulers (none, mq-deadline, bfq, kyber)

7. **Log Management**
   - journald: Systemd's logging system
   - journalctl: Query and follow logs
   - rsyslog: Traditional syslog daemon
   - logrotate: Automatic log rotation and compression
   - Centralized logging (forwarding to ELK, Loki)

8. **Cron and Scheduled Tasks**
   - crontab syntax and scheduling
   - System cron vs. user cron
   - Systemd timers (modern alternative)
   - anacron for non-24/7 systems
   - at command for one-time scheduled tasks

9. **SSH Configuration and Security**
   - SSH key-based authentication
   - sshd_config hardening (disable root login, key-only auth)
   - SSH tunneling (port forwarding, SOCKS proxy)
   - SSH config file for connection management
   - SSH agent for key management

10. **Network Configuration**
    - ip command (modern replacement for ifconfig)
    - ss command (modern replacement for netstat)
    - Network interfaces configuration (netplan, NetworkManager)
    - DNS configuration (/etc/resolv.conf, systemd-resolved)
    - Firewall basics (ufw, firewalld, iptables)
    - Basic routing and network troubleshooting

### What This Skill Does NOT Cover

**Out of Scope:**
- **Advanced Networking:** BGP, OSPF, VLANs, network architecture
- **Deep Security:** Penetration testing, vulnerability assessment, intrusion detection
- **Kubernetes:** Container orchestration (separate skill)
- **Configuration Management:** Ansible playbooks, Puppet manifests (separate skill)
- **Monitoring at Scale:** Prometheus, Grafana, full observability stack
- **Backup Solutions:** Enterprise backup systems (Bacula, Amanda)

### Success Criteria

**A user successfully uses this skill when they can:**
1. Create and manage systemd services for custom applications
2. Troubleshoot production issues using logs, process monitoring, and system metrics
3. Tune Linux systems for specific workloads (web servers, databases, batch processing)
4. Configure users, groups, and sudo access securely
5. Manage disk space, filesystems, and LVM volumes
6. Use package managers effectively across distributions
7. Schedule tasks using cron and systemd timers
8. Secure SSH access and harden sshd configuration
9. Diagnose network connectivity issues
10. Apply performance tuning to optimize resource utilization

---

## Research Findings

### Research Date: December 3, 2025

**Research Tools Used:**
- Google Search Grounding (Vertex AI)
- Context7 for systemd documentation
- Official systemd documentation (systemd.io)

### Key Findings from 2025 Research

#### 1. Security Hardening Best Practices

**Critical Security Measures (2025 Standard):**

**SSH Hardening:**
- Disable root login: `PermitRootLogin no`
- Key-based authentication only (disable password auth)
- Restrict SSH to specific IP addresses (firewall rules)
- Change default SSH port (obscurity, not security)
- Use Fail2ban for brute-force protection

**Firewall Configuration:**
- UFW (Ubuntu) or firewalld (RHEL/CentOS) as primary tools
- Default deny policy, explicit allow rules
- Minimize open ports (only necessary services)
- Use TCP Wrappers for additional access control (`/etc/hosts.allow`, `/etc/hosts.deny`)

**System Updates:**
- Automate security updates: `unattended-upgrades` (Debian/Ubuntu), `dnf-automatic` (Fedora)
- Regular kernel updates with live patching (KernelCare, kpatch) for zero downtime
- Subscribe to security mailing lists (Ubuntu Security, RHEL Security)

**Access Control:**
- Principle of Least Privilege (PoLP): Grant minimal permissions
- Mandatory Access Control: SELinux (RHEL/CentOS/Fedora) or AppArmor (Ubuntu/SUSE)
- Disable unused services and remove unnecessary packages
- Regular security audits and compliance checks

**User Management:**
- Strong password policies (PAM configuration)
- Multi-factor authentication (MFA) for privileged access
- Regular user access reviews
- Disable/lock unused accounts

#### 2. Monitoring and Logging

**Essential Monitoring Tools:**

**System Performance:**
- **top/htop:** Real-time process monitoring
- **vmstat:** Virtual memory statistics
- **iostat:** Disk I/O statistics
- **free:** Memory usage
- **uptime/w:** Load averages and logged-in users

**Advanced Monitoring:**
- **Grafana + Prometheus + Node Exporter:** Modern metrics collection and visualization
- **Zabbix:** Comprehensive monitoring for servers, VMs, network devices
- **Checkmk:** All-in-one monitoring solution
- **SolarWinds:** Enterprise-grade monitoring (commercial)

**Log Management:**
- **Centralized Logging:** ELK Stack (Elasticsearch, Logstash, Kibana) or Graylog
- **journald:** Systemd's binary journal (journalctl for queries)
- **rsyslog:** Traditional syslog daemon (still widely used)
- **logrotate:** Automatic log rotation and compression

**Real-Time Alerts:**
- Set up alerts for critical KPIs (CPU spikes, memory exhaustion, disk space)
- Cloud-based monitoring (AWS CloudWatch, Azure Monitor, GCP Logging)
- PagerDuty/Opsgenie integration for incident response

#### 3. Performance Tuning Insights

**sysctl Tuning (2025 Recommendations):**

**Memory Management:**
```bash
# Reduce swappiness for servers (prefer RAM over swap)
vm.swappiness = 10  # Default is 60, lower = less swapping

# VFS cache pressure (how aggressively kernel reclaims directory/inode cache)
vm.vfs_cache_pressure = 50  # Default is 100
```

**Networking (High-Performance Servers):**
```bash
# TCP congestion control (BBR is modern, performant)
net.ipv4.tcp_congestion_control = bbr

# TCP buffer sizes (min, default, max) - for high-bandwidth connections
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216

# Increase max backlog for high connection rates
net.core.netdev_max_backlog = 250000

# Enable TCP selective acknowledgments and timestamps
net.ipv4.tcp_sack = 1
net.ipv4.tcp_timestamps = 0  # Disable for CPU efficiency (trade-off)
```

**ulimit Configuration (2025 Standards):**

**File Descriptors (Critical for Web Servers, Databases):**
```bash
# Temporary (current session)
ulimit -n 65536

# Permanent (/etc/security/limits.conf)
*  soft  nofile  65536
*  hard  nofile  65536
```

**Process Limits:**
```bash
# Maximum number of processes per user
*  soft  nproc  4096
*  hard  nproc  8192
```

**Best Practices:**
1. **Baseline First:** Measure performance before tuning
2. **Test Changes:** Apply sysctl changes temporarily (`sysctl -w`), test, then persist
3. **Monitor Impact:** Watch metrics after each change
4. **Document Everything:** Keep a changelog of tuning decisions
5. **Workload-Specific:** Database servers vs. web servers have different optimal settings

#### 4. Systemd Service Management (2025 Standard)

**Key Insights from Context7 Research:**

**Unit File Structure:**
- `/lib/systemd/system` - System-provided units (lowest priority, don't modify)
- `/run/systemd/system` - Runtime units (transient)
- `/etc/systemd/system` - Custom/override units (highest priority, customization goes here)

**Essential Service Directives:**

**[Unit] Section:**
- `Description=` - Human-readable description
- `After=` - Start after specified units/targets
- `Requires=` - Hard dependency (fails if dependency fails)
- `Wants=` - Soft dependency (continues if dependency fails)

**[Service] Section:**
- `Type=` - Service type:
  - `simple` - Default, process doesn't fork
  - `forking` - Process forks, systemd tracks parent
  - `oneshot` - Short-lived process (completes and exits)
  - `notify` - Process signals systemd when ready
- `ExecStart=` - Command to start service
- `ExecReload=` - Reload command (HUP signal often)
- `ExecStop=` - Stop command (default: SIGTERM)
- `Restart=` - Restart policy: `on-failure`, `always`, `on-success`, `on-abnormal`
- `RestartSec=` - Delay before restart (default 100ms)
- `User=`, `Group=` - Run as non-root user (security best practice)
- `WorkingDirectory=` - Set working directory
- `Environment=` - Set environment variables
- `PrivateTmp=true` - Use private /tmp (isolation)

**[Install] Section:**
- `WantedBy=` - Target to enable service with (usually `multi-user.target`)
- `Alias=` - Alternative names for the service

**Systemd Timers (Modern Cron Replacement):**
- `OnCalendar=` - Calendar-based scheduling (like cron)
- `OnBootSec=` - Time after boot
- `OnActiveSec=` - Time after service activation
- `Persistent=true` - Run missed timers after boot
- `AccuracySec=` - Timer accuracy (default 1min)

**Example Modern Service:**
```ini
[Unit]
Description=My Web Application
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=notify
User=webapp
Group=webapp
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/server
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5s
Environment="PORT=8080"
Environment="LOG_LEVEL=info"
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

#### 5. Automation and Infrastructure-as-Code

**Configuration Management Integration:**
- Ansible/Puppet/Chef automate Linux administration tasks
- This skill provides the foundation knowledge for what to automate
- Understanding manual administration helps debug automation failures

**Containerization Context:**
- Even with Docker/Kubernetes, the host OS needs management
- Node optimization affects container performance
- Security hardening applies to container hosts

---

## Linux Administration Taxonomy

### Category 1: Service Management (systemd)

**Purpose:** Manage system services, daemons, and scheduled tasks

**Components:**
- **systemd units:** Services (.service), timers (.timer), targets (.target), sockets (.socket)
- **systemctl:** Command-line interface for systemd
- **journalctl:** Query systemd journal logs
- **Unit file management:** Creating, editing, enabling/disabling services

**Common Use Cases:**
- Start/stop/restart web servers (nginx, apache)
- Create custom application services
- Schedule tasks with systemd timers
- Manage service dependencies
- Monitor service status and logs

**Key Commands:**
```bash
systemctl start service         # Start a service
systemctl stop service          # Stop a service
systemctl restart service       # Restart a service
systemctl reload service        # Reload config without restart
systemctl status service        # Check service status
systemctl enable service        # Enable at boot
systemctl disable service       # Disable at boot
systemctl list-units --type=service  # List all services
journalctl -u service -f        # Follow service logs
```

---

### Category 2: Process Management

**Purpose:** Monitor and control running processes

**Components:**
- **Process inspection:** ps, top, htop, pgrep, pidof
- **Process control:** kill, killall, pkill, nice, renice
- **Background execution:** nohup, disown, screen, tmux
- **Process signals:** SIGTERM, SIGKILL, SIGHUP, SIGUSR1, SIGUSR2

**Common Use Cases:**
- Find runaway processes consuming CPU/memory
- Gracefully terminate processes
- Run long-running tasks in background
- Adjust process priority (nice values)
- Monitor system resource usage

**Key Commands:**
```bash
ps aux                          # List all processes
ps aux | grep process_name      # Find specific process
top                             # Interactive process monitor
htop                            # Enhanced interactive monitor
pgrep -a process_name           # Find process by name
pidof process_name              # Get PID of process
kill -15 PID                    # SIGTERM (graceful shutdown)
kill -9 PID                     # SIGKILL (force kill)
killall process_name            # Kill all instances by name
nice -n 10 command              # Start with lower priority
renice -n 5 -p PID              # Change priority of running process
nohup command &                 # Run command immune to hangups
```

**Process States:**
- **R** - Running or runnable
- **S** - Sleeping (waiting for event)
- **D** - Uninterruptible sleep (usually I/O)
- **Z** - Zombie (terminated but not reaped)
- **T** - Stopped (by job control signal)

---

### Category 3: Filesystem Management

**Purpose:** Manage storage, filesystems, and disk space

**Components:**
- **Filesystem types:** ext4, XFS, Btrfs, ZFS
- **Volume management:** LVM (Logical Volume Manager), RAID (mdadm)
- **Mount management:** mount, umount, /etc/fstab
- **Disk usage:** df, du, ncdu
- **Permissions:** chmod, chown, chgrp, ACLs (getfacl, setfacl)

**Common Use Cases:**
- Create and mount new filesystems
- Manage LVM volumes for flexible storage
- Monitor disk usage and clean up
- Set appropriate file permissions
- Extend filesystems without downtime

**Key Commands:**
```bash
# Disk usage
df -h                           # Show filesystem usage (human-readable)
du -sh /path/to/dir             # Show directory size
ncdu /path                      # Interactive disk usage analyzer

# Mounting
mount /dev/sdb1 /mnt            # Mount filesystem
umount /mnt                     # Unmount filesystem
mount -a                        # Mount all filesystems in /etc/fstab
lsblk                           # List block devices

# LVM
pvcreate /dev/sdb               # Create physical volume
vgcreate vg_data /dev/sdb       # Create volume group
lvcreate -L 10G -n lv_data vg_data  # Create logical volume
lvextend -L +5G /dev/vg_data/lv_data  # Extend volume
resize2fs /dev/vg_data/lv_data  # Resize filesystem (ext4)

# Permissions
chmod 755 file                  # Set permissions (rwxr-xr-x)
chmod u+x script.sh             # Add execute for user
chown user:group file           # Change ownership
chgrp group file                # Change group

# ACLs (extended permissions)
getfacl file                    # Show ACLs
setfacl -m u:user:rw file       # Add user read/write access
```

**Filesystem Comparison:**

| Filesystem | Best For | Max File Size | Snapshots | Notes |
|------------|----------|---------------|-----------|-------|
| **ext4** | General purpose | 16 TB | No | Default on most distros |
| **XFS** | Large files, databases | 8 EB | No | RHEL default, excellent performance |
| **Btrfs** | Snapshots, CoW | 16 EB | Yes | Modern features, some stability concerns |
| **ZFS** | Enterprise, data integrity | 16 EB | Yes | Not in mainline kernel, excellent for NAS |

---

### Category 4: User and Group Management

**Purpose:** Manage user accounts, groups, and authentication

**Components:**
- **User management:** useradd, usermod, userdel, passwd
- **Group management:** groupadd, groupmod, groupdel, gpasswd
- **sudo configuration:** /etc/sudoers, visudo
- **Authentication:** PAM (Pluggable Authentication Modules)
- **User info:** id, whoami, w, who, last

**Common Use Cases:**
- Create user accounts for team members
- Add users to groups (docker, sudo, wheel)
- Configure sudo access for specific commands
- Lock/unlock accounts
- Set password policies

**Key Commands:**
```bash
# User management
useradd -m -s /bin/bash username        # Create user with home dir
passwd username                         # Set password
usermod -aG sudo username               # Add user to sudo group
usermod -L username                     # Lock user account
usermod -U username                     # Unlock user account
userdel -r username                     # Delete user and home dir

# Group management
groupadd groupname                      # Create group
usermod -aG groupname username          # Add user to group
gpasswd -a username groupname           # Alternative: add user to group
groups username                         # Show user's groups

# Information
id username                             # Show user ID and groups
whoami                                  # Current user
w                                       # Show who is logged in
who                                     # Show logged-in users
last                                    # Show login history

# sudo configuration
visudo                                  # Edit /etc/sudoers safely
# Example sudoers entries:
# username ALL=(ALL:ALL) ALL            # Full sudo access
# username ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
# %wheel ALL=(ALL) ALL                  # Group-based sudo access
```

**Password Policies (PAM):**
```bash
# /etc/pam.d/common-password (Debian/Ubuntu)
# /etc/pam.d/system-auth (RHEL/CentOS)

# Example: Enforce minimum password length and complexity
password requisite pam_pwquality.so retry=3 minlen=12 ucredit=-1 lcredit=-1 dcredit=-1
```

---

### Category 5: Package Management

**Purpose:** Install, update, and remove software packages

**Components:**
- **apt (Debian/Ubuntu):** apt, apt-get, apt-cache, dpkg
- **yum/dnf (RHEL/CentOS/Fedora):** yum, dnf, rpm
- **snap:** Universal packages (cross-distro)
- **flatpak:** Desktop application sandboxing
- **Repository management:** /etc/apt/sources.list, /etc/yum.repos.d/

**Common Use Cases:**
- Install software packages
- Update system packages (security patches)
- Search for available packages
- Remove unnecessary packages
- Manage third-party repositories

**apt (Debian/Ubuntu):**
```bash
apt update                      # Update package index
apt upgrade                     # Upgrade installed packages
apt full-upgrade                # Upgrade + handle dependencies
apt install package             # Install package
apt remove package              # Remove package (keep config)
apt purge package               # Remove package + config
apt autoremove                  # Remove unused dependencies
apt search keyword              # Search for packages
apt show package                # Show package details
dpkg -l                         # List installed packages
dpkg -L package                 # List files installed by package
```

**dnf/yum (RHEL/CentOS/Fedora):**
```bash
dnf update                      # Update all packages
dnf install package             # Install package
dnf remove package              # Remove package
dnf search keyword              # Search for packages
dnf info package                # Show package info
dnf list installed              # List installed packages
dnf groupinstall "Development Tools"  # Install package group
rpm -qa                         # List installed packages
rpm -ql package                 # List files from package
```

**snap (Universal Packages):**
```bash
snap install package            # Install snap package
snap refresh                    # Update all snaps
snap list                       # List installed snaps
snap remove package             # Remove snap
```

**Repository Management:**
```bash
# Debian/Ubuntu: Add PPA
add-apt-repository ppa:user/repo
apt update

# RHEL/CentOS: Add EPEL
dnf install epel-release

# Manual repo file (RHEL/CentOS)
# /etc/yum.repos.d/myrepo.repo
[myrepo]
name=My Repository
baseurl=https://repo.example.com/el/$releasever/$basearch/
enabled=1
gpgcheck=1
gpgkey=https://repo.example.com/RPM-GPG-KEY
```

---

### Category 6: Performance Tuning

**Purpose:** Optimize system performance for specific workloads

**Components:**
- **sysctl:** Kernel parameter tuning (/etc/sysctl.conf, /etc/sysctl.d/)
- **ulimits:** Resource limits (/etc/security/limits.conf)
- **cgroups:** Control group resource management
- **I/O schedulers:** none, mq-deadline, bfq, kyber
- **CPU governors:** performance, powersave, ondemand, schedutil

**Common Use Cases:**
- Tune network stack for high-throughput applications
- Increase file descriptor limits for web servers
- Reduce swapping for memory-intensive applications
- Optimize I/O for database servers
- CPU frequency scaling for power vs. performance

**sysctl Tuning:**
```bash
# View current value
sysctl vm.swappiness

# Set temporarily (until reboot)
sysctl -w vm.swappiness=10

# Set permanently (/etc/sysctl.conf or /etc/sysctl.d/99-custom.conf)
vm.swappiness = 10
net.ipv4.tcp_congestion_control = bbr

# Apply changes
sysctl -p
sysctl -p /etc/sysctl.d/99-custom.conf
```

**Common sysctl Tunings:**
```bash
# Memory management
vm.swappiness = 10                      # Reduce swapping (prefer RAM)
vm.vfs_cache_pressure = 50              # Keep more dentry/inode cache
vm.dirty_ratio = 15                     # % of RAM for dirty pages before blocking writes
vm.dirty_background_ratio = 5           # % before background writeback

# Networking (high-performance servers)
net.core.netdev_max_backlog = 250000    # Incoming packet queue
net.core.somaxconn = 4096               # Listen() backlog
net.ipv4.tcp_max_syn_backlog = 8192     # SYN queue size
net.ipv4.tcp_congestion_control = bbr   # Modern congestion control
net.ipv4.tcp_rmem = 4096 87380 16777216 # TCP read buffer (min default max)
net.ipv4.tcp_wmem = 4096 65536 16777216 # TCP write buffer

# Security
net.ipv4.conf.all.rp_filter = 1         # Prevent IP spoofing
net.ipv4.icmp_echo_ignore_broadcasts = 1 # Ignore broadcast pings
```

**ulimit Configuration:**
```bash
# Temporary (current session)
ulimit -n 65536                         # Max open files
ulimit -u 4096                          # Max processes

# Permanent (/etc/security/limits.conf)
*  soft  nofile  65536
*  hard  nofile  65536
*  soft  nproc   4096
*  hard  nproc   8192

# Per-user limits
username  soft  nofile  100000
username  hard  nofile  100000

# Verify limits
ulimit -a                               # Show all limits
cat /proc/PID/limits                    # Show limits for running process
```

**I/O Scheduler:**
```bash
# Check current scheduler
cat /sys/block/sda/queue/scheduler

# Change temporarily
echo mq-deadline > /sys/block/sda/queue/scheduler

# Change permanently (via kernel boot parameter)
# Add to GRUB_CMDLINE_LINUX in /etc/default/grub:
elevator=mq-deadline

# Update GRUB
update-grub                             # Debian/Ubuntu
grub2-mkconfig -o /boot/grub2/grub.cfg  # RHEL/CentOS
```

**Scheduler Recommendations:**
- **none:** NVMe SSDs (let device handle scheduling)
- **mq-deadline:** SSDs, default for most cases
- **bfq:** HDDs, desktop systems (better interactivity)
- **kyber:** Low-latency workloads

---

### Category 7: Log Management

**Purpose:** Manage system logs for troubleshooting and monitoring

**Components:**
- **journald:** Systemd's binary logging system
- **journalctl:** Query journald logs
- **rsyslog:** Traditional syslog daemon
- **logrotate:** Automatic log rotation
- **Log files:** /var/log/syslog, /var/log/messages, /var/log/auth.log

**Common Use Cases:**
- Troubleshoot service failures
- Monitor authentication attempts
- Track system errors and warnings
- Rotate logs to prevent disk space issues
- Forward logs to centralized logging systems

**journalctl Commands:**
```bash
# View all logs
journalctl

# Follow logs (like tail -f)
journalctl -f

# Show logs for specific service
journalctl -u nginx
journalctl -u nginx -f          # Follow service logs

# Filter by time
journalctl --since "2025-12-03 10:00:00"
journalctl --since yesterday
journalctl --since "1 hour ago"
journalctl --until "2025-12-03 11:00:00"

# Filter by priority
journalctl -p err               # Show errors only
journalctl -p warning           # Show warnings and above

# Show kernel messages
journalctl -k
journalctl -k --since "10 minutes ago"

# Show boot logs
journalctl -b                   # Current boot
journalctl -b -1                # Previous boot
journalctl --list-boots         # List all boots

# Output formats
journalctl -o json-pretty       # JSON format
journalctl -o cat               # Plain text (no metadata)

# Disk usage
journalctl --disk-usage
journalctl --vacuum-size=1G     # Keep only 1GB of logs
journalctl --vacuum-time=7d     # Keep only 7 days of logs
```

**rsyslog Configuration:**
```bash
# Main config: /etc/rsyslog.conf

# Example: Forward logs to remote server
*.* @@remote-host:514           # TCP
*.* @remote-host:514            # UDP

# Example: Custom log file
if $programname == 'myapp' then /var/log/myapp.log
& stop

# Restart rsyslog
systemctl restart rsyslog
```

**logrotate Configuration:**
```bash
# Config file: /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    daily                       # Rotate daily
    rotate 7                    # Keep 7 days of logs
    compress                    # Compress old logs
    delaycompress               # Compress on next rotation
    missingok                   # Don't error if log missing
    notifempty                  # Don't rotate empty logs
    create 0644 root root       # Create new log with these perms
    postrotate
        systemctl reload myapp  # Reload after rotation
    endscript
}

# Test logrotate
logrotate -d /etc/logrotate.d/myapp     # Dry run
logrotate -f /etc/logrotate.conf        # Force rotation
```

---

### Category 8: Scheduled Tasks (Cron & Systemd Timers)

**Purpose:** Schedule recurring and one-time tasks

**Components:**
- **cron:** Traditional Unix scheduler
- **crontab:** User-specific cron jobs
- **systemd timers:** Modern, systemd-integrated scheduling
- **anacron:** For systems not running 24/7
- **at:** One-time scheduled tasks

**Common Use Cases:**
- Schedule backups
- Run maintenance scripts
- Generate reports
- Clean up temporary files
- Restart services at specific times

**Crontab Syntax:**
```bash
# Edit crontab
crontab -e                      # Edit user crontab
crontab -l                      # List user crontab
crontab -r                      # Remove user crontab

# Crontab format: minute hour day month weekday command
# * * * * * command
# ┬ ┬ ┬ ┬ ┬
# │ │ │ │ └─── Day of week (0-7, 0 or 7 = Sunday)
# │ │ │ └───── Month (1-12)
# │ │ └─────── Day of month (1-31)
# │ └───────── Hour (0-23)
# └─────────── Minute (0-59)

# Examples
0 2 * * * /usr/local/bin/backup.sh              # Daily at 2:00 AM
*/5 * * * * /usr/local/bin/check-health.sh      # Every 5 minutes
0 3 * * 0 /usr/local/bin/weekly-cleanup.sh      # Weekly on Sunday at 3:00 AM
0 0 1 * * /usr/local/bin/monthly-report.sh      # Monthly on 1st at midnight
@reboot /usr/local/bin/startup-script.sh        # Run at boot
@daily /usr/local/bin/daily-task.sh             # Shortcut for daily
```

**System Cron:**
```bash
# System-wide cron directories
/etc/cron.d/            # System cron files
/etc/cron.daily/        # Scripts run daily
/etc/cron.hourly/       # Scripts run hourly
/etc/cron.weekly/       # Scripts run weekly
/etc/cron.monthly/      # Scripts run monthly

# Place executable scripts in these directories (no crontab syntax needed)
chmod +x /etc/cron.daily/my-backup
```

**Systemd Timers (Modern Alternative):**
```bash
# Create timer unit: /etc/systemd/system/backup.timer
[Unit]
Description=Daily Backup Timer

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 02:00:00       # Daily at 2:00 AM
Persistent=true                  # Run missed timers after boot
AccuracySec=5min                 # Allow 5-minute slack

[Install]
WantedBy=timers.target

# Corresponding service: /etc/systemd/system/backup.service
[Unit]
Description=Backup Service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
User=backup
Group=backup

# Enable and start timer
systemctl daemon-reload
systemctl enable backup.timer
systemctl start backup.timer
systemctl list-timers            # List all timers
```

**Systemd Timer Calendar Syntax:**
```bash
OnCalendar=daily                 # Every day at midnight
OnCalendar=weekly                # Every Monday at midnight
OnCalendar=*-*-* 02:00:00        # Daily at 2:00 AM
OnCalendar=Mon *-*-* 09:00:00    # Every Monday at 9:00 AM
OnCalendar=*-*-01 00:00:00       # 1st of every month
OnCalendar=*-01-01 00:00:00      # January 1st every year

# Relative timers
OnBootSec=5min                   # 5 minutes after boot
OnStartupSec=10min               # 10 minutes after systemd starts
OnActiveSec=1h                   # 1 hour after timer activated
```

---

### Category 9: SSH Configuration and Security

**Purpose:** Secure remote access and configuration

**Components:**
- **SSH server:** sshd (/etc/ssh/sshd_config)
- **SSH client:** ssh (/etc/ssh/ssh_config, ~/.ssh/config)
- **SSH keys:** ssh-keygen, ssh-copy-id
- **SSH agent:** ssh-agent, ssh-add
- **SSH tunneling:** Port forwarding, SOCKS proxy

**Common Use Cases:**
- Secure remote access to servers
- Passwordless authentication with SSH keys
- Restrict SSH access to specific users/IPs
- SSH tunneling for secure connections
- Manage multiple SSH connections efficiently

**SSH Key Setup:**
```bash
# Generate SSH key pair
ssh-keygen -t ed25519 -C "user@example.com"    # Modern, secure algorithm
ssh-keygen -t rsa -b 4096 -C "user@example.com" # RSA (broader compatibility)

# Copy public key to server
ssh-copy-id user@server
# Or manually:
cat ~/.ssh/id_ed25519.pub | ssh user@server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Set correct permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 600 ~/.ssh/authorized_keys
```

**sshd_config Hardening (/etc/ssh/sshd_config):**
```bash
# Disable root login
PermitRootLogin no

# Key-based authentication only
PasswordAuthentication no
PubkeyAuthentication yes

# Disable empty passwords
PermitEmptyPasswords no

# Use Protocol 2 only (Protocol 1 is insecure)
Protocol 2

# Restrict users
AllowUsers user1 user2
# Or restrict by group
AllowGroups sshusers

# Change default port (obscurity, not security)
Port 2222

# Disable X11 forwarding if not needed
X11Forwarding no

# Set login grace time
LoginGraceTime 30s

# Maximum authentication attempts
MaxAuthTries 3

# Restart sshd after changes
systemctl restart sshd
```

**SSH Client Config (~/.ssh/config):**
```bash
# Connection-specific settings
Host myserver
    HostName server.example.com
    User admin
    Port 2222
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host *.example.com
    User deploy
    IdentityFile ~/.ssh/deploy_key

# Defaults for all hosts
Host *
    ServerAliveInterval 60
    Compression yes
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600
```

**SSH Tunneling:**
```bash
# Local port forwarding (access remote service locally)
ssh -L 8080:localhost:80 user@server
# Now localhost:8080 forwards to server's localhost:80

# Remote port forwarding (expose local service to remote)
ssh -R 8080:localhost:3000 user@server
# Now server's localhost:8080 forwards to your localhost:3000

# Dynamic port forwarding (SOCKS proxy)
ssh -D 1080 user@server
# Configure browser to use localhost:1080 as SOCKS5 proxy

# Keep tunnel open in background
ssh -fN -L 8080:localhost:80 user@server
```

---

### Category 10: Network Configuration

**Purpose:** Configure and troubleshoot network connectivity

**Components:**
- **ip command:** Modern network configuration (replaces ifconfig)
- **ss command:** Socket statistics (replaces netstat)
- **Network managers:** netplan (Ubuntu), NetworkManager (RHEL/Fedora)
- **DNS:** /etc/resolv.conf, systemd-resolved
- **Firewall:** ufw (Ubuntu), firewalld (RHEL/CentOS), iptables

**Common Use Cases:**
- Configure static IP addresses
- Troubleshoot network connectivity
- View open ports and connections
- Configure DNS resolution
- Set up basic firewall rules

**ip Command:**
```bash
# Show network interfaces
ip addr show
ip a                            # Short form
ip link show                    # Show link status

# Configure IP address
ip addr add 192.168.1.100/24 dev eth0
ip addr del 192.168.1.100/24 dev eth0

# Bring interface up/down
ip link set eth0 up
ip link set eth0 down

# Show routing table
ip route show
ip route get 8.8.8.8            # Show route to specific IP

# Add/delete route
ip route add 10.0.0.0/24 via 192.168.1.1
ip route del 10.0.0.0/24

# Show neighbor table (ARP)
ip neigh show
```

**ss Command (Socket Statistics):**
```bash
# Show all connections
ss -tunap                       # TCP/UDP, numeric, all, processes

# Show listening ports
ss -tlnp                        # TCP, listening, numeric, processes
ss -ulnp                        # UDP, listening, numeric, processes

# Show established connections
ss -tnp state established

# Show connections for specific port
ss -tlnp | grep :80

# Show socket memory usage
ss -tm
```

**netplan Configuration (Ubuntu 18.04+):**
```bash
# Config file: /etc/netplan/01-netcfg.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: false
      addresses:
        - 192.168.1.100/24
      gateway4: 192.168.1.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4

# Apply configuration
netplan apply
netplan try                     # Test configuration (auto-rollback)
```

**NetworkManager (RHEL/CentOS/Fedora):**
```bash
# Command-line interface
nmcli device status
nmcli connection show

# Configure static IP
nmcli con mod eth0 ipv4.addresses 192.168.1.100/24
nmcli con mod eth0 ipv4.gateway 192.168.1.1
nmcli con mod eth0 ipv4.dns "8.8.8.8 8.8.4.4"
nmcli con mod eth0 ipv4.method manual
nmcli con up eth0
```

**DNS Configuration:**
```bash
# systemd-resolved (modern)
resolvectl status
resolvectl query example.com

# Traditional /etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
search example.com
```

**Firewall (ufw - Ubuntu):**
```bash
ufw status                      # Show firewall status
ufw enable                      # Enable firewall
ufw disable                     # Disable firewall

# Allow/deny rules
ufw allow 22/tcp                # Allow SSH
ufw allow 80/tcp                # Allow HTTP
ufw allow 443/tcp               # Allow HTTPS
ufw deny 23/tcp                 # Deny Telnet

# Allow from specific IP
ufw allow from 192.168.1.0/24

# Delete rule
ufw delete allow 80/tcp

# Default policies
ufw default deny incoming
ufw default allow outgoing
```

**Firewall (firewalld - RHEL/CentOS/Fedora):**
```bash
firewall-cmd --state            # Check if running
firewall-cmd --list-all         # List all rules

# Add service/port
firewall-cmd --add-service=http --permanent
firewall-cmd --add-port=8080/tcp --permanent
firewall-cmd --reload           # Apply changes

# Remove service/port
firewall-cmd --remove-service=http --permanent
firewall-cmd --reload

# Zone management
firewall-cmd --get-active-zones
firewall-cmd --zone=public --add-source=192.168.1.0/24 --permanent
```

---

## Decision Frameworks

### Framework 1: Which Service Manager Should I Use?

**Decision Tree:**

```
START: I need to manage a service

Q1: Is systemd available on this system?
  ├─ YES → Use systemd (modern standard)
  │         - Create .service unit file
  │         - Use systemctl for management
  │         - Use journalctl for logs
  │
  └─ NO → Is this a legacy SysV init system?
      ├─ YES → Use init scripts
      │         - /etc/init.d/ scripts
      │         - service command
      │         - /var/log/ text logs
      │
      └─ NO → Special case (Docker, embedded system)
                - Use appropriate init system
                - Consult documentation
```

**Reality Check (2025):**
- **99% of cases:** Use systemd (RHEL, Ubuntu, Debian, Fedora, Arch, SUSE)
- **Legacy systems:** SysV init (old distributions)
- **Containers:** Often no init system (process runs as PID 1)

**When to Create systemd Service:**
- Custom application deployment
- Background daemons
- Scheduled tasks (systemd timers)
- Process management with auto-restart

**When NOT to Create systemd Service:**
- One-time scripts (use cron or systemd timer)
- Interactive applications
- Short-lived processes (use ExecStart in existing service)

---

### Framework 2: How Do I Troubleshoot Performance Issues?

**Decision Tree:**

```
START: System is slow or unresponsive

STEP 1: Identify resource bottleneck
  → Run: top, htop, vmstat, iostat
  → Check: CPU usage, memory usage, disk I/O, load average

Q1: Is CPU usage high (>80% consistently)?
  ├─ YES → Find CPU-intensive processes
  │         - top (press Shift+P to sort by CPU)
  │         - ps aux --sort=-%cpu | head
  │         - Optimize or limit offending processes
  │         - Consider scaling (more CPU cores)
  │
  └─ NO → Q2

Q2: Is memory usage high (swap being used)?
  ├─ YES → Find memory-intensive processes
  │         - top (press Shift+M to sort by memory)
  │         - ps aux --sort=-%mem | head
  │         - Check for memory leaks
  │         - Reduce swappiness (vm.swappiness)
  │         - Add more RAM
  │
  └─ NO → Q3

Q3: Is disk I/O wait high (wa% in top)?
  ├─ YES → Find disk-intensive processes
  │         - iotop
  │         - iostat -x 1
  │         - Check disk health (smartctl)
  │         - Optimize I/O scheduler
  │         - Consider faster storage (SSD, NVMe)
  │
  └─ NO → Q4

Q4: Is load average high but resources seem OK?
  ├─ YES → Check for waiting processes
  │         - ps aux | grep D  (uninterruptible sleep)
  │         - Check for network issues
  │         - Check for locked files
  │
  └─ NO → Likely not a resource issue
            - Check application logs
            - Check network connectivity
            - Check external dependencies
```

**Performance Investigation Commands:**
```bash
# Quick overview
top                             # Real-time resource monitor
htop                            # Enhanced top
uptime                          # Load averages

# CPU analysis
mpstat 1                        # CPU statistics per core
pidstat 1                       # Per-process CPU usage

# Memory analysis
free -h                         # Memory and swap usage
vmstat 1                        # Virtual memory statistics
ps aux --sort=-%mem | head     # Top memory consumers

# Disk I/O analysis
iostat -x 1                     # Extended disk stats
iotop                           # Top-like for I/O
lsof | grep deleted             # Find processes using deleted files

# Network analysis
ss -tunap                       # Active connections
iftop                           # Network bandwidth monitor
nethogs                         # Per-process network usage
```

---

### Framework 3: Which Filesystem Should I Choose?

**Decision Matrix:**

| Use Case | Recommended Filesystem | Rationale |
|----------|------------------------|-----------|
| **General purpose server** | ext4 | Mature, stable, good performance |
| **Database server (PostgreSQL, MySQL)** | XFS | Excellent large file performance, RHEL default |
| **Large file storage (media, backups)** | XFS or ZFS | Handle large files well, ZFS has compression |
| **NAS/File server** | ZFS | Data integrity, snapshots, compression, RAID-Z |
| **Desktop/Laptop** | ext4 or Btrfs | ext4 for stability, Btrfs for snapshots |
| **High-performance computing** | XFS or Lustre | Parallel I/O, scalability |
| **Small embedded devices** | ext4 or F2FS | Low overhead, flash-friendly (F2FS) |

**Filesystem Feature Comparison:**

| Feature | ext4 | XFS | Btrfs | ZFS |
|---------|------|-----|-------|-----|
| **Maturity** | ★★★★★ | ★★★★★ | ★★★ | ★★★★ |
| **Performance** | ★★★★ | ★★★★★ | ★★★★ | ★★★★ |
| **Large files** | ★★★ | ★★★★★ | ★★★★ | ★★★★★ |
| **Snapshots** | ❌ | ❌ | ✅ | ✅ |
| **Compression** | ❌ | ❌ | ✅ | ✅ |
| **Data integrity** | ★★★ | ★★★★ | ★★★★★ | ★★★★★ |
| **Shrink support** | ✅ | ❌ | ✅ | ❌ |
| **In mainline kernel** | ✅ | ✅ | ✅ | ❌ (license) |

**Quick Decision:**
- **Don't overthink it:** ext4 is a safe default for most use cases
- **Database/large files:** XFS
- **Need snapshots:** Btrfs or ZFS
- **NAS/enterprise:** ZFS (via OpenZFS)

---

### Framework 4: Package Management Strategy

**Which Package Manager for Which Distro:**

| Distribution | Primary Package Manager | Package Format | Commands |
|--------------|-------------------------|----------------|----------|
| **Ubuntu/Debian** | apt | .deb | `apt install`, `apt update` |
| **RHEL/CentOS/Fedora** | dnf (yum) | .rpm | `dnf install`, `dnf update` |
| **Arch Linux** | pacman | .pkg.tar.zst | `pacman -S`, `pacman -Syu` |
| **openSUSE** | zypper | .rpm | `zypper install`, `zypper update` |
| **Universal (snap)** | snap | .snap | `snap install` |
| **Universal (flatpak)** | flatpak | .flatpak | `flatpak install` |

**When to Use Universal Packages (snap/flatpak):**
- ✅ Desktop applications (self-contained, sandboxed)
- ✅ Cross-distribution compatibility
- ✅ Latest versions not in distro repos
- ❌ System services (use native package manager)
- ❌ Performance-critical applications (more overhead)
- ❌ Minimal container images (bloated)

**Repository Management Strategy:**
1. **Prefer official repositories** (security, stability)
2. **Use PPAs/third-party repos cautiously** (Ubuntu PPAs, EPEL for RHEL)
3. **Pin package versions for stability** (production servers)
4. **Test updates in staging** before production

---

## Implementation Patterns

### Pattern 1: Creating a Systemd Service for Custom Application

**Scenario:** Deploy a custom web application as a systemd service

**Implementation:**

**Step 1: Create service unit file**
```bash
sudo nano /etc/systemd/system/myapp.service
```

**Step 2: Unit file content**
```ini
[Unit]
Description=My Web Application
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=notify
User=myapp
Group=myapp
WorkingDirectory=/opt/myapp
Environment="PORT=8080"
Environment="LOG_LEVEL=info"
Environment="DATABASE_URL=postgresql://localhost/myapp"
ExecStart=/opt/myapp/bin/server
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5s
StandardOutput=journal
StandardError=journal
PrivateTmp=true

# Security hardening
NoNewPrivileges=true
PrivateDevices=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/myapp /var/log/myapp

[Install]
WantedBy=multi-user.target
```

**Step 3: Enable and start service**
```bash
# Create user
sudo useradd -r -s /bin/false myapp

# Create directories
sudo mkdir -p /var/lib/myapp /var/log/myapp
sudo chown myapp:myapp /var/lib/myapp /var/log/myapp

# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable myapp.service

# Start service
sudo systemctl start myapp.service

# Check status
sudo systemctl status myapp.service

# View logs
sudo journalctl -u myapp -f
```

**Key Points:**
- `Type=notify` - Application signals systemd when ready (use `Type=simple` if app doesn't support sd_notify)
- `Restart=on-failure` - Auto-restart on crashes
- `After=network.target postgresql.service` - Start after network and database
- `Requires=postgresql.service` - Fail if database service fails
- Security hardening directives (`PrivateTmp`, `ProtectSystem`, etc.)

---

### Pattern 2: Systemd Timer (Cron Replacement)

**Scenario:** Run a backup script daily at 2:00 AM

**Implementation:**

**Step 1: Create service unit**
```bash
sudo nano /etc/systemd/system/backup.service
```

```ini
[Unit]
Description=Daily Backup

[Service]
Type=oneshot
User=backup
Group=backup
ExecStart=/usr/local/bin/backup.sh
StandardOutput=journal
StandardError=journal
```

**Step 2: Create timer unit**
```bash
sudo nano /etc/systemd/system/backup.timer
```

```ini
[Unit]
Description=Daily Backup Timer

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true
AccuracySec=5min

[Install]
WantedBy=timers.target
```

**Step 3: Enable and start timer**
```bash
sudo systemctl daemon-reload
sudo systemctl enable backup.timer
sudo systemctl start backup.timer

# List all timers
systemctl list-timers

# Check when timer will next activate
systemctl status backup.timer
```

**Advantages over cron:**
- Integrated with systemd logging (journalctl)
- `Persistent=true` runs missed jobs after system boot
- Better dependency management
- Easier to manage service and schedule together

---

### Pattern 3: Performance Tuning for Web Server

**Scenario:** Optimize Linux server for high-traffic web application

**Implementation:**

**Step 1: Create sysctl configuration**
```bash
sudo nano /etc/sysctl.d/99-web-server.conf
```

```bash
# Network performance tuning
net.core.somaxconn = 4096
net.core.netdev_max_backlog = 250000
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.tcp_congestion_control = bbr
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.ipv4.tcp_slow_start_after_idle = 0
net.ipv4.tcp_tw_reuse = 1

# Memory management
vm.swappiness = 10
vm.vfs_cache_pressure = 50

# File descriptor limits
fs.file-max = 2097152
```

**Step 2: Apply sysctl changes**
```bash
sudo sysctl -p /etc/sysctl.d/99-web-server.conf
```

**Step 3: Increase ulimits**
```bash
sudo nano /etc/security/limits.conf
```

```bash
# Web server user
nginx  soft  nofile  100000
nginx  hard  nofile  100000

# All users
*  soft  nofile  65536
*  hard  nofile  65536
```

**Step 4: Configure I/O scheduler for SSDs**
```bash
# Check current scheduler
cat /sys/block/nvme0n1/queue/scheduler

# Set to none for NVMe
echo none | sudo tee /sys/block/nvme0n1/queue/scheduler

# Make persistent (add to /etc/udev/rules.d/60-scheduler.rules)
ACTION=="add|change", KERNEL=="nvme[0-9]n[0-9]", ATTR{queue/scheduler}="none"
```

**Step 5: Verify and monitor**
```bash
# Check applied settings
sysctl net.core.somaxconn
ulimit -n

# Monitor performance
ss -s                           # Socket statistics
netstat -st                     # Network statistics
```

---

### Pattern 4: SSH Hardening

**Scenario:** Secure SSH access to production server

**Implementation:**

**Step 1: Generate SSH key (client side)**
```bash
ssh-keygen -t ed25519 -C "admin@example.com"
```

**Step 2: Copy key to server**
```bash
ssh-copy-id admin@server.example.com
```

**Step 3: Harden sshd_config (server side)**
```bash
sudo nano /etc/ssh/sshd_config
```

```bash
# Disable root login
PermitRootLogin no

# Key-based auth only
PasswordAuthentication no
PubkeyAuthentication yes
PermitEmptyPasswords no

# Protocol and security
Protocol 2
MaxAuthTries 3
LoginGraceTime 30s

# Restrict users
AllowUsers admin deploy
AllowGroups sshusers

# Disable unused features
X11Forwarding no
PermitTunnel no
AllowAgentForwarding no

# Change port (optional)
Port 2222

# Use strong ciphers (optional, modern defaults are good)
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
KexAlgorithms curve25519-sha256,diffie-hellman-group-exchange-sha256
```

**Step 4: Restart SSH (carefully!)**
```bash
# Test configuration first
sudo sshd -t

# Restart (keep current session open as backup)
sudo systemctl restart sshd
```

**Step 5: Configure firewall**
```bash
# Ubuntu (ufw)
sudo ufw allow 2222/tcp
sudo ufw delete allow 22/tcp

# RHEL/CentOS (firewalld)
sudo firewall-cmd --add-port=2222/tcp --permanent
sudo firewall-cmd --remove-service=ssh --permanent
sudo firewall-cmd --reload
```

**Step 6: Configure Fail2ban**
```bash
sudo apt install fail2ban  # Ubuntu
sudo dnf install fail2ban  # RHEL/CentOS

sudo nano /etc/fail2ban/jail.local
```

```ini
[sshd]
enabled = true
port = 2222
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
```

```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

### Pattern 5: Log Investigation Workflow

**Scenario:** Application is failing, need to diagnose from logs

**Investigation Workflow:**

**Step 1: Check service status**
```bash
sudo systemctl status myapp
```

**Step 2: View recent logs**
```bash
# Last 100 lines
sudo journalctl -u myapp -n 100

# Last 10 minutes
sudo journalctl -u myapp --since "10 minutes ago"

# Follow logs in real-time
sudo journalctl -u myapp -f
```

**Step 3: Filter by severity**
```bash
# Errors only
sudo journalctl -u myapp -p err

# Warnings and above
sudo journalctl -u myapp -p warning
```

**Step 4: Search for patterns**
```bash
# Grep for specific error
sudo journalctl -u myapp | grep "connection refused"

# Show context (10 lines before/after)
sudo journalctl -u myapp | grep -C 10 "database error"
```

**Step 5: Export logs for analysis**
```bash
# Export to file
sudo journalctl -u myapp --since "2025-12-03" > /tmp/myapp.log

# Export as JSON for parsing
sudo journalctl -u myapp -o json-pretty > /tmp/myapp.json
```

**Step 6: Check system logs if app logs insufficient**
```bash
# Kernel messages
sudo journalctl -k --since "1 hour ago"

# All services
sudo journalctl --since "1 hour ago"

# Authentication logs
sudo journalctl -u sshd --since today
```

**Step 7: Correlate with system metrics**
```bash
# Check if performance issue
top -b -n 1 | head -20

# Check disk space
df -h

# Check memory
free -h

# Check recent OOM kills
sudo journalctl -k | grep -i "out of memory"
```

---

## Tool Recommendations

### Essential Command-Line Tools (Standard on Most Distros)

**Process Management:**
- **ps** - Report process status (standard)
- **top** - Real-time process monitor (standard)
- **htop** - Enhanced interactive process viewer (install: `apt install htop`)
- **pgrep/pkill** - Find/kill processes by name (standard)

**System Monitoring:**
- **vmstat** - Virtual memory statistics (standard)
- **iostat** - I/O statistics (sysstat package: `apt install sysstat`)
- **mpstat** - CPU statistics (sysstat package)
- **free** - Memory usage (standard)
- **uptime** - Load averages (standard)

**Disk Management:**
- **df** - Disk space usage (standard)
- **du** - Directory space usage (standard)
- **lsblk** - List block devices (standard)
- **ncdu** - Interactive disk usage (install: `apt install ncdu`)

**Network Tools:**
- **ip** - Network configuration (standard, replaces ifconfig)
- **ss** - Socket statistics (standard, replaces netstat)
- **ping** - Test connectivity (standard)
- **traceroute** - Trace network path (standard)
- **dig/nslookup** - DNS queries (standard)
- **iftop** - Network bandwidth monitor (install: `apt install iftop`)
- **nethogs** - Per-process bandwidth (install: `apt install nethogs`)

**Log Analysis:**
- **journalctl** - Query systemd journal (standard with systemd)
- **grep** - Search text (standard)
- **less/more** - View files (standard)
- **tail** - View end of files (standard, `tail -f` for following)
- **awk/sed** - Text processing (standard)

### Advanced Monitoring Tools (Optional Install)

**Comprehensive Monitoring:**
- **Prometheus + Node Exporter + Grafana**
  - Modern metrics collection and visualization
  - Time-series database
  - Excellent for multiple servers
  - Install: Follow official docs (not in standard repos)

- **Zabbix**
  - All-in-one monitoring solution
  - Monitors servers, VMs, network devices, applications
  - Web-based dashboard
  - Install: `apt install zabbix-server-mysql zabbix-frontend-php`

- **Netdata**
  - Real-time performance monitoring
  - Web-based dashboard (http://localhost:19999)
  - Very easy to install and use
  - Install: `bash <(curl -Ss https://my-netdata.io/kickstart.sh)`

**Log Aggregation:**
- **ELK Stack (Elasticsearch + Logstash + Kibana)**
  - Centralized logging at scale
  - Powerful search and visualization
  - Resource-intensive
  - Install: Follow Elastic official docs

- **Graylog**
  - ELK alternative, easier to set up
  - Good for medium-scale deployments
  - Install: Official Graylog packages

**Performance Analysis:**
- **iotop** - I/O monitor like top (install: `apt install iotop`)
- **atop** - Advanced system monitor (install: `apt install atop`)
- **dstat** - Versatile resource statistics (install: `apt install dstat`)
- **sysstat** - Collection of tools (sar, iostat, mpstat)

**Network Analysis:**
- **tcpdump** - Packet capture (install: `apt install tcpdump`)
- **wireshark** - GUI packet analyzer (install: `apt install wireshark`)
- **nmap** - Network scanner (install: `apt install nmap`)
- **mtr** - Combined ping/traceroute (install: `apt install mtr`)

### Security Tools

**SSH Security:**
- **Fail2ban** - Intrusion prevention (install: `apt install fail2ban`)
- **ssh-audit** - SSH configuration audit (install: `pip install ssh-audit`)

**System Hardening:**
- **lynis** - Security auditing tool (install: `apt install lynis`)
- **rkhunter** - Rootkit detection (install: `apt install rkhunter`)
- **aide** - File integrity checking (install: `apt install aide`)

**Firewall:**
- **ufw** - Uncomplicated Firewall (Ubuntu, standard)
- **firewalld** - Dynamic firewall (RHEL/CentOS, standard)
- **iptables** - Low-level firewall (standard, ufw/firewalld frontend)

### Filesystem Tools

**LVM:**
- **lvm2** - Logical Volume Manager (standard on most distros)
- Commands: pvcreate, vgcreate, lvcreate, lvextend, lvreduce

**RAID:**
- **mdadm** - Software RAID (install: `apt install mdadm`)

**Filesystem-Specific:**
- **e2fsprogs** - ext4 tools (standard)
- **xfsprogs** - XFS tools (install: `apt install xfsprogs`)
- **btrfs-progs** - Btrfs tools (install: `apt install btrfs-progs`)
- **zfsutils-linux** - ZFS tools (install: `apt install zfsutils-linux`)

### Recommended Tool Stack by Role

**DevOps Engineer:**
- systemd + journalctl (service management, logs)
- htop, iostat, free (resource monitoring)
- Prometheus + Grafana (metrics visualization)
- Fail2ban (security)
- ansible (automation, separate skill)

**SRE (Site Reliability Engineer):**
- All DevOps tools plus:
- atop, dstat (advanced performance analysis)
- tcpdump, wireshark (network troubleshooting)
- strace, ltrace (process tracing)
- perf (CPU profiling)

**Security Engineer:**
- lynis, rkhunter (security auditing)
- aide (file integrity)
- fail2ban (intrusion prevention)
- auditd (system auditing)
- SELinux/AppArmor tools

**Backend Developer:**
- systemd basics (deploy services)
- journalctl (debug logs)
- top, free (basic resource monitoring)
- ss, curl (network debugging)
- strace (debug hanging processes)

---

## Skill Structure Design

### Skill File Organization

**Proposed Structure:**

```
linux-administration/
├── SKILL.md                    # Main skill file (<500 lines)
├── references/
│   ├── systemd-guide.md        # Comprehensive systemd reference
│   ├── performance-tuning.md   # sysctl, ulimits, cgroups details
│   ├── filesystem-management.md # LVM, RAID, filesystem types
│   ├── network-configuration.md # ip, ss, firewall details
│   ├── security-hardening.md   # SSH, firewall, SELinux basics
│   └── troubleshooting-guide.md # Common issues and solutions
├── examples/
│   ├── systemd-units/
│   │   ├── webapp.service      # Web application service
│   │   ├── backup.service      # Backup service
│   │   ├── backup.timer        # Corresponding timer
│   │   └── database.service    # Database service example
│   ├── scripts/
│   │   ├── backup.sh           # Example backup script
│   │   ├── health-check.sh     # Service health check
│   │   └── log-cleanup.sh      # Log rotation script
│   ├── configs/
│   │   ├── sshd_config.hardened # Hardened SSH config
│   │   ├── sysctl.conf.webserver # Web server tuning
│   │   ├── sysctl.conf.database  # Database tuning
│   │   └── logrotate.conf      # Log rotation config
│   └── workflows/
│       ├── deploy-app.sh       # Application deployment workflow
│       ├── troubleshoot-performance.sh # Performance investigation
│       └── security-audit.sh   # Basic security audit
└── assets/
    ├── cheatsheets/
    │   ├── systemctl-commands.md # Quick reference
    │   ├── journalctl-commands.md
    │   └── network-commands.md
    └── diagrams/
        └── systemd-boot-process.md # ASCII diagram
```

---

### SKILL.md Structure (Main File)

**Sections (Target: ~450 lines):**

1. **Frontmatter** (YAML)
   - name: `linux-administration`
   - description: "Comprehensive Linux system administration covering systemd, processes, filesystems, networking, performance tuning, and troubleshooting. Use when managing Linux servers, deploying applications, optimizing performance, or diagnosing production issues."

2. **Purpose** (2-3 paragraphs, ~30 lines)
   - What this skill teaches
   - When to use this skill
   - What it doesn't cover (links to other skills)

3. **Quick Start** (~50 lines)
   - Most common tasks with minimal explanation
   - Service management (systemctl basics)
   - Process monitoring (top, htop)
   - Log viewing (journalctl)

4. **Core Concepts** (~100 lines)
   - Systemd overview
   - Process management basics
   - Filesystem hierarchy
   - User/group management
   - Package management by distro

5. **Decision Frameworks** (~80 lines)
   - When to use systemd vs. cron
   - Which filesystem to choose
   - Performance tuning approach
   - Troubleshooting workflow

6. **Common Workflows** (~120 lines)
   - Creating systemd service
   - Setting up systemd timer
   - SSH hardening
   - Performance investigation
   - Log analysis

7. **Reference Links** (~30 lines)
   - Links to detailed references/ files
   - Links to examples/
   - External resources

8. **Integration Points** (~40 lines)
   - Kubernetes nodes (see kubernetes-operations)
   - Configuration management (see configuration-management)
   - CI/CD (see building-ci-pipelines)

---

### Progressive Disclosure Strategy

**Main SKILL.md Contains:**
- Essential commands with minimal explanation
- Decision trees for common scenarios
- Links to detailed references
- Quick examples (3-5 lines each)

**References/ Contains:**
- **systemd-guide.md** (~400 lines)
  - Detailed unit file syntax
  - All systemd commands
  - Advanced dependency management
  - Systemd targets and boot process

- **performance-tuning.md** (~350 lines)
  - Comprehensive sysctl parameters
  - ulimit configuration details
  - cgroups management
  - I/O schedulers
  - CPU governors
  - Workload-specific tuning

- **filesystem-management.md** (~300 lines)
  - LVM complete guide
  - RAID configuration
  - Filesystem comparison
  - Mounting and fstab
  - Permissions and ACLs

- **network-configuration.md** (~250 lines)
  - ip command complete reference
  - ss command details
  - netplan/NetworkManager
  - DNS configuration
  - Firewall rules

- **security-hardening.md** (~300 lines)
  - SSH hardening checklist
  - Firewall best practices
  - SELinux/AppArmor basics
  - User access control
  - Fail2ban configuration

- **troubleshooting-guide.md** (~350 lines)
  - Common issues and solutions
  - Performance bottleneck diagnosis
  - Service failure investigation
  - Network connectivity issues
  - Disk space problems

**Examples/ Contains:**
- Working systemd unit files (copy-paste ready)
- Shell scripts for common tasks
- Configuration file examples
- End-to-end workflows

**Assets/ Contains:**
- Quick reference cheatsheets
- ASCII diagrams for concepts
- Decision tree flowcharts

---

## Integration Points

### Integration with Existing Skills

#### 1. **kubernetes-operations** Skill

Linux administration is the foundation for Kubernetes node management.

**Integration Points:**
- **Node Optimization:** sysctl tuning for container networking
- **Systemd Services:** kubelet runs as systemd service
- **Log Management:** journald logs from kubelet and containers
- **Performance Tuning:** cgroups for container resource limits
- **Network Configuration:** CNI plugins interact with Linux networking

**Example Integration:**
```bash
# Optimize Linux node for Kubernetes
# /etc/sysctl.d/99-kubernetes.conf
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-ip6tables = 1

# Check kubelet service
systemctl status kubelet

# View kubelet logs
journalctl -u kubelet -f
```

---

#### 2. **configuration-management** Skill

Linux administration provides the knowledge; configuration management automates it.

**Integration Points:**
- **Ansible Playbooks:** Automate systemd service creation, user management
- **Puppet Manifests:** Codify system configuration
- **Understanding Automation:** Know what you're automating

**Example Integration (Ansible):**
```yaml
# Ansible playbook using Linux admin knowledge
- name: Configure web server
  hosts: webservers
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
      when: ansible_os_family == "Debian"

    - name: Create systemd service
      copy:
        src: files/myapp.service
        dest: /etc/systemd/system/myapp.service
      notify: Reload systemd

    - name: Apply sysctl tuning
      sysctl:
        name: "{{ item.key }}"
        value: "{{ item.value }}"
        state: present
      loop:
        - { key: "net.core.somaxconn", value: "4096" }
        - { key: "vm.swappiness", value: "10" }

  handlers:
    - name: Reload systemd
      systemd:
        daemon_reload: yes
```

---

#### 3. **security-hardening** Skill

Linux administration covers basics; security-hardening goes deeper.

**Integration Points:**
- **SSH Hardening:** This skill covers SSH config; security-hardening adds MFA, certificate auth
- **Firewall Basics:** This skill covers ufw/firewalld; security-hardening adds iptables deep dive
- **SELinux/AppArmor:** This skill introduces concepts; security-hardening provides policies
- **Compliance:** CIS benchmarks, STIG compliance

**Cross-Reference:**
- For basic SSH hardening: Use this skill
- For advanced security (MFA, hardware tokens, certificate authorities): Use security-hardening

---

#### 4. **building-ci-pipelines** Skill

CI/CD pipelines deploy to Linux servers.

**Integration Points:**
- **Deployment:** CI/CD creates systemd services on target servers
- **Health Checks:** Pipeline uses systemctl status for verification
- **Log Monitoring:** journalctl in pipeline for debugging
- **Rollback:** systemctl restart previous version

**Example Integration (GitHub Actions):**
```yaml
# .github/workflows/deploy.yml
- name: Deploy application
  run: |
    # Copy service file
    scp myapp.service $SSH_USER@$SERVER:/tmp/

    # SSH and deploy
    ssh $SSH_USER@$SERVER << 'EOF'
      sudo mv /tmp/myapp.service /etc/systemd/system/
      sudo systemctl daemon-reload
      sudo systemctl restart myapp
      sudo systemctl status myapp
      sudo journalctl -u myapp -n 50
    EOF
```

---

#### 5. **observability** Skill (If Exists)

Observability builds on basic Linux monitoring.

**Integration Points:**
- **Node Exporter:** Exposes Linux metrics to Prometheus
- **Log Forwarding:** journald → Loki/ELK
- **Tracing:** System-level tracing with bpftrace/eBPF
- **Metrics:** CPU, memory, disk metrics from Linux tools

**Example Integration:**
```bash
# Install node_exporter (Prometheus)
sudo useradd -rs /bin/false node_exporter
sudo cp node_exporter /usr/local/bin/
sudo cp node_exporter.service /etc/systemd/system/

# Systemd service for node_exporter
[Unit]
Description=Prometheus Node Exporter
After=network.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable node_exporter
sudo systemctl start node_exporter
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)

**Deliverables:**
- [x] Complete init.md (this document)
- [ ] Create SKILL.md main file (~450 lines)
- [ ] Write references/systemd-guide.md
- [ ] Create examples/systemd-units/ (3-5 example services)

**Content Focus:**
- Systemd basics (most critical for modern Linux)
- Quick start guide
- Common workflows

**Validation:**
- Test all systemd examples on Ubuntu 22.04 and RHEL 9
- Verify commands work as documented

---

### Phase 2: Core Skills (Week 2)

**Deliverables:**
- [ ] Write references/performance-tuning.md
- [ ] Write references/filesystem-management.md
- [ ] Create examples/configs/ (sysctl, limits.conf)
- [ ] Create examples/scripts/ (backup, health-check)

**Content Focus:**
- Performance tuning (sysctl, ulimits)
- Filesystem management (LVM, RAID basics)
- Practical scripts

**Validation:**
- Test sysctl configurations on test VMs
- Verify LVM commands work correctly

---

### Phase 3: Networking & Security (Week 3)

**Deliverables:**
- [ ] Write references/network-configuration.md
- [ ] Write references/security-hardening.md
- [ ] Create examples/configs/sshd_config.hardened
- [ ] Add firewall examples

**Content Focus:**
- Network configuration (ip, ss, netplan)
- SSH hardening
- Firewall basics

**Validation:**
- Test SSH hardening on test server
- Verify firewall rules work correctly

---

### Phase 4: Troubleshooting & Workflows (Week 4)

**Deliverables:**
- [ ] Write references/troubleshooting-guide.md
- [ ] Create examples/workflows/ (troubleshooting scripts)
- [ ] Create assets/cheatsheets/
- [ ] Add ASCII diagrams

**Content Focus:**
- Troubleshooting workflows
- Common issues and solutions
- Decision trees

**Validation:**
- Walk through troubleshooting workflows on problematic systems
- Verify cheatsheets are accurate

---

### Phase 5: Integration & Polish (Week 5)

**Deliverables:**
- [ ] Cross-link with related skills
- [ ] Add integration examples (Kubernetes, Ansible)
- [ ] Review all content for consistency
- [ ] Test all examples end-to-end

**Content Focus:**
- Integration points with other skills
- Real-world examples
- Final polish

**Validation:**
- Full skill walkthrough with fresh tester
- Verify all links work
- Check progressive disclosure flow

---

## Validation Checklist

### Before Creating SKILL.md

- [x] Research complete (Google Search Grounding, Context7)
- [x] Tool recommendations validated
- [x] Decision frameworks designed
- [x] Implementation patterns documented
- [x] Integration points with other skills identified
- [x] Bash examples verified (commands work on Ubuntu/RHEL)

### Before Finalizing Skill

- [ ] SKILL.md under 500 lines
- [ ] All references/ files created and complete
- [ ] All examples/ tested on Ubuntu 22.04 and RHEL 9
- [ ] Progressive disclosure effective (main → references → examples)
- [ ] Tested with real scenarios (deploy app, troubleshoot issue, tune performance)
- [ ] Cross-references to other skills verified
- [ ] Bash examples tested (no typos, correct syntax)
- [ ] Integration examples work (Kubernetes, Ansible, CI/CD)

---

## Success Metrics

**This skill is successful if users can:**

1. **Service Management:**
   - Create custom systemd services for applications
   - Manage service lifecycle (start, stop, restart, enable)
   - Use systemd timers for scheduled tasks
   - Read and interpret service logs with journalctl

2. **Performance Optimization:**
   - Apply sysctl tuning for specific workloads
   - Configure ulimits for resource-intensive applications
   - Identify performance bottlenecks (CPU, memory, I/O)
   - Optimize I/O schedulers for different storage types

3. **System Administration:**
   - Manage users, groups, and sudo access
   - Install and update packages across distributions
   - Configure SSH securely (keys, hardening)
   - Manage filesystems and LVM volumes

4. **Troubleshooting:**
   - Diagnose service failures using logs and status
   - Investigate performance issues systematically
   - Resolve network connectivity problems
   - Debug disk space and filesystem issues

5. **Security:**
   - Harden SSH configuration
   - Configure firewalls (ufw, firewalld)
   - Set appropriate file permissions
   - Implement basic security best practices

---

## Future Enhancements

**Potential Additions (Not in Initial Release):**

1. **Advanced Systemd:**
   - Socket activation
   - Path units
   - Slice units (cgroup management)
   - systemd-nspawn containers

2. **Advanced Networking:**
   - Bridge configuration for containers/VMs
   - VLAN configuration
   - Bonding/teaming for high availability
   - Advanced iptables rules

3. **Advanced Storage:**
   - ZFS administration deep dive
   - Btrfs snapshots and management
   - NFS/CIFS server configuration
   - iSCSI configuration

4. **Monitoring Integration:**
   - Prometheus node_exporter configuration
   - ELK stack setup for centralized logging
   - Grafana dashboard setup
   - Custom metric collection

5. **eBPF and Modern Tracing:**
   - bpftrace for performance analysis
   - perf tools for CPU profiling
   - strace/ltrace for debugging
   - eBPF-based monitoring tools

---

## Appendix: Distribution-Specific Notes

### Ubuntu/Debian

**Package Manager:** apt
**Init System:** systemd
**Network Manager:** netplan (18.04+), NetworkManager
**Firewall:** ufw
**Default Shell:** bash
**Notable Differences:**
- Uses `/etc/apt/sources.list` for repositories
- PPAs for third-party software
- `update-alternatives` for managing alternatives

### RHEL/CentOS/Fedora

**Package Manager:** dnf (yum on older versions)
**Init System:** systemd
**Network Manager:** NetworkManager
**Firewall:** firewalld
**Default Shell:** bash
**Notable Differences:**
- Uses `/etc/yum.repos.d/` for repositories
- EPEL for additional packages
- SELinux enabled by default

### Arch Linux

**Package Manager:** pacman
**Init System:** systemd
**Network Manager:** NetworkManager or netctl
**Firewall:** ufw or iptables
**Default Shell:** bash
**Notable Differences:**
- Rolling release model
- AUR (Arch User Repository) for community packages
- Very minimal base install

---

## References

**Research Sources:**
- Google Search Grounding (Vertex AI): Linux administration best practices 2025
- Context7 Documentation: systemd.io (/websites/systemd_io)
- Official systemd documentation: https://systemd.io/
- Linux kernel documentation: https://kernel.org/doc/
- Distribution-specific documentation (Ubuntu, RHEL, Arch)

**Related Skills:**
- `kubernetes-operations` - Container orchestration on Linux nodes
- `configuration-management` - Automate Linux administration at scale
- `security-hardening` - Advanced Linux security and compliance
- `building-ci-pipelines` - Deploy to Linux servers via CI/CD
- `observability` - Monitor Linux systems at scale

---

**Document Status:** ✅ Complete
**Next Step:** Create SKILL.md from this master plan
**Owner:** AI Design Components Project
**Last Updated:** December 3, 2025
