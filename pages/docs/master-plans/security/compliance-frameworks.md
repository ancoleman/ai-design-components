---
sidebar_position: 2
title: Compliance Frameworks
description: Master plan for implementing compliance frameworks including SOC 2, PCI-DSS, HIPAA, GDPR with compliance as code patterns
tags: [master-plan, security, compliance, soc2, pci-dss, hipaa, gdpr]
---

# Compliance Frameworks

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Compliance frameworks are mandatory for regulated industries and customer trust. This skill covers SOC 2, PCI-DSS, HIPAA, GDPR implementation with technical control mapping, compliance as code patterns, and evidence collection automation.

## Scope

This skill teaches:

- **Framework Overview** - SOC 2, PCI-DSS, HIPAA, GDPR, ISO 27001 requirements
- **Technical Controls** - Implementation of required security controls
- **Compliance as Code** - Automate compliance checks (Open Policy Agent, Cloud Custodian)
- **Evidence Collection** - Automated audit trail generation
- **Control Mapping** - Map technical implementations to compliance requirements
- **Continuous Compliance** - Real-time compliance monitoring and drift detection

## Key Components

### Major Compliance Frameworks

**SOC 2** - Service Organization Control (Trust Services Criteria)
- Security, Availability, Processing Integrity, Confidentiality, Privacy
- Required for: SaaS companies, service providers

**PCI-DSS** - Payment Card Industry Data Security Standard
- 12 requirements for protecting cardholder data
- Required for: Payment processing, e-commerce

**HIPAA** - Health Insurance Portability and Accountability Act
- Security Rule, Privacy Rule, Breach Notification Rule
- Required for: Healthcare, health data processors

**GDPR** - General Data Protection Regulation
- Data protection, privacy rights, breach notification
- Required for: EU data processing, global best practice

**ISO 27001** - Information Security Management System
- 114 security controls across 14 domains
- Global standard for information security

### Technical Control Examples

**Encryption at Rest (SOC 2, HIPAA, GDPR):**
- Database encryption (PostgreSQL, MySQL)
- Storage encryption (S3, EBS, Azure Storage)
- Key management (KMS, HSM, vault)

**Access Controls (All Frameworks):**
- Multi-factor authentication (MFA)
- Role-based access control (RBAC)
- Least privilege principle
- Access logging and review

**Network Security (PCI-DSS, SOC 2):**
- Network segmentation (VPCs, security groups)
- Firewalls, intrusion detection/prevention
- DDoS protection, WAF

**Logging and Monitoring (All Frameworks):**
- Centralized logging (SIEM)
- Audit trails (immutable logs)
- Real-time alerting
- Log retention (varies by framework)

### Compliance as Code Tools

**Open Policy Agent (OPA):**
- Policy-as-code for Kubernetes, CI/CD, cloud
- Rego language for policies
- Example: Deny pods without resource limits

**Cloud Custodian:**
- Cloud governance and compliance automation
- YAML-based policies for AWS, Azure, GCP
- Example: Auto-tag resources, enforce encryption

**InSpec:**
- Compliance testing framework (Chef)
- Test infrastructure against CIS benchmarks, custom profiles
- Example: Verify SSH hardening

## Decision Framework

**Which Compliance Framework?**

```
Industry?
  SaaS / service provider → SOC 2 (Type II)
  Payment processing → PCI-DSS
  Healthcare / health data → HIPAA
  EU / global → GDPR (baseline)
  Enterprise sales → ISO 27001

Data types processed?
  Payment cards → PCI-DSS mandatory
  Protected health information (PHI) → HIPAA
  Personal data (EU residents) → GDPR
  General business data → SOC 2

Customer requirements?
  Enterprise customers → SOC 2 + ISO 27001
  Healthcare customers → HIPAA + SOC 2
  Financial customers → PCI-DSS (if cards) + SOC 2
```

**Implementation Priority:**

```
1. Encryption (at rest and in transit) - Universal requirement
2. Access controls (MFA, RBAC) - Universal requirement
3. Logging and monitoring (SIEM) - Universal requirement
4. Network security (segmentation, firewalls) - Universal requirement
5. Framework-specific controls - Based on your compliance needs
```

## Tool Recommendations

### Compliance Automation

**Policy Enforcement:**
- Open Policy Agent (OPA/Gatekeeper) - Kubernetes policies
- Cloud Custodian - Multi-cloud governance
- HashiCorp Sentinel - Terraform policy enforcement

**Compliance Testing:**
- InSpec - Infrastructure testing
- Prowler - AWS security assessment
- ScoutSuite - Multi-cloud security auditing

**Evidence Collection:**
- Drata, Vanta, Secureframe - Automated compliance platforms
- Custom scripts + object storage for audit trails

### Platform-Specific Tools

**AWS:**
- AWS Config (compliance rules)
- AWS Security Hub (compliance dashboard)
- AWS Audit Manager (evidence collection)

**Azure:**
- Azure Policy (governance)
- Azure Security Center (compliance assessment)

**GCP:**
- Google Cloud Asset Inventory
- Security Command Center (compliance dashboard)

## Integration Points

**With Other Skills:**
- `security-architecture` - Map security controls to compliance
- `vulnerability-management` - Continuous security assessment
- `siem-logging` - Centralized logging for compliance
- `implementing-tls` - Encryption requirements
- `infrastructure-as-code` - Compliance as code (Terraform policies)

**Workflow Example:**
```
Compliance Requirement → Technical Control → IaC → Continuous Monitoring
         │                      │            │             │
         ▼                      ▼            ▼             ▼
  SOC 2: Encryption    KMS + S3        Terraform    OPA policies +
  at rest              encryption      modules      daily scans
```

## Learn More

- [Full Master Plan (init.md)](https://github.com/ancoleman/ai-design-components/blob/main/skills/compliance-frameworks/init.md)
- Related: `security-architecture`, `vulnerability-management`, `siem-logging`
