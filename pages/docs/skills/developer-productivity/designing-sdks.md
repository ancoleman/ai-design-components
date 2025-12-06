---
sidebar_position: 3
title: Designing SDKs
description: Design developer-friendly software development kits and libraries across multiple programming languages
tags: [developer-productivity, sdk, library-design, api-client, developer-experience]
---

# Designing SDKs

Design developer-friendly software development kits and libraries that provide excellent developer experience across multiple programming languages. Covers API design patterns, language-specific idioms, error handling, testing strategies, and distribution practices for creating SDKs that developers love to use.

## When to Use

Use when:
- Creating client libraries for REST or GraphQL APIs
- Building language-specific wrappers for services
- Designing multi-language SDK offerings
- Implementing authentication and session management in SDKs
- Establishing SDK versioning and deprecation strategies
- Distributing libraries via package managers (npm, PyPI, Maven, Go modules)

## Key Features

### SDK Architecture
- Client design patterns (fluent, builder, factory)
- Authentication and session management
- Request/response handling and serialization
- Error handling and retry logic
- Async vs sync API design

### Language-Specific Design
- JavaScript/TypeScript SDK patterns with type safety
- Python SDK conventions following PEP 8
- Go SDK idioms and package design
- Java/Kotlin enterprise patterns
- Ruby, PHP, .NET considerations

### Developer Experience
- Intuitive API surface design
- Type safety and IntelliSense support
- Sensible defaults and configuration
- Rich examples and code snippets
- Clear migration guides between versions

### Error Handling
- Exception hierarchy design
- Meaningful error codes and messages
- Validation and early failure patterns
- Logging and debugging support
- Retry strategies and circuit breakers

## Quick Start

### TypeScript SDK Example

```typescript
// Fluent API design with builder pattern
export class APIClient {
  private baseURL: string;
  private apiKey: string;
  private timeout: number = 30000;

  constructor(config: APIConfig) {
    this.baseURL = config.baseURL;
    this.apiKey = config.apiKey;
    if (config.timeout) this.timeout = config.timeout;
  }

  async getUser(id: string): Promise<User> {
    const response = await this.request<User>(`/users/${id}`);
    return response.data;
  }

  private async request<T>(
    endpoint: string,
    options?: RequestOptions
  ): Promise<APIResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json',
    };

    try {
      const response = await fetch(url, { headers, ...options });
      if (!response.ok) {
        throw new APIError(response.status, await response.text());
      }
      return await response.json();
    } catch (error) {
      throw this.handleError(error);
    }
  }

  private handleError(error: unknown): APIError {
    if (error instanceof APIError) return error;
    return new APIError(500, 'Unknown error occurred');
  }
}

// Usage
const client = new APIClient({
  baseURL: 'https://api.example.com',
  apiKey: process.env.API_KEY,
  timeout: 5000
});

const user = await client.getUser('123');
```

### Python SDK Example

```python
from typing import Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class APIClient:
    """Client for Example API with automatic retries."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.example.com",
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout

        # Configure session with retry logic
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get_user(self, user_id: str) -> dict:
        """Get user by ID.

        Args:
            user_id: The user's unique identifier

        Returns:
            User data dictionary

        Raises:
            APIError: If the request fails
        """
        return self._request("GET", f"/users/{user_id}")

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> dict:
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = self.session.request(
                method,
                url,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise APIError(f"HTTP {e.response.status_code}: {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

class APIError(Exception):
    """Exception raised for API errors."""
    pass

# Usage
client = APIClient(api_key="your-api-key")
user = client.get_user("123")
```

## Primary Tools & Technologies

- **JavaScript/TypeScript**: Axios, node-fetch, TypeScript compiler, TypeDoc
- **Python**: Requests, httpx, Pydantic, Poetry, Sphinx
- **Go**: net/http, Go modules, GoDoc
- **Java**: OkHttp, Jackson, Maven/Gradle, JavaDoc
- **Testing**: Jest, pytest, Go testing, JUnit

## SDK Design Patterns

### Builder Pattern
Fluent API design for complex configuration:
```typescript
const client = new APIClientBuilder()
  .withBaseURL('https://api.example.com')
  .withAPIKey(process.env.API_KEY)
  .withTimeout(5000)
  .withRetries(3)
  .build();
```

### Factory Pattern
Create specialized clients from a common interface:
```python
class APIClientFactory:
    @staticmethod
    def create_client(environment: str) -> APIClient:
        if environment == "production":
            return APIClient(base_url="https://api.example.com")
        else:
            return APIClient(base_url="https://staging-api.example.com")
```

## Distribution & Versioning

### Package Manager Publishing

**npm (JavaScript/TypeScript):**
```bash
npm publish
```

**PyPI (Python):**
```bash
python -m build
twine upload dist/*
```

**Maven Central (Java):**
```bash
mvn clean deploy
```

**Go Modules:**
```bash
git tag v1.0.0
git push origin v1.0.0
```

### Semantic Versioning
- **MAJOR**: Breaking changes (v2.0.0)
- **MINOR**: New features, backward compatible (v1.1.0)
- **PATCH**: Bug fixes, backward compatible (v1.0.1)

## Related Skills

- [Designing APIs](./designing-apis) - SDKs wrap and consume APIs
- [Generating Documentation](./generating-documentation) - Auto-generate SDK reference docs
- [Building CLIs](./building-clis) - CLIs can use SDKs internally
- [Debugging Techniques](./debugging-techniques) - SDK debugging patterns

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/sdk-design)
- [Master Plan](../../master-plans/developer-productivity/designing-sdks)
