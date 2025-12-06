# Defense in Depth Reference

## Table of Contents

1. [Overview](#overview)
2. [9-Layer Defense Model](#9-layer-defense-model)
3. [Implementation Patterns](#implementation-patterns)
4. [Layer Integration Strategies](#layer-integration-strategies)
5. [Failure Impact Analysis](#failure-impact-analysis)
6. [Architecture Selection Decision Tree](#architecture-selection-decision-tree)

## Overview

Defense in Depth (DiD) is the foundational security architecture principle of implementing multiple independent layers of security controls. If one layer fails or is breached, other layers continue to protect critical assets.

**Core Principle:** Redundancy and diversity of defense mechanisms across all layers from physical to operational.

**Modern Context (2025):** Defense in Depth now incorporates behavioral analytics, workload security, and identity threat detection to address cloud-native architectures and sophisticated attack vectors.

## 9-Layer Defense Model

### Layer 1: Physical Security

**Purpose:** Protect physical access to hardware and facilities.

**Controls:**
- Physical access control systems (badge readers, biometrics, mantrap entries)
- Surveillance systems (CCTV, motion detection, security guards)
- Environmental controls (HVAC, fire suppression, power redundancy, UPS)
- Hardware security modules (HSM) for cryptographic key storage
- Secure disposal of hardware (degaussing magnetic media, physical destruction of drives)

**Cloud Considerations:**
- Cloud providers (AWS, GCP, Azure) handle physical security of data centers
- SOC 2 Type II and ISO 27001 certified facilities
- Shared responsibility: Provider secures data centers, customer secures workloads

**Failure Impact:** Limited (cloud providers provide strong physical security)

**Monitoring:** Access logs, video surveillance, environmental sensors

---

### Layer 2: Network Perimeter

**Purpose:** Control and inspect traffic entering and leaving the network.

**Controls:**
- **Next-Generation Firewalls (NGFW):** Application-aware firewalls (Palo Alto, Fortinet, Cisco)
- **Web Application Firewall (WAF):** OWASP Top 10 protection (Cloudflare, Imperva, F5, AWS WAF)
- **DDoS Protection:** Volumetric attack mitigation (Cloudflare, AWS Shield, Azure DDoS)
- **Intrusion Prevention System (IPS/IDS):** Signature and anomaly-based detection
- **Deep Packet Inspection (DPI):** Traffic analysis and content filtering
- **SSL/TLS Inspection:** Decrypt and inspect encrypted traffic for threats

**Architecture Pattern:**
```
Internet → DDoS Protection → WAF/CDN → NGFW → Internal Network
```

**Failure Impact:** High (direct exposure to internet threats if perimeter fails)

**Monitoring:** Firewall logs, IDS/IPS alerts, traffic flow analysis, DDoS metrics

---

### Layer 3: Network Segmentation

**Purpose:** Divide network into isolated zones to limit lateral movement.

**Controls:**
- **VLANs:** Virtual LAN segmentation (Layer 2)
- **VPCs/Subnets:** Cloud virtual networks (AWS VPC, GCP VPC, Azure VNet)
- **Security Groups:** Stateful firewall rules for cloud instances
- **Network Access Control Lists (NACLs):** Stateless firewall rules for subnets
- **Micro-Segmentation:** Fine-grained segmentation at workload level (service mesh, zero trust)
- **Internal Firewalls:** East-west traffic control between zones

**Segmentation Zones:**
- **DMZ (Demilitarized Zone):** Public-facing services (web servers, mail servers)
- **Web Tier:** Application front-end
- **Application Tier:** Business logic, APIs
- **Data Tier:** Databases, data stores (most restricted)
- **Management Zone:** Administrative access, jump boxes

**Architecture Pattern:**
```
┌─────────────┐
│   Internet  │
└──────┬──────┘
       │
┌──────▼──────────────────────────┐
│  DMZ Zone (Public Web Servers)  │
└──────┬──────────────────────────┘
       │
┌──────▼──────────────────────────┐
│  Web Tier (App Front-End)       │
└──────┬──────────────────────────┘
       │
┌──────▼──────────────────────────┐
│  App Tier (Business Logic)      │
└──────┬──────────────────────────┘
       │
┌──────▼──────────────────────────┐
│  Data Tier (Databases)           │  ← Most Restricted
└──────────────────────────────────┘
```

**Failure Impact:** Medium (limits lateral movement even if one zone is compromised)

**Monitoring:** VPC flow logs, network traffic analysis, connection attempts between zones

---

### Layer 4: Endpoint Protection

**Purpose:** Secure individual devices (workstations, servers, mobile devices).

**Controls:**
- **Antivirus/Anti-malware:** Signature-based and heuristic detection (Windows Defender, CrowdStrike, SentinelOne)
- **Endpoint Detection & Response (EDR):** Real-time monitoring, threat hunting, automated response
- **Mobile Device Management (MDM):** BYOD policies, remote wipe, app control (Intune, Jamf, VMware Workspace ONE)
- **Patch Management:** Automated OS and application patching (WSUS, SCCM, Systems Manager)
- **Device Encryption:** Full-disk encryption (BitLocker, FileVault, LUKS)
- **Device Posture Validation:** Health checks before network access (compliance checks, OS version, encryption status)
- **Host-based Firewall:** Windows Firewall, iptables/nftables (Linux)

**Zero Trust Integration:**
- Continuous device posture assessment
- Device compliance verification before access grant
- Adaptive access based on device trust score

**Failure Impact:** High (endpoint compromise is a common attack vector)

**Monitoring:** EDR alerts, patch compliance dashboards, device health status, antivirus detections

---

### Layer 5: Application Security

**Purpose:** Protect applications, APIs, and software from exploitation.

**Controls:**
- **Secure SDLC:** Security requirements, threat modeling, security testing in development
- **Web Application Firewall (WAF):** OWASP Top 10 protection at application layer
- **API Security:** Authentication (OAuth 2.0, API keys), authorization, rate limiting, input validation
- **Code Analysis:**
  - **SAST (Static Application Security Testing):** Scan source code (SonarQube, Checkmarx)
  - **DAST (Dynamic Application Security Testing):** Scan running applications (OWASP ZAP, Burp Suite)
  - **IAST (Interactive Application Security Testing):** Runtime analysis (Contrast Security)
  - **SCA (Software Composition Analysis):** Dependency scanning (Snyk, Dependabot, Trivy)
- **Runtime Protection:** RASP (Runtime Application Self-Protection)
- **Dependency Management:** SBOM generation, vulnerability scanning, automated updates
- **Input Validation:** Sanitize and validate all user inputs
- **Output Encoding:** Prevent XSS attacks through proper encoding

**OWASP Top 10 Controls:**
1. Injection → Parameterized queries, ORM frameworks
2. Broken Authentication → MFA, secure session management
3. Sensitive Data Exposure → Encryption, key management
4. XXE → Disable XML external entities, prefer JSON
5. Broken Access Control → Authorization checks at every endpoint
6. Security Misconfiguration → Hardening guides, remove defaults
7. XSS → Output encoding, Content Security Policy (CSP)
8. Insecure Deserialization → Validate serialized objects
9. Known Vulnerabilities → Patch management, SBOM
10. Insufficient Logging → Centralized logging, SIEM

**Failure Impact:** High (application vulnerabilities are easily exploitable)

**Monitoring:** WAF logs, application logs, DAST findings, dependency vulnerability alerts

---

### Layer 6: Data Security

**Purpose:** Protect data confidentiality, integrity, and availability throughout its lifecycle.

**Controls:**
- **Encryption at Rest:** AES-256, Transparent Database Encryption (TDE)
- **Encryption in Transit:** TLS 1.3, mutual TLS (mTLS), VPN tunnels
- **Encryption in Use:** Confidential computing (Intel SGX, AMD SEV, ARM TrustZone)
- **Key Management:** HSM (hardware security modules), cloud KMS (AWS KMS, GCP KMS, Azure Key Vault)
- **Data Classification:** Public, Internal, Confidential, Restricted
- **Data Loss Prevention (DLP):** Content inspection, policy enforcement, alerting (Microsoft Purview, Symantec DLP)
- **Database Security:** Least privilege access, audit logging, query monitoring
- **Backup & Recovery:** 3-2-1 rule (3 copies, 2 media types, 1 offsite), immutable backups
- **Data Masking:** Anonymization, pseudonymization for non-production environments

**Data Lifecycle Security:**
```
Create → Store → Process → Share → Archive → Destroy
  │       │        │         │        │         │
  ▼       ▼        ▼         ▼        ▼         ▼
Classify Encrypt  Access   Encrypt  Retention Secure
         +Key Mgmt Control  +Audit   Policy   Deletion
```

**Failure Impact:** Critical (data is the ultimate target of attacks)

**Monitoring:** Data access logs, DLP alerts, encryption status, backup verification, unauthorized access attempts

---

### Layer 7: Identity & Access Management (IAM)

**Purpose:** Control who and what can access resources.

**Authentication Controls:**
- **Multi-Factor Authentication (MFA):** TOTP, push notifications, biometrics, hardware tokens (YubiKey, FIDO2)
- **Passwordless:** WebAuthn, FIDO2, passkeys
- **Single Sign-On (SSO):** SAML 2.0, OAuth 2.0, OpenID Connect (Azure AD, Okta, Auth0)

**Authorization Controls:**
- **Role-Based Access Control (RBAC):** Users → Roles → Permissions
- **Attribute-Based Access Control (ABAC):** Fine-grained based on attributes (department, location, time)
- **Policy-Based Access Control (PBAC):** Centralized policy engines (Open Policy Agent, AWS Cedar)

**Privileged Access Management (PAM):**
- **Just-in-Time (JIT) Access:** Temporary elevated privileges
- **Session Recording:** Audit all privileged sessions
- **Credential Vaulting:** CyberArk, HashiCorp Vault, AWS Secrets Manager

**Identity Governance:**
- User lifecycle management (joiner/mover/leaver)
- Access certification and recertification
- Segregation of Duties (SoD) enforcement

**Identity-First Zero Trust:**
- Identity is the control plane
- Every access request authenticates identity
- Risk-based adaptive authentication (device, location, behavior)

**Failure Impact:** Critical (identity compromise grants full access)

**Monitoring:** Authentication logs, failed login attempts, privileged access, MFA enrollment, risky sign-ins

---

### Layer 8: Behavioral Analytics

**Purpose:** Detect anomalies and threats through machine learning and behavioral analysis.

**Controls:**
- **User & Entity Behavior Analytics (UEBA):** ML-based anomaly detection (Microsoft Sentinel, Splunk)
- **Anomaly Detection:** Detect deviations from normal behavior patterns
- **Threat Intelligence:** Integrate feeds from ISACs, threat intel platforms (MISP, ThreatConnect)
- **Risk Scoring:** Assign risk scores to users, entities, activities
- **Contextual Analysis:** Combine multiple signals (time, location, device, resource accessed)

**Detection Use Cases:**
- Account compromise (unusual login location, time, device)
- Insider threats (unusual data access, exfiltration patterns)
- Lateral movement (unusual network connections)
- Privilege escalation (unusual administrative actions)
- Data exfiltration (large data transfers, unusual file access)

**Failure Impact:** Medium (detection layer, not prevention; delays in detection increase breach impact)

**Monitoring:** UEBA alerts, risk score changes, anomaly detection dashboards

---

### Layer 9: Security Operations

**Purpose:** Continuous monitoring, detection, response, and improvement.

**Controls:**
- **Security Information & Event Management (SIEM):** Centralized log aggregation, correlation, alerting (Splunk, Elastic, Sentinel, Chronicle)
- **Security Orchestration, Automation & Response (SOAR):** Playbook automation, incident response (Splunk SOAR, Cortex XSOAR)
- **Extended Detection & Response (XDR):** Unified visibility across endpoints, network, cloud (Palo Alto Cortex XDR, Trend Micro Vision One)
- **Vulnerability Management:** Continuous scanning, risk-based prioritization (Tenable, Qualys, Rapid7)
- **Penetration Testing:** Red team exercises, bug bounty programs
- **Incident Response:** Documented playbooks, tabletop exercises, post-incident reviews
- **Threat Hunting:** Proactive search for threats using MITRE ATT&CK TTPs

**SIEM Architecture:**
```
Data Sources → Log Collection → Normalization → Correlation → Alerting → Investigation
(Firewalls,    (Agents, APIs)   (Common format) (Rules, ML)   (SOC Team) (Search, Viz)
 Endpoints,
 Apps, Cloud)
```

**Failure Impact:** High (inability to detect or respond to breaches extends dwell time)

**Monitoring:** SIEM alert metrics, MTTD (mean time to detect), MTTR (mean time to respond), incident counts

---

## Implementation Patterns

### Pattern 1: Cloud-Native Defense in Depth (AWS Example)

**Layer Mapping:**

1. **Physical:** AWS data center security (managed by AWS)
2. **Network Perimeter:** AWS WAF + CloudFront + Shield (DDoS)
3. **Network Segmentation:** VPCs, subnets, security groups, NACLs
4. **Endpoint:** Systems Manager (patch), Inspector (vuln scan), GuardDuty (threat detection)
5. **Application:** API Gateway (rate limit, auth), WAF rules, CodeGuru (code analysis)
6. **Data:** S3 encryption, RDS encryption, KMS (key management), Macie (data discovery)
7. **IAM:** IAM Identity Center (SSO), MFA, IAM policies (least privilege), IAM Access Analyzer
8. **Behavioral Analytics:** GuardDuty (anomaly detection), Detective (investigation)
9. **Security Operations:** Security Hub (centralized findings), CloudWatch (monitoring), CloudTrail (audit logs)

**Implementation Steps:**
1. Design VPC architecture with public/private subnets
2. Enable GuardDuty, Security Hub, CloudTrail organization-wide
3. Implement IAM Identity Center for SSO and MFA
4. Deploy WAF on CloudFront and API Gateway
5. Enable encryption for all data stores (S3, RDS, EBS)
6. Configure Security Hub automated response (Lambda)
7. Centralize logs in dedicated Logging Account

---

### Pattern 2: Zero Trust Overlay on Defense in Depth

**Strategy:** Maintain existing Defense in Depth perimeter controls, layer Zero Trust controls progressively.

**Phase 1: Identity Foundation**
- Implement SSO and MFA for all users
- Deploy identity provider (Azure AD, Okta)
- Enable device posture checks

**Phase 2: Least Privilege Access**
- Migrate to RBAC/ABAC
- Implement JIT access for privileged accounts
- Remove standing admin permissions

**Phase 3: Micro-Segmentation**
- Segment critical applications
- Deploy ZTNA (Zero Trust Network Access) for remote access
- Implement service mesh for east-west traffic control

**Phase 4: Continuous Verification**
- Deploy UEBA for anomaly detection
- Implement risk-based conditional access
- Enable continuous compliance monitoring

**Result:** Hybrid architecture with perimeter defense + identity-first zero trust controls

---

### Pattern 3: Defense in Depth for Web Applications

**Layered Controls:**

```
Layer 9: SIEM + SOAR (Splunk, Sentinel)
         ↓
Layer 8: UEBA (Anomaly detection)
         ↓
Layer 7: OAuth 2.0 + MFA + RBAC
         ↓
Layer 6: Database encryption + DLP
         ↓
Layer 5: WAF + SAST/DAST + Secure coding
         ↓
Layer 4: Container security (runtime protection)
         ↓
Layer 3: Kubernetes Network Policies + Service mesh
         ↓
Layer 2: Cloud WAF + DDoS protection
         ↓
Layer 1: Cloud provider data center security
```

**Example Tech Stack:**
- **Layer 2:** Cloudflare (WAF + DDoS)
- **Layer 3:** Kubernetes Network Policies + Istio service mesh
- **Layer 4:** Falco (runtime security) + Trivy (image scanning)
- **Layer 5:** OWASP ZAP (DAST) + SonarQube (SAST) + Snyk (SCA)
- **Layer 6:** PostgreSQL with TDE + AWS KMS
- **Layer 7:** Auth0 (OAuth 2.0 + MFA) + OPA (policy-based authz)
- **Layer 8:** Elastic Security (UEBA)
- **Layer 9:** Elastic SIEM + TheHive (SOAR)

---

## Layer Integration Strategies

### Strategy 1: Centralized Logging

Aggregate logs from all layers into SIEM for unified visibility.

**Log Sources:**
- Layer 2: Firewall logs, IDS/IPS alerts
- Layer 3: VPC flow logs, network connection logs
- Layer 4: Endpoint logs, EDR alerts
- Layer 5: Application logs, WAF logs
- Layer 6: Database audit logs, data access logs
- Layer 7: Authentication logs, IAM events
- Layer 8: UEBA alerts, anomaly scores
- Layer 9: Incident response actions

**SIEM Correlation Rules:**
- Multiple failed logins (Layer 7) + Endpoint compromise (Layer 4) = Account takeover
- Unusual data access (Layer 6) + Large data transfer (Layer 3) = Data exfiltration
- Malware detection (Layer 4) + Lateral movement (Layer 3) = Active breach

---

### Strategy 2: Policy Enforcement Across Layers

Define security policies centrally and enforce at multiple layers.

**Example Policy: "Only encrypted data in transit"**
- Layer 2: WAF blocks HTTP requests (enforce HTTPS)
- Layer 3: Security group rules block port 80 (HTTP)
- Layer 5: Application redirects HTTP to HTTPS
- Layer 6: Database rejects non-TLS connections
- Layer 9: SIEM alerts on any HTTP traffic detected

**Enforcement Points:**
- Network layer (firewalls, security groups)
- Application layer (WAF, API gateway)
- Data layer (database configuration)
- Monitoring layer (SIEM alerts)

---

### Strategy 3: Defense Redundancy

Implement multiple defenses for critical assets.

**Example: Database Protection**
- Layer 2: Firewall blocks external access to database ports
- Layer 3: Database in private subnet, no internet gateway
- Layer 4: Database server hardened (minimal services, patched)
- Layer 5: Application uses parameterized queries (prevent SQL injection)
- Layer 6: Database encryption at rest + TLS in transit
- Layer 7: Database access requires authentication + least privilege
- Layer 8: UEBA detects unusual database queries
- Layer 9: Database audit logs sent to SIEM

**Result:** Even if one layer fails (e.g., SQL injection bypasses Layer 5), other layers still protect the database.

---

## Failure Impact Analysis

### Critical Failures (Immediate Risk)

**Layer 7 (IAM) Failure:**
- **Impact:** Compromised credentials grant full access
- **Mitigation:** MFA prevents credential-only compromise, PAM limits privilege duration
- **Detection:** Monitor failed logins, unusual access patterns

**Layer 6 (Data) Failure:**
- **Impact:** Data breach, regulatory violations, reputational damage
- **Mitigation:** Encryption limits exposure (encrypted data less valuable), DLP prevents exfiltration
- **Detection:** Monitor data access patterns, large transfers

---

### High Failures (Significant Risk)

**Layer 2 (Perimeter) Failure:**
- **Impact:** Direct exposure to internet threats
- **Mitigation:** Layer 3 segmentation limits lateral movement, Layer 7 IAM prevents unauthorized access
- **Detection:** IDS/IPS alerts, unusual inbound traffic

**Layer 4 (Endpoint) Failure:**
- **Impact:** Malware execution, lateral movement platform
- **Mitigation:** Layer 3 micro-segmentation limits spread, Layer 7 prevents privilege escalation
- **Detection:** EDR alerts, anomalous process execution

---

### Medium Failures (Moderate Risk)

**Layer 3 (Segmentation) Failure:**
- **Impact:** Lateral movement possible
- **Mitigation:** Layer 7 IAM limits access even within same network, Layer 8 detects lateral movement
- **Detection:** Flow logs, connection attempts to unusual destinations

**Layer 8 (Behavioral Analytics) Failure:**
- **Impact:** Delayed threat detection
- **Mitigation:** Layer 9 SIEM still provides rule-based detection, Layer 4/5/6 still prevent many attacks
- **Detection:** Increased undetected dwell time

---

## Architecture Selection Decision Tree

```
START: Designing security architecture
  │
  ├─► Is this a greenfield (new) system?
  │     YES ──► Zero Trust from Day 1
  │               ├─► Identity-first architecture (Layer 7 primary)
  │               ├─► Micro-segmentation by default (Layer 3)
  │               ├─► Assume breach mentality
  │               └─► Continuous verification (Layer 8)
  │
  │     NO ──► Brownfield (existing) system?
  │               └─► Hybrid: Defense in Depth + Zero Trust overlay
  │                     ├─► Maintain perimeter controls (Layers 1-3)
  │                     ├─► Strengthen IAM (Layer 7: SSO, MFA, RBAC)
  │                     ├─► Add behavioral analytics (Layer 8)
  │                     └─► Segment critical assets first
  │
  ├─► What is the deployment environment?
  │     CLOUD-NATIVE ──► Cloud provider reference architectures
  │                       ├─► AWS: Well-Architected Security Pillar
  │                       ├─► GCP: Security Best Practices
  │                       └─► Azure: Security Benchmark
  │
  │     HYBRID CLOUD ──► Multi-cloud security posture management
  │                       ├─► Unified policy enforcement (CSPM)
  │                       ├─► Cross-cloud visibility
  │                       └─► Cloud-agnostic IAM (Okta, Azure AD)
  │
  │     ON-PREMISES ──► Traditional Defense in Depth
  │                       ├─► Strong perimeter (Layer 2)
  │                       ├─► Network segmentation (Layer 3)
  │                       └─► Progressive modernization to Zero Trust
  │
  ├─► What are compliance requirements?
  │     SOC 2 ──► NIST CSF + CIS Controls baseline
  │     HIPAA ──► NIST CSF + HIPAA Security Rule mappings
  │     PCI DSS ──► PCI DSS requirements + network segmentation
  │     GDPR ──► NIST Privacy Framework + data protection controls
  │     ISO 27001 ──► ISO 27001/27002 control framework
  │
  └─► What is the risk tolerance?
        HIGH RISK (Financial, Healthcare, Government)
          ├─► Maximum controls across all 9 layers
          ├─► Zero Trust + Defense in Depth
          ├─► 24/7 SOC monitoring
          └─► Penetration testing, red team exercises

        MEDIUM RISK (Enterprise SaaS, E-commerce)
          ├─► Balanced security and usability
          ├─► Cloud-native security services
          └─► Managed SIEM/SOC

        LOW RISK (Internal tools, non-sensitive data)
          ├─► Essential controls (Layers 2, 5, 7, 9)
          ├─► Cloud-native security defaults
          └─► Automated monitoring
```

---

## Summary

Defense in Depth provides comprehensive security through layered, independent controls. Implement all 9 layers for maximum protection, with critical focus on:

1. **Layer 7 (IAM):** Identity is the new perimeter - strongest authentication and authorization
2. **Layer 6 (Data):** Data is the ultimate target - encrypt and protect at all stages
3. **Layer 9 (Security Operations):** Detection and response capabilities determine breach impact

For new systems, design Zero Trust architecture on top of Defense in Depth foundation. For existing systems, progressively add Zero Trust controls while maintaining perimeter defenses.
