# Autocomplete and Typeahead Patterns


## Table of Contents

- [Basic Autocomplete Implementation](#basic-autocomplete-implementation)
  - [React Autocomplete with Downshift](#react-autocomplete-with-downshift)
  - [Highlight Matching Text](#highlight-matching-text)
- [Async Autocomplete with API](#async-autocomplete-with-api)
  - [Debounced API Autocomplete](#debounced-api-autocomplete)
- [Advanced Autocomplete Features](#advanced-autocomplete-features)
  - [Multi-Section Autocomplete](#multi-section-autocomplete)
  - [Recent Searches and Suggestions](#recent-searches-and-suggestions)
- [Search-as-you-type Implementation](#search-as-you-type-implementation)
  - [Real-time Search Results](#real-time-search-results)
- [Performance Optimization](#performance-optimization)
  - [Virtual Scrolling for Large Lists](#virtual-scrolling-for-large-lists)
  - [Memoized Filtering](#memoized-filtering)
- [Accessibility Features](#accessibility-features)
  - [ARIA Live Regions](#aria-live-regions)

## Basic Autocomplete Implementation

### React Autocomplete with Downshift
```tsx
import { useCombobox } from 'downshift';
import { useState, useMemo } from 'react';

interface AutocompleteProps<T> {
  items: T[];
  onSelect: (item: T | null) => void;
  itemToString: (item: T | null) => string;
  placeholder?: string;
  filterFunction?: (items: T[], inputValue: string) => T[];
}

export function Autocomplete<T>({
  items,
  onSelect,
  itemToString,
  placeholder = 'Type to search...',
  filterFunction
}: AutocompleteProps<T>) {
  const [inputItems, setInputItems] = useState(items);

  const defaultFilter = (items: T[], inputValue: string) => {
    return items.filter(item =>
      itemToString(item)
        .toLowerCase()
        .includes(inputValue.toLowerCase())
    );
  };

  const {
    isOpen,
    getToggleButtonProps,
    getLabelProps,
    getMenuProps,
    getInputProps,
    highlightedIndex,
    getItemProps,
    selectedItem,
    inputValue
  } = useCombobox({
    items: inputItems,
    itemToString,
    onInputValueChange: ({ inputValue }) => {
      const filterFn = filterFunction || defaultFilter;
      setInputItems(filterFn(items, inputValue || ''));
    },
    onSelectedItemChange: ({ selectedItem }) => {
      onSelect(selectedItem || null);
    }
  });

  return (
    <div className="autocomplete-container">
      <div className="autocomplete-input-wrapper">
        <input
          {...getInputProps()}
          placeholder={placeholder}
          className="autocomplete-input"
        />
        <button
          type="button"
          {...getToggleButtonProps()}
          aria-label="toggle menu"
          className="autocomplete-toggle"
        >
          {isOpen ? '▲' : '▼'}
        </button>
      </div>

      <ul {...getMenuProps()} className="autocomplete-menu">
        {isOpen && inputItems.length > 0 && (
          inputItems.map((item, index) => (
            <li
              key={`${itemToString(item)}${index}`}
              className={`autocomplete-item ${
                highlightedIndex === index ? 'highlighted' : ''
              } ${selectedItem === item ? 'selected' : ''}`}
              {...getItemProps({ item, index })}
            >
              <HighlightMatch
                text={itemToString(item)}
                query={inputValue || ''}
              />
            </li>
          ))
        )}

        {isOpen && inputItems.length === 0 && (
          <li className="autocomplete-no-results">
            No results found for "{inputValue}"
          </li>
        )}
      </ul>
    </div>
  );
}
```

### Highlight Matching Text
```tsx
interface HighlightMatchProps {
  text: string;
  query: string;
}

export function HighlightMatch({ text, query }: HighlightMatchProps) {
  if (!query) return <>{text}</>;

  const parts = text.split(new RegExp(`(${query})`, 'gi'));

  return (
    <>
      {parts.map((part, index) =>
        part.toLowerCase() === query.toLowerCase() ? (
          <mark key={index} className="highlight">
            {part}
          </mark>
        ) : (
          <span key={index}>{part}</span>
        )
      )}
    </>
  );
}
```

## Async Autocomplete with API

### Debounced API Autocomplete
```tsx
import { useState, useEffect, useCallback } from 'react';
import { debounce } from 'lodash';

interface AsyncAutocompleteProps {
  fetchSuggestions: (query: string) => Promise<string[]>;
  onSelect: (value: string) => void;
  debounceMs?: number;
  minChars?: number;
}

export function AsyncAutocomplete({
  fetchSuggestions,
  onSelect,
  debounceMs = 300,
  minChars = 2
}: AsyncAutocompleteProps) {
  const [inputValue, setInputValue] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);

  // Debounced fetch function
  const debouncedFetch = useCallback(
    debounce(async (query: string) => {
      if (query.length < minChars) {
        setSuggestions([]);
        setIsLoading(false);
        return;
      }

      setIsLoading(true);
      try {
        const results = await fetchSuggestions(query);
        setSuggestions(results);
        setIsOpen(true);
      } catch (error) {
        console.error('Failed to fetch suggestions:', error);
        setSuggestions([]);
      } finally {
        setIsLoading(false);
      }
    }, debounceMs),
    [fetchSuggestions, minChars]
  );

  // Fetch suggestions when input changes
  useEffect(() => {
    debouncedFetch(inputValue);
    return () => debouncedFetch.cancel();
  }, [inputValue, debouncedFetch]);

  // Keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!isOpen || suggestions.length === 0) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev =>
          prev < suggestions.length - 1 ? prev + 1 : 0
        );
        break;

      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev =>
          prev > 0 ? prev - 1 : suggestions.length - 1
        );
        break;

      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0) {
          const selected = suggestions[selectedIndex];
          setInputValue(selected);
          onSelect(selected);
          setIsOpen(false);
        }
        break;

      case 'Escape':
        setIsOpen(false);
        setSelectedIndex(-1);
        break;
    }
  };

  return (
    <div className="async-autocomplete">
      <div className="input-container">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => suggestions.length > 0 && setIsOpen(true)}
          onBlur={() => setTimeout(() => setIsOpen(false), 200)}
          placeholder="Start typing to search..."
          aria-autocomplete="list"
          aria-expanded={isOpen}
          aria-controls="suggestions-list"
          aria-activedescendant={
            selectedIndex >= 0 ? `suggestion-${selectedIndex}` : undefined
          }
        />

        {isLoading && (
          <div className="loading-indicator">
            <span className="spinner" />
          </div>
        )}
      </div>

      {isOpen && suggestions.length > 0 && (
        <ul
          id="suggestions-list"
          className="suggestions-dropdown"
          role="listbox"
        >
          {suggestions.map((suggestion, index) => (
            <li
              key={index}
              id={`suggestion-${index}`}
              role="option"
              aria-selected={index === selectedIndex}
              className={`suggestion-item ${
                index === selectedIndex ? 'selected' : ''
              }`}
              onMouseEnter={() => setSelectedIndex(index)}
              onClick={() => {
                setInputValue(suggestion);
                onSelect(suggestion);
                setIsOpen(false);
              }}
            >
              <HighlightMatch text={suggestion} query={inputValue} />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

## Advanced Autocomplete Features

### Multi-Section Autocomplete
```tsx
interface Section<T> {
  title: string;
  items: T[];
}

interface MultiSectionAutocompleteProps<T> {
  sections: Section<T>[];
  onSelect: (item: T) => void;
  itemToString: (item: T) => string;
  renderItem?: (item: T, isHighlighted: boolean) => React.ReactNode;
}

export function MultiSectionAutocomplete<T>({
  sections,
  onSelect,
  itemToString,
  renderItem
}: MultiSectionAutocompleteProps<T>) {
  const [inputValue, setInputValue] = useState('');
  const [highlightedSection, setHighlightedSection] = useState(0);
  const [highlightedItem, setHighlightedItem] = useState(0);

  // Filter sections based on input
  const filteredSections = useMemo(() => {
    if (!inputValue) return sections;

    return sections
      .map(section => ({
        ...section,
        items: section.items.filter(item =>
          itemToString(item)
            .toLowerCase()
            .includes(inputValue.toLowerCase())
        )
      }))
      .filter(section => section.items.length > 0);
  }, [sections, inputValue, itemToString]);

  // Navigate through sections and items
  const handleKeyDown = (e: React.KeyboardEvent) => {
    // Implementation of keyboard navigation
    // through sections and items
  };

  return (
    <div className="multi-section-autocomplete">
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Search..."
      />

      {inputValue && filteredSections.length > 0 && (
        <div className="sections-dropdown">
          {filteredSections.map((section, sectionIndex) => (
            <div key={section.title} className="section">
              <div className="section-title">{section.title}</div>
              <ul className="section-items">
                {section.items.map((item, itemIndex) => {
                  const isHighlighted =
                    sectionIndex === highlightedSection &&
                    itemIndex === highlightedItem;

                  return (
                    <li
                      key={itemToString(item)}
                      className={`item ${isHighlighted ? 'highlighted' : ''}`}
                      onClick={() => onSelect(item)}
                    >
                      {renderItem ? (
                        renderItem(item, isHighlighted)
                      ) : (
                        <HighlightMatch
                          text={itemToString(item)}
                          query={inputValue}
                        />
                      )}
                    </li>
                  );
                })}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

### Recent Searches and Suggestions
```tsx
interface SmartAutocompleteProps {
  fetchSuggestions: (query: string) => Promise<string[]>;
  recentSearches: string[];
  popularSearches: string[];
  onSelect: (value: string) => void;
  onClearRecent: () => void;
}

export function SmartAutocomplete({
  fetchSuggestions,
  recentSearches,
  popularSearches,
  onSelect,
  onClearRecent
}: SmartAutocompleteProps) {
  const [inputValue, setInputValue] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showInitial, setShowInitial] = useState(true);

  const sections = useMemo(() => {
    const result = [];

    if (showInitial && !inputValue) {
      if (recentSearches.length > 0) {
        result.push({
          title: 'Recent Searches',
          items: recentSearches,
          icon: '🕐',
          clearable: true
        });
      }

      if (popularSearches.length > 0) {
        result.push({
          title: 'Trending',
          items: popularSearches,
          icon: '🔥',
          clearable: false
        });
      }
    } else if (suggestions.length > 0) {
      result.push({
        title: 'Suggestions',
        items: suggestions,
        icon: '🔍',
        clearable: false
      });
    }

    return result;
  }, [showInitial, inputValue, recentSearches, popularSearches, suggestions]);

  return (
    <div className="smart-autocomplete">
      <input
        type="text"
        value={inputValue}
        onChange={(e) => {
          setInputValue(e.target.value);
          setShowInitial(false);
        }}
        onFocus={() => setShowInitial(true)}
        placeholder="Search or select from suggestions..."
      />

      {sections.length > 0 && (
        <div className="smart-dropdown">
          {sections.map((section) => (
            <div key={section.title} className="smart-section">
              <div className="section-header">
                <span className="section-icon">{section.icon}</span>
                <span className="section-title">{section.title}</span>
                {section.clearable && (
                  <button
                    onClick={onClearRecent}
                    className="clear-button"
                  >
                    Clear
                  </button>
                )}
              </div>

              <ul className="section-items">
                {section.items.map((item) => (
                  <li
                    key={item}
                    onClick={() => onSelect(item)}
                    className="smart-item"
                  >
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

## Search-as-you-type Implementation

### Real-time Search Results
```tsx
interface SearchAsYouTypeProps {
  searchFunction: (query: string) => Promise<SearchResult[]>;
  renderResult: (result: SearchResult) => React.ReactNode;
  minChars?: number;
  debounceMs?: number;
}

interface SearchResult {
  id: string;
  title: string;
  description: string;
  category: string;
  url: string;
}

export function SearchAsYouType({
  searchFunction,
  renderResult,
  minChars = 2,
  debounceMs = 200
}: SearchAsYouTypeProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const performSearch = useCallback(
    debounce(async (searchQuery: string) => {
      if (searchQuery.length < minChars) {
        setResults([]);
        setIsSearching(false);
        return;
      }

      setIsSearching(true);
      try {
        const searchResults = await searchFunction(searchQuery);
        setResults(searchResults);
        setShowResults(true);
      } catch (error) {
        console.error('Search failed:', error);
        setResults([]);
      } finally {
        setIsSearching(false);
      }
    }, debounceMs),
    [searchFunction, minChars]
  );

  useEffect(() => {
    performSearch(query);
  }, [query, performSearch]);

  return (
    <div className="search-as-you-type">
      <div className="search-input-container">
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Start typing to search..."
          aria-label="Search"
          aria-describedby="search-status"
        />

        {isSearching && (
          <span className="search-status" id="search-status">
            Searching...
          </span>
        )}
      </div>

      {showResults && results.length > 0 && (
        <div className="instant-results">
          <div className="results-header">
            Found {results.length} results for "{query}"
          </div>

          <div className="results-list">
            {results.map(result => (
              <div key={result.id} className="result-item">
                {renderResult(result)}
              </div>
            ))}
          </div>
        </div>
      )}

      {showResults && results.length === 0 && !isSearching && query.length >= minChars && (
        <div className="no-results">
          No results found for "{query}"
        </div>
      )}
    </div>
  );
}
```

## Performance Optimization

### Virtual Scrolling for Large Lists
```tsx
import { FixedSizeList as List } from 'react-window';

interface VirtualAutocompleteProps {
  items: string[];
  itemHeight?: number;
  maxHeight?: number;
  onSelect: (item: string) => void;
}

export function VirtualAutocomplete({
  items,
  itemHeight = 35,
  maxHeight = 300,
  onSelect
}: VirtualAutocompleteProps) {
  const [inputValue, setInputValue] = useState('');

  const filteredItems = useMemo(() => {
    if (!inputValue) return items;
    return items.filter(item =>
      item.toLowerCase().includes(inputValue.toLowerCase())
    );
  }, [items, inputValue]);

  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div
      style={style}
      className="virtual-item"
      onClick={() => onSelect(filteredItems[index])}
    >
      <HighlightMatch text={filteredItems[index]} query={inputValue} />
    </div>
  );

  return (
    <div className="virtual-autocomplete">
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder="Search from thousands of items..."
      />

      {filteredItems.length > 0 && (
        <List
          height={Math.min(maxHeight, filteredItems.length * itemHeight)}
          itemCount={filteredItems.length}
          itemSize={itemHeight}
          width="100%"
        >
          {Row}
        </List>
      )}
    </div>
  );
}
```

### Memoized Filtering
```tsx
import { useMemo } from 'react';

function useFuzzySearch<T>(
  items: T[],
  searchQuery: string,
  options: {
    keys: string[];
    threshold?: number;
    includeScore?: boolean;
  }
) {
  return useMemo(() => {
    if (!searchQuery) return items;

    // Simple fuzzy matching implementation
    const fuzzyMatch = (str: string, pattern: string) => {
      pattern = pattern.toLowerCase();
      str = str.toLowerCase();

      let patternIdx = 0;
      let strIdx = 0;
      let score = 0;

      while (patternIdx < pattern.length && strIdx < str.length) {
        if (pattern[patternIdx] === str[strIdx]) {
          score++;
          patternIdx++;
        }
        strIdx++;
      }

      return {
        matched: patternIdx === pattern.length,
        score: score / pattern.length
      };
    };

    return items
      .map(item => {
        const scores = options.keys.map(key => {
          const value = String(item[key]);
          return fuzzyMatch(value, searchQuery);
        });

        const bestMatch = scores.reduce((best, current) =>
          current.score > best.score ? current : best
        );

        return {
          item,
          ...bestMatch
        };
      })
      .filter(result => result.matched)
      .sort((a, b) => b.score - a.score)
      .map(result => options.includeScore ? result : result.item);
  }, [items, searchQuery, options]);
}
```

## Accessibility Features

### ARIA Live Regions
```tsx
function AccessibleAutocomplete() {
  const [results, setResults] = useState([]);
  const [announcement, setAnnouncement] = useState('');

  useEffect(() => {
    // Announce results to screen readers
    if (results.length > 0) {
      setAnnouncement(`${results.length} suggestions available`);
    } else {
      setAnnouncement('No suggestions available');
    }
  }, [results]);

  return (
    <>
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
        {announcement}
      </div>

      <div
        role="combobox"
        aria-expanded={results.length > 0}
        aria-haspopup="listbox"
        aria-owns="suggestions"
      >
        <input
          type="text"
          aria-autocomplete="list"
          aria-controls="suggestions"
          aria-describedby="instructions"
        />

        <span id="instructions" className="sr-only">
          Type to search. Use arrow keys to navigate suggestions.
        </span>

        <ul
          id="suggestions"
          role="listbox"
        >
          {results.map((result, index) => (
            <li
              key={index}
              role="option"
              aria-selected={false}
            >
              {result}
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}
```