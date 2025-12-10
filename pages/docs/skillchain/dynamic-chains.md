---
sidebar_position: 5
title: Dynamic Skill Chains
description: Build custom skill chains without pre-defined blueprints
---

# Dynamic Skill Chains

When your goal doesn't match a pre-defined blueprint, Skillchain can dynamically build a custom skill chain by analyzing your requirements and selecting relevant skills from the registry.

## Overview

Dynamic skill chains provide:

- **Flexibility** - Handle any goal, even without a matching blueprint
- **Intelligence** - Skills selected based on keyword relevance scoring
- **Reliability** - >80% skill activation rate through execution protocol
- **Transparency** - User approves chain before execution

## How It Works

### 1. Blueprint Check

When you run `/skillchain:start [goal]`, the system first tries to match your goal to existing blueprints (dashboard, crud-api, rag-pipeline, etc.).

### 2. Dynamic Selection Offer

If no blueprint matches with sufficient confidence:

```
No pre-defined blueprint matched your goal: "build a custom analytics platform"

Options:
1. Dynamic Selection - I'll analyze your goal and build a custom skill chain
2. Manual Matching - Continue with standard keyword matching
3. List Blueprints - Show available blueprints to choose from

Recommended: Option 1 (Dynamic Selection) for novel or complex goals

Your choice (1/2/3):
```

### 3. Skill Scoring

The dynamic orchestrator loads all skill registries and scores each skill against your goal:

| Score | Meaning |
|-------|---------|
| 6+ | Strong match - definitely include |
| 3-5 | Good match - likely include |
| 1-2 | Weak match - consider if related |
| 0 | No match - exclude |

**Scoring algorithm:**
- Primary keyword match: +3 points
- Secondary keyword match: +1 point
- Partial word match: +2 points

### 4. Dependency Resolution

Skills are ordered by tier and dependencies:

1. **Foundation** - Base capabilities (theming, API patterns)
2. **Component** - Individual features (forms, tables, databases)
3. **Integration** - Cross-cutting (observability, testing)
4. **Assembly** - Final wiring (assembling-components)

### 5. User Approval

Before execution, you see the proposed chain:

```
Dynamic Skill Chain Generated

Goal: "build a custom analytics platform"

Foundation:
  1. theming-components (score: 6) - Design tokens and theming

Core Skills:
  2. visualizing-data (score: 5) - Charts and graphs
  3. building-tables (score: 4) - Data tables
  4. creating-dashboards (score: 5) - Dashboard layout

Assembly:
  5. assembling-components - Wire components together

Total Skills: 5
Estimated Questions: 10-15

Proceed? (yes / modify / cancel)
```

### 6. Execution

Once approved, the system enters **Execution Phase** and invokes each skill in sequence using the Skill tool.

## Activation Rate Guarantee

A key goal of dynamic chains is achieving **>80% skill activation rate** - meaning at least 80% of approved skills actually get invoked.

This is achieved through:

### Execution Protocol

The system follows a strict protocol defined in `execution-protocol.md`:

1. **Phase Separation** - Selection phase (no invocations) vs Execution phase (invocations only)
2. **Mandatory Invocation** - Every approved skill MUST be invoked
3. **Progress Tracking** - Visual tracker maintained throughout
4. **Verification Checkpoints** - After each skill, verify it was actually invoked

### Commitment Statement

Before execution begins:

```
Entering EXECUTION PHASE

I will invoke these skills using the Skill tool:
1. Skill: ui-foundation-skills:theming-components
2. Skill: ui-data-skills:visualizing-data
3. Skill: ui-data-skills:building-tables
4. Skill: ui-data-skills:creating-dashboards
5. Skill: ui-assembly-skills:assembling-components

Beginning execution now.
```

### Execution Tracker

Progress is tracked visually:

```
## Skill Chain Execution Tracker

| # | Skill | Status |
|---|-------|--------|
| 1 | theming-components | COMPLETE |
| 2 | visualizing-data | INVOKE NOW |
| 3 | building-tables | PENDING |
| 4 | creating-dashboards | PENDING |
| 5 | assembling-components | PENDING |

Current: visualizing-data
Next Action: INVOKE
```

### Final Report

After execution completes:

```
Dynamic Skill Chain Complete

Execution Summary:
  Skills Approved: 5
  Skills Invoked: 5
  Skills Skipped: 0
  Activation Rate: 100%

Files Generated:
  - src/theme/tokens.css
  - src/components/Chart.tsx
  - src/components/DataTable.tsx
  - src/components/Dashboard.tsx
  - src/App.tsx
```

## Skill Dependency Graph

The dynamic orchestrator uses a skill dependency graph (`skill-graph.yaml`) to ensure proper ordering:

```yaml
skills:
  building-forms:
    tier: component
    domain: frontend
    depends_on:
      soft: [theming-components]
    provides:
      - form-components
      - validation

  assembling-components:
    tier: assembly
    domain: frontend
    depends_on:
      requires_any:
        - building-forms
        - building-tables
        - visualizing-data
```

### Domain Rules

Each domain has default rules:

| Domain | Start With | End With |
|--------|------------|----------|
| Frontend | theming-components | assembling-components |
| Backend | implementing-api-patterns (optional) | implementing-observability (optional) |
| Infrastructure | - | security-hardening (optional) |

## When to Use Dynamic Chains

**Good candidates for dynamic selection:**
- Novel or unique project requirements
- Goals that span multiple domains
- Prototyping with uncertain scope
- Learning/exploring available skills

**Better with blueprints:**
- Common patterns (dashboard, CRUD API, RAG)
- Production projects with clear requirements
- When you want optimized defaults

## Error Handling

### Skill Invocation Failure

```
Skill invocation failed: visualizing-data
Error: Skill file not found

Options:
1. Retry invocation
2. Skip this skill (user must confirm)
3. Stop execution

Choice:
```

### User-Requested Skip

If you want to skip a skill:

```
Skip requested for: building-tables

This skill provides: data-tables, sorting, pagination
Skipping may result in: No table components in output

Confirm skip? (yes/no)
```

Only after confirmation is the skill marked as SKIPPED.

## Technical Details

### Files Created

| File | Purpose |
|------|---------|
| `execution-protocol.md` | Defines high-activation guarantees |
| `dynamic.md` | Dynamic orchestrator implementation |
| `skill-graph.yaml` | Skill dependencies and tiers |

### Locations

- Commands: `~/.claude/commands/skillchain/categories/dynamic.md`
- Data: `~/.claude/skillchain-data/shared/`

### Key Concepts

- **Selection Phase**: Analysis and chain building (no skill invocations)
- **Execution Phase**: Skill invocation only (no skipping without consent)
- **Activation Rate**: % of approved skills actually invoked (target: >80%)
- **Verification Checkpoint**: Post-invocation check before proceeding

## See Also

- [Skillchain Architecture](./architecture.md) - Overall system design
- [Blueprints](./blueprints.md) - Pre-defined skill chains
- [Chain Context](./chain-context.md) - State management during execution
