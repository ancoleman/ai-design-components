# Replication Patterns

## Table of Contents

1. [Leader-Follower Replication](#leader-follower-replication)
2. [Multi-Leader Replication](#multi-leader-replication)
3. [Leaderless Replication](#leaderless-replication)
4. [Synchronous vs Asynchronous Replication](#synchronous-vs-asynchronous-replication)
5. [Failover Strategies](#failover-strategies)

## Leader-Follower Replication

### Architecture

```
┌──────────────────────────────────────────────────────┐
│          Leader-Follower (Single-Leader)             │
│                                                       │
│ Client Writes                                         │
│     │                                                 │
│     ▼                                                 │
│ ┌────────────┐                                       │
│ │   Leader   │ (1) Accept write                      │
│ │            │ (2) Write to WAL (Write-Ahead Log)    │
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

### PostgreSQL Example

```sql
-- On Leader (Primary)
-- Configure for replication
ALTER SYSTEM SET wal_level = replica;
ALTER SYSTEM SET max_wal_senders = 3;
ALTER SYSTEM SET wal_keep_size = '1GB';

-- Create replication slot
SELECT pg_create_physical_replication_slot('replica1');

-- Create publication (for logical replication)
CREATE PUBLICATION my_publication FOR ALL TABLES;

-- On Follower (Replica)
-- Create replica from backup
pg_basebackup -h leader-host -D /var/lib/postgresql/data -U replicator -P -v

-- Configure recovery (standby.signal)
primary_conninfo = 'host=leader-host port=5432 user=replicator'
primary_slot_name = 'replica1'

-- Start replica
pg_ctl start
```

### Use Cases

- Most common replication pattern
- Read scaling (distribute reads across followers)
- Geographic read replicas (low latency reads)
- Backup/DR (follower in different datacenter)

### Benefits & Trade-offs

**Benefits:**
- ✅ Simple to understand and implement
- ✅ Strong consistency (with synchronous replication)
- ✅ Read scaling (multiple followers)
- ✅ No write conflicts

**Trade-offs:**
- ❌ Write bottleneck (single leader)
- ❌ Follower lag (with async replication)
- ❌ Failover complexity

## Multi-Leader Replication

### Architecture

```
┌──────────────────────────────────────────────────────┐
│          Multi-Leader Replication                    │
│                                                       │
│    US-EAST Datacenter         EU-WEST Datacenter     │
│    ┌──────────────┐           ┌──────────────┐      │
│    │   Leader 1   │◄─────────►│   Leader 2   │      │
│    │              │  Replicate │              │      │
│    │              │  (async)   │              │      │
│    └──────┬───────┘           └──────┬───────┘      │
│           │                           │              │
│      ┌────┴────┐                 ┌────┴────┐        │
│      ▼         ▼                 ▼         ▼        │
│  Follower  Follower          Follower  Follower     │
│                                                       │
│ Client (US) → Leader 1 (low latency writes)          │
│ Client (EU) → Leader 2 (low latency writes)          │
│                                                       │
│ CONFLICT SCENARIO:                                    │
│ T=0: Client A → Leader 1 → Write(x=1)                │
│ T=0: Client B → Leader 2 → Write(x=2)                │
│ T=1: Leaders replicate... CONFLICT!                  │
└──────────────────────────────────────────────────────┘
```

### Conflict Resolution Strategies

**1. Last-Write-Wins (LWW) with Timestamps:**
```python
import time

def resolve_lww(write1, write2):
    """Resolve conflict using timestamp"""
    if write1['timestamp'] > write2['timestamp']:
        return write1
    elif write2['timestamp'] > write1['timestamp']:
        return write2
    else:
        # Tie-breaker: use node ID
        return write1 if write1['node_id'] > write2['node_id'] else write2

# Example
write_us = {'value': 1, 'timestamp': 1701000001, 'node_id': 'us-east'}
write_eu = {'value': 2, 'timestamp': 1701000002, 'node_id': 'eu-west'}
winner = resolve_lww(write_us, write_eu)  # write_eu wins (newer timestamp)
```

**2. Application-Specific Merge:**
```python
def merge_shopping_carts(cart1, cart2):
    """Merge shopping carts by union + sum quantities"""
    merged = {}
    for item_id, qty in cart1.items():
        merged[item_id] = qty
    for item_id, qty in cart2.items():
        merged[item_id] = merged.get(item_id, 0) + qty
    return merged

# Example
cart_us = {'item1': 2, 'item2': 1}
cart_eu = {'item2': 1, 'item3': 3}
result = merge_shopping_carts(cart_us, cart_eu)
# {'item1': 2, 'item2': 2, 'item3': 3}
```

**3. Vector Clocks:**
```python
class VectorClock:
    def __init__(self, node_id, nodes):
        self.node_id = node_id
        self.clock = {node: 0 for node in nodes}

    def increment(self):
        self.clock[self.node_id] += 1

    def merge(self, other_clock):
        for node, count in other_clock.items():
            self.clock[node] = max(self.clock[node], count)
        self.increment()

    def happens_before(self, other):
        return (all(self.clock[n] <= other.clock[n] for n in self.clock)
                and self.clock != other.clock)

    def concurrent(self, other):
        return not (self.happens_before(other) or other.happens_before(self))

# Usage
vc1 = VectorClock('us', ['us', 'eu'])
vc1.increment()  # {us:1, eu:0}

vc2 = VectorClock('eu', ['us', 'eu'])
vc2.increment()  # {us:0, eu:1}

if vc1.concurrent(vc2):
    print("Conflict detected - concurrent writes!")
```

### CouchDB Example

```javascript
// CouchDB handles conflicts automatically
// Create document on leader 1
db.put({
  _id: 'user123',
  name: 'Alice',
  email: 'alice@example.com'
});

// Update on leader 2 (conflict scenario)
db.put({
  _id: 'user123',
  _rev: '1-abc',  // Same revision
  name: 'Alicia',  // Different value
  email: 'alicia@example.com'
});

// CouchDB stores both versions as siblings
db.get('user123', {conflicts: true})
  .then(doc => {
    console.log(doc);
    // {
    //   _id: 'user123',
    //   _rev: '2-xyz',
    //   name: 'Alice',
    //   _conflicts: ['2-def']  // Sibling revision
    // }

    // Resolve manually
    db.remove(doc._id, '2-def');  // Delete losing revision
  });
```

### Use Cases

- Multi-datacenter deployments (each datacenter has a leader)
- Low write latency critical (users write to local leader)
- Offline-first applications (local leader syncs when online)

### Benefits & Trade-offs

**Benefits:**
- ✅ Low write latency (write to nearest leader)
- ✅ No single point of failure
- ✅ Datacenter-level redundancy

**Trade-offs:**
- ❌ Conflict resolution complexity
- ❌ Application must handle conflicts
- ❌ Harder to reason about consistency

## Leaderless Replication

### Architecture (Dynamo-style)

```
┌──────────────────────────────────────────────────────┐
│      Leaderless Replication (N=5, W=3, R=2)          │
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
│ Client ─┬──► Node 1 (v=5, ts=T5)                     │
│         ├──► Node 2 (v=5, ts=T5)                     │
│         └──► Node 3 (v=4, ts=T3) [stale]             │
│              │                                         │
│              └─ R=2 quorum satisfied                  │
│                 Return v=5 (most recent)              │
│                 Repair Node 3 in background           │
│                                                       │
│ Consistency Rule: W + R > N                           │
│   W=3, R=2, N=5 → 3+2=5 > 5 ✓ (overlap guaranteed)  │
└──────────────────────────────────────────────────────┘
```

### Quorum Configurations

| Configuration | W | R | N | Consistency | Use Case           |
|--------------|---|---|---|-------------|--------------------|
| Strong       | 3 | 3 | 5 | Strong      | Banking, inventory |
| Balanced     | 3 | 2 | 5 | Strong      | Default            |
| Write-heavy  | 2 | 3 | 5 | Strong      | Logging            |
| Read-heavy   | 3 | 1 | 5 | Eventual    | Caching            |
| Max Avail    | 1 | 1 | 5 | Eventual    | Analytics          |

### Cassandra Example

```sql
-- Create keyspace with replication factor
CREATE KEYSPACE my_app WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'datacenter1': 3,
  'datacenter2': 2
};

-- Write with QUORUM (W=2 for RF=3)
INSERT INTO users (id, name, email)
VALUES (uuid(), 'Alice', 'alice@example.com')
USING CONSISTENCY QUORUM;

-- Read with QUORUM (R=2 for RF=3)
SELECT * FROM users WHERE id = ?
USING CONSISTENCY QUORUM;

-- Tunable consistency per query
-- ONE: Eventual consistency (fast)
SELECT * FROM users WHERE id = ?
USING CONSISTENCY ONE;

-- ALL: Strong consistency (slow)
SELECT * FROM users WHERE id = ?
USING CONSISTENCY ALL;
```

### Read Repair and Anti-Entropy

**Read Repair:**
```python
def read_with_repair(key, nodes, r_quorum):
    # Read from R nodes
    responses = []
    for node in nodes[:r_quorum]:
        response = node.read(key)
        responses.append((node, response))

    # Find most recent value
    latest = max(responses, key=lambda x: x[1].timestamp)

    # Repair stale nodes in background
    for node, response in responses:
        if response.timestamp < latest[1].timestamp:
            async_repair(node, key, latest[1])

    return latest[1].value

def async_repair(node, key, latest_value):
    # Background task to repair stale node
    node.write(key, latest_value)
```

**Anti-Entropy (Merkle Trees):**
```python
import hashlib

class MerkleTree:
    def __init__(self, data):
        self.data = data
        self.tree = self._build_tree(data)

    def _build_tree(self, data):
        # Build Merkle tree from data
        if not data:
            return None
        if len(data) == 1:
            return hashlib.sha256(str(data[0]).encode()).hexdigest()

        mid = len(data) // 2
        left = self._build_tree(data[:mid])
        right = self._build_tree(data[mid:])

        combined = f"{left}{right}"
        return hashlib.sha256(combined.encode()).hexdigest()

    def compare(self, other):
        # Compare root hashes
        return self.tree == other.tree

# Nodes periodically exchange Merkle trees
# If root hashes differ, recursively compare subtrees
# Synchronize only divergent data
```

### Use Cases

- Maximum availability required
- Multi-datacenter with tunable consistency
- Shopping carts, session stores
- Time-series data with eventual consistency

### Benefits & Trade-offs

**Benefits:**
- ✅ No single point of failure
- ✅ Tunable consistency (per query)
- ✅ High availability
- ✅ Symmetric (all nodes equal)

**Trade-offs:**
- ❌ Complexity (quorum math)
- ❌ Read repair overhead
- ❌ Anti-entropy background work
- ❌ Conflict resolution needed

## Synchronous vs Asynchronous Replication

### Synchronous Replication

```
Client → Leader → Wait for follower ACK → Success
                  (blocks until replicated)

Timeline:
T=0: Write arrives at leader
T=1: Leader writes to WAL
T=2: Leader sends to followers
T=3: Followers write to WAL
T=4: Followers send ACK
T=5: Leader confirms to client
     (Total latency: 5 time units)
```

**Benefits:**
- ✅ Strong consistency (guaranteed)
- ✅ No data loss on leader failure

**Trade-offs:**
- ❌ Higher latency
- ❌ Reduced availability (follower failure blocks writes)

**Use Cases:**
- Financial transactions
- Inventory management
- Booking systems

### Asynchronous Replication

```
Client → Leader → Success (replicate in background)
                  (returns immediately)

Timeline:
T=0: Write arrives at leader
T=1: Leader writes to WAL
T=2: Leader confirms to client
     (Total latency: 2 time units)
T=3: Leader sends to followers (async)
T=4: Followers write to WAL
     (Replication lag: 2 time units)
```

**Benefits:**
- ✅ Low latency
- ✅ High availability (follower failure doesn't block)

**Trade-offs:**
- ❌ Eventual consistency (replication lag)
- ❌ Possible data loss (if leader fails before replication)

**Use Cases:**
- Social media
- Content management
- Caching

### Semi-Synchronous Replication

```
PostgreSQL: Wait for at least one follower ACK

ALTER SYSTEM SET synchronous_commit = on;
ALTER SYSTEM SET synchronous_standby_names = 'FIRST 1 (replica1, replica2)';

Behavior:
- Wait for 1 out of 2 followers
- If replica1 fails, use replica2
- Balance: consistency + availability
```

## Failover Strategies

### Automatic Failover Process

```
┌──────────────────────────────────────────────────────┐
│              Automatic Failover                      │
├──────────────────────────────────────────────────────┤
│ 1. Detect Leader Failure                             │
│    - Health checks (heartbeats)                      │
│    - Timeout threshold (e.g., 30 seconds)            │
│                                                       │
│ 2. Elect New Leader                                  │
│    - Follower with longest replication log           │
│    - OR follower with lowest replica lag             │
│    - OR manual promotion                             │
│                                                       │
│ 3. Reconfigure Followers                             │
│    - Point to new leader                             │
│    - Resume replication                              │
│                                                       │
│ 4. Update Clients                                    │
│    - DNS update (new leader IP)                      │
│    - Service discovery update                        │
│    - Connection string update                        │
│                                                       │
│ 5. Handle Old Leader                                 │
│    - Prevent dual writes (split-brain)               │
│    - Use fencing tokens                              │
│    - Demote to follower when recovered               │
└──────────────────────────────────────────────────────┘
```

### Split-Brain Prevention

```python
# Fencing tokens prevent dual writes
class LeaderWithFencing:
    def __init__(self):
        self.fencing_token = 0
        self.is_leader = False

    def promote_to_leader(self, new_token):
        if new_token > self.fencing_token:
            self.fencing_token = new_token
            self.is_leader = True
            return True
        return False

    def write(self, key, value):
        if not self.is_leader:
            raise Exception("Not leader")

        # Include fencing token with write
        storage.write_with_token(key, value, self.fencing_token)

# Storage rejects writes with old tokens
class FencedStorage:
    def __init__(self):
        self.max_token = 0

    def write_with_token(self, key, value, token):
        if token < self.max_token:
            raise Exception("Fencing token too old - rejected")

        self.max_token = token
        self.data[key] = value
```

### Best Practices

**Health Checks:**
- Use multiple checks (TCP, HTTP, application-level)
- Avoid false positives (network glitches)
- Exponential backoff for retries

**Failover Time:**
- Typical: 30-60 seconds for automatic failover
- Manual failover: 5-15 minutes (verification steps)
- Test failover regularly (chaos engineering)

**Data Loss Prevention:**
- Use synchronous replication for critical data
- Implement write-ahead logging (WAL)
- Regular backups independent of replication
