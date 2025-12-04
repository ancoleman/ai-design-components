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

Built following [Anthropic's official Skills best practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills), these skills use progressive disclosure to minimize context usage while maximizing Claude's effectiveness.

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

### Master Plan Skills (47) - Ready for Implementation

These skills have comprehensive `init.md` master plans with research, decision frameworks, and implementation roadmaps.

<details>
<summary><b>🏗️ Infrastructure & Networking (12 skills)</b></summary>

- `infrastructure-as-code` - Terraform, Pulumi, CDK patterns
- `kubernetes-operations` - K8s management, Helm, operators
- `designing-distributed-systems` - CAP theorem, architecture patterns
- `configuration-management` - Ansible, Chef, Puppet
- `network-architecture` - VPC design, subnets, routing
- `load-balancing-patterns` - ALB, NLB, service mesh LB
- `dns-management` - Route53, CloudDNS, record types
- `service-mesh` - Istio, Linkerd, Cilium
- `disaster-recovery` - RPO/RTO, backup strategies
- `linux-administration` - System management, troubleshooting
- `shell-scripting` - Bash/Zsh patterns
- `configuring-nginx` - Reverse proxy, SSL, performance
</details>

<details>
<summary><b>🔒 Security (6 skills)</b></summary>

- `security-architecture` - Zero trust, defense in depth
- `compliance-frameworks` - SOC2, ISO27001, HIPAA, PCI-DSS
- `vulnerability-management` - Scanning, remediation workflows
- `siem-logging` - Security monitoring, alerting
- `implementing-tls` - Certificate management, mTLS
- `configuring-firewalls` - Network security rules
</details>

<details>
<summary><b>👨‍💻 Developer Productivity (7 skills)</b></summary>

- `api-design-principles` - REST, GraphQL design patterns
- `building-clis` - Python, Go, Rust CLI frameworks 🌐
- `sdk-design` - Client library patterns 🌐
- `documentation-generation` - API docs, code documentation
- `debugging-techniques` - Profiling, troubleshooting 🌐
- `git-workflows` - Branching strategies, hooks
- `writing-github-actions` - CI/CD workflow authoring
</details>

<details>
<summary><b>⚙️ DevOps & Platform (6 skills)</b></summary>

- `building-ci-pipelines` - GitHub Actions, GitLab CI, Jenkins
- `gitops-workflows` - ArgoCD, Flux patterns
- `testing-strategies` - Unit, integration, E2E testing 🌐
- `platform-engineering` - IDP, Backstage, developer experience
- `incident-management` - On-call, post-mortems, SRE
- `writing-dockerfiles` - Multi-stage, security hardening
</details>

<details>
<summary><b>📊 Data & Analytics (6 skills)</b></summary>

- `data-architecture` - Data mesh, lakehouse, medallion
- `streaming-data` - Kafka, Flink, event streaming 🌐
- `data-transformation` - dbt, ETL/ELT patterns 🌐
- `sql-optimization` - Query tuning, indexing
- `secret-management` - Vault, secrets rotation
- `performance-engineering` - Profiling, optimization
</details>

<details>
<summary><b>🤖 AI/ML Operations (4 skills)</b></summary>

- `mlops-patterns` - MLflow, experiment tracking, feature stores
- `prompt-engineering` - LLM prompting, chain-of-thought
- `llm-evaluation` - RAGAS, benchmarks, safety testing
- `embedding-optimization` - Chunking strategies, model selection
</details>

<details>
<summary><b>☁️ Cloud Patterns (3 skills)</b></summary>

- `aws-patterns` - Well-Architected, service selection
- `gcp-patterns` - BigQuery, Vertex AI, GKE
- `azure-patterns` - Container Apps, Azure OpenAI
</details>

<details>
<summary><b>💰 FinOps (3 skills)</b></summary>

- `cost-optimization` - FinOps practices, rightsizing
- `resource-tagging` - Tag governance, enforcement
- `security-hardening` - CIS benchmarks, hardening
</details>

🌐 = Multi-language support (TypeScript, Python, Go, Rust)

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
