# Query Parameter Management

## URL State Synchronization

### React Router Integration
```tsx
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';

interface FilterState {
  query?: string;
  categories?: string[];
  minPrice?: number;
  maxPrice?: number;
  sortBy?: string;
  page?: number;
}

export function useUrlFilters() {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  // Parse URL parameters to filter state
  const getFiltersFromUrl = (): FilterState => {
    const filters: FilterState = {};

    // Parse query
    const query = searchParams.get('q');
    if (query) filters.query = query;

    // Parse array parameters
    const categories = searchParams.getAll('category');
    if (categories.length > 0) filters.categories = categories;

    // Parse number parameters
    const minPrice = searchParams.get('min_price');
    if (minPrice) filters.minPrice = parseFloat(minPrice);

    const maxPrice = searchParams.get('max_price');
    if (maxPrice) filters.maxPrice = parseFloat(maxPrice);

    // Parse other parameters
    const sortBy = searchParams.get('sort');
    if (sortBy) filters.sortBy = sortBy;

    const page = searchParams.get('page');
    if (page) filters.page = parseInt(page, 10);

    return filters;
  };

  // Update URL with new filters
  const setFiltersToUrl = (filters: FilterState, replace = false) => {
    const params = new URLSearchParams();

    // Add query
    if (filters.query) {
      params.set('q', filters.query);
    }

    // Add array parameters
    if (filters.categories && filters.categories.length > 0) {
      filters.categories.forEach(cat => params.append('category', cat));
    }

    // Add number parameters
    if (filters.minPrice !== undefined) {
      params.set('min_price', filters.minPrice.toString());
    }

    if (filters.maxPrice !== undefined) {
      params.set('max_price', filters.maxPrice.toString());
    }

    // Add other parameters
    if (filters.sortBy) {
      params.set('sort', filters.sortBy);
    }

    if (filters.page && filters.page > 1) {
      params.set('page', filters.page.toString());
    }

    // Update URL
    if (replace) {
      navigate({ search: params.toString() }, { replace: true });
    } else {
      setSearchParams(params);
    }
  };

  // Update single filter
  const updateFilter = (key: keyof FilterState, value: any) => {
    const currentFilters = getFiltersFromUrl();
    const newFilters = { ...currentFilters };

    if (value === null || value === undefined ||
        (Array.isArray(value) && value.length === 0)) {
      delete newFilters[key];
    } else {
      newFilters[key] = value;
    }

    // Reset page when filters change
    if (key !== 'page') {
      delete newFilters.page;
    }

    setFiltersToUrl(newFilters);
  };

  // Clear all filters
  const clearFilters = () => {
    setSearchParams(new URLSearchParams());
  };

  return {
    filters: getFiltersFromUrl(),
    updateFilter,
    setFilters: setFiltersToUrl,
    clearFilters
  };
}
```

### Next.js URL Management
```tsx
import { useRouter } from 'next/router';
import { ParsedUrlQuery } from 'querystring';

export function useNextUrlFilters() {
  const router = useRouter();

  // Parse query object to filter state
  const parseQuery = (query: ParsedUrlQuery): FilterState => {
    const filters: FilterState = {};

    if (query.q && typeof query.q === 'string') {
      filters.query = query.q;
    }

    if (query.category) {
      filters.categories = Array.isArray(query.category)
        ? query.category
        : [query.category];
    }

    if (query.min_price && typeof query.min_price === 'string') {
      filters.minPrice = parseFloat(query.min_price);
    }

    if (query.max_price && typeof query.max_price === 'string') {
      filters.maxPrice = parseFloat(query.max_price);
    }

    if (query.sort && typeof query.sort === 'string') {
      filters.sortBy = query.sort;
    }

    if (query.page && typeof query.page === 'string') {
      filters.page = parseInt(query.page, 10);
    }

    return filters;
  };

  // Build query object from filters
  const buildQuery = (filters: FilterState): ParsedUrlQuery => {
    const query: ParsedUrlQuery = {};

    if (filters.query) query.q = filters.query;
    if (filters.categories && filters.categories.length > 0) {
      query.category = filters.categories;
    }
    if (filters.minPrice !== undefined) {
      query.min_price = filters.minPrice.toString();
    }
    if (filters.maxPrice !== undefined) {
      query.max_price = filters.maxPrice.toString();
    }
    if (filters.sortBy) query.sort = filters.sortBy;
    if (filters.page && filters.page > 1) {
      query.page = filters.page.toString();
    }

    return query;
  };

  // Update URL with new filters
  const updateFilters = (filters: FilterState, options?: { shallow?: boolean }) => {
    const query = buildQuery(filters);

    router.push(
      {
        pathname: router.pathname,
        query
      },
      undefined,
      { shallow: options?.shallow ?? true }
    );
  };

  return {
    filters: parseQuery(router.query),
    updateFilters,
    clearFilters: () => updateFilters({})
  };
}
```

## Complex Query Compression

### Base64 Encoding for Complex Filters
```typescript
interface ComplexFilter {
  query?: string;
  filters?: {
    [key: string]: any;
  };
  advanced?: {
    must?: string[];
    should?: string[];
    mustNot?: string[];
  };
  dateRange?: {
    start: Date;
    end: Date;
  };
}

class QueryCompressor {
  /**
   * Compress complex filter object to URL-safe string
   */
  static compress(filters: ComplexFilter): string {
    try {
      // Convert to JSON string
      const jsonString = JSON.stringify(filters);

      // Compress using base64
      const base64 = btoa(encodeURIComponent(jsonString));

      // Make URL-safe
      return base64
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=/g, '');
    } catch (error) {
      console.error('Failed to compress filters:', error);
      return '';
    }
  }

  /**
   * Decompress URL string back to filter object
   */
  static decompress(compressed: string): ComplexFilter | null {
    try {
      // Restore base64 padding
      const padding = '='.repeat((4 - (compressed.length % 4)) % 4);
      const base64 = compressed
        .replace(/-/g, '+')
        .replace(/_/g, '/')
        + padding;

      // Decode from base64
      const jsonString = decodeURIComponent(atob(base64));

      // Parse JSON
      return JSON.parse(jsonString);
    } catch (error) {
      console.error('Failed to decompress filters:', error);
      return null;
    }
  }
}

// Usage with React hook
export function useCompressedFilters() {
  const [searchParams, setSearchParams] = useSearchParams();

  const getFilters = (): ComplexFilter => {
    const compressed = searchParams.get('f');
    if (!compressed) return {};

    return QueryCompressor.decompress(compressed) || {};
  };

  const setFilters = (filters: ComplexFilter) => {
    const compressed = QueryCompressor.compress(filters);
    const params = new URLSearchParams();

    if (compressed) {
      params.set('f', compressed);
    }

    setSearchParams(params);
  };

  return { filters: getFilters(), setFilters };
}
```

## Shareable Search URLs

### Creating Shareable Links
```tsx
interface ShareableSearchProps {
  filters: FilterState;
  baseUrl?: string;
}

export function ShareableSearch({ filters, baseUrl = window.location.origin }: ShareableSearchProps) {
  const [shareUrl, setShareUrl] = useState('');
  const [copied, setCopied] = useState(false);

  // Generate shareable URL
  const generateShareUrl = () => {
    const params = new URLSearchParams();

    // Add all active filters
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        if (Array.isArray(value)) {
          value.forEach(v => params.append(key, v.toString()));
        } else {
          params.set(key, value.toString());
        }
      }
    });

    const url = `${baseUrl}/search?${params.toString()}`;
    setShareUrl(url);
    return url;
  };

  // Copy to clipboard
  const copyToClipboard = async () => {
    const url = generateShareUrl();

    try {
      await navigator.clipboard.writeText(url);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy:', error);
    }
  };

  // Share via Web Share API
  const share = async () => {
    const url = generateShareUrl();

    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Search Results',
          text: 'Check out these search results',
          url
        });
      } catch (error) {
        console.error('Share failed:', error);
      }
    } else {
      copyToClipboard();
    }
  };

  return (
    <div className="shareable-search">
      <button onClick={copyToClipboard} className="copy-btn">
        {copied ? '✅ Copied!' : '📋 Copy Link'}
      </button>

      <button onClick={share} className="share-btn">
        📤 Share
      </button>

      {shareUrl && (
        <input
          type="text"
          value={shareUrl}
          readOnly
          className="share-url-input"
        />
      )}
    </div>
  );
}
```

## History Management

### Search History with Local Storage
```tsx
interface SearchHistoryEntry {
  id: string;
  query: string;
  filters: FilterState;
  timestamp: Date;
  resultCount?: number;
}

class SearchHistory {
  private static readonly STORAGE_KEY = 'search_history';
  private static readonly MAX_ENTRIES = 20;

  /**
   * Save search to history
   */
  static save(entry: Omit<SearchHistoryEntry, 'id' | 'timestamp'>): void {
    const history = this.getAll();

    const newEntry: SearchHistoryEntry = {
      ...entry,
      id: Date.now().toString(),
      timestamp: new Date()
    };

    // Add to beginning of array
    history.unshift(newEntry);

    // Limit history size
    if (history.length > this.MAX_ENTRIES) {
      history.pop();
    }

    // Save to local storage
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(history));
  }

  /**
   * Get all history entries
   */
  static getAll(): SearchHistoryEntry[] {
    try {
      const stored = localStorage.getItem(this.STORAGE_KEY);
      if (!stored) return [];

      const history = JSON.parse(stored);
      // Parse dates
      return history.map((entry: any) => ({
        ...entry,
        timestamp: new Date(entry.timestamp)
      }));
    } catch (error) {
      console.error('Failed to load search history:', error);
      return [];
    }
  }

  /**
   * Get recent searches
   */
  static getRecent(count = 5): SearchHistoryEntry[] {
    return this.getAll().slice(0, count);
  }

  /**
   * Clear all history
   */
  static clear(): void {
    localStorage.removeItem(this.STORAGE_KEY);
  }

  /**
   * Remove specific entry
   */
  static remove(id: string): void {
    const history = this.getAll().filter(entry => entry.id !== id);
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(history));
  }
}

// React hook for search history
export function useSearchHistory() {
  const [history, setHistory] = useState<SearchHistoryEntry[]>([]);

  useEffect(() => {
    setHistory(SearchHistory.getAll());
  }, []);

  const saveSearch = (query: string, filters: FilterState, resultCount?: number) => {
    SearchHistory.save({ query, filters, resultCount });
    setHistory(SearchHistory.getAll());
  };

  const clearHistory = () => {
    SearchHistory.clear();
    setHistory([]);
  };

  const removeEntry = (id: string) => {
    SearchHistory.remove(id);
    setHistory(SearchHistory.getAll());
  };

  return {
    history,
    recentSearches: SearchHistory.getRecent(),
    saveSearch,
    clearHistory,
    removeEntry
  };
}
```

## Deep Linking Support

### Handling Deep Links
```tsx
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

export function useDeepLinking(onSearch: (filters: FilterState) => void) {
  const location = useLocation();

  useEffect(() => {
    // Parse deep link parameters on mount
    const params = new URLSearchParams(location.search);

    if (params.toString()) {
      const filters: FilterState = {};

      // Parse all parameters
      params.forEach((value, key) => {
        switch (key) {
          case 'q':
            filters.query = value;
            break;
          case 'category':
            if (!filters.categories) filters.categories = [];
            filters.categories.push(value);
            break;
          case 'min_price':
            filters.minPrice = parseFloat(value);
            break;
          case 'max_price':
            filters.maxPrice = parseFloat(value);
            break;
          case 'sort':
            filters.sortBy = value;
            break;
          case 'page':
            filters.page = parseInt(value, 10);
            break;
        }
      });

      // Execute search with deep link parameters
      onSearch(filters);
    }
  }, [location.search, onSearch]);
}
```

## Validation and Sanitization

### URL Parameter Validation
```typescript
class UrlValidator {
  /**
   * Validate and sanitize search query
   */
  static validateQuery(query: string): string {
    // Remove special characters that could break URLs
    const sanitized = query
      .replace(/[<>]/g, '')  // Remove HTML tags
      .replace(/[^\w\s-.,]/g, '')  // Keep only safe characters
      .trim()
      .substring(0, 200);  // Limit length

    return sanitized;
  }

  /**
   * Validate numeric range
   */
  static validateRange(min?: number, max?: number): { min?: number; max?: number } {
    const result: { min?: number; max?: number } = {};

    if (min !== undefined && !isNaN(min) && min >= 0) {
      result.min = min;
    }

    if (max !== undefined && !isNaN(max) && max >= 0) {
      result.max = max;
    }

    // Ensure min <= max
    if (result.min !== undefined && result.max !== undefined && result.min > result.max) {
      [result.min, result.max] = [result.max, result.min];
    }

    return result;
  }

  /**
   * Validate sort parameter
   */
  static validateSort(sort: string, allowedValues: string[]): string | undefined {
    return allowedValues.includes(sort) ? sort : undefined;
  }

  /**
   * Validate page number
   */
  static validatePage(page: any): number {
    const parsed = parseInt(page, 10);
    return isNaN(parsed) || parsed < 1 ? 1 : Math.min(parsed, 100);
  }
}

// Usage in component
export function useValidatedUrlFilters() {
  const [searchParams, setSearchParams] = useSearchParams();

  const getValidatedFilters = (): FilterState => {
    const filters: FilterState = {};

    // Validate query
    const query = searchParams.get('q');
    if (query) {
      filters.query = UrlValidator.validateQuery(query);
    }

    // Validate price range
    const minPrice = searchParams.get('min_price');
    const maxPrice = searchParams.get('max_price');
    const range = UrlValidator.validateRange(
      minPrice ? parseFloat(minPrice) : undefined,
      maxPrice ? parseFloat(maxPrice) : undefined
    );

    if (range.min !== undefined) filters.minPrice = range.min;
    if (range.max !== undefined) filters.maxPrice = range.max;

    // Validate sort
    const sort = searchParams.get('sort');
    if (sort) {
      const validSort = UrlValidator.validateSort(sort, [
        'relevance',
        'price_asc',
        'price_desc',
        'newest',
        'rating'
      ]);
      if (validSort) filters.sortBy = validSort;
    }

    // Validate page
    const page = searchParams.get('page');
    if (page) {
      filters.page = UrlValidator.validatePage(page);
    }

    return filters;
  };

  return getValidatedFilters();
}
```