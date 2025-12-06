# Pagination Patterns

Guide to implementing cursor-based and offset-based pagination with async iterators.

## Table of Contents

1. [Async Iterator Pattern](#async-iterator-pattern-recommended)
2. [Manual Pagination](#manual-pagination)
3. [Go Pagination with Channels](#go-pagination-with-channels)

## Async Iterator Pattern (Recommended)

### TypeScript Implementation

```typescript
class UsersResource {
  async *list(options?: { limit?: number }): AsyncGenerator<User> {
    let cursor: string | undefined = undefined

    while (true) {
      const response = await this.client.request<ListResponse>('GET', '/users', {
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

// Usage
for await (const user of client.users.list({ limit: 50 })) {
  console.log(user.id, user.email)
}
```

### Python Implementation

```python
from typing import AsyncGenerator, Generator, Optional

class UsersResource:
    # Sync iterator
    def list(self, limit: int = 100) -> Generator[User, None, None]:
        cursor = None

        while True:
            response = self._client.request('GET', '/users', query={
                'limit': limit,
                **({"cursor': cursor} if cursor else {})
            })

            for user in response['data']:
                yield user

            if not response.get('has_more'):
                break
            cursor = response.get('next_cursor')

    # Async iterator
    async def list_async(self, limit: int = 100) -> AsyncGenerator[User, None]:
        cursor = None

        while True:
            response = await self._client.request('GET', '/users', query={
                'limit': limit,
                **({"cursor': cursor} if cursor else {})
            })

            for user in response['data']:
                yield user

            if not response.get('has_more'):
                break
            cursor = response.get('next_cursor')

# Usage
for user in client.users.list(limit=50):
    print(user.id, user.email)

# Async
async for user in client.users.list_async(limit=50):
    print(user.id, user.email)
```

## Manual Pagination

### Cursor-Based

```typescript
interface ListResponse<T> {
  data: T[]
  has_more: boolean
  next_cursor?: string
}

async function paginateManually() {
  let cursor: string | undefined = undefined
  let hasMore = true

  while (hasMore) {
    const response = await client.users.list({ limit: 100, cursor })

    for (const user of response.data) {
      console.log(user.id)
    }

    cursor = response.next_cursor
    hasMore = response.has_more
  }
}
```

### Offset-Based

```typescript
async function paginateWithOffset() {
  let page = 1
  let totalPages = Infinity

  while (page <= totalPages) {
    const response = await client.users.list({ page, perPage: 100 })

    for (const user of response.data) {
      console.log(user.id)
    }

    totalPages = response.total_pages
    page++
  }
}
```

## Go Pagination with Channels

```go
func (r *UsersResource) List(ctx context.Context, limit int) (<-chan User, <-chan error) {
    userCh := make(chan User)
    errCh := make(chan error, 1)

    go func() {
        defer close(userCh)
        defer close(errCh)

        cursor := ""
        for {
            query := map[string]string{"limit": strconv.Itoa(limit)}
            if cursor != "" {
                query["cursor"] = cursor
            }

            response, err := r.client.request(ctx, "GET", "/users", query)
            if err != nil {
                errCh <- err
                return
            }

            for _, user := range response.Data {
                select {
                case <-ctx.Done():
                    errCh <- ctx.Err()
                    return
                case userCh <- user:
                }
            }

            if !response.HasMore {
                break
            }
            cursor = response.NextCursor
        }
    }()

    return userCh, errCh
}
```
