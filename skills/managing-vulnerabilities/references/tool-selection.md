# Vulnerability Scanning Tool Selection Guide

Complete decision frameworks for selecting appropriate security scanning tools across all layers.

## Table of Contents

1. [Container Scanning Tools](#container-scanning-tools)
2. [SAST Tools](#sast-tools)
3. [DAST Tools](#dast-tools)
4. [SCA Tools](#sca-tools)
5. [Secret Scanning Tools](#secret-scanning-tools)
6. [Decision Flowcharts](#decision-flowcharts)
7. [Tool Comparison Matrices](#tool-comparison-matrices)

---

## Container Scanning Tools

### Trivy (Primary Recommendation)

**When to Use:**
- Default choice for most container scanning needs
- Need comprehensive coverage (OS, languages, secrets, misconfig)
- Fast CI/CD pipelines (< 1 minute scans)
- SBOM generation required
- Kubernetes environments (manifest scanning)
- Teams needing all-in-one solution

**Strengths:**
- Comprehensive: OS packages, language libraries, secrets, misconfigurations, licenses
- Fast: Parallel scanning, optimized database
- Zero setup: Single binary, works out-of-the-box
- SBOM native: Generate and consume CycloneDX/SPDX
- Multi-target: Container images, filesystems, Git repos, K8s manifests, Terraform
- Active development: 100+ releases/year, responsive community

**Limitations:**
- Can have false positives (mitigated with .trivyignore)
- Database updates required (automatic but adds startup time)

**Installation:**
```bash
# macOS
brew install trivy

# Linux
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Docker
docker pull aquasec/trivy:latest

# Binary download
wget https://github.com/aquasecurity/trivy/releases/download/v0.48.0/trivy_0.48.0_Linux-64bit.tar.gz
```

**Example Usage:**
```bash
# Basic scan
trivy image alpine:latest

# CI/CD with severity filter
trivy image --severity HIGH,CRITICAL --exit-code 1 myapp:latest

# Generate SBOM
trivy image --format cyclonedx --output sbom.json myapp:latest

# Scan filesystem
trivy fs --scanners vuln,secret,misconfig /path/to/project

# Scan Kubernetes
trivy config deployment.yaml
```

**Best Practices:**
```yaml
# .trivy.yaml
severity: HIGH,CRITICAL
exit-code: 1
ignore-unfixed: true
vuln-type: os,library
skip-dirs:
  - node_modules
  - vendor
  - test
ignorefile: .trivyignore
```

---

### Grype (Alternative - Accuracy Focus)

**When to Use:**
- False positive sensitivity critical
- SBOM-first workflows (pair with Syft)
- Need second opinion validation
- Anchore ecosystem users
- Accuracy more important than comprehensiveness

**Strengths:**
- Minimal false positives: Precise package version matching
- Syft integration: Best-in-class SBOM generation
- Lightweight: No database required
- Fast: Comparable to Trivy
- Clear output: Easy to parse and understand

**Limitations:**
- Requires Syft for SBOM generation (two tools vs. Trivy's one)
- Less comprehensive than Trivy (no misconfig, limited secret scanning)
- Credential disclosure CVE (CVE-2025-65965) - Use v0.104.1+

**Installation:**
```bash
# macOS
brew install grype

# Linux
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

# Docker
docker pull anchore/grype:latest
```

**Example Usage:**
```bash
# Basic scan
grype alpine:latest

# With severity threshold
grype alpine:latest --fail-on high

# Scan SBOM
grype sbom:./sbom.json

# Exclude paths
grype dir:. --exclude './node_modules/**'

# Syft + Grype workflow
syft alpine:latest -o json | grype --fail-on critical
```

**Best Practices:**
```yaml
# .grype.yaml
fail-on-severity: high
output: table
exclude:
  - CVE-2023-12345  # False positive
```

---

### Snyk Container (Commercial)

**When to Use:**
- Budget for commercial tooling
- Developer productivity priority
- Need automated remediation PRs
- Want unified platform (container + SCA + SAST + IaC)
- Require priority intelligence (exploit maturity)

**Strengths:**
- Developer-first UX: Clear fix guidance, base image recommendations
- Automated remediation: PRs for dependency updates
- Priority Intelligence: Risk-based prioritization with exploit data
- IDE integration: Real-time feedback in VS Code, IntelliJ
- Comprehensive: Container, code, dependencies, IaC in one platform

**Limitations:**
- Commercial license required (free tier limited)
- Requires internet connectivity for scanning
- Less customizable than open-source tools

**Example Usage:**
```bash
# Install
npm install -g snyk

# Authenticate
snyk auth

# Scan container
snyk container test alpine:latest

# Monitor in dashboard
snyk container monitor alpine:latest --project-name=myapp

# Automated fixes
snyk container test --file=Dockerfile --exclude-base-image-vulns
```

---

## SAST Tools

### Semgrep (Primary Recommendation)

**When to Use:**
- Need fast, customizable static analysis
- Multi-language projects
- Custom security rules required
- CI/CD integration (< 5 minute scans)
- Open-source preference

**Strengths:**
- Fast: Semantic pattern matching, not full compilation
- Multi-language: 30+ languages supported
- Customizable: Write custom rules in YAML
- Low false positives: Context-aware matching
- CI/CD native: GitHub Actions, GitLab CI, pre-commit hooks

**Limitations:**
- Requires rule customization for best results
- Less comprehensive than commercial tools (fewer rules out-of-box)

**Installation:**
```bash
# macOS
brew install semgrep

# pip
pip install semgrep

# Docker
docker pull returntocorp/semgrep
```

**Example Usage:**
```bash
# Scan with OWASP ruleset
semgrep --config=p/security-audit .

# Multiple rulesets
semgrep --config=p/owasp-top-ten --config=p/secrets .

# CI/CD mode (fail on findings)
semgrep ci

# Custom rules
semgrep --config=rules/custom-security.yaml .
```

---

### Snyk Code (Commercial)

**When to Use:**
- Developer-first experience priority
- IDE integration required
- Need clear fix guidance
- Want AI-powered analysis

**Strengths:**
- IDE plugins: Real-time feedback in editor
- Developer guidance: Clear explanations and fix suggestions
- AI-powered: ML-based vulnerability detection
- Fast: Incremental scanning in IDE

---

### SonarQube (Enterprise)

**When to Use:**
- Enterprise code quality + security
- Need centralized dashboard
- Compliance requirements (audit trails)
- Long-term trend analysis

**Strengths:**
- Comprehensive: Code quality + security
- Quality gates: Enforce thresholds
- Historical analysis: Track technical debt over time
- Enterprise features: LDAP, SSO, audit logs

---

## DAST Tools

### OWASP ZAP (Primary Recommendation)

**When to Use:**
- Need open-source full-featured DAST
- Manual + automated testing required
- API security testing
- Budget constraints

**Strengths:**
- Full-featured: Active scan, passive scan, fuzzing, API testing
- Extensible: Plugins and scripts
- Active community: Well-documented, many resources
- Free: No licensing costs

**Installation:**
```bash
# Docker
docker pull owasp/zap2docker-stable

# macOS
brew install --cask owasp-zap

# Download
# https://www.zaproxy.org/download/
```

**Example Usage:**
```bash
# Baseline scan (non-intrusive)
docker run -v $(pwd):/zap/wrk/:rw -t owasp/zap2docker-stable \
  zap-baseline.py -t https://example.com -r report.html

# Full scan (intrusive)
docker run -v $(pwd):/zap/wrk/:rw -t owasp/zap2docker-stable \
  zap-full-scan.py -t https://example.com -r report.html

# API scan
docker run -v $(pwd):/zap/wrk/:rw -t owasp/zap2docker-stable \
  zap-api-scan.py -t https://api.example.com/openapi.json -f openapi
```

---

### StackHawk (Commercial - CI/CD Native)

**When to Use:**
- Modern CI/CD native DAST required
- Need developer-friendly output
- API-first applications
- Budget for commercial tool

**Strengths:**
- CI/CD native: Built for automated pipelines
- Developer-focused: Clear, actionable results
- API testing: GraphQL, REST, gRPC support
- Fast: Optimized for CI/CD speed

---

## SCA Tools

### Dependabot (GitHub Native)

**When to Use:**
- Using GitHub
- Need automated dependency updates
- Free option required
- Simple dependency scanning sufficient

**Strengths:**
- Native GitHub integration: Zero setup
- Automated PRs: Dependency updates with changelogs
- Free: Included with GitHub
- Security alerts: Integrated with GitHub Security

**Configuration:**
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: "/"
    schedule:
      interval: weekly
    open-pull-requests-limit: 10
```

---

### Renovate (Advanced Automation)

**When to Use:**
- Need advanced customization
- Multi-platform (GitHub, GitLab, Bitbucket, Azure DevOps)
- Complex dependency update strategies
- Monorepo support required

**Strengths:**
- Highly customizable: Granular control over updates
- Multi-platform: Works across Git platforms
- Smart grouping: Group related updates
- Flexible scheduling: Time-based, on-demand, manual approval

**Configuration:**
```json
{
  "extends": ["config:base"],
  "schedule": ["after 10pm every weekday"],
  "packageRules": [
    {
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true
    }
  ]
}
```

---

### Snyk Open Source (Commercial)

**When to Use:**
- Comprehensive commercial solution required
- Need largest vulnerability database
- Want automated fix PRs with testing
- Unified platform preference

**Strengths:**
- Largest database: Most comprehensive vulnerability data
- Fix PRs: Automated updates with CI/CD integration
- Priority Intelligence: Risk-based prioritization
- Unified platform: SCA + SAST + Container + IaC

---

## Secret Scanning Tools

### Gitleaks (Primary Recommendation)

**When to Use:**
- Need fast, open-source secret scanning
- CI/CD integration required
- Custom rule configuration needed
- Pre-commit hooks

**Strengths:**
- Fast: Optimized scanning engine
- Configurable: Custom rules via TOML
- CI/CD ready: Exit codes, JSON output
- Pre-commit support: Prevent secrets before commit

**Installation:**
```bash
# macOS
brew install gitleaks

# Docker
docker pull zricethezav/gitleaks:latest

# Binary
wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz
```

**Example Usage:**
```bash
# Scan current directory
gitleaks detect --source . --verbose

# Scan specific commit range
gitleaks detect --log-opts="--since=2023-01-01"

# Pre-commit hook
gitleaks protect --staged --verbose

# CI/CD mode (exit code on findings)
gitleaks detect --source . --exit-code 1
```

**Configuration:**
```toml
# .gitleaks.toml
title = "Gitleaks Config"

[extend]
useDefault = true

[[rules]]
description = "Custom AWS Key"
regex = '''AKIA[0-9A-Z]{16}'''
tags = ["aws", "key"]
```

---

### TruffleHog (Entropy Detection)

**When to Use:**
- Need entropy-based detection
- Want to find secrets without known patterns
- Historical repository scanning
- High-entropy secret detection

**Strengths:**
- Entropy detection: Find secrets without regex
- Git history: Scan entire repository history
- Verified secrets: Attempts to verify found secrets
- Active scanning: Real-time monitoring

---

### GitGuardian (Commercial)

**When to Use:**
- Need real-time protection
- Want incident response workflow
- Require compliance reporting
- Budget for commercial solution

**Strengths:**
- Real-time monitoring: Instant alerts on secret commits
- Incident response: Guided remediation workflows
- Compliance: Audit trails and reporting
- Developer education: Training and awareness

---

## Decision Flowcharts

### Container Scanning Decision Tree

```
START: Need to scan container image

Q1: Budget and requirements?
  ├─ Open-source + comprehensive → Q2
  ├─ Open-source + accuracy focus → Grype + Syft
  └─ Commercial + developer UX → Snyk Container

Q2: Open-source comprehensive choice
  ├─ Need SBOM + scan in one tool? → YES: Trivy
  ├─ Need minimal false positives? → NO: Grype + Syft
  └─ Default choice → Trivy
```

### SAST Decision Tree

```
START: Need static code analysis

Q1: Budget?
  ├─ Open-source → Q2
  └─ Commercial → Q3

Q2: Open-source SAST
  ├─ Need fast + customizable? → Semgrep
  ├─ Using GitLab? → GitLab SAST
  └─ Default → Semgrep

Q3: Commercial SAST
  ├─ Developer UX priority? → Snyk Code
  ├─ Enterprise quality gates? → SonarQube
  └─ Default → Snyk Code
```

### DAST Decision Tree

```
START: Need dynamic application testing

Q1: Budget?
  ├─ Open-source → OWASP ZAP
  └─ Commercial → Q2

Q2: Commercial DAST needs
  ├─ CI/CD native required? → StackHawk
  ├─ Manual + automated? → Burp Suite
  └─ Default → StackHawk
```

---

## Tool Comparison Matrices

### Container Scanning Comparison

| Feature | Trivy | Grype | Snyk Container |
|---------|-------|-------|----------------|
| **License** | Apache 2.0 | Apache 2.0 | Commercial |
| **Speed** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Accuracy** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **OS Packages** | Yes | Yes | Yes |
| **Language Packages** | Yes | Yes | Yes |
| **Secrets** | Yes | Limited | Yes |
| **Misconfig** | Yes | No | Yes |
| **SBOM Generation** | CycloneDX, SPDX | Via Syft | Yes |
| **SBOM Scanning** | Yes | Yes | Yes |
| **CI/CD Integration** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **False Positives** | Moderate | Low | Low |
| **Setup Complexity** | Low | Low | Low |
| **Best For** | Most projects | Accuracy focus | Enterprise |

### SAST Comparison

| Feature | Semgrep | Snyk Code | SonarQube |
|---------|---------|-----------|-----------|
| **License** | LGPL 2.1 | Commercial | Commercial |
| **Speed** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Languages** | 30+ | 10+ | 25+ |
| **Custom Rules** | Yes (YAML) | No | Limited |
| **IDE Integration** | Yes | Yes | Yes |
| **CI/CD Ready** | Yes | Yes | Yes |
| **False Positives** | Low | Low | Moderate |
| **Fix Guidance** | Basic | Excellent | Good |
| **Best For** | Fast + customizable | Developer UX | Enterprise quality |

### Secret Scanning Comparison

| Feature | Gitleaks | TruffleHog | GitGuardian |
|---------|----------|------------|-------------|
| **License** | MIT | AGPL-3.0 | Commercial |
| **Detection** | Regex | Regex + Entropy | Regex + ML |
| **Speed** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Git History** | Yes | Yes | Yes |
| **Pre-commit** | Yes | Yes | Yes |
| **Verification** | No | Yes | Yes |
| **Real-time** | No | No | Yes |
| **Incident Response** | No | No | Yes |
| **Best For** | CI/CD | Entropy detection | Enterprise |

---

## Recommended Combinations

### Startup/Small Team
```
Container: Trivy (comprehensive, free)
SAST: Semgrep (fast, customizable)
DAST: OWASP ZAP (full-featured, free)
SCA: Dependabot (GitHub native, free)
Secrets: Gitleaks (fast, configurable)

Cost: $0
Setup: Low complexity
```

### Mid-Size Company
```
Container: Trivy + Snyk Container (comprehensive + UX)
SAST: Semgrep + Snyk Code (coverage + developer UX)
DAST: StackHawk (CI/CD native)
SCA: Renovate (advanced automation)
Secrets: GitGuardian (real-time protection)

Cost: Moderate
Setup: Moderate complexity
```

### Enterprise
```
Container: Snyk Container (unified platform)
SAST: SonarQube (quality gates + compliance)
DAST: Burp Suite Enterprise
SCA: Snyk Open Source (comprehensive)
Secrets: GitGuardian Enterprise (incident response)

Cost: High
Setup: High complexity
Benefits: Unified dashboards, compliance, support
```

---

## Selection Checklist

Use this checklist to select appropriate tools:

**Requirements:**
- [ ] Budget: Open-source, commercial, enterprise?
- [ ] Languages: Which languages need scanning?
- [ ] CI/CD platform: GitHub Actions, GitLab CI, Jenkins, other?
- [ ] Team size: How many developers?
- [ ] Security maturity: Beginning, intermediate, advanced?
- [ ] Compliance: SOC2, ISO 27001, PCI-DSS requirements?

**Evaluation Criteria:**
- [ ] Speed: CI/CD pipeline impact (target < 5 minutes)
- [ ] Accuracy: False positive tolerance?
- [ ] Coverage: OS, languages, secrets, misconfig?
- [ ] Integration: Existing tools and workflows?
- [ ] Maintainability: Active development, community support?
- [ ] Scalability: Can handle codebase growth?

**Decision:**
- Container scanning: ________________
- SAST: ________________
- DAST: ________________
- SCA: ________________
- Secret scanning: ________________
