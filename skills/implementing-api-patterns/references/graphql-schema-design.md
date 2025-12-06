# GraphQL Schema Design

## Overview

GraphQL provides a query language for APIs with strong typing and flexible data fetching. This guide covers schema patterns, resolver optimization, and N+1 query prevention.

## Table of Contents

- [Core Concepts](#core-concepts)
- [Schema Definition](#schema-definition)
- [Resolver Patterns](#resolver-patterns)
- [N+1 Problem and DataLoader](#n1-problem-and-dataloader)
- [Error Handling](#error-handling)
- [Pagination](#pagination)
- [Subscriptions](#subscriptions)

## Core Concepts

### When to Use GraphQL

✅ **Use GraphQL when:**
- Frontend needs flexible data fetching
- Mobile apps with bandwidth constraints
- Complex, nested data requirements
- Over-fetching/under-fetching problems exist
- Multiple clients need different data shapes

❌ **Avoid GraphQL when:**
- Simple CRUD operations suffice
- No need for flexible queries
- Team lacks GraphQL experience
- Caching requirements are complex

### GraphQL vs REST

| Feature | GraphQL | REST |
|---------|---------|------|
| **Flexibility** | Request exact data needed | Fixed endpoint responses |
| **Versioning** | Single endpoint, evolve schema | Multiple versions (v1, v2) |
| **Over-fetching** | No - request only needed fields | Yes - endpoints return fixed data |
| **Under-fetching** | No - request nested data in one query | Yes - multiple requests needed |
| **Caching** | More complex (field-level) | Simple (URL-based) |
| **Learning curve** | Higher | Lower |

## Schema Definition

### Python: Strawberry

```python
import strawberry
from typing import List, Optional

@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str
    posts: List['Post']

@strawberry.type
class Post:
    id: strawberry.ID
    title: str
    content: str
    author: User

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: strawberry.ID) -> Optional[User]:
        return get_user(id)

    @strawberry.field
    def users(self) -> List[User]:
        return get_all_users()

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, name: str, email: str) -> User:
        return create_user_in_db(name, email)

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

### TypeScript: Pothos

```typescript
import SchemaBuilder from '@pothos/core'

const builder = new SchemaBuilder({})

builder.objectType('User', {
  fields: (t) => ({
    id: t.exposeID('id'),
    name: t.exposeString('name'),
    email: t.exposeString('email'),
    posts: t.field({
      type: [Post],
      resolve: (user) => getPostsByUserId(user.id)
    })
  })
})

builder.objectType('Post', {
  fields: (t) => ({
    id: t.exposeID('id'),
    title: t.exposeString('title'),
    content: t.exposeString('content'),
    author: t.field({
      type: User,
      resolve: (post) => getUserById(post.authorId)
    })
  })
})

builder.queryType({
  fields: (t) => ({
    user: t.field({
      type: User,
      nullable: true,
      args: { id: t.arg.id({ required: true }) },
      resolve: (parent, args) => getUserById(args.id)
    }),
    users: t.field({
      type: [User],
      resolve: () => getAllUsers()
    })
  })
})

builder.mutationType({
  fields: (t) => ({
    createUser: t.field({
      type: User,
      args: {
        name: t.arg.string({ required: true }),
        email: t.arg.string({ required: true })
      },
      resolve: (parent, args) => createUser(args)
    })
  })
})

const schema = builder.toSchema()
```

### Rust: async-graphql

```rust
use async_graphql::{Object, Schema, EmptySubscription};

struct User {
    id: i32,
    name: String,
    email: String,
}

#[Object]
impl User {
    async fn id(&self) -> i32 { self.id }
    async fn name(&self) -> &str { &self.name }
    async fn email(&self) -> &str { &self.email }

    async fn posts(&self) -> Vec<Post> {
        get_posts_by_user_id(self.id)
    }
}

struct Query;

#[Object]
impl Query {
    async fn user(&self, id: i32) -> Option<User> {
        get_user(id)
    }

    async fn users(&self) -> Vec<User> {
        get_all_users()
    }
}

struct Mutation;

#[Object]
impl Mutation {
    async fn create_user(&self, name: String, email: String) -> User {
        create_user_in_db(name, email)
    }
}

let schema = Schema::build(Query, Mutation, EmptySubscription).finish();
```

## Resolver Patterns

### Field Resolvers

Resolve individual fields (not just top-level queries):

```python
@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str

    @strawberry.field
    async def posts(self) -> List['Post']:
        # Resolve posts field when requested
        return await db.posts.find(author_id=self.id)

    @strawberry.field
    async def followers(self) -> List['User']:
        # Resolve followers only if requested
        follower_ids = await db.follows.find(following_id=self.id)
        return await db.users.find(id__in=follower_ids)
```

**Client can request exactly what they need:**
```graphql
query {
  user(id: "123") {
    name
    # posts field NOT requested - resolver NOT called
  }
}

query {
  user(id: "123") {
    name
    posts {  # NOW posts resolver is called
      title
    }
  }
}
```

### Context Pattern

Share data across resolvers:

```python
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI, Depends

async def get_context(
    request: Request,
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    return {
        "request": request,
        "db": db,
        "user": user
    }

@strawberry.type
class Query:
    @strawberry.field
    async def current_user(self, info: strawberry.Info) -> User:
        # Access context
        return info.context["user"]

app = FastAPI()
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")
```

## N+1 Problem and DataLoader

### The N+1 Problem

**Problem:** Fetching a list and then fetching related data for each item results in N+1 queries.

```python
# BAD: N+1 queries
@strawberry.type
class User:
    id: strawberry.ID
    name: str

    @strawberry.field
    async def posts(self) -> List[Post]:
        # If querying 10 users, this runs 10 times!
        return await db.posts.find(author_id=self.id)

# Query
query {
  users {        # 1 query
    name
    posts {      # N queries (one per user)
      title
    }
  }
}
# Total: 1 + N queries
```

### Solution: DataLoader

**DataLoader** batches and caches requests:

```python
from strawberry.dataloader import DataLoader

async def load_posts_batch(user_ids: List[int]) -> List[List[Post]]:
    # Single query for all users' posts
    posts = await db.posts.find(author_id__in=user_ids)

    # Group by user_id
    posts_by_user = {}
    for post in posts:
        if post.author_id not in posts_by_user:
            posts_by_user[post.author_id] = []
        posts_by_user[post.author_id].append(post)

    # Return in same order as user_ids
    return [posts_by_user.get(uid, []) for uid in user_ids]

# Create DataLoader
posts_loader = DataLoader(load_fn=load_posts_batch)

@strawberry.type
class User:
    id: strawberry.ID
    name: str

    @strawberry.field
    async def posts(self, info: strawberry.Info) -> List[Post]:
        # DataLoader batches requests
        loader = info.context["posts_loader"]
        return await loader.load(self.id)

# In context
async def get_context():
    return {
        "posts_loader": DataLoader(load_fn=load_posts_batch)
    }

# Now querying 10 users = 2 queries total (1 for users, 1 for all posts)
```

### TypeScript DataLoader

```typescript
import DataLoader from 'dataloader'

const postsLoader = new DataLoader(async (userIds: number[]) => {
  // Single query for all users
  const posts = await db.post.findMany({
    where: { authorId: { in: userIds } }
  })

  // Group by authorId
  const postsByUser = new Map<number, Post[]>()
  posts.forEach(post => {
    if (!postsByUser.has(post.authorId)) {
      postsByUser.set(post.authorId, [])
    }
    postsByUser.get(post.authorId)!.push(post)
  })

  // Return in order
  return userIds.map(id => postsByUser.get(id) || [])
})

// In resolver
builder.objectType('User', {
  fields: (t) => ({
    posts: t.field({
      type: [Post],
      resolve: async (user, args, ctx) => {
        return ctx.postsLoader.load(user.id)
      }
    })
  })
})
```

## Error Handling

### Field-Level Errors

GraphQL allows partial success - some fields can error while others succeed:

```python
@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: strawberry.ID) -> Optional[User]:
        user = await db.users.find_one(id=id)
        if not user:
            # Return null - error in response
            return None
        return user

    @strawberry.field
    async def risky_data(self) -> str:
        # Field raises error but other fields still resolve
        raise Exception("This field failed")
```

**Response:**
```json
{
  "data": {
    "user": { "name": "Alice" },
    "riskyData": null
  },
  "errors": [
    {
      "message": "This field failed",
      "path": ["riskyData"]
    }
  ]
}
```

### Custom Errors

```python
from strawberry.types import Info

class NotFoundError(Exception):
    pass

class PermissionError(Exception):
    pass

@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: strawberry.ID, info: Info) -> User:
        user = await db.users.find_one(id=id)

        if not user:
            raise NotFoundError(f"User {id} not found")

        if not can_view_user(info.context["user"], user):
            raise PermissionError("Cannot view this user")

        return user
```

## Pagination

### Relay Cursor Connections

Standard pattern for pagination:

```python
@strawberry.type
class PageInfo:
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]

@strawberry.type
class UserEdge:
    cursor: str
    node: User

@strawberry.type
class UserConnection:
    edges: List[UserEdge]
    page_info: PageInfo

@strawberry.type
class Query:
    @strawberry.field
    async def users(
        self,
        first: Optional[int] = None,
        after: Optional[str] = None
    ) -> UserConnection:
        # Decode cursor
        start_id = decode_cursor(after) if after else 0

        # Fetch first + 1 to check for next page
        users = await db.users.find(
            id__gt=start_id
        ).limit((first or 20) + 1)

        has_next = len(users) > (first or 20)
        if has_next:
            users = users[:first or 20]

        edges = [
            UserEdge(
                cursor=encode_cursor(user.id),
                node=user
            )
            for user in users
        ]

        return UserConnection(
            edges=edges,
            page_info=PageInfo(
                has_next_page=has_next,
                has_previous_page=after is not None,
                start_cursor=edges[0].cursor if edges else None,
                end_cursor=edges[-1].cursor if edges else None
            )
        )

# Query
query {
  users(first: 10, after: "cursor123") {
    edges {
      cursor
      node {
        name
        email
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Offset Pagination (Simpler Alternative)

```python
@strawberry.type
class UserPage:
    items: List[User]
    total: int
    page: int
    per_page: int

@strawberry.type
class Query:
    @strawberry.field
    async def users(
        self,
        page: int = 1,
        per_page: int = 20
    ) -> UserPage:
        offset = (page - 1) * per_page
        users = await db.users.find().skip(offset).limit(per_page)
        total = await db.users.count()

        return UserPage(
            items=users,
            total=total,
            page=page,
            per_page=per_page
        )
```

## Subscriptions

Real-time updates via WebSocket:

```python
import strawberry
from typing import AsyncIterator

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def post_created(self) -> AsyncIterator[Post]:
        # Subscribe to events
        async for post in event_stream('post_created'):
            yield post

    @strawberry.subscription
    async def comment_added(self, post_id: strawberry.ID) -> AsyncIterator[Comment]:
        async for comment in event_stream('comment_added'):
            if comment.post_id == post_id:
                yield comment

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)
```

**Client subscription:**
```graphql
subscription {
  postCreated {
    id
    title
    author {
      name
    }
  }
}
```

## Best Practices

1. **Use DataLoader for N+1 prevention** - Essential for performance
2. **Design schema from client perspective** - Think about what data clients need
3. **Avoid exposing database structure** - Schema should match domain model
4. **Use pagination for lists** - Relay connections for consistency
5. **Field-level authorization** - Check permissions in resolvers
6. **Deprecate fields instead of removing** - GraphQL introspection shows deprecated fields
7. **Limit query complexity** - Prevent malicious deep queries
8. **Enable query depth limiting** - Prevent overly nested queries
9. **Cache at field level** - Use DataLoader caching
10. **Document schema** - Use descriptions for fields and types

## Query Complexity Analysis

Prevent expensive queries:

```python
from strawberry.extensions import QueryDepthLimiter

schema = strawberry.Schema(
    query=Query,
    extensions=[
        QueryDepthLimiter(max_depth=10)
    ]
)
```

This prevents queries like:
```graphql
query {
  user {
    posts {
      author {
        posts {
          author {
            posts {  # Too deep!
              # ...
            }
          }
        }
      }
    }
  }
}
```
