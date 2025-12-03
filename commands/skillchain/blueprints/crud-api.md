# CRUD API Blueprint

## Overview

Pre-configured skill chain for building production-ready RESTful CRUD APIs with database persistence, authentication, and optional observability/deployment.

**Use this blueprint when building:**
- RESTful APIs with database CRUD operations
- Backend services with authentication
- APIs with PostgreSQL/MySQL/SQLite
- FastAPI or Hono-based backends

## Trigger Keywords

**Primary:**
- crud
- rest api
- backend api
- api with database
- crud backend

**Secondary:**
- fastapi
- database api
- postgresql api
- mysql api
- backend with auth
- rest crud

**Detection Logic:**
Must contain at least one primary keyword OR (api/backend + database).

---

## Pre-configured Skill Chain

The blueprint automatically selects these skills in order:

### Core Skills (Always Included)

1. **api-patterns** (Priority: 5)
   - Plugin: `backend-api-skills:api-patterns`
   - Purpose: REST API framework and endpoint patterns
   - Pre-configured defaults (see below)

2. **databases-relational** (Priority: 10)
   - Plugin: `backend-data-skills:databases-relational`
   - Purpose: PostgreSQL/MySQL/SQLite with ORM
   - Pre-configured defaults (see below)

3. **auth-security** (Priority: 8)
   - Plugin: `backend-platform-skills:auth-security`
   - Purpose: JWT authentication and RBAC
   - Pre-configured defaults (see below)

### Optional Skills (Offered to User)

4. **observability** (Priority: 20, Optional)
   - Plugin: `backend-platform-skills:observability`
   - Purpose: OpenTelemetry, metrics, logging
   - Only included if user confirms monitoring needs

5. **deploying-applications** (Priority: 25, Optional)
   - Plugin: `backend-platform-skills:deploying-applications`
   - Purpose: Docker, Kubernetes, deployment configs
   - Only included if user confirms deployment needs

---

## Pre-configured Defaults

### api-patterns

```yaml
api_style: "REST"
framework:
  python: "FastAPI"
  typescript: "Hono"
features:
  - openapi_docs: true
  - cors: true
  - rate_limiting: true
  - request_validation: true
  - error_handling: true
crud_operations:
  - create: "POST /{resource}"
  - read: "GET /{resource}/{id}"
  - update: "PUT /{resource}/{id}"
  - delete: "DELETE /{resource}/{id}"
  - list: "GET /{resource}?page={n}&limit={m}"
versioning: "url"  # /v1/users
pagination: "offset-based"
response_format: "JSON"
```

### databases-relational

```yaml
database:
  python: "PostgreSQL"
  typescript: "PostgreSQL"
orm:
  python: "SQLAlchemy 2.0"
  typescript: "Drizzle ORM"
migrations:
  python: "Alembic"
  typescript: "drizzle-kit"
features:
  - connection_pooling: true
  - async_support: true
  - type_safety: true
  - migration_versioning: true
schema_patterns:
  - timestamps: true  # created_at, updated_at
  - soft_delete: true  # deleted_at
  - audit_fields: false  # created_by, updated_by (enabled if auth included)
indexes:
  - primary_keys: true
  - foreign_keys: true
  - unique_constraints: true
```

### auth-security

```yaml
method: "JWT"
token_storage: "HTTP-only cookies"
session_backend: "database"
features:
  - access_tokens: true
  - refresh_tokens: true
  - password_hashing: "bcrypt"
  - rbac: true
  - api_key_support: false
token_expiry:
  access: "15m"
  refresh: "7d"
protected_routes: "automatic"  # Middleware applied to all CRUD endpoints
public_routes: ["/auth/login", "/auth/register", "/health"]
```

### observability (Optional)

```yaml
enabled: false  # User must confirm
tracing:
  provider: "OpenTelemetry"
  export: "Console + OTLP"
metrics:
  - http_requests: true
  - database_queries: true
  - error_rates: true
logging:
  format: "structured JSON"
  level: "INFO"
```

### deploying-applications (Optional)

```yaml
enabled: false  # User must confirm
targets: ["docker"]  # Minimal by default
docker:
  multi_stage: true
  base_image:
    python: "python:3.11-slim"
    typescript: "node:20-alpine"
healthcheck: true
```

---

## Quick Questions (Only 4)

Blueprint reduces the typical 20+ questions to just 4 high-level choices:

### Question 1: Language Preference
```
Which language for your CRUD API?

[1] Python (FastAPI + SQLAlchemy + Alembic)
[2] TypeScript (Hono + Drizzle ORM)

Choice (1/2): _
```

**Impact:**
- Sets framework: FastAPI vs Hono
- Sets ORM: SQLAlchemy vs Drizzle
- Sets migration tool: Alembic vs drizzle-kit
- Auto-configures async patterns

**Default:** Python (FastAPI)

---

### Question 2: Resources/Entities
```
What resources/entities will your API manage?

Examples:
  - E-commerce: users, products, orders, reviews
  - Blog: users, posts, comments, tags
  - Task Manager: users, projects, tasks, labels

Enter comma-separated list: _
```

**Impact:**
- Generates database models for each resource
- Creates CRUD endpoints for each resource
- Sets up foreign key relationships if detected (e.g., "orders" references "users")
- Creates migration files
- Generates API route files

**Default:** users, items

**Smart Detection:**
- Detects common relationships (users → posts, orders → products)
- Adds audit fields (created_by) if users entity present
- Creates junction tables for many-to-many (posts ↔ tags)

---

### Question 3: Authentication
```
Include authentication?

[1] Yes - Full auth system (login, register, JWT, RBAC)
[2] No - Public API (no authentication)
[3] API Keys only - Simple token-based auth

Choice (1/2/3): _
```

**Impact:**

**If [1] Yes (Full auth):**
- Includes `auth-security` skill
- Creates User model with password hashing
- Generates /auth/login, /auth/register endpoints
- Protects all CRUD endpoints with JWT middleware
- Adds role-based permissions
- Adds audit fields (created_by, updated_by) to all models

**If [2] No:**
- Skips `auth-security` skill
- All endpoints public
- No User model (unless explicitly listed in Q2)
- No audit fields

**If [3] API Keys:**
- Minimal auth (no full skill invocation)
- Simple API key validation middleware
- API key stored in environment
- No user management

**Default:** [1] Yes

---

### Question 4: Advanced Features
```
Enable advanced features? (Select all that apply)

[ ] Monitoring - OpenTelemetry tracing, metrics, logs
[ ] Deployment - Docker + Kubernetes configs
[ ] None - Keep it simple

Selection (m/d/none): _
```

**Input:**
- `m` = Monitoring (includes observability skill)
- `d` = Deployment (includes deploying-applications skill)
- `m,d` = Both
- `none` or blank = Neither

**Impact:**

**If Monitoring:**
- Includes `observability` skill
- Adds OpenTelemetry instrumentation
- Creates prometheus metrics endpoint
- Structured JSON logging
- Trace all HTTP requests and DB queries

**If Deployment:**
- Includes `deploying-applications` skill
- Generates Dockerfile (multi-stage)
- Creates docker-compose.yml (API + DB + optional Redis)
- Kubernetes manifests (deployment, service, ingress)
- Health check endpoints

**Default:** none

---

## Generated Output Structure

### Python (FastAPI) Structure

```
crud-api/
├── src/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app entry point
│   ├── config.py                   # Settings (pydantic-settings)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                 # Dependencies (get_db, get_current_user)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py           # Main API router
│   │       ├── users.py            # User CRUD endpoints
│   │       ├── items.py            # Item CRUD endpoints
│   │       └── auth.py             # Auth endpoints (if enabled)
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py                 # SQLAlchemy Base
│   │   ├── session.py              # Database session
│   │   └── models/
│   │       ├── __init__.py
│   │       ├── user.py             # User model
│   │       └── item.py             # Item model
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py                 # Pydantic schemas
│   │   └── item.py                 # Pydantic schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user.py                 # User business logic
│   │   └── item.py                 # Item business logic
│   │
│   └── auth/                       # If auth enabled
│       ├── __init__.py
│       ├── security.py             # Password hashing, JWT
│       ├── deps.py                 # get_current_user dependency
│       └── permissions.py          # RBAC logic
│
├── alembic/
│   ├── versions/
│   │   └── 001_initial_schema.py
│   ├── env.py
│   └── alembic.ini
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Test fixtures
│   ├── test_users.py
│   └── test_items.py
│
├── docker/                         # If deployment enabled
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── k8s/                            # If deployment enabled
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
│
├── .env.example
├── .gitignore
├── requirements.txt
├── pyproject.toml                  # Poetry/PDM/Rye
└── README.md
```

### TypeScript (Hono) Structure

```
crud-api/
├── src/
│   ├── index.ts                    # Hono app entry point
│   ├── config.ts                   # Environment configuration
│   │
│   ├── api/
│   │   ├── v1/
│   │   │   ├── index.ts            # Main router
│   │   │   ├── users.ts            # User CRUD routes
│   │   │   ├── items.ts            # Item CRUD routes
│   │   │   └── auth.ts             # Auth routes (if enabled)
│   │   └── middleware/
│   │       ├── auth.ts             # JWT middleware
│   │       ├── error.ts            # Error handling
│   │       └── validation.ts       # Request validation
│   │
│   ├── db/
│   │   ├── index.ts                # Database connection
│   │   ├── schema/
│   │   │   ├── users.ts            # Drizzle schema
│   │   │   └── items.ts            # Drizzle schema
│   │   └── migrations/
│   │       └── 0000_initial.sql
│   │
│   ├── services/
│   │   ├── user.service.ts
│   │   └── item.service.ts
│   │
│   ├── types/
│   │   ├── user.ts                 # TypeScript interfaces
│   │   └── item.ts
│   │
│   └── auth/                       # If auth enabled
│       ├── jwt.ts                  # JWT utilities
│       ├── password.ts             # bcrypt utilities
│       └── permissions.ts          # RBAC
│
├── drizzle/
│   └── migrations/
│       └── 0000_initial.sql
│
├── tests/
│   ├── users.test.ts
│   └── items.test.ts
│
├── docker/                         # If deployment enabled
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── k8s/                            # If deployment enabled
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
│
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
├── drizzle.config.ts
└── README.md
```

---

## Example API Endpoints (Generated)

Based on resources: `users, products, orders`

### Authentication Endpoints (if enabled)
```
POST   /api/v1/auth/register        # Register new user
POST   /api/v1/auth/login           # Login (returns JWT)
POST   /api/v1/auth/refresh         # Refresh access token
POST   /api/v1/auth/logout          # Logout (invalidate token)
GET    /api/v1/auth/me              # Get current user
```

### User Endpoints
```
POST   /api/v1/users                # Create user (admin only if auth enabled)
GET    /api/v1/users                # List users (paginated)
GET    /api/v1/users/{id}           # Get user by ID
PUT    /api/v1/users/{id}           # Update user
DELETE /api/v1/users/{id}           # Delete user (soft delete)
```

### Product Endpoints
```
POST   /api/v1/products             # Create product
GET    /api/v1/products             # List products (paginated, filterable)
GET    /api/v1/products/{id}        # Get product by ID
PUT    /api/v1/products/{id}        # Update product
DELETE /api/v1/products/{id}        # Delete product
```

### Order Endpoints
```
POST   /api/v1/orders               # Create order (auto-links to current user)
GET    /api/v1/orders               # List orders (user's own or all if admin)
GET    /api/v1/orders/{id}          # Get order by ID
PUT    /api/v1/orders/{id}          # Update order status
DELETE /api/v1/orders/{id}          # Cancel order
```

### Utility Endpoints
```
GET    /health                      # Health check
GET    /docs                        # OpenAPI/Swagger UI
GET    /metrics                     # Prometheus metrics (if monitoring)
```

---

## Database Schema (Generated)

Based on resources: `users, products, orders`

### Python (SQLAlchemy)

**users table:**
```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]  # If auth enabled
    role: Mapped[str] = mapped_column(default="user")  # If auth enabled
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)  # Soft delete

    # Relationships
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
```

**products table:**
```python
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str | None]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))  # If auth enabled
    deleted_at: Mapped[datetime | None]
```

**orders table:**
```python
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    status: Mapped[str] = mapped_column(default="pending")  # pending, completed, cancelled
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: Mapped[datetime | None]

    # Relationships
    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")
```

### TypeScript (Drizzle)

**users table:**
```typescript
export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  username: varchar('username', { length: 100 }).notNull().unique(),
  hashedPassword: varchar('hashed_password', { length: 255 }).notNull(), // If auth enabled
  role: varchar('role', { length: 50 }).default('user'), // If auth enabled
  isActive: boolean('is_active').default(true),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow(),
  deletedAt: timestamp('deleted_at'), // Soft delete
});
```

**products table:**
```typescript
export const products = pgTable('products', {
  id: serial('id').primaryKey(),
  name: varchar('name', { length: 255 }).notNull(),
  description: text('description'),
  price: numeric('price', { precision: 10, scale: 2 }).notNull(),
  stock: integer('stock').default(0),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow(),
  createdBy: integer('created_by').references(() => users.id), // If auth enabled
  deletedAt: timestamp('deleted_at'),
});
```

**orders table:**
```typescript
export const orders = pgTable('orders', {
  id: serial('id').primaryKey(),
  userId: integer('user_id').references(() => users.id).notNull(),
  status: varchar('status', { length: 50 }).default('pending'),
  totalAmount: numeric('total_amount', { precision: 10, scale: 2 }).notNull(),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow(),
  deletedAt: timestamp('deleted_at'),
});
```

---

## Smart Relationship Detection

Blueprint automatically detects and creates relationships:

### Detected Patterns

**users + orders:**
```
orders.user_id → users.id (one-to-many)
```

**users + posts:**
```
posts.author_id → users.id (one-to-many)
```

**products + orders:**
```
Creates junction table: order_items
  - order_items.order_id → orders.id
  - order_items.product_id → products.id
  - order_items.quantity
  - order_items.price
```

**posts + tags:**
```
Creates junction table: post_tags
  - post_tags.post_id → posts.id
  - post_tags.tag_id → tags.id
```

**posts + comments:**
```
comments.post_id → posts.id (one-to-many)
comments.parent_id → comments.id (self-referencing, optional, for nested comments)
```

### Relationship Keywords

The blueprint scans for these patterns:

- `user` or `users` → Assumed as parent for most relationships
- `order`, `purchase`, `transaction` → References user_id
- `post`, `article`, `blog` → References author_id (users)
- `comment`, `review`, `rating` → References both user_id and parent resource
- `tag`, `category`, `label` → Many-to-many junction table
- `product`, `item` → Many-to-many with orders via order_items

---

## Environment Variables (Generated)

**.env.example:**

```bash
# Application
NODE_ENV=development
PORT=8000
API_VERSION=v1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/crud_api
DB_POOL_SIZE=10

# Authentication (if enabled)
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Observability (if enabled)
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
LOG_LEVEL=INFO

# Deployment (if enabled)
DOCKER_REGISTRY=your-registry.io
K8S_NAMESPACE=default
```

---

## Docker Compose (Generated if Deployment Enabled)

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/crud_api
      JWT_SECRET: dev-secret-change-in-prod
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: crud_api
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis (if auth with refresh tokens enabled)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

---

## README.md (Generated)

```markdown
# CRUD API

RESTful CRUD API built with {FastAPI|Hono} and {PostgreSQL|MySQL|SQLite}.

## Features

- ✅ RESTful CRUD endpoints for: {list of resources}
- ✅ {PostgreSQL|MySQL|SQLite} with {SQLAlchemy|Drizzle} ORM
- ✅ Database migrations with {Alembic|drizzle-kit}
{if auth enabled:}
- ✅ JWT authentication with refresh tokens
- ✅ Role-based access control (RBAC)
{if observability enabled:}
- ✅ OpenTelemetry tracing and metrics
- ✅ Structured JSON logging
{if deployment enabled:}
- ✅ Docker and Docker Compose
- ✅ Kubernetes manifests

## Quick Start

### Prerequisites

{if Python:}
- Python 3.11+
- PostgreSQL 14+

### Installation

1. Clone and install dependencies:
```bash
# Using poetry
poetry install

# Or pip
pip install -r requirements.txt
```

2. Set up environment:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. Run migrations:
```bash
alembic upgrade head
```

4. Start development server:
```bash
uvicorn src.main:app --reload
```

{if TypeScript:}
- Node.js 20+
- PostgreSQL 14+

### Installation

1. Clone and install dependencies:
```bash
npm install
```

2. Set up environment:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. Run migrations:
```bash
npm run db:migrate
```

4. Start development server:
```bash
npm run dev
```

## API Documentation

Once running, visit:
- OpenAPI/Swagger: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Endpoints

### Authentication
{if auth enabled:}
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/auth/me` - Get current user

### Resources
{for each resource:}
- `POST /api/v1/{resource}` - Create
- `GET /api/v1/{resource}` - List (paginated)
- `GET /api/v1/{resource}/{id}` - Get by ID
- `PUT /api/v1/{resource}/{id}` - Update
- `DELETE /api/v1/{resource}/{id}` - Delete

## Database Schema

See `src/db/models/` for SQLAlchemy models or `src/db/schema/` for Drizzle schema.

## Testing

```bash
{if Python:}
pytest

{if TypeScript:}
npm test
```

{if deployment enabled:}
## Deployment

### Docker

```bash
docker compose up -d
```

### Kubernetes

```bash
kubectl apply -f k8s/
```

## Project Structure

See `README.md` for detailed structure.

## License

MIT
```

---

## Token Estimate

### Without Optional Skills
```
api-patterns:           ~450 tokens
databases-relational:   ~450 tokens
auth-security:          ~450 tokens
-----------------------------------------
Total:                  ~1,350 tokens
```

### With All Optional Skills
```
Core skills:            ~1,350 tokens
observability:          ~400 tokens
deploying-applications: ~450 tokens
-----------------------------------------
Total:                  ~2,200 tokens
```

---

## Blueprint Activation Logic

The blueprint is automatically selected when:

```python
def should_activate_crud_api_blueprint(goal: str, keywords: list[str]) -> bool:
    """
    Activates CRUD API blueprint if goal matches pattern.

    Returns: True if blueprint should be used, False otherwise
    """
    primary_keywords = ["crud", "rest api", "backend api", "api with database", "crud backend"]
    secondary_keywords = ["fastapi", "database api", "postgresql api", "mysql api", "backend with auth"]

    # Check for primary keyword match
    for keyword in primary_keywords:
        if keyword in goal.lower():
            return True

    # Check for secondary keyword match
    for keyword in secondary_keywords:
        if keyword in goal.lower():
            return True

    # Check for combination: (api OR backend) AND database
    has_api = any(word in goal.lower() for word in ["api", "backend"])
    has_database = any(word in goal.lower() for word in ["database", "postgres", "mysql", "sqlite", "db"])

    if has_api and has_database:
        return True

    return False
```

---

## Workflow Integration

When blueprint is detected:

```
┌─────────────────────────────────────────────────────────────┐
│ CRUD API BLUEPRINT DETECTED                                 │
├─────────────────────────────────────────────────────────────┤
│ Goal: "Build a REST API with PostgreSQL"                    │
│                                                              │
│ Pre-configured skills:                                      │
│   1. api-patterns        (REST, FastAPI/Hono)               │
│   2. databases-relational (PostgreSQL, SQLAlchemy/Drizzle)  │
│   3. auth-security       (JWT, RBAC)                        │
│                                                              │
│ Optional:                                                   │
│   4. observability       (OpenTelemetry)                    │
│   5. deploying-applications (Docker, K8s)                   │
│                                                              │
│ Questions reduced from 20+ to 4:                            │
│   • Language (Python/TypeScript)                            │
│   • Resources (users, products, etc.)                       │
│   • Authentication (yes/no/api-keys)                        │
│   • Advanced features (monitoring/deployment)               │
│                                                              │
│ OPTIONS:                                                    │
│   "confirm" - Use blueprint (recommended)                   │
│   "customize" - Modify skill chain                          │
│   "skip" - Use defaults, no questions                       │
└─────────────────────────────────────────────────────────────┘

Your choice: _
```

---

## Success Criteria

Blueprint is considered successful if:

1. **User completes workflow in < 5 minutes** (vs 15+ without blueprint)
2. **Generated code runs on first try** (after .env configuration)
3. **All CRUD endpoints functional** (create, read, update, delete, list)
4. **Database migrations work** (alembic upgrade head or drizzle-kit push)
5. **Authentication works if enabled** (login returns valid JWT)
6. **OpenAPI docs accessible** (http://localhost:8000/docs)
7. **Docker compose starts cleanly** (if deployment enabled)

---

## Future Enhancements

Potential additions for v2.1:

- **GraphQL variant** (same blueprint, different api-patterns default)
- **Pagination strategies** (cursor-based vs offset-based choice)
- **Caching layer** (Redis integration for read-heavy APIs)
- **File upload** (S3/MinIO integration for media)
- **Webhooks** (Outgoing webhook support for events)
- **API versioning** (URL vs header-based)
- **Rate limiting strategies** (IP-based, user-based, endpoint-based)
- **Search/filtering** (Full-text search with PostgreSQL or Elasticsearch)

---

**Blueprint Version:** 1.0.0
**Last Updated:** 2024-12-02
**Skillchain Version:** 2.0.0
