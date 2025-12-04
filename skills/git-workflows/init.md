# Git Workflows Skill - Master Plan

**Skill Name:** `git-workflows`
**Skill Level:** Low Level (2,000-5,000 tokens, 300-500 lines)
**Status:** Master Plan (init.md) - Ready for SKILL.md Implementation
**Created:** December 3, 2025
**Research Date:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Git Workflow Taxonomy](#git-workflow-taxonomy)
5. [Decision Framework](#decision-framework)
6. [Branching Strategy Patterns](#branching-strategy-patterns)
7. [Conventional Commits](#conventional-commits)
8. [Merge vs Rebase Patterns](#merge-vs-rebase-patterns)
9. [Monorepo Patterns](#monorepo-patterns)
10. [Git Hooks](#git-hooks)
11. [Code Review Workflows](#code-review-workflows)
12. [Advanced Git Techniques](#advanced-git-techniques)
13. [Tool Recommendations](#tool-recommendations)
14. [Skill Structure Design](#skill-structure-design)
15. [Integration Points](#integration-points)
16. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

**Universal Need:**
- Every software project uses version control
- Git workflows affect team velocity and code quality
- Poor Git practices lead to merge conflicts, lost work, broken builds
- Good workflows enable continuous delivery and team collaboration

**Common Pain Points:**
- Teams adopt GitFlow without understanding if it fits their needs
- Inconsistent commit messages make history hard to navigate
- Merge conflicts from long-lived branches
- Unclear code ownership in monorepos
- Manual release processes prone to errors

**Value Proposition:**
This skill provides decision frameworks for choosing the right Git workflow, implementing conventional commits for automated versioning, managing monorepos effectively, and setting up quality gates via Git hooks.

### Relationship to Other Skills

**Complements:**
- `building-ci-pipelines` - Git workflows trigger CI/CD pipelines
- `writing-github-actions` - GitHub Actions automate Git workflow steps
- `infrastructure-as-code` - IaC repos need structured Git workflows
- `testing-strategies` - Git hooks enforce test requirements
- `security-hardening` - Git hooks prevent secrets from being committed

**Does NOT Overlap:**
- `gitops-workflows` - Focuses on GitOps deployment patterns (not general Git usage)
- `building-ci-pipelines` - Focuses on CI/CD configuration (not Git strategy)

---

## Skill Purpose and Scope

### What This Skill Covers

**Branching Strategies:**
- Trunk-based development
- GitHub Flow
- GitFlow (when appropriate)
- Feature branching patterns

**Commit Conventions:**
- Conventional Commits specification
- Semantic versioning integration
- Automated changelog generation

**Code Review:**
- Pull request templates
- CODEOWNERS files
- Review best practices

**Monorepo Management:**
- Nx and Turborepo patterns
- Sparse checkout for large repos
- Submodules vs subtrees

**Git Hooks:**
- pre-commit (linting, formatting)
- commit-msg (message validation)
- pre-push (testing)

**Advanced Techniques:**
- Cherry-picking for hotfixes
- Interactive rebase for history cleanup
- Git LFS for large files
- Release tagging and versioning

### What This Skill Does NOT Cover

**Out of Scope:**
- CI/CD pipeline configuration → See `building-ci-pipelines`
- GitOps deployment patterns → See `gitops-workflows`
- GitHub Actions workflow files → See `writing-github-actions`
- Git basics (clone, commit, push) → Assumes Git knowledge

---

## Research Findings

### Research Tools Used

**Google Search Grounding (LiteLLM):**
- Query: "Git branching strategies 2025 trunk-based GitFlow GitHub Flow comparison best practices"
- Query: "conventional commits semantic versioning Git commit message best practices 2025"
- Query: "monorepo Git strategies 2025 Nx Turborepo sparse checkout submodules"

**Research Date:** December 3, 2025

### Key Findings Summary

#### 1. Branching Strategies (2025 Trends)

**Trunk-Based Development Rising:**
- High-performing teams increasingly adopt trunk-based development
- Requires strong CI/CD automation and comprehensive testing
- Feature flags enable continuous integration of incomplete features
- Short-lived branches (merged within 1 day) are the norm

**GitFlow Declining:**
- Too complex for modern continuous deployment practices
- High overhead for small to medium teams
- Still valuable for projects with multiple production versions
- Best for scheduled releases with formal QA cycles

**GitHub Flow Dominant:**
- Simple, branch-based workflow
- Main branch always deployable
- Pull request-based code review
- Ideal for web applications with continuous deployment

#### 2. Conventional Commits Widely Adopted

**Standardization:**
- Format: `<type>[optional scope]: <description>`
- Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- `BREAKING CHANGE` in footer or `!` after type for breaking changes

**Automation Benefits:**
- Automatic semantic versioning
- Automated changelog generation
- Better commit history searchability
- Clearer communication within teams

**Tooling:**
- **Commitlint** - Enforces commit message format
- **Husky** - Git hooks for pre-commit validation
- **Semantic Release** - Automates versioning and releases

#### 3. Monorepo Patterns

**Build Tool Advancement:**
- **Nx** and **Turborepo** enable efficient monorepo builds
- Incremental builds and caching critical for performance
- Dependency graph analysis prevents unnecessary rebuilds

**Git Strategies:**
- **Sparse Checkout** - Only clone needed directories
- **CODEOWNERS** - Define ownership per directory
- **Submodules** - Avoid unless necessary (complexity)
- **Subtrees** - Alternative to submodules (merged history)

**Best Practices:**
- Unified tooling (one build system, one linter config)
- No commits to trunk without PR
- Pre-commit hooks enforce standards
- Clear code ownership

#### 4. Git Hooks for Quality Gates

**Common Hooks:**
- **pre-commit** - Run linters, formatters (Prettier, ESLint)
- **commit-msg** - Validate commit message format (Commitlint)
- **pre-push** - Run tests before pushing to remote

**Tools:**
- **Husky** - Simplifies Git hook setup (most popular)
- **lint-staged** - Run linters only on staged files (performance)
- **pre-commit framework** - Python-based hook manager

---

## Git Workflow Taxonomy

### Workflow Classification

```
Git Workflows
│
├── Branching Strategies
│   ├── Trunk-Based Development
│   │   ├── Direct to Trunk (CI/CD mature teams)
│   │   └── Short-Lived Branches (<1 day)
│   │
│   ├── GitHub Flow
│   │   ├── Main Branch (always deployable)
│   │   └── Feature Branches (PR-based review)
│   │
│   ├── GitFlow
│   │   ├── Main + Develop Branches
│   │   ├── Feature Branches
│   │   ├── Release Branches
│   │   └── Hotfix Branches
│   │
│   └── Feature Branching
│       └── Basic feature/* pattern
│
├── Merge Strategies
│   ├── Merge Commits (preserve history)
│   ├── Squash and Merge (clean history)
│   └── Rebase and Merge (linear history)
│
├── Release Strategies
│   ├── Continuous Deployment (every merge)
│   ├── Scheduled Releases (weekly, monthly)
│   └── Manual Releases (tag-based)
│
└── Monorepo Strategies
    ├── Build Tool-Based (Nx, Turborepo)
    ├── Sparse Checkout
    └── Submodules/Subtrees
```

---

## Decision Framework

### Choosing a Branching Strategy

**Use Trunk-Based Development When:**
- ✅ Team has strong CI/CD automation
- ✅ Comprehensive automated test coverage (80%+)
- ✅ Team practices continuous integration
- ✅ Feature flags are used for incomplete features
- ✅ Deployments are frequent (daily or more)
- ✅ Team is experienced with Git and testing

**Example Teams:** Google, Facebook, Netflix (high-velocity engineering)

**Use GitHub Flow When:**
- ✅ Building web applications
- ✅ Main branch always represents production
- ✅ Continuous deployment is the goal
- ✅ Simple, understandable workflow needed
- ✅ Small to medium team size (2-20 developers)
- ✅ Single production environment

**Example Teams:** Startups, SaaS products, open-source projects

**Use GitFlow When:**
- ✅ Multiple production versions supported simultaneously
- ✅ Scheduled releases (monthly, quarterly)
- ✅ Formal QA cycle required before release
- ✅ Hotfixes need to bypass normal release cycle
- ✅ Enterprise environment with change management
- ✅ Mobile apps with App Store release cycles

**Example Teams:** Enterprise software, mobile apps, on-premise software

**Use Feature Branching When:**
- ✅ Team is small (1-5 developers)
- ✅ Simple workflow sufficient
- ✅ No need for complex release management
- ✅ Infrequent deployments acceptable

---

### Choosing Merge vs Rebase

**Use Merge Commits When:**
- ✅ Want to preserve complete history
- ✅ Multiple developers on a feature branch
- ✅ Important to see when feature was integrated
- ✅ Team is less experienced with Git

**Command:**
```bash
git checkout main
git merge feature-branch
```

**Use Squash and Merge When:**
- ✅ Want clean, linear history on main branch
- ✅ Feature branch has many WIP commits
- ✅ Commits on feature branch aren't meaningful individually
- ✅ Each PR represents one logical change

**Command:**
```bash
git checkout main
git merge --squash feature-branch
git commit -m "feat: add user authentication"
```

**Use Rebase When:**
- ✅ Want linear history
- ✅ Working alone on a feature branch
- ✅ Updating feature branch with latest main
- ✅ Cleaning up local commits before PR

**Command:**
```bash
git checkout feature-branch
git rebase main
```

**⚠️ Never Rebase:**
- ❌ Public/shared branches (main, develop)
- ❌ Commits already pushed and used by others
- ❌ After a PR is opened (unless team convention allows)

---

## Branching Strategy Patterns

### 1. Trunk-Based Development

**Branch Structure:**
```
main (trunk)
  ├── feature/short-lived-1 (0-1 days)
  ├── feature/short-lived-2 (0-1 days)
  └── feature/short-lived-3 (0-1 days)
```

**Workflow:**
```bash
# Create short-lived feature branch
git checkout -b feature/add-login main

# Make small changes
git add .
git commit -m "feat: add login form component"

# Update with latest main frequently
git fetch origin
git rebase origin/main

# Push and create PR
git push origin feature/add-login

# After review, merge immediately
# Delete branch after merge
git branch -d feature/add-login
```

**Key Principles:**
- Branches live <24 hours (ideally <4 hours)
- Commit to main multiple times per day
- Feature flags hide incomplete features
- CI/CD runs on every commit to main
- Broken builds are top priority to fix

**Example Feature Flag:**
```javascript
// Hide incomplete feature from users
if (featureFlags.newLogin && user.isBetaTester) {
  return <NewLoginForm />;
}
return <OldLoginForm />;
```

---

### 2. GitHub Flow

**Branch Structure:**
```
main (always deployable)
  ├── feature/user-auth
  ├── feature/payment-integration
  ├── bugfix/login-error
  └── docs/api-documentation
```

**Workflow:**
```bash
# 1. Create feature branch from main
git checkout -b feature/user-auth main

# 2. Make commits
git add .
git commit -m "feat: add JWT authentication"
git commit -m "test: add auth middleware tests"
git commit -m "docs: update API authentication docs"

# 3. Push and open PR
git push origin feature/user-auth
# Open PR on GitHub

# 4. Code review and discussion
# Make changes based on feedback
git add .
git commit -m "fix: handle expired tokens"
git push origin feature/user-auth

# 5. Merge to main after approval
# (via GitHub UI - squash and merge)

# 6. Deploy immediately
# (automated via CI/CD)

# 7. Delete branch
git branch -d feature/user-auth
git push origin --delete feature/user-auth
```

**Key Principles:**
- Main branch is always deployable
- Every merge triggers deployment
- Comprehensive tests required
- Code review via pull requests
- Branch naming convention: `type/description`

---

### 3. GitFlow

**Branch Structure:**
```
main (production)
  └── tag: v1.0.0, v1.1.0, v2.0.0
develop (integration)
  ├── feature/user-profile
  ├── feature/notifications
  └── feature/settings
release/1.1.0 (release prep)
hotfix/critical-bug (urgent fixes)
```

**Workflow:**
```bash
# Initialize GitFlow
git checkout -b develop main

# Create feature branch
git checkout -b feature/user-profile develop

# Develop feature
git add .
git commit -m "feat: add user profile page"

# Merge feature to develop
git checkout develop
git merge --no-ff feature/user-profile
git branch -d feature/user-profile

# Create release branch
git checkout -b release/1.1.0 develop

# Prepare release (version bumps, changelog)
git commit -m "chore: bump version to 1.1.0"

# Merge release to main
git checkout main
git merge --no-ff release/1.1.0
git tag -a v1.1.0 -m "Release version 1.1.0"

# Merge release back to develop
git checkout develop
git merge --no-ff release/1.1.0
git branch -d release/1.1.0

# Hotfix workflow
git checkout -b hotfix/critical-bug main
git commit -m "fix: resolve critical security issue"
git checkout main
git merge --no-ff hotfix/critical-bug
git tag -a v1.1.1 -m "Hotfix version 1.1.1"
git checkout develop
git merge --no-ff hotfix/critical-bug
git branch -d hotfix/critical-bug
```

**Key Principles:**
- Main and develop are long-lived branches
- Features branch from develop
- Releases branch from develop, merge to main and develop
- Hotfixes branch from main, merge to main and develop
- Tags mark production releases

---

## Conventional Commits

### Specification

**Format:**
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Examples:**
```bash
# Feature with scope
git commit -m "feat(auth): add JWT token validation"

# Bug fix
git commit -m "fix: resolve race condition in user login"

# Breaking change
git commit -m "feat!: redesign authentication API

BREAKING CHANGE: Auth endpoints now require API version header"

# Multiple paragraphs
git commit -m "refactor(database): migrate to PostgreSQL

- Migrate from MySQL to PostgreSQL
- Update ORM configuration
- Add migration scripts

Refs: #123"
```

### Commit Types

| Type | Description | SemVer Impact |
|------|-------------|---------------|
| `feat` | New feature | MINOR (0.1.0) |
| `fix` | Bug fix | PATCH (0.0.1) |
| `docs` | Documentation only | - |
| `style` | Formatting, missing semicolons | - |
| `refactor` | Code restructuring (no feature change) | - |
| `perf` | Performance improvement | PATCH |
| `test` | Adding/updating tests | - |
| `build` | Build system changes (webpack, npm) | - |
| `ci` | CI/CD configuration changes | - |
| `chore` | Maintenance tasks | - |
| `revert` | Revert previous commit | - |

**Breaking Changes:**
- Add `!` after type: `feat!:` or `fix!:`
- Add `BREAKING CHANGE:` in footer
- Impact: MAJOR version bump (1.0.0)

### Scopes (Optional)

**Examples:**
- `feat(api): add user endpoints`
- `fix(ui): resolve button alignment`
- `test(auth): add integration tests`
- `docs(readme): update installation steps`

**Benefits of Scopes:**
- Easier to filter commits by area
- Clearer changelog organization
- Better understanding of impact

---

### Semantic Versioning Integration

**Version Format:** `MAJOR.MINOR.PATCH`

**Version Bumping:**
```
feat: add feature          → 1.2.0 to 1.3.0 (MINOR)
fix: fix bug               → 1.2.0 to 1.2.1 (PATCH)
feat!: breaking change     → 1.2.0 to 2.0.0 (MAJOR)
BREAKING CHANGE: in footer → 1.2.0 to 2.0.0 (MAJOR)
```

**Automated Versioning:**
```bash
# Using semantic-release
npm install --save-dev semantic-release

# .releaserc.json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/npm",
    "@semantic-release/git",
    "@semantic-release/github"
  ]
}
```

**Automated Changelog:**
```markdown
# Changelog

## [2.0.0] - 2025-12-03

### ⚠ BREAKING CHANGES

* **api**: redesign authentication endpoints

### Features

* **auth**: add JWT token validation ([a1b2c3d](link))
* **api**: add user profile endpoints ([e4f5g6h](link))

### Bug Fixes

* **ui**: resolve button alignment issue ([i7j8k9l](link))
* resolve race condition in login ([m0n1o2p](link))
```

---

## Merge vs Rebase Patterns

### When to Use Each Strategy

**Merge Commit (Preserve History):**
```bash
git checkout main
git merge feature-branch

# Creates merge commit
# Preserves all feature branch commits
# Maintains context of when feature was integrated
```

**Visualization:**
```
    C---D   feature-branch
   /     \
  A---B---E  main
```

**Use Cases:**
- Large features with multiple developers
- Important to preserve complete history
- Team collaboration on feature branches

---

**Squash and Merge (Clean History):**
```bash
git checkout main
git merge --squash feature-branch
git commit -m "feat: add user authentication"

# Combines all feature commits into one
# Cleaner main branch history
# Loses individual commit details
```

**Visualization:**
```
Before:           After:
    C---D           A---B---E
   /                    (E = C+D squashed)
  A---B
```

**Use Cases:**
- Many WIP commits on feature branch
- Feature branch commits aren't meaningful
- Want clean changelog

---

**Rebase (Linear History):**
```bash
git checkout feature-branch
git rebase main

# Replays feature commits on top of main
# Creates linear history (no merge commits)
# Rewrites commit history
```

**Visualization:**
```
Before:           After:
    C---D           A---B---E---C'---D'
   /
  A---B---E
```

**Use Cases:**
- Updating feature branch with latest main
- Cleaning up commit history before PR
- Solo developer on feature branch

**⚠️ Golden Rule:** Never rebase public branches (main, develop, shared feature branches)

---

### Interactive Rebase for History Cleanup

```bash
# Clean up last 3 commits before opening PR
git rebase -i HEAD~3

# Opens editor with:
pick a1b2c3d feat: add login form
pick e4f5g6h WIP: fix typo
pick i7j8k9l test: add login tests

# Edit to:
pick a1b2c3d feat: add login form
fixup e4f5g6h WIP: fix typo        # Squash into previous
pick i7j8k9l test: add login tests

# Result: 2 clean commits instead of 3
```

**Interactive Rebase Commands:**
- `pick` - Keep commit as-is
- `reword` - Keep commit, edit message
- `edit` - Keep commit, pause for amendments
- `squash` - Combine with previous, keep both messages
- `fixup` - Combine with previous, discard this message
- `drop` - Remove commit entirely

---

## Monorepo Patterns

### Monorepo vs Polyrepo

**Monorepo Benefits:**
- ✅ Atomic commits across multiple projects
- ✅ Easier refactoring (see all usage)
- ✅ Shared tooling and dependencies
- ✅ Single source of truth

**Monorepo Challenges:**
- ❌ Large repository size
- ❌ Slower git operations
- ❌ More complex CI/CD
- ❌ Code ownership ambiguity

---

### Build Tool Strategies

**1. Nx (Recommended for TypeScript/JavaScript)**

```bash
# Install Nx
npx create-nx-workspace@latest myworkspace

# Project structure
monorepo/
├── apps/
│   ├── web-app/
│   └── mobile-app/
├── libs/
│   ├── ui-components/
│   ├── auth/
│   └── shared-utils/
├── nx.json
└── package.json

# Run affected commands (only rebuild changed projects)
nx affected:build --base=main
nx affected:test --base=main
nx affected:lint --base=main
```

**Nx Benefits:**
- Dependency graph analysis
- Incremental builds (only rebuild affected)
- Caching across machines
- Integrated tooling (ESLint, Jest, etc.)

---

**2. Turborepo (Recommended for Next.js/React)**

```bash
# Install Turborepo
npx create-turbo@latest

# Project structure
monorepo/
├── apps/
│   ├── web/
│   └── docs/
├── packages/
│   ├── ui/
│   ├── config/
│   └── tsconfig/
├── turbo.json
└── package.json

# turbo.json configuration
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "dist/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "cache": false
    }
  }
}

# Run tasks
npx turbo run build      # Build all projects
npx turbo run build --filter=web  # Build specific project
```

**Turborepo Benefits:**
- Fast incremental builds
- Remote caching
- Simple configuration
- Works well with npm/yarn/pnpm workspaces

---

### Git Sparse Checkout

**Use Case:** Large monorepo, developers only need subset

```bash
# Enable sparse checkout
git clone --no-checkout https://github.com/org/monorepo.git
cd monorepo
git sparse-checkout init --cone

# Checkout only specific directories
git sparse-checkout set apps/web libs/ui-components

# Now only these directories are in working tree
git checkout main

# List current sparse checkout
git sparse-checkout list

# Disable sparse checkout (get full repo)
git sparse-checkout disable
```

**Benefits:**
- Faster `git status`, `git add`, `git commit`
- IDEs don't index unnecessary files
- Smaller working directory

---

### CODEOWNERS for Monorepos

**File:** `.github/CODEOWNERS`

```bash
# Default owners for everything
* @org/engineering

# Apps ownership
/apps/web/ @org/web-team
/apps/mobile/ @org/mobile-team

# Libs ownership
/libs/ui-components/ @org/design-system-team
/libs/auth/ @org/security-team

# Infra and CI
/.github/ @org/devops-team
/infrastructure/ @org/devops-team

# Docs
/docs/ @org/tech-writers

# Require multiple approvals for critical areas
/libs/auth/ @org/security-team @org/principal-engineers
```

**Benefits:**
- Automatic PR reviewer assignment
- Clear ownership boundaries
- Enforced approvals for critical code

---

### Submodules vs Subtrees

**Git Submodules:**
```bash
# Add submodule
git submodule add https://github.com/org/shared-lib libs/shared

# Clone repo with submodules
git clone --recurse-submodules https://github.com/org/main-repo

# Update submodules
git submodule update --remote

# Remove submodule
git submodule deinit libs/shared
git rm libs/shared
```

**When to Use Submodules:**
- ✅ External dependencies you don't control
- ✅ Need strict version pinning
- ✅ Subproject developed separately

**When to Avoid:**
- ❌ Frequently edit both parent and submodule
- ❌ Simple CI/CD needed
- ❌ Team unfamiliar with Git

**Git Subtrees (Alternative):**
```bash
# Add subtree
git subtree add --prefix libs/shared https://github.com/org/shared-lib main

# Pull updates
git subtree pull --prefix libs/shared https://github.com/org/shared-lib main

# Push changes back
git subtree push --prefix libs/shared https://github.com/org/shared-lib main
```

**Subtree Benefits:**
- Simpler than submodules (no special clone command)
- Entire history in parent repo
- Better for contributors

**Recommendation:** Avoid both if possible. Use monorepo tooling (Nx/Turborepo) or package manager.

---

## Git Hooks

### Hook Types

| Hook | When Triggered | Use Case |
|------|----------------|----------|
| `pre-commit` | Before commit is created | Linting, formatting, tests |
| `prepare-commit-msg` | After default message created | Add issue number, template |
| `commit-msg` | After commit message written | Validate message format |
| `post-commit` | After commit is created | Notifications |
| `pre-push` | Before push to remote | Run tests, prevent force push |
| `pre-rebase` | Before rebase | Prevent rebasing protected branches |

---

### Husky Setup (Most Popular)

```bash
# Install Husky
npm install --save-dev husky
npx husky init

# Add pre-commit hook
npx husky add .husky/pre-commit "npm run lint"

# .husky/pre-commit
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npm run lint
npm run test
```

**Run linters only on staged files (lint-staged):**
```bash
npm install --save-dev lint-staged

# package.json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}

# .husky/pre-commit
npx lint-staged
```

---

### Commitlint Setup

```bash
# Install commitlint
npm install --save-dev @commitlint/cli @commitlint/config-conventional

# commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'build', 'ci', 'chore', 'revert'
    ]],
    'subject-case': [2, 'never', ['upper-case']],
    'header-max-length': [2, 'always', 100]
  }
};

# Add commit-msg hook
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit $1'
```

**Example Validation:**
```bash
# ✅ Valid
git commit -m "feat: add user authentication"
git commit -m "fix(api): resolve timeout issue"

# ❌ Invalid
git commit -m "Add user authentication"  # Missing type
git commit -m "FEAT: add auth"  # Uppercase type
git commit -m "feat add auth"  # Missing colon
```

---

### Pre-push Hook (Run Tests)

```bash
# .husky/pre-push
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Run tests before pushing
npm run test

# Prevent accidental force push to main
branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$branch" = "main" ]; then
  echo "⛔ Cannot force push to main branch"
  exit 1
fi
```

---

### Example: Complete Hook Setup

```bash
# package.json
{
  "scripts": {
    "prepare": "husky install",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "format": "prettier --write .",
    "test": "jest",
    "test:ci": "jest --coverage --maxWorkers=2"
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yml}": ["prettier --write"]
  },
  "devDependencies": {
    "husky": "^8.0.3",
    "lint-staged": "^15.0.0",
    "@commitlint/cli": "^18.0.0",
    "@commitlint/config-conventional": "^18.0.0"
  }
}

# .husky/pre-commit
npx lint-staged

# .husky/commit-msg
npx --no -- commitlint --edit $1

# .husky/pre-push
npm run test:ci
```

---

## Code Review Workflows

### Pull Request Templates

**File:** `.github/PULL_REQUEST_TEMPLATE.md`

```markdown
## Description
<!-- Brief description of changes -->

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## How Has This Been Tested?
<!-- Describe the tests you ran -->

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Screenshots (if applicable)

## Related Issues
<!-- Link to related issues: Closes #123 -->
```

---

### Branch Protection Rules

**Enforce via GitHub Settings:**
```yaml
# Example branch protection for 'main'
- Require pull request before merging
  - Require approvals: 2
  - Dismiss stale approvals
  - Require review from Code Owners

- Require status checks to pass
  - Build
  - Tests
  - Lint
  - Security Scan

- Require branches to be up to date before merging
- Require signed commits
- Include administrators (no bypass)
- Restrict force pushes
- Restrict deletions
```

---

## Advanced Git Techniques

### Cherry-Picking for Hotfixes

```bash
# Scenario: Critical bug fix on main needs to go to release branch

# 1. Fix bug on main
git checkout main
git commit -m "fix: resolve critical security issue"
# Commit hash: a1b2c3d

# 2. Cherry-pick to release branch
git checkout release/1.5
git cherry-pick a1b2c3d

# 3. If conflicts, resolve and continue
git add .
git cherry-pick --continue

# Alternative: Cherry-pick multiple commits
git cherry-pick a1b2c3d..e4f5g6h
```

**Use Cases:**
- Backporting fixes to older releases
- Applying hotfixes to multiple branches
- Selective feature porting

---

### Git LFS for Large Files

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.psd"
git lfs track "*.mp4"
git lfs track "assets/**"

# .gitattributes (auto-created)
*.psd filter=lfs diff=lfs merge=lfs -text
*.mp4 filter=lfs diff=lfs merge=lfs -text

# Commit and push
git add .gitattributes
git add large-file.psd
git commit -m "feat: add design mockups"
git push origin main

# Clone with LFS
git lfs clone https://github.com/org/repo.git
```

**Benefits:**
- Git repo stays small (stores pointers, not files)
- Large files stored on LFS server
- Faster clones and fetches

**Use Cases:**
- Design files (PSD, Sketch, Figma exports)
- Videos and images
- ML models and datasets
- Compiled binaries

---

### Release Tagging

```bash
# Create annotated tag
git tag -a v1.2.0 -m "Release version 1.2.0"

# Push tag to remote
git push origin v1.2.0

# Push all tags
git push origin --tags

# List tags
git tag -l "v1.*"

# Checkout specific tag
git checkout v1.2.0

# Delete tag
git tag -d v1.2.0
git push origin --delete v1.2.0

# Create tag from specific commit
git tag -a v1.2.0 a1b2c3d -m "Release version 1.2.0"
```

**Tag Naming Conventions:**
- `v1.2.3` - Semantic versioning
- `v1.2.3-beta.1` - Pre-release
- `v1.2.3-rc.1` - Release candidate

---

### Automated Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Test
        run: npm test

      - name: Semantic Release
        run: npx semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**Semantic Release:**
- Analyzes commits since last release
- Determines version bump (MAJOR, MINOR, PATCH)
- Generates changelog
- Creates Git tag
- Publishes to npm (if configured)
- Creates GitHub release

---

## Tool Recommendations

### Essential Tools

**1. Husky (Git Hooks)**
- **Purpose:** Simplify Git hook management
- **Why:** Most popular, zero-config, works with all Git hooks
- **Installation:** `npm install --save-dev husky`
- **Alternatives:** pre-commit (Python), lefthook (Go)

**2. Commitlint (Commit Message Validation)**
- **Purpose:** Enforce conventional commit format
- **Why:** Industry standard, integrates with semantic-release
- **Installation:** `npm install --save-dev @commitlint/cli @commitlint/config-conventional`

**3. Lint-staged (Performance)**
- **Purpose:** Run linters only on staged files
- **Why:** Much faster than linting entire codebase
- **Installation:** `npm install --save-dev lint-staged`

**4. Semantic Release (Automated Versioning)**
- **Purpose:** Automate versioning, changelog, releases
- **Why:** Eliminates manual version management
- **Installation:** `npm install --save-dev semantic-release`

---

### Monorepo Build Tools

**1. Nx (Recommended for TypeScript/JavaScript)**
- **Trust Score:** High (used by Google, AWS)
- **Best For:** Large TypeScript/JavaScript monorepos
- **Features:** Dependency graph, affected commands, caching
- **Installation:** `npx create-nx-workspace@latest`

**2. Turborepo (Recommended for Next.js/React)**
- **Trust Score:** High (acquired by Vercel)
- **Best For:** Next.js, React applications
- **Features:** Fast incremental builds, remote caching
- **Installation:** `npx create-turbo@latest`

**3. Lerna (Legacy - Consider Nx/Turborepo)**
- **Status:** Maintenance mode (consider alternatives)
- **Best For:** Existing Lerna projects
- **Migration:** Nx provides Lerna compatibility layer

---

### Comparison Matrix

| Tool | Purpose | Bundle Size | Best For |
|------|---------|-------------|----------|
| **Husky** | Git hooks | ~5KB | All projects |
| **Commitlint** | Message validation | ~10KB | Teams using conventional commits |
| **Lint-staged** | Performance | ~5KB | Large codebases |
| **Semantic Release** | Automation | ~50KB | Projects with frequent releases |
| **Nx** | Monorepo builds | ~500KB | TypeScript monorepos |
| **Turborepo** | Monorepo builds | ~100KB | Next.js/React monorepos |

---

## Skill Structure Design

### Progressive Disclosure Architecture

**Level 1: SKILL.md (Main File)**
- Overview and quick decision tree
- When to use which branching strategy
- Common workflows (< 200 lines)
- References to detailed guides

**Level 2: Reference Files**
```
git-workflows/
├── SKILL.md                          # Main skill file (200 lines)
├── references/
│   ├── branching-strategies.md       # Detailed branching patterns
│   ├── conventional-commits.md       # Full commit spec
│   ├── monorepo-patterns.md          # Monorepo strategies
│   ├── git-hooks-guide.md            # Hook setup and examples
│   └── code-review-workflows.md      # PR templates, CODEOWNERS
├── examples/
│   ├── github-flow-example.sh        # Complete workflow example
│   ├── gitflow-example.sh            # GitFlow commands
│   ├── husky-setup/                  # Hook configuration examples
│   └── pr-templates/                 # PR template examples
└── scripts/
    ├── validate-commit-msg.sh        # Commit message validator
    ├── check-branch-name.sh          # Branch naming validator
    └── setup-hooks.sh                # Automated hook setup
```

**Level 3: Executable Scripts**
- Commit message validation (token-free execution)
- Branch name validation
- Automated hook setup

---

### Decision Tree for SKILL.md

```
User asks about Git workflow
│
├─→ "Which branching strategy?" → Decision framework section
├─→ "How to write commits?" → Conventional commits reference
├─→ "Monorepo management?" → Monorepo patterns reference
├─→ "Setup Git hooks?" → Git hooks guide + setup script
├─→ "Code review process?" → Code review workflows reference
└─→ "Cherry-pick/rebase/etc?" → Advanced techniques reference
```

---

## Integration Points

### Complements Other Skills

**1. building-ci-pipelines**
- Git workflows trigger CI/CD pipelines
- Branch protection rules enforce CI checks
- Conventional commits enable automated releases

**2. writing-github-actions**
- GitHub Actions automate Git workflow steps
- Release workflow uses tags from Git
- PR workflows use branch naming conventions

**3. infrastructure-as-code**
- IaC repos need structured workflows
- Terraform state in Git requires careful branching
- GitOps uses Git as source of truth

**4. testing-strategies**
- Git hooks enforce test requirements
- Pre-push hooks run test suites
- Conventional commits distinguish test-only changes

**5. security-hardening**
- Git hooks prevent secrets in commits
- Signed commits verify author identity
- CODEOWNERS enforce security reviews

---

## Implementation Roadmap

### Phase 1: Core SKILL.md (Week 1)
- [ ] Write main SKILL.md file (200 lines)
- [ ] Create decision framework (which strategy when)
- [ ] Add quick reference for each branching strategy
- [ ] Include conventional commits quick guide

### Phase 2: Reference Documentation (Week 2)
- [ ] `branching-strategies.md` - Detailed patterns with examples
- [ ] `conventional-commits.md` - Full specification
- [ ] `git-hooks-guide.md` - Hook setup and configuration
- [ ] `code-review-workflows.md` - PR templates, CODEOWNERS

### Phase 3: Monorepo Patterns (Week 3)
- [ ] `monorepo-patterns.md` - Nx, Turborepo, sparse checkout
- [ ] Add CODEOWNERS examples
- [ ] Document submodules vs subtrees

### Phase 4: Examples and Scripts (Week 4)
- [ ] Create workflow example scripts
- [ ] Write commit message validator script
- [ ] Create automated hook setup script
- [ ] Add PR template examples

### Phase 5: Testing and Refinement (Week 5)
- [ ] Test with real Git repositories
- [ ] Validate scripts on multiple OS (macOS, Linux, Windows)
- [ ] Gather feedback from developers
- [ ] Iterate based on usage patterns

---

## Success Metrics

**Skill Effectiveness:**
- ✅ Developers choose appropriate branching strategy
- ✅ 90%+ commits follow conventional format
- ✅ Git hooks prevent common errors (secrets, linting)
- ✅ Automated releases reduce manual work
- ✅ Code review process is consistent

**Skill Efficiency:**
- ✅ SKILL.md under 200 lines
- ✅ Developers find answers in <30 seconds
- ✅ Scripts execute without loading into context
- ✅ Reference files loaded only when needed

---

## Appendix: Research Sources

**Research Date:** December 3, 2025

**Google Search Grounding Results:**

1. **Git Branching Strategies 2025:**
   - Trunk-based development rising among high-performing teams
   - GitFlow declining due to complexity
   - GitHub Flow dominant for web applications
   - Feature flags enable continuous integration

2. **Conventional Commits:**
   - Standard format: `<type>[scope]: <description>`
   - Semantic versioning integration
   - Tools: Commitlint, Semantic Release, Husky
   - Automated changelog generation

3. **Monorepo Patterns:**
   - Nx and Turborepo leading build tools
   - Sparse checkout for large repositories
   - CODEOWNERS for code ownership
   - Avoid submodules when possible

**Tools Validated:**
- Husky (most popular Git hooks tool)
- Commitlint (commit message validation)
- Lint-staged (performance optimization)
- Semantic Release (automated versioning)
- Nx (TypeScript/JavaScript monorepos)
- Turborepo (Next.js/React monorepos)

---

## Next Steps

**To Create SKILL.md:**
1. Read this init.md for context
2. Extract decision framework (which strategy when)
3. Create concise main file (<200 lines)
4. Use progressive disclosure for detailed content
5. Write validation scripts (commit message, branch name)
6. Test on real repositories

**Key Principles for SKILL.md:**
- Be concise (only what Claude doesn't know)
- Use imperative form ("To create a feature branch...")
- Provide clear decision criteria
- Reference detailed guides when needed
- Include working code examples

---

**This master plan provides a comprehensive foundation for implementing the `git-workflows` skill. The research validates current best practices (2025), and the structure enables progressive disclosure for token efficiency.**
