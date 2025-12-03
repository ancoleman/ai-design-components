# Cypher Query Patterns Reference

Comprehensive collection of common Cypher query patterns for Neo4j, Memgraph, and Apache AGE.

## Pattern Matching Basics

### Simple Pattern Matching

```cypher
// Find all users
MATCH (u:User)
RETURN u

// Find users with specific property
MATCH (u:User {email: 'alice@example.com'})
RETURN u

// Find users with WHERE clause
MATCH (u:User)
WHERE u.age >= 25 AND u.city = 'San Francisco'
RETURN u.name, u.age
```

### Relationship Patterns

```cypher
// Outgoing relationship
MATCH (u:User)-[:FRIEND]->(friend)
WHERE u.name = 'Alice'
RETURN friend.name

// Incoming relationship
MATCH (u:User)<-[:FRIEND]-(friend)
WHERE u.name = 'Alice'
RETURN friend.name

// Bidirectional (undirected)
MATCH (u:User)-[:FRIEND]-(friend)
WHERE u.name = 'Alice'
RETURN friend.name

// Multiple relationships
MATCH (u:User)-[:FRIEND]->(f)-[:WORKS_AT]->(c:Company)
WHERE u.name = 'Alice'
RETURN f.name, c.name
```

### Relationship Properties

```cypher
// Filter by relationship property
MATCH (u:User)-[r:FRIEND]->(friend)
WHERE u.name = 'Alice' AND r.since >= date('2020-01-01')
RETURN friend.name, r.since

// Return relationship properties
MATCH (u:User)-[r:FRIEND]->(friend)
WHERE u.name = 'Alice'
RETURN friend.name, r.since, r.strength
```

## Variable-Length Paths

### Fixed-Depth Traversal

```cypher
// Friends of friends (exactly 2 hops)
MATCH (u:User {name: 'Alice'})-[:FRIEND*2]->(fof)
RETURN DISTINCT fof.name

// Up to 3 hops
MATCH (u:User {name: 'Alice'})-[:FRIEND*1..3]->(connection)
RETURN DISTINCT connection.name, length(path) AS depth
LIMIT 100
```

### Variable-Depth Traversal

```cypher
// Find all connections (bounded to prevent runaway queries)
MATCH path = (u:User {name: 'Alice'})-[:FRIEND*1..5]->(connection)
WHERE u <> connection
RETURN connection.name, length(path) AS degrees_of_separation
ORDER BY degrees_of_separation
LIMIT 100

// Traverse with relationship type variations
MATCH (u:User {name: 'Alice'})-[:FRIEND|COLLEAGUE*1..3]->(connection)
RETURN DISTINCT connection.name
```

## Path Finding

### Shortest Path

```cypher
// Single shortest path
MATCH path = shortestPath(
  (a:User {name: 'Alice'})-[*]-(b:User {name: 'Bob'})
)
RETURN path, length(path) AS distance

// Shortest path with relationship filter
MATCH path = shortestPath(
  (a:User {name: 'Alice'})-[:FRIEND*]-(b:User {name: 'Bob'})
)
RETURN [node IN nodes(path) | node.name] AS route, length(path)
```

### All Shortest Paths

```cypher
// Find all paths with minimum length
MATCH path = allShortestPaths(
  (a:User {name: 'Alice'})-[*]-(b:User {name: 'Bob'})
)
RETURN path
```

### Weighted Shortest Path (with GDS)

```cypher
// Using Graph Data Science library
MATCH (source:Location {name: 'New York'}), (target:Location {name: 'Los Angeles'})
CALL gds.shortestPath.dijkstra.stream('roadNetwork', {
  sourceNode: source,
  targetNode: target,
  relationshipWeightProperty: 'distance'
})
YIELD path, totalCost
RETURN
  [node IN nodes(path) | node.name] AS route,
  totalCost AS distance
```

## Aggregations

### Count and Group

```cypher
// Count relationships
MATCH (u:User)-[r:FRIEND]->()
RETURN u.name, count(r) AS friend_count
ORDER BY friend_count DESC

// Group by property
MATCH (u:User)-[:WORKS_AT]->(c:Company)
RETURN c.name AS company, count(u) AS employee_count
ORDER BY employee_count DESC

// Multiple aggregations
MATCH (u:User)-[:PURCHASED]->(p:Product)
RETURN
  u.name,
  count(p) AS total_purchases,
  count(DISTINCT p.category) AS categories_purchased,
  avg(p.price) AS avg_price,
  sum(p.price) AS total_spent
```

### Collect and Unwind

```cypher
// Collect related items
MATCH (u:User {name: 'Alice'})-[:FRIEND]->(friend)
RETURN u.name, collect(friend.name) AS friends

// Collect with properties
MATCH (u:User {name: 'Alice'})-[r:FRIEND]->(friend)
RETURN u.name, collect({name: friend.name, since: r.since}) AS friends

// Unwind list to rows
UNWIND ['Alice', 'Bob', 'Charlie'] AS name
MATCH (u:User {name: name})
RETURN u
```

## Filtering

### WHERE Clauses

```cypher
// Multiple conditions
MATCH (u:User)-[:FRIEND]->(friend)
WHERE u.name = 'Alice'
  AND friend.age >= 25
  AND friend.age <= 35
  AND friend.city = 'San Francisco'
RETURN friend.name, friend.age

// String matching
MATCH (u:User)
WHERE u.email ENDS WITH '@example.com'
  AND u.name STARTS WITH 'A'
RETURN u.name, u.email

// Regular expressions
MATCH (u:User)
WHERE u.email =~ '.*@(gmail|yahoo)\\.com'
RETURN u.email

// IN operator
MATCH (u:User)
WHERE u.city IN ['San Francisco', 'New York', 'Boston']
RETURN u.name, u.city
```

### EXISTS and NOT EXISTS

```cypher
// Users who have purchased something
MATCH (u:User)
WHERE exists((u)-[:PURCHASED]->(:Product))
RETURN u.name

// Users who have NOT purchased anything
MATCH (u:User)
WHERE NOT exists((u)-[:PURCHASED]->(:Product))
RETURN u.name

// Complex existence check
MATCH (u:User)
WHERE exists {
  MATCH (u)-[:FRIEND]->(f:User)-[:WORKS_AT]->(:Company {name: 'Google'})
}
RETURN u.name
```

## Write Operations

### Create Nodes

```cypher
// Create single node
CREATE (u:User {id: 'u123', name: 'Alice', email: 'alice@example.com'})
RETURN u

// Create multiple nodes
CREATE
  (u1:User {id: 'u1', name: 'Alice'}),
  (u2:User {id: 'u2', name: 'Bob'}),
  (c:Company {id: 'c1', name: 'Acme Corp'})

// Create with timestamp
CREATE (u:User {
  id: 'u123',
  name: 'Alice',
  created_at: datetime(),
  updated_at: datetime()
})
```

### Create Relationships

```cypher
// Create relationship between existing nodes
MATCH (u1:User {id: 'u1'}), (u2:User {id: 'u2'})
CREATE (u1)-[:FRIEND {since: date('2020-01-15')}]->(u2)

// Create nodes and relationships together
CREATE (u:User {name: 'Alice'})-[:WORKS_AT {since: date('2020-01-01')}]->(c:Company {name: 'Acme'})

// Bidirectional friendship
MATCH (u1:User {id: 'u1'}), (u2:User {id: 'u2'})
CREATE (u1)-[:FRIEND {since: datetime()}]->(u2),
       (u2)-[:FRIEND {since: datetime()}]->(u1)
```

### MERGE (Upsert)

```cypher
// Create or match node
MERGE (u:User {email: 'alice@example.com'})
ON CREATE SET u.created = datetime(), u.name = 'Alice'
ON MATCH SET u.updated = datetime()
RETURN u

// Create unique relationships
MATCH (u1:User {id: 'u1'}), (u2:User {id: 'u2'})
MERGE (u1)-[r:FRIEND]-(u2)
ON CREATE SET r.since = datetime()
RETURN r

// Merge with complex logic
MERGE (u:User {email: $email})
ON CREATE SET
  u.id = randomUUID(),
  u.name = $name,
  u.created_at = datetime()
ON MATCH SET
  u.last_login = datetime()
RETURN u
```

### Update Properties

```cypher
// SET to update/add properties
MATCH (u:User {id: 'u123'})
SET u.age = 29, u.updated_at = datetime()
RETURN u

// SET all properties from map
MATCH (u:User {id: 'u123'})
SET u = {id: 'u123', name: 'Alice Smith', age: 29}

// SET += to add properties without removing existing
MATCH (u:User {id: 'u123'})
SET u += {age: 29, city: 'San Francisco'}

// REMOVE property
MATCH (u:User {id: 'u123'})
REMOVE u.temporary_field
```

### Delete

```cypher
// Delete node (must delete relationships first)
MATCH (u:User {id: 'u123'})
DETACH DELETE u

// Delete relationships only
MATCH (u:User {id: 'u123'})-[r:FRIEND]-()
DELETE r

// Conditional delete
MATCH (u:User)
WHERE u.inactive = true AND u.last_login < datetime() - duration('P365D')
DETACH DELETE u
```

## Recommendations

### Collaborative Filtering

```cypher
// Products purchased by similar users
MATCH (u:User {id: $userId})-[:PURCHASED]->(p:Product)<-[:PURCHASED]-(similar:User)
WITH similar, count(p) AS similarity
ORDER BY similarity DESC
LIMIT 100
MATCH (similar)-[r:PURCHASED]->(rec:Product)
WHERE NOT exists((u)-[:PURCHASED]->(rec))
  AND r.rating >= 4
RETURN rec.name, avg(r.rating) AS avg_rating, count(*) AS purchase_count
ORDER BY purchase_count DESC, avg_rating DESC
LIMIT 10
```

### Content-Based Filtering

```cypher
// Products in same categories as user likes
MATCH (u:User {id: $userId})-[r:PURCHASED]->(p:Product)-[:IN_CATEGORY]->(c:Category)
WHERE r.rating >= 4
WITH c, count(p) AS category_score
ORDER BY category_score DESC
MATCH (c)<-[:IN_CATEGORY]-(rec:Product)
WHERE NOT exists((u)-[:PURCHASED]->(rec))
RETURN rec.name, sum(category_score) AS relevance
ORDER BY relevance DESC
LIMIT 10
```

### Hybrid Recommendations

```cypher
// Combine collaborative + content-based
MATCH (u:User {id: $userId})

// Collaborative component
OPTIONAL MATCH (u)-[:PURCHASED]->(p1:Product)<-[:PURCHASED]-(similar)
OPTIONAL MATCH (similar)-[:PURCHASED]->(collab_rec:Product)
WHERE NOT exists((u)-[:PURCHASED]->(collab_rec))
WITH u, collab_rec, count(*) AS collab_score

// Content-based component
OPTIONAL MATCH (u)-[:PURCHASED]->(p2)-[:IN_CATEGORY]->(c)
OPTIONAL MATCH (c)<-[:IN_CATEGORY]-(content_rec)
WHERE NOT exists((u)-[:PURCHASED]->(content_rec))
WITH collab_rec, collab_score, content_rec, count(*) AS content_score

// Combine scores
WITH coalesce(collab_rec, content_rec) AS recommendation,
     coalesce(collab_score, 0) * 2 + coalesce(content_score, 0) AS total_score
WHERE total_score > 0
RETURN recommendation.name, total_score
ORDER BY total_score DESC
LIMIT 10
```

## Social Graph Patterns

### Friend Suggestions

```cypher
// Friends of friends who aren't already friends
MATCH (u:User {id: $userId})-[:FRIEND]->()-[:FRIEND]->(suggestion)
WHERE NOT exists((u)-[:FRIEND]-(suggestion))
  AND u <> suggestion
WITH suggestion, count(*) AS mutual_friends
WHERE mutual_friends >= 2
RETURN suggestion.name, mutual_friends
ORDER BY mutual_friends DESC
LIMIT 10
```

### Mutual Connections

```cypher
// Find mutual friends between two users
MATCH (u1:User {id: $user1Id})-[:FRIEND]->(mutual)<-[:FRIEND]-(u2:User {id: $user2Id})
RETURN collect(mutual.name) AS mutual_friends, count(mutual) AS count
```

### Influence Metrics

```cypher
// Count followers and following
MATCH (u:User)
OPTIONAL MATCH (u)-[:FOLLOWS]->(following)
OPTIONAL MATCH (u)<-[:FOLLOWS]-(follower)
RETURN
  u.name,
  count(DISTINCT following) AS following_count,
  count(DISTINCT follower) AS follower_count,
  count(DISTINCT follower) * 1.0 / nullif(count(DISTINCT following), 0) AS influence_ratio
ORDER BY follower_count DESC
LIMIT 50
```

## Fraud Detection Patterns

### Circular Money Flows

```cypher
// Detect circular transactions
MATCH path = (a:Account)-[:SENT*3..6]->(a)
WHERE all(r IN relationships(path) WHERE r.amount > 1000)
RETURN
  [n IN nodes(path) | n.id] AS account_chain,
  [r IN relationships(path) | r.amount] AS amounts,
  reduce(total = 0, r IN relationships(path) | total + r.amount) AS total_amount
```

### Shared Devices

```cypher
// Accounts using same device (suspicious)
MATCH (d:Device)<-[:USED_DEVICE]-(t:Transaction)<-[:MADE]-(a:Account)
WITH d, collect(DISTINCT a) AS accounts
WHERE size(accounts) > 5
RETURN
  d.fingerprint,
  [a IN accounts | a.id] AS suspicious_accounts,
  size(accounts) AS account_count
ORDER BY account_count DESC
```

### Rapid Transaction Chains

```cypher
// Fast succession of transfers
MATCH (a1:Account)-[:SENT]->(t1:Transaction)-[:TO]->(a2:Account)
     -[:SENT]->(t2:Transaction)-[:TO]->(a3:Account)
WHERE duration.between(t1.timestamp, t2.timestamp) < duration('PT5M')
  AND t1.amount > 5000
  AND t2.amount > 5000
RETURN a1.id, a2.id, a3.id, t1.amount, t2.amount,
       duration.between(t1.timestamp, t2.timestamp) AS time_between
```

## Performance Patterns

### Use Indexes

```cypher
// Create indexes first
CREATE INDEX user_email FOR (u:User) ON (u.email);
CREATE INDEX product_category FOR (p:Product) ON (p.category);

// Queries benefit from indexes
MATCH (u:User {email: 'alice@example.com'})
RETURN u
```

### Limit Early

```cypher
// GOOD: Limit early in traversal
MATCH (u:User {name: 'Alice'})-[:FRIEND*1..3]->(connection)
RETURN connection.name
LIMIT 100

// BAD: Limit after collecting everything
MATCH (u:User {name: 'Alice'})-[:FRIEND*1..3]->(connection)
WITH collect(connection) AS all_connections
RETURN all_connections[0..100]
```

### Use WITH for Intermediate Results

```cypher
// Materialize expensive computations
MATCH (u:User)-[:FRIEND]->(f)
WITH u, count(f) AS friend_count
WHERE friend_count > 10
MATCH (u)-[:PURCHASED]->(p:Product)
RETURN u.name, friend_count, count(p) AS purchase_count
```

### Avoid Cartesian Products

```cypher
// BAD: Two separate MATCH clauses create cartesian product
MATCH (u:User)
MATCH (p:Product)
RETURN u, p  // Returns every combination!

// GOOD: Connect with relationship
MATCH (u:User)-[:PURCHASED]->(p:Product)
RETURN u, p
```

## Temporal Queries

### Date Filtering

```cypher
// Recent activity
MATCH (u:User)-[r:POSTED]->(post:Post)
WHERE r.timestamp >= datetime() - duration('P7D')
RETURN u.name, post.title, r.timestamp
ORDER BY r.timestamp DESC

// Date range
MATCH (u:User)-[r:PURCHASED]->(p:Product)
WHERE r.date >= date('2025-01-01') AND r.date < date('2025-02-01')
RETURN u.name, p.name, r.date
```

### Time-Based Aggregations

```cypher
// Group by month
MATCH (u:User)-[r:PURCHASED]->(p:Product)
RETURN
  r.date.year AS year,
  r.date.month AS month,
  count(p) AS purchases,
  sum(p.price) AS revenue
ORDER BY year DESC, month DESC
```

## Graph Algorithms (Neo4j GDS)

### PageRank

```cypher
// Find influential nodes
CALL gds.pageRank.stream('socialGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC
LIMIT 10
```

### Community Detection (Louvain)

```cypher
// Find communities
CALL gds.louvain.stream('socialGraph')
YIELD nodeId, communityId
RETURN communityId, collect(gds.util.asNode(nodeId).name) AS members
ORDER BY size(members) DESC
```

### Centrality Metrics

```cypher
// Betweenness centrality (bridge nodes)
CALL gds.betweenness.stream('socialGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC
LIMIT 10

// Degree centrality (most connected)
CALL gds.degree.stream('socialGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC
LIMIT 10
```

## Further Resources

- Neo4j Cypher Manual: https://neo4j.com/docs/cypher-manual/current/
- Cypher Refcard: https://neo4j.com/docs/cypher-refcard/current/
- Graph Data Science: https://neo4j.com/docs/graph-data-science/current/
