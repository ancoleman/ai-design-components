# Azure Security Architecture Reference

## Microsoft Defender for Cloud

### Key Azure Security Services

#### Identity & Access Management

| Service | Purpose |
|---------|---------|
| **Azure AD (Entra ID)** | Identity platform |
| **Privileged Identity Management** | JIT access for admins |
| **Conditional Access** | Risk-based access policies |

#### Detection & Response

| Service | Purpose |
|---------|---------|
| **Microsoft Defender for Cloud** | CSPM and CWPP |
| **Microsoft Sentinel** | SIEM and SOAR platform |
| **Azure Monitor** | Logging and metrics collection |

#### Network Security

| Service | Purpose |
|---------|---------|
| **Azure Firewall** | Stateful network firewall |
| **Azure Front Door + WAF** | Global CDN and web application firewall |
| **Azure DDoS Protection** | DDoS mitigation |

#### Data Protection

| Service | Purpose |
|---------|---------|
| **Azure Key Vault** | Secrets, keys, certificates management |
| **Azure Information Protection** | Data classification and DLP |
| **Storage Encryption** | At-rest encryption for storage |

#### Infrastructure Security

| Service | Purpose |
|---------|---------|
| **Just-in-Time VM Access** | Time-bound SSH/RDP access |
| **Azure Policy** | Compliance enforcement |
| **Azure Blueprints** | Repeatable compliant environments |

## Azure Landing Zone Architecture (Hub-Spoke)

```
Azure AD Tenant (Root)
│
Management Groups Hierarchy:
  Root → Platform → Landing Zones → Applications
│
├── Hub VNet (Shared Services)
│   ├── Azure Firewall
│   ├── VPN Gateway
│   ├── Azure Bastion
│   └── Shared Services (DNS, monitoring)
│
├── Spoke VNet 1 (Production Workloads)
│   └── Application VMs/Services
│
├── Spoke VNet 2 (Development Workloads)
│   └── Application VMs/Services
│
└── Shared Services Subscription
    ├── Microsoft Defender for Cloud
    ├── Azure Monitor / Log Analytics
    └── Microsoft Sentinel
```

**Key Patterns:**

- **Hub-Spoke Topology:** Centralized security and networking
- **Management Groups:** Policy hierarchy and governance
- **Azure Policy:** Enforce compliance (e.g., require encryption)
- **Landing Zones:** Pre-configured secure environments
