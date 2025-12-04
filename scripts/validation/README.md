# Skill Validation Package

A comprehensive validation toolkit for Claude Skills, supporting both CI/CD pipelines and interactive development workflows.

## Installation

The validation package is included in the repository. Ensure you have the required dependencies:

```bash
pip install pyyaml textual rich
```

## Quick Start

### CI Mode (for pipelines)

```bash
# Validate all completed skills
python -m validation ci --completed

# Output JUnit XML for CI
python -m validation ci --format=junit -o results.xml

# JSON output
python -m validation ci --format=json -o results.json
```

### TUI Mode (interactive)

```bash
# Launch interactive terminal UI
python -m validation tui

# Only show completed skills
python -m validation tui --completed
```

### Single Skill Check

```bash
# Validate a specific skill
python -m validation check building-forms

# With verbose output
python -m validation check building-forms --verbose
```

## Features

### Output Formats

| Format | Flag | Use Case |
|--------|------|----------|
| Console | `--format=console` | Human-readable terminal output (default) |
| JSON | `--format=json` | Programmatic parsing, dashboards |
| JUnit XML | `--format=junit` | CI systems (GitHub Actions, Jenkins) |
| TAP | `--format=tap` | Test Anything Protocol consumers |
| Markdown | `--format=markdown` | Documentation, PR comments |

### Three-Tier Rule System

1. **Core Rules** (`config/rules.yaml`)
   - Required frontmatter fields (name, description)
   - SKILL.md length limits (500 lines max)
   - Anti-patterns (Windows paths, nested references)
   - Reference and example file validation

2. **Community Practices** (`config/community.yaml`)
   - Skill design patterns (progressive disclosure, decision trees)
   - Token optimization suggestions
   - Portability recommendations
   - Quality indicators

3. **Project Rules** (`config/project.yaml`)
   - Repository-specific conventions
   - Example: Skills mentioning libraries should reference `RESEARCH_GUIDE.md`

### TUI Features

- **Real-time validation** with progress indicators
- **Filterable skill list** (all/passed/failed/warnings)
- **Detail panel** showing errors, warnings, project rules, and suggestions
- **Color-coded severity**: red (errors), yellow (warnings), magenta (project rules), blue (suggestions)
- **Keyboard navigation**: j/k, arrows, vim-style bindings

## CLI Reference

### Global Options

| Option | Description |
|--------|-------------|
| `--skills-dir, -d` | Path to skills directory (auto-detected by default) |

### CI Command Options

| Option | Description |
|--------|-------------|
| `--format, -f` | Output format: console, json, junit, tap, markdown |
| `--output, -o` | Write output to file instead of stdout |
| `--completed, -c` | Only validate skills with SKILL.md |
| `--phase, -p` | Only validate skills in specific phase (1-4) |
| `--rules-only` | Skip community practice checks |
| `--skip-project-rules` | Skip project-specific rule checks |
| `--fail-fast` | Stop on first failure |
| `--quiet, -q` | Suppress progress output |
| `--verbose, -v` | Show detailed output including suggestions |

### TUI Command Options

| Option | Description |
|--------|-------------|
| `--completed, -c` | Only show skills with SKILL.md |
| `--phase, -p` | Only show skills in specific phase |
| `--rules-only` | Skip community practice checks |
| `--skip-project-rules` | Skip project-specific rule checks |

### Check Command Options

| Option | Description |
|--------|-------------|
| `--rules-only` | Skip community practice checks |
| `--skip-project-rules` | Skip project-specific rule checks |
| `--verbose, -v` | Show detailed output |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All validations passed |
| 1 | One or more validations failed |
| 2 | Error (invalid config, missing files, etc.) |

## Programmatic API

```python
from validation import Validator, ValidationReport

# Create validator
validator = Validator()

# Validate all skills
report = validator.validate_all("./skills", completed_only=True)

# Check results
if report.all_passed:
    print(f"All {report.total} skills passed!")
else:
    for result in report.failures:
        print(f"{result.skill_name}: {result.errors}")

# Validate single skill
result = validator.validate_skill("./skills/building-forms")
print(f"Passed: {result.passed}")
print(f"Errors: {result.errors}")
print(f"Warnings: {result.warnings}")
```

## Configuration

### Custom Rules

```bash
# Use custom rules file
python -m validation ci --rules=/path/to/rules.yaml

# Use custom community practices
python -m validation ci --community=/path/to/community.yaml

# Use custom project rules
python -m validation ci --project=/path/to/project.yaml
```

### Rule File Format

See the default configuration files in `config/` for the full schema:

- `config/rules.yaml` - Core validation rules
- `config/community.yaml` - Community practices
- `config/project.yaml` - Project-specific rules

## GitHub Actions Integration

```yaml
- name: Validate Skills
  run: |
    cd scripts
    python -m validation ci --completed --format=junit -o results.xml

- name: Upload Test Results
  uses: actions/upload-artifact@v4
  with:
    name: validation-results
    path: scripts/results.xml
```

## Development

### Package Structure

```
scripts/validation/
├── __init__.py          # Public API exports
├── __main__.py          # CLI entry point
├── cli.py               # CI-friendly interface
├── tui.py               # Interactive TUI (Textual)
├── validator.py         # Core validation engine
├── result.py            # Result data types
├── rules.py             # Rule loading and parsing
├── formatters.py        # Output formatters
└── config/
    ├── __init__.py      # Config path utilities
    ├── rules.yaml       # Core validation rules
    ├── community.yaml   # Community practices
    └── project.yaml     # Project-specific rules
```

### Adding New Rules

1. **Core Rules**: Edit `config/rules.yaml`
2. **Community Practices**: Edit `config/community.yaml`
3. **Project Rules**: Edit `config/project.yaml`

### Adding New Formatters

1. Create a new class extending `Formatter` in `formatters.py`
2. Register it in `get_formatter()`
3. Add the format option to CLI arguments

## License

MIT License - See repository LICENSE file.
