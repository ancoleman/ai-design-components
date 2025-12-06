# Retry and Backoff Strategies

Comprehensive guide to implementing retry logic with exponential backoff, jitter, and rate limit handling.

## Table of Contents

1. [Exponential Backoff](#exponential-backoff)
2. [Jitter Strategies](#jitter-strategies)
3. [Rate Limit Handling](#rate-limit-handling)
4. [Retry Decision Logic](#retry-decision-logic)
5. [Idempotency Keys](#idempotency-keys)

## Exponential Backoff

### Algorithm

```
delay = min(base_delay * (2 ^ attempt), max_delay) + jitter
```

**Example progression:**
- Attempt 1: 1s + jitter
- Attempt 2: 2s + jitter
- Attempt 3: 4s + jitter
- Attempt 4: 8s + jitter
- Attempt 5: 10s + jitter (capped at max_delay)

### TypeScript Implementation

```typescript
interface RetryOptions {
  maxRetries: number
  baseDelay: number // milliseconds
  maxDelay: number  // milliseconds
}

async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {
    maxRetries: 3,
    baseDelay: 1000,
    maxDelay: 10000
  }
): Promise<T> {
  let attempt = 0

  while (attempt <= options.maxRetries) {
    try {
      return await fn()
    } catch (error) {
      attempt++

      if (attempt > options.maxRetries || !isRetryable(error)) {
        throw error
      }

      const delay = calculateBackoff(attempt, options)
      console.log(`Retry attempt ${attempt} after ${delay}ms`)
      await sleep(delay)
    }
  }

  throw new Error('Max retries exceeded')
}

function calculateBackoff(attempt: number, options: RetryOptions): number {
  const exponential = Math.min(
    options.baseDelay * Math.pow(2, attempt - 1),
    options.maxDelay
  )
  const jitter = Math.random() * 500 // 0-500ms
  return exponential + jitter
}

function isRetryable(error: any): boolean {
  return (
    error.code === 'ECONNRESET' ||
    error.code === 'ETIMEDOUT' ||
    (error.status >= 500 && error.status < 600) ||
    error.status === 429
  )
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}
```

### Python Implementation

```python
import time
import random
from typing import TypeVar, Callable, Any

T = TypeVar('T')

def retry_with_backoff(
    fn: Callable[[], T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 10.0
) -> T:
    attempt = 0

    while attempt <= max_retries:
        try:
            return fn()
        except Exception as error:
            attempt += 1

            if attempt > max_retries or not is_retryable(error):
                raise

            delay = calculate_backoff(attempt, base_delay, max_delay)
            print(f"Retry attempt {attempt} after {delay:.2f}s")
            time.sleep(delay)

    raise Exception("Max retries exceeded")

def calculate_backoff(attempt: int, base_delay: float, max_delay: float) -> float:
    exponential = min(base_delay * (2 ** (attempt - 1)), max_delay)
    jitter = random.random() * 0.5  # 0-0.5 seconds
    return exponential + jitter

def is_retryable(error: Exception) -> bool:
    if hasattr(error, 'status'):
        return error.status >= 500 or error.status == 429
    return False
```

### Go Implementation

```go
func retryWithBackoff[T any](
    fn func() (T, error),
    maxRetries int,
    baseDelay time.Duration,
    maxDelay time.Duration,
) (T, error) {
    var result T
    var lastErr error

    for attempt := 0; attempt <= maxRetries; attempt++ {
        result, err := fn()
        if err == nil {
            return result, nil
        }

        lastErr = err

        if !isRetryable(err) || attempt >= maxRetries {
            break
        }

        delay := calculateBackoff(attempt+1, baseDelay, maxDelay)
        fmt.Printf("Retry attempt %d after %v\n", attempt+1, delay)
        time.Sleep(delay)
    }

    return result, lastErr
}

func calculateBackoff(attempt int, baseDelay, maxDelay time.Duration) time.Duration {
    exponential := time.Duration(math.Min(
        float64(baseDelay)*math.Pow(2, float64(attempt-1)),
        float64(maxDelay),
    ))

    jitter := time.Duration(rand.Intn(500)) * time.Millisecond
    return exponential + jitter
}
```

## Jitter Strategies

### Full Jitter

Random delay between 0 and exponential backoff:

```typescript
function calculateFullJitter(attempt: number, baseDelay: number, maxDelay: number): number {
  const exponential = Math.min(baseDelay * Math.pow(2, attempt - 1), maxDelay)
  return Math.random() * exponential
}
```

**Benefits:**
- Maximum spread across time
- Best for preventing thundering herd
- Used by AWS SDK

### Equal Jitter

Half exponential + half random:

```typescript
function calculateEqualJitter(attempt: number, baseDelay: number, maxDelay: number): number {
  const exponential = Math.min(baseDelay * Math.pow(2, attempt - 1), maxDelay)
  return exponential / 2 + Math.random() * (exponential / 2)
}
```

**Benefits:**
- Balance between predictability and spread
- Shorter average wait time than full jitter

### Decorrelated Jitter

Each delay based on previous delay:

```typescript
function calculateDecorrelatedJitter(
  previousDelay: number,
  baseDelay: number,
  maxDelay: number
): number {
  return Math.min(
    maxDelay,
    Math.random() * (previousDelay * 3 - baseDelay) + baseDelay
  )
}
```

## Rate Limit Handling

### Respect Retry-After Header

```typescript
async function handleRateLimit(error: RateLimitError): Promise<void> {
  // Check for Retry-After header
  const retryAfter = error.retryAfter || 60

  console.log(`Rate limited. Retrying after ${retryAfter}s`)
  await sleep(retryAfter * 1000)
}

// In request method
if (response.status === 429) {
  const retryAfter = parseInt(response.headers.get('retry-after') || '60')

  throw new RateLimitError(
    'Rate limit exceeded',
    response.headers.get('x-request-id') || 'unknown',
    retryAfter
  )
}
```

### Rate Limit Budget Tracking

```typescript
class RateLimiter {
  private remaining: number = 0
  private resetAt: Date = new Date()

  updateFromHeaders(headers: Headers) {
    const remaining = headers.get('x-ratelimit-remaining')
    const reset = headers.get('x-ratelimit-reset')

    if (remaining) {
      this.remaining = parseInt(remaining)
    }

    if (reset) {
      this.resetAt = new Date(parseInt(reset) * 1000)
    }
  }

  async waitIfNeeded(): Promise<void> {
    if (this.remaining <= 0) {
      const now = Date.now()
      const resetTime = this.resetAt.getTime()

      if (now < resetTime) {
        const waitMs = resetTime - now
        console.log(`Rate limit budget exhausted. Waiting ${waitMs}ms`)
        await sleep(waitMs)
      }
    }
  }
}

// Usage in client
class APIClient {
  private rateLimiter = new RateLimiter()

  async request(method: string, path: string, options?: any) {
    // Wait if rate limit budget exhausted
    await this.rateLimiter.waitIfNeeded()

    const response = await fetch(...)

    // Update rate limit tracking
    this.rateLimiter.updateFromHeaders(response.headers)

    return response.json()
  }
}
```

## Retry Decision Logic

### Retryable Errors

```typescript
function isRetryable(error: any): boolean {
  // Network errors
  if (error.code === 'ECONNRESET') return true
  if (error.code === 'ETIMEDOUT') return true
  if (error.code === 'ECONNREFUSED') return true
  if (error.code === 'ENOTFOUND') return true

  // HTTP status codes
  if (!error.status) return false

  // 5xx server errors (retryable)
  if (error.status >= 500 && error.status < 600) return true

  // 429 rate limit (retryable)
  if (error.status === 429) return true

  // 408 request timeout (retryable)
  if (error.status === 408) return true

  // All other errors (not retryable)
  return false
}
```

### Non-Retryable Errors

```typescript
function isNonRetryable(error: any): boolean {
  if (!error.status) return false

  // 4xx client errors (except 408, 429)
  const nonRetryableStatuses = [400, 401, 403, 404, 405, 409, 410, 422]
  return nonRetryableStatuses.includes(error.status)
}
```

## Idempotency Keys

### Generate Idempotency Keys

```typescript
import { randomUUID } from 'crypto'

class APIClient {
  async request(
    method: string,
    path: string,
    options?: {
      body?: any
      idempotencyKey?: string
    }
  ) {
    const headers: Record<string, string> = {
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json'
    }

    // Add idempotency key for mutating operations
    if (['POST', 'PATCH', 'PUT', 'DELETE'].includes(method.toUpperCase())) {
      headers['Idempotency-Key'] = options?.idempotencyKey || randomUUID()
    }

    // Make request with retry
    return retryWithBackoff(() => {
      return fetch(url, { method, headers, body: JSON.stringify(options?.body) })
    })
  }
}

// Usage: Custom idempotency key
await client.charges.create(
  { amount: 1000, currency: 'usd' },
  { idempotencyKey: 'charge_unique_123' }
)
```

### Server-Side Idempotency

Server caches responses by idempotency key:

```typescript
// Pseudo-code for server
const cache = new Map<string, Response>()

async function handleRequest(req: Request): Promise<Response> {
  const idempotencyKey = req.headers['idempotency-key']

  if (idempotencyKey && cache.has(idempotencyKey)) {
    // Return cached response
    return cache.get(idempotencyKey)!
  }

  const response = await processRequest(req)

  if (idempotencyKey) {
    // Cache response for 24 hours
    cache.set(idempotencyKey, response)
    setTimeout(() => cache.delete(idempotencyKey), 24 * 60 * 60 * 1000)
  }

  return response
}
```

## Best Practices

### Configuration

Allow users to configure retry behavior:

```typescript
const client = new APIClient({
  apiKey: 'sk_test_...',
  retry: {
    maxRetries: 5,
    baseDelay: 1000,
    maxDelay: 30000,
    retryableStatuses: [429, 500, 502, 503, 504]
  }
})
```

### Logging

Log retry attempts for debugging:

```typescript
async function retryWithBackoff<T>(fn: () => Promise<T>, options: RetryOptions): Promise<T> {
  let attempt = 0

  while (attempt <= options.maxRetries) {
    try {
      const result = await fn()

      if (attempt > 0) {
        console.log(`Request succeeded after ${attempt} retries`)
      }

      return result
    } catch (error) {
      attempt++

      if (attempt > options.maxRetries || !isRetryable(error)) {
        if (attempt > 1) {
          console.error(`Request failed after ${attempt - 1} retries:`, error)
        }
        throw error
      }

      const delay = calculateBackoff(attempt, options)
      console.log(`Retry attempt ${attempt}/${options.maxRetries} after ${delay}ms (error: ${error.message})`)
      await sleep(delay)
    }
  }
}
```

### Circuit Breaker

Stop retrying if service is down:

```typescript
class CircuitBreaker {
  private failures = 0
  private lastFailure: Date | null = null
  private state: 'closed' | 'open' | 'half-open' = 'closed'

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      // Check if we should try again
      const now = Date.now()
      const lastFailureTime = this.lastFailure?.getTime() || 0
      const timeout = 60000 // 60 seconds

      if (now - lastFailureTime > timeout) {
        this.state = 'half-open'
      } else {
        throw new Error('Circuit breaker is open')
      }
    }

    try {
      const result = await fn()

      // Success - reset circuit
      this.failures = 0
      this.state = 'closed'

      return result
    } catch (error) {
      this.failures++
      this.lastFailure = new Date()

      // Open circuit after 5 failures
      if (this.failures >= 5) {
        this.state = 'open'
      }

      throw error
    }
  }
}
```
