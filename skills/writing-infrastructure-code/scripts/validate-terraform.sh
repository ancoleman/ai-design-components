#!/bin/bash
# Terraform Validation Script
#
# Validates Terraform code using fmt, validate, and tflint
#
# Usage:
#   ./validate-terraform.sh [directory]
#
# Example:
#   ./validate-terraform.sh ../examples/terraform/vpc-module

set -e

DIR="${1:-.}"

echo "========================================="
echo "Terraform Validation: $DIR"
echo "========================================="
echo ""

# Check if directory exists
if [ ! -d "$DIR" ]; then
  echo "Error: Directory $DIR does not exist"
  exit 1
fi

cd "$DIR"

# Check for Terraform files
if ! ls *.tf 1> /dev/null 2>&1; then
  echo "Error: No Terraform files found in $DIR"
  exit 1
fi

# 1. Format check
echo "1. Checking format (terraform fmt)..."
if terraform fmt -check -diff -recursive; then
  echo "✓ Format check passed"
else
  echo "✗ Format check failed - run 'terraform fmt -recursive' to fix"
  exit 1
fi
echo ""

# 2. Initialize
echo "2. Initializing (terraform init)..."
terraform init -backend=false > /dev/null
echo "✓ Initialization successful"
echo ""

# 3. Validate
echo "3. Validating syntax (terraform validate)..."
if terraform validate; then
  echo "✓ Validation passed"
else
  echo "✗ Validation failed"
  exit 1
fi
echo ""

# 4. tflint (if available)
if command -v tflint &> /dev/null; then
  echo "4. Running tflint..."
  if tflint --init &> /dev/null; then
    if tflint; then
      echo "✓ tflint passed"
    else
      echo "✗ tflint found issues"
      exit 1
    fi
  else
    echo "⚠ tflint init failed (skipping)"
  fi
else
  echo "⚠ tflint not installed (skipping)"
fi
echo ""

echo "========================================="
echo "All validation checks passed!"
echo "========================================="
