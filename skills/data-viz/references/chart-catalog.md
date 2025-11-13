# Complete Chart Type Catalog

Detailed reference for all 24+ visualization types with implementation guidance.

## Comparison Charts

### Bar Chart
**Purpose:** Compare values across categories
**Best for:** 2-20 categories, straightforward comparisons
**Data:** Categorical (x-axis) + Continuous (y-axis)
**Variants:** Horizontal, vertical, grouped, stacked

**When to use:**
- Comparing sales across products
- Showing survey results
- Ranking items by value

**Implementation notes:**
- Sort by value for easier reading (unless natural order matters)
- Use horizontal bars for long category names
- Limit to 20 categories (use filtering for more)

**Accessibility:**
- Direct labels on bars
- Color + pattern for grouped bars
- Provide data table

---

### Lollipop Chart
**Purpose:** Space-efficient comparison
**Best for:** 10-30 categories, emphasize differences
**Data:** Same as bar chart

**When to use:**
- Many categories to compare
- Emphasize endpoint values
- Cleaner visual than many bars

**Implementation:**
- Circle at data point
- Thin line from baseline
- Sort by value

---

### Slope Graph
**Purpose:** Before/after comparison
**Best for:** 5-15 entities, two time points
**Data:** Entities with two measurements

**When to use:**
- Showing ranking changes
- Before/after interventions
- Emphasizing direction and magnitude of change

---

## Trend Charts

### Line Chart
**Purpose:** Show change over time
**Best for:** Continuous time series, 1-4 series
**Data:** Temporal (x-axis) + Continuous (y-axis)

**When to use:**
- Stock prices
- Website traffic
- Temperature trends

**Implementation:**
- Use monotone or smooth interpolation
- Add markers for data points
- Multiple series: limit to 4 for readability

---

### Area Chart
**Purpose:** Emphasize magnitude over time
**Best for:** Showing volume/quantity trends
**Variants:** Simple, stacked, normalized (100%)

**When to use:**
- Emphasize scale (filled area draws attention)
- Show composition over time (stacked)
- Display proportions (normalized to 100%)

---

### Stream Graph
**Purpose:** Flowing composition over time
**Best for:** 4-10 categories, aesthetic emphasis
**Implementation:** Center-weighted baseline, organic curves

---

### Sparkline
**Purpose:** Inline, compact trend
**Best for:** Dashboard KPIs, tables, small spaces
**Implementation:** Minimal axes, no labels, ~50px height

---

## Distribution Charts

### Histogram
**Purpose:** Frequency distribution
**Best for:** Continuous data, show distribution shape
**Implementation:**
- Choose bin size carefully (Sturges', Scott's, or Freedman-Diaconis rule)
- 5-20 bins typical
- Equal-width bins

---

### Box Plot
**Purpose:** Summary statistics with outliers
**Best for:** Comparing distributions across groups
**Shows:** Min, Q1, median, Q3, max, outliers

---

### Violin Plot
**Purpose:** Full distribution shape + summary stats
**Best for:** Comparing distributions, revealing bimodality
**Implementation:** Kernel density + box plot overlay

---

### Ridgeline Plot
**Purpose:** Compare many distributions
**Best for:** 6-30 groups, show distribution evolution
**Implementation:** Stack vertically, overlap 20-40%

---

## Relationship Charts

### Scatter Plot
**Purpose:** Two-variable relationship
**Best for:** Exploring correlation, identifying outliers
**Implementation:**
- Point size/color can encode third variable (bubble chart)
- Add trend line if correlation exists
- Limit to ~1000 points (use hexbin for more)

---

### Hexbin Plot
**Purpose:** Dense scatter plots
**Best for:** >1000 points, show density
**Implementation:** Hexagonal binning, color by count

---

### Connected Scatter
**Purpose:** Two-variable relationship over time
**Best for:** Showing trajectory, cycles
**Implementation:** Connect points in temporal order

---

## Composition Charts

### Pie Chart
**Purpose:** Part-to-whole
**Best for:** 2-6 categories MAXIMUM
**Caution:** Use sparingly, bar chart often better

**When acceptable:**
- Simple composition (2-6 parts)
- Percentages are round numbers
- Audience is non-technical

**When to avoid:**
- >6 categories
- Comparing multiple pie charts
- Precise comparison needed

---

### Treemap
**Purpose:** Hierarchical part-to-whole
**Best for:** Nested data, many items
**Implementation:** Squarified algorithm for better aspect ratios

---

### Sunburst
**Purpose:** Radial hierarchy
**Best for:** Aesthetic hierarchical display
**Implementation:** Center = root, outer rings = leaves

---

### Waterfall Chart
**Purpose:** Sequential cumulative changes
**Best for:** Profit bridges, variance analysis
**Implementation:** Floating bars, color-code positive/negative

---

## Flow Charts

### Sankey Diagram
**Purpose:** Flow with proportional width
**Best for:** Energy flow, budget allocation, customer journeys
**Implementation:** D3-sankey, width = flow quantity

---

### Chord Diagram
**Purpose:** Circular flow/relationships
**Best for:** Migration, trade, co-occurrence
**Implementation:** Circular layout, ribbon width = strength

---

## Network Charts

### Force-Directed Graph
**Purpose:** Network structure
**Best for:** <200 nodes, community detection
**Implementation:** Physics simulation, D3-force

**Caution:** Becomes "hairball" with >100 nodes

---

## Temporal Charts

### Gantt Chart
**Purpose:** Task scheduling
**Best for:** Project timelines, resource allocation
**Implementation:** Horizontal bars, dependencies as arrows

---

### Calendar Heatmap
**Purpose:** Daily patterns
**Best for:** GitHub-style activity, habit tracking
**Implementation:** 7-column grid (days of week)

---

## Multivariate Charts

### Parallel Coordinates
**Purpose:** 5-15 dimensions
**Best for:** High-dimensional data exploration
**Implementation:** Vertical axes, polylines for each data point

---

### Radar Chart
**Purpose:** Multivariate profile
**Use cautiously:** Area distortion misleading
**Better alternative:** Bar chart often clearer

---

*For working code examples, see `javascript/recharts-examples.md` and `javascript/d3-patterns.md`*
