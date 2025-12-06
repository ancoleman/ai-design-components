# GitHub Actions Workflow Syntax Reference

Complete reference for GitHub Actions YAML syntax, structure, and configuration options.

## Table of Contents

1. [Workflow File Structure](#workflow-file-structure)
2. [Trigger Configuration (on)](#trigger-configuration-on)
3. [Environment Variables](#environment-variables)
4. [Jobs Configuration](#jobs-configuration)
5. [Steps Configuration](#steps-configuration)
6. [Expressions and Contexts](#expressions-and-contexts)
7. [Filters and Patterns](#filters-and-patterns)

---

## Workflow File Structure

**Location:** `.github/workflows/*.yml` or `.github/workflows/*.yaml`

**Top-Level Keys:**

```yaml
name: Workflow Name                 # Display name (optional)
run-name: Custom run name           # Dynamic run name (optional)
on: [push, pull_request]           # Trigger events (required)
permissions: read-all              # Default permissions (optional)
env:                               # Workflow-level environment variables
  NODE_ENV: production
defaults:                          # Default settings for all jobs
  run:
    shell: bash
    working-directory: ./src
concurrency:                       # Concurrency control
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
jobs:                              # Job definitions (required)
  job_id:
    # Job configuration
```

---

## Trigger Configuration (on)

### Single Event

```yaml
on: push
```

### Multiple Events

```yaml
on: [push, pull_request, workflow_dispatch]
```

### Event with Configuration

**Push Event:**

```yaml
on:
  push:
    branches:
      - main
      - 'releases/**'
    branches-ignore:
      - 'experimental/**'
    tags:
      - v*.*.*
    paths:
      - 'src/**'
      - '**.js'
    paths-ignore:
      - 'docs/**'
      - '**.md'
```

**Pull Request Event:**

```yaml
on:
  pull_request:
    types:
      - opened
      - synchronize
      - reopened
    branches:
      - main
    paths:
      - 'src/**'
```

**Available Types:** `opened`, `synchronize`, `reopened`, `closed`, `assigned`, `unassigned`, `labeled`, `unlabeled`, `review_requested`, `ready_for_review`

**Pull Request Target (Safe for Forks):**

```yaml
on:
  pull_request_target:
    types: [opened, synchronize]
```

**Schedule Event:**

```yaml
on:
  schedule:
    - cron: '30 5 * * 1-5'  # 5:30 AM UTC, Mon-Fri
    - cron: '0 0 * * 0'     # Midnight UTC, Sunday
```

**Manual Trigger (workflow_dispatch):**

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        type: choice
        options:
          - dev
          - staging
          - production
        default: dev
      version:
        description: 'Version to deploy'
        required: true
        type: string
      enable-debug:
        description: 'Enable debug mode'
        required: false
        type: boolean
        default: false
```

**Input Types:** `string`, `choice`, `boolean`, `environment`

**Reusable Workflow (workflow_call):**

```yaml
on:
  workflow_call:
    inputs:
      config-path:
        required: true
        type: string
      node-version:
        required: false
        type: string
        default: '20'
    secrets:
      api-token:
        required: true
      npm-token:
        required: false
    outputs:
      build-artifact:
        description: "Name of build artifact"
        value: ${{ jobs.build.outputs.artifact-name }}
```

**Repository Dispatch:**

```yaml
on:
  repository_dispatch:
    types: [deploy, test-all]
```

**Other Events:**

```yaml
on:
  release:
    types: [published, created, edited]
  issues:
    types: [opened, labeled]
  issue_comment:
    types: [created, edited]
  deployment:
  deployment_status:
  watch:
    types: [started]  # Repository starred
```

---

## Environment Variables

### Workflow-Level

```yaml
env:
  NODE_ENV: production
  API_URL: https://api.example.com

jobs:
  build:
    steps:
      - run: echo $NODE_ENV  # Available to all jobs
```

### Job-Level

```yaml
jobs:
  build:
    env:
      BUILD_TYPE: release
    steps:
      - run: echo $BUILD_TYPE  # Available to all steps in job
```

### Step-Level

```yaml
steps:
  - name: Deploy
    env:
      API_KEY: ${{ secrets.API_KEY }}
      ENVIRONMENT: production
    run: ./deploy.sh
```

### Default Environment Variables

GitHub provides default variables:

- `GITHUB_TOKEN` - Authentication token
- `GITHUB_REPOSITORY` - Repository name (owner/repo)
- `GITHUB_REF` - Branch or tag ref
- `GITHUB_SHA` - Commit SHA
- `GITHUB_ACTOR` - Username that triggered workflow
- `GITHUB_WORKFLOW` - Workflow name
- `GITHUB_RUN_ID` - Unique run ID
- `RUNNER_OS` - Runner OS (Linux, Windows, macOS)
- `RUNNER_TEMP` - Temporary directory path

---

## Jobs Configuration

### Basic Job

```yaml
jobs:
  build:
    name: Build Application
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: npm run build
```

### Job with Dependencies

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    needs: build
    runs-on: ubuntu-latest
    steps: [...]

  deploy:
    needs: [build, test]
    runs-on: ubuntu-latest
    steps: [...]
```

### Job with Outputs

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.get-version.outputs.version }}
      artifact-name: build-${{ steps.get-version.outputs.version }}
    steps:
      - id: get-version
        run: echo "version=$(cat VERSION)" >> $GITHUB_OUTPUT
```

**Accessing Outputs:**

```yaml
jobs:
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Version: ${{ needs.build.outputs.version }}"
```

### Job with Matrix Strategy

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      max-parallel: 4
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [18, 20, 22]
        include:
          - os: ubuntu-latest
            node: 20
            experimental: true
        exclude:
          - os: windows-latest
            node: 18
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
```

### Job with Environment

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://prod.example.com
    steps:
      - run: ./deploy.sh
```

**Environment Features:**
- Protection rules (required reviewers)
- Environment-specific secrets
- Deployment history
- Wait timers

### Job with Container

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: node:20-alpine
      env:
        NODE_ENV: test
      volumes:
        - /data:/data
      options: --cpus 2 --memory 4g
    steps:
      - run: node --version
```

### Job with Services

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    steps:
      - run: psql --host localhost --port 5432
```

### Job Concurrency

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    concurrency:
      group: production-deploy
      cancel-in-progress: false
    steps: [...]
```

### Job Permissions

```yaml
jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps: [...]
```

**Available Permissions:**
- `actions` - GitHub Actions
- `checks` - Checks on code
- `contents` - Repository contents
- `deployments` - Deployments
- `id-token` - OIDC token
- `issues` - Issues and comments
- `packages` - GitHub Packages
- `pull-requests` - Pull requests
- `repository-projects` - Projects
- `security-events` - Security events
- `statuses` - Commit statuses

**Values:** `read`, `write`, `none`

### Job Conditions

```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps: [...]
```

---

## Steps Configuration

### Using Actions

```yaml
- name: Checkout repository
  uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608  # v5.0.0
  with:
    fetch-depth: 0
    submodules: true
```

### Running Commands

```yaml
- name: Build application
  run: |
    npm ci
    npm run build
    npm test
```

### Running Scripts

```yaml
- name: Run script
  run: ./scripts/deploy.sh
  shell: bash
```

**Available Shells:** `bash`, `pwsh`, `python`, `sh`, `cmd`, `powershell`

### Step with ID (for outputs)

```yaml
- id: get-version
  run: |
    VERSION=$(cat VERSION)
    echo "version=$VERSION" >> $GITHUB_OUTPUT
    echo "sha=$(git rev-parse --short HEAD)" >> $GITHUB_OUTPUT
```

**Accessing Outputs:**

```yaml
- run: echo "Version: ${{ steps.get-version.outputs.version }}"
```

### Step with Timeout

```yaml
- name: Long running task
  run: ./slow-script.sh
  timeout-minutes: 30
```

### Step with Continue on Error

```yaml
- name: Optional check
  run: npm audit
  continue-on-error: true
```

### Step Conditions

```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh

- name: Install dependencies
  if: steps.cache.outputs.cache-hit != 'true'
  run: npm ci

- name: Upload artifacts on failure
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: logs
    path: logs/
```

**Status Check Functions:**
- `success()` - Previous steps succeeded
- `always()` - Always run (even on cancellation)
- `cancelled()` - Workflow was cancelled
- `failure()` - Previous step failed

---

## Expressions and Contexts

### Expression Syntax

```yaml
${{ expression }}
```

### Context Objects

**github context:**

```yaml
github.actor              # User who triggered
github.event_name         # Event type (push, pull_request, etc.)
github.ref               # Branch or tag ref
github.ref_name          # Branch or tag name (without refs/)
github.sha               # Commit SHA
github.repository        # owner/repo
github.repository_owner  # Repository owner
github.workflow          # Workflow name
github.run_id            # Unique run ID
github.run_number        # Run number
github.job               # Job ID
```

**env context:**

```yaml
env.NODE_ENV
env.API_KEY
```

**secrets context:**

```yaml
secrets.API_TOKEN
secrets.NPM_TOKEN
```

**inputs context (workflow_dispatch or workflow_call):**

```yaml
inputs.environment
inputs.version
inputs.enable-debug
```

**matrix context:**

```yaml
matrix.os
matrix.node
matrix.experimental
```

**steps context:**

```yaml
steps.build.outputs.version
steps.build.outcome        # success, failure, cancelled, skipped
steps.build.conclusion     # success, failure, cancelled, skipped, neutral
```

**needs context:**

```yaml
needs.build.outputs.version
needs.build.result         # success, failure, cancelled, skipped
```

**runner context:**

```yaml
runner.os                 # Linux, Windows, macOS
runner.arch              # X86, X64, ARM, ARM64
runner.name              # Runner name
runner.temp              # Temp directory path
runner.tool_cache        # Tool cache directory
```

**job context:**

```yaml
job.status               # success, failure, cancelled
job.services             # Service containers
```

### Operators

**Comparison:**
- `==` - Equal
- `!=` - Not equal
- `<` - Less than
- `<=` - Less than or equal
- `>` - Greater than
- `>=` - Greater than or equal

**Logical:**
- `&&` - AND
- `||` - OR
- `!` - NOT

**Example:**

```yaml
if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

### Functions

**contains(search, item):**

```yaml
if: contains(github.event.head_commit.message, '[skip ci]')
```

**startsWith(search, prefix):**

```yaml
if: startsWith(github.ref, 'refs/tags/')
```

**endsWith(search, suffix):**

```yaml
if: endsWith(github.ref, '-beta')
```

**format(template, args):**

```yaml
run: echo ${{ format('Hello {0}', github.actor) }}
```

**join(array, separator):**

```yaml
run: echo ${{ join(github.event.commits.*.message, ', ') }}
```

**toJSON(value):**

```yaml
run: echo '${{ toJSON(github) }}'
```

**fromJSON(value):**

```yaml
strategy:
  matrix:
    version: ${{ fromJSON('[18, 20, 22]') }}
```

**hashFiles(pattern):**

```yaml
key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
```

---

## Filters and Patterns

### Branch Filters

```yaml
on:
  push:
    branches:
      - main
      - 'releases/**'      # Matches releases/v1, releases/v1/beta
      - '!releases/alpha'  # Exclude pattern
```

### Tag Filters

```yaml
on:
  push:
    tags:
      - v*.*.*            # Matches v1.0.0, v2.1.3
      - 'beta-*'          # Matches beta-1, beta-2
```

### Path Filters

```yaml
on:
  push:
    paths:
      - 'src/**'          # Any file in src/ and subdirectories
      - '**.js'           # Any .js file
      - 'config/*.json'   # JSON files in config/ (not subdirectories)
    paths-ignore:
      - 'docs/**'
      - '**.md'
      - '.github/**'
```

**Patterns:**
- `*` - Matches zero or more characters (except `/`)
- `**` - Matches zero or more directories
- `?` - Matches single character
- `!` - Negates pattern (exclude)

### Activity Type Filters

```yaml
on:
  pull_request:
    types:
      - opened
      - synchronize
      - reopened
      - closed

  issues:
    types:
      - opened
      - labeled
      - assigned
```

---

## Advanced Features

### Reusing Workflows

**Caller Workflow:**

```yaml
jobs:
  call-workflow:
    uses: octo-org/repo/.github/workflows/reusable.yml@v1
    with:
      input1: value1
    secrets:
      token: ${{ secrets.TOKEN }}
```

**Reusable Workflow:**

```yaml
on:
  workflow_call:
    inputs:
      input1:
        required: true
        type: string
    secrets:
      token:
        required: true
```

### Composite Actions

**action.yml:**

```yaml
name: 'Setup Project'
description: 'Setup project environment'
inputs:
  node-version:
    description: 'Node version'
    required: false
    default: '20'
runs:
  using: "composite"
  steps:
    - run: echo "Setting up Node ${{ inputs.node-version }}"
      shell: bash
```

### Workflow Commands

**Set output:**

```bash
echo "name=value" >> $GITHUB_OUTPUT
```

**Set environment variable:**

```bash
echo "VAR_NAME=value" >> $GITHUB_ENV
```

**Add to PATH:**

```bash
echo "/path/to/bin" >> $GITHUB_PATH
```

**Set step summary:**

```bash
echo "## Summary" >> $GITHUB_STEP_SUMMARY
echo "Build succeeded" >> $GITHUB_STEP_SUMMARY
```

**Group logs:**

```bash
echo "::group::Group name"
echo "Content"
echo "::endgroup::"
```

**Mask value (secret):**

```bash
echo "::add-mask::$SECRET_VALUE"
```

### Debugging

**Enable debug logging:**

Set repository secret: `ACTIONS_STEP_DEBUG=true`

**Enable runner diagnostic logging:**

Set repository secret: `ACTIONS_RUNNER_DEBUG=true`

---

## Complete Example

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
    paths:
      - 'src/**'
      - 'package.json'
  pull_request:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [dev, staging, production]

env:
  NODE_ENV: production

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read
  pull-requests: write

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node: [18, 20, 22]
    steps:
      - uses: actions/checkout@v5

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'

      - run: npm ci

      - run: npm test

      - if: matrix.node == 20
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage/

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    permissions:
      contents: write
      deployments: write
    steps:
      - uses: actions/checkout@v5

      - run: ./deploy.sh
        env:
          API_KEY: ${{ secrets.API_KEY }}
```

---

For working examples, see the `examples/` directory.
