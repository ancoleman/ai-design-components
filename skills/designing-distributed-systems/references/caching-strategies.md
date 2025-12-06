# Caching Strategies

## Table of Contents

1. [Cache-Aside (Lazy Loading)](#cache-aside-lazy-loading)
2. [Write-Through](#write-through)
3. [Write-Behind (Write-Back)](#write-behind-write-back)
4. [Cache Invalidation](#cache-invalidation)
5. [Best Practices](#best-practices)

## Cache-Aside (Lazy Loading)

### Pattern

```
Read:
1. Check cache → hit? return
2. Miss? Query database
3. Store in cache, return

Write:
1. Write to database
2. Invalidate cache (optional)
```

### Implementation

```python
import redis
import json

class CacheAside:
    def __init__(self, cache, database):
        self.cache = cache  # Redis
        self.db = database
    
    def get(self, key):
        # Try cache first
        cached = self.cache.get(key)
        if cached:
            return json.loads(cached)
        
        # Cache miss - query database
        value = self.db.query(key)
        if value:
            self.cache.setex(key, 3600, json.dumps(value))
        return value
    
    def set(self, key, value):
        # Write to database
        self.db.write(key, value)
        # Invalidate cache
        self.cache.delete(key)
```

## Write-Through

### Pattern

```
Write:
1. Write to cache
2. Cache writes to database synchronously
3. Return success
```

### Implementation

```python
class WriteThrough:
    def __init__(self, cache, database):
        self.cache = cache
        self.db = database
    
    def set(self, key, value):
        # Write to database first
        self.db.write(key, value)
        # Then update cache
        self.cache.set(key, json.dumps(value))
    
    def get(self, key):
        # Always from cache
        cached = self.cache.get(key)
        return json.loads(cached) if cached else None
```

## Write-Behind (Write-Back)

### Pattern

```
Write:
1. Write to cache
2. Return success immediately
3. Cache writes to database asynchronously (batched)
```

### Benefits: Low latency writes
### Trade-off: Data loss if cache fails before DB write

## Cache Invalidation

### Strategies

**TTL (Time-To-Live):**
```python
cache.setex(key, 3600, value)  # Expire after 1 hour
```

**Event-Based:**
```python
# Invalidate on update
def update_user(user_id, data):
    db.update(user_id, data)
    cache.delete(f"user:{user_id}")
```

**Manual:**
```python
# Explicit invalidation
cache.delete(key)
```

## Best Practices

- Set appropriate TTLs
- Handle cache misses gracefully (thundering herd)
- Monitor cache hit rate
- Use consistent hashing for distributed caches
