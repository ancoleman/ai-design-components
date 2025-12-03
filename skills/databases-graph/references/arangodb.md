# ArangoDB Reference Guide

## Overview

ArangoDB is a multi-model database supporting documents, graphs, and key-value storage in a single unified query language (AQL). This makes it ideal for applications that need both flexible document storage AND graph relationships.

## Key Advantages

1. **Multi-model**: Store documents and graphs together
2. **Single query language**: AQL combines document and graph operations
3. **Schema flexibility**: Documents can have varying structures
4. **Distributed**: Built-in sharding and clustering (SmartGraphs)
5. **Open source**: Apache 2.0 license

## Installation

### Docker
```bash
docker run -d \
  --name arangodb \
  -p 8529:8529 \
  -e ARANGO_ROOT_PASSWORD=password \
  arangodb/arangodb:latest
```

Access Web UI at: http://localhost:8529

### Language Drivers

**Python**:
```bash
pip install python-arango
```

**TypeScript/JavaScript**:
```bash
npm install arangojs
```

**Go**:
```bash
go get github.com/arangodb/go-driver
```

## Connection Setup

### Python
```python
from arango import ArangoClient

# Initialize client
client = ArangoClient(hosts='http://localhost:8529')

# Connect to system database
sys_db = client.db('_system', username='root', password='password')

# Create or access custom database
if not sys_db.has_database('mydb'):
    sys_db.create_database('mydb')

db = client.db('mydb', username='root', password='password')
```

### TypeScript
```typescript
import { Database } from 'arangojs'

const db = new Database({
  url: 'http://localhost:8529',
  databaseName: 'mydb',
  auth: { username: 'root', password: 'password' }
})

// Verify connection
const version = await db.version()
console.log(`ArangoDB ${version.version}`)
```

## Multi-Model Architecture

### Collections

ArangoDB has three collection types:

1. **Document Collections**: Standard NoSQL documents
2. **Edge Collections**: Store relationships (graph edges)
3. **Vertex Collections**: Nodes in graphs (can be document collections)

```python
# Create document collection
users = db.create_collection('users')

# Create edge collection (for relationships)
friends = db.create_collection('friends', edge=True)

# Insert document
users.insert({'_key': 'alice', 'name': 'Alice', 'age': 28})
users.insert({'_key': 'bob', 'name': 'Bob', 'age': 30})

# Insert edge (relationship)
friends.insert({
    '_from': 'users/alice',
    '_to': 'users/bob',
    'since': '2020-01-15'
})
```

### Graph Definitions

Named graphs provide schema-like definitions for relationships:

```python
# Define graph
graph = db.create_graph('social')

# Add edge definition
graph.create_edge_definition(
    edge_collection='friends',
    from_vertex_collections=['users'],
    to_vertex_collections=['users']
)

# Now you can traverse using graph name
```

## AQL Query Language

### Document Queries

```aql
// Find all users
FOR user IN users
  RETURN user

// Filter by property
FOR user IN users
  FILTER user.age >= 25
  RETURN {name: user.name, age: user.age}

// Join documents
FOR user IN users
  FOR post IN posts
    FILTER post.author_id == user._key
    RETURN {user: user.name, post: post.title}
```

### Graph Traversals

#### Basic Traversal
```aql
// Find friends (1 hop)
FOR vertex IN 1..1 OUTBOUND 'users/alice' GRAPH 'social'
  RETURN vertex.name

// Friends of friends (2 hops)
FOR vertex IN 2..2 OUTBOUND 'users/alice' GRAPH 'social'
  RETURN DISTINCT vertex.name
```

#### Variable-Depth Traversal
```aql
// Find connections up to 3 levels deep
FOR vertex, edge, path IN 1..3 OUTBOUND 'users/alice' GRAPH 'social'
  RETURN {
    name: vertex.name,
    depth: LENGTH(path.edges),
    relationship: edge.type
  }
```

#### Shortest Path
```aql
// Find shortest path between two users
FOR path IN OUTBOUND SHORTEST_PATH
  'users/alice' TO 'users/charlie' GRAPH 'social'
  RETURN path
```

#### Pattern Matching
```aql
// Find users who like similar products
FOR user IN users
  FILTER user._key == 'alice'
  FOR liked IN OUTBOUND user GRAPH 'shopping'
    FOR similar_user IN INBOUND liked GRAPH 'shopping'
      FILTER similar_user._key != user._key
      COLLECT similar = similar_user WITH COUNT INTO likes
      SORT likes DESC
      LIMIT 10
      RETURN {user: similar.name, common_likes: likes}
```

## Multi-Model Queries

Combine document and graph operations:

```aql
// Find friends in a specific city
FOR user IN users
  FILTER user._key == 'alice'
  FOR friend IN 1..2 OUTBOUND user GRAPH 'social'
    FILTER friend.city == 'San Francisco'
    FILTER friend.age >= 25 AND friend.age <= 35
    RETURN {
      name: friend.name,
      age: friend.age,
      city: friend.city
    }
```

## Recommendation Patterns

### Collaborative Filtering
```aql
// Products purchased by similar users
FOR user IN users
  FILTER user._key == @userId
  FOR product IN OUTBOUND user purchases
    FOR similar_user IN INBOUND product purchases
      FILTER similar_user._key != user._key
      FOR recommendation IN OUTBOUND similar_user purchases
        FILTER recommendation._key NOT IN (
          FOR p IN OUTBOUND user purchases RETURN p._key
        )
        COLLECT rec = recommendation WITH COUNT INTO score
        SORT score DESC
        LIMIT 10
        RETURN {product: rec, score: score}
```

### Content-Based Filtering
```aql
// Products in same categories as user's purchases
FOR user IN users
  FILTER user._key == @userId
  FOR product IN OUTBOUND user purchases
    FOR category IN OUTBOUND product in_category
      FOR recommendation IN INBOUND category in_category
        FILTER recommendation._key NOT IN (
          FOR p IN OUTBOUND user purchases RETURN p._key
        )
        COLLECT rec = recommendation WITH COUNT INTO relevance
        SORT relevance DESC
        LIMIT 10
        RETURN {product: rec.name, relevance: relevance}
```

## SmartGraphs (Enterprise)

SmartGraphs enable horizontal sharding for massive graphs.

```python
# Create smart graph (Enterprise only)
graph = db.create_graph(
    'social',
    edge_definitions=[{
        'edge_collection': 'friends',
        'from_vertex_collections': ['users'],
        'to_vertex_collections': ['users']
    }],
    smart=True,
    smart_graph_attribute='region'
)

# Documents with same region value are co-located
users.insert({'_key': 'alice', 'region': 'US-West', 'name': 'Alice'})
```

## Indexing

### Hash Index
```aql
// Create hash index for exact matches
db._collection('users').ensureIndex({
  type: 'hash',
  fields: ['email'],
  unique: true
})
```

### Skiplist Index
```aql
// Create skiplist index for range queries
db._collection('users').ensureIndex({
  type: 'skiplist',
  fields: ['age', 'city']
})
```

### Full-Text Index
```aql
// Create full-text search index
db._collection('products').ensureIndex({
  type: 'fulltext',
  fields: ['name', 'description'],
  minLength: 3
})

// Query full-text index
FOR doc IN FULLTEXT('products', 'name,description', 'laptop computer')
  RETURN doc
```

### Geo Index
```aql
// Create geo index for location queries
db._collection('stores').ensureIndex({
  type: 'geo',
  fields: ['location'],
  geoJson: true
})

// Find nearby stores
FOR store IN stores
  FILTER GEO_DISTANCE(store.location, [-122.4194, 37.7749]) <= 5000
  RETURN {name: store.name, distance: GEO_DISTANCE(store.location, [-122.4194, 37.7749])}
  SORT distance
```

## Performance Optimization

### Query Profiling
```aql
// Get query execution plan
EXPLAIN
FOR user IN users
  FILTER user.age > 25
  RETURN user

// Execute with profiling
FOR user IN users
  FILTER user.age > 25
  RETURN user
OPTIONS {profile: 2}
```

### Traversal Optimization

**1. Bounded Depth**
```aql
// SLOW: Unbounded
FOR v IN OUTBOUND 'users/alice' GRAPH 'social'
  RETURN v

// FAST: Bounded depth
FOR v IN 1..3 OUTBOUND 'users/alice' GRAPH 'social'
  RETURN v
```

**2. Prune Early**
```aql
FOR v, e, p IN 1..5 OUTBOUND 'users/alice' GRAPH 'social'
  PRUNE v.blocked == true  // Stop traversing if node is blocked
  FILTER v.active == true
  RETURN v
```

**3. Use Edge Collections Directly**
```aql
// When you don't need full graph traversal
FOR edge IN friends
  FILTER edge._from == 'users/alice'
  FOR user IN users
    FILTER user._id == edge._to
    RETURN user
```

## TypeScript Integration

```typescript
import { Database, aql } from 'arangojs'

class ArangoService {
  private db: Database

  constructor() {
    this.db = new Database({
      url: 'http://localhost:8529',
      databaseName: 'mydb',
      auth: { username: 'root', password: 'password' }
    })
  }

  async findFriendsOfFriends(userId: string, maxDepth: number = 2) {
    const query = aql`
      FOR vertex IN ${maxDepth}..${maxDepth} OUTBOUND ${`users/${userId}`} GRAPH 'social'
        RETURN DISTINCT {
          id: vertex._key,
          name: vertex.name,
          email: vertex.email
        }
        LIMIT 100
    `

    const cursor = await this.db.query(query)
    return await cursor.all()
  }

  async createFriendship(user1Id: string, user2Id: string) {
    const friendsCollection = this.db.collection('friends')
    await friendsCollection.save({
      _from: `users/${user1Id}`,
      _to: `users/${user2Id}`,
      since: new Date().toISOString()
    })
  }

  async recommendProducts(userId: string, limit: number = 10) {
    const query = aql`
      FOR user IN users
        FILTER user._key == ${userId}
        FOR product IN OUTBOUND user purchases
          FOR similar_user IN INBOUND product purchases
            FILTER similar_user._key != user._key
            FOR rec IN OUTBOUND similar_user purchases
              FILTER rec._key NOT IN (FOR p IN OUTBOUND user purchases RETURN p._key)
              COLLECT recommendation = rec WITH COUNT INTO score
              SORT score DESC
              LIMIT ${limit}
              RETURN {
                product: recommendation.name,
                score: score
              }
    `

    const cursor = await this.db.query(query)
    return await cursor.all()
  }
}
```

## Go Integration

```go
package main

import (
    "context"
    "fmt"
    driver "github.com/arangodb/go-driver"
    "github.com/arangodb/go-driver/http"
)

type User struct {
    Key   string `json:"_key"`
    Name  string `json:"name"`
    Email string `json:"email"`
}

func findFriendsOfFriends(db driver.Database, userId string, maxDepth int) ([]User, error) {
    ctx := context.Background()

    query := fmt.Sprintf(`
        FOR vertex IN %d..%d OUTBOUND 'users/%s' GRAPH 'social'
            RETURN DISTINCT vertex
            LIMIT 100
    `, maxDepth, maxDepth, userId)

    cursor, err := db.Query(ctx, query, nil)
    if err != nil {
        return nil, err
    }
    defer cursor.Close()

    var users []User
    for cursor.HasMore() {
        var user User
        _, err := cursor.ReadDocument(ctx, &user)
        if err != nil {
            return nil, err
        }
        users = append(users, user)
    }

    return users, nil
}
```

## Data Migration

### Import from JSON
```python
import json

with open('users.json', 'r') as f:
    users_data = json.load(f)

# Batch insert
users.import_bulk(users_data)
```

### Export to JSON
```python
# Export collection
cursor = db.aql.execute('FOR doc IN users RETURN doc')
users_list = [doc for doc in cursor]

with open('users_export.json', 'w') as f:
    json.dump(users_list, f, indent=2)
```

## Graph Algorithms

ArangoDB provides basic graph algorithms through AQL:

### Shortest Path
```aql
FOR path IN OUTBOUND SHORTEST_PATH
  'users/alice' TO 'users/charlie' GRAPH 'social'
  RETURN {
    vertices: path.vertices[*].name,
    edges: path.edges[*].type,
    distance: LENGTH(path.edges)
  }
```

### All Shortest Paths
```aql
FOR path IN OUTBOUND ALL_SHORTEST_PATHS
  'users/alice' TO 'users/charlie' GRAPH 'social'
  RETURN path
```

### K Shortest Paths
```aql
FOR path IN OUTBOUND K_SHORTEST_PATHS
  'users/alice' TO 'users/charlie' GRAPH 'social'
  LIMIT 5
  RETURN path
```

## Backup and Restore

### Backup (arangodump)
```bash
arangodump \
  --server.endpoint tcp://localhost:8529 \
  --server.username root \
  --server.password password \
  --output-directory /backups/mydb \
  --overwrite true
```

### Restore (arangorestore)
```bash
arangorestore \
  --server.endpoint tcp://localhost:8529 \
  --server.username root \
  --server.password password \
  --input-directory /backups/mydb
```

## ArangoDB Oasis (Managed Cloud)

ArangoDB Oasis is the fully managed cloud service.

**Features**:
- Automated backups and updates
- Multi-region deployments
- SSL/TLS encryption
- Monitoring dashboards
- Free tier available

**Connection**:
```python
from arango import ArangoClient

client = ArangoClient(hosts='https://xxxxx.arangodb.cloud:8529')
db = client.db('mydb', username='root', password='password')
```

## When to Use ArangoDB

**Choose ArangoDB when**:
- Need both documents AND graphs (multi-model)
- Schema flexibility is important
- Want single query language for all data
- Need distributed graph processing (SmartGraphs)

**Choose Neo4j when**:
- Graph-first workload (relationships > documents)
- Need advanced graph algorithms (GDS library)
- Prefer Cypher's pattern matching syntax

## Further Resources

- ArangoDB Documentation: https://www.arangodb.com/docs/
- AQL Tutorial: https://www.arangodb.com/docs/stable/aql/
- ArangoDB University (Free): https://www.arangodb.com/arangodb-training-center/
