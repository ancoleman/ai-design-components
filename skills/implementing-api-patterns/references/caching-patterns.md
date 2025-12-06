# Caching Patterns for APIs

Caching reduces latency, improves scalability, and decreases database load by storing frequently accessed data.


## Table of Contents

- [Cache Layers](#cache-layers)
- [HTTP Caching (Browser/CDN)](#http-caching-browsercdn)
  - [Cache-Control Headers](#cache-control-headers)
  - [ETag (Conditional Requests)](#etag-conditional-requests)
  - [Last-Modified (Time-based Caching)](#last-modified-time-based-caching)
- [Application Caching (Redis)](#application-caching-redis)
  - [Simple Key-Value Cache](#simple-key-value-cache)
  - [Cache-Aside Pattern (Recommended)](#cache-aside-pattern-recommended)
  - [Write-Through Cache](#write-through-cache)
  - [Write-Behind Cache (Lazy Write)](#write-behind-cache-lazy-write)
- [Cache Invalidation Strategies](#cache-invalidation-strategies)
  - [Time-based (TTL)](#time-based-ttl)
  - [Event-based Invalidation](#event-based-invalidation)
  - [Cache Tags](#cache-tags)
- [Cache Warming](#cache-warming)
- [Cache Stampede Prevention](#cache-stampede-prevention)
- [Multi-Level Caching](#multi-level-caching)
- [Cache Performance Monitoring](#cache-performance-monitoring)
- [GraphQL-Specific Caching](#graphql-specific-caching)
- [Recommendation Matrix](#recommendation-matrix)

## Cache Layers

```
Client
  ↓ (HTTP Cache)
CDN/Edge Cache
  ↓ (Application Cache)
API Server
  ↓ (Database Query Cache)
Database
```

## HTTP Caching (Browser/CDN)

### Cache-Control Headers

**Public, Long-lived (Static Assets):**
```python
from fastapi import Response

@app.get("/api/config")
async def get_config(response: Response):
    response.headers["Cache-Control"] = "public, max-age=3600, immutable"
    response.headers["ETag"] = '"v1.2.3"'
    return {"version": "1.2.3", "features": ["dark-mode"]}
```

**Private, Short-lived (User Data):**
```python
@app.get("/api/user/profile")
async def get_profile(response: Response):
    response.headers["Cache-Control"] = "private, max-age=60"
    return {"name": "User", "email": "user@example.com"}
```

**No Cache (Sensitive/Real-time):**
```python
@app.get("/api/user/balance")
async def get_balance(response: Response):
    response.headers["Cache-Control"] = "no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    return {"balance": 1234.56}
```

### ETag (Conditional Requests)

**Server-side:**
```python
from fastapi import Request, Response, HTTPException
import hashlib
import json

@app.get("/api/items/{item_id}")
async def get_item(item_id: int, request: Request, response: Response):
    item = await db.get_item(item_id)
    item_json = json.dumps(item, sort_keys=True)

    # Generate ETag from content
    etag = f'"{hashlib.md5(item_json.encode()).hexdigest()}"'

    # Check If-None-Match header
    if request.headers.get("If-None-Match") == etag:
        raise HTTPException(status_code=304)  # Not Modified

    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "private, max-age=60"
    return item
```

**Client-side:**
```typescript
// First request
const res1 = await fetch('/api/items/1')
const etag = res1.headers.get('ETag')
const data = await res1.json()

// Subsequent request
const res2 = await fetch('/api/items/1', {
  headers: { 'If-None-Match': etag }
})

if (res2.status === 304) {
  // Use cached data
  console.log('Using cached data:', data)
} else {
  // Update cache
  const newData = await res2.json()
}
```

### Last-Modified (Time-based Caching)

```python
from datetime import datetime

@app.get("/api/items/{item_id}")
async def get_item(item_id: int, request: Request, response: Response):
    item = await db.get_item(item_id)

    last_modified = item.updated_at
    response.headers["Last-Modified"] = last_modified.strftime("%a, %d %b %Y %H:%M:%S GMT")

    # Check If-Modified-Since
    if_modified_since = request.headers.get("If-Modified-Since")
    if if_modified_since:
        client_date = datetime.strptime(if_modified_since, "%a, %d %b %Y %H:%M:%S GMT")
        if client_date >= last_modified:
            raise HTTPException(status_code=304)

    return item
```

## Application Caching (Redis)

### Simple Key-Value Cache

**FastAPI + Redis:**
```python
from redis import Redis
import json

redis_client = Redis(host='localhost', port=6379, decode_responses=True)

@app.get("/api/items/{item_id}")
async def get_item(item_id: int):
    cache_key = f"item:{item_id}"

    # Try cache first
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Cache miss - query database
    item = await db.get_item(item_id)

    # Store in cache (TTL: 5 minutes)
    redis_client.setex(cache_key, 300, json.dumps(item))

    return item
```

### Cache-Aside Pattern (Recommended)

**Decorator Approach:**
```python
from functools import wraps
import pickle

def cache_aside(ttl: int = 300, key_prefix: str = ""):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{key_prefix}:{func.__name__}:{hash((args, tuple(kwargs.items())))}"

            # Try cache
            cached = redis_client.get(cache_key)
            if cached:
                return pickle.loads(cached)

            # Execute function
            result = await func(*args, **kwargs)

            # Store in cache
            redis_client.setex(cache_key, ttl, pickle.dumps(result))

            return result
        return wrapper
    return decorator

@app.get("/api/items")
@cache_aside(ttl=300, key_prefix="items_list")
async def list_items(limit: int = 20, offset: int = 0):
    return await db.query(Item).limit(limit).offset(offset).all()
```

### Write-Through Cache

**Update cache on write:**
```python
@app.post("/api/items")
async def create_item(item: ItemCreate):
    # Write to database
    new_item = await db.create(item)

    # Immediately update cache
    cache_key = f"item:{new_item.id}"
    redis_client.setex(cache_key, 300, json.dumps(new_item.to_dict()))

    # Invalidate list cache
    redis_client.delete("items_list:*")

    return new_item
```

### Write-Behind Cache (Lazy Write)

**Queue writes for background processing:**
```python
from asyncio import Queue

write_queue = Queue()

@app.post("/api/items")
async def create_item(item: ItemCreate):
    # Update cache immediately
    item_id = generate_id()
    cache_key = f"item:{item_id}"
    redis_client.setex(cache_key, 300, json.dumps(item.dict()))

    # Queue database write
    await write_queue.put(("create", item))

    return {"id": item_id, **item.dict()}

# Background worker
async def write_worker():
    while True:
        operation, data = await write_queue.get()
        try:
            if operation == "create":
                await db.create(data)
        except Exception as e:
            logger.error(f"Write failed: {e}")
```

## Cache Invalidation Strategies

### Time-based (TTL)

**Fixed expiration:**
```python
redis_client.setex("key", 300, "value")  # Expires in 5 minutes
```

**Sliding expiration:**
```python
redis_client.set("key", "value")
redis_client.expire("key", 300)  # Refresh TTL on access
```

### Event-based Invalidation

**Invalidate on write:**
```python
@app.put("/api/items/{item_id}")
async def update_item(item_id: int, item: ItemUpdate):
    # Update database
    updated_item = await db.update(item_id, item)

    # Invalidate specific item cache
    redis_client.delete(f"item:{item_id}")

    # Invalidate related caches
    redis_client.delete(f"user:{updated_item.user_id}:items")

    return updated_item
```

### Cache Tags

**Group related cache entries:**
```python
from typing import List

class TaggedCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    def set_with_tags(self, key: str, value: str, tags: List[str], ttl: int = 300):
        # Store value
        self.redis.setex(key, ttl, value)

        # Add to tag sets
        for tag in tags:
            self.redis.sadd(f"tag:{tag}", key)
            self.redis.expire(f"tag:{tag}", ttl)

    def invalidate_by_tag(self, tag: str):
        # Get all keys with this tag
        keys = self.redis.smembers(f"tag:{tag}")

        # Delete all tagged keys
        if keys:
            self.redis.delete(*keys)

        # Delete tag set
        self.redis.delete(f"tag:{tag}")

cache = TaggedCache(redis_client)

@app.get("/api/items/{item_id}")
async def get_item(item_id: int):
    cache_key = f"item:{item_id}"
    cached = cache.redis.get(cache_key)
    if cached:
        return json.loads(cached)

    item = await db.get_item(item_id)
    cache.set_with_tags(
        cache_key,
        json.dumps(item),
        tags=["items", f"user:{item.user_id}"],
        ttl=300
    )
    return item

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    await db.delete_user(user_id)
    # Invalidate all items for this user
    cache.invalidate_by_tag(f"user:{user_id}")
```

## Cache Warming

**Preload cache on startup:**
```python
@app.on_event("startup")
async def warm_cache():
    # Load frequently accessed items
    popular_items = await db.query(Item).order_by(Item.views.desc()).limit(100).all()

    for item in popular_items:
        cache_key = f"item:{item.id}"
        redis_client.setex(cache_key, 3600, json.dumps(item.to_dict()))

    logger.info(f"Warmed cache with {len(popular_items)} items")
```

## Cache Stampede Prevention

**Problem:** Many requests hit database simultaneously when cache expires.

**Solution: Lock-based Approach:**
```python
import asyncio

async def get_with_lock(key: str, fetch_func, ttl: int = 300):
    # Try cache
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)

    # Acquire lock
    lock_key = f"lock:{key}"
    lock_acquired = redis_client.set(lock_key, "1", nx=True, ex=10)

    if lock_acquired:
        # This request fetches fresh data
        try:
            data = await fetch_func()
            redis_client.setex(key, ttl, json.dumps(data))
            return data
        finally:
            redis_client.delete(lock_key)
    else:
        # Wait for other request to populate cache
        for _ in range(10):
            await asyncio.sleep(0.1)
            cached = redis_client.get(key)
            if cached:
                return json.loads(cached)

        # Fallback: fetch anyway
        return await fetch_func()

@app.get("/api/expensive-query")
async def expensive_query():
    return await get_with_lock(
        "expensive_query_result",
        lambda: db.complex_aggregation(),
        ttl=600
    )
```

**Solution: Probabilistic Early Expiration:**
```python
import random
import time

async def probabilistic_cache(key: str, fetch_func, ttl: int = 300):
    cached_data = redis_client.get(key)
    if not cached_data:
        # Cache miss
        data = await fetch_func()
        redis_client.setex(key, ttl, json.dumps({"data": data, "stored_at": time.time()}))
        return data

    cache_entry = json.loads(cached_data)
    stored_at = cache_entry["stored_at"]
    age = time.time() - stored_at

    # Probability of early refresh increases with age
    refresh_probability = age / ttl

    if random.random() < refresh_probability:
        # Refresh cache early
        data = await fetch_func()
        redis_client.setex(key, ttl, json.dumps({"data": data, "stored_at": time.time()}))
        return data

    return cache_entry["data"]
```

## Multi-Level Caching

**In-memory + Redis:**
```python
from cachetools import TTLCache
import asyncio

# L1: In-memory cache (fast, small)
l1_cache = TTLCache(maxsize=1000, ttl=60)

# L2: Redis cache (slower, larger)
redis_client = Redis()

async def multi_level_get(key: str, fetch_func):
    # Check L1 (in-memory)
    if key in l1_cache:
        return l1_cache[key]

    # Check L2 (Redis)
    cached = redis_client.get(key)
    if cached:
        data = json.loads(cached)
        l1_cache[key] = data  # Populate L1
        return data

    # Cache miss - fetch from source
    data = await fetch_func()

    # Populate both caches
    l1_cache[key] = data
    redis_client.setex(key, 300, json.dumps(data))

    return data
```

## Cache Performance Monitoring

**Track cache hit rate:**
```python
from prometheus_client import Counter, Histogram

cache_hits = Counter('cache_hits_total', 'Number of cache hits')
cache_misses = Counter('cache_misses_total', 'Number of cache misses')
cache_latency = Histogram('cache_latency_seconds', 'Cache operation latency')

async def get_cached(key: str, fetch_func):
    with cache_latency.time():
        cached = redis_client.get(key)
        if cached:
            cache_hits.inc()
            return json.loads(cached)

        cache_misses.inc()
        data = await fetch_func()
        redis_client.setex(key, 300, json.dumps(data))
        return data
```

## GraphQL-Specific Caching

**DataLoader pattern (N+1 prevention):**
```python
from strawberry.dataloader import DataLoader

async def load_users(keys: List[int]) -> List[User]:
    # Batch database query
    users = await db.query(User).filter(User.id.in_(keys)).all()
    user_map = {user.id: user for user in users}

    # Return in same order as keys
    return [user_map.get(key) for key in keys]

user_loader = DataLoader(load_fn=load_users)

@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: int) -> User:
        return await user_loader.load(id)
```

## Recommendation Matrix

| Use Case | Strategy | TTL | Notes |
|----------|----------|-----|-------|
| Static config | HTTP Cache + Redis | 1 hour | Use `immutable` |
| User profiles | Redis (cache-aside) | 5 min | Private cache |
| Search results | Redis (cache-aside) | 1 min | Short TTL |
| Product catalog | Redis + HTTP Cache | 30 min | Public cache |
| Real-time data | No cache or <10s | <10s | Balance freshness |
| Expensive queries | Redis + early expiration | 10 min | Prevent stampede |

**General Guidelines:**
- **Static data:** Long TTL (hours/days)
- **User data:** Medium TTL (minutes)
- **Real-time data:** Short TTL (seconds) or no cache
- **Always measure:** Track hit rate, latency, memory usage
