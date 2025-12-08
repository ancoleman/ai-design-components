# User Preferences System

## Overview

The preferences system allows users to save their preferred settings so they don't have to re-enter the same choices each time they run skillchain. Preferences are stored locally and can be updated at any time.

## Preferences File Location

`~/.claude/skillchain-prefs.yaml`

## Schema

```yaml
version: "1.0"
last_updated: "2024-12-02"

# Global preferences (applied across all workflows)
global:
  theme:
    color_scheme: "blue-gray"        # User's preferred color palette
    theme_modes: ["light", "dark"]   # Supported theme modes
    spacing_base: "8px"              # Base spacing unit

  frameworks:
    frontend: "react"                # react | vue | svelte
    backend: "python"                # python | typescript | rust | go
    orm: "prisma"                    # prisma | drizzle | sqlalchemy
    database: "postgresql"           # postgresql | mysql | sqlite | mongodb

  ai_ml:
    embedding_provider: "openai"     # openai | cohere | voyage | local
    vector_db: "qdrant"              # qdrant | pgvector | pinecone | chroma
    llm_provider: "anthropic"        # anthropic | openai | local

  deployment:
    target: "docker"                 # docker | kubernetes | serverless | vercel
    observability: true              # Include monitoring by default

  coding_style:
    language_preference: "typescript" # typescript | javascript | python
    code_comments: "moderate"        # minimal | moderate | extensive
    testing: "enabled"               # enabled | disabled

# Per-blueprint saved configurations
blueprints:
  dashboard:
    last_used: "2024-12-02"
    config:
      layout: "sidebar-grid"
      kpi_cards: 4
      chart_types: ["line", "bar"]
      include_table: true
      responsive: true

  crud-api:
    last_used: "2024-12-01"
    config:
      language: "python"
      framework: "fastapi"
      database: "postgresql"
      include_auth: true
      deploy_target: "docker"
      observability: true

  rag-pipeline:
    last_used: "2024-11-30"
    config:
      vector_db: "qdrant"
      embedding_provider: "openai"
      chunking_strategy: "recursive"
      include_chat_ui: true

# Per-skill saved preferences
skills:
  theming-components:
    color_scheme: "corporate-blue"
    theme_modes: ["light", "dark"]
    spacing_base: "8px"

  building-forms:
    validation_library: "zod"
    form_library: "react-hook-form"
    include_accessibility: true

  visualizing-data:
    default_library: "recharts"
    responsive: true
    accessibility: "wcag-aa"

  databases-relational:
    preferred_db: "postgresql"
    orm: "prisma"
    migration_tool: "prisma-migrate"

  databases-vector:
    provider: "qdrant"
    embedding_model: "openai-ada-002"

  api-patterns:
    api_style: "rest"
    framework: "fastapi"
    validation: "pydantic"

  auth-security:
    strategy: "jwt"
    provider: "managed"  # managed | self-hosted
    include_rbac: true

  deploying-applications:
    target: "docker"
    registry: "docker-hub"
    ci_cd: "github-actions"
```

## Loading Preferences

### When to Load

Preferences should be loaded at the start of the skillchain workflow (Step 0.5) before skill matching begins.

### How to Load

Add this to the router after Step 0 (Locate Directory):

```bash
# Step 0.5: Load User Preferences
if [ -f "$HOME/.claude/skillchain-prefs.yaml" ]; then
  PREFS_FILE="$HOME/.claude/skillchain-prefs.yaml"
  echo "✓ Loaded preferences from $PREFS_FILE"
else
  PREFS_FILE=""
  echo "ℹ No saved preferences found (will use defaults)"
fi
```

If preferences exist, read the file and store as `USER_PREFS` variable for use throughout the workflow.

### Preference Priority

When a setting can come from multiple sources:

1. **User's explicit choice** (during current workflow) - Highest priority
2. **Saved preferences** (from ~/.claude/skillchain-prefs.yaml) - Medium priority
3. **Default values** (from skill definitions) - Lowest priority

## Using Preferences in Orchestrators

### Pattern 1: Show Preference as Default

When asking questions, display saved preferences as suggested defaults:

```
Question: What color scheme would you like?
Options:
  - blue-gray
  - corporate-blue [from preferences] ← highlighted
  - green-teal
  - custom

User can:
  - Press Enter to accept "corporate-blue"
  - Select different option
  - Choose "custom" to specify new value
```

### Pattern 2: Check Before Asking

For critical preferences, check if saved value exists:

```
if USER_PREFS.global.frameworks.frontend exists:
  frontend_framework = USER_PREFS.global.frameworks.frontend
  inform_user: "Using React (from preferences)"
  ask_user: "Continue with React or change? (continue/change)"
else:
  ask_user: "Which frontend framework? (react/vue/svelte)"
```

### Pattern 3: Prefill Blueprint Configs

When loading a blueprint, check if user has saved config for it:

```
if USER_PREFS.blueprints.dashboard exists:
  config = USER_PREFS.blueprints.dashboard.config
  inform_user: "Found saved dashboard configuration from {last_used}"
  ask_user: "Use saved config or start fresh? (saved/fresh/customize)"
```

## Saving Preferences

### When to Save

After successful workflow completion, offer to save preferences:

```
✓ Workflow complete! Your application is ready.

Would you like to save these preferences for next time?
  - yes (save all choices)
  - selective (choose what to save)
  - no (don't save)
```

### What to Save

**Global preferences:**
- Theme settings (if theming-components was used)
- Framework choices (frontend, backend, database)
- AI/ML providers (if AI skills were used)
- Deployment targets (if deploying-applications was used)

**Blueprint preferences:**
- All configuration choices for the blueprint
- Timestamp of last use

**Skill preferences:**
- Individual skill configuration choices
- Only save skills that were actually used

### How to Save

1. **Read existing preferences** (if file exists)
2. **Merge new preferences** with existing ones
3. **Update last_updated timestamp**
4. **Write back to file**

```bash
# Pseudo-code for saving
if user_wants_to_save:
  existing_prefs = read_yaml("~/.claude/skillchain-prefs.yaml") or {}

  new_prefs = {
    "version": "1.0",
    "last_updated": current_date,
    "global": merge(existing_prefs.global, collected_global_prefs),
    "blueprints": merge(existing_prefs.blueprints, collected_blueprint_prefs),
    "skills": merge(existing_prefs.skills, collected_skill_prefs)
  }

  write_yaml("~/.claude/skillchain-prefs.yaml", new_prefs)
  echo "✓ Preferences saved to ~/.claude/skillchain-prefs.yaml"
```

## Orchestrator Implementation Guide

### For Category Orchestrators

Category orchestrators (frontend.md, backend.md, fullstack.md, ai-ml.md) should:

1. **Receive preferences** from router in context
2. **Apply preferences** when invoking skills
3. **Collect new preferences** during workflow
4. **Return preferences** to router for saving

### Example: Frontend Orchestrator

```markdown
## Step 1: Load Context

Received from router:
- original_goal
- matched_skills
- category
- USER_PREFS (if available)

## Step 2: Apply Global Preferences

If USER_PREFS.global.frameworks.frontend exists:
  default_frontend = USER_PREFS.global.frameworks.frontend
else:
  default_frontend = "react"

## Step 3: Invoke Skills with Preferences

For each skill in matched_skills:
  # Check for saved skill preferences
  if USER_PREFS.skills[skill.name] exists:
    skill_prefs = USER_PREFS.skills[skill.name]
    inform_user: "Using saved preferences for {skill.name}"
    ask_user: "Accept saved preferences or customize?"

    if accept_saved:
      use skill_prefs as defaults
    else:
      ask questions normally (ignore saved prefs)
  else:
    ask questions normally

## Step 4: Collect Preferences for Saving

Track all user choices during workflow:
- global_prefs_collected = {}
- skill_prefs_collected = {}

After workflow complete:
  return {
    global: global_prefs_collected,
    skills: skill_prefs_collected
  }
```

### Example: Blueprint Orchestrator

```markdown
## Step 1: Check for Saved Blueprint Config

if USER_PREFS.blueprints[blueprint_name] exists:
  saved_config = USER_PREFS.blueprints[blueprint_name].config
  last_used = USER_PREFS.blueprints[blueprint_name].last_used

  display:
    "Found saved configuration for {blueprint_name}"
    "Last used: {last_used}"
    "Settings:"
    - list all saved_config values

  ask_user: "Use saved config, customize it, or start fresh?"

  if use_saved:
    config = saved_config
  elif customize:
    config = saved_config (but allow modifications)
  else:
    config = ask_all_questions()
else:
  config = ask_all_questions()

## Step 2: Execute with Config

Run blueprint with chosen config...

## Step 3: Save Blueprint Config

After successful completion:
  if user_wants_to_save:
    save config to USER_PREFS.blueprints[blueprint_name]
```

## Preference Migration

If preference file format changes in future versions:

```yaml
version: "1.0"  # Current version

# Migration logic:
if existing_file.version < "1.0":
  migrate_preferences(existing_file)
  existing_file.version = "1.0"
```

## Preference Validation

Before using preferences, validate them:

1. **Schema validation** - Ensure all required fields exist
2. **Value validation** - Ensure values are valid options
3. **Compatibility check** - Ensure saved preferences are still compatible

```bash
# Example validation
if USER_PREFS.global.frameworks.frontend not in [react, vue, svelte]:
  warn_user: "Saved frontend preference '{value}' is invalid"
  use_default: "react"
```

## Privacy & Security

- Preferences file is stored locally on user's machine
- No preferences are sent to external services
- File contains only configuration choices, no sensitive data
- Users can delete file at any time: `rm ~/.claude/skillchain-prefs.yaml`

## Preference Management Commands

Users can manage preferences through skillchain:

```bash
/skillchain prefs show        # Display current preferences
/skillchain prefs edit        # Open preferences file in editor
/skillchain prefs reset       # Delete all preferences
/skillchain prefs export      # Export preferences to share
/skillchain prefs import      # Import preferences from file
```

## Example User Flow

### First Time User (No Preferences)

```
User: /skillchain dashboard with charts

System:
  ℹ No saved preferences found (will use defaults)

  [Ask all questions...]

  ✓ Dashboard created!

  Would you like to save these preferences? (yes/no/selective)

User: yes

System:
  ✓ Preferences saved to ~/.claude/skillchain-prefs.yaml
  Next time you'll see these as defaults!
```

### Returning User (Has Preferences)

```
User: /skillchain dashboard with charts

System:
  ✓ Loaded preferences from ~/.claude/skillchain-prefs.yaml

  🎯 Detected 'dashboard' blueprint!
  Found saved configuration from 2024-12-02:
    - Layout: sidebar-grid
    - KPI cards: 4
    - Chart types: line, bar
    - Include table: yes

  Use saved config? (yes/customize/fresh)

User: yes

System:
  ✓ Using saved configuration
  [Fewer questions, faster workflow...]
  ✓ Dashboard created!
```

## Benefits

1. **Faster workflows** - Skip repeated questions
2. **Consistency** - Same settings across projects
3. **Flexibility** - Can override preferences at any time
4. **Learning** - System learns user's preferences
5. **Sharing** - Export/import for team consistency

## Implementation Checklist

- [ ] Create ~/.claude/skillchain-prefs.yaml if not exists
- [ ] Add Step 0.5 to router (load preferences)
- [ ] Update orchestrators to use preferences
- [ ] Implement preference saving after workflow
- [ ] Add preference validation logic
- [ ] Create preference management commands
- [ ] Document preference schema
- [ ] Test preference loading/saving
- [ ] Test preference migration
- [ ] Add user documentation
