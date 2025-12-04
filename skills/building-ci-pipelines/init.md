# Building CI Pipelines - Master Plan

**Skill Name:** `building-ci-pipelines`
**Skill Level:** Mid Level (5,000-8,000 tokens)
**Last Updated:** December 3, 2025
**Status:** Master Plan (init.md) - Ready for SKILL.md implementation

---

## Strategic Positioning

### The CI/CD Construction Gap

While many developers can write application code, **constructing robust, secure, and efficient CI/CD pipelines remains a specialized skill**. This gap leads to:

- **Security vulnerabilities**: Secrets leakage, unsigned artifacts, supply chain attacks
- **Wasted compute**: Rebuilding unchanged code, missing cache opportunities
- **Slow feedback loops**: Sequential pipelines that could run in parallel
- **Monorepo nightmares**: Full rebuilds on every commit regardless of changes
- **SLSA compliance failures**: Inability to meet supply chain security standards

### Why This Skill is Critical (2025)

**1. Supply Chain Security is Non-Negotiable**
- SLSA Framework (Supply-chain Levels for Software Artifacts) is now standard
- Provenance attestations required for production deployments
- GitHub/GitLab native support for SLSA Build Level 3
- Software Bill of Materials (SBOM) generation mandatory

**2. Cost Optimization Through Smart Pipelines**
- Monorepo pipelines can save 60-80% CI minutes with proper affected detection
- Remote caching (Turborepo/Nx) eliminates redundant builds across team
- Matrix parallelization reduces wall-clock time by 5-10x

**3. Developer Experience**
- Fast feedback loops (<5 min for common workflows)
- Clear failure signals with granular job separation
- Reproducible builds (same inputs → same outputs)

**4. Platform Diversity**
- GitHub Actions (most popular, 87.7 trust score, 2912+ snippets)
- GitLab CI (integrated with GitLab ecosystem)
- Jenkins (legacy enterprise, Groovy pipelines)
- Argo Workflows/Tekton (Kubernetes-native, cloud-native)

### Integration with Existing Skills

**Upstream Dependencies:**
- `testing-strategies` → Test execution in CI
- `auth-security` → Secrets management, OIDC federation

**Downstream Consumers:**
- `deploying-applications` → GitOps automation (ArgoCD/Flux)
- `observability` → Pipeline monitoring and alerting

**Parallel Skills:**
- `api-patterns` → API testing in pipelines
- `databases-*` → Database migration testing

---

## CI/CD Platform Decision Framework

### Decision Tree: Which Platform?

```
WHAT'S YOUR PRIMARY HOSTING PLATFORM?

├── GITHUB.COM → GitHub Actions
│   ✅ Native integration, best DX
│   ✅ SLSA Build Level 3 native support
│   ✅ Reusable workflows, composite actions
│   ✅ Matrix strategy for multi-language/OS
│   📊 Context7: /websites/github_en_actions (Trust: High, Snippets: 2912, Score: 87.7)
│
├── GITLAB.COM or SELF-HOSTED GITLAB → GitLab CI
│   ✅ Integrated with GitLab repos
│   ✅ Dependency scanning, SAST built-in
│   ✅ Parent-child pipelines for monorepos
│   ✅ Runner isolation for security
│
├── KUBERNETES CLUSTER → Argo Workflows or Tekton
│   ✅ Cloud-native, runs on K8s
│   ✅ DAG-based workflows (Argo)
│   ✅ Event-driven pipelines
│   📊 Context7: /argoproj/argo-workflows (Trust: High, Snippets: 788)
│
└── LEGACY ENTERPRISE → Jenkins
    ✅ Mature plugin ecosystem
    ✅ Groovy-based pipelines
    ⚠️  Higher maintenance overhead
    ⚠️  Requires self-hosted infrastructure

REPOSITORY STRUCTURE?

├── MONOREPO → Affected Detection CRITICAL
│   ├─ Turborepo (JavaScript/TypeScript)
│   ├─ Nx (JavaScript/TypeScript/Python/Go)
│   └─ Bazel (Multi-language, Google-scale)
│
└── POLYREPO → Standard CI patterns
    └─ Per-repo workflows
```

### Platform Comparison Matrix

| Feature | GitHub Actions | GitLab CI | Argo Workflows | Jenkins |
|---------|---------------|-----------|----------------|---------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **SLSA Support** | ⭐⭐⭐⭐⭐ Native | ⭐⭐⭐ Possible | ⭐⭐⭐⭐ Good | ⭐⭐ Manual |
| **Secrets Mgmt** | ⭐⭐⭐⭐⭐ OIDC | ⭐⭐⭐⭐ Vault | ⭐⭐⭐⭐ K8s Secrets | ⭐⭐⭐ Credentials |
| **Caching** | ⭐⭐⭐⭐ actions/cache | ⭐⭐⭐⭐ cache:paths | ⭐⭐⭐ Volumes | ⭐⭐⭐ Plugins |
| **Matrix Builds** | ⭐⭐⭐⭐⭐ Native | ⭐⭐⭐⭐ Parallel | ⭐⭐⭐ Loops | ⭐⭐⭐⭐ Matrix |
| **Cost** | Free (public), $0.008/min (private) | Free (GitLab.com), Self-hosted | Self-hosted | Self-hosted |
| **Monorepo** | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Manual | ⭐⭐⭐ Plugins |
| **Multi-Language** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## CI/CD Pipeline Pattern Taxonomy

### 1. Basic CI Patterns

#### Pattern 1.1: Lint → Test → Build
**When to Use:** Small projects, single language, <10 contributors

```yaml
# GitHub Actions Example
name: Basic CI
on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint code
        run: npm run lint

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: npm run build
```

**GitLab CI Equivalent:**
```yaml
stages:
  - lint
  - test
  - build

lint:
  stage: lint
  script: npm run lint

test:
  stage: test
  script: npm test

build:
  stage: build
  script: npm run build
```

#### Pattern 1.2: Matrix Strategy (Multi-Language/OS)
**When to Use:** Libraries supporting multiple platforms/versions

```yaml
# GitHub Actions - Matrix for Node.js versions & OS
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

**Parallelization Benefit:** 9 jobs (3 OS × 3 Node versions) run simultaneously
**Wall-clock time:** ~5 minutes vs 45 minutes sequential

---

### 2. Monorepo CI Patterns

#### Pattern 2.1: Affected Detection (Turborepo)
**When to Use:** JavaScript/TypeScript monorepo with Turborepo

```yaml
# GitHub Actions - Turborepo with Remote Caching
name: CI
on:
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full git history for affected detection

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      # Turborepo Remote Caching (Vercel)
      - name: Build affected packages
        run: npx turbo run build --filter='...[origin/main]'
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ vars.TURBO_TEAM }}
```

**Key Concepts:**
- `--filter='...[origin/main]'`: Only build packages changed since main
- Remote caching: Share build artifacts across CI runs and developers
- **Performance:** 60-80% reduction in CI minutes for typical monorepos

#### Pattern 2.2: Nx Affected with Cloud Caching
**When to Use:** Nx monorepo (supports TypeScript, Python, Go, Rust)

```yaml
# GitHub Actions - Nx Affected
name: CI
on: [pull_request]

jobs:
  affected:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Derive appropriate SHAs for base and head
        id: setSHAs
        uses: nrwl/nx-set-shas@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - run: npm ci

      - name: Run affected tests
        run: npx nx affected -t test --base=${{ steps.setSHAs.outputs.base }} --head=${{ steps.setSHAs.outputs.head }}
        env:
          NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}
```

**Affected Detection Logic:**
1. Compare current branch against main branch
2. Build dependency graph of packages
3. Identify packages with direct changes OR dependencies on changed packages
4. Run tasks only for affected packages

#### Pattern 2.3: GitLab Parent-Child Pipelines (Monorepo)
**When to Use:** GitLab-hosted monorepo, team-based ownership

```yaml
# .gitlab-ci.yml (Parent)
stages:
  - generate
  - deploy

generate-child-pipeline:
  stage: generate
  script:
    # Generate child pipeline YAML based on changed files
    - python scripts/generate_pipeline.py > child-pipeline.yml
  artifacts:
    paths:
      - child-pipeline.yml

trigger-child:
  stage: deploy
  trigger:
    include:
      - artifact: child-pipeline.yml
        job: generate-child-pipeline
    strategy: depend
```

**Benefits:**
- Independent failure isolation (frontend team vs backend team)
- Parallel execution across teams
- Different deployment cadences per service

---

### 3. Security Patterns (SLSA Framework)

#### Pattern 3.1: SLSA Build Level 3 (GitHub Actions)
**When to Use:** Production deployments requiring supply chain security

**SLSA Levels Overview:**
- **Level 1**: Provenance exists (basic record of build)
- **Level 2**: Hosted build service with tamper-resistant provenance
- **Level 3**: Hardened build platforms + non-falsifiable provenance (RECOMMENDED)
- **Level 4**: Two-party review + hermetic builds (future state)

```yaml
# GitHub Actions - SLSA Level 3 Provenance
name: SLSA Build
on:
  push:
    tags: ['v*']

permissions:
  id-token: write  # For OIDC token
  contents: read
  packages: write

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@v4

      - name: Build container
        id: build
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}

  # Generate SLSA provenance attestation
  provenance:
    needs: build
    permissions:
      id-token: write
      actions: read
      packages: write
    uses: slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml@v1.10.0
    with:
      image: ghcr.io/${{ github.repository }}
      digest: ${{ needs.build.outputs.digest }}
      registry-username: ${{ github.actor }}
    secrets:
      registry-password: ${{ secrets.GITHUB_TOKEN }}
```

**What This Provides:**
- Cryptographically signed provenance (who built, when, from what source)
- Tamper-evident build record
- Verifiable chain of custody from source → artifact

**Verification Example:**
```bash
# Verify SLSA provenance before deployment
cosign verify-attestation \
  --type slsaprovenance \
  --certificate-identity-regexp "^https://github.com/slsa-framework" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  ghcr.io/myorg/myapp@sha256:abcd1234...
```

#### Pattern 3.2: Secrets Management (OIDC Federation)
**When to Use:** AWS/GCP/Azure deployments without long-lived credentials

**The Problem with Traditional Secrets:**
- Long-lived credentials in GitHub Secrets
- Rotation is manual and error-prone
- Risk of exposure if secrets leaked

**The Solution: OIDC Workload Identity Federation**

```yaml
# GitHub Actions - OIDC for AWS (No AWS Access Keys!)
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # Required for OIDC token
      contents: read
    steps:
      - uses: actions/checkout@v4

      # Get temporary credentials from AWS using OIDC
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          aws-region: us-east-1

      # Now you have temporary AWS credentials (valid ~1 hour)
      - name: Deploy to S3
        run: aws s3 sync ./dist s3://my-bucket
```

**Setup (AWS Side):**
1. Create IAM OIDC Identity Provider (GitHub: `token.actions.githubusercontent.com`)
2. Create IAM Role with trust policy:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
    },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "token.actions.githubusercontent.com:sub": "repo:myorg/myrepo:ref:refs/heads/main"
      }
    }
  }]
}
```

**Benefits:**
- ✅ No long-lived credentials stored in GitHub
- ✅ Credentials auto-rotate (1-hour lifetime)
- ✅ Fine-grained permissions per branch/environment
- ✅ Audit trail via CloudTrail

#### Pattern 3.3: Secret Scanning & Dependency Scanning
**When to Use:** ALL projects (security baseline)

```yaml
# GitHub Actions - Secret Scanning
name: Security
on: [push, pull_request]

jobs:
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for detecting secrets

      - name: Gitleaks Secret Scanning
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  dependency-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Snyk to check for vulnerabilities
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          format: spdx-json
          output-file: sbom.spdx.json

      - name: Upload SBOM
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.spdx.json
```

---

### 4. Caching Strategies

#### Pattern 4.1: GitHub Actions Cache
**When to Use:** Node.js, Python, Go, Rust dependency caching

```yaml
# Node.js with npm cache
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'  # Automatic npm cache

      - run: npm ci
      - run: npm test
```

**Manual Cache Control (Advanced):**
```yaml
steps:
  - uses: actions/checkout@v4

  - name: Cache dependencies
    uses: actions/cache@v4
    with:
      path: |
        ~/.cargo/bin
        ~/.cargo/registry/index
        ~/.cargo/registry/cache
        ~/.cargo/git/db
        target/
      key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
      restore-keys: |
        ${{ runner.os }}-cargo-

  - run: cargo build --release
```

**Cache Hit Rate Optimization:**
- Use specific cache keys: `${{ hashFiles('**/Cargo.lock') }}`
- Provide restore-keys fallback: `${{ runner.os }}-cargo-`
- Cache size limit: 10GB per repository (GitHub Actions)

#### Pattern 4.2: Multi-Layer Caching (Nx)
**When to Use:** Complex build pipelines with multiple cache layers

```yaml
# Multiple cache layers for Nx monorepo
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Layer 1: Nx Cache (build outputs)
      - name: Nx Cloud
        env:
          NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}
        run: npx nx affected -t build

      # Layer 2: Vite Cache (for Vite projects)
      - uses: actions/cache@v4
        with:
          path: '**/node_modules/.vite'
          key: vite-${{ hashFiles('**/package-lock.json') }}

      # Layer 3: TypeScript Cache
      - uses: actions/cache@v4
        with:
          path: '**/tsconfig.tsbuildinfo'
          key: tsc-${{ hashFiles('**/tsconfig.json') }}
```

**Why Multiple Layers?**
- Nx Cache: Stores final build outputs (dist/, build/)
- Vite Cache: Stores HMR state, dependency pre-bundling
- TS Cache: Incremental compilation info
- **Result:** 70-90% reduction in build time on cache hit

---

### 5. Parallelization Patterns

#### Pattern 5.1: Job-Level Parallelization
**When to Use:** Independent test suites, multi-platform builds

```yaml
# GitHub Actions - Parallel Jobs
jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run test:unit

  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run test:integration

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run test:e2e

  # All three run in parallel (default behavior)
```

**Argo Workflows - DAG Parallelization:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: parallel-tests-
spec:
  entrypoint: main
  templates:
  - name: main
    dag:
      tasks:
      - name: unit-tests
        template: run-tests
        arguments:
          parameters: [{name: type, value: unit}]

      - name: integration-tests
        template: run-tests
        arguments:
          parameters: [{name: type, value: integration}]

      - name: e2e-tests
        template: run-tests
        arguments:
          parameters: [{name: type, value: e2e}]

      # Run after all tests pass
      - name: deploy
        dependencies: [unit-tests, integration-tests, e2e-tests]
        template: deploy-app

  - name: run-tests
    inputs:
      parameters:
      - name: type
    container:
      image: node:20
      command: [npm, run, "test:{{inputs.parameters.type}}"]
```

**Diamond DAG Pattern:**
```
        lint
         │
    ┌────┴────┐
    │         │
   test     build
    │         │
    └────┬────┘
         │
       deploy
```

#### Pattern 5.2: Test Sharding (Parallel Test Execution)
**When to Use:** Large test suites (>5 minutes runtime)

```yaml
# GitHub Actions - Sharded Tests
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4
      - run: npm test -- --shard=${{ matrix.shard }}/4
```

**Jest Sharding Example:**
```bash
# Shard 1/4: Tests files 1-25
# Shard 2/4: Test files 26-50
# Shard 3/4: Test files 51-75
# Shard 4/4: Test files 76-100

jest --shard=1/4
```

**Performance:**
- 100 test files, 20 minutes total
- 4 shards = 5 minutes wall-clock time
- **4x speedup**

---

### 6. Reusable Workflow Patterns

#### Pattern 6.1: Composite Actions (GitHub)
**When to Use:** Shared setup logic across workflows

```yaml
# .github/actions/setup-node-with-cache/action.yml
name: Setup Node with Cache
description: Setup Node.js with dependency caching
inputs:
  node-version:
    description: Node.js version
    required: false
    default: '20'
runs:
  using: composite
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'

    - run: npm ci
      shell: bash

    - run: echo "Node.js ${{ inputs.node-version }} ready"
      shell: bash
```

**Usage in Workflow:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-node-with-cache
        with:
          node-version: '20'
      - run: npm run build
```

#### Pattern 6.2: Reusable Workflows (GitHub)
**When to Use:** Complete workflow templates shared across repos

```yaml
# .github/workflows/reusable-deploy.yml
name: Reusable Deploy
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      node-version:
        required: false
        type: string
        default: '20'
    secrets:
      deploy-token:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci
      - run: npm run build
      - run: npm run deploy
        env:
          DEPLOY_TOKEN: ${{ secrets.deploy-token }}
```

**Calling Reusable Workflow:**
```yaml
# .github/workflows/production.yml
name: Production Deploy
on:
  push:
    branches: [main]

jobs:
  deploy-prod:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: production
      node-version: '20'
    secrets:
      deploy-token: ${{ secrets.PRODUCTION_DEPLOY_TOKEN }}
```

**Benefits:**
- DRY principle (Don't Repeat Yourself)
- Centralized updates (fix once, apply everywhere)
- Consistent deploy process across environments

---

## Language-Specific Patterns

### Python CI Pipeline

```yaml
# GitHub Actions - Python with Poetry
name: Python CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Cache Poetry dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pypoetry
          key: poetry-${{ hashFiles('**/poetry.lock') }}

      - name: Install Poetry
        run: pipx install poetry

      - name: Install dependencies
        run: poetry install

      - name: Lint with ruff
        run: poetry run ruff check .

      - name: Type check with mypy
        run: poetry run mypy .

      - name: Test with pytest
        run: poetry run pytest --cov=. --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
```

### Rust CI Pipeline

```yaml
# GitHub Actions - Rust with Cargo
name: Rust CI
on: [push, pull_request]

env:
  CARGO_TERM_COLOR: always

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        rust: [stable, nightly]
    steps:
      - uses: actions/checkout@v4

      - uses: dtolnay/rust-toolchain@master
        with:
          toolchain: ${{ matrix.rust }}
          components: rustfmt, clippy

      - uses: Swatinem/rust-cache@v2
        with:
          cache-on-failure: true

      - name: Check formatting
        run: cargo fmt -- --check

      - name: Clippy
        run: cargo clippy -- -D warnings

      - name: Build
        run: cargo build --verbose

      - name: Test
        run: cargo test --verbose
```

### Go CI Pipeline

```yaml
# GitHub Actions - Go
name: Go CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-go@v5
        with:
          go-version: '1.23'
          cache: true

      - name: Verify dependencies
        run: go mod verify

      - name: Lint
        uses: golangci/golangci-lint-action@v4
        with:
          version: latest

      - name: Build
        run: go build -v ./...

      - name: Test
        run: go test -v -race -coverprofile=coverage.txt -covermode=atomic ./...

      - name: Upload coverage
        uses: codecov/codecov-action@v4
```

### TypeScript (Node.js) CI Pipeline

```yaml
# GitHub Actions - Node.js with pnpm
name: Node.js CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v3
        with:
          version: 8

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Lint
        run: pnpm run lint

      - name: Type check
        run: pnpm run type-check

      - name: Test
        run: pnpm run test

      - name: Build
        run: pnpm run build
```

---

## Advanced Patterns

### Pattern: Dynamic Pipeline Generation (GitLab)

**When to Use:** Large monorepos where pipeline definition exceeds YAML limits

```yaml
# .gitlab-ci.yml
stages:
  - generate
  - test
  - deploy

generate-pipeline:
  stage: generate
  image: python:3.12
  script:
    # Python script analyzes changed files and generates child pipeline
    - python scripts/generate_pipeline.py > generated-pipeline.yml
  artifacts:
    paths:
      - generated-pipeline.yml

trigger-child:
  stage: test
  trigger:
    include:
      - artifact: generated-pipeline.yml
        job: generate-pipeline
    strategy: depend
```

**Python Script Logic:**
```python
# scripts/generate_pipeline.py
import subprocess
import yaml

def get_changed_packages():
    """Get list of changed packages since main branch"""
    result = subprocess.run(
        ['git', 'diff', '--name-only', 'origin/main'],
        capture_output=True, text=True
    )
    changed_files = result.stdout.strip().split('\n')

    # Extract package names from paths
    packages = set()
    for file in changed_files:
        if file.startswith('packages/'):
            pkg = file.split('/')[1]
            packages.add(pkg)

    return list(packages)

def generate_pipeline():
    packages = get_changed_packages()

    pipeline = {
        'stages': ['test', 'build'],
        'jobs': {}
    }

    for pkg in packages:
        pipeline['jobs'][f'test-{pkg}'] = {
            'stage': 'test',
            'script': [f'cd packages/{pkg}', 'npm test']
        }
        pipeline['jobs'][f'build-{pkg}'] = {
            'stage': 'build',
            'script': [f'cd packages/{pkg}', 'npm run build'],
            'needs': [f'test-{pkg}']
        }

    print(yaml.dump(pipeline))

if __name__ == '__main__':
    generate_pipeline()
```

### Pattern: Container Build with Multi-Stage Caching

```yaml
# GitHub Actions - Docker Build with Layer Caching
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=registry,ref=ghcr.io/${{ github.repository }}:buildcache
          cache-to: type=registry,ref=ghcr.io/${{ github.repository }}:buildcache,mode=max
```

**Dockerfile (Multi-Stage Build):**
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Cache Optimization:**
- Layer 1: `package*.json` (changes infrequently)
- Layer 2: `npm ci` (reuses layer if package.json unchanged)
- Layer 3: Source code (changes frequently)
- **Result:** 80% faster builds on cache hit

---

## Skill Structure Design

### Progressive Disclosure Architecture

```
building-ci-pipelines/
├── SKILL.md                          # Main skill file (500-700 lines)
│   ├── Purpose & When to Use
│   ├── Platform Decision Tree
│   ├── Quick Start Examples (GitHub Actions, GitLab CI)
│   ├── Core Patterns Overview
│   └── References to deeper content
│
├── references/                       # Detailed documentation
│   ├── github-actions-patterns.md   # GitHub Actions deep dive
│   │   ├── Workflow syntax reference
│   │   ├── Reusable workflows & composite actions
│   │   ├── Matrix strategies
│   │   ├── OIDC federation setup
│   │   └── Secrets management best practices
│   │
│   ├── gitlab-ci-patterns.md        # GitLab CI patterns
│   │   ├── Pipeline syntax
│   │   ├── Parent-child pipelines
│   │   ├── Runner configuration
│   │   └── Dependency scanning
│   │
│   ├── argo-workflows-guide.md      # Argo Workflows for Kubernetes
│   │   ├── DAG templates
│   │   ├── WorkflowTemplates vs Workflows
│   │   ├── Artifact passing
│   │   └── Event-driven triggers
│   │
│   ├── jenkins-pipelines.md         # Jenkins (legacy systems)
│   │   ├── Declarative vs Scripted
│   │   ├── Jenkinsfile patterns
│   │   └── Plugin recommendations
│   │
│   ├── slsa-security-framework.md   # SLSA implementation
│   │   ├── SLSA Level 1-4 overview
│   │   ├── Provenance generation
│   │   ├── Attestation verification
│   │   └── Cosign integration
│   │
│   ├── monorepo-ci-strategies.md    # Monorepo patterns
│   │   ├── Turborepo affected detection
│   │   ├── Nx Cloud caching
│   │   ├── Bazel remote execution
│   │   └── Change detection algorithms
│   │
│   ├── caching-strategies.md        # Caching patterns
│   │   ├── GitHub Actions cache
│   │   ├── GitLab CI cache
│   │   ├── Docker layer caching
│   │   ├── Remote caching (Turborepo/Nx)
│   │   └── Multi-layer cache strategies
│   │
│   ├── parallelization-patterns.md  # Parallel execution
│   │   ├── Job-level parallelization
│   │   ├── Matrix strategies
│   │   ├── Test sharding
│   │   └── DAG-based workflows
│   │
│   └── secrets-management.md        # Security patterns
│       ├── OIDC workload identity (AWS/GCP/Azure)
│       ├── Vault integration
│       ├── Encrypted secrets
│       └── Secret rotation strategies
│
├── examples/                         # Complete runnable examples
│   ├── github-actions-basic/
│   │   ├── .github/workflows/ci.yml
│   │   └── README.md
│   │
│   ├── github-actions-monorepo/
│   │   ├── .github/workflows/ci.yml  # Turborepo example
│   │   ├── turbo.json
│   │   └── README.md
│   │
│   ├── github-actions-slsa/
│   │   ├── .github/workflows/release.yml  # SLSA Level 3
│   │   └── README.md
│   │
│   ├── gitlab-ci-monorepo/
│   │   ├── .gitlab-ci.yml  # Parent-child pattern
│   │   ├── scripts/generate_pipeline.py
│   │   └── README.md
│   │
│   ├── argo-workflows-dag/
│   │   ├── diamond-workflow.yaml
│   │   ├── parallel-tests.yaml
│   │   └── README.md
│   │
│   └── multi-language-matrix/
│       ├── .github/workflows/matrix.yml
│       └── README.md
│
└── scripts/                          # Token-free execution scripts
    ├── generate_github_workflow.py  # Generate workflow from template
    ├── validate_workflow.py         # Validate YAML syntax
    ├── analyze_ci_performance.py    # CI metrics analysis
    └── setup_oidc_aws.py            # AWS OIDC provider setup
```

### SKILL.md Content Breakdown (500-700 lines)

**Section 1: Purpose & When to Use (50 lines)**
- What this skill does
- When to use (triggers)
- Integration with deploying-applications, observability

**Section 2: Platform Decision Tree (100 lines)**
- GitHub Actions vs GitLab CI vs Argo vs Jenkins
- Quick decision framework
- Platform comparison matrix

**Section 3: Quick Start Patterns (150 lines)**
- Basic CI: Lint → Test → Build
- Monorepo: Turborepo affected detection
- Security: SLSA provenance generation
- Each pattern: YAML snippet + explanation

**Section 4: Core Concepts (100 lines)**
- Workflow anatomy
- Jobs, steps, actions
- Matrix strategies
- Caching basics
- Secret management overview

**Section 5: Common Workflows (150 lines)**
- Python pipeline (Poetry)
- Rust pipeline (Cargo)
- Go pipeline
- Node.js pipeline (pnpm)
- Docker build pipeline

**Section 6: Progressive Disclosure (50 lines)**
- Reference to detailed docs
- When to use scripts
- Example directory guide

**Section 7: Best Practices (100 lines)**
- Security checklist
- Performance optimization
- Debugging tips
- Common pitfalls

---

## Library Recommendations (2025)

### CI/CD Platforms

#### **Primary: GitHub Actions**
**Context7 ID:** `/websites/github_en_actions`
**Trust Score:** High
**Code Snippets:** 2,912+
**Benchmark Score:** 87.7

**Why GitHub Actions?**
- Native GitHub integration (pull request checks, GitHub Packages)
- SLSA Build Level 3 native support (best-in-class supply chain security)
- Massive marketplace (10,000+ actions)
- OIDC federation for AWS/GCP/Azure (no long-lived credentials)
- Free for public repos, $0.008/minute for private repos

**When to Use:**
- Hosted on GitHub.com
- Need SLSA provenance attestations
- Want marketplace ecosystem
- Multi-platform builds (Linux/Windows/macOS)

**Example (Basic CI):**
```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

#### **Alternative: GitLab CI**
**Platform:** gitlab.com or self-hosted
**Trust Score:** High

**Why GitLab CI?**
- Integrated with GitLab repos
- Parent-child pipelines (excellent for monorepos)
- Built-in dependency scanning, SAST, DAST
- Runner isolation (security-critical workloads)
- Free for GitLab.com, unlimited CI/CD minutes on self-hosted

**When to Use:**
- Hosted on GitLab
- Need built-in security scanning
- Complex monorepo with team isolation
- Prefer self-hosted runners

**Example (Monorepo Parent-Child):**
```yaml
stages:
  - generate
  - test

generate-child:
  stage: generate
  script:
    - python scripts/generate_pipeline.py > child.yml
  artifacts:
    paths: [child.yml]

trigger-child:
  stage: test
  trigger:
    include:
      - artifact: child.yml
        job: generate-child
```

#### **Cloud-Native: Argo Workflows**
**Context7 ID:** `/argoproj/argo-workflows`
**Trust Score:** High
**Code Snippets:** 788

**Why Argo Workflows?**
- Kubernetes-native (runs on K8s clusters)
- DAG-based workflows (complex dependencies)
- Event-driven (Argo Events integration)
- Workflow-as-Code (CRD-based)

**When to Use:**
- Running on Kubernetes
- Need complex DAG workflows
- Event-driven pipelines (Kafka, webhooks, cron)
- Service mesh integration (Istio/Linkerd)

**Example (Diamond DAG):**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: diamond-
spec:
  entrypoint: main
  templates:
  - name: main
    dag:
      tasks:
      - name: A
        template: echo
      - name: B
        dependencies: [A]
        template: echo
      - name: C
        dependencies: [A]
        template: echo
      - name: D
        dependencies: [B, C]
        template: echo
```

#### **Legacy: Jenkins**
**When to Use:**
- Existing Jenkins infrastructure
- Enterprise on-premises requirements
- Need Java-based plugins

**Recommendation:** Migrate to GitHub Actions or GitLab CI if possible.

---

### Monorepo Tools

#### **Primary (JavaScript/TypeScript): Turborepo**
**Website:** turborepo.org
**Why Turborepo?**
- Zero-config remote caching (Vercel)
- `--filter` for affected packages
- Incremental builds
- Minimal configuration (turbo.json)

**Example (turbo.json):**
```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "cache": false
    }
  }
}
```

**CI Integration:**
```yaml
# GitHub Actions
- run: npx turbo run build --filter='...[origin/main]'
  env:
    TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
    TURBO_TEAM: ${{ vars.TURBO_TEAM }}
```

#### **Alternative (Multi-Language): Nx**
**Why Nx?**
- Supports TypeScript, Python, Go, Rust
- Nx Cloud (distributed caching + task distribution)
- Visual dependency graph
- Affected detection across languages

**Example:**
```bash
# Run tests only for affected projects
npx nx affected -t test --base=origin/main
```

#### **Enterprise (Google-Scale): Bazel**
**When to Use:**
- Massive monorepos (1000+ packages)
- Need hermetic builds
- Multi-language (Java, Go, Rust, Python, C++)

**Note:** Steep learning curve, overkill for most projects.

---

### Security Tools

#### **Secret Scanning: Gitleaks**
**GitHub:** gitleaks/gitleaks-action@v2
**Why Gitleaks?**
- Detects 150+ secret types
- Fast (Go-based)
- Configurable rules
- Pre-commit hooks

**Example:**
```yaml
- name: Gitleaks
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

#### **SBOM Generation: Anchore**
**GitHub:** anchore/sbom-action@v0
**Why Anchore?**
- Generates SPDX, CycloneDX formats
- Integrates with Syft scanner
- Free and open-source

**Example:**
```yaml
- uses: anchore/sbom-action@v0
  with:
    format: spdx-json
    output-file: sbom.spdx.json
```

#### **Provenance: SLSA GitHub Generator**
**GitHub:** slsa-framework/slsa-github-generator
**Version:** v1.10.0
**Why SLSA Generator?**
- SLSA Build Level 3 compliance
- Cryptographically signed provenance
- Container, binary, npm support

**Example:**
```yaml
provenance:
  uses: slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml@v1.10.0
  with:
    image: ghcr.io/${{ github.repository }}
    digest: ${{ needs.build.outputs.digest }}
```

---

## Best Practices & Pitfalls

### Security Best Practices

✅ **DO:**
1. **Use OIDC instead of long-lived credentials**
   - AWS/GCP/Azure support workload identity federation
   - Credentials auto-rotate (1-hour lifetime)
   - No secrets stored in GitHub

2. **Pin action versions to commit SHA**
   ```yaml
   # Good: Immutable reference
   - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1

   # Bad: Mutable reference (v4 could change)
   - uses: actions/checkout@v4
   ```

3. **Restrict GITHUB_TOKEN permissions**
   ```yaml
   permissions:
     contents: read      # Don't give write unless needed
     pull-requests: write  # Only what's necessary
   ```

4. **Scan for secrets on every commit**
   - Use Gitleaks or TruffleHog
   - Block commits with detected secrets

5. **Generate SLSA provenance for releases**
   - Enables supply chain verification
   - Required for compliance (NIST SSDF, PCI DSS 4.0)

❌ **DON'T:**
1. **Store secrets in code or logs**
   ```yaml
   # Bad: Secret exposed in logs
   - run: echo "API_KEY=${{ secrets.API_KEY }}"

   # Good: Use secret in env
   - run: ./deploy.sh
     env:
       API_KEY: ${{ secrets.API_KEY }}
   ```

2. **Use `pull_request_target` without validation**
   - Dangerous for public repos (arbitrary code execution)
   - Always validate fork PRs

3. **Trust third-party actions blindly**
   - Audit source code
   - Use verified publishers
   - Pin to commit SHA

### Performance Best Practices

✅ **DO:**
1. **Use affected detection for monorepos**
   - Turborepo `--filter='...[origin/main]'`
   - Nx `affected -t build`
   - **Result:** 60-80% CI time reduction

2. **Cache aggressively**
   - Dependencies (npm, pip, cargo)
   - Build outputs (dist/, target/)
   - Test results (for flaky test detection)

3. **Parallelize jobs**
   - Run tests, lints, builds in parallel
   - Use matrix strategy for multi-platform

4. **Fail fast**
   ```yaml
   strategy:
     fail-fast: true  # Stop all jobs if one fails
     matrix:
       node-version: [18, 20, 22]
   ```

5. **Use remote caching**
   - Turborepo Remote Cache (Vercel)
   - Nx Cloud
   - GitHub Actions cache (10GB limit)

❌ **DON'T:**
1. **Rebuild everything on every commit**
   - Use affected detection
   - Leverage caching

2. **Run long-running tests in PR checks**
   - PR: Fast tests (<5 min)
   - Post-merge: Full test suite

3. **Ignore cache key optimization**
   ```yaml
   # Bad: Cache invalidates on any file change
   key: ${{ runner.os }}-build

   # Good: Cache invalidates only when dependencies change
   key: ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}
   ```

### Debugging Tips

**GitHub Actions:**
1. **Enable debug logging**
   ```yaml
   env:
     ACTIONS_STEP_DEBUG: true
     ACTIONS_RUNNER_DEBUG: true
   ```

2. **SSH into runner**
   ```yaml
   - name: Setup tmate session
     uses: mxschmitt/action-tmate@v3
   ```

3. **Inspect environment**
   ```yaml
   - run: env | sort
   - run: echo "${{ toJSON(github) }}"
   ```

**GitLab CI:**
1. **Use `artifacts:reports:` for test results**
   ```yaml
   artifacts:
     reports:
       junit: test-results.xml
   ```

2. **Debug with `script: sleep 3600`**
   - SSH into runner before job times out

**Argo Workflows:**
1. **View logs**
   ```bash
   argo logs <workflow-name>
   ```

2. **Debug with retry**
   ```yaml
   retryStrategy:
     limit: 3
     backoff:
       duration: "1m"
   ```

---

## Integration with Other Skills

### Upstream Skills (Dependencies)

**`testing-strategies` → `building-ci-pipelines`**
- Test execution in CI pipelines
- Test sharding for parallel execution
- Coverage reporting (Codecov, Coveralls)

**`auth-security` → `building-ci-pipelines`**
- Secrets management (Vault, AWS Secrets Manager)
- OIDC federation setup
- SLSA provenance verification

### Downstream Skills (Consumers)

**`building-ci-pipelines` → `deploying-applications`**
- GitOps automation (ArgoCD/Flux triggers)
- Container registry pushes
- Deployment triggers (staging → production)

**`building-ci-pipelines` → `observability`**
- Pipeline monitoring (OpenTelemetry)
- Build failure alerting (Slack, PagerDuty)
- CI metrics dashboards (Grafana)

### Parallel Skills (Complementary)

**`api-patterns`**
- API integration testing in CI
- OpenAPI spec validation
- Contract testing (Pact)

**`databases-*`**
- Database migration testing
- Schema validation
- Seed data management

---

## Success Metrics

**Performance:**
- ✅ PR feedback loop <5 minutes (quick checks)
- ✅ Full CI suite <15 minutes (all tests)
- ✅ 60-80% CI time reduction (monorepo affected detection)
- ✅ 70-90% cache hit rate (dependency caching)

**Security:**
- ✅ 100% of releases have SLSA provenance
- ✅ Zero secrets detected in commits (Gitleaks)
- ✅ SBOM generated for all artifacts
- ✅ OIDC federation for cloud deployments (no long-lived credentials)

**Reliability:**
- ✅ <5% flaky test rate
- ✅ 99%+ CI uptime
- ✅ Clear failure signals (granular job separation)

---

## Research Summary

**Google Search Grounding (December 3, 2025):**
- SLSA Framework is industry standard for supply chain security
- GitHub Actions has native SLSA Build Level 3 support
- Monorepo CI strategies critical (Turborepo/Nx affected detection)
- OIDC federation replacing long-lived credentials
- Multi-layer caching (Nx Cache, Vite Cache, TypeScript Cache)

**Context7 Documentation:**
- `/websites/github_en_actions`: 2,912 snippets, 87.7 score
- `/argoproj/argo-workflows`: 788 snippets, Kubernetes-native DAGs
- Reusable workflows, composite actions patterns
- Matrix strategies for multi-platform builds

**Key Findings:**
- CI/CD security is top priority (SLSA, provenance, OIDC)
- Monorepo pipelines need smart caching and affected detection
- Parallelization reduces wall-clock time by 5-10x
- Platform choice depends on hosting (GitHub → Actions, K8s → Argo)

---

## Next Steps: From init.md to SKILL.md

**Phase 1: Create SKILL.md (Week 1)**
1. Write main skill file (500-700 lines)
2. Follow imperative/infinitive style (not second person)
3. Platform decision tree
4. Quick start examples (GitHub Actions, GitLab CI)
5. Core patterns overview

**Phase 2: Write Reference Files (Week 2)**
1. `github-actions-patterns.md` (most popular)
2. `slsa-security-framework.md` (security critical)
3. `monorepo-ci-strategies.md` (high-value optimization)
4. `caching-strategies.md` (performance)

**Phase 3: Create Examples (Week 3)**
1. `github-actions-basic/` (starter template)
2. `github-actions-monorepo/` (Turborepo)
3. `github-actions-slsa/` (SLSA Level 3)
4. `gitlab-ci-monorepo/` (parent-child)

**Phase 4: Write Scripts (Week 4)**
1. `generate_github_workflow.py` (template generator)
2. `validate_workflow.py` (YAML linter)
3. `analyze_ci_performance.py` (metrics)
4. `setup_oidc_aws.py` (OIDC automation)

**Phase 5: Testing & Iteration (Week 5)**
1. Test with Claude Sonnet (balanced)
2. Test with Claude Haiku (needs more guidance?)
3. Real-world task testing
4. Iterate based on observations

---

## Validation Checklist

**Core Quality:**
- [x] Description includes WHAT and WHEN
- [ ] SKILL.md under 500 lines (not created yet)
- [x] No time-sensitive information (2025 references are contextual)
- [x] Consistent terminology (workflow, job, step, action)
- [x] Examples are concrete (real YAML snippets)
- [x] File references one level deep from SKILL.md

**Naming and Structure:**
- [x] Name uses gerund form (`building-ci-pipelines`)
- [x] Name: lowercase, hyphens only, under 64 chars
- [x] Description: under 1024 chars
- [x] File paths use forward slashes

**Content:**
- [x] Platform decision tree
- [x] Pattern taxonomy (basic, monorepo, security, caching, parallelization)
- [x] Multi-language support (Python, Rust, Go, TypeScript)
- [x] Security patterns (SLSA, OIDC, secrets management)
- [x] Performance optimization (caching, affected detection, parallelization)
- [x] Integration with other skills

**Research:**
- [x] Google Search Grounding conducted
- [x] Context7 library resolution (GitHub Actions, Argo Workflows)
- [x] Context7 documentation retrieved
- [x] Trust scores verified
- [x] Code snippets available

---

**This master plan is ready for SKILL.md implementation. The next step is to create the actual skill file following Anthropic's best practices and progressive disclosure patterns.**
