# Security Best Practices for GitHub Actions

Comprehensive security guide for GitHub Actions workflows, including secrets management, OIDC authentication, permissions, and vulnerability prevention.

## Table of Contents

1. [Secrets Management](#secrets-management)
2. [OIDC Authentication](#oidc-authentication)
3. [Permissions and Token Scope](#permissions-and-token-scope)
4. [Action Pinning and Supply Chain Security](#action-pinning-and-supply-chain-security)
5. [Pull Request Security](#pull-request-security)
6. [Environment Protection](#environment-protection)
7. [Script Injection Prevention](#script-injection-prevention)
8. [Security Scanning](#security-scanning)

---

## Secrets Management

### Using GitHub Secrets

**Repository Secrets:**

Settings → Secrets and variables → Actions → New repository secret

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: ./deploy.sh
```

**Environment Secrets:**

Settings → Environments → [environment] → Add secret

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # Uses production-specific secrets
    steps:
      - env:
          API_KEY: ${{ secrets.API_KEY }}  # Environment secret overrides repository secret
        run: ./deploy.sh
```

**Organization Secrets:**

Organization settings → Secrets and variables → Actions

Available to all repos in organization (or selected repos).

### Secret Handling Best Practices

**❌ Never Log Secrets:**

```yaml
# BAD - exposes secret in logs
- run: echo "API_KEY=${{ secrets.API_KEY }}"

# BAD - can leak via error messages
- run: curl -H "Authorization: Bearer ${{ secrets.API_KEY }}" https://api.example.com
```

**✅ Safe Secret Usage:**

```yaml
# GOOD - secret not in command output
- env:
    API_KEY: ${{ secrets.API_KEY }}
  run: ./deploy.sh

# GOOD - mask sensitive values
- run: |
    echo "::add-mask::${{ secrets.API_KEY }}"
    # Now safe to reference
```

**Never Commit Secrets:**

`.gitignore`:
```
.env
.env.local
.env.*.local
secrets.yml
credentials.json
*.key
*.pem
```

**Secret Scanning:**

Enable in Settings → Code security and analysis:
- Secret scanning
- Push protection (blocks commits with secrets)

---

## OIDC Authentication

OIDC (OpenID Connect) enables federated identity for cloud providers without storing long-lived credentials.

### AWS OIDC

**Setup (AWS Side):**

1. Create OIDC provider in IAM:
   - Provider URL: `https://token.actions.githubusercontent.com`
   - Audience: `sts.amazonaws.com`

2. Create IAM role with trust policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:OWNER/REPO:*"
        }
      }
    }
  ]
}
```

**Workflow:**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # Required for OIDC
      contents: read
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          aws-region: us-east-1

      - run: |
          aws s3 sync ./dist s3://my-bucket
          aws cloudfront create-invalidation --distribution-id $DIST_ID --paths "/*"
```

### Azure OIDC

**Setup (Azure Side):**

1. Create App Registration
2. Create Federated Credential:
   - Subject identifier: `repo:OWNER/REPO:ref:refs/heads/main`

**Workflow:**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: azure/login@v1
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - run: az webapp deploy --resource-group $RG --name $APP_NAME --src-path ./dist
```

### Google Cloud OIDC

**Setup (GCP Side):**

1. Create Workload Identity Pool
2. Create Workload Identity Provider
3. Grant service account access

**Workflow:**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: 'projects/PROJECT_ID/locations/global/workloadIdentityPools/POOL/providers/PROVIDER'
          service_account: 'SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com'

      - run: gcloud app deploy
```

### OIDC Benefits

**Security:**
- No long-lived credentials stored as secrets
- Automatic credential rotation
- Short-lived tokens (1 hour default)
- Fine-grained access control

**Compliance:**
- Audit trail via cloud provider logs
- No credential exposure risk
- Meets security compliance requirements

---

## Permissions and Token Scope

### GITHUB_TOKEN Permissions

**Default (Permissive - Legacy):**

```yaml
permissions: write-all
```

**Recommended (Least Privilege):**

```yaml
permissions:
  contents: read
  pull-requests: write
```

**Available Permissions:**

| Permission | Read | Write | Description |
|------------|------|-------|-------------|
| `actions` | ✓ | ✓ | GitHub Actions |
| `checks` | ✓ | ✓ | Check runs and suites |
| `contents` | ✓ | ✓ | Repository contents |
| `deployments` | ✓ | ✓ | Deployments |
| `id-token` | - | ✓ | OIDC token (write only) |
| `issues` | ✓ | ✓ | Issues and comments |
| `packages` | ✓ | ✓ | GitHub Packages |
| `pull-requests` | ✓ | ✓ | Pull requests |
| `repository-projects` | ✓ | ✓ | Projects (classic) |
| `security-events` | ✓ | ✓ | Security events |
| `statuses` | ✓ | ✓ | Commit statuses |

### Workflow-Level Permissions

```yaml
name: CI

permissions:
  contents: read
  pull-requests: write

jobs:
  test:
    runs-on: ubuntu-latest
    steps: [...]
```

### Job-Level Permissions

```yaml
jobs:
  test:
    permissions:
      contents: read
    runs-on: ubuntu-latest
    steps: [...]

  deploy:
    permissions:
      contents: write
      deployments: write
    runs-on: ubuntu-latest
    steps: [...]
```

### Disable Permissions

```yaml
permissions: {}  # No permissions
```

---

## Action Pinning and Supply Chain Security

### Pin Actions to Commit SHAs

**❌ Bad (Tags can be moved):**

```yaml
- uses: actions/checkout@v5
- uses: some-org/action@v1.2.3
```

**✅ Good (SHA is immutable):**

```yaml
- uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608  # v5.0.0
- uses: some-org/action@a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0  # v1.2.3
```

**Benefits:**
- Immutable reference (cannot be modified)
- Protection against tag hijacking
- Specific version for reproducibility

### Get Commit SHA for Tag

```bash
# Find SHA for a tag
git ls-remote --tags https://github.com/actions/checkout refs/tags/v5

# Output: abc123...  refs/tags/v5
```

### Dependabot for Actions

**File:** `.github/dependabot.yml`

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "github-actions"
    reviewers:
      - "security-team"
    commit-message:
      prefix: "chore"
      include: "scope"
```

**Benefits:**
- Automated updates for pinned actions
- Creates PRs with SHA updates
- Security vulnerability notifications

### Verify Action Source

**Before Using Third-Party Actions:**

1. **Check Repository:**
   - Stars (>1,000 = widely trusted)
   - Activity (recent commits, maintained)
   - Issues (security concerns, responsiveness)

2. **Review Code:**
   - Read action source code
   - Look for suspicious behavior
   - Check for security advisories

3. **Verify Publisher:**
   - Official organization (GitHub, AWS, Google, etc.)
   - Verified publisher badge
   - Known maintainer

4. **Use Marketplace:**
   - Verified creators
   - Usage statistics
   - Community feedback

---

## Pull Request Security

### pull_request vs pull_request_target

**pull_request (Safe):**

```yaml
on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - run: npm test
```

**Behavior:**
- Runs workflow from PR head (fork)
- No access to secrets
- Safe for untrusted code
- Cannot write to repository

**pull_request_target (Dangerous):**

```yaml
on:
  pull_request_target:
    branches: [main]

jobs:
  comment:
    if: github.event.pull_request.head.repo.full_name == github.repository
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: 'Thanks for the PR!'
            })
```

**Behavior:**
- Runs workflow from base branch (main)
- Has access to secrets
- Can write to repository
- Dangerous with untrusted code

**Security Rule:**

```yaml
# ❌ NEVER do this with pull_request_target
on: pull_request_target
jobs:
  test:
    steps:
      - uses: actions/checkout@v5  # Checks out untrusted PR code
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - run: npm test  # Runs untrusted code with secrets access

# ✅ SAFE: Use pull_request instead
on: pull_request
jobs:
  test:
    steps:
      - uses: actions/checkout@v5
      - run: npm test
```

### Fork PR Permissions

**Repository Settings:**

Settings → Actions → General → Fork pull request workflows

Options:
- **Require approval for first-time contributors** (Recommended)
- **Require approval for all outside collaborators**
- **Run workflows from fork pull requests**

---

## Environment Protection

### Environment Configuration

Settings → Environments → [environment name]

**Protection Rules:**
- **Required reviewers:** 1-6 reviewers must approve
- **Wait timer:** Delay before deployment (0-43,200 minutes)
- **Branch restrictions:** Only specific branches can deploy

**Example:**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://prod.example.com
    steps:
      - run: ./deploy.sh
```

**Benefits:**
- Manual approval gate
- Environment-specific secrets
- Deployment history
- URL tracking

### Deployment Environments

```yaml
jobs:
  deploy-staging:
    environment: staging
    steps:
      - run: ./deploy.sh staging

  deploy-production:
    needs: deploy-staging
    environment: production  # Requires approval
    steps:
      - run: ./deploy.sh production
```

---

## Script Injection Prevention

### Unsafe: Direct Variable Interpolation

**❌ Vulnerable to injection:**

```yaml
- name: Print commit message
  run: echo "${{ github.event.head_commit.message }}"
```

**Attack:** Commit message like `"; rm -rf / #"` could execute arbitrary commands.

### Safe: Use Environment Variables

**✅ Safe approach:**

```yaml
- name: Print commit message
  env:
    COMMIT_MSG: ${{ github.event.head_commit.message }}
  run: echo "$COMMIT_MSG"
```

### Safe: Use Intermediate Steps

**✅ Sanitize input:**

```yaml
- name: Validate input
  env:
    USER_INPUT: ${{ github.event.inputs.version }}
  run: |
    if [[ ! "$USER_INPUT" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
      echo "Invalid version format"
      exit 1
    fi
    echo "VERSION=$USER_INPUT" >> $GITHUB_ENV

- name: Use validated input
  run: echo "Deploying version $VERSION"
```

### Safe: Use Actions for Complex Operations

Instead of inline scripts with user input:

```yaml
# ✅ Use actions/github-script for safe GitHub API calls
- uses: actions/github-script@v7
  with:
    script: |
      const title = context.payload.pull_request.title;
      await github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: `PR Title: ${title}`
      });
```

---

## Security Scanning

### CodeQL (SAST)

```yaml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read
    strategy:
      matrix:
        language: ['javascript', 'python']
    steps:
      - uses: actions/checkout@v5

      - uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}

      - uses: github/codeql-action/autobuild@v3

      - uses: github/codeql-action/analyze@v3
```

### Dependency Scanning

**Dependabot (Built-in):**

Settings → Code security → Dependabot

**npm audit:**

```yaml
- name: Security audit
  run: npm audit --audit-level=high
```

**OWASP Dependency Check:**

```yaml
- name: OWASP Dependency Check
  uses: dependency-check/Dependency-Check_Action@main
  with:
    project: 'my-project'
    path: '.'
    format: 'HTML'
```

### Container Scanning

**Trivy:**

```yaml
- name: Build image
  run: docker build -t myimage:${{ github.sha }} .

- name: Scan image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myimage:${{ github.sha }}
    format: 'sarif'
    output: 'trivy-results.sarif'

- name: Upload results
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: 'trivy-results.sarif'
```

### Secret Scanning

**gitleaks:**

```yaml
- name: Scan for secrets
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Security Checklist

### Workflow Security

- [ ] Pin actions to commit SHAs
- [ ] Use minimal GITHUB_TOKEN permissions
- [ ] Enable Dependabot for action updates
- [ ] Review third-party actions before use
- [ ] Use environment variables for secrets
- [ ] Never log secrets
- [ ] Enable secret scanning
- [ ] Enable push protection

### Authentication

- [ ] Use OIDC for cloud providers (no long-lived credentials)
- [ ] Rotate secrets regularly
- [ ] Use environment-specific secrets
- [ ] Implement environment protection rules

### Pull Requests

- [ ] Use `pull_request` for untrusted code
- [ ] Restrict `pull_request_target` usage
- [ ] Require approval for fork PRs
- [ ] Never checkout untrusted code with secrets

### Deployment

- [ ] Use environment protection for production
- [ ] Require manual approval
- [ ] Implement deployment gates
- [ ] Use separate environments (dev, staging, prod)

### Monitoring

- [ ] Enable security scanning (CodeQL, Dependabot)
- [ ] Monitor workflow logs
- [ ] Review security advisories
- [ ] Audit GITHUB_TOKEN usage

---

For optimization techniques, see `caching-strategies.md`.
