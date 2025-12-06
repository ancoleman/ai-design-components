---
sidebar_position: 3
title: Vulnerability Management
description: Multi-layer security scanning, SBOM generation, and risk-based vulnerability prioritization
tags: [security, vulnerabilities, scanning, sbom, trivy, cvss, epss]
---

# Vulnerability Management

Implement comprehensive vulnerability detection and remediation workflows across containers, source code, dependencies, and running applications.

## When to Use

Invoke this skill when:
- Building security scanning into CI/CD pipelines
- Generating Software Bills of Materials (SBOMs) for compliance
- Prioritizing vulnerability remediation using risk-based approaches
- Implementing security gates (fail builds on critical vulnerabilities)
- Scanning container images before deployment
- Detecting secrets, misconfigurations, or code vulnerabilities
- Establishing DevSecOps practices and automation
- Meeting regulatory requirements (SBOM mandates, Executive Order 14028)

## Key Features

**Multi-Layer Scanning Strategy:**
- **Container Image Scanning**: Trivy (comprehensive), Grype (accuracy-focused)
- **SAST**: Semgrep (fast, semantic), Snyk Code (developer-first)
- **DAST**: OWASP ZAP (open-source), StackHawk (CI/CD native)
- **SCA**: Dependabot (GitHub native), Renovate (advanced)
- **Secret Scanning**: Gitleaks (fast, configurable), TruffleHog (entropy detection)

**SBOM Generation:**
- **CycloneDX**: Security-focused, OWASP-maintained (recommended for DevSecOps)
- **SPDX**: License compliance focus, ISO standard (recommended for legal/compliance)
- Fast SBOM scanning: Generate once, scan repeatedly without re-scanning images

**Risk-Based Prioritization:**
- **CVSS**: Base severity score (0-10)
- **EPSS**: Exploitation probability from FIRST.org (0-1)
- **KEV**: CISA Known Exploited Vulnerabilities catalog
- **Priority Tiers**: P0 (24h SLA), P1 (7d), P2 (30d), P3 (90d), P4 (no SLA)

**CI/CD Integration:**
- Pre-commit hooks for secrets and SAST
- PR checks with no Critical/High threshold
- Build-time container scanning with SBOM generation
- Pre-deployment DAST in staging
- Production runtime continuous scanning

## Quick Start

```bash
# Container Scanning with Trivy
trivy image --severity HIGH,CRITICAL alpine:latest

# Generate SBOM (CycloneDX)
trivy image --format cyclonedx --output sbom.json myapp:latest

# Scan SBOM (faster than re-scanning image)
trivy sbom sbom.json --severity HIGH,CRITICAL

# Fail build on Critical vulnerabilities (CI/CD)
trivy image --exit-code 1 --severity CRITICAL myapp:latest

# Ignore unfixed vulnerabilities
trivy image --ignore-unfixed --severity HIGH,CRITICAL myapp:latest
```

**GitHub Actions Multi-Stage Scan:**

```yaml
name: Security Scan Pipeline

on: [push, pull_request]

jobs:
  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          extra_args: --only-verified

  container:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t myapp:${{ github.sha }} .

      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: sarif
          output: trivy-results.sarif
          severity: HIGH,CRITICAL
          exit-code: 1

      - name: Generate SBOM
        run: |
          trivy image --format cyclonedx \
            --output sbom.json myapp:${{ github.sha }}

      - uses: actions/upload-artifact@v3
        with:
          name: sbom
          path: sbom.json
```

**Risk-Based Prioritization Example (Log4Shell):**

```
CVE-2021-44228 (Log4Shell)
CVSS: 10.0
EPSS: 0.975 (97.5% exploitation probability)
KEV: Yes (CISA catalog)
Asset: Critical (payment API)
Exposure: Internet-facing

Priority Score = (10 × 0.3) + (97.5 × 0.3) + 50 + (1 × 0.2) + (1 × 0.2) = 82.65
Result: P0 - Critical (24-hour SLA)
```

## Related Skills

- [Security Hardening](./security-hardening.md) - Apply remediation guidance from scan results
- [Implementing Compliance](./implementing-compliance.md) - Generate SBOMs for audit compliance
- [Security Architecture](./architecting-security.md) - Integrate scanning into security architecture
- [SIEM Logging](./siem-logging.md) - Monitor vulnerability remediation activities

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/managing-vulnerabilities)
- [Master Plan](../../master-plans/security/managing-vulnerabilities.md)
