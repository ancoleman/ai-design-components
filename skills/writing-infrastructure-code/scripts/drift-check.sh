#!/bin/bash
# Infrastructure Drift Detection Script
#
# Detects drift between infrastructure code and actual cloud resources
#
# Usage:
#   ./drift-check.sh [directory]
#
# Example:
#   ./drift-check.sh ../environments/prod

set -e

DIR="${1:-.}"
EXIT_CODE=0

echo "========================================="
echo "Infrastructure Drift Detection"
echo "Directory: $DIR"
echo "========================================="
echo ""

cd "$DIR"

# Check if Terraform or Pulumi project
if [ -f "main.tf" ] || [ -f "*.tf" ]; then
  TOOL="terraform"
elif [ -f "Pulumi.yaml" ]; then
  TOOL="pulumi"
else
  echo "Error: No Terraform or Pulumi project found in $DIR"
  exit 1
fi

# Terraform drift detection
if [ "$TOOL" = "terraform" ]; then
  echo "Running Terraform drift detection..."
  echo ""

  # Initialize if needed
  if [ ! -d ".terraform" ]; then
    echo "Initializing Terraform..."
    terraform init > /dev/null
  fi

  # Run plan with detailed exit code
  # Exit code 0: No changes
  # Exit code 1: Error
  # Exit code 2: Changes detected (drift)
  echo "Running terraform plan..."
  if terraform plan -detailed-exitcode -no-color > drift-report.txt 2>&1; then
    echo "✓ No drift detected"
    EXIT_CODE=0
  else
    PLAN_EXIT=$?
    if [ $PLAN_EXIT -eq 2 ]; then
      echo "⚠ DRIFT DETECTED!"
      echo ""
      echo "Changes required to bring infrastructure to desired state:"
      echo ""
      cat drift-report.txt
      EXIT_CODE=2
    else
      echo "✗ Error running terraform plan"
      cat drift-report.txt
      EXIT_CODE=1
    fi
  fi

  # Save drift report
  if [ -f "drift-report.txt" ]; then
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    mv drift-report.txt "drift-report-${TIMESTAMP}.txt"
    echo ""
    echo "Drift report saved: drift-report-${TIMESTAMP}.txt"
  fi
fi

# Pulumi drift detection
if [ "$TOOL" = "pulumi" ]; then
  echo "Running Pulumi drift detection..."
  echo ""

  # Refresh state and preview
  if pulumi preview --diff --non-interactive 2>&1 | tee drift-report.txt; then
    if grep -q "no changes" drift-report.txt; then
      echo "✓ No drift detected"
      EXIT_CODE=0
    else
      echo "⚠ DRIFT DETECTED!"
      EXIT_CODE=2
    fi
  else
    echo "✗ Error running pulumi preview"
    EXIT_CODE=1
  fi

  # Save drift report
  if [ -f "drift-report.txt" ]; then
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    mv drift-report.txt "drift-report-${TIMESTAMP}.txt"
    echo ""
    echo "Drift report saved: drift-report-${TIMESTAMP}.txt"
  fi
fi

echo ""
echo "========================================="
if [ $EXIT_CODE -eq 0 ]; then
  echo "Drift check completed: No drift"
elif [ $EXIT_CODE -eq 2 ]; then
  echo "Drift check completed: DRIFT DETECTED"
else
  echo "Drift check failed"
fi
echo "========================================="

exit $EXIT_CODE
