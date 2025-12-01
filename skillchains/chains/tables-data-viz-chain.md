# Skill Chain: tables + data-viz

**Data tables with embedded visualizations**

Status: 🚧 Future (Requires: tables skill)

---

## Overview

**Chain:** `design-tokens` → `tables` + `data-viz`

**Purpose:** Display data in tables with embedded charts (sparklines, mini-bars, progress indicators)

**Use Cases:**
- Financial reports with trend indicators
- KPI dashboards with inline metrics
- Product tables with sales charts
- Performance tables with progress bars

---

## Chain Architecture

```
design-tokens (foundation)
      ↓
  ┌───┴───┐
  ↓       ↓
tables  data-viz
  ↓       ↓
 Grid   Charts
  └───┬───┘
      ↓
  Enhanced Table
```

---

## Expected User Request

> "Show a product table with sales trend sparklines in each row"

---

## Expected Implementation

### Table with Embedded Charts

```tsx
<DataTable
  columns={[
    { key: 'product', label: 'Product' },
    { key: 'sales', label: 'Total Sales' },
    {
      key: 'trend',
      label: 'Trend',
      render: (row) => (
        // data-viz: Sparkline chart
        <Sparkline
          data={row.monthlySales}
          width={100}
          height={30}
          stroke="var(--chart-color-1)"
        />
      )
    },
    {
      key: 'progress',
      label: 'Goal',
      render: (row) => (
        // data-viz: Mini progress bar
        <ProgressBar
          value={row.percentToGoal}
          color="var(--chart-color-2)"
        />
      )
    }
  ]}
  data={products}
  // tables + design-tokens: Table styling
/>
```

---

## Token Integration

**Table tokens:**
```css
--table-border-color
--table-header-bg
--table-row-hover-bg
--table-cell-padding-inline
```

**Chart tokens (embedded):**
```css
--chart-color-1
--chart-color-2
```

**Both reference design-tokens** - consistent theming!

---

## Token Efficiency

```
design-tokens: 5,000 tokens
tables: 5,000 tokens
data-viz: 5,000 tokens (for sparklines)

TOTAL: 15,000 tokens
```

**Savings: 75% vs. monolithic table + viz skill**

---

**Status:** 🚧 Future
**Priority:** High
**Dependencies:** tables skill
**ETA:** Q1 2026
