# Document Database Implementation - Master Plan

> **Skill Purpose**: Guide NoSQL document database selection and implementation for flexible schema applications across Python, TypeScript, Rust, and Go.
>
> **Date**: December 2025
> **Status**: Planning Phase
> **Sources**: FULL_STACK_SKILLS_UNIFIED.md, Context7 research, MongoDB/DynamoDB/Firestore documentation

---

## Strategic Positioning

### The Document Database Use Case

Document databases excel when applications need:
- **Flexible schemas** - Data models evolve rapidly
- **Nested structures** - JSON-like hierarchical data
- **Horizontal scaling** - Sharding and replication built-in
- **Developer velocity** - Match application objects directly

### When to Use Document Databases

| Scenario | Why Document DB? | Recommended Database |
|----------|------------------|---------------------|
| **Content Management** | Rich metadata, versioning, flexible types | MongoDB |
| **User Profiles** | Variable attributes per user type | MongoDB, Firestore |
| **Product Catalogs** | Different attributes per product category | MongoDB, DynamoDB |
| **Event Logging** | High write throughput, flexible event schemas | MongoDB, DynamoDB |
| **Mobile Apps** | Offline-first sync, real-time updates | Firestore, CouchDB |
| **AWS-Native Apps** | Serverless, auto-scaling, single-digit ms latency | DynamoDB |
| **Firebase/GCP Apps** | Real-time sync, automatic scaling | Firestore |

### Integration with Frontend Skills

| Frontend Skill | Document DB Use Case | Example |
|----------------|---------------------|---------|
| **media/** | Store file metadata (size, type, upload date, tags) | MongoDB GridFS metadata |
| **feedback/** | Event logging (user actions, system events) | DynamoDB time-series writes |
| **ai-chat/** | Conversation history, message metadata | MongoDB with vector search |
| **forms/** | Dynamic form submissions with varying fields | Firestore real-time validation |
| **search-filter/** | Product catalogs with faceted search | MongoDB Atlas Search |

---

## Database Comparison

### Comprehensive Feature Matrix

| Feature | MongoDB | DynamoDB | Firestore | CouchDB |
|---------|---------|----------|-----------|---------|
| **Consistency** | Tunable (eventual to strong) | Strongly consistent reads optional | Strong | Eventual |
| **Query Language** | MQL (MongoDB Query Language) | PartiQL (SQL-like) | Firebase queries | Map/Reduce, Mango |
| **Indexing** | Secondary indexes on any field | Secondary indexes (GSI/LSI) | Composite indexes | Views |
| **Transactions** | Multi-document ACID | Single-item ACID, limited multi | Multi-document ACID | Multi-document MVCC |
| **Aggregation** | Rich aggregation pipeline | Limited (client-side mostly) | Limited | Map/Reduce |
| **Full-Text Search** | Atlas Search (Lucene-based) | CloudSearch integration | Not built-in | Not built-in |
| **Geospatial** | 2D and 2DSphere indexes | Limited | Geohash queries | Limited |
| **Change Streams** | Real-time change notifications | DynamoDB Streams | Real-time listeners | Changes feed |
| **Managed Service** | MongoDB Atlas | AWS (only) | GCP/Firebase (only) | IBM Cloudant |
| **Self-Hosted** | Yes (free Community) | No | No | Yes (Apache 2.0) |
| **Pricing Model** | Storage + Ops/hr | Read/Write capacity units | Read/Write operations | Storage + requests |
| **Horizontal Scaling** | Sharding (auto with Atlas) | Automatic | Automatic | Replication only |
| **Vector Search** | Atlas Vector Search | Not built-in | Not built-in | Not built-in |

### Performance Characteristics

| Database | Write Latency | Read Latency | Max Item Size | Best For |
|----------|---------------|--------------|---------------|----------|
| **MongoDB** | 1-5ms (local), 10-50ms (Atlas) | 1-5ms (indexed) | 16MB | General-purpose, complex queries |
| **DynamoDB** | <10ms (single-digit) | <10ms (cached <1ms) | 400KB | AWS serverless, predictable performance |
| **Firestore** | 50-200ms | 50-200ms (real-time <100ms) | 1MB | Real-time apps, mobile-first |
| **CouchDB** | 10-50ms | 10-50ms | Unlimited (chunked) | Offline-first, sync |

---

## Decision Framework

```
┌─────────────────────────────────────────────────────────────┐
│            Document Database Selection Tree                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  DEPLOYMENT ENVIRONMENT?                                     │
│  ├── AWS-NATIVE APPLICATION                                  │
│  │   └─ DynamoDB                                             │
│  │       ✓ Serverless, auto-scaling                         │
│  │       ✓ Single-digit ms latency                          │
│  │       ✓ Pay-per-request pricing                          │
│  │       ✗ Limited query flexibility                        │
│  │       Example: Event logging, session storage            │
│  │                                                          │
│  ├── FIREBASE / GCP ECOSYSTEM                                │
│  │   └─ Firestore                                            │
│  │       ✓ Real-time sync out-of-box                        │
│  │       ✓ Offline support for mobile                       │
│  │       ✓ Security rules built-in                          │
│  │       ✗ More expensive for heavy reads                   │
│  │       Example: Mobile apps, collaborative tools          │
│  │                                                          │
│  ├── GENERAL-PURPOSE / COMPLEX QUERIES                       │
│  │   └─ MongoDB                                              │
│  │       ✓ Rich aggregation pipeline                        │
│  │       ✓ Full-text search (Atlas Search)                  │
│  │       ✓ Vector search for AI/RAG                         │
│  │       ✓ ACID multi-document transactions                 │
│  │       ✓ Self-hosted or managed (Atlas)                   │
│  │       Example: CMS, e-commerce, analytics                │
│  │                                                          │
│  └── OFFLINE-FIRST / SYNC REQUIRED                           │
│      └─ CouchDB                                              │
│          ✓ Master-master replication                         │
│          ✓ Conflict resolution built-in                      │
│          ✓ HTTP-based API                                    │
│          Example: Field data collection, POS systems         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## MongoDB: Primary Recommendation

### Why MongoDB for Most Use Cases

1. **Query Flexibility**: Full MQL with aggregation pipeline
2. **Schema Evolution**: No migrations, add fields anytime
3. **Vector Search**: Atlas Vector Search for AI/RAG integration
4. **Ecosystem Maturity**: 15+ years, massive community
5. **Multi-Cloud**: Atlas runs on AWS, Azure, GCP

### MongoDB Atlas Features (Managed Service)

| Feature | Capability |
|---------|-----------|
| **Atlas Search** | Lucene-based full-text search, fuzzy matching, autocomplete |
| **Atlas Vector Search** | Semantic search, RAG pipelines, kNN queries |
| **Atlas Triggers** | Database event triggers (like serverless functions) |
| **Atlas App Services** | GraphQL API, authentication, serverless functions |
| **Performance Advisor** | Index recommendations, slow query analysis |
| **Data Lake** | Query S3/Azure Blob data alongside MongoDB |

### MongoDB Aggregation Pipeline Patterns

The aggregation pipeline is MongoDB's killer feature for complex data transformations:

```javascript
// Example: E-commerce product analytics
db.orders.aggregate([
  // Stage 1: Filter recent orders
  { $match: {
      orderDate: { $gte: ISODate("2025-11-01") },
      status: "completed"
  }},

  // Stage 2: Unwind line items
  { $unwind: "$items" },

  // Stage 3: Join with products collection
  { $lookup: {
      from: "products",
      localField: "items.productId",
      foreignField: "_id",
      as: "productInfo"
  }},

  // Stage 4: Group by category
  { $group: {
      _id: "$productInfo.category",
      totalRevenue: { $sum: { $multiply: ["$items.quantity", "$items.price"] }},
      totalQuantity: { $sum: "$items.quantity" },
      avgOrderValue: { $avg: "$totalAmount" }
  }},

  // Stage 5: Sort by revenue
  { $sort: { totalRevenue: -1 }},

  // Stage 6: Limit top 10
  { $limit: 10 }
])
```

**Key Pipeline Operators:**
- `$match` - Filter documents (use early for performance)
- `$project` - Reshape documents, include/exclude fields
- `$group` - Aggregate by key with sum/avg/min/max/count
- `$lookup` - Join with other collections (left outer join)
- `$unwind` - Deconstruct arrays into separate documents
- `$sort` - Order results
- `$limit` / `$skip` - Pagination
- `$facet` - Multi-dimensional aggregations (e.g., filters + results)
- `$bucket` - Histogram grouping

---

## Schema Design Patterns

### Embedding vs Referencing Decision Matrix

| Relationship | Pattern | When to Use | Example |
|--------------|---------|-------------|---------|
| **One-to-Few** | Embed | <10 subdocuments, rarely queried separately | User addresses (2-3 max) |
| **One-to-Many** | Hybrid | 10-100 subdocs, sometimes independent | Blog posts → comments (embed preview, reference rest) |
| **One-to-Millions** | Reference | Unbounded growth, independent access | User → events (logging) |
| **Many-to-Many** | Reference | Shared entities, complex queries | Products ↔ Categories |

### Embedding Pattern (User Profile Example)

```javascript
// Good: Embed when data is always accessed together
{
  _id: ObjectId("..."),
  email: "user@example.com",
  name: "Jane Doe",
  // Embed addresses (few, fixed size)
  addresses: [
    {
      type: "home",
      street: "123 Main St",
      city: "Boston",
      state: "MA",
      zip: "02101",
      default: true
    },
    {
      type: "work",
      street: "456 Business Ave",
      city: "Boston",
      state: "MA",
      zip: "02102"
    }
  ],
  // Embed preferences (key-value pairs)
  preferences: {
    theme: "dark",
    notifications: {
      email: true,
      sms: false,
      push: true
    },
    language: "en-US"
  },
  createdAt: ISODate("2025-01-15"),
  updatedAt: ISODate("2025-11-28")
}
```

### Referencing Pattern (E-commerce Order Example)

```javascript
// Orders collection - Reference products
{
  _id: ObjectId("..."),
  orderNumber: "ORD-2025-001234",
  userId: ObjectId("..."),  // Reference to users collection
  items: [
    {
      productId: ObjectId("..."),  // Reference to products collection
      quantity: 2,
      priceAtPurchase: 49.99,      // Denormalize price (historical)
      name: "Widget Pro"            // Denormalize name (performance)
    },
    {
      productId: ObjectId("..."),
      quantity: 1,
      priceAtPurchase: 149.99,
      name: "Gadget Ultra"
    }
  ],
  shippingAddress: {
    // Embed address (snapshot at order time)
    street: "123 Main St",
    city: "Boston",
    state: "MA",
    zip: "02101"
  },
  totalAmount: 249.97,
  status: "shipped",
  orderDate: ISODate("2025-11-25"),
  shippedDate: ISODate("2025-11-26")
}

// Products collection - Referenced by orders
{
  _id: ObjectId("..."),
  sku: "WGT-PRO-001",
  name: "Widget Pro",
  description: "Professional grade widget",
  price: 49.99,                    // Current price (may differ from order)
  category: "widgets",
  inventory: 245,
  tags: ["professional", "bestseller"],
  specifications: {
    weight: "2.5 lbs",
    dimensions: "10x8x3 inches",
    color: "silver"
  }
}
```

### Denormalization Strategies

**When to Denormalize:**
1. **Frequently Read Together**: Avoid join overhead
2. **Read-Heavy Workloads**: Optimize reads over writes
3. **Historical Snapshots**: Prices, names at transaction time
4. **Reduce Query Complexity**: Eliminate aggregation lookups

**Example: Social Media Post with Author Info**
```javascript
{
  _id: ObjectId("..."),
  content: "Check out this amazing feature!",
  authorId: ObjectId("..."),        // Reference to users
  // Denormalize author info for display
  authorName: "Jane Doe",           // Duplicated from users
  authorAvatar: "/avatars/jane.jpg", // Duplicated from users
  // Original post data
  createdAt: ISODate("2025-11-28"),
  likes: 42,
  comments: 17,
  tags: ["product", "announcement"]
}
```

**Update Pattern for Denormalized Data:**
```javascript
// When user updates profile, update all posts
db.users.updateOne(
  { _id: userId },
  { $set: { name: "Jane Smith", avatar: "/avatars/jane-new.jpg" }}
)

db.posts.updateMany(
  { authorId: userId },
  { $set: {
      authorName: "Jane Smith",
      authorAvatar: "/avatars/jane-new.jpg"
  }}
)
```

---

## Indexing Strategies

### MongoDB Index Types

| Index Type | Use Case | Performance |
|------------|----------|-------------|
| **Single Field** | Query on one field | Fast lookups |
| **Compound** | Query on multiple fields (order matters!) | Efficient multi-field queries |
| **Multikey** | Index array fields | Query array elements |
| **Text** | Full-text search | Search across string fields |
| **Geospatial (2dsphere)** | Location queries | Near, within polygon |
| **Hashed** | Sharding key distribution | Even data distribution |
| **Wildcard** | Dynamic/flexible schemas | Index all fields or subpaths |
| **TTL** | Auto-delete old documents | Session cleanup, logs |

### Index Best Practices

```javascript
// 1. Single Field Index
db.users.createIndex({ email: 1 }, { unique: true })

// 2. Compound Index (ORDER MATTERS!)
// Good for queries: { status: "active", createdAt: { $gte: date }}
db.orders.createIndex({ status: 1, createdAt: -1 })

// 3. Covering Index (query + projection in index)
db.products.createIndex({ category: 1, price: 1, name: 1 })
// Query covered entirely by index (no document fetch):
db.products.find(
  { category: "electronics" },
  { category: 1, price: 1, name: 1, _id: 0 }
)

// 4. Partial Index (index subset of documents)
db.orders.createIndex(
  { userId: 1 },
  { partialFilterExpression: { status: { $eq: "pending" }}}
)

// 5. TTL Index (auto-delete after 30 days)
db.sessions.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 2592000 }
)

// 6. Text Index (full-text search)
db.articles.createIndex({
  title: "text",
  content: "text",
  tags: "text"
})

// Query text index
db.articles.find({ $text: { $search: "mongodb aggregation" }})

// 7. Wildcard Index (for dynamic schemas)
db.products.createIndex({ "specifications.$**": 1 })
// Allows queries on any nested field:
db.products.find({ "specifications.color": "red" })
```

### Index Performance Analysis

```javascript
// Explain query execution plan
db.orders.find({ status: "pending" }).explain("executionStats")

// Key metrics to check:
// - executionTimeMillis: Total execution time
// - totalDocsExamined: Documents scanned (lower is better)
// - totalKeysExamined: Index entries scanned
// - stage: "IXSCAN" (index scan) vs "COLLSCAN" (collection scan - BAD!)

// Ideal: totalDocsExamined ≈ nReturned (no wasted scans)
```

---

## DynamoDB: AWS-Native Serverless

### When to Choose DynamoDB

1. **AWS Ecosystem**: Already using Lambda, API Gateway, etc.
2. **Predictable Performance**: Single-digit millisecond latency
3. **Auto-Scaling**: Pay-per-request pricing, no capacity planning
4. **Serverless Workflows**: Perfect for event-driven architectures

### DynamoDB Data Modeling Principles

**Core Concept**: Design for access patterns, not normalization.

#### Single-Table Design Pattern

```javascript
// Entity types in one table using composite primary key
{
  PK: "USER#12345",           // Partition Key
  SK: "METADATA",             // Sort Key
  email: "user@example.com",
  name: "Jane Doe",
  createdAt: "2025-01-15"
}

{
  PK: "USER#12345",
  SK: "ORDER#2025-001234",    // Order for this user
  orderNumber: "ORD-2025-001234",
  totalAmount: 249.97,
  status: "shipped",
  orderDate: "2025-11-25"
}

{
  PK: "ORDER#2025-001234",    // Same order, different access pattern
  SK: "ITEM#001",
  productId: "PROD-456",
  quantity: 2,
  price: 49.99
}
```

**Query Patterns Enabled:**
- Get user metadata: Query `PK = "USER#12345" AND SK = "METADATA"`
- Get all orders for user: Query `PK = "USER#12345" AND begins_with(SK, "ORDER#")`
- Get order items: Query `PK = "ORDER#2025-001234" AND begins_with(SK, "ITEM#")`

### DynamoDB Global Secondary Indexes (GSI)

```javascript
// Base table: PK = userId, SK = timestamp
// GSI: PK = status, SK = timestamp (query all pending orders)

// Create table with GSI
{
  TableName: "Orders",
  KeySchema: [
    { AttributeName: "userId", KeyType: "HASH" },      // PK
    { AttributeName: "timestamp", KeyType: "RANGE" }   // SK
  ],
  GlobalSecondaryIndexes: [
    {
      IndexName: "StatusIndex",
      KeySchema: [
        { AttributeName: "status", KeyType: "HASH" },
        { AttributeName: "timestamp", KeyType: "RANGE" }
      ],
      Projection: { ProjectionType: "ALL" }
    }
  ]
}

// Query GSI
dynamodb.query({
  TableName: "Orders",
  IndexName: "StatusIndex",
  KeyConditionExpression: "status = :status",
  ExpressionAttributeValues: { ":status": "pending" }
})
```

### DynamoDB Pricing Optimization

| Mode | Use Case | Cost |
|------|----------|------|
| **On-Demand** | Unpredictable traffic, dev/test | $1.25/million writes, $0.25/million reads |
| **Provisioned** | Predictable traffic | $0.47/WCU/month, $0.09/RCU/month |
| **Reserved** | Steady workloads (1-3 year commit) | Save up to 77% |

**Cost Tips:**
- Use DynamoDB Streams instead of polling
- Batch operations (BatchGetItem, BatchWriteItem)
- Use projection expressions (fetch only needed attributes)
- TTL for auto-expiring data (free deletes)

---

## Firestore: Real-Time & Mobile-First

### When to Choose Firestore

1. **Real-Time Sync**: Live updates across clients
2. **Mobile Apps**: Offline support built-in
3. **Firebase Ecosystem**: Authentication, hosting, analytics
4. **Rapid Prototyping**: Generous free tier, quick setup

### Firestore Data Model

```javascript
// Collections and Documents (hierarchical)
users/{userId}/orders/{orderId}/items/{itemId}

// Document structure
{
  // users/user123
  email: "user@example.com",
  name: "Jane Doe",
  createdAt: Timestamp(2025, 1, 15),

  // Subcollection: users/user123/orders/order456
  orders: [
    // Reference, not embedded (use subcollection instead)
  ]
}

// orders/order456 (top-level for cross-user queries)
{
  userId: "user123",           // Reference to user
  items: [
    {
      productId: "prod789",
      quantity: 2,
      price: 49.99
    }
  ],
  totalAmount: 99.98,
  status: "pending",
  createdAt: Timestamp(2025, 11, 25)
}
```

### Real-Time Listeners

```typescript
// React component with real-time updates
import { collection, query, where, onSnapshot } from 'firebase/firestore'

function OrderList({ userId }: { userId: string }) {
  const [orders, setOrders] = useState([])

  useEffect(() => {
    const q = query(
      collection(db, 'orders'),
      where('userId', '==', userId),
      where('status', '==', 'pending')
    )

    // Real-time listener (updates on every change)
    const unsubscribe = onSnapshot(q, (snapshot) => {
      const orderData = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }))
      setOrders(orderData)
    })

    return () => unsubscribe()  // Cleanup on unmount
  }, [userId])

  return <div>{/* Render orders */}</div>
}
```

### Firestore Security Rules

```javascript
// firestore.rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }

    // Orders: users can only see their own
    match /orders/{orderId} {
      allow read: if request.auth != null &&
                     resource.data.userId == request.auth.uid;
      allow create: if request.auth != null &&
                       request.resource.data.userId == request.auth.uid;
      allow update, delete: if request.auth != null &&
                               resource.data.userId == request.auth.uid;
    }

    // Public product catalog
    match /products/{productId} {
      allow read: if true;
      allow write: if request.auth != null &&
                      request.auth.token.admin == true;
    }
  }
}
```

---

## Multi-Language Client Libraries

### Python

#### MongoDB (pymongo + motor for async)

```python
# Synchronous
from pymongo import MongoClient
from pymongo.collection import Collection

client = MongoClient("mongodb://localhost:27017/")
db = client.myapp
users: Collection = db.users

# Insert
user_id = users.insert_one({
    "email": "user@example.com",
    "name": "Jane Doe",
    "createdAt": datetime.utcnow()
}).inserted_id

# Find
user = users.find_one({"email": "user@example.com"})

# Update
users.update_one(
    {"_id": user_id},
    {"$set": {"name": "Jane Smith"}}
)

# Aggregation
pipeline = [
    {"$match": {"status": "active"}},
    {"$group": {
        "_id": "$category",
        "count": {"$sum": 1}
    }}
]
results = list(users.aggregate(pipeline))
```

```python
# Async with motor (FastAPI/AsyncIO)
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI

app = FastAPI()
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client.myapp

@app.get("/users/{email}")
async def get_user(email: str):
    user = await db.users.find_one({"email": email})
    return user
```

#### DynamoDB (boto3)

```python
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Users')

# Put item
table.put_item(Item={
    'userId': 'user123',
    'email': 'user@example.com',
    'name': 'Jane Doe'
})

# Get item
response = table.get_item(Key={'userId': 'user123'})
user = response['Item']

# Query
response = table.query(
    KeyConditionExpression=Key('userId').eq('user123')
)

# Update with condition
table.update_item(
    Key={'userId': 'user123'},
    UpdateExpression='SET #name = :name',
    ExpressionAttributeNames={'#name': 'name'},
    ExpressionAttributeValues={':name': 'Jane Smith'},
    ConditionExpression='attribute_exists(userId)'
)
```

### TypeScript

#### MongoDB (mongodb driver)

```typescript
import { MongoClient, ObjectId } from 'mongodb'

const client = new MongoClient('mongodb://localhost:27017')
await client.connect()

const db = client.db('myapp')
const users = db.collection('users')

// Insert
const result = await users.insertOne({
  email: 'user@example.com',
  name: 'Jane Doe',
  createdAt: new Date()
})

// Find
const user = await users.findOne({ email: 'user@example.com' })

// Update
await users.updateOne(
  { _id: new ObjectId(userId) },
  { $set: { name: 'Jane Smith' }}
)

// Aggregation
const pipeline = [
  { $match: { status: 'active' }},
  { $group: { _id: '$category', count: { $sum: 1 }}}
]
const results = await users.aggregate(pipeline).toArray()
```

#### DynamoDB (AWS SDK v3)

```typescript
import {
  DynamoDBClient,
  PutItemCommand,
  GetItemCommand,
  QueryCommand
} from '@aws-sdk/client-dynamodb'
import { marshall, unmarshall } from '@aws-sdk/util-dynamodb'

const client = new DynamoDBClient({ region: 'us-east-1' })

// Put item
await client.send(new PutItemCommand({
  TableName: 'Users',
  Item: marshall({
    userId: 'user123',
    email: 'user@example.com',
    name: 'Jane Doe'
  })
}))

// Get item
const response = await client.send(new GetItemCommand({
  TableName: 'Users',
  Key: marshall({ userId: 'user123' })
}))
const user = unmarshall(response.Item!)

// Query
const queryResponse = await client.send(new QueryCommand({
  TableName: 'Orders',
  KeyConditionExpression: 'userId = :userId',
  ExpressionAttributeValues: marshall({
    ':userId': 'user123'
  })
}))
```

#### Firestore (Firebase Admin SDK)

```typescript
import { initializeApp } from 'firebase-admin/app'
import { getFirestore } from 'firebase-admin/firestore'

initializeApp()
const db = getFirestore()

// Add document
const docRef = await db.collection('users').add({
  email: 'user@example.com',
  name: 'Jane Doe',
  createdAt: new Date()
})

// Get document
const doc = await db.collection('users').doc(docRef.id).get()
const user = doc.data()

// Update
await db.collection('users').doc(docRef.id).update({
  name: 'Jane Smith'
})

// Query
const snapshot = await db.collection('orders')
  .where('userId', '==', 'user123')
  .where('status', '==', 'pending')
  .get()

snapshot.forEach(doc => console.log(doc.data()))
```

### Rust

#### MongoDB (mongodb crate)

```rust
use mongodb::{Client, Collection, bson::doc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct User {
    #[serde(rename = "_id", skip_serializing_if = "Option::is_none")]
    id: Option<mongodb::bson::oid::ObjectId>,
    email: String,
    name: String,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::with_uri_str("mongodb://localhost:27017").await?;
    let db = client.database("myapp");
    let users: Collection<User> = db.collection("users");

    // Insert
    let user = User {
        id: None,
        email: "user@example.com".to_string(),
        name: "Jane Doe".to_string(),
    };
    let result = users.insert_one(user, None).await?;

    // Find
    let user = users.find_one(doc! { "email": "user@example.com" }, None).await?;

    // Update
    users.update_one(
        doc! { "email": "user@example.com" },
        doc! { "$set": { "name": "Jane Smith" }},
        None
    ).await?;

    Ok(())
}
```

#### DynamoDB (aws-sdk-dynamodb)

```rust
use aws_sdk_dynamodb::{Client, types::AttributeValue};
use std::collections::HashMap;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let config = aws_config::load_from_env().await;
    let client = Client::new(&config);

    // Put item
    let mut item = HashMap::new();
    item.insert("userId".to_string(), AttributeValue::S("user123".to_string()));
    item.insert("email".to_string(), AttributeValue::S("user@example.com".to_string()));

    client.put_item()
        .table_name("Users")
        .set_item(Some(item))
        .send()
        .await?;

    // Get item
    let mut key = HashMap::new();
    key.insert("userId".to_string(), AttributeValue::S("user123".to_string()));

    let response = client.get_item()
        .table_name("Users")
        .set_key(Some(key))
        .send()
        .await?;

    Ok(())
}
```

### Go

#### MongoDB (mongo-go-driver)

```go
package main

import (
    "context"
    "go.mongodb.org/mongo-driver/bson"
    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
)

type User struct {
    ID    primitive.ObjectID `bson:"_id,omitempty"`
    Email string             `bson:"email"`
    Name  string             `bson:"name"`
}

func main() {
    client, err := mongo.Connect(context.TODO(), options.Client().
        ApplyURI("mongodb://localhost:27017"))
    if err != nil {
        panic(err)
    }
    defer client.Disconnect(context.TODO())

    db := client.Database("myapp")
    users := db.Collection("users")

    // Insert
    user := User{
        Email: "user@example.com",
        Name:  "Jane Doe",
    }
    result, err := users.InsertOne(context.TODO(), user)

    // Find
    var foundUser User
    err = users.FindOne(context.TODO(), bson.M{"email": "user@example.com"}).
        Decode(&foundUser)

    // Update
    update := bson.M{"$set": bson.M{"name": "Jane Smith"}}
    _, err = users.UpdateOne(context.TODO(), bson.M{"email": "user@example.com"}, update)
}
```

#### DynamoDB (aws-sdk-go-v2)

```go
package main

import (
    "context"
    "github.com/aws/aws-sdk-go-v2/config"
    "github.com/aws/aws-sdk-go-v2/service/dynamodb"
    "github.com/aws/aws-sdk-go-v2/service/dynamodb/types"
)

func main() {
    cfg, err := config.LoadDefaultConfig(context.TODO())
    if err != nil {
        panic(err)
    }

    client := dynamodb.NewFromConfig(cfg)

    // Put item
    input := &dynamodb.PutItemInput{
        TableName: aws.String("Users"),
        Item: map[string]types.AttributeValue{
            "userId": &types.AttributeValueMemberS{Value: "user123"},
            "email":  &types.AttributeValueMemberS{Value: "user@example.com"},
            "name":   &types.AttributeValueMemberS{Value: "Jane Doe"},
        },
    }
    _, err = client.PutItem(context.TODO(), input)

    // Get item
    getInput := &dynamodb.GetItemInput{
        TableName: aws.String("Users"),
        Key: map[string]types.AttributeValue{
            "userId": &types.AttributeValueMemberS{Value: "user123"},
        },
    }
    result, err := client.GetItem(context.TODO(), getInput)
}
```

---

## Frontend Integration Patterns

### Media Skill Integration (File Metadata)

```javascript
// MongoDB: Store file metadata with GridFS
const { GridFSBucket } = require('mongodb')

const bucket = new GridFSBucket(db, { bucketName: 'uploads' })

// Upload file
const uploadStream = bucket.openUploadStream('profile.jpg', {
  metadata: {
    userId: 'user123',
    contentType: 'image/jpeg',
    tags: ['profile', 'avatar'],
    uploadedAt: new Date()
  }
})
fs.createReadStream('/path/to/file.jpg').pipe(uploadStream)

// Query files by metadata
const files = await db.collection('uploads.files').find({
  'metadata.userId': 'user123',
  'metadata.tags': 'profile'
}).toArray()
```

### Feedback Skill Integration (Event Logging)

```python
# DynamoDB: High-throughput event logging
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
events = dynamodb.Table('UserEvents')

# Log event
events.put_item(Item={
    'userId': 'user123',
    'timestamp': datetime.utcnow().isoformat(),
    'eventType': 'button_click',
    'eventData': {
        'buttonId': 'checkout-btn',
        'page': '/cart',
        'sessionId': 'session456'
    },
    'ttl': int((datetime.utcnow() + timedelta(days=90)).timestamp())
})

# Query recent events
from boto3.dynamodb.conditions import Key

response = events.query(
    KeyConditionExpression=Key('userId').eq('user123') &
                          Key('timestamp').between(
                              '2025-11-01T00:00:00',
                              '2025-11-30T23:59:59'
                          )
)
```

### AI Chat Skill Integration (Conversation History)

```typescript
// MongoDB: Conversation history with vector search
import { MongoClient, ObjectId } from 'mongodb'

interface Message {
  _id?: ObjectId
  conversationId: string
  userId: string
  role: 'user' | 'assistant'
  content: string
  embedding?: number[]  // For semantic search
  timestamp: Date
}

// Store message with embedding
await db.collection<Message>('messages').insertOne({
  conversationId: 'conv123',
  userId: 'user123',
  role: 'user',
  content: 'How do I reset my password?',
  embedding: await generateEmbedding('How do I reset my password?'),
  timestamp: new Date()
})

// Semantic search for similar questions (Atlas Vector Search)
const results = await db.collection('messages').aggregate([
  {
    $vectorSearch: {
      queryVector: await generateEmbedding(userQuestion),
      path: 'embedding',
      numCandidates: 100,
      limit: 5,
      index: 'message_embeddings'
    }
  },
  {
    $project: {
      content: 1,
      score: { $meta: 'vectorSearchScore' }
    }
  }
])
```

---

## Skill Structure

```
skills/databases-document/
├── init.md                           # This file - master plan
├── SKILL.md                          # Main skill file (< 500 lines)
├── references/
│   ├── mongodb-guide.md              # MongoDB setup, queries, aggregation
│   ├── dynamodb-guide.md             # DynamoDB modeling, GSI, best practices
│   ├── firestore-guide.md            # Firestore real-time, security rules
│   ├── couchdb-guide.md              # CouchDB sync patterns
│   ├── schema-design-patterns.md     # Embedding vs referencing
│   ├── indexing-strategies.md        # Index types and performance
│   └── aggregation-patterns.md       # MongoDB pipeline cookbook
├── examples/
│   ├── mongodb-fastapi/              # Python FastAPI + MongoDB
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routes/
│   │   └── requirements.txt
│   ├── mongodb-nextjs/               # TypeScript Next.js + MongoDB
│   │   ├── app/
│   │   ├── lib/mongodb.ts
│   │   └── package.json
│   ├── dynamodb-serverless/          # Python Lambda + DynamoDB
│   │   ├── handler.py
│   │   ├── models.py
│   │   └── serverless.yml
│   ├── firestore-react/              # React + Firestore real-time
│   │   ├── src/
│   │   ├── firestore.rules
│   │   └── package.json
│   └── rust-mongodb/                 # Rust Axum + MongoDB
│       ├── src/
│       └── Cargo.toml
├── scripts/
│   ├── mongodb_schema_analyzer.py    # Analyze schema patterns
│   ├── generate_indexes.py           # Generate optimal indexes
│   └── benchmark_queries.py          # Query performance testing
└── assets/
    └── diagrams/
        ├── embedding-vs-referencing.svg
        ├── dynamodb-gsi-patterns.svg
        └── aggregation-pipeline-flow.svg
```

---

## SKILL.md Frontmatter Template

```yaml
---
name: databases-document
description: Document database implementation for flexible schema applications. Use when building content management, user profiles, catalogs, or event logging. Covers MongoDB (primary), DynamoDB, Firestore, schema design patterns (embedding vs referencing), indexing strategies, aggregation pipelines, and multi-language clients (Python, TypeScript, Rust, Go).
---
```

---

## Quality Checklist

### Core Requirements
- [ ] MongoDB as primary general-purpose recommendation
- [ ] DynamoDB for AWS-native applications
- [ ] Firestore for Firebase/GCP ecosystems
- [ ] CouchDB for offline-first use cases
- [ ] Clear decision framework (ASCII diagram)
- [ ] Embedding vs referencing guidance
- [ ] Aggregation pipeline patterns
- [ ] Indexing strategies with examples
- [ ] Multi-language support (Python, TypeScript, Rust, Go)
- [ ] Frontend integration examples (media, feedback, ai-chat)

### Documentation Quality
- [ ] SKILL.md under 500 lines
- [ ] Progressive disclosure to references/
- [ ] Working code examples for each database
- [ ] Token-free scripts for analysis/benchmarking
- [ ] Clear anti-patterns documented
- [ ] Performance characteristics listed
- [ ] Security best practices included

### Integration Points
- [ ] Connection to media skill (file metadata storage)
- [ ] Connection to feedback skill (event logging patterns)
- [ ] Connection to ai-chat skill (conversation history + vector search)
- [ ] Connection to forms skill (dynamic form submissions)
- [ ] Connection to search-filter skill (full-text search patterns)

### Multi-Language Coverage
- [ ] Python: pymongo (sync), motor (async), boto3 (DynamoDB)
- [ ] TypeScript: mongodb driver, AWS SDK v3, Firestore Admin
- [ ] Rust: mongodb crate, aws-sdk-dynamodb
- [ ] Go: mongo-go-driver, aws-sdk-go-v2

### Anthropic Best Practices
- [ ] Concise frontmatter (name + description)
- [ ] Description includes WHAT and WHEN
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] File references one level deep from SKILL.md
- [ ] Forward slashes in all paths
- [ ] Scripts solve problems (not punt to Claude)

---

## Success Metrics

This skill is successful when:

1. **Database Selection**: Users can confidently choose the right document database for their use case
2. **Schema Design**: Users understand when to embed vs reference
3. **Query Optimization**: Users can write efficient queries and indexes
4. **Multi-Language**: Same quality examples across Python, TypeScript, Rust, Go
5. **Integration**: Clear patterns for connecting to frontend skills

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2025-12-02 | Initial master plan created |

---

*Document Status*: Planning Phase - Ready for SKILL.md implementation
*Research Sources*: FULL_STACK_SKILLS_UNIFIED.md, MongoDB Atlas documentation, AWS DynamoDB best practices, Firestore documentation
*Next Steps*: Create SKILL.md with progressive disclosure, implement reference files, build working examples
