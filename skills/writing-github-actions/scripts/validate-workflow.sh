#!/bin/bash
#
# GitHub Actions Workflow Validator
# Validates YAML syntax and common patterns in workflow files
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS] <workflow-file>

Validate GitHub Actions workflow YAML syntax and patterns.

OPTIONS:
    -h, --help          Show this help message
    -s, --strict        Enable strict mode (warnings become errors)
    -v, --verbose       Verbose output

EXAMPLES:
    $0 .github/workflows/ci.yml
    $0 --strict .github/workflows/deploy.yml
EOF
    exit 1
}

# Parse arguments
STRICT=false
VERBOSE=false
WORKFLOW_FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            ;;
        -s|--strict)
            STRICT=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        *)
            WORKFLOW_FILE="$1"
            shift
            ;;
    esac
done

# Check if workflow file provided
if [ -z "$WORKFLOW_FILE" ]; then
    echo -e "${RED}Error: No workflow file specified${NC}"
    usage
fi

# Check if file exists
if [ ! -f "$WORKFLOW_FILE" ]; then
    echo -e "${RED}Error: File not found: $WORKFLOW_FILE${NC}"
    exit 1
fi

# Check if file is YAML
if [[ ! "$WORKFLOW_FILE" =~ \.(yml|yaml)$ ]]; then
    echo -e "${YELLOW}Warning: File does not have .yml or .yaml extension${NC}"
fi

echo "Validating workflow: $WORKFLOW_FILE"
echo ""

# Error and warning counters
ERRORS=0
WARNINGS=0

# Check 1: YAML syntax
echo "Checking YAML syntax..."
if command -v yq &> /dev/null; then
    if yq eval '.' "$WORKFLOW_FILE" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Valid YAML syntax"
    else
        echo -e "${RED}✗${NC} Invalid YAML syntax"
        ERRORS=$((ERRORS + 1))
        yq eval '.' "$WORKFLOW_FILE" 2>&1 | head -5
    fi
elif command -v python3 &> /dev/null; then
    if python3 -c "import yaml; yaml.safe_load(open('$WORKFLOW_FILE'))" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Valid YAML syntax"
    else
        echo -e "${RED}✗${NC} Invalid YAML syntax"
        ERRORS=$((ERRORS + 1))
        python3 -c "import yaml; yaml.safe_load(open('$WORKFLOW_FILE'))" 2>&1 | head -5
    fi
else
    echo -e "${YELLOW}⚠${NC} Cannot validate YAML (install yq or python3 with pyyaml)"
    WARNINGS=$((WARNINGS + 1))
fi

# Check 2: Required fields
echo "Checking required fields..."
if grep -q "^on:" "$WORKFLOW_FILE" || grep -q "^'on':" "$WORKFLOW_FILE"; then
    echo -e "${GREEN}✓${NC} Has 'on' trigger definition"
else
    echo -e "${RED}✗${NC} Missing 'on' trigger definition"
    ERRORS=$((ERRORS + 1))
fi

if grep -q "^jobs:" "$WORKFLOW_FILE"; then
    echo -e "${GREEN}✓${NC} Has 'jobs' definition"
else
    echo -e "${RED}✗${NC} Missing 'jobs' definition"
    ERRORS=$((ERRORS + 1))
fi

# Check 3: Security patterns
echo "Checking security patterns..."

# Check for pinned actions (should use commit SHA)
UNPINNED=$(grep -E "uses:.*@(v[0-9]|main|master)" "$WORKFLOW_FILE" || true)
if [ -n "$UNPINNED" ]; then
    echo -e "${YELLOW}⚠${NC} Found unpinned actions (recommend pinning to commit SHA):"
    echo "$UNPINNED" | while read -r line; do
        echo "  $line"
    done
    WARNINGS=$((WARNINGS + 1))
fi

# Check for hardcoded secrets
if grep -iE "(password|token|key|secret).*[:=].*['\"][^$]" "$WORKFLOW_FILE" | grep -v "secrets\." | grep -v "inputs\." > /dev/null; then
    echo -e "${RED}✗${NC} Possible hardcoded secrets found"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓${NC} No obvious hardcoded secrets"
fi

# Check for minimal permissions
if grep -q "permissions:" "$WORKFLOW_FILE"; then
    echo -e "${GREEN}✓${NC} Has permissions defined"
else
    echo -e "${YELLOW}⚠${NC} No permissions defined (recommend explicit permissions)"
    WARNINGS=$((WARNINGS + 1))
fi

# Check 4: Best practices
echo "Checking best practices..."

# Check for caching
if grep -q "cache:" "$WORKFLOW_FILE" || grep -q "actions/cache" "$WORKFLOW_FILE"; then
    echo -e "${GREEN}✓${NC} Uses caching"
else
    echo -e "${YELLOW}⚠${NC} No caching detected (consider adding for performance)"
    WARNINGS=$((WARNINGS + 1))
fi

# Check for concurrency control
if grep -q "concurrency:" "$WORKFLOW_FILE"; then
    echo -e "${GREEN}✓${NC} Has concurrency control"
else
    if [ "$VERBOSE" = true ]; then
        echo -e "${YELLOW}ℹ${NC} No concurrency control (consider adding for PR workflows)"
    fi
fi

# Check for timeout settings
if grep -q "timeout-minutes:" "$WORKFLOW_FILE"; then
    echo -e "${GREEN}✓${NC} Has timeout settings"
else
    if [ "$VERBOSE" = true ]; then
        echo -e "${YELLOW}ℹ${NC} No timeout settings (workflows default to 360 minutes)"
    fi
fi

# Check 5: Common issues
echo "Checking for common issues..."

# Check for shell specification in run steps
if grep -q "^  *run:" "$WORKFLOW_FILE"; then
    # This is a simplified check; actual validation would be more complex
    echo -e "${GREEN}✓${NC} Has run commands"
fi

# Check for proper indentation (basic check)
if grep -E "^ {1,2}[a-z]" "$WORKFLOW_FILE" > /dev/null; then
    echo -e "${YELLOW}⚠${NC} Possible indentation issues (use 2-space indentation)"
    WARNINGS=$((WARNINGS + 1))
fi

# Summary
echo ""
echo "================================"
echo "Validation Summary"
echo "================================"
echo "Errors:   $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

# Exit code
if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}VALIDATION FAILED${NC}"
    exit 1
elif [ "$STRICT" = true ] && [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}VALIDATION FAILED (strict mode)${NC}"
    exit 1
else
    echo -e "${GREEN}VALIDATION PASSED${NC}"
    exit 0
fi
