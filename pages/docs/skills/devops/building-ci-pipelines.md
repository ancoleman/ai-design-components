---
sidebar_position: 2
title: Building CI Pipelines
description: Construct secure, efficient CI/CD pipelines with supply chain security (SLSA), monorepo optimization, and caching
tags: [devops, ci-cd, github-actions, gitlab-ci, slsa, security]
---

# Building CI Pipelines

Construct secure, efficient CI/CD pipelines with supply chain security (SLSA), monorepo optimization, caching strategies, and parallelization patterns for GitHub Actions, GitLab CI, and Argo Workflows.

## When to Use

Invoke this skill when:
- Setting up continuous integration for new projects
- Implementing automated testing workflows
- Building container images with security provenance
- Optimizing slow CI pipelines (especially monorepos)
- Implementing SLSA supply chain security
- Configuring multi-platform builds
- Setting up GitOps automation
- Migrating from legacy CI systems

## Key Features

- **SLSA Level 3 Provenance**: Supply chain security with cryptographic verification
- **Monorepo Optimization**: 60-80% CI time reduction with affected detection (Turborepo, Nx)
- **OIDC Federation**: No stored credentials, 1-hour lifetime, full audit trail
- **Multi-Layer Caching**: 70-90% build time reduction with dependency and build output caching
- **Security Scanning**: Gitleaks (secrets), Snyk (vulnerabilities), SBOM generation
- **Parallelization**: Matrix strategies and test sharding for faster feedback

## Platform Selection

| Use Case | Platform | When to Choose |
|----------|----------|----------------|
| GitHub-hosted | GitHub Actions | SLSA native, 10K+ actions, OIDC built-in |
| GitLab-hosted | GitLab CI | Parent-child pipelines, built-in security |
| Kubernetes | Argo Workflows | DAG-based, event-driven |
| Legacy | Jenkins | Migrate when possible |

## Quick Start: Basic CI (Lint → Test → Build)

```yaml
# GitHub Actions
name: CI
on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run lint

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run build
```

## Pattern: Multi-Platform Matrix

```yaml
test:
  runs-on: ${{ matrix.os }}
  strategy:
    matrix:
      os: [ubuntu-latest, windows-latest, macos-latest]
      node-version: [18, 20, 22]
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
    - run: npm test
```

**Result**: 9 jobs (3 OS × 3 versions) in parallel: 5 min vs 45 min sequential.

## Pattern: Monorepo Affected (Turborepo)

```yaml
build:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0  # Required for affected detection

    - uses: actions/setup-node@v4
      with:
        node-version: 20

    - name: Build affected
      run: npx turbo run build --filter='...[origin/main]'
      env:
        TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
        TURBO_TEAM: ${{ vars.TURBO_TEAM }}
```

**Result**: 60-80% CI time reduction for monorepos.

## Pattern: SLSA Level 3 Provenance

```yaml
name: SLSA Build
on:
  push:
    tags: ['v*']

permissions:
  id-token: write
  contents: read
  packages: write

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@v4
      - name: Build container
        id: build
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}

  provenance:
    needs: build
    permissions:
      id-token: write
      actions: read
      packages: write
    uses: slsa-framework/slsa-github-generator/.github/workflows/generator_container_slsa3.yml@v1.10.0
    with:
      image: ghcr.io/${{ github.repository }}
      digest: ${{ needs.build.outputs.digest }}
```

**Verification**:
```bash
cosign verify-attestation --type slsaprovenance \
  --certificate-identity-regexp "^https://github.com/slsa-framework" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  ghcr.io/myorg/myapp@sha256:abcd...
```

## Pattern: OIDC Federation (No Credentials)

```yaml
deploy:
  runs-on: ubuntu-latest
  permissions:
    id-token: write
    contents: read
  steps:
    - uses: actions/checkout@v4

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
        aws-region: us-east-1

    - name: Deploy
      run: aws s3 sync ./dist s3://my-bucket
```

**Benefits**: No stored credentials, 1-hour lifetime, full audit trail.

## Caching Strategies

### Automatic Dependency Caching

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'npm'  # Auto-caches ~/.npm
- run: npm ci
```

**Supported**: npm, yarn, pnpm, pip, poetry, cargo, go

### Multi-Layer Caching (Nx)

```yaml
- name: Nx Cloud (build outputs)
  run: npx nx affected -t build
  env:
    NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}

- name: Vite Cache
  uses: actions/cache@v4
  with:
    path: '**/node_modules/.vite'
    key: vite-${{ hashFiles('package-lock.json') }}
```

**Result**: 70-90% build time reduction.

## Security Best Practices

**DO:**
- Use OIDC instead of long-lived credentials
- Pin actions to commit SHA: `actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11`
- Restrict permissions: `permissions: { contents: read }`
- Scan secrets (Gitleaks) on every commit
- Generate SLSA provenance for releases

**DON'T:**
- Expose secrets in logs
- Use `pull_request_target` without validation
- Trust unverified third-party actions

## Language Examples

### Python
```yaml
test:
  strategy:
    matrix:
      python-version: ['3.10', '3.11', '3.12']
  steps:
    - uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    - run: pipx install poetry
    - run: poetry install
    - run: poetry run pytest --cov
```

### Rust
```yaml
test:
  strategy:
    matrix:
      os: [ubuntu-latest, windows-latest, macos-latest]
      rust: [stable, nightly]
  steps:
    - uses: dtolnay/rust-toolchain@master
      with:
        toolchain: ${{ matrix.rust }}
        components: rustfmt, clippy
    - uses: Swatinem/rust-cache@v2
    - run: cargo test
```

### Go
```yaml
test:
  steps:
    - uses: actions/setup-go@v5
      with:
        go-version: '1.23'
        cache: true
    - run: go test -v -race -coverprofile=coverage.txt ./...
```

## Parallelization Patterns

### Test Sharding

```yaml
test:
  strategy:
    matrix:
      shard: [1, 2, 3, 4]
  steps:
    - run: npm test -- --shard=${{ matrix.shard }}/4
```

**Result**: 20min test suite → 5min (4x speedup).

## Debugging

```yaml
# Enable debug logging
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true

# SSH into runner
- uses: mxschmitt/action-tmate@v3
```

## Related Skills

- [Testing Strategies](./testing-strategies) - Test execution strategies integrated into CI/CD
- [Implementing GitOps](./implementing-gitops) - Deployment automation with ArgoCD/Flux
- [Writing Dockerfiles](./writing-dockerfiles) - Container image builds in CI pipelines
- [Platform Engineering](./platform-engineering) - CI/CD integration in developer platforms

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/building-ci-pipelines)
- [GitHub Actions Patterns](https://github.com/ancoleman/ai-design-components/tree/main/skills/building-ci-pipelines/references/github-actions-patterns.md)
- [SLSA Security Framework](https://github.com/ancoleman/ai-design-components/tree/main/skills/building-ci-pipelines/references/slsa-security-framework.md)
- [Working Examples](https://github.com/ancoleman/ai-design-components/tree/main/skills/building-ci-pipelines/examples)
