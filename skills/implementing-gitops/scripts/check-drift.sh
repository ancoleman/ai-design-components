#!/bin/bash
# Check for configuration drift in GitOps deployments
set -e

TOOL=${1:-auto}

detect_tool() {
  if [ "$TOOL" != "auto" ]; then
    echo "$TOOL"
    return
  fi

  if kubectl get namespace argocd &>/dev/null; then
    echo "argocd"
  elif kubectl get namespace flux-system &>/dev/null; then
    echo "flux"
  else
    echo "none"
  fi
}

check_argocd_drift() {
  echo "Checking ArgoCD drift..."
  echo ""

  # Check if argocd CLI is available
  if ! command -v argocd &> /dev/null; then
    echo "argocd CLI not found. Install from: https://argo-cd.readthedocs.io/en/stable/cli_installation/"
    exit 1
  fi

  # List applications
  argocd app list

  echo ""
  echo "Check specific application drift:"
  echo "  argocd app get <app-name>"
  echo "  argocd app diff <app-name>"
}

check_flux_drift() {
  echo "Checking Flux drift..."
  echo ""

  # Check if flux CLI is available
  if ! command -v flux &> /dev/null; then
    echo "flux CLI not found. Install from: https://fluxcd.io/docs/installation/"
    exit 1
  fi

  # List all resources
  flux get all

  echo ""
  echo "Check specific resource:"
  echo "  flux get kustomizations"
  echo "  flux get helmreleases"
  echo ""
  echo "Force reconciliation:"
  echo "  flux reconcile kustomization <name> --with-source"
}

DETECTED_TOOL=$(detect_tool)

case $DETECTED_TOOL in
  argocd)
    check_argocd_drift
    ;;
  flux)
    check_flux_drift
    ;;
  none)
    echo "No GitOps tool detected (ArgoCD or Flux)"
    echo "Specify tool: $0 argocd|flux"
    exit 1
    ;;
  *)
    echo "Unknown tool: $DETECTED_TOOL"
    echo "Usage: $0 [argocd|flux]"
    exit 1
    ;;
esac
