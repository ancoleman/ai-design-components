#!/bin/bash
# Infrastructure Security Scanning Script
# Runs multiple security scanners and generates reports

set -euo pipefail

# Configuration
REPORT_DIR="${REPORT_DIR:-./security-reports}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "=== Infrastructure Security Scanning ==="
echo "Report directory: $REPORT_DIR"
echo "Timestamp: $TIMESTAMP"
echo

# Create report directory
mkdir -p "$REPORT_DIR"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to run scanner if available
run_scanner() {
    local name=$1
    shift
    local command="$@"

    if command_exists "$(echo $command | awk '{print $1}')"; then
        echo "[✓] Running $name..."
        eval "$command" || echo "[!] $name completed with warnings"
    else
        echo "[✗] $name not installed, skipping"
    fi
}

# Docker CIS Benchmark
if command_exists docker; then
    echo
    echo "=== Docker Security Scan ==="
    run_scanner "docker-bench-security" \
        "docker run --rm --net host --pid host --userns host --cap-add audit_control \
         -v /var/lib:/var/lib:ro \
         -v /var/run/docker.sock:/var/run/docker.sock:ro \
         -v /etc:/etc:ro \
         docker/docker-bench-security > $REPORT_DIR/docker-bench-$TIMESTAMP.txt"
fi

# Kubernetes CIS Benchmark
if command_exists kubectl; then
    echo
    echo "=== Kubernetes Security Scan ==="
    run_scanner "kube-bench" \
        "kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml && \
         sleep 10 && \
         kubectl logs job/kube-bench > $REPORT_DIR/kube-bench-$TIMESTAMP.txt && \
         kubectl delete job/kube-bench"
fi

# Container Image Scanning with Trivy
if command_exists trivy; then
    echo
    echo "=== Container Image Scanning ==="

    # Scan images (replace with your images)
    IMAGES=$(docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>")

    for image in $IMAGES; do
        echo "Scanning $image..."
        run_scanner "trivy image scan" \
            "trivy image --severity HIGH,CRITICAL --format json \
             --output $REPORT_DIR/trivy-${image//[:\/]/_}-$TIMESTAMP.json \
             $image"
    done
fi

# Linux System Audit with Lynis
if command_exists lynis; then
    echo
    echo "=== Linux System Audit ==="
    run_scanner "lynis" \
        "sudo lynis audit system --quick --report-file $REPORT_DIR/lynis-$TIMESTAMP.txt"
fi

# AWS Security Scan with Prowler
if command_exists prowler; then
    echo
    echo "=== AWS Security Scan ==="
    run_scanner "prowler" \
        "prowler aws --output-modes json html \
         --output-directory $REPORT_DIR/prowler-$TIMESTAMP/"
fi

# Infrastructure as Code Scanning with Checkov
if [ -d "terraform" ] && command_exists checkov; then
    echo
    echo "=== Terraform Security Scan ==="
    run_scanner "checkov" \
        "checkov -d terraform/ --framework terraform \
         --output json --output-file $REPORT_DIR/checkov-terraform-$TIMESTAMP.json"
fi

if [ -d "kubernetes" ] && command_exists checkov; then
    echo
    echo "=== Kubernetes Manifest Scan ==="
    run_scanner "checkov" \
        "checkov -d kubernetes/ --framework kubernetes \
         --output json --output-file $REPORT_DIR/checkov-k8s-$TIMESTAMP.json"
fi

# Generate summary report
echo
echo "=== Generating Summary Report ==="

cat > "$REPORT_DIR/summary-$TIMESTAMP.md" <<EOF
# Security Scan Summary

**Date:** $(date)
**Scans Performed:**

EOF

for report in "$REPORT_DIR"/*-$TIMESTAMP.*; do
    if [ -f "$report" ]; then
        filename=$(basename "$report")
        echo "- $filename" >> "$REPORT_DIR/summary-$TIMESTAMP.md"
    fi
done

echo
echo "=== Scan Complete ==="
echo "Reports saved to: $REPORT_DIR"
echo "Summary: $REPORT_DIR/summary-$TIMESTAMP.md"
echo

# Check for critical findings
echo "=== Critical Findings Check ==="
CRITICAL_FOUND=0

# Check Trivy reports for CRITICAL vulnerabilities
for report in "$REPORT_DIR"/trivy-*-$TIMESTAMP.json; do
    if [ -f "$report" ] && grep -q '"Severity":"CRITICAL"' "$report"; then
        echo "[!] CRITICAL vulnerabilities found in $(basename $report)"
        CRITICAL_FOUND=1
    fi
done

if [ $CRITICAL_FOUND -eq 1 ]; then
    echo
    echo "[!] CRITICAL issues detected - review reports immediately"
    exit 1
else
    echo "[✓] No critical issues detected"
    exit 0
fi
