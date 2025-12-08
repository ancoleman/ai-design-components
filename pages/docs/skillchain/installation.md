---
sidebar_position: 2
title: Installation
description: How to install skillchain v3.0 globally or per-project
---

# Installing Skillchain

Skillchain v3.0 can be installed globally (for all projects) or per-project (for team sharing). Both installation methods use the provided installation script.

## Prerequisites

- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)
- Bash shell (macOS, Linux, or WSL on Windows)
- Git (to clone the repository)

## Option 1: Global Installation (Recommended)

Install once, use in all your projects:

```bash
# Clone the repository
git clone https://github.com/ancoleman/ai-design-components.git
cd ai-design-components

# Install globally
./install.sh
```

This installs to:
- `~/.claude/commands/skillchain/` - Commands (exposed as `/skillchain:*`)
- `~/.claude/skillchain-data/` - Data (registries, shared resources)

### Benefits of Global Installation

- **Available everywhere**: Works in any project directory
- **Personal setup**: Your preferences follow you across projects
- **Easy updates**: Update once, affects all projects
- **No repo clutter**: Doesn't add files to project repositories

### Verification

After installation, verify it works:

```bash
# Navigate to any project
cd ~/my-project

# Start Claude Code
claude

# Test skillchain
/skillchain:start help
```

You should see the skillchain help guide with all 76 available skills across 10 domains.

## Option 2: Project-Specific Installation

Install for a single project (can be committed and shared with team):

```bash
# Navigate to your project
cd ~/my-project

# Clone or copy the ai-design-components repo
git clone https://github.com/ancoleman/ai-design-components.git

# Install to current project
./ai-design-components/install.sh --project
```

Or specify a target project:

```bash
# Install to a specific project
cd ai-design-components
./install.sh --project ~/path/to/your/project
```

This installs to:
- `<project>/.claude/commands/skillchain/` - Commands
- `<project>/.claude/skillchain-data/` - Data

### Benefits of Project Installation

- **Team sharing**: Commit `.claude/` to git for team access
- **Version pinning**: Each project can use a different skillchain version
- **Project defaults**: Project-specific preferences
- **Portability**: Works offline without global setup

### Adding to Git

If you want to commit skillchain to your project repository:

```bash
# Ensure .claude directory is tracked
git add .claude/commands/skillchain/
git add .claude/skillchain-data/

# Commit
git commit -m "Add skillchain v3.0 for team collaboration"
```

## Installation Locations

Claude Code looks for commands in two locations:

| Location | Scope | Use Case |
|----------|-------|----------|
| `~/.claude/commands/` | Global (your user) | Personal commands available everywhere |
| `.claude/commands/` | Project-specific | Team commands committed to repo |

**Resolution order:** Project commands override global commands if both exist.

## What Gets Installed

The installation script installs the skillchain in a **separated structure**:

### Commands Directory (exposed as slash commands)

```
~/.claude/commands/skillchain/
├── start.md                    # /skillchain:start (main entry)
├── help.md                     # /skillchain:help
│
├── blueprints/                 # 12 blueprints
│   ├── dashboard.md
│   ├── crud-api.md
│   ├── api-first.md
│   ├── rag-pipeline.md
│   ├── ml-pipeline.md
│   ├── ci-cd.md
│   ├── k8s.md
│   ├── cloud.md
│   ├── observability.md
│   ├── security.md
│   ├── cost.md
│   └── data-pipeline.md
│
└── categories/                 # 12 orchestrators
    ├── frontend.md
    ├── backend.md
    ├── devops.md
    ├── infrastructure.md
    ├── security.md
    ├── developer.md
    ├── data.md
    ├── ai-ml.md
    ├── cloud.md
    ├── finops.md
    ├── fullstack.md
    └── multi-domain.md
```

### Data Directory (NOT exposed as commands)

```
~/.claude/skillchain-data/
├── registries/                 # 11 registry files
│   ├── _index.yaml             # Registry index (76 skills)
│   ├── frontend.yaml           # 15 skills
│   ├── backend.yaml            # 14 skills
│   ├── devops.yaml             # 6 skills
│   ├── infrastructure.yaml     # 12 skills
│   ├── security.yaml           # 7 skills
│   ├── developer.yaml          # 7 skills
│   ├── data.yaml               # 6 skills
│   ├── ai-ml.yaml              # 4 skills
│   ├── cloud.yaml              # 3 skills
│   └── finops.yaml             # 2 skills
│
└── shared/                     # Shared resources
    ├── preferences.md
    ├── theming-rules.md
    └── execution-flow.md
```

**Why two directories?** Every `.md` file in `commands/` becomes a slash command. The separated structure prevents internal files from appearing as unwanted commands like `/skillchain:_registry`.

## Updating

To update an existing installation, simply run the installer again:

```bash
# Update global installation
cd ai-design-components
git pull  # Get latest changes
./install.sh

# Update project installation
./install.sh --project ~/your-project
```

The installer will:
1. Detect existing installation
2. Backup current files (if desired)
3. Replace with new version
4. Preserve your user preferences (`~/.claude/skillchain-prefs.yaml`)

## Uninstalling

To remove skillchain:

```bash
# Remove global installation
rm -rf ~/.claude/commands/skillchain
rm -rf ~/.claude/skillchain-data

# Remove project installation
rm -rf .claude/commands/skillchain
rm -rf .claude/skillchain-data

# Optional: Remove saved preferences
rm ~/.claude/skillchain-prefs.yaml
```

## Troubleshooting

### Command Not Found

If `/skillchain:start` doesn't work:

1. **Check installation location:**
   ```bash
   ls ~/.claude/commands/skillchain/start.md     # Global
   ls .claude/commands/skillchain/start.md       # Project
   ```

2. **Verify data directory exists:**
   ```bash
   ls ~/.claude/skillchain-data/registries/      # Global
   ls .claude/skillchain-data/registries/        # Project
   ```

3. **Verify Claude Code is running:**
   ```bash
   claude --version
   ```

4. **Restart Claude Code:**
   Exit and restart the Claude Code CLI.

### Permission Denied

If you get permission errors:

```bash
# Make installer executable
chmod +x install.sh

# Run with proper permissions
./install.sh
```

### Wrong Version Installed

Check which version is active:

```bash
# View registry version
cat ~/.claude/skillchain-data/registries/_index.yaml | head -5

# Should show:
# version: "3.0.0"
# total_skills: 76
```

### Skills Not Loading

If skills aren't triggering:

1. **Check skill installation:**
   The skills themselves must be installed separately from skillchain. See [Skills Installation](../skills/overview.md).

2. **Verify skill invocation paths:**
   Skills are referenced by their full invocation name (e.g., `frontend-skills:theming-components`).

## Configuration

After installation, skillchain works immediately with default settings. However, you can customize:

### User Preferences

On first run, skillchain will ask if you want to save preferences:

```yaml
# ~/.claude/skillchain-prefs.yaml
global:
  theme:
    color_scheme: "blue-gray"
    theme_modes: ["light", "dark"]
  frameworks:
    frontend: "react"
    backend: "fastapi"
    database: "postgres"
```

### Project-Specific Defaults

For project installations, you can create project-specific defaults:

```yaml
# .claude/skillchain-project.yaml
project:
  name: "my-app"
  defaults:
    theme:
      color_scheme: "brand-colors"
    frameworks:
      frontend: "svelte"
```

These override global preferences when working in that project.

## Next Steps

- [Learn usage patterns](./usage.md) with examples
- [Explore blueprints](./blueprints.md) for fast-track presets (12 available)
- [Understand architecture](./architecture.md) and how it works internally
