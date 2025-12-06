# GitHub Actions Monorepo CI with Turborepo

This example demonstrates an efficient CI/CD pipeline for a JavaScript/TypeScript monorepo using Turborepo's affected detection and remote caching.

## Features

- **Affected Detection**: Only builds, tests, and deploys packages that changed
- **Remote Caching**: Turborepo cloud caching for 70-90% cache hit rate
- **Parallel Execution**: Independent jobs run simultaneously
- **Selective Deployment**: Preview deploys for PRs, production for main branch
- **Performance Optimization**: 60-80% reduction in CI time vs naive approach

## Workflow Structure

### Jobs

1. **setup** - Install dependencies and cache setup
   - Installs npm dependencies
   - Prepares Turborepo cache

2. **lint** - Lint affected packages
   - Runs in parallel with test
   - Only affected packages since main

3. **test** - Test affected packages
   - Runs in parallel with lint
   - Only affected packages since main

4. **build** - Build affected packages
   - Depends on lint and test passing
   - Only affected packages since main
   - Uploads build artifacts

5. **deploy-preview** - Deploy preview (PRs only)
   - Deploys affected apps to preview environment
   - Only runs on pull requests

6. **deploy-production** - Deploy production (main branch only)
   - Deploys affected apps to production
   - Only runs on pushes to main
   - Uses GitHub environment protection

## Turborepo Configuration

### turbo.json

```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],  // Build dependencies first
      "outputs": ["dist/**"],    // Cache these outputs
      "cache": true
    },
    "test": {
      "dependsOn": ["build"],    // Tests depend on build
      "cache": true
    },
    "deploy:production": {
      "dependsOn": ["build", "test"],
      "cache": false             // Never cache deploys
    }
  }
}
```

## Performance Gains

### Before (Naive Approach)

Building all packages on every commit:

```yaml
# 100 packages, 30 minutes total
- run: npm run build --workspaces
```

**Cost:**
- 30 minutes per commit
- $0.008/minute = $0.24 per commit
- 100 commits/week = $24/week = $1,248/year

### After (Affected Detection)

Building only affected packages:

```yaml
# Only 10 packages changed = 6 minutes
- run: npx turbo run build --filter='...[origin/main]'
```

**Cost:**
- 6 minutes per commit (80% reduction)
- $0.008/minute = $0.048 per commit
- 100 commits/week = $4.80/week = $250/year

**Savings:** $998/year (80%)

## Setup

### 1. Install Turborepo

```bash
npm install turbo --save-dev
```

### 2. Configure Remote Caching

```bash
# Login to Vercel (free tier available)
npx turbo login

# Link repository
npx turbo link
```

This generates:
- `TURBO_TOKEN` - Add to GitHub Secrets
- `TURBO_TEAM` - Add to GitHub Variables

### 3. Create turbo.json

See `turbo.json` in this directory.

### 4. Add Workflow

Copy `.github/workflows/ci.yml` to your repository.

### 5. Configure Secrets/Variables

**GitHub Secrets:**
- `TURBO_TOKEN` - Turborepo remote cache token
- `VERCEL_TOKEN` - Vercel deployment token (if deploying)

**GitHub Variables:**
- `TURBO_TEAM` - Turborepo team name

## Repository Structure

```
monorepo/
├── apps/
│   ├── web/              # Next.js app
│   ├── api/              # Express API
│   └── mobile/           # React Native
├── packages/
│   ├── ui-components/    # Shared UI library
│   ├── api-client/       # API client
│   └── utils/            # Shared utilities
├── turbo.json            # Turborepo config
├── package.json
└── .github/
    └── workflows/
        └── ci.yml
```

## Affected Detection Examples

### Scenario 1: API Client Change

**Changed files:**
- `packages/api-client/src/client.ts`

**Affected packages:**
- `api-client` (changed)
- `web` (depends on api-client)
- `api` (depends on api-client)
- `mobile` (depends on api-client)

**Not affected:**
- `ui-components` (no dependency on api-client)
- `utils` (no dependency on api-client)

**CI runs:**
- Lint: api-client, web, api, mobile (4 packages)
- Test: api-client, web, api, mobile (4 packages)
- Build: api-client, web, api, mobile (4 packages)
- Deploy: web, api, mobile (3 apps)

### Scenario 2: UI Component Change

**Changed files:**
- `packages/ui-components/src/Button.tsx`

**Affected packages:**
- `ui-components` (changed)
- `web` (depends on ui-components)
- `mobile` (depends on ui-components)

**Not affected:**
- `api-client`, `api`, `utils`

**CI runs:**
- Lint: ui-components, web, mobile (3 packages)
- Test: ui-components, web, mobile (3 packages)
- Build: ui-components, web, mobile (3 packages)
- Deploy: web, mobile (2 apps)

## Turborepo Filter Patterns

```bash
# All packages changed since main
npx turbo run build --filter='...[origin/main]'

# Specific package and its dependencies
npx turbo run build --filter='web...'

# Specific package and its dependents
npx turbo run build --filter='...api-client'

# Changed packages only (no dependents)
npx turbo run build --filter='[origin/main]'

# Multiple filters
npx turbo run build --filter='web...' --filter='api...'
```

## Cache Strategy

### Local Cache

Turborepo caches task outputs locally in `.turbo/`:

```
.turbo/
├── cache/
│   ├── abc123def456...  # Hash-based cache entries
│   └── ...
```

### Remote Cache

Turborepo uploads cache to Vercel:

- Same inputs → Same hash → Cached output
- Shared across team members and CI runs
- Typical 70-90% cache hit rate

### Cache Hit Example

```bash
# First run (cache miss)
npx turbo run build
# Building packages... (3 minutes)

# Second run (cache hit)
npx turbo run build
# ✓ build:ui-components (cached)
# ✓ build:web (cached)
# ✓ build:api (cached)
# (0.5 seconds)
```

## Troubleshooting

### Cache Not Working

Check cache configuration:
```bash
npx turbo run build --dry-run
```

Verify environment variables:
```yaml
env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ vars.TURBO_TEAM }}
```

### Affected Detection Not Working

Ensure full git history:
```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0  # Important!
```

### Slow Dependency Installation

Enable npm cache:
```yaml
- uses: actions/setup-node@v4
  with:
    cache: 'npm'
```

## Advanced: Dynamic Matrix

Generate matrix based on affected packages:

```yaml
jobs:
  detect-affected:
    outputs:
      packages: ${{ steps.detect.outputs.packages }}
    steps:
      - id: detect
        run: |
          PACKAGES=$(npx turbo run build --filter='...[origin/main]' --dry-run=json | jq -c '.packages')
          echo "packages=$PACKAGES" >> $GITHUB_OUTPUT

  build:
    needs: detect-affected
    strategy:
      matrix:
        package: ${{ fromJSON(needs.detect-affected.outputs.packages) }}
    steps:
      - run: npm run build --workspace=${{ matrix.package }}
```

## Resources

- Turborepo Documentation: https://turbo.build/repo/docs
- Turborepo Remote Caching: https://turbo.build/repo/docs/core-concepts/remote-caching
- Filter Patterns: https://turbo.build/repo/docs/core-concepts/monorepos/filtering
