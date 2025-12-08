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

### Option 1: Installer Script (Recommended)

The interactive installer handles everything - skills, skillchain, and plugins:

```bash
git clone https://github.com/ancoleman/ai-design-components.git
cd ai-design-components
./install.sh
```

The installer provides:
- **Interactive menu** for choosing what to install
- **Skillchain v3.0** with 76 skills across 10 domains
- **Plugin installation** for all 19 plugin groups
- **Automatic setup** of commands and data directories

```bash
# Installer commands
./install.sh                    # Interactive mode
./install.sh plugins list       # See all available plugins
./install.sh plugins install    # Install all plugins
./install.sh skillchain         # Install skillchain only
```

### Option 2: Manual Plugin Installation

If you prefer using Claude's plugin commands directly:

```bash
# Add marketplace
claude plugin marketplace add ancoleman/ai-design-components

# Install all 19 plugins (76 skills)
claude plugin install ui-foundation-skills@ai-design-components
claude plugin install ui-data-skills@ai-design-components
claude plugin install ui-input-skills@ai-design-components
claude plugin install ui-interaction-skills@ai-design-components
claude plugin install ui-structure-skills@ai-design-components
claude plugin install ui-content-skills@ai-design-components
claude plugin install ui-assembly-skills@ai-design-components
claude plugin install backend-data-skills@ai-design-components
claude plugin install backend-api-skills@ai-design-components
claude plugin install backend-platform-skills@ai-design-components
claude plugin install backend-ai-skills@ai-design-components
claude plugin install devops-skills@ai-design-components
claude plugin install infrastructure-skills@ai-design-components
claude plugin install security-skills@ai-design-components
claude plugin install developer-productivity-skills@ai-design-components
claude plugin install data-engineering-skills@ai-design-components
claude plugin install ai-ml-skills@ai-design-components
claude plugin install cloud-provider-skills@ai-design-components
claude plugin install finops-skills@ai-design-components
```

### Option 3: Selective Installation

Install only what you need:

```bash
# Add marketplace first
claude plugin marketplace add ancoleman/ai-design-components

# Install specific plugin groups
claude plugin install infrastructure-skills@ai-design-components
claude plugin install devops-skills@ai-design-components
claude plugin install security-skills@ai-design-components
```

## Plugin Commands Reference

```bash
# Marketplace
claude plugin marketplace add ancoleman/ai-design-components    # Add
claude plugin marketplace rm ai-design-components               # Remove
claude plugin marketplace list                                  # List all
claude plugin marketplace update ai-design-components           # Update

# Plugins
claude plugin install <plugin>@ai-design-components             # Install
claude plugin uninstall <plugin>                                # Uninstall

# Validation
claude plugin validate .claude-plugin/marketplace.json          # Validate
```

## Using Skillchain

Once installed, use the `/skillchain:start` command for guided workflows:

```bash
/skillchain:start dashboard with charts and filters
/skillchain:start REST API with postgres
/skillchain:start kubernetes with monitoring
/skillchain:start RAG pipeline with embeddings
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

- [Plugin Commands Reference](https://ancoleman.github.io/ai-design-components/docs/guides/plugin-commands) - Complete CLI reference for marketplace/plugin management
- [Anthropic Skills Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [LLM Ecosystem Guide](https://ancoleman.github.io/ai-design-components/llm-ecosystem)

## License

MIT License - See [LICENSE](./LICENSE) for details.

---

**[View Full Documentation](https://ancoleman.github.io/ai-design-components/)** | Built following [Anthropic's Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
