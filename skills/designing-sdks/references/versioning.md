# SDK Versioning and Deprecation

Guide to semantic versioning, deprecation strategies, and API version pinning.

## Semantic Versioning (SemVer)

Follow `MAJOR.MINOR.PATCH`:

- **MAJOR**: Breaking changes (2.0.0)
- **MINOR**: New features, backward compatible (1.1.0)
- **PATCH**: Bug fixes (1.0.1)

### Examples

```
1.0.0 → 1.0.1  Bug fix (safe to update)
1.0.0 → 1.1.0  New feature (safe to update)
1.0.0 → 2.0.0  Breaking change (review before updating)
```

## Deprecation Pattern

### TypeScript Decorator

```typescript
function deprecated(message: string, since: string) {
  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value

    descriptor.value = function (...args: any[]) {
      console.warn(
        `[DEPRECATED] ${propertyKey} is deprecated since ${since}.\n${message}`
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

### Python Decorator

```python
import warnings
from functools import wraps

def deprecated(message: str, since: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated since {since}. {message}",
                DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator

class UsersResource:
    @deprecated("Use users.list() instead", "v2.0.0")
    def get_all(self):
        return self.list()
```

## API Version Pinning

```typescript
const client = new APIClient({
  apiKey: 'sk_test_...',
  apiVersion: '2025-01-01'
})

// SDK sends version in header
headers: {
  'API-Version': '2025-01-01'
}
```
