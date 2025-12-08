---
sidebar_position: 2
title: Installation
description: How to install and configure AI Design Components
---

# Installation Guide

This guide walks you through installing **AI Design Components** and getting started with 76 production-ready skills for full-stack AI-assisted development.

## Prerequisites

Before you begin, ensure you have:

1. **Claude Code installed** - Version 2.0.13 or later (includes plugin support)
2. **Git** - For cloning the repository
3. **GitHub access** - If using a private repository, ensure authentication is set up

## Quick Start (Recommended)

The fastest way to get started is with the interactive installer:

```bash
# Clone the repository
git clone https://github.com/ancoleman/ai-design-components.git
cd ai-design-components

# Run the interactive installer
./install.sh
```

Select **Option 1 (Full Install)** to install everything: marketplace, all 19 plugins, and the `/skillchain:start` command.

## Interactive Installer Options

The installer provides a comprehensive menu for managing your installation:

```
What would you like to do?

  Install:
    1) Full Install - Marketplace + all plugins + /skillchain command
    2) Install Skillchain - Install /skillchain:start command globally
    3) Marketplace + Plugins - Add marketplace + install all plugins
    4) Marketplace Only - Just add the marketplace
    5) Select Plugins - Choose which plugins to install

  Update:
    6) Update Skillchain - Refresh /skillchain to latest version
    7) Update Marketplace - Refresh marketplace plugins

  Uninstall:
    8) Uninstall Skillchain - Remove /skillchain commands and data
    9) Uninstall Plugins - Remove marketplace and all plugins
    10) Uninstall Everything - Remove all (skillchain + plugins + marketplace)

  Info:
    11) List Plugins - Show available plugins
    0) Help - Show all commands
```

### Option Descriptions

| Option | What It Does |
|--------|--------------|
| **1) Full Install** | Complete setup: adds marketplace, installs all 19 plugin groups (76 skills), and installs `/skillchain:start` globally |
| **2) Install Skillchain** | Installs only the `/skillchain:start` command to `~/.claude/commands/` |
| **3) Marketplace + Plugins** | Adds marketplace and installs all plugins, but not skillchain |
| **4) Marketplace Only** | Just adds the marketplace - you can install plugins later |
| **5) Select Plugins** | Shows available plugins so you can install specific ones |
| **6) Update Skillchain** | Refreshes skillchain commands and data to the latest version |
| **7) Update Marketplace** | Refreshes marketplace plugin definitions |
| **8-10) Uninstall** | Various removal options |

## Command-Line Installation

For scripting or CI/CD, use direct commands:

```bash
# Full marketplace + plugins installation
./install.sh marketplace add
./install.sh plugins install-all

# Skillchain commands
./install.sh commands               # Install skillchain
./install.sh commands update        # Update to latest version
./install.sh commands uninstall     # Remove skillchain

# Individual plugin installation
./install.sh plugins install ui-data-skills
./install.sh plugins install backend-api-skills

# Complete removal
./install.sh uninstall-all
```

## What Gets Installed

### Skillchain Installation

When you install skillchain (options 1 or 2), files are installed to:

```
~/.claude/
├── commands/
│   └── skillchain/              # Exposed as /skillchain:* commands
│       ├── start.md             # /skillchain:start
│       ├── help.md              # /skillchain:help
│       ├── blueprints/          # /skillchain:blueprints:*
│       └── categories/          # /skillchain:categories:*
│
└── skillchain-data/             # Data files (not exposed as commands)
    ├── registries/              # 10 domain-specific skill registries
    └── shared/                  # Common resources
```

### Plugin Installation

The marketplace includes 19 plugin groups containing 76 skills:

| Plugin Group | Skills | Domain |
|--------------|--------|--------|
| ui-foundation-skills | 1 | Frontend theming |
| ui-data-skills | 3 | Data visualization, tables, dashboards |
| ui-input-skills | 2 | Forms, search/filter |
| ui-interaction-skills | 3 | AI chat, drag-drop, feedback |
| ui-structure-skills | 3 | Navigation, layouts, timelines |
| ui-content-skills | 2 | Media, onboarding |
| ui-assembly-skills | 1 | Component integration |
| backend-data-skills | 6 | All database types |
| backend-api-skills | 3 | API patterns, queues, realtime |
| backend-platform-skills | 3 | Observability, auth, deployment |
| backend-ai-skills | 2 | AI data engineering, model serving |
| devops-skills | 6 | CI/CD, GitOps, testing |
| infrastructure-skills | 12 | Kubernetes, IaC, networking |
| security-skills | 7 | Security architecture, compliance |
| developer-productivity-skills | 7 | API design, CLIs, SDKs |
| data-engineering-skills | 6 | Data pipelines, SQL optimization |
| ai-ml-skills | 4 | MLOps, prompt engineering |
| cloud-provider-skills | 3 | AWS, GCP, Azure |
| finops-skills | 2 | Cost optimization, tagging |

## Alternative: Manual Claude Code Commands

If you prefer to use Claude Code commands directly instead of the installer:

### Add Marketplace

```bash
/plugin marketplace add ancoleman/ai-design-components
```

### Install All Plugins

```bash
# Frontend plugins
/plugin install ui-foundation-skills@ai-design-components
/plugin install ui-data-skills@ai-design-components
/plugin install ui-input-skills@ai-design-components
/plugin install ui-interaction-skills@ai-design-components
/plugin install ui-structure-skills@ai-design-components
/plugin install ui-content-skills@ai-design-components
/plugin install ui-assembly-skills@ai-design-components

# Backend plugins
/plugin install backend-data-skills@ai-design-components
/plugin install backend-api-skills@ai-design-components
/plugin install backend-platform-skills@ai-design-components
/plugin install backend-ai-skills@ai-design-components

# DevOps & Infrastructure
/plugin install devops-skills@ai-design-components
/plugin install infrastructure-skills@ai-design-components
/plugin install security-skills@ai-design-components

# Developer & Data
/plugin install developer-productivity-skills@ai-design-components
/plugin install data-engineering-skills@ai-design-components

# AI/ML & Cloud
/plugin install ai-ml-skills@ai-design-components
/plugin install cloud-provider-skills@ai-design-components
/plugin install finops-skills@ai-design-components
```

## Updating Your Installation

### Update Skillchain

To get the latest skillchain commands, blueprints, and registries:

```bash
# Interactive
./install.sh
# Select option 6) Update Skillchain

# Or command-line
./install.sh commands update
```

### Update Marketplace Plugins

To refresh marketplace plugin definitions:

```bash
# Interactive
./install.sh
# Select option 7) Update Marketplace

# Or command-line
/plugin marketplace update ai-design-components
```

## Uninstalling

### Remove Skillchain Only

Removes `/skillchain:start` commands and data, keeps plugins:

```bash
# Interactive - select option 8
./install.sh

# Or command-line
./install.sh commands uninstall
```

This removes:
- `~/.claude/commands/skillchain/`
- `~/.claude/skillchain-data/`

### Remove Plugins Only

Removes all plugins and marketplace, keeps skillchain:

```bash
# Interactive - select option 9
./install.sh

# Or command-line
./install.sh plugins uninstall-all
./install.sh marketplace remove
```

### Remove Everything

Complete removal of all AI Design Components:

```bash
# Interactive - select option 10
./install.sh

# Or command-line
./install.sh uninstall-all
```

## Verifying Installation

### Check Skillchain

After installation, verify skillchain works:

```bash
# In Claude Code
/skillchain:help
```

You should see the help menu with all 76 skills listed.

### Check Plugins

```bash
# In Claude Code
/plugin list
```

You should see all installed plugin groups.

### Check Marketplace

```bash
# In Claude Code
/plugin marketplace list
```

You should see `ai-design-components` in the list.

## Team Installation

For teams working on shared projects, configure automatic installation in your repository's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "ai-design-components": {
      "source": {
        "source": "github",
        "repo": "ancoleman/ai-design-components"
      }
    }
  },
  "enabledPlugins": [
    "ui-foundation-skills@ai-design-components",
    "ui-data-skills@ai-design-components",
    "backend-data-skills@ai-design-components",
    "backend-api-skills@ai-design-components"
  ]
}
```

When team members open the project and trust the repository, Claude Code will automatically install the specified plugins.

## Troubleshooting

### Skillchain Command Not Found

**Symptoms:** `/skillchain:start` doesn't work

**Solutions:**
1. Check installation: `ls ~/.claude/commands/skillchain/`
2. Re-run installer: `./install.sh commands`
3. Restart Claude Code

### Marketplace Not Loading

**Symptoms:** Can't add marketplace or plugins fail to install

**Solutions:**
1. Verify repository URL is accessible
2. Check `.claude-plugin/marketplace.json` exists
3. For private repos, check GitHub authentication: `gh auth status`

### Skills Not Activating

**Symptoms:** Skills don't trigger automatically

**Solutions:**
1. Verify plugin is installed: `/plugin list`
2. Re-enable the plugin
3. Explicitly invoke: "Use the visualizing-data skill to..."

### Update Issues

**Symptoms:** Updates don't seem to take effect

**Solutions:**
1. Restart Claude Code after updating
2. Try uninstall then reinstall: `./install.sh commands uninstall && ./install.sh commands`

## Multi-Language Support

All backend skills provide patterns for multiple languages:

| Language | Framework Examples |
|----------|-------------------|
| **Python** | FastAPI, SQLAlchemy, dlt, Polars |
| **TypeScript** | Hono, Prisma, Drizzle, tRPC |
| **Rust** | Axum, sqlx, tokio |
| **Go** | Chi, pgx, sqlc |

## Next Steps

After installation:

- [Skills Overview](./skills/overview.md) - Explore all 76 available skills
- [Skillchain Documentation](./skillchain/overview.md) - Learn the skillchain workflow
- [Creating Skills](./guides/creating-skills.md) - Contribute new skills
- [Skill Validation](./guides/skill-validation.md) - Validate skills with CI or TUI

## Resources

- [Anthropic Skills Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Skills Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/skills)

---

**Document Version**: 3.0
**Last Updated**: December 2025
