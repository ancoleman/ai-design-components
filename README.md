<p align="center">
  <img src="https://ancoleman.github.io/ai-design-components/img/logo.png" alt="AI Design Components Logo" width="150">
</p>

> Full-stack development skills for AI-assisted development with Claude

[![Version](https://img.shields.io/badge/version-0.5.0-blue.svg)](./VERSION)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-76-purple.svg)](https://ancoleman.github.io/ai-design-components/docs/skills/overview)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-orange.svg)](https://ancoleman.github.io/ai-design-components/)

## What is this?

A collection of **76 production-ready Claude Skills** covering frontend, backend, DevOps, infrastructure, security, cloud, and AI/ML development. Skills provide Claude with domain expertise, decision frameworks, and production-ready code patterns.

## Documentation

**Full documentation: [ancoleman.github.io/ai-design-components](https://ancoleman.github.io/ai-design-components/)**

| Resource | Description |
|----------|-------------|
| [Getting Started](https://ancoleman.github.io/ai-design-components/docs/intro) | Introduction and overview |
| [Installation](https://ancoleman.github.io/ai-design-components/docs/installation) | Setup instructions |
| [Skills Reference](https://ancoleman.github.io/ai-design-components/docs/skills/overview) | All 76 skills documented |
| [Skillchain Guide](https://ancoleman.github.io/ai-design-components/docs/skillchain/overview) | Guided workflow system |

## Quick Start

### Option 1: Skillchain (Recommended)

The guided workflow that chains skills automatically:

```bash
# Install globally
./commands/install-skillchain.sh --global

# Use in Claude Code
/skillchain dashboard with charts and filters
/skillchain REST API with postgres
/skillchain RAG pipeline with embeddings
```

### Option 2: Plugin Marketplace

```bash
# Add marketplace
/plugin marketplace add ancoleman/ai-design-components

# Install skill groups
/plugin install ui-data-skills@ai-design-components
/plugin install backend-api-skills@ai-design-components
```

### Option 3: Clone Repository

```bash
git clone https://github.com/ancoleman/ai-design-components.git
cd ai-design-components
# Skills available when working in this directory
```

## Skill Categories

| Category | Skills | Description |
|----------|--------|-------------|
| **Frontend** | 15 | UI components, forms, data viz, navigation |
| **Backend** | 14 | Databases, APIs, auth, observability |
| **DevOps** | 6 | CI/CD, GitOps, platform engineering |
| **Infrastructure** | 12 | IaC, Kubernetes, networking, distributed systems |
| **Security** | 7 | Architecture, compliance, TLS, hardening |
| **Developer Productivity** | 7 | APIs, CLIs, SDKs, documentation |
| **Data Engineering** | 6 | Architecture, streaming, SQL, secrets |
| **AI/ML** | 4 | MLOps, RAG, prompt engineering |
| **Cloud** | 3 | AWS, GCP, Azure patterns |
| **FinOps** | 2 | Cost optimization, tagging |

See [Skills Overview](https://ancoleman.github.io/ai-design-components/docs/skills/overview) for the complete list.

## Prerequisites

- **Claude Code CLI** - [Install Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- **Context7 MCP** (recommended) - For up-to-date library documentation

## Resources

- [Anthropic Skills Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [LLM Ecosystem Guide](https://ancoleman.github.io/ai-design-components/llm-ecosystem)

## License

MIT License - See [LICENSE](./LICENSE) for details.

---

**[View Full Documentation](https://ancoleman.github.io/ai-design-components/)** | Built following [Anthropic's Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
