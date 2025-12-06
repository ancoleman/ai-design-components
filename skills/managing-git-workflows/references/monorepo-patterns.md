# Monorepo Management Patterns

Complete guide to managing monorepos with build tools, Git strategies, and code ownership patterns.

## Table of Contents

1. [Monorepo vs Polyrepo](#monorepo-vs-polyrepo)
2. [Build Tool Selection](#build-tool-selection)
3. [Nx Configuration](#nx-configuration)
4. [Turborepo Configuration](#turborepo-configuration)
5. [Git Sparse Checkout](#git-sparse-checkout)
6. [CODEOWNERS Setup](#codeowners-setup)
7. [Submodules vs Subtrees](#submodules-vs-subtrees)

## Monorepo vs Polyrepo

### Monorepo Benefits

**Code Management:**
- ✅ Atomic commits across multiple projects
- ✅ Easier refactoring (see all usage)
- ✅ Single source of truth
- ✅ Shared tooling and configuration

**Development Workflow:**
- ✅ Simplified dependency management
- ✅ Consistent versioning
- ✅ Better code reuse
- ✅ Easier to onboard new developers

**Build and Deploy:**
- ✅ Coordinated releases
- ✅ Shared CI/CD configuration
- ✅ Faster iteration on shared libraries

### Monorepo Challenges

**Performance:**
- ❌ Large repository size
- ❌ Slower Git operations (clone, checkout, status)
- ❌ IDE indexing takes longer
- ❌ CI/CD complexity increases

**Organization:**
- ❌ Code ownership ambiguity
- ❌ More complex CI/CD
- ❌ Access control harder to manage
- ❌ Risk of tight coupling

### When to Use Monorepo

**Use monorepo when:**
- Multiple projects share significant code
- Team owns all projects
- Atomic changes across projects needed
- Shared tooling and standards important

**Use polyrepo when:**
- Projects are independent
- Different teams own projects
- Different release cycles
- Independent scalability needed

---

## Build Tool Selection

### Comparison Matrix

| Feature | Nx | Turborepo | Lerna |
|---------|----|-----------| ------|
| **Language** | TypeScript/JS | Any | TypeScript/JS |
| **Dependency Graph** | ✅ Advanced | ✅ Basic | ❌ No |
| **Affected Commands** | ✅ Yes | ✅ Yes | ❌ No |
| **Caching** | ✅ Local + Remote | ✅ Local + Remote | ❌ No |
| **Incremental Builds** | ✅ Yes | ✅ Yes | ❌ No |
| **IDE Integration** | ✅ Excellent | ⚠️ Limited | ❌ No |
| **Learning Curve** | Medium | Low | Low |
| **Best For** | Large TS/JS monorepos | Next.js/React apps | Legacy projects |

### Recommendation

**Choose Nx when:**
- Large TypeScript/JavaScript monorepo
- Need advanced dependency analysis
- Want IDE integration (VS Code extension)
- Team is experienced with build tools

**Choose Turborepo when:**
- Next.js or React applications
- Want simple, fast setup
- Need remote caching (Vercel)
- Prefer minimal configuration

**Choose Lerna when:**
- Maintaining existing Lerna project
- Simple publishing workflow
- (Note: Consider migrating to Nx or Turborepo)

---

## Nx Configuration

### Installation

```bash
# Create new Nx workspace
npx create-nx-workspace@latest myworkspace

# Options:
# - Select preset: "apps" or "ts"
# - Package manager: npm, yarn, or pnpm
```

### Project Structure

```
monorepo/
├── apps/
│   ├── web-app/              # Frontend application
│   ├── mobile-app/           # Mobile application
│   └── admin-dashboard/      # Admin application
├── libs/
│   ├── ui-components/        # Shared UI components
│   ├── auth/                 # Authentication library
│   ├── api-client/           # API client library
│   └── shared-utils/         # Utility functions
├── tools/
│   └── generators/           # Custom generators
├── nx.json                   # Nx configuration
├── package.json
└── tsconfig.base.json
```

### Nx Configuration

**nx.json:**
```json
{
  "tasksRunnerOptions": {
    "default": {
      "runner": "nx/tasks-runners/default",
      "options": {
        "cacheableOperations": ["build", "test", "lint"],
        "parallel": 3
      }
    }
  },
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["{projectRoot}/dist"]
    },
    "test": {
      "inputs": ["default", "^production"]
    }
  },
  "namedInputs": {
    "default": ["{projectRoot}/**/*"],
    "production": [
      "!{projectRoot}/**/*.spec.ts",
      "!{projectRoot}/tsconfig.spec.json"
    ]
  }
}
```

### Common Nx Commands

```bash
# Run build for specific project
nx build web-app

# Run build for all affected projects
nx affected:build --base=main

# Run tests for all affected projects
nx affected:test --base=main

# Run lint for all affected projects
nx affected:lint --base=main

# Show dependency graph
nx graph

# Run all builds in parallel
nx run-many --target=build --all

# Reset Nx cache
nx reset
```

### Project Configuration

**apps/web-app/project.json:**
```json
{
  "name": "web-app",
  "sourceRoot": "apps/web-app/src",
  "projectType": "application",
  "targets": {
    "build": {
      "executor": "@nx/webpack:webpack",
      "outputs": ["{options.outputPath}"],
      "options": {
        "outputPath": "dist/apps/web-app",
        "main": "apps/web-app/src/main.tsx",
        "tsConfig": "apps/web-app/tsconfig.app.json"
      }
    },
    "serve": {
      "executor": "@nx/webpack:dev-server",
      "options": {
        "buildTarget": "web-app:build",
        "port": 3000
      }
    },
    "test": {
      "executor": "@nx/jest:jest",
      "options": {
        "jestConfig": "apps/web-app/jest.config.ts"
      }
    }
  }
}
```

### Nx Affected Commands

Run only what changed:

```bash
# Build only affected projects since main
nx affected:build --base=main --head=HEAD

# Test only affected projects
nx affected:test --base=main

# Lint only affected projects
nx affected:lint --base=main

# Run all affected targets
nx affected --target=build,test,lint --base=main
```

### Nx Caching

**Local Cache:**
Automatically caches build outputs locally:
```bash
# First build (no cache)
nx build web-app  # Takes 30s

# Second build (cached)
nx build web-app  # Takes <1s
```

**Remote Cache (Nx Cloud):**
```bash
# Connect to Nx Cloud
npx nx connect-to-nx-cloud

# Shared cache across team
nx build web-app  # Downloads from cache if built by teammate
```

---

## Turborepo Configuration

### Installation

```bash
# Create new Turborepo
npx create-turbo@latest

# Project structure will be created
```

### Project Structure

```
monorepo/
├── apps/
│   ├── web/                  # Next.js app
│   │   ├── package.json
│   │   └── src/
│   └── docs/                 # Documentation site
│       ├── package.json
│       └── src/
├── packages/
│   ├── ui/                   # UI component library
│   │   ├── package.json
│   │   └── src/
│   ├── eslint-config-custom/ # Shared ESLint config
│   └── tsconfig/             # Shared TypeScript config
├── turbo.json                # Turborepo configuration
├── package.json              # Root package.json
└── pnpm-workspace.yaml       # Workspace config (if using pnpm)
```

### Turborepo Configuration

**turbo.json:**
```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [".env"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "dist/**", "build/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "cache": false
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### Common Turborepo Commands

```bash
# Run build for all projects
turbo run build

# Run build for specific project
turbo run build --filter=web

# Run dev for all apps
turbo run dev

# Run tests
turbo run test

# Clear cache
turbo run build --force
```

### Workspace Configuration

**package.json (root):**
```json
{
  "name": "monorepo",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "test": "turbo run test",
    "lint": "turbo run lint"
  },
  "devDependencies": {
    "turbo": "^1.10.0"
  }
}
```

**pnpm-workspace.yaml:**
```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

### Package Dependencies

**apps/web/package.json:**
```json
{
  "name": "web",
  "dependencies": {
    "ui": "*",
    "next": "^14.0.0",
    "react": "^18.2.0"
  },
  "devDependencies": {
    "eslint-config-custom": "*",
    "tsconfig": "*"
  }
}
```

**packages/ui/package.json:**
```json
{
  "name": "ui",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch"
  }
}
```

### Remote Caching

**Enable Vercel Remote Cache:**
```bash
# Login to Vercel
npx turbo login

# Link project
npx turbo link

# Builds now use remote cache
turbo run build
```

---

## Git Sparse Checkout

### Overview

Clone only needed directories from large monorepo.

### Enable Sparse Checkout

```bash
# Clone without checking out files
git clone --no-checkout https://github.com/org/monorepo.git
cd monorepo

# Enable sparse checkout
git sparse-checkout init --cone

# Checkout only specific directories
git sparse-checkout set apps/web libs/ui-components

# Now checkout files
git checkout main
```

### Verify Sparse Checkout

```bash
# List current sparse checkout
git sparse-checkout list

# Output:
# apps/web
# libs/ui-components
```

### Add More Directories

```bash
# Add additional directories
git sparse-checkout add libs/auth libs/api-client

# List again
git sparse-checkout list
```

### Disable Sparse Checkout

```bash
# Get full repository
git sparse-checkout disable
```

### Performance Benefits

**Before (full checkout):**
```bash
# Clone full repo: 2.5 GB, 50,000 files
git clone https://github.com/org/monorepo.git  # 5 minutes
git status  # 10 seconds
```

**After (sparse checkout):**
```bash
# Clone sparse: 500 MB, 10,000 files
git sparse-checkout set apps/web  # 1 minute
git status  # 1 second
```

---

## CODEOWNERS Setup

### File Location

Create `.github/CODEOWNERS` in repository root.

### Syntax

```
# Pattern                         Owner(s)

# Default owner for everything
*                                 @org/engineering

# Apps ownership
/apps/web/                        @org/web-team
/apps/mobile/                     @org/mobile-team
/apps/admin/                      @org/admin-team

# Libraries ownership
/libs/ui-components/              @org/design-system-team
/libs/auth/                       @org/security-team
/libs/api-client/                 @org/web-team @org/mobile-team

# Infrastructure and CI
/.github/                         @org/devops-team
/infrastructure/                  @org/devops-team
/docker/                          @org/devops-team

# Documentation
/docs/                            @org/tech-writers
*.md                              @org/tech-writers

# Configuration files
package.json                      @org/principal-engineers
tsconfig*.json                    @org/principal-engineers

# Security-critical (require multiple approvals)
/libs/auth/                       @org/security-team @org/principal-engineers
/apps/*/src/config/secrets*       @org/security-team @org/devops-team
```

### Pattern Examples

```
# Match all files
*

# Match directory
/apps/web/

# Match file extension
*.ts

# Match files in any directory
**/*.md

# Match specific file
/package.json

# Match nested directory
/apps/web/src/components/
```

### Multiple Owners

```
# Require approval from both teams
/libs/payments/  @org/payments-team @org/security-team

# Either team can approve
/docs/           @org/tech-writers @org/engineering
```

### Team Structure

**GitHub Organization Teams:**
```
org/
├── engineering
├── web-team
├── mobile-team
├── security-team
├── devops-team
├── design-system-team
└── principal-engineers
```

### Branch Protection

Enforce CODEOWNERS:
```
Settings → Branches → Branch protection rules → main
☑ Require pull request reviews before merging
  ☑ Require review from Code Owners
```

### Testing CODEOWNERS

```bash
# GitHub CLI
gh pr create

# View required reviewers
gh pr view

# Request review from code owners
gh pr review --request @org/web-team
```

---

## Submodules vs Subtrees

### Git Submodules

#### When to Use

Use submodules when:
- ✅ External dependencies you don't control
- ✅ Need strict version pinning
- ✅ Subproject developed separately

#### Setup

```bash
# Add submodule
git submodule add https://github.com/org/shared-lib libs/shared

# Clone repo with submodules
git clone --recurse-submodules https://github.com/org/main-repo

# Initialize submodules in existing repo
git submodule init
git submodule update

# Update submodules to latest
git submodule update --remote

# Update specific submodule
git submodule update --remote libs/shared
```

#### Workflow

```bash
# Make changes in submodule
cd libs/shared
git checkout main
git pull
cd ../..
git add libs/shared
git commit -m "chore: update shared library"

# Push submodule changes
cd libs/shared
git push origin main
cd ../..
git push origin main
```

#### Remove Submodule

```bash
# Deinitialize
git submodule deinit libs/shared

# Remove from Git
git rm libs/shared

# Remove from .git/config
rm -rf .git/modules/libs/shared
```

### Git Subtrees

#### When to Use

Use subtrees when:
- ✅ Want simpler workflow than submodules
- ✅ Need entire history in parent repo
- ✅ Contributors unfamiliar with submodules

#### Setup

```bash
# Add subtree
git subtree add --prefix libs/shared https://github.com/org/shared-lib main --squash

# Pull updates
git subtree pull --prefix libs/shared https://github.com/org/shared-lib main --squash

# Push changes back
git subtree push --prefix libs/shared https://github.com/org/shared-lib main
```

#### Workflow

```bash
# Make changes to subtree
cd libs/shared
# Edit files
cd ../..
git add libs/shared
git commit -m "feat(shared): add new utility"

# Push changes to subtree repo
git subtree push --prefix libs/shared https://github.com/org/shared-lib main

# Pull updates from subtree
git subtree pull --prefix libs/shared https://github.com/org/shared-lib main --squash
```

### Comparison

| Feature | Submodules | Subtrees |
|---------|------------|----------|
| **Clone Complexity** | Requires --recurse-submodules | Normal clone works |
| **History** | Separate history | Merged history |
| **Learning Curve** | High | Medium |
| **Updates** | Explicit (git submodule update) | Pull/push commands |
| **CI/CD** | More complex | Simpler |
| **Best For** | External dependencies | Internal shared code |

### Recommendation

**Avoid both when possible:**
- Use package manager (npm, yarn) for shared libraries
- Use monorepo build tools (Nx, Turborepo)
- Use workspace features (npm workspaces, yarn workspaces)

**Use submodules only for:**
- External dependencies
- Strict version control needed

**Use subtrees only for:**
- Vendoring dependencies
- One-way code sharing

---

## Best Practices

### Git Workflow

**Frequent Commits:**
```bash
# Commit changes to multiple projects atomically
git add apps/web apps/mobile libs/shared
git commit -m "feat: add new authentication flow"
```

**Branch Naming:**
```bash
# Include affected projects
feature/web-mobile-auth-flow
bugfix/api-timeout-issue
refactor/shared-utils-cleanup
```

**PR Size:**
- Keep PRs small (< 500 lines)
- Split large changes across multiple PRs
- Group related changes together

### Code Organization

**Shared Code:**
```
libs/
├── ui-components/     # Shared UI components
├── utils/             # Utility functions
├── types/             # TypeScript types
└── config/            # Configuration
```

**Apps:**
```
apps/
├── web/               # Web application
├── mobile/            # Mobile application
└── admin/             # Admin dashboard
```

### Dependency Management

**Use Workspace Protocol:**
```json
{
  "dependencies": {
    "ui-components": "workspace:*",
    "shared-utils": "workspace:*"
  }
}
```

**Version Pinning:**
```json
{
  "dependencies": {
    "react": "18.2.0",
    "next": "14.0.0"
  }
}
```

### CI/CD Optimization

**Run Only Affected:**
```yaml
# GitHub Actions
- name: Build affected
  run: nx affected:build --base=origin/main

- name: Test affected
  run: nx affected:test --base=origin/main
```

**Cache Dependencies:**
```yaml
- uses: actions/cache@v3
  with:
    path: |
      ~/.npm
      node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

### Performance Tips

**Use Sparse Checkout:**
For large repos, only checkout needed directories.

**Enable Caching:**
Use Nx Cloud or Turbo Remote Cache.

**Parallel Execution:**
```bash
# Nx
nx run-many --target=build --all --parallel=3

# Turborepo
turbo run build --concurrency=3
```

**Prune Dependencies:**
```bash
# Remove unused dependencies
npm prune

# Or with pnpm
pnpm prune
```
