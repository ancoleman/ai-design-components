# MongoDB Complete Guide

Comprehensive MongoDB reference covering collections, queries, indexes, aggregation framework, and Atlas features.

## Table of Contents

- [Setup and Connection](#setup-and-connection)
- [Collections and Documents](#collections-and-documents)
- [CRUD Operations](#crud-operations)
- [Query Operators](#query-operators)
- [Indexes](#indexes)
- [Aggregation Framework](#aggregation-framework)
- [Transactions](#transactions)
- [Atlas Features](#atlas-features)
- [Performance Tuning](#performance-tuning)

---

## Setup and Connection

### MongoDB Atlas (Managed Service)

```javascript
// Connection string format
mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/myapp?retryWrites=true&w=majority
```

### Python (Motor - Async)

```python
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

# Connect to Atlas
client = AsyncIOMotorClient(
    "mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/",
    server_api=ServerApi('1'),
    maxPoolSize=50,
    minPoolSize=10
)

db = client.myapp
users_collection = db.users

# Test connection
async def ping():
    await client.admin.command('ping')
    print("Connected to MongoDB!")
```

### TypeScript (Native Driver)

```typescript
import { MongoClient, ServerApiVersion } from 'mongodb'

const client = new MongoClient(process.env.MONGODB_URI!, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
})

await client.connect()
const db = client.db('myapp')
const users = db.collection('users')
```

### Connection Pooling Best Practices

```python
# Python: Reuse client across app lifecycle
# Create once at startup
client = AsyncIOMotorClient(
    uri,
    maxPoolSize=50,        # Max concurrent connections
    minPoolSize=10,        # Maintain minimum pool
    maxIdleTimeMS=30000,   # Close idle connections after 30s
    serverSelectionTimeoutMS=5000  # Timeout after 5s
)

# Use throughout application
async def get_user(email: str):
    return await client.myapp.users.find_one({"email": email})
```

---

## Collections and Documents

### Document Structure

```javascript
{
  _id: ObjectId("507f1f77bcf86cd799439011"),  // Auto-generated unique ID
  email: "user@example.com",
  name: "Jane Doe",
  age: 32,
  address: {                                   // Embedded document
    street: "123 Main St",
    city: "Boston",
    state: "MA"
  },
  hobbies: ["reading", "cycling"],            // Array
  metadata: {                                  // Nested object
    createdAt: ISODate("2025-01-15"),
    updatedAt: ISODate("2025-11-28"),
    version: 3
  }
}
```

### Schema Validation (Optional)

```javascript
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "name"],
      properties: {
        email: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        name: {
          bsonType: "string",
          minLength: 1
        },
        age: {
          bsonType: "int",
          minimum: 0,
          maximum: 150
        }
      }
    }
  },
  validationLevel: "moderate",  // moderate or strict
  validationAction: "warn"      // warn or error
})
```

---

## CRUD Operations

### Create (Insert)

```python
# Insert one
from bson import ObjectId

result = await db.users.insert_one({
    "email": "user@example.com",
    "name": "Jane Doe",
    "createdAt": datetime.utcnow()
})
user_id = result.inserted_id

# Insert many
users = [
    {"email": "user1@example.com", "name": "User One"},
    {"email": "user2@example.com", "name": "User Two"}
]
result = await db.users.insert_many(users)
inserted_ids = result.inserted_ids
```

### Read (Find)

```python
# Find one
user = await db.users.find_one({"email": "user@example.com"})

# Find many with filter
active_users = await db.users.find({"status": "active"}).to_list(length=100)

# Find with projection (select specific fields)
users = await db.users.find(
    {"status": "active"},
    {"name": 1, "email": 1, "_id": 0}  # Include name, email; exclude _id
).to_list(length=100)

# Find with sorting
users = await db.users.find().sort([
    ("createdAt", -1),  # Descending
    ("name", 1)         # Then ascending
]).to_list(length=100)

# Find with pagination
page_size = 20
skip = (page_number - 1) * page_size
users = await db.users.find().skip(skip).limit(page_size).to_list(length=100)
```

### Update

```python
# Update one
result = await db.users.update_one(
    {"email": "user@example.com"},           # Filter
    {"$set": {"name": "Jane Smith"}}         # Update
)
print(f"Modified {result.modified_count} documents")

# Update many
result = await db.users.update_many(
    {"status": "inactive"},
    {"$set": {"archived": True}}
)

# Upsert (update or insert)
result = await db.users.update_one(
    {"email": "new@example.com"},
    {"$set": {"name": "New User"}},
    upsert=True  # Create if not found
)
```

### Delete

```python
# Delete one
result = await db.users.delete_one({"email": "user@example.com"})

# Delete many
result = await db.users.delete_many({"status": "archived"})
print(f"Deleted {result.deleted_count} documents")

# Soft delete (recommended)
result = await db.users.update_one(
    {"email": "user@example.com"},
    {"$set": {"deleted": True, "deletedAt": datetime.utcnow()}}
)
```

---

## Query Operators

### Comparison Operators

```python
# Equal
db.users.find({"age": 30})

# Not equal
db.users.find({"age": {"$ne": 30}})

# Greater than, greater than or equal
db.users.find({"age": {"$gt": 25}})
db.users.find({"age": {"$gte": 25}})

# Less than, less than or equal
db.users.find({"age": {"$lt": 40}})
db.users.find({"age": {"$lte": 40}})

# In array
db.users.find({"status": {"$in": ["active", "pending"]}})

# Not in array
db.users.find({"status": {"$nin": ["archived", "deleted"]}})
```

### Logical Operators

```python
# AND (implicit)
db.users.find({"status": "active", "age": {"$gte": 18}})

# AND (explicit)
db.users.find({"$and": [
    {"status": "active"},
    {"age": {"$gte": 18}}
]})

# OR
db.users.find({"$or": [
    {"status": "active"},
    {"status": "pending"}
]})

# NOT
db.users.find({"age": {"$not": {"$gte": 18}}})

# NOR (not or)
db.users.find({"$nor": [
    {"status": "archived"},
    {"deleted": True}
]})
```

### Element Operators

```python
# Field exists
db.users.find({"email": {"$exists": True}})

# Field type
db.users.find({"age": {"$type": "int"}})
```

### Array Operators

```python
# All elements match
db.users.find({"hobbies": {"$all": ["reading", "cycling"]}})

# Array size
db.users.find({"hobbies": {"$size": 3}})

# Element match (for embedded documents)
db.orders.find({
    "items": {
        "$elemMatch": {
            "productId": "PROD-123",
            "quantity": {"$gte": 2}
        }
    }
})
```

### String Operators (Regex)

```python
# Case-insensitive search
db.users.find({"name": {"$regex": "jane", "$options": "i"}})

# Starts with
db.users.find({"email": {"$regex": "^admin"}})

# Contains
db.users.find({"name": {"$regex": "doe"}})
```

---

## Indexes

### Index Types

```python
# Single field index
await db.users.create_index("email", unique=True)

# Compound index (order matters!)
await db.orders.create_index([
    ("status", 1),      # Ascending
    ("createdAt", -1)   # Descending
])

# Multikey index (on array fields)
await db.users.create_index("tags")  # Indexes each element

# Text index (full-text search)
await db.articles.create_index([
    ("title", "text"),
    ("content", "text")
])

# Geospatial index
await db.locations.create_index([("coordinates", "2dsphere")])

# Hashed index (for sharding)
await db.users.create_index([("userId", "hashed")])

# Wildcard index (for dynamic schemas)
await db.products.create_index({"specifications.$**": 1})
```

### Index Options

```python
# Unique index
await db.users.create_index("email", unique=True)

# Partial index (index subset of documents)
await db.orders.create_index(
    "userId",
    partialFilterExpression={"status": {"$eq": "pending"}}
)

# TTL index (auto-delete after expiration)
await db.sessions.create_index(
    "createdAt",
    expireAfterSeconds=86400  # 24 hours
)

# Sparse index (only index documents with field)
await db.users.create_index("phoneNumber", sparse=True)

# Case-insensitive index
await db.users.create_index(
    "email",
    collation={"locale": "en", "strength": 2}
)
```

### Index Management

```python
# List indexes
indexes = await db.users.list_indexes().to_list(length=100)

# Drop index
await db.users.drop_index("email_1")

# Drop all indexes (except _id)
await db.users.drop_indexes()

# Rebuild indexes
await db.users.reindex()
```

### Index Analysis

```python
# Explain query execution plan
explain = await db.users.find({"status": "active"}).explain()

print(f"Execution time: {explain['executionStats']['executionTimeMillis']} ms")
print(f"Documents examined: {explain['executionStats']['totalDocsExamined']}")
print(f"Keys examined: {explain['executionStats']['totalKeysExamined']}")
print(f"Stage: {explain['executionStats']['executionStages']['stage']}")
# Stage should be "IXSCAN" (index scan), not "COLLSCAN" (collection scan)
```

---

## Aggregation Framework

### Pipeline Stages

```javascript
// Complete aggregation example
db.orders.aggregate([
  // Stage 1: Match (filter)
  { $match: {
      orderDate: { $gte: ISODate("2025-11-01") },
      status: "completed"
  }},

  // Stage 2: Lookup (join)
  { $lookup: {
      from: "users",
      localField: "userId",
      foreignField: "_id",
      as: "user"
  }},

  // Stage 3: Unwind (flatten array)
  { $unwind: "$user" },

  // Stage 4: Unwind items
  { $unwind: "$items" },

  // Stage 5: Lookup products
  { $lookup: {
      from: "products",
      localField: "items.productId",
      foreignField: "_id",
      as: "product"
  }},

  // Stage 6: Unwind products
  { $unwind: "$product" },

  // Stage 7: Group by category
  { $group: {
      _id: "$product.category",
      totalRevenue: {
        $sum: { $multiply: ["$items.quantity", "$items.price"] }
      },
      totalQuantity: { $sum: "$items.quantity" },
      orderCount: { $sum: 1 },
      avgOrderValue: { $avg: "$totalAmount" }
  }},

  // Stage 8: Project (reshape)
  { $project: {
      _id: 0,
      category: "$_id",
      totalRevenue: 1,
      totalQuantity: 1,
      orderCount: 1,
      avgOrderValue: { $round: ["$avgOrderValue", 2] }
  }},

  // Stage 9: Sort
  { $sort: { totalRevenue: -1 }},

  // Stage 10: Limit
  { $limit: 10 }
])
```

### Grouping Accumulators

```javascript
// Sum, average, min, max
{ $group: {
    _id: "$category",
    total: { $sum: "$price" },
    avg: { $avg: "$price" },
    min: { $min: "$price" },
    max: { $max: "$price" },
    count: { $sum: 1 }
}}

// Push to array
{ $group: {
    _id: "$userId",
    orders: { $push: "$orderId" }
}}

// Add to set (unique values)
{ $group: {
    _id: "$userId",
    uniqueProducts: { $addToSet: "$productId" }
}}

// First, last
{ $group: {
    _id: "$userId",
    firstOrder: { $first: "$orderDate" },
    lastOrder: { $last: "$orderDate" }
}}
```

### Conditional Aggregation

```javascript
// $cond (if-then-else)
{ $project: {
    discount: {
      $cond: {
        if: { $gte: ["$totalAmount", 100] },
        then: { $multiply: ["$totalAmount", 0.1] },
        else: 0
      }
    }
}}

// $switch (multi-way branch)
{ $project: {
    tier: {
      $switch: {
        branches: [
          { case: { $gte: ["$totalAmount", 1000] }, then: "platinum" },
          { case: { $gte: ["$totalAmount", 500] }, then: "gold" },
          { case: { $gte: ["$totalAmount", 100] }, then: "silver" }
        ],
        default: "bronze"
      }
    }
}}
```

### Faceted Search

```javascript
// Multi-dimensional aggregation
db.products.aggregate([
  { $match: { category: "electronics" }},
  { $facet: {
      // Facet 1: Price ranges
      "priceRanges": [
        { $bucket: {
            groupBy: "$price",
            boundaries: [0, 50, 100, 200, 500],
            default: "500+",
            output: { count: { $sum: 1 }}
        }}
      ],
      // Facet 2: Top brands
      "topBrands": [
        { $group: { _id: "$brand", count: { $sum: 1 }}},
        { $sort: { count: -1 }},
        { $limit: 5 }
      ],
      // Facet 3: Results
      "results": [
        { $sort: { popularity: -1 }},
        { $limit: 20 }
      ]
  }}
])
```

---

## Transactions

### Multi-Document ACID Transactions

```python
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(uri)

async def transfer_funds(from_user_id, to_user_id, amount):
    async with await client.start_session() as session:
        async with session.start_transaction():
            # Debit from sender
            result = await db.accounts.update_one(
                {"userId": from_user_id, "balance": {"$gte": amount}},
                {"$inc": {"balance": -amount}},
                session=session
            )

            if result.modified_count == 0:
                await session.abort_transaction()
                raise ValueError("Insufficient funds")

            # Credit to receiver
            await db.accounts.update_one(
                {"userId": to_user_id},
                {"$inc": {"balance": amount}},
                session=session
            )

            # Commit transaction
            # Auto-committed when exiting context
```

### Transaction Best Practices

- Keep transactions short (< 1 second)
- Limit to 1000 documents
- Use retryable writes for single operations
- Avoid long-running queries in transactions
- Use `writeConcern: "majority"` for consistency

---

## Atlas Features

### Atlas Search (Lucene-based Full-Text)

```javascript
// Create search index (in Atlas UI or CLI)
{
  "mappings": {
    "dynamic": false,
    "fields": {
      "title": { "type": "string" },
      "content": { "type": "string" },
      "tags": { "type": "stringFacet" }
    }
  }
}

// Search query
db.articles.aggregate([
  {
    $search: {
      index: "default",
      text: {
        query: "mongodb aggregation",
        path: ["title", "content"],
        fuzzy: { maxEdits: 1 }
      }
    }
  },
  {
    $project: {
      title: 1,
      content: 1,
      score: { $meta: "searchScore" }
    }
  },
  { $limit: 10 }
])
```

### Atlas Vector Search (AI/RAG)

```javascript
// Create vector search index
{
  "fields": [{
    "type": "vector",
    "path": "embedding",
    "numDimensions": 1536,  // OpenAI ada-002
    "similarity": "cosine"
  }]
}

// Vector search query
db.messages.aggregate([
  {
    $vectorSearch: {
      queryVector: embeddingVector,  // From OpenAI/etc
      path: "embedding",
      numCandidates: 100,
      limit: 5,
      index: "vector_index"
    }
  },
  {
    $project: {
      content: 1,
      score: { $meta: "vectorSearchScore" }
    }
  }
])
```

### Atlas Triggers (Database Events)

```javascript
// Trigger function (in Atlas)
exports = async function(changeEvent) {
  const { fullDocument, operationType } = changeEvent

  if (operationType === 'insert') {
    // Send welcome email
    await context.functions.execute("sendWelcomeEmail", fullDocument.email)
  }
}
```

---

## Performance Tuning

### Query Optimization

```python
# Use projection (fetch only needed fields)
users = await db.users.find(
    {"status": "active"},
    {"name": 1, "email": 1, "_id": 0}
).to_list(length=100)

# Use covered queries (query + projection in index)
# Index: { status: 1, name: 1, email: 1 }
# Query only uses index, no document fetch!
```

### Batch Operations

```python
# Batch inserts
from pymongo import InsertOne, UpdateOne

requests = [
    InsertOne({"email": "user1@example.com"}),
    UpdateOne({"email": "user2@example.com"}, {"$set": {"name": "Updated"}})
]
result = await db.users.bulk_write(requests)
```

### Read Preference

```python
# Read from secondaries (eventual consistency)
from pymongo import ReadPreference

result = await db.users.find(
    {"status": "active"}
).read_preference(ReadPreference.SECONDARY_PREFERRED).to_list(length=100)
```

### Write Concern

```python
# Acknowledge writes after majority of replicas
from pymongo import WriteConcern

result = await db.users.with_options(
    write_concern=WriteConcern(w="majority", wtimeout=5000)
).insert_one({"email": "user@example.com"})
```

### Atlas Performance Advisor

- Automatically suggests indexes for slow queries
- Identifies unused indexes
- Analyzes query patterns
- Available in Atlas UI

---

## Common Patterns

### Pagination (Cursor-Based)

```python
# Better than skip/limit for large datasets
async def get_page(last_id=None, page_size=20):
    query = {}
    if last_id:
        query["_id"] = {"$gt": ObjectId(last_id)}

    results = await db.products.find(query).sort("_id", 1).limit(page_size).to_list(length=100)

    return {
        "data": results,
        "nextCursor": str(results[-1]["_id"]) if results else None
    }
```

### Soft Deletes

```python
# Create compound index excluding deleted
await db.users.create_index(
    [("email", 1)],
    partialFilterExpression={"deleted": {"$ne": True}}
)

# Mark as deleted
await db.users.update_one(
    {"_id": user_id},
    {"$set": {"deleted": True, "deletedAt": datetime.utcnow()}}
)

# Query non-deleted
users = await db.users.find({"deleted": {"$ne": True}}).to_list(length=100)
```

### Audit Logs

```python
# Store version history
{
    "_id": ObjectId("..."),
    "documentId": "doc123",
    "version": 3,
    "content": "Current content",
    "history": [
        {"version": 1, "content": "Original", "timestamp": "..."},
        {"version": 2, "content": "Updated", "timestamp": "..."}
    ]
}
```

---

## TypeScript Type Safety

```typescript
import { MongoClient, Document, ObjectId } from 'mongodb'

interface User extends Document {
  _id?: ObjectId
  email: string
  name: string
  age?: number
  createdAt: Date
}

const client = new MongoClient(process.env.MONGODB_URI!)
const db = client.db('myapp')
const users = db.collection<User>('users')

// Type-safe operations
const user = await users.findOne({ email: 'user@example.com' })
if (user) {
  console.log(user.name)  // TypeScript knows this exists
}

await users.insertOne({
  email: 'new@example.com',
  name: 'New User',
  createdAt: new Date()
})
```

---

## Monitoring and Debugging

### Connection Pool Monitoring

```python
from pymongo import monitoring

class ConnectionPoolLogger(monitoring.ConnectionPoolListener):
    def pool_created(self, event):
        print(f"Pool created: {event.address}")

    def connection_checked_out(self, event):
        print(f"Connection checked out: {event.connection_id}")

monitoring.register(ConnectionPoolLogger())
```

### Slow Query Logging

```javascript
// Enable profiling (level 1 = slow queries only)
db.setProfilingLevel(1, { slowms: 100 })

// View slow queries
db.system.profile.find().sort({ ts: -1 }).limit(10)
```

---

This comprehensive guide covers MongoDB from basics to advanced patterns. For aggregation cookbook, see `aggregation-patterns.md`.
