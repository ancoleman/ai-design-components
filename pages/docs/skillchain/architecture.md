---
sidebar_position: 5
title: Architecture
description: How skillchain works internally
---

# Skillchain Architecture

Skillchain v2.1 uses a modular architecture that separates concerns and enables dynamic path discovery, parallel loading, and user preferences.

## Core Concepts

### 1. Modular Design

Skillchain is built from 19 separate files instead of a monolithic script:

```
skillchain/
├── skillchain.md           # Router (entry point)
├── _registry.yaml          # Skill definitions
├── _help.md                # Help content
├── _shared/                # Shared resources (6 files)
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

**Benefits:**
- **Maintainability** - Each file has single responsibility
- **Extensibility** - Add new blueprints/orchestrators easily
- **Testability** - Test individual components
- **Debuggability** - Easier to trace issues

### 2. Registry System

The `_registry.yaml` file serves as the central configuration:

```yaml
registry_version: "2.1.0"
last_updated: "2025-12-02"

categories:
  frontend: { description, default_tools }
  backend: { description, default_tools }
  fullstack: { description, default_tools }
  ai-ml: { description, default_tools }

blueprints:
  dashboard: { triggers, skill_chain, questions }
  crud-api: { triggers, skill_chain, questions }
  rag-pipeline: { triggers, skill_chain, questions }

skills:
  theming-components:
    category: frontend
    priority: 1
    keywords: { primary, secondary, exclusions }
    dependencies: []
    version: "1.0.0"
  # ... 28 more skills
```

**Registry provides:**
- Skill metadata (name, category, priority)
- Keyword matching rules
- Dependency relationships
- Version tracking
- Blueprint definitions

### 3. Dynamic Path Discovery

Skillchain works from any installation location (global or project):

```bash
# Step 0 in skillchain.md (executed first, every time)
if [ -d ".claude/commands/skillchain" ]; then
  SKILLCHAIN_DIR="$(pwd)/.claude/commands/skillchain"
elif [ -d "$HOME/.claude/commands/skillchain" ]; then
  SKILLCHAIN_DIR="$HOME/.claude/commands/skillchain"
fi
```

All file references use `{SKILLCHAIN_DIR}/...` for portability.

This enables:
- Global installation (`~/.claude/commands/skillchain/`)
- Project installation (`.claude/commands/skillchain/`)
- No hardcoded paths
- Works from any working directory

## System Flow

The complete workflow from user input to generated code follows these steps:

1. **Step 0:** Locate Skillchain Directory - Find installation location
2. **Step 0.5:** Load User Preferences - Load saved choices as defaults
3. **Step 1:** Parse Command - Handle "help" or continue with goal
4. **Step 2:** Load Registry - Parse _registry.yaml for skills
5. **Step 3:** Analyze Goal & Detect Category - Extract keywords, determine frontend/backend/fullstack/ai-ml
6. **Step 3.5:** Detect Blueprint Match - Check if goal matches a blueprint pattern
7. **Step 4:** Match Skills - Find relevant skills based on keywords
8. **Step 5:** Route to Orchestrator - Load appropriate category orchestrator
9. **Step 6:** Orchestrator Execution - Invoke skills, ask questions, generate code
10. **Step 7:** Save Preferences - Offer to save choices for next time

## Category Routing

### Frontend Orchestrator

**Responsibilities:**
- Handle UI-focused workflows
- Ensure theming is always first
- Group skills by phase (foundation → structure → content → interaction)
- Apply token-first styling rules
- Invoke assembling-components last

**Skill Groups:**
1. Foundation (priority 1): theming-components
2. Structure (priority 2-4): layouts, navigation, timelines
3. Data Display (priority 5): dashboards, charts, tables
4. User Input (priority 6): forms, search-filter
5. Interaction (priority 7-8): ai-chat, drag-drop, feedback
6. Content (priority 7): media, guiding-users
7. Assembly (priority 99): assembling-components

### Backend Orchestrator

**Responsibilities:**
- Handle API/database/deployment workflows
- Support multi-language patterns (Python/TypeScript/Rust/Go)
- Group skills by layer (data → APIs → platform)
- Apply observability by default

**Skill Groups:**
1. Data Ingestion (priority 5): ingesting-data
2. Databases (priority 10): relational, vector, timeseries, document, graph
3. APIs (priority 5): api-patterns
4. Messaging (priority 15): message-queues, realtime-sync
5. Platform (priority 8-25): auth-security, observability, deploying-applications
6. AI/ML (priority 15-20): ai-data-engineering, model-serving

### Fullstack Orchestrator

**Responsibilities:**
- Combine frontend + backend workflows
- Ensure API contracts align (frontend expects what backend provides)
- Apply consistent theming across full stack
- Handle data flow (backend → frontend)

**Execution:**
1. Run frontend orchestrator
2. Run backend orchestrator
3. Verify API contracts
4. Generate integration code

### AI-ML Orchestrator

**Responsibilities:**
- Handle RAG pipelines, model serving, AI data engineering
- Optimize for AI-specific patterns
- Support vector databases and embeddings
- Integrate with LLM providers

**Skill Groups:**
1. Data Ingestion: ingesting-data (documents, PDFs)
2. Vector Storage: databases-vector
3. AI Engineering: ai-data-engineering (chunking, embeddings)
4. API Layer: api-patterns (query endpoints)
5. Model Serving: model-serving (vLLM, Ollama)
6. Optional UI: building-ai-chat

## Parallel Loading

### Concept

Independent skills are loaded concurrently to reduce workflow time:

```
Sequential (old):          Parallel (v2.1):
Step 1: skill-a (10s)      Step 1: skill-a (10s)
Step 2: skill-b (8s)       Step 2: skill-b + skill-c (8s)
Step 3: skill-c (6s)       Step 3: skill-d (5s)
Total: 24s                 Total: 23s (10-30% faster)
```

### Parallel Groups

Skills are assigned to `parallel_group` in registry:

```yaml
skills:
  theming-components:
    parallel_group: 1  # Always first (foundation)

  designing-layouts:
    parallel_group: 2  # After theming

  visualizing-data:
    parallel_group: 3  # After layouts
    dependencies: ["theming-components"]

  building-tables:
    parallel_group: 3  # Same as viz (parallel!)
    dependencies: ["theming-components"]

  assembling-components:
    parallel_group: 99  # Always last
```

**Rules:**
- Skills in same `parallel_group` run concurrently
- Dependencies must be in earlier groups
- Foundation skills run first (group 1)
- Assembly skills run last (group 99)

## User Preferences System

### Preference Schema

```yaml
# ~/.claude/skillchain-prefs.yaml
global:
  theme:
    color_scheme: string
    theme_modes: [light, dark, high-contrast]

  frameworks:
    frontend: react | svelte | vue | solid
    backend: fastapi | express | axum | hono
    database: postgres | mysql | sqlite

  ai_ml:
    llm_provider: openai | anthropic | ollama | vllm
    embedding_model: openai | sentence-transformers
    vector_db: qdrant | pgvector | pinecone

last_updated: timestamp
version: "2.1.0"
```

### Preference Priority

When resolving configuration values:

1. **User's explicit choice** (current workflow) - Highest priority
2. **Saved preferences** (from `~/.claude/skillchain-prefs.yaml`)
3. **Blueprint defaults** (if blueprint is active)
4. **Skill defaults** (from `_registry.yaml`)

## Versioning

### Skill Versions

Each skill has semantic version:

```yaml
skills:
  theming-components:
    version: "1.0.0"
  visualizing-data:
    version: "1.0.0"
```

### Registry Version

```yaml
registry_version: "2.1.0"  # Skillchain version
version: "2.0.0"            # Backwards compat
```

## File Structure

### Complete Directory Tree

```
.claude/commands/skillchain/
├── skillchain.md              # Router (200 lines)
├── _registry.yaml             # Skill definitions (759 lines)
├── _help.md                   # Help content (156 lines)
│
├── _shared/                   # Shared resources
│   ├── theming-rules.md       # Token-first styling requirements
│   ├── execution-flow.md      # Workflow command handling
│   ├── preferences.md         # User preferences schema
│   ├── parallel-loading.md    # Dependency graphs
│   ├── changelog.md           # Version history
│   └── compatibility.md       # Version compatibility matrix
│
├── categories/                # Orchestrators
│   ├── frontend.md            # Frontend orchestrator (~300 lines)
│   ├── backend.md             # Backend orchestrator (~350 lines)
│   ├── fullstack.md           # Fullstack orchestrator (~250 lines)
│   └── ai-ml.md               # AI/ML orchestrator (~300 lines)
│
└── blueprints/                # Pre-configured templates
    ├── dashboard.md           # Dashboard blueprint (~150 lines)
    ├── crud-api.md            # CRUD API blueprint (~200 lines)
    └── rag-pipeline.md        # RAG pipeline blueprint (~250 lines)

Total: 19 files, ~3,000 lines
```

## Design Decisions

### Why Modular Architecture?

**Problem:** v1.0 was a single 1,000+ line file that was hard to maintain.

**Solution:** Break into 19 specialized files.

**Benefits:**
- Each file has single responsibility
- Easier to test individual components
- Simpler to add new blueprints
- Better git diffs (changes isolated)

### Why Dynamic Path Discovery?

**Problem:** Hardcoded paths don't work for both global and project installations.

**Solution:** Detect installation location at runtime.

**Benefits:**
- Works from any directory
- Supports global installation (`~/.claude/`)
- Supports project installation (`.claude/`)
- No configuration needed

### Why Registry-Based?

**Problem:** Skill metadata scattered across multiple files.

**Solution:** Centralize in `_registry.yaml`.

**Benefits:**
- Single source of truth
- Easy to update skill definitions
- Supports tooling (validation, linting)
- Clear skill relationships

### Why Parallel Loading?

**Problem:** Sequential skill loading is slow.

**Solution:** Load independent skills concurrently.

**Benefits:**
- 10-30% faster workflows
- Better user experience
- Scales with more skills
- Automatically resolves dependencies

### Why User Preferences?

**Problem:** Repeating same choices every workflow.

**Solution:** Save preferences between sessions.

**Benefits:**
- Faster subsequent workflows
- Consistent configurations
- Easy to override
- Shareable (commit to repo)

## Extension Points

### Adding a New Blueprint

1. Create blueprint file: `blueprints/my-blueprint.md`
2. Add to `_registry.yaml`:
   ```yaml
   blueprints:
     my-blueprint:
       triggers: { primary, secondary }
       skill_chain: [...]
       file: "{SKILLCHAIN_DIR}/blueprints/my-blueprint.md"
   ```
3. Test keyword detection
4. Document in this guide

### Adding a New Orchestrator

1. Create orchestrator file: `categories/my-category.md`
2. Add to `_registry.yaml`:
   ```yaml
   categories:
     my-category:
       description: "..."
       default_tools: [...]
   ```
3. Implement skill routing logic
4. Test with various goals

### Adding a New Skill

1. Create skill package (see [Skills documentation](../skills/overview.md))
2. Add to `_registry.yaml`:
   ```yaml
   skills:
     my-skill:
       category: frontend
       priority: 7
       keywords: { primary, secondary }
       dependencies: [...]
       version: "1.0.0"
   ```
3. Test keyword matching
4. Update compatibility matrix

## Performance Characteristics

### Time Complexity

- **Category detection:** O(k) where k = keyword count
- **Skill matching:** O(n) where n = skill count
- **Dependency resolution:** O(n²) worst case, O(n) typical
- **Blueprint detection:** O(b × k) where b = blueprint count

### Space Complexity

- **Registry:** ~50KB YAML
- **Preferences:** ~5KB YAML
- **Total files:** ~100KB

### Execution Time

- **Router:** under 1 second
- **Orchestrator load:** under 1 second
- **Skill invocation:** 2-5 seconds per skill
- **Total workflow:** 5-12 minutes (depends on questions)

## Next Steps

- [Install skillchain](./installation.md) to try it yourself
- [Learn usage patterns](./usage.md) for effective workflows
- [Explore blueprints](./blueprints.md) for fast-track presets
- [View skills overview](../skills/overview.md) to see what's orchestrated
