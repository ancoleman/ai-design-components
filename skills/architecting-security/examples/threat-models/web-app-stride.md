# Web Application STRIDE Threat Model Example

## System Overview

**Application:** E-commerce Web Application
**Architecture:** Three-tier (Web → Application → Database)
**Technology Stack:**
- Frontend: React SPA
- API: Node.js/Express REST API
- Database: PostgreSQL
- Authentication: OAuth 2.0 + JWT
- Hosting: AWS (CloudFront, ALB, EC2, RDS)

## Data Flow Diagram

```
┌─────────┐                                          ┌──────────┐
│  User   │─────(1) HTTPS Request───────────────────►│CloudFront│
│(Browser)│◄────(10) HTTPS Response──────────────────│   CDN    │
└─────────┘                                          └────┬─────┘
                                                          │
                                                     (2) Forward
                                                          │
                                                     ┌────▼─────┐
                                                     │   WAF    │
                                                     │ (AWS WAF)│
                                                     └────┬─────┘
                                                          │
                                                     (3) Inspect
                                                          │
                                                     ┌────▼─────┐
                                                     │   ALB    │
                                                     │(Load Bal)│
                                                     └────┬─────┘
                                                          │
                                         ┌────────────────┼────────────────┐
                                         │                │                │
                                    ┌────▼────┐     ┌────▼────┐     ┌────▼────┐
                                    │Web App 1│     │Web App 2│     │Web App 3│
                                    │(Express)│     │(Express)│     │(Express)│
                                    └────┬────┘     └────┬────┘     └────┬────┘
                                         │                │                │
                                         └────────────────┼────────────────┘
                                                          │
                                                     (4) SQL Query
                                                          │
                                                     ┌────▼─────┐
                                                     │PostgreSQL│
                                                     │   RDS    │
                                                     └──────────┘

Trust Boundaries:
───────────────── Internet / AWS (1-2)
───────────────── WAF / Application (3)
───────────────── Application / Database (4)
```

## STRIDE Threat Analysis

### Component 1: User (Browser)

#### Threat: Spoofing

**S1.1: Phishing Attack**
- **Description:** Attacker creates fake login page to steal credentials
- **Impact:** HIGH - User credentials compromised
- **Likelihood:** MEDIUM - Common attack vector
- **Mitigation:**
  - Implement HTTPS with EV certificate (visible in browser)
  - User education and security awareness training
  - FIDO2/WebAuthn for phishing-resistant authentication
  - Email warnings for suspicious login attempts

---

### Component 2: CloudFront (CDN)

#### Threat: Tampering

**T2.1: Man-in-the-Middle (MITM) Attack**
- **Description:** Attacker intercepts traffic between user and CDN
- **Impact:** HIGH - Data theft, session hijacking
- **Likelihood:** LOW - HTTPS prevents MITM
- **Mitigation:**
  - Enforce TLS 1.3 minimum
  - HSTS (HTTP Strict Transport Security) headers
  - Certificate pinning for mobile apps

#### Threat: Denial of Service

**D2.1: DDoS Attack on CDN**
- **Description:** Volumetric DDoS attack overwhelms CDN
- **Impact:** HIGH - Service unavailability
- **Likelihood:** MEDIUM - E-commerce targets for extortion
- **Mitigation:**
  - CloudFront DDoS protection (built-in)
  - AWS Shield Standard (free) or Advanced
  - Rate limiting at CDN edge

---

### Component 3: WAF (AWS WAF)

#### Threat: Elevation of Privilege

**E3.1: WAF Bypass**
- **Description:** Attacker bypasses WAF rules to reach application
- **Impact:** HIGH - Exposes application to attacks
- **Likelihood:** MEDIUM - WAF rules can be bypassed
- **Mitigation:**
  - Regularly update WAF rules (OWASP Core Rule Set)
  - Custom rules for application-specific attacks
  - Rate limiting and geographic restrictions
  - Monitor WAF logs for bypass attempts

---

### Component 4: Application Load Balancer (ALB)

#### Threat: Denial of Service

**D4.1: HTTP Flood Attack**
- **Description:** Application-layer DDoS targeting ALB
- **Impact:** HIGH - Service degradation
- **Likelihood:** MEDIUM
- **Mitigation:**
  - ALB connection limits and timeouts
  - Auto-scaling based on load
  - Rate limiting at application layer
  - WAF rate-based rules

---

### Component 5: Web Application (Express API)

#### Threat: Spoofing

**S5.1: JWT Token Forgery**
- **Description:** Attacker forges JWT token to impersonate user
- **Impact:** CRITICAL - Complete account takeover
- **Likelihood:** LOW - Requires key compromise
- **Mitigation:**
  - Strong JWT signing algorithm (RS256, not HS256 with weak secret)
  - Short token expiry (15 minutes)
  - Refresh token rotation
  - Store signing keys in AWS Secrets Manager
  - Validate token signature, expiry, issuer, audience

#### Threat: Tampering

**T5.1: SQL Injection**
- **Description:** Attacker injects SQL code via user input
- **Impact:** CRITICAL - Database compromise, data breach
- **Likelihood:** MEDIUM - Common attack, but mitigable
- **Mitigation:**
  - Use parameterized queries or ORM (Sequelize, TypeORM)
  - Input validation (whitelist, length limits)
  - Least privilege database user (no DROP, CREATE permissions)
  - WAF SQL injection rules
  - Regular SAST/DAST scanning

**T5.2: API Parameter Tampering**
- **Description:** User modifies request parameters to access unauthorized data
- **Impact:** HIGH - Unauthorized data access (IDOR)
- **Likelihood:** MEDIUM
- **Mitigation:**
  - Server-side authorization checks (verify user owns resource)
  - Indirect object references (use UUIDs, not sequential IDs)
  - Input validation on all parameters

#### Threat: Repudiation

**R5.1: User Denies Transaction**
- **Description:** User denies making purchase or action
- **Impact:** MEDIUM - Fraud, chargebacks
- **Likelihood:** MEDIUM
- **Mitigation:**
  - Comprehensive audit logging (user, IP, timestamp, action)
  - Immutable logs (centralized SIEM)
  - Email confirmation for critical actions (purchases, password changes)
  - Transaction receipts and order history

#### Threat: Information Disclosure

**I5.1: Verbose Error Messages**
- **Description:** Error messages reveal internal paths, stack traces
- **Impact:** MEDIUM - Aids attacker reconnaissance
- **Likelihood:** HIGH - Common misconfiguration
- **Mitigation:**
  - Generic error messages to users ("An error occurred")
  - Detailed errors only in server logs
  - Custom error pages (500, 404)
  - Remove stack traces in production

**I5.2: API Responses Leak Sensitive Data**
- **Description:** API returns more data than necessary (full user objects)
- **Impact:** MEDIUM - Exposure of PII, internal data
- **Likelihood:** HIGH
- **Mitigation:**
  - Return only necessary fields (use DTOs)
  - Serialize responses (remove sensitive fields)
  - API response schema validation

**I5.3: Session Token Exposure in Logs**
- **Description:** JWT tokens logged in application logs
- **Impact:** HIGH - Session hijacking if logs compromised
- **Likelihood:** MEDIUM
- **Mitigation:**
  - Redact tokens in logs (mask Authorization headers)
  - Secure log storage (encryption, access control)
  - Short token expiry reduces exposure window

#### Threat: Denial of Service

**D5.1: API Rate Limit Bypass**
- **Description:** Attacker bypasses rate limiting to exhaust resources
- **Impact:** MEDIUM - Service degradation
- **Likelihood:** MEDIUM
- **Mitigation:**
  - Multiple rate limiting layers (IP, user, API key)
  - Distributed rate limiting (Redis)
  - CAPTCHA for suspicious traffic
  - Auto-scaling to handle bursts

**D5.2: Resource Exhaustion (ReDoS)**
- **Description:** Regex Denial of Service via malicious input
- **Impact:** MEDIUM - CPU exhaustion, service unavailability
- **Likelihood:** LOW
- **Mitigation:**
  - Avoid complex regex patterns
  - Timeout limits for regex execution
  - Input length limits
  - Use safe regex libraries (re2)

#### Threat: Elevation of Privilege

**E5.1: Broken Access Control**
- **Description:** User accesses admin endpoints without authorization
- **Impact:** CRITICAL - Complete system compromise
- **Likelihood:** MEDIUM
- **Mitigation:**
  - Authorization checks on every endpoint
  - RBAC (role-based access control)
  - Separate admin API with additional authentication
  - Principle of least privilege

**E5.2: Insecure Direct Object References (IDOR)**
- **Description:** User accesses other users' data by changing ID parameter
- **Impact:** HIGH - Unauthorized data access
- **Likelihood:** HIGH - Very common vulnerability
- **Mitigation:**
  - Verify user owns resource before returning data
  - Use UUIDs instead of sequential IDs
  - Indirect object references (session-based mapping)

---

### Component 6: PostgreSQL Database (RDS)

#### Threat: Tampering

**T6.1: Database Compromise via SQL Injection**
- **Description:** SQL injection leads to data modification/deletion
- **Impact:** CRITICAL - Data integrity loss, data destruction
- **Likelihood:** LOW (if application mitigations applied)
- **Mitigation:**
  - Parameterized queries (primary defense)
  - Database user least privilege (read-only for most operations)
  - Database audit logging
  - Immutable backups

#### Threat: Information Disclosure

**I6.1: Database Backup Exposure**
- **Description:** RDS snapshot publicly accessible or stolen
- **Impact:** CRITICAL - Full database dump exposed
- **Likelihood:** LOW - Requires misconfiguration
- **Mitigation:**
  - Private RDS in VPC (no internet access)
  - Encrypted snapshots (AWS KMS)
  - Access control on snapshots (IAM policies)
  - Regular snapshot access audits

**I6.2: Database Connection String in Code**
- **Description:** Database credentials hardcoded in source code
- **Impact:** CRITICAL - Database full access if code leaked
- **Likelihood:** MEDIUM - Common developer mistake
- **Mitigation:**
  - Store credentials in AWS Secrets Manager
  - IAM database authentication (no passwords)
  - Secrets rotation
  - Code scanning for hardcoded secrets (git-secrets, TruffleHog)

#### Threat: Denial of Service

**D6.1: Database Connection Pool Exhaustion**
- **Description:** Attacker opens many connections, exhausting pool
- **Impact:** HIGH - Database unavailable
- **Likelihood:** MEDIUM
- **Mitigation:**
  - Connection pool limits
  - Connection timeouts
  - Application-level connection management
  - Auto-scaling RDS read replicas

---

## Threat Summary Matrix

| ID | Component | STRIDE | Threat | Risk | Priority |
|----|-----------|--------|--------|------|----------|
| S1.1 | User | Spoofing | Phishing | HIGH | P1 |
| T2.1 | CDN | Tampering | MITM | HIGH | P2 |
| D2.1 | CDN | DoS | DDoS | HIGH | P1 |
| E3.1 | WAF | Elevation | WAF Bypass | HIGH | P2 |
| D4.1 | ALB | DoS | HTTP Flood | HIGH | P2 |
| S5.1 | API | Spoofing | JWT Forgery | CRITICAL | P0 |
| T5.1 | API | Tampering | SQL Injection | CRITICAL | P0 |
| T5.2 | API | Tampering | Param Tampering | HIGH | P1 |
| R5.1 | API | Repudiation | Deny Transaction | MEDIUM | P3 |
| I5.1 | API | Info Disclosure | Verbose Errors | MEDIUM | P3 |
| I5.2 | API | Info Disclosure | API Data Leak | MEDIUM | P2 |
| I5.3 | API | Info Disclosure | Token in Logs | HIGH | P2 |
| D5.1 | API | DoS | Rate Limit Bypass | MEDIUM | P3 |
| D5.2 | API | DoS | ReDoS | MEDIUM | P4 |
| E5.1 | API | Elevation | Broken Access | CRITICAL | P0 |
| E5.2 | API | Elevation | IDOR | HIGH | P1 |
| T6.1 | DB | Tampering | SQLi Compromise | CRITICAL | P0 |
| I6.1 | DB | Info Disclosure | Backup Exposure | CRITICAL | P0 |
| I6.2 | DB | Info Disclosure | Hardcoded Creds | CRITICAL | P0 |
| D6.1 | DB | DoS | Connection Exhaust | HIGH | P2 |

**Priority Levels:**
- P0: Critical - Immediate action required
- P1: High - Address within 1 sprint
- P2: Medium - Address within 1 quarter
- P3: Low - Backlog
- P4: Informational

---

## Mitigation Roadmap

### Sprint 1 (Immediate - P0)
- ☐ Implement parameterized queries for all database operations (T5.1, T6.1)
- ☐ Add authorization checks to all API endpoints (E5.1)
- ☐ Migrate database credentials to AWS Secrets Manager (I6.2)
- ☐ Enable RDS encryption and private VPC placement (I6.1)
- ☐ Strengthen JWT signing (RS256, key rotation) (S5.1)

### Sprint 2-3 (High Priority - P1)
- ☐ Implement FIDO2/WebAuthn for phishing resistance (S1.1)
- ☐ Deploy comprehensive IDOR protection (E5.2)
- ☐ Fix API parameter tampering vulnerabilities (T5.2)
- ☐ Enable AWS Shield and DDoS protection (D2.1)

### Quarter (Medium Priority - P2)
- ☐ Harden WAF rules and monitor bypass attempts (E3.1)
- ☐ Implement multi-layer rate limiting (D4.1, D5.1)
- ☐ Minimize API response data (I5.2)
- ☐ Redact tokens from logs (I5.3)
- ☐ TLS 1.3 enforcement and HSTS (T2.1)

### Backlog (Low Priority - P3-P4)
- ☐ Comprehensive audit logging (R5.1)
- ☐ Custom error pages (I5.1)
- ☐ ReDoS prevention (D5.2)

---

## Validation

**Testing:**
- ☐ SAST: SonarQube scan for SQL injection, hardcoded secrets
- ☐ DAST: OWASP ZAP scan for IDOR, broken access control, XSS
- ☐ Penetration Testing: Third-party security audit
- ☐ Dependency Scanning: Snyk for vulnerable libraries

**Monitoring:**
- ☐ WAF logs for attack patterns
- ☐ API logs for failed authorization attempts
- ☐ SIEM alerts for anomalous behavior (UEBA)
- ☐ Database audit logs for suspicious queries

**Compliance:**
- ☐ Map mitigations to OWASP Top 10
- ☐ Map mitigations to PCI DSS requirements (if applicable)
- ☐ Document security controls for SOC 2 audit

---

## Conclusion

This STRIDE analysis identified 20 threats across 6 components, with 6 critical (P0) threats requiring immediate remediation. Primary focus areas:

1. **SQL Injection Prevention:** Parameterized queries, input validation
2. **Access Control:** Authorization checks, IDOR prevention
3. **Secrets Management:** Migrate to AWS Secrets Manager
4. **Data Protection:** RDS encryption, private VPC placement
5. **Authentication:** Strengthen JWT, implement phishing-resistant auth

Regular threat model updates recommended after significant architecture changes or security incidents.
