# Subagent Tester Framework

Comprehensive documentation for the automated testing framework for Claude Code skills and subagent behaviors.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [CLI Reference](#cli-reference)
5. [Test File Format](#test-file-format)
6. [How It Works](#how-it-works)
7. [Output Formats](#output-formats)
8. [Troubleshooting](#troubleshooting)
9. [CI Integration](#ci-integration)

---

## Overview

### What It Does

The Subagent Tester is a Python-based testing framework that validates Claude Code skills and subagent behaviors by:

- **Spawning Claude Code CLI sessions** in headless mode with structured output
- **Parsing JSONL responses** to extract results, costs, and token usage
- **Validating outputs** against expected results across multiple dimensions
- **Generating reports** with pass/fail metrics, cost analysis, and failure diagnostics
- **Supporting CI/CD integration** for automated quality assurance

### Why It Exists

Testing subagent behaviors requires validating:
1. **Activation** - Does the skill/subagent trigger when it should?
2. **Protocol adherence** - Does it follow defined output formats?
3. **Output quality** - Does it create expected files and content?
4. **Tool compliance** - Does it only use permitted tools?

Manual testing is time-consuming and inconsistent. This framework automates validation across all these dimensions.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Subagent Tester (Python)                 │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │  Test Loader │───▶│ CLI Spawner  │───▶│  Validator   │ │
│  │  (YAML)      │    │  (subprocess)│    │  (expected)  │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                    │                    │         │
│         ▼                    ▼                    ▼         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │ Test Cases   │    │ JSONL Parser │    │   Reporter   │ │
│  │ (setup/      │    │ (stream-json)│    │ (console/    │ │
│  │  teardown)   │    │              │    │  JSON)       │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │   Claude Code CLI    │
                   │   (--print mode)     │
                   │   (stream-json out)  │
                   └──────────────────────┘
```

**Flow:**
1. Load test cases from YAML files
2. Run setup commands (create directories, install dependencies)
3. Spawn Claude Code CLI with `--print` (headless mode) and `--output-format stream-json`
4. Parse JSONL output to extract session ID, text, cost, tokens
5. Validate output against expected criteria
6. Run teardown commands (cleanup)
7. Generate reports with metrics and diagnostics

---

## Prerequisites

### Claude Code CLI Installation

The tester requires the Claude Code CLI to be installed and accessible in your PATH.

**Install via npm:**
```bash
npm install -g @anthropic-ai/claude-code
```

**Install via Homebrew:**
```bash
brew install claude-code
```

**Verify installation:**
```bash
claude --version
```

### Authentication Options

The tester supports multiple authentication methods (in order of precedence):

#### Option 1: API Key (Recommended for CI/CD)
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

#### Option 2: Interactive Login
```bash
claude login
# Follow the browser authentication flow
```

#### Option 3: AWS Bedrock
```bash
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_ACCESS_KEY_ID="your-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-west-2"
# OR use AWS profiles:
export AWS_PROFILE="your-profile-name"
```

#### Option 4: Vertex AI
```bash
export CLAUDE_CODE_USE_VERTEX=1
# Ensure you have Vertex AI credentials configured
# (e.g., via gcloud auth application-default login)
```

### Python Dependencies

**Required:**
```bash
pip install pyyaml
```

**Optional (for development):**
```bash
pip install pytest black flake8
```

### System Requirements

- **Python:** 3.8 or higher
- **OS:** macOS, Linux, or Windows (with WSL)
- **Disk:** Sufficient space for test artifacts (typically < 100MB)

---

## Quick Start

### 1. Setup Verification

Before running tests, verify your environment:

```bash
python evaluation/subagent_tester.py --check
```

**Expected output:**
```
Claude Code CLI Setup Check
==================================================
[PASS] Claude CLI found: /opt/homebrew/bin/claude
[PASS] Authentication detected
[PASS] Tests directory found: evaluation/subagent-tests
       Found 15 test file(s)

Quick CLI Test
--------------------------------------------------
[PASS] CLI responds: claude-code v2.1.0

==================================================
Setup check complete. Ready to run tests.
```

### 2. Run a Specific Test

```bash
python evaluation/subagent_tester.py \
  evaluation/subagent-tests/skill-executor/protocol.yaml
```

### 3. Run All Tests for a Subagent

```bash
python evaluation/subagent_tester.py --subagent skill-executor
```

### 4. Run All Tests

```bash
python evaluation/subagent_tester.py --all
```

### 5. Run with Verbose Output

```bash
python evaluation/subagent_tester.py --subagent skill-executor -v
```

### 6. Export Results to JSON

```bash
python evaluation/subagent_tester.py --all --report test-results.json
```

---

## CLI Reference

### Command Syntax

```bash
python evaluation/subagent_tester.py [OPTIONS] [TEST_FILE]
```

### Positional Arguments

| Argument | Description |
|----------|-------------|
| `test_file` | Path to a specific YAML test file to run (optional) |

### Options

#### Test Selection

| Option | Description | Example |
|--------|-------------|---------|
| `--all` | Run all tests in `evaluation/subagent-tests/` | `--all` |
| `--subagent NAME` | Run all tests for a specific subagent category | `--subagent skill-executor` |
| `test_file` | Run a specific test file | `path/to/test.yaml` |

#### Configuration

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--model MODEL` | Override Claude model | Uses CLI default | `--model claude-sonnet-4-20250514` |
| `--max-turns N` | Limit number of agentic turns | None | `--max-turns 5` |
| `--allow-permissions` | Allow permission prompts | False (skip) | `--allow-permissions` |

**Note:** By default, `--dangerously-skip-permissions` is used for automation. Use `--allow-permissions` to disable this behavior.

#### Output & Debugging

| Option | Description | Example |
|--------|-------------|---------|
| `--verbose`, `-v` | Enable verbose debug output | `-v` |
| `--report FILE` | Export results to JSON file | `--report results.json` |
| `--check` | Verify setup and exit (no tests run) | `--check` |

### Examples

**Check setup:**
```bash
python evaluation/subagent_tester.py --check
```

**Run specific test with verbose output:**
```bash
python evaluation/subagent_tester.py \
  evaluation/subagent-tests/skill-executor/basic.yaml \
  -v
```

**Run all tests for skill-executor with Opus:**
```bash
python evaluation/subagent_tester.py \
  --subagent skill-executor \
  --model claude-opus-4-20250514
```

**Run all tests with cost limits:**
```bash
python evaluation/subagent_tester.py \
  --all \
  --max-turns 3 \
  --report full-results.json
```

**Run with custom authentication:**
```bash
ANTHROPIC_API_KEY="sk-ant-..." \
python evaluation/subagent_tester.py \
  --all \
  --verbose
```

---

## Test File Format

### YAML Schema

Test cases are defined in YAML files following this structure:

```yaml
name: test-suite-name
description: Brief description of what this test suite validates
subagent: subagent-name  # e.g., skill-executor, skillchain-validator

# Optional: Setup commands run before all tests
setup:
  - "mkdir -p /tmp/test-project"
  - "cd /tmp/test-project && npm init -y"

test_cases:
  - name: test-case-id
    description: What this specific test validates

    # The prompt sent to Claude
    prompt: |
      Multi-line prompt text here.
      Can include project context, user preferences, etc.

    # Expected behaviors and outputs
    expected:
      # Check skill invocation (for skill executors)
      skill_invoked: "registry:skill-name"

      # Files that should be created
      files_created:
        - pattern: "*.css"          # Glob pattern
          min_count: 1              # Minimum number of matches
        - pattern: "src/**/*.tsx"
          min_count: 3

      # Content that must appear in final output
      report_contains:
        - "SKILL COMPLETE"
        - "FILES CREATED"
        - "KEY DECISIONS"

      # Content that must NOT appear
      report_excludes:
        - "Error:"
        - "FAILED"

      # Regex patterns for advanced validation
      report_matches:
        - pattern: "COMPLETENESS: \\d+%"
          description: "Completeness percentage reported"
        - pattern: "FILES CREATED:\\n(- .+\\n)+"
          description: "Files listed in bullet format"

    # Test execution settings
    timeout: 120  # Seconds (default: 120)
    cwd: /tmp/test-project  # Working directory (optional)

    # Per-test setup/teardown
    setup:
      - "mkdir -p /tmp/test-project/src"
    teardown:
      - "rm -rf /tmp/test-project"

    # Claude Code CLI overrides (optional)
    model: claude-opus-4-20250514
    max_turns: 5
    system_prompt: "Custom system prompt for this test"
    allowed_tools: ["Read", "Write", "Bash"]
    disallowed_tools: ["WebSearch"]
    resume_session: "session-id-to-resume"

# Optional: Teardown commands run after all tests
teardown:
  - "rm -rf /tmp/test-project"
```

### Field Reference

#### Top-Level Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | String | Test suite name (kebab-case) |
| `description` | Yes | String | Brief description of test suite |
| `subagent` | Yes | String | Subagent category (matches directory name) |
| `setup` | No | List[String] | Commands to run before all tests |
| `teardown` | No | List[String] | Commands to run after all tests |
| `test_cases` | Yes | List[Object] | Individual test case definitions |

#### Test Case Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | String | Test case ID (kebab-case, verb-noun) |
| `description` | No | String | What this test validates |
| `prompt` | Yes | String | Prompt to send to Claude |
| `expected` | Yes | Object | Expected results (see below) |
| `timeout` | No | Integer | Timeout in seconds (default: 120) |
| `cwd` | No | String | Working directory for test |
| `setup` | No | List[String] | Commands to run before this test |
| `teardown` | No | List[String] | Commands to run after this test |
| `model` | No | String | Override Claude model |
| `max_turns` | No | Integer | Limit agentic turns |
| `system_prompt` | No | String | Custom system prompt |
| `allowed_tools` | No | List[String] | Whitelist of allowed tools |
| `disallowed_tools` | No | List[String] | Blacklist of disallowed tools |
| `resume_session` | No | String | Session ID to resume |

#### Expected Results Fields

| Field | Type | Description |
|-------|------|-------------|
| `skill_invoked` | String | Skill name that should appear in output |
| `files_created` | List[Object] | File patterns to validate (see below) |
| `report_contains` | List[String] | Strings that must appear in output |
| `report_excludes` | List[String] | Strings that must NOT appear |
| `report_matches` | List[Object] | Regex patterns to match (see below) |

**File Creation Spec:**
```yaml
files_created:
  - pattern: "src/**/*.tsx"  # Glob pattern
    min_count: 1              # Minimum matches required
```

**Regex Match Spec:**
```yaml
report_matches:
  - pattern: "COMPLETENESS: \\d+%"
    description: "Human-readable description for reports"
```

### Complete Example

See `/Users/antoncoleman/Documents/repos/ai-design-components/evaluation/subagent-tests/skill-executor/protocol.yaml` for a full working example.

**Minimal example:**
```yaml
name: basic-skill-test
description: Test basic skill invocation
subagent: skill-executor

test_cases:
  - name: invoke-theming
    prompt: |
      Execute the theming-components skill for a React app.
      Project: /tmp/test-theming
      Framework: React with TypeScript
      Theme: Blue-gray, light and dark modes

    expected:
      skill_invoked: "ui-foundation-skills:theming-components"
      files_created:
        - pattern: "src/styles/*.css"
          min_count: 1
      report_contains:
        - "SKILL COMPLETE"
      report_excludes:
        - "Error:"

    timeout: 180
    setup:
      - "mkdir -p /tmp/test-theming/src/styles"
    teardown:
      - "rm -rf /tmp/test-theming"
```

---

## How It Works

### 1. CLI Spawning Process

The tester uses Python's `subprocess` module to spawn Claude Code CLI in headless mode:

```python
# Command structure
claude \
  --print "prompt text" \
  --output-format stream-json \
  --dangerously-skip-permissions \
  --model claude-sonnet-4-20250514 \
  --max-turns 5
```

**Key flags:**
- `--print`: Execute prompt and exit (non-interactive/headless mode)
- `--output-format stream-json`: Return structured JSONL for parsing
- `--dangerously-skip-permissions`: Skip permission prompts for automation

**Process management:**
- Working directory set to test's `cwd` or project root
- Environment includes expanded PATH for CLI discovery
- STDIN set to `subprocess.DEVNULL` to prevent blocking
- Timeout enforced via `subprocess.run(timeout=N)`

### 2. JSONL Output Parsing

Claude Code CLI outputs JSONL (JSON Lines) with multiple message types:

**Message Types:**

1. **`system:init`** - Session initialization
```json
{
  "type": "system",
  "subtype": "init",
  "session_id": "sess_abc123",
  "slash_commands": [...]
}
```

2. **`assistant`** - Streaming partial responses (skipped)
```json
{
  "type": "assistant",
  "text": "Partial response..."
}
```

3. **`result`** - Final complete response with metrics
```json
{
  "type": "result",
  "session_id": "sess_abc123",
  "result": "Complete response text...",
  "total_cost_usd": 0.0234,
  "modelUsage": {
    "claude-sonnet-4": {
      "inputTokens": 1500,
      "outputTokens": 500,
      "cacheReadInputTokens": 800,
      "cacheCreationInputTokens": 0
    }
  }
}
```

**Parser extracts:**
- `session_id`: For session tracking
- `text`: Final response text from `result` message
- `cost`: Total cost in USD
- `tokens`: Input/output/cache token counts
- `errors`: Any stderr output

### 3. Result Validation Logic

Validation occurs across four dimensions:

#### A. Protocol Adherence

Checks that output follows defined format:

```python
# Check required strings present
for marker in expected['report_contains']:
    if marker not in output_text:
        errors.append(f"Missing: {marker}")

# Check forbidden strings absent
for marker in expected['report_excludes']:
    if marker in output_text:
        errors.append(f"Forbidden: {marker}")

# Check regex patterns
for pattern_spec in expected['report_matches']:
    if not re.search(pattern_spec['pattern'], output_text):
        errors.append(f"Pattern not matched: {pattern_spec['description']}")
```

**Score:** `passed_checks / total_checks`

#### B. Output Quality

Validates file creation:

```python
# Use glob to find matching files
for file_spec in expected['files_created']:
    matches = Path(work_dir).glob(file_spec['pattern'])
    found_count = len(list(matches))
    if found_count < file_spec['min_count']:
        errors.append(f"File pattern '{pattern}': expected >={min_count}, found {found_count}")
```

**Score:** `passed_file_checks / total_file_checks`

#### C. Activation

Binary check: Did subagent produce output?

```python
activation = bool(output_text.strip())
```

#### D. Tool Compliance

Placeholder for future enhancement (currently assumes compliant):

```python
# TODO: Parse session JSONL for tool_use messages
# Compare against allowed/disallowed tools
tool_score = 1.0
```

### 4. Scoring System

**Per-test scores:**
- **Activation:** Boolean (0.0 or 1.0)
- **Protocol Adherence:** 0.0-1.0 (percentage of checks passed)
- **Output Quality:** 0.0-1.0 (percentage of file checks passed)
- **Tool Compliance:** 0.0-1.0 (currently always 1.0)

**Aggregate scores (across test suite):**
- **Activation Rate:** `sum(activation) / total_tests`
- **Protocol Adherence Avg:** `sum(protocol_scores) / total_tests`
- **Output Quality Avg:** `sum(quality_scores) / total_tests`
- **Tool Compliance Rate:** `sum(tool_scores) / total_tests`

**Pass criteria:**
- Activation Rate: ≥80%
- Protocol Adherence: ≥90%
- Output Quality: ≥85%
- Tool Compliance: 100% (required)

---

## Output Formats

### Console Output

#### Test Execution

**Color-coded results:**
```
======================================================================
Test Suite: skill-executor-protocol-adherence
Subagent: skill-executor
Tests: 7
======================================================================

Running test: announces-before-invocation
Skill/Subagent Category: skill-executor
✓ announces-before-invocation PASSED (45.2s, $0.0234)

Running test: uses-skill-tool
Skill/Subagent Category: skill-executor
✗ uses-skill-tool FAILED (32.1s)
  - Expected text 'Skill:' not found in output
```

**Colors:**
- Green: Pass
- Red: Fail
- Yellow: Warning
- Cyan: Debug (with `-v`)

#### Summary Report

```
SUBAGENT TEST RESULTS: skill-executor
======================================================================

Tests run: 7
Passed: 6
Failed: 1

ACTIVATION RATE: 100.0%
PROTOCOL ADHERENCE: 92.3%
OUTPUT QUALITY: 85.7%
TOOL COMPLIANCE: 100.0%

Total Cost: $0.1432
Avg Duration: 38.4s

FAILED TESTS:
  - uses-skill-tool
    Expected text 'Skill:' not found in output
```

### JSON Export Format

Exported via `--report FILE`:

```json
{
  "timestamp": "2025-12-10T14:23:45.123456",
  "aggregates": [
    {
      "subagent": "skill-executor",
      "total_tests": 7,
      "passed": 6,
      "failed": 1,
      "activation_rate": 1.0,
      "protocol_adherence_avg": 0.923,
      "output_quality_avg": 0.857,
      "tool_compliance_rate": 1.0,
      "total_cost_usd": 0.1432,
      "avg_duration_seconds": 38.4,
      "failed_tests": ["uses-skill-tool"]
    }
  ],
  "individual_results": [
    {
      "name": "announces-before-invocation",
      "subagent": "skill-executor",
      "passed": true,
      "duration_seconds": 45.2,
      "activation": true,
      "protocol_adherence": {
        "score": 1.0,
        "checks": [
          {"check": "contains:Now invoking skill:", "passed": true},
          {"check": "excludes:Error:", "passed": true}
        ],
        "passed": 2,
        "total": 2
      },
      "output_quality": {
        "score": 1.0,
        "checks": [
          {"check": "files:src/styles/*.css", "expected": 1, "found": 2, "passed": true}
        ],
        "passed": 1,
        "total": 1
      },
      "tool_compliance": {
        "score": 1.0,
        "unauthorized_tools": []
      },
      "cost_usd": 0.0234,
      "tokens": {
        "input": 1500,
        "output": 500,
        "cache_read": 800,
        "cache_creation": 0
      },
      "errors": []
    },
    {
      "name": "uses-skill-tool",
      "subagent": "skill-executor",
      "passed": false,
      "duration_seconds": 32.1,
      "activation": true,
      "protocol_adherence": {
        "score": 0.5,
        "checks": [
          {"check": "contains:Skill:", "passed": false},
          {"check": "contains:building-forms", "passed": true}
        ],
        "passed": 1,
        "total": 2
      },
      "output_quality": {
        "score": 1.0,
        "checks": [],
        "passed": 0,
        "total": 0
      },
      "tool_compliance": {
        "score": 1.0,
        "unauthorized_tools": []
      },
      "cost_usd": 0.0198,
      "tokens": {
        "input": 1200,
        "output": 400,
        "cache_read": 600,
        "cache_creation": 0
      },
      "errors": [
        "Expected text 'Skill:' not found in output"
      ]
    }
  ]
}
```

**Use cases:**
- Aggregate analysis across test runs
- Cost tracking over time
- Performance regression detection
- CI/CD pipeline reporting

---

## Troubleshooting

### Common Errors

#### 1. Claude CLI Not Found

**Error:**
```
[FAIL] Claude CLI not found
       Claude Code CLI not found. Please install it:
         npm install -g @anthropic-ai/claude-code
         # or
         brew install claude-code
```

**Solutions:**
- Install Claude Code CLI via npm or Homebrew
- Verify with `which claude`
- Add Claude installation directory to PATH:
  ```bash
  export PATH="/opt/homebrew/bin:$PATH"  # Homebrew Apple Silicon
  export PATH="/usr/local/bin:$PATH"      # Homebrew Intel
  ```
- Use `--check` to diagnose: `python evaluation/subagent_tester.py --check`

#### 2. Authentication Issues

**Error:**
```
[WARN] Authentication may be required
       Claude Code authentication not detected.
       Options:
         1. Set ANTHROPIC_API_KEY environment variable
         2. Run 'claude login' to authenticate interactively
         3. For AWS Bedrock: set CLAUDE_CODE_USE_BEDROCK=1 and AWS credentials
         4. For Vertex AI: set CLAUDE_CODE_USE_VERTEX=1
```

**Solutions:**

**Option 1: API Key**
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**Option 2: Interactive Login**
```bash
claude login
# Follow browser authentication flow
```

**Option 3: AWS Bedrock**
```bash
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_PROFILE="your-profile"
```

**Verify authentication:**
```bash
claude --version  # Should not prompt for auth
```

#### 3. Test Timeout

**Error:**
```
✗ invoke-theming-components TIMEOUT after 120s
```

**Solutions:**
- Increase timeout in test YAML: `timeout: 300`
- Use `--max-turns` to limit agentic loops: `--max-turns 5`
- Check if prompt is unclear or ambiguous
- Use `-v` to see where it's getting stuck

#### 4. File Pattern Not Found

**Error:**
```
✗ invoke-theming FAILED
  - File pattern 'src/styles/*.css': expected >=1, found 0
```

**Solutions:**
- Check setup commands create required directories:
  ```yaml
  setup:
    - "mkdir -p /tmp/test-project/src/styles"
  ```
- Verify `cwd` is set correctly
- Check glob pattern is correct (use `**` for recursive)
- Manually run test and inspect working directory:
  ```bash
  ls -la /tmp/test-project/src/styles/
  ```

#### 5. Skill Not Invoked

**Error:**
```
✗ invoke-theming FAILED
  - Expected skill 'ui-foundation-skills:theming-components' not found in output
```

**Solutions:**
- Verify skill exists in project's `skills/` directory
- Check skill name matches exactly (registry:skill-name)
- Ensure prompt clearly triggers the skill
- Use `-v` to see full output and check for errors
- Verify subagent definition is loaded

#### 6. JSONL Parsing Errors

**Error:**
```
[DEBUG] Non-JSON line: WARNING: Unsupported feature...
```

**Cause:** Claude CLI may output warnings or errors to stdout mixed with JSONL.

**Solutions:**
- Check stderr for additional context
- Use `-v` to see full output
- File bug report if CLI is not producing valid JSONL

#### 7. Permission Errors

**Error:**
```
Error: Operation requires user confirmation
```

**Cause:** Permission prompt appeared despite `--dangerously-skip-permissions`.

**Solutions:**
- Ensure latest Claude Code CLI version
- Check test doesn't require inherently dangerous operations
- Use `--allow-permissions` if interactive prompts are acceptable (not recommended for CI)

### Debugging Workflow

**Step 1: Verify setup**
```bash
python evaluation/subagent_tester.py --check
```

**Step 2: Run test with verbose output**
```bash
python evaluation/subagent_tester.py \
  path/to/test.yaml \
  -v
```

**Step 3: Manual CLI invocation**
```bash
# Navigate to test working directory
cd /tmp/test-project

# Run command manually
claude --print --verbose --output-format stream-json \
  -- "Your test prompt here"
```

**Step 4: Inspect test artifacts**
```bash
# Check files created
ls -la /tmp/test-project/

# Check Claude session logs
ls -la ~/.claude/projects/

# View latest session
cat ~/.claude/projects/*/latest-session.jsonl | jq
```

**Step 5: Isolate the issue**
```bash
# Test without subagent
claude --print -- "Your prompt"

# Test with different model
python evaluation/subagent_tester.py \
  path/to/test.yaml \
  --model claude-haiku-4-20250514
```

### Environment-Specific Issues

#### macOS

**Homebrew Path Issues:**
```bash
# Apple Silicon (M1/M2/M3)
export PATH="/opt/homebrew/bin:$PATH"

# Intel
export PATH="/usr/local/bin:$PATH"
```

**Permission Issues:**
```bash
# Fix npm global permissions
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH="~/.npm-global/bin:$PATH"
```

#### Linux

**Missing Dependencies:**
```bash
# Install Python and pip
sudo apt-get update
sudo apt-get install python3 python3-pip

# Install Node.js for Claude CLI
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### Windows (WSL)

**PATH Issues:**
```bash
# Add Windows npm global to PATH
export PATH="/mnt/c/Users/YourUser/AppData/Roaming/npm:$PATH"
```

**Line Ending Issues:**
```bash
# Convert YAML files to Unix line endings
dos2unix evaluation/subagent-tests/**/*.yaml
```

---

## CI Integration

### GitHub Actions Workflow

**Complete workflow example:**

```yaml
# .github/workflows/test-subagents.yml
name: Test Subagents

on:
  push:
    branches: [main, develop]
    paths:
      - 'skills/**'
      - '.claude/agents/**'
      - 'evaluation/subagent-tests/**'
  pull_request:
    branches: [main, develop]
    paths:
      - 'skills/**'
      - '.claude/agents/**'
      - 'evaluation/subagent-tests/**'
  workflow_dispatch:  # Manual trigger

jobs:
  test-subagents:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    strategy:
      fail-fast: false  # Continue testing other subagents if one fails
      matrix:
        subagent:
          - skill-executor
          - frontend-skill-executor
          - backend-skill-executor
          - skillchain-validator
          - skillchain-planner

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Python dependencies
        run: |
          pip install pyyaml

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install Claude Code CLI
        run: |
          npm install -g @anthropic-ai/claude-code
          claude --version

      - name: Install project skills
        run: |
          # Copy skills to Claude's config directory
          mkdir -p ~/.claude
          # Skills are loaded from project directory automatically

      - name: Run tests
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python evaluation/subagent_tester.py \
            --subagent ${{ matrix.subagent }} \
            --report test-results-${{ matrix.subagent }}.json \
            --max-turns 10 \
            --verbose

      - name: Check pass rate
        run: |
          PASS_RATE=$(jq -r '.aggregates[0].activation_rate * 100' test-results-${{ matrix.subagent }}.json)
          echo "Activation rate for ${{ matrix.subagent }}: $PASS_RATE%"

          if (( $(echo "$PASS_RATE < 80" | bc -l) )); then
            echo "::error::Activation rate $PASS_RATE% below 80% threshold"
            exit 1
          fi

          PROTOCOL_RATE=$(jq -r '.aggregates[0].protocol_adherence_avg * 100' test-results-${{ matrix.subagent }}.json)
          echo "Protocol adherence for ${{ matrix.subagent }}: $PROTOCOL_RATE%"

          if (( $(echo "$PROTOCOL_RATE < 90" | bc -l) )); then
            echo "::error::Protocol adherence $PROTOCOL_RATE% below 90% threshold"
            exit 1
          fi

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results-${{ matrix.subagent }}
          path: test-results-${{ matrix.subagent }}.json
          retention-days: 30

      - name: Comment PR with results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const results = JSON.parse(fs.readFileSync('test-results-${{ matrix.subagent }}.json', 'utf8'));
            const agg = results.aggregates[0];

            const comment = `## Test Results: ${{ matrix.subagent }}

            | Metric | Score | Status |
            |--------|-------|--------|
            | Activation Rate | ${(agg.activation_rate * 100).toFixed(1)}% | ${agg.activation_rate >= 0.8 ? '✅' : '❌'} |
            | Protocol Adherence | ${(agg.protocol_adherence_avg * 100).toFixed(1)}% | ${agg.protocol_adherence_avg >= 0.9 ? '✅' : '❌'} |
            | Output Quality | ${(agg.output_quality_avg * 100).toFixed(1)}% | ${agg.output_quality_avg >= 0.85 ? '✅' : '❌'} |
            | Tool Compliance | ${(agg.tool_compliance_rate * 100).toFixed(1)}% | ${agg.tool_compliance_rate === 1.0 ? '✅' : '❌'} |

            **Tests:** ${agg.passed}/${agg.total_tests} passed
            **Cost:** $${agg.total_cost_usd.toFixed(4)}
            **Avg Duration:** ${agg.avg_duration_seconds.toFixed(1)}s

            ${agg.failed_tests.length > 0 ? `**Failed Tests:**\n${agg.failed_tests.map(t => `- ${t}`).join('\n')}` : ''}
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });

  aggregate-results:
    runs-on: ubuntu-latest
    needs: test-subagents
    if: always()

    steps:
      - name: Download all test results
        uses: actions/download-artifact@v4
        with:
          path: test-results

      - name: Generate aggregate report
        run: |
          echo "# Aggregate Test Results" > aggregate-report.md
          echo "" >> aggregate-report.md

          for file in test-results/*/test-results-*.json; do
            SUBAGENT=$(basename $file .json | sed 's/test-results-//')
            PASSED=$(jq -r '.aggregates[0].passed' $file)
            TOTAL=$(jq -r '.aggregates[0].total_tests' $file)
            COST=$(jq -r '.aggregates[0].total_cost_usd' $file)

            echo "- **$SUBAGENT**: $PASSED/$TOTAL passed (\$$COST)" >> aggregate-report.md
          done

          cat aggregate-report.md

      - name: Upload aggregate report
        uses: actions/upload-artifact@v4
        with:
          name: aggregate-report
          path: aggregate-report.md
```

### Required Secrets

Configure in GitHub repository settings (Settings > Secrets and variables > Actions):

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API key | `sk-ant-api03-...` |

**Optional secrets (for alternative auth):**
| Secret Name | Description |
|-------------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS access key for Bedrock |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key for Bedrock |
| `AWS_REGION` | AWS region for Bedrock |

### CI Best Practices

1. **Cost Control**
   - Use `--max-turns` to limit agentic loops
   - Use Haiku for basic tests, Sonnet for complex tests
   - Monitor total cost via JSON reports

2. **Performance**
   - Use matrix strategy for parallel execution
   - Set reasonable timeouts
   - Cache Python and Node dependencies

3. **Reliability**
   - Set `fail-fast: false` to test all subagents
   - Upload results even on failure (`if: always()`)
   - Implement retry logic for flaky tests

4. **Reporting**
   - Comment PR with test results
   - Generate aggregate reports
   - Track metrics over time

### Local CI Simulation

Test the workflow locally before pushing:

```bash
# Install act (GitHub Actions local runner)
brew install act

# Run workflow locally
act push -s ANTHROPIC_API_KEY="your-key"
```

---

## Advanced Usage

### Custom Test Scenarios

#### Testing Error Handling

```yaml
test_cases:
  - name: handles-missing-dependencies
    prompt: |
      Execute the building-forms skill.
      Project: /tmp/test-error
      Framework: React (but no package.json exists)

    expected:
      report_contains:
        - "WARNING:"
        - "package.json not found"
      report_excludes:
        - "Error:"  # Should warn, not error

    setup:
      - "mkdir -p /tmp/test-error"
    teardown:
      - "rm -rf /tmp/test-error"
```

#### Testing Multi-Skill Chains

```yaml
test_cases:
  - name: chain-theming-to-forms
    prompt: |
      Execute the theming-components skill, then use its outputs
      to execute the building-forms skill.

      Project: /tmp/test-chain
      Framework: React with TypeScript
      Theme: Blue-gray professional

    expected:
      skill_invoked: "ui-foundation-skills:theming-components"
      files_created:
        - pattern: "src/styles/*.css"
          min_count: 1
        - pattern: "src/components/**/*.tsx"
          min_count: 1
      report_contains:
        - "SKILL COMPLETE: theming-components"
        - "SKILL COMPLETE: building-forms"
        - "OUTPUTS FOR NEXT SKILL:"

    timeout: 300
```

#### Testing with Resume

```yaml
test_cases:
  - name: resume-interrupted-session
    prompt: "Continue the previous task"
    resume_session: "sess_abc123"  # From previous test

    expected:
      report_contains:
        - "Continuing from previous session"
```

### Performance Testing

Track performance over time:

```bash
# Run tests and save results with timestamp
python evaluation/subagent_tester.py --all \
  --report "results-$(date +%Y%m%d-%H%M%S).json"

# Extract cost trends
jq '.aggregates[] | {subagent, cost: .total_cost_usd, duration: .avg_duration_seconds}' \
  results-*.json
```

### Integration with Existing Tools

The tester can integrate with existing evaluation tools in `/Users/antoncoleman/Documents/repos/ai-design-components/evaluation/`:

```bash
# Run skill tests
python evaluation/skill_tester.py --all

# Run subagent tests
python evaluation/subagent_tester.py --all

# Compare results
diff skill-results.json subagent-results.json
```

---

## Reference

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All tests passed |
| 1 | One or more tests failed or error occurred |
| 130 | Interrupted by user (Ctrl+C) |

### File Locations

| Path | Description |
|------|-------------|
| `evaluation/subagent_tester.py` | Main test framework script |
| `evaluation/subagent-tests/` | Test case directory |
| `evaluation/subagent-tests/README.md` | Test case format documentation |
| `~/.claude/` | Claude Code configuration directory |
| `~/.claude/projects/` | Claude session data |

### Related Documentation

- [Claude Code CLI Reference](https://code.claude.com/docs/en/cli-reference)
- [Claude SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Test Case Format README](/Users/antoncoleman/Documents/repos/ai-design-components/evaluation/subagent-tests/README.md)
- [Subagent Architecture Plan](../../source_data/ideas/subagent-architecture/PLAN.md)

---

## Changelog

### Version 1.0.0 (2025-12-10)

**Initial release with:**
- Complete test framework implementation
- YAML-based test case format
- CLI spawning and JSONL parsing
- Multi-dimensional validation (activation, protocol, quality, tool compliance)
- Console and JSON reporting
- Setup/teardown support
- Authentication via API key, Bedrock, Vertex, or interactive login
- Verbose debugging mode
- CI integration examples

---

**Last Updated:** 2025-12-10
**Version:** 1.0.0
**Author:** AI Design Components Team
**License:** MIT
