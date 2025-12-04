---
sidebar_position: 3
---

# SDK Design

Master plan for designing developer-friendly software development kits and libraries. This skill covers API design, language-specific idioms, documentation, versioning, and distribution strategies for creating SDKs that provide excellent developer experience across multiple programming languages.

## Status

<span class="badge badge--primary">Master Plan Available</span>

## Key Topics

- **SDK Architecture**
  - Client design patterns (fluent, builder, factory)
  - Authentication and session management
  - Request/response handling
  - Error handling and retry logic
  - Async vs sync API design

- **Language-Specific Design**
  - JavaScript/TypeScript SDK patterns
  - Python SDK conventions (PEP 8)
  - Go SDK idioms
  - Java/Kotlin patterns
  - Ruby, PHP, .NET considerations

- **Developer Experience**
  - Intuitive API surface design
  - Type safety and IntelliSense support
  - Sensible defaults and configuration
  - Examples and code snippets
  - Migration guides between versions

- **Error Handling**
  - Exception hierarchy design
  - Error codes and messages
  - Validation and early failure
  - Logging and debugging support
  - Retry strategies and circuit breakers

- **Testing & Quality**
  - Unit testing SDK methods
  - Integration testing with API
  - Mock and stub strategies
  - Code coverage and quality metrics
  - Example-driven testing

- **Distribution & Versioning**
  - Package manager publishing (npm, PyPI, Maven, Go modules)
  - Semantic versioning strategy
  - Changelog generation
  - Deprecation warnings
  - Breaking change management

## Primary Tools & Technologies

- **JavaScript/TypeScript**: Axios, node-fetch, TypeScript compiler
- **Python**: Requests, httpx, Pydantic, Poetry
- **Go**: net/http, Go modules
- **Java**: OkHttp, Jackson, Maven/Gradle
- **Documentation**: TypeDoc, Sphinx, GoDoc, JavaDoc

## Integration Points

- **API Design Principles**: SDKs wrap APIs
- **Documentation Generation**: Auto-generate SDK docs
- **Building CLIs**: CLIs can use SDKs internally
- **Debugging Techniques**: SDK debugging patterns
- **Git Workflows**: SDK versioning and releases

## Related Skills

- HTTP client design
- Authentication patterns
- Rate limiting and throttling
- Caching strategies
- Multi-language development

## Implementation Approach

The skill will provide:
- SDK architecture templates by language
- Client design patterns and examples
- Error handling frameworks
- Testing strategy templates
- Documentation templates
- Publishing checklists
