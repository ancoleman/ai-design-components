---
slug: skillchain-v2.1
title: "Skillchain v2.1: Modular Architecture"
authors: [ancoleman]
tags: [release, skillchain, features, automation]
---

# Skillchain v2.1: Modular Architecture

Skillchain v2.1 introduces a completely modular architecture with intelligent features that make building full-stack applications faster and more intuitive.

&lt;!-- truncate -->

## What is Skillchain?

Skillchain is an intelligent orchestrator that helps you build full-stack applications by automatically loading the right Claude Skills for your project. Instead of manually selecting skills, just describe what you're building and Skillchain assembles the perfect skill chain.

## New Features in v2.1

### 1. User Preferences System

Skillchain now remembers your choices and provides smart defaults:

```yaml
# Saved to ~/.claude/skillchain-prefs.yaml
frontend_framework: next.js
styling_preference: tailwind
backend_language: typescript
database_preference: postgresql
```

**Benefits:**
- No repetitive questions for similar projects
- Faster project setup
- Consistent technology choices across projects

### 2. Skill Versioning

All 29 skills now have proper versioning (v1.0.0) with:
- **Changelog tracking** - See what's changed between versions
- **Compatibility info** - Know what works together
- **Deprecation notices** - Plan for future changes

### 3. Parallel Skill Loading

Independent skills now load concurrently using `parallel_group` fields:

```yaml
skills:
  - name: databases-postgresql
    parallel_group: data
  - name: using-vector-databases
    parallel_group: data
  # Both load simultaneously!
```

**Benefits:**
- Faster skill chain initialization
- Reduced waiting time
- Smarter dependency resolution

### 4. Blueprint System

Pre-configured skill chains for common patterns:

**Dashboard Blueprint:**
```bash
/skillchain dashboard
```
Automatically loads:
- creating-dashboards
- visualizing-data
- building-tables
- theming-components

**CRUD API Blueprint:**
```bash
/skillchain crud-api
```
Automatically loads:
- api-patterns
- databases-relational
- auth-security
- observability

**RAG Pipeline Blueprint:**
```bash
/skillchain rag-pipeline
```
Automatically loads:
- databases-vector
- ai-data-engineering
- model-serving
- api-patterns

### 5. Category Orchestrators

Specialized handlers for different domains:

- **Frontend Orchestrator** - React, Vue, Svelte projects
- **Backend Orchestrator** - API, database, auth patterns
- **Fullstack Orchestrator** - Combines frontend + backend
- **AI/ML Orchestrator** - RAG, embeddings, model serving

### 6. Dynamic Path Discovery

Works globally from any project directory:

```bash
# Works from anywhere
cd ~/my-project
/skillchain dashboard

# Automatically finds skillchain installation
# No manual path configuration needed
```

## How It Works

### 8-Step Workflow

1. **Step 0: Path Discovery** - Finds skillchain directory
2. **Step 0.5: Load Preferences** - Reads saved choices
3. **Step 1: Goal Input** - What are you building?
4. **Step 2: Keyword Detection** - Identifies relevant skills
5. **Step 3: Configuration** - Asks targeted questions
6. **Step 4: Skill Assembly** - Loads skills in parallel
7. **Step 5: Execution** - Runs the workflow
8. **Step 7: Save Preferences** - Remembers your choices

## Example Usage

### Simple Dashboard

```bash
/skillchain dashboard analytics
```

**Skillchain:**
- Detects keywords: "dashboard", "analytics"
- Loads: creating-dashboards + visualizing-data
- Asks: Chart types? Data source?
- Assembles components with your branding

### Full-Stack RAG App

```bash
/skillchain I need a RAG chatbot with user auth
```

**Skillchain:**
- Detects: "RAG", "chatbot", "auth"
- Loads: building-ai-chat + databases-vector + auth-security + api-patterns
- Asks: Vector DB? Auth provider? API framework?
- Builds complete authenticated RAG pipeline

### Quick CRUD API

```bash
/skillchain rest api with postgresql
```

**Skillchain:**
- Detects: "api", "postgresql"
- Loads: api-patterns + databases-relational
- Uses preferences: TypeScript (from last time)
- Generates API with proper patterns

## Architecture Improvements

### Modular File Structure (19 files)

```
.claude/commands/skillchain/
├── skillchain.md          # Main router
├── _registry.yaml         # 29 skills with metadata
├── _help.md              # Documentation
├── _shared/              # 9 shared resources
│   ├── theming-rules.md
│   ├── execution-flow.md
│   ├── preferences.md
│   ├── parallel-loading.md
│   └── ...
├── categories/           # 4 orchestrators
│   ├── frontend.md
│   ├── backend.md
│   ├── fullstack.md
│   └── ai-ml.md
└── blueprints/          # 3 templates
    ├── dashboard.md
    ├── crud-api.md
    └── rag-pipeline.md
```

### Benefits of Modularity

- **Easier maintenance** - Update one file, not the whole system
- **Better organization** - Clear separation of concerns
- **Extensibility** - Add new categories/blueprints easily
- **Token efficiency** - Load only what's needed

## Performance

- **Skill loading time:** ~2-3 seconds (parallel loading)
- **Preference loading:** &lt;100ms
- **Path discovery:** &lt;50ms
- **Total startup:** ~3-4 seconds (vs 8-10 seconds in v2.0)

## Installation

```bash
# From repository root
/install-skillchain

# With global access (optional)
/install-skillchain --global
```

## Upgrade Notes

If you're upgrading from v2.0:

1. Re-run installer to get modular structure
2. Your preferences will be preserved
3. All existing projects continue to work
4. New features available immediately

## What's Next

Future enhancements planned:
- **Template library** - Community-contributed blueprints
- **Skill recommendations** - AI-suggested skill chains
- **Project scaffolding** - Generate starter code
- **Skill marketplace** - Browse and install community skills

## Learn More

- [Skillchain Documentation](/docs/skillchain/overview)
- [Creating Custom Blueprints](/docs/skillchain/blueprints)
- [Full Changelog](https://github.com/ancoleman/ai-design-components/blob/main/CHANGELOG.md)
- [GitHub Repository](https://github.com/ancoleman/ai-design-components)
