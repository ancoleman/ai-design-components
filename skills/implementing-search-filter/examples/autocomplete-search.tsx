/**
 * Advanced autocomplete search implementation with Downshift
 *
 * Features:
 * - Accessible autocomplete with keyboard navigation
 * - Debounced API calls
 * - Recent searches and suggestions
 * - Highlighting of matched text
 * - Loading states and error handling
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useCombobox } from 'downshift';
import { Search, Clock, TrendingUp, X, Loader2 } from 'lucide-react';
import { useDebounce } from '../hooks/useDebounce';

// Types
interface Suggestion {
  id: string;
  text: string;
  type: 'product' | 'category' | 'brand' | 'recent' | 'trending';
  category?: string;
  count?: number;
  metadata?: any;
}

interface AutocompleteProps {
  onSearch: (query: string) => void;
  onSelect: (item: Suggestion) => void;
  placeholder?: string;
  minChars?: number;
  debounceMs?: number;
  maxSuggestions?: number;
}

export function AutocompleteSearch({
  onSearch,
  onSelect,
  placeholder = 'Search products, categories, brands...',
  minChars = 2,
  debounceMs = 300,
  maxSuggestions = 10
}: AutocompleteProps) {
  // State
  const [inputValue, setInputValue] = useState('');
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [recentSearches, setRecentSearches] = useState<Suggestion[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Refs
  const abortControllerRef = useRef<AbortController | null>(null);

  // Debounced search value
  const debouncedSearchTerm = useDebounce(inputValue, debounceMs);

  // Load recent searches from localStorage
  useEffect(() => {
    const stored = localStorage.getItem('recentSearches');
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setRecentSearches(parsed.slice(0, 5));
      } catch (e) {
        console.error('Failed to parse recent searches:', e);
      }
    }
  }, []);

  // Fetch suggestions
  const fetchSuggestions = useCallback(async (query: string) => {
    // Cancel previous request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    // Don't search if query too short
    if (query.length < minChars) {
      setSuggestions([]);
      return;
    }

    // Create new abort controller
    abortControllerRef.current = new AbortController();

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`/api/autocomplete?q=${encodeURIComponent(query)}&limit=${maxSuggestions}`, {
        signal: abortControllerRef.current.signal
      });

      if (!response.ok) {
        throw new Error('Failed to fetch suggestions');
      }

      const data = await response.json();
      setSuggestions(data.suggestions);
    } catch (err) {
      if (err.name === 'AbortError') {
        // Request was cancelled, ignore
        return;
      }
      setError('Failed to load suggestions');
      setSuggestions([]);
    } finally {
      setIsLoading(false);
    }
  }, [minChars, maxSuggestions]);

  // Fetch suggestions when debounced value changes
  useEffect(() => {
    if (debouncedSearchTerm) {
      fetchSuggestions(debouncedSearchTerm);
    } else {
      setSuggestions([]);
    }
  }, [debouncedSearchTerm, fetchSuggestions]);

  // Save to recent searches
  const saveToRecent = useCallback((text: string) => {
    const newRecent: Suggestion = {
      id: `recent-${Date.now()}`,
      text,
      type: 'recent'
    };

    const updated = [
      newRecent,
      ...recentSearches.filter(r => r.text !== text)
    ].slice(0, 5);

    setRecentSearches(updated);
    localStorage.setItem('recentSearches', JSON.stringify(updated));
  }, [recentSearches]);

  // Get display items (suggestions or recent/trending)
  const displayItems = inputValue.length >= minChars
    ? suggestions
    : recentSearches;

  // Setup Downshift
  const {
    isOpen,
    getMenuProps,
    getInputProps,
    highlightedIndex,
    getItemProps,
    selectedItem,
    reset
  } = useCombobox({
    items: displayItems,
    inputValue,
    onInputValueChange: ({ inputValue: newValue }) => {
      setInputValue(newValue || '');
    },
    onSelectedItemChange: ({ selectedItem }) => {
      if (selectedItem) {
        setInputValue(selectedItem.text);
        onSelect(selectedItem);
        saveToRecent(selectedItem.text);
        reset();
      }
    },
    itemToString: (item) => item?.text || ''
  });

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onSearch(inputValue);
      saveToRecent(inputValue);
      reset();
    }
  };

  // Clear input
  const handleClear = () => {
    setInputValue('');
    setSuggestions([]);
    reset();
  };

  return (
    <div className="autocomplete-search">
      <form onSubmit={handleSubmit} className="search-form">
        <div className="search-input-wrapper">
          <Search className="search-icon" size={20} />

          <input
            {...getInputProps()}
            className="search-input"
            placeholder={placeholder}
            aria-label="Search"
            aria-autocomplete="list"
            aria-describedby="search-instructions"
          />

          <span id="search-instructions" className="sr-only">
            Type to search. Use arrow keys to navigate suggestions.
          </span>

          {/* Loading indicator */}
          {isLoading && (
            <div className="loading-indicator">
              <Loader2 className="animate-spin" size={16} />
            </div>
          )}

          {/* Clear button */}
          {inputValue && (
            <button
              type="button"
              onClick={handleClear}
              className="clear-button"
              aria-label="Clear search"
            >
              <X size={16} />
            </button>
          )}
        </div>
      </form>

      {/* Suggestions dropdown */}
      <div {...getMenuProps()} className="suggestions-dropdown">
        {isOpen && displayItems.length > 0 && (
          <>
            {/* Show section header for recent searches */}
            {inputValue.length < minChars && recentSearches.length > 0 && (
              <div className="suggestions-section">
                <div className="section-header">
                  <Clock size={14} />
                  <span>Recent Searches</span>
                  <button
                    onClick={() => {
                      setRecentSearches([]);
                      localStorage.removeItem('recentSearches');
                    }}
                    className="clear-recent"
                  >
                    Clear
                  </button>
                </div>
              </div>
            )}

            {/* Render suggestions */}
            {displayItems.map((item, index) => (
              <SuggestionItem
                key={item.id}
                item={item}
                isHighlighted={highlightedIndex === index}
                query={inputValue}
                {...getItemProps({ item, index })}
              />
            ))}
          </>
        )}

        {/* No results message */}
        {isOpen && inputValue.length >= minChars && !isLoading && suggestions.length === 0 && (
          <div className="no-suggestions">
            No suggestions found for "{inputValue}"
          </div>
        )}

        {/* Error message */}
        {error && (
          <div className="suggestions-error">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}

// Suggestion Item Component
interface SuggestionItemProps {
  item: Suggestion;
  isHighlighted: boolean;
  query: string;
}

function SuggestionItem({
  item,
  isHighlighted,
  query,
  ...props
}: SuggestionItemProps & React.HTMLAttributes<HTMLLIElement>) {
  return (
    <li
      className={`suggestion-item ${isHighlighted ? 'highlighted' : ''} ${item.type}`}
      {...props}
    >
      <div className="suggestion-content">
        {/* Icon based on type */}
        <div className="suggestion-icon">
          {item.type === 'recent' && <Clock size={16} />}
          {item.type === 'trending' && <TrendingUp size={16} />}
          {item.type === 'product' && <Search size={16} />}
        </div>

        {/* Main text with highlighting */}
        <div className="suggestion-text">
          <HighlightText text={item.text} highlight={query} />

          {/* Additional metadata */}
          {item.category && (
            <span className="suggestion-category">in {item.category}</span>
          )}
        </div>

        {/* Result count */}
        {item.count !== undefined && (
          <span className="suggestion-count">{item.count}</span>
        )}
      </div>
    </li>
  );
}

// Highlight matching text
interface HighlightTextProps {
  text: string;
  highlight: string;
}

function HighlightText({ text, highlight }: HighlightTextProps) {
  if (!highlight.trim()) {
    return <span>{text}</span>;
  }

  const regex = new RegExp(`(${highlight})`, 'gi');
  const parts = text.split(regex);

  return (
    <span>
      {parts.map((part, index) =>
        regex.test(part) ? (
          <mark key={index} className="highlight">
            {part}
          </mark>
        ) : (
          <span key={index}>{part}</span>
        )
      )}
    </span>
  );
}

// Custom debounce hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

// Styles (CSS-in-JS or separate stylesheet)
const styles = `
.autocomplete-search {
  position: relative;
  width: 100%;
  max-width: 600px;
}

.search-form {
  width: 100%;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: var(--search-input-bg);
  border: 1px solid var(--search-input-border);
  border-radius: var(--search-border-radius);
  padding: 0 12px;
  transition: all 0.2s ease;
}

.search-input-wrapper:focus-within {
  border-color: var(--search-input-focus-border);
  box-shadow: 0 0 0 3px var(--search-input-focus-ring);
}

.search-icon {
  color: var(--search-icon-color);
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  background: none;
  padding: 12px;
  font-size: 16px;
  outline: none;
}

.loading-indicator {
  margin-left: 8px;
}

.clear-button {
  margin-left: 8px;
  padding: 4px;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-text-secondary);
  transition: color 0.2s;
}

.clear-button:hover {
  color: var(--color-text-primary);
}

.suggestions-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 4px;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  max-height: 400px;
  overflow-y: auto;
  z-index: 1000;
}

.suggestions-section {
  padding: 8px 12px;
  border-bottom: 1px solid var(--color-border);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--color-text-secondary);
}

.clear-recent {
  margin-left: auto;
  background: none;
  border: none;
  color: var(--color-primary);
  cursor: pointer;
  font-size: 12px;
}

.suggestion-item {
  padding: 12px;
  cursor: pointer;
  transition: background 0.1s;
}

.suggestion-item:hover,
.suggestion-item.highlighted {
  background: var(--color-gray-50);
}

.suggestion-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.suggestion-icon {
  color: var(--color-text-secondary);
  flex-shrink: 0;
}

.suggestion-text {
  flex: 1;
}

.suggestion-category {
  margin-left: 8px;
  font-size: 12px;
  color: var(--color-text-secondary);
}

.suggestion-count {
  font-size: 12px;
  color: var(--color-text-secondary);
  background: var(--color-gray-100);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
}

.highlight {
  background: var(--result-highlight-bg);
  color: var(--result-highlight-text);
  font-weight: 500;
}

.no-suggestions,
.suggestions-error {
  padding: 16px;
  text-align: center;
  color: var(--color-text-secondary);
}

.suggestions-error {
  color: var(--color-error);
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
`;