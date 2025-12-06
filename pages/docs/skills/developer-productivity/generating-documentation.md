---
sidebar_position: 4
title: Generating Documentation
description: Automatically generate comprehensive documentation from code, APIs, and schemas
tags: [developer-productivity, documentation, docstrings, api-docs, static-sites]
---

# Generating Documentation

Automatically generate comprehensive documentation from code, APIs, and schemas using documentation tools, docstring conventions, and API specification generation. Keep documentation synchronized with code through automated processes and CI/CD integration.

## When to Use

Use when:
- Setting up automated documentation generation from code
- Creating API documentation from OpenAPI/Swagger specs
- Building static documentation sites (Docusaurus, MkDocs, Sphinx)
- Generating SDK reference documentation
- Implementing documentation-as-code workflows
- Deploying versioned documentation with CI/CD

## Key Features

### Code Documentation
- Docstring conventions (JSDoc, Python docstrings, GoDoc, JavaDoc)
- Inline documentation best practices
- Markdown in documentation
- Code examples in docs
- Type annotations and documentation

### API Documentation
- OpenAPI/Swagger generation from code
- GraphQL schema documentation
- Postman collection generation
- Interactive API explorers
- API changelog generation

### Static Site Generators
- Docusaurus setup and configuration
- VitePress for Vue-based docs
- Sphinx for Python projects
- MkDocs and Material theme
- GitBook and alternatives

### Documentation as Code
- Markdown-based documentation
- Version control for docs
- Documentation testing and validation
- Broken link checking
- Search functionality

## Quick Start

### TypeScript with TypeDoc

```typescript
/**
 * Represents a user in the system.
 *
 * @example
 * ```typescript
 * const user = new User('john@example.com', 'John Doe');
 * await user.save();
 * ```
 */
export class User {
  /**
   * Creates a new user instance.
   *
   * @param email - The user's email address
   * @param name - The user's full name
   * @throws {ValidationError} If email format is invalid
   */
  constructor(
    public email: string,
    public name: string
  ) {
    if (!this.isValidEmail(email)) {
      throw new ValidationError('Invalid email format');
    }
  }

  /**
   * Saves the user to the database.
   *
   * @returns Promise that resolves when save is complete
   */
  async save(): Promise<void> {
    // Implementation
  }

  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}
```

Generate docs:
```bash
typedoc --out docs src/index.ts
```

### Python with Sphinx

```python
"""
User management module.

This module provides the User class for managing user accounts.
"""

class User:
    """
    Represents a user in the system.

    Args:
        email (str): The user's email address
        name (str): The user's full name

    Raises:
        ValueError: If email format is invalid

    Example:
        >>> user = User('john@example.com', 'John Doe')
        >>> user.save()
    """

    def __init__(self, email: str, name: str):
        if not self._is_valid_email(email):
            raise ValueError('Invalid email format')
        self.email = email
        self.name = name

    def save(self) -> None:
        """
        Save the user to the database.

        Returns:
            None
        """
        # Implementation
        pass

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Validate email format."""
        import re
        return bool(re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email))
```

Generate docs:
```bash
sphinx-apidoc -o docs/source src/
sphinx-build -b html docs/source docs/build
```

### OpenAPI/Swagger Generation

```javascript
// Express.js with swagger-jsdoc
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'User API',
      version: '1.0.0',
    },
  },
  apis: ['./routes/*.js'],
};

const specs = swaggerJsdoc(options);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(specs));

/**
 * @swagger
 * /users/{id}:
 *   get:
 *     summary: Get user by ID
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: User object
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 id:
 *                   type: string
 *                 email:
 *                   type: string
 *                 name:
 *                   type: string
 */
app.get('/users/:id', getUser);
```

### Docusaurus Site

```bash
# Create Docusaurus site
npx create-docusaurus@latest my-docs classic

# Add documentation pages
mkdir -p docs
cat > docs/intro.md << 'EOF'
---
sidebar_position: 1
---

# Introduction

Welcome to our documentation.
EOF

# Build and deploy
npm run build
npm run serve
```

## Auto-Generation Tools by Language

| Language | Tool | Command |
|----------|------|---------|
| **JavaScript/TypeScript** | TypeDoc | `typedoc --out docs src/` |
| **Python** | Sphinx | `sphinx-build -b html source build` |
| **Python** | pdoc | `pdoc --html --output-dir docs mymodule` |
| **Go** | GoDoc | `godoc -http=:6060` |
| **Java** | JavaDoc | `javadoc -d docs src/**/*.java` |
| **Rust** | rustdoc | `cargo doc --open` |

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Documentation

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      # Build documentation
      - run: npm ci
      - run: npm run docs:build

      # Deploy to GitHub Pages (main branch only)
      - if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

## Documentation Quality Checklist

- [ ] All public APIs have docstrings/JSDoc
- [ ] Code examples are tested and working
- [ ] API endpoints documented with OpenAPI/Swagger
- [ ] Breaking changes highlighted in changelogs
- [ ] Search functionality enabled
- [ ] Broken links checked in CI
- [ ] Mobile-responsive documentation site
- [ ] Versioned docs for multiple releases

## Related Skills

- [Designing APIs](./designing-apis) - Generate API documentation automatically
- [Designing SDKs](./designing-sdks) - Generate SDK reference documentation
- [Building CLIs](./building-clis) - Generate CLI help and man pages
- [Managing Git Workflows](./managing-git-workflows) - Documentation versioning and deployment

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/documentation-generation)
- [Master Plan](../../master-plans/developer-productivity/generating-documentation)
