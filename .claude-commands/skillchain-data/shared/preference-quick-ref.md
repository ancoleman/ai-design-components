# Preferences Quick Reference

**For orchestrators:** Quick patterns for using preferences in your workflow.

---

## 1. Check if Preferences Exist

```
if user_prefs exists:
  inform_user: "✓ Using saved preferences as defaults"
else:
  # Use defaults only
```

---

## 2. Use Global Framework Preference

```
if user_prefs.global.frameworks.{category} exists:
  framework = user_prefs.global.frameworks.{category}
  ask_user: "Continue with {framework}? (yes/change)"
else:
  framework = ask_user("Which {category} framework?")

collected_prefs.global.frameworks.{category} = framework
```

---

## 3. Use Blueprint Preference

```
if user_prefs.blueprints.{blueprint_name} exists:
  saved_config = user_prefs.blueprints.{blueprint_name}.config

  ask_user: "Use saved config? (yes/customize/fresh)"

  if yes:
    config = saved_config  # Skip all questions!
  elif customize:
    config = saved_config  # Use as defaults, allow edits
  else:
    config = {}  # Start fresh
```

---

## 4. Use Skill Preference

```
if user_prefs.skills.{skill_name} exists:
  ask_user: "Use saved {skill_name} preferences? (yes/no)"

  if yes:
    result = invoke_skill({skill_name}, user_prefs.skills.{skill_name})
  else:
    result = invoke_skill({skill_name})
else:
  result = invoke_skill({skill_name})

collected_prefs.skills.{skill_name} = result.answers
```

---

## 5. Save Preferences at End

```
ask_user: "Save preferences for next time? (yes/selective/no)"

if yes:
  save_all(collected_prefs)
elif selective:
  save_selected(user_chooses_what)
else:
  # Don't save
```

---

## Common Preference Paths

### Global Preferences

```yaml
user_prefs.global.frameworks.frontend       # react | vue | svelte
user_prefs.global.frameworks.backend        # python | typescript | rust
user_prefs.global.frameworks.database       # postgresql | mysql | sqlite
user_prefs.global.frameworks.orm            # prisma | drizzle | sqlalchemy

user_prefs.global.theme.color_scheme        # blue-gray | corporate-blue | ...
user_prefs.global.theme.theme_modes         # ["light", "dark"]
user_prefs.global.theme.spacing_base        # "8px" | "4px" | "16px"

user_prefs.global.ai_ml.embedding_provider  # openai | cohere | local
user_prefs.global.ai_ml.vector_db           # qdrant | pgvector | pinecone
user_prefs.global.ai_ml.llm_provider        # anthropic | openai | local

user_prefs.global.deployment.target         # docker | kubernetes | serverless
user_prefs.global.deployment.observability  # true | false
```

### Blueprint Preferences

```yaml
user_prefs.blueprints.dashboard.config      # Full dashboard config
user_prefs.blueprints.dashboard.last_used   # "2024-12-02"

user_prefs.blueprints.crud-api.config       # Full API config
user_prefs.blueprints.crud-api.last_used    # "2024-12-01"

user_prefs.blueprints.rag-pipeline.config   # Full RAG config
user_prefs.blueprints.rag-pipeline.last_used # "2024-11-30"
```

### Skill Preferences

```yaml
user_prefs.skills.theming-components        # Theme config
user_prefs.skills.building-forms            # Form config
user_prefs.skills.visualizing-data          # Viz config
user_prefs.skills.databases-relational      # DB config
# ... etc for any skill
```

---

## Collected Preferences Structure

Throughout workflow, collect choices in this structure:

```yaml
collected_prefs:
  global:
    theme:
      color_scheme: "value"
      theme_modes: ["light", "dark"]
    frameworks:
      frontend: "react"
      backend: "python"
      database: "postgresql"
    ai_ml:
      vector_db: "qdrant"
      embedding_provider: "openai"

  blueprints:
    dashboard:  # Only if blueprint was used
      layout: "sidebar-grid"
      kpi_cards: 4

  skills:
    theming-components:  # For each skill used
      color_scheme: "corporate-blue"
    building-forms:
      validation_library: "zod"
    # ... etc
```

---

## Validation

Before using saved preferences:

```
valid_options = ["option1", "option2", "option3"]

if saved_value not in valid_options:
  warn_user: "Saved value '{saved_value}' is invalid"
  use_default_instead
```

---

## Full Reference

See `/Users/antoncoleman/Documents/repos/ai-design-components/commands/skillchain/_shared/orchestrator-preference-guide.md` for complete guide with examples.
