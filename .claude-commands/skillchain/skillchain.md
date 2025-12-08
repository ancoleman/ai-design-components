---
description: "Start a guided skill chaining workflow to build full-stack applications. 76 skills across 10 domains: frontend, backend, devops, infrastructure, security, developer, data, ai-ml, cloud, finops. Usage: /skillchain [goal]"
allowed-tools: Skill, Read, Write, Bash
argument-hint: "[goal] e.g., 'dashboard with charts', 'kubernetes with monitoring', 'RAG pipeline', 'CI/CD pipeline'"
---

# Skill Chain Router v3.0

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
- Help file: `/Users/john/.claude/commands/skillchain/help.md`
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
  - Read and display `{SKILLCHAIN_DIR}/help.md`
  - STOP and wait for user to provide goal
  - Example: `/skillchain dashboard with charts`

---

## Step 2: Load Registry Index

Read `{SKILLCHAIN_DIR}/_registries/_index.yaml` and parse:
- domains: 10 domain registries (frontend, backend, devops, infrastructure, security, developer, data, ai-ml, cloud, finops)
- total_skills: 76
- cross-domain mappings: fullstack, multi-domain

---

## Step 3: Analyze Goal & Detect Domain(s)

### Extract Keywords from Goal
Parse "$ARGUMENTS" to extract:
- Nouns: dashboard, chart, api, database, kubernetes, terraform, etc.
- Verbs: deploy, upload, search, secure, monitor, etc.
- Tech terms: postgres, react, kafka, qdrant, aws, etc.

### Domain Detection Keywords

**Frontend:** [ui, form, dashboard, chart, component, interface, page, design, table, menu, navigation, layout, timeline, media, upload, drag, drop, toast, notification]

**Backend:** [api, database, server, auth, queue, cache, sql, postgres, mongo, redis, kafka, webhook, endpoint, rest, graphql, realtime]

**DevOps:** [ci, cd, pipeline, test, docker, dockerfile, gitops, argocd, incident, platform, jenkins, github actions]

**Infrastructure:** [kubernetes, k8s, terraform, ansible, linux, nginx, network, load balancer, dns, service mesh, istio, distributed]

**Security:** [security, tls, ssl, firewall, compliance, soc2, vulnerability, siem, hardening, encryption, zero trust]

**Developer:** [cli, sdk, api design, documentation, debug, git, workflow, github actions]

**Data:** [etl, pipeline, streaming, kafka, sql optimization, data architecture, secret, vault, performance]

**AI/ML:** [rag, vector, embeddings, llm, agent, model, ai, chat, mlops, prompt, evaluation]

**Cloud:** [aws, gcp, azure, lambda, s3, ec2, cloud functions, cloud run]

**FinOps:** [cost, budget, tagging, finops, optimization, spend]

### Domain Detection Logic
```
detected_domains = []
for each domain in [frontend, backend, devops, infrastructure, security, developer, data, ai-ml, cloud, finops]:
  score = count(domain_keywords in goal)
  if score > 0:
    detected_domains.append({domain, score})

sort detected_domains by score descending

IF len(detected_domains) == 0:
  Ask user: "Which domain is this for? (frontend/backend/devops/infrastructure/security/...)"
ELSE IF len(detected_domains) == 1:
  category = detected_domains[0]
ELSE IF detected_domains contains ONLY [frontend, backend]:
  category = fullstack
ELSE IF len(detected_domains) <= 3:
  category = multi-domain
ELSE:
  Ask user to narrow scope
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

## Step 5: Route to Domain Orchestrator

Based on detected domain(s), load the appropriate orchestrator:

```bash
# Single domain routing
frontend        → Read {SKILLCHAIN_DIR}/categories/frontend.md
backend         → Read {SKILLCHAIN_DIR}/categories/backend.md
devops          → Read {SKILLCHAIN_DIR}/categories/devops.md
infrastructure  → Read {SKILLCHAIN_DIR}/categories/infrastructure.md
security        → Read {SKILLCHAIN_DIR}/categories/security.md
developer       → Read {SKILLCHAIN_DIR}/categories/developer.md
data            → Read {SKILLCHAIN_DIR}/categories/data.md
ai-ml           → Read {SKILLCHAIN_DIR}/categories/ai-ml.md
cloud           → Read {SKILLCHAIN_DIR}/categories/cloud.md
finops          → Read {SKILLCHAIN_DIR}/categories/finops.md

# Multi-domain routing
fullstack       → Read {SKILLCHAIN_DIR}/categories/fullstack.md      # frontend + backend
multi-domain    → Read {SKILLCHAIN_DIR}/categories/multi-domain.md   # 3+ domains
```

**Pass Context to Orchestrator:**
- original_goal: "$ARGUMENTS"
- detected_domains: [list of detected domains with scores]
- matched_skills: [list of skill objects from domain registry]
- primary_domain: highest-scoring domain
- estimated_questions: sum of skill question counts
- estimated_time: calculate based on skill count (3-5 min per skill)
- user_prefs: USER_PREFS (if PREFS_FILE exists, otherwise null)
- registry_path: "{SKILLCHAIN_DIR}/_registries/{domain}.yaml"

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
