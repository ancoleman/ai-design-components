# Linux Hardening Reference

Comprehensive guide to hardening Linux operating systems using kernel parameters, SSH configuration, user management, and file system controls.

## Table of Contents

1. [Kernel Hardening (sysctl)](#kernel-hardening-sysctl)
2. [SSH Hardening](#ssh-hardening)
3. [User and Group Management](#user-and-group-management)
4. [File System Hardening](#file-system-hardening)
5. [Service Minimization](#service-minimization)
6. [SELinux/AppArmor Configuration](#selinux-apparmor-configuration)
7. [Automated Hardening](#automated-hardening)

---

## Kernel Hardening (sysctl)

Configure kernel parameters in `/etc/sysctl.d/99-hardening.conf`:

```bash
# Network Security
# ----------------

# Disable IP forwarding (unless this is a router)
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0

# Ignore ICMP redirects (prevents MITM attacks)
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0

# Disable sending ICMP redirects
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# Enable TCP SYN cookies (SYN flood protection)
net.ipv4.tcp_syncookies = 1

# Disable source routing (prevents IP spoofing)
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
net.ipv6.conf.default.accept_source_route = 0

# Enable reverse path filtering (anti-spoofing)
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Log suspicious packets (Martian packets)
net.ipv4.conf.all.log_martians = 1
net.ipv4.conf.default.log_martians = 1

# Ignore ICMP ping requests (optional, may break monitoring)
# net.ipv4.icmp_echo_ignore_all = 1

# Ignore broadcast ICMP requests
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Kernel Security
# ---------------

# Enable Address Space Layout Randomization (ASLR)
kernel.randomize_va_space = 2

# Restrict kernel pointer exposure
kernel.kptr_restrict = 2

# Restrict dmesg access to root only
kernel.dmesg_restrict = 1

# Restrict access to kernel logs
kernel.dmesg_restrict = 1

# Enable ExecShield (if available)
kernel.exec-shield = 1

# Restrict ptrace (prevents debugging of other processes)
# 0 = classic ptrace, 1 = restricted, 2 = admin only, 3 = no ptrace
kernel.yama.ptrace_scope = 2

# Restrict core dumps
fs.suid_dumpable = 0

# File System Security
# --------------------

# Increase inotify limits for monitoring
fs.inotify.max_user_watches = 524288

# Protect hard links (prevents privilege escalation)
fs.protected_hardlinks = 1

# Protect symbolic links (prevents symlink attacks)
fs.protected_symlinks = 1

# Prevent FIFO attacks
fs.protected_fifos = 2

# Prevent regular file attacks
fs.protected_regular = 2
```

**Apply sysctl settings:**
```bash
# Load settings
sysctl --system

# Verify specific setting
sysctl kernel.randomize_va_space
```

---

## SSH Hardening

Configure SSH in `/etc/ssh/sshd_config.d/hardening.conf`:

```bash
# Authentication
# --------------

# Disable root login
PermitRootLogin no

# Disable password authentication (use keys only)
PasswordAuthentication no
PermitEmptyPasswords no

# Disable challenge-response authentication
ChallengeResponseAuthentication no

# Disable Kerberos and GSSAPI
KerberosAuthentication no
GSSAPIAuthentication no

# Enable public key authentication
PubkeyAuthentication yes

# Limit authentication attempts
MaxAuthTries 3
MaxSessions 2

# Set login grace time (time to complete authentication)
LoginGraceTime 30

# Protocol and Encryption
# -----------------------

# Use only SSH Protocol 2
Protocol 2

# Specify strong key exchange algorithms
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512

# Specify strong ciphers
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr

# Specify strong MACs
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256

# Access Control
# --------------

# Limit users and groups
AllowUsers deploy admin
# OR
AllowGroups ssh-users

# Deny specific users
DenyUsers root guest

# Session Security
# ----------------

# Disable X11 forwarding
X11Forwarding no

# Disable TCP forwarding
AllowTcpForwarding no

# Disable agent forwarding
AllowAgentForwarding no

# Disable SFTP subsystem (if not needed)
# Subsystem sftp /usr/lib/openssh/sftp-server

# Set idle timeout (5 minutes)
ClientAliveInterval 300
ClientAliveCountMax 2

# Limit concurrent unauthenticated connections
MaxStartups 10:30:60

# Banner and Logging
# ------------------

# Display legal banner
Banner /etc/issue.net

# Logging level
LogLevel VERBOSE

# Use privilege separation
UsePrivilegeSeparation sandbox

# Disable host-based authentication
HostbasedAuthentication no
IgnoreRhosts yes
```

**Restart SSH after changes:**
```bash
# Test configuration first
sshd -t

# Restart SSH service
systemctl restart sshd

# Verify SSH is running
systemctl status sshd
```

**Generate strong SSH keys:**
```bash
# ED25519 (recommended)
ssh-keygen -t ed25519 -a 100 -C "user@host"

# RSA 4096-bit (if ED25519 not supported)
ssh-keygen -t rsa -b 4096 -a 100 -C "user@host"
```

---

## User and Group Management

### Password Policies

Configure in `/etc/login.defs`:

```bash
# Password aging
PASS_MAX_DAYS 90        # Maximum password age
PASS_MIN_DAYS 7         # Minimum days between password changes
PASS_MIN_LEN 14         # Minimum password length
PASS_WARN_AGE 14        # Days warning before password expires

# User ID ranges
UID_MIN 1000
UID_MAX 60000
GID_MIN 1000
GID_MAX 60000

# Home directory permissions
UMASK 027               # Default umask for new files

# Login retry and timeout
LOGIN_RETRIES 3
LOGIN_TIMEOUT 60

# Enable SHA512 password hashing
ENCRYPT_METHOD SHA512
```

### PAM Password Quality

Configure in `/etc/security/pwquality.conf`:

```bash
# Minimum password length
minlen = 14

# Require at least one lowercase character
lcredit = -1

# Require at least one uppercase character
ucredit = -1

# Require at least one digit
dcredit = -1

# Require at least one special character
ocredit = -1

# Maximum consecutive characters
maxrepeat = 3

# Check against dictionary
dictcheck = 1

# Enforce for root
enforce_for_root
```

### Lock System Accounts

System accounts should not allow interactive login:

```bash
#!/bin/bash
# Lock all system accounts

SYSTEM_ACCOUNTS=(
  bin daemon adm lp sync shutdown halt mail news uucp operator
  games gopher ftp nobody systemd-network systemd-resolve
)

for user in "${SYSTEM_ACCOUNTS[@]}"; do
  # Lock password
  passwd -l "$user" 2>/dev/null

  # Set nologin shell
  usermod -s /sbin/nologin "$user" 2>/dev/null
done
```

### Sudo Hardening

Configure in `/etc/sudoers.d/hardening`:

```bash
# Require password for sudo
Defaults timestamp_timeout=5

# Log all sudo commands
Defaults log_output
Defaults logfile="/var/log/sudo.log"

# Use secure path
Defaults secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Require TTY
Defaults requiretty

# Disable root login via su
# auth required pam_wheel.so use_uid
```

### Set Default Umask

Create `/etc/profile.d/umask.sh`:

```bash
# Set restrictive umask
umask 027

# For root
if [ $UID -eq 0 ]; then
  umask 022
fi
```

---

## File System Hardening

### Secure Mount Options

Configure in `/etc/fstab`:

```bash
# /tmp with noexec, nosuid, nodev
tmpfs /tmp tmpfs defaults,noexec,nosuid,nodev,size=2G 0 0

# /var/tmp bind mount to /tmp
/tmp /var/tmp none bind 0 0

# /home with nosuid, nodev
/dev/mapper/vg-home /home ext4 defaults,nosuid,nodev 0 2

# /var with nosuid, nodev (if separate partition)
/dev/mapper/vg-var /var ext4 defaults,nosuid,nodev 0 2

# /boot with nodev, nosuid, noexec (after boot complete)
/dev/sda1 /boot ext4 defaults,nodev,nosuid,noexec 0 2

# Shared memory with noexec, nosuid, nodev
tmpfs /dev/shm tmpfs defaults,noexec,nosuid,nodev,size=1G 0 0
```

**Mount options explained:**
- `noexec`: Prevent execution of binaries
- `nosuid`: Ignore SUID/SGID bits
- `nodev`: Prevent device files
- `ro`: Read-only (for specific use cases)

**Apply mount options:**
```bash
# Remount /tmp with new options
mount -o remount /tmp

# Verify mount options
mount | grep "/tmp"
```

### File Permissions

Set secure permissions on critical files:

```bash
#!/bin/bash
# Set secure file permissions

# SSH configuration
chmod 600 /etc/ssh/sshd_config
chmod 600 /etc/ssh/sshd_config.d/*
chown root:root /etc/ssh/sshd_config

# Shadow files
chmod 600 /etc/shadow
chmod 600 /etc/gshadow
chown root:root /etc/shadow /etc/gshadow

# Cron directories
chmod 600 /etc/crontab
chmod 700 /etc/cron.d
chmod 700 /etc/cron.daily
chmod 700 /etc/cron.hourly
chmod 700 /etc/cron.monthly
chmod 700 /etc/cron.weekly

# Grub configuration
chmod 600 /boot/grub/grub.cfg
chown root:root /boot/grub/grub.cfg

# System logs
chmod 640 /var/log/wtmp
chmod 640 /var/log/btmp
chown root:utmp /var/log/wtmp /var/log/btmp
```

### Disable Core Dumps

Prevent core dumps from containing sensitive information:

```bash
# In /etc/security/limits.conf
* hard core 0

# In /etc/sysctl.d/99-hardening.conf
fs.suid_dumpable = 0

# Disable core dumps for systemd
mkdir -p /etc/systemd/coredump.conf.d/
cat > /etc/systemd/coredump.conf.d/disable.conf <<EOF
[Coredump]
Storage=none
EOF
```

---

## Service Minimization

Disable unnecessary services to reduce attack surface:

```bash
#!/bin/bash
# Disable unnecessary services

SERVICES_TO_DISABLE=(
  bluetooth.service
  cups.service
  cups-browsed.service
  avahi-daemon.service
  ModemManager.service
  wpa_supplicant.service
  iscsid.service
  rpcbind.service
  nfs-client.target
)

for service in "${SERVICES_TO_DISABLE[@]}"; do
  if systemctl is-enabled "$service" 2>/dev/null | grep -q enabled; then
    echo "Disabling $service"
    systemctl disable "$service"
    systemctl stop "$service"
  fi
done

# List enabled services
systemctl list-unit-files --state=enabled --no-pager
```

**Services to keep enabled:**
- `sshd.service` (if remote access needed)
- `systemd-*` (system services)
- `networking.service` / `NetworkManager.service`
- `cron.service` / `cronie.service`
- `rsyslog.service` / `journald`

---

## SELinux/AppArmor Configuration

### SELinux (Red Hat, CentOS, Fedora)

**Enable SELinux:**
```bash
# Check SELinux status
sestatus

# Set enforcing mode in /etc/selinux/config
SELINUX=enforcing
SELINUXTYPE=targeted

# Set enforcing mode immediately
setenforce 1

# Verify
getenforce
```

**Common SELinux operations:**
```bash
# Check context of file
ls -Z /path/to/file

# Restore default context
restorecon -Rv /path/to/directory

# Check SELinux denials
ausearch -m avc -ts recent

# Generate policy from denials
audit2allow -a -M mymodule
semodule -i mymodule.pp

# List boolean settings
getsebool -a

# Set boolean
setsebool -P httpd_can_network_connect on
```

### AppArmor (Ubuntu, Debian, SUSE)

**Enable AppArmor:**
```bash
# Check AppArmor status
aa-status

# Enable AppArmor at boot
systemctl enable apparmor

# Start AppArmor
systemctl start apparmor

# Verify
aa-enabled
```

**Common AppArmor operations:**
```bash
# Put profile in complain mode (log only)
aa-complain /etc/apparmor.d/usr.bin.firefox

# Put profile in enforce mode
aa-enforce /etc/apparmor.d/usr.bin.firefox

# Reload all profiles
systemctl reload apparmor

# Generate profile from logs
aa-logprof

# Edit profile
aa-genprof /usr/bin/myapp
```

---

## Automated Hardening

### Using Ansible

```yaml
# playbook/harden-linux.yml
---
- name: Harden Linux System
  hosts: all
  become: yes
  tasks:
    - name: Apply sysctl hardening
      sysctl:
        name: "{{ item.name }}"
        value: "{{ item.value }}"
        state: present
        reload: yes
      loop:
        - { name: 'kernel.randomize_va_space', value: '2' }
        - { name: 'net.ipv4.ip_forward', value: '0' }
        - { name: 'net.ipv4.conf.all.accept_redirects', value: '0' }
        - { name: 'net.ipv4.tcp_syncookies', value: '1' }

    - name: Harden SSH configuration
      lineinfile:
        path: /etc/ssh/sshd_config.d/hardening.conf
        line: "{{ item }}"
        create: yes
      loop:
        - "PermitRootLogin no"
        - "PasswordAuthentication no"
        - "X11Forwarding no"
        - "MaxAuthTries 3"
      notify: restart sshd

    - name: Disable unnecessary services
      systemd:
        name: "{{ item }}"
        state: stopped
        enabled: no
      loop:
        - bluetooth.service
        - cups.service
        - avahi-daemon.service
      ignore_errors: yes

  handlers:
    - name: restart sshd
      systemd:
        name: sshd
        state: restarted
```

### Verification Script

```bash
#!/bin/bash
# verify-hardening.sh

echo "=== Linux Hardening Verification ==="

# Check sysctl settings
echo -e "\n[Kernel Parameters]"
sysctl kernel.randomize_va_space | grep -q "2" && echo "✓ ASLR enabled" || echo "✗ ASLR disabled"
sysctl net.ipv4.ip_forward | grep -q "0" && echo "✓ IP forwarding disabled" || echo "✗ IP forwarding enabled"
sysctl net.ipv4.tcp_syncookies | grep -q "1" && echo "✓ SYN cookies enabled" || echo "✗ SYN cookies disabled"

# Check SSH configuration
echo -e "\n[SSH Configuration]"
sshd -T | grep -q "^permitrootlogin no" && echo "✓ Root login disabled" || echo "✗ Root login enabled"
sshd -T | grep -q "^passwordauthentication no" && echo "✓ Password auth disabled" || echo "✗ Password auth enabled"
sshd -T | grep -q "^x11forwarding no" && echo "✓ X11 forwarding disabled" || echo "✗ X11 forwarding enabled"

# Check file permissions
echo -e "\n[File Permissions]"
[ "$(stat -c %a /etc/shadow)" = "600" ] && echo "✓ /etc/shadow permissions correct" || echo "✗ /etc/shadow permissions incorrect"
[ "$(stat -c %a /etc/ssh/sshd_config)" = "600" ] && echo "✓ sshd_config permissions correct" || echo "✗ sshd_config permissions incorrect"

# Check disabled services
echo -e "\n[Disabled Services]"
systemctl is-enabled bluetooth.service 2>/dev/null | grep -q disabled && echo "✓ Bluetooth disabled" || echo "✗ Bluetooth not disabled"
systemctl is-enabled cups.service 2>/dev/null | grep -q disabled && echo "✓ CUPS disabled" || echo "✗ CUPS not disabled"

# Check SELinux/AppArmor
echo -e "\n[Mandatory Access Control]"
if command -v getenforce &>/dev/null; then
  getenforce | grep -q "Enforcing" && echo "✓ SELinux enforcing" || echo "✗ SELinux not enforcing"
elif command -v aa-enabled &>/dev/null; then
  aa-enabled && echo "✓ AppArmor enabled" || echo "✗ AppArmor not enabled"
fi

echo -e "\n=== Verification Complete ==="
```

Run verification:
```bash
chmod +x verify-hardening.sh
./verify-hardening.sh
```

---

## Additional Resources

- CIS Benchmark for Linux: https://www.cisecurity.org/benchmark/distribution_independent_linux
- NIST Security Configuration Checklist: https://ncp.nist.gov/
- STIG (Security Technical Implementation Guide): https://public.cyber.mil/stigs/
- Lynis Security Auditing: https://cisofy.com/lynis/
- OpenSCAP Security Guide: https://www.open-scap.org/
