/**
 * Complete e-commerce product search implementation with filters
 *
 * Features:
 * - Search input with debouncing
 * - Multiple filter types (category, price, brand)
 * - URL state management
 * - Faceted search with counts
 * - Responsive design
 */

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useDebounce } from '../hooks/useDebounce';
import { Search, X, Filter, ChevronDown } from 'lucide-react';

// Types
interface Product {
  id: string;
  title: string;
  description: string;
  price: number;
  category: string;
  brand: string;
  rating: number;
  imageUrl: string;
  inStock: boolean;
}

interface SearchFilters {
  query?: string;
  categories?: string[];
  brands?: string[];
  minPrice?: number;
  maxPrice?: number;
  inStock?: boolean;
  sortBy?: string;
}

interface Facet {
  value: string;
  count: number;
}

interface SearchResults {
  products: Product[];
  facets: {
    categories: Facet[];
    brands: Facet[];
    priceRanges: Facet[];
  };
  total: number;
  page: number;
  totalPages: number;
}

// Main Component
export function ProductSearch() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [results, setResults] = useState<SearchResults | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isMobileFilterOpen, setIsMobileFilterOpen] = useState(false);

  // Parse filters from URL
  const filters = useMemo<SearchFilters>(() => {
    return {
      query: searchParams.get('q') || undefined,
      categories: searchParams.getAll('category'),
      brands: searchParams.getAll('brand'),
      minPrice: searchParams.get('min_price')
        ? parseFloat(searchParams.get('min_price')!)
        : undefined,
      maxPrice: searchParams.get('max_price')
        ? parseFloat(searchParams.get('max_price')!)
        : undefined,
      inStock: searchParams.get('in_stock') === 'true',
      sortBy: searchParams.get('sort') || 'relevance'
    };
  }, [searchParams]);

  // Update URL with new filters
  const updateFilters = useCallback((newFilters: Partial<SearchFilters>) => {
    const params = new URLSearchParams();

    // Merge with existing filters
    const merged = { ...filters, ...newFilters };

    // Build URL params
    if (merged.query) params.set('q', merged.query);
    merged.categories?.forEach(cat => params.append('category', cat));
    merged.brands?.forEach(brand => params.append('brand', brand));
    if (merged.minPrice) params.set('min_price', merged.minPrice.toString());
    if (merged.maxPrice) params.set('max_price', merged.maxPrice.toString());
    if (merged.inStock) params.set('in_stock', 'true');
    if (merged.sortBy && merged.sortBy !== 'relevance') {
      params.set('sort', merged.sortBy);
    }

    setSearchParams(params);
  }, [filters, setSearchParams]);

  // Perform search
  const performSearch = useCallback(async (searchFilters: SearchFilters) => {
    setIsLoading(true);

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(searchFilters)
      });

      if (!response.ok) throw new Error('Search failed');

      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Search error:', error);
      // Handle error - show toast, etc.
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Search when filters change
  useEffect(() => {
    performSearch(filters);
  }, [filters, performSearch]);

  return (
    <div className="product-search">
      {/* Search Header */}
      <SearchHeader
        query={filters.query}
        onSearch={(query) => updateFilters({ query })}
        resultCount={results?.total}
        isLoading={isLoading}
      />

      <div className="search-body">
        {/* Mobile Filter Toggle */}
        <button
          className="mobile-filter-toggle"
          onClick={() => setIsMobileFilterOpen(true)}
        >
          <Filter size={20} />
          Filters
          {getActiveFilterCount(filters) > 0 && (
            <span className="filter-badge">{getActiveFilterCount(filters)}</span>
          )}
        </button>

        {/* Desktop Filters Sidebar */}
        <aside className="filters-sidebar desktop-only">
          <FilterPanel
            filters={filters}
            facets={results?.facets}
            onFilterChange={updateFilters}
            onClearAll={() => setSearchParams(new URLSearchParams())}
          />
        </aside>

        {/* Results Area */}
        <main className="results-area">
          {/* Active Filters */}
          <ActiveFilters
            filters={filters}
            onRemove={(key, value) => {
              const newFilters = { ...filters };
              if (key === 'query') {
                delete newFilters.query;
              } else if (Array.isArray(newFilters[key])) {
                newFilters[key] = newFilters[key].filter(v => v !== value);
              } else {
                delete newFilters[key];
              }
              updateFilters(newFilters);
            }}
            onClearAll={() => setSearchParams(new URLSearchParams())}
          />

          {/* Sort Bar */}
          <SortBar
            value={filters.sortBy || 'relevance'}
            onChange={(sortBy) => updateFilters({ sortBy })}
            resultCount={results?.total}
          />

          {/* Product Grid */}
          {isLoading ? (
            <LoadingGrid />
          ) : results && results.products.length > 0 ? (
            <ProductGrid products={results.products} />
          ) : (
            <NoResults query={filters.query} />
          )}

          {/* Pagination */}
          {results && results.totalPages > 1 && (
            <Pagination
              currentPage={results.page}
              totalPages={results.totalPages}
              onPageChange={(page) => updateFilters({ page })}
            />
          )}
        </main>
      </div>

      {/* Mobile Filter Drawer */}
      {isMobileFilterOpen && (
        <MobileFilterDrawer
          filters={filters}
          facets={results?.facets}
          onFilterChange={updateFilters}
          onClose={() => setIsMobileFilterOpen(false)}
        />
      )}
    </div>
  );
}

// Search Header Component
function SearchHeader({ query, onSearch, resultCount, isLoading }) {
  const [localQuery, setLocalQuery] = useState(query || '');
  const debouncedQuery = useDebounce(localQuery, 300);

  useEffect(() => {
    if (debouncedQuery !== query) {
      onSearch(debouncedQuery);
    }
  }, [debouncedQuery, query, onSearch]);

  return (
    <header className="search-header">
      <div className="search-input-container">
        <Search className="search-icon" size={20} />
        <input
          type="search"
          value={localQuery}
          onChange={(e) => setLocalQuery(e.target.value)}
          placeholder="Search products..."
          className="search-input"
          aria-label="Search products"
        />
        {localQuery && (
          <button
            onClick={() => {
              setLocalQuery('');
              onSearch('');
            }}
            className="clear-button"
            aria-label="Clear search"
          >
            <X size={16} />
          </button>
        )}
      </div>

      {resultCount !== undefined && (
        <div className="result-count">
          {isLoading ? (
            <span className="loading">Searching...</span>
          ) : (
            <span>{resultCount.toLocaleString()} results</span>
          )}
        </div>
      )}
    </header>
  );
}

// Filter Panel Component
function FilterPanel({ filters, facets, onFilterChange, onClearAll }) {
  const hasActiveFilters = getActiveFilterCount(filters) > 0;

  return (
    <div className="filter-panel">
      <div className="filter-header">
        <h2>Filters</h2>
        {hasActiveFilters && (
          <button onClick={onClearAll} className="clear-all">
            Clear all
          </button>
        )}
      </div>

      {/* Category Filter */}
      <FilterSection title="Category">
        {facets?.categories.map(facet => (
          <CheckboxFilter
            key={facet.value}
            label={facet.value}
            count={facet.count}
            checked={filters.categories?.includes(facet.value)}
            onChange={(checked) => {
              const categories = filters.categories || [];
              onFilterChange({
                categories: checked
                  ? [...categories, facet.value]
                  : categories.filter(c => c !== facet.value)
              });
            }}
          />
        ))}
      </FilterSection>

      {/* Price Range */}
      <FilterSection title="Price">
        <PriceRangeFilter
          min={filters.minPrice}
          max={filters.maxPrice}
          onChange={(min, max) => {
            onFilterChange({ minPrice: min, maxPrice: max });
          }}
        />
      </FilterSection>

      {/* Brand Filter */}
      <FilterSection title="Brand">
        {facets?.brands.map(facet => (
          <CheckboxFilter
            key={facet.value}
            label={facet.value}
            count={facet.count}
            checked={filters.brands?.includes(facet.value)}
            onChange={(checked) => {
              const brands = filters.brands || [];
              onFilterChange({
                brands: checked
                  ? [...brands, facet.value]
                  : brands.filter(b => b !== facet.value)
              });
            }}
          />
        ))}
      </FilterSection>

      {/* Stock Filter */}
      <FilterSection title="Availability">
        <CheckboxFilter
          label="In Stock Only"
          checked={filters.inStock}
          onChange={(checked) => onFilterChange({ inStock: checked })}
        />
      </FilterSection>
    </div>
  );
}

// Helper Components
function FilterSection({ title, children }) {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <div className="filter-section">
      <button
        className="filter-section-header"
        onClick={() => setIsOpen(!isOpen)}
      >
        <span>{title}</span>
        <ChevronDown
          size={16}
          className={`chevron ${isOpen ? 'open' : ''}`}
        />
      </button>
      {isOpen && (
        <div className="filter-section-content">
          {children}
        </div>
      )}
    </div>
  );
}

function CheckboxFilter({ label, count, checked, onChange }) {
  return (
    <label className="checkbox-filter">
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
      />
      <span className="label">{label}</span>
      {count !== undefined && (
        <span className="count">({count})</span>
      )}
    </label>
  );
}

function PriceRangeFilter({ min, max, onChange }) {
  const [localMin, setLocalMin] = useState(min || '');
  const [localMax, setLocalMax] = useState(max || '');

  const handleApply = () => {
    onChange(
      localMin ? parseFloat(localMin) : undefined,
      localMax ? parseFloat(localMax) : undefined
    );
  };

  return (
    <div className="price-range-filter">
      <div className="price-inputs">
        <input
          type="number"
          placeholder="Min"
          value={localMin}
          onChange={(e) => setLocalMin(e.target.value)}
          onBlur={handleApply}
        />
        <span>to</span>
        <input
          type="number"
          placeholder="Max"
          value={localMax}
          onChange={(e) => setLocalMax(e.target.value)}
          onBlur={handleApply}
        />
      </div>
    </div>
  );
}

// Utility Functions
function getActiveFilterCount(filters: SearchFilters): number {
  let count = 0;
  if (filters.query) count++;
  if (filters.categories?.length) count += filters.categories.length;
  if (filters.brands?.length) count += filters.brands.length;
  if (filters.minPrice || filters.maxPrice) count++;
  if (filters.inStock) count++;
  return count;
}

// Additional components would include:
// - ActiveFilters
// - SortBar
// - ProductGrid
// - LoadingGrid
// - NoResults
// - Pagination
// - MobileFilterDrawer

// These follow similar patterns and would be implemented based on specific UI requirements