# CI/CD Integration Reference

Automate documentation generation, validation, and deployment in continuous integration pipelines.

## Table of Contents

1. [GitHub Actions](#github-actions)
2. [GitLab CI](#gitlab-ci)
3. [Validation](#validation)
4. [Deployment Strategies](#deployment-strategies)

## GitHub Actions

### Complete Documentation Workflow

```yaml
# .github/workflows/docs.yml
name: Documentation

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    name: Validate Documentation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Lint Markdown
        uses: nosborn/github-action-markdown-cli@v3.3.0
        with:
          files: docs/
          config_file: .markdownlint.json

      - name: Validate OpenAPI specs
        run: |
          npm install -g @redocly/cli
          redocly lint openapi/*.yaml

      - name: Check broken links
        uses: lycheeverse/lychee-action@v1.8.0
        with:
          args: --verbose --no-progress 'docs/**/*.md'

  build-api-docs:
    name: Build API Documentation
    runs-on: ubuntu-latest
    needs: validate
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Generate API docs from OpenAPI
        run: npm run docs:api

      - name: Upload API docs
        uses: actions/upload-artifact@v3
        with:
          name: api-docs
          path: docs/api/

  build-code-docs:
    name: Build Code Documentation
    runs-on: ubuntu-latest
    needs: validate
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Generate TypeDoc documentation
        run: npm run docs:code

      - name: Upload code docs
        uses: actions/upload-artifact@v3
        with:
          name: code-docs
          path: docs/code/

  build-site:
    name: Build Documentation Site
    runs-on: ubuntu-latest
    needs: [build-api-docs, build-code-docs]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Download API docs
        uses: actions/download-artifact@v3
        with:
          name: api-docs
          path: docs/api/

      - name: Download code docs
        uses: actions/download-artifact@v3
        with:
          name: code-docs
          path: docs/code/

      - name: Install dependencies
        run: npm ci

      - name: Build Docusaurus site
        run: npm run docs:build

      - name: Upload site
        uses: actions/upload-artifact@v3
        with:
          name: documentation-site
          path: build/

  deploy:
    name: Deploy Documentation
    runs-on: ubuntu-latest
    needs: build-site
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Download site
        uses: actions/download-artifact@v3
        with:
          name: documentation-site
          path: build/

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
          cname: docs.example.com  # Optional custom domain
```

### API Documentation Only

```yaml
# .github/workflows/api-docs.yml
name: API Documentation

on:
  push:
    paths:
      - 'openapi/**'
      - '.github/workflows/api-docs.yml'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate OpenAPI
        run: |
          npm install -g @redocly/cli
          redocly lint openapi/api.yaml

      - name: Generate Redoc HTML
        run: |
          npx @redocly/cli build-docs openapi/api.yaml \
            --output docs/api.html

      - name: Deploy to GitHub Pages
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

## GitLab CI

### Complete Documentation Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - build
  - deploy

variables:
  NODE_VERSION: "20"

# Cache dependencies
cache:
  paths:
    - node_modules/

validate:markdown:
  stage: validate
  image: node:${NODE_VERSION}
  script:
    - npm install -g markdownlint-cli
    - markdownlint 'docs/**/*.md'

validate:openapi:
  stage: validate
  image: node:${NODE_VERSION}
  script:
    - npm install -g @redocly/cli
    - redocly lint openapi/*.yaml

validate:links:
  stage: validate
  image: node:${NODE_VERSION}
  script:
    - npm install -g linkinator
    - linkinator docs/ --recurse

build:api-docs:
  stage: build
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run docs:api
  artifacts:
    paths:
      - docs/api/
    expire_in: 1 hour

build:code-docs:
  stage: build
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run docs:code
  artifacts:
    paths:
      - docs/code/
    expire_in: 1 hour

build:site:
  stage: build
  image: node:${NODE_VERSION}
  dependencies:
    - build:api-docs
    - build:code-docs
  script:
    - npm ci
    - npm run docs:build
  artifacts:
    paths:
      - build/
    expire_in: 1 week

deploy:pages:
  stage: deploy
  image: alpine:latest
  dependencies:
    - build:site
  script:
    - mv build public
  artifacts:
    paths:
      - public
  only:
    - main

# GitLab Pages will serve from 'public' directory
pages:
  stage: deploy
  script:
    - echo "Deploying to GitLab Pages"
  artifacts:
    paths:
      - public
  only:
    - main
```

## Validation

### Markdown Linting

```json
// .markdownlint.json
{
  "default": true,
  "MD013": {
    "line_length": 100,
    "code_blocks": false
  },
  "MD033": {
    "allowed_elements": ["details", "summary", "img"]
  },
  "MD041": false
}
```

```bash
# Install
npm install -g markdownlint-cli

# Run
markdownlint 'docs/**/*.md'

# Fix automatically
markdownlint --fix 'docs/**/*.md'
```

### OpenAPI Validation

```yaml
# .redocly.yaml
apiDefinitions:
  main: openapi/api.yaml

lint:
  rules:
    no-empty-servers: error
    no-example-value-and-externalValue: error
    no-unused-components: warn
    operation-2xx-response: error
    operation-operationId: error
    operation-summary: error
    operation-tag-defined: error
    path-not-include-query: error
    tag-description: warn
```

```bash
# Install
npm install -g @redocly/cli

# Validate
redocly lint openapi/api.yaml

# Preview
redocly preview-docs openapi/api.yaml
```

### Link Checking

```bash
# Install
npm install -g linkinator

# Check all Markdown files
linkinator docs/ --recurse --markdown

# Check built site
linkinator build/ --recurse
```

## Deployment Strategies

### GitHub Pages

#### Using peaceiris/actions-gh-pages

```yaml
- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./build
    cname: docs.example.com  # Optional
    user_name: 'github-actions[bot]'
    user_email: 'github-actions[bot]@users.noreply.github.com'
```

#### Manual Deployment

```bash
# Build
npm run build

# Deploy
npm run deploy  # If configured in package.json

# Or manually
git checkout gh-pages
cp -r build/* .
git add .
git commit -m "Update documentation"
git push origin gh-pages
```

### Vercel

```yaml
# vercel.json
{
  "buildCommand": "npm run docs:build",
  "outputDirectory": "build",
  "installCommand": "npm install",
  "framework": "docusaurus2"
}
```

```yaml
# .github/workflows/vercel.yml
- name: Deploy to Vercel
  uses: amondnet/vercel-action@v25
  with:
    vercel-token: ${{ secrets.VERCEL_TOKEN }}
    vercel-org-id: ${{ secrets.ORG_ID }}
    vercel-project-id: ${{ secrets.PROJECT_ID }}
    working-directory: ./
```

### Netlify

```toml
# netlify.toml
[build]
  command = "npm run docs:build"
  publish = "build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
```

```yaml
# .github/workflows/netlify.yml
- name: Deploy to Netlify
  uses: nwtgck/actions-netlify@v2.1
  with:
    publish-dir: './build'
    production-branch: main
    github-token: ${{ secrets.GITHUB_TOKEN }}
    deploy-message: "Deploy from GitHub Actions"
  env:
    NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
    NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

### AWS S3 + CloudFront

```yaml
# .github/workflows/aws.yml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-east-1

- name: Deploy to S3
  run: |
    aws s3 sync build/ s3://docs.example.com --delete

- name: Invalidate CloudFront cache
  run: |
    aws cloudfront create-invalidation \
      --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }} \
      --paths "/*"
```

## Versioning in CI/CD

### Docusaurus Versioning

```yaml
# Create version on release
- name: Create documentation version
  if: startsWith(github.ref, 'refs/tags/v')
  run: |
    VERSION=${GITHUB_REF#refs/tags/v}
    npm run docusaurus docs:version $VERSION

- name: Commit version
  run: |
    git config user.name github-actions
    git config user.email github-actions@github.com
    git add .
    git commit -m "docs: version $VERSION"
    git push
```

### MkDocs with Mike

```yaml
# Deploy versioned documentation
- name: Deploy versioned docs
  if: startsWith(github.ref, 'refs/tags/v')
  run: |
    VERSION=${GITHUB_REF#refs/tags/v}
    pip install mike
    mike deploy --push --update-aliases $VERSION latest
    mike set-default --push latest
```

## Best Practices

1. **Validate on PR**: Run validation on pull requests
2. **Deploy on Merge**: Only deploy from main/production branch
3. **Cache Dependencies**: Cache npm/pip packages for faster builds
4. **Parallel Jobs**: Run validation checks in parallel
5. **Artifacts**: Use artifacts to pass data between jobs
6. **Fail Fast**: Stop pipeline on validation errors
7. **Version Documentation**: Tag documentation with releases
8. **Monitor Builds**: Set up notifications for failed builds
9. **Test Locally**: Test CI configuration locally before committing
10. **Security**: Use secrets for sensitive credentials
