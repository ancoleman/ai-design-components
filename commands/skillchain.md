---
description: "Start a guided skill chaining workflow to build full-stack applications. 29 skills covering frontend, backend, databases, and AI. Usage: /skillchain [goal] or /skillchain help"
allowed-tools: Skill, Read, Glob, Bash, Write
argument-hint: "[goal] e.g., 'dashboard with charts', 'API with postgres', 'RAG pipeline' — or 'help' for usage guide"
---

# Skill Chain Orchestrator

**Input:** $ARGUMENTS

---

## If "$ARGUMENTS" is "help" or empty, show this guide:

```
╔══════════════════════════════════════════════════════════════════╗
║                    SKILL CHAIN HELP GUIDE                        ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  USAGE: /skillchain [your goal]                                  ║
║                                                                  ║
║  FRONTEND EXAMPLES:                                              ║
║    /skillchain sales dashboard with revenue charts               ║
║    /skillchain login form with validation                        ║
║    /skillchain data table with search and filters                ║
║    /skillchain AI chat interface                                 ║
║                                                                  ║
║  BACKEND EXAMPLES:                                               ║
║    /skillchain REST API with PostgreSQL                          ║
║    /skillchain import CSV data to database                       ║
║    /skillchain RAG pipeline with vector search                   ║
║    /skillchain deploy to Kubernetes with monitoring              ║
║                                                                  ║
║  FULL-STACK EXAMPLES:                                            ║
║    /skillchain dashboard with charts and postgres backend        ║
║    /skillchain login form with OAuth authentication              ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  FRONTEND SKILLS (15)                                            ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  FOUNDATION:                                                     ║
║    theming-components    → Colors, tokens, dark mode, branding   ║
║                                                                  ║
║  DATA DISPLAY:                                                   ║
║    visualizing-data      → Charts, graphs, data viz (24+ types)  ║
║    building-tables       → Data grids, sorting, pagination       ║
║    creating-dashboards   → Dashboard layouts, KPI cards          ║
║                                                                  ║
║  USER INPUT:                                                     ║
║    building-forms        → Forms, validation, inputs (50+ types) ║
║    implementing-search-filter → Search bars, faceted filters     ║
║                                                                  ║
║  INTERACTION:                                                    ║
║    building-ai-chat      → Chat UI, streaming, AI interfaces     ║
║    implementing-drag-drop → Kanban, sortable lists, reordering   ║
║    providing-feedback    → Toasts, alerts, loading states        ║
║                                                                  ║
║  STRUCTURE:                                                      ║
║    implementing-navigation → Menus, tabs, breadcrumbs, routing   ║
║    designing-layouts     → Grids, responsive, sidebars           ║
║    displaying-timelines  → Activity feeds, history, events       ║
║                                                                  ║
║  CONTENT:                                                        ║
║    managing-media        → File upload, galleries, video/audio   ║
║    guiding-users         → Onboarding, tutorials, tooltips       ║
║                                                                  ║
║  ASSEMBLY:                                                       ║
║    assembling-components → Wires components, validates tokens    ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  BACKEND SKILLS (14)                                             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  DATA INGESTION:                                                 ║
║    ingesting-data        → ETL, S3, APIs, CDC, dlt pipelines     ║
║                                                                  ║
║  DATABASES:                                                      ║
║    databases-relational  → PostgreSQL, MySQL, SQLite, ORMs       ║
║    databases-vector      → Qdrant, pgvector, Pinecone, RAG       ║
║    databases-timeseries  → ClickHouse, TimescaleDB, InfluxDB     ║
║    databases-document    → MongoDB, Firestore, DynamoDB          ║
║    databases-graph       → Neo4j, memgraph, Cypher               ║
║                                                                  ║
║  APIS & MESSAGING:                                               ║
║    api-patterns          → REST, GraphQL, gRPC, tRPC             ║
║    message-queues        → Kafka, RabbitMQ, NATS, Temporal       ║
║    realtime-sync         → WebSockets, SSE, Y.js, presence       ║
║                                                                  ║
║  PLATFORM:                                                       ║
║    auth-security         → OAuth 2.1, passkeys, RBAC, JWT        ║
║    observability         → OpenTelemetry, LGTM stack, tracing    ║
║    deploying-applications → Kubernetes, serverless, edge         ║
║                                                                  ║
║  AI/ML:                                                          ║
║    ai-data-engineering   → RAG pipelines, embeddings, chunking   ║
║    model-serving         → vLLM, BentoML, Ollama, inference      ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  WORKFLOW COMMANDS (use during skill chain)                      ║
╠══════════════════════════════════════════════════════════════════╣
║    "back"     → Return to previous step                          ║
║    "skip"     → Use defaults, move to next step                  ║
║    "status"   → Show current progress                            ║
║    "done"     → Finish early with current selections             ║
║    "restart"  → Start over from beginning                        ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  HOW IT WORKS                                                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  1. You describe what you want to build                          ║
║  2. I identify required skills from your keywords                ║
║  3. I invoke each skill in the correct order                     ║
║  4. After each skill, I ask you questions based on its options   ║
║  5. Your answers shape the final output                          ║
║  6. All skills chain together for consistent components          ║
║                                                                  ║
║  SKILL ORDER: theming → structure → content → interaction        ║
║               → backend → assembling-components (FINAL STEP)     ║
║                                                                  ║
║  TOTAL SKILLS: 29 (15 frontend + 14 backend)                     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

If showing help, then STOP and wait for user to run `/skillchain [goal]`.

---

## Keyword → Skill Mapping

Parse "$ARGUMENTS" for these keywords to determine which skills to invoke:

### Primary Keywords

| Keywords in Goal | Skills to Invoke (in order) |
|------------------|----------------------------|
| dashboard, analytics, metrics, admin, KPI, overview | theming → designing-layouts → creating-dashboards → visualizing-data → building-tables → building-forms → providing-feedback → assembling-components |
| chart, graph, visualize, plot, bar, line, pie | theming → visualizing-data |
| table, grid, records, data grid, list, rows | theming → building-tables |
| form, login, signup, register, input, validation | theming → building-forms → providing-feedback |
| search, filter, find, query, faceted | theming → implementing-search-filter |
| chat, AI, assistant, chatbot, conversation, streaming | theming → building-ai-chat → building-forms |
| upload, file, image, gallery, media, video, audio | theming → managing-media |
| drag, drop, sortable, kanban, reorder, move | theming → implementing-drag-drop |
| navigation, menu, nav, tabs, sidebar, routing, breadcrumb | theming → implementing-navigation → designing-layouts |
| timeline, activity, history, feed, events, log | theming → displaying-timelines |
| onboarding, tutorial, guide, tour, tooltip, help, wizard | theming → guiding-users |
| layout, grid, columns, responsive, structure | theming → designing-layouts |
| notification, toast, alert, loading, spinner, feedback | theming → providing-feedback → assembling-components |
| theme, colors, brand, dark mode, styling, tokens | theming |
| assemble, wire, integrate, scaffold, validate tokens, production | assembling-components |

### Backend Keywords (v0.3.0)

| Keywords in Goal | Skills to Invoke (in order) |
|------------------|----------------------------|
| database, sql, postgres, mysql, sqlite, orm, prisma, drizzle, sqlalchemy | api-patterns → databases-relational |
| vector, embedding, rag, semantic search, qdrant, pgvector, similarity | building-ai-chat → databases-vector → ai-data-engineering |
| timeseries, metrics, prometheus, grafana, clickhouse, influxdb | creating-dashboards → databases-timeseries → observability |
| nosql, mongo, document, firestore, dynamodb, collection | api-patterns → databases-document |
| graph, neo4j, cypher, relationships, nodes, edges | databases-graph |
| api, rest, graphql, grpc, trpc, fastapi, hono, axum | api-patterns |
| kafka, queue, message, event, rabbitmq, nats, temporal, celery | api-patterns → message-queues |
| websocket, realtime, streaming, sse, collaborative, yjs, presence | api-patterns → realtime-sync |
| deploy, kubernetes, k8s, helm, serverless, lambda, vercel, cloudflare | assembling-components → deploying-applications |
| auth, login, security, jwt, oauth, passkeys, webauthn, authentication | api-patterns → auth-security |
| monitoring, observability, logs, traces, opentelemetry, otel, lgtm | observability |
| llm, model, serving, vllm, inference, bentoml, mlops | ai-data-engineering → model-serving |
| ingest, import, etl, csv, s3, bucket, migration, cdc, extract, load, dlt | ingesting-data → [target-database-skill] |

### Compound Detection

If multiple keywords match, combine the skill chains. Common combinations:

**Frontend Combinations:**
- "dashboard with charts and filters" → theming → layouts → dashboards → visualizing-data → forms
- "table with search" → theming → tables → search-filter
- "form with notifications" → theming → forms → feedback
- "chat with file upload" → theming → ai-chat → media → forms
- "kanban with drag drop" → theming → drag-drop → tables

**Backend Combinations:**
- "REST API with postgres and auth" → api-patterns → databases-relational → auth-security
- "RAG pipeline with embeddings" → ingesting-data → ai-data-engineering → databases-vector
- "real-time chat with websockets" → api-patterns → realtime-sync → message-queues
- "microservices with kafka" → api-patterns → message-queues → observability → deploying-applications
- "import CSV to postgres" → ingesting-data → databases-relational

**Full-Stack Combinations:**
- "dashboard with postgres backend" → theming → dashboards → visualizing-data → api-patterns → databases-relational
- "login form with OAuth" → theming → forms → api-patterns → auth-security
- "chat app with real-time sync" → theming → ai-chat → api-patterns → realtime-sync → databases-document
- "analytics dashboard with timeseries" → theming → dashboards → visualizing-data → databases-timeseries → observability

---

## Skill Invocation Reference

**CRITICAL: You must actually invoke each skill using the Skill tool.**

### Plugin Groups and Skill Names

#### Frontend Skills

```
ui-foundation-skills:
  - theming-components

ui-data-skills:
  - visualizing-data
  - building-tables
  - creating-dashboards

ui-input-skills:
  - building-forms
  - implementing-search-filter

ui-interaction-skills:
  - building-ai-chat
  - implementing-drag-drop
  - providing-feedback

ui-structure-skills:
  - implementing-navigation
  - designing-layouts
  - displaying-timelines

ui-content-skills:
  - managing-media
  - guiding-users

ui-assembly-skills:
  - assembling-components
```

#### Backend Skills

```
backend-data-skills:
  - ingesting-data
  - databases-relational
  - databases-vector
  - databases-timeseries
  - databases-document
  - databases-graph

backend-api-skills:
  - api-patterns
  - message-queues
  - realtime-sync

backend-platform-skills:
  - auth-security
  - observability
  - deploying-applications

backend-ai-skills:
  - ai-data-engineering
  - model-serving
```

### Invocation Syntax

To invoke a skill, use:
```
Skill({ skill: "ui-data-skills:visualizing-data" })
```

#### Frontend Skill Mappings

- theming-components → `ui-foundation-skills:theming-components`
- visualizing-data → `ui-data-skills:visualizing-data`
- building-tables → `ui-data-skills:building-tables`
- creating-dashboards → `ui-data-skills:creating-dashboards`
- building-forms → `ui-input-skills:building-forms`
- implementing-search-filter → `ui-input-skills:implementing-search-filter`
- building-ai-chat → `ui-interaction-skills:building-ai-chat`
- implementing-drag-drop → `ui-interaction-skills:implementing-drag-drop`
- providing-feedback → `ui-interaction-skills:providing-feedback`
- implementing-navigation → `ui-structure-skills:implementing-navigation`
- designing-layouts → `ui-structure-skills:designing-layouts`
- displaying-timelines → `ui-structure-skills:displaying-timelines`
- managing-media → `ui-content-skills:managing-media`
- guiding-users → `ui-content-skills:guiding-users`
- assembling-components → `ui-assembly-skills:assembling-components`

#### Backend Skill Mappings

- ingesting-data → `backend-data-skills:ingesting-data`
- databases-relational → `backend-data-skills:databases-relational`
- databases-vector → `backend-data-skills:databases-vector`
- databases-timeseries → `backend-data-skills:databases-timeseries`
- databases-document → `backend-data-skills:databases-document`
- databases-graph → `backend-data-skills:databases-graph`
- api-patterns → `backend-api-skills:api-patterns`
- message-queues → `backend-api-skills:message-queues`
- realtime-sync → `backend-api-skills:realtime-sync`
- auth-security → `backend-platform-skills:auth-security`
- observability → `backend-platform-skills:observability`
- deploying-applications → `backend-platform-skills:deploying-applications`
- ai-data-engineering → `backend-ai-skills:ai-data-engineering`
- model-serving → `backend-ai-skills:model-serving`

---

## Execution Flow

### Step 1: Parse and Announce

After parsing "$ARGUMENTS", tell the user:

```
🔗 Skill Chain Initiated

Goal: [interpreted from $ARGUMENTS]

I'll guide you through these skills:
1. [skill] → [purpose]
2. [skill] → [purpose]
...

Starting with theming to establish your design foundation.
```

### Step 2: Invoke theming-components (ALWAYS FIRST)

```
Skill({ skill: "ui-foundation-skills:theming-components" })
```

After it loads, ask:
> **🎨 Theming Configuration**
>
> Before building components, let's set up your design tokens:
>
> 1. **Brand Color:** What's your primary color?
>    - Hex code (e.g., "#3B82F6")
>    - Or describe (e.g., "blue", "orange", "company brand")
>    - Or "default" for standard blue
>
> 2. **Theme Modes:**
>    - A) Light only
>    - B) Light + Dark
>    - C) Light + Dark + High Contrast (accessibility)
>
> Reply with: `[color], [A/B/C]` (e.g., "#FF6B35, B")

### Step 3: Continue Through Skill Chain

For each subsequent skill:

1. **Invoke the skill** using the Skill tool
2. **Wait for skill content to load** into context
3. **Use the skill's decision trees** to ask relevant questions
4. **Apply user's answers** to configure the output
5. **Summarize** what was configured
6. **Move to next skill** in the chain

### Step 4: Questions Per Skill

**After designing-layouts:**
> **📐 Layout Configuration**
>
> Choose your layout structure:
> - A) Header + grid of cards (dashboard style)
> - B) Sidebar + main content (app style)
> - C) Full-width sections (landing page style)
> - D) Custom (describe what you need)
>
> Responsive? (Y/N)

**After visualizing-data:**
> **📊 Chart Configuration**
>
> Based on your goal, what data are you visualizing?
> - Describe your metrics (revenue, users, etc.)
> - Time period? (daily, monthly, yearly)
> - Comparison type? (trends, categories, composition)
>
> I'll recommend the best chart type.

**After building-tables:**
> **📋 Table Configuration**
>
> - What columns do you need?
> - Features: sortable? pagination? row selection?
> - Approximate row count? (<100, 100-1000, 1000+)

**After building-forms:**
> **📝 Form Configuration**
>
> - What inputs do you need? (text, email, date, select, etc.)
> - Validation requirements?
> - Single page or multi-step wizard?

**After implementing-search-filter:**
> **🔍 Search/Filter Configuration**
>
> - Search type: text search, autocomplete, or faceted?
> - Filter types: dropdowns, date range, checkboxes?
> - Auto-apply or manual apply button?

**After building-ai-chat:**
> **💬 AI Chat Configuration**
>
> - Streaming responses? (Y/N)
> - File/image upload in chat?
> - Message history display style?

**After providing-feedback:**
> **🔔 Feedback Configuration**
>
> - Loading states: spinner, skeleton, or progress bar?
> - Notifications: toast (auto-dismiss) or alert (manual)?
> - Error display: inline or modal?

### Step 4b: Backend Skill Questions

**After ingesting-data:**
> **📥 Data Ingestion Configuration**
>
> - Source type:
>   - A) Cloud storage (S3, GCS, Azure Blob)
>   - B) Files (CSV, JSON, Parquet)
>   - C) API feeds (REST, webhooks)
>   - D) Database migration (CDC, replication)
>   - E) Streaming (Kafka, Kinesis)
>
> - Target database: PostgreSQL, MongoDB, or other?
> - Incremental or full refresh?
> - Schedule: real-time, hourly, daily?

**After databases-relational:**
> **🗄️ Relational Database Configuration**
>
> - Database:
>   - A) PostgreSQL (recommended)
>   - B) MySQL
>   - C) SQLite (development/embedded)
>
> - ORM preference:
>   - A) Prisma (TypeScript)
>   - B) Drizzle (TypeScript)
>   - C) SQLAlchemy (Python)
>   - D) sqlx (Rust)
>   - E) Raw SQL
>
> - Connection pooling? (Y/N)
> - Migrations strategy: manual or auto-generate?

**After databases-vector:**
> **🔮 Vector Database Configuration**
>
> - Primary use case:
>   - A) RAG/semantic search
>   - B) Recommendation engine
>   - C) Image similarity
>   - D) Hybrid search (vector + keyword)
>
> - Vector store:
>   - A) Qdrant (recommended, full-featured)
>   - B) pgvector (PostgreSQL extension)
>   - C) Pinecone (managed service)
>   - D) Weaviate
>
> - Embedding model: OpenAI, Cohere, or local?
> - Expected vector count: <100k, 100k-1M, 1M+?

**After databases-timeseries:**
> **📈 Time-Series Database Configuration**
>
> - Use case:
>   - A) Metrics/monitoring
>   - B) IoT sensor data
>   - C) Financial data
>   - D) Log aggregation
>
> - Database:
>   - A) ClickHouse (analytics, fast aggregations)
>   - B) TimescaleDB (PostgreSQL extension)
>   - C) InfluxDB (IoT/metrics)
>
> - Retention policy: days, months, years?
> - Expected write rate: low, medium, high?

**After databases-document:**
> **📄 Document Database Configuration**
>
> - Database:
>   - A) MongoDB (self-hosted/Atlas)
>   - B) Firestore (serverless, real-time)
>   - C) DynamoDB (AWS, auto-scaling)
>
> - Data model: embedded or referenced documents?
> - Indexes needed?
> - Real-time subscriptions? (Y/N)

**After databases-graph:**
> **🕸️ Graph Database Configuration**
>
> - Database:
>   - A) Neo4j (full-featured, Cypher query language)
>   - B) Memgraph (in-memory, streaming)
>
> - Primary use case:
>   - A) Social network / relationships
>   - B) Knowledge graph
>   - C) Fraud detection
>   - D) Recommendation engine
>
> - Expected nodes/edges: <1M, 1M-100M, 100M+?

**After api-patterns:**
> **🔌 API Configuration**
>
> - API style:
>   - A) REST (simple, widely supported)
>   - B) GraphQL (flexible queries)
>   - C) gRPC (high-performance, typed)
>   - D) tRPC (end-to-end TypeScript)
>
> - Framework:
>   - Python: FastAPI, Flask
>   - TypeScript: Hono, Express, Fastify
>   - Rust: Axum, Actix
>   - Go: Chi, Gin
>
> - Authentication method? (JWT, API keys, OAuth)
> - Rate limiting? (Y/N)

**After message-queues:**
> **📨 Message Queue Configuration**
>
> - Use case:
>   - A) Event-driven architecture
>   - B) Background job processing
>   - C) Microservice communication
>   - D) Workflow orchestration
>
> - Technology:
>   - A) Kafka (high-throughput, ordered)
>   - B) RabbitMQ (flexible routing)
>   - C) NATS (lightweight, fast)
>   - D) Temporal (durable workflows)
>   - E) BullMQ/Celery (job queues)
>
> - Delivery guarantee: at-least-once or exactly-once?

**After realtime-sync:**
> **⚡ Real-time Configuration**
>
> - Protocol:
>   - A) WebSockets (bidirectional)
>   - B) Server-Sent Events (server push)
>   - C) WebTransport (modern, multiplexed)
>
> - Use case:
>   - A) Live updates / notifications
>   - B) Collaborative editing (Y.js/CRDT)
>   - C) Presence / cursors
>   - D) Chat / messaging
>
> - Scale: single server or distributed?

**After auth-security:**
> **🔐 Authentication Configuration**
>
> - Auth method:
>   - A) OAuth 2.1 / OIDC (Google, GitHub, etc.)
>   - B) Passkeys / WebAuthn (passwordless)
>   - C) Magic links (email)
>   - D) Username/password + MFA
>
> - Provider:
>   - A) Self-hosted (recommended for control)
>   - B) Auth0
>   - C) Clerk
>   - D) Supabase Auth
>
> - Authorization: RBAC, ABAC, or simple roles?
> - Session storage: JWT, cookies, or database?

**After observability:**
> **📊 Observability Configuration**
>
> - Stack:
>   - A) LGTM (Loki, Grafana, Tempo, Mimir) - full open-source
>   - B) OpenTelemetry + Jaeger
>   - C) Datadog (managed)
>   - D) Custom setup
>
> - What to instrument:
>   - [ ] Traces (request flow)
>   - [ ] Metrics (counters, gauges)
>   - [ ] Logs (structured)
>   - [ ] Profiling (continuous)
>
> - Alerting rules needed? (Y/N)

**After deploying-applications:**
> **🚀 Deployment Configuration**
>
> - Platform:
>   - A) Kubernetes (full control)
>   - B) Serverless (Lambda, Cloud Run)
>   - C) Edge (Cloudflare Workers, Vercel Edge)
>   - D) PaaS (Railway, Render, Fly.io)
>
> - Container registry: Docker Hub, ECR, GCR?
> - CI/CD: GitHub Actions, GitLab CI, ArgoCD?
> - Infrastructure as Code: Terraform, Pulumi, Helm?

**After ai-data-engineering:**
> **🧠 AI/RAG Pipeline Configuration**
>
> - Pipeline type:
>   - A) RAG (retrieval-augmented generation)
>   - B) Embedding generation
>   - C) Data preprocessing for ML
>   - D) Feature engineering
>
> - Chunking strategy:
>   - A) Fixed size (simple)
>   - B) Semantic (sentence boundaries)
>   - C) Recursive (hierarchical)
>   - D) Document-aware (markdown, code)
>
> - Embedding model: OpenAI, Cohere, local (sentence-transformers)?

**After model-serving:**
> **🤖 Model Serving Configuration**
>
> - Model type:
>   - A) LLM (language model)
>   - B) Embedding model
>   - C) Custom ML model
>
> - Serving framework:
>   - A) vLLM (fast LLM inference)
>   - B) Ollama (local, easy setup)
>   - C) BentoML (general ML serving)
>   - D) TensorRT-LLM (NVIDIA optimized)
>
> - Hardware: CPU, GPU, or auto-scale?
> - Batching and caching? (Y/N)

### Step 5: Invoke assembling-components (FINAL STEP)

```
Skill({ skill: "ui-assembly-skills:assembling-components" })
```

After it loads, this skill:
1. **Validates token integration** - Runs `validate_tokens.py` on all generated CSS
2. **Wires component imports** - Creates barrel exports and proper import chains
3. **Generates scaffolding** - Creates entry points (main.tsx, index.html)
4. **Configures build system** - Sets up vite.config.ts, tsconfig.json, package.json

Ask:
> **🔧 Assembly Configuration**
>
> - Target framework:
>   - A) React + Vite (SPA)
>   - B) Next.js 14/15 (SSR/SSG)
>   - C) Python FastAPI
>   - D) Rust Axum
>
> - Output directory:
>   - Default: `demo/examples/[project-name]/`
>   - Or specify custom path
>
> - Run validation script? (Y/N)

### Step 6: Generate Output

After all skills in the chain are invoked and configured:

1. **Summarize** all configurations made
2. **Generate component code** using patterns from ALL invoked skills
3. **Use CSS variables** from theming-components for all styling
4. **Apply accessibility patterns** from each skill
5. **Provide integration notes** for how pieces connect

```
✅ Skill Chain Complete!

Summary:
- Theming: [configuration]
- [Skill 2]: [configuration]
- [Skill 3]: [configuration]

Generated components use CSS variables for automatic theme switching.
All accessibility patterns applied.

Would you like me to:
A) Generate the full code
B) Explain any part in detail
C) Modify a specific configuration
```

---

## Reference Files

For detailed decision trees and prompts, read:
- @demo/KEYWORD_TRIGGERS.md
- @demo/DECISION_TREE.md
- @demo/USER_PROMPTS.md
- @demo/QUICKSTART.md

---

## CRITICAL: Theming Integration Requirements

**Every generated component MUST follow these theming rules:**

### 1. Token File Structure

When generating code, ALWAYS create these files in this order:

```
project-name/
├── tokens.css           # FIRST: All design tokens
├── index.html           # Entry point, links tokens.css
├── main.tsx             # App bootstrap, imports tokens.css
├── App.tsx or Dashboard.tsx
├── [Component].tsx      # Each component
└── [Component].css      # Component styles using tokens
```

### 2. Token Import Chain

**index.html must include:**
```html
<link rel="stylesheet" href="./tokens.css" />
```

**OR main.tsx must include:**
```tsx
import './tokens.css';
```

### 3. Component CSS Rules

**EVERY component CSS file MUST:**

1. **Use ONLY CSS variables for colors** - Never hardcode hex values
   ```css
   /* ✅ CORRECT */
   .button { background: var(--color-primary); }

   /* ❌ WRONG */
   .button { background: #3B82F6; }
   ```

2. **Use ONLY CSS variables for spacing** - Never hardcode px values
   ```css
   /* ✅ CORRECT */
   .card { padding: var(--spacing-md); gap: var(--spacing-sm); }

   /* ❌ WRONG */
   .card { padding: 16px; gap: 8px; }
   ```

3. **Use ONLY CSS variables for typography**
   ```css
   /* ✅ CORRECT */
   .title {
     font-size: var(--font-size-xl);
     font-weight: var(--font-weight-semibold);
     font-family: var(--font-sans);
   }

   /* ❌ WRONG */
   .title { font-size: 20px; font-weight: 600; }
   ```

4. **Use ONLY CSS variables for shadows, borders, radii**
   ```css
   /* ✅ CORRECT */
   .card {
     border-radius: var(--radius-lg);
     box-shadow: var(--shadow-md);
     border: var(--border-width-thin) solid var(--color-border-primary);
   }
   ```

5. **Use ONLY CSS variables for transitions**
   ```css
   /* ✅ CORRECT */
   .button { transition: var(--transition-fast); }

   /* ❌ WRONG */
   .button { transition: all 150ms ease; }
   ```

### 4. Required Token Categories

Every tokens.css MUST define these categories:

```css
:root {
  /* 1. COLORS - Brand + Semantic + Component */
  --color-primary: #...;
  --color-bg-primary: #...;
  --color-text-primary: #...;
  --color-border-primary: #...;

  /* 2. SPACING - 4px or 8px base scale */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  /* 3. TYPOGRAPHY */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-weight-normal: 400;
  --font-weight-semibold: 600;

  /* 4. BORDERS & RADIUS */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --border-width-thin: 1px;

  /* 5. SHADOWS */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);

  /* 6. MOTION */
  --duration-fast: 150ms;
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --transition-fast: all var(--duration-fast) var(--ease-out);

  /* 7. Z-INDEX */
  --z-dropdown: 1000;
  --z-modal: 1050;
  --z-toast: 1080;
}

/* DARK THEME - Override semantic tokens */
[data-theme="dark"] {
  --color-bg-primary: #0F172A;
  --color-text-primary: #F8FAFC;
  /* ... all semantic color overrides */
}
```

### 5. Component Token Mapping

Each component type has specific tokens to use:

| Component | Required Tokens |
|-----------|-----------------|
| **Cards/Containers** | `--color-bg-*`, `--radius-*`, `--shadow-*`, `--spacing-*` |
| **Buttons** | `--color-primary`, `--radius-*`, `--font-weight-*`, `--transition-*` |
| **Text** | `--color-text-*`, `--font-size-*`, `--font-weight-*`, `--line-height-*` |
| **Inputs** | `--color-border-*`, `--color-bg-*`, `--radius-*`, `--spacing-*` |
| **Charts** | `--chart-color-1` through `--chart-color-6`, `--color-text-*` |
| **Toasts** | `--color-success`, `--color-error`, `--shadow-lg`, `--z-toast` |
| **Modals** | `--z-modal`, `--shadow-xl`, `--color-bg-*`, `--radius-*` |

### 6. Validation Checklist

Before completing code generation, verify:

- [ ] `tokens.css` exists and is imported first
- [ ] No hardcoded color values in any CSS file
- [ ] No hardcoded spacing values (px/rem) in any CSS file
- [ ] All components reference CSS variables
- [ ] Dark theme tokens are defined
- [ ] `[data-theme="dark"]` overrides exist for all semantic colors
- [ ] Theme toggle functionality works
- [ ] Reduced motion media query included

### 7. Theme Toggle Implementation

Always include a working theme toggle:

```tsx
function ThemeToggle() {
  const [theme, setTheme] = useState(() =>
    localStorage.getItem('theme') || 'light'
  );

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  return (
    <button onClick={() => setTheme(t => t === 'light' ? 'dark' : 'light')}>
      {theme === 'light' ? '🌙' : '☀️'}
    </button>
  );
}
```

### 8. Accessibility Token Requirements

Always include:

```css
/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-fast: 0ms;
    --duration-normal: 0ms;
    --transition-fast: none;
    --transition-normal: none;
  }
}

/* Focus states */
:root {
  --shadow-focus: 0 0 0 3px rgba(var(--color-primary-rgb), 0.3);
}

.interactive-element:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

---

## Begin Execution

Now parse "$ARGUMENTS" and begin the skill chain workflow.

If "$ARGUMENTS" is empty, "help", or unclear, show the help guide above.

Otherwise, identify keywords, announce the skill chain, and invoke the first skill.

**Remember: Theming integration is MANDATORY. Every component must use design tokens.**
