# MongoDB Indexing Strategies

Complete guide to index types, optimization, and best practices for document databases.

## Index Types

### Single Field Index

```javascript
db.users.createIndex({ email: 1 }, { unique: true })  // Ascending
db.posts.createIndex({ createdAt: -1 })              // Descending
```

### Compound Index

**Order matters!** Equality → Range → Sort

```javascript
// Query: WHERE status = 'active' AND createdAt > date ORDER BY createdAt
db.orders.createIndex({ status: 1, createdAt: -1 })

// Query: WHERE userId = 123 AND status = 'active' ORDER BY createdAt
db.orders.createIndex({ userId: 1, status: 1, createdAt: -1 })
```

### Text Index (Full-Text Search)

```javascript
db.articles.createIndex({
  title: "text",
  content: "text",
  tags: "text"
}, {
  weights: { title: 3, content: 1, tags: 2 },  // Title 3x more important
  name: "article_text_index"
})

// Search
db.articles.find({ $text: { $search: "mongodb indexing" } })
  .sort({ score: { $meta: "textScore" } })
```

### Geospatial Index

```javascript
db.locations.createIndex({ location: "2dsphere" })

// Find nearby
db.locations.find({
  location: {
    $near: {
      $geometry: { type: "Point", coordinates: [-73.97, 40.77] },
      $maxDistance: 5000,  // 5km
    }
  }
})
```

### Partial Index (Index Subset)

```javascript
// Only index active users
db.users.createIndex(
  { email: 1 },
  { partialFilterExpression: { status: { $eq: "active" } } }
)

// Only index large orders
db.orders.createIndex(
  { userId: 1, createdAt: -1 },
  { partialFilterExpression: { amount: { $gte: 1000 } } }
)
```

### TTL Index (Auto-Delete)

```javascript
// Auto-delete sessions after 30 days
db.sessions.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 2592000 }  // 30 days
)
```

### Sparse Index

```javascript
// Only index documents with field
db.users.createIndex({ phone: 1 }, { sparse: true })
```

## Index Selection Rules

**Compound index order:**
1. Equality filters first
2. Range filters second
3. Sort fields last

```javascript
// Query: status = X AND createdAt > Y ORDER BY createdAt
// Index: { status: 1, createdAt: -1 }  ✓ Correct order
// Index: { createdAt: -1, status: 1 }  ✗ Wrong order
```

## Covering Indexes

Index includes all queried fields (no document fetch needed):

```javascript
// Query needs: userId, createdAt, amount
db.orders.createIndex({ userId: 1, createdAt: -1, amount: 1 })

// Query
db.orders.find(
  { userId: 123 },
  { userId: 1, createdAt: 1, amount: 1, _id: 0 }  // Only indexed fields
).sort({ createdAt: -1 })

// COVERED - no document fetch!
```

## Performance Optimization

### Index Intersection

MongoDB can combine multiple indexes:

```javascript
db.orders.createIndex({ userId: 1 })
db.orders.createIndex({ status: 1 })

// MongoDB automatically intersects indexes
db.orders.find({ userId: 123, status: "pending" })
```

### Index Prefix Usage

Compound indexes can support prefix queries:

```javascript
db.orders.createIndex({ userId: 1, status: 1, createdAt: -1 })

// Supports queries on:
// { userId }
// { userId, status }
// { userId, status, createdAt }

// Does NOT support:
// { status }
// { createdAt }
```

## Monitoring and Analysis

### List Indexes

```javascript
db.collection.getIndexes()
```

### Index Usage Stats

```javascript
db.collection.aggregate([{ $indexStats: {} }])
```

### Explain Query

```javascript
db.orders.explain("executionStats").find({ userId: 123 })

// Check for:
// - "stage": "IXSCAN" (good - uses index)
// - "stage": "COLLSCAN" (bad - full collection scan)
// - "totalDocsExamined" should be close to "nReturned"
```

### Slow Query Log

```javascript
// Enable profiling
db.setProfilingLevel(1, { slowms: 100 })  // Log queries >100ms

// View slow queries
db.system.profile.find().sort({ ts: -1 }).limit(10)
```

## Index Maintenance

### Rebuild Index

```javascript
db.collection.reIndex()  // Rebuilds all indexes
```

### Drop Unused Indexes

```javascript
// Find unused indexes
db.collection.aggregate([{ $indexStats: {} }])

// Drop index
db.collection.dropIndex("index_name")
```

## Best Practices

1. **Index queried fields** - Every filter/sort should have index
2. **Compound index order** - Equality, Range, Sort
3. **Use covering indexes** - Avoid document fetches
4. **Partial indexes** - Index only needed subset
5. **Monitor index usage** - Drop unused indexes
6. **Limit index count** - Each index slows writes
7. **Use explain()** - Verify index usage
8. **Index foreign keys** - For $lookup performance
9. **TTL indexes** - Auto-cleanup for temp data
10. **Text indexes** - One per collection max

## Anti-Patterns

❌ **Over-indexing** - 10+ indexes per collection slows writes
❌ **Wrong compound order** - Range before equality
❌ **No index on filters** - Collection scans on large data
❌ **Index low-cardinality** - Boolean fields rarely help
❌ **Ignore index size** - Indexes consume RAM

## Resources

- MongoDB Indexes: https://www.mongodb.com/docs/manual/indexes/
- Index Performance: https://www.mongodb.com/docs/manual/core/index-performance/
