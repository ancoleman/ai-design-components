---
description: "Start a guided skill chaining workflow to build full-stack applications. 29 skills covering frontend, backend, databases, and AI. Usage: /skillchain [goal]"
allowed-tools: Skill, Read, Write, Bash
argument-hint: "[goal] e.g., 'dashboard with charts', 'API with postgres', 'RAG pipeline'"
---

# Skill Chain Router v2.0

**Input:** $ARGUMENTS

---

## Step 0: Locate Skillchain Directory (CRITICAL - DO THIS FIRST)

The skillchain command has multiple files. Find them by running this Bash command:

```bash
if [ -d ".claude/commands/skillchain" ]; then
  echo "$(pwd)/.claude/commands/skillchain"
elif [ -d "$HOME/.claude/commands/skillchain" ]; then
  echo "$HOME/.claude/commands/skillchain"
else
  echo "ERROR: skillchain directory not found"
fi
```

**Store the output path as SKILLCHAIN_DIR** - use it for ALL subsequent file reads in this workflow.

Example: If output is `/Users/john/.claude/commands/skillchain`, then:
- Help file: `/Users/john/.claude/commands/skillchain/_help.md`
- Registry: `/Users/john/.claude/commands/skillchain/_registry.yaml`
- Categories: `/Users/john/.claude/commands/skillchain/categories/frontend.md`

---

## Step 0.5: Load User Preferences

Check if user has saved preferences from previous workflows:

```bash
if [ -f "$HOME/.claude/skillchain-prefs.yaml" ]; then
  PREFS_FILE="$HOME/.claude/skillchain-prefs.yaml"
  echo "✓ Loaded preferences from $PREFS_FILE"
else
  PREFS_FILE=""
  echo "ℹ No saved preferences found (will use defaults)"
fi
```

If PREFS_FILE exists:
- Read `{PREFS_FILE}` and store as USER_PREFS
- USER_PREFS will be passed to orchestrators for smart defaults
- See `{SKILLCHAIN_DIR}/_shared/preferences.md` for full schema

**Preference Priority:**
1. User's explicit choice (current workflow) - Highest
2. Saved preferences (from ~/.claude/skillchain-prefs.yaml) - Medium
3. Default values (from skill definitions) - Lowest

---

## Step 1: Parse Command

If "$ARGUMENTS" is empty or "help":
  - Read and display `{SKILLCHAIN_DIR}/_help.md`
  - STOP and wait for user to provide goal
  - Example: `/skillchain dashboard with charts`

---

## Step 2: Load Registry

Read `{SKILLCHAIN_DIR}/_registry.yaml` and parse:
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

## Step 3.5: Detect Blueprint Match (Optional Shortcut)

Check if the user's goal matches a pre-configured blueprint for faster workflow.

**Blueprint Detection:**

| Blueprint | Trigger Patterns | Confidence Threshold |
|-----------|------------------|---------------------|
| dashboard | "dashboard", "analytics", "admin panel", "KPI", "metrics overview" | 70% |
| crud-api | "REST API", "CRUD", "backend API", "FastAPI with database" | 70% |
| rag-pipeline | "RAG", "semantic search", "vector search", "document Q&A", "knowledge base" | 70% |

**Detection Algorithm:**
```
for each blueprint in {SKILLCHAIN_DIR}/blueprints/:
  score = 0
  for keyword in blueprint.trigger_keywords:
    if keyword in goal (case-insensitive):
      score += weight(keyword)

  if score >= confidence_threshold:
    matched_blueprint = blueprint
    break
```

**If Blueprint Matched:**
```
Present to user:
"🎯 I detected this matches our '{blueprint}' preset!

This blueprint provides:
- Pre-configured skill chain
- Optimized defaults
- Only 3-4 questions instead of 12+

Would you like to use the {blueprint} blueprint? (yes/no/customize)"
```

**User Response:**
- "yes" → Read `{SKILLCHAIN_DIR}/blueprints/{blueprint}.md` and use its configuration
- "no" → Continue to Step 4 (normal skill matching)
- "customize" → Load blueprint but allow modifications

**If No Blueprint Matched:**
- Continue directly to Step 4

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
frontend  → Read {SKILLCHAIN_DIR}/categories/frontend.md
backend   → Read {SKILLCHAIN_DIR}/categories/backend.md
fullstack → Read {SKILLCHAIN_DIR}/categories/fullstack.md
ai-ml     → Read {SKILLCHAIN_DIR}/categories/ai-ml.md
```

**Pass Context to Orchestrator:**
- original_goal: "$ARGUMENTS"
- matched_skills: [list of skill objects with scores]
- category: detected category
- estimated_questions: sum of skill question counts
- estimated_time: "8-12 minutes" (calculate based on skill count)
- user_prefs: USER_PREFS (if PREFS_FILE exists, otherwise null)

---

## Step 6: Orchestrator Takes Control

The category orchestrator will:
1. Load shared resources (theming rules, execution flow)
2. Present skill chain to user for confirmation
3. Apply user preferences as smart defaults
4. Invoke each skill in priority order
5. Ask configuration questions (using preferences when available)
6. Pass all configs to final assembly skill
7. Collect preference choices for saving

---

## Step 7: Save Preferences (After Workflow Complete)

After successful workflow completion, offer to save preferences:

```
✓ Workflow complete! Your application is ready.

Would you like to save these preferences for next time?
  Options:
    - yes (save all choices)
    - selective (choose what to save)
    - no (don't save)
```

**If user chooses to save:**

1. Read existing preferences (if file exists)
2. Merge new preferences with existing ones
3. Update last_updated timestamp
4. Write to `~/.claude/skillchain-prefs.yaml`
5. Confirm: "✓ Preferences saved!"

**What to save:**
- Global preferences (theme, frameworks, AI/ML providers)
- Blueprint configuration (if blueprint was used)
- Skill-specific choices (for each skill that was used)

See `{SKILLCHAIN_DIR}/_shared/preferences.md` for complete saving logic.

---

**Router Complete - Total Lines: ~150**
