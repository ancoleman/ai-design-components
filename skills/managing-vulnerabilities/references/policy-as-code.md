# Policy-as-Code for Vulnerability Management

Implement security policies using OPA (Open Policy Agent) and automated enforcement.

## Table of Contents

1. [OPA Vulnerability Policies](#opa-vulnerability-policies)
2. [Using OPA with Trivy](#using-opa-with-trivy)
3. [Advanced Policies](#advanced-policies)
4. [Policy Testing](#policy-testing)

---

## OPA Vulnerability Policies

### Basic Vulnerability Policy

```rego
package vulnerability

# Deny if any Critical vulnerabilities found
deny[msg] {
    input.Vulnerabilities[_].Severity == "CRITICAL"
    msg := "Critical vulnerabilities detected - build failed"
}

# Deny if High vulnerabilities in production dependencies
deny[msg] {
    vuln := input.Vulnerabilities[_]
    vuln.Severity == "HIGH"
    not contains(vuln.PkgPath, "node_modules/dev")
    msg := sprintf("High vulnerability in production: %v (%v)", [vuln.PkgName, vuln.VulnerabilityID])
}

# Warn if unfixed vulnerabilities
warn[msg] {
    vuln := input.Vulnerabilities[_]
    vuln.FixedVersion == ""
    msg := sprintf("Unfixed vulnerability: %v in %v", [vuln.VulnerabilityID, vuln.PkgName])
}
```

### KEV-Aware Policy

```rego
package vulnerability

import future.keywords.in

# KEV catalog data (load separately or embed)
kev_catalog := {
    "CVE-2021-44228",
    "CVE-2021-45046",
    # ... more KEV CVEs
}

# Deny if vulnerability is in KEV catalog
deny[msg] {
    vuln := input.Vulnerabilities[_]
    vuln.VulnerabilityID in kev_catalog
    msg := sprintf("KEV vulnerability detected: %v - immediate remediation required", [vuln.VulnerabilityID])
}

# Helper function to check KEV
is_kev(cve_id) {
    cve_id in kev_catalog
}
```

### CVSS-Based Policy

```rego
package vulnerability

# Deny based on CVSS score and package location
deny[msg] {
    vuln := input.Vulnerabilities[_]
    cvss_score := vuln.CVSS.nvd.V3Score
    cvss_score >= 7.0
    is_production_dependency(vuln.PkgPath)
    msg := sprintf("CVSS %v vulnerability in production: %v", [cvss_score, vuln.VulnerabilityID])
}

# Helper: Check if production dependency
is_production_dependency(path) {
    not contains(path, "test")
    not contains(path, "dev")
    not contains(path, "node_modules/@types")
}
```

## Using OPA with Trivy

### Scan and Evaluate Policy

```bash
#!/bin/bash
# Scan with Trivy and evaluate OPA policy

IMAGE="myapp:latest"
POLICY_DIR="policies"

# Scan image
trivy image --format json --output scan.json "$IMAGE"

# Evaluate policy
opa eval --data "$POLICY_DIR" --input scan.json \
  'data.vulnerability.deny' --format pretty

# Exit code based on policy
if opa eval --data "$POLICY_DIR" --input scan.json 'data.vulnerability.deny' | grep -q "true"; then
  echo "Policy violations found - build failed"
  exit 1
fi
```

### CI/CD Integration

```yaml
# .github/workflows/policy-check.yml
name: Policy Enforcement

on: [push, pull_request]

jobs:
  security-policy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Scan with Trivy
        run: trivy image --format json --output scan.json myapp:${{ github.sha }}

      - name: Install OPA
        run: |
          curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64
          chmod +x opa

      - name: Evaluate security policy
        run: |
          ./opa eval --data policies/ --input scan.json \
            'data.vulnerability.deny' --format pretty

      - name: Enforce policy
        run: |
          VIOLATIONS=$(./opa eval --data policies/ --input scan.json 'data.vulnerability.deny' --format values)
          if [ -n "$VIOLATIONS" ]; then
            echo "Policy violations:"
            echo "$VIOLATIONS"
            exit 1
          fi
```

## Advanced Policies

### Multi-Tier Policy

```rego
package vulnerability

# P0: Critical + KEV
p0_violations[msg] {
    vuln := input.Vulnerabilities[_]
    vuln.Severity == "CRITICAL"
    is_kev(vuln.VulnerabilityID)
    msg := sprintf("P0: %v (KEV + Critical)", [vuln.VulnerabilityID])
}

# P1: High CVSS or High + EPSS
p1_violations[msg] {
    vuln := input.Vulnerabilities[_]
    cvss := vuln.CVSS.nvd.V3Score
    cvss >= 9.0
    msg := sprintf("P1: %v (CVSS %v)", [vuln.VulnerabilityID, cvss])
}

# Aggregate violations
violations := array.concat(p0_violations, p1_violations)

# Deny if any P0 or P1
deny[msg] {
    count(violations) > 0
    msg := sprintf("Found %v high-priority violations", [count(violations)])
}
```

### Environment-Specific Policies

```rego
package vulnerability

# Get environment from metadata
environment := input.Metadata.Environment

# Production: Zero tolerance
deny[msg] {
    environment == "production"
    input.Vulnerabilities[_].Severity == "CRITICAL"
    msg := "Production: No Critical vulnerabilities allowed"
}

# Staging: Warn only
warn[msg] {
    environment == "staging"
    input.Vulnerabilities[_].Severity == "CRITICAL"
    msg := "Staging: Critical vulnerabilities present (warning only)"
}

# Development: Allow but track
info[msg] {
    environment == "development"
    count(input.Vulnerabilities) > 0
    msg := sprintf("Development: %v vulnerabilities tracked", [count(input.Vulnerabilities)])
}
```

## Policy Testing

### OPA Policy Tests

```rego
package vulnerability_test

import data.vulnerability

# Test: Deny Critical vulnerabilities
test_deny_critical {
    input := {"Vulnerabilities": [{"Severity": "CRITICAL", "VulnerabilityID": "CVE-2023-12345"}]}
    count(vulnerability.deny) > 0
}

# Test: Allow Low vulnerabilities
test_allow_low {
    input := {"Vulnerabilities": [{"Severity": "LOW", "VulnerabilityID": "CVE-2023-99999"}]}
    count(vulnerability.deny) == 0
}

# Test: KEV detection
test_kev_detection {
    input := {"Vulnerabilities": [{"VulnerabilityID": "CVE-2021-44228", "Severity": "CRITICAL"}]}
    count(vulnerability.deny) > 0
}
```

Run tests:
```bash
opa test policies/ -v
```

See complete policies in `examples/opa/` directory.
