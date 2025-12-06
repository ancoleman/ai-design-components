# Git Hooks Guide

Complete guide to Git hooks for quality gates, including setup, configuration, and examples.

## Table of Contents

1. [Hook Types](#hook-types)
2. [Husky Setup](#husky-setup)
3. [Lint-Staged Configuration](#lint-staged-configuration)
4. [Commitlint Setup](#commitlint-setup)
5. [Pre-Push Hooks](#pre-push-hooks)
6. [Complete Setup Example](#complete-setup-example)
7. [Troubleshooting](#troubleshooting)

## Hook Types

### Client-Side Hooks

| Hook | Trigger | Common Use Cases |
|------|---------|------------------|
| `pre-commit` | Before commit created | Linting, formatting, quick tests |
| `prepare-commit-msg` | After default message | Add issue number, template |
| `commit-msg` | After message written | Validate format, enforce conventions |
| `post-commit` | After commit created | Notifications, logging |
| `pre-push` | Before push to remote | Run tests, prevent force push |
| `pre-rebase` | Before rebase | Prevent rebasing protected branches |

### Server-Side Hooks

| Hook | Trigger | Common Use Cases |
|------|---------|------------------|
| `pre-receive` | Before refs updated | Enforce policies, run checks |
| `update` | Before each ref updated | Per-branch policies |
| `post-receive` | After refs updated | Deploy, notify, CI trigger |

---

## Husky Setup

### Installation

```bash
# Install Husky
npm install --save-dev husky

# Initialize Husky
npx husky init

# This creates:
# - .husky/ directory
# - .husky/pre-commit hook (example)
# - Updates package.json with "prepare" script
```

**package.json:**
```json
{
  "scripts": {
    "prepare": "husky install"
  },
  "devDependencies": {
    "husky": "^8.0.3"
  }
}
```

### Adding Hooks

```bash
# Add pre-commit hook
npx husky add .husky/pre-commit "npm run lint"

# Add commit-msg hook
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit $1'

# Add pre-push hook
npx husky add .husky/pre-push "npm test"
```

### Hook File Structure

**.husky/pre-commit:**
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npm run lint
npm run format
```

Make hooks executable:
```bash
chmod +x .husky/pre-commit
chmod +x .husky/commit-msg
chmod +x .husky/pre-push
```

---

## Lint-Staged Configuration

### Purpose

Run linters only on staged files for performance. Avoids linting entire codebase on every commit.

### Installation

```bash
npm install --save-dev lint-staged
```

### Configuration

**package.json:**
```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yml,yaml}": [
      "prettier --write"
    ],
    "*.css": [
      "stylelint --fix",
      "prettier --write"
    ]
  }
}
```

**Or .lintstagedrc.json:**
```json
{
  "*.{js,jsx,ts,tsx}": [
    "eslint --fix",
    "prettier --write"
  ],
  "*.{json,md,yml,yaml}": [
    "prettier --write"
  ],
  "*.css": [
    "stylelint --fix",
    "prettier --write"
  ]
}
```

### Pre-Commit Hook with Lint-Staged

**.husky/pre-commit:**
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx lint-staged
```

### Advanced Configuration

**Run tests on changed files:**
```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write",
      "jest --bail --findRelatedTests"
    ]
  }
}
```

**Different commands for different directories:**
```json
{
  "lint-staged": {
    "apps/web/**/*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "apps/api/**/*.ts": [
      "eslint --fix",
      "prettier --write",
      "jest --findRelatedTests"
    ],
    "packages/**/*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ]
  }
}
```

---

## Commitlint Setup

### Installation

```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional
```

### Configuration

**commitlint.config.js:**
```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs',
        'style',
        'refactor',
        'perf',
        'test',
        'build',
        'ci',
        'chore',
        'revert'
      ]
    ],
    'subject-case': [2, 'never', ['upper-case', 'pascal-case', 'start-case']],
    'header-max-length': [2, 'always', 100],
    'body-max-line-length': [2, 'always', 72],
    'scope-case': [2, 'always', 'lower-case']
  }
};
```

### Custom Rules

**Allow custom types:**
```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs',
        'style',
        'refactor',
        'perf',
        'test',
        'build',
        'ci',
        'chore',
        'revert',
        'wip',      // Work in progress
        'hotfix'    // Hot fixes
      ]
    ]
  }
};
```

**Enforce scopes:**
```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'scope-enum': [
      2,
      'always',
      ['api', 'ui', 'auth', 'database', 'docs']
    ],
    'scope-empty': [2, 'never']  // Scope required
  }
};
```

### Commit-Msg Hook

**.husky/commit-msg:**
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx --no -- commitlint --edit $1
```

### Testing Commit Messages

```bash
# Test a commit message
echo "feat: add user registration" | npx commitlint

# Test from file
echo "fix(api): resolve timeout" > /tmp/commit.txt
npx commitlint --edit /tmp/commit.txt
```

---

## Pre-Push Hooks

### Run Tests Before Push

**.husky/pre-push:**
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Run test suite
npm run test:ci

# Exit if tests fail
if [ $? -ne 0 ]; then
  echo "❌ Tests failed. Push aborted."
  exit 1
fi
```

### Prevent Force Push to Main

**.husky/pre-push:**
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Get current branch name
branch=$(git rev-parse --abbrev-ref HEAD)

# Check if force pushing to main
if [ "$branch" = "main" ] && git push --dry-run --force 2>&1 | grep -q "force"; then
  echo "⛔ Force push to main branch is not allowed!"
  exit 1
fi

# Run tests
npm run test:ci
```

### Run Only Affected Tests

**.husky/pre-push:**
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Get list of changed files
changed_files=$(git diff --name-only origin/main...HEAD)

# Run tests for changed files
npm run test -- --findRelatedTests $changed_files
```

### Build Before Push

**.husky/pre-push:**
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Run build
npm run build

if [ $? -ne 0 ]; then
  echo "❌ Build failed. Push aborted."
  exit 1
fi

echo "✅ Build successful. Continuing with push."
```

---

## Complete Setup Example

### Full Package Configuration

**package.json:**
```json
{
  "name": "my-project",
  "version": "1.0.0",
  "scripts": {
    "prepare": "husky install",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "lint:fix": "eslint . --ext .js,.jsx,.ts,.tsx --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "test": "jest",
    "test:ci": "jest --coverage --maxWorkers=2",
    "test:changed": "jest --bail --findRelatedTests",
    "build": "tsc && vite build"
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write",
      "jest --bail --findRelatedTests"
    ],
    "*.{json,md,yml,yaml}": [
      "prettier --write"
    ]
  },
  "devDependencies": {
    "husky": "^8.0.3",
    "lint-staged": "^15.0.0",
    "@commitlint/cli": "^18.0.0",
    "@commitlint/config-conventional": "^18.0.0",
    "eslint": "^8.50.0",
    "prettier": "^3.0.0",
    "jest": "^29.7.0",
    "typescript": "^5.2.0"
  }
}
```

### Husky Hooks

**.husky/pre-commit:**
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Run lint-staged (linting + formatting + tests for staged files)
npx lint-staged

# Check for console.log in staged files
if git diff --cached | grep -E "^\+.*console\.log"; then
  echo "⚠️  Warning: console.log found in staged files"
  echo "Remove console.log or use --no-verify to skip this check"
  exit 1
fi
```

**.husky/commit-msg:**
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Validate commit message format
npx --no -- commitlint --edit $1
```

**.husky/pre-push:**
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Get current branch
branch=$(git rev-parse --abbrev-ref HEAD)

# Prevent force push to main
if [ "$branch" = "main" ]; then
  echo "⛔ Cannot push to main branch directly"
  echo "Please create a pull request instead"
  exit 1
fi

# Run full test suite
echo "Running tests before push..."
npm run test:ci

if [ $? -ne 0 ]; then
  echo "❌ Tests failed. Push aborted."
  exit 1
fi

# Run build
echo "Building project..."
npm run build

if [ $? -ne 0 ]; then
  echo "❌ Build failed. Push aborted."
  exit 1
fi

echo "✅ All checks passed. Pushing to remote..."
```

### Commitlint Configuration

**commitlint.config.js:**
```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs',
        'style',
        'refactor',
        'perf',
        'test',
        'build',
        'ci',
        'chore',
        'revert'
      ]
    ],
    'subject-case': [2, 'never', ['upper-case', 'pascal-case', 'start-case']],
    'header-max-length': [2, 'always', 100],
    'body-max-line-length': [2, 'always', 72],
    'scope-case': [2, 'always', 'lower-case'],
    'scope-enum': [
      2,
      'always',
      ['api', 'ui', 'auth', 'database', 'docs', 'infra', 'tests']
    ]
  }
};
```

---

## Advanced Patterns

### Conditional Hooks

Run hooks only for specific branches:

**.husky/pre-commit:**
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

branch=$(git rev-parse --abbrev-ref HEAD)

# Only run on non-main branches
if [ "$branch" != "main" ]; then
  npx lint-staged
fi
```

### Skip Hooks When Needed

```bash
# Skip pre-commit hook
git commit --no-verify -m "fix: urgent hotfix"

# Skip pre-push hook
git push --no-verify
```

**⚠️ Use sparingly:** Only for urgent fixes or when absolutely necessary.

### Shared Hooks in Monorepo

**Root .husky/pre-commit:**
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Run lint-staged in each workspace
npx lerna run --concurrency 1 --stream lint-staged
```

### Performance Optimization

Run only necessary checks:

**.husky/pre-commit:**
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Quick checks only (no tests)
npx lint-staged --config .lintstagedrc.quick.json
```

**.lintstagedrc.quick.json:**
```json
{
  "*.{js,jsx,ts,tsx}": [
    "eslint --fix --max-warnings=0",
    "prettier --write"
  ]
}
```

---

## Troubleshooting

### Hooks Not Running

**Problem:** Hooks don't execute on commit/push

**Solutions:**
```bash
# Reinstall Husky
rm -rf .husky
npx husky init

# Make hooks executable
chmod +x .husky/pre-commit
chmod +x .husky/commit-msg
chmod +x .husky/pre-push

# Verify Git hooks directory
git config core.hooksPath
# Should output: .husky
```

### Slow Pre-Commit Hook

**Problem:** Pre-commit takes too long

**Solutions:**
- Use lint-staged (only check staged files)
- Remove expensive operations (full test suite)
- Run quick checks only (linting, formatting)
- Move slow checks to pre-push or CI

```bash
# Before (slow)
npm run lint      # Lints entire codebase
npm run test      # Runs all tests

# After (fast)
npx lint-staged   # Only staged files
```

### Commitlint Fails Unexpectedly

**Problem:** Valid commits are rejected

**Solutions:**
```bash
# Test commit message
echo "feat: add feature" | npx commitlint

# Check configuration
cat commitlint.config.js

# Use verbose mode
npx commitlint --verbose

# Verify installed version
npx commitlint --version
```

### Windows Line Endings

**Problem:** Hooks fail on Windows (CRLF vs LF)

**Solutions:**
```bash
# Configure Git to handle line endings
git config core.autocrlf false

# Convert existing hooks to LF
dos2unix .husky/*

# Or use .gitattributes
echo "* text=auto eol=lf" >> .gitattributes
echo ".husky/** text eol=lf" >> .gitattributes
```

### Hook Fails in CI/CD

**Problem:** Hooks run in CI when they shouldn't

**Solutions:**
```bash
# Skip Husky in CI
CI=true npm ci  # Husky won't install

# Or in package.json
{
  "scripts": {
    "prepare": "husky install || true"
  }
}

# Or use postinstall for development only
{
  "scripts": {
    "postinstall": "is-ci || husky install"
  }
}
```

### Bypass Hooks for Urgent Fixes

```bash
# Skip all hooks
git commit --no-verify -m "fix: urgent production hotfix"
git push --no-verify

# Better: Fix and commit properly after
git commit --amend --no-edit
# (hooks will run on amend)
```

---

## Best Practices

### Pre-Commit Checks

**Do:**
- ✅ Linting and formatting (fast)
- ✅ Quick static analysis
- ✅ Check for sensitive data (secrets, API keys)

**Don't:**
- ❌ Full test suite (too slow)
- ❌ Build entire project
- ❌ Network requests

### Pre-Push Checks

**Do:**
- ✅ Run test suite
- ✅ Build project
- ✅ Check branch protection

**Don't:**
- ❌ Deploy to production
- ❌ Modify remote repository

### Hook Performance

Keep hooks fast:
- Pre-commit: <5 seconds
- Commit-msg: <1 second
- Pre-push: <30 seconds

### Team Setup

Document hook requirements:
```markdown
# Development Setup

1. Install dependencies: `npm install`
2. Git hooks are automatically installed via Husky
3. Pre-commit runs linting and formatting
4. Commit messages must follow conventional format
5. Pre-push runs tests and builds project

To skip hooks (emergency only): `git commit --no-verify`
```

### Debugging Hooks

Add debug output:
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

echo "🔍 Running pre-commit hook..."
echo "Branch: $(git rev-parse --abbrev-ref HEAD)"
echo "Staged files:"
git diff --cached --name-only

npx lint-staged
```
