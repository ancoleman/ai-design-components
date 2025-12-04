---
sidebar_position: 5
title: Creating Dashboards
description: Comprehensive dashboard interfaces combining data visualization, KPI cards, and real-time updates
tags: [frontend, dashboards, analytics, real-time]
---

# Creating Dashboards

Creates sophisticated dashboard interfaces that aggregate and present data through coordinated widgets including KPI cards, charts, tables, and filters.

## When to Use

Use this skill when:
- Building business intelligence or analytics dashboards
- Creating executive reporting interfaces
- Implementing real-time monitoring systems
- Designing KPI displays with metrics and trends
- Developing customizable widget-based layouts
- Coordinating filters across multiple data displays
- Building responsive data-heavy interfaces
- Creating template-based analytics systems

## Overview

Dashboards serve as centralized command centers for data-driven decision making, combining multiple component types from other skills (data-viz, tables, design-tokens) into unified analytics experiences with real-time updates, responsive layouts, and interactive filtering.

## Core Dashboard Elements

### KPI Card Anatomy
```
┌────────────────────────────┐
│ Revenue (This Month)       │ ← Label with time period
│                            │
│  $1,245,832               │ ← Big number (primary metric)
│  ↑ 15.3% vs last month    │ ← Trend indicator with comparison
│  ▂▃▅▆▇█ (sparkline)       │ ← Mini visualization
└────────────────────────────┘
```

### Widget Container Structure
- Title bar with widget name and actions
- Loading state (skeleton or spinner)
- Error boundary with retry option
- Resize handles for adjustable layouts
- Settings menu (export, configure, refresh)

### Dashboard Layout Types
- **Fixed Layout**: Designer-defined placement, consistent across users
- **Customizable Grid**: User drag-and-drop, resizable widgets, saved layouts
- **Template-Based**: Pre-built patterns, industry-specific starting points

## Implementation Approach

### 1. Choose Dashboard Architecture

**For Quick Analytics Dashboard → Use Tremor**
Pre-built KPI cards, charts, and tables with minimal code:
```bash
npm install @tremor/react
```

**For Customizable Dashboard → Use react-grid-layout**
Drag-and-drop, resizable widgets, user-defined layouts:
```bash
npm install react-grid-layout
```

### 2. Set Up Global State Management

Implement filter context for cross-widget coordination:
```tsx
const DashboardContext = createContext({
  filters: { dateRange: null, categories: [] },
  setFilters: () => {},
  refreshInterval: 30000
});
```

### 3. Configure Real-Time Updates

**Server-Sent Events (Recommended for Dashboards)**:
```tsx
const eventSource = new EventSource('/api/dashboard/stream');
eventSource.onmessage = (event) => {
  const update = JSON.parse(event.data);
  updateWidget(update.widgetId, update.data);
};
```

## Quick Start with Tremor

```tsx
import { Card, Grid, Metric, Text, BadgeDelta, AreaChart } from '@tremor/react';

function QuickDashboard({ data }) {
  return (
    &lt;Grid numItems={1} numItemsSm={2} numItemsLg={4} className="gap-4">
      &lt;Card>
        &lt;Text>Total Revenue&lt;/Text>
        &lt;Metric>$45,231.89&lt;/Metric>
        &lt;BadgeDelta deltaType="increase">+12.5%&lt;/BadgeDelta>
      &lt;/Card>

      &lt;Card className="lg:col-span-2">
        &lt;Text>Revenue Trend&lt;/Text>
        &lt;AreaChart
          data={data.revenue}
          index="date"
          categories={["revenue"]}
        />
      &lt;/Card>
    &lt;/Grid>
  );
}
```

## Performance Optimization

### Lazy Loading Strategy
```tsx
&lt;LazyLoad height={widget.height} offset={100}>
  &lt;Widget {...widget} />
&lt;/LazyLoad>
```

### Parallel Data Fetching
```tsx
const loadDashboard = async () => {
  const [kpis, charts, tables] = await Promise.all([
    fetchKPIs(),
    fetchChartData(),
    fetchTableData()
  ]);
  return { kpis, charts, tables };
};
```

### Widget-Level Caching
Cache data at widget level with TTL to reduce API calls.

## Cross-Skill Integration

### Using Data Visualization Components
Reference the data-viz skill for chart widgets:
```tsx
import { createChart } from '../data-viz/chart-factory';
```

### Integrating Data Tables
Reference the tables skill for data grids:
```tsx
import { DataGrid } from '../tables/data-grid';
```

### Applying Design Tokens
Use design tokens for consistent theming:
```tsx
const dashboardTokens = {
  '--dashboard-bg': 'var(--color-bg-secondary)',
  '--widget-bg': 'var(--color-white)',
  '--kpi-value-size': 'var(--font-size-4xl)',
};
```

## Library Selection Guide

### Choose Tremor When:
- Need to build dashboards quickly
- Want pre-styled, professional components
- Using Tailwind CSS in your project
- Building standard analytics interfaces

### Choose react-grid-layout When:
- Users need to customize layouts
- Drag-and-drop is required
- Different users need different views
- Maximum flexibility is priority

### Combine Both When:
- Use Tremor for widget contents (KPIs, charts)
- Use react-grid-layout for layout management

## Related Skills

- [Visualizing Data](./visualizing-data.md) - Chart components for dashboard widgets
- [Building Tables](./building-tables.md) - Data grid widgets
- [Theming Components](./theming-components.md) - Dashboard styling and theming
- [Providing Feedback](./providing-feedback.md) - Loading states and notifications
- [Building Forms](./building-forms.md) - Filter controls and inputs

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/creating-dashboards)
- Patterns: `references/kpi-card-patterns.md`, `references/layout-strategies.md`
- Real-time: `references/real-time-updates.md`, `references/filter-coordination.md`
- Performance: `references/performance-optimization.md`
- Libraries: `references/library-guide.md`
- Examples: `examples/sales-dashboard.tsx`, `examples/monitoring-dashboard.tsx`
