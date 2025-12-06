# NIST Cybersecurity Framework (CSF) 2.0 Reference


## Table of Contents

- [Overview](#overview)
- [Framework Structure](#framework-structure)
- [6 Core Functions](#6-core-functions)
  - [GOVERN (GV) - NEW in CSF 2.0](#govern-gv-new-in-csf-20)
  - [IDENTIFY (ID)](#identify-id)
  - [PROTECT (PR)](#protect-pr)
  - [DETECT (DE)](#detect-de)
  - [RESPOND (RS)](#respond-rs)
  - [RECOVER (RC)](#recover-rc)
- [NIST CSF Implementation Tiers](#nist-csf-implementation-tiers)
- [NIST CSF Profiles](#nist-csf-profiles)
- [Control Mapping Examples](#control-mapping-examples)
  - [Mapping OWASP Top 10 to NIST CSF](#mapping-owasp-top-10-to-nist-csf)
  - [Mapping CIS Controls to NIST CSF](#mapping-cis-controls-to-nist-csf)
  - [Mapping Cloud Security to NIST CSF (AWS Example)](#mapping-cloud-security-to-nist-csf-aws-example)
- [Implementation Roadmap](#implementation-roadmap)
  - [Phase 1: Assess Current State (Weeks 1-4)](#phase-1-assess-current-state-weeks-1-4)
  - [Phase 2: Define Target State (Weeks 5-6)](#phase-2-define-target-state-weeks-5-6)
  - [Phase 3: Gap Analysis (Weeks 7-8)](#phase-3-gap-analysis-weeks-7-8)
  - [Phase 4: Implement Controls (Months 3-12)](#phase-4-implement-controls-months-3-12)
  - [Phase 5: Continuous Improvement (Ongoing)](#phase-5-continuous-improvement-ongoing)
- [NIST CSF vs Other Frameworks](#nist-csf-vs-other-frameworks)
- [Summary](#summary)

## Overview

The NIST Cybersecurity Framework provides a risk-based approach to managing cybersecurity risks. Version 2.0 (released 2024) introduces the GOVERN function and expands scope to all organizations.

**Official Source:** NIST CSF 2.0 (https://www.nist.gov/cyberframework)

## Framework Structure

**Hierarchy:**
- 6 Functions (high-level categories)
- 23 Categories (specific outcomes)
- 106 Subcategories (detailed controls)

## 6 Core Functions

### GOVERN (GV) - NEW in CSF 2.0

**Purpose:** Establish and monitor cybersecurity governance, risk management strategy, and policies.

**Categories:**
- **GV.OC:** Organizational Context
- **GV.RM:** Risk Management Strategy
- **GV.RR:** Roles, Responsibilities, and Authorities
- **GV.PO:** Policy
- **GV.OV:** Oversight
- **GV.SC:** Cybersecurity Supply Chain Risk Management

**Key Controls:**
- Establish cybersecurity governance structure
- Define risk tolerance and risk appetite
- Assign cybersecurity roles and responsibilities
- Develop security policies and procedures
- Supply chain risk management program
- Third-party risk assessments

---

### IDENTIFY (ID)

**Purpose:** Develop organizational understanding to manage cybersecurity risk to systems, people, assets, data, and capabilities.

**Categories:**
- **ID.AM:** Asset Management
- **ID.RA:** Risk Assessment
- **ID.IM:** Improvement

**Key Controls:**

**ID.AM (Asset Management):**
- Hardware asset inventory (servers, workstations, network devices, IoT)
- Software asset inventory (applications, operating systems, firmware)
- Data asset classification (public, internal, confidential, restricted)
- Personnel inventory (employees, contractors, privileged users)
- Network architecture documentation (network diagrams, data flows)

**ID.RA (Risk Assessment):**
- Identify and document cybersecurity risks
- Threat intelligence integration
- Vulnerability assessments (continuous scanning)
- Risk prioritization (likelihood × impact)
- Critical asset identification

**ID.IM (Improvement):**
- Lessons learned from incidents
- Continuous improvement processes
- Security metrics and KPIs

---

### PROTECT (PR)

**Purpose:** Develop and implement appropriate safeguards to ensure delivery of critical services.

**Categories:**
- **PR.AA:** Identity Management, Authentication and Access Control
- **PR.AT:** Awareness and Training
- **PR.DS:** Data Security
- **PR.IP:** Platform Security
- **PR.MA:** Maintenance
- **PR.PS:** Technology Infrastructure Resilience

**Key Controls:**

**PR.AA (Access Control):**
- Identity and credential management
- Multi-factor authentication (MFA)
- Role-based access control (RBAC)
- Privileged access management (PAM)
- Remote access management (ZTNA, VPN)

**PR.DS (Data Security):**
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- Data loss prevention (DLP)
- Key management (HSM, KMS)
- Secure data disposal

**PR.IP (Platform Security):**
- Configuration management and hardening
- Secure software development lifecycle (SDLC)
- Security testing (SAST, DAST, SCA)
- Change control processes
- Baseline security configurations (CIS Benchmarks)

**PR.MA (Maintenance):**
- Patch management (automated, risk-based)
- Remote maintenance security
- Asset maintenance logs

**PR.PS (Technology Infrastructure Resilience):**
- Backup and recovery (3-2-1 rule)
- Redundancy and failover
- Capacity planning
- Business continuity planning

---

### DETECT (DE)

**Purpose:** Develop and implement appropriate activities to identify occurrence of cybersecurity events.

**Categories:**
- **DE.AE:** Adverse Event Analysis
- **DE.CM:** Continuous Security Monitoring

**Key Controls:**

**DE.AE (Adverse Event Analysis):**
- Baseline network and system behavior
- Anomaly detection (UEBA, ML-based)
- Security event correlation (SIEM)
- Threat intelligence integration
- Alert prioritization and triage

**DE.CM (Continuous Monitoring):**
- Network monitoring (IDS/IPS, flow logs)
- Endpoint monitoring (EDR)
- Application monitoring (WAF logs, application logs)
- Cloud security monitoring (GuardDuty, Security Command Center)
- Vulnerability scanning (continuous, risk-based)
- Physical access monitoring

---

### RESPOND (RS)

**Purpose:** Develop and implement appropriate activities to take action regarding detected cybersecurity incidents.

**Categories:**
- **RS.MA:** Incident Management
- **RS.AN:** Incident Analysis
- **RS.RP:** Incident Response Reporting and Communication
- **RS.MI:** Incident Mitigation

**Key Controls:**

**RS.MA (Incident Management):**
- Incident response plan (documented, tested)
- Incident response team and roles (CSIRT)
- Incident detection and reporting mechanisms
- Incident categorization and prioritization

**RS.AN (Incident Analysis):**
- Forensic analysis capabilities
- Root cause analysis
- Impact assessment
- Threat intelligence enrichment

**RS.MI (Incident Mitigation):**
- Containment strategies (isolate, quarantine)
- Eradication procedures (remove malware, close vulnerabilities)
- Recovery procedures (restore systems, validate integrity)
- Lessons learned and post-incident review

---

### RECOVER (RC)

**Purpose:** Develop and implement appropriate activities to maintain resilience and restore capabilities or services impaired by cybersecurity incidents.

**Categories:**
- **RC.RP:** Recovery Planning
- **RC.CO:** Recovery Communications

**Key Controls:**

**RC.RP (Recovery Planning):**
- Recovery plan development and maintenance
- Recovery testing (tabletop exercises, full simulations)
- Backup restoration procedures
- Business continuity and disaster recovery (BC/DR)
- Recovery time objectives (RTO) and recovery point objectives (RPO)

**RC.CO (Recovery Communications):**
- Internal communication plans (employees, management)
- External communication plans (customers, regulators, media)
- Stakeholder coordination
- Public relations and reputation management

---

## NIST CSF Implementation Tiers

**Tier 1: Partial**
- Ad-hoc, reactive security
- Limited awareness of cybersecurity risk
- Cybersecurity risk management not formalized

**Tier 2: Risk Informed**
- Risk management practices approved by management but not organization-wide
- Some awareness of cybersecurity risk
- Informal processes

**Tier 3: Repeatable**
- Formal cybersecurity policies and procedures
- Organization-wide risk management program
- Regular risk assessments
- Consistent implementation

**Tier 4: Adaptive**
- Continuous improvement culture
- Advanced threat intelligence integration
- Real-time risk assessment and response
- Predictive indicators and adaptive processes

---

## NIST CSF Profiles

**Current Profile:** Current state of cybersecurity posture (as-is)

**Target Profile:** Desired state of cybersecurity posture (to-be)

**Gap Analysis:** Difference between Current and Target profiles

**Roadmap:** Plan to close gaps and achieve Target profile

---

## Control Mapping Examples

### Mapping OWASP Top 10 to NIST CSF

| OWASP Risk | NIST CSF Function | Category | Example Control |
|------------|-------------------|----------|-----------------|
| **A01: Broken Access Control** | PROTECT | PR.AA | Implement RBAC, least privilege |
| **A02: Cryptographic Failures** | PROTECT | PR.DS | Encryption at rest/transit, key management |
| **A03: Injection** | PROTECT | PR.IP | Input validation, parameterized queries |
| **A04: Insecure Design** | IDENTIFY | ID.RA | Threat modeling, security by design |
| **A05: Security Misconfiguration** | PROTECT | PR.IP | Configuration management, hardening |
| **A06: Vulnerable Components** | IDENTIFY | ID.RA | SCA scanning, dependency management |
| **A07: Authentication Failures** | PROTECT | PR.AA | MFA, secure session management |
| **A08: Software/Data Integrity** | PROTECT | PR.DS | Code signing, integrity checks |
| **A09: Logging/Monitoring Failures** | DETECT | DE.CM | SIEM, centralized logging |
| **A10: Server-Side Request Forgery** | PROTECT | PR.IP | Input validation, network segmentation |

---

### Mapping CIS Controls to NIST CSF

| CIS Control | NIST CSF Function | Category |
|-------------|-------------------|----------|
| **CIS 1: Asset Inventory** | IDENTIFY | ID.AM |
| **CIS 2: Software Inventory** | IDENTIFY | ID.AM |
| **CIS 3: Data Protection** | PROTECT | PR.DS |
| **CIS 4: Secure Configuration** | PROTECT | PR.IP |
| **CIS 5: Account Management** | PROTECT | PR.AA |
| **CIS 6: Access Control** | PROTECT | PR.AA |
| **CIS 7: Vulnerability Management** | IDENTIFY | ID.RA |
| **CIS 8: Audit Log Management** | DETECT | DE.CM |
| **CIS 9: Email/Web Protection** | PROTECT | PR.IP |
| **CIS 10: Malware Defenses** | PROTECT | PR.IP |
| **CIS 11: Data Recovery** | RECOVER | RC.RP |
| **CIS 12: Network Infrastructure** | PROTECT | PR.PS |
| **CIS 13: Network Monitoring** | DETECT | DE.CM |
| **CIS 14: Security Awareness** | PROTECT | PR.AT |
| **CIS 15: Service Provider Mgmt** | GOVERN | GV.SC |
| **CIS 16: Application Security** | PROTECT | PR.IP |
| **CIS 17: Incident Response** | RESPOND | RS.MA |
| **CIS 18: Penetration Testing** | IDENTIFY | ID.RA |

---

### Mapping Cloud Security to NIST CSF (AWS Example)

| AWS Service | NIST CSF Function | Category | Purpose |
|-------------|-------------------|----------|---------|
| **IAM, IAM Identity Center** | PROTECT | PR.AA | Identity and access management |
| **GuardDuty** | DETECT | DE.CM | Threat detection |
| **Security Hub** | DETECT | DE.AE | Centralized security findings |
| **KMS** | PROTECT | PR.DS | Key management |
| **WAF** | PROTECT | PR.IP | Web application firewall |
| **Shield** | PROTECT | PR.PS | DDoS protection |
| **CloudTrail** | DETECT | DE.CM | Audit logging |
| **Config** | PROTECT | PR.IP | Configuration management |
| **Inspector** | IDENTIFY | ID.RA | Vulnerability assessment |
| **Macie** | PROTECT | PR.DS | Data discovery and classification |
| **Systems Manager** | PROTECT | PR.MA | Patch management |
| **Backup** | RECOVER | RC.RP | Backup and recovery |

---

## Implementation Roadmap

### Phase 1: Assess Current State (Weeks 1-4)

1. Conduct cybersecurity risk assessment
2. Document current security controls (Current Profile)
3. Map existing controls to NIST CSF categories
4. Identify gaps and weaknesses

### Phase 2: Define Target State (Weeks 5-6)

1. Define security objectives based on business goals
2. Determine acceptable risk levels (risk appetite)
3. Define Target Profile (desired security posture)
4. Select appropriate Implementation Tier

### Phase 3: Gap Analysis (Weeks 7-8)

1. Compare Current Profile vs. Target Profile
2. Prioritize gaps by risk and business impact
3. Estimate resources and budget for remediation
4. Develop implementation roadmap

### Phase 4: Implement Controls (Months 3-12)

1. Implement high-priority controls first
2. Track progress against roadmap
3. Update Current Profile as controls implemented
4. Regular management reporting

### Phase 5: Continuous Improvement (Ongoing)

1. Monitor security metrics and KPIs
2. Conduct periodic reassessments (annually)
3. Update Target Profile as business changes
4. Lessons learned from incidents

---

## NIST CSF vs Other Frameworks

| Aspect | NIST CSF | CIS Controls | ISO 27001 |
|--------|----------|--------------|-----------|
| **Approach** | Risk-based, flexible | Prescriptive, prioritized | Comprehensive ISMS |
| **Complexity** | Medium | Low (clear priorities) | High (formal certification) |
| **Industry Recognition** | Very high (US focus) | High | Very high (international) |
| **Certification** | No | No | Yes |
| **Cost** | Free | Free | Certification cost |
| **Best For** | Risk management, governance | Baseline security, tactical | Formal ISMS, certification |

---

## Summary

NIST CSF 2.0 provides comprehensive, risk-based framework with 6 functions: GOVERN (new), IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER. Use for security program governance, compliance mapping, and continuous improvement. Implement through phased approach: Assess → Define Target → Gap Analysis → Implement → Improve.

Map NIST CSF to tactical frameworks (CIS Controls for implementation, OWASP for app security, cloud provider frameworks for cloud security). Track progress with Current Profile → Target Profile comparison and Implementation Tiers (1-4).
