# Consensus Algorithms

## Table of Contents

1. [What is Consensus](#what-is-consensus)
2. [Raft Algorithm](#raft-algorithm)
3. [Paxos Algorithm](#paxos-algorithm)
4. [When to Use Consensus](#when-to-use-consensus)
5. [Consensus vs Replication](#consensus-vs-replication)

## What is Consensus

### Definition

Consensus is the problem of getting multiple nodes to agree on a single value, even in the presence of failures.

### Requirements (FLP Impossibility)

Consensus algorithm must guarantee:
1. **Agreement:** All correct nodes decide on the same value
2. **Validity:** Decided value was proposed by some node
3. **Termination:** All correct nodes eventually decide

**FLP Impossibility:** Cannot guarantee all three in an asynchronous system with even one failure. Practical algorithms trade termination for safety.

### Use Cases

- Leader election: Elect exactly one leader
- Distributed locks: Only one node acquires lock
- Configuration management: All nodes agree on config
- Atomic commit: All nodes commit or all abort

## Raft Algorithm

### Overview

Raft is a consensus algorithm designed for understandability. It's equivalent to Paxos in fault-tolerance and performance.

### Raft Components

```
┌──────────────────────────────────────────────────────┐
│                  Raft Roles                          │
├──────────────────────────────────────────────────────┤
│ LEADER:                                               │
│   - Handles all client requests                      │
│   - Replicates log to followers                      │
│   - Only one leader per term                         │
│                                                       │
│ FOLLOWER:                                             │
│   - Passive: responds to leader/candidate requests   │
│   - Becomes candidate if no heartbeat               │
│                                                       │
│ CANDIDATE:                                            │
│   - Requests votes from other nodes                  │
│   - Becomes leader if wins majority                  │
└──────────────────────────────────────────────────────┘
```

### Raft Leader Election

```
┌──────────────────────────────────────────────────────┐
│              Raft Leader Election                    │
├──────────────────────────────────────────────────────┤
│ 1. Initial State: All nodes are followers           │
│    Election timeout: 150-300ms (randomized)          │
│                                                       │
│ 2. Follower times out (no heartbeat from leader)    │
│    → Becomes CANDIDATE                               │
│    → Increments term number                          │
│    → Votes for itself                                │
│    → Sends RequestVote RPCs to all nodes             │
│                                                       │
│ 3. Other nodes respond:                              │
│    ├─ Grant vote if:                                 │
│    │  - Haven't voted this term                      │
│    │  - Candidate's log is up-to-date                │
│    │                                                  │
│    └─ Deny vote otherwise                            │
│                                                       │
│ 4. Outcomes:                                          │
│    ├─ Wins election (majority votes)                 │
│    │  → Becomes LEADER                               │
│    │  → Sends heartbeats to all nodes                │
│    │                                                  │
│    ├─ Another node wins election                     │
│    │  → Receives heartbeat from new leader           │
│    │  → Becomes FOLLOWER                             │
│    │                                                  │
│    └─ Split vote (no majority)                       │
│       → Times out                                    │
│       → Starts new election (higher term)            │
└──────────────────────────────────────────────────────┘
```

### Raft Log Replication

```
┌──────────────────────────────────────────────────────┐
│              Raft Log Replication                    │
├──────────────────────────────────────────────────────┤
│ Leader:  [1][2][3][4][5]                             │
│           │  │  │  │  │                              │
│           └──┼──┼──┼──┼──► AppendEntries RPC        │
│              │  │  │  │                              │
│ Follower 1: [1][2][3][4][5]  (up-to-date)           │
│                                                       │
│ Follower 2: [1][2][3][ ][ ]  (lagging)               │
│              └──────────────► Receives entries 4,5   │
│                                                       │
│ Follower 3: [1][2][X][4][ ]  (conflict at 3)         │
│              └──────────────► Deletes 3, gets 3,4,5  │
│                                                       │
│ Commit:                                               │
│   Leader commits entry when replicated to majority   │
│   Leader notifies followers of commit index          │
│   Followers apply committed entries to state machine │
└──────────────────────────────────────────────────────┘
```

### Raft Safety Properties

**Election Safety:** At most one leader per term
**Leader Append-Only:** Leader never deletes/overwrites entries
**Log Matching:** If two logs contain same entry at same index, all preceding entries are identical
**Leader Completeness:** If entry committed in term T, present in all leaders of future terms
**State Machine Safety:** If node applies entry at index i, no other node applies different entry at i

### Example: etcd

```bash
# Start etcd cluster (3 nodes for fault tolerance)
etcd --name node1 --initial-cluster node1=http://10.0.1.1:2380,node2=http://10.0.1.2:2380,node3=http://10.0.1.3:2380
etcd --name node2 --initial-cluster node1=http://10.0.1.1:2380,node2=http://10.0.1.2:2380,node3=http://10.0.1.3:2380
etcd --name node3 --initial-cluster node1=http://10.0.1.1:2380,node2=http://10.0.1.2:2380,node3=http://10.0.1.3:2380

# Write key-value (goes to leader, replicated via Raft)
etcdctl put mykey "myvalue"

# Read key (can read from any node)
etcdctl get mykey

# Check cluster status
etcdctl endpoint status --cluster

# Simulate leader failure (kill leader process)
# Raft elects new leader automatically (election timeout ~300ms)
# Writes continue with new leader

# Leader election observable:
# - Term number increases
# - New leader sends heartbeats
# - Old leader becomes follower when recovered
```

## Paxos Algorithm

### Overview

Paxos is the original consensus algorithm, known for complexity but proven correct.

### Paxos Roles

```
┌──────────────────────────────────────────────────────┐
│                  Paxos Roles                         │
├──────────────────────────────────────────────────────┤
│ PROPOSER:                                             │
│   - Proposes values                                  │
│   - Coordinates consensus rounds                     │
│                                                       │
│ ACCEPTOR:                                             │
│   - Votes on proposed values                         │
│   - Majority of acceptors must agree                 │
│                                                       │
│ LEARNER:                                              │
│   - Learns chosen value                              │
│   - Passive (doesn't participate in voting)          │
│                                                       │
│ Note: Nodes can play multiple roles                  │
└──────────────────────────────────────────────────────┘
```

### Paxos Phases

```
┌──────────────────────────────────────────────────────┐
│              Paxos Two-Phase Process                 │
├──────────────────────────────────────────────────────┤
│ PHASE 1: Prepare                                      │
│   Proposer:                                          │
│   1. Choose proposal number n (higher than any seen) │
│   2. Send PREPARE(n) to majority of acceptors        │
│                                                       │
│   Acceptors:                                          │
│   3. If n > highest seen:                            │
│      - Promise not to accept proposals < n           │
│      - Reply with highest accepted proposal (if any) │
│                                                       │
│ PHASE 2: Accept                                       │
│   Proposer:                                          │
│   4. If majority promises:                           │
│      - If any acceptor returned value, use it        │
│      - Otherwise, use own value                      │
│   5. Send ACCEPT(n, value) to majority               │
│                                                       │
│   Acceptors:                                          │
│   6. If haven't promised higher n:                   │
│      - Accept proposal (n, value)                    │
│      - Reply with acceptance                         │
│                                                       │
│ LEARN:                                                │
│   7. Majority accepts → Value is chosen              │
│   8. Notify learners of chosen value                 │
└──────────────────────────────────────────────────────┘
```

### Paxos Example

```
Scenario: 5 nodes (A, B, C, D, E) need to agree on value

Round 1:
  Proposer A: PREPARE(1) → B, C, D
  B, C, D: Promise (no prior proposals)
  Proposer A: ACCEPT(1, "value_A") → B, C, D
  B, C, D: Accept
  Result: "value_A" chosen

Round 2 (concurrent with Round 1):
  Proposer E: PREPARE(2) → B, C, D
  B, C, D: Promise (already accepted (1, "value_A"))
  Proposer E: ACCEPT(2, "value_A") → Must use "value_A"
  B, C, D: Accept
  Result: "value_A" chosen (consistency maintained)
```

### Multi-Paxos

```
Single Paxos: Expensive (2 round trips per decision)
Multi-Paxos: Optimize for multiple decisions
  - Elect stable leader
  - Leader skips Phase 1 for subsequent proposals
  - Similar to Raft (leader-based)

Used by: Google Chubby, Google Spanner
```

## When to Use Consensus

### Scenarios Requiring Consensus

**Leader Election:**
```
Problem: Need exactly one leader
Solution: Raft/Paxos elects leader with majority votes
Examples: etcd, Consul, ZooKeeper
```

**Distributed Locks:**
```
Problem: Multiple services need exclusive access to resource
Solution: Consensus on lock ownership
Examples: etcd locks, Consul sessions
```

**Configuration Management:**
```
Problem: All nodes need same configuration
Solution: Consensus on config values
Examples: etcd for Kubernetes config
```

**Atomic Commit (Distributed Transactions):**
```
Problem: All nodes must commit or all must abort
Solution: Two-phase commit with consensus for coordinator election
Examples: Spanner, CockroachDB
```

### When NOT to Use Consensus

**High Write Throughput:**
```
Consensus is slow (coordination overhead)
Alternative: Leaderless replication (Dynamo-style)
```

**Eventual Consistency Acceptable:**
```
Consensus is overkill for social media, caching
Alternative: Asynchronous replication
```

**Single Datacenter:**
```
Leader-follower sufficient (simpler than consensus)
Alternative: PostgreSQL streaming replication
```

## Consensus vs Replication

### Comparison

| Aspect           | Consensus (Raft/Paxos)  | Replication (Leader-Follower) |
|------------------|-------------------------|-------------------------------|
| Leader Election  | Automatic (consensus)   | Manual or external tool       |
| Consistency      | Strong (majority)       | Strong (sync) or Eventual (async) |
| Availability     | Majority needed         | Leader needed                 |
| Complexity       | High                    | Medium                        |
| Latency          | Higher (2 round trips)  | Lower (1 round trip)          |
| Use Case         | Critical systems        | General replication           |

### Decision Framework

```
Choose Consensus When:
├─ Automatic leader election required
├─ Strong consistency critical
├─ Partition tolerance essential
└─ Complexity acceptable

Choose Replication When:
├─ Manual failover acceptable
├─ Lower latency needed
├─ Simpler operations preferred
└─ Eventual consistency OK
```

### Technology Examples

**Consensus-Based:**
- etcd: Raft for key-value store
- Consul: Raft for service discovery, configuration
- ZooKeeper: ZAB (Zookeeper Atomic Broadcast, Paxos-like)
- CockroachDB: Raft for distributed SQL
- TiDB: Raft for distributed SQL

**Replication-Based:**
- PostgreSQL: Streaming replication (leader-follower)
- MySQL: Binary log replication
- MongoDB: Replica sets (with automatic failover, not full consensus)
- Redis: Sentinel (master-replica with failover)

### Best Practices

**Cluster Size:**
- Odd numbers (3, 5, 7) for quorum
- 3 nodes: Tolerates 1 failure
- 5 nodes: Tolerates 2 failures
- More nodes = higher latency

**Network Stability:**
- Consensus sensitive to network partitions
- Ensure low-latency, stable network
- Co-locate nodes in same datacenter if possible

**Monitoring:**
- Track leader elections (frequency)
- Monitor quorum health
- Alert on slow consensus rounds
- Watch for split votes

**Testing:**
- Chaos engineering (kill nodes during consensus)
- Network partition tests
- Leader election under load
