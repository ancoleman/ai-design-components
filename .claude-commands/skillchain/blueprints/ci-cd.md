# CI/CD Pipeline Blueprint

**Version:** 1.0.0
**Last Updated:** 2025-12-06
**Category:** DevOps

---

## Overview

Pre-configured skill chain optimized for building continuous integration and continuous deployment pipelines. This blueprint provides production-ready defaults for the most common CI/CD patterns, automating testing, building, and deployment workflows while minimizing configuration complexity and maximizing reliability.

---

## Trigger Keywords

**Primary (high confidence):**
- ci/cd
- pipeline
- continuous integration
- continuous deployment
- github actions
- gitlab ci
- jenkins
- automation workflow

**Secondary (medium confidence):**
- build automation
- deployment pipeline
- test automation
- release automation
- devops workflow
- build and deploy

**Example goals that match:**
- "ci/cd pipeline with automated testing"
- "github actions workflow for deployment"
- "automated pipeline for node.js app"
- "continuous deployment to kubernetes"
- "build pipeline with docker containers"
- "automated testing and deployment workflow"

---

## Skill Chain (Pre-configured)

This blueprint invokes 6 skills in the following order:

```
1. building-ci-pipelines         (core - pipeline configuration)
2. testing-strategies            (automated testing integration)
3. managing-containers           (container builds and registry)
4. implementing-gitops           (deployment automation)
5. hardening-security            (secret scanning, SAST/DAST)
6. implementing-observability    (pipeline monitoring and alerts)
```

**Total estimated time:** 30-40 minutes
**Total estimated questions:** 15-20 questions (or 3 with blueprint defaults)

---

## Pre-configured Defaults

### 1. building-ci-pipelines
```yaml
platform: "github-actions"
  # GitHub Actions: Native GitHub integration, free for public repos
  # YAML-based configuration in .github/workflows/
  # Extensive marketplace for pre-built actions
  # Built-in secrets management and environment protection

pipeline_stages: ["lint", "test", "build", "deploy"]
  # lint: Code quality checks (ESLint, Prettier, etc.)
  # test: Unit, integration, and E2E tests
  # build: Compile, bundle, and create artifacts
  # deploy: Deploy to target environments

trigger_events: ["push", "pull_request", "release"]
  # push: Trigger on commits to main/develop branches
  # pull_request: Validate PRs before merge
  # release: Deploy on tagged releases

concurrency_control: true
  # Cancel in-progress runs when new commits pushed
  # Prevents wasted compute on outdated code
  # Uses job concurrency groups

cache_strategy: "dependencies"
  # Cache npm/pip/maven dependencies between runs
  # Restore from cache on cache hit
  # Reduces build time by 40-60%
  # Cache key: OS + package-lock.json hash

matrix_testing: true
  # Test across multiple versions
  # Node.js: [18.x, 20.x, 22.x]
  # OS: [ubuntu-latest, macos-latest, windows-latest]
  # Parallel execution for faster feedback

environment_protection: true
  # Production deployments require approval
  # Staging/dev environments auto-deploy
  # Environment-specific secrets and variables
```

### 2. testing-strategies
```yaml
test_levels: ["unit", "integration", "e2e"]
  # unit: Fast, isolated tests (Jest, pytest, JUnit)
  # integration: Component interaction tests
  # e2e: Full user journey tests (Playwright, Cypress)

coverage_threshold: 80
  # Minimum 80% code coverage required
  # Fail pipeline if threshold not met
  # Generate coverage reports (HTML, JSON, LCOV)

parallel_execution: true
  # Run test suites in parallel
  # Shard E2E tests across multiple workers
  # Reduces total test time by 50-70%

test_reporting: "junit-xml"
  # JUnit XML format for test results
  # Visible in GitHub Actions UI
  # Track test trends over time
  # Annotate failed tests in PR comments

fail_fast: false
  # Continue running all test jobs even if one fails
  # Provides complete picture of failures
  # Useful for matrix testing across versions

flaky_test_detection: true
  # Retry failed tests once to detect flakiness
  # Report consistently flaky tests
  # Prevents intermittent failures blocking deploys
```

### 3. managing-containers
```yaml
containerization: true
  # Build Docker images for consistent environments
  # Multi-stage builds for optimized image size
  # Dockerfile best practices (non-root user, layer caching)

registry: "ghcr.io"
  # GitHub Container Registry (free for public images)
  # Integrated with GitHub authentication
  # Alternative: Docker Hub, AWS ECR, GCP Artifact Registry

image_tagging_strategy: ["git-sha", "branch", "semver"]
  # git-sha: Unique tag per commit (e.g., sha-abc123f)
  # branch: Latest for each branch (e.g., main, develop)
  # semver: Semantic version tags (e.g., v1.2.3)

image_scanning: true
  # Trivy/Snyk scanning for vulnerabilities
  # Fail build on high/critical CVEs
  # Generate SBOM (Software Bill of Materials)

multi_platform_builds: false
  # Enable for arm64 + amd64 images
  # Uses Docker buildx
  # Longer build times but broader compatibility

layer_caching: true
  # Cache Docker layers between builds
  # Significantly speeds up rebuilds
  # Uses GitHub Actions cache or registry cache
```

### 4. implementing-gitops
```yaml
deployment_strategy: "rolling"
  # rolling: Gradual replacement (zero downtime)
  # blue-green: Two identical environments, instant switch
  # canary: Gradual traffic shifting to new version

target_platform: "kubernetes"
  # Kubernetes: Scalable, declarative deployments
  # Alternatives: Cloud Run, ECS, EC2, serverless
  # Helm charts or Kustomize for config management

environment_hierarchy: ["dev", "staging", "production"]
  # dev: Auto-deploy on merge to develop branch
  # staging: Auto-deploy on merge to main branch
  # production: Manual approval + deploy on release tag

rollback_enabled: true
  # Automatic rollback on deployment failure
  # Health checks determine success/failure
  # Keep last 3 versions for quick rollback

progressive_delivery: false
  # Enable for canary deployments with traffic shifting
  # Requires service mesh (Istio, Linkerd) or ingress controller
  # Gradual rollout: 10% → 50% → 100%

deployment_approval: "production"
  # Production requires manual approval
  # Staging/dev auto-deploy without approval
  # Approvers defined in environment settings
```

### 5. hardening-security
```yaml
secret_scanning: true
  # Scan code for exposed secrets (API keys, tokens)
  # Prevent commits with secrets from being pushed
  # Integration with GitHub Secret Scanning

sast_scanning: true
  # Static Application Security Testing
  # CodeQL for semantic code analysis
  # Detect security vulnerabilities in source code

dependency_scanning: true
  # Scan dependencies for known vulnerabilities
  # Dependabot alerts for outdated packages
  # Auto-generate PRs for security updates

container_scanning: true
  # Scan container images for CVEs
  # Trivy/Snyk integration
  # Block deployments with critical vulnerabilities

iac_scanning: true
  # Scan infrastructure-as-code (Terraform, CloudFormation)
  # Detect misconfigurations (open S3 buckets, etc.)
  # Checkov/tfsec integration

sbom_generation: true
  # Generate Software Bill of Materials
  # CycloneDX or SPDX format
  # Track all dependencies and versions

security_baseline: "cis"
  # CIS (Center for Internet Security) benchmarks
  # Enforce security best practices
  # Regular compliance audits
```

### 6. implementing-observability
```yaml
pipeline_monitoring: true
  # Track pipeline success/failure rates
  # Monitor build duration trends
  # Alert on unusual patterns

metrics_collection: ["duration", "success_rate", "deployment_frequency"]
  # duration: Build and deployment time
  # success_rate: Percentage of successful runs
  # deployment_frequency: DORA metric

notification_channels: ["github", "slack"]
  # GitHub: PR comments, check runs, status badges
  # Slack: Build failures, deployment notifications
  # Email: Critical failures only

deployment_tracking: true
  # Track deployment events
  # Link deployments to commits and PRs
  # Monitor deployment frequency and lead time

failure_alerts: true
  # Immediate alerts on pipeline failures
  # Include logs and error context
  # Mention relevant team/individuals

badge_generation: true
  # Build status badge for README
  # Test coverage badge
  # Deployment status badge
```

---

## Quick Questions (Only 3)

When blueprint is detected, ask only these essential questions:

### Question 1: CI Platform
```
Which CI/CD platform will you use?

Options:
1. GitHub Actions (recommended for GitHub repos)
2. GitLab CI (recommended for GitLab repos)
3. Jenkins (self-hosted, maximum flexibility)
4. CircleCI (cloud-based, Docker-native)
5. Other (specify)

Your answer: _______________
```

**Why this matters:**
- Determines pipeline configuration syntax (YAML format varies)
- Affects available integrations and features
- Influences caching and secret management approach

**Default if skipped:** "GitHub Actions" (most common, well-documented)

---

### Question 2: Language/Framework
```
What is your primary application language/framework?

Options:
1. Node.js/TypeScript (npm/yarn/pnpm)
2. Python (pip/poetry/pipenv)
3. Go (go modules)
4. Java/Kotlin (Maven/Gradle)
5. Ruby (bundler/gem)
6. Rust (cargo)
7. Multi-language monorepo
8. Other (specify)

Your answer: _______________
```

**Why this matters:**
- Determines build commands and test runners
- Affects dependency caching strategy
- Influences Docker base images
- Sets appropriate linters and formatters

**Default if skipped:** "Node.js/TypeScript" (most common for web apps)

---

### Question 3: Deployment Target
```
Where will you deploy your application?

Options:
1. Kubernetes cluster (GKE, EKS, AKS, self-hosted)
2. Serverless (AWS Lambda, Google Cloud Functions, Vercel)
3. Container platform (Cloud Run, ECS, Fargate)
4. VM/bare metal (EC2, GCE, DigitalOcean)
5. Static hosting (GitHub Pages, Netlify, Cloudflare Pages)
6. Not deploying yet (CI only)

Your answer: _______________
```

**Why this matters:**
- Determines deployment step configuration
- Affects authentication and credential setup
- Influences infrastructure-as-code choices
- Sets monitoring and rollback strategies

**Default if skipped:** "Kubernetes cluster" (scalable, production-grade)

---

## Blueprint Detection Logic

Trigger this blueprint when the user's goal matches:

```python
def should_use_cicd_blueprint(goal: str) -> bool:
    goal_lower = goal.lower()

    # Primary keywords (high confidence)
    primary_match = any(keyword in goal_lower for keyword in [
        "ci/cd",
        "ci cd",
        "pipeline",
        "github actions",
        "gitlab ci",
        "jenkins",
        "continuous integration",
        "continuous deployment"
    ])

    # Secondary keywords + automation context
    secondary_match = (
        any(keyword in goal_lower for keyword in ["automation", "automate", "workflow"]) and
        any(keyword in goal_lower for keyword in ["build", "test", "deploy", "release"])
    )

    # DevOps context
    devops_match = (
        any(keyword in goal_lower for keyword in ["devops", "infrastructure"]) and
        any(keyword in goal_lower for keyword in ["automation", "pipeline", "deployment"])
    )

    return primary_match or secondary_match or devops_match
```

**Confidence levels:**
- **High (90%+):** Contains "ci/cd" or "pipeline" + deployment term
- **Medium (70-89%):** Contains automation + build/test/deploy
- **Low (50-69%):** Contains "devops" + workflow-related terms

**Present blueprint when confidence >= 70%**

---

## Blueprint Offer Message

When blueprint is detected, present this message to the user:

```
┌────────────────────────────────────────────────────────────┐
│ 🚀 CI/CD PIPELINE BLUEPRINT DETECTED                       │
├────────────────────────────────────────────────────────────┤
│ Your goal matches our optimized CI/CD Pipeline Blueprint! │
│                                                            │
│ Pre-configured features:                                   │
│  ✓ Multi-stage pipeline (lint, test, build, deploy)      │
│  ✓ Automated testing with 80% coverage threshold         │
│  ✓ Container builds with vulnerability scanning          │
│  ✓ GitOps deployment with rollback support               │
│  ✓ Secret scanning and security checks                   │
│  ✓ Pipeline monitoring and Slack notifications           │
│  ✓ Dependency caching for faster builds                  │
│                                                            │
│ Using blueprint reduces questions from 20 to 3!           │
│                                                            │
│ Options:                                                   │
│  1. Use blueprint (3 quick questions, ~15 min)            │
│  2. Custom configuration (20 questions, ~40 min)          │
│  3. Skip all questions (use all defaults, ~10 min)        │
│                                                            │
│ Your choice (1/2/3): _____                                │
└────────────────────────────────────────────────────────────┘
```

**Handle responses:**
- **1 or "blueprint"** → Ask only 3 blueprint questions
- **2 or "custom"** → Ask all skill questions (normal flow)
- **3 or "skip"** → Use all defaults, skip all questions

---

## Generated Output Structure

When blueprint is executed, generate this file structure:

```
ci-cd-project/
├── .github/
│   └── workflows/                        # GitHub Actions workflows
│       ├── ci.yml                        # Continuous Integration workflow
│       │   # Runs on push/PR: lint → test → build → scan
│       │
│       ├── cd.yml                        # Continuous Deployment workflow
│       │   # Runs on release: build → scan → deploy
│       │
│       ├── security.yml                  # Security scanning workflow
│       │   # Scheduled daily: dependency scan, secret scan, SAST
│       │
│       └── pr-checks.yml                 # PR validation workflow
│           # Runs on PR: format check, type check, tests
│
├── .gitlab-ci.yml                        # GitLab CI configuration (if selected)
│   # Multi-stage pipeline with jobs for each stage
│   # Cache configuration, artifacts, environment deployments
│
├── Jenkinsfile                           # Jenkins pipeline (if selected)
│   # Declarative pipeline with stages
│   # Agent configuration, post-build actions
│
├── docker/
│   ├── Dockerfile                        # Application container
│   │   # Multi-stage build for optimized image size
│   │   # Non-root user, minimal base image
│   │
│   ├── Dockerfile.test                   # Test environment container
│   │   # Includes dev dependencies and test tools
│   │
│   └── .dockerignore                     # Docker build exclusions
│       # Exclude node_modules, .git, test files
│
├── k8s/                                  # Kubernetes manifests (if K8s selected)
│   ├── deployment.yml                    # Deployment configuration
│   │   # Rolling update strategy, replicas, health checks
│   │
│   ├── service.yml                       # Service configuration
│   │   # LoadBalancer or ClusterIP, port mappings
│   │
│   ├── ingress.yml                       # Ingress configuration
│   │   # Host routing, TLS certificates
│   │
│   ├── configmap.yml                     # ConfigMap for app config
│   │   # Non-sensitive configuration values
│   │
│   └── secrets.yml.example               # Secret template (DO NOT commit real secrets)
│       # Database passwords, API keys, etc.
│
├── helm/                                 # Helm chart (optional)
│   ├── Chart.yaml                        # Chart metadata
│   ├── values.yaml                       # Default values
│   ├── values-dev.yaml                   # Dev environment overrides
│   ├── values-staging.yaml               # Staging environment overrides
│   ├── values-production.yaml            # Production environment overrides
│   └── templates/                        # Kubernetes templates
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       └── hpa.yaml                      # Horizontal Pod Autoscaler
│
├── scripts/
│   ├── build.sh                          # Build script
│   │   # Build application, run optimizations
│   │
│   ├── test.sh                           # Test script
│   │   # Run all test suites, generate coverage
│   │
│   ├── deploy.sh                         # Deployment script
│   │   # Deploy to specified environment
│   │
│   ├── rollback.sh                       # Rollback script
│   │   # Rollback to previous version
│   │
│   └── health-check.sh                   # Health check script
│       # Verify deployment health
│
├── tests/
│   ├── unit/                             # Unit tests
│   │   └── ...test files...
│   │
│   ├── integration/                      # Integration tests
│   │   └── ...test files...
│   │
│   └── e2e/                              # End-to-end tests
│       └── ...test files...
│
├── .github/
│   ├── dependabot.yml                    # Dependabot configuration
│   │   # Auto-update dependencies weekly
│   │
│   └── CODEOWNERS                        # Code ownership for reviews
│       # Require specific team approvals
│
├── config/
│   ├── jest.config.js                    # Jest test configuration (Node.js)
│   ├── pytest.ini                        # Pytest configuration (Python)
│   ├── eslint.config.js                  # ESLint configuration
│   ├── .prettierrc                       # Prettier formatting
│   └── tsconfig.json                     # TypeScript configuration
│
├── .env.example                          # Environment variable template
│   # Example values for all required env vars
│   # DO NOT commit .env file
│
├── .gitignore                            # Git ignore rules
│   # node_modules/, .env, coverage/, dist/
│
├── package.json                          # Node.js dependencies (if applicable)
│   # Scripts: test, build, lint, format
│
├── requirements.txt                      # Python dependencies (if applicable)
│   # Production dependencies
│
├── requirements-dev.txt                  # Python dev dependencies
│   # pytest, coverage, black, flake8
│
├── Makefile                              # Common commands
│   # make test, make build, make deploy
│
└── README.md                             # Pipeline documentation
    # Setup instructions, pipeline overview, deployment guide
```

---

## Component Architecture

### Pipeline Flow (GitHub Actions Example)

```
┌─────────────────────────────────────────────────────────────┐
│                   Trigger Event (push/PR/release)           │
└────────────────────┬────────────────────────────────────────┘
                     │
     ┌───────────────▼────────────────┐
     │  Checkout Code + Setup Runtime │
     │  - actions/checkout@v4         │
     │  - actions/setup-node@v4       │
     │  - Restore dependency cache    │
     └───────────────┬────────────────┘
                     │
     ┌───────────────▼────────────────┐
     │  Stage 1: Lint & Format        │
     │  - ESLint (code quality)       │
     │  - Prettier (formatting)       │
     │  - TypeScript type check       │
     │  ⏱️  Duration: ~30 seconds      │
     └───────────────┬────────────────┘
                     │
     ┌───────────────▼────────────────┐
     │  Stage 2: Test                 │
     │  - Unit tests (Jest/pytest)    │
     │  - Integration tests           │
     │  - E2E tests (Playwright)      │
     │  - Generate coverage report    │
     │  - Fail if coverage < 80%      │
     │  ⏱️  Duration: ~3-5 minutes     │
     └───────────────┬────────────────┘
                     │
     ┌───────────────▼────────────────┐
     │  Stage 3: Build                │
     │  - Compile/bundle application  │
     │  - Build Docker image          │
     │  - Tag with git-sha + semver   │
     │  - Upload build artifacts      │
     │  ⏱️  Duration: ~2-4 minutes     │
     └───────────────┬────────────────┘
                     │
     ┌───────────────▼────────────────┐
     │  Stage 4: Security Scan        │
     │  - Trivy container scan        │
     │  - CodeQL SAST analysis        │
     │  - Dependency vulnerability    │
     │  - Secret scanning             │
     │  - Fail on critical CVEs       │
     │  ⏱️  Duration: ~2-3 minutes     │
     └───────────────┬────────────────┘
                     │
     ┌───────────────▼────────────────┐
     │  Stage 5: Deploy               │
     │  - Push image to registry      │
     │  - Update K8s deployment       │
     │  - Wait for rollout complete   │
     │  - Run health checks           │
     │  - Rollback on failure         │
     │  ⏱️  Duration: ~3-5 minutes     │
     └───────────────┬────────────────┘
                     │
     ┌───────────────▼────────────────┐
     │  Post-Deployment               │
     │  - Send Slack notification     │
     │  - Update deployment tracker   │
     │  - Generate SBOM               │
     │  - Archive artifacts           │
     └────────────────────────────────┘
```

### Multi-Environment Deployment Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  Git Event Triggers                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  develop branch push → DEV environment                      │
│  ├─ Auto-deploy immediately                                 │
│  ├─- No approval required                                   │
│  └─- Smoke tests after deployment                           │
│                                                             │
│  main branch push → STAGING environment                     │
│  ├─ Auto-deploy after CI passes                             │
│  ├─- No approval required                                   │
│  └─- Full test suite after deployment                       │
│                                                             │
│  tag push (v*.*.*) → PRODUCTION environment                 │
│  ├─ Manual approval required                                │
│  ├─- Designated approvers only                              │
│  ├─- Deploy during maintenance window                       │
│  └─- Progressive rollout (optional)                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Environment Variables per Environment:
┌──────────────┬──────────┬─────────┬────────────┐
│ Variable     │   DEV    │ STAGING │ PRODUCTION │
├──────────────┼──────────┼─────────┼────────────┤
│ REPLICAS     │    1     │    2    │     5      │
│ RESOURCES    │  Small   │ Medium  │   Large    │
│ MONITORING   │  Basic   │  Full   │  Full+     │
│ RATE_LIMIT   │  None    │  Loose  │  Strict    │
│ LOG_LEVEL    │  debug   │  info   │   warn     │
└──────────────┴──────────┴─────────┴────────────┘
```

---

## Default Configuration Examples

### GitHub Actions CI Workflow (ci.yml)

```yaml
name: Continuous Integration

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: Lint and Format Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20.x'
          cache: 'npm'

      - run: npm ci

      - run: npm run lint

      - run: npm run format:check

  test:
    name: Test (Node ${{ matrix.node-version }})
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        node-version: [18.x, 20.x, 22.x]
        os: [ubuntu-latest]
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - run: npm ci

      - run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        if: matrix.node-version == '20.x'

  build:
    name: Build and Scan
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          tags: app:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Run Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: app:${{ github.sha }}
          severity: 'CRITICAL,HIGH'
```

### Kubernetes Deployment (deployment.yml)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
  labels:
    app: myapp
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: ghcr.io/org/app:latest
        ports:
        - containerPort: 8080
        env:
        - name: NODE_ENV
          value: "production"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## Dependencies and Tools

### CI/CD Platform Requirements

**GitHub Actions:**
```yaml
# No external dependencies - built into GitHub
# Pricing: Free for public repos, 2000 min/month free for private
# Hosted runners: Ubuntu, macOS, Windows
```

**GitLab CI:**
```yaml
# Requires GitLab account (SaaS or self-hosted)
# Pricing: Free tier available, 400 min/month
# Shared runners available on GitLab.com
```

**Jenkins:**
```yaml
# Requires self-hosted server
# Java runtime required (JDK 11+)
# Plugins for integrations (Git, Docker, K8s)
```

### Build Tools (Language-Specific)

**Node.js/TypeScript:**
```json
{
  "devDependencies": {
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "eslint": "^8.55.0",
    "prettier": "^3.1.0",
    "jest": "^29.7.0",
    "@playwright/test": "^1.40.0"
  }
}
```

**Python:**
```txt
# requirements-dev.txt
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.12.0
flake8>=7.0.0
mypy>=1.7.0
```

### Container and Deployment Tools

```bash
# Docker (container builds)
docker >= 24.0.0

# kubectl (Kubernetes deployments)
kubectl >= 1.28.0

# Helm (Kubernetes package manager)
helm >= 3.13.0

# Trivy (container scanning)
trivy >= 0.48.0
```

---

## Security Best Practices

### Secret Management

1. **Never commit secrets to git**
   - Use `.env.example` for templates
   - Store secrets in CI/CD platform (GitHub Secrets, GitLab CI/CD Variables)
   - Use secret scanning to prevent accidental commits

2. **Rotate secrets regularly**
   - API keys: Quarterly
   - Database passwords: Monthly
   - Service tokens: On personnel changes

3. **Principle of least privilege**
   - Deploy tokens: Write only to production namespace
   - Registry tokens: Push only to specific repositories
   - Cloud credentials: Minimal IAM permissions

### Vulnerability Scanning

```yaml
# Scan at multiple layers:
- Source code: CodeQL, Semgrep
- Dependencies: Dependabot, Snyk, OWASP Dependency Check
- Containers: Trivy, Grype
- Infrastructure: Checkov, tfsec
- Deployed apps: DAST scanning (ZAP, Burp Suite)
```

### Supply Chain Security

```yaml
# Verify integrity of dependencies and actions
- Use pinned versions (not @latest)
- Verify checksums/signatures
- Enable GitHub Actions security alerts
- Use private registries for internal packages
- Generate and verify SBOMs
```

---

## Performance Optimizations

### Caching Strategies

**Dependency Caching:**
```yaml
# Cache package manager dependencies
- npm/yarn: Cache node_modules based on package-lock.json hash
- pip: Cache ~/.cache/pip based on requirements.txt hash
- maven: Cache ~/.m2/repository based on pom.xml hash
```

**Build Caching:**
```yaml
# Cache intermediate build artifacts
- Docker layer caching: Reuse unchanged layers
- TypeScript: Cache .tsbuildinfo
- Webpack: Use cache-loader or built-in caching
```

**Test Caching:**
```yaml
# Cache test results for unchanged code
- Jest: --cache flag
- pytest: --cache-dir flag
- Playwright: Cache browser binaries
```

### Parallel Execution

```yaml
# Run independent jobs in parallel
jobs:
  lint:      # Runs in parallel
  test:      # Runs in parallel
  build:     # Waits for lint + test
    needs: [lint, test]

# Shard tests across multiple runners
strategy:
  matrix:
    shard: [1, 2, 3, 4]
steps:
  - run: npm test -- --shard=${{ matrix.shard }}/4
```

---

## Monitoring and Observability

### Key Metrics (DORA Metrics)

1. **Deployment Frequency**
   - How often code is deployed to production
   - Target: Multiple times per day (elite performers)

2. **Lead Time for Changes**
   - Time from commit to production deployment
   - Target: < 1 hour (elite performers)

3. **Mean Time to Recovery (MTTR)**
   - Time to restore service after incident
   - Target: < 1 hour (elite performers)

4. **Change Failure Rate**
   - Percentage of deployments causing failures
   - Target: < 15% (elite performers)

### Pipeline Monitoring

```yaml
# Track pipeline performance
- Build duration trends (alert if > 15 min)
- Test flakiness (retry same test 3x to detect)
- Cache hit rates (should be > 80%)
- Deployment success rates (should be > 95%)
```

### Notification Configuration

```yaml
# Slack notifications
on_success: staging, production deployments
on_failure: all environments
include: commit message, author, duration, logs URL

# Email notifications
on_success: production deployments only
on_failure: critical failures only
recipients: on-call team + commit author
```

---

## Accessibility Features

### Pipeline Observability

- **Status badges:** Real-time pipeline status in README
- **PR annotations:** Test failures shown inline in PR diff
- **Build logs:** Searchable, timestamped, collapsible sections
- **Deployment history:** Visual timeline of all deployments
- **Rollback controls:** One-click rollback to previous version

### Developer Experience

- **Local testing:** Scripts to run CI locally before push
- **Fast feedback:** Lint/format checks in < 1 minute
- **Clear errors:** Actionable error messages with fix suggestions
- **Auto-fixes:** Automatic formatting, dependency updates
- **Documentation:** Inline comments in pipeline configs

---

## Testing Recommendations

### Pipeline Testing

```bash
# Test pipeline locally before committing
act -j test                    # Run GitHub Actions locally with 'act'
gitlab-runner exec docker test # Run GitLab CI locally

# Validate pipeline syntax
yamllint .github/workflows/*.yml
gitlab-ci-lint .gitlab-ci.yml

# Test deployment to staging
scripts/deploy.sh staging --dry-run
```

### End-to-End Pipeline Validation

```yaml
# Create test repository to validate:
1. Fork main repo
2. Trigger CI on test branch
3. Verify all stages pass
4. Deploy to test environment
5. Run smoke tests
6. Rollback and verify
7. Delete test environment
```

---

## Customization Points

After blueprint generation, users can easily customize:

1. **Add/remove pipeline stages:** Edit workflow YAML
2. **Change deployment targets:** Update deploy job configuration
3. **Adjust test coverage threshold:** Modify coverage settings
4. **Enable/disable security scans:** Comment out scan jobs
5. **Customize notifications:** Update Slack/email configuration
6. **Add manual approval gates:** Add environment protection rules
7. **Implement canary deployments:** Add traffic shifting logic

---

## Migration Path

If user starts with blueprint but needs custom features later:

1. **Add manual QA step:** Add approval gate before production
2. **Implement blue-green deployment:** Modify deployment strategy
3. **Add performance testing:** Add load testing stage
4. **Implement multi-region deployment:** Add regional deployment jobs
5. **Add chaos engineering:** Integrate chaos testing tools
6. **Implement feature flags:** Add feature flag deployment checks

All additions will integrate with existing pipeline structure.

---

## Version History

**1.0.0** (2025-12-06)
- Initial CI/CD pipeline blueprint
- 6-skill chain with optimized defaults
- 3-question quick configuration
- GitHub Actions as default platform
- Kubernetes as default deployment target
- Comprehensive security scanning
- DORA metrics tracking

---

## Related Blueprints

- **API Blueprint:** For backend API deployment pipelines
- **Monorepo Blueprint:** For multi-package CI/CD
- **Mobile App Blueprint:** For mobile app release automation
- **Infrastructure Blueprint:** For Terraform/CDK pipelines

---

**Blueprint Complete**

---

## Deliverables Specification

This section defines concrete validation checks for blueprint promises, ensuring skills produce what users expect.

### Deliverables

```yaml
deliverables:
  "CI workflow with multi-stage pipeline":
    primary_skill: building-ci-pipelines
    required_files:
      - .github/workflows/ci.yml
    content_checks:
      - pattern: "on:\\s*(push|pull_request)"
        in: .github/workflows/ci.yml
      - pattern: "jobs:"
        in: .github/workflows/ci.yml
      - pattern: "lint|test|build"
        in: .github/workflows/ci.yml
    maturity_required: [starter, intermediate, advanced]

  "CD workflow with deployment stages":
    primary_skill: building-ci-pipelines
    required_files:
      - .github/workflows/cd.yml
    content_checks:
      - pattern: "deploy"
        in: .github/workflows/cd.yml
      - pattern: "on:\\s*(release|push)"
        in: .github/workflows/cd.yml
    maturity_required: [starter, intermediate, advanced]

  "Dependency management automation":
    primary_skill: building-ci-pipelines
    required_files:
      - .github/dependabot.yml
    content_checks:
      - pattern: "version:\\s*2"
        in: .github/dependabot.yml
      - pattern: "updates:"
        in: .github/dependabot.yml
    maturity_required: [starter, intermediate, advanced]

  "Test suite with coverage reporting":
    primary_skill: testing-strategies
    required_files:
      - tests/
    content_checks:
      - pattern: "def test_|describe\\(|it\\(|@test"
        in: tests/
      - pattern: "assert|expect"
        in: tests/
    maturity_required: [starter, intermediate, advanced]

  "Test workflow configuration":
    primary_skill: testing-strategies
    required_files:
      - .github/workflows/test.yml
    content_checks:
      - pattern: "test"
        in: .github/workflows/test.yml
      - pattern: "coverage"
        in: .github/workflows/test.yml
    maturity_required: [intermediate, advanced]

  "Container image build configuration":
    primary_skill: writing-dockerfiles
    required_files:
      - Dockerfile
      - .dockerignore
    content_checks:
      - pattern: "FROM"
        in: Dockerfile
      - pattern: "COPY|ADD"
        in: Dockerfile
      - pattern: "\\.git|node_modules|__pycache__"
        in: .dockerignore
    maturity_required: [starter, intermediate, advanced]

  "Multi-stage Docker build":
    primary_skill: writing-dockerfiles
    required_files:
      - Dockerfile
    content_checks:
      - pattern: "AS builder|AS build"
        in: Dockerfile
      - pattern: "COPY --from="
        in: Dockerfile
    maturity_required: [intermediate, advanced]

  "Docker image build workflow":
    primary_skill: building-ci-pipelines
    required_files:
      - .github/workflows/ci.yml
    content_checks:
      - pattern: "docker/build-push-action|docker build"
        in: .github/workflows/
      - pattern: "docker/login-action|docker login"
        in: .github/workflows/
    maturity_required: [intermediate, advanced]

  "Kubernetes deployment manifests":
    primary_skill: implementing-gitops
    required_files:
      - k8s/base/deployment.yaml
      - k8s/base/service.yaml
      - k8s/base/kustomization.yaml
    content_checks:
      - pattern: "kind: Deployment"
        in: k8s/base/deployment.yaml
      - pattern: "kind: Service"
        in: k8s/base/service.yaml
      - pattern: "apiVersion: kustomize.config.k8s.io"
        in: k8s/base/kustomization.yaml
    maturity_required: [intermediate, advanced]

  "Environment-specific Kustomize overlays":
    primary_skill: implementing-gitops
    required_files:
      - k8s/overlays/dev/kustomization.yaml
      - k8s/overlays/prod/kustomization.yaml
    content_checks:
      - pattern: "bases:|resources:"
        in: k8s/overlays/
      - pattern: "namespace:"
        in: k8s/overlays/
    maturity_required: [starter, intermediate, advanced]

  "GitOps deployment documentation":
    primary_skill: implementing-gitops
    required_files:
      - gitops/README.md
    content_checks:
      - pattern: "GitOps"
        in: gitops/README.md
      - pattern: "deployment"
        in: gitops/README.md
    maturity_required: [intermediate, advanced]

  "Security scanning workflow":
    primary_skill: security-hardening
    required_files:
      - .github/workflows/security.yml
    content_checks:
      - pattern: "trivy|snyk|gitleaks|checkov"
        in: .github/workflows/security.yml
      - pattern: "security|scan"
        in: .github/workflows/security.yml
    maturity_required: [intermediate, advanced]

  "Container vulnerability scanning":
    primary_skill: security-hardening
    required_files:
      - .github/workflows/ci.yml
    content_checks:
      - pattern: "trivy|aquasecurity/trivy-action"
        in: .github/workflows/
      - pattern: "image|container"
        in: .github/workflows/
    maturity_required: [intermediate, advanced]

  "Secret scanning configuration":
    primary_skill: security-hardening
    required_files:
      - .github/workflows/security.yml
    content_checks:
      - pattern: "gitleaks|truffleHog|secret"
        in: .github/workflows/
    maturity_required: [intermediate, advanced]

  "Prometheus metrics configuration":
    primary_skill: implementing-observability
    required_files:
      - observability/prometheus.yml
    content_checks:
      - pattern: "scrape_configs:"
        in: observability/prometheus.yml
      - pattern: "job_name:"
        in: observability/prometheus.yml
    maturity_required: [intermediate, advanced]

  "Pipeline monitoring alerts":
    primary_skill: implementing-observability
    required_files:
      - observability/alerts/
    content_checks:
      - pattern: "alert:|expr:"
        in: observability/alerts/
      - pattern: "pipeline|build|deploy"
        in: observability/alerts/
    maturity_required: [advanced]

  "Grafana dashboards for CI/CD metrics":
    primary_skill: implementing-observability
    required_files:
      - observability/grafana/dashboards/
    content_checks:
      - pattern: '"type":\\s*"graph"|"type":\\s*"gauge"'
        in: observability/grafana/dashboards/
      - pattern: "pipeline|build|deployment"
        in: observability/grafana/dashboards/
    maturity_required: [advanced]

  "Matrix testing workflow":
    primary_skill: building-ci-pipelines
    required_files:
      - .github/workflows/ci.yml
    content_checks:
      - pattern: "strategy:"
        in: .github/workflows/ci.yml
      - pattern: "matrix:"
        in: .github/workflows/ci.yml
    maturity_required: [intermediate, advanced]

  "Caching strategy implementation":
    primary_skill: building-ci-pipelines
    required_files:
      - .github/workflows/ci.yml
    content_checks:
      - pattern: "actions/cache|cache:"
        in: .github/workflows/ci.yml
      - pattern: "key:|restore-keys:"
        in: .github/workflows/ci.yml
    maturity_required: [intermediate, advanced]

  "Deployment scripts":
    primary_skill: implementing-gitops
    required_files:
      - scripts/deploy.sh
    content_checks:
      - pattern: "#!/bin/bash|#!/usr/bin/env bash"
        in: scripts/deploy.sh
      - pattern: "deploy|kubectl|helm"
        in: scripts/deploy.sh
    maturity_required: [starter, intermediate, advanced]

  "Rollback scripts":
    primary_skill: implementing-gitops
    required_files:
      - scripts/rollback.sh
    content_checks:
      - pattern: "#!/bin/bash|#!/usr/bin/env bash"
        in: scripts/rollback.sh
      - pattern: "rollback|previous|revert"
        in: scripts/rollback.sh
    maturity_required: [intermediate, advanced]

  "Docker Compose for local development":
    primary_skill: writing-dockerfiles
    required_files:
      - docker-compose.yml
    content_checks:
      - pattern: "version:|services:"
        in: docker-compose.yml
      - pattern: "build:|image:"
        in: docker-compose.yml
    maturity_required: [intermediate, advanced]

  "Integration test suite":
    primary_skill: testing-strategies
    required_files:
      - tests/integration/
    content_checks:
      - pattern: "def test_|describe\\(|it\\("
        in: tests/integration/
      - pattern: "api|endpoint|database|client"
        in: tests/integration/
    maturity_required: [intermediate, advanced]

  "E2E test suite":
    primary_skill: testing-strategies
    required_files:
      - tests/e2e/
      - playwright.config.ts
    content_checks:
      - pattern: "test\\(|page\\."
        in: tests/e2e/
      - pattern: "defineConfig"
        in: playwright.config.ts
    maturity_required: [advanced]

  "SLSA provenance generation":
    primary_skill: building-ci-pipelines
    required_files:
      - .github/workflows/slsa-provenance.yml
    content_checks:
      - pattern: "slsa-framework/slsa-github-generator"
        in: .github/workflows/slsa-provenance.yml
      - pattern: "provenance"
        in: .github/workflows/slsa-provenance.yml
    maturity_required: [advanced]

  "Canary deployment workflow":
    primary_skill: implementing-gitops
    required_files:
      - gitops/rollouts/canary.yaml
    content_checks:
      - pattern: "kind: Rollout"
        in: gitops/rollouts/canary.yaml
      - pattern: "strategy:"
        in: gitops/rollouts/canary.yaml
      - pattern: "canary:"
        in: gitops/rollouts/canary.yaml
    maturity_required: [advanced]

  "Build and test scripts":
    primary_skill: building-ci-pipelines
    required_files:
      - scripts/build.sh
      - scripts/test.sh
    content_checks:
      - pattern: "#!/bin/bash|#!/usr/bin/env bash"
        in: scripts/
      - pattern: "build|compile|package"
        in: scripts/build.sh
      - pattern: "test|coverage"
        in: scripts/test.sh
    maturity_required: [starter, intermediate, advanced]

  "Project documentation with CI/CD badges":
    primary_skill: building-ci-pipelines
    required_files:
      - README.md
    content_checks:
      - pattern: "CI/CD|Build Status|badge"
        in: README.md
      - pattern: "shields.io|github.com.*badge|status"
        in: README.md
    maturity_required: [starter, intermediate, advanced]
```

### Maturity Profiles

```yaml
maturity_profiles:
  starter:
    description: "Single environment (dev/staging), basic CI/CD with Docker, GitHub Actions, simple sequential pipeline"

    require_additionally:
      - "CI workflow with multi-stage pipeline"
      - "CD workflow with deployment stages"
      - "Dependency management automation"
      - "Test suite with coverage reporting"
      - "Container image build configuration"
      - "Environment-specific Kustomize overlays"
      - "Deployment scripts"
      - "Build and test scripts"
      - "Project documentation with CI/CD badges"

    skip_deliverables:
      - "Test workflow configuration"
      - "Multi-stage Docker build"
      - "Docker image build workflow"
      - "Kubernetes deployment manifests"
      - "GitOps deployment documentation"
      - "Security scanning workflow"
      - "Container vulnerability scanning"
      - "Secret scanning configuration"
      - "Prometheus metrics configuration"
      - "Pipeline monitoring alerts"
      - "Grafana dashboards for CI/CD metrics"
      - "Matrix testing workflow"
      - "Caching strategy implementation"
      - "Rollback scripts"
      - "Docker Compose for local development"
      - "Integration test suite"
      - "E2E test suite"
      - "SLSA provenance generation"
      - "Canary deployment workflow"

    empty_dirs_allowed:
      - .github/workflows/
      - k8s/overlays/staging/
      - tests/integration/
      - tests/e2e/
      - observability/
      - gitops/

    generation_adjustments:
      - Use single-stage Dockerfile for simplicity
      - Sequential pipeline (no parallel jobs)
      - Basic unit tests only
      - Docker Compose instead of Kubernetes
      - Manual deployment approval
      - Extensive inline comments and documentation
      - Include setup instructions in README

  intermediate:
    description: "Multi-environment (dev/staging/prod), GitOps with Kubernetes, security scanning, caching, parallel execution"

    require_additionally:
      - "Test workflow configuration"
      - "Multi-stage Docker build"
      - "Docker image build workflow"
      - "Kubernetes deployment manifests"
      - "GitOps deployment documentation"
      - "Security scanning workflow"
      - "Container vulnerability scanning"
      - "Secret scanning configuration"
      - "Prometheus metrics configuration"
      - "Matrix testing workflow"
      - "Caching strategy implementation"
      - "Rollback scripts"
      - "Docker Compose for local development"
      - "Integration test suite"

    skip_deliverables:
      - "Pipeline monitoring alerts"
      - "Grafana dashboards for CI/CD metrics"
      - "E2E test suite"
      - "SLSA provenance generation"
      - "Canary deployment workflow"

    empty_dirs_allowed:
      - tests/e2e/
      - gitops/rollouts/
      - observability/grafana/dashboards/

    generation_adjustments:
      - Multi-stage Docker builds for optimization
      - Parallel test execution with matrix strategy
      - Kubernetes deployment with Kustomize
      - GitOps with ArgoCD or Flux
      - Automated security scanning in CI
      - Dependency caching for faster builds
      - Basic monitoring with Prometheus
      - Environment-specific deployments (dev/staging/prod)

  advanced:
    description: "Enterprise-scale with progressive delivery, SLSA provenance, comprehensive observability, E2E testing"

    require_additionally:
      - "Pipeline monitoring alerts"
      - "Grafana dashboards for CI/CD metrics"
      - "E2E test suite"
      - "SLSA provenance generation"
      - "Canary deployment workflow"

    skip_deliverables: []

    empty_dirs_allowed: []

    generation_adjustments:
      - SLSA Level 3 provenance for supply chain security
      - Progressive delivery with canary deployments
      - Comprehensive E2E testing with Playwright
      - Advanced monitoring with LGTM stack
      - Custom Grafana dashboards for DORA metrics
      - Multi-cluster GitOps deployments
      - Reusable workflow components
      - Advanced caching strategies (BuildKit, layer caching)
      - Automated rollback on deployment failure
      - Performance analysis and optimization
```

### Validation Process

After all skills complete, the skillchain orchestrator validates deliverables:

1. **File Existence Checks**
   - Verify all `required_files` exist at specified paths
   - Check that maturity-level deliverables are present
   - Allow `empty_dirs_allowed` to be missing for lower maturity levels

2. **Content Pattern Matching**
   - Use regex `pattern` to verify file contents
   - Ensure functional code/config exists (not just scaffolding)
   - Validate CI/CD workflows are properly configured

3. **Maturity-Specific Validation**
   - Starter: Basic CI/CD with single-stage builds, unit tests only
   - Intermediate: Multi-stage builds, security scanning, K8s deployment
   - Advanced: SLSA provenance, progressive delivery, comprehensive observability

4. **Integration Validation**
   - CI workflow references Docker build steps
   - CD workflow references deployment scripts
   - Test workflows exist for each test type (unit/integration/e2e)
   - Security workflows scan both code and containers
   - Monitoring configured for pipeline metrics

5. **Blueprint Promise Verification**
   - Multi-stage pipeline: Verify lint → test → build → deploy stages
   - 80% coverage: Check test configuration includes coverage thresholds
   - Container scanning: Verify Trivy or equivalent in CI
   - GitOps deployment: Verify Kustomize/Helm + K8s manifests
   - Rollback support: Verify rollback scripts and deployment strategies
   - Monitoring: Verify Prometheus + alerts exist

### Error Reporting

When validation fails, report:
```yaml
validation_errors:
  - deliverable: "Container vulnerability scanning"
    missing_files: [".github/workflows/security.yml"]
    missing_patterns: ["trivy"]
    severity: "high"
    fix: "Add Trivy scanning step to CI workflow"

  - deliverable: "E2E test suite"
    missing_files: ["tests/e2e/", "playwright.config.ts"]
    severity: "medium"
    fix: "Install Playwright and add E2E tests (required for advanced maturity)"
```

### Success Metrics

Blueprint considered successful when:
- All maturity-required deliverables present
- All content checks pass
- CI/CD pipeline can execute end-to-end
- Deployments succeed to target environment
- Security scans complete without critical issues
- Monitoring captures pipeline metrics
