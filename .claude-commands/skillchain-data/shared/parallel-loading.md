# Parallel Skill Loading Guide

## Overview

Skills can be invoked in parallel when they don't depend on each other's output. This speeds up the workflow by allowing Claude to invoke multiple skills simultaneously.

## Dependency Analysis

### Frontend Skills Dependency Graph

```
theming-components (MUST BE FIRST - foundation)
    │
    ├── designing-layouts ────────────────────┐
    │       │                                 │
    │       └── creating-dashboards ──────────┤
    │                                         │
    ├── visualizing-data ─────────────────────┤
    │                                         │
    ├── building-tables ──────────────────────┤
    │                                         │
    ├── building-forms ───────────────────────┤
    │       │                                 │
    │       └── building-ai-chat ─────────────┤
    │                                         │
    ├── implementing-search-filter ───────────┤
    │                                         │
    ├── implementing-drag-drop ───────────────┤
    │                                         │
    ├── providing-feedback ───────────────────┤
    │                                         │
    ├── implementing-navigation ──────────────┤
    │                                         │
    ├── displaying-timelines ─────────────────┤
    │                                         │
    ├── managing-media ───────────────────────┤
    │                                         │
    └── guiding-users ────────────────────────┤
                                              │
                                              ▼
                              assembling-components (MUST BE LAST)
```

### Backend Skills Dependency Graph

```
Independent Entry Points:
├── ingesting-data
├── api-patterns
├── databases-relational
├── databases-timeseries
├── databases-document
├── databases-graph
└── observability

Dependent Skills:
├── databases-vector ──────► ingesting-data
├── message-queues ────────► api-patterns
├── realtime-sync ─────────► api-patterns
├── auth-security ─────────► api-patterns
├── ai-data-engineering ───► databases-vector
├── model-serving ─────────► ai-data-engineering
└── deploying-applications (independent, no deps)
```

## Parallel Groups

### Frontend Parallel Groups

**Group 1: Foundation (Sequential - MUST be first)**
- theming-components

**Group 2: Structure (Can be parallel)**
- designing-layouts
- implementing-navigation

**Group 3: Data Display (Can be parallel after Group 2)**
- visualizing-data
- building-tables
- creating-dashboards (needs designing-layouts)

**Group 4: User Input (Can be parallel)**
- building-forms
- implementing-search-filter

**Group 5: Interaction (Can be parallel, some need Group 4)**
- building-ai-chat (needs building-forms)
- implementing-drag-drop
- providing-feedback

**Group 6: Content (Can be parallel)**
- displaying-timelines
- managing-media
- guiding-users

**Group 7: Assembly (Sequential - MUST be last)**
- assembling-components

### Backend Parallel Groups

**Group 1: Data Layer (Can be parallel)**
- ingesting-data
- databases-relational
- databases-timeseries
- databases-document
- databases-graph

**Group 2: Vector + API (Can be parallel after relevant Group 1)**
- databases-vector (after ingesting-data)
- api-patterns

**Group 3: API Extensions (Can be parallel after api-patterns)**
- message-queues
- realtime-sync
- auth-security

**Group 4: AI/ML (Sequential)**
- ai-data-engineering (after databases-vector)
- model-serving (after ai-data-engineering)

**Group 5: Platform (Can be parallel)**
- observability
- deploying-applications

## Orchestrator Implementation

When invoking skills, orchestrators should:

1. **Identify parallel opportunities:**
   ```
   If multiple skills in same group are matched:
     Invoke them in parallel using multiple Skill tool calls
   ```

2. **Respect dependencies:**
   ```
   Before invoking skill X:
     Check if all dependencies of X are completed
     If not, wait for dependencies first
   ```

3. **Example parallel invocation:**
   ```markdown
   For dashboard goal with visualizing-data + building-tables:

   Step 1: Invoke theming-components (sequential, required)
   Step 2: Invoke designing-layouts (sequential, dashboard needs it)
   Step 3: Invoke visualizing-data AND building-tables (PARALLEL!)
   Step 4: Invoke creating-dashboards (after Step 2+3)
   Step 5: Invoke assembling-components (sequential, last)
   ```

## Performance Benefits

| Scenario | Sequential Time | Parallel Time | Savings |
|----------|-----------------|---------------|---------|
| Dashboard (5 skills) | ~25 questions | ~18 questions* | 28% |
| CRUD API (4 skills) | ~20 questions | ~15 questions* | 25% |
| RAG Pipeline (5 skills) | ~25 questions | ~20 questions* | 20% |

*Parallel skills can share configuration context, reducing redundant questions.
