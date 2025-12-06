# Git Branching Strategies

Detailed patterns for trunk-based development, GitHub Flow, and GitFlow with complete workflow examples.

## Table of Contents

1. [Trunk-Based Development](#trunk-based-development)
2. [GitHub Flow](#github-flow)
3. [GitFlow](#gitflow)
4. [Feature Branching](#feature-branching)
5. [Comparison Matrix](#comparison-matrix)

## Trunk-Based Development

### Overview

High-velocity workflow where developers commit to main (trunk) frequently, using short-lived branches that merge within 1 day.

### When to Use

- ✅ Strong CI/CD automation in place
- ✅ Comprehensive automated test coverage (80%+)
- ✅ Team practices continuous integration
- ✅ Feature flags hide incomplete features
- ✅ Deployments are frequent (daily or more)
- ✅ Team is experienced with Git and testing

### Branch Structure

```
main (trunk) - Always deployable
  ├── feature/short-lived-1 (0-1 days)
  ├── feature/short-lived-2 (0-1 days)
  └── feature/short-lived-3 (0-1 days)
```

### Complete Workflow

```bash
# 1. Create short-lived feature branch from main
git checkout -b feature/add-login main

# 2. Make small, incremental changes
git add src/components/LoginForm.tsx
git commit -m "feat: add login form component"

# 3. Update with latest main frequently (multiple times per day)
git fetch origin
git rebase origin/main

# 4. Push and create pull request
git push origin feature/add-login

# 5. After review, merge immediately
# (via GitHub UI or CLI)
git checkout main
git merge feature/add-login

# 6. Delete branch immediately after merge
git branch -d feature/add-login
git push origin --delete feature/add-login
```

### Key Principles

**Branch Lifetime:**
- Branches live <24 hours (ideally <4 hours)
- Commit to main multiple times per day
- No long-lived feature branches

**Feature Flags:**
Hide incomplete features from users while integrating code:
```javascript
// Example: React component with feature flag
if (featureFlags.newLogin && user.isBetaTester) {
  return <NewLoginForm />;
}
return <OldLoginForm />;
```

**Continuous Integration:**
- CI/CD runs on every commit to main
- Broken builds are top priority to fix
- Automated deployment to production

**Team Practices:**
- Pair programming or immediate code review
- Small pull requests (100-300 lines)
- Tests written alongside code

### Example: Adding a New Feature

```bash
# Day 1, Morning (9 AM)
git checkout -b feature/user-notifications main

# Add notification model (30 min)
git add src/models/Notification.ts
git commit -m "feat(notifications): add notification model"

# Add API endpoints (1 hour)
git add src/api/notifications.ts
git commit -m "feat(notifications): add API endpoints"

# Update with latest main
git fetch origin
git rebase origin/main

# Push and create PR
git push origin feature/user-notifications
gh pr create --title "Add user notifications (behind feature flag)"

# Day 1, Afternoon (2 PM)
# After review and CI passes
git checkout main
git pull origin main
git merge feature/user-notifications
git push origin main

# Feature deployed but hidden behind flag
# Enable for beta testers only

# Day 2-3: Iterate on feature
# Day 4: Enable for all users
# featureFlags.userNotifications = true
```

---

## GitHub Flow

### Overview

Simple branch-based workflow where main is always deployable. Feature branches are merged via pull requests after code review.

### When to Use

- ✅ Building web applications
- ✅ Main branch always represents production
- ✅ Continuous deployment is the goal
- ✅ Simple, understandable workflow needed
- ✅ Small to medium team size (2-20 developers)
- ✅ Single production environment

### Branch Structure

```
main (always deployable) - Production
  ├── feature/user-auth
  ├── feature/payment-integration
  ├── bugfix/login-error
  └── docs/api-documentation
```

### Complete Workflow

```bash
# 1. Create feature branch from main
git checkout -b feature/user-auth main

# 2. Make commits with descriptive messages
git add src/auth/jwt.ts
git commit -m "feat: add JWT authentication middleware"

git add src/auth/login.ts
git commit -m "feat: add login endpoint"

git add tests/auth.test.ts
git commit -m "test: add authentication tests"

git add docs/api/auth.md
git commit -m "docs: document authentication API"

# 3. Push and open pull request
git push origin feature/user-auth

# Open PR via GitHub CLI or web UI
gh pr create \
  --title "Add JWT authentication" \
  --body "Implements user authentication with JWT tokens. Closes #123"

# 4. Code review and discussion
# Address feedback by pushing more commits
git add src/auth/jwt.ts
git commit -m "fix: handle expired tokens properly"
git push origin feature/user-auth

# 5. Merge to main after approval
# (via GitHub UI - squash and merge recommended)

# 6. Automated deployment triggers
# CI/CD deploys to production automatically

# 7. Delete branch after merge
git branch -d feature/user-auth
git push origin --delete feature/user-auth
```

### Key Principles

**Main Branch:**
- Always deployable to production
- Protected by branch rules (no direct commits)
- Every merge triggers deployment

**Pull Requests:**
- Code review required before merge
- Status checks must pass (CI, tests, linting)
- Descriptive PR descriptions with context

**Branch Naming:**
Use type prefixes for clarity:
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Code refactoring

**Merge Strategy:**
Squash and merge recommended for clean history:
- Combines all feature commits into one
- Main branch has linear, readable history
- Each commit on main represents complete feature

### Example: Bug Fix Workflow

```bash
# User reports login error (Issue #456)

# 1. Create bugfix branch
git checkout -b bugfix/login-timeout main

# 2. Reproduce and fix issue
git add src/auth/login.ts
git commit -m "fix: increase login timeout to 10 seconds"

# 3. Add regression test
git add tests/auth.test.ts
git commit -m "test: add test for login timeout"

# 4. Push and create PR
git push origin bugfix/login-timeout
gh pr create \
  --title "Fix login timeout issue" \
  --body "Fixes #456. Increased timeout and added regression test."

# 5. After review and CI passes, merge via GitHub UI

# 6. Verify deployment in production
# Monitor error logs for the issue

# 7. Clean up local branch
git checkout main
git pull origin main
git branch -d bugfix/login-timeout
```

---

## GitFlow

### Overview

Structured workflow with multiple long-lived branches. Separates development, release preparation, and production code.

### When to Use

- ✅ Multiple production versions supported simultaneously
- ✅ Scheduled releases (monthly, quarterly)
- ✅ Formal QA cycle required before release
- ✅ Hotfixes need to bypass normal release cycle
- ✅ Enterprise environment with change management
- ✅ Mobile apps with App Store release cycles

### Branch Structure

```
main (production) - Tagged releases only
  └── tags: v1.0.0, v1.1.0, v2.0.0

develop (integration) - Next release
  ├── feature/user-profile
  ├── feature/notifications
  └── feature/settings

release/1.1.0 - Release preparation
  └── Bug fixes and version bumps only

hotfix/critical-bug - Urgent production fixes
```

### Branch Types

**Long-Lived Branches:**
- `main` - Production code, tagged releases only
- `develop` - Integration branch for next release

**Short-Lived Branches:**
- `feature/*` - New features (branch from develop)
- `release/*` - Release preparation (branch from develop)
- `hotfix/*` - Urgent fixes (branch from main)

### Complete Workflow

#### Feature Development

```bash
# 1. Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/user-profile develop

# 2. Develop feature
git add src/components/UserProfile.tsx
git commit -m "feat: add user profile page"

git add src/api/user.ts
git commit -m "feat: add user profile API"

git add tests/user-profile.test.tsx
git commit -m "test: add user profile tests"

# 3. Merge feature to develop (no fast-forward)
git checkout develop
git merge --no-ff feature/user-profile -m "Merge feature: user profile"

# 4. Delete feature branch
git branch -d feature/user-profile

# 5. Push develop
git push origin develop
```

#### Release Workflow

```bash
# 1. Create release branch from develop
git checkout -b release/1.1.0 develop

# 2. Prepare release
# - Bump version numbers
# - Update changelog
# - Final bug fixes only (no new features)

git add package.json CHANGELOG.md
git commit -m "chore: bump version to 1.1.0"

git add src/bugfix.ts
git commit -m "fix: resolve minor UI issue"

# 3. Merge release to main
git checkout main
git merge --no-ff release/1.1.0 -m "Release version 1.1.0"

# 4. Tag the release
git tag -a v1.1.0 -m "Release version 1.1.0"

# 5. Merge release back to develop
git checkout develop
git merge --no-ff release/1.1.0 -m "Merge release 1.1.0 back to develop"

# 6. Delete release branch
git branch -d release/1.1.0

# 7. Push everything
git push origin main develop --tags
```

#### Hotfix Workflow

```bash
# 1. Create hotfix branch from main
git checkout -b hotfix/critical-security-issue main

# 2. Fix the issue
git add src/auth/security.ts
git commit -m "fix: resolve critical security vulnerability"

# 3. Merge hotfix to main
git checkout main
git merge --no-ff hotfix/critical-security-issue -m "Hotfix: security issue"

# 4. Tag the hotfix
git tag -a v1.1.1 -m "Hotfix version 1.1.1"

# 5. Merge hotfix back to develop
git checkout develop
git merge --no-ff hotfix/critical-security-issue -m "Merge hotfix 1.1.1 to develop"

# 6. If release branch exists, merge there too
git checkout release/1.2.0
git merge --no-ff hotfix/critical-security-issue

# 7. Delete hotfix branch
git branch -d hotfix/critical-security-issue

# 8. Push everything
git push origin main develop --tags
```

### Key Principles

**Branch Discipline:**
- Never commit directly to main or develop
- Always use --no-ff (no fast-forward) for merges
- Preserve branch history for audit trails

**Release Process:**
- Feature freeze when release branch created
- Only bug fixes on release branch
- QA tests release branch thoroughly
- Merge to main only when ready to deploy

**Version Tagging:**
- Tag all releases on main branch
- Use semantic versioning (v1.2.3)
- Annotated tags with release notes

---

## Feature Branching

### Overview

Simple workflow for small teams. Feature branches merge to main when complete.

### When to Use

- ✅ Team is small (1-5 developers)
- ✅ Simple workflow sufficient
- ✅ No need for complex release management
- ✅ Infrequent deployments acceptable

### Workflow

```bash
# Create feature branch
git checkout -b feature/new-component main

# Develop and commit
git commit -m "feat: add new component"

# Merge to main
git checkout main
git merge feature/new-component

# Deploy manually
./deploy.sh
```

---

## Comparison Matrix

| Aspect | Trunk-Based | GitHub Flow | GitFlow | Feature Branching |
|--------|-------------|-------------|---------|-------------------|
| **Complexity** | Medium | Low | High | Very Low |
| **Branch Lifetime** | <1 day | 1-7 days | Varies | 1-14 days |
| **Release Frequency** | Continuous | Continuous | Scheduled | Manual |
| **CI/CD Requirements** | High | Medium | Low | Low |
| **Team Size** | Any | 2-20 | 5-50+ | 1-5 |
| **Learning Curve** | Medium | Low | High | Low |
| **QA Integration** | Automated | Automated | Manual cycle | Manual |
| **Hotfix Process** | Immediate | Fast | Structured | Ad-hoc |
| **Best For** | High-velocity teams | Web apps | Enterprise | Small projects |

## Choosing the Right Strategy

### Start Here: GitHub Flow

For most teams, GitHub Flow is the recommended starting point:
- Simple to understand and adopt
- Works well for modern web applications
- Easy to transition to trunk-based later
- Supports continuous deployment

### Migrate to Trunk-Based When:
- Team has mature CI/CD practices
- Test coverage is comprehensive
- Feature flags are implemented
- Team is comfortable with Git

### Use GitFlow Only If:
- Multiple production versions required
- Formal release schedule needed
- App Store release process (mobile)
- Enterprise change management required

### Avoid Feature Branching Unless:
- Team is very small (1-2 developers)
- Project is simple and short-term
- Deployment frequency is low

## Migration Strategies

### From Feature Branching to GitHub Flow

1. Set up branch protection on main
2. Require pull requests for all changes
3. Add CI/CD checks (tests, linting)
4. Train team on PR process
5. Implement automated deployments

### From GitHub Flow to Trunk-Based

1. Reduce branch lifetime (aim for <1 day)
2. Implement feature flags
3. Increase test coverage to 80%+
4. Set up comprehensive CI/CD
5. Commit directly to main (with short-lived branches)

### From GitFlow to GitHub Flow

1. Merge develop into main
2. Delete develop branch
3. Switch to feature branches from main
4. Remove release branch process
5. Implement continuous deployment

## Troubleshooting Common Issues

### Long-Lived Branches

**Problem:** Feature branches last weeks or months

**Solutions:**
- Break features into smaller increments
- Use feature flags to merge incomplete work
- Implement daily rebasing with main
- Set branch lifetime limits (auto-close PRs after 7 days)

### Merge Conflicts

**Problem:** Frequent conflicts when merging

**Solutions:**
- Reduce branch lifetime
- Rebase frequently with main
- Communicate about overlapping work
- Use CODEOWNERS to prevent overlap

### Broken Main Branch

**Problem:** Main branch fails CI/CD

**Solutions:**
- Require status checks before merge
- Add pre-push hooks to run tests
- Implement revert-first policy (revert, fix, re-merge)
- Block direct commits to main

### Unclear Release State

**Problem:** Don't know what's in production

**Solutions:**
- Tag all production releases
- Use semantic versioning
- Maintain CHANGELOG.md
- Track deployments in monitoring tools
