# MongoDB Performance Optimization

Query optimization, index strategies, and production tuning for document databases.

## Query Optimization

### 1. Use Indexes

```javascript
// Check if query uses index
db.orders.explain("executionStats").find({ status: "pending" })

// Look for:
{
  "executionStats": {
    "executionSuccess": true,
    "nReturned": 100,           // Documents returned
    "totalDocsExamined": 100,   // Should match nReturned
    "executionTimeMillis": 5,
    "stage": "IXSCAN"           // ✓ Index scan (good)
  }
}

// Bad example (no index):
"stage": "COLLSCAN",            // ✗ Collection scan (bad)
"totalDocsExamined": 1000000,   // Scanned all docs
"nReturned": 100,               // Only returned 100
```

**Target:** `totalDocsExamined / nReturned ≈ 1.0`

### 2. Covered Queries

Query entirely satisfied by index (no document fetch):

```javascript
db.users.createIndex({ userId: 1, email: 1, name: 1 })

// Covered query (fast)
db.users.find(
  { userId: 123 },
  { userId: 1, email: 1, name: 1, _id: 0 }  // Only indexed fields
)

// Check explain output:
"totalDocsExamined": 0  // ✓ Zero docs examined (covered)
```

### 3. Projection (Select Only Needed Fields)

```javascript
// ❌ Fetch entire document
db.users.find({ _id: userId })

// ✅ Project only needed fields
db.users.find({ _id: userId }, { email: 1, name: 1 })
```

## Index Performance

### Index Selectivity

**Good indexes** are selective (filter out most documents):

```javascript
// ✓ Good: email (unique, very selective)
db.users.createIndex({ email: 1 })

// ✗ Bad: boolean field (low selectivity)
db.users.createIndex({ isActive: 1 })  // Only 2 values, not helpful
```

### Index Size

```javascript
// Check index sizes
db.users.stats().indexSizes

// Keep indexes in RAM
// Formula: Total index size < Available RAM
```

### Compound Index Prefix

```javascript
db.orders.createIndex({ userId: 1, status: 1, createdAt: -1 })

// Supports:
// { userId }                          ✓
// { userId, status }                  ✓
// { userId, status, createdAt }       ✓

// Does NOT support:
// { status }                          ✗
// { createdAt }                       ✗
// { status, createdAt }               ✗
```

## Connection Pooling

```javascript
const { MongoClient } = require('mongodb');

const client = new MongoClient(uri, {
  maxPoolSize: 10,        // Max connections
  minPoolSize: 2,         // Min connections kept open
  maxIdleTimeMS: 30000,   // Close idle connections after 30s
});
```

**Pool sizing:**
- Web API: 10-20 connections
- Serverless: 1-2 connections + connection pooler (mongos)
- Background workers: 5-10 connections

## Aggregation Optimization

### Pipeline Order

```javascript
// ✓ Optimize: Filter early, limit early
db.orders.aggregate([
  { $match: { status: "completed" } },     // Reduce documents
  { $match: { amount: { $gte: 100 } } },   // Further reduce
  { $sort: { createdAt: -1 } },
  { $limit: 100 },                         // Limit before expensive operations
  { $lookup: { from: "users" } },          // Expensive, but on 100 docs only
])

// ✗ Bad: Expensive operations on all docs
db.orders.aggregate([
  { $lookup: { from: "users" } },          // Join all orders
  { $match: { status: "completed" } },     // Filter after expensive join
  { $limit: 100 },
])
```

### $lookup Performance

```javascript
// Index foreign key
db.users.createIndex({ _id: 1 })  // Usually exists
db.orders.createIndex({ userId: 1 })  // Add if missing

// Limit lookup results
db.orders.aggregate([
  { $lookup: {
      from: "orderItems",
      localField: "_id",
      foreignField: "orderId",
      as: "items",
      pipeline: [
        { $limit: 10 },  // Limit items per order
      ]
  }},
])
```

## Write Performance

### Bulk Inserts

```javascript
// ✓ Batch inserts (10-100x faster)
db.events.insertMany(documents, { ordered: false })

// ✗ Individual inserts (slow)
for (const doc of documents) {
  await db.events.insertOne(doc);
}
```

### Limit Index Count

**Each index slows writes:**
- 0 indexes: Fastest writes, slow reads
- 5 indexes: Balanced
- 10+ indexes: Slow writes, need justification

```javascript
// Check index impact
db.users.stats().indexSizes

// Drop unused indexes
db.users.dropIndex("unused_index_name")
```

## Monitoring Queries

### Enable Profiling

```javascript
// Profile slow queries (>100ms)
db.setProfilingLevel(1, { slowms: 100 })

// View slow queries
db.system.profile.find().sort({ ts: -1 }).limit(10).pretty()

// Disable profiling
db.setProfilingLevel(0)
```

### Query Analysis

```javascript
// Find queries missing indexes
db.system.profile.find({
  "planSummary": { $eq: "COLLSCAN" }
}).limit(10)
```

## Production Tuning

### WiredTiger Cache

```javascript
// Set in mongod.conf
storage:
  wiredTiger:
    engineConfig:
      cacheSizeGB: 4  // 50-80% of available RAM
```

### Read Preference

```javascript
// Distribute reads to replicas
const client = new MongoClient(uri, {
  readPreference: 'secondaryPreferred',  // Read from secondary if available
});
```

### Write Concern

```javascript
// Balance durability vs performance
db.collection.insertOne(doc, {
  writeConcern: {
    w: "majority",  // Wait for majority acknowledgment
    j: true,        // Wait for journal
    wtimeout: 5000  // Timeout after 5s
  }
})
```

## Best Practices

1. **Indexes for all queries** - Avoid collection scans
2. **Explain every query** - Verify index usage
3. **Connection pooling** - Reuse connections
4. **Batch operations** - Use bulkWrite, insertMany
5. **Monitor slow queries** - Set profiling level
6. **Limit document size** - <1MB for performance
7. **Project only needed** - Don't fetch unused fields
8. **Use covered queries** - Index-only access
9. **Pagination** - Use cursor-based, not offset
10. **Regular maintenance** - Monitor index usage, rebuild if needed

## Performance Checklist

- [ ] All queries have supporting indexes
- [ ] Index usage verified with explain()
- [ ] Slow query profiling enabled (>100ms)
- [ ] Connection pool sized appropriately
- [ ] Bulk operations used for batch inserts
- [ ] Documents <1MB (ideally <100KB)
- [ ] Projections used (not fetching all fields)
- [ ] Pagination implemented (cursor-based)
- [ ] Read preference configured for replicas
- [ ] WiredTiger cache sized correctly

## Resources

- MongoDB Performance: https://www.mongodb.com/docs/manual/administration/analyzing-mongodb-performance/
- Query Optimization: https://www.mongodb.com/docs/manual/core/query-optimization/
