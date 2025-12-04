---
sidebar_position: 2
title: Visualizing Data
description: Systematic framework for selecting and implementing data visualizations with 24+ chart types
tags: [frontend, data-viz, charts, accessibility]
---

# Visualizing Data

Systematic guidance for selecting and implementing effective data visualizations, matching data characteristics with appropriate visualization types, ensuring clarity, accessibility, and impact.

## When to Use

Use this skill when:
- Creating visualizations or choosing chart types
- Displaying data graphically in reports or dashboards
- Building data-driven interfaces requiring analytics
- Ensuring visualization accessibility (WCAG 2.1 AA)
- Optimizing performance for large datasets
- Implementing colorblind-safe palettes

## Overview

Data visualization transforms raw data into visual representations that reveal patterns, trends, and insights. This skill provides:

1. **Selection Framework**: Systematic decision trees from data type + purpose → chart type
2. **24+ Visualization Methods**: Organized by analytical purpose
3. **Accessibility Patterns**: WCAG 2.1 AA compliance, colorblind-safe palettes
4. **Performance Strategies**: Optimize for dataset size (&lt;1000 to >100K points)
5. **Multi-Language Support**: JavaScript/TypeScript (primary), Python, Rust, Go

## Quick Start Workflow

### 3-Step Selection Process

1. **Assess Data**: What type? [categorical | continuous | temporal | spatial | hierarchical]
2. **Determine Purpose**: What story? [comparison | trend | distribution | relationship | composition]
3. **Select Chart Type**: Match purpose to visualization

### Quick Selection Guide

- Compare 5-10 categories → Bar Chart
- Show sales over 12 months → Line Chart
- Display distribution of ages → Histogram or Violin Plot
- Explore correlation → Scatter Plot
- Show budget breakdown → Treemap or Stacked Bar

## Purpose-First Selection

| Purpose | Chart Types |
|---------|-------------|
| **Compare values** | Bar Chart, Lollipop Chart |
| **Show trends** | Line Chart, Area Chart |
| **Reveal distributions** | Histogram, Violin Plot, Box Plot |
| **Explore relationships** | Scatter Plot, Bubble Chart |
| **Explain composition** | Treemap, Stacked Bar, Pie Chart (&lt;6 slices) |
| **Visualize flow** | Sankey Diagram, Chord Diagram |
| **Display hierarchy** | Sunburst, Dendrogram, Treemap |
| **Show geographic** | Choropleth Map, Symbol Map |

## Visualization Catalog (3 Tiers)

### Tier 1: Fundamental Primitives
General audiences, straightforward data stories:
- Bar Chart, Line Chart, Scatter Plot, Pie Chart, Area Chart

### Tier 2: Purpose-Driven
Specific analytical insights:
- Comparison: Grouped Bar, Lollipop, Bullet Chart
- Trend: Stream Graph, Slope Graph, Sparklines
- Distribution: Violin Plot, Box Plot, Histogram
- Composition: Treemap, Sunburst, Waterfall

### Tier 3: Advanced
Complex data, sophisticated audiences:
- Parallel Coordinates, Radar Chart, Small Multiples
- Gantt Chart, Calendar Heatmap, Force-Directed Graph

## Accessibility Requirements (WCAG 2.1 AA)

### Essential Patterns
- **Text Alternatives**: aria-label describing insights
- **Color Requirements**: 3:1 minimum contrast, don't rely on color alone
- **Colorblind-Safe Palettes**: IBM palette (Blue, Purple, Magenta, Orange, Yellow)
- **Keyboard Navigation**: Tab through interactive elements, arrow keys for data points

### Avoid
Red/Green combinations (8% of males have red-green colorblindness)

## Performance by Data Volume

| Rows | Strategy | Implementation |
|------|----------|----------------|
| &lt;1,000 | Direct rendering | Standard libraries (SVG) |
| 1K-10K | Sampling/aggregation | Downsample to ~500 points |
| 10K-100K | Canvas rendering | Switch from SVG to Canvas |
| >100K | Server-side aggregation | Backend processing |

## JavaScript/TypeScript Implementation

### Recharts (Business Dashboards)
Composable React components, declarative API, responsive by default.

```tsx
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export function SalesChart() {
  return (
    &lt;ResponsiveContainer width="100%" height={300}>
      &lt;LineChart data={data}>
        &lt;XAxis dataKey="month" />
        &lt;YAxis />
        &lt;Tooltip />
        &lt;Line type="monotone" dataKey="sales" stroke="#8884d8" />
      &lt;/LineChart>
    &lt;/ResponsiveContainer>
  );
}
```

### Other Libraries
- **D3.js**: Maximum flexibility, industry standard
- **Plotly**: 3D visualizations, scientific/interactive charts

## Decision Framework

```
START: What is your data?

Categorical (categories/groups)
  ├─ Compare values → Bar Chart
  ├─ Show composition → Treemap or Pie Chart (&lt;6 slices)
  └─ Show flow → Sankey Diagram

Continuous (numbers)
  ├─ Single variable → Histogram, Violin Plot
  └─ Two variables → Scatter Plot

Temporal (time series)
  ├─ Single metric → Line Chart
  ├─ Multiple metrics → Small Multiples
  └─ Daily patterns → Calendar Heatmap

Hierarchical (nested)
  ├─ Proportions → Treemap
  └─ Show depth → Sunburst, Dendrogram
```

## Related Skills

- [Theming Components](./theming-components.md) - Chart color tokens and theming
- [Creating Dashboards](./creating-dashboards.md) - Integrating charts into dashboards
- [Building Tables](./building-tables.md) - Displaying data in tables vs charts

## References

- [Full Skill Documentation](https://github.com/ancoleman/ai-design-components/tree/main/skills/visualizing-data)
- Selection Guides: `references/chart-catalog.md`, `references/selection-matrix.md`
- Technical: `references/accessibility.md`, `references/color-systems.md`, `references/performance.md`
- Examples: `examples/javascript/` - React, D3.js, Plotly implementations
