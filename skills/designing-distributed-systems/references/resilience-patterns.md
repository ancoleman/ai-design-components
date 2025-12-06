# Resilience Patterns

## Table of Contents

1. [Circuit Breaker Pattern](#circuit-breaker-pattern)
2. [Bulkhead Isolation](#bulkhead-isolation)
3. [Timeout and Retry Strategies](#timeout-and-retry-strategies)
4. [Rate Limiting and Backpressure](#rate-limiting-and-backpressure)

## Circuit Breaker Pattern

### Concept

Prevent cascading failures by failing fast when a service is unavailable.

### States

```
[CLOSED] → Normal operation, requests flow through
   │ (failures exceed threshold)
   ▼
[OPEN] → Fail fast, don't call failing service
   │ (timeout expires)
   ▼
[HALF-OPEN] → Try single request to test recovery
   │ success → [CLOSED]
   │ failure → [OPEN]
```

### Implementation

```python
from enum import Enum
from datetime import datetime, timedelta
import threading

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60, success_threshold=2):
        self.failure_threshold = failure_threshold
        self.timeout = timeout  # seconds
        self.success_threshold = success_threshold
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.lock = threading.Lock()
    
    def call(self, func, *args, **kwargs):
        with self.lock:
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitState.HALF_OPEN
                else:
                    raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_reset(self):
        return (self.last_failure_time and 
                datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout))
    
    def _on_success(self):
        with self.lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.success_threshold:
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    self.success_count = 0
            else:
                self.failure_count = 0
    
    def _on_failure(self):
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
                self.success_count = 0

# Usage
circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60)

def call_external_service():
    try:
        return circuit_breaker.call(external_service_function)
    except Exception as e:
        return "Fallback response"
```

## Bulkhead Isolation

### Concept

Isolate resources (thread pools, connection pools) to prevent one failing component from exhausting all resources.

### Implementation

```python
from concurrent.futures import ThreadPoolExecutor
import threading

class BulkheadExecutor:
    def __init__(self):
        # Separate thread pools for different services
        self.pools = {
            'payment_service': ThreadPoolExecutor(max_workers=10),
            'inventory_service': ThreadPoolExecutor(max_workers=20),
            'email_service': ThreadPoolExecutor(max_workers=5)
        }
    
    def execute(self, service_name, func, *args, **kwargs):
        pool = self.pools.get(service_name)
        if not pool:
            raise ValueError(f"Unknown service: {service_name}")
        
        future = pool.submit(func, *args, **kwargs)
        return future

# Usage
bulkhead = BulkheadExecutor()

# Payment service failure doesn't affect inventory service
bulkhead.execute('payment_service', process_payment, order_id)
bulkhead.execute('inventory_service', reserve_inventory, product_id)
```

## Timeout and Retry Strategies

### Exponential Backoff with Jitter

```python
import time
import random

class RetryStrategy:
    def __init__(self, max_retries=3, base_delay=1, max_delay=60):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    def execute(self, func, *args, **kwargs):
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries:
                    raise e
                
                # Exponential backoff with jitter
                delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                jitter = random.uniform(0, delay * 0.1)
                sleep_time = delay + jitter
                
                print(f"Retry {attempt + 1} after {sleep_time:.2f}s")
                time.sleep(sleep_time)

# Usage
retry = RetryStrategy(max_retries=3, base_delay=1)
result = retry.execute(unreliable_service_call)
```

## Rate Limiting and Backpressure

### Token Bucket

```python
import time
import threading

class TokenBucket:
    def __init__(self, capacity, fill_rate):
        self.capacity = capacity
        self.fill_rate = fill_rate  # tokens per second
        self.tokens = capacity
        self.last_update = time.time()
        self.lock = threading.Lock()
    
    def acquire(self, tokens=1):
        with self.lock:
            self._refill()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def _refill(self):
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.fill_rate)
        self.last_update = now

# Usage
rate_limiter = TokenBucket(capacity=100, fill_rate=10)  # 10 requests/sec

if rate_limiter.acquire():
    handle_request()
else:
    return "Rate limit exceeded"
```
