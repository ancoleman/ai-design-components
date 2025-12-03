# Deep Analysis: skillchain.md Scaling

## Current State Metrics

| Metric | Current Value | At 50 Skills | At 100 Skills | At 200 Skills |
|--------|---------------|--------------|---------------|---------------|
| Lines in skillchain.md | 941 | ~1,700 | ~3,300 | ~6,600 |
| Keyword mappings | ~25 rows | ~45 rows | ~90 rows | ~180 rows |
| Skill questions | ~350 lines | ~650 lines | ~1,250 lines | ~2,500 lines |
| Tokens (estimated) | ~8,000 | ~15,000 | ~30,000 | ~60,000 |

---

## Architectural Problems Identified

### 1. Monolithic Loading

Every `/skillchain` invocation loads 941 lines regardless of request complexity. A simple "login form" loads all backend database questions, AI/ML skill mappings, and deployment configurations.

### 2. Linear Growth Pattern

Each new skill adds ~33 lines:
- 5 lines: keyword mapping
- 3 lines: invocation reference
- 25 lines: configuration questions

### 3. Context Dilution

Critical instructions (theming rules, execution flow) get buried between skill-specific content. As the file grows, AI models increasingly "lose" important rules mid-document.

### 4. Maintenance Fragility

Adding a skill requires editing 3+ locations in skillchain.md, plus potentially DECISION_TREE.md, KEYWORD_TRIGGERS.md.

---

## Proposed Architecture: Hierarchical Tree Router

```
commands/
└── skillchain.md              # SLIM ROUTER (~120 lines)
    └── Reads → commands/skillchain/

commands/skillchain/
├── _registry.yaml             # Machine-readable skill metadata
├── _shared/
│   ├── theming-rules.md       # Extracted (always loaded for frontend)
│   ├── execution-flow.md      # Common execution patterns
│   └── question-format.md     # Standard question templates
│
├── categories/
│   ├── frontend.md            # Frontend orchestrator (~150 lines)
│   ├── backend.md             # Backend orchestrator (~150 lines)
│   ├── fullstack.md           # Cross-domain patterns (~100 lines)
│   └── ai-ml.md               # AI/ML specific patterns (~100 lines)
│
└── blueprints/                # Pre-composed chains (fast path)
    ├── dashboard.md           # theming → layouts → viz → tables
    ├── crud-api.md            # api → db → auth
    ├── rag-pipeline.md        # ingest → vectors → ai-data → serving
    ├── auth-flow.md           # forms → api → auth-security
    ├── chat-app.md            # ai-chat → realtime → forms
    └── monitoring-stack.md    # dashboards → timeseries → observability
```

---

## Core Principles

### 1. Slim Entry Point

skillchain.md becomes ~120 lines:
- Parse goal
- Read `_registry.yaml` to identify required skills
- Determine category (frontend/backend/fullstack)
- Route to category orchestrator or blueprint

### 2. Lazy Loading

Category orchestrators only load when needed:
- `"login form"` → loads only `frontend.md`
- `"postgres API"` → loads only `backend.md`
- `"dashboard with postgres"` → loads `fullstack.md`

### 3. Machine-Readable Registry

```yaml
# _registry.yaml
skills:
  theming-components:
    category: frontend
    group: foundation
    keywords: [theme, colors, brand, dark mode, styling, tokens]
    invocation: ui-foundation-skills:theming-components
    dependencies: []
    questions_in_skill: true  # Questions live in SKILL.md

  databases-vector:
    category: backend
    group: data
    keywords: [vector, embedding, rag, semantic, qdrant, pgvector]
    invocation: backend-data-skills:databases-vector
    dependencies: [ingesting-data]  # Optional dependency
    questions_in_skill: true

# ... all 29+ skills
```

### 4. Blueprint Shortcuts

Common patterns get pre-composed chains:

```markdown
# blueprints/dashboard.md
## Dashboard Blueprint

Skill Chain: theming → layouts → dashboards → visualizing → tables → forms → feedback → assembling

Default Questions (skip with "defaults"):
- Brand color: default blue
- Theme: light + dark
- Layout: sidebar + grid
- Charts: line + bar
...
```

### 5. Questions Move to Skills

Each SKILL.md gets a new section:

```markdown
## Skillchain Integration

### Configuration Questions
> **📊 Chart Configuration**
>
> Based on your goal, what data are you visualizing?
> - Describe your metrics (revenue, users, etc.)
> - Time period? (daily, monthly, yearly)
> - Comparison type? (trends, categories, composition)

### Defaults
- Chart library: Recharts
- Responsive: true
- Accessibility: full ARIA
```

---

## Comparison: Current vs. Proposed

| Aspect | Current | Proposed |
|--------|---------|----------|
| Initial context load | 941 lines (8K tokens) | ~120 lines (~1K tokens) |
| Frontend-only request | Loads ALL skills | Loads frontend.md only (~150 lines) |
| Adding new skill | Edit 3+ places in one file | Add to _registry.yaml + category file |
| Common patterns | Parsed fresh each time | Blueprint shortcut (~50 lines) |
| Skill questions | Duplicated in skillchain.md | Single source in SKILL.md |
| Scalability | O(n) linear growth | O(1) router + O(k) category (k << n) |

---

## Implementation Phases

### Phase 1: Extract & Restructure

- [ ] Create `commands/skillchain/` directory
- [ ] Extract `_registry.yaml` from current keyword mappings
- [ ] Extract `_shared/theming-rules.md` (lines 715-929)
- [ ] Create category orchestrators from current skill groupings

### Phase 2: Slim the Router

- [ ] Rewrite skillchain.md as lightweight router
- [ ] Implement YAML parsing logic
- [ ] Add category routing logic
- [ ] Test backward compatibility

### Phase 3: Build Blueprints

- [ ] Identify top 5-6 common patterns from usage
- [ ] Create blueprint files with sensible defaults
- [ ] Add "fast path" detection in router

### Phase 4: Migrate Questions

- [ ] Add `## Skillchain Integration` section to each SKILL.md
- [ ] Move questions from skillchain.md to respective skills
- [ ] Update orchestrators to read questions from skills

---

## Decision Point

Before proceeding, I need your input:

### 1. Blueprint Priority

Which patterns do you see users requesting most?

- [ ] Dashboard (analytics)
- [ ] CRUD API (REST + DB)
- [ ] RAG Pipeline (AI search)
- [ ] Auth Flow (login/signup)
- [ ] Chat App (real-time)
- [ ] Other?

### 2. Registry Format

Preference?

- [ ] **YAML** (human-readable, easy to edit)
- [ ] **JSON** (faster parsing, tool-friendly)
- [ ] **Markdown tables** (simpler, no new format)

### 3. Question Location

Where should skill-specific questions live?

- [ ] **A) Stay in category orchestrators** (current pattern, centralized)
- [ ] **B) Move to SKILL.md files** (single source of truth, distributed)
- [ ] **C) Hybrid** (defaults in SKILL.md, overrides in orchestrators)
