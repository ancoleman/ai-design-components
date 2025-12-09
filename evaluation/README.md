# Evaluation Tools

Post-generation validation and quality assurance tools for skillchain-generated projects.

## Overview

This directory contains tools to validate that generated projects meet blueprint requirements and quality standards.

**Note:** Tools have been integrated into the validation package for better organization:
- `completeness_checker.py` → `scripts/runtime/completeness_checker.py`
- `outputs_validator.py` logic → Integrated into `scripts/validation/validator.py` (runs automatically)
- `blueprint_validator.py` logic → Integrated into `scripts/validation/blueprints.py` (CLI: `validation blueprints`)

## Tools

### Blueprint Validation (via `scripts/validation`)

Pre-generation tool for validating blueprint deliverables specifications.

**Purpose:**
- Validates that all blueprints have proper deliverables specifications
- Checks YAML syntax in deliverables and maturity profiles sections
- Ensures deliverables have required fields (primary_skill, required_files)
- Verifies maturity profiles structure (starter, intermediate, advanced)
- Catches blueprint configuration errors before generation

**Usage:**

```bash
# Validate all blueprints
python -m scripts.validation blueprints

# Validate a single blueprint
python -m scripts.validation blueprints api-first.md

# Verbose output
python -m scripts.validation blueprints --verbose

# Show help
python -m scripts.validation blueprints --help
```

**Exit Codes:**
- `0`: All validations passed
- `1`: Some validations failed

**What it validates:**

1. **File Structure:**
   - Blueprint file exists and is valid markdown
   - Has `## Deliverables Specification` section
   - Has `### Deliverables` subsection with valid YAML
   - Has `### Maturity Profiles` subsection with valid YAML

2. **Deliverables:**
   - Has `deliverables` key with at least one deliverable
   - Each deliverable has required fields: `primary_skill`, `required_files`
   - Optional fields are valid: `content_checks`, `maturity_required`, `condition`, `conditional`, `cloud_provider`

3. **Maturity Profiles:**
   - Has all three required profiles: `starter`, `intermediate`, `advanced`
   - Optional fields are valid: `description`, `require_additionally`, `skip_deliverables`, `empty_dirs_allowed`, `generation_adjustments`

**Output Example:**

```
BLUEPRINT DELIVERABLES VALIDATOR
==================================================

Checking blueprints...

✓ api-first.md (31 deliverables)
✓ ci-cd.md (28 deliverables)
✗ crud-api.md - YAML syntax error in maturity profiles

SUMMARY
--------------------------------------------------
Total:   12
Valid:   11
Invalid: 1

ERRORS:
- crud-api.md:
  • No valid YAML code block found in maturity profiles section (YAML syntax error: while parsing a block collection)
```

### `completeness_checker.py` (located at `scripts/runtime/completeness_checker.py`)

Primary tool for checking project completeness after skillchain generation.

**Purpose:**
- Validates generated projects against blueprint deliverables
- Checks for missing files, incomplete implementations
- Supports maturity-level filtering (starter/intermediate/advanced)
- Provides both blueprint-based and basic validation modes

**Usage:**

```bash
# Blueprint-based validation (recommended)
python scripts/runtime/completeness_checker.py --project /path/to/project --blueprint ml-pipeline

# With specific maturity level
python scripts/runtime/completeness_checker.py --project ./my-app --blueprint api-first --maturity advanced

# Basic validation (no blueprint)
python scripts/runtime/completeness_checker.py --project ./my-project

# Verbose output for debugging
python scripts/runtime/completeness_checker.py --project ./my-app --blueprint ml-pipeline --verbose
```

**Exit Codes:**
- `0`: Completeness >= 80% (PASSED)
- `1`: Completeness < 80% (NEEDS ATTENTION)
- `2`: Error (project not found, blueprint not found, etc.)

**Features:**

1. **Blueprint Mode:**
   - Loads blueprint from `~/.claude/commands/skillchain/blueprints/`
   - Parses YAML deliverables specification
   - Checks required files (supports glob patterns)
   - Validates content patterns (regex checks)
   - Filters by maturity level
   - Shows fulfilled/missing/incomplete/skipped status

2. **Basic Mode:**
   - Counts directories and files
   - Identifies empty directories
   - Checks for README.md
   - Calculates directory completeness percentage

**Output Example (Blueprint Mode):**

```
PROJECT COMPLETENESS CHECK
==================================================

Project: /Users/me/my-ml-pipeline
Blueprint: ml-pipeline
Maturity: starter

DELIVERABLES:
✓ MLflow experiment tracking
✓ Training pipeline
✗ Grafana dashboards - MISSING
  └─ Missing: monitoring/grafana/dashboards/*.json
○ Feature store (skipped - not required for starter)
○ Kubernetes (skipped - not required for starter)

SUMMARY:
Required: 5
Fulfilled: 3
Missing: 2
Skipped: 2

Completeness: 60%
Status: NEEDS ATTENTION (target: 80%)
```

**Output Example (Basic Mode):**

```
PROJECT COMPLETENESS CHECK
==================================================

Project: /Users/me/my-project
Mode: Basic (no blueprint)

METRICS:
Total directories: 15
Total files: 42
Empty directories: 3
README exists: Yes

EMPTY DIRECTORIES:
• src/features/
• monitoring/grafana/dashboards/
• data/raw/

Directory completeness: 80%
Status: PASSED
```

## Integration with Skillchain

The completeness checker is designed to work seamlessly with the skillchain workflow:

1. **During Development:**
   ```bash
   /skillchain ml-pipeline
   # ... generation happens ...
   python scripts/runtime/completeness_checker.py --project ./generated-project --blueprint ml-pipeline
   ```

2. **CI/CD Integration:**
   ```yaml
   - name: Validate Project Completeness
     run: |
       python scripts/runtime/completeness_checker.py \
         --project ./generated-project \
         --blueprint ${{ matrix.blueprint }} \
         --maturity intermediate
   ```

3. **Post-Generation Hook:**
   Can be called automatically after skillchain completes to validate output.

## Outputs.yaml Validation

Skill outputs.yaml files (which declare expected deliverables) are now validated automatically as part of the skill validation pipeline:

```bash
# Validates SKILL.md AND outputs.yaml
python -m scripts.validation check building-forms

# Run full CI validation on all skills
python -m scripts.validation ci --completed
```

The validation checks:
- Required fields: `skill`, `version`
- At least one output section: `base_outputs` or `conditional_outputs`
- Proper structure for output items (`path` field required)
- Valid maturity levels in conditional outputs

## Blueprint Requirements

For the completeness checker to work in blueprint mode, blueprints must include a `deliverables` section in YAML format:

```yaml
deliverables:
  mlflow-tracking:
    required_files:
      - "mlflow/mlflow.yml"
      - "scripts/train.py"
    content_checks:
      "scripts/train.py":
        - "import mlflow"
        - "mlflow.start_run"

  training-pipeline:
    required_files:
      - "src/training/**/*.py"
    content_checks:
      "src/training/train.py":
        - "def train_model"

maturity_profiles:
  starter:
    deliverables:
      - mlflow-tracking
      - training-pipeline
  intermediate:
    deliverables:
      - mlflow-tracking
      - training-pipeline
      - grafana-dashboards
  advanced:
    deliverables:
      - mlflow-tracking
      - training-pipeline
      - grafana-dashboards
      - feature-store
      - kubernetes-deployment
```

## Validation Logic

### File Checks
- Supports glob patterns: `monitoring/**/*.json`
- Recursive matching with `**`
- Checks if at least one file matches pattern

### Content Checks
- Uses regex patterns to validate file content
- Can check for imports, function definitions, configurations
- Skips binary files gracefully

### Maturity Filtering
- Loads maturity profile from blueprint
- Only checks deliverables required for specified maturity level
- Reports skipped deliverables separately

## Future Enhancements

Potential additions:
- JSON/YAML output format for machine parsing
- GitHub Actions annotation support
- Auto-fix suggestions for common issues
- Parallel file checking for large projects
- Custom threshold configuration
- Report generation (HTML/PDF)
- Integration with test runners

## Dependencies

- Python 3.7+
- PyYAML (for blueprint parsing)

Install dependencies:
```bash
pip install pyyaml
```

## Development

The script is self-contained and can be extended with additional validators:

```python
class CustomValidator:
    """Add custom validation logic"""

    def validate(self) -> Dict[str, Any]:
        # Your validation logic
        pass
```

See the script source for implementation details.

## License

Same as parent project (see root LICENSE file).
