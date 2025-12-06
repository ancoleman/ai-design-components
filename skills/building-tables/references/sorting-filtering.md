# Sorting and Filtering Patterns


## Table of Contents

- [Sorting Implementation](#sorting-implementation)
  - [Single Column Sorting](#single-column-sorting)
  - [Multi-Column Sorting](#multi-column-sorting)
  - [Custom Sort Functions](#custom-sort-functions)
- [Filtering Implementation](#filtering-implementation)
  - [Text Filtering](#text-filtering)
  - [Column-Specific Filters](#column-specific-filters)
  - [Advanced Filter Logic](#advanced-filter-logic)
  - [Filter UI Components](#filter-ui-components)
- [Combined Sort and Filter](#combined-sort-and-filter)
- [Server-Side Operations](#server-side-operations)
  - [API Integration](#api-integration)
  - [Backend Implementation (Node.js)](#backend-implementation-nodejs)
- [Performance Optimizations](#performance-optimizations)
  - [Debounced Filtering](#debounced-filtering)
  - [Memoized Sort and Filter](#memoized-sort-and-filter)
  - [Virtual Filtering](#virtual-filtering)

## Sorting Implementation

### Single Column Sorting

Basic implementation for sortable columns:

```javascript
const useSortableTable = (data, columns) => {
  const [sortConfig, setSortConfig] = useState({
    key: null,
    direction: 'ascending'
  });

  const sortedData = useMemo(() => {
    if (!sortConfig.key) return data;

    return [...data].sort((a, b) => {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];

      if (aValue === bValue) return 0;

      const comparison = aValue > bValue ? 1 : -1;
      return sortConfig.direction === 'ascending'
        ? comparison
        : -comparison;
    });
  }, [data, sortConfig]);

  const handleSort = (key) => {
    let direction = 'ascending';

    if (sortConfig.key === key) {
      if (sortConfig.direction === 'ascending') {
        direction = 'descending';
      } else {
        // Reset sort on third click
        setSortConfig({ key: null, direction: 'ascending' });
        return;
      }
    }

    setSortConfig({ key, direction });
  };

  return { sortedData, sortConfig, handleSort };
};
```

### Multi-Column Sorting

Support sorting by multiple columns with priority:

```javascript
const useMultiSort = (data) => {
  const [sortKeys, setSortKeys] = useState([]);

  const sortedData = useMemo(() => {
    if (!sortKeys.length) return data;

    return [...data].sort((a, b) => {
      for (const { key, direction } of sortKeys) {
        const aValue = a[key];
        const bValue = b[key];

        if (aValue !== bValue) {
          const comparison = aValue > bValue ? 1 : -1;
          return direction === 'asc' ? comparison : -comparison;
        }
      }
      return 0;
    });
  }, [data, sortKeys]);

  const addSortKey = (key, direction = 'asc') => {
    setSortKeys(prev => {
      const existing = prev.find(k => k.key === key);

      if (existing) {
        // Toggle direction or remove
        if (existing.direction === 'asc') {
          return prev.map(k =>
            k.key === key ? { ...k, direction: 'desc' } : k
          );
        } else {
          return prev.filter(k => k.key !== key);
        }
      } else {
        // Add new sort key
        return [...prev, { key, direction }];
      }
    });
  };

  const clearSort = () => setSortKeys([]);

  return { sortedData, sortKeys, addSortKey, clearSort };
};
```

### Custom Sort Functions

Handle different data types appropriately:

```javascript
const sortFunctions = {
  // String sorting (case-insensitive)
  string: (a, b) =>
    a.toLowerCase().localeCompare(b.toLowerCase()),

  // Numeric sorting
  number: (a, b) => a - b,

  // Date sorting
  date: (a, b) => new Date(a) - new Date(b),

  // Boolean sorting (false first)
  boolean: (a, b) => Number(a) - Number(b),

  // Natural sorting (handles "File 2" before "File 10")
  natural: (a, b) => {
    return a.localeCompare(b, undefined, {
      numeric: true,
      sensitivity: 'base'
    });
  },

  // Custom priority sorting
  priority: (a, b) => {
    const order = ['high', 'medium', 'low'];
    return order.indexOf(a) - order.indexOf(b);
  },

  // Null handling
  withNulls: (compareFn) => (a, b) => {
    if (a == null && b == null) return 0;
    if (a == null) return 1;  // nulls last
    if (b == null) return -1;
    return compareFn(a, b);
  }
};

// Usage
const sortData = (data, key, type = 'string') => {
  const sortFn = sortFunctions[type] || sortFunctions.string;
  return [...data].sort((a, b) =>
    sortFunctions.withNulls(sortFn)(a[key], b[key])
  );
};
```

## Filtering Implementation

### Text Filtering

Basic text search across columns:

```javascript
const useTextFilter = (data, searchableColumns) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredData = useMemo(() => {
    if (!searchTerm) return data;

    const term = searchTerm.toLowerCase();

    return data.filter(row => {
      return searchableColumns.some(column => {
        const value = row[column];
        if (value == null) return false;
        return String(value).toLowerCase().includes(term);
      });
    });
  }, [data, searchTerm, searchableColumns]);

  return { filteredData, searchTerm, setSearchTerm };
};
```

### Column-Specific Filters

Different filter types per column:

```javascript
const useColumnFilters = (data, columns) => {
  const [filters, setFilters] = useState({});

  const filteredData = useMemo(() => {
    return data.filter(row => {
      return Object.entries(filters).every(([columnId, filterValue]) => {
        const column = columns.find(c => c.id === columnId);
        const cellValue = row[columnId];

        if (!filterValue || !column) return true;

        switch (column.filterType) {
          case 'text':
            return String(cellValue)
              .toLowerCase()
              .includes(filterValue.toLowerCase());

          case 'exact':
            return cellValue === filterValue;

          case 'select':
            return filterValue.includes(cellValue);

          case 'range':
            const { min, max } = filterValue;
            return cellValue >= min && cellValue <= max;

          case 'date':
            const cellDate = new Date(cellValue);
            const { startDate, endDate } = filterValue;
            return cellDate >= startDate && cellDate <= endDate;

          case 'boolean':
            return cellValue === filterValue;

          default:
            return true;
        }
      });
    });
  }, [data, filters, columns]);

  const setFilter = (columnId, value) => {
    setFilters(prev => ({
      ...prev,
      [columnId]: value
    }));
  };

  const clearFilter = (columnId) => {
    setFilters(prev => {
      const next = { ...prev };
      delete next[columnId];
      return next;
    });
  };

  const clearAllFilters = () => setFilters({});

  return {
    filteredData,
    filters,
    setFilter,
    clearFilter,
    clearAllFilters
  };
};
```

### Advanced Filter Logic

Support complex filter expressions:

```javascript
const useAdvancedFilters = (data) => {
  const [filterGroups, setFilterGroups] = useState([]);

  const filteredData = useMemo(() => {
    if (!filterGroups.length) return data;

    return data.filter(row => {
      // OR between groups
      return filterGroups.some(group => {
        // AND within group
        return group.filters.every(filter => {
          const value = row[filter.field];

          switch (filter.operator) {
            case 'equals':
              return value === filter.value;
            case 'not_equals':
              return value !== filter.value;
            case 'contains':
              return String(value).includes(filter.value);
            case 'starts_with':
              return String(value).startsWith(filter.value);
            case 'ends_with':
              return String(value).endsWith(filter.value);
            case 'greater_than':
              return value > filter.value;
            case 'less_than':
              return value < filter.value;
            case 'between':
              return value >= filter.value[0] && value <= filter.value[1];
            case 'in':
              return filter.value.includes(value);
            case 'not_in':
              return !filter.value.includes(value);
            case 'is_empty':
              return !value;
            case 'is_not_empty':
              return !!value;
            default:
              return true;
          }
        });
      });
    });
  }, [data, filterGroups]);

  return { filteredData, filterGroups, setFilterGroups };
};
```

### Filter UI Components

#### Text Filter Input

```javascript
function TextFilter({ columnId, value, onChange }) {
  const [localValue, setLocalValue] = useState(value || '');
  const debouncedOnChange = useMemo(
    () => debounce(onChange, 300),
    [onChange]
  );

  const handleChange = (e) => {
    const newValue = e.target.value;
    setLocalValue(newValue);
    debouncedOnChange(columnId, newValue);
  };

  return (
    <input
      type="text"
      value={localValue}
      onChange={handleChange}
      placeholder="Filter..."
      aria-label={`Filter by ${columnId}`}
    />
  );
}
```

#### Select Filter

```javascript
function SelectFilter({ columnId, options, value, onChange }) {
  return (
    <select
      value={value || ''}
      onChange={(e) => onChange(columnId, e.target.value)}
      aria-label={`Filter by ${columnId}`}
    >
      <option value="">All</option>
      {options.map(option => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
}
```

#### Range Filter

```javascript
function RangeFilter({ columnId, min, max, value, onChange }) {
  const [range, setRange] = useState(value || { min, max });

  const handleChange = (type, newValue) => {
    const newRange = { ...range, [type]: newValue };
    setRange(newRange);
    onChange(columnId, newRange);
  };

  return (
    <div className="range-filter">
      <input
        type="number"
        value={range.min}
        onChange={(e) => handleChange('min', e.target.value)}
        placeholder="Min"
        aria-label={`Minimum ${columnId}`}
      />
      <span>to</span>
      <input
        type="number"
        value={range.max}
        onChange={(e) => handleChange('max', e.target.value)}
        placeholder="Max"
        aria-label={`Maximum ${columnId}`}
      />
    </div>
  );
}
```

#### Date Range Filter

```javascript
function DateRangeFilter({ columnId, value, onChange }) {
  const [dateRange, setDateRange] = useState(
    value || { startDate: null, endDate: null }
  );

  const handleChange = (type, date) => {
    const newRange = { ...dateRange, [type]: date };
    setDateRange(newRange);
    onChange(columnId, newRange);
  };

  return (
    <div className="date-range-filter">
      <input
        type="date"
        value={dateRange.startDate || ''}
        onChange={(e) => handleChange('startDate', e.target.value)}
        aria-label={`Start date for ${columnId}`}
      />
      <span>to</span>
      <input
        type="date"
        value={dateRange.endDate || ''}
        onChange={(e) => handleChange('endDate', e.target.value)}
        aria-label={`End date for ${columnId}`}
      />
    </div>
  );
}
```

## Combined Sort and Filter

Integrate sorting and filtering together:

```javascript
const useTableData = (initialData, columns) => {
  const [data] = useState(initialData);

  // Filtering
  const {
    filteredData,
    filters,
    setFilter,
    clearAllFilters
  } = useColumnFilters(data, columns);

  // Sorting
  const {
    sortedData,
    sortConfig,
    handleSort
  } = useSortableTable(filteredData, columns);

  // Search
  const {
    filteredData: searchedData,
    searchTerm,
    setSearchTerm
  } = useTextFilter(
    sortedData,
    columns.filter(c => c.searchable).map(c => c.id)
  );

  // Pagination
  const {
    paginatedData,
    currentPage,
    totalPages,
    goToPage
  } = usePagination(searchedData, 25);

  return {
    data: paginatedData,
    totalRows: searchedData.length,
    // Sorting
    sortConfig,
    handleSort,
    // Filtering
    filters,
    setFilter,
    clearAllFilters,
    // Search
    searchTerm,
    setSearchTerm,
    // Pagination
    currentPage,
    totalPages,
    goToPage
  };
};
```

## Server-Side Operations

### API Integration

```javascript
const useServerData = () => {
  const [params, setParams] = useState({
    page: 1,
    pageSize: 50,
    sortBy: null,
    sortOrder: 'asc',
    filters: {},
    search: ''
  });

  const { data, isLoading, error } = useQuery(
    ['table-data', params],
    () => fetchTableData(params),
    {
      keepPreviousData: true, // Keep old data while fetching
      staleTime: 5 * 60 * 1000, // 5 minutes
    }
  );

  const updateSort = (column) => {
    setParams(prev => ({
      ...prev,
      sortBy: column,
      sortOrder: prev.sortBy === column && prev.sortOrder === 'asc'
        ? 'desc'
        : 'asc',
      page: 1 // Reset to first page
    }));
  };

  const updateFilter = (columnId, value) => {
    setParams(prev => ({
      ...prev,
      filters: { ...prev.filters, [columnId]: value },
      page: 1 // Reset to first page
    }));
  };

  const updateSearch = debounce((term) => {
    setParams(prev => ({
      ...prev,
      search: term,
      page: 1
    }));
  }, 300);

  return {
    data: data?.rows || [],
    totalCount: data?.totalCount || 0,
    isLoading,
    error,
    updateSort,
    updateFilter,
    updateSearch,
    params
  };
};

// API endpoint
async function fetchTableData(params) {
  const queryParams = new URLSearchParams({
    page: params.page,
    limit: params.pageSize,
    sort: params.sortBy || '',
    order: params.sortOrder,
    search: params.search,
    ...params.filters
  });

  const response = await fetch(`/api/data?${queryParams}`);
  return response.json();
}
```

### Backend Implementation (Node.js)

```javascript
// Express endpoint with sorting and filtering
app.get('/api/data', async (req, res) => {
  const {
    page = 1,
    limit = 50,
    sort,
    order = 'asc',
    search,
    ...filters
  } = req.query;

  let query = db('users');

  // Apply filters
  Object.entries(filters).forEach(([key, value]) => {
    if (value) {
      query = query.where(key, 'like', `%${value}%`);
    }
  });

  // Apply search
  if (search) {
    query = query.where(function() {
      this.where('name', 'like', `%${search}%`)
        .orWhere('email', 'like', `%${search}%`)
        .orWhere('department', 'like', `%${search}%`);
    });
  }

  // Apply sorting
  if (sort) {
    query = query.orderBy(sort, order);
  }

  // Get total count before pagination
  const totalCount = await query.clone().count('* as count');

  // Apply pagination
  const offset = (page - 1) * limit;
  const rows = await query.limit(limit).offset(offset);

  res.json({
    rows,
    totalCount: totalCount[0].count,
    page: Number(page),
    pageSize: Number(limit),
    totalPages: Math.ceil(totalCount[0].count / limit)
  });
});
```

## Performance Optimizations

### Debounced Filtering

```javascript
import { debounce } from 'lodash';

const DebouncedFilter = ({ onFilter }) => {
  const debouncedFilter = useMemo(
    () => debounce(onFilter, 300),
    [onFilter]
  );

  useEffect(() => {
    return () => {
      debouncedFilter.cancel();
    };
  }, [debouncedFilter]);

  return (
    <input
      type="text"
      onChange={(e) => debouncedFilter(e.target.value)}
      placeholder="Type to filter..."
    />
  );
};
```

### Memoized Sort and Filter

```javascript
const useOptimizedData = (data, sortConfig, filters) => {
  // Memoize expensive operations
  const sortedData = useMemo(() => {
    if (!sortConfig.key) return data;
    return sortData(data, sortConfig);
  }, [data, sortConfig]);

  const filteredData = useMemo(() => {
    if (!Object.keys(filters).length) return sortedData;
    return filterData(sortedData, filters);
  }, [sortedData, filters]);

  return filteredData;
};
```

### Virtual Filtering

For large datasets with virtual scrolling:

```javascript
const useVirtualFilter = (allData, filter) => {
  const [filteredIndices, setFilteredIndices] = useState([]);

  useEffect(() => {
    // Run filter in Web Worker for large datasets
    const worker = new Worker('filterWorker.js');

    worker.postMessage({ data: allData, filter });

    worker.onmessage = (e) => {
      setFilteredIndices(e.data.indices);
    };

    return () => worker.terminate();
  }, [allData, filter]);

  return filteredIndices;
};
```