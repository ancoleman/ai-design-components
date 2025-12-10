# API-First Blueprint

**Version:** 1.0.0
**Last Updated:** 2024-12-06
**Category:** Backend

---

## Overview

Pre-configured skill chain optimized for building production-ready REST APIs, GraphQL endpoints, gRPC services, and API-first architectures. This blueprint provides battle-tested defaults for the most common API patterns, minimizing configuration while maximizing reliability, security, and developer experience.

---

## Trigger Keywords

**Primary (high confidence):**
- api
- rest api
- graphql
- grpc
- api design
- openapi

**Secondary (medium confidence):**
- endpoints
- crud
- microservices
- api gateway
- web service
- backend api
- api server
- json api

**Example goals that match:**
- "build a REST API for user management"
- "create GraphQL API with authentication"
- "design API endpoints for e-commerce"
- "build microservices with gRPC"
- "API with OpenAPI documentation"
- "backend API with JWT auth"

---

## Skill Chain (Pre-configured)

This blueprint invokes 6 skills in the following order:

```
1. designing-apis                (core API design & patterns)
2. implementing-securing-authentication    (authentication & authorization)
3. designing-using-relational-databases (data layer & persistence)
4. testing-strategies            (API testing & validation)
5. implementing-observability    (monitoring, logging, metrics)
6. building-clis                 (optional - API client generation)
```

**Total estimated time:** 30-40 minutes
**Total estimated questions:** 10-15 questions (or 3 with blueprint defaults)

---

## Pre-configured Defaults

### 1. designing-apis
```yaml
api_style: "rest"
  # RESTful API with resource-based endpoints
  # HTTP verbs: GET, POST, PUT, PATCH, DELETE
  # JSON request/response bodies
  # Standard HTTP status codes

version_strategy: "url"
  # Versioning in URL path: /api/v1/users
  # Clean migration path for breaking changes
  # Easy to route and cache

specification: "openapi-3.0"
  # OpenAPI 3.0 specification (formerly Swagger)
  # Auto-generated interactive documentation
  # Client SDK generation support
  # Industry standard for REST APIs

response_format: "json-api"
  # Consistent response structure
  # {
  #   "data": {...},
  #   "meta": { "requestId": "...", "timestamp": "..." },
  #   "errors": [...]
  # }

pagination: "cursor-based"
  # Cursor-based pagination for large datasets
  # Query params: ?limit=20&cursor=abc123
  # More efficient than offset-based
  # Works with real-time data

error_handling: "rfc7807"
  # Problem Details for HTTP APIs (RFC 7807)
  # {
  #   "type": "https://api.example.com/errors/validation",
  #   "title": "Validation Failed",
  #   "status": 422,
  #   "detail": "Email is required",
  #   "instance": "/api/v1/users"
  # }

rate_limiting: true
  # Rate limiting enabled by default
  # Default: 100 requests/minute per API key
  # Headers: X-RateLimit-Limit, X-RateLimit-Remaining
  # 429 Too Many Requests on exceed

cors: "permissive-dev"
  # Development: Allow all origins
  # Production: Whitelist specific domains
  # Credentials support optional
```

### 2. implementing-securing-authentication
```yaml
auth_type: "jwt"
  # JWT (JSON Web Tokens) for stateless auth
  # Access token (15 min expiry) + Refresh token (7 day expiry)
  # HS256 or RS256 signing algorithm
  # Industry standard, works with OAuth2

auth_flow: "bearer-token"
  # Authorization header: Bearer <token>
  # Standard HTTP authentication
  # Works with all HTTP clients
  # Easy to test and debug

api_key_support: true
  # Optional API key authentication for server-to-server
  # Header: X-API-Key or query param: ?api_key=...
  # Useful for webhooks, integrations, public APIs

oauth2_support: false
  # Set to true for OAuth2/OpenID Connect
  # Supports authorization code, client credentials flows
  # Integration with Google, GitHub, Auth0, etc.

rbac: true
  # Role-Based Access Control
  # Roles: admin, user, readonly
  # Permission checks on endpoints
  # Database-backed role assignments

input_validation: "strict"
  # Validate all incoming request bodies
  # JSON schema validation
  # Type coercion and sanitization
  # Reject unknown fields by default

security_headers: true
  # X-Content-Type-Options: nosniff
  # X-Frame-Options: DENY
  # X-XSS-Protection: 1; mode=block
  # Strict-Transport-Security: max-age=31536000

https_only: true
  # Enforce HTTPS in production
  # Redirect HTTP -> HTTPS
  # HSTS headers
  # Secure cookie flags
```

### 3. designing-using-relational-databases
```yaml
database: "postgresql"
  # PostgreSQL for relational data
  # ACID compliance, JSON support
  # Excellent performance and reliability
  # Rich ecosystem of tools

orm: "auto-detect"
  # Python: SQLAlchemy
  # Node.js: Prisma
  # Go: GORM
  # Rust: Diesel

migrations: true
  # Database migration management
  # Version-controlled schema changes
  # Up/down migrations
  # Rollback support

connection_pool: true
  # Connection pooling enabled
  # Pool size: 10-20 connections
  # Prevents connection exhaustion
  # Improves performance

indexing: "auto-suggest"
  # Analyze queries and suggest indexes
  # Index foreign keys by default
  # Composite indexes for common queries
  # EXPLAIN ANALYZE for optimization

transactions: true
  # ACID transaction support
  # Rollback on errors
  # Isolation levels configurable
  # Critical for data integrity
```

### 4. testing-strategies
```yaml
test_types: ["unit", "integration", "e2e"]
  # Unit: Test individual functions/methods
  # Integration: Test API endpoints with test database
  # E2E: Test full request/response cycles

test_framework: "auto-detect"
  # Python: pytest
  # Node.js: Jest
  # Go: testing package
  # Rust: built-in test framework

api_testing: "supertest-style"
  # HTTP request/response testing
  # Test status codes, headers, body
  # Mock external dependencies
  # Snapshot testing for responses

test_database: "separate"
  # Separate test database
  # Reset between test runs
  # Seed with test fixtures
  # Fast and isolated

coverage_target: "80%"
  # 80% code coverage minimum
  # 100% for critical paths (auth, payment)
  # Coverage reports in CI/CD
  # Enforce with pre-commit hooks

load_testing: "optional"
  # Optional load/stress testing
  # Tools: k6, Apache Bench, wrk
  # Test rate limits, throughput
  # Identify bottlenecks
```

### 5. implementing-observability
```yaml
logging: "structured"
  # Structured JSON logs
  # Log levels: DEBUG, INFO, WARN, ERROR, FATAL
  # Request ID correlation
  # Searchable in log aggregation tools

log_destination: "stdout"
  # Log to stdout/stderr
  # Container-friendly (Docker, K8s)
  # Collected by log aggregators
  # Development: Pretty-printed

metrics: "prometheus"
  # Prometheus metrics format
  # /metrics endpoint for scraping
  # Request count, latency, error rate
  # Custom business metrics

tracing: "optional"
  # Distributed tracing with OpenTelemetry
  # Trace requests across services
  # Identify slow operations
  # Enable for microservices

health_checks: true
  # Health check endpoints
  # GET /health (liveness probe)
  # GET /health/ready (readiness probe)
  # Check database, external services

request_logging: true
  # Log all incoming requests
  # Method, path, status, duration
  # User ID, request ID
  # IP address (anonymized in prod)

error_tracking: "optional"
  # Error tracking integration
  # Sentry, Rollbar, Bugsnag
  # Automatic error reporting
  # Stack traces, context
```

### 6. building-clis (optional)
```yaml
cli_generation: "auto"
  # Generate CLI client from OpenAPI spec
  # Language-specific clients
  # HTTP client wrapper

sdk_generation: true
  # Generate SDK for common languages
  # Python, JavaScript/TypeScript, Go
  # Type-safe API clients
  # Auto-complete in IDEs

documentation: "interactive"
  # Interactive API documentation
  # Swagger UI / ReDoc
  # Try-it-out functionality
  # Code examples in multiple languages
```

---

## Quick Questions (Only 3)

When blueprint is detected, ask only these essential questions:

### Question 1: API Style
```
What type of API are you building?

Options:
1. REST API (recommended - resource-based, HTTP verbs, JSON)
2. GraphQL API (query language, single endpoint, type system)
3. gRPC API (high-performance, protobuf, bidirectional streaming)
4. Hybrid (REST + GraphQL)

Your answer: _______________
```

**Why this matters:**
- Determines API design patterns and routing
- Affects serialization format (JSON vs protobuf)
- Influences tooling and client generation
- Impacts performance characteristics

**Default if skipped:** "REST API"

---

### Question 2: Authentication Type
```
How should clients authenticate with your API?

Options:
1. JWT tokens (recommended - stateless, widely supported)
2. API keys (simple, server-to-server, webhooks)
3. OAuth2/OpenID Connect (third-party login, enterprise SSO)
4. None/Public API (no authentication required)

Your answer: _______________
```

**Why this matters:**
- Determines authentication middleware and flows
- Affects token storage and refresh logic
- Influences session management strategy
- Impacts security considerations

**Default if skipped:** "JWT tokens"

---

### Question 3: Language/Framework
```
What language and framework should we use?

Options:
1. Python + FastAPI (modern, async, auto-docs, great DX)
2. Node.js + Express (popular, mature, huge ecosystem)
3. Go + Gin (high performance, compiled, great for microservices)
4. Rust + Axum (blazing fast, memory safe, compile-time guarantees)
5. TypeScript + NestJS (enterprise, Angular-inspired, decorators)

Your answer: _______________
```

**Why this matters:**
- Determines project structure and conventions
- Affects performance characteristics
- Influences dependency management
- Impacts deployment options

**Default if skipped:** "Python + FastAPI"

---

## Blueprint Detection Logic

Trigger this blueprint when the user's goal matches:

```python
def should_use_api_first_blueprint(goal: str) -> bool:
    goal_lower = goal.lower()

    # Primary keywords (high confidence)
    primary_match = any(keyword in goal_lower for keyword in [
        "rest api",
        "graphql",
        "grpc",
        "api design",
        "openapi",
        "api server"
    ])

    # Secondary keywords + backend context
    secondary_match = (
        any(keyword in goal_lower for keyword in ["api", "endpoint", "web service"]) and
        any(keyword in goal_lower for keyword in ["backend", "server", "microservice", "crud"])
    )

    # Exclude frontend-only requests
    frontend_only = any(keyword in goal_lower for keyword in [
        "react", "vue", "angular", "frontend", "ui", "component"
    ])

    return (primary_match or secondary_match) and not frontend_only
```

**Confidence levels:**
- **High (90%+):** Contains "REST API", "GraphQL", or "gRPC"
- **Medium (70-89%):** Contains "API" + backend term
- **Low (50-69%):** Contains "endpoint" or "web service"

**Present blueprint when confidence >= 70%**

---

## Blueprint Offer Message

When blueprint is detected, present this message to the user:

```
┌────────────────────────────────────────────────────────────┐
│ 🚀 API-FIRST BLUEPRINT DETECTED                            │
├────────────────────────────────────────────────────────────┤
│ Your goal matches our optimized API-First Blueprint!      │
│                                                            │
│ Pre-configured features:                                   │
│  ✓ RESTful API with OpenAPI 3.0 spec                      │
│  ✓ JWT authentication + RBAC                              │
│  ✓ PostgreSQL database with ORM                           │
│  ✓ Request validation & error handling                    │
│  ✓ Rate limiting & CORS                                   │
│  ✓ Structured logging & metrics                           │
│  ✓ Health checks & observability                          │
│  ✓ Interactive API documentation                          │
│  ✓ Unit + integration + E2E tests                         │
│  ✓ Auto-generated client SDKs                             │
│                                                            │
│ Using blueprint reduces questions from 15 to 3!           │
│                                                            │
│ Options:                                                   │
│  1. Use blueprint (3 quick questions, ~15 min)            │
│  2. Custom configuration (15 questions, ~40 min)          │
│  3. Skip all questions (use all defaults, ~10 min)        │
│                                                            │
│ Your choice (1/2/3): _____                                │
└────────────────────────────────────────────────────────────┘
```

**Handle responses:**
- **1 or "blueprint"** → Ask only 3 blueprint questions
- **2 or "custom"** → Ask all skill questions (normal flow)
- **3 or "skip"** → Use all defaults, skip all questions

---

## Generated Output Structure

When blueprint is executed, generate this file structure:

```
api-project/
├── src/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py              # API v1 package init
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── users.py             # User CRUD endpoints
│   │   │   │   ├── auth.py              # Auth endpoints (login, refresh)
│   │   │   │   ├── health.py            # Health check endpoints
│   │   │   │   └── metrics.py           # Metrics endpoint (optional)
│   │   │   │
│   │   │   ├── schemas/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user.py              # User request/response schemas
│   │   │   │   ├── auth.py              # Auth schemas (login, token)
│   │   │   │   ├── common.py            # Shared schemas (pagination, error)
│   │   │   │   └── validators.py        # Custom validators
│   │   │   │
│   │   │   ├── dependencies.py          # Route dependencies (auth, db)
│   │   │   └── errors.py                # Custom exceptions
│   │   │
│   │   ├── openapi.yaml                 # OpenAPI 3.0 specification
│   │   ├── router.py                    # Main API router
│   │   └── middleware.py                # Request/response middleware
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt.py                       # JWT token creation/validation
│   │   ├── password.py                  # Password hashing (bcrypt)
│   │   ├── rbac.py                      # Role-based access control
│   │   └── api_keys.py                  # API key management (optional)
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── session.py                   # Database session management
│   │   ├── base.py                      # SQLAlchemy base models
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py                  # User model
│   │   │   ├── token.py                 # Refresh token model
│   │   │   └── api_key.py               # API key model (optional)
│   │   │
│   │   └── migrations/                  # Alembic migrations
│   │       ├── env.py
│   │       ├── alembic.ini
│   │       └── versions/
│   │           └── 001_initial_schema.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                    # Configuration management
│   │   ├── logging.py                   # Structured logging setup
│   │   ├── metrics.py                   # Prometheus metrics
│   │   ├── security.py                  # Security headers, CORS
│   │   └── rate_limit.py                # Rate limiting logic
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py              # User business logic
│   │   └── auth_service.py              # Auth business logic
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── pagination.py                # Cursor-based pagination
│   │   ├── validation.py                # Custom validation helpers
│   │   ├── responses.py                 # Standard response formatters
│   │   └── errors.py                    # Error handling utilities
│   │
│   ├── main.py                          # Application entry point
│   └── app.py                           # FastAPI app creation
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                      # Pytest fixtures
│   │
│   ├── unit/
│   │   ├── test_auth.py                 # Auth logic tests
│   │   ├── test_password.py             # Password hashing tests
│   │   └── test_validators.py           # Validation tests
│   │
│   ├── integration/
│   │   ├── test_user_routes.py          # User endpoint tests
│   │   ├── test_auth_routes.py          # Auth endpoint tests
│   │   └── test_health_routes.py        # Health check tests
│   │
│   └── e2e/
│       ├── test_user_flow.py            # End-to-end user flows
│       └── test_auth_flow.py            # Login/refresh flow
│
├── scripts/
│   ├── generate_api_key.py              # Generate API keys
│   ├── create_user.py                   # Create test user
│   └── migrate.sh                       # Run database migrations
│
├── docs/
│   ├── api-reference.md                 # API documentation
│   ├── authentication.md                # Auth guide
│   ├── rate-limiting.md                 # Rate limiting docs
│   └── examples/
│       ├── curl-examples.sh             # cURL examples
│       ├── python-client.py             # Python client example
│       └── javascript-client.js         # JS client example
│
├── .env.example                         # Environment variables template
├── .gitignore                           # Git ignore rules
├── requirements.txt                     # Python dependencies
├── Dockerfile                           # Docker container definition
├── docker-compose.yml                   # Local development setup
├── pytest.ini                           # Pytest configuration
├── alembic.ini                          # Database migrations config
└── README.md                            # Setup and usage instructions
```

---

## Component Architecture

### Request Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     Incoming HTTP Request                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Middleware Layer                         │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 1. CORS handler (validate origin)                     │ │
│  │ 2. Security headers (X-Content-Type-Options, etc.)    │ │
│  │ 3. Request ID generator (correlation)                 │ │
│  │ 4. Request logger (log incoming request)              │ │
│  │ 5. Rate limiter (check request quota)                 │ │
│  └────────────────────────┬──────────────────────────────────┘ │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Route Handler                            │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 1. Route matching (/api/v1/users)                     │ │
│  │ 2. Authentication check (JWT validation)              │ │
│  │ 3. Authorization check (RBAC permissions)             │ │
│  │ 4. Input validation (Pydantic schemas)                │ │
│  └────────────────────────┬──────────────────────────────────┘ │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Service Layer                            │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 1. Business logic execution                           │ │
│  │ 2. Database queries (via ORM)                         │ │
│  │ 3. External API calls (if needed)                     │ │
│  │ 4. Data transformations                               │ │
│  └────────────────────────┬──────────────────────────────────┘ │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Response Formatting                        │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 1. Serialize response (Pydantic → JSON)               │ │
│  │ 2. Add metadata (requestId, timestamp)                │ │
│  │ 3. Set status code (200, 201, 400, etc.)              │ │
│  │ 4. Set headers (Content-Type, Cache-Control)          │ │
│  └────────────────────────┬──────────────────────────────────┘ │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Response Middleware                        │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 1. Response logger (log status, duration)             │ │
│  │ 2. Metrics collection (increment counters)            │ │
│  │ 3. Error handler (catch uncaught exceptions)          │ │
│  └────────────────────────┬──────────────────────────────────┘ │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   HTTP Response to Client                   │
└─────────────────────────────────────────────────────────────┘
```

### Authentication Flow (JWT)

```
┌─────────────────────────────────────────────────────────────┐
│                   Client Login Request                      │
│  POST /api/v1/auth/login                                    │
│  { "email": "user@example.com", "password": "secret" }      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  1. Validate email/password (check against database)        │
│  2. Hash password and compare (bcrypt)                      │
│  3. Generate JWT access token (15 min expiry)               │
│  4. Generate refresh token (7 day expiry, stored in DB)     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Response with tokens:                                      │
│  {                                                           │
│    "access_token": "eyJhbGc...",                            │
│    "refresh_token": "dGhpcyBp...",                          │
│    "token_type": "Bearer",                                  │
│    "expires_in": 900                                        │
│  }                                                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Client stores tokens and makes authenticated requests:     │
│  GET /api/v1/users/me                                       │
│  Authorization: Bearer eyJhbGc...                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  1. Extract token from Authorization header                 │
│  2. Verify token signature (HS256/RS256)                    │
│  3. Check expiration (exp claim)                            │
│  4. Extract user ID (sub claim)                             │
│  5. Load user from database (optional)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  When access token expires:                                 │
│  POST /api/v1/auth/refresh                                  │
│  { "refresh_token": "dGhpcyBp..." }                         │
│                                                              │
│  → New access token issued                                  │
│  → Refresh token rotated (optional)                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Default API Endpoints

### Authentication Endpoints

```yaml
POST /api/v1/auth/register
  Description: Register new user account
  Request: { "email": "...", "password": "...", "name": "..." }
  Response: { "user": {...}, "access_token": "...", "refresh_token": "..." }
  Status: 201 Created

POST /api/v1/auth/login
  Description: Login with email and password
  Request: { "email": "...", "password": "..." }
  Response: { "access_token": "...", "refresh_token": "...", "expires_in": 900 }
  Status: 200 OK

POST /api/v1/auth/refresh
  Description: Refresh access token
  Request: { "refresh_token": "..." }
  Response: { "access_token": "...", "expires_in": 900 }
  Status: 200 OK

POST /api/v1/auth/logout
  Description: Logout and invalidate refresh token
  Request: { "refresh_token": "..." }
  Response: { "message": "Logged out successfully" }
  Status: 200 OK

POST /api/v1/auth/forgot-password
  Description: Request password reset email
  Request: { "email": "..." }
  Response: { "message": "Password reset email sent" }
  Status: 200 OK

POST /api/v1/auth/reset-password
  Description: Reset password with token
  Request: { "token": "...", "password": "..." }
  Response: { "message": "Password reset successfully" }
  Status: 200 OK
```

### User CRUD Endpoints

```yaml
GET /api/v1/users
  Description: List users (paginated)
  Query: ?limit=20&cursor=abc123&search=john
  Response: { "data": [...], "meta": { "next_cursor": "..." } }
  Status: 200 OK
  Auth: Required (admin role)

POST /api/v1/users
  Description: Create new user
  Request: { "email": "...", "name": "...", "role": "user" }
  Response: { "data": {...}, "meta": {...} }
  Status: 201 Created
  Auth: Required (admin role)

GET /api/v1/users/:id
  Description: Get user by ID
  Response: { "data": {...}, "meta": {...} }
  Status: 200 OK
  Auth: Required (own account or admin)

PATCH /api/v1/users/:id
  Description: Update user (partial)
  Request: { "name": "...", "email": "..." }
  Response: { "data": {...}, "meta": {...} }
  Status: 200 OK
  Auth: Required (own account or admin)

DELETE /api/v1/users/:id
  Description: Delete user
  Response: { "message": "User deleted successfully" }
  Status: 204 No Content
  Auth: Required (admin role)

GET /api/v1/users/me
  Description: Get current authenticated user
  Response: { "data": {...}, "meta": {...} }
  Status: 200 OK
  Auth: Required
```

### Health & Metrics Endpoints

```yaml
GET /health
  Description: Liveness probe (is server running?)
  Response: { "status": "healthy", "timestamp": "..." }
  Status: 200 OK
  Auth: None

GET /health/ready
  Description: Readiness probe (can serve traffic?)
  Response: { "status": "ready", "checks": { "database": "ok", "redis": "ok" } }
  Status: 200 OK
  Auth: None

GET /metrics
  Description: Prometheus metrics
  Response: (Prometheus text format)
  Status: 200 OK
  Auth: None (or internal only)

GET /api/v1/version
  Description: API version info
  Response: { "version": "1.0.0", "build": "abc123", "timestamp": "..." }
  Status: 200 OK
  Auth: None
```

---

## OpenAPI Specification Template

```yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0
  description: Production-ready REST API with authentication
  contact:
    name: API Support
    email: api@example.com
  license:
    name: MIT

servers:
  - url: https://api.example.com/api/v1
    description: Production
  - url: https://staging-api.example.com/api/v1
    description: Staging
  - url: http://localhost:8000/api/v1
    description: Development

security:
  - bearerAuth: []

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        role:
          type: string
          enum: [admin, user, readonly]
        created_at:
          type: string
          format: date-time
      required: [id, email, name, role]

    Error:
      type: object
      properties:
        type:
          type: string
        title:
          type: string
        status:
          type: integer
        detail:
          type: string
        instance:
          type: string

paths:
  /users:
    get:
      summary: List users
      tags: [Users]
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
        - name: cursor
          in: query
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  meta:
                    type: object
                    properties:
                      next_cursor:
                        type: string
```

---

## Dependencies

The blueprint includes these packages (Python + FastAPI example):

```txt
# Core framework
fastapi==0.104.1                  # Modern async web framework
uvicorn[standard]==0.24.0         # ASGI server
pydantic==2.5.0                   # Data validation
pydantic-settings==2.1.0          # Settings management

# Database
sqlalchemy==2.0.23                # ORM
asyncpg==0.29.0                   # Async PostgreSQL driver
alembic==1.12.1                   # Database migrations

# Authentication
python-jose[cryptography]==3.3.0  # JWT creation/validation
passlib[bcrypt]==1.7.4            # Password hashing
python-multipart==0.0.6           # Form data parsing

# Security
python-dotenv==1.0.0              # Environment variables
cryptography==41.0.7              # Cryptographic operations

# Observability
structlog==23.2.0                 # Structured logging
prometheus-client==0.19.0         # Metrics

# Testing
pytest==7.4.3                     # Test framework
pytest-asyncio==0.21.1            # Async test support
httpx==0.25.2                     # HTTP client for testing
faker==20.1.0                     # Test data generation

# Development
black==23.12.0                    # Code formatter
ruff==0.1.7                       # Linter
mypy==1.7.1                       # Type checker
```

**Framework alternatives:**
- **Node.js:** express, fastify, nestjs
- **Go:** gin, echo, fiber
- **Rust:** axum, actix-web, rocket

---

## Error Response Format (RFC 7807)

All errors follow Problem Details for HTTP APIs:

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Failed",
  "status": 422,
  "detail": "Email field is required",
  "instance": "/api/v1/users",
  "errors": [
    {
      "field": "email",
      "message": "Email is required",
      "code": "required"
    }
  ],
  "meta": {
    "request_id": "abc123-def456",
    "timestamp": "2024-12-06T10:30:00Z"
  }
}
```

**Common error types:**
- `validation-error` (400 Bad Request)
- `authentication-error` (401 Unauthorized)
- `authorization-error` (403 Forbidden)
- `not-found` (404 Not Found)
- `conflict` (409 Conflict)
- `rate-limit-exceeded` (429 Too Many Requests)
- `internal-error` (500 Internal Server Error)

---

## Rate Limiting

Default rate limiting configuration:

```yaml
Rate Limits:
  - Anonymous: 60 requests/minute
  - Authenticated (API key): 100 requests/minute
  - Authenticated (JWT): 200 requests/minute
  - Premium tier: 1000 requests/minute

Headers:
  - X-RateLimit-Limit: Maximum requests per window
  - X-RateLimit-Remaining: Remaining requests
  - X-RateLimit-Reset: Unix timestamp when limit resets

Response (when exceeded):
  Status: 429 Too Many Requests
  Body: {
    "type": "https://api.example.com/errors/rate-limit",
    "title": "Rate Limit Exceeded",
    "status": 429,
    "detail": "Too many requests. Try again in 30 seconds.",
    "retry_after": 30
  }
```

---

## Pagination Response Format

Cursor-based pagination (recommended for large datasets):

```json
{
  "data": [
    { "id": "user1", "name": "Alice" },
    { "id": "user2", "name": "Bob" }
  ],
  "meta": {
    "limit": 20,
    "next_cursor": "eyJpZCI6InVzZXIyIn0=",
    "prev_cursor": null,
    "total": null
  }
}
```

**Query parameters:**
- `?limit=20` - Number of items per page (default: 20, max: 100)
- `?cursor=abc123` - Cursor for next/previous page

**Offset-based pagination** (simpler, but less efficient):

```json
{
  "data": [...],
  "meta": {
    "limit": 20,
    "offset": 0,
    "total": 150
  }
}
```

---

## Testing Structure

### Unit Tests (70% of tests)

```python
# tests/unit/test_password.py
def test_hash_password():
    hashed = hash_password("secret123")
    assert hashed != "secret123"
    assert verify_password("secret123", hashed)

def test_verify_password_fails_on_wrong_password():
    hashed = hash_password("secret123")
    assert not verify_password("wrong", hashed)
```

### Integration Tests (25% of tests)

```python
# tests/integration/test_user_routes.py
async def test_create_user(client, admin_token):
    response = await client.post(
        "/api/v1/users",
        json={"email": "test@example.com", "name": "Test User"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["email"] == "test@example.com"

async def test_create_user_requires_auth(client):
    response = await client.post(
        "/api/v1/users",
        json={"email": "test@example.com", "name": "Test User"}
    )
    assert response.status_code == 401
```

### E2E Tests (5% of tests)

```python
# tests/e2e/test_auth_flow.py
async def test_complete_auth_flow(client):
    # Register
    register_response = await client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "secret123", "name": "User"}
    )
    assert register_response.status_code == 201

    # Login
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "secret123"}
    )
    assert login_response.status_code == 200
    tokens = login_response.json()

    # Access protected route
    me_response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    assert me_response.status_code == 200
    assert me_response.json()["data"]["email"] == "user@example.com"
```

---

## Environment Variables

```bash
# .env.example

# Application
APP_NAME="My API"
APP_VERSION="1.0.0"
APP_ENV="development"  # development, staging, production
DEBUG=true

# Server
HOST="0.0.0.0"
PORT=8000
RELOAD=true  # Development only

# Database
DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/myapi"
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# Authentication
JWT_SECRET_KEY="your-secret-key-here-change-in-production"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Security
ALLOWED_ORIGINS="http://localhost:3000,https://example.com"
API_KEY_HEADER="X-API-Key"
BCRYPT_ROUNDS=12

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=100

# Logging
LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT="json"  # json or pretty

# Monitoring
PROMETHEUS_ENABLED=true
SENTRY_DSN=""  # Optional error tracking

# External Services (examples)
SMTP_HOST="smtp.example.com"
SMTP_PORT=587
SMTP_USER=""
SMTP_PASSWORD=""
REDIS_URL="redis://localhost:6379/0"
```

---

## Docker Setup

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/

# Non-root user
RUN useradd -m -u 1000 apiuser && chown -R apiuser:apiuser /app
USER apiuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/myapi
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./src:/app/src  # Development hot-reload

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=myapi
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

---

## Observability & Monitoring

### Structured Logging

```python
# Example log output (JSON format)
{
  "event": "http_request",
  "method": "GET",
  "path": "/api/v1/users/123",
  "status_code": 200,
  "duration_ms": 45,
  "user_id": "user-456",
  "request_id": "abc123-def456",
  "timestamp": "2024-12-06T10:30:00.123Z",
  "level": "info"
}
```

### Prometheus Metrics

```
# Sample /metrics endpoint output

# Request count by method and status
http_requests_total{method="GET",status="200",path="/api/v1/users"} 1523
http_requests_total{method="POST",status="201",path="/api/v1/users"} 89

# Request duration histogram
http_request_duration_seconds_bucket{method="GET",path="/api/v1/users",le="0.1"} 1450
http_request_duration_seconds_bucket{method="GET",path="/api/v1/users",le="0.5"} 1520

# Active requests gauge
http_requests_in_progress{method="GET"} 3

# Database connection pool
db_connections_active 8
db_connections_idle 2
db_connections_max 10
```

---

## Client SDK Examples

### Python Client

```python
# Auto-generated from OpenAPI spec
from my_api_client import MyAPIClient

client = MyAPIClient(
    base_url="https://api.example.com",
    api_key="your-api-key"
)

# Login
tokens = client.auth.login(email="user@example.com", password="secret")

# Set access token
client.set_access_token(tokens.access_token)

# Fetch users
users = client.users.list(limit=20)

# Create user
new_user = client.users.create(email="new@example.com", name="New User")
```

### JavaScript Client

```javascript
// Auto-generated from OpenAPI spec
import { MyAPIClient } from 'my-api-client';

const client = new MyAPIClient({
  baseUrl: 'https://api.example.com',
  apiKey: 'your-api-key'
});

// Login
const { access_token } = await client.auth.login({
  email: 'user@example.com',
  password: 'secret'
});

// Set access token
client.setAccessToken(access_token);

// Fetch users
const users = await client.users.list({ limit: 20 });

// Create user
const newUser = await client.users.create({
  email: 'new@example.com',
  name: 'New User'
});
```

---

## Customization Points

After blueprint generation, users can easily customize:

1. **Database schema:** Add tables/columns in `database/models/`
2. **Endpoints:** Add routes in `api/v1/routes/`
3. **Authentication:** Modify JWT settings in `auth/jwt.py`
4. **Rate limits:** Adjust limits in `core/rate_limit.py`
5. **Validation:** Add custom validators in `api/v1/schemas/validators.py`
6. **Business logic:** Implement in `services/`

---

## Migration Path

If user starts with blueprint but needs additional features later:

1. **Add GraphQL:** Run `/skillchain designing-apis` with GraphQL option
2. **Add WebSockets:** Run `/skillchain implementing-realtime`
3. **Add caching:** Run `/skillchain optimizing-performance`
4. **Add background jobs:** Run `/skillchain processing-async-tasks`
5. **Add file uploads:** Run `/skillchain handling-file-uploads`

All additions will integrate with existing auth and database setup.

---

## Version History

**1.0.0** (2024-12-06)
- Initial API-First blueprint
- 6-skill chain with production-ready defaults
- 3-question quick configuration
- REST API with OpenAPI 3.0 spec
- JWT authentication + RBAC
- PostgreSQL database with migrations
- Structured logging + Prometheus metrics
- Comprehensive test suite
- Auto-generated client SDKs

---

## Related Blueprints

- **Microservices Blueprint:** For distributed API architecture
- **GraphQL Blueprint:** For GraphQL-specific APIs
- **Serverless Blueprint:** For AWS Lambda/Cloud Functions APIs
- **Real-time Blueprint:** For WebSocket/SSE APIs

---

**Blueprint Complete**

---

## Deliverables Specification

This section defines concrete validation checks for blueprint promises, ensuring skills produce what users expect.

### Deliverables

```yaml
deliverables:
  "OpenAPI 3.0 specification":
    primary_skill: designing-apis
    required_files:
      - api/openapi.yaml
    content_checks:
      - pattern: "openapi:\\s*3\\."
        in: api/openapi.yaml
      - pattern: "paths:"
        in: api/openapi.yaml
      - pattern: "components:"
        in: api/openapi.yaml
    maturity_required: [starter, intermediate, advanced]

  "API versioning implementation":
    primary_skill: designing-apis
    required_files:
      - src/api/v1/router.py
    content_checks:
      - pattern: "/v1/"
        in: src/api/v1/
      - pattern: "APIRouter|router|app"
        in: src/api/v1/router.py
    maturity_required: [starter, intermediate, advanced]

  "User CRUD endpoints":
    primary_skill: designing-apis
    required_files:
      - src/api/v1/routes/users.py
    content_checks:
      - pattern: "@.*\\.(get|post|put|patch|delete)"
        in: src/api/v1/routes/users.py
      - pattern: "def (get|create|update|delete).*user"
        in: src/api/v1/routes/users.py
    maturity_required: [starter, intermediate, advanced]

  "Authentication endpoints":
    primary_skill: designing-apis
    required_files:
      - src/api/v1/routes/auth.py
    content_checks:
      - pattern: "login|register|refresh"
        in: src/api/v1/routes/auth.py
      - pattern: "@.*\\.post"
        in: src/api/v1/routes/auth.py
    maturity_required: [starter, intermediate, advanced]

  "JWT token management":
    primary_skill: implementing-securing-authentication
    required_files:
      - src/auth/jwt.py
    content_checks:
      - pattern: "create.*token|encode.*token"
        in: src/auth/jwt.py
      - pattern: "verify.*token|decode.*token"
        in: src/auth/jwt.py
      - pattern: "jwt|jose"
        in: src/auth/jwt.py
    maturity_required: [starter, intermediate, advanced]

  "Password hashing":
    primary_skill: implementing-securing-authentication
    required_files:
      - src/auth/password.py
    content_checks:
      - pattern: "hash.*password|bcrypt"
        in: src/auth/password.py
      - pattern: "verify.*password"
        in: src/auth/password.py
    maturity_required: [starter, intermediate, advanced]

  "RBAC authorization":
    primary_skill: implementing-securing-authentication
    required_files:
      - src/auth/rbac.py
    content_checks:
      - pattern: "role|permission"
        in: src/auth/rbac.py
      - pattern: "check.*permission|require.*role"
        in: src/auth/rbac.py
    maturity_required: [intermediate, advanced]

  "Security headers middleware":
    primary_skill: implementing-securing-authentication
    required_files:
      - src/api/middleware.py
    content_checks:
      - pattern: "X-Content-Type-Options|X-Frame-Options|X-XSS-Protection"
        in: src/api/middleware.py
      - pattern: "middleware|before_request"
        in: src/api/middleware.py
    maturity_required: [intermediate, advanced]

  "Database models":
    primary_skill: designing-using-relational-databases
    required_files:
      - src/database/models/user.py
    content_checks:
      - pattern: "class User|Base|Model"
        in: src/database/models/user.py
      - pattern: "Column|Field|Integer|String"
        in: src/database/models/user.py
    maturity_required: [starter, intermediate, advanced]

  "Database migrations":
    primary_skill: designing-using-relational-databases
    required_files:
      - src/database/migrations/
      - alembic.ini
    content_checks:
      - pattern: "alembic|migration"
        in: alembic.ini
      - pattern: "def upgrade|def downgrade"
        in: src/database/migrations/
    maturity_required: [starter, intermediate, advanced]

  "Database session management":
    primary_skill: designing-using-relational-databases
    required_files:
      - src/database/session.py
    content_checks:
      - pattern: "sessionmaker|Session|engine"
        in: src/database/session.py
      - pattern: "create_engine|get_db"
        in: src/database/session.py
    maturity_required: [starter, intermediate, advanced]

  "Connection pooling":
    primary_skill: designing-using-relational-databases
    required_files:
      - src/database/session.py
    content_checks:
      - pattern: "pool_size|max_overflow"
        in: src/database/session.py
    maturity_required: [intermediate, advanced]

  "Request/response schemas":
    primary_skill: designing-apis
    required_files:
      - src/api/v1/schemas/user.py
      - src/api/v1/schemas/auth.py
    content_checks:
      - pattern: "BaseModel|Schema"
        in: src/api/v1/schemas/
      - pattern: "class.*Request|class.*Response"
        in: src/api/v1/schemas/
    maturity_required: [starter, intermediate, advanced]

  "Input validation schemas":
    primary_skill: implementing-securing-authentication
    required_files:
      - src/api/v1/schemas/validators.py
    content_checks:
      - pattern: "validator|field_validator"
        in: src/api/v1/schemas/validators.py
      - pattern: "validate|check"
        in: src/api/v1/schemas/validators.py
    maturity_required: [intermediate, advanced]

  "RFC 7807 error handling":
    primary_skill: designing-apis
    required_files:
      - src/api/v1/errors.py
      - src/utils/errors.py
    content_checks:
      - pattern: "type.*title.*status.*detail"
        in: src/api/v1/errors.py
      - pattern: "ProblemDetails|RFC7807|problem\\+json"
        in: src/api/v1/errors.py
    maturity_required: [intermediate, advanced]

  "Rate limiting":
    primary_skill: implementing-securing-authentication
    required_files:
      - src/core/rate_limit.py
    content_checks:
      - pattern: "rate.*limit|throttle"
        in: src/core/rate_limit.py
      - pattern: "X-RateLimit|429"
        in: src/core/rate_limit.py
    maturity_required: [intermediate, advanced]

  "CORS configuration":
    primary_skill: implementing-securing-authentication
    required_files:
      - src/core/security.py
    content_checks:
      - pattern: "CORS|allow_origins"
        in: src/core/security.py
      - pattern: "Access-Control-Allow"
        in: src/core/security.py
    maturity_required: [starter, intermediate, advanced]

  "Pagination utilities":
    primary_skill: designing-apis
    required_files:
      - src/utils/pagination.py
    content_checks:
      - pattern: "cursor|next_cursor|prev_cursor"
        in: src/utils/pagination.py
      - pattern: "paginate|limit"
        in: src/utils/pagination.py
    maturity_required: [intermediate, advanced]

  "Structured logging":
    primary_skill: implementing-observability
    required_files:
      - src/core/logging.py
    content_checks:
      - pattern: "structlog|logging|logger"
        in: src/core/logging.py
      - pattern: "json|structured"
        in: src/core/logging.py
    maturity_required: [starter, intermediate, advanced]

  "Prometheus metrics endpoint":
    primary_skill: implementing-observability
    required_files:
      - src/core/metrics.py
      - src/api/v1/routes/metrics.py
    content_checks:
      - pattern: "prometheus|metrics"
        in: src/core/metrics.py
      - pattern: "Counter|Histogram|Gauge"
        in: src/core/metrics.py
      - pattern: "/metrics"
        in: src/api/v1/routes/metrics.py
    maturity_required: [intermediate, advanced]

  "Health check endpoints":
    primary_skill: implementing-observability
    required_files:
      - src/api/v1/routes/health.py
    content_checks:
      - pattern: "/health"
        in: src/api/v1/routes/health.py
      - pattern: "liveness|readiness"
        in: src/api/v1/routes/health.py
      - pattern: "database.*check"
        in: src/api/v1/routes/health.py
    maturity_required: [starter, intermediate, advanced]

  "Request logging middleware":
    primary_skill: implementing-observability
    required_files:
      - src/api/middleware.py
    content_checks:
      - pattern: "log.*request|request.*logger"
        in: src/api/middleware.py
      - pattern: "method|path|status|duration"
        in: src/api/middleware.py
    maturity_required: [starter, intermediate, advanced]

  "Unit tests":
    primary_skill: testing-strategies
    required_files:
      - tests/unit/test_auth.py
      - tests/unit/test_password.py
    content_checks:
      - pattern: "def test_|@pytest"
        in: tests/unit/
      - pattern: "assert"
        in: tests/unit/
    maturity_required: [intermediate, advanced]

  "Integration tests":
    primary_skill: testing-strategies
    required_files:
      - tests/integration/test_user_routes.py
      - tests/integration/test_auth_routes.py
    content_checks:
      - pattern: "def test_|@pytest"
        in: tests/integration/
      - pattern: "client\\.|TestClient"
        in: tests/integration/
      - pattern: "assert.*status_code"
        in: tests/integration/
    maturity_required: [intermediate, advanced]

  "E2E tests":
    primary_skill: testing-strategies
    required_files:
      - tests/e2e/test_auth_flow.py
      - tests/e2e/test_user_flow.py
    content_checks:
      - pattern: "def test_|@pytest"
        in: tests/e2e/
      - pattern: "register.*login|end.*to.*end"
        in: tests/e2e/
    maturity_required: [advanced]

  "Test fixtures and configuration":
    primary_skill: testing-strategies
    required_files:
      - tests/conftest.py
    content_checks:
      - pattern: "@pytest\\.fixture"
        in: tests/conftest.py
      - pattern: "client|db|session"
        in: tests/conftest.py
    maturity_required: [intermediate, advanced]

  "OpenAPI-based client SDK":
    primary_skill: building-clis
    required_files:
      - docs/examples/python-client.py
      - docs/examples/javascript-client.js
    content_checks:
      - pattern: "client|api"
        in: docs/examples/
      - pattern: "auth|login|users"
        in: docs/examples/
    maturity_required: [intermediate, advanced]

  "Docker containerization":
    primary_skill: designing-apis
    required_files:
      - Dockerfile
      - docker-compose.yml
    content_checks:
      - pattern: "FROM"
        in: Dockerfile
      - pattern: "services:|postgres:|redis:"
        in: docker-compose.yml
    maturity_required: [starter, intermediate, advanced]

  "Environment configuration":
    primary_skill: designing-apis
    required_files:
      - .env.example
      - src/core/config.py
    content_checks:
      - pattern: "DATABASE_URL|JWT_SECRET"
        in: .env.example
      - pattern: "Settings|Config|BaseSettings"
        in: src/core/config.py
    maturity_required: [starter, intermediate, advanced]

  "Interactive API documentation":
    primary_skill: designing-apis
    required_files:
      - docs/api-reference.md
    content_checks:
      - pattern: "endpoint|authentication|example"
        in: docs/api-reference.md
    maturity_required: [starter, intermediate, advanced]

  "Setup and usage documentation":
    primary_skill: designing-apis
    required_files:
      - README.md
    content_checks:
      - pattern: "installation|setup|usage"
        in: README.md
      - pattern: "docker|run|start"
        in: README.md
    maturity_required: [starter, intermediate, advanced]
```

### Maturity Profiles

```yaml
maturity_profiles:
  starter:
    description: "Learning-focused REST API with core features, basic authentication, minimal infrastructure"

    require_additionally:
      - "OpenAPI 3.0 specification"
      - "API versioning implementation"
      - "User CRUD endpoints"
      - "Authentication endpoints"
      - "JWT token management"
      - "Password hashing"
      - "Database models"
      - "Database migrations"
      - "Database session management"
      - "Request/response schemas"
      - "CORS configuration"
      - "Structured logging"
      - "Health check endpoints"
      - "Request logging middleware"
      - "Docker containerization"
      - "Environment configuration"
      - "Interactive API documentation"
      - "Setup and usage documentation"

    skip_deliverables:
      - "RBAC authorization"
      - "Security headers middleware"
      - "Connection pooling"
      - "Input validation schemas"
      - "RFC 7807 error handling"
      - "Rate limiting"
      - "Pagination utilities"
      - "Prometheus metrics endpoint"
      - "Unit tests"
      - "Integration tests"
      - "E2E tests"
      - "Test fixtures and configuration"
      - "OpenAPI-based client SDK"

    empty_dirs_allowed:
      - tests/unit/
      - tests/integration/
      - tests/e2e/
      - scripts/
      - docs/examples/

    generation_adjustments:
      - Use Docker Compose for local development (no Kubernetes)
      - Include inline comments explaining API patterns
      - Provide sample .env file with working defaults
      - Generate basic error responses (not RFC 7807)
      - Use simple offset-based pagination instead of cursor-based
      - Include Swagger UI for interactive documentation
      - Add step-by-step setup guide in README

  intermediate:
    description: "Production-ready REST API with comprehensive security, testing, monitoring, and automation"

    require_additionally:
      - "RBAC authorization"
      - "Security headers middleware"
      - "Connection pooling"
      - "Input validation schemas"
      - "RFC 7807 error handling"
      - "Rate limiting"
      - "Pagination utilities"
      - "Prometheus metrics endpoint"
      - "Unit tests"
      - "Integration tests"
      - "Test fixtures and configuration"
      - "OpenAPI-based client SDK"

    skip_deliverables:
      - "E2E tests"

    empty_dirs_allowed:
      - tests/e2e/
      - scripts/

    generation_adjustments:
      - Implement RFC 7807 Problem Details error format
      - Add cursor-based pagination for scalability
      - Include rate limiting with configurable quotas
      - Add comprehensive test suite (80% coverage target)
      - Generate Prometheus metrics for monitoring
      - Include RBAC with role-based permissions
      - Add security headers middleware
      - Configure connection pooling for database
      - Generate Python and JavaScript client SDKs
      - Include API versioning with deprecation support

  advanced:
    description: "Enterprise-grade REST API with full test coverage, advanced security, comprehensive monitoring, client SDKs"

    require_additionally:
      - "E2E tests"

    skip_deliverables: []

    empty_dirs_allowed: []

    generation_adjustments:
      - Include complete test pyramid (unit, integration, E2E)
      - Add end-to-end authentication and user flow tests
      - Implement advanced rate limiting (per-user, per-endpoint)
      - Add comprehensive Prometheus metrics with SLOs
      - Generate multi-language client SDKs (Python, JS, Go)
      - Include API gateway patterns (if microservices)
      - Add distributed tracing support (optional)
      - Implement advanced RBAC with fine-grained permissions
      - Add comprehensive API documentation with examples
      - Include performance testing utilities
```

### Validation Process

After all skills complete, the skillchain orchestrator validates deliverables:

1. **File existence checks**: Verify all `required_files` exist for the selected maturity level
2. **Content pattern matching**: Run regex `content_checks` against file contents
3. **Maturity profile validation**: Ensure deliverables match maturity requirements
4. **Empty directory allowances**: Verify only allowed directories are empty
5. **Cross-skill integration**: Validate that skills work together cohesively

**Validation output:**
```
✓ OpenAPI 3.0 specification (designing-apis)
✓ API versioning implementation (designing-apis)
✓ User CRUD endpoints (designing-apis)
✓ Authentication endpoints (designing-apis)
✓ JWT token management (implementing-securing-authentication)
✓ Password hashing (implementing-securing-authentication)
✗ RBAC authorization - SKIPPED (starter maturity)
✓ Database models (designing-using-relational-databases)
✓ Database migrations (designing-using-relational-databases)
...

Blueprint validation: 18/18 required deliverables present
Maturity level: starter
Status: PASSED
```

---
