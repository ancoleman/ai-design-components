# Performance Tuning Guide

Complete reference for optimizing Linux system performance through sysctl, ulimits, cgroups, I/O schedulers, and workload-specific tuning.

## Table of Contents

1. [Performance Analysis Methodology](#performance-analysis-methodology)
2. [sysctl Kernel Parameter Tuning](#sysctl-kernel-parameter-tuning)
3. [ulimit Resource Limits](#ulimit-resource-limits)
4. [Control Groups (cgroups)](#control-groups-cgroups)
5. [I/O Schedulers](#io-schedulers)
6. [CPU Governors](#cpu-governors)
7. [Workload-Specific Tuning](#workload-specific-tuning)
8. [Monitoring and Validation](#monitoring-and-validation)

## Performance Analysis Methodology

### Baseline First

**Before tuning, establish baseline:**

1. **Measure current performance**
   ```bash
   # CPU metrics
   mpstat 1 10                     # 10 samples, 1 second apart

   # Memory metrics
   free -h && vmstat 1 10

   # Disk I/O
   iostat -x 1 10

   # Network
   sar -n DEV 1 10
   ```

2. **Identify bottleneck**
   - CPU: High user/system time, low idle
   - Memory: High swap usage, low free/available
   - Disk: High I/O wait (wa%), high service times
   - Network: High packet loss, retransmissions

3. **Apply one change at a time**
4. **Measure impact**
5. **Document everything**

### Performance Investigation Tools

```bash
# Overview
top                              # Real-time
htop                             # Enhanced
uptime                           # Load averages

# CPU
mpstat 1                         # Per-CPU stats
pidstat -u 1                     # Per-process CPU
perf top                         # CPU profiling

# Memory
free -h                          # Memory usage
vmstat 1                         # Virtual memory stats
smem -t                          # Memory by process

# Disk I/O
iostat -x 1                      # Extended disk stats
iotop -oPa                       # I/O by process
lsof | grep deleted              # Deleted files still open

# Network
ss -tunap                        # Connections
iftop                            # Bandwidth
nethogs                          # Per-process network
```

## sysctl Kernel Parameter Tuning

### sysctl Basics

**View current value:**
```bash
sysctl vm.swappiness
sysctl -a | grep tcp             # All TCP parameters
```

**Set temporarily (until reboot):**
```bash
sudo sysctl -w vm.swappiness=10
```

**Set permanently:**
```bash
# Create file in /etc/sysctl.d/
sudo nano /etc/sysctl.d/99-custom.conf

# Add parameters
vm.swappiness = 10
net.ipv4.tcp_congestion_control = bbr

# Apply immediately
sudo sysctl -p /etc/sysctl.d/99-custom.conf

# Or reload all
sudo sysctl --system
```

### Memory Management Parameters

**Swappiness:**
```bash
# vm.swappiness (0-100, default 60)
# Lower = prefer RAM, higher = more aggressive swapping

vm.swappiness = 10                # Good for servers (prefer RAM)
vm.swappiness = 60                # Default (balanced)
vm.swappiness = 1                 # Minimal swapping (databases)
vm.swappiness = 100               # Aggressive swapping (unusual)
```

**VFS Cache Pressure:**
```bash
# vm.vfs_cache_pressure (default 100)
# Lower = keep dentry/inode cache longer
# Higher = reclaim faster

vm.vfs_cache_pressure = 50        # Keep more cached (file servers)
vm.vfs_cache_pressure = 100       # Default
vm.vfs_cache_pressure = 200       # Aggressive reclaim (memory-constrained)
```

**Dirty Page Writeback:**
```bash
# Controls when dirty pages written to disk

# vm.dirty_ratio (default 20)
# % of RAM that can be dirty before blocking writes
vm.dirty_ratio = 15               # Start blocking at 15% RAM

# vm.dirty_background_ratio (default 10)
# % of RAM that triggers background writeback
vm.dirty_background_ratio = 5     # Earlier background writes

# vm.dirty_expire_centisecs (default 3000 = 30 seconds)
# Age before dirty page written
vm.dirty_expire_centisecs = 1500  # Write after 15 seconds

# vm.dirty_writeback_centisecs (default 500 = 5 seconds)
# Interval for writeback daemon
vm.dirty_writeback_centisecs = 300  # Check every 3 seconds
```

**Overcommit:**
```bash
# vm.overcommit_memory (default 0)
# 0 = Heuristic (default, sane overcommit)
# 1 = Always overcommit (no checks)
# 2 = Never overcommit (strict accounting)

vm.overcommit_memory = 0          # Default (recommended)

# vm.overcommit_ratio (default 50)
# % of RAM to allow overcommit (when mode = 2)
vm.overcommit_ratio = 80          # Allow 80% overcommit
```

**Transparent Huge Pages (THP):**
```bash
# Check status
cat /sys/kernel/mm/transparent_hugepage/enabled

# Disable (recommended for databases like MongoDB, Redis)
echo never | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
echo never | sudo tee /sys/kernel/mm/transparent_hugepage/defrag

# Make persistent (add to /etc/rc.local or systemd service)
```

### Network Parameters

**TCP Congestion Control:**
```bash
# View available algorithms
sysctl net.ipv4.tcp_available_congestion_control

# Set BBR (modern, high-performance)
net.ipv4.tcp_congestion_control = bbr

# Alternatives:
# cubic (default) - Good for most cases
# reno - Classical TCP
# htcp - High-speed TCP
```

**Enable BBR (requires kernel 4.9+):**
```bash
# Load modules
sudo modprobe tcp_bbr
echo "tcp_bbr" | sudo tee -a /etc/modules-load.d/modules.conf

# Enable BBR
echo "net.ipv4.tcp_congestion_control=bbr" | sudo tee -a /etc/sysctl.d/99-bbr.conf
sudo sysctl -p /etc/sysctl.d/99-bbr.conf
```

**TCP Buffer Sizes:**
```bash
# net.ipv4.tcp_rmem (min default max)
# Read buffer sizes
net.ipv4.tcp_rmem = 4096 87380 16777216   # 4KB min, 85KB default, 16MB max

# net.ipv4.tcp_wmem (min default max)
# Write buffer sizes
net.ipv4.tcp_wmem = 4096 65536 16777216   # 4KB min, 64KB default, 16MB max

# net.core.rmem_max / net.core.wmem_max
# Maximum socket buffer sizes
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216

# net.core.rmem_default / net.core.wmem_default
# Default socket buffer sizes
net.core.rmem_default = 262144
net.core.wmem_default = 262144
```

**Connection Queue Sizes:**
```bash
# net.core.somaxconn
# Max listen() backlog
net.core.somaxconn = 4096         # Default 128 (too low for busy servers)

# net.ipv4.tcp_max_syn_backlog
# Max SYN queue size
net.ipv4.tcp_max_syn_backlog = 8192  # Default 1024

# net.core.netdev_max_backlog
# Max packets in input queue
net.core.netdev_max_backlog = 250000  # Default 1000
```

**TCP Tuning:**
```bash
# TIME_WAIT reuse (connections in TIME_WAIT state)
net.ipv4.tcp_tw_reuse = 1         # Reuse TIME_WAIT sockets (safe)

# Keepalive settings
net.ipv4.tcp_keepalive_time = 600     # Send keepalive after 10 min idle
net.ipv4.tcp_keepalive_intvl = 60     # Probe interval
net.ipv4.tcp_keepalive_probes = 3     # Max probes before drop

# Fast open (reduce latency)
net.ipv4.tcp_fastopen = 3         # 3 = client and server

# Slow start after idle
net.ipv4.tcp_slow_start_after_idle = 0  # Disable for persistent connections

# Timestamps (helps with high-bandwidth connections)
net.ipv4.tcp_timestamps = 1       # Enable (adds 12 bytes per packet)

# SACK (Selective Acknowledgment)
net.ipv4.tcp_sack = 1             # Enable (improves performance on lossy networks)

# Window scaling (essential for high-bandwidth)
net.ipv4.tcp_window_scaling = 1   # Enable

# MTU probing (avoid fragmentation)
net.ipv4.tcp_mtu_probing = 1      # Enable
```

**Security:**
```bash
# SYN flood protection
net.ipv4.tcp_syncookies = 1       # Enable SYN cookies

# IP forwarding (routers/NAT)
net.ipv4.ip_forward = 1           # Enable forwarding

# Reverse path filtering (prevent IP spoofing)
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Ignore ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0

# Ignore source routed packets
net.ipv4.conf.all.accept_source_route = 0

# Ignore broadcast pings
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Ignore bogus ICMP errors
net.ipv4.icmp_ignore_bogus_error_responses = 1

# Log martians (packets with impossible addresses)
net.ipv4.conf.all.log_martians = 1
```

### Filesystem Parameters

```bash
# fs.file-max
# Maximum file handles
fs.file-max = 2097152             # Default ~100k

# fs.nr_open
# Per-process file descriptor limit
fs.nr_open = 2097152

# fs.aio-max-nr
# Maximum async I/O requests
fs.aio-max-nr = 1048576           # Default 65536
```

### Kernel Parameters

```bash
# kernel.pid_max
# Maximum PID value
kernel.pid_max = 4194304          # Default 32768

# kernel.threads-max
# Maximum number of threads
kernel.threads-max = 4194304

# kernel.panic
# Seconds before reboot after kernel panic
kernel.panic = 10                 # Reboot after 10 seconds

# kernel.panic_on_oops
# Panic on kernel oops
kernel.panic_on_oops = 1          # Recommended for production
```

## ulimit Resource Limits

### Understanding ulimits

User-level resource limits per process.

**View current limits:**
```bash
ulimit -a                         # All limits
ulimit -n                         # Open files
ulimit -u                         # Max processes
```

**Set temporarily (current session):**
```bash
ulimit -n 65536                   # Max open files
ulimit -u 4096                    # Max user processes
```

### Permanent ulimit Configuration

**Edit `/etc/security/limits.conf`:**
```bash
# Format: <domain> <type> <item> <value>
# domain: username, @groupname, *
# type: soft (warning), hard (enforced)
# item: nofile, nproc, memlock, stack, etc.

# Example: Web server user
nginx  soft  nofile  100000
nginx  hard  nofile  100000

# Example: All users
*      soft  nofile  65536
*      hard  nofile  65536
*      soft  nproc   4096
*      hard  nproc   8192

# Example: Database user (PostgreSQL, MySQL)
postgres  soft  nofile  200000
postgres  hard  nofile  200000
postgres  soft  nproc   16384
postgres  hard  nproc   16384

# Example: Allow memory locking (for databases)
postgres  soft  memlock  unlimited
postgres  hard  memlock  unlimited
```

**Drop-in files (recommended):**
```bash
# Create file per application
sudo nano /etc/security/limits.d/99-myapp.conf

myapp  soft  nofile  100000
myapp  hard  nofile  100000
```

### Common ulimit Items

| Item | Description | Common Values |
|------|-------------|---------------|
| `nofile` | Max open files | 65536 (web), 200000 (db) |
| `nproc` | Max processes | 4096-16384 |
| `memlock` | Max locked memory | unlimited (databases) |
| `stack` | Stack size | 8192 KB (default) |
| `fsize` | Max file size | unlimited |
| `cpu` | Max CPU time (seconds) | unlimited |
| `as` | Max address space | unlimited |
| `locks` | Max file locks | unlimited |
| `sigpending` | Max pending signals | 16384 |
| `msgqueue` | Max message queue size | 819200 |
| `nice` | Max nice priority | 0 |
| `rtprio` | Max realtime priority | 0 |

### Systemd Service Limits

Override ulimits in systemd units:

```ini
[Service]
LimitNOFILE=100000                # Max open files
LimitNPROC=16384                  # Max processes
LimitMEMLOCK=infinity             # Memory locking
LimitCORE=infinity                # Core dump size
```

View service limits:
```bash
systemctl show myapp.service | grep ^Limit
cat /proc/$(pidof myapp)/limits
```

## Control Groups (cgroups)

### cgroups v2 (Modern)

**Check version:**
```bash
mount | grep cgroup
stat -fc %T /sys/fs/cgroup
# cgroup2fs = v2, tmpfs = v1
```

### Resource Limits via Systemd

Systemd manages cgroups automatically.

**CPU Limits:**
```ini
[Service]
# CPUQuota - Percentage of CPU time (200% = 2 CPUs)
CPUQuota=50%                      # Limit to 50% of one CPU core

# CPUWeight - Relative CPU share (1-10000, default 100)
CPUWeight=200                     # 2x priority
CPUWeight=50                      # 0.5x priority

# Enable CPU accounting
CPUAccounting=yes
```

**Memory Limits:**
```ini
[Service]
# MemoryMax - Hard limit (kills process if exceeded)
MemoryMax=2G

# MemoryHigh - Soft limit (throttles before hard limit)
MemoryHigh=1.5G

# MemoryMin - Guaranteed memory
MemoryMin=512M

# Enable memory accounting
MemoryAccounting=yes
```

**I/O Limits:**
```ini
[Service]
# IOWeight - I/O priority (1-10000, default 100)
IOWeight=500

# IOReadBandwidthMax - Read bandwidth limit
IOReadBandwidthMax=/dev/sda 10M

# IOWriteBandwidthMax - Write bandwidth limit
IOWriteBandwidthMax=/dev/sda 5M

# IOReadIOPSMax - Read IOPS limit
IOReadIOPSMax=/dev/sda 1000

# IOWriteIOPSMax - Write IOPS limit
IOWriteIOPSMax=/dev/sda 500

# Enable I/O accounting
IOAccounting=yes
```

**Task Limits:**
```ini
[Service]
# TasksMax - Maximum number of tasks (processes/threads)
TasksMax=100                      # Limit to 100 tasks
TasksMax=50%                      # 50% of system TasksMax
TasksMax=infinity                 # No limit
```

**View cgroup usage:**
```bash
systemctl status myapp.service    # Shows CPU/memory usage
systemd-cgtop                     # Interactive cgroup monitor
```

### Custom Slices

Group services with shared resources:

```ini
# /etc/systemd/system/myapp.slice
[Unit]
Description=My Application Resource Slice

[Slice]
CPUQuota=200%                     # 2 CPUs for all services in slice
MemoryMax=4G                      # 4GB total
```

Assign services to slice:
```ini
[Service]
Slice=myapp.slice
```

## I/O Schedulers

### Available Schedulers

Modern Linux uses multi-queue (blk-mq) schedulers:

| Scheduler | Best For | Description |
|-----------|----------|-------------|
| `none` | NVMe SSDs | No scheduling (device handles it) |
| `mq-deadline` | SSDs | Deadline-based, default for most SSDs |
| `bfq` | HDDs, desktops | Budget Fair Queueing, interactive |
| `kyber` | Low-latency | Adaptive, low-latency focused |

**Legacy (single-queue) schedulers:**
- `cfq` - Completely Fair Queueing (deprecated)
- `deadline` - Deadline-based (deprecated)
- `noop` - No scheduling (deprecated)

### Check Current Scheduler

```bash
cat /sys/block/sda/queue/scheduler
# Output: [mq-deadline] none kyber bfq
# [ ] = currently active
```

### Change Scheduler Temporarily

```bash
echo none | sudo tee /sys/block/nvme0n1/queue/scheduler
echo mq-deadline | sudo tee /sys/block/sda/queue/scheduler
```

### Change Scheduler Permanently

**Method 1: udev rule**
```bash
sudo nano /etc/udev/rules.d/60-scheduler.rules

# NVMe: use none
ACTION=="add|change", KERNEL=="nvme[0-9]n[0-9]", ATTR{queue/scheduler}="none"

# SSDs: use mq-deadline
ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/rotational}=="0", ATTR{queue/scheduler}="mq-deadline"

# HDDs: use bfq
ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/rotational}=="1", ATTR{queue/scheduler}="bfq"
```

**Method 2: kernel boot parameter**
```bash
# Edit /etc/default/grub
GRUB_CMDLINE_LINUX="elevator=mq-deadline"

# Update GRUB
sudo update-grub                  # Debian/Ubuntu
sudo grub2-mkconfig -o /boot/grub2/grub.cfg  # RHEL/CentOS
```

### Scheduler Recommendations

**NVMe SSDs:**
```bash
echo none > /sys/block/nvme0n1/queue/scheduler
```

**SATA SSDs:**
```bash
echo mq-deadline > /sys/block/sda/queue/scheduler
```

**HDDs:**
```bash
echo bfq > /sys/block/sda/queue/scheduler
```

**Low-latency workloads:**
```bash
echo kyber > /sys/block/sda/queue/scheduler
```

## CPU Governors

### Available Governors

Control CPU frequency scaling:

| Governor | Behavior | Use Case |
|----------|----------|----------|
| `performance` | Max frequency always | High-performance servers |
| `powersave` | Min frequency always | Battery saving |
| `ondemand` | Scale on load (fast) | General purpose |
| `conservative` | Scale gradually | Battery, less aggressive |
| `schedutil` | Scheduler-driven (modern) | Default (recommended) |
| `userspace` | Manual control | Testing, specific tuning |

### Check Current Governor

```bash
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
# Or
cpupower frequency-info
```

### Change Governor

**Temporary:**
```bash
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

**Permanent (systemd):**
```bash
sudo nano /etc/systemd/system/cpufreq-performance.service

[Unit]
Description=Set CPU Governor to Performance

[Service]
Type=oneshot
ExecStart=/bin/bash -c "echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable cpufreq-performance.service
sudo systemctl start cpufreq-performance.service
```

**Using cpupower:**
```bash
sudo apt install linux-tools-common  # Ubuntu
sudo dnf install kernel-tools         # RHEL/Fedora

# Set governor
sudo cpupower frequency-set -g performance

# View info
cpupower frequency-info
cpupower monitor
```

## Workload-Specific Tuning

### Web Server Tuning

```bash
# /etc/sysctl.d/99-web-server.conf

# Network
net.core.somaxconn = 4096
net.core.netdev_max_backlog = 250000
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.tcp_congestion_control = bbr
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.ipv4.tcp_slow_start_after_idle = 0
net.ipv4.tcp_tw_reuse = 1

# Memory
vm.swappiness = 10
vm.vfs_cache_pressure = 50

# File descriptors
fs.file-max = 2097152
```

```bash
# /etc/security/limits.d/99-nginx.conf
nginx  soft  nofile  100000
nginx  hard  nofile  100000
```

**I/O Scheduler:** none (NVMe) or mq-deadline (SSD)
**CPU Governor:** schedutil or performance

### Database Server Tuning

```bash
# /etc/sysctl.d/99-database.conf

# Memory (minimal swapping)
vm.swappiness = 1
vm.vfs_cache_pressure = 50
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5

# Huge pages (for large databases)
vm.nr_hugepages = 1024  # Calculate based on memory needs

# Overcommit (strict)
vm.overcommit_memory = 2
vm.overcommit_ratio = 80

# Network (if applicable)
net.core.somaxconn = 4096
net.ipv4.tcp_congestion_control = bbr

# File descriptors
fs.file-max = 2097152
fs.aio-max-nr = 1048576
```

```bash
# /etc/security/limits.d/99-postgres.conf
postgres  soft  nofile  200000
postgres  hard  nofile  200000
postgres  soft  nproc   16384
postgres  hard  nproc   16384
postgres  soft  memlock  unlimited
postgres  hard  memlock  unlimited
```

**Disable Transparent Huge Pages:**
```bash
echo never | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
echo never | sudo tee /sys/kernel/mm/transparent_hugepage/defrag
```

**I/O Scheduler:** none (NVMe) or mq-deadline (SSD)
**CPU Governor:** performance

### High-Throughput File Server

```bash
# /etc/sysctl.d/99-file-server.conf

# Memory (cache files aggressively)
vm.swappiness = 10
vm.vfs_cache_pressure = 30    # Keep dentry/inode cache longer
vm.dirty_ratio = 40           # Allow more dirty pages
vm.dirty_background_ratio = 10

# Network
net.core.rmem_max = 67108864
net.core.wmem_max = 67108864
net.ipv4.tcp_rmem = 4096 87380 67108864
net.ipv4.tcp_wmem = 4096 65536 67108864

# File descriptors
fs.file-max = 4194304
```

**I/O Scheduler:** none (NVMe) or mq-deadline (SSD)

## Monitoring and Validation

### Before and After Comparison

**CPU:**
```bash
# Before tuning
mpstat 1 60 > before_cpu.txt

# After tuning
mpstat 1 60 > after_cpu.txt

# Compare
diff before_cpu.txt after_cpu.txt
```

**Memory:**
```bash
vmstat 1 60 > before_memory.txt
# ... apply changes ...
vmstat 1 60 > after_memory.txt
```

**Network:**
```bash
sar -n DEV 1 60 > before_network.txt
# ... apply changes ...
sar -n DEV 1 60 > after_network.txt
```

### Continuous Monitoring

**sysstat (sar):**
```bash
sudo apt install sysstat
sudo systemctl enable sysstat

# View historical data
sar -u                            # CPU
sar -r                            # Memory
sar -b                            # Disk I/O
sar -n DEV                        # Network
```

**Prometheus Node Exporter:**
```bash
# Install node_exporter
# Expose metrics at :9100/metrics
# Visualize in Grafana
```

### Performance Testing

**CPU stress test:**
```bash
sudo apt install stress-ng
stress-ng --cpu 4 --timeout 60s
```

**Memory stress test:**
```bash
stress-ng --vm 2 --vm-bytes 2G --timeout 60s
```

**Disk I/O benchmark:**
```bash
sudo apt install fio

# Sequential read
fio --name=seqread --rw=read --bs=1M --size=1G --numjobs=1

# Random read
fio --name=randread --rw=randread --bs=4k --size=1G --numjobs=4

# Sequential write
fio --name=seqwrite --rw=write --bs=1M --size=1G --numjobs=1
```

**Network benchmark:**
```bash
sudo apt install iperf3

# Server
iperf3 -s

# Client
iperf3 -c server_ip -t 60
```

## Best Practices

1. **Establish baseline before changes**
2. **Apply one change at a time**
3. **Test in staging first**
4. **Monitor impact continuously**
5. **Document all changes**
6. **Keep configuration in version control**
7. **Use workload-specific tuning**
8. **Don't tune without measuring**

## References

- sysctl.conf(5) man page: `man sysctl.conf`
- limits.conf(5) man page: `man limits.conf`
- systemd.resource-control(5): `man systemd.resource-control`
- Linux kernel documentation: https://kernel.org/doc/Documentation/sysctl/
