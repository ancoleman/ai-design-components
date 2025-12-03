# Authentication & Security - Master Plan

> **Skill Purpose**: Implement modern authentication, authorization, and API security patterns across Python, Rust, Go, and TypeScript using OAuth 2.1, passkeys, and policy engines.
>
> **Date**: December 2025
> **Status**: Planning Phase
> **Research Sources**: FULL_STACK_SKILLS_UNIFIED.md (Skill 10), Context7 library research, OWASP 2025 guidelines

---

## Strategic Positioning

### Critical Infrastructure Skill

**Security cannot be an afterthought.** This skill is foundational for ALL frontend and backend skills because:

1. **Universal Dependency**: Every application with user data needs authentication
2. **Compliance Requirements**: GDPR, SOC 2, HIPAA require proper auth/authz
3. **OAuth 2.1 (2025)**: PKCE is now mandatory, implicit grant removed
4. **Passkeys/WebAuthn**: Production-ready passwordless authentication
5. **Zero Trust**: Modern architectures require fine-grained authorization

### Cross-Skill Integration Map

| Frontend Skill | Security Integration | Implementation Pattern |
|----------------|---------------------|------------------------|
| **forms** | Login/register forms, validation | OAuth flows, password hashing |
| **dashboards** | Role-based widget visibility | RBAC/ABAC policies |
| **tables** | Row-level security | Data filtering by permissions |
| **ai-chat** | User context, API keys | JWT auth, rate limiting |
| **feedback** | Auth error messages | Friendly error UX |
| **navigation** | Permission-based nav items | Route guards |
| **All Skills** | Session management | Token refresh, logout |

| Backend Skill | Security Integration | Implementation Pattern |
|---------------|---------------------|------------------------|
| **api-patterns** | JWT validation, CORS | Middleware, interceptors |
| **databases-*** | Connection pooling secrets | Encrypted credentials |
| **message-queues** | Service auth | mTLS, API keys |
| **realtime-sync** | WebSocket auth | Token-based connections |
| **observability** | Audit logging | Who accessed what, when |
| **deploying-applications** | Secrets management | Vault, env vars |

---

## Component Taxonomy

### Tier 1: Authentication Methods

```
┌──────────────────────────────────────────────────────────────────┐
│                    Authentication Methods                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  PASSWORD-BASED (Traditional)                                     │
│  ├── Local (username + password)                                 │
│  │   ├── Argon2id hashing (m=64MB, t=3, p=4)                    │
│  │   ├── Timing-safe comparison                                  │
│  │   └── Password complexity rules (NIST SP 800-63B)            │
│  │                                                               │
│  ├── Sessions (server-side storage)                              │
│  │   ├── Redis/Valkey for session store                         │
│  │   ├── HTTP-only cookies + SameSite=Strict                    │
│  │   └── CSRF protection required                               │
│  │                                                               │
│  └── JWT (stateless tokens)                                      │
│      ├── EdDSA (Ed25519) or ES256 signing                       │
│      ├── Access: 5-15 min, Refresh: 1-7 days                    │
│      └── Refresh token rotation mandatory                        │
│                                                                   │
│  FEDERATED (SSO/Social)                                          │
│  ├── OAuth 2.1 / OpenID Connect                                  │
│  │   ├── PKCE MANDATORY for all flows (2025)                    │
│  │   ├── Exact redirect URI matching                            │
│  │   ├── State parameter for CSRF prevention                    │
│  │   └── Providers: Google, GitHub, Microsoft, etc.             │
│  │                                                               │
│  ├── SAML 2.0 (Enterprise SSO)                                   │
│  │   └── For enterprise customers with existing IdP             │
│  │                                                               │
│  └── Enterprise Identity Providers                               │
│      ├── Keycloak (self-hosted)                                 │
│      ├── Ory (cloud-native, open-source)                        │
│      └── Managed: Auth0, Okta, WorkOS                           │
│                                                                   │
│  PASSWORDLESS (Modern)                                           │
│  ├── Passkeys / WebAuthn                                         │
│  │   ├── FIDO2 standard, biometric auth                         │
│  │   ├── Phishing-resistant by design                           │
│  │   └── Cross-device passkey sync (iCloud, Google)            │
│  │                                                               │
│  ├── Magic Links (email)                                         │
│  │   ├── Time-limited tokens (15 min)                           │
│  │   ├── Single-use only                                         │
│  │   └── Rate limiting critical                                  │
│  │                                                               │
│  └── SMS/Authenticator OTP                                       │
│      ├── TOTP: Time-based (RFC 6238)                            │
│      └── SMS: Least secure, avoid for 2FA                       │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Tier 2: Authorization Models

```
┌──────────────────────────────────────────────────────────────────┐
│                   Authorization Models                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  RBAC (Role-Based Access Control)                                │
│  ├── Assign roles to users                                       │
│  ├── Assign permissions to roles                                 │
│  ├── Simple, widely understood                                   │
│  └── Best for: <100 roles, hierarchical orgs                    │
│                                                                   │
│  ABAC (Attribute-Based Access Control)                           │
│  ├── Rules based on user/resource attributes                    │
│  ├── Example: "Allow if user.department == resource.department" │
│  ├── Flexible, context-aware                                     │
│  └── Best for: Complex policies, dynamic environments           │
│                                                                   │
│  ReBAC (Relationship-Based Access Control)                       │
│  ├── Google Zanzibar model                                       │
│  ├── Graph-based permissions (user → org → team → resource)    │
│  ├── Example: "Can edit if member of doc's workspace"           │
│  └── Best for: Multi-tenant, collaborative apps (Notion-like)   │
│                                                                   │
│  ACL (Access Control Lists)                                      │
│  ├── Direct user → resource mappings                            │
│  ├── Simple but doesn't scale                                    │
│  └── Best for: Small apps, file systems                         │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Tier 3: Implementation Options

#### Managed Auth Services (SaaS)

| Service | Best For | Pricing Model | Key Features |
|---------|----------|---------------|--------------|
| **Clerk** | Rapid development, startups | Free → $25/mo/MAU | Prebuilt UI, Next.js SDK |
| **Auth0** | Enterprise, established | $240/mo → custom | 25+ social providers, SSO |
| **WorkOS AuthKit** | B2B SaaS, enterprise SSO | $0 → custom | SAML/SCIM, admin portal |
| **Supabase Auth** | Postgres users | Free → $25/mo | Built on Postgres, RLS |
| **Firebase Auth** | Mobile-first, GCP | Free → pay-as-you-go | Phone auth, anonymous auth |

#### Self-Hosted Auth Solutions

| Solution | Language | Use Case | Complexity |
|----------|----------|----------|------------|
| **Keycloak** | Java | Enterprise, on-prem | High |
| **Ory** | Go | Cloud-native, microservices | Medium |
| **Authentik** | Python | Modern, developer-friendly | Medium |
| **Authelia** | Go | Reverse proxy auth | Low-Medium |

#### Library-Based (Build Your Own)

| Language | JWT | OAuth/OIDC Client | Passkeys | Password Hashing |
|----------|-----|-------------------|----------|------------------|
| **TypeScript** | jose | Auth.js v5 | @simplewebauthn/server | bcrypt (legacy), Argon2id via Rust |
| **Python** | joserfc | Authlib 1.3+ | py_webauthn | argon2-cffi |
| **Rust** | jsonwebtoken 10.x | oauth2 | webauthn-rs | argon2 |
| **Go** | golang-jwt v5 | go-oidc v3 | go-webauthn | golang.org/x/crypto/argon2 |

---

## Context7 Library Research

### Authentication Libraries

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **Auth.js** | `/websites/authjs_dev` | High | 2,480 | 87.4 | Multi-framework (Next, SvelteKit, SolidStart) |
| NextAuth.js | `/nextauthjs/next-auth` | High | 749 | 91.8 | Next.js specific (legacy name) |
| Auth0 Next.js | `/auth0/nextjs-auth0` | High | 353 | 82.7 | Auth0 SDK for Next.js |
| AuthKit | `/workos/authkit-nextjs` | High | 57 | 93.2 | WorkOS enterprise SSO |

### Validation Libraries

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **Zod** | `/colinhacks/zod` | High | 542 | 90.4 | TypeScript schema validation |
| Zod Full | `/websites/zod_dev` | High | 98,238 | 80.7 | Complete documentation |

### Key Insights

1. **Auth.js v5** (formerly NextAuth.js) is the production standard for TypeScript
2. **Zod** complements auth with input validation (90.4 score, 542 snippets)
3. **WorkOS AuthKit** (93.2 score) is best for B2B enterprise SSO
4. **Lucia v3 deprecation**: Use Auth.js or self-implement (Lucia sunset announced 2024)

---

## OAuth 2.1 Requirements (2025 Standard)

```
┌──────────────────────────────────────────────────────────────────┐
│                 OAuth 2.1 MANDATORY REQUIREMENTS                  │
│                        (RFC 9798 - 2025)                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ✅ REQUIRED (Breaking Changes from OAuth 2.0)                   │
│  ├─ PKCE (Proof Key for Code Exchange) MANDATORY                │
│  │   └─ S256 method (SHA-256), minimum entropy 43 chars         │
│  ├─ Exact redirect URI matching                                  │
│  │   └─ No wildcard matching, no substring matching             │
│  ├─ Authorization code flow ONLY for public clients             │
│  │   └─ All other flows require confidential client             │
│  └─ TLS 1.2+ required for all endpoints                         │
│                                                                   │
│  ❌ REMOVED (No Longer Supported)                                │
│  ├─ Implicit grant (security vulnerabilities)                   │
│  ├─ Resource Owner Password Credentials grant                    │
│  │   └─ Use OAuth 2.0 Device Flow (RFC 8628) instead            │
│  └─ Bearer token in query parameters                             │
│      └─ Must use Authorization header or POST body              │
│                                                                   │
│  JWT ACCESS TOKEN BEST PRACTICES                                 │
│  ├─ Signing Algorithms (in order of preference)                 │
│  │   ├─ EdDSA with Ed25519 (fastest, smallest signatures)       │
│  │   ├─ ES256 (ECDSA with P-256)                                │
│  │   └─ RS256 (RSA, legacy compatibility)                       │
│  ├─ NEVER allow algorithm switching (alg: none attack)          │
│  ├─ Access token lifetime: 5-15 minutes                         │
│  ├─ Refresh token lifetime: 1-7 days with rotation              │
│  ├─ Include 'jti' (JWT ID) for revocation                       │
│  └─ Include 'aud' (audience) for API segmentation               │
│                                                                   │
│  STORAGE & TRANSMISSION                                          │
│  ├─ Access token: Memory only (never localStorage)              │
│  ├─ Refresh token: HTTP-only cookie + SameSite=Strict           │
│  ├─ CSRF token: Separate non-HTTP-only cookie                   │
│  └─ Never log tokens (redact in logs)                           │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Example OAuth 2.1 Flow (TypeScript)

```typescript
// 1. Generate PKCE challenge
import { randomBytes, createHash } from 'crypto'

const codeVerifier = randomBytes(32).toString('base64url') // 43+ chars
const codeChallenge = createHash('sha256')
  .update(codeVerifier)
  .digest('base64url')

// 2. Authorization request
const authUrl = new URL('https://provider.com/oauth/authorize')
authUrl.searchParams.set('client_id', 'your_client_id')
authUrl.searchParams.set('redirect_uri', 'https://app.com/callback') // EXACT match required
authUrl.searchParams.set('response_type', 'code')
authUrl.searchParams.set('scope', 'openid profile email')
authUrl.searchParams.set('state', randomBytes(16).toString('hex')) // CSRF protection
authUrl.searchParams.set('code_challenge', codeChallenge)
authUrl.searchParams.set('code_challenge_method', 'S256')

// 3. Token exchange (in callback route)
const tokenResponse = await fetch('https://provider.com/oauth/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code: authorizationCode,
    redirect_uri: 'https://app.com/callback', // Must match step 2
    client_id: 'your_client_id',
    code_verifier: codeVerifier, // PKCE verification
  }),
})
```

---

## Password Hashing (OWASP 2025)

### Argon2id Standard

```
┌──────────────────────────────────────────────────────────────────┐
│              Argon2id Configuration (2025)                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ALGORITHM: Argon2id                                             │
│  ├─ Hybrid of Argon2i (data-independent) + Argon2d (resistant)  │
│  └─ Winner of Password Hashing Competition (2015)               │
│                                                                   │
│  PARAMETERS (OWASP Recommended)                                  │
│  ├─ Memory cost (m): 64 MB (65536 KiB)                          │
│  ├─ Time cost (t): 3 iterations                                  │
│  ├─ Parallelism (p): 4 threads                                   │
│  └─ Salt length: 16 bytes (128 bits) - random per password      │
│                                                                   │
│  TARGET PERFORMANCE                                              │
│  ├─ Hash time: 150-250ms on server hardware                     │
│  ├─ Adjust 'm' parameter to hit target on your hardware         │
│  └─ Balance: User experience vs. brute-force resistance         │
│                                                                   │
│  ENCODING FORMAT                                                 │
│  └─ PHC String Format (Password Hashing Competition)            │
│      Example:                                                     │
│      $argon2id$v=19$m=65536,t=3,p=4$<salt>$<hash>               │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Implementation Examples

#### Python (argon2-cffi)

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Initialize with OWASP 2025 parameters
ph = PasswordHasher(
    time_cost=3,        # iterations
    memory_cost=65536,  # 64 MB
    parallelism=4,      # threads
    hash_len=32,        # output length
    salt_len=16         # salt length
)

# Hash password
password_hash = ph.hash("user_password")
# Returns: $argon2id$v=19$m=65536,t=3,p=4$...$...

# Verify password (timing-safe)
try:
    ph.verify(password_hash, "user_password")
    # Password matches

    # Check if rehashing needed (parameters changed)
    if ph.check_needs_rehash(password_hash):
        new_hash = ph.hash("user_password")
        # Update database with new_hash
except VerifyMismatchError:
    # Password does not match
    pass
```

#### Rust (argon2)

```rust
use argon2::{
    password_hash::{rand_core::OsRng, PasswordHash, PasswordHasher, PasswordVerifier, SaltString},
    Argon2, Params, Algorithm, Version
};

// Create Argon2 instance with OWASP 2025 parameters
let params = Params::new(
    65536,  // memory cost (64 MB)
    3,      // time cost
    4,      // parallelism
    None    // output length (default 32)
).unwrap();

let argon2 = Argon2::new(
    Algorithm::Argon2id,
    Version::V0x13,
    params
);

// Hash password
let salt = SaltString::generate(&mut OsRng);
let password_hash = argon2
    .hash_password(b"user_password", &salt)
    .unwrap()
    .to_string();

// Verify password (timing-safe)
let parsed_hash = PasswordHash::new(&password_hash).unwrap();
let result = argon2.verify_password(b"user_password", &parsed_hash);

match result {
    Ok(_) => println!("Password matches"),
    Err(_) => println!("Invalid password"),
}
```

### Legacy Migration

If migrating from bcrypt/scrypt:

1. **Don't force password resets** - migrate on next login
2. **Check hash format** - bcrypt starts with `$2a$` or `$2b$`
3. **Verify with old algorithm** - if match, rehash with Argon2id
4. **Update database** - atomic update to prevent race conditions

```python
def verify_and_migrate(user_password: str, stored_hash: str) -> tuple[bool, str | None]:
    """Verify password and migrate to Argon2id if needed."""
    if stored_hash.startswith('$argon2id$'):
        # Already using Argon2id
        try:
            ph.verify(stored_hash, user_password)
            return (True, None)
        except VerifyMismatchError:
            return (False, None)

    elif stored_hash.startswith('$2a$') or stored_hash.startswith('$2b$'):
        # Legacy bcrypt
        import bcrypt
        if bcrypt.checkpw(user_password.encode(), stored_hash.encode()):
            # Valid password - migrate to Argon2id
            new_hash = ph.hash(user_password)
            return (True, new_hash)
        else:
            return (False, None)

    else:
        raise ValueError(f"Unknown hash format: {stored_hash[:10]}")
```

---

## Authorization Engines

### Comparison Table

| Engine | Model | Language | Deployment | Best Use Case |
|--------|-------|----------|------------|---------------|
| **Open Policy Agent (OPA)** | ABAC/General | Rego DSL | Sidecar/Library | Kubernetes, cloud-native |
| **Casbin** | RBAC/ABAC/ACL | Native (Go, Rust, Python, JS) | Embedded library | Multi-language projects |
| **SpiceDB** | ReBAC (Zanzibar) | Go | Standalone service | Multi-tenant, relationship-heavy |
| **Cerbos** | ABAC | Go | API service | API-first, policy-as-code |
| **Oso** | RBAC/ABAC/ReBAC | Polar DSL | Embedded library | Application-level policies |

### Decision Framework

```
┌──────────────────────────────────────────────────────────────────┐
│              Authorization Engine Selection                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  AUTHORIZATION NEED?                                             │
│  ├── SIMPLE ROLES (<20 roles)                                    │
│  │   └─ Self-implement with Casbin (embedded, any language)     │
│  │       └─ Example: Admin, User, Guest                         │
│  │                                                               │
│  ├── KUBERNETES / INFRASTRUCTURE                                 │
│  │   └─ OPA (Gatekeeper for K8s admission control)              │
│  │       └─ Example: Enforce pod security policies              │
│  │                                                               │
│  ├── COMPLEX ATTRIBUTE RULES                                     │
│  │   ├─ Many attributes → OPA or Cerbos                         │
│  │   │   └─ Example: "Allow if user.clearance >= doc.level      │
│  │   │                AND user.dept == doc.dept                 │
│  │   │                AND time.hour >= 9 AND time.hour < 17"    │
│  │   └─ API-first → Cerbos (gRPC API, policy git sync)         │
│  │                                                               │
│  ├── RELATIONSHIP-BASED (Multi-Tenant, Collaborative)           │
│  │   └─ SpiceDB (Google Zanzibar model)                         │
│  │       └─ Example: "Can edit if member of doc's workspace    │
│  │                    AND workspace.plan includes feature"      │
│  │       └─ Use cases: Notion-like, GitHub-like permissions    │
│  │                                                               │
│  └── EMBEDDED APPLICATION LOGIC                                  │
│      └─ Oso (Python/Ruby/Java/Rust/Node)                        │
│          └─ Example: Resource-level policies in app code        │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### SpiceDB (Zanzibar-Style ReBAC)

**Why SpiceDB for Modern Apps:**

- **Relationship graphs**: `user:alice → member → workspace:acme → parent → doc:123`
- **Recursive checks**: Permissions inherit through relationships
- **Sub-second performance**: Optimized for deep graph traversal
- **Consistency**: Distributed system with snapshot reads

**Example Schema (Notion-like):**

```zed
// SpiceDB schema language

definition user {}

definition workspace {
    relation member: user
    relation admin: user

    permission view = member + admin
    permission edit = admin
}

definition document {
    relation workspace: workspace
    relation writer: user

    permission view = workspace->view + writer
    permission edit = workspace->edit + writer
}
```

**Check Permission:**

```bash
# Can alice edit doc:123?
spicedb check user:alice edit document:123

# Returns: true/false based on relationship graph
```

---

## Libraries by Language

### TypeScript/JavaScript

| Category | Library | Version | Notes |
|----------|---------|---------|-------|
| **Auth Framework** | Auth.js (NextAuth) | v5 | Next.js, SvelteKit, SolidStart |
| **JWT** | jose | 5.x | EdDSA, ES256, RS256 support |
| **OAuth Client** | arctic | 2.x | Lightweight OAuth flows |
| **Passkeys** | @simplewebauthn/server | 11.x | FIDO2 server implementation |
| **Password Hashing** | Call Rust via FFI | - | No native Argon2id in JS |
| **Validation** | Zod | 3.x | Schema validation, type inference |
| **Policy Engine** | Casbin.js | 1.x | RBAC/ABAC embedded |

### Python

| Category | Library | Version | Notes |
|----------|---------|---------|-------|
| **Auth Framework** | Authlib | 1.3+ | OAuth/OIDC client + server |
| **JWT** | joserfc | 1.x | Modern, maintained (replaces PyJWT) |
| **OAuth Client** | Authlib | 1.3+ | Google, GitHub, etc. |
| **Passkeys** | py_webauthn | 2.x | WebAuthn server |
| **Password Hashing** | argon2-cffi | 24.x | Argon2id with OWASP params |
| **Validation** | Pydantic | 2.x | Data validation, FastAPI integration |
| **Policy Engine** | PyCasbin | 1.x | RBAC/ABAC embedded |

### Rust

| Category | Library | Version | Notes |
|----------|---------|---------|-------|
| **JWT** | jsonwebtoken | 10.x | EdDSA, ES256, RS256 |
| **OAuth Client** | oauth2 | 5.x | OAuth 2.1 flows |
| **Passkeys** | webauthn-rs | 0.5.x | WebAuthn server + attestation |
| **Password Hashing** | argon2 | 0.5.x | Native Argon2id |
| **Validation** | validator | 0.18.x | Struct validation |
| **Policy Engine** | Casbin-RS | 2.x | RBAC/ABAC embedded |

### Go

| Category | Library | Version | Notes |
|----------|---------|---------|-------|
| **JWT** | golang-jwt | v5 | Community-maintained |
| **OAuth Client** | go-oidc | v3 | OIDC client only |
| **Passkeys** | go-webauthn | 0.11.x | Duo-maintained |
| **Password Hashing** | golang.org/x/crypto/argon2 | - | Standard library |
| **Validation** | validator | v10 | Struct tag validation |
| **Policy Engine** | Casbin | v2 | Original implementation |

---

## API Security Best Practices

### Rate Limiting

```typescript
// Tiered rate limiting (per IP + per user)
const rateLimits = {
  anonymous: '10 requests/minute',
  authenticated: '100 requests/minute',
  premium: '1000 requests/minute',
}

// Use sliding window (not fixed window)
// Redis-based implementation with `ioredis`
```

### CORS Configuration

```typescript
// Restrictive CORS (production)
const corsOptions = {
  origin: ['https://app.example.com'],
  credentials: true,
  maxAge: 86400, // 24 hours
  allowedHeaders: ['Content-Type', 'Authorization'],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
}

// NEVER use origin: '*' with credentials: true
```

### Security Headers

```typescript
// Helmet.js or manual headers
const securityHeaders = {
  'Strict-Transport-Security': 'max-age=63072000; includeSubDomains; preload',
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
  'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'",
}
```

### Input Validation (Defense in Depth)

```typescript
// 1. Schema validation (Zod/Pydantic)
const LoginSchema = z.object({
  email: z.string().email().max(255),
  password: z.string().min(8).max(128),
})

// 2. Sanitization (escape HTML, SQL injection prevention)
// Use parameterized queries (ALWAYS)
const user = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [email] // Parameterized - prevents SQL injection
)

// 3. Rate limiting on auth endpoints
// 4. CAPTCHA for signup/login (Cloudflare Turnstile, hCaptcha)
```

---

## Frontend Integration Patterns

### Login Form (React + Auth.js)

```typescript
// app/login/page.tsx
'use client'

import { signIn } from 'next-auth/react'
import { useState } from 'react'
import { z } from 'zod'

const LoginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be 8+ characters'),
})

export default function LoginPage() {
  const [error, setError] = useState('')

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)

    // Validate input
    const result = LoginSchema.safeParse({
      email: formData.get('email'),
      password: formData.get('password'),
    })

    if (!result.success) {
      setError(result.error.errors[0].message)
      return
    }

    // Sign in with credentials
    const response = await signIn('credentials', {
      email: result.data.email,
      password: result.data.password,
      redirect: false,
    })

    if (response?.error) {
      setError('Invalid credentials')
    } else {
      window.location.href = '/dashboard'
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" required />
      <input name="password" type="password" required />
      {error && <p className="error">{error}</p>}
      <button type="submit">Sign In</button>
    </form>
  )
}
```

### Protected Route (Middleware)

```typescript
// middleware.ts (Next.js)
import { withAuth } from 'next-auth/middleware'

export default withAuth({
  callbacks: {
    authorized: ({ token, req }) => {
      // Require authentication for /dashboard/*
      if (req.nextUrl.pathname.startsWith('/dashboard')) {
        return !!token
      }
      // Admin-only routes
      if (req.nextUrl.pathname.startsWith('/admin')) {
        return token?.role === 'admin'
      }
      return true
    },
  },
})

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*'],
}
```

### Role-Based UI Rendering

```typescript
// components/AdminPanel.tsx
'use client'

import { useSession } from 'next-auth/react'

export function AdminPanel() {
  const { data: session } = useSession()

  if (session?.user?.role !== 'admin') {
    return null // Don't render for non-admins
  }

  return (
    <div>
      <h2>Admin Controls</h2>
      {/* Admin-only UI */}
    </div>
  )
}
```

---

## Decision Framework

```
┌──────────────────────────────────────────────────────────────────┐
│            Authentication & Authorization Selection               │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  PROJECT TYPE?                                                   │
│  ├── RAPID DEVELOPMENT / STARTUP (Time to Market)               │
│  │   ├─ Need UI components? → Clerk ($25/mo, prebuilt UI)      │
│  │   └─ Flexible framework? → Auth.js v5 (free, open-source)   │
│  │                                                               │
│  ├── ENTERPRISE / B2B SAAS (SSO Required)                        │
│  │   ├─ Managed + SAML/SCIM → WorkOS AuthKit or Auth0          │
│  │   ├─ Self-hosted → Keycloak (Java, mature)                  │
│  │   └─ Cloud-native → Ory (Go, Kubernetes-friendly)           │
│  │                                                               │
│  ├── API-ONLY BACKEND (No UI)                                   │
│  │   ├─ Simple JWT auth → jsonwebtoken library                 │
│  │   ├─ OAuth provider → Build with Authlib (Python) or       │
│  │   │                    oauth2 (Rust)                         │
│  │   └─ Fine-grained authz → OPA or Cerbos policy engine       │
│  │                                                               │
│  ├── PASSWORDLESS / MODERN UX                                    │
│  │   ├─ Passkeys/WebAuthn → @simplewebauthn (TS),              │
│  │   │                       py_webauthn (Python),              │
│  │   │                       webauthn-rs (Rust)                 │
│  │   ├─ Magic links → Resend (email), Auth.js (built-in)       │
│  │   └─ SMS OTP → Twilio (avoid for 2FA, phishing risk)        │
│  │                                                               │
│  ├── MULTI-TENANT / COLLABORATIVE (Notion-like)                 │
│  │   └─ Relationship-based permissions → SpiceDB (Zanzibar)    │
│  │       └─ Example: user → workspace → document hierarchy     │
│  │                                                               │
│  └── HIGH COMPLIANCE (HIPAA, SOC 2, FedRAMP)                    │
│      ├─ Audit logging → OPA with decision logs                 │
│      ├─ Session management → Short-lived tokens + rotation     │
│      └─ Consider managed: Auth0 (SOC 2), Keycloak (on-prem)    │
│                                                                   │
│  AUTHORIZATION COMPLEXITY?                                       │
│  ├─ Simple roles (<20) → Self-implement with Casbin            │
│  ├─ Attribute-based → OPA or Cerbos                            │
│  └─ Relationship graphs → SpiceDB                               │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Skill Structure

```
auth-security/
├── init.md                          # This file - master plan
├── SKILL.md                         # Main skill file (< 500 lines)
├── references/
│   ├── oauth21-guide.md             # OAuth 2.1 implementation guide
│   ├── jwt-best-practices.md       # JWT generation, validation, storage
│   ├── passkeys-webauthn.md        # Passkeys/FIDO2 implementation
│   ├── password-hashing.md         # Argon2id parameters, migration
│   ├── authorization-patterns.md   # RBAC, ABAC, ReBAC comparison
│   ├── spicedb-guide.md            # Zanzibar-style permissions
│   ├── api-security.md             # Rate limiting, CORS, headers
│   ├── session-management.md       # Server-side sessions, Redis
│   ├── managed-auth-comparison.md  # Clerk, Auth0, WorkOS, Supabase
│   └── self-hosted-auth.md         # Keycloak, Ory, Authentik setup
├── scripts/
│   ├── generate_jwt_keys.py        # EdDSA/ES256 key generation
│   ├── validate_oauth_config.py    # OAuth 2.1 config validator
│   ├── benchmark_argon2.py         # Tune Argon2id params for hardware
│   └── audit_permissions.py        # Scan code for hardcoded permissions
├── examples/
│   ├── authjs-nextjs/              # Auth.js v5 + Next.js 15
│   ├── keycloak-fastapi/           # Keycloak + FastAPI + OIDC
│   ├── passkeys-demo/              # Passkeys with @simplewebauthn
│   ├── spicedb-permissions/        # SpiceDB + multi-tenant app
│   └── oauth-pkce-flow/            # Manual OAuth 2.1 implementation
└── assets/
    ├── templates/
    │   ├── auth-middleware.ts.tmpl
    │   ├── login-form.tsx.tmpl
    │   └── oauth-callback.py.tmpl
    └── schemas/
        └── jwt-claims.json          # Standard JWT claim schema
```

---

## SKILL.md Frontmatter Template

```yaml
---
name: auth-security
description: Authentication, authorization, and API security implementation across Python, Rust, Go, and TypeScript. Use when building user systems, protecting APIs, or implementing access control. Covers OAuth 2.1/OIDC (PKCE mandatory), JWT best practices (EdDSA/ES256), sessions, Passkeys/WebAuthn (FIDO2), password hashing (Argon2id), RBAC/ABAC/ReBAC authorization, policy engines (OPA, Casbin, SpiceDB), managed auth (Clerk, Auth0, WorkOS), self-hosted (Keycloak, Ory), and API security (rate limiting, CORS, CSP).
---
```

---

## Quality Checklist

### Before Finalizing SKILL.md:

**Core Quality:**
- [ ] OAuth 2.1 mandatory PKCE emphasized (2025 standard)
- [ ] Passkeys/WebAuthn presented as production-ready option
- [ ] Argon2id parameters justify 150-250ms target
- [ ] JWT signing algorithms prioritized: EdDSA > ES256 > RS256
- [ ] Refresh token rotation pattern documented
- [ ] Lucia v3 deprecation note included (use Auth.js or self-implement)
- [ ] Token storage rules (HTTP-only cookies, not localStorage)
- [ ] No hardcoded secrets in examples

**Authorization Coverage:**
- [ ] RBAC, ABAC, ReBAC models compared
- [ ] SpiceDB positioned for Zanzibar-like use cases
- [ ] OPA for Kubernetes/infrastructure policies
- [ ] Casbin for embedded application logic
- [ ] Decision framework for engine selection

**Multi-Language Support:**
- [ ] TypeScript: Auth.js v5, jose, @simplewebauthn
- [ ] Python: Authlib, joserfc, argon2-cffi, py_webauthn
- [ ] Rust: jsonwebtoken, oauth2, webauthn-rs, argon2
- [ ] Go: golang-jwt, go-oidc, go-webauthn
- [ ] Consistent patterns across languages

**Security Best Practices:**
- [ ] Rate limiting examples (per IP + per user)
- [ ] CORS configuration (no wildcards with credentials)
- [ ] Security headers (Helmet.js equivalent)
- [ ] Input validation (Zod/Pydantic + parameterized queries)
- [ ] CSRF protection patterns
- [ ] Audit logging for compliance

**Context7 Integration:**
- [ ] Auth.js (87.4 score, 2,480 snippets) as primary TypeScript library
- [ ] Zod (90.4 score, 542 snippets) for validation
- [ ] WorkOS AuthKit (93.2 score) for enterprise SSO
- [ ] Trust scores cited for library recommendations

**Frontend Integration:**
- [ ] Login/register form examples
- [ ] Protected route middleware (Next.js, React Router)
- [ ] Role-based UI rendering patterns
- [ ] Session management (useSession hook examples)
- [ ] OAuth callback handling

**Scripts & Validation:**
- [ ] JWT key generation script (EdDSA, ES256)
- [ ] OAuth 2.1 config validator (PKCE checks)
- [ ] Argon2id benchmark script (tune for hardware)
- [ ] Permission audit script (find hardcoded roles)
- [ ] All scripts executable without context loading (token-free)

**Examples & Templates:**
- [ ] Auth.js v5 + Next.js 15 full example
- [ ] Keycloak + FastAPI integration
- [ ] Passkeys demo with @simplewebauthn
- [ ] SpiceDB multi-tenant permissions
- [ ] Manual OAuth 2.1 PKCE flow

**Documentation Quality:**
- [ ] SKILL.md under 500 lines (progressive disclosure)
- [ ] References are one level deep from SKILL.md
- [ ] No Windows-style paths (use forward slashes)
- [ ] Consistent terminology (access token, refresh token, etc.)
- [ ] Real code examples, not pseudocode
- [ ] Version numbers specified for libraries

---

## Integration with Other Skills

### forms Skill
- Validation schemas → Zod/Pydantic for auth inputs
- Login forms → Email validation, password strength
- Register forms → Password confirmation, terms acceptance
- Error states → Auth-specific error messages

### dashboards Skill
- Role-based widgets → Show/hide based on user.role
- Data filtering → Row-level security in API
- Audit trail → Who viewed what, when
- User profile → Display user info, logout button

### tables Skill
- Row-level security → Filter data by user permissions
- Action buttons → Disable edit/delete for non-owners
- Bulk actions → Check permissions before execution

### api-patterns Skill
- JWT middleware → Validate tokens before route handlers
- CORS config → Match auth cookie SameSite settings
- Error handling → Return 401/403 with descriptive messages
- OpenAPI docs → Document auth requirements (Bearer token)

### observability Skill
- Audit logs → Log auth events (login, logout, permission denied)
- Trace context → Include user ID in spans
- Metrics → Track login success/failure rates
- Alerts → Notify on suspicious auth activity

### deploying-applications Skill
- Secrets management → Vault, AWS Secrets Manager, env vars
- OAuth redirect URIs → Set per environment (dev, staging, prod)
- Database migrations → Secure connection strings
- Health checks → Exclude from auth requirements

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2025-12-02 | Initial master plan created |

---

## Research References

### Standards & Specifications
- **OAuth 2.1** (RFC 9798, 2025) - PKCE mandatory, implicit grant removed
- **OpenID Connect** (OIDC) - Identity layer on OAuth 2.1
- **FIDO2/WebAuthn** (W3C) - Passkeys specification
- **OWASP Authentication Cheat Sheet** (2025) - Password hashing, session management
- **NIST SP 800-63B** - Digital identity guidelines

### Libraries (Context7 Verified)
- **Auth.js v5** (87.4 score, 2,480 snippets) - Multi-framework auth
- **Zod** (90.4 score, 542 snippets) - TypeScript validation
- **WorkOS AuthKit** (93.2 score, 57 snippets) - Enterprise SSO
- **NextAuth.js** (91.8 score, 749 snippets) - Legacy name for Auth.js

### Authorization Engines
- **SpiceDB** - Google Zanzibar-inspired ReBAC
- **Open Policy Agent (OPA)** - CNCF project, Rego policies
- **Casbin** - Multi-language RBAC/ABAC library
- **Cerbos** - API-first policy engine

### Password Hashing
- **Argon2** - Winner of Password Hashing Competition (2015)
- **argon2-cffi** (Python) - OWASP recommended parameters
- **argon2** (Rust) - Native implementation

### Managed Auth Services
- **Clerk** - Developer-friendly, prebuilt UI
- **Auth0** - Enterprise SSO, 25+ providers
- **WorkOS** - B2B SaaS focus, SAML/SCIM
- **Supabase Auth** - Postgres-based, row-level security

### Self-Hosted Solutions
- **Keycloak** - Java, mature, SAML/OIDC
- **Ory** - Go, cloud-native, Kubernetes-friendly
- **Authentik** - Python, modern UI

---

*Document generated: December 2025*
*Status: Planning Phase - Ready for SKILL.md implementation*
