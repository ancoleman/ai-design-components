# Relational Databases - Master Plan

> **Skill Purpose**: Guide selection and implementation of relational databases across Python, TypeScript, Rust, and Go for transactional systems, CRUD applications, and structured data storage.
>
> **Date**: December 2025
> **Status**: Planning Phase
> **Research Sources**: Context7 library research, FULL_STACK_SKILLS_UNIFIED.md

---

## Strategic Positioning

### The Gap This Skill Fills

Current backend development pain points:
```
Developer needs database → Searches docs → Overwhelmed by options → Copy-pastes tutorial → Production issues
```

With this skill:
```
Developer specifies requirements → Skill recommends optimal stack → Production-ready implementation
```

**Problem Statement**: Every application needs a database, but choosing between PostgreSQL, MySQL, SQLite, and their respective ORMs/query builders is time-consuming and error-prone. Developers need:

1. **Database engine selection** - When to use PostgreSQL vs MySQL vs SQLite
2. **ORM/query builder selection** - Trade-offs between ORMs (SQLAlchemy, Prisma, SeaORM) and query builders (Drizzle, sqlc, SQLx)
3. **Migration patterns** - Safe schema evolution in production
4. **Connection pooling** - Performance optimization
5. **Serverless database options** - Scale-to-zero for cost-sensitive applications (Neon, PlanetScale, Turso)

### Unique Value Proposition

| Capability | Why It Matters |
|------------|----------------|
| Multi-language support | Python, TypeScript, Rust, Go patterns in one skill |
| Context7-validated libraries | Trust scores, snippet counts, benchmark scores from production usage |
| Decision framework | Clear decision tree from requirements to implementation |
| Serverless-first guidance | Modern deployment patterns (Neon, PlanetScale, Turso) |
| Production patterns | Connection pooling, migrations, transaction management |

### Frontend Integration Points

| Frontend Skill | Integration Pattern | Example |
|----------------|---------------------|---------|
| **forms** | Form submission → API → Database CRUD | User registration, contact forms |
| **tables** | Database query → API → Table display | User lists, data grids |
| **dashboards** | Aggregation queries → API → KPI cards | Sales metrics, analytics |
| **search-filter** | Full-text search → API → Results | Product search, user lookup |

---

## Component Taxonomy

### Tier 1: Database Engines

#### PostgreSQL (Primary Recommendation)

**When to Use:**
- Maximum flexibility needed
- Advanced features required (JSON, arrays, extensions)
- Vector search needed (pgvector)
- Geospatial data (PostGIS)
- Time-series data (TimescaleDB extension)
- Graph relationships (Apache AGE extension)

**Key Features:**
- ACID compliant
- Rich data types (JSON, JSONB, arrays, hstore)
- Extensible (custom types, operators, functions)
- Advanced indexing (GIN, GiST, BRIN, etc.)
- Mature ecosystem

**Production Deployments:**
- Traditional: Self-hosted, AWS RDS, Google Cloud SQL
- Serverless: **Neon** (database branching, scale-to-zero), Supabase

#### MySQL

**When to Use:**
- Legacy system compatibility required
- Read-heavy workloads
- Simple queries with excellent read performance
- PlanetScale serverless deployment

**Key Features:**
- High read performance
- Replication and clustering mature
- Wide hosting support

**Production Deployments:**
- Traditional: Self-hosted, AWS RDS, Google Cloud SQL
- Serverless: **PlanetScale** (Vitess-based, non-blocking migrations)

#### SQLite

**When to Use:**
- Embedded applications
- Edge deployment
- Local-first applications
- Development/testing environments
- Single-user applications

**Key Features:**
- Zero-configuration
- Single file database
- Excellent for reads
- Extremely reliable (well-tested)

**Production Deployments:**
- Embedded: Mobile apps, desktop apps, CLI tools
- Serverless edge: **Turso** (libSQL, distributed SQLite with microsecond latency)

---

### Tier 2: ORMs and Query Builders by Language

#### Python Stack

| Library | Context7 ID | Trust | Snippets | Type | Best For |
|---------|-------------|-------|----------|------|----------|
| **SQLAlchemy 2.0** | `/websites/sqlalchemy_en_21` | High | 7,090 | ORM + Core | Production applications |
| SQLAlchemy ORM | `/websites/sqlalchemy_en_20_orm` | High | 2,047 | ORM | Advanced ORM features |
| SQLModel | - | - | - | ORM | FastAPI integration, rapid prototyping |
| asyncpg | - | - | - | Driver | High-performance async PostgreSQL |

**SQLAlchemy 2.0 Pattern:**
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)

# Engine with connection pooling
engine = create_engine(
    "postgresql+asyncpg://user:pass@host/db",
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True  # Verify connection before use
)

# Usage
with Session(engine) as session:
    user = User(email="test@example.com", name="Test User")
    session.add(user)
    session.commit()
```

**SQLModel Pattern (FastAPI Integration):**
```python
from sqlmodel import SQLModel, Field, create_engine, Session

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str

engine = create_engine("postgresql://...")

# FastAPI integration
from fastapi import Depends

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/users/")
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
```

#### TypeScript Stack

| Library | Context7 ID | Trust | Snippets | Score | Type | Best For |
|---------|-------------|-------|----------|-------|------|----------|
| **Prisma 6.x** | `/prisma/prisma` | High | 115 | 96.4 | ORM | Best DX, migrations, type safety |
| Prisma Docs | `/prisma/docs` | High | 4,281 | - | Docs | Comprehensive documentation |
| **Drizzle ORM** | `/llmstxt/orm_drizzle_team-llms.txt` | High | 4,037 | 95.4 | Query Builder | Performance, SQL-like syntax |
| Drizzle Docs | `/drizzle-team/drizzle-orm-docs` | High | 1,666 | - | Docs | Documentation |
| Kysely | - | - | - | Query Builder | Type-safe SQL builder |

**Prisma Pattern:**
```typescript
// schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  name  String
  posts Post[]
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  authorId  Int
  author    User     @relation(fields: [authorId], references: [id])
}

// TypeScript usage
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function main() {
  const user = await prisma.user.create({
    data: {
      email: "test@example.com",
      name: "Test User",
      posts: {
        create: {
          title: "First Post",
          content: "Hello World"
        }
      }
    },
    include: { posts: true }
  })

  console.log(user)
}
```

**Drizzle ORM Pattern:**
```typescript
// schema.ts
import { pgTable, serial, text, integer, boolean } from 'drizzle-orm/pg-core'

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: text('email').notNull().unique(),
  name: text('name').notNull(),
})

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: text('title').notNull(),
  content: text('content'),
  published: boolean('published').default(false),
  authorId: integer('author_id').references(() => users.id),
})

// TypeScript usage
import { drizzle } from 'drizzle-orm/node-postgres'
import { eq } from 'drizzle-orm'
import { Pool } from 'pg'

const pool = new Pool({ connectionString: process.env.DATABASE_URL })
const db = drizzle(pool)

// Type-safe queries
const allUsers = await db.select().from(users)
const user = await db.select().from(users).where(eq(users.id, 1))

// Joins
const usersWithPosts = await db
  .select()
  .from(users)
  .leftJoin(posts, eq(users.id, posts.authorId))
```

#### Rust Stack

| Library | Use Case | Key Features |
|---------|----------|--------------|
| **SQLx 0.8** | Compile-time query validation | Async, type-safe, no ORM overhead |
| **SeaORM 1.x** | Full ORM experience | Active Record + Data Mapper patterns |
| **Diesel 2.3** | Mature, stable ORM | Compile-time guarantees, migrations |

**SQLx Pattern (Recommended for Rust):**
```rust
use sqlx::postgres::PgPoolOptions;
use sqlx::FromRow;

#[derive(FromRow)]
struct User {
    id: i32,
    email: String,
    name: String,
}

#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
    // Connection pool
    let pool = PgPoolOptions::new()
        .max_connections(20)
        .connect("postgresql://user:pass@localhost/db")
        .await?;

    // Compile-time checked query (verified at build time!)
    let user = sqlx::query_as::<_, User>(
        "SELECT id, email, name FROM users WHERE email = $1"
    )
    .bind("test@example.com")
    .fetch_one(&pool)
    .await?;

    println!("User: {} ({})", user.name, user.email);

    // Insert with macro (also compile-time checked)
    sqlx::query!(
        "INSERT INTO users (email, name) VALUES ($1, $2)",
        "new@example.com",
        "New User"
    )
    .execute(&pool)
    .await?;

    Ok(())
}
```

**SeaORM Pattern:**
```rust
use sea_orm::*;

#[derive(Clone, Debug, PartialEq, DeriveEntityModel)]
#[sea_orm(table_name = "users")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i32,
    pub email: String,
    pub name: String,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {
    #[sea_orm(has_many = "super::post::Entity")]
    Post,
}

impl ActiveModelBehavior for ActiveModel {}

// Usage
#[tokio::main]
async fn main() -> Result<(), DbErr> {
    let db = Database::connect("postgresql://...").await?;

    // Insert
    let user = users::ActiveModel {
        email: Set("test@example.com".to_owned()),
        name: Set("Test User".to_owned()),
        ..Default::default()
    };
    let insert_result = user.insert(&db).await?;

    // Query
    let users = Users::find()
        .filter(users::Column::Email.contains("@example.com"))
        .all(&db)
        .await?;

    Ok(())
}
```

#### Go Stack

| Library | Use Case | Key Features |
|---------|----------|--------------|
| **GORM v2** | Full ORM | Associations, hooks, auto-migrations |
| **sqlc** | Type-safe code generation | Generates Go from SQL queries |
| **Ent** | Graph-based ORM | Schema as code, powerful queries |
| **pgx** | PostgreSQL driver | High performance, low-level control |

**sqlc Pattern (Recommended for Go):**
```sql
-- queries.sql
-- name: GetUser :one
SELECT id, email, name FROM users WHERE id = $1;

-- name: CreateUser :one
INSERT INTO users (email, name) VALUES ($1, $2) RETURNING *;

-- name: ListUsers :many
SELECT id, email, name FROM users ORDER BY id;
```

```yaml
# sqlc.yaml
version: "2"
sql:
  - engine: "postgresql"
    queries: "queries.sql"
    schema: "schema.sql"
    gen:
      go:
        package: "db"
        out: "db"
```

```go
// Generated code provides type-safe functions
package main

import (
    "context"
    "database/sql"
    "yourproject/db"
    _ "github.com/lib/pq"
)

func main() {
    conn, _ := sql.Open("postgres", "postgresql://...")
    queries := db.New(conn)

    ctx := context.Background()

    // Type-safe, compile-time checked
    user, err := queries.CreateUser(ctx, db.CreateUserParams{
        Email: "test@example.com",
        Name:  "Test User",
    })

    users, err := queries.ListUsers(ctx)
}
```

**GORM Pattern:**
```go
package main

import (
    "gorm.io/gorm"
    "gorm.io/driver/postgres"
)

type User struct {
    ID    uint   `gorm:"primaryKey"`
    Email string `gorm:"uniqueIndex;not null"`
    Name  string `gorm:"not null"`
    Posts []Post
}

type Post struct {
    ID       uint   `gorm:"primaryKey"`
    Title    string
    Content  string
    UserID   uint
}

func main() {
    db, _ := gorm.Open(postgres.Open("postgresql://..."), &gorm.Config{})

    // Auto-migrate (creates tables)
    db.AutoMigrate(&User{}, &Post{})

    // Create
    user := User{Email: "test@example.com", Name: "Test User"}
    db.Create(&user)

    // Query with associations
    var userWithPosts User
    db.Preload("Posts").First(&userWithPosts, user.ID)
}
```

---

### Tier 3: Advanced Patterns

#### Connection Pooling

**Why It Matters:**
Database connections are expensive to create (100-500ms). Connection pooling reuses connections, reducing latency from 100ms to <1ms.

**Recommended Pool Sizes:**

| Deployment Type | Pool Size | Reasoning |
|----------------|-----------|-----------|
| **Web API (single instance)** | 10-20 | Formula: (CPU cores × 2) + effective_spindle_count |
| **Serverless (per function)** | 1-2 | Minimize idle connections, use pgBouncer |
| **Background workers** | 5-10 | Depends on concurrency needs |
| **High-traffic API** | 20-50 | Monitor with pgBouncer/PgPool II |

**Python (SQLAlchemy):**
```python
engine = create_engine(
    "postgresql+asyncpg://...",
    pool_size=20,           # Normal connections
    max_overflow=10,        # Extra connections under load
    pool_timeout=30,        # Wait 30s for connection
    pool_recycle=3600,      # Recycle connections after 1 hour
    pool_pre_ping=True      # Verify connection before use
)
```

**TypeScript (Prisma):**
```typescript
// Prisma automatically manages connection pooling
// Configure in DATABASE_URL:
// postgresql://user:pass@host/db?connection_limit=20&pool_timeout=30
```

**Rust (SQLx):**
```rust
let pool = PgPoolOptions::new()
    .max_connections(20)
    .min_connections(5)
    .acquire_timeout(Duration::from_secs(30))
    .idle_timeout(Duration::from_secs(600))
    .max_lifetime(Duration::from_secs(3600))
    .connect("postgresql://...")
    .await?;
```

#### Migration Patterns

**Schema Evolution Strategies:**

| Strategy | Use Case | Example Tools |
|----------|----------|---------------|
| **Version-based** | Sequential migrations | Alembic (Python), Prisma Migrate, Diesel |
| **State-based** | Declarative schema | Atlas, Flyway |
| **Reversible** | Rollback support | SQLAlchemy-Migrate, golang-migrate |

**Safe Migration Practices:**

1. **Never drop columns in production without multi-phase deployment:**
   ```sql
   -- Phase 1: Add new column (safe)
   ALTER TABLE users ADD COLUMN new_email VARCHAR(255);

   -- Phase 2: Backfill data (deploy code that writes to both)
   UPDATE users SET new_email = email WHERE new_email IS NULL;

   -- Phase 3: Make NOT NULL (after verification)
   ALTER TABLE users ALTER COLUMN new_email SET NOT NULL;

   -- Phase 4: Drop old column (after code no longer reads it)
   ALTER TABLE users DROP COLUMN email;
   ```

2. **Use concurrent index creation (PostgreSQL):**
   ```sql
   -- Blocks writes (BAD)
   CREATE INDEX idx_users_email ON users(email);

   -- Does not block writes (GOOD)
   CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
   ```

3. **Test migrations in staging with production-like data volume**

**Python (Alembic with SQLAlchemy):**
```python
# alembic/versions/001_add_users.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('ix_users_email', 'users')
    op.drop_table('users')
```

**TypeScript (Prisma Migrate):**
```bash
# Create migration
npx prisma migrate dev --name add_users

# Apply migration to production
npx prisma migrate deploy
```

**Rust (SQLx Migrations):**
```bash
# Create migration
sqlx migrate add add_users

# Run migrations
sqlx migrate run
```

```rust
// Embed migrations in binary
sqlx::migrate!("./migrations")
    .run(&pool)
    .await?;
```

**Go (golang-migrate):**
```bash
migrate create -ext sql -dir migrations -seq add_users
```

```sql
-- migrations/000001_add_users.up.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL
);

-- migrations/000001_add_users.down.sql
DROP TABLE users;
```

#### Serverless Databases

**Modern Deployment Pattern:**
Traditional databases charge 24/7 even when idle. Serverless databases scale to zero when not in use.

| Database | Type | Key Feature | Best For |
|----------|------|-------------|----------|
| **Neon** | PostgreSQL | Database branching (like Git), scale-to-zero | Development workflows, preview environments |
| **PlanetScale** | MySQL (Vitess) | Non-blocking schema changes | MySQL apps, zero-downtime migrations |
| **Turso** | SQLite (libSQL) | Edge deployment, microsecond latency | Edge functions, global distribution |

**Neon Example (PostgreSQL):**
```typescript
import { neon } from '@neondatabase/serverless'

// Connects via HTTP (works in Cloudflare Workers, Vercel Edge)
const sql = neon(process.env.DATABASE_URL!)

const users = await sql`
  SELECT id, email, name FROM users WHERE email = ${email}
`
```

**Features:**
- **Branching**: Create database branch per PR/feature
- **Scale to zero**: Pauses after inactivity, resumes in <1s
- **Pricing**: Pay only for active time + storage

**PlanetScale Example (MySQL):**
```typescript
import { connect } from '@planetscale/database'

const conn = connect({
  host: process.env.DATABASE_HOST,
  username: process.env.DATABASE_USERNAME,
  password: process.env.DATABASE_PASSWORD
})

const results = await conn.execute(
  'SELECT * FROM users WHERE email = ?',
  [email]
)
```

**Features:**
- **Non-blocking migrations**: Deploy schema changes without locking tables
- **Branching**: Safe schema testing in branches
- **Insights**: Query performance analytics

**Turso Example (SQLite at the edge):**
```typescript
import { createClient } from '@libsql/client'

const client = createClient({
  url: process.env.TURSO_DATABASE_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN
})

const result = await client.execute({
  sql: 'SELECT * FROM users WHERE email = ?',
  args: [email]
})
```

**Features:**
- **Edge deployment**: Database replicas near users
- **Embedded replicas**: Local-first with sync
- **Pricing**: Pay per row read/write

---

## Decision Framework

### Database Selection Tree

```
┌─────────────────────────────────────────────────────────────┐
│                 Database Selection Tree                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PRIMARY CONCERN?                                            │
│  ├── MAXIMUM FLEXIBILITY & EXTENSIONS                        │
│  │   └─ PostgreSQL (pgvector, PostGIS, TimescaleDB)         │
│  │       ├─ Serverless → Neon (scale-to-zero)               │
│  │       └─ Traditional → Self-hosted, AWS RDS, Cloud SQL   │
│  │                                                          │
│  ├── EMBEDDED / EDGE DEPLOYMENT                             │
│  │   └─ SQLite or Turso (libSQL)                            │
│  │       ├─ Global distribution → Turso                     │
│  │       └─ Local-only → SQLite                             │
│  │                                                          │
│  ├── LEGACY SYSTEM / MYSQL REQUIRED                         │
│  │   └─ MySQL                                                │
│  │       ├─ Serverless → PlanetScale (non-blocking mig)    │
│  │       └─ Traditional → Self-hosted, AWS RDS, Cloud SQL   │
│  │                                                          │
│  ├── RAPID PROTOTYPING                                       │
│  │   ├─ TypeScript → Prisma (best DX) or Drizzle (perf)    │
│  │   ├─ Python → SQLModel (FastAPI) or SQLAlchemy          │
│  │   ├─ Go → sqlc (type-safe from SQL)                     │
│  │   └─ Rust → SQLx (compile-time checks)                  │
│  │                                                          │
│  └── MAXIMUM PERFORMANCE                                     │
│      ├─ Rust → SQLx (compile-time verification)             │
│      ├─ Go → sqlc (generated type-safe code)                │
│      └─ TypeScript → Drizzle ORM (zero-overhead)            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### ORM vs Query Builder Selection

```
┌─────────────────────────────────────────────────────────────┐
│              ORM vs Query Builder Selection                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  TEAM PRIORITIES?                                            │
│  ├── DEVELOPMENT SPEED / DEVELOPER EXPERIENCE                │
│  │   └─ ORM                                                  │
│  │       ├─ Python → SQLAlchemy 2.0, SQLModel               │
│  │       ├─ TypeScript → Prisma (best DX)                   │
│  │       ├─ Rust → SeaORM                                    │
│  │       └─ Go → GORM, Ent                                   │
│  │                                                          │
│  ├── PERFORMANCE / QUERY CONTROL                             │
│  │   └─ Query Builder                                        │
│  │       ├─ Python → SQLAlchemy Core, asyncpg               │
│  │       ├─ TypeScript → Drizzle, Kysely                    │
│  │       ├─ Rust → SQLx (compile-time checked!)             │
│  │       └─ Go → sqlc (generates code from SQL)             │
│  │                                                          │
│  ├── TYPE SAFETY / COMPILE-TIME GUARANTEES                  │
│  │   ├─ Rust → SQLx (queries checked at build time)        │
│  │   ├─ Go → sqlc (generates types from SQL)               │
│  │   ├─ TypeScript → Prisma or Drizzle                     │
│  │   └─ Python → SQLModel (Pydantic integration)           │
│  │                                                          │
│  └── COMPLEX QUERIES / JOINS                                 │
│      ├─ SQL-first → Query builders or raw SQL               │
│      └─ ORM-friendly → SeaORM, SQLAlchemy ORM               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Multi-Language Support Tables

### Python: Database Library Comparison

| Library | Type | Async | Type Safety | Learning Curve | Best For |
|---------|------|-------|-------------|----------------|----------|
| **SQLAlchemy 2.0** | ORM + Core | ✅ | Pydantic v2 | Medium | Production apps |
| **SQLModel** | ORM | ✅ | Pydantic v2 | Low | FastAPI, rapid prototyping |
| **Tortoise ORM** | ORM | ✅ | Pydantic | Low | Async-first apps |
| **asyncpg** | Driver | ✅ | Manual | High | Maximum performance |
| **psycopg3** | Driver | ✅ | Manual | Medium | PostgreSQL-specific |

### TypeScript: Database Library Comparison

| Library | Type | Bundle Size | Type Safety | DX Score | Best For |
|---------|------|-------------|-------------|----------|----------|
| **Prisma** | ORM | Large (client gen) | Excellent | 96.4 | Best DX, migrations |
| **Drizzle** | Query Builder | ~14KB | Excellent | 95.4 | Performance, SQL-like |
| **Kysely** | Query Builder | ~10KB | Excellent | - | Type-safe SQL |
| **TypeORM** | ORM | Medium | Good | - | Legacy projects |
| **MikroORM** | ORM | Medium | Excellent | - | Unit of Work pattern |

### Rust: Database Library Comparison

| Library | Type | Compile-Time | Runtime | Learning Curve | Best For |
|---------|------|--------------|---------|----------------|----------|
| **SQLx** | Query Builder | ✅ Queries | Async (Tokio) | Medium | Type safety, performance |
| **SeaORM** | ORM | ✅ Schema | Async (Tokio) | Medium | ORM features |
| **Diesel** | ORM | ✅ Schema | Sync/Async | High | Mature, stable |
| **tokio-postgres** | Driver | ❌ | Async (Tokio) | Low | Low-level control |

### Go: Database Library Comparison

| Library | Type | Code Gen | Type Safety | Learning Curve | Best For |
|---------|------|----------|-------------|----------------|----------|
| **sqlc** | Query Builder | ✅ From SQL | Excellent | Low | Type-safe, SQL-first |
| **GORM** | ORM | ❌ | Good (tags) | Low | Rapid development |
| **Ent** | ORM | ✅ From schema | Excellent | Medium | Graph queries |
| **pgx** | Driver | ❌ | Manual | Low | PostgreSQL performance |

---

## Frontend Integration Mapping

### Forms Skill Integration

**Scenario:** User registration form

```
Frontend (forms skill):
├── React Hook Form validates input
├── POST /api/users
└── Sends { email, password, name }

Backend (databases-relational skill):
├── Receives request (FastAPI/Axum/Express)
├── Validates with Pydantic/Zod
├── Hashes password (Argon2)
├── INSERT INTO users (email, password_hash, name)
└── Returns { id, email, name }

Database:
└── PostgreSQL enforces UNIQUE constraint on email
```

**Implementation Example (Python + FastAPI + SQLModel):**
```python
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class UserCreate(SQLModel):
    email: str
    password: str
    name: str

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    name: str

app = FastAPI()
engine = create_engine("postgresql://...")

@app.post("/api/users", response_model=User)
def create_user(user: UserCreate):
    with Session(engine) as session:
        # Check if email exists
        existing = session.query(User).filter(User.email == user.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash password
        hashed = pwd_context.hash(user.password)

        # Create user
        db_user = User(
            email=user.email,
            password_hash=hashed,
            name=user.name
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
```

### Tables Skill Integration

**Scenario:** Paginated user list with sorting

```
Frontend (tables skill):
├── TanStack Table requests page 2, sort by email
├── GET /api/users?page=2&pageSize=20&sortBy=email&sortOrder=asc
└── Receives { data: [...], total: 1500, page: 2, pageSize: 20 }

Backend (databases-relational skill):
├── Parse query parameters
├── SELECT * FROM users ORDER BY email ASC LIMIT 20 OFFSET 20
└── Returns paginated results + metadata

Database:
└── Uses index on email for fast sorting
```

**Implementation Example (TypeScript + Drizzle):**
```typescript
import { drizzle } from 'drizzle-orm/node-postgres'
import { asc, desc, count } from 'drizzle-orm'
import { users } from './schema'

app.get('/api/users', async (req, res) => {
  const page = parseInt(req.query.page as string) || 1
  const pageSize = parseInt(req.query.pageSize as string) || 20
  const sortBy = (req.query.sortBy as string) || 'id'
  const sortOrder = (req.query.sortOrder as string) || 'asc'

  const offset = (page - 1) * pageSize
  const sortFn = sortOrder === 'asc' ? asc : desc

  // Get total count
  const [{ total }] = await db.select({ total: count() }).from(users)

  // Get paginated data
  const data = await db
    .select()
    .from(users)
    .orderBy(sortFn(users[sortBy]))
    .limit(pageSize)
    .offset(offset)

  res.json({ data, total, page, pageSize })
})
```

### Dashboards Skill Integration

**Scenario:** KPI cards with aggregated metrics

```
Frontend (dashboards skill):
├── Displays KPI cards (total users, active users, revenue)
├── GET /api/dashboard/kpis
└── Receives { totalUsers: 1500, activeUsers: 1200, revenue: 45000 }

Backend (databases-relational skill):
├── Runs aggregation queries
├── SELECT COUNT(*) FROM users
├── SELECT COUNT(*) FROM users WHERE last_active > NOW() - INTERVAL '30 days'
└── Returns aggregated metrics

Database:
└── PostgreSQL optimizes COUNT(*) with table statistics
```

**Implementation Example (Rust + SQLx):**
```rust
use axum::{Json, extract::State};
use sqlx::PgPool;
use serde::Serialize;

#[derive(Serialize)]
struct DashboardKpis {
    total_users: i64,
    active_users: i64,
    revenue: f64,
}

async fn get_dashboard_kpis(
    State(pool): State<PgPool>
) -> Json<DashboardKpis> {
    let total_users = sqlx::query_scalar!(
        "SELECT COUNT(*) FROM users"
    )
    .fetch_one(&pool)
    .await
    .unwrap_or(0);

    let active_users = sqlx::query_scalar!(
        "SELECT COUNT(*) FROM users WHERE last_active > NOW() - INTERVAL '30 days'"
    )
    .fetch_one(&pool)
    .await
    .unwrap_or(0);

    let revenue = sqlx::query_scalar!(
        "SELECT COALESCE(SUM(amount), 0) FROM orders WHERE status = 'completed'"
    )
    .fetch_one(&pool)
    .await
    .unwrap_or(0.0);

    Json(DashboardKpis {
        total_users,
        active_users,
        revenue,
    })
}
```

### Search/Filter Skill Integration

**Scenario:** Full-text search across products

```
Frontend (search-filter skill):
├── User types "wireless headphones"
├── GET /api/products/search?q=wireless+headphones
└── Receives ranked results

Backend (databases-relational skill):
├── Uses PostgreSQL full-text search (tsvector, tsquery)
├── SELECT * FROM products WHERE search_vector @@ to_tsquery('wireless & headphones')
├── Ranks by ts_rank
└── Returns results

Database:
└── Uses GIN index on tsvector for fast full-text search
```

**Implementation Example (Python + SQLAlchemy + PostgreSQL):**
```python
from sqlalchemy import Column, Integer, String, Index, func
from sqlalchemy.dialects.postgresql import TSVECTOR

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    search_vector = Column(TSVECTOR)  # Auto-updated via trigger

    __table_args__ = (
        Index('ix_products_search', 'search_vector', postgresql_using='gin'),
    )

@app.get("/api/products/search")
def search_products(q: str, session: Session = Depends(get_session)):
    search_query = func.to_tsquery('english', q)

    results = session.query(Product).filter(
        Product.search_vector.op('@@')(search_query)
    ).order_by(
        func.ts_rank(Product.search_vector, search_query).desc()
    ).limit(20).all()

    return results
```

---

## Skill Structure

```
databases-relational/
├── init.md                       # This file - master plan
├── SKILL.md                      # Main skill file (< 500 lines)
├── references/
│   ├── postgresql-guide.md       # PostgreSQL features, extensions
│   ├── mysql-guide.md            # MySQL-specific patterns
│   ├── sqlite-guide.md           # SQLite and Turso patterns
│   ├── orms-python.md            # SQLAlchemy, SQLModel, asyncpg
│   ├── orms-typescript.md        # Prisma, Drizzle, Kysely
│   ├── orms-rust.md              # SQLx, SeaORM, Diesel
│   ├── orms-go.md                # GORM, sqlc, Ent, pgx
│   ├── migrations-guide.md       # Migration best practices
│   ├── connection-pooling.md     # Pool configuration guide
│   ├── serverless-databases.md   # Neon, PlanetScale, Turso
│   └── performance-tuning.md     # Indexing, query optimization
├── examples/
│   ├── python-sqlalchemy/
│   │   ├── basic-crud.py
│   │   ├── async-example.py
│   │   ├── migrations/
│   │   └── README.md
│   ├── typescript-prisma/
│   │   ├── schema.prisma
│   │   ├── crud-operations.ts
│   │   ├── migrations/
│   │   └── README.md
│   ├── typescript-drizzle/
│   │   ├── schema.ts
│   │   ├── queries.ts
│   │   └── README.md
│   ├── rust-sqlx/
│   │   ├── src/main.rs
│   │   ├── migrations/
│   │   └── README.md
│   └── go-sqlc/
│       ├── queries.sql
│       ├── sqlc.yaml
│       └── README.md
└── scripts/
    ├── generate_migration.py     # Create migration templates
    ├── validate_schema.py        # Schema validation
    ├── benchmark_queries.py      # Query performance testing
    └── setup_connection_pool.py  # Connection pool calculator
```

---

## SKILL.md Frontmatter Template

```yaml
---
name: databases-relational
description: Relational database implementation across Python, Rust, Go, and TypeScript. Use when building CRUD applications, transactional systems, or structured data storage. Covers PostgreSQL (primary), MySQL, SQLite, ORMs (SQLAlchemy, Prisma, SeaORM, GORM), query builders (Drizzle, sqlc, SQLx), migrations, connection pooling, and serverless databases (Neon, PlanetScale, Turso).
---
```

---

## Quality Checklist

### Before Considering This Skill Complete:

**Core Quality:**
- [ ] Description includes both WHAT and WHEN
- [ ] SKILL.md body under 500 lines
- [ ] No time-sensitive information (library versions OK in references/)
- [ ] Consistent terminology throughout (ORM vs query builder clearly defined)
- [ ] Examples are concrete, runnable code
- [ ] File references are one level deep from SKILL.md

**Naming and Structure:**
- [ ] Name uses appropriate form: `databases-relational` (noun form acceptable for infrastructure)
- [ ] Name: lowercase, hyphens only, max 64 chars
- [ ] Description: max 1024 chars, non-empty
- [ ] File paths use forward slashes (not backslashes)

**Multi-Language Coverage:**
- [ ] Python examples (SQLAlchemy, SQLModel)
- [ ] TypeScript examples (Prisma, Drizzle)
- [ ] Rust examples (SQLx, SeaORM)
- [ ] Go examples (sqlc, GORM)
- [ ] All examples include connection pooling
- [ ] All examples include error handling

**Code and Scripts:**
- [ ] Scripts solve problems rather than punt to Claude
- [ ] Migration scripts include rollback examples
- [ ] Schema validation script works across languages
- [ ] Connection pool calculator provides concrete recommendations
- [ ] No "magic numbers" - all values justified in comments
- [ ] Required packages listed and verified

**Testing:**
- [ ] At least 3 evaluations per language ecosystem
- [ ] Tested with Haiku, Sonnet, Opus
- [ ] Tested with real usage scenarios (CRUD, migrations, pooling)
- [ ] Performance and token usage acceptable

**Context7 Integration:**
- [ ] All Context7 IDs validated and current
- [ ] Trust scores documented
- [ ] Snippet counts included
- [ ] Benchmark scores noted where available

**Frontend Integration:**
- [ ] forms skill integration documented
- [ ] tables skill integration documented
- [ ] dashboards skill integration documented
- [ ] search-filter skill integration documented
- [ ] Working examples for each integration

**Production Readiness:**
- [ ] Migration safety patterns documented
- [ ] Connection pooling best practices clear
- [ ] Serverless deployment options covered
- [ ] Performance tuning guidance included
- [ ] Security best practices (parameterized queries, password hashing)

---

## Research Methodology

### Context7 Library Validation

All libraries in this skill were validated using Context7 data from FULL_STACK_SKILLS_UNIFIED.md:

**Python Libraries:**
- SQLAlchemy 2.0: `/websites/sqlalchemy_en_21` (High trust, 7,090 snippets)
- SQLAlchemy ORM: `/websites/sqlalchemy_en_20_orm` (High trust, 2,047 snippets)

**TypeScript Libraries:**
- Prisma 6.x: `/prisma/prisma` (High trust, 115 snippets, 96.4 score)
- Prisma Docs: `/prisma/docs` (High trust, 4,281 snippets)
- Drizzle ORM: `/llmstxt/orm_drizzle_team-llms.txt` (High trust, 4,037 snippets, 95.4 score)
- Drizzle Docs: `/drizzle-team/drizzle-orm-docs` (High trust, 1,666 snippets)

**Validation Process:**
1. Cross-reference Context7 trust scores
2. Verify snippet counts indicate active documentation
3. Check benchmark scores for quality indicators
4. Validate against current production usage (November 2025)

---

## Success Metrics

This skill is successful when:

1. **Database Selection**: Developer can choose optimal database in < 5 minutes using decision tree
2. **ORM Selection**: Developer can choose optimal ORM/query builder for language + use case
3. **Connection Pooling**: Developer implements correct pool sizes without trial-and-error
4. **Migration Safety**: Zero production incidents from migrations following skill guidance
5. **Serverless Adoption**: Developer can evaluate serverless database options confidently
6. **Multi-Language Parity**: Same quality guidance across Python, TypeScript, Rust, Go
7. **Frontend Integration**: Seamless connection to forms, tables, dashboards, search-filter skills

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2025-12-02 | Initial master plan created with Context7 research |

---

**Document Status**: Planning Phase - Ready for SKILL.md implementation
**Next Steps**: Create SKILL.md (< 500 lines) with progressive disclosure to references/
**Research Completeness**: ✅ Context7 validated, ✅ Multi-language coverage, ✅ Decision frameworks, ✅ Frontend integration
