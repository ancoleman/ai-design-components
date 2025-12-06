# Documentation Sites Reference

Guide to building comprehensive documentation sites with Docusaurus and MkDocs Material.

## Table of Contents

1. [Docusaurus Setup](#docusaurus-setup)
2. [MkDocs Material Setup](#mkdocs-material-setup)
3. [Versioning](#versioning)
4. [Search Integration](#search-integration)
5. [Deployment](#deployment)

## Docusaurus Setup

React-based documentation site generator with versioning, i18n, and search.

### Installation

```bash
npx create-docusaurus@latest my-website classic
cd my-website
npm start
```

### Configuration

```javascript
// docusaurus.config.js
module.exports = {
  title: 'My Project',
  tagline: 'Awesome documentation',
  url: 'https://docs.example.com',
  baseUrl: '/',
  favicon: 'img/favicon.ico',

  organizationName: 'my-org',
  projectName: 'my-project',

  themeConfig: {
    navbar: {
      title: 'My Project',
      logo: {
        alt: 'My Project Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'doc',
          docId: 'intro',
          position: 'left',
          label: 'Docs',
        },
        {
          type: 'docsVersionDropdown',
          position: 'right',
        },
        {
          href: 'https://github.com/my-org/my-project',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Getting Started',
              to: '/docs/intro',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} My Company.`,
    },
    algolia: {
      apiKey: 'YOUR_API_KEY',
      indexName: 'YOUR_INDEX_NAME',
      contextualSearch: true,
    },
  },

  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/my-org/my-project/edit/main/',
        },
        blog: {
          showReadingTime: true,
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],
};
```

### Sidebars Configuration

```javascript
// sidebars.js
module.exports = {
  docs: [
    'intro',
    {
      type: 'category',
      label: 'Getting Started',
      items: ['installation', 'configuration', 'first-steps'],
    },
    {
      type: 'category',
      label: 'Guides',
      items: ['guides/authentication', 'guides/deployment'],
    },
    {
      type: 'category',
      label: 'API Reference',
      items: ['api/overview', 'api/rest-api'],
    },
  ],
};
```

## MkDocs Material Setup

Python-based documentation site with beautiful Material Design theme.

### Installation

```bash
pip install mkdocs mkdocs-material
mkdocs new my-project
cd my-project
```

### Configuration

```yaml
# mkdocs.yml
site_name: My Project
site_url: https://docs.example.com
repo_url: https://github.com/my-org/my-project
repo_name: my-org/my-project

theme:
  name: material
  palette:
    # Light mode
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    # Dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy
    - content.tabs.link

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google
            show_source: true

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - admonition
  - pymdownx.details
  - attr_list
  - md_in_html
  - toc:
      permalink: true

nav:
  - Home: index.md
  - Getting Started:
    - Installation: getting-started/installation.md
    - Configuration: getting-started/configuration.md
  - Guides:
    - Authentication: guides/authentication.md
    - Deployment: guides/deployment.md
  - API Reference:
    - Overview: api/overview.md
```

### Build and Serve

```bash
# Development server
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## Versioning

### Docusaurus Versioning

```bash
# Create version 1.0.0
npm run docusaurus docs:version 1.0.0

# Directory structure after versioning:
# versioned_docs/
#   version-1.0.0/
#     intro.md
# versioned_sidebars/
#   version-1.0.0-sidebars.json
# versions.json
```

### MkDocs Versioning with Mike

```bash
# Install mike
pip install mike

# Deploy version 1.0
mike deploy 1.0 latest --update-aliases

# Set default version
mike set-default latest

# Deploy to GitHub Pages
mike deploy --push --update-aliases 1.0 latest
```

## Search Integration

### Algolia DocSearch (Docusaurus)

```javascript
// docusaurus.config.js
themeConfig: {
  algolia: {
    apiKey: 'YOUR_SEARCH_API_KEY',
    indexName: 'YOUR_INDEX_NAME',
    appId: 'YOUR_APP_ID',
    contextualSearch: true,
    searchParameters: {},
  },
}
```

Apply for Algolia DocSearch: https://docsearch.algolia.com/apply/

### Built-in Search (MkDocs)

```yaml
# mkdocs.yml
plugins:
  - search:
      lang: en
      separator: '[\s\-\.]+'
```

## Deployment

### GitHub Pages (Docusaurus)

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - name: Install dependencies
        run: npm ci
      - name: Build website
        run: npm run build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
```

### Vercel (Docusaurus)

```json
// vercel.json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "installCommand": "npm install"
}
```

### Netlify (Docusaurus)

```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### GitHub Pages (MkDocs)

```bash
# One-time deployment
mkdocs gh-deploy

# With version management (mike)
mike deploy --push --update-aliases 1.0 latest
```

## Best Practices

1. **Structure Content Logically**: Getting Started → Guides → API Reference
2. **Use Categories**: Group related documentation together
3. **Enable Search**: Make content discoverable
4. **Version Documentation**: Match docs to software versions
5. **Add Edit Links**: Enable community contributions
6. **Include Examples**: Embed working code examples
7. **Test Locally**: Preview changes before deploying
8. **Automate Deployment**: Use CI/CD pipelines
9. **Monitor Analytics**: Track usage and improve content
10. **Keep Updated**: Regular reviews and updates
