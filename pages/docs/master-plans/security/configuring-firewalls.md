---
sidebar_position: 6
title: Configuring Firewalls
description: Master plan for firewall configuration including iptables, cloud security groups, network policies, and defense patterns
tags: [master-plan, security, firewalls, iptables, security-groups]
---

# Configuring Firewalls

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Firewalls are the first line of network defense. This skill covers iptables, firewalld, cloud security groups (AWS, GCP, Azure), Kubernetes network policies, and defense-in-depth firewall patterns.

## Scope

This skill teaches:

- **Host-Based Firewalls** - iptables, firewalld, ufw (Ubuntu)
- **Cloud Security Groups** - AWS Security Groups, Azure NSGs, GCP Firewall Rules
- **Kubernetes Network Policies** - Pod-to-pod traffic control
- **Firewall Patterns** - Default deny, DMZ, bastion hosts
- **Stateful vs Stateless** - Connection tracking, performance trade-offs
- **WAF (Web Application Firewall)** - Application-layer protection

## Key Components

### Host-Based Firewalls

**iptables (Legacy, Still Widely Used):**
```bash
# Default deny incoming
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow established connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow SSH (port 22)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT

# Save rules
iptables-save > /etc/iptables/rules.v4
```

**firewalld (Modern, RHEL/CentOS/Fedora):**
```bash
# Add service
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https

# Add custom port
firewall-cmd --permanent --add-port=8080/tcp

# Reload
firewall-cmd --reload

# List rules
firewall-cmd --list-all
```

**ufw (Ubuntu/Debian):**
```bash
# Enable firewall
ufw enable

# Allow services
ufw allow ssh
ufw allow http
ufw allow https

# Allow specific port
ufw allow 8080/tcp

# Status
ufw status
```

### Cloud Security Groups

**AWS Security Groups:**
```yaml
# Terraform example
resource "aws_security_group" "web" {
  name = "web-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

**Azure Network Security Groups (NSGs):**
```yaml
resource "azurerm_network_security_group" "web" {
  name                = "web-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "HTTP"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}
```

**GCP Firewall Rules:**
```yaml
resource "google_compute_firewall" "web" {
  name    = "web-firewall"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["web-server"]
}
```

### Kubernetes Network Policies

**Default Deny All Traffic:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

**Allow Specific Traffic:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-allow-frontend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
```

## Decision Framework

**Which Firewall Type?**

```
Cloud-based infrastructure?
  YES → Cloud Security Groups (AWS SG, Azure NSG, GCP FW)
        + Host-based firewall (defense in depth)

Kubernetes workloads?
  YES → Network Policies (default deny)
        + Cloud Security Groups (node protection)

On-premises / VMs?
  YES → Host-based firewall (iptables/firewalld/ufw)
        + Network firewall (physical/virtual appliance)

Web application?
  YES → WAF (CloudFlare, AWS WAF, Azure Front Door)
        + Security Groups + Host firewall
```

**Default Deny vs Default Allow?**

```
Production environment?
  YES → **Default Deny** (explicit allow rules)
        Most secure, requires planning

Development environment?
  MAYBE → Default Allow (easier, less secure)
           Only if isolated network

Compliance required (PCI-DSS, HIPAA)?
  YES → **Default Deny** (mandatory)
```

## Tool Recommendations

### Host-Based

**Linux:**
- iptables (legacy, universal)
- nftables (modern replacement)
- firewalld (RHEL/CentOS/Fedora)
- ufw (Ubuntu/Debian)

**Configuration Management:**
- Ansible firewall module
- Puppet firewall module
- Chef iptables cookbook

### Cloud-Based

**AWS:**
- Security Groups (stateful)
- Network ACLs (stateless)
- AWS Network Firewall (advanced)
- AWS WAF (web application firewall)

**Azure:**
- Network Security Groups (NSGs)
- Azure Firewall (managed)
- Azure Front Door + WAF

**GCP:**
- VPC Firewall Rules
- Cloud Armor (WAF)
- Cloud IDS (intrusion detection)

### Kubernetes

**Network Policies:**
- Calico (most features)
- Cilium (eBPF-based)
- Weave Net
- Canal (Calico + Flannel)

**Web Application Firewalls:**
- CloudFlare (CDN + WAF)
- AWS WAF
- Azure Front Door + WAF
- ModSecurity (open source)

## Integration Points

**With Other Skills:**
- `network-architecture` - Firewall placement in network topology
- `security-architecture` - Firewall as preventive security control
- `kubernetes-operations` - Network policies for pod security
- `infrastructure-as-code` - Automate firewall rules (Terraform)
- `compliance-frameworks` - Firewall configuration for compliance

**Defense in Depth Example:**
```
Internet → WAF → Cloud FW → Security Group → Host FW → App
    │       │        │            │             │       │
    ▼       ▼        ▼            ▼             ▼       ▼
  Layer 7  Cloud  Network      Instance     Process  Code
  (HTTP)   edge   (VPC)        firewall     firewall  logic
```

## Learn More

- [Full Master Plan (init.md)](https://github.com/ancoleman/ai-design-components/blob/main/skills/configuring-firewalls/init.md)
- Related: `network-architecture`, `security-architecture`, `kubernetes-operations`
