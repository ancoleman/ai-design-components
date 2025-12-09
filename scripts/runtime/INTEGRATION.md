# Integrating Completeness Checker into Workflows

Guide for integrating `completeness_checker.py` into various workflows and automation pipelines.

## Table of Contents

1. [Manual Usage](#manual-usage)
2. [Skillchain Integration](#skillchain-integration)
3. [CI/CD Integration](#cicd-integration)
4. [Pre-commit Hooks](#pre-commit-hooks)
5. [Automated Testing](#automated-testing)

---

## Manual Usage

### Basic Workflow

```bash
# 1. Generate project with skillchain
/skillchain ml-pipeline

# 2. Validate completeness
cd /path/to/generated-project
python /path/to/evaluation/completeness_checker.py \
  --project . \
  --blueprint ml-pipeline \
  --maturity intermediate

# 3. Address any missing deliverables

# 4. Re-validate
python /path/to/evaluation/completeness_checker.py \
  --project . \
  --blueprint ml-pipeline \
  --maturity intermediate
```

### Quick Check Script

Create a convenience script `check.sh`:

```bash
#!/bin/bash
# check.sh - Quick completeness check

PROJECT_DIR="${1:-.}"
BLUEPRINT="${2:-ml-pipeline}"
MATURITY="${3:-intermediate}"

python evaluation/completeness_checker.py \
  --project "$PROJECT_DIR" \
  --blueprint "$BLUEPRINT" \
  --maturity "$MATURITY" \
  --verbose
```

Usage:
```bash
chmod +x check.sh
./check.sh ./my-project ml-pipeline intermediate
```

---

## Skillchain Integration

### Post-Generation Hook

Add validation to the end of skillchain execution:

**Option 1: In skillchain script**

Edit `commands/install-skillchain.sh` to add post-generation validation:

```bash
# After project generation completes
echo "Validating project completeness..."

python "$REPO_ROOT/evaluation/completeness_checker.py" \
  --project "$OUTPUT_DIR" \
  --blueprint "$BLUEPRINT_NAME" \
  --maturity "$MATURITY_LEVEL"

VALIDATION_EXIT_CODE=$?

if [ $VALIDATION_EXIT_CODE -eq 0 ]; then
  echo "✓ Project validation PASSED"
elif [ $VALIDATION_EXIT_CODE -eq 1 ]; then
  echo "⚠ Project validation NEEDS ATTENTION"
  echo "Run with --verbose to see details"
else
  echo "✗ Project validation ERROR"
fi
```

**Option 2: Separate validation command**

Create `commands/validate-project.md`:

```markdown
---
description: Validate generated project completeness
---

Validate a skillchain-generated project against its blueprint.

Usage: /validate-project <project-path> <blueprint-name> [maturity]

Example:
  /validate-project ./my-ml-pipeline ml-pipeline intermediate
```

With companion script `commands/validate-project.sh`:

```bash
#!/bin/bash

PROJECT_PATH="$1"
BLUEPRINT="$2"
MATURITY="${3:-intermediate}"

if [ -z "$PROJECT_PATH" ] || [ -z "$BLUEPRINT" ]; then
  echo "Usage: /validate-project <project-path> <blueprint-name> [maturity]"
  exit 1
fi

python "$(dirname "$0")/../evaluation/completeness_checker.py" \
  --project "$PROJECT_PATH" \
  --blueprint "$BLUEPRINT" \
  --maturity "$MATURITY" \
  --verbose
```

---

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/validate-generated-projects.yml`:

```yaml
name: Validate Generated Projects

on:
  push:
    paths:
      - 'commands/skillchain/**'
      - 'evaluation/**'
  pull_request:
    paths:
      - 'commands/skillchain/**'
      - 'evaluation/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        blueprint:
          - ml-pipeline
          - api-first
          - data-pipeline
          - ci-cd
          - k8s
        maturity:
          - starter
          - intermediate
          - advanced

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install pyyaml

      - name: Generate project
        run: |
          # Simulate skillchain generation
          # Replace with actual generation command
          ./scripts/generate_test_project.sh \
            --blueprint ${{ matrix.blueprint }} \
            --maturity ${{ matrix.maturity }} \
            --output ./test-project

      - name: Validate project completeness
        run: |
          python evaluation/completeness_checker.py \
            --project ./test-project \
            --blueprint ${{ matrix.blueprint }} \
            --maturity ${{ matrix.maturity }} \
            --verbose

      - name: Upload validation report
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: validation-report-${{ matrix.blueprint }}-${{ matrix.maturity }}
          path: ./test-project/
```

### GitLab CI

Create `.gitlab-ci.yml`:

```yaml
stages:
  - generate
  - validate

variables:
  BLUEPRINTS: "ml-pipeline api-first data-pipeline ci-cd k8s"
  MATURITY_LEVELS: "starter intermediate advanced"

.validate_template:
  stage: validate
  image: python:3.9
  before_script:
    - pip install pyyaml
  script:
    - |
      python evaluation/completeness_checker.py \
        --project ./test-project \
        --blueprint $BLUEPRINT \
        --maturity $MATURITY \
        --verbose
  artifacts:
    when: on_failure
    paths:
      - ./test-project/

validate:ml-pipeline:starter:
  extends: .validate_template
  variables:
    BLUEPRINT: ml-pipeline
    MATURITY: starter
  needs:
    - generate:ml-pipeline:starter

validate:ml-pipeline:intermediate:
  extends: .validate_template
  variables:
    BLUEPRINT: ml-pipeline
    MATURITY: intermediate
  needs:
    - generate:ml-pipeline:intermediate

# ... more validation jobs
```

### Jenkins Pipeline

Create `Jenkinsfile`:

```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'BLUEPRINT', choices: ['ml-pipeline', 'api-first', 'data-pipeline', 'ci-cd', 'k8s'], description: 'Blueprint to test')
        choice(name: 'MATURITY', choices: ['starter', 'intermediate', 'advanced'], description: 'Maturity level')
    }

    stages {
        stage('Setup') {
            steps {
                sh 'pip install pyyaml'
            }
        }

        stage('Generate Project') {
            steps {
                sh """
                    ./scripts/generate_test_project.sh \
                        --blueprint ${params.BLUEPRINT} \
                        --maturity ${params.MATURITY} \
                        --output ./test-project
                """
            }
        }

        stage('Validate Completeness') {
            steps {
                sh """
                    python evaluation/completeness_checker.py \
                        --project ./test-project \
                        --blueprint ${params.BLUEPRINT} \
                        --maturity ${params.MATURITY} \
                        --verbose
                """
            }
        }
    }

    post {
        failure {
            archiveArtifacts artifacts: 'test-project/**/*', allowEmptyArchive: true
        }
    }
}
```

---

## Pre-commit Hooks

### Local Development

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Pre-commit hook to validate project completeness

# Only run if blueprint files changed
BLUEPRINT_CHANGED=$(git diff --cached --name-only | grep -c "commands/skillchain/blueprints")

if [ $BLUEPRINT_CHANGED -eq 0 ]; then
  exit 0
fi

echo "Blueprint files changed, validating test projects..."

# Test each blueprint
for blueprint in ml-pipeline api-first data-pipeline; do
  echo "Testing $blueprint..."

  # Generate test project (mock)
  TEST_DIR="/tmp/test-$blueprint-$$"
  mkdir -p "$TEST_DIR"

  # Run validation
  python evaluation/completeness_checker.py \
    --project "$TEST_DIR" \
    --blueprint "$blueprint" \
    --maturity intermediate

  EXIT_CODE=$?

  # Cleanup
  rm -rf "$TEST_DIR"

  if [ $EXIT_CODE -ne 0 ]; then
    echo "Validation failed for $blueprint"
    exit 1
  fi
done

echo "All blueprints validated successfully"
exit 0
```

### Pre-commit Framework

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: validate-blueprints
        name: Validate Blueprint Completeness
        entry: python evaluation/completeness_checker.py
        language: python
        files: ^commands/skillchain/blueprints/.*\.md$
        pass_filenames: false
        additional_dependencies: ['pyyaml']
```

---

## Automated Testing

### Pytest Integration

Create `tests/test_completeness.py`:

```python
import pytest
import subprocess
import tempfile
import shutil
from pathlib import Path

BLUEPRINTS = ['ml-pipeline', 'api-first', 'data-pipeline', 'ci-cd', 'k8s']
MATURITY_LEVELS = ['starter', 'intermediate', 'advanced']

@pytest.fixture
def temp_project_dir():
    """Create temporary project directory"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.mark.parametrize('blueprint', BLUEPRINTS)
@pytest.mark.parametrize('maturity', MATURITY_LEVELS)
def test_blueprint_completeness(temp_project_dir, blueprint, maturity):
    """Test that generated projects meet completeness requirements"""

    # Generate project (mock or actual)
    # ... generation code ...

    # Run completeness checker
    result = subprocess.run(
        [
            'python',
            'evaluation/completeness_checker.py',
            '--project', str(temp_project_dir),
            '--blueprint', blueprint,
            '--maturity', maturity
        ],
        capture_output=True,
        text=True
    )

    # Check exit code
    assert result.returncode in [0, 1], f"Validation error: {result.stderr}"

    # Parse output for completeness percentage
    output = result.stdout
    completeness_match = re.search(r'Completeness: (\d+)%', output)
    assert completeness_match, "Could not find completeness percentage"

    completeness = int(completeness_match.group(1))

    # Assert minimum threshold
    assert completeness >= 80, f"Completeness {completeness}% below 80% threshold"

def test_basic_validation(temp_project_dir):
    """Test basic validation without blueprint"""

    # Create some files
    (temp_project_dir / 'README.md').write_text('# Test Project')
    (temp_project_dir / 'src').mkdir()
    (temp_project_dir / 'src' / 'main.py').write_text('print("hello")')

    # Run basic validation
    result = subprocess.run(
        [
            'python',
            'evaluation/completeness_checker.py',
            '--project', str(temp_project_dir)
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert 'README exists: Yes' in result.stdout
```

Run tests:
```bash
pytest tests/test_completeness.py -v
```

### Test Matrix Script

Create `scripts/test_all_blueprints.sh`:

```bash
#!/bin/bash
# Test all blueprint/maturity combinations

set -e

BLUEPRINTS=("ml-pipeline" "api-first" "data-pipeline" "ci-cd" "k8s")
MATURITY_LEVELS=("starter" "intermediate" "advanced")

PASSED=0
FAILED=0

for blueprint in "${BLUEPRINTS[@]}"; do
  for maturity in "${MATURITY_LEVELS[@]}"; do
    echo "Testing $blueprint @ $maturity..."

    TEST_DIR="/tmp/test-$blueprint-$maturity-$$"
    mkdir -p "$TEST_DIR"

    # Generate project (replace with actual generation)
    # ./generate_project.sh --blueprint "$blueprint" --maturity "$maturity" --output "$TEST_DIR"

    # Validate
    if python evaluation/completeness_checker.py \
       --project "$TEST_DIR" \
       --blueprint "$blueprint" \
       --maturity "$maturity"; then
      echo "✓ PASSED"
      ((PASSED++))
    else
      echo "✗ FAILED"
      ((FAILED++))
    fi

    rm -rf "$TEST_DIR"
    echo ""
  done
done

echo "Results: $PASSED passed, $FAILED failed"

if [ $FAILED -gt 0 ]; then
  exit 1
fi
```

---

## Advanced Usage

### Custom Exit Code Handling

```bash
#!/bin/bash
# Script with custom handling for different exit codes

python evaluation/completeness_checker.py \
  --project "$PROJECT" \
  --blueprint "$BLUEPRINT" \
  --maturity "$MATURITY"

EXIT_CODE=$?

case $EXIT_CODE in
  0)
    echo "✓ Validation passed (≥80% complete)"
    send_notification "success" "Project validation passed"
    ;;
  1)
    echo "⚠ Validation needs attention (<80% complete)"
    send_notification "warning" "Project needs attention"
    # Could still deploy to dev, but not prod
    ;;
  2)
    echo "✗ Validation error"
    send_notification "error" "Project validation failed"
    exit 1
    ;;
esac
```

### Parsing Output

```python
import subprocess
import re

def check_project_completeness(project_path, blueprint, maturity):
    """Check project completeness and return structured data"""

    result = subprocess.run(
        [
            'python',
            'evaluation/completeness_checker.py',
            '--project', project_path,
            '--blueprint', blueprint,
            '--maturity', maturity
        ],
        capture_output=True,
        text=True
    )

    output = result.stdout

    # Parse metrics
    completeness_match = re.search(r'Completeness: (\d+)%', output)
    required_match = re.search(r'Required: (\d+)', output)
    fulfilled_match = re.search(r'Fulfilled: (\d+)', output)
    missing_match = re.search(r'Missing: (\d+)', output)

    return {
        'exit_code': result.returncode,
        'completeness': int(completeness_match.group(1)) if completeness_match else 0,
        'required': int(required_match.group(1)) if required_match else 0,
        'fulfilled': int(fulfilled_match.group(1)) if fulfilled_match else 0,
        'missing': int(missing_match.group(1)) if missing_match else 0,
        'status': 'passed' if result.returncode == 0 else 'failed',
        'output': output
    }

# Usage
results = check_project_completeness('./my-project', 'ml-pipeline', 'intermediate')
print(f"Completeness: {results['completeness']}%")
```

### Slack Notifications

```bash
#!/bin/bash
# Send validation results to Slack

OUTPUT=$(python evaluation/completeness_checker.py \
  --project "$PROJECT" \
  --blueprint "$BLUEPRINT" \
  --maturity "$MATURITY" 2>&1)

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  COLOR="good"
  STATUS="PASSED"
elif [ $EXIT_CODE -eq 1 ]; then
  COLOR="warning"
  STATUS="NEEDS ATTENTION"
else
  COLOR="danger"
  STATUS="ERROR"
fi

curl -X POST "$SLACK_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d @- <<EOF
{
  "attachments": [
    {
      "color": "$COLOR",
      "title": "Project Validation: $STATUS",
      "fields": [
        {
          "title": "Project",
          "value": "$PROJECT",
          "short": true
        },
        {
          "title": "Blueprint",
          "value": "$BLUEPRINT",
          "short": true
        },
        {
          "title": "Maturity",
          "value": "$MATURITY",
          "short": true
        }
      ],
      "text": "\`\`\`$OUTPUT\`\`\`"
    }
  ]
}
EOF
```

---

## Best Practices

1. **Run Early and Often**
   - Validate immediately after generation
   - Re-validate after manual changes
   - Include in CI/CD pipeline

2. **Use Appropriate Maturity Levels**
   - Starter: Quick prototypes, learning
   - Intermediate: Production-ready projects
   - Advanced: Enterprise deployments

3. **Verbose Mode for Debugging**
   - Use `--verbose` when troubleshooting
   - Shows exactly which checks failed
   - Helpful for fixing deliverables

4. **Fail Fast**
   - Exit code 2 should stop pipelines immediately
   - Exit code 1 might allow dev deployments
   - Exit code 0 is safe for production

5. **Customize Thresholds**
   - Default 80% threshold works for most cases
   - Lower for prototypes, higher for critical systems
   - Modify `COMPLETENESS_THRESHOLD` in script

6. **Version Control Integration**
   - Track validation results over time
   - Notice trends in completeness
   - Correlate with quality metrics

---

## Troubleshooting

### Common Issues

**Blueprint not found:**
```bash
# Check blueprint path
ls ~/.claude/commands/skillchain/blueprints/

# Or use absolute path
python evaluation/completeness_checker.py \
  --project . \
  --blueprint /full/path/to/blueprint.md
```

**Import errors:**
```bash
# Install dependencies
pip install pyyaml
```

**Permissions errors:**
```bash
# Make script executable
chmod +x evaluation/completeness_checker.py

# Run with python explicitly
python evaluation/completeness_checker.py --help
```

**False positives/negatives:**
- Use `--verbose` to see details
- Check glob patterns in blueprint
- Verify content check regex patterns
- Test patterns manually with `grep`

---

## Future Enhancements

Planned features:
- JSON output format for machine parsing
- Custom threshold configuration via CLI
- Report generation (HTML, PDF, Markdown)
- Integration with GitHub Actions annotations
- Parallel file checking for large projects
- Auto-fix suggestions for common issues
- Historical tracking and trending
- Custom validators via plugins

See `evaluation/README.md` for updates.
