# Blueprint Deliverables Specification

Guide for creating blueprint deliverables that work with `completeness_checker.py`.

## Overview

Blueprints must include a YAML block with `deliverables` and optional `maturity_profiles` sections. The completeness checker parses this YAML to validate generated projects.

## YAML Structure

```yaml
deliverables:
  deliverable-key:
    required_files:
      - "path/to/file.ext"
      - "path/with/glob/**/*.ext"
    content_checks:
      "path/to/file.ext":
        - "regex pattern 1"
        - "regex pattern 2"

maturity_profiles:
  starter:
    deliverables:
      - deliverable-key-1
      - deliverable-key-2
  intermediate:
    deliverables:
      - deliverable-key-1
      - deliverable-key-2
      - deliverable-key-3
  advanced:
    deliverables:
      - deliverable-key-1
      - deliverable-key-2
      - deliverable-key-3
      - deliverable-key-4
```

## Field Specifications

### `deliverables`

Map of deliverable keys to specifications. Each deliverable can have:

#### `required_files` (array of strings)

List of file paths or glob patterns that must exist in the generated project.

**Glob Support:**
- `*` - Matches any characters except path separator
- `**` - Matches any characters including path separators (recursive)
- `?` - Matches single character
- `[abc]` - Matches character set

**Examples:**
```yaml
required_files:
  # Exact file
  - "README.md"
  - "src/main.py"

  # Files in directory
  - "tests/*.py"

  # Recursive matching
  - "src/**/*.ts"
  - "config/**/*.yml"

  # Multiple patterns
  - "docker-compose*.yml"
  - "monitoring/grafana/dashboards/*.json"
```

**Validation:**
- At least ONE file must match each pattern
- If ANY pattern has zero matches, deliverable is marked MISSING

#### `content_checks` (map of file paths to pattern arrays)

Map of specific file paths to regex patterns that must be found in those files.

**Pattern Syntax:**
- Standard Python regex (`re` module)
- Case-sensitive by default
- Must match somewhere in file content

**Examples:**
```yaml
content_checks:
  # Single pattern
  "src/main.py":
    - "import logging"

  # Multiple patterns (all must match)
  "scripts/train.py":
    - "import mlflow"
    - "mlflow\\.start_run"
    - "def train_model"

  # Complex patterns
  "docker-compose.yml":
    - "services:"
    - "prometheus:"
    - "grafana:"

  # Configuration validation
  ".github/workflows/ci.yml":
    - "name:\\s+CI"
    - "on:\\s+\\[push,\\s*pull_request\\]"
```

**Validation:**
- File must exist (checked first)
- ALL patterns must be found in file
- If ANY pattern missing, deliverable is marked INCOMPLETE

### `maturity_profiles`

Map of maturity levels to required deliverables for that level.

**Levels:**
- `starter` - Minimal viable project
- `intermediate` - Production-ready with standard practices
- `advanced` - Full production setup with all bells and whistles

**Structure:**
```yaml
maturity_profiles:
  starter:
    deliverables:
      - basic-setup
      - core-functionality
  intermediate:
    deliverables:
      - basic-setup
      - core-functionality
      - testing
      - ci-cd
  advanced:
    deliverables:
      - basic-setup
      - core-functionality
      - testing
      - ci-cd
      - monitoring
      - kubernetes
```

**Behavior:**
- If maturity profile specified, only listed deliverables are checked
- Unlisted deliverables shown as "skipped"
- If no maturity profiles defined, all deliverables checked regardless of maturity level

## Complete Example: ML Pipeline Blueprint

```yaml
deliverables:
  # Core tracking
  mlflow-tracking:
    required_files:
      - "mlflow/mlflow.yml"
      - "scripts/train.py"
    content_checks:
      "scripts/train.py":
        - "import mlflow"
        - "mlflow\\.start_run"
      "mlflow/mlflow.yml":
        - "backend_store_uri:"

  # Training pipeline
  training-pipeline:
    required_files:
      - "src/training/**/*.py"
      - "src/data/**/*.py"
    content_checks:
      "src/training/train.py":
        - "def train_model"
        - "def evaluate_model"

  # Testing
  unit-tests:
    required_files:
      - "tests/**/*_test.py"
      - "pytest.ini"
    content_checks:
      "pytest.ini":
        - "\\[pytest\\]"

  # CI/CD
  github-actions:
    required_files:
      - ".github/workflows/ci.yml"
    content_checks:
      ".github/workflows/ci.yml":
        - "name:\\s+CI"
        - "pytest"

  # Monitoring
  grafana-dashboards:
    required_files:
      - "monitoring/grafana/dashboards/*.json"
      - "monitoring/prometheus/prometheus.yml"

  # Feature store (advanced)
  feature-store:
    required_files:
      - "src/features/**/*.py"
      - "feature_store.yml"
    content_checks:
      "feature_store.yml":
        - "registry:"

  # Kubernetes deployment (advanced)
  kubernetes-deployment:
    required_files:
      - "k8s/**/*.yaml"
      - "k8s/training-job.yaml"
    content_checks:
      "k8s/training-job.yaml":
        - "kind:\\s+Job"

maturity_profiles:
  starter:
    deliverables:
      - mlflow-tracking
      - training-pipeline

  intermediate:
    deliverables:
      - mlflow-tracking
      - training-pipeline
      - unit-tests
      - github-actions
      - grafana-dashboards

  advanced:
    deliverables:
      - mlflow-tracking
      - training-pipeline
      - unit-tests
      - github-actions
      - grafana-dashboards
      - feature-store
      - kubernetes-deployment
```

## Complete Example: API-First Blueprint

```yaml
deliverables:
  # Core API
  api-implementation:
    required_files:
      - "src/**/*.ts"
      - "openapi.yml"
    content_checks:
      "src/app.ts":
        - "import express"
        - "app\\.listen"

  # OpenAPI spec
  openapi-spec:
    required_files:
      - "openapi.yml"
    content_checks:
      "openapi.yml":
        - "openapi:\\s+['\"]?3\\."
        - "paths:"
        - "components:"

  # Testing
  api-tests:
    required_files:
      - "tests/**/*.test.ts"
    content_checks:
      "tests/api.test.ts":
        - "describe\\("
        - "supertest"

  # Documentation
  api-docs:
    required_files:
      - "README.md"
      - "docs/**/*.md"

  # Docker
  containerization:
    required_files:
      - "Dockerfile"
      - "docker-compose.yml"

  # CI/CD
  ci-cd:
    required_files:
      - ".github/workflows/*.yml"

  # Database migrations (intermediate)
  database-migrations:
    required_files:
      - "migrations/**/*.sql"
      - "knexfile.js"

  # API gateway (advanced)
  api-gateway:
    required_files:
      - "kong.yml"

maturity_profiles:
  starter:
    deliverables:
      - api-implementation
      - openapi-spec
      - api-docs

  intermediate:
    deliverables:
      - api-implementation
      - openapi-spec
      - api-tests
      - api-docs
      - containerization
      - ci-cd
      - database-migrations

  advanced:
    deliverables:
      - api-implementation
      - openapi-spec
      - api-tests
      - api-docs
      - containerization
      - ci-cd
      - database-migrations
      - api-gateway
```

## Best Practices

### File Patterns

**Be Specific:**
```yaml
# Good - clear intent
required_files:
  - "src/training/train.py"
  - "src/training/evaluate.py"

# Too vague - could match anything
required_files:
  - "**/*.py"
```

**Use Appropriate Wildcards:**
```yaml
# Good - checks for any dashboard
required_files:
  - "monitoring/grafana/dashboards/*.json"

# Good - checks for nested structure
required_files:
  - "src/features/**/*.py"

# Too broad - matches too much
required_files:
  - "**/*"
```

### Content Checks

**Escape Special Regex Characters:**
```yaml
# Correct - dots escaped
content_checks:
  "src/main.py":
    - "mlflow\\.start_run"
    - "config\\.load"

# Wrong - dot matches any character
content_checks:
  "src/main.py":
    - "mlflow.start_run"  # Will match "mlflowXstart_run"
```

**Check Key Functionality:**
```yaml
# Good - validates actual implementation
content_checks:
  "src/training/train.py":
    - "def train_model"
    - "model\\.fit"
    - "mlflow\\.log_metric"

# Too shallow - just checks imports
content_checks:
  "src/training/train.py":
    - "import"
```

**Avoid Overly Specific Patterns:**
```yaml
# Good - checks for presence
content_checks:
  "README.md":
    - "Installation"
    - "Usage"

# Too specific - breaks easily
content_checks:
  "README.md":
    - "## Installation\\n\\nRun the following:"
```

### Maturity Levels

**Progressive Complexity:**
```yaml
maturity_profiles:
  # Starter: Just get it working
  starter:
    deliverables:
      - basic-setup
      - core-functionality

  # Intermediate: Production-ready
  intermediate:
    deliverables:
      - basic-setup
      - core-functionality
      - testing
      - ci-cd
      - monitoring

  # Advanced: Full enterprise setup
  advanced:
    deliverables:
      - basic-setup
      - core-functionality
      - testing
      - ci-cd
      - monitoring
      - kubernetes
      - observability-stack
      - disaster-recovery
```

**Cumulative Requirements:**
- Each level should include all previous levels
- Starter ⊆ Intermediate ⊆ Advanced
- Don't remove requirements at higher levels

## Embedding in Markdown

The YAML must be in a fenced code block marked as `yaml`:

````markdown
## Deliverables Specification

The following deliverables are generated by this blueprint:

```yaml
deliverables:
  api-implementation:
    required_files:
      - "src/**/*.ts"
```
````

**Parser Behavior:**
- Extracts first ````yaml ... ```` block
- Ignores all other content
- Fails if no YAML block found
- Fails if YAML is invalid

## Validation Tips

**Test Your Patterns:**
```bash
# Dry-run validation
python evaluation/completeness_checker.py \
  --project ./test-project \
  --blueprint your-blueprint \
  --verbose
```

**Common Issues:**

1. **Glob doesn't match:**
   - Check path separators (use `/` not `\`)
   - Verify paths are relative to project root
   - Test with `ls -la` to see actual files

2. **Content check fails:**
   - Escape regex special characters
   - Use `--verbose` to see which patterns failed
   - Check file encoding (script uses UTF-8)

3. **Skipped unexpectedly:**
   - Verify maturity profile includes the deliverable
   - Check spelling of deliverable keys
   - Ensure profiles are properly indented

## Future Extensions

Potential additions to spec format:

```yaml
deliverables:
  example:
    # Existing
    required_files: [...]
    content_checks: {...}

    # Proposed
    optional_files: [...]  # Nice-to-have, not required
    file_count:
      min: 5  # At least 5 files
      max: 20  # No more than 20 files
    size_checks:
      "data/model.pkl":
        min: 1048576  # At least 1MB
        max: 104857600  # No more than 100MB
    command_checks:  # Run command to validate
      - "pytest tests/"
      - "npm run lint"
```

## Resources

- **Regex Reference:** https://docs.python.org/3/library/re.html
- **Glob Patterns:** https://docs.python.org/3/library/glob.html
- **YAML Spec:** https://yaml.org/spec/1.2/spec.html
- **Blueprint Examples:** See `commands/skillchain/blueprints/*.md`
