---
sidebar_position: 1
title: Skills Overview
description: 29 production-ready Claude Skills for full-stack development
---

# Skills Overview

AI Design Components provides **29 production-ready Claude Skills** organized into frontend and backend categories. Each skill has complete SKILL.md implementations with progressive disclosure, code examples, and multi-language support.

## What are Claude Skills?

Skills are modular packages that extend Claude's capabilities through specialized knowledge and workflows. They use **progressive disclosure** - only metadata is pre-loaded, full content loads when relevant.

**Key Features:**
- **Modular design** - Use individually or chain together
- **Progressive disclosure** - Efficient context management
- **Multi-language support** - Backend skills support Python, TypeScript, Rust, Go
- **Production-ready** - Complete implementations with examples
- **Skillchain compatible** - Orchestrated automatically via `/skillchain`

## Frontend Skills (15)

### Foundation (1)

| Skill | Description | Key Features |
|-------|-------------|--------------|
| **theming-components** | Design tokens, colors, dark mode, brand theming | 7 token categories, theme switching, accessible colors |

### Structure (3)

| Skill | Description | Key Features |
|-------|-------------|--------------|
| **designing-layouts** | Grid systems, responsive design, sidebars | CSS Grid, Flexbox, responsive breakpoints |
| **implementing-navigation** | Menus, tabs, breadcrumbs, routing | Sidebar, top nav, tabs, accessibility |
| **displaying-timelines** | Activity feeds, history, event logs | Vertical/horizontal, timestamps, icons |

### Data Display (3)

| Skill | Description | Key Features |
|-------|-------------|--------------|
| **visualizing-data** | Charts, graphs, plots (24+ types) | Bar, line, pie, scatter, heatmap, treemap |
| **building-tables** | Data grids, sorting, pagination | Filtering, sorting, virtual scrolling |
| **creating-dashboards** | KPI cards, widgets, analytics | Grid layouts, responsive, real-time |

### User Input (2)

| Skill | Description | Key Features |
|-------|-------------|--------------|
| **building-forms** | Forms, validation, inputs (50+ types) | React Hook Form, Zod, accessibility |
| **implementing-search-filter** | Search bars, faceted filters | Real-time, autocomplete, multi-facet |

### Interaction (3)

| Skill | Description | Key Features |
|-------|-------------|--------------|
| **building-ai-chat** | Chat UI, streaming, AI interfaces | Message history, streaming, multi-modal |
| **implementing-drag-drop** | Kanban, sortable lists, reordering | dnd-kit, touch support, accessibility |
| **providing-feedback** | Toasts, alerts, loading states | Notifications, skeleton screens, progress |

### Content (2)

| Skill | Description | Key Features |
|-------|-------------|--------------|
| **managing-media** | File upload, galleries, video/audio | Drag-and-drop, previews, cloud storage |
| **guiding-users** | Onboarding, tutorials, tooltips | Product tours, hints, wizards |

### Assembly (1)

| Skill | Description | Key Features |
|-------|-------------|--------------|
| **assembling-components** | Final integration, validation | Token validation, production-ready output |

## Backend Skills (14)

### Data Ingestion (1)

| Skill | Description | Languages |
|-------|-------------|-----------|
| **ingesting-data** | ETL, CSV, S3, APIs, CDC, dlt pipelines | Python, TypeScript |

### Databases (5)

| Skill | Description | Languages |
|-------|-------------|-----------|
| **databases-relational** | PostgreSQL, MySQL, SQLite, ORMs | Python, TypeScript, Rust, Go |
| **databases-vector** | Qdrant, pgvector, Pinecone, RAG | Python, TypeScript |
| **databases-timeseries** | ClickHouse, TimescaleDB, InfluxDB | Python, TypeScript, Go |
| **databases-document** | MongoDB, Firestore, DynamoDB | Python, TypeScript, Go |
| **databases-graph** | Neo4j, memgraph, Cypher | Python, TypeScript |

### APIs & Messaging (3)

| Skill | Description | Languages |
|-------|-------------|-----------|
| **api-patterns** | REST, GraphQL, gRPC, tRPC | Python, TypeScript, Rust |
| **message-queues** | Kafka, RabbitMQ, NATS, Temporal | Python, TypeScript, Go |
| **realtime-sync** | WebSockets, SSE, Y.js, presence | TypeScript, Python |

### Platform (3)

| Skill | Description | Languages |
|-------|-------------|-----------|
| **auth-security** | OAuth 2.1, passkeys, RBAC, JWT | Python, TypeScript, Rust |
| **observability** | OpenTelemetry, LGTM stack, tracing | Python, TypeScript, Go, Rust |
| **deploying-applications** | Kubernetes, serverless, edge | Python, TypeScript, Go, Rust |

### AI/ML (2)

| Skill | Description | Languages |
|-------|-------------|-----------|
| **ai-data-engineering** | RAG pipelines, embeddings, chunking | Python, TypeScript |
| **model-serving** | vLLM, BentoML, Ollama, inference | Python |

## Multi-Language Support

All backend skills provide idiomatic patterns for multiple languages:

### Python
- **Framework:** FastAPI, SQLAlchemy, Pydantic
- **Style:** Type hints, async/await, modern tooling
- **Package Manager:** uv, Poetry
- **Use Case:** ML/AI, data engineering, rapid prototyping

### TypeScript
- **Framework:** Express, Hono, Prisma, Drizzle
- **Style:** Strict types, Zod validation
- **Runtime:** Node.js, Bun, Deno
- **Use Case:** Full-stack, serverless, edge computing

### Rust
- **Framework:** Axum, SeaORM, Serde
- **Style:** Memory-safe, zero-cost abstractions
- **Build:** Cargo
- **Use Case:** High-performance, systems programming

### Go
- **Framework:** Gin, GORM, Chi
- **Style:** Idiomatic Go, goroutines
- **Build:** Go modules
- **Use Case:** Microservices, cloud-native, CLI tools

## Skill Invocation

### Individual Skills

Load skills directly using the Skill tool:

```
Use the ui-foundation-skills:theming-components skill
Use the backend-data-skills:databases-relational skill
```

### Skillchain (Recommended)

Use the `/skillchain` command for guided workflows:

```bash
/skillchain dashboard with charts        # Auto-selects 7 skills
/skillchain REST API with postgres       # Auto-selects 5 skills
/skillchain RAG pipeline                 # Auto-selects 6 skills
```

See [Skillchain documentation](../skillchain/overview.md) for details.

## Skill Structure

Each skill follows Anthropic's best practices:

```
skills/[skill-name]/
├── SKILL.md                # Main skill file (< 500 lines)
├── init.md                 # Master plan and research
├── references/             # Detailed documentation
│   ├── patterns.md
│   ├── examples.md
│   └── library-guide.md
├── scripts/                # Utility scripts (token-free execution)
│   └── helper.py
├── examples/               # Code examples
│   ├── basic.tsx
│   └── advanced.tsx
└── assets/                 # Templates, schemas
    └── template.json
```

**Progressive Disclosure:**
1. **Level 1:** Metadata (name + description) - Always in context
2. **Level 2:** SKILL.md body - Loaded when skill triggers
3. **Level 3:** References, scripts, examples - Loaded on-demand

## Getting Started

### Option 1: Use Skillchain (Recommended)

```bash
# Install skillchain
./commands/install-skillchain.sh --global

# Start Claude Code
claude

# Use skillchain
/skillchain dashboard with charts
```

See [Skillchain documentation](../skillchain/overview.md).

### Option 2: Use Skills Directly

```
# In Claude Code conversation
Use the ui-foundation-skills:theming-components skill
Then use the ui-data-skills:visualizing-data skill
```

### Option 3: Explore Individual Skills

Browse skill documentation:
- [Frontend Skills](./frontend/)
- [Backend Skills](./backend/)

## Next Steps

- [Install Skillchain](../skillchain/installation.md) for guided workflows
- [Explore Frontend Skills](./frontend/) for UI components
- [Explore Backend Skills](./backend/) for API/database patterns
- [View Skillchain Blueprints](../skillchain/blueprints.md) for common patterns
