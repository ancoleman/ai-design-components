# Orchestrator Preference Guide

**For:** Category orchestrators (frontend.md, backend.md, fullstack.md, ai-ml.md)

This guide shows how to use the User Preferences System in orchestrators to provide smart defaults and faster workflows.

---

## Receiving Preferences

The router passes `user_prefs` to orchestrators in the context:

```yaml
Context received from router:
  original_goal: "dashboard with charts"
  matched_skills: [...]
  category: "frontend"
  estimated_questions: 12
  estimated_time: "8-12 minutes"
  user_prefs:            # ← This is what you'll use
    version: "1.0"
    global: {...}
    blueprints: {...}
    skills: {...}
```

**Check if preferences exist:**

```
if user_prefs is not null:
  has_preferences = true
  inform_user: "✓ Loaded preferences from previous workflows"
else:
  has_preferences = false
  # Use defaults only
```

---

## Using Global Preferences

Global preferences apply across all workflows and should be used as defaults when asking framework/technology questions.

### Example: Frontend Framework Selection

```markdown
## Determine Frontend Framework

if user_prefs.global.frameworks.frontend exists:
  saved_frontend = user_prefs.global.frameworks.frontend

  inform_user: "Using {saved_frontend} (from preferences)"

  ask_user: "Continue with {saved_frontend} or change?"
  options:
    - continue (use saved preference)
    - change (ask for new choice)

  if continue:
    frontend_framework = saved_frontend
  else:
    ask_user: "Which frontend framework?"
    options: [react, vue, svelte]
    frontend_framework = user_choice
else:
  # No saved preference, ask normally
  ask_user: "Which frontend framework?"
  options: [react, vue, svelte]
  frontend_framework = user_choice

# Store for saving later
collected_prefs.global.frameworks.frontend = frontend_framework
```

### Common Global Preferences

**Frontend workflows:**
```
user_prefs.global.frameworks.frontend → react | vue | svelte
user_prefs.global.theme.color_scheme → blue-gray | corporate-blue | etc.
user_prefs.global.theme.theme_modes → ["light", "dark"]
```

**Backend workflows:**
```
user_prefs.global.frameworks.backend → python | typescript | rust | go
user_prefs.global.frameworks.database → postgresql | mysql | sqlite
user_prefs.global.frameworks.orm → prisma | drizzle | sqlalchemy
user_prefs.global.deployment.target → docker | kubernetes | serverless
```

**AI/ML workflows:**
```
user_prefs.global.ai_ml.embedding_provider → openai | cohere | local
user_prefs.global.ai_ml.vector_db → qdrant | pgvector | pinecone
user_prefs.global.ai_ml.llm_provider → anthropic | openai | local
```

---

## Using Blueprint Preferences

If a blueprint was matched, check for saved blueprint configuration.

### Example: Dashboard Blueprint

```markdown
## Check for Saved Blueprint Configuration

blueprint_name = "dashboard"

if user_prefs.blueprints[blueprint_name] exists:
  saved_config = user_prefs.blueprints[blueprint_name].config
  last_used = user_prefs.blueprints[blueprint_name].last_used

  inform_user:
    "Found saved configuration for {blueprint_name} blueprint"
    "Last used: {last_used}"
    ""
    "Saved settings:"
    "  - Layout: {saved_config.layout}"
    "  - KPI cards: {saved_config.kpi_cards}"
    "  - Chart types: {saved_config.chart_types}"
    "  - Include table: {saved_config.include_table}"
    ""

  ask_user: "How would you like to proceed?"
  options:
    - use-saved: Use saved configuration (fastest)
    - customize: Start with saved but allow changes
    - fresh: Ignore saved config, start fresh

  if use-saved:
    config = saved_config
    inform_user: "✓ Using saved configuration"
    # Skip all blueprint questions!

  elif customize:
    config = saved_config
    # Ask questions but show saved values as defaults
    for each question:
      show saved_config.value as [default]
      allow user to accept or change

  else:  # fresh
    config = {}
    # Ask all questions normally
else:
  # No saved config, ask all questions
  config = {}
```

**Benefits:**
- "use-saved" → Skip all questions, instant workflow
- "customize" → Quick edits to known-good config
- "fresh" → Clean slate when needed

---

## Using Skill Preferences

For individual skills, check if user has saved preferences for that specific skill.

### Example: theming-components Skill

```markdown
## Invoke theming-components Skill

skill_name = "theming-components"

if user_prefs.skills[skill_name] exists:
  saved_skill_prefs = user_prefs.skills[skill_name]

  inform_user: "Found saved preferences for {skill_name}:"
  for key, value in saved_skill_prefs:
    inform_user: "  - {key}: {value}"

  ask_user: "Use saved preferences or customize?"
  options:
    - use-saved
    - customize
    - ignore

  if use-saved:
    # Pass saved preferences directly to skill
    invoke_skill(skill_name, config=saved_skill_prefs)

  elif customize:
    # Load skill and show saved values as defaults
    invoke_skill(skill_name, defaults=saved_skill_prefs)
    # User can modify any value

  else:  # ignore
    # Invoke skill normally, no defaults
    invoke_skill(skill_name)
else:
  # No saved preferences for this skill
  invoke_skill(skill_name)

# After skill completes, collect answers for saving
collected_prefs.skills[skill_name] = skill_answers
```

### Pattern: Show Saved Value as Default

When asking questions with saved preferences available:

```
❓ What color scheme would you like?

Options:
  1. blue-gray
  2. corporate-blue [from preferences] ← highlighted as default
  3. green-teal
  4. warm-orange
  5. custom

Your choice (1-5, or Enter for 2):
```

---

## Collecting Preferences for Saving

Throughout the workflow, collect user choices so they can be saved at the end.

### Data Structure

```yaml
collected_prefs:
  global:
    theme:
      color_scheme: "corporate-blue"
      theme_modes: ["light", "dark"]
    frameworks:
      frontend: "react"
      backend: "python"
      database: "postgresql"

  blueprints:
    dashboard:
      layout: "sidebar-grid"
      kpi_cards: 4
      chart_types: ["line", "bar"]

  skills:
    theming-components:
      color_scheme: "corporate-blue"
    building-forms:
      validation_library: "zod"
    visualizing-data:
      default_library: "recharts"
```

### What to Collect

**Always collect:**
- Framework choices (frontend, backend, database, etc.)
- Theme preferences (color scheme, modes)
- Technology selections (libraries, providers)

**Don't collect:**
- Project-specific values (project names, file paths)
- One-time choices (API keys, credentials)
- User content (component names, data)

**Rule of thumb:** Only collect choices that would be reused across different projects.

---

## Saving Preferences

At the end of the workflow, offer to save preferences.

### Pattern: Offer to Save

```markdown
## Workflow Complete - Offer to Save Preferences

inform_user:
  "✓ Workflow complete! Your {category} application is ready."
  ""
  "Would you like to save these preferences for next time?"
  ""
  "This will remember your:"
  - show list of what would be saved
  ""

ask_user: "Save preferences?"
options:
  - yes: Save all preferences
  - selective: Choose what to save
  - no: Don't save anything

if yes:
  save_all_preferences(collected_prefs)
  inform_user: "✓ Preferences saved to ~/.claude/skillchain-prefs.yaml"

elif selective:
  ask_user: "What would you like to save?"
  options:
    - [ ] Global framework preferences
    - [ ] Theme settings
    - [ ] Blueprint configuration
    - [ ] Individual skill preferences

  save_selected_preferences(user_selection)
  inform_user: "✓ Selected preferences saved"

else:
  inform_user: "Preferences not saved"
```

### Implementation: Save to File

```bash
# Read existing preferences (if any)
if [ -f "$HOME/.claude/skillchain-prefs.yaml" ]; then
  existing_prefs=$(cat "$HOME/.claude/skillchain-prefs.yaml")
else
  existing_prefs=""
fi

# Merge new preferences with existing
merged_prefs = merge_yaml(existing_prefs, collected_prefs)

# Update metadata
merged_prefs.version = "1.0"
merged_prefs.last_updated = current_date

# Write back to file
write_yaml("$HOME/.claude/skillchain-prefs.yaml", merged_prefs)

echo "✓ Preferences saved to ~/.claude/skillchain-prefs.yaml"
```

---

## Complete Orchestrator Flow with Preferences

### 1. Receive Context

```
received_context:
  - original_goal
  - matched_skills
  - category
  - user_prefs ← Check this
```

### 2. Check Preferences

```
if user_prefs exists:
  has_prefs = true
  inform_user: "✓ Using saved preferences as defaults"
else:
  has_prefs = false
```

### 3. Apply Global Preferences

```
# Framework selection
if user_prefs.global.frameworks.{category} exists:
  framework = user_prefs.global.frameworks.{category}
  ask_user: "Continue with {framework}? (yes/change)"
else:
  ask_user: "Which framework?"

collected_prefs.global.frameworks.{category} = framework
```

### 4. Apply Blueprint Preferences (if applicable)

```
if blueprint_matched and user_prefs.blueprints[blueprint] exists:
  ask_user: "Use saved blueprint config? (yes/customize/fresh)"

  if yes:
    config = user_prefs.blueprints[blueprint].config
    # Skip questions!
```

### 5. Invoke Skills with Preferences

```
for each skill in matched_skills:
  if user_prefs.skills[skill.name] exists:
    ask_user: "Use saved preferences for {skill.name}?"

    if yes:
      invoke_skill(skill.name, config=user_prefs.skills[skill.name])
    else:
      invoke_skill(skill.name)
  else:
    invoke_skill(skill.name)

  # Collect answers
  collected_prefs.skills[skill.name] = skill_answers
```

### 6. Complete Workflow

```
# Assembly, final output, etc.
```

### 7. Save Preferences

```
ask_user: "Save preferences for next time?"

if yes:
  save_preferences(collected_prefs)
  inform_user: "✓ Saved!"
```

---

## Validation

Before using saved preferences, validate them:

### Framework Validation

```
valid_frontends = ["react", "vue", "svelte"]
valid_backends = ["python", "typescript", "rust", "go"]

if user_prefs.global.frameworks.frontend not in valid_frontends:
  warn_user: "Saved frontend '{value}' is invalid, using default 'react'"
  framework = "react"
```

### Library Validation

```
# Check if saved library still exists/is recommended
if user_prefs.skills.visualizing-data.default_library == "victory":
  warn_user: "Victory is deprecated, would you like to use Recharts instead?"
  ask_user: "Use Recharts or keep Victory?"
```

---

## Benefits Summary

**For first-time users:**
- All questions asked normally
- Option to save preferences at end
- Future workflows will be faster

**For returning users:**
- Smart defaults from saved preferences
- Can accept all defaults for instant workflow
- Can customize any preference
- Can start fresh if needed

**Time savings:**
- First run: 8-12 minutes (answer all questions)
- Second run with saved prefs: 2-4 minutes (accept defaults)
- Third run with blueprint: 1-2 minutes (instant config)

---

## Example: Complete Frontend Workflow

```markdown
# Frontend Orchestrator

## Step 1: Receive Context

context = {
  original_goal: "dashboard with charts",
  matched_skills: [...],
  category: "frontend",
  user_prefs: { ... }  ← Has preferences!
}

## Step 2: Check Global Preferences

if user_prefs.global.frameworks.frontend == "react":
  inform_user: "Using React (from preferences)"
  ask_user: "Continue with React? (yes/change)"

  if yes:
    frontend = "react"
  else:
    frontend = ask_user("Which framework?")
else:
  frontend = ask_user("Which framework?")

collected_prefs.global.frameworks.frontend = frontend

## Step 3: Check Blueprint Preferences

blueprint = "dashboard"

if user_prefs.blueprints.dashboard exists:
  saved_config = user_prefs.blueprints.dashboard.config

  inform_user: "Found saved dashboard config from 2024-12-01"
  ask_user: "Use saved config? (yes/customize/fresh)"

  if yes:
    config = saved_config
    # Skip all blueprint questions!!!
    goto Step 4
  elif customize:
    config = saved_config  # Use as defaults
  else:
    config = {}

# Ask blueprint questions (if needed)
if config is empty:
  config.layout = ask_user("Layout?", default="sidebar-grid")
  config.kpi_cards = ask_user("KPI cards?", default=4)
  config.chart_types = ask_user("Chart types?")

collected_prefs.blueprints.dashboard = config

## Step 4: Invoke Skills

# Skill 1: theming-components
if user_prefs.skills.theming-components exists:
  ask_user: "Use saved theme preferences?"
  if yes:
    theme = invoke_skill("theming", user_prefs.skills.theming-components)
else:
  theme = invoke_skill("theming")

collected_prefs.skills.theming-components = theme

# Skill 2: visualizing-data
if user_prefs.skills.visualizing-data exists:
  viz = invoke_skill("visualizing", user_prefs.skills.visualizing-data)
else:
  viz = invoke_skill("visualizing")

collected_prefs.skills.visualizing-data = viz

# ... more skills ...

## Step 5: Assembly

assemble(theme, viz, ...)

## Step 6: Save Preferences

inform_user: "✓ Dashboard complete!"
ask_user: "Save preferences? (yes/no)"

if yes:
  save_preferences(collected_prefs)
  inform_user: "✓ Saved to ~/.claude/skillchain-prefs.yaml"
```

---

## Key Takeaways

1. **Always check** if preferences exist before asking questions
2. **Show saved values** as highlighted defaults
3. **Allow overrides** - user can always change preferences
4. **Collect answers** throughout workflow for saving
5. **Validate** preferences before using them
6. **Offer to save** at the end of successful workflows
7. **Merge carefully** when saving (don't overwrite unrelated preferences)

This creates a learning system that gets faster and smarter with each use!
