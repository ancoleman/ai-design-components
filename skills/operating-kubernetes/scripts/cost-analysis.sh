#!/bin/bash
# Cost Analysis Script
# Calculate resource costs by namespace

set -euo pipefail

# Cost per resource (example pricing)
COST_PER_CPU_HOUR=0.03  # $0.03 per CPU core per hour
COST_PER_GB_HOUR=0.004  # $0.004 per GB memory per hour

echo "=== Kubernetes Resource Cost Analysis ==="
echo

# Get all pods
PODS=$(kubectl get pods -A -o json)

# Calculate costs by namespace
NAMESPACES=$(echo "$PODS" | jq -r '.items[].metadata.namespace' | sort -u)

printf "%-30s %10s %12s %14s %12s\n" "Namespace" "CPU Cores" "Memory (GB)" "Cost/Hour" "Cost/Month"
echo "--------------------------------------------------------------------------------"

TOTAL_CPU=0
TOTAL_MEMORY=0

for ns in $NAMESPACES; do
  # Calculate CPU requests (convert 'm' to cores)
  CPU=$(echo "$PODS" | jq -r --arg ns "$ns" '
    .items[] |
    select(.metadata.namespace == $ns) |
    .spec.containers[].resources.requests.cpu // "0" |
    if endswith("m") then
      (.[:-1] | tonumber) / 1000
    else
      tonumber
    end
  ' | awk '{sum += $1} END {print sum}')

  # Calculate memory requests (convert to GB)
  MEMORY=$(echo "$PODS" | jq -r --arg ns "$ns" '
    .items[] |
    select(.metadata.namespace == $ns) |
    .spec.containers[].resources.requests.memory // "0" |
    if endswith("Mi") then
      (.[:-2] | tonumber) / 1024
    elif endswith("Gi") then
      .[:-2] | tonumber
    else
      0
    end
  ' | awk '{sum += $1} END {print sum}')

  # Calculate costs
  COST_HOUR=$(echo "$CPU $MEMORY" | awk -v cpu_cost=$COST_PER_CPU_HOUR -v mem_cost=$COST_PER_GB_HOUR '{
    print ($1 * cpu_cost) + ($2 * mem_cost)
  }')

  COST_MONTH=$(echo "$COST_HOUR" | awk '{print $1 * 24 * 30}')

  # Print row
  printf "%-30s %10.2f %12.2f \$%11.2f \$%10.2f\n" \
    "$ns" "$CPU" "$MEMORY" "$COST_HOUR" "$COST_MONTH"

  TOTAL_CPU=$(echo "$TOTAL_CPU $CPU" | awk '{print $1 + $2}')
  TOTAL_MEMORY=$(echo "$TOTAL_MEMORY $MEMORY" | awk '{print $1 + $2}')
done

# Totals
TOTAL_COST_HOUR=$(echo "$TOTAL_CPU $TOTAL_MEMORY" | awk -v cpu_cost=$COST_PER_CPU_HOUR -v mem_cost=$COST_PER_GB_HOUR '{
  print ($1 * cpu_cost) + ($2 * mem_cost)
}')
TOTAL_COST_MONTH=$(echo "$TOTAL_COST_HOUR" | awk '{print $1 * 24 * 30}')

echo "--------------------------------------------------------------------------------"
printf "%-30s %10.2f %12.2f \$%11.2f \$%10.2f\n" \
  "TOTAL" "$TOTAL_CPU" "$TOTAL_MEMORY" "$TOTAL_COST_HOUR" "$TOTAL_COST_MONTH"

echo
echo "* Costs based on: CPU \$$COST_PER_CPU_HOUR/core/hr, Memory \$$COST_PER_GB_HOUR/GB/hr"
echo "* Actual cloud costs may vary based on instance types and commitments"
