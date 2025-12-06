/**
 * Advanced SDK Client Example (TypeScript)
 *
 * Demonstrates:
 * - Retry logic with exponential backoff
 * - Typed error hierarchy
 * - Rate limit handling
 * - Streaming with async iterators
 * - Pagination
 *
 * Dependencies:
 * - None (uses native fetch)
 *
 * Usage:
 * - Set API_KEY environment variable
 * - Run: npx tsx advanced-client.ts
 */

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

class AuthenticationError extends APIError {
  constructor(message: string, requestId: string) {
    super(message, 401, 'authentication_error', requestId)
    this.name = 'AuthenticationError'
  }
}

// Client configuration
interface ClientConfig {
  apiKey: string
  baseURL?: string
  maxRetries?: number
  timeout?: number
}

// Advanced API client with retry and error handling
class AdvancedAPIClient {
  private apiKey: string
  private baseURL: string
  private maxRetries: number
  private timeout: number

  constructor(config: ClientConfig) {
    this.apiKey = config.apiKey
    this.baseURL = config.baseURL || 'https://api.example.com'
    this.maxRetries = config.maxRetries ?? 3
    this.timeout = config.timeout ?? 30000
  }

  get users() {
    return new AdvancedUsersResource(this)
  }

  // Request with retry and error handling
  async request<T>(
    method: string,
    path: string,
    options?: {
      body?: any
      query?: Record<string, string>
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
            'Content-Type': 'application/json'
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

          if (response.status === 401) {
            throw new AuthenticationError(
              errorData.message || 'Authentication failed',
              requestId
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
    options?: { body?: any }
  ): AsyncGenerator<any, void, unknown> {
    const url = new URL(path, this.baseURL)

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

// Advanced users resource with pagination
class AdvancedUsersResource {
  constructor(private client: AdvancedAPIClient) {}

  async create(params: { name: string; email: string }) {
    return this.client.request('POST', '/users', { body: params })
  }

  async retrieve(id: string) {
    return this.client.request('GET', `/users/${id}`)
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

// Usage example
async function main() {
  const client = new AdvancedAPIClient({
    apiKey: process.env.API_KEY || 'test_key',
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

    // Pagination with async iterator
    console.log('All users:')
    for await (const user of client.users.list({ limit: 10 })) {
      console.log('-', user.name, user.email)
    }

    // Streaming example
    console.log('Streaming example:')
    for await (const chunk of client.stream('POST', '/stream', {
      body: { prompt: 'Hello' }
    })) {
      process.stdout.write(chunk.content || '')
    }
    console.log('\n')
  } catch (error) {
    if (error instanceof RateLimitError) {
      console.error(`Rate limited. Retry after ${error.retryAfter}s`)
    } else if (error instanceof AuthenticationError) {
      console.error('Invalid API key')
    } else if (error instanceof APIError) {
      console.error(`API Error: ${error.message} (${error.code})`)
      console.error(`Request ID: ${error.requestId}`)
    } else {
      console.error('Unexpected error:', error)
    }
  }
}

if (require.main === module) {
  main()
}

export { AdvancedAPIClient }
