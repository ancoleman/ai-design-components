# AI-Assisted Component Library: Tables & Data Grids
## Master Plan for Table Component Skill

**Document Version:** 1.0
**Date:** November 13, 2025
**Purpose:** Comprehensive research and strategic planning for building an AI-assisted component library focused on tables, data grids, and tabular data presentation

---

## Executive Summary

Tables are the second most common way to display data (after charts), yet building performant, accessible, feature-rich tables is surprisingly complex. This skill provides systematic guidance for table selection, implementation, and optimization across the spectrum from simple responsive tables to enterprise data grids handling millions of rows.

**Key Challenges:**
- Performance at scale (10 rows vs 10,000 vs 1,000,000)
- Feature complexity (sort, filter, group, edit, export)
- Responsive design (mobile-friendly tables)
- Accessibility (screen readers, keyboard navigation)
- State management (selections, expansions, edits)

**Value Proposition:**
- Clear decision framework: Data volume → Feature needs → Implementation tier
- Performance optimization strategies for each scale
- Comprehensive accessibility patterns
- Modern UX best practices (2024-2025)

---

## Table of Contents

1. [Component Taxonomy](#component-taxonomy)
2. [Selection Decision Framework](#selection-decision-framework)
3. [Performance Tiers](#performance-tiers)
4. [Feature Catalog](#feature-catalog)
5. [Accessibility Requirements](#accessibility-requirements)
6. [Responsive Strategies](#responsive-strategies)
7. [Implementation Patterns](#implementation-patterns)
8. [Skill Structure](#skill-structure)

---

## Component Taxonomy

### Tier 1: Basic Tables (<100 rows)

**Simple Responsive Table**
- Plain HTML `<table>`
- Responsive via card stacking or horizontal scroll
- No JavaScript required
- Perfect for: Documentation, simple lists, content pages

**Sortable Table**
- Click column headers to sort
- Visual indicators (↑↓ arrows)
- Client-side sorting
- Perfect for: Product lists, directories, reports

**Striped/Hover Table**
- Alternating row colors
- Hover highlighting
- Improved scannability
- Perfect for: Dense data, comparison tasks

---

### Tier 2: Interactive Tables (100-10,000 rows)

**Filterable Table**
- Column filters (text, select, range)
- Global search
- Client or server-side filtering
- Perfect for: Searchable lists, inventory, customer tables

**Paginated Table**
- Page size selection (10, 25, 50, 100)
- Page navigation (first, prev, next, last)
- Client or server-side pagination
- Perfect for: Large datasets, reducing initial load

**Editable Table**
- Inline editing (click to edit cells)
- Row-level or cell-level editing
- Validation and error handling
- Perfect for: Data entry, spreadsheet-like interfaces

**Selectable Table**
- Row selection (single or multi)
- Select all/none
- Bulk actions on selected
- Perfect for: Batch operations, delete, export, move

---

### Tier 3: Advanced Data Grids (10,000+ rows)

**Virtual Scrolling Table**
- Renders only visible rows
- Infinite scroll feel
- Handles 100,000+ rows smoothly
- Perfect for: Large datasets, real-time data, logs

**Grouped/Aggregated Table**
- Group by column values
- Expandable/collapsible groups
- Aggregate functions (sum, avg, count)
- Perfect for: Hierarchical data, pivot tables, reports

**Tree Table**
- Parent-child relationships
- Expand/collapse nested rows
- Indentation visualization
- Perfect for: File systems, org charts, threaded data

**Spreadsheet-like Grid**
- Excel-like keyboard navigation
- Formula support
- Cell formatting
- Copy/paste from Excel
- Perfect for: Financial data, complex data entry

---

## Selection Decision Framework

### Primary Decision Tree

```
START: How many rows?

├─→ <100 ROWS (Simple)
│   ├─ Read-only? → Simple Responsive Table
│   ├─ Need sorting? → Sortable Table
│   ├─ Need filtering? → Filterable Table (client-side)
│   └─ Need editing? → Editable Table (simple)

├─→ 100-1,000 ROWS (Interactive)
│   ├─ Read-only?
│   │   ├─ Need pagination? → Paginated Table (client-side)
│   │   └─ Need filtering? → Filterable + Paginated
│   ├─ Need selections? → Selectable Table + features
│   ├─ Need editing? → Editable Table (with validation)
│   └─ Need grouping? → Grouped Table (client-side)

├─→ 1,000-10,000 ROWS (Enhanced)
│   ├─ Move to server-side operations
│   │   ├─ Server-side pagination
│   │   ├─ Server-side filtering
│   │   ├─ Server-side sorting
│   │   └─ Consider virtual scrolling
│   └─ Use data grid library (AG Grid, TanStack Table)

├─→ 10,000-100,000 ROWS (Advanced)
│   ├─ Virtual scrolling REQUIRED
│   ├─ Server-side everything
│   ├─ Progressive loading
│   ├─ Consider: AG Grid, React Virtual, TanStack Virtual
│   └─ Optimize backend queries (indexing, caching)

└─→ >100,000 ROWS (Enterprise)
    ├─ Virtual scrolling
    ├─ Server-side aggregation
    ├─ Database-level filtering
    ├─ Consider: Streaming, web workers, WebAssembly
    └─ Enterprise grid: AG Grid Enterprise, Handsontable
```

---

### Feature Decision Matrix

| Need | <100 rows | 100-1k | 1k-10k | 10k+ |
|------|-----------|--------|--------|------|
| **Sorting** | Client JS | Client | Server | Server |
| **Filtering** | Client | Client | Server | Server |
| **Pagination** | Optional | Client | Server | Virtual Scroll |
| **Search** | Client | Client | Server | Server + Index |
| **Editing** | Simple | Validated | Server sync | Optimistic UI |
| **Selection** | Simple | Multi + bulk | Multi | Multi virtual |
| **Grouping** | Client | Client | Server | Server aggregate |
| **Export** | Client CSV | Client | Server | Server stream |

---

## Performance Tiers

### Tier 1: Client-Side (< 1,000 rows)

**Approach:** Load all data, operate in browser

**Techniques:**
- Standard React rendering
- `array.sort()`, `array.filter()` for operations
- LocalStorage for state persistence
- Minimal optimization needed

**Performance Targets:**
- Initial render: <100ms
- Sort/filter: <50ms
- Feels instant

---

### Tier 2: Server-Side (1,000-10,000 rows)

**Approach:** Backend handles operations, return pages

**Techniques:**
- API pagination: `?page=2&limit=50`
- API filtering: `?search=query&category=X`
- API sorting: `?sort=name&order=asc`
- Backend indexing for speed
- Caching frequent queries

**Performance Targets:**
- API response: <200ms
- Page change: <300ms
- Filter/sort: <500ms

---

### Tier 3: Virtual Scrolling (10,000+ rows)

**Approach:** Render only visible rows (viewport)

**Techniques:**
- React Virtual, TanStack Virtual, or react-window
- Render 10-20 rows (visible) instead of 10,000
- Recycle DOM nodes as user scrolls
- Windowing algorithm

**Performance Targets:**
- Smooth 60fps scrolling
- Constant memory usage
- Instant re-renders

**Example:**
```
Total rows: 50,000
Visible rows: 20 (at any time)
DOM nodes: 20-30 (with buffer)
Memory: Constant, not scaling with rows
```

---

### Tier 4: Extreme Scale (100,000+ rows)

**Approach:** Hybrid strategies, extreme optimization

**Techniques:**
- Virtual scrolling + server-side filtering
- Web Workers for data processing
- WebAssembly for computations
- Streaming data (render as arrives)
- Database-level aggregation
- Materialized views/caching

**Performance Targets:**
- First render: <1s
- Scroll: 60fps
- Filter/sort: <2s

---

## Feature Catalog

### Sorting

**Single Column Sort**
- Click header to sort
- Toggle asc/desc/none
- Visual indicator (arrow icons)
- Keyboard accessible (Enter/Space)

**Multi-Column Sort**
- Shift+click to add columns
- Visual priority indicators (1, 2, 3)
- Complex sort logic
- Clear all option

**Custom Sort Logic**
- Numerical vs alphabetical
- Date/time sorting
- Natural sort ("File 2" before "File 10")
- Null handling (first, last, or ignore)

---

### Filtering

**Column Filters**
- Text input (contains, exact, starts with)
- Dropdown (single select)
- Multi-select (checkbox list)
- Range (min-max for numbers/dates)
- Boolean (true/false/both)

**Global Search**
- Search across all columns
- Highlight matches
- Debounced input (300ms)
- Clear button

**Advanced Filters**
- Boolean logic (AND/OR)
- Nested conditions
- Save filter presets
- Filter chips (active filters)
- Quick filters (pre-defined)

---

### Pagination

**Client-Side Pagination**
- Page size selector
- Page navigation (1, 2, 3...)
- First/Previous/Next/Last buttons
- "Showing X-Y of Z results"
- Jump to page input

**Server-Side Pagination**
- Backend calculates pages
- Total count from API
- Loading states
- URL params for deep linking
- Prefetch next page

**Infinite Scroll**
- Load more on scroll bottom
- "Load More" button (fallback)
- Loading spinner
- End indicator ("No more results")

---

### Selection

**Single Selection**
- Radio buttons (column 1)
- Click row to select
- Visual highlight
- Access selected via callback

**Multi-Selection**
- Checkboxes (column 1)
- Shift+click for range
- Ctrl/Cmd+click for individual
- Select all/none header checkbox
- "X items selected" indicator

**Bulk Actions**
- Action toolbar when items selected
- Delete, export, move, edit
- Confirmation dialogs
- Clear selection after action

---

### Editing

**Inline Editing**
- Click cell to edit
- Tab to next cell
- Enter to save, Esc to cancel
- Validation on blur
- Error indicators

**Row Editing**
- Edit entire row at once
- Edit/Save/Cancel buttons
- Optimistic UI updates
- Rollback on error
- Dirty state indicator

**Modal Editing**
- Open form in modal
- Complex multi-field edits
- Better for mobile
- Validation before submit

---

### Grouping

**Simple Grouping**
- Group by single column
- Expand/collapse groups
- Group headers
- Item count per group

**Nested Grouping**
- Group by multiple columns
- Hierarchical structure
- Expand all/collapse all
- Indentation visualization

**Aggregations**
- Sum, average, count, min, max
- Shown in group footer
- Custom aggregation functions
- Grand totals row

---

### Export

**CSV Export**
- Export visible data
- Export all data
- Custom column selection
- Encoding handling (UTF-8)

**Excel Export**
- .xlsx format
- Formatted cells
- Multiple sheets
- Formulas (if applicable)

**PDF Export**
- Formatted table layout
- Page breaks
- Headers/footers
- Landscape mode for wide tables

**Clipboard Copy**
- Copy selected rows
- Copy entire table
- Paste into Excel
- Preserve formatting

---

## Accessibility Requirements

### Semantic HTML

```html
<table role="grid">
  <caption>Employee Directory</caption>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Role</th>
      <th scope="col">Department</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>John Doe</td>
      <td>Engineer</td>
      <td>Product</td>
    </tr>
  </tbody>
</table>
```

**Required Elements:**
- `<caption>` for table title
- `<thead>`, `<tbody>`, `<tfoot>` structure
- `<th scope="col">` for column headers
- `<th scope="row">` for row headers (if applicable)

---

### ARIA for Interactive Tables

**Data Grid Pattern (role="grid"):**
```html
<table role="grid" aria-labelledby="table-title">
  <thead>
    <tr>
      <th role="columnheader" aria-sort="ascending">Name</th>
      <th role="columnheader">Email</th>
    </tr>
  </thead>
  <tbody>
    <tr role="row">
      <td role="gridcell" tabindex="0">Alice</td>
      <td role="gridcell" tabindex="-1">alice@example.com</td>
    </tr>
  </tbody>
</table>
```

**Attributes:**
- `role="grid"` for interactive tables
- `role="gridcell"` for focusable cells
- `aria-sort="ascending|descending|none"` on sorted column
- `aria-rowcount`, `aria-colcount` for virtual scrolling
- `aria-selected="true"` for selected rows

---

### Keyboard Navigation

**Essential:**
- **Tab**: Move between interactive elements
- **Enter/Space**: Activate buttons, toggle checkboxes
- **Arrow keys**: Navigate cells (grid role)
- **Home/End**: First/last row or cell
- **Page Up/Down**: Scroll by page

**Advanced:**
- **Ctrl+Home**: First cell in grid
- **Ctrl+End**: Last cell in grid
- **Ctrl+A**: Select all
- **Escape**: Cancel editing, clear selection

---

### Screen Reader Support

**Announcements:**
- "Sorted by Name, ascending"
- "Filtered by Department: Engineering"
- "3 of 50 items selected"
- "Row 5 of 100"
- "Loading more results..."

**Techniques:**
- `aria-live="polite"` for status messages
- `aria-busy="true"` during loading
- `aria-label` for icon buttons
- `aria-describedby` for help text

---

## Responsive Strategies

### Strategy 1: Horizontal Scroll

**Approach:** Allow table to scroll horizontally
```css
.table-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch; /* iOS smooth scroll */
}
```

**Pros:**
- Simple to implement
- Preserves table structure
- Works for all tables

**Cons:**
- Hidden columns not obvious
- Horizontal scrolling awkward
- Not ideal for mobile

---

### Strategy 2: Card Stack (Mobile)

**Approach:** Transform rows into cards on small screens

**Desktop:**
```
| Name    | Email           | Role      |
| Alice   | alice@x.com     | Engineer  |
| Bob     | bob@x.com       | Designer  |
```

**Mobile:**
```
┌────────────────────┐
│ Name: Alice        │
│ Email: alice@x.com │
│ Role: Engineer     │
└────────────────────┘
┌────────────────────┐
│ Name: Bob          │
│ Email: bob@x.com   │
│ Role: Designer     │
└────────────────────┘
```

**Pros:**
- Excellent mobile experience
- All data visible without scrolling
- Clear reading flow

**Cons:**
- More implementation work
- Different layouts by breakpoint

---

### Strategy 3: Priority Columns

**Approach:** Hide less important columns on small screens

```css
/* Hide on mobile */
@media (max-width: 768px) {
  th.optional, td.optional {
    display: none;
  }
}
```

**Enhance with:** "Show more columns" button

**Pros:**
- Table structure preserved
- Simple CSS solution
- Progressive enhancement

**Cons:**
- Data hidden from users
- Requires column prioritization

---

### Strategy 4: Truncate + Expand

**Approach:** Truncate cell content, click to expand

**Pros:**
- Keeps table compact
- All data accessible
- Good for variable content length

**Cons:**
- Extra clicks required
- Not ideal for scanability

---

## Implementation Patterns

### Recommended Libraries

**React:**
- **TanStack Table** (formerly React Table): Headless, flexible, popular
- **AG Grid**: Feature-rich enterprise grid (free & paid tiers)
- **Material-UI Data Grid**: Polished, integrated with MUI
- **React Data Grid**: Spreadsheet-like, Excel features
- **Handsontable**: Excel replacement, commercial

**Vue:**
- **AG Grid**: Also supports Vue
- **Vuetify Data Table**: Material Design
- **PrimeVue DataTable**: Feature-rich

**Framework-Agnostic:**
- **Tabulator**: Pure JS, extensive features
- **DataTables**: jQuery classic (still used widely)

---

### Basic Implementation Pattern (React)

```tsx
import { useTable, useSortBy, useFilters, usePagination } from '@tanstack/react-table';

function DataTable({ data, columns }) {
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    page,
    prepareRow,
    state: { pageIndex, pageSize },
  } = useTable(
    { columns, data, initialState: { pageIndex: 0 } },
    useFilters,
    useSortBy,
    usePagination
  );

  return (
    <table {...getTableProps()}>
      <thead>
        {headerGroups.map(headerGroup => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map(column => (
              <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                {column.render('Header')}
                <span>
                  {column.isSorted ? (column.isSortedDesc ? ' 🔽' : ' 🔼') : ''}
                </span>
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody {...getTableBodyProps()}>
        {page.map(row => {
          prepareRow(row);
          return (
            <tr {...row.getRowProps()}>
              {row.cells.map(cell => (
                <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
              ))}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
```

---

## Before Implementation: Library Validation

**Optional but Recommended:** Before implementing, see `../RESEARCH_GUIDE.md` for methodology to validate these library recommendations using available research tools (Google Search Grounding, Context7). This ensures you're using the latest, most secure versions.

**Note:** The recommendations below were researched comprehensively in November 2025 and are production-ready. Validation is optional.

---

## Recommended Libraries & Tools

### React Table Libraries (2025)

#### **Primary: TanStack Table** (Recommended - Headless)

**Library:** `/tanstack/table`
**Trust Score:** 8/10
**Code Snippets:** 661+

**Why TanStack Table?**
- **Headless UI**: 100% control over markup and styling
- **Framework Agnostic**: Works with React, Vue, Solid, Svelte
- **TypeScript First**: Excellent type inference
- **Feature Rich**: Sorting, filtering, pagination, grouping, virtualization
- **Small Bundle**: ~15KB (core logic only)
- **Flexible**: From simple to complex use cases

**When to Use:**
- Want complete control over UI/styling
- Need custom table designs
- TypeScript projects
- Building design system
- Any data volume (supports virtualization)

**Installation:**
```bash
npm install @tanstack/react-table
```

**Basic Example:**
```tsx
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  flexRender,
} from '@tanstack/react-table';

function DataTable({ data, columns }) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <table>
      <thead>
        {table.getHeaderGroups().map(headerGroup => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map(header => (
              <th key={header.id}>
                {flexRender(header.column.columnDef.header, header.getContext())}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody>
        {table.getRowModel().rows.map(row => (
          <tr key={row.id}>
            {row.getVisibleCells().map(cell => (
              <td key={cell.id}>
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

---

#### **Enterprise: AG Grid** (Feature-Rich Commercial)

**Trust Score:** High (industry standard)

**Why AG Grid?**
- **Enterprise Features**: Pivoting, charting, grouping, aggregation
- **High Performance**: Handles millions of rows
- **Feature Complete**: Everything built-in
- **Commercial Support**: Enterprise license available
- **Excel-like UX**: Familiar to users

**Versions:**
- **Community (Free)**: Sorting, filtering, pagination, editing, selection
- **Enterprise (Paid)**: Advanced features (row grouping, pivoting, charts, server-side row model)

**When to Use:**
- Enterprise applications
- Need advanced features (pivoting, charting)
- Commercial support required
- Budget allows for licensing

**Installation:**
```bash
npm install ag-grid-react ag-grid-community
```

---

### Virtual Scrolling (10K+ Rows)

#### **TanStack Virtual**

**Library:** Part of TanStack ecosystem
**Integration:** Works seamlessly with TanStack Table

```bash
npm install @tanstack/react-virtual
```

**Pattern:**
```tsx
import { useVirtualizer } from '@tanstack/react-virtual';
import { useReactTable } from '@tanstack/react-table';

function VirtualizedTable({ data, columns }) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  const { rows } = table.getRowModel();

  const parentRef = useRef();

  const virtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 35, // estimated row height
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map(virtualRow => {
          const row = rows[virtualRow.index];
          return (
            <div
              key={row.id}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: `${virtualRow.size}px`,
                transform: `translateY(${virtualRow.start}px)`,
              }}
            >
              {/* Render row */}
            </div>
          );
        })}
      </div>
    </div>
  );
}
```

---

### Library Comparison Matrix

| Library | Flexibility | Features | Performance | Bundle Size | License | Best For |
|---------|-------------|----------|-------------|-------------|---------|----------|
| **TanStack Table** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ~15KB | MIT | Custom designs |
| **AG Grid Community** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Large | MIT | Standard features |
| **AG Grid Enterprise** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Large | Commercial | Enterprise apps |
| **Material-UI DataGrid** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Medium | MIT/Commercial | Material Design |
| **React Data Grid** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Medium | Commercial | Excel-like |

---

### Recommendation by Use Case

**Custom Design / Design System → TanStack Table**
- Complete styling control
- Headless architecture
- Flexible integration

**Enterprise Features / Excel-like → AG Grid**
- Pivoting and aggregation
- Built-in charting
- Commercial support

**Material Design → MUI X Data Grid**
- Integrates with MUI components
- Polished out-of-box
- Free and Pro tiers

**Quick Prototype → Basic HTML Table + Library**
- Use browser-native features
- Progressive enhancement
- Minimal dependencies

---

## Styling & Theming

### Design Token Integration

All table and data grid components use the **design-tokens** skill for visual styling, enabling consistent design, theme switching, and brand customization.

**See:** `skills/design-tokens/` for complete theming documentation.

### Token Categories Used

**Color Tokens:**
- `--table-bg` - Table background color
- `--table-header-bg` - Header row background
- `--table-row-bg-even` - Even row background (striping)
- `--table-row-bg-odd` - Odd row background
- `--table-row-bg-hover` - Row hover state
- `--table-row-bg-selected` - Selected row background
- `--table-border-color` - Cell borders
- `--table-text-color` - Cell text color
- `--table-header-text-color` - Header text color
- `--table-sort-icon-color` - Sort indicator color

**Spacing Tokens:**
- `--table-cell-padding-x` - Horizontal cell padding
- `--table-cell-padding-y` - Vertical cell padding
- `--table-header-padding-y` - Header cell vertical padding
- `--table-row-gap` - Space between rows (if not using borders)

**Typography Tokens:**
- `--table-font-size` - Cell text size
- `--table-header-font-size` - Header text size
- `--table-header-font-weight` - Header text weight
- `--table-line-height` - Cell line height

**Border Tokens:**
- `--table-border-width` - Cell border thickness
- `--table-outer-border-width` - Table outer border
- `--table-border-radius` - Table corner radius

**Shadow Tokens:**
- `--table-shadow` - Table elevation shadow
- `--table-header-shadow` - Sticky header shadow

### Component-Specific Tokens

```css
/* Basic Table */
--table-bg: var(--color-white);
--table-border-color: var(--color-gray-300);
--table-border-width: 1px;
--table-cell-padding-x: var(--spacing-md);
--table-cell-padding-y: var(--spacing-sm);
--table-font-size: var(--font-size-sm);

/* Table Header */
--table-header-bg: var(--color-gray-50);
--table-header-text-color: var(--color-text-primary);
--table-header-font-weight: var(--font-weight-semibold);
--table-header-padding-y: var(--spacing-md);

/* Row States */
--table-row-bg-even: var(--color-white);
--table-row-bg-odd: var(--color-gray-50);
--table-row-bg-hover: var(--color-gray-100);
--table-row-bg-selected: var(--color-primary-50);

/* Sortable Headers */
--table-sort-icon-color: var(--color-text-secondary);
--table-sort-active-color: var(--color-primary);

/* Table Container */
--table-shadow: var(--shadow-md);
--table-border-radius: var(--radius-md);
```

### Theme Support

- ✅ **Light Mode** - Clean, readable tables
- ✅ **Dark Mode** - Adjusted backgrounds and borders for dark interfaces
- ✅ **High Contrast** - Strong borders and text contrast for accessibility
- ✅ **Striped Rows** - Even/odd row coloring for scannability
- ✅ **Custom Brand Themes** - Match table design to brand identity

### Example: Custom Table Theming

```css
/* Dense, compact table theme */
:root[data-theme="compact-table"] {
  /* Tighter spacing */
  --table-cell-padding-x: var(--spacing-sm);
  --table-cell-padding-y: var(--spacing-xs);

  /* Smaller text */
  --table-font-size: var(--font-size-xs);

  /* Minimal borders */
  --table-border-width: 0;
  --table-row-gap: 1px;
}

/* Elevated, card-like table theme */
:root[data-theme="card-table"] {
  /* Generous spacing */
  --table-cell-padding-x: var(--spacing-lg);
  --table-cell-padding-y: var(--spacing-md);

  /* Strong elevation */
  --table-shadow: var(--shadow-xl);

  /* Rounded corners */
  --table-border-radius: var(--radius-lg);

  /* No striping, rely on shadow */
  --table-row-bg-even: var(--color-white);
  --table-row-bg-odd: var(--color-white);
}
```

### Dark Mode Considerations

```css
:root[data-theme="dark"] {
  --table-bg: var(--color-gray-900);
  --table-header-bg: var(--color-gray-800);
  --table-border-color: var(--color-gray-700);
  --table-row-bg-even: var(--color-gray-900);
  --table-row-bg-odd: var(--color-gray-850);
  --table-row-bg-hover: var(--color-gray-800);
  --table-row-bg-selected: var(--color-primary-900);
  --table-text-color: var(--color-gray-100);

  /* Softer shadows in dark mode */
  --table-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
}
```

### Accessibility via Tokens

- **High Contrast Mode**: Strong cell borders and text contrast
- **Focus Indicators**: Visible focus states for keyboard navigation
- **Row Striping**: Alternating colors improve scannability
- **Hover States**: Clear visual feedback for interactive tables

---

## Skill Structure

```
tables/
├── SKILL.md (decision framework, quick start)
├── references/
│   ├── basic-tables.md (simple, sortable, striped)
│   ├── interactive-tables.md (filterable, paginated, editable, selectable)
│   ├── advanced-grids.md (virtual scrolling, grouped, tree, spreadsheet)
│   ├── performance-optimization.md (tiers, strategies, benchmarks)
│   ├── features/
│   │   ├── sorting.md
│   │   ├── filtering.md
│   │   ├── pagination.md
│   │   ├── selection.md
│   │   ├── editing.md
│   │   ├── grouping.md
│   │   └── export.md
│   ├── accessibility.md (WCAG, ARIA, keyboard, screen readers)
│   ├── responsive-strategies.md (4 approaches)
│   └── library-comparison.md (TanStack, AG Grid, MUI, etc.)
├── examples/
│   ├── simple-table.tsx
│   ├── sortable-table.tsx
│   ├── paginated-table.tsx
│   ├── virtual-scrolling.tsx
│   └── full-featured-grid.tsx
└── scripts/
    ├── generate_mock_data.py (for testing)
    └── benchmark_table.js (performance testing)
```

### SKILL.md Frontmatter

```yaml
---
name: tables-data-grids
description: Comprehensive component library for tables and data grids. Use when displaying tabular data, building data tables, creating spreadsheet-like interfaces, or presenting structured information. Covers simple HTML tables to enterprise data grids with sorting, filtering, pagination, inline editing, row selection, grouping, virtual scrolling, and export features. Includes performance optimization strategies for datasets from 10 to 1,000,000+ rows, accessibility patterns (WCAG, ARIA grid), responsive design strategies, and modern UX best practices. Triggered by requests to: create table, display data grid, build spreadsheet, implement sorting/filtering, handle large datasets, or design data-heavy interfaces.
---
```

---

**END OF MASTER PLAN**

*This document serves as the foundation for building a comprehensive tables and data grids skill. Tables are the second most common data display pattern - mastering them is essential for any UI component library.*
