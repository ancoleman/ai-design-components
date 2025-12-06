# Testing SDK Code

Guide to unit testing, mocking HTTP requests, and integration testing for SDKs.

## Table of Contents

1. [Mocking HTTP Requests](#mocking-http-requests)
2. [Integration Tests](#integration-tests)

## Mocking HTTP Requests

### TypeScript (Vitest)

```typescript
import { describe, it, expect, vi } from 'vitest'

describe('APIClient', () => {
  it('should create a user', async () => {
    // Mock fetch
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ id: '123', email: 'user@example.com' }),
      headers: new Headers({ 'x-request-id': 'req_123' })
    })

    const client = new APIClient({ apiKey: 'test_key' })
    const user = await client.users.create({ email: 'user@example.com' })

    expect(user.id).toBe('123')
    expect(user.email).toBe('user@example.com')
  })

  it('should retry on 500 error', async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({ ok: false, status: 500 }) // First attempt fails
      .mockResolvedValueOnce({ // Second attempt succeeds
        ok: true,
        status: 200,
        json: async () => ({ id: '123' })
      })

    global.fetch = fetchMock

    const client = new APIClient({ apiKey: 'test_key', maxRetries: 3 })
    const user = await client.users.create({ email: 'user@example.com' })

    expect(fetchMock).toHaveBeenCalledTimes(2)
    expect(user.id).toBe('123')
  })
})
```

### Python (pytest)

```python
import pytest
from unittest.mock import Mock, patch

def test_create_user():
    with patch('requests.request') as mock_request:
        mock_request.return_value = Mock(
            status_code=200,
            json=lambda: {'id': '123', 'email': 'user@example.com'},
            headers={'x-request-id': 'req_123'}
        )

        client = APIClient(api_key='test_key')
        user = client.users.create(email='user@example.com')

        assert user['id'] == '123'
        assert user['email'] == 'user@example.com'

def test_retry_on_500():
    with patch('requests.request') as mock_request:
        # First call fails, second succeeds
        mock_request.side_effect = [
            Mock(status_code=500),
            Mock(status_code=200, json=lambda: {'id': '123'})
        ]

        client = APIClient(api_key='test_key', max_retries=3)
        user = client.users.create(email='user@example.com')

        assert mock_request.call_count == 2
```

## Integration Tests

### TypeScript

```typescript
describe('APIClient Integration', () => {
  // Use real API in test environment
  const client = new APIClient({
    apiKey: process.env.TEST_API_KEY!,
    baseURL: 'https://api-test.example.com'
  })

  it('should create and retrieve user', async () => {
    // Create
    const created = await client.users.create({
      email: `test-${Date.now()}@example.com`
    })

    expect(created.id).toBeDefined()

    // Retrieve
    const retrieved = await client.users.retrieve(created.id)
    expect(retrieved.email).toBe(created.email)

    // Cleanup
    await client.users.delete(created.id)
  })
})
```
