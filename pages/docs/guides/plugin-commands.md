---
sidebar_position: 6
title: Plugin Commands Reference
description: Complete CLI reference for managing the AI Design Components marketplace and plugins
tags: [installation, cli, plugins, reference]
---

# Plugin Commands Reference

Complete reference for managing the AI Design Components marketplace and plugins using Claude Code CLI.

:::tip No Cloning Required
Claude Code handles fetching from GitHub automatically. Just run the commands below.
:::

## Quick Start

```bash
# 1. Add the marketplace (Claude fetches from GitHub automatically)
claude plugin marketplace add ancoleman/ai-design-components

# 2. Install plugins you want
claude plugin install infrastructure-skills@ai-design-components
claude plugin install devops-skills@ai-design-components

# 3. Restart Claude Code to load new plugins
```

## Marketplace Commands

### Add Marketplace

**From GitHub (recommended):**
```bash
claude plugin marketplace add ancoleman/ai-design-components
```

**From local directory (for development):**
```bash
claude plugin marketplace add /path/to/ai-design-components
claude plugin marketplace add ./
```

### List Marketplaces

```bash
claude plugin marketplace list
```

### Update Marketplace

```bash
claude plugin marketplace update ai-design-components   # Update specific
claude plugin marketplace update                        # Update all
```

### Remove Marketplace

```bash
claude plugin marketplace rm ai-design-components
# or
claude plugin marketplace remove ai-design-components
```

## Plugin Commands

### Install Plugin

```bash
claude plugin install <plugin-name>@ai-design-components
```

**Examples:**
```bash
# Frontend plugins
claude plugin install ui-foundation-skills@ai-design-components
claude plugin install ui-data-skills@ai-design-components
claude plugin install ui-input-skills@ai-design-components
claude plugin install ui-interaction-skills@ai-design-components
claude plugin install ui-structure-skills@ai-design-components
claude plugin install ui-content-skills@ai-design-components
claude plugin install ui-assembly-skills@ai-design-components

# Backend plugins
claude plugin install backend-data-skills@ai-design-components
claude plugin install backend-api-skills@ai-design-components
claude plugin install backend-platform-skills@ai-design-components
claude plugin install backend-ai-skills@ai-design-components

# DevOps & Infrastructure
claude plugin install devops-skills@ai-design-components
claude plugin install infrastructure-skills@ai-design-components

# Security
claude plugin install security-skills@ai-design-components

# Developer Productivity
claude plugin install developer-productivity-skills@ai-design-components

# Data Engineering
claude plugin install data-engineering-skills@ai-design-components

# AI/ML
claude plugin install ai-ml-skills@ai-design-components

# Cloud Providers
claude plugin install cloud-provider-skills@ai-design-components

# FinOps
claude plugin install finops-skills@ai-design-components
```

### Uninstall Plugin

```bash
claude plugin uninstall <plugin-name>
# or
claude plugin remove <plugin-name>
```

### Enable/Disable Plugin

```bash
claude plugin enable <plugin-name>
claude plugin disable <plugin-name>
```

## Validation

### Validate Marketplace

```bash
claude plugin validate .claude-plugin/marketplace.json
```

### Validate Plugin/Skill

```bash
claude plugin validate ./skills/theming-components
```

## Available Plugins

| Plugin | Skills | Description |
|--------|--------|-------------|
| `ui-foundation-skills` | 1 | Design tokens and theming |
| `ui-data-skills` | 3 | Data viz, tables, dashboards |
| `ui-input-skills` | 2 | Forms, search/filter |
| `ui-interaction-skills` | 3 | AI chat, drag-drop, feedback |
| `ui-structure-skills` | 3 | Navigation, layouts, timelines |
| `ui-content-skills` | 2 | Media, onboarding |
| `ui-assembly-skills` | 1 | Component assembly |
| `backend-data-skills` | 6 | All database types |
| `backend-api-skills` | 3 | API patterns, queues, realtime |
| `backend-platform-skills` | 3 | Observability, auth, deployment |
| `backend-ai-skills` | 2 | AI data engineering, model serving |
| `devops-skills` | 6 | CI/CD, GitOps, testing |
| `infrastructure-skills` | 12 | Kubernetes, IaC, networking |
| `security-skills` | 7 | Security architecture, compliance |
| `developer-productivity-skills` | 7 | API design, CLI, SDK |
| `data-engineering-skills` | 6 | Data pipelines, SQL |
| `ai-ml-skills` | 4 | MLOps, prompt engineering |
| `cloud-provider-skills` | 3 | AWS, GCP, Azure |
| `finops-skills` | 2 | Cost optimization, tagging |

**Total: 76 skills across 19 plugins**

## Install All Plugins

To install all plugins from the marketplace:

```bash
# Add marketplace first
claude plugin marketplace add ancoleman/ai-design-components

# Install all 19 plugins
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

## Uninstall All Plugins

```bash
claude plugin uninstall ui-foundation-skills
claude plugin uninstall ui-data-skills
claude plugin uninstall ui-input-skills
claude plugin uninstall ui-interaction-skills
claude plugin uninstall ui-structure-skills
claude plugin uninstall ui-content-skills
claude plugin uninstall ui-assembly-skills
claude plugin uninstall backend-data-skills
claude plugin uninstall backend-api-skills
claude plugin uninstall backend-platform-skills
claude plugin uninstall backend-ai-skills
claude plugin uninstall devops-skills
claude plugin uninstall infrastructure-skills
claude plugin uninstall security-skills
claude plugin uninstall developer-productivity-skills
claude plugin uninstall data-engineering-skills
claude plugin uninstall ai-ml-skills
claude plugin uninstall cloud-provider-skills
claude plugin uninstall finops-skills

# Then remove marketplace
claude plugin marketplace rm ai-design-components
```

## settings.json Configuration

For automatic installation when entering a project, add to `.claude/settings.json`:

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
  "enabledPlugins": {
    "ui-foundation-skills@ai-design-components": true,
    "ui-data-skills@ai-design-components": true,
    "infrastructure-skills@ai-design-components": true
  }
}
```

## Troubleshooting

### Marketplace not found

```bash
# Check if marketplace is added
claude plugin marketplace list

# Re-add if missing
claude plugin marketplace add ancoleman/ai-design-components
```

### Marketplace already installed

```bash
# Update existing marketplace
claude plugin marketplace update ai-design-components

# Or remove and re-add
claude plugin marketplace rm ai-design-components
claude plugin marketplace add ancoleman/ai-design-components
```

### Plugin already installed

This is informational - the plugin is ready to use:
```
Plugin '<name>@ai-design-components' is already installed.
```

### Restart required

After installing plugins, restart Claude Code to load them:
```
✓ Installed X plugins. Restart Claude Code to load new plugins.
```
