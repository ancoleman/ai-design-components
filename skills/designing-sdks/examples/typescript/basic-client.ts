/**
 * Basic SDK Client Example (TypeScript)
 *
 * Demonstrates:
 * - Simple async API client
 * - API key authentication
 * - Resource-based organization
 * - Basic error handling
 *
 * Dependencies:
 * - None (uses native fetch)
 *
 * Usage:
 * - Set API_KEY environment variable
 * - Run: npx tsx basic-client.ts
 */

// Types
interface User {
  id: string
  name: string
  email: string
}

interface CreateUserParams {
  name: string
  email: string
}

// Configuration
interface ClientConfig {
  apiKey: string
  baseURL?: string
}

// Simple API client
class APIClient {
  private apiKey: string
  private baseURL: string

  constructor(config: ClientConfig) {
    this.apiKey = config.apiKey
    this.baseURL = config.baseURL || 'https://api.example.com'
  }

  // Resource accessors
  get users() {
    return new UsersResource(this)
  }

  // Core request method
  async request<T>(
    method: string,
    path: string,
    options?: {
      body?: any
      query?: Record<string, string>
    }
  ): Promise<T> {
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
      body: options?.body ? JSON.stringify(options.body) : undefined
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${await response.text()}`)
    }

    return await response.json()
  }
}

// Users resource
class UsersResource {
  constructor(private client: APIClient) {}

  async create(params: CreateUserParams): Promise<User> {
    return this.client.request<User>('POST', '/users', { body: params })
  }

  async retrieve(id: string): Promise<User> {
    return this.client.request<User>('GET', `/users/${id}`)
  }

  async update(id: string, params: Partial<CreateUserParams>): Promise<User> {
    return this.client.request<User>('PATCH', `/users/${id}`, { body: params })
  }

  async delete(id: string): Promise<void> {
    await this.client.request<void>('DELETE', `/users/${id}`)
  }

  async list(params?: { limit?: number }): Promise<User[]> {
    const response = await this.client.request<{ data: User[] }>('GET', '/users', {
      query: { limit: String(params?.limit || 100) }
    })
    return response.data
  }
}

// Usage example
async function main() {
  const client = new APIClient({
    apiKey: process.env.API_KEY || 'test_key'
  })

  try {
    // Create user
    const user = await client.users.create({
      name: 'Alice',
      email: 'alice@example.com'
    })
    console.log('Created user:', user)

    // Retrieve user
    const retrieved = await client.users.retrieve(user.id)
    console.log('Retrieved user:', retrieved)

    // Update user
    const updated = await client.users.update(user.id, { name: 'Alice Smith' })
    console.log('Updated user:', updated)

    // List users
    const users = await client.users.list({ limit: 10 })
    console.log(`Found ${users.length} users`)

    // Delete user
    await client.users.delete(user.id)
    console.log('Deleted user')
  } catch (error) {
    console.error('Error:', error)
  }
}

if (require.main === module) {
  main()
}

export { APIClient, UsersResource }
