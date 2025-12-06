#!/bin/bash
#
# setup_vault.sh - Automated Vault installation and configuration
#
# Usage:
#   ./setup_vault.sh [kubernetes|docker|local]
#
# Modes:
#   kubernetes - Deploy Vault on Kubernetes (default)
#   docker     - Run Vault in Docker container
#   local      - Install and run Vault locally

set -e

MODE=${1:-kubernetes}

echo "🔐 Vault Setup Script"
echo "Mode: $MODE"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

info() {
  echo -e "${GREEN}✓${NC} $1"
}

warn() {
  echo -e "${YELLOW}⚠${NC} $1"
}

error() {
  echo -e "${RED}✗${NC} $1"
  exit 1
}

# Check if Vault CLI is installed
check_vault_cli() {
  if ! command -v vault &> /dev/null; then
    warn "Vault CLI not installed. Installing..."

    if [[ "$OSTYPE" == "darwin"* ]]; then
      brew install hashicorp/tap/vault
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
      wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
      echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
      sudo apt update && sudo apt install vault
    else
      error "Unsupported OS. Install Vault manually: https://www.vaultproject.io/downloads"
    fi

    info "Vault CLI installed"
  else
    info "Vault CLI already installed ($(vault version))"
  fi
}

# Kubernetes deployment
setup_kubernetes() {
  info "Deploying Vault on Kubernetes..."

  # Check if kubectl is available
  if ! command -v kubectl &> /dev/null; then
    error "kubectl not found. Install kubectl first."
  fi

  # Create namespace
  kubectl create namespace vault --dry-run=client -o yaml | kubectl apply -f -
  info "Namespace 'vault' created"

  # Deploy using Helm (recommended)
  if command -v helm &> /dev/null; then
    info "Using Helm for deployment..."

    helm repo add hashicorp https://helm.releases.hashicorp.com
    helm repo update

    helm install vault hashicorp/vault \
      --namespace vault \
      --set "server.dev.enabled=true" \
      --set "injector.enabled=false"

    info "Vault deployed via Helm"
  else
    # Fallback to manual deployment
    warn "Helm not found. Using manual deployment..."
    kubectl apply -f ../examples/vault-eso-setup/vault-deployment.yaml
    info "Vault deployed via kubectl"
  fi

  # Wait for pod to be ready
  info "Waiting for Vault pod to be ready..."
  kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=vault -n vault --timeout=120s

  # Initialize and unseal (dev mode)
  info "Vault is ready!"
  info "To access Vault:"
  echo "  kubectl port-forward -n vault svc/vault 8200:8200"
  echo "  export VAULT_ADDR='http://localhost:8200'"
  echo "  export VAULT_TOKEN='root'  # Dev mode root token"
}

# Docker deployment
setup_docker() {
  info "Running Vault in Docker (dev mode)..."

  docker run -d \
    --name vault-dev \
    --cap-add=IPC_LOCK \
    -e 'VAULT_DEV_ROOT_TOKEN_ID=root' \
    -p 8200:8200 \
    hashicorp/vault:latest

  info "Vault running in Docker"
  info "Access at: http://localhost:8200"
  info "Root token: root"
  echo ""
  echo "Set environment variables:"
  echo "  export VAULT_ADDR='http://localhost:8200'"
  echo "  export VAULT_TOKEN='root'"
}

# Local installation
setup_local() {
  check_vault_cli

  info "Starting Vault in dev mode..."

  # Create config directory
  mkdir -p ~/.vault

  # Start Vault in background
  nohup vault server -dev \
    -dev-root-token-id=root \
    -dev-listen-address=127.0.0.1:8200 \
    > ~/.vault/vault.log 2>&1 &

  VAULT_PID=$!
  echo $VAULT_PID > ~/.vault/vault.pid

  sleep 2

  info "Vault started (PID: $VAULT_PID)"
  info "Access at: http://localhost:8200"
  info "Root token: root"
  echo ""
  echo "Set environment variables:"
  echo "  export VAULT_ADDR='http://localhost:8200'"
  echo "  export VAULT_TOKEN='root'"
  echo ""
  echo "To stop Vault:"
  echo "  kill $(cat ~/.vault/vault.pid)"
}

# Configure Vault basics
configure_vault() {
  info "Configuring Vault..."

  # Enable KV v2 secrets engine
  vault secrets enable -path=secret kv-v2 || warn "KV v2 already enabled"
  info "KV v2 secrets engine enabled at secret/"

  # Enable database secrets engine
  vault secrets enable database || warn "Database engine already enabled"
  info "Database secrets engine enabled"

  # Enable Kubernetes auth (if in Kubernetes mode)
  if [[ "$MODE" == "kubernetes" ]]; then
    vault auth enable kubernetes || warn "Kubernetes auth already enabled"
    info "Kubernetes auth method enabled"
  fi

  info "Basic configuration complete!"
}

# Main execution
main() {
  check_vault_cli

  case $MODE in
    kubernetes)
      setup_kubernetes
      ;;
    docker)
      setup_docker
      ;;
    local)
      setup_local
      ;;
    *)
      error "Unknown mode: $MODE. Use: kubernetes, docker, or local"
      ;;
  esac

  echo ""
  info "Vault setup complete!"
  echo ""
  echo "Next steps:"
  echo "1. Set environment variables (see above)"
  echo "2. Verify connection: vault status"
  echo "3. Create secrets: vault kv put secret/myapp/config api_key=EXAMPLE"
  echo "4. Read secrets: vault kv get secret/myapp/config"
}

main
