# JWT Best Practices

JSON Web Tokens (JWT) for stateless authentication and authorization.

## JWT Structure

```
header.payload.signature
```

### Header

```json
{
  "alg": "EdDSA",
  "typ": "JWT"
}
```

### Payload (Claims)

```json
{
  "iss": "https://auth.example.com",
  "sub": "user-id-123",
  "aud": "api.example.com",
  "exp": 1735689600,
  "iat": 1735686000,
  "jti": "unique-token-id-abc123",
  "scope": "read:profile write:data"
}
```

### Signature

HMAC or asymmetric signature (EdDSA, ES256, RS256).

## Signing Algorithms (Priority Order)

### 1. EdDSA with Ed25519 (Recommended)

**Why:**
- Fastest performance (10x faster than RSA)
- Smallest signatures (64 bytes)
- Modern cryptography (no known weaknesses)
- Deterministic signatures (same input = same signature)

**When to Use:**
- New projects (2025+)
- High-performance requirements
- Microservices (small token size)

**TypeScript (jose):**
```typescript
import { SignJWT, jwtVerify, generateKeyPair } from 'jose'

// Generate key pair (do this once, store securely)
const { publicKey, privateKey } = await generateKeyPair('EdDSA')

// Sign JWT
const jwt = await new SignJWT({ userId: '123', role: 'admin' })
  .setProtectedHeader({ alg: 'EdDSA' })
  .setIssuedAt()
  .setIssuer('https://auth.example.com')
  .setAudience('api.example.com')
  .setExpirationTime('15m')
  .sign(privateKey)

// Verify JWT
const { payload } = await jwtVerify(jwt, publicKey, {
  issuer: 'https://auth.example.com',
  audience: 'api.example.com',
})
```

**Python (joserfc):**
```python
from joserfc import jwt
from joserfc.jwk import OKPKey

# Generate key pair
private_key = OKPKey.generate_key('Ed25519')
public_key = private_key.as_public()

# Sign JWT
claims = {
    'iss': 'https://auth.example.com',
    'sub': 'user-123',
    'aud': 'api.example.com',
    'exp': int(time.time()) + 900,  # 15 minutes
}
token = jwt.encode({'alg': 'EdDSA'}, claims, private_key)

# Verify JWT
claims = jwt.decode(token, public_key)
```

**Rust (jsonwebtoken):**
```rust
use jsonwebtoken::{encode, decode, Header, Validation, Algorithm, EncodingKey, DecodingKey};
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct Claims {
    sub: String,
    iss: String,
    aud: String,
    exp: usize,
}

// Generate key pair with `openssl genpkey -algorithm ED25519`
let encoding_key = EncodingKey::from_ed_pem(private_key_pem)?;
let decoding_key = DecodingKey::from_ed_pem(public_key_pem)?;

// Sign JWT
let claims = Claims {
    sub: "user-123".to_string(),
    iss: "https://auth.example.com".to_string(),
    aud: "api.example.com".to_string(),
    exp: (chrono::Utc::now() + chrono::Duration::minutes(15)).timestamp() as usize,
};
let token = encode(&Header::new(Algorithm::EdDSA), &claims, &encoding_key)?;

// Verify JWT
let mut validation = Validation::new(Algorithm::EdDSA);
validation.set_audience(&["api.example.com"]);
validation.set_issuer(&["https://auth.example.com"]);
let token_data = decode::<Claims>(&token, &decoding_key, &validation)?;
```

### 2. ES256 (ECDSA with P-256)

**Why:**
- Industry standard (widely supported)
- Good performance (faster than RSA)
- Smaller keys than RSA (256-bit)
- FIPS 186-4 approved

**When to Use:**
- Compatibility requirements
- Government/regulated industries
- Legacy systems upgrade from RS256

**TypeScript (jose):**
```typescript
const { publicKey, privateKey } = await generateKeyPair('ES256')

const jwt = await new SignJWT({ userId: '123' })
  .setProtectedHeader({ alg: 'ES256' })
  .setExpirationTime('15m')
  .sign(privateKey)
```

### 3. RS256 (RSA with SHA-256)

**Why:**
- Maximum compatibility
- Well-understood algorithm
- Key rotation easier (public key distribution)

**When to Use:**
- Legacy system compatibility
- OpenID Connect providers (common default)
- When EdDSA/ES256 not available

**Performance Note:** 10x slower than EdDSA, larger signatures (256 bytes).

### Never Use

- **HS256 (HMAC):** Symmetric key, hard to rotate, key must be on all services
- **RS384, RS512:** No benefit over RS256, larger signatures
- **none:** Algorithm bypass attack, always validate algorithm

## Token Lifetimes

### Access Token: 5-15 Minutes

**Reasoning:**
- Limits damage if token stolen
- Forces refresh, enabling revocation
- Balances UX (not too many refreshes) with security

**Implementation:**
```typescript
.setExpirationTime('15m') // 15 minutes
```

### Refresh Token: 1-7 Days with Rotation

**Reasoning:**
- Long enough to avoid re-login annoyance
- Short enough to limit exposure
- Rotation prevents replay attacks

**Implementation:**
```typescript
.setExpirationTime('7d') // 7 days
```

**Rotation Pattern:**
1. Client sends refresh token
2. Server validates refresh token
3. Server issues NEW access token + NEW refresh token
4. Server invalidates OLD refresh token
5. Client stores new refresh token

### ID Token: Same as Access Token

ID tokens (OIDC) verify user identity, not API access. Use same lifetime as access token.

## Required Claims

### Standard Claims

| Claim | Name | Required | Example |
|-------|------|----------|---------|
| `iss` | Issuer | Yes | `https://auth.example.com` |
| `sub` | Subject | Yes | `user-123` |
| `aud` | Audience | Yes | `api.example.com` |
| `exp` | Expiration | Yes | `1735689600` (Unix timestamp) |
| `iat` | Issued At | Yes | `1735686000` (Unix timestamp) |
| `jti` | JWT ID | Recommended | `abc123` (unique ID for revocation) |

### Custom Claims

```json
{
  "scope": "read:profile write:data",
  "role": "admin",
  "tenant_id": "org-456",
  "permissions": ["users:create", "posts:delete"]
}
```

**Avoid:** Sensitive data (passwords, credit cards, SSNs). Tokens are base64-encoded, not encrypted.

## Token Storage

### Access Token: Memory Only

```typescript
// Store in React state or module variable
let accessToken: string | null = null

export function setAccessToken(token: string) {
  accessToken = token
}

export function getAccessToken() {
  return accessToken
}
```

**Why:**
- XSS can't steal from memory if token is cleared on page reload
- Forces refresh on page load (good for short-lived tokens)

**Never:**
- localStorage (persists across tabs, vulnerable to XSS)
- sessionStorage (still vulnerable to XSS)
- Cookies without HttpOnly flag

### Refresh Token: HTTP-Only Cookie

```typescript
// Set cookie (server-side)
response.cookies.set('refresh_token', refreshToken, {
  httpOnly: true,      // Not accessible via JavaScript
  secure: true,        // HTTPS only
  sameSite: 'strict',  // CSRF protection
  maxAge: 7 * 24 * 60 * 60, // 7 days
  path: '/api/auth/refresh', // Only sent to refresh endpoint
})
```

**Why:**
- HttpOnly prevents XSS theft
- SameSite=Strict prevents CSRF
- Secure flag requires HTTPS
- Path restriction limits exposure

### CSRF Token: Separate Cookie

For additional CSRF protection with refresh tokens:

```typescript
// Set CSRF token (non-HttpOnly)
response.cookies.set('csrf_token', csrfToken, {
  httpOnly: false,     // Accessible via JavaScript
  secure: true,
  sameSite: 'strict',
  maxAge: 7 * 24 * 60 * 60,
})

// Client sends CSRF token in header
fetch('/api/auth/refresh', {
  headers: {
    'X-CSRF-Token': getCookie('csrf_token'),
  },
  credentials: 'include', // Send cookies
})

// Server validates
if (request.headers.get('X-CSRF-Token') !== request.cookies.get('csrf_token')) {
  throw new Error('CSRF token mismatch')
}
```

## Token Validation

### Validation Checklist

```typescript
const { payload } = await jwtVerify(token, publicKey, {
  // 1. Check algorithm
  algorithms: ['EdDSA'], // Never allow "none"

  // 2. Check issuer
  issuer: 'https://auth.example.com',

  // 3. Check audience
  audience: 'api.example.com',

  // 4. Check expiration (automatic)
  // Fails if current time > exp

  // 5. Clock skew tolerance (optional)
  clockTolerance: 60, // 60 seconds
})

// 6. Check custom claims
if (payload.role !== 'admin') {
  throw new Error('Insufficient permissions')
}

// 7. Check revocation (if using jti)
const isRevoked = await redis.get(`revoked:${payload.jti}`)
if (isRevoked) {
  throw new Error('Token revoked')
}
```

### Express Middleware Example

```typescript
import { Request, Response, NextFunction } from 'express'
import { jwtVerify } from 'jose'

export async function authenticateToken(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const authHeader = req.headers.authorization
  const token = authHeader?.split(' ')[1] // "Bearer TOKEN"

  if (!token) {
    return res.status(401).json({ error: 'No token provided' })
  }

  try {
    const { payload } = await jwtVerify(token, publicKey, {
      algorithms: ['EdDSA'],
      issuer: 'https://auth.example.com',
      audience: 'api.example.com',
    })

    req.user = payload // Attach to request
    next()
  } catch (error) {
    return res.status(403).json({ error: 'Invalid token' })
  }
}

// Usage
app.get('/api/protected', authenticateToken, (req, res) => {
  res.json({ user: req.user })
})
```

## Key Generation

Use `scripts/generate_jwt_keys.py` to generate keys:

```bash
# EdDSA (Recommended)
python scripts/generate_jwt_keys.py --algorithm EdDSA

# ES256
python scripts/generate_jwt_keys.py --algorithm ES256

# RS256 (legacy)
python scripts/generate_jwt_keys.py --algorithm RS256
```

Output:
```
private_key.pem  # Keep secure, never commit to git
public_key.pem   # Can be shared, used for verification
```

### Key Storage

**Development:**
- Store in `.env` file (add to `.gitignore`)
- Use multiline strings or file paths

**Production:**
- AWS Secrets Manager
- Google Secret Manager
- HashiCorp Vault
- Environment variables (encrypted at rest)

**Never:**
- Hardcode in source code
- Commit to version control
- Share via insecure channels

## Token Refresh Flow

### Client-Side (TypeScript)

```typescript
let accessToken: string | null = null

async function refreshAccessToken() {
  const response = await fetch('/api/auth/refresh', {
    method: 'POST',
    credentials: 'include', // Send refresh token cookie
    headers: {
      'X-CSRF-Token': getCookie('csrf_token'),
    },
  })

  if (!response.ok) {
    // Refresh token expired or invalid
    window.location.href = '/login'
    return null
  }

  const { access_token } = await response.json()
  accessToken = access_token
  return access_token
}

async function fetchWithAuth(url: string, options: RequestInit = {}) {
  // Try request with current access token
  let response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      Authorization: `Bearer ${accessToken}`,
    },
  })

  // If 401, refresh and retry once
  if (response.status === 401) {
    const newAccessToken = await refreshAccessToken()
    if (!newAccessToken) return response

    response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${newAccessToken}`,
      },
    })
  }

  return response
}
```

### Server-Side (Next.js API Route)

```typescript
// app/api/auth/refresh/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { jwtVerify, SignJWT } from 'jose'

export async function POST(request: NextRequest) {
  const refreshToken = request.cookies.get('refresh_token')?.value
  const csrfToken = request.headers.get('X-CSRF-Token')

  // Validate CSRF token
  if (csrfToken !== request.cookies.get('csrf_token')?.value) {
    return NextResponse.json({ error: 'CSRF token mismatch' }, { status: 403 })
  }

  if (!refreshToken) {
    return NextResponse.json({ error: 'No refresh token' }, { status: 401 })
  }

  try {
    // Verify refresh token
    const { payload } = await jwtVerify(refreshToken, publicKey, {
      algorithms: ['EdDSA'],
      issuer: 'https://auth.example.com',
      audience: 'api.example.com',
    })

    // Generate new access token
    const newAccessToken = await new SignJWT({
      userId: payload.sub,
      role: payload.role,
    })
      .setProtectedHeader({ alg: 'EdDSA' })
      .setIssuedAt()
      .setIssuer('https://auth.example.com')
      .setAudience('api.example.com')
      .setExpirationTime('15m')
      .sign(privateKey)

    // Generate new refresh token (rotation)
    const newRefreshToken = await new SignJWT({
      userId: payload.sub,
      role: payload.role,
    })
      .setProtectedHeader({ alg: 'EdDSA' })
      .setIssuedAt()
      .setIssuer('https://auth.example.com')
      .setAudience('api.example.com')
      .setExpirationTime('7d')
      .sign(privateKey)

    // Set new refresh token cookie
    const response = NextResponse.json({ access_token: newAccessToken })
    response.cookies.set('refresh_token', newRefreshToken, {
      httpOnly: true,
      secure: true,
      sameSite: 'strict',
      maxAge: 7 * 24 * 60 * 60,
      path: '/api/auth/refresh',
    })

    // Revoke old refresh token (if using jti)
    if (payload.jti) {
      await redis.set(`revoked:${payload.jti}`, '1', {
        ex: 7 * 24 * 60 * 60, // Expire after original token lifetime
      })
    }

    return response
  } catch (error) {
    return NextResponse.json({ error: 'Invalid refresh token' }, { status: 403 })
  }
}
```

## Token Revocation

### Using jti (JWT ID)

Add unique `jti` claim to enable revocation:

```typescript
const token = await new SignJWT({ userId: '123' })
  .setProtectedHeader({ alg: 'EdDSA' })
  .setJti(randomUUID()) // Unique ID
  .setExpirationTime('15m')
  .sign(privateKey)
```

### Revocation Check (Redis)

```typescript
async function isTokenRevoked(jti: string): Promise<boolean> {
  const revoked = await redis.get(`revoked:${jti}`)
  return revoked === '1'
}

// Revoke token
async function revokeToken(jti: string, exp: number) {
  const ttl = exp - Math.floor(Date.now() / 1000)
  await redis.set(`revoked:${jti}`, '1', { ex: ttl })
}
```

### Logout Flow

```typescript
// Server-side logout
export async function POST(request: NextRequest) {
  const accessToken = request.headers.get('Authorization')?.split(' ')[1]
  const refreshToken = request.cookies.get('refresh_token')?.value

  if (accessToken) {
    const { payload } = await jwtVerify(accessToken, publicKey)
    if (payload.jti) {
      await revokeToken(payload.jti, payload.exp!)
    }
  }

  if (refreshToken) {
    const { payload } = await jwtVerify(refreshToken, publicKey)
    if (payload.jti) {
      await revokeToken(payload.jti, payload.exp!)
    }
  }

  const response = NextResponse.json({ success: true })
  response.cookies.delete('refresh_token')
  response.cookies.delete('csrf_token')
  return response
}
```

## Common Attacks and Mitigations

### Algorithm Confusion Attack

**Attack:** Change `alg` header to `none` or `HS256` when expecting `RS256`.

**Mitigation:**
```typescript
// Explicitly specify allowed algorithms
const { payload } = await jwtVerify(token, publicKey, {
  algorithms: ['EdDSA'], // Never allow "none"
})
```

### Token Replay Attack

**Attack:** Reuse stolen token before expiration.

**Mitigation:**
- Short access token lifetime (5-15 min)
- Refresh token rotation
- Token revocation via `jti`

### XSS Token Theft

**Attack:** JavaScript steals token from localStorage.

**Mitigation:**
- Store access token in memory only
- Store refresh token in HttpOnly cookie
- Implement Content Security Policy (CSP)

### CSRF Attack on Refresh Endpoint

**Attack:** Malicious site triggers refresh endpoint.

**Mitigation:**
- Use SameSite=Strict cookies
- Require CSRF token in header
- Validate Origin/Referer headers

## Performance Optimization

### Token Size

- EdDSA: ~200 bytes (smallest)
- ES256: ~250 bytes
- RS256: ~400 bytes (largest)

**Optimization:**
- Use EdDSA for smallest tokens
- Minimize custom claims
- Use claim abbreviations (`uid` instead of `userId`)

### Verification Caching

Cache public keys for signature verification:

```typescript
const keyCache = new Map<string, CryptoKey>()

async function getPublicKey(kid: string): Promise<CryptoKey> {
  if (keyCache.has(kid)) {
    return keyCache.get(kid)!
  }

  const key = await fetchPublicKey(kid)
  keyCache.set(kid, key)
  return key
}
```

## Testing JWTs

### Manual Verification

Use [jwt.io](https://jwt.io) debugger (paste token, verify signature).

### Unit Tests

```typescript
import { expect, test } from 'vitest'

test('generates valid JWT', async () => {
  const token = await generateAccessToken({ userId: '123' })
  const { payload } = await jwtVerify(token, publicKey)

  expect(payload.sub).toBe('123')
  expect(payload.iss).toBe('https://auth.example.com')
  expect(payload.exp).toBeGreaterThan(Date.now() / 1000)
})

test('rejects expired JWT', async () => {
  const expiredToken = await new SignJWT({ userId: '123' })
    .setProtectedHeader({ alg: 'EdDSA' })
    .setExpirationTime('-1m') // 1 minute ago
    .sign(privateKey)

  await expect(jwtVerify(expiredToken, publicKey)).rejects.toThrow()
})
```
