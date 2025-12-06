#!/bin/bash

# Validate Commit Message Format
# Enforces conventional commit format: <type>[optional scope]: <description>

set -e

# Get commit message (either from file or stdin)
if [ -n "$1" ]; then
  COMMIT_MSG=$(cat "$1")
else
  COMMIT_MSG=$(cat)
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Valid commit types
VALID_TYPES="feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert"

# Commit message pattern
# Format: <type>[optional scope]: <description>
PATTERN="^(${VALID_TYPES})(\([a-z0-9-]+\))?!?: .{1,100}$"

# Extract first line (subject)
SUBJECT=$(echo "$COMMIT_MSG" | head -n 1)

# Validation functions
validate_format() {
  if ! echo "$SUBJECT" | grep -qE "$PATTERN"; then
    return 1
  fi
  return 0
}

validate_type() {
  TYPE=$(echo "$SUBJECT" | sed -E 's/^([a-z]+).*/\1/')
  if ! echo "$TYPE" | grep -qE "^(${VALID_TYPES})$"; then
    echo -e "${RED}❌ Invalid type: '$TYPE'${NC}"
    echo ""
    echo "Valid types:"
    echo "  feat     - New feature"
    echo "  fix      - Bug fix"
    echo "  docs     - Documentation only"
    echo "  style    - Formatting, missing semicolons"
    echo "  refactor - Code restructuring"
    echo "  perf     - Performance improvement"
    echo "  test     - Adding tests"
    echo "  build    - Build system changes"
    echo "  ci       - CI configuration"
    echo "  chore    - Maintenance tasks"
    echo "  revert   - Revert previous commit"
    return 1
  fi
  return 0
}

validate_scope() {
  # Scope is optional, but if present must be lowercase
  if echo "$SUBJECT" | grep -q '('; then
    SCOPE=$(echo "$SUBJECT" | sed -E 's/^[a-z]+\(([^)]+)\).*/\1/')
    if ! echo "$SCOPE" | grep -qE '^[a-z0-9-]+$'; then
      echo -e "${RED}❌ Invalid scope: '$SCOPE'${NC}"
      echo "Scope must be lowercase with hyphens only"
      return 1
    fi
  fi
  return 0
}

validate_description() {
  # Extract description (after colon)
  if ! echo "$SUBJECT" | grep -q ':'; then
    echo -e "${RED}❌ Missing colon after type/scope${NC}"
    echo "Format: <type>[scope]: <description>"
    return 1
  fi

  DESC=$(echo "$SUBJECT" | sed -E 's/^[a-z]+(\([^)]+\))?!?: (.*)$/\2/')

  # Check description exists
  if [ -z "$DESC" ]; then
    echo -e "${RED}❌ Missing description${NC}"
    return 1
  fi

  # Check description is lowercase
  if echo "$DESC" | grep -qE '^[A-Z]'; then
    echo -e "${RED}❌ Description must start with lowercase${NC}"
    echo "Current: '$DESC'"
    echo "Correct: '$(echo "$DESC" | sed 's/^\(.\)/\L\1/')'"
    return 1
  fi

  # Check description doesn't end with period
  if echo "$DESC" | grep -q '\.$'; then
    echo -e "${RED}❌ Description must not end with period${NC}"
    return 1
  fi

  # Check length
  if [ ${#DESC} -gt 100 ]; then
    echo -e "${RED}❌ Description too long (${#DESC} > 100 chars)${NC}"
    return 1
  fi

  if [ ${#DESC} -lt 3 ]; then
    echo -e "${RED}❌ Description too short (${#DESC} < 3 chars)${NC}"
    return 1
  fi

  return 0
}

validate_subject_length() {
  if [ ${#SUBJECT} -gt 100 ]; then
    echo -e "${RED}❌ Subject line too long (${#SUBJECT} > 100 chars)${NC}"
    return 1
  fi
  return 0
}

# Main validation
echo "🔍 Validating commit message..."
echo ""
echo "Subject: $SUBJECT"
echo ""

# Track errors
ERRORS=0

# Run all validations
if ! validate_format; then
  echo -e "${RED}❌ Invalid commit message format${NC}"
  echo ""
  echo "Expected format:"
  echo "  <type>[optional scope]: <description>"
  echo ""
  echo "Examples:"
  echo "  feat: add user authentication"
  echo "  fix(api): resolve timeout issue"
  echo "  feat(auth)!: redesign authentication API"
  echo ""
  ERRORS=$((ERRORS + 1))
else
  if ! validate_type; then
    ERRORS=$((ERRORS + 1))
  fi

  if ! validate_scope; then
    ERRORS=$((ERRORS + 1))
  fi

  if ! validate_description; then
    ERRORS=$((ERRORS + 1))
  fi

  if ! validate_subject_length; then
    ERRORS=$((ERRORS + 1))
  fi
fi

# Check for warnings
WARNINGS=0

# Warn about merge commits
if echo "$SUBJECT" | grep -qE "^Merge"; then
  echo -e "${YELLOW}⚠️  Warning: Merge commit detected${NC}"
  echo "Consider using squash and merge for cleaner history"
  WARNINGS=$((WARNINGS + 1))
fi

# Warn about WIP commits
if echo "$SUBJECT" | grep -qiE "\bwip\b"; then
  echo -e "${YELLOW}⚠️  Warning: WIP commit detected${NC}"
  echo "Remember to squash WIP commits before merging"
  WARNINGS=$((WARNINGS + 1))
fi

# Result
echo ""
if [ $ERRORS -eq 0 ]; then
  echo -e "${GREEN}✅ Commit message is valid${NC}"
  if [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}   ($WARNINGS warning(s))${NC}"
  fi
  exit 0
else
  echo -e "${RED}❌ Commit message validation failed${NC}"
  echo -e "${RED}   $ERRORS error(s)${NC}"
  echo ""
  echo "Fix the commit message or use --no-verify to skip validation"
  exit 1
fi
