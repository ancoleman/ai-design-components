---
sidebar_position: 2
title: Compliance Frameworks
description: Implement SOC 2, HIPAA, PCI-DSS, and GDPR compliance with unified controls and automation
tags: [security, compliance, soc2, hipaa, pci-dss, gdpr, automation]
---

# Compliance Frameworks

Implement continuous compliance with major regulatory frameworks through unified control mapping, policy-as-code enforcement, and automated evidence collection.

## When to Use

Invoke when:
- Building SaaS products requiring SOC 2 Type II for enterprise sales
- Handling healthcare data (PHI) requiring HIPAA compliance
- Processing payment cards requiring PCI-DSS validation
- Serving EU residents and processing personal data under GDPR
- Implementing security controls that satisfy multiple compliance frameworks
- Automating compliance evidence collection and audit preparation
- Enforcing compliance policies in CI/CD pipelines

## Key Features

**Unified Control Strategy:**
- Implement controls once, map to multiple frameworks (reduces effort by 60-80%)
- Encryption (ENC-001): AES-256 at rest, TLS 1.3 in transit
- Access Control (MFA-001, RBAC-001): MFA, RBAC, least privilege
- Audit Logging (LOG-001): Centralized, immutable, 7-year retention
- Monitoring (MON-001): SIEM, intrusion detection, alerting
- Incident Response (IR-001): Detection, escalation, breach notification

**Framework Selection:**
- **SOC 2 Type II**: SaaS vendors, enterprise B2B sales (6-12 month observation period)
- **HIPAA**: Healthcare providers, health tech handling PHI
- **PCI-DSS 4.0**: Merchants, payment processors (mandatory April 2025)
- **GDPR**: Organizations processing EU residents' data (48-hour breach reporting)

**Policy-as-Code Enforcement:**
- Open Policy Agent (OPA): General-purpose policy engine
- Checkov: IaC security scanning with built-in compliance frameworks
- Automated testing in CI/CD pipelines

**Evidence Collection Automation:**
- Continuous monitoring via AWS Config, EventBridge, Lambda
- Automated audit report generation for SOC 2, HIPAA, PCI-DSS, GDPR
- Real-time compliance status dashboards

## Quick Start

```hcl
# Universal Control: Encryption at Rest
# Maps to: SOC2-CC6.1, HIPAA-164.312(a)(2)(iv), PCI-DSS Req 3.4, GDPR Art 32

resource "aws_kms_key" "data" {
  enable_key_rotation = true
  tags = { Compliance = "ENC-001" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.data.arn
    }
  }
}

resource "aws_db_instance" "main" {
  storage_encrypted = true
  kms_key_id       = aws_kms_key.data.arn
}
```

**Policy-as-Code (OPA Example):**

```bash
# Enforce encryption in CI/CD
terraform plan -out=tfplan.binary
terraform show -json tfplan.binary > tfplan.json
opa eval --data policies/ --input tfplan.json 'data.compliance.main.deny'
```

**Checkov Compliance Scanning:**

```bash
# Scan IaC with built-in compliance frameworks
checkov -d ./terraform \
  --check SOC2 --check HIPAA --check PCI --check GDPR \
  --output cli --output json
```

**Breach Notification Timelines:**
- HIPAA: 60 days to HHS and affected individuals
- GDPR: 48 hours to supervisory authority (2025 update)
- SOC 2: 72 hours to affected customers
- PCI-DSS: Immediate to payment brands

## Related Skills

- [Security Hardening](./security-hardening.md) - Technical security control implementation
- [Security Architecture](./architecting-security.md) - Strategic security design and governance
- [Managing Vulnerabilities](./managing-vulnerabilities.md) - Continuous vulnerability scanning for compliance
- [SIEM Logging](./siem-logging.md) - Audit logging and monitoring requirements
- [Secret Management](#) - Secrets handling per HIPAA/PCI-DSS requirements

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/implementing-compliance)
- [Master Plan](../../master-plans/security/implementing-compliance.md)
