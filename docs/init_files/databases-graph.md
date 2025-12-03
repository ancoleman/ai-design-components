# Graph Databases - Master Plan

> **Skill Purpose**: Guide graph database selection and implementation for relationship-heavy data models across social networks, recommendation engines, knowledge graphs, and fraud detection systems.
>
> **Date**: December 2025
> **Status**: Planning Phase
> **Sources**: FULL_STACK_SKILLS_UNIFIED.md + Context7 + Graph Database Research (2025)

---

## Executive Summary

This skill enables developers to select and implement graph databases for applications where relationships between entities are first-class citizens. Unlike relational databases that model relationships through foreign keys and joins, graph databases natively represent connections, making them optimal for traversal-heavy queries like "find friends of friends" or "shortest path between entities."

### Primary Use Cases

| Use Case | Example Queries | Value Proposition |
|----------|----------------|-------------------|
| **Social Networks** | "Friends of friends", "mutual connections" | Sub-second social graph traversals |
| **Recommendation Engines** | "Users who liked this also liked...", "similar products" | Real-time collaborative filtering |
| **Knowledge Graphs** | "All concepts related to X", "semantic relationships" | AI/RAG context enrichment |
| **Fraud Detection** | "Suspicious connection patterns", "circular transactions" | Pattern-based anomaly detection |
| **Network/IT Management** | "Impact analysis", "dependency chains" | Infrastructure relationship mapping |
| **Access Control** | "Who can access what and why", "permission inheritance" | ReBAC (relationship-based access) |

---

## Strategic Positioning

### When to Choose Graph Over Relational

```
┌─────────────────────────────────────────────────────────────┐
│              Graph vs. Relational Decision Tree              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  DATA CHARACTERISTICS?                                       │
│  ├── FIXED SCHEMA, KNOWN RELATIONSHIPS                       │
│  │   └─ Relational Database (PostgreSQL)                    │
│  │       └─ Use when: Joins are shallow (2-3 tables max)    │
│  │                                                          │
│  ├── DEEP RELATIONSHIP TRAVERSALS (4+ hops)                 │
│  │   └─ Graph Database                                      │
│  │       └─ Example: "Friends of friends of friends"        │
│  │                                                          │
│  ├── VARIABLE/EVOLVING RELATIONSHIPS                         │
│  │   └─ Graph Database                                      │
│  │       └─ Schema changes don't break existing queries     │
│  │                                                          │
│  ├── PATH FINDING / SHORTEST ROUTE                          │
│  │   └─ Graph Database                                      │
│  │       └─ Dijkstra, A*, breadth-first search built-in    │
│  │                                                          │
│  └── ALREADY ON POSTGRESQL + SIMPLE GRAPHS                   │
│      └─ Apache AGE (PostgreSQL extension)                   │
│          └─ Add graph queries to existing relational data   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Integration with Other Skills

| Frontend Skill | Integration Point | Use Case |
|----------------|------------------|----------|
| **search-filter** | Relationship-based queries | "Find all users within 3 degrees of connection" |
| **ai-chat** | Knowledge graph RAG | Context-aware retrieval using semantic relationships |
| **data-viz** | Graph visualization | Network diagrams, relationship maps |
| **dashboards** | Connected data analytics | Influence metrics, centrality scores |

| Backend Skill | Integration Point | Use Case |
|---------------|------------------|----------|
| **databases-vector** | Hybrid graph + vector | Semantic similarity + relationship traversal |
| **auth-security** | ReBAC (relationship-based access) | "Can user X access resource Y through relation Z?" |
| **api-patterns** | Graph API endpoints | GraphQL native support, RESTful graph queries |
| **observability** | Query performance monitoring | Track traversal depths, cache hit rates |

---

## Component Taxonomy

### Tier 1: Database Engines

| Database | Query Language | Open Source | Best For | Cloud Managed |
|----------|---------------|-------------|----------|---------------|
| **Neo4j** | Cypher | Community Edition | General-purpose, mature ecosystem | Neo4j Aura |
| **ArangoDB** | AQL | Yes (Apache 2.0) | Multi-model (document + graph) | ArangoDB Oasis |
| **Amazon Neptune** | Gremlin/SPARQL | No | AWS-native, serverless | AWS (only) |
| **Memgraph** | Cypher | Yes (BSL 1.1) | Real-time, in-memory, streaming | Memgraph Cloud |
| **Apache AGE** | Cypher (via PostgreSQL) | Yes (Apache 2.0) | Extend existing PostgreSQL | Self-hosted |
| **JanusGraph** | Gremlin | Yes (Apache 2.0) | Billion-scale, distributed | Self-hosted |
| **Dgraph** | GraphQL± | Yes (Apache 2.0) | GraphQL-native | Dgraph Cloud |

### Tier 2: Query Languages

#### Cypher (Neo4j, Memgraph, Apache AGE)
```cypher
// Find friends of friends who like the same movies
MATCH (user:Person {name: 'Alice'})-[:FRIEND]->(friend)-[:FRIEND]->(fof)
MATCH (user)-[:LIKES]->(movie)<-[:LIKES]-(fof)
WHERE user <> fof
RETURN DISTINCT fof.name, collect(movie.title) AS common_movies
ORDER BY size(common_movies) DESC
LIMIT 10
```

**Strengths**:
- Most readable, SQL-like syntax
- Pattern matching with ASCII art: `(a)-[:RELATES_TO]->(b)`
- Largest community (2M+ developers)
- Best tooling (Neo4j Browser, Bloom visualization)

#### Gremlin (Apache TinkerPop)
```groovy
// Same query in Gremlin
g.V().has('name', 'Alice')
  .out('FRIEND').out('FRIEND').dedup()
  .where(out('LIKES').in('LIKES').has('name', 'Alice'))
  .project('name', 'common_movies')
    .by('name')
    .by(out('LIKES').values('title').fold())
  .order().by(select('common_movies').count(), desc)
  .limit(10)
```

**Strengths**:
- Language-agnostic (Java, Python, JavaScript drivers)
- Functional programming style
- Cross-database standard (JanusGraph, Neptune, CosmosDB)

#### AQL (ArangoDB Query Language)
```aql
// Multi-model query combining documents and graphs
FOR user IN users
  FILTER user.name == 'Alice'
  FOR friend IN 2..2 OUTBOUND user GRAPH 'social'
    FOR movie IN movies
      FILTER movie._id IN user.liked_movies
        AND movie._id IN friend.liked_movies
      COLLECT friendName = friend.name, movieTitle = movie.title
      RETURN {friend: friendName, movies: movieTitle}
```

**Strengths**:
- Combines document and graph queries
- SQL-like readability
- Unified query across data models

#### SPARQL (RDF/Semantic Web)
```sparql
# Query RDF triples for semantic web data
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX movie: <http://example.org/movie#>

SELECT ?fofName (GROUP_CONCAT(?movieTitle; separator=", ") AS ?commonMovies)
WHERE {
  ?alice foaf:name "Alice" .
  ?alice foaf:knows ?friend .
  ?friend foaf:knows ?fof .
  ?alice movie:likes ?movie .
  ?fof movie:likes ?movie .
  ?fof foaf:name ?fofName .
  ?movie movie:title ?movieTitle .
  FILTER (?alice != ?fof)
}
GROUP BY ?fofName
ORDER BY DESC(COUNT(?movie))
LIMIT 10
```

**Strengths**:
- W3C standard for semantic web
- RDF triple stores (subject-predicate-object)
- Ontology reasoning support
- Best for: Knowledge graphs, linked open data

### Tier 3: Graph Data Modeling Patterns

#### Property Graph Model (Most Common)

```
┌─────────────────────────────────────────────────────────────┐
│                    Property Graph Model                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  NODES (Vertices)                                            │
│  ┌────────────────────┐                                      │
│  │ Person             │                                      │
│  │ ────────────────── │                                      │
│  │ id: "u123"         │                                      │
│  │ name: "Alice"      │                                      │
│  │ age: 28            │                                      │
│  │ labels: ["Person"] │                                      │
│  └────────────────────┘                                      │
│                                                              │
│  RELATIONSHIPS (Edges)                                       │
│  ┌────────────────────────────────┐                         │
│  │ FRIEND                         │                         │
│  │ ────────────────────────────── │                         │
│  │ since: "2020-01-15"            │                         │
│  │ strength: 0.85                 │                         │
│  │ type: "FRIEND"                 │                         │
│  └────────────────────────────────┘                         │
│                                                              │
│  (Person)-[:FRIEND {since: "2020-01-15"}]->(Person)         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Used by**: Neo4j, Memgraph, ArangoDB, Apache AGE

#### RDF Triple Model (Semantic Web)

```
┌─────────────────────────────────────────────────────────────┐
│                       RDF Triple Model                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  TRIPLE: (Subject, Predicate, Object)                        │
│                                                              │
│  <http://example.org/alice>                                  │
│    foaf:knows                                                │
│    <http://example.org/bob> .                                │
│                                                              │
│  <http://example.org/alice>                                  │
│    foaf:name                                                 │
│    "Alice"^^xsd:string .                                     │
│                                                              │
│  Every statement is a (Subject → Predicate → Object)         │
│  Enables reasoning: If A knows B and B knows C,              │
│                     then A indirectly knows C                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Used by**: Amazon Neptune (SPARQL mode), Apache Jena, Blazegraph

---

## Database Comparison Table

| Feature | Neo4j | ArangoDB | Amazon Neptune | Memgraph | Apache AGE |
|---------|-------|----------|----------------|----------|------------|
| **Query Language** | Cypher | AQL | Gremlin/SPARQL | Cypher | Cypher (via SQL) |
| **Open Source** | Community edition | Yes (Apache 2.0) | No | Yes (BSL 1.1) | Yes (Apache 2.0) |
| **Multi-Model** | Graph only | Doc + Graph + K/V | Graph only | Graph only | Graph + Relational |
| **Performance** | Excellent | Very good | Good | Excellent (in-memory) | Good (PostgreSQL) |
| **Scalability** | Horizontal sharding | Cluster sharding | Fully managed, auto-scale | Cluster | PostgreSQL scaling |
| **ACID Transactions** | Yes | Yes | Yes | Yes | Yes (PostgreSQL) |
| **Best Use Case** | General graph | Multi-model apps | AWS-native | Real-time streaming | Extend PostgreSQL |
| **Managed Service** | Neo4j Aura | ArangoDB Oasis | AWS (only) | Memgraph Cloud | None |
| **Graph Algorithms** | 65+ built-in (GDS) | Limited | Limited | Built-in (MAGE) | Limited |
| **Developer Tooling** | Excellent (Browser, Bloom) | Good (Web UI) | AWS Console | Good (Lab) | pgAdmin |
| **Learning Curve** | Low (Cypher) | Medium (AQL) | Medium-High (Gremlin) | Low (Cypher) | Low (SQL + Cypher) |

---

## Decision Framework

```
┌─────────────────────────────────────────────────────────────┐
│              Graph Database Selection Tree                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PRIMARY REQUIREMENT?                                        │
│                                                              │
│  ├── ALREADY ON POSTGRESQL                                   │
│  │   └─ Apache AGE                                          │
│  │       • Add graph extension to existing PostgreSQL       │
│  │       • Query both relational and graph data             │
│  │       • Use when: Simple graphs, no new infrastructure   │
│  │                                                          │
│  ├── GENERAL-PURPOSE GRAPH / PRODUCTION                      │
│  │   └─ Neo4j                                                │
│  │       • Most mature (2007), largest community            │
│  │       • 65+ graph algorithms (GDS library)               │
│  │       • Best tooling (Neo4j Browser, Bloom viz)          │
│  │       • Use when: Need battle-tested, enterprise support │
│  │                                                          │
│  ├── MULTI-MODEL (DOCUMENT + GRAPH)                         │
│  │   └─ ArangoDB                                             │
│  │       • Store documents AND graph in one database        │
│  │       • AQL combines document and graph queries          │
│  │       • Use when: Schema flexibility + relationships     │
│  │                                                          │
│  ├── AWS-NATIVE / SERVERLESS                                │
│  │   └─ Amazon Neptune                                       │
│  │       • Fully managed, auto-scaling                      │
│  │       • Supports Gremlin AND SPARQL                      │
│  │       • Use when: AWS ecosystem, zero ops               │
│  │                                                          │
│  ├── REAL-TIME / HIGH-THROUGHPUT STREAMING                  │
│  │   └─ Memgraph                                             │
│  │       • In-memory, millisecond latency                   │
│  │       • Kafka streaming integration                      │
│  │       • Use when: Real-time fraud detection, IoT         │
│  │                                                          │
│  ├── SEMANTIC WEB / RDF / ONTOLOGIES                        │
│  │   └─ Amazon Neptune (SPARQL mode)                        │
│  │       • W3C standard RDF triples                         │
│  │       • Reasoning engines                                │
│  │       • Use when: Knowledge graphs, linked open data     │
│  │                                                          │
│  └── BILLION-SCALE / DISTRIBUTED                             │
│      └─ JanusGraph                                            │
│          • Cassandra/HBase backend                           │
│          • Horizontal scaling to billions of edges           │
│          • Use when: Google/Facebook-scale graphs            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Cypher Query Patterns Section

### Common Patterns (Neo4j/Memgraph/AGE)

#### 1. Basic Pattern Matching
```cypher
// Find all users who work at a specific company
MATCH (u:User)-[:WORKS_AT]->(c:Company {name: 'Acme Corp'})
RETURN u.name, u.title

// Find users and their managers
MATCH (u:User)-[:REPORTS_TO]->(m:User)
RETURN u.name AS employee, m.name AS manager
```

#### 2. Variable-Length Paths
```cypher
// Find all reports up to 3 levels deep
MATCH (u:User {name: 'Alice'})-[:REPORTS_TO*1..3]->(manager)
RETURN manager.name, length(path) AS levels

// Find shortest path between two users
MATCH path = shortestPath(
  (u1:User {name: 'Alice'})-[*]-(u2:User {name: 'Bob'})
)
RETURN path, length(path) AS distance
```

#### 3. Traversals with Filters
```cypher
// Find friends who like similar content
MATCH (u:User {id: $userId})-[:FRIEND]->(friend)
WHERE friend.age >= 25 AND friend.age <= 35
  AND exists((friend)-[:LIKES]->(:Movie {genre: 'Sci-Fi'}))
RETURN friend.name, friend.age
ORDER BY friend.lastActive DESC
LIMIT 20
```

#### 4. Aggregations
```cypher
// Count mutual friends
MATCH (u1:User {name: 'Alice'})-[:FRIEND]->(mutual)<-[:FRIEND]-(u2:User {name: 'Bob'})
RETURN count(mutual) AS mutualFriends

// Find most influential users (by connection count)
MATCH (u:User)-[r:FRIEND]->()
RETURN u.name, count(r) AS connections
ORDER BY connections DESC
LIMIT 10
```

#### 5. Graph Algorithms (Neo4j GDS)
```cypher
// PageRank (find influential nodes)
CALL gds.pageRank.stream('socialGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC
LIMIT 10

// Community Detection (Louvain)
CALL gds.louvain.stream('socialGraph')
YIELD nodeId, communityId
RETURN gds.util.asNode(nodeId).name AS name, communityId
ORDER BY communityId

// Shortest Path (Dijkstra)
MATCH (source:Location {name: 'New York'}), (target:Location {name: 'Los Angeles'})
CALL gds.shortestPath.dijkstra.stream('roadNetwork', {
  sourceNode: source,
  targetNode: target,
  relationshipWeightProperty: 'distance'
})
YIELD path, totalCost
RETURN path, totalCost
```

#### 6. Write Operations
```cypher
// Create nodes and relationships
CREATE (u:User {id: 'u123', name: 'Alice', email: 'alice@example.com'})
CREATE (c:Company {id: 'c456', name: 'Acme Corp'})
CREATE (u)-[:WORKS_AT {since: date('2020-01-15'), role: 'Engineer'}]->(c)

// Update properties
MATCH (u:User {id: 'u123'})
SET u.lastLogin = datetime()

// Merge (upsert)
MERGE (u:User {email: 'alice@example.com'})
ON CREATE SET u.created = datetime()
ON MATCH SET u.updated = datetime()
```

#### 7. Recommendations
```cypher
// Collaborative filtering: Find products liked by similar users
MATCH (u:User {id: $userId})-[:PURCHASED]->(p:Product)<-[:PURCHASED]-(similar:User)
MATCH (similar)-[:PURCHASED]->(recommendation:Product)
WHERE NOT exists((u)-[:PURCHASED]->(recommendation))
RETURN recommendation.name, count(*) AS score
ORDER BY score DESC
LIMIT 10

// Content-based: Products similar to what user already likes
MATCH (u:User {id: $userId})-[:PURCHASED]->(p:Product)-[:IN_CATEGORY]->(c:Category)
MATCH (c)<-[:IN_CATEGORY]-(rec:Product)
WHERE NOT exists((u)-[:PURCHASED]->(rec))
RETURN rec.name, count(c) AS categoryOverlap
ORDER BY categoryOverlap DESC
LIMIT 10
```

---

## Use Case Examples

### 1. Social Network Graph

#### Schema Design
```cypher
// Nodes
(:Person {id, name, email, joined_date})
(:Post {id, content, created_at})
(:Comment {id, text, created_at})

// Relationships
(:Person)-[:FRIEND {since}]->(:Person)
(:Person)-[:FOLLOWS]->(:Person)
(:Person)-[:POSTED]->(:Post)
(:Person)-[:COMMENTED]->(:Comment)
(:Comment)-[:REPLY_TO]->(:Post)
(:Comment)-[:REPLY_TO]->(:Comment)
(:Person)-[:LIKES]->(:Post)
(:Person)-[:LIKES]->(:Comment)
```

#### Key Queries
```cypher
// News feed: Posts from friends and followed users
MATCH (u:Person {id: $userId})-[:FRIEND|FOLLOWS]->(author)-[:POSTED]->(post)
OPTIONAL MATCH (post)<-[:LIKES]-(liker)
RETURN post, author, count(liker) AS likes
ORDER BY post.created_at DESC
LIMIT 50

// Friend suggestions (friends of friends)
MATCH (u:Person {id: $userId})-[:FRIEND]->()-[:FRIEND]->(suggestion)
WHERE NOT exists((u)-[:FRIEND]->(suggestion)) AND u <> suggestion
RETURN suggestion.name, count(*) AS mutualFriends
ORDER BY mutualFriends DESC
LIMIT 10
```

### 2. Knowledge Graph for AI/RAG

#### Schema Design
```cypher
// Nodes
(:Concept {id, name, description, embedding[]})
(:Document {id, title, url})
(:Entity {id, name, type})  // person, org, location

// Relationships
(:Concept)-[:RELATED_TO {strength}]->(:Concept)
(:Concept)-[:IS_A]->(:Concept)  // Hierarchical
(:Concept)-[:HAS_PROPERTY]->(:Concept)
(:Document)-[:MENTIONS]->(:Concept)
(:Document)-[:MENTIONS]->(:Entity)
(:Entity)-[:WORKS_AT]->(:Entity)
(:Entity)-[:LOCATED_IN]->(:Entity)
```

#### Integration with Vector Database
```cypher
// Hybrid search: Vector similarity + graph context
// Step 1: Vector search (in Qdrant/pgvector) returns concept IDs
// Step 2: Expand with graph context
MATCH (c:Concept) WHERE c.id IN $vector_search_results
MATCH path = (c)-[:RELATED_TO|IS_A*1..2]-(related:Concept)
RETURN c, related, relationships(path)
ORDER BY length(path)

// Find all documents that mention related concepts
MATCH (c:Concept {id: $conceptId})-[:RELATED_TO*1..2]-(related)
MATCH (doc:Document)-[:MENTIONS]->(related)
RETURN doc.title, doc.url, collect(related.name) AS mentioned_concepts
```

### 3. Recommendation Engine

#### Schema Design
```cypher
// Nodes
(:User {id, age, location})
(:Product {id, name, category, price})
(:Category {id, name})

// Relationships
(:User)-[:PURCHASED {date, rating}]->(:Product)
(:User)-[:VIEWED {timestamp}]->(:Product)
(:User)-[:ADDED_TO_CART {timestamp}]->(:Product)
(:Product)-[:IN_CATEGORY]->(:Category)
(:Product)-[:SIMILAR_TO {score}]->(:Product)
```

#### Recommendation Strategies
```cypher
// 1. Collaborative filtering
MATCH (u:User {id: $userId})-[r1:PURCHASED]->(p:Product)<-[r2:PURCHASED]-(similar:User)
WHERE r1.rating >= 4 AND r2.rating >= 4
WITH similar, count(p) AS commonProducts
ORDER BY commonProducts DESC
LIMIT 100
MATCH (similar)-[r:PURCHASED]->(rec:Product)
WHERE NOT exists((u)-[:PURCHASED]->(rec)) AND r.rating >= 4
RETURN rec.name, avg(r.rating) AS avgRating, count(*) AS purchaseCount
ORDER BY purchaseCount DESC, avgRating DESC
LIMIT 10

// 2. Content-based filtering
MATCH (u:User {id: $userId})-[r:PURCHASED]->(p:Product)-[:IN_CATEGORY]->(c:Category)
WHERE r.rating >= 4
WITH c, count(p) AS categoryScore
MATCH (c)<-[:IN_CATEGORY]-(rec:Product)
WHERE NOT exists((u)-[:PURCHASED]->(rec))
RETURN rec.name, sum(categoryScore) AS score
ORDER BY score DESC
LIMIT 10

// 3. Session-based (recently viewed)
MATCH (u:User {id: $userId})-[v:VIEWED]->(p:Product)-[:SIMILAR_TO]->(rec)
WHERE v.timestamp > datetime() - duration('P7D')
  AND NOT exists((u)-[:PURCHASED]->(rec))
RETURN rec.name, count(*) AS relevance
ORDER BY relevance DESC
LIMIT 10
```

### 4. Fraud Detection Network

#### Schema Design
```cypher
// Nodes
(:Account {id, created_at, status})
(:Transaction {id, amount, timestamp})
(:Device {id, fingerprint, ip_address})
(:Email {address})
(:PhoneNumber {number})

// Relationships
(:Account)-[:OWNS]->(:Email)
(:Account)-[:OWNS]->(:PhoneNumber)
(:Account)-[:SENT {amount}]->(:Transaction)
(:Account)-[:RECEIVED]->(:Transaction)
(:Transaction)-[:FROM_DEVICE]->(:Device)
```

#### Fraud Detection Patterns
```cypher
// Circular money flow detection
MATCH path = (a:Account)-[:SENT*3..6]->(a)
WHERE all(r IN relationships(path) WHERE r.amount > 1000)
RETURN path, [r IN relationships(path) | r.amount] AS amounts

// Shared device across multiple accounts (suspicious)
MATCH (d:Device)<-[:FROM_DEVICE]-(:Transaction)<-[:SENT]-(a:Account)
WITH d, count(DISTINCT a) AS accountCount
WHERE accountCount > 5
MATCH (d)<-[:FROM_DEVICE]-(:Transaction)<-[:SENT]-(account)
RETURN d.fingerprint, collect(account.id) AS suspicious_accounts

// Rapid transaction chains
MATCH (a1:Account)-[:SENT]->(t1:Transaction)-[:RECEIVED]->(a2:Account)
     -[:SENT]->(t2:Transaction)-[:RECEIVED]->(a3:Account)
WHERE t2.timestamp - t1.timestamp < duration('PT5M')
  AND t1.amount > 5000 AND t2.amount > 5000
RETURN a1.id, a2.id, a3.id, t1.amount, t2.amount
```

---

## Frontend Integration

### Connection to search-filter Skill

Graph databases excel at relationship-based queries that extend traditional search:

```typescript
// Frontend: Relationship-aware search component
interface GraphSearchProps {
  searchType: 'direct' | 'friends-of-friends' | 'shortest-path' | 'community'
  maxDepth?: number
}

// Backend: FastAPI endpoint
from fastapi import APIRouter, Query
from neo4j import GraphDatabase

router = APIRouter()

@router.get("/search/graph")
async def graph_search(
    user_id: str,
    search_type: str = Query(..., regex="^(direct|fof|path|community)$"),
    max_depth: int = Query(3, ge=1, le=5)
):
    """
    Relationship-based search using graph traversals.

    - direct: First-degree connections
    - fof: Friends of friends (variable depth)
    - path: Shortest path between entities
    - community: All nodes in same community cluster
    """
    if search_type == "fof":
        query = """
        MATCH (u:User {id: $userId})-[:FRIEND*1..$maxDepth]->(connection)
        RETURN DISTINCT connection.name, connection.id
        LIMIT 100
        """
    # ... other query types

    with driver.session() as session:
        result = session.run(query, userId=user_id, maxDepth=max_depth)
        return [dict(record) for record in result]
```

### Graph Visualization Integration

```typescript
// Use with data-viz skill for network diagrams
import { ForceGraph2D } from 'react-force-graph'

interface GraphNode {
  id: string
  name: string
  type: string  // 'Person', 'Company', etc.
}

interface GraphLink {
  source: string
  target: string
  relationship: string
  strength?: number
}

function SocialNetworkVisualization({ data }: { data: { nodes: GraphNode[], links: GraphLink[] }}) {
  return (
    <ForceGraph2D
      graphData={data}
      nodeLabel="name"
      nodeColor={node => node.type === 'Person' ? '#FA582D' : '#3B82F6'}
      linkLabel="relationship"
      linkWidth={link => Math.sqrt(link.strength || 1)}
    />
  )
}
```

---

## Graph Data Modeling Best Practices

### 1. Node vs. Relationship Properties

**Anti-pattern**: Storing relationship data in nodes
```cypher
// BAD: Relationship data in node properties
(:Person {name: 'Alice', friend_ids: ['b123', 'c456']})

// GOOD: Explicit relationships
(:Person {name: 'Alice'})-[:FRIEND]->(:Person {id: 'b123'})
(:Person {name: 'Alice'})-[:FRIEND]->(:Person {id: 'c456'})
```

**Pattern**: Use relationship properties for metadata
```cypher
// Relationship properties track interaction details
(:Person)-[:FRIEND {since: '2020-01-15', strength: 0.85, last_interaction: datetime()}]->(:Person)
```

### 2. Bidirectional vs. Unidirectional Relationships

```cypher
// Symmetric relationships (bidirectional): Create once, query both directions
CREATE (a:Person {name: 'Alice'})-[:FRIEND]->(b:Person {name: 'Bob'})

// Query works in both directions with undirected pattern
MATCH (a:Person {name: 'Alice'})-[:FRIEND]-(friend)  // No arrow direction
RETURN friend.name

// Asymmetric relationships: Create both if truly bidirectional
CREATE (a)-[:FOLLOWS]->(b)
CREATE (b)-[:FOLLOWS]->(a)  // Mutual follows
```

### 3. Multi-Hop Performance Optimization

```cypher
// SLOW: Unbounded traversal
MATCH (a:Person {name: 'Alice'})-[:FRIEND*]->(distant)
RETURN distant

// FAST: Bounded depth + index
MATCH (a:Person {name: 'Alice'})-[:FRIEND*1..4]->(distant)
WHERE distant.active = true
RETURN distant
LIMIT 100

// Create index for better performance
CREATE INDEX person_active FOR (p:Person) ON (p.active)
```

### 4. Avoiding Supernodes (High-Degree Nodes)

**Problem**: Nodes with thousands of relationships slow traversals.

**Solution**: Intermediate aggregation nodes
```cypher
// BAD: User connected to 1M+ posts directly
(:User)-[:POSTED]->(:Post)  // 1M relationships

// GOOD: Partition by time
(:User)-[:POSTED_IN]->(:Year {year: 2025})
       -[:HAS_MONTH]->(:Month {month: 12})
       -[:HAS_POST]->(:Post)
```

### 5. Schema Design Patterns

#### Star Schema (Hub and Spokes)
```cypher
// Central entity with many connections
(:User)-[:PURCHASED]->(:Product)
(:User)-[:VIEWED]->(:Product)
(:User)-[:RATED]->(:Product)
(:User)-[:REVIEWED]->(:Product)
```

#### Hierarchical Schema (Trees)
```cypher
// Organizational structure
(:CEO)-[:MANAGES]->(:VP)-[:MANAGES]->(:Director)-[:MANAGES]->(:Manager)-[:MANAGES]->(:Employee)

// Category taxonomy
(:RootCategory)-[:HAS_SUBCATEGORY]->(:Category)-[:HAS_SUBCATEGORY]->(:Subcategory)
```

#### Temporal Schema (Time-based)
```cypher
// Event sequences
(:Event {timestamp})-[:NEXT]->(:Event {timestamp})-[:NEXT]->(:Event)

// Version history
(:DocumentV1)-[:REVISED_TO]->(:DocumentV2)-[:REVISED_TO]->(:DocumentV3)
```

---

## Performance and Scaling

### Indexing Strategies

```cypher
// Single-property index
CREATE INDEX user_email FOR (u:User) ON (u.email)

// Composite index (Neo4j 5.x+)
CREATE INDEX user_name_location FOR (u:User) ON (u.name, u.location)

// Full-text search index
CREATE FULLTEXT INDEX product_search FOR (p:Product) ON EACH [p.name, p.description]

// Query full-text index
CALL db.index.fulltext.queryNodes('product_search', 'laptop ~2') YIELD node, score
RETURN node.name, score
```

### Caching and Materialized Paths

```cypher
// Cache expensive aggregations
// Instead of computing on every query:
MATCH (u:User)-[:FRIEND]->(f)
WITH u, count(f) AS friendCount  // Computed every time

// Materialize as property:
MATCH (u:User)-[:FRIEND]->(f)
WITH u, count(f) AS friendCount
SET u.friend_count = friendCount

// Then query is instant:
MATCH (u:User) WHERE u.friend_count > 100
RETURN u.name, u.friend_count
```

### Scaling Strategies

| Scale | Strategy | Implementation |
|-------|----------|----------------|
| **Vertical** | Add RAM, CPU | In-memory caching, larger instances |
| **Horizontal (Read)** | Read replicas | Neo4j Cluster, ArangoDB Cluster |
| **Horizontal (Write)** | Sharding | ArangoDB SmartGraphs, JanusGraph |
| **Caching** | Application-level cache | Redis for hot paths, query result caching |
| **Archival** | Cold storage | Move old data to relational DB, keep recent in graph |

---

## Language Integration Examples

### Python (Neo4j)
```python
from neo4j import GraphDatabase
from typing import List, Dict

class Neo4jConnector:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def find_friends_of_friends(self, user_id: str, max_depth: int = 2) -> List[Dict]:
        """Find friends of friends up to max_depth."""
        query = """
        MATCH (u:User {id: $userId})-[:FRIEND*1..$maxDepth]->(fof)
        WHERE u <> fof
        RETURN DISTINCT fof.id AS id, fof.name AS name
        LIMIT 100
        """
        with self.driver.session() as session:
            result = session.run(query, userId=user_id, maxDepth=max_depth)
            return [dict(record) for record in result]

    def create_friendship(self, user1_id: str, user2_id: str):
        """Create bidirectional friendship."""
        query = """
        MATCH (u1:User {id: $user1Id}), (u2:User {id: $user2Id})
        MERGE (u1)-[:FRIEND {since: datetime()}]->(u2)
        MERGE (u2)-[:FRIEND {since: datetime()}]->(u1)
        """
        with self.driver.session() as session:
            session.run(query, user1Id=user1_id, user2Id=user2_id)

# Usage
db = Neo4jConnector("bolt://localhost:7687", "neo4j", "password")
friends = db.find_friends_of_friends("u123", max_depth=3)
db.close()
```

### TypeScript (Neo4j)
```typescript
import neo4j, { Driver, Session } from 'neo4j-driver'

interface User {
  id: string
  name: string
  email: string
}

class Neo4jService {
  private driver: Driver

  constructor(uri: string, username: string, password: string) {
    this.driver = neo4j.driver(uri, neo4j.auth.basic(username, password))
  }

  async close(): Promise<void> {
    await this.driver.close()
  }

  async findFriendsOfFriends(userId: string, maxDepth: number = 2): Promise<User[]> {
    const session: Session = this.driver.session()
    try {
      const result = await session.run(
        `
        MATCH (u:User {id: $userId})-[:FRIEND*1..$maxDepth]->(fof)
        WHERE u <> fof
        RETURN DISTINCT fof.id AS id, fof.name AS name, fof.email AS email
        LIMIT 100
        `,
        { userId, maxDepth }
      )
      return result.records.map(record => ({
        id: record.get('id'),
        name: record.get('name'),
        email: record.get('email'),
      }))
    } finally {
      await session.close()
    }
  }

  async recommendProducts(userId: string, limit: number = 10): Promise<any[]> {
    const session = this.driver.session()
    try {
      const result = await session.run(
        `
        MATCH (u:User {id: $userId})-[:PURCHASED]->(p:Product)<-[:PURCHASED]-(similar)
        MATCH (similar)-[:PURCHASED]->(rec:Product)
        WHERE NOT exists((u)-[:PURCHASED]->(rec))
        RETURN rec.id, rec.name, count(*) AS score
        ORDER BY score DESC
        LIMIT $limit
        `,
        { userId, limit }
      )
      return result.records.map(r => r.toObject())
    } finally {
      await session.close()
    }
  }
}

// Usage
const db = new Neo4jService('bolt://localhost:7687', 'neo4j', 'password')
const friends = await db.findFriendsOfFriends('u123', 3)
await db.close()
```

### Rust (Neo4j via neo4rs)
```rust
use neo4rs::*;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct User {
    id: String,
    name: String,
    email: String,
}

async fn find_friends_of_friends(
    graph: &Graph,
    user_id: &str,
    max_depth: i64,
) -> Result<Vec<User>> {
    let query = query(
        "MATCH (u:User {id: $userId})-[:FRIEND*1..$maxDepth]->(fof)
         WHERE u <> fof
         RETURN DISTINCT fof.id AS id, fof.name AS name, fof.email AS email
         LIMIT 100"
    )
    .param("userId", user_id)
    .param("maxDepth", max_depth);

    let mut result = graph.execute(query).await?;
    let mut users = Vec::new();

    while let Some(row) = result.next().await? {
        let user = User {
            id: row.get("id")?,
            name: row.get("name")?,
            email: row.get("email")?,
        };
        users.push(user);
    }

    Ok(users)
}

#[tokio::main]
async fn main() -> Result<()> {
    let config = ConfigBuilder::default()
        .uri("bolt://localhost:7687")
        .user("neo4j")
        .password("password")
        .build()?;

    let graph = Graph::connect(config).await?;
    let friends = find_friends_of_friends(&graph, "u123", 3).await?;

    println!("Found {} friends of friends", friends.len());
    Ok(())
}
```

---

## Skill Structure

```
databases-graph/
├── init.md                          # This file - master plan
├── SKILL.md                         # Main skill file (< 500 lines)
├── references/
│   ├── neo4j-guide.md               # Neo4j setup, drivers, GDS algorithms
│   ├── arangodb-guide.md            # ArangoDB multi-model patterns
│   ├── amazon-neptune-guide.md      # Neptune (Gremlin + SPARQL)
│   ├── memgraph-guide.md            # Memgraph real-time streaming
│   ├── apache-age-guide.md          # PostgreSQL + AGE extension
│   ├── cypher-reference.md          # Comprehensive Cypher patterns
│   ├── gremlin-reference.md         # Gremlin query language
│   ├── aql-reference.md             # ArangoDB Query Language
│   ├── graph-algorithms.md          # PageRank, Louvain, Dijkstra, etc.
│   ├── data-modeling-patterns.md    # Property graph best practices
│   └── performance-tuning.md        # Indexing, caching, scaling
├── examples/
│   ├── social-network/
│   │   ├── python-neo4j/
│   │   │   ├── main.py
│   │   │   ├── models.py
│   │   │   └── queries.py
│   │   ├── typescript-neo4j/
│   │   │   ├── index.ts
│   │   │   └── neo4j.service.ts
│   │   └── schema.cypher
│   ├── knowledge-graph/
│   │   ├── rag-integration.py       # Hybrid vector + graph
│   │   ├── entity-extraction.py
│   │   └── schema.cypher
│   ├── recommendation-engine/
│   │   ├── collaborative-filtering.cypher
│   │   ├── content-based.cypher
│   │   └── hybrid-recommender.py
│   └── fraud-detection/
│       ├── pattern-detection.cypher
│       ├── risk-scoring.py
│       └── real-time-monitoring.py
├── scripts/
│   ├── validate_schema.py           # Check graph schema consistency
│   ├── benchmark_queries.py         # Performance testing
│   └── migrate_to_graph.py          # Relational → Graph migration helper
└── assets/
    └── diagrams/
        ├── property-graph-model.svg
        └── graph-vs-relational.svg
```

---

## SKILL.md Frontmatter Template

```yaml
---
name: databases-graph
description: Graph database implementation for relationship-heavy data models. Use when building social networks, recommendation engines, knowledge graphs, or fraud detection systems. Covers Neo4j (primary with Cypher and 65+ algorithms), ArangoDB (multi-model document + graph), Amazon Neptune (AWS-native Gremlin/SPARQL), Memgraph (real-time in-memory), Apache AGE (PostgreSQL extension), graph data modeling patterns, Cypher query optimization, and hybrid vector + graph architectures for AI/RAG applications.
---
```

---

## Quality Checklist

### Core Quality
- [ ] Clear scope: Relationship-heavy data models (not general databases)
- [ ] Decision framework includes "when NOT to use graph"
- [ ] Multi-database comparison (not just Neo4j)
- [ ] Multi-language examples (Python, TypeScript, Rust)
- [ ] Real-world use cases with complete schemas
- [ ] Performance considerations and scaling strategies

### Naming and Structure
- [ ] Name: `databases-graph` (gerund implied: "managing graph databases")
- [ ] Description: Under 1024 chars, includes WHAT and WHEN
- [ ] File paths use forward slashes
- [ ] References are one level deep from SKILL.md

### Technical Completeness
- [ ] Cypher pattern library (10+ common queries)
- [ ] Gremlin examples for cross-database compatibility
- [ ] Graph algorithm coverage (PageRank, community detection, shortest path)
- [ ] Integration with databases-vector (hybrid search)
- [ ] Integration with search-filter (relationship queries)
- [ ] Integration with ai-chat (knowledge graph RAG)

### Code and Scripts
- [ ] validate_schema.py checks for anti-patterns (supernodes, unbounded traversals)
- [ ] benchmark_queries.py measures query performance
- [ ] migrate_to_graph.py provides relational → graph migration helpers
- [ ] All scripts have clear error messages
- [ ] Dependencies listed (neo4j-driver, neo4rs, py2neo)

### Examples
- [ ] Complete social network schema with queries
- [ ] Knowledge graph for RAG with vector integration
- [ ] Recommendation engine (collaborative + content-based)
- [ ] Fraud detection patterns
- [ ] Each example includes schema + queries + backend code

### Testing
- [ ] At least 3 evaluations:
  1. Social network friend recommendations
  2. Knowledge graph traversal for RAG
  3. Fraud pattern detection
- [ ] Tested with Neo4j Community Edition
- [ ] Tested with Apache AGE (PostgreSQL extension)
- [ ] Performance benchmarks documented

---

## Integration with Other Backend Skills

### With databases-vector
```python
# Hybrid: Vector similarity + graph context
# Step 1: Vector search in Qdrant
from qdrant_client import QdrantClient

qdrant = QdrantClient("localhost", port=6333)
vector_results = qdrant.search(
    collection_name="concepts",
    query_vector=embedding,
    limit=10
)

# Step 2: Expand with graph relationships in Neo4j
concept_ids = [hit.id for hit in vector_results]
graph_query = """
MATCH (c:Concept) WHERE c.id IN $conceptIds
MATCH (c)-[:RELATED_TO|IS_A*1..2]-(related)
RETURN c, related, relationships(path) AS context
"""
expanded_context = neo4j_session.run(graph_query, conceptIds=concept_ids)
```

### With auth-security (ReBAC)
```cypher
// Relationship-based access control
// Can user access resource through any relationship path?
MATCH path = shortestPath(
  (u:User {id: $userId})-[:MEMBER_OF|OWNS|MANAGES*1..5]-(r:Resource {id: $resourceId})
)
RETURN path IS NOT NULL AS hasAccess, relationships(path) AS accessPath
```

### With api-patterns
```python
# FastAPI with Neo4j
from fastapi import APIRouter, Depends
from neo4j import Driver

router = APIRouter()

async def get_neo4j_driver() -> Driver:
    # Dependency injection
    return neo4j_driver

@router.get("/users/{user_id}/recommendations")
async def get_recommendations(
    user_id: str,
    limit: int = 10,
    driver: Driver = Depends(get_neo4j_driver)
):
    """Collaborative filtering recommendations using graph traversal."""
    query = """
    MATCH (u:User {id: $userId})-[:PURCHASED]->(p:Product)<-[:PURCHASED]-(similar)
    MATCH (similar)-[:PURCHASED]->(rec:Product)
    WHERE NOT exists((u)-[:PURCHASED]->(rec))
    RETURN rec.id, rec.name, count(*) AS score
    ORDER BY score DESC
    LIMIT $limit
    """
    with driver.session() as session:
        result = session.run(query, userId=user_id, limit=limit)
        return [dict(record) for record in result]
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2025-12-02 | Initial master plan created |

---

*Document generated: December 2025*
*Status: Ready for SKILL.md implementation*
*Next steps: Create SKILL.md, references/, examples/, scripts/*
