# OAuth 2.1 Implementation Guide

OAuth 2.1 consolidates best practices and security improvements from OAuth 2.0, making PKCE mandatory and removing insecure flows.


## Table of Contents

- [Key Changes from OAuth 2.0](#key-changes-from-oauth-20)
- [PKCE Flow (Authorization Code + PKCE)](#pkce-flow-authorization-code-pkce)
  - [Step 1: Generate Code Verifier and Challenge](#step-1-generate-code-verifier-and-challenge)
  - [Step 2: Authorization Request](#step-2-authorization-request)
  - [Step 3: Handle Callback](#step-3-handle-callback)
  - [Step 4: Token Exchange](#step-4-token-exchange)
  - [Step 5: Store Tokens Securely](#step-5-store-tokens-securely)
- [OAuth 2.1 with Auth.js (Next.js)](#oauth-21-with-authjs-nextjs)
- [OAuth 2.1 with Authlib (Python FastAPI)](#oauth-21-with-authlib-python-fastapi)
- [Redirect URI Validation](#redirect-uri-validation)
  - [Valid Configuration](#valid-configuration)
  - [Authorization Request](#authorization-request)
- [Refresh Token Flow](#refresh-token-flow)
- [Device Flow (Replacement for Password Grant)](#device-flow-replacement-for-password-grant)
  - [Step 1: Device Requests Code](#step-1-device-requests-code)
  - [Step 2: User Enters Code](#step-2-user-enters-code)
  - [Step 3: Device Polls for Token](#step-3-device-polls-for-token)
- [Security Checklist](#security-checklist)
- [Common Errors](#common-errors)
  - [Error: PKCE Required](#error-pkce-required)
  - [Error: Redirect URI Mismatch](#error-redirect-uri-mismatch)
  - [Error: Invalid Code Verifier](#error-invalid-code-verifier)
- [Provider-Specific Notes](#provider-specific-notes)
  - [Google](#google)
  - [GitHub](#github)
  - [Microsoft (Azure AD)](#microsoft-azure-ad)
  - [Auth0](#auth0)
- [Testing OAuth 2.1 Flows](#testing-oauth-21-flows)

## Key Changes from OAuth 2.0

| Feature | OAuth 2.0 | OAuth 2.1 |
|---------|-----------|-----------|
| PKCE | Optional | **MANDATORY** for all clients |
| Implicit Grant | Allowed | **REMOVED** (security risks) |
| Password Grant | Allowed | **REMOVED** (use device flow) |
| Redirect URI Matching | Substring allowed | **EXACT MATCH ONLY** |
| Bearer Token in URL | Allowed | **FORBIDDEN** |

## PKCE Flow (Authorization Code + PKCE)

### Step 1: Generate Code Verifier and Challenge

**TypeScript:**
```typescript
import { randomBytes, createHash } from 'crypto'

// 1. Generate code_verifier (43-128 characters, base64url)
const codeVerifier = randomBytes(32).toString('base64url') // 43 chars

// 2. Generate code_challenge (SHA-256 hash of verifier)
const codeChallenge = createHash('sha256')
  .update(codeVerifier)
  .digest('base64url')

// Store codeVerifier in session/memory for later use
```

**Python:**
```python
import hashlib
import secrets
import base64

# 1. Generate code_verifier
code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')

# 2. Generate code_challenge
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode('utf-8')).digest()
).decode('utf-8').rstrip('=')
```

**Rust:**
```rust
use sha2::{Sha256, Digest};
use base64::{engine::general_purpose::URL_SAFE_NO_PAD, Engine as _};

// 1. Generate code_verifier
let mut rng = rand::thread_rng();
let mut bytes = [0u8; 32];
rng.fill(&mut bytes);
let code_verifier = URL_SAFE_NO_PAD.encode(bytes);

// 2. Generate code_challenge
let mut hasher = Sha256::new();
hasher.update(code_verifier.as_bytes());
let code_challenge = URL_SAFE_NO_PAD.encode(hasher.finalize());
```

### Step 2: Authorization Request

Redirect user to authorization endpoint with PKCE parameters.

```http
GET /oauth/authorize HTTP/1.1
Host: auth.provider.com

client_id=your_client_id
redirect_uri=https://app.example.com/callback  # EXACT match required
response_type=code
scope=openid profile email
state=random_state_value  # CSRF protection
code_challenge=<code_challenge>
code_challenge_method=S256
```

**TypeScript Example:**
```typescript
const authUrl = new URL('https://auth.provider.com/oauth/authorize')
authUrl.searchParams.set('client_id', 'your_client_id')
authUrl.searchParams.set('redirect_uri', 'https://app.example.com/callback')
authUrl.searchParams.set('response_type', 'code')
authUrl.searchParams.set('scope', 'openid profile email')
authUrl.searchParams.set('state', randomBytes(16).toString('hex'))
authUrl.searchParams.set('code_challenge', codeChallenge)
authUrl.searchParams.set('code_challenge_method', 'S256')

// Redirect user
window.location.href = authUrl.toString()
```

### Step 3: Handle Callback

User is redirected back with authorization code.

```http
GET /callback HTTP/1.1
Host: app.example.com

code=authorization_code_here
state=random_state_value
```

**Validate state parameter** to prevent CSRF attacks.

### Step 4: Token Exchange

Exchange authorization code for tokens using code_verifier.

```http
POST /oauth/token HTTP/1.1
Host: auth.provider.com
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
code=authorization_code_here
redirect_uri=https://app.example.com/callback  # MUST match step 2
client_id=your_client_id
code_verifier=<code_verifier>  # PKCE verification
```

**TypeScript Example:**
```typescript
const tokenResponse = await fetch('https://auth.provider.com/oauth/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code: authorizationCode,
    redirect_uri: 'https://app.example.com/callback',
    client_id: 'your_client_id',
    code_verifier: codeVerifier, // From step 1
  }),
})

const tokens = await tokenResponse.json()
// {
//   access_token: "...",
//   refresh_token: "...",
//   id_token: "...",
//   token_type: "Bearer",
//   expires_in: 3600
// }
```

### Step 5: Store Tokens Securely

- **Access token:** Memory only (JavaScript variable)
- **Refresh token:** HTTP-only cookie with SameSite=Strict
- **ID token:** Memory (or discard if not needed)

**Never store in localStorage or sessionStorage** (vulnerable to XSS).

## OAuth 2.1 with Auth.js (Next.js)

Auth.js handles PKCE automatically.

```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      authorization: {
        params: {
          prompt: 'consent',
          access_type: 'offline',
          response_type: 'code', // OAuth 2.1 authorization code flow
        },
      },
    }),
  ],
  session: {
    strategy: 'jwt',
    maxAge: 7 * 24 * 60 * 60, // 7 days
  },
  callbacks: {
    async jwt({ token, account }) {
      if (account) {
        token.accessToken = account.access_token
        token.refreshToken = account.refresh_token
      }
      return token
    },
    async session({ session, token }) {
      session.accessToken = token.accessToken
      return session
    },
  },
})

export const { GET, POST } = handlers
```

## OAuth 2.1 with Authlib (Python FastAPI)

```python
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

config = Config('.env')
oauth = OAuth(config)

oauth.register(
    name='google',
    client_id=config('GOOGLE_CLIENT_ID'),
    client_secret=config('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'code_challenge_method': 'S256',  # PKCE enabled
    },
)

@app.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get('/auth/callback')
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    # token contains: access_token, refresh_token, id_token
    return user
```

## Redirect URI Validation

OAuth 2.1 requires **exact match** for redirect URIs.

### Valid Configuration

```json
{
  "client_id": "app123",
  "redirect_uris": [
    "https://app.example.com/callback",
    "https://app.example.com/auth/callback",
    "http://localhost:3000/callback"
  ]
}
```

### Authorization Request

```
redirect_uri=https://app.example.com/callback  ✅ Exact match
redirect_uri=https://app.example.com/auth      ❌ Not in list
redirect_uri=https://app.example.com/callback?foo=bar  ❌ Query params differ
```

## Refresh Token Flow

When access token expires, use refresh token to get new tokens.

```http
POST /oauth/token HTTP/1.1
Host: auth.provider.com
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token
refresh_token=<refresh_token>
client_id=your_client_id
```

**Response:**
```json
{
  "access_token": "new_access_token",
  "refresh_token": "new_refresh_token",  // Rotated
  "token_type": "Bearer",
  "expires_in": 3600
}
```

**Refresh token rotation:** Old refresh token is invalidated, new one issued.

## Device Flow (Replacement for Password Grant)

For devices without browsers (TVs, IoT), use Device Authorization Grant (RFC 8628).

### Step 1: Device Requests Code

```http
POST /oauth/device/code HTTP/1.1
Host: auth.provider.com

client_id=your_client_id
scope=openid profile
```

**Response:**
```json
{
  "device_code": "device_code_here",
  "user_code": "WDJB-MJHT",  // User enters this
  "verification_uri": "https://auth.provider.com/device",
  "expires_in": 1800,
  "interval": 5  // Poll every 5 seconds
}
```

### Step 2: User Enters Code

Display to user:
```
Go to https://auth.provider.com/device
Enter code: WDJB-MJHT
```

### Step 3: Device Polls for Token

```http
POST /oauth/token HTTP/1.1
Host: auth.provider.com

grant_type=urn:ietf:params:oauth:grant-type:device_code
device_code=device_code_here
client_id=your_client_id
```

Poll every `interval` seconds until user authorizes or code expires.

## Security Checklist

- [ ] PKCE enabled for all flows
- [ ] S256 code challenge method (not plain)
- [ ] Exact redirect URI matching enforced
- [ ] State parameter used for CSRF protection
- [ ] Access tokens short-lived (5-15 minutes)
- [ ] Refresh token rotation implemented
- [ ] Tokens never in URL query parameters
- [ ] TLS 1.2+ for all endpoints
- [ ] No implicit or password grants
- [ ] Redirect URIs validated server-side

## Common Errors

### Error: PKCE Required

```json
{
  "error": "invalid_request",
  "error_description": "PKCE is required for this client"
}
```

**Solution:** Add `code_challenge` and `code_challenge_method=S256` to authorization request.

### Error: Redirect URI Mismatch

```json
{
  "error": "invalid_request",
  "error_description": "redirect_uri does not match"
}
```

**Solution:** Ensure exact match between registered URI and request URI (including protocol, host, path).

### Error: Invalid Code Verifier

```json
{
  "error": "invalid_grant",
  "error_description": "code_verifier does not match code_challenge"
}
```

**Solution:** Ensure `code_verifier` sent in token request matches the one used to generate `code_challenge` in authorization request.

## Provider-Specific Notes

### Google

- PKCE automatically enabled for public clients
- `access_type=offline` required for refresh tokens
- `prompt=consent` required to get refresh token each time

### GitHub

- PKCE support added 2023
- Refresh tokens optional (enable in OAuth app settings)
- Scopes: `read:user`, `user:email`, `repo`

### Microsoft (Azure AD)

- PKCE required for all client types (2024+)
- Use `/.well-known/openid-configuration` for discovery
- Multi-tenant apps: `common` tenant in URL

### Auth0

- PKCE enabled by default for SPAs
- Custom domains supported for branded login
- Universal Login recommended for security

## Testing OAuth 2.1 Flows

Use `scripts/validate_oauth_config.py` to validate OAuth 2.1 compliance:

```bash
python scripts/validate_oauth_config.py --provider google
```

Checks:
- PKCE parameters present
- Redirect URI exact match
- No forbidden grant types
- TLS 1.2+ enforcement
