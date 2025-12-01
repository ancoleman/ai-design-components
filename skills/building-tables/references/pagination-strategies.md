# Pagination Strategies

## Client-Side Pagination

For datasets under 1,000 rows where all data is loaded upfront.

### Basic Implementation

```javascript
const usePagination = (data, itemsPerPage = 25) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(itemsPerPage);

  const totalPages = Math.ceil(data.length / pageSize);
  const startIndex = (currentPage - 1) * pageSize;
  const endIndex = startIndex + pageSize;

  const paginatedData = useMemo(
    () => data.slice(startIndex, endIndex),
    [data, startIndex, endIndex]
  );

  const goToPage = (page) => {
    const pageNumber = Math.max(1, Math.min(page, totalPages));
    setCurrentPage(pageNumber);
  };

  const nextPage = () => goToPage(currentPage + 1);
  const previousPage = () => goToPage(currentPage - 1);
  const firstPage = () => goToPage(1);
  const lastPage = () => goToPage(totalPages);

  const canPreviousPage = currentPage > 1;
  const canNextPage = currentPage < totalPages;

  const changePageSize = (size) => {
    setPageSize(size);
    setCurrentPage(1); // Reset to first page
  };

  return {
    paginatedData,
    currentPage,
    totalPages,
    pageSize,
    startIndex: startIndex + 1,
    endIndex: Math.min(endIndex, data.length),
    totalItems: data.length,
    // Navigation
    goToPage,
    nextPage,
    previousPage,
    firstPage,
    lastPage,
    canPreviousPage,
    canNextPage,
    // Settings
    changePageSize
  };
};
```

### Pagination Controls Component

```javascript
function PaginationControls({
  currentPage,
  totalPages,
  pageSize,
  totalItems,
  startIndex,
  endIndex,
  goToPage,
  nextPage,
  previousPage,
  firstPage,
  lastPage,
  canPreviousPage,
  canNextPage,
  changePageSize
}) {
  return (
    <div className="pagination-controls">
      {/* Page size selector */}
      <div className="page-size">
        <label htmlFor="page-size">Show:</label>
        <select
          id="page-size"
          value={pageSize}
          onChange={(e) => changePageSize(Number(e.target.value))}
        >
          <option value={10}>10</option>
          <option value={25}>25</option>
          <option value={50}>50</option>
          <option value={100}>100</option>
        </select>
        <span>entries</span>
      </div>

      {/* Results summary */}
      <div className="results-summary">
        Showing {startIndex} to {endIndex} of {totalItems} results
      </div>

      {/* Page navigation */}
      <nav aria-label="Table pagination">
        <button
          onClick={firstPage}
          disabled={!canPreviousPage}
          aria-label="Go to first page"
        >
          First
        </button>

        <button
          onClick={previousPage}
          disabled={!canPreviousPage}
          aria-label="Go to previous page"
        >
          Previous
        </button>

        {/* Page numbers */}
        <PageNumbers
          currentPage={currentPage}
          totalPages={totalPages}
          goToPage={goToPage}
        />

        <button
          onClick={nextPage}
          disabled={!canNextPage}
          aria-label="Go to next page"
        >
          Next
        </button>

        <button
          onClick={lastPage}
          disabled={!canNextPage}
          aria-label="Go to last page"
        >
          Last
        </button>
      </nav>

      {/* Jump to page */}
      <div className="jump-to-page">
        <label htmlFor="jump-page">Go to page:</label>
        <input
          id="jump-page"
          type="number"
          min={1}
          max={totalPages}
          value={currentPage}
          onChange={(e) => goToPage(Number(e.target.value))}
        />
      </div>
    </div>
  );
}
```

### Smart Page Numbers

Show limited page numbers with ellipsis:

```javascript
function PageNumbers({ currentPage, totalPages, goToPage }) {
  const getPageNumbers = () => {
    const delta = 2; // Pages to show around current
    const range = [];
    const rangeWithDots = [];

    for (
      let i = Math.max(2, currentPage - delta);
      i <= Math.min(totalPages - 1, currentPage + delta);
      i++
    ) {
      range.push(i);
    }

    if (currentPage - delta > 2) {
      rangeWithDots.push(1, '...');
    } else {
      rangeWithDots.push(1);
    }

    rangeWithDots.push(...range);

    if (currentPage + delta < totalPages - 1) {
      rangeWithDots.push('...', totalPages);
    } else if (totalPages > 1) {
      rangeWithDots.push(totalPages);
    }

    return rangeWithDots;
  };

  return (
    <div className="page-numbers">
      {getPageNumbers().map((number, index) => (
        number === '...' ? (
          <span key={`dots-${index}`} className="dots">
            ...
          </span>
        ) : (
          <button
            key={number}
            onClick={() => goToPage(number)}
            className={currentPage === number ? 'active' : ''}
            aria-label={`Go to page ${number}`}
            aria-current={currentPage === number ? 'page' : undefined}
          >
            {number}
          </button>
        )
      ))}
    </div>
  );
}
```

## Server-Side Pagination

For large datasets where data is fetched page by page.

### API Integration

```javascript
const useServerPagination = (apiEndpoint, pageSize = 25) => {
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(pageSize);

  const { data, isLoading, error, isPreviousData } = useQuery(
    ['table-data', page, size],
    () => fetchPage(apiEndpoint, page, size),
    {
      keepPreviousData: true, // Smooth transitions
      staleTime: 5 * 60 * 1000, // Cache for 5 minutes
    }
  );

  // Prefetch next page
  const queryClient = useQueryClient();
  useEffect(() => {
    if (data?.hasMore) {
      queryClient.prefetchQuery(
        ['table-data', page + 1, size],
        () => fetchPage(apiEndpoint, page + 1, size)
      );
    }
  }, [data, page, size, queryClient]);

  const goToPage = (newPage) => {
    setPage(newPage);
  };

  const changePageSize = (newSize) => {
    setSize(newSize);
    setPage(1); // Reset to first page
  };

  return {
    data: data?.items || [],
    currentPage: page,
    totalPages: data?.totalPages || 0,
    totalItems: data?.totalItems || 0,
    pageSize: size,
    isLoading,
    error,
    isPreviousData, // True while fetching new page
    goToPage,
    changePageSize,
    hasNextPage: page < (data?.totalPages || 0),
    hasPreviousPage: page > 1
  };
};

async function fetchPage(endpoint, page, pageSize) {
  const params = new URLSearchParams({
    page,
    limit: pageSize
  });

  const response = await fetch(`${endpoint}?${params}`);
  if (!response.ok) throw new Error('Failed to fetch data');

  return response.json();
}
```

### Backend Implementation

```javascript
// Express.js endpoint
app.get('/api/users', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 25;
  const offset = (page - 1) * limit;

  try {
    // Get total count
    const [{ count }] = await db('users').count('* as count');

    // Get paginated data
    const items = await db('users')
      .select('*')
      .orderBy('created_at', 'desc')
      .limit(limit)
      .offset(offset);

    const totalPages = Math.ceil(count / limit);

    res.json({
      items,
      currentPage: page,
      totalPages,
      totalItems: count,
      pageSize: limit,
      hasMore: page < totalPages
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

### Cursor-Based Pagination

More stable for real-time data:

```javascript
// Frontend
const useCursorPagination = (apiEndpoint, pageSize = 25) => {
  const [cursors, setCursors] = useState([null]); // Track cursor history
  const [currentCursor, setCurrentCursor] = useState(null);

  const { data, isLoading, error } = useQuery(
    ['cursor-data', currentCursor, pageSize],
    () => fetchWithCursor(apiEndpoint, currentCursor, pageSize),
    {
      keepPreviousData: true
    }
  );

  const goToNextPage = () => {
    if (data?.nextCursor) {
      setCursors([...cursors, data.nextCursor]);
      setCurrentCursor(data.nextCursor);
    }
  };

  const goToPreviousPage = () => {
    if (cursors.length > 1) {
      const newCursors = [...cursors];
      newCursors.pop();
      setCursors(newCursors);
      setCurrentCursor(newCursors[newCursors.length - 1]);
    }
  };

  return {
    data: data?.items || [],
    isLoading,
    error,
    hasNextPage: !!data?.nextCursor,
    hasPreviousPage: cursors.length > 1,
    goToNextPage,
    goToPreviousPage
  };
};

// Backend
app.get('/api/users/cursor', async (req, res) => {
  const limit = parseInt(req.query.limit) || 25;
  const cursor = req.query.cursor;

  let query = db('users')
    .select('*')
    .orderBy('id', 'asc')
    .limit(limit + 1); // Fetch one extra to check for more

  if (cursor) {
    query = query.where('id', '>', cursor);
  }

  const rows = await query;

  const hasMore = rows.length > limit;
  const items = hasMore ? rows.slice(0, -1) : rows;
  const nextCursor = hasMore ? items[items.length - 1].id : null;

  res.json({
    items,
    nextCursor,
    hasMore
  });
});
```

## Infinite Scroll

Load more data as user scrolls.

### Implementation with Intersection Observer

```javascript
const useInfiniteScroll = (fetchMore) => {
  const loadMoreRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          fetchMore();
        }
      },
      { threshold: 0.5 }
    );

    if (loadMoreRef.current) {
      observer.observe(loadMoreRef.current);
    }

    return () => observer.disconnect();
  }, [fetchMore]);

  return loadMoreRef;
};

function InfiniteTable() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
    error
  } = useInfiniteQuery(
    'infinite-table',
    ({ pageParam = 0 }) => fetchTablePage(pageParam),
    {
      getNextPageParam: (lastPage, pages) => lastPage.nextCursor
    }
  );

  const loadMoreRef = useInfiniteScroll(() => {
    if (hasNextPage && !isFetchingNextPage) {
      fetchNextPage();
    }
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  const allRows = data.pages.flatMap(page => page.items);

  return (
    <div className="infinite-scroll-container">
      <table>
        <tbody>
          {allRows.map(row => (
            <tr key={row.id}>
              <td>{row.name}</td>
              <td>{row.email}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Load more trigger */}
      <div ref={loadMoreRef} className="load-more">
        {isFetchingNextPage && <div>Loading more...</div>}
        {!hasNextPage && <div>No more results</div>}
      </div>
    </div>
  );
}
```

### Manual Load More Button

Alternative to automatic infinite scroll:

```javascript
function LoadMoreTable() {
  const [items, setItems] = useState([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [isLoading, setIsLoading] = useState(false);

  const loadMore = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`/api/data?page=${page}&limit=50`);
      const data = await response.json();

      setItems([...items, ...data.items]);
      setPage(page + 1);
      setHasMore(data.hasMore);
    } catch (error) {
      console.error('Failed to load more:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <table>
        <tbody>
          {items.map(item => (
            <tr key={item.id}>
              <td>{item.name}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {hasMore && (
        <button
          onClick={loadMore}
          disabled={isLoading}
          className="load-more-btn"
        >
          {isLoading ? 'Loading...' : 'Load More'}
        </button>
      )}

      {!hasMore && (
        <div className="end-message">
          You've reached the end of the list
        </div>
      )}
    </div>
  );
}
```

## Virtual Scrolling with Pagination

Combine virtual scrolling with data pagination:

```javascript
const useVirtualPagination = (totalItems, itemHeight = 35) => {
  const [loadedPages, setLoadedPages] = useState(new Map());
  const [isLoading, setIsLoading] = useState(new Set());

  const pageSize = 100;
  const totalPages = Math.ceil(totalItems / pageSize);

  const loadPage = async (pageIndex) => {
    if (loadedPages.has(pageIndex) || isLoading.has(pageIndex)) {
      return;
    }

    setIsLoading(prev => new Set(prev).add(pageIndex));

    try {
      const response = await fetch(
        `/api/data?page=${pageIndex + 1}&limit=${pageSize}`
      );
      const data = await response.json();

      setLoadedPages(prev => new Map(prev).set(pageIndex, data.items));
    } finally {
      setIsLoading(prev => {
        const next = new Set(prev);
        next.delete(pageIndex);
        return next;
      });
    }
  };

  const getItem = (index) => {
    const pageIndex = Math.floor(index / pageSize);
    const itemIndex = index % pageSize;

    // Load page if needed
    if (!loadedPages.has(pageIndex)) {
      loadPage(pageIndex);
      return null; // Return placeholder
    }

    const page = loadedPages.get(pageIndex);
    return page?.[itemIndex];
  };

  return { getItem, loadedPages: loadedPages.size, totalPages };
};
```

## Performance Considerations

### Optimistic Updates

Update UI immediately while fetching:

```javascript
const useOptimisticPagination = () => {
  const [optimisticPage, setOptimisticPage] = useState(1);
  const [actualPage, setActualPage] = useState(1);

  const goToPage = (page) => {
    // Update UI immediately
    setOptimisticPage(page);

    // Fetch actual data
    fetchPage(page).then(() => {
      setActualPage(page);
    }).catch(() => {
      // Revert on error
      setOptimisticPage(actualPage);
    });
  };

  return { currentPage: optimisticPage, goToPage };
};
```

### Cache Management

```javascript
const usePaginationCache = () => {
  const cache = useRef(new Map());
  const maxCacheSize = 10; // Cache last 10 pages

  const getCachedPage = (page) => {
    return cache.current.get(page);
  };

  const setCachedPage = (page, data) => {
    // Remove oldest if cache is full
    if (cache.current.size >= maxCacheSize) {
      const firstKey = cache.current.keys().next().value;
      cache.current.delete(firstKey);
    }

    cache.current.set(page, {
      data,
      timestamp: Date.now()
    });
  };

  const clearCache = () => {
    cache.current.clear();
  };

  return { getCachedPage, setCachedPage, clearCache };
};
```

## Accessibility for Pagination

### ARIA Labels and Roles

```javascript
function AccessiblePagination({ currentPage, totalPages, onPageChange }) {
  return (
    <nav
      role="navigation"
      aria-label="Pagination Navigation"
    >
      <ul className="pagination">
        <li>
          <button
            onClick={() => onPageChange(currentPage - 1)}
            disabled={currentPage === 1}
            aria-label="Go to previous page"
          >
            Previous
          </button>
        </li>

        {[...Array(totalPages)].map((_, i) => (
          <li key={i + 1}>
            <button
              onClick={() => onPageChange(i + 1)}
              aria-label={`Go to page ${i + 1}`}
              aria-current={currentPage === i + 1 ? 'page' : undefined}
            >
              {i + 1}
            </button>
          </li>
        ))}

        <li>
          <button
            onClick={() => onPageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
            aria-label="Go to next page"
          >
            Next
          </button>
        </li>
      </ul>

      <div role="status" aria-live="polite" aria-atomic="true">
        Page {currentPage} of {totalPages}
      </div>
    </nav>
  );
}
```

### Keyboard Navigation

```javascript
function KeyboardPagination({ currentPage, totalPages, onPageChange }) {
  useEffect(() => {
    const handleKeyPress = (e) => {
      if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
          case 'ArrowLeft':
            if (currentPage > 1) {
              onPageChange(currentPage - 1);
            }
            break;
          case 'ArrowRight':
            if (currentPage < totalPages) {
              onPageChange(currentPage + 1);
            }
            break;
          case 'Home':
            onPageChange(1);
            break;
          case 'End':
            onPageChange(totalPages);
            break;
        }
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [currentPage, totalPages, onPageChange]);

  return null; // This component only handles keyboard events
}
```