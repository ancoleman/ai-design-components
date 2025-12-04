# AI Design Components

> Comprehensive Full-Stack, DevOps, Security, Cloud, and AI/ML skills for AI-assisted development with Claude

[![Version](https://img.shields.io/badge/version-0.4.1-blue.svg)](./VERSION)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-76-purple.svg)](./skills)
[![Production](https://img.shields.io/badge/production-29-green.svg)](./skills)
[![Master Plans](https://img.shields.io/badge/master_plans-47-orange.svg)](./skills)

## Overview

AI Design Components is a comprehensive collection of Claude Skills covering **76 skill domains** for full-stack development, DevOps, Security, Cloud, and AI/ML. With **29 production-ready skills** (SKILL.md) and **47 master plans** (init.md) ready for implementation, this project provides research-backed recommendations, decision frameworks, and production-ready code patterns.

**v0.4.1 Highlights:**
- 47 new skill master plans covering DevOps, Infrastructure, Security, Cloud, and AI/ML
- Multi-language support (TypeScript, Python, Go, Rust) across 9 skills
- Research-backed recommendations using Google Search Grounding and Context7

Built following [Anthropic's official Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), these skills use progressive disclosure to minimize context usage while maximizing Claude's effectiveness.

## Quick Start with Skillchain (v2.1)

The **recommended way** to use AI Design Components is through the `/skillchain` command. Instead of manually triggering individual skills, skillchain provides a guided workflow with intelligent defaults.

```bash
# Install globally (available in ALL your projects)
./commands/install-skillchain.sh --global

# Then start Claude Code and use skillchain
claude
/skillchain dashboard with charts and filters
```

### Why Skillchain?

| Traditional Approach | Skillchain Approach |
|---------------------|---------------------|
| Must know skill names | Just describe what you want |
| Trigger skills individually | Skills chain automatically |
| Easy to miss required skills | Correct order enforced |
| Manual theming | Theming always applied first |
| Hope components integrate | Assembly validation at end |
| Answer same questions each time | **Preferences saved for next time** |

### Skillchain v2.1 Features

| Feature | Description |
|---------|-------------|
| **Blueprints** | Pre-configured chains for common patterns (dashboard, crud-api, rag-pipeline) |
| **User Preferences** | Saves your choices to `~/.claude/skillchain-prefs.yaml` for smart defaults |
| **Parallel Loading** | Independent skills load concurrently for faster workflows |
| **Skill Versioning** | All 29 skills versioned (v1.0.0) with compatibility tracking |
| **Category Routing** | Automatic routing to frontend, backend, fullstack, or ai-ml orchestrators |

### Examples

```
/skillchain help                              # Show all 29 skills + v2.1 features
/skillchain sales dashboard with KPIs         # → Uses dashboard blueprint
/skillchain REST API with postgres            # → Uses crud-api blueprint
/skillchain RAG pipeline with embeddings      # → Uses rag-pipeline blueprint
/skillchain login form with OAuth             # Full-stack: theming → forms → auth-security
```

### Modular Architecture

```
commands/skillchain/
├── skillchain.md           # Router with dynamic path discovery
├── _registry.yaml          # 29 skills with keywords, dependencies, versions
├── _help.md                # Help content
├── _shared/                # Theming rules, preferences, parallel loading
├── categories/             # Frontend, backend, fullstack, ai-ml orchestrators
└── blueprints/             # Dashboard, crud-api, rag-pipeline templates
```

See [commands/README.md](./commands/README.md) for complete skillchain documentation.

## Project Status

- **Current Version:** 0.4.1
- **Skillchain Version:** 2.1.0 (modular architecture)
- **Production Skills (SKILL.md):** 29 complete
  - Frontend Skills: 15/15
  - Backend Skills: 14/14
- **Master Plans (init.md):** 47 complete
  - Infrastructure & Networking: 12 skills
  - Security: 6 skills
  - Developer Productivity: 7 skills
  - DevOps & Platform: 6 skills
  - Data & Analytics: 6 skills
  - AI/ML Operations: 4 skills
  - Cloud Patterns: 3 skills
  - FinOps: 3 skills
- **Total Skill Coverage:** 76

## Skill Categories

### Frontend Skills (15)

#### 🎨 UI Foundation Skills
- `theming-components` - Design tokens and theming system

#### 📊 UI Data Skills
- `visualizing-data` - Data visualization (24+ chart types)
- `building-tables` - Tables and data grids
- `creating-dashboards` - Dashboard layouts and analytics

#### 📝 UI Input Skills
- `building-forms` - Form systems and validation (50+ input types)
- `implementing-search-filter` - Search and filter interfaces

#### 🤖 UI Interaction Skills
- `building-ai-chat` - AI chat interfaces
- `implementing-drag-drop` - Drag-and-drop functionality
- `providing-feedback` - Feedback and notification systems

#### 🧭 UI Structure Skills
- `implementing-navigation` - Navigation patterns
- `designing-layouts` - Layout systems and responsive design
- `displaying-timelines` - Timeline and activity components

#### 🎬 UI Content Skills
- `managing-media` - Media and file management
- `guiding-users` - Onboarding and help systems

#### 🔧 UI Assembly Skills
- `assembling-components` - Component integration and validation

### Backend Skills (14)

#### 💾 Backend Data Skills
- `ingesting-data` - ETL, data ingestion from S3/APIs/files
- `databases-relational` - PostgreSQL, MySQL, SQLite
- `databases-vector` - Qdrant, Pinecone, pgvector
- `databases-timeseries` - ClickHouse, TimescaleDB, InfluxDB
- `databases-document` - MongoDB, Firestore, DynamoDB
- `databases-graph` - Neo4j, memgraph

#### 🔌 Backend API Skills
- `api-patterns` - REST, GraphQL, gRPC, tRPC
- `message-queues` - Kafka, RabbitMQ, NATS, Temporal
- `realtime-sync` - WebSockets, SSE, Y.js

#### 🛡️ Backend Platform Skills
- `observability` - OpenTelemetry, LGTM stack
- `auth-security` - OAuth 2.1, passkeys, RBAC
- `deploying-applications` - Kubernetes, serverless, edge

#### 🧠 Backend AI Skills
- `ai-data-engineering` - RAG pipelines, embeddings
- `model-serving` - vLLM, BentoML, Ollama

### Master Plan Skills (47)

47 additional skills have comprehensive `init.md` master plans ready for SKILL.md implementation, covering:

- **Infrastructure & Networking** (12) - IaC, Kubernetes, distributed systems, networking
- **Security** (6) - Architecture, compliance, vulnerability management
- **Developer Productivity** (7) - API design, CLIs, SDKs, debugging
- **DevOps & Platform** (6) - CI/CD, GitOps, testing, platform engineering
- **Data & Analytics** (6) - Data architecture, streaming, transformation
- **AI/ML Operations** (4) - MLOps, prompt engineering, LLM evaluation
- **Cloud Patterns** (3) - AWS, GCP, Azure architectural patterns
- **FinOps** (3) - Cost optimization, tagging, hardening

See **[docs/MASTER_PLANS.md](./docs/MASTER_PLANS.md)** for the complete list.

## Prerequisites

### Required
- **Claude Code CLI** - [Install Claude Code](https://docs.anthropic.com/en/docs/claude-code)

### Recommended (for latest library documentation)
- **Context7 MCP Server** - Provides up-to-date documentation lookup for libraries

  ```bash
  # Add to your Claude Code MCP configuration
  # ~/.config/claude/mcp.json (or project .claude/mcp.json)
  {
    "mcpServers": {
      "context7": {
        "command": "npx",
        "args": ["-y", "@anthropics/context7-mcp"]
      }
    }
  }
  ```

  With Context7 enabled, skills can verify library recommendations against current documentation, ensuring you always get the latest patterns and best practices.

### Optional
- **Google Search MCP** - For real-time library research and validation

## Installation

### Option 1: Add as Claude Code Marketplace (Recommended)

```bash
/plugin marketplace add ancoleman/ai-design-components
```

Then install plugin groups:

```bash
# Frontend skills
/plugin install ui-data-skills@ai-design-components
/plugin install ui-input-skills@ai-design-components

# Backend skills
/plugin install backend-data-skills@ai-design-components
/plugin install backend-api-skills@ai-design-components
```

### Option 2: Install Skillchain Command

For the guided workflow experience:

```bash
git clone https://github.com/ancoleman/ai-design-components.git
cd ai-design-components
./commands/install-skillchain.sh ~/your-project
```

### Option 3: Local Development

```bash
git clone https://github.com/ancoleman/ai-design-components.git
cd ai-design-components
# Skills available immediately when working in this directory
```

## Multi-Language Support

All backend skills provide patterns for multiple languages:

| Language | Framework Examples |
|----------|-------------------|
| **Python** | FastAPI, SQLAlchemy, dlt, Polars |
| **TypeScript** | Hono, Prisma, Drizzle, tRPC |
| **Rust** | Axum, sqlx, tokio |
| **Go** | Chi, pgx, sqlc |

## Skill Structure

Each skill follows a standardized structure:

```
skills/[skill-name]/
├── SKILL.md              # Main skill file (<500 lines)
├── references/           # Detailed documentation
├── examples/             # Code examples by language
├── scripts/              # Utility scripts (executed without loading)
└── assets/               # Templates and schemas
```

## Documentation

- **[commands/README.md](./commands/README.md)** - Skillchain command documentation
- **[SETUP.md](./SETUP.md)** - Complete marketplace installation guide
- **[CLAUDE.md](./CLAUDE.md)** - Repository guidance for Claude
- **[CHANGELOG.md](./CHANGELOG.md)** - Version history and updates
- **[docs/MASTER_PLANS.md](./docs/MASTER_PLANS.md)** - 47 skill master plans (DevOps, Security, Cloud, AI/ML)
- **[skills/RESEARCH_GUIDE.md](./skills/RESEARCH_GUIDE.md)** - Library research methodology
- **[docs/architecture/](./docs/architecture/)** - Token efficiency and architecture docs

## Resources

- [Anthropic Skills Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Skills Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/skills)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)

## License

MIT License - See [LICENSE](./LICENSE) for details.

---

**Built with Claude** | Following [Anthropic's Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
