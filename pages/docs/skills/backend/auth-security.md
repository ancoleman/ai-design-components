---
sidebar_position: 10
title: Auth & Security
description: Authentication, authorization, and API security implementation
tags: [backend, security, auth, oauth, jwt, passkeys]
---

# Authentication & Security

Implement modern authentication, authorization, and API security across Python, Rust, Go, and TypeScript.

## When to Use

Use when:
- Building user authentication systems (login, signup, SSO)
- Implementing authorization (roles, permissions, access control)
- Securing APIs (JWT validation, rate limiting)
- Adding passwordless auth (Passkeys/WebAuthn)
- Migrating from password-based to modern auth
- Integrating enterprise SSO (SAML, OIDC)
- Implementing fine-grained permissions (RBAC, ABAC, ReBAC)

## Multi-Language Support

This skill provides patterns for:
- **Python**: Authlib, joserfc (JWT), argon2-cffi, py_webauthn
- **TypeScript**: Auth.js v5, jose 5.x, @simplewebauthn/server, Zod
- **Rust**: jsonwebtoken, oauth2, webauthn-rs, argon2
- **Go**: golang-jwt, go-oidc, go-webauthn, x/crypto/argon2

## OAuth 2.1 Mandatory Requirements (2025 Standard)

```
┌─────────────────────────────────────────────────────────────┐
│           OAuth 2.1 MANDATORY REQUIREMENTS                  │
│                   (RFC 9798 - 2025)                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ REQUIRED (Breaking Changes from OAuth 2.0)             │
│  ├─ PKCE (Proof Key for Code Exchange) MANDATORY           │
│  │   └─ S256 method (SHA-256), minimum entropy 43 chars   │
│  ├─ Exact redirect URI matching                            │
│  │   └─ No wildcard matching, no substring matching       │
│  ├─ Authorization code flow ONLY for public clients       │
│  │   └─ All other flows require confidential client       │
│  └─ TLS 1.2+ required for all endpoints                   │
│                                                             │
│  ❌ REMOVED (No Longer Supported)                          │
│  ├─ Implicit grant (security vulnerabilities)             │
│  ├─ Resource Owner Password Credentials grant              │
│  └─ Bearer token in query parameters                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Critical:** PKCE is now mandatory for ALL OAuth flows, not just public clients.

## JWT Best Practices

### Signing Algorithms (Priority Order)

1. **EdDSA with Ed25519** (Recommended)
   - Fastest performance
   - Smallest signature size
   - Modern cryptography

2. **ES256 (ECDSA with P-256)**
   - Good performance
   - Industry standard
   - Wide compatibility

3. **RS256 (RSA)**
   - Legacy compatibility
   - Larger signatures
   - Slower performance

**NEVER allow `alg: none` or algorithm switching attacks.**

### Token Lifetimes (Concrete Values)

- **Access token:** 5-15 minutes
- **Refresh token:** 1-7 days with rotation
- **ID token:** Same as access token (5-15 minutes)

**Refresh token rotation:** Each refresh generates new access AND refresh tokens, invalidating the old refresh token.

### Token Storage

- **Access token:** Memory only (never localStorage)
- **Refresh token:** HTTP-only cookie + SameSite=Strict
- **CSRF token:** Separate non-HTTP-only cookie
- **Never log tokens:** Redact in application logs

### JWT Claims (Required)

```json
{
  "iss": "https://auth.example.com",
  "sub": "user-id-123",
  "aud": "api.example.com",
  "exp": 1234567890,
  "iat": 1234567890,
  "jti": "unique-token-id",
  "scope": "read:profile write:data"
}
```

## Password Hashing with Argon2id

### OWASP 2025 Parameters

```
Algorithm: Argon2id
Memory cost (m): 64 MB (65536 KiB)
Time cost (t): 3 iterations
Parallelism (p): 4 threads
Salt length: 16 bytes (128 bits)
Target hash time: 150-250ms
```

**Key Points:**
- Argon2id is hybrid: data-independent timing + memory-hard
- Tune memory cost to achieve 150-250ms on YOUR hardware
- Use timing-safe comparison for verification
- Migrate from bcrypt gradually (verify with old, rehash with new)

## Passkeys / WebAuthn

Passkeys provide phishing-resistant, passwordless authentication using FIDO2/WebAuthn.

### When to Use Passkeys

- User-facing applications prioritizing security
- Reducing password-related support burden
- Mobile-first applications (biometric auth)
- Applications requiring MFA without SMS

### Cross-Device Passkey Sync

- **iCloud Keychain:** Apple ecosystem (iOS 16+, macOS 13+)
- **Google Password Manager:** Android, Chrome
- **1Password, Bitwarden:** Third-party password managers

## Authorization Models

```text
┌─────────────────────────────────────────────────────────────┐
│                Authorization Model Selection                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Simple Roles (<20 roles)                                  │
│  └─ RBAC with Casbin (embedded, any language)              │
│      Example: Admin, User, Guest                           │
│                                                             │
│  Complex Attribute Rules                                    │
│  └─ ABAC with OPA or Cerbos                                │
│      Example: "Allow if user.clearance >= doc.level        │
│                AND user.dept == doc.dept"                   │
│                                                             │
│  Relationship-Based (Multi-Tenant, Collaborative)          │
│  └─ ReBAC with SpiceDB (Zanzibar model)                    │
│      Example: "Can edit if member of doc's workspace       │
│                AND workspace.plan includes feature"         │
│      Use cases: Notion-like, GitHub-like permissions       │
│                                                             │
│  Kubernetes / Infrastructure Policies                       │
│  └─ OPA (Gatekeeper for admission control)                 │
│      Example: Enforce pod security policies                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Library Selection by Language

### TypeScript
- **Auth Framework**: Auth.js v5
- **JWT**: jose 5.x
- **Passkeys**: @simplewebauthn/server 11.x
- **Validation**: Zod 3.x
- **Policy Engine**: Casbin.js 1.x

### Python
- **Auth Framework**: Authlib 1.3+
- **JWT**: joserfc 1.x
- **Passkeys**: py_webauthn 2.x
- **Password Hashing**: argon2-cffi 24.x
- **Validation**: Pydantic 2.x
- **Policy Engine**: PyCasbin 1.x

### Rust
- **JWT**: jsonwebtoken 10.x
- **OAuth Client**: oauth2 5.x
- **Passkeys**: webauthn-rs 0.5.x
- **Password Hashing**: argon2 0.5.x
- **Policy Engine**: Casbin-RS 2.x

### Go
- **JWT**: golang-jwt v5
- **OAuth Client**: go-oidc v3
- **Passkeys**: go-webauthn 0.11.x
- **Password Hashing**: golang.org/x/crypto/argon2
- **Policy Engine**: Casbin v2

## Managed Auth Services

| Service | Best For | Key Features |
|---------|----------|--------------|
| **Clerk** | Rapid development, startups | Prebuilt UI, Next.js SDK |
| **Auth0** | Enterprise, established | 25+ social providers, SSO |
| **WorkOS AuthKit** | B2B SaaS, enterprise SSO | SAML/SCIM, admin portal |
| **Supabase Auth** | Postgres users | Built on Postgres, RLS |

## Self-Hosted Solutions

| Solution | Language | Use Case |
|----------|----------|----------|
| **Keycloak** | Java | Enterprise, on-prem |
| **Ory** | Go | Cloud-native, microservices |
| **Authentik** | Python | Modern, developer-friendly |

## API Security Best Practices

### Rate Limiting

```typescript
// Tiered rate limiting (per IP + per user)
const rateLimits = {
  anonymous: '10 requests/minute',
  authenticated: '100 requests/minute',
  premium: '1000 requests/minute',
}
```

Use sliding window algorithm (not fixed window) with Redis.

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
const securityHeaders = {
  'Strict-Transport-Security': 'max-age=63072000; includeSubDomains; preload',
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
  'Content-Security-Policy': "default-src 'self'; script-src 'self'",
}
```

## Frontend Integration Patterns

### Protected Routes (Next.js)

```typescript
// middleware.ts
import { withAuth } from 'next-auth/middleware'

export default withAuth({
  callbacks: {
    authorized: ({ token, req }) => {
      if (req.nextUrl.pathname.startsWith('/dashboard')) {
        return !!token
      }
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
import { useSession } from 'next-auth/react'

export function AdminPanel() {
  const { data: session } = useSession()

  if (session?.user?.role !== 'admin') {
    return null
  }

  return <div>Admin Controls</div>
}
```

## Common Workflows

### 1. OAuth 2.1 Integration

1. Generate PKCE challenge
2. Redirect to authorization endpoint
3. Handle callback with authorization code
4. Exchange code for tokens (with code_verifier)
5. Store tokens securely
6. Implement refresh token rotation

### 2. JWT Implementation

1. Generate signing keys
2. Configure token lifetimes (5-15 min access, 1-7 day refresh)
3. Implement token validation middleware
4. Set up refresh token rotation
5. Configure token storage (memory for access, HTTP-only cookie for refresh)

### 3. Passkeys Setup

1. Register credential during signup/settings
2. Generate challenge for registration
3. Verify attestation
4. Store credential ID and public key
5. Implement authentication flow with assertion

## Integration with Other Skills

### Forms Skill
- Login/register forms with validation
- Error states for auth failures
- Password strength indicators

### API Patterns Skill
- JWT middleware integration
- Error response formats (401, 403)
- OpenAPI security schemas

### Dashboards Skill
- Role-based widget visibility
- User profile display
- Permission-based data filtering

### Observability Skill
- Auth event logging (login, logout, permission denied)
- Failed login tracking
- Token refresh monitoring

## Related Skills

- [API Patterns](./api-patterns) - Secure REST/GraphQL APIs
- [Forms](../frontend/forms) - Login and registration forms
- [Observability](./observability) - Security event logging

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/auth-security)
- OAuth 2.1: https://oauth.net/2.1/
- Auth.js: https://authjs.dev/
- Authlib: https://docs.authlib.org/
- Passkeys: https://passkeys.dev/
