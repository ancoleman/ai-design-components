# CAP and PACELC Theorem

## Table of Contents

1. [CAP Theorem Deep-Dive](#cap-theorem-deep-dive)
2. [PACELC Extension](#pacelc-extension)
3. [PACELC Matrix](#pacelc-matrix)
4. [Real-World System Classification](#real-world-system-classification)
5. [Decision Framework](#decision-framework)

## CAP Theorem Deep-Dive

### Definition

In a distributed system experiencing a network partition, choose between:
- **Consistency (C):** All nodes see the same data at the same time
- **Availability (A):** Every request receives a response (success or failure)
- **Partition Tolerance (P):** System continues operating despite network failures

**Critical Insight:** Partition tolerance is mandatory in distributed systems. Network failures WILL occur. The choice is between C or A during partitions.

### CAP Decision Tree

```
START: Designing distributed system
  │
  ├─► Will network partitions occur?
  │   Answer: YES (always in distributed systems)
  │
  ├─► DURING PARTITION, choose:
  │   │
  │   ├─► CP (Consistency + Partition Tolerance)
  │   │   │
  │   │   ├─ Behavior: Reject writes, return errors
  │   │   ├─ Use when: Correctness > availability
  │   │   ├─ Examples:
  │   │   │   - Banking (account balance must be correct)
  │   │   │   - Inventory (prevent overselling)
  │   │   │   - Seat booking (no double-booking)
  │   │   │   - Distributed locks
  │   │   │
  │   │   ├─ Systems: HBase, MongoDB (default), etcd, Consul
  │   │   └─ Trade-off: System unavailable during partition
  │   │
  │   └─► AP (Availability + Partition Tolerance)
  │       │
  │       ├─ Behavior: Accept writes, resolve conflicts later
  │       ├─ Use when: Availability > strict consistency
  │       ├─ Examples:
  │       │   - Social media (likes, follows, posts)
  │       │   - Shopping cart (can merge carts)
  │       │   - Product catalog (stale prices OK briefly)
  │       │   - Analytics (approximate counts acceptable)
  │       │
  │       ├─ Systems: Cassandra, DynamoDB, Riak, Couchbase
  │       └─ Trade-off: Stale reads, conflict resolution needed
```

### CP Systems: Consistency + Partition Tolerance

**Behavior During Partition:**
```
┌─────────────────────────────────────────────────────┐
│              CP System During Partition             │
├─────────────────────────────────────────────────────┤
│ Datacenter A          │     Network Partition       │
│   ┌─────────┐        │                             │
│   │ Leader  │        │         Datacenter B        │
│   │         │        │           ┌─────────┐       │
│   │ Can     │        │           │Follower │       │
│   │ serve   │        │           │         │       │
│   │ writes  │        │   ╳╳╳╳╳   │ Cannot  │       │
│   │ (quorum)│◄───────┼───╳╳╳╳╳───│ reach   │       │
│   └─────────┘        │   ╳╳╳╳╥   │ quorum  │       │
│      ▲               │          │         │       │
│      │               │          │ REJECTS │       │
│   Succeeds           │          │ WRITES  │       │
│                      │          └─────────┘       │
│                      │             ▲               │
│                      │             │               │
│                      │          Returns            │
│                      │          Error              │
└─────────────────────────────────────────────────────┘

Result: Only partition with quorum accepts writes
        Other partition rejects writes (unavailable)
```

**Examples:**
- MongoDB (default): Requires majority for writes during partition
- etcd: Raft consensus requires quorum (N/2 + 1)
- HBase: Region servers must reach ZooKeeper quorum

### AP Systems: Availability + Partition Tolerance

**Behavior During Partition:**
```
┌─────────────────────────────────────────────────────┐
│              AP System During Partition             │
├─────────────────────────────────────────────────────┤
│ Datacenter A          │     Network Partition       │
│   ┌─────────┐        │                             │
│   │ Node 1  │        │         Datacenter B        │
│   │         │        │           ┌─────────┐       │
│   │ Accepts │        │           │ Node 2  │       │
│   │ write   │        │           │         │       │
│   │ x=1     │        │   ╥╥╥╥╥   │ Accepts │       │
│   │         │        │   ╥╥╥╥╥   │ write   │       │
│   └─────────┘        │   ╥╥╥╥╥   │ x=2     │       │
│      ▲               │          └─────────┘       │
│      │               │             ▲               │
│   Client A           │          Client B           │
│   (succeeds)         │          (succeeds)         │
│                      │                              │
│ When partition heals:                              │
│   Conflict: x=1 vs x=2                             │
│   Resolution: Last-Write-Wins, vector clocks, etc. │
└─────────────────────────────────────────────────────┘

Result: Both partitions accept writes
        Conflicts resolved after partition heals
```

**Examples:**
- Cassandra: Tunable consistency (can choose AP with QUORUM ONE)
- DynamoDB: Eventual consistency by default
- Riak: Last-Write-Wins or sibling resolution

## PACELC Extension

### Why PACELC?

CAP only describes behavior during partitions. What about normal operations (99%+ of the time)?

**PACELC:** If Partition, choose A or C; Else (normal), choose Latency or Consistency

### PACELC Components

```
P-A-C-E-L-C
│ │ │ │ │ │
│ │ │ │ │ └─ Consistency (normal operation)
│ │ │ │ └─── Latency (normal operation)
│ │ │ └───── Else (no partition)
│ │ └─────── Consistency (during partition)
│ └───────── Availability (during partition)
└─────────── Partition occurs
```

### PACELC Decision Matrix

```
┌─────────────────────────────────────────────────────┐
│               PACELC Trade-offs                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│ IF PARTITION OCCURS:                                │
│   PA: Choose Availability (stale reads OK)          │
│   PC: Choose Consistency (reject some requests)     │
│                                                      │
│ ELSE (Normal Operation):                            │
│   EL: Choose Latency (async replication, fast)     │
│   EC: Choose Consistency (sync replication, slow)   │
│                                                      │
│ Common Combinations:                                 │
│   PA/EL: High availability, eventual consistency    │
│   PC/EC: Strong consistency, reduced availability   │
│   PC/EL: Hybrid (consistent during partition,       │
│          optimized for latency normally)            │
└─────────────────────────────────────────────────────┘
```

## PACELC Matrix

### Database Classification

| System       | P: A or C? | E: L or C? | Notes                           |
|--------------|------------|------------|---------------------------------|
| **Spanner**  | PC         | EC         | Global strong consistency       |
| **DynamoDB** | PA         | EL         | Eventual consistency by default |
| **Cassandra**| PA         | EL         | Tunable (can choose PC/EC)      |
| **MongoDB**  | PC         | EC         | Default: strong consistency     |
| **Cosmos DB**| PA/PC      | EL/EC      | 5 consistency levels            |
| **VoltDB**   | PC         | EC         | In-memory, strong consistency   |
| **Riak**     | PA         | EL         | Eventual consistency            |
| **etcd**     | PC         | EC         | Raft consensus                  |
| **Redis**    | PC         | EC         | Cluster mode with sync rep      |

### Detailed System Behaviors

**PA/EL Systems (DynamoDB, Cassandra):**
```
During Partition:
  - Accept writes in both partitions (A)
  - Conflicts resolved later

Normal Operation:
  - Async replication (L)
  - Low latency writes
  - Eventual consistency
```

**PC/EC Systems (MongoDB, etcd):**
```
During Partition:
  - Only majority partition accepts writes (C)
  - Minority partition rejects writes

Normal Operation:
  - Synchronous replication (C)
  - Higher latency (wait for replicas)
  - Strong consistency
```

**Tunable Systems (Cosmos DB):**
```
Cosmos DB offers 5 consistency levels:
  1. Strong (PC/EC)
  2. Bounded Staleness (PC/EC with lag bound)
  3. Session (PA/EL with session consistency)
  4. Consistent Prefix (PA/EL with ordered reads)
  5. Eventual (PA/EL)
```

## Real-World System Classification

### Banking System (PC/EC)

```
Requirements:
  - Account balance must be correct
  - No overdrafts allowed
  - Transactions must be atomic

Design:
  ├─ During Partition: Choose Consistency (PC)
  │  Reject writes if quorum unavailable
  │
  └─ Normal Operation: Choose Consistency (EC)
     Synchronous replication to all replicas
     Higher latency acceptable for correctness

Technology: Spanner, VoltDB, PostgreSQL (sync replication)
```

### Social Media Feed (PA/EL)

```
Requirements:
  - Users can always post
  - Slight delay in seeing posts OK
  - Likes/follows can be approximate

Design:
  ├─ During Partition: Choose Availability (PA)
  │  Accept posts in all datacenters
  │  Resolve conflicts later (merge likes)
  │
  └─ Normal Operation: Choose Latency (EL)
     Async replication for low latency
     Eventual consistency acceptable

Technology: Cassandra, DynamoDB, Couchbase
```

### E-Commerce (Hybrid: PC for inventory, PA for catalog)

```
Inventory:
  ├─ PC/EC: Strong consistency for stock count
  └─ Prevent overselling

Product Catalog:
  ├─ PA/EL: Eventual consistency for descriptions, prices
  └─ Stale data acceptable briefly

Shopping Cart:
  ├─ PA/EL: Eventually consistent, can merge carts
  └─ High availability critical
```

## Decision Framework

### Step 1: Identify Requirements

Ask:
1. Is data correctness critical? (banking, inventory)
2. Is availability more important than consistency? (social media)
3. Are users globally distributed? (latency matters)
4. Can the system tolerate stale reads? (analytics)

### Step 2: Choose CAP Profile

```
Correctness Critical:
  └─► CP (Consistency + Partition Tolerance)
      Examples: Banking, inventory, booking

Availability Critical:
  └─► AP (Availability + Partition Tolerance)
      Examples: Social media, analytics, catalog

Hybrid (Different Per Feature):
  └─► CP for critical data, AP for non-critical
      Examples: E-commerce, SaaS platforms
```

### Step 3: Choose PACELC Profile

```
Low Latency Critical:
  └─► PA/EL (Eventual consistency, async replication)
      Examples: Social media, caching, analytics

Strong Consistency Critical:
  └─► PC/EC (Strong consistency, sync replication)
      Examples: Banking, financial systems

Middle Ground:
  └─► PC/EL (Consistent during partition, optimized latency normally)
      Examples: Session stores, collaborative editing
```

### Step 4: Select Technology

```
PA/EL Systems:
  - Cassandra (wide-column, tunable)
  - DynamoDB (key-value, managed)
  - Riak (key-value, open-source)

PC/EC Systems:
  - MongoDB (document, strong by default)
  - etcd (key-value, Raft consensus)
  - Spanner (SQL, global consistency)

Tunable Systems:
  - Cosmos DB (multi-model, 5 levels)
  - Cassandra (tunable quorum)
  - PostgreSQL (async, sync, quorum replication)
```

### Example Decision Path

**Use Case: Multi-Region Order System**

```
Step 1: Requirements
  - Orders must be processed (availability)
  - Payment must be correct (consistency)
  - Users globally distributed (latency)

Step 2: Hybrid Approach
  ├─ Order placement: PA/EL (accept orders anywhere)
  ├─ Payment processing: PC/EC (strong consistency)
  └─ Order history: PA/EL (eventual consistency)

Step 3: Technology Choices
  ├─ Order service: DynamoDB (PA/EL)
  ├─ Payment service: PostgreSQL with sync replication (PC/EC)
  └─ Read model (CQRS): Elasticsearch (PA/EL)

Step 4: Conflict Resolution
  ├─ Orders: Timestamps + vector clocks
  ├─ Payments: Saga pattern with compensation
  └─ Idempotency: Unique request IDs
```

## Best Practices

**Start with PACELC, not just CAP:**
- CAP only covers partition scenarios
- PACELC covers both partition and normal operation
- Most systems operate normally 99%+ of the time

**Don't Assume CA is Achievable:**
- CA (Consistency + Availability without Partition Tolerance) is impossible in distributed systems
- Network partitions WILL occur

**Use Tunable Consistency:**
- Cassandra: Per-query consistency (ONE, QUORUM, ALL)
- Cosmos DB: 5 consistency levels
- Choose based on operation criticality

**Test Partition Scenarios:**
- Use chaos engineering (e.g., Chaos Monkey)
- Simulate network partitions in testing
- Verify behavior matches expectations (CP or AP)

**Monitor Trade-offs:**
- Track replication lag (PA/EL systems)
- Monitor quorum health (PC systems)
- Alert on inconsistency windows exceeding SLA
