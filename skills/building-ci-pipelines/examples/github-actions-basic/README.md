# Basic GitHub Actions CI Example

This example demonstrates a standard CI workflow for a Node.js project with linting, testing, building, and security scanning.

## Workflow Structure

### Jobs

1. **lint** - Code quality checks
   - ESLint
   - Prettier formatting

2. **test** - Unit and integration tests
   - Matrix strategy (Node.js 18, 20, 22)
   - Coverage reporting to Codecov
   - Parallel execution across versions

3. **build** - Production build
   - Depends on lint and test passing
   - Uploads build artifacts
   - Single Node.js version (20)

4. **security** - Security scanning
   - Gitleaks (secret detection)
   - Snyk (vulnerability scanning)
   - Runs in parallel with other jobs

## Features

- **Parallel Execution**: lint, test, and security run simultaneously
- **Matrix Strategy**: Tests run across Node.js 18, 20, and 22
- **Dependency Caching**: npm cache speeds up installs
- **Job Dependencies**: Build only runs after lint and test pass
- **Artifact Upload**: Build artifacts saved for 7 days
- **Coverage Reporting**: Codecov integration for code coverage

## Setup

### Required Secrets

Configure these secrets in repository settings:

- `SNYK_TOKEN` - Snyk API token (optional)
- `CODECOV_TOKEN` - Codecov token (optional)

### Required package.json Scripts

```json
{
  "scripts": {
    "lint": "eslint src/**/*.ts",
    "format:check": "prettier --check 'src/**/*.ts'",
    "test": "jest --coverage",
    "build": "tsc && vite build"
  }
}
```

## Customization

### Add More Node.js Versions

```yaml
strategy:
  matrix:
    node-version: [16, 18, 20, 22]  # Add Node 16
```

### Add Type Checking

```yaml
- name: Type check
  run: npm run type-check
```

### Add E2E Tests

```yaml
e2e:
  name: E2E Tests
  needs: build
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/download-artifact@v4
      with:
        name: build-artifacts
        path: dist/
    - run: npm run test:e2e
```

## Performance

**Typical Runtime:**
- Lint: ~1 minute
- Test (3 versions): ~3 minutes (parallel)
- Build: ~2 minutes
- Security: ~1 minute

**Total wall-clock time:** ~4 minutes (parallelization)

**Sequential time:** ~7 minutes (without parallelization)

## Triggers

- Pushes to `main` and `develop` branches
- Pull requests targeting `main` branch

## Permissions

- `contents: read` - Read repository files
- `pull-requests: write` - Comment on PRs (for coverage reports)
