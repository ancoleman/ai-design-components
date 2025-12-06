---
sidebar_position: 6
title: Graph Databases
description: Graph database implementation for relationship-heavy data models
tags: [backend, database, graph, neo4j, cypher, relationships]
---

# Graph Databases

Graph database selection and implementation for applications where relationships between entities are first-class citizens. Unlike relational databases that model relationships through foreign keys and joins, graph databases natively represent connections as properties, enabling efficient traversal-heavy queries.

## When to Use

Use graph databases when:
- **Deep relationship traversals** (4+ hops): "Friends of friends of friends"
- **Variable/evolving relationships**: Schema changes don't break existing queries
- **Path finding**: Shortest route, network analysis, dependency chains
- **Pattern matching**: Fraud detection, recommendation engines, access control

**Do NOT use graph databases when:**
- Fixed schema with shallow joins (2-3 tables) → Use PostgreSQL
- Primarily aggregations/analytics → Use columnar databases
- Key-value lookups only → Use Redis/DynamoDB

## Multi-Language Support

This skill provides patterns for:
- **Python**: neo4j driver
- **TypeScript**: neo4j-driver
- **Rust**: neo4rs
- **Go**: neo4j-go-driver, ArangoDB (go-driver)

## Quick Decision Framework

```
DATA CHARACTERISTICS?
├── Fixed schema, shallow joins (≤3 hops)
│   └─ PostgreSQL (relational)
│
├── Already on PostgreSQL + simple graphs
│   └─ Apache AGE (PostgreSQL extension)
│
├── Deep traversals (4+ hops) + general purpose
│   └─ Neo4j (battle-tested, largest ecosystem)
│
├── Multi-model (documents + graph)
│   └─ ArangoDB
│
├── AWS-native, serverless
│   └─ Amazon Neptune
│
└── Real-time streaming, in-memory
    └─ Memgraph
```

## Core Concepts

### Property Graph Model

Graph databases store data as:
- **Nodes** (vertices): Entities with labels and properties
- **Relationships** (edges): Typed connections with properties
- **Properties**: Key-value pairs on nodes and relationships

```
(Person {name: "Alice", age: 28})-[:FRIEND {since: "2020-01-15"}]->(Person {name: "Bob"})
```

## Common Cypher Patterns

### Pattern 1: Basic Matching
```cypher
// Find all users at a company
MATCH (u:User)-[:WORKS_AT]->(c:Company {name: 'Acme Corp'})
RETURN u.name, u.title
```

### Pattern 2: Variable-Length Paths
```cypher
// Find friends up to 3 degrees away
MATCH (u:User {name: 'Alice'})-[:FRIEND*1..3]->(friend)
WHERE u &lt;> friend
RETURN DISTINCT friend.name
LIMIT 100
```

### Pattern 3: Shortest Path
```cypher
// Find shortest connection between two users
MATCH path = shortestPath(
  (a:User {name: 'Alice'})-[*]-(b:User {name: 'Bob'})
)
RETURN path, length(path) AS distance
```

### Pattern 4: Recommendations
```cypher
// Collaborative filtering: Products liked by similar users
MATCH (u:User {id: $userId})-[:PURCHASED]->(p:Product)<-[:PURCHASED]-(similar)
MATCH (similar)-[:PURCHASED]->(rec:Product)
WHERE NOT exists((u)-[:PURCHASED]->(rec))
RETURN rec.name, count(*) AS score
ORDER BY score DESC
LIMIT 10
```

### Pattern 5: Fraud Detection
```cypher
// Detect circular money flows
MATCH path = (a:Account)-[:SENT*3..6]->(a)
WHERE all(r IN relationships(path) WHERE r.amount > 1000)
RETURN path, [r IN relationships(path) | r.amount] AS amounts
```

## Database Selection Guide

### Neo4j (Primary Recommendation)

**Use for:** General-purpose graph applications

**Strengths:**
- Most mature (2007), largest community (2M+ developers)
- 65+ graph algorithms (GDS library): PageRank, Louvain, Dijkstra
- Best tooling: Neo4j Browser, Bloom visualization
- Comprehensive Cypher support

**Installation:**
```bash
# Python driver
pip install neo4j

# TypeScript driver
npm install neo4j-driver

# Rust driver
cargo add neo4rs
```

### ArangoDB

**Use for:** Multi-model applications (documents + graph)

**Strengths:**
- Store documents AND graph in one database
- AQL combines document and graph queries
- Schema flexibility with relationships

### Apache AGE

**Use for:** Adding graph capabilities to existing PostgreSQL

**Strengths:**
- Extend PostgreSQL with graph queries
- No new infrastructure needed
- Query both relational and graph data

## Graph Data Modeling Patterns

### Best Practice 1: Relationships as First-Class Citizens

**Anti-pattern** (storing relationships in node properties):
```cypher
// BAD
(:Person {name: 'Alice', friend_ids: ['b123', 'c456']})
```

**Pattern** (explicit relationships):
```cypher
// GOOD
(:Person {name: 'Alice'})-[:FRIEND]->(:Person {id: 'b123'})
(:Person {name: 'Alice'})-[:FRIEND]->(:Person {id: 'c456'})
```

### Best Practice 2: Relationship Properties for Metadata

```cypher
// Track interaction details on relationships
(:Person)-[:FRIEND {
  since: '2020-01-15',
  strength: 0.85,
  last_interaction: datetime()
}]->(:Person)
```

### Best Practice 3: Bounded Traversals for Performance

```cypher
// SLOW: Unbounded traversal
MATCH (a)-[:FRIEND*]->(distant)
RETURN distant

// FAST: Bounded depth with index
MATCH (a)-[:FRIEND*1..4]->(distant)
WHERE distant.active = true
RETURN distant
LIMIT 100
```

### Best Practice 4: Avoid Supernodes

**Problem:** Nodes with thousands of relationships slow traversals.

**Solution:** Intermediate aggregation nodes
```cypher
// Instead of: (:User)-[:POSTED]->(:Post) [1M relationships]

// Use time partitioning:
(:User)-[:POSTED_IN]->(:Year {year: 2025})
       -[:HAS_MONTH]->(:Month {month: 12})
       -[:HAS_POST]->(:Post)
```

## Use Case Examples

### Social Network

**Key features:**
- Friend recommendations (friends-of-friends)
- Mutual connections
- News feed generation
- Influence metrics

### Knowledge Graph for AI/RAG

**Key features:**
- Hybrid vector + graph search
- Entity relationship mapping
- Context expansion for LLM prompts
- Semantic relationship traversal

**Integration with Vector Databases:**
```python
# Step 1: Vector search in Qdrant/pgvector
vector_results = qdrant.search(collection="concepts", query_vector=embedding)

# Step 2: Expand with graph relationships
concept_ids = [r.id for r in vector_results]
graph_context = neo4j.run("""
  MATCH (c:Concept) WHERE c.id IN $ids
  MATCH (c)-[:RELATED_TO|IS_A*1..2]-(related)
  RETURN c, related, relationships(path)
""", ids=concept_ids)
```

### Recommendation Engine

**Strategies:**
1. **Collaborative filtering**: "Users who bought X also bought Y"
2. **Content-based**: "Products similar to what you like"
3. **Session-based**: "Recently viewed items"

### Fraud Detection

**Detection patterns:**
- Circular money flows
- Shared devices across accounts
- Rapid transaction chains
- Connection pattern anomalies

## Performance Optimization

### Indexing
```cypher
// Single-property index
CREATE INDEX user_email FOR (u:User) ON (u.email)

// Composite index (Neo4j 5.x+)
CREATE INDEX user_name_location FOR (u:User) ON (u.name, u.location)

// Full-text search
CREATE FULLTEXT INDEX product_search FOR (p:Product) ON EACH [p.name, p.description]
```

### Caching Expensive Aggregations
```cypher
// Materialize friend count as property
MATCH (u:User)-[:FRIEND]->(f)
WITH u, count(f) AS friendCount
SET u.friend_count = friendCount

// Query becomes instant
MATCH (u:User) WHERE u.friend_count > 100
RETURN u.name, u.friend_count
```

## Language Integration

### Python (Neo4j)

```python
from neo4j import GraphDatabase

class GraphDB:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def find_friends_of_friends(self, user_id: str, max_depth: int = 2):
        query = """
        MATCH (u:User {id: $userId})-[:FRIEND*1..$maxDepth]->(fof)
        WHERE u &lt;> fof
        RETURN DISTINCT fof.id, fof.name
        LIMIT 100
        """
        with self.driver.session() as session:
            result = session.run(query, userId=user_id, maxDepth=max_depth)
            return [dict(record) for record in result]
```

### TypeScript (Neo4j)

```typescript
import neo4j, { Driver } from 'neo4j-driver'

class Neo4jService {
  private driver: Driver

  constructor(uri: string, username: string, password: string) {
    this.driver = neo4j.driver(uri, neo4j.auth.basic(username, password))
  }

  async findFriendsOfFriends(userId: string, maxDepth: number = 2) {
    const session = this.driver.session()
    try {
      const result = await session.run(
        `MATCH (u:User {id: $userId})-[:FRIEND*1..$maxDepth]->(fof)
         WHERE u &lt;> fof
         RETURN DISTINCT fof.id, fof.name
         LIMIT 100`,
        { userId, maxDepth }
      )
      return result.records.map(r => r.toObject())
    } finally {
      await session.close()
    }
  }
}
```

## Integration with Other Skills

### With databases-vector (Hybrid Search)
Combine vector similarity with graph context for AI/RAG applications.

### With search-filter
Implement relationship-based queries: "Find all users within 3 degrees of connection"

### With ai-chat
Use knowledge graphs to enrich LLM context with structured relationships.

### With auth-security (ReBAC)
Implement relationship-based access control: "Can user X access resource Y through relation Z?"

## Related Skills

- [Vector Databases](./using-vector-databases) - Hybrid vector + graph search
- [AI Data Engineering](./ai-data-engineering) - Knowledge graph pipelines
- [Search & Filter](../frontend/implementing-search-filter) - Graph-based search UIs

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/using-graph-databases)
- Neo4j: https://neo4j.com/
- ArangoDB: https://www.arangodb.com/
- Apache AGE: https://age.apache.org/
