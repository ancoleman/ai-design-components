---
sidebar_position: 2
title: Installation
description: How to install and configure AI Design Components
---

# Installation Guide

This guide walks you through installing **AI Design Components** and getting started with the 29 comprehensive skills for full-stack AI-assisted development.

## Prerequisites

Before you begin, ensure you have:

1. **Claude Code installed** - Version 2.0.13 or later (includes plugin support)
2. **Git access** - If using a private repository, ensure authentication is set up
3. **Repository location** - Know where your ai-design-components repo is hosted

## Installation Methods

### Method 1: GitHub Repository (Recommended)

If your marketplace is hosted on GitHub, this is the simplest method.

#### Step 1: Add the Marketplace

Open Claude Code and run:

```bash
/plugin marketplace add ancoleman/ai-design-components
```

#### Step 2: Verify Installation

Check that the marketplace was added successfully:

```bash
/plugin marketplace list
```

You should see `ai-design-components` in the list of available marketplaces.

#### Step 3: Browse Available Skills

Open the plugin menu to see all available skills:

```bash
/plugin
```

This will show you all 11 plugin categories and their 29 individual skills.

### Method 2: Direct Git Repository URL

If you're using GitLab, Bitbucket, or another git hosting service:

```bash
/plugin marketplace add https://github.com/ancoleman/ai-design-components.git
```

### Method 3: Local Development/Testing

For local testing or development of the marketplace:

```bash
/plugin marketplace add ./path/to/ai-design-components
```

Or if you're in a different directory:

```bash
/plugin marketplace add ~/projects/ai-design-components
```

## Installing Individual Plugins

Once the marketplace is added, you can install specific plugin categories:

### Frontend Plugin Categories

```bash
# Foundation (theming)
/plugin install ui-foundation-skills@ai-design-components

# Data visualization, tables, dashboards
/plugin install ui-data-skills@ai-design-components

# Forms and search/filter
/plugin install ui-input-skills@ai-design-components

# AI chat, drag-drop, feedback
/plugin install ui-interaction-skills@ai-design-components

# Navigation, layout, timelines
/plugin install ui-structure-skills@ai-design-components

# Media and onboarding
/plugin install ui-content-skills@ai-design-components

# Component assembly
/plugin install ui-assembly-skills@ai-design-components
```

### Backend Plugin Categories

```bash
# Data ingestion and databases
/plugin install backend-data-skills@ai-design-components

# REST, GraphQL, messaging, realtime
/plugin install backend-api-skills@ai-design-components

# Observability, auth, deployment
/plugin install backend-platform-skills@ai-design-components

# AI/ML data engineering and model serving
/plugin install backend-ai-skills@ai-design-components
```

## Quick Start: The Skillchain Command

The **recommended way** to use AI Design Components is through the `/skillchain` command:

```bash
# Install skillchain globally (available in all projects)
./commands/install-skillchain.sh --global

# Or install to a specific project
./commands/install-skillchain.sh ~/your-project

# Then use it in Claude Code
/skillchain dashboard with charts and postgres backend
/skillchain login form with OAuth authentication
/skillchain RAG pipeline with vector search
```

See [Skillchain Documentation](./skillchain/overview.md) for complete details.

## Using Skills

### Option 1: Skillchain (Recommended)

Use the `/skillchain` command for guided, multi-skill workflows:

```bash
/skillchain help                              # Show all 29 skills
/skillchain sales dashboard with KPIs         # Frontend workflow
/skillchain REST API with postgres and auth   # Backend workflow
/skillchain chat app with real-time sync      # Full-stack workflow
```

### Option 2: Direct Skill Invocation

Skills activate automatically based on context, or you can invoke them directly:

```
"I need to display monthly revenue trends - what visualization should I use?"
→ Automatically uses visualizing-data skill

"Set up a design system with dark mode support"
→ Automatically uses theming-components skill

"Create a REST API with PostgreSQL"
→ Automatically uses api-patterns and databases-relational skills
```

## Automatic Team Installation

For teams working on shared projects, configure automatic marketplace installation in your repository's `.claude/settings.json`:

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

When team members open the project and trust the repository, Claude Code will:
1. Automatically add the ai-design-components marketplace
2. Install the specified plugins
3. Make all skills immediately available

## Managing Your Installation

### Update Marketplace Data
```bash
/plugin marketplace update ai-design-components
```

### List All Marketplaces
```bash
/plugin marketplace list
```

### Remove Marketplace
```bash
/plugin marketplace remove ai-design-components
```

### List Installed Plugins
```bash
/plugin list
```

### Enable/Disable Plugins
```bash
/plugin disable ui-interaction-skills
/plugin enable ui-interaction-skills
```

### Uninstall a Plugin
```bash
/plugin uninstall ui-foundation-skills
```

### Update All Plugins
```bash
/plugin update
```

## Multi-Language Support

All backend skills provide patterns for multiple languages:

| Language | Framework Examples |
|----------|-------------------|
| **Python** | FastAPI, SQLAlchemy, dlt, Polars |
| **TypeScript** | Hono, Prisma, Drizzle, tRPC |
| **Rust** | Axum, sqlx, tokio |
| **Go** | Chi, pgx, sqlc |

## Troubleshooting

### Issue: Marketplace Not Loading

**Solutions:**
1. Verify the repository URL is correct and accessible
2. Ensure `.claude-plugin/marketplace.json` exists in the repo
3. Validate JSON syntax: `claude plugin validate`
4. For private repos, check GitHub authentication: `gh auth status`

### Issue: Skills Not Activating

**Solutions:**
1. Verify plugin is enabled: `/plugin list`
2. Re-enable the plugin
3. Explicitly mention the skill: "Use the visualizing-data skill to..."
4. Check skill files exist at `skills/[skill-name]/SKILL.md`

### Issue: Skillchain Command Not Found

**Solutions:**
1. Ensure skillchain is installed: Check `~/.claude/commands/skillchain.md` or `.claude/commands/skillchain.md`
2. Re-run installation: `./commands/install-skillchain.sh --global`
3. Restart Claude Code

## Next Steps

After installation, explore:

- [Skills Overview](./skills/overview.md) - Learn about all available skills
- [Skillchain Documentation](./skillchain/overview.md) - Master the skillchain workflow
- [Creating Skills](./guides/creating-skills.md) - Contribute new skills
- [Best Practices](./guides/best-practices.md) - Learn skill development best practices

## Resources

- [Anthropic Skills Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Skills Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/skills)

---

**Document Version**: 2.0
**Last Updated**: December 2025
