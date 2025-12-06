# Pagination Patterns

Implementation guide for offset-based, cursor-based, and keyset pagination.


## Table of Contents

- [Pattern Comparison](#pattern-comparison)
- [Offset-Based Pagination](#offset-based-pagination)
  - [Request Format](#request-format)
  - [Response Format](#response-format)
  - [SQL Implementation](#sql-implementation)
  - [Best Practices](#best-practices)
- [Cursor-Based Pagination](#cursor-based-pagination)
  - [Request Format](#request-format)
  - [Response Format](#response-format)
  - [SQL Implementation](#sql-implementation)
  - [Cursor Encoding/Decoding](#cursor-encodingdecoding)
  - [Best Practices](#best-practices)
- [Keyset Pagination](#keyset-pagination)
  - [Request Format](#request-format)
  - [Response Format](#response-format)
  - [SQL Implementation](#sql-implementation)
  - [Best Practices](#best-practices)
- [Link Headers (Optional)](#link-headers-optional)
- [GraphQL Pagination (Relay Spec)](#graphql-pagination-relay-spec)
- [Best Practices Checklist](#best-practices-checklist)

## Pattern Comparison

| Pattern | Use Case | Pros | Cons |
|---------|----------|------|------|
| Offset-based | Small datasets, page numbers | Simple, predictable | Slow at scale, inconsistent |
| Cursor-based | Large datasets, feeds | Efficient, consistent | No page jumping |
| Keyset | Sorted data | Efficient, stable | Complex, requires index |

## Offset-Based Pagination

### Request Format

```http
GET /users?limit=20&offset=40
GET /users?limit=20&page=3  (alternative)
```

### Response Format

```json
{
  "data": [
    { "id": "41", "username": "user41" },
    { "id": "42", "username": "user42" }
  ],
  "pagination": {
    "limit": 20,
    "offset": 40,
    "total": 1543,
    "totalPages": 78,
    "currentPage": 3,
    "hasNext": true,
    "hasPrevious": true
  }
}
```

### SQL Implementation

```sql
SELECT * FROM users
ORDER BY id ASC
LIMIT 20 OFFSET 40;
```

### Best Practices

- Default limit: 20-50 items
- Maximum limit: 100-200 items
- Always include total count (if feasible)
- Use `hasNext` / `hasPrevious` booleans

## Cursor-Based Pagination

### Request Format

```http
GET /users?limit=20&cursor=eyJpZCI6MTIzfQ==
```

Cursor is base64-encoded JSON:
```javascript
const cursor = { id: 123, timestamp: "2025-12-03T10:00:00Z" };
const encoded = Buffer.from(JSON.stringify(cursor)).toString('base64');
// eyJpZCI6MTIzLCJ0aW1lc3RhbXAiOiIyMDI1LTEyLTAzVDEwOjAwOjAwWiJ9
```

### Response Format

```json
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6MTQzfQ==",
    "prevCursor": "eyJpZCI6MTAzfQ==",
    "hasNext": true,
    "hasPrevious": true
  }
}
```

### SQL Implementation

```sql
-- Forward pagination
SELECT * FROM users
WHERE id > 123
ORDER BY id ASC
LIMIT 20;

-- Backward pagination
SELECT * FROM users
WHERE id < 123
ORDER BY id DESC
LIMIT 20;
```

### Cursor Encoding/Decoding

```javascript
// Encode cursor
function encodeCursor(data) {
  return Buffer.from(JSON.stringify(data)).toString('base64');
}

// Decode cursor
function decodeCursor(cursor) {
  return JSON.parse(Buffer.from(cursor, 'base64').toString('utf8'));
}

// Usage
const cursor = encodeCursor({ id: 123, createdAt: "2025-12-03T10:00:00Z" });
const decoded = decodeCursor(cursor);
```

### Best Practices

- Encode position info, not just ID
- Include sort field in cursor
- Validate cursor format
- Handle invalid/expired cursors gracefully

## Keyset Pagination

### Request Format

```http
GET /posts?limit=20&after_id=456&after_created_at=2025-12-03T10:00:00Z
```

### Response Format

```json
{
  "data": [...],
  "pagination": {
    "nextId": 476,
    "nextCreatedAt": "2025-12-03T11:00:00Z",
    "hasNext": true
  }
}
```

### SQL Implementation

```sql
SELECT * FROM posts
WHERE (created_at, id) > ('2025-12-03T10:00:00Z', 456)
ORDER BY created_at ASC, id ASC
LIMIT 20;

-- Requires composite index
CREATE INDEX idx_posts_pagination ON posts(created_at, id);
```

### Best Practices

- Always use unique tiebreaker (e.g., id)
- Create composite index on sort columns
- Use same sort order for consistency

## Link Headers (Optional)

Provide pagination links in headers:

```http
Link: </users?limit=20&cursor=abc123>; rel="next",
      </users?limit=20&cursor=xyz789>; rel="prev",
      </users?limit=20>; rel="first"
```

## GraphQL Pagination (Relay Spec)

```graphql
type Query {
  users(
    first: Int
    after: String
    last: Int
    before: String
  ): UserConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int
}

type UserEdge {
  cursor: String!
  node: User!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

## Best Practices Checklist

- [ ] Set reasonable default and max limits
- [ ] Include pagination metadata
- [ ] Support both forward and backward pagination
- [ ] Handle empty result sets gracefully
- [ ] Validate pagination parameters
- [ ] Use indexes for efficiency
- [ ] Document pagination behavior
- [ ] Consider total count performance impact
