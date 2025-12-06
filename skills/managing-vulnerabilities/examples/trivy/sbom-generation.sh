#!/bin/bash
# Trivy SBOM Generation and Scanning Examples

set -e

IMAGE="${1:-alpine:latest}"

echo "=== Trivy SBOM Examples ==="
echo "Image: $IMAGE"
echo ""

# Example 1: Generate CycloneDX SBOM
echo "1. Generate CycloneDX SBOM (recommended for security)"
trivy image --format cyclonedx --output sbom-cyclonedx.json "$IMAGE"
echo "CycloneDX SBOM saved to sbom-cyclonedx.json"
jq '.components | length' sbom-cyclonedx.json | xargs echo "Component count:"
echo ""

# Example 2: Generate SPDX SBOM
echo "2. Generate SPDX SBOM (for compliance)"
trivy image --format spdx-json --output sbom-spdx.json "$IMAGE"
echo "SPDX SBOM saved to sbom-spdx.json"
jq '.packages | length' sbom-spdx.json | xargs echo "Package count:"
echo ""

# Example 3: Scan SBOM (faster than re-scanning image)
echo "3. Scan existing SBOM"
trivy sbom sbom-cyclonedx.json --severity HIGH,CRITICAL
echo ""

# Example 4: Generate SBOM with vulnerabilities
echo "4. Generate SBOM with vulnerability data included"
trivy image --format cyclonedx --scanners vuln --output sbom-with-vulns.json "$IMAGE"
echo "SBOM with vulnerabilities saved to sbom-with-vulns.json"
jq '.vulnerabilities | length' sbom-with-vulns.json | xargs echo "Vulnerability count in SBOM:"
echo ""

# Example 5: SBOM for filesystem
echo "5. Generate SBOM for local filesystem"
trivy fs --format cyclonedx --output sbom-fs.json .
echo "Filesystem SBOM saved to sbom-fs.json"
echo ""

# Example 6: Compare SBOMs
echo "6. Extract package lists for comparison"
jq -r '.components[] | "\(.name)@\(.version)"' sbom-cyclonedx.json | sort > packages.txt
echo "Package list saved to packages.txt"
head -10 packages.txt
echo ""

# Clean up
echo "=== SBOM generation complete ==="
echo "Files created:"
ls -lh sbom-*.json packages.txt
