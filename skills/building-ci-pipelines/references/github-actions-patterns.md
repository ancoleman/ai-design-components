# GitHub Actions Patterns

This reference provides detailed patterns for GitHub Actions workflows including reusable workflows, composite actions, matrix strategies, and advanced techniques.

## Table of Contents

1. [Workflow Syntax Reference](#workflow-syntax-reference)
2. [Reusable Workflows](#reusable-workflows)
3. [Composite Actions](#composite-actions)
4. [Matrix Strategies](#matrix-strategies)
5. [OIDC Federation Setup](#oidc-federation-setup)
6. [Secrets Management](#secrets-management)
7. [Artifact Management](#artifact-management)
8. [Concurrency Control](#concurrency-control)

## Workflow Syntax Reference

### Basic Workflow Structure

```yaml
name: Workflow Name
on: [push, pull_request]

permissions:
  contents: read
  pull-requests: write

env:
  NODE_VERSION: '20'

jobs:
  job-name:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - run: npm test
```

### Trigger Events

```yaml
on:
  # Simple events
  push:
  pull_request:
  workflow_dispatch:  # Manual trigger

  # Event with filters
  push:
    branches: [main, develop]
    paths:
      - 'src/**'
      - '!**.md'

  # Scheduled runs
  schedule:
    - cron: '0 2 * * *'  # 2 AM UTC daily

  # Release events
  release:
    types: [published, created]

  # Pull request events
  pull_request:
    types: [opened, synchronize, reopened]
    branches: [main]

  # Workflow call (for reusable workflows)
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
```

### Job Dependencies

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build

  test:
    needs: build  # Wait for build
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  deploy:
    needs: [build, test]  # Wait for both
    runs-on: ubuntu-latest
    steps:
      - run: npm run deploy
```

### Conditional Execution

```yaml
jobs:
  deploy:
    # Only run on main branch pushes
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - run: deploy.sh

  # Step-level conditions
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Notify on failure
        if: failure()
        run: echo "Workflow failed"

      - name: Notify on success
        if: success()
        run: echo "Workflow succeeded"
```

## Reusable Workflows

### Creating Reusable Workflow

File: `.github/workflows/reusable-deploy.yml`

```yaml
name: Reusable Deploy
on:
  workflow_call:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        type: string
      node-version:
        description: 'Node.js version'
        required: false
        type: string
        default: '20'
      run-tests:
        description: 'Run tests before deploy'
        required: false
        type: boolean
        default: true
    secrets:
      deploy-token:
        required: true
      slack-webhook:
        required: false
    outputs:
      deployment-url:
        description: 'URL of deployed application'
        value: ${{ jobs.deploy.outputs.url }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    outputs:
      url: ${{ steps.deploy.outputs.url }}
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: 'npm'

      - run: npm ci

      - name: Run tests
        if: inputs.run-tests
        run: npm test

      - name: Build
        run: npm run build

      - name: Deploy
        id: deploy
        run: |
          npm run deploy
          echo "url=https://app.example.com" >> $GITHUB_OUTPUT
        env:
          DEPLOY_TOKEN: ${{ secrets.deploy-token }}

      - name: Notify Slack
        if: always() && secrets.slack-webhook != ''
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.slack-webhook }}
          payload: |
            {
              "text": "Deployment to ${{ inputs.environment }}: ${{ job.status }}"
            }
```

### Calling Reusable Workflow

File: `.github/workflows/production.yml`

```yaml
name: Production Deploy
on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: staging
      node-version: '20'
      run-tests: true
    secrets:
      deploy-token: ${{ secrets.STAGING_DEPLOY_TOKEN }}

  deploy-production:
    needs: deploy-staging
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: production
      node-version: '20'
      run-tests: false  # Already tested in staging
    secrets:
      deploy-token: ${{ secrets.PRODUCTION_DEPLOY_TOKEN }}
      slack-webhook: ${{ secrets.SLACK_WEBHOOK }}

  verify:
    needs: deploy-production
    runs-on: ubuntu-latest
    steps:
      - name: Verify deployment
        run: |
          URL="${{ needs.deploy-production.outputs.deployment-url }}"
          curl -f "$URL/health" || exit 1
```

## Composite Actions

### Creating Composite Action

File: `.github/actions/setup-node-with-cache/action.yml`

```yaml
name: Setup Node with Cache
description: Setup Node.js with dependency caching and installation
author: Your Team

inputs:
  node-version:
    description: Node.js version
    required: false
    default: '20'
  package-manager:
    description: Package manager (npm, yarn, pnpm)
    required: false
    default: 'npm'
  install-dependencies:
    description: Install dependencies after setup
    required: false
    default: 'true'

outputs:
  cache-hit:
    description: Whether cache was hit
    value: ${{ steps.cache.outputs.cache-hit }}

runs:
  using: composite
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: ${{ inputs.package-manager }}

    - name: Cache node modules
      id: cache
      uses: actions/cache@v4
      with:
        path: node_modules
        key: ${{ runner.os }}-${{ inputs.package-manager }}-${{ hashFiles('**/package-lock.json', '**/yarn.lock', '**/pnpm-lock.yaml') }}

    - name: Install dependencies
      if: inputs.install-dependencies == 'true' && steps.cache.outputs.cache-hit != 'true'
      shell: bash
      run: |
        case "${{ inputs.package-manager }}" in
          npm) npm ci ;;
          yarn) yarn install --frozen-lockfile ;;
          pnpm) pnpm install --frozen-lockfile ;;
        esac

    - name: Report status
      shell: bash
      run: |
        echo "✅ Node.js ${{ inputs.node-version }} setup complete"
        echo "📦 Package manager: ${{ inputs.package-manager }}"
        echo "💾 Cache hit: ${{ steps.cache.outputs.cache-hit }}"
```

### Using Composite Action

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: ./.github/actions/setup-node-with-cache
        with:
          node-version: '20'
          package-manager: 'pnpm'

      - run: pnpm run build
      - run: pnpm test
```

## Matrix Strategies

### Basic Matrix

```yaml
jobs:
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

Result: 9 jobs (3 OS × 3 versions)

### Matrix with Include/Exclude

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    node-version: [18, 20, 22]
    # Exclude specific combinations
    exclude:
      - os: macos-latest
        node-version: 18
    # Add specific combinations
    include:
      - os: ubuntu-latest
        node-version: 22
        experimental: true
```

### Matrix with Custom Variables

```yaml
strategy:
  matrix:
    config:
      - { os: ubuntu-latest, python: '3.10', toxenv: py310 }
      - { os: ubuntu-latest, python: '3.11', toxenv: py311 }
      - { os: ubuntu-latest, python: '3.12', toxenv: py312 }
      - { os: windows-latest, python: '3.12', toxenv: py312-windows }
      - { os: macos-latest, python: '3.12', toxenv: py312-macos }

steps:
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.config.python }}

  - run: tox -e ${{ matrix.config.toxenv }}
```

### Dynamic Matrix (JSON)

```yaml
jobs:
  generate-matrix:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - uses: actions/checkout@v4
      - id: set-matrix
        run: |
          # Generate matrix from changed packages
          MATRIX=$(python scripts/get_changed_packages.py)
          echo "matrix=$MATRIX" >> $GITHUB_OUTPUT

  test:
    needs: generate-matrix
    runs-on: ubuntu-latest
    strategy:
      matrix: ${{ fromJSON(needs.generate-matrix.outputs.matrix) }}
    steps:
      - run: npm test --workspace=${{ matrix.package }}
```

### Matrix with Fail-Fast Control

```yaml
strategy:
  fail-fast: false  # Continue other jobs even if one fails
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    node-version: [18, 20, 22]
  max-parallel: 4  # Limit concurrent jobs
```

## OIDC Federation Setup

### AWS OIDC Configuration

**Step 1: Create IAM OIDC Identity Provider**

```bash
# Via AWS CLI
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

**Step 2: Create IAM Role with Trust Policy**

Trust policy JSON:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:myorg/myrepo:*"
        }
      }
    }
  ]
}
```

More restrictive conditions:
```json
"Condition": {
  "StringEquals": {
    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
    "token.actions.githubusercontent.com:sub": "repo:myorg/myrepo:ref:refs/heads/main"
  }
}
```

**Step 3: Attach Permission Policy**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-deploy-bucket",
        "arn:aws:s3:::my-deploy-bucket/*"
      ]
    }
  ]
}
```

**Step 4: Use in Workflow**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # Required for OIDC
      contents: read
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          role-session-name: GitHubActions-${{ github.run_id }}
          aws-region: us-east-1

      - name: Verify credentials
        run: aws sts get-caller-identity

      - name: Deploy
        run: aws s3 sync ./dist s3://my-deploy-bucket
```

### GCP OIDC Configuration

**Step 1: Create Workload Identity Pool**

```bash
gcloud iam workload-identity-pools create github-pool \
  --location="global" \
  --description="GitHub Actions pool"
```

**Step 2: Create Workload Identity Provider**

```bash
gcloud iam workload-identity-pools providers create-oidc github-provider \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository=='myorg/myrepo'"
```

**Step 3: Grant Service Account Access**

```bash
gcloud iam service-accounts add-iam-policy-binding deploy-sa@myproject.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/attribute.repository/myorg/myrepo"
```

**Step 4: Use in Workflow**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: 'projects/123456789/locations/global/workloadIdentityPools/github-pool/providers/github-provider'
          service_account: 'deploy-sa@myproject.iam.gserviceaccount.com'

      - name: Deploy to Cloud Run
        run: gcloud run deploy myapp --image gcr.io/myproject/myapp:latest
```

### Azure OIDC Configuration

**Step 1: Create Azure AD Application**

```bash
az ad app create --display-name github-actions-app
```

**Step 2: Create Service Principal**

```bash
az ad sp create --id <APP_ID>
```

**Step 3: Create Federated Credential**

```bash
az ad app federated-credential create \
  --id <APP_ID> \
  --parameters '{
    "name": "github-actions-credential",
    "issuer": "https://token.actions.githubusercontent.com",
    "subject": "repo:myorg/myrepo:ref:refs/heads/main",
    "audiences": ["api://AzureADTokenExchange"]
  }'
```

**Step 4: Use in Workflow**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4

      - name: Azure Login
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Deploy to Azure
        run: az webapp up --name myapp --resource-group myrg
```

## Secrets Management

### GitHub Encrypted Secrets

Store secrets at repository, environment, or organization level.

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Use secret
        run: ./deploy.sh
        env:
          API_KEY: ${{ secrets.API_KEY }}
```

Never expose secrets in logs:
```yaml
# BAD - secret exposed
- run: echo "API_KEY=${{ secrets.API_KEY }}"

# GOOD - secret used in env
- run: ./script.sh
  env:
    API_KEY: ${{ secrets.API_KEY }}
```

### Vault Integration

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: hashicorp/vault-action@v3
        with:
          url: https://vault.example.com
          method: jwt
          role: github-actions
          secrets: |
            secret/data/production/api API_KEY | API_KEY ;
            secret/data/production/db DB_PASSWORD | DB_PASSWORD

      - name: Use secrets from Vault
        run: ./deploy.sh
        env:
          API_KEY: ${{ env.API_KEY }}
          DB_PASSWORD: ${{ env.DB_PASSWORD }}
```

## Artifact Management

### Upload Artifacts

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build

      - uses: actions/upload-artifact@v4
        with:
          name: build-artifacts
          path: |
            dist/
            build/
          retention-days: 30
          if-no-files-found: error
```

### Download Artifacts

```yaml
jobs:
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build-artifacts
          path: dist/

      - run: ls -R dist/
      - run: ./deploy.sh
```

### Share Between Jobs

```yaml
jobs:
  build:
    outputs:
      version: ${{ steps.version.outputs.version }}
    steps:
      - id: version
        run: echo "version=1.2.3" >> $GITHUB_OUTPUT

  deploy:
    needs: build
    steps:
      - run: echo "Deploying version ${{ needs.build.outputs.version }}"
```

## Concurrency Control

### Cancel In-Progress Runs

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

For PRs, this cancels previous runs when new commits are pushed.

### Environment-Specific Concurrency

```yaml
jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment: production
    concurrency:
      group: production-deploy
      cancel-in-progress: false  # Never cancel production deploys
```

### Branch-Specific Concurrency

```yaml
concurrency:
  group: deploy-${{ github.ref_name }}
  cancel-in-progress: ${{ github.ref_name != 'main' }}
```

Main branch deploys never cancel; feature branch deploys cancel previous runs.
