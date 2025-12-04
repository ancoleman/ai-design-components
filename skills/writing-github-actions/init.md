# Writing GitHub Actions

**Skill Level:** Low Level
**Status:** Master Plan Complete
**Created:** December 3, 2025
**Research Date:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [GitHub Actions Taxonomy](#github-actions-taxonomy)
5. [Decision Framework](#decision-framework)
6. [Workflow Patterns](#workflow-patterns)
7. [Reusable Workflows](#reusable-workflows)
8. [Composite Actions](#composite-actions)
9. [Matrix Builds](#matrix-builds)
10. [Caching and Optimization](#caching-and-optimization)
11. [Security Best Practices](#security-best-practices)
12. [Concurrency Control](#concurrency-control)
13. [Artifact Management](#artifact-management)
14. [Recommended Tools and Actions](#recommended-tools-and-actions)
15. [Skill Structure Design](#skill-structure-design)
16. [Integration Points](#integration-points)
17. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

GitHub Actions is the native CI/CD platform for GitHub repositories, offering deep integration with the GitHub ecosystem. While CI/CD pipeline design is covered by `building-ci-pipelines`, this skill focuses on the specific syntax, patterns, and best practices unique to GitHub Actions.

**Key Differentiators:**
- **Native GitHub Integration**: Seamless access to GitHub APIs, events, and context
- **Marketplace Ecosystem**: 10,000+ pre-built actions for common tasks
- **YAML-First Configuration**: Declarative workflow syntax with expressions
- **Free Tier**: Generous free minutes for public and private repositories
- **Modern Features**: Reusable workflows, composite actions, matrix builds, OIDC

### Market Position (2025)

**Strengths:**
- Dominant for GitHub-hosted projects (>70% adoption for repos using CI/CD)
- Tight integration with GitHub features (PRs, Issues, Releases, Packages)
- Active ecosystem with thousands of marketplace actions
- Modern security features (OIDC, secret scanning, Dependabot integration)
- AI-powered workflow generation capabilities

**Use Cases:**
- **Primary:** Projects hosted on GitHub (any language/framework)
- **Ideal for:** Open source projects, GitHub-centric workflows, teams using GitHub Enterprise
- **Complements:** Infrastructure as Code (`infrastructure-as-code`), GitOps (`gitops-workflows`), Testing (`testing-strategies`)

---

## Skill Purpose and Scope

### What This Skill Covers

**Core Focus:**
- GitHub Actions workflow syntax (YAML structure, triggers, jobs, steps)
- Reusable workflows (`workflow_call` pattern)
- Composite actions (`action.yml` structure)
- Matrix builds and parallel execution strategies
- Caching patterns (dependencies, build outputs)
- Secrets management (GitHub Secrets, OIDC authentication)
- Concurrency control (`cancel-in-progress`, concurrency groups)
- Artifact management (upload, download, retention)
- Self-hosted runners (when to use, configuration)
- Environment protection rules and deployment gates

**Advanced Patterns:**
- Multi-job workflows with dependencies
- Dynamic matrix strategies from API responses
- Cross-repository workflow reuse
- Custom actions (composite and Docker-based)
- Optimization techniques (parallel jobs, caching, minimal checkout)

### What This Skill Does NOT Cover

**Out of Scope:**
- **Full CI/CD Pipeline Design** → See `building-ci-pipelines` (strategy, testing pyramid, deployment patterns)
- **GitOps and Deployment Automation** → See `gitops-workflows` (ArgoCD, Flux, declarative deployments)
- **Infrastructure as Code** → See `infrastructure-as-code` (Terraform, Pulumi integration details)
- **Testing Strategies** → See `testing-strategies` (test frameworks, coverage, integration testing)
- **Security Hardening** → See `security-hardening` (container scanning, SAST/DAST tools)
- **Other CI Systems** → GitLab CI, Jenkins, CircleCI (different syntax/patterns)

### Relationship to Other Skills

**Depends On:**
- `git-workflows` - Understanding branches, PRs, merge strategies
- `testing-strategies` - Knowing what tests to run in CI

**Used By:**
- `building-ci-pipelines` - Uses GitHub Actions as the execution engine
- `gitops-workflows` - Triggers deployments via GitHub Actions
- `infrastructure-as-code` - Executes IaC via GitHub Actions workflows
- `deploying-applications` - Uses GitHub Actions for deployment automation

---

## Research Findings

### Research Sources

**Google Search Grounding (December 2025):**
- Query 1: "GitHub Actions best practices 2025 workflows" (8 results)
- Query 2: "GitHub Actions reusable workflows composite actions" (8 results)
- Query 3: "GitHub Actions caching matrix builds optimization" (failed - service error)

**Context7 Documentation:**
- **Library:** `/websites/github_en_actions`
- **Trust Score:** High (official GitHub documentation)
- **Code Snippets:** 2,912+ examples
- **Benchmark Score:** 87.7/100
- **Topics Researched:** workflows, reusable workflows, composite actions, caching, triggers, concurrency, artifacts

### Key Research Insights (2025)

**1. Reusable Workflows vs Composite Actions**

| Feature | Reusable Workflows | Composite Actions |
|---------|-------------------|-------------------|
| **Scope** | Entire job replacement | Step-level reuse |
| **Trigger** | `workflow_call` | `uses:` in step |
| **Nesting** | Cannot nest reusable workflows | Up to 10 layers deep |
| **Secrets** | Inherit by default | Must pass explicitly |
| **Environment Vars** | Do not inherit | Inherit from job |
| **File Sharing** | Requires artifacts | Same runner/workspace |
| **Best For** | Complete CI/CD jobs | Utility step sequences |

**When to Use:**
- **Reusable Workflows:** Standardize entire CI/CD jobs (build, test, deploy) across repos
- **Composite Actions:** Package common step sequences (setup, validation, cleanup)

**2. Caching Best Practices (2025)**

**Built-in Caching (Recommended):**
```yaml
# Modern approach - setup actions handle caching
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'  # or 'yarn', 'pnpm'
```

**Manual Caching (Advanced Control):**
```yaml
# When you need custom cache keys
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

**Cache Key Strategies:**
- **Dependency caching:** Hash lock files (`hashFiles('**/package-lock.json')`)
- **Build caching:** Include source hash for incremental builds
- **Multi-layer restore:** Use `restore-keys` for partial cache hits

**3. Concurrency Control (2025)**

**Cancel In-Progress Pattern:**
```yaml
concurrency:
  group: ${{ github.ref }}
  cancel-in-progress: true
```

**Use Cases:**
- **Deployments:** Only one deployment per environment at a time
- **PR Workflows:** Cancel old runs when new commits pushed
- **Resource Management:** Prevent concurrent access to shared resources

**4. Matrix Build Optimization**

**Static Matrix:**
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    node: [18, 20, 22]
```

**Dynamic Matrix (from API):**
```yaml
strategy:
  matrix:
    version: ${{ github.event.client_payload.versions }}
```

**Best Practices:**
- **Fail Fast:** Set `fail-fast: false` for comprehensive testing
- **Parallel Execution:** GitHub provides up to 20 concurrent jobs (free tier)
- **Matrix with Reusable Workflows:** Combine for powerful multi-environment testing

**5. Security Best Practices (2025)**

**Secrets Management:**
- Use GitHub Secrets for sensitive data (never hardcode)
- OIDC for cloud provider authentication (no long-lived credentials)
- Environment-specific secrets with protection rules

**Workflow Security:**
- Pin actions to commit SHAs (not tags): `actions/checkout@abc123`
- Review third-party actions before use
- Use `GITHUB_TOKEN` permissions: principle of least privilege
- Enable Dependabot for action updates

**6. Modern Features (2025)**

**Nested Reusable Workflows:**
- Increased limit: Up to 10 levels of nesting
- Total workflow calls: Up to 50 per run

**AI-Powered Workflow Generation:**
- GitHub Copilot can suggest workflow YAML
- Context-aware action recommendations

**Enhanced OIDC Support:**
- Federated identity for AWS, Azure, GCP
- No need to store cloud credentials as secrets

---

## GitHub Actions Taxonomy

### Workflow Components Hierarchy

```
Repository
└── .github/workflows/
    ├── workflow.yml              # Main workflow file
    │   ├── name                  # Workflow name (displayed in UI)
    │   ├── on                    # Trigger events
    │   │   ├── push              # Code push events
    │   │   ├── pull_request      # PR events
    │   │   ├── schedule          # Cron schedule
    │   │   ├── workflow_dispatch # Manual trigger
    │   │   └── workflow_call     # Reusable workflow
    │   ├── env                   # Workflow-level env vars
    │   ├── concurrency           # Concurrency control
    │   └── jobs                  # Job definitions
    │       ├── job_id            # Unique job identifier
    │       │   ├── runs-on       # Runner type
    │       │   ├── needs         # Job dependencies
    │       │   ├── strategy      # Matrix strategy
    │       │   ├── environment   # Deployment environment
    │       │   ├── concurrency   # Job-level concurrency
    │       │   └── steps         # Step sequence
    │       │       ├── name      # Step name
    │       │       ├── uses      # Action to use
    │       │       ├── with      # Action inputs
    │       │       ├── run       # Shell command
    │       │       ├── env       # Step-level env vars
    │       │       └── if        # Conditional execution
    │       └── ...
    └── ...
```

### Trigger Types

**1. Code Events**
- `push` - Commits pushed to branch
- `pull_request` - PR opened, synchronized, reopened
- `pull_request_target` - PR from fork (safe for secrets)

**2. Scheduled Events**
- `schedule` - Cron-based scheduling

**3. Manual Events**
- `workflow_dispatch` - Manual trigger with inputs
- `repository_dispatch` - Webhook-triggered

**4. Reuse Events**
- `workflow_call` - Called by other workflows

**5. GitHub Events**
- `release` - Release published/created
- `issues` - Issue opened/closed/labeled
- `deployment` - Deployment created

### Action Types

**1. GitHub Official Actions**
- `actions/checkout@v5` - Clone repository
- `actions/setup-node@v4` - Setup Node.js
- `actions/cache@v4` - Cache dependencies
- `actions/upload-artifact@v4` - Upload artifacts
- `actions/download-artifact@v5` - Download artifacts

**2. Third-Party Marketplace Actions**
- 10,000+ actions available
- Verified publishers (GitHub, AWS, Azure, etc.)
- Community-contributed actions

**3. Custom Actions**
- **Composite Actions:** YAML-based step sequences
- **Docker Actions:** Containerized actions
- **JavaScript Actions:** Node.js-based actions

### Runner Types

**1. GitHub-Hosted Runners**
- `ubuntu-latest`, `ubuntu-22.04`, `ubuntu-20.04`
- `windows-latest`, `windows-2022`, `windows-2019`
- `macos-latest`, `macos-14`, `macos-13`, `macos-12`

**2. Self-Hosted Runners**
- Custom hardware/software configurations
- Private network access
- Cost optimization for high usage
- Custom labels for targeting

---

## Decision Framework

### Should I Use GitHub Actions?

```
Start: Need CI/CD for project
│
├─→ Hosted on GitHub?
│   ├─ YES → GitHub Actions (native integration)
│   └─ NO → Consider GitLab CI, Jenkins, CircleCI
│
├─→ Need GitHub-specific features?
│   ├─ YES (PRs, Issues, Releases) → GitHub Actions
│   └─ NO → Any CI system works
│
└─→ Budget constraints?
    ├─ Open Source → GitHub Actions (unlimited)
    ├─ Private (low usage) → GitHub Actions (free tier: 2,000 min/month)
    └─ Private (high usage) → Compare costs (GitHub vs self-hosted)
```

### Workflow vs Reusable Workflow vs Composite Action

```
What are you trying to reuse?
│
├─→ Entire CI/CD job (build, test, deploy)?
│   └─ Use Reusable Workflow
│       - Define in separate .yml file
│       - Trigger: workflow_call
│       - Call with: uses: org/repo/.github/workflows/name.yml@ref
│
├─→ Sequence of steps (5-20 steps)?
│   └─ Use Composite Action
│       - Define in action.yml
│       - Store in .github/actions/ or separate repo
│       - Call with: uses: ./path/to/action or org/repo@ref
│
├─→ Single command or script?
│   └─ Use run step directly
│       - No need for abstraction
│       - Keep it simple
│
└─→ Complex logic with dependencies?
    └─ Consider Docker or JavaScript Action
        - More powerful but more complex
        - Better for published marketplace actions
```

### Caching Strategy Decision Tree

```
What do you want to cache?
│
├─→ Node.js dependencies (npm/yarn/pnpm)?
│   └─ Use setup-node with cache parameter
│       cache: 'npm'  # Simplest approach
│
├─→ Other language dependencies?
│   ├─ Python → setup-python with cache: 'pip'
│   ├─ Java → setup-java with cache: 'maven' or 'gradle'
│   ├─ .NET → setup-dotnet with cache: true
│   └─ Go → setup-go with cache: true
│
├─→ Build outputs or custom files?
│   └─ Use actions/cache with custom paths
│       - Define path and key strategy
│       - Use hashFiles() for cache invalidation
│
└─→ Docker layers?
    └─ Use docker/build-push-action with cache
        - BuildKit cache backend
        - Cache to GitHub Container Registry
```

### When to Use Self-Hosted Runners

**Use GitHub-Hosted Runners When:**
- Standard build environments sufficient
- No private network access needed
- Within free tier limits or budget acceptable
- Don't want infrastructure management

**Use Self-Hosted Runners When:**
- Need specific hardware (GPU, ARM, etc.)
- Require private network/VPN access
- High usage (cost optimization)
- Custom software pre-installed
- Security/compliance requirements

---

## Workflow Patterns

### 1. Basic CI Workflow

**Use Case:** Run tests on every push and PR

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
      - run: npm run lint
```

**Key Elements:**
- Triggers on push to main and all PRs
- Uses caching for faster runs
- `npm ci` for clean, reproducible installs

### 2. Multi-Job Workflow with Dependencies

**Use Case:** Build, test, then deploy (sequential)

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build

      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
          retention-days: 5

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
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/download-artifact@v5
        with:
          name: dist
      - name: Deploy to production
        run: echo "Deploying..."
```

**Key Elements:**
- `needs:` creates job dependencies
- Artifacts pass data between jobs
- `environment:` enables protection rules

### 3. Parallel Jobs (Independent)

**Use Case:** Run lint, test, and security scan simultaneously

```yaml
name: Quality Checks

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint

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

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: npm audit
```

**Key Elements:**
- No `needs:` - all jobs run in parallel
- Faster overall execution
- Independent failure domains

### 4. Conditional Job Execution

**Use Case:** Deploy only on main branch, skip on PRs

```yaml
name: CI/CD

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
      - run: npm test

  deploy:
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: echo "Deploying to production"
```

**Key Elements:**
- `if:` condition on job or step level
- `github.event_name` and `github.ref` context variables
- Deploy only runs for pushes to main

### 5. Manual Workflow with Inputs

**Use Case:** Manually trigger deployment to specific environment

```yaml
name: Manual Deploy

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        type: choice
        options:
          - dev
          - staging
          - production
      version:
        description: 'Version to deploy'
        required: true
        type: string

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: Deploy version ${{ inputs.version }}
        run: |
          echo "Deploying version ${{ inputs.version }} to ${{ inputs.environment }}"
```

**Key Elements:**
- `workflow_dispatch` trigger
- Typed inputs (choice, string, boolean, etc.)
- Access inputs via `${{ inputs.name }}`

### 6. Scheduled Workflow (Cron)

**Use Case:** Nightly dependency updates, cleanup, backups

```yaml
name: Nightly Maintenance

on:
  schedule:
    # Every day at 2 AM UTC
    - cron: '0 2 * * *'
  workflow_dispatch:  # Also allow manual trigger

jobs:
  update-dependencies:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: npm update
      - run: npm audit fix

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          title: "chore: Update dependencies"
          branch: deps/auto-update
```

**Key Elements:**
- `schedule` with cron syntax
- `workflow_dispatch` for manual testing
- Automated PR creation for changes

---

## Reusable Workflows

### Defining a Reusable Workflow

**File:** `.github/workflows/reusable-build.yml`

```yaml
name: Reusable Build

on:
  workflow_call:
    inputs:
      node-version:
        required: false
        type: string
        default: '20'
      build-command:
        required: false
        type: string
        default: 'npm run build'
    secrets:
      NPM_TOKEN:
        required: false
    outputs:
      build-artifact:
        description: "Name of the build artifact"
        value: ${{ jobs.build.outputs.artifact-name }}

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      artifact-name: ${{ steps.upload.outputs.artifact-name }}
    steps:
      - uses: actions/checkout@v5

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci
        env:
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}

      - name: Build
        run: ${{ inputs.build-command }}

      - id: upload
        uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/
```

**Key Elements:**
- `on: workflow_call` - Makes workflow reusable
- `inputs:` - Define parameters with types and defaults
- `secrets:` - Define required secrets
- `outputs:` - Return data to caller

### Calling a Reusable Workflow

**Same Repository:**

```yaml
name: CI

on: [push]

jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      node-version: '20'
      build-command: 'npm run build:prod'
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**Different Repository:**

```yaml
name: CI

on: [push]

jobs:
  build:
    uses: my-org/shared-workflows/.github/workflows/reusable-build.yml@v1
    with:
      node-version: '20'
    secrets: inherit  # Pass all secrets (same org only)
```

**Key Elements:**
- `uses:` points to workflow file
- Use `.` for same repo, `org/repo@ref` for external
- `secrets: inherit` passes all secrets (same org/enterprise)
- Pin to specific ref (`@v1`, `@main`, `@sha`)

### Reusable Workflow with Matrix

**Caller Workflow:**

```yaml
jobs:
  multi-env-deploy:
    strategy:
      matrix:
        environment: [dev, staging, production]
    uses: ./.github/workflows/deploy.yml
    with:
      environment: ${{ matrix.environment }}
    secrets: inherit
```

**Reusable Deploy Workflow:**

```yaml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: Deploy to ${{ inputs.environment }}
        run: echo "Deploying..."
```

---

## Composite Actions

### Defining a Composite Action

**File:** `.github/actions/setup-project/action.yml`

```yaml
name: 'Setup Project'
description: 'Install dependencies and setup project environment'

inputs:
  node-version:
    description: 'Node.js version to use'
    required: false
    default: '20'
  install-command:
    description: 'Command to install dependencies'
    required: false
    default: 'npm ci'

outputs:
  cache-hit:
    description: "Whether dependencies were cached"
    value: ${{ steps.cache.outputs.cache-hit }}

runs:
  using: "composite"
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'

    - name: Cache dependencies
      id: cache
      uses: actions/cache@v4
      with:
        path: node_modules
        key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}

    - name: Install dependencies
      if: steps.cache.outputs.cache-hit != 'true'
      shell: bash
      run: ${{ inputs.install-command }}

    - name: Verify installation
      shell: bash
      run: node --version && npm --version
```

**Key Elements:**
- `runs.using: "composite"` - Marks as composite action
- `shell:` required for all `run` steps
- Can use other actions with `uses:`
- Access inputs via `${{ inputs.name }}`

### Using a Composite Action

**Local Action (same repo):**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Setup project
        uses: ./.github/actions/setup-project
        with:
          node-version: '20'

      - run: npm run build
```

**External Action (separate repo):**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Setup project
        uses: my-org/shared-actions/setup-project@v1
        with:
          node-version: '20'

      - run: npm run build
```

### Composite Action with Script Execution

**Action Structure:**

```
.github/actions/validate/
├── action.yml
└── scripts/
    └── validate.sh
```

**action.yml:**

```yaml
name: 'Validate Project'
description: 'Run validation checks'

runs:
  using: "composite"
  steps:
    - name: Make script executable
      shell: bash
      run: chmod +x ${{ github.action_path }}/scripts/validate.sh

    - name: Run validation
      shell: bash
      run: ${{ github.action_path }}/scripts/validate.sh
      env:
        GITHUB_ACTION_PATH: ${{ github.action_path }}
```

**Key Elements:**
- `${{ github.action_path }}` - Path to action directory
- Scripts included with action
- Environment variables passed to scripts

---

## Matrix Builds

### Basic Matrix Strategy

**Test across multiple versions:**

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [18, 20, 22]
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm test
```

**Result:** 9 jobs (3 OS × 3 Node versions)

### Matrix with Include/Exclude

**Add specific configurations:**

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [18, 20]
    include:
      # Add macOS with Node 20 only
      - os: macos-latest
        node: 20
    exclude:
      # Skip Windows + Node 18 (known issues)
      - os: windows-latest
        node: 18
```

### Matrix with Fail-Fast Control

**Continue all jobs even if one fails:**

```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    node: [18, 20, 22]
```

**Use Cases:**
- Comprehensive testing (see all failures)
- Flaky test environments
- Coverage reports from all platforms

### Dynamic Matrix from API

**Generate matrix from external source:**

```yaml
on:
  repository_dispatch:
    types: [test-versions]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        version: ${{ github.event.client_payload.versions }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.version }}
      - run: npm test
```

**Trigger via API:**

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/owner/repo/dispatches \
  -d '{"event_type":"test-versions","client_payload":{"versions":[18,20,22]}}'
```

---

## Caching and Optimization

### 1. Built-in Setup Action Caching

**Node.js (npm/yarn/pnpm):**

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'  # or 'yarn', 'pnpm'
```

**Python:**

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'
```

**Java (Maven/Gradle):**

```yaml
- uses: actions/setup-java@v4
  with:
    java-version: '17'
    distribution: 'temurin'
    cache: 'maven'  # or 'gradle'
```

**.NET:**

```yaml
- uses: actions/setup-dotnet@v4
  with:
    dotnet-version: '6.x'
    cache: true
```

### 2. Manual Cache Configuration

**Cache node_modules with custom key:**

```yaml
- name: Cache dependencies
  id: cache-deps
  uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      node_modules
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-deps-
      ${{ runner.os }}-

- name: Install dependencies
  if: steps.cache-deps.outputs.cache-hit != 'true'
  run: npm ci
```

**Key Elements:**
- `key:` - Unique cache identifier
- `hashFiles()` - Generate hash of file contents
- `restore-keys:` - Fallback cache keys (partial matches)
- Check `cache-hit` output to skip install

### 3. Multi-Layer Cache Strategy

**Cache both dependencies and build outputs:**

```yaml
- name: Cache dependencies
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: deps-${{ hashFiles('**/package-lock.json') }}

- name: Cache build
  uses: actions/cache@v4
  with:
    path: .next/cache
    key: build-${{ github.sha }}
    restore-keys: |
      build-${{ github.ref }}-
      build-
```

### 4. Docker Layer Caching

**Cache Docker builds:**

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: false
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### 5. Optimization Techniques

**Minimize Checkout:**

```yaml
# Shallow clone (faster)
- uses: actions/checkout@v5
  with:
    fetch-depth: 1

# Sparse checkout (specific paths only)
- uses: actions/checkout@v5
  with:
    sparse-checkout: |
      src/
      package.json
```

**Conditional Steps:**

```yaml
# Skip unnecessary steps
- name: Run tests
  if: github.event_name == 'pull_request'
  run: npm test

# Cache hit - skip install
- name: Install deps
  if: steps.cache.outputs.cache-hit != 'true'
  run: npm ci
```

**Parallel Jobs:**

```yaml
# Run independent tasks in parallel
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    runs-on: ubuntu-latest
    steps: [...]

  build:
    runs-on: ubuntu-latest
    steps: [...]
```

---

## Security Best Practices

### 1. Secrets Management

**Using GitHub Secrets:**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        run: ./deploy.sh
```

**Environment-Specific Secrets:**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # Uses production secrets
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}  # From production environment
        run: ./deploy.sh
```

### 2. OIDC Authentication (No Long-Lived Credentials)

**AWS OIDC Example:**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          aws-region: us-east-1

      - name: Deploy to AWS
        run: aws s3 sync ./dist s3://my-bucket
```

**Azure OIDC Example:**

```yaml
- uses: azure/login@v1
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

### 3. Minimal GITHUB_TOKEN Permissions

**Default (permissive):**

```yaml
permissions: write-all  # ❌ Avoid this
```

**Principle of Least Privilege:**

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

**Job-Level Permissions:**

```yaml
jobs:
  read-only-job:
    permissions:
      contents: read
    steps: [...]

  deploy-job:
    permissions:
      contents: write
      deployments: write
    steps: [...]
```

### 4. Action Pinning

**❌ Avoid Tag References:**

```yaml
- uses: actions/checkout@v5  # Tag can be moved
```

**✅ Pin to Commit SHA:**

```yaml
- uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608  # v5.0.0
```

**Use Dependabot for Updates:**

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### 5. Pull Request Security

**Protect Against Fork PRs:**

```yaml
# ❌ Dangerous - exposes secrets to forks
on: pull_request

# ✅ Safe - limits secrets to trusted branches
on: pull_request_target
  if: github.event.pull_request.head.repo.full_name == github.repository
```

**Review Required for Workflow Changes:**

```yaml
# Settings → Environments → production
# Required reviewers: 2
# Restrict to protected branches only
```

### 6. Secret Scanning

**Enable GitHub Features:**
- Secret scanning (Settings → Security → Code security)
- Push protection (block commits with secrets)
- Dependabot alerts for actions

**Use .gitignore:**

```
# Never commit
.env
.env.local
secrets.yml
credentials.json
```

---

## Concurrency Control

### Workflow-Level Concurrency

**Cancel in-progress runs on new push:**

```yaml
name: CI

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps: [...]
```

**Key Elements:**
- `group:` - Concurrency identifier (workflow + branch)
- `cancel-in-progress: true` - Cancel old runs
- Useful for PR workflows (save resources)

### Job-Level Concurrency

**Single deployment at a time:**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    concurrency:
      group: production-deployment
      cancel-in-progress: false  # Queue instead of cancel
    environment: production
    steps:
      - name: Deploy
        run: ./deploy.sh
```

**Use Cases:**
- **Deployments:** Prevent concurrent deploys to same environment
- **Database migrations:** Ensure sequential execution
- **Resource locks:** Prevent conflicts

### Per-Environment Concurrency

**Separate concurrency groups per environment:**

```yaml
jobs:
  deploy:
    strategy:
      matrix:
        environment: [dev, staging, production]
    runs-on: ubuntu-latest
    concurrency:
      group: deploy-${{ matrix.environment }}
      cancel-in-progress: false
    environment: ${{ matrix.environment }}
    steps:
      - name: Deploy to ${{ matrix.environment }}
        run: ./deploy.sh
```

### Concurrency Patterns

**Pattern 1: Cancel Old PR Runs**

```yaml
concurrency:
  group: pr-${{ github.event.pull_request.number }}
  cancel-in-progress: true
```

**Pattern 2: One Deploy Per Environment**

```yaml
concurrency:
  group: deploy-${{ inputs.environment }}
  cancel-in-progress: false  # Queue
```

**Pattern 3: Single Cron Job**

```yaml
concurrency:
  group: nightly-maintenance
  cancel-in-progress: true  # Skip if still running
```

---

## Artifact Management

### Upload Artifacts

**Basic Upload:**

```yaml
- name: Upload build artifacts
  uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: dist/
    retention-days: 5
```

**Multiple Paths:**

```yaml
- name: Upload artifacts
  uses: actions/upload-artifact@v4
  with:
    name: release-assets
    path: |
      dist/
      docs/
      !dist/**/*.md
```

**Custom Retention:**

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: coverage-report
    path: coverage/
    retention-days: 30  # Max: repository setting (default 90)
```

### Download Artifacts

**Download Specific Artifact:**

```yaml
- name: Download build
  uses: actions/download-artifact@v5
  with:
    name: build-output
```

**Download All Artifacts:**

```yaml
- name: Download all artifacts
  uses: actions/download-artifact@v5
  # No 'name' parameter - downloads all
```

**Download to Specific Path:**

```yaml
- uses: actions/download-artifact@v5
  with:
    name: build-output
    path: ./artifacts/
```

### Artifact Patterns

**Pattern 1: Build → Test (Same Workflow)**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v5
        with:
          name: dist
      - run: npm test
```

**Pattern 2: Multi-Platform Builds**

```yaml
jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build-${{ matrix.os }}
          path: dist/

  release:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v5  # Download all
      - name: Create release
        run: ./create-release.sh
```

**Pattern 3: Test Results**

```yaml
- name: Run tests
  run: npm test -- --coverage

- name: Upload coverage
  uses: actions/upload-artifact@v4
  with:
    name: coverage
    path: coverage/
    retention-days: 7

- name: Upload test results
  if: always()  # Upload even if tests fail
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: test-results.xml
```

---

## Recommended Tools and Actions

### Essential GitHub Actions

**1. actions/checkout@v5**
- **Purpose:** Clone repository
- **Trust:** Official GitHub action
- **Best Practice:** Pin to SHA, use `fetch-depth: 1` for speed

```yaml
- uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608  # v5.0.0
  with:
    fetch-depth: 1  # Shallow clone
```

**2. actions/setup-node@v4**
- **Purpose:** Setup Node.js environment
- **Features:** Built-in caching for npm/yarn/pnpm
- **Trust:** Official GitHub action

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'
```

**3. actions/cache@v4**
- **Purpose:** Cache dependencies and build outputs
- **Trust:** Official GitHub action
- **Use When:** Need custom cache keys or paths

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
```

**4. actions/upload-artifact@v4 / actions/download-artifact@v5**
- **Purpose:** Share data between jobs
- **Trust:** Official GitHub actions
- **Retention:** Default 90 days (configurable per repo)

**5. docker/build-push-action@v5**
- **Purpose:** Build and push Docker images
- **Features:** BuildKit caching, multi-platform builds
- **Trust:** Official Docker action

### Useful Third-Party Actions

**1. peter-evans/create-pull-request@v5**
- **Purpose:** Create PRs from workflow changes
- **Use Case:** Automated dependency updates, code generation
- **Trust:** Highly trusted community action (6K+ stars)

**2. codecov/codecov-action@v3**
- **Purpose:** Upload code coverage reports
- **Trust:** Official Codecov action

**3. google-github-actions/auth@v2**
- **Purpose:** Authenticate to Google Cloud via OIDC
- **Trust:** Official Google action

**4. aws-actions/configure-aws-credentials@v4**
- **Purpose:** Configure AWS credentials via OIDC
- **Trust:** Official AWS action

**5. docker/setup-buildx-action@v3**
- **Purpose:** Setup Docker Buildx for advanced builds
- **Trust:** Official Docker action

### Action Verification

**Before Using Third-Party Actions:**
1. Check GitHub Stars and Usage (>1K stars = widely trusted)
2. Review Source Code (look for malicious behavior)
3. Pin to Commit SHA (not tag)
4. Enable Dependabot for updates
5. Check Security Advisories

---

## Skill Structure Design

### Proposed File Structure

```
writing-github-actions/
├── SKILL.md                          # Main skill file (<500 lines)
├── references/
│   ├── workflow-syntax.md            # Complete YAML syntax reference
│   ├── reusable-workflows.md         # Reusable workflow patterns
│   ├── composite-actions.md          # Composite action guide
│   ├── caching-strategies.md         # Caching patterns and optimization
│   ├── security-practices.md         # Security best practices
│   ├── triggers-events.md            # All trigger types and filters
│   └── marketplace-actions.md        # Recommended actions
├── examples/
│   ├── basic-ci.yml                  # Simple CI workflow
│   ├── matrix-build.yml              # Matrix strategy examples
│   ├── reusable-deploy.yml           # Reusable deployment workflow
│   ├── composite-setup/              # Composite action example
│   │   └── action.yml
│   ├── monorepo-workflow.yml         # Monorepo with path filters
│   └── security-scan.yml             # Security scanning workflow
├── scripts/
│   └── validate-workflow.sh          # Validate YAML syntax
└── assets/
    └── decision-trees.md             # Visual decision frameworks
```

### SKILL.md Content Outline

**Target Length:** 400-500 lines

**Structure:**
1. **Purpose** (50 lines)
   - What is GitHub Actions
   - When to use this skill
   - Relationship to other skills

2. **Quick Start** (100 lines)
   - Minimal CI workflow
   - Common triggers
   - Basic syntax patterns

3. **Decision Frameworks** (100 lines)
   - Workflow vs Reusable vs Composite
   - Caching strategy selection
   - Self-hosted vs GitHub-hosted runners

4. **Common Patterns** (150 lines)
   - Multi-job workflows
   - Matrix builds
   - Conditional execution
   - Artifact passing

5. **Best Practices** (100 lines)
   - Security (secrets, OIDC, pinning)
   - Optimization (caching, parallelization)
   - Concurrency control

6. **Progressive Disclosure** (50 lines)
   - Links to reference docs
   - When to use scripts
   - Advanced topics signposting

### Progressive Disclosure Strategy

**Level 1: SKILL.md (Always Loaded)**
- Core concepts and quick start
- Decision frameworks (which pattern to use)
- Links to detailed references

**Level 2: References (Loaded on Demand)**
- `workflow-syntax.md` - Complete YAML reference
- `reusable-workflows.md` - Advanced reusable workflow patterns
- `composite-actions.md` - Composite action deep dive
- `caching-strategies.md` - Caching optimization techniques
- `security-practices.md` - Comprehensive security guide

**Level 3: Examples (Loaded as Needed)**
- Working YAML files for copy/paste
- Composite action templates
- Scripts for validation

**Why This Structure:**
- SKILL.md provides "enough to start"
- References provide "deep knowledge"
- Examples provide "copy/paste solutions"
- Scripts provide "validation and safety"

---

## Integration Points

### With Other Skills

**1. building-ci-pipelines**
- **Relationship:** Uses GitHub Actions as execution engine
- **Integration:** This skill provides syntax, that skill provides strategy
- **Handoff:** Pipeline design → GitHub Actions implementation

**2. gitops-workflows**
- **Relationship:** GitHub Actions triggers GitOps deployments
- **Integration:** Workflows push to GitOps repos (ArgoCD, Flux)
- **Example:** Build → Push Image → Update GitOps Manifest

**3. infrastructure-as-code**
- **Relationship:** GitHub Actions executes Terraform/Pulumi
- **Integration:** Workflows run `terraform apply`, manage state
- **Actions:** `hashicorp/setup-terraform`, `pulumi/actions`

**4. testing-strategies**
- **Relationship:** GitHub Actions runs tests
- **Integration:** Workflows execute test suites, upload coverage
- **Actions:** `codecov/codecov-action`, test framework integrations

**5. security-hardening**
- **Relationship:** GitHub Actions performs security scans
- **Integration:** SAST/DAST tools, dependency scanning, image scanning
- **Actions:** `github/codeql-action`, `aquasecurity/trivy-action`

**6. deploying-applications**
- **Relationship:** GitHub Actions deploys applications
- **Integration:** CD workflows for containers, serverless, static sites
- **Actions:** Cloud provider actions (AWS, Azure, GCP)

**7. secret-management**
- **Relationship:** GitHub Actions accesses secrets
- **Integration:** GitHub Secrets, OIDC, external secret managers
- **Actions:** `aws-actions/configure-aws-credentials`, vault integration

### GitHub Ecosystem Integration

**GitHub Features:**
- **Pull Requests:** Status checks, review automation
- **Issues:** Auto-labeling, project management
- **Releases:** Automated release creation, asset uploads
- **Packages:** Publish to GitHub Container Registry, npm
- **Projects:** Update project boards from workflows
- **Discussions:** Automation via GraphQL API

**GitHub Apps:**
- Dependabot (dependency updates)
- CodeQL (security scanning)
- Copilot (workflow suggestions)

---

## Implementation Roadmap

### Phase 1: Core Skill (Week 1)

**Deliverables:**
- [ ] SKILL.md (400-500 lines)
  - Purpose and scope
  - Quick start guide
  - Decision frameworks
  - Common patterns
  - Best practices summary
- [ ] `references/workflow-syntax.md` (200 lines)
- [ ] `examples/basic-ci.yml`
- [ ] `examples/matrix-build.yml`

**Focus:** Get developers writing workflows quickly

### Phase 2: Reusability (Week 2)

**Deliverables:**
- [ ] `references/reusable-workflows.md` (250 lines)
- [ ] `references/composite-actions.md` (200 lines)
- [ ] `examples/reusable-deploy.yml`
- [ ] `examples/composite-setup/action.yml`

**Focus:** Code reuse and standardization

### Phase 3: Optimization (Week 3)

**Deliverables:**
- [ ] `references/caching-strategies.md` (200 lines)
- [ ] Concurrency patterns in SKILL.md
- [ ] `examples/monorepo-workflow.yml`
- [ ] `scripts/validate-workflow.sh`

**Focus:** Performance and cost optimization

### Phase 4: Security (Week 4)

**Deliverables:**
- [ ] `references/security-practices.md` (300 lines)
- [ ] OIDC examples for AWS/Azure/GCP
- [ ] `examples/security-scan.yml`
- [ ] Action pinning recommendations

**Focus:** Production-ready security

### Phase 5: Advanced Topics (Week 5)

**Deliverables:**
- [ ] Self-hosted runners guide
- [ ] Dynamic matrix strategies
- [ ] Cross-repository workflows
- [ ] `references/marketplace-actions.md`

**Focus:** Advanced use cases

### Phase 6: Polish (Week 6)

**Deliverables:**
- [ ] Comprehensive testing across examples
- [ ] Decision trees visualization
- [ ] Integration with other skills documented
- [ ] Validation scripts tested

**Focus:** Production readiness

---

## Success Metrics

### Skill Effectiveness

**Qualitative:**
- Can developers write a basic CI workflow in <5 minutes?
- Can they choose between reusable workflow vs composite action?
- Do they understand caching strategies?
- Do they follow security best practices?

**Quantitative:**
- Workflow creation time (baseline vs with skill)
- Error rate in workflows (syntax errors, logical errors)
- Optimization adoption (caching, parallelization)
- Security score (pinned actions, OIDC usage, minimal permissions)

### Skill Quality

**Checklist (from skill_best_practice.md):**
- [ ] SKILL.md under 500 lines
- [ ] Progressive disclosure used
- [ ] Examples are concrete, not abstract
- [ ] Consistent terminology
- [ ] No time-sensitive information
- [ ] File references one level deep
- [ ] Scripts solve problems (validation)
- [ ] Tested with real workflows

---

## Notes and Considerations

### Key Insights from Research

**1. Reusable Workflows vs Composite Actions**
- Most developers confused about when to use which
- Clear decision framework needed
- Both have valid use cases

**2. Caching is Critical**
- Setup actions have built-in caching (use that first)
- Manual caching for advanced cases only
- Cache key strategy is often overcomplicated

**3. Security Often Overlooked**
- Tag pinning vs SHA pinning
- OIDC adoption still low (opportunity to educate)
- Minimal permissions rarely set

**4. Matrix Builds Powerful but Underutilized**
- Most teams use static matrices only
- Dynamic matrices enable powerful patterns
- Fail-fast default can hide issues

### Common Pitfalls to Address

**1. YAML Syntax Errors**
- Provide validation script
- Common mistakes reference

**2. Workflow Naming Confusion**
- `name:` vs `jobs.<job_id>` vs `steps.name`
- Clear examples needed

**3. Context Variable Confusion**
- `${{ }}` syntax
- When to use `env:` vs direct reference
- `secrets.` vs `inputs.` vs `github.`

**4. Artifact Misuse**
- Retention costs
- When to use artifacts vs cache
- Cross-workflow artifact access

### Future-Proofing

**Emerging Trends (2025+):**
- AI-generated workflows (Copilot integration)
- Deeper cloud integrations (native OIDC)
- Low-code workflow builders
- Enhanced security features (signed workflows)

**Skill Maintenance:**
- Update quarterly for new GitHub features
- Monitor marketplace for new essential actions
- Track GitHub Actions roadmap
- Community feedback integration

---

## Conclusion

This skill provides comprehensive coverage of GitHub Actions, from basic workflows to advanced patterns like reusable workflows, composite actions, and optimization strategies. The progressive disclosure structure ensures developers get started quickly while having access to deep technical knowledge when needed.

**Key Success Factors:**
1. **Clear Decision Frameworks** - Know which pattern to use when
2. **Working Examples** - Copy/paste templates that actually work
3. **Security by Default** - Best practices baked into examples
4. **Optimization Guidance** - Faster, cheaper workflows
5. **Integration Points** - Works with other skills seamlessly

**Next Steps:**
1. Implement Phase 1 (Core Skill)
2. Validate with real workflows
3. Gather feedback from developers
4. Iterate based on usage patterns
5. Expand to advanced topics

---

**Document Version:** 1.0
**Last Updated:** December 3, 2025
**Skill Status:** Master Plan Complete → Ready for Implementation
