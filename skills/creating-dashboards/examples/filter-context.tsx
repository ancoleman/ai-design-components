import React, { createContext, useContext, useState, ReactNode } from 'react';

/**
 * Dashboard Filter Context
 *
 * Provides global filter state (date range, region, etc.) to all dashboard widgets.
 * When filters change, all connected widgets re-fetch data automatically.
 */

interface FilterState {
  dateRange: { start: Date; end: Date };
  region: string;
  category: string;
}

interface FilterContextType {
  filters: FilterState;
  setFilters: (filters: Partial<FilterState>) => void;
  resetFilters: () => void;
}

const DEFAULT_FILTERS: FilterState = {
  dateRange: {
    start: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),  // 30 days ago
    end: new Date(),
  },
  region: 'all',
  category: 'all',
};

const FilterContext = createContext<FilterContextType | undefined>(undefined);

export function FilterProvider({ children }: { children: ReactNode }) {
  const [filters, setFiltersState] = useState<FilterState>(DEFAULT_FILTERS);

  const setFilters = (newFilters: Partial<FilterState>) => {
    setFiltersState((prev) => ({ ...prev, ...newFilters }));
  };

  const resetFilters = () => {
    setFiltersState(DEFAULT_FILTERS);
  };

  return (
    <FilterContext.Provider value={{ filters, setFilters, resetFilters }}>
      {children}
    </FilterContext.Provider>
  );
}

export function useFilters() {
  const context = useContext(FilterContext);
  if (!context) {
    throw new Error('useFilters must be used within FilterProvider');
  }
  return context;
}

// Example widget using filters
function RevenueWidget() {
  const { filters } = useFilters();

  // Re-fetches when filters change
  const { data } = useQuery({
    queryKey: ['revenue', filters],
    queryFn: () => fetchRevenue(filters.dateRange, filters.region),
  });

  return <div>Revenue: {data?.total}</div>;
}

// Example filter controls
export function DashboardFilters() {
  const { filters, setFilters, resetFilters } = useFilters();

  return (
    <div style={{
      display: 'flex',
      gap: '16px',
      padding: '16px',
      backgroundColor: '#fff',
      borderRadius: '8px',
      border: '1px solid #e2e8f0',
      marginBottom: '24px',
    }}>
      <div>
        <label style={{ display: 'block', fontSize: '14px', fontWeight: 500, marginBottom: '4px' }}>
          Date Range
        </label>
        <input
          type="date"
          value={filters.dateRange.start.toISOString().split('T')[0]}
          onChange={(e) =>
            setFilters({
              dateRange: { ...filters.dateRange, start: new Date(e.target.value) },
            })
          }
          style={{ padding: '8px', borderRadius: '6px', border: '1px solid #e2e8f0' }}
        />
        <span style={{ margin: '0 8px' }}>to</span>
        <input
          type="date"
          value={filters.dateRange.end.toISOString().split('T')[0]}
          onChange={(e) =>
            setFilters({
              dateRange: { ...filters.dateRange, end: new Date(e.target.value) },
            })
          }
          style={{ padding: '8px', borderRadius: '6px', border: '1px solid #e2e8f0' }}
        />
      </div>

      <div>
        <label style={{ display: 'block', fontSize: '14px', fontWeight: 500, marginBottom: '4px' }}>
          Region
        </label>
        <select
          value={filters.region}
          onChange={(e) => setFilters({ region: e.target.value })}
          style={{ padding: '8px', borderRadius: '6px', border: '1px solid #e2e8f0', minWidth: '150px' }}
        >
          <option value="all">All Regions</option>
          <option value="us">North America</option>
          <option value="eu">Europe</option>
          <option value="asia">Asia Pacific</option>
        </select>
      </div>

      <div>
        <label style={{ display: 'block', fontSize: '14px', fontWeight: 500, marginBottom: '4px' }}>
          Category
        </label>
        <select
          value={filters.category}
          onChange={(e) => setFilters({ category: e.target.value })}
          style={{ padding: '8px', borderRadius: '6px', border: '1px solid #e2e8f0', minWidth: '150px' }}
        >
          <option value="all">All Categories</option>
          <option value="electronics">Electronics</option>
          <option value="clothing">Clothing</option>
          <option value="home">Home & Garden</option>
        </select>
      </div>

      <button
        onClick={resetFilters}
        style={{
          marginLeft: 'auto',
          padding: '8px 16px',
          backgroundColor: '#fff',
          border: '1px solid #e2e8f0',
          borderRadius: '6px',
          cursor: 'pointer',
          fontWeight: 600,
          color: '#64748b',
        }}
      >
        Reset Filters
      </button>
    </div>
  );
}

export default DashboardFilters;
