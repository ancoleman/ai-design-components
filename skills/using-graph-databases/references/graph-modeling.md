# Graph Data Modeling Best Practices


## Table of Contents

- [Core Principles](#core-principles)
  - [1. Relationships Are First-Class Citizens](#1-relationships-are-first-class-citizens)
  - [2. Model for Query Patterns](#2-model-for-query-patterns)
  - [3. Denormalize for Performance](#3-denormalize-for-performance)
- [Node Design](#node-design)
  - [Labels](#labels)
  - [Properties](#properties)
- [Relationship Design](#relationship-design)
  - [Relationship Types](#relationship-types)
  - [Relationship Direction](#relationship-direction)
  - [Relationship Properties](#relationship-properties)
- [Common Anti-Patterns](#common-anti-patterns)
  - [Anti-Pattern 1: Arrays Instead of Relationships](#anti-pattern-1-arrays-instead-of-relationships)
  - [Anti-Pattern 2: Supernodes](#anti-pattern-2-supernodes)
  - [Anti-Pattern 3: Dense Nodes Without Indexes](#anti-pattern-3-dense-nodes-without-indexes)
  - [Anti-Pattern 4: Unbounded Traversals](#anti-pattern-4-unbounded-traversals)
- [Schema Design Patterns](#schema-design-patterns)
  - [Pattern 1: Star Schema (Hub and Spokes)](#pattern-1-star-schema-hub-and-spokes)
  - [Pattern 2: Hierarchical Schema (Trees)](#pattern-2-hierarchical-schema-trees)
  - [Pattern 3: Linked List (Sequences)](#pattern-3-linked-list-sequences)
  - [Pattern 4: Many-to-Many with Junction Nodes](#pattern-4-many-to-many-with-junction-nodes)
  - [Pattern 5: Temporal Versioning](#pattern-5-temporal-versioning)
- [Specialized Schemas](#specialized-schemas)
  - [Social Network Schema](#social-network-schema)
  - [Knowledge Graph Schema](#knowledge-graph-schema)
  - [Recommendation Engine Schema](#recommendation-engine-schema)
  - [Access Control Schema (ReBAC)](#access-control-schema-rebac)
- [Modeling for Performance](#modeling-for-performance)
  - [Strategy 1: Materialize Computed Values](#strategy-1-materialize-computed-values)
  - [Strategy 2: Shortcut Relationships](#strategy-2-shortcut-relationships)
  - [Strategy 3: Denormalize Frequently Accessed Data](#strategy-3-denormalize-frequently-accessed-data)
- [Indexing Strategy](#indexing-strategy)
  - [When to Index](#when-to-index)
  - [Composite Indexes](#composite-indexes)
  - [Full-Text Indexes](#full-text-indexes)
- [Migration Patterns](#migration-patterns)
  - [From Relational to Graph](#from-relational-to-graph)
  - [Migration Steps](#migration-steps)
- [Schema Validation](#schema-validation)
  - [Constraints](#constraints)
  - [Validation Queries](#validation-queries)
- [Further Reading](#further-reading)

## Core Principles

### 1. Relationships Are First-Class Citizens

Unlike relational databases where relationships are implied through foreign keys, graph databases make relationships explicit and queryable.

**Relational Model** (relationships hidden in foreign keys):
```sql
CREATE TABLE users (id, name, email);
CREATE TABLE friendships (user_id, friend_id, since);
```

**Graph Model** (relationships are explicit):
```cypher
(:User {id, name, email})-[:FRIEND {since}]->(:User)
```

### 2. Model for Query Patterns

Design your graph schema based on how you'll query it, not just the entity relationships.

**Example**: If you frequently ask "Who works with Alice?", create direct `COLLEAGUE` relationships instead of traversing through `WORKS_AT` to `COMPANY` and back.

### 3. Denormalize for Performance

Graph databases benefit from denormalization. Duplicate data to avoid expensive traversals.

```cypher
// Instead of traversing to get user's company name every time
(u:User)-[:WORKS_AT]->(c:Company {name: 'Acme'})

// Consider denormalizing if frequently accessed
(u:User {company_name: 'Acme'})-[:WORKS_AT]->(c:Company {name: 'Acme'})
```

## Node Design

### Labels

Use labels to categorize nodes. A node can have multiple labels.

```cypher
// Single label
(:User {name: 'Alice'})

// Multiple labels for refinement
(:User:Premium:Verified {name: 'Alice'})
(:Content:Video:Tutorial {title: 'Intro to Graphs'})
```

**Best Practice**: Use labels for types you'll filter by frequently.

```cypher
// Efficient with label
MATCH (u:PremiumUser)
RETURN count(u)

// Less efficient without label
MATCH (u:User)
WHERE u.premium = true
RETURN count(u)
```

### Properties

Store attributes that don't need to be queryable separately as properties.

```cypher
(:User {
  id: 'u123',
  name: 'Alice',
  email: 'alice@example.com',
  age: 28,
  created_at: datetime(),
  preferences: {theme: 'dark', language: 'en'}  // Nested object
})
```

**Property Types** (Neo4j):
- String
- Integer, Float
- Boolean
- Date, DateTime, Duration
- Point (geospatial)
- Lists of above types

**Best Practice**: Index properties you'll filter by:
```cypher
CREATE INDEX user_email FOR (u:User) ON (u.email);
```

## Relationship Design

### Relationship Types

Use descriptive, verb-based relationship types.

**Good**:
```cypher
(:User)-[:FRIEND]->(:User)
(:User)-[:PURCHASED]->(:Product)
(:User)-[:MANAGES]->(:Team)
```

**Avoid**:
```cypher
(:User)-[:RELATES_TO]->(:User)  // Too generic
(:User)-[:LINK]->(:Product)     // Not descriptive
```

### Relationship Direction

Choose direction based on query patterns.

```cypher
// If you ask "Who does Alice manage?"
(:User {name: 'Alice'})-[:MANAGES]->(:User)

// If you ask "Who manages Alice?"
(:User)-[:MANAGES]->(:User {name: 'Alice'})

// For symmetric relationships, choose one direction and query both ways
(:User)-[:FRIEND]->(:User)
// Query: MATCH (u)-[:FRIEND]-(friend) // No arrow = both directions
```

### Relationship Properties

Store metadata about relationships as properties.

```cypher
(:User)-[:FRIEND {
  since: date('2020-01-15'),
  strength: 0.85,
  last_interaction: datetime(),
  interaction_count: 142
}]->(:User)

(:User)-[:PURCHASED {
  date: datetime(),
  quantity: 2,
  price: 49.99,
  rating: 5
}]->(:Product)
```

## Common Anti-Patterns

### Anti-Pattern 1: Arrays Instead of Relationships

**Bad**:
```cypher
(:User {name: 'Alice', friend_ids: ['u2', 'u3', 'u4']})
```

**Good**:
```cypher
(:User {name: 'Alice'})-[:FRIEND]->(:User {id: 'u2'})
(:User {name: 'Alice'})-[:FRIEND]->(:User {id: 'u3'})
```

**Why**: Relationships are indexed and traversable. Arrays require loading the entire node.

### Anti-Pattern 2: Supernodes

**Problem**: Nodes with thousands of relationships slow down traversals.

```cypher
// BAD: User connected to 1M posts
(:User)-[:POSTED]->(:Post)  // 1,000,000 relationships
```

**Solution 1**: Time-based partitioning
```cypher
(:User)-[:POSTED_IN]->(:Year {year: 2025})
  -[:HAS_MONTH]->(:Month {month: 12})
  -[:HAS_POST]->(:Post)
```

**Solution 2**: Category partitioning
```cypher
(:User)-[:HAS_POSTS_IN]->(:Category {name: 'Tech'})
  -[:CONTAINS]->(:Post)
```

### Anti-Pattern 3: Dense Nodes Without Indexes

**Problem**: Querying node properties without indexes on large graphs.

```cypher
// SLOW: Full scan
MATCH (u:User)
WHERE u.email = 'alice@example.com'
RETURN u
```

**Solution**: Create index
```cypher
CREATE INDEX user_email FOR (u:User) ON (u.email);

// Now fast
MATCH (u:User {email: 'alice@example.com'})
RETURN u
```

### Anti-Pattern 4: Unbounded Traversals

**Problem**: Variable-length paths without depth limits.

```cypher
// BAD: Can traverse entire graph
MATCH (a:User {name: 'Alice'})-[:FRIEND*]->(distant)
RETURN distant
```

**Solution**: Bound the depth
```cypher
// GOOD: Limited to 4 hops
MATCH (a:User {name: 'Alice'})-[:FRIEND*1..4]->(distant)
RETURN distant
LIMIT 100
```

## Schema Design Patterns

### Pattern 1: Star Schema (Hub and Spokes)

Central entity with many relationships to different types.

```cypher
// E-commerce user
(:User)-[:PURCHASED]->(:Product)
(:User)-[:VIEWED]->(:Product)
(:User)-[:ADDED_TO_CART]->(:Product)
(:User)-[:RATED]->(:Product)
(:User)-[:REVIEWED]->(:Product)
(:User)-[:HAS_ADDRESS]->(:Address)
(:User)-[:HAS_PAYMENT_METHOD]->(:PaymentMethod)
```

**Use when**: Central entity has many different relationships.

### Pattern 2: Hierarchical Schema (Trees)

Parent-child relationships forming a tree.

```cypher
// Organizational hierarchy
(:CEO)-[:MANAGES]->(:VP)
  -[:MANAGES]->(:Director)
  -[:MANAGES]->(:Manager)
  -[:MANAGES]->(:Employee)

// Category taxonomy
(:RootCategory {name: 'Electronics'})
  -[:HAS_SUBCATEGORY]->(:Category {name: 'Computers'})
  -[:HAS_SUBCATEGORY]->(:Category {name: 'Laptops'})
```

**Query pattern**: Variable-length paths
```cypher
MATCH (root:RootCategory {name: 'Electronics'})-[:HAS_SUBCATEGORY*]->(sub)
RETURN sub.name
```

### Pattern 3: Linked List (Sequences)

Events or items in temporal order.

```cypher
// Event timeline
(:Event {timestamp: '2025-01-01'})-[:NEXT]->
(:Event {timestamp: '2025-01-02'})-[:NEXT]->
(:Event {timestamp: '2025-01-03'})

// Version history
(:DocumentV1)-[:REVISED_TO]->(:DocumentV2)-[:REVISED_TO]->(:DocumentV3)
```

**Query pattern**: Follow chain
```cypher
MATCH (start:Event {id: 'event1'})-[:NEXT*]->(subsequent)
RETURN subsequent
ORDER BY subsequent.timestamp
```

### Pattern 4: Many-to-Many with Junction Nodes

Complex many-to-many with additional attributes.

```cypher
// Student enrollment with grades
(:Student)-[:ENROLLED_IN {semester: 'Fall 2025'}]->
(:Enrollment {grade: 'A', credits: 3})<-[:OFFERS]-
(:Course {name: 'Graph Databases'})
```

**Alternative**: Direct relationship with properties
```cypher
(:Student)-[:ENROLLED_IN {
  semester: 'Fall 2025',
  grade: 'A',
  credits: 3
}]->(:Course)
```

### Pattern 5: Temporal Versioning

Track entity changes over time.

```cypher
// Current version
(:User {id: 'u123', name: 'Alice', version: 3})
  -[:PREVIOUS_VERSION]->(:UserVersion {name: 'Alice Smith', version: 2})
  -[:PREVIOUS_VERSION]->(:UserVersion {name: 'Alice Jones', version: 1})

// Query history
MATCH (u:User {id: 'u123'})-[:PREVIOUS_VERSION*]->(history)
RETURN history.name, history.version
ORDER BY history.version
```

## Specialized Schemas

### Social Network Schema

```cypher
// Nodes
(:Person {id, name, email, joined_date})
(:Post {id, content, created_at})
(:Comment {id, text, created_at})
(:Group {id, name, description})

// Relationships
(:Person)-[:FRIEND {since}]->(:Person)
(:Person)-[:FOLLOWS]->(:Person)
(:Person)-[:MEMBER_OF {joined}]->(:Group)
(:Person)-[:POSTED {timestamp}]->(:Post)
(:Person)-[:COMMENTED {timestamp}]->(:Comment)
(:Comment)-[:REPLY_TO]->(:Post)
(:Comment)-[:REPLY_TO]->(:Comment)
(:Person)-[:LIKES {timestamp}]->(:Post)
(:Person)-[:LIKES {timestamp}]->(:Comment)
```

### Knowledge Graph Schema

```cypher
// Nodes
(:Concept {id, name, description})
(:Document {id, title, url})
(:Entity {id, name, type})  // person, org, location
(:Topic {id, name})

// Relationships
(:Concept)-[:RELATED_TO {strength}]->(:Concept)
(:Concept)-[:IS_A]->(:Concept)  // Hierarchical (ontology)
(:Concept)-[:HAS_PROPERTY]->(:Concept)
(:Concept)-[:OPPOSITE_OF]->(:Concept)
(:Document)-[:MENTIONS]->(:Concept)
(:Document)-[:MENTIONS]->(:Entity)
(:Document)-[:ABOUT]->(:Topic)
(:Entity)-[:WORKS_AT]->(:Entity)
(:Entity)-[:LOCATED_IN]->(:Entity)
```

### Recommendation Engine Schema

```cypher
// Nodes
(:User {id, age, location})
(:Product {id, name, category, price})
(:Category {id, name})
(:Brand {id, name})

// Relationships
(:User)-[:PURCHASED {date, rating, quantity}]->(:Product)
(:User)-[:VIEWED {timestamp, duration}]->(:Product)
(:User)-[:ADDED_TO_CART {timestamp}]->(:Product)
(:User)-[:SEARCHED_FOR {query, timestamp}]->(:Product)
(:Product)-[:IN_CATEGORY]->(:Category)
(:Product)-[:MADE_BY]->(:Brand)
(:Product)-[:SIMILAR_TO {score}]->(:Product)
(:Category)-[:PARENT_CATEGORY]->(:Category)
```

### Access Control Schema (ReBAC)

Relationship-Based Access Control.

```cypher
// Nodes
(:User {id, name})
(:Role {id, name})
(:Resource {id, name, type})
(:Permission {id, action})  // read, write, delete

// Relationships
(:User)-[:HAS_ROLE]->(:Role)
(:User)-[:MEMBER_OF]->(:Group)
(:Group)-[:HAS_ROLE]->(:Role)
(:Role)-[:HAS_PERMISSION]->(:Permission)
(:Permission)-[:ON_RESOURCE]->(:Resource)
(:User)-[:OWNS]->(:Resource)
(:Resource)-[:CHILD_OF]->(:Resource)  // Inheritance

// Query: Can user access resource?
MATCH path = shortestPath(
  (u:User {id: $userId})-[:HAS_ROLE|MEMBER_OF|OWNS*]-(r:Resource {id: $resourceId})
)
RETURN path IS NOT NULL AS hasAccess
```

## Modeling for Performance

### Strategy 1: Materialize Computed Values

Cache expensive calculations as properties.

```cypher
// Instead of computing every time:
MATCH (u:User)-[:FRIEND]->(f)
RETURN u.name, count(f) AS friend_count

// Materialize:
MATCH (u:User)-[:FRIEND]->(f)
WITH u, count(f) AS fc
SET u.friend_count = fc

// Query becomes instant:
MATCH (u:User)
RETURN u.name, u.friend_count
ORDER BY u.friend_count DESC
```

**Update strategy**: Batch update periodically or trigger on changes.

### Strategy 2: Shortcut Relationships

Create direct paths for frequent traversals.

```cypher
// Instead of: User -> Company -> Department -> Manager
(:User)-[:WORKS_AT]->(:Company)-[:HAS_DEPARTMENT]->(:Department)-[:MANAGED_BY]->(:Manager)

// Add shortcut:
(:User)-[:MANAGER]->(:Manager)

// Query is now single hop
MATCH (u:User {id: 'u123'})-[:MANAGER]->(m)
RETURN m.name
```

### Strategy 3: Denormalize Frequently Accessed Data

```cypher
// Original: Always traverse to get company name
(:User {name: 'Alice'})-[:WORKS_AT]->(:Company {name: 'Acme'})

// Denormalized: Store company name on user
(:User {name: 'Alice', company_name: 'Acme'})-[:WORKS_AT]->(:Company {name: 'Acme'})
```

**Trade-off**: Faster reads, but need to update duplicates when source changes.

## Indexing Strategy

### When to Index

Index properties that are:
1. Frequently filtered (WHERE clauses)
2. Used for lookups (MATCH with property)
3. Sorted (ORDER BY)

```cypher
// High-value indexes
CREATE INDEX user_email FOR (u:User) ON (u.email);
CREATE INDEX product_sku FOR (p:Product) ON (p.sku);
CREATE INDEX order_date FOR (o:Order) ON (o.date);
```

### Composite Indexes

For queries filtering on multiple properties.

```cypher
CREATE INDEX user_location FOR (u:User) ON (u.city, u.state);

// Benefits this query:
MATCH (u:User {city: 'San Francisco', state: 'CA'})
RETURN u
```

### Full-Text Indexes

For text search queries.

```cypher
CREATE FULLTEXT INDEX product_search FOR (p:Product) ON EACH [p.name, p.description];

CALL db.index.fulltext.queryNodes('product_search', 'laptop computer')
YIELD node, score
RETURN node.name, score
ORDER BY score DESC
```

## Migration Patterns

### From Relational to Graph

**Relational**:
```sql
users (id, name, email)
friendships (user_id, friend_id, since)
posts (id, user_id, content, created_at)
comments (id, post_id, user_id, text)
```

**Graph**:
```cypher
// Nodes (rows become nodes)
(:User {id, name, email})
(:Post {id, content, created_at})
(:Comment {id, text})

// Relationships (foreign keys become relationships)
(:User)-[:FRIEND {since}]->(:User)
(:User)-[:POSTED]->(:Post)
(:User)-[:COMMENTED]->(:Comment)
(:Comment)-[:ON_POST]->(:Post)
```

### Migration Steps

1. **Identify entities** → Nodes
2. **Identify relationships** → Edges
3. **Foreign keys** → Relationships
4. **Junction tables** → Either relationships with properties OR intermediate nodes
5. **Attributes** → Properties

```python
# Example migration script
from neo4j import GraphDatabase
import psycopg2

# Connect to PostgreSQL
pg_conn = psycopg2.connect("dbname=mydb user=postgres")
pg_cur = pg_conn.cursor()

# Connect to Neo4j
neo4j_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

def migrate_users():
    pg_cur.execute("SELECT id, name, email FROM users")
    users = pg_cur.fetchall()

    with neo4j_driver.session() as session:
        for user_id, name, email in users:
            session.run(
                "CREATE (u:User {id: $id, name: $name, email: $email})",
                id=user_id, name=name, email=email
            )

def migrate_friendships():
    pg_cur.execute("SELECT user_id, friend_id, since FROM friendships")
    friendships = pg_cur.fetchall()

    with neo4j_driver.session() as session:
        for user_id, friend_id, since in friendships:
            session.run(
                """
                MATCH (u1:User {id: $user_id}), (u2:User {id: $friend_id})
                CREATE (u1)-[:FRIEND {since: $since}]->(u2)
                """,
                user_id=user_id, friend_id=friend_id, since=since
            )
```

## Schema Validation

### Constraints

```cypher
// Uniqueness
CREATE CONSTRAINT user_email_unique FOR (u:User) REQUIRE u.email IS UNIQUE;

// Existence (Enterprise only)
CREATE CONSTRAINT user_name_exists FOR (u:User) REQUIRE u.name IS NOT NULL;

// Node key (composite uniqueness)
CREATE CONSTRAINT user_key FOR (u:User) REQUIRE (u.id, u.email) IS NODE KEY;
```

### Validation Queries

Check for schema violations:

```cypher
// Find nodes without required properties
MATCH (u:User)
WHERE u.email IS NULL
RETURN u

// Find orphaned nodes (no relationships)
MATCH (n)
WHERE NOT (n)--()
RETURN labels(n), count(n)

// Find supernodes (too many relationships)
MATCH (n)
WITH n, size((n)--()) AS degree
WHERE degree > 10000
RETURN labels(n), n.id, degree
ORDER BY degree DESC
```

## Further Reading

- Neo4j Graph Data Modeling Guide: https://neo4j.com/developer/guide-data-modeling/
- Graph Databases (O'Reilly Book): https://neo4j.com/graph-databases-book/
