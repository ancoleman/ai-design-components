# SDK Architecture Patterns

Comprehensive guide to organizing SDK code for maintainability, discoverability, and developer experience.

## Table of Contents

1. [Resource-Based Architecture](#resource-based-architecture)
2. [Command-Based Architecture](#command-based-architecture)
3. [Hybrid Approaches](#hybrid-approaches)
4. [Client Organization](#client-organization)
5. [Decision Framework](#decision-framework)

## Resource-Based Architecture

### Overview

Resource-based SDKs organize methods around API resources (users, payments, customers). Each resource is a class or object with CRUD methods.

**Example (Stripe-style):**

```typescript
const stripe = new Stripe('sk_test_...')

// Resource-based organization
const customer = await stripe.customers.create({ email: 'user@example.com' })
const charge = await stripe.charges.create({ amount: 1000, customer: customer.id })
const invoice = await stripe.invoices.retrieve('inv_123')
```

### Structure

```
Client
├─ customers (CustomersResource)
│   ├─ create(params)
│   ├─ retrieve(id)
│   ├─ update(id, params)
│   ├─ delete(id)
│   └─ list(params)
├─ charges (ChargesResource)
│   ├─ create(params)
│   └─ refund(id)
└─ invoices (InvoicesResource)
    ├─ retrieve(id)
    └─ finalize(id)
```

### Implementation (TypeScript)

```typescript
class StripeClient {
  private apiKey: string
  private baseURL: string

  constructor(apiKey: string) {
    this.apiKey = apiKey
    this.baseURL = 'https://api.stripe.com/v1'
  }

  // Lazy-loaded resources
  get customers() {
    return new CustomersResource(this)
  }

  get charges() {
    return new ChargesResource(this)
  }

  // Core request method
  async request(method: string, path: string, params?: any) {
    // HTTP request implementation
  }
}

class CustomersResource {
  constructor(private client: StripeClient) {}

  async create(params: CreateCustomerParams) {
    return this.client.request('POST', '/customers', params)
  }

  async retrieve(id: string) {
    return this.client.request('GET', `/customers/${id}`)
  }

  async update(id: string, params: UpdateCustomerParams) {
    return this.client.request('PATCH', `/customers/${id}`, params)
  }

  async delete(id: string) {
    return this.client.request('DELETE', `/customers/${id}`)
  }

  async *list(params?: ListParams): AsyncGenerator<Customer> {
    // Pagination implementation
  }
}
```

### Advantages

1. **Intuitive**: Matches API documentation and mental models
2. **Discoverable**: Autocomplete shows all available resources
3. **Clear Namespacing**: No method name conflicts (`customers.create` vs. `charges.create`)
4. **Easy to Extend**: Add new resources without changing existing code
5. **Developer Experience**: Users can easily find methods

### Disadvantages

1. **Bundle Size**: All resources loaded even if unused
2. **Tree-Shaking**: Harder to eliminate dead code
3. **Maintenance**: More files and classes to maintain

### When to Use

- Small-to-medium API surface (<100 methods)
- Developer experience is priority
- Bundle size is not critical (Node.js servers)
- API has clear resource boundaries (REST APIs)

---

## Command-Based Architecture

### Overview

Command-based SDKs (AWS SDK v3 pattern) separate client from commands. Each operation is a command object sent through the client.

**Example (AWS SDK v3):**

```typescript
import { S3Client, PutObjectCommand, GetObjectCommand } from '@aws-sdk/client-s3'

const client = new S3Client({ region: 'us-east-1' })

// Command-based organization
const putCommand = new PutObjectCommand({ Bucket: 'my-bucket', Key: 'file.txt', Body: 'content' })
await client.send(putCommand)

const getCommand = new GetObjectCommand({ Bucket: 'my-bucket', Key: 'file.txt' })
const result = await client.send(getCommand)
```

### Structure

```
Client (generic send method)
Commands (separate imports)
├─ PutObjectCommand
├─ GetObjectCommand
├─ DeleteObjectCommand
└─ ListObjectsCommand
```

### Implementation (TypeScript)

```typescript
// Client (generic)
class S3Client {
  private config: ClientConfig

  constructor(config: ClientConfig) {
    this.config = config
  }

  async send<Input, Output>(command: Command<Input, Output>): Promise<Output> {
    // Middleware pipeline
    const request = command.serialize(this.config)
    const response = await this.httpHandler.handle(request)
    return command.deserialize(response)
  }
}

// Command interface
interface Command<Input, Output> {
  serialize(config: ClientConfig): HttpRequest
  deserialize(response: HttpResponse): Output
}

// Concrete command
class PutObjectCommand implements Command<PutObjectInput, PutObjectOutput> {
  constructor(private input: PutObjectInput) {}

  serialize(config: ClientConfig): HttpRequest {
    return {
      method: 'PUT',
      path: `/${this.input.Bucket}/${this.input.Key}`,
      headers: { 'Content-Type': 'application/octet-stream' },
      body: this.input.Body
    }
  }

  deserialize(response: HttpResponse): PutObjectOutput {
    return {
      ETag: response.headers['etag'],
      VersionId: response.headers['x-amz-version-id']
    }
  }
}

// Usage
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'

const client = new S3Client({ region: 'us-east-1' })
const command = new PutObjectCommand({ Bucket: 'my-bucket', Key: 'file.txt', Body: 'content' })
const result = await client.send(command)
```

### Advantages

1. **Tree-Shakeable**: Import only needed commands
2. **Smaller Bundles**: Eliminate unused code (critical for browsers)
3. **Modular**: Each command is independent
4. **Middleware**: Easy to add cross-cutting concerns
5. **Testable**: Mock commands independently

### Disadvantages

1. **Verbose**: Two steps (create command, send command)
2. **Less Intuitive**: Extra indirection
3. **Discovery**: Harder to find available operations
4. **Boilerplate**: More code to write

### When to Use

- Large API surface (>100 methods)
- Bundle size is critical (browser SDKs)
- Modular architecture preferred
- Middleware/interceptors needed
- API surface changes frequently

---

## Hybrid Approaches

### Top-Level Convenience + Resources

Combine both patterns:

```typescript
class APIClient {
  // Resource-based (full control)
  get users() {
    return new UsersResource(this)
  }

  // Top-level convenience methods
  async createUser(params: CreateUserParams) {
    return this.users.create(params)
  }

  async getUser(id: string) {
    return this.users.retrieve(id)
  }
}

// Usage (both work)
await client.createUser({ email: 'user@example.com' })  // Convenience
await client.users.create({ email: 'user@example.com' }) // Resource
```

**Advantages:**
- Quick common operations (top-level)
- Advanced use cases (resources)
- Backward compatibility

**Disadvantages:**
- Two ways to do the same thing
- Larger API surface

---

## Client Organization

### Configuration

```typescript
interface ClientConfig {
  // Required
  apiKey: string

  // Optional with defaults
  baseURL?: string
  maxRetries?: number
  timeout?: number
  apiVersion?: string

  // Callbacks
  onTokenRefresh?: (token: string) => void
  onRequest?: (config: RequestConfig) => void
  onResponse?: (response: Response) => void
}

class APIClient {
  constructor(config: ClientConfig) {
    this.apiKey = config.apiKey
    this.baseURL = config.baseURL || 'https://api.example.com'
    this.maxRetries = config.maxRetries ?? 3
    this.timeout = config.timeout ?? 30000
  }
}
```

### Core Request Method

All resource methods delegate to a central request method:

```typescript
class APIClient {
  async request<T>(
    method: string,
    path: string,
    options?: {
      body?: any
      query?: Record<string, string>
      headers?: Record<string, string>
    }
  ): Promise<T> {
    // 1. Build URL
    const url = new URL(path, this.baseURL)
    if (options?.query) {
      Object.entries(options.query).forEach(([key, value]) => {
        url.searchParams.append(key, value)
      })
    }

    // 2. Build headers
    const headers = {
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json',
      ...options?.headers
    }

    // 3. Make request with retry
    let attempt = 0
    while (attempt <= this.maxRetries) {
      try {
        const response = await fetch(url.toString(), {
          method,
          headers,
          body: options?.body ? JSON.stringify(options.body) : undefined,
          signal: AbortSignal.timeout(this.timeout)
        })

        if (!response.ok) {
          throw await this.handleErrorResponse(response)
        }

        return await response.json()
      } catch (error) {
        if (++attempt > this.maxRetries || !this.isRetryable(error)) {
          throw error
        }
        await this.sleep(this.calculateBackoff(attempt))
      }
    }

    throw new Error('Max retries exceeded')
  }

  private isRetryable(error: any): boolean {
    return (
      error.code === 'ECONNRESET' ||
      error.code === 'ETIMEDOUT' ||
      (error.status >= 500 && error.status < 600) ||
      error.status === 429
    )
  }

  private calculateBackoff(attempt: number): number {
    const baseDelay = 1000
    const maxDelay = 10000
    const exponential = Math.min(baseDelay * Math.pow(2, attempt - 1), maxDelay)
    const jitter = Math.random() * 500
    return exponential + jitter
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
}
```

### Resource Classes

```typescript
class UsersResource {
  constructor(private client: APIClient) {}

  async create(params: CreateUserParams): Promise<User> {
    return this.client.request<User>('POST', '/users', { body: params })
  }

  async retrieve(id: string): Promise<User> {
    return this.client.request<User>('GET', `/users/${id}`)
  }

  async update(id: string, params: UpdateUserParams): Promise<User> {
    return this.client.request<User>('PATCH', `/users/${id}`, { body: params })
  }

  async delete(id: string): Promise<void> {
    await this.client.request<void>('DELETE', `/users/${id}`)
  }

  async *list(params?: ListParams): AsyncGenerator<User> {
    let cursor: string | undefined = undefined

    while (true) {
      const response = await this.client.request<ListUsersResponse>('GET', '/users', {
        query: {
          limit: String(params?.limit || 100),
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
```

---

## Decision Framework

### Choose Resource-Based If:

- API has <100 methods
- Clear resource boundaries (REST API)
- Developer experience is priority
- Target is Node.js servers (bundle size not critical)
- Team is familiar with Stripe/Twilio SDKs

### Choose Command-Based If:

- API has >100 methods
- Bundle size is critical (browser SDKs)
- Modular architecture preferred
- Need tree-shaking for performance
- Middleware/plugin system required

### Choose Hybrid If:

- Want both convenience and flexibility
- Backward compatibility with existing API
- Different user personas (beginners vs. advanced)
- Gradual migration from one pattern to another

### Language-Specific Considerations

**TypeScript/JavaScript:**
- Both patterns work well
- Resource-based more common for web APIs
- Command-based for large APIs (AWS)

**Python:**
- Resource-based is pythonic
- Use properties for lazy-loaded resources
- Context managers for client lifecycle

**Go:**
- Resource-based with interfaces
- Use exported functions for package-level API
- Context.Context required for all operations

---

## Real-World Examples

**Resource-Based:**
- Stripe (Node, Python, Go)
- Twilio
- SendGrid
- Most SaaS APIs

**Command-Based:**
- AWS SDK v3 (JavaScript)
- AWS SDK v2 (Go)
- Google Cloud Client Libraries

**Hybrid:**
- GitHub API (Octokit)
- OpenAI (convenience + resource methods)
