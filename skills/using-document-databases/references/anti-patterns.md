# MongoDB Anti-Patterns

Common mistakes and how to avoid them.


## Table of Contents

- [1. Unbounded Arrays](#1-unbounded-arrays)
- [2. Over-Embedding](#2-over-embedding)
- [3. Collection Scans](#3-collection-scans)
- [4. Large Documents (>1MB)](#4-large-documents-1mb)
- [5. Inefficient $lookup](#5-inefficient-lookup)
- [6. Massive Projections](#6-massive-projections)
- [7. Client-Side Joins](#7-client-side-joins)
- [8. Unbounded $group](#8-unbounded-group)
- [9. No Error Handling](#9-no-error-handling)
- [10. Wrong Data Types](#10-wrong-data-types)
- [Summary of Best Practices](#summary-of-best-practices)
- [Resources](#resources)

## 1. Unbounded Arrays

❌ **Problem:**
```javascript
{
  _id: ObjectId("..."),
  userId: 123,
  events: [
    { type: "login", timestamp: "..." },
    { type: "click", timestamp: "..." },
    // ... 10,000 more events (document grows forever)
  ]
}
```

✅ **Solution:** Use separate collection with reference

```javascript
// User document (bounded)
{ _id: ObjectId("..."), userId: 123, email: "..." }

// Events collection
{ _id: ObjectId("..."), userId: 123, type: "login", timestamp: "..." }

// Query recent events
db.events.find({ userId: 123 }).sort({ timestamp: -1 }).limit(100)
```

**Rule:** Arrays with potential for >100 elements should be separate collections.

## 2. Over-Embedding

❌ **Problem:**
```javascript
{
  _id: ObjectId("..."),
  title: "Blog Post",
  author: {
    _id: ObjectId("..."),
    name: "John",
    email: "john@example.com",
    bio: "Long biography...",
    socialLinks: [...],  // Embedded author data duplicated in every post
  },
  comments: [
    {
      author: { /* full author embedded again */ },
      replies: [
        { author: { /* embedded again */ } }  // Deeply nested
      ]
    }
  ]
}
```

✅ **Solution:** Reference pattern

```javascript
// Post (minimal author info)
{
  _id: ObjectId("..."),
  title: "Blog Post",
  authorId: ObjectId("author_id"),  // Reference only
  authorName: "John",  // Denormalize only display name
}

// Fetch author details when needed
const post = db.posts.findOne({ _id: postId })
const author = db.users.findOne({ _id: post.authorId })
```

## 3. Collection Scans

❌ **Problem:**
```javascript
// No index on status
db.orders.find({ status: "pending" })  // COLLSCAN on 1M documents
```

✅ **Solution:** Create index

```javascript
db.orders.createIndex({ status: 1, createdAt: -1 })
db.orders.find({ status: "pending" })  // IXSCAN
```

## 4. Large Documents (>1MB)

❌ **Problem:**
```javascript
{
  _id: ObjectId("..."),
  productId: 123,
  largeImage: "<base64 encoded 5MB image>",  // 16MB doc limit approaching
}
```

✅ **Solution:** Use GridFS or external storage

```javascript
// Reference S3/GridFS
{
  _id: ObjectId("..."),
  productId: 123,
  imageUrl: "https://cdn.example.com/products/123.jpg",
  thumbnailUrl: "https://cdn.example.com/products/123_thumb.jpg",
}
```

## 5. Inefficient $lookup

❌ **Problem:**
```javascript
// $lookup without index on foreign key
db.orders.aggregate([
  { $lookup: {
      from: "users",  // No index on users._id
      localField: "userId",
      foreignField: "_id",
      as: "user"
  }}
])
```

✅ **Solution:** Index foreign keys

```javascript
// Create index on lookup field
db.users.createIndex({ _id: 1 })  // Usually exists by default

// Or denormalize frequently accessed fields
{
  _id: ObjectId("..."),
  userId: 123,
  userName: "John",  // Denormalized for display
  userEmail: "john@example.com",
}
```

## 6. Massive Projections

❌ **Problem:**
```javascript
// Selecting all fields when only need few
db.users.find({}, { password: 0 })  // Returns everything except password
```

✅ **Solution:** Explicit projection

```javascript
// Select only needed fields
db.users.find({}, { email: 1, name: 1, _id: 0 })

// Covering index (no document fetch)
db.users.createIndex({ email: 1, name: 1 })
db.users.find({}, { email: 1, name: 1, _id: 0 })
```

## 7. Client-Side Joins

❌ **Problem:**
```javascript
// N+1 queries
const posts = await db.posts.find({}).toArray();

for (const post of posts) {
  post.author = await db.users.findOne({ _id: post.authorId });  // N queries!
}
```

✅ **Solution:** Aggregation or denormalization

```javascript
// Aggregation (server-side join)
db.posts.aggregate([
  { $lookup: {
      from: "users",
      localField: "authorId",
      foreignField: "_id",
      as: "author"
  }},
  { $unwind: "$author" },
])

// Or denormalize
{
  _id: ObjectId("..."),
  authorId: ObjectId("..."),
  authorName: "John",  // Cached for display
}
```

## 8. Unbounded $group

❌ **Problem:**
```javascript
// Group by high-cardinality field
db.events.aggregate([
  { $group: {
      _id: "$userId",  // Millions of unique users
      events: { $push: "$$ROOT" }  // Massive memory usage
  }}
])
```

✅ **Solution:** Add $match and $limit

```javascript
db.events.aggregate([
  { $match: { timestamp: { $gte: recentDate } } },  // Filter first
  { $group: { _id: "$userId", count: { $sum: 1 } } },  // Don't $push all docs
  { $limit: 1000 },  // Limit results
])
```

## 9. No Error Handling

❌ **Problem:**
```javascript
const user = await db.users.insertOne({ email: "duplicate@example.com" });
// Throws on duplicate email if unique index exists
```

✅ **Solution:** Handle errors

```javascript
try {
  const user = await db.users.insertOne({ email: "user@example.com" });
} catch (error) {
  if (error.code === 11000) {  // Duplicate key error
    throw new Error("Email already exists");
  }
  throw error;
}
```

## 10. Wrong Data Types

❌ **Problem:**
```javascript
{
  createdAt: "2025-12-03T10:00:00Z",  // String, not Date
  price: "49.99",  // String, not Number
  isActive: "true",  // String, not Boolean
}
```

✅ **Solution:** Use proper types

```javascript
{
  createdAt: ISODate("2025-12-03T10:00:00Z"),  // Date object
  price: 49.99,  // Number
  isActive: true,  // Boolean
}
```

## Summary of Best Practices

✅ **DO:**
- Reference for one-to-many (>100 related docs)
- Index all query filters
- Use cursor-based pagination
- Implement soft deletes for important data
- Denormalize display fields
- Use proper data types
- Handle errors explicitly
- Limit array sizes (<100 elements)
- Use aggregation for complex queries
- Monitor slow queries

❌ **DON'T:**
- Embed unbounded arrays
- Do client-side joins (N+1 queries)
- Skip indexing query fields
- Store large binary data in documents
- Use offset pagination for large datasets
- Store strings when you need dates/numbers
- Ignore 16MB document limit
- Over-normalize (too many $lookups)
- Create 10+ indexes per collection
- Use $regex without index

## Resources

- MongoDB Anti-Patterns: https://www.mongodb.com/developer/products/mongodb/schema-design-anti-pattern-summary/
