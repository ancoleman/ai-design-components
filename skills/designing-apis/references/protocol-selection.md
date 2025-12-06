# API Protocol Selection Guide

Decision framework for choosing REST, GraphQL, WebSockets, or message queues.


## Table of Contents

- [Quick Decision Tree](#quick-decision-tree)
- [Protocol Comparison](#protocol-comparison)
- [REST: Request-Response Pattern](#rest-request-response-pattern)
  - [When to Use](#when-to-use)
  - [Advantages](#advantages)
  - [Disadvantages](#disadvantages)
  - [Example Use Cases](#example-use-cases)
- [GraphQL: Client-Specified Queries](#graphql-client-specified-queries)
  - [When to Use](#when-to-use)
  - [Advantages](#advantages)
  - [Disadvantages](#disadvantages)
  - [Example Use Cases](#example-use-cases)
- [WebSockets: Real-Time Bidirectional](#websockets-real-time-bidirectional)
  - [When to Use](#when-to-use)
  - [Advantages](#advantages)
  - [Disadvantages](#disadvantages)
  - [Example Use Cases](#example-use-cases)
- [Message Queues: Event-Driven](#message-queues-event-driven)
  - [When to Use](#when-to-use)
  - [Advantages](#advantages)
  - [Disadvantages](#disadvantages)
  - [Example Use Cases](#example-use-cases)
- [Hybrid Approaches](#hybrid-approaches)
  - [REST + WebSockets](#rest-websockets)
  - [REST + Message Queue](#rest-message-queue)
  - [GraphQL + Subscriptions](#graphql-subscriptions)
- [Decision Checklist](#decision-checklist)
  - [Choose REST if:](#choose-rest-if)
  - [Choose GraphQL if:](#choose-graphql-if)
  - [Choose WebSockets if:](#choose-websockets-if)
  - [Choose Message Queue if:](#choose-message-queue-if)

## Quick Decision Tree

```
START: What type of API do you need?
  │
  ├─► Public API for third-party developers?
  │     YES ──► REST (widest compatibility, best tooling)
  │
  ├─► Complex data with many relationships?
  │     YES ──► GraphQL (client-controlled queries)
  │
  ├─► Real-time bidirectional communication?
  │     YES ──► WebSockets (low latency, push updates)
  │
  ├─► Event-driven, decoupled microservices?
  │     YES ──► Message Queue (Kafka, RabbitMQ)
  │
  └─► Simple CRUD, caching important?
        YES ──► REST (HTTP caching, stateless)
```

## Protocol Comparison

| Factor | REST | GraphQL | WebSocket | Message Queue |
|--------|------|---------|-----------|---------------|
| **Simplicity** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Public API** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| **Complex Data** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **Caching** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ |
| **Real-time** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Bandwidth** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Tooling** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

## REST: Request-Response Pattern

### When to Use
- Public-facing APIs with diverse clients
- CRUD operations on resources
- Caching is critical (HTTP caching)
- Simple, predictable patterns needed
- Wide client compatibility required

### Advantages
- ✅ Simple, well-understood HTTP semantics
- ✅ Built-in caching (HTTP headers)
- ✅ Stateless, scales horizontally
- ✅ Mature tooling ecosystem
- ✅ Works everywhere (browsers, mobile, IoT)

### Disadvantages
- ❌ Over-fetching (get more data than needed)
- ❌ Under-fetching (need multiple requests)
- ❌ Version management complexity
- ❌ No built-in real-time updates

### Example Use Cases
- SaaS public APIs (Stripe, Twilio)
- Mobile app backends
- Microservices (internal APIs)
- CRUD applications

## GraphQL: Client-Specified Queries

### When to Use
- Complex, interconnected data models
- Mobile apps (minimize over-fetching)
- Clients need flexible data queries
- Rapid frontend iteration required
- Real-time subscriptions needed

### Advantages
- ✅ Client specifies exact data needed
- ✅ Single endpoint for all queries
- ✅ Strongly typed schema
- ✅ Real-time subscriptions
- ✅ Introspection for tooling

### Disadvantages
- ❌ More complex than REST
- ❌ Caching more difficult
- ❌ N+1 query problem (requires DataLoader)
- ❌ Monitoring and rate limiting harder
- ❌ Learning curve for developers

### Example Use Cases
- GitHub API
- Facebook/Instagram apps
- Content management systems
- Internal tools with complex data

## WebSockets: Real-Time Bidirectional

### When to Use
- Real-time updates required (chat, notifications)
- Low-latency communication needed
- Bidirectional communication (server can push)
- Long-lived connections acceptable

### Advantages
- ✅ Persistent connection
- ✅ Bidirectional (client and server send)
- ✅ Low overhead (no HTTP header per message)
- ✅ Low latency

### Disadvantages
- ❌ Stateful (harder to scale)
- ❌ Connection management complexity
- ❌ No HTTP caching
- ❌ Firewall/proxy issues

### Example Use Cases
- Chat applications (Slack)
- Real-time dashboards
- Collaborative editing (Google Docs)
- Gaming
- Live sports scores

## Message Queues: Event-Driven

### When to Use
- Decoupled microservices communication
- Event sourcing and CQRS patterns
- High-throughput message processing
- Guaranteed delivery required

### Advantages
- ✅ Publish-subscribe pattern
- ✅ Durable message storage
- ✅ Ordered processing
- ✅ Decoupling of services
- ✅ High throughput

### Disadvantages
- ❌ Additional infrastructure (Kafka, RabbitMQ)
- ❌ Eventual consistency
- ❌ Complex error handling
- ❌ Message ordering challenges

### Example Use Cases
- Microservices event bus
- Order processing systems
- Log aggregation
- IoT data streams

## Hybrid Approaches

### REST + WebSockets
- REST for CRUD operations
- WebSockets for real-time updates
- Example: Chat app (REST for message history, WebSockets for live chat)

### REST + Message Queue
- REST for synchronous requests
- Message queue for async background jobs
- Example: E-commerce (REST for orders, queue for email notifications)

### GraphQL + Subscriptions
- GraphQL queries/mutations for data
- GraphQL subscriptions (over WebSockets) for real-time
- Example: Social media feed

## Decision Checklist

### Choose REST if:
- [ ] Building public API
- [ ] Simple CRUD operations
- [ ] Caching is important
- [ ] Wide client compatibility needed
- [ ] Team familiar with HTTP/REST

### Choose GraphQL if:
- [ ] Complex, nested data relationships
- [ ] Mobile app (bandwidth constraints)
- [ ] Rapid frontend iteration
- [ ] Multiple client types with different needs
- [ ] Real-time subscriptions needed

### Choose WebSockets if:
- [ ] Real-time updates critical
- [ ] Bidirectional communication required
- [ ] Low latency important
- [ ] Long-lived connections acceptable
- [ ] Chat, gaming, or collaborative editing

### Choose Message Queue if:
- [ ] Microservices architecture
- [ ] Event-driven system
- [ ] High throughput required
- [ ] Guaranteed delivery needed
- [ ] Decoupling services important
