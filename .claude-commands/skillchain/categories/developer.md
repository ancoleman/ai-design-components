# Developer Productivity Workflow Orchestrator

**Context Received:**
- Goal: {original_goal}
- Skills: {matched_skills}
- Category: developer-productivity
- Estimated: {estimated_time}, {estimated_questions} questions

---

## Step 1: Load Shared Resources

Read `{SKILLCHAIN_DIR}/_shared/execution-flow.md`

Store in context for all skills.

**Note:** Developer workflows do not require theming-rules.md (frontend-only).

---

## Step 2: Confirm Skill Chain with User

Present detected chain:

```
TPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPW
Q  SKILL CHAIN DETECTED FOR: "{original_goal}"             Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  MATCHED DEVELOPER PRODUCTIVITY SKILLS:                  Q
{for each matched skill with score > 0:}
Q    {n}. ⚙ {skill.name} (matched: "{keyword}")            Q
Q          Plugin: {skill.plugin_namespace}               Q
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

Wait for user response:
- "confirm" → Proceed to Step 3
- "skip" → Set skip_all_questions = true, proceed to Step 3
- "customize" → Allow skill additions/removals, then proceed
- "help" → Show workflow commands from execution-flow.md

---

## Step 3: Skill Invocation Loop

**CRITICAL: You MUST use the Skill tool to invoke each skill. This is a REQUIRED ACTION, not documentation.**

### 3.0 Developer Productivity Skills Reference

| Order | Skill | Tool Invocation | When |
|-------|-------|----------------|------|
| 1st | API Design | `Skill({ skill: "developer-productivity-skills:designing-apis" })` | Building APIs or SDKs |
| 2nd | SDK Design | `Skill({ skill: "developer-productivity-skills:designing-sdks" })` | Creating client libraries (depends on API) |
| 3rd | CLI Building | `Skill({ skill: "developer-productivity-skills:building-clis" })` | Command-line tools |
| 4th | GitHub Actions | `Skill({ skill: "developer-productivity-skills:writing-github-actions" })` | CI/CD automation |
| 5th | Git Workflows | `Skill({ skill: "developer-productivity-skills:managing-git-workflows" })` | Team collaboration processes |
| 6th | Debugging | `Skill({ skill: "developer-productivity-skills:debugging-techniques" })` | Development tooling |
| 7th | Documentation | `Skill({ skill: "developer-productivity-skills:generating-documentation" })` | Reference docs (run last) |

**THIS IS A REQUIRED ACTION, NOT DOCUMENTATION.** You must invoke each matched skill using the Skill tool.

### Execution Loop Pattern

Initialize:
```
skill_configs = {}
current_skill_index = 1
total_skills = len(confirmed_skills)
```

For each skill in confirmed_skills:

### 3.1 ANNOUNCE → Skill Starting

```
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
 STEP {current_skill_index}/{total_skills}: {SKILL.NAME}
 Plugin: {skill.plugin_namespace}:{skill.name}
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
```

### 3.2 INVOKE → Execute Skill Tool

**CRITICAL: YOU MUST NOW USE THE SKILL TOOL:**

```
Skill({ skill: "{skill.invocation}" })
```

Example invocations:
```
Skill({ skill: "developer-productivity-skills:designing-apis" })
Skill({ skill: "developer-productivity-skills:building-clis" })
Skill({ skill: "developer-productivity-skills:designing-sdks" })
```

**Wait for skill to load before proceeding.**

### 3.3 FOLLOW → Execute Skill Instructions

**After invoking the skill, you will receive expanded instructions from the skill's SKILL.md file.**

Follow all instructions provided by the loaded skill. The skill will guide you through:
- Configuration questions to ask the user
- Decisions to make based on the goal
- Files to generate or modify
- Integration points with other skills

All developer skills use `questions.source: "skill"` format - questions come from the skill's SKILL.md.

### 3.4 TRACK → Store Configuration

After completing the skill's instructions, store the configuration:

```
skill_configs[skill.name] = {
  answers: user_answers,
  invocation: skill.invocation,
  priority: skill.priority,
  plugin: skill.plugin_namespace,
  dependencies: skill.dependencies,
  outputs: files_generated
}
```

### 3.5 PROCEED → Next Skill

```
current_skill_index += 1
```

If more skills remain, return to Step 3.1 (ANNOUNCE).

---

### Workflow Commands During Skill Execution

While executing any skill, user can respond with:
- Answer → Store and continue with skill
- "skip" → Use default for current question
- "back" → Return to previous skill
- "status" → Show progress, continue current skill
- "done" → Break loop, proceed to Step 4
- "restart" → Go back to Step 2

---

## Step 4: Generate Developer Output

**IMPORTANT:** Developer workflows DO NOT use `assembling-components` skill (frontend-only).

Instead, generate developer artifacts directly:

### 4.1 Analyze Collected Configurations

Review all `skill_configs` to identify:
- API design patterns and specifications (OpenAPI, GraphQL schemas)
- CLI framework and command structure
- SDK architecture and client library patterns
- Documentation generation tools and formats
- Debugging strategies and tooling setup
- Git workflow and branching strategies
- GitHub Actions workflows and automation

### 4.2 Identify Integration Points

Detect where skills need to interact:
- SDK wraps API specifications (designing-sdks depends on designing-apis)
- Documentation references API specs and SDK usage
- GitHub Actions workflows include testing, deployment
- Git workflows integrated with CI/CD pipelines
- Debug configurations for CLI and API development

### 4.3 Generate Production-Ready Artifacts

Create complete developer tooling implementation:

```
TPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPW
Q  GENERATING DEVELOPER ARTIFACTS FOR: "{original_goal}"   Q
`PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPc
Q  Based on configurations:                                Q
{for each skill in skill_configs:}
Q    ⚙ {skill.name}: {summary of choices}                  Q
ZPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP]

Generating:
  1. API specifications and documentation
  2. CLI implementation and command structure
  3. SDK client libraries and usage examples
  4. Documentation site and reference guides
  5. Debug configurations and tooling
  6. Git workflow documentation and templates
  7. GitHub Actions workflows and CI/CD pipelines
```

### 4.4 Output Organization

Organize artifacts by developer tooling pattern:

**For API Projects:**
```
project/
  api/
    openapi.yaml      # API specification
    docs/             # API documentation
  sdk/
    src/              # Client library code
    examples/         # Usage examples
  docs/
    api-reference/    # Generated API docs
    guides/           # User guides
  .github/
    workflows/        # CI/CD automation
  scripts/
    debug/            # Debug utilities
```

**For CLI Tools:**
```
cli-tool/
  src/
    commands/         # CLI command implementations
    utils/            # Shared utilities
  docs/
    commands/         # Command reference
    guides/           # User guides
  .github/
    workflows/        # Release automation
  scripts/
    debug/            # Debug configurations
```

**For SDK Libraries:**
```
sdk/
  src/
    client/           # API client code
    models/           # Data models
    types/            # Type definitions
  examples/           # Code examples
  docs/
    api-reference/    # Generated docs
    guides/           # Usage guides
  tests/
  .github/
    workflows/        # Testing and publishing
```

### 4.5 Validation Checklist

Verify generated artifacts include:
- [ ] API specifications are valid (OpenAPI/GraphQL)
- [ ] CLI commands have proper help text and validation
- [ ] SDK has comprehensive error handling
- [ ] Documentation is complete and accurate
- [ ] Debug configurations work for target IDEs
- [ ] Git workflow documentation is clear
- [ ] GitHub Actions workflows are tested
- [ ] README with setup and usage instructions
- [ ] Contributing guidelines if applicable
- [ ] License file included

### 4.6 Present Output

Display generated files with explanations:

```
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
  DEVELOPER ARTIFACTS COMPLETE
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP

Generated {file_count} files across {skill_count} developer skills:

KEY FILES:
  ⚙ {api_spec_file}             - API specification
  ⚙ {cli_main_file}             - CLI entry point
  ⚙ {sdk_client_file}           - SDK client library
  ⚙ {docs_index_file}           - Documentation home
  ⚙ {workflow_file}             - CI/CD automation

NEXT STEPS:
  1. Review generated specifications
  2. Test CLI commands: {cli_test_command}
  3. Build SDK: {sdk_build_command}
  4. Generate docs: {docs_command}
  5. Push to GitHub to trigger workflows

PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
```

---

## Step 5.5: Validate Chain Outputs

After all skills have executed, validate the combined output:

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
│ DEVELOPER SKILLCHAIN VALIDATION        │
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
  "⚠️ Some developer components weren't fully generated:

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

### Developer-Specific Validation Notes

When validating developer tooling outputs, check for:

**CLI Tools:**
- Command entry points exist and are executable
- Help text is present for all commands
- Configuration files have valid schemas

**SDKs:**
- Client library has proper exports
- Type definitions exist (TypeScript) or type hints (Python)
- Examples directory contains working code

**Documentation:**
- API reference is generated and non-empty
- Getting started guide exists
- Code examples are syntactically valid

**Git Workflows:**
- `.github/workflows/` contains valid YAML
- Branch protection rules documented
- Commit message conventions specified

**Debug Configurations:**
- IDE config files exist (`.vscode/launch.json`, etc.)
- Environment variable templates present
- Debug scripts have proper error handling

---

## Error Handling

### Skill Invocation Failure

If skill invocation fails:

```
⚠ ERROR: Skill '{skill.name}' failed to load

Plugin: {skill.invocation}
Reason: {error_message}

Options:
1. Continue with remaining skills (skip this one)
2. Retry this skill
3. Stop workflow and show partial progress

Your choice (1/2/3):
```

Handle user choice:
- 1 → Mark skill as skipped, continue to next skill
- 2 → Re-invoke skill, reset current_skill_index
- 3 → Stop loop, proceed to Step 4 with partial configs

### Dependency Failures

When a dependent skill was skipped/failed:

```
⚠ WARNING: '{skill.name}' depends on '{dependency}' which was skipped.

We'll use default configuration for {dependency} integration.
Continue? (yes/no)
```

If "no" → Allow user to go back and configure dependency

### Invalid Configuration Combinations

Detect incompatible choices:

```
⚠ CONFIGURATION CONFLICT DETECTED

designing-apis specified: REST API with OpenAPI
designing-sdks specified: GraphQL client

SDKs should match the API type. Options:
1. Generate REST SDK (matches API spec)
2. Keep GraphQL SDK (requires additional API endpoint)
3. Go back and reconfigure

Your choice (1/2/3):
```

### Missing Required Information

If critical configuration is missing:

```
⚠ ERROR: Cannot generate SDK without API specification

designing-sdks depends on designing-apis.

Options:
1. Add designing-apis skill (recommended)
2. Continue with manual API specification
3. Restart workflow

Your choice (1/2/3):
```

---

## Developer Skill Ordering

Follow these ordering principles:

1. **API Design First** (priority 10-12):
   - designing-apis (if API/SDK needed)
   - designing-sdks (depends on designing-apis)

2. **CLI Development** (priority 8):
   - building-clis (independent)

3. **Automation & Workflows** (priority 9):
   - writing-github-actions (can reference other artifacts)

4. **Debugging & Git** (priority 6-7):
   - managing-git-workflows (team processes)
   - debugging-techniques (development support)

5. **Documentation Last** (priority 5):
   - generating-documentation (references all other artifacts)

---

**Orchestrator Complete**
