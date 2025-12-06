# Caching Strategies and Optimization

Techniques for optimizing GitHub Actions workflows through caching, parallelization, and resource management.

## Table of Contents

1. [Caching Overview](#caching-overview)
2. [Built-in Setup Action Caching](#built-in-setup-action-caching)
3. [Manual Caching with actions/cache](#manual-caching-with-actionscache)
4. [Cache Key Strategies](#cache-key-strategies)
5. [Docker Layer Caching](#docker-layer-caching)
6. [Parallelization Strategies](#parallelization-strategies)
7. [Workflow Optimization](#workflow-optimization)
8. [Resource Management](#resource-management)

---

## Caching Overview

### What Gets Cached

**Suitable for Caching:**
- Package manager dependencies (npm, pip, maven, etc.)
- Build outputs (compiled code, generated files)
- Downloaded tools and binaries
- Test fixtures and data
- Docker layers

**NOT Suitable for Caching:**
- Secrets or sensitive data
- Very large files (>10GB limit)
- Files that change every run
- OS-specific system files

### Cache Limits

- **Size Limit:** 10GB per repository
- **Retention:** 7 days for unused caches
- **Eviction:** Oldest caches removed when limit reached
- **Access:** Read-only from forks (can't save caches)

### Cache Scope

- **Branch:** Caches created on branch available to that branch and default branch
- **Default Branch:** Caches available to all branches
- **Pull Requests:** Can restore caches from base branch

---

## Built-in Setup Action Caching

Most setup actions include built-in caching. This is the recommended approach.

### Node.js (npm/yarn/pnpm)

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'  # or 'yarn', 'pnpm'
```

**What it Caches:**
- `npm`: `~/.npm`
- `yarn`: `~/.yarn/cache`
- `pnpm`: `~/.pnpm-store`

**Cache Key:** Based on lock file hash

### Python (pip/pipenv/poetry)

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'  # or 'pipenv', 'poetry'
```

**What it Caches:**
- `pip`: `~/.cache/pip`
- `pipenv`: `~/.cache/pipenv`
- `poetry`: `~/.cache/pypoetry`

**Cache Key:** Based on requirements.txt or lock file

### Java (Maven/Gradle)

```yaml
- uses: actions/setup-java@v4
  with:
    java-version: '17'
    distribution: 'temurin'
    cache: 'maven'  # or 'gradle'
```

**What it Caches:**
- `maven`: `~/.m2/repository`
- `gradle`: `~/.gradle/caches`, `~/.gradle/wrapper`

### .NET

```yaml
- uses: actions/setup-dotnet@v4
  with:
    dotnet-version: '6.x'
    cache: true
```

**What it Caches:** NuGet packages

### Go

```yaml
- uses: actions/setup-go@v5
  with:
    go-version: '1.21'
    cache: true
```

**What it Caches:** Go modules and build cache

### Ruby (Bundler)

```yaml
- uses: ruby/setup-ruby@v1
  with:
    ruby-version: '3.2'
    bundler-cache: true
```

---

## Manual Caching with actions/cache

Use `actions/cache@v4` for custom caching needs.

### Basic Usage

```yaml
- name: Cache dependencies
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-npm-
```

**Parameters:**
- `path`: Directory or file(s) to cache (required)
- `key`: Unique cache identifier (required)
- `restore-keys`: Fallback keys for partial matches (optional)
- `upload-chunk-size`: Upload chunk size in bytes (optional, default: 32MB)

### Multiple Paths

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      ~/.cache
      node_modules
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
```

### Checking Cache Hit

```yaml
- name: Cache dependencies
  id: cache-deps
  uses: actions/cache@v4
  with:
    path: node_modules
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}

- name: Install dependencies
  if: steps.cache-deps.outputs.cache-hit != 'true'
  run: npm ci

- name: Use cached dependencies
  if: steps.cache-deps.outputs.cache-hit == 'true'
  run: echo "Using cached dependencies"
```

### Save Cache Only on Success

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    save-always: false  # Default: saves on success only
```

### Cache Read-Only Mode

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    lookup-only: true  # Don't save, only restore
```

---

## Cache Key Strategies

### Hash-Based Keys

**Dependency Files:**

```yaml
# Single lock file
key: ${{ runner.os }}-deps-${{ hashFiles('package-lock.json') }}

# Multiple lock files
key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}

# Multiple file types
key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json', '**/yarn.lock') }}
```

**Source Files (Incremental Builds):**

```yaml
key: ${{ runner.os }}-build-${{ hashFiles('src/**/*.ts') }}
```

### Composite Keys

```yaml
# OS + Node version + Dependencies
key: ${{ runner.os }}-node-${{ matrix.node }}-${{ hashFiles('**/package-lock.json') }}

# Branch + Dependencies
key: ${{ runner.os }}-${{ github.ref_name }}-${{ hashFiles('**/package-lock.json') }}

# Date-based (weekly cache rotation)
key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}-${{ github.run_number }}
```

### Restore Keys (Fallback)

```yaml
key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
restore-keys: |
  ${{ runner.os }}-deps-
  ${{ runner.os }}-
```

**Matching Logic:**
1. Exact match on `key`
2. Prefix match on `restore-keys` (most recent)
3. No cache if no match

**Example:**
- Key: `Linux-deps-abc123`
- Restore keys: `Linux-deps-`, `Linux-`
- Will match: `Linux-deps-xyz789` (if `abc123` doesn't exist)

### Dynamic Keys

```yaml
# From file content
- id: get-date
  run: echo "date=$(date +'%Y-%m-%d')" >> $GITHUB_OUTPUT

- uses: actions/cache@v4
  with:
    path: ~/.cache
    key: ${{ runner.os }}-cache-${{ steps.get-date.outputs.date }}
```

---

## Docker Layer Caching

### Using docker/build-push-action

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

**Cache Backends:**
- `type=gha` - GitHub Actions cache
- `type=registry` - Container registry
- `type=local` - Local directory
- `type=s3` - S3 bucket

### Cache Mode

```yaml
# Default mode (minimal layers cached)
cache-to: type=gha

# Max mode (all layers cached)
cache-to: type=gha,mode=max
```

### Multi-Platform Builds with Cache

```yaml
- uses: docker/build-push-action@v5
  with:
    platforms: linux/amd64,linux/arm64
    cache-from: type=gha
    cache-to: type=gha,mode=max
    build-args: |
      BUILDKIT_INLINE_CACHE=1
```

### Registry Cache

```yaml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    push: true
    tags: user/app:latest
    cache-from: type=registry,ref=user/app:buildcache
    cache-to: type=registry,ref=user/app:buildcache,mode=max
```

---

## Parallelization Strategies

### Independent Parallel Jobs

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: npm test

  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: npm run build

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: npm audit
```

**Result:** All 4 jobs run simultaneously

### Matrix Strategy

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
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm test
```

**Result:** 9 jobs (3 OS × 3 Node versions)

### Test Splitting

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v5
      - run: npm test -- --shard=${{ matrix.shard }}/4
```

### Monorepo Parallel Builds

```yaml
jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      frontend: ${{ steps.filter.outputs.frontend }}
      backend: ${{ steps.filter.outputs.backend }}
    steps:
      - uses: actions/checkout@v5
      - uses: dorny/paths-filter@v2
        id: filter
        with:
          filters: |
            frontend:
              - 'packages/frontend/**'
            backend:
              - 'packages/backend/**'

  frontend:
    needs: changes
    if: needs.changes.outputs.frontend == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: npm run build --workspace=frontend

  backend:
    needs: changes
    if: needs.changes.outputs.backend == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: npm run build --workspace=backend
```

---

## Workflow Optimization

### Minimize Checkout

**Shallow Clone:**

```yaml
- uses: actions/checkout@v5
  with:
    fetch-depth: 1
```

**Sparse Checkout:**

```yaml
- uses: actions/checkout@v5
  with:
    sparse-checkout: |
      src/
      package.json
      package-lock.json
```

**Partial Clone:**

```yaml
- uses: actions/checkout@v5
  with:
    fetch-depth: 0
    filter: blob:none
```

### Conditional Steps

```yaml
# Skip on specific branches
- name: Deploy
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh

# Skip on PR
- name: Publish
  if: github.event_name != 'pull_request'
  run: npm publish

# Run only on schedule
- name: Cleanup
  if: github.event_name == 'schedule'
  run: ./cleanup.sh

# Skip if files unchanged
- name: Build frontend
  if: contains(github.event.head_commit.modified, 'frontend/')
  run: npm run build:frontend
```

### Early Termination

```yaml
- name: Check commit message
  run: |
    if [[ "${{ github.event.head_commit.message }}" =~ \[skip\ ci\] ]]; then
      echo "Skipping CI"
      exit 78  # Neutral exit code
    fi
```

### Artifacts Strategy

**Minimize Retention:**

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build
    path: dist/
    retention-days: 1  # Delete after 1 day
```

**Compress Before Upload:**

```yaml
- name: Compress artifacts
  run: tar -czf dist.tar.gz dist/

- uses: actions/upload-artifact@v4
  with:
    name: build
    path: dist.tar.gz
```

### Concurrency Control

**Cancel Redundant Runs:**

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

**Per-Job Concurrency:**

```yaml
jobs:
  deploy:
    concurrency:
      group: deploy-production
      cancel-in-progress: false
    steps: [...]
```

---

## Resource Management

### Self-Hosted Runner Optimization

**Clean Workspace:**

```yaml
jobs:
  build:
    runs-on: self-hosted
    steps:
      - name: Clean workspace
        run: |
          rm -rf ${{ github.workspace }}/*
          rm -rf ${{ github.workspace }}/.??*

      - uses: actions/checkout@v5
```

**Pre-installed Tools:**

```yaml
# Verify tools available
- name: Check tools
  run: |
    node --version
    npm --version
    docker --version
```

### Memory and CPU Constraints

**Container Resources:**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    container:
      image: node:20
      options: --cpus 2 --memory 4g
    steps: [...]
```

**Job Timeout:**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps: [...]
```

**Step Timeout:**

```yaml
- name: Long running task
  run: ./slow-process.sh
  timeout-minutes: 15
```

### Workflow Limits

**GitHub-Hosted Runners (Free Tier):**
- **Linux:** 2-core CPU, 7GB RAM, 14GB SSD
- **Windows:** 2-core CPU, 7GB RAM, 14GB SSD
- **macOS:** 3-core CPU, 14GB RAM, 14GB SSD
- **Concurrent Jobs:** 20 (free), 60 (Team), 180 (Enterprise)

**Usage Limits:**
- **Public repos:** Unlimited minutes
- **Private repos:** 2,000 min/month (free), 3,000 (Team)
- **Workflow file size:** 20KB per file, 100 files per repo
- **Workflow run time:** 72 hours maximum
- **API requests:** 1,000 per hour per repo

---

## Advanced Patterns

### Multi-Layer Caching

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # Layer 1: Dependencies
      - uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
          restore-keys: ${{ runner.os }}-npm-

      # Layer 2: Node modules
      - uses: actions/cache@v4
        with:
          path: node_modules
          key: ${{ runner.os }}-modules-${{ hashFiles('**/package-lock.json') }}

      # Layer 3: Build cache
      - uses: actions/cache@v4
        with:
          path: .next/cache
          key: ${{ runner.os }}-nextjs-${{ hashFiles('**/package-lock.json') }}-${{ hashFiles('**/*.js', '**/*.tsx') }}
          restore-keys: |
            ${{ runner.os }}-nextjs-${{ hashFiles('**/package-lock.json') }}-
            ${{ runner.os }}-nextjs-

      - run: npm ci
      - run: npm run build
```

### Incremental Build Cache

```yaml
- name: Cache build
  uses: actions/cache@v4
  with:
    path: |
      dist/
      .cache/
    key: build-${{ hashFiles('src/**') }}-${{ github.sha }}
    restore-keys: |
      build-${{ hashFiles('src/**') }}-
      build-

- name: Incremental build
  run: npm run build -- --incremental
```

### Cross-Job Caching

```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/cache@v4
        id: cache
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
      - if: steps.cache.outputs.cache-hit != 'true'
        run: npm ci

  build:
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
      - run: npm ci --prefer-offline
      - run: npm run build
```

---

## Monitoring and Debugging

### Cache Statistics

View cache usage in repository:
- Settings → Actions → Caches
- See size, creation date, last accessed
- Manually delete caches if needed

### Debugging Cache Issues

**Enable Debug Logging:**

Add repository secret: `ACTIONS_STEP_DEBUG=true`

**Check Cache Hits:**

```yaml
- name: Cache dependencies
  id: cache
  uses: actions/cache@v4
  with:
    path: node_modules
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}

- name: Debug cache
  run: |
    echo "Cache hit: ${{ steps.cache.outputs.cache-hit }}"
    echo "Cache key: ${{ steps.cache.outputs.cache-primary-key }}"
```

**List Cache Contents:**

```yaml
- name: List cached files
  run: |
    echo "=== Cached Dependencies ==="
    ls -lah node_modules/ || echo "No node_modules cached"
```

---

For security optimization, see `security-practices.md`.
