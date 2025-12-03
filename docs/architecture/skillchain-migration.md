# Skillchain v2.0 Implementation Plan

**Decisions Made:**
- ✅ Support ALL 29 skills (no blueprint shortcuts initially)
- ✅ Option C: Hybrid questions (simple inline, complex in SKILL.md)
- ✅ Clean break (no backward compatibility)

**Timeline:** 2-3 weeks (simplified from 4 weeks)

---

## Week 1: Structure & Registry

### Day 1: Create Directory Structure

```bash
cd commands/
mkdir -p skillchain/{_shared,categories,blueprints}
cd skillchain/

# Create placeholder files
touch _registry.yaml
touch _help.md
touch _shared/theming-rules.md
touch _shared/execution-flow.md
touch categories/frontend.md
touch categories/backend.md
touch categories/fullstack.md
touch categories/ai-ml.md
```

### Day 2-3: Build _registry.yaml

**Task:** Convert current keyword mappings to YAML structure

**Template to use:**

```yaml
# _registry.yaml
version: "1.0.0"
last_updated: "2024-12-02"

# Category definitions
categories:
  frontend:
    description: "UI components and interactions"
    default_tools: ["Read", "Write", "Skill"]
    
  backend:
    description: "APIs, databases, deployment"
    default_tools: ["Read", "Write", "Bash", "Skill"]
    
  fullstack:
    description: "Frontend + Backend combinations"
    default_tools: ["Read", "Write", "Bash", "Skill"]
    
  ai-ml:
    description: "AI/ML specific workflows"
    default_tools: ["Read", "Write", "Bash", "Skill"]

# Skills registry
skills:
  # FRONTEND SKILLS (15)
  
  theming-components:
    category: frontend
    group: foundation
    priority: 1
    required: true  # Always included for frontend
    
    keywords:
      primary: [theme, colors, brand, styling, tokens]
      secondary: [dark mode, palette, design system]
      exclusions: [api, database, backend]
    
    invocation: "ui-foundation-skills:theming-components"
    dependencies: []
    dependents: ["*"]  # All frontend depends on this
    
    questions:
      source: "inline"  # Simple skill, use inline defaults
      defaults:
        color_scheme: "blue-gray"
        theme_modes: ["light", "dark"]
        spacing_base: "8px"
    
    estimate_tokens: 200

  visualizing-data:
    category: frontend
    group: data-display
    priority: 5
    required: false
    
    keywords:
      primary: [chart, graph, visualize, plot, analytics]
      secondary: [bar, line, pie, donut, scatter]
      exclusions: []
    
    invocation: "ui-foundation-skills:visualizing-data"
    dependencies: ["theming-components"]
    
    questions:
      source: "skill"  # Complex skill, read from SKILL.md
      section: "## Skillchain Configuration"
    
    estimate_tokens: 350

  building-tables:
    category: frontend
    group: data-display
    priority: 5
    required: false
    
    keywords:
      primary: [table, grid, records, rows, columns]
      secondary: [data grid, list, pagination, sorting]
      exclusions: []
    
    invocation: "ui-foundation-skills:building-tables"
    dependencies: ["theming-components"]
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 300

  creating-dashboards:
    category: frontend
    group: data-display
    priority: 5
    required: false
    
    keywords:
      primary: [dashboard, admin, metrics, overview, analytics]
      secondary: [kpi, cards, widgets]
      exclusions: []
    
    invocation: "ui-foundation-skills:creating-dashboards"
    dependencies: ["theming-components", "designing-layouts"]
    
    questions:
      source: "inline"
      defaults:
        layout: "sidebar-grid"
        kpi_cards: 4
        responsive: true
    
    estimate_tokens: 250

  building-forms:
    category: frontend
    group: user-input
    priority: 6
    required: false
    
    keywords:
      primary: [form, input, validation, login, signup, register]
      secondary: [fields, submit, textarea, select]
      exclusions: []
    
    invocation: "ui-foundation-skills:building-forms"
    dependencies: ["theming-components"]
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 400

  implementing-search-filter:
    category: frontend
    group: user-input
    priority: 6
    required: false
    
    keywords:
      primary: [search, filter, find, query]
      secondary: [faceted, autocomplete, typeahead]
      exclusions: []
    
    invocation: "ui-foundation-skills:implementing-search-filter"
    dependencies: ["theming-components"]
    
    questions:
      source: "inline"
      defaults:
        realtime: true
        position: "top-right"
        scope: "all"
    
    estimate_tokens: 250

  building-ai-chat:
    category: frontend
    group: interaction
    priority: 7
    required: false
    
    keywords:
      primary: [chat, ai, assistant, chatbot, conversation]
      secondary: [streaming, messages, llm]
      exclusions: []
    
    invocation: "ui-foundation-skills:building-ai-chat"
    dependencies: ["theming-components", "building-forms"]
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 400

  implementing-drag-drop:
    category: frontend
    group: interaction
    priority: 7
    required: false
    
    keywords:
      primary: [drag, drop, sortable, reorder, move]
      secondary: [kanban, dnd, draggable]
      exclusions: []
    
    invocation: "ui-foundation-skills:implementing-drag-drop"
    dependencies: ["theming-components"]
    
    questions:
      source: "inline"
      defaults:
        library: "dnd-kit"
        touch_support: true
    
    estimate_tokens: 250

  providing-feedback:
    category: frontend
    group: interaction
    priority: 8
    required: false
    
    keywords:
      primary: [notification, toast, alert, loading, spinner]
      secondary: [feedback, skeleton, progress]
      exclusions: []
    
    invocation: "ui-foundation-skills:providing-feedback"
    dependencies: ["theming-components"]
    
    questions:
      source: "inline"
      defaults:
        toast_position: "top-right"
        loading_type: "skeleton"
    
    estimate_tokens: 200

  implementing-navigation:
    category: frontend
    group: structure
    priority: 4
    required: false
    
    keywords:
      primary: [navigation, menu, nav, tabs, routing]
      secondary: [sidebar, breadcrumb, links]
      exclusions: []
    
    invocation: "ui-foundation-skills:implementing-navigation"
    dependencies: ["theming-components"]
    
    questions:
      source: "inline"
      defaults:
        type: "sidebar"
        collapsible: true
    
    estimate_tokens: 250

  designing-layouts:
    category: frontend
    group: structure
    priority: 3
    required: false
    
    keywords:
      primary: [layout, grid, columns, structure, responsive]
      secondary: [flexbox, css grid, container]
      exclusions: []
    
    invocation: "ui-foundation-skills:designing-layouts"
    dependencies: ["theming-components"]
    
    questions:
      source: "inline"
      defaults:
        system: "css-grid"
        responsive: true
        breakpoints: ["sm", "md", "lg", "xl"]
    
    estimate_tokens: 250

  displaying-timelines:
    category: frontend
    group: structure
    priority: 6
    required: false
    
    keywords:
      primary: [timeline, activity, history, feed, events, log]
      secondary: [chronological, audit]
      exclusions: []
    
    invocation: "ui-foundation-skills:displaying-timelines"
    dependencies: ["theming-components"]
    
    questions:
      source: "inline"
      defaults:
        orientation: "vertical"
        timestamps: true
    
    estimate_tokens: 200

  managing-media:
    category: frontend
    group: content
    priority: 7
    required: false
    
    keywords:
      primary: [upload, file, image, gallery, media, video, audio]
      secondary: [attachment, dropzone]
      exclusions: []
    
    invocation: "ui-foundation-skills:managing-media"
    dependencies: ["theming-components"]
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 350

  guiding-users:
    category: frontend
    group: content
    priority: 8
    required: false
    
    keywords:
      primary: [onboarding, tutorial, guide, tour, tooltip, help, wizard]
      secondary: [walkthrough, hints]
      exclusions: []
    
    invocation: "ui-foundation-skills:guiding-users"
    dependencies: ["theming-components"]
    
    questions:
      source: "inline"
      defaults:
        type: "tooltips"
        dismissible: true
    
    estimate_tokens: 200

  assembling-components:
    category: frontend
    group: assembly
    priority: 99  # Always last
    required: true
    
    keywords:
      primary: [assemble, wire, integrate, scaffold, production]
      secondary: [validate, combine]
      exclusions: []
    
    invocation: "ui-foundation-skills:assembling-components"
    dependencies: ["*"]  # Depends on all previous skills
    
    questions:
      source: "inline"
      defaults:
        validate_tokens: true
        production_ready: true
    
    estimate_tokens: 300

  # BACKEND SKILLS (14)
  
  ingesting-data:
    category: backend
    group: data-ingestion
    priority: 5
    required: false
    
    keywords:
      primary: [ingest, import, etl, csv, extract, load, migration]
      secondary: [s3, bucket, cdc, dlt, pipeline]
      exclusions: []
    
    invocation: "backend-data-skills:ingesting-data"
    dependencies: []
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 400

  databases-relational:
    category: backend
    group: databases
    priority: 10
    required: false
    
    keywords:
      primary: [database, sql, postgres, mysql, sqlite]
      secondary: [orm, prisma, drizzle, sqlalchemy, rds]
      exclusions: []
    
    invocation: "backend-data-skills:databases-relational"
    dependencies: []
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 450

  databases-vector:
    category: backend
    group: databases
    priority: 10
    required: false
    
    keywords:
      primary: [vector, embedding, qdrant, pgvector, similarity]
      secondary: [rag, semantic search, pinecone]
      requires_any: [database, search, ai, rag]
    
    invocation: "backend-data-skills:databases-vector"
    dependencies: ["ingesting-data"]
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 450

  databases-timeseries:
    category: backend
    group: databases
    priority: 10
    required: false
    
    keywords:
      primary: [timeseries, metrics, clickhouse, influxdb, timescale]
      secondary: [prometheus, grafana, tsdb]
      exclusions: []
    
    invocation: "backend-data-skills:databases-timeseries"
    dependencies: []
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 400

  databases-document:
    category: backend
    group: databases
    priority: 10
    required: false
    
    keywords:
      primary: [nosql, mongo, document, firestore, dynamodb]
      secondary: [collection, json, bson]
      exclusions: []
    
    invocation: "backend-data-skills:databases-document"
    dependencies: []
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 400

  databases-graph:
    category: backend
    group: databases
    priority: 10
    required: false
    
    keywords:
      primary: [graph, neo4j, cypher, relationships, nodes, edges]
      secondary: [memgraph, knowledge graph]
      exclusions: []
    
    invocation: "backend-data-skills:databases-graph"
    dependencies: []
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 400

  api-patterns:
    category: backend
    group: apis
    priority: 5
    required: false
    
    keywords:
      primary: [api, rest, graphql, grpc, trpc]
      secondary: [fastapi, hono, axum, endpoints]
      exclusions: []
    
    invocation: "backend-data-skills:api-patterns"
    dependencies: []
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 450

  message-queues:
    category: backend
    group: messaging
    priority: 15
    required: false
    
    keywords:
      primary: [kafka, queue, message, event, rabbitmq, nats]
      secondary: [temporal, celery, pub-sub]
      exclusions: []
    
    invocation: "backend-data-skills:message-queues"
    dependencies: ["api-patterns"]
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 400

  realtime-sync:
    category: backend
    group: messaging
    priority: 15
    required: false
    
    keywords:
      primary: [websocket, realtime, streaming, sse, collaborative]
      secondary: [yjs, presence, live]
      exclusions: []
    
    invocation: "backend-data-skills:realtime-sync"
    dependencies: ["api-patterns"]
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 400

  auth-security:
    category: backend
    group: platform
    priority: 8
    required: false
    
    keywords:
      primary: [auth, login, security, jwt, oauth, authentication]
      secondary: [passkeys, webauthn, rbac, permissions]
      exclusions: []
    
    invocation: "backend-data-skills:auth-security"
    dependencies: ["api-patterns"]
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 450

  observability:
    category: backend
    group: platform
    priority: 20
    required: false
    
    keywords:
      primary: [monitoring, observability, logs, traces, opentelemetry]
      secondary: [otel, lgtm, metrics, prometheus]
      exclusions: []
    
    invocation: "backend-data-skills:observability"
    dependencies: []
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 400

  deploying-applications:
    category: backend
    group: platform
    priority: 25
    required: false
    
    keywords:
      primary: [deploy, kubernetes, k8s, serverless, helm]
      secondary: [lambda, vercel, cloudflare, docker]
      exclusions: []
    
    invocation: "backend-data-skills:deploying-applications"
    dependencies: []
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 450

  ai-data-engineering:
    category: backend
    group: ai-ml
    priority: 15
    required: false
    
    keywords:
      primary: [rag, embeddings, chunking, pipeline]
      secondary: [vector, indexing, semantic]
      requires_any: [ai, rag, llm, search]
    
    invocation: "backend-data-skills:ai-data-engineering"
    dependencies: ["databases-vector"]
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 450

  model-serving:
    category: backend
    group: ai-ml
    priority: 20
    required: false
    
    keywords:
      primary: [llm, model, serving, vllm, inference]
      secondary: [bentoml, ollama, mlops]
      requires_any: [ai, llm, model]
    
    invocation: "backend-data-skills:model-serving"
    dependencies: ["ai-data-engineering"]
    
    questions:
      source: "skill"
      section: "## Skillchain Configuration"
    
    estimate_tokens: 400
```

**Action Items for Day 2-3:**
1. Copy template above
2. Review each skill's keywords (adjust if needed)
3. Decide for each skill: `source: "inline"` or `source: "skill"`
   - **Rule of thumb:** < 5 questions = inline, 5+ questions = skill
4. For inline questions, add defaults YAML block

### Day 4: Extract Shared Resources

**Task:** Extract from current skillchain.md

```bash
# Extract theming rules (lines 715-929)
# Save to _shared/theming-rules.md

# Create execution-flow.md with common patterns:
cat > _shared/execution-flow.md << 'FLOW'
# Execution Flow Guidelines

## Skill Invocation Order

1. **Foundation First**: theming-components always runs first for frontend
2. **Structure Before Content**: layouts before components
3. **Data Before Display**: database before API
4. **Assembly Last**: assembling-components always runs last

## Question Asking Strategy

1. Present questions with context from previous skills
2. Show smart defaults based on user goal
3. Allow "skip" for any question
4. Confirm full chain before starting

## Workflow Commands

Available during any skill:
- "back" → Return to previous skill
- "skip" → Use defaults for current skill  
- "status" → Show progress (X/Y complete)
- "done" → Finish early with current config
- "restart" → Start over from beginning
FLOW
```

### Day 5: Extract Help Content

```bash
# Extract lines 1-126 from current skillchain.md
# Save to _help.md (the help guide box)
```

---

## Week 2: Router & Orchestrators

### Day 1-2: Write New skillchain.md (Router)

**Create the slim router:**

```markdown
---
description: "Start a guided skill chaining workflow to build full-stack applications. 29 skills covering frontend, backend, databases, and AI. Usage: /skillchain [goal]"
allowed-tools: Skill, Read, Write
argument-hint: "[goal] e.g., 'dashboard with charts', 'API with postgres', 'RAG pipeline'"
---

# Skill Chain Router v2.0

**Input:** $ARGUMENTS

---

## Step 1: Parse Command

If "$ARGUMENTS" is empty or "help":
  - Read and display commands/skillchain/_help.md
  - STOP and wait for user to provide goal
  - Example: `/skillchain dashboard with charts`

---

## Step 2: Load Registry

Read commands/skillchain/_registry.yaml and parse:
- categories: frontend, backend, fullstack, ai-ml
- skills: all 29 skill definitions
- metadata: keywords, dependencies, questions

---

## Step 3: Analyze Goal & Detect Category

### Extract Keywords from Goal
Parse "$ARGUMENTS" to extract:
- Nouns: dashboard, chart, api, database, form, etc.
- Verbs: deploy, upload, search, etc.
- Tech terms: postgres, react, kafka, qdrant, etc.

### Detect Primary Category

**Frontend indicators:**
[ui, form, dashboard, chart, component, interface, page, design, table, menu, navigation, layout, timeline, media, upload, drag, drop, toast, notification, loading]

**Backend indicators:**
[api, database, server, deploy, auth, queue, cache, sql, postgres, mongo, redis, kafka, webhook, endpoint, rest, graphql]

**AI/ML indicators:**
[rag, vector, embeddings, llm, agent, model, ai, chat, assistant, semantic, similarity]

**Fullstack indicators:**
Both frontend AND backend keywords present

**Category Detection Logic:**
```
IF (frontend keywords > 0 AND backend keywords > 0):
  category = fullstack
ELSE IF (ai/ml keywords > 0):
  category = ai-ml (might also trigger backend)
ELSE IF (frontend keywords > backend keywords):
  category = frontend
ELSE IF (backend keywords > 0):
  category = backend
ELSE:
  Ask user: "Is this frontend (UI), backend (API/DB), or fullstack?"
```

---

## Step 4: Match Skills

For each skill in registry where skill.category matches detected category:

**Scoring Algorithm:**
```
score = 0

# Primary keyword match (high confidence)
for keyword in skill.keywords.primary:
  if keyword in goal_keywords:
    score += 10

# Secondary keyword match (medium confidence)
for keyword in skill.keywords.secondary:
  if keyword in goal_keywords:
    score += 5

# Exclusion check (reject skill)
for keyword in skill.keywords.exclusions:
  if keyword in goal_keywords:
    score = 0
    break

# Requirement check (must have at least one)
if skill.keywords.requires_any exists:
  has_required = false
  for required in skill.keywords.requires_any:
    if required in goal_keywords:
      has_required = true
      break
  if not has_required:
    score = 0

# Add skill if scored
if score > 0:
  matched_skills.append({skill, score})
```

**Add Required Skills:**
- For frontend: Always include theming-components (priority 1)
- For all categories: Always include final assembly skill (priority 99)

**Sort Skills:**
```
Sort matched_skills by:
  1. priority (ascending)
  2. score (descending)
```

**Resolve Dependencies:**
```
for skill in matched_skills:
  for dependency in skill.dependencies:
    if dependency not in matched_skills:
      matched_skills.add(dependency)
      
Re-sort by priority after adding dependencies
```

---

## Step 5: Route to Category Orchestrator

Based on detected category, load orchestrator:

```bash
frontend  → Read commands/skillchain/categories/frontend.md
backend   → Read commands/skillchain/categories/backend.md
fullstack → Read commands/skillchain/categories/fullstack.md
ai-ml     → Read commands/skillchain/categories/ai-ml.md
```

**Pass Context to Orchestrator:**
- original_goal: "$ARGUMENTS"
- matched_skills: [list of skill objects with scores]
- category: detected category
- estimated_questions: sum of skill question counts
- estimated_time: "8-12 minutes" (calculate based on skill count)

---

## Step 6: Orchestrator Takes Control

The category orchestrator will:
1. Load shared resources (theming rules, execution flow)
2. Present skill chain to user for confirmation
3. Invoke each skill in priority order
4. Ask configuration questions
5. Pass all configs to final assembly skill

---

**Router Complete - Total Lines: ~120**
```

### Day 3-4: Write Category Orchestrators

**Frontend Orchestrator Template:**

```markdown
# Frontend Workflow Orchestrator

**Context Received:**
- Goal: {original_goal}
- Skills: {matched_skills}
- Category: frontend
- Estimated: {estimated_time}, {estimated_questions} questions

---

## Step 1: Load Shared Resources

Read commands/skillchain/_shared/theming-rules.md
Read commands/skillchain/_shared/execution-flow.md

Store in context for all skills.

---

## Step 2: Confirm Skill Chain with User

Present detected chain:

```
╔══════════════════════════════════════════════════════════╗
║  SKILL CHAIN DETECTED FOR: "{original_goal}"             ║
╠══════════════════════════════════════════════════════════╣
║  REQUIRED SKILLS (always included):                      ║
║    1. ✓ theming-components (foundation)                  ║
║                                                          ║
║  MATCHED FROM YOUR GOAL:                                 ║
{for each matched skill with score > 0:}
║    {n}. ◆ {skill.name} (matched: "{keyword}")            ║
║                                                          ║
║  ASSEMBLY (always included):                             ║
║    99. ✓ assembling-components (final step)              ║
╠══════════════════════════════════════════════════════════╣
║  Estimated time: {estimated_time}                        ║
║  Estimated questions: {estimated_questions}              ║
╠══════════════════════════════════════════════════════════╣
║  OPTIONS:                                                ║
║    • Type "confirm" to proceed                           ║
║    • Type "skip" to use all defaults (faster)            ║
║    • Type "customize" to add/remove skills               ║
║    • Type "help" to see workflow commands                ║
╚══════════════════════════════════════════════════════════╝
```

Wait for user response:
- "confirm" → Proceed to Step 3
- "skip" → Set skip_all_questions = true, proceed to Step 3
- "customize" → Allow skill additions/removals, then proceed
- "help" → Show workflow commands from execution-flow.md

---

## Step 3: Skill Invocation Loop

Initialize:
```
skill_configs = {}
current_skill_index = 1
```

For each skill in confirmed_skills:

### 3.1 Announce Skill
```
═══════════════════════════════════════════════════════════
 STEP {current_skill_index}/{total_skills}: {SKILL.NAME}
═══════════════════════════════════════════════════════════
```

### 3.2 Invoke Skill
```
Invoke {skill.invocation}
```

### 3.3 Load Questions

```python
if skill.questions.source == "inline":
  # Use defaults from registry
  questions = skill.questions.defaults
  
else if skill.questions.source == "skill":
  # Read from SKILL.md
  skill_md = Read /mnt/skills/public/{skill_name}/SKILL.md
  
  # Extract section
  section = extract_section(skill_md, skill.questions.section)
  
  # Parse questions from markdown
  questions = parse_questions(section)
```

### 3.4 Ask User (unless skip_all_questions)

If skip_all_questions:
  Use defaults for all questions
Else:
  For each question in questions:
    Present question with:
      - Context from previous skills
      - Smart defaults based on goal keywords
      - Current answer if revisiting (for "back" command)
    
    Wait for answer or workflow command:
      - Answer → Store and continue
      - "skip" → Use default for this question
      - "back" → Return to previous skill
      - "status" → Show progress, re-ask question
      - "done" → Break loop, proceed to assembly
      - "restart" → Go back to Step 2

### 3.5 Store Configuration
```
skill_configs[skill.name] = {
  answers: user_answers,
  invocation: skill.invocation,
  priority: skill.priority
}

current_skill_index += 1
```

---

## Step 4: Final Assembly

```
Invoke ui-foundation-skills:assembling-components with:
  - skill_configs: all collected configurations
  - original_goal: user's original goal
  - theming_rules: from shared resources
  - execution_flow: workflow guidelines
  
Generate complete, production-ready code.
```

---

## Error Handling

If skill invocation fails:
1. Log error
2. Ask user: "Skill {name} failed. Continue with remaining skills? (yes/no)"
3. If yes: Skip failed skill, continue
4. If no: Stop workflow, show partial progress

---

**Orchestrator Complete - Lines: ~150**
```

**Repeat for backend.md, fullstack.md, ai-ml.md** (similar structure, different skill loading logic)

### Day 5: Integration Testing

Test with 5 representative goals:

```bash
# Test 1: Pure Frontend
/skillchain dashboard with charts and tables

# Expected: frontend orchestrator, loads theming + visualizing + tables

# Test 2: Pure Backend
/skillchain REST API with PostgreSQL and auth

# Expected: backend orchestrator, loads api-patterns + databases-relational + auth-security

# Test 3: Fullstack
/skillchain dashboard with postgres backend

# Expected: fullstack orchestrator, loads frontend + backend skills

# Test 4: AI/ML
/skillchain RAG pipeline with vector search

# Expected: ai-ml orchestrator (or backend), loads vector DB + ai-data-engineering

# Test 5: Simple Frontend
/skillchain login form with validation

# Expected: frontend orchestrator, loads theming + forms + feedback
```

**Validation Checklist:**
- [ ] Router correctly detects category
- [ ] Skills matched based on keywords
- [ ] Required skills always included
- [ ] Dependencies auto-added
- [ ] Orchestrator loads shared resources
- [ ] Questions asked in order
- [ ] "skip" command works
- [ ] Final assembly receives all configs

---

## Week 3: Question Migration (Option C)

### Classification: Inline vs SKILL.md

**Review each skill and classify:**

**Inline Candidates (< 5 questions, simple choices):**
- theming-components (3 questions: color, theme modes, spacing)
- implementing-search-filter (3 questions: position, realtime, scope)
- implementing-drag-drop (2 questions: library, touch support)
- providing-feedback (2 questions: toast position, loading type)
- implementing-navigation (2 questions: type, collapsible)
- designing-layouts (3 questions: system, responsive, breakpoints)
- displaying-timelines (2 questions: orientation, timestamps)
- guiding-users (2 questions: type, dismissible)
- creating-dashboards (3 questions: layout, kpi cards, responsive)

**SKILL.md Candidates (5+ questions, complex configurations):**
- visualizing-data (10+ questions: chart types, library, colors, axes, legends, responsive, animations, data format, accessibility, export)
- building-tables (8+ questions: features, pagination, sorting, filtering, columns, row actions, responsive, export)
- building-forms (12+ questions: fields, validation, layout, submission, error handling, accessibility, progress, autocomplete)
- building-ai-chat (8+ questions: UI layout, streaming, message display, input handling, file uploads, markdown, code highlighting)
- managing-media (7+ questions: upload method, preview, file types, size limits, storage, compression, gallery)
- All backend skills (database configs, API specs, deployment settings)

### Day 1-3: Update SKILL.md Files (Complex Skills)

**For each complex skill, add to SKILL.md:**

```markdown
## Skillchain Configuration

### When This Skill Is Used

This skill is automatically included when your goal mentions:
- **Primary keywords:** {list from registry}
- **Secondary keywords:** {list from registry}

### Configuration Questions

> **📊 Chart Types Selection**
>
> Which chart types do you need?
> - [ ] Line chart (trends over time)
> - [ ] Bar chart (comparisons)
> - [ ] Pie/Donut chart (composition)
> - [ ] Area chart (cumulative values)
> - [ ] Scatter plot (correlations)
> - [ ] Heatmap (density)
>
> You can select multiple types.

> **🎨 Chart Library**
>
> Which charting library should we use?
> - **Recharts** (recommended): React-native, responsive, simple API
> - **Chart.js**: Feature-rich, canvas-based, excellent docs
> - **D3.js**: Maximum flexibility, steep learning curve
> - **Plotly**: Scientific/technical, 3D support
>
> Default: Recharts

{Continue with remaining questions...}

### Default Configuration

```yaml
chart_types: ["line", "bar"]
library: "recharts"
responsive: true
animations: true
theme_aware: true
accessibility: "full"
export_formats: ["png", "svg"]
data_format: "array-of-objects"
axes:
  x_axis: "category"
  y_axis: "value"
legend:
  position: "top-right"
  interactive: true
```

### Dependencies

This skill requires:
- theming-components (for colors and styling)

This skill is enhanced by:
- building-tables (for data exploration)
- creating-dashboards (for layout integration)
```

### Day 4-5: Update Inline Skills in Registry

**For simple skills, expand defaults in _registry.yaml:**

```yaml
theming-components:
  questions:
    source: "inline"
    defaults:
      color_scheme: "blue-gray"
      theme_modes: ["light", "dark"]
      spacing_base: "8px"
      font_family: "Inter"
      radius_scale: "medium"
    prompts:
      - question: "What color scheme fits your brand?"
        options:
          - "Corporate (blue-gray): Professional, trustworthy"
          - "Vibrant (purple-orange): Creative, energetic"
          - "Minimalist (monochrome): Clean, modern"
          - "Custom: I'll provide specific colors"
        answer_key: "color_scheme"
        
      - question: "Which theme modes should be supported?"
        options:
          - "Light mode only"
          - "Dark mode only"
          - "Both (recommended for accessibility)"
        answer_key: "theme_modes"
        
      - question: "What spacing system?"
        options:
          - "8px base (Material Design)"
          - "4px base (Tailwind)"
          - "Custom scale"
        answer_key: "spacing_base"
```

**Update orchestrators to parse inline prompts:**

```markdown
### 3.3 Ask User

If skill.questions.source == "inline":
  For each prompt in skill.questions.prompts:
    Display prompt.question
    Display prompt.options
    
    Get user answer
    Store in skill_configs[skill.name][prompt.answer_key]
    
    If answer is empty, use skill.questions.defaults[prompt.answer_key]
```

---

## Final Validation

### Before Deployment Checklist

- [ ] Router parses YAML correctly
- [ ] All 29 skills in registry
- [ ] All 4 orchestrators created
- [ ] Shared resources extracted
- [ ] Help file extracted
- [ ] Inline questions have prompts
- [ ] Complex skills have SKILL.md sections
- [ ] Dependencies resolve correctly
- [ ] Test all 5 example goals
- [ ] "skip" works for each question
- [ ] "back" navigates correctly
- [ ] "status" shows progress
- [ ] "done" exits early
- [ ] Final assembly receives all configs

### Success Metrics

**Token Reduction:**
- Before: 941 lines (~8K tokens)
- After: ~270 lines for frontend-only (~2.5K tokens)
- **Improvement: 71% reduction** ✅

**Maintenance:**
- Before: Edit 3+ locations to add skill
- After: Edit 1 location (_registry.yaml)
- **Improvement: 66% less work** ✅

**Scalability:**
- Before: O(n) linear growth
- After: O(1) router + O(k) category
- **Improvement: Sub-linear growth** ✅

---

## Post-Launch: Future Enhancements

### Phase 2: Blueprints (Optional, Later)

Once v2.0 is stable and you have usage data:

1. **Identify Top 3 Patterns** (based on actual user goals)
2. **Create Blueprint Files:**
   ```
   blueprints/
   ├── dashboard.md         # Most common pattern
   ├── crud-api.md          # Second most common
   └── rag-pipeline.md      # Emerging pattern
   ```

3. **Add Blueprint Detection to Router:**
   ```markdown
   ## Step 3.5: Detect Blueprint Match (Optional)
   
   If goal contains "dashboard with charts":
     Suggest blueprint:dashboard
   
   If goal contains "CRUD API" or "REST API with database":
     Suggest blueprint:crud-api
   
   Present to user:
   "I detected this matches our '{blueprint}' preset.
    Would you like to use preset defaults? (yes/no)"
   ```

### Phase 3: Advanced Features

- **Skill versioning** (track breaking changes)
- **Usage analytics** (which skills are most used)
- **Caching layer** (common combinations)
- **User preferences** (remember default answers)
- **Parallel skill loading** (independent skills)

---

## Implementation Timeline

| Week | Focus | Deliverables |
|------|-------|--------------|
| 1 | Structure & Registry | Directory structure, _registry.yaml, shared resources |
| 2 | Router & Orchestrators | New skillchain.md, 4 orchestrators, integration tests |
| 3 | Question Migration | SKILL.md sections (complex), inline prompts (simple) |

**Total: 3 weeks to v2.0 production release**

---

## Quick Reference: File Locations

```
commands/
└── skillchain/
    ├── skillchain.md              # 120-line router (was 941)
    ├── _registry.yaml             # All skill metadata
    ├── _help.md                   # Help system
    ├── _shared/
    │   ├── theming-rules.md       # CSS token requirements
    │   └── execution-flow.md      # Workflow patterns
    ├── categories/
    │   ├── frontend.md            # ~150 lines
    │   ├── backend.md             # ~150 lines
    │   ├── fullstack.md           # ~100 lines
    │   └── ai-ml.md               # ~100 lines
    └── blueprints/                # (Phase 2, optional)
        └── (empty for now)
```

---

## Questions?

As you implement, track:
- Which skills are actually used most (for future blueprint decisions)
- Which questions users "skip" most (candidates for better defaults)
- Any skills that should be split (too complex) or merged (too simple)
- Any missing keyword triggers (users expecting matches that don't happen)

This data will inform Phase 2 optimizations!