/**
 * Integration Testing Examples with Vitest + MSW
 *
 * Demonstrates: Integration testing with API mocking
 *
 * Dependencies:
 * - npm install -D vitest msw @mswjs/http-middleware
 *
 * Usage:
 * - npx vitest run vitest-integration.test.ts
 */

import { beforeAll, afterAll, afterEach, describe, test, expect } from 'vitest'
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'

// ====================
// System Under Test (API Client)
// ====================

interface User {
  id: string
  name: string
  email: string
}

interface CreateUserRequest {
  name: string
  email: string
}

class ApiClient {
  constructor(private baseUrl: string = 'http://localhost:3000') {}

  async getUser(id: string): Promise<User> {
    const response = await fetch(`${this.baseUrl}/api/users/${id}`)
    if (!response.ok) {
      throw new Error(`Failed to fetch user: ${response.statusText}`)
    }
    return response.json()
  }

  async createUser(data: CreateUserRequest): Promise<User> {
    const response = await fetch(`${this.baseUrl}/api/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) {
      throw new Error(`Failed to create user: ${response.statusText}`)
    }
    return response.json()
  }

  async updateUser(id: string, data: Partial<User>): Promise<User> {
    const response = await fetch(`${this.baseUrl}/api/users/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) {
      throw new Error(`Failed to update user: ${response.statusText}`)
    }
    return response.json()
  }

  async deleteUser(id: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/api/users/${id}`, {
      method: 'DELETE'
    })
    if (!response.ok) {
      throw new Error(`Failed to delete user: ${response.statusText}`)
    }
  }
}

// ====================
// MSW Server Setup
// ====================

const server = setupServer(
  // GET /api/users/:id
  http.get('http://localhost:3000/api/users/:id', ({ params }) => {
    const { id } = params
    return HttpResponse.json({
      id,
      name: 'Test User',
      email: 'test@example.com'
    })
  }),

  // POST /api/users
  http.post('http://localhost:3000/api/users', async ({ request }) => {
    const body = await request.json() as CreateUserRequest
    return HttpResponse.json(
      {
        id: '123',
        ...body
      },
      { status: 201 }
    )
  }),

  // PATCH /api/users/:id
  http.patch('http://localhost:3000/api/users/:id', async ({ params, request }) => {
    const { id } = params
    const body = await request.json() as Partial<User>
    return HttpResponse.json({
      id,
      name: 'Test User',
      email: 'test@example.com',
      ...body
    })
  }),

  // DELETE /api/users/:id
  http.delete('http://localhost:3000/api/users/:id', () => {
    return new HttpResponse(null, { status: 204 })
  })
)

// Start server before all tests
beforeAll(() => server.listen())

// Reset handlers after each test
afterEach(() => server.resetHandlers())

// Close server after all tests
afterAll(() => server.close())

// ====================
// Integration Tests
// ====================

describe('ApiClient integration tests', () => {
  let client: ApiClient

  beforeAll(() => {
    client = new ApiClient()
  })

  describe('getUser', () => {
    test('fetches user successfully', async () => {
      const user = await client.getUser('123')
      expect(user).toEqual({
        id: '123',
        name: 'Test User',
        email: 'test@example.com'
      })
    })

    test('handles 404 error', async () => {
      server.use(
        http.get('http://localhost:3000/api/users/:id', () => {
          return HttpResponse.json(
            { error: 'User not found' },
            { status: 404 }
          )
        })
      )

      await expect(client.getUser('999')).rejects.toThrow('Failed to fetch user')
    })

    test('handles network error', async () => {
      server.use(
        http.get('http://localhost:3000/api/users/:id', () => {
          return HttpResponse.error()
        })
      )

      await expect(client.getUser('123')).rejects.toThrow()
    })
  })

  describe('createUser', () => {
    test('creates user successfully', async () => {
      const newUser = await client.createUser({
        name: 'Alice',
        email: 'alice@example.com'
      })

      expect(newUser).toEqual({
        id: '123',
        name: 'Alice',
        email: 'alice@example.com'
      })
    })

    test('validates request payload', async () => {
      let capturedRequest: any

      server.use(
        http.post('http://localhost:3000/api/users', async ({ request }) => {
          capturedRequest = await request.json()
          return HttpResponse.json({ id: '123', ...capturedRequest }, { status: 201 })
        })
      )

      await client.createUser({
        name: 'Bob',
        email: 'bob@example.com'
      })

      expect(capturedRequest).toEqual({
        name: 'Bob',
        email: 'bob@example.com'
      })
    })

    test('handles validation error', async () => {
      server.use(
        http.post('http://localhost:3000/api/users', () => {
          return HttpResponse.json(
            { error: 'Invalid email' },
            { status: 400 }
          )
        })
      )

      await expect(
        client.createUser({ name: 'Test', email: 'invalid' })
      ).rejects.toThrow('Failed to create user')
    })
  })

  describe('updateUser', () => {
    test('updates user successfully', async () => {
      const updated = await client.updateUser('123', {
        name: 'Updated Name'
      })

      expect(updated.name).toBe('Updated Name')
      expect(updated.id).toBe('123')
    })

    test('allows partial updates', async () => {
      const updated = await client.updateUser('123', {
        email: 'newemail@example.com'
      })

      expect(updated.email).toBe('newemail@example.com')
    })
  })

  describe('deleteUser', () => {
    test('deletes user successfully', async () => {
      await expect(client.deleteUser('123')).resolves.toBeUndefined()
    })

    test('handles 404 on delete', async () => {
      server.use(
        http.delete('http://localhost:3000/api/users/:id', () => {
          return HttpResponse.json(
            { error: 'User not found' },
            { status: 404 }
          )
        })
      )

      await expect(client.deleteUser('999')).rejects.toThrow('Failed to delete user')
    })
  })
})

// ====================
// Advanced Integration Testing: Request Sequencing
// ====================

describe('user workflow integration', () => {
  let client: ApiClient

  beforeAll(() => {
    client = new ApiClient()
  })

  test('complete CRUD workflow', async () => {
    // Create user
    const created = await client.createUser({
      name: 'Alice',
      email: 'alice@example.com'
    })
    expect(created.id).toBeDefined()

    // Fetch user
    const fetched = await client.getUser(created.id)
    expect(fetched.name).toBe('Alice')

    // Update user
    const updated = await client.updateUser(created.id, {
      name: 'Alice Updated'
    })
    expect(updated.name).toBe('Alice Updated')

    // Delete user
    await expect(client.deleteUser(created.id)).resolves.toBeUndefined()
  })
})

// ====================
// Testing Headers and Authentication
// ====================

describe('authentication integration', () => {
  test('includes authorization header', async () => {
    let capturedHeaders: Headers | undefined

    server.use(
      http.get('http://localhost:3000/api/users/:id', ({ request }) => {
        capturedHeaders = request.headers
        return HttpResponse.json({ id: '123', name: 'Test', email: 'test@example.com' })
      })
    )

    class AuthenticatedClient extends ApiClient {
      async getUser(id: string): Promise<User> {
        const response = await fetch(`${this['baseUrl']}/api/users/${id}`, {
          headers: {
            'Authorization': 'Bearer test-token'
          }
        })
        return response.json()
      }
    }

    const authClient = new AuthenticatedClient()
    await authClient.getUser('123')

    expect(capturedHeaders?.get('Authorization')).toBe('Bearer test-token')
  })
})

// ====================
// Testing Rate Limiting and Retries
// ====================

describe('error handling and retries', () => {
  let client: ApiClient

  beforeAll(() => {
    client = new ApiClient()
  })

  test('handles rate limiting', async () => {
    let attemptCount = 0

    server.use(
      http.get('http://localhost:3000/api/users/:id', () => {
        attemptCount++
        if (attemptCount === 1) {
          return HttpResponse.json(
            { error: 'Rate limit exceeded' },
            {
              status: 429,
              headers: { 'Retry-After': '1' }
            }
          )
        }
        return HttpResponse.json({ id: '123', name: 'Test', email: 'test@example.com' })
      })
    )

    // First attempt should fail with 429
    await expect(client.getUser('123')).rejects.toThrow()
    expect(attemptCount).toBe(1)
  })
})
