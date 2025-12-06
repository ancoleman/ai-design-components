---
sidebar_position: 4
---

# Documentation Generation

Master plan for automatically generating comprehensive documentation from code, APIs, and schemas. This skill covers docstring conventions, documentation tools, API specification generation, and strategies for keeping documentation synchronized with code through automated processes.

## Status

<span class="badge badge--primary">Master Plan Available</span>

## Key Topics

- **Code Documentation**
  - Docstring conventions (JSDoc, Python docstrings, GoDoc, JavaDoc)
  - Inline documentation best practices
  - Markdown in documentation
  - Code examples in docs
  - Type annotations and documentation

- **API Documentation**
  - OpenAPI/Swagger generation from code
  - GraphQL schema documentation
  - Postman collection generation
  - Interactive API explorers
  - API changelog generation

- **Static Site Generators**
  - Docusaurus setup and configuration
  - VitePress for Vue-based docs
  - Sphinx for Python projects
  - MkDocs and Material theme
  - GitBook and alternatives

- **Documentation as Code**
  - Markdown-based documentation
  - Version control for docs
  - Documentation testing and validation
  - Broken link checking
  - Search functionality

- **Auto-Generation Tools**
  - TypeDoc for TypeScript
  - Sphinx autodoc for Python
  - GoDoc and pkg.go.dev
  - JavaDoc and Dokka for Kotlin
  - Rust documentation (rustdoc)

- **CI/CD Integration**
  - Automated doc building
  - Documentation deployment
  - Preview deployments for PRs
  - Versioned documentation
  - Documentation coverage metrics

## Primary Tools & Technologies

- **JavaScript/TypeScript**: TypeDoc, JSDoc, Docusaurus, VitePress
- **Python**: Sphinx, MkDocs, pdoc, pydoc-markdown
- **Go**: GoDoc, pkgsite
- **Java/Kotlin**: JavaDoc, Dokka
- **API Tools**: Swagger/OpenAPI, GraphQL Code Generator, Postman

## Integration Points

- **API Design Principles**: Generate API documentation automatically
- **SDK Design**: Generate SDK reference documentation
- **Building CLIs**: Generate CLI help and man pages
- **Git Workflows**: Documentation versioning and deployment
- **Debugging Techniques**: Documentation for troubleshooting

## Related Skills

- Technical writing
- Markdown authoring
- Static site hosting
- CI/CD pipelines
- Version management

## Implementation Approach

The skill will provide:
- Documentation tool selection framework
- Docstring templates by language
- OpenAPI/GraphQL generation scripts
- Static site generator configurations
- CI/CD pipeline examples
- Documentation quality checklists
