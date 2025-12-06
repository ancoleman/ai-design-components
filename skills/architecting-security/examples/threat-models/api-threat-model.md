# API Threat Model

## Overview

Threat model for RESTful API using STRIDE methodology. Identify threats across authentication, authorization, data validation, and API-specific attack vectors. Apply defense-in-depth controls to mitigate risks.

## System Description

**API Architecture:**

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Client     │────────▶│  API Gateway │────────▶│   Backend    │
│  (Browser/   │         │              │         │   Service    │
│   Mobile)    │         │ - Auth       │         │              │
└──────────────┘         │ - Rate Limit │         └──────┬───────┘
                         │ - Validation │                │
                         │ - Logging    │                │
                         └──────────────┘                │
                                                          ▼
                                                  ┌──────────────┐
                                                  │   Database   │
                                                  │              │
                                                  └──────────────┘
```

**API Endpoints:**

- `POST /api/v1/auth/login` - User authentication
- `POST /api/v1/auth/refresh` - Token refresh
- `GET /api/v1/users/{id}` - Retrieve user profile
- `PUT /api/v1/users/{id}` - Update user profile
- `DELETE /api/v1/users/{id}` - Delete user account
- `GET /api/v1/resources` - List resources (paginated)
- `POST /api/v1/resources` - Create resource
- `GET /api/v1/resources/{id}` - Retrieve specific resource
- `PUT /api/v1/resources/{id}` - Update resource
- `DELETE /api/v1/resources/{id}` - Delete resource
- `POST /api/v1/resources/{id}/share` - Share resource with other users

## STRIDE Threat Analysis

### Spoofing (Identity)

**Threat 1.1: Credential Theft**

- **Description:** Attacker obtains user credentials through phishing, keylogging, or database breach
- **Attack Vector:** Stolen username/password used to authenticate to API
- **Impact:** HIGH - Unauthorized access to user account and data
- **Likelihood:** MEDIUM - Common attack method

**Mitigations:**
```yaml
- control: Multi-factor authentication (MFA)
  effectiveness: HIGH
  implementation:
    - Require MFA for all sensitive operations
    - Use time-based one-time passwords (TOTP)
    - Support WebAuthn/FIDO2 hardware keys

- control: Password complexity requirements
  effectiveness: MEDIUM
  implementation:
    - Minimum 12 characters
    - Mix of uppercase, lowercase, numbers, symbols
    - Check against known breached passwords (HaveIBeenPwned)

- control: Account lockout after failed attempts
  effectiveness: MEDIUM
  implementation:
    - Lock account after 5 failed login attempts
    - Exponential backoff (5min, 15min, 30min)
    - CAPTCHA after 3 failed attempts

- control: Monitor for credential stuffing
  effectiveness: MEDIUM
  implementation:
    - Track login attempts from same IP
    - Detect patterns of credential testing
    - Block suspicious IPs automatically
```

**Threat 1.2: Token Theft**

- **Description:** Attacker steals JWT access token or refresh token
- **Attack Vector:** XSS, insecure storage, man-in-the-middle, token logging
- **Impact:** HIGH - Session hijacking and unauthorized API access
- **Likelihood:** MEDIUM - Multiple attack vectors exist

**Mitigations:**
```yaml
- control: Short-lived access tokens
  effectiveness: HIGH
  implementation:
    - Access token TTL: 15 minutes
    - Refresh token TTL: 7 days
    - Require re-authentication for sensitive operations

- control: Secure token storage
  effectiveness: HIGH
  implementation:
    - Store tokens in httpOnly, secure, SameSite cookies
    - Never store in localStorage or sessionStorage
    - Use memory-only storage for SPAs where possible

- control: Token binding to client
  effectiveness: MEDIUM
  implementation:
    - Include client fingerprint in token
    - Bind token to IP address (with caution for mobile)
    - Validate User-Agent consistency

- control: Token rotation on use
  effectiveness: HIGH
  implementation:
    - Issue new refresh token on each use
    - Invalidate old refresh token immediately
    - Detect refresh token reuse (possible theft)
```

**Threat 1.3: API Key Compromise**

- **Description:** API keys leaked in code repositories, logs, or client-side code
- **Attack Vector:** GitHub scanning, log analysis, decompilation
- **Impact:** MEDIUM - Unauthorized API access within key scope
- **Likelihood:** HIGH - Very common occurrence

**Mitigations:**
```yaml
- control: Avoid API keys for user authentication
  effectiveness: HIGH
  implementation:
    - Use API keys only for service-to-service auth
    - Never embed keys in mobile apps or client-side code
    - Use OAuth 2.0 for user authentication

- control: Secret scanning in CI/CD
  effectiveness: HIGH
  implementation:
    - Use git-secrets, TruffleHog, or GitHub secret scanning
    - Block commits containing API keys
    - Scan all historical commits

- control: API key rotation and scoping
  effectiveness: MEDIUM
  implementation:
    - Rotate keys every 90 days
    - Scope keys to specific operations
    - Track key usage and expire unused keys

- control: Key management service
  effectiveness: HIGH
  implementation:
    - Store keys in HashiCorp Vault, AWS Secrets Manager, etc.
    - Retrieve keys at runtime only
    - Audit all key access
```

### Tampering (Data Integrity)

**Threat 2.1: Request Tampering**

- **Description:** Attacker modifies API request parameters to bypass authorization or manipulate data
- **Attack Vector:** Intercepted request modified in transit or by client
- **Impact:** HIGH - Unauthorized data modification or privilege escalation
- **Likelihood:** MEDIUM - Requires MITM or client-side manipulation

**Mitigations:**
```yaml
- control: HTTPS enforcement (TLS 1.3)
  effectiveness: HIGH
  implementation:
    - Enforce TLS 1.3 minimum
    - Use HSTS with includeSubDomains and preload
    - Implement certificate pinning for mobile apps

- control: Request signing
  effectiveness: HIGH
  implementation:
    - Sign sensitive requests with HMAC
    - Include timestamp to prevent replay
    - Validate signature on server before processing

- control: Input validation
  effectiveness: HIGH
  implementation:
    - Validate all parameters against schema
    - Reject unexpected fields
    - Sanitize all input before processing

- control: Server-side authorization checks
  effectiveness: CRITICAL
  implementation:
    - Never trust client-provided user IDs
    - Verify user has permission for requested operation
    - Re-validate authorization for each request
```

**Threat 2.2: Response Tampering**

- **Description:** Attacker intercepts and modifies API response data
- **Attack Vector:** Man-in-the-middle attack, compromised proxy
- **Impact:** MEDIUM - Client receives incorrect data, potential security decisions based on false data
- **Likelihood:** LOW - Requires MITM position

**Mitigations:**
```yaml
- control: TLS encryption
  effectiveness: HIGH
  implementation:
    - All API traffic over HTTPS only
    - Proper certificate validation
    - No mixed content allowed

- control: Response integrity checks
  effectiveness: MEDIUM
  implementation:
    - Include response signature for critical data
    - Use Content-Security-Policy headers
    - Subresource Integrity (SRI) for any CDN resources

- control: Certificate pinning
  effectiveness: HIGH
  implementation:
    - Pin server certificates in mobile apps
    - Use public key pinning for critical connections
    - Implement pin backup keys
```

**Threat 2.3: SQL Injection**

- **Description:** Attacker injects SQL commands through API parameters
- **Attack Vector:** Unsanitized input used in SQL queries
- **Impact:** CRITICAL - Database compromise, data exfiltration, data modification
- **Likelihood:** MEDIUM - Common vulnerability if not properly mitigated

**Mitigations:**
```yaml
- control: Parameterized queries
  effectiveness: CRITICAL
  implementation:
    - Use prepared statements exclusively
    - Never concatenate user input into SQL
    - Use ORM with parameterized queries

- control: Input validation
  effectiveness: HIGH
  implementation:
    - Validate data types (integer, UUID, etc.)
    - Whitelist allowed characters
    - Reject SQL keywords in unexpected fields

- control: Least privilege database access
  effectiveness: MEDIUM
  implementation:
    - API service uses read-only account where possible
    - Separate accounts for read vs. write operations
    - Restrict database permissions to required tables only

- control: Web Application Firewall (WAF)
  effectiveness: MEDIUM
  implementation:
    - Deploy WAF with SQL injection rules
    - Block common SQL injection patterns
    - Log and alert on detected attempts
```

### Repudiation (Accountability)

**Threat 3.1: Action Denial**

- **Description:** User denies performing an action (data deletion, unauthorized access)
- **Attack Vector:** Lack of audit trail, insufficient logging
- **Impact:** MEDIUM - Cannot prove user performed action, compliance violations
- **Likelihood:** HIGH - Users frequently claim they didn't perform actions

**Mitigations:**
```yaml
- control: Comprehensive audit logging
  effectiveness: HIGH
  implementation:
    - Log all state-changing operations
    - Include user ID, timestamp, IP, action, resource
    - Log authentication events (success and failure)
    - Never log sensitive data (passwords, tokens, PII)

- control: Immutable audit trail
  effectiveness: HIGH
  implementation:
    - Write logs to append-only storage
    - Use centralized logging (ELK, Splunk, CloudWatch)
    - Prevent log modification or deletion
    - Cryptographically sign log entries

- control: Request tracking
  effectiveness: MEDIUM
  implementation:
    - Assign unique request ID to each API call
    - Include request ID in all logs and responses
    - Enable correlation across distributed services

- control: User consent tracking
  effectiveness: MEDIUM
  implementation:
    - Record explicit user consent for sensitive actions
    - Require confirmation for destructive operations
    - Log consent timestamps and IP addresses
```

**Threat 3.2: Log Tampering**

- **Description:** Attacker modifies or deletes audit logs to hide malicious activity
- **Attack Vector:** Compromised server access, insufficient log protection
- **Impact:** HIGH - Loss of audit trail, inability to investigate incidents
- **Likelihood:** LOW - Requires elevated access

**Mitigations:**
```yaml
- control: Centralized logging
  effectiveness: HIGH
  implementation:
    - Forward logs to external SIEM immediately
    - No local log storage on API servers
    - Use TLS for log transmission

- control: Log integrity verification
  effectiveness: HIGH
  implementation:
    - Cryptographic hashing of log entries
    - Chain logs together (blockchain-style)
    - Periodic integrity checks

- control: Access controls on logs
  effectiveness: MEDIUM
  implementation:
    - Separate logging service account
    - Read-only access for auditors
    - Alert on log access by unauthorized users

- control: Log retention and backup
  effectiveness: MEDIUM
  implementation:
    - Retain logs for minimum 1 year
    - Immutable S3 storage or WORM media
    - Automated backup verification
```

### Information Disclosure (Confidentiality)

**Threat 4.1: Sensitive Data Exposure in Responses**

- **Description:** API returns excessive data including sensitive fields
- **Attack Vector:** Over-fetching, verbose error messages, debug mode
- **Impact:** HIGH - Exposure of PII, credentials, internal system details
- **Likelihood:** HIGH - Very common in APIs

**Mitigations:**
```yaml
- control: Response filtering
  effectiveness: HIGH
  implementation:
    - Return only requested fields
    - Use DTO pattern to control response shape
    - Never include password hashes in responses
    - Redact sensitive fields (SSN, credit cards)

- control: Field-level authorization
  effectiveness: HIGH
  implementation:
    - Check permissions for each returned field
    - Hide fields user doesn't have access to
    - Use different response schemas for different roles

- control: Generic error messages
  effectiveness: MEDIUM
  implementation:
    - Return generic errors to client
    - Log detailed errors server-side only
    - Never expose stack traces
    - Use error codes instead of detailed messages

- control: Disable debug mode in production
  effectiveness: CRITICAL
  implementation:
    - No verbose error messages
    - No debug endpoints exposed
    - Remove all console.log and debug code
```

**Threat 4.2: Insecure Direct Object Reference (IDOR)**

- **Description:** Attacker accesses resources by guessing or enumerating IDs
- **Attack Vector:** Sequential IDs, predictable UUIDs, missing authorization checks
- **Impact:** HIGH - Unauthorized data access, privacy violation
- **Likelihood:** HIGH - Extremely common vulnerability

**Mitigations:**
```yaml
- control: Authorization checks on every request
  effectiveness: CRITICAL
  implementation:
    - Verify user owns or has access to requested resource
    - Check permissions before database query
    - Never rely on client-provided IDs alone

- control: Non-sequential identifiers
  effectiveness: MEDIUM
  implementation:
    - Use UUIDv4 for resource IDs
    - Avoid auto-incrementing integer IDs
    - Don't expose internal database IDs

- control: Indirect object references
  effectiveness: HIGH
  implementation:
    - Map external IDs to internal IDs
    - Use per-user ID namespaces
    - Implement access tokens for resources

- control: Rate limiting enumeration attempts
  effectiveness: MEDIUM
  implementation:
    - Limit requests per user/IP
    - Detect ID enumeration patterns
    - CAPTCHA after repeated 404s
```

**Threat 4.3: Mass Assignment**

- **Description:** Attacker modifies object properties they shouldn't have access to
- **Attack Vector:** Sending unexpected fields in PUT/PATCH requests
- **Impact:** HIGH - Privilege escalation, unauthorized data modification
- **Likelihood:** MEDIUM - Requires knowledge of internal field names

**Mitigations:**
```yaml
- control: Explicit field whitelisting
  effectiveness: CRITICAL
  implementation:
    - Define allowed fields for each endpoint
    - Reject requests with unexpected fields
    - Use separate DTOs for input validation

- control: Read-only fields enforcement
  effectiveness: HIGH
  implementation:
    - Mark fields as read-only (id, created_at, role)
    - Prevent modification even if included in request
    - Validate field-level permissions

- control: Separate admin endpoints
  effectiveness: HIGH
  implementation:
    - Use different endpoints for admin operations
    - Don't mix user and admin fields in same request
    - Require elevated permissions for admin endpoints
```

### Denial of Service

**Threat 5.1: API Abuse / Resource Exhaustion**

- **Description:** Attacker overwhelms API with excessive requests
- **Attack Vector:** Automated bots, distributed attacks, large payload requests
- **Impact:** HIGH - Service unavailability, increased costs
- **Likelihood:** HIGH - Very common attack

**Mitigations:**
```yaml
- control: Rate limiting
  effectiveness: HIGH
  implementation:
    - 100 requests per minute per user
    - 1000 requests per hour per IP
    - Lower limits for expensive endpoints
    - Return 429 Too Many Requests with Retry-After

- control: Request size limits
  effectiveness: HIGH
  implementation:
    - Max request body: 1MB
    - Max URL length: 2048 characters
    - Reject oversized requests immediately
    - Limit file upload sizes

- control: Response pagination
  effectiveness: MEDIUM
  implementation:
    - Maximum 100 items per page
    - Default page size: 20 items
    - Cursor-based pagination for large datasets
    - Timeout long-running queries (30 seconds)

- control: DDoS protection
  effectiveness: MEDIUM
  implementation:
    - Use CloudFlare, AWS Shield, or Akamai
    - Implement connection limits
    - Geographic blocking for suspicious regions
    - Challenge-based verification (CAPTCHA)
```

**Threat 5.2: Regex DoS (ReDoS)**

- **Description:** Attacker sends input that causes catastrophic backtracking in regex validation
- **Attack Vector:** Crafted input exploiting inefficient regex patterns
- **Impact:** MEDIUM - CPU exhaustion, slow response times
- **Likelihood:** LOW - Requires specific vulnerable regex patterns

**Mitigations:**
```yaml
- control: Regex timeout enforcement
  effectiveness: HIGH
  implementation:
    - Set regex execution timeout (100ms)
    - Terminate on timeout and reject input
    - Use regex analysis tools (safe-regex)

- control: Avoid complex regex
  effectiveness: HIGH
  implementation:
    - Use simple patterns where possible
    - Avoid nested quantifiers (.*.*. etc.)
    - Test regex with ReDoS checkers

- control: Input length limits
  effectiveness: MEDIUM
  implementation:
    - Limit input before regex validation
    - Reject excessively long strings early
    - Validate length before pattern matching
```

**Threat 5.3: Database Query Amplification**

- **Description:** Single API request triggers expensive database operations
- **Attack Vector:** Unbounded queries, missing pagination, N+1 query problems
- **Impact:** HIGH - Database overload, slow response times
- **Likelihood:** MEDIUM - Common in poorly optimized APIs

**Mitigations:**
```yaml
- control: Query result limits
  effectiveness: HIGH
  implementation:
    - Hard limit on query results (1000 rows max)
    - Force pagination on list endpoints
    - Use LIMIT clause in all queries

- control: Query timeout
  effectiveness: HIGH
  implementation:
    - Database query timeout: 10 seconds
    - Cancel long-running queries
    - Alert on frequent timeouts

- control: Database connection pooling
  effectiveness: MEDIUM
  implementation:
    - Limit max concurrent connections
    - Implement connection queue
    - Reject requests when pool exhausted

- control: Caching
  effectiveness: MEDIUM
  implementation:
    - Cache frequently accessed data (Redis)
    - Set appropriate TTLs
    - Cache invalidation on updates
```

### Elevation of Privilege

**Threat 6.1: Broken Authorization**

- **Description:** User accesses resources or performs actions beyond their permissions
- **Attack Vector:** Missing authorization checks, flawed permission logic
- **Impact:** CRITICAL - Unauthorized data access, system compromise
- **Likelihood:** HIGH - Very common vulnerability

**Mitigations:**
```yaml
- control: Centralized authorization
  effectiveness: CRITICAL
  implementation:
    - Single authorization service/library
    - Consistent permission checks across all endpoints
    - Deny by default policy

- control: Role-based access control (RBAC)
  effectiveness: HIGH
  implementation:
    - Define clear roles (admin, user, viewer)
    - Assign minimal required permissions
    - Check role before operation

- control: Attribute-based access control (ABAC)
  effectiveness: HIGH
  implementation:
    - Evaluate context (time, location, resource owner)
    - Dynamic permission decisions
    - Fine-grained access control

- control: Authorization testing
  effectiveness: HIGH
  implementation:
    - Automated tests for each permission scenario
    - Test negative cases (should be denied)
    - Regular security audits
```

**Threat 6.2: JWT Algorithm Confusion**

- **Description:** Attacker exploits JWT library to accept unsigned tokens
- **Attack Vector:** Changing JWT algorithm from RS256 to "none"
- **Impact:** CRITICAL - Complete authentication bypass
- **Likelihood:** LOW - Modern libraries protect against this

**Mitigations:**
```yaml
- control: Explicit algorithm specification
  effectiveness: CRITICAL
  implementation:
    - Specify allowed algorithms (RS256, ES256)
    - Reject "none" algorithm explicitly
    - Never allow symmetric algorithm if using asymmetric keys

- control: JWT library security
  effectiveness: HIGH
  implementation:
    - Use well-maintained libraries
    - Keep libraries up to date
    - Review security advisories

- control: Token validation
  effectiveness: CRITICAL
  implementation:
    - Validate signature on every request
    - Verify issuer (iss claim)
    - Verify audience (aud claim)
    - Check expiration (exp claim)
    - Validate not-before (nbf claim)
```

**Threat 6.3: Path Traversal in API Routes**

- **Description:** Attacker manipulates path parameters to access unauthorized endpoints
- **Attack Vector:** Using ../ in path parameters, URL encoding tricks
- **Impact:** MEDIUM - Access to admin endpoints, information disclosure
- **Likelihood:** LOW - Most frameworks protect against this

**Mitigations:**
```yaml
- control: Path parameter validation
  effectiveness: HIGH
  implementation:
    - Validate path parameters against whitelist
    - Reject ../ and encoded equivalents
    - Use strict routing patterns

- control: Framework security features
  effectiveness: HIGH
  implementation:
    - Use framework's built-in protections
    - Enable strict routing mode
    - Validate all path segments

- control: Separate route handlers
  effectiveness: MEDIUM
  implementation:
    - Don't use dynamic paths for critical endpoints
    - Use different route prefixes for admin vs. user
    - Implement route-level authentication
```

## Attack Surface Analysis

**High-Risk Endpoints:**

1. **POST /api/v1/auth/login**
   - Risks: Credential stuffing, brute force, timing attacks
   - Priority Mitigations: Rate limiting, MFA, account lockout

2. **PUT /api/v1/users/{id}**
   - Risks: IDOR, mass assignment, privilege escalation
   - Priority Mitigations: Authorization checks, field whitelisting

3. **DELETE /api/v1/users/{id}**
   - Risks: Unauthorized deletion, lack of audit trail
   - Priority Mitigations: Strong authorization, audit logging, soft delete

4. **POST /api/v1/resources/{id}/share**
   - Risks: Unauthorized sharing, information disclosure
   - Priority Mitigations: Permission verification, notification, audit logging

**Trust Boundaries:**

```
Untrusted:
- All client input (headers, parameters, body)
- External API integrations
- User-uploaded files

Semi-Trusted:
- Internal microservices (verify with mTLS)
- Database responses (could be tampered if DB compromised)

Trusted:
- Configuration management system
- Secrets manager
- Internal audit logs
```

## Threat Risk Matrix

| Threat | Impact | Likelihood | Risk Level | Priority |
|--------|--------|------------|------------|----------|
| SQL Injection | CRITICAL | MEDIUM | CRITICAL | P0 |
| Broken Authorization | CRITICAL | HIGH | CRITICAL | P0 |
| JWT Algorithm Confusion | CRITICAL | LOW | HIGH | P1 |
| IDOR | HIGH | HIGH | HIGH | P1 |
| Credential Theft | HIGH | MEDIUM | HIGH | P1 |
| Token Theft | HIGH | MEDIUM | HIGH | P1 |
| Mass Assignment | HIGH | MEDIUM | HIGH | P1 |
| Sensitive Data Exposure | HIGH | HIGH | HIGH | P1 |
| API Abuse / DoS | HIGH | HIGH | HIGH | P1 |
| Request Tampering | HIGH | MEDIUM | MEDIUM | P2 |
| API Key Compromise | MEDIUM | HIGH | MEDIUM | P2 |
| Log Tampering | HIGH | LOW | MEDIUM | P2 |
| Database Query Amplification | HIGH | MEDIUM | MEDIUM | P2 |
| Response Tampering | MEDIUM | LOW | LOW | P3 |
| ReDoS | MEDIUM | LOW | LOW | P3 |
| Path Traversal | MEDIUM | LOW | LOW | P3 |

## Security Controls Summary

**Critical Controls (Must Implement):**
- Parameterized queries for all database operations
- Authorization checks on every endpoint
- JWT signature validation with explicit algorithm
- HTTPS enforcement with HSTS
- Comprehensive audit logging
- Input validation and sanitization

**High-Priority Controls:**
- Multi-factor authentication
- Rate limiting (per user and per IP)
- Non-sequential resource identifiers
- Field-level authorization
- Token rotation and short TTLs
- WAF deployment

**Recommended Controls:**
- API key rotation and scoping
- Response pagination and limits
- Request signing for sensitive operations
- Certificate pinning for mobile apps
- Caching for performance and DoS protection
- Automated security testing in CI/CD

## Testing Recommendations

```yaml
Security Testing:
  - tool: OWASP ZAP
    focus: Automated vulnerability scanning
    frequency: Every build

  - tool: Burp Suite
    focus: Manual penetration testing
    frequency: Quarterly

  - tool: SQLMap
    focus: SQL injection detection
    frequency: Every release

  - tool: Postman / Newman
    focus: Authorization testing
    frequency: Every build

  - tool: JMeter / Locust
    focus: Load testing and DoS resilience
    frequency: Monthly

  - tool: SonarQube
    focus: Static code analysis
    frequency: Every commit

  - tool: Dependency-Check
    focus: Vulnerable dependencies
    frequency: Weekly
```

## Compliance Considerations

**OWASP API Security Top 10 Coverage:**
- API1:2023 Broken Object Level Authorization → Mitigated by authorization checks
- API2:2023 Broken Authentication → Mitigated by MFA, token management
- API3:2023 Broken Object Property Level Authorization → Mitigated by field whitelisting
- API4:2023 Unrestricted Resource Consumption → Mitigated by rate limiting
- API5:2023 Broken Function Level Authorization → Mitigated by RBAC
- API6:2023 Unrestricted Access to Sensitive Business Flows → Mitigated by rate limiting
- API7:2023 Server Side Request Forgery → Mitigated by input validation
- API8:2023 Security Misconfiguration → Mitigated by secure defaults
- API9:2023 Improper Inventory Management → Mitigated by API documentation
- API10:2023 Unsafe Consumption of APIs → Mitigated by validation of external data

## References

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- [Microsoft Threat Modeling Tool](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling)
- [STRIDE Methodology](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
