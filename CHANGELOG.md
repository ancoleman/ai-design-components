# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.1] - 2025-12-03

### 🚀 MILESTONE: 47 New Skill Master Plans (DevOps, Security, Cloud, AI/ML)

**Major Achievement:** Created comprehensive init.md master plans for 47 new skills covering DevOps, Infrastructure, Security, Cloud, and AI/ML domains. Total of 90,839 lines of strategic planning documentation.

### Added

**47 New Skill Master Plans (init.md files):**

**Infrastructure & Networking (12 skills):**
- `infrastructure-as-code` - Terraform, Pulumi, CDK patterns (769 lines)
- `kubernetes-operations` - K8s management, Helm, operators (2,083 lines)
- `designing-distributed-systems` - Architecture patterns, CAP theorem (2,905 lines)
- `configuration-management` - Ansible, Chef, Puppet (1,844 lines)
- `network-architecture` - VPC design, subnets, routing (2,302 lines)
- `load-balancing-patterns` - ALB, NLB, service mesh LB (2,224 lines)
- `dns-management` - Route53, CloudDNS, record types (2,534 lines)
- `service-mesh` - Istio, Linkerd, Cilium (2,051 lines)
- `disaster-recovery` - RPO/RTO, backup strategies (2,843 lines)
- `linux-administration` - System management, troubleshooting (2,559 lines)
- `shell-scripting` - Bash/Zsh patterns (1,194 lines)
- `configuring-nginx` - Reverse proxy, SSL, performance (1,917 lines)

**Security (6 skills):**
- `security-architecture` - Zero trust, defense in depth (1,570 lines)
- `compliance-frameworks` - SOC2, ISO27001, HIPAA (2,333 lines)
- `vulnerability-management` - Scanning, remediation (2,023 lines)
- `siem-logging` - Security monitoring, alerting (2,666 lines)
- `implementing-tls` - Certificate management, mTLS (2,093 lines)
- `configuring-firewalls` - Network security rules (1,704 lines)

**Developer Productivity (7 skills):**
- `api-design-principles` - REST, GraphQL design patterns (2,781 lines)
- `building-clis` - Python, Go, Rust CLI frameworks (2,368 lines) [MULTI-LANGUAGE]
- `sdk-design` - Client library patterns (2,461 lines) [MULTI-LANGUAGE]
- `documentation-generation` - API docs, code docs (3,140 lines)
- `debugging-techniques` - Profiling, troubleshooting (1,711 lines) [MULTI-LANGUAGE]
- `git-workflows` - Branching strategies, hooks (1,549 lines)
- `writing-github-actions` - CI/CD workflows (1,996 lines)

**DevOps & Platform (6 skills):**
- `building-ci-pipelines` - GitHub Actions, GitLab CI, Jenkins (1,793 lines)
- `gitops-workflows` - ArgoCD, Flux patterns (1,454 lines)
- `testing-strategies` - Unit, integration, E2E testing (1,791 lines) [MULTI-LANGUAGE]
- `platform-engineering` - IDP, Backstage, developer experience (2,876 lines)
- `incident-management` - On-call, post-mortems, SRE (1,615 lines)
- `writing-dockerfiles` - Multi-stage, security hardening (1,212 lines)

**Data & Analytics (6 skills):**
- `data-architecture` - Data mesh, lakehouse, medallion (2,359 lines)
- `streaming-data` - Kafka, Flink, event streaming (1,624 lines) [MULTI-LANGUAGE]
- `data-transformation` - dbt, ETL/ELT patterns (1,780 lines) [MULTI-LANGUAGE]
- `sql-optimization` - Query tuning, indexing (1,106 lines)
- `secret-management` - Vault, secrets rotation (1,427 lines)
- `performance-engineering` - Profiling, optimization (1,714 lines)

**AI/ML Operations (4 skills):**
- `mlops-patterns` - MLflow, experiment tracking, feature stores (2,295 lines)
- `prompt-engineering` - LLM prompting, chain-of-thought (1,577 lines)
- `llm-evaluation` - RAGAS, benchmarks, safety testing (1,557 lines)
- `embedding-optimization` - Chunking, model selection (1,416 lines)

**Cloud Patterns (3 skills):**
- `aws-patterns` - Well-Architected, service selection (2,475 lines)
- `gcp-patterns` - BigQuery, Vertex AI, GKE (1,840 lines)
- `azure-patterns` - Container Apps, Azure OpenAI (1,695 lines)

**FinOps (3 skills):**
- `cost-optimization` - FinOps practices, rightsizing (1,370 lines)
- `resource-tagging` - Tag governance, enforcement (1,175 lines)
- `security-hardening` - CIS benchmarks, hardening (1,068 lines)

**Project Documentation:**
- `docs/SKILL_ORCHESTRATION_PLAN.md` - Wave-based execution strategy for skill creation

### Multi-Language Skills

9 skills include implementations across TypeScript, Python, Go, and Rust:
- `testing-strategies`, `building-clis`, `sdk-design`, `debugging-techniques`
- `streaming-data`, `data-transformation`, `shell-scripting`, `sql-optimization`
- All cloud pattern skills include Terraform, CDK, and native SDK examples

### Research Methodology

All init.md files include research from:
- **Google Search Grounding**: 100+ queries for 2025 best practices
- **Context7**: Library trust scores and documentation (e.g., Argo CD 91.8/100, MLflow 95/100)
- Decision frameworks with actionable guidance
- Production-ready tool recommendations

### Statistics

- **Total init.md files:** 47
- **Total lines written:** 90,839
- **Average lines per skill:** 1,933
- **Skills with SKILL.md (production):** 29
- **Total skill coverage:** 76 skills

---

## [0.4.0] - 2025-12-03

### 🎉 MILESTONE: 100% Progressive Disclosure Coverage

**Major Achievement:** All 29 skills now have complete progressive disclosure with zero broken references.

### Added

**110 new files created across 17 skills to complete progressive disclosure:**

**Phase 0 - Low Priority (7 skills, 20 files):**
- `databases-timeseries/references/questdb.md` - QuestDB high-throughput guide
- `visualizing-data/examples/javascript/accessible-chart.tsx` - WCAG 2.1 AA compliant chart
- `auth-security/references/` - 3 files (api-security, managed-auth-comparison, self-hosted-auth)
- `databases-relational/references/` - 3 files (mysql-guide, sqlite-guide, serverless-databases)
- `implementing-navigation/examples/` - 3 files (mobile-navigation, django_urls, fastapi_routes)
- `model-serving/` - 3 files (streaming-sse.md, k8s-vllm-deployment/, langchain-rag-qdrant/)
- `databases-vector/` - 4 files (hybrid-search.md, rust-axum-vector/, typescript-rag/, evaluate_rag.py)

**Phase 1 - Medium Priority (4 skills, 22 files):**
- `assembling-components/` - 7 files (Python/React/Rust templates + 4 dashboard examples)
- `api-patterns/examples/` - 5 files (go-gin, graphql-strawberry, grpc-tonic, rust-axum, typescript-trpc)
- `message-queues/` - 5 files (BullMQ/Celery guides + 3 complete workflow examples)
- `observability/` - 4 files (axum-tracing, lgtm-docker-compose, 2 automation scripts)

**Phase 2 - High Priority (4 skills, 30 files):**
- `creating-dashboards/` - 10 files (grid layouts, KPI formats, themes, 5 dashboard examples, 2 scripts)
- `building-ai-chat/` - 8 files (4 reference guides + 4 complete chat examples)
- `ai-data-engineering/` - 4 files (chunking strategies, data versioning, orchestration, Qdrant setup)
- `databases-document/` - 8 files (aggregation, indexing, patterns, anti-patterns, 2 examples)

**Phase 3 - Critical Priority (2 skills, 38 files):**
- `building-tables/` - 14 files (6 reference guides + 6 examples + 2 scripts)
  - References: basic-tables, interactive, advanced-grids, editing, responsive, selection
  - Examples: TanStack basic, sortable/filtered, virtual scrolling, AG Grid, responsive patterns, editable cells, state persistence, server-side sorting
  - Scripts: export_table_data, (existing scripts)
- `managing-media/` - 24 files (13 reference guides + 11 examples)
  - References: image upload/optimization, video optimization, PDF viewer, audio player, cloud storage, carousel, responsive, accessibility (images/video/audio), advanced upload, office viewer
  - Examples: image crop, carousel, gallery, chunked upload, S3 direct, audio player/waveform, video player, PDF viewers

**Project Documentation:**
- `SKILL_COMPLETION_PLAN.md` - Comprehensive completion tracking document (v2.0 - FINAL)

### Changed

- **Completion Status:** 41% → 100% (all 29 skills complete)
- **Missing Files:** 116 → 0 (100% reduction)
- **Progressive Disclosure:** Fully intact across all skills
- Updated `SKILL_COMPLETION_PLAN.md` through versions 1.0 → 2.0 (FINAL)

### Impact

**Coverage Now Complete For:**
- All database types (relational, document, vector, timeseries, graph)
- All API patterns (REST, GraphQL, gRPC, tRPC) across 5 languages
- Full AI/ML pipeline (RAG, embeddings, chunking, orchestration)
- Complete chat interfaces (streaming, multi-modal, tool-calling, accessibility)
- Dashboard components (executive, monitoring, customizable, real-time)
- Data tables (basic, interactive, advanced grids, virtual scrolling, editing)
- Media handling (image, video, audio, PDF, Office docs)
- Message queues (BullMQ, Celery, Temporal)
- Observability (LGTM stack, OpenTelemetry)
- Full-stack templates (Python, TypeScript, Rust, Go)
- Authentication and security
- Navigation patterns
- All 29 skills production-ready

### Files Created

- **Reference Documentation:** 54 comprehensive guides
- **Code Examples:** 42 working implementations
- **Scripts:** 12 automation utilities (token-free execution)
- **Assets:** 2 configuration files

### Statistics

- Total files created: 110
- Time elapsed: ~7 hours
- Skills completed: 17 (from 12 to 29)
- Languages supported: Python, TypeScript, Rust, Go
- Zero broken references remaining

## [0.3.4] - 2025-12-03

### Added
- **Community Health Files**:
  - `CODE_OF_CONDUCT.md` - Contributor Covenant v2.1
  - `CONTRIBUTING.md` - Comprehensive contribution guidelines
    - Skill development guidelines from skill_best_practice.md
    - Branch naming, commit messages, PR process
    - Quality checklist for skills
    - Multi-language support expectations

- **GitHub Issue Templates** (`.github/ISSUE_TEMPLATE/`):
  - `bug_report.yml` - Bug reporting with component, skill, environment fields
  - `feature_request.yml` - Feature proposals with priority and acceptance criteria
  - `skill_contribution.yml` - Dedicated skill contribution workflow
    - Quality checklist (500 line limit, gerund naming, progressive disclosure)
    - Decision framework requirements
    - Multi-language support
  - `documentation.yml` - Documentation improvement requests
  - `question.yml` - General questions and discussions
  - `config.yml` - Template configuration with contact links

- **Project Roadmap System**:
  - `.github/ROADMAP.md` - Comprehensive project roadmap reflecting all 29 skills complete
  - `.github/ISSUE_TEMPLATE/roadmap_item.yml` - Issue template for proposing roadmap items

### Changed
- **Documentation Updates**:
  - `docs/STYLING_TEMPLATE.md` - Completely rewritten as integration guide
    - Updated to reflect all 29 skills complete
    - Added component-specific token references for all 12 UI skills
    - Added theme switching, RTL support, and accessibility sections
    - Uses correct gerund skill naming convention
  - Added `source_data/` to `.gitignore`

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

[0.4.1]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.4.1
[0.4.0]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.4.0
[0.3.4]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.3.4
[0.3.3]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.3.3
[0.3.2]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.3.2
[0.3.1]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.3.1
[0.3.0]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.3.0
[0.2.0]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.2.0
[0.1.0]: https://github.com/ancoleman/ai-design-components/releases/tag/v0.1.0
