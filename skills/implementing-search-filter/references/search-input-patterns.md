# Search Input Patterns

## Basic Search Input

### Minimal Implementation
```tsx
import { useState, useCallback } from 'react';
import { debounce } from 'lodash';

function SearchInput({ onSearch }) {
  const [value, setValue] = useState('');

  const debouncedSearch = useCallback(
    debounce((query) => onSearch(query), 300),
    [onSearch]
  );

  const handleChange = (e) => {
    const newValue = e.target.value;
    setValue(newValue);
    debouncedSearch(newValue);
  };

  return (
    <div role="search">
      <input
        type="search"
        value={value}
        onChange={handleChange}
        placeholder="Search..."
        aria-label="Search"
      />
    </div>
  );
}
```

## Advanced Search Input

### With Clear Button and Loading State
```tsx
import { useState, useCallback } from 'react';
import { Search, X, Loader2 } from 'lucide-react';

interface SearchInputProps {
  onSearch: (query: string) => void;
  isLoading?: boolean;
  placeholder?: string;
}

export function SearchInput({
  onSearch,
  isLoading = false,
  placeholder = "Search products..."
}: SearchInputProps) {
  const [value, setValue] = useState('');
  const [isFocused, setIsFocused] = useState(false);

  const handleClear = () => {
    setValue('');
    onSearch('');
  };

  return (
    <div className="search-container">
      <div className="search-icon">
        {isLoading ? (
          <Loader2 className="animate-spin" />
        ) : (
          <Search />
        )}
      </div>

      <input
        type="search"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        placeholder={placeholder}
        className="search-input"
        aria-label="Search"
        aria-busy={isLoading}
      />

      {value && (
        <button
          onClick={handleClear}
          className="clear-button"
          aria-label="Clear search"
        >
          <X />
        </button>
      )}
    </div>
  );
}
```

## Search with Keyboard Shortcuts

### Global Search Hotkey (Cmd/Ctrl + K)
```tsx
import { useEffect, useRef } from 'react';

export function GlobalSearch() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Cmd+K (Mac) or Ctrl+K (Windows/Linux)
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen(true);
        inputRef.current?.focus();
      }

      // Escape to close
      if (e.key === 'Escape') {
        setIsOpen(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  if (!isOpen) return null;

  return (
    <div className="search-modal">
      <input
        ref={inputRef}
        type="search"
        placeholder="Type to search..."
        autoFocus
      />
    </div>
  );
}
```

## Debouncing Strategies

### Custom Debounce Hook
```tsx
import { useEffect, useState } from 'react';

function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
function SearchComponent() {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearchTerm = useDebounce(searchTerm, 300);

  useEffect(() => {
    if (debouncedSearchTerm) {
      // Perform search
      performSearch(debouncedSearchTerm);
    }
  }, [debouncedSearchTerm]);
}
```

### Cancellable Search Requests
```tsx
import { useRef, useCallback } from 'react';

function useSearchAPI() {
  const abortControllerRef = useRef<AbortController | null>(null);

  const search = useCallback(async (query: string) => {
    // Cancel previous request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    // Create new abort controller
    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch(`/api/search?q=${query}`, {
        signal: abortControllerRef.current.signal
      });

      if (!response.ok) throw new Error('Search failed');

      return await response.json();
    } catch (error) {
      if (error.name === 'AbortError') {
        // Request was cancelled, ignore
        return null;
      }
      throw error;
    }
  }, []);

  return { search };
}
```

## Search Input States

### Visual States
```css
/* Base state */
.search-input {
  border: 1px solid var(--search-input-border);
  background: var(--search-input-bg);
  padding: var(--search-padding);
  border-radius: var(--search-border-radius);
  transition: all 0.2s ease;
}

/* Focus state */
.search-input:focus {
  outline: none;
  border-color: var(--search-input-focus-border);
  box-shadow: 0 0 0 3px var(--search-input-focus-ring);
}

/* Loading state */
.search-input[aria-busy="true"] {
  background-image: url('data:image/svg+xml;...');
  background-position: right 12px center;
  background-repeat: no-repeat;
}

/* Empty state */
.search-input:placeholder-shown {
  color: var(--search-placeholder-color);
}

/* Error state */
.search-input[aria-invalid="true"] {
  border-color: var(--color-error);
}
```

## Mobile Search Patterns

### Expandable Search
```tsx
function MobileSearch() {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className={`mobile-search ${isExpanded ? 'expanded' : ''}`}>
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        aria-label="Toggle search"
      >
        <Search />
      </button>

      {isExpanded && (
        <input
          type="search"
          placeholder="Search..."
          autoFocus
          onBlur={() => setIsExpanded(false)}
        />
      )}
    </div>
  );
}
```

### Full-Screen Search Modal
```tsx
function FullScreenSearch() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button onClick={() => setIsOpen(true)}>
        Search
      </button>

      {isOpen && (
        <div className="fullscreen-search">
          <div className="search-header">
            <input
              type="search"
              placeholder="What are you looking for?"
              autoFocus
            />
            <button onClick={() => setIsOpen(false)}>
              Cancel
            </button>
          </div>

          <div className="search-suggestions">
            {/* Recent searches, trending, etc */}
          </div>
        </div>
      )}
    </>
  );
}
```

## Accessibility Patterns

### ARIA Attributes
```tsx
<div role="search" aria-label="Site search">
  <label htmlFor="search-input" className="sr-only">
    Search products
  </label>

  <input
    id="search-input"
    type="search"
    aria-describedby="search-hint"
    aria-controls="search-results"
    aria-expanded={hasResults}
    aria-autocomplete="list"
    aria-busy={isSearching}
  />

  <span id="search-hint" className="sr-only">
    Type to search, use arrow keys to navigate suggestions
  </span>

  <div
    id="search-results"
    role="region"
    aria-live="polite"
    aria-relevant="additions removals"
  >
    {/* Results */}
  </div>
</div>
```

### Announcing Results
```tsx
function SearchResults({ results, query }) {
  return (
    <div role="region" aria-live="polite">
      <div className="sr-only">
        {results.length > 0
          ? `${results.length} results found for ${query}`
          : `No results found for ${query}`
        }
      </div>

      {results.map(result => (
        <SearchResult key={result.id} {...result} />
      ))}
    </div>
  );
}
```

## Performance Metrics

### Optimal Debounce Timing
- **Fast typists**: 200-250ms
- **Average typists**: 300-350ms
- **Slow typists**: 400-500ms
- **Mobile users**: 500-750ms

### Search Latency Targets
- **Autocomplete**: <100ms
- **Instant search**: <200ms
- **Full search**: <500ms
- **Complex search**: <1000ms

## Error Handling

### User-Friendly Error Messages
```tsx
function SearchError({ error, query }) {
  const getErrorMessage = () => {
    switch(error.type) {
      case 'NETWORK':
        return 'Unable to search. Please check your connection.';
      case 'TIMEOUT':
        return 'Search is taking longer than expected...';
      case 'INVALID_QUERY':
        return 'Please enter a valid search term.';
      case 'NO_RESULTS':
        return `No results found for "${query}". Try different keywords.`;
      default:
        return 'Something went wrong. Please try again.';
    }
  };

  return (
    <div role="alert" className="search-error">
      {getErrorMessage()}
    </div>
  );
}
```