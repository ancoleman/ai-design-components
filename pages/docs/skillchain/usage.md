---
sidebar_position: 3
title: Usage Guide
description: How to use skillchain effectively with examples
---

# Using Skillchain

Skillchain provides a conversational workflow for building applications. This guide covers basic usage, keyword detection patterns, and real-world examples.

## Basic Usage

After [installing skillchain](./installation.md), start Claude Code in any project:

```bash
# Start Claude Code
claude

# Use skillchain with natural language
/skillchain [describe what you want to build]
```

### Command Syntax

```bash
/skillchain help                         # Show help guide
/skillchain [goal]                       # Start workflow with goal
```

Examples:
```bash
/skillchain dashboard with charts        # Frontend: dashboard + visualizations
/skillchain login form with validation   # Frontend: form system
/skillchain REST API with postgres       # Backend: API + database
/skillchain RAG pipeline                 # Backend: AI/ML workflow
```

## How Skillchain Interprets Your Goal

Skillchain uses **keyword detection** to understand what you want to build:

### Frontend Keywords

Trigger frontend orchestrator when detected:

| Category | Keywords |
|----------|----------|
| **UI/Components** | ui, component, interface, page, design |
| **Forms** | form, input, validation, login, signup, register |
| **Data Display** | dashboard, chart, graph, table, grid, analytics |
| **Navigation** | menu, nav, tabs, routing, sidebar, breadcrumb |
| **Interaction** | drag, drop, chat, toast, notification, loading |
| **Layout** | layout, responsive, columns, grid |
| **Media** | upload, file, image, gallery, video, audio |
| **Guidance** | onboarding, tutorial, wizard, tooltip |

### Backend Keywords

Trigger backend orchestrator when detected:

| Category | Keywords |
|----------|----------|
| **APIs** | api, rest, graphql, grpc, endpoint |
| **Databases** | database, sql, postgres, mongo, redis |
| **Data Flow** | ingest, import, etl, pipeline, stream |
| **Messaging** | kafka, queue, websocket, realtime |
| **Platform** | deploy, kubernetes, auth, oauth, jwt |
| **AI/ML** | rag, vector, embeddings, llm, model |

### AI/ML Keywords

Trigger AI/ML orchestrator when detected:

| Category | Keywords |
|----------|----------|
| **RAG/Search** | rag, semantic search, vector search |
| **Embeddings** | embeddings, similarity, indexing |
| **Models** | llm, model, inference, serving |
| **Pipelines** | chunking, preprocessing, data engineering |

### Fullstack Detection

If **both frontend AND backend keywords** are present, skillchain routes to the fullstack orchestrator:

```bash
/skillchain dashboard with postgres backend
# Detects: "dashboard" (frontend) + "postgres" (backend)
# Routes to: fullstack orchestrator
```

## Frontend Examples

### Example 1: Analytics Dashboard

```bash
/skillchain analytics dashboard with revenue charts
```

**What happens:**
1. Detects keywords: `analytics`, `dashboard`, `charts`
2. Matches blueprint: `dashboard`
3. Routes to: Frontend orchestrator
4. Skills selected:
   - theming-components (foundation)
   - designing-layouts (structure)
   - creating-dashboards (dashboard layout)
   - visualizing-data (charts)
   - building-tables (optional, if data tables mentioned)
   - providing-feedback (loading states)
   - assembling-components (final assembly)
5. Questions asked: ~3 (using dashboard blueprint)
6. Output: Complete themed dashboard with charts and KPIs

### Example 2: Login Form

```bash
/skillchain login form with email and password validation
```

**What happens:**
1. Detects keywords: `login`, `form`, `validation`
2. Routes to: Frontend orchestrator
3. Skills selected:
   - theming-components
   - building-forms (form system)
   - providing-feedback (error messages)
   - assembling-components
4. Questions asked: ~5
5. Output: Form with validation, error handling, and accessibility

### Example 3: AI Chat Interface

```bash
/skillchain AI chat interface with streaming responses
```

**What happens:**
1. Detects keywords: `chat`, `ai`, `streaming`
2. Routes to: Frontend orchestrator
3. Skills selected:
   - theming-components
   - designing-layouts
   - building-ai-chat (chat UI)
   - building-forms (message input)
   - providing-feedback (loading states)
   - assembling-components
4. Questions asked: ~8
5. Output: Chat UI with streaming, message history, and user input

## Backend Examples

### Example 4: REST API with PostgreSQL

```bash
/skillchain REST API with PostgreSQL database
```

**What happens:**
1. Detects keywords: `rest`, `api`, `postgresql`, `database`
2. Matches blueprint: `crud-api`
3. Routes to: Backend orchestrator
4. Skills selected:
   - api-patterns (REST endpoints)
   - databases-relational (Postgres)
   - auth-security (optional, if mentioned)
   - observability (optional)
5. Questions asked: ~4 (using crud-api blueprint)
6. Output: FastAPI/Express/Axum API with Postgres, migrations, and CRUD endpoints

### Example 5: Data Ingestion Pipeline

```bash
/skillchain import CSV data from S3 to PostgreSQL
```

**What happens:**
1. Detects keywords: `import`, `csv`, `s3`, `postgresql`
2. Routes to: Backend orchestrator
3. Skills selected:
   - ingesting-data (ETL pipeline)
   - databases-relational (Postgres)
   - observability (monitoring)
4. Questions asked: ~6
5. Output: ETL pipeline with S3 source, data validation, and Postgres sink

### Example 6: RAG Pipeline

```bash
/skillchain RAG pipeline with vector search and embeddings
```

**What happens:**
1. Detects keywords: `rag`, `vector`, `search`, `embeddings`
2. Matches blueprint: `rag-pipeline`
3. Routes to: AI-ML orchestrator
4. Skills selected:
   - ingesting-data (document ingestion)
   - databases-vector (Qdrant/pgvector)
   - ai-data-engineering (chunking, embeddings)
   - api-patterns (query API)
   - model-serving (optional)
5. Questions asked: ~4 (using rag-pipeline blueprint)
6. Output: Complete RAG system with document ingestion, vector storage, and semantic search

## Fullstack Examples

### Example 7: Dashboard with Backend

```bash
/skillchain sales dashboard with revenue charts and postgres backend
```

**What happens:**
1. Detects keywords: `dashboard`, `charts` (frontend) + `postgres`, `backend` (backend)
2. Routes to: Fullstack orchestrator
3. Skills selected:
   - **Frontend:** theming-components, designing-layouts, creating-dashboards, visualizing-data, assembling-components
   - **Backend:** api-patterns, databases-relational
4. Questions asked: ~10
5. Output: Full-stack app with React/Svelte dashboard + FastAPI/Express backend + Postgres

### Example 8: Login with OAuth

```bash
/skillchain login form with OAuth 2.0 authentication
```

**What happens:**
1. Detects keywords: `login`, `form` (frontend) + `oauth`, `authentication` (backend)
2. Routes to: Fullstack orchestrator
3. Skills selected:
   - **Frontend:** theming-components, building-forms, assembling-components
   - **Backend:** api-patterns, auth-security
4. Questions asked: ~8
5. Output: Login UI + OAuth 2.1 backend with JWT tokens

## Workflow Commands

During a skillchain session, you can control the flow:

| Command | Action | Example |
|---------|--------|---------|
| `back` | Return to previous skill | Go back to change theme choice |
| `skip` | Use defaults for current question | Skip framework selection, use React |
| `status` | Show current progress | See which skills remain |
| `done` | Finish early with current selections | Stop before optional skills |
| `restart` | Start over from beginning | Change entire approach |
| `help` | Show workflow commands | List available commands |

### Example Session with Commands

```
You: /skillchain dashboard with charts

Claude: I detected this matches our 'dashboard' blueprint!
Would you like to use the dashboard blueprint? (yes/no/customize)

You: yes

Claude: [Question 1/3] Choose color scheme:
- blue-gray (default)
- purple
- green
- custom

You: skip

Claude: Using default: blue-gray
[Question 2/3] Which chart types?

You: bar and line charts

Claude: [Question 3/3] Include data tables?

You: status

Claude: Progress: 66% complete (2/3 questions answered)
Remaining: data tables question

You: yes

Claude: Generating dashboard... [complete output]
```

## Advanced Patterns

### Using Saved Preferences

After your first workflow, skillchain offers to save preferences:

```yaml
# ~/.claude/skillchain-prefs.yaml
global:
  theme:
    color_scheme: "blue-gray"
    theme_modes: ["light", "dark"]
  frameworks:
    frontend: "react"
    backend: "fastapi"
```

**Next time you run skillchain:**
- Saved values become smart defaults
- Questions are pre-filled
- You can override by providing different answers
- Faster workflows (fewer questions)

### Customizing Blueprints

When a blueprint is detected, you can customize it:

```
Claude: Would you like to use the dashboard blueprint? (yes/no/customize)

You: customize

Claude: Starting with dashboard blueprint. You can modify any defaults.
[Question 1/5] Choose color scheme...
```

This gives you blueprint benefits (skill selection, ordering) while allowing full customization.

### Multi-Language Backend

All backend skills support multiple languages:

```bash
/skillchain REST API with PostgreSQL
```

You'll be asked:
```
Choose backend framework:
- fastapi (Python)
- express (TypeScript)
- axum (Rust)
- hono (TypeScript/Cloudflare)
```

All patterns work across languages with idiomatic implementations.

## Tips for Better Results

### 1. Be Specific About Requirements

```bash
# Vague
/skillchain dashboard

# Better
/skillchain sales dashboard with bar charts and KPI cards

# Best
/skillchain sales dashboard with monthly revenue bar chart, year-over-year comparison, and 4 KPI cards for revenue, profit, orders, and customers
```

### 2. Mention Key Technologies

```bash
# Generic
/skillchain API with database

# Specific
/skillchain REST API with PostgreSQL and JWT authentication
```

### 3. Include User Experience Details

```bash
# Basic
/skillchain form

# Enhanced
/skillchain login form with email validation, password strength meter, and social login
```

### 4. Leverage Blueprints

When your goal matches a blueprint pattern, let skillchain detect it:

```bash
# Blueprint-friendly patterns
/skillchain analytics dashboard       # → dashboard blueprint
/skillchain CRUD API                  # → crud-api blueprint
/skillchain RAG system                # → rag-pipeline blueprint
```

### 5. Use Workflow Commands

Don't restart from scratch when you need to adjust:

```bash
# Change a previous choice
You: back

# Skip tedious questions
You: skip

# Check progress
You: status
```

## Troubleshooting

### Wrong Category Detected

If skillchain routes to the wrong category:

```bash
# Be more explicit
/skillchain backend API with postgres  # Forces backend

# Or use both frontend and backend keywords for fullstack
/skillchain dashboard UI with postgres backend
```

### Blueprint Not Detected

If you want a blueprint but it's not triggered:

```bash
# Use exact blueprint keywords
/skillchain analytics dashboard     # ✓ Triggers dashboard blueprint
/skillchain data overview page      # ✗ May not trigger blueprint

# Explicitly mention the pattern
/skillchain REST API CRUD operations  # ✓ Triggers crud-api blueprint
```

### Too Many Questions

Use blueprints to reduce questions:

```bash
# Standard: 12+ questions
/skillchain I want to build a dashboard with charts

# Blueprint: 3 questions
/skillchain analytics dashboard
```

Or use `skip` command during workflow to accept defaults.

## Next Steps

- [Explore blueprints](./blueprints.md) for fast-track presets
- [Understand architecture](./architecture.md) and how it works internally
- [View skills overview](../skills/overview.md) to see all 29 available skills
