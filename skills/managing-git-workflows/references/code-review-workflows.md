# Code Review Workflows

Complete guide to pull request templates, branch protection, and code review best practices.

## Table of Contents

1. [Pull Request Templates](#pull-request-templates)
2. [Branch Protection Rules](#branch-protection-rules)
3. [Review Best Practices](#review-best-practices)
4. [CODEOWNERS Integration](#codeowners-integration)
5. [Automated Checks](#automated-checks)

## Pull Request Templates

### Basic Template

**File:** `.github/PULL_REQUEST_TEMPLATE.md`

```markdown
## Description
<!-- Brief description of changes -->

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test updates

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
<!-- Link to related issues: Closes #123, Fixes #456 -->
```

### Feature Template

**File:** `.github/PULL_REQUEST_TEMPLATE/feature.md`

```markdown
## Feature Description
<!-- What feature does this PR add? -->

## Motivation
<!-- Why is this feature needed? -->

## Implementation Details
<!-- How was this implemented? -->

### Architecture Changes
<!-- Any architectural changes? -->

### API Changes
<!-- New endpoints, changed responses, etc. -->

### Database Changes
<!-- Migrations, schema changes, etc. -->

## Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] E2E tests added (if applicable)
- [ ] Manual testing completed

### Test Coverage
- Before: X%
- After: Y%

## Documentation
- [ ] API documentation updated
- [ ] README updated
- [ ] Migration guide created (if breaking change)

## Performance Impact
<!-- Any performance considerations? -->

## Security Considerations
<!-- Any security implications? -->

## Screenshots/Videos
<!-- Visual demonstration of feature -->

## Rollout Plan
<!-- How will this be rolled out? -->

## Related Issues
Closes #

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added
- [ ] All tests pass locally
```

### Bug Fix Template

**File:** `.github/PULL_REQUEST_TEMPLATE/bugfix.md`

```markdown
## Bug Description
<!-- What bug does this fix? -->

## Root Cause
<!-- What caused the bug? -->

## Solution
<!-- How does this fix the bug? -->

## Reproduction Steps (Before Fix)
1.
2.
3.

## Expected Behavior
<!-- What should happen? -->

## Actual Behavior (Before Fix)
<!-- What was happening? -->

## Testing
- [ ] Bug reproduction verified
- [ ] Fix verified
- [ ] Regression test added
- [ ] Related functionality tested

## Impact
<!-- Who is affected by this bug? -->

## Related Issues
Fixes #

## Checklist
- [ ] Root cause identified and documented
- [ ] Fix verified
- [ ] Regression test added
- [ ] No new warnings introduced
```

### Using Multiple Templates

**.github/PULL_REQUEST_TEMPLATE.md** (default)
**.github/PULL_REQUEST_TEMPLATE/feature.md**
**.github/PULL_REQUEST_TEMPLATE/bugfix.md**

Select template when creating PR:
```
https://github.com/org/repo/compare/main...branch?template=feature.md
```

---

## Branch Protection Rules

### GitHub Settings

Navigate to: `Settings → Branches → Branch protection rules → Add rule`

### Essential Rules for Main Branch

**Branch name pattern:** `main`

**Require pull request before merging:**
- ☑ Require a pull request before merging
- Required number of approvals: 2
- ☑ Dismiss stale pull request approvals when new commits are pushed
- ☑ Require review from Code Owners
- ☑ Restrict who can dismiss pull request reviews
  - Select: @org/principal-engineers

**Require status checks to pass before merging:**
- ☑ Require status checks to pass before merging
- ☑ Require branches to be up to date before merging
- Required status checks:
  - Build
  - Tests
  - Lint
  - Security Scan
  - TypeScript Check

**Require conversation resolution before merging:**
- ☑ Require conversation resolution before merging

**Require signed commits:**
- ☑ Require signed commits

**Require linear history:**
- ☑ Require linear history (prevents merge commits)

**Additional settings:**
- ☑ Include administrators (apply rules to admins too)
- ☑ Restrict who can push to matching branches
  - Select: (empty - no one can push directly)
- ☑ Allow force pushes: NO
- ☑ Allow deletions: NO

### Protection Rules for Develop Branch

**Branch name pattern:** `develop`

**Settings:**
- Required approvals: 1
- Require status checks
- Allow administrators to bypass (for urgent fixes)

### Protection Rules for Release Branches

**Branch name pattern:** `release/*`

**Settings:**
- Required approvals: 2
- Require Code Owner review
- Require status checks
- Restrict who can push: @org/release-managers

### Status Check Configuration

**Required checks:**
```yaml
# .github/workflows/pr-checks.yml
name: PR Checks

on:
  pull_request:
    branches: [main, develop]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node
        uses: actions/setup-node@v3
      - name: Install dependencies
        run: npm ci
      - name: Build
        run: npm run build

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node
        uses: actions/setup-node@v3
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm test -- --coverage

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node
        uses: actions/setup-node@v3
      - name: Install dependencies
        run: npm ci
      - name: Lint
        run: npm run lint

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run security audit
        run: npm audit --audit-level=moderate
```

---

## Review Best Practices

### For PR Authors

**Before Creating PR:**
1. Self-review all changes
2. Run tests locally
3. Update documentation
4. Add descriptive PR title and description
5. Link related issues

**PR Size:**
- Keep PRs small (< 400 lines changed)
- Split large changes into multiple PRs
- Each PR should represent one logical change

**PR Description:**
- Explain WHY, not just WHAT
- Include screenshots for UI changes
- List breaking changes clearly
- Provide testing instructions

**Responding to Feedback:**
- Respond to all comments
- Mark conversations as resolved after addressing
- Push fixup commits, squash before merge
- Request re-review after significant changes

### For Reviewers

**Review Checklist:**
- [ ] Code quality and readability
- [ ] Tests cover new functionality
- [ ] Documentation updated
- [ ] No obvious bugs or logic errors
- [ ] Performance considerations addressed
- [ ] Security implications considered
- [ ] Follows project conventions

**Providing Feedback:**
- Be specific and constructive
- Provide code examples when suggesting changes
- Distinguish between required changes and suggestions
- Acknowledge good code and smart solutions

**Comment Tags:**
```
[REQUIRED] - Must be addressed before approval
[SUGGESTION] - Nice to have, not blocking
[QUESTION] - Seeking clarification
[NITPICK] - Minor style issue
[PRAISE] - Acknowledging good work
```

**Example Comments:**
```
[REQUIRED] This function could cause a memory leak.
Please add cleanup logic in the useEffect return.

[SUGGESTION] Consider extracting this logic into a
separate hook for reusability.

[QUESTION] Why did we choose this approach over using
the existing utility function?

[PRAISE] Great solution! This is much cleaner than
the previous implementation.
```

---

## CODEOWNERS Integration

### File Structure

**.github/CODEOWNERS:**
```
# Default owners
* @org/engineering

# Frontend
/apps/web/ @org/frontend-team
/libs/ui-components/ @org/design-system-team

# Backend
/apps/api/ @org/backend-team
/libs/database/ @org/backend-team

# Infrastructure
/.github/ @org/devops-team
/infrastructure/ @org/devops-team
/docker/ @org/devops-team

# Security-critical (require multiple approvals)
/libs/auth/ @org/security-team @org/principal-engineers
/apps/*/src/config/secrets* @org/security-team @org/devops-team

# Documentation
/docs/ @org/tech-writers
*.md @org/tech-writers

# Configuration
package.json @org/principal-engineers
tsconfig*.json @org/principal-engineers
```

### Auto-Assignment

When PR is created, GitHub automatically:
1. Requests review from code owners
2. Marks code owner review as required (if branch protection enabled)
3. Prevents merge until code owner approves

### Multiple Owners

```
# Require approval from ALL listed teams
/libs/payments/ @org/payments-team @org/security-team

# First matching pattern wins
/libs/shared/           @org/engineering
/libs/shared/security/  @org/security-team
```

---

## Automated Checks

### GitHub Actions for PR Validation

**.github/workflows/pr-validation.yml:**
```yaml
name: PR Validation

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  validate-pr-title:
    runs-on: ubuntu-latest
    steps:
      - uses: amannn/action-semantic-pull-request@v5
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          types: |
            feat
            fix
            docs
            style
            refactor
            perf
            test
            build
            ci
            chore
            revert
          requireScope: false

  check-pr-size:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check PR size
        run: |
          FILES_CHANGED=$(git diff --name-only origin/${{ github.base_ref }}...HEAD | wc -l)
          LINES_CHANGED=$(git diff --stat origin/${{ github.base_ref }}...HEAD | tail -1 | awk '{print $4+$6}')

          if [ $LINES_CHANGED -gt 500 ]; then
            echo "::warning::PR is large ($LINES_CHANGED lines). Consider splitting."
          fi

  label-pr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v4
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          configuration-path: .github/labeler.yml

  check-todos:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check for TODO comments
        run: |
          if git diff origin/${{ github.base_ref }}...HEAD | grep -i "TODO"; then
            echo "::warning::PR contains TODO comments"
          fi

  require-changelog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check CHANGELOG updated
        run: |
          if git diff --name-only origin/${{ github.base_ref }}...HEAD | grep -q "CHANGELOG.md"; then
            echo "✅ CHANGELOG updated"
          else
            echo "::warning::Consider updating CHANGELOG.md"
          fi
```

### Auto-Labeling

**.github/labeler.yml:**
```yaml
'frontend':
  - apps/web/**/*
  - libs/ui-components/**/*

'backend':
  - apps/api/**/*
  - libs/database/**/*

'infrastructure':
  - .github/**/*
  - infrastructure/**/*
  - docker/**/*

'documentation':
  - docs/**/*
  - '**/*.md'

'tests':
  - '**/*.test.ts'
  - '**/*.test.tsx'
  - '**/*.spec.ts'

'dependencies':
  - package.json
  - package-lock.json
  - yarn.lock
```

### PR Size Labels

**.github/workflows/pr-size.yml:**
```yaml
name: PR Size Labeler

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  size-label:
    runs-on: ubuntu-latest
    steps:
      - uses: codelytv/pr-size-labeler@v1
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          xs_label: 'size/xs'
          xs_max_size: 10
          s_label: 'size/s'
          s_max_size: 100
          m_label: 'size/m'
          m_max_size: 500
          l_label: 'size/l'
          l_max_size: 1000
          xl_label: 'size/xl'
          fail_if_xl: 'false'
```

### Require Issue Link

**.github/workflows/require-issue.yml:**
```yaml
name: Require Issue Link

on:
  pull_request:
    types: [opened, edited]

jobs:
  check-issue-link:
    runs-on: ubuntu-latest
    steps:
      - name: Check for issue reference
        run: |
          if echo "${{ github.event.pull_request.body }}" | grep -qE "(Closes|Fixes|Refs) #[0-9]+"; then
            echo "✅ Issue reference found"
          else
            echo "::error::PR must reference an issue (Closes #123, Fixes #456, Refs #789)"
            exit 1
          fi
```

---

## Best Practices Summary

### PR Creation

**Do:**
- ✅ Keep PRs small and focused
- ✅ Write descriptive titles (conventional format)
- ✅ Include detailed description
- ✅ Link related issues
- ✅ Add screenshots for UI changes
- ✅ Self-review before requesting review

**Don't:**
- ❌ Mix unrelated changes
- ❌ Submit large PRs (>500 lines)
- ❌ Leave TODO comments
- ❌ Skip tests
- ❌ Forget documentation

### Code Review

**Do:**
- ✅ Review within 24 hours
- ✅ Provide constructive feedback
- ✅ Test locally for complex changes
- ✅ Approve when ready (don't block unnecessarily)
- ✅ Use comment tags ([REQUIRED], [SUGGESTION])

**Don't:**
- ❌ Nitpick style issues (use automated tools)
- ❌ Block on personal preferences
- ❌ Leave comments without explanation
- ❌ Approve without reviewing

### Branch Protection

**Required:**
- ✅ Require PR reviews (2+ approvals)
- ✅ Require status checks
- ✅ Require code owner approval
- ✅ Prevent force pushes
- ✅ Require linear history

**Optional:**
- ⚠️ Require signed commits (if security critical)
- ⚠️ Restrict merge methods (squash only)
- ⚠️ Auto-delete branches after merge
