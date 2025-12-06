# MongoDB Aggregation Pipeline Patterns

Complete guide to MongoDB aggregation framework for complex queries, analytics, and data transformations.


## Table of Contents

- [Aggregation Pipeline Basics](#aggregation-pipeline-basics)
- [Core Stages](#core-stages)
  - [$match (Filter)](#match-filter)
  - [$group (Aggregate)](#group-aggregate)
  - [$project (Reshape)](#project-reshape)
  - [$lookup (Join)](#lookup-join)
  - [$unwind (Flatten Arrays)](#unwind-flatten-arrays)
- [Common Patterns](#common-patterns)
  - [Top N per Category](#top-n-per-category)
  - [Time-Based Aggregation](#time-based-aggregation)
  - [Moving Average](#moving-average)
  - [Pagination](#pagination)
- [Advanced Patterns](#advanced-patterns)
  - [Faceted Search](#faceted-search)
  - [Full-Text Search + Aggregation](#full-text-search-aggregation)
  - [Conditional Aggregation](#conditional-aggregation)
- [Performance Optimization](#performance-optimization)
  - [Index Usage](#index-usage)
  - [$match and $project Early](#match-and-project-early)
  - [Limit Result Size](#limit-result-size)
- [Pipeline Validation](#pipeline-validation)
- [Best Practices](#best-practices)
- [Resources](#resources)

## Aggregation Pipeline Basics

Pipeline stages process documents sequentially:

```javascript
db.collection.aggregate([
  { $match: { status: "active" } },      // Filter
  { $group: { _id: "$category" } },      // Group
  { $sort: { count: -1 } },              // Sort
  { $limit: 10 },                        // Limit
])
```

## Core Stages

### $match (Filter)

```javascript
// Filter before expensive operations
db.orders.aggregate([
  { $match: {
      status: "completed",
      createdAt: { $gte: ISODate("2025-01-01") }
  }},
  // ... other stages
])
```

**Best practice:** Use $match early to reduce document count.

### $group (Aggregate)

```javascript
// Revenue by category
db.orders.aggregate([
  { $group: {
      _id: "$category",
      totalRevenue: { $sum: "$amount" },
      avgOrder: { $avg: "$amount" },
      count: { $sum: 1 },
      maxOrder: { $max: "$amount" },
      minOrder: { $min: "$amount" },
  }},
])
```

**Accumulators:** `$sum`, `$avg`, `$max`, `$min`, `$first`, `$last`, `$push`, `$addToSet`

### $project (Reshape)

```javascript
// Select and transform fields
db.users.aggregate([
  { $project: {
      fullName: { $concat: ["$firstName", " ", "$lastName"] },
      email: 1,  // Include field
      _id: 0,    // Exclude field
      ageGroup: {
        $cond: {
          if: { $gte: ["$age", 18] },
          then: "adult",
          else: "minor"
        }
      }
  }},
])
```

### $lookup (Join)

```javascript
// Join orders with users
db.orders.aggregate([
  { $lookup: {
      from: "users",
      localField: "userId",
      foreignField: "_id",
      as: "user"
  }},
  { $unwind: "$user" },  // Flatten array
])
```

### $unwind (Flatten Arrays)

```javascript
// Expand array elements into separate documents
db.posts.aggregate([
  { $unwind: "$tags" },  // Create one doc per tag
  { $group: {
      _id: "$tags",
      count: { $sum: 1 }
  }},
])
```

## Common Patterns

### Top N per Category

```javascript
// Top 3 products per category
db.products.aggregate([
  { $sort: { category: 1, sales: -1 } },
  { $group: {
      _id: "$category",
      products: { $push: "$$ROOT" },
  }},
  { $project: {
      category: "$_id",
      topProducts: { $slice: ["$products", 3] }
  }},
])
```

### Time-Based Aggregation

```javascript
// Daily revenue
db.orders.aggregate([
  { $match: {
      createdAt: { $gte: ISODate("2025-11-01") }
  }},
  { $group: {
      _id: {
        $dateToString: { format: "%Y-%m-%d", date: "$createdAt" }
      },
      revenue: { $sum: "$amount" },
      orders: { $sum: 1 },
  }},
  { $sort: { _id: 1 } },
])
```

### Moving Average

```javascript
// 7-day moving average
db.metrics.aggregate([
  { $setWindowFields: {
      sortBy: { date: 1 },
      output: {
        movingAvg: {
          $avg: "$value",
          window: { documents: [-6, 0] }  // Current + 6 previous
        }
      }
  }},
])
```

### Pagination

```javascript
// Efficient pagination
db.products.aggregate([
  { $match: { category: "electronics" } },
  { $sort: { createdAt: -1 } },
  { $skip: 20 },   // Page 2 (skip 20)
  { $limit: 10 },  // 10 per page
])

// Total count for pagination
db.products.aggregate([
  { $match: { category: "electronics" } },
  { $facet: {
      items: [
        { $skip: 20 },
        { $limit: 10 },
      ],
      totalCount: [
        { $count: "count" },
      ],
  }},
])
```

## Advanced Patterns

### Faceted Search

```javascript
// Multiple aggregations in one query
db.products.aggregate([
  { $match: { price: { $lte: 1000 } } },
  { $facet: {
      byCategory: [
        { $group: { _id: "$category", count: { $sum: 1 } } },
        { $sort: { count: -1 } },
      ],
      byBrand: [
        { $group: { _id: "$brand", count: { $sum: 1 } } },
        { $sort: { count: -1 } },
      ],
      priceRanges: [
        { $bucket: {
            groupBy: "$price",
            boundaries: [0, 100, 500, 1000],
            default: "Other",
            output: { count: { $sum: 1 } }
        }},
      ],
  }},
])
```

### Full-Text Search + Aggregation

```javascript
db.articles.aggregate([
  { $match: { $text: { $search: "mongodb aggregation" } } },
  { $addFields: {
      score: { $meta: "textScore" }
  }},
  { $sort: { score: -1 } },
  { $limit: 10 },
])
```

### Conditional Aggregation

```javascript
// Revenue by payment method
db.orders.aggregate([
  { $group: {
      _id: null,
      creditCardRevenue: {
        $sum: { $cond: [
          { $eq: ["$paymentMethod", "credit_card"] },
          "$amount",
          0
        ]}
      },
      paypalRevenue: {
        $sum: { $cond: [
          { $eq: ["$paymentMethod", "paypal"] },
          "$amount",
          0
        ]}
      },
  }},
])
```

## Performance Optimization

### Index Usage

```javascript
// Use indexes for $match and $sort
db.orders.createIndex({ status: 1, createdAt: -1 });

db.orders.aggregate([
  { $match: { status: "active" } },  // Uses index
  { $sort: { createdAt: -1 } },      // Uses index
  // ... other stages
])

// Check index usage
db.orders.explain().aggregate([...])
```

### $match and $project Early

```javascript
// ✅ Good: Filter and project early
db.large_collection.aggregate([
  { $match: { active: true } },           // Reduce documents
  { $project: { needed_field: 1 } },      // Reduce field count
  { $lookup: ... },                       // Expensive operation on smaller dataset
])

// ❌ Bad: Expensive operations on full collection
db.large_collection.aggregate([
  { $lookup: ... },                       // Processes all documents
  { $match: { active: true } },           // Filter after expensive operation
])
```

### Limit Result Size

```javascript
// Limit intermediate results
db.products.aggregate([
  { $match: { inStock: true } },
  { $sort: { popularity: -1 } },
  { $limit: 100 },                  // Limit before expensive stages
  { $lookup: { /* join details */ } },
])
```

## Pipeline Validation

```javascript
// Use $merge for debugging
db.orders.aggregate([
  { $match: { status: "pending" } },
  { $merge: { into: "debug_stage1" } },  // Save intermediate result
  { $group: { _id: "$userId", total: { $sum: "$amount" } } },
  { $merge: { into: "debug_stage2" } },
])
```

## Best Practices

1. **$match early** - Filter before expensive operations
2. **Use indexes** - Ensure $match and $sort use indexes
3. **$project unwanted fields** - Reduce memory usage
4. **Limit results** - Use $limit early when possible
5. **Avoid $lookup on large collections** - Index foreign keys
6. **Test with explain()** - Verify index usage
7. **Use $facet sparingly** - Multiple sub-pipelines are expensive
8. **Consider denormalization** - Avoid $lookup for frequent queries

## Resources

- MongoDB Aggregation Docs: https://www.mongodb.com/docs/manual/aggregation/
- Aggregation Pipeline Operators: https://www.mongodb.com/docs/manual/reference/operator/aggregation/
