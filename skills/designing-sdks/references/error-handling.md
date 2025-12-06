# Error Handling in SDKs

Guide to creating typed error hierarchies, error metadata, and user-friendly error messages.

## Table of Contents

1. [Typed Error Hierarchy](#typed-error-hierarchy)
2. [Python Error Hierarchy](#python-error-hierarchy)
3. [Go Error Types](#go-error-types)
4. [Error Handling Patterns](#error-handling-patterns)
5. [User-Friendly Error Messages](#user-friendly-error-messages)
6. [Debugging Support](#debugging-support)

## Typed Error Hierarchy

### Base Error Class

```typescript
class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public code: string,
    public requestId: string,
    public headers?: Record<string, string>
  ) {
    super(message)
    this.name = 'APIError'
    Object.setPrototypeOf(this, APIError.prototype)
  }

  toJSON() {
    return {
      name: this.name,
      message: this.message,
      status: this.status,
      code: this.code,
      requestId: this.requestId
    }
  }
}
```

### Specific Error Types

```typescript
class RateLimitError extends APIError {
  constructor(message: string, requestId: string, headers: Record<string, string>) {
    super(message, 429, 'rate_limit_error', requestId, headers)
    this.name = 'RateLimitError'
  }

  get retryAfter(): number {
    return parseInt(this.headers?.['retry-after'] || '60')
  }
}

class AuthenticationError extends APIError {
  constructor(message: string, requestId: string) {
    super(message, 401, 'authentication_error', requestId)
    this.name = 'AuthenticationError'
  }
}

class InvalidRequestError extends APIError {
  constructor(
    message: string,
    requestId: string,
    public param?: string,
    public validationErrors?: Array<{field: string; message: string}>
  ) {
    super(message, 400, 'invalid_request_error', requestId)
    this.name = 'InvalidRequestError'
  }
}

class NotFoundError extends APIError {
  constructor(message: string, requestId: string, public resourceType?: string) {
    super(message, 404, 'not_found', requestId)
    this.name = 'NotFoundError'
  }
}

class PermissionError extends APIError {
  constructor(message: string, requestId: string) {
    super(message, 403, 'permission_denied', requestId)
    this.name = 'PermissionError'
  }
}

class ServerError extends APIError {
  constructor(message: string, status: number, requestId: string) {
    super(message, status, 'server_error', requestId)
    this.name = 'ServerError'
  }
}
```

### Error Factory

```typescript
function createErrorFromResponse(response: Response, requestId: string): APIError {
  const status = response.status
  const errorData = response.data || {}

  switch (status) {
    case 400:
      return new InvalidRequestError(
        errorData.message || 'Invalid request',
        requestId,
        errorData.param,
        errorData.errors
      )
    case 401:
      return new AuthenticationError(
        errorData.message || 'Authentication failed',
        requestId
      )
    case 403:
      return new PermissionError(
        errorData.message || 'Permission denied',
        requestId
      )
    case 404:
      return new NotFoundError(
        errorData.message || 'Resource not found',
        requestId,
        errorData.resource
      )
    case 429:
      return new RateLimitError(
        errorData.message || 'Rate limit exceeded',
        requestId,
        response.headers
      )
    case 500:
    case 502:
    case 503:
    case 504:
      return new ServerError(
        errorData.message || 'Server error',
        status,
        requestId
      )
    default:
      return new APIError(
        errorData.message || `HTTP ${status}`,
        status,
        errorData.code || 'unknown_error',
        requestId
      )
  }
}
```

## Python Error Hierarchy

```python
class APIError(Exception):
    def __init__(self, message: str, status: int, code: str, request_id: str):
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.request_id = request_id

    def __str__(self):
        return f"{self.name}: {self.message} (status={self.status}, request_id={self.request_id})"

    @property
    def name(self):
        return self.__class__.__name__

class RateLimitError(APIError):
    def __init__(self, message: str, request_id: str, retry_after: int):
        super().__init__(message, 429, 'rate_limit_error', request_id)
        self.retry_after = retry_after

class AuthenticationError(APIError):
    def __init__(self, message: str, request_id: str):
        super().__init__(message, 401, 'authentication_error', request_id)

class InvalidRequestError(APIError):
    def __init__(self, message: str, request_id: str, param: str = None):
        super().__init__(message, 400, 'invalid_request_error', request_id)
        self.param = param
```

## Go Error Types

```go
type APIError struct {
    Message   string
    Status    int
    Code      string
    RequestID string
}

func (e *APIError) Error() string {
    return fmt.Sprintf("%s: %s (status=%d, request_id=%s)",
        e.Code, e.Message, e.Status, e.RequestID)
}

type RateLimitError struct {
    APIError
    RetryAfter int
}

type AuthenticationError struct {
    APIError
}

type InvalidRequestError struct {
    APIError
    Param string
}
```

## Error Handling Patterns

### Try-Catch with Type Guards

```typescript
try {
  const user = await client.users.create({ email: 'invalid' })
} catch (error) {
  if (error instanceof RateLimitError) {
    console.log(`Rate limited. Retry after ${error.retryAfter}s`)
    await sleep(error.retryAfter * 1000)
    // Retry request
  } else if (error instanceof AuthenticationError) {
    console.error('Invalid API key. Check your credentials.')
  } else if (error instanceof InvalidRequestError) {
    console.error(`Invalid parameter: ${error.param}`)
    if (error.validationErrors) {
      error.validationErrors.forEach(err => {
        console.error(`  - ${err.field}: ${err.message}`)
      })
    }
  } else if (error instanceof NotFoundError) {
    console.error(`${error.resourceType || 'Resource'} not found`)
  } else if (error instanceof PermissionError) {
    console.error('Insufficient permissions')
  } else if (error instanceof ServerError) {
    console.error('Server error. Please try again later.')
  } else {
    // Unknown error
    console.error('Unexpected error:', error)
    throw error
  }
}
```

### Python Exception Handling

```python
try:
    user = client.users.create(email='invalid')
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
    time.sleep(e.retry_after)
except AuthenticationError:
    print("Invalid API key")
except InvalidRequestError as e:
    print(f"Invalid parameter: {e.param}")
except APIError as e:
    print(f"API Error: {e.message} ({e.code})")
```

## User-Friendly Error Messages

### Include Context

```typescript
class InvalidRequestError extends APIError {
  constructor(
    message: string,
    requestId: string,
    public param?: string,
    public expected?: string
  ) {
    // Enhance message with context
    const fullMessage = param
      ? `Invalid ${param}: ${message}${expected ? `. Expected: ${expected}` : ''}`
      : message

    super(fullMessage, 400, 'invalid_request_error', requestId)
  }
}

// Usage
throw new InvalidRequestError(
  'must be a valid email address',
  requestId,
  'email',
  'format: user@example.com'
)
// Error: "Invalid email: must be a valid email address. Expected: format: user@example.com"
```

### Link to Documentation

```typescript
class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public code: string,
    public requestId: string,
    public docUrl?: string
  ) {
    super(message)
    this.docUrl = docUrl || `https://docs.example.com/errors/${code}`
  }

  toString(): string {
    return `${this.message}\n\nFor more information: ${this.docUrl}\nRequest ID: ${this.requestId}`
  }
}
```

### Actionable Guidance

```typescript
throw new AuthenticationError(
  'API key is invalid. Please check that you are using the correct API key from your dashboard (https://dashboard.example.com/api-keys).',
  requestId
)

throw new RateLimitError(
  'You have exceeded the rate limit. Please wait 60 seconds before retrying, or upgrade your plan for higher limits (https://example.com/pricing).',
  requestId,
  60
)
```

## Debugging Support

### Request ID in All Errors

```typescript
async request(method: string, path: string, options?: any) {
  const response = await fetch(...)

  const requestId = response.headers.get('x-request-id') || randomUUID()

  if (!response.ok) {
    throw createErrorFromResponse(response, requestId)
  }
}
```

### Stack Traces

```typescript
class APIError extends Error {
  constructor(...) {
    super(message)
    // Capture stack trace
    Error.captureStackTrace(this, this.constructor)
  }
}
```

### Logging Integration

```typescript
class APIClient {
  async request(method: string, path: string, options?: any) {
    try {
      const response = await fetch(...)
      return response.json()
    } catch (error) {
      // Log error details
      console.error('API request failed:', {
        method,
        path,
        error: error instanceof APIError ? error.toJSON() : error,
        timestamp: new Date().toISOString()
      })

      throw error
    }
  }
}
```
