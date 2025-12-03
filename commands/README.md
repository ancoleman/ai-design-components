# Claude Code Commands

This directory contains slash commands for Claude Code that provide guided workflows for AI Design Components.

## The Skillchain Command

The `/skillchain` command is the **recommended entry point** for using AI Design Components. Instead of relying on prompt formulation to trigger individual skills, skillchain provides a guided, step-by-step workflow.

### Why Use Skillchain?

| Traditional Approach | Skillchain Approach |
|---------------------|---------------------|
| User must know skill names | Describe what you want to build |
| User triggers skills individually | Skills chain automatically |
| Easy to miss required skills | Correct skill order enforced |
| No theming consistency | Theming always applied first |
| Manual component assembly | Assembly skill runs at end |

**Example:**

Traditional (requires knowledge):
```
"Use the theming-components skill, then designing-layouts,
then creating-dashboards, then visualizing-data..."
```

Skillchain (just describe your goal):
```
/skillchain sales dashboard with revenue charts
```

## Installation

### Option 1: Global Installation (Recommended)

Install once, use in all your projects:

```bash
./commands/install-skillchain.sh --global
```

This installs to `~/.claude/commands/skillchain.md`, making the command available in **every project** you work on.

### Option 2: Project-Specific Installation

Install for a single project (can be committed and shared with team):

```bash
# Install to current directory
./commands/install-skillchain.sh

# Or install to a specific project
./commands/install-skillchain.sh ~/path/to/your/project
```

This installs to `<project>/.claude/commands/skillchain.md`, making it available only in that project.

### Option 3: Manual Installation

Copy `skillchain.md` directly:

```bash
# Global (all projects, your user only)
mkdir -p ~/.claude/commands
cp commands/skillchain.md ~/.claude/commands/

# Project-specific (shareable with team)
mkdir -p ~/your-project/.claude/commands
cp commands/skillchain.md ~/your-project/.claude/commands/
```

## Installation Locations

Claude Code looks for commands in two locations:

| Location | Scope | Use Case |
|----------|-------|----------|
| `~/.claude/commands/` | Global (your user) | Personal commands available everywhere |
| `.claude/commands/` | Project-specific | Team commands committed to repo |

**Resolution order:** Project commands override global commands if both exist.

## Usage

After installation, start Claude Code in any project:

```bash
claude
```

Then use the skillchain command:

```
/skillchain help                         # Show all 29 available skills
/skillchain dashboard with charts        # Build a dashboard
/skillchain login form with validation   # Build a login form
/skillchain AI chat interface            # Build a chat UI
/skillchain import CSV data to postgres  # Build ETL pipeline
/skillchain RAG pipeline with embeddings # Build AI data pipeline
```

### How It Works

1. **Parse Goal** - Skillchain analyzes keywords in your description
2. **Identify Skills** - Matches keywords to required skills (29 total)
3. **Order Skills** - Ensures correct execution order (theming first)
4. **Guide Configuration** - Asks questions for each skill
5. **Generate Code** - Produces themed, accessible components
6. **Validate** - Runs assembly skill to validate token usage

### Keyword Mappings

#### Frontend Keywords
| Keywords | Skills Invoked |
|----------|----------------|
| dashboard, analytics, KPI | theming → layouts → dashboards → visualizing-data |
| form, login, signup | theming → building-forms → providing-feedback |
| chart, graph, visualize | theming → visualizing-data |
| table, grid, data | theming → building-tables |
| chat, AI, assistant | theming → building-ai-chat |

#### Backend Keywords
| Keywords | Skills Invoked |
|----------|----------------|
| database, sql, postgres | api-patterns → databases-relational |
| vector, embedding, rag | ai-data-engineering → databases-vector |
| ingest, import, etl, csv | ingesting-data → [database-skill] |
| api, rest, graphql | api-patterns |
| deploy, kubernetes | assembling-components → deploying-applications |

See `skillchain.md` for the complete keyword mapping.

### Workflow Commands

During a skillchain session, you can use:

| Command | Action |
|---------|--------|
| `back` | Return to previous step |
| `skip` | Use defaults, move to next |
| `status` | Show current progress |
| `done` | Finish early with current selections |
| `restart` | Start over |

## Requirements

- Claude Code CLI installed
- AI Design Components skills installed (via marketplace or local)

## Files

- `skillchain.md` - The slash command definition (613 lines)
- `install-skillchain.sh` - Installation script with global/project options
- `README.md` - This documentation

## Updating

To update an existing installation, run the installer again:

```bash
# Update global installation
./commands/install-skillchain.sh --global

# Update project installation
./commands/install-skillchain.sh ~/your-project
```

The installer will detect and update existing installations.
