# Conventional Commits Specification

Complete guide to conventional commit format for automated versioning and changelog generation.

## Table of Contents

1. [Specification](#specification)
2. [Commit Types](#commit-types)
3. [Scopes](#scopes)
4. [Breaking Changes](#breaking-changes)
5. [Semantic Versioning Integration](#semantic-versioning-integration)
6. [Tool Setup](#tool-setup)
7. [Examples](#examples)

## Specification

### Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Components

**Type** (required): Category of change
**Scope** (optional): Area of codebase affected
**Description** (required): Short summary (imperative mood)
**Body** (optional): Detailed explanation
**Footer** (optional): Breaking changes, issue references

### Rules

1. Type and description are mandatory
2. Type must be lowercase
3. Description must be lowercase (no capitalization)
4. No period at end of description
5. Body separated by blank line
6. Footer separated by blank line
7. Line length: header ≤100 chars, body ≤72 chars

---

## Commit Types

### Core Types

| Type | Description | Changelog | SemVer Impact |
|------|-------------|-----------|---------------|
| `feat` | New feature | ✅ Yes | MINOR (0.1.0) |
| `fix` | Bug fix | ✅ Yes | PATCH (0.0.1) |
| `docs` | Documentation only | ❌ No | - |
| `style` | Formatting, whitespace | ❌ No | - |
| `refactor` | Code change (no feature/fix) | ❌ No | - |
| `perf` | Performance improvement | ✅ Yes | PATCH (0.0.1) |
| `test` | Adding or updating tests | ❌ No | - |
| `build` | Build system changes | ❌ No | - |
| `ci` | CI configuration changes | ❌ No | - |
| `chore` | Maintenance tasks | ❌ No | - |
| `revert` | Revert previous commit | ✅ Yes | Context-dependent |

### Type Guidelines

#### feat (Feature)

New functionality visible to users:
```bash
feat: add user registration
feat(auth): add password reset flow
feat(api): add pagination to user endpoint
```

**Not a feature:**
- Internal refactoring
- Test improvements
- Build changes

#### fix (Bug Fix)

Fixes user-facing bug:
```bash
fix: resolve login redirect loop
fix(ui): correct button alignment on mobile
fix(api): handle null values in response
```

**Not a fix:**
- Fixing tests
- Fixing CI
- Code cleanup

#### docs (Documentation)

Documentation changes only:
```bash
docs: update installation instructions
docs(api): add authentication examples
docs: fix typo in README
```

**Scope:**
- README updates
- API documentation
- Code comments
- Migration guides

#### style (Code Style)

Formatting changes (no logic change):
```bash
style: format code with prettier
style: fix indentation in user controller
style: remove trailing whitespace
```

**Examples:**
- Prettier/ESLint formatting
- Import order changes
- Whitespace cleanup

#### refactor (Code Refactoring)

Code restructuring without feature/fix:
```bash
refactor: extract user validation logic
refactor(auth): simplify token generation
refactor: rename variables for clarity
```

**Not a refactor:**
- Adding new functionality → `feat`
- Fixing bugs → `fix`

#### perf (Performance)

Performance improvements:
```bash
perf: reduce database query time by 50%
perf(api): add caching to user endpoint
perf: optimize image loading
```

#### test (Tests)

Adding or updating tests:
```bash
test: add unit tests for user service
test(auth): add integration tests
test: increase coverage to 80%
```

#### build (Build System)

Changes to build configuration:
```bash
build: upgrade webpack to v5
build: add source maps to production build
build(deps): update dependencies
```

**Examples:**
- Webpack configuration
- Babel configuration
- Package.json scripts

#### ci (Continuous Integration)

CI configuration changes:
```bash
ci: add GitHub Actions workflow
ci: increase test timeout
ci: add caching to CI pipeline
```

**Examples:**
- GitHub Actions
- Jenkins
- CircleCI
- GitLab CI

#### chore (Maintenance)

Maintenance tasks:
```bash
chore: update .gitignore
chore: bump version to 1.2.0
chore(deps): update dev dependencies
```

#### revert (Revert Commit)

Reverting previous commit:
```bash
revert: feat(auth): add social login

This reverts commit a1b2c3d4e5f6.
```

---

## Scopes

### Purpose

Scopes indicate which part of codebase is affected. Use when repository has clear module boundaries.

### Format

```bash
<type>(<scope>): <description>
```

### Common Scopes

**By Module:**
```bash
feat(auth): add JWT validation
fix(api): resolve timeout issue
test(database): add migration tests
```

**By Layer:**
```bash
feat(frontend): add user dashboard
fix(backend): resolve memory leak
docs(infrastructure): update deployment guide
```

**By Feature:**
```bash
feat(notifications): add email notifications
fix(payments): resolve Stripe integration
refactor(analytics): simplify event tracking
```

### Scope Examples by Project Type

**Web Application:**
- `ui`, `api`, `auth`, `database`, `cache`

**Library:**
- `core`, `utils`, `types`, `validation`

**Monorepo:**
- `web`, `mobile`, `shared`, `api`, `admin`

### Multiple Scopes

Use comma separation for changes affecting multiple areas:
```bash
refactor(api,database): migrate to PostgreSQL
```

Or omit scope if change is global:
```bash
refactor: migrate to PostgreSQL
```

---

## Breaking Changes

### Format

Add `!` after type/scope:
```bash
feat!: redesign authentication API
feat(api)!: change user endpoint response format
```

And/or add `BREAKING CHANGE:` in footer:
```bash
feat(api): redesign authentication endpoints

BREAKING CHANGE: Auth endpoints now require API version header.
Migration guide: https://docs.example.com/v2-migration
```

### When to Use

Mark as breaking change when:
- API contract changes
- Function signature changes
- Configuration format changes
- Database schema migrations required
- Behavior change affects existing users

### Examples

**API Change:**
```bash
feat(api)!: change user response format

BREAKING CHANGE: User API now returns nested objects.

Before:
{
  "id": 1,
  "name": "John",
  "email": "john@example.com"
}

After:
{
  "id": 1,
  "profile": {
    "name": "John",
    "email": "john@example.com"
  }
}
```

**Configuration Change:**
```bash
refactor(config)!: change configuration file format

BREAKING CHANGE: Configuration now uses YAML instead of JSON.
Rename config.json to config.yml and update syntax.
```

**Function Signature:**
```bash
feat(auth)!: change login function signature

BREAKING CHANGE: login() now returns Promise instead of callback.

Before: login(credentials, callback)
After: await login(credentials)
```

---

## Semantic Versioning Integration

### Version Format

`MAJOR.MINOR.PATCH` (e.g., 2.1.3)

### Version Bumping

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat:` | MINOR | 1.2.0 → 1.3.0 |
| `fix:` | PATCH | 1.2.0 → 1.2.1 |
| `perf:` | PATCH | 1.2.0 → 1.2.1 |
| `feat!:` or `BREAKING CHANGE:` | MAJOR | 1.2.0 → 2.0.0 |

### Pre-1.0.0 Versions

Before 1.0.0, breaking changes bump MINOR:
```
0.2.0 → 0.3.0 (breaking change)
0.2.0 → 0.2.1 (fix)
```

### Examples

**Patch Release (1.2.0 → 1.2.1):**
```
fix: resolve login timeout
fix(api): handle null responses
perf: optimize database queries
```

**Minor Release (1.2.0 → 1.3.0):**
```
feat: add dark mode
feat(notifications): add email notifications
fix: resolve various bugs
```

**Major Release (1.2.0 → 2.0.0):**
```
feat!: redesign API
BREAKING CHANGE: API v1 endpoints removed
```

---

## Tool Setup

### Commitlint Installation

```bash
# Install commitlint
npm install --save-dev @commitlint/cli @commitlint/config-conventional

# Create configuration file
echo "module.exports = { extends: ['@commitlint/config-conventional'] };" > commitlint.config.js
```

### Commitlint Configuration

**commitlint.config.js:**
```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Type enumeration
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'build', 'ci', 'chore', 'revert'
    ]],

    // Subject case (lowercase)
    'subject-case': [2, 'never', ['upper-case', 'pascal-case', 'start-case']],

    // Header max length
    'header-max-length': [2, 'always', 100],

    // Body max line length
    'body-max-line-length': [2, 'always', 72],

    // Scope case (lowercase)
    'scope-case': [2, 'always', 'lower-case'],

    // Empty subject not allowed
    'subject-empty': [2, 'never'],

    // Subject must not end with period
    'subject-full-stop': [2, 'never', '.']
  }
};
```

### Husky Integration

```bash
# Install Husky
npm install --save-dev husky
npx husky init

# Add commit-msg hook
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit $1'
```

**.husky/commit-msg:**
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx --no -- commitlint --edit $1
```

### Validation Examples

**Valid commits:**
```bash
git commit -m "feat: add user registration"
✅ PASS

git commit -m "fix(auth): resolve login timeout"
✅ PASS

git commit -m "feat!: redesign API"
✅ PASS
```

**Invalid commits:**
```bash
git commit -m "Add user registration"
❌ FAIL: type missing

git commit -m "FEAT: add registration"
❌ FAIL: type must be lowercase

git commit -m "feat add registration"
❌ FAIL: missing colon

git commit -m "feat: Add registration"
❌ FAIL: description must be lowercase
```

---

## Semantic Release Setup

### Installation

```bash
npm install --save-dev semantic-release \
  @semantic-release/commit-analyzer \
  @semantic-release/release-notes-generator \
  @semantic-release/changelog \
  @semantic-release/npm \
  @semantic-release/git \
  @semantic-release/github
```

### Configuration

**.releaserc.json:**
```json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/npm",
    [
      "@semantic-release/git",
      {
        "assets": ["package.json", "CHANGELOG.md"],
        "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
      }
    ],
    "@semantic-release/github"
  ]
}
```

### GitHub Actions Workflow

**.github/workflows/release.yml:**
```yaml
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
          persist-credentials: false

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
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release
```

### Automated Changelog

Semantic Release generates CHANGELOG.md automatically:

```markdown
# Changelog

## [2.0.0](https://github.com/org/repo/compare/v1.2.3...v2.0.0) (2025-12-04)

### ⚠ BREAKING CHANGES

* **api**: Auth endpoints now require API version header

### Features

* **auth**: add JWT token validation ([a1b2c3d](link))
* **api**: add user profile endpoints ([e4f5g6h](link))

### Bug Fixes

* **ui**: resolve button alignment issue ([i7j8k9l](link))
* resolve race condition in login ([m0n1o2p](link))
```

---

## Examples

### Simple Feature

```bash
git commit -m "feat: add dark mode toggle"
```

### Feature with Scope

```bash
git commit -m "feat(ui): add dark mode toggle to settings"
```

### Bug Fix

```bash
git commit -m "fix: resolve memory leak in event listeners"
```

### Bug Fix with Scope and Body

```bash
git commit -m "fix(auth): resolve token expiration issue

Token expiration was not being checked correctly, causing users
to remain logged in after token expired. Added proper validation
and automatic logout when token expires.

Fixes #123"
```

### Breaking Change (Short Form)

```bash
git commit -m "feat(api)!: change user endpoint response format"
```

### Breaking Change (Full Form)

```bash
git commit -m "feat(api): redesign authentication endpoints

Redesigned authentication endpoints for better security and
performance. New endpoints use JWT tokens instead of sessions.

BREAKING CHANGE: Auth endpoints now require API version header.

Migration guide:
1. Add 'X-API-Version: 2' header to all API requests
2. Update client libraries to latest version
3. Clear browser cookies

Closes #456"
```

### Multiple Types in One Commit

If commit contains multiple changes, use the primary type:
```bash
# Fix is primary, docs are secondary
git commit -m "fix(api): resolve timeout issue

Also updated API documentation to reflect new timeout values.

Fixes #789"
```

Or split into multiple commits (preferred):
```bash
git commit -m "fix(api): resolve timeout issue"
git commit -m "docs(api): update timeout documentation"
```

### Revert Commit

```bash
git commit -m "revert: feat(auth): add social login

This reverts commit a1b2c3d4e5f6.

Social login feature caused authentication issues in production.
Reverting to investigate and fix before re-deploying."
```

### Monorepo Scopes

```bash
git commit -m "feat(web): add user dashboard"
git commit -m "fix(mobile): resolve crash on startup"
git commit -m "refactor(shared): extract common utilities"
git commit -m "test(api): add integration tests"
```

## Best Practices

### Commit Frequency

**Good:** Small, focused commits
```bash
git commit -m "feat(auth): add login form"
git commit -m "feat(auth): add password validation"
git commit -m "test(auth): add login form tests"
```

**Avoid:** Large, unfocused commits
```bash
git commit -m "feat: add authentication and user profile and settings"
```

### Description Quality

**Good:** Clear, specific descriptions
```bash
git commit -m "fix(api): resolve race condition in user creation"
git commit -m "perf(database): add index to user_id column"
git commit -m "feat(notifications): add email notification support"
```

**Avoid:** Vague descriptions
```bash
git commit -m "fix: fix bug"
git commit -m "feat: add stuff"
git commit -m "refactor: update code"
```

### Body Usage

Use body for complex changes:
```bash
git commit -m "refactor(database): migrate from MySQL to PostgreSQL

- Migrate all table schemas to PostgreSQL syntax
- Update ORM configuration
- Add migration scripts for existing data
- Update backup procedures

This migration improves performance and adds support for
advanced query features needed for analytics.

Refs: #123, #456"
```

### Footer Usage

**Issue References:**
```bash
Fixes #123
Closes #456
Refs #789
```

**Breaking Changes:**
```bash
BREAKING CHANGE: Configuration file format changed from JSON to YAML
```

**Co-authors:**
```bash
Co-authored-by: John Doe <john@example.com>
Co-authored-by: Jane Smith <jane@example.com>
```
