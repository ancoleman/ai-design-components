# Caching Strategies for CI Pipelines

Comprehensive guide to caching strategies for faster CI/CD pipelines across multiple platforms.

## Table of Contents

1. [Cache Fundamentals](#cache-fundamentals)
2. [GitHub Actions Caching](#github-actions-caching)
3. [GitLab CI Caching](#gitlab-ci-caching)
4. [Docker Layer Caching](#docker-layer-caching)
5. [Remote Caching (Turborepo/Nx)](#remote-caching-turboreponx)
6. [Multi-Layer Strategies](#multi-layer-strategies)
7. [Cache Invalidation](#cache-invalidation)

## Cache Fundamentals

### What to Cache

**Dependencies:**
- `node_modules` (Node.js)
- `~/.cargo` (Rust)
- `~/.cache/pip` (Python)
- `~/go/pkg/mod` (Go)

**Build Outputs:**
- `dist/`, `build/` (compiled code)
- `.next/`, `.nuxt/` (framework builds)
- `target/` (Rust)

**Intermediate Artifacts:**
- `tsconfig.tsbuildinfo` (TypeScript)
- `.vite/` (Vite)
- Coverage data

### Cache Key Design

**Good cache keys:**
```yaml
# Dependencies - invalidate on lock file change
key: deps-${{ hashFiles('**/package-lock.json') }}

# Build outputs - invalidate on source change
key: build-${{ hashFiles('src/**/*.ts') }}

# OS-specific
key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
```

**Bad cache keys:**
```yaml
# Too generic - never invalidates
key: node-modules

# Too specific - low cache hit rate
key: build-${{ github.sha }}
```

### Cache Restore Keys

Provide fallback keys:
```yaml
key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
restore-keys: |
  ${{ runner.os }}-deps-
  ${{ runner.os }}-
```

## GitHub Actions Caching

### Automatic Language Caching

```yaml
# Node.js
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'npm'  # Automatically caches ~/.npm

# Python
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'

# Go
- uses: actions/setup-go@v5
  with:
    go-version: '1.23'
    cache: true

# Rust (use external action)
- uses: Swatinem/rust-cache@v2
```

### Manual Cache Control

```yaml
- name: Cache dependencies
  uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      ~/.cache
      node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### Cache Limits

- **Size limit:** 10GB per repository
- **Retention:** 7 days for inactive caches
- **Entries:** Unlimited (until 10GB total)

### Cache Hit Reporting

```yaml
- name: Cache dependencies
  id: cache
  uses: actions/cache@v4
  with:
    path: node_modules
    key: deps-${{ hashFiles('package-lock.json') }}

- name: Install dependencies
  if: steps.cache.outputs.cache-hit != 'true'
  run: npm ci

- name: Report cache hit
  run: echo "Cache hit: ${{ steps.cache.outputs.cache-hit }}"
```

## GitLab CI Caching

### Basic Cache

```yaml
cache:
  key: "${CI_COMMIT_REF_SLUG}"
  paths:
    - node_modules/
    - .npm/

build:
  script:
    - npm ci
    - npm run build
```

### Per-Job Cache

```yaml
test:
  cache:
    key: test-cache
    paths:
      - node_modules/
  script:
    - npm test

build:
  cache:
    key: build-cache
    paths:
      - node_modules/
      - dist/
  script:
    - npm run build
```

### Cache Policies

```yaml
# Only download cache (don't update)
cache:
  key: deps
  paths:
    - node_modules/
  policy: pull

# Only upload cache (don't download)
cache:
  key: deps
  paths:
    - node_modules/
  policy: push
```

### Fallback Keys

```yaml
cache:
  key:
    files:
      - package-lock.json
  fallback_keys:
    - default-npm-cache
  paths:
    - node_modules/
```

## Docker Layer Caching

### BuildKit Cache

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build with cache
  uses: docker/build-push-action@v5
  with:
    context: .
    cache-from: type=registry,ref=ghcr.io/${{ github.repository }}:buildcache
    cache-to: type=registry,ref=ghcr.io/${{ github.repository }}:buildcache,mode=max
```

### Multi-Stage Dockerfile Optimization

```dockerfile
# Base stage - changes infrequently
FROM node:20-alpine AS base
WORKDIR /app

# Dependencies stage - changes when package.json changes
FROM base AS deps
COPY package.json package-lock.json ./
RUN npm ci

# Build stage - changes when source changes
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production stage - minimal final image
FROM base AS runner
COPY --from=builder /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

**Layer reuse:**
- Layer 1: Base image (rarely changes)
- Layer 2: Dependencies (changes when package.json changes)
- Layer 3: Source code (changes frequently)

### GitHub Actions Docker Cache

```yaml
- name: Docker meta
  id: meta
  uses: docker/metadata-action@v5
  with:
    images: ghcr.io/${{ github.repository }}

- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: ${{ steps.meta.outputs.tags }}
    cache-from: |
      type=registry,ref=ghcr.io/${{ github.repository }}:buildcache
      type=registry,ref=ghcr.io/${{ github.repository }}:latest
    cache-to: type=registry,ref=ghcr.io/${{ github.repository }}:buildcache,mode=max
```

## Remote Caching (Turborepo/Nx)

### Turborepo Remote Cache

**Setup:**
```bash
npx turbo login
npx turbo link
```

**CI Usage:**
```yaml
- name: Build with remote cache
  run: npx turbo run build
  env:
    TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
    TURBO_TEAM: ${{ vars.TURBO_TEAM }}
```

**Benefits:**
- Shared across team and CI
- 70-90% cache hit rate
- Zero configuration after setup

### Nx Cloud

**Setup:**
```bash
npx nx connect-to-nx-cloud
```

**CI Usage:**
```yaml
- name: Build with Nx Cloud
  run: npx nx affected -t build
  env:
    NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}
```

**Features:**
- Distributed task execution
- Smart cache invalidation
- Performance analytics

## Multi-Layer Strategies

### Layer 1: Package Manager Cache

```yaml
- uses: actions/setup-node@v4
  with:
    cache: 'npm'  # Caches ~/.npm
```

### Layer 2: Node Modules Cache

```yaml
- uses: actions/cache@v4
  with:
    path: node_modules
    key: deps-${{ hashFiles('package-lock.json') }}
```

### Layer 3: Build Tool Cache (Nx)

```yaml
- uses: actions/cache@v4
  with:
    path: .nx/cache
    key: nx-${{ hashFiles('nx.json') }}
```

### Layer 4: Build Outputs Cache

```yaml
- uses: actions/cache@v4
  with:
    path: |
      apps/**/dist
      packages/**/dist
    key: build-${{ hashFiles('src/**/*.ts') }}
```

### Layer 5: Remote Cache (Turborepo/Nx)

```yaml
env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
```

**Result:** 90%+ cache hit rate across all layers

## Cache Invalidation

### When to Invalidate

**Dependency changes:**
```yaml
key: deps-${{ hashFiles('**/package-lock.json') }}
```

**Source code changes:**
```yaml
key: build-${{ hashFiles('src/**/*.ts') }}
```

**Configuration changes:**
```yaml
key: config-${{ hashFiles('tsconfig.json', 'vite.config.ts') }}
```

### Manual Invalidation

**GitHub Actions:**
Delete cache via API:
```bash
gh api repos/{owner}/{repo}/actions/caches/{cache_id} --method DELETE
```

**GitLab CI:**
Clear project cache:
```bash
curl --request POST "https://gitlab.com/api/v4/projects/{id}/jobs/{job_id}/erase"
```

### Time-Based Invalidation

```yaml
key: cache-${{ runner.os }}-${{ github.run_number }}
restore-keys: |
  cache-${{ runner.os }}-
```

Uses run number as cache key, falls back to previous runs.

## Performance Benchmarks

### Node.js Project (50 packages)

**No caching:**
- npm install: 3 minutes
- Build: 5 minutes
- Total: 8 minutes

**With dependency caching:**
- npm ci (cache hit): 30 seconds
- Build: 5 minutes
- Total: 5.5 minutes (31% faster)

**With dependency + build caching:**
- npm ci (cache hit): 30 seconds
- Build (partial cache): 2 minutes
- Total: 2.5 minutes (69% faster)

**With Turborepo remote cache:**
- npm ci (cache hit): 30 seconds
- Build (full cache): 10 seconds
- Total: 40 seconds (92% faster)

## Best Practices

**DO:**
- Use hash-based cache keys
- Provide restore-keys for fallback
- Cache dependencies separately from builds
- Use remote caching for monorepos
- Monitor cache hit rates

**DON'T:**
- Use generic cache keys (e.g., "cache")
- Cache sensitive data
- Exceed 10GB limit (GitHub Actions)
- Cache generated files in git
- Forget to invalidate on config changes

## Troubleshooting

### Low Cache Hit Rate

Check cache key specificity:
```yaml
# Too specific (low hits)
key: build-${{ github.sha }}

# Better
key: build-${{ hashFiles('src/**') }}
```

### Cache Size Issues

Check cache size:
```bash
gh api repos/{owner}/{repo}/actions/cache/usage
```

Reduce cache size:
```yaml
# Only cache necessary files
path: |
  node_modules
  !node_modules/.cache
```

### Stale Cache

Force cache refresh:
```yaml
key: v2-deps-${{ hashFiles('package-lock.json') }}
```

Increment version prefix to invalidate old caches.
