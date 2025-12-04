# Security Architecture Skill - Master Plan

**Skill Name:** `security-architecture`
**Skill Level:** High Level (8,000-12,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Security Architecture Taxonomy](#security-architecture-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Defense in Depth Strategy](#defense-in-depth-strategy)
7. [Zero Trust Architecture](#zero-trust-architecture)
8. [Threat Modeling Methodologies](#threat-modeling-methodologies)
9. [Security Controls Mapping](#security-controls-mapping)
10. [Supply Chain Security](#supply-chain-security)
11. [Cloud Security Architecture](#cloud-security-architecture)
12. [Framework Recommendations](#framework-recommendations)
13. [Skill Structure Design](#skill-structure-design)
14. [Integration Points](#integration-points)
15. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why Security Architecture Matters

Security architecture is the foundational discipline for building resilient, compliant, and trustworthy systems. In 2025, with increasing sophistication of cyber threats, regulatory compliance mandates (GDPR, SOC 2, HIPAA), and zero-trust adoption, comprehensive security architecture expertise is critical.

**Market Drivers:**
- **Regulatory Compliance:** GDPR, SOC 2, HIPAA, PCI DSS require architectural controls
- **Zero Trust Adoption:** 80%+ enterprises moving to zero trust models by 2025
- **Supply Chain Attacks:** SolarWinds, Log4Shell highlight supply chain vulnerabilities
- **Cloud-Native Security:** 90%+ workloads in cloud require cloud-native security patterns
- **AI/ML Security:** New attack vectors from AI systems require architectural defenses

**Strategic Value:**
1. **Foundational Discipline:** Security must be architected, not bolted on
2. **Risk Management:** Proactive architecture prevents costly breaches
3. **Compliance Enablement:** Architecture enables audit and compliance
4. **Business Enablement:** Secure systems enable business innovation
5. **Cost Efficiency:** Preventing breaches is 10-100x cheaper than remediation

### How This Differs from Tactical Security

**Tactical Security Skills:**
- **auth-security:** Authentication/authorization implementation details
- **vulnerability-management:** Scanning and patching vulnerabilities
- **configuring-firewalls:** Network firewall rules and configurations
- **siem-logging:** Security information and event management

**Security Architecture (This Skill):**
- **Strategic Planning:** Defense in depth, zero trust strategy
- **Threat Modeling:** STRIDE, PASTA, attack tree analysis
- **Control Frameworks:** NIST CSF, CIS Controls, ISO 27001
- **Reference Architectures:** Cloud provider security patterns
- **Security Governance:** Policies, standards, risk management

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **Defense in Depth Strategy**
   - Layered security controls across infrastructure, network, application, data
   - Redundancy and diversity of defense mechanisms
   - Fail-secure design patterns

2. **Zero Trust Architecture (ZTA)**
   - Never trust, always verify principles
   - Identity-first security architecture
   - Micro-segmentation and least privilege access
   - Continuous verification and monitoring

3. **Threat Modeling**
   - STRIDE methodology (Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation)
   - PASTA methodology (Process for Attack Simulation and Threat Analysis)
   - DREAD scoring (Damage, Reproducibility, Exploitability, Affected Users, Discoverability)
   - Attack trees and data flow diagrams

4. **Security Controls Mapping**
   - NIST Cybersecurity Framework (CSF)
   - CIS Critical Security Controls
   - ISO 27001/27002 controls
   - OWASP Top 10 risk mitigation

5. **Supply Chain Security**
   - SLSA framework (Supply-chain Levels for Software Artifacts)
   - SBOM (Software Bill of Materials)
   - Dependency scanning and vulnerability management
   - Secure development lifecycle integration

6. **Cloud Security Architecture**
   - AWS Well-Architected Framework (Security Pillar)
   - GCP Security Command Center architecture
   - Azure Security Center and Defender patterns
   - Multi-cloud security posture management

### What This Skill Does NOT Cover

- **Implementation Details:** Use auth-security, configuring-firewalls, secret-management skills
- **Vulnerability Scanning:** Use vulnerability-management skill
- **Incident Response:** Use incident-response skill (if available)
- **Application Security Testing:** Use sast-dast-scanning skill (if available)
- **Network Security Devices:** Use configuring-firewalls, configuring-waf skills

---

## Research Findings

### Google Search Grounding (December 2025)

#### Defense in Depth (Research Query 1)

**Key 2025 Findings:**
- Defense in Depth (DiD) remains the core security architecture principle
- Multiple layers of security controls provide redundancy
- Modern DiD incorporates behavioral analytics, workload security, and ITDR
- AI/ML increasingly used for threat detection and predictive analytics
- Zero Trust Architecture complements (not replaces) Defense in Depth

**Modern Defense in Depth Layers:**
1. **Physical Security:** Data center access controls, environmental protection
2. **Network Security:** Firewalls, IPS/IDS, network segmentation, microsegmentation
3. **Endpoint Security:** EDR, antivirus, patch management, device compliance
4. **Application Security:** WAF, secure coding, vulnerability scanning, SAST/DAST
5. **Data Security:** Encryption at rest/transit, DLP, data classification, backup
6. **Identity & Access Management:** MFA, RBAC, privileged access management
7. **Behavioral Analytics:** ML-based anomaly detection, UEBA (User/Entity Behavior Analytics)
8. **Workload Security:** Container security, runtime protection, cloud security posture
9. **ITDR (Identity Threat Detection & Response):** Real-time identity threat monitoring

**Sources:**
- rsisecurity.com - Defense in Depth Strategy
- cyberlab.co.uk - Layered Security Best Practices
- delinea.com - Modern DiD Implementation
- wallarm.com - Application Security in DiD

#### Zero Trust Architecture (Research Query 2)

**Key 2025 Findings:**
- Zero Trust adoption accelerating (80%+ enterprises by 2025)
- Core principle: "Never trust, always verify" at every access request
- Identity is the new perimeter (IAM is foundational)
- Micro-segmentation limits lateral movement
- Continuous verification and monitoring required

**Zero Trust Core Principles:**
1. **Continuous Verification:** Authenticate and authorize every access request
2. **Least-Privilege Access:** Grant minimal access needed for tasks
3. **Assume Breach Mentality:** Design systems expecting compromise
4. **Micro-Segmentation:** Network divided into small, isolated zones
5. **Device Posture Verification:** Trust devices only after validation

**Zero Trust Implementation Steps:**
1. Conduct comprehensive asset and identity inventory
2. Strengthen authentication (MFA, passwordless, biometrics)
3. Implement least-privilege access controls
4. Start micro-segmentation (network zones)
5. Establish continuous monitoring and analytics
6. Choose Zero Trust-aligned tools (ZTNA, SASE)
7. Foster security-first culture through training

**Benefits:**
- Enhanced protection against ransomware, phishing, insider threats
- Reduced attack surface and limited lateral movement
- Improved breach detection and containment
- Better regulatory compliance (GDPR, SOC 2, HIPAA)
- Average cost savings: $1.76M per breach (IBM 2024 Cost of Breach Report)

**Challenges:**
- Complexity integrating with legacy systems
- Scalability in large distributed environments
- Cultural resistance from users and stakeholders
- Balancing security with user experience

**Sources:**
- journalwjarr.com - ZTA Implementation 2025
- hyetech.com.au - Enterprise ZTA Adoption
- ntgit.com - Zero Trust Best Practices
- seraphicsecurity.com - Browser Security in ZTA

#### Threat Modeling and Supply Chain Security

**Note:** Google Search Grounding queries for threat modeling and supply chain security encountered errors. Relying on established methodologies and OWASP research.

### Context7 Research (December 2025)

#### OWASP Cheat Sheet Series
**Library ID:** `/owasp/cheatsheetseries`
**Trust Score:** High
**Code Snippets:** 963
**Benchmark Score:** 78.5

**Key Findings:**
- Comprehensive security patterns for authentication, authorization, access control
- Kubernetes security context examples (Pod security, RBAC)
- Node.js permissions model for least-privilege execution
- Authorization matrix testing patterns for RBAC validation
- Serverless security (API Gateway JWT authorizers)

#### OWASP Top Ten
**Library ID:** `/websites/owasp_www-project-top-ten`
**Trust Score:** High
**Code Snippets:** 365

**Key 2017 Risks (Still Relevant 2025):**
1. **Injection** (Score: 8.0) - SQL, NoSQL, OS command injection
2. **Broken Authentication** (Score: 7.0) - Session management, credential stuffing
3. **Sensitive Data Exposure** (Score: 7.0) - Unencrypted data, weak crypto
4. **XML External Entities (XXE)** (Score: 7.0) - XML parser vulnerabilities
5. **Broken Access Control** (Score: 6.0) - Authorization bypasses
6. **Security Misconfiguration** (Score: 6.0) - Default configs, unnecessary features
7. **Cross-Site Scripting (XSS)** (Score: 6.0) - Reflected, stored, DOM-based XSS
8. **Insecure Deserialization** (Score: 5.0) - Remote code execution via deserialization
9. **Using Components with Known Vulnerabilities** (Score: 4.7) - Supply chain risk
10. **Insufficient Logging & Monitoring** (Score: 4.0) - Limited breach detection

**Prevention Strategies:**
- Parameterized queries and ORM frameworks (Injection)
- MFA and session management best practices (Authentication)
- Encryption at rest/transit, key management (Data Exposure)
- Component inventory and vulnerability scanning (Supply Chain)
- Centralized logging and SIEM integration (Monitoring)

---

## Security Architecture Taxonomy

### Layer 1: Physical Security

**Scope:** Data center, office, hardware protection

**Controls:**
- Physical access control systems (badge readers, biometrics)
- Surveillance systems (CCTV, motion detection)
- Environmental controls (HVAC, fire suppression, power redundancy)
- Hardware security modules (HSM) for key storage
- Secure disposal of hardware (degaussing, physical destruction)

**Cloud Considerations:**
- Cloud providers handle physical security (AWS, GCP, Azure SOC 2 certified)
- Shared responsibility model: Provider secures data centers, customer secures workloads

---

### Layer 2: Network Security

**Scope:** Network infrastructure, traffic control, segmentation

**Controls:**
- **Perimeter Defense:** Next-gen firewalls (NGFW), WAF, DDoS protection
- **Network Segmentation:** VLANs, VPCs, subnets, security groups
- **Micro-Segmentation:** Zero-trust network access (ZTNA), service mesh
- **Intrusion Prevention:** IPS/IDS, network behavior analysis
- **Traffic Inspection:** Deep packet inspection (DPI), SSL/TLS decryption
- **VPN & Remote Access:** IPsec VPN, SSL VPN, ZTNA for remote workers

**Architecture Pattern:**

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERNET (UNTRUSTED)                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │   DDoS      │
                    │  Protection │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   WAF/CDN   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Firewall  │
                    │    (NGFW)   │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐     ┌─────▼─────┐
   │   DMZ   │       │   Web     │     │   API     │
   │  Zone   │       │   Tier    │     │  Gateway  │
   └─────────┘       └─────┬─────┘     └─────┬─────┘
                           │                  │
                    ┌──────▼──────────────────▼──────┐
                    │    Internal Firewall           │
                    └──────┬──────────────────┬──────┘
                           │                  │
                    ┌──────▼──────┐    ┌─────▼─────┐
                    │ Application │    │   Data    │
                    │    Tier     │    │   Tier    │
                    └─────────────┘    └───────────┘
```

---

### Layer 3: Endpoint Security

**Scope:** Devices, workstations, mobile devices, IoT

**Controls:**
- **Antivirus/Anti-malware:** Signature-based and heuristic detection
- **Endpoint Detection & Response (EDR):** Real-time monitoring, threat hunting
- **Mobile Device Management (MDM):** BYOD policies, remote wipe, app control
- **Patch Management:** Automated OS and application patching
- **Device Encryption:** Full-disk encryption (BitLocker, FileVault, LUKS)
- **Device Posture Validation:** Health checks before network access

**Zero Trust Endpoint Integration:**
- Device compliance verification before access grant
- Continuous device posture assessment
- Adaptive access based on device trust score

---

### Layer 4: Application Security

**Scope:** Web applications, APIs, microservices, serverless functions

**Controls:**
- **Secure SDLC:** Security requirements, threat modeling, security testing
- **Web Application Firewall (WAF):** OWASP Top 10 protection
- **API Security:** Authentication (OAuth 2.0, API keys), rate limiting, input validation
- **Code Analysis:** SAST (static), DAST (dynamic), IAST (interactive), SCA (composition)
- **Runtime Protection:** RASP (Runtime Application Self-Protection)
- **Dependency Management:** SBOM generation, vulnerability scanning

**OWASP Top 10 Mitigation:**
1. **Injection:** Parameterized queries, input validation, ORM frameworks
2. **Broken Authentication:** MFA, secure session management, credential policies
3. **Sensitive Data Exposure:** Encryption (TLS, AES-256), key management (HSM, KMS)
4. **XXE:** Disable XML external entities, use JSON instead
5. **Broken Access Control:** Enforce authorization at every endpoint, principle of least privilege
6. **Security Misconfiguration:** Hardening guides, remove default accounts, minimal services
7. **XSS:** Output encoding, Content Security Policy (CSP), sanitize inputs
8. **Insecure Deserialization:** Validate serialized objects, use safe serialization formats
9. **Known Vulnerabilities:** Continuous dependency scanning, patch management
10. **Insufficient Logging:** Centralized logging, SIEM integration, audit trails

---

### Layer 5: Data Security

**Scope:** Data at rest, in transit, in use, backups

**Controls:**
- **Encryption at Rest:** AES-256, transparent database encryption (TDE)
- **Encryption in Transit:** TLS 1.3, mutual TLS (mTLS), VPN tunnels
- **Encryption in Use:** Confidential computing (Intel SGX, AMD SEV, ARM TrustZone)
- **Key Management:** HSM, cloud KMS (AWS KMS, GCP KMS, Azure Key Vault)
- **Data Classification:** Public, internal, confidential, restricted
- **Data Loss Prevention (DLP):** Content inspection, policy enforcement, alerting
- **Backup & Recovery:** 3-2-1 rule (3 copies, 2 media types, 1 offsite), immutable backups

**Data Lifecycle Security:**
```
Create → Store → Process → Share → Archive → Destroy
  │       │        │         │        │         │
  ▼       ▼        ▼         ▼        ▼         ▼
 Classify Encrypt  Access   Encrypt  Retention Secure
          +Key Mgmt Control  +Audit   Policy   Deletion
```

---

### Layer 6: Identity & Access Management (IAM)

**Scope:** Authentication, authorization, identity governance

**Controls:**
- **Authentication:**
  - Multi-Factor Authentication (MFA): TOTP, push notifications, biometrics, hardware tokens
  - Passwordless: WebAuthn, FIDO2, passkeys
  - Single Sign-On (SSO): SAML 2.0, OAuth 2.0, OpenID Connect
- **Authorization:**
  - Role-Based Access Control (RBAC): Users assigned to roles, roles have permissions
  - Attribute-Based Access Control (ABAC): Fine-grained access based on attributes
  - Policy-Based Access Control (PBAC): Centralized policy engines (OPA, Cedar)
- **Privileged Access Management (PAM):**
  - Just-in-Time (JIT) access: Temporary elevated privileges
  - Session recording and auditing
  - Credential vaulting (CyberArk, HashiCorp Vault)
- **Identity Governance & Administration (IGA):**
  - User lifecycle management (joiner/mover/leaver)
  - Access certification and recertification
  - Segregation of Duties (SoD) enforcement

**Identity-First Zero Trust:**
- Identity is the control plane for zero trust
- Every access request authenticates identity
- Risk-based adaptive authentication (device, location, behavior)

---

### Layer 7: Security Monitoring & Operations

**Scope:** Logging, monitoring, detection, response

**Controls:**
- **Security Information & Event Management (SIEM):** Centralized log aggregation, correlation, alerting
- **Security Orchestration, Automation & Response (SOAR):** Playbook automation, incident response
- **User & Entity Behavior Analytics (UEBA):** ML-based anomaly detection
- **Extended Detection & Response (XDR):** Unified visibility across endpoints, network, cloud
- **Threat Intelligence:** Feeds from ISACs, threat intel platforms (MISP, ThreatConnect)
- **Vulnerability Management:** Continuous scanning, risk-based prioritization
- **Penetration Testing:** Red team exercises, bug bounty programs

---

## Decision Frameworks

### Framework 1: Security Architecture Approach Selection

```
START: Designing security architecture for a system
  │
  ├─► Greenfield (new system)?
  │     YES ──► Zero Trust from Day 1
  │               ├─► Identity-first architecture
  │               ├─► Micro-segmentation by default
  │               ├─► Assume breach mentality
  │               └─► Continuous verification
  │     NO ──► Brownfield (existing system)?
  │               └─► Hybrid: Defense in Depth + Zero Trust overlay
  │                     ├─► Maintain existing perimeter controls
  │                     ├─► Layer Zero Trust controls progressively
  │                     └─► Segment critical assets first
  │
  ├─► Compliance requirements? (GDPR, SOC 2, HIPAA, PCI DSS)
  │     YES ──► Map to control frameworks
  │               ├─► NIST CSF for general security
  │               ├─► CIS Controls for baseline hardening
  │               ├─► ISO 27001 for comprehensive ISMS
  │               └─► Framework-specific (PCI DSS, HIPAA Security Rule)
  │
  ├─► Cloud-native or hybrid?
  │     CLOUD-NATIVE ──► Cloud provider reference architectures
  │                       ├─► AWS Well-Architected Framework (Security Pillar)
  │                       ├─► GCP Security Best Practices
  │                       └─► Azure Security Benchmark
  │     HYBRID ──► Multi-cloud security posture management (CSPM)
  │                 ├─► Unified security policy enforcement
  │                 ├─► Cross-cloud visibility
  │                 └─► Cloud-agnostic IAM (Okta, Azure AD)
  │
  └─► Risk tolerance? (High, Medium, Low)
        HIGH RISK ──► Maximum security controls
                      ├─► Air-gapped networks
                      ├─► Hardware security modules (HSM)
                      ├─► Zero trust + defense in depth
                      └─► 24/7 SOC monitoring
        MEDIUM RISK ──► Balanced security and usability
                        ├─► Standard enterprise security
                        ├─► Cloud-managed security services
                        └─► Managed SIEM/SOC
        LOW RISK ──► Essential controls only
                     ├─► Basic firewalls, encryption
                     ├─► Cloud-native security tools
                     └─► Automated monitoring
```

---

### Framework 2: Threat Modeling Methodology Selection

| Methodology | Best For | Complexity | Output |
|-------------|----------|------------|--------|
| **STRIDE** | Threat identification | Low | Threat categories (6 types) |
| **PASTA** | Risk-centric analysis | High | Prioritized threats, attack scenarios |
| **DREAD** | Risk scoring | Low | Numeric risk scores |
| **Attack Trees** | Visual threat analysis | Medium | Tree diagrams of attack paths |
| **LINDDUN** | Privacy-focused | Medium | Privacy threats (7 categories) |

**Decision Tree:**
```
What is your primary goal?
  │
  ├─► Identify all possible threats
  │     └─► STRIDE (Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation)
  │
  ├─► Prioritize threats by business risk
  │     └─► PASTA (7-stage process: business objectives → attack simulation)
  │
  ├─► Score existing threats numerically
  │     └─► DREAD (Damage, Reproducibility, Exploitability, Affected users, Discoverability)
  │
  ├─► Visualize attack scenarios
  │     └─► Attack Trees (Hierarchical tree of attack goals and paths)
  │
  └─► Privacy-specific threats
        └─► LINDDUN (Linkability, Identifiability, Non-repudiation, Detectability, Disclosure, Unawareness, Non-compliance)
```

---

### Framework 3: Security Controls Selection (NIST CSF)

**NIST Cybersecurity Framework Functions:**

1. **IDENTIFY (ID):**
   - Asset Management (ID.AM)
   - Business Environment (ID.BE)
   - Governance (ID.GV)
   - Risk Assessment (ID.RA)
   - Risk Management Strategy (ID.RM)
   - Supply Chain Risk Management (ID.SC)

2. **PROTECT (PR):**
   - Identity Management & Access Control (PR.AC)
   - Awareness & Training (PR.AT)
   - Data Security (PR.DS)
   - Information Protection Processes & Procedures (PR.IP)
   - Maintenance (PR.MA)
   - Protective Technology (PR.PT)

3. **DETECT (DE):**
   - Anomalies & Events (DE.AE)
   - Security Continuous Monitoring (DE.CM)
   - Detection Processes (DE.DP)

4. **RESPOND (RS):**
   - Response Planning (RS.RP)
   - Communications (RS.CO)
   - Analysis (RS.AN)
   - Mitigation (RS.MI)
   - Improvements (RS.IM)

5. **RECOVER (RC):**
   - Recovery Planning (RC.RP)
   - Improvements (RC.IM)
   - Communications (RC.CO)

**Mapping Example:**

| Risk | NIST Function | Control Category | Example Control |
|------|---------------|------------------|-----------------|
| Data breach | PROTECT | PR.DS (Data Security) | Encryption at rest/transit |
| Ransomware | PROTECT | PR.IP (Info Protection) | Immutable backups |
| Insider threat | DETECT | DE.CM (Continuous Monitoring) | UEBA anomaly detection |
| DDoS attack | PROTECT | PR.PT (Protective Technology) | DDoS mitigation service |
| Compromised credentials | PROTECT | PR.AC (Access Control) | MFA enforcement |

---

### Framework 4: Cloud Security Architecture Selection

| Cloud Provider | Security Service | Purpose | When to Use |
|----------------|------------------|---------|-------------|
| **AWS** | AWS Security Hub | Centralized security findings | Multi-account AWS environments |
|         | AWS GuardDuty | Threat detection | All AWS deployments |
|         | AWS IAM Identity Center | SSO, centralized IAM | Multi-account orgs |
|         | AWS KMS | Key management | Encryption key lifecycle |
|         | AWS WAF | Web application firewall | Public web apps |
| **GCP** | Security Command Center | Asset inventory, threat detection | All GCP organizations |
|         | Cloud Armor | DDoS, WAF | Internet-facing services |
|         | Cloud IAM | Access control | All GCP resources |
|         | Cloud KMS | Key management | Encryption key lifecycle |
| **Azure** | Microsoft Defender for Cloud | CSPM, threat protection | All Azure subscriptions |
|           | Azure AD (Entra ID) | Identity & access | All Azure resources |
|           | Azure Key Vault | Secrets, keys, certificates | Application secrets |
|           | Azure Firewall | Network security | Hub-spoke network architectures |

---

## Defense in Depth Strategy

### Comprehensive Layered Security Model

**Principle:** Multiple independent layers of defense, so if one layer fails, others continue to protect.

**9 Defense Layers (2025 Model):**

#### Layer 1: Physical Security
- **Controls:** Badge access, CCTV, biometrics, secure cages
- **Failure Impact:** Limited (cloud providers handle this)
- **Monitoring:** Access logs, video surveillance

#### Layer 2: Network Perimeter
- **Controls:** NGFW, IPS/IDS, DDoS protection, WAF
- **Failure Impact:** High (direct exposure to internet threats)
- **Monitoring:** Firewall logs, IDS alerts, traffic analysis

#### Layer 3: Network Segmentation
- **Controls:** VLANs, VPCs, security groups, micro-segmentation
- **Failure Impact:** Medium (limits lateral movement)
- **Monitoring:** Flow logs, network traffic analysis

#### Layer 4: Endpoint Protection
- **Controls:** EDR, antivirus, device encryption, patch management
- **Failure Impact:** High (endpoint compromise common entry point)
- **Monitoring:** EDR alerts, patch compliance, device health

#### Layer 5: Application Layer
- **Controls:** WAF, input validation, secure coding, API gateway
- **Failure Impact:** High (application vulnerabilities exploitable)
- **Monitoring:** WAF logs, application logs, DAST findings

#### Layer 6: Data Layer
- **Controls:** Encryption, DLP, database security, backup
- **Failure Impact:** Critical (data is the ultimate target)
- **Monitoring:** Data access logs, DLP alerts, backup verification

#### Layer 7: Identity & Access
- **Controls:** MFA, SSO, PAM, least privilege, RBAC/ABAC
- **Failure Impact:** Critical (identity compromise = full access)
- **Monitoring:** Authentication logs, failed login attempts, privileged access

#### Layer 8: Behavioral Analytics
- **Controls:** UEBA, anomaly detection, threat intelligence
- **Failure Impact:** Medium (detection layer, not prevention)
- **Monitoring:** ML-based anomaly alerts, risk scores

#### Layer 9: Security Operations
- **Controls:** SIEM, SOAR, incident response, threat hunting
- **Failure Impact:** High (inability to detect/respond to breaches)
- **Monitoring:** SIEM alerts, incident metrics, MTTD/MTTR

---

### Defense in Depth Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LAYER 9: SECURITY OPERATIONS                     │
│            SIEM, SOAR, Threat Hunting, Incident Response            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │             LAYER 8: BEHAVIORAL ANALYTICS                     │  │
│  │           UEBA, Anomaly Detection, Threat Intel               │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │          LAYER 7: IDENTITY & ACCESS MANAGEMENT          │  │  │
│  │  │         MFA, SSO, PAM, RBAC, Least Privilege            │  │  │
│  │  │  ┌───────────────────────────────────────────────────┐  │  │  │
│  │  │  │           LAYER 6: DATA SECURITY                  │  │  │  │
│  │  │  │    Encryption, DLP, Database Security, Backup     │  │  │  │
│  │  │  │  ┌─────────────────────────────────────────────┐  │  │  │  │
│  │  │  │  │      LAYER 5: APPLICATION SECURITY          │  │  │  │  │
│  │  │  │  │  WAF, Secure Coding, API Security, SAST     │  │  │  │  │
│  │  │  │  │  ┌───────────────────────────────────────┐  │  │  │  │  │
│  │  │  │  │  │   LAYER 4: ENDPOINT PROTECTION        │  │  │  │  │  │
│  │  │  │  │  │  EDR, Antivirus, Encryption, Patches  │  │  │  │  │  │
│  │  │  │  │  │  ┌─────────────────────────────────┐  │  │  │  │  │  │
│  │  │  │  │  │  │ LAYER 3: NETWORK SEGMENTATION   │  │  │  │  │  │  │
│  │  │  │  │  │  │  VLANs, VPCs, Micro-segmentation│  │  │  │  │  │  │
│  │  │  │  │  │  │  ┌───────────────────────────┐  │  │  │  │  │  │  │
│  │  │  │  │  │  │  │ LAYER 2: NETWORK PERIMETER│  │  │  │  │  │  │  │
│  │  │  │  │  │  │  │ Firewall, IPS, DDoS, WAF  │  │  │  │  │  │  │  │
│  │  │  │  │  │  │  │  ┌─────────────────────┐  │  │  │  │  │  │  │  │
│  │  │  │  │  │  │  │  │ LAYER 1: PHYSICAL   │  │  │  │  │  │  │  │  │
│  │  │  │  │  │  │  │  │ Data Center Access  │  │  │  │  │  │  │  │  │
│  │  │  │  │  │  │  │  │   CRITICAL ASSETS   │  │  │  │  │  │  │  │  │
│  │  │  │  │  │  │  │  └─────────────────────┘  │  │  │  │  │  │  │  │
│  │  │  │  │  │  │  └───────────────────────────┘  │  │  │  │  │  │  │
│  │  │  │  │  │  └─────────────────────────────────┘  │  │  │  │  │  │
│  │  │  │  │  └───────────────────────────────────────┘  │  │  │  │  │
│  │  │  │  └─────────────────────────────────────────────┘  │  │  │  │
│  │  │  └───────────────────────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Zero Trust Architecture

### Core Principles (Detailed)

**1. Never Trust, Always Verify**
- Every access request is authenticated and authorized
- No implicit trust based on network location
- Continuous verification throughout session

**2. Assume Breach**
- Design systems expecting compromise
- Limit blast radius of breaches
- Continuous monitoring for indicators of compromise

**3. Explicit Verification**
- Verify user identity (MFA, biometrics)
- Verify device health (posture, compliance)
- Verify application integrity (code signing, runtime checks)
- Verify context (location, time, behavior)

**4. Least Privilege Access**
- Just-in-time (JIT) access provisioning
- Just-enough-access (JEA) - minimal permissions
- Time-bound access grants
- Regular access reviews and recertification

**5. Micro-Segmentation**
- Network divided into small, isolated zones
- Each workload/application in separate segment
- East-west traffic (lateral) controlled
- Zero-trust network access (ZTNA)

---

### Zero Trust Reference Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      SECURITY POLICY ENGINE                      │
│           (Centralized authorization decision point)             │
└──────────────────────┬───────────────────────────────────────────┘
                       │ Policy decisions
         ┌─────────────┼─────────────┐
         │             │             │
    ┌────▼────┐   ┌────▼────┐   ┌───▼────┐
    │ Identity│   │ Device  │   │Context │
    │  Store  │   │ Posture │   │ (Risk) │
    │ (IdP)   │   │ Check   │   │ Engine │
    └─────────┘   └─────────┘   └────────┘
         │             │             │
         └─────────────┼─────────────┘
                       │ Trust signals
         ┌─────────────▼─────────────┐
         │   POLICY ENFORCEMENT      │
         │         POINTS            │
         │  (Gateways, Proxies)      │
         └─────────────┬─────────────┘
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
┌───▼───┐         ┌────▼────┐        ┌───▼────┐
│ User  │         │  App    │        │  Data  │
│Access │         │ Access  │        │ Access │
│Gateway│         │ Gateway │        │ Proxy  │
└───┬───┘         └────┬────┘        └───┬────┘
    │                  │                 │
┌───▼────────┐    ┌────▼─────────┐  ┌───▼─────────┐
│  Users     │    │ Applications │  │  Databases  │
│  (Humans   │    │ (Workloads)  │  │  (Storage)  │
│  & Machines)│   └──────────────┘  └─────────────┘
└────────────┘
```

**Components:**

1. **Policy Engine:** Centralized decision-making (Allow/Deny access)
2. **Identity Provider (IdP):** User/machine identity verification (Azure AD, Okta)
3. **Device Posture Service:** Device health checks (MDM, EDR integration)
4. **Context/Risk Engine:** Behavioral analytics, location, time, threat intel
5. **Policy Enforcement Points:** Gateways that enforce decisions (ZTNA, API gateways)

---

### Zero Trust Implementation Roadmap

**Phase 1: Foundation (Months 1-3)**
- [ ] Complete asset inventory (users, devices, applications, data)
- [ ] Implement MFA for all users (workforce + customers)
- [ ] Deploy centralized identity provider (SSO)
- [ ] Establish device inventory and management (MDM/UEM)

**Phase 2: Access Controls (Months 4-6)**
- [ ] Implement least-privilege access (RBAC/ABAC)
- [ ] Deploy privileged access management (PAM) for admins
- [ ] Enable device posture checks before access
- [ ] Implement conditional access policies (risk-based)

**Phase 3: Micro-Segmentation (Months 7-9)**
- [ ] Map application dependencies and data flows
- [ ] Design micro-segmentation zones
- [ ] Implement ZTNA for remote access
- [ ] Deploy service mesh for east-west traffic control

**Phase 4: Monitoring & Automation (Months 10-12)**
- [ ] Deploy SIEM for centralized logging
- [ ] Implement UEBA for anomaly detection
- [ ] Automate incident response (SOAR playbooks)
- [ ] Establish continuous compliance monitoring

---

## Threat Modeling Methodologies

### STRIDE Methodology

**Developed by:** Microsoft (Loren Kohnfelder and Praerit Garg, 1999)

**Threat Categories:**

1. **S - Spoofing Identity**
   - **Definition:** Attacker pretends to be someone else
   - **Example:** Phishing, session hijacking, credential theft
   - **Mitigation:** Strong authentication (MFA), certificate validation, anti-phishing

2. **T - Tampering with Data**
   - **Definition:** Unauthorized modification of data
   - **Example:** Man-in-the-middle attacks, SQL injection, data manipulation
   - **Mitigation:** Encryption in transit, digital signatures, integrity checks

3. **R - Repudiation**
   - **Definition:** User denies performing an action (and no proof exists)
   - **Example:** "I didn't make that purchase", "I didn't delete that file"
   - **Mitigation:** Audit logs, digital signatures, non-repudiation mechanisms

4. **I - Information Disclosure**
   - **Definition:** Exposure of confidential information to unauthorized parties
   - **Example:** Data leaks, SQL injection revealing data, API exposing PII
   - **Mitigation:** Encryption, access controls, DLP, minimize data exposure

5. **D - Denial of Service**
   - **Definition:** Making system unavailable to legitimate users
   - **Example:** DDoS attacks, resource exhaustion, crash exploits
   - **Mitigation:** Rate limiting, DDoS protection, resource quotas, redundancy

6. **E - Elevation of Privilege**
   - **Definition:** Gaining higher privileges than authorized
   - **Example:** Privilege escalation, buffer overflow, misconfigurations
   - **Mitigation:** Least privilege, input validation, regular patching, security testing

**STRIDE Application Process:**

1. **Model the system:** Create data flow diagrams (DFDs)
2. **Identify threats:** Apply STRIDE to each component/data flow
3. **Document threats:** Create threat list with STRIDE categories
4. **Prioritize threats:** Use DREAD or other scoring
5. **Mitigate threats:** Design security controls

**Example: Web Application STRIDE Analysis**

| Component | Threat Type | Threat | Mitigation |
|-----------|-------------|--------|------------|
| Login page | Spoofing | Credential phishing | MFA, anti-phishing (FIDO2) |
| API endpoint | Tampering | SQL injection | Parameterized queries, ORM |
| User actions | Repudiation | Deny deleting data | Audit logs, digital signatures |
| Database | Info Disclosure | Data breach | Encryption at rest, access control |
| API | Denial of Service | Rate limit bypass | API gateway rate limiting |
| Admin panel | Elevation | Privilege escalation | RBAC, input validation |

---

### PASTA Methodology

**Process for Attack Simulation and Threat Analysis**

**Developed by:** VerSprite (Tony UcedaVélez and Marco Morana)

**7 Stages:**

**Stage 1: Define Business Objectives**
- Identify business goals and compliance requirements
- Determine acceptable risk levels
- Define security objectives aligned with business

**Stage 2: Define Technical Scope**
- Inventory assets (applications, data, infrastructure)
- Document network architecture and data flows
- Identify trust boundaries

**Stage 3: Application Decomposition**
- Break down application into components
- Identify entry points and data flows
- Map authentication and authorization mechanisms

**Stage 4: Threat Analysis**
- Identify threat actors and motivations
- Map to MITRE ATT&CK framework
- Analyze past attack patterns

**Stage 5: Vulnerability & Weakness Analysis**
- Code review, SAST/DAST findings
- Configuration review
- Map to CWE (Common Weakness Enumeration)

**Stage 6: Attack Modeling**
- Create attack trees for identified threats
- Simulate attack scenarios
- Analyze attack feasibility and impact

**Stage 7: Risk & Impact Analysis**
- Quantify business impact (financial, reputational)
- Calculate risk scores
- Prioritize remediation based on risk

**PASTA vs STRIDE:**

| Aspect | PASTA | STRIDE |
|--------|-------|--------|
| Focus | Risk-centric, business-aligned | Threat identification |
| Complexity | High (7 stages) | Low (6 categories) |
| Output | Prioritized risks, attack scenarios | Threat list |
| Best For | Enterprise risk management | Development teams |

---

### DREAD Risk Scoring

**Developed by:** Microsoft (deprecated internally but still widely used)

**Scoring Factors (1-10 scale):**

1. **D - Damage Potential**
   - 10: Complete system compromise, data destruction
   - 5: Information disclosure, partial DoS
   - 1: Minor inconvenience

2. **R - Reproducibility**
   - 10: Attack works every time with no special conditions
   - 5: Attack requires specific timing or conditions
   - 1: Attack is extremely difficult to reproduce

3. **E - Exploitability**
   - 10: No authentication required, automated exploit available
   - 5: Requires authentication, manual exploit
   - 1: Requires deep technical knowledge, custom exploit

4. **A - Affected Users**
   - 10: All users affected
   - 5: Some users affected
   - 1: Few users affected (admin only)

5. **D - Discoverability**
   - 10: Vulnerability is obvious, already public
   - 5: Requires some effort to discover
   - 1: Nearly impossible to discover

**Risk Score Formula:**
```
Risk = (Damage + Reproducibility + Exploitability + Affected Users + Discoverability) / 5
```

**Risk Levels:**
- **Critical:** 8.0-10.0
- **High:** 6.0-7.9
- **Medium:** 4.0-5.9
- **Low:** 1.0-3.9

**Example: SQL Injection in Login Form**
- Damage: 9 (Database compromise)
- Reproducibility: 10 (Works every time)
- Exploitability: 8 (Automated tools available)
- Affected Users: 10 (All users' data)
- Discoverability: 9 (Common vulnerability)
- **Risk Score:** 9.2 (Critical)

---

### Attack Trees

**Visual threat modeling technique showing attack paths**

**Example: Compromise Web Application**

```
                    Compromise Web Application (GOAL)
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   Exploit SQLi        Steal Credentials      Exploit Vuln Dependency
        │                     │                     │
    ┌───┴───┐           ┌─────┴─────┐         ┌────┴────┐
    │       │           │           │         │         │
Find Input Bypass  Phishing   Credential  Find Vuln  Exploit
Validation WAF     Email      Stuffing    Lib       Outdated
                                                     Library
    │       │           │           │         │         │
    ▼       ▼           ▼           ▼         ▼         ▼
 [TEST]  [TEST]      [TEST]      [TEST]    [SCAN]    [EXPLOIT]
```

**Attack Tree Analysis:**
- **AND gates:** All child nodes must succeed for parent to succeed
- **OR gates:** Any child node success leads to parent success
- **Leaf nodes:** Atomic actions (test, scan, exploit)

---

## Security Controls Mapping

### NIST Cybersecurity Framework (CSF) 2.0

**Structure:** 6 Functions, 23 Categories, 106 Subcategories

**Functions:**

**1. GOVERN (GV)** - NEW in CSF 2.0
- Organizational context, risk management strategy, roles/responsibilities
- Supply chain risk management
- Cybersecurity policies and procedures

**2. IDENTIFY (ID)**
- Asset Management: Inventory of devices, data, personnel, facilities
- Risk Assessment: Identify and prioritize cybersecurity risks
- Improvement: Continuous improvement processes

**3. PROTECT (PR)**
- Identity Management & Access Control: MFA, least privilege, PAM
- Data Security: Encryption, DLP, data classification
- Platform Security: Secure configurations, patch management
- Technology Infrastructure Resilience: Backup, failover, redundancy

**4. DETECT (DE)**
- Continuous Monitoring: Network, endpoint, log monitoring
- Adverse Event Analysis: Detect anomalies and indicators of compromise
- Security Continuous Monitoring: SIEM, IDS/IPS

**5. RESPOND (RS)**
- Incident Management: Incident response plan, communication, containment
- Incident Analysis: Root cause analysis, lessons learned
- Incident Response Reporting and Communication

**6. RECOVER (RC)**
- Incident Recovery Plan Execution: Restore operations
- Incident Recovery Communication: Stakeholder updates
- Improvement post-incident: Update plans based on lessons learned

---

### CIS Critical Security Controls v8

**18 Controls organized in 3 Implementation Groups:**

**IG1 (Basic Cyber Hygiene) - 56 Safeguards:**
1. Inventory and Control of Enterprise Assets
2. Inventory and Control of Software Assets
3. Data Protection
4. Secure Configuration of Enterprise Assets and Software
5. Account Management
6. Access Control Management
7. Continuous Vulnerability Management
8. Audit Log Management
9. Email and Web Browser Protections
10. Malware Defenses
11. Data Recovery
12. Network Infrastructure Management
13. Network Monitoring and Defense
14. Security Awareness and Skills Training
15. Service Provider Management
16. Application Software Security
17. Incident Response Management
18. Penetration Testing

**IG2 (Intermediate) - +74 Safeguards (130 total):**
- More sophisticated controls for organizations with IT security staff

**IG3 (Advanced) - +23 Safeguards (153 total):**
- Advanced controls for organizations with dedicated security teams

---

### OWASP Top 10 to Controls Mapping

| OWASP Risk | Primary Control | NIST CSF Category | CIS Control |
|------------|-----------------|-------------------|-------------|
| **A1: Injection** | Input validation, parameterized queries | PR.DS (Data Security) | 16 (App Security) |
| **A2: Broken Authentication** | MFA, secure session management | PR.AC (Access Control) | 5, 6 (Account, Access Mgmt) |
| **A3: Sensitive Data Exposure** | Encryption, key management | PR.DS (Data Security) | 3 (Data Protection) |
| **A4: XXE** | Disable external entities, use JSON | PR.DS (Data Security) | 16 (App Security) |
| **A5: Broken Access Control** | Authorization checks, RBAC | PR.AC (Access Control) | 6 (Access Control) |
| **A6: Security Misconfiguration** | Hardening, minimal configs | PR.IP (Protective Tech) | 4 (Secure Configuration) |
| **A7: XSS** | Output encoding, CSP | PR.DS (Data Security) | 16 (App Security) |
| **A8: Insecure Deserialization** | Validate objects, safe formats | PR.DS (Data Security) | 16 (App Security) |
| **A9: Known Vulnerabilities** | Patch management, SBOM | ID.RA (Risk Assessment) | 7 (Vulnerability Mgmt) |
| **A10: Logging & Monitoring** | SIEM, centralized logging | DE.CM (Continuous Monitoring) | 8 (Audit Log Mgmt) |

---

## Supply Chain Security

### SLSA Framework

**Supply-chain Levels for Software Artifacts**

**Developed by:** Google (Open Source Security Foundation)

**Purpose:** Protect against supply chain attacks (tampering, backdoors, compromised build processes)

**4 Levels (Progressive security guarantees):**

**SLSA Level 1: Provenance**
- Build process generates provenance metadata
- Documents how artifact was built
- Not tamper-proof

**SLSA Level 2: Hosted Build Platform**
- Build on trusted, hosted service (GitHub Actions, Cloud Build)
- Provenance is generated by trusted platform
- Stronger assurance than self-hosted builds

**SLSA Level 3: Hardened Build Platform**
- Build platform prevents compromises
- Provenance generation cannot be tampered with
- Audit logs of build process

**SLSA Level 4: Hermetic, Reproducible Builds**
- Fully hermetic builds (no network access during build)
- Reproducible builds (same inputs = same output)
- Two-party review for all changes
- Highest supply chain security

**SLSA Requirements:**

| Requirement | L1 | L2 | L3 | L4 |
|-------------|----|----|----|----|
| Provenance exists | ✓ | ✓ | ✓ | ✓ |
| Hosted build platform | | ✓ | ✓ | ✓ |
| Build service hardened | | | ✓ | ✓ |
| Provenance non-falsifiable | | | ✓ | ✓ |
| Isolated build process | | | | ✓ |
| Hermetic builds | | | | ✓ |
| Reproducible builds | | | | ✓ |

---

### SBOM (Software Bill of Materials)

**Definition:** Inventory of software components and dependencies

**Standards:**
- **SPDX** (Software Package Data Exchange) - Linux Foundation
- **CycloneDX** - OWASP standard
- **SWID** (Software Identification Tags) - ISO/IEC 19770-2

**SBOM Contents:**
- Component name, version, license
- Supplier/author information
- Dependencies and relationships
- Known vulnerabilities (CVEs)
- Hash/checksum for integrity

**SBOM Use Cases:**
1. **Vulnerability Management:** Quickly identify affected components
2. **License Compliance:** Track open-source licenses
3. **Supply Chain Risk:** Visibility into third-party code
4. **Incident Response:** Rapid assessment of Log4Shell-type incidents

**CycloneDX Example (JSON):**
```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "version": 1,
  "metadata": {
    "component": {
      "type": "application",
      "name": "my-app",
      "version": "1.0.0"
    }
  },
  "components": [
    {
      "type": "library",
      "name": "express",
      "version": "4.18.2",
      "purl": "pkg:npm/express@4.18.2",
      "licenses": [{"license": {"id": "MIT"}}]
    },
    {
      "type": "library",
      "name": "lodash",
      "version": "4.17.21",
      "purl": "pkg:npm/lodash@4.17.21",
      "licenses": [{"license": {"id": "MIT"}}]
    }
  ],
  "dependencies": [
    {
      "ref": "pkg:npm/express@4.18.2",
      "dependsOn": ["pkg:npm/lodash@4.17.21"]
    }
  ]
}
```

---

### Dependency Scanning & Management

**Tools:**

| Tool | Language Support | Features | Best For |
|------|------------------|----------|----------|
| **Dependabot** | Multi-language | Automated PRs, GitHub native | GitHub users |
| **Snyk** | Multi-language | Vuln scanning, license compliance | Developers |
| **OWASP Dependency-Check** | Java, .NET, Python, Ruby | CVE scanning, CLI/CI | Open-source projects |
| **Renovate** | Multi-language | Automated updates, flexible | Advanced automation |
| **Trivy** | Multi-language, containers | CVE scanning, misconfig | Containers & IaC |
| **Grype** | Multi-language, containers | Fast CVE scanning | CI/CD pipelines |

**Dependency Management Best Practices:**
1. **Generate SBOM:** Automated SBOM generation in CI/CD
2. **Continuous Scanning:** Scan on every commit and nightly
3. **Automated Updates:** Use Dependabot/Renovate for security patches
4. **License Compliance:** Track and approve open-source licenses
5. **Vendor Monitoring:** Subscribe to security advisories
6. **Minimize Dependencies:** Fewer dependencies = smaller attack surface
7. **Pin Versions:** Use lock files (package-lock.json, Pipfile.lock)

---

## Cloud Security Architecture

### AWS Security Architecture

**AWS Well-Architected Framework - Security Pillar**

**5 Design Principles:**
1. **Implement a strong identity foundation:** Centralize IAM, least privilege
2. **Enable traceability:** Log and monitor all actions
3. **Apply security at all layers:** Defense in depth
4. **Automate security best practices:** Infrastructure as Code
5. **Protect data in transit and at rest:** Encryption everywhere

**Key AWS Security Services:**

| Category | Service | Purpose |
|----------|---------|---------|
| **IAM** | AWS IAM | Identity and access management |
|         | AWS IAM Identity Center | SSO for multi-account |
|         | AWS Cognito | User authentication for apps |
| **Detection** | Amazon GuardDuty | Threat detection (ML-based) |
|               | AWS Security Hub | Centralized security findings |
|               | Amazon Detective | Incident investigation |
| **Network** | AWS WAF | Web application firewall |
|             | AWS Shield | DDoS protection |
|             | AWS Network Firewall | Stateful network firewall |
| **Data** | AWS KMS | Key management service |
|          | AWS Secrets Manager | Secrets rotation |
|          | Amazon Macie | Data discovery & classification |
| **Compute** | AWS Systems Manager | Patch management, config |
|             | Amazon Inspector | Vulnerability scanning |

**AWS Multi-Account Security Architecture:**

```
┌────────────────────────────────────────────────────────┐
│           AWS Organizations (Root)                     │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │       Security OU (Organizational Unit)          │ │
│  │  ┌────────────┐  ┌────────────┐  ┌───────────┐  │ │
│  │  │ Security   │  │   Logging  │  │  Audit    │  │ │
│  │  │  Account   │  │   Account  │  │  Account  │  │ │
│  │  └─────┬──────┘  └──────┬─────┘  └─────┬─────┘  │ │
│  └────────┼─────────────────┼──────────────┼────────┘ │
│           │                 │              │          │
│  ┌────────▼─────────────────▼──────────────▼────────┐ │
│  │     Workload OU (Production)                     │ │
│  │  ┌────────────┐  ┌────────────┐  ┌───────────┐  │ │
│  │  │    App1    │  │    App2    │  │    App3   │  │ │
│  │  │   Prod     │  │   Prod     │  │   Prod    │  │ │
│  │  └────────────┘  └────────────┘  └───────────┘  │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │     Workload OU (Non-Production)                 │ │
│  │  ┌────────────┐  ┌────────────┐  ┌───────────┐  │ │
│  │  │    Dev     │  │   Staging  │  │    Test   │  │ │
│  │  └────────────┘  └────────────┘  └───────────┘  │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘

Security Controls Applied via SCPs (Service Control Policies)
IAM Identity Center provides SSO across all accounts
GuardDuty/Security Hub enabled organization-wide
Centralized logging to Logging Account (S3 + CloudWatch)
```

---

### GCP Security Architecture

**GCP Security Best Practices**

**Key GCP Security Services:**

| Category | Service | Purpose |
|----------|---------|---------|
| **IAM** | Cloud IAM | Identity and access management |
|         | Identity Platform | Customer identity (CIAM) |
|         | Cloud Identity | Workforce identity |
| **Detection** | Security Command Center | Unified security & risk dashboard |
|               | Chronicle | SIEM and threat intelligence |
|               | Event Threat Detection | Real-time threat detection |
| **Network** | Cloud Armor | DDoS & WAF |
|             | VPC Service Controls | Data exfiltration prevention |
|             | Cloud Firewall | Stateful firewall |
| **Data** | Cloud KMS | Key management |
|          | Secret Manager | Secrets management |
|          | Cloud DLP | Data loss prevention |
| **Compute** | Binary Authorization | Container image signing |
|             | Confidential Computing | Encryption in use |

**GCP Organization Hierarchy:**

```
Organization (example.com)
  │
  ├── Folder: Production
  │     ├── Project: prod-app1
  │     ├── Project: prod-app2
  │     └── Project: prod-shared-services
  │
  ├── Folder: Non-Production
  │     ├── Project: dev-app1
  │     ├── Project: staging-app1
  │     └── Project: test-app1
  │
  └── Folder: Security
        ├── Project: security-logging
        └── Project: security-monitoring

IAM Policies inherited down hierarchy
Security Command Center scans entire organization
VPC Service Controls protect sensitive projects
```

---

### Azure Security Architecture

**Microsoft Defender for Cloud (formerly Azure Security Center)**

**Key Azure Security Services:**

| Category | Service | Purpose |
|----------|---------|---------|
| **IAM** | Azure AD (Entra ID) | Identity platform |
|         | Privileged Identity Management | JIT access for admins |
|         | Conditional Access | Risk-based access |
| **Detection** | Microsoft Defender for Cloud | CSPM & CWPP |
|               | Microsoft Sentinel | SIEM & SOAR |
|               | Azure Monitor | Logging & metrics |
| **Network** | Azure Firewall | Stateful firewall |
|             | Azure Front Door + WAF | Global CDN & WAF |
|             | Azure DDoS Protection | DDoS mitigation |
| **Data** | Azure Key Vault | Secrets, keys, certificates |
|          | Azure Information Protection | Data classification & DLP |
|          | Storage encryption | At-rest encryption |
| **Compute** | Just-in-Time VM Access | JIT SSH/RDP |
|             | Azure Policy | Compliance enforcement |

**Azure Landing Zone Architecture (Hub-Spoke):**

```
┌────────────────────────────────────────────────────────┐
│              Azure AD Tenant (Root)                    │
│                                                        │
│  Management Groups Hierarchy:                         │
│    Root → Platform → Landing Zones → Applications     │
└────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼─────┐      ┌─────▼─────┐     ┌─────▼─────┐
   │   Hub    │      │  Spoke 1  │     │  Spoke 2  │
   │  VNet    │      │   (Prod)  │     │   (Dev)   │
   │          │      │           │     │           │
   │ Firewall │      │  App VMs  │     │  App VMs  │
   │   VPN    │◄────►│  Subnets  │     │  Subnets  │
   │  Azure  │      │           │     │           │
   │  Bastion│      └───────────┘     └───────────┘
   └──────────┘
        │
   ┌────▼────────────────────────────────┐
   │  Shared Services Subscription       │
   │  - Defender for Cloud               │
   │  - Azure Monitor / Log Analytics    │
   │  - Azure Sentinel                   │
   └─────────────────────────────────────┘
```

---

## Framework Recommendations

### Primary Frameworks by Use Case

| Use Case | Framework | Why |
|----------|-----------|-----|
| **General Security Program** | NIST CSF 2.0 | Industry standard, risk-based, flexible |
| **Compliance Baseline** | CIS Controls v8 | Prescriptive, measurable, prioritized |
| **ISO Certification** | ISO 27001/27002 | International standard for ISMS |
| **Application Security** | OWASP ASVS | Comprehensive app security verification |
| **Cloud Security** | Cloud provider frameworks | AWS/GCP/Azure Well-Architected |
| **Supply Chain Security** | SLSA + SBOM | Protect software supply chain |
| **Zero Trust** | NIST SP 800-207 | Zero Trust Architecture guidelines |
| **Privacy & GDPR** | NIST Privacy Framework | Privacy controls and compliance |

---

### Security Tools Ecosystem

**Detection & Response:**
- **SIEM:** Splunk, Elastic Security, Microsoft Sentinel, Chronicle
- **EDR:** CrowdStrike Falcon, Microsoft Defender for Endpoint, SentinelOne
- **XDR:** Palo Alto Cortex XDR, Trend Micro Vision One
- **SOAR:** Splunk SOAR, Palo Alto Cortex XSOAR, IBM Resilient

**Vulnerability Management:**
- **Scanners:** Tenable Nessus, Qualys, Rapid7 InsightVM
- **DAST:** OWASP ZAP, Burp Suite, Acunetix
- **SAST:** SonarQube, Checkmarx, Veracode
- **Container Scanning:** Trivy, Grype, Snyk, Aqua Security

**Identity & Access:**
- **IAM Platforms:** Okta, Azure AD, Ping Identity, Auth0
- **PAM:** CyberArk, BeyondTrust, Delinea (Thycotic)
- **MFA:** Duo, Okta, Microsoft Authenticator, YubiKey

**Cloud Security:**
- **CSPM:** Wiz, Orca Security, Prisma Cloud (Palo Alto)
- **CWPP:** Aqua Security, Prisma Cloud, Sysdig Secure
- **CNAPP:** Wiz, Orca, Palo Alto Prisma Cloud (converged CSPM + CWPP)

**Network Security:**
- **NGFW:** Palo Alto Networks, Fortinet FortiGate, Cisco Firepower
- **WAF:** Cloudflare, Imperva, F5, AWS WAF
- **ZTNA:** Zscaler Private Access, Palo Alto Prisma Access, Cloudflare Access

---

## Skill Structure Design

```
security-architecture/
├── SKILL.md                              # Main skill (600-800 lines)
│   ├── Purpose and when to use
│   ├── Core principles (Defense in Depth, Zero Trust)
│   ├── Threat modeling overview (STRIDE, PASTA)
│   ├── Quick reference: Control frameworks
│   ├── Progressive disclosure pointers to references/
│
├── references/
│   ├── defense-in-depth.md               # 9-layer DiD model, patterns
│   ├── zero-trust-architecture.md        # ZTA principles, implementation
│   ├── threat-modeling.md                # STRIDE, PASTA, DREAD, Attack Trees
│   ├── nist-csf-mapping.md               # NIST CSF functions, categories
│   ├── cis-controls.md                   # CIS Controls v8, implementation groups
│   ├── owasp-top10-mitigation.md         # OWASP Top 10 + controls mapping
│   ├── supply-chain-security.md          # SLSA, SBOM, dependency scanning
│   ├── aws-security-architecture.md      # AWS reference architectures
│   ├── gcp-security-architecture.md      # GCP reference architectures
│   ├── azure-security-architecture.md    # Azure reference architectures
│   ├── iam-patterns.md                   # IAM, MFA, RBAC/ABAC, PAM
│   └── security-operations.md            # SIEM, SOAR, incident response
│
├── examples/
│   ├── threat-models/
│   │   ├── web-app-stride.md             # Web app STRIDE analysis
│   │   ├── api-threat-model.md           # REST API threat model
│   │   └── microservices-threat-model.md # Microservices threat model
│   ├── architectures/
│   │   ├── aws-multi-account-security.md # AWS Org security setup
│   │   ├── gcp-security-hierarchy.md     # GCP folder/project security
│   │   ├── azure-landing-zone.md         # Azure hub-spoke landing zone
│   │   └── zero-trust-network.md         # Zero trust network design
│   └── control-mappings/
│       ├── nist-to-cis.md                # NIST CSF to CIS Controls
│       ├── owasp-to-nist.md              # OWASP Top 10 to NIST CSF
│       └── iso27001-to-cis.md            # ISO 27001 to CIS Controls
│
└── scripts/
    ├── threat-model-template.py          # Generate STRIDE template
    ├── control-gap-analysis.sh           # Compare controls vs frameworks
    ├── sbom-generate.sh                  # Generate SBOM (CycloneDX)
    └── security-checklist.sh             # Automated security checklist
```

---

## Integration Points

### With Existing Skills

| Skill | Integration Point |
|-------|-------------------|
| `infrastructure-as-code` | IaC security hardening, secure defaults |
| `kubernetes-operations` | K8s security contexts, RBAC, Pod Security |
| `secret-management` | Secrets architecture, KMS integration |
| `building-ci-pipelines` | Secure CI/CD, SAST/DAST integration |
| `configuring-firewalls` | Network security layer of DiD |
| `vulnerability-management` | Vuln scanning in security architecture |
| `auth-security` | IAM layer implementation details |
| `observability` | Security monitoring, logging architecture |

### Skill Chaining Example

```
security-architecture → infrastructure-as-code → kubernetes-operations
         │                       │                        │
         ▼                       ▼                        ▼
  Design security       Implement secure       Deploy secure
  controls & layers     infrastructure via     workloads with
  (Zero Trust + DiD)    Terraform/Pulumi       RBAC + Network Policies
         │                       │                        │
         └───────────────────────┴────────────────────────┘
                                 │
                                 ▼
                    secret-management + observability
                          │                │
                          ▼                ▼
                    Secure secrets    Monitor & detect
                    in Vault/KMS      threats via SIEM
```

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [x] Research defense in depth and zero trust (Google Search Grounding)
- [x] Research OWASP security patterns (Context7)
- [ ] Document core security architecture principles
- [ ] Create STRIDE and PASTA threat modeling guides
- [ ] Design 9-layer defense in depth reference

### Phase 2: Frameworks (Weeks 3-4)
- [ ] NIST CSF 2.0 detailed mapping
- [ ] CIS Controls v8 implementation guidance
- [ ] OWASP Top 10 to controls mapping
- [ ] ISO 27001/27002 control families

### Phase 3: Cloud Security (Weeks 5-6)
- [ ] AWS Well-Architected Security Pillar patterns
- [ ] GCP Security Command Center architecture
- [ ] Azure Defender for Cloud reference architectures
- [ ] Multi-cloud security posture management

### Phase 4: Zero Trust & Supply Chain (Weeks 7-8)
- [ ] Zero trust reference architecture (detailed)
- [ ] Zero trust implementation roadmap
- [ ] SLSA framework implementation guide
- [ ] SBOM generation and management
- [ ] Dependency scanning automation

### Phase 5: Examples & Automation (Weeks 9-10)
- [ ] Threat model examples (web app, API, microservices)
- [ ] Cloud security architecture examples
- [ ] Threat modeling scripts (templates, automation)
- [ ] Security checklist automation
- [ ] Control gap analysis tooling

### Phase 6: Integration & Polish (Weeks 11-12)
- [ ] Integration with related skills (IaC, K8s, secrets)
- [ ] SKILL.md creation (progressive disclosure)
- [ ] Review and validation
- [ ] Documentation polish

---

## Key Takeaways

1. **Security is Architectural:** Security cannot be bolted on; it must be designed into systems from the start
2. **Defense in Depth:** Multiple layers of security controls provide redundancy and resilience
3. **Zero Trust:** "Never trust, always verify" is the modern security paradigm for cloud and hybrid environments
4. **Threat Modeling:** Systematic threat identification (STRIDE, PASTA) enables proactive security
5. **Framework Alignment:** Map security controls to frameworks (NIST CSF, CIS Controls) for compliance and completeness
6. **Supply Chain Security:** Modern attacks target the supply chain (SLSA, SBOM critical)
7. **Cloud-Native Security:** Cloud requires new architectural patterns (CSPM, CWPP, IAM-first)
8. **Continuous Verification:** Security is continuous, not point-in-time (monitoring, detection, response)

---

**Progressive Disclosure:** This init.md provides the comprehensive master plan for the security-architecture skill. Detailed reference documentation will be organized in `references/` directory. SKILL.md (to be created) will provide high-level guidance with pointers to detailed references.

**Next Step:** Create SKILL.md following Anthropic's skill-creator 6-step process (concrete examples first, plan resources, write skill, add bundled resources, validate, iterate).
