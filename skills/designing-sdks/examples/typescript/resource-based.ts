/**
 * Resource-Based SDK Example (TypeScript)
 *
 * Demonstrates Stripe-style resource organization with lazy-loaded resources
 */

interface ClientConfig {
  apiKey: string
  baseURL?: string
}

class StripeStyleClient {
  private apiKey: string
  private baseURL: string

  constructor(config: ClientConfig) {
    this.apiKey = config.apiKey
    this.baseURL = config.baseURL || 'https://api.example.com'
  }

  get customers() {
    return new CustomersResource(this)
  }

  get payments() {
    return new PaymentsResource(this)
  }

  async request<T>(method: string, path: string, options?: any): Promise<T> {
    const response = await fetch(`${this.baseURL}${path}`, {
      method,
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      },
      body: options?.body ? JSON.stringify(options.body) : undefined
    })

    return await response.json()
  }
}

class CustomersResource {
  constructor(private client: StripeStyleClient) {}

  async create(params: { email: string }) {
    return this.client.request('POST', '/customers', { body: params })
  }

  async retrieve(id: string) {
    return this.client.request('GET', `/customers/${id}`)
  }
}

class PaymentsResource {
  constructor(private client: StripeStyleClient) {}

  async create(params: { amount: number; customer: string }) {
    return this.client.request('POST', '/payments', { body: params })
  }
}

// Usage
const client = new StripeStyleClient({ apiKey: 'sk_test_...' })
const customer = await client.customers.create({ email: 'user@example.com' })
const payment = await client.payments.create({ amount: 1000, customer: customer.id })
