#!/bin/bash

# GitHub Flow Complete Workflow Example
# This script demonstrates a complete GitHub Flow workflow from feature creation to deployment

set -e  # Exit on error

echo "🚀 GitHub Flow Workflow Example"
echo "================================"
echo ""

# Step 1: Create feature branch from main
echo "📝 Step 1: Create feature branch from main"
git checkout main
git pull origin main
git checkout -b feature/user-authentication

echo "✅ Created feature branch: feature/user-authentication"
echo ""

# Step 2: Make changes and commit
echo "📝 Step 2: Make changes with conventional commits"

# Simulate file changes
echo "// JWT authentication middleware" > src/auth/jwt.ts
git add src/auth/jwt.ts
git commit -m "feat(auth): add JWT authentication middleware

Implements JWT token generation and validation
for user authentication."

echo "// User login endpoint" > src/api/login.ts
git add src/api/login.ts
git commit -m "feat(api): add user login endpoint

POST /api/login endpoint that accepts credentials
and returns JWT token."

echo "// Authentication tests" > tests/auth.test.ts
git add tests/auth.test.ts
git commit -m "test(auth): add authentication tests

Unit tests for JWT middleware and login endpoint.
Coverage: 95%"

echo "✅ Created 3 commits with conventional format"
echo ""

# Step 3: Push and create PR
echo "📝 Step 3: Push branch and create pull request"
git push origin feature/user-authentication

# Create PR using GitHub CLI (if available)
if command -v gh &> /dev/null; then
  gh pr create \
    --title "Add user authentication" \
    --body "## Description
Implements JWT-based user authentication.

## Changes
- JWT middleware for token validation
- Login endpoint for credential verification
- Comprehensive test coverage

## Type of Change
- [x] New feature

## Testing
- [x] Unit tests added (95% coverage)
- [x] Integration tests added
- [x] Manual testing completed

Closes #123"

  echo "✅ Pull request created via GitHub CLI"
else
  echo "⚠️  GitHub CLI not installed. Create PR manually at:"
  echo "   https://github.com/org/repo/compare/main...feature/user-authentication"
fi
echo ""

# Step 4: Code review process
echo "📝 Step 4: Code review process"
echo "
Code review workflow:
1. Request review from code owners
2. Reviewers provide feedback
3. Address feedback with additional commits
4. Request re-review after changes
5. Merge after approval

To address feedback:
  git add <files>
  git commit -m 'fix(auth): handle edge case in token validation'
  git push origin feature/user-authentication
"
echo ""

# Step 5: Merge to main
echo "📝 Step 5: Merge to main (after approval)"
echo "
Merge options:
1. Squash and merge (recommended for clean history)
   - Combines all commits into one
   - Main branch has linear history

2. Merge commit (preserve all commits)
   - Keeps all individual commits
   - Creates merge commit

3. Rebase and merge (linear history)
   - Replays commits on top of main
   - No merge commit

To merge via GitHub CLI:
  gh pr merge --squash --delete-branch

Or merge via GitHub UI:
  - Click 'Squash and merge'
  - Confirm merge
  - Delete branch
"
echo ""

# Step 6: Post-merge cleanup
echo "📝 Step 6: Post-merge cleanup"
echo "
After merge:
1. Automated deployment triggers
2. CI/CD pipeline runs
3. Feature deployed to production
4. Branch is deleted automatically

Local cleanup:
  git checkout main
  git pull origin main
  git branch -d feature/user-authentication
"
echo ""

# Example of continuous deployment
echo "📝 Step 7: Continuous deployment"
echo "
GitHub Actions automatically:
1. Runs tests
2. Builds application
3. Deploys to staging
4. Runs smoke tests
5. Deploys to production
6. Notifies team

See .github/workflows/deploy.yml for configuration
"
echo ""

echo "✅ GitHub Flow workflow complete!"
echo ""
echo "Key Principles:"
echo "  ✓ Main branch is always deployable"
echo "  ✓ Every merge triggers deployment"
echo "  ✓ Code review via pull requests"
echo "  ✓ Automated testing and deployment"
echo "  ✓ Fast feedback loop"
