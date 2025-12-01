# Dashboard Filter Coordination

## Table of Contents
- [Global Filter Architecture](#global-filter-architecture)
- [Context-Based Filtering](#context-based-filtering)
- [Filter Types & Controls](#filter-types--controls)
- [Cross-Widget Synchronization](#cross-widget-synchronization)
- [URL State Management](#url-state-management)
- [Filter Persistence](#filter-persistence)
- [Performance Optimization](#performance-optimization)

## Global Filter Architecture

### Filter State Management
```typescript
interface DashboardFilters {
  dateRange: {
    start: Date;
    end: Date;
    preset?: 'today' | 'week' | 'month' | 'quarter' | 'year' | 'custom';
  };
  categories: string[];
  regions: string[];
  metrics: string[];
  comparison?: {
    enabled: boolean;
    period: 'previous' | 'year-ago';
  };
  granularity: 'hour' | 'day' | 'week' | 'month';
}

interface FilterAction {
  type: 'SET_DATE_RANGE' | 'ADD_CATEGORY' | 'REMOVE_CATEGORY' | 'RESET_FILTERS';
  payload: any;
}

function filterReducer(state: DashboardFilters, action: FilterAction): DashboardFilters {
  switch (action.type) {
    case 'SET_DATE_RANGE':
      return {
        ...state,
        dateRange: action.payload
      };

    case 'ADD_CATEGORY':
      return {
        ...state,
        categories: [...state.categories, action.payload]
      };

    case 'REMOVE_CATEGORY':
      return {
        ...state,
        categories: state.categories.filter(c => c !== action.payload)
      };

    case 'RESET_FILTERS':
      return getDefaultFilters();

    default:
      return state;
  }
}
```

## Context-Based Filtering

### Dashboard Filter Context
```tsx
const DashboardFilterContext = createContext<{
  filters: DashboardFilters;
  dispatch: React.Dispatch<FilterAction>;
  applyFilters: () => void;
  resetFilters: () => void;
  activeFilterCount: number;
}>({
  filters: getDefaultFilters(),
  dispatch: () => {},
  applyFilters: () => {},
  resetFilters: () => {},
  activeFilterCount: 0
});

export function DashboardFilterProvider({ children }) {
  const [filters, dispatch] = useReducer(filterReducer, getDefaultFilters());
  const [pendingFilters, setPendingFilters] = useState(filters);

  const activeFilterCount = useMemo(() => {
    let count = 0;
    if (filters.dateRange.preset !== 'all-time') count++;
    count += filters.categories.length;
    count += filters.regions.length;
    count += filters.metrics.length;
    if (filters.comparison?.enabled) count++;
    return count;
  }, [filters]);

  const applyFilters = useCallback(() => {
    // Batch filter updates
    setPendingFilters(filters);
    // Trigger data refresh for all widgets
    broadcastFilterChange(filters);
  }, [filters]);

  const resetFilters = useCallback(() => {
    dispatch({ type: 'RESET_FILTERS' });
  }, []);

  return (
    <DashboardFilterContext.Provider
      value={{
        filters,
        dispatch,
        applyFilters,
        resetFilters,
        activeFilterCount
      }}
    >
      {children}
    </DashboardFilterContext.Provider>
  );
}
```

### Using Filters in Widgets
```tsx
function FilteredWidget({ widgetConfig }) {
  const { filters } = useContext(DashboardFilterContext);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFilteredData = async () => {
      setLoading(true);

      const params = new URLSearchParams({
        startDate: filters.dateRange.start.toISOString(),
        endDate: filters.dateRange.end.toISOString(),
        categories: filters.categories.join(','),
        regions: filters.regions.join(','),
        metrics: filters.metrics.join(','),
        granularity: filters.granularity
      });

      try {
        const response = await fetch(`/api/widget/${widgetConfig.id}?${params}`);
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error('Failed to fetch widget data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchFilteredData();
  }, [filters, widgetConfig.id]);

  if (loading) return <WidgetSkeleton />;

  return (
    <Widget
      title={widgetConfig.title}
      data={data}
      filters={filters}
    />
  );
}
```

## Filter Types & Controls

### Date Range Filter
```tsx
function DateRangeFilter() {
  const { filters, dispatch } = useContext(DashboardFilterContext);
  const [customRange, setCustomRange] = useState(false);

  const presets = [
    { label: 'Today', value: 'today' },
    { label: 'Last 7 Days', value: 'week' },
    { label: 'Last 30 Days', value: 'month' },
    { label: 'Last Quarter', value: 'quarter' },
    { label: 'Last Year', value: 'year' },
    { label: 'Custom', value: 'custom' }
  ];

  const handlePresetChange = (preset: string) => {
    if (preset === 'custom') {
      setCustomRange(true);
      return;
    }

    const range = calculateDateRange(preset);
    dispatch({
      type: 'SET_DATE_RANGE',
      payload: { ...range, preset }
    });
  };

  return (
    <div className="date-range-filter">
      <label>Date Range</label>

      <div className="preset-buttons">
        {presets.map(preset => (
          <button
            key={preset.value}
            className={filters.dateRange.preset === preset.value ? 'active' : ''}
            onClick={() => handlePresetChange(preset.value)}
          >
            {preset.label}
          </button>
        ))}
      </div>

      {customRange && (
        <div className="custom-range">
          <DatePicker
            selected={filters.dateRange.start}
            onChange={date => dispatch({
              type: 'SET_DATE_RANGE',
              payload: { ...filters.dateRange, start: date }
            })}
            selectsStart
            startDate={filters.dateRange.start}
            endDate={filters.dateRange.end}
          />
          <DatePicker
            selected={filters.dateRange.end}
            onChange={date => dispatch({
              type: 'SET_DATE_RANGE',
              payload: { ...filters.dateRange, end: date }
            })}
            selectsEnd
            startDate={filters.dateRange.start}
            endDate={filters.dateRange.end}
            minDate={filters.dateRange.start}
          />
        </div>
      )}
    </div>
  );
}
```

### Multi-Select Filter
```tsx
function MultiSelectFilter({
  label,
  options,
  filterKey,
  maxSelections = Infinity
}) {
  const { filters, dispatch } = useContext(DashboardFilterContext);
  const selectedValues = filters[filterKey] || [];

  const handleToggle = (value: string) => {
    if (selectedValues.includes(value)) {
      dispatch({
        type: `REMOVE_${filterKey.toUpperCase()}`,
        payload: value
      });
    } else if (selectedValues.length < maxSelections) {
      dispatch({
        type: `ADD_${filterKey.toUpperCase()}`,
        payload: value
      });
    }
  };

  return (
    <div className="multi-select-filter">
      <label>{label}</label>

      <div className="options">
        {options.map(option => (
          <label key={option.value} className="checkbox-label">
            <input
              type="checkbox"
              checked={selectedValues.includes(option.value)}
              onChange={() => handleToggle(option.value)}
            />
            <span>{option.label}</span>
            {option.count && (
              <span className="count">({option.count})</span>
            )}
          </label>
        ))}
      </div>

      {selectedValues.length > 0 && (
        <button
          className="clear-selection"
          onClick={() => dispatch({
            type: `CLEAR_${filterKey.toUpperCase()}`
          })}
        >
          Clear {selectedValues.length} selected
        </button>
      )}
    </div>
  );
}
```

### Search Filter
```tsx
function SearchFilter({ onSearch, placeholder = "Search..." }) {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (debouncedQuery.length >= 2) {
      fetchSuggestions(debouncedQuery).then(setSuggestions);
    } else {
      setSuggestions([]);
    }
  }, [debouncedQuery]);

  const handleSearch = () => {
    onSearch(query);
    setSuggestions([]);
  };

  return (
    <div className="search-filter">
      <div className="search-input-wrapper">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          placeholder={placeholder}
        />
        <button onClick={handleSearch}>
          <SearchIcon />
        </button>
      </div>

      {suggestions.length > 0 && (
        <ul className="suggestions">
          {suggestions.map(suggestion => (
            <li
              key={suggestion}
              onClick={() => {
                setQuery(suggestion);
                onSearch(suggestion);
                setSuggestions([]);
              }}
            >
              {suggestion}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

## Cross-Widget Synchronization

### Filter Broadcast System
```tsx
class FilterBroadcaster {
  private subscribers = new Set<(filters: DashboardFilters) => void>();

  subscribe(callback: (filters: DashboardFilters) => void) {
    this.subscribers.add(callback);

    return () => {
      this.subscribers.delete(callback);
    };
  }

  broadcast(filters: DashboardFilters) {
    this.subscribers.forEach(callback => {
      callback(filters);
    });
  }
}

const filterBroadcaster = new FilterBroadcaster();

// Widget subscription
function useSyncedFilters() {
  const [filters, setFilters] = useState<DashboardFilters>();

  useEffect(() => {
    const unsubscribe = filterBroadcaster.subscribe(setFilters);
    return unsubscribe;
  }, []);

  return filters;
}
```

### Selective Filter Application
```tsx
interface WidgetFilterConfig {
  ignoreDateRange?: boolean;
  ignoreCategories?: boolean;
  customFilterMapping?: Record<string, string>;
  requiredFilters?: string[];
}

function SelectiveFilterWidget({ config }: { config: WidgetFilterConfig }) {
  const { filters } = useContext(DashboardFilterContext);

  const applicableFilters = useMemo(() => {
    const filtered = { ...filters };

    if (config.ignoreDateRange) {
      delete filtered.dateRange;
    }

    if (config.ignoreCategories) {
      delete filtered.categories;
    }

    // Apply custom mappings
    if (config.customFilterMapping) {
      Object.entries(config.customFilterMapping).forEach(([from, to]) => {
        filtered[to] = filtered[from];
        delete filtered[from];
      });
    }

    return filtered;
  }, [filters, config]);

  // Check if required filters are set
  const hasRequiredFilters = config.requiredFilters?.every(
    filterKey => applicableFilters[filterKey]?.length > 0
  );

  if (!hasRequiredFilters) {
    return (
      <div className="widget-message">
        Please select {config.requiredFilters?.join(', ')} to view this widget
      </div>
    );
  }

  return <WidgetContent filters={applicableFilters} />;
}
```

## URL State Management

### Syncing Filters with URL
```tsx
function useUrlFilterSync() {
  const { filters, dispatch } = useContext(DashboardFilterContext);
  const [searchParams, setSearchParams] = useSearchParams();

  // Read filters from URL on mount
  useEffect(() => {
    const urlFilters = parseUrlFilters(searchParams);
    if (urlFilters) {
      Object.entries(urlFilters).forEach(([key, value]) => {
        dispatch({
          type: `SET_${key.toUpperCase()}`,
          payload: value
        });
      });
    }
  }, []);

  // Update URL when filters change
  useEffect(() => {
    const params = new URLSearchParams();

    // Add date range
    if (filters.dateRange.preset !== 'all-time') {
      params.set('from', filters.dateRange.start.toISOString());
      params.set('to', filters.dateRange.end.toISOString());
      params.set('preset', filters.dateRange.preset || '');
    }

    // Add array filters
    if (filters.categories.length > 0) {
      params.set('categories', filters.categories.join(','));
    }

    if (filters.regions.length > 0) {
      params.set('regions', filters.regions.join(','));
    }

    // Update URL without navigation
    setSearchParams(params, { replace: true });
  }, [filters, setSearchParams]);
}

function parseUrlFilters(searchParams: URLSearchParams): Partial<DashboardFilters> {
  const filters: Partial<DashboardFilters> = {};

  // Parse date range
  const from = searchParams.get('from');
  const to = searchParams.get('to');
  if (from && to) {
    filters.dateRange = {
      start: new Date(from),
      end: new Date(to),
      preset: searchParams.get('preset') as any || 'custom'
    };
  }

  // Parse array filters
  const categories = searchParams.get('categories');
  if (categories) {
    filters.categories = categories.split(',');
  }

  const regions = searchParams.get('regions');
  if (regions) {
    filters.regions = regions.split(',');
  }

  return filters;
}
```

### Shareable Dashboard Links
```tsx
function ShareableLink() {
  const { filters } = useContext(DashboardFilterContext);
  const [shareUrl, setShareUrl] = useState('');
  const [copied, setCopied] = useState(false);

  const generateShareableLink = () => {
    const params = new URLSearchParams();

    // Encode all active filters
    params.set('filters', encodeFilters(filters));
    params.set('v', '1'); // Version for backwards compatibility

    const url = `${window.location.origin}/dashboard?${params.toString()}`;
    setShareUrl(url);

    // Optionally create short URL
    createShortUrl(url).then(shortUrl => {
      setShareUrl(shortUrl);
    });
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(shareUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="shareable-link">
      <button onClick={generateShareableLink}>
        Generate Shareable Link
      </button>

      {shareUrl && (
        <div className="share-url">
          <input
            type="text"
            value={shareUrl}
            readOnly
            onClick={(e) => e.currentTarget.select()}
          />
          <button onClick={copyToClipboard}>
            {copied ? 'Copied!' : 'Copy'}
          </button>
        </div>
      )}
    </div>
  );
}
```

## Filter Persistence

### Local Storage Persistence
```tsx
function useFilterPersistence() {
  const { filters, dispatch } = useContext(DashboardFilterContext);
  const storageKey = 'dashboard-filters';

  // Load saved filters on mount
  useEffect(() => {
    const saved = localStorage.getItem(storageKey);
    if (saved) {
      try {
        const savedFilters = JSON.parse(saved);

        // Validate and restore filters
        if (validateFilters(savedFilters)) {
          Object.entries(savedFilters).forEach(([key, value]) => {
            dispatch({
              type: `SET_${key.toUpperCase()}`,
              payload: value
            });
          });
        }
      } catch (error) {
        console.error('Failed to load saved filters:', error);
      }
    }
  }, []);

  // Save filters on change
  useEffect(() => {
    const filterData = {
      ...filters,
      savedAt: new Date().toISOString()
    };

    localStorage.setItem(storageKey, JSON.stringify(filterData));
  }, [filters]);

  const clearSavedFilters = () => {
    localStorage.removeItem(storageKey);
    dispatch({ type: 'RESET_FILTERS' });
  };

  return { clearSavedFilters };
}
```

### User Preference Storage
```tsx
interface FilterPreset {
  id: string;
  name: string;
  filters: DashboardFilters;
  isDefault?: boolean;
  createdAt: Date;
}

function FilterPresetManager() {
  const { filters, dispatch } = useContext(DashboardFilterContext);
  const [presets, setPresets] = useState<FilterPreset[]>([]);
  const [showSaveDialog, setShowSaveDialog] = useState(false);

  useEffect(() => {
    // Load user presets from API
    fetchUserPresets().then(setPresets);
  }, []);

  const savePreset = async (name: string, isDefault = false) => {
    const preset: FilterPreset = {
      id: generateId(),
      name,
      filters: { ...filters },
      isDefault,
      createdAt: new Date()
    };

    try {
      await saveUserPreset(preset);
      setPresets([...presets, preset]);
      setShowSaveDialog(false);
    } catch (error) {
      console.error('Failed to save preset:', error);
    }
  };

  const loadPreset = (preset: FilterPreset) => {
    Object.entries(preset.filters).forEach(([key, value]) => {
      dispatch({
        type: `SET_${key.toUpperCase()}`,
        payload: value
      });
    });
  };

  const deletePreset = async (presetId: string) => {
    try {
      await deleteUserPreset(presetId);
      setPresets(presets.filter(p => p.id !== presetId));
    } catch (error) {
      console.error('Failed to delete preset:', error);
    }
  };

  return (
    <div className="filter-presets">
      <div className="preset-list">
        {presets.map(preset => (
          <div key={preset.id} className="preset-item">
            <span>{preset.name}</span>
            {preset.isDefault && <span className="badge">Default</span>}
            <button onClick={() => loadPreset(preset)}>Load</button>
            <button onClick={() => deletePreset(preset.id)}>Delete</button>
          </div>
        ))}
      </div>

      <button onClick={() => setShowSaveDialog(true)}>
        Save Current Filters
      </button>

      {showSaveDialog && (
        <SavePresetDialog
          onSave={savePreset}
          onCancel={() => setShowSaveDialog(false)}
        />
      )}
    </div>
  );
}
```

## Performance Optimization

### Debounced Filter Updates
```tsx
function useDebouncedFilters(delay = 500) {
  const { filters } = useContext(DashboardFilterContext);
  const [debouncedFilters, setDebouncedFilters] = useState(filters);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedFilters(filters);
    }, delay);

    return () => clearTimeout(timer);
  }, [filters, delay]);

  return debouncedFilters;
}

// Use in widgets to avoid excessive re-fetching
function OptimizedWidget() {
  const filters = useDebouncedFilters(300);
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchWidgetData(filters).then(setData);
  }, [filters]); // Only refetch when debounced filters change

  return <WidgetContent data={data} />;
}
```

### Filter Change Detection
```tsx
function useFilterChanges() {
  const { filters } = useContext(DashboardFilterContext);
  const previousFilters = useRef(filters);
  const [changes, setChanges] = useState<string[]>([]);

  useEffect(() => {
    const changedKeys: string[] = [];

    Object.keys(filters).forEach(key => {
      if (JSON.stringify(filters[key]) !== JSON.stringify(previousFilters.current[key])) {
        changedKeys.push(key);
      }
    });

    setChanges(changedKeys);
    previousFilters.current = filters;
  }, [filters]);

  return changes;
}

// Use to selectively update widgets
function SmartWidget({ affectedBy }) {
  const changes = useFilterChanges();
  const shouldUpdate = changes.some(change => affectedBy.includes(change));

  useEffect(() => {
    if (shouldUpdate) {
      // Only refetch if relevant filters changed
      refetchData();
    }
  }, [shouldUpdate]);

  return <WidgetContent />;
}
```

### Cached Filter Results
```tsx
class FilterCache {
  private cache = new Map<string, { data: any; timestamp: number }>();
  private ttl = 5 * 60 * 1000; // 5 minutes

  getCacheKey(filters: DashboardFilters): string {
    return JSON.stringify(filters);
  }

  get(filters: DashboardFilters): any | null {
    const key = this.getCacheKey(filters);
    const cached = this.cache.get(key);

    if (cached) {
      const age = Date.now() - cached.timestamp;
      if (age < this.ttl) {
        return cached.data;
      }
      // Remove expired entry
      this.cache.delete(key);
    }

    return null;
  }

  set(filters: DashboardFilters, data: any) {
    const key = this.getCacheKey(filters);
    this.cache.set(key, {
      data,
      timestamp: Date.now()
    });

    // Limit cache size
    if (this.cache.size > 50) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
  }

  clear() {
    this.cache.clear();
  }
}

const filterCache = new FilterCache();

function useCachedFilterData(endpoint: string) {
  const filters = useContext(DashboardFilterContext).filters;
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Check cache first
    const cached = filterCache.get(filters);
    if (cached) {
      setData(cached);
      return;
    }

    // Fetch if not cached
    setLoading(true);
    fetchWithFilters(endpoint, filters)
      .then(result => {
        filterCache.set(filters, result);
        setData(result);
      })
      .finally(() => setLoading(false));
  }, [filters, endpoint]);

  return { data, loading };
}
```