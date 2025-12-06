# Secret Scanning and Remediation

Comprehensive guide to detecting, preventing, and remediating leaked secrets using Gitleaks and other tools.

## Table of Contents

1. [Why Scan for Secrets](#why-scan-for-secrets)
2. [Gitleaks](#gitleaks)
3. [Pre-Commit Hooks](#pre-commit-hooks)
4. [CI/CD Integration](#cicd-integration)
5. [Remediation Workflow](#remediation-workflow)
6. [Alternative Tools](#alternative-tools)

## Why Scan for Secrets

**The Problem:**
- 10M+ secrets exposed on GitHub in 2024 (GitGuardian)
- Average breach cost: $4.45M (IBM 2025)
- 63% of breaches from leaked credentials (Verizon DBIR)
- 95% preventable with secret scanning

**Common Leak Sources:**
- Git commits (hardcoded passwords, API keys)
- Environment files (.env, config.json)
- Configuration files (application.yml, settings.py)
- CI/CD logs (exposed secrets in build output)
- Docker images (secrets baked into layers)

## Gitleaks

High-performance secret scanner with customizable rules.

### Installation

```bash
# macOS
brew install gitleaks

# Linux
curl -sSfL https://raw.githubusercontent.com/gitleaks/gitleaks/master/scripts/install.sh | sh

# Docker
docker pull ghcr.io/gitleaks/gitleaks:latest
```

### Basic Usage

```bash
# Scan current repository
gitleaks detect --verbose

# Scan specific directory
gitleaks detect --source /path/to/repo --verbose

# Scan Git history
gitleaks detect --log-opts "--all" --verbose

# Protect mode (scan uncommitted changes)
gitleaks protect --staged --verbose

# Generate report
gitleaks detect --report-format json --report-path gitleaks-report.json
```

### Configuration (.gitleaks.toml)

```toml
title = "Gitleaks Configuration"

[extend]
useDefault = true

[[rules]]
id = "generic-api-key"
description = "Generic API Key"
regex = '''(?i)(api[_-]?key|apikey)['"` ]*[:=]['"` ]*[a-zA-Z0-9]{20,}'''
tags = ["key", "API"]

[[rules]]
id = "aws-access-key"
description = "AWS Access Key"
regex = '''AKIA[0-9A-Z]{16}'''
tags = ["AWS", "key"]

[[rules]]
id = "private-key"
description = "Private Key"
regex = '''-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----'''
tags = ["key", "private"]

[[rules]]
id = "jwt"
description = "JSON Web Token"
regex = '''eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}'''
tags = ["JWT"]

[allowlist]
description = "Allowlist for test files and examples"
paths = [
  '''.*/test/.*''',
  '''.*/examples/.*''',
  '''.*_test\.go''',
  '''.*\.md'''
]
regexes = [
  '''sk_test_''',  # Stripe test keys
  '''pk_test_''',  # Stripe test keys
  '''EXAMPLE_API_KEY''',  # Placeholder examples
]
```

### Exit Codes

```bash
gitleaks detect
echo $?

# 0: No secrets found
# 1: Secrets detected
# 2: Error occurred
```

## Pre-Commit Hooks

### Install pre-commit

```bash
# Install pre-commit framework
pip install pre-commit

# Or via Homebrew
brew install pre-commit
```

### .pre-commit-config.yaml

```yaml
repos:
- repo: https://github.com/gitleaks/gitleaks
  rev: v8.18.1
  hooks:
  - id: gitleaks
    name: Gitleaks
    description: Detect secrets in staged files
    entry: gitleaks protect --staged --redact
    language: system
    pass_filenames: false
```

### Manual Hook (.git/hooks/pre-commit)

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running Gitleaks secret scan..."

# Run Gitleaks on staged files
gitleaks protect --staged --verbose --redact

if [ $? -ne 0 ]; then
  echo ""
  echo "❌ Secret detected! Commit blocked."
  echo "To fix:"
  echo "  1. Remove the secret from your code"
  echo "  2. Store it in Vault: vault kv put secret/myapp/config api_key=<YOUR_KEY>"
  echo "  3. Reference it in code: vault.read('secret/data/myapp/config')"
  echo ""
  echo "To bypass (NOT recommended): git commit --no-verify"
  exit 1
fi

echo "✅ No secrets detected. Proceeding with commit."
exit 0
```

**Install hook:**
```bash
chmod +x .git/hooks/pre-commit
```

### Husky (for Node.js projects)

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "gitleaks protect --staged --verbose"
    }
  }
}
```

```bash
npx husky install
npx husky add .husky/pre-commit "gitleaks protect --staged --verbose"
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/secret-scan.yml
name: Secret Scanning

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  gitleaks:
    name: Gitleaks Secret Scan
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0  # Full history for comprehensive scan

    - name: Run Gitleaks
      uses: gitleaks/gitleaks-action@v2
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}  # For commercial use

    - name: Upload results (if secrets found)
      if: failure()
      uses: actions/upload-artifact@v4
      with:
        name: gitleaks-report
        path: gitleaks-report.sarif
```

### GitLab CI

```yaml
# .gitlab-ci.yml
gitleaks:
  stage: test
  image: ghcr.io/gitleaks/gitleaks:latest
  script:
  - gitleaks detect --verbose --report-format json --report-path gitleaks-report.json
  artifacts:
    when: on_failure
    paths:
    - gitleaks-report.json
  allow_failure: false
```

### Jenkins

```groovy
pipeline {
  agent any
  stages {
    stage('Secret Scan') {
      steps {
        sh 'gitleaks detect --verbose --report-format json --report-path gitleaks-report.json'
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'gitleaks-report.json', allowEmptyArchive: true
    }
  }
}
```

### CircleCI

```yaml
# .circleci/config.yml
version: 2.1

jobs:
  gitleaks:
    docker:
    - image: ghcr.io/gitleaks/gitleaks:latest
    steps:
    - checkout
    - run:
        name: Run Gitleaks
        command: gitleaks detect --verbose
    - store_artifacts:
        path: gitleaks-report.json

workflows:
  version: 2
  build:
    jobs:
    - gitleaks
```

## Remediation Workflow

### When a Secret is Leaked

**Immediate Actions (within 1 hour):**

1. **Rotate the Exposed Secret**
```bash
# PRIORITY 1: Create new secret in Vault
vault kv put secret/api-keys/stripe \
  key=sk_live_NEW_KEY_AFTER_LEAK \
  rotated_reason="Leaked to Git on 2025-12-03" \
  previous_key=sk_live_OLD_KEY_LEAKED
```

2. **Revoke at Provider**
```bash
# Stripe: Dashboard → API Keys → Revoke
# AWS: IAM → Delete access key
# GitHub: Settings → Developer settings → Revoke token
```

3. **Update Applications**
```bash
# Update all environments immediately
kubectl set env deployment/api-service -n staging STRIPE_API_KEY=sk_live_NEW_KEY_AFTER_LEAK
kubectl set env deployment/api-service -n production STRIPE_API_KEY=sk_live_NEW_KEY_AFTER_LEAK
```

**Git History Cleanup (within 24 hours):**

4. **Remove from Git History (BFG Repo-Cleaner)**
```bash
# Install BFG
brew install bfg

# Clone fresh copy
git clone --mirror https://github.com/org/repo.git repo.git
cd repo.git

# Create file with secrets to remove
cat > secrets.txt <<EOF
sk_live_OLD_KEY_LEAKED
AKIA1234567890ABCDEF
-----BEGIN RSA PRIVATE KEY-----
EOF

# Remove secrets
bfg --replace-text secrets.txt .

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (CAUTION: Coordinate with team)
git push --force --all
git push --force --tags
```

**Alternative: filter-repo**
```bash
pip install git-filter-repo

# Remove specific file
git filter-repo --invert-paths --path config/secrets.json

# Remove specific pattern
echo "sk_live_" > secrets-pattern.txt
git filter-repo --replace-text secrets-pattern.txt
```

5. **Audit Access**
```bash
# Check Vault audit logs
vault audit list

# Read audit log
cat /vault/logs/audit.log | jq 'select(.request.path == "secret/data/api-keys/stripe")'

# GitHub: Who cloned during leak window?
# Check repository Insights → Traffic → Git clones
```

6. **Document Incident**
```markdown
# Incident Report: Secret Leak 2025-12-03

## Summary
- **Date**: 2025-12-03 10:15 UTC
- **Secret**: Stripe API key (sk_live_OLD_KEY_LEAKED)
- **Exposure**: Committed to main branch, pushed to GitHub
- **Discovered**: Gitleaks CI/CD scan
- **Resolved**: Secret rotated within 30 minutes

## Timeline
- 10:15: Secret committed (commit abc123)
- 10:20: CI/CD pipeline detected leak, blocked merge
- 10:25: Secret rotated in Vault
- 10:30: Old key revoked at Stripe
- 11:00: Git history rewritten (BFG)
- 11:15: Force push completed

## Root Cause
- Developer accidentally committed .env file
- Pre-commit hook not installed locally

## Prevention
- [ ] Enforce pre-commit hooks (CI check)
- [ ] Add .env to .gitignore (template)
- [ ] Developer training on secret management
- [ ] Mandatory .gitleaks.toml in all repos

## Impact
- No unauthorized API usage detected
- No customer data accessed
- Leak window: 15 minutes (before rotation)
```

### False Positive Handling

**Allowlist in .gitleaks.toml:**
```toml
[allowlist]
description = "Allowlist for test files and examples"

# Ignore test files
paths = [
  '''.*/test/.*''',
  '''.*/examples/.*''',
  '''.*\.md''',  # Documentation
]

# Ignore test keys and placeholders
regexes = [
  '''sk_test_[a-zA-Z0-9]{24}''',  # Stripe test keys
  '''pk_test_[a-zA-Z0-9]{24}''',
  '''EXAMPLE_[A-Z_]+''',  # Placeholders
  '''YOUR_API_KEY_HERE''',
]

# Ignore specific commits (emergency override)
commits = [
  "abc123def456",  # Migration commit with test data
]
```

**Inline Ignore:**
```python
# gitleaks:allow
api_key = "sk_test_THIS_IS_A_TEST_KEY_FOR_EXAMPLES"
```

## Alternative Tools

### TruffleHog

Deep Git history scanning with entropy detection.

```bash
# Installation
pip install truffleHog

# Scan repository
trufflehog git https://github.com/org/repo.git

# Scan since specific commit
trufflehog git https://github.com/org/repo.git --since-commit abc123

# JSON output
trufflehog git https://github.com/org/repo.git --json
```

### detect-secrets (Yelp)

Baseline-based scanning for Python projects.

```bash
# Installation
pip install detect-secrets

# Create baseline
detect-secrets scan > .secrets.baseline

# Audit baseline (interactive)
detect-secrets audit .secrets.baseline

# Scan for new secrets
detect-secrets scan --baseline .secrets.baseline
```

### git-secrets (AWS)

Prevents committing AWS credentials.

```bash
# Installation
brew install git-secrets

# Install hooks
git secrets --install
git secrets --register-aws

# Scan repository
git secrets --scan
```

### Comparison Matrix

| Tool | Performance | Accuracy | Custom Rules | CI/CD | License |
|------|-------------|----------|--------------|-------|---------|
| **Gitleaks** | Excellent | High | Yes (regex) | Easy | MIT |
| **TruffleHog** | Good | High (entropy) | Limited | Moderate | GPL-3.0 |
| **detect-secrets** | Moderate | Moderate | Yes (plugins) | Easy | Apache-2.0 |
| **git-secrets** | Good | Moderate | Yes (regex) | Easy | Apache-2.0 |

**Recommendation:** Use Gitleaks for most projects (fast, accurate, easy CI/CD integration).

## Best Practices

1. **Layer Defenses**
   - Pre-commit hooks (local)
   - CI/CD scanning (remote)
   - Periodic full repository scans

2. **Rotate Immediately**
   - Assume leaked = compromised
   - Rotate within 1 hour
   - Revoke at provider

3. **Educate Developers**
   - Secret management training
   - Code review checklist
   - Security champions

4. **Monitor Audit Logs**
   - Track secret access patterns
   - Alert on unusual activity
   - Regular audit reviews

5. **Automate Response**
   - Auto-rotate on detection
   - Auto-revoke leaked credentials
   - Incident tickets
