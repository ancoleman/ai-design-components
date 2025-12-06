---
sidebar_position: 1
title: Designing APIs
description: Design robust REST and GraphQL APIs with systematic guidance for architecture, versioning, and developer experience
tags: [developer-productivity, api-design, rest, graphql, backend]
---

# Designing APIs

Design robust and developer-friendly REST and GraphQL APIs with systematic guidance for API architecture, versioning strategies, authentication patterns, and best practices that ensure consistency, scalability, and excellent developer experience.

## When to Use

Use when:
- Designing new REST or GraphQL APIs from scratch
- Making architectural decisions between REST and GraphQL
- Implementing API versioning strategies
- Defining resource naming and URI structures
- Establishing API authentication and authorization patterns
- Creating API documentation with OpenAPI/Swagger

## Key Features

### REST API Design
- Resource naming conventions and URI structure
- HTTP method selection (GET, POST, PUT, PATCH, DELETE)
- Status code usage and error response patterns
- Pagination, filtering, and sorting strategies
- HATEOAS and API discoverability

### GraphQL API Design
- Schema design and type system
- Query and mutation patterns
- Resolver optimization and N+1 query prevention
- Subscription design for real-time updates
- Error handling and partial responses

### API Versioning
- Versioning strategies (URL, header, content negotiation)
- Deprecation policies and migration paths
- Backward compatibility considerations
- Semantic versioning for APIs

### Authentication & Authorization
- OAuth 2.0 and OpenID Connect patterns
- API key management
- JWT token design and validation
- Rate limiting and throttling

## Quick Start

### REST API Example

```javascript
// Express.js REST API with proper conventions
const express = require('express');
const app = express();

// Resource-based routes
app.get('/api/v1/users', listUsers);           // List collection
app.post('/api/v1/users', createUser);         // Create resource
app.get('/api/v1/users/:id', getUser);         // Get single resource
app.put('/api/v1/users/:id', updateUser);      // Full update
app.patch('/api/v1/users/:id', partialUpdate); // Partial update
app.delete('/api/v1/users/:id', deleteUser);   // Delete resource

// Proper error response
function errorResponse(res, statusCode, message) {
  res.status(statusCode).json({
    error: {
      message,
      code: statusCode,
      timestamp: new Date().toISOString()
    }
  });
}
```

### GraphQL API Example

```javascript
// Apollo Server GraphQL schema
const { ApolloServer, gql } = require('apollo-server');

const typeDefs = gql`
  type User {
    id: ID!
    email: String!
    name: String
    posts: [Post!]!
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    author: User!
  }

  type Query {
    user(id: ID!): User
    users(limit: Int, offset: Int): [User!]!
  }

  type Mutation {
    createUser(email: String!, name: String): User!
    updateUser(id: ID!, name: String): User
  }
`;

const resolvers = {
  Query: {
    user: (_, { id }) => getUserById(id),
    users: (_, { limit = 10, offset = 0 }) => getUsers(limit, offset)
  },
  Mutation: {
    createUser: (_, { email, name }) => createUser(email, name)
  }
};
```

## Primary Tools & Technologies

- **REST Frameworks**: Express.js, FastAPI, Django REST Framework, Spring Boot
- **GraphQL Tools**: Apollo Server, GraphQL Yoga, Hasura
- **Documentation**: Swagger/OpenAPI, GraphQL Playground, Postman
- **Validation**: JSON Schema, Zod, Joi, GraphQL type system
- **Testing**: Postman, Insomnia, REST Client, GraphQL testing libraries

## Related Skills

- [Designing SDKs](./designing-sdks) - Create client SDKs for your APIs
- [Generating Documentation](./generating-documentation) - Auto-generate API documentation
- [Building CLIs](./building-clis) - Build CLI tools that interact with APIs
- [Debugging Techniques](./debugging-techniques) - Debug API issues and trace requests

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/api-design-principles)
- [Master Plan](../../master-plans/developer-productivity/designing-apis)
