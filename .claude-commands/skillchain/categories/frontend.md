# Frontend Workflow Orchestrator

**Context Received:**
- Goal: {original_goal}
- Skills: {matched_skills}
- Category: frontend
- Estimated: {estimated_time}, {estimated_questions} questions

---

## Step 1: Load Shared Resources

Read the following shared resources and store them in context for all skills:

```
Read {SKILLCHAIN_DIR}/_shared/theming-rules.md
Read {SKILLCHAIN_DIR}/_shared/execution-flow.md
```

These resources contain:
- **theming-rules.md**: Token-first architecture requirements for ALL components
- **execution-flow.md**: Workflow management guidelines and command handling

---

## Step 2: Confirm Skill Chain with User

Present the detected skill chain in an ASCII box format:

```
TPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPW
Q  SKILL CHAIN DETECTED FOR: "{original_goal}"             Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  REQUIRED SKILLS (always included):                      Q
Q    1.  theming-components (foundation)                  Q
Q                                                          Q
Q  MATCHED FROM YOUR GOAL:                                 Q
{for each matched skill with score > 0:}
Q    {n}. � {skill.name} (matched: "{keyword}")            Q
Q                                                          Q
Q  ASSEMBLY (always included):                             Q
Q    99.  assembling-components (final step)              Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  Estimated time: {estimated_time}                        Q
Q  Estimated questions: {estimated_questions}              Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  OPTIONS:                                                Q
Q    " Type "confirm" to proceed                           Q
Q    " Type "skip" to use all defaults (faster)            Q
Q    " Type "customize" to add/remove skills               Q
Q    " Type "help" to see workflow commands                Q
ZPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP]
```

Wait for user response and handle accordingly:

- **"confirm"** � Proceed to Step 3 with interactive questions
- **"skip"** � Set `skip_all_questions = true`, proceed to Step 3 (uses all defaults)
- **"customize"** � Allow user to add/remove skills from the chain, then proceed
- **"help"** � Display workflow commands from execution-flow.md, then re-ask

---

## Step 3: Skill Invocation Loop

Initialize workflow state:

```
skill_configs = {}
current_skill_index = 1
total_skills = len(confirmed_skills)
skip_all_questions = false
```

For each skill in `confirmed_skills`, execute the following steps:

### 3.1 Announce Skill

Display a clear separator showing current progress:

```
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
 STEP {current_skill_index}/{total_skills}: {SKILL.NAME}
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
```

### 3.2 Invoke Skill

**CRITICAL: You MUST use the Skill tool to invoke each skill.** Do not skip this step. Do not just describe what skills to use - actually invoke them.

**THIS IS A REQUIRED ACTION, NOT DOCUMENTATION.**

Invoke the skill using the Skill tool with the exact invocation string from registry:

```
Use the Skill tool with: skill: "ui-foundation-skills:theming-components"
```

The skill will load and provide you with instructions. Follow those instructions, then proceed to the next skill.

**Invocation strings for frontend skills:**

| Order | Skill | Tool Invocation | When |
|-------|-------|-----------------|------|
| 1 | theming-components | `Skill: ui-foundation-skills:theming-components` | ALWAYS FIRST |
| 2 | designing-layouts | `Skill: ui-structure-skills:designing-layouts` | If layout needed |
| 3 | implementing-navigation | `Skill: ui-structure-skills:implementing-navigation` | If navigation needed |
| 4 | visualizing-data | `Skill: ui-data-skills:visualizing-data` | If charts needed |
| 5 | building-tables | `Skill: ui-data-skills:building-tables` | If tables needed |
| 6 | creating-dashboards | `Skill: ui-data-skills:creating-dashboards` | If dashboard needed |
| 7 | building-forms | `Skill: ui-input-skills:building-forms` | If forms needed |
| 8 | implementing-search-filter | `Skill: ui-input-skills:implementing-search-filter` | If search needed |
| 9 | building-ai-chat | `Skill: ui-interaction-skills:building-ai-chat` | If chat needed |
| 10 | implementing-drag-drop | `Skill: ui-interaction-skills:implementing-drag-drop` | If drag-drop needed |
| 11 | providing-feedback | `Skill: ui-interaction-skills:providing-feedback` | If feedback needed |
| 12 | displaying-timelines | `Skill: ui-structure-skills:displaying-timelines` | If timeline needed |
| 13 | managing-media | `Skill: ui-content-skills:managing-media` | If media needed |
| 14 | guiding-users | `Skill: ui-content-skills:guiding-users` | If onboarding needed |
| 99 | assembling-components | `Skill: ui-assembly-skills:assembling-components` | ALWAYS LAST |

### Execution Loop

```
FOR EACH skill in matched_skills (sorted by priority):
  1. ANNOUNCE: "Now invoking skill: {skill_name}"
  2. INVOKE: Use the Skill tool with the skill name
  3. FOLLOW: Complete the skill's instructions
  4. TRACK: Record what files were created
  5. PROCEED: Move to the next skill
END FOR
```

### Output Tracking

After each skill completes, track what it created:
- Note files mentioned in the skill output (lines starting with "Created:", "Generated:", "✓")
- Update chain_context.skill_outputs with files_created
- Match files against blueprint deliverables

### 3.3 Load Questions

Retrieve questions based on the skill's configuration source:

**If skill.questions.source == "inline":**
- Use default questions from registry (_registry.yaml)
- These are simple skills with < 5 questions

**If skill.questions.source == "skill":**
- The skill's SKILL.md will be loaded when the Skill tool is invoked
- Extract the section specified in `skill.questions.section` (typically "## Skillchain Configuration")
- Parse questions from markdown format

**Questions for inline-source skills:**

- **theming-components**: color_scheme, theme_modes, spacing_base
- **creating-dashboards**: layout, kpi_cards, responsive
- **implementing-search-filter**: realtime, position, scope
- **implementing-drag-drop**: library, touch_support
- **providing-feedback**: toast_position, loading_type
- **implementing-navigation**: type, collapsible
- **designing-layouts**: system, responsive, breakpoints
- **displaying-timelines**: orientation, timestamps
- **guiding-users**: type, dismissible
- **assembling-components**: validate_tokens, production_ready

### 3.4 Ask User (unless skip_all_questions)

If `skip_all_questions == true`:
- Use default answers for all questions
- Skip directly to Step 3.5

Otherwise, for each question in the skill:

1. **Present question with context:**
   - Reference user's original goal
   - Show answers from previous skills (if relevant)
   - Highlight smart defaults based on detected keywords
   - Show current answer if user typed "back" (revisiting)

2. **Example question format:**
   ```
   Question 2/5: What chart types do you need?

   Context: You mentioned "analytics dashboard" in your goal
   Default: [bar, line, pie] (common for dashboards)

   Enter chart types (comma-separated), or type:
   - "skip" to use default
   - "back" to return to previous skill
   - "status" to show progress
   - "done" to finish early
   - "restart" to start over
   - "help" for workflow commands

   Your answer:
   ```

3. **Handle user input:**

   - **Answer provided** � Store answer, continue to next question
   - **"skip"** � Use default for this question, continue
   - **"back"** � Decrement `current_skill_index`, return to previous skill (preserve answers)
   - **"status"** � Display progress indicator (see execution-flow.md �3.2), re-ask current question
   - **"done"** � Break loop immediately, proceed to Step 4 (Final Assembly)
   - **"restart"** � Clear all `skill_configs`, return to Step 2
   - **"help"** � Display workflow commands, re-ask current question

4. **Status display format:**
   ```
   PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
   PROGRESS: Step {current_skill_index}/{total_skills}
   PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
    theming-components (complete)
    visualizing-data (complete)
   � building-tables (current: question 2/5)
     creating-dashboards (pending)
     providing-feedback (pending)
     assembling-components (pending)
   PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
   ```

### 3.5 Store Configuration

After all questions for a skill are answered (or skipped):

```
skill_configs[skill.name] = {
  skill_name: skill.name,
  invocation: skill.invocation,
  answers: user_answers,
  priority: skill.priority,
  dependencies: skill.dependencies
}

current_skill_index += 1
```

Continue to next skill in `confirmed_skills`.

---

## Step 4: Final Assembly

Once all skills have been invoked and configured, invoke the assembling-components skill with all collected context:

```
Invoke Skill({ skill: "ui-assembly-skills:assembling-components" })

Provide to assembling-components:
- skill_configs: Complete map of all skill configurations
- original_goal: User's original goal text
- theming_rules: Content from theming-rules.md
- execution_flow: Workflow guidelines from execution-flow.md
```

The assembling-components skill will:
1. Validate token integration (no hardcoded colors/spacing)
2. Generate complete, production-ready code
3. Wire all components together
4. Create proper import chains
5. Provide tokens.css as the first file
6. Ensure theme toggle functionality
7. Include accessibility features

---

## Step 5.5: Validate Chain Outputs

After all skills have executed and final assembly is complete, validate the combined output:

### Load Validation Logic

```
Read {SKILLCHAIN_DATA}/shared/validation.md
```

### Per-Skill Output Validation

For each skill that was invoked:
```
skill_outputs = Read {SKILLS_DIR}/{skill_name}/outputs.yaml
For each output in skill_outputs.base_outputs:
  If NOT exists {project_path}/{output.path}:
    Mark as missing, log for user
  Else if output.must_contain exists:
    Check file contains expected patterns
```

### Run Chain Validation

```
If chain_context.blueprint exists:
  # Option 1: Use completeness checker script
  Run: python scripts/runtime/completeness_checker.py {project_path} --blueprint {blueprint} --maturity {maturity}

  # Option 2: Manual validation (if script not available)
  # Load blueprint deliverables
  Read {SKILLCHAIN_CMD}/blueprints/{chain_context.blueprint}.md
  Parse "## Deliverables Specification" section

  # Apply maturity adjustments
  For each deliverable in deliverables:
    If deliverable.maturity_required exists:
      If chain_context.maturity NOT in deliverable.maturity_required:
        Mark deliverable as "skipped"

  # Validate each required deliverable
  For each deliverable NOT skipped:
    result = validate_deliverable(deliverable, chain_context.project_path)
    chain_context.deliverables_status[deliverable.name] = result

  # Calculate completeness
  required_count = count(deliverables where status != "skipped")
  fulfilled_count = count(deliverables where status == "fulfilled")
  completeness = fulfilled_count / required_count

Else:
  # No blueprint - run basic completeness check
  Run run_basic_completeness_check(chain_context.project_path)
```

### Generate Validation Report

```
┌────────────────────────────────────────┐
│ FRONTEND SKILLCHAIN VALIDATION         │
├────────────────────────────────────────┤
│ Blueprint: {chain_context.blueprint}   │
│ Maturity: {chain_context.maturity}     │
├────────────────────────────────────────┤
For each deliverable in chain_context.deliverables_status:
  If status == "fulfilled": │ ✓ {name}
  If status == "missing":   │ ✗ {name} - MISSING
  If status == "skipped":   │ ○ {name} (skipped - {maturity})
├────────────────────────────────────────┤
│ Required: {required_count}             │
│ Fulfilled: {fulfilled_count}           │
│ Completeness: {completeness}%          │
└────────────────────────────────────────┘
```

### Handle Missing Deliverables

```
If completeness < 80%:
  "⚠️ Some frontend components weren't fully generated:

   Missing:
   [list deliverables where status == "missing"]

   Would you like me to:
   A) Generate the missing components
   B) Continue without them
   C) See detailed validation report"

  If user chooses A:
    For each missing deliverable:
      Invoke primary_skill for that deliverable
    Re-run validation (go back to "Run Chain Validation")
```

---

## Error Handling

### Skill Invocation Failure

If a skill fails to invoke or load:

```
�  ERROR: Skill '{skill_name}' failed to load

Reason: {error_message}

Options:
1. Continue with remaining skills (skip this one)
2. Retry this skill
3. Stop workflow and show partial progress

Your choice (1/2/3):
```

Handle user response:
- **1** � Mark skill as skipped, continue to next skill, proceed to assembly
- **2** � Retry invoking the skill up to 2 additional times
- **3** � Stop workflow, display completed skills and partial configuration

### Dependency Failures

If a skill's dependency was skipped or failed:

```
�  WARNING: This skill depends on '{dependency_name}' which was skipped.

We'll use default values for {dependency_name}. Continue? (yes/no)
```

- **yes** � Proceed with default configuration
- **no** � Skip this skill as well

### Assembly Validation Failures

If final assembly detects token violations:

```
�  Assembly validation failed:

Issues found:
- Missing tokens.css import in main.tsx
- Hardcoded color value (#3B82F6) in Button.css line 23
- Hardcoded spacing (16px) in Card.css line 45

Auto-fix these issues? (yes/no)
```

- **yes** � Apply automatic fixes, regenerate affected files
- **no** � Provide code as-is with warning annotations

---

## Frontend Skill Ordering

Follow these ordering principles when invoking frontend skills:

1. **Foundation First** (priority 1-3):
   - theming-components (always first)
   - designing-layouts
   - implementing-navigation

2. **Data Display** (priority 5):
   - visualizing-data
   - building-tables
   - creating-dashboards

3. **User Input** (priority 6):
   - building-forms
   - implementing-search-filter

4. **Interaction** (priority 7-8):
   - building-ai-chat
   - implementing-drag-drop
   - providing-feedback
   - displaying-timelines
   - managing-media
   - guiding-users

5. **Assembly Last** (priority 99):
   - assembling-components (always last)

---

## Parallel Skill Invocation

When multiple skills are in the same `parallel_group`, invoke them together to speed up the workflow:

### Parallel Groups (from _registry.yaml)

- **Group 1 (Foundation)**: theming-components - MUST be first, sequential
- **Group 2 (Structure)**: designing-layouts, implementing-navigation - Can parallelize
- **Group 3 (Data Display)**: visualizing-data, building-tables, creating-dashboards - Can parallelize (dashboard needs layouts first)
- **Group 4 (User Input)**: building-forms, implementing-search-filter - Can parallelize
- **Group 5 (Interaction)**: building-ai-chat, implementing-drag-drop, providing-feedback - Can parallelize (ai-chat needs forms first)
- **Group 6 (Content)**: displaying-timelines, managing-media, guiding-users - Can parallelize
- **Group 99 (Assembly)**: assembling-components - MUST be last, sequential

### Example Parallel Invocations

**Dashboard with charts + tables:**
```
Step 1: Skill({ skill: "ui-foundation-skills:theming-components" })
Step 2: Skill({ skill: "ui-structure-skills:designing-layouts" })
Step 3 (PARALLEL):
  Skill({ skill: "ui-data-skills:visualizing-data" })
  Skill({ skill: "ui-data-skills:building-tables" })
Step 4: Skill({ skill: "ui-data-skills:creating-dashboards" })
Step 5: Skill({ skill: "ui-assembly-skills:assembling-components" })
```

**Form with search functionality:**
```
Step 1: Skill({ skill: "ui-foundation-skills:theming-components" })
Step 2 (PARALLEL):
  Skill({ skill: "ui-input-skills:building-forms" })
  Skill({ skill: "ui-input-skills:implementing-search-filter" })
Step 3: Skill({ skill: "ui-assembly-skills:assembling-components" })
```

### Implementation Notes

- Always check dependencies before parallelizing (from _registry.yaml `dependencies` field)
- Respect the dependency graph in `{SKILLCHAIN_DIR}/_shared/parallel-loading.md`
- Group 1 and Group 99 are ALWAYS sequential (foundation and assembly)
- Parallel skills share configuration context, reducing redundant questions

---

## Special Frontend Considerations

### Required Skills
These skills are ALWAYS included for frontend workflows:
- `theming-components` (foundation)
- `assembling-components` (final step)

Never allow skipping these entirely, but individual questions can be skipped (defaults used).

### Smart Defaults Based on Goal Keywords

When user's goal contains specific keywords, suggest these defaults:

| Keyword | Auto-include Skill | Default Config |
|---------|-------------------|----------------|
| dashboard, admin, analytics | creating-dashboards | layout=sidebar-grid |
| chart, graph, visualize | visualizing-data | types=bar,line,pie |
| form, login, signup | building-forms | validation=yup |
| table, grid, list | building-tables | pagination=true |
| chat, ai, assistant | building-ai-chat | streaming=true |
| drag, sortable, kanban | implementing-drag-drop | library=dnd-kit |
| search, filter | implementing-search-filter | realtime=true |
| upload, file, media | managing-media | multi=true |

### Conflict Detection

Before final assembly, check for configuration conflicts:

**Example conflict:**
```
�  CONFLICT DETECTED

visualizing-data specified: library="d3"
creating-dashboards specified: library="recharts"

Which should we use for consistency?
1. D3 (more flexible, higher complexity)
2. Recharts (simpler, better for dashboards)
3. Use both (components will differ)

Your choice (1/2/3):
```

---

**Orchestrator Complete**
