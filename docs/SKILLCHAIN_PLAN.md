# Skillchain Methodology Improvement Plan

**Status:** Draft
**Created:** December 2, 2025
**Version:** 0.3.1 (29 skills)

---

## Executive Summary

This plan consolidates our skill chaining approach into a simple, user-friendly system:

1. **One command to rule them all:** `/skillchain [goal]`
2. **Remove outdated documentation:** `skillchains/` directory
3. **Preserve valuable content:** Move efficiency analysis to `docs/`
4. **Add helper commands:** `/skilllist`, `/skillhelp`
5. **Update README:** Clear user journey

---

## Current State Analysis

### What We Have

```
ai-design-components/
├── commands/                    # USER-FACING (Current)
│   ├── skillchain.md           # The actual /skillchain command (613 lines)
│   ├── install-skillchain.sh   # Installation script
│   └── README.md               # Command documentation
│
├── demo/                        # SKILLCHAIN REFERENCE (Current)
│   ├── KEYWORD_TRIGGERS.md     # Detailed keyword mappings
│   ├── DECISION_TREE.md        # Decision trees for each skill
│   ├── USER_PROMPTS.md         # Example prompts per skill
│   ├── QUICKSTART.md           # Quick start guide
│   └── SKILLCHAIN_WORKFLOW.md  # Workflow documentation
│
└── skillchains/                 # THEORETICAL DOCS (OUTDATED - Nov 13)
    ├── README.md               # Says "3/14 skills" - now 29!
    ├── GUIDE.md                # Usage guide (duplicates commands/README.md)
    ├── ROADMAP.md              # Outdated roadmap
    ├── TOKEN_EFFICIENCY.md     # Valuable - keep this
    ├── patterns/               # Patterns embedded in skillchain.md
    │   ├── hub-and-spoke.md
    │   ├── linear-chain.md
    │   └── parallel-composition.md
    ├── chains/                 # Chain definitions (superseded by skillchain.md)
    │   └── 6 chain files
    └── examples/               # Example code
```

### Problems Identified

| Issue | Location | Impact |
|-------|----------|--------|
| Claims "3/14 skills complete" | skillchains/README.md | Confusing - we have 29 |
| Duplicate keyword mappings | skillchains/ vs commands/ | Maintenance burden |
| Orphaned documentation | skillchains/ | Not referenced anywhere |
| Outdated chain definitions | skillchains/chains/ | Wrong skill counts |
| Duplicate patterns | patterns/ vs skillchain.md | Inconsistency |

---

## Proposed Solution

### Phase 1: Consolidate Documentation

**Action:** Remove `skillchains/` directory, preserve valuable content

```bash
# Move valuable content
mv skillchains/TOKEN_EFFICIENCY.md docs/architecture/

# Remove outdated directory
rm -rf skillchains/
```

**Rationale:**
- `TOKEN_EFFICIENCY.md` has valuable analysis - preserve in docs/
- Pattern documentation is now embedded in `commands/skillchain.md`
- Chain definitions superseded by skillchain.md keyword mapping
- GUIDE.md duplicates `commands/README.md`
- ROADMAP.md is outdated (Nov 13 dates, wrong skill counts)

### Phase 2: Add Helper Commands

**New command: `/skilllist`**

Purpose: Show all 29 skills organized by category

```markdown
---
description: "List all available skills organized by category"
allowed-tools: Read
---

# Available Skills (29 total)

## Frontend Skills (15)

### Foundation
- theming-components - Design tokens, dark mode, brand colors

### Data Display
- visualizing-data - 24+ chart types
- building-tables - Data grids, sorting, pagination
- creating-dashboards - Dashboard layouts, KPI cards

### User Input
- building-forms - 50+ input types, validation
- implementing-search-filter - Search, faceted filters

### Interaction
- building-ai-chat - AI chat interfaces, streaming
- implementing-drag-drop - Kanban, sortable lists
- providing-feedback - Toasts, alerts, loading states

### Structure
- implementing-navigation - Menus, tabs, routing
- designing-layouts - Grids, responsive design
- displaying-timelines - Activity feeds, history

### Content
- managing-media - File upload, galleries
- guiding-users - Onboarding, tutorials

### Assembly
- assembling-components - Component integration

## Backend Skills (14)

### Data
- ingesting-data - ETL, S3, APIs, CDC
- databases-relational - PostgreSQL, MySQL, SQLite
- databases-vector - Qdrant, pgvector, Pinecone
- databases-timeseries - ClickHouse, TimescaleDB
- databases-document - MongoDB, Firestore
- databases-graph - Neo4j, memgraph

### API
- api-patterns - REST, GraphQL, gRPC
- message-queues - Kafka, RabbitMQ, NATS
- realtime-sync - WebSockets, SSE, Y.js

### Platform
- observability - OpenTelemetry, LGTM
- auth-security - OAuth 2.1, passkeys
- deploying-applications - Kubernetes, serverless

### AI
- ai-data-engineering - RAG, embeddings
- model-serving - vLLM, BentoML

---

**Usage:**
- `/skillchain [goal]` - Guided workflow
- `/skillchain help` - Detailed help
```

**New command: `/skillhelp [skill-name]`**

Purpose: Get detailed help on a specific skill

```markdown
---
description: "Get detailed help on a specific skill. Usage: /skillhelp [skill-name]"
allowed-tools: Read, Glob
argument-hint: "[skill-name] e.g., 'building-forms', 'databases-vector'"
---

# Skill Help: $ARGUMENTS

Read the SKILL.md file for the specified skill and provide:
1. What it does
2. When to use it
3. Key features
4. Example usage

If skill not found, list similar skills.
```

### Phase 3: Simplify User Journey

**Update main README.md with clear entry points:**

```markdown
## Quick Start

### I want to build something
/skillchain dashboard with charts and filters

### I want to see all skills
/skillchain help

### I need backend help
/skillchain API with PostgreSQL and auth

### I need a specific skill
Just describe what you need - skills trigger automatically
```

### Phase 4: Organize demo/ Directory

**Rename demo/ to commands/reference/**

The demo/*.md files are skillchain reference documentation, not demos.

```bash
# Move reference docs into commands/
mv demo/KEYWORD_TRIGGERS.md commands/reference/
mv demo/DECISION_TREE.md commands/reference/
mv demo/USER_PROMPTS.md commands/reference/
mv demo/SKILLCHAIN_WORKFLOW.md commands/reference/

# Keep QUICKSTART.md in demo/ for actual demos
# Or move to docs/
```

---

## Implementation Checklist

### Phase 1: Consolidate (Do First)
- [ ] Create docs/architecture/ directory
- [ ] Move TOKEN_EFFICIENCY.md to docs/architecture/
- [ ] Delete skillchains/ directory
- [ ] Update any references to skillchains/

### Phase 2: Add Commands
- [ ] Create commands/skilllist.md
- [ ] Create commands/skillhelp.md
- [ ] Update install-skillchain.sh to install all commands

### Phase 3: Organize
- [ ] Create commands/reference/ directory
- [ ] Move demo/*.md to commands/reference/
- [ ] Update skillchain.md references
- [ ] Clean up demo/ (keep only actual demo code)

### Phase 4: Documentation
- [ ] Update main README.md with user journey
- [ ] Update commands/README.md with all commands
- [ ] Update CLAUDE.md with new structure

### Phase 5: Release
- [ ] Commit all changes
- [ ] Tag as v0.3.2
- [ ] Update CHANGELOG.md

---

## Expected Benefits

| Before | After |
|--------|-------|
| 3 locations for skillchain docs | 1 location (commands/) |
| Outdated "3/14 skills" references | Accurate "29 skills" |
| Confusing directory structure | Clear separation |
| Only `/skillchain` command | `/skillchain`, `/skilllist`, `/skillhelp` |
| Theory + Practice mixed | Practice for users, theory in docs/ |

---

## Decision Required

**Option A: Full Implementation**
- Do all 5 phases
- Most comprehensive
- Takes longest

**Option B: Minimal (Recommended)**
- Phase 1 (remove skillchains/)
- Phase 4 (update docs)
- Quick, cleans up confusion

**Option C: Staged**
- Phase 1 now
- Phases 2-3 in v0.4.0
- Phase 4-5 after testing

---

## Appendix: Files to Delete

```
skillchains/
├── README.md              # Outdated, duplicates commands/
├── GUIDE.md               # Duplicates commands/README.md
├── ROADMAP.md             # Outdated (Nov 13)
├── TOKEN_EFFICIENCY.md    # KEEP - move to docs/
├── patterns/
│   ├── hub-and-spoke.md   # Now in skillchain.md
│   ├── linear-chain.md    # Now in skillchain.md
│   └── parallel-composition.md  # Now in skillchain.md
├── chains/
│   ├── ai-chat-interface.md
│   ├── dashboard-full-stack.md
│   ├── data-viz-plus-forms.md
│   ├── design-tokens-to-data-viz.md
│   ├── design-tokens-to-forms.md
│   └── tables-data-viz-chain.md
└── examples/
    └── README.md
```

**Total: 14 files to delete, 1 to preserve**
