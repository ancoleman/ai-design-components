---
sidebar_position: 1
title: Skillchain Overview
description: Guided workflow for building full-stack applications with 29 production-ready skills
---

# Skillchain

Skillchain is a guided, step-by-step workflow system that chains Claude Skills together to build full-stack applications. Instead of manually triggering individual skills, skillchain automatically routes to the right orchestrator, loads dependencies, and ensures correct execution order.

## What is Skillchain?

The `/skillchain` command is the **recommended entry point** for using AI Design Components. It provides a conversational workflow that:

- **Analyzes your goal** from natural language descriptions
- **Detects the category** (frontend, backend, fullstack, or ai-ml)
- **Matches relevant skills** using keyword detection and scoring
- **Orders skills correctly** with automatic dependency resolution
- **Applies user preferences** as smart defaults from previous sessions
- **Loads skills in parallel** when dependencies allow
- **Guides configuration** through targeted questions
- **Generates production code** with theming, accessibility, and best practices

## Why Use Skillchain?

| Traditional Approach | Skillchain Approach |
|---------------------|---------------------|
| User must know skill names | Describe what you want to build |
| User triggers skills individually | Skills chain automatically |
| Easy to miss required skills | Correct skill order enforced |
| No theming consistency | Theming always applied first |
| Manual component assembly | Assembly skill runs at end |
| Repeat configuration every time | Preferences saved between sessions |

### Example Comparison

**Traditional (requires knowledge):**
```
"Use the theming-components skill, then designing-layouts,
then creating-dashboards, then visualizing-data..."
```

**Skillchain (just describe your goal):**
```
/skillchain sales dashboard with revenue charts
```

## Version 2.1 Features

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
- **First run:** Answer questions, offered to save preferences
- **Future runs:** Your saved preferences become smart defaults
- **Override anytime:** Just provide a different answer

**Preference Priority:**
1. User's explicit choice (current workflow) - Highest
2. Saved preferences (from `~/.claude/skillchain-prefs.yaml`) - Medium
3. Default values (from skill definitions) - Lowest

### Skill Versioning

All 29 skills are versioned for compatibility tracking:

```yaml
# In _registry.yaml
visualizing-data:
  version: "1.0.0"
  # ...
```

This enables:
- **Compatibility matrix** tracking which skills work together
- **Changelog tracking** for each skill's evolution
- **Version pinning** for reproducible builds

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

Skills are grouped by `parallel_group` in the registry. Dependencies are automatically resolved to ensure safe parallelization.

### Blueprints

Pre-configured skill chains for common patterns:

| Blueprint | Trigger Keywords | Time Saved |
|-----------|-----------------|------------|
| `dashboard` | dashboard, analytics, admin panel | 12+ questions → 3 questions |
| `crud-api` | REST API, CRUD, FastAPI | 15+ questions → 4 questions |
| `rag-pipeline` | RAG, semantic search, embeddings | 20+ questions → 4 questions |

When detected, blueprints offer a faster path with optimized defaults.

## Quick Start Example

```bash
# Start Claude Code in your project
claude

# Use skillchain
/skillchain sales dashboard with revenue charts

# Skillchain will:
# 1. Detect category: frontend
# 2. Match blueprint: dashboard
# 3. Ask 3 quick questions
# 4. Generate: themed dashboard with charts, KPIs, and responsive layout
```

## How It Works

1. **Parse Goal** - Skillchain analyzes keywords in your description
2. **Detect Category** - Routes to frontend, backend, fullstack, or ai-ml orchestrator
3. **Match Blueprint** - Checks for pre-configured patterns (dashboard, crud-api, rag-pipeline)
4. **Order Skills** - Ensures correct execution order with dependency resolution
5. **Load Preferences** - Applies saved preferences from previous sessions
6. **Guide Configuration** - Asks questions for each skill (or uses defaults)
7. **Parallel Loading** - Invokes independent skills concurrently
8. **Generate Code** - Produces themed, accessible components
9. **Save Preferences** - Optionally saves choices for next time

## Available Skills

Skillchain orchestrates **29 production-ready skills** across 4 categories:

### Frontend Skills (15)

**Foundation:**
- theming-components

**Data Display:**
- visualizing-data, building-tables, creating-dashboards

**User Input:**
- building-forms, implementing-search-filter

**Interaction:**
- building-ai-chat, implementing-drag-drop, providing-feedback

**Structure:**
- implementing-navigation, designing-layouts, displaying-timelines

**Content:**
- managing-media, guiding-users

**Assembly:**
- assembling-components

### Backend Skills (14)

**Data Ingestion:**
- ingesting-data

**Databases:**
- databases-relational, databases-vector, databases-timeseries, databases-document, databases-graph

**APIs & Messaging:**
- api-patterns, message-queues, realtime-sync

**Platform:**
- auth-security, observability, deploying-applications

**AI/ML:**
- ai-data-engineering, model-serving

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

## Next Steps

- [Install Skillchain](./installation.md) globally or per-project
- [Learn usage patterns](./usage.md) with examples
- [Explore blueprints](./blueprints.md) for fast-track presets
- [Understand architecture](./architecture.md) and how it works internally
