# Threat Modeling Reference

## Table of Contents

1. [Overview](#overview)
2. [STRIDE Methodology](#stride-methodology)
3. [PASTA Methodology](#pasta-methodology)
4. [DREAD Risk Scoring](#dread-risk-scoring)
5. [Attack Trees](#attack-trees)
6. [Methodology Selection Guide](#methodology-selection-guide)

## Overview

Threat modeling systematically identifies, analyzes, and prioritizes security threats to design appropriate mitigations proactively.

**When to Threat Model:**
- Designing new applications or systems
- Making significant architecture changes
- Entering new threat environments (cloud migration, IoT deployment)
- Regulatory compliance requirements (PCI DSS, HIPAA)
- After security incidents (lessons learned)

**Threat Modeling Process:**
1. Model the system (data flow diagrams, architecture diagrams)
2. Identify threats (apply methodology - STRIDE, PASTA)
3. Prioritize threats (risk scoring - DREAD, business impact)
4. Design mitigations (security controls)
5. Validate mitigations (testing, review)
6. Document and maintain (living document, update regularly)

---

## STRIDE Methodology

**Developed by:** Microsoft (Loren Kohnfelder and Praerit Garg, 1999)

**Purpose:** Systematic threat identification using 6 threat categories

**Complexity:** Low (accessible to development teams)

### STRIDE Threat Categories

#### S - Spoofing Identity

**Definition:** Attacker pretends to be someone else (user, service, system)

**Examples:**
- Phishing emails impersonating legitimate senders
- Session hijacking (stealing session tokens)
- Credential theft and replay
- Man-in-the-middle attacks
- IP address spoofing

**Mitigations:**
- Multi-factor authentication (MFA)
- Certificate validation (mutual TLS)
- Anti-phishing controls (DMARC, SPF, DKIM)
- Session token security (HttpOnly, Secure flags, short expiry)
- Strong authentication protocols (OAuth 2.0, SAML 2.0)

---

#### T - Tampering with Data

**Definition:** Unauthorized modification of data in storage or transit

**Examples:**
- SQL injection modifying database records
- Man-in-the-middle modifying network traffic
- File system tampering
- Log tampering to hide malicious activity
- Message interception and alteration

**Mitigations:**
- Encryption in transit (TLS 1.3)
- Encryption at rest (AES-256)
- Digital signatures and hashing (SHA-256, HMAC)
- Integrity checks (checksums, cryptographic hashes)
- Input validation and parameterized queries
- Immutable logs (append-only, centralized SIEM)

---

#### R - Repudiation

**Definition:** User denies performing an action, and no proof exists

**Examples:**
- "I didn't make that purchase"
- "I didn't delete that file"
- "I didn't send that email"
- "I didn't access that data"

**Mitigations:**
- Comprehensive audit logging
- Digital signatures (non-repudiation)
- Timestamping (trusted time source)
- Centralized log aggregation (SIEM)
- Tamper-proof logs (immutable storage)
- Video/session recording for critical actions

---

#### I - Information Disclosure

**Definition:** Exposure of confidential information to unauthorized parties

**Examples:**
- SQL injection revealing database contents
- Directory traversal exposing file system
- API responses leaking sensitive data
- Error messages revealing system details
- Unencrypted data transmission
- Misconfigured cloud storage (public S3 buckets)

**Mitigations:**
- Encryption (at rest, in transit, in use)
- Access control (RBAC, ABAC, least privilege)
- Data classification and DLP (Data Loss Prevention)
- Minimize data exposure (return only necessary data)
- Secure error handling (generic error messages)
- Regular security scanning (DAST, penetration testing)

---

#### D - Denial of Service

**Definition:** Making system unavailable to legitimate users

**Examples:**
- DDoS attacks (volumetric, protocol, application layer)
- Resource exhaustion (memory leaks, CPU spikes)
- Application crash exploits (buffer overflow)
- Database locking attacks
- API rate limit bypass

**Mitigations:**
- DDoS protection services (Cloudflare, AWS Shield)
- Rate limiting and throttling (API gateways)
- Resource quotas and limits (CPU, memory, connections)
- Auto-scaling (horizontal scaling under load)
- Circuit breakers and graceful degradation
- Input validation (prevent malformed requests)
- Redundancy and load balancing

---

#### E - Elevation of Privilege

**Definition:** Gaining higher privileges than authorized

**Examples:**
- Privilege escalation exploits (kernel exploits, sudo misconfigurations)
- Buffer overflow attacks
- SQL injection leading to admin access
- Insecure direct object references (IDOR)
- Misconfigured permissions (excessive IAM policies)

**Mitigations:**
- Principle of least privilege
- Input validation and sanitization
- Regular security patching
- Secure coding practices (OWASP guidelines)
- SAST/DAST scanning in CI/CD
- Role-based access control (RBAC)
- Privilege separation (run services as non-root)
- Security testing (penetration testing, fuzzing)

---

### STRIDE Application Process

**Step 1: Model the System**

Create Data Flow Diagrams (DFDs) showing:
- **External Entities:** Users, external systems, APIs
- **Processes:** Application components, services, functions
- **Data Stores:** Databases, file systems, caches
- **Data Flows:** Communication paths between components
- **Trust Boundaries:** Network perimeters, authentication boundaries

**Example DFD Elements:**
```
[User] --(HTTPS)--> [Web Server] --(SQL)--> [Database]
         │                           │
    External Entity            Process      Data Store
         │                           │
    ─────┼───────────────────────────┼────────  Trust Boundary
```

**Step 2: Identify Threats**

Apply STRIDE to each element:
- **External Entities:** Spoofing
- **Processes:** Tampering, Repudiation, Denial of Service, Elevation of Privilege
- **Data Stores:** Tampering, Information Disclosure, Denial of Service
- **Data Flows:** Tampering, Information Disclosure, Denial of Service

**Step 3: Document Threats**

Create threat list with:
- Threat ID
- STRIDE category
- Affected component
- Threat description
- Potential impact
- Proposed mitigation

**Step 4: Prioritize Threats**

Use DREAD scoring or business impact to prioritize.

**Step 5: Mitigate Threats**

Design and implement security controls.

---

### STRIDE Example: Web Application Login

| Component | Threat Type | Threat | Mitigation |
|-----------|-------------|--------|------------|
| Login page | Spoofing | Credential phishing | MFA, anti-phishing (FIDO2), user education |
| Login form | Tampering | Form field manipulation | Server-side validation, CSRF tokens |
| Authentication flow | Repudiation | User denies login | Audit logs with IP, timestamp, device info |
| Database | Info Disclosure | SQL injection exposing passwords | Parameterized queries, password hashing (bcrypt, Argon2) |
| Login endpoint | Denial of Service | Brute force attacks | Rate limiting, account lockout, CAPTCHA |
| Session management | Elevation | Session hijacking → admin access | Secure session tokens, HttpOnly/Secure flags, short expiry |

---

## PASTA Methodology

**Process for Attack Simulation and Threat Analysis**

**Developed by:** VerSprite (Tony UcedaVélez and Marco Morana)

**Purpose:** Risk-centric threat analysis aligned with business objectives

**Complexity:** High (enterprise-level, comprehensive)

### 7 Stages of PASTA

#### Stage 1: Define Business Objectives

Identify business goals, compliance requirements, and acceptable risk levels.

**Activities:**
- Document business objectives (revenue, customer trust, compliance)
- Define security objectives aligned with business (data protection, availability, integrity)
- Identify compliance requirements (GDPR, SOC 2, HIPAA, PCI DSS)
- Determine risk tolerance (risk appetite, risk thresholds)

**Output:** Business context and security objectives

---

#### Stage 2: Define Technical Scope

Inventory assets and document technical architecture.

**Activities:**
- Asset inventory (applications, databases, servers, network devices, cloud resources)
- Network architecture documentation (network diagrams, data flows)
- Identify trust boundaries (internet-facing, internal networks, DMZ)
- Document dependencies (third-party services, APIs, libraries)

**Output:** Technical scope and asset inventory

---

#### Stage 3: Application Decomposition

Break down application into components and analyze each.

**Activities:**
- Identify application components (front-end, API, database, authentication)
- Map data flows between components
- Document authentication and authorization mechanisms
- Identify entry points (user inputs, API endpoints, file uploads)
- Analyze session management

**Output:** Detailed application architecture and data flow diagrams

---

#### Stage 4: Threat Analysis

Identify threat actors and attack vectors.

**Activities:**
- Identify threat actors (cybercriminals, nation-states, insiders, competitors)
- Determine threat actor motivations (financial gain, espionage, disruption)
- Map to MITRE ATT&CK framework (tactics, techniques, procedures)
- Analyze past attack patterns (threat intelligence, incident history)
- Identify attack surfaces (internet-facing assets, supply chain)

**Output:** Threat actor profiles and attack scenarios

---

#### Stage 5: Vulnerability & Weakness Analysis

Identify vulnerabilities in the system.

**Activities:**
- Code review (SAST findings, manual review)
- DAST/penetration testing findings
- Configuration review (misconfigurations, default credentials)
- Map to CWE (Common Weakness Enumeration)
- Dependency vulnerabilities (SCA findings, SBOM analysis)

**Output:** Vulnerability inventory and weaknesses

---

#### Stage 6: Attack Modeling

Simulate attack scenarios and analyze feasibility.

**Activities:**
- Create attack trees for identified threats
- Simulate attack scenarios (walkthrough attack paths)
- Analyze attack feasibility (required skills, resources, time)
- Determine likelihood of success
- Estimate attack impact (data loss, downtime, financial)

**Output:** Attack scenarios and feasibility analysis

---

#### Stage 7: Risk & Impact Analysis

Quantify business impact and prioritize remediation.

**Activities:**
- Quantify financial impact (data breach costs, downtime costs, regulatory fines)
- Assess reputational impact (customer trust, brand damage)
- Calculate risk scores (likelihood × impact)
- Prioritize risks by business impact
- Recommend risk treatments (mitigate, accept, transfer, avoid)

**Output:** Prioritized risk list with business impact and remediation recommendations

---

### PASTA vs STRIDE Comparison

| Aspect | PASTA | STRIDE |
|--------|-------|--------|
| **Focus** | Risk-centric, business-aligned | Threat identification |
| **Complexity** | High (7 stages, comprehensive) | Low (6 categories, straightforward) |
| **Time Required** | Weeks to months | Days to weeks |
| **Output** | Prioritized risks, attack scenarios, business impact | Threat list with mitigations |
| **Best For** | Enterprise risk management, C-level reporting | Development teams, agile environments |
| **Business Alignment** | Strong (starts with business objectives) | Weak (technical focus) |

**When to Use PASTA:**
- Enterprise risk assessments
- Compliance-driven threat modeling
- C-level security reporting
- High-risk systems (financial, healthcare, critical infrastructure)

**When to Use STRIDE:**
- Development team threat modeling
- Agile/DevSecOps integration
- Quick threat identification
- Low to medium risk systems

---

## DREAD Risk Scoring

**Developed by:** Microsoft (now deprecated internally but still widely used)

**Purpose:** Quantify risk with numeric scores for prioritization

### DREAD Factors (1-10 scale)

#### D - Damage Potential

How much damage can the attack cause?

- **10:** Complete system compromise, data destruction, total business disruption
- **7-9:** Significant data loss, major service disruption, regulatory violations
- **4-6:** Information disclosure, partial denial of service, limited data loss
- **1-3:** Minor inconvenience, limited impact

**Example:**
- SQL injection exposing customer database: **9** (massive data breach)
- XSS on low-traffic page: **4** (limited user impact)

---

#### R - Reproducibility

How easily can the attack be reproduced?

- **10:** Attack works every time with no special conditions
- **7-9:** Attack works most of the time with minimal setup
- **4-6:** Attack requires specific timing, conditions, or configuration
- **1-3:** Attack is extremely difficult to reproduce, requires rare conditions

**Example:**
- SQL injection with automated tool: **10** (always works)
- Race condition exploit: **4** (requires precise timing)

---

#### E - Exploitability

How easy is it to launch the attack?

- **10:** No authentication required, automated exploit available, script kiddie level
- **7-9:** Requires authentication, manual exploit, moderate skill
- **4-6:** Requires deep technical knowledge, custom exploit development
- **1-3:** Requires expert-level skills, significant resources, insider access

**Example:**
- Public RCE exploit for known CVE: **10** (Metasploit module available)
- Zero-day kernel exploit: **3** (requires advanced skills)

---

#### A - Affected Users

How many users are affected?

- **10:** All users affected (entire user base)
- **7-9:** Large subset of users (most users, all customers)
- **4-6:** Some users affected (specific user segment)
- **1-3:** Few users affected (admin only, single user)

**Example:**
- Authentication bypass on public website: **10** (all users)
- Privilege escalation requiring admin role: **2** (admin only)

---

#### D - Discoverability

How easy is it to discover the vulnerability?

- **10:** Vulnerability is obvious, already public, scanners detect it
- **7-9:** Vulnerability easily found with standard tools
- **4-6:** Requires some effort, security testing to discover
- **1-3:** Nearly impossible to discover, requires source code access

**Example:**
- Unpatched public CVE: **10** (scanners detect, exploits available)
- Logic flaw in business workflow: **4** (requires code review)

---

### Risk Score Calculation

**Formula:**
```
Risk Score = (Damage + Reproducibility + Exploitability + Affected Users + Discoverability) / 5
```

**Risk Levels:**
- **Critical:** 8.0 - 10.0 (immediate action required)
- **High:** 6.0 - 7.9 (urgent remediation)
- **Medium:** 4.0 - 5.9 (plan remediation)
- **Low:** 1.0 - 3.9 (monitor, low priority)

---

### DREAD Scoring Examples

**Example 1: SQL Injection in Login Form**

- **Damage:** 9 (Database compromise, all user data exposed)
- **Reproducibility:** 10 (Works every time)
- **Exploitability:** 8 (Automated tools available, moderate skill)
- **Affected Users:** 10 (All users' data at risk)
- **Discoverability:** 9 (Common vulnerability, scanners detect)

**Risk Score:** (9 + 10 + 8 + 10 + 9) / 5 = **9.2 (Critical)**

---

**Example 2: Stored XSS on Admin Panel**

- **Damage:** 6 (Admin session hijacking, limited to admin accounts)
- **Reproducibility:** 10 (Works every time)
- **Exploitability:** 7 (Requires authentication, manual exploit)
- **Affected Users:** 2 (Admin users only)
- **Discoverability:** 6 (Requires security testing to find)

**Risk Score:** (6 + 10 + 7 + 2 + 6) / 5 = **6.2 (High)**

---

**Example 3: Information Disclosure in Error Messages**

- **Damage:** 4 (Reveals internal paths, versions; aids reconnaissance)
- **Reproducibility:** 10 (Consistent error messages)
- **Exploitability:** 10 (No authentication required, trivial to trigger)
- **Affected Users:** 10 (All users can trigger)
- **Discoverability:** 8 (Easy to find with basic testing)

**Risk Score:** (4 + 10 + 10 + 10 + 8) / 5 = **8.4 (Critical)**

*Note: Despite low damage, high exploitability and discoverability make this critical for remediation.*

---

## Attack Trees

**Visual threat modeling technique showing hierarchical attack paths**

### Attack Tree Structure

- **Goal (Root Node):** Attacker's objective (e.g., "Compromise Web Application")
- **Attack Paths (Branches):** Different ways to achieve goal
- **Attack Steps (Leaf Nodes):** Atomic actions required

**Gates:**
- **OR Gate:** Any child node success achieves parent goal
- **AND Gate:** All child nodes must succeed for parent goal

---

### Attack Tree Example: Compromise Web Application

```
                    Compromise Web Application (GOAL)
                              │
        ┌─────────────────────┼─────────────────────┐
        │ [OR]                │ [OR]                │ [OR]
   Exploit SQLi        Steal Credentials      Exploit Vuln Lib
        │                     │                     │
    ┌───┴───┐           ┌─────┴─────┐         ┌────┴────┐
    │ [AND] │           │ [OR]      │ [OR]    │ [AND]   │
Find Input Bypass   Phishing  Credential  Find Vuln Exploit
Validation WAF      Email     Stuffing    in SBOM   CVE
    │       │           │           │         │         │
    ▼       ▼           ▼           ▼         ▼         ▼
 [TEST]  [TEST]      [SEND]      [RUN]    [SCAN]    [RUN]
                                 [SCRIPT]            [EXPLOIT]

Leaf Nodes (Actions):
- TEST: Automated scanning (sqlmap, Burp Suite)
- SEND: Phishing campaign
- RUN SCRIPT: Credential stuffing attack
- SCAN: SBOM analysis, vulnerability scanning
- RUN EXPLOIT: Execute public exploit (Metasploit)
```

---

### Attack Tree Analysis

**Assign Values to Leaf Nodes:**

- **Cost:** Time, resources, skills required
- **Likelihood:** Probability of success
- **Detection Risk:** Probability of detection

**Example:**

| Attack Step | Cost | Likelihood | Detection Risk |
|-------------|------|------------|----------------|
| Find Input Validation (SQLi) | Low (automated) | High (common) | Medium (WAF logs) |
| Bypass WAF | Medium (manual) | Medium (depends on WAF) | High (alerts) |
| Phishing Email | Low (templates) | Medium (user training) | High (email filters) |
| Credential Stuffing | Low (automated) | Medium (depends on passwords) | Medium (rate limiting) |
| Find Vuln in SBOM | Low (scanners) | High (if outdated libs) | Low (passive) |
| Exploit CVE | Low (public exploits) | High (if unpatched) | High (IDS/IPS) |

**Risk Calculation:**

Most likely path: **Find Vuln in SBOM → Exploit CVE**
- Low cost, high likelihood, low detection risk (until exploit runs)

**Mitigation Priority:**
1. Dependency scanning and patching (blocks "Find Vuln in SBOM")
2. WAF with virtual patching (blocks "Exploit CVE")
3. Input validation and parameterized queries (blocks "Find Input Validation")

---

## Methodology Selection Guide

### Decision Matrix

| Criterion | STRIDE | PASTA | DREAD | Attack Trees |
|-----------|--------|-------|-------|--------------|
| **Ease of Use** | High | Low | High | Medium |
| **Time Required** | Low (days) | High (weeks) | Low (hours) | Medium (days) |
| **Business Alignment** | Low | High | Medium | Low |
| **Comprehensive Coverage** | High | Very High | N/A (scoring only) | Medium |
| **Quantitative Risk** | No | Yes | Yes | Yes (if values assigned) |
| **Best For** | Dev teams | Enterprise | Prioritization | Visualization |

---

### Recommendation by Use Case

**Use Case: Agile Development Team Threat Modeling**
- **Primary:** STRIDE (quick, comprehensive threat identification)
- **Secondary:** DREAD (prioritize threats for sprint planning)
- **Cadence:** Every major feature, architecture change

**Use Case: Enterprise Risk Assessment**
- **Primary:** PASTA (business-aligned, comprehensive)
- **Secondary:** Attack Trees (visualize complex attack scenarios)
- **Cadence:** Annually, or for critical systems

**Use Case: Prioritizing Vulnerability Remediation**
- **Primary:** DREAD (quantitative risk scoring)
- **Secondary:** CVSS scores (industry standard for CVEs)
- **Cadence:** Continuous (as vulnerabilities discovered)

**Use Case: Security Architecture Review**
- **Primary:** Attack Trees (visualize attack paths)
- **Secondary:** STRIDE (comprehensive threat coverage)
- **Cadence:** During architecture design, major changes

---

## Summary

**Threat Modeling Methodologies:**
- **STRIDE:** Systematic threat identification using 6 categories (Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation of Privilege)
- **PASTA:** 7-stage risk-centric analysis aligned with business objectives
- **DREAD:** Numeric risk scoring (Damage, Reproducibility, Exploitability, Affected Users, Discoverability)
- **Attack Trees:** Visual representation of attack paths and scenarios

**Recommended Approach:**
1. Use STRIDE for comprehensive threat identification
2. Use DREAD to prioritize threats by risk
3. Use Attack Trees to visualize complex attack scenarios
4. Use PASTA for enterprise-level risk assessments with business impact analysis

Integrate threat modeling into SDLC: Design phase (architecture threat modeling), Development (code-level STRIDE), Pre-deployment (comprehensive PASTA for critical systems).
