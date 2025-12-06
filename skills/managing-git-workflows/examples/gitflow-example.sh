#!/bin/bash

# GitFlow Complete Workflow Example
# This script demonstrates a complete GitFlow workflow including features, releases, and hotfixes

set -e  # Exit on error

echo "🚀 GitFlow Workflow Example"
echo "==========================="
echo ""

# Initialize GitFlow
echo "📝 Step 1: Initialize GitFlow"
echo "
GitFlow uses two main branches:
- main: Production-ready code
- develop: Integration branch for next release
"

git checkout -b develop main
echo "✅ Created develop branch from main"
echo ""

# Feature Development
echo "📝 Step 2: Feature Development"
echo ""

# Feature 1: User Profile
echo "Creating feature/user-profile..."
git checkout -b feature/user-profile develop

echo "// User profile component" > src/components/UserProfile.tsx
git add src/components/UserProfile.tsx
git commit -m "feat(profile): add user profile component"

echo "// User profile API" > src/api/profile.ts
git add src/api/profile.ts
git commit -m "feat(api): add user profile endpoints"

echo "// Profile tests" > tests/profile.test.ts
git add tests/profile.test.ts
git commit -m "test(profile): add user profile tests"

# Merge feature to develop
git checkout develop
git merge --no-ff feature/user-profile -m "Merge feature: user profile

Added user profile functionality with full test coverage."
git branch -d feature/user-profile

echo "✅ Feature user-profile merged to develop"
echo ""

# Feature 2: Notifications
echo "Creating feature/notifications..."
git checkout -b feature/notifications develop

echo "// Notification service" > src/services/notifications.ts
git add src/services/notifications.ts
git commit -m "feat(notifications): add notification service"

echo "// Email notifications" > src/services/email.ts
git add src/services/email.ts
git commit -m "feat(notifications): add email notification support"

# Merge feature to develop
git checkout develop
git merge --no-ff feature/notifications -m "Merge feature: notifications

Added notification system with email support."
git branch -d feature/notifications

echo "✅ Feature notifications merged to develop"
echo ""

# Release Process
echo "📝 Step 3: Release Process"
echo ""

# Create release branch
echo "Creating release/1.1.0..."
git checkout -b release/1.1.0 develop

# Prepare release (version bumps, changelog)
echo '{
  "version": "1.1.0"
}' > package.json
git add package.json
git commit -m "chore(release): bump version to 1.1.0"

echo "# Changelog

## [1.1.0] - 2025-12-04

### Features
- User profile functionality
- Notification system with email support

### Bug Fixes
- Minor UI improvements
" > CHANGELOG.md
git add CHANGELOG.md
git commit -m "docs(changelog): update changelog for 1.1.0"

# Bug fixes on release branch (last-minute fixes only)
echo "// Fix minor UI issue" > src/bugfix.ts
git add src/bugfix.ts
git commit -m "fix(ui): resolve alignment issue in profile page"

echo "✅ Release 1.1.0 prepared"
echo ""

# Merge release to main
echo "Merging release to main..."
git checkout main
git merge --no-ff release/1.1.0 -m "Release version 1.1.0

Features:
- User profile functionality
- Notification system

Bug fixes:
- UI alignment issues
"

# Tag the release
git tag -a v1.1.0 -m "Release version 1.1.0"

echo "✅ Release 1.1.0 merged to main and tagged"
echo ""

# Merge release back to develop
echo "Merging release back to develop..."
git checkout develop
git merge --no-ff release/1.1.0 -m "Merge release 1.1.0 back to develop"

# Delete release branch
git branch -d release/1.1.0

echo "✅ Release branch merged back to develop and deleted"
echo ""

# Hotfix Process
echo "📝 Step 4: Hotfix Process"
echo ""

# Critical bug discovered in production
echo "Creating hotfix/critical-security-issue..."
git checkout -b hotfix/critical-security-issue main

echo "// Security fix" > src/security/patch.ts
git add src/security/patch.ts
git commit -m "fix(security): resolve critical authentication vulnerability

CVE-2025-12345: Fixed authentication bypass vulnerability
in JWT token validation.

BREAKING CHANGE: Tokens issued before this fix are invalidated."

# Update version for hotfix
echo '{
  "version": "1.1.1"
}' > package.json
git add package.json
git commit -m "chore(hotfix): bump version to 1.1.1"

echo "✅ Hotfix prepared"
echo ""

# Merge hotfix to main
echo "Merging hotfix to main..."
git checkout main
git merge --no-ff hotfix/critical-security-issue -m "Hotfix version 1.1.1

Security Fix:
- Resolved critical authentication vulnerability (CVE-2025-12345)
"

# Tag the hotfix
git tag -a v1.1.1 -m "Hotfix version 1.1.1 - Security patch"

echo "✅ Hotfix 1.1.1 merged to main and tagged"
echo ""

# Merge hotfix back to develop
echo "Merging hotfix back to develop..."
git checkout develop
git merge --no-ff hotfix/critical-security-issue -m "Merge hotfix 1.1.1 to develop"

# If release branch exists, merge there too
# git checkout release/1.2.0
# git merge --no-ff hotfix/critical-security-issue

# Delete hotfix branch
git branch -d hotfix/critical-security-issue

echo "✅ Hotfix branch merged back to develop and deleted"
echo ""

# Summary
echo "📝 GitFlow Summary"
echo "=================="
echo ""
echo "Branch Structure:"
echo "  main (production)"
echo "    └── tags: v1.0.0, v1.1.0, v1.1.1"
echo "  develop (integration)"
echo "    ├── feature/user-profile (merged)"
echo "    └── feature/notifications (merged)"
echo "  release/1.1.0 (merged, deleted)"
echo "  hotfix/critical-security-issue (merged, deleted)"
echo ""
echo "Workflow Steps:"
echo "  1. Features branch from develop"
echo "  2. Features merge back to develop (--no-ff)"
echo "  3. Release branches from develop"
echo "  4. Release merges to main (tagged) and back to develop"
echo "  5. Hotfixes branch from main"
echo "  6. Hotfixes merge to main (tagged) and back to develop"
echo ""
echo "Key Principles:"
echo "  ✓ main and develop are long-lived branches"
echo "  ✓ Never commit directly to main or develop"
echo "  ✓ Always use --no-ff for merges (preserve history)"
echo "  ✓ Tag all releases on main branch"
echo "  ✓ Hotfixes go to both main and develop"
echo ""
echo "Commands Reference:"
echo ""
echo "Feature workflow:"
echo "  git checkout -b feature/name develop"
echo "  # Make commits"
echo "  git checkout develop"
echo "  git merge --no-ff feature/name"
echo "  git branch -d feature/name"
echo ""
echo "Release workflow:"
echo "  git checkout -b release/X.Y.Z develop"
echo "  # Version bump and final fixes"
echo "  git checkout main"
echo "  git merge --no-ff release/X.Y.Z"
echo "  git tag -a vX.Y.Z -m 'Release X.Y.Z'"
echo "  git checkout develop"
echo "  git merge --no-ff release/X.Y.Z"
echo "  git branch -d release/X.Y.Z"
echo ""
echo "Hotfix workflow:"
echo "  git checkout -b hotfix/name main"
echo "  # Make fix and version bump"
echo "  git checkout main"
echo "  git merge --no-ff hotfix/name"
echo "  git tag -a vX.Y.Z -m 'Hotfix X.Y.Z'"
echo "  git checkout develop"
echo "  git merge --no-ff hotfix/name"
echo "  git branch -d hotfix/name"
echo ""
echo "✅ GitFlow workflow complete!"
