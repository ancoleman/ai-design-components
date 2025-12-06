---
sidebar_position: 7
title: Writing GitHub Actions
description: Write GitHub Actions workflows with proper syntax, reusable workflows, and security best practices
tags: [developer-productivity, github-actions, ci-cd, automation, workflows]
---

# Writing GitHub Actions

Create GitHub Actions workflows for CI/CD pipelines, automated testing, deployments, and repository automation using YAML-based configuration with native GitHub integration. Covers workflow syntax, triggers, reusable patterns, optimization techniques, and security practices.

## When to Use

Use when:
- Creating CI/CD workflows for GitHub repositories
- Automating tests, builds, and deployments via GitHub Actions
- Setting up reusable workflows across multiple repositories
- Optimizing workflow performance with caching and parallelization
- Implementing security best practices for GitHub Actions
- Troubleshooting GitHub Actions YAML syntax or behavior

## Key Features

- **Workflow Syntax**: Triggers, jobs, steps, contexts, and expressions
- **Reusable Workflows**: Share workflows across repositories
- **Composite Actions**: Package step sequences for reuse
- **Matrix Builds**: Test across multiple OS, languages, and versions
- **Caching**: Optimize build times with dependency caching
- **Security**: OIDC authentication, secrets management, minimal permissions
- **Concurrency Control**: Manage parallel and sequential execution

## Quick Start

### Basic CI Workflow

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci
      - run: npm test
      - run: npm run build
```

### Matrix Build Strategy

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [18, 20, 22]
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm test
```

Result: 9 jobs (3 OS × 3 Node versions)

## Common Triggers

```yaml
# Code events
on:
  push:
    branches: [main, develop]
    paths: ['src/**']
  pull_request:
    types: [opened, synchronize, reopened]

# Manual trigger with inputs
on:
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [dev, staging, production]
        description: 'Deployment environment'

# Scheduled runs
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
```

## Reusable Workflows

### Defining a Reusable Workflow

File: `.github/workflows/reusable-build.yml`

```yaml
name: Reusable Build
on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '20'
    secrets:
      NPM_TOKEN:
        required: false
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

### Calling a Reusable Workflow

```yaml
jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      node-version: '20'
    secrets: inherit  # Same org only
```

## Composite Actions

### Defining a Composite Action

File: `.github/actions/setup-project/action.yml`

```yaml
name: 'Setup Project'
description: 'Install dependencies and setup environment'

inputs:
  node-version:
    description: 'Node.js version'
    default: '20'

outputs:
  cache-hit:
    value: ${{ steps.cache.outputs.cache-hit }}

runs:
  using: "composite"
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'

    - id: cache
      uses: actions/cache@v4
      with:
        path: node_modules
        key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}

    - if: steps.cache.outputs.cache-hit != 'true'
      shell: bash
      run: npm ci
```

### Using a Composite Action

```yaml
steps:
  - uses: actions/checkout@v5
  - uses: ./.github/actions/setup-project
    with:
      node-version: '20'
  - run: npm run build
```

## Multi-Job Workflow with Dependencies

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/download-artifact@v5
        with:
          name: dist
      - run: npm test

  deploy:
    needs: [build, test]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/download-artifact@v5
        with:
          name: dist
      - run: ./deploy.sh
```

## Security Best Practices

### Minimal Permissions

```yaml
# Workflow-level
permissions:
  contents: read
  pull-requests: write

# Job-level
jobs:
  deploy:
    permissions:
      contents: write
      deployments: write
    steps: [...]
```

### OIDC Authentication (No Long-Lived Credentials)

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # Required for OIDC
      contents: read
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          aws-region: us-east-1
      - run: aws s3 sync ./dist s3://my-bucket
```

### Action Pinning with Dependabot

```yaml
# Pin to commit SHA (not tags)
- uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608  # v5.0.0
```

**Enable Dependabot:**

File: `.github/dependabot.yml`

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Optimization Techniques

### Built-in Caching

```yaml
# Node.js
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'  # or 'yarn', 'pnpm'

# Python
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'

# Go
- uses: actions/setup-go@v5
  with:
    go-version: '1.21'
    cache: true
```

### Manual Caching

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
    restore-keys: ${{ runner.os }}-deps-
```

### Concurrency Control

```yaml
# Cancel in-progress runs on new push
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

# Single deployment per environment
jobs:
  deploy:
    concurrency:
      group: production-deployment
      cancel-in-progress: false
    steps: [...]
```

### Conditional Execution

```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    steps:
      - if: runner.os == 'Linux'
        run: ./deploy-linux.sh
      - if: runner.os == 'Windows'
        run: .\deploy-windows.ps1
```

## Common Context Variables

```yaml
steps:
  - name: Print context info
    run: |
      echo "Branch: ${{ github.ref }}"
      echo "Event: ${{ github.event_name }}"
      echo "Actor: ${{ github.actor }}"
      echo "SHA: ${{ github.sha }}"
      echo "Runner OS: ${{ runner.os }}"
```

## Decision Framework

### Reusable Workflow vs Composite Action

**Use Reusable Workflow when:**
- Standardizing entire CI/CD jobs across repositories
- Need complete job replacement with inputs/outputs
- Want secrets to inherit by default
- Orchestrating multiple steps with job-level configuration

**Use Composite Action when:**
- Packaging 5-20 step sequences for reuse
- Need step-level abstraction within jobs
- Want to distribute via marketplace or private repos
- Require local file access without artifacts

| Feature | Reusable Workflow | Composite Action |
|---------|------------------|------------------|
| Scope | Complete job | Step sequence |
| Trigger | `workflow_call` | `uses:` in step |
| Secrets | Inherit by default | Must pass explicitly |
| File Sharing | Requires artifacts | Same runner/workspace |

### Self-Hosted vs GitHub-Hosted Runners

**Use GitHub-Hosted Runners when:**
- Standard build environments sufficient
- No private network access required
- Within budget or free tier limits

**Use Self-Hosted Runners when:**
- Need specific hardware (GPU, ARM, high memory)
- Require private network/VPN access
- High usage volume (cost optimization)
- Custom software must be pre-installed

## Related Skills

- [Managing Git Workflows](./managing-git-workflows) - Understanding branches and PRs
- [Building CLIs](./building-clis) - Automated releases and distribution
- [Debugging Techniques](./debugging-techniques) - CI/CD debugging
- [Generating Documentation](./generating-documentation) - Automated doc deployment

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/writing-github-actions)
