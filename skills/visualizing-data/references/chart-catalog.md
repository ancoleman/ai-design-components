# Complete Chart Type Catalog

Detailed reference for all 24+ visualization types with implementation guidance, use cases, and design patterns.

## Table of Contents

1. [Comparison Charts](#comparison-charts)
2. [Trend Charts](#trend-charts)
3. [Distribution Charts](#distribution-charts)
4. [Relationship Charts](#relationship-charts)
5. [Composition Charts](#composition-charts)
6. [Flow Charts](#flow-charts)
7. [Network Charts](#network-charts)
8. [Temporal Charts](#temporal-charts)
9. [Multivariate Charts](#multivariate-charts)
10. [Advanced Techniques](#advanced-techniques)

---

## Comparison Charts

### Bar Chart

**Purpose:** Compare values across categories

**When to Use:**
- Comparing sales across products
- Showing survey results
- Ranking items by value
- 2-20 categories, straightforward comparisons

**Why It's Powerful:**
- Universally understood
- Precise value comparison through length
- Easy to scan and rank
- Works for most audiences

**Implementation Guidance:**
- Sort by value for easier reading (unless natural order matters)
- Use horizontal bars for long category names
- Limit to 20 categories (use filtering for more)
- Start y-axis at zero

**Variants:**
- Horizontal: Better for many categories or long labels
- Grouped: Compare multiple series side-by-side
- Stacked: Show composition within categories

**Accessibility:**
- Direct labels on bars
- Color + pattern for grouped bars
- Provide data table alternative

---

### Lollipop Chart

**Purpose:** Space-efficient alternative to bar charts

**When to Use:**
- Many categories to compare (10-30)
- Emphasize endpoint values
- Cleaner visual than dense bars
- Modern, minimal aesthetic desired

**Why It's Powerful:**
- Less visual clutter than bars
- Draws attention to data point
- Better ink-to-data ratio
- Effective for ranking displays

**Implementation:**
- Circle at data point end
- Thin line from baseline to circle
- Sort by value for readability
- Circle size should be consistent

---

### Slope Graph

**Purpose:** Before/after comparison showing change

**When to Use:**
- Showing ranking changes between two periods
- Before/after interventions
- Emphasizing rate and direction of change
- 5-15 entities, two time points

**Why It's Powerful:**
- Instantly shows direction of change
- Reveals ranking shifts
- Emphasizes magnitude of change
- Simple yet information-rich

**Implementation Guidance:**
- Two vertical axes (start and end)
- Lines connect same entity across time
- Color-code by direction (up/down)
- Label both endpoints

**Design Pattern:**
```
Before  After
  10 ──────→ 15  Entity A (↑)
  20 ──────→ 18  Entity B (↓)
  15 ──────→ 22  Entity C (↑)
```

---

## Trend Charts

### Line Chart

**Purpose:** Show change over continuous time

**When to Use:**
- Stock prices, sales trends
- Website traffic patterns
- Temperature/weather data
- 1-4 series maximum for clarity

**Why It's Powerful:**
- Natural representation of time flow
- Easy to spot trends and patterns
- Reveals seasonality and cycles
- Handles many data points well

**Implementation:**
- Use monotone or smooth interpolation
- Add markers for actual data points
- Multiple series: limit to 4
- Include legend for multi-series

**Variants:**
- Step chart: Discrete value changes
- Multi-line: Compare several trends
- With confidence bands: Show uncertainty

---

### Area Chart

**Purpose:** Emphasize magnitude and volume over time

**When to Use:**
- Showing total volume/quantity
- Emphasizing scale of values
- Cumulative totals
- When filled area reinforces the message

**Variants:**
- Simple: Single series with fill
- Stacked: Multiple series showing composition
- Normalized (100%): Proportional composition

**When to use stacked:**
- Parts that sum to a meaningful total
- Showing composition changes over time
- Comparing category proportions

---

### Stream Graph (ThemeRiver)

**Purpose:** Flowing composition over time with aesthetic emphasis

**When to Use:**
- Showing proportional change with visual appeal
- Displaying evolving composition (4-10 categories)
- Cultural/music evolution over decades
- Technology adoption patterns
- Presentations where engagement matters

**Why It's Powerful:**
- Beautiful, engaging visual form
- Natural "flow" metaphor resonates
- Emphasizes continuity and organic change
- Center baseline reduces perceptual distortion
- Memorable for presentations

**Implementation Guidance:**
- Use center-weighted or symmetric baseline
- Organic, flowing shapes (not sharp edges)
- Related categories placed near each other
- Add interactive hover to isolate streams
- Consider transparency for overlapping

**Visual Form:**
```
         ╱════════════════╲
        ╱  Category A      ╲
       ╱────────────────────╲     ← Flowing
      ╱   Category B         ╲       organic
     │─────────────────────────│     shapes
      ╲   Category C         ╱
       ╲────────────────────╱
        ╲  Category D      ╱
         ╲════════════════╱
```

**Cautions:**
- Difficult to read exact values
- Baseline ambiguity can confuse some users
- Not suitable when precise comparison needed

---

### Sparkline

**Purpose:** Compact inline trend visualization

**When to Use:**
- Dashboard KPIs
- Tables with trend context
- Small multiples in constrained space
- Quick trend overview without detail

**Implementation:**
- Minimal: no axes, no labels
- Typical height: 30-50px
- Can include min/max markers
- Often grayscale or single color

---

## Distribution Charts

### Histogram

**Purpose:** Show frequency distribution of continuous data

**When to Use:**
- Understanding data spread
- Identifying skewness, bimodality
- Detecting outliers
- Statistical analysis

**Implementation:**
- Choose bin size using rules:
  - Sturges: k = 1 + log2(n)
  - Scott: h = 3.49σn^(-1/3)
  - Freedman-Diaconis: h = 2*IQR*n^(-1/3)
- Typical: 5-20 bins
- Equal-width bins for comparability

---

### Box Plot

**Purpose:** Summary statistics with outlier detection

**When to Use:**
- Comparing distributions across groups
- Quick statistical summary
- Identifying outliers
- Technical/statistical audiences

**Shows:** Minimum, Q1, median, Q3, maximum, outliers

**Anatomy:**
```
    ╭─────╮        ← Upper adjacent value
    │     │
    │─────│        ← Upper quartile (Q3)
    │  │  │        ← Median
    │─────│        ← Lower quartile (Q1)
    │     │
    ╰─────╯        ← Lower adjacent value
      ●            ← Outliers beyond 1.5×IQR
```

---

### Violin Plot

**Purpose:** Full distribution shape with summary statistics

**When to Use:**
- Comparing distributions across categories
- When distribution shape matters as much as summary
- Revealing bimodal or multimodal distributions
- Scientific/technical data with complex distributions

**Why It's Powerful:**
- Shows full distribution, not just summary
- Reveals bimodality that box plots hide
- Combines statistical rigor with visual richness
- More informative than box plots alone

**Implementation Guidance:**
- Mirror density estimation around vertical axis
- Include box plot elements (median line, quartiles)
- Optionally add individual data points
- Width represents density at that value

**Example Use Cases:**
- Salary distributions showing bimodal patterns
- Gene expression across experimental conditions
- Response times in treatment groups
- Product ratings showing polarization

**Cautions:**
- Requires more space than box plots
- Can be unfamiliar to non-technical audiences
- Less effective with <20 data points

---

### Ridgeline Plot (Joy Plot)

**Purpose:** Compare many distributions efficiently

**When to Use:**
- Comparing distributions across many categories (6-30+)
- Showing distribution evolution over time
- Temperature patterns by month
- Any data where distribution shape matters

**Why It's Powerful:**
- Shows both shape and between-group comparison
- Aesthetically appealing and space-efficient
- Easier to read than overlapping curves
- Reveals patterns like bimodality, shifts

**Implementation:**
- Stack from top to bottom
- Overlap by 20-40% for visibility
- Consistent horizontal scale
- Add subtle transparency
- Clear labels on the left

---

## Relationship Charts

### Scatter Plot

**Purpose:** Explore two-variable relationships

**When to Use:**
- Exploring correlation
- Identifying outliers and clusters
- Finding patterns in two dimensions
- <1000 points (use hexbin for more)

**Implementation:**
- Point size/color can encode third variable (bubble chart)
- Add trend line if correlation exists
- Consider jittering for overlapping points

---

### Bubble Chart

**Purpose:** Three-variable scatter plot

**When to Use:**
- Relationship + magnitude
- Comparing entities across 3 dimensions
- Making impactful presentations

**Implementation:**
- Size encodes third variable
- Use AREA not radius for sizing
- Limit to 20-50 bubbles
- Consider overlap handling

---

### Hexbin Plot

**Purpose:** Handle dense scatter plots with binning

**When to Use:**
- Scatter plots with thousands of overlapping points
- Geographic density visualization
- When individual points are less important than density
- Large datasets (10,000+ points)

**Why It's Powerful:**
- Handles overplotting better than scatter
- Hexagons tile more naturally than squares
- Shows density patterns at multiple scales
- Reduces visual noise

**Implementation:**
- Choose bin size based on data density
- Color gradient shows density
- Optionally add contour lines
- Provide zoom interaction

---

### Connected Scatter Plot

**Purpose:** Two-variable relationship evolving over time

**When to Use:**
- Showing relationship AND temporal evolution
- Economic analysis (e.g., Phillips curve)
- Before/after with intermediate states
- Cyclical relationship analysis

**Why It's Powerful:**
- Shows relationship AND time simultaneously
- Reveals loops, spirals, reversals
- Path density shows acceleration/deceleration
- Memorable visual form

**Implementation:**
- Add directional arrows or gradients
- Label key points (start, end, inflections)
- Color gradient for temporal encoding
- Annotate major events

---

## Composition Charts

### Pie Chart

**Purpose:** Simple part-to-whole for few categories

**Use ONLY When:**
- 2-6 categories MAXIMUM
- Simple, round percentages
- Non-technical audience
- Single point comparison (not multiple pies)

**Avoid When:**
- >6 categories
- Comparing multiple compositions
- Precise comparison needed
- Similar-sized slices

**Better Alternative:** Horizontal bar chart sorted by value

---

### Treemap

**Purpose:** Hierarchical part-to-whole with nesting

**When to Use:**
- Hierarchical data with size comparison
- Portfolio allocation (sectors → stocks)
- File system disk usage
- Budget breakdown by categories
- Market share with sub-segments

**Why It's Powerful:**
- Space-efficient visualization
- Shows proportions and hierarchy together
- Can display thousands of items
- Immediate visual size comparison
- Effective use of screen space

**Implementation:**
- Use squarified algorithm for better aspect ratios
- Color-code by category or performance
- Add borders to distinguish levels
- Implement zoom/drill-down for deep hierarchies
- Label only significant rectangles

---

### Sunburst Diagram

**Purpose:** Radial hierarchical visualization

**When to Use:**
- Hierarchical data with aesthetic emphasis
- Drill-down navigation through levels
- When circular/radial metaphor fits
- Alternative to treemap

**Implementation:**
- Center is root, outer rings are leaves
- Color by category or value
- Click-to-zoom for interactivity
- Add breadcrumb trail
- Limit to 4-6 levels

---

### Waterfall Chart

**Purpose:** Sequential cumulative changes

**When to Use:**
- Profit bridges (revenue → costs → profit)
- Variance analysis
- Step-by-step value breakdown
- Financial reporting

**Implementation:**
- Floating bars showing incremental changes
- Color-code positive (green) and negative (red)
- Show running total at each step
- Final bar shows total

---

## Flow Charts

### Sankey Diagram

**Purpose:** Flow visualization with proportional width

**When to Use:**
- Resource flow and transformation
- Budget allocation through departments
- Energy flow from sources to uses
- Customer journey through website
- Supply chain visualization

**Why It's Powerful:**
- Instantly reveals major flows and losses
- Shows redistribution and transformation
- Width encoding is highly intuitive
- Reveals inefficiencies and bottlenecks

**Implementation:**
- Use D3-sankey library
- Nodes = states, Links = flows
- Link width proportional to quantity
- Color-code by category or source
- Add hover for exact values

**Structure:**
```
Source A ━━━━━━━━━━━━━━━┓
                       ┃━━━━━→ Destination 1
Source B ━━━━━━┓      ┃
               ┃━━━━━━┛
               ┃━━━━━━━━━━━━━→ Destination 2
Source C ━━━━━━┛
```

**Cautions:**
- Can become cluttered with many nodes
- Crossing flows reduce readability
- Requires careful node ordering

---

### Chord Diagram

**Purpose:** Circular flow showing inter-relationships

**When to Use:**
- Inter-relationships in a network
- Migration patterns between regions
- Trade relationships between countries
- Character co-occurrence

**Why It's Powerful:**
- Compact representation of full relationship matrix
- Visually striking and memorable
- Shows bidirectional flows
- Space-efficient for many-to-many relationships

**Implementation:**
- Use D3-chord library
- Order entities logically around circle
- Color-code by category or cluster
- Ribbon opacity for direction/confidence
- Hover highlighting to follow connections

---

## Network Charts

### Force-Directed Graph

**Purpose:** Network structure and communities

**When to Use:**
- Social networks
- Organizational structures
- Citation networks
- <200 nodes (becomes "hairball" beyond)

**Implementation:**
- Physics simulation (D3-force)
- Node size by importance/degree
- Edge thickness by weight
- Color by community/cluster

**Cautions:**
- Performance degrades >100 nodes
- Layout is non-deterministic
- Can be hard to interpret
- Consider alternatives for large networks

---

## Temporal Charts

### Gantt Chart

**Purpose:** Task scheduling and project timelines

**When to Use:**
- Project management
- Resource allocation
- Manufacturing schedules
- Sprint planning

**Implementation:**
- Horizontal bars showing duration
- Dependencies as arrows
- Color by status or assignee
- Include milestones as diamonds

---

### Calendar Heatmap

**Purpose:** Daily patterns over long periods

**When to Use:**
- Daily activity tracking (GitHub-style)
- Showing seasonality and weekly cycles
- Habit tracking and streaks
- Event frequency patterns

**Why It's Powerful:**
- Natural calendar metaphor
- Reveals weekly/monthly patterns
- Shows micro (daily) and macro (seasonal)
- Engaging for personal metrics

**Layout:**
```
       M  T  W  T  F  S  S
Jan   ██ ▓▓ ░░ ▓▓ ██ ░░ ░░
      ▓▓ ██ ░░ ▓▓ ▓▓ ██ ░░
Feb   ░░ ▓▓ ██ ░░ ▓▓ ░░ ██

Legend: ░░ Low  ▓▓ Medium  ██ High
```

---

## Multivariate Charts

### Parallel Coordinates

**Purpose:** Explore high-dimensional data (5-15 dimensions)

**When to Use:**
- Finding patterns across multiple dimensions
- Filtering and brushing multivariate data
- Comparing profiles of entities
- Identifying clusters and outliers

**Why It's Powerful:**
- Shows high-dimensional relationships in 2D
- Interactive brushing reveals patterns
- Can display hundreds of observations
- Reveals correlations and anti-correlations

**Implementation:**
- Normalize axes to comparable ranges
- Use brushing to filter/highlight
- Allow axis reordering
- Add transparency for overplotting

**Structure:**
```
Var1  Var2  Var3  Var4  Var5
 │     │     │     │     │
 ├─────┼─────┼─────┼─────┤   ← Data point 1
 ├───────────┼───────────┤   ← Data point 2
 │     │     │     │     │
```

---

### Radar/Spider Chart

**Purpose:** Multivariate profile comparison

**Use Cautiously:**
- Area distortion makes comparison misleading
- Axis order affects perceived patterns
- Hard to read exact values
- Many experts recommend alternatives

**When Acceptable:**
- Familiar domain (gaming, sports stats)
- Comparing 2-3 entities
- Audience expects this format
- 5-8 dimensions maximum

**Better Alternative:** Small multiples of bar charts

---

### Small Multiples (Trellis Plots)

**Purpose:** Compare patterns across many categories

**When to Use:**
- Comparing patterns across categories
- Regional comparisons with consistent metrics
- Time-period analysis (monthly breakdown)
- When faceting reveals more than grouping

**Why It's Powerful:**
- Enables pattern recognition at a glance
- Maintains context while showing variation
- Avoids overcrowding single chart
- Scalable to many categories (4-20+ panels)

**Implementation:**
- Keep scales consistent across panels
- Use 2-6 columns depending on width
- Order by meaningful dimension
- Each panel readable at reduced size

---

## Advanced Techniques

### Animated Transitions & Morphing

**Purpose:** Smooth transformations between states

**When to Use:**
- Before/after comparisons
- Showing data evolution
- Narrative-driven presentations
- Reducing cognitive load during changes

**Implementation:**
- D3.js transitions with interpolators
- Duration: 500-800ms typical
- Easing: ease-in-out for natural feel
- Maintain data keys for object constancy

**Code Pattern:**
```javascript
svg.selectAll('circle')
  .data(newData, d => d.id)
  .transition()
  .duration(750)
  .ease(d3.easeCubicInOut)
  .attr('cx', d => xScale(d.value));
```

**Cautions:**
- Don't overuse (becomes gimmicky)
- Provide option to skip for accessibility
- Performance concerns with 1000+ elements

---

### Bubble Timeline

**Purpose:** Events of varying importance over time

**When to Use:**
- Product releases with impact metrics
- Historical events with varying significance
- Milestone visualization

**Implementation:**
- Horizontal time axis
- Circle AREA (not radius) proportional to value
- Labels for major events
- Color by category

---

*For working code examples, see:*
- `javascript/recharts-examples.md`
- `javascript/d3-patterns.md`
- `python/plotly-examples.md`
