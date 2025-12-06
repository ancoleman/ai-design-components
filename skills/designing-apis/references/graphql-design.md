# GraphQL API Design

Schema design, N+1 problem solutions, and GraphQL best practices.


## Table of Contents

- [Schema Design Principles](#schema-design-principles)
  - [Type System](#type-system)
  - [Queries, Mutations, Subscriptions](#queries-mutations-subscriptions)
- [N+1 Query Problem](#n1-query-problem)
  - [The Problem](#the-problem)
  - [Solution: DataLoader](#solution-dataloader)
- [Pagination in GraphQL](#pagination-in-graphql)
  - [Relay Connection Specification](#relay-connection-specification)
  - [Query Example](#query-example)
  - [Response Example](#response-example)
- [Error Handling](#error-handling)
  - [Partial Errors](#partial-errors)
  - [Custom Error Codes](#custom-error-codes)
- [Best Practices](#best-practices)
  - [Schema Design](#schema-design)
  - [Performance](#performance)
  - [Error Handling](#error-handling)
  - [Security](#security)

## Schema Design Principles

### Type System

```graphql
# Scalar types
scalar DateTime
scalar URL
scalar Email

# Object types
type User {
  id: ID!              # Non-null ID
  username: String!    # Non-null string
  email: Email!
  bio: String          # Nullable
  avatar: URL
  createdAt: DateTime!

  # Relationships
  posts(limit: Int, offset: Int): [Post!]!
  followers(first: Int, after: String): UserConnection!
}

type Post {
  id: ID!
  title: String!
  content: String!
  published: Boolean!

  # Relationships
  author: User!
  comments: [Comment!]!
  tags: [String!]!
}

# Enums
enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

# Input types
input CreateUserInput {
  username: String!
  email: Email!
  password: String!
  bio: String
}

input UpdateUserInput {
  email: Email
  bio: String
}
```

### Queries, Mutations, Subscriptions

```graphql
type Query {
  # Single resource
  user(id: ID!): User
  post(id: ID!): Post

  # Collections
  users(limit: Int, offset: Int, status: String): [User!]!
  posts(authorId: ID, published: Boolean): [Post!]!

  # Search
  searchUsers(query: String!): [User!]!
}

type Mutation {
  # User mutations
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!

  # Post mutations
  createPost(input: CreatePostInput!): Post!
  publishPost(id: ID!): Post!
}

type Subscription {
  # Real-time updates
  postCreated: Post!
  userStatusChanged(userId: ID!): User!
  commentAdded(postId: ID!): Comment!
}
```

## N+1 Query Problem

### The Problem

```graphql
query {
  posts {           # 1 query: Get all posts
    id
    title
    author {        # N queries: Get author for EACH post
      id
      username
    }
  }
}
```

If there are 100 posts, this triggers 101 database queries (1 + 100).

### Solution: DataLoader

**DataLoader batches and caches requests:**

```javascript
const DataLoader = require('dataloader');

// Create loader
const userLoader = new DataLoader(async (userIds) => {
  // Single query for all users
  const users = await db.users.findByIds(userIds);

  // Return in same order as userIds
  return userIds.map(id =>
    users.find(user => user.id === id)
  );
});

// Resolvers use loader
const resolvers = {
  Post: {
    author: (post) => userLoader.load(post.authorId)
  }
};
```

**What happens:**
1. Query requests 100 posts
2. Each post needs author → 100 calls to `userLoader.load()`
3. DataLoader batches all 100 IDs → 1 database query
4. Results cached for request duration

## Pagination in GraphQL

### Relay Connection Specification

```graphql
type Query {
  users(
    first: Int          # Forward pagination
    after: String       # Cursor
    last: Int           # Backward pagination
    before: String      # Cursor
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

### Query Example

```graphql
query {
  users(first: 10, after: "cursor123") {
    edges {
      cursor
      node {
        id
        username
        email
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
    totalCount
  }
}
```

### Response Example

```json
{
  "data": {
    "users": {
      "edges": [
        {
          "cursor": "cursor_1",
          "node": {
            "id": "1",
            "username": "alice",
            "email": "alice@example.com"
          }
        }
      ],
      "pageInfo": {
        "hasNextPage": true,
        "endCursor": "cursor_10"
      },
      "totalCount": 1543
    }
  }
}
```

## Error Handling

### Partial Errors

GraphQL returns partial data with errors array:

```json
{
  "data": {
    "user": {
      "id": "123",
      "username": "alice",
      "posts": null
    }
  },
  "errors": [
    {
      "message": "Failed to load posts",
      "path": ["user", "posts"],
      "extensions": {
        "code": "DATABASE_ERROR",
        "timestamp": "2025-12-03T10:30:00Z"
      }
    }
  ]
}
```

### Custom Error Codes

```javascript
class NotFoundError extends Error {
  constructor(message, resource) {
    super(message);
    this.extensions = {
      code: 'NOT_FOUND',
      resource: resource
    };
  }
}

// In resolver
if (!user) {
  throw new NotFoundError('User not found', 'user');
}
```

## Best Practices

### Schema Design
- [ ] Use non-null (!) for required fields
- [ ] Use custom scalars (DateTime, URL, Email)
- [ ] Group related fields in types
- [ ] Use enums for fixed sets of values
- [ ] Provide input types for mutations

### Performance
- [ ] Implement DataLoader for all relationships
- [ ] Use connection pattern for pagination
- [ ] Limit query depth and complexity
- [ ] Implement query cost analysis
- [ ] Cache expensive resolvers

### Error Handling
- [ ] Return partial data when possible
- [ ] Use custom error codes
- [ ] Include helpful error messages
- [ ] Log errors server-side

### Security
- [ ] Validate all inputs
- [ ] Implement authorization in resolvers
- [ ] Limit query depth
- [ ] Implement query complexity limits
- [ ] Use persisted queries for production
