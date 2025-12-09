# Example Blueprint for Testing

This is a minimal example blueprint that demonstrates the YAML format expected by `completeness_checker.py`.

## Overview

This blueprint creates a simple Python project with testing and CI/CD.

## Deliverables Specification

```yaml
deliverables:
  # Core project structure
  project-structure:
    required_files:
      - "README.md"
      - "setup.py"
      - "requirements.txt"
      - "src/**/*.py"

  # Source code
  main-module:
    required_files:
      - "src/main.py"
      - "src/__init__.py"
    content_checks:
      "src/main.py":
        - "def main\\("
        - "if __name__ == ['\"]__main__['\"]:"

  # Testing
  test-suite:
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
        - "on:\\s+\\[?push"

  # Documentation (intermediate+)
  api-docs:
    required_files:
      - "docs/**/*.md"
      - "docs/api.md"

  # Docker (advanced)
  containerization:
    required_files:
      - "Dockerfile"
      - "docker-compose.yml"
    content_checks:
      "Dockerfile":
        - "FROM python:"
        - "COPY \\. \\."
      "docker-compose.yml":
        - "version:"
        - "services:"

  # Kubernetes (advanced only)
  kubernetes:
    required_files:
      - "k8s/**/*.yaml"
      - "k8s/deployment.yaml"
    content_checks:
      "k8s/deployment.yaml":
        - "kind:\\s+Deployment"
        - "apiVersion:\\s+apps/v1"

maturity_profiles:
  starter:
    deliverables:
      - project-structure
      - main-module
      - test-suite

  intermediate:
    deliverables:
      - project-structure
      - main-module
      - test-suite
      - github-actions
      - api-docs

  advanced:
    deliverables:
      - project-structure
      - main-module
      - test-suite
      - github-actions
      - api-docs
      - containerization
      - kubernetes
```

## Usage

Test this blueprint:

```bash
# Starter level (3 deliverables)
python evaluation/completeness_checker.py \
  --project /path/to/generated/project \
  --blueprint example \
  --maturity starter

# Intermediate level (5 deliverables)
python evaluation/completeness_checker.py \
  --project /path/to/generated/project \
  --blueprint example \
  --maturity intermediate

# Advanced level (7 deliverables)
python evaluation/completeness_checker.py \
  --project /path/to/generated/project \
  --blueprint example \
  --maturity advanced
```

## Expected Results

### Starter Maturity

Checks:
- ✓ project-structure (README, setup.py, requirements.txt, src/*.py)
- ✓ main-module (src/main.py with main function)
- ✓ test-suite (tests/*_test.py, pytest.ini)

Skips:
- ○ github-actions (not required)
- ○ api-docs (not required)
- ○ containerization (not required)
- ○ kubernetes (not required)

### Intermediate Maturity

Checks:
- ✓ project-structure
- ✓ main-module
- ✓ test-suite
- ✓ github-actions (CI/CD workflow)
- ✓ api-docs (documentation)

Skips:
- ○ containerization (not required)
- ○ kubernetes (not required)

### Advanced Maturity

Checks all 7 deliverables, no skips.

## Creating Test Projects

### Starter Project

```bash
mkdir -p test-project-starter/{src,tests,.github/workflows}

# Core files
echo "# Test Project" > test-project-starter/README.md
echo "from setuptools import setup" > test-project-starter/setup.py
echo "pytest" > test-project-starter/requirements.txt

# Source
cat > test-project-starter/src/__init__.py <<'EOF'
__version__ = "0.1.0"
EOF

cat > test-project-starter/src/main.py <<'EOF'
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
EOF

# Tests
cat > test-project-starter/tests/main_test.py <<'EOF'
from src.main import main

def test_main():
    assert True
EOF

cat > test-project-starter/pytest.ini <<'EOF'
[pytest]
testpaths = tests
EOF

# Validate
python evaluation/completeness_checker.py \
  --project test-project-starter \
  --blueprint example \
  --maturity starter
```

Expected output:
```
Completeness: 100%
Status: PASSED
```

### Intermediate Project

```bash
# Start with starter project
cp -r test-project-starter test-project-intermediate

# Add CI/CD
cat > test-project-intermediate/.github/workflows/ci.yml <<'EOF'
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest
EOF

# Add docs
mkdir -p test-project-intermediate/docs
cat > test-project-intermediate/docs/api.md <<'EOF'
# API Documentation

## main()

Main entry point.
EOF

# Validate
python evaluation/completeness_checker.py \
  --project test-project-intermediate \
  --blueprint example \
  --maturity intermediate
```

Expected output:
```
Completeness: 100%
Status: PASSED
```

### Advanced Project

```bash
# Start with intermediate project
cp -r test-project-intermediate test-project-advanced

# Add Docker
cat > test-project-advanced/Dockerfile <<'EOF'
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "src/main.py"]
EOF

cat > test-project-advanced/docker-compose.yml <<'EOF'
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
EOF

# Add Kubernetes
mkdir -p test-project-advanced/k8s
cat > test-project-advanced/k8s/deployment.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: test-app
  template:
    metadata:
      labels:
        app: test-app
    spec:
      containers:
      - name: app
        image: test-app:latest
EOF

# Validate
python evaluation/completeness_checker.py \
  --project test-project-advanced \
  --blueprint example \
  --maturity advanced
```

Expected output:
```
Completeness: 100%
Status: PASSED
```

## Key Patterns

### Glob Patterns

```yaml
# Exact file
required_files:
  - "README.md"

# Any file in directory
required_files:
  - "src/*.py"

# Recursive (any depth)
required_files:
  - "src/**/*.py"
  - "tests/**/*_test.py"

# Multiple extensions
required_files:
  - "config/**/*.{yml,yaml}"
```

### Content Checks

```yaml
# Simple string presence
content_checks:
  "src/main.py":
    - "import logging"

# Function definition
content_checks:
  "src/main.py":
    - "def main\\("

# Escaped special characters
content_checks:
  "setup.py":
    - "version\\s*=\\s*['\"]\\d+\\.\\d+\\.\\d+['\"]"

# Configuration keys
content_checks:
  "pytest.ini":
    - "\\[pytest\\]"
    - "testpaths\\s*="
```

### Progressive Maturity

Each level builds on the previous:

```yaml
maturity_profiles:
  starter:
    deliverables: [A, B, C]
  intermediate:
    deliverables: [A, B, C, D, E]  # Includes all starter
  advanced:
    deliverables: [A, B, C, D, E, F, G]  # Includes all intermediate
```

## Cleanup

```bash
# Remove test projects
rm -rf test-project-starter test-project-intermediate test-project-advanced
```

## References

- See `BLUEPRINT_SPEC.md` for full specification
- See `README.md` for completeness checker usage
- See `INTEGRATION.md` for CI/CD integration examples
