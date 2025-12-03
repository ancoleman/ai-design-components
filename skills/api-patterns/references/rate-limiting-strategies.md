# Rate Limiting Strategies

Rate limiting controls request frequency to prevent abuse, ensure fair resource allocation, and maintain API stability.

## Algorithm Comparison

| Algorithm | Accuracy | Memory | Burst Handling | Best For |
|-----------|----------|--------|----------------|----------|
| Token Bucket | High | Low | Excellent | General use (recommended) |
| Sliding Window | Very High | Medium | Good | Strict rate enforcement |
| Fixed Window | Medium | Low | Poor | Simple cases only |
| Leaky Bucket | High | Low | Fair | Smooth traffic shaping |

## Token Bucket Algorithm (Recommended)

**Concept:**
- Bucket holds tokens (max capacity = rate limit)
- Tokens added at fixed rate (e.g., 100/minute)
- Each request consumes 1 token
- Request rejected if bucket empty
- Allows bursts up to bucket capacity

**FastAPI Implementation:**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/items")
@limiter.limit("100/minute")
async def list_items():
    return {"items": []}

# Multiple limits
@app.post("/items")
@limiter.limit("10/second;100/minute;1000/hour")
async def create_item(item: Item):
    return {"id": 1, **item.dict()}
```

**Hono + Redis Implementation:**
```typescript
import { Hono } from 'hono'
import { RedisStore } from 'rate-limit-redis'
import { rateLimit } from 'hono-rate-limiter'
import { createClient } from 'redis'

const redis = createClient({ url: 'redis://localhost:6379' })
await redis.connect()

const limiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 100, // 100 requests per minute
  standardHeaders: true,
  store: new RedisStore({
    client: redis,
    prefix: 'rl:',
  }),
})

const app = new Hono()
app.use('/api/*', limiter)
```

## Sliding Window Algorithm

**Concept:**
- Tracks exact request timestamps in rolling window
- More accurate than fixed window
- Higher memory usage (stores all timestamps)
- No burst allowance issues

**Redis Lua Script (Atomic Operation):**
```lua
-- sliding_window_rate_limit.lua
local key = KEYS[1]
local window = tonumber(ARGV[1])  -- Window size in seconds
local limit = tonumber(ARGV[2])   -- Max requests per window
local now = tonumber(ARGV[3])     -- Current timestamp

-- Remove old entries outside window
redis.call('ZREMRANGEBYSCORE', key, 0, now - window)

-- Count requests in current window
local current = redis.call('ZCARD', key)

if current < limit then
    -- Add new request timestamp
    redis.call('ZADD', key, now, now)
    redis.call('EXPIRE', key, window)
    return 1  -- Allow
else
    return 0  -- Reject
end
```

**FastAPI + Redis Implementation:**
```python
import redis
import time
from fastapi import HTTPException

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

async def sliding_window_limiter(
    user_id: str,
    limit: int = 100,
    window: int = 60  # seconds
):
    key = f"rate_limit:{user_id}"
    now = time.time()

    # Load Lua script
    script = redis_client.register_script("""
        local key = KEYS[1]
        local window = tonumber(ARGV[1])
        local limit = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])

        redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
        local current = redis.call('ZCARD', key)

        if current < limit then
            redis.call('ZADD', key, now, now)
            redis.call('EXPIRE', key, window)
            return 1
        else
            return 0
        end
    """)

    allowed = script(keys=[key], args=[window, limit, now])

    if not allowed:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
```

## Fixed Window Algorithm (Simple, Not Recommended)

**Concept:**
- Resets counter at fixed intervals
- Simple but inaccurate
- Allows 2x rate at window boundaries

**Problem Example:**
```
Rate limit: 100 req/minute
Window 1: 11:59:00 - 11:59:59 → 100 requests at 11:59:59
Window 2: 12:00:00 - 12:00:59 → 100 requests at 12:00:00
Result: 200 requests in 1 second (burst problem)
```

**Use only for low-stakes scenarios.**

## Distributed Rate Limiting (Microservices)

**Redis Centralized Approach:**
```python
from redis import Redis
from fastapi import Request, HTTPException
import hashlib

redis_client = Redis(host='redis', port=6379)

async def distributed_rate_limit(request: Request, limit: int = 100, window: int = 60):
    # Use client IP or API key
    identifier = request.client.host
    key = f"rate_limit:{hashlib.sha256(identifier.encode()).hexdigest()}"

    pipe = redis_client.pipeline()
    pipe.incr(key)
    pipe.expire(key, window)
    result = pipe.execute()

    current_count = result[0]

    if current_count > limit:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Try again in {window} seconds.",
            headers={"Retry-After": str(window)}
        )

    return current_count

@app.get("/items")
async def list_items(request: Request):
    await distributed_rate_limit(request, limit=100, window=60)
    return {"items": []}
```

## Per-User vs Per-IP Rate Limiting

**Per-User (Authenticated APIs):**
```python
from fastapi import Depends
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    # Decode JWT, return user ID
    return decode_token(token)

@app.get("/items")
async def list_items(user_id: str = Depends(get_current_user)):
    await rate_limit_user(user_id, limit=1000, window=3600)  # Higher limit for auth users
    return {"items": []}
```

**Per-IP (Public APIs):**
```python
from fastapi import Request

@app.get("/public/items")
async def public_items(request: Request):
    ip = request.client.host
    await rate_limit_ip(ip, limit=100, window=3600)  # Lower limit for anonymous
    return {"items": []}
```

## Rate Limit Headers (Best Practice)

Include standard headers in responses:

```python
from fastapi import Response

@app.get("/items")
async def list_items(response: Response):
    limit = 100
    remaining = 95
    reset = 1640995200  # Unix timestamp

    response.headers["X-RateLimit-Limit"] = str(limit)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Reset"] = str(reset)

    return {"items": []}
```

**Response on rate limit exceeded:**
```python
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
        headers={
            "Retry-After": "60",
            "X-RateLimit-Limit": "100",
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": str(int(time.time()) + 60)
        }
    )
```

## Performance Considerations

**In-Memory (Single Instance):**
- Fastest (no network I/O)
- Lost on restart
- Doesn't scale across instances

**Redis (Distributed):**
- Persistent, shared state
- ~1-2ms latency per operation
- Scales horizontally
- Requires Redis infrastructure

**DynamoDB/Database (Rare):**
- Persistent, global
- 10-50ms latency
- Overkill for most use cases

## Adaptive Rate Limiting

Adjust limits based on load:

```python
import asyncio
from datetime import datetime

class AdaptiveRateLimiter:
    def __init__(self, base_limit: int = 100):
        self.base_limit = base_limit
        self.current_load = 0.0

    async def get_current_limit(self) -> int:
        # Reduce limit during high load
        if self.current_load > 0.8:
            return int(self.base_limit * 0.5)
        elif self.current_load > 0.6:
            return int(self.base_limit * 0.75)
        else:
            return self.base_limit

    async def update_load(self):
        # Monitor CPU, memory, request queue
        self.current_load = await get_system_load()

limiter = AdaptiveRateLimiter(base_limit=1000)

@app.get("/items")
async def list_items():
    limit = await limiter.get_current_limit()
    # Apply limit...
```

## Cost-Based Rate Limiting

Different costs for different endpoints:

```python
ENDPOINT_COSTS = {
    "GET /items": 1,           # Cheap read
    "POST /items": 5,          # Write operation
    "POST /search": 10,        # Expensive search
    "POST /ai/analyze": 50,    # AI processing
}

async def cost_based_limiter(request: Request, budget: int = 1000):
    endpoint = f"{request.method} {request.url.path}"
    cost = ENDPOINT_COSTS.get(endpoint, 1)

    user_id = get_user_id(request)
    key = f"cost:{user_id}"

    current = redis_client.incrby(key, cost)
    redis_client.expire(key, 3600)  # 1 hour window

    if current > budget:
        raise HTTPException(429, detail=f"Budget exceeded. Used {current}/{budget} credits.")
```

## Testing Rate Limiting

**Load Test Script:**
```python
import asyncio
import aiohttp

async def test_rate_limit(url: str, total_requests: int = 200):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(total_requests):
            tasks.append(session.get(url))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        success = sum(1 for r in results if isinstance(r, aiohttp.ClientResponse) and r.status == 200)
        rate_limited = sum(1 for r in results if isinstance(r, aiohttp.ClientResponse) and r.status == 429)

        print(f"Success: {success}, Rate Limited: {rate_limited}")

asyncio.run(test_rate_limit("http://localhost:8000/items"))
```

## Recommendation Matrix

| Use Case | Algorithm | Storage | Notes |
|----------|-----------|---------|-------|
| Small API (<1k req/s) | Token Bucket | In-memory | Simple, effective |
| Public API | Sliding Window | Redis | Accurate, fair |
| Microservices | Token Bucket | Redis | Fast, distributed |
| Cost-based | Custom | Redis/DB | Track budget |
| Adaptive | Token Bucket | Redis + metrics | Respond to load |

**Default recommendation:** Token Bucket with Redis for production systems.
