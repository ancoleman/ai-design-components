---
sidebar_position: 7
title: Chain Context & Validation
description: Understanding skillchain state tracking, validation flow, and deliverables verification
---

# Chain Context & Validation

The chain context system provides state tracking and validation throughout skillchain execution, enabling deliverables verification and remediation when outputs are incomplete.

## Architecture Overview

```
                              SKILLCHAIN EXECUTION FLOW
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   /skillchain "build ML pipeline, starter"                              │
    │            │                                                            │
    │            ▼                                                            │
    │   ┌─────────────────┐         ┌──────────────────────────────────┐     │
    │   │   start.md      │         │         chain_context            │     │
    │   │   (Router)      │───────▶ │  ┌─────────────────────────────┐ │     │
    │   │                 │         │  │ blueprint: "ml-pipeline"    │ │     │
    │   │ • Parse goal    │         │  │ original_goal: "build ML.." │ │     │
    │   │ • Match skills  │         │  │ detected_domains: [ai-ml]   │ │     │
    │   │ • Find blueprint│         │  │ matched_skills: [...]       │ │     │
    │   └────────┬────────┘         │  └─────────────────────────────┘ │     │
    │            │                  └──────────────────────────────────┘     │
    │            ▼                                                            │
    │   ┌─────────────────┐         ┌──────────────────────────────────┐     │
    │   │ ai-ml.md        │         │         chain_context            │     │
    │   │ (Orchestrator)  │───────▶ │  ┌─────────────────────────────┐ │     │
    │   │                 │         │  │ maturity: "starter"         │ │     │
    │   │ • Ask maturity  │         │  │ project_path: "/path/to/..."│ │     │
    │   │ • Configure     │         │  │ skills_sequence: [...]      │ │     │
    │   │ • Execute skills│         │  │ skill_outputs: {...}        │ │     │
    │   └────────┬────────┘         │  │ deliverables_status: {...}  │ │     │
    │            │                  │  └─────────────────────────────┘ │     │
    │            ▼                  └──────────────────────────────────┘     │
    │   ┌─────────────────┐                                                   │
    │   │ Step 5.5:       │         ┌──────────────────────────────────┐     │
    │   │ VALIDATION      │───────▶ │      COMPLETION REPORT           │     │
    │   │                 │         │  ✓ MLflow tracking               │     │
    │   │ • Load blueprint│         │  ✓ Training pipeline             │     │
    │   │ • Check files   │         │  ○ Feature store (skipped)       │     │
    │   │ • Run patterns  │         │  ✗ Sample data - MISSING         │     │
    │   │ • Remediate     │         │                                  │     │
    │   └─────────────────┘         │  Completeness: 75%               │     │
    │                               └──────────────────────────────────┘     │
    └─────────────────────────────────────────────────────────────────────────┘
```

## Chain Context Schema

The `chain_context` object tracks state throughout skillchain execution. It's defined in `skillchain-data/shared/chain-context-schema.yaml`.

### Router Metadata (Set by start.md)

| Field | Type | Description |
|-------|------|-------------|
| `blueprint` | string \| null | Matched blueprint name (e.g., "ml-pipeline") |
| `original_goal` | string | User's original request |
| `detected_domains` | list[object] | Domains with confidence scores |
| `matched_skills` | list[object] | Skills matched by router |

### Orchestrator Configuration

| Field | Type | Description |
|-------|------|-------------|
| `maturity` | enum | starter \| intermediate \| advanced |
| `project_path` | string | Absolute path to generated project |
| `skills_sequence` | list[object] | Ordered skills with status tracking |

### Execution Tracking

```yaml
skill_outputs:
  "implementing-mlops":
    status: "completed"
    files_created:
      - "src/models/train.py"
      - "pipelines/training_pipeline.py"
    directories_created:
      - "src/models"
    deliverables_contributed:
      - "MLflow experiment tracking"
```

### Deliverables Validation

```yaml
deliverables_status:
  "MLflow experiment tracking":
    status: "fulfilled"
    required_for_maturity: ["starter", "intermediate", "advanced"]
    primary_skill: "implementing-mlops"
    validation_results:
      files_exist: true
      content_checks_passed: true
  "Feature store":
    status: "skipped"
    required_for_maturity: ["intermediate", "advanced"]
```

## Validation Flow

### Step 5.5: Post-Skill Validation

After all skills complete, orchestrators run validation:

```
┌─────────────────────────────────────────────────────────────┐
│                    VALIDATION PIPELINE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Load Blueprint Deliverables                              │
│     ┌─────────────────┐                                      │
│     │ ml-pipeline.md  │────▶ Parse ## Deliverables section   │
│     └─────────────────┘                                      │
│                                                              │
│  2. Apply Maturity Filters                                   │
│     starter ──────▶ Skip: Feature store, K8s, Advanced CI    │
│     intermediate ──▶ Skip: K8s only                          │
│     advanced ─────▶ All deliverables required                │
│                                                              │
│  3. Validate Each Deliverable                                │
│     ┌─────────────────────────────────────────────┐          │
│     │ For each required deliverable:              │          │
│     │   • Check required_files exist              │          │
│     │   • Run content_checks (regex patterns)     │          │
│     │   • Mark status: fulfilled/missing/skipped  │          │
│     └─────────────────────────────────────────────┘          │
│                                                              │
│  4. Calculate Completeness                                   │
│     fulfilled / total_required × 100 = completeness%         │
│                                                              │
│  5. Generate Report & Offer Remediation                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Validation Functions

The validation logic in `skillchain-data/shared/validation.md` provides:

| Function | Purpose |
|----------|---------|
| `validate_deliverable()` | Validate single deliverable against specs |
| `check_files_exist()` | Check file/directory existence with glob support |
| `run_content_checks()` | Run regex pattern checks against files |
| `validate_chain()` | Complete chain validation |
| `run_basic_completeness_check()` | Fallback when no blueprint |

## Blueprint Deliverables Specification

Blueprints define expected outputs using YAML embedded in markdown:

```yaml
deliverables:
  "MLflow experiment tracking":
    primary_skill: implementing-mlops
    required_files:
      - src/models/train.py
    content_checks:
      - pattern: "import mlflow"
        in: src/models/train.py
    maturity_required:
      - starter
      - intermediate
      - advanced

  "Kubernetes Manifests":
    primary_skill: operating-kubernetes
    required_files:
      - infrastructure/kubernetes/deployment.yaml
      - infrastructure/kubernetes/service.yaml
    maturity_required:
      - intermediate
      - advanced

maturity_profiles:
  starter:
    description: "Basic setup for getting started"
    skip_deliverables:
      - "Kubernetes Manifests"
      - "Feature Store"
    require_additionally:
      - "Sample Data Script"

  intermediate:
    description: "Production-ready configuration"

  advanced:
    description: "Enterprise features and observability"
```

## Per-Skill Output Declarations

Each skill declares expected outputs in `outputs.yaml`:

```yaml
skill: implementing-mlops
version: "1.0"

base_outputs:
  - path: "src/models/train.py"
    reason: "Main training script with MLflow integration"
    must_contain:
      - "import mlflow"
      - "mlflow.start_run"

  - path: "pipelines/training_pipeline.py"
    reason: "Orchestrated training pipeline"

conditional_outputs:
  maturity:
    intermediate:
      - path: "src/models/hyperparameter_tuning.py"
        reason: "HPO with Optuna integration"
    advanced:
      - path: "monitoring/model_metrics.py"
        reason: "Model performance monitoring"
```

### outputs.yaml Validation Rules

| Field | Required | Description |
|-------|----------|-------------|
| `skill` | Yes | Must match directory name |
| `version` | Yes | Semantic version string |
| `base_outputs` | Yes* | Files always created (*at least one of base/conditional) |
| `conditional_outputs` | Yes* | Maturity/context-dependent outputs |
| `path` | Yes | Relative path from project root |
| `reason` | No | Human-readable explanation |
| `must_contain` | No | Content patterns to verify |

## Remediation Flow

When validation finds missing deliverables:

```
┌────────────────────────────────────────────────────────────┐
│ SKILLCHAIN COMPLETION REPORT                                │
│                                                             │
│ Blueprint: ml-pipeline                                      │
│ Maturity: starter                                           │
│ Project: ~/projects/my-ml-pipeline                          │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ DELIVERABLES:                                               │
│                                                             │
│ ✓ MLflow experiment tracking                                │
│ ✓ Training pipeline                                         │
│ ✓ Model serving API                                         │
│ ○ Feature store (skipped - starter)                         │
│ ✗ Sample data script - MISSING                              │
│   └─ Expected: scripts/generate_sample_data.py              │
│   └─ Primary skill: ai-data-engineering                     │
│                                                             │
├────────────────────────────────────────────────────────────┤
│ Completeness: 75%                                           │
│ Status: NEEDS ATTENTION                                     │
│                                                             │
│ Would you like me to:                                       │
│ A) Generate the missing components                          │
│ B) Generate specific components                             │
│ C) Continue without them                                    │
│ D) See detailed validation report                           │
└────────────────────────────────────────────────────────────┘
```

## CI/CD Integration

### Skills Validation (Pre-Generation)

Validates skill definitions, not generated outputs:

```bash
cd scripts
python -m validation ci --completed --format=junit -o results.xml
```

### Blueprint Validation (Pre-Generation)

Validates blueprint deliverables specifications:

```bash
python -m validation blueprints --verbose
```

### Project Validation (Post-Generation)

Validates actual generated project against blueprint:

```bash
python scripts/runtime/completeness_checker.py \
  ./my-generated-project \
  --blueprint ml-pipeline \
  --maturity starter
```

## GitHub Actions Workflow

```yaml
name: Validate Skillchain

on: [push, pull_request]

jobs:
  validate-registries:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install pyyaml
      - run: python3 scripts/validation/validate_registries.py

  validate-blueprints:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install pyyaml
      - run: python -m scripts.validation blueprints --verbose

  run-evaluation:
    runs-on: ubuntu-latest
    needs: [validate-registries, validate-blueprints]
    steps:
      - uses: actions/checkout@v4
      - run: python3 evaluation/evaluate.py --report
```

## Related Documentation

- [Skill Validation](/docs/guides/skill-validation) - Validation package CLI and API
- [Blueprints](/docs/skillchain/blueprints) - Blueprint authoring guide
- [Architecture](/docs/skillchain/architecture) - Overall skillchain architecture
- [Best Practices](/docs/guides/best-practices) - Skill authoring guidelines
