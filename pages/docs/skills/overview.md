---
sidebar_position: 1
title: Skills Overview
description: 76 production-ready Claude Skills for full-stack development
---

# Skills Overview

AI Design Components provides **76 production-ready Claude Skills** organized into 10 comprehensive categories. Each skill has complete SKILL.md implementations with progressive disclosure, code examples, and multi-language support.

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

## DevOps Skills (6)

| Skill | Description | Key Features |
|-------|-------------|--------------|
| **testing-strategies** | Unit, integration, E2E testing patterns | Test frameworks, coverage, best practices |
| **building-ci-pipelines** | CI/CD pipelines, GitHub Actions, automation | Pipeline design, testing, deployment |
| **implementing-gitops** | GitOps workflows, ArgoCD, Flux | Git-based deployments, declarative config |
| **platform-engineering** | Internal developer platforms, self-service | Platform design, developer experience |
| **managing-incidents** | Incident response, postmortems, on-call | Runbooks, escalation, retrospectives |
| **writing-dockerfiles** | Container images, multi-stage builds | Optimization, security, best practices |

## Infrastructure Skills (12)

| Skill | Description | Key Features |
|-------|-------------|--------------|
| **operating-kubernetes** | K8s deployments, operators, management | Pods, services, ingress, scaling |
| **writing-infrastructure-code** | Terraform, Pulumi, CloudFormation | IaC patterns, modules, state management |
| **administering-linux** | Linux server management, systemd | Package management, security, monitoring |
| **architecting-networks** | Network design, VPC, subnets | Routing, firewalls, load balancing |
| **load-balancing-patterns** | Load balancers, traffic distribution | Layer 4/7, health checks, algorithms |
| **planning-disaster-recovery** | Backup, recovery, business continuity | RTO/RPO, failover, testing |
| **configuring-nginx** | Nginx configuration, reverse proxy | SSL, caching, performance tuning |
| **shell-scripting** | Bash scripting, automation | Best practices, error handling, portability |
| **managing-dns** | DNS configuration, Route53, zones | Records, routing policies, DNSSEC |
| **implementing-service-mesh** | Istio, Linkerd, service mesh patterns | mTLS, observability, traffic management |
| **managing-configuration** | Configuration management, secrets | Environment variables, config files |
| **designing-distributed-systems** | Distributed system patterns, scalability | Consistency, availability, partitioning |

## Security Skills (7)

| Skill | Description | Key Features |
|-------|-------------|--------------|
| **architecting-security** | Security architecture, zero trust | Defense in depth, least privilege |
| **implementing-compliance** | Compliance frameworks, SOC 2, GDPR | Controls, audits, documentation |
| **managing-vulnerabilities** | Vulnerability scanning, patching | CVE management, remediation |
| **implementing-tls** | TLS/SSL configuration, certificates | mTLS, certificate management |
| **configuring-firewalls** | Firewall rules, network security | iptables, cloud firewalls, segmentation |
| **siem-logging** | Security information and event management | Log aggregation, alerts, correlation |
| **security-hardening** | System hardening, CIS benchmarks | OS hardening, secure configuration |

## Developer Productivity Skills (7)

| Skill | Description | Key Features |
|-------|-------------|--------------|
| **designing-apis** | API design, REST, GraphQL | Design principles, versioning, documentation |
| **building-clis** | Command-line tools, CLI frameworks | Argument parsing, output formatting |
| **designing-sdks** | SDK design, client libraries | API wrapping, versioning, examples |
| **generating-documentation** | Auto-generated docs, API references | Docusaurus, OpenAPI, JSDoc |
| **debugging-techniques** | Debugging strategies, tools | Breakpoints, logging, profiling |
| **managing-git-workflows** | Git workflows, branching strategies | Feature branches, releases, conflicts |
| **writing-github-actions** | GitHub Actions workflows, CI/CD | Workflows, runners, marketplace actions |

## Data Engineering Skills (6)

| Skill | Description | Key Features |
|-------|-------------|--------------|
| **architecting-data** | Data architecture, warehouses, lakes | Schema design, modeling, partitioning |
| **streaming-data** | Stream processing, Kafka, event-driven | Real-time processing, windowing |
| **transforming-data** | ETL/ELT, data pipelines, dbt | Data transformation, quality, lineage |
| **optimizing-sql** | SQL optimization, query performance | Indexes, execution plans, tuning |
| **secret-management** | Secrets management, Vault, rotation | Secret storage, rotation, access control |
| **performance-engineering** | Performance optimization, profiling | Benchmarking, bottlenecks, scaling |

## AI/ML Skills (4)

| Skill | Description | Key Features |
|-------|-------------|--------------|
| **implementing-mlops** | MLOps pipelines, model deployment | Training, versioning, monitoring |
| **prompt-engineering** | Prompt design, techniques, optimization | Chain-of-thought, few-shot, evaluation |
| **evaluating-llms** | LLM evaluation, benchmarks, metrics | Quality assessment, A/B testing |
| **embedding-optimization** | Embedding models, vector search | Chunking, retrieval, optimization |

## Cloud Skills (3)

| Skill | Description | Key Features |
|-------|-------------|--------------|
| **deploying-on-aws** | AWS deployments, services, best practices | EC2, Lambda, RDS, S3, CloudFront |
| **deploying-on-gcp** | GCP deployments, services, best practices | Compute Engine, Cloud Run, BigQuery |
| **deploying-on-azure** | Azure deployments, services, best practices | VMs, App Service, Cosmos DB |

## FinOps Skills (2)

| Skill | Description | Key Features |
|-------|-------------|--------------|
| **optimizing-costs** | Cost optimization, budgets, forecasting | Cost allocation, savings plans, reserved instances |
| **resource-tagging** | Resource tagging, cost allocation | Tag strategies, compliance, reporting |

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

Browse skill documentation by category:
- **Frontend Skills (15):** [Theming](./frontend/theming-components), [Forms](./frontend/building-forms), [Charts](./frontend/visualizing-data), [AI Chat](./frontend/building-ai-chat)
- **Backend Skills (14):** [API Patterns](./backend/implementing-api-patterns), [Databases](./backend/using-relational-databases), [Auth](./backend/securing-authentication), [Observability](./backend/implementing-observability)
- **DevOps Skills (6):** [Testing](./devops/testing-strategies), [CI/CD](./devops/building-ci-pipelines), [GitOps](./devops/implementing-gitops), [Platform Engineering](./devops/platform-engineering)
- **Infrastructure Skills (12):** [Kubernetes](./infrastructure/operating-kubernetes), [IaC](./infrastructure/writing-infrastructure-code), [Linux](./infrastructure/administering-linux), [Networking](./infrastructure/architecting-networks)
- **Security Skills (7):** [Security Architecture](./security/architecting-security), [Compliance](./security/implementing-compliance), [Vulnerabilities](./security/managing-vulnerabilities), [TLS](./security/implementing-tls)
- **Developer Productivity (7):** [API Design](./developer-productivity/designing-apis), [CLIs](./developer-productivity/building-clis), [SDKs](./developer-productivity/designing-sdks), [Documentation](./developer-productivity/generating-documentation)
- **Data Engineering (6):** [Data Architecture](./data-engineering/architecting-data), [Streaming](./data-engineering/streaming-data), [SQL](./data-engineering/optimizing-sql), [Performance](./data-engineering/performance-engineering)
- **AI/ML Skills (4):** [MLOps](./ai-ml/implementing-mlops), [Prompt Engineering](./ai-ml/prompt-engineering), [LLM Evaluation](./ai-ml/evaluating-llms), [Embeddings](./ai-ml/embedding-optimization)
- **Cloud Skills (3):** [AWS](./cloud/deploying-on-aws), [GCP](./cloud/deploying-on-gcp), [Azure](./cloud/deploying-on-azure)
- **FinOps Skills (2):** [Cost Optimization](./finops/optimizing-costs), [Resource Tagging](./finops/resource-tagging)

## Next Steps

- [Install Skillchain](../skillchain/installation.md) for guided workflows
- Explore Popular Skills:
  - **Frontend:** [Theming](./frontend/theming-components), [Forms](./frontend/building-forms), [Data Viz](./frontend/visualizing-data), [AI Chat](./frontend/building-ai-chat)
  - **Backend:** [APIs](./backend/implementing-api-patterns), [Databases](./backend/using-relational-databases), [Auth](./backend/securing-authentication)
  - **DevOps:** [Testing](./devops/testing-strategies), [CI/CD](./devops/building-ci-pipelines), [Docker](./devops/writing-dockerfiles)
  - **Infrastructure:** [Kubernetes](./infrastructure/operating-kubernetes), [IaC](./infrastructure/writing-infrastructure-code), [Nginx](./infrastructure/configuring-nginx)
  - **Security:** [Security Architecture](./security/architecting-security), [Compliance](./security/implementing-compliance), [TLS](./security/implementing-tls)
- [View Skillchain Blueprints](../skillchain/blueprints.md) for common patterns
