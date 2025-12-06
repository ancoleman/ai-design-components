#!/bin/bash
# Bootstrap Flux CD on Kubernetes cluster
set -e

# Check required environment variables
if [ -z "$GITHUB_TOKEN" ]; then
  echo "Error: GITHUB_TOKEN environment variable not set"
  echo "Export your GitHub token: export GITHUB_TOKEN=<your-token>"
  exit 1
fi

if [ -z "$GITHUB_OWNER" ]; then
  echo "Error: GITHUB_OWNER environment variable not set"
  echo "Export your GitHub org/user: export GITHUB_OWNER=<your-org>"
  exit 1
fi

if [ -z "$GITHUB_REPO" ]; then
  echo "Error: GITHUB_REPO environment variable not set"
  echo "Export your repo name: export GITHUB_REPO=fleet-infra"
  exit 1
fi

echo "Bootstrapping Flux CD..."
echo "  Owner: $GITHUB_OWNER"
echo "  Repo: $GITHUB_REPO"
echo ""

# Check if flux CLI is installed
if ! command -v flux &> /dev/null; then
  echo "Flux CLI not found. Installing..."
  curl -s https://fluxcd.io/install.sh | sudo bash
fi

# Bootstrap Flux
flux bootstrap github \
  --owner="$GITHUB_OWNER" \
  --repository="$GITHUB_REPO" \
  --branch=main \
  --path=clusters/production \
  --personal

echo ""
echo "Flux installed successfully!"
echo ""
echo "Check status:"
echo "  flux check"
echo "  flux get all"
