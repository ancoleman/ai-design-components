# API Security Best Practices

Comprehensive guide to securing REST, GraphQL, and gRPC APIs in production environments.


## Table of Contents

- [Core Security Principles](#core-security-principles)
- [Authentication Patterns](#authentication-patterns)
  - [JWT (JSON Web Tokens)](#jwt-json-web-tokens)
  - [API Keys](#api-keys)
  - [OAuth 2.1 Client Credentials Flow](#oauth-21-client-credentials-flow)
- [Rate Limiting](#rate-limiting)
  - [Strategy 1: Fixed Window](#strategy-1-fixed-window)
  - [Strategy 2: Sliding Window (Recommended)](#strategy-2-sliding-window-recommended)
  - [Strategy 3: Token Bucket (Advanced)](#strategy-3-token-bucket-advanced)
  - [Tiered Rate Limiting](#tiered-rate-limiting)
- [Input Validation](#input-validation)
  - [Request Validation (TypeScript + Zod)](#request-validation-typescript-zod)
  - [SQL Injection Prevention](#sql-injection-prevention)
  - [XSS Prevention](#xss-prevention)
- [CORS Configuration](#cors-configuration)
  - [Restrictive CORS (Recommended)](#restrictive-cors-recommended)
- [Security Headers](#security-headers)
  - [Helmet.js Configuration (Express/Node.js)](#helmetjs-configuration-expressnodejs)
  - [FastAPI Security Headers](#fastapi-security-headers)
- [GraphQL Security](#graphql-security)
  - [Query Depth Limiting](#query-depth-limiting)
  - [Query Complexity Analysis](#query-complexity-analysis)
  - [Disable Introspection in Production](#disable-introspection-in-production)
- [File Upload Security](#file-upload-security)
  - [Validation and Sanitization](#validation-and-sanitization)
- [API Versioning](#api-versioning)
  - [URI Versioning (Simple)](#uri-versioning-simple)
  - [Header Versioning (REST Best Practice)](#header-versioning-rest-best-practice)
- [Logging and Monitoring](#logging-and-monitoring)
  - [Security Event Logging](#security-event-logging)
  - [Sensitive Data Redaction](#sensitive-data-redaction)
- [Secrets Management](#secrets-management)
  - [Environment Variables (Basic)](#environment-variables-basic)
  - [HashiCorp Vault (Production)](#hashicorp-vault-production)
- [Security Checklist](#security-checklist)
  - [Pre-Deployment](#pre-deployment)
  - [Ongoing](#ongoing)
- [Common Vulnerabilities](#common-vulnerabilities)
  - [Mass Assignment](#mass-assignment)
  - [Insecure Direct Object References (IDOR)](#insecure-direct-object-references-idor)
  - [Timing Attacks](#timing-attacks)
- [Resources](#resources)

## Core Security Principles

1. **Defense in Depth** - Multiple layers of security
2. **Least Privilege** - Grant minimum required permissions
3. **Fail Securely** - Default to deny on errors
4. **Don't Trust Input** - Validate and sanitize everything
5. **Keep Security Simple** - Complex systems have more vulnerabilities

---

## Authentication Patterns

### JWT (JSON Web Tokens)

**Best practices:**
- Use EdDSA (Ed25519) or ES256 for signing (avoid RS256 unless required)
- Set short expiration times (5-15 minutes for access tokens)
- Implement refresh token rotation
- Include `aud` (audience) claim for token binding
- Validate all claims on every request

**Secure JWT validation:**
```typescript
import { jwtVerify, importSPKI } from 'jose';

const publicKey = await importSPKI(process.env.JWT_PUBLIC_KEY, 'EdDSA');

export async function verifyToken(token: string) {
  try {
    const { payload } = await jwtVerify(token, publicKey, {
      issuer: 'https://auth.example.com',
      audience: 'api.example.com',
      algorithms: ['EdDSA'],
      maxTokenAge: '15m',  // Reject tokens older than 15 minutes
    });

    // Check for revocation (Redis/database check)
    const isRevoked = await checkTokenRevocation(payload.jti);
    if (isRevoked) throw new Error('Token revoked');

    return payload;
  } catch (error) {
    throw new UnauthorizedError('Invalid token');
  }
}
```

**Python (FastAPI):**
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from joserfc import jwt
from joserfc.jwk import RSAKey

security = HTTPBearer()

public_key = RSAKey.import_key(open('public_key.pem').read())

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            public_key,
            claims_options={
                "iss": {"essential": True, "value": "https://auth.example.com"},
                "aud": {"essential": True, "value": "api.example.com"},
                "exp": {"essential": True},
            }
        )
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### API Keys

**When to use:**
- Server-to-server communication
- Third-party integrations
- Long-lived tokens for automation

**Implementation:**
```typescript
// Hashed storage (never store plain-text API keys)
import crypto from 'crypto';

function hashApiKey(apiKey: string): string {
  return crypto.createHash('sha256').update(apiKey).digest('hex');
}

// Generate API key
function generateApiKey(): { key: string; hash: string } {
  const key = `sk_${crypto.randomBytes(32).toString('hex')}`;
  const hash = hashApiKey(key);
  return { key, hash };  // Store hash in database, return key once to user
}

// Validate API key
async function validateApiKey(providedKey: string): Promise<boolean> {
  const hash = hashApiKey(providedKey);
  const storedApiKey = await db.apiKeys.findOne({ hash });

  if (!storedApiKey) return false;
  if (storedApiKey.revokedAt) return false;
  if (storedApiKey.expiresAt && storedApiKey.expiresAt < new Date()) return false;

  // Update last_used_at
  await db.apiKeys.update({ hash }, { lastUsedAt: new Date() });

  return true;
}
```

### OAuth 2.1 Client Credentials Flow

**For machine-to-machine (M2M) authentication:**
```typescript
async function getAccessToken() {
  const response = await fetch('https://auth.example.com/oauth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'client_credentials',
      client_id: process.env.CLIENT_ID,
      client_secret: process.env.CLIENT_SECRET,
      scope: 'read:data write:data',
    }),
  });

  const { access_token, expires_in } = await response.json();

  // Cache token until expiration
  cache.set('m2m_token', access_token, expires_in - 60);

  return access_token;
}
```

---

## Rate Limiting

### Strategy 1: Fixed Window

**Simple but has boundary issues (burst at window reset).**

```typescript
import Redis from 'ioredis';

const redis = new Redis();

async function fixedWindowRateLimit(userId: string, limit: number, windowSeconds: number): Promise<boolean> {
  const key = `rate:${userId}:${Math.floor(Date.now() / 1000 / windowSeconds)}`;
  const count = await redis.incr(key);

  if (count === 1) {
    await redis.expire(key, windowSeconds);
  }

  return count <= limit;
}

// Usage: Allow 100 requests per 60 seconds
const allowed = await fixedWindowRateLimit('user_123', 100, 60);
if (!allowed) {
  throw new Error('Rate limit exceeded');
}
```

### Strategy 2: Sliding Window (Recommended)

**More accurate, prevents burst attacks.**

```typescript
async function slidingWindowRateLimit(userId: string, limit: number, windowSeconds: number): Promise<boolean> {
  const now = Date.now();
  const windowStart = now - windowSeconds * 1000;
  const key = `rate:${userId}`;

  // Remove old entries
  await redis.zremrangebyscore(key, 0, windowStart);

  // Count requests in window
  const count = await redis.zcard(key);

  if (count >= limit) {
    return false;
  }

  // Add current request
  await redis.zadd(key, now, `${now}`);
  await redis.expire(key, windowSeconds);

  return true;
}
```

### Strategy 3: Token Bucket (Advanced)

**Allows bursts while maintaining average rate.**

```typescript
async function tokenBucketRateLimit(userId: string, capacity: number, refillRate: number): Promise<boolean> {
  const key = `bucket:${userId}`;
  const now = Date.now();

  const bucket = await redis.hgetall(key);

  let tokens = parseFloat(bucket.tokens) || capacity;
  let lastRefill = parseInt(bucket.lastRefill) || now;

  // Refill tokens based on time elapsed
  const elapsed = (now - lastRefill) / 1000;
  tokens = Math.min(capacity, tokens + elapsed * refillRate);

  if (tokens < 1) {
    await redis.hset(key, { tokens: tokens.toString(), lastRefill: now.toString() });
    await redis.expire(key, 3600);
    return false;
  }

  // Consume one token
  tokens -= 1;
  await redis.hset(key, { tokens: tokens.toString(), lastRefill: now.toString() });
  await redis.expire(key, 3600);

  return true;
}

// Usage: 10 token capacity, refill 1 token/second
const allowed = await tokenBucketRateLimit('user_123', 10, 1);
```

### Tiered Rate Limiting

**Different limits for different user types:**

```typescript
const RATE_LIMITS = {
  anonymous: { limit: 10, window: 60 },      // 10 req/min
  authenticated: { limit: 100, window: 60 }, // 100 req/min
  premium: { limit: 1000, window: 60 },      // 1000 req/min
  internal: { limit: 10000, window: 60 },    // 10K req/min (internal services)
};

async function getRateLimit(user: User | null): Promise<{ limit: number; window: number }> {
  if (!user) return RATE_LIMITS.anonymous;
  if (user.tier === 'premium') return RATE_LIMITS.premium;
  if (user.isInternal) return RATE_LIMITS.internal;
  return RATE_LIMITS.authenticated;
}
```

---

## Input Validation

### Request Validation (TypeScript + Zod)

```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100),
  age: z.number().int().min(18).max(120),
  role: z.enum(['user', 'admin']).default('user'),
  metadata: z.record(z.string()).optional(),
});

type CreateUserInput = z.infer<typeof CreateUserSchema>;

app.post('/users', async (req, res) => {
  try {
    const validatedData = CreateUserSchema.parse(req.body);
    // Safe to use validatedData
    const user = await createUser(validatedData);
    res.json(user);
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ errors: error.errors });
    }
    throw error;
  }
});
```

### SQL Injection Prevention

**Always use parameterized queries:**

```typescript
// ✅ SAFE (parameterized)
const user = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
);

// ❌ UNSAFE (string concatenation)
const user = await db.query(
  `SELECT * FROM users WHERE email = '${email}'`
);
```

### XSS Prevention

```typescript
import DOMPurify from 'isomorphic-dompurify';

// Sanitize user input before storing
function sanitizeHtml(html: string): string {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
    ALLOWED_ATTR: ['href'],
  });
}

// Always escape output
function escapeHtml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
}
```

---

## CORS Configuration

### Restrictive CORS (Recommended)

```typescript
const corsOptions = {
  origin: (origin, callback) => {
    const allowedOrigins = [
      'https://app.example.com',
      'https://admin.example.com',
    ];

    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,  // Allow cookies
  maxAge: 86400,  // Cache preflight for 24 hours
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Request-ID'],
  exposedHeaders: ['X-Total-Count', 'X-Page-Count'],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
};

app.use(cors(corsOptions));
```

**NEVER use:**
```typescript
// ❌ DANGEROUS (allows all origins with credentials)
app.use(cors({
  origin: '*',
  credentials: true,  // This combination is a security vulnerability
}));
```

---

## Security Headers

### Helmet.js Configuration (Express/Node.js)

```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],  // Avoid 'unsafe-inline' in production
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", 'data:', 'https:'],
      connectSrc: ["'self'", 'https://api.example.com'],
      fontSrc: ["'self'", 'https:', 'data:'],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"],
    },
  },
  hsts: {
    maxAge: 31536000,  // 1 year
    includeSubDomains: true,
    preload: true,
  },
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
  permissionsPolicy: {
    features: {
      geolocation: ["'none'"],
      microphone: ["'none'"],
      camera: ["'none'"],
      payment: ["'none'"],
    },
  },
}));
```

### FastAPI Security Headers

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"]
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response
```

---

## GraphQL Security

### Query Depth Limiting

```typescript
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(7)],  // Max 7 levels deep
});
```

### Query Complexity Analysis

```typescript
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const complexityLimit = createComplexityLimitRule(1000, {
  onCost: (cost) => console.log('Query cost:', cost),
  formatErrorMessage: (cost) => `Query too complex: ${cost} (max 1000)`,
});

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [complexityLimit],
});
```

### Disable Introspection in Production

```typescript
import { ApolloServerPluginLandingPageDisabled } from '@apollo/server/plugin/disabled';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production',
  plugins: [
    process.env.NODE_ENV === 'production'
      ? ApolloServerPluginLandingPageDisabled()
      : ApolloServerPluginLandingPageLocalDefault(),
  ],
});
```

---

## File Upload Security

### Validation and Sanitization

```typescript
import multer from 'multer';
import path from 'path';
import crypto from 'crypto';

const ALLOWED_MIME_TYPES = [
  'image/jpeg',
  'image/png',
  'image/webp',
  'application/pdf',
];

const MAX_FILE_SIZE = 10 * 1024 * 1024;  // 10MB

const storage = multer.diskStorage({
  destination: '/tmp/uploads',
  filename: (req, file, cb) => {
    // Generate random filename (prevent directory traversal)
    const randomName = crypto.randomBytes(16).toString('hex');
    const ext = path.extname(file.originalname);
    cb(null, `${randomName}${ext}`);
  },
});

const upload = multer({
  storage,
  limits: { fileSize: MAX_FILE_SIZE },
  fileFilter: (req, file, cb) => {
    if (!ALLOWED_MIME_TYPES.includes(file.mimetype)) {
      return cb(new Error('Invalid file type'));
    }
    cb(null, true);
  },
});

app.post('/upload', upload.single('file'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  // Verify MIME type (don't trust client-provided MIME type)
  const { fileTypeFromFile } = await import('file-type');
  const type = await fileTypeFromFile(req.file.path);

  if (!type || !ALLOWED_MIME_TYPES.includes(type.mime)) {
    fs.unlinkSync(req.file.path);  // Delete invalid file
    return res.status(400).json({ error: 'Invalid file content' });
  }

  // Process file...
  res.json({ filename: req.file.filename });
});
```

---

## API Versioning

### URI Versioning (Simple)

```typescript
app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);
```

### Header Versioning (REST Best Practice)

```typescript
app.use((req, res, next) => {
  const version = req.headers['api-version'] || '1';
  req.apiVersion = version;
  next();
});

app.get('/users', (req, res) => {
  if (req.apiVersion === '2') {
    return getUsersV2(req, res);
  }
  return getUsersV1(req, res);
});
```

---

## Logging and Monitoring

### Security Event Logging

```typescript
enum SecurityEvent {
  LOGIN_SUCCESS = 'login_success',
  LOGIN_FAILED = 'login_failed',
  RATE_LIMIT_EXCEEDED = 'rate_limit_exceeded',
  INVALID_TOKEN = 'invalid_token',
  PERMISSION_DENIED = 'permission_denied',
}

function logSecurityEvent(event: SecurityEvent, metadata: Record<string, any>) {
  logger.warn({
    type: 'security_event',
    event,
    timestamp: new Date().toISOString(),
    ip: metadata.ip,
    userId: metadata.userId,
    endpoint: metadata.endpoint,
    userAgent: metadata.userAgent,
  });

  // Send to security monitoring (Datadog, Sentry, etc.)
  if ([SecurityEvent.LOGIN_FAILED, SecurityEvent.RATE_LIMIT_EXCEEDED].includes(event)) {
    alertSecurityTeam(event, metadata);
  }
}
```

### Sensitive Data Redaction

```typescript
function redactSensitiveData(obj: any): any {
  const sensitiveKeys = ['password', 'ssn', 'creditCard', 'apiKey', 'secret'];

  return JSON.parse(JSON.stringify(obj, (key, value) => {
    if (sensitiveKeys.includes(key)) {
      return '[REDACTED]';
    }
    return value;
  }));
}

logger.info('User created', redactSensitiveData(userData));
```

---

## Secrets Management

### Environment Variables (Basic)

```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost/db
JWT_SECRET=...
API_KEY=...
```

```typescript
import dotenv from 'dotenv';

dotenv.config();

if (!process.env.JWT_SECRET) {
  throw new Error('JWT_SECRET not configured');
}
```

### HashiCorp Vault (Production)

```typescript
import Vault from 'node-vault';

const vault = Vault({
  endpoint: 'https://vault.example.com',
  token: process.env.VAULT_TOKEN,
});

const { data } = await vault.read('secret/data/api');
const JWT_SECRET = data.data.JWT_SECRET;
```

---

## Security Checklist

### Pre-Deployment

- [ ] All secrets in environment variables/vault (not hardcoded)
- [ ] HTTPS enforced (TLS 1.3+)
- [ ] Security headers configured (HSTS, CSP, etc.)
- [ ] CORS configured restrictively
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (sanitize output)
- [ ] Authentication required on protected endpoints
- [ ] Authorization checks on every request
- [ ] Sensitive data redacted from logs
- [ ] Error messages don't leak information
- [ ] File uploads validated (MIME type, size)
- [ ] API versioning strategy implemented
- [ ] Security logging and monitoring active

### Ongoing

- [ ] Regular dependency updates (npm audit, Snyk)
- [ ] Penetration testing (quarterly)
- [ ] Security headers scan (securityheaders.com)
- [ ] SSL/TLS configuration test (ssllabs.com)
- [ ] Review access logs for anomalies
- [ ] Rotate secrets/API keys (annually)

---

## Common Vulnerabilities

### Mass Assignment

**Problem:** Allowing users to modify restricted fields.

```typescript
// ❌ VULNERABLE
app.put('/users/:id', async (req, res) => {
  await db.users.update(req.params.id, req.body);  // User could set isAdmin: true
});

// ✅ SAFE
const UpdateUserSchema = z.object({
  name: z.string(),
  email: z.string().email(),
  // isAdmin NOT allowed
});

app.put('/users/:id', async (req, res) => {
  const data = UpdateUserSchema.parse(req.body);
  await db.users.update(req.params.id, data);
});
```

### Insecure Direct Object References (IDOR)

**Problem:** Users accessing resources they shouldn't.

```typescript
// ❌ VULNERABLE
app.get('/documents/:id', async (req, res) => {
  const doc = await db.documents.findById(req.params.id);
  res.json(doc);  // No ownership check!
});

// ✅ SAFE
app.get('/documents/:id', requireAuth, async (req, res) => {
  const doc = await db.documents.findById(req.params.id);

  if (!doc) return res.status(404).json({ error: 'Not found' });
  if (doc.userId !== req.user.id) return res.status(403).json({ error: 'Forbidden' });

  res.json(doc);
});
```

### Timing Attacks

**Problem:** Timing differences reveal information.

```typescript
// ❌ VULNERABLE (early return on failure)
if (user.password !== providedPassword) {
  return false;
}

// ✅ SAFE (constant-time comparison)
import crypto from 'crypto';

function safeCompare(a: string, b: string): boolean {
  return crypto.timingSafeEqual(
    Buffer.from(a),
    Buffer.from(b)
  );
}
```

---

## Resources

- OWASP API Security Top 10: https://owasp.org/API-Security/
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- Mozilla Observatory: https://observatory.mozilla.org/
- Security Headers: https://securityheaders.com/
- SSL Labs: https://www.ssllabs.com/ssltest/
