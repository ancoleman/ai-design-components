# API Authentication and Authorization

Security design patterns for OAuth 2.0, API keys, and scope-based authorization.


## Table of Contents

- [OAuth 2.0 Flows](#oauth-20-flows)
  - [Authorization Code Flow (Web Applications)](#authorization-code-flow-web-applications)
  - [Client Credentials Flow (Service-to-Service)](#client-credentials-flow-service-to-service)
  - [Refresh Token Flow](#refresh-token-flow)
- [API Key Management](#api-key-management)
  - [API Key Patterns](#api-key-patterns)
  - [API Key Format](#api-key-format)
  - [API Key Storage](#api-key-storage)
  - [API Key Best Practices](#api-key-best-practices)
- [Scope-Based Authorization](#scope-based-authorization)
  - [Defining Scopes](#defining-scopes)
  - [Scope Hierarchy](#scope-hierarchy)
  - [Authorization Check](#authorization-check)
- [CORS Configuration](#cors-configuration)
  - [Development (Permissive)](#development-permissive)
  - [Production (Restrictive)](#production-restrictive)
  - [Implementation](#implementation)
- [Security Headers](#security-headers)
  - [Essential Headers](#essential-headers)
  - [Implementation](#implementation)
- [Best Practices Checklist](#best-practices-checklist)
  - [OAuth 2.0](#oauth-20)
  - [API Keys](#api-keys)
  - [Authorization](#authorization)
  - [Security](#security)

## OAuth 2.0 Flows

### Authorization Code Flow (Web Applications)

**Use Case:** Web applications with server-side backend

**Flow:**
1. User clicks "Login" → Redirect to authorization server
2. User authenticates and grants permission
3. Authorization server redirects with authorization code
4. Backend exchanges code for access token (with client secret)
5. Backend uses access token to call API

**Example:**

```http
# Step 1: Authorization Request
GET https://auth.example.com/oauth/authorize?
  response_type=code&
  client_id=abc123&
  redirect_uri=https://myapp.com/callback&
  scope=read:users write:users&
  state=random_state_string

# Step 2: Authorization Response (redirect)
GET https://myapp.com/callback?
  code=auth_code_xyz&
  state=random_state_string

# Step 3: Token Request
POST https://auth.example.com/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
code=auth_code_xyz&
client_id=abc123&
client_secret=secret456&
redirect_uri=https://myapp.com/callback

# Step 4: Token Response
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "refresh_token_abc",
  "scope": "read:users write:users"
}

# Step 5: API Request
GET https://api.example.com/v1/users
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Client Credentials Flow (Service-to-Service)

**Use Case:** Backend services, cron jobs, automated processes

**Flow:**
1. Service authenticates with client ID and secret
2. Receives access token
3. Uses token for API requests

**Example:**

```http
# Token Request
POST https://auth.example.com/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&
client_id=service_abc123&
client_secret=service_secret456&
scope=read:orders write:orders

# Token Response
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "read:orders write:orders"
}

# API Request
GET https://api.example.com/v1/orders
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Refresh Token Flow

Refresh expired access tokens without re-authentication:

```http
POST https://auth.example.com/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&
refresh_token=refresh_token_abc&
client_id=abc123&
client_secret=secret456

# Response
{
  "access_token": "new_access_token...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "new_refresh_token_abc"
}
```

## API Key Management

### API Key Patterns

**Header-Based (Recommended):**
```http
GET /api/v1/users
X-API-Key: sk_live_abc123xyz456
```

**Bearer Token:**
```http
GET /api/v1/users
Authorization: Bearer sk_live_abc123xyz456
```

**Query Parameter (NOT Recommended):**
```http
GET /api/v1/users?api_key=sk_live_abc123xyz456
```

Reason: Query params appear in logs, browser history, referrer headers

### API Key Format

Use prefixed keys for identification:
```
sk_live_abc123xyz456789     (live/production)
sk_test_xyz789abc123456     (test/sandbox)
pk_live_public123456789     (public/client-side)
```

Prefix meanings:
- `sk_` - Secret key (server-side only)
- `pk_` - Public key (client-side safe)
- `live_` - Production environment
- `test_` - Test/sandbox environment

### API Key Storage

**Never store plaintext keys:**

```javascript
// Generate key
const apiKey = generateSecureKey(); // sk_live_abc123...

// Hash for storage
const hashedKey = await bcrypt.hash(apiKey, 10);

// Store in database
await db.apiKeys.create({
  userId: user.id,
  keyHash: hashedKey,
  prefix: apiKey.substring(0, 12), // For identification
  createdAt: new Date(),
  lastUsedAt: null
});

// Return to user ONCE
return { apiKey }; // User must save this
```

**Verification:**

```javascript
// Find key by prefix
const keyRecord = await db.apiKeys.findByPrefix(key.substring(0, 12));

// Verify hash
const valid = await bcrypt.compare(key, keyRecord.keyHash);

if (valid) {
  await db.apiKeys.update(keyRecord.id, { lastUsedAt: new Date() });
  return keyRecord;
}
```

### API Key Best Practices

- [ ] Use prefixes for environment identification
- [ ] Store hashed keys only
- [ ] Support multiple keys per user
- [ ] Track last-used timestamp
- [ ] Allow key rotation without downtime
- [ ] Implement key expiration
- [ ] Log key usage for security audit

## Scope-Based Authorization

### Defining Scopes

Granular permissions using resource:action pattern:

```
read:users      - Read user data
write:users     - Create/update users
delete:users    - Delete users
admin:users     - Full user management

read:posts
write:posts
delete:posts

admin:*         - Full admin access
```

### Scope Hierarchy

```
admin:users  includes  write:users, read:users
write:users  includes  read:users
```

### Authorization Check

```javascript
function requireScope(requiredScope) {
  return (req, res, next) => {
    const userScopes = req.user.scopes; // From JWT or session

    // Check if user has required scope
    if (!hasScope(userScopes, requiredScope)) {
      return res.status(403).json({
        type: 'https://api.example.com/errors/forbidden',
        title: 'Insufficient Permissions',
        status: 403,
        detail: `This operation requires the '${requiredScope}' scope`,
        requiredScope: requiredScope,
        currentScopes: userScopes
      });
    }

    next();
  };
}

// Helper function
function hasScope(userScopes, requiredScope) {
  // Check for exact match
  if (userScopes.includes(requiredScope)) {
    return true;
  }

  // Check for admin wildcard
  if (userScopes.includes('admin:*')) {
    return true;
  }

  // Check for resource admin (e.g., admin:users includes write:users)
  const [resource] = requiredScope.split(':');
  if (userScopes.includes(`admin:${resource}`)) {
    return true;
  }

  return false;
}

// Apply to routes
router.get('/users', requireScope('read:users'), getUsers);
router.post('/users', requireScope('write:users'), createUser);
router.delete('/users/:id', requireScope('delete:users'), deleteUser);
```

## CORS Configuration

### Development (Permissive)

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization, X-API-Key
```

### Production (Restrictive)

```http
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 86400
```

### Implementation

```javascript
app.use((req, res, next) => {
  const allowedOrigins = [
    'https://app.example.com',
    'https://www.example.com'
  ];

  const origin = req.headers.origin;
  if (allowedOrigins.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
  }

  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.setHeader('Access-Control-Allow-Credentials', 'true');

  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  next();
});
```

## Security Headers

### Essential Headers

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
```

### Implementation

```javascript
app.use((req, res, next) => {
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  next();
});
```

## Best Practices Checklist

### OAuth 2.0
- [ ] Use authorization code flow for web apps
- [ ] Use client credentials for service-to-service
- [ ] Store client secrets securely
- [ ] Implement token refresh
- [ ] Use PKCE for mobile/SPA
- [ ] Validate redirect URIs
- [ ] Use state parameter to prevent CSRF

### API Keys
- [ ] Use header-based keys (not query params)
- [ ] Store hashed keys only
- [ ] Use prefixes for identification
- [ ] Support key rotation
- [ ] Track last-used timestamps
- [ ] Implement key expiration
- [ ] Allow multiple keys per user

### Authorization
- [ ] Use scope-based permissions
- [ ] Implement principle of least privilege
- [ ] Check scopes on every request
- [ ] Return clear 403 errors
- [ ] Document required scopes per endpoint

### Security
- [ ] Use HTTPS everywhere
- [ ] Implement CORS correctly
- [ ] Set security headers
- [ ] Rate limit authentication attempts
- [ ] Log authentication events
- [ ] Monitor for suspicious activity
