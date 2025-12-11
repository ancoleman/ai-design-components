# Subagent Testing Framework

Automated testing framework for validating subagent definitions in the AI Design Components library.

## Purpose

This testing framework validates that subagents:
1. **Activate correctly** - Trigger when they should (>80% activation rate)
2. **Execute completely** - Follow their defined protocols without skipping steps
3. **Report consistently** - Use standardized output formats
4. **Maintain tool restrictions** - Only use permitted tools
5. **Produce quality outputs** - Generate expected files and content

## Test Case Format

Test cases are defined in YAML format following this schema:

```yaml
# evaluation/subagent-tests/{subagent-name}/{test-file}.yaml

name: test-suite-name
description: Brief description of what this test suite validates
subagent: subagent-name  # skill-executor, skillchain-validator, skillchain-planner

test_cases:
  - name: test-case-id
    description: What this specific test validates

    # The prompt sent to the subagent
    prompt: |
      Multi-line prompt text here.
      Can include project context, preferences, etc.

    # Expected behaviors and outputs
    expected:
      # Skill invocation (for skill executors)
      skill_invoked: "registry:skill-name"

      # Files that should be created
      files_created:
        - pattern: "*.css"          # Glob pattern
          min_count: 1              # Minimum number of matches
        - pattern: "src/**/*.tsx"
          min_count: 3

      # Content that should appear in the final report
      report_contains:
        - "SKILL COMPLETE"
        - "FILES CREATED"
        - "KEY DECISIONS"

      # Content that should NOT appear
      report_excludes:
        - "Error:"
        - "FAILED"

      # Optional: Regex patterns for advanced validation
      report_matches:
        - pattern: "COMPLETENESS: \\d+%"
          description: "Completeness percentage reported"

    # Test execution settings
    timeout: 120  # Seconds (default: 120)
    cwd: /tmp/test-project  # Working directory (optional)

    # Optional: Setup/teardown commands
    setup:
      - "mkdir -p /tmp/test-project"
      - "cd /tmp/test-project && npm init -y"
    teardown:
      - "rm -rf /tmp/test-project"
```

## Expected Section Structure

### For Skill Executors

```yaml
expected:
  skill_invoked: "ui-foundation-skills:theming-components"

  files_created:
    - pattern: "src/styles/tokens.css"
      min_count: 1
    - pattern: "src/components/**/*.tsx"
      min_count: 2

  report_contains:
    - "SKILL COMPLETE: theming-components"
    - "FILES CREATED:"
    - "KEY DECISIONS:"
    - "OUTPUTS FOR NEXT SKILL:"

  report_excludes:
    - "Error"
    - "WARNINGS:"  # Should have no warnings for basic tests
```

### For Validator Subagent

```yaml
expected:
  files_created: []  # Validators should not create files

  report_contains:
    - "VALIDATION REPORT"
    - "DELIVERABLES:"
    - "FILE COVERAGE:"
    - "COMPLETENESS:"
    - "STATUS: PASS"

  report_matches:
    - pattern: "COMPLETENESS: \\d+%"
    - pattern: "Expected: \\d+ files"
```

### For Planner Subagent

```yaml
expected:
  files_created: []  # Planners should not create files

  report_contains:
    - "skillchain_plan:"
    - "goal:"
    - "skills:"
    - "execution_mode:"

  report_matches:
    - pattern: "name: [a-z-]+"
      description: "Skill names in kebab-case"
    - pattern: "invocation: [a-z-]+:[a-z-]+"
      description: "Skill invocation strings"
```

## How to Run Tests

### Using the Test Runner

The `subagent_tester.py` script (to be created in Phase 4 of the implementation plan) will provide automated test execution:

```bash
# Run all tests for a specific subagent
python evaluation/subagent_tester.py --subagent skill-executor

# Run a specific test file
python evaluation/subagent_tester.py --test evaluation/subagent-tests/skill-executor/basic.yaml

# Run all tests across all subagents
python evaluation/subagent_tester.py --all

# Verbose output for debugging
python evaluation/subagent_tester.py --subagent skill-executor --verbose

# Generate JSON report
python evaluation/subagent_tester.py --all --report subagent-test-results.json
```

### Manual Testing

You can manually test a subagent using the Claude Code CLI directly:

```bash
# Navigate to test project directory
mkdir -p /tmp/test-project
cd /tmp/test-project

# Execute with the subagent
claude \
  --print \
  --verbose \
  --output-format stream-json \
  --dangerously-skip-permissions \
  --agent skill-executor \
  -- "Execute the theming-components skill for a React dashboard"

# Check output manually
ls -la
```

## Pass Criteria

Tests are evaluated on multiple dimensions:

### 1. Activation Rate (>80% required)

**Definition:** Percentage of tests where the subagent correctly activates and completes.

**Calculation:**
```
activation_rate = (successful_completions / total_tests) * 100
```

**Pass threshold:** 80%

### 2. Protocol Adherence (>90% required)

**Definition:** Percentage of tests where the subagent follows its defined protocol (e.g., includes all required report sections).

**Validation:**
- All `report_contains` items present
- No `report_excludes` items present
- All `report_matches` patterns match

**Pass threshold:** 90%

### 3. Output Quality (>85% required)

**Definition:** Percentage of tests where expected files are created with correct structure.

**Validation:**
- All `files_created` patterns match minimum counts
- Files contain expected content (if content checks defined)
- No unexpected files created

**Pass threshold:** 85%

### 4. Tool Compliance (100% required)

**Definition:** Subagent only uses permitted tools (per tool restrictions matrix).

**Validation:**
- Parse session JSONL for tool invocations
- Compare against subagent's allowed tools
- Any unauthorized tool use = FAIL

**Pass threshold:** 100%

## Example Test Case (Complete)

```yaml
name: skill-executor-basic-invocation
description: Validates basic skill invocation and reporting for skill-executor subagent
subagent: skill-executor

test_cases:
  - name: invoke-theming-components
    description: Execute theming-components skill with preferences

    prompt: |
      Execute the theming-components skill for a React dashboard project.

      Project context:
      - Path: /tmp/test-theming
      - Framework: React with TypeScript
      - Build tool: Vite

      User preferences:
      - Color scheme: blue-gray
      - Modes: light and dark
      - Typography: Inter font family

    expected:
      skill_invoked: "ui-foundation-skills:theming-components"

      files_created:
        - pattern: "src/styles/tokens.css"
          min_count: 1
        - pattern: "src/styles/*-theme.css"
          min_count: 2  # light-theme.css, dark-theme.css

      report_contains:
        - "SKILL COMPLETE: theming-components"
        - "FILES CREATED:"
        - "src/styles/tokens.css"
        - "KEY DECISIONS:"
        - "color scheme: blue-gray"
        - "OUTPUTS FOR NEXT SKILL:"
        - "theme_tokens"

      report_excludes:
        - "Error:"
        - "failed"

      report_matches:
        - pattern: "FILES CREATED:\n(- .+\n)+"
          description: "Files listed in bullet format"

    timeout: 180

    setup:
      - "mkdir -p /tmp/test-theming/src/styles"
      - "cd /tmp/test-theming && npm init -y"

    teardown:
      - "rm -rf /tmp/test-theming"

  - name: invoke-building-forms
    description: Execute building-forms skill with validation requirements

    prompt: |
      Execute the building-forms skill.

      Project context:
      - Path: /tmp/test-forms
      - Framework: React with TypeScript

      Requirements:
      - Use React Hook Form
      - Validation: Zod
      - Include email, password, and checkbox fields

    expected:
      skill_invoked: "ui-input-skills:building-forms"

      files_created:
        - pattern: "src/components/**/*.tsx"
          min_count: 1
        - pattern: "src/validation/**/*.ts"
          min_count: 1

      report_contains:
        - "SKILL COMPLETE: building-forms"
        - "React Hook Form"
        - "Zod"

    timeout: 180

    setup:
      - "mkdir -p /tmp/test-forms/src/{components,validation}"

    teardown:
      - "rm -rf /tmp/test-forms"
```

## CI Integration

### GitHub Actions Workflow

The testing framework integrates with CI via GitHub Actions:

```yaml
# .github/workflows/test-subagents.yml
name: Test Subagents

on:
  push:
    paths:
      - '.claude/agents/**'
      - 'evaluation/subagent-tests/**'
  pull_request:
    paths:
      - '.claude/agents/**'
      - 'evaluation/subagent-tests/**'

jobs:
  test-subagents:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        subagent:
          - skill-executor
          - frontend-skill-executor
          - backend-skill-executor
          - skillchain-validator
          - skillchain-planner

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Claude Code CLI
        run: |
          npm install -g @anthropic-ai/claude-code

      - name: Install Subagents
        run: |
          mkdir -p ~/.claude/agents
          cp -r .claude/agents/* ~/.claude/agents/

      - name: Run Tests
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python evaluation/subagent_tester.py \
            --subagent ${{ matrix.subagent }} \
            --report test-results-${{ matrix.subagent }}.json \
            --verbose

      - name: Check Pass Rate
        run: |
          PASS_RATE=$(jq '.pass_rate' test-results-${{ matrix.subagent }}.json)
          echo "Pass rate for ${{ matrix.subagent }}: $PASS_RATE%"

          if (( $(echo "$PASS_RATE < 80" | bc -l) )); then
            echo "::error::Pass rate $PASS_RATE% below 80% threshold"
            exit 1
          fi

      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results-${{ matrix.subagent }}
          path: test-results-${{ matrix.subagent }}.json
```

### Expected CI Output

```
Test Subagents / test-subagents (skill-executor)
  ✓ Setup Python
  ✓ Install Claude Code CLI
  ✓ Install Subagents
  ✓ Run Tests

    SUBAGENT TEST RESULTS: skill-executor
    ==================================================

    Tests run: 5
    Passed: 4
    Failed: 1

    ACTIVATION RATE: 80%
    PROTOCOL ADHERENCE: 100%
    OUTPUT QUALITY: 80%
    TOOL COMPLIANCE: 100%

    FAILED TESTS:
    - invoke-complex-chain: Expected file pattern not found

  ✓ Check Pass Rate (80% >= 80%)
  ✓ Upload Results
```

## Test Organization

### Directory Structure

```
evaluation/subagent-tests/
├── README.md (this file)
│
├── skill-executor/
│   ├── basic.yaml              # Basic skill invocation
│   ├── frontend-skills.yaml    # Frontend-specific skills
│   ├── backend-skills.yaml     # Backend-specific skills
│   ├── error-handling.yaml     # Error scenarios
│   └── context-passing.yaml    # Multi-skill chains
│
├── validator/
│   ├── blueprint-validation.yaml     # Blueprint deliverable checks
│   ├── file-validation.yaml          # File existence checks
│   ├── content-validation.yaml       # Content pattern checks
│   └── readonly-enforcement.yaml     # Ensure no modifications
│
└── planner/
    ├── blueprint-matching.yaml       # Blueprint selection
    ├── skill-selection.yaml          # Skill graph traversal
    ├── dependency-ordering.yaml      # Skill ordering logic
    └── parallel-detection.yaml       # Parallelization opportunities
```

### Naming Conventions

**Test suite files:** Use kebab-case with descriptive names
- ✓ `basic.yaml`, `frontend-skills.yaml`, `error-handling.yaml`
- ✗ `test1.yaml`, `tests.yaml`, `misc.yaml`

**Test case IDs:** Use kebab-case with verb-noun pattern
- ✓ `invoke-theming-components`, `validate-deliverables`, `plan-rag-pipeline`
- ✗ `test1`, `theming`, `case_2`

**Subagent names:** Match agent definition filenames (without .md)
- ✓ `skill-executor`, `skillchain-validator`, `frontend-skill-executor`
- ✗ `executor`, `validator`, `frontend`

## Writing Effective Tests

### Test Independence

Each test should be self-contained and not depend on other tests:

```yaml
# GOOD: Self-contained test
- name: invoke-theming
  setup:
    - "mkdir -p /tmp/test-theming"
  prompt: "Execute theming-components skill"
  teardown:
    - "rm -rf /tmp/test-theming"

# BAD: Depends on previous test state
- name: invoke-forms
  prompt: "Execute building-forms (assumes theming already run)"
```

### Clear Expectations

Be specific about what you expect:

```yaml
# GOOD: Specific expectations
expected:
  files_created:
    - pattern: "src/styles/tokens.css"
      min_count: 1
  report_contains:
    - "color scheme: blue-gray"

# BAD: Vague expectations
expected:
  files_created:
    - pattern: "**/*"
      min_count: 1
  report_contains:
    - "complete"
```

### Realistic Prompts

Use prompts that match real usage:

```yaml
# GOOD: Realistic prompt with context
prompt: |
  Execute the theming-components skill for a React dashboard.

  Project: /tmp/test-project
  Framework: React + TypeScript
  Preferences: blue-gray theme, light/dark modes

# BAD: Minimal prompt
prompt: "Run theming skill"
```

## Troubleshooting

### Test Failures

**Activation failures (subagent doesn't run):**
- Check subagent name matches definition file
- Verify subagent is installed in `~/.claude/agents/`
- Check prompt triggers subagent's description keywords

**Protocol violations (missing report sections):**
- Review subagent definition for required output format
- Check if prompt provided enough context
- Verify timeout is sufficient

**File creation failures:**
- Check glob patterns are correct
- Verify setup commands created required directories
- Review subagent's file writing permissions

**Tool compliance failures:**
- Parse session JSONL for tool invocations
- Compare against subagent's tool restrictions
- Report unauthorized tool usage

### Debugging Tips

```bash
# 1. Run test manually with verbose output
claude --print --verbose --agent skill-executor -- "Execute theming skill"

# 2. Check session file for tool invocations
cat ~/.claude/projects/*/latest-session.jsonl | grep '"type":"tool_use"'

# 3. Verify subagent definition
cat ~/.claude/agents/skill-executor.md

# 4. Test without subagent (compare behavior)
claude --print -- "Execute theming skill"
```

## Test Metrics

### Collected Metrics

For each test run, collect:

```json
{
  "test_name": "invoke-theming-components",
  "subagent": "skill-executor",
  "status": "passed",
  "duration_seconds": 45.2,
  "activation": true,
  "protocol_adherence": {
    "score": 1.0,
    "missing_sections": [],
    "unexpected_sections": []
  },
  "output_quality": {
    "score": 1.0,
    "files_expected": 3,
    "files_found": 3,
    "content_checks_passed": 2,
    "content_checks_failed": 0
  },
  "tool_compliance": {
    "score": 1.0,
    "unauthorized_tools": []
  },
  "cost_usd": 0.0234,
  "tokens": {
    "input": 1500,
    "output": 500
  }
}
```

### Aggregate Reports

Generate aggregate reports across all tests:

```json
{
  "subagent": "skill-executor",
  "total_tests": 12,
  "passed": 11,
  "failed": 1,
  "activation_rate": 0.917,
  "protocol_adherence_avg": 0.983,
  "output_quality_avg": 0.908,
  "tool_compliance_rate": 1.0,
  "total_cost_usd": 0.42,
  "avg_duration_seconds": 52.3,
  "failed_tests": [
    "invoke-complex-chain"
  ]
}
```

## Future Enhancements

Potential improvements to the testing framework:

1. **Parallel test execution** - Run independent tests concurrently
2. **Snapshot testing** - Compare output against saved snapshots
3. **Performance regression detection** - Track duration/cost trends
4. **Flakiness detection** - Automatic retry for flaky tests
5. **Test generation** - Auto-generate tests from subagent definitions
6. **Visual diff tools** - Compare generated files visually
7. **Integration with existing evaluation/** - Unified test runner
8. **Coverage tracking** - Which subagent features are tested

## Contributing

When adding new tests:

1. Follow the test case format exactly
2. Include setup/teardown for isolated execution
3. Use descriptive names for tests and files
4. Add comments explaining non-obvious expectations
5. Test locally before committing
6. Update this README if adding new patterns

## Related Documentation

- [Subagent Architecture Plan](../../source_data/ideas/subagent-architecture/PLAN.md) - Complete subagent system design
- [Claude Code Integration Patterns](../../source_data/ideas/cc-integration/patterns.md) - CLI integration patterns
- [Existing Evaluation Tools](../README.md) - Other validation tools in this repo

---

**Last Updated:** 2025-12-10
**Version:** 1.0.0
**Status:** Initial implementation (Phase 4 pending)
