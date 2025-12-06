# Vulnerability Remediation Workflows

Patterns for tracking, managing, and remediating vulnerabilities with SLAs and automation.

## Table of Contents

1. [SLA Tracking](#sla-tracking)
2. [False Positive Management](#false-positive-management)
3. [Automated Remediation](#automated-remediation)
4. [Metrics and Reporting](#metrics-and-reporting)

---

## SLA Tracking

### Priority-Based SLAs

| Priority | SLA | Escalation Path |
|----------|-----|-----------------|
| P0 - Critical | 24 hours | Security team → CISO → CEO |
| P1 - High | 7 days | Team lead → Engineering manager → Director |
| P2 - Medium | 30 days | Sprint planning → Normal backlog |
| P3 - Low | 90 days | Maintenance windows → Technical debt |
| P4 - Info | No SLA | Opportunistic fixes |

### Automated SLA Tracker

```bash
#!/bin/bash
# scripts/sla-tracker.sh

# Track vulnerability remediation SLAs

SCAN_RESULTS="scan-results.json"
KEV_CATALOG="kev.json"
OUTPUT="sla-report.json"

# Download KEV catalog
curl -s -o "$KEV_CATALOG" https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json

# Parse vulnerabilities and calculate SLA
jq --slurpfile kev "$KEV_CATALOG" '
.Results[].Vulnerabilities[] |
{
  cve: .VulnerabilityID,
  severity: .Severity,
  found_date: (.PublishedDate | fromdateiso8601),
  cvss: .CVSS.nvd.V3Score,
  package: .PkgName,
  fixed_version: .FixedVersion,
  in_kev: ([($kev[0].vulnerabilities[] | select(.cveID == .VulnerabilityID))] | length > 0)
} |
# Calculate priority and SLA
if .in_kev then
  .priority = "P0" | .sla_hours = 24
elif .cvss >= 9.0 then
  .priority = "P1" | .sla_hours = 168
elif .cvss >= 7.0 then
  .priority = "P2" | .sla_hours = 720
elif .cvss >= 4.0 then
  .priority = "P3" | .sla_hours = 2160
else
  .priority = "P4" | .sla_hours = null
end |
# Calculate deadline
if .sla_hours then
  .deadline = (.found_date + .sla_hours * 3600) | .overdue = (now > .deadline)
else
  .deadline = null | .overdue = false
end
' "$SCAN_RESULTS" > "$OUTPUT"

# Generate summary
echo "SLA Summary:"
jq -r '
group_by(.priority) |
map({
  priority: .[0].priority,
  count: length,
  overdue: ([.[] | select(.overdue == true)] | length)
}) |
.[]
| "\(.priority): \(.count) total, \(.overdue) overdue"
' "$OUTPUT"
```

## False Positive Management

### Suppression File (.trivyignore)

```
# CVE-2023-12345
# Reason: False positive - vulnerability not applicable to our usage
# Verified by: security-team@example.com
# Date: 2025-12-04
# Review date: 2026-03-04
CVE-2023-12345

# CVE-2023-67890
# Reason: Risk accepted - fix requires major refactor, compensating controls in place
# Approved by: CISO
# Compensating controls: WAF rules, network isolation
# Review date: 2025-06-04
CVE-2023-67890

# Development dependencies (not in production)
CVE-2023-11111  # webpack-dev-server (devDependency only)
```

### False Positive Workflow

```yaml
# .github/workflows/manage-false-positives.yml
name: False Positive Management

on:
  issues:
    types: [labeled]

jobs:
  add-suppression:
    if: github.event.label.name == 'false-positive'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Extract CVE from issue
        id: cve
        run: |
          CVE=$(echo "${{ github.event.issue.title }}" | grep -oP 'CVE-\d{4}-\d+')
          echo "cve=$CVE" >> $GITHUB_OUTPUT

      - name: Add to .trivyignore
        run: |
          echo "" >> .trivyignore
          echo "# ${{ steps.cve.outputs.cve }}" >> .trivyignore
          echo "# Reason: ${{ github.event.issue.body }}" >> .trivyignore
          echo "# Added by: ${{ github.event.issue.user.login }}" >> .trivyignore
          echo "# Date: $(date +%Y-%m-%d)" >> .trivyignore
          echo "${{ steps.cve.outputs.cve }}" >> .trivyignore

      - name: Create PR
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git checkout -b suppress-${{ steps.cve.outputs.cve }}
          git add .trivyignore
          git commit -m "chore: Suppress ${{ steps.cve.outputs.cve }} (false positive)"
          git push origin suppress-${{ steps.cve.outputs.cve }}
          gh pr create --title "Suppress ${{ steps.cve.outputs.cve }}" \
                       --body "Closes #${{ github.event.issue.number }}" \
                       --label "security,false-positive"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Automated Remediation

### Dependency Update Automation

```yaml
name: Automated Vulnerability Remediation

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:

jobs:
  scan-and-remediate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Scan for vulnerabilities
        id: scan
        run: |
          trivy image myapp:latest --format json --output scan.json
          FIXABLE=$(jq '[.Results[].Vulnerabilities[] | select(.Severity == "HIGH" or .Severity == "CRITICAL") | select(.FixedVersion != "")] | length' scan.json)
          echo "fixable_count=$FIXABLE" >> $GITHUB_OUTPUT

      - name: Update dependencies (Node.js)
        if: steps.scan.outputs.fixable_count > 0
        run: |
          npm update
          npm audit fix

      - name: Update dependencies (Python)
        if: steps.scan.outputs.fixable_count > 0
        run: |
          pip install pip-audit
          pip-audit --fix

      - name: Rebuild and re-scan
        if: steps.scan.outputs.fixable_count > 0
        run: |
          docker build -t myapp:remediation .
          trivy image myapp:remediation --format json --output scan-after.json

      - name: Create remediation PR
        if: steps.scan.outputs.fixable_count > 0
        run: |
          git config user.name "security-bot"
          git config user.email "security-bot@example.com"
          git checkout -b security/auto-remediation-$(date +%Y%m%d)
          git add package*.json requirements.txt
          git commit -m "security: Fix ${{ steps.scan.outputs.fixable_count }} vulnerabilities"
          git push origin security/auto-remediation-$(date +%Y%m%d)

          gh pr create \
            --title "Security: Automated vulnerability remediation" \
            --body "Fixes ${{ steps.scan.outputs.fixable_count }} fixable vulnerabilities" \
            --label "security,automated"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Metrics and Reporting

### Vulnerability Dashboard Metrics

```python
#!/usr/bin/env python3
# scripts/vulnerability-metrics.py

import json
import sys
from datetime import datetime

def analyze_scan_results(scan_file):
    with open(scan_file) as f:
        scan_data = json.load(f)

    metrics = {
        'total_vulnerabilities': 0,
        'by_severity': {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0},
        'fixable': 0,
        'unfixable': 0,
        'by_priority': {'P0': 0, 'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0},
        'scan_date': datetime.now().isoformat()
    }

    for result in scan_data.get('Results', []):
        for vuln in result.get('Vulnerabilities', []):
            metrics['total_vulnerabilities'] += 1
            severity = vuln.get('Severity', 'UNKNOWN')
            metrics['by_severity'][severity] = metrics['by_severity'].get(severity, 0) + 1

            if vuln.get('FixedVersion'):
                metrics['fixable'] += 1
            else:
                metrics['unfixable'] += 1

    return metrics

if __name__ == '__main__':
    metrics = analyze_scan_results(sys.argv[1] if len(sys.argv) > 1 else 'scan.json')
    print(json.dumps(metrics, indent=2))
```

### Executive Report Generation

```bash
#!/bin/bash
# scripts/executive-report.sh

SCAN_FILE="scan.json"
REPORT_FILE="security-report.md"

cat > "$REPORT_FILE" << EOF
# Security Vulnerability Report
**Date:** $(date +%Y-%m-%d)
**Scan Date:** $(jq -r '.CreatedAt' "$SCAN_FILE")

## Executive Summary

$(jq -r '
[.Results[].Vulnerabilities[]] |
{
  total: length,
  critical: ([.[] | select(.Severity == "CRITICAL")] | length),
  high: ([.[] | select(.Severity == "HIGH")] | length),
  medium: ([.[] | select(.Severity == "MEDIUM")] | length),
  low: ([.[] | select(.Severity == "LOW")] | length)
} |
"- **Total Vulnerabilities:** \(.total)
- **Critical:** \(.critical)
- **High:** \(.high)
- **Medium:** \(.medium)
- **Low:** \(.low)"
' "$SCAN_FILE")

## Priority Breakdown

$(jq -r '
[.Results[].Vulnerabilities[]] |
group_by(
  if .CVSS.nvd.V3Score >= 9.0 then "P1"
  elif .CVSS.nvd.V3Score >= 7.0 then "P2"
  elif .CVSS.nvd.V3Score >= 4.0 then "P3"
  else "P4"
  end
) |
map({priority: .[0], count: length}) |
.[] |
"- **\(.priority):** \(.count) vulnerabilities"
' "$SCAN_FILE")

## Action Items

### Immediate (P0/P1)
$(jq -r '
[.Results[].Vulnerabilities[] | select(.CVSS.nvd.V3Score >= 9.0)] |
.[] |
"- [ ] Fix \(.VulnerabilityID) in \(.PkgName) (CVSS: \(.CVSS.nvd.V3Score))"
' "$SCAN_FILE" | head -10)

### Upcoming Sprint (P2)
$(jq -r '
[.Results[].Vulnerabilities[] | select(.CVSS.nvd.V3Score >= 7.0 and .CVSS.nvd.V3Score < 9.0)] |
length |
"- \(.) vulnerabilities to address in upcoming sprint"
' "$SCAN_FILE")

---
*Generated automatically by security scanning pipeline*
EOF

echo "Report generated: $REPORT_FILE"
```

See complete scripts in `scripts/` directory.
