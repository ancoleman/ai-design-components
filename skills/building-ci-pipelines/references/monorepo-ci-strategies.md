# Monorepo CI Strategies

Strategies for building efficient CI pipelines in monorepos with affected detection, intelligent caching, and parallel execution.

## Table of Contents

1. [Monorepo Challenges](#monorepo-challenges)
2. [Affected Detection](#affected-detection)
3. [Turborepo Strategy](#turborepo-strategy)
4. [Nx Strategy](#nx-strategy)
5. [Bazel Strategy](#bazel-strategy)
6. [Change Detection Algorithms](#change-detection-algorithms)
7. [Performance Optimization](#performance-optimization)

## Monorepo Challenges

### Problems with Naive CI

**Build Everything:**
```yaml
# BAD: Rebuilds all packages on every commit
- run: npm run build --workspaces
```

**Impact:**
- 100+ packages = 30+ minute builds
- Wastes CI minutes (60-80% unnecessary builds)
- Slow feedback loop for developers
- Expensive cloud CI costs

### Monorepo Scale Examples

| Repository | Packages | Build Time (Naive) | With Affected | Savings |
|------------|----------|-------------------|---------------|---------|
| Small | 10 packages | 3 min | 1 min | 67% |
| Medium | 50 packages | 15 min | 4 min | 73% |
| Large | 200 packages | 60 min | 12 min | 80% |

## Affected Detection

### Core Concept

**Affected Packages = Changed Packages + Dependent Packages**

Example dependency graph:
```
@myorg/api-client (changed)
    ├── @myorg/frontend (depends on api-client) ← affected
    └── @myorg/mobile (depends on api-client) ← affected

@myorg/backend (changed)
    └── @myorg/admin (depends on backend) ← affected

@myorg/docs (unchanged) ← NOT affected
```

Changed files:
- `packages/api-client/src/index.ts`
- `packages/backend/src/server.ts`

Affected packages:
- `api-client` (changed)
- `frontend` (depends on api-client)
- `mobile` (depends on api-client)
- `backend` (changed)
- `admin` (depends on backend)

Not affected:
- `docs` (no changes, no dependencies on changed packages)

### Dependency Graph Construction

**Package Dependencies (package.json):**
```json
{
  "name": "@myorg/frontend",
  "dependencies": {
    "@myorg/api-client": "workspace:*",
    "@myorg/ui-components": "workspace:*"
  }
}
```

**Build Dependencies (turbo.json / nx.json):**
```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"]  // Build dependencies first
    },
    "test": {
      "dependsOn": ["build"]   // Test depends on build
    }
  }
}
```

**Full Graph:**
```
ui-components#build → frontend#build → frontend#test
api-client#build    ↗
```

## Turborepo Strategy

### Setup

```bash
npm install turbo --save-dev
```

**turbo.json:**
```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "build/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "cache": false  // Don't cache test results (always run)
    },
    "lint": {
      "outputs": []
    },
    "deploy": {
      "dependsOn": ["build", "test"],
      "cache": false
    }
  },
  "remoteCache": {
    "signature": true
  }
}
```

### CI Integration (GitHub Actions)

```yaml
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
          fetch-depth: 0  # Required for comparison

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: npm ci

      # Build only affected packages since main
      - name: Build affected
        run: npx turbo run build --filter='...[origin/main]'
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ vars.TURBO_TEAM }}

      # Test only affected packages
      - name: Test affected
        run: npx turbo run test --filter='...[origin/main]'
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ vars.TURBO_TEAM }}
```

### Filter Patterns

```bash
# All packages changed since main
npx turbo run build --filter='...[origin/main]'

# Specific package and its dependencies
npx turbo run build --filter='@myorg/frontend...'

# Specific package and its dependents
npx turbo run build --filter='...@myorg/api-client'

# Changed packages only (no dependents)
npx turbo run build --filter='[origin/main]'

# Multiple filters
npx turbo run build --filter='@myorg/frontend...' --filter='@myorg/mobile...'
```

### Remote Caching

**Benefits:**
- Share build artifacts across CI runs
- Share artifacts across team members
- 70-90% cache hit rate in practice

**Setup (Vercel):**
```bash
npx turbo login
npx turbo link
```

**In CI:**
```yaml
env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}  # From Vercel
  TURBO_TEAM: ${{ vars.TURBO_TEAM }}       # From Vercel
```

Cache is automatically used for matching builds.

### Turborepo + Docker

```dockerfile
FROM node:20-alpine AS base

FROM base AS builder
WORKDIR /app
RUN npm install -g turbo
COPY . .
RUN turbo prune --scope=@myorg/api --docker

FROM base AS installer
WORKDIR /app
COPY --from=builder /app/out/json/ .
COPY --from=builder /app/out/package-lock.json ./package-lock.json
RUN npm ci

COPY --from=builder /app/out/full/ .
RUN npx turbo run build --filter=@myorg/api...

FROM base AS runner
WORKDIR /app
COPY --from=installer /app .
CMD ["node", "apps/api/dist/index.js"]
```

## Nx Strategy

### Setup

```bash
npx create-nx-workspace@latest myorg --preset=npm
```

**nx.json:**
```json
{
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["{projectRoot}/dist"],
      "cache": true
    },
    "test": {
      "dependsOn": ["build"],
      "cache": true
    }
  },
  "tasksRunnerOptions": {
    "default": {
      "runner": "nx-cloud",
      "options": {
        "cacheableOperations": ["build", "test", "lint"],
        "accessToken": "NX_CLOUD_TOKEN"
      }
    }
  }
}
```

### CI Integration (GitHub Actions)

```yaml
name: CI
on: [pull_request]

jobs:
  affected:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # Derive base/head for comparison
      - name: Derive SHAs
        id: setSHAs
        uses: nrwl/nx-set-shas@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - run: npm ci

      # Run tasks only for affected projects
      - name: Affected build
        run: npx nx affected -t build --base=${{ steps.setSHAs.outputs.base }} --head=${{ steps.setSHAs.outputs.head }}
        env:
          NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}

      - name: Affected test
        run: npx nx affected -t test --base=${{ steps.setSHAs.outputs.base }} --head=${{ steps.setSHAs.outputs.head }}
        env:
          NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}

      - name: Affected lint
        run: npx nx affected -t lint --base=${{ steps.setSHAs.outputs.base }} --head=${{ steps.setSHAs.outputs.head }}
        env:
          NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}
```

### Nx Commands

```bash
# Show affected projects
npx nx affected:graph --base=main --head=HEAD

# Run target for affected projects
npx nx affected -t build --base=main

# Run multiple targets
npx nx affected -t build,test,lint --base=main

# Run specific project
npx nx run @myorg/frontend:build

# Run target for all projects
npx nx run-many -t build --all
```

### Nx Cloud Features

**Distributed Task Execution:**
- Nx Cloud distributes tasks across multiple agents
- 10x speedup for large monorepos

```yaml
# .github/workflows/ci.yml
- name: Start Nx Cloud agents
  run: npx nx-cloud start-ci-run --distribute-on="8 linux-medium-js"

- name: Run affected tasks
  run: npx nx affected -t build,test,lint --base=main --parallel=3

- name: Stop Nx Cloud agents
  run: npx nx-cloud stop-all-agents
```

**Computation Caching:**
- Hash inputs (source files, dependencies, environment)
- Store outputs in cloud
- Restore exact outputs on cache hit

**Performance:**
- 70-90% cache hit rate
- 50-80% reduction in CI time

## Bazel Strategy

### When to Use Bazel

**Use Bazel if:**
- 1000+ packages (Google-scale monorepo)
- Multi-language (Java, Go, Rust, Python, C++)
- Need hermetic builds (fully reproducible)
- Have dedicated build team

**Skip Bazel if:**
- <100 packages
- JavaScript/TypeScript only (use Turborepo/Nx)
- Prototype/startup (steep learning curve)

### Bazel Basics

**BUILD file:**
```python
# packages/api-client/BUILD
load("@npm//@bazel/typescript:index.bzl", "ts_library")

ts_library(
    name = "api-client",
    srcs = glob(["src/**/*.ts"]),
    deps = [
        "@npm//axios",
        "@npm//@types/node",
    ],
    module_name = "@myorg/api-client",
    visibility = ["//visibility:public"],
)
```

**WORKSPACE file:**
```python
workspace(name = "myorg")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# Node.js rules
http_archive(
    name = "build_bazel_rules_nodejs",
    sha256 = "...",
    urls = ["https://github.com/bazelbuild/rules_nodejs/releases/..."],
)
```

### Affected Targets

```bash
# Show changed targets
bazel query 'rdeps(//..., set($(git diff --name-only main...HEAD | sed "s|^|//|" | sed "s|/BUILD$||")))'

# Build affected targets
bazel build $(bazel query '...')
```

### Remote Execution

Bazel can execute builds on remote servers:

```bash
bazel build //... \
  --remote_executor=grpcs://remote.buildbuddy.io \
  --remote_cache=grpcs://remote.buildbuddy.io \
  --remote_upload_local_results=true
```

**Benefits:**
- Consistent build environment
- Massive parallelization (100+ machines)
- Shared remote cache across team

## Change Detection Algorithms

### Git-Based Detection

**1. Get Changed Files:**
```bash
git diff --name-only origin/main...HEAD
```

Output:
```
packages/api-client/src/index.ts
packages/api-client/package.json
packages/backend/src/server.ts
```

**2. Map Files to Packages:**
```typescript
function getAffectedPackages(changedFiles: string[]): string[] {
  const packages = new Set<string>();

  for (const file of changedFiles) {
    // Find nearest package.json
    const pkg = findNearestPackageJson(file);
    if (pkg) packages.add(pkg.name);
  }

  return Array.from(packages);
}
```

Result: `['@myorg/api-client', '@myorg/backend']`

**3. Build Dependency Graph:**
```typescript
function buildDependencyGraph(): Map<string, Set<string>> {
  const graph = new Map();

  for (const pkg of allPackages) {
    const deps = new Set();

    // Add package dependencies
    for (const dep of pkg.dependencies) {
      if (isWorkspacePackage(dep)) {
        deps.add(dep);
      }
    }

    graph.set(pkg.name, deps);
  }

  return graph;
}
```

**4. Find Affected Packages (BFS):**
```typescript
function findAffectedPackages(
  changedPackages: string[],
  graph: Map<string, Set<string>>
): string[] {
  const affected = new Set(changedPackages);
  const queue = [...changedPackages];

  while (queue.length > 0) {
    const current = queue.shift()!;

    // Find packages that depend on current
    for (const [pkg, deps] of graph.entries()) {
      if (deps.has(current) && !affected.has(pkg)) {
        affected.add(pkg);
        queue.push(pkg);
      }
    }
  }

  return Array.from(affected);
}
```

### Content-Based Detection

**Turborepo/Nx approach:**

**1. Compute task hash:**
```typescript
function computeTaskHash(task: Task): string {
  const inputs = [
    hashSourceFiles(task.package),
    hashDependencies(task.package),
    hashBuildConfig(task),
    hashEnvironment(task),
  ];

  return sha256(inputs.join(''));
}
```

**2. Check cache:**
```typescript
async function runTask(task: Task) {
  const hash = computeTaskHash(task);

  // Check local cache
  const cached = await getFromCache(hash);
  if (cached) {
    console.log(`Cache hit for ${task.name}`);
    return cached;
  }

  // Execute task
  const output = await executeTask(task);

  // Store in cache
  await putInCache(hash, output);

  return output;
}
```

**3. Cache hit = skip execution**

Same inputs → Same hash → Cached output restored

## Performance Optimization

### Parallel Execution

**Turborepo:**
```bash
# Run tasks in parallel (default)
npx turbo run build test --parallel

# Limit parallelism
npx turbo run build --concurrency=4
```

**Nx:**
```bash
# Parallel execution (default)
npx nx affected -t build --parallel=3

# Max parallelism
npx nx affected -t build --parallel=true
```

### Pipeline Optimization

**Sequential (slow):**
```
lint (2m) → test (5m) → build (3m) = 10m total
```

**Parallel (fast):**
```
lint (2m) ──┐
            ├─→ build (3m) = 5m total
test (5m) ──┘
```

**turbo.json (parallel lint/test):**
```json
{
  "pipeline": {
    "lint": {},
    "test": {},
    "build": {
      "dependsOn": ["lint", "test"]
    }
  }
}
```

### Incremental Builds

**TypeScript incremental compilation:**
```json
{
  "compilerOptions": {
    "incremental": true,
    "tsBuildInfoFile": ".tsbuildinfo"
  }
}
```

Cache `.tsbuildinfo` in CI:
```yaml
- uses: actions/cache@v4
  with:
    path: '**/tsconfig.tsbuildinfo'
    key: tsc-${{ hashFiles('**/tsconfig.json') }}
```

### CI-Specific Optimizations

**Shallow clones:**
```yaml
# Fetch minimal history
- uses: actions/checkout@v4
  with:
    fetch-depth: 1  # Only latest commit
```

**Sparse checkouts (large monorepos):**
```yaml
- uses: actions/checkout@v4
  with:
    sparse-checkout: |
      packages/api-client
      packages/frontend
```

**Split jobs by affected packages:**
```yaml
jobs:
  detect-affected:
    outputs:
      packages: ${{ steps.detect.outputs.packages }}
    steps:
      - id: detect
        run: |
          PACKAGES=$(npx turbo run build --filter='...[origin/main]' --dry-run | jq -c '.packages')
          echo "packages=$PACKAGES" >> $GITHUB_OUTPUT

  build-package:
    needs: detect-affected
    strategy:
      matrix:
        package: ${{ fromJSON(needs.detect-affected.outputs.packages) }}
    steps:
      - run: npm run build --workspace=${{ matrix.package }}
```

## Best Practices

**DO:**
- Use affected detection for all monorepo CI
- Enable remote caching (Turborepo/Nx Cloud)
- Cache build artifacts between CI runs
- Parallelize independent tasks
- Use shallow clones when possible

**DON'T:**
- Build all packages on every commit
- Skip dependency graph construction
- Ignore cache optimization
- Run serial pipelines unnecessarily
- Use Bazel for small JavaScript monorepos

## Tool Comparison

| Feature | Turborepo | Nx | Bazel |
|---------|-----------|-----|-------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Performance** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Caching** | Remote | Remote + Distributed | Remote |
| **Languages** | JS/TS | JS/TS/Python/Go | All |
| **Setup Time** | 5 min | 10 min | Hours |
| **Best For** | JS monorepos | Multi-language | Google-scale |
