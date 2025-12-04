# Compliance Frameworks Skill - Master Plan

**Skill Name:** `compliance-frameworks`
**Skill Level:** High Level (8,000-12,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Compliance Framework Taxonomy](#compliance-framework-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Technical Control Implementations](#technical-control-implementations)
7. [Compliance as Code Patterns](#compliance-as-code-patterns)
8. [Evidence Collection Automation](#evidence-collection-automation)
9. [Control Mapping Matrix](#control-mapping-matrix)
10. [Tool Recommendations](#tool-recommendations)
11. [Skill Structure Design](#skill-structure-design)
12. [Integration Points](#integration-points)
13. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why Compliance Frameworks Matter in 2025

Compliance is no longer an annual audit checkbox—it's a continuous engineering discipline. In 2025, with AI governance requirements, real-time breach reporting, and automated enforcement becoming standard, compliance frameworks must be treated as critical infrastructure.

**Market Drivers:**

- **Regulatory Expansion:** New requirements for AI governance (SOC 2 2025), stricter breach timelines (GDPR 48hrs, SOC 2 72hrs)
- **Continuous Compliance:** Shift from annual audits to real-time monitoring and automated evidence collection
- **Multi-Framework Reality:** Organizations must comply with 3-5+ frameworks simultaneously (SOC 2, HIPAA, PCI-DSS, GDPR, ISO 27001)
- **Policy as Code:** Infrastructure-as-code patterns applied to compliance policies (OPA, Checkov)
- **Zero Trust Architecture:** Traditional perimeter security insufficient; continuous verification required

**Strategic Value:**

1. **Risk Reduction:** Automated compliance reduces breach risk and regulatory penalties
2. **Customer Trust:** Compliance certifications (SOC 2 Type II) required for enterprise sales
3. **Operational Efficiency:** Automation reduces manual audit preparation from weeks to days
4. **Unified Controls:** Single control implementation can satisfy multiple frameworks

### 2025 Compliance Landscape

**Key Trends:**

- **SOC 2 Type II Evolution:** Monthly control testing (vs annual), AI governance controls, 72-hour breach disclosure
- **HIPAA Enhanced:** Zero Trust Architecture, XDR/EDR requirements, AI/third-party API assessments
- **PCI-DSS 4.0 Mandatory:** Client-side security, 12-character passwords, enhanced MFA (effective April 2025)
- **GDPR 2025 Updates:** AI transparency, 48-hour breach reporting, fines up to 6% of global revenue
- **Compliance as Code:** Policy automation becoming standard practice (not experimental)

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **Framework Selection & Mapping**
   - Which frameworks apply to your industry/region
   - Control mapping across multiple frameworks
   - Unified compliance strategies

2. **Technical Control Implementation**
   - Encryption at rest and in transit (AES-256, TLS 1.3+)
   - Access controls (RBAC, MFA, least privilege)
   - Audit logging and monitoring
   - Network security controls
   - Data protection patterns

3. **Compliance as Code**
   - Open Policy Agent (OPA) for policy enforcement
   - Checkov for IaC security scanning
   - Automated policy validation in CI/CD
   - Policy versioning and testing

4. **Evidence Collection**
   - Automated evidence gathering
   - Continuous monitoring dashboards
   - Audit trail generation
   - Report automation

5. **Operational Patterns**
   - Breach detection and notification
   - Incident response procedures
   - Vendor management (BAAs, DPAs)
   - Regular access reviews

### What This Skill Does NOT Cover

- **Legal Interpretation:** Consult legal counsel for compliance advice
- **Certification Process:** How to hire auditors, prepare for audits
- **Industry-Specific Regulations:** FINRA, FedRAMP, etc. (separate skills)
- **General Security Architecture:** Use `security-hardening` skill
- **Secret Management Details:** Use `secret-management` skill

---

## Research Findings

### Google Search Grounding Results (December 2025)

#### SOC 2 Type II (2025 Updates)

**Key Findings:**

- **Monthly Control Testing:** Type II reports now require monthly testing (previously annual)
- **AI Governance Controls (New):** Mandatory for systems handling client data with ML
  - AI logging and monitoring requirements
  - Algorithmic transparency
  - Bias mitigation controls
- **Third-Party Risk:** Vendor SOC 2 reports must be ≤90 days old
- **Real-Time Incident Reporting:** 72-hour breach disclosure (down from previous timelines)
- **Cloud Misconfigurations:** Automated CSPM checks expected
- **Zero Trust Security:** Continuous verification becoming mandatory
- **Encryption Standards:** AES-256 for data at rest, TLS 1.3 for data in transit

**Trust Services Criteria (TSC):**
1. **Security** (Mandatory): Protection against unauthorized access
2. **Availability** (Optional): System uptime guarantees (e.g., ≥99.99%)
3. **Processing Integrity** (Optional): Data processing accuracy
4. **Confidentiality** (Optional): Protection of confidential information
5. **Privacy** (Optional): Personal information handling

#### HIPAA Compliance (2025 Best Practices)

**Key Findings:**

- **Zero Trust Architecture:** "Never trust, always verify" across hybrid networks
- **Encryption Requirements:**
  - Data in transit: TLS 1.2+ (1.3 recommended)
  - Data at rest: AES-256 or FIPS 140-2 validated
  - Key management: HSMs or managed KMS
- **Access Controls:**
  - Role-based access control (RBAC)
  - Multi-factor authentication (MFA) for all ePHI access
  - Regular access audits
- **Endpoint Protection:** EDR/XDR required for all devices handling ePHI
- **Business Associate Agreements (BAAs):**
  - Required for all vendors handling PHI
  - Annual review mandatory
- **Incident Response:** 60-day breach notification timeline (unchanged)
- **AI/Third-Party APIs:** New compliance assessments required

**Technical Safeguards:**
- Access control, audit controls, integrity controls, transmission security

**Physical Safeguards:**
- Facility access controls, workstation security, device disposal

**Administrative Safeguards:**
- Privacy Officer, workforce training, risk assessments, contingency plans

#### PCI-DSS 4.0 (Effective April 1, 2025)

**Key Changes:**

- **Client-Side Security:** New requirements for payment page scripts
- **Multi-Factor Authentication:** Enhanced MFA for all CDE access
- **Password Requirements:** Minimum 12 characters (8 if system limitation)
- **Access Reviews:**
  - Human accounts: Every 6 months
  - Application/system accounts: Risk-based frequency
- **Encryption Updates:** Enhanced key management, no hard-coded passwords
- **Logging & Monitoring:** Enhanced capabilities required
- **Scope Validation:** Annual (or semi-annual for TPSPs)
- **Sensitive Authentication Data (SAD):** Explicit retention policies

**12 Core Requirements:**
1. Network security controls
2. Secure configurations
3. Protect stored account data
4. Encrypt transmission over public networks
5. Protect from malicious software
6. Secure systems and software
7. Restrict access to cardholder data
8. Identify users and authenticate access
9. Restrict physical access
10. Log and monitor access
11. Test security regularly
12. Support information security policies

#### GDPR (2025 Enhancements)

**Key Changes:**

- **48-Hour Breach Reporting:** Reduced from 72 hours (potential breaches included)
- **Increased Fines:** Up to 6% of global revenue (up from 4%)
- **AI Compliance:**
  - Algorithmic transparency required
  - Bias mitigation mandatory
  - Ethical AI governance frameworks
- **Expanded Personal Data:** Broader definition includes more data types
- **Cross-Border Transfers:** Greater transparency required

**Core Principles:**
1. Lawfulness, fairness, transparency
2. Purpose limitation
3. Data minimization
4. Accuracy
5. Storage limitation
6. Integrity and confidentiality (security)
7. Accountability

**Data Subject Rights:**
- Right to be informed, access, rectification, erasure
- Right to restrict processing, data portability, object
- Rights around automated decision-making

**Key Technical Requirements:**
- Privacy by Design and by Default
- Data Protection Impact Assessments (DPIAs)
- Data Protection Officer (DPO) for high-risk processing
- Consent Management Platforms (CMPs)

### Context7 Library Research

#### Open Policy Agent (OPA)

**Library:** `/open-policy-agent/opa`
**Trust Score:** High
**Code Snippets:** 1,741+
**Source Reputation:** High

**What is OPA?**
- General-purpose policy engine
- Unified policy enforcement across the stack
- High-level declarative language (Rego)
- Cloud-native, lightweight

**Key Features:**
- Policy as code with Rego language
- REST API for policy queries
- Integration with Kubernetes, Terraform, APIs
- Syntax checking and unit testing
- Schema annotations for type checking

**Use Cases:**
- API authorization
- Kubernetes admission control
- Terraform/IaC policy enforcement
- Microservices authorization
- Data filtering

#### Checkov

**Library:** `/bridgecrewio/checkov`
**Trust Score:** High (Benchmark: 90.5)
**Code Snippets:** 338+
**Source Reputation:** High

**What is Checkov?**
- Static code analysis for IaC
- Software composition analysis for images/packages
- Detects security and compliance misconfigurations

**Supported Frameworks:**
- Terraform, CloudFormation, Kubernetes, Helm
- Dockerfile, Serverless, ARM templates
- Custom policies (YAML-based)

**Key Features:**
- 1,000+ built-in policies
- Multi-framework support
- CI/CD integration
- Custom policy creation
- Terraform plan scanning
- Policy suppression (skip comments)

---

## Compliance Framework Taxonomy

### Tier 1: Trust & Security Certifications

#### SOC 2 Type II

**Audience:** SaaS vendors, cloud service providers
**Geography:** Global (US origin)
**Timeline:** 6-12 month observation period

**When Required:**
- Enterprise B2B sales
- Handling customer data in cloud
- Service provider / vendor relationships

**Control Categories:**
- Security (mandatory)
- Availability, Processing Integrity, Confidentiality, Privacy (optional)

**Implementation Effort:**
- First-time: 6-12 months
- Renewal: 3-6 months (annual)
- Continuous monitoring: Ongoing

#### ISO 27001

**Audience:** Global enterprises
**Geography:** International standard
**Timeline:** 3-6 month certification process

**When Required:**
- International business
- Government contracts
- Financial services

**Control Categories:**
- 14 domains, 114 controls
- ISMS (Information Security Management System)
- Risk-based approach

**Implementation Effort:**
- First-time: 12-18 months
- Renewal: 6-12 months (every 3 years)
- Surveillance audits: Annual

### Tier 2: Industry-Specific Regulations

#### HIPAA (Healthcare)

**Audience:** Healthcare providers, health tech companies
**Geography:** United States
**Timeline:** N/A (regulation, not certification)

**When Required:**
- Handling Protected Health Information (PHI)
- Electronic PHI (ePHI) transmission/storage
- Business Associates of Covered Entities

**Rule Categories:**
- Privacy Rule (patient rights)
- Security Rule (technical safeguards)
- Breach Notification Rule (60 days)

**Implementation Effort:**
- First-time: 6-12 months
- Ongoing: Continuous compliance

#### PCI-DSS (Payment Card Industry)

**Audience:** Merchants, payment processors
**Geography:** Global (applies to card payments)
**Timeline:** Annual validation

**When Required:**
- Processing credit/debit card payments
- Storing cardholder data
- Third-party service providers (TPSPs)

**Validation Levels:**
- Level 1: >6M transactions/year (QSA audit)
- Level 2: 1-6M transactions (SAQ + scans)
- Level 3: 20K-1M e-commerce (SAQ + scans)
- Level 4: <20K e-commerce (SAQ)

**Implementation Effort:**
- First-time: 6-12 months
- Renewal: 3-6 months (annual)

### Tier 3: Privacy Regulations

#### GDPR (General Data Protection Regulation)

**Audience:** Any organization processing EU residents' data
**Geography:** European Union (extraterritorial)
**Timeline:** N/A (regulation, not certification)

**When Required:**
- EU residents as customers/users
- Processing personal data of EU residents
- Establishment in EU

**Key Concepts:**
- Data Controller vs Data Processor
- Lawful basis for processing
- Data subject rights

**Implementation Effort:**
- First-time: 6-12 months
- Ongoing: Continuous compliance
- DPIAs for high-risk processing

#### CCPA/CPRA (California Privacy)

**Audience:** Businesses serving California residents
**Geography:** California, USA
**Timeline:** N/A (regulation)

**When Required:**
- Annual gross revenue >$25M
- Buy/sell personal info of 100K+ CA residents
- 50%+ revenue from selling personal info

**Key Rights:**
- Right to know, delete, opt-out, non-discrimination

**Implementation Effort:**
- First-time: 3-6 months
- Ongoing: Continuous compliance

---

## Decision Frameworks

### Framework 1: Which Compliance Frameworks Apply?

```
START: What type of organization?
  │
  ├─► SaaS/Cloud Service?
  │     YES ──► Customers require it?
  │               YES ──► SOC 2 Type II (mandatory for enterprise sales)
  │               NO ──► Consider for competitive advantage
  │
  ├─► Handle Payment Cards?
  │     YES ──► PCI-DSS 4.0 (mandatory, validate by April 2025)
  │
  ├─► Handle Healthcare Data?
  │     YES ──► US-based?
  │               YES ──► HIPAA (mandatory)
  │               NO ──► Consider local health data regulations
  │
  ├─► Serve EU Residents?
  │     YES ──► GDPR (mandatory)
  │
  ├─► Serve California Residents?
  │     YES ──► Revenue/volume thresholds met?
  │               YES ──► CCPA/CPRA (mandatory)
  │
  ├─► International Business?
  │     YES ──► ISO 27001 (competitive advantage, often required)
  │
  └─► Government Contracts?
        YES ──► FedRAMP, NIST, industry-specific (separate skills)
```

### Framework 2: Control Implementation Priority

**Phase 1: Foundation (Weeks 1-4)**
1. **Access Control**
   - MFA for all user accounts
   - RBAC implementation
   - Least privilege principle
2. **Encryption**
   - TLS 1.3 for all external traffic
   - AES-256 for data at rest
   - Key management system (KMS)
3. **Audit Logging**
   - Centralized logging infrastructure
   - Log retention policies
   - Log review procedures

**Phase 2: Detection (Weeks 5-8)**
1. **Monitoring**
   - SIEM or log aggregation
   - Alerting rules
   - Incident response procedures
2. **Vulnerability Management**
   - Automated scanning
   - Patch management
   - Dependency scanning
3. **Network Security**
   - Firewall rules
   - Network segmentation
   - DDoS protection

**Phase 3: Response (Weeks 9-12)**
1. **Incident Response Plan**
   - Detection procedures
   - Escalation paths
   - Communication templates
2. **Business Continuity**
   - Backup procedures
   - Disaster recovery
   - Failover testing
3. **Vendor Management**
   - Vendor risk assessment
   - BAAs/DPAs execution
   - Vendor monitoring

**Phase 4: Continuous Improvement (Ongoing)**
1. **Policy as Code**
   - OPA policy implementation
   - Checkov IaC scanning
   - CI/CD integration
2. **Automation**
   - Evidence collection
   - Compliance dashboards
   - Automated testing
3. **Training & Awareness**
   - Security awareness training
   - Phishing simulations
   - Policy acknowledgment

### Framework 3: Unified Control Mapping

Many controls satisfy multiple frameworks simultaneously.

| Control | SOC 2 | HIPAA | PCI-DSS | GDPR | ISO 27001 |
|---------|-------|-------|---------|------|-----------|
| MFA | CC6.1 | 164.312(d) | Req 8.3 | Art 32 | A.9.4.2 |
| Encryption at Rest | CC6.1 | 164.312(a)(2)(iv) | Req 3.4 | Art 32 | A.10.1.1 |
| Encryption in Transit | CC6.1 | 164.312(e)(1) | Req 4.1 | Art 32 | A.13.1.1 |
| Access Logging | CC7.2 | 164.312(b) | Req 10.2 | Art 30 | A.12.4.1 |
| Access Reviews | CC6.1 | 164.308(a)(3)(ii)(C) | Req 8.2.4 | Art 32 | A.9.2.5 |
| Vulnerability Scanning | CC7.1 | 164.308(a)(8) | Req 11.2 | Art 32 | A.12.6.1 |
| Patch Management | CC7.1 | 164.308(a)(5)(ii)(B) | Req 6.2 | Art 32 | A.12.6.1 |
| Incident Response | CC7.3 | 164.308(a)(6) | Req 12.10 | Art 33 | A.16.1.1 |
| Backup & Recovery | CC7.4 | 164.308(a)(7)(ii)(A) | Req 12.10 | Art 32 | A.12.3.1 |
| Security Training | CC1.4 | 164.308(a)(5) | Req 12.6 | Art 32 | A.7.2.2 |

**Strategy:** Implement once, map to multiple frameworks, reduce audit burden.

---

## Technical Control Implementations

### Control 1: Encryption

#### Encryption at Rest

**Requirement Mapping:**
- SOC 2: CC6.1, CC6.7
- HIPAA: 164.312(a)(2)(iv)
- PCI-DSS: Req 3.4
- GDPR: Article 32(1)(a)

**Implementation (AWS Example):**

```python
# terraform/encryption.tf
# S3 Bucket with KMS encryption
resource "aws_s3_bucket" "data" {
  bucket = "company-data-${var.environment}"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.data.arn
    }
    bucket_key_enabled = true
  }
}

# KMS key with rotation
resource "aws_kms_key" "data" {
  description             = "Data encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = {
    Compliance = "SOC2-HIPAA-GDPR"
    Purpose    = "data-encryption"
  }
}

resource "aws_kms_alias" "data" {
  name          = "alias/${var.environment}-data-key"
  target_key_id = aws_kms_key.data.id
}

# RDS with encryption
resource "aws_db_instance" "main" {
  identifier     = "${var.environment}-database"
  engine         = "postgres"
  engine_version = "15.4"

  storage_encrypted = true
  kms_key_id       = aws_kms_key.data.arn

  # ... other configuration
}

# EBS volume encryption (default)
resource "aws_ebs_encryption_by_default" "enabled" {
  enabled = true
}

resource "aws_ebs_default_kms_key" "default" {
  key_arn = aws_kms_key.data.arn
}
```

**Policy Validation (OPA):**

```rego
# policies/encryption_at_rest.rego
package compliance.encryption

# Deny S3 buckets without encryption
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket"
  not has_encryption(resource)

  msg := sprintf("S3 bucket '%s' must have encryption enabled", [resource.name])
}

has_encryption(resource) {
  resource.change.after.server_side_encryption_configuration[_].rule[_].apply_server_side_encryption_by_default
}

# Deny RDS instances without encryption
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_db_instance"
  resource.change.after.storage_encrypted != true

  msg := sprintf("RDS instance '%s' must have storage encryption enabled", [resource.name])
}

# Require KMS (not default AES256)
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket_server_side_encryption_configuration"
  encryption := resource.change.after.rule[_].apply_server_side_encryption_by_default
  encryption.sse_algorithm == "AES256"  # Default S3 encryption, not KMS

  msg := sprintf("Bucket encryption for '%s' must use aws:kms, not AES256", [resource.name])
}
```

#### Encryption in Transit

**Requirement Mapping:**
- SOC 2: CC6.1, CC6.6
- HIPAA: 164.312(e)(1)
- PCI-DSS: Req 4.1
- GDPR: Article 32(1)(a)

**Implementation (Application Level):**

```python
# api/config.py
import ssl
from typing import Dict

class SecurityConfig:
    """Security configuration for API"""

    # TLS Configuration
    TLS_MIN_VERSION = ssl.TLSVersion.TLSv1_3  # HIPAA, PCI-DSS 4.0
    TLS_CIPHERS = [
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS_AES_128_GCM_SHA256",
    ]

    # HSTS (HTTP Strict Transport Security)
    HSTS_MAX_AGE = 31536000  # 1 year
    HSTS_INCLUDE_SUBDOMAINS = True
    HSTS_PRELOAD = True

    @staticmethod
    def get_ssl_context() -> ssl.SSLContext:
        """Create secure SSL context"""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.minimum_version = SecurityConfig.TLS_MIN_VERSION
        context.set_ciphers(":".join(SecurityConfig.TLS_CIPHERS))
        return context

    @staticmethod
    def get_security_headers() -> Dict[str, str]:
        """Security headers for all responses"""
        return {
            "Strict-Transport-Security": f"max-age={SecurityConfig.HSTS_MAX_AGE}; includeSubDomains; preload",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Content-Security-Policy": "default-src 'self'",
        }
```

**Infrastructure (ALB):**

```hcl
# terraform/alb.tf
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"  # TLS 1.3
  certificate_arn   = aws_acm_certificate.main.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# Redirect HTTP to HTTPS
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      protocol    = "HTTPS"
      port        = "443"
      status_code = "HTTP_301"
    }
  }
}
```

### Control 2: Access Control

#### Multi-Factor Authentication (MFA)

**Requirement Mapping:**
- SOC 2: CC6.1
- HIPAA: 164.312(d)
- PCI-DSS: Req 8.3 (enhanced in 4.0)
- GDPR: Article 32

**Implementation (AWS IAM):**

```hcl
# terraform/iam_mfa_policy.tf
# Require MFA for all IAM users
resource "aws_iam_policy" "require_mfa" {
  name        = "RequireMFAPolicy"
  description = "Deny all actions except MFA management if MFA not enabled"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "DenyAllExceptMFAManagementIfMFANotEnabled"
        Effect = "Deny"
        NotAction = [
          "iam:CreateVirtualMFADevice",
          "iam:EnableMFADevice",
          "iam:GetUser",
          "iam:ListMFADevices",
          "iam:ListVirtualMFADevices",
          "iam:ResyncMFADevice",
          "sts:GetSessionToken"
        ]
        Resource = "*"
        Condition = {
          BoolIfExists = {
            "aws:MultiFactorAuthPresent" = "false"
          }
        }
      }
    ]
  })
}

# Attach to all users
resource "aws_iam_user_policy_attachment" "mfa_all_users" {
  for_each   = toset(var.iam_users)
  user       = each.value
  policy_arn = aws_iam_policy.require_mfa.arn
}

# Require MFA for console access
resource "aws_iam_policy" "require_mfa_console" {
  name        = "RequireMFAConsolePolicy"
  description = "Require MFA for console login"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "DenyConsoleAccessWithoutMFA"
        Effect = "Deny"
        Action = "*"
        Resource = "*"
        Condition = {
          BoolIfExists = {
            "aws:MultiFactorAuthPresent" = "false"
          }
          StringEquals = {
            "aws:RequestedRegion" = var.allowed_regions
          }
        }
      }
    ]
  })
}
```

**Application-Level MFA (TOTP):**

```python
# api/auth/mfa.py
import pyotp
import qrcode
from io import BytesIO
from typing import Optional

class MFAService:
    """Multi-Factor Authentication service"""

    @staticmethod
    def generate_secret() -> str:
        """Generate TOTP secret for user"""
        return pyotp.random_base32()

    @staticmethod
    def get_provisioning_uri(secret: str, user_email: str, issuer: str) -> str:
        """Get provisioning URI for QR code"""
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=user_email, issuer_name=issuer)

    @staticmethod
    def generate_qr_code(provisioning_uri: str) -> bytes:
        """Generate QR code image"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()

    @staticmethod
    def verify_token(secret: str, token: str, window: int = 1) -> bool:
        """
        Verify TOTP token

        Args:
            secret: User's TOTP secret
            token: 6-digit token from authenticator app
            window: Time window for validity (default 1 = ±30 seconds)
        """
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=window)

    @staticmethod
    def generate_backup_codes(count: int = 10) -> list[str]:
        """Generate one-time backup codes"""
        import secrets
        return [secrets.token_hex(4).upper() for _ in range(count)]
```

#### Role-Based Access Control (RBAC)

**Requirement Mapping:**
- SOC 2: CC6.1, CC6.2
- HIPAA: 164.312(a)(2)(i)
- PCI-DSS: Req 7.1
- GDPR: Article 32

**Implementation (Kubernetes RBAC):**

```yaml
# k8s/rbac/developer-role.yaml
# Developer role - read/write in dev namespace only
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
  namespace: development
  labels:
    compliance: "soc2-hipaa"
rules:
- apiGroups: ["", "apps", "batch"]
  resources: ["pods", "deployments", "jobs", "services", "configmaps"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list"]  # Read-only for secrets

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-binding
  namespace: development
subjects:
- kind: Group
  name: developers
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io

---
# Production role - read-only
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer-production-readonly
  namespace: production
  labels:
    compliance: "soc2-hipaa-pci"
rules:
- apiGroups: ["", "apps"]
  resources: ["pods", "deployments", "services"]
  verbs: ["get", "list", "watch"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-production-binding
  namespace: production
subjects:
- kind: Group
  name: developers
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer-production-readonly
  apiGroup: rbac.authorization.k8s.io
```

**Policy Validation (OPA for Kubernetes):**

```rego
# policies/k8s_rbac.rego
package kubernetes.admission

# Deny RoleBindings that grant cluster-admin to service accounts
deny[msg] {
  input.request.kind.kind == "RoleBinding"
  input.request.object.roleRef.name == "cluster-admin"
  subject := input.request.object.subjects[_]
  subject.kind == "ServiceAccount"

  msg := sprintf("Service account '%s' cannot be granted cluster-admin role", [subject.name])
}

# Require approval annotation for production namespace access
deny[msg] {
  input.request.kind.kind == "RoleBinding"
  input.request.namespace == "production"
  not input.request.object.metadata.annotations["approved-by"]

  msg := "Production RoleBinding requires 'approved-by' annotation"
}

# Deny wildcard permissions in production
deny[msg] {
  input.request.kind.kind == "Role"
  input.request.namespace == "production"
  rule := input.request.object.rules[_]
  rule.verbs[_] == "*"

  msg := "Wildcard verbs not allowed in production Role"
}
```

### Control 3: Audit Logging

**Requirement Mapping:**
- SOC 2: CC7.2
- HIPAA: 164.312(b)
- PCI-DSS: Req 10.2
- GDPR: Article 30

**Implementation (Structured Logging):**

```python
# api/logging/audit_logger.py
import logging
import json
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class AuditEventType(Enum):
    """Audit event types for compliance"""
    # Authentication & Authorization
    LOGIN_SUCCESS = "auth.login.success"
    LOGIN_FAILURE = "auth.login.failure"
    LOGOUT = "auth.logout"
    MFA_ENABLED = "auth.mfa.enabled"
    MFA_DISABLED = "auth.mfa.disabled"
    PASSWORD_CHANGED = "auth.password.changed"

    # Data Access
    PHI_ACCESSED = "data.phi.accessed"
    PHI_MODIFIED = "data.phi.modified"
    PHI_DELETED = "data.phi.deleted"
    PHI_EXPORTED = "data.phi.exported"

    # Administrative
    USER_CREATED = "admin.user.created"
    USER_DELETED = "admin.user.deleted"
    ROLE_ASSIGNED = "admin.role.assigned"
    ROLE_REVOKED = "admin.role.revoked"
    CONFIG_CHANGED = "admin.config.changed"

    # Security
    ACCESS_DENIED = "security.access.denied"
    PRIVILEGE_ESCALATION = "security.privilege.escalation"
    SUSPICIOUS_ACTIVITY = "security.suspicious.activity"

class AuditLogger:
    """
    Compliance-focused audit logger

    Logs structured events for SOC 2, HIPAA, PCI-DSS compliance
    """

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(f"audit.{service_name}")
        self.logger.setLevel(logging.INFO)

        # JSON formatter for structured logs
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

    def log_event(
        self,
        event_type: AuditEventType,
        user_id: Optional[str],
        resource_type: Optional[str],
        resource_id: Optional[str],
        action: str,
        result: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Log audit event in structured format

        Required fields for compliance:
        - Timestamp (ISO 8601)
        - Event type
        - User identification
        - Action performed
        - Result (success/failure)
        - Resource accessed
        - Source IP
        """
        audit_event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": self.service_name,
            "event_type": event_type.value,
            "user_id": user_id,
            "action": action,
            "result": result,
            "resource": {
                "type": resource_type,
                "id": resource_id
            },
            "source": {
                "ip": ip_address,
                "user_agent": user_agent
            },
            "metadata": metadata or {}
        }

        self.logger.info(json.dumps(audit_event))

    def log_phi_access(
        self,
        user_id: str,
        patient_id: str,
        action: str,
        result: str,
        ip_address: str,
        reason: Optional[str] = None
    ):
        """HIPAA-specific: Log PHI access"""
        self.log_event(
            event_type=AuditEventType.PHI_ACCESSED,
            user_id=user_id,
            resource_type="patient_record",
            resource_id=patient_id,
            action=action,
            result=result,
            ip_address=ip_address,
            metadata={"access_reason": reason, "hipaa_audit": True}
        )

    def log_authentication(
        self,
        user_id: str,
        success: bool,
        ip_address: str,
        user_agent: str,
        mfa_used: bool = False
    ):
        """Log authentication attempt"""
        event_type = AuditEventType.LOGIN_SUCCESS if success else AuditEventType.LOGIN_FAILURE

        self.log_event(
            event_type=event_type,
            user_id=user_id,
            resource_type="session",
            resource_id=None,
            action="authenticate",
            result="success" if success else "failure",
            ip_address=ip_address,
            user_agent=user_agent,
            metadata={"mfa_used": mfa_used}
        )

# Usage example
audit = AuditLogger("patient-api")

def get_patient_record(patient_id: str, user_id: str, request):
    """Example: Accessing patient record"""
    try:
        # Business logic here
        record = fetch_patient_record(patient_id)

        # Audit log
        audit.log_phi_access(
            user_id=user_id,
            patient_id=patient_id,
            action="read",
            result="success",
            ip_address=request.client.host,
            reason="Treatment"
        )

        return record
    except PermissionError:
        audit.log_event(
            event_type=AuditEventType.ACCESS_DENIED,
            user_id=user_id,
            resource_type="patient_record",
            resource_id=patient_id,
            action="read",
            result="denied",
            ip_address=request.client.host
        )
        raise
```

**Log Retention (Terraform):**

```hcl
# terraform/cloudwatch_logs.tf
# Audit logs with compliance retention
resource "aws_cloudwatch_log_group" "audit" {
  name              = "/compliance/audit-logs"
  retention_in_days = 2555  # 7 years (PCI-DSS, SOC 2)
  kms_key_id        = aws_kms_key.logs.arn

  tags = {
    Compliance = "SOC2-HIPAA-PCI-GDPR"
    DataClass  = "audit"
  }
}

# Immutable audit trail (S3 with Object Lock)
resource "aws_s3_bucket" "audit_logs" {
  bucket = "company-audit-logs-${var.account_id}"
}

resource "aws_s3_bucket_versioning" "audit_logs" {
  bucket = aws_s3_bucket.audit_logs.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_object_lock_configuration" "audit_logs" {
  bucket = aws_s3_bucket.audit_logs.id

  rule {
    default_retention {
      mode = "COMPLIANCE"  # Immutable
      years = 7
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "audit_logs" {
  bucket = aws_s3_bucket.audit_logs.id

  rule {
    id     = "archive-old-logs"
    status = "Enabled"

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    transition {
      days          = 365
      storage_class = "DEEP_ARCHIVE"
    }
  }
}
```

---

## Compliance as Code Patterns

### Pattern 1: Policy as Code with OPA

**Use Case:** Enforce compliance policies in CI/CD pipeline before infrastructure deployment.

**Architecture:**

```
Developer → Git Push → CI/CD Pipeline
                            ├─► Terraform Plan
                            ├─► Convert Plan to JSON
                            ├─► OPA Policy Evaluation
                            │     ├─► Pass → Deploy
                            │     └─► Fail → Block + Alert
                            └─► Evidence Collection
```

**OPA Policy Structure:**

```rego
# policies/compliance/main.rego
package compliance.main

import data.compliance.encryption
import data.compliance.access_control
import data.compliance.networking
import data.compliance.logging

# Aggregate all policy violations
deny[msg] {
  msg := encryption.deny[_]
}

deny[msg] {
  msg := access_control.deny[_]
}

deny[msg] {
  msg := networking.deny[_]
}

deny[msg] {
  msg := logging.deny[_]
}

# Policy metadata for reporting
policies[policy] {
  policy := {
    "name": "Encryption at Rest",
    "frameworks": ["SOC2", "HIPAA", "GDPR"],
    "severity": "critical"
  }
}
```

**Encryption Policy (OPA):**

```rego
# policies/compliance/encryption.rego
package compliance.encryption

# METADATA
# title: Encryption at Rest
# description: Ensure all data stores use encryption at rest
# frameworks:
#   - SOC 2 (CC6.1)
#   - HIPAA (164.312(a)(2)(iv))
#   - PCI-DSS (Req 3.4)
#   - GDPR (Article 32)

# Deny S3 buckets without encryption
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket"
  not has_bucket_encryption(resource.address)

  msg := sprintf(
    "CRITICAL: S3 bucket '%s' must have encryption enabled (SOC2:CC6.1, HIPAA:164.312(a)(2)(iv))",
    [resource.address]
  )
}

has_bucket_encryption(bucket_address) {
  encryption_resource := input.resource_changes[_]
  encryption_resource.type == "aws_s3_bucket_server_side_encryption_configuration"
  startswith(encryption_resource.address, bucket_address)
}

# Deny RDS without encryption
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_db_instance"
  resource.change.after.storage_encrypted != true

  msg := sprintf(
    "CRITICAL: RDS instance '%s' must enable storage_encrypted (HIPAA:164.312(a)(2)(iv), PCI-DSS:Req3.4)",
    [resource.address]
  )
}

# Require KMS encryption (not default)
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket_server_side_encryption_configuration"
  rule := resource.change.after.rule[_]
  encryption := rule.apply_server_side_encryption_by_default
  encryption.sse_algorithm != "aws:kms"

  msg := sprintf(
    "HIGH: Bucket '%s' must use KMS encryption, not default AES256 (SOC2:CC6.7)",
    [resource.address]
  )
}

# Require key rotation for KMS keys
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_kms_key"
  resource.change.after.enable_key_rotation != true

  msg := sprintf(
    "MEDIUM: KMS key '%s' must have rotation enabled (PCI-DSS:Req3.6)",
    [resource.address]
  )
}
```

**Access Control Policy (OPA):**

```rego
# policies/compliance/access_control.rego
package compliance.access_control

# METADATA
# title: Access Control
# description: Enforce least privilege and MFA requirements
# frameworks:
#   - SOC 2 (CC6.1, CC6.2)
#   - HIPAA (164.312(a)(2)(i))
#   - PCI-DSS (Req 7.1, 8.3)

# Deny IAM policies with wildcard resources
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_iam_policy"
  policy := json.unmarshal(resource.change.after.policy)
  statement := policy.Statement[_]
  statement.Resource == "*"
  statement.Effect == "Allow"
  not is_allowed_wildcard_action(statement.Action)

  msg := sprintf(
    "HIGH: IAM policy '%s' grants overly broad permissions with Resource='*' (SOC2:CC6.2)",
    [resource.address]
  )
}

is_allowed_wildcard_action(actions) {
  # Allow specific read-only wildcards
  allowed := {"s3:List*", "ec2:Describe*", "cloudwatch:Get*"}
  actions[_] == allowed[_]
}

# Require MFA for privileged roles
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_iam_role"
  is_privileged_role(resource)
  policy := json.unmarshal(resource.change.after.assume_role_policy)
  not requires_mfa(policy)

  msg := sprintf(
    "CRITICAL: Privileged role '%s' must require MFA (PCI-DSS:Req8.3)",
    [resource.address]
  )
}

is_privileged_role(resource) {
  # Define what constitutes a privileged role
  privileged_keywords := ["admin", "power", "elevated"]
  contains(lower(resource.name), privileged_keywords[_])
}

requires_mfa(policy) {
  statement := policy.Statement[_]
  statement.Condition.Bool["aws:MultiFactorAuthPresent"] == "true"
}

# Deny overly permissive security groups
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_security_group_rule"
  resource.change.after.type == "ingress"
  resource.change.after.cidr_blocks[_] == "0.0.0.0/0"
  resource.change.after.from_port != 443
  resource.change.after.from_port != 80

  msg := sprintf(
    "HIGH: Security group rule '%s' allows ingress from 0.0.0.0/0 on non-standard port (PCI-DSS:Req1.3)",
    [resource.address]
  )
}
```

**CI/CD Integration (GitLab CI):**

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - plan
  - compliance-check
  - deploy

variables:
  TF_ROOT: ${CI_PROJECT_DIR}/terraform
  OPA_VERSION: "0.59.0"

terraform:validate:
  stage: validate
  image: hashicorp/terraform:1.6
  script:
    - cd ${TF_ROOT}
    - terraform init -backend=false
    - terraform validate
    - terraform fmt -check

terraform:plan:
  stage: plan
  image: hashicorp/terraform:1.6
  script:
    - cd ${TF_ROOT}
    - terraform init
    - terraform plan -out=tfplan.binary
    - terraform show -json tfplan.binary > tfplan.json
  artifacts:
    paths:
      - ${TF_ROOT}/tfplan.json
      - ${TF_ROOT}/tfplan.binary
    expire_in: 1 hour

compliance:opa-check:
  stage: compliance-check
  image: openpolicyagent/opa:${OPA_VERSION}
  dependencies:
    - terraform:plan
  script:
    # Run OPA policy evaluation
    - opa eval \
        --data policies/ \
        --input ${TF_ROOT}/tfplan.json \
        --format pretty \
        'data.compliance.main.deny' > opa-violations.txt

    # Check for violations
    - |
      if [ -s opa-violations.txt ]; then
        echo "❌ Compliance violations detected:"
        cat opa-violations.txt
        exit 1
      else
        echo "✅ All compliance checks passed"
      fi
  artifacts:
    paths:
      - opa-violations.txt
    when: always
  allow_failure: false  # Block deployment on policy violations

compliance:checkov-scan:
  stage: compliance-check
  image: bridgecrew/checkov:latest
  script:
    - checkov -d ${TF_ROOT} \
        --framework terraform \
        --output cli \
        --output junitxml \
        --output-file-path console,checkov-report.xml \
        --soft-fail  # Report but don't fail (OPA is primary gate)
  artifacts:
    reports:
      junit: checkov-report.xml
    paths:
      - checkov-report.xml
    when: always

deploy:production:
  stage: deploy
  image: hashicorp/terraform:1.6
  dependencies:
    - terraform:plan
  script:
    - cd ${TF_ROOT}
    - terraform init
    - terraform apply tfplan.binary
  only:
    - main
  when: manual  # Require manual approval
  environment:
    name: production
```

### Pattern 2: Checkov for IaC Scanning

**Custom Policy Example (YAML):**

```yaml
# policies/checkov/hipaa_phi_tagging.yaml
# Ensure resources handling PHI are properly tagged
metadata:
  name: "Ensure PHI resources are tagged"
  id: "CUSTOM_HIPAA_1"
  category: "HIPAA"
  severity: "HIGH"
  frameworks:
    - HIPAA

definition:
  cond_type: "attribute"
  resource_types:
    - "aws_s3_bucket"
    - "aws_rds_db_instance"
    - "aws_dynamodb_table"
  attribute: "tags.DataClassification"
  operator: "contains"
  value: "PHI"
```

**Custom Policy Example (Python):**

```python
# policies/checkov/hipaa_backup_check.py
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories

class HIPAABackupRetention(BaseResourceCheck):
    """
    Ensure backup retention meets HIPAA requirements (6 years)
    HIPAA: 164.308(a)(7)(ii)(A) - Data Backup Plan
    """

    def __init__(self):
        name = "Ensure backup retention meets HIPAA requirements"
        id = "CUSTOM_HIPAA_2"
        supported_resources = ["aws_db_instance", "aws_backup_plan"]
        categories = [CheckCategories.BACKUP_AND_RECOVERY]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        """
        Check if backup retention >= 6 years (2190 days)
        """
        if conf.get("backup_retention_period"):
            # RDS backup_retention_period (days)
            retention_days = conf["backup_retention_period"][0]
            if retention_days >= 2190:  # 6 years
                return CheckResult.PASSED
            return CheckResult.FAILED

        if conf.get("rule"):
            # AWS Backup Plan rules
            for rule in conf["rule"]:
                lifecycle = rule.get("lifecycle", [{}])[0]
                delete_after = lifecycle.get("delete_after", [0])[0]
                if delete_after >= 2190:
                    return CheckResult.PASSED
            return CheckResult.FAILED

        return CheckResult.UNKNOWN

check = HIPAABackupRetention()
```

**Checkov Execution:**

```bash
# Scan with custom policies
checkov -d ./terraform \
  --framework terraform \
  --external-checks-dir ./policies/checkov \
  --output cli \
  --output json \
  --output-file-path console,checkov-results.json \
  --compact \
  --quiet

# Scan with specific compliance frameworks
checkov -d ./terraform \
  --framework terraform \
  --check HIPAA \
  --check PCI \
  --check SOC2

# Terraform plan scanning
terraform plan -out=tfplan.binary
terraform show -json tfplan.binary > tfplan.json
checkov -f tfplan.json \
  --repo-root-for-plan-enrichment ./terraform
```

### Pattern 3: Automated Compliance Testing

**Pytest Integration:**

```python
# tests/compliance/test_encryption.py
import pytest
import json
import subprocess

@pytest.fixture
def terraform_plan():
    """Generate Terraform plan for testing"""
    subprocess.run(["terraform", "init"], cwd="terraform", check=True)
    subprocess.run(
        ["terraform", "plan", "-out=tfplan.binary"],
        cwd="terraform",
        check=True
    )
    result = subprocess.run(
        ["terraform", "show", "-json", "tfplan.binary"],
        cwd="terraform",
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)

def test_s3_buckets_encrypted(terraform_plan):
    """SOC2:CC6.1, HIPAA:164.312(a)(2)(iv) - All S3 buckets must be encrypted"""
    buckets = [
        r for r in terraform_plan["resource_changes"]
        if r["type"] == "aws_s3_bucket"
    ]

    encrypted_buckets = [
        r for r in terraform_plan["resource_changes"]
        if r["type"] == "aws_s3_bucket_server_side_encryption_configuration"
    ]

    bucket_addresses = {b["address"] for b in buckets}
    encrypted_addresses = {
        e["address"].replace("_server_side_encryption_configuration", "")
        for e in encrypted_buckets
    }

    unencrypted = bucket_addresses - encrypted_addresses
    assert not unencrypted, f"Unencrypted S3 buckets found: {unencrypted}"

def test_rds_encrypted(terraform_plan):
    """HIPAA:164.312(a)(2)(iv), PCI-DSS:Req3.4 - All RDS instances must be encrypted"""
    rds_instances = [
        r for r in terraform_plan["resource_changes"]
        if r["type"] == "aws_db_instance" and r["change"]["actions"] != ["delete"]
    ]

    for instance in rds_instances:
        encrypted = instance["change"]["after"].get("storage_encrypted")
        assert encrypted is True, f"RDS instance {instance['address']} is not encrypted"

def test_kms_rotation_enabled(terraform_plan):
    """PCI-DSS:Req3.6 - KMS keys must have rotation enabled"""
    kms_keys = [
        r for r in terraform_plan["resource_changes"]
        if r["type"] == "aws_kms_key" and r["change"]["actions"] != ["delete"]
    ]

    for key in kms_keys:
        rotation = key["change"]["after"].get("enable_key_rotation")
        assert rotation is True, f"KMS key {key['address']} does not have rotation enabled"

def test_opa_compliance_policies():
    """Run OPA policy evaluation"""
    result = subprocess.run(
        [
            "opa", "eval",
            "--data", "policies/",
            "--input", "terraform/tfplan.json",
            "--format", "values",
            "data.compliance.main.deny"
        ],
        capture_output=True,
        text=True
    )

    violations = json.loads(result.stdout)
    assert not violations, f"OPA policy violations: {violations}"

def test_checkov_compliance():
    """Run Checkov compliance scan"""
    result = subprocess.run(
        [
            "checkov", "-d", "terraform",
            "--framework", "terraform",
            "--compact",
            "--quiet",
            "--soft-fail"
        ],
        capture_output=True,
        text=True
    )

    # Parse Checkov output for failed checks
    output = result.stdout
    assert "Failed checks: 0" in output or result.returncode == 0
```

---

## Evidence Collection Automation

### Pattern 1: Continuous Compliance Dashboard

**Architecture:**

```
AWS Config → EventBridge → Lambda → S3 (Evidence Store)
                                   → DynamoDB (Control Status)
                                   → QuickSight (Dashboard)
```

**Lambda Function (Evidence Collector):**

```python
# lambda/evidence_collector.py
import json
import boto3
from datetime import datetime, timedelta
from typing import Dict, List, Any

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
config = boto3.client('config')
iam = boto3.client('iam')
cloudtrail = boto3.client('cloudtrail')

EVIDENCE_BUCKET = "company-compliance-evidence"
CONTROL_TABLE = "compliance-controls"

class EvidenceCollector:
    """Automated evidence collection for compliance audits"""

    def collect_encryption_evidence(self) -> Dict[str, Any]:
        """
        SOC2:CC6.1, HIPAA:164.312(a)(2)(iv)
        Evidence: All data stores are encrypted
        """
        evidence = {
            "control_id": "ENC-001",
            "control_name": "Encryption at Rest",
            "frameworks": ["SOC2-CC6.1", "HIPAA-164.312(a)(2)(iv)", "PCI-DSS-Req3.4"],
            "timestamp": datetime.utcnow().isoformat(),
            "evidence_type": "configuration_snapshot",
            "status": "PASS",
            "findings": []
        }

        # Check S3 encryption
        s3_resources = config.select_resource_config(
            Expression="SELECT * WHERE resourceType = 'AWS::S3::Bucket'"
        )

        for resource in s3_resources["Results"]:
            resource_config = json.loads(resource)
            bucket_name = resource_config["resourceName"]

            # Check encryption configuration
            try:
                encryption = s3.get_bucket_encryption(Bucket=bucket_name)
                evidence["findings"].append({
                    "resource": f"s3://{bucket_name}",
                    "status": "COMPLIANT",
                    "encryption": encryption["ServerSideEncryptionConfiguration"]
                })
            except s3.exceptions.ServerSideEncryptionConfigurationNotFoundError:
                evidence["findings"].append({
                    "resource": f"s3://{bucket_name}",
                    "status": "NON_COMPLIANT",
                    "issue": "No encryption configured"
                })
                evidence["status"] = "FAIL"

        # Check RDS encryption
        rds_resources = config.select_resource_config(
            Expression="SELECT * WHERE resourceType = 'AWS::RDS::DBInstance'"
        )

        for resource in rds_resources["Results"]:
            resource_config = json.loads(resource)
            db_identifier = resource_config["resourceName"]
            encrypted = resource_config.get("configuration", {}).get("storageEncrypted")

            evidence["findings"].append({
                "resource": f"rds://{db_identifier}",
                "status": "COMPLIANT" if encrypted else "NON_COMPLIANT",
                "encrypted": encrypted
            })

            if not encrypted:
                evidence["status"] = "FAIL"

        return evidence

    def collect_mfa_evidence(self) -> Dict[str, Any]:
        """
        SOC2:CC6.1, PCI-DSS:Req8.3
        Evidence: MFA enforced for all users
        """
        evidence = {
            "control_id": "IAM-001",
            "control_name": "Multi-Factor Authentication",
            "frameworks": ["SOC2-CC6.1", "PCI-DSS-Req8.3", "HIPAA-164.312(d)"],
            "timestamp": datetime.utcnow().isoformat(),
            "evidence_type": "user_configuration",
            "status": "PASS",
            "findings": []
        }

        # List all IAM users
        paginator = iam.get_paginator('list_users')
        for page in paginator.paginate():
            for user in page['Users']:
                username = user['UserName']

                # Check MFA devices
                mfa_devices = iam.list_mfa_devices(UserName=username)
                has_mfa = len(mfa_devices['MFADevices']) > 0

                evidence["findings"].append({
                    "user": username,
                    "mfa_enabled": has_mfa,
                    "status": "COMPLIANT" if has_mfa else "NON_COMPLIANT"
                })

                if not has_mfa:
                    evidence["status"] = "FAIL"

        return evidence

    def collect_access_log_evidence(self) -> Dict[str, Any]:
        """
        SOC2:CC7.2, HIPAA:164.312(b), PCI-DSS:Req10.2
        Evidence: Access logs are captured and retained
        """
        evidence = {
            "control_id": "LOG-001",
            "control_name": "Access Logging",
            "frameworks": ["SOC2-CC7.2", "HIPAA-164.312(b)", "PCI-DSS-Req10.2"],
            "timestamp": datetime.utcnow().isoformat(),
            "evidence_type": "logging_configuration",
            "status": "PASS",
            "findings": []
        }

        # Check CloudTrail trails
        trails = cloudtrail.list_trails()
        for trail_arn in trails['Trails']:
            trail_name = trail_arn['Name']
            trail_status = cloudtrail.get_trail_status(Name=trail_name)

            evidence["findings"].append({
                "trail": trail_name,
                "logging_enabled": trail_status['IsLogging'],
                "status": "COMPLIANT" if trail_status['IsLogging'] else "NON_COMPLIANT"
            })

            if not trail_status['IsLogging']:
                evidence["status"] = "FAIL"

        # Check VPC Flow Logs
        ec2 = boto3.client('ec2')
        vpcs = ec2.describe_vpcs()

        for vpc in vpcs['Vpcs']:
            vpc_id = vpc['VpcId']
            flow_logs = ec2.describe_flow_logs(
                Filters=[{'Name': 'resource-id', 'Values': [vpc_id]}]
            )

            has_flow_logs = len(flow_logs['FlowLogs']) > 0
            evidence["findings"].append({
                "vpc": vpc_id,
                "flow_logs_enabled": has_flow_logs,
                "status": "COMPLIANT" if has_flow_logs else "NON_COMPLIANT"
            })

            if not has_flow_logs:
                evidence["status"] = "FAIL"

        return evidence

    def store_evidence(self, evidence: Dict[str, Any]):
        """Store evidence in S3 and update control status"""
        # Store in S3 (immutable evidence)
        date_path = datetime.utcnow().strftime("%Y/%m/%d")
        evidence_key = f"evidence/{date_path}/{evidence['control_id']}-{evidence['timestamp']}.json"

        s3.put_object(
            Bucket=EVIDENCE_BUCKET,
            Key=evidence_key,
            Body=json.dumps(evidence, indent=2),
            ServerSideEncryption='aws:kms',
            Metadata={
                'control-id': evidence['control_id'],
                'status': evidence['status'],
                'frameworks': ','.join(evidence['frameworks'])
            }
        )

        # Update control status in DynamoDB
        table = dynamodb.Table(CONTROL_TABLE)
        table.put_item(
            Item={
                'control_id': evidence['control_id'],
                'timestamp': evidence['timestamp'],
                'status': evidence['status'],
                'evidence_location': f"s3://{EVIDENCE_BUCKET}/{evidence_key}",
                'frameworks': evidence['frameworks'],
                'findings_count': len(evidence['findings']),
                'ttl': int((datetime.utcnow() + timedelta(days=2555)).timestamp())  # 7 years
            }
        )

def lambda_handler(event, context):
    """Lambda handler for scheduled evidence collection"""
    collector = EvidenceCollector()

    # Collect evidence for all controls
    evidence_items = [
        collector.collect_encryption_evidence(),
        collector.collect_mfa_evidence(),
        collector.collect_access_log_evidence()
    ]

    # Store evidence
    for evidence in evidence_items:
        collector.store_evidence(evidence)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Evidence collection complete',
            'controls_checked': len(evidence_items)
        })
    }
```

**EventBridge Schedule (Terraform):**

```hcl
# terraform/evidence_collection.tf
resource "aws_cloudwatch_event_rule" "daily_evidence" {
  name                = "daily-compliance-evidence-collection"
  description         = "Trigger daily evidence collection"
  schedule_expression = "cron(0 2 * * ? *)"  # 2 AM UTC daily
}

resource "aws_cloudwatch_event_target" "evidence_lambda" {
  rule      = aws_cloudwatch_event_rule.daily_evidence.name
  target_id = "EvidenceCollectorLambda"
  arn       = aws_lambda_function.evidence_collector.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.evidence_collector.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_evidence.arn
}
```

### Pattern 2: Audit Report Generation

**Automated Report Script:**

```python
# scripts/generate_audit_report.py
import boto3
import json
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

EVIDENCE_BUCKET = "company-compliance-evidence"
CONTROL_TABLE = "compliance-controls"

class AuditReportGenerator:
    """Generate compliance audit reports"""

    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date
        self.table = dynamodb.Table(CONTROL_TABLE)

    def get_control_status(self, framework: str) -> Dict[str, List]:
        """Get control status for framework"""
        response = self.table.scan(
            FilterExpression="contains(frameworks, :framework)",
            ExpressionAttributeValues={":framework": framework}
        )

        controls = defaultdict(list)
        for item in response['Items']:
            controls[item['control_id']].append(item)

        return controls

    def calculate_compliance_score(self, controls: Dict) -> float:
        """Calculate compliance percentage"""
        total = 0
        passed = 0

        for control_id, items in controls.items():
            # Get most recent evidence
            latest = max(items, key=lambda x: x['timestamp'])
            total += 1
            if latest['status'] == 'PASS':
                passed += 1

        return (passed / total * 100) if total > 0 else 0

    def generate_soc2_report(self) -> Dict:
        """Generate SOC 2 Type II report"""
        controls = self.get_control_status("SOC2")

        report = {
            "framework": "SOC 2 Type II",
            "report_period": {
                "start": self.start_date.isoformat(),
                "end": self.end_date.isoformat()
            },
            "generated_at": datetime.utcnow().isoformat(),
            "compliance_score": self.calculate_compliance_score(controls),
            "trust_services_criteria": {
                "security": self._assess_tsc("security", controls),
                "availability": self._assess_tsc("availability", controls),
                "confidentiality": self._assess_tsc("confidentiality", controls)
            },
            "controls": self._format_controls(controls)
        }

        return report

    def generate_hipaa_report(self) -> Dict:
        """Generate HIPAA compliance report"""
        controls = self.get_control_status("HIPAA")

        report = {
            "framework": "HIPAA",
            "report_period": {
                "start": self.start_date.isoformat(),
                "end": self.end_date.isoformat()
            },
            "generated_at": datetime.utcnow().isoformat(),
            "compliance_score": self.calculate_compliance_score(controls),
            "safeguards": {
                "administrative": self._assess_safeguard("admin", controls),
                "physical": self._assess_safeguard("physical", controls),
                "technical": self._assess_safeguard("technical", controls)
            },
            "controls": self._format_controls(controls)
        }

        return report

    def _assess_tsc(self, category: str, controls: Dict) -> Dict:
        """Assess Trust Services Criteria category"""
        relevant_controls = {
            k: v for k, v in controls.items()
            if category.upper() in k
        }
        return {
            "total_controls": len(relevant_controls),
            "passed": sum(1 for items in relevant_controls.values()
                         if max(items, key=lambda x: x['timestamp'])['status'] == 'PASS'),
            "compliance": self.calculate_compliance_score(relevant_controls)
        }

    def _assess_safeguard(self, category: str, controls: Dict) -> Dict:
        """Assess HIPAA safeguard category"""
        # Similar to _assess_tsc
        return self._assess_tsc(category, controls)

    def _format_controls(self, controls: Dict) -> List[Dict]:
        """Format control details for report"""
        formatted = []
        for control_id, items in controls.items():
            latest = max(items, key=lambda x: x['timestamp'])
            formatted.append({
                "control_id": control_id,
                "status": latest['status'],
                "last_checked": latest['timestamp'],
                "evidence_location": latest['evidence_location'],
                "findings_count": latest.get('findings_count', 0)
            })
        return formatted

    def export_report(self, report: Dict, filename: str):
        """Export report to S3"""
        report_key = f"reports/{datetime.utcnow().strftime('%Y/%m')}/{filename}"

        s3.put_object(
            Bucket=EVIDENCE_BUCKET,
            Key=report_key,
            Body=json.dumps(report, indent=2),
            ServerSideEncryption='aws:kms',
            ContentType='application/json'
        )

        print(f"Report exported to s3://{EVIDENCE_BUCKET}/{report_key}")

# Usage
if __name__ == "__main__":
    # Generate report for last 6 months
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=180)

    generator = AuditReportGenerator(start_date, end_date)

    # SOC 2 report
    soc2_report = generator.generate_soc2_report()
    generator.export_report(soc2_report, "soc2-report.json")
    print(f"SOC 2 Compliance Score: {soc2_report['compliance_score']:.2f}%")

    # HIPAA report
    hipaa_report = generator.generate_hipaa_report()
    generator.export_report(hipaa_report, "hipaa-report.json")
    print(f"HIPAA Compliance Score: {hipaa_report['compliance_score']:.2f}%")
```

---

## Control Mapping Matrix

### Unified Control Framework

This matrix shows how to implement a single control that satisfies multiple framework requirements:

| Control Category | SOC 2 | HIPAA | PCI-DSS 4.0 | GDPR | ISO 27001 | Implementation |
|------------------|-------|-------|-------------|------|-----------|----------------|
| **Identity & Access** | | | | | | |
| Multi-Factor Authentication | CC6.1 | §164.312(d) | Req 8.3 | Art 32(1) | A.9.4.2 | AWS IAM MFA, Okta, Auth0 |
| Role-Based Access Control | CC6.2 | §164.312(a)(2)(i) | Req 7.1 | Art 32(1) | A.9.2.3 | AWS IAM Roles, K8s RBAC |
| Least Privilege | CC6.3 | §164.308(a)(3)(ii)(B) | Req 7.1.2 | Art 25 | A.9.2.3 | Policy-based access |
| Access Reviews | CC6.1 | §164.308(a)(3)(ii)(C) | Req 8.2.4 | Art 32(1) | A.9.2.5 | Quarterly access audits |
| Password Policy | CC6.1 | §164.308(a)(5)(ii)(D) | Req 8.3.6 | Art 32(1) | A.9.4.3 | 12+ chars, complexity |
| **Data Protection** | | | | | | |
| Encryption at Rest | CC6.1, CC6.7 | §164.312(a)(2)(iv) | Req 3.4 | Art 32(1)(a) | A.10.1.1 | AES-256, KMS |
| Encryption in Transit | CC6.1, CC6.6 | §164.312(e)(1) | Req 4.1 | Art 32(1)(a) | A.13.1.1 | TLS 1.3 |
| Data Classification | CC6.1 | §164.308(a)(3)(ii)(A) | Req 9.6.1 | Art 30 | A.8.2.1 | Tagging system |
| Data Retention | CC6.7 | §164.316(b)(2) | Req 3.1 | Art 5(1)(e) | A.11.2.7 | Lifecycle policies |
| Data Minimization | - | §164.502(b) | Req 3.2 | Art 5(1)(c) | - | Application logic |
| **Logging & Monitoring** | | | | | | |
| Audit Logging | CC7.2 | §164.312(b) | Req 10.2 | Art 30 | A.12.4.1 | CloudWatch, Splunk |
| Log Retention | CC7.2 | §164.316(b)(2) | Req 10.5.1 | Art 5(1)(e) | A.12.4.1 | 7 years (S3) |
| Log Protection | CC7.2 | §164.312(c)(1) | Req 10.5.2 | Art 32(1) | A.12.4.2 | Immutable logs |
| Security Monitoring | CC7.2, CC7.3 | §164.308(a)(1)(ii)(D) | Req 10.6 | Art 32 | A.12.4.1 | SIEM, alerts |
| **Network Security** | | | | | | |
| Firewall Configuration | CC6.6 | §164.312(a)(2)(ii) | Req 1.2 | Art 32(1) | A.13.1.1 | Security groups, WAF |
| Network Segmentation | CC6.6 | §164.308(a)(3)(ii)(B) | Req 1.3 | Art 32(1) | A.13.1.3 | VPC, subnets |
| Intrusion Detection | CC7.3 | §164.312(b) | Req 11.4 | Art 32 | A.12.6.1 | GuardDuty, IDS |
| **Vulnerability Management** | | | | | | |
| Vulnerability Scanning | CC7.1 | §164.308(a)(8) | Req 11.2 | Art 32 | A.12.6.1 | Inspector, Qualys |
| Patch Management | CC7.1, CC8.1 | §164.308(a)(5)(ii)(B) | Req 6.2 | Art 32 | A.12.6.1 | Systems Manager |
| Secure Development | CC8.1 | - | Req 6.3 | Art 25 | A.14.2 | SAST/DAST, SCA |
| **Incident Response** | | | | | | |
| Incident Detection | CC7.3 | §164.308(a)(6)(i) | Req 12.10.1 | Art 33 | A.16.1.2 | SIEM, monitoring |
| Incident Response Plan | CC7.4, CC7.5 | §164.308(a)(6)(ii) | Req 12.10.1 | Art 33 | A.16.1.5 | Documented procedures |
| Breach Notification | CC7.5 | §164.410 | Req 12.10.6 | Art 33 | A.16.1.2 | 60d (HIPAA), 48h (GDPR) |
| **Business Continuity** | | | | | | |
| Data Backup | CC7.4 | §164.308(a)(7)(ii)(A) | Req 12.10.2 | Art 32(1)(c) | A.12.3.1 | AWS Backup, S3 |
| Disaster Recovery | CC7.4 | §164.308(a)(7)(ii)(C) | Req 12.10.3 | Art 32(1)(c) | A.17.1.1 | Multi-region DR |
| **Governance** | | | | | | |
| Security Policies | CC1.2, CC1.3 | §164.316(a) | Req 12.1 | Art 24 | A.5.1.1 | Policy documents |
| Security Training | CC1.4 | §164.308(a)(5) | Req 12.6 | Art 32(4) | A.7.2.2 | Annual training |
| Vendor Management | CC9.1, CC9.2 | §164.308(b) | Req 12.8 | Art 28 | A.15.1.1 | BAAs, vendor audits |
| Risk Assessments | CC4.1, CC4.2 | §164.308(a)(1) | Req 12.2 | Art 32 | A.12.6.1 | Annual risk analysis |

---

## Tool Recommendations

### Primary Tools

| Category | Tool | Purpose | Frameworks | Trust |
|----------|------|---------|------------|-------|
| **Policy as Code** | Open Policy Agent | Policy enforcement | All | High (1741+ snippets) |
| **IaC Security** | Checkov | Static analysis | All | High (338+ snippets, 90.5 score) |
| **IaC Security** | tfsec | Terraform scanning | All | High |
| **Container Security** | Trivy | Container/IaC scanning | All | High |
| **Compliance Frameworks** | AWS Config | AWS resource compliance | SOC2, HIPAA, PCI-DSS | Native |
| **Compliance Frameworks** | Cloud Custodian | Multi-cloud compliance | All | High |
| **Secret Scanning** | GitGuardian | Secret detection in code | All | High |
| **Vulnerability Scanning** | Snyk | Dependency/container scanning | All | High |

### Supporting Tools

| Category | Tool | Purpose |
|----------|------|---------|
| **Evidence Collection** | Drata, Vanta, Secureframe | Automated compliance monitoring |
| **SIEM** | Splunk, Datadog, Elastic | Log aggregation and analysis |
| **IDS/IPS** | AWS GuardDuty, Cloudflare | Threat detection |
| **Backup** | AWS Backup, Veeam | Data backup and recovery |
| **Encryption** | AWS KMS, HashiCorp Vault | Key management |

---

## Skill Structure Design

```
compliance-frameworks/
├── SKILL.md                                # Main skill (600-800 lines)
├── references/
│   ├── soc2-controls.md                   # SOC 2 control details
│   ├── hipaa-safeguards.md                # HIPAA technical/admin/physical
│   ├── pci-dss-requirements.md            # PCI-DSS 4.0 12 requirements
│   ├── gdpr-articles.md                   # GDPR key articles
│   ├── control-mapping-matrix.md          # Unified control mapping
│   ├── encryption-implementations.md      # Encryption patterns
│   ├── access-control-patterns.md         # IAM, RBAC, MFA
│   ├── audit-logging-patterns.md          # Logging requirements
│   ├── incident-response-templates.md     # IR procedures
│   └── vendor-management.md               # BAAs, DPAs, vendor assessments
├── examples/
│   ├── opa-policies/
│   │   ├── encryption.rego
│   │   ├── access_control.rego
│   │   ├── networking.rego
│   │   └── logging.rego
│   ├── checkov-policies/
│   │   ├── custom_hipaa_checks.py
│   │   └── custom_soc2_checks.yaml
│   ├── terraform/
│   │   ├── encryption_at_rest.tf
│   │   ├── mfa_enforcement.tf
│   │   ├── audit_logging.tf
│   │   └── network_security.tf
│   └── evidence-collection/
│       ├── evidence_collector.py
│       └── report_generator.py
└── scripts/
    ├── run-opa-policies.sh                # Execute OPA validation
    ├── run-checkov-scan.sh                # Execute Checkov scan
    ├── collect-evidence.sh                # Trigger evidence collection
    └── generate-audit-report.sh           # Generate compliance report
```

---

## Integration Points

### With Existing Skills

| Skill | Integration |
|-------|-------------|
| `infrastructure-as-code` | IaC templates implement compliance controls |
| `secret-management` | Secrets handling per HIPAA, PCI-DSS requirements |
| `security-hardening` | Technical security controls implementation |
| `kubernetes-operations` | K8s RBAC, network policies for compliance |
| `building-ci-pipelines` | Policy enforcement in CI/CD |
| `observability` | Audit logging and monitoring requirements |

### Skill Chaining Example

```
compliance-frameworks → infrastructure-as-code → security-hardening
        │                        │                       │
        ▼                        ▼                       ▼
  Define requirements    Implement controls      Harden systems
  (OPA policies)        (Terraform + OPA)       (CIS benchmarks)
```

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
- [x] Research completion
- [ ] Core decision frameworks
- [ ] SOC 2, HIPAA, PCI-DSS, GDPR overviews
- [ ] Control mapping matrix

### Phase 2: Technical Controls (Weeks 5-8)
- [ ] Encryption implementations
- [ ] Access control patterns (MFA, RBAC)
- [ ] Audit logging patterns
- [ ] Network security controls

### Phase 3: Compliance as Code (Weeks 9-12)
- [ ] OPA policy examples (encryption, access, networking, logging)
- [ ] Checkov custom policies
- [ ] CI/CD integration patterns
- [ ] Automated testing

### Phase 4: Evidence & Reporting (Weeks 13-16)
- [ ] Evidence collection automation
- [ ] Compliance dashboards
- [ ] Audit report generation
- [ ] Vendor management templates

### Phase 5: Polish & Integration (Weeks 17-18)
- [ ] Integration with other skills
- [ ] Documentation review
- [ ] Example validation
- [ ] Final testing

---

## Key Takeaways

1. **Compliance is Continuous** - Not a one-time audit, but ongoing engineering discipline
2. **Unified Controls** - Single implementation satisfies multiple frameworks
3. **Policy as Code** - OPA + Checkov enable automated enforcement
4. **Evidence Automation** - Reduce audit prep from weeks to days
5. **Framework Mapping** - Understand control overlap to reduce effort
6. **2025 Updates** - AI governance, shorter breach timelines, enhanced requirements
7. **Zero Trust** - Continuous verification becoming mandatory across frameworks

---

**Progressive disclosure:** This init.md provides the master plan. Detailed framework documentation, control implementations, and policy examples in `references/` and `examples/` directories.
