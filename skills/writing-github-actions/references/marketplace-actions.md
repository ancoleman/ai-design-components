# GitHub Marketplace Actions

Recommended actions from GitHub Marketplace for common workflows.

## Official GitHub Actions

**actions/checkout@v5**
- Repository: https://github.com/actions/checkout
- Purpose: Clone repository
- Trust: Official GitHub
- Pin to: `8ade135a41bc03ea155e62e844d188df1ea18608`

**actions/setup-node@v4**
- Repository: https://github.com/actions/setup-node
- Purpose: Setup Node.js with caching
- Trust: Official GitHub

**actions/cache@v4**
- Repository: https://github.com/actions/cache
- Purpose: Cache dependencies and build outputs
- Trust: Official GitHub

**actions/upload-artifact@v4 / download-artifact@v5**
- Repository: https://github.com/actions/upload-artifact
- Purpose: Share data between jobs
- Trust: Official GitHub

## Cloud Provider Actions

**aws-actions/configure-aws-credentials@v4**
- Purpose: Configure AWS credentials via OIDC
- Trust: Official AWS

**google-github-actions/auth@v2**
- Purpose: Authenticate to GCP via OIDC
- Trust: Official Google

**azure/login@v1**
- Purpose: Azure login via OIDC
- Trust: Official Microsoft

## Docker Actions

**docker/build-push-action@v5**
- Purpose: Build and push Docker images
- Trust: Official Docker

**docker/setup-buildx-action@v3**
- Purpose: Setup Docker Buildx
- Trust: Official Docker

## Security Actions

**github/codeql-action**
- Purpose: Code security scanning (SAST)
- Trust: Official GitHub

**aquasecurity/trivy-action**
- Purpose: Container and dependency scanning
- Trust: Widely trusted (5K+ stars)

**gitleaks/gitleaks-action@v2**
- Purpose: Secret scanning
- Trust: Widely trusted (3K+ stars)

## Utility Actions

**peter-evans/create-pull-request@v5**
- Purpose: Create PRs from workflow changes
- Trust: Widely trusted (6K+ stars)

**dorny/paths-filter@v2**
- Purpose: Detect changed paths (monorepo)
- Trust: Widely trusted (2K+ stars)

## Action Verification

Before using third-party actions:
1. Check repository stars (>1,000 = widely trusted)
2. Review source code
3. Verify publisher identity
4. Pin to commit SHA
5. Enable Dependabot for updates

For security best practices, see `security-practices.md`.
