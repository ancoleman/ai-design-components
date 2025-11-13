# Visualization Selection Matrix

Complete decision trees and quick reference tables for choosing the right visualization type.

## By Data Story (Quick Reference)

| Data Story | Primary Choice | Alternative | When to Use Alternative |
|------------|---------------|-------------|------------------------|
| **Compare categories** | Bar Chart | Lollipop Chart | Emphasize differences, save space |
| **Show trend over time** | Line Chart | Area Chart | Emphasize magnitude/volume |
| **Part-to-whole** | Stacked Bar | Treemap | Hierarchical data |
| **Distribution shape** | Histogram | Violin Plot | Show full distribution, not just bins |
| **Correlation** | Scatter Plot | Hexbin Plot | >1000 points (reduce overplotting) |
| **Flow/transformation** | Sankey Diagram | Chord Diagram | Circular relationships |
| **Ranking changes** | Slope Graph | Bump Chart | More than 2 time points |
| **Dense time series** | Calendar Heatmap | Small Multiples | Daily patterns vs. multiple series |
| **Network structure** | Force-Directed | Adjacency Matrix | <200 nodes vs. large networks |
| **Hierarchy** | Treemap | Sunburst | Space efficiency vs. radial aesthetic |

---

## By Data Type

| Data Type | Characteristics | Recommended Charts |
|-----------|----------------|-------------------|
| **Categorical (Nominal)** | Unordered categories | Bar chart, lollipop, treemap |
| **Categorical (Ordinal)** | Ordered categories | Bar chart (sorted), bullet chart |
| **Continuous (Single)** | One numeric variable | Histogram, density plot, box plot |
| **Continuous (Two)** | Two numeric variables | Scatter plot, hexbin, bubble chart |
| **Time Series (Single)** | One metric over time | Line chart, area chart, sparkline |
| **Time Series (Multiple)** | Multiple metrics over time | Small multiples, stacked area |
| **Temporal Events** | Discrete events in time | Timeline, Gantt chart |
| **Hierarchical** | Nested structure | Treemap, sunburst, dendrogram |
| **Network/Graph** | Connected entities | Force-directed, chord, sankey |
| **Geographic** | Location-based | Choropleth, symbol map, flow map |
| **Multivariate (3-15 dims)** | Many variables | Parallel coordinates, radar, SPLOM |

---

## Decision Tree: Compare Values

```
COMPARE VALUES ACROSS CATEGORIES

How many categories?
├─ 2-10 categories
│   ├─ Emphasize differences?
│   │   ├─ Yes → Lollipop Chart
│   │   └─ No → Bar Chart
│   │
│   ├─ Multiple series?
│   │   ├─ Stacked (composition) → Stacked Bar
│   │   └─ Side-by-side (comparison) → Grouped Bar
│   │
│   └─ Two time points?
│       └─ Slope Graph (emphasizes change)
│
├─ 11-20 categories
│   ├─ Can sort by value → Sorted Bar Chart
│   └─ Hierarchical → Treemap
│
└─ >20 categories
    ├─ Hierarchical structure → Treemap or Sunburst
    ├─ Can filter/search → Interactive bar with filter
    └─ Show top N → Top 10 bar + "Others" category
```

---

## Decision Tree: Show Trends

```
SHOW CHANGE OVER TIME

How many series?
├─ 1 series
│   ├─ Emphasize magnitude → Area Chart
│   ├─ Simple line → Line Chart
│   └─ Inline/compact → Sparkline
│
├─ 2-4 series
│   ├─ Different scales → Small Multiples
│   ├─ Same scale → Multi-line Chart
│   └─ Composition over time → Stacked Area
│
├─ 5-10 series
│   ├─ Compare patterns → Small Multiples (grid)
│   ├─ Show composition → Stacked Area (normalized to 100%)
│   └─ Flowing aesthetic → Stream Graph
│
└─ >10 series
    ├─ Interactive filter (select series to show)
    └─ Heatmap (series as rows, time as columns)

Just two time points?
└─ Slope Graph (before/after)

Daily patterns?
└─ Calendar Heatmap (days in grid)
```

---

## Decision Tree: Reveal Distribution

```
REVEAL DISTRIBUTION

Single variable?
├─ Show bins/frequency → Histogram
├─ Show summary stats → Box Plot
├─ Show full shape → Violin Plot
└─ Smooth curve → Density Plot

Compare distributions?
├─ 2-4 groups
│   ├─ Overlaid → Overlaid Density Plots
│   └─ Side-by-side → Box Plots or Violin Plots
│
├─ 5-10 groups
│   └─ Violin Plots (side-by-side)
│
└─ >10 groups
    └─ Ridgeline Plot (stacked density curves)

Show outliers?
├─ With summary stats → Box Plot
└─ All points visible → Beeswarm Plot
```

---

## By Audience Type

| Audience | Chart Complexity | Recommendations | Avoid |
|----------|-----------------|-----------------|-------|
| **Executive/C-Suite** | Simple, clear | Bar, line, slope graphs. Heavy annotation. One insight per chart. | Complex charts, jargon, small text |
| **General Public** | Familiar types | Bar, line, pie (<6 slices). Clear labels. Strong narrative. | Novel chart types, technical terms |
| **Data Analysts** | Moderate-Complex | Any chart type. Interactive. Access to raw data. | Oversimplification |
| **Scientists** | Complex, rigorous | Violin, box, scatter with CI. Methodological transparency. | Decorative elements |
| **Domain Experts** | Specialized OK | Candlestick (finance), Gantt (PM). Assume domain knowledge. | Explaining basics |

---

## Performance Decision Matrix

| Data Points | Rendering Method | Library Choice | Notes |
|-------------|-----------------|----------------|-------|
| <100 | SVG (standard) | Recharts, Plotly | Fast, crisp, scalable |
| 100-1,000 | SVG optimized | Recharts, D3.js | Good performance |
| 1K-10K | SVG or Canvas | D3.js (Canvas) | Canvas for better perf |
| 10K-100K | Canvas | D3.js (Canvas), Plotly WebGL | Required for smooth interaction |
| >100K | Server aggregation | Backend → Simple viz | Aggregate before sending to client |

**Canvas vs SVG:**
- **SVG**: Crisp, scalable, accessible, but slow with many elements
- **Canvas**: Fast, handles 10K+ points, but less accessible (rasterized)

---

## Chart Type Index (Alphabetical)

Quick lookup for specific chart types:

- **Area Chart** - Trend (magnitude emphasis)
- **Bar Chart** - Comparison (categorical)
- **Box Plot** - Distribution (summary stats)
- **Bubble Chart** - Relationship (3 variables)
- **Bullet Chart** - Comparison (performance indicators)
- **Calendar Heatmap** - Temporal (daily patterns)
- **Candlestick Chart** - Temporal (OHLC financial data)
- **Chord Diagram** - Flow (circular relationships)
- **Choropleth Map** - Geographic (regional aggregates)
- **Connected Scatter** - Relationship (over time)
- **Dendrogram** - Hierarchy (tree structure)
- **Donut Chart** - Composition (part-to-whole)
- **Force-Directed Graph** - Network (node relationships)
- **Gantt Chart** - Temporal (task scheduling)
- **Hexbin Plot** - Relationship (dense scatter)
- **Histogram** - Distribution (frequency bins)
- **Line Chart** - Trend (continuous change)
- **Lollipop Chart** - Comparison (space-efficient)
- **Parallel Coordinates** - Multi-dimensional (5-15 variables)
- **Pie Chart** - Composition (max 5-6 slices)
- **Radar Chart** - Multi-dimensional (use cautiously)
- **Ridgeline Plot** - Distribution (multiple groups)
- **Sankey Diagram** - Flow (proportional bandwidth)
- **Scatter Plot** - Relationship (two variables)
- **Slope Graph** - Comparison (before/after)
- **Small Multiples** - Any type (faceted comparison)
- **Sparkline** - Trend (inline, compact)
- **Stacked Area** - Trend (composition over time)
- **Stacked Bar** - Composition (cumulative categories)
- **Stream Graph** - Trend (flowing composition)
- **Sunburst** - Hierarchy (radial)
- **Symbol Map** - Geographic (point locations)
- **Treemap** - Hierarchy (nested rectangles)
- **Violin Plot** - Distribution (full shape)
- **Waterfall Chart** - Composition (sequential changes)

**Detailed guidance for each:** See `references/chart-catalog.md`

---

*Use this matrix to quickly identify appropriate visualizations. For detailed implementation guidance, accessibility patterns, and code examples, reference the language-specific directories.*
