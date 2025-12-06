# Table Performance Optimization


## Table of Contents

- [Performance Tier Overview](#performance-tier-overview)
  - [Tier 1: Client-Side Operations (<1,000 rows)](#tier-1-client-side-operations-1000-rows)
  - [Tier 2: Server-Side Operations (1,000-10,000 rows)](#tier-2-server-side-operations-1000-10000-rows)
  - [Tier 3: Virtual Scrolling (10,000-100,000 rows)](#tier-3-virtual-scrolling-10000-100000-rows)
  - [Tier 4: Extreme Scale (100,000+ rows)](#tier-4-extreme-scale-100000-rows)
- [Rendering Optimizations](#rendering-optimizations)
  - [Reduce React Re-renders](#reduce-react-re-renders)
  - [Batch DOM Updates](#batch-dom-updates)
  - [CSS-based Optimizations](#css-based-optimizations)
- [Memory Management](#memory-management)
  - [Prevent Memory Leaks](#prevent-memory-leaks)
  - [Efficient Data Structures](#efficient-data-structures)
- [Network Optimizations](#network-optimizations)
  - [Request Deduplication](#request-deduplication)
  - [Response Compression](#response-compression)
- [Benchmarking Tools](#benchmarking-tools)
  - [Performance Measurement](#performance-measurement)
  - [React DevTools Profiler](#react-devtools-profiler)
- [Common Performance Pitfalls](#common-performance-pitfalls)
  - [❌ Avoid These Patterns](#avoid-these-patterns)
- [Performance Checklist](#performance-checklist)

## Performance Tier Overview

### Tier 1: Client-Side Operations (<1,000 rows)

All data loaded and processed in the browser.

**Optimization Techniques:**
- Use `React.memo()` to prevent unnecessary re-renders
- Memoize filtered/sorted data with `useMemo()`
- Debounce search inputs (300ms typical)
- Virtualize if approaching 1,000 rows
- Use CSS for hover/selection states (not JS)

**Example optimization:**
```javascript
const MemoizedTable = React.memo(({ data, columns }) => {
  const sortedData = useMemo(
    () => data.sort((a, b) => a.name.localeCompare(b.name)),
    [data]
  );

  const filteredData = useMemo(
    () => sortedData.filter(row => row.active),
    [sortedData, filterValue]
  );

  return <Table data={filteredData} columns={columns} />;
});
```

**Performance Metrics:**
- Initial render: <100ms
- Re-sort: <50ms
- Re-filter: <50ms
- Scroll: 60fps

### Tier 2: Server-Side Operations (1,000-10,000 rows)

Backend handles data operations, frontend displays pages.

**Optimization Techniques:**
- Database indexing on sort/filter columns
- Query result caching (Redis, memory cache)
- Cursor-based pagination for stable results
- Compress API responses (gzip)
- Prefetch next page in background

**Backend optimization:**
```sql
-- Add indexes for common operations
CREATE INDEX idx_users_name ON users(name);
CREATE INDEX idx_users_created ON users(created_at);
CREATE INDEX idx_users_active ON users(is_active);

-- Use efficient queries
SELECT * FROM users
WHERE is_active = true
ORDER BY name ASC
LIMIT 50 OFFSET 100;
```

**Frontend optimization:**
```javascript
// Prefetch next page
const prefetchNextPage = () => {
  const nextPage = currentPage + 1;
  queryClient.prefetchQuery(['users', nextPage], () =>
    fetchUsers({ page: nextPage })
  );
};

// Cache previous results
const { data } = useQuery(
  ['users', page, filters],
  fetchUsers,
  {
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
  }
);
```

**Performance Metrics:**
- API response: <200ms
- Page navigation: <300ms
- Filter application: <500ms
- Time to interactive: <1s

### Tier 3: Virtual Scrolling (10,000-100,000 rows)

Render only visible rows, recycle DOM nodes.

**Core Concepts:**
- **Viewport**: Visible area of the table
- **Buffer**: Extra rows above/below viewport
- **Window**: Total rows in DOM (viewport + buffer)
- **Overscan**: Number of buffer rows (typically 3-5)

**Implementation with TanStack Virtual:**
```javascript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualTable({ data }) {
  const parentRef = useRef();

  const rowVirtualizer = useVirtualizer({
    count: data.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 35, // Estimated row height
    overscan: 5, // Buffer rows
  });

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: rowVirtualizer.getTotalSize() }}>
        {rowVirtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${virtualRow.start}px)`,
              height: virtualRow.size,
            }}
          >
            <TableRow data={data[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

**Advanced Optimizations:**
- Fixed row heights for better performance
- Dynamic row heights with measurement
- Horizontal virtualization for many columns
- Sticky headers/columns with virtualization

**Performance Metrics:**
- Constant 60fps scrolling
- Memory usage: O(visible rows) not O(total rows)
- Initial render: <500ms
- Scroll lag: <16ms

### Tier 4: Extreme Scale (100,000+ rows)

Combination of techniques for massive datasets.

**Advanced Techniques:**

1. **Web Workers for Processing**
```javascript
// main.js
const worker = new Worker('tableWorker.js');

worker.postMessage({
  type: 'FILTER',
  data: largeDataset,
  filter: filterCriteria
});

worker.onmessage = (e) => {
  if (e.data.type === 'FILTER_COMPLETE') {
    setFilteredData(e.data.result);
  }
};

// tableWorker.js
self.onmessage = (e) => {
  if (e.data.type === 'FILTER') {
    const filtered = e.data.data.filter(/* filter logic */);
    self.postMessage({
      type: 'FILTER_COMPLETE',
      result: filtered
    });
  }
};
```

2. **Streaming Data Loading**
```javascript
async function streamLargeDataset() {
  const response = await fetch('/api/stream-data');
  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  let buffer = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop(); // Keep incomplete line

    // Process complete lines
    const rows = lines.map(line => JSON.parse(line));
    appendRowsToTable(rows);
  }
}
```

3. **IndexedDB for Client Storage**
```javascript
// Store large datasets locally
async function cacheInIndexedDB(data) {
  const db = await openDB('TableCache', 1, {
    upgrade(db) {
      db.createObjectStore('rows', { keyPath: 'id' });
      db.createObjectStore('metadata');
    },
  });

  // Batch insert for performance
  const tx = db.transaction('rows', 'readwrite');
  await Promise.all(data.map(row => tx.store.add(row)));
  await tx.done;
}
```

## Rendering Optimizations

### Reduce React Re-renders

```javascript
// Use React.memo with custom comparison
const TableRow = React.memo(({ row, columns }) => {
  return (
    <tr>
      {columns.map(col => (
        <td key={col.id}>{row[col.accessor]}</td>
      ))}
    </tr>
  );
}, (prevProps, nextProps) => {
  // Only re-render if row data changes
  return prevProps.row.id === nextProps.row.id &&
         prevProps.row.updatedAt === nextProps.row.updatedAt;
});
```

### Batch DOM Updates

```javascript
// Use React 18's automatic batching
import { flushSync } from 'react-dom';

function handleMultipleUpdates() {
  // These will be batched automatically
  setSortColumn('name');
  setSortOrder('asc');
  setCurrentPage(1);
}

// Force synchronous update when needed
function handleCriticalUpdate() {
  flushSync(() => {
    setImportantData(newData);
  });
  // DOM is updated here
}
```

### CSS-based Optimizations

```css
/* Use CSS containment for better performance */
.table-container {
  contain: layout style paint;
}

/* Hardware acceleration for smooth scrolling */
.virtual-scroll-container {
  will-change: transform;
  transform: translateZ(0);
}

/* Efficient hover states */
tr:hover {
  background-color: var(--hover-bg);
  /* Avoid expensive properties like box-shadow */
}

/* Fixed table layout for consistent performance */
table {
  table-layout: fixed;
  width: 100%;
}
```

## Memory Management

### Prevent Memory Leaks

```javascript
function TableComponent() {
  useEffect(() => {
    const handleScroll = throttle(() => {
      // Handle scroll
    }, 100);

    window.addEventListener('scroll', handleScroll);

    // Cleanup to prevent leaks
    return () => {
      window.removeEventListener('scroll', handleScroll);
      handleScroll.cancel(); // Cancel throttled function
    };
  }, []);
}
```

### Efficient Data Structures

```javascript
// Use Map for O(1) lookups
const rowMap = new Map(data.map(row => [row.id, row]));

// Use Set for unique values
const uniqueCategories = new Set(data.map(row => row.category));

// Use typed arrays for numeric data
const numericColumn = new Float32Array(data.map(row => row.value));
```

## Network Optimizations

### Request Deduplication

```javascript
const requestCache = new Map();

async function fetchTableData(params) {
  const key = JSON.stringify(params);

  // Return cached promise if request in flight
  if (requestCache.has(key)) {
    return requestCache.get(key);
  }

  const promise = fetch(`/api/data?${new URLSearchParams(params)}`)
    .then(r => r.json())
    .finally(() => requestCache.delete(key));

  requestCache.set(key, promise);
  return promise;
}
```

### Response Compression

```javascript
// Server: Enable compression
app.use(compression({
  filter: (req, res) => {
    // Compress JSON responses
    return /json/.test(res.getHeader('Content-Type'));
  },
  level: 6 // Balance speed vs size
}));

// Client: Accept compressed responses
fetch('/api/data', {
  headers: {
    'Accept-Encoding': 'gzip, deflate, br'
  }
});
```

## Benchmarking Tools

### Performance Measurement

```javascript
// Measure render performance
function measureTablePerformance() {
  const startTime = performance.now();

  // Render table
  renderTable(data);

  const endTime = performance.now();
  console.log(`Render took ${endTime - startTime}ms`);

  // Use Performance Observer API
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      console.log(`${entry.name}: ${entry.duration}ms`);
    }
  });

  observer.observe({ entryTypes: ['measure'] });

  performance.mark('table-start');
  // ... table operations ...
  performance.mark('table-end');
  performance.measure('table-render', 'table-start', 'table-end');
}
```

### React DevTools Profiler

```javascript
import { Profiler } from 'react';

function onRenderCallback(id, phase, actualDuration) {
  console.log(`${id} (${phase}) took ${actualDuration}ms`);
}

<Profiler id="Table" onRender={onRenderCallback}>
  <Table data={data} />
</Profiler>
```

## Common Performance Pitfalls

### ❌ Avoid These Patterns

```javascript
// BAD: Creating new objects in render
<TableRow style={{ backgroundColor: row.color }} />

// GOOD: Use className or memoized styles
<TableRow className={row.className} />

// BAD: Inline function props
<TableRow onClick={() => handleClick(row.id)} />

// GOOD: Stable callback reference
const handleClick = useCallback((id) => {
  // handle click
}, []);

// BAD: Filtering in render
{data.filter(row => row.active).map(row => <Row />)}

// GOOD: Memoize filtered data
const activeRows = useMemo(
  () => data.filter(row => row.active),
  [data]
);
```

## Performance Checklist

- [ ] Implement virtual scrolling for >1,000 rows
- [ ] Add database indexes for sort/filter columns
- [ ] Enable API response compression
- [ ] Implement request caching strategy
- [ ] Use React.memo for row components
- [ ] Memoize expensive computations
- [ ] Debounce user inputs
- [ ] Profile with React DevTools
- [ ] Test on slower devices
- [ ] Monitor bundle size impact
- [ ] Implement progressive loading
- [ ] Add loading states
- [ ] Handle error states gracefully
- [ ] Test with realistic data volumes
- [ ] Measure and track key metrics