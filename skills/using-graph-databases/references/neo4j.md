# Neo4j Reference Guide


## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
  - [Docker (Recommended for Development)](#docker-recommended-for-development)
  - [Language Drivers](#language-drivers)
- [Connection Setup](#connection-setup)
  - [Python](#python)
  - [TypeScript](#typescript)
- [Graph Data Science (GDS) Library](#graph-data-science-gds-library)
  - [Installation](#installation)
  - [Common Graph Algorithms](#common-graph-algorithms)
- [APOC Procedures](#apoc-procedures)
  - [Installation](#installation)
  - [Common APOC Procedures](#common-apoc-procedures)
- [Indexing and Constraints](#indexing-and-constraints)
  - [Indexes](#indexes)
  - [Constraints](#constraints)
- [Transaction Management](#transaction-management)
  - [Python](#python)
  - [TypeScript](#typescript)
- [Performance Optimization](#performance-optimization)
  - [Query Profiling](#query-profiling)
  - [Performance Best Practices](#performance-best-practices)
- [Neo4j Aura (Managed Cloud)](#neo4j-aura-managed-cloud)
  - [Connection](#connection)
  - [Features](#features)
- [Schema Design Patterns](#schema-design-patterns)
  - [Time-Based Partitioning](#time-based-partitioning)
  - [Intermediate Nodes for Filtering](#intermediate-nodes-for-filtering)
- [Backup and Restore](#backup-and-restore)
  - [Dump Database](#dump-database)
  - [Load Database](#load-database)
  - [Export to Cypher Script](#export-to-cypher-script)
- [Monitoring](#monitoring)
  - [Check Database Stats](#check-database-stats)
  - [Kill Long-Running Queries](#kill-long-running-queries)
- [Common Cypher Functions](#common-cypher-functions)
  - [String Functions](#string-functions)
  - [List Functions](#list-functions)
  - [Aggregation Functions](#aggregation-functions)
- [Further Resources](#further-resources)

## Overview

Neo4j is the most mature and widely-used graph database (since 2007). It uses the Cypher query language and provides 65+ graph algorithms through the Graph Data Science (GDS) library.

## Installation

### Docker (Recommended for Development)
```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest
```

Access Neo4j Browser at: http://localhost:7474

### Language Drivers

**Python**:
```bash
pip install neo4j
```

**TypeScript/JavaScript**:
```bash
npm install neo4j-driver
```

**Rust**:
```bash
cargo add neo4rs
```

**Go**:
```bash
go get github.com/neo4j/neo4j-go-driver/v5/neo4j
```

## Connection Setup

### Python
```python
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def verify_connectivity(self):
        with self.driver.session() as session:
            result = session.run("RETURN 1 AS num")
            return result.single()["num"] == 1

# Usage
db = Neo4jConnection("bolt://localhost:7687", "neo4j", "password")
print(f"Connected: {db.verify_connectivity()}")
```

### TypeScript
```typescript
import neo4j, { Driver, Session } from 'neo4j-driver'

class Neo4jConnection {
  private driver: Driver

  constructor(uri: string, username: string, password: string) {
    this.driver = neo4j.driver(uri, neo4j.auth.basic(username, password))
  }

  async close(): Promise<void> {
    await this.driver.close()
  }

  async verifyConnectivity(): Promise<boolean> {
    const session: Session = this.driver.session()
    try {
      const result = await session.run('RETURN 1 AS num')
      return result.records[0].get('num') === 1
    } finally {
      await session.close()
    }
  }
}

// Usage
const db = new Neo4jConnection('bolt://localhost:7687', 'neo4j', 'password')
console.log(`Connected: ${await db.verifyConnectivity()}`)
```

## Graph Data Science (GDS) Library

Neo4j's GDS library provides 65+ production-quality graph algorithms.

### Installation
```cypher
// Check if GDS is installed
CALL gds.list()

// For Neo4j Desktop or self-hosted, install GDS plugin
// Docker: Include GDS-enabled image
```

### Common Graph Algorithms

#### PageRank (Centrality)
Find influential nodes based on their connections.

```cypher
// 1. Create graph projection
CALL gds.graph.project(
  'socialGraph',
  'Person',
  'FRIEND'
)

// 2. Run PageRank
CALL gds.pageRank.stream('socialGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC
LIMIT 10
```

#### Community Detection (Louvain)
Find clusters of densely connected nodes.

```cypher
CALL gds.louvain.stream('socialGraph')
YIELD nodeId, communityId
RETURN gds.util.asNode(nodeId).name AS name, communityId
ORDER BY communityId
```

#### Shortest Path (Dijkstra)
Find optimal path between nodes considering weighted relationships.

```cypher
MATCH (source:Location {name: 'New York'}), (target:Location {name: 'Los Angeles'})
CALL gds.shortestPath.dijkstra.stream('roadNetwork', {
  sourceNode: source,
  targetNode: target,
  relationshipWeightProperty: 'distance'
})
YIELD path, totalCost
RETURN [node IN nodes(path) | node.name] AS route, totalCost
```

#### Node Similarity
Find similar nodes based on their neighborhoods.

```cypher
CALL gds.nodeSimilarity.stream('socialGraph')
YIELD node1, node2, similarity
RETURN
  gds.util.asNode(node1).name AS person1,
  gds.util.asNode(node2).name AS person2,
  similarity
ORDER BY similarity DESC
LIMIT 20
```

## APOC Procedures

APOC (Awesome Procedures On Cypher) extends Neo4j with utility functions.

### Installation
```bash
# Docker: Include APOC-enabled image
docker run -d \
  --name neo4j \
  -e NEO4J_PLUGINS='["apoc"]' \
  neo4j:latest
```

### Common APOC Procedures

#### Batch Operations
```cypher
// Batch create nodes from list
CALL apoc.periodic.iterate(
  "UNWIND $users AS user RETURN user",
  "CREATE (u:User {id: user.id, name: user.name})",
  {batchSize: 1000, params: {users: $userList}}
)
```

#### JSON Import/Export
```cypher
// Import JSON
CALL apoc.load.json('file:///path/to/data.json')
YIELD value
CREATE (u:User {id: value.id, name: value.name})

// Export to JSON
CALL apoc.export.json.query(
  "MATCH (u:User) RETURN u",
  "users.json",
  {}
)
```

#### Graph Algorithms (APOC)
```cypher
// Betweenness centrality
MATCH (u:User)
WITH collect(u) AS users
CALL apoc.algo.betweenness(['FRIEND'], users, 'BOTH')
YIELD node, score
RETURN node.name, score
ORDER BY score DESC
LIMIT 10
```

## Indexing and Constraints

### Indexes
```cypher
// Single-property index
CREATE INDEX user_email FOR (u:User) ON (u.email)

// Composite index (Neo4j 5.x+)
CREATE INDEX user_name_location FOR (u:User) ON (u.name, u.location)

// Full-text search index
CREATE FULLTEXT INDEX product_search FOR (p:Product) ON EACH [p.name, p.description]

// List all indexes
SHOW INDEXES
```

### Constraints
```cypher
// Unique constraint
CREATE CONSTRAINT user_email_unique FOR (u:User) REQUIRE u.email IS UNIQUE

// Existence constraint (Enterprise only)
CREATE CONSTRAINT user_name_exists FOR (u:User) REQUIRE u.name IS NOT NULL

// Node key (composite uniqueness)
CREATE CONSTRAINT user_key FOR (u:User) REQUIRE (u.id, u.email) IS NODE KEY

// List all constraints
SHOW CONSTRAINTS
```

## Transaction Management

### Python
```python
def create_friendship_transaction(tx, user1_id, user2_id):
    query = """
    MATCH (u1:User {id: $user1Id}), (u2:User {id: $user2Id})
    MERGE (u1)-[:FRIEND {since: datetime()}]->(u2)
    MERGE (u2)-[:FRIEND {since: datetime()}]->(u1)
    RETURN u1.name, u2.name
    """
    result = tx.run(query, user1Id=user1_id, user2Id=user2_id)
    return result.single()

# Execute in transaction
with driver.session() as session:
    result = session.execute_write(create_friendship_transaction, "u123", "u456")
    print(f"Created friendship between {result[0]} and {result[1]}")
```

### TypeScript
```typescript
async createFriendship(user1Id: string, user2Id: string): Promise<void> {
  const session = this.driver.session()
  try {
    await session.executeWrite(async tx => {
      const query = `
        MATCH (u1:User {id: $user1Id}), (u2:User {id: $user2Id})
        MERGE (u1)-[:FRIEND {since: datetime()}]->(u2)
        MERGE (u2)-[:FRIEND {since: datetime()}]->(u1)
      `
      await tx.run(query, { user1Id, user2Id })
    })
  } finally {
    await session.close()
  }
}
```

## Performance Optimization

### Query Profiling
```cypher
// EXPLAIN: Shows query plan without executing
EXPLAIN
MATCH (u:User {email: 'alice@example.com'})-[:FRIEND*1..3]->(friend)
RETURN friend.name

// PROFILE: Executes and shows detailed statistics
PROFILE
MATCH (u:User {email: 'alice@example.com'})-[:FRIEND*1..3]->(friend)
RETURN friend.name
LIMIT 100
```

### Performance Best Practices

**1. Bounded Variable-Length Paths**
```cypher
// SLOW
MATCH (u:User)-[:FRIEND*]->(distant)

// FAST
MATCH (u:User)-[:FRIEND*1..4]->(distant)
LIMIT 100
```

**2. Use Indexes**
```cypher
// Create index before querying
CREATE INDEX user_email FOR (u:User) ON (u.email)

// Query benefits from index
MATCH (u:User {email: 'alice@example.com'})
RETURN u
```

**3. Eager Loading with WITH**
```cypher
// Materialize intermediate results
MATCH (u:User)-[:FRIEND]->(f)
WITH u, count(f) AS friendCount
WHERE friendCount > 10
RETURN u.name, friendCount
```

## Neo4j Aura (Managed Cloud)

Neo4j Aura is the fully managed cloud service.

### Connection
```python
# Aura uses neo4j+s:// or neo4j+ssc:// protocols
driver = GraphDatabase.driver(
    "neo4j+s://xxxxx.databases.neo4j.io",
    auth=("neo4j", "password")
)
```

### Features
- Auto-scaling
- Automated backups
- Security (encryption at rest and in transit)
- Monitoring dashboards
- Free tier available (50K nodes, 175K relationships)

## Schema Design Patterns

### Time-Based Partitioning
```cypher
// Avoid: User directly connected to millions of posts
(:User)-[:POSTED]->(:Post) // 1M+ relationships

// Better: Partition by time
(:User)-[:POSTED_IN]->(:Year {year: 2025})
  -[:HAS_MONTH]->(:Month {month: 12})
  -[:HAS_DAY]->(:Day {day: 15})
  -[:CONTAINS]->(:Post)
```

### Intermediate Nodes for Filtering
```cypher
// Complex filtering on categories
(:Product)-[:IN_CATEGORY]->(:Category)
(:Product)-[:HAS_TAG]->(:Tag)

// Query becomes simpler
MATCH (c:Category {name: 'Electronics'})<-[:IN_CATEGORY]-(p:Product)-[:HAS_TAG]->(t:Tag {name: 'Sale'})
RETURN p
```

## Backup and Restore

### Dump Database
```bash
neo4j-admin database dump neo4j --to-path=/backups
```

### Load Database
```bash
neo4j-admin database load neo4j --from-path=/backups
```

### Export to Cypher Script
```cypher
CALL apoc.export.cypher.all("backup.cypher", {
  format: "cypher-shell",
  useOptimizations: {type: "UNWIND_BATCH", unwindBatchSize: 20}
})
```

## Monitoring

### Check Database Stats
```cypher
// Database info
CALL dbms.queryJmx('org.neo4j:instance=kernel#0,name=Store sizes') YIELD attributes
RETURN attributes

// Transaction stats
CALL dbms.listTransactions()

// Active queries
CALL dbms.listQueries()
```

### Kill Long-Running Queries
```cypher
// List queries
CALL dbms.listQueries() YIELD queryId, query, elapsedTimeMillis
WHERE elapsedTimeMillis > 30000
RETURN queryId, query

// Kill query
CALL dbms.killQuery('query-123')
```

## Common Cypher Functions

### String Functions
```cypher
RETURN toLower('HELLO') // 'hello'
RETURN toUpper('hello') // 'HELLO'
RETURN substring('Hello World', 0, 5) // 'Hello'
RETURN replace('Hello World', 'World', 'Neo4j') // 'Hello Neo4j'
```

### List Functions
```cypher
RETURN size([1,2,3,4,5]) // 5
RETURN head([1,2,3,4,5]) // 1
RETURN tail([1,2,3,4,5]) // [2,3,4,5]
RETURN range(0, 10, 2) // [0,2,4,6,8,10]
```

### Aggregation Functions
```cypher
MATCH (u:User)-[:PURCHASED]->(p:Product)
RETURN
  count(p) AS totalPurchases,
  count(DISTINCT p) AS uniqueProducts,
  avg(p.price) AS avgPrice,
  sum(p.price) AS totalSpent,
  collect(p.name) AS productNames
```

## Further Resources

- Official Neo4j Documentation: https://neo4j.com/docs/
- Graph Data Science Manual: https://neo4j.com/docs/graph-data-science/current/
- APOC Documentation: https://neo4j.com/labs/apoc/
- Cypher Manual: https://neo4j.com/docs/cypher-manual/current/
- Neo4j GraphAcademy (Free Training): https://graphacademy.neo4j.com/
