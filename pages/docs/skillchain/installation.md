---
sidebar_position: 2
title: Installation
description: How to install skillchain globally or per-project
---

# Installing Skillchain

Skillchain can be installed globally (for all projects) or per-project (for team sharing). Both installation methods use the provided installation script.

## Prerequisites

- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)
- Bash shell (macOS, Linux, or WSL on Windows)
- Git (to clone the repository)

## Option 1: Global Installation (Recommended)

Install once, use in all your projects:

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-design-components.git
cd ai-design-components

# Install globally
./commands/install-skillchain.sh --global
```

This installs to `~/.claude/commands/skillchain/`, making the command available in **every project** you work on.

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
/skillchain help
```

You should see the skillchain help guide with all 29 available skills.

## Option 2: Project-Specific Installation

Install for a single project (can be committed and shared with team):

```bash
# Navigate to your project
cd ~/my-project

# Clone or copy the ai-design-components repo
git clone https://github.com/yourusername/ai-design-components.git

# Install to current project
./ai-design-components/commands/install-skillchain.sh
```

Or specify a target project:

```bash
# Install to a specific project
cd ai-design-components
./commands/install-skillchain.sh ~/path/to/your/project
```

This installs to `&lt;project>/.claude/commands/skillchain/`, making it available only in that project.

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

# Commit
git commit -m "Add skillchain v2.1 for team collaboration"
```

## Installation Locations

Claude Code looks for commands in two locations:

| Location | Scope | Use Case |
|----------|-------|----------|
| `~/.claude/commands/` | Global (your user) | Personal commands available everywhere |
| `.claude/commands/` | Project-specific | Team commands committed to repo |

**Resolution order:** Project commands override global commands if both exist.

## What Gets Installed

The installation script copies the complete skillchain structure:

```
.claude/commands/skillchain/
├── skillchain.md           # Router (main entry point)
├── _registry.yaml          # 29 skill definitions
├── _help.md                # Help content
├── _shared/                # Shared resources (9 files)
│   ├── theming-rules.md
│   ├── execution-flow.md
│   ├── preferences.md
│   ├── parallel-loading.md
│   ├── changelog.md
│   └── compatibility.md
├── categories/             # Orchestrators (4 files)
│   ├── frontend.md
│   ├── backend.md
│   ├── fullstack.md
│   └── ai-ml.md
└── blueprints/             # Pre-configured templates (3 files)
    ├── dashboard.md
    ├── crud-api.md
    └── rag-pipeline.md
```

Total: 19 files, approximately 3,000 lines of optimized guidance.

## Updating

To update an existing installation, simply run the installer again:

```bash
# Update global installation
cd ai-design-components
git pull  # Get latest changes
./commands/install-skillchain.sh --global

# Update project installation
./commands/install-skillchain.sh ~/your-project
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

# Remove project installation
rm -rf .claude/commands/skillchain

# Optional: Remove saved preferences
rm ~/.claude/skillchain-prefs.yaml
```

## Troubleshooting

### Command Not Found

If `/skillchain` doesn't work:

1. **Check installation location:**
   ```bash
   ls ~/.claude/commands/skillchain/skillchain.md  # Global
   ls .claude/commands/skillchain/skillchain.md    # Project
   ```

2. **Verify Claude Code is running:**
   ```bash
   claude --version
   ```

3. **Restart Claude Code:**
   Exit and restart the Claude Code CLI.

### Permission Denied

If you get permission errors:

```bash
# Make installer executable
chmod +x commands/install-skillchain.sh

# Run with proper permissions
./commands/install-skillchain.sh --global
```

### Wrong Version Installed

Check which version is active:

```bash
# View registry version
cat ~/.claude/commands/skillchain/_registry.yaml | head -5

# Should show:
# registry_version: "2.1.0"
# version: "2.0.0"
# last_updated: "2025-12-02"
```

### Skills Not Loading

If skills aren't triggering:

1. **Check skill installation:**
   The skills themselves must be installed separately from skillchain. See [Skills Installation](../skills/overview.md).

2. **Verify skill invocation paths:**
   Skills are referenced by their full invocation name (e.g., `ui-foundation-skills:theming-components`).

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
- [Explore blueprints](./blueprints.md) for fast-track presets
- [Understand architecture](./architecture.md) and how it works internally
