#!/bin/bash
# Audit NetworkPolicies Script
# Find namespaces without NetworkPolicies (security risk)

set -euo pipefail

echo "=== NetworkPolicy Audit ==="
echo

# Get all namespaces (exclude kube-system and kube-public)
NAMESPACES=$(kubectl get namespaces -o json | jq -r '
  .items[] |
  select(.metadata.name | test("^kube-") | not) |
  .metadata.name
')

MISSING_POLICIES=()
HAS_POLICIES=()

echo "Checking namespaces for NetworkPolicies..."
echo

for ns in $NAMESPACES; do
  POLICY_COUNT=$(kubectl get networkpolicies -n "$ns" --no-headers 2>/dev/null | wc -l | tr -d ' ')

  if [ "$POLICY_COUNT" -eq 0 ]; then
    MISSING_POLICIES+=("$ns")
    echo "  $ns: NO POLICIES (RISK)"
  else
    HAS_POLICIES+=("$ns")
    echo "  $ns: $POLICY_COUNT policies"
  fi
done

echo
echo "=== Summary ==="
echo "Total namespaces checked: ${#MISSING_POLICIES[@]} + ${#HAS_POLICIES[@]}"
echo "Namespaces WITH policies: ${#HAS_POLICIES[@]}"
echo "Namespaces WITHOUT policies: ${#MISSING_POLICIES[@]}"

if [ ${#MISSING_POLICIES[@]} -gt 0 ]; then
  echo
  echo "WARNING: These namespaces have NO NetworkPolicies:"
  for ns in "${MISSING_POLICIES[@]}"; do
    echo "  - $ns"
  done
  echo
  echo "Recommendation: Implement default-deny NetworkPolicies"
  exit 1
else
  echo
  echo "PASS: All namespaces have NetworkPolicies"
  exit 0
fi
