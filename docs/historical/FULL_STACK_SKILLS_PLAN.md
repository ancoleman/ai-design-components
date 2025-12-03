# Full-Stack Skills Plan: Backend Integration for AI Design Components

> **Purpose:** Comprehensive plan for extending the AI Design Components library with backend/full-stack skills that bridge frontend components to production-ready backend systems.
>
> **Date:** December 2025
> **Status:** Planning Phase
> **Research Sources:** Context7, FULL_STACK_SKILLS_source.md

---

## Executive Summary

This plan defines **8 new backend skill categories** that will extend our 15 frontend-focused skills into a complete full-stack component library. These skills follow Anthropic's best practices for Skills development and integrate seamlessly with our existing design token architecture.

### Current State (15 Frontend Skills)
```
├── design-tokens/      # Foundational theming
├── data-viz/           # Data visualization
├── ai-chat/            # AI/Chat interfaces
├── forms/              # Form systems
├── tables/             # Tables & data grids
├── dashboards/         # Dashboard components
├── feedback/           # Feedback & notifications
├── navigation/         # Navigation patterns
├── search-filter/      # Search & filter
├── layout/             # Layout systems
├── media/              # Media management
├── timeline/           # Timeline & activity
├── drag-drop/          # Drag-and-drop
├── onboarding/         # Onboarding & help
└── assembling-components/  # Capstone assembly skill
```

### Proposed State (23 Total Skills)
```
Frontend Skills (15) + Backend Skills (8) = 23 Complete Full-Stack Skills
```

---

## New Backend Skill Categories

### Overview Matrix

| # | Skill Name | Domain | Primary Languages | Strategic Priority |
|---|------------|--------|-------------------|-------------------|
| 1 | `connecting-databases` | Databases | Python, TypeScript, Rust, Go | **CRITICAL** |
| 2 | `managing-vectors` | Vector DBs | Python, TypeScript | **HIGH** |
| 3 | `handling-messages` | Messaging | Python, TypeScript, Go | **HIGH** |
| 4 | `building-apis` | APIs | Python, TypeScript, Rust, Go | **CRITICAL** |
| 5 | `observing-systems` | Observability | Python, TypeScript, Rust, Go | **HIGH** |
| 6 | `securing-applications` | Security | TypeScript, Python | **CRITICAL** |
| 7 | `engineering-ai-data` | AI/ML | Python, TypeScript | **STRATEGIC** |
| 8 | `deploying-applications` | Deployment | TypeScript, Go | **HIGH** |

---

## Skill 1: `connecting-databases`

### Overview
Provides patterns for connecting to and managing databases across relational, time-series, and key-value stores.

### Scope
- **Relational Databases**: PostgreSQL, MySQL, SQLite
- **ORMs & Query Builders**: SQLAlchemy, Prisma, Drizzle ORM, SeaORM
- **Time-Series**: TimescaleDB, ClickHouse
- **Key-Value**: Redis, Valkey, DragonflyDB
- **Serverless DBs**: Neon, Turso, PlanetScale

### Library Research (Context7)

#### Python
| Library | Context7 ID | Trust | Snippets | Use Case |
|---------|-------------|-------|----------|----------|
| **SQLAlchemy 2.0** | `/websites/sqlalchemy_en_21` | High | 7,090 | Primary ORM |
| SQLAlchemy ORM | `/websites/sqlalchemy_en_20_orm` | High | 2,047 | ORM-specific |
| asyncpg | - | - | - | Async PostgreSQL |

#### TypeScript
| Library | Context7 ID | Trust | Snippets | Use Case |
|---------|-------------|-------|----------|----------|
| **Prisma 6.x** | `/prisma/prisma` | High | 115 | Primary ORM (96.4 score) |
| Prisma Docs | `/prisma/docs` | High | 4,281 | Documentation |
| **Drizzle ORM** | `/llmstxt/orm_drizzle_team-llms.txt` | High | 4,037 | Performance-focused (95.4 score) |
| Drizzle Docs | `/drizzle-team/drizzle-orm-docs` | High | 1,666 | Documentation |

#### Rust
| Library | Context7 ID | Trust | Snippets | Use Case |
|---------|-------------|-------|----------|----------|
| SQLx | - | - | - | Compile-time checked queries |
| SeaORM | - | - | - | Full ORM |

#### Go
| Library | Context7 ID | Trust | Snippets | Use Case |
|---------|-------------|-------|----------|----------|
| GORM v2 | - | - | - | Full ORM |
| sqlc | - | - | - | Code generation |
| pgx | - | - | - | PostgreSQL driver |

### Key-Value Stores
| Library | Context7 ID | Trust | Snippets | Use Case |
|---------|-------------|-------|----------|----------|
| **Valkey** | `/valkey-io/valkey-doc` | High | 1,199 | Redis-compatible (87.5 score) |
| Redis | `/websites/redis_io` | High | 15,375 | Primary cache |
| Valkey GLIDE | `/valkey-io/valkey-glide` | High | 1,044 | Official client |

### Decision Framework
```
┌─────────────────────────────────────────────────────────────┐
│                 Database Selection Tree                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Data Type?                                                  │
│  ├── Relational/Transactional → PostgreSQL                  │
│  │   ├── Python → SQLAlchemy 2.0 + asyncpg                  │
│  │   ├── TypeScript → Drizzle (performance) or Prisma (DX)  │
│  │   ├── Rust → SQLx (compile-time) or SeaORM (full ORM)   │
│  │   └── Go → sqlc (codegen) or GORM (ORM)                 │
│  │                                                          │
│  ├── Time-Series → TimescaleDB (PostgreSQL) or ClickHouse  │
│  │                                                          │
│  ├── Key-Value/Cache → Redis/Valkey                        │
│  │   └── High throughput → DragonflyDB (25x faster)        │
│  │                                                          │
│  └── Edge/Serverless                                        │
│      ├── PostgreSQL → Neon (branching, scale-to-zero)      │
│      ├── MySQL → PlanetScale (non-blocking migrations)     │
│      └── SQLite → Turso (edge, microsecond latency)        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Init.md Structure
```
connecting-databases/
├── init.md                    # Master plan (this content)
├── SKILL.md                   # Main skill file
├── references/
│   ├── orm-patterns.md        # ORM best practices
│   ├── connection-pooling.md  # Connection management
│   ├── migrations.md          # Schema migrations
│   ├── query-optimization.md  # Performance tuning
│   └── serverless-dbs.md      # Neon, Turso, PlanetScale
├── scripts/
│   ├── generate_schema.py     # Schema generation
│   └── validate_migrations.py # Migration validation
└── examples/
    ├── prisma-nextjs/         # Prisma + Next.js
    ├── drizzle-hono/          # Drizzle + Hono
    ├── sqlalchemy-fastapi/    # SQLAlchemy + FastAPI
    └── sqlx-axum/             # SQLx + Axum
```

---

## Skill 2: `managing-vectors`

### Overview
Enables vector database operations for RAG systems, semantic search, and AI-native applications.

### Scope
- **Dedicated Vector DBs**: Qdrant, Milvus, Weaviate, Pinecone
- **PostgreSQL Extension**: pgvector
- **Embedding Generation**: Voyage AI, OpenAI, sentence-transformers
- **Hybrid Search**: BM25 + Vector

### Library Research (Context7)

| Library | Context7 ID | Trust | Snippets | Use Case |
|---------|-------------|-------|----------|----------|
| **Qdrant** | `/llmstxt/qdrant_tech_llms-full_txt` | High | 10,154 | Primary vector DB (83.1 score) |
| Qdrant Docs | `/websites/qdrant_tech` | High | 2,731 | Documentation |
| Qdrant Python | `/qdrant/qdrant-client` | High | 43 | Python client |
| Qdrant Rust | `/websites/rs_qdrant-client_qdrant_client` | High | 1,549 | Rust client |
| LangChain Qdrant | `/websites/python_langchain_api_reference_qdrant` | High | 108 | LangChain integration |

### Decision Framework
```
┌─────────────────────────────────────────────────────────────┐
│              Vector Database Selection Tree                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Scale & Requirements?                                       │
│  ├── < 1M vectors + existing PostgreSQL → pgvector          │
│  │                                                          │
│  ├── 1M-100M vectors                                        │
│  │   ├── Complex filtering needed → Qdrant                  │
│  │   ├── GraphQL-native → Weaviate                         │
│  │   └── Zero-ops managed → Pinecone                       │
│  │                                                          │
│  └── > 100M vectors (billion-scale)                         │
│      ├── GPU acceleration → Milvus/Zilliz                  │
│      └── Self-hosted performance → Qdrant (clustered)      │
│                                                              │
│  Hybrid Search (BM25 + Vector)?                             │
│  ├── Yes → Qdrant, Weaviate, or Milvus                     │
│  └── No → Any above                                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Embedding Strategy
```
┌─────────────────────────────────────────────────────────────┐
│                  Embedding Selection                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Quality Priority?                                           │
│  ├── Highest quality → Voyage AI (9.74% better than OpenAI)│
│  ├── Enterprise reliability → OpenAI text-embedding-3-large│
│  └── Self-hosted/Open source                                │
│      ├── Multilingual → BAAI/bge-m3                        │
│      └── English → nomic-embed-text-v1.5                   │
│                                                              │
│  Chunking Strategy:                                          │
│  ├── Default: 512 tokens, 50-100 token overlap              │
│  └── Complex docs: Semantic chunking (embedding-based)      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Init.md Structure
```
managing-vectors/
├── init.md                    # Master plan
├── SKILL.md                   # Main skill file
├── references/
│   ├── vector-db-comparison.md
│   ├── embedding-strategies.md
│   ├── chunking-patterns.md
│   ├── hybrid-search.md
│   └── rag-evaluation.md      # RAGAS metrics
├── scripts/
│   ├── generate_embeddings.py
│   ├── chunk_documents.py
│   └── evaluate_rag.py        # RAGAS evaluation
└── examples/
    ├── qdrant-langchain/
    ├── pgvector-prisma/
    └── hybrid-search-demo/
```

---

## Skill 3: `handling-messages`

### Overview
Implements message queue patterns for async communication, event streaming, and task orchestration.

### Scope
- **Event Streaming**: Apache Kafka, NATS JetStream
- **Message Queues**: RabbitMQ, Redis Streams
- **Task Queues**: Temporal, Celery, BullMQ

### Library Research (Context7)

#### Message Brokers
| Library | Context7 ID | Trust | Snippets | Use Case |
|---------|-------------|-------|----------|----------|
| **Confluent Kafka Python** | `/confluentinc/confluent-kafka-python` | High | 192 | Python Kafka (68.8 score) |
| Confluent Kafka Go | `/confluentinc/confluent-kafka-go` | High | 305 | Go Kafka |
| Confluent Platform | `/websites/confluent_io-platform-current` | High | 18,627 | Full platform |

#### Workflow Orchestration
| Library | Context7 ID | Trust | Snippets | Use Case |
|---------|-------------|-------|----------|----------|
| **Temporal Platform** | `/websites/temporal_io` | High | 3,769 | Workflow orchestration (80.9 score) |
| Temporal Python Samples | `/temporalio/samples-python` | High | 196 | Python examples |
| Temporal Go Samples | `/temporalio/samples-go` | High | 79 | Go examples |

### Decision Framework
```
┌─────────────────────────────────────────────────────────────┐
│              Message Broker Selection Tree                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Pattern & Scale?                                            │
│  ├── Event Streaming (500K+ msg/s)                          │
│  │   └── Apache Kafka (log aggregation, event sourcing)     │
│  │                                                          │
│  ├── Cloud-Native Microservices (200K-400K msg/s)           │
│  │   └── NATS JetStream (sub-ms latency, IoT)              │
│  │                                                          │
│  ├── Complex Routing (50K-100K msg/s)                       │
│  │   └── RabbitMQ (task queues, fan-out patterns)          │
│  │                                                          │
│  └── Simple Queues + Already using Redis                    │
│      └── Redis Streams (100K+ msg/s)                       │
│                                                              │
│  Need Durable Workflows?                                     │
│  └── Yes → Temporal (fault-tolerant, long-running)          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Init.md Structure
```
handling-messages/
├── init.md
├── SKILL.md
├── references/
│   ├── kafka-patterns.md
│   ├── temporal-workflows.md
│   ├── event-sourcing.md
│   └── dead-letter-queues.md
├── scripts/
│   └── kafka_producer_consumer.py
└── examples/
    ├── kafka-python/
    ├── temporal-order-processing/
    └── redis-streams-notifications/
```

---

## Skill 4: `building-apis`

### Overview
Comprehensive API development patterns across REST, GraphQL, gRPC, and tRPC.

### Scope
- **REST**: FastAPI, Axum, Hono, Gin
- **GraphQL**: Strawberry, async-graphql, Pothos
- **gRPC**: Tonic, grpc-go, Connect-Go
- **tRPC**: End-to-end type safety

### Library Research (Context7)

#### REST Frameworks
| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **FastAPI** | `/websites/fastapi_tiangolo` | High | 29,015 | 79.8 | Python REST |
| FastAPI Core | `/fastapi/fastapi` | High | 684 | 87.8 | Core framework |
| **Axum** | `/websites/rs_axum_axum` | High | 7,260 | 77.5 | Rust REST |
| Axum Core | `/tokio-rs/axum` | High | 96 | 76.3 | Tokio-based |
| **Hono** | `/llmstxt/hono_dev_llms_txt` | High | 1,817 | 92.1 | Edge-first |
| Hono Core | `/honojs/hono` | High | 42 | 87.8 | Any JS runtime |

#### Type-Safe APIs
| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **tRPC** | `/trpc/trpc` | High | 900 | 92.7 | TypeScript E2E |
| tRPC Docs | `/websites/trpc_io` | High | 1,068 | 90.2 | Documentation |

### Framework Performance Matrix
```
┌─────────────────────────────────────────────────────────────┐
│                 Framework Performance                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Language    Framework       Req/s      Latency   Bundle    │
│  ──────────────────────────────────────────────────────────│
│  Rust        Actix-web       ~150,000   <1ms      N/A       │
│  Rust        Axum            ~140,000   <1ms      N/A       │
│  Go          Gin             ~100,000+  1-2ms     N/A       │
│  Python      FastAPI         ~40,000    5-10ms    N/A       │
│  TypeScript  Hono (edge)     ~50,000    <5ms cold 14KB      │
│  TypeScript  Express         ~15,000    10-20ms   N/A       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Decision Framework
```
┌─────────────────────────────────────────────────────────────┐
│                   API Framework Selection                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  API Type?                                                   │
│  ├── Public REST API                                         │
│  │   ├── Python → FastAPI (auto-docs, Pydantic v2)          │
│  │   ├── Rust → Axum (Tower ecosystem, Tokio)              │
│  │   ├── Go → Gin (largest ecosystem)                       │
│  │   └── TypeScript → Hono (edge-first, any runtime)        │
│  │                                                          │
│  ├── Internal Microservices                                  │
│  │   └── gRPC (Tonic/Rust, Connect-Go)                      │
│  │                                                          │
│  ├── TypeScript Monorepo (client + server)                  │
│  │   └── tRPC (E2E type safety, no codegen)                │
│  │                                                          │
│  └── Complex Data Graphs                                     │
│      ├── Python → Strawberry (type-hints)                   │
│      ├── Rust → async-graphql                               │
│      └── TypeScript → Pothos (inference-based)              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Init.md Structure
```
building-apis/
├── init.md
├── SKILL.md
├── references/
│   ├── rest-best-practices.md
│   ├── graphql-patterns.md
│   ├── grpc-guide.md
│   ├── trpc-patterns.md
│   ├── openapi-generation.md
│   └── api-versioning.md
├── scripts/
│   ├── generate_openapi.py
│   └── validate_api_schema.py
└── examples/
    ├── fastapi-complete/
    ├── axum-rest/
    ├── hono-edge/
    └── trpc-nextjs/
```

---

## Skill 5: `observing-systems`

### Overview
Implements unified observability with OpenTelemetry, structured logging, and the LGTM stack.

### Scope
- **Telemetry**: OpenTelemetry (traces, metrics, logs)
- **Logging**: structlog, tracing, slog, pino
- **Visualization**: Grafana, Loki, Tempo, Mimir

### Library Research (Context7)

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **OpenTelemetry** | `/websites/opentelemetry_io` | High | 5,888 | 85.9 | Unified observability |
| OTel Python | `/websites/opentelemetry-python_readthedocs_io_en_stable` | High | 926 | - | Python SDK |
| OTel .NET | `/open-telemetry/opentelemetry-dotnet` | High | 202 | 96.9 | .NET SDK |
| OTel JS | `/open-telemetry/opentelemetry-js` | High | 219 | 81.3 | JavaScript SDK |
| OTel Rust | `/open-telemetry/opentelemetry-rust` | High | 55 | 68.2 | Rust SDK |
| OTel Go | `/open-telemetry/opentelemetry-go` | High | 76 | 64.3 | Go SDK |
| Tracing OTel | `/tokio-rs/tracing-opentelemetry` | High | 10 | 86.6 | Rust tracing |

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

### Init.md Structure
```
observing-systems/
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

---

## Skill 6: `securing-applications`

### Overview
Implements modern authentication and authorization patterns including OAuth 2.1, passkeys, and policy engines.

### Scope
- **Authentication**: OAuth 2.1/OIDC, JWT, Passkeys/WebAuthn
- **Authorization**: RBAC, ABAC, ReBAC (Zanzibar)
- **Libraries**: Auth.js, Authlib, Clerk, Keycloak

### Library Research (Context7)

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

### Authorization Engine Selection
```
┌─────────────────────────────────────────────────────────────┐
│              Authorization Engine Selection                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Model Type?                                                 │
│  ├── General Policy (ABAC) → Open Policy Agent (OPA)        │
│  │   └── Best for: Kubernetes, cloud-native                 │
│  │                                                          │
│  ├── Role/Attribute-Based → Casbin                          │
│  │   └── Best for: Embedded, multi-language                 │
│  │                                                          │
│  ├── Relationship-Based (ReBAC/Zanzibar) → SpiceDB          │
│  │   └── Best for: Large-scale, social graphs               │
│  │                                                          │
│  └── API-First Policy → Cerbos                              │
│      └── Best for: Developer-friendly, simple setup         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Init.md Structure
```
securing-applications/
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

---

## Skill 7: `engineering-ai-data`

### Overview
Enables AI/ML data engineering including feature stores, embedding pipelines, RAG systems, and model serving.

### Scope
- **Feature Stores**: Feast, Tecton, Hopsworks
- **Orchestration**: LangChain, LlamaIndex, Haystack
- **Model Serving**: vLLM, TensorRT-LLM, BentoML
- **Evaluation**: RAGAS, promptfoo

### Library Research (Context7)

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **LangChain** | `/websites/langchain_oss_python_langchain` | High | 435 | 79.8 | LLM orchestration |
| LangChain API | `/websites/python_langchain_api_reference` | High | 24,215 | 70.5 | Full API |
| LangChain llms | `/llmstxt/langchain_llms_txt` | High | 3,707 | 75.0 | llms.txt |
| LangChain4j | `/langchain4j/langchain4j` | High | 712 | 82.0 | Java version |
| LangChainGo | `/tmc/langchaingo` | High | 397 | 80.1 | Go version |
| OpenLLMetry | `/traceloop/openllmetry` | High | 97 | 46.7 | LLM observability |

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

### Model Serving Selection
```
┌─────────────────────────────────────────────────────────────┐
│                 Model Serving Selection                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Priority?                                                   │
│  ├── Flexibility + HuggingFace → vLLM                       │
│  │   └── PagedAttention, high throughput                    │
│  │                                                          │
│  ├── Max NVIDIA GPU efficiency → TensorRT-LLM               │
│  │   └── Peak performance, requires compilation             │
│  │                                                          │
│  └── Easy deployment + Kubernetes → BentoML                 │
│      └── Good DX, cloud-native                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Init.md Structure
```
engineering-ai-data/
├── init.md
├── SKILL.md
├── references/
│   ├── rag-architecture.md
│   ├── embedding-strategies.md
│   ├── langchain-patterns.md
│   ├── model-serving.md
│   └── evaluation-metrics.md
├── scripts/
│   ├── evaluate_rag.py      # RAGAS evaluation
│   ├── chunk_documents.py
│   └── benchmark_retrieval.py
└── examples/
    ├── langchain-rag/
    ├── llamaindex-agents/
    └── vllm-serving/
```

---

## Skill 8: `deploying-applications`

### Overview
Covers deployment patterns from Kubernetes to serverless and edge functions.

### Scope
- **Container Orchestration**: Kubernetes, Helm, ArgoCD
- **Serverless**: AWS Lambda, Vercel, Cloudflare Workers
- **Infrastructure as Code**: Pulumi, OpenTofu, SST
- **Edge Functions**: Cloudflare Workers, Deno Deploy

### Library Research (Context7)

| Library | Context7 ID | Trust | Snippets | Score | Use Case |
|---------|-------------|-------|----------|-------|----------|
| **Pulumi** | `/websites/pulumi` | High | 6,034 | 86.4 | IaC (TypeScript) |
| Pulumi Docs | `/pulumi/docs` | High | 9,525 | 94.6 | Documentation |
| Pulumi K8s | `/pulumi/pulumi-kubernetes` | High | 462 | - | Kubernetes |
| Pulumi AWS | `/pulumi/pulumi-aws` | High | 125 | 35.4 | AWS provider |
| Pulumi Examples | `/pulumi/examples` | High | 1,667 | - | Examples |

### Deployment Decision Framework
```
┌─────────────────────────────────────────────────────────────┐
│                Deployment Strategy Selection                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Workload Type?                                              │
│  ├── Complex Microservices                                   │
│  │   └── Kubernetes + ArgoCD/Flux (GitOps)                  │
│  │       ├── Service mesh: Linkerd (5-10% overhead)        │
│  │       └── Helm 4.0 for packaging                         │
│  │                                                          │
│  ├── Variable Traffic / Cost-Sensitive                      │
│  │   └── Serverless                                         │
│  │       ├── Database: Neon, Turso (scale-to-zero)         │
│  │       ├── Compute: Vercel, AWS Lambda                    │
│  │       └── Edge: Cloudflare Workers (<5ms cold start)    │
│  │                                                          │
│  └── Consistent Load / Predictable                          │
│      └── Containers (ECS, Cloud Run, Fly.io)               │
│                                                              │
│  IaC Choice?                                                 │
│  ├── TypeScript-first → Pulumi (Apache 2.0)                │
│  ├── HCL-based → OpenTofu (CNCF, Terraform fork)           │
│  └── Serverless TypeScript → SST v3 (built on Pulumi)      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Init.md Structure
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

---

## Implementation Priority & Timeline

### Phase 1: Critical Foundation (Weeks 1-4)
| Week | Skill | Rationale |
|------|-------|-----------|
| 1-2 | `building-apis` | Every app needs APIs |
| 2-3 | `connecting-databases` | Data persistence foundation |
| 3-4 | `securing-applications` | Security can't be afterthought |

### Phase 2: AI/ML & Observability (Weeks 5-8)
| Week | Skill | Rationale |
|------|-------|-----------|
| 5-6 | `managing-vectors` | RAG is critical for AI apps |
| 6-7 | `engineering-ai-data` | Builds on vectors |
| 7-8 | `observing-systems` | Production monitoring |

### Phase 3: Operations (Weeks 9-12)
| Week | Skill | Rationale |
|------|-------|-----------|
| 9-10 | `handling-messages` | Async patterns |
| 11-12 | `deploying-applications` | Production deployment |

---

## Skill Architecture: Integration with Existing Skills

### Frontend-Backend Integration Points

```
┌──────────────────────────────────────────────────────────────────┐
│                    Full-Stack Skill Integration                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  FRONTEND SKILLS              BACKEND SKILLS                      │
│  ─────────────────            ──────────────────                  │
│                                                                   │
│  forms/                  ←→   building-apis/                      │
│  (validation, inputs)         (API endpoints, validation)        │
│                                                                   │
│  tables/                 ←→   connecting-databases/               │
│  (pagination, sorting)        (queries, cursor pagination)        │
│                                                                   │
│  data-viz/               ←→   connecting-databases/               │
│  (charts, dashboards)         (aggregations, time-series)         │
│                                                                   │
│  ai-chat/                ←→   engineering-ai-data/                │
│  (streaming UI)               (RAG, LLM orchestration)            │
│                                                                   │
│  search-filter/          ←→   managing-vectors/                   │
│  (search UI)                  (semantic search, hybrid)           │
│                                                                   │
│  feedback/               ←→   observing-systems/                  │
│  (error toasts)               (error tracking, logs)              │
│                                                                   │
│  All Frontend Skills     ←→   securing-applications/              │
│                               (auth, protected routes)            │
│                                                                   │
│  assembling-components/  ←→   deploying-applications/             │
│  (production assembly)        (deployment, CI/CD)                 │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Design Token Integration

All backend skills that return data for frontend display must follow token conventions:

```typescript
// API responses include semantic status for frontend styling
interface APIResponse<T> {
  data: T;
  status: 'success' | 'error' | 'warning' | 'info';  // Maps to --color-{status}
  timestamp: string;
}

// Error responses use feedback token categories
interface APIError {
  code: string;
  message: string;
  severity: 'error' | 'warning' | 'info';  // Maps to toast styling
}
```

---

## Marketplace Integration

### New Plugin Groups

```json
{
  "name": "backend-foundation-skills",
  "description": "Core backend infrastructure: databases, APIs, security",
  "skills": [
    "./skills/connecting-databases",
    "./skills/building-apis",
    "./skills/securing-applications"
  ]
},
{
  "name": "backend-ai-skills",
  "description": "AI/ML backend: vectors, RAG, data engineering",
  "skills": [
    "./skills/managing-vectors",
    "./skills/engineering-ai-data"
  ]
},
{
  "name": "backend-ops-skills",
  "description": "Operations: messaging, observability, deployment",
  "skills": [
    "./skills/handling-messages",
    "./skills/observing-systems",
    "./skills/deploying-applications"
  ]
}
```

---

## Recommended Stack Combinations

### Startup MVP (TypeScript Full-Stack)
```
Frontend: forms + tables + dashboards + ai-chat
Backend: building-apis (tRPC) + connecting-databases (Drizzle + Neon) + securing-applications (Auth.js)
Deploy: deploying-applications (Vercel + SST)
```

### Enterprise Microservices (Python/Go)
```
Frontend: data-viz + tables + dashboards + feedback
Backend: building-apis (FastAPI/gRPC) + connecting-databases (SQLAlchemy) + handling-messages (Kafka) + observing-systems (OTel)
Deploy: deploying-applications (Kubernetes + ArgoCD)
```

### AI-Native Application (Python)
```
Frontend: ai-chat + search-filter + data-viz
Backend: engineering-ai-data (LangChain) + managing-vectors (Qdrant) + building-apis (FastAPI) + observing-systems (OpenLLMetry)
Deploy: deploying-applications (vLLM + K8s)
```

### High-Performance API (Rust)
```
Frontend: tables + data-viz + forms
Backend: building-apis (Axum) + connecting-databases (SQLx) + managing-vectors (Qdrant Rust client)
Deploy: deploying-applications (Docker + K8s)
```

---

## Quality Checklist for Backend Skills

### Each init.md Must Include:

- [ ] Clear scope definition
- [ ] Library research with Context7 trust scores
- [ ] Decision framework (ASCII diagram)
- [ ] Multi-language support (Python, TypeScript, Rust, Go where applicable)
- [ ] Integration points with frontend skills
- [ ] Design token considerations
- [ ] Security best practices
- [ ] Performance benchmarks where relevant
- [ ] Example project structure

### Each SKILL.md Must Follow:

- [ ] YAML frontmatter (name, description)
- [ ] Under 500 lines
- [ ] Progressive disclosure to references
- [ ] Working code examples
- [ ] Token-free scripts for automation

---

## Appendix: Context7 Library Summary

### Highest-Scoring Libraries Researched

| Library | Context7 ID | Score | Snippets | Recommended For |
|---------|-------------|-------|----------|-----------------|
| Prisma | `/prisma/prisma` | 96.4 | 115 | TypeScript ORM |
| Drizzle | `/llmstxt/orm_drizzle_team-llms.txt` | 95.4 | 4,037 | Performance ORM |
| tRPC | `/trpc/trpc` | 92.7 | 900 | E2E Type Safety |
| Hono | `/llmstxt/hono_dev_llms_txt` | 92.1 | 1,817 | Edge-first APIs |
| NextAuth | `/nextauthjs/next-auth` | 91.8 | 749 | Auth |
| Zod | `/colinhacks/zod` | 90.4 | 542 | Validation |
| tRPC Docs | `/websites/trpc_io` | 90.2 | 1,068 | Documentation |
| Pulumi Docs | `/pulumi/docs` | 94.6 | 9,525 | IaC |
| Valkey | `/valkey-io/valkey-doc` | 87.5 | 1,199 | Redis Alternative |
| FastAPI | `/fastapi/fastapi` | 87.8 | 684 | Python REST |
| Auth.js | `/websites/authjs_dev` | 87.4 | 2,480 | Multi-framework Auth |
| OpenTelemetry | `/websites/opentelemetry_io` | 85.9 | 5,888 | Observability |
| Qdrant | `/llmstxt/qdrant_tech_llms-full_txt` | 83.1 | 10,154 | Vector DB |
| Temporal | `/websites/temporal_io` | 80.9 | 3,769 | Workflows |

---

## Next Steps

1. **Review this plan** - Ensure alignment with project goals
2. **Prioritize skills** - Confirm Phase 1 skills
3. **Generate init.md files** - Create detailed master plans for each skill
4. **Update skillchain.md** - Add backend skill keywords and workflows
5. **Update marketplace.json** - Add new plugin groups
6. **Begin implementation** - Start with `building-apis` skill

---

*Document generated: December 2025*
*Research sources: Context7, FULL_STACK_SKILLS_source.md*
*Status: Ready for review*
