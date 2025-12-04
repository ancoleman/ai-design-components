---
sidebar_position: 1
title: API Patterns
description: API design and implementation across REST, GraphQL, gRPC, and tRPC patterns
tags: [backend, api, rest, graphql, grpc, trpc]
---

# API Patterns

API design and implementation using the optimal pattern and framework for your use case. Choose between REST, GraphQL, gRPC, and tRPC based on API consumers, performance requirements, and type safety needs.

## When to Use

Use when:
- Building backend APIs for web, mobile, or service consumers
- Connecting frontend components (forms, tables, dashboards) to databases
- Implementing pagination, rate limiting, or caching strategies
- Generating OpenAPI documentation automatically
- Choosing between REST, GraphQL, gRPC, or tRPC patterns
- Integrating authentication and authorization
- Optimizing API performance and scalability

## Multi-Language Support

This skill provides patterns for:
- **Python**: FastAPI (auto OpenAPI docs, 40k req/s)
- **TypeScript**: Hono (edge-first, 50k req/s, 14KB), tRPC (E2E type safety)
- **Rust**: Axum (140k req/s, &lt;1ms latency)
- **Go**: Gin (100k+ req/s, mature ecosystem)

## Quick Decision Framework

```
WHO CONSUMES YOUR API?
├─ PUBLIC/THIRD-PARTY DEVELOPERS → REST with OpenAPI
│  ├─ Python → FastAPI (auto-docs, 40k req/s)
│  ├─ TypeScript → Hono (edge-first, 50k req/s, 14KB)
│  ├─ Rust → Axum (140k req/s, &lt;1ms latency)
│  └─ Go → Gin (100k+ req/s, mature ecosystem)
│
├─ FRONTEND TEAM (same org)
│  ├─ TypeScript full-stack? → tRPC (E2E type safety)
│  └─ Complex data needs? → GraphQL
│
├─ SERVICE-TO-SERVICE (microservices)
│  └─ High performance → gRPC
│
└─ MOBILE APPS
   ├─ Bandwidth constrained → GraphQL (request only needed fields)
   └─ Simple CRUD → REST (standard, well-understood)
```

## Quick Start: FastAPI (Python)

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
async def create_item(item: Item):
    return {"id": 1, **item.dict()}
```

## Quick Start: Hono (TypeScript)

```typescript
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const app = new Hono()
app.post('/items', zValidator('json', z.object({
  name: z.string(), price: z.number()
})), (c) => c.json({ id: 1, ...c.req.valid('json') }))
```

## Key Features

- **REST frameworks** with automatic OpenAPI documentation
- **GraphQL** for flexible data fetching (Python: Strawberry, Rust: async-graphql, Go: gqlgen, TypeScript: Pothos)
- **gRPC** for high-performance service-to-service communication
- **tRPC** for end-to-end type safety in TypeScript full-stack
- **Pagination strategies** (cursor-based, offset-based)
- **Rate limiting** and caching
- **API versioning** and OpenAPI docs

## Performance Benchmarks

| Language | Framework | Req/s | Latency | Best For |
|----------|-----------|-------|---------|----------|
| Rust | Axum | ~140k | &lt;1ms | Maximum throughput |
| Go | Gin | ~100k+ | 1-2ms | Mature ecosystem |
| TypeScript | Hono | ~50k | &lt;5ms | Edge deployment |
| Python | FastAPI | ~40k | 5-10ms | Developer experience |

## Pagination Patterns

### Cursor-Based (Recommended)

- Handles real-time changes
- No skipped/duplicate records
- Scales to billions

```python
@app.get("/items")
async def list_items(cursor: Optional[str] = None, limit: int = 20):
    query = db.query(Item).filter(Item.id > cursor) if cursor else db.query(Item)
    items = query.limit(limit).all()
    return {
        "items": items,
        "next_cursor": items[-1].id if items else None,
        "has_more": len(items) == limit
    }
```

## Frontend Integration

- **Forms skill**: Form submission → API validation → Database CRUD
- **Tables skill**: Paginated queries → API → Table display with sorting/filtering
- **AI Chat skill**: SSE streaming for real-time responses
- **Dashboards skill**: Aggregation queries → API → KPI cards

## Related Skills

- [Relational Databases](./databases-relational) - API backends with PostgreSQL/MySQL
- [Auth & Security](./auth-security) - JWT validation, OAuth 2.1
- [Real-time Sync](./realtime-sync) - WebSocket and SSE streaming
- [Observability](./observability) - API metrics and tracing

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/api-patterns)
- FastAPI: https://fastapi.tiangolo.com/
- Hono: https://hono.dev/
- tRPC: https://trpc.io/
