# Full-Stack Backend Skills Research
## Expanding the AI-Assisted Component Library to Full-Stack

**Document Version:** 1.0
**Date:** December 1, 2025
**Purpose:** Define new backend skill directories that complement existing frontend skills, following the established init.md patterns

---

## Executive Summary

The current component library covers 14 frontend skills. To achieve full-stack capability, we need **12 new backend skill directories** organized into 4 domains:

1. **Data Layer** (5 skills): databases-relational, databases-document, databases-vector, databases-timeseries, databases-graph
2. **Communication Layer** (3 skills): api-patterns, message-queues, realtime-sync
3. **Platform Layer** (2 skills): observability, auth-security
4. **AI/ML Layer** (2 skills): ai-data-engineering, model-serving

Each backend skill follows the same structure as frontend skills (init.md → SKILL.md → references/ → examples/ → scripts/).

---

## Frontend ↔ Backend Mapping

### How Backend Skills Connect to Existing Frontend Skills

| Frontend Skill | Primary Backend Skills | Secondary Backend Skills |
|----------------|----------------------|-------------------------|
| **data-viz** | databases-timeseries, api-patterns | databases-relational, realtime-sync |
| **ai-chat** | databases-vector, model-serving | message-queues, realtime-sync |
| **forms** | databases-relational, api-patterns | auth-security |
| **tables** | databases-relational, api-patterns | databases-document |
| **dashboards** | databases-timeseries, api-patterns | observability, realtime-sync |
| **feedback** | message-queues, api-patterns | databases-document |
| **media** | api-patterns, databases-document | message-queues |
| **search-filter** | databases-vector, databases-document | api-patterns |

---

## Proposed Backend Skill Directory Structure

```
skills/
├── [existing frontend skills...]
│
├── databases-relational/
│   ├── init.md
│   ├── SKILL.md
│   ├── references/
│   │   ├── postgresql.md
│   │   ├── mysql.md
│   │   ├── sqlite.md
│   │   ├── orms-by-language.md
│   │   └── migration-patterns.md
│   ├── examples/
│   │   ├── python-sqlalchemy/
│   │   ├── rust-sqlx/
│   │   ├── go-sqlc/
│   │   └── typescript-drizzle/
│   └── scripts/
│       ├── generate_migration.py
│       └── validate_schema.py
│
├── databases-vector/
│   ├── init.md
│   ├── SKILL.md
│   ├── references/
│   │   ├── qdrant.md
│   │   ├── pinecone.md
│   │   ├── milvus.md
│   │   ├── pgvector.md
│   │   ├── chroma.md
│   │   └── embedding-strategies.md
│   ├── examples/
│   │   ├── rag-pipeline/
│   │   ├── semantic-search/
│   │   └── hybrid-search/
│   └── scripts/
│       ├── generate_embeddings.py
│       └── benchmark_similarity.py
│
├── databases-timeseries/
│   ├── init.md
│   ├── SKILL.md
│   ├── references/
│   │   ├── timescaledb.md
│   │   ├── influxdb.md
│   │   ├── clickhouse.md
│   │   └── downsampling-strategies.md
│   └── examples/
│       ├── metrics-dashboard-backend/
│       └── iot-data-pipeline/
│
├── databases-document/
│   ├── init.md
│   ├── SKILL.md
│   ├── references/
│   │   ├── mongodb.md
│   │   ├── dynamodb.md
│   │   ├── firestore.md
│   │   └── schema-design-patterns.md
│   └── examples/
│
├── databases-graph/
│   ├── init.md
│   ├── SKILL.md
│   ├── references/
│   │   ├── neo4j.md
│   │   ├── arangodb.md
│   │   └── cypher-patterns.md
│   └── examples/
│
├── api-patterns/
│   ├── init.md
│   ├── SKILL.md
│   ├── references/
│   │   ├── rest-design.md
│   │   ├── graphql-design.md
│   │   ├── grpc-design.md
│   │   ├── trpc-design.md
│   │   └── pagination-patterns.md
│   ├── examples/
│   │   ├── python-fastapi/
│   │   ├── rust-axum/
│   │   ├── go-gin/
│   │   └── typescript-hono/
│   └── scripts/
│       ├── generate_openapi.py
│       └── validate_api_spec.py
│
├── message-queues/
│   ├── init.md
│   ├── SKILL.md
│   ├── references/
│   │   ├── kafka.md
│   │   ├── rabbitmq.md
│   │   ├── nats.md
│   │   ├── redis-streams.md
│   │   └── event-patterns.md
│   └── examples/
│
├── realtime-sync/
│   ├── init.md
│   ├── SKILL.md
│   ├── references/
│   │   ├── websockets.md
│   │   ├── sse.md
│   │   ├── crdts.md
│   │   └── presence-patterns.md
│   └── examples/
│
├── observability/
│   ├── init.md
│   ├── SKILL.md
│   ├── references/
│   │   ├── opentelemetry.md
│   │   ├── prometheus-grafana.md
│   │   ├── logging-patterns.md
│   │   └── alerting-strategies.md
│   └── examples/
│
├── auth-security/
│   ├── init.md
│   ├── SKILL.md
│   ├── references/
│   │   ├── oauth2-oidc.md
│   │   ├── jwt-patterns.md
│   │   ├── rbac-abac.md
│   │   ├── passkeys.md
│   │   └── api-security.md
│   └── examples/
│
├── ai-data-engineering/
│   ├── init.md
│   ├── SKILL.md
│   ├── references/
│   │   ├── feature-stores.md
│   │   ├── embedding-pipelines.md
│   │   ├── chunking-strategies.md
│   │   ├── data-versioning.md
│   │   └── orchestration.md
│   └── examples/
│
└── model-serving/
    ├── init.md
    ├── SKILL.md
    ├── references/
    │   ├── vllm.md
    │   ├── tgi.md
    │   ├── bentoml.md
    │   └── inference-optimization.md
    └── examples/
```

---

## NEW SKILL #1: databases-relational

### Master Plan Summary

**Purpose:** Guide selection and implementation of relational databases across Python, Rust, Go, and TypeScript.

**Component Taxonomy:**

**Tier 1: Database Engines**
- PostgreSQL (default recommendation - most versatile)
- MySQL/MariaDB (legacy systems, specific workloads)
- SQLite (embedded, edge, development)

**Tier 2: Access Patterns by Language**

| Language | ORM (Full) | Query Builder | Raw/Async |
|----------|-----------|---------------|-----------|
| **Python** | SQLAlchemy 2.0 | SQLModel | asyncpg, psycopg3 |
| **Rust** | SeaORM, Diesel | SQLx | SQLx (compile-time) |
| **Go** | GORM, Ent | sqlc | pgx |
| **TypeScript** | Prisma 6.x | Drizzle ORM | pg, postgres.js |

**Tier 3: Advanced Patterns**
- Connection pooling (PgBouncer, built-in pools)
- Read replicas and write splitting
- Migrations (Alembic, sqlx-migrate, golang-migrate, Prisma Migrate)
- Serverless databases (Neon, PlanetScale, Turso)

**Decision Tree:**

```
START: What's your primary concern?

├─→ MAXIMUM FLEXIBILITY & EXTENSIONS
│   └─ PostgreSQL (pgvector, PostGIS, TimescaleDB)
│
├─→ EMBEDDED / EDGE DEPLOYMENT
│   └─ SQLite or Turso (libSQL)
│
├─→ LEGACY SYSTEM / MYSQL REQUIRED
│   └─ MySQL with PlanetScale (serverless) or traditional
│
├─→ RAPID PROTOTYPING
│   ├─ TypeScript → Prisma or Drizzle
│   ├─ Python → SQLModel
│   └─ Go → sqlc (type-safe from SQL)
│
└─→ MAXIMUM PERFORMANCE (compiled queries)
    ├─ Rust → SQLx (compile-time verification)
    └─ Go → sqlc (generates type-safe code)
```

**Frontend Integration:**

| Frontend Skill | Backend Pattern |
|----------------|-----------------|
| **forms** | Form submission → API → ORM → Database |
| **tables** | Cursor pagination, sorting, filtering APIs |
| **dashboards** | Aggregation queries, materialized views |

**SKILL.md Frontmatter:**

```yaml
---
name: databases-relational
description: Relational database implementation across Python, Rust, Go, and TypeScript. Use when building CRUD applications, transactional systems, or any structured data storage. Covers PostgreSQL (primary), MySQL, SQLite, ORMs (SQLAlchemy, Prisma, SeaORM, GORM), query builders (Drizzle, sqlc, SQLx), migrations, connection pooling, and serverless databases (Neon, PlanetScale, Turso). Triggered by requests to: store structured data, implement CRUD operations, design database schemas, handle transactions, or connect to SQL databases.
---
```

---

## NEW SKILL #2: databases-vector

### Master Plan Summary

**Purpose:** Guide selection and implementation of vector databases for AI/ML applications, semantic search, and RAG systems.

**Component Taxonomy:**

**Tier 1: Vector Database Engines**

| Database | Best For | Open Source | Managed Option |
|----------|----------|-------------|----------------|
| **Qdrant** | Complex filtering, Rust performance | Yes | Qdrant Cloud |
| **Pinecone** | Zero-ops, enterprise | No | Pinecone (only) |
| **Milvus** | Billion-scale, GPU | Yes | Zilliz Cloud |
| **Weaviate** | GraphQL-native, modules | Yes | Weaviate Cloud |
| **pgvector** | PostgreSQL integration | Yes | Any PG host |
| **Chroma** | Local dev, prototyping | Yes | Chroma Cloud |
| **LanceDB** | Embedded, serverless | Yes | LanceDB Cloud |

**Tier 2: Client Libraries by Language**

| Language | Qdrant | Pinecone | Milvus | pgvector |
|----------|--------|----------|--------|----------|
| **Python** | qdrant-client | pinecone-client | pymilvus | pgvector (SQLAlchemy) |
| **Rust** | qdrant-client | - | - | pgvector (SQLx) |
| **Go** | go-client | pinecone-go | milvus-sdk-go | pgx + pgvector |
| **TypeScript** | @qdrant/js-client | @pinecone-database/pinecone | @milvus-io/sdk | pg + pgvector |

**Tier 3: Embedding Generation**

| Provider | Model | Dimensions | Best For |
|----------|-------|------------|----------|
| **OpenAI** | text-embedding-3-large | 3072 | General purpose |
| **Voyage AI** | voyage-3 | 1024 | Best quality (benchmarks) |
| **Cohere** | embed-v3 | 1024 | Multilingual |
| **Open Source** | nomic-embed-text-v1.5 | 768 | Self-hosted |
| **Open Source** | BAAI/bge-m3 | 1024 | Multilingual self-hosted |

**Decision Tree:**

```
START: What's your scale and requirements?

├─→ ALREADY USING POSTGRESQL
│   └─ pgvector (add extension, no new infra)
│       └─ Scale limit: ~10M vectors efficiently
│
├─→ PROTOTYPE / LOCAL DEVELOPMENT
│   └─ Chroma (in-memory or persistent)
│
├─→ COMPLEX METADATA FILTERING
│   └─ Qdrant (best filtering performance)
│
├─→ BILLION-SCALE VECTORS
│   └─ Milvus / Zilliz (GPU acceleration)
│
├─→ ZERO-OPS / MANAGED ONLY
│   └─ Pinecone (fully managed, no self-host)
│
├─→ GRAPHQL-NATIVE / SEMANTIC MODULES
│   └─ Weaviate (built-in vectorizers)
│
└─→ EMBEDDED / SERVERLESS
    └─ LanceDB (no server required)
```

**Frontend Integration (ai-chat skill):**

```
User Query
    ↓
Embedding Generation (OpenAI/Voyage/local)
    ↓
Vector Search (Qdrant/Pinecone/pgvector)
    ↓
Context Retrieval (top-k documents)
    ↓
LLM Generation (with context)
    ↓
Streaming Response → ai-chat frontend
```

**SKILL.md Frontmatter:**

```yaml
---
name: databases-vector
description: Vector database implementation for AI/ML applications, semantic search, and RAG systems. Use when building chatbots, search engines, recommendation systems, or any similarity-based retrieval. Covers Qdrant (primary for filtering), Pinecone (managed), Milvus (scale), pgvector (PostgreSQL), Chroma (prototyping), embedding generation (OpenAI, Voyage, Cohere, sentence-transformers), chunking strategies, and hybrid search patterns. Triggered by requests to: implement RAG, build semantic search, store embeddings, create recommendation engines, or add AI-powered search.
---
```

---

## NEW SKILL #3: databases-timeseries

### Master Plan Summary

**Purpose:** Guide selection and implementation of time-series databases for metrics, IoT, financial data, and observability.

**Component Taxonomy:**

**Tier 1: Database Engines**

| Database | Best For | Query Language | Compression |
|----------|----------|----------------|-------------|
| **TimescaleDB** | PostgreSQL shops | SQL | Excellent |
| **InfluxDB** | DevOps metrics | InfluxQL/Flux | Good |
| **ClickHouse** | Analytics, fast aggregation | SQL | Best |
| **QuestDB** | High-ingest IoT | SQL | Good |

**Tier 2: Key Patterns**
- Hypertables (TimescaleDB) - automatic partitioning
- Continuous aggregates - pre-computed rollups
- Retention policies - automatic data expiration
- Downsampling - LTTB algorithm for visualization

**Decision Tree:**

```
START: What's your primary use case?

├─→ ALREADY ON POSTGRESQL
│   └─ TimescaleDB (extension, SQL compatible)
│
├─→ DEVOPS / PROMETHEUS METRICS
│   └─ InfluxDB or Mimir (Prometheus long-term)
│
├─→ FASTEST AGGREGATION QUERIES
│   └─ ClickHouse (columnar, blazing fast)
│
├─→ HIGH-INGEST IOT (millions/sec)
│   └─ QuestDB (optimized for writes)
│
└─→ FINANCIAL / TICK DATA
    └─ TimescaleDB or QuestDB
```

**Frontend Integration (data-viz, dashboards):**

```
Dashboard Request (time range, granularity)
    ↓
Continuous Aggregate Query (pre-computed)
    ↓
Downsampling (LTTB for large ranges)
    ↓
JSON Response → data-viz charts
```

**SKILL.md Frontmatter:**

```yaml
---
name: databases-timeseries
description: Time-series database implementation for metrics, IoT, financial data, and observability backends. Use when building dashboards, monitoring systems, IoT platforms, or financial applications. Covers TimescaleDB (PostgreSQL), InfluxDB, ClickHouse, QuestDB, continuous aggregates, downsampling (LTTB), retention policies, and real-time streaming patterns. Triggered by requests to: store metrics, build monitoring dashboards, handle IoT data, implement time-based analytics, or create financial data systems.
---
```

---

## NEW SKILL #4: api-patterns

### Master Plan Summary

**Purpose:** Guide API design and implementation across REST, GraphQL, gRPC, and tRPC patterns.

**Component Taxonomy:**

**Tier 1: API Paradigms**

| Pattern | Best For | Type Safety | Streaming |
|---------|----------|-------------|-----------|
| **REST** | Public APIs, simple CRUD | OpenAPI spec | Limited |
| **GraphQL** | Complex data graphs, frontend flexibility | Schema | Subscriptions |
| **gRPC** | Service-to-service, performance | Protobuf | Bidirectional |
| **tRPC** | TypeScript full-stack, internal APIs | Full inference | Limited |

**Tier 2: Frameworks by Language**

| Language | REST | GraphQL | gRPC |
|----------|------|---------|------|
| **Python** | FastAPI, Litestar | Strawberry, Ariadne | grpcio, grpc-aio |
| **Rust** | Axum, Actix-web | async-graphql, Juniper | Tonic |
| **Go** | Gin, Fiber, Echo | gqlgen, 99designs | Connect-Go |
| **TypeScript** | Hono, NestJS, Fastify | Pothos, Apollo Server | nice-grpc |

**Tier 3: Cross-Cutting Concerns**
- Pagination (cursor vs offset)
- Rate limiting
- Caching (HTTP cache, CDN)
- Versioning (URL, header, content-type)
- Error handling (RFC 7807 Problem Details)
- OpenAPI/Swagger documentation

**Decision Tree:**

```
START: Who consumes your API?

├─→ PUBLIC / THIRD-PARTY DEVELOPERS
│   └─ REST with OpenAPI documentation
│       └─ Framework: FastAPI (Python), Hono (TS), Axum (Rust), Gin (Go)
│
├─→ FRONTEND TEAM (same org)
│   ├─ TypeScript full-stack? → tRPC (zero codegen)
│   └─ Complex data needs? → GraphQL
│
├─→ SERVICE-TO-SERVICE (internal)
│   ├─ High performance? → gRPC
│   └─ Need browser debugging? → Connect-Go (gRPC + HTTP/JSON)
│
└─→ MOBILE APPS
    ├─ Bandwidth constrained? → GraphQL (fetch only needed fields)
    └─ Simple CRUD? → REST
```

**Frontend Integration:**

| Frontend Skill | API Pattern | Key Considerations |
|----------------|-------------|-------------------|
| **forms** | REST POST/PUT | Validation errors (422), file uploads |
| **tables** | REST GET with query params | Cursor pagination, sorting, filtering |
| **data-viz** | REST or GraphQL | Aggregation endpoints, SSE for real-time |
| **ai-chat** | SSE (Server-Sent Events) | Streaming LLM responses |
| **dashboards** | GraphQL or REST | Batch queries, partial updates |

**Pagination Pattern for tables skill:**

```
Cursor-based (recommended for infinite scroll):
GET /api/items?cursor=abc123&limit=20

Offset-based (admin panels with page numbers):
GET /api/items?page=3&per_page=20

Response includes:
{
  "data": [...],
  "pagination": {
    "next_cursor": "xyz789",
    "has_more": true
  }
}
```

**SKILL.md Frontmatter:**

```yaml
---
name: api-patterns
description: API design and implementation across REST, GraphQL, gRPC, and tRPC patterns. Use when building backend services, public APIs, or service-to-service communication. Covers REST (FastAPI, Axum, Gin, Hono), GraphQL (Strawberry, async-graphql, gqlgen, Pothos), gRPC (Tonic, Connect-Go), tRPC (TypeScript), pagination patterns, error handling, rate limiting, caching, and OpenAPI documentation. Triggered by requests to: design APIs, implement endpoints, handle pagination, set up GraphQL, configure gRPC, or create type-safe APIs.
---
```

---

## NEW SKILL #5: message-queues

### Master Plan Summary

**Purpose:** Guide async communication patterns using message brokers and task queues.

**Component Taxonomy:**

**Tier 1: Message Brokers**

| Broker | Throughput | Latency | Best For |
|--------|-----------|---------|----------|
| **Apache Kafka** | 1M+ msg/s | 10-50ms | Event streaming, logs |
| **NATS JetStream** | 400K msg/s | <5ms | Cloud-native, IoT |
| **RabbitMQ** | 100K msg/s | 5-20ms | Complex routing |
| **Redis Streams** | 100K+ msg/s | <1ms | Simple queues |

**Tier 2: Task Queues**

| Queue | Language | Backend | Best For |
|-------|----------|---------|----------|
| **Celery** | Python | Redis/RabbitMQ | Background jobs |
| **BullMQ** | TypeScript | Redis | Node.js jobs |
| **Temporal** | Multi | PostgreSQL | Workflow orchestration |
| **Tokio** | Rust | In-process | Async tasks |

**Tier 3: Client Libraries**

| Language | Kafka | RabbitMQ | NATS |
|----------|-------|----------|------|
| **Python** | confluent-kafka | aio-pika | nats-py |
| **Rust** | rdkafka | lapin | async-nats |
| **Go** | confluent-kafka-go | amqp091-go | nats.go |
| **TypeScript** | kafkajs | amqplib | nats.js |

**Decision Tree:**

```
START: What's your messaging need?

├─→ EVENT STREAMING / LOG AGGREGATION
│   └─ Apache Kafka
│       └─ Need: Replay, partitioning, exactly-once
│
├─→ SIMPLE BACKGROUND JOBS
│   ├─ Python → Celery + Redis
│   └─ TypeScript → BullMQ + Redis
│
├─→ COMPLEX WORKFLOWS / SAGAS
│   └─ Temporal (durable execution)
│
├─→ REQUEST-REPLY / RPC
│   └─ NATS (built-in request-reply)
│
├─→ COMPLEX ROUTING / FANOUT
│   └─ RabbitMQ (exchanges, bindings)
│
└─→ ALREADY USING REDIS
    └─ Redis Streams (no new infra)
```

**Frontend Integration:**

| Frontend Skill | Message Pattern |
|----------------|-----------------|
| **forms** | Form submission → Queue → Async processing |
| **feedback** | Notification events → Queue → Push to users |
| **ai-chat** | LLM request → Queue → Worker → Stream response |
| **media** | Upload event → Queue → Transcode worker |

**SKILL.md Frontmatter:**

```yaml
---
name: message-queues
description: Async communication patterns using message brokers and task queues. Use when building event-driven systems, background job processing, or service decoupling. Covers Kafka (event streaming), RabbitMQ (complex routing), NATS (cloud-native), Redis Streams (simple queues), Celery (Python), BullMQ (TypeScript), Temporal (workflows), and event sourcing patterns. Triggered by requests to: process background jobs, implement event-driven architecture, decouple services, handle async operations, or build workflow systems.
---
```

---

## NEW SKILL #6: realtime-sync

### Master Plan Summary

**Purpose:** Guide real-time communication patterns for live updates, collaboration, and presence.

**Component Taxonomy:**

**Tier 1: Transport Protocols**

| Protocol | Direction | Reconnection | Best For |
|----------|-----------|--------------|----------|
| **SSE** | Server → Client | Automatic | Live feeds, LLM streaming |
| **WebSocket** | Bidirectional | Manual | Chat, games, collaboration |
| **WebRTC** | Peer-to-peer | Complex | Video, screen share |

**Tier 2: Libraries by Language**

| Language | WebSocket | SSE |
|----------|-----------|-----|
| **Python** | websockets, FastAPI WS | sse-starlette |
| **Rust** | tokio-tungstenite, axum WS | axum SSE |
| **Go** | gorilla/websocket, nhooyr/websocket | net/http |
| **TypeScript** | ws, Socket.io | native EventSource |

**Tier 3: Collaboration Patterns**
- CRDTs (Yjs, Automerge) - conflict-free replicated data types
- OT (Operational Transform) - sequential transforms
- Presence (who's online, cursor positions)

**Decision Tree:**

```
START: What type of real-time do you need?

├─→ ONE-WAY UPDATES (server to client)
│   └─ SSE (simpler than WebSocket)
│       └─ Use: Live feeds, notifications, LLM streaming
│
├─→ BIDIRECTIONAL COMMUNICATION
│   └─ WebSocket
│       └─ Use: Chat, games, real-time collaboration
│
├─→ COLLABORATIVE EDITING
│   ├─ Simple (presence, cursors) → WebSocket + custom
│   └─ Complex (text editing) → Yjs or Automerge (CRDTs)
│
├─→ VIDEO / SCREEN SHARING
│   └─ WebRTC (peer-to-peer)
│
└─→ MOBILE / UNRELIABLE CONNECTIONS
    └─ WebSocket with offline queue + sync
```

**Frontend Integration:**

| Frontend Skill | Realtime Pattern |
|----------------|------------------|
| **ai-chat** | SSE for LLM streaming responses |
| **dashboards** | SSE for live metric updates |
| **tables** | WebSocket for collaborative editing |
| **data-viz** | SSE for real-time chart updates |

**SKILL.md Frontmatter:**

```yaml
---
name: realtime-sync
description: Real-time communication patterns for live updates, collaboration, and presence. Use when building chat applications, collaborative tools, live dashboards, or streaming interfaces. Covers WebSocket (bidirectional), SSE (server push), WebRTC (peer-to-peer), CRDTs (Yjs, Automerge), presence patterns, and offline sync. Triggered by requests to: implement real-time updates, build chat systems, add collaboration features, stream data, or sync across clients.
---
```

---

## NEW SKILL #7: observability

### Master Plan Summary

**Purpose:** Guide monitoring, logging, and tracing implementation using OpenTelemetry as the standard.

**Component Taxonomy:**

**Tier 1: Three Pillars**
- **Metrics** - Prometheus, Grafana, Datadog
- **Logs** - Loki, Elasticsearch, structured logging
- **Traces** - Jaeger, Tempo, distributed tracing

**Tier 2: OpenTelemetry (Unified Standard)**

| Language | SDK | Auto-Instrumentation |
|----------|-----|---------------------|
| **Python** | opentelemetry-python | Zero-code via CLI |
| **Rust** | opentelemetry-rust | Manual via tracing |
| **Go** | go.opentelemetry.io/otel | eBPF (beta) |
| **TypeScript** | @opentelemetry/sdk-node | Zero-code via --require |

**Tier 3: Logging Libraries**

| Language | Structured Logger | Key Feature |
|----------|------------------|-------------|
| **Python** | structlog | Context binding |
| **Rust** | tracing | Spans + events |
| **Go** | slog (stdlib) | Native in 1.21+ |
| **TypeScript** | pino | Fastest Node logger |

**Decision Tree:**

```
START: What's your observability need?

├─→ STARTING FRESH
│   └─ OpenTelemetry (all three signals)
│       └─ Export to: Grafana Cloud, Datadog, or self-hosted
│
├─→ METRICS ONLY
│   └─ Prometheus + Grafana
│
├─→ LOGS ONLY
│   └─ Structured logging → Loki or Elasticsearch
│
├─→ DISTRIBUTED TRACING
│   └─ OpenTelemetry → Jaeger or Tempo
│
└─→ KUBERNETES NATIVE
    └─ Grafana LGTM Stack (Loki, Grafana, Tempo, Mimir)
```

**Frontend Integration:**

| Frontend Skill | Observability Pattern |
|----------------|----------------------|
| **dashboards** | Display Prometheus metrics in Grafana panels |
| **data-viz** | Visualize application metrics |
| **feedback** | Alert on error rate thresholds |

**SKILL.md Frontmatter:**

```yaml
---
name: observability
description: Monitoring, logging, and tracing implementation using OpenTelemetry as the unified standard. Use when building production systems requiring visibility into performance, errors, and behavior. Covers OpenTelemetry (metrics, logs, traces), Prometheus, Grafana, Loki, Jaeger, Tempo, structured logging (structlog, tracing, slog, pino), alerting, and dashboards. Triggered by requests to: add monitoring, implement logging, set up tracing, create alerts, or debug production issues.
---
```

---

## NEW SKILL #8: auth-security

### Master Plan Summary

**Purpose:** Guide authentication, authorization, and API security implementation.

**Component Taxonomy:**

**Tier 1: Authentication Methods**
- **OAuth 2.1 / OIDC** - Third-party login, enterprise SSO
- **JWT** - Stateless tokens for APIs
- **Session** - Server-side sessions
- **Passkeys/WebAuthn** - Passwordless (2025 standard)

**Tier 2: Authorization Models**

| Model | Best For | Engine |
|-------|----------|--------|
| **RBAC** | Simple role-based | Built-in or Casbin |
| **ABAC** | Attribute-based policies | OPA, Cerbos |
| **ReBAC** | Relationship-based (Zanzibar) | SpiceDB |

**Tier 3: Libraries by Language**

| Language | JWT | OAuth/OIDC | Passkeys |
|----------|-----|------------|----------|
| **Python** | joserfc, Authlib | Authlib | py_webauthn |
| **Rust** | jsonwebtoken | oauth2 | webauthn-rs |
| **Go** | golang-jwt/jwt | go-oidc | go-webauthn |
| **TypeScript** | jose | Auth.js v5 | @simplewebauthn |

**Tier 4: Managed vs Self-Hosted**

| Managed | Self-Hosted | Best For |
|---------|-------------|----------|
| **Clerk** | Keycloak | Speed vs Control |
| **Auth0** | Ory Hydra | Enterprise vs Open Source |
| **Supabase Auth** | SuperTokens | Integrated vs Flexible |

**Decision Tree:**

```
START: What's your auth requirement?

├─→ RAPID DEVELOPMENT / STARTUP
│   └─ Managed: Clerk or Auth.js (NextAuth)
│
├─→ ENTERPRISE / SSO REQUIRED
│   ├─ Managed → Auth0 or Okta
│   └─ Self-hosted → Keycloak
│
├─→ API-ONLY (no UI)
│   └─ JWT with refresh tokens
│       └─ Library: jose (TS), jsonwebtoken (Rust)
│
├─→ PASSWORDLESS
│   └─ Passkeys/WebAuthn
│       └─ Library: @simplewebauthn (TS), py_webauthn
│
└─→ FINE-GRAINED AUTHORIZATION
    ├─ Simple roles → RBAC with Casbin
    ├─ Complex policies → OPA or Cerbos
    └─ Relationships → SpiceDB (Zanzibar-like)
```

**Frontend Integration:**

| Frontend Skill | Auth Pattern |
|----------------|--------------|
| **forms** | Login/register forms, password reset |
| **ai-chat** | User context in conversations |
| **dashboards** | Role-based widget visibility |
| **tables** | Row-level security filtering |

**SKILL.md Frontmatter:**

```yaml
---
name: auth-security
description: Authentication, authorization, and API security implementation. Use when building user systems, protecting APIs, or implementing access control. Covers OAuth 2.1/OIDC, JWT patterns, sessions, Passkeys/WebAuthn, RBAC/ABAC/ReBAC, policy engines (OPA, Casbin, SpiceDB), managed auth (Clerk, Auth0), self-hosted (Keycloak, Ory), and API security best practices. Triggered by requests to: implement login, protect APIs, add authorization, set up SSO, or secure applications.
---
```

---

## NEW SKILL #9: ai-data-engineering

### Master Plan Summary

**Purpose:** Guide data pipelines, feature stores, and embedding generation for AI/ML systems.

**Component Taxonomy:**

**Tier 1: Feature Stores**

| Store | Best For | Real-time | Open Source |
|-------|----------|-----------|-------------|
| **Feast** | Flexibility, any backend | Yes | Yes |
| **Tecton** | Enterprise, managed | Yes | No |
| **Hopsworks** | Governance, regulated | Yes | Yes |

**Tier 2: Embedding Pipelines**
- Text chunking strategies (fixed, semantic, recursive)
- Embedding models (OpenAI, Voyage, Cohere, open source)
- Batch vs streaming generation

**Tier 3: Orchestration**

| Tool | Best For | Language |
|------|----------|----------|
| **Dagster** | Asset-centric, modern | Python |
| **Prefect** | Pythonic, cloud-native | Python |
| **Airflow 3.0** | Event-driven (2025) | Python |
| **dbt** | SQL transformations | SQL |

**Tier 4: Data Versioning**
- LakeFS (acquired DVC in 2025)
- MLflow (experiment tracking)
- Weights & Biases (ML observability)

**Decision Tree:**

```
START: What's your AI data need?

├─→ RAG / SEMANTIC SEARCH
│   ├─ Chunking → recursive with overlap
│   ├─ Embeddings → OpenAI or Voyage AI
│   └─ Storage → databases-vector skill
│
├─→ ML FEATURE SERVING
│   ├─ Simple → Feast (open source)
│   └─ Enterprise → Tecton
│
├─→ DATA TRANSFORMATIONS
│   ├─ SQL-based → dbt
│   └─ Python-based → Dagster or Prefect
│
├─→ EXPERIMENT TRACKING
│   └─ MLflow or Weights & Biases
│
└─→ DATA VERSIONING
    └─ LakeFS (includes DVC)
```

**Frontend Integration (ai-chat):**

```
Document Upload → Chunking → Embedding → Vector DB
                                            ↓
User Query → Embedding → Similarity Search → Context
                                            ↓
                    LLM Generation → ai-chat streaming
```

**SKILL.md Frontmatter:**

```yaml
---
name: ai-data-engineering
description: Data pipelines, feature stores, and embedding generation for AI/ML systems. Use when building RAG pipelines, ML feature serving, or data transformations. Covers feature stores (Feast, Tecton), embedding pipelines, chunking strategies (fixed, semantic, recursive), orchestration (Dagster, Prefect, Airflow), dbt transformations, data versioning (LakeFS/DVC), and experiment tracking (MLflow, W&B). Triggered by requests to: build RAG pipelines, generate embeddings, manage ML features, orchestrate data workflows, or version datasets.
---
```

---

## NEW SKILL #10: model-serving

### Master Plan Summary

**Purpose:** Guide LLM and ML model deployment for inference.

**Component Taxonomy:**

**Tier 1: LLM Serving Engines**

| Engine | Best For | Performance |
|--------|----------|-------------|
| **vLLM** | Flexible, HuggingFace models | High (PagedAttention) |
| **TensorRT-LLM** | Maximum NVIDIA GPU efficiency | Highest |
| **TGI** | HuggingFace ecosystem | Good |
| **Ollama** | Local development, simple | Moderate |

**Tier 2: ML Model Serving**

| Platform | Best For |
|----------|----------|
| **BentoML** | Easy deployment, microservices |
| **Triton** | Multi-model, multi-framework |
| **TorchServe** | PyTorch models |
| **TFServing** | TensorFlow models |

**Tier 3: LLM Orchestration**

| Framework | Best For |
|-----------|----------|
| **LangChain** | General workflows, agents |
| **LlamaIndex** | RAG-focused applications |
| **Haystack** | Enterprise search + generation |
| **Semantic Kernel** | Microsoft ecosystem |

**Decision Tree:**

```
START: What are you deploying?

├─→ LLM (Large Language Model)
│   ├─ Self-hosted OSS model → vLLM
│   ├─ Maximum GPU efficiency → TensorRT-LLM
│   ├─ Local development → Ollama
│   └─ API provider → Use SDK directly
│
├─→ TRADITIONAL ML MODEL
│   ├─ Simple deployment → BentoML
│   ├─ Multi-model serving → Triton
│   └─ PyTorch specific → TorchServe
│
└─→ RAG / AGENT SYSTEM
    ├─ General purpose → LangChain
    ├─ Search-focused → LlamaIndex
    └─ Enterprise search → Haystack
```

**Frontend Integration (ai-chat):**

```
ai-chat frontend
    ↓
API Gateway (rate limiting, auth)
    ↓
LLM Router (model selection)
    ↓
vLLM / TensorRT-LLM (inference)
    ↓
SSE Streaming → ai-chat frontend
```

**SKILL.md Frontmatter:**

```yaml
---
name: model-serving
description: LLM and ML model deployment for inference. Use when serving models in production, building AI APIs, or optimizing inference. Covers vLLM (LLM serving), TensorRT-LLM (GPU optimization), Ollama (local), BentoML (ML deployment), Triton (multi-model), LangChain (orchestration), LlamaIndex (RAG), inference optimization, and streaming patterns. Triggered by requests to: deploy models, serve LLMs, optimize inference, build AI APIs, or create agent systems.
---
```

---

## Implementation Priorities

### Recommended Order

**Phase 1: Core Infrastructure (Weeks 1-4)**
1. **databases-relational** - Foundation for most apps
2. **api-patterns** - Connect frontend to backend
3. **auth-security** - Required for any real app

**Phase 2: AI-Native (Weeks 5-8)**
4. **databases-vector** - Powers ai-chat skill
5. **ai-data-engineering** - RAG pipelines
6. **model-serving** - LLM deployment

**Phase 3: Advanced (Weeks 9-12)**
7. **databases-timeseries** - Powers dashboards/data-viz
8. **message-queues** - Async processing
9. **realtime-sync** - Live updates
10. **observability** - Production monitoring

**Phase 4: Specialized (Weeks 13-16)**
11. **databases-document** - NoSQL patterns
12. **databases-graph** - Relationship data

---

## Cross-Skill Integration Examples

### Example 1: Full-Stack Form Submission

```
Frontend: forms skill
    ↓
Backend: api-patterns (FastAPI POST endpoint)
    ↓
Backend: auth-security (JWT validation)
    ↓
Backend: databases-relational (SQLAlchemy insert)
    ↓
Backend: message-queues (Celery task for email)
```

### Example 2: AI Chat with RAG

```
Frontend: ai-chat skill
    ↓
Backend: api-patterns (SSE endpoint)
    ↓
Backend: databases-vector (Qdrant similarity search)
    ↓
Backend: ai-data-engineering (context retrieval)
    ↓
Backend: model-serving (vLLM generation)
    ↓
Backend: realtime-sync (SSE streaming)
```

### Example 3: Real-Time Dashboard

```
Frontend: dashboards + data-viz skills
    ↓
Backend: api-patterns (GraphQL subscription)
    ↓
Backend: databases-timeseries (TimescaleDB aggregates)
    ↓
Backend: realtime-sync (WebSocket updates)
    ↓
Backend: observability (Prometheus metrics)
```

---

## Summary

| New Skill | Primary Use | Integrates With |
|-----------|------------|-----------------|
| **databases-relational** | CRUD, transactions | forms, tables |
| **databases-vector** | Semantic search, RAG | ai-chat, search-filter |
| **databases-timeseries** | Metrics, IoT | dashboards, data-viz |
| **databases-document** | Flexible schemas | media, feedback |
| **databases-graph** | Relationships | search-filter |
| **api-patterns** | Backend APIs | ALL frontend skills |
| **message-queues** | Async processing | forms, feedback, media |
| **realtime-sync** | Live updates | ai-chat, dashboards, tables |
| **observability** | Monitoring | dashboards |
| **auth-security** | User management | forms, ALL skills |
| **ai-data-engineering** | ML pipelines | ai-chat, databases-vector |
| **model-serving** | LLM deployment | ai-chat |

---

**END OF BACKEND SKILLS RESEARCH**

*This document defines 12 new backend skill directories that complement the existing 14 frontend skills, creating a complete full-stack AI-assisted component library.*