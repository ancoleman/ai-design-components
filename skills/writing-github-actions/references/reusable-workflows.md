# Reusable Workflows Guide

Advanced patterns and best practices for creating and using reusable workflows in GitHub Actions.

## Table of Contents

1. [Overview](#overview)
2. [Creating Reusable Workflows](#creating-reusable-workflows)
3. [Calling Reusable Workflows](#calling-reusable-workflows)
4. [Passing Data](#passing-data)
5. [Matrix Strategies with Reusable Workflows](#matrix-strategies-with-reusable-workflows)
6. [Nested Reusable Workflows](#nested-reusable-workflows)
7. [Best Practices](#best-practices)
8. [Common Patterns](#common-patterns)

---

## Overview

Reusable workflows enable job-level reuse across repositories and workflows. They standardize CI/CD processes and reduce duplication.

**Key Benefits:**
- Centralize CI/CD logic in single location
- Standardize workflows across organization
- Version workflows independently
- Reduce maintenance burden

**When to Use:**
- Standardizing build/test/deploy jobs
- Enforcing organization policies
- Sharing workflows across repositories
- Complex multi-step jobs with configuration

**Limitations:**
- Maximum 10 levels of nesting
- Maximum 50 workflow calls per run
- Cannot call reusable workflows from same repository in different directory
- Secrets must be explicitly passed or inherited

---

## Creating Reusable Workflows

### Basic Structure

File: `.github/workflows/reusable-build.yml`

```yaml
name: Reusable Build

on:
  workflow_call:
    inputs:
      # Define inputs here
    secrets:
      # Define secrets here
    outputs:
      # Define outputs here

jobs:
  # Job definitions
```

### With Inputs

```yaml
name: Reusable Build

on:
  workflow_call:
    inputs:
      node-version:
        description: 'Node.js version to use'
        required: false
        type: string
        default: '20'
      build-command:
        description: 'Build command to run'
        required: false
        type: string
        default: 'npm run build'
      working-directory:
        description: 'Working directory'
        required: false
        type: string
        default: '.'

jobs:
  build:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ${{ inputs.working-directory }}
    steps:
      - uses: actions/checkout@v5

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: 'npm'

      - run: npm ci

      - run: ${{ inputs.build-command }}
```

**Input Types:**
- `string` - Text value
- `number` - Numeric value
- `boolean` - true/false
- `choice` - Predefined options (not available in workflow_call)

### With Secrets

```yaml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      api-key:
        required: true
      npm-token:
        required: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: actions/checkout@v5

      - name: Deploy
        env:
          API_KEY: ${{ secrets.api-key }}
          NPM_TOKEN: ${{ secrets.npm-token }}
        run: ./deploy.sh
```

### With Outputs

```yaml
name: Reusable Build with Outputs

on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '20'
    outputs:
      artifact-name:
        description: "Name of the uploaded artifact"
        value: ${{ jobs.build.outputs.artifact }}
      version:
        description: "Version number"
        value: ${{ jobs.build.outputs.version }}

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      artifact: ${{ steps.upload.outputs.artifact-name }}
      version: ${{ steps.version.outputs.version }}
    steps:
      - uses: actions/checkout@v5

      - id: version
        run: echo "version=$(cat VERSION)" >> $GITHUB_OUTPUT

      - run: npm run build

      - id: upload
        uses: actions/upload-artifact@v4
        with:
          name: build-${{ steps.version.outputs.version }}
          path: dist/
```

---

## Calling Reusable Workflows

### Same Repository

```yaml
name: CI

on: [push]

jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      node-version: '20'
      build-command: 'npm run build:prod'
```

**Path Requirements:**
- Must start with `./`
- Must reference `.github/workflows/` directory
- Use relative path from repository root

### Different Repository (Same Organization)

```yaml
name: CI

on: [push]

jobs:
  build:
    uses: my-org/shared-workflows/.github/workflows/reusable-build.yml@v1
    with:
      node-version: '20'
    secrets: inherit
```

**Reference Format:** `{owner}/{repo}/{path}@{ref}`

**Refs:**
- Tag: `@v1`, `@v1.2.3`
- Branch: `@main`, `@develop`
- Commit SHA: `@abc123...` (most secure)

### Different Repository (Public)

```yaml
jobs:
  build:
    uses: other-org/public-workflows/.github/workflows/build.yml@v1
    with:
      node-version: '20'
    secrets:
      npm-token: ${{ secrets.NPM_TOKEN }}
```

**Note:** Cannot use `secrets: inherit` for external organizations

---

## Passing Data

### Passing Inputs

```yaml
jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      node-version: '20'
      build-command: 'npm run build'
      enable-tests: true
```

### Passing Secrets (Explicit)

```yaml
jobs:
  deploy:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: production
    secrets:
      api-key: ${{ secrets.PROD_API_KEY }}
      npm-token: ${{ secrets.NPM_TOKEN }}
```

### Passing All Secrets (Inherit)

```yaml
jobs:
  deploy:
    uses: my-org/workflows/.github/workflows/deploy.yml@v1
    with:
      environment: production
    secrets: inherit
```

**Requirements for `secrets: inherit`:**
- Same organization or enterprise
- Caller workflow has access to secrets

### Using Outputs from Reusable Workflows

```yaml
jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      node-version: '20'

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Artifact: ${{ needs.build.outputs.artifact-name }}"
      - run: echo "Version: ${{ needs.build.outputs.version }}"

      - uses: actions/download-artifact@v5
        with:
          name: ${{ needs.build.outputs.artifact-name }}
```

---

## Matrix Strategies with Reusable Workflows

### Matrix in Caller Workflow

```yaml
jobs:
  multi-platform-build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [18, 20, 22]
    uses: ./.github/workflows/build.yml
    with:
      os: ${{ matrix.os }}
      node-version: ${{ matrix.node }}
```

**Reusable Workflow:**

```yaml
on:
  workflow_call:
    inputs:
      os:
        required: true
        type: string
      node-version:
        required: true
        type: string

jobs:
  build:
    runs-on: ${{ inputs.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm run build
```

### Matrix in Reusable Workflow

```yaml
# Reusable workflow with internal matrix
on:
  workflow_call:
    inputs:
      environments:
        required: true
        type: string  # JSON array

jobs:
  deploy:
    strategy:
      matrix:
        environment: ${{ fromJSON(inputs.environments) }}
    runs-on: ubuntu-latest
    environment: ${{ matrix.environment }}
    steps:
      - run: ./deploy.sh ${{ matrix.environment }}
```

**Calling:**

```yaml
jobs:
  multi-env-deploy:
    uses: ./.github/workflows/deploy.yml
    with:
      environments: '["dev", "staging", "production"]'
```

---

## Nested Reusable Workflows

### Two-Level Nesting

**Level 1: Base Workflow**

File: `.github/workflows/base-build.yml`

```yaml
name: Base Build

on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '20'
    outputs:
      artifact-name:
        value: ${{ jobs.build.outputs.artifact }}

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      artifact: build-output
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci && npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/
```

**Level 2: Extended Workflow**

File: `.github/workflows/build-and-test.yml`

```yaml
name: Build and Test

on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '20'

jobs:
  build:
    uses: ./.github/workflows/base-build.yml
    with:
      node-version: ${{ inputs.node-version }}

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v5
        with:
          name: ${{ needs.build.outputs.artifact-name }}
      - run: npm test
```

**Level 3: Main Workflow**

```yaml
name: CI

on: [push]

jobs:
  ci:
    uses: ./.github/workflows/build-and-test.yml
    with:
      node-version: '20'
```

### Limits

- Maximum nesting: 10 levels
- Maximum workflow calls: 50 per run
- Each level counts toward limits

---

## Best Practices

### 1. Version Reusable Workflows

**Use Semantic Versioning:**

```yaml
# Pin to major version (recommended)
uses: my-org/workflows/.github/workflows/build.yml@v1

# Pin to specific version (most stable)
uses: my-org/workflows/.github/workflows/build.yml@v1.2.3

# Pin to commit SHA (most secure)
uses: my-org/workflows/.github/workflows/build.yml@abc123...
```

**Create Tags:**

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Update major version tag
git tag -fa v1 -m "Update v1 to v1.0.0"
git push origin v1 --force
```

### 2. Document Inputs and Outputs

```yaml
on:
  workflow_call:
    inputs:
      node-version:
        description: |
          Node.js version to use for build.
          Supports: 18, 20, 22
          Default: 20
        required: false
        type: string
        default: '20'
    outputs:
      artifact-name:
        description: |
          Name of the uploaded build artifact.
          Use with actions/download-artifact to retrieve.
        value: ${{ jobs.build.outputs.artifact }}
```

### 3. Provide Sensible Defaults

```yaml
inputs:
  node-version:
    type: string
    default: '20'
  build-command:
    type: string
    default: 'npm run build'
  test-command:
    type: string
    default: 'npm test'
  working-directory:
    type: string
    default: '.'
```

### 4. Use Permissions Explicitly

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps: [...]
```

### 5. Handle Errors Gracefully

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Build
        run: npm run build
        continue-on-error: ${{ inputs.allow-build-failure || false }}

      - if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: build-logs
          path: logs/
```

### 6. Use Concurrency Controls

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    concurrency:
      group: deploy-${{ inputs.environment }}
      cancel-in-progress: false
    steps: [...]
```

---

## Common Patterns

### Pattern 1: Standardized Build

```yaml
name: Standard Node.js Build

on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '20'
      package-manager:
        type: string
        default: 'npm'
    outputs:
      artifact-name:
        value: ${{ jobs.build.outputs.artifact }}

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      artifact: build-${{ github.sha }}
    steps:
      - uses: actions/checkout@v5

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: ${{ inputs.package-manager }}

      - name: Install dependencies
        run: |
          if [ "${{ inputs.package-manager }}" = "npm" ]; then
            npm ci
          elif [ "${{ inputs.package-manager }}" = "yarn" ]; then
            yarn install --frozen-lockfile
          elif [ "${{ inputs.package-manager }}" = "pnpm" ]; then
            pnpm install --frozen-lockfile
          fi

      - run: ${{ inputs.package-manager }} run build

      - uses: actions/upload-artifact@v4
        with:
          name: build-${{ github.sha }}
          path: dist/
```

### Pattern 2: Multi-Environment Deploy

```yaml
name: Deploy to Environment

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      version:
        required: true
        type: string
    secrets:
      aws-access-key-id:
        required: true
      aws-secret-access-key:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: ${{ inputs.environment }}
      url: https://${{ inputs.environment }}.example.com
    concurrency:
      group: deploy-${{ inputs.environment }}
      cancel-in-progress: false
    steps:
      - uses: actions/checkout@v5

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.aws-access-key-id }}
          aws-secret-access-key: ${{ secrets.aws-secret-access-key }}
          aws-region: us-east-1

      - name: Deploy
        run: |
          echo "Deploying version ${{ inputs.version }} to ${{ inputs.environment }}"
          ./deploy.sh
```

### Pattern 3: Test Matrix

```yaml
name: Test Matrix

on:
  workflow_call:
    inputs:
      node-versions:
        type: string
        default: '["18", "20", "22"]'
      os-list:
        type: string
        default: '["ubuntu-latest"]'

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: ${{ fromJSON(inputs.os-list) }}
        node: ${{ fromJSON(inputs.node-versions) }}
    steps:
      - uses: actions/checkout@v5

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'

      - run: npm ci
      - run: npm test

      - if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results-${{ matrix.os }}-${{ matrix.node }}
          path: test-results/
```

### Pattern 4: Conditional Jobs

```yaml
name: CI with Optional Deploy

on:
  workflow_call:
    inputs:
      run-tests:
        type: boolean
        default: true
      run-lint:
        type: boolean
        default: true
      deploy:
        type: boolean
        default: false
      environment:
        type: string
        default: 'dev'

jobs:
  lint:
    if: inputs.run-lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: npm run lint

  test:
    if: inputs.run-tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: npm test

  deploy:
    if: inputs.deploy
    needs: [lint, test]
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - run: ./deploy.sh
```

### Pattern 5: Composite Build and Release

```yaml
name: Build and Release

on:
  workflow_call:
    inputs:
      create-release:
        type: boolean
        default: false
      version:
        type: string
        required: true
    secrets:
      github-token:
        required: true

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      artifact-name: build-${{ inputs.version }}
    steps:
      - uses: actions/checkout@v5
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build-${{ inputs.version }}
          path: dist/

  release:
    if: inputs.create-release
    needs: build
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/download-artifact@v5
        with:
          name: ${{ needs.build.outputs.artifact-name }}

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          tag_name: v${{ inputs.version }}
          files: dist/*
        env:
          GITHUB_TOKEN: ${{ secrets.github-token }}
```

---

## Troubleshooting

### Common Issues

**1. Secrets Not Available**

**Problem:** Reusable workflow cannot access secrets

**Solution:**
```yaml
# Caller must pass secrets explicitly or use inherit
jobs:
  deploy:
    uses: ./.github/workflows/deploy.yml
    secrets: inherit  # Or pass explicitly
```

**2. Cannot Reference Local Reusable Workflow**

**Problem:** `uses: ./.github/workflows/build.yml` not found

**Solution:**
- Ensure workflow file exists in `.github/workflows/` directory
- Use `./` prefix for same repository
- Check file path is relative to repository root

**3. Matrix Evaluation Errors**

**Problem:** Matrix values from inputs not working

**Solution:**
```yaml
# Pass as JSON string
strategy:
  matrix:
    version: ${{ fromJSON(inputs.versions) }}

# Caller provides JSON array
with:
  versions: '["18", "20", "22"]'
```

**4. Outputs Not Available**

**Problem:** Cannot access outputs from reusable workflow

**Solution:**
```yaml
# Reusable workflow must define outputs
on:
  workflow_call:
    outputs:
      result:
        value: ${{ jobs.build.outputs.result }}

# Job must export outputs
jobs:
  build:
    outputs:
      result: ${{ steps.step-id.outputs.result }}
```

---

## Migration from Regular Workflows

### Before (Duplicated Workflow)

```yaml
# repo-a/.github/workflows/ci.yml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v4
      - run: npm ci && npm run build

# repo-b/.github/workflows/ci.yml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v4
      - run: npm ci && npm run build
```

### After (Reusable Workflow)

**Shared Workflow:**

```yaml
# shared-workflows/.github/workflows/node-build.yml
name: Node.js Build
on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '20'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci && npm run build
```

**Caller Workflows:**

```yaml
# repo-a/.github/workflows/ci.yml
name: CI
on: [push]
jobs:
  build:
    uses: org/shared-workflows/.github/workflows/node-build.yml@v1
    with:
      node-version: '20'

# repo-b/.github/workflows/ci.yml
name: CI
on: [push]
jobs:
  build:
    uses: org/shared-workflows/.github/workflows/node-build.yml@v1
    with:
      node-version: '18'
```

---

For composite actions (step-level reuse), see `composite-actions.md`.
