#!/bin/bash
# Trivy Basic Container Scanning Examples

set -e

IMAGE="${1:-alpine:latest}"

echo "=== Trivy Basic Scanning Examples ==="
echo "Image: $IMAGE"
echo ""

# Example 1: Basic scan
echo "1. Basic scan (all vulnerabilities)"
trivy image "$IMAGE"
echo ""

# Example 2: Severity filtering
echo "2. Scan with severity filter (HIGH, CRITICAL only)"
trivy image --severity HIGH,CRITICAL "$IMAGE"
echo ""

# Example 3: Exit code (fail build on findings)
echo "3. Exit code mode (fail on HIGH/CRITICAL)"
trivy image --severity HIGH,CRITICAL --exit-code 1 "$IMAGE" || echo "Build would fail due to vulnerabilities"
echo ""

# Example 4: Ignore unfixed vulnerabilities
echo "4. Ignore unfixed vulnerabilities"
trivy image --ignore-unfixed --severity HIGH,CRITICAL "$IMAGE"
echo ""

# Example 5: Specific vulnerability types
echo "5. Scan only OS packages"
trivy image --vuln-type os "$IMAGE"
echo ""

# Example 6: JSON output
echo "6. JSON output for automation"
trivy image --format json --output scan-results.json "$IMAGE"
echo "Results saved to scan-results.json"
jq '.Results[].Vulnerabilities | length' scan-results.json | head -1 | xargs echo "Total vulnerabilities:"
echo ""

# Example 7: Table output (formatted)
echo "7. Table output (formatted)"
trivy image --format table "$IMAGE"
echo ""

# Example 8: Scan specific directories
echo "8. Skip directories"
trivy image --skip-dirs /usr/share/doc,/var/lib/dpkg "$IMAGE"
echo ""

# Example 9: Quiet mode
echo "9. Quiet mode (minimal output)"
trivy image --quiet --severity CRITICAL "$IMAGE"
echo ""

# Example 10: Template output (custom format)
echo "10. Custom template output"
trivy image --format template --template '{{- range .Results }}{{ range .Vulnerabilities }}{{ .VulnerabilityID }},{{ .Severity }},{{ .PkgName }}
{{ end }}{{ end }}' "$IMAGE" > vulnerabilities.csv
echo "CSV output saved to vulnerabilities.csv"
head -5 vulnerabilities.csv
echo ""

echo "=== Scan complete ==="