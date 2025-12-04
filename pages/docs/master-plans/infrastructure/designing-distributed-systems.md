---
sidebar_position: 3
title: Designing Distributed Systems
description: Master plan for distributed systems architecture including CAP/PACELC, consistency models, replication, partitioning, and resilience patterns
tags: [master-plan, infrastructure, distributed-systems, microservices, architecture]
---

# Designing Distributed Systems

:::info Status
**Master Plan** - Comprehensive init.md complete, ready for SKILL.md implementation
:::

Distributed systems are the foundation of modern cloud-native applications. This skill covers fundamental theorems, consistency models, replication patterns, partitioning strategies, resilience patterns, and transaction patterns for building reliable, scalable distributed systems.

## Scope

This skill teaches:

- **Fundamental Theorems** - CAP theorem, PACELC framework, trade-off analysis
- **Consistency Models** - Strong, sequential, causal, eventual consistency
- **Partitioning Strategies** - Hash, range, geographic partitioning
- **Replication Patterns** - Leader-follower, multi-leader, leaderless
- **Consensus Algorithms** - Raft, Paxos overview (conceptual)
- **Resilience Patterns** - Circuit breaker, bulkhead, timeout/retry, rate limiting
- **Transaction Patterns** - Saga, event sourcing, CQRS, outbox pattern
- **Service Discovery** - Client-side, server-side, service mesh
- **Caching Strategies** - Cache-aside, write-through, write-behind, invalidation

## Key Components

### CAP Theorem
- **Consistency + Availability + Partition Tolerance** - Choose 2 of 3
- **Partition tolerance is mandatory** - Network failures are inevitable
- **CP Systems** (Banking): Sacrifice availability during partitions
- **AP Systems** (Social media): Sacrifice consistency for availability

### PACELC - Beyond CAP
- **If Partition**: Choose Availability (A) or Consistency (C)
- **Else (no partition)**: Choose Latency (L) or Consistency (C)

**Examples:**
- Spanner: PC/EC (strong consistency)
- DynamoDB: PA/EL (eventual consistency)
- Cassandra: PA/EL (tunable)
- MongoDB: PC/EC (default strong)

### Replication Topologies

**Leader-Follower (Single-Leader)**
- Most common, strong consistency
- Examples: PostgreSQL, MySQL replication

**Multi-Leader**
- Multi-datacenter, low write latency
- Challenges: Conflict resolution needed
- Examples: Cassandra (tunable), CouchDB

**Leaderless (Dynamo-style)**
- High availability, partition tolerance
- Quorum: W + R > N
- Examples: Cassandra, Riak, DynamoDB

### Partitioning Strategies

**Hash Partitioning (Consistent Hashing)**
- Even distribution, easy rebalancing
- Use: Point queries by ID
- Examples: Cassandra, DynamoDB

**Range Partitioning**
- Range queries, ordered data
- Risk: Hot spots (uneven distribution)
- Examples: HBase, Bigtable

**Geographic Partitioning**
- Data locality, GDPR compliance
- Use: Multi-region, data residency
- Examples: Spanner, Cosmos DB

## Decision Framework

**Consistency Model Selection:**

```
Money involved? → Strong Consistency
Double booking unacceptable? → Strong Consistency
Causality important (chat, edits)? → Causal Consistency
Read-heavy, stale tolerable? → Eventual Consistency
Default? → Eventual (then strengthen if needed)
```

**Replication Strategy:**

```
Single datacenter? → Leader-Follower
Multi-datacenter (low write)? → Leader-Follower with replicas
Multi-datacenter (high write)? → Multi-Leader
Maximum availability? → Leaderless (Dynamo-style)
Strong consistency? → Leader-Follower with sync replication
```

**Partitioning Strategy:**

```
Need range scans? → Range Partitioning (risk: hot spots)
Data residency requirements? → Geographic Partitioning
Default? → Hash Partitioning (consistent hashing)
```

## Tool Recommendations

### Patterns by Use Case

| Use Case | Consistency Model | Example Systems |
|----------|-------------------|-----------------|
| Bank account balance | Strong (Linearizable) | Spanner, VoltDB |
| Seat booking | Strong (Linearizable) | MongoDB, PostgreSQL |
| Inventory stock | Strong or Bounded Staleness | Cosmos DB, CockroachDB |
| Shopping cart | Eventual | DynamoDB, Cassandra |
| Product catalog | Eventual | Redis, Memcached |
| Collaborative editing | Causal | CouchDB, Riak |
| Chat messages | Causal | Cassandra (tuned) |
| Social media likes | Eventual | Cassandra, Redis |
| DNS records | Eventual | DNS system |

### Resilience Patterns

**Circuit Breaker** - Prevent cascading failures
**Bulkhead Isolation** - Limit failure blast radius
**Timeout/Retry** - Handle transient failures
**Rate Limiting** - Protect against overload
**Backpressure** - Slow down producers

## Integration Points

**With Other Skills:**
- `microservices-architecture` - Apply distributed patterns to services
- `message-queues` - Async communication patterns
- `databases-*` - Database-specific consistency models
- `observability` - Distributed tracing (OpenTelemetry)
- `testing-strategies` - Chaos engineering

**Communication Patterns:**
- Synchronous: REST/gRPC for request-response
- Asynchronous: Kafka, RabbitMQ for events
- Saga Pattern: Coordinates multi-service transactions
- Outbox Pattern: Ensures reliable event publishing

## Learn More

- [Full Master Plan (init.md)](https://github.com/ancoleman/ai-design-components/blob/main/skills/designing-distributed-systems/init.md)
- Related: `microservices-architecture`, `message-queues`, `observability`
