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

Initialize:
```
skill_configs = {}
current_skill_index = 1
total_skills = len(confirmed_skills)
```

For each skill in confirmed_skills:

### 3.1 Announce Skill

```
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
 STEP {current_skill_index}/{total_skills}: {SKILL.NAME}
 Plugin: {skill.plugin_namespace}:{skill.name}
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
```

### 3.2 Invoke Skill

```
Skill({ skill: "{skill.invocation}" })
```

**Developer skill invocation strings:**
- `developer-productivity-skills:designing-apis`
- `developer-productivity-skills:building-clis`
- `developer-productivity-skills:designing-sdks`
- `developer-productivity-skills:generating-documentation`
- `developer-productivity-skills:debugging-techniques`
- `developer-productivity-skills:managing-git-workflows`
- `developer-productivity-skills:writing-github-actions`

### 3.3 Load Questions

All developer skills use `questions.source: "skill"` format.

```python
# Read from SKILL.md in the plugin
skill_md_path = f"/mnt/skills/public/{skill.invocation.replace(':', '/')}/SKILL.md"
skill_md = Read(skill_md_path)

# Extract section specified in registry
section_name = skill.questions.section  # "## Skillchain Configuration"
section_content = extract_section(skill_md, section_name)

# Parse questions from markdown
questions = parse_questions(section_content)
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
      - Dependency information if applicable

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
  priority: skill.priority,
  plugin: skill.plugin_namespace,
  dependencies: skill.dependencies
}

current_skill_index += 1
```

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
