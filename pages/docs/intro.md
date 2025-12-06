---
sidebar_position: 1
title: Introduction
description: Comprehensive Claude Skills for full-stack development
---

# AI Design Components

> Comprehensive Full-Stack, DevOps, Security, Cloud, and AI/ML skills for AI-assisted development with Claude

## Overview

AI Design Components is a comprehensive collection of **76 production-ready Claude Skills** covering full-stack development, DevOps, Security, Cloud, and AI/ML. This project provides research-backed recommendations, decision frameworks, and production-ready code patterns.

**v0.5.0 Highlights:**
- All 76 skills now production-ready with complete SKILL.md documentation
- 47 new skills covering DevOps, Infrastructure, Security, Cloud, Data Engineering, and AI/ML
- Validation package with CI and TUI modes for skill quality checks
- Multi-language support (TypeScript, Python, Go, Rust) across all applicable skills

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
| **Skill Versioning** | All 76 skills versioned (v1.0.0) with compatibility tracking |
| **Category Routing** | Automatic routing to frontend, backend, fullstack, or ai-ml orchestrators |

### Examples

```
/skillchain help                              # Show all 76 skills + v2.1 features
/skillchain sales dashboard with KPIs         # → Uses dashboard blueprint
/skillchain REST API with postgres            # → Uses crud-api blueprint
/skillchain RAG pipeline with embeddings      # → Uses rag-pipeline blueprint
/skillchain login form with OAuth             # Full-stack: theming → forms → auth-security
```

## Project Status

- **Current Version:** 0.5.0
- **Skillchain Version:** 2.1.0 (modular architecture)
- **Production Skills:** 76 complete
  - Frontend Skills: 15
  - Backend Skills: 14
  - Infrastructure & Networking: 12
  - Security: 7
  - Developer Productivity: 7
  - DevOps & Platform: 6
  - Data Engineering: 6
  - AI/ML Operations: 4
  - Cloud Patterns: 3
  - FinOps: 2

## Skill Categories

### Frontend Skills (15)

#### UI Foundation Skills
- `theming-components` - Design tokens and theming system

#### UI Data Skills
- `visualizing-data` - Data visualization (24+ chart types)
- `building-tables` - Tables and data grids
- `creating-dashboards` - Dashboard layouts and analytics

#### UI Input Skills
- `building-forms` - Form systems and validation (50+ input types)
- `implementing-search-filter` - Search and filter interfaces

#### UI Interaction Skills
- `building-ai-chat` - AI chat interfaces
- `implementing-drag-drop` - Drag-and-drop functionality
- `providing-feedback` - Feedback and notification systems

#### UI Structure Skills
- `implementing-navigation` - Navigation patterns
- `designing-layouts` - Layout systems and responsive design
- `displaying-timelines` - Timeline and activity components

#### UI Content Skills
- `managing-media` - Media and file management
- `guiding-users` - Onboarding and help systems

#### UI Assembly Skills
- `assembling-components` - Component integration and validation

### Backend Skills (14)

#### Backend Data Skills
- `ingesting-data` - ETL, data ingestion from S3/APIs/files
- `using-relational-databases` - PostgreSQL, MySQL, SQLite
- `using-vector-databases` - Qdrant, Pinecone, pgvector
- `using-timeseries-databases` - ClickHouse, TimescaleDB, InfluxDB
- `using-document-databases` - MongoDB, Firestore, DynamoDB
- `using-graph-databases` - Neo4j, memgraph

#### Backend API Skills
- `implementing-api-patterns` - REST, GraphQL, gRPC, tRPC
- `using-message-queues` - Kafka, RabbitMQ, NATS, Temporal
- `implementing-realtime-sync` - WebSockets, SSE, Y.js

#### Backend Platform Skills
- `implementing-observability` - OpenTelemetry, LGTM stack
- `securing-authentication` - OAuth 2.1, passkeys, RBAC
- `deploying-applications` - Kubernetes, serverless, edge

#### Backend AI Skills
- `ai-data-engineering` - RAG pipelines, embeddings
- `model-serving` - vLLM, BentoML, Ollama

### Additional Skill Categories

See [Skills Overview](./skills/overview.md) for the complete list of all 76 skills organized by category:

- **Infrastructure & Networking** (12) - IaC, Kubernetes, distributed systems, networking
- **Security** (7) - Architecture, compliance, TLS, hardening
- **Developer Productivity** (7) - API design, CLIs, SDKs, debugging
- **DevOps & Platform** (6) - CI/CD, GitOps, testing, platform engineering
- **Data Engineering** (6) - Data architecture, streaming, SQL optimization
- **AI/ML Operations** (4) - MLOps, prompt engineering, LLM evaluation
- **Cloud Patterns** (3) - AWS, GCP, Azure architectural patterns
- **FinOps** (2) - Cost optimization, resource tagging

## Multi-Language Support

All backend skills provide patterns for multiple languages:

| Language | Framework Examples |
|----------|-------------------|
| **Python** | FastAPI, SQLAlchemy, dlt, Polars |
| **TypeScript** | Hono, Prisma, Drizzle, tRPC |
| **Rust** | Axum, sqlx, tokio |
| **Go** | Chi, pgx, sqlc |

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

## Next Steps

- [Installation Guide](./installation.md) - Get started with AI Design Components
- [Skills Overview](./skills/overview.md) - Explore all available skills
- [Skillchain Documentation](./skillchain/overview.md) - Learn about the skillchain framework
- [Creating Skills](./guides/creating-skills.md) - Contribute new skills
- [Skill Validation](./guides/skill-validation.md) - Validate skills with CI or TUI

## Resources

- [Anthropic Skills Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Skills Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/skills)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)

## License

MIT License - See LICENSE for details.

---

**Built with Claude** | Following [Anthropic's Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
