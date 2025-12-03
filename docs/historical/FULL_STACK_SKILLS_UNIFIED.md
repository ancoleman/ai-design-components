# Full-Stack Backend Skills: Unified Plan

> **Purpose:** Unified plan merging granular skill structure with Context7 library research for 13 new backend skill categories.
>
> **Date:** December 2025
> **Status:** Ready for Implementation
> **Sources:** FULL_STACK_RESEARCH.md (12 skills) + FULL_STACK_SKILLS_PLAN.md (Context7 research) + deploying-applications

---

## Executive Summary

This unified plan defines **13 backend skill directories** that extend the existing 15 frontend skills into a complete full-stack component library. Each skill follows Anthropic's best practices with progressive disclosure architecture.

### Skill Categories

| Domain | Skills | Count |
|--------|--------|-------|
| **Data Layer** | databases-relational, databases-vector, databases-timeseries, databases-document, databases-graph | 5 |
| **Communication Layer** | api-patterns, message-queues, realtime-sync | 3 |
| **Platform Layer** | observability, auth-security | 2 |
| **AI/ML Layer** | ai-data-engineering, model-serving | 2 |
| **Operations Layer** | deploying-applications | 1 |
| **Total** | | **13** |

### Current + Proposed Skills

```
skills/
├── [15 Frontend Skills]           # Existing
│   ├── design-tokens/
│   ├── data-viz/
│   ├── ai-chat/
│   ├── forms/
│   ├── tables/
│   ├── dashboards/
│   ├── feedback/
│   ├── navigation/
│   ├── search-filter/
│   ├── layout/
│   ├── media/
│   ├── timeline/
│   ├── drag-drop/
│   ├── onboarding/
│   └── assembling-components/
│
└── [13 Backend Skills]            # NEW
    ├── databases-relational/
    ├── databases-vector/
    ├── databases-timeseries/
    ├── databases-document/
    ├── databases-graph/
    ├── api-patterns/
    ├── message-queues/
    ├── realtime-sync/
    ├── observability/
    ├── auth-security/
    ├── ai-data-engineering/
    ├── model-serving/
    └── deploying-applications/
```

---

## Frontend ↔ Backend Integration Map

| Frontend Skill | Primary Backend Skills | Secondary Backend Skills |
|----------------|----------------------|-------------------------|
| **forms** | databases-relational, api-patterns | auth-security |
| **tables** | databases-relational, api-patterns | databases-document |
| **data-viz** | databases-timeseries, api-patterns | databases-relational, realtime-sync |
| **dashboards** | databases-timeseries, api-patterns | observability, realtime-sync |
| **ai-chat** | databases-vector, model-serving | message-queues, realtime-sync |
| **search-filter** | databases-vector, databases-document | api-patterns |
| **feedback** | message-queues, api-patterns | databases-document |
| **media** | api-patterns, databases-document | message-queues |
| **All Frontend** | auth-security | - |
| **assembling-components** | deploying-applications | - |

---

## Skill 1: `databases-relational`

### Overview
Guide selection and implementation of relational databases across Python, Rust, Go, and TypeScript.

### Context7 Library Research

#### Python
| Library | Context7 ID | Trust | Snippets | Use Case |
|---------|-------------|-------|----------|----------|
| **SQLAlchemy 2.0** | `/websites/sqlalchemy_en_21` | High | 7,090 | Primary ORM |
| SQLAlchemy ORM | `/websites/sqlalchemy_en_20_orm` | High | 2,047 | ORM-specific |
| asyncpg | - | - | - | Async PostgreSQL |

#### TypeScript
| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **Prisma 6.x** | `/prisma/prisma` | High | 115 | 96.4 | Primary ORM |
| Prisma Docs | `/prisma/docs` | High | 4,281 | - | Documentation |
| **Drizzle ORM** | `/llmstxt/orm_drizzle_team-llms.txt` | High | 4,037 | 95.4 | Performance-focused |
| Drizzle Docs | `/drizzle-team/drizzle-orm-docs` | High | 1,666 | - | Documentation |

#### Rust
| Library | Use Case |
|---------|----------|
| SQLx 0.8 | Compile-time checked queries |
| SeaORM 1.x | Full ORM |
| Diesel 2.3 | Mature ORM |

#### Go
| Library | Use Case |
|---------|----------|
| GORM v2 | Full ORM |
| sqlc | Code generation from SQL |
| Ent | Graph-based ORM |
| pgx | PostgreSQL driver |

### Decision Framework

```
┌─────────────────────────────────────────────────────────────┐
│                 Database Selection Tree                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PRIMARY CONCERN?                                            │
│  ├── MAXIMUM FLEXIBILITY & EXTENSIONS                        │
│  │   └─ PostgreSQL (pgvector, PostGIS, TimescaleDB)         │
│  │                                                          │
│  ├── EMBEDDED / EDGE DEPLOYMENT                             │
│  │   └─ SQLite or Turso (libSQL)                            │
│  │                                                          │
│  ├── LEGACY SYSTEM / MYSQL REQUIRED                         │
│  │   └─ MySQL with PlanetScale (serverless) or traditional  │
│  │                                                          │
│  ├── RAPID PROTOTYPING                                       │
│  │   ├─ TypeScript → Prisma (DX) or Drizzle (perf)          │
│  │   ├─ Python → SQLModel                                    │
│  │   └─ Go → sqlc (type-safe from SQL)                      │
│  │                                                          │
│  └── MAXIMUM PERFORMANCE                                     │
│      ├─ Rust → SQLx (compile-time verification)             │
│      └─ Go → sqlc (generates type-safe code)                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Serverless Databases
| Database | Type | Key Feature |
|----------|------|-------------|
| **Neon** | PostgreSQL | Database branching, scale-to-zero |
| **PlanetScale** | MySQL (Vitess) | Non-blocking migrations |
| **Turso** | SQLite/libSQL | Edge deployment, microsecond latency |

### Skill Structure

```
databases-relational/
├── init.md                    # Master plan
├── SKILL.md                   # Main skill file
├── references/
│   ├── postgresql.md
│   ├── mysql.md
│   ├── sqlite.md
│   ├── orms-by-language.md
│   └── migration-patterns.md
├── examples/
│   ├── python-sqlalchemy/
│   ├── rust-sqlx/
│   ├── go-sqlc/
│   └── typescript-drizzle/
└── scripts/
    ├── generate_migration.py
    └── validate_schema.py
```

### SKILL.md Frontmatter

```yaml
---
name: databases-relational
description: Relational database implementation across Python, Rust, Go, and TypeScript. Use when building CRUD applications, transactional systems, or structured data storage. Covers PostgreSQL (primary), MySQL, SQLite, ORMs (SQLAlchemy, Prisma, SeaORM, GORM), query builders (Drizzle, sqlc, SQLx), migrations, connection pooling, and serverless databases (Neon, PlanetScale, Turso).
---
```

---

## Skill 2: `databases-vector`

### Overview
Enable vector database operations for RAG systems, semantic search, and AI-native applications.

### Context7 Library Research

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **Qdrant** | `/llmstxt/qdrant_tech_llms-full_txt` | High | 10,154 | 83.1 | Primary vector DB |
| Qdrant Docs | `/websites/qdrant_tech` | High | 2,731 | - | Documentation |
| Qdrant Python | `/qdrant/qdrant-client` | High | 43 | - | Python client |
| Qdrant Rust | `/websites/rs_qdrant-client_qdrant_client` | High | 1,549 | - | Rust client |
| LangChain Qdrant | `/websites/python_langchain_api_reference_qdrant` | High | 108 | - | LangChain integration |

### Vector Database Comparison

| Database | Best For | Open Source | Hybrid Search |
|----------|----------|-------------|---------------|
| **Qdrant** | Complex metadata filtering | Yes | Yes (BM25) |
| **Pinecone** | Zero-ops managed service | No | Yes |
| **Milvus/Zilliz** | Billion-scale, GPU acceleration | Yes | Yes |
| **Weaviate** | GraphQL-native, modules | Yes | Yes |
| **pgvector** | PostgreSQL integration | Yes | Via pg_search |
| **Chroma** | Local development, prototyping | Yes | Limited |
| **LanceDB** | Embedded, serverless | Yes | Yes |

### Decision Framework

```
┌─────────────────────────────────────────────────────────────┐
│              Vector Database Selection Tree                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SCALE & REQUIREMENTS?                                       │
│  ├── ALREADY USING POSTGRESQL                                │
│  │   └─ pgvector (add extension, no new infra)              │
│  │       └─ Scale limit: ~10M vectors efficiently            │
│  │                                                          │
│  ├── PROTOTYPE / LOCAL DEVELOPMENT                          │
│  │   └─ Chroma (in-memory or persistent)                    │
│  │                                                          │
│  ├── COMPLEX METADATA FILTERING                             │
│  │   └─ Qdrant (best filtering performance)                 │
│  │                                                          │
│  ├── BILLION-SCALE VECTORS                                  │
│  │   └─ Milvus / Zilliz (GPU acceleration)                  │
│  │                                                          │
│  ├── ZERO-OPS / MANAGED ONLY                                │
│  │   └─ Pinecone (fully managed, no self-host)              │
│  │                                                          │
│  └── EMBEDDED / SERVERLESS                                   │
│      └─ LanceDB (no server required)                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Embedding Strategy

| Provider | Model | Dimensions | Best For |
|----------|-------|------------|----------|
| **Voyage AI** | voyage-3 | 1024 | Best quality (9.74% better than OpenAI) |
| **OpenAI** | text-embedding-3-large | 3072 | Enterprise reliability |
| **Cohere** | embed-v3 | 1024 | Multilingual |
| **Open Source** | nomic-embed-text-v1.5 | 768 | Self-hosted (English) |
| **Open Source** | BAAI/bge-m3 | 1024 | Self-hosted (Multilingual) |

### Skill Structure

```
databases-vector/
├── init.md
├── SKILL.md
├── references/
│   ├── qdrant.md
│   ├── pinecone.md
│   ├── milvus.md
│   ├── pgvector.md
│   ├── embedding-strategies.md
│   └── chunking-patterns.md
├── examples/
│   ├── rag-pipeline/
│   ├── semantic-search/
│   └── hybrid-search/
└── scripts/
    ├── generate_embeddings.py
    └── benchmark_similarity.py
```

### SKILL.md Frontmatter

```yaml
---
name: databases-vector
description: Vector database implementation for AI/ML applications, semantic search, and RAG systems. Use when building chatbots, search engines, recommendation systems, or similarity-based retrieval. Covers Qdrant (primary), Pinecone, Milvus, pgvector, Chroma, embedding generation (OpenAI, Voyage, Cohere), chunking strategies, and hybrid search patterns.
---
```

---

## Skill 3: `databases-timeseries`

### Overview
Guide selection and implementation of time-series databases for metrics, IoT, financial data, and observability.

### Database Comparison

| Database | Best For | Query Language | Compression |
|----------|----------|----------------|-------------|
| **TimescaleDB** | PostgreSQL shops | SQL | Excellent |
| **InfluxDB** | DevOps metrics | InfluxQL/Flux | Good |
| **ClickHouse** | Analytics, fast aggregation | SQL | Best |
| **QuestDB** | High-ingest IoT | SQL | Good |

### Decision Framework

```
┌─────────────────────────────────────────────────────────────┐
│              Time-Series Database Selection                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PRIMARY USE CASE?                                           │
│  ├── ALREADY ON POSTGRESQL                                   │
│  │   └─ TimescaleDB (extension, SQL compatible)             │
│  │                                                          │
│  ├── DEVOPS / PROMETHEUS METRICS                            │
│  │   └─ InfluxDB or Mimir (Prometheus long-term)            │
│  │                                                          │
│  ├── FASTEST AGGREGATION QUERIES                            │
│  │   └─ ClickHouse (columnar, blazing fast)                 │
│  │                                                          │
│  ├── HIGH-INGEST IOT (millions/sec)                         │
│  │   └─ QuestDB (optimized for writes)                      │
│  │                                                          │
│  └── FINANCIAL / TICK DATA                                   │
│      └─ TimescaleDB or QuestDB                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Key Patterns
- **Hypertables** (TimescaleDB) - automatic partitioning
- **Continuous aggregates** - pre-computed rollups
- **Retention policies** - automatic data expiration
- **Downsampling** - LTTB algorithm for visualization

### Skill Structure

```
databases-timeseries/
├── init.md
├── SKILL.md
├── references/
│   ├── timescaledb.md
│   ├── influxdb.md
│   ├── clickhouse.md
│   └── downsampling-strategies.md
└── examples/
    ├── metrics-dashboard-backend/
    └── iot-data-pipeline/
```

### SKILL.md Frontmatter

```yaml
---
name: databases-timeseries
description: Time-series database implementation for metrics, IoT, financial data, and observability backends. Use when building dashboards, monitoring systems, IoT platforms, or financial applications. Covers TimescaleDB (PostgreSQL), InfluxDB, ClickHouse, QuestDB, continuous aggregates, downsampling (LTTB), and retention policies.
---
```

---

## Skill 4: `databases-document`

### Overview
Guide NoSQL document database selection and implementation for flexible schema applications.

### Database Comparison

| Database | Best For | Consistency | Managed Option |
|----------|----------|-------------|----------------|
| **MongoDB** | General-purpose, aggregation | Tunable | MongoDB Atlas |
| **DynamoDB** | AWS-native, serverless | Strong | AWS (only) |
| **Firestore** | Firebase/GCP, real-time sync | Strong | GCP (only) |
| **CouchDB** | Offline-first, sync | Eventual | Couchbase |

### Skill Structure

```
databases-document/
├── init.md
├── SKILL.md
├── references/
│   ├── mongodb.md
│   ├── dynamodb.md
│   ├── firestore.md
│   └── schema-design-patterns.md
└── examples/
    ├── mongodb-fastapi/
    └── dynamodb-serverless/
```

### SKILL.md Frontmatter

```yaml
---
name: databases-document
description: Document database implementation for flexible schema applications. Use when building content management, user profiles, catalogs, or event logging. Covers MongoDB (primary), DynamoDB, Firestore, schema design patterns, indexing strategies, and aggregation pipelines.
---
```

---

## Skill 5: `databases-graph`

### Overview
Guide graph database selection for relationship-heavy data models.

### Database Comparison

| Database | Best For | Query Language | Open Source |
|----------|----------|----------------|-------------|
| **Neo4j** | General graph, mature | Cypher | Community edition |
| **ArangoDB** | Multi-model (doc+graph) | AQL | Yes |
| **Amazon Neptune** | AWS-native | Gremlin/SPARQL | No |
| **Memgraph** | Real-time, in-memory | Cypher | Yes |

### Skill Structure

```
databases-graph/
├── init.md
├── SKILL.md
├── references/
│   ├── neo4j.md
│   ├── arangodb.md
│   └── cypher-patterns.md
└── examples/
    ├── social-graph/
    └── knowledge-graph/
```

### SKILL.md Frontmatter

```yaml
---
name: databases-graph
description: Graph database implementation for relationship-heavy data models. Use when building social networks, recommendation engines, knowledge graphs, or fraud detection. Covers Neo4j (primary), ArangoDB, Amazon Neptune, Cypher query patterns, and graph data modeling.
---
```

---

## Skill 6: `api-patterns`

### Overview
Comprehensive API development patterns across REST, GraphQL, gRPC, and tRPC.

### Context7 Library Research

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **FastAPI** | `/websites/fastapi_tiangolo` | High | 29,015 | 79.8 | Python REST |
| FastAPI Core | `/fastapi/fastapi` | High | 684 | 87.8 | Core framework |
| **Axum** | `/websites/rs_axum_axum` | High | 7,260 | 77.5 | Rust REST |
| Axum Core | `/tokio-rs/axum` | High | 96 | 76.3 | Tokio-based |
| **Hono** | `/llmstxt/hono_dev_llms_txt` | High | 1,817 | 92.1 | Edge-first |
| Hono Core | `/honojs/hono` | High | 42 | 87.8 | Any JS runtime |
| **tRPC** | `/trpc/trpc` | High | 900 | 92.7 | TypeScript E2E |
| tRPC Docs | `/websites/trpc_io` | High | 1,068 | 90.2 | Documentation |

### Framework Performance Matrix

| Language | Framework | Req/s | Latency | Key Strength |
|----------|-----------|-------|---------|--------------|
| **Rust** | Actix-web | ~150,000 | <1ms | Highest throughput |
| **Rust** | Axum | ~140,000 | <1ms | Tower middleware |
| **Go** | Gin | ~100,000+ | 1-2ms | Largest ecosystem |
| **TypeScript** | Hono | ~50,000 | <5ms cold | Edge-first, 14KB |
| **Python** | FastAPI | ~40,000 | 5-10ms | Auto-docs, Pydantic v2 |
| **TypeScript** | Express | ~15,000 | 10-20ms | Legacy standard |

### Decision Framework

```
┌─────────────────────────────────────────────────────────────┐
│                   API Pattern Selection                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  WHO CONSUMES YOUR API?                                      │
│  ├── PUBLIC / THIRD-PARTY DEVELOPERS                         │
│  │   └─ REST with OpenAPI documentation                      │
│  │       └─ FastAPI (Python), Hono (TS), Axum (Rust)        │
│  │                                                          │
│  ├── FRONTEND TEAM (same org)                                │
│  │   ├─ TypeScript full-stack? → tRPC (zero codegen)        │
│  │   └─ Complex data needs? → GraphQL                        │
│  │                                                          │
│  ├── SERVICE-TO-SERVICE (internal)                           │
│  │   ├─ High performance? → gRPC (Tonic, Connect-Go)        │
│  │   └─ Need browser debugging? → Connect-Go                 │
│  │                                                          │
│  └── MOBILE APPS                                             │
│      ├─ Bandwidth constrained? → GraphQL                     │
│      └─ Simple CRUD? → REST                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### GraphQL Libraries

| Language | Library | Key Feature |
|----------|---------|-------------|
| **Python** | Strawberry 0.287 | Type-hint-based schema |
| **Rust** | async-graphql | High performance |
| **Go** | gqlgen | Code generation |
| **TypeScript** | Pothos | Inference-based, no codegen |

### Skill Structure

```
api-patterns/
├── init.md
├── SKILL.md
├── references/
│   ├── rest-design.md
│   ├── graphql-design.md
│   ├── grpc-design.md
│   ├── trpc-design.md
│   └── pagination-patterns.md
├── examples/
│   ├── python-fastapi/
│   ├── rust-axum/
│   ├── go-gin/
│   └── typescript-hono/
└── scripts/
    ├── generate_openapi.py
    └── validate_api_spec.py
```

### SKILL.md Frontmatter

```yaml
---
name: api-patterns
description: API design and implementation across REST, GraphQL, gRPC, and tRPC patterns. Use when building backend services, public APIs, or service-to-service communication. Covers REST (FastAPI, Axum, Gin, Hono), GraphQL (Strawberry, async-graphql, gqlgen, Pothos), gRPC (Tonic, Connect-Go), tRPC (TypeScript), pagination patterns, and OpenAPI documentation.
---
```

---

## Skill 7: `message-queues`

### Overview
Implement async communication patterns using message brokers and task queues.

### Context7 Library Research

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **Confluent Kafka Python** | `/confluentinc/confluent-kafka-python` | High | 192 | 68.8 | Python Kafka |
| Confluent Kafka Go | `/confluentinc/confluent-kafka-go` | High | 305 | - | Go Kafka |
| Confluent Platform | `/websites/confluent_io-platform-current` | High | 18,627 | - | Full platform |
| **Temporal** | `/websites/temporal_io` | High | 3,769 | 80.9 | Workflow orchestration |
| Temporal Python | `/temporalio/samples-python` | High | 196 | - | Python examples |
| Temporal Go | `/temporalio/samples-go` | High | 79 | - | Go examples |

### Message Broker Comparison

| Broker | Throughput | Latency | Best Use Case |
|--------|-----------|---------|---------------|
| **Apache Kafka** | 500K-1M+ msg/s | 10-50ms | Event streaming, log aggregation |
| **NATS JetStream** | 200K-400K msg/s | Sub-ms to 5ms | Cloud-native microservices, IoT |
| **RabbitMQ** | 50K-100K msg/s | 5-20ms | Complex routing, task queues |
| **Redis Streams** | 100K+ msg/s | Sub-ms | Simple queues, already using Redis |

### Task Queue Comparison

| Queue | Language | Backend | Best For |
|-------|----------|---------|----------|
| **Celery 5.4** | Python | Redis/RabbitMQ | Background jobs |
| **BullMQ 5.x** | TypeScript | Redis | Node.js jobs |
| **Temporal** | Multi | PostgreSQL | Workflow orchestration |
| **Tokio** | Rust | In-process | Async tasks |

### Decision Framework

```
┌─────────────────────────────────────────────────────────────┐
│              Message Queue Selection                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  MESSAGING NEED?                                             │
│  ├── EVENT STREAMING / LOG AGGREGATION                       │
│  │   └─ Apache Kafka (replay, partitioning, exactly-once)   │
│  │                                                          │
│  ├── SIMPLE BACKGROUND JOBS                                  │
│  │   ├─ Python → Celery + Redis                             │
│  │   └─ TypeScript → BullMQ + Redis                         │
│  │                                                          │
│  ├── COMPLEX WORKFLOWS / SAGAS                               │
│  │   └─ Temporal (durable execution)                         │
│  │                                                          │
│  ├── REQUEST-REPLY / RPC                                     │
│  │   └─ NATS (built-in request-reply)                        │
│  │                                                          │
│  ├── COMPLEX ROUTING / FANOUT                                │
│  │   └─ RabbitMQ (exchanges, bindings)                       │
│  │                                                          │
│  └── ALREADY USING REDIS                                     │
│      └─ Redis Streams (no new infra)                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Skill Structure

```
message-queues/
├── init.md
├── SKILL.md
├── references/
│   ├── kafka.md
│   ├── rabbitmq.md
│   ├── nats.md
│   ├── redis-streams.md
│   ├── temporal-workflows.md
│   └── event-patterns.md
└── examples/
    ├── kafka-python/
    ├── temporal-order-processing/
    └── redis-streams-notifications/
```

### SKILL.md Frontmatter

```yaml
---
name: message-queues
description: Async communication patterns using message brokers and task queues. Use when building event-driven systems, background job processing, or service decoupling. Covers Kafka (event streaming), RabbitMQ (complex routing), NATS (cloud-native), Redis Streams, Celery (Python), BullMQ (TypeScript), Temporal (workflows), and event sourcing patterns.
---
```

---

## Skill 8: `realtime-sync`

### Overview
Guide real-time communication patterns for live updates, collaboration, and presence.

### Transport Protocol Comparison

| Protocol | Direction | Reconnection | Best For |
|----------|-----------|--------------|----------|
| **SSE** | Server → Client | Automatic | Live feeds, LLM streaming |
| **WebSocket** | Bidirectional | Manual | Chat, games, collaboration |
| **WebRTC** | Peer-to-peer | Complex | Video, screen share |

### Libraries by Language

| Language | WebSocket | SSE |
|----------|-----------|-----|
| **Python** | websockets, FastAPI WS | sse-starlette |
| **Rust** | tokio-tungstenite, axum WS | axum SSE |
| **Go** | gorilla/websocket, nhooyr/websocket | net/http |
| **TypeScript** | ws, Socket.io | native EventSource |

### Collaboration Patterns
- **CRDTs** (Yjs, Automerge) - conflict-free replicated data types
- **OT** (Operational Transform) - sequential transforms
- **Presence** (who's online, cursor positions)

### Decision Framework

```
┌─────────────────────────────────────────────────────────────┐
│              Real-Time Pattern Selection                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  REAL-TIME TYPE?                                             │
│  ├── ONE-WAY UPDATES (server to client)                      │
│  │   └─ SSE (simpler than WebSocket)                         │
│  │       └─ Use: Live feeds, notifications, LLM streaming   │
│  │                                                          │
│  ├── BIDIRECTIONAL COMMUNICATION                             │
│  │   └─ WebSocket                                            │
│  │       └─ Use: Chat, games, real-time collaboration       │
│  │                                                          │
│  ├── COLLABORATIVE EDITING                                   │
│  │   ├─ Simple (presence, cursors) → WebSocket + custom     │
│  │   └─ Complex (text editing) → Yjs or Automerge (CRDTs)   │
│  │                                                          │
│  ├── VIDEO / SCREEN SHARING                                  │
│  │   └─ WebRTC (peer-to-peer)                                │
│  │                                                          │
│  └── MOBILE / UNRELIABLE CONNECTIONS                         │
│      └─ WebSocket with offline queue + sync                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Skill Structure

```
realtime-sync/
├── init.md
├── SKILL.md
├── references/
│   ├── websockets.md
│   ├── sse.md
│   ├── crdts.md
│   └── presence-patterns.md
└── examples/
    ├── chat-websocket/
    ├── llm-streaming-sse/
    └── collaborative-yjs/
```

### SKILL.md Frontmatter

```yaml
---
name: realtime-sync
description: Real-time communication patterns for live updates, collaboration, and presence. Use when building chat applications, collaborative tools, live dashboards, or streaming interfaces. Covers WebSocket (bidirectional), SSE (server push), WebRTC (peer-to-peer), CRDTs (Yjs, Automerge), presence patterns, and offline sync.
---
```

---

## Skill 9: `observability`

### Overview
Guide monitoring, logging, and tracing implementation using OpenTelemetry as the standard.

### Context7 Library Research

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **OpenTelemetry** | `/websites/opentelemetry_io` | High | 5,888 | 85.9 | Unified observability |
| OTel Python | `/websites/opentelemetry-python_readthedocs_io_en_stable` | High | 926 | - | Python SDK |
| OTel .NET | `/open-telemetry/opentelemetry-dotnet` | High | 202 | 96.9 | .NET SDK |
| OTel JS | `/open-telemetry/opentelemetry-js` | High | 219 | 81.3 | JavaScript SDK |
| OTel Rust | `/open-telemetry/opentelemetry-rust` | High | 55 | 68.2 | Rust SDK |
| OTel Go | `/open-telemetry/opentelemetry-go` | High | 76 | 64.3 | Go SDK |
| Tracing OTel | `/tokio-rs/tracing-opentelemetry` | High | 10 | 86.6 | Rust tracing |

### Three Pillars
- **Metrics** - Prometheus, Grafana, Datadog
- **Logs** - Loki, Elasticsearch, structured logging
- **Traces** - Jaeger, Tempo, distributed tracing

### The LGTM Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    LGTM Observability Stack                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐  │
│  │   Loki   │   │  Grafana │   │   Tempo  │   │   Mimir  │  │
│  │  (Logs)  │   │  (Viz)   │   │ (Traces) │   │ (Metrics)│  │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘  │
│       │              │              │              │         │
│       └──────────────┴──────────────┴──────────────┘         │
│                          │                                   │
│                   Grafana Alloy                              │
│                (Unified Collector)                           │
│                          │                                   │
│                   OpenTelemetry                              │
│               (Application Layer)                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Structured Logging Libraries

| Language | Logger | Key Feature |
|----------|--------|-------------|
| **Python** | structlog 24.x | Context binding |
| **Rust** | tracing 0.1.40 | Spans + events |
| **Go** | slog (stdlib 1.21+) | Native structured |
| **TypeScript** | pino 9.x | Fastest Node logger |

### Critical Pattern: Log Correlation

```python
# Always inject trace_id and span_id
logger.info(
    "request_processed",
    trace_id=span.get_span_context().trace_id,
    span_id=span.get_span_context().span_id,
    user_id=user.id,
    duration_ms=elapsed
)
```

### Skill Structure

```
observability/
├── init.md
├── SKILL.md
├── references/
│   ├── opentelemetry-setup.md
│   ├── structured-logging.md
│   ├── lgtm-stack.md
│   ├── trace-context.md
│   └── alerting-rules.md
├── scripts/
│   ├── setup_otel.py
│   └── generate_dashboards.py
└── examples/
    ├── fastapi-otel/
    ├── axum-tracing/
    └── lgtm-docker-compose/
```

### SKILL.md Frontmatter

```yaml
---
name: observability
description: Monitoring, logging, and tracing implementation using OpenTelemetry as the unified standard. Use when building production systems requiring visibility into performance, errors, and behavior. Covers OpenTelemetry (metrics, logs, traces), Prometheus, Grafana, Loki, Jaeger, Tempo, structured logging (structlog, tracing, slog, pino), and alerting.
---
```

---

## Skill 10: `auth-security`

### Overview
Implement modern authentication and authorization patterns including OAuth 2.1, passkeys, and policy engines.

### Context7 Library Research

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **Auth.js** | `/websites/authjs_dev` | High | 2,480 | 87.4 | Multi-framework auth |
| NextAuth.js | `/nextauthjs/next-auth` | High | 749 | 91.8 | Next.js auth |
| Auth0 Next.js | `/auth0/nextjs-auth0` | High | 353 | 82.7 | Managed auth |
| AuthKit | `/workos/authkit-nextjs` | High | 57 | 93.2 | Enterprise SSO |
| **Zod** | `/colinhacks/zod` | High | 542 | 90.4 | Validation |
| Zod Full | `/websites/zod_dev` | High | 98,238 | 80.7 | Full docs |

### OAuth 2.1 Requirements (2025)

```
┌─────────────────────────────────────────────────────────────┐
│               OAuth 2.1 Mandatory Requirements               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✅ PKCE mandatory for ALL OAuth flows                       │
│  ✅ Exact redirect URI matching                              │
│  ❌ Implicit grant REMOVED                                   │
│  ❌ Resource Owner Password grant REMOVED                    │
│                                                              │
│  JWT Best Practices:                                         │
│  ├── Algorithms: EdDSA (Ed25519) or ES256                   │
│  ├── Never allow algorithm switching                         │
│  ├── Access tokens: 5-15 minutes                            │
│  ├── Refresh tokens: 1-7 days with rotation                 │
│  └── Storage: HTTP-only cookies + SameSite=Strict           │
│                                                              │
│  Password Hashing (OWASP 2025):                             │
│  └── Argon2id: m=64MB, t=3, p=4 (target 150-250ms)          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Authorization Engines

| Engine | Model | Best For |
|--------|-------|----------|
| **Open Policy Agent** | ABAC/general | Kubernetes, cloud-native |
| **Casbin** | RBAC/ABAC/ACL | Embedded library, multi-language |
| **SpiceDB** | ReBAC (Zanzibar) | Large-scale, relationship-heavy |
| **Cerbos** | ABAC | API-first, developer-friendly |

### Libraries by Language

| Language | JWT | OAuth/OIDC | Passkeys |
|----------|-----|------------|----------|
| **Python** | joserfc, Authlib | Authlib | py_webauthn |
| **Rust** | jsonwebtoken 10.x | oauth2 | webauthn-rs |
| **Go** | golang-jwt v5 | go-oidc v3 | go-webauthn |
| **TypeScript** | jose | Auth.js v5 | @simplewebauthn |

### Decision Framework

```
┌─────────────────────────────────────────────────────────────┐
│              Authentication Selection                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  AUTH REQUIREMENT?                                           │
│  ├── RAPID DEVELOPMENT / STARTUP                             │
│  │   └─ Managed: Clerk or Auth.js (NextAuth)                │
│  │                                                          │
│  ├── ENTERPRISE / SSO REQUIRED                               │
│  │   ├─ Managed → Auth0 or Okta                             │
│  │   └─ Self-hosted → Keycloak                              │
│  │                                                          │
│  ├── API-ONLY (no UI)                                        │
│  │   └─ JWT with refresh tokens                              │
│  │       └─ Library: jose (TS), jsonwebtoken (Rust)         │
│  │                                                          │
│  ├── PASSWORDLESS                                            │
│  │   └─ Passkeys/WebAuthn                                    │
│  │       └─ Library: @simplewebauthn (TS), py_webauthn      │
│  │                                                          │
│  └── FINE-GRAINED AUTHORIZATION                              │
│      ├─ Simple roles → RBAC with Casbin                     │
│      ├─ Complex policies → OPA or Cerbos                    │
│      └─ Relationships → SpiceDB (Zanzibar-like)             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Skill Structure

```
auth-security/
├── init.md
├── SKILL.md
├── references/
│   ├── oauth21-guide.md
│   ├── jwt-best-practices.md
│   ├── passkeys-webauthn.md
│   ├── authorization-patterns.md
│   └── password-hashing.md
├── scripts/
│   ├── generate_jwt_keys.py
│   └── validate_oauth_config.py
└── examples/
    ├── authjs-nextjs/
    ├── keycloak-fastapi/
    └── passkeys-demo/
```

### SKILL.md Frontmatter

```yaml
---
name: auth-security
description: Authentication, authorization, and API security implementation. Use when building user systems, protecting APIs, or implementing access control. Covers OAuth 2.1/OIDC, JWT patterns, sessions, Passkeys/WebAuthn, RBAC/ABAC/ReBAC, policy engines (OPA, Casbin, SpiceDB), managed auth (Clerk, Auth0), self-hosted (Keycloak, Ory), and API security best practices.
---
```

---

## Skill 11: `ai-data-engineering`

### Overview
Enable data pipelines, feature stores, and embedding generation for AI/ML systems.

### Context7 Library Research

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **LangChain** | `/websites/langchain_oss_python_langchain` | High | 435 | 79.8 | LLM orchestration |
| LangChain API | `/websites/python_langchain_api_reference` | High | 24,215 | 70.5 | Full API |
| LangChain llms | `/llmstxt/langchain_llms_txt` | High | 3,707 | 75.0 | llms.txt |
| LangChain4j | `/langchain4j/langchain4j` | High | 712 | 82.0 | Java version |
| LangChainGo | `/tmc/langchaingo` | High | 397 | 80.1 | Go version |
| OpenLLMetry | `/traceloop/openllmetry` | High | 97 | 46.7 | LLM observability |

### Feature Stores

| Store | Best For | Real-time | Open Source |
|-------|----------|-----------|-------------|
| **Feast** | Flexibility, any backend | Yes | Yes |
| **Tecton** | Enterprise, managed | Yes | No |
| **Hopsworks** | Governance, regulated | Yes | Yes |

### RAG Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline Architecture                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. INGESTION                                                │
│     ├── Document Loading (PDF, web, code)                   │
│     ├── Chunking (512 tokens, 50-100 overlap)               │
│     └── Embedding Generation (Voyage AI, OpenAI)            │
│                                                              │
│  2. INDEXING                                                 │
│     ├── Vector Store (Qdrant, pgvector)                     │
│     └── Metadata Indexing (filtering, hybrid search)        │
│                                                              │
│  3. RETRIEVAL                                                │
│     ├── Query Embedding                                      │
│     ├── Hybrid Search (Vector + BM25)                       │
│     └── Re-ranking (Cohere, cross-encoder)                  │
│                                                              │
│  4. GENERATION                                               │
│     ├── Context Injection                                    │
│     ├── LLM Call (streaming)                                │
│     └── Citation Extraction                                  │
│                                                              │
│  5. EVALUATION (RAGAS)                                       │
│     ├── Faithfulness                                         │
│     ├── Answer Relevancy                                     │
│     └── Context Precision                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Orchestration Tools

| Tool | Best For | Language |
|------|----------|----------|
| **Dagster** | Asset-centric, modern | Python |
| **Prefect** | Pythonic, cloud-native | Python |
| **Airflow 3.0** | Event-driven (2025) | Python |
| **dbt** | SQL transformations | SQL |

### Skill Structure

```
ai-data-engineering/
├── init.md
├── SKILL.md
├── references/
│   ├── rag-architecture.md
│   ├── embedding-strategies.md
│   ├── langchain-patterns.md
│   ├── feature-stores.md
│   └── evaluation-metrics.md
├── scripts/
│   ├── evaluate_rag.py        # RAGAS evaluation
│   ├── chunk_documents.py
│   └── benchmark_retrieval.py
└── examples/
    ├── langchain-rag/
    ├── llamaindex-agents/
    └── feast-features/
```

### SKILL.md Frontmatter

```yaml
---
name: ai-data-engineering
description: Data pipelines, feature stores, and embedding generation for AI/ML systems. Use when building RAG pipelines, ML feature serving, or data transformations. Covers feature stores (Feast, Tecton), embedding pipelines, chunking strategies, orchestration (Dagster, Prefect, Airflow), dbt transformations, data versioning (LakeFS), and experiment tracking (MLflow, W&B).
---
```

---

## Skill 12: `model-serving`

### Overview
Guide LLM and ML model deployment for inference.

### LLM Serving Engines

| Engine | Best For | Performance |
|--------|----------|-------------|
| **vLLM** | Flexible, HuggingFace models | High (PagedAttention) |
| **TensorRT-LLM** | Maximum NVIDIA GPU efficiency | Highest |
| **TGI** | HuggingFace ecosystem | Good |
| **Ollama** | Local development, simple | Moderate |

### ML Model Serving

| Platform | Best For |
|----------|----------|
| **BentoML** | Easy deployment, microservices |
| **Triton** | Multi-model, multi-framework |
| **TorchServe** | PyTorch models |
| **TFServing** | TensorFlow models |

### LLM Orchestration

| Framework | Best For |
|-----------|----------|
| **LangChain** | General workflows, agents |
| **LlamaIndex** | RAG-focused applications |
| **Haystack** | Enterprise search + generation |
| **Semantic Kernel** | Microsoft ecosystem |

### Decision Framework

```
┌─────────────────────────────────────────────────────────────┐
│                 Model Serving Selection                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  DEPLOYING?                                                  │
│  ├── LLM (Large Language Model)                              │
│  │   ├─ Self-hosted OSS model → vLLM                        │
│  │   ├─ Maximum GPU efficiency → TensorRT-LLM               │
│  │   ├─ Local development → Ollama                          │
│  │   └─ API provider → Use SDK directly                     │
│  │                                                          │
│  ├── TRADITIONAL ML MODEL                                    │
│  │   ├─ Simple deployment → BentoML                         │
│  │   ├─ Multi-model serving → Triton                        │
│  │   └─ PyTorch specific → TorchServe                       │
│  │                                                          │
│  └── RAG / AGENT SYSTEM                                      │
│      ├─ General purpose → LangChain                         │
│      ├─ Search-focused → LlamaIndex                         │
│      └─ Enterprise search → Haystack                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Skill Structure

```
model-serving/
├── init.md
├── SKILL.md
├── references/
│   ├── vllm.md
│   ├── tgi.md
│   ├── bentoml.md
│   ├── langchain-orchestration.md
│   └── inference-optimization.md
└── examples/
    ├── vllm-serving/
    ├── ollama-local/
    └── langchain-agents/
```

### SKILL.md Frontmatter

```yaml
---
name: model-serving
description: LLM and ML model deployment for inference. Use when serving models in production, building AI APIs, or optimizing inference. Covers vLLM (LLM serving), TensorRT-LLM (GPU optimization), Ollama (local), BentoML (ML deployment), Triton (multi-model), LangChain (orchestration), LlamaIndex (RAG), and streaming patterns.
---
```

---

## Skill 13: `deploying-applications`

### Overview
Cover deployment patterns from Kubernetes to serverless and edge functions.

### Context7 Library Research

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **Pulumi** | `/websites/pulumi` | High | 6,034 | 86.4 | IaC (TypeScript) |
| Pulumi Docs | `/pulumi/docs` | High | 9,525 | 94.6 | Documentation |
| Pulumi K8s | `/pulumi/pulumi-kubernetes` | High | 462 | - | Kubernetes |
| Pulumi AWS | `/pulumi/pulumi-aws` | High | 125 | 35.4 | AWS provider |
| Pulumi Examples | `/pulumi/examples` | High | 1,667 | - | Examples |

### Deployment Strategy Selection

```
┌─────────────────────────────────────────────────────────────┐
│                Deployment Strategy Selection                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  WORKLOAD TYPE?                                              │
│  ├── COMPLEX MICROSERVICES                                   │
│  │   └─ Kubernetes + ArgoCD/Flux (GitOps)                   │
│  │       ├─ Service mesh: Linkerd (5-10% overhead)          │
│  │       └─ Helm 4.0 for packaging                          │
│  │                                                          │
│  ├── VARIABLE TRAFFIC / COST-SENSITIVE                       │
│  │   └─ Serverless                                           │
│  │       ├─ Database: Neon, Turso (scale-to-zero)           │
│  │       ├─ Compute: Vercel, AWS Lambda                     │
│  │       └─ Edge: Cloudflare Workers (<5ms cold start)      │
│  │                                                          │
│  └── CONSISTENT LOAD / PREDICTABLE                           │
│      └─ Containers (ECS, Cloud Run, Fly.io)                 │
│                                                              │
│  IaC CHOICE?                                                 │
│  ├─ TypeScript-first → Pulumi (Apache 2.0)                  │
│  ├─ HCL-based → OpenTofu (CNCF, Terraform fork)             │
│  └─ Serverless TypeScript → SST v3 (built on Pulumi)        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Kubernetes Patterns
- **Helm 4.0** (November 2025) - significant architectural changes
- **ArgoCD/Flux** - GitOps over manual helm
- **Linkerd** - 5-10% overhead (vs 25-35% for Istio)

### Edge Functions
- **Cloudflare Workers** - <5ms cold starts with V8 isolates
- **Deno Deploy** - excellent TypeScript DX
- **Hono** - runs identically across all edge runtimes

### Skill Structure

```
deploying-applications/
├── init.md
├── SKILL.md
├── references/
│   ├── kubernetes-patterns.md
│   ├── gitops-argocd.md
│   ├── serverless-dbs.md
│   ├── edge-functions.md
│   └── pulumi-guide.md
├── scripts/
│   ├── generate_k8s_manifests.py
│   └── validate_deployment.py
└── examples/
    ├── pulumi-aws/
    ├── k8s-argocd/
    └── sst-serverless/
```

### SKILL.md Frontmatter

```yaml
---
name: deploying-applications
description: Deployment patterns from Kubernetes to serverless and edge functions. Use when deploying applications, setting up CI/CD, or managing infrastructure. Covers Kubernetes (Helm, ArgoCD), serverless (Vercel, Lambda), edge (Cloudflare Workers, Deno), IaC (Pulumi, OpenTofu, SST), and GitOps patterns.
---
```

---

## Implementation Priority

### Phase 1: Critical Foundation (Weeks 1-4)

| Week | Skill | Rationale |
|------|-------|-----------|
| 1-2 | `api-patterns` | Every app needs APIs |
| 2-3 | `databases-relational` | Data persistence foundation |
| 3-4 | `auth-security` | Security can't be afterthought |

### Phase 2: AI/ML & Observability (Weeks 5-8)

| Week | Skill | Rationale |
|------|-------|-----------|
| 5-6 | `databases-vector` | RAG is critical for AI apps |
| 6-7 | `ai-data-engineering` | Builds on vectors |
| 7-8 | `observability` | Production monitoring |

### Phase 3: Advanced Patterns (Weeks 9-12)

| Week | Skill | Rationale |
|------|-------|-----------|
| 9 | `message-queues` | Async patterns |
| 10 | `realtime-sync` | Live updates |
| 11 | `model-serving` | LLM deployment |
| 12 | `deploying-applications` | Production deployment |

### Phase 4: Specialized (Weeks 13-16)

| Week | Skill | Rationale |
|------|-------|-----------|
| 13 | `databases-timeseries` | Metrics/IoT |
| 14 | `databases-document` | NoSQL patterns |
| 15-16 | `databases-graph` | Relationship data |

---

## Marketplace Integration

### New Plugin Groups

```json
{
  "name": "backend-data-skills",
  "description": "Database and data storage: relational, vector, time-series, document, graph",
  "skills": [
    "./skills/databases-relational",
    "./skills/databases-vector",
    "./skills/databases-timeseries",
    "./skills/databases-document",
    "./skills/databases-graph"
  ]
},
{
  "name": "backend-api-skills",
  "description": "API development, messaging, and real-time communication",
  "skills": [
    "./skills/api-patterns",
    "./skills/message-queues",
    "./skills/realtime-sync"
  ]
},
{
  "name": "backend-platform-skills",
  "description": "Observability, security, and deployment",
  "skills": [
    "./skills/observability",
    "./skills/auth-security",
    "./skills/deploying-applications"
  ]
},
{
  "name": "backend-ai-skills",
  "description": "AI/ML data engineering and model serving",
  "skills": [
    "./skills/ai-data-engineering",
    "./skills/model-serving"
  ]
}
```

---

## Recommended Stack Combinations

### Startup MVP (TypeScript Full-Stack)
```
Frontend: forms + tables + dashboards + ai-chat
Backend: api-patterns (tRPC) + databases-relational (Drizzle + Neon) + auth-security (Auth.js)
Deploy: deploying-applications (Vercel + SST)
```

### Enterprise Microservices (Python/Go)
```
Frontend: data-viz + tables + dashboards + feedback
Backend: api-patterns (FastAPI/gRPC) + databases-relational (SQLAlchemy) + message-queues (Kafka) + observability (OTel)
Deploy: deploying-applications (Kubernetes + ArgoCD)
```

### AI-Native Application (Python)
```
Frontend: ai-chat + search-filter + data-viz
Backend: ai-data-engineering (LangChain) + databases-vector (Qdrant) + api-patterns (FastAPI) + observability (OpenLLMetry)
Deploy: deploying-applications (vLLM + K8s)
```

### High-Performance API (Rust)
```
Frontend: tables + data-viz + forms
Backend: api-patterns (Axum) + databases-relational (SQLx) + databases-vector (Qdrant Rust)
Deploy: deploying-applications (Docker + K8s)
```

---

## Context7 Library Summary

### Highest-Scoring Libraries

| Library | Context7 ID | Score | Snippets | Recommended For |
|---------|-------------|-------|----------|-----------------|
| Prisma | `/prisma/prisma` | 96.4 | 115 | TypeScript ORM |
| OTel .NET | `/open-telemetry/opentelemetry-dotnet` | 96.9 | 202 | .NET observability |
| Drizzle | `/llmstxt/orm_drizzle_team-llms.txt` | 95.4 | 4,037 | Performance ORM |
| Pulumi Docs | `/pulumi/docs` | 94.6 | 9,525 | IaC documentation |
| AuthKit | `/workos/authkit-nextjs` | 93.2 | 57 | Enterprise SSO |
| tRPC | `/trpc/trpc` | 92.7 | 900 | E2E Type Safety |
| Hono | `/llmstxt/hono_dev_llms_txt` | 92.1 | 1,817 | Edge-first APIs |
| NextAuth | `/nextauthjs/next-auth` | 91.8 | 749 | Auth |
| Zod | `/colinhacks/zod` | 90.4 | 542 | Validation |
| tRPC Docs | `/websites/trpc_io` | 90.2 | 1,068 | Documentation |
| FastAPI | `/fastapi/fastapi` | 87.8 | 684 | Python REST |
| Auth.js | `/websites/authjs_dev` | 87.4 | 2,480 | Multi-framework Auth |
| Valkey | `/valkey-io/valkey-doc` | 87.5 | 1,199 | Redis Alternative |
| OpenTelemetry | `/websites/opentelemetry_io` | 85.9 | 5,888 | Observability |
| Qdrant | `/llmstxt/qdrant_tech_llms-full_txt` | 83.1 | 10,154 | Vector DB |
| Temporal | `/websites/temporal_io` | 80.9 | 3,769 | Workflows |

---

## Quality Checklist

### Each init.md Must Include:

- [ ] Clear scope definition
- [ ] Library research with Context7 trust scores
- [ ] Decision framework (ASCII diagram)
- [ ] Multi-language support (Python, TypeScript, Rust, Go where applicable)
- [ ] Integration points with frontend skills
- [ ] Security best practices
- [ ] Performance benchmarks where relevant
- [ ] Example project structure
- [ ] SKILL.md frontmatter template

### Each SKILL.md Must Follow:

- [ ] YAML frontmatter (name, description)
- [ ] Under 500 lines
- [ ] Progressive disclosure to references
- [ ] Working code examples
- [ ] Token-free scripts for automation

---

*Document generated: December 2025*
*Sources: FULL_STACK_RESEARCH.md + FULL_STACK_SKILLS_PLAN.md + Context7*
*Status: Ready for implementation*
