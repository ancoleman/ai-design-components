#!/bin/bash
# Validate Resources Script
# Check that all pods have resource requests and limits set

set -euo pipefail

NAMESPACE="${1:-}"

if [ -z "$NAMESPACE" ]; then
  echo "Usage: $0 <namespace>"
  echo "Example: $0 production"
  exit 1
fi

echo "=== Validating Resources in Namespace: $NAMESPACE ==="
echo

# Get all pods in namespace
PODS=$(kubectl get pods -n "$NAMESPACE" -o json)

# Check for missing requests
echo "Checking for missing resource requests..."
MISSING_REQUESTS=$(echo "$PODS" | jq -r '
  .items[] |
  select(.spec.containers[]? | .resources.requests == null) |
  .metadata.name
')

if [ -n "$MISSING_REQUESTS" ]; then
  echo "ERROR: Pods without resource requests:"
  echo "$MISSING_REQUESTS" | while read -r pod; do
    echo "  - $pod"
  done
  echo
else
  echo "PASS: All pods have resource requests"
  echo
fi

# Check for missing limits
echo "Checking for missing resource limits..."
MISSING_LIMITS=$(echo "$PODS" | jq -r '
  .items[] |
  select(.spec.containers[]? | .resources.limits == null) |
  .metadata.name
')

if [ -n "$MISSING_LIMITS" ]; then
  echo "WARNING: Pods without resource limits:"
  echo "$MISSING_LIMITS" | while read -r pod; do
    echo "  - $pod"
  done
  echo
else
  echo "PASS: All pods have resource limits"
  echo
fi

# Summary
TOTAL_PODS=$(echo "$PODS" | jq '.items | length')
echo "=== Summary ==="
echo "Total pods checked: $TOTAL_PODS"

if [ -z "$MISSING_REQUESTS" ] && [ -z "$MISSING_LIMITS" ]; then
  echo "Status: ALL CHECKS PASSED"
  exit 0
elif [ -n "$MISSING_REQUESTS" ]; then
  echo "Status: FAILED (missing requests)"
  exit 1
else
  echo "Status: WARNINGS (missing limits)"
  exit 0
fi
