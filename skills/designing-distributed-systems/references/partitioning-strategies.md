# Partitioning Strategies

## Table of Contents

1. [Hash Partitioning](#hash-partitioning)
2. [Consistent Hashing](#consistent-hashing)
3. [Range Partitioning](#range-partitioning)
4. [Geographic Partitioning](#geographic-partitioning)
5. [Partition Rebalancing](#partition-rebalancing)

## Hash Partitioning

### Basic Concept

```
Key → Hash(Key) % N → Partition Number

Example:
  user_id = "user123"
  hash("user123") = 2489017
  2489017 % 4 = 1
  → Partition 1
```

### Simple Hash Partitioning

```python
import hashlib

class SimpleHashPartitioner:
    def __init__(self, num_partitions):
        self.num_partitions = num_partitions

    def get_partition(self, key):
        # Hash the key
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        # Modulo to get partition
        return hash_value % self.num_partitions

# Usage
partitioner = SimpleHashPartitioner(num_partitions=4)
print(partitioner.get_partition("user123"))  # → 1
print(partitioner.get_partition("user456"))  # → 3
```

### Problem: Adding/Removing Nodes

```
Initial: 4 nodes
  user123 → hash % 4 = 1 → Node 1

Add 1 node (5 nodes total):
  user123 → hash % 5 = 2 → Node 2 (MOVED!)

Result: Most keys move to different partitions
        Massive data reshuffling required
```

### Use Cases

- Even key distribution
- Random access patterns
- No range query requirements

### Benefits & Trade-offs

**Benefits:**
- ✅ Even distribution
- ✅ Simple to implement

**Trade-offs:**
- ❌ No range queries
- ❌ Rebalancing shuffles most data
- ❌ Keys with similar values scattered

## Consistent Hashing

### Architecture

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

### Implementation

```python
import hashlib
import bisect

class ConsistentHash:
    def __init__(self, nodes=None, replicas=150):
        """
        nodes: List of node identifiers
        replicas: Number of virtual nodes per physical node
        """
        self.replicas = replicas
        self.ring = {}  # hash -> node
        self.sorted_keys = []

        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key):
        """Hash function returning integer"""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node):
        """Add node with virtual replicas"""
        for i in range(self.replicas):
            virtual_key = f"{node}:{i}"
            hash_val = self._hash(virtual_key)
            self.ring[hash_val] = node
            bisect.insort(self.sorted_keys, hash_val)

    def remove_node(self, node):
        """Remove node and its virtual replicas"""
        for i in range(self.replicas):
            virtual_key = f"{node}:{i}"
            hash_val = self._hash(virtual_key)
            del self.ring[hash_val]
            self.sorted_keys.remove(hash_val)

    def get_node(self, key):
        """Find node responsible for key"""
        if not self.ring:
            return None

        hash_val = self._hash(key)

        # Binary search for first node >= hash_val
        idx = bisect.bisect(self.sorted_keys, hash_val)
        if idx == len(self.sorted_keys):
            idx = 0  # Wrap around

        return self.ring[self.sorted_keys[idx]]

    def get_nodes(self, key, n=3):
        """Get N nodes for replication"""
        if not self.ring or n > len(set(self.ring.values())):
            return []

        hash_val = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, hash_val)

        nodes = []
        seen = set()

        while len(nodes) < n:
            if idx >= len(self.sorted_keys):
                idx = 0

            node = self.ring[self.sorted_keys[idx]]
            if node not in seen:
                nodes.append(node)
                seen.add(node)

            idx += 1

        return nodes

# Usage
ch = ConsistentHash(['node1', 'node2', 'node3', 'node4'])

# Get node for key
print(ch.get_node('user123'))  # → node2

# Add new node (minimal data movement)
ch.add_node('node5')
print(ch.get_node('user123'))  # → May still be node2

# Get replication nodes
print(ch.get_nodes('user123', n=3))  # → [node2, node3, node4]
```

### Virtual Nodes (Vnodes)

```
Why Virtual Nodes?

Without Vnodes (4 physical nodes):
  Node A: 25% of data
  Node B: 25% of data
  Node C: 25% of data
  Node D: 25% of data
  (Uneven if nodes have different capacities)

With Vnodes (150 per node):
  Node A: ~25% of data (even distribution)
  Node B: ~25% of data
  Node C: ~25% of data
  Node D: ~25% of data

Benefits:
- More even distribution
- Easier rebalancing (move vnodes, not entire nodes)
- Handle heterogeneous nodes (more vnodes for powerful nodes)
```

### Use Cases

- Distributed caches: Redis Cluster, Memcached
- Distributed databases: Cassandra, DynamoDB
- Load balancing: consistent server selection
- CDN: edge server selection

### Benefits & Trade-offs

**Benefits:**
- ✅ Minimal data movement when scaling
- ✅ Even distribution with virtual nodes
- ✅ No central coordinator
- ✅ Predictable data location

**Trade-offs:**
- ❌ No range queries
- ❌ Complexity (virtual nodes, rebalancing)

## Range Partitioning

### Architecture

```
┌──────────────────────────────────────────────────────┐
│              Range Partitioning                      │
│                                                       │
│ Key Range      Partition     Node                    │
│ A - F       →  Partition 1 → Node 1                  │
│ G - M       →  Partition 2 → Node 2                  │
│ N - S       →  Partition 3 → Node 3                  │
│ T - Z       →  Partition 4 → Node 4                  │
│                                                       │
│ Examples:                                             │
│ "Alice"   (A-F)  → Node 1                            │
│ "Bob"     (A-F)  → Node 1                            │
│ "Nancy"   (N-S)  → Node 3                            │
│ "Zoe"     (T-Z)  → Node 4                            │
└──────────────────────────────────────────────────────┘
```

### Implementation

```python
class RangePartitioner:
    def __init__(self, ranges):
        """
        ranges: List of (start_key, end_key, node) tuples
        Example: [('A', 'F', 'node1'), ('G', 'M', 'node2'), ...]
        """
        self.ranges = sorted(ranges, key=lambda x: x[0])

    def get_node(self, key):
        """Find node for key using binary search"""
        for start, end, node in self.ranges:
            if start <= key <= end:
                return node
        return None

    def get_range(self, start_key, end_key):
        """Get all nodes for range query"""
        nodes = set()
        for range_start, range_end, node in self.ranges:
            # Check if ranges overlap
            if not (end_key < range_start or start_key > range_end):
                nodes.add(node)
        return list(nodes)

# Usage
partitioner = RangePartitioner([
    ('A', 'F', 'node1'),
    ('G', 'M', 'node2'),
    ('N', 'S', 'node3'),
    ('T', 'Z', 'node4')
])

print(partitioner.get_node('Alice'))  # → node1
print(partitioner.get_node('Nancy'))  # → node3

# Range query: Get all names from 'D' to 'P'
print(partitioner.get_range('D', 'P'))  # → [node1, node2, node3]
```

### Time-Series Partitioning

```python
from datetime import datetime, timedelta

class TimeSeriesPartitioner:
    def __init__(self, partition_duration_days=7):
        self.partition_duration = timedelta(days=partition_duration_days)
        self.partitions = {}

    def get_partition(self, timestamp):
        """Get partition for timestamp"""
        partition_start = timestamp - (timestamp - datetime.min) % self.partition_duration
        partition_name = partition_start.strftime('%Y-%m-%d')

        if partition_name not in self.partitions:
            self.partitions[partition_name] = {
                'start': partition_start,
                'end': partition_start + self.partition_duration,
                'node': self._assign_node(partition_name)
            }

        return self.partitions[partition_name]

    def _assign_node(self, partition_name):
        # Round-robin or hash-based assignment
        return f"node{hash(partition_name) % 4}"

# Usage
partitioner = TimeSeriesPartitioner(partition_duration_days=7)

# Logs from different dates
log1 = partitioner.get_partition(datetime(2025, 1, 1))  # → node1 (week 1)
log2 = partitioner.get_partition(datetime(2025, 1, 8))  # → node2 (week 2)
```

### Hot Spot Problem

```
Problem: Uneven access patterns

Example: Social media
  Users 'A' - 'C': 1M requests/sec (celebrity accounts)
  Users 'D' - 'Z': 100K requests/sec (normal users)

  Node 1 (A-C): OVERLOADED
  Node 2-4 (D-Z): Underutilized

Solutions:
1. Add hash component
   Key = (range_key, hash(range_key) % 10)
   Splits hot partition into 10 sub-partitions

2. Manual splitting
   Detect hot partition, split into smaller ranges

3. Dynamic rebalancing
   Monitor load, redistribute partitions
```

### Use Cases

- Time-series data: Logs, metrics, events
- Leaderboards: Scores by range
- Geographic data: Coordinates
- Alphabetical listings: User directories

### Benefits & Trade-offs

**Benefits:**
- ✅ Efficient range queries
- ✅ Ordered scans
- ✅ Natural data organization

**Trade-offs:**
- ❌ Hot spots (skewed access patterns)
- ❌ Manual range definition
- ❌ Rebalancing complexity

## Geographic Partitioning

### Architecture

```
┌──────────────────────────────────────────────────────┐
│            Geographic Partitioning                   │
│                                                       │
│ Region         Partition       Datacenter            │
│ US-East     →  Partition 1  →  Virginia             │
│ US-West     →  Partition 2  →  Oregon               │
│ EU-West     →  Partition 3  →  Ireland              │
│ APAC        →  Partition 4  →  Singapore            │
│                                                       │
│ User Location → Nearest Partition                    │
│                                                       │
│ US user (IP: 192.168.1.1)  → US-East partition       │
│ EU user (IP: 82.45.67.89)  → EU-West partition       │
└──────────────────────────────────────────────────────┘
```

### Implementation

```python
import geoip2.database

class GeoPartitioner:
    def __init__(self, geoip_db_path):
        self.geoip_reader = geoip2.database.Reader(geoip_db_path)
        self.region_mapping = {
            'NA': 'us-east',  # North America
            'EU': 'eu-west',  # Europe
            'AS': 'apac',     # Asia
            'SA': 'sa-east',  # South America
            'AF': 'eu-west',  # Africa → Europe (closer)
            'OC': 'apac'      # Oceania → Asia-Pacific
        }

    def get_partition(self, ip_address):
        """Get partition based on IP geolocation"""
        try:
            response = self.geoip_reader.city(ip_address)
            continent = response.continent.code
            return self.region_mapping.get(continent, 'us-east')
        except:
            return 'us-east'  # Default fallback

    def get_partition_by_country(self, country_code):
        """Get partition based on country code"""
        eu_countries = ['GB', 'FR', 'DE', 'IT', 'ES', 'NL', 'IE']
        apac_countries = ['CN', 'JP', 'IN', 'SG', 'AU', 'KR']

        if country_code in eu_countries:
            return 'eu-west'
        elif country_code in apac_countries:
            return 'apac'
        else:
            return 'us-east'

# Usage
partitioner = GeoPartitioner('/path/to/GeoLite2-City.mmdb')

# Route based on IP
partition = partitioner.get_partition('82.45.67.89')  # → eu-west
partition = partitioner.get_partition('192.168.1.1')  # → us-east
```

### GDPR Compliance

```python
class GDPRCompliantPartitioner:
    def __init__(self):
        # EU user data MUST stay in EU
        self.eu_countries = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK',
                            'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE',
                            'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL',
                            'PT', 'RO', 'SK', 'SI', 'ES', 'SE']

    def get_partition(self, user_country):
        """Ensure EU data stays in EU"""
        if user_country in self.eu_countries:
            return {
                'partition': 'eu-west',
                'replication': ['eu-central', 'eu-north'],  # Within EU only
                'compliance': 'GDPR'
            }
        else:
            return {
                'partition': 'us-east',
                'replication': ['us-west', 'apac'],
                'compliance': 'None'
            }

# Usage
partitioner = GDPRCompliantPartitioner()
eu_user = partitioner.get_partition('DE')  # → eu-west (GDPR compliant)
us_user = partitioner.get_partition('US')  # → us-east
```

### Use Cases

- GDPR/data residency compliance
- Low-latency access (users read/write locally)
- Multi-region SaaS applications
- Content delivery networks (CDN)

### Benefits & Trade-offs

**Benefits:**
- ✅ Low latency (local access)
- ✅ Compliance (GDPR, data residency)
- ✅ Disaster recovery (region-level)

**Trade-offs:**
- ❌ Complex cross-region queries
- ❌ User migration (if user moves regions)
- ❌ Operational overhead (multiple datacenters)

## Partition Rebalancing

### Strategies

**1. Fixed Number of Partitions:**
```
Create more partitions than nodes
Example: 256 partitions, 4 nodes → 64 partitions/node

Add node 5:
  Move 51 partitions from existing nodes to node 5
  (256 / 5 = 51 partitions/node)

Pro: Simple, predictable
Con: Fixed, may need rebalancing later
```

**2. Dynamic Partitioning:**
```
Split partitions when they grow too large

Partition 1 size: 100GB → Split into Partition 1A and 1B
Partition 1A: 50GB → Node 1
Partition 1B: 50GB → Node 2 (new)

Pro: Adapts to data growth
Con: Complexity
```

**3. Proportional Partitioning:**
```
Nodes with more capacity get more partitions

Node 1 (2TB): 200 partitions
Node 2 (1TB): 100 partitions
Node 3 (1TB): 100 partitions

Pro: Efficient resource utilization
Con: Requires capacity awareness
```

### Rebalancing Example (Cassandra)

```python
# Cassandra uses consistent hashing with vnodes
# Default: 256 vnodes per node

# Adding new node
# 1. New node joins cluster
# 2. Cassandra assigns vnodes to new node
# 3. Data streams from existing nodes to new node
# 4. Gradual rebalancing (no downtime)

# Monitor rebalancing
from cassandra.cluster import Cluster

cluster = Cluster(['node1', 'node2', 'node3'])
session = cluster.connect()

# Check token distribution
result = session.execute("SELECT * FROM system.peers")
for row in result:
    print(f"Node: {row.peer}, Tokens: {row.tokens}")

# Check rebalancing progress
result = session.execute("SELECT * FROM system.compaction_history")
for row in result:
    print(f"Keyspace: {row.keyspace_name}, Progress: {row.bytes_compacted}/{row.bytes_total}")
```

### Best Practices

**Avoid Frequent Rebalancing:**
- Plan capacity ahead
- Over-provision partitions (256-1024 per node)
- Monitor growth trends

**Minimize Data Movement:**
- Use consistent hashing
- Virtual nodes for fine-grained rebalancing
- Gradual rebalancing (not all at once)

**Monitor Rebalancing:**
- Track data movement progress
- Monitor network bandwidth
- Alert on slow rebalancing

**Test Before Production:**
- Test rebalancing in staging
- Chaos engineering (node failures during rebalancing)
- Verify data integrity post-rebalancing
