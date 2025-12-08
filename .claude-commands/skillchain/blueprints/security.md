# Security Hardening Blueprint

**Version:** 1.0.0
**Last Updated:** 2024-12-06
**Category:** Security

---

## Overview

Pre-configured skill chain optimized for implementing comprehensive security hardening, compliance frameworks, authentication/authorization systems, and security monitoring. This blueprint provides production-ready defaults for the most common security patterns, minimizing configuration while maximizing protection.

---

## Trigger Keywords

**Primary (high confidence):**
- security
- hardening
- compliance
- soc2
- zero trust
- secure

**Secondary (medium confidence):**
- authentication
- authorization
- encryption
- firewall
- vulnerability
- pentesting
- audit
- hipaa
- gdpr
- pci-dss

**Example goals that match:**
- "security hardening for production app"
- "implement SOC2 compliance"
- "zero trust security architecture"
- "secure authentication and authorization"
- "security audit and vulnerability scanning"
- "HIPAA compliant data encryption"

---

## Skill Chain (Pre-configured)

This blueprint invokes 7 skills in the following order:

```
1. hardening-security            (core security hardening)
2. implementing-auth-security    (authentication/authorization)
3. managing-secrets              (secret management & rotation)
4. implementing-siem             (security monitoring & logging)
5. building-ci-pipelines         (security scanning in CI/CD)
6. configuring-networking        (network security & firewall)
7. documenting-compliance        (compliance documentation)
```

**Total estimated time:** 40-60 minutes
**Total estimated questions:** 15-20 questions (or 3 with blueprint defaults)

---

## Pre-configured Defaults

### 1. hardening-security
```yaml
security_level: "strict"
  # Enterprise-grade security hardening
  # Defense in depth with multiple layers
  # Zero trust principles applied

os_hardening: true
  # CIS Benchmarks compliance
  # Disable unnecessary services
  # Secure kernel parameters
  # File system hardening (noexec, nosuid)
  # Automatic security updates

container_security: true
  # Non-root containers by default
  # Read-only file systems where possible
  # Minimal base images (distroless preferred)
  # Image scanning for vulnerabilities
  # Runtime security policies (AppArmor/SELinux)

tls_config:
  version: "TLS 1.3"
  # Modern TLS only (1.3 preferred, 1.2 minimum)
  cipher_suites:
    - "TLS_AES_256_GCM_SHA384"
    - "TLS_AES_128_GCM_SHA256"
    - "TLS_CHACHA20_POLY1305_SHA256"
  # Strong cipher suites only
  # Perfect forward secrecy (PFS)
  # HSTS headers enforced

rate_limiting: true
  # Per-IP rate limiting
  # Sliding window algorithm
  # Default: 100 req/min for authenticated
  # Default: 20 req/min for unauthenticated
  # Burst allowance: 20% above limit

cors_policy: "restrictive"
  # Explicit origin whitelist (no wildcards)
  # Credentials allowed only for trusted origins
  # Preflight caching enabled
```

### 2. implementing-auth-security
```yaml
auth_method: "oauth2_oidc"
  # OAuth 2.0 with OpenID Connect
  # Industry standard, widely supported
  # Supports SSO and federated identity

token_type: "jwt"
  # JSON Web Tokens (JWT)
  # Signed with RS256 (asymmetric)
  # Short-lived access tokens (15 min)
  # Long-lived refresh tokens (7 days)
  # Token rotation on refresh

authorization: "rbac"
  # Role-Based Access Control (RBAC)
  # Predefined roles: admin, editor, viewer
  # Fine-grained permissions
  # Least privilege principle
  # Optional: ABAC (Attribute-Based) for complex scenarios

mfa_required: true
  # Multi-factor authentication mandatory
  # TOTP (Time-based One-Time Password)
  # Backup codes provided
  # SMS fallback (optional, not recommended)

session_management:
  timeout: "30m"
  # Idle timeout: 30 minutes
  # Absolute timeout: 8 hours
  # Concurrent session limit: 3
  # Session fixation protection
  # Secure, HttpOnly, SameSite=Strict cookies

password_policy:
  min_length: 12
  # Minimum 12 characters
  # Complexity: uppercase, lowercase, number, special
  # No common passwords (10k most common blocked)
  # Password history: last 5 not reusable
  # Bcrypt with cost factor 12
```

### 3. managing-secrets
```yaml
secret_storage: "vault"
  # HashiCorp Vault (recommended)
  # Alternative: AWS Secrets Manager, Azure Key Vault
  # Encryption at rest (AES-256)
  # Encryption in transit (TLS 1.3)
  # Audit logging enabled

rotation_policy:
  database_credentials: "90d"
  # Database passwords: 90 days
  api_keys: "180d"
  # API keys: 180 days
  encryption_keys: "365d"
  # Data encryption keys: annually (with versioning)
  tls_certificates: "90d"
  # TLS certs: 90 days (Let's Encrypt 90-day standard)

access_control:
  method: "dynamic_secrets"
  # Dynamic secrets generated on-demand
  # Automatic revocation after TTL
  # No long-lived credentials
  # Principle of least privilege

environment_variables:
  disallow_plaintext: true
  # No secrets in env vars (use secret management)
  # No secrets in code repositories
  # No secrets in CI/CD logs
  # Secrets injected at runtime
```

### 4. implementing-siem
```yaml
logging_standard: "structured_json"
  # JSON-formatted logs for easy parsing
  # Consistent schema across services
  # Correlation IDs for request tracing

security_events:
  - "authentication_attempts"
  - "authorization_failures"
  - "data_access"
  - "privilege_escalation"
  - "configuration_changes"
  - "network_anomalies"
  # Comprehensive security event logging

log_aggregation: "elasticsearch"
  # ELK Stack (Elasticsearch, Logstash, Kibana)
  # Alternative: Splunk, Datadog, Azure Sentinel
  # Centralized log storage
  # Real-time search and analysis
  # Long-term retention (1 year minimum)

alerting:
  channels: ["email", "slack", "pagerduty"]
  # Multiple notification channels
  # Severity-based routing
  # Critical: PagerDuty (immediate)
  # High: Slack + Email (5 min SLA)
  # Medium: Email (1 hour SLA)

siem_rules:
  - "Multiple failed login attempts (5 in 10 min)"
  - "Privilege escalation detected"
  - "Data exfiltration patterns"
  - "Unusual access times/locations"
  - "API rate limit violations"
  - "Configuration drift detection"
```

### 5. building-ci-pipelines
```yaml
security_scanning:
  sast: true
  # Static Application Security Testing
  # Tools: SonarQube, Checkmarx, Semgrep
  # Scan on every commit
  # Block merge if critical vulnerabilities

  dast: true
  # Dynamic Application Security Testing
  # Tools: OWASP ZAP, Burp Suite
  # Scan in staging environment
  # Pre-production gate

  sca: true
  # Software Composition Analysis
  # Tools: Snyk, Dependabot, WhiteSource
  # Dependency vulnerability scanning
  # License compliance checking
  # Automatic PR for dependency updates

  container_scanning: true
  # Image vulnerability scanning
  # Tools: Trivy, Clair, Anchore
  # Scan base images and final images
  # Block deployment if critical CVEs

  secrets_scanning: true
  # Detect secrets in code
  # Tools: TruffleHog, git-secrets, GitGuardian
  # Prevent credential commits
  # Scan commit history

security_gates:
  block_on_critical: true
  # Critical vulnerabilities block deployment
  # High vulnerabilities require approval
  # Medium/Low vulnerabilities tracked
  # Zero-day grace period: 7 days
```

### 6. configuring-networking
```yaml
network_segmentation: "zero_trust"
  # Zero trust network architecture
  # No implicit trust based on network location
  # Micro-segmentation with network policies
  # Least privilege network access

firewall_rules:
  default_policy: "deny_all"
  # Default deny all traffic
  # Explicit allow rules only
  # Egress filtering enabled
  # Rate limiting on public endpoints

ingress_security:
  waf_enabled: true
  # Web Application Firewall
  # OWASP Top 10 protection
  # Custom rule sets
  # Bot detection and mitigation
  # DDoS protection

  load_balancer_security:
    - "SSL/TLS termination"
    - "HTTP to HTTPS redirect"
    - "X-Frame-Options: DENY"
    - "X-Content-Type-Options: nosniff"
    - "Strict-Transport-Security (HSTS)"
    - "Content-Security-Policy (CSP)"

service_mesh: "istio"
  # Mutual TLS (mTLS) between services
  # Traffic encryption by default
  # Service-to-service authentication
  # Circuit breaker patterns
  # Observability (tracing, metrics)

vpn_access:
  required_for: ["production", "staging"]
  # VPN required for infrastructure access
  # IP allowlisting for CI/CD
  # Bastion host for SSH access
  # Certificate-based authentication
```

### 7. documenting-compliance
```yaml
compliance_frameworks:
  - "SOC2 Type II"
  - "ISO 27001"
  # Common frameworks (customize based on Q2)
  # HIPAA (if healthcare)
  # PCI-DSS (if payment processing)
  # GDPR (if EU data)

documentation_required:
  - "Security policies and procedures"
  - "Risk assessment and treatment plans"
  - "Incident response playbooks"
  - "Business continuity plan"
  - "Access control matrix"
  - "Data flow diagrams"
  - "Third-party vendor assessments"
  - "Security training materials"
  - "Audit logs and evidence"

audit_trail:
  retention: "7_years"
  # 7-year log retention for compliance
  # Immutable audit logs
  # Tamper-evident storage
  # Regular compliance audits (quarterly)

security_controls:
  - "Access controls (authentication/authorization)"
  - "Encryption (data at rest and in transit)"
  - "Network security (firewall, segmentation)"
  - "Vulnerability management (scanning, patching)"
  - "Incident response (detection, containment)"
  - "Business continuity (backup, disaster recovery)"
  - "Security awareness training (annual)"
  - "Third-party risk management"
```

---

## Quick Questions (Only 3)

When blueprint is detected, ask only these essential questions:

### Question 1: Primary Security Concern
```
What is your primary security concern?

Options:
1. Authentication & Access Control (identity management, SSO, MFA)
2. Data Protection (encryption, data loss prevention, privacy)
3. Network Security (firewall, DDoS, zero trust)
4. Compliance & Audit (SOC2, HIPAA, GDPR, audit trails)
5. Comprehensive Hardening (all of the above)

Your answer: _______________
```

**Why this matters:**
- Determines skill prioritization and depth
- Focuses effort on highest-risk areas
- Influences default configurations

**Default if skipped:** "5 - Comprehensive Hardening"

---

### Question 2: Compliance Requirements
```
Which compliance frameworks must you meet? (select multiple)

Options:
a. SOC2 Type II (standard for SaaS companies)
b. HIPAA (healthcare data protection)
c. PCI-DSS (payment card processing)
d. GDPR (EU data privacy)
e. ISO 27001 (international security standard)
f. None / Custom requirements

Your answer (comma-separated, e.g., "a,d,e"): _______________
```

**Why this matters:**
- Determines required controls and documentation
- Sets audit log retention periods
- Influences data handling requirements
- Affects third-party vendor requirements

**Default if skipped:** "a,e" (SOC2 + ISO 27001)

---

### Question 3: Infrastructure Type
```
What type of infrastructure are you securing?

Options:
1. Cloud-native (AWS, Azure, GCP - using managed services)
2. Kubernetes/containers (self-managed or managed)
3. Traditional VMs/servers (on-premise or IaaS)
4. Serverless (Lambda, Cloud Functions, Azure Functions)
5. Hybrid (combination of above)

Your answer: _______________
```

**Why this matters:**
- Cloud-native enables managed security services
- Kubernetes requires pod security policies
- Traditional servers need OS hardening
- Serverless has different security model
- Determines tooling and best practices

**Default if skipped:** "1 - Cloud-native"

---

## Blueprint Detection Logic

Trigger this blueprint when the user's goal matches:

```python
def should_use_security_blueprint(goal: str) -> bool:
    goal_lower = goal.lower()

    # Primary keywords (high confidence)
    primary_match = any(keyword in goal_lower for keyword in [
        "security",
        "hardening",
        "compliance",
        "soc2",
        "soc 2",
        "hipaa",
        "zero trust",
        "penetration test",
        "pentest",
        "security audit"
    ])

    # Secondary keywords + security context
    secondary_match = (
        any(keyword in goal_lower for keyword in [
            "authentication",
            "authorization",
            "encryption",
            "firewall",
            "vulnerability"
        ]) and
        any(keyword in goal_lower for keyword in [
            "secure",
            "protect",
            "harden",
            "compliance",
            "audit"
        ])
    )

    # Compliance frameworks
    compliance_match = any(keyword in goal_lower for keyword in [
        "gdpr",
        "pci-dss",
        "pci dss",
        "iso 27001",
        "iso27001",
        "fedramp",
        "nist"
    ])

    return primary_match or secondary_match or compliance_match
```

**Confidence levels:**
- **High (90%+):** Contains "security hardening" or compliance framework
- **Medium (70-89%):** Contains "security" + infrastructure term
- **Low (50-69%):** Contains auth/encryption + protection term

**Present blueprint when confidence >= 70%**

---

## Blueprint Offer Message

When blueprint is detected, present this message to the user:

```
┌────────────────────────────────────────────────────────────┐
│ 🔒 SECURITY HARDENING BLUEPRINT DETECTED                   │
├────────────────────────────────────────────────────────────┤
│ Your goal matches our Security Hardening Blueprint!       │
│                                                            │
│ Pre-configured security layers:                            │
│  ✓ TLS 1.3 with strong cipher suites                      │
│  ✓ OAuth2/OIDC authentication + MFA                       │
│  ✓ RBAC authorization (admin/editor/viewer)               │
│  ✓ HashiCorp Vault secret management                      │
│  ✓ 90-day automatic secret rotation                       │
│  ✓ SIEM with ELK stack (centralized logging)              │
│  ✓ Security scanning in CI/CD pipeline                    │
│  ✓ Zero trust network architecture                        │
│  ✓ SOC2 + ISO 27001 compliance docs                       │
│                                                            │
│ Using blueprint reduces questions from 20 to 3!           │
│                                                            │
│ Options:                                                   │
│  1. Use blueprint (3 quick questions, ~15 min)            │
│  2. Custom configuration (20 questions, ~60 min)          │
│  3. Skip all questions (use all defaults, ~10 min)        │
│                                                            │
│ Your choice (1/2/3): _____                                │
└────────────────────────────────────────────────────────────┘
```

**Handle responses:**
- **1 or "blueprint"** → Ask only 3 blueprint questions
- **2 or "custom"** → Ask all skill questions (normal flow)
- **3 or "skip"** → Use all defaults, skip all questions

---

## Generated Output Structure

When blueprint is executed, generate this file structure:

```
security-hardening/
├── infrastructure/
│   ├── terraform/                      # Infrastructure as Code
│   │   ├── main.tf                     # Main Terraform configuration
│   │   ├── security-groups.tf          # Firewall rules
│   │   ├── network.tf                  # VPC, subnets, network policies
│   │   ├── iam.tf                      # Identity and access management
│   │   ├── kms.tf                      # Key management service
│   │   └── variables.tf                # Terraform variables
│   │
│   ├── kubernetes/                     # Kubernetes security manifests
│   │   ├── network-policies/           # Network segmentation
│   │   │   ├── default-deny.yaml       # Default deny all traffic
│   │   │   ├── allow-dns.yaml          # Allow DNS queries
│   │   │   └── app-specific.yaml       # Application network rules
│   │   │
│   │   ├── pod-security/               # Pod security policies
│   │   │   ├── restricted.yaml         # Restrictive PSP (default)
│   │   │   ├── baseline.yaml           # Baseline PSP
│   │   │   └── security-context.yaml   # Security context examples
│   │   │
│   │   ├── rbac/                       # Role-based access control
│   │   │   ├── roles.yaml              # Kubernetes roles
│   │   │   ├── role-bindings.yaml      # Role bindings
│   │   │   └── service-accounts.yaml   # Service accounts
│   │   │
│   │   └── secrets/                    # Secret management
│   │       ├── sealed-secrets.yaml     # Encrypted secrets
│   │       └── external-secrets.yaml   # External secret integration
│   │
│   └── docker/                         # Container security
│       ├── Dockerfile.secure           # Hardened Dockerfile template
│       ├── .dockerignore               # Prevent secret inclusion
│       └── docker-compose.secure.yml   # Secure compose configuration
│
├── auth/                               # Authentication & Authorization
│   ├── oauth2/
│   │   ├── oauth2-config.yaml          # OAuth2 server configuration
│   │   ├── client-registration.yaml    # OAuth2 client registry
│   │   └── scopes.yaml                 # OAuth2 scopes definition
│   │
│   ├── jwt/
│   │   ├── jwt-generator.ts            # JWT token generation
│   │   ├── jwt-validator.ts            # JWT token validation
│   │   ├── jwt-middleware.ts           # Express/FastAPI middleware
│   │   └── keys/                       # RSA key pair storage (gitignored)
│   │       ├── private.pem             # Private key (generated)
│   │       └── public.pem              # Public key (generated)
│   │
│   ├── rbac/
│   │   ├── roles.yaml                  # Role definitions
│   │   ├── permissions.yaml            # Permission matrix
│   │   ├── rbac-middleware.ts          # Authorization middleware
│   │   └── access-control-matrix.md    # Human-readable ACL documentation
│   │
│   └── mfa/
│       ├── totp-setup.ts               # TOTP enrollment flow
│       ├── totp-verify.ts              # TOTP verification
│       └── backup-codes.ts             # Backup code generation
│
├── secrets/                            # Secret Management
│   ├── vault/
│   │   ├── vault-config.hcl            # HashiCorp Vault configuration
│   │   ├── policies/                   # Vault access policies
│   │   │   ├── admin-policy.hcl        # Admin access policy
│   │   │   ├── app-policy.hcl          # Application access policy
│   │   │   └── ci-policy.hcl           # CI/CD access policy
│   │   │
│   │   ├── init-vault.sh               # Vault initialization script
│   │   └── rotate-secrets.sh           # Secret rotation automation
│   │
│   ├── rotation/
│   │   ├── database-rotation.ts        # Database credential rotation
│   │   ├── api-key-rotation.ts         # API key rotation
│   │   └── tls-cert-renewal.sh         # TLS certificate renewal
│   │
│   └── templates/
│       ├── .env.template               # Environment variable template
│       └── secrets.yaml.template       # Kubernetes secrets template
│
├── monitoring/                         # Security Monitoring & SIEM
│   ├── logging/
│   │   ├── logstash/
│   │   │   ├── logstash.conf           # Log parsing configuration
│   │   │   └── pipelines/              # Log processing pipelines
│   │   │       ├── security-events.conf
│   │   │       ├── access-logs.conf
│   │   │       └── audit-logs.conf
│   │   │
│   │   ├── fluentd/
│   │   │   ├── fluentd.conf            # Alternative to Logstash
│   │   │   └── filters/                # Log filtering rules
│   │   │
│   │   └── structured-logging.ts       # Application logging library
│   │
│   ├── alerting/
│   │   ├── prometheus/
│   │   │   ├── alerts.yaml             # Prometheus alert rules
│   │   │   └── recording-rules.yaml    # Metric aggregation rules
│   │   │
│   │   ├── alertmanager/
│   │   │   ├── config.yaml             # Alert routing configuration
│   │   │   └── templates/              # Notification templates
│   │   │
│   │   └── siem-rules/
│   │       ├── failed-auth.yaml        # Failed authentication detection
│   │       ├── privilege-escalation.yaml
│   │       ├── data-exfiltration.yaml
│   │       └── anomaly-detection.yaml
│   │
│   └── dashboards/
│       ├── grafana/
│       │   ├── security-overview.json  # Main security dashboard
│       │   ├── auth-metrics.json       # Authentication metrics
│       │   └── compliance-metrics.json # Compliance KPIs
│       │
│       └── kibana/
│           ├── security-logs.ndjson    # Kibana dashboard export
│           └── saved-searches.ndjson   # Common security queries
│
├── ci-cd/                              # CI/CD Security Integration
│   ├── github-actions/
│   │   ├── security-scan.yml           # Security scanning workflow
│   │   ├── dependency-check.yml        # Dependency vulnerability scan
│   │   ├── container-scan.yml          # Container image scanning
│   │   └── secrets-scan.yml            # Secret detection workflow
│   │
│   ├── gitlab-ci/
│   │   ├── .gitlab-ci.yml              # GitLab CI security jobs
│   │   └── security-templates/         # Reusable security templates
│   │
│   ├── security-gates/
│   │   ├── gate-policy.yaml            # Security gate criteria
│   │   ├── approve-deployment.sh       # Approval script
│   │   └── vulnerability-threshold.yaml
│   │
│   └── scanning-tools/
│       ├── sonarqube-config.xml        # SAST configuration
│       ├── snyk-config.json            # SCA configuration
│       ├── trivy-config.yaml           # Container scanning
│       └── zap-baseline.conf           # DAST configuration
│
├── network/                            # Network Security
│   ├── firewall/
│   │   ├── iptables-rules.sh           # iptables configuration
│   │   ├── ufw-setup.sh                # UFW (Ubuntu firewall) setup
│   │   └── cloud-firewall.tf           # Cloud provider firewall
│   │
│   ├── waf/
│   │   ├── waf-rules.json              # Web application firewall rules
│   │   ├── owasp-top10.yaml            # OWASP Top 10 protection
│   │   └── rate-limiting.yaml          # Rate limiting configuration
│   │
│   ├── vpn/
│   │   ├── wireguard-config.conf       # WireGuard VPN configuration
│   │   ├── openvpn-config.ovpn         # OpenVPN configuration
│   │   └── client-certificates/        # VPN client certs
│   │
│   └── service-mesh/
│       ├── istio/
│       │   ├── mtls-policy.yaml        # Mutual TLS configuration
│       │   ├── authorization-policy.yaml
│       │   └── peer-authentication.yaml
│       │
│       └── linkerd/
│           ├── linkerd-config.yaml     # Alternative to Istio
│           └── server-authorization.yaml
│
├── compliance/                         # Compliance Documentation
│   ├── policies/
│   │   ├── information-security-policy.md
│   │   ├── access-control-policy.md
│   │   ├── data-protection-policy.md
│   │   ├── incident-response-policy.md
│   │   ├── acceptable-use-policy.md
│   │   └── business-continuity-policy.md
│   │
│   ├── procedures/
│   │   ├── user-onboarding.md          # New user access provisioning
│   │   ├── user-offboarding.md         # Access revocation procedure
│   │   ├── security-incident-response.md
│   │   ├── vulnerability-management.md
│   │   ├── change-management.md
│   │   └── backup-restore.md
│   │
│   ├── evidence/
│   │   ├── access-reviews/             # Quarterly access reviews
│   │   ├── security-training/          # Training completion records
│   │   ├── vulnerability-scans/        # Scan reports
│   │   ├── penetration-tests/          # Pentest reports
│   │   └── audit-logs/                 # Audit log exports
│   │
│   ├── frameworks/
│   │   ├── soc2/
│   │   │   ├── control-matrix.xlsx     # SOC2 control mapping
│   │   │   ├── trust-services-criteria.md
│   │   │   └── evidence-collection.md
│   │   │
│   │   ├── iso27001/
│   │   │   ├── isms-scope.md           # ISMS scope definition
│   │   │   ├── risk-assessment.xlsx    # Risk register
│   │   │   └── statement-applicability.xlsx
│   │   │
│   │   ├── hipaa/ (if selected)
│   │   │   ├── hipaa-security-rule.md
│   │   │   ├── phi-inventory.xlsx
│   │   │   └── breach-notification.md
│   │   │
│   │   └── gdpr/ (if selected)
│   │       ├── data-processing-agreement.md
│   │       ├── privacy-impact-assessment.md
│   │       └── data-flow-diagram.png
│   │
│   └── audits/
│       ├── internal-audit-plan.md
│       ├── audit-checklist.xlsx
│       └── findings-tracker.xlsx
│
├── scripts/                            # Automation Scripts
│   ├── hardening/
│   │   ├── harden-ubuntu.sh            # Ubuntu server hardening
│   │   ├── harden-rhel.sh              # RHEL/CentOS hardening
│   │   ├── harden-docker.sh            # Docker daemon hardening
│   │   └── cis-benchmark-check.sh      # CIS compliance validation
│   │
│   ├── scanning/
│   │   ├── vulnerability-scan.sh       # Automated vulnerability scan
│   │   ├── port-scan.sh                # Network port scanning
│   │   ├── ssl-scan.sh                 # TLS/SSL configuration check
│   │   └── dependency-audit.sh         # Dependency vulnerability check
│   │
│   └── incident-response/
│       ├── isolate-host.sh             # Quarantine compromised host
│       ├── collect-forensics.sh        # Forensic data collection
│       └── revoke-all-access.sh        # Emergency access revocation
│
├── tests/                              # Security Testing
│   ├── integration/
│   │   ├── auth-flow.test.ts           # Authentication flow tests
│   │   ├── rbac.test.ts                # Authorization tests
│   │   └── secret-injection.test.ts    # Secret management tests
│   │
│   ├── security/
│   │   ├── xss-prevention.test.ts      # XSS attack prevention
│   │   ├── sql-injection.test.ts       # SQL injection prevention
│   │   ├── csrf-protection.test.ts     # CSRF protection
│   │   └── rate-limiting.test.ts       # Rate limiting validation
│   │
│   └── compliance/
│       ├── password-policy.test.ts     # Password policy enforcement
│       ├── session-timeout.test.ts     # Session management tests
│       └── audit-logging.test.ts       # Audit trail verification
│
├── docs/                               # Documentation
│   ├── architecture/
│   │   ├── security-architecture.md    # Overall security architecture
│   │   ├── threat-model.md             # Threat modeling analysis
│   │   └── data-flow-diagrams/         # DFD for sensitive data
│   │
│   ├── runbooks/
│   │   ├── security-incident.md        # Incident response runbook
│   │   ├── certificate-renewal.md      # TLS cert renewal steps
│   │   └── disaster-recovery.md        # DR procedures
│   │
│   └── training/
│       ├── security-awareness.md       # Employee security training
│       ├── secure-coding.md            # Developer secure coding guide
│       └── phishing-prevention.md      # Phishing awareness
│
├── config/                             # Configuration Files
│   ├── tls/
│   │   ├── tls-config.yaml             # TLS version and ciphers
│   │   ├── nginx-ssl.conf              # Nginx TLS configuration
│   │   └── apache-ssl.conf             # Apache TLS configuration
│   │
│   ├── cors/
│   │   ├── cors-policy.yaml            # CORS configuration
│   │   └── allowed-origins.yaml        # Origin whitelist
│   │
│   └── headers/
│       ├── security-headers.yaml       # HTTP security headers
│       └── csp-policy.yaml             # Content Security Policy
│
├── .github/
│   ├── dependabot.yml                  # Automated dependency updates
│   └── SECURITY.md                     # Security policy and contact
│
├── README.md                           # Setup and usage guide
├── SECURITY.md                         # Security disclosure policy
└── COMPLIANCE.md                       # Compliance status and evidence
```

---

## Security Architecture

### Defense in Depth Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    DEFENSE IN DEPTH                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 7: Compliance & Governance                           │
│   ├─ Security policies and procedures                      │
│   ├─ Security awareness training                           │
│   ├─ Third-party risk management                           │
│   └─ Audit and compliance reporting                        │
│                                                             │
│  Layer 6: Application Security                             │
│   ├─ Input validation and sanitization                     │
│   ├─ Output encoding (XSS prevention)                      │
│   ├─ Parameterized queries (SQL injection prevention)      │
│   ├─ CSRF protection                                       │
│   └─ Security headers (CSP, HSTS, X-Frame-Options)         │
│                                                             │
│  Layer 5: Authentication & Authorization                    │
│   ├─ OAuth 2.0 / OpenID Connect                            │
│   ├─ Multi-factor authentication (MFA)                     │
│   ├─ Role-based access control (RBAC)                      │
│   ├─ JWT token validation                                  │
│   └─ Session management                                    │
│                                                             │
│  Layer 4: Data Security                                    │
│   ├─ Encryption at rest (AES-256)                          │
│   ├─ Encryption in transit (TLS 1.3)                       │
│   ├─ Secret management (HashiCorp Vault)                   │
│   ├─ Data classification and labeling                      │
│   └─ Secure key management (KMS)                           │
│                                                             │
│  Layer 3: Network Security                                 │
│   ├─ Zero trust network architecture                       │
│   ├─ Firewall rules (default deny)                         │
│   ├─ Web application firewall (WAF)                        │
│   ├─ DDoS protection                                       │
│   ├─ Network segmentation                                  │
│   └─ VPN for remote access                                 │
│                                                             │
│  Layer 2: Infrastructure Security                          │
│   ├─ OS hardening (CIS benchmarks)                         │
│   ├─ Container security (non-root, read-only)              │
│   ├─ Pod security policies (Kubernetes)                    │
│   ├─ Immutable infrastructure                              │
│   └─ Automatic security patching                           │
│                                                             │
│  Layer 1: Monitoring & Incident Response                   │
│   ├─ Security information and event management (SIEM)      │
│   ├─ Intrusion detection/prevention (IDS/IPS)              │
│   ├─ Real-time alerting                                    │
│   ├─ Incident response automation                          │
│   └─ Forensic data collection                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Zero Trust Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ZERO TRUST MODEL                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Principles:                                                │
│   1. Never trust, always verify                            │
│   2. Assume breach (least privilege)                       │
│   3. Verify explicitly (every request)                     │
│                                                             │
│  Implementation:                                            │
│                                                             │
│  User/Service                                               │
│       │                                                     │
│       ├─► [Authentication] ────► Identity Provider         │
│       │         (OAuth2/OIDC)     (Okta, Auth0, Keycloak)  │
│       │                                                     │
│       ├─► [Authorization] ─────► Policy Engine             │
│       │         (RBAC/ABAC)       (OPA, Casbin)            │
│       │                                                     │
│       ├─► [Device Trust] ──────► Device Verification       │
│       │     (certificate-based)   (MDM, device fingerprint) │
│       │                                                     │
│       ├─► [Network] ───────────► Service Mesh              │
│       │         (mTLS)            (Istio, Linkerd)         │
│       │                                                     │
│       └─► [Continuous Monitoring] ─► SIEM / UBA            │
│             (behavior analysis)      (Splunk, ELK, Sentinel)│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Compliance Control Matrix

### SOC2 Type II Trust Service Criteria

| Control | Description | Implementation | Evidence |
|---------|-------------|----------------|----------|
| CC1.1 | Board oversight of security | Security committee, quarterly reviews | Meeting minutes, risk reports |
| CC1.2 | Management oversight | CISO role, security team structure | Org chart, job descriptions |
| CC6.1 | Logical access controls | RBAC, MFA, password policy | Access control matrix, audit logs |
| CC6.2 | Authentication mechanisms | OAuth2/OIDC, JWT, session management | Auth configuration, code review |
| CC6.3 | Authorization enforcement | RBAC middleware, policy engine | Authorization tests, access reviews |
| CC6.6 | Encryption | TLS 1.3, AES-256, encryption at rest | TLS config, encryption verification |
| CC7.2 | Security monitoring | SIEM, intrusion detection, alerting | SIEM dashboards, alert configurations |
| CC7.3 | Incident response | IR playbooks, on-call rotation | Incident logs, IR drills |
| CC7.4 | Vulnerability management | Automated scanning, patch management | Scan reports, patch logs |
| CC8.1 | Change management | Code review, approval process | Pull requests, change logs |

### ISO 27001 Controls (Annex A)

| Domain | Control | Implementation |
|--------|---------|----------------|
| A.5 | Information security policies | Security policy documents in `/compliance/policies/` |
| A.6 | Organization of security | CISO role, security team, incident response team |
| A.8 | Asset management | Asset inventory, data classification |
| A.9 | Access control | RBAC, MFA, access reviews in `/auth/rbac/` |
| A.10 | Cryptography | TLS 1.3, AES-256, key management in `/secrets/` |
| A.12 | Operations security | Change management, backup procedures |
| A.13 | Communications security | Network security, TLS encryption in `/network/` |
| A.14 | System acquisition | Secure SDLC, security requirements |
| A.16 | Incident management | IR procedures in `/compliance/procedures/` |
| A.17 | Business continuity | DR plan, backup testing |
| A.18 | Compliance | Audit logs, compliance monitoring |

---

## Threat Model

### STRIDE Analysis

| Threat | Mitigation | Implementation |
|--------|-----------|----------------|
| **Spoofing** | Strong authentication (OAuth2 + MFA) | `/auth/oauth2/`, `/auth/mfa/` |
| **Tampering** | Encryption in transit (TLS 1.3) | `/config/tls/tls-config.yaml` |
| **Repudiation** | Audit logging, immutable logs | `/monitoring/logging/`, SIEM |
| **Information Disclosure** | Encryption at rest (AES-256) | KMS, Vault encryption |
| **Denial of Service** | Rate limiting, DDoS protection | `/network/waf/rate-limiting.yaml` |
| **Elevation of Privilege** | RBAC, least privilege, ABAC | `/auth/rbac/roles.yaml` |

### Attack Surface Reduction

```
External Attack Surface:
├─ Public APIs
│  ├─ WAF protection (OWASP Top 10)
│  ├─ Rate limiting (20 req/min unauthenticated)
│  ├─ Input validation and sanitization
│  └─ TLS 1.3 encryption

├─ Web Application
│  ├─ Content Security Policy (CSP)
│  ├─ CSRF protection
│  ├─ XSS prevention (output encoding)
│  └─ Security headers (HSTS, X-Frame-Options)

└─ SSH/Management Access
   ├─ VPN required
   ├─ Certificate-based auth
   ├─ IP allowlisting
   └─ Bastion host (jump server)

Internal Attack Surface:
├─ Service-to-Service Communication
│  ├─ Mutual TLS (mTLS) via service mesh
│  ├─ Service accounts with minimal permissions
│  └─ Network policies (zero trust)

└─ Data Access
   ├─ Dynamic secrets (Vault)
   ├─ Encryption at rest
   └─ Column-level access control
```

---

## Security Tools and Technologies

### Recommended Tool Stack

**Authentication & Authorization:**
- Identity Provider: Okta, Auth0, Keycloak (open-source)
- Policy Engine: Open Policy Agent (OPA), Casbin
- MFA: Authy, Google Authenticator, Duo

**Secret Management:**
- Primary: HashiCorp Vault
- Alternatives: AWS Secrets Manager, Azure Key Vault, GCP Secret Manager

**Security Scanning:**
- SAST: SonarQube, Semgrep, Checkmarx
- DAST: OWASP ZAP, Burp Suite
- SCA: Snyk, Dependabot, WhiteSource
- Container: Trivy, Clair, Anchore
- Secrets: TruffleHog, git-secrets, GitGuardian

**SIEM & Monitoring:**
- Log Aggregation: ELK Stack, Splunk, Datadog
- Metrics: Prometheus + Grafana
- Tracing: Jaeger, Zipkin
- Alerting: PagerDuty, Opsgenie, AlertManager

**Network Security:**
- WAF: AWS WAF, Cloudflare, ModSecurity
- Service Mesh: Istio, Linkerd, Consul
- VPN: WireGuard, OpenVPN
- DDoS: Cloudflare, AWS Shield

**Compliance & Governance:**
- GRC Platform: Vanta, Drata, Secureframe
- Vulnerability Management: Tenable, Qualys, Rapid7

---

## Incident Response Playbook

### Severity Levels

| Severity | Description | Response Time | Escalation |
|----------|-------------|---------------|------------|
| **Critical** | Active breach, data exfiltration, ransomware | Immediate (< 15 min) | CEO, CISO, Legal |
| **High** | Vulnerability exploitation, privilege escalation | < 1 hour | CISO, Security Team |
| **Medium** | Failed attack attempts, suspicious activity | < 4 hours | Security Team Lead |
| **Low** | Policy violations, misconfigurations | < 24 hours | Security Analyst |

### Response Phases

```
1. Detection
   ├─ SIEM alerts trigger
   ├─ Automated threat detection
   └─ User reports suspicious activity

2. Triage
   ├─ Determine severity
   ├─ Assign incident commander
   └─ Assemble response team

3. Containment
   ├─ Isolate affected systems
   ├─ Revoke compromised credentials
   ├─ Block malicious IPs
   └─ Preserve forensic evidence

4. Eradication
   ├─ Remove malware/backdoors
   ├─ Patch vulnerabilities
   └─ Close attack vectors

5. Recovery
   ├─ Restore from clean backups
   ├─ Verify system integrity
   └─ Monitor for reinfection

6. Post-Incident
   ├─ Root cause analysis
   ├─ Update security controls
   ├─ Document lessons learned
   └─ Notify affected parties (if required)
```

---

## Security Metrics and KPIs

### Key Performance Indicators

```yaml
Authentication Metrics:
  - Failed login attempts (threshold: 5 per user per 10 min)
  - MFA enrollment rate (target: 100%)
  - Password reset frequency (monitor for anomalies)
  - Session duration average (monitor for outliers)

Vulnerability Management:
  - Mean time to patch critical vulnerabilities (target: < 7 days)
  - Open vulnerabilities by severity (trend down)
  - Vulnerability scan coverage (target: 100% of assets)
  - False positive rate (target: < 10%)

Incident Response:
  - Mean time to detect (MTTD) (target: < 15 minutes)
  - Mean time to respond (MTTR) (target: < 1 hour for high)
  - Number of security incidents (trend down)
  - Incident recurrence rate (target: 0%)

Compliance:
  - Audit findings (target: 0 critical)
  - Policy compliance rate (target: 100%)
  - Security training completion (target: 100% annually)
  - Access review completion (target: quarterly)

Network Security:
  - Blocked malicious requests (monitor trends)
  - DDoS attacks mitigated (monitor)
  - TLS version distribution (target: 100% TLS 1.3)
  - Certificate expiration warnings (renew 30 days prior)
```

---

## Dependencies and Tools

### Required Software

```yaml
Infrastructure:
  - Terraform: "~> 1.6"
  - Kubernetes: "~> 1.28"
  - Docker: "~> 24.0"

Authentication:
  - Keycloak: "~> 22.0" (if self-hosted)
  - OAuth2 Proxy: "~> 7.5"

Secret Management:
  - HashiCorp Vault: "~> 1.15"

Monitoring:
  - Elasticsearch: "~> 8.11"
  - Logstash: "~> 8.11"
  - Kibana: "~> 8.11"
  - Prometheus: "~> 2.48"
  - Grafana: "~> 10.2"

Security Scanning:
  - Trivy: "~> 0.48"
  - Snyk CLI: "~> 1.1266"
  - SonarQube: "~> 10.3"

Network:
  - Istio: "~> 1.20"
  - WireGuard: "~> 1.0"
```

---

## Customization Points

After blueprint generation, users can customize:

1. **Authentication provider:** Switch from Keycloak to Okta/Auth0
2. **Secret storage:** Replace Vault with cloud provider service
3. **Compliance frameworks:** Add/remove frameworks based on needs
4. **Monitoring stack:** Replace ELK with Splunk/Datadog
5. **Network architecture:** Adjust for specific cloud provider
6. **Security policies:** Fine-tune policies for organization

---

## Migration and Integration

### Adding Security to Existing Applications

```
Phase 1: Assessment (Week 1-2)
├─ Security audit of current architecture
├─ Identify critical vulnerabilities
├─ Map compliance gaps
└─ Prioritize remediation efforts

Phase 2: Quick Wins (Week 3-4)
├─ Enable TLS 1.3 across all services
├─ Implement rate limiting
├─ Add security headers
├─ Enable automated security scanning in CI/CD
└─ Set up centralized logging

Phase 3: Core Security (Week 5-8)
├─ Implement OAuth2/OIDC authentication
├─ Deploy HashiCorp Vault for secrets
├─ Configure RBAC authorization
├─ Set up SIEM and alerting
└─ Implement network segmentation

Phase 4: Advanced Security (Week 9-12)
├─ Deploy service mesh with mTLS
├─ Implement zero trust architecture
├─ Complete compliance documentation
├─ Conduct penetration testing
└─ Security awareness training

Phase 5: Continuous Improvement
├─ Regular vulnerability scanning
├─ Quarterly access reviews
├─ Annual penetration testing
├─ Security training updates
└─ Compliance audits
```

---

## Testing and Validation

### Security Test Checklist

```markdown
## Authentication Tests
- [ ] Failed login attempts are rate-limited
- [ ] Weak passwords are rejected
- [ ] MFA cannot be bypassed
- [ ] Session timeout enforced
- [ ] Concurrent session limit enforced
- [ ] Password reset flow is secure

## Authorization Tests
- [ ] Users can only access authorized resources
- [ ] Horizontal privilege escalation prevented
- [ ] Vertical privilege escalation prevented
- [ ] RBAC policies enforced correctly
- [ ] Token validation works for all endpoints

## Application Security Tests
- [ ] XSS attacks prevented (input validation)
- [ ] SQL injection prevented (parameterized queries)
- [ ] CSRF protection enabled
- [ ] Security headers present (CSP, HSTS, etc.)
- [ ] File upload restrictions enforced

## Network Security Tests
- [ ] TLS 1.3 enforced (1.2 minimum)
- [ ] Weak cipher suites disabled
- [ ] Firewall rules block unauthorized traffic
- [ ] Rate limiting prevents DoS
- [ ] WAF blocks common attacks

## Secret Management Tests
- [ ] No secrets in environment variables
- [ ] No secrets in code repositories
- [ ] Secrets rotated on schedule
- [ ] Vault access requires authentication
- [ ] Dynamic secrets revoked after TTL

## Monitoring and Logging Tests
- [ ] Security events logged correctly
- [ ] Alerts triggered for suspicious activity
- [ ] Audit logs immutable
- [ ] Log retention meets compliance requirements
- [ ] SIEM correlation rules functional

## Compliance Tests
- [ ] All required policies documented
- [ ] Access reviews completed quarterly
- [ ] Security training completed annually
- [ ] Audit logs exported and archived
- [ ] Third-party vendor assessments current
```

---

## Version History

**1.0.0** (2024-12-06)
- Initial security hardening blueprint
- 7-skill chain with comprehensive defaults
- 3-question quick configuration
- Zero trust architecture
- SOC2 + ISO 27001 compliance defaults
- Multi-layered defense in depth

---

## Related Blueprints

- **Auth Blueprint:** Deep dive into authentication/authorization only
- **Compliance Blueprint:** Focus on compliance documentation/audit
- **Monitoring Blueprint:** Advanced SIEM and security monitoring
- **DevSecOps Blueprint:** Security in CI/CD and development workflow

---

**Blueprint Complete**
