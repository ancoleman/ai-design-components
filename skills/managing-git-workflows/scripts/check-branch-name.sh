#!/bin/bash

# Validate Branch Name Convention
# Enforces branch naming pattern: <type>/<description>

set -e

# Get branch name
if [ -n "$1" ]; then
  BRANCH_NAME="$1"
else
  BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Valid branch types
VALID_TYPES="feature|bugfix|hotfix|release|docs|refactor|test|chore"

# Branch name pattern
# Format: <type>/<description-with-hyphens>
PATTERN="^(${VALID_TYPES})/[a-z0-9-]+$"

# Protected branches that don't need to follow pattern
PROTECTED_BRANCHES="main|develop|master|staging|production"

# Validation functions
is_protected_branch() {
  if echo "$BRANCH_NAME" | grep -qE "^(${PROTECTED_BRANCHES})$"; then
    return 0
  fi
  return 1
}

validate_format() {
  if ! echo "$BRANCH_NAME" | grep -qE "$PATTERN"; then
    return 1
  fi
  return 0
}

validate_type() {
  TYPE=$(echo "$BRANCH_NAME" | sed -E 's/^([a-z]+)\/.*/\1/')
  if ! echo "$TYPE" | grep -qE "^(${VALID_TYPES})$"; then
    echo -e "${RED}❌ Invalid branch type: '$TYPE'${NC}"
    echo ""
    echo "Valid types:"
    echo "  feature  - New features"
    echo "  bugfix   - Bug fixes"
    echo "  hotfix   - Urgent production fixes"
    echo "  release  - Release preparation"
    echo "  docs     - Documentation changes"
    echo "  refactor - Code refactoring"
    echo "  test     - Test updates"
    echo "  chore    - Maintenance tasks"
    return 1
  fi
  return 0
}

validate_description() {
  # Extract description (after slash)
  if ! echo "$BRANCH_NAME" | grep -q '/'; then
    echo -e "${RED}❌ Missing slash separator${NC}"
    echo "Format: <type>/<description>"
    return 1
  fi

  DESC=$(echo "$BRANCH_NAME" | sed -E 's/^[a-z]+\/(.*)$/\1/')

  # Check description exists
  if [ -z "$DESC" ]; then
    echo -e "${RED}❌ Missing description${NC}"
    return 1
  fi

  # Check description is lowercase with hyphens
  if ! echo "$DESC" | grep -qE '^[a-z0-9-]+$'; then
    echo -e "${RED}❌ Description must be lowercase with hyphens only${NC}"
    echo "Current: '$DESC'"
    echo "Allowed: a-z, 0-9, hyphens"
    return 1
  fi

  # Check no consecutive hyphens
  if echo "$DESC" | grep -q '--'; then
    echo -e "${RED}❌ No consecutive hyphens allowed${NC}"
    return 1
  fi

  # Check doesn't start or end with hyphen
  if echo "$DESC" | grep -qE '^-|-$'; then
    echo -e "${RED}❌ Description cannot start or end with hyphen${NC}"
    return 1
  fi

  # Check minimum length
  if [ ${#DESC} -lt 3 ]; then
    echo -e "${RED}❌ Description too short (${#DESC} < 3 chars)${NC}"
    return 1
  fi

  # Check maximum length
  if [ ${#DESC} -gt 50 ]; then
    echo -e "${YELLOW}⚠️  Warning: Description is long (${#DESC} > 50 chars)${NC}"
    echo "Consider using shorter branch names"
  fi

  return 0
}

# Main validation
echo "🔍 Validating branch name..."
echo ""
echo "Branch: $BRANCH_NAME"
echo ""

# Skip validation for protected branches
if is_protected_branch; then
  echo -e "${GREEN}✅ Protected branch (validation skipped)${NC}"
  exit 0
fi

# Track errors
ERRORS=0

# Run all validations
if ! validate_format; then
  echo -e "${RED}❌ Invalid branch name format${NC}"
  echo ""
  echo "Expected format:"
  echo "  <type>/<description-with-hyphens>"
  echo ""
  echo "Examples:"
  echo "  feature/user-authentication"
  echo "  bugfix/login-timeout"
  echo "  hotfix/critical-security-issue"
  echo "  release/v1.2.0"
  echo ""
  ERRORS=$((ERRORS + 1))
else
  if ! validate_type; then
    ERRORS=$((ERRORS + 1))
  fi

  if ! validate_description; then
    ERRORS=$((ERRORS + 1))
  fi
fi

# Check for common mistakes
WARNINGS=0

# Warn about uppercase letters
if echo "$BRANCH_NAME" | grep -qE '[A-Z]'; then
  echo -e "${YELLOW}⚠️  Warning: Branch name contains uppercase letters${NC}"
  echo "Branch names should be lowercase"
  WARNINGS=$((WARNINGS + 1))
fi

# Warn about underscores
if echo "$BRANCH_NAME" | grep -q '_'; then
  echo -e "${YELLOW}⚠️  Warning: Branch name contains underscores${NC}"
  echo "Use hyphens instead: ${BRANCH_NAME//_/-}"
  WARNINGS=$((WARNINGS + 1))
fi

# Warn about spaces
if echo "$BRANCH_NAME" | grep -q ' '; then
  echo -e "${YELLOW}⚠️  Warning: Branch name contains spaces${NC}"
  echo "Use hyphens instead"
  WARNINGS=$((WARNINGS + 1))
fi

# Suggest better names for common patterns
suggest_better_name() {
  local SUGGESTED=""

  # Convert to lowercase
  SUGGESTED=$(echo "$BRANCH_NAME" | tr '[:upper:]' '[:lower:]')

  # Replace underscores with hyphens
  SUGGESTED=$(echo "$SUGGESTED" | tr '_' '-')

  # Remove special characters
  SUGGESTED=$(echo "$SUGGESTED" | sed 's/[^a-z0-9\/-]/-/g')

  # Remove consecutive hyphens
  SUGGESTED=$(echo "$SUGGESTED" | sed 's/--*/-/g')

  # Remove leading/trailing hyphens
  SUGGESTED=$(echo "$SUGGESTED" | sed 's/^-//' | sed 's/-$//')

  if [ "$SUGGESTED" != "$BRANCH_NAME" ]; then
    echo ""
    echo -e "${YELLOW}💡 Suggested name: $SUGGESTED${NC}"
  fi
}

# Result
echo ""
if [ $ERRORS -eq 0 ]; then
  echo -e "${GREEN}✅ Branch name is valid${NC}"
  if [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}   ($WARNINGS warning(s))${NC}"
    suggest_better_name
  fi
  exit 0
else
  echo -e "${RED}❌ Branch name validation failed${NC}"
  echo -e "${RED}   $ERRORS error(s)${NC}"
  suggest_better_name
  echo ""
  echo "Rename the branch:"
  echo "  git branch -m $BRANCH_NAME <new-name>"
  exit 1
fi
