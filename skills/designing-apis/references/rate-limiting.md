# Rate Limiting Strategies

Guide to rate limiting algorithms, headers, and implementation patterns.


## Table of Contents

- [Token Bucket Algorithm](#token-bucket-algorithm)
  - [Concept](#concept)
  - [Example](#example)
  - [Implementation](#implementation)
- [Rate Limit Headers](#rate-limit-headers)
  - [Standard Headers](#standard-headers)
  - [On Every Response](#on-every-response)
  - [When Limit Exceeded](#when-limit-exceeded)
- [Rate Limiting Strategies](#rate-limiting-strategies)
  - [Per User](#per-user)
  - [Per API Key](#per-api-key)
  - [Per IP Address](#per-ip-address)
  - [Tiered Limits](#tiered-limits)
  - [Endpoint-Specific](#endpoint-specific)
- [Quota Management](#quota-management)
  - [Monthly Quotas](#monthly-quotas)
  - [Quota Headers](#quota-headers)
  - [When Quota Exceeded](#when-quota-exceeded)
- [Implementation Patterns](#implementation-patterns)
  - [Redis-Based Rate Limiting](#redis-based-rate-limiting)
  - [Middleware Example](#middleware-example)
- [Best Practices](#best-practices)
  - [Transparent Limits](#transparent-limits)
  - [Graceful Degradation](#graceful-degradation)
  - [Monitoring](#monitoring)
  - [Checklist](#checklist)

## Token Bucket Algorithm

### Concept

- Each user has a bucket with tokens
- Each request consumes 1 token
- Tokens refill at constant rate
- Empty bucket = reject request

### Example

Bucket capacity: 100 tokens
Refill rate: 100 tokens/hour (1.67 tokens/minute)

Sequence:
1. User makes 50 requests → 50 tokens left
2. Wait 30 minutes → 50 tokens refilled (100 total)
3. User makes 120 requests → 100 succeed, 20 rejected

### Implementation

```javascript
class TokenBucket {
  constructor(capacity, refillRate) {
    this.capacity = capacity;
    this.tokens = capacity;
    this.refillRate = refillRate; // tokens per second
    this.lastRefill = Date.now();
  }

  tryConsume(tokens = 1) {
    this.refill();

    if (this.tokens >= tokens) {
      this.tokens -= tokens;
      return true;
    }
    return false;
  }

  refill() {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;
    const tokensToAdd = elapsed * this.refillRate;

    this.tokens = Math.min(this.capacity, this.tokens + tokensToAdd);
    this.lastRefill = now;
  }

  getReset() {
    const tokensNeeded = this.capacity - this.tokens;
    return Math.ceil(tokensNeeded / this.refillRate);
  }
}

// Usage
const bucket = new TokenBucket(100, 100 / 3600); // 100/hour
if (bucket.tryConsume(1)) {
  // Allow request
} else {
  // Reject with 429
}
```

## Rate Limit Headers

### Standard Headers

```http
X-RateLimit-Limit: 100           # Max requests per window
X-RateLimit-Remaining: 73        # Requests remaining
X-RateLimit-Reset: 1672531200    # Unix timestamp when limit resets
```

### On Every Response

```http
GET /api/v1/users

200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 73
X-RateLimit-Reset: 1672531200
```

### When Limit Exceeded

```http
GET /api/v1/users

429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1672531200
Retry-After: 3600

{
  "type": "https://api.example.com/errors/rate-limit",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "You have exceeded 100 requests per hour",
  "retryAfter": 3600
}
```

## Rate Limiting Strategies

### Per User

```
User 123: 100 requests/hour
User 456: 100 requests/hour
```

Key: `rate_limit:user:123`

### Per API Key

```
API Key abc123: 1000 requests/hour
API Key xyz789: 1000 requests/hour
```

Key: `rate_limit:apikey:abc123`

### Per IP Address

```
IP 1.2.3.4: 50 requests/hour (unauthenticated)
```

Key: `rate_limit:ip:1.2.3.4`

### Tiered Limits

```
Free tier:    100 requests/hour
Pro tier:     1000 requests/hour
Enterprise:   10000 requests/hour
```

### Endpoint-Specific

```
GET  /users:        100 requests/hour
POST /users:        10 requests/hour  (writes limited more)
GET  /search:       20 requests/hour  (expensive ops)
POST /reports:      5 requests/hour   (very expensive)
```

## Quota Management

### Monthly Quotas

```json
{
  "quota": {
    "limit": 10000,
    "used": 7453,
    "remaining": 2547,
    "resetAt": "2026-01-01T00:00:00Z"
  }
}
```

### Quota Headers

```http
X-Quota-Limit: 10000
X-Quota-Used: 7453
X-Quota-Remaining: 2547
X-Quota-Reset: 2026-01-01T00:00:00Z
```

### When Quota Exceeded

```http
403 Forbidden

{
  "type": "https://api.example.com/errors/quota-exceeded",
  "title": "Monthly Quota Exceeded",
  "status": 403,
  "detail": "You have used 10000 of 10000 requests this month",
  "resetAt": "2026-01-01T00:00:00Z",
  "upgradeUrl": "https://example.com/upgrade"
}
```

## Implementation Patterns

### Redis-Based Rate Limiting

```javascript
async function checkRateLimit(userId, limit, window) {
  const key = `rate_limit:${userId}`;
  const now = Date.now();
  const windowStart = now - (window * 1000);

  // Remove old entries
  await redis.zremrangebyscore(key, 0, windowStart);

  // Count requests in window
  const count = await redis.zcard(key);

  if (count >= limit) {
    return {
      allowed: false,
      remaining: 0,
      reset: Math.ceil((windowStart + (window * 1000)) / 1000)
    };
  }

  // Add current request
  await redis.zadd(key, now, now);
  await redis.expire(key, window);

  return {
    allowed: true,
    remaining: limit - count - 1,
    reset: Math.ceil((now + (window * 1000)) / 1000)
  };
}
```

### Middleware Example

```javascript
async function rateLimitMiddleware(req, res, next) {
  const userId = req.user?.id || req.ip;
  const limit = req.user?.tier === 'pro' ? 1000 : 100;

  const result = await checkRateLimit(userId, limit, 3600);

  res.setHeader('X-RateLimit-Limit', limit);
  res.setHeader('X-RateLimit-Remaining', result.remaining);
  res.setHeader('X-RateLimit-Reset', result.reset);

  if (!result.allowed) {
    return res.status(429).json({
      type: 'https://api.example.com/errors/rate-limit',
      title: 'Rate Limit Exceeded',
      status: 429,
      retryAfter: result.reset - Math.floor(Date.now() / 1000)
    });
  }

  next();
}
```

## Best Practices

### Transparent Limits

- Document rate limits clearly
- Include limits in response headers
- Return clear error messages
- Provide upgrade paths

### Graceful Degradation

- Return 429 (not 403) for rate limits
- Include `Retry-After` header
- Suggest when to retry
- Offer caching guidance

### Monitoring

- Track rate limit hits per user
- Alert on unusual patterns
- Log rejected requests
- Monitor quota usage trends

### Checklist

- [ ] Implement token bucket or sliding window
- [ ] Return rate limit headers on all responses
- [ ] Use 429 status code when exceeded
- [ ] Include Retry-After header
- [ ] Document rate limits
- [ ] Support tiered limits
- [ ] Monitor and alert on limits
- [ ] Provide upgrade options
