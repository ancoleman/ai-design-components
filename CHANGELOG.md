# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.3] - 2025-12-02

### Added
- **Skillchain v2.1 - Modular Architecture (Phase 3 Complete)**:
  - **User Preferences System**: Saves choices to `~/.claude/skillchain-prefs.yaml` for smart defaults
  - **Skill Versioning**: All 29 skills versioned (v1.0.0) with changelog and compatibility tracking
  - **Parallel Skill Loading**: Independent skills load concurrently via `parallel_group` field
  - **Blueprint System**: Pre-configured skill chains for common patterns:
    - `dashboard` - Analytics dashboard with charts & KPIs
    - `crud-api` - REST API with database & auth
    - `rag-pipeline` - RAG with vector search & embeddings
  - **Category Orchestrators**: Specialized handlers for frontend, backend, fullstack, ai-ml
  - **Dynamic Path Discovery**: Works globally from any project via Bash path detection

- New skillchain directory structure (19 files):
  - `skillchain.md` - Router with Step 0 (path discovery), Step 0.5 (preferences), Step 7 (save prefs)
  - `_registry.yaml` - 29 skills with keywords, dependencies, versions, parallel_group
  - `_help.md` - Updated help with v2.1 features
  - `_shared/` - 9 shared resource files (theming-rules, execution-flow, preferences, parallel-loading, changelog, compatibility)
  - `categories/` - 4 orchestrators (frontend.md, backend.md, fullstack.md, ai-ml.md)
  - `blueprints/` - 3 templates (dashboard.md, crud-api.md, rag-pipeline.md)

- Updated `commands/README.md` with comprehensive v2.1 documentation
- Updated `_help.md` with v2.1 features section and revised workflow steps

### Changed
- Installer updated to v2.1 with Phase 3 feature display
- Registry version bumped to 2.1.0
- All file references now use `{SKILLCHAIN_DIR}/...` pattern for portability
- `_help.md` "How It Works" section updated to reflect 8-step workflow

### Removed
- Old monolithic `skillchain.md` files (replaced by modular structure)

## [0.3.2] - 2025-12-02

### Added
- Complete backend support in `/skillchain` command:
  - Backend plugin groups: `backend-data-skills`, `backend-api-skills`, `backend-platform-skills`, `backend-ai-skills`
  - Backend skill mappings for all 14 backend skills
  - 14 new backend configuration question blocks (databases, APIs, auth, observability, deployment, AI/ML)
  - Backend keyword detection (database, api, vector, kafka, deploy, auth, etc.)
  - Full-stack compound detection combining frontend and backend skills
- Backend examples in skillchain help guide
- Global installation option for skillchain command (`--global` flag)
- Architecture documentation directory (`docs/architecture/`)

### Changed
- Updated skillchain.md to show all 29 skills (was showing only 15)
- Help guide now displays both frontend (15) and backend (14) skill categories
- Skillchain description updated to "full-stack applications" (from "UI components")
- Moved TOKEN_EFFICIENCY.md to `docs/architecture/` for better organization
- Updated README.md with architecture docs link

### Removed
- Deleted `skillchains/` directory (17 files) - outdated documentation superseded by `/skillchain` command
  - README.md, GUIDE.md, ROADMAP.md (outdated, claimed "3/14 skills")
  - patterns/ directory (now embedded in skillchain.md)
  - chains/ directory (superseded by keyword mapping)
  - examples/ directory

### Fixed
- YAML frontmatter error in skillchain.md (unquoted values containing colons)

## [0.3.1] - 2025-12-02

### Added
- New `ingesting-data` skill for data onboarding and ETL pipelines
  - Cloud storage ingestion (S3, GCS, Azure Blob)
  - File format handling (CSV, JSON, Parquet, Excel)
  - API feed consumption (REST polling, webhooks, GraphQL subscriptions)
  - Streaming sources (Kafka, Kinesis, Pub/Sub)
  - Database migration and CDC patterns
  - ETL tools reference (dlt, Meltano, Airbyte, Dagster)
- Scripts for ingesting-data:
  - `validate_csv_schema.py` - CSV schema validation
  - `test_s3_connection.py` - S3 connectivity testing
  - `generate_dlt_pipeline.py` - dlt pipeline scaffold generator

### Changed
- Updated skillchain.md with ingestion keyword mapping
- backend-data-skills plugin now includes ingesting-data as first skill
- Version bump to 0.3.1

## [0.3.0] - 2025-12-02

### Added
- **13 Backend Skills** - Complete backend development capability:

  **Database Skills (5):**
  - `databases-relational` - PostgreSQL, MySQL, SQLite with Prisma/Drizzle/SQLAlchemy
  - `databases-vector` - Qdrant, Pinecone, pgvector for RAG and semantic search
  - `databases-timeseries` - ClickHouse, TimescaleDB, InfluxDB for metrics
  - `databases-document` - MongoDB, Firestore, DynamoDB for flexible schemas
  - `databases-graph` - Neo4j, memgraph with Cypher query patterns

  **API & Communication Skills (3):**
  - `api-patterns` - REST, GraphQL, gRPC, tRPC across Python/TypeScript/Rust/Go
  - `message-queues` - Kafka, RabbitMQ, NATS, Temporal for async processing
  - `realtime-sync` - WebSockets, SSE, Y.js, Liveblocks for live collaboration

  **Platform Skills (3):**
  - `observability` - OpenTelemetry, LGTM stack (Loki, Grafana, Tempo, Mimir)
  - `auth-security` - OAuth 2.1, passkeys/WebAuthn, RBAC, secrets management
  - `deploying-applications` - Kubernetes, serverless, edge deployment patterns

  **AI/ML Skills (2):**
  - `ai-data-engineering` - RAG pipelines, embedding strategies, chunking
  - `model-serving` - vLLM, BentoML, Ollama for LLM deployment

- 4 new plugin groups in marketplace.json:
  - `backend-data-skills` - All database skills
  - `backend-api-skills` - API, messaging, realtime
  - `backend-platform-skills` - Observability, auth, deployment
  - `backend-ai-skills` - AI data engineering, model serving

- Backend keyword mappings in skillchain.md for automatic skill chaining
- Multi-language support across all backend skills (Python, TypeScript, Rust, Go)
- Scripts for auth-security:
  - `generate_jwt_keys.py` - EdDSA/ES256 key pair generation
  - `validate_oauth_config.py` - OAuth 2.1 compliance validation
- Script for realtime-sync:
  - `test_websocket_connection.py` - WebSocket connectivity testing

### Changed
- Total skill count: 15 frontend + 13 backend = 28 skills
- All backend SKILL.md files under 500 lines (progressive disclosure applied)
- Updated CLAUDE.md with backend skill references

## [0.2.0] - 2025-12-01

### Added
- Complete SKILL.md implementations for all 14 component skills
- New skills completed:
  - `managing-media` - Media & file management components
  - `guiding-users` - Onboarding & help systems
  - `displaying-timelines` - Timeline & activity components
  - `building-ai-chat` - AI chat interfaces (strategic priority)
  - `creating-dashboards` - Dashboard & analytics components
  - `building-tables` - Tables & data grids
  - `implementing-search-filter` - Search & filter interfaces
  - `implementing-drag-drop` - Drag-and-drop functionality
  - `providing-feedback` - Feedback & notification systems
  - `implementing-navigation` - Navigation patterns
  - `designing-layouts` - Layout systems & responsive design
- Reference files for theming-components:
  - `color-system.md` - Complete color token reference
  - `typography-system.md` - Typography token reference
  - `spacing-system.md` - Spacing token reference
- Comprehensive chart catalog for visualizing-data (24+ chart types)

### Changed
- Renamed all skill directories to use gerund naming convention (Anthropic best practice):
  - `data-viz` → `visualizing-data`
  - `forms` → `building-forms`
  - `design-tokens` → `theming-components`
  - `ai-chat` → `building-ai-chat`
  - `dashboards` → `creating-dashboards`
  - `tables` → `building-tables`
  - `search-filter` → `implementing-search-filter`
  - `drag-drop` → `implementing-drag-drop`
  - `feedback` → `providing-feedback`
  - `navigation` → `implementing-navigation`
  - `layout` → `designing-layouts`
  - `timeline` → `displaying-timelines`
  - `media` → `managing-media`
  - `onboarding` → `guiding-users`
- Reduced `theming-components/SKILL.md` from 878 to 384 lines (progressive disclosure)
- Reduced `visualizing-data/SKILL.md` from 639 to 329 lines (progressive disclosure)
- Updated marketplace.json with all 14 correct skill paths
- Moved all init.md files to `docs/init_files/` for reference

### Fixed
- Skill naming convention violations (now all use gerund form)
- SKILL.md line count violations (all now under 500 lines)
- Directory names now match SKILL.md frontmatter names

## [0.1.0] - 2025-01-13

### Added
- Initial project structure with 14 component skill categories
- Completed `data-viz` skill with 24+ visualization types and decision frameworks
- Completed `forms` skill with 50+ input types and validation patterns
- Comprehensive master plans (init.md) for all 14 skill categories
- Research methodology guide for library recommendations
- Skills organized into 6 plugin groups in marketplace.json:
  - ui-foundation-skills (design-tokens)
  - ui-data-skills (data-viz, tables, dashboards)
  - ui-input-skills (forms, search-filter)
  - ui-interaction-skills (ai-chat, drag-drop, feedback)
  - ui-structure-skills (navigation, layout, timeline)
  - ui-content-skills (media, onboarding)
- Project documentation (README.md, CLAUDE.md, skill_best_practice.md)
- MIT License
- Comprehensive .gitignore for development

### In Progress
- 12 additional component skills awaiting SKILL.md implementation
- Design tokens foundational system
- AI chat interfaces (strategic priority)

[0.3.3]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.3.3
[0.3.2]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.3.2
[0.3.1]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.3.1
[0.3.0]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.3.0
[0.2.0]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.2.0
[0.1.0]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.1.0
