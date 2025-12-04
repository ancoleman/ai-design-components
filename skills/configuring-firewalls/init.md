# Configuring Firewalls - Skill Master Plan

**Skill Level:** Low Level (2,000-5,000 tokens, 300-500 lines init.md)
**Status:** Master Plan Complete - Ready for SKILL.md Implementation
**Created:** December 3, 2025
**Research Date:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Firewall Taxonomy](#firewall-taxonomy)
5. [Decision Framework](#decision-framework)
6. [Implementation Patterns](#implementation-patterns)
7. [Cloud Security Groups](#cloud-security-groups)
8. [Common Patterns](#common-patterns)
9. [Tool Recommendations](#tool-recommendations)
10. [Skill Structure Design](#skill-structure-design)
11. [Integration Points](#integration-points)
12. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Market Context (December 2025)

**Industry Shift: iptables → nftables**
- nftables is now the recommended standard for Linux firewalls
- Most modern distributions (Ubuntu 22.04+, Debian 11+, RHEL 8+) default to nftables
- iptables still relevant for legacy systems and specific use cases
- UFW provides user-friendly abstraction over both

**Cloud-Native Security**
- Security Groups and NACLs are foundational AWS skills
- Multi-cloud strategies require understanding GCP firewall rules and Azure NSGs
- Infrastructure as Code (Terraform, CloudFormation) is standard practice
- Defense-in-depth combines host-based and network-based firewalls

**Key Insight:** Firewall configuration is a foundational DevOps skill that bridges traditional sysadmin work with modern cloud-native architectures.

### Why This Skill Matters

**Universal Need:**
- Every server needs firewall protection
- Misconfiguration is a top security vulnerability
- Compliance requirements (PCI-DSS, SOC 2, HIPAA) mandate firewall controls
- Zero-trust architectures depend on granular firewall rules

**Common Pain Points:**
- Accidentally locking yourself out (especially SSH)
- Forgetting to enable firewall after configuration
- Stateful vs stateless confusion
- Ephemeral port ranges in cloud environments
- Managing rules across multiple instances

**Success Metrics:**
- Zero lockouts during configuration
- Minimal exposed ports (principle of least privilege)
- Documented and version-controlled rules
- Passing external security scans (nmap)

---

## Skill Purpose and Scope

### Purpose

Guide engineers through configuring firewalls across host-based (iptables, nftables, UFW), cloud-based (AWS Security Groups, NACLs), and container-based (Kubernetes NetworkPolicies) environments with practical rule examples and safety patterns.

### When to Use This Skill

**Trigger Phrases:**
- "Configure firewall for [server/service]"
- "Set up security groups for [AWS resource]"
- "Allow port [X] through firewall"
- "Block IP address [X.X.X.X]"
- "Set up UFW on Ubuntu server"
- "Create iptables/nftables rules"
- "Configure bastion host firewall"
- "Implement egress filtering"

**Scenarios:**
- Initial server setup and hardening
- Exposing a new service (web server, API, database)
- Implementing network segmentation
- Creating bastion host or jump box
- Migrating from iptables to nftables
- Configuring cloud security groups
- Troubleshooting connectivity issues

### Scope

**Covers:**
- iptables basics and rule management
- nftables syntax and migration from iptables
- UFW for simplified firewall management (Ubuntu/Debian)
- AWS Security Groups and Network ACLs
- GCP firewall rules and VPC configuration
- Azure Network Security Groups (NSGs)
- Stateful vs stateless firewall concepts
- Common security patterns (bastion, DMZ, egress filtering)
- Firewall logging and auditing
- Kubernetes NetworkPolicies (basic ingress/egress)

**Does NOT Cover:**
- Network architecture design (see network-architecture skill)
- Full security architecture (see security-hardening skill)
- Service mesh policies (see service-mesh skill)
- WAF (Web Application Firewall) configuration
- Advanced IDS/IPS systems (Snort, Suricata)
- DDoS mitigation strategies

---

## Research Findings

### Research Methodology

**Tools Used:**
- Google Search Grounding (8 results per query)
- Direct source analysis

**Queries Executed:**
1. "iptables nftables firewall best practices 2025"
2. "AWS security groups vs NACLs best practices"
3. "UFW firewall configuration Ubuntu server 2025"

**Sources Analyzed:** 20+ recent articles, official documentation, community guides

---

### Key Finding 1: nftables is Now Recommended Standard

**From Research:**
- nftables offers O(log n) performance vs iptables O(n) linear processing
- Unified syntax for IPv4, IPv6, NAT, and filtering
- Built-in sets/maps (no external ipset required)
- Transaction-based atomicity (vs rule-by-rule in iptables)
- Advanced tracing for debugging

**Best Practices (2025):**
- ✅ Use nftables for new deployments
- ✅ Use `meta l4proto` (more robust than `nexthdr`)
- ✅ Leverage sets for IP/port lists
- ✅ Structure: Tables → Chains → Rules
- ⚠️ Don't mix iptables and nftables (causes conflicts)

**When iptables Still Makes Sense:**
- Legacy systems that can't upgrade
- Existing automation heavily dependent on iptables syntax
- Granular packet-level scripting requirements

---

### Key Finding 2: AWS Security Groups vs NACLs

**Core Differences:**

| Feature             | Security Groups              | Network ACLs                      |
|---------------------|------------------------------|-----------------------------------|
| **Level**           | Instance (ENI)               | Subnet                            |
| **State**           | Stateful                     | Stateless                         |
| **Rules**           | Allow only                   | Allow + Deny                      |
| **Evaluation**      | All rules evaluated          | Sequential (order matters)        |
| **Default**         | Deny inbound, allow outbound | Allow all inbound and outbound    |
| **Use Case**        | Resource-specific control    | Subnet-wide policies              |

**Security Groups Best Practices:**
- Principle of least privilege (only open required ports)
- Dedicated security group for SSH/RDP access
- Descriptive names and rule descriptions
- Avoid "default" security group for active resources
- Use managed prefix lists for IP grouping
- Regular auditing and removal of unused rules
- Infrastructure as Code (Terraform/CloudFormation)
- Enable VPC Flow Logs

**NACLs Best Practices:**
- Separate NACLs for public vs private subnets
- Start with default deny, explicitly allow required traffic
- Manage ephemeral port ranges (1024-65535 for Linux)
- Sequential rule numbering (100, 200, 300 for easy insertion)
- Place deny rules earlier in sequence
- Separate IPv4 and IPv6 rules
- Limit number of rules (performance impact)
- Include ELB, Lambda health check ranges

**Defense-in-Depth Strategy:**
- Use Security Groups for instance-level control (primary)
- Use NACLs for subnet-wide enforcement (secondary)
- Combine both for layered security

---

### Key Finding 3: UFW Best Practices

**UFW (Uncomplicated Firewall):**
- User-friendly front-end for iptables/nftables
- Default on Ubuntu, available on Debian-based systems
- Ideal for servers where simplicity > granular control

**Best Practices:**
- Enable default deny: `ufw default deny incoming`
- Allow SSH BEFORE enabling: `ufw allow ssh` (prevent lockout)
- Use service names when possible: `ufw allow http` vs `ufw allow 80`
- Limit SSH attempts: `ufw limit ssh` (rate limiting)
- Check status: `ufw status verbose`
- Enable logging: `ufw logging on` (check `/var/log/ufw.log`)
- Delete by rule number: `ufw status numbered` then `ufw delete [N]`

**Common Patterns:**
```bash
# Basic web server
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw limit ssh  # Rate limit SSH
ufw allow http
ufw allow https
ufw enable

# Allow from specific IP
ufw allow from 192.168.1.100 to any port 3306  # MySQL

# Allow port range
ufw allow 6000:6007/tcp
```

---

### Key Finding 4: General Firewall Best Practices

**Universal Principles:**
1. **Default Deny:** Start with deny-all, explicitly allow required traffic
2. **Principle of Least Privilege:** Only open necessary ports/IPs
3. **Documentation:** Version control firewall rules (Git)
4. **Testing:** Use nmap to verify external port exposure
5. **Logging:** Enable and monitor firewall logs
6. **Auditing:** Regular reviews of rules and access patterns
7. **Multi-Layered:** Combine host and network firewalls
8. **Fail2Ban:** Pair with intrusion prevention tools

**Common Mistakes to Avoid:**
- ❌ Allowing 0.0.0.0/0 on sensitive ports (database, SSH)
- ❌ Forgetting to enable firewall after configuration
- ❌ Not testing before enabling (risk lockout)
- ❌ Opening large port ranges unnecessarily
- ❌ Missing ephemeral port ranges (breaks return traffic)
- ❌ No logging (can't debug or audit)
- ❌ Running iptables and nftables simultaneously

---

## Firewall Taxonomy

### 1. Host-Based Firewalls

**iptables** (Legacy, Still Widely Used)
- Netfilter kernel module front-end
- Separate tools: `iptables` (IPv4), `ip6tables` (IPv6), `iptables-nat`
- Tables: filter, nat, mangle, raw
- Chains: INPUT, OUTPUT, FORWARD, PREROUTING, POSTROUTING
- Linear rule processing (O(n))

**nftables** (Modern, Recommended)
- Unified replacement for iptables family
- Single tool for IPv4, IPv6, NAT, filtering
- Tables → Chains → Rules hierarchy
- Set-based rule matching (O(log n))
- Transaction-based updates

**UFW (Uncomplicated Firewall)**
- Front-end for iptables/nftables
- Simplified syntax
- Profile-based rules (`/etc/ufw/applications.d/`)
- Default on Ubuntu/Debian

**firewalld** (RHEL/CentOS/Fedora)
- Dynamic firewall management
- Zone-based configuration
- D-Bus interface for runtime changes
- Uses nftables backend (RHEL 8+)

---

### 2. Cloud-Based Firewalls

**AWS Security Groups**
- Virtual firewall for EC2, RDS, ELB, etc.
- Stateful (return traffic automatically allowed)
- Operates at ENI (Elastic Network Interface) level
- Allow rules only (implicit deny)
- Multiple security groups per instance

**AWS Network ACLs**
- Subnet-level firewall
- Stateless (must explicitly allow return traffic)
- Allow and deny rules
- Sequential rule evaluation (lowest number first)
- One NACL per subnet

**GCP Firewall Rules**
- VPC-level firewall
- Stateful (like AWS Security Groups)
- Priority-based (0-65535, lower = higher priority)
- Target tags or service accounts
- Implied allow egress / deny ingress by default

**Azure Network Security Groups (NSGs)**
- Subnet or NIC level
- Stateful
- Priority-based (100-4096)
- Service tags for Azure services
- Application Security Groups for logical grouping

---

### 3. Container/Orchestration Firewalls

**Kubernetes NetworkPolicies**
- Pod-level ingress/egress rules
- Namespace-scoped
- Label-based selection
- Requires CNI plugin support (Calico, Cilium, Weave)

**Docker iptables Integration**
- Docker manipulates iptables for port publishing
- DOCKER chain for container rules
- User-defined bridge networks have isolation

---

## Decision Framework

### Which Firewall Tool to Use?

```
START: Need to configure firewall

├─ Cloud Environment?
│  ├─ YES: AWS?
│  │  ├─ Instance-level control → Security Groups
│  │  └─ Subnet-level enforcement → NACLs
│  ├─ YES: GCP?
│  │  └─ Use VPC Firewall Rules
│  ├─ YES: Azure?
│  │  └─ Use Network Security Groups (NSGs)
│  └─ NO: Continue to host-based
│
├─ Host-Based Linux Firewall?
│  ├─ Ubuntu/Debian + Simplicity needed?
│  │  └─ Use UFW (recommended for most users)
│  ├─ RHEL/CentOS/Fedora?
│  │  └─ Use firewalld (default)
│  ├─ Modern distro + Advanced control?
│  │  └─ Use nftables (best performance)
│  └─ Legacy system or existing iptables scripts?
│     └─ Use iptables (migrate to nftables when feasible)
│
├─ Kubernetes/Container?
│  └─ Use NetworkPolicies (requires CNI support)
│
└─ Multiple layers needed?
   └─ Implement defense-in-depth:
      - Cloud: Security Groups + NACLs
      - Host: UFW/nftables + fail2ban
      - Container: NetworkPolicies
```

---

### Stateful vs Stateless Decision

**Use Stateful Firewalls When:**
- Simplicity is priority (don't manage return traffic)
- Instance/resource-level control
- Examples: Security Groups, UFW, nftables (default)

**Use Stateless Firewalls When:**
- Subnet-wide policies needed
- Fine-grained control over both directions
- Performance at scale (less state tracking)
- Examples: NACLs

---

## Implementation Patterns

### Pattern 1: Basic UFW Setup (Ubuntu Server)

**Scenario:** Secure a new Ubuntu web server

```bash
# 1. Check status (should be inactive initially)
sudo ufw status

# 2. Set defaults (deny incoming, allow outgoing)
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 3. CRITICAL: Allow SSH BEFORE enabling (prevent lockout)
sudo ufw allow ssh
# OR specific port:
sudo ufw allow 22/tcp

# 4. Rate-limit SSH to prevent brute force
sudo ufw limit ssh

# 5. Allow web traffic
sudo ufw allow http   # Port 80
sudo ufw allow https  # Port 443

# 6. Allow from specific IP (e.g., office IP to database)
sudo ufw allow from 203.0.113.100 to any port 5432  # PostgreSQL

# 7. Enable firewall
sudo ufw enable

# 8. Verify rules
sudo ufw status verbose
sudo ufw status numbered  # Shows rule numbers for deletion

# 9. Enable logging
sudo ufw logging on

# 10. Test externally
nmap -Pn <server-ip>  # Should only show 22, 80, 443
```

**Deletion Example:**
```bash
# By rule number
sudo ufw status numbered
sudo ufw delete 3

# By rule specification
sudo ufw delete allow 80/tcp
```

---

### Pattern 2: nftables Basic Setup

**Scenario:** Configure nftables on modern Linux system

```bash
# 1. Install nftables (if not present)
sudo apt install nftables  # Debian/Ubuntu
sudo dnf install nftables  # RHEL/Fedora

# 2. Create basic firewall ruleset
sudo nano /etc/nftables.conf
```

```nftables
#!/usr/sbin/nft -f

# Flush existing rules
flush ruleset

# Define table
table inet filter {
    # Input chain (incoming traffic)
    chain input {
        type filter hook input priority 0; policy drop;

        # Accept loopback
        iif "lo" accept

        # Accept established/related connections (stateful)
        ct state established,related accept

        # Drop invalid packets
        ct state invalid drop

        # Allow ICMP (ping)
        meta l4proto icmp accept
        meta l4proto ipv6-icmp accept

        # Allow SSH (port 22)
        tcp dport 22 accept

        # Allow HTTP/HTTPS
        tcp dport { 80, 443 } accept

        # Log dropped packets
        log prefix "nftables-drop: " drop
    }

    # Forward chain (for routing)
    chain forward {
        type filter hook forward priority 0; policy drop;
    }

    # Output chain (outgoing traffic)
    chain output {
        type filter hook output priority 0; policy accept;
    }
}
```

```bash
# 3. Load ruleset
sudo nft -f /etc/nftables.conf

# 4. Enable nftables service (persist on reboot)
sudo systemctl enable nftables
sudo systemctl start nftables

# 5. Verify rules
sudo nft list ruleset

# 6. Test connectivity
ss -tuln  # Check listening ports
```

**Advanced nftables: Using Sets**
```nftables
table inet filter {
    # Define set of allowed IPs
    set allowed_ips {
        type ipv4_addr
        elements = { 192.168.1.100, 203.0.113.50 }
    }

    chain input {
        type filter hook input priority 0; policy drop;

        # Allow SSH only from allowed IPs
        tcp dport 22 ip saddr @allowed_ips accept

        # ... other rules
    }
}
```

---

### Pattern 3: iptables Basic Setup (Legacy Systems)

**Scenario:** Configure iptables on older Linux system

```bash
# 1. Check existing rules
sudo iptables -L -v -n

# 2. Set default policies
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# 3. Allow loopback
sudo iptables -A INPUT -i lo -j ACCEPT

# 4. Allow established connections (stateful)
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# 5. Allow SSH
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 6. Rate-limit SSH (prevent brute force)
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 -j DROP

# 7. Allow HTTP/HTTPS
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# 8. Allow ICMP (ping)
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT

# 9. Log dropped packets
sudo iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables-drop: " --log-level 7

# 10. Save rules (Debian/Ubuntu)
sudo netfilter-persistent save
# OR (RHEL/CentOS)
sudo service iptables save

# 11. Enable on boot
sudo systemctl enable netfilter-persistent  # Debian/Ubuntu
sudo systemctl enable iptables              # RHEL/CentOS
```

**List and Delete Rules:**
```bash
# List with line numbers
sudo iptables -L INPUT --line-numbers

# Delete by line number
sudo iptables -D INPUT 5

# Flush all rules (dangerous!)
sudo iptables -F
```

---

### Pattern 4: Migrate iptables to nftables

**Scenario:** Migrating existing iptables rules to nftables

```bash
# 1. Export existing iptables rules
sudo iptables-save > /tmp/iptables-rules.txt

# 2. Convert to nftables format
sudo iptables-restore-translate -f /tmp/iptables-rules.txt > /tmp/nftables-rules.nft

# 3. Review converted rules
cat /tmp/nftables-rules.nft

# 4. Test in separate table (don't break existing setup)
sudo nft -f /tmp/nftables-rules.nft

# 5. Verify both work
sudo nft list ruleset
sudo iptables -L

# 6. Once confident, switch:
# Disable iptables
sudo systemctl stop iptables
sudo systemctl disable iptables

# Enable nftables
sudo systemctl enable nftables
sudo systemctl start nftables

# 7. Clean up iptables rules
sudo iptables -F
sudo iptables -X
```

---

## Cloud Security Groups

### AWS Security Groups - Best Practices

**Pattern 1: Web Server Security Group**

```hcl
# Terraform example
resource "aws_security_group" "web" {
  name        = "web-server-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  # Inbound rules
  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description     = "SSH from bastion only"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]  # Reference bastion SG
  }

  # Outbound rules (default allow all, but explicit is better)
  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # All protocols
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "web-server-sg"
    Environment = "production"
  }
}
```

**Pattern 2: Database Security Group (Private)**

```hcl
resource "aws_security_group" "database" {
  name        = "database-sg"
  description = "Security group for RDS database"
  vpc_id      = aws_vpc.main.id

  # Only allow from app tier
  ingress {
    description     = "PostgreSQL from app servers"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  # No outbound internet access needed for database
  egress {
    description = "Local VPC only"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

  tags = {
    Name        = "database-sg"
    Environment = "production"
  }
}
```

---

### AWS Network ACLs - Best Practices

**Pattern: Public Subnet NACL**

```hcl
resource "aws_network_acl" "public" {
  vpc_id     = aws_vpc.main.id
  subnet_ids = aws_subnet.public[*].id

  # Inbound rules (evaluated in order)

  # Rule 100: Allow HTTP
  ingress {
    rule_no    = 100
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 80
    to_port    = 80
  }

  # Rule 110: Allow HTTPS
  ingress {
    rule_no    = 110
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 443
    to_port    = 443
  }

  # Rule 120: Allow SSH from specific IP
  ingress {
    rule_no    = 120
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "203.0.113.0/24"  # Office IP range
    from_port  = 22
    to_port    = 22
  }

  # Rule 140: CRITICAL - Allow ephemeral ports (return traffic)
  ingress {
    rule_no    = 140
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 1024
    to_port    = 65535
  }

  # Rule 200: Deny specific malicious IP
  ingress {
    rule_no    = 200
    protocol   = "-1"  # All protocols
    action     = "deny"
    cidr_block = "198.51.100.0/24"
    from_port  = 0
    to_port    = 0
  }

  # Default deny (implicit, rule *)

  # Outbound rules

  # Rule 100: Allow all outbound (typical for public subnet)
  egress {
    rule_no    = 100
    protocol   = "-1"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }

  tags = {
    Name = "public-subnet-nacl"
  }
}
```

**Key Points:**
- Stateless = must explicitly allow return traffic (ephemeral ports 1024-65535)
- Rules evaluated in order (lowest number first)
- Place deny rules before allow rules when blocking specific IPs
- Number rules by 10s or 100s to allow easy insertion

---

## Common Patterns

### Pattern 1: Bastion Host (Jump Box)

**Purpose:** Single hardened entry point for SSH access to private instances

**UFW Configuration (Bastion Host):**
```bash
# On bastion host
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH from specific IPs only (office, VPN)
sudo ufw allow from 203.0.113.0/24 to any port 22

# Rate limit SSH
sudo ufw limit ssh

# Enable and verify
sudo ufw enable
sudo ufw status verbose
```

**Security Group (AWS):**
```hcl
# Bastion security group
resource "aws_security_group" "bastion" {
  name        = "bastion-sg"
  description = "Bastion host for SSH access"
  vpc_id      = aws_vpc.main.id

  # Allow SSH from office IP only
  ingress {
    description = "SSH from office"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["203.0.113.0/24"]  # Office IP
  }

  # Allow outbound SSH to private instances
  egress {
    description     = "SSH to private instances"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.private.id]
  }

  tags = {
    Name = "bastion-sg"
  }
}

# Private instance security group
resource "aws_security_group" "private" {
  name        = "private-instance-sg"
  description = "Private instances accessible via bastion"
  vpc_id      = aws_vpc.main.id

  # Only allow SSH from bastion
  ingress {
    description     = "SSH from bastion only"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "private-instance-sg"
  }
}
```

---

### Pattern 2: DMZ (Demilitarized Zone)

**Purpose:** Isolate public-facing services from internal network

**Network Topology:**
```
Internet
    │
    ├─ Public Subnet (DMZ) - Web/API Servers
    │   - Restricted outbound to internal
    │   - Monitored heavily
    │
    ├─ Private Subnet (App Tier)
    │   - No direct internet access
    │   - Accepts connections from DMZ only
    │
    └─ Private Subnet (Data Tier)
        - Accepts connections from App Tier only
```

**NACL Example (DMZ Subnet):**
```hcl
resource "aws_network_acl" "dmz" {
  vpc_id     = aws_vpc.main.id
  subnet_ids = [aws_subnet.dmz.id]

  # Inbound: Public access to web services
  ingress {
    rule_no    = 100
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 443
    to_port    = 443
  }

  # Inbound: Ephemeral ports for return traffic
  ingress {
    rule_no    = 140
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 1024
    to_port    = 65535
  }

  # Outbound: Allow to app tier only (not internet)
  egress {
    rule_no    = 100
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "10.0.2.0/24"  # App tier subnet
    from_port  = 8080
    to_port    = 8080
  }

  # Outbound: Ephemeral ports for responses
  egress {
    rule_no    = 140
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 1024
    to_port    = 65535
  }

  tags = {
    Name = "dmz-nacl"
  }
}
```

---

### Pattern 3: Egress Filtering (Prevent Data Exfiltration)

**Purpose:** Control outbound traffic to prevent malware communication and data leaks

**nftables Example (Allow only specific external services):**
```nftables
table inet filter {
    # Define allowed external IPs (e.g., API endpoints)
    set allowed_destinations {
        type ipv4_addr
        elements = {
            52.4.48.0/24,     # AWS API
            140.82.112.0/20   # GitHub
        }
    }

    chain output {
        type filter hook output priority 0; policy drop;

        # Allow loopback
        oif "lo" accept

        # Allow established/related
        ct state established,related accept

        # Allow DNS (needed for name resolution)
        udp dport 53 accept
        tcp dport 53 accept

        # Allow only to approved destinations
        ip daddr @allowed_destinations accept

        # Allow internal network
        ip daddr 10.0.0.0/8 accept

        # Log and drop everything else
        log prefix "egress-blocked: " drop
    }
}
```

**Security Group Example (AWS - Restrictive Egress):**
```hcl
resource "aws_security_group" "restricted_egress" {
  name        = "restricted-egress-sg"
  description = "Only allow specific outbound connections"
  vpc_id      = aws_vpc.main.id

  # Explicit egress rules (remove default allow-all)

  egress {
    description = "HTTPS to internal API"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.5.0/24"]  # Internal API subnet
  }

  egress {
    description = "PostgreSQL to database"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.10.0/24"]  # Database subnet
  }

  egress {
    description = "DNS for name resolution"
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # No general internet access - must be explicit

  tags = {
    Name = "restricted-egress-sg"
  }
}
```

---

### Pattern 4: Kubernetes NetworkPolicy (Basic)

**Scenario:** Restrict pod-to-pod communication in Kubernetes

```yaml
# Deny all ingress by default (namespace-wide)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}  # Applies to all pods in namespace
  policyTypes:
    - Ingress

---
# Allow frontend pods to access backend API
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend  # Backend pods
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend  # Only from frontend pods
      ports:
        - protocol: TCP
          port: 8080

---
# Allow backend to access database (different namespace)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-backend-to-db
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: database
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: production
          podSelector:
            matchLabels:
              app: backend
      ports:
        - protocol: TCP
          port: 5432

---
# Restrict egress from frontend (no external calls)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: restrict-frontend-egress
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
    - Egress
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: backend  # Only talk to backend
      ports:
        - protocol: TCP
          port: 8080
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns  # Allow DNS
      ports:
        - protocol: UDP
          port: 53
```

---

## Tool Recommendations

### Host-Based Firewall Tools (2025)

#### **Primary: nftables** (Modern Linux)

**Why nftables?**
- Best performance (O(log n) vs O(n))
- Unified IPv4/IPv6/NAT syntax
- Built-in sets/maps for scalability
- Transaction-based updates (atomic)
- Advanced debugging with tracing
- Default on most modern distros

**When to Use:**
- New deployments on Linux 4.14+
- Need for complex rule logic (sets, maps)
- Performance-critical environments
- Advanced packet filtering requirements

**Installation:**
```bash
# Debian/Ubuntu
sudo apt install nftables

# RHEL/CentOS
sudo dnf install nftables
```

**Configuration:** `/etc/nftables.conf`

---

#### **Alternative 1: UFW** (User-Friendly)

**Why UFW?**
- Simplest syntax for common use cases
- Default on Ubuntu
- Reasonable defaults out of box
- Application profiles (`/etc/ufw/applications.d/`)
- Lower learning curve

**When to Use:**
- Ubuntu/Debian servers
- Simple firewall requirements
- Prefer simplicity over granular control
- Quick server hardening

**Installation:**
```bash
sudo apt install ufw  # Usually pre-installed on Ubuntu
```

---

#### **Alternative 2: firewalld** (RHEL/CentOS)

**Why firewalld?**
- Default on RHEL/CentOS/Fedora
- Zone-based management
- Dynamic updates (no connection interruption)
- D-Bus API for integration
- Rich rule language

**When to Use:**
- Red Hat ecosystem
- Zone-based security requirements
- Need dynamic rule updates
- GUI management desired (firewall-config)

**Installation:**
```bash
sudo dnf install firewalld
```

---

#### **Legacy: iptables**

**Why iptables?**
- Still widely used and understood
- Extensive documentation and examples
- Existing scripts and automation
- Required for some older kernels

**When to Use:**
- Legacy systems (kernel < 4.14)
- Existing iptables automation
- Migration to nftables not feasible

**Note:** Migrate to nftables when possible for better performance and maintainability.

---

### Cloud Firewall Tools

#### **AWS: Terraform + Security Groups**

**Why Terraform?**
- Infrastructure as Code (version control)
- Multi-account consistency
- Plan-before-apply (review changes)
- State management
- Reusable modules

**Example Module Structure:**
```
terraform/
├── modules/
│   └── security-groups/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/
│   ├── production/
│   └── staging/
└── main.tf
```

**Alternative:** AWS CloudFormation (native AWS IaC)

---

#### **Multi-Cloud: Terraform with Provider Abstraction**

Use Terraform with cloud-agnostic modules:
- `aws_security_group` for AWS
- `google_compute_firewall` for GCP
- `azurerm_network_security_group` for Azure

---

### Monitoring & Auditing Tools

#### **VPC Flow Logs (AWS)**
- Capture IP traffic to/from network interfaces
- Store in CloudWatch Logs or S3
- Query with CloudWatch Insights or Athena

#### **nmap**
- External port scanning
- Verify firewall rules work as expected
```bash
nmap -Pn <server-ip>  # TCP SYN scan
nmap -sU <server-ip>  # UDP scan
```

#### **fail2ban**
- Intrusion prevention (ban IPs after failed attempts)
- Integrates with UFW/iptables/nftables
- Common filters: SSH, Apache, Nginx

#### **auditd**
- Linux audit framework
- Track firewall rule changes
- Compliance requirements (PCI-DSS)

---

## Skill Structure Design

### SKILL.md Structure (Main File)

**Target:** 400-500 lines (under 500 line limit)

```markdown
---
name: configuring-firewalls
description: Configure host-based firewalls (iptables, nftables, UFW) and cloud security groups (AWS, GCP, Azure) with practical rules for common scenarios like web servers, databases, and bastion hosts. Includes stateful/stateless patterns and safety checks to prevent lockouts.
---

# Configuring Firewalls

## Purpose
[2-3 sentences on skill purpose]

## When to Use
[Trigger phrases and scenarios]

## Decision Framework
[Quick guide: Which tool to use?]
See reference/decision-tree.md for detailed decision tree

## Common Patterns

### Quick Start: UFW (Ubuntu)
[5-10 line example]
See reference/ufw-patterns.md for complete guide

### Quick Start: nftables
[5-10 line example]
See reference/nftables-patterns.md for complete guide

### Quick Start: AWS Security Groups
[5-10 line Terraform example]
See reference/aws-security-groups.md for complete guide

## Safety Checklist
- [ ] Always allow SSH before enabling firewall
- [ ] Test rules before enabling
- [ ] Enable logging for debugging
- [ ] Document rules in version control
- [ ] Verify externally with nmap

## Advanced Topics
- Bastion host setup → reference/bastion-pattern.md
- DMZ architecture → reference/dmz-pattern.md
- Egress filtering → reference/egress-filtering.md
- Kubernetes NetworkPolicies → reference/k8s-networkpolicies.md
- Migrating iptables to nftables → reference/migration-guide.md

## Troubleshooting
See reference/troubleshooting.md

## Integration Points
- security-hardening (full server security)
- building-ci-pipelines (CI runner network access)
- deploying-applications (app server firewall rules)
```

---

### Reference Files (Progressive Disclosure)

**reference/ufw-patterns.md** (~100 lines)
- Installation and setup
- Common rule patterns (web, database, ssh)
- Rate limiting
- Logging and monitoring
- Deletion and management

**reference/nftables-patterns.md** (~150 lines)
- Installation and basic syntax
- Complete ruleset examples
- Sets and maps
- Logging and debugging
- Performance tips

**reference/iptables-patterns.md** (~100 lines)
- Basic rule syntax
- Common patterns
- Persistence across reboots
- Migration path to nftables

**reference/aws-security-groups.md** (~150 lines)
- Security Groups vs NACLs
- Terraform examples (web, app, database tiers)
- Best practices
- Managed prefix lists
- VPC Flow Logs integration

**reference/gcp-firewall.md** (~80 lines)
- GCP firewall rule structure
- Priority system
- Target tags
- Terraform examples

**reference/azure-nsg.md** (~80 lines)
- NSG structure and priority
- Application Security Groups
- Service tags
- Terraform examples

**reference/bastion-pattern.md** (~80 lines)
- Bastion host architecture
- UFW and Security Group examples
- SSH key management
- Session Manager alternative (AWS)

**reference/dmz-pattern.md** (~100 lines)
- DMZ topology
- NACL configuration
- Security Group layering
- Monitoring strategy

**reference/egress-filtering.md** (~100 lines)
- Why egress filtering matters
- nftables egress rules
- Security Group egress restrictions
- Allowlist approach

**reference/k8s-networkpolicies.md** (~120 lines)
- NetworkPolicy basics
- Default deny patterns
- Namespace isolation
- CNI plugin requirements (Calico, Cilium)

**reference/migration-guide.md** (~80 lines)
- iptables-save and iptables-restore-translate
- Testing in parallel
- Switchover process
- Rollback plan

**reference/troubleshooting.md** (~100 lines)
- "I locked myself out" recovery
- Connection timeouts
- Ephemeral port issues (cloud)
- Logging and debugging
- Common error messages

**reference/decision-tree.md** (~60 lines)
- Visual decision tree (which tool to use)
- Stateful vs stateless guide
- Cloud vs host-based considerations

---

### Scripts (Optional - No scripts needed for this skill)

Firewall configuration is typically declarative (config files) or imperative (CLI commands), not script-based. However, we could include:

**scripts/test-firewall.sh** (Optional)
- Automated testing after firewall changes
- Checks for common misconfigurations
- Runs nmap scan and verifies expected ports

**Decision:** Skip scripts for v1. Declarative configs in reference files are sufficient.

---

### Assets (Optional)

**assets/firewall-architecture-diagrams/** (Optional)
- Bastion host topology diagram
- DMZ architecture diagram
- Defense-in-depth layers

**Decision:** Include simple ASCII diagrams in reference files for v1.

---

## Integration Points

### 1. security-hardening Skill

**Relationship:** Firewalls are ONE component of server hardening

**Integration:**
- security-hardening skill should reference configuring-firewalls for firewall setup
- configuring-firewalls focuses ONLY on firewall configuration
- security-hardening covers: SSH hardening, user permissions, package updates, fail2ban, auditd, SELinux

**Cross-Reference:**
```markdown
# In security-hardening/SKILL.md
## Firewall Configuration
For detailed firewall setup, see the configuring-firewalls skill.
Quick: Use UFW on Ubuntu, firewalld on RHEL.

# In configuring-firewalls/SKILL.md
## Broader Security Context
Firewalls are one layer of defense. For complete server hardening, see security-hardening skill.
```

---

### 2. building-ci-pipelines Skill

**Relationship:** CI runners need network access to repos and artifact stores

**Integration:**
- CI pipelines often run on instances that need firewall rules
- Self-hosted runners need outbound HTTPS (GitHub, GitLab)
- May need inbound webhook access

**Example Use Case:**
```markdown
# In building-ci-pipelines/SKILL.md
## Self-Hosted Runner Network Configuration

For firewall configuration, see configuring-firewalls skill.

Required outbound access:
- HTTPS (443) to github.com, api.github.com
- Package registries (npm, PyPI, Docker Hub)

Security Group example:
See configuring-firewalls for complete Terraform module.
```

---

### 3. deploying-applications Skill

**Relationship:** Application deployment requires firewall rules for services

**Integration:**
- Web apps need port 80/443 open
- APIs need specific port access
- Databases should be restricted to app tier only

**Example Use Case:**
```markdown
# In deploying-applications/SKILL.md
## Exposing Your Application

After deployment, configure firewall rules to allow traffic.
See configuring-firewalls skill for:
- UFW rules for standalone servers
- Security Groups for AWS deployments
- NACLs for subnet-level control
```

---

### 4. infrastructure-as-code Skill

**Relationship:** Firewalls should be managed as code (Terraform, CloudFormation)

**Integration:**
- configuring-firewalls provides Terraform examples
- infrastructure-as-code covers broader IaC principles
- Both skills complement each other

**Cross-Reference:**
```markdown
# In infrastructure-as-code/SKILL.md
## Network Security Resources

For firewall-specific Terraform/CloudFormation:
- Security Groups and NACLs → configuring-firewalls skill
- VPC and subnet design → network-architecture skill

# In configuring-firewalls/SKILL.md
## Infrastructure as Code

All examples use Terraform for reproducibility.
For IaC best practices (state management, modules, testing):
See infrastructure-as-code skill.
```

---

### 5. kubernetes-operations Skill

**Relationship:** Kubernetes NetworkPolicies are firewall-like controls

**Integration:**
- NetworkPolicies covered at basic level in configuring-firewalls
- kubernetes-operations covers broader K8s networking (Services, Ingress, CNI)

**Boundary:**
- configuring-firewalls: Basic NetworkPolicy examples (default deny, pod-to-pod rules)
- kubernetes-operations: Advanced K8s networking, service meshes, CNI plugin config

---

## Implementation Roadmap

### Phase 1: Core SKILL.md (Week 1)
- [ ] Write SKILL.md main file (400-500 lines)
- [ ] Include decision framework
- [ ] Add safety checklist
- [ ] Quick start examples (UFW, nftables, AWS SG)
- [ ] Cross-references to detailed guides

### Phase 2: Host-Based Firewall References (Week 1-2)
- [ ] reference/ufw-patterns.md
- [ ] reference/nftables-patterns.md
- [ ] reference/iptables-patterns.md
- [ ] reference/migration-guide.md

### Phase 3: Cloud Firewall References (Week 2)
- [ ] reference/aws-security-groups.md (Security Groups + NACLs)
- [ ] reference/gcp-firewall.md
- [ ] reference/azure-nsg.md

### Phase 4: Advanced Patterns (Week 2-3)
- [ ] reference/bastion-pattern.md
- [ ] reference/dmz-pattern.md
- [ ] reference/egress-filtering.md
- [ ] reference/k8s-networkpolicies.md

### Phase 5: Supporting Content (Week 3)
- [ ] reference/troubleshooting.md
- [ ] reference/decision-tree.md
- [ ] ASCII diagrams in reference files

### Phase 6: Testing & Iteration (Week 3-4)
- [ ] Test with real firewall configuration scenarios
- [ ] Validate Terraform examples
- [ ] Verify no lockout scenarios in examples
- [ ] Test cross-references work as expected
- [ ] Token count optimization

---

## Success Criteria

### Functionality
- ✅ Engineer can configure firewalls without getting locked out
- ✅ Clear decision framework guides tool selection
- ✅ Examples work as-is (copy-paste ready)
- ✅ Cloud and host-based firewalls both covered
- ✅ Safety practices emphasized throughout

### Quality
- ✅ SKILL.md under 500 lines
- ✅ All Terraform examples syntactically valid
- ✅ All bash commands tested
- ✅ No time-sensitive information
- ✅ Consistent terminology (Security Groups, not "SGs" inconsistently)

### Usability
- ✅ Quick start examples in main SKILL.md
- ✅ Progressive disclosure to detailed guides
- ✅ Clear troubleshooting section
- ✅ Safety checklist prevents common mistakes
- ✅ Integration points documented

---

## Research Sources

**Google Search Grounding (December 3, 2025):**

1. **nftables vs iptables best practices**
   - wpsauce.com: nftables recommended, O(log n) performance
   - webasha.com: Unified syntax, transaction-based updates
   - stackademic.com: meta l4proto best practice
   - medium.com: Migration guide and comparison

2. **AWS Security Groups vs NACLs**
   - dev.to: Detailed comparison, stateful vs stateless
   - jit.io: Best practices and defense-in-depth
   - plainenglish.io: Terraform examples
   - aws.com: Official documentation
   - k21academy.com: Use case guide

3. **UFW Configuration**
   - digitalocean.com: Comprehensive UFW guide
   - medium.com: Best practices
   - hostman.com: Ubuntu-specific setup
   - milesweb.ae: Advanced configuration

---

## Version History

**v1.0 (December 3, 2025)** - Master Plan Complete
- Research completed using Google Search Grounding
- Taxonomy and decision framework established
- Implementation patterns documented
- Skill structure designed
- Ready for SKILL.md implementation

---

**Next Step:** Implement SKILL.md following the structure outlined in Section 10 (Skill Structure Design).
