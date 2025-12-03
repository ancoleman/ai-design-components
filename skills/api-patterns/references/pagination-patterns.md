# Pagination Patterns

## Overview

Pagination divides large datasets into manageable chunks. This guide covers cursor-based, offset-based, and keyset pagination with implementation examples.

## Table of Contents

- [Cursor-Based Pagination](#cursor-based-pagination)
- [Offset-Based Pagination](#offset-based-pagination)
- [Keyset Pagination](#keyset-pagination)
- [Comparison Matrix](#comparison-matrix)
- [Frontend Integration](#frontend-integration)

## Cursor-Based Pagination

### Advantages

- **Scales to billions of records:** O(1) lookup regardless of dataset size
- **Handles real-time changes:** No skipped or duplicate records when data changes
- **Consistent performance:** No degradation at high page numbers
- **Works with any sortable column:** Not limited to IDs

### Disadvantages

- **No direct page access:** Can't jump to arbitrary page number
- **Stateless cursors required:** Cursor must encode position completely
- **More complex implementation:** Requires cursor encoding/decoding

### When to Use

✅ **Use cursor pagination when:**
- Dataset changes frequently (real-time data)
- Dataset is large (>10,000 records)
- Consistency is critical (no duplicates/skips acceptable)
- Infinite scroll UX pattern
- API will scale to millions of records

❌ **Avoid cursor pagination when:**
- Dataset is small and static
- Direct page number access required
- Implementation complexity not justified

### Implementation (FastAPI)

```python
from fastapi import Query
from typing import Optional
from pydantic import BaseModel

class PaginatedResponse(BaseModel):
    items: list
    next_cursor: Optional[str]
    has_more: bool

@app.get("/items", response_model=PaginatedResponse)
async def list_items(
    cursor: Optional[str] = Query(None, description="Pagination cursor"),
    limit: int = Query(20, ge=1, le=100, description="Items per page")
):
    query = db.query(Item).order_by(Item.id)

    # Apply cursor filter
    if cursor:
        query = query.filter(Item.id > cursor)

    # Fetch limit + 1 to check if more results exist
    items = query.limit(limit + 1).all()

    # Check if there are more results
    has_more = len(items) > limit
    if has_more:
        items = items[:limit]

    # Next cursor is the last item's ID
    next_cursor = items[-1].id if items else None

    return {
        "items": [item.to_dict() for item in items],
        "next_cursor": next_cursor,
        "has_more": has_more
    }
```

### Implementation (Hono)

```typescript
import { Hono } from 'hono'

const app = new Hono()

app.get('/items', async (c) => {
  const cursor = c.req.query('cursor')
  const limit = parseInt(c.req.query('limit') || '20')

  let query = db.select().from(items).orderBy(items.id)

  if (cursor) {
    query = query.where(gt(items.id, cursor))
  }

  const results = await query.limit(limit + 1)

  const hasMore = results.length > limit
  const items = hasMore ? results.slice(0, limit) : results
  const nextCursor = items.length > 0 ? items[items.length - 1].id : null

  return c.json({
    items,
    next_cursor: nextCursor,
    has_more: hasMore
  })
})
```

### Cursor Encoding (Opaque Cursors)

For security and flexibility, encode cursor as base64 JSON:

```python
import base64
import json

def encode_cursor(item_id: str, timestamp: str) -> str:
    """Encode cursor with multiple fields"""
    cursor_data = {
        "id": item_id,
        "timestamp": timestamp
    }
    json_str = json.dumps(cursor_data)
    return base64.b64encode(json_str.encode()).decode()

def decode_cursor(cursor: str) -> dict:
    """Decode cursor back to fields"""
    json_str = base64.b64decode(cursor.encode()).decode()
    return json.loads(json_str)

@app.get("/items")
async def list_items(cursor: Optional[str] = None, limit: int = 20):
    query = db.query(Item).order_by(Item.created_at, Item.id)

    if cursor:
        cursor_data = decode_cursor(cursor)
        query = query.filter(
            (Item.created_at > cursor_data["timestamp"]) |
            ((Item.created_at == cursor_data["timestamp"]) & (Item.id > cursor_data["id"]))
        )

    items = query.limit(limit + 1).all()
    has_more = len(items) > limit
    if has_more:
        items = items[:limit]

    next_cursor = None
    if items:
        last_item = items[-1]
        next_cursor = encode_cursor(last_item.id, last_item.created_at)

    return {
        "items": [item.to_dict() for item in items],
        "next_cursor": next_cursor,
        "has_more": has_more
    }
```

### Multi-Column Sorting

For sorting by multiple columns (e.g., `ORDER BY created_at DESC, id ASC`):

```python
from sqlalchemy import and_, or_

@app.get("/items")
async def list_items(cursor: Optional[str] = None, limit: int = 20):
    query = db.query(Item).order_by(Item.created_at.desc(), Item.id.asc())

    if cursor:
        cursor_data = decode_cursor(cursor)
        # WHERE (created_at < cursor.created_at) OR
        #       (created_at = cursor.created_at AND id > cursor.id)
        query = query.filter(
            or_(
                Item.created_at < cursor_data["timestamp"],
                and_(
                    Item.created_at == cursor_data["timestamp"],
                    Item.id > cursor_data["id"]
                )
            )
        )

    items = query.limit(limit + 1).all()
    # ... rest of implementation
```

## Offset-Based Pagination

### Advantages

- **Simple to implement:** Just `OFFSET` and `LIMIT` in SQL
- **Direct page access:** Can jump to any page number
- **Easy to understand:** Familiar "page 1, 2, 3..." UX

### Disadvantages

- **Poor performance at high offsets:** `OFFSET 1000000` scans 1M rows
- **Inconsistent results:** Skipped/duplicate records when data changes
- **Not scalable:** Performance degrades with dataset size

### When to Use

✅ **Use offset pagination when:**
- Dataset is small (<10,000 records)
- Dataset is static (rarely changes)
- Direct page number access required
- Implementation simplicity critical

❌ **Avoid offset pagination when:**
- Dataset is large or growing
- Data changes frequently
- Performance at scale matters

### Implementation (FastAPI)

```python
from math import ceil

@app.get("/items")
async def list_items(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page")
):
    # Calculate offset
    offset = (page - 1) * per_page

    # Query items
    items = db.query(Item).offset(offset).limit(per_page).all()

    # Get total count (expensive!)
    total = db.query(Item).count()

    return {
        "items": [item.to_dict() for item in items],
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": ceil(total / per_page),
        "has_next": page < ceil(total / per_page),
        "has_prev": page > 1
    }
```

### Performance Optimization

**Problem:** High offset scans many rows:
```sql
SELECT * FROM items OFFSET 1000000 LIMIT 20;
-- Scans 1,000,020 rows to return 20!
```

**Solution:** Use keyset pagination (see below) or limit maximum offset:

```python
MAX_OFFSET = 10000  # Limit to first 10,000 records

@app.get("/items")
async def list_items(page: int = 1, per_page: int = 20):
    offset = (page - 1) * per_page

    if offset > MAX_OFFSET:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum offset is {MAX_OFFSET}. Use cursor pagination for deep pagination."
        )

    # ... rest of implementation
```

## Keyset Pagination

Keyset pagination is a variant of cursor-based pagination using the last seen value directly in the query.

### Implementation

```python
@app.get("/items")
async def list_items(
    last_id: Optional[int] = Query(None, description="ID of last item from previous page"),
    limit: int = Query(20, le=100)
):
    query = db.query(Item).order_by(Item.id)

    if last_id:
        query = query.filter(Item.id > last_id)

    items = query.limit(limit).all()

    return {
        "items": [item.to_dict() for item in items],
        "last_id": items[-1].id if items else None
    }
```

**Advantages over cursor-based:**
- Simpler (no encoding/decoding)
- Transparent to client

**Disadvantages:**
- Exposes database IDs
- Harder to change sort logic
- Can't sort by multiple columns easily

**Recommendation:** Use cursor-based with encoded cursors for production. Use keyset for simple internal APIs.

## Comparison Matrix

| Feature | Cursor-Based | Offset-Based | Keyset |
|---------|--------------|--------------|---------|
| **Performance (small dataset)** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Performance (large dataset)** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Performance at high pages** | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ |
| **Handles real-time changes** | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ |
| **Direct page access** | ❌ | ✅ | ❌ |
| **Implementation complexity** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Security** | ⭐⭐⭐⭐⭐ (opaque) | ⭐⭐⭐⭐ | ⭐⭐⭐ (exposes IDs) |
| **Flexibility** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

## Frontend Integration

### React + Cursor Pagination

```typescript
import { useState, useEffect } from 'react'

interface PaginatedResponse<T> {
  items: T[]
  next_cursor: string | null
  has_more: boolean
}

function useInfiniteScroll<T>(endpoint: string) {
  const [items, setItems] = useState<T[]>([])
  const [cursor, setCursor] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [hasMore, setHasMore] = useState(true)

  const loadMore = async () => {
    if (loading || !hasMore) return

    setLoading(true)

    const url = cursor
      ? `${endpoint}?cursor=${cursor}&limit=20`
      : `${endpoint}?limit=20`

    const response = await fetch(url)
    const data: PaginatedResponse<T> = await response.json()

    setItems(prev => [...prev, ...data.items])
    setCursor(data.next_cursor)
    setHasMore(data.has_more)
    setLoading(false)
  }

  return { items, loadMore, loading, hasMore }
}

// Usage
function ItemList() {
  const { items, loadMore, loading, hasMore } = useInfiniteScroll('/api/items')

  return (
    <div>
      {items.map(item => (
        <div key={item.id}>{item.name}</div>
      ))}

      {hasMore && (
        <button onClick={loadMore} disabled={loading}>
          {loading ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  )
}
```

### React + Offset Pagination

```typescript
import { useState, useEffect } from 'react'

interface OffsetPaginatedResponse<T> {
  items: T[]
  page: number
  per_page: number
  total: number
  total_pages: number
}

function usePagination<T>(endpoint: string) {
  const [items, setItems] = useState<T[]>([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [loading, setLoading] = useState(false)

  const loadPage = async (pageNum: number) => {
    setLoading(true)

    const response = await fetch(`${endpoint}?page=${pageNum}&per_page=20`)
    const data: OffsetPaginatedResponse<T> = await response.json()

    setItems(data.items)
    setPage(data.page)
    setTotalPages(data.total_pages)
    setLoading(false)
  }

  useEffect(() => {
    loadPage(page)
  }, [page])

  return {
    items,
    page,
    totalPages,
    loading,
    goToPage: setPage,
    nextPage: () => setPage(p => Math.min(p + 1, totalPages)),
    prevPage: () => setPage(p => Math.max(p - 1, 1))
  }
}

// Usage
function ItemList() {
  const { items, page, totalPages, loading, goToPage, nextPage, prevPage } =
    usePagination('/api/items')

  return (
    <div>
      {items.map(item => (
        <div key={item.id}>{item.name}</div>
      ))}

      <div>
        <button onClick={prevPage} disabled={page === 1 || loading}>
          Previous
        </button>

        <span>Page {page} of {totalPages}</span>

        <button onClick={nextPage} disabled={page === totalPages || loading}>
          Next
        </button>
      </div>
    </div>
  )
}
```

### Integration with TanStack Table

See tables skill for integration with table virtualization and sorting.

```typescript
import { useInfiniteQuery } from '@tanstack/react-query'
import { useVirtualizer } from '@tanstack/react-virtual'

async function fetchItems({ pageParam = null }) {
  const url = pageParam
    ? `/api/items?cursor=${pageParam}&limit=50`
    : '/api/items?limit=50'

  const response = await fetch(url)
  return response.json()
}

function VirtualizedTable() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage
  } = useInfiniteQuery({
    queryKey: ['items'],
    queryFn: fetchItems,
    getNextPageParam: (lastPage) => lastPage.next_cursor
  })

  const allItems = data?.pages.flatMap(page => page.items) ?? []

  // Virtualization setup
  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: allItems.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
    overscan: 5
  })

  // Load more when scrolled near bottom
  useEffect(() => {
    const [lastItem] = [...virtualizer.getVirtualItems()].reverse()

    if (
      lastItem &&
      lastItem.index >= allItems.length - 1 &&
      hasNextPage &&
      !isFetchingNextPage
    ) {
      fetchNextPage()
    }
  }, [virtualizer.getVirtualItems(), hasNextPage, isFetchingNextPage])

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map(virtualRow => {
          const item = allItems[virtualRow.index]
          return (
            <div
              key={virtualRow.key}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: `${virtualRow.size}px`,
                transform: `translateY(${virtualRow.start}px)`
              }}
            >
              {item.name}
            </div>
          )
        })}
      </div>
    </div>
  )
}
```

## Database Indexing

For optimal pagination performance, ensure proper indexing:

```sql
-- Cursor pagination on ID
CREATE INDEX idx_items_id ON items(id);

-- Cursor pagination on created_at + id
CREATE INDEX idx_items_created_id ON items(created_at DESC, id ASC);

-- Offset pagination (less important but helpful)
CREATE INDEX idx_items_id ON items(id);
```

## Best Practices Summary

1. **Use cursor pagination for production APIs** - Scales better, handles real-time data
2. **Encode cursors as opaque tokens** - Security and flexibility
3. **Return `has_more` flag** - Avoids extra count query
4. **Limit maximum page size** - Prevent resource exhaustion (max 100 items)
5. **Index sort columns** - Essential for performance
6. **Document pagination in OpenAPI** - Include cursor/page parameters
7. **Consistent ordering** - Always include tiebreaker (ID) for deterministic results
8. **Cache count queries** - For offset pagination, cache total count
9. **Avoid `COUNT(*)` when possible** - Expensive on large tables
10. **Use virtualization on frontend** - For smooth infinite scroll experience

## Migration Path

**From offset to cursor pagination:**

1. Support both simultaneously with different endpoints or parameters
2. Deprecate offset version over time
3. Provide migration guide for API consumers

```python
@app.get("/items")
async def list_items(
    # Cursor-based (new)
    cursor: Optional[str] = None,
    # Offset-based (deprecated)
    page: Optional[int] = None,
    per_page: int = 20
):
    if page is not None:
        # Offset-based (deprecated)
        warnings.warn("Offset pagination is deprecated. Use cursor parameter.", DeprecationWarning)
        return offset_paginate(page, per_page)
    else:
        # Cursor-based (recommended)
        return cursor_paginate(cursor, per_page)
```
