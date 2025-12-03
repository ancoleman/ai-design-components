# AI Design Components

> Comprehensive UI/UX and Backend component design skills for AI-assisted development with Claude

[![Version](https://img.shields.io/badge/version-0.3.1-blue.svg)](./VERSION)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-29-purple.svg)](./skills)

## Overview

AI Design Components is a collection of Claude Skills that provide expert guidance for designing and implementing full-stack applications. With **29 skills** across frontend and backend development, these skills combine research-backed recommendations, decision frameworks, and production-ready code patterns.

Built following [Anthropic's official Skills best practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills), these skills use progressive disclosure to minimize context usage while maximizing Claude's effectiveness.

## Quick Start with Skillchain

The **recommended way** to use AI Design Components is through the `/skillchain` command. Instead of manually triggering individual skills, skillchain provides a guided workflow:

```bash
# Option A: Install globally (available in ALL your projects)
./commands/install-skillchain.sh --global

# Option B: Install to specific project
./commands/install-skillchain.sh ~/your-project

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

**Examples:**

```
/skillchain help                              # Show all 29 skills
/skillchain sales dashboard with KPIs         # Frontend: theming → layouts → dashboards → data-viz
/skillchain login form with OAuth             # Full-stack: theming → forms → api-patterns → auth-security
/skillchain import CSV to postgres            # Backend: ingesting-data → databases-relational
/skillchain RAG pipeline with vector search   # AI/ML: ingesting-data → ai-data-engineering → databases-vector
```

See [commands/README.md](./commands/README.md) for complete skillchain documentation.

## Project Status

- **Current Version:** 0.3.1
- **Frontend Skills:** 15/15 complete
- **Backend Skills:** 14/14 complete
- **Total Skills:** 29

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
- **[skills/RESEARCH_GUIDE.md](./skills/RESEARCH_GUIDE.md)** - Library research methodology
- **[docs/architecture/](./docs/architecture/)** - Token efficiency and architecture docs

## Resources

- [Anthropic Skills Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills)
- [Skills Best Practices](https://anthropic.mintlify.app/en/docs/agents-and-tools/agent-skills/best-practices)
- [Skills Cookbook](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/cookbook)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)

## License

MIT License - See [LICENSE](./LICENSE) for details.

---

**Built with Claude** | Following [Anthropic's Skills best practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills)
