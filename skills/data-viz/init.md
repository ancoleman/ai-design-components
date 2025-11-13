# AI-Assisted Component Library: Master Plan
## Data Visualization Components for Claude

**Document Version:** 1.0  
**Date:** November 10, 2025  
**Purpose:** Comprehensive research and strategic planning for building an AI-assisted component library focused on data visualization

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Part 1: Claude Skills Architecture](#part-1-claude-skills-architecture)
3. [Part 2: Component Library Organization](#part-2-component-library-organization)
4. [Part 3: 24+ Visualization Methods](#part-3-24-visualization-methods)
5. [Part 4: Implementation Strategy](#part-4-implementation-strategy)
6. [Part 5: Visualization Selection Matrix](#part-5-visualization-selection-matrix)
7. [Part 6: Next Steps & Decision Framework](#part-6-next-steps--decision-framework)

---

## Executive Summary

This document outlines a comprehensive strategy for building a component library that assists AI agents in selecting and implementing appropriate design components for data visualization projects. The approach leverages Claude's skills architecture for progressive disclosure, combines modern data visualization best practices from 2024-2025 research, and provides a systematic framework for matching visualization types to analytical tasks.

**Key Innovations:**
- 3-tier hierarchical system (Primitives → Purpose-Driven → Advanced)
- 24+ detailed visualization methods with use-case guidance
- Progressive disclosure design for token efficiency
- Purpose-first selection (not chart-first)
- Integration with Claude's native tooling capabilities

---

## Part 1: Claude Skills Architecture

### Understanding Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. They function as "onboarding guides" for specific domains, transforming Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge.

### Core Principles

#### 1. Conciseness is Key
- **Context window is a public good** - Skills share space with system prompts, conversation history, and user requests
- **Default assumption: Claude is already smart** - Only add context Claude doesn't inherently possess
- **Challenge each piece of information** - Ask "Does Claude really need this?" and "Does this justify its token cost?"
- **Prefer concise examples over verbose explanations**

#### 2. Set Appropriate Degrees of Freedom

Match specificity to task fragility:

- **High freedom (text-based instructions)**: Multiple valid approaches, context-dependent decisions, heuristic-guided
- **Medium freedom (pseudocode/parameterized scripts)**: Preferred pattern exists, acceptable variation, configuration-dependent
- **Low freedom (specific scripts)**: Fragile operations, consistency critical, specific sequences required

#### 3. Progressive Disclosure Design

Three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words, ideally <500 lines)
3. **Bundled resources** - As needed by Claude (unlimited since scripts can execute without loading)

### Recommended File Structure

```
data-viz-components/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: data-viz-components
│   │   └── description: [comprehensive triggering description]
│   └── Markdown instructions (required)
│       ├── Quick start workflow
│       ├── Component selection guide
│       └── References to detailed docs
└── Resources (optional)
    ├── scripts/
    │   ├── generate_chart.py
    │   ├── process_data.py
    │   └── validate_accessibility.py
    ├── references/
    │   ├── chart-types.md (detailed catalog)
    │   ├── color-systems.md (palettes & accessibility)
    │   ├── interaction-patterns.md (hover, click, zoom, etc.)
    │   ├── best-practices.md (2024-2025 standards)
    │   ├── accessibility-standards.md (WCAG compliance)
    │   └── selection-matrix.md (decision trees)
    └── assets/
        ├── templates/
        │   ├── dashboard-template.html
        │   └── report-template.jsx
        ├── color-palettes/
        │   ├── accessible-palette.json
        │   └── categorical-schemes.json
        └── example-datasets/
            ├── sales-data.csv
            └── time-series.json
```

### Key Documentation Patterns

#### Pattern 1: High-level Guide with References
```markdown
# Data Visualization Components

## Quick Start

For most comparisons, use a bar chart:
[concise code example]

## Advanced Techniques

- **Time series analysis**: See [TIME-SERIES.md](references/time-series.md)
- **Geospatial visualization**: See [MAPS.md](references/maps.md)
- **Interactive patterns**: See [INTERACTIONS.md](references/interactions.md)
```

Claude loads reference files only when needed.

#### Pattern 2: Selection Workflow
```markdown
# Component Selection Process

1. **Assess your data**
   - What type? (categorical, continuous, temporal, spatial)
   - How many dimensions?
   - How many data points?

2. **Determine your purpose**
   - Compare values? → Bar Chart
   - Show trend? → Line Chart
   - Reveal distribution? → Histogram/Violin
   - Explain composition? → Treemap/Stacked Bar

3. **Choose tier** (see Component Hierarchy below)
```

### SKILL.md Frontmatter Example

```yaml
---
name: data-viz-components
description: Comprehensive component library for data visualization. Use when building dashboards, reports, or any data-driven interfaces requiring charts, graphs, or visual analytics. Includes 24+ visualization types optimized for different data stories - trends, comparisons, distributions, relationships, flows, hierarchies, and geospatial analysis. Provides design patterns, interaction guidelines, color systems, and accessibility standards. Triggered by requests to create visualizations, choose chart types, build dashboards, or represent data visually.
---
```

---

## Part 2: Component Library Organization

### 3-Tier Hierarchical System

This organization balances cognitive load, token efficiency, and use-case specificity.

#### **TIER 1: Fundamental Primitives**

*Always available as foundational knowledge*

**Encoding Systems** - How data maps to visual properties:
- Position (x, y coordinates)
- Size (length, area, volume)
- Color (hue, saturation, luminance)
- Shape (circle, square, triangle, custom)
- Texture (patterns, fills)
- Orientation (angle, direction)

**Mark Types** - Basic visual elements:
- Points (dots, symbols)
- Lines (straight, curved, stepped)
- Areas (filled regions)
- Bars (rectangles, columns)
- Arcs (circular segments)

**Interaction Patterns** - User engagement methods:
- Hover (tooltips, highlights)
- Click (selection, drill-down)
- Drag (pan, reorder)
- Zoom (scale, focus+context)
- Filter (subset selection)
- Brush (range selection)

---

#### **TIER 2: Purpose-Driven Compositions**

*Context-triggered based on analytical task*

##### **Comparison Group**
Visual comparison of values across categories

- **Bar Chart** - Horizontal or vertical rectangles for categorical comparison
- **Column Chart** - Vertical bars for discrete comparisons
- **Grouped Bar** - Multiple series side-by-side
- **Stacked Bar** - Cumulative composition comparison
- **Lollipop Chart** - Space-efficient alternative to bars
- **Bullet Chart** - Compact performance indicators

##### **Trend Group**
Showing change over time or continuous variables

- **Line Chart** - Connected points showing progression
- **Area Chart** - Filled line chart emphasizing magnitude
- **Stream Graph** - Stacked area with organic flowing baseline
- **Slope Graph** - Two-point comparison emphasizing change rate
- **Sparklines** - Minimal inline trend indicators
- **Step Chart** - Discrete value changes over time

##### **Distribution Group**
Revealing how data is spread or clustered

- **Histogram** - Frequency distribution in bins
- **Box Plot** - Summary statistics (quartiles, outliers)
- **Violin Plot** - Box plot + density curve
- **Ridge Plot** - Overlapping density curves for multiple groups
- **Density Plot** - Smooth continuous distribution
- **Beeswarm Plot** - Individual points showing distribution

##### **Relationship Group**
Exploring correlations and connections

- **Scatter Plot** - Two-variable relationship as points
- **Bubble Chart** - Scatter plot with size encoding third variable
- **Connected Scatter** - Scatter plot with temporal sequence
- **Hexbin Plot** - 2D histogram for dense scatter data
- **Correlation Matrix** - Grid showing pairwise correlations
- **Network Graph** - Nodes and edges showing connections

##### **Part-to-Whole Group**
Showing composition and proportions

- **Pie Chart** - Circular sections (use with caution, max 5-6 slices)
- **Donut Chart** - Pie chart with center removed
- **Treemap** - Nested rectangles sized by value
- **Sunburst** - Radial treemap showing hierarchy
- **Stacked Bar** - Cumulative bars showing composition
- **Waterfall Chart** - Sequential cumulative changes

##### **Geospatial Group**
Location-based visualizations

- **Choropleth Map** - Regions colored by value
- **Symbol Map** - Markers placed at locations
- **Flow Map** - Lines showing movement between locations
- **Heat Map (Geographic)** - Density overlay on map
- **Cartogram** - Map distorted by data values
- **Dot Density Map** - Individual dots representing quantities

---

#### **TIER 3: Advanced Analytical Constructs**

*Specialist-triggered for complex data stories*

##### **Multi-dimensional**
Handling 3+ variables simultaneously

- **Parallel Coordinates** - Multiple vertical axes with connecting lines
- **Radar Chart** - Radial axes forming polygon (use cautiously)
- **Small Multiples** - Grid of identical charts with different data slices
- **Scatterplot Matrix (SPLOM)** - Grid showing all pairwise relationships
- **3D Surface Plot** - Continuous surface for two-variable functions
- **Heatmap Matrix** - Grid with color encoding values

##### **Temporal**
Sophisticated time-based analysis

- **Gantt Chart** - Task scheduling with duration bars
- **Timeline** - Chronological event sequence
- **Calendar Heatmap** - Grid of days colored by metric
- **Arc Diagram** - Temporal relationships as arcs
- **Horizon Chart** - Layered area charts for compact time series
- **Candlestick Chart** - OHLC (Open-High-Low-Close) financial data

##### **Flow & Process**
Visualizing movement and transformation

- **Sankey Diagram** - Flow with width proportional to quantity
- **Chord Diagram** - Circular flow showing inter-relationships
- **Alluvial Diagram** - Flow showing changes over discrete steps
- **Flowchart** - Process steps with decision points
- **Stream Graph** - Stacked area with flowing baseline
- **Arc Diagram** - Connections as arcs above linear axis

##### **Hierarchical**
Nested structures and taxonomies

- **Dendrogram** - Tree structure showing hierarchy
- **Icicle Plot** - Rectangular hierarchy from root to leaves
- **Circle Packing** - Nested circles sized by value
- **Radial Tree** - Tree layout in circular arrangement
- **Treemap** - Nested rectangles (also in Part-to-Whole)
- **Sunburst** - Radial treemap (also in Part-to-Whole)

---

## Part 3: 24+ Visualization Methods

*Extremely effective ways to visualize data - detailed analysis*

---

### 1. ANIMATED TRANSITIONS & MORPHING

**What It Is:**  
Smooth transformations between visualization states, where marks smoothly move, resize, or change type while maintaining object constancy (same data points remain recognizable across views).

**When to Use:**
- Comparing before/after states
- Showing data evolution over time
- Creating narrative-driven presentations
- Guiding users through complex data exploration
- Reducing cognitive load during state changes

**Why It's Powerful:**
- Maintains mental model during transitions
- Helps users track individual elements
- Creates engaging, memorable experiences
- Reduces disorientation from abrupt changes
- Effective for storytelling and presentations

**Implementation Guidance:**
- Use D3.js transitions with interpolators
- Implement spring physics (Framer Motion, GSAP)
- Duration: 500-800ms for most transitions
- Easing: ease-in-out for natural feel
- Maintain consistent data keys for object constancy

**Code Pattern:**
```javascript
// D3.js example
svg.selectAll('circle')
  .data(newData, d => d.id) // Key function for constancy
  .transition()
  .duration(750)
  .ease(d3.easeCubicInOut)
  .attr('cx', d => xScale(d.value))
  .attr('r', d => rScale(d.size))
  .style('fill', d => colorScale(d.category));
```

**Example Use Cases:**
- Sales dashboard morphing from bars → lines → map as time range changes
- Product comparison transitioning from table → scatter → radar
- Portfolio allocation flowing from pie → treemap → sunburst

**Cautions:**
- Don't overuse - can become gimmicky
- Ensure transitions serve purpose, not just decoration
- Provide option to skip animations for accessibility
- Performance concerns with 1000+ elements

---

### 2. SMALL MULTIPLES (TRELLIS PLOTS)

**What It Is:**  
Grid arrangement of identical chart types, each showing different slices of data (by category, time period, or other dimension), using shared scales for direct comparison.

**When to Use:**
- Comparing patterns across multiple categories
- Regional comparisons with consistent metrics
- Time-period analysis (e.g., monthly breakdown)
- A/B test results across segments
- When faceting reveals more than grouping

**Why It's Powerful:**
- Enables pattern recognition at a glance
- Maintains context while showing variation
- Avoids overcrowding single chart
- Leverages human visual comparison abilities
- Scalable to many categories (4-20+ panels)

**Implementation Guidance:**
- Keep scales consistent across panels for valid comparison
- Use 2-6 columns depending on screen width
- Each panel should be readable at reduced size
- Add clear labels for each facet
- Consider ordering by a meaningful dimension

**Layout Patterns:**
```
[Panel 1] [Panel 2] [Panel 3]
[Panel 4] [Panel 5] [Panel 6]
[Panel 7] [Panel 8] [Panel 9]

Shared X-axis ↓
Shared Y-axis →
```

**Example Use Cases:**
- 12 line charts showing monthly sales trends for each region
- 4x3 grid of scatter plots showing correlations in different industries
- Multiple histograms comparing distributions across age groups
- Weather patterns for 10 cities using identical chart format

**Cautions:**
- Requires sufficient screen space
- Not ideal for mobile without scrolling
- Can be overwhelming if panels too small
- Consider interactive filtering as alternative

---

### 3. CONNECTED SCATTER PLOTS

**What It Is:**  
Traditional scatter plot with points connected in sequential order (usually time), creating a path that shows how the relationship between two variables evolves.

**When to Use:**
- Showing two-variable relationships changing over time
- Revealing trajectory and acceleration patterns
- Economic analysis (e.g., Phillips curve)
- Before/after with many intermediate states
- Cyclical relationship analysis

**Why It's Powerful:**
- Shows relationship AND temporal evolution simultaneously
- Reveals patterns like loops, spirals, reversals
- Can show acceleration/deceleration through path density
- Combines scatter plot and time series strengths
- Memorable visual form for key insights

**Implementation Guidance:**
- Add directional arrows or gradients to show time direction
- Label key points (start, end, inflection points)
- Consider using color gradient along path for temporal encoding
- Add annotations for major events affecting trajectory
- Optionally show dots at each time point

**Design Pattern:**
```
Y-axis ↑
      |     ●━━━━━━●
      |    ╱         ╲
      |   ●           ●
      |   │            │
      |   ●━━━●━━━━━━━●
      |   (loop pattern showing cyclic relationship)
      └─────────────────→ X-axis
      Start ●        ● End
```

**Example Use Cases:**
- GDP vs Life Expectancy over decades (Gapminder style)
- Inflation vs Unemployment (Phillips curve)
- Marketing spend vs Revenue quarter-by-quarter
- Stock price vs Trading volume over time
- Customer satisfaction vs Product quality scores monthly

**Cautions:**
- Can become cluttered with too many points
- Path crossing itself can be confusing
- Requires clear temporal direction indicators
- Not intuitive for all audiences

---

### 4. RIDGELINE PLOTS (JOY PLOTS)

**What It Is:**  
Multiple density curves or area charts stacked vertically with partial overlap, creating a mountain range appearance that shows distribution shapes across categories.

**When to Use:**
- Comparing distributions across many categories (6-30+)
- Showing distribution evolution over time
- Temperature/weather patterns by month
- Test score distributions by class/school
- Any data where distribution shape matters

**Why It's Powerful:**
- Shows both distribution shape and between-group comparison
- Aesthetically appealing and space-efficient
- Easier to read than many overlapping curves
- Natural reading from top to bottom
- Reveals patterns like bimodality, skew, shifts

**Implementation Guidance:**
- Stack from top to bottom (most recent/important first)
- Overlap by 20-40% for visibility without excess occlusion
- Use consistent horizontal scale across all curves
- Add subtle transparency or outline to distinguish layers
- Label each curve clearly on the left

**Visual Structure:**
```
Category A  [smooth curve ∩]
Category B    [smooth curve ∩]
Category C      [smooth curve ∩]
Category D        [smooth curve ∩]
```

**Example Use Cases:**
- Temperature distributions for each month showing seasonality
- Movie lengths by genre revealing distinct patterns
- Income distributions across decades showing inequality changes
- Commute times by city highlighting urban differences
- Test scores by school year showing improvement trends

**Cautions:**
- Overlapping can obscure exact values
- Not ideal for precise numerical reading
- Baseline can be ambiguous with overlap
- Cultural note: Originally called "Joy Plots" but renamed for sensitivity

---

### 5. VIOLIN PLOTS

**What It Is:**  
Combination of box plot and kernel density plot, showing distribution shape (via mirrored density curves on each side) along with summary statistics (median, quartiles) in the center.

**When to Use:**
- Comparing distributions across categories
- When distribution shape is as important as summary stats
- Revealing bimodal or multimodal distributions
- Scientific data with outliers and complex distributions
- When box plots hide important distribution features

**Why It's Powerful:**
- Shows full distribution, not just summary
- Reveals bimodality that box plots hide
- Combines statistical rigor with visual richness
- More informative than box plots alone
- Good for technical audiences

**Implementation Guidance:**
- Mirror density estimation around vertical axis
- Include box plot elements (median line, quartile box, whiskers)
- Optionally add individual data points as overlay
- Width of violin represents density at that value
- Use consistent vertical scale for comparison

**Anatomy:**
```
    ╭─────╮        ← Upper adjacent value
    │     │
    │     │        ← Upper quartile (Q3)
   ╱│─────│╲       ← Median
  │ │     │ │      ← Lower quartile (Q1)
   ╲│     │╱
    ╰─────╯        ← Lower adjacent value
```

**Example Use Cases:**
- Salary distributions across departments showing bimodal patterns
- Gene expression levels across experimental conditions
- Response times in different treatment groups
- Customer lifetime value by acquisition channel
- Product ratings showing polarization

**Cautions:**
- Requires more space than simple box plots
- Can be unfamiliar to non-technical audiences
- Density estimation can smooth over discrete data
- Less effective with very small sample sizes (<20 points)

---

### 6. STREAM GRAPHS (THEMERIVER)

**What It Is:**  
Stacked area chart with organic, flowing baseline (often center-weighted) that creates a river-like appearance showing evolving composition over time.

**When to Use:**
- Showing proportional change over time with aesthetic emphasis
- Displaying evolving composition of categories
- When you want to emphasize flow and continuity
- Cultural/music evolution over decades
- Technology adoption patterns

**Why It's Powerful:**
- Beautiful, engaging visual form
- Natural "flow" metaphor resonates with audiences
- Emphasizes continuity and organic change
- Center baseline reduces perceptual distortion
- Memorable for presentations

**Implementation Guidance:**
- Use center-weighted or symmetric baseline (ThemeRiver layout)
- Organic, flowing shapes rather than sharp edges
- Color carefully - related categories near each other
- Add interactive hover to isolate specific streams
- Consider using transparency for overlapping regions

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
    └──────────time→──────────┘
```

**Example Use Cases:**
- Music genre popularity flowing over decades (Last.fm)
- Technology stack adoption in companies over time
- Movie box office by genre showing cultural shifts
- Energy source mix evolving from coal → renewables
- Social media platform usage by age group

**Cautions:**
- Difficult to read exact values
- Baseline ambiguity can confuse some users
- Not suitable when precise comparison needed
- Can be challenging to implement correctly

---

### 7. SANKEY DIAGRAMS

**What It Is:**  
Flow diagram where connecting bands have width proportional to flow quantity, showing transfer, transformation, or allocation from sources through intermediate steps to destinations.

**When to Use:**
- Showing resource flow and transformation
- Budget allocation through departments
- Energy flow from sources to uses
- Customer journey through website
- Supply chain visualization

**Why It's Powerful:**
- Instantly reveals major flows and losses
- Shows redistribution and transformation
- Width encoding is highly intuitive
- Reveals inefficiencies and bottlenecks
- Comprehensive view of system flows

**Implementation Guidance:**
- Use D3-sankey or SankeyMATIC libraries
- Nodes represent states, links represent flows
- Link width proportional to quantity
- Color-code by category or source
- Add hover interactions for exact values

**Structure:**
```
Source A ━━━━━━━━━━━━━━━┓
                       ┃━━━━━→ Destination 1
Source B ━━━━━━┓      ┃
               ┃━━━━━━┛
               ┃━━━━━━━━━━━━━→ Destination 2
Source C ━━━━━━┛
    ↑              ↑
  Inputs      Intermediate      Outputs
```

**Example Use Cases:**
- Energy flow: Production → Transformation → Consumption → Waste
- Budget: Revenue streams → Departments → Projects → Expenses
- Customer flow: Acquisition → Engagement → Conversion → Retention
- Manufacturing: Raw materials → Processing → Assembly → Distribution
- Website traffic: Entry pages → Navigation → Conversions → Exits

**Cautions:**
- Can become cluttered with many nodes
- Crossing flows reduce readability
- Requires careful node ordering
- Not suitable for cyclic flows

---

### 8. CHORD DIAGRAMS

**What It Is:**  
Circular layout where entities are arranged around a circle's perimeter, with ribbons connecting them to show relationships or flows, with ribbon width representing strength or quantity.

**When to Use:**
- Displaying inter-relationships in a network
- Flow between entities in circular arrangement
- Migration patterns between regions
- Trade relationships between countries
- Character co-occurrence in literature

**Why It's Powerful:**
- Compact representation of full relationship matrix
- Visually striking and memorable
- Shows bidirectional or unidirectional flows
- Circular symmetry aids comparison
- Space-efficient for many-to-many relationships

**Implementation Guidance:**
- Use D3-chord or similar library
- Order entities logically around circle
- Color-code by category or cluster
- Ribbon opacity can show direction or confidence
- Add hover highlighting to follow connections

**Layout:**
```
         Entity A
          ╱    ╲
         ╱      ╲━━━━━━━━━━┓
        ╱              ╲   ┃
   Entity B            Entity D
        ╲               ╱   ┃
         ╲      ╱━━━━━━━━━━┛
          ╲    ╱
         Entity C
```

**Example Use Cases:**
- Trade flows between countries showing bilateral relationships
- Migration patterns between cities/regions
- Co-occurrence of skills in job postings
- Gene regulatory networks
- Collaboration patterns between departments

**Cautions:**
- Can become dense with many connections
- Difficult to follow individual relationships in complex diagrams
- Not intuitive for all audiences
- Poor for precise value reading

---

### 9. PARALLEL COORDINATES

**What It Is:**  
Multiple vertical parallel axes representing different variables, with each data point shown as a polyline connecting its values across all axes.

**When to Use:**
- Exploring multivariate data (5-15 dimensions)
- Finding patterns across multiple dimensions
- Filtering and brushing high-dimensional data
- Comparing profiles of entities
- Identifying clusters and outliers

**Why It's Powerful:**
- Shows high-dimensional relationships in 2D
- Interactive brushing reveals patterns
- Can display hundreds of observations
- Reveals correlations and anti-correlations
- Effective for data with mixed scales

**Implementation Guidance:**
- Normalize axes to comparable ranges
- Use brushing interaction to filter/highlight
- Allow axis reordering to reveal different patterns
- Add transparency to manage overplotting
- Consider bundling or sampling for dense datasets

**Structure:**
```
Var1  Var2  Var3  Var4  Var5
 │     │     │     │     │
 ├─────┼─────┼─────┼─────┤   ← Data point 1
 ├───────────┼───────────┤   ← Data point 2
 ├─────────────────┼─────┤   ← Data point 3
 │     │     │     │     │
min  min   min   min   min
max  max   max   max   max
```

**Example Use Cases:**
- Car comparisons across MPG, price, horsepower, weight, acceleration
- Product feature analysis across multiple attributes
- Student performance across different subjects
- Chemical properties of compounds
- Financial ratios for company comparison

**Cautions:**
- Overplotting with many observations
- Axis order affects pattern visibility
- Steep learning curve for some users
- Requires interactivity to be effective

---

### 10. HEXBIN PLOTS

**What It Is:**  
2D histogram using hexagonal bins instead of square bins to show density of point clouds, with color or height representing point count in each hexagon.

**When to Use:**
- Scatter plots with thousands of overlapping points
- Geographic density visualization
- Heatmap alternative with better tiling properties
- When individual points are less important than density
- Large dataset visualization (10,000+ points)

**Why It's Powerful:**
- Handles overplotting better than scatter plots
- Hexagons tile more naturally than squares
- Shows density patterns at multiple scales
- More aesthetically pleasing than square bins
- Reduces moiré patterns in regular grids

**Implementation Guidance:**
- Choose bin size based on data density (D3-hexbin)
- Use color gradient to show density
- Optionally use hexagon height in 3D view
- Add contour lines for major density levels
- Provide zoom interaction for multi-scale exploration

**Visual Pattern:**
```
  ⬡ ⬡ ⬡ ⬡ ⬡
 ⬡ ⬢ ⬢ ⬡ ⬡    ⬡ = Low density
  ⬡ ⬢ ⬢ ⬢ ⬡   ⬢ = Medium density
 ⬡ ⬢ ⬢ ⬢ ⬡    ⬢ = High density (darker)
  ⬡ ⬡ ⬢ ⬡ ⬡
```

**Example Use Cases:**
- 100,000 customer locations showing geographic concentration
- Gene expression correlations with thousands of genes
- Website click heatmaps showing user attention
- Astrophysics data with millions of observations
- Network traffic analysis showing packet distribution

**Cautions:**
- Bin size choice affects patterns revealed
- Loss of individual point information
- Can miss outliers if bins too large
- Requires careful color scale selection

---

### 11. TREEMAPS

**What It Is:**  
Nested rectangles where size represents a quantitative value and nesting represents hierarchical structure, creating a space-filling visualization of hierarchical part-to-whole relationships.

**When to Use:**
- Showing hierarchical data with size comparison
- Portfolio allocation across sectors/stocks
- File system disk usage
- Budget breakdown by department and categories
- Market share visualization with sub-segments

**Why It's Powerful:**
- Space-efficient visualization of hierarchy
- Shows proportions and hierarchy simultaneously
- Can display thousands of items
- Immediate visual comparison of sizes
- Effective use of screen real estate

**Implementation Guidance:**
- Use squarified algorithm for better aspect ratios
- Color-code by category or performance metric
- Add borders to distinguish levels
- Implement zoom/drill-down for deep hierarchies
- Label only significant rectangles

**Layout Example:**
```
┌─────────────────────────────────┐
│ Category A                      │
│ ┌──────────┬──────────────────┐ │
│ │  A1      │      A2          │ │
│ └──────────┴──────────────────┘ │
└─────────────────────────────────┘
┌────────────┬────────────────────┐
│ Category B │   Category C       │
│ ┌───┬───┐  │   ┌─────┬────────┐│
│ │B1 │B2 │  │   │ C1  │   C2   ││
│ └───┴───┘  │   └─────┴────────┘│
└────────────┴────────────────────┘
```

**Example Use Cases:**
- Stock portfolio: Sectors → Industries → Individual stocks
- Budget: Departments → Teams → Projects → Line items
- Hard drive usage: Folders → Subfolders → Files
- Sales: Regions → Territories → Accounts → Products
- Market cap: Industries → Companies

**Cautions:**
- Difficult to compare similar-sized rectangles
- Deep hierarchies can become cluttered
- Labels may not fit in small rectangles
- Aspect ratios can be very elongated

---

### 12. SUNBURST DIAGRAMS

**What It Is:**  
Radial treemap where hierarchy radiates from center outward, with each ring representing a level of the hierarchy and arc angles proportional to values.

**When to Use:**
- Hierarchical data visualization with aesthetic emphasis
- Drill-down navigation through levels
- Circular/radial metaphor is appropriate
- Alternative to treemap when circularity desired
- Multi-level categorization

**Why It's Powerful:**
- Aesthetically appealing radial structure
- Shows depth and breadth of hierarchy clearly
- Natural drill-down interaction (click to zoom)
- Space-efficient for moderate-depth hierarchies
- Memorable visual form

**Implementation Guidance:**
- Center is root, outer rings are leaves
- Use color to encode categories or values
- Implement click-to-zoom for interactivity
- Add breadcrumb trail for navigation context
- Limit to 4-6 levels for readability

**Structure:**
```
        ┌─────── Level 3
    ┌───┴───── Level 2
  ┌─┴─── Level 1
  ● Root (center)
```

**Example Use Cases:**
- File system hierarchy with disk usage
- Organizational chart with employee counts
- Biological taxonomy from kingdom to species
- Website navigation structure with page views
- Product catalog: Category → Subcategory → Products

**Cautions:**
- Outer rings can become crowded
- Hard to compare arc lengths at different radii
- Not suitable for very deep hierarchies (>6 levels)
- Labels can be difficult to fit

---

### 13. CALENDAR HEATMAPS

**What It Is:**  
Grid of days arranged in calendar format (weeks as rows, days as columns), with each day colored by a metric value, revealing daily patterns and seasonality.

**When to Use:**
- Daily activity tracking and patterns
- Showing seasonality and weekly cycles
- Habit tracking and streaks
- Contribution graphs (GitHub-style)
- Event frequency over time

**Why It's Powerful:**
- Natural calendar metaphor everyone understands
- Instantly reveals weekly/monthly patterns
- Shows both micro (daily) and macro (seasonal) trends
- Visually appealing and engaging
- Good for personal metrics and gamification

**Implementation Guidance:**
- Use 7-column grid (Sunday-Saturday or Monday-Sunday)
- Each row represents one week
- Color scale from low to high activity
- Add month boundaries for navigation
- Include hover for exact values

**Layout:**
```
       M  T  W  T  F  S  S
Jan   ██ ▓▓ ░░ ▓▓ ██ ░░ ░░
      ▓▓ ██ ░░ ▓▓ ▓▓ ██ ░░
Feb   ░░ ▓▓ ██ ░░ ▓▓ ░░ ██
      ▓▓ ░░ ░░ ██ ▓▓ ░░ ░░

Legend: ░░ Low  ▓▓ Medium  ██ High
```

**Example Use Cases:**
- GitHub contribution graph showing coding activity
- Daily sales pattern revealing weekday/weekend differences
- Exercise/habit tracking showing consistency
- Temperature calendar revealing seasonal patterns
- Website traffic by day showing usage patterns

**Cautions:**
- Limited to daily-level granularity
- Requires full year for seasonal patterns
- Color scale must be carefully chosen
- Can miss hourly patterns

---

### 14. RADAR/SPIDER CHARTS

**What It Is:**  
Multiple axes radiating from a central point, with data points connected to form a polygon showing multivariate profiles.

**When to Use (with caution):**
- Comparing profiles across multiple attributes
- Sports player statistics (strength, speed, skill)
- Product feature comparison (5-8 features)
- Balanced scorecard visualization
- When radial metaphor is meaningful

**Why It's Powerful (but controversial):**
- Compact multi-attribute comparison
- Symmetrical display aids quick assessment
- Shows balance vs imbalance visually
- Good for identifying strengths/weaknesses
- Familiar in certain domains (gaming, sports)

**Implementation Guidance:**
- Limit to 5-8 axes for readability
- Arrange axes in meaningful order
- Use consistent scale across all axes
- Add gridlines for reference
- Consider normalizing values (0-100%)

**Structure:**
```
        Attribute A
             ↑
             ●━━━━━●  Attribute B
            ╱ ╲   ╱
           ╱   ╲ ╱
    Att F ●─────●
           ╲   ╱ ╲
            ╲ ╱   ╲
             ●━━━━━● Attribute C
```

**Example Use Cases:**
- Video game character stats (strength, agility, intelligence, etc.)
- Employee performance across competencies
- Product comparison across features
- Nutritional profiles of foods
- City livability across dimensions

**Cautions (Important):**
- Area distortion makes visual comparison misleading
- Axis order affects perceived patterns
- Hard to read exact values
- Many dataviz experts recommend alternatives (bar charts)
- Use only when audience familiar with format

---

### 15. BUBBLE TIMELINE

**What It Is:**  
Timeline with events represented as bubbles, where bubble size encodes a quantitative value (importance, revenue, impact), combining temporal sequence with magnitude.

**When to Use:**
- Showing events of varying importance over time
- Product release timelines with impact
- Milestone visualization with significance
- Historical events with varying impact
- Project timeline with resource allocation

**Why It's Powerful:**
- Combines temporal and quantitative information
- Size naturally draws attention to important events
- Clean, scannable format
- Good for storytelling and presentations
- Flexible for various event types

**Implementation Guidance:**
- Horizontal time axis
- Circle size proportional to value (careful: area not radius)
- Add labels for major events
- Use color to categorize event types
- Consider adding connecting lines for related events

**Visual Pattern:**
```
Time →
━━━━●━━━━━━━●━━━━━━━━━●━━━●━━━━━━━●━━
   small  medium    large small   medium
   event  event     event event   event
```

**Example Use Cases:**
- Product releases with revenue impact over company history
- Scientific discoveries with citation impact
- Marketing campaigns with ROI on timeline
- Funding rounds with amount raised
- Natural disasters with casualty counts

**Cautions:**
- Size perception can be misleading (use area not radius)
- Too many events create clutter
- Overlapping bubbles need careful handling
- May need interaction for details

---

### 16. SLOPE GRAPHS

**What It Is:**  
Two vertical axes representing two time points or states, with lines connecting each entity between the two points to show change and ranking shifts.

**When to Use:**
- Before/after comparisons
- Showing ranking changes between two periods
- Emphasizing rate and direction of change
- Comparing two states across many entities
- When change is more important than absolute values

**Why It's Powerful:**
- Emphasizes direction and magnitude of change
- Shows both individual changes and group patterns
- Easy to identify leaders, losers, and stability
- Clean, minimalist design
- Effective for presentations

**Implementation Guidance:**
- Left axis: Before state, Right axis: After state
- Lines slope shows direction (up/down/flat)
- Steeper slope = greater change
- Label important entities or extremes
- Use color to highlight key stories

**Layout:**
```
Before          After
  A 100 ━━━━━━━━ 120  +20%
  B  90 ━━━━━━━━  95  +5%
  C  80 ━━━━━━━━  75  -5%
  D  70 ━━━━━━━━  85  +15%
  E  60 ━━━━━━━━  50  -10%
```

**Example Use Cases:**
- City rankings change from 2020 to 2025
- Before/after treatment outcomes in clinical trial
- Company performance pre/post intervention
- Election results comparing two elections
- Student test scores at start vs end of course

**Cautions:**
- Only compares two points, not continuous change
- Can be cluttered with too many lines
- Crossing lines can reduce readability
- Not suitable for more than 2 time points

---

### 17. CANDLESTICK CHARTS

**What It Is:**  
Financial chart where each bar (candlestick) shows four values for a time period: open price, close price, high price, low price. Body color indicates whether close was higher (green/white) or lower (red/black) than open.

**When to Use:**
- Financial market data (stocks, crypto, forex)
- Any OHLC (Open-High-Low-Close) data
- Trading analysis and technical indicators
- Showing volatility and price action
- Time periods: minutes to months

**Why It's Powerful:**
- High information density in compact form
- Industry standard for traders and analysts
- Shows both trend and volatility
- Color-coding for quick sentiment reading
- Combines well with volume and indicators

**Implementation Guidance:**
- Rectangle body: open to close
- Wicks (thin lines): high and low
- Green/white: close > open (bullish)
- Red/black: close < open (bearish)
- Add volume bars below for confirmation

**Anatomy:**
```
    ─── High
     │
    ┌┴┐
    │█│ ← Body (Open to Close)
    │█│   Green if Close > Open
    └┬┘   Red if Close < Open
     │
    ─── Low
```

**Example Use Cases:**
- Stock price movements for technical analysis
- Cryptocurrency trading with high volatility
- Commodity futures price action
- Foreign exchange rate movements
- Any price data with open/high/low/close values

**Cautions:**
- Requires understanding of financial terminology
- Not intuitive for general audiences
- Needs sufficient time periods to be meaningful
- Can be misleading without volume context

---

### 18. WATERFALL CHARTS

**What It Is:**  
Stacked bars showing sequential positive and negative contributions that lead to a final total, with floating bars that show cumulative effect.

**When to Use:**
- Explaining variance from budget to actual
- Profit bridge (Revenue - Costs - Tax = Net)
- Sequential changes leading to final result
- Bridge analysis between two periods
- Showing contribution of factors to total

**Why It's Powerful:**
- Shows cumulative effect of sequential changes
- Explains "how we got here" narrative
- Identifies major positive/negative contributors
- Common in financial analysis
- Intuitive for explaining variance

**Implementation Guidance:**
- Start with initial value (bar from zero)
- Intermediate bars "float" showing change
- Use color: green for increases, red for decreases
- Connector lines between bars optional
- End with final total bar (from zero)

**Structure:**
```
120│         ┌────┐Final: 95
100│ ┌────┐ │    │
 80│ │    │╲│    │
 60│ │    │ ╲────┐
 40│ │    │      │
 20│ │    │      │
  0└─┴────┴──────┴────
    Start -15 -20 +10
```

**Example Use Cases:**
- Profit bridge: Revenue → COGS → OpEx → Tax → Net Income
- Budget variance: Plan → Volume → Price → Mix → Actual
- Cash flow: Opening balance → Operations → Investment → Financing → Closing
- Inventory changes: Beginning → Purchases → Sales → Ending
- Headcount: Jan → Hires → Departures → Transfers → Dec

**Cautions:**
- Order of components affects visual impact
- Floating bars can confuse some viewers
- Not suitable for circular flows
- Requires clear labeling

---

### 19. FORCE-DIRECTED NETWORK GRAPHS

**What It Is:**  
Network visualization where node positions emerge from physics simulation, with attractive forces between connected nodes and repulsive forces between all nodes.

**When to Use:**
- Exploring network structure and communities
- Social network analysis
- Knowledge graphs and ontologies
- Dependency mapping
- Identifying central/influential nodes

**Why It's Powerful:**
- Layout emerges naturally from structure
- Clusters and communities self-organize
- Interactive exploration (drag, zoom, filter)
- Central nodes naturally positioned centrally
- Reveals network topology

**Implementation Guidance:**
- Use D3-force or similar physics engine
- Adjust force strengths for optimal layout
- Node size by importance/degree
- Edge thickness by weight/strength
- Add labels for key nodes

**Simulation Forces:**
```
    ●─────●
   ╱│╲   ╱│╲
  ● │ ● ● │ ●    Forces:
   ╲│╱   ╲│╱     • Link attraction
    ●─────●      • Node repulsion
                 • Center gravity
                 • Collision detection
```

**Example Use Cases:**
- Social network showing friend connections and communities
- Citation network revealing influential papers
- Protein interaction networks
- Software dependency graphs
- Organizational collaboration patterns

**Cautions:**
- Large networks become hairballs (>100 nodes)
- Non-deterministic layout (different each time)
- Requires interaction for meaningful exploration
- Performance issues with thousands of nodes

---

### 20. 3D SURFACE PLOTS

**What It Is:**  
Continuous 3D surface showing function of two variables (z = f(x, y)), with shading and perspective providing depth cues.

**When to Use:**
- Visualizing mathematical functions
- Terrain elevation modeling
- Optimization landscapes
- Probability distributions in 2D
- Scientific/engineering applications

**Why It's Powerful:**
- Shows complex relationships in 3D space
- Natural representation for certain phenomena
- Shading enhances perception of form
- Can show peaks, valleys, ridges intuitively
- Useful for finding optima

**Implementation Guidance:**
- Use WebGL for performance (Three.js, Plotly)
- Add lighting and shading for depth perception
- Enable rotation interaction
- Optionally project contour lines to base
- Color gradient for additional encoding

**Visual Characteristics:**
```
     z↑
      │    ╱╲╱╲  ← Surface peaks
      │   ╱  ╲ ╲
      │  ╱    ╲╱  ← Valleys
      │ ╱
      └───────→ y
       ╱
      x
```

**Example Use Cases:**
- Machine learning loss landscapes for optimization
- Geographic terrain elevation models
- Probability density functions (bivariate normal)
- Response surfaces in experimental design
- Financial option pricing surfaces

**Cautions:**
- Can obscure data behind surfaces
- Occlusion issues with complex shapes
- Not accessible (screenreaders)
- Often better alternatives exist (contour plots)

---

### 21. MARIMEKKO CHARTS (MOSAIC PLOTS)

**What It Is:**  
Stacked bar chart where both the width and height of bars vary, showing two categorical variables and their proportions simultaneously.

**When to Use:**
- Market share by product line and region
- Showing two dimensions of proportions
- Category composition with category sizes varying
- Portfolio analysis across two dimensions
- Comparing sub-segments with different totals

**Why It's Powerful:**
- Shows proportions in two dimensions
- More information dense than simple stacked bars
- Reveals both composition and size differences
- Good for business presentations
- Intuitive once explained

**Implementation Guidance:**
- Width represents one category's proportion
- Height shows sub-category proportions within
- Both dimensions sum to 100%
- Use consistent color scheme for sub-categories
- Label segments clearly

**Structure:**
```
100%│████│█████│███│
    │░░░░│▓▓▓▓▓│░░░│
    │████│█████│███│
 0% └────┴─────┴───┘
    30%  45%  25%
    (Category widths)
```

**Example Use Cases:**
- Market share: Product lines (width) × Regions (height)
- Revenue: Business units (width) × Product types (height)
- Portfolio: Asset classes (width) × Risk levels (height)
- Sales: Channels (width) × Customer segments (height)
- Energy: Sources (width) × Uses (height)

**Cautions:**
- Can be confusing for unfamiliar audiences
- Hard to compare areas of different shapes
- Requires careful labeling
- Not suitable for more than 2 dimensions

---

### 22. WORD CLOUDS (WITH CAVEATS)

**What It Is:**  
Text visualization where word size is proportional to frequency or importance, arranged in visually appealing layout.

**When to Use (sparingly):**
- Quick visual summary of text content
- Identifying dominant themes at a glance
- Presentations where precision not critical
- Exploratory analysis starting point
- Aesthetic/decorative purposes

**Why It Can Be Powerful:**
- Immediate visual impression of content
- Accessible to all audiences
- Engaging and shareable
- Good for non-technical presentations

**Why It's Often Criticized:**
- Lacks precision - hard to compare sizes
- No context or relationships
- Better alternatives exist (bar charts)
- Can be misleading
- Often used poorly

**Implementation Guidance:**
- Use when approximate patterns sufficient
- Consider alternatives first
- If using: consistent font, clear size differences
- Remove stop words
- Consider stemming/lemmatization

**Better Alternatives:**
- Horizontal bar chart (more accurate)
- Treemap (hierarchical relationships)
- Network graph (word co-occurrence)

**Example Use Cases (acceptable):**
- Marketing campaign theme identification
- Initial exploration of survey responses
- Conference presentation decoration
- Social media post thumbnails

**Strong Recommendation:**
Use word clouds only for quick impressions or decorative purposes. For analysis requiring precision, use bar charts or treemaps instead.

---

### 23. ANNOTATED TIME SERIES

**What It Is:**  
Line or area chart enriched with contextual annotations, reference lines, highlighted regions, and explanatory text that tells the story behind the data.

**When to Use:**
- Explaining causes of trends and changes
- Narrative-driven data presentations
- Financial market commentary
- Showing impact of events on metrics
- Storytelling with data

**Why It's Powerful:**
- Combines data with narrative
- Highlights key insights
- Provides context for understanding
- Makes data memorable
- Guides audience interpretation

**Implementation Guidance:**
- Start with clean line/area chart
- Add vertical lines or bands for events
- Include text annotations for key points
- Use reference lines (averages, targets)
- Highlight regions of interest
- Don't over-annotate

**Annotation Types:**
```
         ↑ "Product launch"
100      │
         │  ┌───────┐
 75      │  │ "Peak │ ← Annotation
         │  │ season"│
 50 ─────┼──┴───────┴─── ← Reference line
         │              ← Highlighted region
 25      │
    ─────┴───────────────
   Jan   Mar   May   Jul
```

**Example Use Cases:**
- Stock price with earnings announcements, news events
- Website traffic with marketing campaign launches
- Sales with seasonal patterns and promotions highlighted
- Economic indicators with policy changes marked
- COVID-19 cases with intervention timing

**Cautions:**
- Too many annotations create clutter
- Balance data visibility with context
- Ensure annotations enhance, not distract
- Maintain objectivity in commentary

---

### 24. INTERACTIVE DRILL-DOWN HIERARCHIES

**What It Is:**  
Hierarchical visualization with click-to-expand/collapse functionality, allowing progressive exploration from high-level overview to detailed leaf nodes.

**When to Use:**
- Large hierarchical datasets
- Organizational charts with hundreds of nodes
- File/folder explorers
- Product taxonomies
- When full hierarchy too large to show at once

**Why It's Powerful:**
- Manages complexity through progressive disclosure
- User controls exploration path
- Reduces initial cognitive load
- Scalable to thousands of nodes
- Natural drill-down metaphor

**Implementation Guidance:**
- Start with top 1-2 levels visible
- Click node to expand/collapse children
- Show expand/collapse indicators (+ / -)
- Highlight current path (breadcrumbs)
- Smooth animations for transitions
- Search functionality for large hierarchies

**Interaction Pattern:**
```
Initial:
[+] Root
  [+] Category A
  [+] Category B

After clicking Category A:
[+] Root
  [-] Category A
    [+] Subcategory A1
    [+] Subcategory A2
  [+] Category B
```

**Example Use Cases:**
- Corporate organizational chart (1000+ employees)
- Product catalog with deep category nesting
- File system browser
- Knowledge base with hierarchical topics
- Geographic breakdown: Country → State → City → Neighborhood

**Cautions:**
- Can become clicking maze if too deep
- Users may miss important branches
- Provide search/filter for large hierarchies
- Consider alternative views (treemap) for overview

---

## Part 4: Implementation Strategy

### Recommended SKILL.md Structure

```markdown
---
name: data-viz-components
description: Comprehensive component library for data visualization. Use when building dashboards, reports, or any data-driven interfaces requiring charts, graphs, or visual analytics. Includes 24+ visualization types optimized for different data stories (trends, comparisons, distributions, relationships, flows, hierarchies, geospatial). Provides design patterns, interaction guidelines, color systems, and accessibility standards. Triggered by requests to: create visualizations, choose chart types, build dashboards, represent data visually, design data interfaces, or explain data effectively.
---

# Data Visualization Component Library

## Overview

This skill helps you select and implement the most effective visualization for your data and analytical purpose. It provides a systematic framework for matching data characteristics with visualization types, ensuring clarity, accessibility, and impact.

## Quick Start Workflow

### 1. Assess Your Data
- **Type**: Categorical, continuous, temporal, spatial, or hierarchical?
- **Dimensions**: How many variables? (1D, 2D, multivariate?)
- **Volume**: How many data points? (<100, 100-1000, >1000)
- **Characteristics**: Any outliers, missing values, or special patterns?

### 2. Determine Your Purpose
What story are you trying to tell?

- **Compare values** → Bar Chart, Lollipop
- **Show trend over time** → Line Chart, Area Chart
- **Reveal distribution** → Histogram, Violin Plot
- **Explore relationships** → Scatter Plot, Hexbin
- **Explain composition** → Treemap, Stacked Bar
- **Visualize flow** → Sankey, Chord Diagram
- **Display hierarchy** → Sunburst, Dendrogram
- **Show geographic patterns** → Choropleth, Symbol Map

### 3. Choose Appropriate Tier

**Tier 1 - Fundamental Primitives** (Simple, common tasks)
- Bar charts, line charts, scatter plots
- Use when: Standard comparisons, basic trends, simple relationships

**Tier 2 - Purpose-Driven Compositions** (Specific analytical tasks)
- Violin plots, stream graphs, parallel coordinates
- Use when: Need specialized visualization for specific insight type

**Tier 3 - Advanced Constructs** (Complex data stories)
- Force-directed networks, 3D surfaces, interactive hierarchies
- Use when: Data is complex, audience is sophisticated, exploration needed

### 4. Apply Design Patterns

Once you've selected a visualization type, enhance it with:

- **Color systems**: See [COLOR-SYSTEMS.md](references/color-systems.md)
- **Interaction patterns**: See [INTERACTIONS.md](references/interactions.md)
- **Accessibility**: See [ACCESSIBILITY.md](references/accessibility.md)
- **Annotations**: See [ANNOTATIONS.md](references/annotations.md)

### 5. Implement and Iterate

Build the visualization, test with actual data, gather feedback, and refine.

## Detailed Component Reference

For comprehensive details on each visualization type, see:
- [COMPARISON-CHARTS.md](references/comparison-charts.md) - Bar, column, lollipop, bullet
- [TREND-CHARTS.md](references/trend-charts.md) - Line, area, stream, slope
- [DISTRIBUTION-CHARTS.md](references/distribution-charts.md) - Histogram, box, violin, ridge
- [RELATIONSHIP-CHARTS.md](references/relationship-charts.md) - Scatter, bubble, hexbin, parallel
- [COMPOSITION-CHARTS.md](references/composition-charts.md) - Pie, treemap, sunburst, waterfall
- [FLOW-CHARTS.md](references/flow-charts.md) - Sankey, chord, alluvial
- [HIERARCHY-CHARTS.md](references/hierarchy-charts.md) - Dendrogram, circle packing, treemap
- [GEOSPATIAL-CHARTS.md](references/geospatial-charts.md) - Choropleth, symbol, flow maps
- [ADVANCED-TECHNIQUES.md](references/advanced-techniques.md) - All 24+ methods detailed

## Common Mistakes to Avoid

1. **Chart-first thinking** - Choose based on purpose, not aesthetics
2. **Pie charts for >6 categories** - Use bar chart instead
3. **Dual-axis charts** - Usually misleading, use small multiples
4. **3D when 2D sufficient** - Adds complexity without benefit
5. **Rainbow color scales** - Not perceptually uniform or colorblind-safe
6. **Too many colors** - Limit to 6-8 distinct categories
7. **Truncated y-axis without clear indication** - Can mislead
8. **Missing context** - Always label axes, add units, cite sources

## Best Practices (2024-2025 Standards)

### Clarity
- Start with simplest visualization that conveys the message
- Remove chartjunk and unnecessary decorations
- Use clear, explicit labels (including units)
- Provide adequate context (source, date, methodology)

### Accessibility
- Minimum contrast ratio: 4.5:1 (WCAG AA)
- Don't rely on color alone
- Provide text alternatives
- Support keyboard navigation
- Test with screenreaders

### Interactivity
- Use progressive disclosure for complex data
- Provide tooltips for details on demand
- Enable filtering and brushing where appropriate
- Maintain context during interactions

### Performance
- Optimize for dataset size (sample, aggregate for >10k points)
- Use canvas for >1000 points, SVG for <1000
- Implement virtualization for large datasets
- Consider using WebGL for 3D or high-volume

## When to Use Each Tier

### Use Tier 1 (Fundamental Primitives) when:
- Audience is general/non-technical
- Data story is straightforward
- Clarity and simplicity are paramount
- Presentation time is limited

### Use Tier 2 (Purpose-Driven Compositions) when:
- Specific analytical insight required
- Standard charts insufficient
- Audience has moderate data literacy
- Exploration of patterns needed

### Use Tier 3 (Advanced Constructs) when:
- Data is inherently complex (high-dimensional, networked)
- Audience is sophisticated
- Interactive exploration is valuable
- Standard approaches have been exhausted

## Examples by Use Case

### Business Dashboard
- **KPIs**: Big numbers with sparklines
- **Trends**: Line charts with annotations
- **Comparisons**: Bar charts
- **Composition**: Stacked bars or treemaps
- **Geographic**: Choropleth maps

### Scientific Publication
- **Distributions**: Violin plots, box plots
- **Relationships**: Scatter plots with confidence regions
- **Time series**: Line charts with error bands
- **Multivariate**: Parallel coordinates, small multiples

### Executive Presentation
- **Keep simple**: Bar, line, and slope charts
- **Heavy annotation**: Context and storytelling
- **Minimal charts**: One insight per slide
- **High contrast**: Clear from distance

### Exploratory Analysis
- **Interactive**: Brushing, filtering, drilling
- **Multiple views**: Linked charts
- **Flexible**: Support hypothesis generation
- **Raw access**: Show underlying data

## Tools and Technologies

### Recommended Libraries
- **D3.js**: Maximum flexibility, steep learning curve
- **Plotly**: Quick interactive charts
- **Observable Plot**: Modern, concise D3 successor
- **Recharts**: React-based, component approach
- **Vega-Lite**: Declarative grammar
- **Chart.js**: Simple, lightweight

### Implementation Approach
1. Start with library (Plotly, Chart.js) for speed
2. Customize with D3 when needed for unique requirements
3. Optimize performance for production
4. Add accessibility features
5. Test across devices and browsers

---

*For detailed implementation examples, code snippets, and interactive demos, see the `references/` directory.*
```

---

## Part 5: Visualization Selection Matrix

### Quick Reference Table

| Data Story | Primary Choice | Alternative | Advanced | Notes |
|------------|---------------|-------------|----------|-------|
| **Compare categories** | Bar Chart | Lollipop Chart | Slope Graph | Bar chart universally understood |
| **Show trend over time** | Line Chart | Area Chart | Stream Graph | Line chart best for single series |
| **Part-to-whole composition** | Stacked Bar | Treemap | Sunburst | Avoid pie charts with >6 slices |
| **Distribution shape** | Histogram | Violin Plot | Ridgeline Plot | Violin shows more than box plot |
| **Correlation/relationship** | Scatter Plot | Hexbin (dense) | Parallel Coords | Hexbin for >1000 points |
| **Flow/transformation** | Sankey Diagram | Chord Diagram | Alluvial | Width = quantity is intuitive |
| **Ranking changes** | Slope Graph | Bump Chart | Animated Bar Race | Slope best for 2 time points |
| **Dense time series** | Calendar Heatmap | Small Multiples | Horizon Chart | Calendar for daily patterns |
| **Network structure** | Force-Directed | Arc Diagram | Adjacency Matrix | Force for <200 nodes |
| **Hierarchy** | Treemap | Sunburst | Icicle Plot | Treemap more space-efficient |
| **Geographic patterns** | Choropleth Map | Symbol Map | Flow Map | Choropleth for regional aggregates |
| **Multivariate** | Parallel Coords | Small Multiples | Radar (caution) | Parallel for 5-15 dimensions |
| **Frequency/counts** | Histogram | Bar Chart | Dot Plot | Histogram for continuous data |
| **Before/after** | Slope Graph | Dumbbell | Side-by-side Bars | Slope emphasizes change |
| **Cumulative effect** | Waterfall Chart | Area Chart | Step Chart | Waterfall explains variance |

---

### Decision Tree

```
START: What is your primary goal?
│
├─→ COMPARE VALUES ACROSS CATEGORIES
│   ├─ How many categories? 
│   │  ├─ <10 → Bar Chart
│   │  ├─ 10-20 → Bar Chart (sorted)
│   │  └─ >20 → Consider filtering or treemap
│   │
│   ├─ Multiple series to compare?
│   │  ├─ Yes, stacked → Stacked Bar
│   │  ├─ Yes, side-by-side → Grouped Bar
│   │  └─ No → Bar Chart
│   │
│   └─ Need to emphasize differences?
│      ├─ Yes → Lollipop Chart
│      └─ Between two time points → Slope Graph
│
├─→ SHOW CHANGE OVER TIME
│   ├─ One series → Line Chart
│   ├─ Multiple series?
│   │  ├─ <5 series → Multiple Lines
│   │  ├─ 5-10 series → Small Multiples
│   │  └─ >10 series → Interactive filter or heatmap
│   │
│   ├─ Want to show composition over time?
│   │  ├─ Proportions → Stacked Area (normalize to 100%)
│   │  ├─ Absolute values → Stacked Area
│   │  └─ Flowing aesthetic → Stream Graph
│   │
│   └─ Just two time points?
│      └─ Slope Graph
│
├─→ REVEAL DISTRIBUTION
│   ├─ Single variable → Histogram
│   ├─ Compare distributions?
│   │  ├─ 2-4 groups → Overlaid Histograms or Box Plots
│   │  ├─ 5-10 groups → Violin Plots
│   │  └─ >10 groups → Ridgeline Plot
│   │
│   └─ Show outliers explicitly?
│      ├─ Yes, summary stats → Box Plot
│      └─ Yes, full shape → Violin Plot
│
├─→ EXPLORE RELATIONSHIPS
│   ├─ Two continuous variables → Scatter Plot
│   ├─ Too many points (>1000)?
│   │  ├─ Yes → Hexbin Plot
│   │  └─ Add third variable → Bubble Chart
│   │
│   ├─ Many variables (3-15)?
│   │  ├─ Linear relationships → Scatterplot Matrix
│   │  └─ Mixed types → Parallel Coordinates
│   │
│   └─ Network of connections?
│      ├─ <200 nodes → Force-Directed Graph
│      └─ >200 nodes → Consider filtering or matrix
│
├─→ SHOW COMPOSITION (PART-TO-WHOLE)
│   ├─ Simple composition (<6 parts) → Pie Chart (acceptable)
│   ├─ >6 parts → Bar Chart (sorted)
│   ├─ Hierarchical data?
│   │  ├─ Focus on proportions → Treemap
│   │  └─ Circular metaphor → Sunburst
│   │
│   └─ Show sequential contributions?
│      └─ Waterfall Chart
│
├─→ VISUALIZE FLOW OR PROCESS
│   ├─ Resource flow → Sankey Diagram
│   ├─ Circular relationships → Chord Diagram
│   ├─ Changes across stages → Alluvial Diagram
│   └─ Process steps → Flowchart
│
├─→ DISPLAY HIERARCHY
│   ├─ Space-efficient → Treemap
│   ├─ Radial/circular → Sunburst
│   ├─ Traditional tree → Dendrogram
│   ├─ Interactive depth → Drill-down Hierarchy
│   └─ Emphasis on clustering → Dendrogram with heatmap
│
├─→ SHOW GEOGRAPHIC PATTERNS
│   ├─ Regional aggregates → Choropleth Map
│   ├─ Point locations → Symbol Map
│   ├─ Movement/migration → Flow Map
│   └─ Density → Heat Map (geographic)
│
└─→ MULTIPLE PURPOSES OR COMPLEX STORY
    ├─ Consider dashboard with multiple charts
    ├─ Use small multiples for comparisons
    ├─ Add interactivity for exploration
    └─ Tell story with annotated sequence
```

---

### By Data Type

| Data Type | Recommended Visualizations |
|-----------|---------------------------|
| **Categorical** (nominal) | Bar chart, lollipop, treemap, word cloud (limited) |
| **Categorical** (ordinal) | Bar chart (sorted), slope graph, bullet chart |
| **Continuous** (single) | Histogram, density plot, box plot, violin plot |
| **Continuous** (two variables) | Scatter plot, hexbin, connected scatter, bubble chart |
| **Time series** (single) | Line chart, area chart, sparkline, annotated time series |
| **Time series** (multiple) | Small multiples, stacked area, stream graph |
| **Temporal events** | Timeline, Gantt chart, calendar heatmap |
| **Hierarchical** | Treemap, sunburst, dendrogram, icicle, circle packing |
| **Network/Graph** | Force-directed, arc diagram, chord, adjacency matrix |
| **Geographic** | Choropleth, symbol map, flow map, cartogram |
| **Text** | Word cloud (limited), bar chart of frequencies, network |
| **Multivariate** (3-15 dimensions) | Parallel coordinates, small multiples, radar, SPLOM |

---

### By Audience

| Audience | Recommended Approaches |
|----------|----------------------|
| **Executive/C-Suite** | Simple (bar, line, slope), heavily annotated, one insight per chart, high-level only |
| **General Public** | Familiar chart types, clear labels, avoid jargon, strong narrative |
| **Data Analysts** | Interactive, multiple views, access to raw data, standard statistical charts |
| **Scientists** | Rigorous (box, violin, scatter with CI), publication-ready, methodological transparency |
| **Designers** | Aesthetic considerations, experimental forms okay, but maintain clarity |
| **Domain Experts** | Can use specialized charts (candlestick for traders, Gantt for PM), assume domain knowledge |

---

## Part 6: Next Steps & Decision Framework

### Recommended Paths Forward

Based on the comprehensive research and planning completed, here are five strategic approaches to implementing this component library:

---

#### **Option A: Build Core Skill First** ⭐ *RECOMMENDED*

**Approach:**
1. Create main SKILL.md with comprehensive metadata and workflow
2. Build 5-10 reference files organized by chart category
3. Include color systems, accessibility standards, and interaction patterns
4. Provide decision trees and selection matrices
5. Add example datasets and code snippets

**Deliverables:**
- `SKILL.md` (trigger logic and quick start)
- `references/chart-types.md` (catalog of all 24+ methods)
- `references/color-systems.md` (palettes and accessibility)
- `references/interaction-patterns.md` (hover, click, zoom, etc.)
- `references/best-practices.md` (2024-2025 standards)
- `references/accessibility.md` (WCAG compliance guide)
- `assets/example-datasets/` (sample data for testing)

**Timeline:** 2-3 hours for comprehensive skill

**Benefits:**
- Provides complete framework from day one
- Claude can immediately start using systematic approach
- Progressive disclosure keeps token usage efficient
- Extensible foundation for future enhancements

**Best For:** 
- Creating reusable, long-term infrastructure
- Projects requiring systematic, principled approach
- When you want Claude to be self-sufficient in viz selection

---

#### **Option B: Create Exemplar Artifacts**

**Approach:**
1. Build 15-20 React artifacts demonstrating each major viz type
2. Create reusable component templates with props
3. Include extensive inline documentation
4. Provide working examples with real data
5. Focus on production-ready, copy-paste components

**Deliverables:**
- React components for each Tier 2 visualization
- Interactive examples with controls
- Storybook or documentation site
- TypeScript definitions
- CSS/styling examples

**Timeline:** 4-6 hours for full library

**Benefits:**
- Immediate, tangible components to use
- Learn by example approach
- Can copy-paste into projects
- Visual reference library

**Best For:**
- Developers who prefer code over documentation
- Projects with immediate component needs
- When showing is better than telling

---

#### **Option C: Hybrid Approach** 

**Approach:**
1. Start with SKILL.md framework (1 hour)
2. Build 5-7 exemplar artifacts for most-used types (2 hours)
3. Create reference docs for remaining methods (1 hour)
4. Focus on 80/20 rule - cover most common use cases deeply

**Deliverables:**
- Core SKILL.md with selection workflow
- React artifacts for: Bar, Line, Scatter, Treemap, Sankey, Small Multiples, Annotated Time Series
- Reference documentation for other 17+ methods
- Quick start guide

**Timeline:** 3-4 hours for essential coverage

**Benefits:**
- Balanced between documentation and code
- Quick wins with most common charts
- Comprehensive coverage without overbuilding
- Iterative improvement path

**Best For:**
- Projects wanting both guidance and examples
- When you need results quickly but want completeness
- Pragmatic, incremental approach

---

#### **Option D: Specialized Deep Dive**

**Approach:**
1. Choose a subdomain (e.g., "Financial Dashboards" or "Scientific Visualization")
2. Go ultra-deep on 8-10 related viz types
3. Include domain-specific patterns, examples, and best practices
4. Build specialized reference material
5. Create templates for common dashboard layouts

**Example Subdomains:**
- **Financial/Trading**: Candlestick, waterfall, bullet, sparklines, area charts
- **Scientific/Research**: Scatter, violin, box, parallel coords, heatmaps
- **Business Intelligence**: Bar, line, treemap, KPI cards, small multiples
- **Geographic/Spatial**: Choropleth, symbol maps, flow maps, hex binning
- **Network Analysis**: Force-directed, chord, sankey, arc diagrams

**Timeline:** 2-3 hours for specialized skill

**Benefits:**
- Deep domain expertise in one area
- Highly relevant for specific project types
- Can be expert-level quality in chosen domain
- Easier to maintain focus

**Best For:**
- Projects with clear domain focus
- When you need excellence in one area vs coverage of all areas
- Domain-specific consulting or product

---

#### **Option E: Iterative Research & Build**

**Approach:**
1. Build minimal viable skill (1 hour)
2. Test with Claude in real conversations
3. Identify gaps and pain points
4. Iterate based on actual usage
5. Expand organically over time

**Process:**
- Week 1: Basic SKILL.md with 5 chart types
- Week 2: Add interaction patterns based on usage
- Week 3: Expand to 10 chart types
- Week 4: Add specialized deep dives
- Ongoing: Refine based on real-world feedback

**Timeline:** Ongoing, starting with 1-hour base

**Benefits:**
- Learn what actually gets used
- No premature optimization
- Rapid iteration cycles
- Evolves with real needs

**Best For:**
- Experimental, learning-focused approach
- When requirements are unclear
- Agile, feedback-driven development
- Long-term projects

---

### Decision Matrix

Choose your path based on these factors:

| Factor | Option A | Option B | Option C | Option D | Option E |
|--------|----------|----------|----------|----------|----------|
| **Time Investment** | 2-3 hrs | 4-6 hrs | 3-4 hrs | 2-3 hrs | Ongoing |
| **Completeness** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ → ⭐⭐⭐⭐⭐ |
| **Immediate Usability** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Long-term Value** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Maintenance** | Low | Medium | Medium | Low | Variable |
| **Flexibility** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

### Recommendation

**For most use cases, I recommend Option C (Hybrid Approach)** because it:
- Provides immediate value with working components
- Establishes systematic framework for future expansion
- Balances documentation with practical examples
- Delivers 80% of value with 40% of effort
- Creates foundation for iterative improvement

**However, choose Option A if:**
- You want the most comprehensive, professional foundation
- Token efficiency and progressive disclosure are critical
- You're building a long-term, reusable asset
- You value systematic approach over quick examples

---

### Next Actions

**To proceed with Option C (Recommended Hybrid):**

1. **Hour 1: Core Framework**
   - Create SKILL.md with metadata and workflow
   - Build selection decision tree
   - Write quick start guide

2. **Hour 2-3: Exemplar Artifacts**
   - Bar Chart component (comparison)
   - Line Chart component (trends)
   - Scatter Plot component (relationships)
   - Treemap component (hierarchy)
   - Sankey component (flows)
   - Small Multiples pattern
   - Annotated Time Series example

3. **Hour 4: Reference Documentation**
   - Complete catalog of remaining 17+ methods
   - Color system guide
   - Accessibility checklist
   - Common mistakes to avoid

4. **Beyond: Iterate and Expand**
   - Add more artifacts based on usage
   - Refine selection logic
   - Include user feedback
   - Build advanced techniques

---

## Appendix

### Resources and Further Reading

**Data Visualization Books:**
- "The Visual Display of Quantitative Information" - Edward Tufte
- "Storytelling with Data" - Cole Nussbaumer Knaflic
- "The Functional Art" - Alberto Cairo
- "Information Dashboard Design" - Stephen Few

**Online Resources:**
- [From Data to Viz](https://www.data-to-viz.com/) - Classification of charts
- [The Data Visualisation Catalogue](https://datavizcatalogue.com/)
- [D3.js Gallery](https://observablehq.com/@d3/gallery)
- [Dataviz Project](https://datavizproject.com/)

**Best Practices:**
- [IBCS Standards](https://www.ibcs.com/) - International Business Communication Standards
- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/) - Web Content Accessibility Guidelines
- [Chartjunk](https://en.wikipedia.org/wiki/Chartjunk) - What to avoid

### Glossary

**Terms used in this document:**

- **Mark**: Basic geometric element (point, line, area, bar)
- **Encoding**: Mapping data to visual properties (position, size, color)
- **Faceting**: Creating small multiples by splitting data
- **Brushing**: Interactive selection of data ranges
- **Drill-down**: Navigation from summary to detail
- **Object constancy**: Maintaining element identity across transitions
- **Chartjunk**: Unnecessary decoration reducing clarity
- **Aspect ratio**: Width-to-height ratio affecting perception
- **Bin**: Range or bucket for grouping continuous data
- **Kernel density**: Smooth estimate of probability distribution

---

## Before Implementation: Library Validation

**Optional but Recommended:** Before implementing, see `../RESEARCH_GUIDE.md` for methodology to validate these library recommendations using available research tools (Google Search Grounding, Context7). This ensures you're using the latest, most secure versions.

**Note:** The recommendations below were researched comprehensively in November 2025 and are production-ready. Validation is optional.

---

## Recommended Libraries & Tools

### React Visualization Libraries (2025)

#### **Primary: Recharts** (Recommended for Most Use Cases)

**Library:** `/recharts/recharts`
**Trust Score:** 8.2/10
**Code Snippets:** 89+

**Why Recharts?**
- Composable React components (native React, not wrapper)
- Declarative API (easy to understand and maintain)
- Responsive by default (ResponsiveContainer)
- Good balance of features and simplicity
- Built on D3 (power of D3, ease of React)
- Excellent for business dashboards and standard charts

**When to Use:**
- Building business dashboards
- Need quick, professional charts
- Standard chart types (bar, line, pie, area)
- React-based projects
- Time-to-market is important

**Installation:**
```bash
npm install recharts
```

**Basic Example:**
```tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { name: 'Jan', value: 400 },
  { name: 'Feb', value: 300 },
  { name: 'Mar', value: 600 },
];

function MyChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="value" stroke="#8884d8" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

---

#### **Advanced: D3.js** (Maximum Flexibility)

**Library:** `/d3/d3`
**Trust Score:** 8/10
**Code Snippets:** 1,721+

**Why D3?**
- Maximum control and customization
- Industry standard for custom visualizations
- Handles any chart type imaginable
- Excellent for novel, unique visualizations
- Large ecosystem and community
- Animation and interaction capabilities

**When to Use:**
- Need custom, unique visualizations
- Recharts/Plotly don't support your use case
- Maximum control over every pixel
- Complex interactions required
- Novel chart types not in other libraries

**Trade-offs:**
- Steeper learning curve
- More code required
- Needs integration work with React

**Installation:**
```bash
npm install d3
```

**React Integration Pattern:**
```tsx
import * as d3 from 'd3';
import { useRef, useEffect } from 'react';

function D3Chart({ data }) {
  const svgRef = useRef();

  useEffect(() => {
    const svg = d3.select(svgRef.current);

    // D3 code here - full control
    svg.selectAll('circle')
      .data(data)
      .join('circle')
        .attr('cx', (d, i) => i * 30)
        .attr('cy', d => 200 - d)
        .attr('r', 5)
        .attr('fill', '#8884d8');
  }, [data]);

  return <svg ref={svgRef} width={600} height={400}></svg>;
}
```

---

#### **Alternative: Plotly.js** (Interactive & Scientific)

**Library:** `/plotly/plotly.js`
**Trust Score:** 8/10
**Code Snippets:** 49+

**Why Plotly?**
- Highly interactive out-of-the-box
- Excellent for scientific/technical charts
- 3D visualizations built-in
- Statistical chart types
- Export to PNG/SVG easily

**When to Use:**
- Scientific/research applications
- Need 3D charts
- Statistical visualizations (box plots, violin plots)
- Users need to zoom/pan/export charts
- Cross-platform (same API in Python, R, JavaScript)

**Installation:**
```bash
npm install plotly.js-dist-min
# Or for React wrapper:
npm install react-plotly.js
```

---

### Library Comparison Matrix

| Library | Ease of Use | Flexibility | Performance | Chart Types | Best For |
|---------|-------------|-------------|-------------|-------------|----------|
| **Recharts** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 15+ standard | Business dashboards |
| **D3.js** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Unlimited | Custom visualizations |
| **Plotly** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 40+ types | Scientific/3D |
| **Chart.js** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | 8 standard | Simple, lightweight |
| **Observable Plot** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 20+ types | Modern D3 successor |

---

### Accessibility Best Practices (WCAG 2.1)

Based on research, here are critical accessibility requirements for data visualizations:

**1. Text Alternatives (WCAG 1.1.1 Level A)**
```html
<!-- Simple chart -->
<figure role="img" aria-label="Sales increased 15% from Q3 to Q4">
  <svg>...</svg>
</figure>

<!-- Complex chart with long description -->
<figure role="img" aria-labelledby="chart-title" aria-describedby="chart-desc">
  <figcaption id="chart-title">Quarterly Sales 2024</figcaption>
  <svg>...</svg>
  <div id="chart-desc" class="sr-only">
    Sales started at $1.2M in Q1, dipped to $1.0M in Q2,
    recovered to $1.3M in Q3, and peaked at $1.5M in Q4,
    showing strong year-end performance.
  </div>
</figure>
```

**2. Color Contrast (WCAG 1.4.3 Level AA)**
- Non-text elements: 3:1 minimum
- Text: 4.5:1 minimum (or 3:1 for large text 24px+)

**Don't rely on color alone** - Use patterns/textures:
```tsx
// ✅ GOOD - Uses patterns + color
<Bar dataKey="sales" fill="url(#pattern1)" />
<Bar dataKey="costs" fill="url(#pattern2)" />

// Define patterns in SVG
<defs>
  <pattern id="pattern1" patternUnits="userSpaceOnUse" width="4" height="4">
    <path d="M-1,1 l2,-2 M0,4 l4,-4 M3,5 l2,-2" stroke="#8884d8" />
  </pattern>
</defs>
```

**3. Provide Data Tables**
```tsx
function AccessibleChart({ data }) {
  const [viewMode, setViewMode] = useState('chart');

  return (
    <div>
      <button onClick={() => setViewMode(viewMode === 'chart' ? 'table' : 'chart')}>
        {viewMode === 'chart' ? 'View as Table' : 'View as Chart'}
      </button>

      {viewMode === 'chart' ? (
        <LineChart data={data}>...</LineChart>
      ) : (
        <table>
          <caption>Sales Data</caption>
          <thead>
            <tr><th>Month</th><th>Sales</th></tr>
          </thead>
          <tbody>
            {data.map(row => (
              <tr key={row.month}>
                <td>{row.month}</td>
                <td>{row.sales}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
```

**4. Keyboard Navigation**
- Interactive charts must be keyboard accessible
- Tab through data points
- Enter/Space to activate tooltips
- Arrow keys to navigate between points

**5. Screen Reader Support**
```tsx
// Announce chart updates
<div role="status" aria-live="polite" aria-atomic="true">
  {isLoading ? 'Loading chart data...' : 'Chart updated with latest data'}
</div>
```

**6. Labels & Direct Labeling**
- Always label axes clearly
- Include units (%, $, etc.)
- Use direct labels on data points when possible (reduces cognitive load)
- Provide legends with clear icons

---

### Colorblind-Safe Palettes

**Recommended Palettes (from research):**

**IBM Color Palette (Colorblind-Safe):**
```javascript
const colorblindSafe = [
  '#648FFF', // Blue
  '#785EF0', // Purple
  '#DC267F', // Magenta
  '#FE6100', // Orange
  '#FFB000', // Yellow
];
```

**Paul Tol's Palette (Scientific):**
```javascript
const paulTol = [
  '#4477AA', // Blue
  '#EE6677', // Red
  '#228833', // Green
  '#CCBB44', // Yellow
  '#66CCEE', // Cyan
  '#AA3377', // Purple
  '#BBBBBB', // Grey
];
```

**Avoid:** Red/Green combinations (deuteranopia/protanopia can't distinguish)

**Test Tools:**
- Sim Daltonism (Mac)
- Color Oracle (Windows/Mac/Linux)
- Chromelens (Chrome extension)

---

### Performance Optimization

**Data Volume Guidelines:**

| Rows | Recommended Approach | Library Choice |
|------|---------------------|----------------|
| <1000 | Direct rendering | Recharts, Plotly |
| 1K-10K | Sampling/aggregation | D3 with optimization |
| 10K-100K | Canvas rendering | D3 (Canvas), Plotly (WebGL) |
| >100K | Server-side aggregation | Backend processing + simple viz |

**Optimization Techniques:**

**1. Use Canvas for Large Datasets** (>1000 points)
```tsx
// Recharts uses SVG (good for <1000 points)
// For >1000, switch to D3 with Canvas

const canvas = d3.select('canvas').node();
const context = canvas.getContext('2d');
// Draw using canvas API (60fps with 10K+ points)
```

**2. Sampling/Aggregation:**
```javascript
// Downsample to ~500 points for display
const sampledData = data.filter((_, i) => i % Math.ceil(data.length / 500) === 0);
```

**3. Virtualization for Charts:**
- Only render visible portion
- Load data chunks as user zooms/pans

---

### Recommendation by Use Case

**Business Dashboards → Recharts**
- Fast implementation
- Professional appearance
- Responsive out-of-box
- Easy maintenance

**Custom/Novel Visualizations → D3.js**
- Full control
- Unique designs
- Complex interactions
- Publication-quality

**Scientific/Technical → Plotly**
- 3D charts
- Statistical plots
- Interactive exploration
- Export capabilities

**Simple/Lightweight → Chart.js**
- Minimal bundle size
- Quick setup
- Basic chart types
- No React needed

---

## Styling & Theming

### Design Token Integration

All data visualization components use the **design-tokens** skill for visual styling, enabling consistent design, theme switching, and brand customization across all chart types.

**See:** `skills/design-tokens/` for complete theming documentation.

### Token Categories Used

**Color Tokens:**
- `--chart-color-primary` - Primary data series color
- `--chart-color-secondary` - Secondary data series color
- `--chart-color-accent` - Accent/highlight color
- `--chart-color-1` through `--chart-color-10` - Categorical color palette
- `--chart-axis-color` - Axis lines color
- `--chart-grid-color` - Grid lines color
- `--chart-label-color` - Axis labels and legends
- `--chart-tooltip-bg` - Tooltip background
- `--chart-tooltip-text` - Tooltip text color
- `--chart-tooltip-border` - Tooltip border color

**Spacing Tokens:**
- `--chart-padding` - Chart container padding
- `--chart-margin` - Space around chart
- `--chart-legend-gap` - Space between legend items
- `--chart-axis-label-gap` - Space between axis and labels

**Typography Tokens:**
- `--chart-font-family` - Chart text font
- `--chart-font-size-sm` - Small text (axis labels)
- `--chart-font-size-md` - Medium text (legends)
- `--chart-font-size-lg` - Large text (titles)
- `--chart-title-font-weight` - Chart title weight
- `--chart-label-font-weight` - Label text weight

**Border & Radius:**
- `--chart-border-radius` - Container corner radius
- `--chart-stroke-width` - Line chart stroke width
- `--chart-bar-border-radius` - Bar chart corner radius

**Shadow Tokens:**
- `--chart-shadow` - Chart container elevation
- `--chart-tooltip-shadow` - Tooltip shadow

**Motion Tokens:**
- `--chart-transition-duration` - Animation duration
- `--chart-transition-easing` - Animation easing function

### Component-Specific Tokens

```css
/* Chart Container */
--chart-bg: var(--color-white);
--chart-border-color: var(--color-border);
--chart-padding: var(--spacing-lg);
--chart-border-radius: var(--radius-md);
--chart-shadow: var(--shadow-md);

/* Color Scales */
--chart-color-primary: var(--color-primary);
--chart-color-secondary: var(--color-secondary);
--chart-color-accent: var(--color-accent);

/* Categorical Palette (10-color) */
--chart-color-1: #3B82F6;  /* Blue */
--chart-color-2: #10B981;  /* Green */
--chart-color-3: #F59E0B;  /* Orange */
--chart-color-4: #8B5CF6;  /* Purple */
--chart-color-5: #EF4444;  /* Red */
--chart-color-6: #14B8A6;  /* Teal */
--chart-color-7: #F97316;  /* Deep Orange */
--chart-color-8: #6366F1;  /* Indigo */
--chart-color-9: #EC4899;  /* Pink */
--chart-color-10: #84CC16; /* Lime */

/* Sequential Scales (for heatmaps, choropleths) */
--chart-sequential-1: var(--color-blue-100);
--chart-sequential-5: var(--color-blue-500);
--chart-sequential-9: var(--color-blue-900);

/* Diverging Scales (for positive/negative data) */
--chart-diverging-negative: var(--color-red-500);
--chart-diverging-neutral: var(--color-gray-200);
--chart-diverging-positive: var(--color-green-500);

/* Axes & Grid */
--chart-axis-color: var(--color-gray-700);
--chart-grid-color: var(--color-gray-200);
--chart-label-color: var(--color-text-secondary);
--chart-axis-stroke-width: 1px;
--chart-grid-stroke-width: 1px;

/* Tooltips */
--chart-tooltip-bg: var(--color-gray-900);
--chart-tooltip-text: var(--color-white);
--chart-tooltip-border-color: var(--color-gray-700);
--chart-tooltip-shadow: var(--shadow-lg);
--chart-tooltip-padding: var(--spacing-sm);
--chart-tooltip-border-radius: var(--radius-sm);

/* Typography */
--chart-font-family: var(--font-sans);
--chart-font-size-sm: var(--font-size-xs);
--chart-font-size-md: var(--font-size-sm);
--chart-font-size-lg: var(--font-size-base);
--chart-title-font-weight: var(--font-weight-semibold);

/* Animations */
--chart-transition-duration: var(--duration-normal);
--chart-transition-easing: var(--ease-out);
```

### Chart Type-Specific Tokens

**Bar Charts:**
```css
--bar-fill-color: var(--chart-color-primary);
--bar-stroke-color: transparent;
--bar-border-radius: var(--radius-sm);
--bar-hover-opacity: 0.8;
--bar-min-width: 4px;
```

**Line Charts:**
```css
--line-stroke-color: var(--chart-color-primary);
--line-stroke-width: 2px;
--line-point-radius: 4px;
--line-point-fill: var(--color-white);
--line-point-stroke: var(--chart-color-primary);
--line-area-opacity: 0.1;
```

**Pie/Donut Charts:**
```css
--pie-stroke-color: var(--color-white);
--pie-stroke-width: 2px;
--pie-hover-offset: 5px;
--donut-hole-radius: 50%;
```

**Scatter Plots:**
```css
--scatter-point-radius: 5px;
--scatter-point-opacity: 0.7;
--scatter-point-stroke-width: 0;
```

### Theme Support

- ✅ **Light Mode** - Clean, professional charts with subtle colors
- ✅ **Dark Mode** - Inverted color schemes, adjusted contrast
- ✅ **High Contrast** - Strong colors for accessibility
- ✅ **Print-Friendly** - Grayscale-optimized palettes
- ✅ **Colorblind-Safe** - Perceptually distinct color palettes
- ✅ **Custom Brand Themes** - Apply brand colors to all charts

### Example: Custom Chart Theming

```css
/* Brand-specific chart theme */
:root[data-theme="brand-charts"] {
  /* Use brand colors for data */
  --chart-color-primary: #FF6B35;      /* Brand Orange */
  --chart-color-secondary: #004E89;    /* Brand Blue */

  /* Categorical palette matching brand */
  --chart-color-1: #FF6B35;
  --chart-color-2: #004E89;
  --chart-color-3: #00A8E8;
  --chart-color-4: #FFA73B;

  /* Softer grid for cleaner look */
  --chart-grid-color: var(--color-gray-100);
  --chart-grid-stroke-width: 0.5px;

  /* Elevated charts */
  --chart-shadow: var(--shadow-xl);
  --chart-border-radius: var(--radius-lg);
}
```

### Dark Mode Considerations

```css
:root[data-theme="dark"] {
  --chart-bg: var(--color-gray-900);
  --chart-axis-color: var(--color-gray-400);
  --chart-grid-color: var(--color-gray-700);
  --chart-label-color: var(--color-gray-300);

  /* Adjusted categorical colors for dark bg */
  --chart-color-1: #60A5FA;  /* Lighter blue */
  --chart-color-2: #34D399;  /* Lighter green */
  --chart-color-3: #FBBF24;  /* Lighter orange */

  /* Tooltip on dark */
  --chart-tooltip-bg: var(--color-gray-800);
  --chart-tooltip-text: var(--color-gray-100);
  --chart-tooltip-border-color: var(--color-gray-600);
}
```

### Accessibility via Tokens

- **Colorblind-Safe Palettes**: Use perceptually distinct hues (blue/orange, not red/green)
- **High Contrast Mode**: Minimum 7:1 contrast ratio for chart elements
- **Texture/Pattern Support**: Add patterns to bars/areas for non-color differentiation
- **Focus Indicators**: Visible focus states for interactive chart elements
- **Reduced Motion**: Disable animations when `prefers-reduced-motion` is set

### Recommended Color Palettes

**Colorblind-Friendly (Categorical):**
- Uses blue/orange/green palette avoiding red/green confusion
- Safe for deuteranopia, protanopia, tritanopia

**Sequential (Heatmaps):**
- Single-hue progression (light → dark)
- Perceptually uniform (equal steps feel equal)

**Diverging (Positive/Negative):**
- Blue (negative) ← Gray (neutral) → Orange (positive)
- Avoid red/green for colorblind accessibility

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 10, 2025 | Initial comprehensive research and planning document |

---

## License

This research document is created for the purpose of building an AI-assisted component library. All visualization concepts are based on established data visualization practices and open-source community standards.

---

**END OF MASTER PLAN DOCUMENT**

---

*This document serves as the foundation for building a comprehensive, AI-assisted component library for data visualization. Use it as a reference for decision-making, implementation, and ongoing refinement of the visualization skill system.*