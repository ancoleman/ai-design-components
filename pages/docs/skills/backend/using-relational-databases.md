---
sidebar_position: 2
title: Relational Databases
description: Relational database implementation across Python, Rust, Go, and TypeScript
tags: [backend, database, postgresql, mysql, sqlite, orm]
---

# Relational Databases

Relational database selection and implementation across multiple languages. Choose the optimal database engine, ORM/query builder, and deployment strategy for transactional systems, CRUD applications, and structured data storage.

## When to Use

Use when:
- Building user authentication, content management, e-commerce applications
- Implementing CRUD operations (Create, Read, Update, Delete)
- Designing data models with relationships (users → posts, orders → items)
- Migrating schemas safely in production
- Setting up connection pooling for performance
- Evaluating serverless database options (Neon, PlanetScale, Turso)

Skip for:
- Time-series data at scale → use time-series databases
- Real-time analytics → use columnar databases
- Document-heavy workloads → use document databases

## Multi-Language Support

This skill provides patterns for:
- **Python**: SQLAlchemy 2.0, SQLModel (FastAPI), asyncpg
- **TypeScript**: Prisma (best DX), Drizzle (performance)
- **Rust**: SQLx (compile-time checks), SeaORM, Diesel
- **Go**: sqlc (type-safe codegen), GORM, pgx

## Quick Decision Framework

### Database Selection

```
PRIMARY CONCERN?
├─ MAXIMUM FLEXIBILITY & EXTENSIONS (JSON, arrays, vector search)
│  └─ PostgreSQL
│     ├─ Serverless → Neon (scale-to-zero, database branching)
│     └─ Traditional → Self-hosted, AWS RDS, Google Cloud SQL
│
├─ EMBEDDED / EDGE DEPLOYMENT (local-first, global latency)
│  └─ SQLite or Turso
│     ├─ Global distribution → Turso (libSQL, edge replicas)
│     └─ Local-only → SQLite (embedded, zero-config)
│
└─ RAPID PROTOTYPING
   ├─ Python → SQLModel (FastAPI) or SQLAlchemy 2.0
   ├─ TypeScript → Prisma (best DX) or Drizzle (performance)
   ├─ Rust → SQLx (compile-time checks)
   └─ Go → sqlc (type-safe code generation)
```

### ORM vs Query Builder

```
TEAM PRIORITIES?
├─ DEVELOPMENT SPEED / DEVELOPER EXPERIENCE
│  └─ ORM (abstracts SQL, handles relations automatically)
│     ├─ Python → SQLAlchemy 2.0, SQLModel
│     ├─ TypeScript → Prisma (migrations, type generation)
│     ├─ Rust → SeaORM (Active Record + Data Mapper)
│     └─ Go → GORM, Ent
│
├─ PERFORMANCE / QUERY CONTROL
│  └─ Query Builder (SQL-like, zero abstraction overhead)
│     ├─ Python → SQLAlchemy Core, asyncpg
│     ├─ TypeScript → Drizzle, Kysely
│     ├─ Rust → SQLx (compile-time query validation!)
│     └─ Go → sqlc (generates types from SQL)
```

## Quick Start: Python (SQLModel + FastAPI)

```python
from sqlmodel import SQLModel, Field, Session

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
```

## Quick Start: TypeScript (Prisma)

```typescript
// schema.prisma
model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  posts Post[]
}

// Usage
const user = await prisma.user.create({
  data: { email: 'test@example.com' }
})
```

## Quick Start: Rust (SQLx)

```rust
use sqlx::FromRow;

#[derive(FromRow)]
struct User { id: i32, email: String, name: String }

// Compile-time checked queries (verified at build time!)
let user = sqlx::query_as::&lt;_, User>("SELECT * FROM users WHERE email = $1")
    .bind("test@example.com")
    .fetch_one(&pool)
    .await?;
```

## Key Features

- **PostgreSQL** (primary recommendation): JSON, arrays, vector search, extensions
- **Serverless databases**: Neon (branching), PlanetScale (non-blocking migrations), Turso (edge)
- **ORMs**: SQLAlchemy, Prisma, SeaORM, GORM for developer productivity
- **Query builders**: Drizzle, SQLx, sqlc for performance and control
- **Migrations**: Safe schema evolution with multi-phase deployments
- **Connection pooling**: 10-20 connections for web APIs, 1-2 for serverless

## Connection Pooling

**Recommended pool sizes:**
- Web API (single instance): 10-20 connections
- Serverless (per function): 1-2 connections + pgBouncer
- Background workers: 5-10 connections

## Serverless Databases

| Database | Type | Key Feature | Best For |
|----------|------|-------------|----------|
| **Neon** | PostgreSQL | Database branching, scale-to-zero | Development workflows, preview environments |
| **PlanetScale** | MySQL | Non-blocking schema changes | MySQL apps, zero-downtime migrations |
| **Turso** | SQLite | Edge deployment, low latency | Edge functions, global distribution |

## Frontend Integration

- **Forms skill**: Form submission → API validation → Database CRUD (INSERT/UPDATE)
- **Tables skill**: Paginated queries → API → Table display with sorting/filtering
- **Dashboards skill**: Aggregation queries (COUNT, SUM) → API → KPI cards
- **Search-filter skill**: Full-text search (PostgreSQL tsvector) → Ranked results

## Related Skills

- [API Patterns](./implementing-api-patterns) - Expose database via REST/GraphQL
- [Observability](./implementing-observability) - Monitor query performance
- [Deploying Applications](./deploying-applications) - Database deployment strategies

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/using-relational-databases)
- PostgreSQL: https://www.postgresql.org/
- Neon: https://neon.tech/
- Prisma: https://www.prisma.io/
- SQLAlchemy: https://www.sqlalchemy.org/
