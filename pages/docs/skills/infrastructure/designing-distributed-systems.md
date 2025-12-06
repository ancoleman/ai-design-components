---
sidebar_position: 12
title: Designing Distributed Systems
description: Distributed system patterns with CAP theorem, consistency models, and resilience
tags: [infrastructure, distributed-systems, architecture, scalability]
---

# Designing Distributed Systems

Design scalable, reliable, and fault-tolerant distributed systems using proven patterns and consistency models. Covers CAP/PACELC theorems, replication strategies, partitioning, and resilience patterns.

## When to Use

Use when:
- Designing microservices architectures with multiple services
- Building systems that must scale across multiple datacenters or regions
- Choosing between consistency vs availability during network partitions
- Selecting replication strategies (single-leader, multi-leader, leaderless)
- Implementing distributed transactions (saga pattern, event sourcing, CQRS)
- Designing partition-tolerant systems with proper consistency guarantees
- Building resilient services with circuit breakers, bulkheads, retries

## Core Concepts

### CAP Theorem Fundamentals

**CAP Theorem:** In a distributed system experiencing a network partition, choose between Consistency (C) or Availability (A). Partition tolerance (P) is mandatory.

```
Network partitions WILL occur → Always design for P

During partition:
├─ CP (Consistency + Partition Tolerance)
│  Use when: Financial transactions, inventory, seat booking
│  Trade-off: System unavailable during partition
│  Examples: HBase, MongoDB (default), etcd
│
└─ AP (Availability + Partition Tolerance)
   Use when: Social media, caching, analytics, shopping carts
   Trade-off: Stale reads possible, conflicts need resolution
   Examples: Cassandra, DynamoDB, Riak
```

**PACELC:** Extends CAP to consider normal operations (no partition).
- **If Partition:** Choose Availability (A) or Consistency (C)
- **Else (normal):** Choose Latency (L) or Consistency (C)

### Consistency Models Spectrum

```
Strong Consistency ◄─────────────────────► Eventual Consistency
      │                    │                      │
  Linearizable      Causal Consistency     Convergent
  (Slowest,         (Middle Ground,        (Fastest,
   Most Consistent)  Causally Ordered)     Eventually Consistent)
```

**Strong Consistency (Linearizability):**
- All operations appear atomically in sequential order
- Reads always return most recent write
- Use for: Bank balances, inventory stock, seat booking
- Trade-off: Higher latency, reduced availability

**Eventual Consistency:**
- If no new updates, all replicas eventually converge
- Use for: Social feeds, product catalogs, user profiles, DNS
- Trade-off: Stale reads possible, conflict resolution needed

**Causal Consistency:**
- Causally related operations seen in same order by all nodes
- Use for: Chat apps, collaborative editing, comment threads
- Trade-off: More complex than eventual, requires causality tracking

**Bounded Staleness:**
- Staleness bounded by time or version count
- Use for: Real-time dashboards, leaderboards, monitoring
- Trade-off: Must monitor lag, more complex than eventual

### Replication Patterns

**1. Leader-Follower (Single-Leader):**
- All writes to leader, replicated to followers
- Followers handle reads (load distribution)
- **Synchronous:** Wait for follower ACK (strong consistency, higher latency)
- **Asynchronous:** Don't wait (eventual consistency, possible data loss)
- Use for: Most common pattern, strong consistency with sync replication

**2. Multi-Leader:**
- Multiple leaders accept writes in different datacenters
- Leaders replicate to each other
- **Conflict resolution required:** Last-Write-Wins, application merge, vector clocks
- Use for: Multi-datacenter, low write latency, geo-distributed users
- Trade-off: Conflict resolution complexity

**3. Leaderless (Dynamo-style):**
- No single leader, quorum-based reads/writes
- **Quorum rule:** W + R > N (W=write quorum, R=read quorum, N=replicas)
- Example: N=5, W=3, R=2 → Strong consistency (overlap guaranteed)
- Use for: Maximum availability, partition tolerance
- Trade-off: Complexity, read repair needed

### Partitioning Strategies

**Hash Partitioning (Consistent Hashing):**
- Key → Hash(Key) → Partition assignment
- Even distribution, minimal rebalancing when nodes added/removed
- Use for: Point queries by ID, even distribution critical
- Examples: Cassandra, DynamoDB, Redis Cluster

**Range Partitioning:**
- Key ranges assigned to partitions (A-F, G-M, N-S, T-Z)
- Enables range queries, ordered data
- Risk: Hot spots if data skewed
- Use for: Time-series data, leaderboards, range scans
- Examples: HBase, Bigtable

**Geographic Partitioning:**
- Partition by location (US-East, EU-West, APAC)
- Use for: Data locality, GDPR compliance, low latency
- Examples: Spanner, Cosmos DB

### Resilience Patterns

**Circuit Breaker:**
```
[Closed] → Normal operation
   │ (failures exceed threshold)
   ▼
[Open] → Fail fast (don't call failing service)
   │ (timeout expires)
   ▼
[Half-Open] → Try single request
   │ success → [Closed]
   │ failure → [Open]
```
- Prevents cascading failures
- Fast-fail instead of waiting for timeout

**Bulkhead Isolation:**
- Isolate resources (thread pools, connection pools)
- Failure in one partition doesn't affect others
- Like ship compartments preventing total flooding

**Timeout and Retry:**
- **Timeout:** Set deadlines, fail fast if exceeded
- **Retry:** Exponential backoff with jitter
- **Idempotency:** Ensure safe retry (critical)

**Rate Limiting and Backpressure:**
- Protect services from overload
- Token bucket, leaky bucket algorithms
- Backpressure: Signal upstream to slow down

### Transaction Patterns

**Saga Pattern:**
- Coordinate distributed transactions across services
- No distributed 2PC (two-phase commit)

**Choreography:** Services react to events
```
Order Service → OrderCreated event
Payment Service → listens → PaymentProcessed event
Inventory Service → listens → InventoryReserved event
(Compensating: if payment fails → InventoryReleased event)
```

**Orchestration:** Central coordinator
```
Saga Orchestrator:
1. Call Order Service
2. Call Payment Service
3. Call Inventory Service
(If step fails → call compensating transactions in reverse)
```

**Event Sourcing:**
- Store state changes as immutable events
- Rebuild state by replaying events
- Audit trail, time travel, debugging
- Trade-off: Query complexity, snapshot optimization

**CQRS (Command Query Responsibility Segregation):**
- Separate read and write models
- Write model: Normalized, transactional
- Read model: Denormalized, cached, optimized
- Use for: Different read/write patterns, high read:write ratio (10:1+)
- Often paired with Event Sourcing

## Decision Frameworks

### Choosing Consistency Model

```
Decision Tree:
├─ Money involved? → Strong Consistency
├─ Double-booking unacceptable? → Strong Consistency
├─ Causality important (chat, edits)? → Causal Consistency
├─ Read-heavy, stale tolerable? → Eventual Consistency
└─ Default? → Eventual (then strengthen if needed)
```

### Choosing Replication Pattern

```
├─ Single region writes? → Leader-Follower
├─ Multi-region writes + conflicts OK? → Multi-Leader
├─ Multi-region writes + no conflicts? → Leader-Follower with failover
└─ Maximum availability? → Leaderless (quorum)
```

### Choosing Partitioning Strategy

```
├─ Need range scans? → Range Partitioning (risk: hot spots)
├─ Data residency requirements? → Geographic Partitioning
└─ Default? → Hash Partitioning (consistent hashing)
```

## Quick Reference Tables

### CAP/PACELC System Comparison

| System     | If Partition | Else (Normal) | Use Case           |
|------------|--------------|---------------|--------------------|
| Spanner    | PC           | EC (strong)   | Global SQL         |
| DynamoDB   | PA           | EL (eventual) | High availability  |
| Cassandra  | PA           | EL (tunable)  | Wide-column store  |
| MongoDB    | PC           | EC (default)  | Document store     |
| Cosmos DB  | PA/PC        | EL/EC (5 levels) | Multi-model     |

### Consistency Model Use Cases

| Use Case                   | Consistency Model       |
|----------------------------|------------------------|
| Bank account balance       | Strong (Linearizable)  |
| Seat booking (airline)     | Strong (Linearizable)  |
| Inventory stock count      | Strong or Bounded      |
| Shopping cart              | Eventual               |
| Product catalog            | Eventual               |
| Collaborative editing      | Causal                 |
| Chat messages              | Causal                 |
| Social media likes         | Eventual               |
| DNS records                | Eventual               |

### Quorum Configurations

| Configuration | W | R | N | Consistency | Use Case    |
|--------------|---|---|---|-------------|-------------|
| Strong       | 3 | 3 | 5 | Strong      | Banking     |
| Balanced     | 3 | 2 | 5 | Strong      | Default     |
| Write-heavy  | 2 | 3 | 5 | Strong      | Logs        |
| Read-heavy   | 3 | 1 | 5 | Eventual    | Cache       |
| Max Avail    | 1 | 1 | 5 | Eventual    | Analytics   |

## Best Practices

**Design for Failure:**
- Network partitions will occur - always design for partition tolerance
- Use timeouts, retries with exponential backoff
- Implement circuit breakers to prevent cascading failures
- Test chaos engineering scenarios (partition nodes, inject latency)

**Choose Consistency Carefully:**
- Default to eventual consistency, strengthen only where needed
- Strong consistency has real costs (latency, availability)
- Use bounded staleness for middle ground

**Idempotency is Critical:**
- Design operations to be safely retryable
- Use unique request IDs for deduplication
- Essential for saga compensating transactions

**Monitor and Observe:**
- Distributed tracing with correlation IDs
- Monitor replication lag, quorum health
- Alert on circuit breaker state changes
- Track saga progress and failures

## Related Skills

- [Operating Kubernetes](./operating-kubernetes) - Pod anti-affinity, service mesh
- [Writing Infrastructure Code](./writing-infrastructure-code) - Deploying distributed systems
- [Implementing Service Mesh](./implementing-service-mesh) - Service-to-service communication
- [Architecting Networks](./architecting-networks) - Network topology for distributed systems
- [Load Balancing Patterns](./load-balancing-patterns) - Traffic distribution strategies

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/designing-distributed-systems)
- CAP/PACELC Theorem: `references/cap-pacelc-theorem.md`
- Consistency Models: `references/consistency-models.md`
- Replication Patterns: `references/replication-patterns.md`
- Partitioning Strategies: `references/partitioning-strategies.md`
- Resilience Patterns: `references/resilience-patterns.md`
- Saga Pattern: `references/saga-pattern.md`
- Event Sourcing/CQRS: `references/event-sourcing-cqrs.md`
