---
sidebar_position: 1
---

# API Design Principles

Master plan for designing robust and developer-friendly REST and GraphQL APIs. This skill provides systematic guidance for API architecture, versioning strategies, and best practices that ensure consistency, scalability, and excellent developer experience.

## Status

<span class="badge badge--primary">Master Plan Available</span>

## Key Topics

- **REST API Design**
  - Resource naming conventions and URI structure
  - HTTP method selection (GET, POST, PUT, PATCH, DELETE)
  - Status code usage and error response patterns
  - Pagination, filtering, and sorting strategies
  - HATEOAS and API discoverability

- **GraphQL API Design**
  - Schema design and type system
  - Query and mutation patterns
  - Resolver optimization and N+1 query prevention
  - Subscription design for real-time updates
  - Error handling and partial responses

- **API Versioning**
  - Versioning strategies (URL, header, content negotiation)
  - Deprecation policies and migration paths
  - Backward compatibility considerations
  - Semantic versioning for APIs

- **Authentication & Authorization**
  - OAuth 2.0 and OpenID Connect patterns
  - API key management
  - JWT token design and validation
  - Rate limiting and throttling

- **API Documentation**
  - OpenAPI/Swagger specification
  - GraphQL schema documentation
  - Interactive API explorers
  - Code examples and SDKs

## Primary Tools & Technologies

- **REST Frameworks**: Express.js, FastAPI, Django REST Framework, Spring Boot
- **GraphQL Tools**: Apollo Server, GraphQL Yoga, Hasura
- **Documentation**: Swagger/OpenAPI, GraphQL Playground, Postman
- **Validation**: JSON Schema, Zod, Joi, GraphQL type system
- **Testing**: Postman, Insomnia, REST Client, GraphQL testing libraries

## Integration Points

- **SDK Design**: APIs are consumed through SDKs
- **Documentation Generation**: Auto-generate API docs from code
- **Building CLIs**: CLIs often interact with APIs
- **Debugging Techniques**: API debugging and tracing
- **Git Workflows**: API versioning and change management

## Related Skills

- Backend development patterns
- Database schema design
- Microservices architecture
- Security best practices
- Performance optimization

## Implementation Approach

The skill will provide:
- Decision frameworks for REST vs GraphQL selection
- API design templates and boilerplates
- Validation scripts for API consistency
- OpenAPI/GraphQL schema generators
- Testing strategy templates
