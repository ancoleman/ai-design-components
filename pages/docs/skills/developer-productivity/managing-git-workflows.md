---
sidebar_position: 6
title: Managing Git Workflows
description: Effective Git branching strategies, collaboration patterns, and version control best practices
tags: [developer-productivity, git, git-flow, github-flow, branching, collaboration]
---

# Managing Git Workflows

Effective Git branching strategies, collaboration patterns, and version control best practices for team environments. Covers popular workflows (Git Flow, GitHub Flow, trunk-based), commit conventions, code review processes, and strategies for managing releases.

## When to Use

Use when:
- Establishing branching strategies for development teams
- Implementing commit message conventions
- Setting up code review workflows
- Managing release processes and versioning
- Automating Git operations with hooks
- Resolving merge conflicts systematically
- Choosing between Git Flow, GitHub Flow, or trunk-based development

## Key Features

### Branching Strategies
- **Git Flow**: feature, develop, release, hotfix branches
- **GitHub Flow**: main branch + feature branches (simple, continuous deployment)
- **Trunk-Based Development**: Short-lived feature branches, frequent integration
- Branch naming conventions
- Release branching patterns

### Commit Best Practices
- Atomic commits and logical grouping
- Conventional Commits specification
- Commit message templates
- Co-authored commits
- Commit signing and verification

### Collaboration Patterns
- Pull request/merge request workflows
- Code review best practices
- Conflict resolution strategies
- Pair programming with Git
- Distributed team workflows

### Advanced Git Techniques
- Interactive rebase and history rewriting
- Cherry-picking and backporting
- Git bisect for bug hunting
- Submodules and subtrees
- Worktrees for parallel work

## Quick Start

### GitHub Flow (Recommended for Most Teams)

```bash
# 1. Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/add-user-authentication

# 2. Make changes and commit
git add src/auth.js
git commit -m "feat: add JWT authentication middleware"

# 3. Push and create pull request
git push -u origin feature/add-user-authentication

# 4. After PR approval, merge to main
# (Done via GitHub UI with squash merge)

# 5. Delete feature branch
git branch -d feature/add-user-authentication
git push origin --delete feature/add-user-authentication
```

### Conventional Commits

```bash
# Format: <type>(<scope>): <description>

# Types:
feat: add new user authentication system
fix: resolve login token expiration bug
docs: update API documentation for auth endpoints
style: format code with prettier
refactor: extract authentication logic to service
test: add unit tests for auth service
chore: update dependencies

# With scope
feat(auth): add OAuth2 integration
fix(api): handle rate limit errors gracefully

# Breaking changes
feat!: redesign authentication API

BREAKING CHANGE: Authentication now requires API key in header
```

### Git Hooks with Husky

```bash
# Install Husky
npm install --save-dev husky
npx husky install

# Add pre-commit hook
npx husky add .husky/pre-commit "npm run lint && npm test"

# Add commit-msg hook for conventional commits
npm install --save-dev @commitlint/cli @commitlint/config-conventional
npx husky add .husky/commit-msg "npx commitlint --edit $1"
```

## Branching Strategy Decision Framework

### Choose GitHub Flow When:
- Deploying continuously to production
- Small to medium team (2-20 developers)
- Simple release process (main = production)
- Cloud-native, microservices architecture

### Choose Git Flow When:
- Scheduled releases (monthly, quarterly)
- Supporting multiple versions simultaneously
- Enterprise environment with formal release cycles
- Need hotfix process separate from features

### Choose Trunk-Based When:
- Very frequent deployments (multiple per day)
- Strong CI/CD and feature flags
- Experienced team with good practices
- Monorepo or single product focus

## Common Workflows

### Creating a Feature

```bash
# 1. Update main branch
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/user-profile

# 3. Work and commit
git add .
git commit -m "feat: add user profile page"

# 4. Keep branch updated (rebase)
git fetch origin
git rebase origin/main

# 5. Push for review
git push -u origin feature/user-profile
```

### Code Review Process

```bash
# Reviewer: Check out PR branch
git fetch origin pull/123/head:pr-123
git checkout pr-123

# Test changes locally
npm install
npm test

# Request changes or approve via GitHub UI

# Author: Address feedback
git add src/profile.js
git commit -m "fix: address code review feedback"
git push origin feature/user-profile
```

### Resolving Merge Conflicts

```bash
# Update your branch with latest main
git fetch origin
git rebase origin/main

# Conflict occurs - resolve in editor
# Look for conflict markers:
# <<<<<<< HEAD
# Your changes
# =======
# Their changes
# >>>>>>> origin/main

# After resolving
git add resolved-file.js
git rebase --continue

# Force push (safe for feature branches)
git push --force-with-lease origin feature/user-profile
```

### Using Git Bisect for Bug Hunting

```bash
# Start bisect session
git bisect start
git bisect bad                    # Current commit is bad
git bisect good v1.0.0            # Last known good commit

# Git checks out a commit in between
# Test it
npm test

# Mark result
git bisect good   # or 'git bisect bad'

# Git continues binary search
# Repeat until bug is found

# Reset when done
git bisect reset
```

## Release Management

### Semantic Versioning

- **MAJOR** (v2.0.0): Breaking changes, incompatible API changes
- **MINOR** (v1.1.0): New features, backward compatible
- **PATCH** (v1.0.1): Bug fixes, backward compatible

### Creating a Release

```bash
# 1. Update version in package.json
npm version minor  # or major/patch

# 2. Push tag
git push origin main --tags

# 3. Create GitHub release
gh release create v1.1.0 --generate-notes

# 4. Publish package
npm publish
```

### Automated Changelog

```bash
# Install conventional-changelog
npm install --save-dev conventional-changelog-cli

# Generate changelog
npx conventional-changelog -p angular -i CHANGELOG.md -s

# Or use semantic-release for full automation
npm install --save-dev semantic-release
```

## Git Hooks Examples

### Pre-commit: Lint and Format

```bash
#!/bin/sh
# .husky/pre-commit

# Run linter
npm run lint || {
  echo "Linting failed. Please fix errors before committing."
  exit 1
}

# Run formatter
npm run format

# Add formatted files
git add -u
```

### Commit-msg: Validate Format

```bash
#!/bin/sh
# .husky/commit-msg

# Validate conventional commit format
npx commitlint --edit $1
```

### Pre-push: Run Tests

```bash
#!/bin/sh
# .husky/pre-push

# Run test suite
npm test || {
  echo "Tests failed. Please fix before pushing."
  exit 1
}
```

## Best Practices

### Commit Messages
- Use imperative mood ("add feature" not "added feature")
- First line under 50 characters
- Detailed description after blank line if needed
- Reference issue numbers (#123)

### Branch Naming
```
feature/user-authentication
bugfix/login-error
hotfix/security-patch
release/v1.2.0
```

### Pull Request Guidelines
- Small, focused changes (under 400 lines)
- Self-review before submitting
- Provide context in description
- Link related issues
- Request specific reviewers

### Code Review Checklist
- [ ] Code follows project conventions
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No console.log or debug code
- [ ] Security considerations reviewed
- [ ] Performance implications considered

## Related Skills

- [Building CLIs](./building-clis) - Git automation tools
- [Generating Documentation](./generating-documentation) - Changelog generation from commits
- [Writing GitHub Actions](./writing-github-actions) - Automated workflows and releases
- [Debugging Techniques](./debugging-techniques) - Git bisect for debugging

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/git-workflows)
- [Master Plan](../../master-plans/developer-productivity/managing-git-workflows)
