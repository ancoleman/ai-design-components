# Network Configuration Guide

Network configuration, troubleshooting, and firewall management for Linux systems.

## Table of Contents

1. [ip Command Reference](#ip-command-reference)
2. [ss Socket Statistics](#ss-socket-statistics)
3. [Network Managers](#network-managers)
4. [DNS Configuration](#dns-configuration)
5. [Firewall Configuration](#firewall-configuration)
6. [Network Troubleshooting](#network-troubleshooting)

## ip Command Reference

Modern replacement for `ifconfig`, `route`, and `arp`.

### Interface Management

```bash
# Show interfaces
ip link show
ip addr show
ip a                               # Short form

# Show specific interface
ip addr show eth0

# Bring interface up/down
sudo ip link set eth0 up
sudo ip link set eth0 down

# Add IP address
sudo ip addr add 192.168.1.100/24 dev eth0

# Delete IP address
sudo ip addr del 192.168.1.100/24 dev eth0

# Change MTU
sudo ip link set eth0 mtu 9000
```

### Routing

```bash
# Show routing table
ip route show
ip route list
ip r                               # Short form

# Show route to specific IP
ip route get 8.8.8.8

# Add route
sudo ip route add 10.0.0.0/24 via 192.168.1.1
sudo ip route add default via 192.168.1.1

# Delete route
sudo ip route del 10.0.0.0/24
sudo ip route del default

# Add route via interface
sudo ip route add 10.0.0.0/24 dev eth0
```

### Neighbor (ARP) Table

```bash
# Show ARP cache
ip neigh show
ip n

# Add static ARP entry
sudo ip neigh add 192.168.1.10 lladdr 00:11:22:33:44:55 dev eth0

# Delete ARP entry
sudo ip neigh del 192.168.1.10 dev eth0

# Flush ARP cache
sudo ip neigh flush all
```

## ss Socket Statistics

Modern replacement for `netstat`.

### Basic Usage

```bash
# All connections
ss -a

# TCP connections
ss -t

# UDP connections
ss -u

# Listening ports
ss -l

# Combine options
ss -tunap                          # TCP+UDP, numeric, all, processes
ss -tlnp                           # TCP, listening, numeric, processes
ss -ulnp                           # UDP, listening, numeric, processes
```

### Filtering

```bash
# Established connections
ss -tnp state established

# Listening ports
ss -tlnp

# Specific port
ss -tlnp | grep :80
ss -tunap '( dport = :80 )'

# Specific host
ss dst 192.168.1.100

# Show process names
ss -tp

# Show memory usage
ss -tm
```

### Common Filters

```bash
# By state
ss state established
ss state time-wait
ss state close-wait
ss state syn-sent

# By port
ss sport = :22                     # Source port 22
ss dport = :80                     # Destination port 80
ss dport \> :1024                  # Ports > 1024

# By IP
ss src 192.168.1.0/24
ss dst 10.0.0.0/8
```

## Network Managers

### netplan (Ubuntu 18.04+)

**Configuration:** `/etc/netplan/*.yaml`

**DHCP:**
```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: true
      dhcp6: false
```

**Static IP:**
```yaml
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
        search:
          - example.com
```

**Multiple IPs:**
```yaml
network:
  version: 2
  ethernets:
    eth0:
      addresses:
        - 192.168.1.100/24
        - 192.168.1.101/24
```

**Apply configuration:**
```bash
sudo netplan apply
sudo netplan try                   # Test with auto-rollback
sudo netplan --debug apply         # Verbose
```

### NetworkManager (RHEL/Fedora)

**Command-line (nmcli):**
```bash
# Show status
nmcli device status
nmcli connection show

# Show details
nmcli device show eth0
nmcli connection show "Wired connection 1"

# Configure static IP
nmcli con mod eth0 ipv4.addresses 192.168.1.100/24
nmcli con mod eth0 ipv4.gateway 192.168.1.1
nmcli con mod eth0 ipv4.dns "8.8.8.8 8.8.4.4"
nmcli con mod eth0 ipv4.method manual

# Apply changes
nmcli con up eth0

# Configure DHCP
nmcli con mod eth0 ipv4.method auto
nmcli con up eth0

# Add connection
nmcli con add type ethernet con-name eth0 ifname eth0

# Delete connection
nmcli con del "Wired connection 1"
```

**Interactive TUI:**
```bash
nmtui
```

## DNS Configuration

### systemd-resolved (Modern)

**Status:**
```bash
resolvectl status
resolvectl query example.com
resolvectl flush-caches
```

**Configuration:** `/etc/systemd/resolved.conf`
```ini
[Resolve]
DNS=8.8.8.8 8.8.4.4
FallbackDNS=1.1.1.1
Domains=example.com
```

**Apply changes:**
```bash
sudo systemctl restart systemd-resolved
```

### Traditional resolv.conf

**Configuration:** `/etc/resolv.conf`
```bash
nameserver 8.8.8.8
nameserver 8.8.4.4
search example.com local.example.com
options timeout:2 attempts:3
```

**For static configuration (prevent overwrite):**
```bash
sudo chattr +i /etc/resolv.conf    # Make immutable
sudo chattr -i /etc/resolv.conf    # Remove immutable
```

### DNS Tools

```bash
# Query DNS
dig example.com
dig @8.8.8.8 example.com           # Specific DNS server
dig +short example.com             # Brief output
dig -x 8.8.8.8                     # Reverse DNS

# nslookup
nslookup example.com
nslookup example.com 8.8.8.8

# host
host example.com
host 8.8.8.8                       # Reverse DNS
```

## Firewall Configuration

### ufw (Ubuntu)

**Basic usage:**
```bash
# Status
sudo ufw status
sudo ufw status verbose
sudo ufw status numbered           # Show rule numbers

# Enable/disable
sudo ufw enable
sudo ufw disable

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw default deny routed
```

**Allow/deny rules:**
```bash
# By port
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw deny 23/tcp

# By service name
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https

# Port ranges
sudo ufw allow 6000:6007/tcp

# Specific interface
sudo ufw allow in on eth0 to any port 22
```

**Advanced rules:**
```bash
# From specific IP
sudo ufw allow from 192.168.1.100

# From subnet
sudo ufw allow from 192.168.1.0/24

# From IP to specific port
sudo ufw allow from 192.168.1.100 to any port 22

# Delete rules
sudo ufw delete allow 80/tcp
sudo ufw delete 3                  # By rule number

# Reset firewall
sudo ufw reset
```

**Application profiles:**
```bash
# List profiles
sudo ufw app list

# Allow application
sudo ufw allow 'Nginx Full'
sudo ufw allow 'OpenSSH'

# Show app info
sudo ufw app info 'Nginx Full'
```

### firewalld (RHEL/CentOS/Fedora)

**Basic usage:**
```bash
# Status
sudo firewall-cmd --state
sudo firewall-cmd --list-all
sudo firewall-cmd --list-all-zones

# Get default zone
sudo firewall-cmd --get-default-zone
sudo firewall-cmd --get-active-zones
```

**Services:**
```bash
# List available services
firewall-cmd --get-services

# Allow service
sudo firewall-cmd --add-service=http
sudo firewall-cmd --add-service=https
sudo firewall-cmd --add-service=http --permanent

# Remove service
sudo firewall-cmd --remove-service=http
sudo firewall-cmd --remove-service=http --permanent

# Reload (apply permanent changes)
sudo firewall-cmd --reload
```

**Ports:**
```bash
# Add port
sudo firewall-cmd --add-port=8080/tcp
sudo firewall-cmd --add-port=8080/tcp --permanent

# Port range
sudo firewall-cmd --add-port=6000-6007/tcp --permanent

# Remove port
sudo firewall-cmd --remove-port=8080/tcp --permanent
```

**Sources:**
```bash
# Allow from IP/subnet
sudo firewall-cmd --zone=public --add-source=192.168.1.0/24 --permanent
sudo firewall-cmd --zone=public --add-source=192.168.1.100 --permanent

# Remove source
sudo firewall-cmd --zone=public --remove-source=192.168.1.100 --permanent
```

**Zones:**
```bash
# List zones
firewall-cmd --get-zones

# Change default zone
sudo firewall-cmd --set-default-zone=home

# Add interface to zone
sudo firewall-cmd --zone=public --add-interface=eth0 --permanent
```

**Rich rules:**
```bash
# Allow SSH from specific IP
sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.100" service name="ssh" accept' --permanent

# Block IP
sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="10.0.0.50" reject' --permanent

# Rate limiting
sudo firewall-cmd --add-rich-rule='rule service name="ssh" limit value="10/m" accept' --permanent
```

### iptables (Low-level)

**Basic usage:**
```bash
# List rules
sudo iptables -L
sudo iptables -L -n -v             # Numeric, verbose
sudo iptables -L -n --line-numbers

# Allow port
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Block IP
sudo iptables -A INPUT -s 10.0.0.50 -j DROP

# Delete rule
sudo iptables -D INPUT 3           # By line number

# Flush all rules
sudo iptables -F

# Save rules
sudo iptables-save > /etc/iptables/rules.v4
sudo netfilter-persistent save     # Ubuntu
```

## Network Troubleshooting

### Connectivity Tests

```bash
# Ping
ping -c 4 8.8.8.8                  # 4 packets
ping -c 4 google.com               # Test DNS too

# Traceroute
traceroute 8.8.8.8
traceroute -n 8.8.8.8              # Numeric (faster)
mtr 8.8.8.8                        # Combined ping/traceroute

# Port connectivity
telnet server 80
nc -zv server 80                   # netcat
curl -v telnet://server:80

# DNS lookup
dig google.com
nslookup google.com
host google.com
```

### Bandwidth Testing

```bash
# iperf3
# Server:
iperf3 -s

# Client:
iperf3 -c server_ip -t 60          # 60 second test
iperf3 -c server_ip -R             # Reverse (download)
iperf3 -c server_ip -u -b 100M     # UDP, 100 Mbps
```

### Network Statistics

```bash
# Interface statistics
ip -s link show eth0
ifconfig eth0                      # Legacy

# Error counts
netstat -i                         # Legacy
ip -s link

# Protocol statistics
netstat -s
ss -s
```

### Packet Capture

```bash
# tcpdump
sudo tcpdump -i eth0                      # All traffic
sudo tcpdump -i eth0 port 80              # HTTP
sudo tcpdump -i eth0 host 192.168.1.100   # Specific host
sudo tcpdump -i eth0 -w capture.pcap      # Save to file
sudo tcpdump -r capture.pcap              # Read from file

# More specific
sudo tcpdump -i eth0 'tcp port 80 and host 192.168.1.100'
```

### Common Issues

**No network connectivity:**
```bash
# Check interface status
ip link show eth0
# Should show "state UP"

# Check IP address
ip addr show eth0

# Check routes
ip route show

# Check DNS
cat /etc/resolv.conf
dig google.com

# Check firewall
sudo iptables -L -n -v
sudo ufw status
sudo firewall-cmd --list-all
```

**Slow network:**
```bash
# Check errors
ip -s link show eth0
# Look for RX/TX errors, drops

# Check MTU
ip link show eth0 | grep mtu

# Test bandwidth
iperf3 -c server

# Check latency
ping -c 100 server | tail -1
```

**Port already in use:**
```bash
# Find process
sudo ss -tlnp | grep :8080
sudo lsof -i :8080

# Kill process
sudo kill -9 PID
```

## Best Practices

1. **Use static IP for servers** (easier management)
2. **Document firewall rules** (know what's open)
3. **Default deny policy** (explicit allow)
4. **Test configuration changes** before applying
5. **Monitor network metrics** regularly
6. **Keep firewall rules minimal** (only necessary ports)
7. **Use fail2ban** for SSH brute-force protection

## References

- ip(8): `man ip`
- ss(8): `man ss`
- iptables(8): `man iptables`
- firewalld documentation: https://firewalld.org/
- ufw documentation: https://help.ubuntu.com/community/UFW
