# API Patterns - Master Plan

> **Skill Purpose**: Comprehensive guide for designing and implementing APIs across REST, GraphQL, gRPC, and tRPC patterns. Covers framework selection, pagination strategies, OpenAPI documentation, and integration with all frontend skills.
>
> **Date**: December 2025
> **Status**: Planning Phase
> **Research Sources**: FULL_STACK_SKILLS_UNIFIED.md (Context7 research), Anthropic best practices

---

## Strategic Positioning

### The Critical Backend Foundation

**Problem Statement**: Every application needs an API layer, but choosing the right pattern and framework depends on:
- API consumer type (public developers, frontend teams, mobile apps, services)
- Performance requirements (throughput, latency, cold starts)
- Type safety needs (TypeScript end-to-end, schema validation)
- Documentation requirements (auto-generated, interactive)

**Why This Skill Matters**:
- **Universal Need**: 100% of full-stack applications require API implementation
- **Integration Hub**: Connects ALL frontend skills to backend databases and services
- **Multiple Paradigms**: REST, GraphQL, gRPC, tRPC serve different use cases optimally
- **Framework Explosion**: Python, TypeScript, Rust, Go each have distinct best-in-class options

### Position in Full-Stack Ecosystem

```
┌─────────────────────────────────────────────────────────────┐
│            Frontend ← API Patterns → Backend                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  FRONTEND SKILLS          API LAYER         DATA LAYER      │
│  ├── forms            →   POST/PUT      →   databases-*     │
│  ├── tables           →   GET+pagination →  databases-*     │
│  ├── dashboards       →   GET+SSE       →  databases-*     │
│  ├── ai-chat          →   SSE/WebSocket →  databases-vector │
│  ├── search-filter    →   GraphQL       →  databases-*     │
│  ├── media            →   Multipart     →  databases-*     │
│  └── feedback         →   WebSocket     →  message-queues  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Unique Value Proposition

| Capability | Why It Matters |
|------------|----------------|
| Multi-paradigm coverage | Choose optimal pattern per use case (REST vs GraphQL vs gRPC vs tRPC) |
| Language-specific guidance | Best frameworks for Python, TypeScript, Rust, Go |
| Performance benchmarks | Data-driven framework selection (req/s, latency, cold starts) |
| Frontend integration maps | Explicit connections to frontend skill patterns |
| OpenAPI automation | Self-documenting APIs with interactive testing |

---

## Component Taxonomy

### Tier 1: API Paradigms (Architectural Patterns)

#### 1.1 REST (Representational State Transfer)

**When to Use:**
- Public APIs for third-party developers
- CRUD operations with resource-based modeling
- Need for HTTP caching and CDN integration
- Standard browser compatibility required

**Best Frameworks by Language:**

| Language | Framework | Req/s | Latency | Key Strength |
|----------|-----------|-------|---------|--------------|
| **Python** | FastAPI | ~40,000 | 5-10ms | Auto OpenAPI, Pydantic v2 validation |
| **TypeScript** | Hono | ~50,000 | <5ms cold | Edge-first, 14KB, any runtime |
| **Rust** | Axum | ~140,000 | <1ms | Tower middleware, type-safe extractors |
| **Go** | Gin | ~100,000+ | 1-2ms | Largest ecosystem, mature patterns |

**Core Patterns:**
- Resource naming (`/users`, `/posts/{id}`)
- HTTP method semantics (GET, POST, PUT, PATCH, DELETE)
- Status code usage (200, 201, 400, 404, 500)
- Pagination (cursor-based, offset-based, keyset)
- Versioning (URI, header, media type)
- HATEOAS (optional hypermedia)

#### 1.2 GraphQL

**When to Use:**
- Frontend teams need flexible data fetching
- Mobile apps with bandwidth constraints
- Complex, nested data requirements
- Over-fetching/under-fetching problems exist

**Best Frameworks by Language:**

| Language | Library | Key Feature |
|----------|---------|-------------|
| **Python** | Strawberry 0.287 | Type-hint-based schema, async support |
| **Rust** | async-graphql | High performance, built on tokio |
| **Go** | gqlgen | Code generation from schema |
| **TypeScript** | Pothos | Type-safe builder, no codegen needed |

**Core Patterns:**
- Schema definition (types, queries, mutations, subscriptions)
- Resolvers and data loaders (N+1 prevention)
- Query complexity analysis and depth limiting
- Batching and caching strategies
- Error handling (field-level vs top-level)
- Subscriptions for real-time updates

#### 1.3 gRPC (Google Remote Procedure Call)

**When to Use:**
- Service-to-service communication (microservices)
- High-performance requirements
- Strong typing and contract enforcement
- Bidirectional streaming needed

**Best Frameworks by Language:**

| Language | Framework | Key Feature |
|----------|-----------|-------------|
| **Rust** | Tonic | Async, type-safe, code generation |
| **Go** | Connect-Go | gRPC-compatible + browser-friendly |
| **Python** | grpcio | Official implementation |
| **TypeScript** | @connectrpc/connect | Browser + Node.js support |

**Core Patterns:**
- Protocol Buffers (proto3 syntax)
- Service definitions and code generation
- Streaming (unary, server, client, bidirectional)
- Interceptors for middleware
- Error handling and status codes
- TLS and authentication

#### 1.4 tRPC (TypeScript Remote Procedure Call)

**When to Use:**
- Full-stack TypeScript applications
- Same team owns frontend and backend
- Want end-to-end type safety without codegen
- Rapid prototyping with DX priority

**Best Practices:**
- Router-based API organization
- Zod for runtime validation + TS inference
- React Query integration for caching
- Middleware for auth and logging
- Subscription support via WebSocket
- OpenAPI generation (with trpc-openapi plugin)

---

### Tier 2: Framework Selection by Language

#### 2.1 Python REST Frameworks

**FastAPI (Primary Recommendation)**

**Context7 Research:**
| Source | Context7 ID | Trust | Snippets | Score |
|--------|-------------|-------|----------|-------|
| FastAPI Docs | `/websites/fastapi_tiangolo` | High | 29,015 | 79.8 |
| FastAPI Core | `/fastapi/fastapi` | High | 684 | 87.8 |

**Key Features:**
- Automatic OpenAPI/Swagger documentation
- Pydantic v2 validation (10-50x faster)
- Async/await support with Starlette
- Dependency injection system
- WebSocket and SSE support
- Type hints drive validation and docs

**Example Structure:**
```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
```

**When to Use Flask Instead:**
- Lightweight projects with minimal dependencies
- Legacy systems already on Flask
- More control over architecture preferred

#### 2.2 TypeScript/JavaScript Frameworks

**Hono (Edge-First Primary)**

**Context7 Research:**
| Source | Context7 ID | Trust | Snippets | Score |
|--------|-------------|-------|----------|-------|
| Hono llms.txt | `/llmstxt/hono_dev_llms_txt` | High | 1,817 | 92.1 |
| Hono Core | `/honojs/hono` | High | 42 | 87.8 |

**Key Features:**
- 14KB bundle, zero dependencies
- Runs on ANY runtime (Node, Deno, Bun, Cloudflare Workers, Vercel Edge)
- <5ms cold starts on edge
- Express-like API but modern
- Built-in validation with Zod
- OpenAPI generation via middleware

**Example Structure:**
```typescript
import { Hono } from 'hono'
import { z } from 'zod'

const app = new Hono()

const itemSchema = z.object({
  name: z.string(),
  price: z.number().positive()
})

app.post('/items', async (c) => {
  const item = itemSchema.parse(await c.req.json())
  return c.json(item, 201)
})

export default app
```

**tRPC (TypeScript Full-Stack)**

**Context7 Research:**
| Source | Context7 ID | Trust | Snippets | Score |
|--------|-------------|-------|----------|-------|
| tRPC Core | `/trpc/trpc` | High | 900 | 92.7 |
| tRPC Docs | `/websites/trpc_io` | High | 1,068 | 90.2 |

**Key Features:**
- Zero codegen, pure TypeScript inference
- End-to-end type safety (frontend ↔ backend)
- React Query integration
- Subscriptions via WebSocket
- Middleware for auth/logging
- Can expose OpenAPI endpoints

**Example Structure:**
```typescript
import { initTRPC } from '@trpc/server'
import { z } from 'zod'

const t = initTRPC.create()

export const appRouter = t.router({
  getUser: t.procedure
    .input(z.object({ id: z.string() }))
    .query(({ input }) => {
      return { id: input.id, name: 'Alice' }
    }),
  createUser: t.procedure
    .input(z.object({ name: z.string() }))
    .mutation(({ input }) => {
      return { id: '1', name: input.name }
    })
})

export type AppRouter = typeof appRouter
```

#### 2.3 Rust Frameworks

**Axum (Primary Recommendation)**

**Context7 Research:**
| Source | Context7 ID | Trust | Snippets | Score |
|--------|-------------|-------|----------|-------|
| Axum Docs | `/websites/rs_axum_axum` | High | 7,260 | 77.5 |
| Axum Core | `/tokio-rs/axum` | High | 96 | 76.3 |

**Key Features:**
- Built on Tower middleware ecosystem
- Type-safe extractors
- Excellent ergonomics
- ~140,000 req/s, <1ms latency
- WebSocket and SSE support
- Compile-time verification

**Example Structure:**
```rust
use axum::{
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct CreateItem {
    name: String,
    price: f64,
}

#[derive(Serialize)]
struct Item {
    id: u64,
    name: String,
    price: f64,
}

async fn create_item(Json(payload): Json<CreateItem>) -> Json<Item> {
    Json(Item {
        id: 1,
        name: payload.name,
        price: payload.price,
    })
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/items", post(create_item));

    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}
```

**When to Use Actix-web Instead:**
- Need absolute maximum throughput (~150,000 req/s)
- Actor model pattern preferred
- More mature ecosystem required

#### 2.4 Go Frameworks

**Gin (Primary Recommendation)**

**Key Features:**
- Largest Go web framework ecosystem
- ~100,000+ req/s, 1-2ms latency
- Middleware system
- JSON validation with struct tags
- Group routing
- Error management

**Example Structure:**
```go
package main

import (
    "github.com/gin-gonic/gin"
    "net/http"
)

type Item struct {
    ID    uint    `json:"id"`
    Name  string  `json:"name" binding:"required"`
    Price float64 `json:"price" binding:"required,gt=0"`
}

func main() {
    r := gin.Default()

    r.POST("/items", func(c *gin.Context) {
        var item Item
        if err := c.ShouldBindJSON(&item); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }
        item.ID = 1
        c.JSON(http.StatusCreated, item)
    })

    r.Run(":3000")
}
```

---

### Tier 3: Cross-Cutting Concerns

#### 3.1 Pagination Patterns

**Cursor-Based Pagination (Recommended for Scale)**

**Advantages:**
- Handles real-time data changes gracefully
- No skipped/duplicate records during pagination
- Scales to billions of records efficiently
- Works with any sortable column

**Implementation Pattern:**
```python
# FastAPI example
from fastapi import Query
from typing import Optional

@app.get("/items")
async def list_items(
    cursor: Optional[str] = Query(None),
    limit: int = Query(20, le=100)
):
    query = db.query(Item)
    if cursor:
        query = query.filter(Item.id > cursor)
    items = query.limit(limit).all()

    next_cursor = items[-1].id if items else None

    return {
        "items": items,
        "next_cursor": next_cursor,
        "has_more": len(items) == limit
    }
```

**Offset-Based Pagination (Legacy/Simple Cases)**

**Advantages:**
- Simple to implement and understand
- Direct page number access
- Good for static datasets

**Disadvantages:**
- Poor performance on large offsets (OFFSET 1000000)
- Data inconsistencies during pagination
- Not suitable for real-time data

**Implementation Pattern:**
```python
@app.get("/items")
async def list_items(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, le=100)
):
    offset = (page - 1) * per_page
    items = db.query(Item).offset(offset).limit(per_page).all()
    total = db.query(Item).count()

    return {
        "items": items,
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": (total + per_page - 1) // per_page
    }
```

#### 3.2 Rate Limiting

**Token Bucket Algorithm (Recommended)**

**Libraries by Language:**
- **Python**: `slowapi` (FastAPI), `flask-limiter` (Flask)
- **TypeScript**: `express-rate-limit`, Hono middleware
- **Rust**: `tower-governor` (Axum), `actix-governor` (Actix)
- **Go**: `golang.org/x/time/rate`

**Example (FastAPI):**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/items")
@limiter.limit("100/minute")
async def list_items():
    return {"items": []}
```

#### 3.3 Caching Strategies

**HTTP Caching Headers:**
```python
from fastapi import Response

@app.get("/items/{id}")
async def get_item(id: int, response: Response):
    item = db.get(id)

    # Cache for 5 minutes
    response.headers["Cache-Control"] = "public, max-age=300"
    response.headers["ETag"] = f'"{item.version}"'

    return item
```

**Application-Level Caching:**
- **Python**: `cachetools`, Redis
- **TypeScript**: Node-cache, Redis
- **Rust**: `moka`, Redis
- **Go**: `groupcache`, Redis

#### 3.4 API Versioning

**URI Versioning (Most Common):**
```
/api/v1/users
/api/v2/users
```

**Header Versioning (REST Purist):**
```
Accept: application/vnd.myapi.v1+json
```

**Media Type Versioning:**
```
Content-Type: application/vnd.myapi-v2+json
```

**Best Practice**: URI versioning for simplicity, header versioning for strict REST adherence.

#### 3.5 OpenAPI/Swagger Documentation

**Auto-Generation by Framework:**

| Framework | OpenAPI Support | Interactive Docs |
|-----------|----------------|------------------|
| **FastAPI** | Automatic | Swagger UI + ReDoc |
| **Hono** | Middleware plugin | Swagger UI |
| **Axum** | utoipa crate | Swagger UI |
| **Gin** | swaggo/swag | Swagger UI |

**Example (FastAPI - automatic):**
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="My API",
    description="API for managing items",
    version="1.0.0"
)

class Item(BaseModel):
    """Item model with name and price"""
    name: str
    price: float

@app.post("/items", tags=["items"], summary="Create a new item")
async def create_item(item: Item) -> Item:
    """
    Create an item with:
    - **name**: Item name
    - **price**: Item price (must be positive)
    """
    return item

# Docs automatically available at:
# - /docs (Swagger UI)
# - /redoc (ReDoc)
# - /openapi.json (OpenAPI spec)
```

---

## Decision Framework

### Primary Selection: API Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                   API Pattern Selection                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  WHO CONSUMES YOUR API?                                      │
│  ├── PUBLIC / THIRD-PARTY DEVELOPERS                         │
│  │   └─ REST with OpenAPI documentation                      │
│  │       ├─ Python → FastAPI (auto-docs)                    │
│  │       ├─ TypeScript → Hono (edge-first)                  │
│  │       ├─ Rust → Axum (performance)                       │
│  │       └─ Go → Gin (ecosystem)                            │
│  │                                                          │
│  ├── FRONTEND TEAM (same organization)                       │
│  │   ├─ TypeScript full-stack? → tRPC                       │
│  │   │   └─ Zero codegen, E2E type safety                  │
│  │   └─ Complex data needs? → GraphQL                       │
│  │       ├─ Python → Strawberry                             │
│  │       ├─ Rust → async-graphql                            │
│  │       ├─ Go → gqlgen                                     │
│  │       └─ TypeScript → Pothos                             │
│  │                                                          │
│  ├── SERVICE-TO-SERVICE (internal microservices)            │
│  │   ├─ High performance? → gRPC                            │
│  │   │   ├─ Rust → Tonic                                    │
│  │   │   ├─ Go → Connect-Go (browser-friendly)             │
│  │   │   └─ Python → grpcio                                │
│  │   └─ Need browser debugging? → Connect-Go               │
│  │                                                          │
│  └── MOBILE APPS                                             │
│      ├─ Bandwidth constrained? → GraphQL                    │
│      │   └─ Request only needed fields                      │
│      └─ Simple CRUD? → REST                                 │
│          └─ Standard, well-understood                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Secondary Selection: Framework

```
┌─────────────────────────────────────────────────────────────┐
│                REST Framework Selection                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  LANGUAGE PREFERENCE?                                        │
│  ├── PYTHON                                                  │
│  │   ├─ Modern, auto-docs → FastAPI                         │
│  │   ├─ Lightweight → Flask                                 │
│  │   └─ Full-featured → Django REST Framework               │
│  │                                                          │
│  ├── TYPESCRIPT/JAVASCRIPT                                   │
│  │   ├─ Edge deployment → Hono                              │
│  │   ├─ Full-stack TS → tRPC                                │
│  │   ├─ Serverless/AWS → AWS Lambda + API Gateway           │
│  │   └─ Legacy → Express                                    │
│  │                                                          │
│  ├── RUST                                                    │
│  │   ├─ Modern, ergonomic → Axum                            │
│  │   ├─ Maximum perf → Actix-web                            │
│  │   └─ Easy DX → Rocket                                    │
│  │                                                          │
│  └── GO                                                      │
│      ├─ Standard → Gin                                       │
│      ├─ Minimal → net/http (stdlib)                         │
│      └─ Enterprise → Echo or Fiber                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Frontend Integration Mapping

### Frontend Skill → API Pattern Mapping

| Frontend Skill | API Methods | Pattern | Example Endpoints |
|----------------|-------------|---------|-------------------|
| **forms** | POST, PUT, PATCH | REST/tRPC | `/api/users`, `/api/posts` |
| **tables** | GET + pagination | REST/GraphQL | `/api/items?cursor=xyz&limit=20` |
| **data-viz** | GET + aggregation | REST/GraphQL | `/api/metrics/timeseries` |
| **dashboards** | GET + SSE | REST + realtime-sync | `/api/dashboard/kpis`, `/api/events` |
| **ai-chat** | POST + SSE | REST + streaming | `/api/chat/completions` (SSE) |
| **search-filter** | GET/POST + GraphQL | GraphQL/REST | `/api/search?q=query&filters=...` |
| **media** | POST multipart | REST | `/api/upload`, `/api/files/{id}` |
| **feedback** | POST/WebSocket | REST/realtime-sync | `/api/notifications`, `ws://api/updates` |

### Integration Code Examples

#### Forms → FastAPI POST
```python
# Backend (FastAPI)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    age: int

@app.post("/api/users", status_code=201)
async def create_user(user: UserCreate):
    # Validation automatic via Pydantic
    return {"id": 1, **user.dict()}
```

```typescript
// Frontend (React + forms skill)
async function handleSubmit(data: UserForm) {
  const response = await fetch('/api/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail)
  }

  return response.json()
}
```

#### Tables → REST Pagination
```python
# Backend (FastAPI cursor pagination)
from typing import Optional

@app.get("/api/items")
async def list_items(
    cursor: Optional[str] = None,
    limit: int = 20
):
    query = db.query(Item)
    if cursor:
        query = query.filter(Item.id > cursor)

    items = query.limit(limit).all()
    next_cursor = items[-1].id if items else None

    return {
        "items": [item.to_dict() for item in items],
        "next_cursor": next_cursor,
        "has_more": len(items) == limit
    }
```

```typescript
// Frontend (React + tables skill)
async function fetchItems(cursor?: string) {
  const url = cursor
    ? `/api/items?cursor=${cursor}&limit=20`
    : '/api/items?limit=20'

  const response = await fetch(url)
  return response.json()
}
```

#### AI Chat → SSE Streaming
```python
# Backend (FastAPI SSE)
from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse

@app.post("/api/chat/completions")
async def chat_completion(message: str):
    async def event_generator():
        # Simulate streaming LLM response
        for chunk in llm_stream(message):
            yield {
                "event": "message",
                "data": chunk
            }
        yield {"event": "done", "data": "[DONE]"}

    return EventSourceResponse(event_generator())
```

```typescript
// Frontend (React + ai-chat skill)
function streamChatResponse(message: string) {
  const eventSource = new EventSource('/api/chat/completions')

  eventSource.addEventListener('message', (e) => {
    const chunk = e.data
    appendToChat(chunk)
  })

  eventSource.addEventListener('done', () => {
    eventSource.close()
  })
}
```

---

## Performance Benchmarks

### Framework Performance Matrix

| Language | Framework | Requests/sec | Latency | Cold Start | Memory |
|----------|-----------|--------------|---------|------------|---------|
| **Rust** | Actix-web | ~150,000 | <1ms | N/A | 2-5MB |
| **Rust** | Axum | ~140,000 | <1ms | N/A | 2-5MB |
| **Go** | Gin | ~100,000+ | 1-2ms | N/A | 5-10MB |
| **TypeScript** | Hono (edge) | ~50,000 | <5ms | <5ms | 128MB isolate |
| **Python** | FastAPI | ~40,000 | 5-10ms | 1-2s | 30-50MB |
| **TypeScript** | Express | ~15,000 | 10-20ms | 1-3s | 50-100MB |

**Notes:**
- Benchmarks assume single-core, JSON responses
- Actual performance varies with workload complexity
- Cold start only applies to serverless/edge deployments

### When Performance Matters

| Use Case | Recommended | Rationale |
|----------|-------------|-----------|
| **Startup MVP** | FastAPI, Hono, tRPC | Developer experience > raw performance |
| **High-traffic API** | Axum, Actix, Gin | Every ms counts at scale |
| **Edge/CDN** | Hono, Cloudflare Workers | Cold start critical |
| **Microservices** | Axum, Go (gRPC) | Service-to-service efficiency |
| **Public API** | FastAPI, Gin | Auto-docs + performance balance |

---

## GraphQL Specifics

### When GraphQL Makes Sense

**Advantages:**
- Client controls data shape (no over-fetching)
- Single endpoint for complex queries
- Strong typing with schema
- Real-time subscriptions built-in
- Excellent for mobile apps (bandwidth savings)

**Disadvantages:**
- Complexity overhead for simple APIs
- Potential N+1 query problems
- Caching more difficult than REST
- Learning curve for team

### GraphQL Libraries by Language

#### Python: Strawberry

```python
import strawberry
from typing import List

@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: strawberry.ID) -> User:
        return get_user(id)

    @strawberry.field
    def users(self) -> List[User]:
        return get_all_users()

schema = strawberry.Schema(query=Query)
```

#### TypeScript: Pothos

```typescript
import SchemaBuilder from '@pothos/core'

const builder = new SchemaBuilder({})

builder.queryType({
  fields: (t) => ({
    user: t.field({
      type: User,
      args: { id: t.arg.id({ required: true }) },
      resolve: (parent, args) => getUser(args.id)
    })
  })
})

const schema = builder.toSchema()
```

#### Rust: async-graphql

```rust
use async_graphql::{Object, Schema, EmptyMutation, EmptySubscription};

struct User {
    id: i32,
    name: String,
}

#[Object]
impl User {
    async fn id(&self) -> i32 { self.id }
    async fn name(&self) -> &str { &self.name }
}

struct Query;

#[Object]
impl Query {
    async fn user(&self, id: i32) -> User {
        get_user(id)
    }
}

let schema = Schema::build(Query, EmptyMutation, EmptySubscription).finish();
```

#### Go: gqlgen

```go
// schema.graphql
type User {
  id: ID!
  name: String!
}

type Query {
  user(id: ID!): User
}

// resolver.go
func (r *queryResolver) User(ctx context.Context, id string) (*User, error) {
    return getUserByID(id)
}
```

---

## Skill Structure

```
api-patterns/
├── init.md                           # This file - master plan
├── SKILL.md                          # Main skill file (< 500 lines)
├── references/
│   ├── rest-design-principles.md     # REST best practices, resource modeling
│   ├── graphql-schema-design.md      # Schema patterns, resolver optimization
│   ├── grpc-protobuf-guide.md        # Proto3 syntax, service definitions
│   ├── trpc-setup-guide.md           # tRPC router patterns, middleware
│   ├── pagination-patterns.md        # Cursor vs offset, keyset pagination
│   ├── rate-limiting-strategies.md   # Token bucket, sliding window, Redis
│   ├── caching-patterns.md           # HTTP caching, application caching
│   ├── versioning-strategies.md      # URI, header, media type versioning
│   ├── openapi-documentation.md      # Swagger/OpenAPI best practices
│   ├── error-handling.md             # Error codes, problem details (RFC 7807)
│   ├── authentication-integration.md # JWT, OAuth, API keys
│   └── performance-optimization.md   # Connection pooling, query optimization
├── examples/
│   ├── python-fastapi/
│   │   ├── main.py                   # Complete FastAPI app
│   │   ├── models.py                 # Pydantic models
│   │   ├── routers/
│   │   │   ├── users.py
│   │   │   └── items.py
│   │   └── requirements.txt
│   ├── typescript-hono/
│   │   ├── index.ts                  # Hono app
│   │   ├── routes/
│   │   │   ├── users.ts
│   │   │   └── items.ts
│   │   └── package.json
│   ├── typescript-trpc/
│   │   ├── server.ts                 # tRPC server
│   │   ├── routers/
│   │   │   └── app.ts
│   │   ├── client.ts                 # Frontend client
│   │   └── package.json
│   ├── rust-axum/
│   │   ├── main.rs
│   │   ├── routes/
│   │   │   ├── mod.rs
│   │   │   ├── users.rs
│   │   │   └── items.rs
│   │   └── Cargo.toml
│   ├── go-gin/
│   │   ├── main.go
│   │   ├── routes/
│   │   │   ├── users.go
│   │   │   └── items.go
│   │   └── go.mod
│   ├── graphql-strawberry/          # Python GraphQL
│   │   ├── schema.py
│   │   ├── resolvers.py
│   │   └── main.py
│   └── grpc-tonic/                  # Rust gRPC
│       ├── proto/
│       │   └── service.proto
│       ├── src/
│       │   ├── server.rs
│       │   └── client.rs
│       └── Cargo.toml
└── scripts/
    ├── generate_openapi.py          # Generate OpenAPI from code
    ├── validate_api_spec.py         # Validate OpenAPI compliance
    ├── benchmark_endpoints.py       # Load test API endpoints
    └── test_pagination.py           # Validate pagination implementation
```

---

## SKILL.md Frontmatter Template

```yaml
---
name: api-patterns
description: API design and implementation across REST, GraphQL, gRPC, and tRPC patterns. Use when building backend services, public APIs, or service-to-service communication. Covers REST frameworks (FastAPI, Axum, Gin, Hono), GraphQL libraries (Strawberry, async-graphql, gqlgen, Pothos), gRPC (Tonic, Connect-Go), tRPC for TypeScript, pagination strategies (cursor-based, offset-based), rate limiting, caching, versioning, and OpenAPI documentation generation. Includes frontend integration patterns for forms, tables, dashboards, and ai-chat skills.
---
```

---

## Quality Checklist

### Before Creating SKILL.md

#### Core Content
- [ ] All 4 API paradigms covered (REST, GraphQL, gRPC, tRPC)
- [ ] Context7 library data included with IDs and scores
- [ ] Framework recommendations for Python, TypeScript, Rust, Go
- [ ] Performance benchmarks documented (req/s, latency)
- [ ] Frontend skill integration mappings complete
- [ ] Decision framework ASCII diagrams clear and actionable

#### Technical Accuracy
- [ ] FastAPI Context7 ID: `/websites/fastapi_tiangolo` (79.8 score)
- [ ] Hono Context7 ID: `/llmstxt/hono_dev_llms_txt` (92.1 score)
- [ ] Axum Context7 ID: `/websites/rs_axum_axum` (77.5 score)
- [ ] tRPC Context7 ID: `/trpc/trpc` (92.7 score)
- [ ] Pagination patterns: cursor-based (recommended) vs offset-based
- [ ] OpenAPI auto-generation documented per framework

#### Examples & References
- [ ] Complete code examples for each language/framework
- [ ] Pagination implementation examples (cursor + offset)
- [ ] GraphQL schema examples for all 4 languages
- [ ] Frontend integration code snippets
- [ ] Rate limiting implementation patterns
- [ ] OpenAPI documentation examples

#### Progressive Disclosure
- [ ] SKILL.md under 500 lines
- [ ] References organized by topic (one level deep)
- [ ] Scripts executable without loading into context
- [ ] Examples in separate directories
- [ ] Clear signposting to reference files

#### Integration Points
- [ ] Forms skill: POST/PUT patterns documented
- [ ] Tables skill: GET + pagination patterns
- [ ] Dashboards skill: SSE streaming examples
- [ ] AI-chat skill: SSE/WebSocket integration
- [ ] Search-filter skill: GraphQL examples
- [ ] Auth-security skill: JWT/OAuth integration points

### Anthropic Best Practices Compliance

#### Naming & Structure
- [ ] Name: `api-patterns` (lowercase, hyphens, <64 chars)
- [ ] Description: <1024 chars, includes WHAT and WHEN
- [ ] Description in third-person (not "you" or "I")
- [ ] No angle brackets in description
- [ ] File paths use forward slashes only

#### Content Quality
- [ ] No time-sensitive information (or clearly marked)
- [ ] Consistent terminology throughout
- [ ] Examples concrete, not abstract
- [ ] No unnecessary general knowledge
- [ ] Token-efficient content

#### Scripts & Tools
- [ ] Scripts solve problems (don't punt to Claude)
- [ ] Error handling explicit and helpful
- [ ] No "voodoo constants" without explanation
- [ ] Package dependencies listed and verified
- [ ] Clear execution intent (run vs read)

#### Testing Requirements
- [ ] At least 3 evaluation scenarios planned
- [ ] Real-world usage scenarios identified
- [ ] Cross-model testing plan (Haiku, Sonnet, Opus)
- [ ] Performance/token usage acceptable

---

## Implementation Notes

### Critical Patterns to Emphasize

1. **OpenAPI Auto-Generation**: FastAPI and Hono make documentation effortless
2. **Cursor Pagination**: Scalable, handles real-time data changes
3. **tRPC for TypeScript**: Zero-codegen E2E type safety is a game-changer
4. **Framework Performance**: Rust/Go for high-throughput, Python/TS for DX
5. **Frontend Integration**: Explicit mappings show skill interconnections

### Token-Free Validation Scripts

The scripts directory should contain:
- **generate_openapi.py**: Extract OpenAPI spec from code (FastAPI, Axum, etc.)
- **validate_api_spec.py**: Ensure spec compliance with OpenAPI 3.1
- **benchmark_endpoints.py**: Load test to verify performance claims
- **test_pagination.py**: Validate cursor/offset pagination correctness

These scripts execute WITHOUT consuming context tokens - infinite complexity, zero cost.

### Progressive Disclosure Strategy

**SKILL.md** (< 500 lines):
- Overview of 4 paradigms
- Quick decision framework
- Language/framework matrix
- References to detailed guides

**references/** (detailed guides):
- `rest-design-principles.md`: Deep dive on REST patterns
- `graphql-schema-design.md`: Schema best practices, N+1 prevention
- `pagination-patterns.md`: Cursor vs offset with math explanations
- `openapi-documentation.md`: Auto-generation per framework

**examples/** (working code):
- Complete runnable projects for each language/framework
- Integration examples with frontend skills
- Demonstrates patterns in practice

---

## Research Sources Summary

### Context7 Libraries Covered

| Library | Context7 ID | Score | Snippets |
|---------|-------------|-------|----------|
| FastAPI | `/websites/fastapi_tiangolo` | 79.8 | 29,015 |
| FastAPI Core | `/fastapi/fastapi` | 87.8 | 684 |
| Hono | `/llmstxt/hono_dev_llms_txt` | 92.1 | 1,817 |
| Hono Core | `/honojs/hono` | 87.8 | 42 |
| tRPC | `/trpc/trpc` | 92.7 | 900 |
| tRPC Docs | `/websites/trpc_io` | 90.2 | 1,068 |
| Axum Docs | `/websites/rs_axum_axum` | 77.5 | 7,260 |
| Axum Core | `/tokio-rs/axum` | 76.3 | 96 |

### Additional Research

- OpenAPI 3.1 specification
- REST maturity model (Richardson)
- GraphQL best practices (Apollo, The Guild)
- gRPC performance benchmarks
- Cursor pagination algorithms (Relay spec)
- Rate limiting strategies (token bucket, sliding window)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2025-12-02 | Initial master plan created with Context7 research |

---

*This master plan provides the foundation for creating a comprehensive API patterns skill that connects all frontend skills to backend databases and services. The skill will support Python, TypeScript, Rust, and Go with production-ready framework recommendations based on Context7 research and performance benchmarks.*
