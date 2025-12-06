# Authentication Patterns for SDKs

Comprehensive guide to handling authentication in client libraries, from simple API keys to complex OAuth flows.

## Table of Contents

1. [API Key Authentication](#api-key-authentication)
2. [OAuth 2.0 Token Management](#oauth-20-token-management)
3. [Bearer Token Injection](#bearer-token-injection)
4. [JWT Authentication](#jwt-authentication)
5. [Credential Storage](#credential-storage)
6. [Multi-Tenant Authentication](#multi-tenant-authentication)

## API Key Authentication

### Pattern 1: API Key in Constructor

Most common pattern for service-to-service authentication.

**TypeScript:**

```typescript
class APIClient {
  private apiKey: string

  constructor(apiKey: string) {
    this.apiKey = apiKey
  }

  async request(method: string, path: string, options?: any) {
    const headers = {
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json',
      ...options?.headers
    }

    const response = await fetch(`${this.baseURL}${path}`, {
      method,
      headers,
      body: options?.body ? JSON.stringify(options.body) : undefined
    })

    return response.json()
  }
}

// Usage
const client = new APIClient(process.env.API_KEY!)
```

**Python:**

```python
class APIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.example.com"

    def request(self, method: str, path: str, body=None):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.request(
            method=method,
            url=f"{self.base_url}{path}",
            json=body,
            headers=headers
        )

        return response.json()

# Usage
client = APIClient(os.environ['API_KEY'])
```

**Go:**

```go
type Client struct {
    apiKey  string
    baseURL string
}

func New(apiKey string) *Client {
    return &Client{
        apiKey:  apiKey,
        baseURL: "https://api.example.com",
    }
}

func (c *Client) request(ctx context.Context, method, path string, body interface{}) (interface{}, error) {
    req, err := http.NewRequestWithContext(ctx, method, c.baseURL+path, nil)
    if err != nil {
        return nil, err
    }

    req.Header.Set("Authorization", "Bearer "+c.apiKey)
    req.Header.Set("Content-Type", "application/json")

    // Execute request
}

// Usage
client := apiclient.New(os.Getenv("API_KEY"))
```

### Pattern 2: API Key in Header vs. Query Parameter

**Header-Based (Recommended):**

```typescript
headers: {
  'Authorization': `Bearer ${apiKey}`
}
```

**Query Parameter (Avoid if possible):**

```typescript
const url = `${baseURL}${path}?api_key=${apiKey}`
```

**Rationale:**
- Headers are more secure (not logged by proxies)
- Headers don't appear in browser history
- Query parameters may be cached

---

## OAuth 2.0 Token Management

### Pattern 1: Automatic Token Refresh

**TypeScript:**

```typescript
interface OAuthConfig {
  clientId: string
  clientSecret: string
  accessToken: string
  refreshToken: string
  expiresAt: Date
  onTokenRefresh?: (tokens: TokenResponse) => void
}

interface TokenResponse {
  access_token: string
  refresh_token: string
  expires_in: number
}

class OAuthClient {
  private config: OAuthConfig

  constructor(config: OAuthConfig) {
    this.config = config
  }

  async request(method: string, path: string, options?: any) {
    // Check if token is expired
    if (this.isTokenExpired()) {
      await this.refreshAccessToken()
    }

    const headers = {
      'Authorization': `Bearer ${this.config.accessToken}`,
      'Content-Type': 'application/json',
      ...options?.headers
    }

    const response = await fetch(`${this.baseURL}${path}`, {
      method,
      headers,
      body: options?.body ? JSON.stringify(options.body) : undefined
    })

    // Handle 401 (token expired during request)
    if (response.status === 401) {
      await this.refreshAccessToken()
      // Retry request
      return this.request(method, path, options)
    }

    return response.json()
  }

  private isTokenExpired(): boolean {
    // Refresh 5 minutes before actual expiry
    const bufferTime = 5 * 60 * 1000 // 5 minutes
    return Date.now() >= this.config.expiresAt.getTime() - bufferTime
  }

  private async refreshAccessToken(): Promise<void> {
    const response = await fetch('https://api.example.com/oauth/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        refresh_token: this.config.refreshToken,
        client_id: this.config.clientId,
        client_secret: this.config.clientSecret
      })
    })

    const tokens: TokenResponse = await response.json()

    // Update config
    this.config.accessToken = tokens.access_token
    this.config.refreshToken = tokens.refresh_token
    this.config.expiresAt = new Date(Date.now() + tokens.expires_in * 1000)

    // Notify callback
    if (this.config.onTokenRefresh) {
      this.config.onTokenRefresh(tokens)
    }
  }
}

// Usage
const client = new OAuthClient({
  clientId: 'client_id',
  clientSecret: 'client_secret',
  accessToken: 'current_access_token',
  refreshToken: 'refresh_token',
  expiresAt: new Date('2025-12-31'),
  onTokenRefresh: (tokens) => {
    // Save new tokens to database
    saveTokens(tokens)
  }
})

// SDK automatically refreshes token
const user = await client.users.create({ email: 'user@example.com' })
```

**Python:**

```python
from datetime import datetime, timedelta
from typing import Callable, Optional

class OAuthClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        access_token: str,
        refresh_token: str,
        expires_at: datetime,
        on_token_refresh: Optional[Callable[[dict], None]] = None
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at
        self.on_token_refresh = on_token_refresh

    def request(self, method: str, path: str, body=None):
        # Check if token is expired
        if self._is_token_expired():
            self._refresh_access_token()

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        response = requests.request(
            method=method,
            url=f"{self.base_url}{path}",
            json=body,
            headers=headers
        )

        # Handle 401
        if response.status_code == 401:
            self._refresh_access_token()
            return self.request(method, path, body)

        return response.json()

    def _is_token_expired(self) -> bool:
        # Refresh 5 minutes before expiry
        buffer = timedelta(minutes=5)
        return datetime.now() >= self.expires_at - buffer

    def _refresh_access_token(self):
        response = requests.post(
            "https://api.example.com/oauth/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
        )

        tokens = response.json()

        # Update tokens
        self.access_token = tokens['access_token']
        self.refresh_token = tokens['refresh_token']
        self.expires_at = datetime.now() + timedelta(seconds=tokens['expires_in'])

        # Notify callback
        if self.on_token_refresh:
            self.on_token_refresh(tokens)
```

---

## Bearer Token Injection

### Pattern: Per-Request Token

For multi-tenant applications where each request uses a different user token.

**TypeScript:**

```typescript
class APIClient {
  private baseURL: string

  constructor(baseURL: string) {
    this.baseURL = baseURL
  }

  async request(
    method: string,
    path: string,
    options?: {
      body?: any
      headers?: Record<string, string>
      token?: string // Per-request token
    }
  ) {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...options?.headers
    }

    // Add token if provided
    if (options?.token) {
      headers['Authorization'] = `Bearer ${options.token}`
    }

    const response = await fetch(`${this.baseURL}${path}`, {
      method,
      headers,
      body: options?.body ? JSON.stringify(options.body) : undefined
    })

    return response.json()
  }
}

// Usage in multi-tenant app
const client = new APIClient('https://api.example.com')

// Request 1 (user A's token)
const userAData = await client.request('GET', '/users/me', {
  token: userAToken
})

// Request 2 (user B's token)
const userBData = await client.request('GET', '/users/me', {
  token: userBToken
})
```

---

## JWT Authentication

### Pattern: JWT with Automatic Refresh

**TypeScript:**

```typescript
interface JWTConfig {
  getAccessToken: () => string
  getRefreshToken: () => string
  onTokenRefresh: (tokens: { accessToken: string; refreshToken: string }) => void
}

class JWTClient {
  private config: JWTConfig

  constructor(config: JWTConfig) {
    this.config = config
  }

  async request(method: string, path: string, options?: any) {
    const accessToken = this.config.getAccessToken()

    const headers = {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
      ...options?.headers
    }

    let response = await fetch(`${this.baseURL}${path}`, {
      method,
      headers,
      body: options?.body ? JSON.stringify(options.body) : undefined
    })

    // Handle 401 (expired token)
    if (response.status === 401) {
      const newTokens = await this.refreshToken()
      this.config.onTokenRefresh(newTokens)

      // Retry with new token
      headers['Authorization'] = `Bearer ${newTokens.accessToken}`
      response = await fetch(`${this.baseURL}${path}`, {
        method,
        headers,
        body: options?.body ? JSON.stringify(options.body) : undefined
      })
    }

    return response.json()
  }

  private async refreshToken(): Promise<{ accessToken: string; refreshToken: string }> {
    const refreshToken = this.config.getRefreshToken()

    const response = await fetch(`${this.baseURL}/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refreshToken })
    })

    const { accessToken, refreshToken: newRefreshToken } = await response.json()

    return {
      accessToken,
      refreshToken: newRefreshToken
    }
  }
}

// Usage with local storage
const client = new JWTClient({
  getAccessToken: () => localStorage.getItem('accessToken') || '',
  getRefreshToken: () => localStorage.getItem('refreshToken') || '',
  onTokenRefresh: (tokens) => {
    localStorage.setItem('accessToken', tokens.accessToken)
    localStorage.setItem('refreshToken', tokens.refreshToken)
  }
})
```

---

## Credential Storage

### Environment Variables (Recommended)

**TypeScript (Node.js):**

```typescript
const client = new APIClient({
  apiKey: process.env.API_KEY!
})
```

**Python:**

```python
import os

client = APIClient(api_key=os.environ['API_KEY'])
```

**Go:**

```go
import "os"

client := apiclient.New(os.Getenv("API_KEY"))
```

### Configuration Files

**TypeScript (dotenv):**

```typescript
import dotenv from 'dotenv'
dotenv.config()

const client = new APIClient({
  apiKey: process.env.API_KEY!
})
```

**.env file:**

```
API_KEY=sk_test_1234567890abcdef
API_BASE_URL=https://api.example.com
```

### Credential Providers (AWS SDK Pattern)

```typescript
interface CredentialProvider {
  getCredentials(): Promise<Credentials>
}

class EnvironmentCredentialProvider implements CredentialProvider {
  async getCredentials(): Promise<Credentials> {
    return {
      apiKey: process.env.API_KEY || ''
    }
  }
}

class FileCredentialProvider implements CredentialProvider {
  constructor(private filePath: string) {}

  async getCredentials(): Promise<Credentials> {
    const config = await fs.readFile(this.filePath, 'utf-8')
    const parsed = JSON.parse(config)
    return {
      apiKey: parsed.apiKey
    }
  }
}

class APIClient {
  private credentialProvider: CredentialProvider

  constructor(credentialProvider: CredentialProvider) {
    this.credentialProvider = credentialProvider
  }

  async request(method: string, path: string, options?: any) {
    const credentials = await this.credentialProvider.getCredentials()

    const headers = {
      'Authorization': `Bearer ${credentials.apiKey}`,
      ...options?.headers
    }

    // Make request
  }
}

// Usage
const client = new APIClient(new EnvironmentCredentialProvider())
// or
const client = new APIClient(new FileCredentialProvider('~/.config/api/credentials.json'))
```

---

## Multi-Tenant Authentication

### Pattern: Token Manager

For applications managing multiple API clients:

```typescript
class TokenManager {
  private tokens: Map<string, string> = new Map()

  setToken(tenantId: string, token: string) {
    this.tokens.set(tenantId, token)
  }

  getToken(tenantId: string): string | undefined {
    return this.tokens.get(tenantId)
  }
}

class MultiTenantClient {
  private tokenManager: TokenManager

  constructor(tokenManager: TokenManager) {
    this.tokenManager = tokenManager
  }

  async request(
    tenantId: string,
    method: string,
    path: string,
    options?: any
  ) {
    const token = this.tokenManager.getToken(tenantId)

    if (!token) {
      throw new Error(`No token for tenant: ${tenantId}`)
    }

    const headers = {
      'Authorization': `Bearer ${token}`,
      ...options?.headers
    }

    const response = await fetch(`${this.baseURL}${path}`, {
      method,
      headers,
      body: options?.body ? JSON.stringify(options.body) : undefined
    })

    return response.json()
  }
}

// Usage
const tokenManager = new TokenManager()
tokenManager.setToken('tenant-a', 'token-a')
tokenManager.setToken('tenant-b', 'token-b')

const client = new MultiTenantClient(tokenManager)

// Request for tenant A
await client.request('tenant-a', 'GET', '/users')

// Request for tenant B
await client.request('tenant-b', 'GET', '/users')
```

---

## Best Practices

### Security

1. **Never Hardcode Credentials**
   ```typescript
   // ❌ Bad
   const client = new APIClient({ apiKey: 'sk_test_1234' })

   // ✅ Good
   const client = new APIClient({ apiKey: process.env.API_KEY })
   ```

2. **Use HTTPS Only**
   ```typescript
   if (!this.baseURL.startsWith('https://')) {
     throw new Error('API base URL must use HTTPS')
   }
   ```

3. **Don't Log Credentials**
   ```typescript
   // ❌ Bad
   console.log('Making request with API key:', apiKey)

   // ✅ Good
   console.log('Making request to:', path)
   ```

4. **Rotate Credentials**
   - Support credential rotation without downtime
   - Accept both old and new credentials during rotation period

### Error Handling

```typescript
class AuthenticationError extends Error {
  constructor(message: string, public requestId: string) {
    super(message)
    this.name = 'AuthenticationError'
  }
}

if (response.status === 401) {
  throw new AuthenticationError(
    'Invalid API key or expired token',
    response.headers.get('x-request-id') || 'unknown'
  )
}
```

### Token Storage

**Browser (Web Storage API):**

```typescript
// Use sessionStorage for sensitive tokens (cleared on tab close)
sessionStorage.setItem('accessToken', token)

// Use localStorage for less sensitive tokens (persistent)
localStorage.setItem('refreshToken', token)
```

**Node.js (Keychain):**

```typescript
import keytar from 'keytar'

// Store securely in OS keychain
await keytar.setPassword('my-app', 'api-key', apiKey)

// Retrieve
const apiKey = await keytar.getPassword('my-app', 'api-key')
```

---

## Language-Specific Patterns

### Python Context Managers

```python
class APIClient:
    def __enter__(self):
        # Initialize client
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup (revoke tokens, close connections)
        self.close()

# Usage
with APIClient(api_key=os.environ['API_KEY']) as client:
    user = client.users.create(email='user@example.com')
# Token automatically cleaned up
```

### Go Context for Auth

```go
type authKey struct{}

func WithToken(ctx context.Context, token string) context.Context {
    return context.WithValue(ctx, authKey{}, token)
}

func (c *Client) request(ctx context.Context, method, path string) (interface{}, error) {
    token, ok := ctx.Value(authKey{}).(string)
    if !ok {
        return nil, errors.New("no auth token in context")
    }

    req.Header.Set("Authorization", "Bearer "+token)
    // Make request
}

// Usage
ctx := context.Background()
ctx = apiclient.WithToken(ctx, "api_key")
user, err := client.Users().Create(ctx, req)
```
