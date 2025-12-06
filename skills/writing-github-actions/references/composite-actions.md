# Composite Actions Guide

Step-level reusability through composite actions in GitHub Actions.

## Table of Contents

1. [Overview](#overview)
2. [Creating Composite Actions](#creating-composite-actions)
3. [Using Composite Actions](#using-composite-actions)
4. [Inputs and Outputs](#inputs-and-outputs)
5. [Best Practices](#best-practices)
6. [Common Patterns](#common-patterns)
7. [Comparison with Reusable Workflows](#comparison-with-reusable-workflows)

---

## Overview

Composite actions package multiple workflow steps into a single reusable action. They enable step-level code reuse without creating separate repositories or publishing to the marketplace.

**Key Benefits:**
- Package common step sequences
- Distribute via repository or marketplace
- Share same runner and workspace
- Support up to 10 levels of nesting

**When to Use:**
- Packaging 5-20 step sequences
- Setup/teardown operations
- Utility functions (validation, formatting)
- Organization-wide tooling standards

**vs Reusable Workflows:**
- Composite actions: Step-level reuse
- Reusable workflows: Job-level reuse

---

## Creating Composite Actions

### Basic Structure

File: `.github/actions/my-action/action.yml`

```yaml
name: 'Action Name'
description: 'What this action does'

inputs:
  # Input definitions

outputs:
  # Output definitions

runs:
  using: "composite"
  steps:
    # Step definitions
```

### Minimal Example

```yaml
name: 'Hello World'
description: 'Print hello message'

runs:
  using: "composite"
  steps:
    - run: echo "Hello from composite action"
      shell: bash
```

**Key Requirements:**
- `runs.using: "composite"` is required
- All `run` steps must specify `shell:`
- Located in `action.yml` file

### With Inputs

```yaml
name: 'Setup Project'
description: 'Install dependencies and setup environment'

inputs:
  node-version:
    description: 'Node.js version to use'
    required: false
    default: '20'
  install-command:
    description: 'Command to install dependencies'
    required: false
    default: 'npm ci'
  working-directory:
    description: 'Working directory'
    required: false
    default: '.'

runs:
  using: "composite"
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'
        cache-dependency-path: ${{ inputs.working-directory }}/package-lock.json

    - name: Install dependencies
      shell: bash
      working-directory: ${{ inputs.working-directory }}
      run: ${{ inputs.install-command }}

    - name: Verify installation
      shell: bash
      run: node --version && npm --version
```

### With Outputs

```yaml
name: 'Get Version'
description: 'Extract version from package.json'

inputs:
  package-file:
    description: 'Path to package.json'
    required: false
    default: 'package.json'

outputs:
  version:
    description: "Version number"
    value: ${{ steps.get-version.outputs.version }}
  major:
    description: "Major version"
    value: ${{ steps.parse.outputs.major }}
  minor:
    description: "Minor version"
    value: ${{ steps.parse.outputs.minor }}

runs:
  using: "composite"
  steps:
    - id: get-version
      shell: bash
      run: |
        VERSION=$(jq -r '.version' ${{ inputs.package-file }})
        echo "version=$VERSION" >> $GITHUB_OUTPUT

    - id: parse
      shell: bash
      run: |
        VERSION="${{ steps.get-version.outputs.version }}"
        IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"
        echo "major=$MAJOR" >> $GITHUB_OUTPUT
        echo "minor=$MINOR" >> $GITHUB_OUTPUT
        echo "patch=$PATCH" >> $GITHUB_OUTPUT
```

### With Script Execution

**Directory Structure:**

```
.github/actions/validate/
├── action.yml
└── scripts/
    └── validate.sh
```

**action.yml:**

```yaml
name: 'Validate Project'
description: 'Run validation checks'

inputs:
  strict-mode:
    description: 'Enable strict validation'
    required: false
    default: 'false'

runs:
  using: "composite"
  steps:
    - name: Make script executable
      shell: bash
      run: chmod +x ${{ github.action_path }}/scripts/validate.sh

    - name: Run validation
      shell: bash
      run: ${{ github.action_path }}/scripts/validate.sh
      env:
        STRICT_MODE: ${{ inputs.strict-mode }}
        ACTION_PATH: ${{ github.action_path }}
```

**scripts/validate.sh:**

```bash
#!/bin/bash
set -e

echo "Running validation..."

if [ "$STRICT_MODE" = "true" ]; then
  echo "Strict mode enabled"
  npm run lint
  npm run type-check
  npm test
else
  echo "Standard validation"
  npm run lint
fi
```

---

## Using Composite Actions

### Local Action (Same Repository)

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Setup project
        uses: ./.github/actions/setup-project
        with:
          node-version: '20'
          install-command: 'npm ci'

      - run: npm run build
```

**Path Requirements:**
- Start with `./`
- Point to directory containing `action.yml`
- Relative to repository root

### External Action (Different Repository)

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Setup project
        uses: my-org/shared-actions/setup-project@v1
        with:
          node-version: '20'

      - run: npm run build
```

**Reference Format:** `{owner}/{repo}/{path}@{ref}`

### Marketplace Action

```yaml
- name: Setup Java
  uses: actions/setup-java@v4
  with:
    distribution: 'temurin'
    java-version: '17'
```

### Accessing Outputs

```yaml
- name: Get version
  id: version
  uses: ./.github/actions/get-version
  with:
    package-file: 'package.json'

- name: Use version
  run: |
    echo "Version: ${{ steps.version.outputs.version }}"
    echo "Major: ${{ steps.version.outputs.major }}"
    echo "Minor: ${{ steps.version.outputs.minor }}"
```

---

## Inputs and Outputs

### Input Configuration

```yaml
inputs:
  input-name:
    description: 'Human-readable description'
    required: true|false
    default: 'default-value'
```

**Input Types:**
All inputs are strings in composite actions (no type specification like workflow_call)

**Accessing Inputs:**

```yaml
runs:
  using: "composite"
  steps:
    - run: echo "Input value: ${{ inputs.input-name }}"
      shell: bash
```

### Output Configuration

```yaml
outputs:
  output-name:
    description: 'Human-readable description'
    value: ${{ steps.step-id.outputs.value }}
```

**Setting Outputs:**

```yaml
steps:
  - id: step-id
    shell: bash
    run: echo "value=result" >> $GITHUB_OUTPUT
```

**Composite Action Output:**

```yaml
outputs:
  result:
    description: "Result value"
    value: ${{ steps.compute.outputs.result }}
```

### Environment Variables

**Passing to Steps:**

```yaml
runs:
  using: "composite"
  steps:
    - shell: bash
      env:
        INPUT_VALUE: ${{ inputs.my-input }}
        CUSTOM_VAR: custom-value
      run: |
        echo "Input: $INPUT_VALUE"
        echo "Custom: $CUSTOM_VAR"
```

**From Caller:**

Environment variables from the caller job are available:

```yaml
# Caller
jobs:
  build:
    env:
      BUILD_ENV: production
    steps:
      - uses: ./.github/actions/my-action
        # BUILD_ENV available in action

# Action can access BUILD_ENV
- run: echo $BUILD_ENV
  shell: bash
```

---

## Best Practices

### 1. Always Specify Shell

```yaml
# ❌ Bad - missing shell
- run: echo "Hello"

# ✅ Good - shell specified
- run: echo "Hello"
  shell: bash
```

**Available Shells:**
- `bash` - Bash (default on Linux/macOS)
- `sh` - Bourne shell
- `pwsh` - PowerShell Core
- `powershell` - Windows PowerShell
- `cmd` - Windows Command Prompt
- `python` - Python interpreter

### 2. Use github.action_path

```yaml
# Reference files relative to action directory
- run: ${{ github.action_path }}/scripts/setup.sh
  shell: bash

- run: |
    cat ${{ github.action_path }}/config/default.json
  shell: bash
```

### 3. Provide Sensible Defaults

```yaml
inputs:
  node-version:
    description: 'Node.js version'
    default: '20'
  install-command:
    description: 'Install command'
    default: 'npm ci'
  working-directory:
    description: 'Working directory'
    default: '.'
```

### 4. Document Inputs and Outputs

```yaml
name: 'Setup Project'
description: |
  Install dependencies and setup project environment.
  Supports npm, yarn, and pnpm package managers.

inputs:
  node-version:
    description: |
      Node.js version to use.
      Supports: 18, 20, 22
      Default: 20
    default: '20'
  package-manager:
    description: |
      Package manager to use.
      Options: npm, yarn, pnpm
      Default: npm
    default: 'npm'

outputs:
  cache-hit:
    description: |
      Whether dependencies were restored from cache.
      Values: 'true' or 'false'
    value: ${{ steps.cache.outputs.cache-hit }}
```

### 5. Handle Errors Gracefully

```yaml
runs:
  using: "composite"
  steps:
    - name: Setup
      shell: bash
      run: ./setup.sh || true

    - name: Build
      shell: bash
      run: |
        if ! npm run build; then
          echo "::error::Build failed"
          exit 1
        fi

    - if: failure()
      shell: bash
      run: echo "::warning::Action failed, check logs"
```

### 6. Use Conditional Steps

```yaml
inputs:
  run-tests:
    description: 'Run tests'
    default: 'true'

runs:
  using: "composite"
  steps:
    - name: Build
      shell: bash
      run: npm run build

    - if: inputs.run-tests == 'true'
      name: Test
      shell: bash
      run: npm test
```

### 7. Pin Action Versions

```yaml
# ✅ Pin to commit SHA
- uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608  # v5.0.0

# ⚠️  Tag can be moved
- uses: actions/checkout@v5
```

---

## Common Patterns

### Pattern 1: Setup and Cache

```yaml
name: 'Setup Node.js with Cache'
description: 'Setup Node.js and cache dependencies'

inputs:
  node-version:
    description: 'Node.js version'
    default: '20'
  cache-key-prefix:
    description: 'Cache key prefix'
    default: 'deps'

outputs:
  cache-hit:
    description: "Cache hit status"
    value: ${{ steps.cache.outputs.cache-hit }}

runs:
  using: "composite"
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}

    - id: cache
      uses: actions/cache@v4
      with:
        path: node_modules
        key: ${{ runner.os }}-${{ inputs.cache-key-prefix }}-${{ hashFiles('**/package-lock.json') }}
        restore-keys: |
          ${{ runner.os }}-${{ inputs.cache-key-prefix }}-

    - if: steps.cache.outputs.cache-hit != 'true'
      shell: bash
      run: npm ci
```

### Pattern 2: Multi-Step Validation

```yaml
name: 'Validate Code Quality'
description: 'Run linting, type checking, and tests'

inputs:
  skip-tests:
    description: 'Skip test execution'
    default: 'false'

runs:
  using: "composite"
  steps:
    - name: Lint
      shell: bash
      run: npm run lint

    - name: Type Check
      shell: bash
      run: npm run type-check

    - if: inputs.skip-tests != 'true'
      name: Test
      shell: bash
      run: npm test

    - if: always()
      name: Generate Report
      shell: bash
      run: |
        echo "# Quality Report" >> $GITHUB_STEP_SUMMARY
        echo "✅ Linting passed" >> $GITHUB_STEP_SUMMARY
        echo "✅ Type checking passed" >> $GITHUB_STEP_SUMMARY
```

### Pattern 3: Conditional Tool Installation

```yaml
name: 'Install Tools'
description: 'Install required development tools'

inputs:
  install-docker:
    description: 'Install Docker'
    default: 'false'
  install-kubectl:
    description: 'Install kubectl'
    default: 'false'

runs:
  using: "composite"
  steps:
    - if: inputs.install-docker == 'true'
      name: Setup Docker
      uses: docker/setup-buildx-action@v3

    - if: inputs.install-kubectl == 'true'
      name: Install kubectl
      shell: bash
      run: |
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
        chmod +x kubectl
        sudo mv kubectl /usr/local/bin/
```

### Pattern 4: Build Matrix Support

```yaml
name: 'Build Project'
description: 'Build for different configurations'

inputs:
  build-type:
    description: 'Build type: development, production'
    default: 'production'
  target-platform:
    description: 'Target platform'
    default: 'linux'

runs:
  using: "composite"
  steps:
    - name: Configure build
      shell: bash
      run: |
        echo "BUILD_TYPE=${{ inputs.build-type }}" >> $GITHUB_ENV
        echo "PLATFORM=${{ inputs.target-platform }}" >> $GITHUB_ENV

    - name: Build
      shell: bash
      run: |
        npm run build -- --mode $BUILD_TYPE --platform $PLATFORM

    - name: Upload artifact
      uses: actions/upload-artifact@v4
      with:
        name: build-${{ inputs.build-type }}-${{ inputs.target-platform }}
        path: dist/
```

### Pattern 5: Notification Action

```yaml
name: 'Send Notification'
description: 'Send build status notifications'

inputs:
  webhook-url:
    description: 'Webhook URL'
    required: true
  status:
    description: 'Build status: success, failure'
    required: true
  message:
    description: 'Custom message'
    default: ''

runs:
  using: "composite"
  steps:
    - name: Prepare payload
      id: payload
      shell: bash
      run: |
        MESSAGE="${{ inputs.message }}"
        if [ -z "$MESSAGE" ]; then
          MESSAGE="Build ${{ inputs.status }} for ${{ github.repository }}"
        fi

        PAYLOAD=$(cat <<EOF
        {
          "status": "${{ inputs.status }}",
          "message": "$MESSAGE",
          "repository": "${{ github.repository }}",
          "ref": "${{ github.ref }}",
          "sha": "${{ github.sha }}"
        }
        EOF
        )

        echo "payload<<EOF" >> $GITHUB_OUTPUT
        echo "$PAYLOAD" >> $GITHUB_OUTPUT
        echo "EOF" >> $GITHUB_OUTPUT

    - name: Send notification
      shell: bash
      run: |
        curl -X POST \
          -H "Content-Type: application/json" \
          -d '${{ steps.payload.outputs.payload }}' \
          ${{ inputs.webhook-url }}
```

### Pattern 6: Cleanup Action

```yaml
name: 'Cleanup Workspace'
description: 'Clean build artifacts and caches'

inputs:
  remove-node-modules:
    description: 'Remove node_modules'
    default: 'true'
  remove-build:
    description: 'Remove build directory'
    default: 'true'
  remove-cache:
    description: 'Remove cache'
    default: 'false'

runs:
  using: "composite"
  steps:
    - if: inputs.remove-node-modules == 'true'
      shell: bash
      run: rm -rf node_modules

    - if: inputs.remove-build == 'true'
      shell: bash
      run: rm -rf dist build out

    - if: inputs.remove-cache == 'true'
      shell: bash
      run: rm -rf .cache ~/.npm ~/.yarn
```

---

## Comparison with Reusable Workflows

| Feature | Composite Actions | Reusable Workflows |
|---------|------------------|-------------------|
| **Scope** | Step-level | Job-level |
| **Trigger** | `uses:` in step | `uses:` in job |
| **Location** | `action.yml` | `.github/workflows/*.yml` |
| **Secrets** | Must pass explicitly | Inherit by default |
| **Environment Vars** | Inherit from job | Do not inherit |
| **Outputs** | Step outputs | Job outputs |
| **File Sharing** | Same workspace | Requires artifacts |
| **Nesting** | Up to 10 levels | Up to 10 levels |
| **Best For** | Utility functions | Complete CI/CD jobs |

**When to Use Composite Actions:**
- Packaging step sequences (5-20 steps)
- Setup/teardown operations
- Need access to same workspace
- Distributing via marketplace

**When to Use Reusable Workflows:**
- Standardizing entire jobs
- Multi-job orchestration
- Need job-level configuration
- Cross-repository job reuse

---

## Publishing to Marketplace

### 1. Create Public Repository

```
my-action/
├── action.yml
├── README.md
├── LICENSE
└── .github/
    └── workflows/
        └── test.yml
```

### 2. Complete action.yml Metadata

```yaml
name: 'My Awesome Action'
description: 'Does something awesome'
author: 'Your Name'
branding:
  icon: 'package'
  color: 'blue'

inputs:
  # Input definitions

outputs:
  # Output definitions

runs:
  using: "composite"
  steps:
    # Steps
```

### 3. Create README.md

```markdown
# My Awesome Action

Description of what your action does.

## Usage

\`\`\`yaml
- uses: username/my-action@v1
  with:
    input-name: value
\`\`\`

## Inputs

- `input-name` - Description

## Outputs

- `output-name` - Description

## Example

\`\`\`yaml
# Full example workflow
\`\`\`
```

### 4. Tag Release

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Create major version tag
git tag -fa v1 -m "Update v1 to v1.0.0"
git push origin v1 --force
```

### 5. Publish to Marketplace

1. Go to repository on GitHub
2. Click "Releases" → "Create a new release"
3. Select tag (v1.0.0)
4. Check "Publish this Action to the GitHub Marketplace"
5. Fill in details
6. Publish release

---

## Troubleshooting

### Issue: Shell Not Specified

**Error:** `Error: Required property is missing: shell`

**Solution:**
```yaml
# Add shell to all run steps
- run: echo "Hello"
  shell: bash
```

### Issue: Cannot Access Script Files

**Error:** Script file not found

**Solution:**
```yaml
# Use github.action_path
- run: ${{ github.action_path }}/scripts/setup.sh
  shell: bash
```

### Issue: Inputs Not Working

**Problem:** Input values are empty

**Solution:**
```yaml
# Ensure inputs are defined in action.yml
inputs:
  my-input:
    description: 'Description'
    default: 'default-value'

# Access with correct syntax
- run: echo "${{ inputs.my-input }}"
  shell: bash
```

### Issue: Outputs Not Available

**Problem:** Cannot access step outputs

**Solution:**
```yaml
# Step must have id
- id: my-step
  run: echo "result=value" >> $GITHUB_OUTPUT
  shell: bash

# Output references step id
outputs:
  result:
    value: ${{ steps.my-step.outputs.result }}
```

---

For job-level reuse, see `reusable-workflows.md`.
