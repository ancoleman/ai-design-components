# Identity & Access Management Patterns Reference

## Authentication Controls

### Multi-Factor Authentication (MFA)

**Types:**
- TOTP (Time-based One-Time Password): Google Authenticator, Authy
- Push Notifications: Duo, Okta Verify
- Biometrics: Fingerprint, Face ID
- Hardware Tokens: YubiKey, FIDO2

**Implementation:**
- Enforce MFA for all users (prioritize privileged accounts)
- Support multiple MFA methods (user choice)
- Backup codes for account recovery
- Risk-based MFA (adaptive authentication)

### Single Sign-On (SSO)

**Protocols:**
- SAML 2.0: Enterprise federation
- OAuth 2.0: API authorization
- OpenID Connect (OIDC): Authentication layer on OAuth 2.0

**Benefits:**
- Centralized authentication
- Reduced password fatigue
- Improved security posture
- Better user experience

## Authorization Controls

### Role-Based Access Control (RBAC)

**Structure:**
- Users → Roles → Permissions
- Roles represent job functions (admin, developer, analyst)
- Coarse-grained, simple to implement

**Best For:** Organizations with stable role structures

### Attribute-Based Access Control (ABAC)

**Structure:**
- Fine-grained access based on attributes
- User attributes (department, clearance level)
- Resource attributes (classification, owner)
- Environmental attributes (time, location)

**Best For:** Complex, dynamic access requirements

### Policy-Based Access Control (PBAC)

**Centralized Policy Engines:**
- Open Policy Agent (OPA)
- AWS Cedar
- Authzed (SpiceDB)

**Best For:** Microservices, API gateways, cloud-native architectures

## Privileged Access Management (PAM)

### Just-in-Time (JIT) Access

**Principle:** Temporary elevated privileges for specific tasks

**Implementation:**
- Request-based access (approval workflow)
- Time-bound grants (4-8 hours)
- Automated de-provisioning
- Audit all privilege activations

### Credential Vaulting

**Solutions:**
- CyberArk
- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault

**Features:**
- Centralized credential storage
- Automatic password rotation
- Session recording
- Break-glass procedures
