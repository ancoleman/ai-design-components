# Filter UI Patterns

## Checkbox Filters

### Basic Multi-Select Filter
```tsx
interface FilterOption {
  id: string;
  label: string;
  count?: number;
}

interface CheckboxFilterProps {
  title: string;
  options: FilterOption[];
  selected: string[];
  onChange: (selected: string[]) => void;
}

export function CheckboxFilter({
  title,
  options,
  selected,
  onChange
}: CheckboxFilterProps) {
  const handleToggle = (optionId: string) => {
    if (selected.includes(optionId)) {
      onChange(selected.filter(id => id !== optionId));
    } else {
      onChange([...selected, optionId]);
    }
  };

  const handleSelectAll = () => {
    if (selected.length === options.length) {
      onChange([]);
    } else {
      onChange(options.map(opt => opt.id));
    }
  };

  return (
    <div className="filter-group">
      <h3>{title}</h3>

      <button
        onClick={handleSelectAll}
        className="select-all-btn"
      >
        {selected.length === options.length ? 'Clear all' : 'Select all'}
      </button>

      {options.map(option => (
        <label key={option.id} className="checkbox-label">
          <input
            type="checkbox"
            checked={selected.includes(option.id)}
            onChange={() => handleToggle(option.id)}
            aria-label={`Filter by ${option.label}`}
          />
          <span>{option.label}</span>
          {option.count !== undefined && (
            <span className="count">({option.count})</span>
          )}
        </label>
      ))}
    </div>
  );
}
```

### Collapsible Filter Groups
```tsx
import { ChevronDown, ChevronUp } from 'lucide-react';

function CollapsibleFilter({ title, children, defaultOpen = true }) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="filter-section">
      <button
        className="filter-header"
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-controls={`filter-${title}`}
      >
        <span>{title}</span>
        {isOpen ? <ChevronUp /> : <ChevronDown />}
      </button>

      {isOpen && (
        <div id={`filter-${title}`} className="filter-content">
          {children}
        </div>
      )}
    </div>
  );
}
```

## Range Filters

### Price Range Slider
```tsx
interface RangeFilterProps {
  min: number;
  max: number;
  value: [number, number];
  onChange: (value: [number, number]) => void;
  step?: number;
  prefix?: string;
}

export function RangeFilter({
  min,
  max,
  value,
  onChange,
  step = 1,
  prefix = '$'
}: RangeFilterProps) {
  const [localValue, setLocalValue] = useState(value);

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      onChange(localValue);
    }, 500); // Debounce

    return () => clearTimeout(timeoutId);
  }, [localValue]);

  return (
    <div className="range-filter">
      <div className="range-inputs">
        <input
          type="number"
          value={localValue[0]}
          onChange={(e) => setLocalValue([+e.target.value, localValue[1]])}
          min={min}
          max={localValue[1]}
          aria-label="Minimum price"
        />
        <span>to</span>
        <input
          type="number"
          value={localValue[1]}
          onChange={(e) => setLocalValue([localValue[0], +e.target.value])}
          min={localValue[0]}
          max={max}
          aria-label="Maximum price"
        />
      </div>

      <div className="range-slider">
        <input
          type="range"
          min={min}
          max={max}
          value={localValue[0]}
          onChange={(e) => setLocalValue([+e.target.value, localValue[1]])}
          step={step}
        />
        <input
          type="range"
          min={min}
          max={max}
          value={localValue[1]}
          onChange={(e) => setLocalValue([localValue[0], +e.target.value])}
          step={step}
        />
      </div>

      <div className="range-labels">
        <span>{prefix}{min}</span>
        <span>{prefix}{max}</span>
      </div>
    </div>
  );
}
```

### Date Range Picker
```tsx
import { Calendar } from 'lucide-react';

function DateRangeFilter({ value, onChange }) {
  const [startDate, endDate] = value;

  return (
    <div className="date-range-filter">
      <div className="date-input">
        <Calendar size={16} />
        <input
          type="date"
          value={startDate}
          onChange={(e) => onChange([e.target.value, endDate])}
          aria-label="Start date"
        />
      </div>

      <span className="separator">to</span>

      <div className="date-input">
        <Calendar size={16} />
        <input
          type="date"
          value={endDate}
          onChange={(e) => onChange([startDate, e.target.value])}
          min={startDate}
          aria-label="End date"
        />
      </div>
    </div>
  );
}
```

## Dropdown Filters

### Single Select Dropdown
```tsx
interface DropdownFilterProps {
  label: string;
  options: { value: string; label: string }[];
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

export function DropdownFilter({
  label,
  options,
  value,
  onChange,
  placeholder = 'Select...'
}: DropdownFilterProps) {
  return (
    <div className="dropdown-filter">
      <label htmlFor={`filter-${label}`}>{label}</label>
      <select
        id={`filter-${label}`}
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        <option value="">{placeholder}</option>
        {options.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}
```

### Searchable Dropdown with Downshift
```tsx
import { useCombobox } from 'downshift';

function SearchableDropdown({ items, onSelect, placeholder }) {
  const [inputItems, setInputItems] = useState(items);

  const {
    isOpen,
    getToggleButtonProps,
    getLabelProps,
    getMenuProps,
    getInputProps,
    highlightedIndex,
    getItemProps,
    selectedItem,
  } = useCombobox({
    items: inputItems,
    onInputValueChange: ({ inputValue }) => {
      setInputItems(
        items.filter(item =>
          item.toLowerCase().includes(inputValue.toLowerCase())
        )
      );
    },
    onSelectedItemChange: ({ selectedItem }) => {
      onSelect(selectedItem);
    },
  });

  return (
    <div className="searchable-dropdown">
      <label {...getLabelProps()}>Choose an element:</label>

      <div className="input-wrapper">
        <input
          {...getInputProps()}
          placeholder={placeholder}
        />
        <button
          type="button"
          {...getToggleButtonProps()}
          aria-label="toggle menu"
        >
          &#8595;
        </button>
      </div>

      <ul {...getMenuProps()} className="dropdown-menu">
        {isOpen &&
          inputItems.map((item, index) => (
            <li
              className={highlightedIndex === index ? 'highlighted' : ''}
              key={`${item}${index}`}
              {...getItemProps({ item, index })}
            >
              {item}
            </li>
          ))}
      </ul>
    </div>
  );
}
```

## Filter Chips

### Active Filter Display
```tsx
import { X } from 'lucide-react';

interface FilterChip {
  id: string;
  label: string;
  value: string;
}

interface ActiveFiltersProps {
  filters: FilterChip[];
  onRemove: (filterId: string) => void;
  onClearAll: () => void;
}

export function ActiveFilters({
  filters,
  onRemove,
  onClearAll
}: ActiveFiltersProps) {
  if (filters.length === 0) return null;

  return (
    <div className="active-filters">
      <span className="filters-label">Active filters:</span>

      {filters.map(filter => (
        <div key={filter.id} className="filter-chip">
          <span>{filter.label}: {filter.value}</span>
          <button
            onClick={() => onRemove(filter.id)}
            aria-label={`Remove ${filter.label} filter`}
          >
            <X size={14} />
          </button>
        </div>
      ))}

      <button
        onClick={onClearAll}
        className="clear-all-btn"
      >
        Clear all
      </button>
    </div>
  );
}
```

## Faceted Search

### Dynamic Count Updates
```tsx
interface FacetedSearchProps {
  facets: {
    category: string;
    options: Array<{
      value: string;
      label: string;
      count: number;
      disabled?: boolean;
    }>;
  }[];
  selected: Record<string, string[]>;
  onChange: (category: string, values: string[]) => void;
}

export function FacetedSearch({
  facets,
  selected,
  onChange
}: FacetedSearchProps) {
  return (
    <div className="faceted-search">
      {facets.map(facet => (
        <div key={facet.category} className="facet-group">
          <h3>{facet.category}</h3>

          {facet.options.map(option => (
            <label
              key={option.value}
              className={`facet-option ${option.disabled ? 'disabled' : ''}`}
            >
              <input
                type="checkbox"
                checked={selected[facet.category]?.includes(option.value)}
                onChange={(e) => {
                  const current = selected[facet.category] || [];
                  if (e.target.checked) {
                    onChange(facet.category, [...current, option.value]);
                  } else {
                    onChange(
                      facet.category,
                      current.filter(v => v !== option.value)
                    );
                  }
                }}
                disabled={option.disabled}
              />
              <span className="facet-label">{option.label}</span>
              <span className="facet-count">({option.count})</span>
            </label>
          ))}
        </div>
      ))}
    </div>
  );
}
```

## Mobile Filter Patterns

### Filter Drawer
```tsx
import { Filter, X } from 'lucide-react';

function MobileFilterDrawer({ children, filterCount = 0 }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="filter-trigger"
      >
        <Filter />
        Filters
        {filterCount > 0 && (
          <span className="filter-badge">{filterCount}</span>
        )}
      </button>

      {isOpen && (
        <>
          <div
            className="drawer-overlay"
            onClick={() => setIsOpen(false)}
          />

          <div className="filter-drawer">
            <div className="drawer-header">
              <h2>Filters</h2>
              <button onClick={() => setIsOpen(false)}>
                <X />
              </button>
            </div>

            <div className="drawer-content">
              {children}
            </div>

            <div className="drawer-footer">
              <button onClick={() => setIsOpen(false)}>
                Apply Filters
              </button>
            </div>
          </div>
        </>
      )}
    </>
  );
}
```

## Sort Options

### Sort Dropdown
```tsx
interface SortOption {
  value: string;
  label: string;
}

const sortOptions: SortOption[] = [
  { value: 'relevance', label: 'Most Relevant' },
  { value: 'price-asc', label: 'Price: Low to High' },
  { value: 'price-desc', label: 'Price: High to Low' },
  { value: 'rating', label: 'Highest Rated' },
  { value: 'newest', label: 'Newest First' },
];

export function SortDropdown({ value, onChange }) {
  return (
    <div className="sort-dropdown">
      <label htmlFor="sort">Sort by:</label>
      <select
        id="sort"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        {sortOptions.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}
```

## Filter State Management

### Using URL Parameters
```tsx
import { useSearchParams } from 'react-router-dom';

function useFilterState() {
  const [searchParams, setSearchParams] = useSearchParams();

  const getFilters = () => {
    const filters: Record<string, string[]> = {};

    searchParams.forEach((value, key) => {
      if (!filters[key]) {
        filters[key] = [];
      }
      filters[key].push(value);
    });

    return filters;
  };

  const updateFilter = (key: string, values: string[]) => {
    const newParams = new URLSearchParams(searchParams);

    // Remove existing
    newParams.delete(key);

    // Add new values
    values.forEach(value => {
      newParams.append(key, value);
    });

    setSearchParams(newParams);
  };

  const clearFilters = () => {
    setSearchParams(new URLSearchParams());
  };

  return {
    filters: getFilters(),
    updateFilter,
    clearFilters,
  };
}
```

## Accessibility Considerations

### Filter Region ARIA
```tsx
<div
  role="region"
  aria-label="Product filters"
  className="filter-panel"
>
  <h2 id="filter-heading">Filter Products</h2>

  <div
    role="group"
    aria-labelledby="filter-heading"
  >
    {/* Filter groups */}
  </div>

  <div aria-live="polite" aria-atomic="true">
    {resultCount} products found
  </div>
</div>
```

### Keyboard Navigation
```tsx
// Ensure all interactive elements are keyboard accessible
// Tab order should be logical
// Provide skip links for long filter lists

<a href="#results" className="skip-link">
  Skip to results
</a>
```