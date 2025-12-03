# Claude Code Commands

This directory contains slash commands for Claude Code that provide guided workflows for AI Design Components.

## The Skillchain Command (v2.1)

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

This installs to `~/.claude/commands/skillchain/`, making the command available in **every project** you work on.

### Option 2: Project-Specific Installation

Install for a single project (can be committed and shared with team):

```bash
# Install to current directory
./commands/install-skillchain.sh

# Or install to a specific project
./commands/install-skillchain.sh ~/path/to/your/project
```

This installs to `<project>/.claude/commands/skillchain/`, making it available only in that project.

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
2. **Detect Category** - Routes to frontend, backend, fullstack, or ai-ml orchestrator
3. **Match Blueprint** - Checks for pre-configured patterns (dashboard, crud-api, rag-pipeline)
4. **Order Skills** - Ensures correct execution order with dependency resolution
5. **Load Preferences** - Applies saved preferences from previous sessions
6. **Guide Configuration** - Asks questions for each skill (or uses defaults)
7. **Parallel Loading** - Invokes independent skills concurrently
8. **Generate Code** - Produces themed, accessible components
9. **Save Preferences** - Optionally saves choices for next time

---

## v2.1 Features

### User Preferences System

Skillchain remembers your choices between sessions:

```yaml
# Saved to ~/.claude/skillchain-prefs.yaml
global:
  theme:
    color_scheme: "blue-gray"
    theme_modes: ["light", "dark"]
  frameworks:
    frontend: "react"
    backend: "fastapi"
```

**How it works:**
- First run: Answer questions, offered to save preferences
- Future runs: Your saved preferences become smart defaults
- Override anytime: Just provide a different answer

### Skill Versioning

All 29 skills are versioned for compatibility tracking:

```yaml
# In _registry.yaml
visualizing-data:
  version: "1.0.0"
  # ...
```

See `_shared/changelog.md` for version history and `_shared/compatibility.md` for the compatibility matrix.

### Parallel Skill Loading

Independent skills are loaded concurrently for faster workflows:

```
# Instead of sequential:
Step 1: theming-components
Step 2: designing-layouts
Step 3: visualizing-data   # waits for layouts
Step 4: building-tables    # waits for viz

# Parallel loading:
Step 1: theming-components
Step 2: designing-layouts
Step 3 (PARALLEL): visualizing-data + building-tables
```

Skills are grouped by `parallel_group` in the registry. See `_shared/parallel-loading.md` for dependency graphs.

### Blueprints

Pre-configured skill chains for common patterns:

| Blueprint | Trigger Keywords | Skills |
|-----------|-----------------|--------|
| `dashboard` | dashboard, analytics, admin panel | theming → layouts → dashboards → data-viz → feedback → assembly |
| `crud-api` | REST API, CRUD, FastAPI | api-patterns → databases-relational → auth-security |
| `rag-pipeline` | RAG, semantic search, embeddings | ingesting-data → databases-vector → ai-data-engineering |

When detected, blueprints offer a faster path with fewer questions.

---

## Architecture (v2.0+)

Skillchain uses a modular architecture:

```
skillchain/
├── skillchain.md           # Router (parses goal, routes to orchestrator)
├── _registry.yaml          # 29 skills with keywords, dependencies, versions
├── _help.md                # Help content shown for /skillchain help
├── _shared/
│   ├── theming-rules.md    # Token-first styling requirements
│   ├── execution-flow.md   # Workflow command handling
│   ├── preferences.md      # User preferences schema
│   ├── parallel-loading.md # Dependency graphs for parallel loading
│   ├── changelog.md        # Version history
│   └── compatibility.md    # Version compatibility matrix
├── categories/
│   ├── frontend.md         # Frontend orchestrator (15 skills)
│   ├── backend.md          # Backend orchestrator (14 skills)
│   ├── fullstack.md        # Combined frontend + backend
│   └── ai-ml.md            # AI/ML specific patterns
└── blueprints/
    ├── dashboard.md        # Pre-configured dashboard chain
    ├── crud-api.md         # Pre-configured API chain
    └── rag-pipeline.md     # Pre-configured RAG chain
```

### Dynamic Path Discovery

Skillchain works from any project by dynamically finding its installation location:

```bash
# Step 0 in skillchain.md discovers the path:
if [ -d ".claude/commands/skillchain" ]; then
  SKILLCHAIN_DIR="$(pwd)/.claude/commands/skillchain"
elif [ -d "$HOME/.claude/commands/skillchain" ]; then
  SKILLCHAIN_DIR="$HOME/.claude/commands/skillchain"
fi
```

All file references use `{SKILLCHAIN_DIR}/...` pattern for portability.

---

## Skill Categories

### Frontend Skills (15)

| Skill | Group | Description |
|-------|-------|-------------|
| theming-components | foundation | Design tokens, colors, dark mode |
| designing-layouts | structure | Grid systems, responsive design |
| implementing-navigation | structure | Menus, tabs, routing |
| visualizing-data | data-display | Charts, graphs, plots |
| building-tables | data-display | Data grids, pagination |
| creating-dashboards | data-display | KPI cards, widgets |
| building-forms | user-input | Inputs, validation |
| implementing-search-filter | user-input | Search, faceted filters |
| building-ai-chat | interaction | Chat UI, streaming |
| implementing-drag-drop | interaction | Sortable, kanban |
| providing-feedback | interaction | Toasts, alerts, loading |
| displaying-timelines | structure | Activity feeds, history |
| managing-media | content | File upload, galleries |
| guiding-users | content | Onboarding, tooltips |
| assembling-components | assembly | Final integration |

### Backend Skills (14)

| Skill | Group | Description |
|-------|-------|-------------|
| ingesting-data | data-ingestion | ETL, CSV, S3 imports |
| databases-relational | databases | Postgres, MySQL, SQLite |
| databases-vector | databases | Qdrant, pgvector, Pinecone |
| databases-timeseries | databases | ClickHouse, InfluxDB |
| databases-document | databases | MongoDB, DynamoDB |
| databases-graph | databases | Neo4j, knowledge graphs |
| api-patterns | apis | REST, GraphQL, gRPC |
| message-queues | messaging | Kafka, RabbitMQ, Celery |
| realtime-sync | messaging | WebSocket, SSE, CRDTs |
| auth-security | platform | JWT, OAuth, RBAC |
| observability | platform | OpenTelemetry, logging |
| deploying-applications | platform | Kubernetes, serverless |
| ai-data-engineering | ai-ml | RAG pipelines, chunking |
| model-serving | ai-ml | vLLM, Ollama, inference |

---

## Workflow Commands

During a skillchain session, you can use:

| Command | Action |
|---------|--------|
| `back` | Return to previous skill |
| `skip` | Use defaults for current question |
| `status` | Show current progress |
| `done` | Finish early with current selections |
| `restart` | Start over from beginning |
| `help` | Show workflow commands |

---

## Files

```
commands/
├── skillchain/              # Modular command structure (19 files)
│   ├── skillchain.md        # Router
│   ├── _registry.yaml       # Skill definitions
│   ├── _help.md             # Help content
│   ├── _shared/             # Shared resources (9 files)
│   ├── categories/          # Orchestrators (4 files)
│   └── blueprints/          # Templates (3 files)
├── install-skillchain.sh    # Installation script
└── README.md                # This documentation
```

## Updating

To update an existing installation, run the installer again:

```bash
# Update global installation
./commands/install-skillchain.sh --global

# Update project installation
./commands/install-skillchain.sh ~/your-project
```

The installer will detect and update existing installations.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v2.1.0 | 2025-12-02 | User preferences, skill versioning, parallel loading |
| v2.0.0 | 2025-12-02 | Modular architecture, blueprints, dynamic paths |
| v1.0.0 | 2025-12-01 | Initial monolithic release |

See `skillchain/_shared/changelog.md` for detailed version history.
