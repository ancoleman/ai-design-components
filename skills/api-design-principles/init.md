# API Design Principles Skill - Master Plan

**Skill Name:** `api-design-principles`
**Skill Level:** High Level (8,000-12,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [API Design Taxonomy](#api-design-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [RESTful Design Patterns](#restful-design-patterns)
7. [GraphQL Design Patterns](#graphql-design-patterns)
8. [API Versioning Strategies](#api-versioning-strategies)
9. [Error Handling Standards](#error-handling-standards)
10. [Pagination Patterns](#pagination-patterns)
11. [Rate Limiting Design](#rate-limiting-design)
12. [OpenAPI Specification Examples](#openapi-specification-examples)
13. [AsyncAPI Specification Examples](#asyncapi-specification-examples)
14. [API Security Design](#api-security-design)
15. [Tool Recommendations](#tool-recommendations)
16. [Skill Structure Design](#skill-structure-design)
17. [Integration Points](#integration-points)
18. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

In 2025, APIs are the connective tissue of modern software. Every microservice, mobile app, SaaS integration, and AI agent relies on well-designed APIs. Poor API design leads to:
- **Integration friction** (developers spend weeks on what should take hours)
- **Breaking changes** (versioning nightmares that break production)
- **Security vulnerabilities** (injection attacks, unauthorized access)
- **Performance issues** (N+1 queries, excessive payloads)
- **Poor developer experience** (cryptic errors, missing documentation)

**Market Drivers:**
- **API-First Development**: Designing APIs before applications ensures scalability and integration readiness
- **Multi-Client Reality**: Web, mobile, IoT, AI agents all consume the same APIs
- **Third-Party Integrations**: Partner APIs require stable, well-documented contracts
- **Microservices Architecture**: Internal service communication depends on API consistency
- **AI Integration**: LLMs increasingly consume APIs through function calling (tool use)

**Strategic Value:**
1. **Foundation Skill**: API design principles apply across all protocols (REST, GraphQL, gRPC)
2. **Language Agnostic**: Patterns work in any backend language
3. **Reduces Technical Debt**: Good design prevents costly rewrites
4. **Improves Developer Experience**: Clear APIs = faster integrations

### How This Differs from Existing Solutions

**Existing API Documentation:**
- **Tool-Specific**: OpenAPI OR GraphQL OR gRPC docs, not unified
- **Implementation-Focused**: "How to write code" vs "How to design APIs"
- **Lacks Decision Guidance**: No framework for choosing REST vs GraphQL
- **Missing Security Patterns**: Authentication mentioned but not architectural

**Our Approach:**
- **Decision Frameworks**: When to use REST vs GraphQL vs WebSockets
- **Multi-Protocol Coverage**: RESTful, GraphQL, event-driven (AsyncAPI)
- **Security by Design**: OAuth2, scopes, rate limiting as core patterns
- **Real-World Examples**: OpenAPI 3.1 and AsyncAPI specs with working code
- **Breaking Change Management**: Versioning strategies with migration patterns

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **RESTful API Design**
   - Resource-oriented design (nouns, not verbs)
   - HTTP method semantics (GET, POST, PUT, PATCH, DELETE)
   - Status code selection (2xx, 4xx, 5xx)
   - HATEOAS and hypermedia controls (when appropriate)

2. **API Versioning**
   - URL path versioning (`/v1/`, `/v2/`)
   - Header-based versioning (`Accept-Version`)
   - Media type versioning (`application/vnd.api.v2+json`)
   - Breaking change management and deprecation policies

3. **Error Response Standards**
   - RFC 7807 Problem Details for HTTP APIs
   - Consistent error structures across endpoints
   - Meaningful error codes and messages
   - Validation error patterns

4. **Pagination Patterns**
   - Offset-based pagination (simple but slow at scale)
   - Cursor-based pagination (efficient for streams)
   - Keyset pagination (best for sorted data)
   - Pagination metadata (`next`, `prev`, `total`)

5. **Rate Limiting**
   - Token bucket algorithm
   - Rate limit headers (`X-RateLimit-*`)
   - Quota management (per user, per API key)
   - Throttling strategies (reject vs queue)

6. **API Documentation**
   - OpenAPI 3.1 specification (REST APIs)
   - AsyncAPI specification (event-driven APIs)
   - Schema validation and code generation
   - Interactive documentation (Swagger UI, Redoc)

7. **GraphQL Design**
   - Schema design principles
   - Query vs Mutation vs Subscription
   - N+1 query problem and DataLoader pattern
   - Schema stitching and federation

8. **API Security Design**
   - OAuth 2.0 flows (authorization code, client credentials)
   - API key management
   - Scope-based authorization
   - CORS and CSP headers

### What This Skill Does NOT Cover

- **Implementation code** (use `api-patterns` skill for Express, FastAPI, etc.)
- **Authentication implementation** (use `auth-security` skill for JWT, session management)
- **Database optimization** (use `database-design` skill)
- **API testing** (use `testing-strategies` skill)
- **API deployment** (use `deploying-applications` skill)

**Boundary Example:**
- ✅ This skill: "Use RFC 7807 for error responses with `type`, `title`, `detail`, `status`"
- ❌ Not this skill: "Here's Express middleware to implement RFC 7807 errors"

---

## Research Findings

### Google Search Grounding (December 2025)

#### REST API Best Practices (2025)

**Key Findings:**
- **Resource-oriented design** remains foundational (use nouns: `/users`, not `/getUsers`)
- **HTTP method semantics** critical for RESTful APIs (GET for read, POST for create, etc.)
- **Status codes** communicate intent (2xx success, 4xx client error, 5xx server error)
- **API versioning** essential for evolution (URL path most common)
- **Pagination and filtering** optimize data retrieval and reduce payload size
- **HATEOAS** decouples client from URI structure (but adds complexity)
- **Comprehensive error handling** with meaningful messages improves DX
- **Rate limiting** protects APIs from abuse
- **Statelessness** improves scalability
- **Caching** (ETags, Cache-Control) reduces server load

**Source:** docuwriter.ai, refgrow.com, zemith.com, microsoft.com

#### API Versioning Strategies (2025)

**Why Versioning Matters:**
- **Backward compatibility**: New versions coexist with old versions
- **Evolving requirements**: Structured way to incorporate changes
- **Multiple clients**: Different clients may need different API capabilities
- **Controlled rollouts**: Gradual migration reduces risk

**Common Strategies:**

1. **URI Path Versioning** (Most Popular)
   - Format: `/v1/resource`, `/api/v2/resource`
   - **Pros**: Clear, visible, easy to implement, simplifies testing
   - **Cons**: Maintenance overhead as versions increase

2. **Query Parameter Versioning**
   - Format: `/resource?version=1`
   - **Pros**: Flexible, clients specify version
   - **Cons**: Can be messy, less intuitive

3. **Header-Based Versioning**
   - Format: `Accept-Version: v1` or `X-API-Version: 2`
   - **Pros**: Clean URLs, RESTful principles
   - **Cons**: More setup, less transparent

4. **Media Type Versioning**
   - Format: `Accept: application/vnd.example.v1+json`
   - **Pros**: Aligns with content negotiation
   - **Cons**: Complex, requires Accept header parsing

5. **Semantic Versioning**
   - Format: `Major.Minor.Patch` (e.g., `2.1.3`)
   - **Breaking changes**: Increment Major
   - **New features**: Increment Minor
   - **Bug fixes**: Increment Patch

**Best Practices for Breaking Changes:**
- **Deprecation policy**: Clear timelines (announce → migrate → remove)
- **Migration guides**: Step-by-step instructions for every breaking change
- **Migration tools**: Scripts or SDK updates to assist consumers
- **Monitoring**: Track usage of old versions
- **Direct engagement**: Reach out to high-traffic partners
- **Error handling**: Return 406 Not Acceptable for unsupported versions

**2025 Trends:**
- **API-first development**: Design APIs before applications
- **AI/ML integration**: APIs infused with AI capabilities
- **Zero-trust architecture**: Security embedded in API lifecycle
- **API standardization**: Industry-specific standards for interoperability
- **API productization**: Packaging APIs for external revenue

**Source:** docuwriter.ai, api7.ai, refgrow.com, apidog.com, dreamfactory.com, redocly.com, measureone.com, itsecurityguru.org

#### GraphQL vs REST (2025)

**Note:** Google Search encountered errors for GraphQL queries. Relying on established patterns.

**REST Advantages:**
- Simple, well-understood HTTP semantics
- Caching built-in (HTTP caching headers)
- Stateless, scales horizontally
- Mature tooling ecosystem

**GraphQL Advantages:**
- Client-specified queries (no over-fetching)
- Single endpoint for all data
- Strongly typed schema
- Real-time subscriptions

**When to Choose:**
- **REST**: Public APIs, simple CRUD, caching critical, diverse clients
- **GraphQL**: Complex data graphs, mobile apps (bandwidth concerns), rapid iteration

### Context7 Library Research (December 2025)

#### OpenAPI Specification (Primary)

**Library:** `/oai/openapi-specification`
**Trust Score:** N/A (Official specification)
**Code Snippets:** 2,230+
**Benchmark Score:** 76.6
**Versions:** 3.0.4, 3.1.1

**Key Insights:**
- OpenAPI 3.1 fully compatible with JSON Schema Draft 2020-12
- Schema Object supports primitives, objects, arrays with validation
- Discriminator enables polymorphism
- Examples vs `example` field (examples preferred)
- Parameter serialization with `style` and `explode`

**Primitive Data Types:**

| Type | `type` | `format` | Comments |
|------|--------|----------|----------|
| integer | `integer` | `int32` | signed 32 bits |
| long | `integer` | `int64` | signed 64 bits |
| float | `number` | `float` | |
| double | `number` | `double` | |
| string | `string` | | |
| byte | `string` | `byte` | |
| boolean | `boolean` | | |
| date | `string` | `date` | |
| dateTime | `string` | `date-time` | |

**Source:** Context7 - /oai/openapi-specification

#### AsyncAPI Specification (Event-Driven APIs)

**Library:** `/asyncapi/spec`
**Trust Score:** N/A (Official specification)
**Code Snippets:** 72
**Source Reputation:** High

**Key Insights:**
- AsyncAPI defines machine-readable interfaces for asynchronous APIs
- Supports WebSockets, Kafka, MQTT, AMQP, and more
- Schema definitions similar to OpenAPI (JSON Schema based)
- Channel parameters for dynamic routing
- Server/Channel/Message bindings for protocol-specific details
- Polymorphic schemas using discriminator pattern

**AsyncAPI Components:**
- **Servers**: Connection details (protocol, host, variables)
- **Channels**: Message routes (pub/sub topics, queue names)
- **Messages**: Payload schemas and headers
- **Schemas**: Reusable data models
- **Parameters**: Dynamic channel addressing

**Source:** Context7 - /asyncapi/spec

---

## API Design Taxonomy

### Tier 1: Synchronous Request-Response APIs

#### REST (Representational State Transfer)

**Use When:**
- Public-facing APIs with diverse clients
- CRUD operations on resources
- Caching is critical (HTTP caching)
- Simple, predictable patterns needed
- Client doesn't control data shape

**Core Principles:**
- **Resource-oriented**: Use nouns (`/users`, `/orders`)
- **HTTP methods**: GET (read), POST (create), PUT (replace), PATCH (update), DELETE (remove)
- **Status codes**: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error
- **Stateless**: Each request contains all context
- **HATEOAS**: Include links to related resources (optional, adds complexity)

**Example REST Endpoint:**
```http
GET /api/v1/users/123
Authorization: Bearer <token>
Accept: application/json

200 OK
Content-Type: application/json
Cache-Control: max-age=3600

{
  "id": "123",
  "username": "alice",
  "email": "alice@example.com",
  "createdAt": "2025-01-15T10:30:00Z",
  "_links": {
    "self": { "href": "/api/v1/users/123" },
    "posts": { "href": "/api/v1/users/123/posts" },
    "followers": { "href": "/api/v1/users/123/followers" }
  }
}
```

#### GraphQL

**Use When:**
- Complex, interconnected data models
- Mobile apps (minimize over-fetching)
- Clients need flexible data queries
- Rapid frontend iteration required
- Real-time subscriptions needed

**Core Principles:**
- **Single endpoint**: `/graphql` for all queries
- **Client-specified queries**: Request exactly the data you need
- **Strongly typed schema**: Type system defines API contract
- **Introspection**: Schema is queryable
- **Batching**: Multiple queries in one request

**Example GraphQL Query:**
```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    username
    email
    posts(limit: 10) {
      id
      title
      createdAt
    }
    followers(limit: 5) {
      id
      username
    }
  }
}
```

**Response:**
```json
{
  "data": {
    "user": {
      "id": "123",
      "username": "alice",
      "email": "alice@example.com",
      "posts": [
        { "id": "1", "title": "First Post", "createdAt": "2025-01-10T08:00:00Z" }
      ],
      "followers": [
        { "id": "456", "username": "bob" }
      ]
    }
  }
}
```

### Tier 2: Asynchronous Event-Driven APIs

#### WebSockets (Real-Time Bidirectional)

**Use When:**
- Real-time updates required (chat, notifications)
- Low-latency communication needed
- Bidirectional communication (server can push)
- Long-lived connections acceptable

**Core Principles:**
- **Persistent connection**: Single TCP connection
- **Bidirectional**: Client and server send messages
- **Low overhead**: No HTTP header per message
- **Stateful**: Connection maintains state

**Example WebSocket (AsyncAPI):**
```yaml
asyncapi: 3.0.0
info:
  title: Chat API
  version: 1.0.0
servers:
  production:
    host: chat.example.com
    protocol: wss
channels:
  chat/messages:
    address: chat/messages
    messages:
      chatMessage:
        payload:
          type: object
          properties:
            userId:
              type: string
            message:
              type: string
            timestamp:
              type: string
              format: date-time
```

#### Message Queues (Kafka, RabbitMQ, AMQP)

**Use When:**
- Decoupled microservices communication
- Event sourcing and CQRS patterns
- High-throughput message processing
- Guaranteed delivery required

**Core Principles:**
- **Publish-subscribe**: Producers publish, consumers subscribe
- **Topics/queues**: Message routing
- **Durability**: Messages persisted until consumed
- **Ordering**: Messages processed in order (per partition/queue)

**Example Kafka Topic (AsyncAPI):**
```yaml
asyncapi: 3.0.0
info:
  title: Order Processing API
  version: 1.0.0
servers:
  kafka:
    host: kafka.example.com:9092
    protocol: kafka
channels:
  orders/created:
    address: orders.created
    messages:
      orderCreated:
        payload:
          type: object
          properties:
            orderId:
              type: string
            userId:
              type: string
            items:
              type: array
              items:
                type: object
                properties:
                  productId:
                    type: string
                  quantity:
                    type: integer
            totalAmount:
              type: number
```

### Tier 3: RPC-Style APIs

#### gRPC (HTTP/2, Protocol Buffers)

**Use When:**
- Internal microservice communication
- High performance required (binary protocol)
- Strong typing and code generation needed
- Streaming (bidirectional) required

**Core Principles:**
- **Binary protocol**: More efficient than JSON
- **HTTP/2**: Multiplexing, streaming
- **Protocol Buffers**: Strongly typed schema
- **Code generation**: Client/server stubs

**Not covered in detail** (out of scope - use `grpc-patterns` skill)

---

## Decision Frameworks

### Framework 1: Which API Style?

```
START: What type of API do you need?
  │
  ├─► Public API for third-party developers?
  │     YES ──► REST (widest compatibility, best tooling)
  │
  ├─► Complex data with many relationships?
  │     YES ──► GraphQL (client-controlled queries, flexible)
  │
  ├─► Real-time bidirectional communication?
  │     YES ──► WebSockets (low latency, persistent connection)
  │
  ├─► Event-driven, decoupled microservices?
  │     YES ──► Message Queue (Kafka, RabbitMQ)
  │
  ├─► Internal services, high performance?
  │     YES ──► gRPC (binary, HTTP/2, code generation)
  │
  └─► Simple CRUD, caching important?
        YES ──► REST (HTTP caching, stateless, simple)
```

### Framework 2: API Versioning Strategy Selection

| Factor | URL Path | Header | Media Type | Query Param |
|--------|----------|--------|------------|-------------|
| **Visibility** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **Simplicity** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **RESTful** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Caching** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Best For** | Most APIs | Internal APIs | Content negotiation | Prototyping |

**Recommendation:** URL path versioning (`/v1/`, `/v2/`) for most APIs due to simplicity and visibility.

### Framework 3: Pagination Strategy Selection

| Scenario | Strategy | Why |
|----------|----------|-----|
| Small datasets (<1000 items) | Offset-based | Simple, predictable page numbers |
| Large datasets (>10K items) | Cursor-based | Efficient, handles concurrent writes |
| Sorted data (e.g., leaderboard) | Keyset pagination | Consistent results, no skipped items |
| Real-time feeds (Twitter-like) | Cursor-based | Handles new items between requests |
| Admin panels (paginated tables) | Offset-based | Users expect page numbers |

### Framework 4: Error Response Selection

| Scenario | Use |
|----------|-----|
| **Standard REST errors** | RFC 7807 Problem Details |
| **Validation errors** | RFC 7807 with `errors` array |
| **GraphQL errors** | `errors` array in response |
| **WebSocket errors** | Error event with error code |
| **Legacy APIs** | Simple `{ "error": "message" }` (migrate to RFC 7807) |

---

## RESTful Design Patterns

### Pattern 1: Resource Naming

**Principles:**
- Use **nouns**, not verbs (`/users`, not `/getUsers`)
- Use **plural nouns** for collections (`/users`, not `/user`)
- Use **kebab-case** for multi-word resources (`/user-profiles`)
- Nest resources for relationships (`/users/123/posts`)
- Limit nesting to 2-3 levels (`/users/123/posts/456/comments` - OK)

**Good Examples:**
```
GET    /users                    # List all users
GET    /users/123                # Get user 123
POST   /users                    # Create new user
PUT    /users/123                # Replace user 123
PATCH  /users/123                # Update user 123
DELETE /users/123                # Delete user 123
GET    /users/123/posts          # List posts by user 123
GET    /users/123/followers      # List followers of user 123
```

**Bad Examples:**
```
❌ GET  /getUsers                # Verb in URL
❌ GET  /user/123                # Singular noun
❌ POST /users/create            # Redundant verb
❌ GET  /UserProfiles            # CamelCase
❌ GET  /users/123/posts/456/comments/789/replies  # Too deep
```

### Pattern 2: HTTP Method Semantics

| Method | Idempotent? | Safe? | Use Case | Success Status |
|--------|-------------|-------|----------|----------------|
| **GET** | Yes | Yes | Retrieve resource | 200 OK |
| **POST** | No | No | Create resource | 201 Created |
| **PUT** | Yes | No | Replace resource | 200 OK or 204 No Content |
| **PATCH** | No | No | Partial update | 200 OK or 204 No Content |
| **DELETE** | Yes | No | Remove resource | 204 No Content or 200 OK |
| **HEAD** | Yes | Yes | Get metadata only | 200 OK |
| **OPTIONS** | Yes | Yes | Get allowed methods | 200 OK |

**Idempotent:** Multiple identical requests have the same effect as one request.
**Safe:** Request does not modify server state.

**PUT vs PATCH:**
- **PUT**: Replace entire resource (send all fields)
- **PATCH**: Update specific fields (send only changed fields)

**Example PUT:**
```http
PUT /api/v1/users/123
Content-Type: application/json

{
  "username": "alice",
  "email": "alice@newdomain.com",
  "bio": "Updated bio"
}
```

**Example PATCH:**
```http
PATCH /api/v1/users/123
Content-Type: application/json

{
  "email": "alice@newdomain.com"
}
```

### Pattern 3: HTTP Status Codes

**Success Codes (2xx):**
- **200 OK**: Request succeeded, response body included
- **201 Created**: Resource created, include `Location` header
- **202 Accepted**: Request accepted for async processing
- **204 No Content**: Request succeeded, no response body

**Client Error Codes (4xx):**
- **400 Bad Request**: Invalid syntax or validation error
- **401 Unauthorized**: Authentication required or failed
- **403 Forbidden**: Authenticated but not authorized
- **404 Not Found**: Resource doesn't exist
- **405 Method Not Allowed**: HTTP method not supported
- **406 Not Acceptable**: Cannot produce requested content type
- **409 Conflict**: Request conflicts with current state
- **410 Gone**: Resource permanently deleted
- **422 Unprocessable Entity**: Valid syntax but semantic errors
- **429 Too Many Requests**: Rate limit exceeded

**Server Error Codes (5xx):**
- **500 Internal Server Error**: Generic server error
- **502 Bad Gateway**: Invalid response from upstream
- **503 Service Unavailable**: Server temporarily unavailable
- **504 Gateway Timeout**: Upstream server timeout

**Example:**
```http
POST /api/v1/users
Content-Type: application/json

{
  "username": "alice",
  "email": "invalid-email"
}

400 Bad Request
Content-Type: application/problem+json

{
  "type": "https://example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "One or more fields failed validation",
  "errors": [
    {
      "field": "email",
      "message": "Must be a valid email address"
    }
  ]
}
```

### Pattern 4: Filtering, Sorting, Searching

**Query Parameters for Data Operations:**

**Filtering:**
```http
GET /api/v1/users?status=active&role=admin
GET /api/v1/posts?authorId=123&published=true
```

**Sorting:**
```http
GET /api/v1/users?sort=createdAt:desc
GET /api/v1/posts?sort=title:asc,createdAt:desc  # Multiple sorts
```

**Searching:**
```http
GET /api/v1/users?q=alice
GET /api/v1/posts?search=api+design
```

**Field Selection (Sparse Fieldsets):**
```http
GET /api/v1/users?fields=id,username,email
```

**Combining:**
```http
GET /api/v1/users?status=active&sort=createdAt:desc&fields=id,username&limit=20
```

### Pattern 5: HATEOAS (Hypermedia)

**When to Use:**
- API evolution without breaking clients
- Clients navigate API dynamically
- Workflow-driven applications

**When to Skip:**
- Mobile apps (bandwidth concerns)
- Simple CRUD APIs
- Clients hardcode URLs anyway

**Example with HATEOAS:**
```json
{
  "id": "123",
  "username": "alice",
  "email": "alice@example.com",
  "_links": {
    "self": { "href": "/api/v1/users/123" },
    "posts": { "href": "/api/v1/users/123/posts" },
    "followers": { "href": "/api/v1/users/123/followers" },
    "follow": {
      "href": "/api/v1/users/123/followers",
      "method": "POST"
    }
  }
}
```

---

## GraphQL Design Patterns

### Pattern 1: Schema Design Principles

**Type System:**
```graphql
# Scalar types
type User {
  id: ID!           # Non-null ID
  username: String!
  email: String!
  bio: String       # Nullable
  createdAt: DateTime!
}

# Object relationships
type Post {
  id: ID!
  title: String!
  content: String!
  author: User!     # Relationship
  comments: [Comment!]!  # List of comments
}

# Enums
enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

# Input types
input CreateUserInput {
  username: String!
  email: String!
  password: String!
}
```

**Query vs Mutation:**
```graphql
type Query {
  # Read operations
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
  post(id: ID!): Post
}

type Mutation {
  # Write operations
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

type Subscription {
  # Real-time updates
  postCreated: Post!
  userStatusChanged(userId: ID!): User!
}
```

### Pattern 2: N+1 Query Problem and DataLoader

**Problem:**
```graphql
query {
  posts {           # 1 query: Get all posts
    id
    title
    author {        # N queries: Get author for each post (BAD!)
      username
    }
  }
}
```

**Solution: DataLoader (Batching)**
```javascript
// DataLoader batches requests
const userLoader = new DataLoader(async (userIds) => {
  // Single query for all users
  const users = await db.users.findByIds(userIds);
  return userIds.map(id => users.find(u => u.id === id));
});

// Resolver uses loader
const resolvers = {
  Post: {
    author: (post) => userLoader.load(post.authorId)
  }
};
```

### Pattern 3: Pagination in GraphQL

**Cursor-Based (Relay Specification):**
```graphql
type Query {
  users(
    first: Int
    after: String
    last: Int
    before: String
  ): UserConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  cursor: String!
  node: User!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

**Query Example:**
```graphql
query {
  users(first: 10, after: "cursor123") {
    edges {
      cursor
      node {
        id
        username
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Pattern 4: Error Handling in GraphQL

**GraphQL Response Structure:**
```json
{
  "data": { ... },     # Successful data
  "errors": [ ... ]    # Errors array
}
```

**Partial Success Example:**
```json
{
  "data": {
    "user": {
      "id": "123",
      "username": "alice",
      "posts": null       # Failed to load posts
    }
  },
  "errors": [
    {
      "message": "Failed to fetch posts",
      "path": ["user", "posts"],
      "extensions": {
        "code": "DATABASE_ERROR",
        "timestamp": "2025-12-03T10:30:00Z"
      }
    }
  ]
}
```

---

## API Versioning Strategies

### Strategy 1: URL Path Versioning (Recommended)

**Format:**
```
https://api.example.com/v1/users
https://api.example.com/v2/users
```

**Pros:**
- ✅ Highly visible and explicit
- ✅ Easy to implement and test
- ✅ Works with all HTTP clients
- ✅ Simplifies caching (different URLs)
- ✅ Clear in documentation and logs

**Cons:**
- ❌ Not strictly RESTful (resource identity changes)
- ❌ Maintenance overhead (multiple codebases)

**Implementation:**
```javascript
// Express.js example structure
app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

// v1Router
router.get('/users', (req, res) => {
  // v1 implementation
});

// v2Router
router.get('/users', (req, res) => {
  // v2 implementation with breaking changes
});
```

### Strategy 2: Header-Based Versioning

**Format:**
```http
GET /api/users
Accept-Version: v1
```

or

```http
GET /api/users
X-API-Version: 2
```

**Pros:**
- ✅ Clean URLs (resource identity preserved)
- ✅ RESTful principles
- ✅ Supports content negotiation

**Cons:**
- ❌ Less visible (hidden in headers)
- ❌ Harder to test in browser
- ❌ Requires header parsing logic

**Implementation:**
```javascript
app.use((req, res, next) => {
  const version = req.headers['accept-version'] || 'v1';
  req.apiVersion = version;
  next();
});

router.get('/users', (req, res) => {
  if (req.apiVersion === 'v2') {
    // v2 implementation
  } else {
    // v1 implementation
  }
});
```

### Strategy 3: Media Type Versioning

**Format:**
```http
GET /api/users
Accept: application/vnd.example.v1+json
```

**Pros:**
- ✅ True content negotiation
- ✅ RESTful principles
- ✅ Allows multiple representations

**Cons:**
- ❌ Complex implementation
- ❌ Requires proper Accept header handling
- ❌ Less discoverable

### Strategy 4: Query Parameter Versioning

**Format:**
```
https://api.example.com/users?version=1
```

**Pros:**
- ✅ Easy to test
- ✅ Visible in URL

**Cons:**
- ❌ Clutters query string
- ❌ Not RESTful
- ❌ Complicates caching

**Use Only For:** Prototyping or internal APIs

### Breaking Change Management

**Deprecation Timeline:**
```
Month 0: Announce deprecation
  - Add deprecation warnings to API responses
  - Update documentation
  - Notify all API consumers

Month 1-3: Migration period
  - Provide migration guide
  - Offer support for migration
  - Monitor usage of old version

Month 4-6: Deprecation warnings
  - Return deprecation headers
  - Log usage for proactive outreach

Month 6: Sunset
  - Remove old version
  - Return 410 Gone for old endpoints
```

**Deprecation Headers:**
```http
GET /api/v1/users
Deprecation: true
Sunset: Sat, 31 Dec 2025 23:59:59 GMT
Link: </api/v2/users>; rel="successor-version"
```

**Example Migration Guide:**
```markdown
# Migration Guide: v1 to v2

## Breaking Changes

### 1. User `name` field split into `firstName` and `lastName`

**v1:**
```json
{ "name": "Alice Smith" }
```

**v2:**
```json
{ "firstName": "Alice", "lastName": "Smith" }
```

**Migration:** Split `name` field on client side until v2 adoption.

### 2. Date format changed from Unix timestamp to ISO 8601

**v1:** `"createdAt": 1609459200`
**v2:** `"createdAt": "2021-01-01T00:00:00Z"`

**Migration:** Update date parsing logic.
```

---

## Error Handling Standards

### RFC 7807: Problem Details for HTTP APIs

**Standard Structure:**
```json
{
  "type": "https://example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "One or more fields failed validation",
  "instance": "/api/v1/users",
  "errors": [
    {
      "field": "email",
      "message": "Must be a valid email address",
      "code": "INVALID_EMAIL"
    },
    {
      "field": "username",
      "message": "Username already exists",
      "code": "DUPLICATE_USERNAME"
    }
  ]
}
```

**Field Definitions:**
- **type**: URI identifying the error type (should be dereferenceable documentation)
- **title**: Short, human-readable summary
- **status**: HTTP status code
- **detail**: Human-readable explanation specific to this occurrence
- **instance**: URI identifying the specific occurrence
- **errors**: (Extension) Array of validation errors

### Error Response Patterns

**Validation Error (400):**
```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Failed",
  "status": 400,
  "detail": "Request body contains invalid fields",
  "errors": [
    {
      "field": "email",
      "message": "Must be a valid email",
      "code": "INVALID_FORMAT"
    }
  ]
}
```

**Unauthorized (401):**
```json
{
  "type": "https://api.example.com/errors/unauthorized",
  "title": "Authentication Required",
  "status": 401,
  "detail": "Valid authentication credentials are required"
}
```

**Forbidden (403):**
```json
{
  "type": "https://api.example.com/errors/forbidden",
  "title": "Insufficient Permissions",
  "status": 403,
  "detail": "You do not have permission to access this resource",
  "requiredScope": "admin:write"
}
```

**Not Found (404):**
```json
{
  "type": "https://api.example.com/errors/not-found",
  "title": "Resource Not Found",
  "status": 404,
  "detail": "User with id '123' does not exist"
}
```

**Rate Limit Exceeded (429):**
```json
{
  "type": "https://api.example.com/errors/rate-limit",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "You have exceeded the rate limit of 100 requests per hour",
  "retryAfter": 3600
}
```

**Internal Server Error (500):**
```json
{
  "type": "https://api.example.com/errors/internal",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred. Please try again later.",
  "traceId": "abc123-def456"
}
```

---

## Pagination Patterns

### Pattern 1: Offset-Based Pagination

**Use Case:** Small to medium datasets, user expects page numbers

**Query Parameters:**
```http
GET /api/v1/users?limit=20&offset=40
```

**Response:**
```json
{
  "data": [ ... ],
  "pagination": {
    "limit": 20,
    "offset": 40,
    "total": 1543,
    "totalPages": 78,
    "currentPage": 3
  }
}
```

**Pros:**
- ✅ Simple to implement
- ✅ Predictable (jump to page N)
- ✅ Works with SQL: `LIMIT 20 OFFSET 40`

**Cons:**
- ❌ Slow for large offsets (database scans)
- ❌ Inconsistent results if data changes (items skipped/duplicated)

### Pattern 2: Cursor-Based Pagination

**Use Case:** Large datasets, real-time feeds, consistent results

**Query Parameters:**
```http
GET /api/v1/users?limit=20&cursor=eyJpZCI6MTIzfQ==
```

**Response:**
```json
{
  "data": [ ... ],
  "pagination": {
    "nextCursor": "eyJpZCI6MTQzfQ==",
    "prevCursor": "eyJpZCI6MTAzfQ==",
    "hasNext": true,
    "hasPrev": true
  }
}
```

**Cursor Encoding:**
```javascript
// Cursor is base64-encoded JSON
const cursor = { id: 123, timestamp: "2025-12-03T10:00:00Z" };
const encodedCursor = Buffer.from(JSON.stringify(cursor)).toString('base64');
// Result: eyJpZCI6MTIzLCJ0aW1lc3RhbXAiOiIyMDI1LTEyLTAzVDEwOjAwOjAwWiJ9
```

**SQL Query:**
```sql
SELECT * FROM users
WHERE id > 123  -- Decoded from cursor
ORDER BY id ASC
LIMIT 20;
```

**Pros:**
- ✅ Efficient for large datasets (indexed queries)
- ✅ Consistent results (no skipped items)
- ✅ Handles concurrent writes

**Cons:**
- ❌ Can't jump to arbitrary page
- ❌ More complex implementation

### Pattern 3: Keyset Pagination

**Use Case:** Sorted data, consistent ordering required

**Query Parameters:**
```http
GET /api/v1/posts?limit=20&after_id=456&after_created_at=2025-12-03T10:00:00Z
```

**Response:**
```json
{
  "data": [ ... ],
  "pagination": {
    "nextId": 476,
    "nextCreatedAt": "2025-12-03T11:00:00Z",
    "hasNext": true
  }
}
```

**SQL Query:**
```sql
SELECT * FROM posts
WHERE (created_at, id) > ('2025-12-03T10:00:00Z', 456)
ORDER BY created_at ASC, id ASC
LIMIT 20;
```

**Pros:**
- ✅ Efficient (indexed columns)
- ✅ Stable results
- ✅ Works with complex sorting

**Cons:**
- ❌ Requires composite index
- ❌ More complex query logic

### Pagination Best Practices

1. **Include metadata:**
   - Total count (if feasible)
   - Has next/previous page
   - Cursors or page numbers

2. **Set reasonable limits:**
   - Default limit: 20-50 items
   - Max limit: 100-200 items
   - Prevent unlimited queries

3. **Link headers (optional):**
```http
Link: </api/v1/users?limit=20&cursor=abc123>; rel="next",
      </api/v1/users?limit=20&cursor=xyz789>; rel="prev"
```

4. **Consistent ordering:**
   - Always sort by a unique column (e.g., `id`)
   - Avoid ambiguous sorts (multiple rows with same value)

---

## Rate Limiting Design

### Token Bucket Algorithm

**Concept:**
- Each user has a bucket with tokens
- Each request consumes 1 token
- Tokens refill at a constant rate
- If bucket is empty, request is rejected

**Example:**
- Bucket capacity: 100 tokens
- Refill rate: 100 tokens per hour (1.67 tokens/minute)
- User makes 50 requests: 50 tokens left
- Wait 30 minutes: 50 tokens refilled (100 total)

### Rate Limit Headers

**Standard Headers:**
```http
X-RateLimit-Limit: 100           # Max requests per window
X-RateLimit-Remaining: 73        # Requests remaining
X-RateLimit-Reset: 1672531200    # Unix timestamp when limit resets
Retry-After: 3600                # Seconds until retry (for 429)
```

**Example Response:**
```http
GET /api/v1/users

200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 73
X-RateLimit-Reset: 1672531200

{ "data": [ ... ] }
```

**Rate Limit Exceeded:**
```http
GET /api/v1/users

429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1672531200
Retry-After: 3600

{
  "type": "https://api.example.com/errors/rate-limit",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "You have exceeded the rate limit of 100 requests per hour",
  "retryAfter": 3600
}
```

### Rate Limiting Strategies

**Per User:**
```
User 123: 100 requests/hour
User 456: 100 requests/hour
```

**Per API Key:**
```
API Key abc123: 1000 requests/hour
API Key xyz789: 1000 requests/hour
```

**Per IP Address:**
```
IP 1.2.3.4: 50 requests/hour (unauthenticated)
```

**Tiered Limits:**
```
Free tier:   100 requests/hour
Pro tier:    1000 requests/hour
Enterprise:  10000 requests/hour
```

**Endpoint-Specific:**
```
GET  /users:      100 requests/hour
POST /users:      10 requests/hour  (write operations limited)
GET  /search:     20 requests/hour  (expensive operations)
```

### Quota Management

**Monthly Quotas:**
```json
{
  "quota": {
    "limit": 10000,
    "used": 7453,
    "remaining": 2547,
    "resetAt": "2026-01-01T00:00:00Z"
  }
}
```

**Quota Headers:**
```http
X-Quota-Limit: 10000
X-Quota-Used: 7453
X-Quota-Remaining: 2547
X-Quota-Reset: 2026-01-01T00:00:00Z
```

---

## OpenAPI Specification Examples

### Complete OpenAPI 3.1 Example

```yaml
openapi: 3.1.0
info:
  title: User Management API
  version: 2.0.0
  description: |
    A comprehensive user management API demonstrating best practices for API design.

    ## Features
    - RESTful resource design
    - OAuth 2.0 authentication
    - Pagination support
    - Error handling with RFC 7807
    - Rate limiting
  contact:
    name: API Support
    email: api@example.com
    url: https://example.com/support
  license:
    name: Apache 2.0
    url: https://www.apache.org/licenses/LICENSE-2.0

servers:
  - url: https://api.example.com/v2
    description: Production server
  - url: https://staging-api.example.com/v2
    description: Staging server

security:
  - oauth2: []
  - apiKey: []

tags:
  - name: Users
    description: User management operations
  - name: Posts
    description: Blog post operations

paths:
  /users:
    get:
      summary: List users
      description: Retrieve a paginated list of users
      operationId: listUsers
      tags:
        - Users
      parameters:
        - name: limit
          in: query
          description: Maximum number of users to return
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: offset
          in: query
          description: Number of users to skip
          schema:
            type: integer
            minimum: 0
            default: 0
        - name: status
          in: query
          description: Filter by user status
          schema:
            type: string
            enum: [active, inactive, suspended]
        - name: sort
          in: query
          description: Sort field and order
          schema:
            type: string
            default: "createdAt:desc"
            example: "username:asc"
      responses:
        '200':
          description: Successful response
          headers:
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
            X-RateLimit-Remaining:
              $ref: '#/components/headers/X-RateLimit-Remaining'
            X-RateLimit-Reset:
              $ref: '#/components/headers/X-RateLimit-Reset'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '429':
          $ref: '#/components/responses/TooManyRequests'
        '500':
          $ref: '#/components/responses/InternalServerError'

    post:
      summary: Create user
      description: Create a new user account
      operationId: createUser
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created successfully
          headers:
            Location:
              description: URI of the created user
              schema:
                type: string
                format: uri
                example: /users/123
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '409':
          $ref: '#/components/responses/Conflict'

  /users/{userId}:
    parameters:
      - name: userId
        in: path
        required: true
        description: Unique identifier of the user
        schema:
          type: string
          format: uuid

    get:
      summary: Get user by ID
      description: Retrieve a specific user by their ID
      operationId: getUserById
      tags:
        - Users
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

    patch:
      summary: Update user
      description: Partially update a user's information
      operationId: updateUser
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUserRequest'
      responses:
        '200':
          description: User updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '404':
          $ref: '#/components/responses/NotFound'

    delete:
      summary: Delete user
      description: Permanently delete a user account
      operationId: deleteUser
      tags:
        - Users
      responses:
        '204':
          description: User deleted successfully
        '404':
          $ref: '#/components/responses/NotFound'

  /users/{userId}/posts:
    parameters:
      - name: userId
        in: path
        required: true
        schema:
          type: string
          format: uuid

    get:
      summary: List user's posts
      description: Retrieve all posts by a specific user
      operationId: listUserPosts
      tags:
        - Posts
      parameters:
        - $ref: '#/components/parameters/LimitParam'
        - $ref: '#/components/parameters/OffsetParam'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PostListResponse'

components:
  securitySchemes:
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/oauth/authorize
          tokenUrl: https://auth.example.com/oauth/token
          scopes:
            read:users: Read user information
            write:users: Create and update users
            delete:users: Delete users
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key

  headers:
    X-RateLimit-Limit:
      description: Maximum number of requests allowed per hour
      schema:
        type: integer
        example: 100
    X-RateLimit-Remaining:
      description: Number of requests remaining in current window
      schema:
        type: integer
        example: 73
    X-RateLimit-Reset:
      description: Unix timestamp when rate limit resets
      schema:
        type: integer
        format: int64
        example: 1672531200

  parameters:
    LimitParam:
      name: limit
      in: query
      description: Maximum number of items to return
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20
    OffsetParam:
      name: offset
      in: query
      description: Number of items to skip
      schema:
        type: integer
        minimum: 0
        default: 0

  schemas:
    User:
      type: object
      required:
        - id
        - username
        - email
        - status
        - createdAt
      properties:
        id:
          type: string
          format: uuid
          description: Unique identifier
          example: 123e4567-e89b-12d3-a456-426614174000
        username:
          type: string
          minLength: 3
          maxLength: 30
          pattern: '^[a-zA-Z0-9_-]+$'
          description: Unique username
          example: alice
        email:
          type: string
          format: email
          description: Email address
          example: alice@example.com
        firstName:
          type: string
          maxLength: 50
          example: Alice
        lastName:
          type: string
          maxLength: 50
          example: Smith
        bio:
          type: string
          maxLength: 500
          nullable: true
          example: Software engineer and API enthusiast
        status:
          type: string
          enum: [active, inactive, suspended]
          description: Account status
          example: active
        createdAt:
          type: string
          format: date-time
          description: Account creation timestamp
          example: '2025-01-15T10:30:00Z'
        updatedAt:
          type: string
          format: date-time
          description: Last update timestamp
          example: '2025-12-03T14:20:00Z'

    CreateUserRequest:
      type: object
      required:
        - username
        - email
        - password
      properties:
        username:
          type: string
          minLength: 3
          maxLength: 30
          pattern: '^[a-zA-Z0-9_-]+$'
        email:
          type: string
          format: email
        password:
          type: string
          minLength: 8
          format: password
        firstName:
          type: string
          maxLength: 50
        lastName:
          type: string
          maxLength: 50

    UpdateUserRequest:
      type: object
      properties:
        email:
          type: string
          format: email
        firstName:
          type: string
          maxLength: 50
        lastName:
          type: string
          maxLength: 50
        bio:
          type: string
          maxLength: 500

    UserListResponse:
      type: object
      required:
        - data
        - pagination
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      required:
        - limit
        - offset
        - total
      properties:
        limit:
          type: integer
          example: 20
        offset:
          type: integer
          example: 0
        total:
          type: integer
          example: 1543
        totalPages:
          type: integer
          example: 78
        currentPage:
          type: integer
          example: 1

    Post:
      type: object
      required:
        - id
        - title
        - authorId
        - status
        - createdAt
      properties:
        id:
          type: string
          format: uuid
        title:
          type: string
          maxLength: 200
        content:
          type: string
        authorId:
          type: string
          format: uuid
        status:
          type: string
          enum: [draft, published, archived]
        createdAt:
          type: string
          format: date-time

    PostListResponse:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Post'
        pagination:
          $ref: '#/components/schemas/Pagination'

    ProblemDetails:
      type: object
      required:
        - type
        - title
        - status
      properties:
        type:
          type: string
          format: uri
          description: URI identifying the problem type
          example: https://api.example.com/errors/validation
        title:
          type: string
          description: Short, human-readable summary
          example: Validation Error
        status:
          type: integer
          description: HTTP status code
          example: 400
        detail:
          type: string
          description: Human-readable explanation
          example: One or more fields failed validation
        instance:
          type: string
          format: uri
          description: URI identifying this specific occurrence
          example: /api/v2/users

    ValidationError:
      allOf:
        - $ref: '#/components/schemas/ProblemDetails'
        - type: object
          properties:
            errors:
              type: array
              items:
                type: object
                required:
                  - field
                  - message
                properties:
                  field:
                    type: string
                    example: email
                  message:
                    type: string
                    example: Must be a valid email address
                  code:
                    type: string
                    example: INVALID_FORMAT

  responses:
    BadRequest:
      description: Bad request - validation error
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/ValidationError'

    Unauthorized:
      description: Unauthorized - authentication required
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'
          example:
            type: https://api.example.com/errors/unauthorized
            title: Authentication Required
            status: 401
            detail: Valid authentication credentials are required

    NotFound:
      description: Not found - resource does not exist
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'
          example:
            type: https://api.example.com/errors/not-found
            title: Resource Not Found
            status: 404
            detail: The requested resource does not exist

    Conflict:
      description: Conflict - resource already exists
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'
          example:
            type: https://api.example.com/errors/conflict
            title: Resource Conflict
            status: 409
            detail: A user with this username already exists

    TooManyRequests:
      description: Too many requests - rate limit exceeded
      headers:
        X-RateLimit-Limit:
          $ref: '#/components/headers/X-RateLimit-Limit'
        X-RateLimit-Remaining:
          $ref: '#/components/headers/X-RateLimit-Remaining'
        X-RateLimit-Reset:
          $ref: '#/components/headers/X-RateLimit-Reset'
        Retry-After:
          description: Seconds until rate limit resets
          schema:
            type: integer
            example: 3600
      content:
        application/problem+json:
          schema:
            allOf:
              - $ref: '#/components/schemas/ProblemDetails'
              - type: object
                properties:
                  retryAfter:
                    type: integer
                    example: 3600
          example:
            type: https://api.example.com/errors/rate-limit
            title: Rate Limit Exceeded
            status: 429
            detail: You have exceeded the rate limit of 100 requests per hour
            retryAfter: 3600

    InternalServerError:
      description: Internal server error
      content:
        application/problem+json:
          schema:
            allOf:
              - $ref: '#/components/schemas/ProblemDetails'
              - type: object
                properties:
                  traceId:
                    type: string
                    example: abc123-def456
          example:
            type: https://api.example.com/errors/internal
            title: Internal Server Error
            status: 500
            detail: An unexpected error occurred
            traceId: abc123-def456
```

---

## AsyncAPI Specification Examples

### Complete AsyncAPI 3.0 Example

```yaml
asyncapi: 3.0.0

info:
  title: Order Processing Events API
  version: 1.0.0
  description: |
    Event-driven API for order processing using Kafka.

    ## Event Flow
    1. Order created → `orders.created` topic
    2. Payment processed → `orders.payment_completed` topic
    3. Order fulfilled → `orders.fulfilled` topic
    4. Order shipped → `orders.shipped` topic
  contact:
    name: Events Team
    email: events@example.com
  license:
    name: Apache 2.0
    url: https://www.apache.org/licenses/LICENSE-2.0

servers:
  production:
    host: kafka.example.com:9092
    protocol: kafka
    description: Production Kafka cluster
    security:
      - $ref: '#/components/securitySchemes/saslScram'

  staging:
    host: kafka-staging.example.com:9092
    protocol: kafka
    description: Staging Kafka cluster

channels:
  orders/created:
    address: orders.created
    description: Channel for order creation events
    messages:
      orderCreated:
        $ref: '#/components/messages/OrderCreated'
    bindings:
      kafka:
        topic: orders.created
        partitions: 10
        replicas: 3

  orders/payment_completed:
    address: orders.payment_completed
    description: Channel for payment completion events
    messages:
      paymentCompleted:
        $ref: '#/components/messages/PaymentCompleted'

  orders/fulfilled:
    address: orders.fulfilled
    description: Channel for order fulfillment events
    messages:
      orderFulfilled:
        $ref: '#/components/messages/OrderFulfilled'

  orders/shipped:
    address: orders.shipped
    description: Channel for order shipping events
    messages:
      orderShipped:
        $ref: '#/components/messages/OrderShipped'

operations:
  publishOrderCreated:
    action: send
    channel:
      $ref: '#/channels/orders~1created'
    summary: Publish order creation event
    description: Triggered when a new order is created in the system

  subscribeOrderCreated:
    action: receive
    channel:
      $ref: '#/channels/orders~1created'
    summary: Subscribe to order creation events
    description: Payment service subscribes to initiate payment processing

  publishPaymentCompleted:
    action: send
    channel:
      $ref: '#/channels/orders~1payment_completed'
    summary: Publish payment completion event

  subscribePaymentCompleted:
    action: receive
    channel:
      $ref: '#/channels/orders~1payment_completed'
    summary: Subscribe to payment completion events
    description: Fulfillment service subscribes to start order processing

components:
  securitySchemes:
    saslScram:
      type: scramSha256
      description: SASL/SCRAM authentication

  messages:
    OrderCreated:
      name: OrderCreated
      title: Order Created Event
      summary: Published when a new order is created
      contentType: application/json
      payload:
        $ref: '#/components/schemas/OrderCreatedPayload'
      examples:
        - name: StandardOrder
          summary: Standard order example
          payload:
            eventId: evt_123456
            eventType: order.created
            timestamp: '2025-12-03T10:30:00Z'
            version: 1
            data:
              orderId: ord_789012
              userId: usr_345678
              items:
                - productId: prd_111
                  quantity: 2
                  price: 29.99
              totalAmount: 59.98
              currency: USD
              status: pending_payment

    PaymentCompleted:
      name: PaymentCompleted
      title: Payment Completed Event
      summary: Published when payment is successfully processed
      contentType: application/json
      payload:
        $ref: '#/components/schemas/PaymentCompletedPayload'

    OrderFulfilled:
      name: OrderFulfilled
      title: Order Fulfilled Event
      summary: Published when order is prepared for shipping
      contentType: application/json
      payload:
        $ref: '#/components/schemas/OrderFulfilledPayload'

    OrderShipped:
      name: OrderShipped
      title: Order Shipped Event
      summary: Published when order is handed to carrier
      contentType: application/json
      payload:
        $ref: '#/components/schemas/OrderShippedPayload'

  schemas:
    OrderCreatedPayload:
      type: object
      required:
        - eventId
        - eventType
        - timestamp
        - version
        - data
      properties:
        eventId:
          type: string
          description: Unique event identifier
          example: evt_123456
        eventType:
          type: string
          const: order.created
        timestamp:
          type: string
          format: date-time
          description: Event creation timestamp (ISO 8601)
        version:
          type: integer
          description: Event schema version
          example: 1
        data:
          type: object
          required:
            - orderId
            - userId
            - items
            - totalAmount
            - currency
            - status
          properties:
            orderId:
              type: string
              description: Unique order identifier
              example: ord_789012
            userId:
              type: string
              description: User who created the order
              example: usr_345678
            items:
              type: array
              minItems: 1
              items:
                type: object
                required:
                  - productId
                  - quantity
                  - price
                properties:
                  productId:
                    type: string
                    example: prd_111
                  quantity:
                    type: integer
                    minimum: 1
                    example: 2
                  price:
                    type: number
                    format: float
                    minimum: 0
                    example: 29.99
            totalAmount:
              type: number
              format: float
              minimum: 0
              description: Total order amount
              example: 59.98
            currency:
              type: string
              enum: [USD, EUR, GBP]
              example: USD
            status:
              type: string
              enum: [pending_payment, paid, fulfilled, shipped, delivered, cancelled]
              example: pending_payment
            shippingAddress:
              $ref: '#/components/schemas/Address'

    PaymentCompletedPayload:
      type: object
      required:
        - eventId
        - eventType
        - timestamp
        - version
        - data
      properties:
        eventId:
          type: string
        eventType:
          type: string
          const: order.payment_completed
        timestamp:
          type: string
          format: date-time
        version:
          type: integer
        data:
          type: object
          required:
            - orderId
            - paymentId
            - amount
            - currency
            - paymentMethod
          properties:
            orderId:
              type: string
            paymentId:
              type: string
            amount:
              type: number
              format: float
            currency:
              type: string
            paymentMethod:
              type: string
              enum: [credit_card, debit_card, paypal, bank_transfer]

    OrderFulfilledPayload:
      type: object
      required:
        - eventId
        - eventType
        - timestamp
        - version
        - data
      properties:
        eventId:
          type: string
        eventType:
          type: string
          const: order.fulfilled
        timestamp:
          type: string
          format: date-time
        version:
          type: integer
        data:
          type: object
          required:
            - orderId
            - fulfilledAt
            - warehouseId
          properties:
            orderId:
              type: string
            fulfilledAt:
              type: string
              format: date-time
            warehouseId:
              type: string

    OrderShippedPayload:
      type: object
      required:
        - eventId
        - eventType
        - timestamp
        - version
        - data
      properties:
        eventId:
          type: string
        eventType:
          type: string
          const: order.shipped
        timestamp:
          type: string
          format: date-time
        version:
          type: integer
        data:
          type: object
          required:
            - orderId
            - trackingNumber
            - carrier
            - shippedAt
          properties:
            orderId:
              type: string
            trackingNumber:
              type: string
            carrier:
              type: string
            shippedAt:
              type: string
              format: date-time
            estimatedDelivery:
              type: string
              format: date-time

    Address:
      type: object
      required:
        - street
        - city
        - country
        - postalCode
      properties:
        street:
          type: string
          example: 123 Main St
        city:
          type: string
          example: San Francisco
        state:
          type: string
          example: CA
        country:
          type: string
          example: US
        postalCode:
          type: string
          example: '94102'
```

---

## API Security Design

### OAuth 2.0 Flows

#### Authorization Code Flow (Web Apps)

**Use Case:** Web applications with server-side backend

**Flow:**
```
1. User clicks "Login" → Redirect to authorization server
2. User authenticates and grants permission
3. Authorization server redirects back with authorization code
4. Backend exchanges code for access token
5. Backend uses access token to call API
```

**Example:**
```http
# Step 1: Redirect user to authorization URL
GET https://auth.example.com/oauth/authorize?
  response_type=code&
  client_id=abc123&
  redirect_uri=https://myapp.com/callback&
  scope=read:users write:users&
  state=random_state_string

# Step 2: Authorization server redirects back
GET https://myapp.com/callback?
  code=auth_code_xyz&
  state=random_state_string

# Step 3: Exchange code for token
POST https://auth.example.com/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
code=auth_code_xyz&
client_id=abc123&
client_secret=secret456&
redirect_uri=https://myapp.com/callback

# Response
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "refresh_token_abc",
  "scope": "read:users write:users"
}

# Step 4: Use access token
GET https://api.example.com/v1/users
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Client Credentials Flow (Service-to-Service)

**Use Case:** Backend services, cron jobs, automated processes

**Flow:**
```
1. Service authenticates with client ID and secret
2. Authorization server returns access token
3. Service uses access token to call API
```

**Example:**
```http
POST https://auth.example.com/oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&
client_id=service_abc123&
client_secret=service_secret456&
scope=read:orders write:orders

# Response
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "read:orders write:orders"
}
```

### API Key Management

**API Key Patterns:**

**Header-Based (Recommended):**
```http
GET /api/v1/users
X-API-Key: sk_live_abc123xyz456
```

**Query Parameter (Not Recommended - logs exposure):**
```http
GET /api/v1/users?api_key=sk_live_abc123xyz456
```

**Bearer Token:**
```http
GET /api/v1/users
Authorization: Bearer sk_live_abc123xyz456
```

**API Key Best Practices:**
- Prefix keys with environment: `sk_live_*`, `sk_test_*`
- Store hashed keys in database (never plaintext)
- Support key rotation without downtime
- Allow multiple keys per user/organization
- Provide last-used timestamp for each key

### Scope-Based Authorization

**Scopes Define Permissions:**
```
read:users      - Read user data
write:users     - Create/update users
delete:users    - Delete users
admin:users     - Full user management

read:posts
write:posts
admin:*         - Full admin access
```

**Example Authorization Check:**
```javascript
// Check if token has required scope
function requireScope(scope) {
  return (req, res, next) => {
    const tokenScopes = req.user.scopes; // From JWT or session
    if (!tokenScopes.includes(scope)) {
      return res.status(403).json({
        type: "https://api.example.com/errors/forbidden",
        title: "Insufficient Permissions",
        status: 403,
        detail: `This operation requires the '${scope}' scope`,
        requiredScope: scope
      });
    }
    next();
  };
}

// Apply to route
router.delete('/users/:id', requireScope('delete:users'), deleteUser);
```

### CORS Configuration

**Development (Permissive):**
```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization, X-API-Key
```

**Production (Restrictive):**
```http
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 86400
```

### Security Headers

**Essential Headers:**
```http
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
```

---

## Tool Recommendations

### API Specification Tools

| Tool | Purpose | Use Case |
|------|---------|----------|
| **Swagger Editor** | Write OpenAPI specs | Interactive editing with live preview |
| **Stoplight Studio** | Design-first API development | Visual API designer + OpenAPI editor |
| **Insomnia Designer** | API design and testing | Design, document, and test APIs |
| **Redocly** | OpenAPI documentation | Generate beautiful API docs |
| **AsyncAPI Studio** | Event-driven API design | Design AsyncAPI specifications |

### Code Generation Tools

| Tool | Purpose | Languages |
|------|---------|-----------|
| **OpenAPI Generator** | Client/server code generation | 50+ languages |
| **Swagger Codegen** | Client library generation | Java, Python, JavaScript, etc. |
| **oapi-codegen** | Go server/client generation | Go |
| **openapi-typescript** | TypeScript types from OpenAPI | TypeScript |

### Validation & Testing

| Tool | Purpose |
|------|---------|
| **Spectral** | OpenAPI/AsyncAPI linting |
| **Prism** | Mock server from OpenAPI |
| **Dredd** | API testing against OpenAPI |
| **Postman** | API testing and documentation |
| **Insomnia** | API testing and debugging |

### Documentation Generators

| Tool | Output | Features |
|------|--------|----------|
| **Redoc** | Single-page docs | Beautiful, responsive, fast |
| **Swagger UI** | Interactive docs | Try-it-out functionality |
| **RapiDoc** | Modern docs | Dark mode, search, examples |
| **Docusaurus OpenAPI** | Static site | Integrates with Docusaurus |

---

## Skill Structure Design

```
api-design-principles/
├── SKILL.md                          # Main skill (600-800 lines)
├── references/
│   ├── rest-design.md                # RESTful patterns deep-dive
│   ├── graphql-design.md             # GraphQL schema and resolvers
│   ├── versioning-strategies.md      # API versioning detailed guide
│   ├── error-handling.md             # RFC 7807 implementation guide
│   ├── pagination-patterns.md        # Offset vs cursor vs keyset
│   ├── rate-limiting.md              # Token bucket, quota management
│   ├── authentication.md             # OAuth2, API keys, scopes
│   └── async-api-patterns.md         # WebSockets, Kafka, AsyncAPI
├── examples/
│   ├── openapi/
│   │   ├── user-api.yaml             # Complete OpenAPI 3.1 example
│   │   ├── product-api.yaml          # E-commerce API example
│   │   └── errors.yaml               # RFC 7807 error schemas
│   ├── asyncapi/
│   │   ├── order-events.yaml         # Kafka event-driven API
│   │   ├── chat-websocket.yaml       # WebSocket real-time API
│   │   └── notification-queue.yaml   # RabbitMQ notification system
│   └── graphql/
│       ├── schema.graphql            # Complete GraphQL schema
│       └── resolvers-pattern.md      # DataLoader and N+1 solutions
└── scripts/
    ├── validate-openapi.sh           # OpenAPI validation script
    ├── generate-docs.sh              # Documentation generation
    └── mock-server.sh                # Start Prism mock server
```

---

## Integration Points

### With Existing Skills

| Skill | Integration |
|-------|-------------|
| `api-patterns` | Implementation code (Express, FastAPI) |
| `auth-security` | Authentication implementation (JWT, sessions) |
| `database-design` | Database schema for API resources |
| `testing-strategies` | API testing (integration, contract, load) |
| `deploying-applications` | API deployment and scaling |
| `observability` | API monitoring, logging, tracing |
| `performance-engineering` | API performance optimization |

### Skill Chaining Example

```
api-design-principles → api-patterns → auth-security → testing-strategies
        │                    │              │                 │
        ▼                    ▼              ▼                 ▼
  Design REST API    Implement with    Add OAuth2      Test with Postman
  with OpenAPI       Express/FastAPI   authentication   and Dredd
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [x] Research REST best practices
- [x] Research API versioning strategies
- [x] Research OpenAPI and AsyncAPI
- [ ] Write core decision frameworks
- [ ] Create REST design patterns reference

### Phase 2: Specifications (Week 3-4)
- [ ] Complete OpenAPI 3.1 examples
- [ ] Complete AsyncAPI examples
- [ ] Error handling patterns (RFC 7807)
- [ ] Pagination patterns with examples

### Phase 3: Advanced Patterns (Week 5-6)
- [ ] GraphQL design patterns
- [ ] Rate limiting strategies
- [ ] Security design patterns
- [ ] Real-world case studies

### Phase 4: Polish & Integration (Week 7-8)
- [ ] Validation scripts
- [ ] Tool recommendations with examples
- [ ] Integration with other skills
- [ ] Final review and testing

---

## Key Takeaways

1. **Choose the right API style** - REST for simplicity, GraphQL for flexibility, WebSockets for real-time
2. **Version from day one** - URL path versioning is simplest and most visible
3. **Standardize errors** - RFC 7807 Problem Details provides consistency
4. **Design for scale** - Pagination, rate limiting, and caching are non-negotiable
5. **Document with specs** - OpenAPI/AsyncAPI enable code generation and testing
6. **Security by design** - OAuth2 scopes, API keys, CORS, security headers
7. **Think long-term** - Good API design prevents costly breaking changes

---

**Progressive disclosure:** This init.md provides the master plan. Detailed documentation in `references/` directory. Working examples in `examples/` directory.
