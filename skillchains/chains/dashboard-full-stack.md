# Skill Chain: Dashboard Full Stack

**Complete analytics platform with layout, charts, tables, and filters**

Status: 🚧 Future (Requires: dashboards, tables skills)

---

## Overview

**Chain:** `design-tokens` → `dashboards` + `data-viz` + `tables` + `forms`

**Purpose:** Build complete, production-ready analytics dashboards with layout grid, multiple visualizations, data tables, and interactive filters

**Use Cases:**
- Business intelligence platforms
- Executive dashboards
- SaaS analytics features
- Admin panels
- Reporting systems

---

## Chain Architecture

### Pattern: Parallel Composition with Hub

```
        design-tokens (HUB)
              ↓
    ┌─────────┼─────────┬─────────┐
    ↓         ↓         ↓         ↓
dashboards data-viz  tables   forms
    ↓         ↓         ↓         ↓
  Layout   Charts    Grid    Filters
    └─────────┼─────────┴─────────┘
              ↓
      Complete Dashboard
```

**Coordination:**
- design-tokens: Unified styling (loaded once)
- dashboards: Grid layout system
- data-viz: Multiple chart types
- tables: Data grid display
- forms: Filter controls

---

## Expected User Request

> "Build a complete analytics dashboard with:
> - 3-column layout
> - Revenue chart (bar)
> - Top products chart (pie)
> - Recent transactions table
> - Date range and category filters"

---

## Expected Implementation

### Structure from dashboards Skill

```tsx
<DashboardGrid>
  <DashboardCard span={2}>
    {/* data-viz: Bar chart */}
    <RevenueChart />
  </DashboardCard>

  <DashboardCard span={1}>
    {/* data-viz: Pie chart */}
    <TopProductsChart />
  </DashboardCard>

  <DashboardCard span={3}>
    {/* tables: Data grid */}
    <TransactionsTable />
  </DashboardCard>

  <DashboardFilters>
    {/* forms: Filter controls */}
    <DateRangePicker />
    <CategorySelect />
  </DashboardFilters>
</DashboardGrid>
```

### All Styled by design-tokens

```css
/* dashboards uses */
--dashboard-gap: var(--spacing-lg)
--dashboard-card-bg: var(--color-bg-primary)
--dashboard-card-border: var(--color-border)

/* data-viz uses */
--chart-color-1, --chart-axis-color

/* tables uses */
--table-border-color, --table-row-hover-bg

/* forms uses */
--input-border-color, --button-bg-primary
```

**Result:** Cohesive, themed dashboard

---

## Token Efficiency

**Skills loaded:**
```
design-tokens: 5,000 tokens (hub, loaded once)
dashboards: 5,000 tokens
data-viz: 5,000 tokens
tables: 5,000 tokens
forms: 5,000 tokens

TOTAL: 25,000 tokens
```

**Without chaining:**
```
Each skill with inline theming + layout + coordination:
5 skills × 40,000 tokens = 200,000 tokens

TOTAL: 200,000 tokens
```

**Savings: 175,000 tokens (88%)** 🚀

---

## Key Features

### 1. Responsive Layout (dashboards)
```tsx
// Grid adapts to screen size
<DashboardGrid columns={{ mobile: 1, tablet: 2, desktop: 3 }}>
  {/* Cards use design-tokens for spacing/sizing */}
</DashboardGrid>
```

### 2. Multiple Visualizations (data-viz)
```tsx
// All charts use same color palette
<BarChart>
  <Bar fill="var(--chart-color-1)" />
</BarChart>

<PieChart>
  <Pie fill="var(--chart-color-2)" />
</PieChart>
```

### 3. Data Tables (tables)
```tsx
// Sortable, paginated, themed
<DataTable
  columns={columns}
  data={data}
  // Uses table tokens from design-tokens
/>
```

### 4. Interactive Filters (forms)
```tsx
// Update dashboard in real-time
<FilterBar onFilterChange={handleFilter}>
  <DateRangePicker />
  <CategorySelect />
  <ApplyButton />
</FilterBar>
```

---

## Theme Switching

**All components update together:**

```javascript
// Light mode
setTheme('light');
// → Dashboard layout: white cards
// → Charts: bright colors
// → Tables: light rows
// → Forms: white inputs

// Dark mode
setTheme('dark');
// → Dashboard layout: dark cards
// → Charts: high-contrast colors
// → Tables: dark rows
// → Forms: dark inputs

// Brand theme
setTheme('enterprise');
// → All use brand colors consistently
```

---

## Dependencies

**Required skills:**
- ✅ design-tokens (complete)
- ✅ data-viz (complete)
- ✅ forms (complete)
- 🚧 tables (in progress)
- 🚧 dashboards (in progress)

**Blocking factor:** tables + dashboards completion

**Estimated availability:** 2-3 months

---

## Business Value

**Market:** Very high
- Every SaaS needs dashboards
- BI tools are universal
- Admin panels essential

**Complexity:** Moderate
- 5 skills coordinating
- Well-defined integration points

**Token efficiency:** 88%
- Best ROI for complex applications

**Priority:** **VERY HIGH** 🎯

---

**Status:** 🚧 Planned (waiting on tables + dashboards)
**Token Efficiency:** 88% estimated savings
**Priority:** Very High
**ETA:** Q1 2026 (when dependencies complete)
