# Firewall Troubleshooting Guide

Common firewall issues and solutions across UFW, nftables, iptables, and cloud security groups.


## Table of Contents

- ["I Locked Myself Out" (SSH)](#i-locked-myself-out-ssh)
  - [Symptoms](#symptoms)
  - [Solutions](#solutions)
- [Connection Timeouts](#connection-timeouts)
  - [Symptoms](#symptoms)
  - [Diagnosis Steps](#diagnosis-steps)
  - [Common Fixes](#common-fixes)
- [AWS Ephemeral Port Issues](#aws-ephemeral-port-issues)
  - [Symptoms](#symptoms)
  - [Cause](#cause)
  - [Solution](#solution)
  - [Ephemeral Port Ranges by OS](#ephemeral-port-ranges-by-os)
- [Firewall Active But Not Blocking](#firewall-active-but-not-blocking)
  - [Symptoms](#symptoms)
  - [Diagnosis](#diagnosis)
  - [Common Fixes](#common-fixes)
- [iptables and nftables Conflict](#iptables-and-nftables-conflict)
  - [Symptoms](#symptoms)
  - [Cause](#cause)
  - [Solution](#solution)
- [Kubernetes Pods Can't Communicate](#kubernetes-pods-cant-communicate)
  - [Symptoms](#symptoms)
  - [Diagnosis](#diagnosis)
  - [Common Fixes](#common-fixes)
- [Logging Not Working](#logging-not-working)
  - [Symptoms](#symptoms)
  - [Solutions](#solutions)
- [Performance Issues](#performance-issues)
  - [Symptoms](#symptoms)
  - [Diagnosis](#diagnosis)
  - [Solutions](#solutions)
- [Testing Firewall Rules](#testing-firewall-rules)
  - [External Port Scan](#external-port-scan)
  - [Internal Testing](#internal-testing)
  - [Verify Rules Applied](#verify-rules-applied)
- [Common Error Messages](#common-error-messages)
  - ["Operation not permitted"](#operation-not-permitted)
  - ["Could not process rule: No such file or directory"](#could-not-process-rule-no-such-file-or-directory)
  - ["iptables: No chain/target/match by that name"](#iptables-no-chaintargetmatch-by-that-name)
  - ["RTNETLINK answers: File exists"](#rtnetlink-answers-file-exists)
- [Debugging Checklist](#debugging-checklist)
- [Emergency Recovery](#emergency-recovery)
  - [Temporarily Disable Firewall](#temporarily-disable-firewall)
  - [Reset to Safe State](#reset-to-safe-state)
- [Getting Help](#getting-help)
  - [Useful Commands for Support](#useful-commands-for-support)
  - [Where to Ask](#where-to-ask)

## "I Locked Myself Out" (SSH)

### Symptoms
- Can't SSH to server after enabling firewall
- Connection times out or refused

### Solutions

#### Cloud (AWS/GCP/Azure)
```bash
# Use console access (serial console or Session Manager)
# AWS: EC2 Instance Connect or Systems Manager Session Manager
aws ssm start-session --target i-1234567890abcdef0

# Once connected via console:
# Check and fix firewall rules
sudo ufw status
sudo ufw allow from YOUR_IP to any port 22
sudo ufw enable
```

#### Physical/VM Access
```bash
# Access via console (IPMI, iLO, or hypervisor console)
# Disable firewall temporarily
sudo ufw disable

# Fix rules
sudo ufw allow ssh
sudo ufw enable
```

#### Prevention
```bash
# ALWAYS allow SSH before enabling
sudo ufw allow ssh
sudo ufw limit ssh  # Rate limiting
sudo ufw enable

# Test with timeout (auto-disable after 30 sec if no re-enable)
sudo ufw --force enable && sleep 30 && sudo ufw disable
# If SSH works, re-enable permanently
sudo ufw enable
```

## Connection Timeouts

### Symptoms
- Services not reachable
- Connection hangs then times out
- `telnet <ip> <port>` fails

### Diagnosis Steps

#### 1. Check if Service is Running
```bash
# List listening ports
sudo ss -tuln | grep <port>
sudo netstat -tuln | grep <port>

# Check service status
sudo systemctl status <service>

# Example: Check if Nginx is listening on 80
sudo ss -tuln | grep :80
```

#### 2. Check Firewall Rules

**UFW:**
```bash
sudo ufw status verbose

# Check if port is allowed
sudo ufw status | grep <port>
```

**nftables:**
```bash
# List all rules
sudo nft list ruleset

# Check specific table
sudo nft list table inet filter

# Check if port is accepted
sudo nft list ruleset | grep "dport <port>"
```

**iptables:**
```bash
# List rules with line numbers
sudo iptables -L INPUT -v -n --line-numbers

# Check if port is accepted
sudo iptables -L INPUT -v -n | grep <port>
```

**AWS Security Groups:**
```bash
# Describe security group
aws ec2 describe-security-groups --group-ids sg-xxxxx

# Check specific port
aws ec2 describe-security-group-rules \
  --filters Name=group-id,Values=sg-xxxxx \
  --query 'SecurityGroupRules[?FromPort==`80`]'
```

#### 3. Test Connectivity

**From local machine:**
```bash
# TCP connection test
telnet <server-ip> <port>
nc -zv <server-ip> <port>

# Port scan
nmap -Pn <server-ip> -p <port>
```

**From server (test outbound):**
```bash
# Test outbound HTTPS
curl -I https://google.com

# Test outbound to specific port
nc -zv external-server.com 443
```

### Common Fixes

**UFW - Allow port:**
```bash
sudo ufw allow <port>/tcp
sudo ufw reload
```

**nftables - Add rule:**
```bash
sudo nft add rule inet filter input tcp dport <port> accept
sudo nft list ruleset  # Verify
```

**iptables - Add rule:**
```bash
sudo iptables -A INPUT -p tcp --dport <port> -j ACCEPT
sudo netfilter-persistent save  # Persist
```

## AWS Ephemeral Port Issues

### Symptoms
- Outbound connections from EC2 fail
- Return traffic blocked
- Works with Security Groups but not NACLs

### Cause
Network ACLs are **stateless** - must explicitly allow return traffic on ephemeral ports (1024-65535).

### Solution

```hcl
# Add ephemeral ports to NACL inbound rules
resource "aws_network_acl" "example" {
  # ... other rules

  # CRITICAL: Allow ephemeral ports for return traffic
  ingress {
    rule_no    = 140
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 1024
    to_port    = 65535
  }
}
```

### Ephemeral Port Ranges by OS
- Linux: 32768-60999 (or 32768-65535)
- Windows: 49152-65535
- AWS NAT Gateway/ALB: 1024-65535

**Best Practice:** Allow 1024-65535 to cover all cases.

## Firewall Active But Not Blocking

### Symptoms
- Firewall shows as enabled
- Rules configured but traffic not blocked
- nmap shows ports open that should be closed

### Diagnosis

**UFW:**
```bash
# Check if UFW is actually active
sudo ufw status
# Should show: Status: active

# Check if rules are loaded
sudo iptables -L -v -n

# Check UFW service
sudo systemctl status ufw
```

**nftables:**
```bash
# Check if service is running
sudo systemctl status nftables

# List actual kernel rules
sudo nft list ruleset

# If empty, rules not loaded
sudo nft -f /etc/nftables.conf
```

**iptables:**
```bash
# Check if rules are loaded
sudo iptables -L -v -n

# Check if iptables service is enabled
sudo systemctl status iptables  # RHEL/CentOS
sudo systemctl status netfilter-persistent  # Debian/Ubuntu
```

### Common Fixes

**UFW - Ensure enabled:**
```bash
sudo ufw enable
sudo systemctl enable ufw
```

**nftables - Load rules:**
```bash
sudo systemctl enable nftables
sudo systemctl start nftables
sudo nft -f /etc/nftables.conf
```

**iptables - Save and persist:**
```bash
# Debian/Ubuntu
sudo netfilter-persistent save
sudo systemctl enable netfilter-persistent

# RHEL/CentOS
sudo service iptables save
sudo systemctl enable iptables
```

## iptables and nftables Conflict

### Symptoms
- Unpredictable firewall behavior
- Rules not working as expected
- Both iptables and nftables show active

### Cause
Running both iptables and nftables simultaneously causes conflicts.

### Solution

**Choose one and disable the other:**

```bash
# Option 1: Use nftables (recommended)
sudo systemctl stop iptables
sudo systemctl disable iptables
sudo iptables -F  # Flush iptables rules
sudo systemctl enable nftables
sudo systemctl start nftables

# Option 2: Use iptables
sudo systemctl stop nftables
sudo systemctl disable nftables
sudo nft flush ruleset  # Flush nftables rules
sudo systemctl enable iptables
sudo systemctl start iptables
```

## Kubernetes Pods Can't Communicate

### Symptoms
- Pod-to-pod communication blocked
- Services unreachable from pods
- curl/wget from pods times out

### Diagnosis

```bash
# Check NetworkPolicies
kubectl get networkpolicies -n <namespace>

# Describe specific policy
kubectl describe networkpolicy <name> -n <namespace>

# Check if CNI plugin supports NetworkPolicies
# Calico: yes, Flannel: no, Weave: yes, Cilium: yes

# Test without NetworkPolicies (delete temporarily)
kubectl delete networkpolicy <name> -n <namespace>
```

### Common Fixes

**1. Allow DNS:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: UDP
          port: 53
```

**2. Default deny is too restrictive:**
```bash
# Check for default deny-all policy
kubectl get networkpolicy -n <namespace> -o yaml | grep "podSelector: {}"

# If exists, must explicitly allow required traffic
```

**3. CNI plugin doesn't support NetworkPolicies:**
```bash
# Check CNI plugin
kubectl get pods -n kube-system | grep -E 'calico|flannel|weave|cilium'

# If using Flannel (no NetworkPolicy support), switch to Calico or Cilium
```

## Logging Not Working

### Symptoms
- No firewall logs appearing
- Can't debug dropped connections

### Solutions

**UFW:**
```bash
# Enable logging
sudo ufw logging on

# Set log level
sudo ufw logging medium

# View logs
sudo tail -f /var/log/ufw.log

# Or via syslog
sudo journalctl -u ufw -f
```

**nftables:**
```bash
# Ensure log rule exists
sudo nft list ruleset | grep "log"

# Add logging if missing
sudo nft add rule inet filter input log prefix "nft-drop: " limit rate 5/minute

# View logs
sudo dmesg | grep "nft-drop"
sudo journalctl -k | grep "nft-drop"
```

**iptables:**
```bash
# Add logging rule (before DROP)
sudo iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "ipt-drop: " --log-level 7

# View logs
sudo tail -f /var/log/syslog | grep "ipt-drop"
sudo dmesg | grep "ipt-drop"
```

**AWS VPC Flow Logs:**
```bash
# Check if Flow Logs enabled
aws ec2 describe-flow-logs

# Enable Flow Logs
aws ec2 create-flow-log \
  --resource-type VPC \
  --resource-ids vpc-xxxxx \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name /aws/vpc/flow-logs
```

## Performance Issues

### Symptoms
- High CPU on firewall processing
- Packet loss
- Slow network performance

### Diagnosis

```bash
# Check CPU usage
top
htop

# Check network stats
sudo iptables -L -v -n  # Check packet counters
sudo nft list ruleset   # Check rule counters

# Check kernel logs
dmesg | tail
```

### Solutions

**1. Optimize rule order (put frequently matched rules first):**
```bash
# iptables: Use -I to insert at top
sudo iptables -I INPUT -p tcp --dport 80 -j ACCEPT

# nftables: Define rules in order of frequency
```

**2. Use sets instead of multiple rules:**
```nftables
# Bad (multiple rules):
tcp dport 80 accept
tcp dport 443 accept
tcp dport 8080 accept

# Good (single rule with set):
tcp dport { 80, 443, 8080 } accept
```

**3. Limit logging:**
```bash
# Add rate limit to log rules
log prefix "dropped: " limit rate 5/minute
```

**4. Consider nftables for better performance:**
```bash
# nftables has O(log n) vs iptables O(n)
# See migration-guide.md
```

## Testing Firewall Rules

### External Port Scan

```bash
# From external machine
nmap -Pn <server-ip>

# Specific ports
nmap -Pn <server-ip> -p 22,80,443

# UDP scan
nmap -sU <server-ip>
```

### Internal Testing

```bash
# Check listening ports
sudo ss -tuln
sudo netstat -tuln

# Test local connection
telnet localhost 80
nc -zv localhost 80

# Test from specific IP (simulate)
# Not directly possible, but can test with:
sudo iptables -I INPUT 1 -s <test-ip> -j LOG --log-prefix "test: "
```

### Verify Rules Applied

```bash
# UFW
sudo ufw status verbose

# nftables
sudo nft list ruleset

# iptables
sudo iptables -L -v -n

# AWS (CLI)
aws ec2 describe-security-groups --group-ids sg-xxxxx
```

## Common Error Messages

### "Operation not permitted"
```bash
# Cause: Insufficient permissions
# Fix: Use sudo
sudo ufw allow 80
```

### "Could not process rule: No such file or directory"
```bash
# Cause: nftables kernel module not loaded
# Fix:
sudo modprobe nf_tables
```

### "iptables: No chain/target/match by that name"
```bash
# Cause: Invalid chain name or syntax
# Fix: Check syntax
sudo iptables -L  # List valid chains
```

### "RTNETLINK answers: File exists"
```bash
# Cause: Rule already exists
# Fix: Check existing rules first
sudo iptables -L -v -n
```

## Debugging Checklist

When troubleshooting firewall issues:

- [ ] Verify service is running and listening on port
- [ ] Check firewall status (active/inactive)
- [ ] List current firewall rules
- [ ] Test connectivity from external/internal
- [ ] Check logs for dropped packets
- [ ] Verify no conflicting firewalls (iptables vs nftables)
- [ ] For cloud: Check both Security Groups AND NACLs
- [ ] For Kubernetes: Check NetworkPolicies and CNI support
- [ ] Test with firewall temporarily disabled (if safe)
- [ ] Use packet tracing (nftables) or logging (all)

## Emergency Recovery

### Temporarily Disable Firewall

**CAUTION:** Only use in emergency situations with console access.

```bash
# UFW
sudo ufw disable

# nftables
sudo nft flush ruleset
sudo systemctl stop nftables

# iptables
sudo iptables -F
sudo iptables -P INPUT ACCEPT
sudo iptables -P OUTPUT ACCEPT
sudo iptables -P FORWARD ACCEPT
```

### Reset to Safe State

```bash
# UFW - Reset completely
sudo ufw reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable

# iptables - Reset
sudo iptables -F
sudo iptables -X
sudo iptables -P INPUT ACCEPT
sudo iptables -P OUTPUT ACCEPT
sudo iptables -P FORWARD ACCEPT

# nftables - Reset
sudo nft flush ruleset
sudo nft -f /etc/nftables.conf.default
```

## Getting Help

### Useful Commands for Support

```bash
# System info
uname -a
cat /etc/os-release

# Firewall status
sudo ufw status verbose
sudo nft list ruleset
sudo iptables -L -v -n

# Network interfaces
ip addr show
ip route show

# Listening ports
sudo ss -tuln

# Recent logs
sudo journalctl -u ufw -n 50
sudo dmesg | tail -50

# AWS (if cloud)
aws ec2 describe-security-groups --group-ids sg-xxxxx
aws ec2 describe-network-acls --network-acl-ids acl-xxxxx
```

### Where to Ask

- **UFW:** Ubuntu forums, Ask Ubuntu (StackExchange)
- **nftables:** netfilter mailing list, nftables wiki
- **iptables:** netfilter project, Linux forums
- **AWS:** AWS forums, Stack Overflow (tag: amazon-web-services)
- **Kubernetes:** Kubernetes Slack, Stack Overflow (tag: kubernetes)
