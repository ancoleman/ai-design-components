---
sidebar_position: 5
title: Skill Validation
description: Validate skills using CI pipelines or interactive TUI
---

# Skill Validation

Validate your Claude Skills using the built-in validation toolkit, supporting both CI/CD pipelines and interactive development workflows.

## Overview

The validation package ensures skills follow Anthropic's best practices and project conventions. It provides:

- **CI Mode**: Machine-readable output for automated pipelines
- **TUI Mode**: Interactive terminal interface for development
- **Three-tier rules**: Core rules, community practices, and project-specific rules

## Quick Start

### Run from the scripts directory

```bash
cd scripts

# CI mode - validate all completed skills
python -m validation ci --completed

# TUI mode - interactive interface
python -m validation tui

# Check a single skill
python -m validation check building-forms
```

## CI Mode

Use CI mode for automated validation in GitHub Actions, Jenkins, or other CI systems.

### Output Formats

```bash
# Console output (default)
python -m validation ci --completed

# JUnit XML for CI systems
python -m validation ci --completed --format=junit -o results.xml

# JSON for programmatic parsing
python -m validation ci --completed --format=json -o results.json

# TAP (Test Anything Protocol)
python -m validation ci --completed --format=tap

# Markdown for PR comments
python -m validation ci --completed --format=markdown
```

### GitHub Actions Example

```yaml
name: Validate Skills

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install pyyaml

      - name: Validate Skills
        run: |
          cd scripts
          python -m validation ci --completed --format=junit -o results.xml

      - name: Upload Results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: validation-results
          path: scripts/results.xml
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All validations passed |
| 1 | One or more validations failed |
| 2 | Error (invalid config, missing files) |

## TUI Mode

Use TUI mode during development for real-time feedback.

```bash
python -m validation tui
```

### Features

- **Real-time validation** with progress indicators
- **Filterable skill list** - press number keys to filter:
  - `1` - All skills
  - `2` - Passed only
  - `3` - Failed only
  - `4` - With warnings
- **Detail panel** showing categorized issues
- **Keyboard navigation**: `j`/`k` or arrows to move, `Enter` to select

### Column Display

| Column | Description | Color |
|--------|-------------|-------|
| # | Row number | - |
| Skill Name | Skill directory name | - |
| Status | PASS/FAIL/PEND | green/red/yellow |
| Err | Error count | red |
| Warn | Core warning count | yellow |
| Proj | Project rule warnings | magenta |
| Sug | Suggestions | blue |

## Three-Tier Rule System

### 1. Core Rules (Errors & Warnings)

Enforced rules based on Anthropic's skill best practices:

- **Frontmatter validation**
  - Required fields: `name`, `description`
  - Name format: lowercase, hyphens, max 64 chars
  - Description: max 1024 chars, no XML tags

- **SKILL.md validation**
  - Maximum 500 lines (body only)
  - Frontmatter must be valid YAML

- **Anti-patterns**
  - Windows-style paths (`\` instead of `/`)
  - Nested references (SKILL.md → file.md → another.md)
  - Second-person language ("you should" instead of imperatives)

- **File references**
  - Referenced files must exist
  - No deeply nested reference chains

### 2. Community Practices (Suggestions)

Best practices from the Claude Skills community:

- Progressive disclosure patterns
- Decision tree frameworks
- Token optimization techniques
- Portability guidelines

### 3. Project Rules (Project-Specific)

Rules specific to ai-design-components:

- Skills mentioning libraries should reference `RESEARCH_GUIDE.md`
- (Additional rules can be added to `config/project.yaml`)

## CLI Options

### Common Options

| Option | Description |
|--------|-------------|
| `--completed, -c` | Only validate skills with SKILL.md |
| `--phase, -p` | Only validate skills in specific phase (1-4) |
| `--rules-only` | Skip community practice checks |
| `--skip-project-rules` | Skip project-specific rules |

### CI-Specific Options

| Option | Description |
|--------|-------------|
| `--format, -f` | Output format (console, json, junit, tap, markdown) |
| `--output, -o` | Write output to file |
| `--fail-fast` | Stop on first failure |
| `--quiet, -q` | Suppress progress output |
| `--verbose, -v` | Include suggestions in output |

## Programmatic API

Use the validation package programmatically:

```python
from validation import Validator, ValidationReport

# Create validator with default rules
validator = Validator()

# Validate all completed skills
report = validator.validate_all(
    skills_dir="./skills",
    completed_only=True
)

# Check results
print(f"Total: {report.total}")
print(f"Passed: {report.passed}")
print(f"Failed: {report.failed}")

if not report.all_passed:
    for result in report.failures:
        print(f"\n{result.skill_name}:")
        for error in result.errors:
            print(f"  ERROR: {error}")

# Validate single skill
result = validator.validate_skill("./skills/building-forms")
print(f"Status: {result.status}")
print(f"Errors: {len(result.errors)}")
print(f"Warnings: {len(result.warnings)}")
```

## Customizing Rules

### Adding Project Rules

Edit `scripts/validation/config/project.yaml`:

```yaml
rules:
  my_custom_rule:
    enabled: true
    severity: "warning"
    description: "Description of the rule"
    check_type: "keyword"
    keywords:
      - "keyword1"
      - "keyword2"
    message: "Message shown when rule fails"
    conditional:
      applies_when_contains:
        - "trigger_word"
```

### Rule Severity Levels

| Level | Behavior |
|-------|----------|
| `error` | Fails validation, exit code 1 |
| `warning` | Reported but doesn't fail |
| `suggestion` | Informational only (community practices) |

## Troubleshooting

### Common Issues

**"No module named validation"**
- Run from the `scripts/` directory: `cd scripts && python -m validation ...`

**TUI not displaying**
- Install Textual: `pip install textual rich`

**Encoding errors**
- Files are read with UTF-8 and error replacement
- Convert problematic files: `iconv -f ISO-8859-1 -t UTF-8 file.md > file_new.md`

## See Also

- [Creating Skills](/docs/guides/creating-skills) - How to create new skills
- [Best Practices](/docs/guides/best-practices) - Skill authoring guidelines
- [Research Methodology](/docs/guides/research-methodology) - Library research guide
