# SDK Design Skill - Master Plan

**Skill Name:** `sdk-design`
**Skill Level:** Mid Level (5,000-8,000 tokens, 500-800 lines init.md)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [SDK Architecture Taxonomy](#sdk-architecture-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [TypeScript SDK Patterns](#typescript-sdk-patterns)
7. [Python SDK Patterns](#python-sdk-patterns)
8. [Go SDK Patterns](#go-sdk-patterns)
9. [Cross-Cutting Patterns](#cross-cutting-patterns)
10. [Library Recommendations](#library-recommendations)
11. [Skill Structure Design](#skill-structure-design)
12. [Integration Points](#integration-points)
13. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

In 2025, every SaaS company, API platform, and cloud service needs a well-designed SDK to enable developer adoption. Poor SDK design leads to integration failures, support burden, and developer churn. This skill addresses a critical gap: strategic SDK design that goes beyond basic HTTP client wrappers.

**Market Drivers:**

- **Developer Experience is Competitive Advantage:** Companies with great SDKs (Stripe, AWS, OpenAI) win developer mindshare
- **Multi-Language Support Required:** Modern platforms serve polyglot teams (TypeScript, Python, Go, Rust)
- **AI SDK Explosion:** Every AI platform (OpenAI, Anthropic, Cohere) ships SDKs with streaming, retries, and async patterns
- **OpenAPI-Driven Generation:** Tools like openapi-generator and liblab automate SDK generation, but custom patterns still needed
- **SDK-as-Product Mindset:** SDKs are no longer afterthoughts; they're core product experiences

**Strategic Value:**

1. **Universal Need:** Every API needs a client library
2. **Cross-Cutting Concern:** Integrates with API design, error handling, observability
3. **Developer Enabler:** Good SDKs reduce time-to-first-API-call from hours to minutes
4. **Maintenance Critical:** Poor SDK design creates ongoing support burden

### How This Differs from Existing Solutions

**Existing SDK Documentation:**

- **Framework-Specific:** Most docs focus on single languages (JS SDK guide, Python SDK guide)
- **Tactical Focus:** "How to make an HTTP request" vs. "How to design retry logic"
- **Generated Code Assumptions:** Assumes OpenAPI generation solves everything (it doesn't)
- **Missing Strategic Guidance:** When to use sync vs. async, how to handle pagination, error hierarchies

**Our Approach:**

- **Multi-Language Unified:** Consistent patterns across TypeScript, Python, Go
- **Strategic Decision Framework:** When to use which patterns (sync/async, callback/promise/generator)
- **Real-World Patterns:** Based on AWS SDK, Stripe, OpenAI best practices (2025 research)
- **Beyond Generated Code:** Custom patterns for retry, backoff, auth refresh, pagination
- **Developer Experience Focus:** Optimizing for time-to-first-success

### Target Audience

**Primary Users:**

- Backend developers building API client libraries
- Platform engineers creating internal service SDKs
- Developer relations teams improving SDK quality
- Full-stack developers consuming third-party SDKs

**Skill Level Assumptions:**

- Understands REST/HTTP basics
- Familiar with at least one programming language (TypeScript, Python, or Go)
- Knows async/sync differences (but needs guidance on when to use each)

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **SDK Architecture Patterns**
   - Client, resources, and methods organization
   - Sync vs. async API design
   - Request/response interceptors
   - Middleware and plugin systems

2. **Authentication Handling**
   - API key management (headers, query params)
   - OAuth token refresh patterns
   - Bearer token handling
   - Credential rotation without downtime

3. **Retry and Backoff Strategies**
   - Exponential backoff with jitter
   - Retry on transient errors (5xx, network timeouts)
   - Rate limit handling (429 response codes)
   - Idempotency key management

4. **Error Handling Patterns**
   - Typed error hierarchies (APIError, AuthenticationError, RateLimitError)
   - Error metadata (request ID, status code, error type)
   - Retryable vs. non-retryable errors
   - User-friendly error messages

5. **Pagination Abstraction**
   - Cursor-based pagination (next token)
   - Offset-based pagination (page number)
   - Async iterators (for await loops)
   - Manual vs. automatic pagination

6. **Multi-Language SDK Consistency**
   - TypeScript: Promise-based, async/await, streaming
   - Python: Sync and async clients, context managers, generators
   - Go: Idiomatic patterns, context.Context, channels

7. **Versioning and Deprecation**
   - Semantic versioning (SemVer) strategy
   - Backward compatibility guarantees
   - Deprecation warnings and migration guides
   - API version pinning

### What This Skill Does NOT Cover

**Out of Scope:**

- **API Server Implementation:** Covered by `api-patterns` skill
- **OpenAPI Specification Writing:** Covered by API design skills
- **CLI Tools:** Covered by `building-clis` skill
- **GraphQL Clients:** Different patterns, separate skill
- **Low-Level HTTP Clients:** Focus on SDK design, not building Axios/Fetch from scratch

### Success Criteria

**A user successfully uses this skill when they can:**

1. Design an SDK architecture with clear client/resource/method organization
2. Implement retry logic with exponential backoff and jitter
3. Handle authentication (API keys, token refresh) cleanly
4. Create typed error hierarchies for debugging
5. Implement pagination with async iterators or generators
6. Design consistent SDK APIs across TypeScript, Python, and Go
7. Version and deprecate SDK methods without breaking users

---

## Research Findings

### Research Date: December 3, 2025

**Research Tools Used:**

- Google Search Grounding (Vertex AI): SDK design best practices, retry patterns
- Context7: AWS SDK v3, Stripe Node, OpenAI Node documentation
- Official SDK documentation: AWS, Stripe, OpenAI, Anthropic

### Key Trends for 2025

**1. Streaming-First APIs**

- AI/LLM APIs (OpenAI, Anthropic) prioritize streaming responses
- SDKs provide async iterators and event-driven streaming helpers
- Server-Sent Events (SSE) and WebSocket support built-in

**2. Typed Errors with Rich Metadata**

- Error classes include request ID, status code, error type, retryability
- Users can differentiate card declines from rate limits from server errors
- Error messages link to documentation

**3. Automatic Retry with Smart Backoff**

- SDKs retry transient errors by default (configurable)
- Exponential backoff with jitter prevents thundering herd
- Idempotency keys automatically added to prevent duplicate operations

**4. Multi-Client Architecture**

- Separate sync and async clients (Python: `Client` vs. `AsyncClient`)
- Resource-based organization (Stripe: `stripe.customers`, `stripe.charges`)
- Top-level convenience methods vs. resource-specific methods

**5. OpenAPI-Driven, Human-Polished**

- Generated from OpenAPI specs (consistency across languages)
- Hand-tuned for idiomatic patterns (Python generators, Go contexts)
- Custom methods for complex workflows (streaming, pagination)

### SDK Design Principles from Research

**1. Simplicity and Ease of Use (Top Priority)**

- Easy installation (single `npm install`, `pip install`)
- Intuitive API design (guide users to the most important methods)
- Clear abstractions (hide complexity, expose power when needed)

**2. Comprehensive Documentation**

- API reference (every method, parameter, return value)
- Tutorials (step-by-step for common workflows)
- Sample code (copy-paste ready examples)
- Embedded docs (TypeScript types, Python docstrings)

**3. Robust Error Handling**

- Meaningful error messages (what went wrong, why, how to fix)
- Typed error classes (differentiate by error type)
- Debugging support (logs, stack traces, request IDs)

**4. Performance and Size**

- Lightweight (tree-shakeable, minimal dependencies)
- Modular (import only what you need)
- Optimized (connection pooling, request batching)

**5. Backward Compatibility**

- Semantic versioning (breaking changes only in major versions)
- Deprecation warnings (with migration paths)
- Long-term support (LTS) versions

**6. Security by Default**

- HTTPS only (no HTTP fallback)
- Secure credential storage (environment variables, not hardcoded)
- Vulnerability scanning (regular security audits)

---

## SDK Architecture Taxonomy

### Architecture Pattern: Client → Resources → Methods

**Hierarchy:**

```
SDK Client (top-level)
  ├─ Configuration (API key, base URL, retries, timeout)
  ├─ Resources (logical grouping of related methods)
  │   ├─ Users Resource
  │   │   ├─ create()
  │   │   ├─ retrieve()
  │   │   ├─ update()
  │   │   ├─ delete()
  │   │   └─ list() (with pagination)
  │   └─ Payments Resource
  │       ├─ create()
  │       ├─ retrieve()
  │       └─ refund()
  └─ Top-Level Methods (convenience, common actions)
```

**Example (Stripe-style):**

```typescript
const stripe = new Stripe('sk_test_...')

// Resource-based
const customer = await stripe.customers.create({ email: 'user@example.com' })
const charge = await stripe.charges.create({ amount: 1000, customer: customer.id })

// Top-level convenience
const paymentIntent = await stripe.paymentIntents.create({ amount: 1000 })
```

**Example (AWS SDK v3 style):**

```typescript
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'

const client = new S3Client({ region: 'us-east-1' })
const command = new PutObjectCommand({ Bucket: 'my-bucket', Key: 'file.txt', Body: 'content' })
const result = await client.send(command)
```

**Trade-offs:**

- **Resource-Based (Stripe):** More intuitive, easier discovery, larger bundle size
- **Command-Based (AWS SDK v3):** Tree-shakeable, smaller bundles, more verbose

---

### Sync vs. Async API Design

#### Pattern 1: Async-Only (Modern JavaScript/TypeScript)

**When to Use:**

- Node.js >= 14 (native async/await support)
- Modern web applications (fetch API is async)
- Long-running operations (API calls are I/O-bound)

**Example:**

```typescript
// All methods return Promises
const customer = await stripe.customers.create({ email: 'user@example.com' })
const list = await stripe.customers.list({ limit: 10 })
```

**Benefits:**

- Non-blocking (doesn't freeze the event loop)
- Composable (easy to chain with `await`)
- Modern (async/await is standard in 2025)

---

#### Pattern 2: Dual Sync/Async Clients (Python)

**When to Use:**

- Python SDKs (async is opt-in, not default)
- Supporting both sync and async users
- Migration path from sync to async

**Example:**

```python
# Sync client
from stripe import Stripe
stripe = Stripe(api_key='sk_test_...')
customer = stripe.customers.create(email='user@example.com')

# Async client
from stripe import AsyncStripe
async_stripe = AsyncStripe(api_key='sk_test_...')
customer = await async_stripe.customers.create(email='user@example.com')
```

**Benefits:**

- Users choose sync or async based on their architecture
- No breaking changes (sync users don't need to refactor)
- Clear separation (different imports)

---

#### Pattern 3: Callback-Based (Legacy, Avoid in 2025)

**When to Use:**

- Legacy codebases (Node.js < 8)
- Only if backward compatibility is critical

**Example (Avoid):**

```javascript
stripe.customers.create({ email: 'user@example.com' }, (err, customer) => {
  if (err) throw err
  console.log(customer)
})
```

**Why Avoid:**

- Callback hell (nested callbacks are hard to read)
- Error handling is awkward (if (err) checks everywhere)
- Not composable (can't use with async/await)

---

### Authentication Patterns

#### Pattern 1: API Key in Constructor (Most Common)

**When to Use:**

- Simple authentication (single API key)
- No token refresh needed
- Key is long-lived

**TypeScript:**

```typescript
const client = new APIClient({ apiKey: process.env.API_KEY })
```

**Python:**

```python
client = APIClient(api_key=os.environ['API_KEY'])
```

**Go:**

```go
client := apiclient.New(os.Getenv("API_KEY"))
```

---

#### Pattern 2: OAuth Token Refresh (Complex Auth)

**When to Use:**

- OAuth 2.0 authentication
- Tokens expire (need refresh)
- User-based authentication (not service-to-service)

**TypeScript:**

```typescript
const client = new APIClient({
  clientId: 'client_id',
  clientSecret: 'client_secret',
  refreshToken: 'refresh_token',
  onTokenRefresh: (newToken) => {
    // Save new token to database
    console.log('Token refreshed:', newToken)
  }
})

// SDK automatically refreshes token before it expires
const data = await client.users.list()
```

**Python:**

```python
def on_token_refresh(new_token):
    # Save to database
    print(f"Token refreshed: {new_token}")

client = APIClient(
    client_id='client_id',
    client_secret='client_secret',
    refresh_token='refresh_token',
    on_token_refresh=on_token_refresh
)
```

---

#### Pattern 3: Bearer Token Injection

**When to Use:**

- Token provided per-request (not global)
- Multi-tenant applications (different token per user)

**TypeScript:**

```typescript
const client = new APIClient({ baseURL: 'https://api.example.com' })

// Inject token per-request
const data = await client.users.list({
  headers: { Authorization: `Bearer ${userToken}` }
})
```

---

### Retry and Backoff Strategies

#### Pattern 1: Exponential Backoff with Jitter (Best Practice)

**When to Use:**

- All SDKs (default behavior in 2025)
- Prevents thundering herd problem
- Balances fast retry with server recovery time

**Algorithm:**

```
retry_delay = base_delay * (2 ^ attempt) + random_jitter

Example:
Attempt 1: 1s + jitter (0-500ms) = 1-1.5s
Attempt 2: 2s + jitter (0-500ms) = 2-2.5s
Attempt 3: 4s + jitter (0-500ms) = 4-4.5s
```

**TypeScript Implementation:**

```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries: number
    baseDelay: number
    maxDelay: number
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

      const exponentialDelay = Math.min(
        options.baseDelay * Math.pow(2, attempt - 1),
        options.maxDelay
      )
      const jitter = Math.random() * 500 // 0-500ms jitter
      const delay = exponentialDelay + jitter

      console.log(`Retry attempt ${attempt} after ${delay}ms`)
      await sleep(delay)
    }
  }

  throw new Error('Max retries exceeded')
}

function isRetryable(error: any): boolean {
  // Retry on network errors, 5xx, and 429
  return (
    error.code === 'ECONNRESET' ||
    error.code === 'ETIMEDOUT' ||
    (error.status >= 500 && error.status < 600) ||
    error.status === 429
  )
}
```

---

#### Pattern 2: Rate Limit Handling (429 Response)

**When to Use:**

- API returns 429 Too Many Requests
- `Retry-After` header provided
- Need to respect server-side rate limits

**TypeScript:**

```typescript
if (error.status === 429) {
  const retryAfter = error.headers['retry-after']
  const delaySeconds = retryAfter ? parseInt(retryAfter) : 60

  console.log(`Rate limited. Retrying after ${delaySeconds}s`)
  await sleep(delaySeconds * 1000)
  return retryRequest()
}
```

**Python:**

```python
if error.status == 429:
    retry_after = int(error.headers.get('retry-after', 60))
    print(f"Rate limited. Retrying after {retry_after}s")
    time.sleep(retry_after)
    return retry_request()
```

---

### Error Handling Patterns

#### Pattern 1: Typed Error Hierarchy (Best Practice)

**When to Use:**

- All SDKs (essential for debugging)
- Users need to handle different errors differently
- Errors have common properties (request ID, status code)

**TypeScript:**

```typescript
// Base error class
class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public code: string,
    public requestId: string,
    public headers: Record<string, string>
  ) {
    super(message)
    this.name = 'APIError'
  }
}

// Specific error types
class AuthenticationError extends APIError {
  constructor(message: string, status: number, requestId: string, headers: Record<string, string>) {
    super(message, status, 'authentication_error', requestId, headers)
    this.name = 'AuthenticationError'
  }
}

class RateLimitError extends APIError {
  constructor(message: string, status: number, requestId: string, headers: Record<string, string>) {
    super(message, status, 'rate_limit_error', requestId, headers)
    this.name = 'RateLimitError'
  }

  get retryAfter(): number {
    return parseInt(this.headers['retry-after'] || '60')
  }
}

class InvalidRequestError extends APIError {
  constructor(
    message: string,
    status: number,
    requestId: string,
    headers: Record<string, string>,
    public param?: string
  ) {
    super(message, status, 'invalid_request_error', requestId, headers)
    this.name = 'InvalidRequestError'
  }
}

// Usage
try {
  const customer = await stripe.customers.create({ email: 'invalid' })
} catch (error) {
  if (error instanceof RateLimitError) {
    console.log(`Rate limited. Retry after ${error.retryAfter}s`)
    await sleep(error.retryAfter * 1000)
  } else if (error instanceof AuthenticationError) {
    console.error('Invalid API key')
  } else if (error instanceof InvalidRequestError) {
    console.error(`Invalid parameter: ${error.param}`)
  } else {
    throw error
  }
}
```

---

### Pagination Patterns

#### Pattern 1: Async Iterators (Modern TypeScript/Python)

**When to Use:**

- Node.js >= 10, Python >= 3.6
- Users want to iterate over all results
- Automatic page fetching (simplest UX)

**TypeScript:**

```typescript
// Async iterator
for await (const customer of stripe.customers.list({ limit: 100 })) {
  console.log(customer.id, customer.email)
}

// Or collect all (careful with memory)
const allCustomers = []
for await (const customer of stripe.customers.list()) {
  allCustomers.push(customer)
}
```

**Python:**

```python
# Async iterator
async for customer in stripe.customers.list(limit=100):
    print(customer.id, customer.email)

# Sync iterator
for customer in stripe.customers.list(limit=100):
    print(customer.id, customer.email)
```

---

#### Pattern 2: Manual Pagination (Explicit Control)

**When to Use:**

- Users need control over pagination
- Displaying page numbers in UI
- Cursor-based pagination (next token)

**TypeScript (Cursor-Based):**

```typescript
let hasMore = true
let cursor: string | undefined = undefined

while (hasMore) {
  const response = await client.users.list({ limit: 100, cursor })

  for (const user of response.data) {
    console.log(user.id)
  }

  cursor = response.nextCursor
  hasMore = response.hasMore
}
```

**Python (Offset-Based):**

```python
page = 1
while True:
    response = client.users.list(limit=100, page=page)

    for user in response.data:
        print(user.id)

    if not response.has_next_page:
        break

    page += 1
```

---

## Decision Frameworks

### Framework 1: Sync vs. Async API Design

**Decision Tree:**

```
START: Which language am I targeting?

Q1: JavaScript/TypeScript?
  → YES: Use async-only (Promises, async/await)
  → NO: Go to Q2

Q2: Python?
  → YES: Provide both sync and async clients
  → NO: Go to Q3

Q3: Go?
  → YES: Use sync methods (idiomatic Go)
  → NO: Go to Q4

Q4: Other language?
  → YES: Follow language conventions
```

**Examples:**

| Language | API Style | Rationale |
|----------|-----------|-----------|
| **TypeScript** | Async-only (Promises) | Non-blocking, composable with `await`, modern standard |
| **Python** | Dual (sync + async) | Async is opt-in, not default; support both use cases |
| **Go** | Sync with context.Context | Idiomatic Go uses blocking calls with context for cancellation |
| **Rust** | Async with futures | Async is zero-cost abstraction, but requires explicit runtime |

---

### Framework 2: When to Retry vs. Fail Fast

**Decision Matrix:**

| Error Type | Retry? | Rationale |
|------------|--------|-----------|
| **5xx Server Error** | ✅ Yes | Transient, server may recover |
| **429 Rate Limit** | ✅ Yes | Respect `Retry-After` header |
| **Network Timeout** | ✅ Yes | Network may recover |
| **Connection Reset** | ✅ Yes | Transient network issue |
| **4xx Client Error** | ❌ No | Invalid request, won't fix itself |
| **401 Unauthorized** | ❌ No | Invalid credentials, user must fix |
| **403 Forbidden** | ❌ No | Insufficient permissions |
| **404 Not Found** | ❌ No | Resource doesn't exist |

**Guiding Principles:**

1. **Retry transient errors:** Network issues, server overload, rate limits
2. **Fail fast on client errors:** Invalid parameters, authentication failures
3. **Add jitter:** Prevent thundering herd problem
4. **Max retries:** Limit to 3-5 attempts (avoid infinite loops)

---

### Framework 3: Resource Organization Strategy

**Option A: Resource-Based (Stripe, Twilio)**

**Structure:**

```typescript
client.customers.create()
client.customers.retrieve()
client.charges.create()
client.invoices.list()
```

**Pros:**

- Intuitive (matches API documentation)
- Easy discovery (autocomplete shows all methods)
- Clear namespacing (no method name conflicts)

**Cons:**

- Larger bundle size (all resources loaded)
- More code to maintain

**When to Use:**

- Small-to-medium API surface (<100 methods)
- Developer experience priority
- Not concerned with bundle size

---

**Option B: Command-Based (AWS SDK v3)**

**Structure:**

```typescript
import { S3Client, PutObjectCommand, GetObjectCommand } from '@aws-sdk/client-s3'

const client = new S3Client({ region: 'us-east-1' })
await client.send(new PutObjectCommand({ Bucket: '...', Key: '...' }))
await client.send(new GetObjectCommand({ Bucket: '...', Key: '...' }))
```

**Pros:**

- Tree-shakeable (import only what you need)
- Smaller bundle size
- Modular (each command is separate file)

**Cons:**

- More verbose (create command, then send)
- Less intuitive (extra step)

**When to Use:**

- Large API surface (>100 methods)
- Bundle size critical (browser SDKs)
- Modular design priority

---

## TypeScript SDK Patterns

### Pattern 1: Modern Async SDK with Streaming

**Full Example:**

```typescript
import { EventEmitter } from 'events'

// Error hierarchy
class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public code: string,
    public requestId: string
  ) {
    super(message)
    this.name = 'APIError'
  }
}

class RateLimitError extends APIError {
  constructor(message: string, requestId: string, public retryAfter: number) {
    super(message, 429, 'rate_limit_error', requestId)
    this.name = 'RateLimitError'
  }
}

// Configuration
interface ClientOptions {
  apiKey: string
  baseURL?: string
  maxRetries?: number
  timeout?: number
}

// Client
class APIClient {
  private apiKey: string
  private baseURL: string
  private maxRetries: number
  private timeout: number

  constructor(options: ClientOptions) {
    this.apiKey = options.apiKey
    this.baseURL = options.baseURL || 'https://api.example.com'
    this.maxRetries = options.maxRetries ?? 3
    this.timeout = options.timeout ?? 30000
  }

  // Resource namespaces
  get users() {
    return new UsersResource(this)
  }

  get posts() {
    return new PostsResource(this)
  }

  // Core request method with retry
  async request<T>(
    method: string,
    path: string,
    options?: {
      body?: any
      query?: Record<string, string>
      headers?: Record<string, string>
    }
  ): Promise<T> {
    let attempt = 0

    while (attempt <= this.maxRetries) {
      try {
        const url = new URL(path, this.baseURL)
        if (options?.query) {
          Object.entries(options.query).forEach(([key, value]) => {
            url.searchParams.append(key, value)
          })
        }

        const response = await fetch(url.toString(), {
          method,
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json',
            ...options?.headers
          },
          body: options?.body ? JSON.stringify(options.body) : undefined,
          signal: AbortSignal.timeout(this.timeout)
        })

        const requestId = response.headers.get('x-request-id') || 'unknown'

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}))

          if (response.status === 429) {
            const retryAfter = parseInt(response.headers.get('retry-after') || '60')
            throw new RateLimitError(
              errorData.message || 'Rate limit exceeded',
              requestId,
              retryAfter
            )
          }

          throw new APIError(
            errorData.message || `HTTP ${response.status}`,
            response.status,
            errorData.code || 'unknown_error',
            requestId
          )
        }

        return await response.json()
      } catch (error) {
        attempt++

        if (attempt > this.maxRetries || !this.isRetryable(error)) {
          throw error
        }

        const delay = this.calculateBackoff(attempt)
        console.log(`Retry attempt ${attempt} after ${delay}ms`)
        await this.sleep(delay)
      }
    }

    throw new Error('Max retries exceeded')
  }

  // Streaming with async iterator
  async *stream(
    method: string,
    path: string,
    options?: { body?: any; query?: Record<string, string> }
  ): AsyncGenerator<any, void, unknown> {
    const url = new URL(path, this.baseURL)
    if (options?.query) {
      Object.entries(options.query).forEach(([key, value]) => {
        url.searchParams.append(key, value)
      })
    }

    const response = await fetch(url.toString(), {
      method,
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
      },
      body: options?.body ? JSON.stringify(options.body) : undefined
    })

    if (!response.ok) {
      throw new APIError(
        `HTTP ${response.status}`,
        response.status,
        'stream_error',
        response.headers.get('x-request-id') || 'unknown'
      )
    }

    const reader = response.body!.getReader()
    const decoder = new TextDecoder()

    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n').filter(line => line.trim())

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') return

            try {
              yield JSON.parse(data)
            } catch {
              // Skip malformed JSON
            }
          }
        }
      }
    } finally {
      reader.releaseLock()
    }
  }

  private isRetryable(error: any): boolean {
    return (
      error instanceof RateLimitError ||
      error.code === 'ECONNRESET' ||
      error.code === 'ETIMEDOUT' ||
      (error.status >= 500 && error.status < 600)
    )
  }

  private calculateBackoff(attempt: number): number {
    const baseDelay = 1000 // 1 second
    const maxDelay = 10000 // 10 seconds
    const exponential = Math.min(baseDelay * Math.pow(2, attempt - 1), maxDelay)
    const jitter = Math.random() * 500 // 0-500ms jitter
    return exponential + jitter
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
}

// Resource classes
class UsersResource {
  constructor(private client: APIClient) {}

  async create(data: { name: string; email: string }) {
    return this.client.request('POST', '/users', { body: data })
  }

  async retrieve(id: string) {
    return this.client.request('GET', `/users/${id}`)
  }

  async update(id: string, data: Partial<{ name: string; email: string }>) {
    return this.client.request('PATCH', `/users/${id}`, { body: data })
  }

  async delete(id: string) {
    return this.client.request('DELETE', `/users/${id}`)
  }

  // Pagination with async iterator
  async *list(options?: { limit?: number }): AsyncGenerator<any, void, unknown> {
    let cursor: string | undefined = undefined

    while (true) {
      const response: any = await this.client.request('GET', '/users', {
        query: {
          limit: String(options?.limit || 100),
          ...(cursor ? { cursor } : {})
        }
      })

      for (const user of response.data) {
        yield user
      }

      if (!response.has_more) break
      cursor = response.next_cursor
    }
  }
}

class PostsResource {
  constructor(private client: APIClient) {}

  async create(data: { title: string; content: string }) {
    return this.client.request('POST', '/posts', { body: data })
  }

  async retrieve(id: string) {
    return this.client.request('GET', `/posts/${id}`)
  }

  // Streaming example (e.g., for AI-generated content)
  async *stream(data: { prompt: string }): AsyncGenerator<string, void, unknown> {
    for await (const chunk of this.client.stream('POST', '/posts/generate', { body: data })) {
      if (chunk.content) {
        yield chunk.content
      }
    }
  }
}

// Usage examples
async function main() {
  const client = new APIClient({
    apiKey: process.env.API_KEY!,
    maxRetries: 3,
    timeout: 30000
  })

  try {
    // Create user
    const user = await client.users.create({
      name: 'Alice',
      email: 'alice@example.com'
    })
    console.log('Created user:', user)

    // List all users with pagination
    console.log('All users:')
    for await (const user of client.users.list({ limit: 10 })) {
      console.log('-', user.name, user.email)
    }

    // Stream AI-generated content
    console.log('Generating post:')
    for await (const chunk of client.posts.stream({ prompt: 'Write about TypeScript' })) {
      process.stdout.write(chunk)
    }
    console.log('\n')

  } catch (error) {
    if (error instanceof RateLimitError) {
      console.error(`Rate limited. Retry after ${error.retryAfter}s`)
    } else if (error instanceof APIError) {
      console.error(`API Error: ${error.message} (${error.code})`)
      console.error(`Request ID: ${error.requestId}`)
    } else {
      throw error
    }
  }
}

main()
```

---

## Python SDK Patterns

### Pattern 1: Dual Sync/Async with Context Managers

**Full Example:**

```python
import os
import time
import asyncio
from typing import Any, Dict, Optional, AsyncIterator, Iterator
from contextlib import contextmanager, asynccontextmanager
import httpx

# Error hierarchy
class APIError(Exception):
    def __init__(self, message: str, status: int, code: str, request_id: str):
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.request_id = request_id

class RateLimitError(APIError):
    def __init__(self, message: str, request_id: str, retry_after: int):
        super().__init__(message, 429, 'rate_limit_error', request_id)
        self.retry_after = retry_after

class AuthenticationError(APIError):
    def __init__(self, message: str, request_id: str):
        super().__init__(message, 401, 'authentication_error', request_id)

# Sync client
class APIClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.example.com",
        max_retries: int = 3,
        timeout: int = 30
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.max_retries = max_retries
        self.timeout = timeout
        self._client = httpx.Client(timeout=timeout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.close()

    @property
    def users(self):
        return UsersResource(self)

    @property
    def posts(self):
        return PostsResource(self)

    def request(
        self,
        method: str,
        path: str,
        body: Optional[Dict[str, Any]] = None,
        query: Optional[Dict[str, str]] = None
    ) -> Any:
        attempt = 0

        while attempt <= self.max_retries:
            try:
                response = self._client.request(
                    method=method,
                    url=f"{self.base_url}{path}",
                    json=body,
                    params=query,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    }
                )

                request_id = response.headers.get('x-request-id', 'unknown')

                if response.status_code == 429:
                    retry_after = int(response.headers.get('retry-after', 60))
                    raise RateLimitError(
                        response.json().get('message', 'Rate limit exceeded'),
                        request_id,
                        retry_after
                    )

                if response.status_code == 401:
                    raise AuthenticationError(
                        response.json().get('message', 'Unauthorized'),
                        request_id
                    )

                if not response.is_success:
                    error_data = response.json()
                    raise APIError(
                        error_data.get('message', f"HTTP {response.status_code}"),
                        response.status_code,
                        error_data.get('code', 'unknown_error'),
                        request_id
                    )

                return response.json()

            except (httpx.TimeoutException, httpx.NetworkError) as e:
                attempt += 1
                if attempt > self.max_retries:
                    raise APIError(str(e), 0, 'network_error', 'unknown')

                delay = self._calculate_backoff(attempt)
                print(f"Retry attempt {attempt} after {delay}ms")
                time.sleep(delay / 1000)

        raise APIError('Max retries exceeded', 0, 'max_retries', 'unknown')

    def _calculate_backoff(self, attempt: int) -> float:
        import random
        base_delay = 1000  # 1 second
        max_delay = 10000  # 10 seconds
        exponential = min(base_delay * (2 ** (attempt - 1)), max_delay)
        jitter = random.random() * 500  # 0-500ms jitter
        return exponential + jitter

    def close(self):
        self._client.close()

# Async client
class AsyncAPIClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.example.com",
        max_retries: int = 3,
        timeout: int = 30
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.max_retries = max_retries
        self.timeout = timeout
        self._client = httpx.AsyncClient(timeout=timeout)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()

    @property
    def users(self):
        return AsyncUsersResource(self)

    @property
    def posts(self):
        return AsyncPostsResource(self)

    async def request(
        self,
        method: str,
        path: str,
        body: Optional[Dict[str, Any]] = None,
        query: Optional[Dict[str, str]] = None
    ) -> Any:
        attempt = 0

        while attempt <= self.max_retries:
            try:
                response = await self._client.request(
                    method=method,
                    url=f"{self.base_url}{path}",
                    json=body,
                    params=query,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    }
                )

                request_id = response.headers.get('x-request-id', 'unknown')

                if response.status_code == 429:
                    retry_after = int(response.headers.get('retry-after', 60))
                    raise RateLimitError(
                        response.json().get('message', 'Rate limit exceeded'),
                        request_id,
                        retry_after
                    )

                if not response.is_success:
                    error_data = response.json()
                    raise APIError(
                        error_data.get('message', f"HTTP {response.status_code}"),
                        response.status_code,
                        error_data.get('code', 'unknown_error'),
                        request_id
                    )

                return response.json()

            except (httpx.TimeoutException, httpx.NetworkError):
                attempt += 1
                if attempt > self.max_retries:
                    raise APIError('Network error', 0, 'network_error', 'unknown')

                delay = self._calculate_backoff(attempt)
                print(f"Retry attempt {attempt} after {delay}ms")
                await asyncio.sleep(delay / 1000)

        raise APIError('Max retries exceeded', 0, 'max_retries', 'unknown')

    def _calculate_backoff(self, attempt: int) -> float:
        import random
        base_delay = 1000
        max_delay = 10000
        exponential = min(base_delay * (2 ** (attempt - 1)), max_delay)
        jitter = random.random() * 500
        return exponential + jitter

    async def close(self):
        await self._client.aclose()

# Sync resource
class UsersResource:
    def __init__(self, client: APIClient):
        self._client = client

    def create(self, name: str, email: str) -> Dict[str, Any]:
        return self._client.request('POST', '/users', body={'name': name, 'email': email})

    def retrieve(self, user_id: str) -> Dict[str, Any]:
        return self._client.request('GET', f'/users/{user_id}')

    def update(self, user_id: str, **kwargs) -> Dict[str, Any]:
        return self._client.request('PATCH', f'/users/{user_id}', body=kwargs)

    def delete(self, user_id: str) -> Dict[str, Any]:
        return self._client.request('DELETE', f'/users/{user_id}')

    def list(self, limit: int = 100) -> Iterator[Dict[str, Any]]:
        cursor = None
        while True:
            query = {'limit': str(limit)}
            if cursor:
                query['cursor'] = cursor

            response = self._client.request('GET', '/users', query=query)

            for user in response['data']:
                yield user

            if not response.get('has_more'):
                break
            cursor = response.get('next_cursor')

# Async resource
class AsyncUsersResource:
    def __init__(self, client: AsyncAPIClient):
        self._client = client

    async def create(self, name: str, email: str) -> Dict[str, Any]:
        return await self._client.request('POST', '/users', body={'name': name, 'email': email})

    async def retrieve(self, user_id: str) -> Dict[str, Any]:
        return await self._client.request('GET', f'/users/{user_id}')

    async def update(self, user_id: str, **kwargs) -> Dict[str, Any]:
        return await self._client.request('PATCH', f'/users/{user_id}', body=kwargs)

    async def delete(self, user_id: str) -> Dict[str, Any]:
        return await self._client.request('DELETE', f'/users/{user_id}')

    async def list(self, limit: int = 100) -> AsyncIterator[Dict[str, Any]]:
        cursor = None
        while True:
            query = {'limit': str(limit)}
            if cursor:
                query['cursor'] = cursor

            response = await self._client.request('GET', '/users', query=query)

            for user in response['data']:
                yield user

            if not response.get('has_more'):
                break
            cursor = response.get('next_cursor')

class PostsResource:
    def __init__(self, client: APIClient):
        self._client = client

    def create(self, title: str, content: str) -> Dict[str, Any]:
        return self._client.request('POST', '/posts', body={'title': title, 'content': content})

class AsyncPostsResource:
    def __init__(self, client: AsyncAPIClient):
        self._client = client

    async def create(self, title: str, content: str) -> Dict[str, Any]:
        return await self._client.request('POST', '/posts', body={'title': title, 'content': content})

# Usage examples
def sync_example():
    # Context manager ensures cleanup
    with APIClient(api_key=os.environ['API_KEY']) as client:
        try:
            # Create user
            user = client.users.create(name='Alice', email='alice@example.com')
            print(f"Created user: {user}")

            # List all users with pagination
            print("All users:")
            for user in client.users.list(limit=10):
                print(f"- {user['name']} ({user['email']})")

        except RateLimitError as e:
            print(f"Rate limited. Retry after {e.retry_after}s")
        except APIError as e:
            print(f"API Error: {e.message} ({e.code})")
            print(f"Request ID: {e.request_id}")

async def async_example():
    async with AsyncAPIClient(api_key=os.environ['API_KEY']) as client:
        try:
            # Create user
            user = await client.users.create(name='Bob', email='bob@example.com')
            print(f"Created user: {user}")

            # List all users with pagination
            print("All users:")
            async for user in client.users.list(limit=10):
                print(f"- {user['name']} ({user['email']})")

        except RateLimitError as e:
            print(f"Rate limited. Retry after {e.retry_after}s")
        except APIError as e:
            print(f"API Error: {e.message} ({e.code})")

if __name__ == '__main__':
    # Sync usage
    sync_example()

    # Async usage
    asyncio.run(async_example())
```

---

## Go SDK Patterns

### Pattern 1: Idiomatic Go with Context

**Full Example:**

```go
package apiclient

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"math"
	"math/rand"
	"net/http"
	"strconv"
	"time"
)

// Error types
type APIError struct {
	Message   string
	Status    int
	Code      string
	RequestID string
}

func (e *APIError) Error() string {
	return fmt.Sprintf("API error %d: %s (code: %s, request_id: %s)",
		e.Status, e.Message, e.Code, e.RequestID)
}

type RateLimitError struct {
	APIError
	RetryAfter int
}

type AuthenticationError struct {
	APIError
}

// Client configuration
type ClientOptions struct {
	APIKey     string
	BaseURL    string
	MaxRetries int
	Timeout    time.Duration
}

// Client
type Client struct {
	apiKey     string
	baseURL    string
	maxRetries int
	httpClient *http.Client
}

func New(apiKey string) *Client {
	return NewWithOptions(ClientOptions{
		APIKey:     apiKey,
		BaseURL:    "https://api.example.com",
		MaxRetries: 3,
		Timeout:    30 * time.Second,
	})
}

func NewWithOptions(opts ClientOptions) *Client {
	if opts.BaseURL == "" {
		opts.BaseURL = "https://api.example.com"
	}
	if opts.MaxRetries == 0 {
		opts.MaxRetries = 3
	}
	if opts.Timeout == 0 {
		opts.Timeout = 30 * time.Second
	}

	return &Client{
		apiKey:     opts.APIKey,
		baseURL:    opts.BaseURL,
		maxRetries: opts.MaxRetries,
		httpClient: &http.Client{
			Timeout: opts.Timeout,
		},
	}
}

// Resource accessors
func (c *Client) Users() *UsersResource {
	return &UsersResource{client: c}
}

func (c *Client) Posts() *PostsResource {
	return &PostsResource{client: c}
}

// Core request method with retry
func (c *Client) request(
	ctx context.Context,
	method string,
	path string,
	body interface{},
) (interface{}, error) {
	var lastErr error

	for attempt := 0; attempt <= c.maxRetries; attempt++ {
		result, err := c.doRequest(ctx, method, path, body)
		if err == nil {
			return result, nil
		}

		lastErr = err

		// Don't retry on non-retryable errors
		if !isRetryable(err) {
			return nil, err
		}

		// Check if we've exhausted retries
		if attempt >= c.maxRetries {
			break
		}

		// Calculate backoff delay
		delay := calculateBackoff(attempt + 1)
		fmt.Printf("Retry attempt %d after %v\n", attempt+1, delay)

		// Wait with context cancellation support
		timer := time.NewTimer(delay)
		select {
		case <-ctx.Done():
			timer.Stop()
			return nil, ctx.Err()
		case <-timer.C:
			// Continue to next retry
		}
	}

	return nil, lastErr
}

func (c *Client) doRequest(
	ctx context.Context,
	method string,
	path string,
	body interface{},
) (interface{}, error) {
	url := c.baseURL + path

	var bodyReader io.Reader
	if body != nil {
		bodyBytes, err := json.Marshal(body)
		if err != nil {
			return nil, fmt.Errorf("marshal body: %w", err)
		}
		bodyReader = bytes.NewReader(bodyBytes)
	}

	req, err := http.NewRequestWithContext(ctx, method, url, bodyReader)
	if err != nil {
		return nil, fmt.Errorf("create request: %w", err)
	}

	req.Header.Set("Authorization", "Bearer "+c.apiKey)
	req.Header.Set("Content-Type", "application/json")

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("do request: %w", err)
	}
	defer resp.Body.Close()

	requestID := resp.Header.Get("X-Request-ID")
	if requestID == "" {
		requestID = "unknown"
	}

	if resp.StatusCode == 429 {
		retryAfter, _ := strconv.Atoi(resp.Header.Get("Retry-After"))
		if retryAfter == 0 {
			retryAfter = 60
		}

		var errData struct {
			Message string `json:"message"`
		}
		json.NewDecoder(resp.Body).Decode(&errData)

		return nil, &RateLimitError{
			APIError: APIError{
				Message:   errData.Message,
				Status:    429,
				Code:      "rate_limit_error",
				RequestID: requestID,
			},
			RetryAfter: retryAfter,
		}
	}

	if resp.StatusCode == 401 {
		var errData struct {
			Message string `json:"message"`
		}
		json.NewDecoder(resp.Body).Decode(&errData)

		return nil, &AuthenticationError{
			APIError: APIError{
				Message:   errData.Message,
				Status:    401,
				Code:      "authentication_error",
				RequestID: requestID,
			},
		}
	}

	if resp.StatusCode >= 400 {
		var errData struct {
			Message string `json:"message"`
			Code    string `json:"code"`
		}
		json.NewDecoder(resp.Body).Decode(&errData)

		return nil, &APIError{
			Message:   errData.Message,
			Status:    resp.StatusCode,
			Code:      errData.Code,
			RequestID: requestID,
		}
	}

	var result interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("decode response: %w", err)
	}

	return result, nil
}

func isRetryable(err error) bool {
	switch e := err.(type) {
	case *RateLimitError:
		return true
	case *APIError:
		return e.Status >= 500 && e.Status < 600
	default:
		return false
	}
}

func calculateBackoff(attempt int) time.Duration {
	baseDelay := 1 * time.Second
	maxDelay := 10 * time.Second

	exponential := time.Duration(math.Min(
		float64(baseDelay)*math.Pow(2, float64(attempt-1)),
		float64(maxDelay),
	))

	jitter := time.Duration(rand.Intn(500)) * time.Millisecond
	return exponential + jitter
}

// User types
type User struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

type CreateUserRequest struct {
	Name  string `json:"name"`
	Email string `json:"email"`
}

type ListUsersResponse struct {
	Data       []User `json:"data"`
	HasMore    bool   `json:"has_more"`
	NextCursor string `json:"next_cursor"`
}

// Users resource
type UsersResource struct {
	client *Client
}

func (r *UsersResource) Create(ctx context.Context, req CreateUserRequest) (*User, error) {
	result, err := r.client.request(ctx, "POST", "/users", req)
	if err != nil {
		return nil, err
	}

	var user User
	data, _ := json.Marshal(result)
	json.Unmarshal(data, &user)
	return &user, nil
}

func (r *UsersResource) Retrieve(ctx context.Context, id string) (*User, error) {
	result, err := r.client.request(ctx, "GET", "/users/"+id, nil)
	if err != nil {
		return nil, err
	}

	var user User
	data, _ := json.Marshal(result)
	json.Unmarshal(data, &user)
	return &user, nil
}

func (r *UsersResource) Update(ctx context.Context, id string, updates map[string]interface{}) (*User, error) {
	result, err := r.client.request(ctx, "PATCH", "/users/"+id, updates)
	if err != nil {
		return nil, err
	}

	var user User
	data, _ := json.Marshal(result)
	json.Unmarshal(data, &user)
	return &user, nil
}

func (r *UsersResource) Delete(ctx context.Context, id string) error {
	_, err := r.client.request(ctx, "DELETE", "/users/"+id, nil)
	return err
}

// List with pagination (channel-based iterator)
func (r *UsersResource) List(ctx context.Context, limit int) (<-chan User, <-chan error) {
	userCh := make(chan User)
	errCh := make(chan error, 1)

	go func() {
		defer close(userCh)
		defer close(errCh)

		cursor := ""
		for {
			// Build query parameters
			query := fmt.Sprintf("?limit=%d", limit)
			if cursor != "" {
				query += "&cursor=" + cursor
			}

			result, err := r.client.request(ctx, "GET", "/users"+query, nil)
			if err != nil {
				errCh <- err
				return
			}

			var response ListUsersResponse
			data, _ := json.Marshal(result)
			json.Unmarshal(data, &response)

			for _, user := range response.Data {
				select {
				case <-ctx.Done():
					errCh <- ctx.Err()
					return
				case userCh <- user:
				}
			}

			if !response.HasMore {
				break
			}
			cursor = response.NextCursor
		}
	}()

	return userCh, errCh
}

// Posts resource
type PostsResource struct {
	client *Client
}

type Post struct {
	ID      string `json:"id"`
	Title   string `json:"title"`
	Content string `json:"content"`
}

type CreatePostRequest struct {
	Title   string `json:"title"`
	Content string `json:"content"`
}

func (r *PostsResource) Create(ctx context.Context, req CreatePostRequest) (*Post, error) {
	result, err := r.client.request(ctx, "POST", "/posts", req)
	if err != nil {
		return nil, err
	}

	var post Post
	data, _ := json.Marshal(result)
	json.Unmarshal(data, &post)
	return &post, nil
}

// Usage example
func Example() {
	client := New("api_key_here")

	ctx := context.Background()

	// Create user
	user, err := client.Users().Create(ctx, CreateUserRequest{
		Name:  "Alice",
		Email: "alice@example.com",
	})
	if err != nil {
		if rateLimitErr, ok := err.(*RateLimitError); ok {
			fmt.Printf("Rate limited. Retry after %d seconds\n", rateLimitErr.RetryAfter)
		} else {
			fmt.Printf("Error: %v\n", err)
		}
		return
	}
	fmt.Printf("Created user: %s (%s)\n", user.Name, user.Email)

	// List users with pagination
	fmt.Println("All users:")
	userCh, errCh := client.Users().List(ctx, 10)
	for user := range userCh {
		fmt.Printf("- %s (%s)\n", user.Name, user.Email)
	}

	// Check for errors
	if err := <-errCh; err != nil {
		fmt.Printf("Error listing users: %v\n", err)
	}
}
```

---

## Cross-Cutting Patterns

### Pattern 1: Idempotency Keys

**Why:** Prevent duplicate operations when retrying requests (e.g., duplicate charges)

**TypeScript:**

```typescript
import { randomUUID } from 'crypto'

class APIClient {
  async request(method: string, path: string, options?: any) {
    // Add idempotency key for POST/PATCH/PUT
    if (['POST', 'PATCH', 'PUT'].includes(method.toUpperCase())) {
      options = options || {}
      options.headers = options.headers || {}
      options.headers['Idempotency-Key'] = options.idempotencyKey || randomUUID()
    }

    // ... make request
  }
}

// Usage
await client.charges.create(
  { amount: 1000, currency: 'usd' },
  { idempotencyKey: 'charge_abc123' } // Custom key
)
```

**Python:**

```python
import uuid

class APIClient:
    def request(self, method: str, path: str, body=None, idempotency_key=None):
        headers = {'Authorization': f'Bearer {self.api_key}'}

        if method.upper() in ['POST', 'PATCH', 'PUT']:
            headers['Idempotency-Key'] = idempotency_key or str(uuid.uuid4())

        # ... make request
```

---

### Pattern 2: Request/Response Interceptors

**Why:** Add logging, metrics, auth refresh, custom headers globally

**TypeScript:**

```typescript
type Interceptor = {
  request?: (config: RequestConfig) => RequestConfig | Promise<RequestConfig>
  response?: (response: Response) => Response | Promise<Response>
  error?: (error: Error) => Error | Promise<Error>
}

class APIClient {
  private interceptors: Interceptor[] = []

  use(interceptor: Interceptor) {
    this.interceptors.push(interceptor)
  }

  async request(method: string, path: string, options?: any) {
    let config = { method, path, ...options }

    // Request interceptors
    for (const interceptor of this.interceptors) {
      if (interceptor.request) {
        config = await interceptor.request(config)
      }
    }

    try {
      let response = await this.doRequest(config)

      // Response interceptors
      for (const interceptor of this.interceptors) {
        if (interceptor.response) {
          response = await interceptor.response(response)
        }
      }

      return response
    } catch (error) {
      // Error interceptors
      for (const interceptor of this.interceptors) {
        if (interceptor.error) {
          error = await interceptor.error(error)
        }
      }
      throw error
    }
  }
}

// Usage: Logging interceptor
client.use({
  request: (config) => {
    console.log(`→ ${config.method} ${config.path}`)
    return config
  },
  response: (response) => {
    console.log(`← ${response.status}`)
    return response
  },
  error: (error) => {
    console.error(`✗ ${error.message}`)
    return error
  }
})
```

---

### Pattern 3: Versioning and Deprecation

**Strategy:**

1. **Semantic Versioning (SemVer):**
   - `1.0.0` → `1.1.0` (new features, backward compatible)
   - `1.1.0` → `2.0.0` (breaking changes)
   - `1.0.0` → `1.0.1` (bug fixes)

2. **Deprecation Warnings:**

```typescript
function deprecated(message: string, since: string) {
  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value

    descriptor.value = function (...args: any[]) {
      console.warn(
        `[DEPRECATED] ${propertyKey} is deprecated since ${since}. ${message}`
      )
      return originalMethod.apply(this, args)
    }

    return descriptor
  }
}

class UsersResource {
  @deprecated('Use users.list() instead', 'v2.0.0')
  async getAll() {
    return this.list()
  }

  async list() {
    // New method
  }
}
```

3. **API Version Pinning:**

```typescript
const client = new APIClient({
  apiKey: 'sk_test_...',
  apiVersion: '2025-01-01' // Pin to specific API version
})
```

---

## Library Recommendations

### Research Summary

**Research Date:** December 3, 2025
**Libraries Evaluated:** 30+ SDKs (AWS, Stripe, OpenAI, Twilio, Anthropic)
**Research Tools:** Google Search Grounding, Context7, Official documentation

---

### Best-in-Class SDK Examples (2025)

#### **1. AWS SDK for JavaScript v3**

**Library:** `/aws/aws-sdk-js-v3`
**Trust Score:** 85.2/100 (Context7)
**Code Snippets:** 10,626+

**Why Study AWS SDK v3:**

- **Modular Architecture:** Tree-shakeable, import only what you need
- **Middleware System:** Request/response interceptors for auth, retry, logging
- **Automatic Retry:** Configurable retry strategy with exponential backoff
- **Paginator Helpers:** Async iterators for pagination
- **Command Pattern:** Separation of client and commands

**Key Patterns:**

```typescript
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'

const client = new S3Client({
  region: 'us-east-1',
  maxAttempts: 5, // Retry configuration
})

const command = new PutObjectCommand({ Bucket: 'my-bucket', Key: 'file.txt' })
const result = await client.send(command)
```

---

#### **2. Stripe Node.js SDK**

**Library:** `/stripe/stripe-node`
**Trust Score:** 91.6/100 (Context7)
**Code Snippets:** 140+

**Why Study Stripe SDK:**

- **Resource-Based Organization:** Intuitive API (`stripe.customers.create()`)
- **Typed Error Hierarchy:** 8+ error types with detailed metadata
- **Automatic Retry:** Configurable network retries with idempotency keys
- **Pagination:** Async iterators for listing resources
- **Developer Experience:** Best-in-class DX, widely praised

**Key Patterns:**

```typescript
const stripe = new Stripe('sk_test_...', {
  maxNetworkRetries: 3,
  timeout: 30000
})

// Error handling with typed errors
try {
  const charge = await stripe.charges.create({ amount: 1000 })
} catch (err) {
  if (err instanceof Stripe.errors.StripeCardError) {
    console.log('Card declined:', err.decline_code)
  } else if (err instanceof Stripe.errors.StripeRateLimitError) {
    console.log('Rate limited')
  }
}
```

---

#### **3. OpenAI Node.js SDK**

**Library:** `/openai/openai-node`
**Trust Score:** 85.2/100 (Context7)
**Code Snippets:** 355+

**Why Study OpenAI SDK:**

- **Streaming-First:** Async iterators for streaming responses
- **Typed Errors:** Rich error metadata (request ID, status, retry-after)
- **Event-Based Streaming:** Runner helpers with event handlers
- **Automatic Retry:** Configurable retry logic
- **Modern TypeScript:** Excellent type inference

**Key Patterns:**

```typescript
const openai = new OpenAI({ maxRetries: 5 })

// Streaming with async iterator
const stream = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: 'Hello' }],
  stream: true,
})

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content || '')
}

// Error handling
try {
  await openai.chat.completions.create({ ... })
} catch (error) {
  if (error instanceof OpenAI.RateLimitError) {
    const retryAfter = error.headers?.['retry-after']
    console.log(`Retry after ${retryAfter}s`)
  }
}
```

---

### Python SDK Examples

#### **4. Boto3 (AWS SDK for Python)**

**Library:** `/boto/boto3`
**Trust Score:** 83.2/100 (Context7)
**Code Snippets:** 445+

**Why Study Boto3:**

- **Pythonic API:** Follows Python conventions
- **Resource vs. Client:** High-level resources + low-level clients
- **Pagination:** Paginator objects for automatic pagination
- **Waiter Objects:** Wait for resource state changes

---

### Go SDK Examples

#### **5. AWS SDK for Go v2**

**Library:** `/aws/aws-sdk-go-v2`
**Trust Score:** 59.6/100 (Context7)
**Code Snippets:** 25+

**Why Study AWS SDK Go:**

- **Context.Context:** Idiomatic Go context handling
- **Middleware:** Request/response interceptors
- **Modular:** Import only needed services

---

## Skill Structure Design

### Skill File Organization

```
sdk-design/
├── SKILL.md                          # Main skill file (<500 lines)
├── references/
│   ├── architecture-patterns.md      # Client/resource/method organization
│   ├── authentication.md             # API keys, OAuth, token refresh
│   ├── retry-backoff.md              # Exponential backoff, jitter, rate limits
│   ├── error-handling.md             # Typed errors, error hierarchies
│   ├── pagination.md                 # Async iterators, cursors, manual pagination
│   ├── versioning.md                 # SemVer, deprecation, API version pinning
│   └── testing-sdks.md               # Testing SDK code, mocking, fixtures
├── examples/
│   ├── typescript/
│   │   ├── basic-client.ts           # Simple async SDK
│   │   ├── advanced-client.ts        # Retry, errors, streaming
│   │   ├── resource-based.ts         # Stripe-style resources
│   │   └── command-based.ts          # AWS SDK v3 style
│   ├── python/
│   │   ├── sync-client.py            # Sync client with retries
│   │   ├── async-client.py           # Async client
│   │   ├── dual-client.py            # Both sync and async
│   │   └── pagination.py             # Generators for pagination
│   └── go/
│       ├── basic-client.go           # Simple Go client
│       ├── context-client.go         # Context.Context patterns
│       └── channel-pagination.go     # Channel-based pagination
├── scripts/
│   └── validate-sdk-design.sh        # Check SDK design patterns
└── assets/
    └── sdk-architecture.png          # Diagrams
```

---

### SKILL.md Structure (Main File)

**Sections (Target: ~450 lines):**

1. **Frontmatter** (YAML)
2. **Purpose** (2-3 paragraphs)
3. **SDK Architecture Fundamentals** (~80 lines)
   - Client → Resources → Methods
   - Sync vs. Async decision tree
4. **Core Patterns** (~120 lines)
   - Authentication (API keys, OAuth)
   - Retry and backoff (exponential + jitter)
   - Error handling (typed errors)
   - Pagination (async iterators)
5. **Language-Specific Quick Starts** (~150 lines)
   - TypeScript (Promise-based)
   - Python (sync + async)
   - Go (context.Context)
6. **Real-World Examples** (~80 lines)
   - Stripe-style (resource-based)
   - AWS SDK v3 (command-based)
   - OpenAI (streaming)
7. **Reference Links** (~20 lines)

---

## Integration Points

### Integration with Existing Skills

#### 1. **api-patterns** Skill

- SDK design complements API design
- API returns 429 → SDK implements retry
- API returns typed errors → SDK creates error hierarchy

#### 2. **building-clis** Skill

- CLI wraps SDK for command-line access
- CLI handles authentication → passes to SDK
- CLI displays progress → SDK streams responses

#### 3. **testing-strategies** Skill

- Testing SDKs requires mocking HTTP requests
- Testing retry logic with artificial failures
- Integration tests for real API calls

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)

- [x] Complete init.md
- [ ] Create SKILL.md main file
- [ ] Write references/architecture-patterns.md
- [ ] Write references/authentication.md

### Phase 2: TypeScript Examples (Week 2)

- [ ] Create examples/typescript/basic-client.ts
- [ ] Create examples/typescript/advanced-client.ts
- [ ] Create examples/typescript/resource-based.ts
- [ ] Write references/retry-backoff.md

### Phase 3: Python Examples (Week 3)

- [ ] Create examples/python/sync-client.py
- [ ] Create examples/python/async-client.py
- [ ] Create examples/python/dual-client.py
- [ ] Write references/error-handling.md

### Phase 4: Go Examples (Week 4)

- [ ] Create examples/go/basic-client.go
- [ ] Create examples/go/context-client.go
- [ ] Create examples/go/channel-pagination.go
- [ ] Write references/pagination.md

### Phase 5: Documentation and Polish (Week 5)

- [ ] Write references/versioning.md
- [ ] Write references/testing-sdks.md
- [ ] Create validation script
- [ ] Cross-link with related skills

---

## Success Metrics

**This skill is successful if developers can:**

1. **Design SDK Architecture:**
   - Choose resource-based vs. command-based organization
   - Decide sync vs. async API patterns
   - Create intuitive method naming

2. **Implement Core Patterns:**
   - Retry with exponential backoff and jitter
   - Handle authentication (API keys, token refresh)
   - Create typed error hierarchies
   - Implement pagination (async iterators)

3. **Maintain Quality:**
   - Version SDKs with SemVer
   - Deprecate methods without breaking users
   - Write comprehensive tests

4. **Achieve Consistency:**
   - Maintain consistent patterns across TypeScript, Python, Go
   - Follow language conventions
   - Provide excellent developer experience

---

## Future Enhancements

**Potential Additions (Not in Initial Release):**

1. **GraphQL Client Design:** Different patterns from REST
2. **Rust SDK Patterns:** Zero-cost abstractions, lifetimes
3. **Mobile SDKs:** iOS (Swift), Android (Kotlin) patterns
4. **SDK Code Generation:** OpenAPI → SDK automation
5. **Advanced Streaming:** WebSockets, Server-Sent Events
6. **Observability:** Metrics, tracing, logging integration

---

**Document Status:** ✅ Complete
**Next Step:** Create SKILL.md from this master plan
**Owner:** AI Design Components Project
**Last Updated:** December 3, 2025
