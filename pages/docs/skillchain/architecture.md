---
sidebar_position: 5
title: Architecture
description: How skillchain v3.0 works internally
---

# Skillchain Architecture

Skillchain v3.0 uses a **separated architecture** that keeps command files (exposed as slash commands) separate from data files (registries, shared resources). This prevents internal files from appearing as unwanted commands.

## Core Concepts

### 1. Separated Directory Structure

The key innovation in v3.0 is separating commands from data:

```
~/.claude/
├── commands/
│   └── skillchain/                    # Commands (exposed as /skillchain:*)
│       ├── start.md                   # /skillchain:start (main entry)
│       ├── help.md                    # /skillchain:help
│       ├── blueprints/                # /skillchain:blueprints:*
│       │   ├── dashboard.md
│       │   ├── crud-api.md
│       │   └── ... (12 total)
│       └── categories/                # /skillchain:categories:*
│           ├── frontend.md
│           ├── backend.md
│           ├── devops.md
│           ├── infrastructure.md
│           ├── security.md
│           ├── developer.md
│           ├── data.md
│           ├── ai-ml.md
│           ├── cloud.md
│           ├── finops.md
│           ├── fullstack.md
│           └── multi-domain.md
│
└── skillchain-data/                   # Data (NOT exposed as commands)
    ├── registries/
    │   ├── _index.yaml
    │   ├── frontend.yaml
    │   ├── backend.yaml
    │   └── ... (10 domain registries)
    └── shared/
        ├── preferences.md
        ├── theming-rules.md
        └── execution-flow.md
```

**Why this matters:**
- Every `.md` file in `commands/` becomes a slash command
- There's **no mechanism** to hide files with underscore prefix
- Solution: Keep data files outside `commands/` directory entirely

### 2. Domain Registry System

Instead of a single `_registry.yaml`, v3.0 uses domain-specific registries:

```yaml
# registries/_index.yaml
version: "3.0.0"
total_skills: 76

domains:
  frontend:
    file: "frontend.yaml"
    skill_count: 15
    orchestrator: "categories/frontend.md"

  backend:
    file: "backend.yaml"
    skill_count: 14
    orchestrator: "categories/backend.md"

  devops:
    file: "devops.yaml"
    skill_count: 6
    orchestrator: "categories/devops.md"

  # ... 7 more domains
```

Each domain registry contains skill definitions:

```yaml
# registries/devops.yaml
domain: devops
version: "1.0.0"
plugin_group: devops-skills

skills:
  writing-dockerfiles:
    priority: 3
    keywords:
      primary: [docker, dockerfile, container, image]
      secondary: [multi-stage, buildkit, layer]
    invocation: "devops-skills:writing-dockerfiles"
    dependencies: []
    version: "1.0.0"
```

### 3. Dynamic Path Discovery

Skillchain works from any installation location:

```bash
# Step 0 in start.md (executed first, every time)

# Find commands directory
if [ -d ".claude/commands/skillchain" ]; then
  SKILLCHAIN_CMD="$(pwd)/.claude/commands/skillchain"
elif [ -d "$HOME/.claude/commands/skillchain" ]; then
  SKILLCHAIN_CMD="$HOME/.claude/commands/skillchain"
fi

# Find data directory (separate from commands)
if [ -d ".claude/skillchain-data" ]; then
  SKILLCHAIN_DATA="$(pwd)/.claude/skillchain-data"
elif [ -d "$HOME/.claude/skillchain-data" ]; then
  SKILLCHAIN_DATA="$HOME/.claude/skillchain-data"
fi
```

All file references use:
- `{SKILLCHAIN_CMD}/...` for commands (blueprints, categories, help)
- `{SKILLCHAIN_DATA}/...` for data (registries, shared)

## System Flow

The complete workflow from user input to generated code:

1. **Step 0:** Locate Directories - Find `skillchain/` and `skillchain-data/`
2. **Step 0.5:** Load User Preferences - Load saved choices as defaults
3. **Step 1:** Parse Command - Handle "help" or continue with goal
4. **Step 2:** Load Registry Index - Parse `registries/_index.yaml`
5. **Step 3:** Analyze Goal & Detect Domain(s) - Extract keywords, determine domain(s)
6. **Step 3.5:** Detect Blueprint Match - Check if goal matches a blueprint pattern
7. **Step 4:** Match Skills - Load domain registry, find relevant skills
8. **Step 5:** Route to Orchestrator - Load appropriate category orchestrator
9. **Step 6:** Orchestrator Execution - Invoke skills, ask questions, generate code
10. **Step 7:** Save Preferences - Offer to save choices for next time

## Domain Routing

### 10 Single-Domain Orchestrators

| Domain | Skills | Focus |
|--------|--------|-------|
| frontend | 15 | UI components, forms, charts |
| backend | 14 | APIs, databases, messaging |
| devops | 6 | CI/CD, Docker, GitOps |
| infrastructure | 12 | Kubernetes, Terraform, networking |
| security | 7 | Compliance, TLS, firewalls |
| developer | 7 | APIs, CLIs, SDKs |
| data | 6 | ETL, streaming, SQL |
| ai-ml | 4 | MLOps, prompts, evaluation |
| cloud | 3 | AWS, GCP, Azure |
| finops | 2 | Cost optimization |

### Multi-Domain Orchestrators

| Orchestrator | When Used |
|--------------|-----------|
| fullstack | frontend + backend detected |
| multi-domain | 3+ domains detected |

### Domain Detection Logic

```python
detected_domains = []

for domain in [frontend, backend, devops, infrastructure, ...]:
  score = count(domain_keywords in goal)
  if score > 0:
    detected_domains.append({domain, score})

sort detected_domains by score descending

if len(detected_domains) == 0:
  ask_user("Which domain?")
elif len(detected_domains) == 1:
  route_to_single_domain()
elif detected_domains == [frontend, backend]:
  route_to_fullstack()
elif len(detected_domains) <= 3:
  route_to_multi_domain()
else:
  ask_user("Too broad, please narrow scope")
```

## Parallel Loading

Skills are assigned to `parallel_group` in registry:

```yaml
skills:
  theming-components:
    parallel_group: 1  # Always first (foundation)

  designing-layouts:
    parallel_group: 2  # After theming

  visualizing-data:
    parallel_group: 3  # Can run with building-tables
    dependencies: ["theming-components"]

  building-tables:
    parallel_group: 3  # Same group = parallel!
    dependencies: ["theming-components"]

  assembling-components:
    parallel_group: 99  # Always last
```

**Rules:**
- Skills in same `parallel_group` run concurrently
- Dependencies must be in earlier groups
- Foundation skills run first (group 1)
- Assembly skills run last (group 99)

## User Preferences System

### Preference Schema

```yaml
# ~/.claude/skillchain-prefs.yaml
global:
  theme:
    color_scheme: string
    theme_modes: [light, dark, high-contrast]

  frameworks:
    frontend: react | svelte | vue | solid
    backend: fastapi | express | axum | hono
    database: postgres | mysql | sqlite

  ai_ml:
    llm_provider: openai | anthropic | ollama | vllm
    embedding_model: openai | sentence-transformers
    vector_db: qdrant | pgvector | pinecone

last_updated: timestamp
version: "3.0.0"
```

### Preference Priority

1. **User's explicit choice** (current workflow) - Highest
2. **Saved preferences** (from `~/.claude/skillchain-prefs.yaml`)
3. **Blueprint defaults** (if blueprint is active)
4. **Skill defaults** (from registry)

## Blueprint System

### 12 Available Blueprints

| Blueprint | Domain | Skills Included |
|-----------|--------|-----------------|
| dashboard | Frontend | theming, layouts, dashboards, viz, feedback |
| crud-api | Backend | api-patterns, relational-db, auth |
| api-first | Developer | designing-apis, documentation |
| rag-pipeline | AI/ML | ingesting-data, vector-db, ai-engineering |
| ml-pipeline | AI/ML | mlops, model-serving |
| ci-cd | DevOps | testing, ci-pipelines, gitops |
| k8s | Infrastructure | kubernetes, infrastructure-code |
| cloud | Cloud | aws/gcp/azure deployment |
| observability | DevOps | observability, logging |
| security | Security | architecture, compliance, hardening |
| cost | FinOps | cost optimization, tagging |
| data-pipeline | Data | architecting-data, transforming-data |

### Blueprint Detection

```python
for blueprint in blueprints:
  score = 0
  for keyword in blueprint.trigger_keywords:
    if keyword in goal:
      score += weight(keyword)

  if score >= confidence_threshold:
    offer_blueprint(blueprint)
    break
```

## Command Pattern

### Exposed Commands

| Command | Description |
|---------|-------------|
| `/skillchain:start [goal]` | Main guided workflow |
| `/skillchain:help` | Show help and 76 skills |
| `/skillchain:blueprints:dashboard` | Direct dashboard blueprint |
| `/skillchain:blueprints:k8s` | Direct Kubernetes blueprint |
| `/skillchain:categories:frontend` | Direct frontend orchestrator |
| `/skillchain:categories:devops` | Direct DevOps orchestrator |

### Data Files (NOT exposed)

- `skillchain-data/registries/*.yaml` - Skill definitions
- `skillchain-data/shared/*.md` - Internal resources

## File Structure

### Complete Directory Tree

```
~/.claude/
├── commands/skillchain/           # Commands (26 files)
│   ├── start.md                   # Router (entry point)
│   ├── help.md                    # Help content
│   │
│   ├── blueprints/                # 12 blueprints
│   │   ├── dashboard.md
│   │   ├── crud-api.md
│   │   ├── api-first.md
│   │   ├── rag-pipeline.md
│   │   ├── ml-pipeline.md
│   │   ├── ci-cd.md
│   │   ├── k8s.md
│   │   ├── cloud.md
│   │   ├── observability.md
│   │   ├── security.md
│   │   ├── cost.md
│   │   └── data-pipeline.md
│   │
│   └── categories/                # 12 orchestrators
│       ├── frontend.md
│       ├── backend.md
│       ├── devops.md
│       ├── infrastructure.md
│       ├── security.md
│       ├── developer.md
│       ├── data.md
│       ├── ai-ml.md
│       ├── cloud.md
│       ├── finops.md
│       ├── fullstack.md
│       └── multi-domain.md
│
└── skillchain-data/               # Data (NOT commands)
    ├── registries/                # 11 registry files
    │   ├── _index.yaml
    │   ├── frontend.yaml
    │   ├── backend.yaml
    │   ├── devops.yaml
    │   ├── infrastructure.yaml
    │   ├── security.yaml
    │   ├── developer.yaml
    │   ├── data.yaml
    │   ├── ai-ml.yaml
    │   ├── cloud.yaml
    │   └── finops.yaml
    │
    └── shared/                    # Shared resources
        ├── preferences.md
        ├── theming-rules.md
        └── execution-flow.md

Total: ~40 files
```

## Design Decisions

### Why Separated Directories?

**Problem:** Every `.md` file in `commands/` becomes a slash command. Internal files (`_registry.yaml`, `_shared/*.md`) were appearing as unwanted commands.

**Solution:** Move data files outside `commands/` to `skillchain-data/`.

**Benefits:**
- Clean command structure
- No unwanted `/skillchain:_shared:*` commands
- Clear separation of concerns
- Easier maintenance

### Why Domain Registries?

**Problem:** Single registry file became too large (700+ lines).

**Solution:** Split into 10 domain-specific registries.

**Benefits:**
- Smaller, focused files
- Domain teams can own their registry
- Faster loading (only load relevant domains)
- Better organization

### Why 10 Domains?

**Problem:** 2 categories (frontend/backend) didn't cover DevOps, infrastructure, security, etc.

**Solution:** Expand to 10 comprehensive domains.

**Benefits:**
- Full-stack coverage
- Specialized orchestrators
- Better keyword matching
- More accurate routing

## Extension Points

### Adding a New Blueprint

1. Create `blueprints/my-blueprint.md`
2. Blueprint auto-detected (no registry update needed)
3. Add trigger keywords in blueprint file
4. Test with `/skillchain:start [keywords]`

### Adding a New Domain

1. Create `skillchain-data/registries/my-domain.yaml`
2. Update `skillchain-data/registries/_index.yaml`
3. Create `categories/my-domain.md` orchestrator
4. Add domain keywords to `start.md`

### Adding a New Skill

1. Create skill package (SKILL.md, references/, etc.)
2. Add to appropriate domain registry
3. Test keyword matching
4. Update help.md if needed

## Performance

### Time Complexity

- **Domain detection:** O(k × d) where k = keywords, d = domains
- **Skill matching:** O(n) where n = skills in domain
- **Blueprint detection:** O(b × k) where b = blueprints

### Execution Time

- **Router:** < 1 second
- **Registry load:** < 1 second
- **Orchestrator load:** < 1 second
- **Skill invocation:** 2-5 seconds per skill
- **Total workflow:** 5-15 minutes (depends on questions)

## Next Steps

- [Install skillchain](./installation.md) to try it yourself
- [Learn usage patterns](./usage.md) for effective workflows
- [Explore blueprints](./blueprints.md) for fast-track presets
- [View skills overview](../skills/overview.md) to see what's orchestrated
