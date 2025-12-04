---
sidebar_position: 5
title: Document Databases
description: Document database implementation for flexible schema applications
tags: [backend, database, nosql, mongodb, dynamodb, firestore]
---

# Document Database Implementation

NoSQL document database selection and implementation for flexible schema applications across Python, TypeScript, Rust, and Go.

## When to Use

Use document databases when applications need:
- **Flexible schemas** - Data models evolve rapidly without migrations
- **Nested structures** - JSON-like hierarchical data
- **Horizontal scaling** - Built-in sharding and replication
- **Developer velocity** - Object-to-database mapping without ORM complexity

## Multi-Language Support

This skill provides patterns for:
- **Python**: MongoDB (motor, pymongo), DynamoDB (boto3), Firestore (firebase-admin)
- **TypeScript**: MongoDB (mongodb), DynamoDB (@aws-sdk), Firestore (firebase)
- **Rust**: MongoDB (mongodb 2.8), DynamoDB (aws-sdk-dynamodb)
- **Go**: MongoDB (mongo-driver), DynamoDB (aws-sdk-go-v2)

## Database Selection

### Quick Decision Framework

```
DEPLOYMENT ENVIRONMENT?
├── AWS-Native Application → DynamoDB
│   ✓ Serverless, auto-scaling, single-digit ms latency
│   ✗ Limited query flexibility
│
├── Firebase/GCP Ecosystem → Firestore
│   ✓ Real-time sync, offline support, mobile-first
│   ✗ More expensive for heavy reads
│
└── General-Purpose/Complex Queries → MongoDB
    ✓ Rich aggregation, full-text search, vector search
    ✓ ACID transactions, self-hosted or managed
```

### Database Comparison

| Database | Best For | Latency | Max Item | Query Language |
|----------|----------|---------|----------|----------------|
| **MongoDB** | General-purpose, complex queries | 1-5ms | 16MB | MQL (rich) |
| **DynamoDB** | AWS serverless, predictable performance | &lt;10ms | 400KB | PartiQL (limited) |
| **Firestore** | Real-time apps, mobile-first | 50-200ms | 1MB | Firebase queries |

## Schema Design Patterns

### Embedding vs Referencing

Quick guide:

| Relationship | Pattern | Example |
|--------------|---------|---------|
| One-to-Few | Embed | User addresses (2-3 max) |
| One-to-Many | Hybrid | Blog posts → comments |
| One-to-Millions | Reference | User → events (logging) |
| Many-to-Many | Reference | Products ↔ Categories |

### Embedding Example (MongoDB)

```javascript
// User with embedded addresses
{
  _id: ObjectId("..."),
  email: "user@example.com",
  name: "Jane Doe",
  addresses: [
    {
      type: "home",
      street: "123 Main St",
      city: "Boston",
      default: true
    }
  ],
  preferences: {
    theme: "dark",
    notifications: { email: true, sms: false }
  }
}
```

### Referencing Example (E-commerce)

```javascript
// Orders reference products
{
  _id: ObjectId("..."),
  userId: ObjectId("..."),
  items: [
    {
      productId: ObjectId("..."),      // Reference
      priceAtPurchase: 49.99,          // Denormalize (historical)
      quantity: 2
    }
  ],
  totalAmount: 99.98
}
```

**When to denormalize:**
- Frequently read together
- Historical snapshots (prices, names)
- Read-heavy workloads

## Indexing Strategies

### MongoDB Index Types

```javascript
// 1. Single field (unique email)
db.users.createIndex({ email: 1 }, { unique: true })

// 2. Compound index (ORDER MATTERS!)
db.orders.createIndex({ status: 1, createdAt: -1 })

// 3. Partial index (index subset)
db.orders.createIndex(
  { userId: 1 },
  { partialFilterExpression: { status: { $eq: "pending" }}}
)

// 4. TTL index (auto-delete after 30 days)
db.sessions.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 2592000 }
)

// 5. Text index (full-text search)
db.articles.createIndex({
  title: "text",
  content: "text"
})
```

**Index Best Practices:**
- Add indexes for all query filters
- Compound index order: Equality → Range → Sort
- Use covering indexes (query + projection in index)
- Use `explain()` to verify index usage
- Monitor with Performance Advisor (Atlas)

## MongoDB Aggregation Pipelines

**Key Operators:** `$match` (filter), `$group` (aggregate), `$lookup` (join), `$unwind` (arrays), `$project` (reshape)

Example aggregation:
```javascript
db.orders.aggregate([
  { $match: { status: "completed", createdAt: { $gte: new Date("2025-01-01") } } },
  { $group: {
      _id: "$userId",
      totalOrders: { $sum: 1 },
      totalRevenue: { $sum: "$totalAmount" }
  }},
  { $sort: { totalRevenue: -1 } },
  { $limit: 10 }
])
```

## DynamoDB Single-Table Design

Design for access patterns using PK/SK patterns. Store multiple entity types in one table with composite keys.

**Example:**
```
PK                    SK                    Attributes
USER#alice            #METADATA             {name: "Alice", email: "..."}
USER#alice            ORDER#2025-01-15      {orderId: "...", total: 99.98}
USER#alice            SESSION#abc123        {expires: "..."}
```

## Firestore Real-Time Patterns

Use `onSnapshot()` for real-time listeners:

```typescript
const unsubscribe = onSnapshot(
  collection(db, "messages"),
  (snapshot) => {
    snapshot.docChanges().forEach((change) => {
      if (change.type === "added") {
        console.log("New message:", change.doc.data())
      }
    })
  }
)
```

## Performance Optimization

**Key practices:**
- Always use indexes for query filters (verify with `.explain()`)
- Use connection pooling (reuse clients across requests)
- Avoid collection scans in production
- Implement pagination for large result sets
- Use transactions for multi-statement operations

## Frontend Integration

- **Forms skill**: Form submission → API validation → Database CRUD (INSERT/UPDATE)
- **Tables skill**: Paginated queries → API → Table display with sorting/filtering
- **Media skill**: MongoDB GridFS for large file storage with metadata
- **AI Chat skill**: MongoDB Atlas Vector Search for semantic conversation retrieval
- **Feedback skill**: DynamoDB for high-throughput event logging with TTL

## Common Patterns

**Pagination:** Use cursor-based pagination for large datasets (recommended over offset)

```javascript
// MongoDB cursor pagination
db.items.find({ _id: { $gt: lastSeenId } }).limit(20)
```

**Soft Deletes:** Mark as deleted with timestamp instead of removing

```javascript
db.users.updateOne(
  { _id: userId },
  { $set: { deletedAt: new Date(), isDeleted: true } }
)
```

**Audit Logs:** Store version history within documents

```javascript
{
  _id: ObjectId("..."),
  currentVersion: 3,
  data: { /* current data */ },
  history: [
    { version: 1, data: { /* v1 */ }, updatedAt: "..." },
    { version: 2, data: { /* v2 */ }, updatedAt: "..." }
  ]
}
```

## Anti-Patterns to Avoid

**Unbounded Arrays:** Limit embedded arrays (use references for large collections)
**Over-Indexing:** Only index queried fields (indexes slow writes)
**DynamoDB Scans:** Always use Query with partition key (avoid Scan)

## Related Skills

- [API Patterns](./api-patterns) - Expose document databases via REST/GraphQL
- [Relational Databases](./databases-relational) - When to use SQL vs NoSQL
- [Real-time Sync](./realtime-sync) - Firestore real-time listeners

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/databases-document)
- MongoDB: https://www.mongodb.com/
- DynamoDB: https://aws.amazon.com/dynamodb/
- Firestore: https://firebase.google.com/docs/firestore
