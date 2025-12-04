# Common MongoDB Patterns

Frequently-used patterns for pagination, soft deletes, audit logs, and data modeling.

## Pagination Patterns

### Cursor-Based (Recommended)

**Handles real-time changes, no skipped records:**

```javascript
// First page
db.posts.find({})
  .sort({ _id: -1 })
  .limit(20)

// Next page (using last _id as cursor)
db.posts.find({ _id: { $lt: lastSeenId } })
  .sort({ _id: -1 })
  .limit(20)
```

**API response:**
```javascript
{
  "items": [...],
  "nextCursor": "507f1f77bcf86cd799439011",
  "hasMore": true
}
```

### Offset-Based (Simple Cases)

**Only for static datasets <10K records:**

```javascript
const page = 2;
const perPage = 20;

db.posts.find({})
  .sort({ createdAt: -1 })
  .skip(page * perPage)
  .limit(perPage)
```

**Problem:** Performance degrades with large skip values.

### Range-Based (Time Series)

```javascript
// Page by date range
db.events.find({
  createdAt: {
    $gte: ISODate("2025-12-01"),
    $lt: ISODate("2025-12-02")
  }
})
```

## Soft Deletes

### Pattern 1: Boolean Flag

```javascript
// Schema
{
  _id: ObjectId("..."),
  email: "user@example.com",
  deletedAt: null,  // or ISODate("...")
  isDeleted: false,
}

// Soft delete
db.users.updateOne(
  { _id: userId },
  { $set: { isDeleted: true, deletedAt: new Date() } }
)

// Query (exclude deleted)
db.users.find({ isDeleted: { $ne: true } })

// Create index for efficient querying
db.users.createIndex({ isDeleted: 1, createdAt: -1 })
```

### Pattern 2: Status Field

```javascript
// Schema with status
{
  _id: ObjectId("..."),
  status: "active",  // active | archived | deleted
  statusChangedAt: ISODate("..."),
}

// Archive (soft delete)
db.posts.updateOne(
  { _id: postId },
  { $set: { status: "archived", statusChangedAt: new Date() } }
)

// Query active only
db.posts.find({ status: "active" })

// Index
db.posts.createIndex({ status: 1, createdAt: -1 })
```

## Audit Logs

### Pattern 1: Embedded History

```javascript
{
  _id: ObjectId("..."),
  email: "user@example.com",
  name: "John Doe",
  history: [
    {
      action: "created",
      timestamp: ISODate("2025-01-01T00:00:00Z"),
      by: ObjectId("admin_id"),
    },
    {
      action: "updated",
      timestamp: ISODate("2025-02-01T00:00:00Z"),
      by: ObjectId("user_id"),
      changes: { name: { old: "John", new: "John Doe" } },
    },
  ],
}
```

**Use when:** <100 updates per document

### Pattern 2: Separate Audit Collection

```javascript
// Main collection
db.users.updateOne({ _id: userId }, { $set: { name: "New Name" } })

// Audit log collection
db.audit_log.insertOne({
  collection: "users",
  documentId: userId,
  action: "update",
  changes: { name: { old: "John", new: "New Name" } },
  userId: currentUserId,
  timestamp: new Date(),
  ip: "192.168.1.1",
})
```

**Use when:** Many updates, need queryable audit history

## Versioning Documents

### Pattern: Version Number + History

```javascript
{
  _id: ObjectId("..."),
  version: 3,
  content: "Current content",
  versions: [
    { version: 1, content: "Original", createdAt: ISODate("...") },
    { version: 2, content: "Updated", createdAt: ISODate("...") },
    { version: 3, content: "Current content", createdAt: ISODate("...") },
  ],
}

// Update with versioning
db.documents.updateOne(
  { _id: docId },
  {
    $inc: { version: 1 },
    $set: { content: newContent },
    $push: {
      versions: {
        version: currentVersion + 1,
        content: newContent,
        createdAt: new Date(),
      }
    }
  }
)
```

## Counter Pattern (Atomic Increments)

```javascript
// Page view counter
db.posts.updateOne(
  { _id: postId },
  { $inc: { views: 1 } }
)

// Multiple counters
db.posts.updateOne(
  { _id: postId },
  {
    $inc: { views: 1, shares: 1 },
    $set: { lastViewed: new Date() }
  }
)
```

## Hierarchical Data

### Pattern 1: Parent Reference

```javascript
// Category tree
{
  _id: ObjectId("..."),
  name: "Electronics",
  parentId: null,  // Root category
}

{
  _id: ObjectId("..."),
  name: "Laptops",
  parentId: ObjectId("electronics_id"),  // Child
}

// Find all children
db.categories.find({ parentId: electronicsId })

// Find path to root
function getPath(categoryId) {
  const path = [];
  let current = db.categories.findOne({ _id: categoryId });

  while (current) {
    path.unshift(current.name);
    current = current.parentId ?
      db.categories.findOne({ _id: current.parentId }) :
      null;
  }

  return path;
}
```

### Pattern 2: Materialized Path

```javascript
{
  _id: ObjectId("..."),
  name: "Laptops",
  path: "Electronics,Computers,Laptops",  // Full path
}

// Find all descendants
db.categories.find({ path: /^Electronics,Computers/ })

// Index for performance
db.categories.createIndex({ path: 1 })
```

## Upsert Pattern

```javascript
// Insert if not exists, update if exists
db.users.updateOne(
  { email: "user@example.com" },
  {
    $set: { name: "John", lastLogin: new Date() },
    $setOnInsert: { createdAt: new Date() },  // Only on insert
  },
  { upsert: true }
)
```

## Bulk Operations

```javascript
// Batch inserts (faster than individual)
db.users.insertMany([
  { email: "user1@example.com", name: "User 1" },
  { email: "user2@example.com", name: "User 2" },
  // ... thousands more
], { ordered: false })  // Continue on error

// Bulk write operations
db.users.bulkWrite([
  {
    insertOne: {
      document: { email: "new@example.com", name: "New User" }
    }
  },
  {
    updateOne: {
      filter: { _id: ObjectId("...") },
      update: { $set: { name: "Updated" } }
    }
  },
  {
    deleteOne: {
      filter: { _id: ObjectId("...") }
    }
  }
])
```

## Caching Pattern

```javascript
// Cache frequently accessed data
db.users.aggregate([
  { $match: { _id: userId } },
  { $lookup: {
      from: "posts",
      localField: "_id",
      foreignField: "userId",
      as: "recentPosts",
      pipeline: [
        { $sort: { createdAt: -1 } },
        { $limit: 5 }
      ]
  }},
  { $project: {
      email: 1,
      name: 1,
      postCount: { $size: "$recentPosts" },
      recentPosts: { $slice: ["$recentPosts", 3] }
  }},
  { $merge: {
      into: "user_cache",
      whenMatched: "replace",
      whenNotMatched: "insert"
  }}
])
```

## Best Practices

1. **Index all queries** - Every filter should have supporting index
2. **Compound index order** - Equality, Range, Sort
3. **Use partial indexes** - Index only needed subset
4. **Cursor pagination** - Avoid skip for large offsets
5. **Soft deletes** - Preserve data, add isDeleted flag
6. **Audit critical changes** - Log who/what/when
7. **Version important docs** - Maintain history
8. **Use upserts** - Idempotent operations
9. **Bulk operations** - Batch for performance
10. **Monitor slow queries** - Enable profiling

## Resources

- MongoDB Schema Design: https://www.mongodb.com/docs/manual/core/data-modeling-introduction/
- Index Best Practices: https://www.mongodb.com/docs/manual/applications/indexes/
