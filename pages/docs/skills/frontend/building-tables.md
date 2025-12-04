---
sidebar_position: 4
title: Building Tables
description: Tables and data grids from simple HTML to enterprise grids handling millions of rows
tags: [frontend, tables, data-grids, performance]
---

# Building Tables & Data Grids

Systematic creation of tables and data grids from simple HTML tables to enterprise-scale virtualized grids handling millions of rows.

## When to Use

Use this skill when:
- Creating tables, data grids, or spreadsheet-like interfaces
- Displaying tabular or structured data
- Implementing sorting, filtering, or pagination features
- Handling large datasets or addressing performance concerns
- Building inline editing or data entry interfaces
- Requiring row selection or bulk operations
- Implementing data export (CSV, Excel, PDF)
- Ensuring table accessibility or responsive behavior

## Quick Decision Framework

Select implementation tier based on data volume:

```
&lt;100 rows        → Simple HTML table with progressive enhancement
100-1,000 rows   → Client-side features (sort, filter, paginate)
1,000-10,000     → Server-side operations with API pagination
10,000-100,000   → Virtual scrolling with windowing
>100,000 rows    → Enterprise grid with streaming and workers
```

## Core Implementation Patterns

### Tier 1: Basic Tables (&lt;100 rows)
For simple, read-only data display:
- Use semantic HTML `&lt;table>` structure
- Add responsive behavior via CSS
- Implement client-side sorting if needed

### Tier 2: Interactive Tables (100-10K rows)
For feature-rich interactions:
- Add filtering, pagination, and selection
- Implement inline or modal editing
- Use client-side operations up to 1K rows
- Switch to server-side beyond 1K rows

### Tier 3: Advanced Grids (10K+ rows)
For massive datasets:
- Implement virtual scrolling
- Use server-side aggregation
- Add grouping and hierarchies
- Consider enterprise solutions

## Performance Optimization

Critical performance thresholds:
- Client-side operations: &lt;1,000 rows (instant, &lt;50ms)
- Server-side operations: 1,000-10,000 rows (&lt;200ms API)
- Virtual scrolling: 10,000+ rows (60fps, constant memory)
- Streaming: 100,000+ rows (progressive rendering)

## Feature Implementation

### Sorting
- Single or multi-column sorting
- Custom sort logic (numeric, date, natural)
- Visual indicators and keyboard support

### Filtering & Search
- Column-specific filters (text, range, select)
- Global search across all columns
- Advanced filter logic (AND/OR)

### Pagination
- Client-side for small datasets
- Server-side for large datasets
- Infinite scroll alternative

### Selection & Bulk Actions
- Single or multi-row selection
- Range selection (Shift+click)
- Bulk operations toolbar

### Inline Editing
- Cell-level or row-level editing
- Validation and error handling
- Optimistic updates

## Accessibility Requirements

Essential WCAG compliance:
- Semantic HTML with proper structure
- ARIA grid pattern for interactive tables
- Full keyboard navigation
- Screen reader announcements

## Responsive Design Strategies

1. **Horizontal scroll** - Simple, preserves structure
2. **Card stack** - Transform rows to cards on mobile
3. **Priority columns** - Hide less important columns
4. **Truncate & expand** - Compact with details on demand

## Library Recommendations

### Primary: TanStack Table (Headless)
Best for custom designs and complete control:
- TypeScript-first with excellent DX
- Small bundle size (~15KB)
- Framework agnostic
- Virtual scrolling support

```bash
npm install @tanstack/react-table
```

### Enterprise: AG Grid
Best for feature-complete solutions:
- Handles millions of rows
- Built-in advanced features
- Community (free) + Enterprise (paid)
- Excel-like user experience

```bash
npm install ag-grid-react
```

## Design Token Integration

Tables use the design-tokens skill for consistent theming:
- Color tokens for backgrounds, borders, and states
- Spacing tokens for cell padding
- Typography tokens for text styling
- Shadow tokens for elevation

Supports light, dark, high-contrast, and custom themes.

## Related Skills

- [Theming Components](./theming-components.md) - Table styling with design tokens
- [Visualizing Data](./visualizing-data.md) - Complementary data visualization
- [Implementing Search Filter](./implementing-search-filter.md) - Search and filter functionality
- [Creating Dashboards](./creating-dashboards.md) - Tables within dashboard widgets

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/building-tables)
- Selection: `references/selection-framework.md`
- Implementation: `references/basic-tables.md`, `references/interactive-tables.md`, `references/advanced-grids.md`
- Features: `references/sorting-filtering.md`, `references/pagination-strategies.md`
- Optimization: `references/performance-optimization.md`
- Accessibility: `references/accessibility-patterns.md`
