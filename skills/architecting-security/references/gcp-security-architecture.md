# GCP Security Architecture Reference

## GCP Security Best Practices

### Key GCP Security Services

#### Identity & Access Management

| Service | Purpose |
|---------|---------|
| **Cloud IAM** | Identity and access management |
| **Identity Platform** | Customer identity (CIAM) |
| **Cloud Identity** | Workforce identity management |

#### Detection & Response

| Service | Purpose |
|---------|---------|
| **Security Command Center** | Unified security and risk dashboard |
| **Chronicle** | SIEM and threat intelligence platform |
| **Event Threat Detection** | Real-time threat detection |

#### Network Security

| Service | Purpose |
|---------|---------|
| **Cloud Armor** | DDoS protection and WAF |
| **VPC Service Controls** | Data exfiltration prevention |
| **Cloud Firewall** | Stateful firewall rules |

#### Data Protection

| Service | Purpose |
|---------|---------|
| **Cloud KMS** | Key management service |
| **Secret Manager** | Secrets management |
| **Cloud DLP** | Data loss prevention |

#### Infrastructure Security

| Service | Purpose |
|---------|---------|
| **Binary Authorization** | Container image signing |
| **Confidential Computing** | Encryption in use (VMs, GKE) |

## GCP Organization Hierarchy

```
Organization (example.com)
│
├── Folder: Production
│   ├── Project: prod-app1
│   ├── Project: prod-app2
│   └── Project: prod-shared-services
│
├── Folder: Non-Production
│   ├── Project: dev-app1
│   ├── Project: staging-app1
│   └── Project: test-app1
│
└── Folder: Security
    ├── Project: security-logging
    └── Project: security-monitoring
```

**Key Patterns:**

- **Organization Policies:** Enforce constraints at org/folder level
- **Shared VPC:** Centralized network management
- **Security Command Center:** Organization-wide security posture
- **VPC Service Controls:** Protect sensitive projects from data exfiltration
