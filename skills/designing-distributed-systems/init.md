# Designing Distributed Systems Skill - Master Plan

**Skill Name:** `designing-distributed-systems`
**Skill Level:** High Level (8,000-12,000 tokens)
**Status:** Planning Phase (init.md complete, SKILL.md to be created)
**Last Updated:** December 3, 2025

---

## Table of Contents

1. [Strategic Positioning](#strategic-positioning)
2. [Skill Purpose and Scope](#skill-purpose-and-scope)
3. [Research Findings](#research-findings)
4. [Distributed Systems Taxonomy](#distributed-systems-taxonomy)
5. [Decision Frameworks](#decision-frameworks)
6. [Consistency Models and Patterns](#consistency-models-and-patterns)
7. [Partitioning and Replication Patterns](#partitioning-and-replication-patterns)
8. [Resilience and Fault Tolerance Patterns](#resilience-and-fault-tolerance-patterns)
9. [Transaction Patterns (Saga, Event Sourcing, CQRS)](#transaction-patterns-saga-event-sourcing-cqrs)
10. [Service Discovery and Communication](#service-discovery-and-communication)
11. [Caching Strategies](#caching-strategies)
12. [Tool Recommendations](#tool-recommendations)
13. [Skill Structure Design](#skill-structure-design)
14. [Integration Points](#integration-points)
15. [Implementation Roadmap](#implementation-roadmap)

---

## Strategic Positioning

### Why This Skill Matters

Distributed systems are the foundation of modern cloud-native applications. In 2025, with microservices, serverless, edge computing, and multi-cloud becoming standard, understanding distributed systems design patterns is essential for building reliable, scalable systems.

**Market Drivers:**
- **Microservices Dominance:** 85%+ of new cloud applications use microservices
- **Multi-Cloud Reality:** Organizations need systems that work across AWS, GCP, Azure
- **Edge Computing:** IoT and 5G driving distributed compute to the edge
- **Scale Requirements:** Systems must handle millions of users globally
- **Resilience Expectations:** 99.99% uptime is the minimum standard

**Strategic Value:**
1. **Architectural Foundation:** Every distributed application needs these patterns
2. **Cross-Cutting Skill:** Applies to microservices, databases, message queues, caching
3. **Interview Essential:** CAP theorem, consistency models, consensus are standard questions
4. **Operational Critical:** Understanding trade-offs prevents production incidents

### How This Differs from Existing Solutions

**Existing Resources:**
- **Academic Focus:** CAP theorem explained in isolation, not applied
- **Tool-Specific:** Kubernetes patterns OR database patterns, not unified
- **Theory-Heavy:** Mathematical proofs without practical implementation

**Our Approach:**
- **Decision-Driven:** When to choose CP vs AP, strong vs eventual consistency
- **Pattern Catalog:** Reusable patterns with ASCII diagrams and examples
- **Trade-Off Analysis:** PACELC framework for nuanced decisions
- **Operational Reality:** Drift detection, failure modes, monitoring
- **Integration Focus:** How patterns combine in real systems

---

## Skill Purpose and Scope

### What This Skill Teaches

**Core Competencies:**

1. **Fundamental Theorems**
   - CAP theorem (Consistency, Availability, Partition tolerance)
   - PACELC (extends CAP with latency considerations)
   - Trade-off analysis for real-world systems

2. **Consistency Models**
   - Strong consistency (linearizability)
   - Sequential consistency
   - Causal consistency
   - Eventual consistency
   - When to use each model

3. **Partitioning Strategies**
   - Hash partitioning (consistent hashing)
   - Range partitioning
   - Geographic partitioning
   - Partition rebalancing

4. **Replication Patterns**
   - Leader-follower (single-leader)
   - Multi-leader replication
   - Leaderless replication (Dynamo-style)
   - Synchronous vs asynchronous replication

5. **Consensus Algorithms (Conceptual)**
   - Raft overview (leader election, log replication)
   - Paxos overview (proposer, acceptor, learner)
   - When consensus is needed vs overkill

6. **Resilience Patterns**
   - Circuit breaker
   - Bulkhead isolation
   - Timeout and retry strategies
   - Rate limiting and backpressure

7. **Transaction Patterns**
   - Saga pattern (choreography vs orchestration)
   - Event sourcing
   - CQRS (Command Query Responsibility Segregation)
   - Outbox pattern

8. **Service Discovery**
   - Client-side discovery
   - Server-side discovery
   - Service mesh patterns

9. **Caching Strategies**
   - Cache-aside
   - Write-through
   - Write-behind
   - Cache invalidation patterns

### What This Skill Does NOT Cover

- Specific database implementations (see `databases-*` skills)
- Kubernetes operational details (see `kubernetes-operations`)
- Message queue specifics (see `message-queues`)
- Cloud provider services (see `aws-patterns`, `gcp-patterns`)
- Performance testing (see `performance-engineering`)

---

## Research Findings

### Google Search Grounding (December 2025)

**Research Methodology:**
- Conducted searches on CAP theorem, microservices patterns, consistency models
- Tool experienced intermittent errors (4 queries attempted, 2 successful)
- Successfully gathered insights on CAP/PACELC, microservices patterns, and saga/CQRS

**Key 2025 Trends:**

**1. CAP and PACELC Theorem Applications:**
- **CAP remains fundamental:** Choose 2 of 3 (Consistency, Availability, Partition tolerance)
- **PACELC provides nuance:** Else (when no Partition), choose Latency vs Consistency
- **Trade-offs are contextual:** Banking (CP), social media (AP), e-commerce (hybrid)
- **Partition tolerance is mandatory:** Network failures are inevitable, always design for P

**2. Microservices Architecture Patterns (2025):**
- **API Gateway:** Single entry point, handles cross-cutting concerns
- **Service Mesh:** Decouples service-to-service communication (Istio, Linkerd)
- **Circuit Breaker:** Prevents cascading failures
- **Event Sourcing:** Captures state changes as events
- **CQRS:** Separates read/write models for scalability
- **Saga Pattern:** Manages distributed transactions with compensating actions
- **Strangler Fig:** Incremental migration from monolith

**3. Consistency Models Evolution:**
- **Strong consistency:** Required for financial transactions, inventory
- **Eventual consistency:** Acceptable for social feeds, analytics
- **Causal consistency:** Middle ground for collaborative applications
- **Bounded staleness:** Configurable lag (e.g., Azure Cosmos DB)

**4. Communication Patterns:**
- **Synchronous:** REST/gRPC for request-response
- **Asynchronous:** Kafka, RabbitMQ, Azure Service Bus for events
- **Saga Pattern:** Coordinates multi-service transactions
- **Outbox Pattern:** Ensures reliable event publishing

**5. Observability Requirements:**
- **OpenTelemetry:** Standard for distributed tracing
- **Prometheus + Grafana:** Metrics and dashboards
- **Jaeger/Zipkin:** Trace aggregation
- **Correlation IDs:** Track requests across services

### Key Insights from Research

**From CAP Theorem Research:**
- CP systems (e.g., banking) sacrifice availability during partitions for consistency
- AP systems (e.g., shopping carts) sacrifice consistency for availability
- Real-world systems often use hybrid approaches (different guarantees per operation)

**From Microservices Research:**
- Single Responsibility Principle applied to services
- Autonomy: Each service owns its data and decisions
- Replaceability: Services evolve independently
- Database per service pattern for fault isolation

**From Best Practices:**
1. Treat distributed systems as inherently unreliable
2. Design for failure (timeouts, retries, circuit breakers)
3. Use idempotency for safe retries
4. Implement observability from day one
5. Test chaos engineering scenarios

---

## Distributed Systems Taxonomy

### Tier 1: Consistency Spectrum

```
Strong Consistency ◄────────────────────► Eventual Consistency
      │                    │                      │
      │                    │                      │
  Linearizable    Causal Consistency    Convergent
   (Slowest,         (Middle Ground,      (Fastest,
    Most Consistent)  Causally Ordered)   Eventually Consistent)

Examples:
Strong:     Bank account balance, inventory stock
Causal:     Chat messages, collaborative editing
Eventual:   Social media likes, view counts, DNS
```

### Tier 2: Replication Topologies

```
1. LEADER-FOLLOWER (Single-Leader)

   ┌─────────┐
   │ Leader  │ ◄─── All writes
   └────┬────┘
        │ (replicates)
   ┌────┴────┬────────┐
   │         │        │
   ▼         ▼        ▼
Follower  Follower Follower
(reads)   (reads)  (reads)

Use: Most common, strong consistency
Examples: PostgreSQL replication, MySQL replication


2. MULTI-LEADER

   ┌─────────┐      ┌─────────┐
   │ Leader  │◄────►│ Leader  │
   │ (US)    │      │ (EU)    │
   └────┬────┘      └────┬────┘
        │                │
   (replicates)     (replicates)
        │                │
   Followers        Followers

Use: Multi-datacenter, low write latency
Challenges: Conflict resolution needed
Examples: Cassandra (tunable), CouchDB


3. LEADERLESS (Dynamo-style)

   ┌─────────┐      ┌─────────┐
   │  Node   │◄────►│  Node   │
   │  (R/W)  │      │  (R/W)  │
   └────┬────┘      └────┬────┘
        │   ╲        ╱   │
        │    ╲      ╱    │
        │     ╲    ╱     │
   ┌────┴────┐ ╲  ╱ ┌────┴────┐
   │  Node   │  ╳  │  Node   │
   │  (R/W)  │ ╱  ╲│  (R/W)  │
   └─────────┘╱    ╲└─────────┘

Use: High availability, partition tolerance
Quorum: W + R > N (W=write quorum, R=read quorum, N=replicas)
Examples: Cassandra, Riak, DynamoDB
```

### Tier 3: Partitioning Strategies

```
1. HASH PARTITIONING (Consistent Hashing)

   Key → Hash(Key) % N → Partition

   User ID "user123" → hash() → 42 → Partition 3

   ┌──────────┐
   │ Hash Ring│
   │    ●─────┼──── Partition 1
   │   ╱ ╲    │
   │  ●   ●───┼──── Partition 2
   │  │   │   │
   │  ●   ●───┼──── Partition 3
   │   ╲ ╱    │
   │    ●─────┼──── Partition 4
   └──────────┘

Use: Even distribution, easy rebalancing
Examples: Cassandra, DynamoDB


2. RANGE PARTITIONING

   Key range → Partition

   A-F  → Partition 1
   G-M  → Partition 2
   N-S  → Partition 3
   T-Z  → Partition 4

Use: Range queries, ordered data
Risk: Hot spots (uneven distribution)
Examples: HBase, Bigtable


3. GEOGRAPHIC PARTITIONING

   Location → Partition

   US-East  → Partition 1 (Virginia)
   US-West  → Partition 2 (Oregon)
   EU       → Partition 3 (Ireland)
   APAC     → Partition 4 (Singapore)

Use: Data locality, GDPR compliance
Examples: Spanner, Cosmos DB
```

---

## Decision Frameworks

### Framework 1: CAP Theorem Selection

```
START: Designing a distributed system
  │
  ├─► Network partitions will occur? (Always YES in distributed systems)
  │   │
  │   └─► Choose 2: Consistency + Availability is impossible
  │
  ├─► What happens during a partition?
  │   │
  │   ├─► CONSISTENCY + PARTITION TOLERANCE (CP)
  │   │   │
  │   │   ├─ Use when: Financial transactions, inventory, booking systems
  │   │   ├─ Trade-off: System becomes unavailable during partition
  │   │   ├─ Examples: HBase, MongoDB (default), Redis Cluster
  │   │   └─ Pattern: Fail writes until partition heals
  │   │
  │   └─► AVAILABILITY + PARTITION TOLERANCE (AP)
  │       │
  │       ├─ Use when: Social media, caching, shopping carts, analytics
  │       ├─ Trade-off: Stale reads possible, conflicts need resolution
  │       ├─ Examples: Cassandra, DynamoDB, Riak
  │       └─ Pattern: Accept writes, resolve conflicts later (LWW, vector clocks)
```

### Framework 2: PACELC - Beyond CAP

**PACELC extends CAP:**
- **If Partition:** Choose Availability (A) or Consistency (C)
- **Else (no partition):** Choose Latency (L) or Consistency (C)

```
┌─────────────────────────────────────────────────────┐
│                   PACELC Matrix                     │
├─────────────────────────────────────────────────────┤
│ System         │ If Partition │ Else (Normal)      │
├────────────────┼──────────────┼────────────────────┤
│ Spanner        │ PC           │ EC (strong)        │
│ DynamoDB       │ PA           │ EL (eventual)      │
│ Cassandra      │ PA           │ EL (tunable)       │
│ MongoDB        │ PC           │ EC (default)       │
│ Cosmos DB      │ PA/PC        │ EL/EC (5 levels)   │
│ VoltDB         │ PC           │ EC                 │
│ Riak           │ PA           │ EL                 │
└────────────────┴──────────────┴────────────────────┘

Key:
P = Partition occurs
A = Choose Availability
C = Choose Consistency
E = Else (no partition)
L = Choose Latency (lower)
```

### Framework 3: Consistency Model Selection

```
┌─────────────────────────────────────────────────────────────────┐
│                    Consistency Model Selection                  │
├─────────────────────────────────────────────────────────────────┤
│ Use Case                          │ Consistency Model           │
├───────────────────────────────────┼─────────────────────────────┤
│ Bank account balance              │ Strong (Linearizable)       │
│ Seat booking (airline)            │ Strong (Linearizable)       │
│ Inventory stock count             │ Strong or Bounded Staleness │
│ Shopping cart                     │ Eventual                    │
│ Product catalog                   │ Eventual                    │
│ User profile updates              │ Eventual                    │
│ Collaborative editing             │ Causal                      │
│ Chat messages                     │ Causal                      │
│ Social media likes                │ Eventual                    │
│ View counts                       │ Eventual                    │
│ DNS records                       │ Eventual                    │
│ Global config (read-heavy)        │ Eventual with cache         │
└───────────────────────────────────┴─────────────────────────────┘

Decision Tree:
  │
  ├─► Money involved? → Strong Consistency
  │
  ├─► Double booking unacceptable? → Strong Consistency
  │
  ├─► Causality important (chat, edits)? → Causal Consistency
  │
  ├─► Read-heavy, stale tolerable? → Eventual Consistency
  │
  └─► Default? → Eventual (then strengthen if needed)
```

### Framework 4: Replication Strategy Selection

```
┌─────────────────────────────────────────────────────────────────┐
│ Scenario                     │ Replication Pattern              │
├──────────────────────────────┼──────────────────────────────────┤
│ Single datacenter            │ Leader-Follower                  │
│ Multi-datacenter (low write) │ Leader-Follower with replicas    │
│ Multi-datacenter (high write)│ Multi-Leader                     │
│ Maximum availability needed  │ Leaderless (Dynamo-style)        │
│ Strong consistency required  │ Leader-Follower with sync rep    │
│ Read scaling needed          │ Leader-Follower with read replicas│
│ Geo-distributed users        │ Multi-Leader or Leaderless       │
└──────────────────────────────┴──────────────────────────────────┘

Write Patterns:
  │
  ├─► Single region writes? → Leader-Follower
  │
  ├─► Multi-region writes + conflicts OK? → Multi-Leader
  │
  ├─► Multi-region writes + no conflicts? → Leader-Follower with failover
  │
  └─► Maximum availability? → Leaderless (quorum writes)
```

### Framework 5: Partitioning Strategy Selection

```
┌─────────────────────────────────────────────────────────────────┐
│ Access Pattern               │ Partitioning Strategy            │
├──────────────────────────────┼──────────────────────────────────┤
│ Point queries (by ID)        │ Hash partitioning                │
│ Range queries (by date)      │ Range partitioning               │
│ Geographic queries           │ Geographic partitioning          │
│ Even distribution critical   │ Hash partitioning                │
│ GDPR data residency          │ Geographic partitioning          │
│ Leaderboard queries          │ Range partitioning               │
│ Time-series data             │ Range partitioning (by time)     │
└──────────────────────────────┴──────────────────────────────────┘

Decision Flow:
  │
  ├─► Need range scans? → Range Partitioning
  │     (Risk: Hot spots, needs monitoring)
  │
  ├─► Data residency requirements? → Geographic Partitioning
  │
  └─► Default? → Hash Partitioning (consistent hashing)
```

---

## Consistency Models and Patterns

### Pattern 1: Strong Consistency (Linearizability)

**Definition:** All operations appear to execute atomically in some sequential order. Reads always return the most recent write.

```
┌─────────────────────────────────────────────────────┐
│              Strong Consistency Timeline            │
├─────────────────────────────────────────────────────┤
│ Time →                                              │
│                                                      │
│ Client A:  Write(x=1) ────────────► Success         │
│                │                                     │
│                │ (replicated)                        │
│                │                                     │
│ Client B:      └─────────► Read(x) → Returns 1      │
│                                │                     │
│                                │                     │
│ Client C:                      └──► Read(x) → Returns 1│
│                                                      │
│ Guarantee: All reads after write return new value   │
└─────────────────────────────────────────────────────┘
```

**When to Use:**
- Financial transactions (money transfers, payments)
- Inventory management (prevent overselling)
- Seat/ticket booking systems
- Distributed locks

**Implementation Approaches:**
- Single-leader replication with synchronous writes
- Consensus algorithms (Raft, Paxos)
- Two-phase commit (2PC) - slower, blocking
- Strongly consistent databases (Spanner, VoltDB)

**Trade-offs:**
- ✅ Simplifies application logic (no conflicts)
- ✅ Immediate consistency guarantees
- ❌ Higher latency (coordination overhead)
- ❌ Reduced availability during network issues

### Pattern 2: Eventual Consistency

**Definition:** System guarantees that if no new updates are made, all replicas will eventually converge to the same value.

```
┌─────────────────────────────────────────────────────┐
│            Eventual Consistency Timeline            │
├─────────────────────────────────────────────────────┤
│ Time →                                              │
│                                                      │
│ Client A:  Write(x=1) ──► Success (to leader)       │
│                │                                     │
│                │ (async replication)                 │
│                │                                     │
│ Client B:      └──► Read(x) → Returns 0 (stale!)    │
│                          │                           │
│                          │ (replication catches up)  │
│                          │                           │
│ Client B:                └──► Read(x) → Returns 1   │
│                                                      │
│ Guarantee: Eventually consistent (seconds/minutes)  │
└─────────────────────────────────────────────────────┘
```

**When to Use:**
- Social media feeds (likes, comments, follows)
- Product catalogs (prices, descriptions)
- User profiles
- Analytics and metrics
- DNS
- Shopping cart (can tolerate stale briefly)

**Implementation Approaches:**
- Asynchronous replication
- Anti-entropy (gossip protocols)
- Conflict-free replicated data types (CRDTs)
- Last-write-wins (LWW) with timestamps
- Vector clocks for conflict detection

**Trade-offs:**
- ✅ Low latency (no coordination)
- ✅ High availability
- ✅ Scales better
- ❌ Application must handle stale reads
- ❌ Conflict resolution complexity

### Pattern 3: Causal Consistency

**Definition:** Operations that are causally related are seen by all nodes in the same order. Concurrent operations may be seen in different orders.

```
┌─────────────────────────────────────────────────────┐
│              Causal Consistency Example             │
├─────────────────────────────────────────────────────┤
│ Alice:  Post message A                              │
│            │                                         │
│            │ (causes)                                │
│            ▼                                         │
│ Bob:    Reply B (to A)                              │
│            │                                         │
│            │ (causes)                                │
│            ▼                                         │
│ Carol:  Reply C (to B)                              │
│                                                      │
│ Guarantee: All users see messages in order A→B→C    │
│            (causally related)                       │
│                                                      │
│ Charlie: Post X (concurrent with A, B, C)           │
│                                                      │
│ No Guarantee: X may appear anywhere in timeline     │
│               (not causally related)                │
└─────────────────────────────────────────────────────┘
```

**When to Use:**
- Chat applications
- Collaborative editing (Google Docs)
- Comment threads
- Distributed version control (Git)
- Notification systems

**Implementation Approaches:**
- Lamport timestamps
- Vector clocks
- Causal broadcast protocols
- Databases: Azure Cosmos DB (Session consistency), Cassandra (with special config)

**Trade-offs:**
- ✅ Stronger than eventual, weaker than strong
- ✅ Better performance than strong consistency
- ✅ Intuitive for users (causality preserved)
- ❌ More complex than eventual consistency
- ❌ Requires tracking causality metadata

### Pattern 4: Bounded Staleness

**Definition:** Reads may lag behind writes, but staleness is bounded by time or number of versions.

```
┌─────────────────────────────────────────────────────┐
│            Bounded Staleness (Example: 5 sec)       │
├─────────────────────────────────────────────────────┤
│ Time →                                              │
│                                                      │
│ T=0:   Write(x=1) ──► Leader                        │
│                                                      │
│ T=2:   Read(x) → May return 0 or 1 (within bound)  │
│                                                      │
│ T=4:   Read(x) → May return 0 or 1 (within bound)  │
│                                                      │
│ T=6:   Read(x) → MUST return 1 (bound exceeded)    │
│                                                      │
│ Guarantee: Staleness ≤ 5 seconds                    │
└─────────────────────────────────────────────────────┘
```

**When to Use:**
- Real-time dashboards (slight delay acceptable)
- Inventory with buffer (e.g., "at least 100 in stock")
- Leaderboards
- Monitoring systems

**Implementation:**
- Azure Cosmos DB (configurable staleness window)
- Custom logic with timestamps
- Read from replicas with lag monitoring

**Trade-offs:**
- ✅ Middle ground: consistency + performance
- ✅ Predictable staleness window
- ❌ More complex than eventual
- ❌ Requires monitoring lag

---

## Partitioning and Replication Patterns

### Pattern 1: Consistent Hashing

**Purpose:** Distribute data evenly across nodes, minimize rebalancing when nodes added/removed.

```
┌──────────────────────────────────────────────────────┐
│              Consistent Hashing Ring                 │
│                                                       │
│                   0° ─────┐                          │
│                          Node A                      │
│                    ╱           ╲                     │
│                   ╱             ╲                    │
│            270° ─┤    Virtual    ├─ 90°             │
│         Node D   │     Nodes     │   Node B         │
│                   ╲             ╱                    │
│                    ╲           ╱                     │
│                          Node C                      │
│                  180° ─────┘                         │
│                                                       │
│ Key "user123" → hash("user123") → angle 45°          │
│                   → Stored on Node B                 │
│                                                       │
│ When Node E joins at 135°:                           │
│   Only keys between 90°-135° move from B to E        │
│   (~25% of one node's data)                          │
└──────────────────────────────────────────────────────┘
```

**Implementation:**
```python
# Consistent hashing example
import hashlib

class ConsistentHash:
    def __init__(self, nodes=None, replicas=3):
        self.replicas = replicas
        self.ring = {}  # hash -> node
        self.sorted_keys = []

        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node):
        for i in range(self.replicas):
            virtual_key = f"{node}:{i}"
            hash_val = self._hash(virtual_key)
            self.ring[hash_val] = node
            self.sorted_keys.append(hash_val)
        self.sorted_keys.sort()

    def remove_node(self, node):
        for i in range(self.replicas):
            virtual_key = f"{node}:{i}"
            hash_val = self._hash(virtual_key)
            del self.ring[hash_val]
            self.sorted_keys.remove(hash_val)

    def get_node(self, key):
        if not self.ring:
            return None
        hash_val = self._hash(key)

        # Find first node >= hash_val
        for ring_key in self.sorted_keys:
            if ring_key >= hash_val:
                return self.ring[ring_key]

        # Wrap around to first node
        return self.ring[self.sorted_keys[0]]

# Usage
ch = ConsistentHash(['node1', 'node2', 'node3'])
print(ch.get_node('user123'))  # node2
print(ch.get_node('user456'))  # node1
```

**When to Use:**
- Distributed caches (Redis Cluster, Memcached)
- Distributed databases (Cassandra, DynamoDB)
- Load balancing
- CDN edge selection

**Benefits:**
- ✅ Even distribution with virtual nodes
- ✅ Minimal data movement when scaling
- ✅ No central coordinator needed

### Pattern 2: Leader-Follower Replication

**Purpose:** All writes go to leader, replicated to followers for read scaling.

```
┌──────────────────────────────────────────────────────┐
│          Leader-Follower Replication                 │
│                                                       │
│ Client Writes                                         │
│     │                                                 │
│     ▼                                                 │
│ ┌────────────┐                                       │
│ │   Leader   │ (1) Accept write                      │
│ │            │ (2) Write to local log                │
│ └─────┬──────┘ (3) Replicate to followers            │
│       │                                               │
│       ├──────────────┬──────────────┐                │
│       │              │              │                │
│       ▼              ▼              ▼                │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│ │Follower 1│  │Follower 2│  │Follower 3│            │
│ │ (Replica)│  │ (Replica)│  │ (Replica)│            │
│ └──────────┘  └──────────┘  └──────────┘            │
│       ▲              ▲              ▲                │
│       │              │              │                │
│       └──────────────┴──────────────┘                │
│                   │                                   │
│              Client Reads                             │
│              (Load balanced)                          │
└──────────────────────────────────────────────────────┘
```

**Synchronous vs Asynchronous:**

```
SYNCHRONOUS (Strong Consistency):
  Client → Leader → Wait for Follower ACK → Success
  Pro: Guaranteed consistency
  Con: Higher latency, reduced availability

ASYNCHRONOUS (Eventual Consistency):
  Client → Leader → Success (replicate in background)
  Pro: Low latency, high availability
  Con: Possible data loss if leader fails
```

**Implementation Example (PostgreSQL):**
```sql
-- On Leader (Primary)
CREATE PUBLICATION my_publication FOR ALL TABLES;

-- On Follower (Replica)
CREATE SUBSCRIPTION my_subscription
    CONNECTION 'host=leader port=5432 dbname=mydb'
    PUBLICATION my_publication;

-- Read-only queries on follower
SELECT * FROM users WHERE id = 123;
```

**When to Use:**
- Most common replication pattern
- Single datacenter with read scaling
- Strong consistency required (with sync replication)

**Leader Failover:**
```
Leader fails
    │
    ▼
Detect failure (health checks, timeout)
    │
    ▼
Elect new leader (manual or automatic)
    │ Options:
    ├─ Longest replication log
    ├─ Lowest replica lag
    └─ Manual promotion
    │
    ▼
Reconfigure followers → point to new leader
    │
    ▼
Redirect writes to new leader
```

### Pattern 3: Multi-Leader Replication

**Purpose:** Accept writes in multiple datacenters, replicate between leaders.

```
┌──────────────────────────────────────────────────────┐
│          Multi-Leader Replication                    │
│                                                       │
│    US-EAST Datacenter         EU-WEST Datacenter     │
│    ┌──────────────┐           ┌──────────────┐      │
│    │   Leader 1   │◄─────────►│   Leader 2   │      │
│    │              │  Replicate │              │      │
│    └──────┬───────┘           └──────┬───────┘      │
│           │                           │              │
│      ┌────┴────┐                 ┌────┴────┐        │
│      ▼         ▼                 ▼         ▼        │
│  Follower  Follower          Follower  Follower     │
│                                                       │
│ Client (US) → Leader 1 (low latency)                 │
│ Client (EU) → Leader 2 (low latency)                 │
│                                                       │
│ CONFLICT SCENARIO:                                    │
│ T=0: Client A → Leader 1 → Write(x=1)                │
│ T=0: Client B → Leader 2 → Write(x=2)                │
│ T=1: Leaders replicate... CONFLICT!                  │
│                                                       │
│ Resolution strategies:                                │
│ 1. Last-Write-Wins (timestamp)                       │
│ 2. Application-specific merge                        │
│ 3. Vector clocks                                     │
│ 4. Custom conflict handlers                          │
└──────────────────────────────────────────────────────┘
```

**Conflict Resolution Strategies:**

```python
# 1. Last-Write-Wins (LWW)
def resolve_lww(version1, version2):
    if version1.timestamp > version2.timestamp:
        return version1
    return version2

# 2. Application-specific (shopping cart merge)
def merge_shopping_carts(cart1, cart2):
    # Union of items
    merged = {}
    for item_id, qty in cart1.items():
        merged[item_id] = qty
    for item_id, qty in cart2.items():
        merged[item_id] = merged.get(item_id, 0) + qty
    return merged

# 3. Version vectors (detect conflicts)
class VersionVector:
    def __init__(self):
        self.vector = {}  # node_id -> counter

    def increment(self, node_id):
        self.vector[node_id] = self.vector.get(node_id, 0) + 1

    def is_concurrent(self, other):
        # Neither dominates = concurrent = conflict
        self_dominates = False
        other_dominates = False

        all_nodes = set(self.vector.keys()) | set(other.vector.keys())
        for node in all_nodes:
            self_val = self.vector.get(node, 0)
            other_val = other.vector.get(node, 0)
            if self_val > other_val:
                self_dominates = True
            elif other_val > self_val:
                other_dominates = True

        return self_dominates and other_dominates
```

**When to Use:**
- Multi-datacenter deployments
- Low write latency critical (users write locally)
- Can tolerate conflict resolution complexity

**Examples:**
- CouchDB (built-in conflict resolution)
- Cassandra (tunable consistency)
- MySQL with multi-source replication

### Pattern 4: Leaderless (Dynamo-style)

**Purpose:** No single leader, clients write to multiple nodes, quorum for consistency.

```
┌──────────────────────────────────────────────────────┐
│          Leaderless Replication (N=5, W=3, R=2)      │
│                                                       │
│ Write Operation:                                      │
│                                                       │
│ Client ─┬──► Node 1 (ACK) ─┐                         │
│         ├──► Node 2 (ACK) ─┤                         │
│         ├──► Node 3 (ACK) ─┼─ W=3 quorum satisfied   │
│         ├──► Node 4 (timeout)                         │
│         └──► Node 5 (failed)                          │
│                            │                          │
│                   SUCCESS ◄┘                          │
│                                                       │
│ Read Operation:                                       │
│                                                       │
│ Client ─┬──► Node 1 (v=5, timestamp=T5)              │
│         ├──► Node 2 (v=5, timestamp=T5)              │
│         └──► Node 3 (v=4, timestamp=T3) [stale]      │
│              │                                         │
│              └─ R=2 quorum satisfied                  │
│                 Return v=5 (most recent)              │
│                 Repair Node 3 in background           │
│                                                       │
│ Consistency Rule: W + R > N                           │
│   W=3, R=2, N=5 → 3+2=5 > 5 ✓ (overlap guaranteed)  │
└──────────────────────────────────────────────────────┘
```

**Quorum Configurations:**

| Configuration | W | R | N | Consistency | Use Case |
|--------------|---|---|---|-------------|----------|
| Strong       | 3 | 3 | 5 | Strong      | Banking |
| Balanced     | 3 | 2 | 5 | Strong      | Default |
| Write-heavy  | 2 | 3 | 5 | Strong      | Logs |
| Read-heavy   | 3 | 1 | 5 | Eventual    | Cache |
| Max Avail    | 1 | 1 | 5 | Eventual    | Analytics |

**Implementation (Cassandra):**
```sql
-- Create keyspace with replication
CREATE KEYSPACE my_app WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'datacenter1': 3,
  'datacenter2': 2
};

-- Write with quorum
INSERT INTO users (id, name) VALUES (123, 'Alice')
  USING CONSISTENCY QUORUM;

-- Read with quorum
SELECT * FROM users WHERE id = 123
  USING CONSISTENCY QUORUM;

-- Tunable consistency per query
SELECT * FROM users WHERE id = 123
  USING CONSISTENCY ONE;  -- Eventual (fast)
```

**Read Repair and Anti-Entropy:**
```
READ REPAIR:
  Client reads from 3 nodes
    ├─ Node 1: version 5
    ├─ Node 2: version 5
    └─ Node 3: version 4 (stale)
  Return version 5 to client
  Background: Repair Node 3 → version 5

ANTI-ENTROPY (Gossip):
  Nodes periodically exchange Merkle trees
  Detect divergences
  Synchronize missing data
```

**When to Use:**
- Maximum availability required
- Multi-datacenter
- Can tolerate eventual consistency (or configure strong quorum)

**Examples:**
- Cassandra
- DynamoDB
- Riak

---

## Resilience and Fault Tolerance Patterns

### Pattern 1: Circuit Breaker

**Purpose:** Prevent cascading failures by failing fast when downstream service is unhealthy.

```
┌──────────────────────────────────────────────────────┐
│              Circuit Breaker State Machine           │
│                                                       │
│                   ┌─────────┐                        │
│                   │ CLOSED  │                        │
│         ┌─────────│(Normal) │◄────────┐              │
│         │         └────┬────┘         │              │
│         │              │               │              │
│         │ Success      │ Failure       │ Success      │
│         │ count        │ threshold     │ (health)     │
│         │ reset        │ exceeded      │ restored     │
│         │              │               │              │
│         │         ┌────▼────┐          │              │
│         │         │  OPEN   │          │              │
│         │         │(Failing)│──────────┘              │
│         │         └────┬────┘                         │
│         │              │                               │
│         │              │ Timeout                       │
│         │              │ elapsed                       │
│         │              │                               │
│         │         ┌────▼────┐                         │
│         └────────►│   HALF  │                         │
│           Fail    │  OPEN   │                         │
│                   │(Testing)│                         │
│                   └─────────┘                         │
│                                                       │
│ CLOSED:    Pass through all requests                 │
│            Track failure rate                         │
│                                                       │
│ OPEN:      Fail immediately (no downstream call)     │
│            Return cached/default response             │
│                                                       │
│ HALF-OPEN: Allow limited requests to test            │
│            If successful → CLOSED                     │
│            If failed → OPEN                           │
└──────────────────────────────────────────────────────┘
```

**Implementation:**

```python
import time
from enum import Enum
from typing import Callable, Any

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self,
                 failure_threshold: int = 5,
                 timeout: float = 60.0,
                 expected_exception: Exception = Exception):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.timeout:
                self.state = CircuitState.HALF_OPEN
                self.failure_count = 0
            else:
                raise Exception("Circuit breaker OPEN - failing fast")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage
import requests

def call_api():
    response = requests.get('http://api.example.com/data', timeout=5)
    response.raise_for_status()
    return response.json()

breaker = CircuitBreaker(failure_threshold=3, timeout=30)

try:
    data = breaker.call(call_api)
    print(data)
except Exception as e:
    print(f"Request failed: {e}")
    # Return cached data or default value
```

**When to Use:**
- Calling external services (APIs, databases, microservices)
- Preventing cascading failures
- Graceful degradation

**Configuration Guidelines:**
- **Failure threshold:** 3-10 failures (depends on traffic volume)
- **Timeout:** 30-120 seconds (time to recover)
- **Half-open requests:** 1-3 (test carefully)

### Pattern 2: Bulkhead Isolation

**Purpose:** Isolate resources to prevent one failing component from exhausting shared resources.

```
┌──────────────────────────────────────────────────────┐
│              Bulkhead Isolation Pattern              │
│                                                       │
│ WITHOUT BULKHEAD (Shared Thread Pool):               │
│                                                       │
│ ┌────────────────────────────────┐                   │
│ │    Shared Thread Pool (10)     │                   │
│ ├────────────────────────────────┤                   │
│ │ Payment API (all 10 threads)   │ ← Blocked!        │
│ │ ███████████████████████████    │                   │
│ │                                 │                   │
│ │ User API (0 threads)            │ ← Starved!        │
│ │ Order API (0 threads)           │ ← Starved!        │
│ └────────────────────────────────┘                   │
│ Problem: One slow service blocks everything          │
│                                                       │
│ WITH BULKHEAD (Isolated Pools):                      │
│                                                       │
│ ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│ │ Payment Pool │  │  User Pool   │  │ Order Pool  │ │
│ │  (4 threads) │  │  (3 threads) │  │ (3 threads) │ │
│ ├──────────────┤  ├──────────────┤  ├─────────────┤ │
│ │ ████         │  │ ███          │  │ ███         │ │
│ │ Slow but     │  │ Available!   │  │ Available!  │ │
│ │ contained    │  │              │  │             │ │
│ └──────────────┘  └──────────────┘  └─────────────┘ │
│ Benefit: Isolated failure, other services work       │
└──────────────────────────────────────────────────────┘
```

**Implementation (Thread Pool Isolation):**

```python
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

class Bulkhead:
    def __init__(self, name: str, max_workers: int = 5):
        self.name = name
        self.executor = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix=f"{name}-bulkhead"
        )

    def execute(self, func, *args, **kwargs):
        future = self.executor.submit(func, *args, **kwargs)
        return future.result()  # Blocks until complete

# Create isolated bulkheads
payment_bulkhead = Bulkhead("payment", max_workers=4)
user_bulkhead = Bulkhead("user", max_workers=3)
order_bulkhead = Bulkhead("order", max_workers=3)

# Usage
def call_payment_api():
    # Slow API call
    import time
    time.sleep(5)
    return {"status": "success"}

def call_user_api():
    # Fast API call
    return {"user": "Alice"}

# Even if payment is slow, user API still works
payment_result = payment_bulkhead.execute(call_payment_api)
user_result = user_bulkhead.execute(call_user_api)  # Not blocked!
```

**When to Use:**
- Microservices architecture
- Multiple downstream dependencies
- Prevent resource exhaustion

**Bulkhead Types:**
1. **Thread pool isolation** (shown above)
2. **Semaphore isolation** (limit concurrent requests)
3. **Process isolation** (separate processes)
4. **Container isolation** (Kubernetes resource limits)

### Pattern 3: Timeout and Retry

**Purpose:** Prevent indefinite waiting and recover from transient failures.

```
┌──────────────────────────────────────────────────────┐
│           Timeout and Retry Strategy                 │
│                                                       │
│ EXPONENTIAL BACKOFF with JITTER:                     │
│                                                       │
│ Attempt 1: ───X (timeout 2s)                         │
│                │                                      │
│                └─ Wait: 1s + jitter(0-500ms)         │
│                   │                                   │
│ Attempt 2:        └───X (timeout 2s)                 │
│                       │                               │
│                       └─ Wait: 2s + jitter(0-1s)     │
│                          │                            │
│ Attempt 3:               └───X (timeout 2s)          │
│                              │                        │
│                              └─ Wait: 4s + jitter     │
│                                 │                     │
│ Attempt 4:                      └───✓ (success)      │
│                                                       │
│ Formula:                                              │
│   wait = min(max_wait, base * 2^attempt) + jitter    │
│   jitter = random(0, wait * 0.1)                     │
└──────────────────────────────────────────────────────┘
```

**Implementation:**

```python
import time
import random
from typing import Callable, Any

class RetryConfig:
    def __init__(self,
                 max_attempts: int = 3,
                 base_delay: float = 1.0,
                 max_delay: float = 60.0,
                 timeout: float = 5.0,
                 exponential: bool = True,
                 jitter: bool = True):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.timeout = timeout
        self.exponential = exponential
        self.jitter = jitter

def retry_with_backoff(config: RetryConfig):
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(config.max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == config.max_attempts - 1:
                        raise  # Last attempt, re-raise

                    # Calculate delay
                    if config.exponential:
                        delay = min(
                            config.max_delay,
                            config.base_delay * (2 ** attempt)
                        )
                    else:
                        delay = config.base_delay

                    # Add jitter
                    if config.jitter:
                        jitter = random.uniform(0, delay * 0.1)
                        delay += jitter

                    print(f"Attempt {attempt+1} failed: {e}. "
                          f"Retrying in {delay:.2f}s...")
                    time.sleep(delay)

        return wrapper
    return decorator

# Usage
config = RetryConfig(
    max_attempts=4,
    base_delay=1.0,
    max_delay=30.0,
    exponential=True,
    jitter=True
)

@retry_with_backoff(config)
def call_unreliable_api():
    import requests
    response = requests.get('http://api.example.com/data', timeout=5)
    response.raise_for_status()
    return response.json()

# Will retry up to 4 times with exponential backoff
data = call_unreliable_api()
```

**Retry Guidelines:**

| Error Type | Retry? | Strategy |
|------------|--------|----------|
| Network timeout | ✅ Yes | Exponential backoff |
| 500 Internal Server Error | ✅ Yes | Exponential backoff |
| 503 Service Unavailable | ✅ Yes | Exponential backoff |
| 429 Rate Limited | ✅ Yes | Use Retry-After header |
| 400 Bad Request | ❌ No | Client error, won't succeed |
| 401 Unauthorized | ❌ No | Fix auth first |
| 404 Not Found | ❌ No | Resource doesn't exist |

**When to Use:**
- Network calls (APIs, databases)
- Transient failures
- Rate-limited services

### Pattern 4: Rate Limiting and Backpressure

**Purpose:** Protect services from overload by limiting request rate.

```
┌──────────────────────────────────────────────────────┐
│              Rate Limiting Algorithms                │
│                                                       │
│ 1. TOKEN BUCKET:                                     │
│                                                       │
│    ┌──────────────┐                                  │
│    │    Bucket    │  Capacity: 100 tokens            │
│    │  [████████]  │  Refill: 10 tokens/sec           │
│    └──────────────┘                                  │
│         │                                             │
│    Request arrives → Take 1 token                    │
│    │                                                  │
│    ├─ Tokens available? → Allow                      │
│    └─ Tokens empty? → Reject (429)                   │
│                                                       │
│ 2. LEAKY BUCKET:                                     │
│                                                       │
│    Requests    ┌──────────────┐                      │
│       │        │    Buffer    │  Process at          │
│       ▼        │  [████████]  │  constant rate       │
│    Queue here  └──────┬───────┘                      │
│                       │ Drip (constant)              │
│                       ▼                               │
│                   Process                             │
│                                                       │
│ 3. SLIDING WINDOW:                                   │
│                                                       │
│    Last 60 seconds:  [════════════════════]          │
│    Requests: 95/100  [█████████████████  ]           │
│                      Allow ✓                         │
│                                                       │
│    Last 60 seconds:  [════════════════════]          │
│    Requests: 100/100 [████████████████████]          │
│                      Reject ✗ (limit reached)        │
└──────────────────────────────────────────────────────┘
```

**Implementation (Token Bucket):**

```python
import time
from threading import Lock

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        """
        capacity: Maximum tokens
        refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = Lock()

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate

        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

    def consume(self, tokens: int = 1) -> bool:
        with self.lock:
            self._refill()

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

# Usage
rate_limiter = TokenBucket(capacity=100, refill_rate=10.0)

def handle_request():
    if rate_limiter.consume(1):
        # Process request
        return {"status": "success"}
    else:
        # Rate limited
        return {"error": "Rate limit exceeded"}, 429

# API integration
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api/data')
def api_endpoint():
    if not rate_limiter.consume():
        return jsonify({"error": "Rate limit exceeded"}), 429

    # Process request
    return jsonify({"data": "value"})
```

**Backpressure Strategies:**

```python
# 1. Queue with max size (drop oldest)
from collections import deque

class BackpressureQueue:
    def __init__(self, max_size: int):
        self.queue = deque(maxlen=max_size)

    def push(self, item):
        if len(self.queue) >= self.queue.maxlen:
            # Drop oldest
            self.queue.popleft()
        self.queue.append(item)

# 2. Reject when overloaded
def handle_with_backpressure(queue_size: int):
    if get_queue_size() > queue_size:
        return {"error": "Service overloaded"}, 503

    # Process request
    process_request()

# 3. Adaptive rate limiting
class AdaptiveRateLimiter:
    def __init__(self):
        self.error_rate = 0.0
        self.limit = 100

    def adjust_limit(self, success: bool):
        if success:
            # Decrease error rate
            self.error_rate *= 0.95
            # Increase limit
            self.limit = min(1000, self.limit * 1.01)
        else:
            # Increase error rate
            self.error_rate = self.error_rate * 0.95 + 0.05
            # Decrease limit if error rate high
            if self.error_rate > 0.1:
                self.limit = max(10, self.limit * 0.9)
```

**When to Use:**
- Public APIs (prevent abuse)
- Protect downstream services
- Fair resource allocation
- Cost control (pay-per-request services)

---

## Transaction Patterns (Saga, Event Sourcing, CQRS)

### Pattern 1: Saga Pattern

**Purpose:** Manage distributed transactions across microservices using compensating transactions.

```
┌──────────────────────────────────────────────────────┐
│              Saga Pattern: Order Workflow            │
│                                                       │
│ CHOREOGRAPHY (Event-Driven):                         │
│                                                       │
│ Order Service    Payment Service    Inventory Service│
│      │                 │                   │          │
│      │ CreateOrder     │                   │          │
│      ├────────────────►│                   │          │
│      │                 │ OrderCreated      │          │
│      │                 │ event             │          │
│      │                 ├──────────────────►│          │
│      │                 │                   │          │
│      │                 │ ReserveInventory  │          │
│      │                 │◄──────────────────┤          │
│      │                 │                   │          │
│      │                 │ InventoryReserved │          │
│      │◄────────────────┤                   │          │
│      │                 │                   │          │
│      │ ChargePayment   │                   │          │
│      ├────────────────►│                   │          │
│      │                 │                   │          │
│      │ PaymentSuccess  │                   │          │
│      │◄────────────────┤                   │          │
│      │                 │                   │          │
│      │        ✓ Order Complete             │          │
│                                                       │
│ FAILURE SCENARIO (Compensating Transactions):        │
│                                                       │
│ Order Service    Payment Service    Inventory Service│
│      │                 │                   │          │
│      │ CreateOrder     │                   │          │
│      ├────────────────►│                   │          │
│      │                 │ ReserveInventory  │          │
│      │                 ├──────────────────►│          │
│      │                 │                   │          │
│      │                 │ InventoryReserved │          │
│      │                 │◄──────────────────┤          │
│      │                 │                   │          │
│      │ ChargePayment   │                   │          │
│      ├────────────────►│                   │          │
│      │                 │                   │          │
│      │ PaymentFailed   │                   │          │
│      │◄────────────────┤                   │          │
│      │                 │                   │          │
│      │ COMPENSATE: ReleaseInventory        │          │
│      ├─────────────────┼──────────────────►│          │
│      │                 │                   │          │
│      │ CancelOrder     │                   │          │
│      ├────────────────►│                   │          │
│      │                 │                   │          │
│      │        ✗ Order Cancelled            │          │
└──────────────────────────────────────────────────────┘
```

**Choreography vs Orchestration:**

```
CHOREOGRAPHY (Decentralized):
  - Services listen to events
  - No central coordinator
  - Each service knows next step
  - Pro: Loose coupling
  - Con: Hard to understand flow

ORCHESTRATION (Centralized):
  - Central orchestrator controls flow
  - Orchestrator calls services
  - Clear workflow definition
  - Pro: Easy to understand/debug
  - Con: Orchestrator is single point of failure
```

**Orchestration Example:**

```python
from enum import Enum
from typing import List, Callable

class SagaStepStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    COMPENSATED = "compensated"

class SagaStep:
    def __init__(self,
                 name: str,
                 action: Callable,
                 compensation: Callable):
        self.name = name
        self.action = action
        self.compensation = compensation
        self.status = SagaStepStatus.PENDING

class SagaOrchestrator:
    def __init__(self):
        self.steps: List[SagaStep] = []
        self.completed_steps: List[SagaStep] = []

    def add_step(self, step: SagaStep):
        self.steps.append(step)

    def execute(self):
        try:
            # Execute forward steps
            for step in self.steps:
                print(f"Executing: {step.name}")
                step.action()
                step.status = SagaStepStatus.SUCCESS
                self.completed_steps.append(step)

            print("Saga completed successfully!")
            return True

        except Exception as e:
            print(f"Saga failed at {step.name}: {e}")
            # Execute compensating transactions in reverse
            self._compensate()
            return False

    def _compensate(self):
        print("Compensating transactions...")
        for step in reversed(self.completed_steps):
            try:
                print(f"Compensating: {step.name}")
                step.compensation()
                step.status = SagaStepStatus.COMPENSATED
            except Exception as e:
                print(f"Compensation failed for {step.name}: {e}")

# Example: Order saga
class OrderSaga:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.orchestrator = SagaOrchestrator()

        # Define saga steps
        self.orchestrator.add_step(SagaStep(
            name="Create Order",
            action=self.create_order,
            compensation=self.cancel_order
        ))

        self.orchestrator.add_step(SagaStep(
            name="Reserve Inventory",
            action=self.reserve_inventory,
            compensation=self.release_inventory
        ))

        self.orchestrator.add_step(SagaStep(
            name="Charge Payment",
            action=self.charge_payment,
            compensation=self.refund_payment
        ))

        self.orchestrator.add_step(SagaStep(
            name="Send Confirmation",
            action=self.send_confirmation,
            compensation=self.send_cancellation
        ))

    def create_order(self):
        print(f"Creating order {self.order_id}")
        # Call Order Service API

    def cancel_order(self):
        print(f"Cancelling order {self.order_id}")
        # Compensating action

    def reserve_inventory(self):
        print(f"Reserving inventory for {self.order_id}")
        # Call Inventory Service API
        # Simulate failure:
        # raise Exception("Out of stock")

    def release_inventory(self):
        print(f"Releasing inventory for {self.order_id}")
        # Compensating action

    def charge_payment(self):
        print(f"Charging payment for {self.order_id}")
        # Call Payment Service API

    def refund_payment(self):
        print(f"Refunding payment for {self.order_id}")
        # Compensating action

    def send_confirmation(self):
        print(f"Sending confirmation for {self.order_id}")
        # Call Notification Service

    def send_cancellation(self):
        print(f"Sending cancellation for {self.order_id}")
        # Compensating action

    def execute(self):
        return self.orchestrator.execute()

# Usage
saga = OrderSaga("order-123")
success = saga.execute()
```

**When to Use Sagas:**
- Distributed transactions across microservices
- Long-running business processes
- Need to maintain eventual consistency
- Two-phase commit (2PC) not feasible

**Saga Best Practices:**
1. Design compensating transactions carefully
2. Idempotent operations (safe to retry)
3. Persist saga state (survive failures)
4. Timeout handling
5. Monitoring and observability

### Pattern 2: Event Sourcing

**Purpose:** Store all changes to application state as a sequence of events, enabling audit trails and state reconstruction.

```
┌──────────────────────────────────────────────────────┐
│              Event Sourcing Pattern                  │
│                                                       │
│ TRADITIONAL (CRUD):                                  │
│                                                       │
│ ┌──────────────┐                                     │
│ │   Database   │                                     │
│ ├──────────────┤                                     │
│ │ user_id: 123 │                                     │
│ │ balance: 100 │  ← Current state only               │
│ │ status: act. │    (history lost)                   │
│ └──────────────┘                                     │
│                                                       │
│ EVENT SOURCING:                                      │
│                                                       │
│ ┌────────────────────────────────────┐               │
│ │         Event Store                │               │
│ ├────────────────────────────────────┤               │
│ │ 1. AccountCreated(123, name=Alice) │               │
│ │ 2. MoneyDeposited(123, amount=100) │               │
│ │ 3. MoneyWithdrawn(123, amount=20)  │               │
│ │ 4. MoneyDeposited(123, amount=50)  │               │
│ └────────────────────────────────────┘               │
│              │                                        │
│              │ Replay events                          │
│              ▼                                        │
│ ┌────────────────────────────────────┐               │
│ │   Current State (Projection)       │               │
│ ├────────────────────────────────────┤               │
│ │ user_id: 123                       │               │
│ │ balance: 130  (100 - 20 + 50)      │               │
│ │ status: active                     │               │
│ └────────────────────────────────────┘               │
│                                                       │
│ Benefits:                                             │
│ - Complete audit trail                                │
│ - Time travel (replay to any point)                   │
│ - Debug production issues                             │
│ - Multiple projections from same events               │
└──────────────────────────────────────────────────────┘
```

**Implementation:**

```python
from datetime import datetime
from typing import List, Dict, Any
from abc import ABC, abstractmethod

class Event(ABC):
    def __init__(self):
        self.timestamp = datetime.utcnow()
        self.event_id = None  # Set by event store

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

class AccountCreated(Event):
    def __init__(self, account_id: str, owner: str):
        super().__init__()
        self.account_id = account_id
        self.owner = owner

    def to_dict(self):
        return {
            "type": "AccountCreated",
            "account_id": self.account_id,
            "owner": self.owner,
            "timestamp": self.timestamp.isoformat()
        }

class MoneyDeposited(Event):
    def __init__(self, account_id: str, amount: float):
        super().__init__()
        self.account_id = account_id
        self.amount = amount

    def to_dict(self):
        return {
            "type": "MoneyDeposited",
            "account_id": self.account_id,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat()
        }

class MoneyWithdrawn(Event):
    def __init__(self, account_id: str, amount: float):
        super().__init__()
        self.account_id = account_id
        self.amount = amount

    def to_dict(self):
        return {
            "type": "MoneyWithdrawn",
            "account_id": self.account_id,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat()
        }

class EventStore:
    def __init__(self):
        self.events: List[Event] = []

    def append(self, event: Event):
        event.event_id = len(self.events)
        self.events.append(event)

    def get_events(self, aggregate_id: str) -> List[Event]:
        # Filter events for specific aggregate
        return [e for e in self.events
                if hasattr(e, 'account_id') and e.account_id == aggregate_id]

class BankAccount:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.owner = None
        self.balance = 0.0
        self.version = 0

    def apply_event(self, event: Event):
        if isinstance(event, AccountCreated):
            self.owner = event.owner
        elif isinstance(event, MoneyDeposited):
            self.balance += event.amount
        elif isinstance(event, MoneyWithdrawn):
            self.balance -= event.amount
        self.version += 1

    @staticmethod
    def from_events(events: List[Event]) -> 'BankAccount':
        account = None
        for event in events:
            if isinstance(event, AccountCreated):
                account = BankAccount(event.account_id)
            if account:
                account.apply_event(event)
        return account

# Usage
event_store = EventStore()

# Create account
event1 = AccountCreated("acc-123", "Alice")
event_store.append(event1)

# Deposit money
event2 = MoneyDeposited("acc-123", 100.0)
event_store.append(event2)

# Withdraw money
event3 = MoneyWithdrawn("acc-123", 20.0)
event_store.append(event3)

# Deposit more
event4 = MoneyDeposited("acc-123", 50.0)
event_store.append(event4)

# Rebuild current state from events
events = event_store.get_events("acc-123")
account = BankAccount.from_events(events)

print(f"Account: {account.account_id}")
print(f"Owner: {account.owner}")
print(f"Balance: {account.balance}")  # 130.0
print(f"Version: {account.version}")
```

**Event Store Technologies:**
- **EventStoreDB:** Purpose-built event store
- **Kafka:** Event streaming platform
- **DynamoDB Streams:** AWS event streams
- **PostgreSQL:** Can store events (with ordering)

**When to Use Event Sourcing:**
- Audit requirements (financial, healthcare)
- Complex business logic (need to replay)
- Temporal queries ("what was balance on Jan 1?")
- Debugging production issues
- Multiple read models from same events

**Challenges:**
- Event schema evolution
- Event versioning
- Snapshot optimization (avoid replaying millions of events)
- Query complexity (need projections)

### Pattern 3: CQRS (Command Query Responsibility Segregation)

**Purpose:** Separate read and write models for optimized performance and scalability.

```
┌──────────────────────────────────────────────────────┐
│                  CQRS Pattern                        │
│                                                       │
│ TRADITIONAL (Shared Model):                          │
│                                                       │
│ ┌─────────┐                                          │
│ │ Client  │                                          │
│ └────┬────┘                                          │
│      │                                                │
│      ├─── Write ──►┐                                 │
│      │             ├─► Single Model ──► Database     │
│      └─── Read ───►┘                                 │
│                                                       │
│ Problem: Reads and writes have different needs       │
│                                                       │
│ CQRS (Separate Models):                              │
│                                                       │
│ ┌─────────┐                                          │
│ │ Client  │                                          │
│ └────┬────┘                                          │
│      │                                                │
│      ├─── Command ──► ┌──────────────┐              │
│      │                │ Write Model   │              │
│      │                │  (Normalized) │              │
│      │                └───────┬───────┘              │
│      │                        │                       │
│      │                        │ Events/Changes        │
│      │                        ▼                       │
│      │                  ┌──────────┐                 │
│      │                  │Event Bus │                 │
│      │                  └─────┬────┘                 │
│      │                        │                       │
│      │                        │ Update projections    │
│      │                        ▼                       │
│      │                ┌──────────────┐               │
│      └─── Query ────► │ Read Models  │               │
│                       │ (Denormalized)│               │
│                       │ - SQL view    │               │
│                       │ - Elasticsearch│               │
│                       │ - Redis cache │               │
│                       └──────────────┘               │
│                                                       │
│ Benefits:                                             │
│ - Optimized writes (normalized, transactional)       │
│ - Optimized reads (denormalized, cached)             │
│ - Independent scaling                                 │
│ - Multiple read models from same data                 │
└──────────────────────────────────────────────────────┘
```

**Implementation:**

```python
from typing import List
from dataclasses import dataclass

# Command side (Write model)
@dataclass
class CreateOrderCommand:
    order_id: str
    customer_id: str
    items: List[dict]

@dataclass
class AddItemCommand:
    order_id: str
    item_id: str
    quantity: int

class OrderWriteModel:
    """Normalized write model - focused on consistency"""
    def __init__(self, db):
        self.db = db

    def handle_create_order(self, command: CreateOrderCommand):
        # Validate business rules
        if self.db.order_exists(command.order_id):
            raise ValueError("Order already exists")

        # Write to normalized tables
        self.db.insert_order({
            "order_id": command.order_id,
            "customer_id": command.customer_id,
            "status": "pending"
        })

        for item in command.items:
            self.db.insert_order_item({
                "order_id": command.order_id,
                "item_id": item["id"],
                "quantity": item["qty"]
            })

        # Publish event for read model update
        self.publish_event({
            "type": "OrderCreated",
            "order_id": command.order_id,
            "customer_id": command.customer_id,
            "items": command.items
        })

    def publish_event(self, event):
        # Send to message bus (Kafka, RabbitMQ, etc.)
        pass

# Query side (Read model)
class OrderReadModel:
    """Denormalized read model - optimized for queries"""
    def __init__(self, cache, search):
        self.cache = cache  # Redis
        self.search = search  # Elasticsearch

    def get_order_summary(self, order_id: str):
        # Try cache first
        cached = self.cache.get(f"order:{order_id}")
        if cached:
            return cached

        # Fallback to search index
        result = self.search.get("orders", order_id)

        # Cache for next time
        self.cache.set(f"order:{order_id}", result, expire=3600)
        return result

    def search_customer_orders(self, customer_id: str):
        # Use Elasticsearch for complex queries
        return self.search.search("orders", {
            "query": {
                "term": {"customer_id": customer_id}
            },
            "sort": [{"created_at": "desc"}]
        })

# Event handler (Updates read model)
class OrderReadModelUpdater:
    def __init__(self, read_model: OrderReadModel):
        self.read_model = read_model

    def handle_order_created(self, event):
        # Update Elasticsearch
        order_doc = {
            "order_id": event["order_id"],
            "customer_id": event["customer_id"],
            "items": event["items"],
            "total_items": len(event["items"]),
            "created_at": datetime.utcnow()
        }
        self.read_model.search.index("orders", event["order_id"], order_doc)

        # Update cache
        self.read_model.cache.set(
            f"order:{event['order_id']}",
            order_doc,
            expire=3600
        )

# Usage
write_model = OrderWriteModel(database)
read_model = OrderReadModel(redis_cache, elasticsearch)

# Command (Write)
command = CreateOrderCommand(
    order_id="order-123",
    customer_id="cust-456",
    items=[{"id": "item1", "qty": 2}]
)
write_model.handle_create_order(command)

# Query (Read)
order = read_model.get_order_summary("order-123")
customer_orders = read_model.search_customer_orders("cust-456")
```

**CQRS Read Model Strategies:**

| Strategy | Use Case | Technology |
|----------|----------|------------|
| **SQL View** | Complex joins | PostgreSQL materialized views |
| **Cache** | Hot data | Redis, Memcached |
| **Search** | Full-text, facets | Elasticsearch, Algolia |
| **Graph** | Relationships | Neo4j |
| **Time-series** | Metrics, logs | InfluxDB, TimescaleDB |
| **Document** | Flexible schema | MongoDB |

**When to Use CQRS:**
- Read/write patterns vastly different
- Need multiple read models (admin, user, analytics)
- High read-to-write ratio (10:1 or higher)
- Complex querying requirements
- Often paired with Event Sourcing

**Challenges:**
- Eventual consistency (read model lags write model)
- Complexity (two models to maintain)
- Data synchronization
- Debugging (harder than single model)

---

## Service Discovery and Communication

### Pattern 1: Client-Side Service Discovery

**Purpose:** Client queries service registry and load balances directly.

```
┌──────────────────────────────────────────────────────┐
│          Client-Side Service Discovery              │
│                                                       │
│ ┌────────────────────────────────────────┐           │
│ │         Service Registry               │           │
│ │         (Consul, etcd, Eureka)         │           │
│ ├────────────────────────────────────────┤           │
│ │ Service A: [10.0.1.5:8080,             │           │
│ │             10.0.1.6:8080,             │           │
│ │             10.0.1.7:8080]             │           │
│ └─────────▲──────────────────────────────┘           │
│           │                                           │
│           │ (1) Register                              │
│           │                                           │
│   ┌───────┴────┬──────────┬──────────┐               │
│   │            │          │          │               │
│   │            │          │          │               │
│ ┌─▼─────┐  ┌──▼────┐  ┌──▼────┐  ┌──▼────┐         │
│ │Service│  │Service│  │Service│  │Service│         │
│ │A:8080 │  │A:8080 │  │A:8080 │  │B:9090 │         │
│ └───────┘  └───────┘  └───────┘  └───▲───┘         │
│                                       │              │
│                                       │ (3) Call     │
│ ┌───────────────┐                     │              │
│ │    Client     │                     │              │
│ │               │─────────────────────┘              │
│ │ (2) Query registry for Service B                  │
│ │ (3) Load balance and call                         │
│ └───────────────┘                                    │
│                                                       │
│ Flow:                                                 │
│ 1. Services register with registry on startup        │
│ 2. Client queries registry for service instances     │
│ 3. Client selects instance (round-robin, random)     │
│ 4. Client calls service directly                     │
└──────────────────────────────────────────────────────┘
```

**Implementation (Consul):**

```python
import consul
import random
import requests

class ServiceDiscovery:
    def __init__(self, consul_host='localhost', consul_port=8500):
        self.consul = consul.Consul(host=consul_host, port=consul_port)

    def register_service(self, service_name: str, service_id: str,
                        host: str, port: int, health_check_url: str):
        """Register service with Consul"""
        self.consul.agent.service.register(
            name=service_name,
            service_id=service_id,
            address=host,
            port=port,
            check=consul.Check.http(
                health_check_url,
                interval='10s',
                timeout='5s'
            )
        )

    def deregister_service(self, service_id: str):
        """Deregister service"""
        self.consul.agent.service.deregister(service_id)

    def discover_service(self, service_name: str) -> list:
        """Discover healthy service instances"""
        index, services = self.consul.health.service(
            service_name,
            passing=True  # Only healthy instances
        )

        instances = []
        for service in services:
            instances.append({
                'host': service['Service']['Address'],
                'port': service['Service']['Port']
            })
        return instances

    def call_service(self, service_name: str, path: str):
        """Call service with client-side load balancing"""
        instances = self.discover_service(service_name)

        if not instances:
            raise Exception(f"No healthy instances of {service_name}")

        # Client-side load balancing (random)
        instance = random.choice(instances)
        url = f"http://{instance['host']}:{instance['port']}{path}"

        response = requests.get(url, timeout=5)
        return response.json()

# Usage
sd = ServiceDiscovery()

# Register service
sd.register_service(
    service_name='payment-service',
    service_id='payment-1',
    host='10.0.1.5',
    port=8080,
    health_check_url='http://10.0.1.5:8080/health'
)

# Discover and call
result = sd.call_service('payment-service', '/api/charge')
```

**When to Use:**
- Microservices architecture
- Need fine-grained control over load balancing
- Client can handle discovery logic

**Pros:**
- ✅ No extra network hop
- ✅ Client controls load balancing strategy

**Cons:**
- ❌ Client complexity (every client needs discovery logic)
- ❌ Multiple languages = multiple implementations

### Pattern 2: Server-Side Service Discovery (API Gateway)

**Purpose:** Central gateway handles service discovery and routing.

```
┌──────────────────────────────────────────────────────┐
│          Server-Side Service Discovery              │
│                                                       │
│ ┌────────────┐                                       │
│ │   Client   │                                       │
│ └──────┬─────┘                                       │
│        │                                              │
│        │ (1) Call via gateway                         │
│        │     GET /api/payments/123                    │
│        ▼                                              │
│ ┌────────────────────────────────┐                   │
│ │       API Gateway              │                   │
│ │       (Kong, Nginx, Traefik)   │                   │
│ │                                 │                   │
│ │ (2) Query service registry      │                   │
│ │ (3) Load balance                │                   │
│ │ (4) Route to service            │                   │
│ └──────┬─────────────────────────┘                   │
│        │                                              │
│        │ (2) Discover payment service instances       │
│        ▼                                              │
│ ┌────────────────────────────────┐                   │
│ │     Service Registry           │                   │
│ │     (Consul, Eureka)           │                   │
│ └────────────────────────────────┘                   │
│                                                       │
│        │ (4) Forward request                          │
│   ┌────┴───┬──────────┬──────────┐                   │
│   │        │          │          │                   │
│ ┌─▼─────┐┌─▼─────┐┌──▼─────┐┌───▼────┐             │
│ │Payment││Payment││Payment ││Order   │             │
│ │Service││Service││Service ││Service │             │
│ │:8080  ││:8080  ││:8080   ││:9090   │             │
│ └───────┘└───────┘└────────┘└────────┘             │
│                                                       │
│ Benefits:                                             │
│ - Client simplicity (single endpoint)                │
│ - Centralized cross-cutting concerns                 │
│ - Protocol translation (HTTP → gRPC)                 │
└──────────────────────────────────────────────────────┘
```

**When to Use:**
- Public-facing APIs
- Need centralized auth, rate limiting, logging
- Clients can't handle discovery

**Pros:**
- ✅ Client simplicity
- ✅ Centralized policies
- ✅ Protocol translation

**Cons:**
- ❌ Extra network hop (latency)
- ❌ Gateway is single point of failure
- ❌ Potential bottleneck

### Pattern 3: Service Mesh

**Purpose:** Dedicated infrastructure layer for service-to-service communication with sidecar proxies.

```
┌──────────────────────────────────────────────────────┐
│              Service Mesh (Istio/Linkerd)            │
│                                                       │
│ ┌─────────────────────────────────────────────────┐  │
│ │           Control Plane                          │  │
│ │  (Service Discovery, Config, Telemetry)          │  │
│ └──────────────────┬───────────────────────────────┘  │
│                    │ Configure proxies                │
│   ┌────────────────┼────────────────┐                 │
│   │                │                │                 │
│   ▼                ▼                ▼                 │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐     │
│ │  Service A  │ │  Service B  │ │  Service C  │     │
│ ├─────────────┤ ├─────────────┤ ├─────────────┤     │
│ │   App       │ │   App       │ │   App       │     │
│ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘     │
│        │                │                │            │
│ ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐     │
│ │  Sidecar    │ │  Sidecar    │ │  Sidecar    │     │
│ │  Proxy      │◄┼─Proxy       │◄┼─Proxy       │     │
│ │  (Envoy)    │ │  (Envoy)    │ │  (Envoy)    │     │
│ └─────────────┘ └─────────────┘ └─────────────┘     │
│                                                       │
│ Features:                                             │
│ - Service discovery (automatic)                       │
│ - Load balancing                                      │
│ - Circuit breaking                                    │
│ - Retries and timeouts                                │
│ - Distributed tracing                                 │
│ - Metrics collection                                  │
│ - mTLS encryption                                     │
└──────────────────────────────────────────────────────┘
```

**When to Use:**
- Kubernetes-based microservices
- Need observability, security, traffic management
- Many services (mesh shines at scale)

**Pros:**
- ✅ No code changes (sidecar injection)
- ✅ Unified observability
- ✅ mTLS encryption
- ✅ Advanced traffic management

**Cons:**
- ❌ Complexity (operational overhead)
- ❌ Performance overhead (extra proxy hop)
- ❌ Learning curve

**Popular Service Meshes:**
- **Istio:** Feature-rich, complex
- **Linkerd:** Lightweight, simpler
- **Consul Connect:** HashiCorp ecosystem
- **AWS App Mesh:** AWS-native

---

## Caching Strategies

### Pattern 1: Cache-Aside (Lazy Loading)

**Purpose:** Application manages cache explicitly, loads on demand.

```
┌──────────────────────────────────────────────────────┐
│              Cache-Aside Pattern                     │
│                                                       │
│ READ FLOW:                                            │
│                                                       │
│ ┌────────────┐                                       │
│ │    App     │                                       │
│ └──────┬─────┘                                       │
│        │                                              │
│        │ (1) Read key                                 │
│        ▼                                              │
│ ┌─────────────┐                                      │
│ │    Cache    │                                      │
│ │   (Redis)   │                                      │
│ └──────┬──────┘                                      │
│        │                                              │
│        ├─ Cache Hit? → Return value                  │
│        │                                              │
│        └─ Cache Miss?                                 │
│              │                                        │
│              │ (2) Query database                     │
│              ▼                                        │
│        ┌──────────────┐                              │
│        │   Database   │                              │
│        └──────┬───────┘                              │
│               │                                       │
│               │ (3) Return value                      │
│               ▼                                       │
│        ┌──────────────┐                              │
│        │     App      │                              │
│        │ (4) Write to cache                          │
│        └──────┬───────┘                              │
│               │                                       │
│               ▼                                       │
│        ┌──────────────┐                              │
│        │    Cache     │                              │
│        └──────────────┘                              │
│                                                       │
│ WRITE FLOW:                                           │
│                                                       │
│ App → (1) Write to DB → (2) Invalidate cache         │
└──────────────────────────────────────────────────────┘
```

**Implementation:**

```python
import redis
import json
from typing import Optional

class CacheAside:
    def __init__(self, redis_client: redis.Redis, db):
        self.cache = redis_client
        self.db = db
        self.ttl = 3600  # 1 hour

    def get(self, key: str) -> Optional[dict]:
        # Try cache first
        cached = self.cache.get(key)
        if cached:
            print(f"Cache HIT: {key}")
            return json.loads(cached)

        # Cache miss - query database
        print(f"Cache MISS: {key}")
        value = self.db.query(key)

        if value:
            # Populate cache for next time
            self.cache.setex(key, self.ttl, json.dumps(value))

        return value

    def set(self, key: str, value: dict):
        # Write to database
        self.db.write(key, value)

        # Invalidate cache (or update it)
        self.cache.delete(key)
        # Alternative: Update cache immediately
        # self.cache.setex(key, self.ttl, json.dumps(value))

# Usage
cache = CacheAside(redis.Redis(), database)

# First call: Cache miss, queries DB
user = cache.get('user:123')

# Second call: Cache hit, fast!
user = cache.get('user:123')

# Update: Invalidates cache
cache.set('user:123', {'name': 'Alice', 'email': 'alice@example.com'})
```

**When to Use:**
- Read-heavy workloads
- Application controls what to cache
- Can tolerate cache misses

**Pros:**
- ✅ Simple to understand
- ✅ Works with any cache
- ✅ Resilient (cache failure = slower, not down)

**Cons:**
- ❌ Initial request is slow (cold cache)
- ❌ Cache/DB consistency managed by app

### Pattern 2: Write-Through Cache

**Purpose:** Write to cache and database synchronously, always consistent.

```
┌──────────────────────────────────────────────────────┐
│              Write-Through Pattern                   │
│                                                       │
│ WRITE FLOW:                                           │
│                                                       │
│ ┌────────────┐                                       │
│ │    App     │                                       │
│ └──────┬─────┘                                       │
│        │                                              │
│        │ (1) Write data                               │
│        ▼                                              │
│ ┌─────────────┐                                      │
│ │    Cache    │                                      │
│ │   (Redis)   │                                      │
│ └──────┬──────┘                                      │
│        │                                              │
│        │ (2) Write to DB (sync)                       │
│        ▼                                              │
│ ┌──────────────┐                                     │
│ │   Database   │                                     │
│ └──────┬───────┘                                     │
│        │                                              │
│        │ (3) Success                                  │
│        ▼                                              │
│   Return to app                                       │
│                                                       │
│ READ FLOW:                                            │
│                                                       │
│ App → Read from cache (always up-to-date)            │
│                                                       │
│ Benefits:                                             │
│ - Cache always consistent with DB                     │
│ - Reads always fast (always cached)                   │
│                                                       │
│ Drawbacks:                                            │
│ - Writes slower (two writes)                          │
│ - Write latency increased                             │
└──────────────────────────────────────────────────────┘
```

**When to Use:**
- Consistency critical
- Read-heavy, write-light
- Can tolerate slower writes

### Pattern 3: Write-Behind (Write-Back)

**Purpose:** Write to cache immediately, asynchronously persist to database.

```
┌──────────────────────────────────────────────────────┐
│              Write-Behind Pattern                    │
│                                                       │
│ WRITE FLOW:                                           │
│                                                       │
│ ┌────────────┐                                       │
│ │    App     │                                       │
│ └──────┬─────┘                                       │
│        │                                              │
│        │ (1) Write data                               │
│        ▼                                              │
│ ┌─────────────┐                                      │
│ │    Cache    │                                      │
│ │   (Redis)   │                                      │
│ └──────┬──────┘                                      │
│        │                                              │
│        │ (2) Return success immediately               │
│        │                                              │
│        │ (3) Background process                       │
│        │     writes to DB (async)                     │
│        ▼                                              │
│ ┌──────────────┐                                     │
│ │   Database   │                                     │
│ └──────────────┘                                     │
│                                                       │
│ Benefits:                                             │
│ - Very fast writes                                    │
│ - Batch database writes                               │
│ - Absorbs write spikes                                │
│                                                       │
│ Risks:                                                │
│ - Data loss if cache crashes before persist           │
│ - Eventual consistency                                │
└──────────────────────────────────────────────────────┘
```

**When to Use:**
- Write-heavy workloads
- Latency critical
- Can tolerate potential data loss
- Examples: Analytics, logs, metrics

### Pattern 4: Cache Invalidation Strategies

**Problem:** "There are only two hard things in Computer Science: cache invalidation and naming things." - Phil Karlton

```
┌──────────────────────────────────────────────────────┐
│          Cache Invalidation Strategies              │
│                                                       │
│ 1. TIME-TO-LIVE (TTL):                               │
│                                                       │
│    SET user:123 value EX 3600  (expire in 1 hour)    │
│                                                       │
│    Pro: Simple, automatic                             │
│    Con: Stale data before expiry                      │
│                                                       │
│ 2. WRITE INVALIDATION:                               │
│                                                       │
│    On write → DELETE cache key                        │
│                                                       │
│    Pro: Always fresh after update                     │
│    Con: Cache miss on next read                       │
│                                                       │
│ 3. EVENT-DRIVEN INVALIDATION:                        │
│                                                       │
│    Service publishes event → Cache listener          │
│    invalidates related keys                           │
│                                                       │
│    Pro: Decoupled, scalable                           │
│    Con: Eventual consistency                          │
│                                                       │
│ 4. CACHE TAGS/GROUPS:                                │
│                                                       │
│    Tag cache entries by entity:                       │
│    user:123 → tags: [user, profile]                  │
│    post:456 → tags: [post, user:123]                 │
│                                                       │
│    Invalidate all tagged entries:                     │
│    INVALIDATE tag:user:123                            │
│                                                       │
│    Pro: Invalidate related data                       │
│    Con: Complex implementation                        │
└──────────────────────────────────────────────────────┘
```

**Implementation (Event-Driven Invalidation):**

```python
import redis
import json
from typing import Set

class CacheInvalidator:
    def __init__(self, redis_client: redis.Redis):
        self.cache = redis_client
        self.pubsub = redis_client.pubsub()
        self.pubsub.subscribe('cache_invalidation')

    def invalidate(self, pattern: str):
        """Invalidate cache keys matching pattern"""
        keys = self.cache.keys(pattern)
        if keys:
            self.cache.delete(*keys)
            print(f"Invalidated {len(keys)} keys: {pattern}")

    def listen(self):
        """Listen for invalidation events"""
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                event = json.loads(message['data'])
                self.handle_event(event)

    def handle_event(self, event: dict):
        event_type = event.get('type')

        if event_type == 'user_updated':
            user_id = event['user_id']
            # Invalidate all user-related caches
            self.invalidate(f'user:{user_id}:*')
            self.invalidate(f'profile:{user_id}')

        elif event_type == 'post_created':
            user_id = event['user_id']
            # Invalidate user's post list
            self.invalidate(f'posts:user:{user_id}')

# Publisher side
def update_user(user_id: str, data: dict):
    # Update database
    db.update_user(user_id, data)

    # Publish invalidation event
    redis_client.publish('cache_invalidation', json.dumps({
        'type': 'user_updated',
        'user_id': user_id
    }))
```

**Cache Stampede Prevention:**

```python
import time
import random

def get_with_lock(key: str, fetch_func, ttl=3600):
    """Prevent cache stampede with locking"""
    cached = cache.get(key)
    if cached:
        return cached

    # Try to acquire lock
    lock_key = f"{key}:lock"
    lock_acquired = cache.setnx(lock_key, "1")
    cache.expire(lock_key, 10)  # Lock expires in 10 sec

    if lock_acquired:
        # This thread fetches data
        value = fetch_func()
        cache.setex(key, ttl, value)
        cache.delete(lock_key)
        return value
    else:
        # Other threads wait briefly and retry
        time.sleep(random.uniform(0.01, 0.1))
        return get_with_lock(key, fetch_func, ttl)
```

---

## Tool Recommendations

### Consensus and Coordination

| Tool | Purpose | Use Case |
|------|---------|----------|
| **etcd** | Distributed key-value store (Raft) | Kubernetes config, service discovery |
| **ZooKeeper** | Coordination service | Kafka cluster management, leader election |
| **Consul** | Service mesh + discovery | Multi-DC service discovery |

### Message Queues and Event Streaming

| Tool | Type | Use Case |
|------|------|----------|
| **Kafka** | Event streaming platform | Event sourcing, log aggregation |
| **RabbitMQ** | Message broker (AMQP) | Task queues, pub/sub |
| **NATS** | Lightweight messaging | Microservices communication |
| **Pulsar** | Multi-tenant event streaming | Cloud-native streaming |
| **Redis Streams** | Lightweight streaming | Simple event streaming |

### Distributed Caching

| Tool | Use Case | Notes |
|------|----------|-------|
| **Redis** | General caching, pub/sub | Fast, versatile |
| **Memcached** | Simple key-value cache | Faster than Redis for simple gets |
| **Hazelcast** | In-memory data grid | Distributed Java caching |

### Distributed Tracing

| Tool | Use Case |
|------|----------|
| **Jaeger** | OpenTelemetry-compatible tracing |
| **Zipkin** | Distributed tracing |
| **Tempo** | Grafana tracing backend |

### Service Mesh

| Tool | Pros | Cons |
|------|------|------|
| **Istio** | Feature-rich, mature | Complex, resource-heavy |
| **Linkerd** | Lightweight, simple | Fewer features |
| **Consul Connect** | HashiCorp ecosystem | Smaller community |

---

## Skill Structure Design

```
designing-distributed-systems/
├── SKILL.md                         # Main skill (700-900 lines)
├── references/
│   ├── cap-pacelc-theorem.md        # CAP and PACELC deep-dive
│   ├── consistency-models.md        # Strong, eventual, causal
│   ├── replication-patterns.md      # Leader-follower, multi-leader, leaderless
│   ├── partitioning-strategies.md   # Hash, range, geographic
│   ├── consensus-algorithms.md      # Raft, Paxos overview
│   ├── resilience-patterns.md       # Circuit breaker, bulkhead, retry
│   ├── saga-pattern.md              # Choreography vs orchestration
│   ├── event-sourcing-cqrs.md       # Event sourcing + CQRS
│   ├── service-discovery.md         # Client-side, server-side, mesh
│   └── caching-strategies.md        # Cache-aside, write-through, etc.
├── examples/
│   ├── consistent-hashing/
│   │   └── consistent_hash.py
│   ├── circuit-breaker/
│   │   └── circuit_breaker.py
│   ├── saga-orchestration/
│   │   └── saga_orchestrator.py
│   ├── event-sourcing/
│   │   └── event_store.py
│   ├── cqrs/
│   │   └── cqrs_example.py
│   └── service-discovery/
│       └── consul_discovery.py
├── diagrams/
│   ├── cap-theorem.txt              # ASCII diagrams
│   ├── replication-topologies.txt
│   ├── saga-flow.txt
│   └── caching-patterns.txt
└── scripts/
    ├── generate-architecture-diagram.py
    └── simulate-network-partition.sh
```

---

## Integration Points

### With Existing Skills

| Skill | Integration |
|-------|-------------|
| `kubernetes-operations` | Service mesh deployment, pod anti-affinity |
| `infrastructure-as-code` | Deploy distributed systems infrastructure |
| `databases-sql` | Replication setup, sharding configuration |
| `databases-nosql` | CAP theorem application, consistency tuning |
| `message-queues` | Event-driven architectures, saga orchestration |
| `observability` | Distributed tracing, monitoring distributed systems |
| `performance-engineering` | Load testing distributed systems |
| `security-hardening` | mTLS, service authentication |

### Skill Chaining Example

```
designing-distributed-systems → kubernetes-operations → observability
        │                              │                      │
        ▼                              ▼                      ▼
  Architecture patterns     Deploy with service mesh   Monitor with tracing
  (CAP, replication)        (Istio, mTLS)              (Jaeger, Prometheus)
```

---

## Implementation Roadmap

### Phase 1: Foundations (Week 1-2)
- [ ] CAP and PACELC theorem
- [ ] Consistency models (strong, eventual, causal)
- [ ] Decision frameworks
- [ ] ASCII diagrams for core concepts

### Phase 2: Replication and Partitioning (Week 3-4)
- [ ] Leader-follower, multi-leader, leaderless
- [ ] Hash partitioning, consistent hashing
- [ ] Range and geographic partitioning
- [ ] Python examples

### Phase 3: Resilience Patterns (Week 5-6)
- [ ] Circuit breaker implementation
- [ ] Bulkhead isolation
- [ ] Timeout and retry strategies
- [ ] Rate limiting and backpressure

### Phase 4: Transaction Patterns (Week 7-8)
- [ ] Saga pattern (choreography + orchestration)
- [ ] Event sourcing
- [ ] CQRS
- [ ] Working examples for each

### Phase 5: Service Communication (Week 9-10)
- [ ] Service discovery patterns
- [ ] Service mesh overview
- [ ] Caching strategies
- [ ] Cache invalidation

### Phase 6: Polish and Integration (Week 11-12)
- [ ] Review all content
- [ ] Create comprehensive examples
- [ ] Integration with other skills
- [ ] Testing and validation

---

## Key Takeaways

1. **CAP Theorem is Fundamental** - Choose 2 of 3, partition tolerance is mandatory
2. **PACELC Adds Nuance** - Consider latency vs consistency trade-offs
3. **Consistency Models Matter** - Strong (banking), eventual (social), causal (chat)
4. **Replication Strategies** - Leader-follower (common), multi-leader (multi-DC), leaderless (high availability)
5. **Resilience is Critical** - Circuit breakers, bulkheads, retries prevent cascading failures
6. **Sagas for Distributed Transactions** - Compensating transactions, not 2PC
7. **Event Sourcing + CQRS** - Audit trails, multiple read models, temporal queries
8. **Service Discovery** - Client-side (flexibility), server-side (simplicity), mesh (observability)
9. **Caching Strategies** - Cache-aside (common), write-through (consistency), write-behind (performance)
10. **Test Failure Scenarios** - Chaos engineering, network partitions, node failures

---

## References and Further Reading

**Books:**
- "Designing Data-Intensive Applications" by Martin Kleppmann (2017) - *The definitive guide*
- "Building Microservices" by Sam Newman (2021, 2nd edition)
- "Release It!" by Michael Nygard (2018, 2nd edition) - *Resilience patterns*

**Papers:**
- "Dynamo: Amazon's Highly Available Key-value Store" (2007)
- "The Google File System" (2003)
- "Spanner: Google's Globally-Distributed Database" (2012)
- "In Search of an Understandable Consensus Algorithm (Raft)" (2014)

**Online Resources:**
- Martin Fowler's blog (martinfowler.com) - Microservices patterns
- AWS Architecture Blog - Distributed systems at scale
- Netflix Tech Blog - Chaos engineering, resilience

---

**Progressive disclosure:** This init.md provides the master plan. Detailed explanations, working code examples, and operational guidance in `references/` and `examples/` directories.

**Target audience:** Software engineers, architects, SRE teams building or operating distributed systems.

**Skill complexity:** High level - requires understanding of networking, databases, and system architecture fundamentals.
