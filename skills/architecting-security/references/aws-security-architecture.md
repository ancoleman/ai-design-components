# AWS Security Architecture Reference


## Table of Contents

- [AWS Well-Architected Framework - Security Pillar](#aws-well-architected-framework-security-pillar)
  - [5 Design Principles](#5-design-principles)
- [Key AWS Security Services](#key-aws-security-services)
  - [Identity & Access Management](#identity-access-management)
  - [Detection & Response](#detection-response)
  - [Network Security](#network-security)
  - [Data Protection](#data-protection)
  - [Infrastructure Security](#infrastructure-security)
- [Multi-Account Security Architecture](#multi-account-security-architecture)
- [VPC Security Architecture](#vpc-security-architecture)

## AWS Well-Architected Framework - Security Pillar

### 5 Design Principles

1. **Implement strong identity foundation:** Centralize IAM, least privilege, separation of duties
2. **Enable traceability:** Log and monitor all actions
3. **Apply security at all layers:** Defense in depth across network, instance, application, data
4. **Automate security best practices:** Infrastructure as Code
5. **Protect data in transit and at rest:** Encryption everywhere

## Key AWS Security Services

### Identity & Access Management

| Service | Purpose |
|---------|---------|
| **AWS IAM** | User and service identity management |
| **IAM Identity Center** | SSO for multi-account environments |
| **AWS Cognito** | Customer identity and authentication |
| **AWS Organizations** | Multi-account management |

### Detection & Response

| Service | Purpose |
|---------|---------|
| **Amazon GuardDuty** | Threat detection (ML-based) |
| **AWS Security Hub** | Centralized security findings |
| **Amazon Detective** | Security investigation |
| **AWS CloudTrail** | API audit logging |

### Network Security

| Service | Purpose |
|---------|---------|
| **AWS WAF** | Web application firewall |
| **AWS Shield** | DDoS protection |
| **AWS Network Firewall** | Stateful network firewall |
| **AWS PrivateLink** | Private connectivity to services |

### Data Protection

| Service | Purpose |
|---------|---------|
| **AWS KMS** | Key management service |
| **AWS Secrets Manager** | Secrets rotation and management |
| **Amazon Macie** | Data discovery and classification |
| **AWS Certificate Manager** | SSL/TLS certificate management |

### Infrastructure Security

| Service | Purpose |
|---------|---------|
| **AWS Systems Manager** | Patch management, configuration |
| **Amazon Inspector** | Vulnerability scanning |
| **AWS Config** | Configuration compliance monitoring |

## Multi-Account Security Architecture

```
AWS Organizations (Root)
│
├── Security OU
│   ├── Security Account (GuardDuty, Security Hub)
│   ├── Logging Account (CloudTrail, Config, VPC Flow Logs)
│   └── Audit Account (Read-only cross-account access)
│
├── Production OU
│   ├── App1 Production Account
│   ├── App2 Production Account
│   └── Shared Services Account
│
└── Non-Production OU
    ├── Development Account
    ├── Staging Account
    └── Testing Account
```

**Key Patterns:**

- **Service Control Policies (SCPs):** Apply guardrails at OU level
- **IAM Identity Center:** SSO across all accounts
- **GuardDuty/Security Hub:** Organization-wide threat detection
- **Centralized Logging:** All CloudTrail logs to dedicated Logging Account
- **Network Isolation:** Separate VPCs per account, Transit Gateway for connectivity

## VPC Security Architecture

**Best Practices:**
- Public subnets: Internet-facing resources (ALB, NAT Gateway)
- Private subnets: Application tier (no direct internet access)
- Isolated subnets: Database tier (no outbound internet)
- Security groups: Stateful, least privilege rules
- NACLs: Stateless, additional layer of defense

**Example:**
```
VPC (10.0.0.0/16)
├── Public Subnet (10.0.1.0/24)
│   └── Internet Gateway → ALB → Internet
├── Private Subnet (10.0.2.0/24)
│   └── EC2 Instances (application tier)
└── Isolated Subnet (10.0.3.0/24)
    └── RDS (database tier)
```
