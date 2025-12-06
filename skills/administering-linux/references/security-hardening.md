# Security Hardening Guide

Security best practices for Linux servers including SSH, firewall, user management, and SELinux/AppArmor basics.

## Table of Contents

1. [SSH Hardening](#ssh-hardening)
2. [Firewall Best Practices](#firewall-best-practices)
3. [User and Access Control](#user-and-access-control)
4. [SELinux Basics](#selinux-basics)
5. [AppArmor Basics](#apparmor-basics)
6. [System Hardening](#system-hardening)

## SSH Hardening

### SSH Key Setup

**Generate strong SSH key:**
```bash
# Ed25519 (modern, recommended)
ssh-keygen -t ed25519 -C "user@example.com"

# RSA (broader compatibility)
ssh-keygen -t rsa -b 4096 -C "user@example.com"
```

**Copy to server:**
```bash
ssh-copy-id user@server
# Or manually:
cat ~/.ssh/id_ed25519.pub | ssh user@server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

**Set correct permissions:**
```bash
# Client
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub

# Server
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

### sshd_config Hardening

**Essential settings:** `/etc/ssh/sshd_config`
```bash
# Disable root login
PermitRootLogin no

# Key-based authentication only
PubkeyAuthentication yes
PasswordAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no

# Protocol
Protocol 2

# Login restrictions
MaxAuthTries 3
LoginGraceTime 30s
MaxSessions 10

# User/group restrictions
AllowUsers deploy admin
AllowGroups sshusers

# Disable features
X11Forwarding no
PermitTunnel no
AllowAgentForwarding no
AllowTcpForwarding no
GatewayPorts no

# Logging
SyslogFacility AUTH
LogLevel VERBOSE

# Keep connections alive
ClientAliveInterval 300
ClientAliveCountMax 2

# Disable GSSAPI (if not needed)
GSSAPIAuthentication no
```

**Apply changes:**
```bash
# Test configuration
sudo sshd -t

# Restart (keep backup session open!)
sudo systemctl restart sshd
```

### Fail2ban

**Install:**
```bash
sudo apt install fail2ban         # Ubuntu
sudo dnf install fail2ban         # RHEL/Fedora
```

**Configure:** `/etc/fail2ban/jail.local`
```ini
[DEFAULT]
# Ban for 1 hour
bantime = 3600

# Find window of 10 minutes
findtime = 600

# Ban after 3 failures
maxretry = 3

# Email notifications (optional)
destemail = admin@example.com
sendername = Fail2Ban
action = %(action_mwl)s

[sshd]
enabled = true
port = ssh,2222
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
```

**Manage fail2ban:**
```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Check status
sudo fail2ban-client status
sudo fail2ban-client status sshd

# Unban IP
sudo fail2ban-client set sshd unbanip 192.168.1.100
```

## Firewall Best Practices

### Principles

1. **Default deny** - Block everything by default
2. **Explicit allow** - Only open necessary ports
3. **Principle of least privilege** - Minimum access required
4. **Regular review** - Audit rules periodically

### Ubuntu (ufw) Hardening

```bash
# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw default deny routed

# Essential services only
sudo ufw allow 22/tcp comment 'SSH'
sudo ufw allow 80/tcp comment 'HTTP'
sudo ufw allow 443/tcp comment 'HTTPS'

# Restrict SSH to specific IPs
sudo ufw delete allow 22/tcp
sudo ufw allow from 192.168.1.0/24 to any port 22 comment 'SSH from office'

# Rate limiting (prevent brute force)
sudo ufw limit 22/tcp

# Enable
sudo ufw enable

# Logging
sudo ufw logging on
sudo ufw logging medium
```

### RHEL/CentOS (firewalld) Hardening

```bash
# Set default zone
sudo firewall-cmd --set-default-zone=drop

# Create custom zone
sudo firewall-cmd --permanent --new-zone=servers
sudo firewall-cmd --permanent --zone=servers --set-target=DROP

# Add services
sudo firewall-cmd --permanent --zone=servers --add-service=ssh
sudo firewall-cmd --permanent --zone=servers --add-service=http
sudo firewall-cmd --permanent --zone=servers --add-service=https

# Restrict SSH to specific IPs
sudo firewall-cmd --permanent --zone=servers --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" service name="ssh" accept'

# Rate limiting
sudo firewall-cmd --permanent --add-rich-rule='rule service name="ssh" limit value="10/m" accept'

# Apply
sudo firewall-cmd --reload
```

## User and Access Control

### User Management

**Create system user (for services):**
```bash
sudo useradd -r -s /bin/false -M username
# -r = system user
# -s /bin/false = no login shell
# -M = no home directory
```

**Create regular user:**
```bash
sudo useradd -m -s /bin/bash username
sudo passwd username
```

**Disable account:**
```bash
sudo usermod -L username          # Lock account
sudo usermod -s /usr/sbin/nologin username  # Disable shell
```

**Remove inactive users:**
```bash
# Find users not logged in for 90 days
lastlog -b 90

# Lock old accounts
sudo passwd -l username
```

### sudo Configuration

**Edit sudoers safely:**
```bash
sudo visudo
```

**Common configurations:**
```bash
# Full sudo access
username ALL=(ALL:ALL) ALL

# Passwordless sudo (use carefully!)
username ALL=(ALL) NOPASSWD: ALL

# Specific commands only
username ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx

# Group-based
%wheel ALL=(ALL:ALL) ALL          # RHEL/CentOS
%sudo ALL=(ALL:ALL) ALL           # Ubuntu/Debian

# Require password every time (no caching)
Defaults timestamp_timeout=0

# Log all sudo commands
Defaults logfile="/var/log/sudo.log"
Defaults log_year, log_host, log_input, log_output
```

### Password Policies

**Configure PAM:** `/etc/pam.d/common-password` (Ubuntu) or `/etc/pam.d/system-auth` (RHEL)
```bash
# Password quality requirements
password requisite pam_pwquality.so retry=3 minlen=12 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1

# Options:
# retry=3 - 3 attempts
# minlen=12 - 12 characters minimum
# ucredit=-1 - require 1 uppercase
# lcredit=-1 - require 1 lowercase
# dcredit=-1 - require 1 digit
# ocredit=-1 - require 1 special character
```

**Password aging:** `/etc/login.defs`
```bash
PASS_MAX_DAYS 90                  # Max 90 days
PASS_MIN_DAYS 1                   # Min 1 day between changes
PASS_WARN_AGE 7                   # Warn 7 days before expiry
```

**Set for existing user:**
```bash
sudo chage -M 90 -m 1 -W 7 username

# View settings
sudo chage -l username
```

## SELinux Basics

### SELinux Modes

**Check status:**
```bash
getenforce
sestatus
```

**Modes:**
- **Enforcing** - SELinux actively enforces policy
- **Permissive** - SELinux logs violations but doesn't enforce
- **Disabled** - SELinux completely disabled

**Change mode:**
```bash
# Temporary
sudo setenforce 0                 # Permissive
sudo setenforce 1                 # Enforcing

# Permanent: /etc/selinux/config
SELINUX=enforcing
SELINUX=permissive
SELINUX=disabled
```

### SELinux Contexts

**View contexts:**
```bash
ls -Z /var/www/html
ps auxZ                           # Process contexts
```

**Common contexts:**
- `httpd_sys_content_t` - Web server readable content
- `httpd_sys_rw_content_t` - Web server writable content
- `httpd_sys_script_exec_t` - Web server executable scripts

**Change context:**
```bash
# Set specific context
sudo chcon -t httpd_sys_content_t /var/www/html/index.html

# Restore default contexts
sudo restorecon -Rv /var/www/html

# Make permanent (file context rules)
sudo semanage fcontext -a -t httpd_sys_content_t "/var/www/html(/.*)?"
sudo restorecon -Rv /var/www/html
```

### SELinux Troubleshooting

**Check denials:**
```bash
# Recent denials
sudo ausearch -m avc -ts recent

# All denials
sudo grep avc /var/log/audit/audit.log

# Human-readable
sudo sealert -a /var/log/audit/audit.log
```

**Create policy module:**
```bash
# Generate policy from denials
sudo audit2allow -a -M mypolicy

# Install policy
sudo semodule -i mypolicy.pp

# View installed modules
sudo semodule -l
```

**Booleans:**
```bash
# List booleans
getsebool -a
getsebool -a | grep httpd

# Set boolean
sudo setsebool -P httpd_can_network_connect on
# -P = permanent
```

## AppArmor Basics

### AppArmor Status

**Check status:**
```bash
sudo aa-status
```

**Modes:**
- **Enforce** - Policy is enforced
- **Complain** - Policy violations logged but not blocked
- **Unconfined** - No policy applied

### Manage Profiles

**Profile locations:** `/etc/apparmor.d/`

**Set mode:**
```bash
# Complain mode (testing)
sudo aa-complain /usr/sbin/nginx

# Enforce mode
sudo aa-enforce /usr/sbin/nginx

# Disable profile
sudo ln -s /etc/apparmor.d/usr.sbin.nginx /etc/apparmor.d/disable/
sudo apparmor_parser -R /etc/apparmor.d/usr.sbin.nginx

# Enable profile
sudo rm /etc/apparmor.d/disable/usr.sbin.nginx
sudo apparmor_parser -r /etc/apparmor.d/usr.sbin.nginx
```

### Troubleshooting

**Check denials:**
```bash
# System logs
sudo dmesg | grep -i apparmor
sudo journalctl | grep -i apparmor

# Audit log
sudo grep DENIED /var/log/syslog
sudo grep DENIED /var/log/audit/audit.log
```

**Update profile:**
```bash
# Edit profile
sudo nano /etc/apparmor.d/usr.sbin.nginx

# Reload profile
sudo apparmor_parser -r /etc/apparmor.d/usr.sbin.nginx
```

## System Hardening

### Disable Unnecessary Services

```bash
# List all services
systemctl list-unit-files --type=service

# Disable service
sudo systemctl disable service_name
sudo systemctl mask service_name  # Prevent accidental start
```

**Common services to disable (if not needed):**
- `bluetooth.service`
- `cups.service` (printing)
- `avahi-daemon.service` (zeroconf)

### Kernel Hardening

**sysctl settings:** `/etc/sysctl.d/99-security.conf`
```bash
# IP forwarding (disable if not router)
net.ipv4.ip_forward = 0

# Ignore ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0

# Ignore source routed packets
net.ipv4.conf.all.accept_source_route = 0

# Ignore broadcast pings
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Ignore bogus ICMP errors
net.ipv4.icmp_ignore_bogus_error_responses = 1

# Enable reverse path filtering (anti-spoofing)
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Log martians
net.ipv4.conf.all.log_martians = 1

# SYN flood protection
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_synack_retries = 2

# Disable IPv6 (if not used)
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
```

**Apply:**
```bash
sudo sysctl -p /etc/sysctl.d/99-security.conf
```

### Automatic Updates

**Ubuntu/Debian:**
```bash
sudo apt install unattended-upgrades

# Configure: /etc/apt/apt.conf.d/50unattended-upgrades
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
};

# Enable
sudo dpkg-reconfigure -plow unattended-upgrades
```

**RHEL/CentOS/Fedora:**
```bash
sudo dnf install dnf-automatic

# Configure: /etc/dnf/automatic.conf
[commands]
upgrade_type = security
apply_updates = yes

# Enable
sudo systemctl enable --now dnf-automatic.timer
```

### File Integrity Monitoring

**AIDE (Advanced Intrusion Detection Environment):**
```bash
# Install
sudo apt install aide              # Ubuntu
sudo dnf install aide              # RHEL/Fedora

# Initialize database
sudo aideinit

# Check integrity
sudo aide --check

# Update database
sudo aide --update
```

### Rootkit Detection

**rkhunter:**
```bash
# Install
sudo apt install rkhunter

# Update database
sudo rkhunter --update

# Scan system
sudo rkhunter --check

# Schedule daily scan
sudo systemctl enable rkhunter.timer
```

### Audit Logging

**auditd:**
```bash
# Install
sudo apt install auditd

# Status
sudo systemctl status auditd

# View logs
sudo ausearch -m USER_LOGIN
sudo ausearch -m EXECVE            # Command execution

# Add rule
sudo auditctl -w /etc/passwd -p wa -k passwd_changes
# -w = watch file
# -p wa = write, attribute change
# -k = key for searching
```

## Security Checklist

- [ ] SSH key-based authentication only
- [ ] Root login disabled
- [ ] Firewall configured with default deny
- [ ] Fail2ban installed and configured
- [ ] Strong password policies
- [ ] Automatic security updates enabled
- [ ] Unnecessary services disabled
- [ ] SELinux/AppArmor enabled
- [ ] Regular system updates
- [ ] Log monitoring configured
- [ ] User accounts reviewed regularly
- [ ] sudo access limited
- [ ] File integrity monitoring
- [ ] Kernel hardening applied

## Best Practices

1. **Defense in depth** - Multiple security layers
2. **Principle of least privilege** - Minimal access
3. **Regular updates** - Apply security patches promptly
4. **Monitor logs** - Watch for suspicious activity
5. **Backup regularly** - Before making changes
6. **Test changes** - Staging environment first
7. **Document security policies** - Know what's configured
8. **Regular audits** - Review security posture

## References

- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks/
- NIST Guidelines: https://csrc.nist.gov/
- SELinux documentation: https://selinuxproject.org/
- AppArmor documentation: https://wiki.ubuntu.com/AppArmor
