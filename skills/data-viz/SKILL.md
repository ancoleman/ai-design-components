---
name: data-viz
description: This skill should be used when building dashboards, reports, or data-driven interfaces requiring charts, graphs, or visual analytics. Provides systematic framework for selecting appropriate visualizations based on data characteristics and analytical purpose. Includes 24+ visualization types organized by purpose (trends, comparisons, distributions, relationships, flows, hierarchies, geospatial), accessibility patterns (WCAG 2.1 AA compliance), colorblind-safe palettes, and performance optimization strategies. Triggered by requests to create visualizations, choose chart types, display data graphically, or design data interfaces.
---

# Data Visualization Component Library

Assist with selecting and implementing effective data visualizations. Provide systematic guidance for matching data characteristics with appropriate visualization types, ensuring clarity, accessibility, and impact.

## Overview

Data visualization transforms raw data into visual representations that reveal patterns, trends, and insights. This skill provides:

1. **Selection Framework**: Systematic decision trees from data type + purpose → chart type
2. **24+ Visualization Methods**: Organized by analytical purpose (comparison, trend, distribution, relationship, flow, hierarchy)
3. **Accessibility Patterns**: WCAG 2.1 AA compliance, colorblind-safe palettes, screen reader support
4. **Performance Strategies**: Optimize for dataset size (<1000 to >100K points)
5. **Multi-Language Support**: JavaScript/TypeScript (primary), Python, Rust, Go

---

## Universal Visualization Principles (Framework-Agnostic)

These concepts apply regardless of programming language or visualization library.

### 1. Purpose-First Selection

**Match analytical purpose to chart type:**
- **Compare values** → Bar Chart, Lollipop Chart
- **Show trends** → Line Chart, Area Chart
- **Reveal distributions** → Histogram, Violin Plot, Box Plot
- **Explore relationships** → Scatter Plot, Bubble Chart
- **Explain composition** → Treemap, Stacked Bar, Pie Chart (<6 slices)
- **Visualize flow** → Sankey Diagram, Chord Diagram
- **Display hierarchy** → Sunburst, Dendrogram, Treemap
- **Show geographic** → Choropleth Map, Symbol Map

### 2. Data Characteristics Assessment

**Before choosing visualization, assess:**
- **Type**: Categorical, continuous, temporal, spatial, hierarchical?
- **Dimensions**: How many variables? (1D, 2D, multivariate?)
- **Volume**: Data point count? (<100, 100-1K, 1K-10K, >10K)
- **Characteristics**: Outliers, missing values, special patterns?

### 3. Accessibility Requirements (WCAG 2.1 AA)

**All visualizations must include:**

**Text Alternatives:**
```html
<figure role="img" aria-label="Sales increased 15% from Q3 to Q4">
  <svg>...</svg>
</figure>
```

**Color Contrast:**
- Non-text UI elements: 3:1 minimum
- Text: 4.5:1 minimum (or 3:1 for large text ≥24px)

**Don't Rely on Color Alone:**
- Use patterns/textures + color
- Add direct labels to data points
- Provide alternative data table view

**Keyboard Navigation:**
- Tab through interactive elements
- Enter/Space to activate tooltips
- Arrow keys to navigate data points

**Screen Reader Announcements:**
```tsx
<div role="status" aria-live="polite">
  {isLoading ? 'Loading chart...' : 'Chart updated'}
</div>
```

### 4. Colorblind-Safe Palettes

**Use these palettes instead of red/green:**

**IBM Palette (Recommended):**
```
#648FFF (Blue), #785EF0 (Purple), #DC267F (Magenta),
#FE6100 (Orange), #FFB000 (Yellow)
```

**Paul Tol Palette (Scientific):**
```
#4477AA (Blue), #EE6677 (Red), #228833 (Green),
#CCBB44 (Yellow), #66CCEE (Cyan), #AA3377 (Purple)
```

**Avoid:** Red/Green combinations (8% of males have red-green colorblindness)

### 5. Performance by Data Volume

| Rows | Strategy | Implementation |
|------|----------|----------------|
| <1,000 | Direct rendering | Standard libraries (SVG) |
| 1K-10K | Sampling/aggregation | Downsample to ~500 points |
| 10K-100K | Canvas rendering | Switch from SVG to Canvas |
| >100K | Server-side aggregation | Backend processing, send aggregated |

---

## Visualization Catalog (Tier System)

### Tier 1: Fundamental Primitives

**When to use:** General audiences, straightforward data stories, simple comparisons/trends

**Chart Types:**
- **Bar Chart**: Compare categories
- **Line Chart**: Show trends over time
- **Scatter Plot**: Explore relationships between two variables
- **Pie Chart**: Part-to-whole (max 5-6 slices)
- **Area Chart**: Emphasize magnitude over time

### Tier 2: Purpose-Driven Compositions

**When to use:** Specific analytical insights, moderate data literacy audience

**By Purpose:**
- **Comparison**: Grouped Bar, Lollipop, Bullet Chart
- **Trend**: Stream Graph, Slope Graph, Sparklines
- **Distribution**: Violin Plot, Box Plot, Histogram, Ridgeline Plot
- **Relationship**: Bubble Chart, Hexbin Plot, Connected Scatter
- **Composition**: Treemap, Sunburst, Waterfall Chart
- **Flow**: Sankey Diagram, Chord Diagram, Alluvial
- **Hierarchy**: Dendrogram, Circle Packing
- **Geographic**: Choropleth, Symbol Map, Flow Map

### Tier 3: Advanced Analytical Constructs

**When to use:** Complex data, sophisticated audience, interactive exploration needed

**Chart Types:**
- **Multi-dimensional**: Parallel Coordinates, Radar Chart, Small Multiples, SPLOM
- **Temporal**: Gantt Chart, Calendar Heatmap, Horizon Chart, Candlestick
- **Flow**: Sankey, Chord, Arc Diagram
- **Network**: Force-Directed Graph, Adjacency Matrix
- **3D**: Surface Plots (use cautiously, accessibility concerns)

**Detailed descriptions:** See `references/chart-catalog.md`

---

## Quick Start Workflow

### Step 1: Assess Data
```
What type? [categorical | continuous | temporal | spatial | hierarchical]
How many dimensions? [1D | 2D | multivariate]
How many points? [<100 | 100-1K | 1K-10K | >10K]
```

### Step 2: Determine Purpose
```
What story to tell? [comparison | trend | distribution | relationship | composition | flow | hierarchy | geographic]
```

### Step 3: Select Chart Type
Use decision tree (see `references/selection-matrix.md`) or:

**Quick Selection:**
- Compare 5-10 categories → Bar Chart
- Show sales over 12 months → Line Chart
- Display distribution of ages → Histogram or Violin Plot
- Explore correlation between price and sales → Scatter Plot
- Show budget breakdown → Treemap or Stacked Bar

### Step 4: Implement with Language-Specific Library
See language sections below for recommended libraries and code examples.

### Step 5: Apply Accessibility
- Add text alternative (aria-label or long description)
- Ensure color contrast (3:1 minimum)
- Use colorblind-safe palette
- Provide data table alternative
- Test keyboard navigation

### Step 6: Optimize Performance
- <1000 points: Use standard rendering
- >1000 points: Consider sampling or Canvas rendering
- Very large: Server-side aggregation

---

## Language-Specific Implementations

### JavaScript/TypeScript (Primary)

#### Recommended Libraries

**For Business Dashboards: Recharts**
- Composable React components
- Declarative API
- Responsive by default
- 15+ standard chart types

**Installation:**
```bash
npm install recharts
```

**Example - Line Chart:**
```tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const salesData = [
  { month: 'Jan', sales: 4000 },
  { month: 'Feb', sales: 3000 },
  { month: 'Mar', sales: 5000 },
];

export function SalesChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={salesData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="sales" stroke="#8884d8" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

**Example - Bar Chart:**
```tsx
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export function RevenueChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="category" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="revenue" fill="#3B82F6" />
        <Bar dataKey="expenses" fill="#EF4444" />
      </BarChart>
    </ResponsiveContainer>
  );
}
```

---

**For Custom Visualizations: D3.js**
- Maximum flexibility and control
- Industry standard
- Unlimited chart types

**Installation:**
```bash
npm install d3
```

**Example - Custom Scatter Plot:**
```tsx
import * as d3 from 'd3';
import { useRef, useEffect } from 'react';

export function D3ScatterPlot({ data, width = 600, height = 400 }) {
  const svgRef = useRef();

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove(); // Clear previous

    const margin = { top: 20, right: 20, bottom: 30, left: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Scales
    const xScale = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.x)])
      .range([0, innerWidth]);

    const yScale = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.y)])
      .range([innerHeight, 0]);

    // Axes
    g.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(xScale));

    g.append('g')
      .call(d3.axisLeft(yScale));

    // Points
    g.selectAll('circle')
      .data(data)
      .join('circle')
        .attr('cx', d => xScale(d.x))
        .attr('cy', d => yScale(d.y))
        .attr('r', 5)
        .attr('fill', '#3B82F6')
        .attr('opacity', 0.7);
  }, [data, width, height]);

  return <svg ref={svgRef} width={width} height={height}></svg>;
}
```

---

**For Scientific/Interactive: Plotly**
- 3D visualizations
- Statistical charts
- Interactive out-of-box

**Installation:**
```bash
npm install react-plotly.js plotly.js
```

**Detailed JavaScript/TypeScript Examples:**
See `references/javascript/` for:
- `recharts-examples.md` - All Recharts chart types
- `d3-patterns.md` - D3.js integration patterns
- `plotly-examples.md` - Plotly chart types
- `accessibility-react.md` - WCAG implementation in React

---

### Python (Future - Add as Needed)

**Common Libraries:**
- **Plotly** - Interactive charts (same API as JavaScript Plotly)
- **Matplotlib** - Publication-quality static plots
- **Seaborn** - Statistical visualizations
- **Altair** - Declarative visualization grammar
- **Bokeh** - Interactive web visualizations

**When building Python implementations:**
1. Follow universal patterns above (same selection criteria)
2. Use RESEARCH_GUIDE.md to research Python libraries
3. Add to `references/python/` directory
4. Create examples in `examples/python/`

**Research Starting Points:**
```
Query: "Python data visualization library 2025 Plotly Matplotlib comparison"
Context7: /plotly/plotly.py, /matplotlib/matplotlib
```

---

### Rust (Future - Add as Needed)

**Common Libraries:**
- **plotters** - Pure Rust plotting library
- **egui_plot** - Immediate mode plotting for egui
- **Leptos charts** - Reactive web charts

**When building Rust implementations:**
1. Apply universal patterns (purpose-first selection)
2. Research Rust visualization crates
3. Add to `references/rust/`

---

### Go (Future - Add as Needed)

**Common Libraries:**
- **gonum/plot** - Plotting library for Go
- **go-echarts** - ECharts binding for Go

**When building Go implementations:**
1. Apply universal patterns
2. Research Go visualization packages
3. Add to `references/go/`

---

## Common Workflows

### Workflow 1: Business Dashboard

**Scenario:** Displaying monthly sales, expenses, and profit trends

**Steps:**
1. Assess: Time series data (temporal), 3 metrics, 12 months
2. Purpose: Show trends and compare metrics
3. Select: Line Chart (multiple series)
4. Implement: Use Recharts (JavaScript) or Plotly (Python)
5. Accessibility: Add aria-label, provide data table toggle
6. Style: Apply design tokens for theming

**Reference:** `references/examples/business-dashboard.md`

---

### Workflow 2: Scientific Publication

**Scenario:** Comparing distributions across experimental groups

**Steps:**
1. Assess: Continuous data, 4-6 groups, ~100 samples per group
2. Purpose: Reveal distribution shapes and compare
3. Select: Violin Plot or Box Plot
4. Implement: Plotly (Python/JavaScript) or D3.js
5. Accessibility: Provide statistical summary table
6. Export: High-resolution PNG/SVG for publication

**Reference:** `references/examples/scientific-visualization.md`

---

### Workflow 3: Executive Presentation

**Scenario:** Before/after comparison for C-suite

**Steps:**
1. Assess: Two time points, 8-10 entities, emphasize change
2. Purpose: Show ranking shifts and magnitude of change
3. Select: Slope Graph (simple, clear)
4. Implement: D3.js for custom styling or Recharts
5. Accessibility: High contrast, large text, clear labels
6. Annotate: Add context for changes

**Reference:** `references/examples/executive-presentation.md`

---

## Decision Trees

### Quick Chart Selection

```
START: What is your data?

Categorical data (categories/groups)
  ├─ Compare values → Bar Chart
  ├─ Show composition → Treemap (hierarchical) or Pie Chart (<6 slices)
  └─ Show flow between categories → Sankey Diagram

Continuous data (numbers)
  ├─ Single variable
  │   ├─ Show distribution → Histogram, Violin Plot
  │   └─ Track over time → Line Chart, Area Chart
  │
  └─ Two variables
      ├─ Explore relationship → Scatter Plot
      ├─ Many points (>1000) → Hexbin Plot
      └─ Show change over time → Connected Scatter Plot

Temporal data (time series)
  ├─ Single metric → Line Chart, Area Chart
  ├─ Multiple metrics → Small Multiples or Stacked Area
  ├─ Daily patterns → Calendar Heatmap
  └─ Events on timeline → Timeline, Gantt Chart

Hierarchical data (nested structures)
  ├─ Focus on proportions → Treemap
  ├─ Show depth → Sunburst, Dendrogram
  └─ Interactive drill-down → Collapsible Tree

Geographic data (locations)
  ├─ Regional aggregates → Choropleth Map
  ├─ Point locations → Symbol Map
  └─ Movement/flow → Flow Map

Network data (connections)
  ├─ <200 nodes → Force-Directed Graph
  ├─ Flow between entities → Chord Diagram, Sankey
  └─ Large network → Adjacency Matrix, filtered view
```

**Complete decision trees:** `references/selection-matrix.md`

---

## Accessibility Checklist

Before finalizing any visualization:

**Visual Design:**
- [ ] Color contrast meets 3:1 for UI elements, 4.5:1 for text
- [ ] Colorblind-safe palette used (no red/green reliance)
- [ ] Patterns/textures available, not just color
- [ ] Clear, legible labels with units
- [ ] Sufficient spacing between elements

**Semantic HTML:**
- [ ] `<figure role="img">` for charts
- [ ] `aria-label` or `aria-describedby` for description
- [ ] `<figcaption>` for title
- [ ] Data table alternative provided

**Interaction:**
- [ ] Keyboard navigation works (Tab, Enter, arrows)
- [ ] Tooltips accessible via keyboard
- [ ] Focus indicators visible
- [ ] No keyboard traps

**Screen Readers:**
- [ ] Chart updates announced (aria-live regions)
- [ ] Alternative text describes trend/insight
- [ ] Data table has proper headers (<th scope>)

**Full checklist:** `references/accessibility.md`

---

## Common Mistakes to Avoid

1. **Chart-first thinking** - Choose based on data + purpose, not aesthetics
2. **Pie charts for >6 categories** - Use sorted bar chart instead
3. **Dual-axis charts** - Usually misleading, use small multiples
4. **3D when 2D sufficient** - Adds complexity, reduces clarity
5. **Rainbow color scales** - Not perceptually uniform, not colorblind-safe
6. **Truncated y-axis** - Indicate clearly or start at zero
7. **Too many colors** - Limit to 6-8 distinct categories
8. **Missing context** - Always label axes, include units, cite data source

---

## Integration with Design Tokens

Reference the **design-tokens** skill for theming and styling.

**Chart-specific tokens:**
```css
--chart-color-primary        /* Primary data series */
--chart-color-1 through --chart-color-10  /* Categorical palette */
--chart-axis-color           /* Axis lines */
--chart-grid-color           /* Grid lines */
--chart-tooltip-bg           /* Tooltip background */
--chart-font-family          /* Chart text font */
```

**Apply tokens:**
```tsx
// With Recharts
<Line stroke="var(--chart-color-primary)" />

// With D3
.attr('fill', 'var(--chart-color-1)')
```

**Theme switching:**
Light/dark/high-contrast themes work automatically via design tokens.

**Details:** See `../design-tokens/` skill and `references/theming.md`

---

## References

**Chart Catalog:**
- `references/chart-catalog.md` - All 24+ visualization types with detailed guidance

**Selection Guides:**
- `references/selection-matrix.md` - Complete decision trees and matrices
- `references/data-type-mapping.md` - Data type → recommended charts

**Technical Guides:**
- `references/accessibility.md` - WCAG 2.1 AA compliance patterns
- `references/color-systems.md` - Colorblind-safe palettes, sequential/diverging scales
- `references/performance.md` - Optimization by data volume
- `references/interaction-patterns.md` - Hover, click, zoom, brush, filter

**Language-Specific:**
- `references/javascript/` - React, D3.js, Plotly examples and patterns
- `references/python/` - (Future) Plotly, Matplotlib, Seaborn examples
- `references/rust/` - (Future) plotters crate examples
- `references/go/` - (Future) gonum/plot examples

**Assets:**
- `assets/color-palettes/` - Accessible color schemes (JSON)
- `assets/example-datasets/` - Sample data for testing
- `assets/templates/` - Boilerplate chart code

---

## Examples

**Working code examples:**
- `examples/javascript/bar-chart.tsx` - Basic and grouped bar charts
- `examples/javascript/line-chart.tsx` - Single and multi-series line charts
- `examples/javascript/scatter-plot.tsx` - Basic scatter with trend line
- `examples/javascript/treemap.tsx` - Hierarchical data visualization
- `examples/javascript/accessible-chart.tsx` - WCAG-compliant chart with data table

**Run examples:**
```bash
cd examples/javascript
npm install
npm start
```

---

## Validation & Best Practices

**Before deploying visualizations:**

**Validate Accessibility:**
```bash
# Run accessibility validator (if available)
scripts/validate_accessibility.py <chart-html>
```

**Test Colorblind:**
- Use browser DevTools color vision deficiency emulator
- Or tools: Sim Daltonism, Color Oracle

**Performance Check:**
- Test with maximum expected data volume
- Monitor frame rate (should be 60fps)
- Check memory usage (should not grow unbounded)

**Complete validation:** `references/validation-checklist.md`

---

## Advanced Topics

**For advanced use cases, see:**
- `references/advanced/animations.md` - Transitions, morphing, object constancy
- `references/advanced/custom-d3.md` - Building novel chart types with D3
- `references/advanced/webgl.md` - High-performance rendering for >10K points
- `references/advanced/streaming-data.md` - Real-time updating charts

---

**This skill uses progressive disclosure:** SKILL.md provides overview and quick start. Detailed documentation, code examples, and language-specific implementations in `references/` and `examples/` directories. Load additional resources as needed.
