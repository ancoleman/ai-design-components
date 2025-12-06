#!/usr/bin/env bash
# Validate OpenAPI specifications
# Requires: spectral (npm install -g @stoplight/spectral-cli)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLES_DIR="$SCRIPT_DIR/../examples/openapi"

echo "Validating OpenAPI specifications..."

if ! command -v spectral &> /dev/null; then
    echo "Error: spectral not found"
    echo "Install: npm install -g @stoplight/spectral-cli"
    exit 1
fi

for spec in "$EXAMPLES_DIR"/*.yaml; do
    echo "Validating: $(basename "$spec")"
    spectral lint "$spec" || true
done

echo "Validation complete"
