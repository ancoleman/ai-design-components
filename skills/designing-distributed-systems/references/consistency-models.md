# Consistency Models

## Table of Contents

1. [Consistency Spectrum](#consistency-spectrum)
2. [Strong Consistency (Linearizability)](#strong-consistency-linearizability)
3. [Sequential Consistency](#sequential-consistency)
4. [Causal Consistency](#causal-consistency)
5. [Eventual Consistency](#eventual-consistency)
6. [Bounded Staleness](#bounded-staleness)
7. [Choosing Consistency Models](#choosing-consistency-models)

## Consistency Spectrum

```
Strongest ◄─────────────────────────────────────────────► Weakest
   │           │              │              │              │
   │           │              │              │              │
Linearizable Sequential   Causal        Bounded        Eventual
(Strictest)  (Program     (Causally     Staleness     (Converges
             order)       ordered)      (Time-bounded) eventually)

Trade-offs:
Latency:    Highest  →→→→→→→→→→→→→→→→→→→→→→→→→→→→→→  Lowest
Throughput: Lowest   →→→→→→→→→→→→→→→→→→→→→→→→→→→→→→  Highest
Availability: Low    →→→→→→→→→→→→→→→→→→→→→→→→→→→→→→  High
Complexity: Low      →→→→→→→→→→→→→→→→→→→→→→→→→→→→→→  High
```

## Strong Consistency (Linearizability)

### Definition

All operations appear to execute atomically in some sequential order. Once a write completes, all subsequent reads see that value or a newer one.

### Formal Guarantee

If operation A completes before operation B begins, then B must see the effects of A.

### Timeline Example

```
┌──────────────────────────────────────────────────────┐
│         Strong Consistency (Linearizable)           │
├──────────────────────────────────────────────────────┤
│ Time →                                               │
│                                                       │
│ Client A:  Write(x=1) ───┬───► [Complete]           │
│                          │                           │
│                          │ (replication latency)     │
│                          │                           │
│ Client B:                └──────► Read(x) → 1        │
│                                    │                  │
│ Client C:                          └───► Read(x) → 1 │
│                                                       │
│ Guarantee: All reads after write see new value      │
│            No stale reads allowed                    │
└──────────────────────────────────────────────────────┘
```

### Implementation Approaches

**1. Single-Leader with Synchronous Replication:**
```
┌────────────┐
│   Leader   │ ◄── All writes
└─────┬──────┘
      │ (sync replication)
      ├──────────┬──────────┐
      ▼          ▼          ▼
  Follower   Follower   Follower
  (wait ACK) (wait ACK) (wait ACK)
      │          │          │
      └──────────┴──────────┘
              │
        Write confirmed only after
        all replicas ACK
```

**2. Consensus Algorithms (Raft, Paxos):**
- Leader election + log replication
- Majority quorum required
- Examples: etcd, Consul

**3. Two-Phase Commit (2PC):**
- Coordinator + participants
- Prepare phase + commit phase
- Blocking (not recommended for high availability)

### Use Cases

**Financial Transactions:**
```sql
-- Bank transfer: Must be atomic and consistent
BEGIN TRANSACTION;
  UPDATE accounts SET balance = balance - 100 WHERE id = 'A';
  UPDATE accounts SET balance = balance + 100 WHERE id = 'B';
COMMIT;

-- Subsequent read must see both updates
SELECT balance FROM accounts WHERE id IN ('A', 'B');
```

**Inventory Management:**
```
Read stock: 5 items
Client attempts purchase: 2 items
Write new stock: 3 items

All subsequent reads must see 3 (or fewer if another purchase)
Never see stale value of 5
```

**Seat/Ticket Booking:**
- Prevent double-booking
- Once seat sold, all clients see it as unavailable

### Trade-offs

**Benefits:**
- ✅ Simplifies application logic (no conflicts)
- ✅ Immediate consistency guarantees
- ✅ Easy to reason about

**Costs:**
- ❌ Higher latency (coordination overhead)
- ❌ Reduced availability (partition blocks writes)
- ❌ Lower throughput (synchronous operations)

### Technology Examples

| Database      | Strong Consistency Implementation |
|---------------|----------------------------------|
| Spanner       | TrueTime API + Paxos             |
| VoltDB        | In-memory, single-threaded       |
| MongoDB       | Majority write concern (default) |
| etcd          | Raft consensus                   |
| Consul        | Raft consensus                   |
| PostgreSQL    | Synchronous replication          |

## Sequential Consistency

### Definition

Operations from each client appear in the order they were issued, but operations from different clients may be interleaved differently at different nodes.

### Difference from Linearizability

- Linearizability: Global real-time ordering
- Sequential: Per-client ordering, but no global time

### Timeline Example

```
┌──────────────────────────────────────────────────────┐
│            Sequential Consistency                    │
├──────────────────────────────────────────────────────┤
│ Client A:  Write(x=1) → Write(x=2)                  │
│                         (Order preserved)            │
│                                                       │
│ Client B:  Read(x) → May see 0, 1, or 2             │
│            But if sees 2, cannot later see 1         │
│            (Order within client preserved)           │
│                                                       │
│ Node 1 sees: x=1, x=2                                │
│ Node 2 sees: x=1, x=2  (Same order)                 │
│                                                       │
│ Guarantee: Per-client program order preserved        │
│            But no real-time ordering across clients  │
└──────────────────────────────────────────────────────┘
```

### Use Cases

- Distributed caches with invalidation
- Session stores
- Collaborative applications (weaker than causal)

### Implementation

- Lamport clocks
- Vector clocks (partial)
- FIFO queues per client

## Causal Consistency

### Definition

Operations that are causally related are seen by all nodes in the same order. Concurrent operations may be seen in different orders.

### Causality Rules

```
Event A → Event B (A "happens-before" B) if:
1. A and B occur on same process, A before B
2. A is send(message), B is receive(message)
3. Transitivity: A→B and B→C, then A→C

Concurrent events (A || B):
  Neither A→B nor B→A
  Can be observed in any order
```

### Timeline Example

```
┌──────────────────────────────────────────────────────┐
│              Causal Consistency Example              │
├──────────────────────────────────────────────────────┤
│ Alice:  Post message A                               │
│            │                                          │
│            │ (causes - Bob sees A first)             │
│            ▼                                          │
│ Bob:    Reply B (to A)                               │
│            │                                          │
│            │ (causes - Carol sees A and B first)     │
│            ▼                                          │
│ Carol:  Reply C (to B)                               │
│                                                        │
│ Guarantee: All users see messages A → B → C          │
│            (Causally ordered)                         │
│                                                        │
│ Charlie: Post X (concurrent with A, B, C)            │
│                                                        │
│ No Guarantee: X may appear anywhere in timeline      │
│               (Not causally related to A, B, C)      │
│                                                        │
│ Possible orderings for users:                        │
│ - User 1 sees: A, B, X, C                            │
│ - User 2 sees: X, A, B, C                            │
│ - User 3 sees: A, B, C, X                            │
│                                                        │
│ Invalid ordering: B, A, C (violates causality)       │
└──────────────────────────────────────────────────────┘
```

### Use Cases

**Chat Applications:**
```
User A: "What's for dinner?"
User B: "Pizza!" (reply to A)
User C: "Sounds great!" (reply to B)

All users must see:
  "What's for dinner?" → "Pizza!" → "Sounds great!"

Concurrent message: "Meeting at 3pm" may appear anywhere
```

**Collaborative Editing:**
```
User A: Add paragraph at line 10
User B: Edit paragraph at line 10 (depends on A's add)

All editors must see A's add before B's edit
```

**Comment Threads:**
- Replies to comments preserve causality
- Concurrent comments can appear in any order

### Implementation Approaches

**1. Vector Clocks:**
```python
class VectorClock:
    def __init__(self, node_id, nodes):
        self.node_id = node_id
        self.clock = {node: 0 for node in nodes}

    def increment(self):
        self.clock[self.node_id] += 1

    def update(self, other_clock):
        for node, count in other_clock.items():
            self.clock[node] = max(self.clock[node], count)
        self.increment()

    def happens_before(self, other):
        # self → other if self ≤ other and self ≠ other
        return (all(self.clock[n] <= other.clock[n] for n in self.clock)
                and self.clock != other.clock)

    def concurrent(self, other):
        return not (self.happens_before(other) or other.happens_before(self))
```

**2. Lamport Timestamps:**
```python
class LamportClock:
    def __init__(self):
        self.time = 0

    def tick(self):
        self.time += 1
        return self.time

    def update(self, received_time):
        self.time = max(self.time, received_time) + 1
        return self.time
```

**3. Database Support:**
- Azure Cosmos DB: Session consistency level
- Cassandra: WITH CONSISTENCY QUORUM + lightweight transactions

### Trade-offs

**Benefits:**
- ✅ Stronger than eventual, weaker than strong
- ✅ Better performance than strong consistency
- ✅ Intuitive for users (causality preserved)
- ✅ Suitable for collaborative applications

**Costs:**
- ❌ More complex than eventual consistency
- ❌ Requires tracking causality metadata
- ❌ Higher storage overhead (vector clocks)

## Eventual Consistency

### Definition

If no new updates are made, all replicas will eventually converge to the same value. Stale reads are possible.

### Timeline Example

```
┌──────────────────────────────────────────────────────┐
│            Eventual Consistency Timeline             │
├──────────────────────────────────────────────────────┤
│ Time →                                               │
│                                                       │
│ Client A:  Write(x=1) ──► Leader (success)          │
│                │                                      │
│                │ (async replication starts)          │
│                │                                      │
│ Client B:      └──► Read(x) → 0 (STALE!)            │
│                          │                            │
│                          │ (replication continues)   │
│                          │                            │
│ Client B (later):        └──► Read(x) → 1 (fresh)   │
│                                                       │
│ Guarantee: Eventually consistent (seconds to minutes)│
│            Intermediate stale reads possible         │
└──────────────────────────────────────────────────────┘
```

### Conflict Resolution Strategies

**1. Last-Write-Wins (LWW):**
```python
def resolve_lww(value1, timestamp1, value2, timestamp2):
    if timestamp1 > timestamp2:
        return value1
    return value2
```

**2. Application-Specific Merge:**
```python
def merge_shopping_carts(cart1, cart2):
    # Union of items with quantity sum
    merged = {}
    for item_id, qty in cart1.items():
        merged[item_id] = qty
    for item_id, qty in cart2.items():
        merged[item_id] = merged.get(item_id, 0) + qty
    return merged
```

**3. Conflict-Free Replicated Data Types (CRDTs):**
```python
# G-Counter (Grow-only counter)
class GCounter:
    def __init__(self, node_id, nodes):
        self.node_id = node_id
        self.counts = {node: 0 for node in nodes}

    def increment(self):
        self.counts[self.node_id] += 1

    def value(self):
        return sum(self.counts.values())

    def merge(self, other):
        for node, count in other.counts.items():
            self.counts[node] = max(self.counts[node], count)
```

### Use Cases

**Social Media:**
- Likes, follows, unfollows (counts can be approximate)
- Post feeds (slight delay acceptable)
- Profile updates (stale OK briefly)

**Product Catalogs:**
- Prices, descriptions (brief staleness OK)
- Inventory counts (with reservation system)

**DNS:**
- Zone updates propagate eventually
- TTL-based caching

**Analytics:**
- View counts, metrics (approximation acceptable)
- Aggregations (eventual consistency sufficient)

### Implementation Techniques

**1. Asynchronous Replication:**
```
Leader → Log entry → Async send to followers
         ↓
    Return success
    (Don't wait for followers)
```

**2. Anti-Entropy (Gossip Protocol):**
```python
def gossip_protocol(node, peers, interval=10):
    while True:
        # Select random peer
        peer = random.choice(peers)

        # Exchange data
        my_data = node.get_data()
        peer_data = peer.get_data()

        # Merge (reconcile differences)
        node.merge(peer_data)
        peer.merge(my_data)

        time.sleep(interval)
```

**3. Read Repair:**
```python
def read_with_repair(key, replicas, quorum):
    # Read from quorum nodes
    responses = [replica.read(key) for replica in replicas[:quorum]]

    # Find most recent value
    latest = max(responses, key=lambda r: r.timestamp)

    # Repair stale replicas in background
    for replica, response in zip(replicas, responses):
        if response.timestamp < latest.timestamp:
            asyncio.create_task(replica.write(key, latest))

    return latest.value
```

### Trade-offs

**Benefits:**
- ✅ Low latency (no coordination)
- ✅ High availability (accepts writes anytime)
- ✅ Scales better (no synchronous waits)
- ✅ Partition-tolerant

**Costs:**
- ❌ Application must handle stale reads
- ❌ Conflict resolution complexity
- ❌ Hard to reason about (non-deterministic)
- ❌ Testing challenges

## Bounded Staleness

### Definition

Reads may lag behind writes, but staleness is bounded by time or number of versions.

### Timeline Example

```
┌──────────────────────────────────────────────────────┐
│      Bounded Staleness (Bound: 5 seconds)           │
├──────────────────────────────────────────────────────┤
│ Time →                                               │
│                                                       │
│ T=0:   Write(x=1) ──► Leader                         │
│                                                       │
│ T=2:   Read(x) → May return 0 or 1 (within bound)   │
│                                                       │
│ T=4:   Read(x) → May return 0 or 1 (within bound)   │
│                                                       │
│ T=6:   Read(x) → MUST return 1 (bound exceeded)     │
│                                                       │
│ Guarantee: Staleness ≤ 5 seconds                     │
│            OR                                         │
│ Guarantee: Staleness ≤ K versions behind             │
└──────────────────────────────────────────────────────┘
```

### Configuration Examples

**Time-Based Bound:**
```sql
-- Azure Cosmos DB: Bounded Staleness
-- Max lag: 10 seconds OR 1000 operations
CREATE COLLECTION my_collection
WITH CONSISTENCY_LEVEL = 'BoundedStaleness',
     MAX_STALENESS_PREFIX = 1000,
     MAX_STALENESS_INTERVAL = 10;
```

**Version-Based Bound:**
```python
def read_with_bound(key, max_versions_behind):
    # Read with staleness bound
    current_version = leader.get_version(key)
    replica_value, replica_version = replica.read(key)

    # If too stale, read from leader
    if current_version - replica_version > max_versions_behind:
        return leader.read(key)

    return replica_value
```

### Use Cases

**Real-Time Dashboards:**
- Metrics with acceptable lag (e.g., 10 seconds)
- SLA: "Dashboard data max 30 seconds old"

**Inventory with Buffer:**
- Stock count can be slightly stale
- Buffer ensures no overselling

**Leaderboards:**
- Slight delay acceptable (eventual rankings)
- Bound: "Rank updates within 1 minute"

### Trade-offs

**Benefits:**
- ✅ Middle ground: consistency + performance
- ✅ Predictable staleness window
- ✅ Suitable for real-time systems with tolerance

**Costs:**
- ❌ More complex than eventual
- ❌ Requires monitoring lag
- ❌ Must handle bound violations

## Choosing Consistency Models

### Decision Framework

```
START: Choose consistency model
  │
  ├─► Money involved? → Strong Consistency
  │
  ├─► Double-booking unacceptable? → Strong Consistency
  │
  ├─► Causality important (chat, edits)? → Causal Consistency
  │
  ├─► Stale reads tolerable with time bound? → Bounded Staleness
  │
  ├─► Read-heavy, stale tolerable? → Eventual Consistency
  │
  └─► Default? → Eventual (then strengthen if needed)
```

### Use Case Matrix

| Use Case                   | Consistency Model       | Rationale                        |
|----------------------------|------------------------|----------------------------------|
| Bank account balance       | Strong (Linearizable)  | Money correctness critical       |
| Seat booking (airline)     | Strong (Linearizable)  | No double-booking allowed        |
| Inventory stock count      | Strong or Bounded      | Prevent overselling, buffer OK   |
| Shopping cart              | Eventual               | Can merge carts, availability↑   |
| Product catalog            | Eventual               | Stale prices OK briefly          |
| Collaborative editing      | Causal                 | Preserve edit order              |
| Chat messages              | Causal                 | Preserve reply causality         |
| Social media likes         | Eventual               | Approximation acceptable         |
| DNS records                | Eventual               | Propagation delay expected       |
| Real-time dashboard        | Bounded Staleness      | Lag acceptable within SLA        |

### Implementation Checklist

**For Strong Consistency:**
- [ ] Use synchronous replication or consensus (Raft, Paxos)
- [ ] Accept higher latency for correctness
- [ ] Plan for reduced availability during partitions
- [ ] Consider PostgreSQL sync replication, etcd, Spanner

**For Eventual Consistency:**
- [ ] Implement conflict resolution strategy (LWW, merge, CRDTs)
- [ ] Design for idempotency (safe retries)
- [ ] Monitor convergence time
- [ ] Consider Cassandra, DynamoDB, Riak

**For Causal Consistency:**
- [ ] Implement vector clocks or Lamport timestamps
- [ ] Track causality metadata
- [ ] Test causality violations
- [ ] Consider Azure Cosmos DB (Session consistency)

**For Bounded Staleness:**
- [ ] Define acceptable staleness window
- [ ] Monitor replication lag
- [ ] Alert on bound violations
- [ ] Consider Azure Cosmos DB (Bounded Staleness level)
