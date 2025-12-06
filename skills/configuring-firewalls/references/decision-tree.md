# Firewall Decision Tree

Visual guide for choosing the right firewall tool for your situation.


## Table of Contents

- [Quick Decision Matrix](#quick-decision-matrix)
- [Detailed Decision Flow](#detailed-decision-flow)
- [Feature Comparison](#feature-comparison)
- [Use Case Recommendations](#use-case-recommendations)
  - [Simple Web Server](#simple-web-server)
  - [High-Performance Server](#high-performance-server)
  - [Database Server](#database-server)
  - [Enterprise Multi-Server](#enterprise-multi-server)
  - [Kubernetes Cluster](#kubernetes-cluster)
  - [Legacy System](#legacy-system)
- [When to Use Multiple Layers](#when-to-use-multiple-layers)
- [Migration Path](#migration-path)
- [Quick Reference Commands](#quick-reference-commands)
  - [Check What's Running](#check-whats-running)
- [Decision Factors Summary](#decision-factors-summary)

## Quick Decision Matrix

| Context | Recommended Tool | Alternative |
|---------|-----------------|-------------|
| **Ubuntu/Debian server** | UFW | nftables |
| **RHEL/CentOS/Fedora** | firewalld | nftables |
| **Modern Linux (kernel 4.14+)** | nftables | UFW/firewalld |
| **Legacy Linux (kernel < 4.14)** | iptables | - |
| **AWS EC2 instances** | Security Groups | + host firewall (UFW/nftables) |
| **GCP Compute Engine** | VPC Firewall Rules | + host firewall |
| **Azure VMs** | Network Security Groups | + host firewall |
| **Kubernetes pods** | NetworkPolicies | - |
| **High performance needs** | nftables | iptables |

## Detailed Decision Flow

```
START: Need to configure firewall

│
├─── Running in Cloud?
│    │
│    ├─ YES → Which cloud provider?
│    │   ├─ AWS → Use Security Groups (primary)
│    │   │        + NACLs (secondary, subnet-level)
│    │   │        + Host firewall (defense-in-depth)
│    │   │
│    │   ├─ GCP → Use VPC Firewall Rules
│    │   │        + Host firewall (defense-in-depth)
│    │   │
│    │   └─ Azure → Use Network Security Groups
│    │             + Host firewall (defense-in-depth)
│    │
│    └─ NO → Continue to host-based firewalls
│
├─── Operating System?
│    │
│    ├─ Ubuntu/Debian
│    │   ├─ Simple requirements → UFW ✓ (recommended)
│    │   ├─ Advanced control → nftables
│    │   └─ Legacy system → iptables
│    │
│    ├─ RHEL/CentOS/Fedora
│    │   ├─ Standard setup → firewalld ✓ (default)
│    │   ├─ Advanced control → nftables
│    │   └─ Legacy (RHEL 6) → iptables
│    │
│    ├─ Modern Linux (kernel 4.14+)
│    │   ├─ Performance critical → nftables ✓
│    │   ├─ Simplicity preferred → UFW
│    │   └─ Existing scripts → iptables (migrate later)
│    │
│    └─ Old Linux (kernel < 4.14)
│        └─ Only option → iptables
│
├─── Kubernetes Environment?
│    │
│    ├─ YES → Check CNI plugin
│    │   ├─ Calico, Cilium, Weave → NetworkPolicies ✓
│    │   └─ Flannel → No NetworkPolicy support (upgrade CNI)
│    │
│    └─ NO → Continue to other considerations
│
├─── Performance Requirements?
│    │
│    ├─ High throughput (>100k pps) → nftables (O(log n))
│    ├─ Standard workload → Any tool acceptable
│    └─ Low resource system → UFW or nftables
│
├─── Stateful or Stateless?
│    │
│    ├─ Stateful (recommended for most)
│    │   → Security Groups, UFW, nftables default, iptables with conntrack
│    │
│    └─ Stateless (specialized needs)
│        → Network ACLs, custom nftables/iptables rules
│
└─── Multiple Layers Needed?
     │
     ├─ YES → Defense-in-Depth
     │   ├─ Cloud: Security Groups + NACLs
     │   ├─ Host: UFW/nftables + fail2ban
     │   └─ Container: NetworkPolicies
     │
     └─ NO → Choose most appropriate single layer
```

## Feature Comparison

| Feature | UFW | nftables | iptables | firewalld | Security Groups | NetworkPolicies |
|---------|-----|----------|----------|-----------|----------------|-----------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Performance** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Flexibility** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **IPv6 Support** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Stateful** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **NAT Support** | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Dynamic Updates** | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ |
| **GUI Available** | ❌ | ❌ | ❌ | ✅ | ✅ (Console) | ❌ |

## Use Case Recommendations

### Simple Web Server
**Recommendation:** UFW
- Easy to configure
- Sufficient for most web servers
- Good defaults

### High-Performance Server
**Recommendation:** nftables
- O(log n) performance
- Efficient rule processing
- Modern kernel features

### Database Server
**Recommendation:** UFW or nftables
- UFW: Simple IP/port restrictions
- nftables: Advanced egress filtering

### Enterprise Multi-Server
**Recommendation:** Infrastructure as Code (Terraform) + host firewall
- Cloud: Security Groups/NSGs via Terraform
- Host: Ansible-managed UFW/nftables

### Kubernetes Cluster
**Recommendation:** NetworkPolicies + node firewalls
- NetworkPolicies: Pod-to-pod control
- UFW/nftables on nodes: External access control

### Legacy System
**Recommendation:** iptables
- Stick with existing tool
- Plan migration to nftables

## When to Use Multiple Layers

**Defense-in-Depth Strategy:**

```
┌─────────────────────────────────────┐
│  Cloud Network ACLs (Layer 1)       │  ← Subnet-wide policies
│  ├─ Deny known malicious IPs        │
│  └─ Enforce ephemeral port policies │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Cloud Security Groups (Layer 2)    │  ← Instance-specific
│  ├─ Allow required services         │
│  └─ Reference-based rules           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Host Firewall (Layer 3)            │  ← Fine-grained control
│  ├─ UFW/nftables rules              │
│  ├─ fail2ban integration            │
│  └─ Application-specific ports      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Container NetworkPolicies (Layer 4)│  ← Pod isolation
│  ├─ Default deny                    │
│  └─ Explicit allow rules            │
└─────────────────────────────────────┘
```

**Use Multiple Layers When:**
- High security requirements (PCI-DSS, HIPAA)
- Public-facing services
- Multi-tenant environments
- Zero-trust architecture

**Single Layer Sufficient When:**
- Internal development environments
- Trusted network zones
- Resource-constrained systems

## Migration Path

**Current State → Recommended State:**

```
iptables (legacy)
    └─→ nftables (modern, better performance)

No firewall
    └─→ UFW (quick hardening) or nftables (production)

Cloud only (Security Groups)
    └─→ + Host firewall (defense-in-depth)

No NetworkPolicies (K8s)
    └─→ NetworkPolicies (pod isolation)
```

## Quick Reference Commands

### Check What's Running

```bash
# UFW
sudo ufw status

# nftables
sudo nft list ruleset
sudo systemctl status nftables

# iptables
sudo iptables -L -v -n
sudo systemctl status iptables

# firewalld
sudo firewall-cmd --state
sudo systemctl status firewalld

# AWS
aws ec2 describe-security-groups

# Kubernetes
kubectl get networkpolicies -A
```

## Decision Factors Summary

**Choose UFW if:**
- Ubuntu/Debian server
- Simple requirements
- Quick setup needed
- Prefer simplicity over advanced features

**Choose nftables if:**
- Modern Linux (kernel 4.14+)
- Need high performance
- Complex rule requirements
- Want unified IPv4/IPv6/NAT syntax

**Choose firewalld if:**
- RHEL/CentOS/Fedora
- Zone-based management needed
- Dynamic updates required
- GUI management desired

**Choose iptables if:**
- Legacy system (kernel < 4.14)
- Existing automation
- Migration not yet feasible

**Use Cloud Firewalls if:**
- Running in AWS/GCP/Azure
- Need centralized management
- Infrastructure as Code approach
- Multi-account/multi-VPC setup

**Use NetworkPolicies if:**
- Kubernetes environment
- CNI plugin supports it
- Need pod-level isolation
- Implementing zero-trust
