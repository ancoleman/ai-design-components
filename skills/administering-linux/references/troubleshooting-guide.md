# Troubleshooting Guide

Comprehensive guide for diagnosing and resolving common Linux system issues.

## Table of Contents

1. [Service Failures](#service-failures)
2. [Performance Issues](#performance-issues)
3. [Network Problems](#network-problems)
4. [Disk Space Issues](#disk-space-issues)
5. [Memory Problems](#memory-problems)
6. [Permission Errors](#permission-errors)
7. [Boot Issues](#boot-issues)
8. [Process Problems](#process-problems)

## Service Failures

### Symptom: Service Won't Start

**Investigation Steps:**

1. **Check service status**
   ```bash
   systemctl status myapp.service
   ```

2. **View full logs**
   ```bash
   journalctl -u myapp.service -n 100
   journalctl -u myapp.service --since "5 minutes ago"
   ```

3. **Check unit file syntax**
   ```bash
   systemd-analyze verify myapp.service
   ```

4. **Test executable manually**
   ```bash
   sudo -u myapp /usr/bin/myapp
   ```

**Common Causes:**

**Missing executable:**
```bash
# Symptom: "Failed to execute command: No such file or directory"
# Solution: Check path
which myapp
ls -la /usr/bin/myapp
```

**Permission denied:**
```bash
# Symptom: "Permission denied"
# Solution: Fix permissions
sudo chmod +x /usr/bin/myapp
sudo chown myapp:myapp /usr/bin/myapp
```

**User doesn't exist:**
```bash
# Symptom: "Failed to look up user"
# Solution: Create user
sudo useradd -r -s /bin/false myapp
```

**Missing directory:**
```bash
# Symptom: "No such file or directory" for WorkingDirectory
# Solution: Create directory
sudo mkdir -p /var/lib/myapp
sudo chown myapp:myapp /var/lib/myapp
```

**Port already in use:**
```bash
# Symptom: "Address already in use"
# Solution: Find process using port
sudo ss -tlnp | grep :8080
sudo kill PID
```

### Symptom: Service Starts Then Stops

**Investigation:**
```bash
journalctl -u myapp.service -f    # Follow logs in real-time
```

**Common Causes:**

**Type mismatch:**
```ini
# Wrong: Type=forking but process doesn't fork
[Service]
Type=simple                        # Use simple for most cases

# Wrong: Type=simple but process forks
[Service]
Type=forking
PIDFile=/var/run/myapp.pid        # Must specify PID file
```

**Missing RemainAfterExit:**
```ini
# For oneshot services that should stay "active"
[Service]
Type=oneshot
RemainAfterExit=yes
```

**Application crash:**
```bash
# Check for segfaults, core dumps
journalctl -k | grep -i segfault
coredumpctl list
coredumpctl info PID
```

**Memory limit:**
```bash
# Check for OOM kills
journalctl -k | grep -i "out of memory"
dmesg | grep oom

# Solution: Increase limit
[Service]
MemoryMax=2G
```

### Symptom: Dependency Timeout

**Investigation:**
```bash
systemctl list-dependencies myapp.service
systemctl list-dependencies --reverse myapp.service
```

**Solution:**
```ini
# Increase timeout
[Service]
TimeoutStartSec=300               # 5 minutes (default 90s)

# Or make dependency optional
[Unit]
Wants=slow-service.service        # Instead of Requires
```

## Performance Issues

### High CPU Usage

**Investigation:**
```bash
top                               # Press Shift+P for CPU sort
htop                              # Enhanced view
ps aux --sort=-%cpu | head -10   # Top 10 CPU consumers
mpstat -P ALL 1                   # Per-CPU statistics
```

**Common Causes:**

**Runaway process:**
```bash
# Find and kill
pgrep -a process_name
kill -15 PID                      # SIGTERM (graceful)
kill -9 PID                       # SIGKILL (force)
```

**CPU-bound application:**
```bash
# Reduce priority (nice)
renice -n 10 -p PID               # Lower priority

# Limit CPU with systemd
systemctl edit myapp.service
[Service]
CPUQuota=50%                      # Limit to 50% of one core
```

**High system time (kernel):**
```bash
# Check I/O wait
top                               # Look at wa% column
iostat -x 1                       # Disk I/O stats

# Check context switches
vmstat 1                          # cs = context switches/sec
pidstat -w 1                      # Per-process context switches
```

### High Memory Usage / Swap

**Investigation:**
```bash
free -h                           # Memory overview
top                               # Press Shift+M for memory sort
ps aux --sort=-%mem | head -10   # Top memory consumers
smem -tk                          # Memory by process (with swap)
```

**Common Causes:**

**Memory leak:**
```bash
# Monitor memory over time
watch -n 5 'ps aux --sort=-%mem | head -10'

# Restart affected service
systemctl restart myapp.service
```

**Excessive swap:**
```bash
# Check swap usage
swapon --show
cat /proc/swaps

# Reduce swappiness
sudo sysctl -w vm.swappiness=10
echo "vm.swappiness = 10" | sudo tee -a /etc/sysctl.d/99-swap.conf
```

**Insufficient memory:**
```bash
# Check OOM kills
journalctl -k | grep -i oom

# Solutions:
# 1. Add more RAM
# 2. Reduce application memory
# 3. Add swap (temporary)
```

**Page cache using memory:**
```bash
# This is normal! Linux uses free memory for cache
# Check "available" memory, not "free"
free -h
# "available" is what matters

# Clear cache if needed (usually not necessary)
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
```

### High Disk I/O Wait

**Investigation:**
```bash
iostat -x 1                       # Extended disk stats
iotop -oPa                        # I/O by process (requires install)
lsof | grep deleted               # Deleted files still open
```

**Common Causes:**

**Heavy disk activity:**
```bash
# Find I/O-intensive processes
iotop -oPa

# Check specific disk
iostat -x 1 /dev/sda

# High %util = disk saturated
# High await = high latency
```

**Slow storage:**
```bash
# Benchmark disk
sudo hdparm -Tt /dev/sda          # Sequential read

# Or use fio
fio --name=read --rw=read --bs=1M --size=1G
```

**Wrong I/O scheduler:**
```bash
# Check scheduler
cat /sys/block/sda/queue/scheduler

# For SSDs/NVMe
echo mq-deadline | sudo tee /sys/block/sda/queue/scheduler
echo none | sudo tee /sys/block/nvme0n1/queue/scheduler
```

**Deleted files still open:**
```bash
# Find processes holding deleted files
lsof | grep deleted

# Restart services to release
systemctl restart service_name
```

### High Load Average

**Understanding Load Average:**
- 1-minute, 5-minute, 15-minute averages
- Load of 1.0 = one CPU fully utilized
- Load > number of CPUs = some processes waiting

**Investigation:**
```bash
uptime                            # Load averages
cat /proc/loadavg                 # Detailed load info
mpstat 1                          # CPU utilization
```

**High load but low CPU:**
```bash
# Processes in uninterruptible sleep (I/O wait)
ps aux | grep D                   # D state = waiting for I/O
iostat -x 1                       # Check disk I/O
```

## Network Problems

### Cannot Connect to Service

**Investigation:**
```bash
# Check if service listening
ss -tlnp | grep :80
netstat -tlnp | grep :80          # Legacy alternative

# Check connectivity
ping server_ip
telnet server_ip 80
curl -v http://server_ip
```

**Common Causes:**

**Service not running:**
```bash
systemctl status nginx
systemctl start nginx
```

**Firewall blocking:**
```bash
# Ubuntu (ufw)
sudo ufw status
sudo ufw allow 80/tcp

# RHEL/CentOS (firewalld)
sudo firewall-cmd --list-all
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --reload

# iptables
sudo iptables -L -n -v
```

**Wrong port/IP:**
```bash
# Check what IP service binds to
ss -tlnp | grep :80
# 0.0.0.0:80 = all interfaces
# 127.0.0.1:80 = localhost only

# Fix in application config or use:
nginx -t                          # Test nginx config
```

**DNS issues:**
```bash
# Test DNS resolution
nslookup example.com
dig example.com
host example.com

# Check resolver
cat /etc/resolv.conf
resolvectl status
```

### Slow Network Performance

**Investigation:**
```bash
# Check bandwidth
iftop                             # Real-time bandwidth
nethogs                           # Per-process bandwidth
iperf3 -c server                  # Bandwidth test

# Check latency
ping server
mtr server                        # Combined ping/traceroute

# Check dropped packets
netstat -s | grep -i drop
ip -s link show eth0
```

**Common Causes:**

**Network congestion:**
```bash
# Check interface statistics
ip -s link show eth0

# Look for:
# RX errors, dropped
# TX errors, dropped
```

**MTU issues:**
```bash
# Check MTU
ip link show eth0

# Test path MTU
ping -M do -s 1472 server         # 1472 + 28 = 1500
```

**TCP tuning needed:**
```bash
# Increase TCP buffers (for high-bandwidth links)
sudo sysctl -w net.ipv4.tcp_rmem="4096 87380 16777216"
sudo sysctl -w net.ipv4.tcp_wmem="4096 65536 16777216"
```

### Port Conflict

**Symptom: "Address already in use"**

**Investigation:**
```bash
# Find process using port
sudo ss -tlnp | grep :8080
sudo lsof -i :8080
sudo fuser 8080/tcp

# Kill process
sudo kill -9 PID

# Or change service port
```

## Disk Space Issues

### Disk Full

**Investigation:**
```bash
df -h                             # Filesystem usage
df -i                             # Inode usage (can be full!)
du -sh /*                         # Usage by top-level dir
du -sh /var/* | sort -h           # Find large directories
ncdu /var                         # Interactive disk analyzer
```

**Common Causes:**

**Log files:**
```bash
# Find large log files
find /var/log -type f -size +100M

# Check log size
du -sh /var/log/*

# Rotate logs manually
sudo logrotate -f /etc/logrotate.conf

# Clear systemd journal
sudo journalctl --vacuum-size=500M
sudo journalctl --vacuum-time=7d
```

**Deleted files still open:**
```bash
# Find processes holding deleted files
sudo lsof | grep deleted | grep -v /tmp

# Restart service to release
systemctl restart service_name
```

**Package cache:**
```bash
# Ubuntu/Debian
sudo apt clean
sudo apt autoremove

# RHEL/CentOS/Fedora
sudo dnf clean all
```

**Temp files:**
```bash
# Clear /tmp (be careful!)
sudo find /tmp -type f -atime +7 -delete

# Clear user caches
rm -rf ~/.cache/*
```

**Docker images/containers:**
```bash
docker system df                  # Docker disk usage
docker system prune -a            # Remove unused data
docker volume prune               # Remove unused volumes
```

### Inode Exhaustion

**Symptom:** "No space left on device" but df shows space available

**Investigation:**
```bash
df -i                             # Check inode usage
```

**Solution:**
```bash
# Find directories with many files
for dir in /*; do echo $dir; find $dir -xdev | wc -l; done

# Common culprits:
# - /var/spool/postfix (mail queue)
# - /tmp (many small files)
# - /var/lib/php/sessions

# Remove unnecessary files
find /tmp -type f -delete
```

## Memory Problems

### OOM (Out of Memory) Killer

**Symptom:** Processes killed randomly

**Investigation:**
```bash
# Check for OOM kills
journalctl -k | grep -i oom
dmesg | grep -i oom
grep -i oom /var/log/kern.log
```

**View OOM scores:**
```bash
# Higher score = more likely to be killed
for proc in /proc/[0-9]*; do
  printf "%2d %s\n" "$(cat $proc/oom_score 2>/dev/null)" "$(cat $proc/cmdline 2>/dev/null | tr '\000' ' ')";
done | sort -rn | head -10
```

**Solutions:**

1. **Add more RAM or swap**
2. **Reduce application memory usage**
3. **Adjust OOM score (discourage killing critical services)**
   ```bash
   echo -1000 | sudo tee /proc/PID/oom_score_adj  # Less likely to kill
   ```

4. **Systemd service protection**
   ```ini
   [Service]
   OOMScoreAdjust=-500            # Less likely to kill
   ```

### Memory Leak Detection

**Monitor memory over time:**
```bash
# Watch specific process
watch -n 5 'ps aux --sort=-%mem | head -10'

# Or use pidstat
pidstat -r -p PID 5               # Memory stats every 5 seconds

# Log to file for analysis
while true; do
  date >> mem.log
  ps aux --sort=-%mem | head -10 >> mem.log
  sleep 60
done
```

**Tools:**
- Valgrind (for C/C++ applications)
- heaptrack (heap memory profiler)
- Application-specific tools (Node.js heap snapshots, Python tracemalloc)

## Permission Errors

### Permission Denied

**Common Scenarios:**

**File permissions:**
```bash
ls -la /path/to/file              # Check permissions
# Fix:
sudo chmod 644 file               # rw-r--r--
sudo chmod 755 script             # rwxr-xr-x
sudo chown user:group file
```

**Directory permissions:**
```bash
# Execute bit required to enter directory
chmod +x directory
```

**SELinux (RHEL/CentOS):**
```bash
# Check SELinux status
getenforce

# Check SELinux denials
ausearch -m avc -ts recent
grep avc /var/log/audit/audit.log

# Temporary: Set permissive mode
sudo setenforce 0

# Fix SELinux contexts
restorecon -Rv /path
chcon -t httpd_sys_content_t /var/www/html

# Create SELinux policy (if needed)
audit2allow -a -M mypolicy
semodule -i mypolicy.pp
```

**AppArmor (Ubuntu):**
```bash
# Check AppArmor status
sudo aa-status

# Check denials
sudo dmesg | grep -i apparmor
sudo journalctl | grep -i apparmor

# Disable profile (temporary)
sudo aa-complain /etc/apparmor.d/usr.bin.nginx

# Edit profile
sudo nano /etc/apparmor.d/usr.bin.nginx
```

**sudo access:**
```bash
# Check sudo config
sudo visudo

# Add user to sudo group
sudo usermod -aG sudo username    # Debian/Ubuntu
sudo usermod -aG wheel username   # RHEL/CentOS
```

## Boot Issues

### System Won't Boot

**Emergency shell:**
1. At GRUB, press 'e' to edit boot entry
2. Add `systemd.unit=rescue.target` or `systemd.unit=emergency.target` to kernel line
3. Press Ctrl+X to boot

**Common causes:**

**Filesystem error:**
```bash
# Run filesystem check
fsck /dev/sda1
```

**fstab error:**
```bash
# Comment out problematic line
nano /etc/fstab
```

**Failed service blocking boot:**
```bash
# Check failed units
systemctl --failed

# Mask service temporarily
systemctl mask failing-service.service
```

### Slow Boot

**Investigation:**
```bash
systemd-analyze                   # Total boot time
systemd-analyze blame             # Time per unit
systemd-analyze critical-chain    # Critical path
```

**Common causes:**
- Slow network service (waiting for DHCP)
- Filesystem check
- Slow service startup

**Solutions:**
- Make services optional with `Wants=` instead of `Requires=`
- Use `After=network-online.target` for network services
- Increase timeout for slow services

## Process Problems

### Zombie Processes

**Symptom:** Processes in `Z` state

**Investigation:**
```bash
ps aux | grep Z                   # Find zombies
ps aux | grep 'Z'
```

**Cause:** Parent process hasn't reaped child process

**Solution:**
- Usually harmless (parent will reap eventually)
- If many zombies: restart parent process
- Killing zombie won't work (already dead)

### Hung Process

**Symptom:** Process not responding

**Investigation:**
```bash
# Check process state
ps aux | grep process_name        # Look for D state

# D state = uninterruptible sleep (usually I/O)
# Check I/O
iotop
iostat -x 1

# Trace syscalls
strace -p PID                     # See what process doing
lsof -p PID                       # See open files

# Check locks
lslocks                           # Show file locks
```

**Solution:**
- Wait for I/O to complete (D state usually temporary)
- Kill if truly hung: `kill -9 PID`
- Fix underlying I/O issue

### Too Many Open Files

**Symptom:** "Too many open files"

**Investigation:**
```bash
# Check current limit
ulimit -n

# Check process usage
lsof -p PID | wc -l
cat /proc/PID/limits
```

**Solution:**
```bash
# Increase limit temporarily
ulimit -n 65536

# Increase permanently
# Edit /etc/security/limits.conf
username soft nofile 65536
username hard nofile 65536

# For systemd service
[Service]
LimitNOFILE=65536
```

## General Troubleshooting Workflow

1. **Define the problem clearly**
   - What's not working?
   - What's the expected behavior?
   - When did it start?

2. **Gather information**
   - Check logs: `journalctl`, `/var/log/`
   - Check status: `systemctl status`, `top`, `df -h`
   - Check network: `ss`, `ping`

3. **Form hypothesis**
   - Based on symptoms and logs
   - Consider recent changes

4. **Test hypothesis**
   - Make one change at a time
   - Document changes
   - Verify impact

5. **Fix and document**
   - Apply permanent fix
   - Document in runbook
   - Monitor for recurrence

## Useful Commands Reference

**System overview:**
```bash
uptime                            # Load averages
top                               # Real-time monitor
htop                              # Enhanced monitor
df -h                             # Disk usage
free -h                           # Memory usage
```

**Logs:**
```bash
journalctl -xe                    # Recent logs with explanations
journalctl -f                     # Follow all logs
journalctl -u service -f          # Follow service logs
dmesg                             # Kernel ring buffer
```

**Network:**
```bash
ss -tunap                         # All connections
ip addr                           # IP addresses
ip route                          # Routing table
ping server                       # Connectivity
```

**Processes:**
```bash
ps aux                            # All processes
pgrep -a name                     # Find by name
kill -15 PID                      # Graceful kill
kill -9 PID                       # Force kill
```

**Files:**
```bash
lsof                              # Open files
lsof -p PID                       # Files for process
lsof -i :80                       # Process using port
find / -name filename             # Find file
```

## References

- systemd.service(5): `man systemd.service`
- journalctl(1): `man journalctl`
- ps(1): `man ps`
- ss(8): `man ss`
- Linux troubleshooting guides: https://www.kernel.org/doc/
