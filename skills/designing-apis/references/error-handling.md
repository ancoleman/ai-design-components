# API Error Handling Standards

Comprehensive guide to error response design using RFC 7807 Problem Details standard.

## Table of Contents

1. [RFC 7807 Problem Details](#rfc-7807-problem-details)
2. [Common Error Patterns](#common-error-patterns)
3. [Validation Errors](#validation-errors)
4. [Error Code Design](#error-code-design)
5. [Best Practices](#best-practices)

## RFC 7807 Problem Details

### Standard Structure

RFC 7807 defines a standard format for HTTP API error responses.

**Content-Type:** `application/problem+json`

**Required Fields:**
- `type`: URI identifying the error type
- `title`: Short, human-readable summary
- `status`: HTTP status code

**Optional Fields:**
- `detail`: Human-readable explanation
- `instance`: URI identifying this specific occurrence

**Custom Extensions:** Additional fields allowed

### Basic Example

```json
{
  "type": "https://api.example.com/errors/not-found",
  "title": "Resource Not Found",
  "status": 404,
  "detail": "User with id '123' does not exist",
  "instance": "/api/v1/users/123"
}
```

### Error Type URIs

Error type URIs should be dereferenceable documentation:

```
https://api.example.com/errors/validation
  → Documents validation error format

https://api.example.com/errors/rate-limit
  → Documents rate limiting policy

https://api.example.com/errors/unauthorized
  → Documents authentication requirements
```

## Common Error Patterns

### 400 Bad Request - Validation Error

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Failed",
  "status": 400,
  "detail": "Request body contains invalid fields",
  "instance": "/api/v1/users",
  "errors": [
    {
      "field": "email",
      "message": "Must be a valid email address",
      "code": "INVALID_FORMAT",
      "rejectedValue": "not-an-email"
    },
    {
      "field": "age",
      "message": "Must be at least 18",
      "code": "MIN_VALUE",
      "rejectedValue": 15
    }
  ]
}
```

### 401 Unauthorized - Authentication Required

```json
{
  "type": "https://api.example.com/errors/unauthorized",
  "title": "Authentication Required",
  "status": 401,
  "detail": "Valid authentication credentials are required to access this resource",
  "instance": "/api/v1/users/123"
}
```

**With WWW-Authenticate header:**
```http
401 Unauthorized
WWW-Authenticate: Bearer realm="api", error="invalid_token"
Content-Type: application/problem+json
```

### 403 Forbidden - Insufficient Permissions

```json
{
  "type": "https://api.example.com/errors/forbidden",
  "title": "Insufficient Permissions",
  "status": 403,
  "detail": "You do not have permission to delete this resource",
  "instance": "/api/v1/users/123",
  "requiredScope": "admin:write",
  "currentScopes": ["read:users", "write:users"]
}
```

### 404 Not Found

```json
{
  "type": "https://api.example.com/errors/not-found",
  "title": "Resource Not Found",
  "status": 404,
  "detail": "User with id '123' does not exist",
  "instance": "/api/v1/users/123"
}
```

### 409 Conflict

```json
{
  "type": "https://api.example.com/errors/conflict",
  "title": "Resource Conflict",
  "status": 409,
  "detail": "A user with username 'alice' already exists",
  "instance": "/api/v1/users",
  "conflictingField": "username",
  "conflictingValue": "alice"
}
```

### 422 Unprocessable Entity - Semantic Error

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 422,
  "detail": "The request is syntactically correct but semantically invalid",
  "errors": [
    {
      "field": "startDate",
      "message": "Start date must be before end date",
      "code": "DATE_RANGE_INVALID"
    }
  ]
}
```

### 429 Too Many Requests - Rate Limit

```json
{
  "type": "https://api.example.com/errors/rate-limit",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "You have exceeded the rate limit of 100 requests per hour",
  "instance": "/api/v1/users",
  "limit": 100,
  "remaining": 0,
  "resetAt": "2025-12-03T11:00:00Z",
  "retryAfter": 3600
}
```

**With headers:**
```http
429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1672531200
Retry-After: 3600
Content-Type: application/problem+json
```

### 500 Internal Server Error

```json
{
  "type": "https://api.example.com/errors/internal",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred. Please try again later.",
  "instance": "/api/v1/users",
  "traceId": "abc123-def456-ghi789"
}
```

**Important:** Never expose internal error details to clients.

### 503 Service Unavailable

```json
{
  "type": "https://api.example.com/errors/unavailable",
  "title": "Service Unavailable",
  "status": 503,
  "detail": "The service is temporarily unavailable. Please try again later.",
  "retryAfter": 120
}
```

**With header:**
```http
503 Service Unavailable
Retry-After: 120
Content-Type: application/problem+json
```

## Validation Errors

### Single Field Error

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 400,
  "detail": "Email field validation failed",
  "errors": [
    {
      "field": "email",
      "message": "Must be a valid email address",
      "code": "INVALID_EMAIL_FORMAT",
      "rejectedValue": "not-an-email"
    }
  ]
}
```

### Multiple Field Errors

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 400,
  "detail": "Multiple fields failed validation",
  "errors": [
    {
      "field": "email",
      "message": "Must be a valid email address",
      "code": "INVALID_EMAIL_FORMAT"
    },
    {
      "field": "password",
      "message": "Must be at least 8 characters",
      "code": "MIN_LENGTH",
      "params": { "minLength": 8 }
    },
    {
      "field": "age",
      "message": "Must be at least 18",
      "code": "MIN_VALUE",
      "params": { "min": 18 }
    }
  ]
}
```

### Nested Field Errors

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 400,
  "errors": [
    {
      "field": "address.zipCode",
      "message": "Must be a valid US ZIP code",
      "code": "INVALID_ZIP_FORMAT"
    },
    {
      "field": "items[0].quantity",
      "message": "Must be a positive number",
      "code": "MIN_VALUE",
      "params": { "min": 1 }
    }
  ]
}
```

### Error Field Structure

Standard error object fields:

```typescript
interface ValidationError {
  field: string;           // Field path (e.g., "email", "address.city")
  message: string;         // Human-readable message
  code: string;            // Machine-readable code
  rejectedValue?: any;     // Value that was rejected (optional)
  params?: object;         // Validation parameters (optional)
}
```

## Error Code Design

### Machine-Readable Codes

Use consistent, uppercase, underscore-separated codes:

**Format:** `CATEGORY_SPECIFIC_ERROR`

```
INVALID_EMAIL_FORMAT
INVALID_DATE_RANGE
DUPLICATE_USERNAME
INSUFFICIENT_PERMISSIONS
RESOURCE_NOT_FOUND
RATE_LIMIT_EXCEEDED
```

### Code Categories

**Validation:**
- `INVALID_FORMAT`
- `MIN_LENGTH`, `MAX_LENGTH`
- `MIN_VALUE`, `MAX_VALUE`
- `REQUIRED_FIELD`
- `INVALID_ENUM_VALUE`

**Business Logic:**
- `DUPLICATE_RESOURCE`
- `INSUFFICIENT_BALANCE`
- `ORDER_NOT_ALLOWED`
- `RESOURCE_LOCKED`

**Authentication/Authorization:**
- `INVALID_CREDENTIALS`
- `TOKEN_EXPIRED`
- `INSUFFICIENT_PERMISSIONS`
- `ACCOUNT_SUSPENDED`

**Rate Limiting:**
- `RATE_LIMIT_EXCEEDED`
- `QUOTA_EXCEEDED`

**System:**
- `INTERNAL_ERROR`
- `SERVICE_UNAVAILABLE`
- `TIMEOUT`

### Localizable Error Messages

Separate code from message for internationalization:

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 400,
  "errors": [
    {
      "field": "email",
      "code": "INVALID_EMAIL_FORMAT",
      "message": "Must be a valid email address",
      "messageKey": "validation.email.invalid",
      "params": {}
    }
  ]
}
```

Client can use `messageKey` for localization:
```javascript
const messages = {
  en: { "validation.email.invalid": "Must be a valid email address" },
  es: { "validation.email.invalid": "Debe ser una dirección de correo válida" },
  fr: { "validation.email.invalid": "Doit être une adresse e-mail valide" }
};
```

## Best Practices

### Consistency

**Always use RFC 7807 format:**
```json
{
  "type": "...",
  "title": "...",
  "status": 400
}
```

**Never mix formats:**
```json
❌ { "error": "Something went wrong" }
❌ { "message": "Invalid input" }
```

### Security

**Never expose sensitive information:**
```json
❌ {
  "detail": "SQL error: SELECT * FROM users WHERE password='...'",
  "stackTrace": "..."
}

✓ {
  "detail": "An internal error occurred",
  "traceId": "abc-123"
}
```

**Use trace IDs for internal debugging:**
- Return trace ID to client
- Log full error details server-side with trace ID
- Customer support can reference trace ID

### User-Friendly Messages

**Bad:**
```json
{
  "detail": "Validation failed: field 'email' does not match regex pattern"
}
```

**Good:**
```json
{
  "detail": "Please enter a valid email address",
  "errors": [
    {
      "field": "email",
      "message": "Must be a valid email address (e.g., user@example.com)"
    }
  ]
}
```

### Actionable Errors

Tell users what to do:

```json
{
  "type": "https://api.example.com/errors/rate-limit",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "You have exceeded 100 requests per hour. Please wait 15 minutes before trying again.",
  "retryAfter": 900,
  "upgradeUrl": "https://example.com/upgrade"
}
```

### Error Documentation

Each error type URI should link to documentation:

```markdown
# https://api.example.com/errors/validation

## Validation Error

HTTP Status: 400 Bad Request

Returned when request body contains invalid data.

### Response Format

{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 400,
  "errors": [...]
}

### Common Causes
- Missing required fields
- Invalid field format
- Field value out of range

### Resolution
Review the `errors` array for specific field issues.
```

### Implementation Checklist

- [ ] Use RFC 7807 Problem Details format
- [ ] Set Content-Type to `application/problem+json`
- [ ] Include type, title, and status in all errors
- [ ] Use dereferenceable URIs for error types
- [ ] Provide actionable error messages
- [ ] Never expose sensitive information
- [ ] Use machine-readable error codes
- [ ] Support internationalization with message keys
- [ ] Include trace IDs for debugging
- [ ] Document all error types
